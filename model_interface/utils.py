from abc import ABC, abstractmethod
from typing import Any

# Utility interface for debugging
class UtilInterface(ABC):

    @abstractmethod
    def count_tokens(self, model: Any, prompt: str) -> int:
        """ Counts the number of tokens in the given prompt, useful for context budgeting. """
        raise NotImplementedError("count_tokens not implemented")
