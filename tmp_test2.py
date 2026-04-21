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
    with open("test_results.txt", "w", encoding="utf-8") as f:
        for idea in ideas:
            f.write(f"--- Testing idea: {idea} ---\n")
            result = await run_autopsy(idea)
            if "error" in result:
                f.write(f"Error: {result['error']}\n\n")
                continue
            original_score = result.get('deathScore')
            final_result = validate_and_correct_score(result)
            f.write(f"Original LLM Score: {original_score}\n")
            f.write(f"Final Calibrated Score: {final_result.get('deathScore')}\n")
            f.write(f"Verdict: {final_result.get('verdict')}\n\n")

if __name__ == "__main__":
    asyncio.run(test())
