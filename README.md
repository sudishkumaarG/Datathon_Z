# TrustTrace — Evidence-Based Seller Risk Assessment

**IBM Z Datathon 2026 | IBM LinuxONE | Edge AI / Machine Learning**

TrustTrace is a prototype that helps online shoppers assess potential seller risk using observable listing and profile indicators. It combines evidence-based rules, a synthetic-data machine-learning experiment, and a locally hosted IBM Granite language model to generate understandable risk reports.

> **Important:** This prototype uses synthetic demonstration data. Its scores are illustrative assessments, not proof of fraud or validated real-world scam-detection predictions.

## The Problem

Online shoppers may encounter unusually low prices, reused product images, and newly created seller accounts. TrustTrace combines available indicators into one explainable assessment and distinguishes missing information from established risk indicators.

## Features

- Illustrative risk score from 0–10.
- Risk level and confidence indication.
- Evidence-based explanations and practical precautions.
- Local IBM Granite explanations when the inference service is available.
- Synthetic-data machine-learning experiment.
- Web interface and FastAPI endpoints.

Risk indicators do not prove fraud, and missing data does not automatically make a seller suspicious.

## Architecture

```text
Listing Link
    |
    v
FastAPI Backend
    |
    v
Evidence and Risk Assessment
    |
    +----> Rules
    +----> Synthetic-data ML experiment
    +----> Local IBM Granite LLM
    |
    v
Evidence Report and Web Interface
```

The prototype runs on IBM LinuxONE Community Cloud, using Ubuntu Linux on the `s390x` architecture. The API listens on `127.0.0.1:8000` and the local Granite server on `127.0.0.1:8080`.

## Technology Stack

- Python, FastAPI and Uvicorn
- scikit-learn, NumPy and SciPy
- llama.cpp and IBM Granite
- HTML, CSS and JavaScript
- Git and GitHub

## Machine-Learning Experiment

- Dataset generator: `model/create_dataset.py`
- Training script: `model/train_model.py`
- Dataset: `data/synthetic_sellers.csv`
- Demo evidence: `data/demo_sellers.json`

The synthetic labels are generated from illustrative rules. Therefore, evaluation metrics measure agreement with those labels—not performance on real sellers or actual fraud cases. This is an experimental prototype, not a validated production fraud detector.

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /` | Web interface |
| `GET /health` | Health check |
| `GET /demo-sellers` | Synthetic demonstration records |
| `POST /analyze` | Assess a listing |
| `POST /explain` | Generate an evidence-based explanation |

Example request:

```json
{
  "link": "https://demo.trusttrace.test/product/012"
}
```

Demo URLs represent synthetic scenarios, not verified external seller listings.

## Setup and Run

On the configured LinuxONE instance:

```bash
sudo apt-get update
sudo apt-get install -y python3-sklearn python3-numpy python3-scipy

cd ~/trusttrace
source .venv/bin/activate
pip install fastapi uvicorn httpx
```

Start the configured local Granite server in a separate terminal:

```bash
nohup ~/trusttrace/llama.cpp/build/bin/llama-server \
  -m ~/trusttrace/models/granite-1b-be-04.Q4_K_M.gguf \
  --host 127.0.0.1 --port 8080 -c 1024 -t 2 \
  > ~/trusttrace/granite.log 2>&1 &
```

Confirm that the model loads successfully before testing LLM explanations.

Start the API:

```bash
cd ~/trusttrace
source .venv/bin/activate
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

If the API is already running, do not start a duplicate instance.

Verify:

```bash
curl -s http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok","service":"TrustTrace"}
```

For browser access from your development computer, use an SSH tunnel:

```bash
ssh -i "PATH_TO_YOUR_PRIVATE_KEY" \
  -N -L 8000:127.0.0.1:8000 \
  linux1@YOUR_LINUXONE_IP
```

Keep the tunnel open and visit `http://127.0.0.1:8000/`. Replace the placeholders with your connection details. Never commit private keys or credentials.

The `llama.cpp` source/build directory and local model file are excluded from the repository. A compatible `llama.cpp` build and model must be installed separately.

## Responsible Use and Limitations

- Demonstration records and dataset labels are synthetic.
- A score is an indicator for further checking, not a probability of fraud.
- Missing evidence is unknown, not automatically suspicious.
- Synthetic evaluation metrics do not establish real-world performance.
- Generated explanations must remain grounded in supplied evidence.
- Production use requires verified sources, representative validation, security testing, privacy safeguards and ongoing monitoring.

TrustTrace is a hackathon prototype, not a substitute for independent verification or protected payment methods.

## Open-Source Software

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [scikit-learn](https://scikit-learn.org/)
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [IBM Granite](https://huggingface.co/ibm-granite)

Review each software and model licence before redistribution or commercial use.

---

**TrustTrace — Don't just trust the page. Check the evidence.**
