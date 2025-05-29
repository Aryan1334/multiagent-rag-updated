from fastapi import FastAPI, HTTPException, Request, Form
from pydantic import BaseModel
import asyncpg
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DATABASE_URL = "postgresql://postgres:root@localhost:5432/ragdb"
db_pool = None

# Pydantic model for the request body
class QuestionRequest(BaseModel):
    question: str

# DB connection management
@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    print("Database connected")

@app.on_event("shutdown")
async def shutdown():
    await db_pool.close()
    print("Database connection closed")

async def execute_query(query: str):
    async with db_pool.acquire() as connection:
        return await connection.fetch(query)

# Placeholder agent implementations
def get_relevant_schema(question: str):
    # Example: always return a fixed schema for demo purposes
    return {
        "tables": ["customers", "orders"],
        "columns": {
            "customers": ["id", "name", "email"],
            "orders": ["id", "customer_id", "amount"]
        }
    }

def generate_sql(question: str, schema: dict):
    # Dummy SQL generator - in reality, use NLP + schema to generate SQL
    if "customers" in question.lower():
        return "SELECT id, name, email FROM customers LIMIT 5;"
    if "orders" in question.lower():
        return "SELECT id, customer_id, amount FROM orders LIMIT 5;"
    # fallback
    return "SELECT 1;"

def synthesize_answer(question: str, rows):
    # Dummy synthesizer - summarize rows count
    return f"Found {len(rows)} rows matching your query."

# API endpoints
@app.post("/ask")
async def ask_question(body: QuestionRequest):
    question = body.question

    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Invalid or empty question.")

    try:
        schema = get_relevant_schema(question)
        sql_query = generate_sql(question, schema)
        rows = await execute_query(sql_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    answer = synthesize_answer(question, rows)

    return {
        "question": question,
        "schema": schema,
        "sql_query": sql_query,
        "result_rows": [dict(row) for row in rows],
        "answer": answer
    }

@app.get("/test")
async def test_db():
    try:
        rows = await execute_query("SELECT * FROM customers LIMIT 5;")
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB test failed: {str(e)}")

# Single home GET endpoint
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Home POST to ask question from form
@app.post("/", response_class=HTMLResponse)
async def ask_via_form(request: Request, question: str = Form(...)):
    if not question.strip():
        return templates.TemplateResponse("index.html", {"request": request, "result": {"answer": "Invalid question."}})

    try:
        schema = get_relevant_schema(question)
        sql_query = generate_sql(question, schema)
        rows = await execute_query(sql_query)
        answer = synthesize_answer(question, rows)

        result = {
            "answer": answer,
            "sql_query": sql_query,
            "result_rows": [dict(row) for row in rows]
        }

        return templates.TemplateResponse("index.html", {"request": request, "result": result})

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": {"answer": f"Error: {str(e)}"}
        })
