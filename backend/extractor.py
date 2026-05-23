# backend/extractor.py
import os, json, re
from google import genai
from dotenv import load_dotenv
from schemas import InvoiceSchema, ResumeSchema, ContractSchema, ReportSchema

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

INVOICE_PROMPT = """
You are a precise document extraction engine. Extract structured data from the invoice text below.

RULES:
1. Return ONLY valid JSON — no markdown, no explanation.
2. For each scalar field, return: {{ "value": "...", "confidence": "high|medium|low", "note": null }}
   - high: value is clearly and explicitly stated
   - medium: value is inferred or partially visible
   - low: value is guessed or ambiguous
3. If a field is missing, return: {{ "value": null, "confidence": "low", "note": "Field not found in document" }}
4. NEVER hallucinate or invent values. If unsure, return null.
5. line_items: list of objects with description, quantity, unit_price, total.

Return this exact JSON structure:
{{
  "vendor":         {{"value": "", "confidence": "", "note": null}},
  "invoice_number": {{"value": "", "confidence": "", "note": null}},
  "date":           {{"value": "", "confidence": "", "note": null}},
  "due_date":       {{"value": "", "confidence": "", "note": null}},
  "line_items":     [],
  "subtotal":       {{"value": "", "confidence": "", "note": null}},
  "tax":            {{"value": "", "confidence": "", "note": null}},
  "total":          {{"value": "", "confidence": "", "note": null}},
  "currency":       {{"value": "", "confidence": "", "note": null}}
}}

DOCUMENT TEXT:
{text}
"""

RESUME_PROMPT = """
You are a precise document extraction engine. Extract structured data from the resume text below.

RULES:
1. Return ONLY valid JSON — no markdown, no explanation.
2. For each scalar field, return: {{ "value": "...", "confidence": "high|medium|low", "note": null }}
3. If a field is missing: {{ "value": null, "confidence": "low", "note": "Field not found in document" }}
4. NEVER hallucinate. If unsure, return null.
5. skills: flat list of strings. experience/education: list of structured objects.

Return this exact JSON structure:
{{
  "name":       {{"value": "", "confidence": "", "note": null}},
  "email":      {{"value": "", "confidence": "", "note": null}},
  "phone":      {{"value": "", "confidence": "", "note": null}},
  "location":   {{"value": "", "confidence": "", "note": null}},
  "skills":     [],
  "experience": [{{"company": "", "role": "", "duration": "", "description": ""}}],
  "education":  [{{"institution": "", "degree": "", "year": ""}}],
  "summary":    {{"value": "", "confidence": "", "note": null}}
}}

DOCUMENT TEXT:
{text}
"""

CONTRACT_PROMPT = """
You are a precise legal document extraction engine. Extract structured data from the contract below.

RULES:
1. Return ONLY valid JSON — no markdown, no explanation.
2. For each scalar field, return: {{ "value": "...", "confidence": "high|medium|low", "note": null }}
3. If a field is missing: {{ "value": null, "confidence": "low", "note": "Field not found in document" }}
4. NEVER hallucinate legal terms. If unsure, return null.
5. parties: list of objects with name, role, email.

Return this exact JSON structure:
{{
  "contract_title":      {{"value": "", "confidence": "", "note": null}},
  "contract_type":       {{"value": "", "confidence": "", "note": null}},
  "effective_date":      {{"value": "", "confidence": "", "note": null}},
  "expiry_date":         {{"value": "", "confidence": "", "note": null}},
  "governing_law":       {{"value": "", "confidence": "", "note": null}},
  "parties":             [{{"name": "", "role": "", "email": ""}}],
  "payment_terms":       {{"value": "", "confidence": "", "note": null}},
  "termination_clause":  {{"value": "", "confidence": "", "note": null}},
  "confidentiality":     {{"value": "", "confidence": "", "note": null}},
  "total_value":         {{"value": "", "confidence": "", "note": null}}
}}

DOCUMENT TEXT:
{text}
"""

REPORT_PROMPT = """
You are a precise document extraction engine. Extract structured data from the document below.
This could be any type of report, research paper, business document, or custom document.

RULES:
1. Return ONLY valid JSON — no markdown, no explanation.
2. For each scalar field, return: {{ "value": "...", "confidence": "high|medium|low", "note": null }}
3. If a field is missing: {{ "value": null, "confidence": "low", "note": "Field not found in document" }}
4. NEVER hallucinate. If unsure, return null.
5. key_findings and recommendations: flat list of strings.

Return this exact JSON structure:
{{
  "title":           {{"value": "", "confidence": "", "note": null}},
  "author":          {{"value": "", "confidence": "", "note": null}},
  "date":            {{"value": "", "confidence": "", "note": null}},
  "document_type":   {{"value": "", "confidence": "", "note": null}},
  "organization":    {{"value": "", "confidence": "", "note": null}},
  "summary":         {{"value": "", "confidence": "", "note": null}},
  "key_findings":    [],
  "recommendations": [],
  "conclusion":      {{"value": "", "confidence": "", "note": null}},
  "total_pages":     {{"value": "", "confidence": "", "note": null}}
}}

DOCUMENT TEXT:
{text}
"""

PROMPTS = {
    "invoice":  INVOICE_PROMPT,
    "resume":   RESUME_PROMPT,
    "contract": CONTRACT_PROMPT,
    "report":   REPORT_PROMPT,
}

SCHEMAS = {
    "invoice":  InvoiceSchema,
    "resume":   ResumeSchema,
    "contract": ContractSchema,
    "report":   ReportSchema,
}

def extract_document(text: str, doc_type: str) -> dict:
    """Send text to Gemini, parse JSON, validate with Pydantic."""
    if doc_type not in PROMPTS:
        raise ValueError(f"Unsupported document type: {doc_type}")

    prompt = PROMPTS[doc_type].format(text=text)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        raw = response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {e}")

    raw = re.sub(r"^```json\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"^```\s*",     "", raw, flags=re.MULTILINE)
    raw = re.sub(r"```$",        "", raw, flags=re.MULTILINE).strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw: {raw[:300]}")

    schema_class = SCHEMAS[doc_type]
    try:
        validated = schema_class(**parsed)
    except Exception as e:
        raise ValueError(f"Schema validation failed: {e}")

    return validated.model_dump()