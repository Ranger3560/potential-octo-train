from fastapi import FastAPI
from pydantic import BaseModel
from classifier import EmailClassifier
from pii_detector import PIIDetector
import joblib

app = FastAPI()

# Pydantic models
class EmailRequest(BaseModel):
    email_body: str

class EmailResponse(BaseModel):
    input_email_body: str
    list_of_masked_entities: list
    masked_email: str
    category_of_the_email: str

# Initialize components
classifier = EmailClassifier()
# Instead of classifier.load_model(), call classifier.load()
classifier.load("email_classifier.joblib")  # Load the model using classifier.load()
pii_detector = PIIDetector()

@app.post("/classify_email", response_model=EmailResponse)
async def classify_email(request: EmailRequest):
    # Step 1: Mask PII
    masked_email, entities = pii_detector.mask_pii(request.email_body)
    
    # Step 2: Classify email
    category = classifier.model.predict([masked_email])[0] # make prediction using the loaded model.
    
    return {
        "input_email_body": request.email_body,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }
