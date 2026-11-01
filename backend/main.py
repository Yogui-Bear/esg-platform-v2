from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict

app = FastAPI(
    title="ESG Impact Platform 2.0 API",
    description="Motor open-source de medición de sostenibilidad y transformación competitiva para PYMEs",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ESGInputMetrics(BaseModel):
    company_name: str = Field(..., example="Industrias Sostenibles S.L.")
    cif: str = Field(..., example="B12345678")
    sector: str = Field(..., example="Manufactura")
    employees: int = Field(..., gt=0, example=45)
    renewable_energy_pct: float = Field(..., ge=0, le=100)
    recycling_rate_pct: float = Field(..., ge=0, le=100)
    has_carbon_footprint_plan: bool
    women_in_leadership_pct: float = Field(..., ge=0, le=100)
    permanent_contracts_pct: float = Field(..., ge=0, le=100)
    training_hours_per_employee: float = Field(..., ge=0)
    has_ethics_code: bool
    local_suppliers_pct: float = Field(..., ge=0, le=100)
    data_privacy_audited: bool

class ESGReportResponse(BaseModel):
    company_name: str
    cif: str
    scores: Dict[str, float]
    total_score: float
    rating: str
    sdg_alignment: List[str]
    action_plan: List[str]

@app.post("/api/v2/evaluate", response_model=ESGReportResponse)
def evaluate_company(data: ESGInputMetrics):
    recommendations, sdgs = [], []

    e_score = (data.renewable_energy_pct * 0.45) + (data.recycling_rate_pct * 0.35) + (20.0 if data.has_carbon_footprint_plan else 0.0)
    if data.renewable_energy_pct < 50:
        recommendations.append("Ambiental: Contratar energía con garantía de origen 100% renovable.")
    else:
        sdgs.append("ODS 7: Energía asequible y no contaminante")
    if not data.has_carbon_footprint_plan:
        recommendations.append("Ambiental: Registrar la huella de carbono (Alcance 1 y 2) en MITECO.")
    else:
        sdgs.append("ODS 13: Acción por el clima")

    training_score = min(data.training_hours_per_employee / 40.0, 1.0) * 20.0
    parity_score = max(0.0, (100.0 - abs(50.0 - data.women_in_leadership_pct) * 2) * 0.40)
    stability_score = data.permanent_contracts_pct * 0.40
    s_score = training_score + parity_score + stability_score

    if data.women_in_leadership_pct < 40:
        recommendations.append("Social: Implementar Plan de Igualdad en puestos directivos.")
    else:
        sdgs.append("ODS 5: Igualdad de género")
    if data.permanent_contracts_pct >= 85:
        sdgs.append("ODS 8: Trabajo decente y crecimiento económico")

    g_score = (35.0 if data.has_ethics_code else 0.0) + (data.local_suppliers_pct * 0.35) + (30.0 if data.data_privacy_audited else 0.0)
    if not data.has_ethics_code:
        recommendations.append("Gobernanza: Implantar canal ético conforme a la Ley 2/2023.")
    if not data.data_privacy_audited:
        recommendations.append("Gobernanza: Realizar auditoría RGPD vigente.")

    total = round((e_score * 0.40) + (s_score * 0.35) + (g_score * 0.25), 2)
    rating = "A+ (Líder ESG)" if total >= 85 else "A (Consolidado)" if total >= 70 else "B (En Transición)" if total >= 50 else "C (Riesgo ESG)"

    return ESGReportResponse(
        company_name=data.company_name,
        cif=data.cif,
        scores={"environmental": round(e_score, 2), "social": round(s_score, 2), "governance": round(g_score, 2)},
        total_score=total,
        rating=rating,
        sdg_alignment=sdgs or ["Sin alineación destacada aún"],
        action_plan=recommendations or ["Mantener políticas actuales y auditar anualmente."]
    )

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.0.0"}

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("../frontend/index.html")
