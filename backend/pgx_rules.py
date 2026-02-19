# pgx_rules.py

DRUG_GENE_MAP = {
    "CODEINE": "CYP2D6",
    "WARFARIN": "CYP2C9",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}


CPIC_RULES = {

    "CODEINE": {
        "PM": {
            "risk_label": "Ineffective",
            "severity": "moderate",
            "recommendation": "Avoid codeine. Consider morphine or non-opioid analgesics."
        },
        "URM": {
            "risk_label": "Toxic",
            "severity": "high",
            "recommendation": "Avoid codeine due to risk of respiratory depression."
        },
        "NM": {
            "risk_label": "Safe",
            "severity": "none",
            "recommendation": "Standard dosing recommended."
        }
    },

    "CLOPIDOGREL": {
        "PM": {
            "risk_label": "Ineffective",
            "severity": "high",
            "recommendation": "Use alternative antiplatelet therapy (e.g., prasugrel)."
        },
        "IM": {
            "risk_label": "Adjust Dosage",
            "severity": "moderate",
            "recommendation": "Consider alternative therapy or monitor closely."
        },
        "NM": {
            "risk_label": "Safe",
            "severity": "none",
            "recommendation": "Standard dosing."
        }
    },

    "WARFARIN": {
        "PM": {
            "risk_label": "Toxic",
            "severity": "high",
            "recommendation": "Reduce initial dose and monitor INR closely."
        },
        "IM": {
            "risk_label": "Adjust Dosage",
            "severity": "moderate",
            "recommendation": "Consider lower starting dose."
        },
        "NM": {
            "risk_label": "Safe",
            "severity": "none",
            "recommendation": "Standard dosing."
        }
    }

}


def evaluate_risk(drug, phenotype):

    drug = drug.upper()

    if drug not in CPIC_RULES:
        return {
            "risk_label": "Unknown",
            "severity": "low",
            "recommendation": "No CPIC guidance available."
        }

    drug_rules = CPIC_RULES[drug]

    return drug_rules.get(
        phenotype,
        {
            "risk_label": "Unknown",
            "severity": "low",
            "recommendation": "Phenotype not covered in CPIC guidance."
        }
    )
