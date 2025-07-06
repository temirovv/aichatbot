import google.generativeai as genai
from loader import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)
generation_config = genai.types.GenerationConfig(
    temperature=0.7,
)
model = genai.GenerativeModel(model_name="gemini-2.0-flash",
                             generation_config=generation_config)


def make_converstaion(prompt: str):
    try:
        chat = model.start_chat()
        res = chat.send_message(prompt,generation_config=generation_config)
        return res.text
    except Exception:
        return


