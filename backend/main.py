import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def load_data():
      try:
                df = pd.read_excel("data.xlsx")
                return df.to_string()
except Exception as e:
        print(f"Error loading Excel: {e}")
        return "No data loaded."

EXCEL_CONTENT = load_data()

@app.get("/")
def home():
      return {"status": "online"}

@app.post("/query")
async def query_excel(data: dict):
      query = data.get("query")
      if not query:
                raise HTTPException(status_code=400, detail="Query required")

      try:
                response = client.chat.completions.create(
                              messages=[
                                                {"role": "system", "content": f"Answer based on: {EXCEL_CONTENT}"},
                                                {"role": "user", "content": query}
                              ],
                              model="llama3-70b-8192",
                )
                return {"response": response.choices[0].message.content}
except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
      import uvicorn
      print(f"Key Loaded: {GROQ_API_KEY[:7]}...{GROQ_API_KEY[-5:]}")
      uvicorn.run(app, host="0.0.0.0", port=8000)
