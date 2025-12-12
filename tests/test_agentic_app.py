import pytest
from agentic_app.tools import ToolRegistry, Tool, ToolType, ToolParameter
from agentic_app.agent import Agent, ExecutionPlan
from agentic_app.app import AgenticApp, create_app


class TestToolRegistry:
    def test_default_tools_registration(self):
        registry = ToolRegistry()
        tools = registry.list_all()
        assert len(tools) > 0
        
        assert registry.get("add") is not None
        assert registry.get("subtract") is not None
        assert registry.get("multiply") is not None

    def test_register_custom_tool(self):
        registry = ToolRegistry()
        custom_tool = Tool(
            name="square",
            description="Square a number",
            func=lambda x: x ** 2,
            parameters=[ToolParameter("x", "float")],
            tool_type=ToolType.ARITHMETIC,
        )
        registry.register(custom_tool)
        assert registry.get("square") is not None

    def test_register_duplicate_tool_raises_error(self):
        registry = ToolRegistry()
        custom_tool = Tool(
            name="add",
            description="Duplicate",
            func=lambda a, b: a + b,
            parameters=[
                ToolParameter("a", "float"),
                ToolParameter("b", "float"),
            ],
            tool_type=ToolType.ARITHMETIC,
        )
        with pytest.raises(ValueError, match="already exists"):
            registry.register(custom_tool)

    def test_list_tools_by_type(self):
        registry = ToolRegistry()
        arithmetic_tools = registry.list_by_type(ToolType.ARITHMETIC)
        assert len(arithmetic_tools) > 0
        assert all(t.tool_type == ToolType.ARITHMETIC for t in arithmetic_tools)

    def test_tool_invocation(self):
        registry = ToolRegistry()
        tool = registry.get("add")
        result = tool.invoke(a=2, b=3)
        assert result == 5

    def test_tool_invocation_with_invalid_params(self):
        registry = ToolRegistry()
        tool = registry.get("add")
        with pytest.raises(ValueError):
            tool.invoke(a=2)

    def test_division_by_zero(self):
        registry = ToolRegistry()
        tool = registry.get("divide")
        with pytest.raises(ValueError, match="Division by zero"):
            tool.invoke(a=10, b=0)

    def test_safe_conversions(self):
        registry = ToolRegistry()
        
        to_float_tool = registry.get("to_float")
        result = to_float_tool.invoke(value="3.14")
        assert result == 3.14
        
        with pytest.raises(ValueError):
            to_float_tool.invoke(value="not_a_number")


class TestAgent:
    def test_agent_creation(self):
        agent = Agent()
        assert agent.tool_registry is not None
        assert len(agent.execution_history) == 0

    def test_simple_addition(self):
        agent = Agent()
        result = agent.execute("Add 1 and 1")
        assert result == 2

    def test_chained_operations(self):
        agent = Agent()
        result = agent.execute(
            "Add 1 and 1, then multiply with 10, then subtract 0.5 from it"
        )
        assert result == 19.5

    def test_execution_history(self):
        agent = Agent()
        agent.execute("Add 5 and 3")
        assert len(agent.execution_history) == 1
        assert agent.execution_history[0].tool_name == "add"
        assert agent.execution_history[0].result == 8

    def test_plan_generation(self):
        agent = Agent()
        plan = agent.plan("Add 2 and 3, then multiply with 4")
        assert len(plan.steps) == 2
        assert plan.steps[0][0] == "add"
        assert plan.steps[1][0] == "multiply"

    def test_multiplication_operation(self):
        agent = Agent()
        result = agent.execute("Multiply 5 and 3")
        assert result == 15

    def test_division_operation(self):
        agent = Agent()
        result = agent.execute("Divide 10 by 2")
        assert result == 5.0

    def test_power_operation(self):
        agent = Agent()
        result = agent.execute("2 to the power of 3")
        assert result == 8

    def test_subtraction_with_context(self):
        agent = Agent()
        result = agent.execute("Add 10 and 5, then subtract 3 from it")
        assert result == 12

    def test_verbose_execution(self):
        agent = Agent(verbose=True)
        result = agent.execute("Add 1 and 1")
        assert result == 2

    def test_error_handling_invalid_query(self):
        agent = Agent()
        result = agent.execute("This is not a valid mathematical query")
        assert result is None

    def test_multiple_operations_complex(self):
        agent = Agent()
        result = agent.execute(
            "Add 2 and 3, then multiply by 4, then subtract 5"
        )
        assert result == 15

    def test_parameter_resolution(self):
        agent = Agent()
        agent.execute("Add 10 and 5")
        assert "last_result" in agent.current_context


class TestAgenticApp:
    def test_app_creation(self):
        app = create_app()
        assert isinstance(app, AgenticApp)

    def test_query_execution(self):
        app = create_app()
        result = app.query("Add 2 and 3")
        assert result == 5

    def test_query_with_empty_string(self):
        app = create_app()
        with pytest.raises(ValueError):
            app.query("")

    def test_list_tools(self):
        app = create_app()
        tools = app.list_tools()
        assert len(tools) > 0
        assert all(hasattr(t, 'name') for t in tools)

    def test_get_tool_info(self):
        app = create_app()
        info = app.get_tool_info("add")
        assert info is not None
        assert info["name"] == "add"
        assert "parameters" in info

    def test_get_tool_info_nonexistent(self):
        app = create_app()
        info = app.get_tool_info("nonexistent")
        assert info is None

    def test_register_custom_tool(self):
        app = create_app()
        custom_tool = Tool(
            name="double",
            description="Double a number",
            func=lambda x: x * 2,
            parameters=[ToolParameter("x", "float")],
            tool_type=ToolType.ARITHMETIC,
        )
        app.register_tool(custom_tool)
        assert app.get_tool_info("double") is not None

    def test_complex_query(self):
        app = create_app()
        result = app.query(
            "Add 1 and 1, then multiply with 10, then subtract 0.5 from it"
        )
        assert result == 19.5

    def test_execution_summary(self):
        app = create_app()
        app.query("Add 5 and 3")
        summary = app.get_execution_summary()
        assert "add" in summary.lower()
        assert "8" in summary


class TestEdgeCases:
    def test_very_large_numbers(self):
        app = create_app()
        result = app.query("Add 999999999 and 1")
        assert result == 1000000000

    def test_floating_point_precision(self):
        app = create_app()
        result = app.query("Multiply 0.1 and 0.2")
        assert abs(result - 0.02) < 1e-10

    def test_negative_numbers(self):
        app = create_app()
        result = app.query("Add -5 and 3")
        assert result == -2

    def test_zero_operations(self):
        app = create_app()
        result = app.query("Multiply 0 and 100")
        assert result == 0

    def test_chained_multiplications(self):
        app = create_app()
        result = app.query("Multiply 2 and 3, then multiply by 4")
        assert result == 24

    def test_power_zero(self):
        agent = Agent()
        result = agent.execute("5 to the power of 0")
        assert result == 1


class TestStringOperations:
    def test_string_concatenation(self):
        app = create_app()
        tool = app.tool_registry.get("concatenate")
        result = tool.invoke(s1="hello", s2="world")
        assert result == "helloworld"

    def test_string_length(self):
        app = create_app()
        tool = app.tool_registry.get("length")
        result = tool.invoke(text="hello")
        assert result == 5

    def test_uppercase(self):
        app = create_app()
        tool = app.tool_registry.get("uppercase")
        result = tool.invoke(text="hello")
        assert result == "HELLO"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
