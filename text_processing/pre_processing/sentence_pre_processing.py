import re
from .abreviation_dict import ABBREVIATIONS_DICT


class SentencePreProcessing:

    def process_text(self, text: str) -> str:
        text = self.convert_lowercase(text)
        text = self.remove_invisible_spaces(text)
        text = self.remove_emojis(text)
        text = self.remove_html_tags(text)
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.remove_mentions(text)
        text = self.remove_hashtags(text)
        text = self.remove_phone_numbers(text)
        text = self.normalize_laughs(text)
        text = self.remove_duplicate_punctuations(text)
        text = self.remove_duplicate_spaces(text)
        text = self.expand_abbreviations(text)
        return text

    def convert_lowercase(self, text: str) -> str:
        return text.lower()

    def remove_invisible_spaces(self, text: str) -> str:
        return re.sub(r"[\u200b]", "", text)

    def remove_duplicate_spaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def expand_abbreviations(self, text: str) -> str:
        final_sentence = ""
        for word in text.split():
            final_sentence += ABBREVIATIONS_DICT.get(word, word) + " "
        return final_sentence

    def remove_emojis(self, text: str) -> str:
        emoji_pattern = re.compile(
            "["
            "\U0001f600-\U0001f64f"  # emoticons
            "\U0001f300-\U0001f5ff"  # symbols & pictographs
            "\U0001f680-\U0001f6ff"  # transport & map symbols
            "\U0001f1e0-\U0001f1ff"  # flags
            "\U00002700-\U000027bf"  # Dingbats
            "\U0001f900-\U0001f9ff"  # Supplemental Symbols and Pictographs
            "\U00002600-\U000026ff"  # Misc symbols
            "\U00002b50"  # Star
            "\U00002b06"  # Up arrow
            "\U0001fa70-\U0001faff"  # Symbols and Pictographs Extended-A
            "\U000025a0-\U000025ff"  # Geometric Shapes
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", text)

    def remove_html_tags(self, text: str) -> str:
        return re.sub(r"<.*?>", "", text)

    def remove_urls(self, text: str) -> str:
        return re.sub(r"(https?://\S+|www\.\S+)", "", text)

    def remove_emails(self, text: str) -> str:
        return re.sub(r"\S+@\S+\.\S+", "", text)

    def remove_mentions(self, text: str) -> str:
        return re.sub(r"@\w+", "", text)

    def remove_hashtags(self, text: str) -> str:
        return re.sub(r"#\w+", "", text)

    def remove_phone_numbers(self, text: str) -> str:
        return re.sub(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", "", text)

    def normalize_laughs(self, text: str) -> str:
        return re.sub(r"\b(k{2,}|rs{2,}|ha(ha)+|he(he)+|hue{2,})\b", " LAUGH ", text)

    def remove_duplicate_punctuations(self, text: str) -> str:
        return re.sub(r"([!?.\-])\1+", r"\1", text)


if __name__ == "__main__":
    pre_processor = SentencePreProcessing()
    test_chat_messages = [
        # 1. abreviações + emoji
        "Oi vc tá bem? 😊",
        # 2. múltiplos espaços + “risada”
        "kkkk   esse meme é mt bom kkkk",
        # 3. link encurtado + “please”
        "manda o link pfv 👉 https://bit.ly/3abcXYZ",
        # 5. CAPS LOCK + pontuação repetida
        "CHEGUEI!!!!!!!!",
        # 6. menção estilo rede social
        "@theo_coelho vc viu aquele post?",
        # 7. hashtag
        "Tô viciado nessa série #incrível",
        # 8. emoji no meio da palavra
        "Essa pizza tá uma delíciaaaa 🍕🤤",
        # 9. erros de digitação comuns
        "Nao consigo logar no sistma, ajuda ae",
        # 10. contração informal
        "cê vem hj à noite?",
        # 11. negação dupla + repetição
        "eu NÃO aceito não!!!",
        # 12. HTML perdido
        "<div>Promo! Só hj 50% off</div>",
        # 13. URL longa + emoji
        "Confere aqui: https://www.minhaempresa.com.br/produto/123 😎",
        # 14. risada alternativa
        "rsrsrs, entendi nada 😂",
        # 15. código/ID específico
        "Pedido #000123-A foi enviado.",
        # 16. telefone brasileiro
        "Me chama no (11) 91234-5678 depois.",
        # 17. e-mail
        "Qualquer coisa, fala com suporte@exemplo.com.br",
        # 18. pontuação incomum
        "Olha só---> AGORA!!!",
        # 19. link sem https
        "acesse: www.minha-loja.com/promocao",
        # 20. emoji repetido
        "Parabéns!!! 🎉🎉🎉",
        # 21. misto pt-en + cifrão
        "Partiu W-I-N $$$ agora msm",
        # 22. texto vazio só com espaços (edge case)
        "     ",
        # 23. zeros à esquerda na hashtag
        "#0001 pronto e testado",
        # 24. siglas + acentos ausentes
        "Qdo chega o relatório da semana?",
        # 25. varios \n para testar quebras
        "Linha1\nLinha2\n\nLinha4",
        # 26. zero-width space escondido
        "\u200bTem um char invisível aqui.",
        # 27. emoji de foguete no meio
        "Entrega foi rá🚀pida demais!",
        # 28. tag de spoiler informal
        "/spoiler o vilão era o mordomo",
        # 29. “...” + abreviação
        "blz… então até +",
        # 30. frase curta com CAPS + números
        "OK 100% CONFIRMADO",
    ]
    for text in test_chat_messages:
        processed_text = pre_processor.process_text(text)
        print(f"{text} -> {processed_text}")
