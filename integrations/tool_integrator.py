from abc import ABC, abstractmethod
from typing import Callable, Any
import json
import re

class Tool(ABC):
    """ Parent class for all tools. Key-name must be of format: DERIVED-CLASS.method-name """
    def __init__(self):
        self.__exported_tool_descriptions: dict[str, str | None] = {}
        self._set_exported_tool_docs()

    @abstractmethod
    def _set_exported_tool_docs(self) -> None:
        """ Must set the self.__exported_tool_descriptions with the relevant tool usage(s)."""
        raise NotImplementedError("Tool._set_exported_tool_docs has not been implemented.")

    def get_exported_tool_docs(self) -> dict[str, str | None]:
        return self.__exported_tool_descriptions

class ToolIntegrator:
    """ This class is responsible for injecting tool docs & evaluating tool calls. """
    def __init__(self, tools: list[Tool], suppress_warning: bool=False):
        self.__consolidated_docs = {}
        self.__consolidated_docs_str = ""
        self.__tool_map: dict[str, Callable] = {}

        skipped_items: int = 0

        for tool in tools:
            for k, v in tool.get_exported_tool_docs().items():
                if v:
                    self.__consolidated_docs[k] = v
                    self.__consolidated_docs_str += f"{v}\n"

                    # Dynamically bind the actual method
                    cls_name, method_name = k.split(".")
                    if cls_name == tool.__class__.__name__:
                        self.__tool_map[k] = getattr(tool, method_name)

                else:
                    skipped_items += 1
        
        if skipped_items >= 1 and not suppress_warning:
            raise RuntimeWarning(f"{skipped_items} items were skipped because they had no doc string.")
        
        self.__tool_available_prompt = f"""
        When appropriate, respond with one or more tool calls in this format:
        TOOL_CALLS:
        [
        {{
            "tool": "<tool_name>",
            "args": {{
            "param1": "...",
            "param2": "..."
            }}
        }},
        ...
        ]
        Only use tools listed below. Do not invent new tools.
        Available tools:
        { self.__consolidated_docs_str }
        """
    
    def get_tool_prompt(self) -> str:
        return self.__tool_available_prompt
        
    def extract_tool_calls(self, output: str) -> list[dict] | None:
        hit = re.search(r'TOOL_CALLS:\s*(\[.*?\])', output, re.DOTALL)

        if not hit:
            return None
        try:
            return json.loads(hit.group(1))
        except json.JSONDecodeError:
            return None
        
    def call_tool(self, tool_name: str, args: dict) -> Any:
        func = self.__tool_map.get(tool_name)

        if not func:
            raise ValueError(f"Tool not found: { tool_name }")
        
        return func(**args)
    
