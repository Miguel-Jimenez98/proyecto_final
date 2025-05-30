document.getElementById("designForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const location = formData.get("location");
  const consumo = formData.get("consumo");
  const fuente = formData.get("fuente");
  
  // 🔧 MODIFICACIÓN: Construcción dinámica de la URL
  const incluirAutonomia = document.getElementById("incluirAutonomia").checked;
  const diasAutonomia = document.getElementById("diasAutonomia").value;

  let url = `http://localhost:8000/simulador?location=${location}&consumo=${consumo}`;
  if (incluirAutonomia) {
  url += `&incluir_autonomia=true&autonomia=${diasAutonomia}`;
}

  const res = await fetch(url);

  const data = await res.json();

  const resultadoDiv = document.getElementById("resultadoSimulacion");

  resultadoDiv.innerHTML = `
    <h3>🔍 Resultados para ${data.zona}</h3>
    <p><strong>Irradiación Solar:</strong> ${data.irradiacion_solar} kWh/m²/día</p>
    <p><strong>Velocidad del Viento:</strong> ${data.viento} m/s</p>
    <p><strong>Consumo Diario:</strong> ${data.consumo_diario_kwh} kWh</p>

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
      <p style="font-size: 0.9em; font-style: italic; color: #555;">
      Los cálculos consideran pérdidas por eficiencia del inversor (95%) y del cableado (97%).
    </p>
  `;
});
