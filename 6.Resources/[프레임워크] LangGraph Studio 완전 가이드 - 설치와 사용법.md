---
title: "LangGraph Studio 완전 가이드 - 설치와 사용법"
type: resource
category: 개발도구/AI프레임워크
tags: [도구/LangGraph, 기술/멀티에이전트, 방법론/개발환경]
status: active
date: 2025-09-24
updated: 2025-09-24
source: ["실제 설치 및 테스트 경험", "LangGraph 공식 문서"]
---

## 1. LangGraph Studio 개요

**LangGraph Studio**는 LangChain에서 제공하는 시각적 멀티 에이전트 워크플로우 개발 및 디버깅 도구입니다. 드래그&드롭으로 에이전트 그래프를 설계하고, 실시간으로 실행 상태를 모니터링할 수 있습니다.

### 1.1. 핵심 기능

- **시각적 워크플로우 디자인**: 노드와 엣지로 에이전트 관계 정의
- **실시간 디버깅**: 각 노드별 실행 상태와 데이터 흐름 추적
- **인터랙티브 테스팅**: 웹 UI에서 직접 그래프 실행 및 결과 확인
- **Hot Reloading**: 코드 변경 시 자동 반영

---

## 2. 설치 가이드

### 2.1. 시스템 요구사항

```bash
# Python 3.11+ 필요
python --version
```

### 2.2. macOS 외부 관리 환경 문제 해결

macOS에서는 시스템 Python이 외부 관리되므로 가상 환경 사용이 필수입니다.

```bash
# 가상 환경 생성
python3 -m venv langgraph_env

# 가상 환경 활성화
source langgraph_env/bin/activate

# LangGraph CLI 및 필요 패키지 설치
pip install -U "langgraph-cli[inmem]"
```

**설치 확인:**
```bash
langgraph --version
```

---

## 3. 프로젝트 설정

### 3.1. 기본 프로젝트 구조

```bash
my-agent-project/
├── langgraph.json          # 프로젝트 설정
├── .env                    # 환경 변수
├── simple_agent.py         # 에이전트 정의
└── langgraph_env/          # 가상 환경
```

### 3.2. 설정 파일 생성

**langgraph.json:**
```json
{
  "dependencies": ["."],
  "graphs": {
    "simple_agent": "./simple_agent.py:graph"
  },
  "env": ".env"
}
```

**.env:**
```env
# 선택사항 - LangChain 추적을 위한 API 키
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_api_key_here
```

---

## 4. 간단한 에이전트 예제

### 4.1. Sequential 패턴 에이전트 구현

**simple_agent.py:**
```python
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

# 상태 정의
class AgentState(TypedDict):
    messages: list[str]

# 노드 함수들
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

# 그래프 구축
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
```

---

## 5. LangGraph Studio 실행

### 5.1. 개발 서버 시작

```bash
# 프로젝트 디렉토리에서 실행
cd my-agent-project
source langgraph_env/bin/activate

# Studio 실행 (브라우저 자동 실행 안 함)
langgraph dev --port 8123 --no-browser
```

**성공 메시지:**
```
Welcome to
╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

- 🚀 API: http://127.0.0.1:8123
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
- 📚 API Docs: http://127.0.0.1:8123/docs
```

### 5.2. 접속 방법

1. **Studio UI (추천)**: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
2. **API 문서**: http://127.0.0.1:8123/docs
3. **직접 API**: http://127.0.0.1:8123

---

## 6. API 사용법

### 6.1. 기본 워크플로우

1. **Assistant 생성**
2. **Thread 생성**
3. **Run 실행**
4. **결과 확인**

### 6.2. 실제 API 호출 예제

**1단계: Assistant 생성**
```bash
curl -X POST http://127.0.0.1:8123/assistants \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "simple_agent",
    "config": {"configurable": {}},
    "name": "My Simple Agent"
  }'
```

**응답 예시:**
```json
{
  "assistant_id": "6ddced78-669d-411a-8951-be85967f1f12",
  "graph_id": "simple_agent",
  "name": "My Simple Agent",
  "created_at": "2025-09-24T06:18:59.995504+00:00"
}
```

**2단계: Thread 생성**
```bash
curl -X POST http://127.0.0.1:8123/threads \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Thread"}'
```

**응답 예시:**
```json
{
  "thread_id": "1d5025e2-6092-4fee-acf7-9bcbec3411da",
  "created_at": "2025-09-24T06:19:06.779779+00:00",
  "status": "idle"
}
```

**3단계: Run 실행**
```bash
curl -X POST http://127.0.0.1:8123/threads/[THREAD_ID]/runs/wait \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "[ASSISTANT_ID]",
    "input": {"messages": ["Starting workflow..."]}
  }'
```

**실행 결과:**
```json
{
  "messages": [
    "Starting workflow...",
    "Research completed: 데이터 수집 완료",
    "Analysis completed: 데이터 분석 완료",
    "Summary completed: 최종 보고서 작성 완료"
  ]
}
```

---

## 7. 주요 API 엔드포인트

### 7.1. Assistant 관리
- `POST /assistants`: Assistant 생성
- `GET /assistants/{assistant_id}`: Assistant 조회
- `GET /assistants/{assistant_id}/graph`: 그래프 구조 확인

### 7.2. Thread 관리
- `POST /threads`: Thread 생성
- `GET /threads/{thread_id}/state`: Thread 상태 확인
- `GET /threads/{thread_id}/history`: 실행 히스토리 조회

### 7.3. Run 실행
- `POST /threads/{thread_id}/runs/wait`: 실행 후 결과 대기
- `POST /threads/{thread_id}/runs/stream`: 스트리밍 실행
- `POST /threads/{thread_id}/runs`: 백그라운드 실행

### 7.4. 모니터링
- `GET /info`: 서버 정보
- `GET /metrics`: 시스템 메트릭
- `GET /ok`: 헬스 체크

---

## 8. 트러블슈팅

### 8.1. 일반적인 문제들

**1. "externally-managed-environment" 오류**
```bash
# 해결책: 가상 환경 사용
python3 -m venv langgraph_env
source langgraph_env/bin/activate
pip install -U "langgraph-cli[inmem]"
```

**2. "Required package 'langgraph-api' is not installed" 오류**
```bash
# 해결책: inmem 백엔드 설치
pip install -U "langgraph-cli[inmem]"
```

**3. "404 Not Found" API 오류**
- 루트 경로(`/`)는 지원하지 않음
- `/docs` 또는 Studio UI 사용

**4. 메타데이터 제출 실패 (403 Forbidden)**
- LangChain API 키가 없어서 발생하는 정상적인 경고
- 기능에는 영향 없음

### 8.2. 디버깅 팁

**서버 상태 확인:**
```bash
curl http://127.0.0.1:8123/ok
```

**등록된 그래프 확인:**
```bash
curl http://127.0.0.1:8123/assistants -X POST -H "Content-Type: application/json" -d '{}'
```

---

## 9. 고급 사용법

### 9.1. 조건부 분기 구현

```python
def create_conditional_graph():
    workflow = StateGraph(AgentState)

    # 조건부 라우팅 함수
    def route_condition(state):
        if "error" in state["messages"][-1]:
            return "error_handler"
        return "success_handler"

    # 조건부 엣지 추가
    workflow.add_conditional_edges(
        "analyzer",
        route_condition,
        {"error_handler": "error_node", "success_handler": "success_node"}
    )

    return workflow.compile()
```

### 9.2. Human-in-the-Loop 패턴

```python
def create_hitl_graph():
    workflow = StateGraph(AgentState)

    # 인간 승인 대기 노드
    def human_approval_node(state):
        # 여기서 실제로는 외부 승인 시스템과 연동
        state["messages"].append("Waiting for human approval...")
        return state

    workflow.add_node("human_approval", human_approval_node)
    workflow.add_edge("analyzer", "human_approval")
    workflow.add_edge("human_approval", "final_executor")

    return workflow.compile()
```

---

## 10. 베스트 프랙티스

### 10.1. 개발 권장사항

- **점진적 복잡도 증가**: Single → Sequential → Parallel → Hierarchical
- **상태 관리 중앙화**: 모든 에이전트가 공유하는 중앙 상태 정의
- **에러 처리**: 각 노드에서 발생할 수 있는 예외 상황 고려
- **로깅**: 디버깅을 위한 상세한 로그 기록

### 10.2. 프로덕션 고려사항

- **성능 모니터링**: 각 노드별 실행 시간과 리소스 사용량 추적
- **스케일링**: 워커 수 및 동시 실행 제한 설정
- **보안**: 입력 검증과 출력 필터링 구현
- **관찰 가능성**: 전체 워크플로우 실행 과정 추적 가능

---

## 11. 참고 자료

- **공식 문서**: https://langchain-ai.github.io/langgraph/
- **GitHub**: https://github.com/langchain-ai/langgraph
- **예제 코드**: https://github.com/langchain-ai/langgraph/tree/main/examples
- **LangSmith**: https://smith.langchain.com/

---

## 12. 실습 체크리스트

- [ ] Python 3.11+ 설치 확인
- [ ] 가상 환경 생성 및 활성화
- [ ] LangGraph CLI 설치
- [ ] 기본 프로젝트 구조 생성
- [ ] 간단한 Sequential 에이전트 구현
- [ ] 개발 서버 실행
- [ ] API를 통한 Assistant/Thread/Run 테스트
- [ ] Studio UI에서 시각적 확인
- [ ] 조건부 분기 또는 Loop 패턴 구현

**2025년 9월 기준 최신 정보로 작성된 실무 중심 가이드입니다.**