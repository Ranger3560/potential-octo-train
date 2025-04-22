from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from classifier import EmailClassifier
from pii_detector import PIIDetector
import joblib

app = FastAPI()

# Pydantic models for request/response
class EmailRequest(BaseModel):
    email_body: str

class PIIEntity(BaseModel):
    position: List[int]
    classification: str
    entity: str

class EmailResponse(BaseModel):
    input_email_body: str
    list_of_masked_entities: List[PIIEntity]
    masked_email: str
    category_of_the_email: str

# Initialize components
pii_detector = PIIDetector()
classifier = EmailClassifier()
classifier.load("email_classifier.joblib")  # Pre-trained model

@app.post("/classify_email", response_model=EmailResponse)
async def classify_email(request: EmailRequest):
    # Mask PII
    masked_email, masked_entities = pii_detector.mask_text(request.email_body)
    
    # Classify email
    category = classifier.predict(masked_email)
    
    return {
        "input_email_body": request.email_body,
        "list_of_masked_entities": masked_entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }

@app.get("/")
def health_check():
    return {"status": "API is running"}
