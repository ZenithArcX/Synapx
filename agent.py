"""
Main Claims Processing Agent
Orchestrates the claim extraction, validation, and routing process
"""
import json
from typing import Dict, Any, List
from pathlib import Path
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pdf_parser import DocumentParser
from field_extractor import FieldExtractor
from routing_engine import RoutingEngine


class ClaimsProcessingAgent:
    """Main agent for processing insurance claims"""
    
    def __init__(self):
        self.parser = DocumentParser()
        self.extractor = FieldExtractor()
        self.router = RoutingEngine()
        self.processed_count = 0
    
    def process_claim(self, document_path: str) -> Dict[str, Any]:
        """
        Process a single claim document
        
        Args:
            document_path: Path to the claim document (PDF or TXT)
            
        Returns:
            Dictionary with extracted fields, missing fields, and routing decision
        """
        
        # Step 1: Parse the document
        try:
            document_text = self.parser.parse_document(document_path)
        except Exception as e:
            return {
                "error": str(e),
                "status": "FAILED",
                "extractedFields": {},
                "missingFields": self.extractor.MANDATORY_FIELDS,
                "recommendedRoute": "MANUAL_REVIEW",
                "reasoning": f"Document parsing failed: {str(e)}"
            }
        
        # Step 2: Extract fields
        extracted_fields = self.extractor.extract_fields(document_text)
        
        # Step 3: Validate fields (identify missing mandatory fields)
        missing_fields = self.extractor.validate_fields(extracted_fields)
        
        # Step 4: Check for fraud indicators
        fraud_indicators = self.extractor.check_for_fraud_indicators(document_text)
        
        # Step 5: Determine routing
        routing_decision = self.router.determine_route(
            extracted_fields, 
            missing_fields, 
            fraud_indicators
        )
        
        # Step 6: Build result
        result = {
            "status": "SUCCESS",
            "document_path": document_path,
            "extractedFields": self._clean_extracted_fields(extracted_fields),
            "missingFields": missing_fields,
            "fraudIndicators": fraud_indicators,
            "recommendedRoute": routing_decision["recommendedRoute"],
            "reasoning": routing_decision["reasoning"]
        }
        
        self.processed_count += 1
        return result
    
    def process_multiple_claims(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Process multiple claim documents from a directory
        
        Args:
            directory_path: Path to directory containing claim documents
            
        Returns:
            List of processing results
        """
        results = []
        
        if not os.path.isdir(directory_path):
            raise ValueError(f"Directory not found: {directory_path}")
        
        # Process all supported file types
        supported_files = []
        for ext in self.parser.SUPPORTED_FORMATS:
            supported_files.extend(Path(directory_path).glob(f"*{ext}"))
        
        if not supported_files:
            print(f"No documents found in {directory_path}")
            return results
        
        for file_path in supported_files:
            print(f"Processing: {file_path.name}...")
            result = self.process_claim(str(file_path))
            results.append(result)
        
        return results
    
    def _clean_extracted_fields(self, extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
        """Remove None values and internal fields from extracted fields"""
        return {k: v for k, v in extracted_fields.items() 
                if v is not None and not k.endswith("_value")}
    
    def save_results(self, results: List[Dict[str, Any]], output_path: str) -> None:
        """
        Save processing results to JSON file
        
        Args:
            results: List of processing results
            output_path: Path to save the JSON file
        """
        directory = os.path.dirname(output_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Results saved to: {output_path}")
    
    def print_summary(self, results: List[Dict[str, Any]]) -> None:
        """Print summary of processing results"""
        print("\n" + "="*60)
        print(f"CLAIMS PROCESSING SUMMARY")
        print("="*60)
        print(f"Total documents processed: {len(results)}")
        
        # Count by route
        routes = {}
        for result in results:
            route = result.get("recommendedRoute", "UNKNOWN")
            routes[route] = routes.get(route, 0) + 1
        
        print("\nRouting Distribution:")
        for route, count in sorted(routes.items()):
            print(f"  {route}: {count}")
        
        print("="*60 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Insurance Claims Processing Agent - Extract and route FNOL claims"
    )
    parser.add_argument(
        "-i", "--input",
        help="Input file or directory path",
        required=True
    )
    parser.add_argument(
        "-o", "--output",
        help="Output JSON file path",
        default="output/claims_processing_results.json"
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = ClaimsProcessingAgent()
    
    # Process claims
    if os.path.isfile(args.input):
        # Single file
        result = agent.process_claim(args.input)
        results = [result]
    elif os.path.isdir(args.input):
        # Directory
        results = agent.process_multiple_claims(args.input)
    else:
        print(f"Error: {args.input} is not a valid file or directory")
        return
    
    # Save results
    agent.save_results(results, args.output)
    
    # Print summary
    agent.print_summary(results)
    
    # Print detailed results
    print("\nDETAILED RESULTS:")
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
