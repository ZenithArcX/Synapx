"""
Routing Engine Module
Determines claim routing based on rules and extracted fields
"""
from typing import Dict, List, Any

class RoutingEngine:
    """Route claims to appropriate queues based on business rules"""
    
    # Damage threshold in dollars
    FAST_TRACK_THRESHOLD = 25000
    
    def __init__(self):
        self.route_history = []
    
    def determine_route(self, extracted_fields: Dict[str, Any], 
                       missing_fields: List[str], 
                       fraud_indicators: List[str]) -> Dict[str, str]:
        """
        Determine the recommended route for a claim
        
        Args:
            extracted_fields: Dictionary of extracted field values
            missing_fields: List of missing mandatory fields
            fraud_indicators: List of fraud-related keywords found
            
        Returns:
            Dictionary with recommended_route and reasoning
        """
        
        route = None
        reasoning = ""
        
        # Rule 1: Check for missing mandatory fields
        if missing_fields:
            route = "MANUAL_REVIEW"
            reasoning = f"Missing mandatory fields: {', '.join(missing_fields)}"
            return {"recommendedRoute": route, "reasoning": reasoning}
        
        # Rule 2: Check for fraud indicators
        if fraud_indicators:
            route = "INVESTIGATION_FLAG"
            reasoning = f"Potential fraud indicators detected: {', '.join(fraud_indicators)}"
            return {"recommendedRoute": route, "reasoning": reasoning}
        
        # Rule 3: Check for injury claims (specialist queue)
        claim_type = extracted_fields.get("claim_type", "").lower()
        if "injury" in claim_type or "bodily" in claim_type or "personal" in claim_type:
            route = "SPECIALIST_QUEUE"
            reasoning = "Claim type requires specialist handling (injury/bodily harm involved)"
            return {"recommendedRoute": route, "reasoning": reasoning}
        
        # Rule 4: Check damage amount for fast-track
        damage_value = extracted_fields.get("estimated_damage_value", 0)
        if damage_value < self.FAST_TRACK_THRESHOLD:
            route = "FAST_TRACK"
            reasoning = f"Low damage amount (${damage_value:,.2f} < ${self.FAST_TRACK_THRESHOLD:,}). Eligible for expedited processing."
        else:
            route = "STANDARD_REVIEW"
            reasoning = f"High damage amount (${damage_value:,.2f} >= ${self.FAST_TRACK_THRESHOLD:,}). Requires standard review."
        
        return {"recommendedRoute": route, "reasoning": reasoning}
    
    def get_all_routes(self) -> List[str]:
        """Get list of all possible routes"""
        return [
            "FAST_TRACK",
            "STANDARD_REVIEW",
            "MANUAL_REVIEW",
            "INVESTIGATION_FLAG",
            "SPECIALIST_QUEUE"
        ]
