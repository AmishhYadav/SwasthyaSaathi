import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

try:
    print("Testing get_faq_agent with the new implementation in rag.py...")
    from app.rag import get_faq_agent
    qa = get_faq_agent()
    
    if qa is None:
        print("Agent failed to initialize (this might be expected if the API key is completely invalid or offline).")
    else:
        print("Agent initialized successfully with gemini-1.5-flash.")
        query = "What is dengue?"
        print(f"Invoking agent with query: {query}")
        result = qa.invoke(query)
        print("Result received:")
        print(result)
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
