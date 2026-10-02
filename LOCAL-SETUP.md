# Classroom Graph Builder: OpenRouter + local embeddings

This customized version of [Neo4j LLM Graph Builder](https://github.com/neo4j-labs/llm-graph-builder) adds OpenRouter support and a local Docker setup. Upstream Apache 2.0 license and attribution are preserved.

## Requirements

- Docker with Docker Compose (start Docker Desktop on macOS/Windows).
- Python 3 for the setup script.
- Your own OpenRouter API key and account credit.
- Available ports 8081, 8000, 7475, and 7688.

## Start

```sh
git clone https://github.com/juananpe/llm-graph-builder.git
cd llm-graph-builder
python3 setup-local.py
```

The script asks for your OpenRouter key with hidden input, generates a random Neo4j password, and builds/starts the services. First build downloads PDF-processing dependencies and the embedding model and can take several minutes. Credentials are stored in ignored `.env` files and excluded from Docker image builds.

Alternatively, copy `.env.example` to `.env` and `backend/.env.local.example` to `backend/.env`, fill in your credentials, and run `docker compose -f compose.local.yaml up -d --build`.

## Connect and ingest

Open http://127.0.0.1:8081 and click **Connect to Neo4j**:

- URI: `bolt://host.docker.internal:7688`
- Username: `neo4j`
- Database: `neo4j`
- Password: the generated value in the root `.env`.

That URI is used by the backend inside Docker. Neo4j Browser is at http://127.0.0.1:7475/browser/; connect there with `bolt://127.0.0.1:7688` and the same credentials.

Upload a PDF, select **Openrouter gpt 5 mini**, and click **Generate Graph**. You can configure graph patterns in Entity Extraction Settings before extraction.

For the course PDFs, clone [the local course reader](https://github.com/juananpe/neo4j-course-local) and open its `exercises/llm-knowledge-graph/data/course/pdfs/` folder.

Extraction and chat use **`openai/gpt-5-mini` through OpenRouter**. Document text is sent through OpenRouter to the model provider and incurs API usage. Embeddings use **`sentence-transformers/all-MiniLM-L6-v2` locally**, producing 384-dimensional vectors.

## Stop and restart

```sh
docker compose -f compose.local.yaml stop
docker compose -f compose.local.yaml up -d
```

Neo4j data persists in a Docker volume. Services bind to localhost. This database is separate from the course election graph on ports 7474/7687. Uploaded temporary files are not persisted across backend container recreation; keep original PDFs.

To change the model, edit `LLM_MODEL_CONFIG_OPENROUTER_GPT_5_MINI` in `backend/.env` to the desired OpenRouter model slug, then recreate the backend with `docker compose -f compose.local.yaml up -d --force-recreate backend`. The UI option retains its configured name.

## Local changes

- Added an OpenRouter branch to `backend/src/llm.py`, using the OpenAI-compatible endpoint with a separate `OPENROUTER_API_KEY`.
- Added `compose.local.yaml` with Neo4j Community + APOC, one backend worker, local embeddings, and authentication-free localhost UI.
- Added example configuration and `setup-local.py`.
