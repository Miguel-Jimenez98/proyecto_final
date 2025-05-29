from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import pandas as pd
import math
import spacy

# Cargar modelo spaCy español
nlp = spacy.load("es_core_news_md")

# Datos
equipos_df = pd.read_csv("catalogo_equipos.csv")
zonas_df = pd.read_csv("zonas_no_interconectadas.csv")
equipos_df["Capacidad_num"] = equipos_df["Capacidad"].str.extract(r'(\d+)').astype(int)

# Preguntas semánticas
faq_semanticas = {
    "¿Qué es una microred híbrida?": "Una microred híbrida combina varias fuentes de energía (solar, eólica, diésel, etc.) para asegurar un suministro estable, especialmente útil en zonas aisladas.",
    "¿Qué tipo de batería me conviene?": "Las baterías de litio tienen mayor vida útil y eficiencia, pero son más costosas. Las de plomo-ácido son más económicas, pero requieren más mantenimiento.",
    "¿Cuál es la diferencia entre litio y plomo ácido?": "Las baterías de litio son más ligeras, duran más y requieren menos mantenimiento. Las de plomo-ácido son más baratas pero menos duraderas.",
    "¿Qué inversor necesito si consumo 6 kWh diarios?": "Depende del tipo de carga y si usarás energía solar, eólica u otra. En general, necesitarías un inversor de al menos 3 kW y que sea compatible con tu sistema de baterías.",
    
    # Nuevas preguntas y respuestas
    "¿Qué es la energía geotérmica?": "La energía geotérmica aprovecha el calor interno de la Tierra para generar electricidad o calefacción. Es una fuente renovable constante y de baja emisión de CO₂, aunque su instalación puede ser costosa.",
    "¿Qué es la energía undimotriz?": "La energía undimotriz convierte el movimiento de las olas del mar en electricidad mediante dispositivos como boyas o plataformas. Es una fuente renovable con gran potencial en zonas costeras.",
    "¿Qué es la energía mareomotriz?": "La energía mareomotriz utiliza el movimiento de las mareas para generar electricidad, generalmente mediante turbinas instaladas en estuarios o bahías con gran amplitud de marea.",
    "¿Qué es la energía azul?": "La energía azul, o energía osmótica, se obtiene por la diferencia de salinidad entre agua dulce y salada, generando electricidad a través de membranas semipermeables.",
    "¿Qué es la energía de las corrientes marinas?": "La energía de las corrientes marinas aprovecha el flujo constante de las corrientes oceánicas para generar electricidad mediante turbinas submarinas.",
    "¿Qué es la energía maremotérmica?": "La energía maremotérmica utiliza la diferencia de temperatura entre las aguas superficiales y profundas del océano para generar electricidad, especialmente en zonas tropicales.",
    "¿Qué es la energía de biomasa?": "La energía de biomasa se produce a partir de materia orgánica, como residuos agrícolas o forestales, que se queman o descomponen para generar calor o electricidad.",
    "¿Qué es la energía de biogás?": "El biogás se genera mediante la descomposición anaeróbica de materia orgánica, como residuos orgánicos o estiércol, produciendo un gas que puede utilizarse como combustible.",
    "¿Qué es el hidrógeno verde?": "El hidrógeno verde se produce mediante electrólisis del agua utilizando electricidad de fuentes renovables, resultando en un combustible limpio sin emisiones de CO₂.",
    "¿Qué es una PCH?": "Una PCH, o Pequeña Central Hidroeléctrica, es una planta que genera electricidad aprovechando el flujo de ríos o arroyos, generalmente con una capacidad menor a 20 MW.",
    "¿Qué es la energía solar térmica?": "La energía solar térmica utiliza colectores solares para captar el calor del sol y utilizarlo en calefacción o generación de electricidad mediante turbinas de vapor.",
    "¿Qué es la energía solar pasiva?": "La energía solar pasiva aprovecha el diseño arquitectónico y materiales para captar y distribuir el calor del sol sin necesidad de sistemas mecánicos.",
    "¿Qué es la energía eólica marina?": "La energía eólica marina utiliza aerogeneradores instalados en el mar para aprovechar los vientos más constantes y fuertes que en tierra firme.",
    "¿Qué es la energía renovable no convencional?": "Las energías renovables no convencionales incluyen fuentes como la solar, eólica, geotérmica, biomasa y mareomotriz, que no dependen de combustibles fósiles y tienen bajo impacto ambiental.",
    "¿Qué es la energía renovable convencional?": "La energía renovable convencional se refiere principalmente a la energía hidroeléctrica a gran escala, que ha sido utilizada durante décadas para generar electricidad.",
    "¿Qué es la energía renovable?": "La energía renovable proviene de fuentes naturales que se regeneran constantemente, como el sol, el viento, el agua y la biomasa, y se caracteriza por su bajo impacto ambiental.",
    "¿Qué es una microred?": "Una microred es un sistema energético local que puede operar de forma autónoma o conectada a la red principal, integrando diversas fuentes de energía y almacenamiento para suministrar electricidad a una comunidad o instalación específica.",
    "¿Qué es una microred aislada?": "Una microred aislada opera de forma independiente de la red eléctrica principal, utilizando fuentes de energía locales y almacenamiento para abastecer a comunidades remotas o instalaciones específicas.",
    "¿Qué es una microred conectada a la red?": "Una microred conectada a la red puede operar en paralelo con la red eléctrica principal, permitiendo la integración de fuentes de energía renovable y mejorando la resiliencia del suministro eléctrico.",
    "¿Qué es el almacenamiento de energía?": "El almacenamiento de energía permite guardar electricidad generada en momentos de baja demanda para su uso posterior, mejorando la eficiencia y estabilidad del sistema eléctrico.",
    "¿Qué es la eficiencia energética?": "La eficiencia energética consiste en utilizar menos energía para realizar la misma tarea, reduciendo el consumo y las emisiones sin sacrificar el confort o la productividad.",
    "¿Qué es la transición energética?": "La transición energética es el proceso de cambio hacia un sistema energético más sostenible, basado en fuentes renovables y tecnologías limpias, para reducir las emisiones de gases de efecto invernadero.",
    "¿Qué es la electrificación rural?": "La electrificación rural busca llevar acceso a la electricidad a comunidades alejadas o sin conexión a la red, mejorando su calidad de vida y oportunidades de desarrollo.",
    "¿Qué es el autoconsumo energético?": "El autoconsumo energético permite a los usuarios generar su propia electricidad, generalmente mediante paneles solares, reduciendo su dependencia de la red y sus costos energéticos.",
    "¿Qué es la generación distribuida?": "La generación distribuida se refiere a la producción de electricidad cerca del punto de consumo, utilizando pequeñas instalaciones como paneles solares o turbinas eólicas, mejorando la eficiencia y reduciendo pérdidas en la transmisión.",
    "¿Qué es la energía limpia?": "La energía limpia es aquella que produce electricidad sin emitir contaminantes ni gases de efecto invernadero, como la solar, eólica, hidroeléctrica y geotérmica.",
    "¿Qué es la energía sostenible?": "La energía sostenible satisface las necesidades actuales sin comprometer las de futuras generaciones, integrando fuentes renovables, eficiencia energética y responsabilidad ambiental.",
    "¿Qué es la energía alternativa?": "La energía alternativa engloba fuentes de energía diferentes a las convencionales, como la solar, eólica, geotérmica y biomasa, que ofrecen opciones más sostenibles y menos contaminantes."
}

faq_semantica_docs = [(nlp(preg), resp) for preg, resp in faq_semanticas.items()]

def respuesta_semantica(pregunta_usuario):
    doc_usuario = nlp(pregunta_usuario)
    mejor_similitud = 0
    mejor_respuesta = None
    for doc_pregunta, respuesta in faq_semantica_docs:
        similitud = doc_usuario.similarity(doc_pregunta)
        if similitud > mejor_similitud:
            mejor_similitud = similitud
            mejor_respuesta = respuesta
    return mejor_respuesta if mejor_similitud >= 0.65 else None


# FastAPI
app = FastAPI(title="Plataforma de Microredes", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

import re

def extraer_consumo(texto):
    """
    Extrae un valor numérico seguido de 'kwh' del texto.
    Soporta formatos como 6 kWh, 8.5kwh, 12,75 kWh, etc.
    """
    coincidencias = re.findall(r'(\d+[.,]?\d*)\s*kwh', texto.lower())
    if coincidencias:
        # Reemplaza coma por punto si es necesario
        valor = coincidencias[0].replace(",", ".")
        return float(valor)
    return None
def detectar_tipo_instalacion(texto):
    """
    Detecta el tipo de instalación mencionado en el texto y retorna un tipo y consumo estimado.
    """
    texto = texto.lower()
    if "escuela" in texto or "colegio" in texto:
        return "escuela rural", 10
    elif "finca" in texto:
        return "finca agrícola", 15
    elif "casa" in texto or "hogar" in texto or "vivienda" in texto:
        return "casa rural", 7
    elif "salud" in texto or "puesto médico" in texto or "hospital" in texto:
        return "puesto de salud", 12
    elif "negocio" in texto or "tienda" in texto or "comercio" in texto:
        return "negocio local", 9
    return None, None



def recomendar_fuente_energia(zona_nombre):
    zona = zonas_df[zonas_df["Zona"].str.lower() == zona_nombre.lower()]
    if zona.empty:
        return None

    datos = zona.iloc[0]
    mensaje = f"En la zona de {datos['Zona']}, se recomienda principalmente "

    solar = datos["Irradiacion_solar"] >= 5.5
    eolica = datos["Velocidad_viento"] >= 4.5
    hidrica = datos["Caudal_rio"] >= 80 and datos["Altura_salto"] >= 8

    fuentes = []
    if solar:
        fuentes.append("energía solar")
    if eolica:
        fuentes.append("energía eólica")
    if hidrica:
        fuentes.append("energía hídrica (PCH)")

    if fuentes:
        return mensaje + " y ".join(fuentes) + " debido a sus condiciones locales."
    else:
        return f"En la zona de {datos['Zona']}, no se identificaron condiciones óptimas destacadas para energía solar, eólica o hídrica."

@app.get("/chatbot", tags=["Chatbot"])
def chatbot(query: str):
    query_lower = query.lower()
    consumo_detectado = extraer_consumo(query_lower)
    tipo_instalacion, consumo_estimado = detectar_tipo_instalacion(query_lower)
    if tipo_instalacion:
        if tipo_instalacion == "escuela rural":
            respuesta = f"Para una {tipo_instalacion} con un consumo aproximado de {consumo_estimado} kWh/día, se recomienda una microred solar con baterías. También es aconsejable un generador diésel de respaldo para asegurar el suministro en días nublados o cortes prolongados."
        elif tipo_instalacion == "finca agrícola":
            respuesta = f"Para una {tipo_instalacion} que suele requerir energía para riego o refrigeración, con un consumo estimado de {consumo_estimado} kWh/día, lo ideal es un sistema solar con baterías. Si hay buen viento, puede complementarse con energía eólica. Un generador diésel es útil como respaldo."
        elif tipo_instalacion == "casa rural":
            respuesta = f"Una {tipo_instalacion} con un consumo promedio de {consumo_estimado} kWh/día puede funcionar bien con paneles solares y baterías. Si el área tiene viento constante, una turbina eólica puede ser un buen complemento."
        elif tipo_instalacion == "puesto de salud":
            respuesta = f"Para un {tipo_instalacion}, donde la continuidad del servicio es crítica, se recomienda una microred solar con baterías de alta capacidad, complementada con un generador diésel como respaldo para garantizar un suministro confiable."
        elif tipo_instalacion == "negocio local":
            respuesta = f"Un {tipo_instalacion} suele requerir un suministro estable, especialmente si opera refrigeración o equipos eléctricos. Un sistema solar con baterías puede cubrir la mayor parte del consumo estimado de {consumo_estimado} kWh/día. También es útil contar con una fuente de respaldo como generador diésel para continuidad en horarios extendidos."

        return JSONResponse(content={"respuesta": respuesta})


    
    # Si detectamos un consumo y la pregunta es sobre inversores
    if consumo_detectado and "inversor" in query_lower:
        respuesta = f"Si tu consumo es de {consumo_detectado} kWh diarios, un inversor de al menos {round(consumo_detectado / 2, 1)} kW sería adecuado. Asegúrate de que sea compatible con tu sistema solar o eólico."
        return JSONResponse(content={"respuesta": respuesta})

    # También podemos responder sobre paneles
    if consumo_detectado and "panel" in query_lower:
        respuesta = f"Con un consumo de {consumo_detectado} kWh diarios, necesitarías aproximadamente {math.ceil((consumo_detectado * 1000) / 400 / 5)} paneles solares de 400 Wp en una zona con buena irradiación."
        return JSONResponse(content={"respuesta": respuesta})


    # Reglas directas
    if "solar" in query_lower and "eólica" in query_lower:
        respuesta = "La energía solar es más estable en zonas con alta irradiación como La Guajira, mientras que la eólica es útil en lugares con vientos constantes. Ambas pueden complementarse en un sistema híbrido."
    elif "eólica" in query_lower and "pch" in query_lower:
        respuesta = "La energía eólica depende del viento, mientras que una PCH aprovecha ríos con buen caudal y altura. La PCH puede generar energía continua, pero requiere una ubicación muy específica."
    elif "solar" in query_lower and "pch" in query_lower:
        respuesta = "La energía solar es fácil de instalar y más versátil. Las PCH requieren estudios de caudal y topografía. En zonas con sol constante y sin ríos, la solar es mejor. En regiones húmedas con ríos potentes, una PCH puede ser más eficiente."
    elif "diésel" in query_lower and "solar" in query_lower:
        respuesta = "El diésel es confiable, pero costoso y contaminante. La energía solar reduce costos a largo plazo, es limpia y requiere menos mantenimiento. Por eso, muchas zonas están migrando de diésel a renovables."
    elif "diésel" in query_lower and "eólica" in query_lower:
        respuesta = "El diésel ofrece energía constante, pero con altos costos de combustible. La eólica es más económica a largo plazo, aunque depende del viento. Combinarlas es útil en zonas con vientos variables."
    elif "diésel" in query_lower and "pch" in query_lower:
        respuesta = "Una PCH puede reemplazar un sistema diésel si hay suficiente caudal y desnivel. Aunque la inversión inicial es mayor, la generación hídrica tiene costos operativos bajos y es más sostenible."

    # NUEVA regla específica: batería + solar
    elif ("batería" in query_lower or "almacenamiento" in query_lower) and "solar" in query_lower:
        respuesta = "Para energía solar, se recomiendan baterías de litio por su eficiencia y duración. Aunque son más costosas, ofrecen mejor rendimiento que las de plomo-ácido."

    # Reglas más generales
    elif "software" in query_lower or "herramienta" in query_lower:
        respuesta = "Existen varios softwares para diseñar y simular microredes. Algunos populares son: HOMER Pro, PV*SOL, PVsyst y RETScreen. También estamos desarrollando esta plataforma para ayudarte sin necesidad de conocimientos técnicos."
    elif "ley" in query_lower or "norma" in query_lower or "regulación" in query_lower:
        respuesta = "En Colombia, la Ley 1715 de 2014 promueve el uso de energías renovables. Ofrece beneficios tributarios y facilita la integración a la red. La CREG y la UPME regulan temas técnicos y de incentivos."
    elif "inyectar" in query_lower or "vender energía" in query_lower or "subir energía a la red" in query_lower:
        respuesta = "En Colombia puedes inyectar energía a la red si eres autogenerador. Debes registrarte con tu operador de red y cumplir con requisitos técnicos. La energía inyectada puede compensar tu consumo."
    elif "permiso" in query_lower or "instalación" in query_lower:
        respuesta = "Para instalar un sistema solar o híbrido verifica las normas locales. Los sistemas aislados no requieren tantos trámites. La UPME y operadores regionales pueden orientarte."
    elif "curso" in query_lower or "aprender" in query_lower:
        respuesta = "Puedes aprender sobre energías renovables en el SENA, Coursera, EdX y otras plataformas. Hay cursos gratuitos y diplomados disponibles."
    elif "panel" in query_lower and "cuánto" in query_lower:
        respuesta = "El número de paneles depende de tu consumo y la irradiación solar en tu zona. Usa el simulador para una estimación personalizada."
    elif "solar" in query_lower:
        respuesta = "La energía solar es ideal en regiones con alta irradiación. En Colombia, zonas como La Guajira tienen gran potencial."
    elif "batería" in query_lower or "almacenamiento" in query_lower:
        if "funciona" in query_lower:
            respuesta = "Las baterías almacenan energía para uso nocturno o días nublados. Su capacidad se mide en Wh o kWh."
        else:
            respuesta = "Las baterías permiten autonomía. Las de litio duran más que las de plomo-ácido."
    elif "eólica" in query_lower or "viento" in query_lower:
        respuesta = "La energía eólica es útil si tu zona tiene viento promedio mayor a 4.5 m/s. Puede complementar la solar."
    elif "diésel" in query_lower:
        respuesta = "Los generadores diésel ofrecen respaldo confiable, pero tienen costos operativos altos y requieren mantenimiento."
    elif "pch" in query_lower or "pequeña central hidroeléctrica" in query_lower:
        respuesta = "Una PCH genera energía aprovechando el caudal de un río y un desnivel. Ideal en zonas como Chocó o Amazonas."
    elif "precio" in query_lower or "cuánto cuesta" in query_lower or "retorno" in query_lower or "inversión" in query_lower:
        respuesta = "El costo depende de la combinación elegida. Puedes recuperar la inversión en 3 a 7 años."
    elif "zona" in query_lower and "recomiendas" in query_lower:
        respuesta = "Cada zona tiene condiciones únicas. Por ejemplo, La Guajira es ideal para solar y eólica, y el Chocó para hídrica."
    elif "qué fuente" in query_lower or "no sé qué fuente" in query_lower or "cuál es mejor" in query_lower:
        respuesta = "Dinos tu zona y consumo y te daremos una recomendación personalizada."
    elif "nube" in query_lower or "lluvia" in query_lower:
        respuesta = "En días nublados, las baterías o generadores aseguran energía."
    elif "ayuda" in query_lower or "no sé" in query_lower:
        respuesta = "Puedo ayudarte con solar, eólica, baterías o diésel. También puedes usar el simulador."
        # Intentar detectar una zona y recomendar fuente de energía
    for zona_nombre in zonas_df["Zona"]:
        if zona_nombre.lower() in query_lower:
            respuesta = recomendar_fuente_energia(zona_nombre)
            return JSONResponse(content={"respuesta": respuesta})
    else:
        # Intentar con el modelo semántico
        respuesta = respuesta_semantica(query)
        if not respuesta:
            respuesta = "Estoy aquí para ayudarte con microredes híbridas. Pregúntame sobre paneles, baterías, viento o zonas recomendadas."

    return JSONResponse(content={"respuesta": respuesta})


@app.get("/simulador", tags=["Simulador"])
def simulador(location: str, consumo: float):
    zona = zonas_df[zonas_df["Zona"].str.lower() == location.lower()]
    if zona.empty:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    zona_info = zona.iloc[0]
    irradiacion = float(zona_info["Irradiacion_solar"])
    viento = float(zona_info["Velocidad_viento"])

    panel = equipos_df[equipos_df["Tipo"] == "Panel Solar"].iloc[0]
    bateria = equipos_df[equipos_df["Tipo"] == "Batería"].iloc[0]
    inversor = equipos_df[equipos_df["Tipo"] == "Inversor"].iloc[0]
    eolica = equipos_df[equipos_df["Tipo"] == "Turbina Eólica"].iloc[0]
    diesel = equipos_df[equipos_df["Tipo"] == "Generador Diésel"].iloc[0]

    consumo_diario_wh = consumo * 1000
    n_paneles = math.ceil(consumo_diario_wh / int(panel["Capacidad_num"]) / irradiacion)
    n_baterias = math.ceil(consumo_diario_wh * 2 / int(bateria["Capacidad_num"]))
    costo_solar = (n_paneles * float(panel["Precio (USD)"])) + (n_baterias * float(bateria["Precio (USD)"])) + float(inversor["Precio (USD)"])

    incluye_eolica = viento >= 4.5
    if incluye_eolica:
        n_turbinas = math.ceil(consumo_diario_wh / int(eolica["Capacidad_num"]) / 24)
        costo_eolica = (n_turbinas * float(eolica["Precio (USD)"])) + float(inversor["Precio (USD)"])
    else:
        n_turbinas = 0
        costo_eolica = 0

    incluye_diesel = True
    costo_diesel = float(diesel["Precio (USD)"])
    costo_total = costo_solar + (costo_eolica if incluye_eolica else 0) + costo_diesel

    return {
        "zona": str(zona_info["Zona"]),
        "irradiacion_solar": irradiacion,
        "viento": viento,
        "consumo_diario_kwh": consumo,
        "configuracion_recomendada": {
            "paneles_solares": int(n_paneles),
            "baterias": int(n_baterias),
            "turbinas_eolicas": int(n_turbinas),
            "incluir_diesel": incluye_diesel
        },
        "costos_estimados_usd": {
            "solar": round(costo_solar, 2),
            "eolica": round(costo_eolica, 2) if incluye_eolica else "No aplica",
            "diesel": round(costo_diesel, 2),
            "total": round(costo_total, 2)
        }
    }
