# pgx_rules.py

DRUG_GENE_MAP = {
    "CODEINE": "CYP2D6",
    "WARFARIN": "CYP2C9",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}

# CPIC Guideline version tracking
CPIC_VERSION = "2023.1"
EVIDENCE_LEVELS = {
    "A": "Strong evidence for phenotype-guided dosing",
    "B": "Moderate evidence for phenotype-guided dosing",
    "C": "Optional phenotype-guided dosing",
    "D": "No evidence for phenotype-guided dosing"
}

CPIC_RULES = {

    "CODEINE": {
        "evidence_level": "A",
        "cpic_version": "2023.1",
        "PM": {
            "risk_label": "Ineffective",
            "severity": "moderate",
            "recommendation": "Avoid codeine. Consider morphine or non-opioid analgesics.",
            "evidence_level": "A"
        },
        "URM": {
            "risk_label": "Toxic",
            "severity": "high",
            "recommendation": "Avoid codeine due to risk of respiratory depression.",
            "evidence_level": "A"
        },
        "IM": {
            "risk_label": "Reduced Effect",
            "severity": "low",
            "recommendation": "Consider alternative analgesics.",
            "evidence_level": "A"
        },
        "NM": {
            "risk_label": "Safe",
            "severity": "none",
            "recommendation": "Standard dosing recommended.",
            "evidence_level": "A"
        }
    },

    "CLOPIDOGREL": {
        "evidence_level": "A",
        "cpic_version": "2023.1",
        "PM": {
            "risk_label": "Ineffective",
            "severity": "high",
            "recommendation": "Use alternative antiplatelet therapy (e.g., prasugrel, ticagrelor).",
            "evidence_level": "A"
        },
        "IM": {
            "risk_label": "Adjust Dosage",
            "severity": "moderate",
            "recommendation": "Consider alternative therapy or high-intensity dosing with close monitoring.",
            "evidence_level": "A"
        },
        "NM": {
            "risk_label": "Safe",
            "severity": "none",
            "recommendation": "Standard dosing.",
            "evidence_level": "A"
        }
    },

    "WARFARIN": {
        "evidence_level": "A",
        "cpic_version": "2023.1",
        "PM": {
            "risk_label": "Toxic",
            "severity": "high",
            "recommendation": "Reduce initial dose (typically 25-50% of standard) and monitor INR closely.",
            "evidence_level": "A"
        },
        "IM": {
            "risk_label": "Adjust Dosage",
            "severity": "moderate",
            "recommendation": "Consider lower starting dose and titrate based on INR response.",
            "evidence_level": "A"
        },
        "NM": {
            "risk_label": "Safe",
            "severity": "none",
            "recommendation": "Standard dosing with regular INR monitoring.",
            "evidence_level": "A"
        }
    }

}


def evaluate_risk(drug, phenotype):
    """
    Evaluate pharmacogenomic risk based on drug and phenotype.
    
    Args:
        drug (str): Drug name
        phenotype (str): Metabolizer phenotype (NM, IM, PM, URM)
        
    Returns:
        dict: Risk assessment with evidence level and CPIC version
    """
    drug = drug.upper()

    if drug not in CPIC_RULES:
        return {
            "risk_label": "Unknown",
            "severity": "low",
            "recommendation": "No CPIC guidance available.",
            "evidence_level": "D",
            "cpic_version": CPIC_VERSION
        }

    drug_rules = CPIC_RULES[drug]
    
    # Get phenotype-specific rules
    phenotype_rules = drug_rules.get(
        phenotype,
        {
            "risk_label": "Unknown",
            "severity": "low",
            "recommendation": "Phenotype not covered in CPIC guidance.",
            "evidence_level": "D"
        }
    )
    
    # Add CPIC metadata if not present
    if "cpic_version" not in phenotype_rules:
        phenotype_rules["cpic_version"] = CPIC_VERSION
    
    if "evidence_level" not in phenotype_rules and "evidence_level" in drug_rules:
        phenotype_rules["evidence_level"] = drug_rules["evidence_level"]
    
    return phenotype_rules
