# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime

Confidence = Literal["high", "medium", "low"]

class Field(BaseModel):
    value:      Optional[str] = None
    confidence: Confidence = "low"
    note:       Optional[str] = None

# ── INVOICE ──────────────────────────────────────────────────
class LineItem(BaseModel):
    description: Optional[str]   = None
    quantity:    Optional[float] = None
    unit_price:  Optional[float] = None
    total:       Optional[float] = None

class InvoiceSchema(BaseModel):
    vendor:         Field
    invoice_number: Field
    date:           Field
    due_date:       Field
    line_items:     List[LineItem] = []
    subtotal:       Field
    tax:            Field
    total:          Field
    currency:       Field

# ── RESUME ───────────────────────────────────────────────────
class ExperienceItem(BaseModel):
    company:     Optional[str] = None
    role:        Optional[str] = None
    duration:    Optional[str] = None
    description: Optional[str] = None

class EducationItem(BaseModel):
    institution: Optional[str] = None
    degree:      Optional[str] = None
    year:        Optional[str] = None

class ResumeSchema(BaseModel):
    name:       Field
    email:      Field
    phone:      Field
    location:   Field
    skills:     List[str] = []
    experience: List[ExperienceItem] = []
    education:  List[EducationItem] = []
    summary:    Field

# ── CONTRACT ─────────────────────────────────────────────────
class PartyItem(BaseModel):
    name:  Optional[str] = None
    role:  Optional[str] = None
    email: Optional[str] = None

class ContractSchema(BaseModel):
    contract_title:     Field
    contract_type:      Field
    effective_date:     Field
    expiry_date:        Field
    governing_law:      Field
    parties:            List[PartyItem] = []
    payment_terms:      Field
    termination_clause: Field
    confidentiality:    Field
    total_value:        Field

# ── REPORT / CUSTOM DOC ──────────────────────────────────────
class ReportSchema(BaseModel):
    title:           Field
    author:          Field
    date:            Field
    document_type:   Field
    organization:    Field
    summary:         Field
    key_findings:    List[str] = []
    recommendations: List[str] = []
    conclusion:      Field
    total_pages:     Field

# ── METADATA ─────────────────────────────────────────────────
class ExtractionRecord(BaseModel):
    id:            str
    filename:      str
    document_type: Literal["invoice", "resume", "contract", "report"]
    timestamp:     datetime
    result:        dict