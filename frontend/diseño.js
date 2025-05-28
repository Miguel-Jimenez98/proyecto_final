
document.getElementById("designForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const location = formData.get("location");
  const consumo = formData.get("consumo");
  const fuente = formData.get("fuente");

  const res = await fetch(`http://localhost:8000/simulador?location=${location}&consumo=${consumo}&fuente=${fuente}`);
  const data = await res.json();

  const resultadoDiv = document.getElementById("resultadoSimulacion");
  resultadoDiv.innerHTML = "<h3>Resultados:</h3><pre>" + JSON.stringify(data, null, 2) + "</pre>";
});
