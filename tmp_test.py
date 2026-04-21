import sys
import asyncio
import os
sys.path.append(os.path.join(os.getcwd(), "backend"))
from main import validate_and_correct_score
from rag_pipeline import run_autopsy

ideas = [
    "A tool that helps developers write better commit messages using AI",
    "Uber for dog walkers",
    "Premium smart juice press that connects to WiFi",
    "A new social network to replace Twitter",
    "SaaS tool for restaurant inventory management"
]

async def test():
    for idea in ideas:
        print(f"--- Testing idea: {idea} ---")
        result = await run_autopsy(idea)
        if "error" in result:
            print("Error:", result["error"])
            continue
        original_score = result.get('deathScore')
        final_result = validate_and_correct_score(result)
        print(f"Original LLM Score: {original_score}")
        print(f"Final Calibrated Score: {final_result.get('deathScore')}")
        print(f"Verdict: {final_result.get('verdict')}\n")

if __name__ == "__main__":
    asyncio.run(test())
