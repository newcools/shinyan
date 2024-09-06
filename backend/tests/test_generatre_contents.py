from src.ShinyanCard.ContentGeneration.ContentGenerator import generate_contents


class TestGenerateContents:
    def test_generate_content(self):
        generate_contents("より", "japanese")
