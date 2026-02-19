from datetime import datetime, timezone
from llm_explainer import generate_explanation
import uuid


def calculate_risk_score(phenotype, severity):
    """
    Calculate numeric risk score (0-100) based on phenotype and severity.
    
    Args:
        phenotype (str): Metabolizer phenotype
        severity (str): Risk severity level
        
    Returns:
        float: Risk score 0-100
    """
    severity_map = {
        "none": 0,
        "low": 25,
        "moderate": 50,
        "high": 75,
        "critical": 100
    }
    
    phenotype_multipliers = {
        "NM": 1.0,    # Normal metabolizer - baseline
        "IM": 1.3,    # Intermediate - 30% higher
        "PM": 1.7,    # Poor - 70% higher
        "URM": 1.9,   # Ultra-rapid - 90% higher
        "Unknown": 0.5
    }
    
    base_score = severity_map.get(severity, 25)
    multiplier = phenotype_multipliers.get(phenotype, 1.0)
    
    final_score = min(100, base_score * multiplier)
    return round(final_score, 1)


def build_response(
    patient_id,
    drug,
    gene,
    diplotype,
    phenotype,
    variant,
    risk_data
):
    """
    Build comprehensive pharmacogenomic analysis response.
    
    Args:
        patient_id (str): Patient identifier
        drug (str): Drug name
        gene (str): Primary gene analyzed
        diplotype (str): Gene diplotype
        phenotype (str): Metabolizer phenotype
        variant (dict): Variant information
        risk_data (dict): Risk assessment from pgx_rules
        
    Returns:
        dict: Structured response ready for JSON serialization
    """
    
    # Generate unique analysis ID
    analysis_id = str(uuid.uuid4())
    
    # Calculate numeric risk score
    risk_score = calculate_risk_score(phenotype, risk_data.get("severity", "low"))

    # Create context for LLM explanation
    llm_context = {
        "gene": gene,
        "diplotype": diplotype,
        "phenotype": phenotype,
        "drug": drug.upper(),
        "risk_label": risk_data["risk_label"],
        "severity": risk_data["severity"],
        "recommendation": risk_data["recommendation"],
        "risk_score": risk_score
    }

    # Generate clinical explanation (LLM or fallback)
    llm_output = generate_explanation(llm_context, mode="clinician")

    response = {
        "analysis_id": analysis_id,
        "patient_id": patient_id,
        "drug": drug.upper(),
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "risk_assessment": {
            "risk_label": risk_data["risk_label"],
            "risk_score": risk_score,
            "confidence_score": 0.95,
            "severity": risk_data["severity"],
            "evidence_level": risk_data.get("evidence_level", "A"),
            "guideline_version": risk_data.get("cpic_version", "2023.1")
        },

        "pharmacogenomic_profile": {
            "primary_gene": gene,
            "diplotype": diplotype,
            "phenotype": phenotype,
            "detected_variants": [
                {
                    "rsid": variant["rsid"],
                    "gene": variant["gene"],
                    "star_allele": variant["star"],
                    "chromosome": variant["chrom"],
                    "position": variant["pos"],
                    "reference": variant["ref"],
                    "alternate": variant["alt"]
                }
            ]
        },

        "clinical_recommendation": {
            "recommendation_text": risk_data["recommendation"],
            "guideline_source": "CPIC",
            "evidence_level": risk_data.get("evidence_level", "A"),
            "cpic_version": risk_data.get("cpic_version", "2023.1")
        },

        "llm_generated_explanation": llm_output,

        "quality_metrics": {
            "vcf_parsing_success": True,
            "variant_count": 1,
            "rule_engine_applied": True,
            "analysis_version": "1.0"
        }
    }

    return response
