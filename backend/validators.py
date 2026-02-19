from config import Config
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """Validate file extension and filename safety"""
    if not filename or "." not in filename:
        return False
    
    # Prevent path traversal attacks
    safe_name = secure_filename(filename)
    if safe_name != filename:
        return False
    
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS


def validate_drug(drug):
    """Validate drug is in whitelist"""
    if not drug or not isinstance(drug, str):
        return False
    return drug.upper() in Config.DRUG_WHITELIST


def validate_patient_id(patient_id):
    """Validate patient ID format"""
    if not patient_id or not isinstance(patient_id, str):
        return False
    return len(patient_id.strip()) > 0


def validate_vcf_file(file):
    """Validate VCF file object"""
    if not file or file.filename == "":
        return False
    return allowed_file(file.filename)
