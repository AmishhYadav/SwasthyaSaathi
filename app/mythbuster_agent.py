def handle(query: str):
    if "garlic" in query.lower() and "malaria" in query.lower():
        return "Myth: Garlic does NOT cure malaria. Treatment requires medical attention."
    if "papaya" in query.lower() and "dengue" in query.lower():
        return "Myth: Papaya leaf extract is not a proven cure for dengue. Only supportive treatment works."
    return "I couldn't match that myth. Please consult verified sources."
