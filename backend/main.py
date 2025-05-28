
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import pandas as pd

# Cargar datasets
equipos_df = pd.read_csv("catalogo_equipos.csv")
zonas_df = pd.read_csv("zonas_no_interconectadas.csv")

app = FastAPI(title="Plataforma de Microredes", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Home"])
def home():
    return HTMLResponse("<h1>Bienvenido a la API de Microredes Híbridas</h1>")

@app.get("/chatbot", tags=["Chatbot"])
def chatbot(query: str):
    query_lower = query.lower()
    if "solar" in query_lower:
        respuesta = "La energía solar es ideal para zonas con alta irradiación. ¿Sabías que muchas ZNI tienen gran potencial solar?"
    elif "eólica" in query_lower or "viento" in query_lower:
        respuesta = "La energía eólica puede complementar la solar en regiones con viento constante."
    elif "diesel" in query_lower:
        respuesta = "Los generadores diésel ofrecen respaldo confiable, pero tienen altos costos operativos."
    elif "baterías" in query_lower or "almacenamiento" in query_lower:
        respuesta = "Las baterías permiten autonomía nocturna o en días nublados. Existen varias tecnologías disponibles."
    else:
        respuesta = "Estoy aquí para ayudarte con microredes. Pregúntame sobre fuentes de energía, costos o configuraciones."
    return JSONResponse(content={"respuesta": respuesta})

@app.get("/simulador", tags=["Simulador"])
def simulador(location: str, consumo: float, fuente: str):
    zona = zonas_df[zonas_df["ubicacion"].str.contains(location, case=False)]
    if zona.empty:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    
    equipos_filtrados = equipos_df[equipos_df["tipo"].str.contains(fuente, case=False)]
    equipos_ordenados = equipos_filtrados.sort_values("capacidad", ascending=False).head(5)
    return {
        "ubicacion": zona.iloc[0].to_dict(),
        "equipos_sugeridos": equipos_ordenados.to_dict(orient="records")
    }
