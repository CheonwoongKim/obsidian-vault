from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

# 상태 정의
class AgentState(TypedDict):
    messages: list[str]

# 간단한 노드 함수들
def research_node(state: AgentState) -> AgentState:
    """리서치 에이전트"""
    messages = state["messages"]
    messages.append("Research completed: 데이터 수집 완료")
    return {"messages": messages}

def analyze_node(state: AgentState) -> AgentState:
    """분석 에이전트"""
    messages = state["messages"]
    messages.append("Analysis completed: 데이터 분석 완료")
    return {"messages": messages}

def summarize_node(state: AgentState) -> AgentState:
    """요약 에이전트"""
    messages = state["messages"]
    messages.append("Summary completed: 최종 보고서 작성 완료")
    return {"messages": messages}

# 그래프 빌드
def create_graph():
    workflow = StateGraph(AgentState)

    # 노드 추가
    workflow.add_node("research", research_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("summarize", summarize_node)

    # 엣지 연결 (Sequential 패턴)
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "analyze")
    workflow.add_edge("analyze", "summarize")
    workflow.add_edge("summarize", END)

    return workflow.compile()

# 그래프 생성
graph = create_graph()

if __name__ == "__main__":
    # 테스트 실행
    initial_state = {"messages": ["Starting workflow..."]}
    result = graph.invoke(initial_state)

    print("Workflow completed!")
    for msg in result["messages"]:
        print(f"- {msg}")