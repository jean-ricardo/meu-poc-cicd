# Imagem base enxuta (slim = Debian mínimo, pesa bem menos que a padrão)
FROM python:3.12-slim

WORKDIR /app

# Copia só o requirements primeiro para aproveitar o CACHE de camadas do Docker:
# enquanto as dependências não mudarem, o Docker reusa esta camada e o build fica rápido.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o código da aplicação
COPY app/ ./app/

# Boa prática de segurança: não rodar como root dentro do container
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Sobe o servidor ASGI servindo a aplicação FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
