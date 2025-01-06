from langchain_core.messages import ( BaseMessage, HumanMessage, ToolMessage, ) 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder 
from langgraph.graph import END, StateGraph, START 
from typing import Annotated
from langchain_core.tools import tool


def create_agent(llm, tools, system_message: str):
    """创建代理."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "您是一位乐于助人的 AI 助手，与其他助手协作。 "
                "使用提供的工具来推进回答问题。 "
                "如果您无法完全回答，没关系，其他具有不同工具的助手 "
                "将在您结束的地方提供帮助。执行您所能执行的操作以取得进展。 "
                "如果您或任何其他助手拥有最终答案或交付结果，"
                "在您的回复前面加上 FINAL ANSWER，以便团队知道何时停止。 "
                "您可以使用以下工具：{tool_names}.\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_tools(tools)


from langchain_experimental.utilities import PythonREPL """这个库可以执行python脚本"""

"""创建工具仓tools"""
@tool
def tool_1():
    



"""定义tools_node节点"""
from langgraph.prebuilt import ToolNode 
tools = [tavily_tool, python_repl] 
tool_node = ToolNode(tools)


"""创建agents"""
import functools
from langchain_core.messages import AIMessage

# Helper function to create a node for a given agent
def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }

"""确定llm,这里还不确定本地的llm怎么封装
测试的时候可以：llm = ChatOpenAI(model="gpt-4o")"""
llm = 

#创建agents
TrendAnalysis_agent = create_agent(
    llm,
    [],#这里添加tool 
    system_message="",#这里添加agent特殊的prompt
)
TrendAnalysis = functools.partial(agent_node, agent=TrendAnalysis_agent, name="TrendAnalysis")





"""定义路由  用来跳转状态机"""
from typing import Literal
def router(state):
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        # The previous agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return END
    return "continue"


from langgraph import StateGraph, Node, Edge, ConditionalEdge

workflow = StateGraph()

# 添加节点
workflow.add_node("Charting", chart_node)
workflow.add_node("Trend Analysis", trend_node)
workflow.add_node("Cause Analysis", cause_node)
workflow.add_node("Recommendations", recommend_node)
workflow.add_node("Synthesis", synthesis_node)

# 添加条件边
workflow.add_conditional_edges(
    "Charting", router, 
    {"continue": "Trend Analysis", "call_tool": "call_tool", "end": "END"},
)
workflow.add_conditional_edges(
    "Trend Analysis", router, 
    {"continue": "Cause Analysis", "call_tool": "call_tool", "end": "END"},
)
workflow.add_conditional_edges(
    "Cause Analysis", router, 
    {"continue": "Recommendations", "call_tool": "call_tool", "end": "END"},
)
workflow.add_conditional_edges(
    "Recommendations", router, 
    {"continue": "Synthesis", "call_tool": "call_tool", "end": "END"},
)
workflow.add_conditional_edges(
    "Synthesis", router, 
    {"continue": "Charting", "call_tool": "call_tool", "end": "END"},
)

workflow.add_conditional_edges(
    "call_tool",
    # 这里的sender加的 每个agent  call的对应的tool
    lambda x: x["sender"],
    {
        
    },
)

workflow.add_edge(START, "Trend Analysis")

from IPython.display import Image, display 
try: 
    display(Image(graph.get_graph(xray=True).draw_mermaid_png())) 
except Exception: 
    # 这需要一些额外的依赖项，并且是可选的 pass
    pass
    
    
events = graph.stream(
    {
        "messages": [
            HumanMessage(
                content="  "#人类指令  
            )
        ],
    },
   
    {"recursion_limit": 150},
)
for s in events:
    print(s)
    print("----")
    