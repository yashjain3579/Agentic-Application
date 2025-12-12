from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import re

from .tools import Tool, ToolRegistry, ToolType

logger = logging.getLogger(__name__)


@dataclass
class ExecutionStep:
    step_id: int
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self) -> str:
        status = "OK" if self.result is not None else "ERROR" if self.error else "PENDING"
        return f"Step {self.step_id}: {self.tool_name} [{status}]"


@dataclass
class ExecutionPlan:
    steps: List[Tuple[str, Dict[str, Any]]]
    original_query: str
    reasoning: str

    def __repr__(self) -> str:
        steps_str = "\n".join([f"  {i+1}. {tool}({params})" 
                               for i, (tool, params) in enumerate(self.steps)])
        return f"Plan: {self.original_query}\nSteps:\n{steps_str}"


class Agent:
    def __init__(self, tool_registry: Optional[ToolRegistry] = None, verbose: bool = False):
        self.tool_registry = tool_registry or ToolRegistry()
        self.verbose = verbose
        self.execution_history: List[ExecutionStep] = []
        self.current_context: Dict[str, Any] = {}
        self.max_iterations = 100
        self.max_retries = 3

        if verbose:
            logging.basicConfig(level=logging.DEBUG)
            logger.setLevel(logging.DEBUG)

    def plan(self, query: str) -> ExecutionPlan:
        logger.debug(f"Planning: {query}")
        steps = self._parse_query(query)
        reasoning = self._generate_reasoning(query, steps)
        plan = ExecutionPlan(steps=steps, original_query=query, reasoning=reasoning)
        logger.debug(f"Plan created with {len(steps)} steps")
        return plan

    def execute(self, query: str, max_iterations: Optional[int] = None) -> Any:
        if max_iterations:
            self.max_iterations = max_iterations
        
        self.execution_history = []
        self.current_context = {}
        
        logger.info(f"Executing: {query}")
        plan = self.plan(query)
        
        if self.verbose:
            print(f"\n{plan}\n")
        
        result = None
        for step_id, (tool_name, params) in enumerate(plan.steps, 1):
            try:
                result = self._run_step(step_id, tool_name, params)
                self.current_context['last_result'] = result
            except Exception as e:
                logger.error(f"Step {step_id} failed: {e}")
                raise RuntimeError(f"Step {step_id} failed: {e}")
        
        logger.info(f"Execution complete. Result: {result}")
        return result

    def _run_step(self, step_id: int, tool_name: str, params: Dict[str, Any], retry: int = 0) -> Any:
        tool = self.tool_registry.get(tool_name)
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")
        
        resolved = self._resolve_parameters(params)
        
        try:
            logger.debug(f"Step {step_id}: {tool_name} {resolved}")
            result = tool.invoke(**resolved)
            
            step = ExecutionStep(step_id, tool_name, resolved, result=result)
            self.execution_history.append(step)
            
            if self.verbose:
                print(f"  Step {step_id}: {tool_name} = {result}")
            
            return result
            
        except Exception as e:
            logger.warning(f"Step {step_id} error (attempt {retry + 1}): {e}")
            
            if retry < self.max_retries:
                return self._run_step(step_id, tool_name, params, retry + 1)
            
            step = ExecutionStep(step_id, tool_name, resolved, error=str(e))
            self.execution_history.append(step)
            raise

    def _parse_query(self, query: str) -> List[Tuple[str, Dict[str, Any]]]:
        steps = []
        context = None
        
        if not re.search(r'\bthen\b', query, re.IGNORECASE):
            tool, params = self._extract_tool(query, context)
            if tool:
                steps.append((tool, params))
            return steps
        
        phrases = re.split(r'\bthen\b', query, flags=re.IGNORECASE)
        for phrase in phrases:
            phrase = phrase.strip()
            if not phrase:
                continue
            tool, params = self._extract_tool(phrase, context)
            if tool:
                steps.append((tool, params))
                context = f"{{step_{len(steps)}}}"
        
        return steps

    def _extract_tool(self, phrase: str, context: Optional[str] = None) -> Tuple[Optional[str], Dict[str, Any]]:
        phrase_lower = phrase.lower().strip()
        
        patterns = [
            (r'add\s+([\d\.\-\{_\}]+)\s+(?:and|to)?\s+([\d\.\-\{_\}]+)', 'add'),
            (r'add\s+([\d\.\-\{_\}]+)(?:\s|$)', lambda m: ('add', (context or "0", m.group(1)))),
            (r'subtract\s+([\d\.\-\{_\}]+)\s+from\s+([\d\.\-\{_\}]+)', lambda m: ('subtract', (m.group(2), m.group(1)))),
            (r'subtract\s+([\d\.\-\{_\}]+)', lambda m: ('subtract', (context or "0", m.group(1)))),
            (r'multiply\s+([\d\.\-\{_\}]+)\s+(?:and|with|by)\s+([\d\.\-\{_\}]+)', 'multiply'),
            (r'multiply\s+(?:by|with|and)?\s*([\d\.\-\{_\}]+)', lambda m: ('multiply', (context or "1", m.group(1)))),
            (r'divide\s+([\d\.\-\{_\}]+)\s+by\s+([\d\.\-\{_\}]+)', 'divide'),
            (r'divide\s+(?:by)?\s*([\d\.\-\{_\}]+)', lambda m: ('divide', (context or "1", m.group(1)))),
            (r'([\d\.\-\{_\}]+)\s+to\s+(?:the\s+)?power\s+of\s+([\d\.\-\{_\}]+)', lambda m: ('power', (m.group(1), m.group(2)))),
            (r'raise\s+([\d\.\-\{_\}]+)\s+to\s+(?:(?:the\s+)?power\s+of\s+)?([\d\.\-\{_\}]+)', 'power'),
            (r'(?:to\s+the\s+)?power\s+(?:of\s+)?([\d\.\-\{_\}]+)', lambda m: ('power', (context or "2", m.group(1)))),
            (r'uppercase\s+(.+)', lambda m: ('uppercase', (m.group(1),))),
            (r'lowercase\s+(.+)', lambda m: ('lowercase', (m.group(1),))),
            (r'length\s+of\s+(.+)', lambda m: ('length', (m.group(1),))),
            (r'concatenate\s+(.+)\s+and\s+(.+)', lambda m: ('concatenate', (m.group(1), m.group(2)))),
            (r'replace\s+(.+)\s+with\s+(.+)', lambda m: ('replace', (context or m.group(1), m.group(2)))),
            (r'square\s+([\d\.\-\{_\}]+)', lambda m: ('square', (m.group(1),))),
            (r'square\s+root\s+of\s+([\d\.\-\{_\}]+)', lambda m: ('square_root', (m.group(1),))),
        ]
        
        for pattern, tool_info in patterns:
            match = re.search(pattern, phrase_lower)
            if match:
                if callable(tool_info):
                    tool_name, param_tuple = tool_info(match)
                else:
                    tool_name = tool_info
                    param_tuple = tuple(match.groups())
                
                params = self._build_parameters(tool_name, param_tuple)
                if params:
                    return tool_name, params
        
        return None, {}

    def _build_parameters(self, tool_name: str, values: Tuple) -> Dict[str, Any]:
        tool = self.tool_registry.get(tool_name)
        if not tool:
            return {}
        
        params = {}
        param_names = [p.name for p in tool.parameters]
        
        for name, value in zip(param_names, values):
            params[name] = self._parse_value(value)
        
        return params

    def _parse_value(self, value: str) -> Any:
        if value.startswith("{") and value.endswith("}"):
            return value
        
        try:
            if '.' in str(value):
                return float(value)
            return int(value)
        except ValueError:
            return value

    def _resolve_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        resolved = {}
        
        for key, value in params.items():
            if isinstance(value, str) and value.startswith("{step_"):
                match = re.match(r'\{step_(\d+)\}', value)
                if match:
                    step_num = int(match.group(1)) - 1
                    if 0 <= step_num < len(self.execution_history):
                        resolved[key] = self.execution_history[step_num].result
                    else:
                        raise ValueError(f"Step not found: {value}")
                else:
                    resolved[key] = value
            else:
                resolved[key] = value
        
        return resolved

    def _generate_reasoning(self, query: str, steps: List[Tuple[str, Dict[str, Any]]]) -> str:
        if not steps:
            return "No steps found"
        
        descriptions = []
        for i, (tool, params) in enumerate(steps, 1):
            param_str = ", ".join([f"{k}={v}" for k, v in params.items()])
            descriptions.append(f"Step {i}: {tool}({param_str})")
        
        return "Plan: " + " -> ".join([d.split(":")[1].strip() for d in descriptions])

    def get_execution_summary(self) -> str:
        if not self.execution_history:
            return "No history"
        
        lines = ["Execution:"]
        for step in self.execution_history:
            if step.error:
                lines.append(f"  {step.tool_name}: ERROR - {step.error}")
            else:
                lines.append(f"  {step.tool_name}: {step.result}")
        
        return "\n".join(lines)
