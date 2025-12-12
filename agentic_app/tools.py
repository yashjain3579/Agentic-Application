from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ToolType(Enum):
    ARITHMETIC = "arithmetic"
    STRING = "string"
    LOGIC = "logic"
    CONVERSION = "conversion"

@dataclass
class ToolParameter:
    name: str
    param_type: str
    required: bool = True
    description: str = ""
    default: Optional[Any] = None

    def validate(self, value: Any) -> bool:
        if value is None:
            return not self.required
        
        type_map = {
            'int': int,
            'float': (int, float),
            'str': str,
            'bool': bool,
            'list': list,
        }
        expected_type = type_map.get(self.param_type)
        if expected_type is None:
            return True
        
        return isinstance(value, expected_type)


@dataclass
class Tool:
    name: str
    description: str
    func: Callable
    parameters: List[ToolParameter]
    tool_type: ToolType
    category: str = ""

    def invoke(self, **kwargs) -> Any:
        for param in self.parameters:
            if param.required and param.name not in kwargs:
                raise ValueError(f"Missing required parameter: {param.name}")
            
            if param.name in kwargs:
                value = kwargs[param.name]
                if not param.validate(value):
                    raise ValueError(f"Invalid type for {param.name}")
        
        return self.func(**kwargs)

    def __repr__(self) -> str:
        param_str = ", ".join([p.name for p in self.parameters])
        return f"Tool({self.name}({param_str}))"


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._register_defaults()

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already exists")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_all(self) -> List[Tool]:
        return list(self._tools.values())

    def list_by_type(self, tool_type: ToolType) -> List[Tool]:
        return [t for t in self._tools.values() if t.tool_type == tool_type]

    def _register_defaults(self) -> None:
        self.register(Tool(
            name="add",
            description="Add two numbers",
            func=lambda a, b: a + b,
            parameters=[
                ToolParameter("a", "float"),
                ToolParameter("b", "float"),
            ],
            tool_type=ToolType.ARITHMETIC,
        ))

        self.register(Tool(
            name="subtract",
            description="Subtract numbers",
            func=lambda a, b: a - b,
            parameters=[
                ToolParameter("a", "float"),
                ToolParameter("b", "float"),
            ],
            tool_type=ToolType.ARITHMETIC,
        ))

        self.register(Tool(
            name="multiply",
            description="Multiply numbers",
            func=lambda a, b: a * b,
            parameters=[
                ToolParameter("a", "float"),
                ToolParameter("b", "float"),
            ],
            tool_type=ToolType.ARITHMETIC,
        ))

        self.register(Tool(
            name="divide",
            description="Divide numbers",
            func=self._safe_divide,
            parameters=[
                ToolParameter("a", "float"),
                ToolParameter("b", "float"),
            ],
            tool_type=ToolType.ARITHMETIC,
        ))

        self.register(Tool(
            name="power",
            description="Raise to power",
            func=lambda base, exponent: base ** exponent,
            parameters=[
                ToolParameter("base", "float"),
                ToolParameter("exponent", "float"),
            ],
            tool_type=ToolType.ARITHMETIC,
        ))

        self.register(Tool(
            name="modulo",
            description="Get remainder",
            func=lambda a, b: a % b,
            parameters=[
                ToolParameter("a", "float"),
                ToolParameter("b", "float"),
            ],
            tool_type=ToolType.ARITHMETIC,
        ))

        self.register(Tool(
            name="absolute",
            description="Get absolute value",
            func=lambda value: abs(value),
            parameters=[ToolParameter("value", "float")],
            tool_type=ToolType.ARITHMETIC,
        ))

        self.register(Tool(
            name="concatenate",
            description="Join strings",
            func=lambda s1, s2: str(s1) + str(s2),
            parameters=[
                ToolParameter("s1", "str"),
                ToolParameter("s2", "str"),
            ],
            tool_type=ToolType.STRING,
        ))

        self.register(Tool(
            name="uppercase",
            description="Convert to uppercase",
            func=lambda text: str(text).upper(),
            parameters=[ToolParameter("text", "str")],
            tool_type=ToolType.STRING,
        ))

        self.register(Tool(
            name="lowercase",
            description="Convert to lowercase",
            func=lambda text: str(text).lower(),
            parameters=[ToolParameter("text", "str")],
            tool_type=ToolType.STRING,
        ))

        self.register(Tool(
            name="reverse",
            description="Reverse a string",
            func=lambda text: str(text)[::-1],
            parameters=[ToolParameter("text", "str")],
            tool_type=ToolType.STRING,
        ))

        self.register(Tool(
            name="length",
            description="Get string length",
            func=lambda text: len(str(text)),
            parameters=[ToolParameter("text", "str")],
            tool_type=ToolType.STRING,
        ))

        self.register(Tool(
            name="equals",
            description="Check if equal",
            func=lambda a, b: a == b,
            parameters=[
                ToolParameter("a", "str"),
                ToolParameter("b", "str"),
            ],
            tool_type=ToolType.LOGIC,
        ))

        self.register(Tool(
            name="greater_than",
            description="Check if greater",
            func=lambda a, b: a > b,
            parameters=[
                ToolParameter("a", "float"),
                ToolParameter("b", "float"),
            ],
            tool_type=ToolType.LOGIC,
        ))

        self.register(Tool(
            name="less_than",
            description="Check if less",
            func=lambda a, b: a < b,
            parameters=[
                ToolParameter("a", "float"),
                ToolParameter("b", "float"),
            ],
            tool_type=ToolType.LOGIC,
        ))

        self.register(Tool(
            name="to_int",
            description="Convert to integer",
            func=self._safe_to_int,
            parameters=[ToolParameter("value", "str")],
            tool_type=ToolType.CONVERSION,
        ))

        self.register(Tool(
            name="to_float",
            description="Convert to float",
            func=self._safe_to_float,
            parameters=[ToolParameter("value", "str")],
            tool_type=ToolType.CONVERSION,
        ))

        self.register(Tool(
            name="to_string",
            description="Convert to string",
            func=lambda value: str(value),
            parameters=[ToolParameter("value", "str")],
            tool_type=ToolType.CONVERSION,
        ))

    @staticmethod
    def _safe_divide(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

    @staticmethod
    def _safe_to_int(value: str) -> int:
        try:
            return int(float(value))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert to int: {e}")

    @staticmethod
    def _safe_to_float(value: str) -> float:
        try:
            return float(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert to float: {e}")
