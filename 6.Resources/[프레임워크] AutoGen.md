---
title: "Microsoft AutoGen 완전 가이드 - 대화형 멀티 에이전트"
type: resource
category: 개발도구/AI프레임워크
tags: [autogen, 멀티에이전트, ai협업, 자동화도구, 파이썬]
status: active
date: 2025-09-24
updated: 2025-09-24
source: ["AutoGen 공식 문서", "Microsoft Research 논문", "실무 프로젝트 경험"]
---

## 🔗 관련 가이드

### 멀티 에이전트 프레임워크
- **[프레임워크] Microsoft AutoGen 완전 가이드 - 대화형 멀티 에이전트** ← **현재 가이드**
- **[[프레임워크] CrewAI]]** - 역할 기반 작업 분담 시스템
- **[[프레임워크] Phidata]]** - 다양한 모달을 활용하는 에이전트
- **[[프레임워크] AgentScope]]** - 대규모 리스케일 에이전트 플랫폼

### 기본 AI 프레임워크
- **[[프레임워크] LangChain]]** - 종합 AI 애플리케이션 프레임워크
- **[[프레임워크] LangGraph]]** - 복잡한 워크플로우 설계
- **[[프레임워크] DSPy]]** - 프롬프트 최적화

### RAG 시스템 가이드
- **[[프롬프트] 11 Retrieval Augmented Generation (RAG) 프롬프팅]]** - RAG 프롬프팅 기법
- **[[[RAG] 04 리트리버(Retriever) 최적화 가이드]]** - 검색 시스템 성능 개선

### 프롬프트 엔지니어링
- **[[프롬프트 엔지니어링 - 마스터 가이드]]** - 전체 프롬프팅 기법 개요
- **[[프롬프트] 04 ReAct 프롬프팅]]** - 추론과 도구 활용 기법

---

## 1. AutoGen 개요

**Microsoft AutoGen**은 대화형 멀티 에이전트 시스템 구축을 위한 프레임워크입니다. 에이전트 간의 '대화'를 통해 복잡한 문제를 협업으로 해결하는 것이 핵심 특징입니다.

### 1.1. 핵심 특징

- **대화 중심**: 에이전트 간 자연스러운 대화로 협업
- **역할 특화**: 각 에이전트가 명확한 역할과 페르소나 보유
- **코드 실행**: 실시간 코드 생성 및 실행 환경 제공
- **Human-in-the-Loop**: 인간이 대화에 자연스럽게 참여
- **확장성**: 2명부터 수십명까지 에이전트 스케일링

### 1.2. 2025년 주요 업데이트

- **AutoGen Studio 2.0**: 노코드 에이전트 구성 환경
- **Multi-Modal 지원**: 텍스트, 이미지, 파일 처리
- **Enterprise Features**: 대규모 배포 및 관리 도구
- **Advanced Workflows**: 복잡한 비즈니스 로직 지원

---

## 2. 설치 및 환경 설정

### 2.1. 기본 설치

```bash
# 가상 환경 생성
python -m venv autogen_env
source autogen_env/bin/activate  # macOS/Linux
# autogen_env\Scripts\activate  # Windows

# AutoGen 설치
pip install pyautogen

# 선택적 의존성
pip install pyautogen[teachable]  # 학습 가능 에이전트
pip install pyautogen[lmm]        # 멀티모달 지원
pip install pyautogen[graph]      # 그래프 시각화
pip install pyautogen[jupyter]    # Jupyter 노트북 지원
```

### 2.2. 환경 변수 설정

**.env 파일:**
```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Azure OpenAI (선택사항)
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Other LLMs
ANTHROPIC_API_KEY=your_claude_key
GOOGLE_API_KEY=your_gemini_key
```

### 2.3. 설정 파일 (OAI_CONFIG_LIST.json)

```json
[
  {
    "model": "gpt-4",
    "api_key": "your_openai_api_key_here",
    "api_type": "openai"
  },
  {
    "model": "gpt-3.5-turbo",
    "api_key": "your_openai_api_key_here",
    "api_type": "openai"
  }
]
```

---

## 3. 기본 사용법

### 3.1. 첫 번째 에이전트 대화

```python
import autogen

# LLM 설정
config_list = [
    {
        "model": "gpt-4",
        "api_key": "your_api_key_here"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
    "timeout": 120,
}

# 사용자 프록시 (인간 대표)
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # 자동 실행
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # Docker 사용 시 True
    },
)

# AI 어시스턴트
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

# 대화 시작
user_proxy.initiate_chat(
    assistant,
    message="파이썬으로 피보나치 수열을 생성하는 함수를 작성하고 테스트해주세요."
)
```

### 3.2. 다중 에이전트 협업

```python
# 전문가 에이전트들
data_scientist = autogen.AssistantAgent(
    name="data_scientist",
    llm_config=llm_config,
    system_message="""
    당신은 데이터 사이언티스트입니다.
    - 데이터 분석과 머신러닝에 전문성을 가지고 있습니다.
    - 통계적 접근과 시각화를 중요시합니다.
    - 코드는 pandas, numpy, matplotlib을 주로 사용합니다.
    """
)

software_engineer = autogen.AssistantAgent(
    name="software_engineer",
    llm_config=llm_config,
    system_message="""
    당신은 소프트웨어 엔지니어입니다.
    - 깔끔하고 유지보수 가능한 코드 작성을 중요시합니다.
    - 성능 최적화와 에러 처리에 신경씁니다.
    - 테스트 코드 작성을 필수로 합니다.
    """
)

# 그룹 채팅 설정
groupchat = autogen.GroupChat(
    agents=[user_proxy, data_scientist, software_engineer],
    messages=[],
    max_round=20,
    speaker_selection_method="round_robin"  # 또는 "auto"
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# 협업 시작
user_proxy.initiate_chat(
    manager,
    message="""
    고객 데이터 분석 시스템을 만들어주세요.
    - CSV 파일을 읽어서 기본 통계를 분석하고
    - 시각화 차트를 생성하며
    - 결과를 웹 대시보드로 표시하는 시스템이 필요합니다.
    """
)
```

---

## 4. 고급 기능

### 4.1. 코드 실행 환경

```python
# Docker 기반 코드 실행
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": True,
        "timeout": 60,
        "last_n_messages": 3,
    }
)

# 커스텀 실행 함수
def custom_execution_function(code: str, lang: str) -> tuple:
    """커스텀 코드 실행 로직"""
    if lang == "python":
        # 보안 검사
        forbidden = ["import os", "import subprocess", "exec("]
        if any(f in code for f in forbidden):
            return 1, "보안상 허용되지 않는 코드입니다."

        # 실행
        try:
            exec_globals = {"__builtins__": __builtins__}
            exec(code, exec_globals)
            return 0, "코드가 성공적으로 실행되었습니다."
        except Exception as e:
            return 1, f"실행 오류: {str(e)}"

    return 1, "지원되지 않는 언어입니다."

# 커스텀 실행기 적용
user_proxy.code_execution_config["function"] = custom_execution_function
```

### 4.2. 전문가 에이전트 페르소나

```python
# 코드 리뷰어
code_reviewer = autogen.AssistantAgent(
    name="code_reviewer",
    llm_config=llm_config,
    system_message="""
    당신은 시니어 코드 리뷰어입니다.

    검토 기준:
    1. 코드 품질: 가독성, 유지보수성, 일관성
    2. 성능: 시간/공간 복잡도, 병목 지점
    3. 보안: 취약점, 입력 검증, 권한 관리
    4. 테스트: 커버리지, 엣지 케이스

    출력 형식:
    - 요약: 전반적인 평가
    - 주요 이슈: 심각도별 분류
    - 개선 제안: 구체적인 코드 예시 포함
    - 승인 여부: APPROVED/NEEDS_REVISION
    """
)

# QA 테스터
qa_tester = autogen.AssistantAgent(
    name="qa_tester",
    llm_config=llm_config,
    system_message="""
    당신은 QA 테스터입니다.

    테스트 전략:
    1. 기능 테스트: 요구사항 충족 여부
    2. 경계값 테스트: 극단적 입력값
    3. 오류 처리: 예외 상황 대응
    4. 사용성: 직관적 인터페이스

    테스트 케이스는 Given-When-Then 형식으로 작성합니다.
    """
)

# 프로덕트 매니저
product_manager = autogen.AssistantAgent(
    name="product_manager",
    llm_config=llm_config,
    system_message="""
    당신은 프로덕트 매니저입니다.

    책임 영역:
    1. 요구사항 명확화: 모호한 요구사항을 구체화
    2. 우선순위 결정: 기능별 중요도와 긴급도
    3. 사용자 관점: 실제 사용 시나리오 고려
    4. 비즈니스 임팩트: ROI와 KPI 영향 분석

    의사결정은 데이터와 사용자 피드백에 기반합니다.
    """
)
```

### 4.3. 조건부 워크플로우

```python
# 조건부 에이전트 선택
def custom_speaker_selection_func(last_speaker, groupchat):
    """마지막 메시지 내용에 따라 다음 발언자 결정"""
    messages = groupchat.messages
    if not messages:
        return None

    last_message = messages[-1]["content"]

    # 키워드 기반 라우팅
    if "코드" in last_message or "함수" in last_message:
        return software_engineer
    elif "데이터" in last_message or "분석" in last_message:
        return data_scientist
    elif "테스트" in last_message or "버그" in last_message:
        return qa_tester
    elif "요구사항" in last_message or "기능" in last_message:
        return product_manager

    return None  # 자동 선택

# 그룹 채팅에 적용
groupchat = autogen.GroupChat(
    agents=[user_proxy, software_engineer, data_scientist, qa_tester, product_manager],
    messages=[],
    max_round=30,
    speaker_selection_method=custom_speaker_selection_func
)
```

---

## 5. 실무 패턴

### 5.1. 코드 개발 파이프라인

```python
class CodeDevelopmentPipeline:
    def __init__(self, config_list):
        self.llm_config = {"config_list": config_list, "temperature": 0.3}
        self.setup_agents()

    def setup_agents(self):
        # 요구사항 분석가
        self.analyst = autogen.AssistantAgent(
            name="analyst",
            llm_config=self.llm_config,
            system_message="요구사항을 분석하고 기술 스펙을 작성하는 전문가"
        )

        # 개발자
        self.developer = autogen.AssistantAgent(
            name="developer",
            llm_config=self.llm_config,
            system_message="클린 코드와 Best Practice를 따르는 개발자"
        )

        # 리뷰어
        self.reviewer = autogen.AssistantAgent(
            name="reviewer",
            llm_config=self.llm_config,
            system_message="코드 품질과 보안을 검토하는 시니어 개발자"
        )

        # 테스터
        self.tester = autogen.AssistantAgent(
            name="tester",
            llm_config=self.llm_config,
            system_message="포괄적인 테스트 케이스를 작성하는 QA 엔지니어"
        )

        # 사용자 프록시
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "development", "use_docker": True}
        )

    def develop_feature(self, requirements):
        """기능 개발 파이프라인 실행"""
        agents = [self.user_proxy, self.analyst, self.developer, self.reviewer, self.tester]

        groupchat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=50,
            speaker_selection_method="round_robin"
        )

        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)

        # 개발 프로세스 시작
        self.user_proxy.initiate_chat(
            manager,
            message=f"""
            다음 요구사항에 따라 기능을 개발해주세요:

            {requirements}

            프로세스:
            1. Analyst: 요구사항 분석 및 기술 스펙 작성
            2. Developer: 코드 구현
            3. Reviewer: 코드 리뷰 및 개선 제안
            4. Tester: 테스트 케이스 작성 및 실행
            5. 필요시 반복 개선

            최종적으로 프로덕션 레디 코드를 생성해주세요.
            """
        )

# 사용 예시
pipeline = CodeDevelopmentPipeline(config_list)
pipeline.develop_feature("""
사용자 인증 시스템을 구현해주세요.
- 이메일/패스워드 로그인
- JWT 토큰 기반 인증
- 비밀번호 해싱 (bcrypt)
- 로그인 시도 제한
- 패스워드 재설정 기능
""")
```

### 5.2. 연구 및 분석 팀

```python
class ResearchTeam:
    def __init__(self, config_list):
        self.llm_config = {"config_list": config_list, "temperature": 0.7}
        self.setup_research_agents()

    def setup_research_agents(self):
        # 리서처
        self.researcher = autogen.AssistantAgent(
            name="researcher",
            llm_config=self.llm_config,
            system_message="""
            당신은 연구 전문가입니다.
            - 신뢰할 수 있는 출처에서 정보를 수집합니다
            - 다각도에서 주제를 분석합니다
            - 편향을 피하고 객관적인 시각을 유지합니다
            - 출처를 명확히 인용합니다
            """
        )

        # 분석가
        self.analyst = autogen.AssistantAgent(
            name="analyst",
            llm_config=self.llm_config,
            system_message="""
            당신은 데이터 분석가입니다.
            - 수집된 정보를 체계적으로 분석합니다
            - 패턴과 트렌드를 식별합니다
            - 정량적/정성적 분석을 수행합니다
            - 결론을 뒷받침하는 증거를 제시합니다
            """
        )

        # 작성자
        self.writer = autogen.AssistantAgent(
            name="writer",
            llm_config=self.llm_config,
            system_message="""
            당신은 기술 작성자입니다.
            - 복잡한 내용을 명확하게 전달합니다
            - 대상 독자에 맞춰 톤을 조절합니다
            - 구조적이고 논리적인 글을 작성합니다
            - 시각적 요소(차트, 다이어그램)를 활용합니다
            """
        )

        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "research"}
        )

    def conduct_research(self, topic, output_format="report"):
        """연구 수행 및 보고서 생성"""
        agents = [self.user_proxy, self.researcher, self.analyst, self.writer]

        groupchat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=30,
            speaker_selection_method="auto"
        )

        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)

        message = f"""
        다음 주제에 대한 종합적인 연구를 수행해주세요: {topic}

        연구 프로세스:
        1. Researcher: 관련 정보 수집 및 출처 정리
        2. Analyst: 수집된 데이터 분석 및 인사이트 도출
        3. Writer: {output_format} 형태로 최종 문서 작성

        최종 결과물은 다음을 포함해야 합니다:
        - 주요 발견사항
        - 트렌드 및 패턴
        - 실무 적용 방안
        - 향후 전망
        - 참고 문헌
        """

        self.user_proxy.initiate_chat(manager, message=message)

# 사용 예시
research_team = ResearchTeam(config_list)
research_team.conduct_research(
    "2025년 생성형 AI의 기업 도입 현황과 전망",
    output_format="executive_summary"
)
```

---

## 6. AutoGen Studio 사용법

### 6.1. 설치 및 실행

```bash
# AutoGen Studio 설치
pip install autogenstudio

# 실행
autogenstudio ui --port 8081
```

### 6.2. 웹 인터페이스 활용

**주요 기능:**
- **드래그 앤 드롭**: 에이전트 시각적 구성
- **템플릿**: 사전 정의된 에이전트 역할
- **실시간 채팅**: 웹 UI에서 직접 대화
- **워크플로우 저장**: 재사용 가능한 설정 저장

**에이전트 구성:**
```json
{
  "name": "research_assistant",
  "type": "assistant",
  "system_message": "연구 보조 전문가",
  "llm_config": {
    "model": "gpt-4",
    "temperature": 0.7
  },
  "tools": ["web_search", "file_reader"]
}
```

---

## 7. 성능 최적화

### 7.1. 토큰 사용량 최적화

```python
# 대화 히스토리 관리
def trim_conversation_history(messages, max_tokens=4000):
    """토큰 수를 제한하여 비용 절약"""
    total_tokens = sum(len(msg["content"].split()) for msg in messages)

    if total_tokens <= max_tokens:
        return messages

    # 중요한 메시지 보존 (시스템 메시지, 최근 메시지)
    system_messages = [msg for msg in messages if msg.get("role") == "system"]
    recent_messages = messages[-10:]  # 최근 10개 메시지

    return system_messages + recent_messages

# 에이전트에 적용
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    max_consecutive_auto_reply=5,  # 자동 응답 제한
    # 커스텀 메시지 처리
)
```

### 7.2. 병렬 처리

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelAutoGen:
    def __init__(self, config_list):
        self.config_list = config_list
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def run_multiple_conversations(self, tasks):
        """여러 대화를 병렬로 실행"""
        loop = asyncio.get_event_loop()

        futures = []
        for task in tasks:
            future = loop.run_in_executor(
                self.executor,
                self.run_single_conversation,
                task
            )
            futures.append(future)

        results = await asyncio.gather(*futures)
        return results

    def run_single_conversation(self, task):
        """단일 대화 실행"""
        # AutoGen 에이전트 설정 및 실행
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
        )

        assistant = autogen.AssistantAgent(
            name="assistant",
            llm_config={"config_list": self.config_list}
        )

        user_proxy.initiate_chat(assistant, message=task["message"])
        return user_proxy.chat_messages

# 사용 예시
parallel_system = ParallelAutoGen(config_list)

tasks = [
    {"message": "파이썬 리스트 정렬 알고리즘 설명해줘"},
    {"message": "데이터베이스 인덱스 최적화 방법은?"},
    {"message": "RESTful API 설계 원칙을 알려줘"}
]

results = asyncio.run(parallel_system.run_multiple_conversations(tasks))
```

---

## 8. 트러블슈팅

### 8.1. 일반적인 문제들

**1. 에이전트가 무한 대화에 빠지는 경우**
```python
# 해결책: 명확한 종료 조건 설정
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").upper(),
)

# 종료 메시지를 명시적으로 요청
system_message = """
작업을 완료하면 반드시 'TERMINATE'로 응답을 마무리하세요.
"""
```

**2. 코드 실행 오류**
```python
# Docker 환경 문제 해결
code_execution_config = {
    "work_dir": "workspace",
    "use_docker": False,  # Docker 문제 시 False로 설정
    "timeout": 60,
    "last_n_messages": 3,
}

# 권한 문제 해결
import os
os.makedirs("workspace", exist_ok=True)
os.chmod("workspace", 0o755)
```

**3. API 요청 한도 초과**
```python
# 요청 간격 조절
import time

def rate_limited_config():
    return {
        "config_list": config_list,
        "timeout": 120,
        "retry_wait_time": 30,  # 재시도 대기 시간
        "max_retries": 3,
    }
```

### 8.2. 디버깅 도구

```python
# 대화 로그 저장
import json
import logging

logging.basicConfig(level=logging.INFO)

def save_conversation_log(chat_messages, filename):
    """대화 내용을 파일로 저장"""
    with open(f"logs/{filename}.json", "w", encoding="utf-8") as f:
        json.dump(chat_messages, f, ensure_ascii=False, indent=2)

# 메시지 분석
def analyze_conversation(messages):
    """대화 패턴 분석"""
    stats = {
        "total_messages": len(messages),
        "agents": set(),
        "average_length": 0,
        "termination_found": False
    }

    total_length = 0
    for msg in messages:
        if "name" in msg:
            stats["agents"].add(msg["name"])

        content = msg.get("content", "")
        total_length += len(content)

        if "TERMINATE" in content.upper():
            stats["termination_found"] = True

    stats["average_length"] = total_length / len(messages) if messages else 0
    stats["agents"] = list(stats["agents"])

    return stats

# 사용
conversation_stats = analyze_conversation(user_proxy.chat_messages)
print(json.dumps(conversation_stats, indent=2))
```

---

## 9. 베스트 프랙티스

### 9.1. 에이전트 설계 원칙

```python
# 1. 명확한 역할 정의
good_system_message = """
당신은 Python 백엔드 개발자입니다.

전문 영역:
- FastAPI, Django 프레임워크
- PostgreSQL, Redis 데이터베이스
- Docker, Kubernetes 배포

작업 방식:
- 코드는 PEP8 스타일을 따릅니다
- 에러 처리를 반드시 포함합니다
- 단위 테스트를 함께 제공합니다
- 보안 취약점을 점검합니다

결과 형식:
- 코드 블록 + 설명
- 실행 방법 안내
- 주의사항 명시
"""

# 2. 상호작용 프로토콜
interaction_protocol = """
다른 에이전트와 협업 시:
- @에이전트명으로 직접 언급
- 완료된 작업은 "✅ 완료: [작업내용]" 형식
- 도움 요청은 "🆘 요청: [구체적 내용]" 형식
- 의견 충돌 시 근거와 대안 제시
"""
```

### 9.2. 워크플로우 최적화

```python
class OptimizedWorkflow:
    def __init__(self):
        self.conversation_history = []
        self.performance_metrics = {}

    def create_focused_agent(self, role, expertise_areas, prohibited_areas=None):
        """집중된 전문성을 가진 에이전트 생성"""
        prohibited = prohibited_areas or []

        system_message = f"""
        역할: {role}
        전문 분야: {', '.join(expertise_areas)}

        작업 범위:
        - 전문 분야 내 질문에만 답변합니다
        - 범위 밖 질문은 적절한 전문가에게 라우팅합니다

        금지 영역: {', '.join(prohibited)}
        이 영역의 질문을 받으면 "이 질문은 {전문가}에게 전달하겠습니다"라고 응답하세요.
        """

        return autogen.AssistantAgent(
            name=role.lower().replace(" ", "_"),
            llm_config=self.llm_config,
            system_message=system_message
        )

    def measure_performance(self, start_time, end_time, message_count, tokens_used):
        """성능 지표 측정"""
        duration = end_time - start_time
        self.performance_metrics.update({
            "duration_seconds": duration,
            "messages_per_second": message_count / duration,
            "tokens_per_message": tokens_used / message_count if message_count > 0 else 0,
            "efficiency_score": (message_count * 100) / tokens_used if tokens_used > 0 else 0
        })
        return self.performance_metrics
```

---

## 10. 실습 프로젝트

### 10.1. 소프트웨어 개발팀 시뮬레이션

```python
class SoftwareDevelopmentTeam:
    def __init__(self, config_list):
        self.config_list = config_list
        self.setup_team()

    def setup_team(self):
        """개발팀 구성"""
        base_config = {"config_list": self.config_list, "temperature": 0.5}

        # 팀 리더
        self.tech_lead = autogen.AssistantAgent(
            name="tech_lead",
            llm_config=base_config,
            system_message="""
            기술 리더로서 아키텍처 결정과 코드 리뷰를 담당합니다.
            - 기술 스택 선택과 아키텍처 설계
            - 코드 품질과 표준 관리
            - 팀원 간 의견 조율
            - 기술적 위험 요소 식별
            """
        )

        # 풀스택 개발자
        self.fullstack_dev = autogen.AssistantAgent(
            name="fullstack_developer",
            llm_config=base_config,
            system_message="""
            풀스택 개발자로서 프론트엔드와 백엔드를 모두 담당합니다.
            - React/Vue.js 프론트엔드 개발
            - Node.js/Python 백엔드 개발
            - API 설계 및 데이터베이스 연동
            - 반응형 UI/UX 구현
            """
        )

        # DevOps 엔지니어
        self.devops = autogen.AssistantAgent(
            name="devops_engineer",
            llm_config=base_config,
            system_message="""
            DevOps 엔지니어로서 배포와 인프라를 담당합니다.
            - CI/CD 파이프라인 구축
            - Docker, Kubernetes 컨테이너 관리
            - 클라우드 인프라 설계 (AWS/Azure/GCP)
            - 모니터링 및 로깅 시스템
            """
        )

        # QA 엔지니어
        self.qa_engineer = autogen.AssistantAgent(
            name="qa_engineer",
            llm_config=base_config,
            system_message="""
            QA 엔지니어로서 품질 보증을 담당합니다.
            - 테스트 계획 수립 및 실행
            - 자동화 테스트 스크립트 작성
            - 버그 리포트 및 재현 시나리오
            - 성능 및 보안 테스트
            """
        )

        self.user_proxy = autogen.UserProxyAgent(
            name="product_owner",
            human_input_mode="NEVER",
            code_execution_config={
                "work_dir": "project_workspace",
                "use_docker": True
            }
        )

    def develop_project(self, project_requirements):
        """프로젝트 개발 수행"""
        team = [
            self.user_proxy,
            self.tech_lead,
            self.fullstack_dev,
            self.devops,
            self.qa_engineer
        ]

        groupchat = autogen.GroupChat(
            agents=team,
            messages=[],
            max_round=100,
            speaker_selection_method="auto"
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config={"config_list": self.config_list}
        )

        self.user_proxy.initiate_chat(
            manager,
            message=f"""
            새로운 프로젝트를 시작합니다: {project_requirements}

            개발 프로세스:
            1. Tech Lead: 기술 스택 및 아키텍처 설계
            2. Fullstack Dev: 핵심 기능 구현
            3. DevOps: 배포 환경 구축
            4. QA: 테스트 계획 및 실행
            5. 팀 협업을 통한 이슈 해결

            최종 목표: 프로덕션 배포 가능한 완성된 애플리케이션
            """
        )

# 사용 예시
dev_team = SoftwareDevelopmentTeam(config_list)
dev_team.develop_project("""
온라인 북마크 관리 시스템

주요 기능:
- 사용자 회원가입/로그인
- 북마크 추가/편집/삭제
- 태그 기반 분류
- 검색 및 필터링
- 소셜 공유 기능

기술 요구사항:
- 반응형 웹 인터페이스
- RESTful API
- 사용자 인증 및 권한 관리
- 데이터베이스 최적화
- 클라우드 배포
""")
```

---

## 11. 참고 자료

### 11.1. 공식 문서
- **AutoGen GitHub**: https://github.com/microsoft/autogen
- **공식 문서**: https://microsoft.github.io/autogen/
- **AutoGen Studio**: https://github.com/microsoft/autogen/tree/main/samples/apps/autogen-studio

### 11.2. 커뮤니티
- **Discord**: Microsoft AutoGen Community
- **논문**: "AutoGen: Enabling Next-Gen LLM Applications"
- **YouTube**: AutoGen Tutorial Series

### 11.3. 관련 도구
- **Jupyter Integration**: AutoGen + Jupyter Notebook
- **Docker Images**: 사전 구성된 AutoGen 환경
- **VS Code Extension**: AutoGen 개발 도구

---

## 12. 체크리스트

**기본 설정:**
- [ ] Python 3.8+ 환경 준비
- [ ] AutoGen 패키지 설치
- [ ] LLM API 키 설정
- [ ] 기본 에이전트 대화 테스트

**멀티 에이전트:**
- [ ] 2-3개 에이전트 협업 구현
- [ ] 역할별 시스템 메시지 최적화
- [ ] 그룹 채팅 관리자 설정
- [ ] 종료 조건 명확화

**고급 기능:**
- [ ] 코드 실행 환경 구성
- [ ] 조건부 워크플로우 구현
- [ ] 성능 모니터링 도구 적용
- [ ] 오류 처리 및 복구 로직

**프로덕션:**
- [ ] AutoGen Studio 활용
- [ ] 보안 설정 강화
- [ ] 비용 최적화 적용
- [ ] 로깅 및 디버깅 환경

**2025년 9월 기준 최신 AutoGen 기능과 실무 패턴을 반영한 종합 가이드입니다.**