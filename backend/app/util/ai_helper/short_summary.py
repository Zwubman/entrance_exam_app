from app.config.ai_helper import llm
from langchain.prompts import PromptTemplate

def short_summary(text):

    template = """
You are a teacher.

Summarize the following text in single and too short phrase
<context>
{text}
</context>

Your task:
Summarized the text clearly and instructively.
Keep your tone educational and encouraging.

Output only the structured answer in text format.
"""

    prompt = PromptTemplate.from_template(template.strip())
    prompt_input = {
        "text": text
    }
    formatted_prompt = prompt.format(**prompt_input)

    try:
        result = llm.invoke(formatted_prompt)
        response = getattr(result, "content", str(result)).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate short summary: {e}")

    response = response.removeprefix("```text").removesuffix("```").strip()
    return response