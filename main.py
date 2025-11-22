import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

# Database helpers
from database import db, create_document, get_documents

app = FastAPI(title="LVFRD API", description="Backend for Las Vegas Fire & Rescue public website")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "LVFRD Backend Running"}

# Schemas endpoint for Flames DB viewer
@app.get("/schema")
def get_schema():
    from schemas import Unit, Member, ContactInfo
    # Return models metadata as simple shapes for the viewer
    return {
        "unit": Unit.model_json_schema(),
        "member": Member.model_json_schema(),
        "contactinfo": ContactInfo.model_json_schema(),
    }

# Utility to convert ObjectId

def _stringify_ids(docs):
    for d in docs:
        if isinstance(d.get("_id"), ObjectId):
            d["id"] = str(d.pop("_id"))
    return docs

# Public endpoints

@app.get("/api/units")
def list_units():
    try:
        docs = get_documents("unit")
        return _stringify_ids(docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/units")
def create_unit(payload: dict):
    try:
        inserted_id = create_document("unit", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hierarchy")
def get_hierarchy():
    try:
        members = get_documents("member")
        return _stringify_ids(members)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/hierarchy")
def add_member(payload: dict):
    try:
        inserted_id = create_document("member", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/contact")
def get_contact():
    try:
        info = get_documents("contactinfo", limit=1)
        data = _stringify_ids(info)
        if data:
            return data[0]
        # default fallback if no record exists yet
        return {
            "department_name": "Las Vegas Fire & Rescue",
            "emergency": "911",
            "non_emergency": "(702) 229-2000",
            "address": "500 N Casino Center Blvd, Las Vegas, NV",
            "website": "https://www.lasvegasnevada.gov/Residents/Public-Safety/Fire",
            "email": "lvfrd@lasvegasnevada.gov",
            "social": [
                "https://twitter.com/LasVegasFD",
                "https://www.facebook.com/LasVegasFireRescue/",
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def set_contact(payload: dict):
    try:
        inserted_id = create_document("contactinfo", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
