import json
from . import llm
from langchain.prompts import PromptTemplate

def generate_exams(context, questions_length):

    template = """
You are a teacher.

Context:
<context>
{context}
</context>

Your task:
Create {questions_length} multiple-choice questions for the student's based on the above context.
Each question must:
- Be relevant to the student's completed learning plan.
- Include **exactly four distinct options** (A–D).
- Have **one correct answer** (but do not mark it in output).

Output requirements:
Return a valid **JSON array** following this structure:

[
  {{
    "question": "string",
    "options": {{
      "A": "string",
      "B": "string",
      "C": "string",
      "D": "string"
    }}
  }}
]

Ensure the output is strictly valid JSON, with no explanations or extra text.
"""

    prompt = PromptTemplate.from_template(template.strip())
    prompt_input = {
        "context": context,
        "questions_length": questions_length
    }
    formatted_prompt = prompt.format(**prompt_input)

    try:
        result = llm.invoke(formatted_prompt)
        response = getattr(result, "content", str(result)).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate exam: {e}")

    response = (
        response
        .removeprefix("```json")
        .removesuffix("```")
        .strip()
    )

    try:
        data = json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by LLM. First 200 chars:\n{response[:200]}"
        )

    if not isinstance(data, list) or not all("question" in q and "options" in q for q in data):
        raise ValueError("Generated exam does not match expected schema.")

    return data