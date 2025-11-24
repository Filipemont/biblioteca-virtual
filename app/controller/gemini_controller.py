from service.gemini_service import GeminiService

class GeminiController:
    
    @staticmethod
    def get_gemini_resume(nome_livro):
        gemini_service = GeminiService()
        return gemini_service.get_resumo(nome_livro)
