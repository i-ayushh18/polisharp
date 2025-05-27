from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from urllib.request import HTTPRedirectHandler, build_opener, install_opener, urlretrieve
from requests import RequestException, head
import google.generativeai as genai
from re import DOTALL, search
import json
import os
import logging
from dotenv import load_dotenv


logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


PROMPT = """
Read this pdf carefully.
Extract information and all important data policy points.
Arrange them in a serialized JSON without formatting.
Schema should be like this:

{
    companyName: "",
    dataPolicyPoints: [
        {
            "dataCollected": "",
            "purpose": "",
            "retentionPeriod": "",
            "criticality": ""
        }
    ]
}

Try to be as correct as possible.
"""

app = FastAPI(
    title="PoliSharp",
    description="FastAPI backend for Polisharp using Gemini",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://polisharp-1.onrender.com"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


FILE_PATH = "policies.pdf"


@app.get("/url")
def process_from_url(url: str, api_key: Optional[str] = None):
    try:
        logger.debug(f"URL specified as: {url}")
        download_file(url)
        return process(api_key)
    except HTTPException as e:
        return {"status": "error", "detail": e.detail}

@app.post("/file")
async def process_from_file(file: UploadFile = File(...), api_key: Optional[str] = Form(None)):
    try:
        with open(FILE_PATH, "wb") as pdf:
            content = await file.read()
            pdf.write(content)
            logger.debug("PDF upload successful")
        return process(api_key)
    except HTTPException as e:
        return {"status": "error", "detail": e.detail}
    except Exception as e:
        logger.error(f"Unexpected error during file processing: {e}")
        return {"status": "error", "detail": str(e)}


def process(api_key: Optional[str] = None) -> dict:
    try:
        response_text = upload_and_query_gemini(api_key)
        response_json = jsonify(response_text)
        return {"status": "success", "response": response_json}
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Error Encountered: {e}")
    finally:
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)

def download_file(url: str):
    try:
        content_type = head(url, allow_redirects=True, timeout=5).headers.get('Content-Type', '')
        if 'application/pdf' not in content_type:
            raise HTTPException(status_code=400, detail="The URL does not contain a valid PDF file.")

        opener = build_opener(HTTPRedirectHandler())
        install_opener(opener)
        urlretrieve(url, FILE_PATH)
    except RequestException:
        raise HTTPException(status_code=400, detail="Unable to fetch the PDF from the specified URL.")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error while downloading the file.")


def upload_and_query_gemini(api_key: Optional[str] = None) -> str:
    try:
        if not api_key:
            load_dotenv(override=True)
            api_key = os.getenv("GEMINI_API_KEY")
            logger.debug("Loading Gemini API key from environment")

        if not api_key:
            raise HTTPException(status_code=401, detail="API key for Gemini is missing.")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        pdf = genai.upload_file(FILE_PATH, mime_type="application/pdf")
        response = model.generate_content([PROMPT, pdf])
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise HTTPException(status_code=500, detail="Gemini API error.")


def jsonify(text: str) -> dict:
    json_pattern = r'(\{.*\})'
    match = search(json_pattern, text, DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except:
            raise HTTPException(status_code=400, detail="Cannot parse JSON from Gemini response.")
    
    raise HTTPException(status_code=404, detail="No JSON found in response.")
