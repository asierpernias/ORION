const button      = document.getElementById("listenButton");
const orb         = document.getElementById("orb");
const statusEl    = document.getElementById("status");
const resultBox   = document.getElementById("resultBox");
const textResult  = document.getElementById("textResult");
const jsonResult  = document.getElementById("jsonResult"); 
const urlResult   = document.getElementById("urlResult");

function setStatus(text) {
    statusEl.textContent = text;
    statusEl.classList.toggle("visible", text.length > 0);
}

button.addEventListener("click", async () => {
    button.disabled = true;
    button.textContent = "···";
    orb.classList.add("listening");
    setStatus("Escuchando…");

    try {
        setStatus("Escuchando…");
        const response = await fetch("/run", { method: "POST" });

        setStatus("Procesando…");
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Error ejecutando ORION");
        }

        textResult.textContent = data.text;
        jsonResult.textContent = JSON.stringify(data.intent, null, 2);
        urlResult.textContent  = data.url;
        urlResult.href         = data.url;

        resultBox.classList.add("visible");

        if (data.url) {
            setStatus("Abriendo…");
            window.open(data.url, "_blank");
        }

    } catch (error) {
        alert(error.message);
    } finally {
        button.disabled = false;
        button.textContent = "Escuchar";
        orb.classList.remove("listening");
        setStatus("");
    }
});