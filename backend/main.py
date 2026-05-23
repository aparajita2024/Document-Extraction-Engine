# backend/main.py
import uuid, shutil, os, json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List
import pandas as pd
import io
from pdf_parser import extract_text
from extractor import extract_document
from database import init_db, save_extraction, list_extractions, get_extraction, update_extraction

app = FastAPI(title="Aurum Extraction Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

init_db()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

SUPPORTED_TYPES = {"invoice", "resume", "contract", "report"}
SUPPORTED_EXTS  = {".pdf", ".txt", ".docx", ".png", ".jpg", ".jpeg"}

@app.post("/extract")
async def extract(file: UploadFile = File(...), document_type: str = Form(...)):
    if document_type not in SUPPORTED_TYPES:
        raise HTTPException(400, f"document_type must be one of {SUPPORTED_TYPES}")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in SUPPORTED_EXTS:
        raise HTTPException(415, f"Unsupported file type '{ext}'.")

    file_id   = str(uuid.uuid4())
    save_path = f"{UPLOAD_DIR}/{file_id}{ext}"
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        raw_text = extract_text(save_path)
        result   = extract_document(raw_text, document_type)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except RuntimeError as e:
        raise HTTPException(502, str(e))
    finally:
        if os.path.exists(save_path):
            os.remove(save_path)

    save_extraction(file_id, file.filename, document_type, result)
    return {"id": file_id, "document_type": document_type,
            "filename": file.filename, "result": result}

@app.post("/extract/batch")
async def batch_extract(files: List[UploadFile] = File(...), document_type: str = Form(...)):
    if document_type not in SUPPORTED_TYPES:
        raise HTTPException(400, f"document_type must be one of {SUPPORTED_TYPES}")
    results = []
    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in SUPPORTED_EXTS:
            results.append({"filename": file.filename, "status": "error",
                            "message": f"Unsupported: {ext}"})
            continue
        file_id   = str(uuid.uuid4())
        save_path = f"{UPLOAD_DIR}/{file_id}{ext}"
        try:
            with open(save_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            raw_text = extract_text(save_path)
            result   = extract_document(raw_text, document_type)
            save_extraction(file_id, file.filename, document_type, result)
            results.append({"filename": file.filename, "status": "success",
                            "id": file_id, "result": result})
        except Exception as e:
            results.append({"filename": file.filename, "status": "error", "message": str(e)})
        finally:
            if os.path.exists(save_path):
                os.remove(save_path)
    return {"total": len(files), "results": results}

@app.get("/extractions")
def list_all():
    return list_extractions()

@app.get("/extractions/{id}")
def get_one(id: str):
    record = get_extraction(id)
    if not record:
        raise HTTPException(404, "Extraction not found")
    return record

@app.patch("/extractions/{id}/correct")
def correct_extraction(id: str, corrections: dict):
    record = get_extraction(id)
    if not record:
        raise HTTPException(404, "Extraction not found")
    result = record["result"]
    for field, value in corrections.items():
        if field in result:
            if isinstance(result[field], dict):
                result[field]["value"]      = value
                result[field]["confidence"] = "high"
                result[field]["note"]       = "Manually corrected"
            else:
                result[field] = value
    update_extraction(id, result)
    return {"id": id, "status": "updated", "result": result}

@app.get("/extractions/{id}/export")
def export_extraction(id: str, format: str = "csv"):
    record = get_extraction(id)
    if not record:
        raise HTTPException(404, "Extraction not found")
    result = record["result"]
    rows = []
    for field, val in result.items():
        if isinstance(val, dict):
            rows.append({"field": field, "value": val.get("value",""),
                         "confidence": val.get("confidence",""), "note": val.get("note","")})
        elif isinstance(val, list):
            for i, item in enumerate(val):
                rows.append({"field": f"{field}[{i}]", "value": str(item),
                             "confidence": "", "note": ""})
    df = pd.DataFrame(rows)
    if format == "csv":
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return StreamingResponse(io.BytesIO(output.getvalue().encode()), media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={id}.csv"})
    elif format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Extraction")
        output.seek(0)
        return StreamingResponse(output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={id}.xlsx"})
    else:
        raise HTTPException(400, "Format must be csv or excel")