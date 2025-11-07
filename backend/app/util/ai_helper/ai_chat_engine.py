from app.config.ai_helper import llm
from app.util.ai_helper.summarize_conversation import summarize_conversation
from app.model.chat import Chat
from app.model.conversation import Conversation
from langchain.prompts import PromptTemplate

def ai_chat_engine(user_question: str, chat: Chat, prev_conversations: Conversation):
    conversation_summary = summarize_conversation(prev_conversations)

    template = """
You are a teacher.

Student are start from the following idea:
<context>
{initial_idea}
</context>

Summary of previous conversation:
<summary>
{conversation_summary}
</summary>

The student has asked the following question:
<question>
{user_question}
</question>

Your task:
Answer the student's question clearly and instructively.
Keep your tone educational and encouraging.

Output only the structured answer in **Markdown** format.
"""

    prompt = PromptTemplate.from_template(template.strip())
    prompt_input = {
        "initial_idea": chat.initial_idea,
        "conversation_summary": conversation_summary,
        "user_question": user_question
    }
    formatted_prompt = prompt.format(**prompt_input)

    try:
        result = llm.invoke(formatted_prompt)
        response = getattr(result, "content", str(result)).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate answer: {e}")

    response = response.removeprefix("```markdown").removesuffix("```").strip()
    return response