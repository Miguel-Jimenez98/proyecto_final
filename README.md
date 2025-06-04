# Plataforma Inteligente para el Diseño de Microredes Híbridas en Colombia 🇨🇴⚡

Este proyecto desarrolla una plataforma web que permite simular y recomendar configuraciones óptimas de microredes híbridas (solar, eólica, diésel y PCH) para zonas rurales no interconectadas (ZNI) de Colombia. La herramienta integra un **chatbot inteligente** y un **motor técnico de simulación energética**, facilitando el acceso a propuestas técnicas incluso para usuarios sin formación especializada.

---

## 🔧 Estructura del Proyecto

```
/backend
    └── main.py               # Lógica de la API, chatbot y simulador
    └── catalogo_equipos.csv  # Base de datos técnica de equipos energéticos
    └── zonas_no_interconectadas.csv  # Datos ambientales, sociales y de consumo por zona

/frontend
    └── index.html            # Interfaz principal del usuario
    └── chatbot.js            # Script del chatbot
    └── diseño.js             # Script del simulador técnico
    └── styles.css            # Estilos de la interfaz

requirements.txt              # Lista de dependencias del backend
README.md                     # Documentación general del proyecto
```

---

## 🚀 Funcionalidades

- 🧠 **Chatbot energético** con procesamiento semántico y reglas por zona, perfil e infraestructura.
- ⚙️ **Simulador técnico** de microredes híbridas con parámetros como irradiación solar, viento, PCH, consumo promedio, etc.
- 📊 **Visualización de resultados** con gráficos intuitivos (barras y donut) para facilitar la comprensión.
- 🗺️ **Adaptación a contexto colombiano**, incluyendo zonas específicas como Amazonas, La Guajira, Chocó, entre otras.

---

## 📦 Instalación (Modo local)

### Backend (FastAPI)

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/nombre_repositorio.git
   cd nombre_repositorio/backend
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend

Abre el archivo `index.html` en tu navegador preferido. Asegúrate de que el backend esté corriendo en `http://127.0.0.1:8000`.

---

## ✅ Tecnologías utilizadas

- **Python + FastAPI** (API backend)
- **pandas / numpy** (cálculos técnicos)
- **spaCy** (procesamiento de lenguaje natural para el chatbot)
- **HTML / CSS / JS** (frontend web)
- **Chart.js** (gráficas de resultados)

---

## 📚 Casos de uso

- Hogares, fincas, escuelas o puestos de salud rurales sin acceso al sistema eléctrico nacional.
- Estimación técnica preliminar para diseño de microredes sin necesidad de software especializado.
- Herramienta educativa para estudiantes, ingenieros o técnicos energéticos en formación.

---

## 📌 Estado actual del proyecto

- ✅ Chatbot funcional con lógica semántica y por reglas.
- ✅ Simulador técnico operativo con resultados visuales.
- 🔄 Mejora futura: conexión a APIs de clima en tiempo real.
- 🔄 Mejora futura: optimización económica avanzada.

---

## 🧑‍💻 Autor

Miguel Ángel Jiménez 
Lizeth Quevedo Narvaez 
Proyecto desarrollado como parte del Bootcamp de Inteligencia Artificial (Explorador) 2025.

---

## 📄 Licencia

Este proyecto está disponible bajo licencia MIT.
