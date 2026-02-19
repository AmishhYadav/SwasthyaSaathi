from fastapi import FastAPI
from pydantic import BaseModel
from app import router
import asyncio
from concurrent.futures import ThreadPoolExecutor
from google.api_core import exceptions as google_exceptions

app = FastAPI(title="SwasthyaSathi API", description="AI Public Health Chatbot for India")

executor = ThreadPoolExecutor(max_workers=4)

class Query(BaseModel):
    From: str
    Body: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/query")
async def query(data: Query):
    try:
        user_msg = data.Body
        user_id = data.From or "demo"

        try:
            # Use the semantic router to dispatch to the correct agent
            if hasattr(asyncio, 'to_thread'):
                answer = await asyncio.wait_for(
                    asyncio.to_thread(router.route, user_id, user_msg),
                    timeout=50.0
                )
            else:
                loop = asyncio.get_event_loop()
                answer = await asyncio.wait_for(
                    loop.run_in_executor(executor, router.route, user_id, user_msg),
                    timeout=50.0
                )
            
            if not answer:
                answer = "⚠️ Error: No answer returned from the model."
                
            return {"answer": answer}
            
        except asyncio.TimeoutError:
            return {"answer": "⚠️ Error: The request timed out. Please try again."}
        except google_exceptions.ResourceExhausted as e:
            return {
                "answer": "⚠️ API Quota Exceeded: Your Gemini API quota has been exceeded. "
                         "Please check your plan or try again later."
            }
    except Exception as e:
        print(f"Error during query processing: {e}")
        return {"answer": f"⚠️ System Error: {str(e)[:300]}"}
