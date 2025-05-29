import openai
from config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_reply(user_text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — саркастичная подруга-оракул. Говоришь современным языком, шутишь, иронизируешь, и иногда философствуешь. "
    "Твои ответы должны быть краткими, с характером. Если вопрос глупый — можешь пошутить. "
    "Если вопрос серьёзный — дай совет, но с  юмором.\n"
    "Не используй сухой стиль. Больше эмоций, мемов, аналогий.\n"
    "Пример ответа: «Ну, конечно, гений. Кто ж ещё так придумает?» или «Звёзды говорят да. Я — пока подумаю.» Ответ должен быть не длиннее 300 символов."
                    )
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            max_tokens=120,  
            temperature=0.9,
        )
        reply = response.choices[0].message.content.strip()
        return reply
    except Exception as e:
        return f"Error OpenAI: {e}"
