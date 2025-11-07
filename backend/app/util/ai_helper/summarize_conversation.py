import json
from app.config.ai_helper import llm
from langchain.prompts import PromptTemplate
from app.model.conversation import Conversation

def summarize_conversation(prev_conversations: Conversation | dict):

    template = """
You are a teacher.

Summarize the following conversation between the student and teacher
<conversation>
{prev_conversations}
</conversation>

Your task:
Summarized the conversation clearly and instructively.
Keep your tone educational and encouraging.

Output only the structured answer in **Markdown** format.
"""

    prompt = PromptTemplate.from_template(template.strip())
    prompt_input = {
        "prev_conversations": json.dumps(prev_conversations)
    }
    formatted_prompt = prompt.format(**prompt_input)

    try:
        result = llm.invoke(formatted_prompt)
        response = getattr(result, "content", str(result)).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate conversation summary: {e}")

    response = response.removeprefix("```markdown").removesuffix("```").strip()
    return response