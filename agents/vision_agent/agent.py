import base64
from pydantic import BaseModel, Field
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from backend.core.config import settings

class ExtractedDocumentData(BaseModel):
    document_id: str = Field(description="A unique identifier extracted from the document (e.g. invoice number)")
    document_type: str = Field(description="The type of document: invoice, receipt, etc.")
    amount: float = Field(description="The total amount of the transaction")
    currency: str = Field(description="The currency of the transaction (e.g. USD, EUR)")
    vendor: str = Field(description="The name of the vendor or company issuing the document")
    date: str = Field(description="The date on the document in YYYY-MM-DD format")
    
class VisionAgent:
    def __init__(self):
        # We assume OPENAI_API_KEY is available in the environment
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.structured_llm = self.llm.with_structured_output(ExtractedDocumentData)
        
    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def extract_from_image(self, image_path: str) -> ExtractedDocumentData:
        """
        Parses an image and returns structured JSON (validated by Pydantic).
        """
        base64_image = self._encode_image(image_path)
        
        prompt = "Extract the required fields from this document image. If a field is missing, infer it if possible or return a default reasonable value."
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ]
        )
        
        # Invoke the structured LLM
        # If parsing fails, LangChain structured output handles retries internally (depending on setup),
        # but we can also wrap this in a custom retry loop in LangGraph later.
        extracted_data = self.structured_llm.invoke([message])
        
        return extracted_data
