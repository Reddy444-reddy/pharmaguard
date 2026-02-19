from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import tempfile
import os
import logging
from datetime import datetime
import uuid

from config import Config
from validators import allowed_file, validate_drug, validate_patient_id, validate_vcf_file
from error_handler import error_response, validation_error, server_error

from vcf_parser import parse_vcf
from phenotype_mapper import determine_phenotype
from pgx_rules import evaluate_risk
from response_builder import build_response

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Rate limiting setup
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Logging setup
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Request ID middleware for tracing
@app.before_request
def assign_request_id():
    """Assign unique ID to each request for audit tracing"""
    g.request_id = str(uuid.uuid4())
    logger.info(f"[{g.request_id}] {request.method} {request.path} from {get_remote_address()}")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/analyze", methods=["POST"])
@limiter.limit("20 per hour")
def analyze():
    """
    Main pharmacogenomic analysis endpoint.
    
    Expected POST parameters:
    - patient_id (str): Patient identifier
    - drug (str): Drug name
    - vcf_file (file): VCF format file
    
    Returns:
    - JSON response with risk assessment
    """
    
    try:
        # Validate patient_id
        patient_id = request.form.get("patient_id", "").strip()
        if not validate_patient_id(patient_id):
            logger.warning(f"[{g.request_id}] Invalid patient_id attempted")
            return validation_error("patient_id", "Patient ID is required and must be non-empty", g.request_id)
        
        # Validate drug
        drug = request.form.get("drug", "").strip()
        if not drug:
            logger.warning(f"Missing drug parameter for {patient_id}")
            return validation_error("drug", "Drug name is required")
        
        if not validate_drug(drug):
            logger.warning(f"Unsupported drug: {drug} for patient {patient_id}")
            return validation_error("drug", f"Drug '{drug}' is not supported. Supported drugs: {', '.join(Config.DRUG_WHITELIST)}")
        
        # Validate VCF file
        if "vcf_file" not in request.files:
            logger.warning(f"No VCF file provided for {patient_id}")
            return validation_error("vcf_file", "VCF file is required")
        
        file = request.files["vcf_file"]
        if not validate_vcf_file(file):
            logger.warning(f"Invalid file type for {patient_id}: {file.filename}")
            return validation_error("vcf_file", "File must be a .vcf file")
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > Config.MAX_CONTENT_LENGTH:
            logger.warning(f"File too large for {patient_id}: {file_size} bytes")
            return validation_error("vcf_file", f"File exceeds maximum size of {Config.MAX_CONTENT_LENGTH} bytes")
        
        # Process VCF file
        vcf_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".vcf", mode='wb') as tmp:
                vcf_path = tmp.name
                file.save(vcf_path)
            
            # Parse VCF
            parsed = parse_vcf(vcf_path)
            
            if not parsed["success"]:
                logger.error(f"VCF parsing failed for {patient_id}: {parsed.get('error')}")
                return server_error("VCF parsing failed")
            
            if not parsed["variants"] or len(parsed["variants"]) == 0:
                logger.warning(f"No target variants found for {patient_id}")
                return error_response("No target pharmacogenomic variants detected in VCF", 400)
            
            # Use first variant
            variant = parsed["variants"][0]
            gene = variant["gene"]
            star = variant["star"]
            
            # Determine phenotype
            diplotype, phenotype = determine_phenotype(gene, star)
            
            # Evaluate risk
            risk_data = evaluate_risk(drug, phenotype)
            
            # Build response
            final_response = build_response(
                patient_id,
                drug,
                gene,
                diplotype,
                phenotype,
                variant,
                risk_data
            )
            
            # Log successful analysis
            logger.info(
                f"[{g.request_id}] Analysis completed - Patient: {patient_id}, Drug: {drug}, "
                f"Gene: {gene}, Diplotype: {diplotype}, Phenotype: {phenotype}, "
                f"Risk: {risk_data['risk_label']}"
            )
            
            return jsonify(final_response), 200
        
        finally:
            # Clean up temporary file
            if vcf_path and os.path.exists(vcf_path):
                try:
                    os.remove(vcf_path)
                except Exception as e:
                    logger.warning(f"[{g.request_id}] Failed to delete temp file {vcf_path}: {e}")
    
    except Exception as e:
        logger.error(f"[{g.request_id}] Unexpected error during analysis: {str(e)}", exc_info=True)
        return server_error(f"Unexpected error: {str(e)}", g.request_id)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return error_response("Endpoint not found", 404)


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return error_response("Method not allowed", 405)


if __name__ == "__main__":
    logger.info("Starting PharmGuard API Server")
    app.run(host="0.0.0.0", port=5000, debug=False)
