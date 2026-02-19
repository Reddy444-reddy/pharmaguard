import os

class Config:
    """Production configuration settings"""
    
    DEBUG = False
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {"vcf"}
    DRUG_WHITELIST = {
        "CODEINE",
        "WARFARIN", 
        "CLOPIDOGREL",
        "SIMVASTATIN",
        "AZATHIOPRINE",
        "FLUOROURACIL"
    }
    LOG_FILE = "audit.log"
    TEMP_DIR = "/tmp"
