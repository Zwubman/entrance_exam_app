from app.config.ai_helper import llm
from langchain.prompts import PromptTemplate

def evaluate_exam_answer(questions, answers):

    template = """
You are a teacher.

The Student is ask him the following questions:
<questions>
{questions}
</questions>

and He answer as follow:
<answers>
{answers}
</answers>

Your task:
Evaluate the student. give short answer for each questions.
and finally calculate the result in percentage.

Output requirements:
Return a valid **Markdown** format:
"""

    prompt = PromptTemplate.from_template(template.strip())
    prompt_input = {
        "questions": questions,
        "answers": answers
    }
    formatted_prompt = prompt.format(**prompt_input)

    try:
        result = llm.invoke(formatted_prompt)
        response = getattr(result, "content", str(result)).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate exam: {e}")

    response = (
        response
        .removeprefix("```markdown")
        .removesuffix("```")
        .strip()
    )
    return response