---
title: "Google ADK 모듈 분석"
type: resource
category: AI 개발
tags: [자료/기술, 기술/SDK, 주제/AI-에이전트]
date: 2025-09-20
updated: 2025-09-20
---


## 1. 개요

본 문서는 Google Agent Development Kit (ADK)의 주요 모듈들을 분석하고 각 모듈의 역할과 활용 예시를 제공합니다. ADK는 LLM 기반 에이전트 시스템을 구축하기 위한 프레임워크입니다.

---

## 2. 주요 모듈 분석

### 2.1. `google.adk.agents`

-   **설명**: 에이전트 정의, 실행 흐름 제어, 다중 에이전트 구조 설계 담당. LLM 기반 에이전트, 시퀀셜 에이전트, 커스텀 에이전트 등을 생성하고 제어할 수 있습니다.
-   **주요 클래스**: `LlmAgent`, `Agent`, `BaseAgent`, `SequentialAgent`
-   **예시**:
    ```python
    from google.adk.agents import LlmAgent, Agent
    from google.adk.models.lite_llm import LiteLlm

    root_agent = Agent(
        name="basic_search_agent",
        model=LiteLlm(model="ollama/deepseek-r1:8b"),
        description="Agent to answer questions.",
        instruction="You are an expert researcher. You always stick to the facts."
    )
    ```

### 2.2. `google.adk.artifacts`

-   **설명**: 대용량 텍스트, JSON, 바이너리 등 아티팩트 데이터를 관리하는 모듈.
-   **주요 클래스**: `Artifact`, `TextArtifact`, `BinaryArtifact`
-   **예시**:
    ```python
    from google.adk.artifacts import TextArtifact

    doc = TextArtifact(content="This is a knowledge base entry.")
    print(doc.content)
    ```

### 2.3. `google.adk.code_executors`

-   **설명**: 코드 실행을 위한 실행기(executor) 제공. 에이전트가 Python 등 코드를 실행할 수 있도록 지원합니다.
-   **주요 클래스**: `CodeExecutor`, `PythonCodeExecutor`
-   **예시**:
    ```python
    from google.adk.code_executors import PythonCodeExecutor

    executor = PythonCodeExecutor()
    result = executor.execute("print(2 + 3)")
    ```

### 2.4. `google.adk.evaluation`

-   **설명**: 에이전트/LLM 출력 결과에 대한 품질 평가 도구.
-   **주요 클래스**: `Evaluator`, `ComparisonEvaluator`, `ScoringEvaluator`
-   **예시**:
    ```python
    from google.adk.evaluation import Evaluator

    evaluator = Evaluator(criteria="accuracy")
    score = evaluator.evaluate("정답", "예상 출력")
    ```

### 2.5. `google.adk.events`

-   **설명**: 실행 과정에서 발생하는 이벤트(로그, 상태 변화)를 관리.
-   **주요 클래스**: `Event`, `AgentEvent`, `RunEvent`
-   **예시**:
    ```python
    from google.adk.events import AgentEvent

    event = AgentEvent(name="AgentStarted", payload={"agent": "basic_search_agent"})
    print(event)
    ```

### 2.6. `google.adk.models`

-   **설명**: LLM, Embedding 등 모델 추상화 계층을 제공.
-   **주요 클래스**: `LiteLlm`, `VertexLlm`, `OpenAILlm`
-   **예시**:
    ```python
    from google.adk.models.lite_llm import LiteLlm

    model = LiteLlm(model="ollama/deepseek-r1:8b")
    ```

### 2.7. `google.adk.planners`

-   **설명**: 복잡한 작업 플로우를 계획(Planning)하는 모듈.
-   **주요 클래스**: `Planner`, `TaskPlanner`
-   **예시**:
    ```python
    from google.adk.planners import Planner

    planner = Planner()
    steps = planner.plan("사용자 질문 분석 후 답변 생성")
    ```

### 2.8. `google.adk.runners`

-   **설명**: 에이전트 실행 및 Orchestration 담당.
-   **주요 클래스**: `Runner`, `AsyncRunner`
-   **예시**:
    ```python
    from google.adk.runners import Runner

    runner = Runner(agent=root_agent)
    runner.run("서울 날씨 알려줘")
    ```

### 2.9. `google.adk.sessions`

-   **설명**: 세션 기반으로 대화 상태, 컨텍스트 관리.
-   **주요 클래스**: `Session`, `SessionManager`
-   **예시**:
    ```python
    from google.adk.sessions import Session

    session = Session(user_id="user123")
    session.add_message("user", "안녕?")
    ```

### 프로젝트 활용
- AI 에이전트 시스템 아키텍처 설계
- 기술 스택 선정 및 모듈별 기능 매핑
- 복잡한 워크플로우 자동화 구현

## 🏷️ 관련 키워드

`google-adk` `ai-agent` `llm-framework` `python-sdk` `google-cloud`

