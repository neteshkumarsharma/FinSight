# 📈 FinSight: AI Earnings Call Analyst

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![AI Model](https://img.shields.io/badge/AI-Llama3.3-orange)

**FinSight** is an AI-powered financial research tool that automatically analyzes earnings call transcripts and financial PDFs. It extracts key insights, management sentiment, and forward guidance using the Groq Llama 3 AI engine, helping analysts save hours of reading time.

🔗 **Live Demo:** https://finsightaianalyst.netlify.app/

---

## 🚀 Key Features

- **📄 Document Analysis:** Upload any PDF or Text file (Earnings Calls, Financial Reports).
- **🧠 AI-Powered Insights:** Extracts:
  - **Management Tone:** (e.g., "Cautiously Optimistic") with confidence scores.
  - **Forward Guidance:** Revenue targets, margin expectations, and volume goals.
  - **Key Risks:** Supply chain issues, regulatory headwinds, etc.
  - **Strategic Wins:** Deal wins, record metrics, and expansion plans.
- **🛡️ Robust Error Handling:** Includes a **"Simulation Mode"** that serves mock data if the API limit is reached or the AI service is down, ensuring the app never crashes during a demo.
- **⚡ High Performance:** Powered by Groq's LPU inference engine for near-instant analysis.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **AI Engine:** Groq API (Llama-3.3-70b-versatile)
- **PDF Processing:** `pypdf` / `pdfplumber`
- **Deployment:** Render (Backend) + Netlify (Frontend)

---

## ⚙️ Installation & Local Setup

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/neteshkumarsharma/finsight-analyst.git](https://github.com/neteshkumarsharma/finsight-analyst.git)
cd finsight-analyst
```
