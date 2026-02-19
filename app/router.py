from app.rag import get_llm
from app import faq_agent, symptom_agent, mythbuster_agent, referral_agent, quiz_agent

llm = get_llm()

def get_intent(text):
    """Classify user intent using LLM."""
    if not llm:
        return "FAQ"
    
    prompt = f"""
    Analyze the following user health-related query and classify it into EXACTLY ONE of these categories:
    - SYMPTOMS: User is describing feeling unwell or asking about signs of a disease.
    - MYTHS: User is asking if a common belief or home remedy is true.
    - REFERRALS: User is asking for hospitals, doctors, or where to buy medicine.
    - QUIZ: User wants to play a game, test their knowledge, or start a health quiz.
    - FAQ: General health questions or everything else.

    User Query: "{text}"
    Category:"""
    
    try:
        response = llm.invoke(prompt)
        intent = response.content.strip().upper()
        # Clean up response
        for category in ["SYMPTOMS", "MYTHS", "REFERRALS", "QUIZ", "FAQ"]:
            if category in intent:
                return category
        return "FAQ"
    except Exception as e:
        print(f"Routing error: {e}")
        return "FAQ"

def route(user_id, text):
    # Special case: Quick check for quiz answers (numerical)
    t = text.strip()
    if t in ["1", "2"]:
        return quiz_agent.check_answer(user_id, t)

    intent = get_intent(text)

    if intent == "SYMPTOMS":
        return symptom_agent.handle(text)
    elif intent == "MYTHS":
        return mythbuster_agent.handle(text)
    elif intent == "REFERRALS":
        return referral_agent.handle(text)
    elif intent == "QUIZ":
        return quiz_agent.start_quiz(user_id)
    else:
        return faq_agent.handle(text)
