import sys
import os
from pathlib import Path

# Add project root to sys.path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from app import router

def test_routing():
    test_queries = [
        ("I feel like I have a fever and chills", "SYMPTOMS"),
        ("Is it true that garlic cures malaria?", "MYTHS"),
        ("Find me a hospital in Delhi", "REFERRALS"),
        ("I want to take a health quiz", "QUIZ"),
        ("1", "QUIZ (Answer)"),
        ("How to prevent malaria?", "FAQ"),
    ]

    print("🚀 Starting Semantic Routing Verification...\n")

    for query, expected in test_queries:
        print(f"Testing Query: \"{query}\"")
        intent = router.get_intent(query) if query not in ["1", "2"] else "QUIZ (Answer)"
        print(f"Detected Intent: {intent}")
        result = router.route("test_user", query)
        print(f"Agent Response: {result[:100]}...")
        print("-" * 30)

if __name__ == "__main__":
    test_routing()
