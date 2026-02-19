from vcf_parser import parse_vcf
from phenotype_mapper import determine_phenotype
from pgx_rules import evaluate_risk
from response_builder import build_response
import json

drug = "CODEINE"
patient_id = "PATIENT_001"

result = parse_vcf("test_sample.vcf")

if result["success"] and result["variants"]:

    variant = result["variants"][0]
    gene = variant["gene"]
    star = variant["star"]

    diplotype, phenotype = determine_phenotype(gene, star)

    risk_data = evaluate_risk(drug, phenotype)

    final_response = build_response(
        patient_id,
        drug,
        gene,
        diplotype,
        phenotype,
        variant,
        risk_data
    )

    print("\nFINAL JSON OUTPUT:\n")
    print(json.dumps(final_response, indent=2))
