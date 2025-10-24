document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("send-song-btn");
  const songInput = document.getElementById("song");
  const resultDiv = document.getElementById("result");

  async function send() {
    const song = songInput.value;
    resultDiv.innerText = "Analyse en cours...";

    try {
      const res = await fetch("/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ Musique: song }),
      });

      const data = await res.json();

      if (data.error) {
        resultDiv.innerText = "❌ " + data.error;
      } else {
        resultDiv.innerText = "🎧 Cette musique correspond à : " + data.result;
      }
    } catch (error) {
      console.error("Error:", error);
      resultDiv.innerText = "Erreur lors de la requête.";
    }
  }

  if (button) {
    button.addEventListener("click", send);
  }
});