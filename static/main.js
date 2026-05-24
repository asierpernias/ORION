const button = document.getElementById("listenButton");
const resultBox = document.getElementById("resultBox");
const textResult = document.getElementById("textResult");
const jsonResult = document.getElementById("jsonResult");
const urlResult = document.getElementById("urlResult");

button.addEventListener("click", async () => {
    button.disabled = true;
    button.textContent = "Escuchando...";

    try {
        const response = await fetch("/run", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Error ejecutando ORION");
        }

        textResult.textContent = data.text;
        jsonResult.textContent = JSON.stringify(data.intent, null, 2);
        urlResult.textContent = data.url;
        urlResult.href = data.url;

        resultBox.style.display = "block";

        if (data.url) {
            window.open(data.url, "_blank");
        }
    } catch (error) {
        alert(error.message);
    } finally {
        button.disabled = false;
        button.textContent = "Escuchar";
    }
});