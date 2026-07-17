import unittest

from src.main import extrair_linhas


class TestExtracaoDeLinhas(unittest.TestCase):
    def test_retorna_apenas_blocos_line(self):
        resposta = {
            "Blocks": [
                {"BlockType": "PAGE", "Id": "pagina-1"},
                {"BlockType": "LINE", "Text": "Lista de materiais"},
                {"BlockType": "WORD", "Text": "Lista"},
                {"BlockType": "LINE", "Text": "1. Caderno"},
            ]
        }

        resultado = extrair_linhas(resposta)

        self.assertEqual(
            resultado,
            ["Lista de materiais", "1. Caderno"],
        )

    def test_retorna_lista_vazia_sem_blocos(self):
        self.assertEqual(extrair_linhas({}), [])


if __name__ == "__main__":
    unittest.main()
