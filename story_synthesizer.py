class StorySynthesizer:
    """
    Generates a structured story blueprint from a user vibe and retrieved books using an LLM.
    For now, uses a mock LLM for demonstration.
    """
    def __init__(self, llm=None):
        # llm: a callable that takes a prompt and returns a string (can be OpenAI, HuggingFace, etc.)
        self.llm = llm if llm is not None else self.mock_llm

    def synthesize(self, vibe, retrieved_books):
        """
        Returns a story blueprint (dict) given a vibe and a list of book dicts.
        """
        prompt = self._build_prompt(vibe, retrieved_books)
        story = self.llm(prompt)
        return self._parse_story(story)

    def _build_prompt(self, vibe, books):
        # Example prompt engineering
        book_summaries = "\n".join([
            f"- {b['Title']} ({b['Genre']}): {b['Description']}" for b in books
        ])
        prompt = (
            f"Given the following vibe: '{vibe}'\n"
            f"And these book inspirations:\n{book_summaries}\n"
            "Generate a unique, detailed story blueprint including: Title, Characters, Plot, Setting, and Themes."
        )
        return prompt

    def _parse_story(self, story_text):
        # For MVP, just return the raw text; can be improved to parse structured output
        return {"story_blueprint": story_text}

    def mock_llm(self, prompt):
        # Simple mock LLM that returns a formatted string
        return (
            "Title: The Vibe Adventure\n"
            "Characters: The Dreamer, The Guide, The Shadow\n"
            "Plot: Inspired by your vibe and the selected books, a journey unfolds where the protagonist faces challenges, discovers secrets, and grows.\n"
            "Setting: A world blending the elements of the retrieved books.\n"
            "Themes: Discovery, Growth, Adventure\n"
        ) 