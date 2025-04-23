import re
from typing import List, Dict, Tuple

class PIIDetector:
    def __init__(self):
        self.patterns = {
            "full_name": r'(?:my name is|i am)\s([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)',
            "email": r'you can reach me at\s([A-Za-z0-9._%+-]+@[A-Za-z.-]+\.[A-Z|a-z]{2,})',
            "phone_number": r"(?:(?:\+?\d{1,3}[- ]?)?(?:\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}))\b",
            "dob": r"\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12][0-9]|3[01])[/-](?:19|20)\d{2}\b",
            "aadhar_num": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
            "cvv_no": r"\b\d{3,4}\b",
            "expiry_no": r"\b(0[1-9]|1[0-2])/?(?:\d{2}|\d{4})\b",
        }

    def mask_pii(self, text: str) -> Tuple[str, List[Dict]]:
        """Detect and mask PII entities"""
        entities = []
        masked_text = text
        
        for entity_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    "position": [match.start(), match.end()],
                    "classification": entity_type,
                    "entity": match.group()
                })
        
        # Mask entities in reverse order to preserve positions
        for entity in sorted(entities, key=lambda x: -x['position'][0]):
            masked_text = (
                masked_text[:entity['position'][0]] + 
                f"[{entity['classification']}]" + 
                masked_text[entity['position'][1]:]
            )
        
        return masked_text, entities
