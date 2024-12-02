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

PROMPT="""
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
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

FILE_PATH="policies.pdf"

@app.get("/url/")
def process_from_url(url: str, api_key: Optional[str] = None):
    try:
        logger.debug(f"URL specified as: {url}")
        download_file(url)
        return process(api_key)
    except HTTPException as e:
        return {"status": "error", "detail": e.detail}
    

@app.post("/file/")
async def process_from_file(file: UploadFile = File(...), api_key: Optional[str] = Form(...)):
    try:
        with open(FILE_PATH, "wb") as pdf:
            content = await file.read()
            pdf.write(content)
            return process(api_key)
    except HTTPException as e:
        return {"status": "error", "detail": e.detail}
    except Exception:
        return {"status": "error", "detail": "File upload failed !! Please try again"}

def process(api_key: Optional[str] = None) -> str:
    try:
        response_text = upload_and_query_gemini(api_key)

        response_json = jsonify(response_text)

        return {"status": "success", "response": response_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Encountered: {e}")
    finally:
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)
    

def download_file(url: str):
    try:
        if head(url, allow_redirects=True, timeout=5).headers.get('Content-Type', '') != 'application/pdf':
            raise HTTPException(status_code=400, detail="The URL doesn't contain a PDF file. Enter a valid URL")
        
        opener = build_opener(HTTPRedirectHandler())
        install_opener(opener)
        urlretrieve(url, FILE_PATH)
    except RequestException:
        raise HTTPException(status_code=400, detail="We are unable to get PDF from the specified URL. Please give us some time.")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error while downloading. Please retry later.")
    

def upload_and_query_gemini(api_key: Optional[str] = None) -> str:
    try:

        if api_key == None or api_key == '':
            load_dotenv(override=True)
            api_key=os.getenv("GEMINI_API_KEY")
            logger.debug("Loading api key from environment")

        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel("gemini-1.5-flash")

        pdf = genai.upload_file(FILE_PATH, mime_type="application/pdf")

        response = model.generate_content([PROMPT, pdf])

        return response.text
    
    except:
        raise HTTPException(status_code=500, detail="Gemini API error.")
    

def jsonify(text: str) -> str:
    json_pattern = r'(\{.*\})'
    match = search(json_pattern, text, DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except:
            raise HTTPException(status_code=400, detail="Cannot extract json from response")
    
    raise HTTPException(status_code=404, detail="No json found in response")