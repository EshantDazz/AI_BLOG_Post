from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Any,Union,Dict
import logging
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.runnables.base import RunnableSerializable
from core.ai.prompts import ai_blog_prompt

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", max_retries=3, temperature=0.5)


class AI_Blog(BaseModel):
    """THi will contain the entire Blog content generated by AI"""

    content: str = Field(default=..., description="This will store the entire blog generated")





async def _run_chain(
    chain: RunnableSerializable[dict, Any],
    input_data: dict,
    max_retries: int = 10,
) -> Union[str, Dict[str, str]]:
    """Helper function to run a given chain with retries."""
    for attempt in range(1, max_retries + 1):
        try:
            return await chain.ainvoke(input_data)
        except Exception as e:
            logging.error(
                f"Error during 'ainvoke' execution (Attempt {attempt}/{max_retries}): {e}"
            )
            if attempt < max_retries:
                logging.info("Retrying...")
                await asyncio.sleep(1)
            else:
                return {"error": f"Failed after maximum retries. {e}"}

async def return_ai_blog_content(
    topic: str,
    keywords:str,
    lsi_keywords:str,
    content_angle:str,
    density:str,
    product:str,
    max_retries: int = 10,
):
    """Return a list of string about all the technical skills mentioned in the cv"""
    try:
        llms = llm.with_structured_output(schema=AI_Blog)
        chain=ai_blog_prompt|llms
        input_data: Dict[str, str] = {"topic":topic,"keywords":keywords,"LSI_keywords":lsi_keywords,"content_angle":content_angle,"density":density,"product":product}
        result: str | Dict[str, str] = await _run_chain(chain=chain, input_data=input_data, max_retries=max_retries)
        return result

    except Exception as e:
        logging.error(f"Unexpected error in generate_follow_up_question: {e}")
        return "An unexpected error occured"