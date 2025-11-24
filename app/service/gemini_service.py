from google import genai
from google.genai import types


class GeminiService:
    CLIENT = genai.Client()

    def get_resumo(self, nome_livro):
        try:
            response = self.CLIENT.models.generate_content(
                model="gemini-2.5-flash", contents=(
                    f'Levando em consideração o contexto de uma biblioteca virtual,'
                    f'faça um resumo do livro  {nome_livro}, faça o resumo com no mínimo 7 parágrafos' 
                ),
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0) 
                ),
            )
            mensagem = {'resumo':f'```{response.text}```'}
            return mensagem
        except Exception:
            mensagem = {
                'resumo': 'Não foi possível gerar o seu resumo, tente novamente'
            }
            return mensagem
