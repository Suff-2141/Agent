import google.generativeai as genai

class LLMHandler:
    def __init__(self, api_key, model_name="gemini-pro"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt, max_output_tokens=500):
        try:
            resp = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_output_tokens,
                    temperature=0.1
                )
            )
            return resp.text.strip()
        except Exception as e:
            print("LLM error:", e)
            return None
