let graficoCostos; // Para controlar y actualizar el gráfico si ya existe
let graficoContribucion; // Para controlar el gráfico tipo doughnut


document.getElementById("designForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const location = formData.get("location");
  const consumo = formData.get("consumo");
  const perfil = formData.get("perfil");
  const fuente = formData.get("fuente");
  
  // 🔧 MODIFICACIÓN: Construcción dinámica de la URL
  const incluirAutonomia = document.getElementById("incluirAutonomia").checked;
  const diasAutonomia = document.getElementById("diasAutonomia").value;

  let url = `http://localhost:8000/simulador?location=${encodeURIComponent(location)}`;
  if (consumo) url += `&consumo=${consumo}`;
  if (perfil) url += `&perfil=${perfil}`;
  if (incluirAutonomia) {
  url += `&incluir_autonomia=true&autonomia=${diasAutonomia}`;
}

  let data;
  try {
    const res = await fetch(url);
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Error desconocido");
    }
    data = await res.json();
    console.log("📦 Respuesta completa del simulador:", data); // ✅ Agregado
  } catch (err) {
    const resultadoDiv = document.getElementById("resultadoSimulacion");
    resultadoDiv.innerHTML = `<p style="color: red;"><strong>❌ Error:</strong> ${err.message}</p>`;
    return; // Detener ejecución si hubo error
  }


  const resultadoDiv = document.getElementById("resultadoSimulacion");

  resultadoDiv.innerHTML = `
    <h3>🔍 Resultados para ${data.zona}</h3>
    <p><strong>Irradiación Solar:</strong> ${data.irradiacion_solar} kWh/m²/día</p>
    <p><strong>Velocidad del Viento:</strong> ${data.viento} m/s</p>
    <p><strong>Consumo Diario:</strong> ${data.consumo_diario_kwh} kWh</p>

    <h4>🌍 Información del Entorno</h4>
    <ul>
      <li><strong>Acceso Difícil:</strong> ${data.acceso_dificil}</li>
      <li><strong>Potencial PCH:</strong> ${data.potencial_pch}</li>
      <li><strong>Tipo de Clima:</strong> ${data.tipo_de_clima}</li>
      <li><strong>Demanda Creciente:</strong> ${data.demanda_creciente}</li>
      <li><strong>Observaciones:</strong> ${data.observaciones}</li>
    </ul>

    ${data.nota
      ? `<p style="${
          data.nota.includes("⚠️")
            ? "color: #e67e22; font-weight: bold;"
            : "font-size: 0.9em; font-style: italic; color: #555;"
        }"><strong>Nota:</strong> ${data.nota}</p>`
    : ""}
    ${data.consumo_estimado ? "<p style='color: #aa7700; font-style: italic;'>⚠️ El consumo fue estimado automáticamente según el perfil seleccionado.</p>" : ""}


    <h4>⚙️ Configuración Recomendada</h4>
    <ul>
      <li><strong>Paneles Solares:</strong> ${data.configuracion_recomendada.paneles_solares}</li>
      <li><strong>Baterías:</strong> ${data.configuracion_recomendada.baterias}</li>
      <li><strong>Turbinas Eólicas:</strong> ${data.configuracion_recomendada.turbinas_eolicas}</li>
      <li><strong>¿Incluir Diésel?:</strong> ${data.configuracion_recomendada.incluir_diesel ? "Sí" : "No"}</li>
    </ul>

    <h4>💲 Costos Estimados (USD)</h4>
    <ul>
      <li><strong>Solar:</strong> $${data.costos_estimados_usd.solar}</li>
      <li><strong>Eólica:</strong> ${data.costos_estimados_usd.eolica === "No aplica" ? "No aplica" : "$" + data.costos_estimados_usd.eolica}</li>
      <li><strong>Diésel:</strong> $${data.costos_estimados_usd.diesel}</li>
      <li><strong>Total:</strong> <strong>$${data.costos_estimados_usd.total}</strong></li>
    </ul>

    ${data.recomendaciones && data.recomendaciones.length > 0 ? `
      <h4>📌 Recomendaciones Técnicas</h4>
      <ul style="background-color: #f9f9f9; padding: 10px; border-left: 5px solid #3498db;">
        ${data.recomendaciones.map(r => `<li style="margin-bottom: 6px;">${r}</li>`).join("")}
      </ul>
    ` : ""}

  `;

    // 🎯 Generar gráfico de barras con Chart.js
  const ctx = document.getElementById("graficoCostos").getContext("2d");

  // Si ya existe un gráfico previo, lo destruimos antes de crear uno nuevo
  if (graficoCostos) {
    graficoCostos.destroy();
  }

  const costos = data.costos_estimados_usd;

  graficoCostos = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Solar", "Eólica", "Diésel"],
      datasets: [{
        label: "Costo estimado (USD)",
        data: [
          costos.solar,
          costos.eolica === "No aplica" ? 0 : costos.eolica,
          costos.diesel
        ],
        backgroundColor: ["#f1c40f", "#3498db", "#95a5a6"]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: (context) => `$${context.raw}`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "USD"
          }
        }
      }
    }
  });

// 🎯 Segundo gráfico: Distribución porcentual de costos
const ctx2 = document.getElementById("graficoContribucion").getContext("2d");

// Destruir gráfico anterior si existe
if (graficoContribucion) {
  graficoContribucion.destroy();
}

// Calculamos solo los valores numéricos válidos
const costoSolar = costos.solar || 0;
const costoEolica = costos.eolica === "No aplica" ? 0 : costos.eolica;
const costoDiesel = costos.diesel || 0;
const total = costoSolar + costoEolica + costoDiesel;

// Validar si hay algo que graficar
if (total > 0) {
  const porcentajes = [
    ((costoSolar / total) * 100).toFixed(1),
    ((costoEolica / total) * 100).toFixed(1),
    ((costoDiesel / total) * 100).toFixed(1)
  ];

  graficoContribucion = new Chart(ctx2, {
    type: "doughnut",
    data: {
      labels: [
        `Solar (${porcentajes[0]}%)`,
        `Eólica (${porcentajes[1]}%)`,
        `Diésel (${porcentajes[2]}%)`
      ],
      datasets: [{
        label: "Distribución porcentual",
        data: [costoSolar, costoEolica, costoDiesel],
        backgroundColor: ["#f1c40f", "#3498db", "#95a5a6"]
      }]
    },
    options: {
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => `${context.label}: $${context.raw}`
          }
        }
      }
    }
  });
}

});


