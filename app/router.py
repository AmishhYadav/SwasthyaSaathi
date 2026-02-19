from app import faq_agent, symptom_agent, mythbuster_agent, referral_agent, quiz_agent

def route(user_id, text):
    t = text.lower()

    if "symptom" in t:
        return symptom_agent.handle(text)
    elif "myth" in t:
        return mythbuster_agent.handle(text)
    elif "hospital" in t or "medicine" in t or "treatment" in t:
        return referral_agent.handle(text)
    elif "quiz" in t:
        return quiz_agent.start_quiz(user_id)
    elif t.strip() in ["1", "2"]:
        return quiz_agent.check_answer(user_id, t.strip())
    else:
        return faq_agent.handle(text)
