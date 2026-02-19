TARGET_GENES = [
    "CYP2D6",
    "CYP2C19",
    "CYP2C9",
    "SLCO1B1",
    "TPMT",
    "DPYD"
]

def parse_vcf(file_path):
    """
    Parse VCF file with defensive error handling.
    
    Args:
        file_path (str): Path to VCF file
        
    Returns:
        dict: {success: bool, variants: list, error: str}
    """
    try:
        variants = []
        line_count = 0
        
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines and headers
                if not line or line.startswith('##') or line.startswith('#'):
                    continue
                
                line_count += 1
                
                try:
                    # Parse VCF data line
                    fields = line.split('\t')
                    if len(fields) < 8:
                        continue
                    
                    chrom, pos, rsid, ref, alt, qual, filt, info = fields[:8]
                    
                    # Validate chromosome
                    if not chrom or not chrom.startswith(('chr', '1', '2', '3', '4', '5', '6', 
                                                          '7', '8', '9', 'X', 'Y', 'M')):
                        continue
                    
                    # Safely parse position
                    try:
                        pos_int = int(pos)
                    except ValueError:
                        continue
                    
                    # Parse INFO field defensively
                    info_dict = {}
                    if info and info != ".":
                        for item in info.split(';'):
                            if '=' in item:
                                key, value = item.split('=', 1)
                                info_dict[key] = value
                    
                    gene = info_dict.get("GENE", "").upper()
                    star = info_dict.get("STAR", "").upper() if info_dict.get("STAR") else None
                    
                    # Only include variants for target genes
                    if gene and gene in TARGET_GENES:
                        variants.append({
                            "gene": gene,
                            "rsid": rsid if rsid != "." else None,
                            "star": star,
                            "chrom": chrom,
                            "pos": pos_int,
                            "ref": ref,
                            "alt": alt.split(',') if alt != "." else []
                        })
                
                except Exception as line_error:
                    # Log malformed line but continue processing
                    continue
        
        return {
            "success": True,
            "variants": variants,
            "lines_processed": line_count
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": f"VCF file not found: {file_path}",
            "lines_processed": 0
        }
    
    except IOError as e:
        return {
            "success": False,
            "error": f"Error reading VCF file: {str(e)}",
            "lines_processed": 0
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error parsing VCF: {str(e)}",
            "lines_processed": 0
        }
