# phenotype_mapper.py

STAR_PHENOTYPE_MAP = {
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


def determine_phenotype(gene, star):
    """
    If only one star allele detected,
    assume homozygous (*4 -> *4/*4)
    """

    if not star:
        return "Unknown", "Unknown"

    # Simulate diplotype if only one allele detected
    diplotype = f"{star}/{star}"

    gene_map = STAR_PHENOTYPE_MAP.get(gene, {})

    phenotype = gene_map.get(diplotype, "Unknown")

    return diplotype, phenotype
