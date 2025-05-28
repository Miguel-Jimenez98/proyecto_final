
async function sendQuestion() {
  const input = document.getElementById("userInput").value;
  const responseDiv = document.getElementById("chatResponse");

  const res = await fetch(`http://localhost:8000/chatbot?query=${encodeURIComponent(input)}`);
  const data = await res.json();

  responseDiv.innerHTML = `<p><strong>Bot:</strong> ${data.respuesta}</p>`;
}
