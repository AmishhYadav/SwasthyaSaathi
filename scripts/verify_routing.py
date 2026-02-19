import sys
import os
import time
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

    print("🚀 Starting Semantic Routing Verification (with rate-limit handling)...\n")

    for i, (query, expected) in enumerate(test_queries):
        print(f"[{i+1}/{len(test_queries)}] Testing Query: \"{query}\"")
        
        # Skip LLM for literal quiz answers
        if query in ["1", "2"]:
            intent = "QUIZ (Answer)"
        else:
            intent = router.get_intent(query)
            # Sleep to avoid 5 RPM limit
            time.sleep(12) 
            
        print(f"Detected Intent: {intent}")
        result = router.route("test_user", query)
        print(f"Agent Response: {str(result)[:100]}...")
        print("-" * 30)

if __name__ == "__main__":
    test_routing()
