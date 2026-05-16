from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

import anthropic
import os
import json

load_dotenv()

app = FastAPI()

client = anthropic.Anthropic(
   api_key=os.getenv("ANTHROPIC_API_KEY")
)

db = {}

class Query(BaseModel):
   query: str


@app.post("/queries")
async def create_query(data: Query):

   prompt = f"""
      Extract structured data from this query.

      Return ONLY raw valid JSON.
      Do not use markdown.
      Do not explain anything.

      Query: {data.query}
   """

   response = client.messages.create(
      model="claude-haiku-4-5-20251001",
      max_tokens=200,
      messages=[
            {
               "role": "user",
               "content": prompt
            }
      ]
   )

   output = response.content[0].text

   print(output) 

   output = output.strip()

   output = output.replace("```json", "")
   output = output.replace("```", "")

   structured_data = json.loads(output)

   query_id = len(db) + 1

   db[query_id] = {
      "id": query_id,
      "query": data.query,
      "data": structured_data
   }

   return db[query_id]


@app.get("/queries/{query_id}")
async def get_query(query_id: int):
   return db.get(query_id, {"error": "Query not found"})