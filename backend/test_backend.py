"""
Unit tests for PharmaGuard backend modules
"""

import pytest
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))


class TestValidators:
    """Test input validation functions"""
    
    def test_allowed_file_valid_vcf(self):
        """Test that VCF files are accepted"""
        from backend.validators import allowed_file
        assert allowed_file("test.vcf") is True
    
    def test_allowed_file_invalid_extension(self):
        """Test that non-VCF files are rejected"""
        from backend.validators import allowed_file
        assert allowed_file("test.txt") is False
        assert allowed_file("test.vcf.bak") is False
    
    def test_allowed_file_path_traversal(self):
        """Test that path traversal attempts are blocked"""
        from backend.validators import allowed_file
        assert allowed_file("../../../etc/passwd.vcf") is False
        assert allowed_file("..\\..\\..\\windows\\system32.vcf") is False
    
    def test_validate_drug_valid(self):
        """Test valid drug validation"""
        from backend.validators import validate_drug
        assert validate_drug("CODEINE") is True
        assert validate_drug("codeine") is True
        assert validate_drug("Warfarin") is True
    
    def test_validate_drug_invalid(self):
        """Test invalid drug validation"""
        from backend.validators import validate_drug
        assert validate_drug("INVALID_DRUG") is False
        assert validate_drug("") is False
        assert validate_drug(None) is False
    
    def test_validate_patient_id(self):
        """Test patient ID validation"""
        from backend.validators import validate_patient_id
        assert validate_patient_id("P12345") is True
        assert validate_patient_id("") is False
        assert validate_patient_id(None) is False


class TestPhenotypeMapper:
    """Test phenotype mapping"""
    
    def test_cyp2d6_mapping(self):
        """Test CYP2D6 phenotype mapping"""
        from backend.phenotype_mapper import determine_phenotype
        
        diplotype, phenotype = determine_phenotype("CYP2D6", "*1")
        assert diplotype == "*1/*1"
        assert phenotype == "NM"
        
        diplotype, phenotype = determine_phenotype("CYP2D6", "*4")
        assert diplotype == "*4/*4"
        assert phenotype == "PM"
    
    def test_unknown_phenotype(self):
        """Test handling of unknown star alleles"""
        from backend.phenotype_mapper import determine_phenotype
        
        diplotype, phenotype = determine_phenotype("CYP2D6", None)
        assert phenotype == "Unknown"
        assert diplotype == "Unknown"


class TestPgxRules:
    """Test pharmacogenomic rule engine"""
    
    def test_codeine_pm_risk(self):
        """Test Codeine PM risk assessment"""
        from backend.pgx_rules import evaluate_risk
        
        result = evaluate_risk("CODEINE", "PM")
        assert result["risk_label"] == "Ineffective"
        assert result["severity"] == "moderate"
        assert "evidence_level" in result
        assert "cpic_version" in result
    
    def test_warfarin_im_risk(self):
        """Test Warfarin IM risk assessment"""
        from backend.pgx_rules import evaluate_risk
        
        result = evaluate_risk("WARFARIN", "IM")
        assert result["risk_label"] == "Adjust Dosage"
        assert result["severity"] == "moderate"
    
    def test_unknown_drug(self):
        """Test handling of unsupported drugs"""
        from backend.pgx_rules import evaluate_risk
        
        result = evaluate_risk("UNKNOWN_DRUG", "NM")
        assert result["risk_label"] == "Unknown"
        assert result["evidence_level"] == "D"


class TestResponseBuilder:
    """Test response builder"""
    
    def test_calculate_risk_score(self):
        """Test risk score calculation"""
        from backend.response_builder import calculate_risk_score
        
        # Normal metabolizer, no severity
        score = calculate_risk_score("NM", "none")
        assert score == 0.0
        
        # Poor metabolizer, high severity
        score = calculate_risk_score("PM", "high")
        assert 50 < score <= 100
        
        # Ultra-rapid metabolizer, high severity
        score = calculate_risk_score("URM", "high")
        assert score > 70


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
