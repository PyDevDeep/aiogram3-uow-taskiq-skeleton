from abc import ABC, abstractmethod


class IAIConnector(ABC):
    """Abstract interface for AI interaction. Implementation details are encapsulated."""

    @abstractmethod
    async def get_response(self, text: str) -> str | None:
        pass


class OpenAIConnector(IAIConnector):
    """ "Concrete AI connector implementation. Isolated request logic."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        # Initialize the client here, e.g.: self.client = AsyncOpenAI(api_key=self.api_key)

    async def get_response(self, text: str) -> str | None:
        """
        Placeholder method. Implement your LLM call logic (OpenAI/Gemini) here.
        """
        pass
