# phenotype_mapper.py

import json
import os

# Load allele database from JSON
ALLELE_DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'allele_database.json')

def load_allele_database():
    """Load phenotype mappings from JSON database"""
    try:
        with open(ALLELE_DB_PATH, 'r') as f:
            db = json.load(f)
        return db.get('phenotype_mappings', {})
    except Exception as e:
        # Fallback to hardcoded mappings if file not found
        return {
            "CYP2D6": {
                "*1/*1": "NM",
                "*1/*4": "IM",
                "*4/*4": "PM",
                "*1/*2xN": "URM"
            },
            "CYP2C19": {
                "*1/*1": "NM",
                "*1/*2": "IM",
                "*2/*2": "PM"
            },
            "CYP2C9": {
                "*1/*1": "NM",
                "*1/*3": "IM",
                "*3/*3": "PM"
            }
        }

STAR_PHENOTYPE_MAP = load_allele_database()


def determine_phenotype(gene, star):
    """
    Map star alleles to metabolizer phenotypes.
    If only one star allele detected, assume homozygous (*4 -> *4/*4)
    
    Args:
        gene (str): Gene name (e.g., CYP2D6)
        star (str): Star allele designation (e.g., *1)
        
    Returns:
        tuple: (diplotype, phenotype) e.g., ("*4/*4", "PM")
    """
    if not star:
        return "Unknown", "Unknown"

    # Normalize input
    star = star.upper().strip()
    
    # Simulate diplotype if only one allele detected
    diplotype = f"{star}/{star}"

    gene_map = STAR_PHENOTYPE_MAP.get(gene, {})

    # Try exact match first
    phenotype_data = gene_map.get(diplotype)
    if isinstance(phenotype_data, dict):
        phenotype = phenotype_data.get("phenotype", "Unknown")
    else:
        phenotype = phenotype_data if phenotype_data else "Unknown"

    return diplotype, phenotype
