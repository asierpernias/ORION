from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from ORION import run_orion

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>ORION</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #111;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }

        main {
            width: 90%;
            max-width: 700px;
            text-align: center;
        }

        h1 {
            font-size: 56px;
            margin-bottom: 10px;
        }

        p {
            color: #bbb;
        }

        button {
            margin-top: 30px;
            padding: 16px 28px;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            background-color: #00c2ff;
            color: #000;
            font-weight: bold;
        }

        button:disabled {
            opacity: 0.5;
            cursor: wait;
        }

        .result {
            margin-top: 30px;
            text-align: left;
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 8px;
            display: none;
        }

        pre {
            white-space: pre-wrap;
            background-color: #000;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
        }

        a {
            color: #00c2ff;
        }
    </style>
</head>
<body>
    <main>
        <h1>ORION</h1>
        <p>Asistente local por voz para buscar en Google o YouTube.</p>

        <button id="listenButton">Escuchar</button>

        <section class="result" id="resultBox">
            <h2>Resultado:</h2>

            <p><strong>Texto detectado:</strong></p>
            <pre id="textResult"></pre>

            <p><strong>JSON:</strong></p>
            <pre id="jsonResult"></pre>

            <p><strong>URL:</strong></p>
            <a id="urlResult" href="#" target="_blank"></a>
        </section>
    </main>

    <script>
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
    </script>
</body>
</html>
"""

@app.post("/run")
def run():
    try:
        result = run_orion()
         
        if not result:
            return JSONResponse(
                status_code = 400,
                content={"error": "No se pudo obtener resultado de ORION"}
            )
        return result
    except Exception as error:
        return JSONResponse(
            status_code = 500,
            content={"error": str(error)}
        )
           