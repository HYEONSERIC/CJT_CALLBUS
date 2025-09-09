from pydantic import BaseModel

class QuoteInitIn(BaseModel):
    customerType: str
    purpose: str

class QuoteOut(BaseModel):
    quoteId: str

    class Config:
        from_attributes = True
