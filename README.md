# TrustTrace — Evidence-Based Seller Risk Assessment

**IBM Z Datathon 2026 | IBM LinuxONE | Edge AI / Machine Learning**

TrustTrace is a prototype that helps online shoppers assess potential seller risk using observable listing and profile indicators. It combines evidence-based rules, a synthetic-data machine-learning model, and a locally hosted IBM Granite language model to generate an understandable risk report.

> **Important:** This prototype uses synthetic demonstration data. Its scores are illustrative risk assessments, not proof of fraud or validated real-world scam-detection predictions.

## The Problem

Online shoppers may encounter unusually low prices, reused product images, and newly created seller accounts. Evaluating these signals individually can be difficult, especially when evidence is incomplete.

TrustTrace combines available indicators into one explainable assessment and clearly distinguishes missing information from established risk indicators.

## Our Solution

A user submits a product or seller listing link. TrustTrace evaluates the available demonstration evidence and returns:

- **Risk score:** An illustrative score from 0–10.
- **Risk level:** Low, elevated, high, or insufficient evidence, according to the implemented assessment logic.
- **Confidence:** An indication of how much usable evidence is available.
- **Evidence report:** A concise explanation of the observed indicators and recommended precautions.
- **Local AI explanation:** IBM Granite generates a natural-language explanation when the local inference service is available.

The application uses cautious language: risk indicators do not prove fraud, and missing data does not automatically make a seller suspicious.

## Architecture

```text
Product / Seller Link
        |
        v
TrustTrace FastAPI Backend
        |
        v
Evidence Collection / Demo Evidence
        |
        v
Rule-Based Risk Assessment
        |
        +----> Synthetic-Data ML Model
        |
        +----> Local IBM Granite LLM
        |
        v
Evidence Report and Risk Summary
        |
        v
Web Interface
```

The prototype runs on **IBM LinuxONE Community Cloud**, using Ubuntu Linux on the `s390x` architecture. The Granite inference service runs locally on the instance and communicates with the application over localhost.

## Technology Stack

- **Python** — application and model development
- **FastAPI** — HTTP API
- **Uvicorn** — application server
- **scikit-learn** — synthetic-data classification experiment
- **NumPy and SciPy** — numerical and scientific computing
- **llama.cpp** — local GGUF model inference
- **IBM Granite** — local language-model explanation
- **HTML, CSS and JavaScript** — web interface
- **Git and GitHub** — version control and source hosting

## IBM LinuxONE Deployment

TrustTrace was developed and tested on an IBM LinuxONE Community Cloud instance running Ubuntu 24.04 on `s390x`.

The application API listens on `127.0.0.1:8000`, while the local Granite inference server listens on `127.0.0.1:8080`. These services are bound to localhost rather than exposed directly to the public internet.

A local SSH tunnel can be used to access the web interface from a development computer.

## Machine-Learning Experiment

The repository includes scripts for generating a synthetic dataset and training a scikit-learn logistic regression classifier.

- Dataset generation: `model/create_dataset.py`
- Model training: `model/train_model.py`
- Dataset: `data/synthetic_sellers.csv`
- Demo evidence: `data/demo_sellers.json`

The synthetic labels are generated from illustrative rules. Consequently, the reported evaluation metrics measure agreement with those generated labels—not accuracy on real sellers or actual fraud cases.

The trained model is an experimental component and should not be interpreted as a validated production fraud detector.

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /` | Web interface |
| `GET /health` | Service health check |
| `GET /demo-sellers` | Demonstration seller records |
| `POST /analyze` | Assess a listing using the implemented analysis pipeline |
| `POST /explain` | Generate an evidence-based explanation, using the local LLM when available |

Example request:

```json
{
  "link": "https://demo.trusttrace.test/product/012"
}
```

The demonstration URLs represent synthetic scenarios; they are not verified external seller listings.

## Running the Application

Run the commands on the configured LinuxONE instance from the project directory.

### 1. Install system dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3-sklearn python3-numpy python3-scipy
```

### 2. Install application dependencies

Activate the existing virtual environment:

```bash
cd ~/trusttrace
source .venv/bin/activate
pip install fastapi uvicorn httpx
```

### 3. Start the local Granite server

Build or install a compatible `llama.cpp` version for IBM Z/LinuxONE and obtain a compatible Granite GGUF model.

With the configured local model and server executable available:

```bash
nohup ~/trusttrace/llama.cpp/build/bin/llama-server \
  -m ~/trusttrace/models/granite-1b-be-04.Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  -c 1024 \
  -t 2 \
  > ~/trusttrace/granite.log 2>&1 &
```

Check the log to confirm that the model loaded and the server is listening before testing the LLM integration.

### 4. Start the API

In another terminal, from the project directory:

```bash
cd ~/trusttrace
source .venv/bin/activate
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

If the API is already running, do not start a duplicate server.

### 5. Verify the service

```bash
curl -s http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "TrustTrace"
}
```

For local browser access, create an SSH tunnel from your development computer:

```bash
ssh -i "PATH_TO_YOUR_PRIVATE_KEY" \
  -N -L 8000:127.0.0.1:8000 \
  linux1@YOUR_LINUXONE_IP
```

Keep the tunnel open and visit `http://127.0.0.1:8000/`.

Replace the placeholders with your own connection details. Never commit your private key or credentials to GitHub.

## Responsible Use and Limitations

- Demonstration evidence and dataset labels are synthetic.
- A risk score is an indicator for further checking, not a probability of fraud.
- Missing evidence must be treated as unknown, not automatically suspicious.
- Model metrics on synthetic labels do not establish real-world performance.
- Generated explanations must remain grounded in supplied evidence.
- Production use would require verified data sources, representative real-world validation, security testing, privacy safeguards, and ongoing monitoring.

TrustTrace is a hackathon prototype and is not a substitute for independent verification or protected payment methods.

## Open-Source Software

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [scikit-learn](https://scikit-learn.org/)
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [IBM Granite](https://huggingface.co/ibm-granite)

Consult each project's licence and the specific model's licence before redistribution or commercial use.

---

**TrustTrace — Don't just trust the page. Check the evidence.**
