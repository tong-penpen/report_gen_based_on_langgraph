from langchain_core.messages import HumanMessage
from typing import Annotated
from langchain_experimental.tools import PythonREPLTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Literal
import functools
import operator
from typing import Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import create_react_agent

python_repl_tool = PythonREPLTool()

def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }

members = ["chart_generator", "trend_analysis","reason_analysis","suggestion_generator","Synthesis"]
system_prompt = (
    "你是一个主管，负责管理以下工作者之间的对话：{members}。给定以下用户请求，"
    " 回答下一个要执行的任务的工作者。每个工作者将执行一项任务并用其结果和状态进行响应。完成后，"
    " 回答 FINISH。"
)
# 我们的团队主管是一个 LLM 节点。它只是选择下一个要处理的智能体，
# 并在工作完成时做出决定
options = ["FINISH"] + members

class routeResponse(BaseModel):
    next: Literal[*options]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "给定上面的对话，谁应该接下来行动？"
            " 或者我们应该 FINISH？ 选择以下一项：{options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

llm = ChatOpenAI(model="gpt-4o")

def supervisor_agent(state):
    supervisor_chain = prompt | llm.with_structured_output(routeResponse)
    return supervisor_chain.invoke(state)

# 智能体状态是图中每个节点的输入
class AgentState(TypedDict):
    # 注释告诉图，新消息将始终
    # 添加到当前状态的消息
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # 'next' 字段指示下一个路由位置
    next: str

# 注意：这执行任意代码执行。请谨慎操作
chart_prompt = "你是一个绘图者，按要求编写python代码并使用工具执行画图。"
chart_agent = create_react_agent(llm,state_modifier = chart_prompt, tools=[python_repl_tool])
chart_node = functools.partial(agent_node, agent=chart_agent, name="chart_generator")

# 趋势分析
trend_prompt = ""
trend_agent = create_react_agent(llm, state_modifier = trend_prompt,tools=[python_repl_tool])
trend_node = functools.partial(agent_node, agent=trend_agent, name="trend_analysis")

# 原因分析
reson_prompt = ""
reason_agent = create_react_agent(llm,state_modifier = reason_prompt, tools=[python_repl_tool])
reason_node = functools.partial(agent_node, agent=reason_agent, name="reason_analysis")

# 建议
suggestion_prompt = ""
suggestion_agent = create_react_agent(llm, state_modifier = suggestion_prompt, tools=[python_repl_tool])
suggestion_node = functools.partial(agent_node, agent=suggestion_agent, name="suggestion_generator")

# 格式化
synthesis_prompt = ""
synthesis_agent = create_react_agent(llm,state_modifier = synthesis_prompt, tools=[python_repl_tool])
synthesis_node = functools.partial(agent_node, agent=synthesis_agent, name="synthesis_generator")

workflow = StateGraph(AgentState)
workflow.add_node("chart_generator", chart_node)
workflow.add_node("trend_analysis", trend_node)
workflow.add_node("reason_analysis", reason_node)
workflow.add_node("suggestion_generator", suggestion_node)
workflow.add_node("synthesis", synthesis_node)
workflow.add_node("supervisor", supervisor_agent)

for member in members:
    # 我们希望我们的工作者在完成时始终“报告给”主管
    workflow.add_edge(member, "supervisor")


# 主管填充图状态中的“next”字段
# 这将路由到一个节点或完成
conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)


# 最后，添加入口点
workflow.add_edge(START, "supervisor")
graph = workflow.compile()
