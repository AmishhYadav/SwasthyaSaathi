def handle(query: str):
    if "malaria" in query.lower():
        return "Common symptoms of malaria: fever, chills, sweating, headache, nausea."
    if "dengue" in query.lower():
        return "Common symptoms of dengue: high fever, severe headache, joint pain, skin rash."
    return "Sorry, I don’t have symptom data for that disease."
