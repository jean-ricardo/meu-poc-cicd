from fastapi import FastAPI

app = FastAPI(title="POC CI/CD + Container Registry")

# Rota principal: para a demo, basta trocar "1.0" por "2.0" e dar git push.
# O pipeline reconstrói a imagem e publica a nova versão no Registry.
@app.get("/")
def read_root():
    return {
        "versao": "1.0",
        "mensagem": "API publicada automaticamente via pipeline CI/CD",
    }


# Rota de health check (boa prática: usada por Kubernetes/load balancers
# para saber se o container está saudável).
@app.get("/health")
def health():
    return {"status": "ok"}
