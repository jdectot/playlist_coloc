document.addEventListener("DOMContentLoaded", () => {
  const sendButton = document.getElementById("send-song-btn");
  const songInput = document.getElementById("song-input");
  const resultsList = document.getElementById("results");
  const resultDiv = document.getElementById("prediction");
  const newSearchButton = document.getElementById("new-search-btn");
  const resultsText = document.getElementById("result-text");


  // Function to send song query and handle responses.
  // If no song is provided, return message.

   async function send() {
    const song = songInput.value.trim();
    if (!song) {
        resultDiv.innerText = "Veuillez entrer le nom d'une chanson.";
        return;
    }

    resultsList.innerHTML = ""; // empty previous results

    songInput.classList.add("invisible");
    sendButton.classList.add("invisible");
    newSearchButton.classList.remove("invisible");


    try {
      // Appel à la route search_song pour récupérer les morceaux
      const res = await fetch("/search_song", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ Musique: song }),
      });

      const data = await res.json();

      if (data.error) {
        resultDiv.innerText = "❌ " + data.error;
        return;
      }

      resultsText.classList.remove("invisible");

      const tracks = data.result.slice(0, 5); // max 5 chansons

      if (tracks.length === 0) {
        resultDiv.innerText = "Aucun résultat trouvé.";
        return;
      }


      // Création de la liste cliquable
      newSearchButton.classList.remove("invisible");
      tracks.forEach(([track_name, track_id]) => {
        const li = document.createElement("li");
        li.textContent = track_name;
        li.style.cursor = "pointer";

        li.addEventListener("click", async () => {
          // Affiche le texte de chargement pour la prédiction
          newSearchButton.classList.add("invisible");
          resultsList.classList.add("invisible");
          resultDiv.innerText = "Analyse en cours...";

          try {
            const predRes = await fetch("/predict_song", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ id: track_id }),
            });
            newSearchButton.classList.remove("invisible");
            resultsText.classList.add("invisible");
            const predData = await predRes.json();
            resultDiv.innerText = "🎧 Cette musique correspond à : " + predData.result;
          } catch (error) {
            console.error("Error:", error);
            resultDiv.innerText = "Erreur lors de la requête de prédiction.";
          }
        });

        resultsList.appendChild(li);
      });
    } catch (error) {
      console.error("Error:", error);
      resultDiv.innerText = "Erreur lors de la requête de recherche.";
    }

  }



   // Fonction pour réafficher le champ et le bouton de recherche
  function restoreSearch() {
    songInput.classList.remove("invisible");
    sendButton.classList.remove("invisible");
    newSearchButton.classList.add("invisible");
    resultsText.classList.add("invisible");
    resultsList.classList.add("invisible");
    resultsList.innerHTML = "";
    resultDiv.innerText = "";
    songInput.value = "";
  }

  // Event listeners
  sendButton.addEventListener("click", send);
  newSearchButton.addEventListener("click", restoreSearch);


});