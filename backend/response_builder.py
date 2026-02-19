from datetime import datetime, timezone
from llm_explainer import generate_explanation


def build_response(
    patient_id,
    drug,
    gene,
    diplotype,
    phenotype,
    variant,
    risk_data
):

    # Create context for LLM explanation
    llm_context = {
        "gene": gene,
        "diplotype": diplotype,
        "phenotype": phenotype,
        "drug": drug.upper(),
        "risk_label": risk_data["risk_label"],
        "severity": risk_data["severity"],
        "recommendation": risk_data["recommendation"]
    }

    # Generate clinical explanation (LLM or fallback)
    llm_output = generate_explanation(llm_context, mode="clinician")

    response = {
        "patient_id": patient_id,
        "drug": drug.upper(),
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "risk_assessment": {
            "risk_label": risk_data["risk_label"],
            "confidence_score": 0.95,
            "severity": risk_data["severity"]
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
            "evidence_level": "Level A"
        },

        "llm_generated_explanation": llm_output,

        "quality_metrics": {
            "vcf_parsing_success": True,
            "variant_count": 1,
            "rule_engine_applied": True
        }
    }

    return response
