# POC: Integração de Container Registry com Pipeline CI/CD

Prova de conceito (Proof of Concept) de um pipeline de **CI/CD** que, a cada push no
GitHub, **constrói** uma imagem Docker, **versiona** e **publica** no
**GitHub Container Registry (GHCR)** — de forma automática e sem senhas no código.

> API mínima em **FastAPI** com uma rota `GET /` que retorna a versão. É só o
> suficiente para demonstrar o fluxo; o conceito é idêntico para Docker Hub,
> AWS ECR, Google Artifact Registry, Azure ACR ou Harbor.

---

## Equipe

| Aluno | Matrícula |
|-------|-----------|
| Arthur Belo da Silva | 01615335 |
| Bruno Lourenço Bezerra | 01606518 |
| Jean Ricardo França da Silva | 01583760 |
| Thiago Vinicius de Araújo | 01664566 |
| Victor Gouveia Crespo Leitão | 01602538 |

---

## Estrutura do projeto

```
meu-poc-cicd/
├── app/
│   └── main.py                 # API FastAPI (rota GET / -> {"versao": "1.0"})
├── requirements.txt            # dependências Python
├── Dockerfile                  # imagem enxuta, com cache e usuário não-root
├── .dockerignore               # tira lixo da imagem
├── .gitignore
├── .github/
│   └── workflows/
│       └── docker-publish.yml  # o pipeline (CI/CD) de build + push + scan
└── README.md
```

---

## Como o pipeline funciona (o coração da POC)

Fluxo: **git push → Build & Test → Login no Registry → Push da imagem → (Deploy)**

O arquivo `.github/workflows/docker-publish.yml`:

1. **Dispara** a cada push na `main` e quando você cria uma tag `v*.*.*`.
2. Faz **login no GHCR** usando o `GITHUB_TOKEN` (token temporário gerado na hora — **nenhuma senha no código**).
3. Gera **tags automaticamente** com uma estratégia de versionamento rastreável:
   - `sha-<commit>` → imutável, garante rollback preciso;
   - `v1.2.0` → versionamento semântico (quando você cria uma tag no Git);
   - `latest` → só na branch principal.
4. Faz **build + push** com **cache** de camadas (builds seguintes ficam rápidos).
5. Roda um **scan de vulnerabilidades (Trivy)** — em modo relatório na POC.

---

## Passo a passo para colocar no ar

### 1. Criar o repositório no GitHub
Crie um repositório novo (ex: `meu-poc-cicd`) e suba estes arquivos:

```bash
git init
git add .
git commit -m "POC CI/CD + Container Registry"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/meu-poc-cicd.git
git push -u origin main
```

Só o push já dispara o pipeline. Vá na aba **Actions** do repositório e acompanhe
o build ficar **verde** ✅.

### 2. Garantir a permissão de escrita no Registry
O workflow já pede `packages: write`. Se der erro de permissão, confira em:
**Settings → Actions → General → Workflow permissions** e marque
**"Read and write permissions"**.

### 3. Ver a imagem publicada
A imagem aparece no seu perfil/repositório do GitHub, na seção **Packages**
(ou em `ghcr.io/SEU-USUARIO/meu-poc-cicd`). Para baixar e rodar a imagem publicada:

```bash
docker pull ghcr.io/SEU-USUARIO/meu-poc-cicd:latest
docker run -p 8000:8000 ghcr.io/SEU-USUARIO/meu-poc-cicd:latest
```

Acesse http://localhost:8000 → deve retornar `{"versao": "1.0", ...}`.
A documentação automática fica em http://localhost:8000/docs.

---

## Handoff — passando para outra pessoa subir

Se quem vai subir o projeto for outro colega da equipe, há dois caminhos:

**Opção A — o colega sobe na conta dele (mais simples):**
1. Envie para ele **a pasta/zip completa deste projeto** (`meu-poc-cicd`).
   Não é preciso enviar nenhuma senha ou token: o pipeline usa o `GITHUB_TOKEN`
   automático do GitHub.
2. O colega cria um repositório novo na conta dele e roda os comandos da seção
   **"1. Criar o repositório no GitHub"** acima (trocando `SEU-USUARIO` pelo usuário dele).
3. Ele confere a permissão de escrita (seção 2) e acompanha o Actions ficar verde.
   A imagem ficará em `ghcr.io/USUARIO-DELE/meu-poc-cicd`.

**Opção B — você cria o repositório e adiciona o colega:**
1. Você cria o repositório e faz o primeiro push.
2. Em **Settings → Collaborators**, adicione o colega pelo usuário do GitHub.
3. Ele clona (`git clone`), faz as alterações e dá push no mesmo repositório.

**Checklist do que enviar para o colega:**
- [ ] A pasta/zip `meu-poc-cicd` (código + `Dockerfile` + `.github/workflows/`)
- [ ] O link deste README (as instruções que ele vai seguir)
- [ ] Se for a Opção B: o usuário do GitHub dele, para adicionar como colaborador
- [ ] **Não** envie senhas, tokens ou arquivos `.env` — o pipeline não precisa

---

## Rodar localmente (opcional, bom para testar antes)

**Com Docker:**
```bash
docker build -t poc-cicd .
docker run -p 8000:8000 poc-cicd
```

**Sem Docker (direto em Python):**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Roteiro do vídeo da demo (1 a 2 minutos)

A "dica de ouro": grave este fluxo para não depender da internet da sala.
Para gravar a tela: **Windows** → `Win + G` (Xbox Game Bar); **Mac** → `Cmd + Shift + 5`;
ou use o **OBS Studio** (grátis, nas duas plataformas).

| Tempo | O que mostrar na tela | O que falar |
|-------|-----------------------|-------------|
| 0:00–0:15 | Repositório no GitHub + abrir `docker-publish.yml` | "Este é o pipeline: faz login no registry, gera as tags e publica a imagem." |
| 0:15–0:30 | Abrir `app/main.py` e trocar `"1.0"` por `"2.0"`, salvar | "Vou simular uma nova versão da aplicação." |
| 0:30–0:45 | Terminal: `git commit -am "versao 2.0"` e `git push` | "Um único push dispara todo o processo." |
| 0:45–1:20 | Aba **Actions**: o workflow rodando e ficando **verde** ✅ | "O pipeline testa, constrói e publica sozinho." |
| 1:20–1:40 | Aba **Packages**: a nova imagem com a tag `sha-…` | "A imagem versionada já está no Container Registry." |
| 1:40–2:00 | *(opcional)* `docker run` da imagem mostrando `{"versao":"2.0"}` | "E aqui a nova versão rodando a partir da imagem publicada." |

Comandos usados no vídeo:
```bash
git commit -am "Atualiza versao para 2.0"
git push
# depois do Actions ficar verde (opcional):
docker pull ghcr.io/SEU-USUARIO/meu-poc-cicd:latest
docker run -p 8000:8000 ghcr.io/SEU-USUARIO/meu-poc-cicd:latest
```

Pronto: isso prova, de ponta a ponta, que o código novo virou imagem publicada
automaticamente.

---

## Boas práticas demonstradas (para citar na apresentação)

- **Sem credenciais no código** — uso do `GITHUB_TOKEN` (ou PAT/OIDC em outros registries).
- **Tags imutáveis** — `sha-<commit>` em vez de depender só de `:latest`, permitindo rollback preciso.
- **Cache de build** — acelera execuções seguintes.
- **Usuário não-root** no container — reduz superfície de ataque.
- **Scan de vulnerabilidades (Trivy)** — etapa de DevSecOps (em produção, bloqueia o deploy em falhas CRITICAL).
- **Próximos passos (CD):** gatilho de deploy via `kubectl set image` (push) ou GitOps com ArgoCD/Flux (pull, recomendado).
