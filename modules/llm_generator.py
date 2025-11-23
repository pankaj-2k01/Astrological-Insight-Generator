from typing import Dict, List


class LLMGenerator:
    """
    Pseudo-LLM wrapper that:
      - builds prompts from user + zodiac context
      - has an embedding stub for future LangChain/vector-store extensions
      - generates a natural-language insight (stubbed)
      - supports a dummy Hindi translation path
    """

    def build_prompt(
        self,
        name: str,
        zodiac_info: Dict[str, str],
        daily_context: Dict[str, object]
    ) -> str:
        traits = daily_context.get("traits", [])
        theme = daily_context.get("today_theme", "general balance and reflection")

        traits_str = ", ".join(traits)
        sign = zodiac_info.get("sign", "Unknown")
        element = zodiac_info.get("element", "Unknown element")
        planet = zodiac_info.get("ruling_planet", "Unknown planet")

        return (
            "You are an expert astrologer generating a daily guidance.\n\n"
            f"User name: {name}\n"
            f"Zodiac sign: {sign}\n"
            f"Element: {element}\n"
            f"Ruling planet: {planet}\n"
            f"Core traits: {traits_str}\n"
            f"Today's theme: {theme}\n\n"
            "Write a short, friendly, realistic daily insight in SECOND person (use 'you'). "
            "Keep it 1–2 sentences, positive but not overly dramatic."
        )

    def get_embedding_stub(self, text: str) -> List[float]:
        """
        Placeholder for embedding generation (HuggingFace/OpenAI/etc).

        Currently returns a deterministic fake vector so that the pipeline
        is structurally correct and easy to swap out later.
        """
        base = len(text) % 7
        return [float((base + i) % 5) for i in range(8)]

    def run_pseudo_llm(self, prompt: str) -> str:
        """
        Stub that simulates LLM generation.

        In a real implementation, this method would call:
          - OpenAI chat completion
          - HuggingFace text-generation
          - LangChain chain, etc.
        """
        # We ignore the prompt in this stub, but keep it in the signature
        # so swapping to a real LLM later is easy.
        return (
            "Today, your natural strengths will help you navigate unexpected changes "
            "with calm and clarity. Trust your instincts, be honest in your conversations, "
            "and avoid wasting energy on things you cannot control."
        )

    def translate_stub(self, text: str, language: str) -> str:
        """
        Dummy translation stub.

        For 'hi', we just wrap the English text. In production this could
        call IndicTrans2, NLLB, or any translation API.
        """
        if language == "hi":
            return "यह एक सामान्य मार्गदर्शन है: " + text
        return text

    def generate_insight(
        self,
        name: str,
        zodiac_info: Dict[str, str],
        daily_context: Dict[str, object],
        language: str = "en",
    ) -> str:
        """
        High-level method to generate the final natural-language insight:

        1. Build prompt from user + zodiac + rules.
        2. Generate an embedding stub (not used further yet).
        3. Run the pseudo LLM.
        4. Translate stub if needed.
        """
        prompt = self.build_prompt(name, zodiac_info, daily_context)
        _embedding = self.get_embedding_stub(prompt)  # placeholder hook

        base_insight = self.run_pseudo_llm(prompt)
        final_text = self.translate_stub(base_insight, language)

        return final_text
