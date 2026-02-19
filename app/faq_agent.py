from app.rag import get_faq_agent

qa = get_faq_agent()

def handle(query: str):
    return qa.run(query)
