TARGET_GENES = [
    "CYP2D6",
    "CYP2C19",
    "CYP2C9",
    "SLCO1B1",
    "TPMT",
    "DPYD"
]

def parse_vcf(file_path):
    try:
        variants = []
        
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines and headers
                if not line or line.startswith('##') or line.startswith('#'):
                    continue
                
                # Parse VCF data line
                fields = line.split('\t')
                if len(fields) < 8:
                    continue
                
                chrom, pos, rsid, ref, alt, qual, filt, info = fields[:8]
                
                # Parse INFO field
                info_dict = {}
                for item in info.split(';'):
                    if '=' in item:
                        key, value = item.split('=', 1)
                        info_dict[key] = value
                
                gene = info_dict.get("GENE")
                star = info_dict.get("STAR")
                
                if gene and gene in TARGET_GENES:
                    variants.append({
                        "gene": gene,
                        "rsid": rsid,
                        "star": star,
                        "chrom": chrom,
                        "pos": int(pos),
                        "ref": ref,
                        "alt": alt.split(',')
                    })
        
        return {
            "success": True,
            "variants": variants
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
