from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import get_faq_agent
import asyncio
from concurrent.futures import ThreadPoolExecutor
from google.api_core import exceptions as google_exceptions

app = FastAPI(title="SwasthyaSathi API", description="AI Public Health Chatbot for India")
qa = get_faq_agent()

executor = ThreadPoolExecutor(max_workers=2)

class Query(BaseModel):
    From: str
    Body: str

@app.get("/health")
async def health_check():
    return {"status": "ok", "agent_loaded": qa is not None}

@app.post("/query")
async def query(data: Query):
    try:
        user_msg = data.Body
        if qa is None:
            return {"answer": "⚠️ Error: The AI agent failed to initialize. Please check your API key and network connection."}

        try:
            if hasattr(asyncio, 'to_thread'):
                result = await asyncio.wait_for(
                    asyncio.to_thread(qa.invoke, user_msg),
                    timeout=45.0
                )
            else:
                loop = asyncio.get_event_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(executor, qa.invoke, user_msg),
                    timeout=45.0
                )
            answer = result.get("result", "⚠️ Error: No answer returned from the model.")
            return {"answer": answer}
        except asyncio.TimeoutError:
            return {"answer": "⚠️ Error: The request timed out. The AI model took too long to respond. Please try again."}
        except google_exceptions.ResourceExhausted as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                return {
                    "answer": "⚠️ API Quota Exceeded: Your Gemini API quota has been exceeded. "
                             "Please check your plan and billing details at https://ai.google.dev/gemini-api/docs/rate-limits."
                }
            else:
                return {"answer": f"⚠️ API Rate Limit Error: {error_msg[:200]}"}
    except Exception as e:
        error_str = str(e)
        print(f"Error during query processing: {e}")
        import traceback
        traceback.print_exc()

        if "quota" in error_str.lower() or "429" in error_str or "ResourceExhausted" in error_str:
            return {
                "answer": "⚠️ API Quota Exceeded: Your Gemini API quota has been exceeded. "
                         "Please check your plan and billing details."
            }

        return {"answer": f"⚠️ Error: {error_str[:300]}"}
