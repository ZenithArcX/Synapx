"""
Field Extraction Module for FNOL Claims
Extracts key information from claim documents
"""
import re
from typing import Dict, List, Any

class FieldExtractor:
    """Extract structured fields from FNOL documents"""
    
    # Define mandatory fields for validation
    MANDATORY_FIELDS = [
        "policy_number",
        "policyholder_name",
        "incident_date",
        "incident_location",
        "claim_type",
        "estimated_damage"
    ]
    
    # Field mapping patterns
    FIELD_PATTERNS = {
        "policy_number": r"(?:POLICY\s*(?:NUMBER|#)|POLICY_NUMBER)[:\s]*([0-9A-Za-z-]+)",
        "policyholder_name": r"(?:NAME\s*OF\s*INSURED|POLICYHOLDER\s*NAME)[:\s]*([^,\n]+)",
        "effective_date": r"(?:EFFECTIVE\s*DATE|COVERAGE\s*PERIOD)[:\s]*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})",
        "incident_date": r"(?:DATE\s*OF\s*(?:LOSS|ACCIDENT)|DATE)[:\s]*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})",
        "incident_time": r"(?:TIME)[:\s]*([0-9]{1,2}:[0-9]{2}\s*(?:AM|PM)?)",
        "incident_location": r"(?:LOCATION\s*OF\s*(?:LOSS|ACCIDENT)|STREET|ADDRESS|LOC)[:\s]*([^;\n]+?)(?=\n|;|$)",
        "city_state_zip": r"(?:CITY|CITY,\s*STATE)[:\s]*([^,\n]+(?:,[^,\n]+)*)",
        "claimant_name": r"(?:NAME\s*OF\s*(?:CLAIMANT|CONTACT)|CONTACT\s*NAME)[:\s]*([^,\n]+)",
        "third_party": r"(?:OTHER\s*(?:VEHICLE|PARTY)|THIRD\s*PARTY)[:\s]*([^\n]+)",
        "contact_phone": r"(?:(?:PRIMARY\s*|SECONDARY\s*)?PHONE)[:\s]*([0-9]{3}[.-]?[0-9]{3}[.-]?[0-9]{4})",
        "contact_email": r"(?:E-MAIL|EMAIL)[:\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
        "asset_type": r"(?:INSURED\s*VEHICLE|ASSET\s*TYPE)[:\s]*([^\n]+)",
        "vehicle_vin": r"(?:V\.I\.N\.|VIN)[:\s]*([A-HJ-NPR-Z0-9]{17})",
        "vehicle_plate": r"(?:PLATE\s*NUMBER)[:\s]*([A-Za-z0-9]{2,8})",
        "claim_type": r"(?:CLAIM\s*TYPE|LINE\s*OF\s*BUSINESS)[:\s]*([^\n]+)",
        "estimated_damage": r"(?:ESTIMATE\s*(?:AMOUNT|DAMAGE)|ESTIMATED\s*(?:DAMAGE|LOSS))[:\s]*\$?([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
        "accident_description": r"(?:DESCRIBE\s*(?:LOSS|ACCIDENT|DAMAGE)|DESCRIPTION)[:\s]*([^;]+(?:[;][^;]+)?)"
    }
    
    def __init__(self):
        pass
    
    def extract_fields(self, text: str) -> Dict[str, Any]:
        """
        Extract all fields from document text
        
        Args:
            text: Raw text from document
            
        Returns:
            Dictionary of extracted fields
        """
        extracted = {}
        
        for field_name, pattern in self.FIELD_PATTERNS.items():
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            if match:
                value = match.group(1).strip()
                extracted[field_name] = value
            else:
                extracted[field_name] = None
        
        # Fallback: If incident_location not found, try to extract from description
        if not extracted.get("incident_location") and extracted.get("accident_description"):
            desc = extracted["accident_description"].lower()
            # Look for common location keywords
            if "driveway" in desc:
                extracted["incident_location"] = "Driveway"
            elif "street" in desc:
                match = re.search(r"(\w+\s+street)", desc, re.IGNORECASE)
                if match:
                    extracted["incident_location"] = match.group(1).title()
            elif "parking" in desc:
                extracted["incident_location"] = "Parking lot/garage"
            elif "intersection" in desc:
                match = re.search(r"intersection\s+of\s+([^.]+)", desc, re.IGNORECASE)
                if match:
                    extracted["incident_location"] = match.group(1).title()
        
        # Clean up estimated damage (remove $ and commas)
        if extracted.get("estimated_damage"):
            try:
                extracted["estimated_damage_value"] = float(
                    extracted["estimated_damage"].replace(",", "").replace("$", "")
                )
            except ValueError:
                extracted["estimated_damage_value"] = 0
        else:
            extracted["estimated_damage_value"] = 0
        
        return extracted
    
    def validate_fields(self, extracted_fields: Dict[str, Any]) -> List[str]:
        """
        Identify missing mandatory fields
        
        Args:
            extracted_fields: Dictionary of extracted fields
            
        Returns:
            List of missing mandatory field names
        """
        missing = []
        
        # Placeholder values that indicate missing/invalid fields
        placeholder_values = ["not", "not provided", "n/a", "na", "unknown", "incomplete", "insufficient", "missing"]
        
        for field in self.MANDATORY_FIELDS:
            value = extracted_fields.get(field)
            
            # Check if field is missing or contains placeholder text
            if not value:
                missing.append(field)
            elif isinstance(value, str) and value.lower().strip() in placeholder_values:
                missing.append(field)
        
        return missing
    
    def check_for_fraud_indicators(self, text: str) -> List[str]:
        """
        Check for fraud-related keywords in document
        
        Args:
            text: Document text to analyze
            
        Returns:
            List of fraud indicators found
        """
        fraud_keywords = ["fraud", "inconsistent", "staged", "suspicious", "falsified"]
        indicators = []
        
        text_lower = text.lower()
        for keyword in fraud_keywords:
            if keyword in text_lower:
                indicators.append(keyword)
        
        return indicators
