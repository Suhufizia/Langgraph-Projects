from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        groq_api_key = self.user_controls_input.get("GROQ_API_KEY", "")
        selected_groq_model = self.user_controls_input.get("selected_groq_model", "llama3-8b-8192")
        if not groq_api_key:
            raise ValueError("GROQ API Key is required.")
        return ChatGroq(api_key=groq_api_key, model=selected_groq_model)

