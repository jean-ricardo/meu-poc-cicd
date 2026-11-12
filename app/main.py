from fastapi import FastAPI

app = FastAPI(title="POC CI/CD + Container Registry")

@app.get("/")
def read_root():
    return {
        "versao": "1.0",
        "mensagem": "API publicada automaticamente via pipeline CI/CD",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
