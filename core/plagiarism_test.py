import asyncio
import aiohttp
import json
from dotenv import load_dotenv
import os

# Load environment variables once at module level
load_dotenv()
PLAGIARISM_API_KEY = os.environ.get("plagiarism_api")


async def check_plagiarism(text, language="en", country="us", display_results=True):
    """
    Asynchronously checks text for plagiarism using Winston AI API.

    Args:
        text (str): The text to check for plagiarism
        language (str, optional): Language code. Defaults to "en".
        country (str, optional): Country code. Defaults to "us".
        display_results (bool, optional): Whether to print results. Defaults to True.

    Returns:
        dict: A dictionary containing plagiarism check results or error details
    """
    url = "https://api.gowinston.ai/v2/plagiarism"

    payload = {"text": text, "language": language, "country": country}

    headers = {
        "Authorization": f"Bearer {PLAGIARISM_API_KEY}",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            status_code = response.status
            response_text = await response.text()

            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                return {
                    "error": "Invalid JSON response from API",
                    "status_code": status_code,
                    "response_text": response_text,
                }

            # Check if the expected "result" key is in the response
            if "result" not in result:
                return {
                    "error": "Unexpected API response structure",
                    "status_code": status_code,
                    "response_text": response_text,
                }

            # Extract relevant information
            plagiarism_result = {
                "status_code": status_code,
                "plagiarism_detected": result["result"].get("score", 0) > 0,
                "plagiarism_score": result["result"].get("score", 0),
                "total_words": result["result"].get("textWordCounts", 0),
                "plagiarized_words": result["result"].get("totalPlagiarismWords", 0),
                "sources": result.get("sources", []),
                "credits_used": result.get("credits_used"),
                "credits_remaining": result.get("credits_remaining"),
                "raw_response": result,  # Include full response for debugging
            }

            if display_results:
                print("\nPLAGIARISM DETECTION RESULTS:")
                print("-----------------------------")
                print(f"Status Code: {plagiarism_result['status_code']}")
                print(f"Plagiarism Score: {plagiarism_result['plagiarism_score']}%")
                print(f"Total Words: {plagiarism_result['total_words']}")
                print(f"Plagiarized Words: {plagiarism_result['plagiarized_words']}")

                if plagiarism_result["plagiarism_detected"]:
                    print("\nPLAGIARISM DETECTED!")
                    if plagiarism_result["sources"]:
                        print("\nSources detected:")
                        for i, source in enumerate(plagiarism_result["sources"], 1):
                            print(f"  {i}. {source.get('url', 'Unknown source')}")
                else:
                    print("\nNo plagiarism detected. The text appears to be original.")

                print(f"\nCredits used: {plagiarism_result['credits_used']}")
                print(f"Credits remaining: {plagiarism_result['credits_remaining']}")

            return plagiarism_result, plagiarism_result["plagiarism_score"]


async def main():
    sample_text = """
    Rohit Sharma (born 30 April 1987) is an Indian international cricketer and the captain of Indian cricket team in Test and ODI formats. He is widely regarded as one of the greatest ODI opening batters of all time. He is a right-handed batsman who plays for Mumbai Indians in Indian Premier League and for Mumbai in domestic cricket.
    """

    result, plagiarism_score = await check_plagiarism(sample_text)

    if "error" in result:
        print(f"Error: {result['error']}")
        print(f"Status Code: {result['status_code']}")
        print(f"Response: {result['response_text']}")
    print(plagiarism_score)


if __name__ == "__main__":
    asyncio.run(main())
