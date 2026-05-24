from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ORION import run_orion

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/run")
def run():
    try:
        result = run_orion()
        if not result:
            return JSONResponse(
                status_code=400,
                content={"error": "No se pudo obtener resultado de ORION"}
            )
        return result
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"error": str(error)}
        )