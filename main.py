import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
import io
import json


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


client = None
if GROQ_API_KEY:
    try:
        client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq Client Initialized")
    except Exception as e:
        print(f"⚠️ Groq Error: {e}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MOCK_RESPONSE = {
    "management_tone": "Cautiously Optimistic (Mock Data)",
    "tone_evidence": "We see strong demand but are monitoring raw material costs.",
    "key_concerns": ["Inflationary pressure impacting margins", "Supply chain delays in the EU region"],
    "key_positives": ["Record order book of $500M", "New plant operational ahead of schedule"],
    "guidance": {"Revenue": "10-12% growth", "Margins": "Expand by 50bps"},
    "confidence_score": "High (Simulation Mode)"
}

def extract_text_from_pdf(file_content: bytes) -> str:
    print("... Attempting to read PDF ...")
    try:
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            extract = page.extract_text()
            if extract:
                text += extract + "\n"
        return text
    except Exception as e:
        print(f"❌ PDF Error: {e}")
        return ""

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    print(f"\n📥 Received file: {file.filename}")
    
    
    content = await file.read()
    text_content = ""

    
    if file.content_type == "application/pdf" or file.filename.endswith(".pdf"):
        text_content = extract_text_from_pdf(content)
    else:
        try:
            text_content = content.decode("utf-8")
        except UnicodeDecodeError:
            print("⚠️ UTF-8 failed, trying Latin-1...")
            try:
                text_content = content.decode("latin-1")
            except:
                text_content = ""

    
    if not text_content or not text_content.strip():
        print("⚠️ Empty text detected. Switching to Fallback.")
        return {"filename": file.filename, "analysis": json.dumps(MOCK_RESPONSE)}

    print(f"✅ Text extracted! Length: {len(text_content)} chars")

    
    print("... Sending to Groq ...")
    
    
    prompt = f"""
    You are a Senior Financial Analyst. Analyze this earnings call transcript or financial document in detail.
    
    Your goal is to extract specific, actionable insights, not generic summaries. 
    Focus on numbers, specific project names, and direct causes/effects.

    Input Text: {text_content[:35000]}
    
    Return a valid JSON object with the following fields:
    
    1. "management_tone": A short phrase (e.g., "Highly Confident", "Cautious").
    2. "tone_evidence": A detailed sentence explaining WHY, citing specific quotes or metrics mentioned.
    3. "key_concerns": A list of 3-5 specific risks. Do not just say "Supply Chain". Say "Supply chain disruptions in the Red Sea impacting Q3 deliveries".
    4. "key_positives": A list of 3-5 specific wins. Include numbers (e.g., "Revenue grew 20% to $5B" instead of just "Revenue grew").
    5. "guidance": A dictionary or list of forward-looking targets (Revenue, Margins, Capex, Volume) with specific numbers/dates.
    6. "confidence_score": Your confidence in this analysis (High/Medium/Low).

    IMPORTANT: Return ONLY raw JSON. No Markdown formatting (```json).
    """
    
    try:
        if not client:
            raise Exception("No API Key configured")

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", 
            temperature=0.1, 
            max_tokens=2000  
        )
        
        response_text = chat_completion.choices[0].message.content
        print("✅ Groq Responded!")
        
        
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        return {"filename": file.filename, "analysis": clean_json}
        
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return {"filename": file.filename, "analysis": json.dumps(MOCK_RESPONSE)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)