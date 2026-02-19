user_scores = {}

def start_quiz(user_id):
    return "Quick quiz: How is malaria transmitted?\n1) Mosquito bite\n2) Contaminated food"

def check_answer(user_id, answer):
    if user_id not in user_scores:
        user_scores[user_id] = 0
    if answer.strip() == "1":
        user_scores[user_id] += 1
        return "✅ Correct! Your awareness score increased."
    else:
        return "❌ Incorrect. Correct answer: Mosquito bite."
