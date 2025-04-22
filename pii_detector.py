import re
from typing import List, Dict, Tuple

class PIIDetector:
    def __init__(self):
        self.patterns = {
            "full_name": r'(?:my name is|i am)\s([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)',
            "email": r'you can reach me at\s([A-Za-z0-9._%+-]+@[A-Za-z.-]+\.[A-Z|a-z]{2,})',
            "phone_number": r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            "dob": r'\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/(?:19|20)\d{2}\b',
            "aadhar_num": r'\b\d{4}[ -]?\d{4}[ -]?\d{4}\b',
            "credit_debit_no": r'\b(?:\d[ -]*?){13,16}\b',
            "cvv_no": r'\b\d{3,4}\b',
            "expiry_no": r'\b(?:0[1-9]|1[0-2])/?\d{2}\b'
        }
        
    def detect_pii(self, text: str) -> List[Dict]:
        pii_entities = []
        text_lower = text.lower()
        
        for entity_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text_lower):
                original_text = text[match.start():match.end()]
                if entity_type in ["full_name", "email"]:
                    # Extract only the name/email (not the prefix)
                    entity_match = re.search(r'([A-Za-z0-9._%+-]+@[A-Za-z.-]+\.[A-Z|a-z]{2,}|[A-Z][a-z]+(?:\s[A-Z][a-z]+)+)', original_text)
                    if entity_match:
                        pii_entities.append({
                            "position": [match.start() + entity_match.start(), match.start() + entity_match.end()],
                            "classification": entity_type,
                            "entity": entity_match.group()
                        })
                else:
                    pii_entities.append({
                        "position": [match.start(), match.end()],
                        "classification": entity_type,
                        "entity": original_text
                    })
        
        return sorted(pii_entities, key=lambda x: x["position"][0])
    
    def mask_text(self, text: str) -> Tuple[str, List[Dict]]:
        pii_entities = self.detect_pii(text)
        masked_text = text
        offset = 0
        masked_entities = []
        
        for entity in pii_entities:
            start, end = entity["position"]
            masked_entity = f"[{entity['classification']}]"
            
            # Adjust positions for previous replacements
            adjusted_start = start + offset
            adjusted_end = end + offset
            
            # Apply masking
            masked_text = masked_text[:adjusted_start] + masked_entity + masked_text[adjusted_end:]
            offset += len(masked_entity) - (end - start)
            
            masked_entities.append({
                "position": [adjusted_start, adjusted_start + len(masked_entity)],
                "classification": entity["classification"],
                "entity": entity["entity"]
            })
        
        return masked_text, masked_entities
