---
title: "[프레임워크] Google ADK 완전 가이드 - 구글 에이전트 개발 키트"
type: resource
category: AI/프레임워크
tags: [google-adk, 구글, AI에이전트, 멀티에이전트, gemini, 클라우드]
source: "공식 문서 및 실습 기반 작성"
status: active
updated: 2025-09-24
---

## 🔗 관련 가이드

### 엔터프라이즈 AI 프레임워크
- **[프레임워크] Google ADK 완전 가이드 - 구글 에이전트 개발 키트** ← **현재 가이드**
- **[[프레임워크] Haystack]]** - 엔터프라이즈 RAG 솔루션
- **[[프레임워크] AgentScope]]** - 대규모 에이전트 플랫폼

### 멀티 에이전트 프레임워크
- **[[프레임워크] AutoGen]]** - 대화형 에이전트 시스템
- **[[프레임워크] CrewAI]]** - 역할 기반 작업 분담
- **[[프레임워크] Phidata]]** - 다양한 모달을 활용하는 에이전트

### 기본 AI 프레임워크
- **[[프레임워크] LangChain]]** - 종합 AI 애플리케이션 프레임워크
- **[[프레임워크] LlamaIndex]]** - RAG 특화 데이터 연결
- **[[프레임워크] DSPy]]** - 프롬프트 최적화

### 프롬프트 엔지니어링
- **[[프롬프트 엔지니어링 - 마스터 가이드]]** - 전체 프롬프팅 기법 개요

---

# 1. 개요

Google Agent Development Kit (ADK)는 **코드 우선적이고 모듈형인 AI 에이전트 구축 프레임워크**입니다. Gemini와 Google 생태계에 최적화되어 있지만, **모델 및 배포 환경에 구애받지 않는** 유연한 구조를 제공합니다.

## 핵심 특징

### 🎯 Google의 공식 프레임워크
- **Google 개발**: 구글이 직접 개발하고 유지보수하는 공식 ADK
- **Gemini 최적화**: Google의 최신 AI 모델과 완벽 통합
- **Google Cloud 통합**: Vertex AI와 자연스러운 연동
- **Enterprise 급**: 프로덕션 환경을 고려한 견고한 아키텍처

### 🔧 핵심 역량
- **멀티 에이전트 설계**: 병렬, 순차, 계층적 워크플로우
- **모델 중립적**: Gemini, GPT-4o, Claude, Mistral 등 지원
- **실시간 상호작용**: 양방향 오디오/비디오 스트리밍
- **모듈형 아키텍처**: 전문화된 에이전트 구성과 지능형 위임

---

# 2. 설치 및 환경 설정

## 2.1. Python 설치

```bash
# 가상환경 생성 (권장)
python3 -m venv adk_env
source adk_env/bin/activate  # macOS/Linux
# adk_env\Scripts\activate  # Windows

# 기본 설치
pip install google-adk

# 완전 설치 (권장)
pip install google-adk litellm fastapi uvicorn httpx pydantic openai streamlit

# 개발 버전 설치 (최신 기능)
pip install git+https://github.com/google/adk-python.git@main
```

## 2.2. Java 설치 (Maven)

```xml
<dependencies>
    <!-- ADK 코어 라이브러리 -->
    <dependency>
        <groupId>com.google.adk</groupId>
        <artifactId>google-adk</artifactId>
        <version>0.2.0</version>
    </dependency>
    <!-- ADK 개발 웹 UI (선택사항) -->
    <dependency>
        <groupId>com.google.adk</groupId>
        <artifactId>google-adk-dev</artifactId>
        <version>0.2.0</version>
    </dependency>
</dependencies>
```

## 2.3. API 키 설정

```bash
# .env 파일 생성
GOOGLE_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-key  # 선택사항
ANTHROPIC_API_KEY=your-claude-key  # 선택사항

# 환경 변수 설정
export GOOGLE_API_KEY=your-gemini-api-key
```

## 2.4. 설치 확인

```python
import google.adk
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

print(f"✅ Google ADK 설치 완료")
print(f"ADK version: {google.adk.__version__}")

# 기본 에이전트 테스트
test_agent = Agent(
    name="test_agent",
    model=LiteLlm(model="gemini/gemini-pro"),
    description="Test agent for verification"
)

print("✅ 에이전트 생성 성공")
```

---

# 3. 기본 사용법

## 3.1. 간단한 에이전트 생성

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner

# 기본 에이전트 생성
basic_agent = Agent(
    name="basic_assistant",
    model=LiteLlm(model="gemini/gemini-pro"),
    description="Helpful assistant agent",
    instruction="You are a helpful assistant. Answer questions clearly and concisely."
)

# 에이전트 실행
runner = Runner(agent=basic_agent)
response = runner.run("What is artificial intelligence?")
print(response)
```

## 3.2. 도구를 사용하는 에이전트

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
import requests
from typing import Dict, Any

def search_web(query: str) -> Dict[str, Any]:
    """웹 검색 도구"""
    # 실제 구현에서는 실제 검색 API 사용
    return {
        "query": query,
        "results": f"Search results for '{query}': Relevant information found."
    }

def get_weather(city: str) -> Dict[str, Any]:
    """날씨 정보 도구"""
    # 실제 구현에서는 날씨 API 사용
    return {
        "city": city,
        "weather": f"Weather in {city}: Sunny, 22°C"
    }

# 도구가 있는 에이전트
tool_agent = Agent(
    name="tool_agent",
    model=LiteLlm(model="gemini/gemini-pro"),
    description="Agent with web search and weather tools",
    instruction="""You are an assistant with access to web search and weather information.
    Use the appropriate tool when needed to answer user questions.""",
    tools=[search_web, get_weather]
)

# 실행
runner = Runner(agent=tool_agent)
response = runner.run("What's the weather like in Seoul and find recent news about AI?")
print(response)
```

## 3.3. 세션 기반 대화

```python
from google.adk.sessions import Session
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner

# 세션 생성
session = Session(user_id="user123")

# 에이전트 생성
chat_agent = Agent(
    name="chat_agent",
    model=LiteLlm(model="gemini/gemini-pro"),
    description="Conversational agent with memory",
    instruction="You are a helpful assistant. Remember our conversation context."
)

# 세션과 함께 실행
runner = Runner(agent=chat_agent, session=session)

# 첫 번째 대화
response1 = runner.run("My name is John and I'm a software developer.")
print(f"Agent: {response1}")

# 두 번째 대화 (이전 컨텍스트 기억)
response2 = runner.run("What programming languages should I learn?")
print(f"Agent: {response2}")

# 세션 정보 확인
print(f"Session messages: {len(session.messages)}")
```

---

# 4. 고급 활용법

## 4.1. 멀티 에이전트 시스템 - 순차 실행

```python
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner

# 개별 에이전트들 생성
research_agent = Agent(
    name="researcher",
    model=LiteLlm(model="gemini/gemini-pro"),
    description="Research specialist",
    instruction="Research the given topic thoroughly and provide factual information."
)

analysis_agent = Agent(
    name="analyst",
    model=LiteLlm(model="gemini/gemini-pro"),
    description="Analysis specialist",
    instruction="Analyze the research data and provide insights and recommendations."
)

writer_agent = Agent(
    name="writer",
    model=LiteLlm(model="gemini/gemini-pro"),
    description="Content writer",
    instruction="Create a well-structured article based on research and analysis."
)

# 순차 에이전트 생성
sequential_workflow = SequentialAgent(
    name="content_creation_workflow",
    agents=[research_agent, analysis_agent, writer_agent],
    description="Sequential workflow for content creation"
)

# 실행
runner = Runner(agent=sequential_workflow)
result = runner.run("Create an article about sustainable energy solutions")
print(result)
```

## 4.2. 계층적 에이전트 시스템

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.planners import Planner
from google.adk.runners import Runner

class BusinessAnalysisSystem:
    def __init__(self):
        self.setup_agents()
        self.setup_orchestrator()

    def setup_agents(self):
        """전문 에이전트들 구성"""
        # 시장 조사 에이전트
        self.market_researcher = Agent(
            name="market_researcher",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Market research specialist",
            instruction="""You are a market research expert.
            Analyze market trends, competitor landscape, and industry insights."""
        )

        # 재무 분석가
        self.financial_analyst = Agent(
            name="financial_analyst",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Financial analysis expert",
            instruction="""You are a financial analyst.
            Analyze financial data, profitability, and investment opportunities."""
        )

        # 전략 기획자
        self.strategist = Agent(
            name="strategist",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Business strategy consultant",
            instruction="""You are a strategy consultant.
            Synthesize research and financial data into actionable business strategies."""
        )

    def setup_orchestrator(self):
        """오케스트레이터 에이전트 구성"""
        self.orchestrator = Agent(
            name="business_orchestrator",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Business analysis orchestrator",
            instruction="""You coordinate business analysis workflow.
            Delegate tasks to appropriate specialists and synthesize results."""
        )

    def analyze_business_opportunity(self, business_idea: str):
        """비즈니스 기회 분석"""
        # 시장 조사
        market_runner = Runner(agent=self.market_researcher)
        market_analysis = market_runner.run(
            f"Conduct market research for this business idea: {business_idea}"
        )

        # 재무 분석
        financial_runner = Runner(agent=self.financial_analyst)
        financial_analysis = financial_runner.run(
            f"Analyze financial aspects of this business: {business_idea}\n"
            f"Market context: {market_analysis}"
        )

        # 전략 수립
        strategy_runner = Runner(agent=self.strategist)
        strategy = strategy_runner.run(
            f"Develop business strategy based on:\n"
            f"Business idea: {business_idea}\n"
            f"Market analysis: {market_analysis}\n"
            f"Financial analysis: {financial_analysis}"
        )

        return {
            "market_analysis": market_analysis,
            "financial_analysis": financial_analysis,
            "strategy": strategy
        }

# 사용 예제
business_system = BusinessAnalysisSystem()
result = business_system.analyze_business_opportunity(
    "AI 기반 개인화 학습 플랫폼"
)

print("=== 시장 분석 ===")
print(result["market_analysis"])
print("\n=== 재무 분석 ===")
print(result["financial_analysis"])
print("\n=== 전략 수립 ===")
print(result["strategy"])
```

## 4.3. 코드 실행 에이전트

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.code_executors import PythonCodeExecutor
from google.adk.runners import Runner

# 코드 실행기 생성
code_executor = PythonCodeExecutor()

# 코드 실행 에이전트
code_agent = Agent(
    name="code_analyst",
    model=LiteLlm(model="gemini/gemini-pro"),
    description="Data analysis agent with Python code execution",
    instruction="""You are a data analyst that can execute Python code.
    When asked to analyze data or perform calculations, write and execute Python code.
    Always explain your code and interpret the results.""",
    code_executor=code_executor
)

# 실행
runner = Runner(agent=code_agent)
response = runner.run("""
Analyze the following sales data and calculate trends:
Monthly sales: [120, 135, 158, 142, 165, 180, 195, 210, 188, 205, 225, 240]
Create a simple visualization and calculate growth rate.
""")

print(response)
```

---

# 5. 실제 프로젝트 예제

## 5.1. 고객 서비스 자동화 시스템

```python
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import Session, SessionManager
from google.adk.runners import Runner
from google.adk.events import AgentEvent
import json
from datetime import datetime
from typing import Dict, List

class CustomerServiceSystem:
    def __init__(self):
        self.session_manager = SessionManager()
        self.setup_agents()
        self.ticket_database = {}

    def setup_agents(self):
        """고객 서비스 에이전트 구성"""

        # 1차 접수 에이전트
        self.intake_agent = Agent(
            name="intake_specialist",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Customer inquiry intake specialist",
            instruction="""You are a customer service intake specialist.
            Your role is to:
            1. Greet customers warmly
            2. Understand their issue clearly
            3. Classify the inquiry type (technical, billing, general, complaint)
            4. Gather necessary information
            5. Route to appropriate specialist if needed
            """
        )

        # 기술 지원 에이전트
        self.tech_support = Agent(
            name="tech_support",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Technical support specialist",
            instruction="""You are a technical support specialist.
            Provide step-by-step troubleshooting solutions.
            Ask clarifying questions when needed.
            Escalate complex issues appropriately.
            """
        )

        # 빌링 지원 에이전트
        self.billing_support = Agent(
            name="billing_support",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Billing and account specialist",
            instruction="""You are a billing support specialist.
            Handle account inquiries, billing questions, and payment issues.
            Provide clear explanations of charges and policies.
            """
        )

        # 에스컬레이션 매니저
        self.escalation_manager = Agent(
            name="escalation_manager",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Customer escalation manager",
            instruction="""You are an escalation manager.
            Handle complex complaints and difficult situations.
            Make decisions on refunds, compensations, and policy exceptions.
            Ensure customer satisfaction while protecting company interests.
            """
        )

    def create_ticket(self, customer_id: str, inquiry: str) -> str:
        """고객 티켓 생성"""
        ticket_id = f"TICKET-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        ticket = {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "inquiry": inquiry,
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "interactions": []
        }

        self.ticket_database[ticket_id] = ticket
        return ticket_id

    def process_customer_inquiry(self, customer_id: str, inquiry: str):
        """고객 문의 처리"""
        # 티켓 생성
        ticket_id = self.create_ticket(customer_id, inquiry)

        # 세션 생성
        session = Session(user_id=customer_id)

        # 1차 접수 처리
        intake_runner = Runner(agent=self.intake_agent, session=session)
        intake_response = intake_runner.run(inquiry)

        # 티켓 업데이트
        self.ticket_database[ticket_id]["interactions"].append({
            "agent": "intake_specialist",
            "response": intake_response,
            "timestamp": datetime.now().isoformat()
        })

        # 문의 유형 분류 (실제 구현에서는 NLP 분류 모델 사용)
        inquiry_type = self.classify_inquiry(inquiry)

        # 적절한 전문가에게 라우팅
        if inquiry_type == "technical":
            specialist_runner = Runner(agent=self.tech_support, session=session)
            specialist_response = specialist_runner.run(
                f"Customer inquiry: {inquiry}\n"
                f"Initial assessment: {intake_response}"
            )
            routing_info = "Routed to Technical Support"

        elif inquiry_type == "billing":
            specialist_runner = Runner(agent=self.billing_support, session=session)
            specialist_response = specialist_runner.run(
                f"Customer inquiry: {inquiry}\n"
                f"Initial assessment: {intake_response}"
            )
            routing_info = "Routed to Billing Support"

        elif inquiry_type == "complaint":
            specialist_runner = Runner(agent=self.escalation_manager, session=session)
            specialist_response = specialist_runner.run(
                f"Customer complaint: {inquiry}\n"
                f"Initial assessment: {intake_response}"
            )
            routing_info = "Escalated to Management"

        else:
            specialist_response = intake_response
            routing_info = "Handled by Intake Specialist"

        # 최종 티켓 업데이트
        self.ticket_database[ticket_id]["interactions"].append({
            "agent": routing_info,
            "response": specialist_response,
            "timestamp": datetime.now().isoformat()
        })
        self.ticket_database[ticket_id]["status"] = "resolved"

        return {
            "ticket_id": ticket_id,
            "routing": routing_info,
            "final_response": specialist_response,
            "session_id": session.session_id
        }

    def classify_inquiry(self, inquiry: str) -> str:
        """문의 유형 분류"""
        inquiry_lower = inquiry.lower()

        if any(keyword in inquiry_lower for keyword in
               ["error", "bug", "not working", "crashed", "technical", "setup"]):
            return "technical"
        elif any(keyword in inquiry_lower for keyword in
                 ["bill", "charge", "payment", "refund", "account", "subscription"]):
            return "billing"
        elif any(keyword in inquiry_lower for keyword in
                 ["complaint", "unsatisfied", "angry", "terrible", "worst"]):
            return "complaint"
        else:
            return "general"

    def get_ticket_status(self, ticket_id: str):
        """티켓 상태 조회"""
        return self.ticket_database.get(ticket_id, "Ticket not found")

# 사용 예제
cs_system = CustomerServiceSystem()

# 다양한 문의 처리
inquiries = [
    {
        "customer_id": "CUST001",
        "inquiry": "My app keeps crashing when I try to upload photos. Can you help?"
    },
    {
        "customer_id": "CUST002",
        "inquiry": "I was charged twice for my subscription this month. I need a refund."
    },
    {
        "customer_id": "CUST003",
        "inquiry": "Your customer service is terrible! I've been waiting for a response for days!"
    }
]

for inquiry_data in inquiries:
    print(f"\n{'='*50}")
    print(f"Processing inquiry from {inquiry_data['customer_id']}")
    print(f"Inquiry: {inquiry_data['inquiry']}")

    result = cs_system.process_customer_inquiry(
        inquiry_data["customer_id"],
        inquiry_data["inquiry"]
    )

    print(f"Ticket ID: {result['ticket_id']}")
    print(f"Routing: {result['routing']}")
    print(f"Response: {result['final_response']}")
```

## 5.2. 콘텐츠 제작 파이프라인

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.artifacts import TextArtifact
import json

class ContentCreationPipeline:
    def __init__(self):
        self.setup_agents()

    def setup_agents(self):
        """콘텐츠 제작 에이전트들 구성"""

        # SEO 분석가
        self.seo_analyst = Agent(
            name="seo_analyst",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="SEO and keyword research specialist",
            instruction="""You are an SEO expert.
            Analyze topics for keyword opportunities, search intent, and SEO potential.
            Provide keyword suggestions and content optimization recommendations.
            """
        )

        # 콘텐츠 기획자
        self.content_strategist = Agent(
            name="content_strategist",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Content strategy and planning specialist",
            instruction="""You are a content strategist.
            Create comprehensive content plans including structure, key points, and audience targeting.
            Consider engagement, value proposition, and content goals.
            """
        )

        # 작가
        self.writer = Agent(
            name="content_writer",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Professional content writer",
            instruction="""You are a skilled content writer.
            Create engaging, well-structured, and valuable content.
            Adapt tone and style for the target audience.
            Focus on readability and engagement.
            """
        )

        # 편집자
        self.editor = Agent(
            name="editor",
            model=LiteLlm(model="gemini/gemini-pro"),
            description="Content editor and quality assurance",
            instruction="""You are a content editor.
            Review content for grammar, clarity, flow, and overall quality.
            Suggest improvements and ensure consistent style.
            Check for factual accuracy and proper structure.
            """
        )

    def create_blog_post(self, topic: str, target_audience: str, word_count: int = 1500):
        """블로그 포스트 생성 파이프라인"""

        # 1단계: SEO 분석
        seo_runner = Runner(agent=self.seo_analyst)
        seo_analysis = seo_runner.run(
            f"Analyze SEO opportunities for the topic '{topic}' "
            f"targeting {target_audience}. Provide keyword suggestions and search intent analysis."
        )

        # 2단계: 콘텐츠 기획
        strategy_runner = Runner(agent=self.content_strategist)
        content_plan = strategy_runner.run(
            f"Create a comprehensive content plan for a {word_count}-word blog post about '{topic}' "
            f"for {target_audience}. Use this SEO analysis: {seo_analysis}"
        )

        # 3단계: 글 작성
        writer_runner = Runner(agent=self.writer)
        draft_content = writer_runner.run(
            f"Write a {word_count}-word blog post following this plan: {content_plan}"
        )

        # 4단계: 편집
        editor_runner = Runner(agent=self.editor)
        final_content = editor_runner.run(
            f"Edit and improve this blog post: {draft_content}"
        )

        return {
            "seo_analysis": seo_analysis,
            "content_plan": content_plan,
            "draft_content": draft_content,
            "final_content": final_content
        }

    def create_social_media_campaign(self, product: str, campaign_goal: str):
        """소셜 미디어 캠페인 생성"""

        # 전략 수립
        strategy_runner = Runner(agent=self.content_strategist)
        campaign_strategy = strategy_runner.run(
            f"Create a social media campaign strategy for '{product}' "
            f"with the goal of {campaign_goal}. Include platform recommendations and content types."
        )

        # 콘텐츠 생성
        writer_runner = Runner(agent=self.writer)
        social_content = writer_runner.run(
            f"Create social media content based on this strategy: {campaign_strategy}. "
            f"Include posts for different platforms (Instagram, Twitter, LinkedIn, Facebook)."
        )

        # SEO 최적화 (해시태그, 키워드)
        seo_runner = Runner(agent=self.seo_analyst)
        seo_optimization = seo_runner.run(
            f"Optimize this social media content for discoverability: {social_content}. "
            f"Suggest relevant hashtags and keywords for each platform."
        )

        return {
            "campaign_strategy": campaign_strategy,
            "social_content": social_content,
            "seo_optimization": seo_optimization
        }

# 사용 예제
content_pipeline = ContentCreationPipeline()

# 블로그 포스트 생성
blog_result = content_pipeline.create_blog_post(
    topic="AI 에이전트를 활용한 비즈니스 자동화",
    target_audience="중소기업 CEO 및 IT 담당자",
    word_count=2000
)

# 소셜 미디어 캠페인 생성
social_result = content_pipeline.create_social_media_campaign(
    product="AI 마케팅 자동화 도구",
    campaign_goal="브랜드 인지도 향상 및 리드 생성"
)

# 결과 저장
output = {
    "blog_post": blog_result,
    "social_campaign": social_result,
    "created_at": datetime.now().isoformat()
}

with open("content_creation_results.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ 콘텐츠 제작 파이프라인 완료")
```

---

# 6. 프로덕션 배포

## 6.1. ADK 웹 UI 서버

```python
# main.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
import os

# 에이전트 생성
agent = Agent(
    name="production_agent",
    model=LiteLlm(model="gemini/gemini-pro"),
    description="Production ready agent",
    instruction="You are a helpful assistant optimized for production use."
)

# ADK 웹 UI로 실행
if __name__ == "__main__":
    # 터미널에서 실행
    # adk web --agent main:agent --port 8080
    pass
```

```bash
# ADK 웹 UI 실행
adk web --agent main:agent --port 8080

# API 서버 실행
adk api_server --agent main:agent --port 8000

# 터미널에서 직접 실행
adk run --agent main:agent
```

## 6.2. FastAPI 통합

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import SessionManager
import uvicorn
import os

app = FastAPI(title="Google ADK API", version="1.0.0")

# 글로벌 객체들
agent = None
session_manager = None

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.on_event("startup")
async def startup_event():
    """서버 시작시 초기화"""
    global agent, session_manager

    # 에이전트 초기화
    agent = Agent(
        name="api_agent",
        model=LiteLlm(model="gemini/gemini-pro"),
        description="API service agent",
        instruction="""You are an API service agent.
        Provide helpful, accurate, and concise responses.
        Maintain conversation context when session_id is provided.
        """
    )

    # 세션 매니저 초기화
    session_manager = SessionManager()

    print("✅ Google ADK API 서버 초기화 완료")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """채팅 엔드포인트"""
    try:
        # 세션 관리
        if request.session_id:
            session = session_manager.get_session(request.session_id)
        else:
            session = session_manager.create_session()

        # 에이전트 실행
        runner = Runner(agent=agent, session=session)
        response = runner.run(request.message)

        return ChatResponse(
            response=response,
            session_id=session.session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "agent_name": agent.name if agent else "Not loaded",
        "active_sessions": len(session_manager.sessions) if session_manager else 0
    }

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """세션 정보 조회"""
    session = session_manager.get_session(session_id)
    if session:
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "message_count": len(session.messages)
        }
    else:
        raise HTTPException(status_code=404, detail="Session not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 6.3. Docker 배포

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 환경 변수
ENV PYTHONPATH=/app
ENV PORT=8000

# 포트 노출
EXPOSE 8000

# 헬스체크
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 서버 실행
CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  google-adk-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENVIRONMENT=production
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=adk_sessions
      - POSTGRES_USER=adk_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
```

## 6.4. Google Cloud 배포

```yaml
# app.yaml (Google App Engine)
runtime: python311

env_variables:
  GOOGLE_API_KEY: "your-gemini-api-key"
  ENVIRONMENT: "production"

resources:
  cpu: 2
  memory_gb: 4

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

```bash
# Google Cloud 배포
gcloud app deploy app.yaml

# Cloud Run 배포
gcloud run deploy google-adk-api \
  --source . \
  --port 8000 \
  --set-env-vars GOOGLE_API_KEY=${GOOGLE_API_KEY} \
  --allow-unauthenticated
```

---

# 7. 모범 사례 및 최적화

## 7.1. 성능 최적화

### 7.1.1. 모델 선택 전략

```python
from google.adk.models.lite_llm import LiteLlm

class OptimizedModelFactory:
    """작업별 최적화된 모델 선택"""

    @staticmethod
    def get_fast_model():
        """빠른 응답이 필요한 작업"""
        return LiteLlm(model="gemini/gemini-flash")

    @staticmethod
    def get_smart_model():
        """복잡한 추론이 필요한 작업"""
        return LiteLlm(model="gemini/gemini-pro")

    @staticmethod
    def get_multimodal_model():
        """멀티모달 작업"""
        return LiteLlm(model="gemini/gemini-pro-vision")

    @staticmethod
    def get_coding_model():
        """코딩 작업"""
        return LiteLlm(model="gemini/gemini-pro")
```

### 7.1.2. 캐싱 전략

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
import hashlib
import time
from typing import Dict, Any

class CachedRunner:
    def __init__(self, agent: Agent, cache_ttl: int = 3600):
        self.agent = agent
        self.cache_ttl = cache_ttl
        self.cache = {}

    def run(self, message: str) -> str:
        """캐싱이 포함된 실행"""
        # 캐시 키 생성
        cache_key = hashlib.md5(
            f"{self.agent.name}:{message}".encode()
        ).hexdigest()

        # 캐시 확인
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data["timestamp"] < self.cache_ttl:
                return cached_data["response"]

        # 캐시 미스 - 실제 실행
        runner = Runner(agent=self.agent)
        response = runner.run(message)

        # 캐시 저장
        self.cache[cache_key] = {
            "response": response,
            "timestamp": time.time()
        }

        return response
```

## 7.2. 에러 처리 및 복구

```python
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from google.adk.runners import Runner
from google.adk.agents import Agent

class ResilientRunner:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.logger = logging.getLogger(__name__)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def run_with_retry(self, message: str):
        """재시도 로직이 포함된 실행"""
        try:
            runner = Runner(agent=self.agent)
            return runner.run(message)
        except Exception as e:
            self.logger.error(f"Agent execution failed: {e}")
            raise

    def safe_run(self, message: str, fallback_response: str = "일시적인 오류가 발생했습니다."):
        """안전한 실행 (항상 응답 반환)"""
        try:
            return self.run_with_retry(message)
        except Exception as e:
            self.logger.error(f"All retry attempts failed: {e}")
            return fallback_response
```

## 7.3. 모니터링 및 로깅

```python
from google.adk.events import AgentEvent
from google.adk.runners import Runner
from google.adk.agents import Agent
import json
import time
from datetime import datetime

class MonitoredAgent:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0
        }

    def run_with_monitoring(self, message: str):
        """모니터링이 포함된 실행"""
        start_time = time.time()
        self.metrics["total_requests"] += 1

        try:
            # 에이전트 실행
            runner = Runner(agent=self.agent)
            response = runner.run(message)

            # 성공 메트릭 업데이트
            self.metrics["successful_requests"] += 1
            response_time = time.time() - start_time

            # 평균 응답 시간 업데이트
            self._update_average_response_time(response_time)

            # 로그 기록
            self._log_interaction(message, response, response_time, "success")

            return response

        except Exception as e:
            # 실패 메트릭 업데이트
            self.metrics["failed_requests"] += 1
            response_time = time.time() - start_time

            # 에러 로그
            self._log_interaction(message, str(e), response_time, "error")

            raise

    def _update_average_response_time(self, response_time: float):
        """평균 응답 시간 업데이트"""
        current_avg = self.metrics["average_response_time"]
        successful_count = self.metrics["successful_requests"]

        if successful_count == 1:
            self.metrics["average_response_time"] = response_time
        else:
            self.metrics["average_response_time"] = (
                (current_avg * (successful_count - 1) + response_time) / successful_count
            )

    def _log_interaction(self, message: str, response: str,
                        response_time: float, status: str):
        """상호작용 로깅"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "agent_name": self.agent.name,
            "message": message,
            "response": response,
            "response_time": response_time,
            "status": status,
            "metrics": self.metrics.copy()
        }

        # JSON 로그 출력 (실제 환경에서는 파일이나 로그 시스템에 저장)
        print(json.dumps(log_data, ensure_ascii=False, indent=2))

    def get_metrics(self):
        """메트릭 조회"""
        return self.metrics.copy()
```

---

# 8. 트러블슈팅

## 8.1. 일반적인 문제들

### 문제: Google API 키 관련 오류
```bash
# 해결책: API 키 설정 확인
echo $GOOGLE_API_KEY

# Gemini API 활성화 확인
# Google AI Studio에서 API 키 생성 및 권한 확인
```

### 문제: LiteLLM 모델 호출 실패
```python
# 해결책: 지원되는 모델 형식 확인
from google.adk.models.lite_llm import LiteLlm

# 올바른 형식
model = LiteLlm(model="gemini/gemini-pro")  # ✓
# model = LiteLlm(model="gemini-pro")       # ✗

# 사용 가능한 모델 확인
available_models = [
    "gemini/gemini-pro",
    "gemini/gemini-flash",
    "gemini/gemini-pro-vision",
    "openai/gpt-4o",
    "anthropic/claude-3-sonnet"
]
```

### 문제: 세션 관리 오류
```python
# 해결책: 세션 정리 및 관리
from google.adk.sessions import SessionManager

class ManagedSessionManager:
    def __init__(self, max_sessions: int = 1000):
        self.session_manager = SessionManager()
        self.max_sessions = max_sessions

    def cleanup_old_sessions(self):
        """오래된 세션 정리"""
        # 구현에 따라 세션 정리 로직 추가
        pass

    def get_or_create_session(self, user_id: str):
        """세션 가져오기 또는 생성"""
        return self.session_manager.create_session(user_id=user_id)
```

## 8.2. 디버깅 도구

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
import logging

# 디버깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def debug_agent_execution(agent: Agent, message: str):
    """에이전트 실행 디버깅"""
    print(f"🔍 Debugging Agent: {agent.name}")
    print(f"📝 Input Message: {message}")
    print(f"🤖 Model: {agent.model}")
    print(f"📋 Instructions: {agent.instruction}")

    try:
        runner = Runner(agent=agent)
        response = runner.run(message)

        print(f"✅ Success Response: {response}")
        return response

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"📊 Agent Details: {agent.__dict__}")
        raise

# ADK 웹 UI를 통한 디버깅
def launch_debug_ui(agent: Agent):
    """디버깅용 웹 UI 실행"""
    # 터미널에서 실행: adk web --agent module:agent --debug
    print("Run in terminal: adk web --agent your_module:agent --debug")
```

---

# 9. 추가 리소스

## 9.1. 공식 문서 및 학습 자료
- **공식 문서**: https://google.github.io/adk-docs/
- **GitHub (Python)**: https://github.com/google/adk-python
- **GitHub (Java)**: https://github.com/google/adk-java
- **Google Cloud 가이드**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart

## 9.2. 개발 도구
- **ADK 웹 UI**: 브라우저 기반 개발 및 디버깅 도구
- **Google AI Studio**: Gemini API 키 관리
- **Vertex AI**: 엔터프라이즈 배포 및 관리

## 9.3. 커뮤니티 및 지원
- **Google Developers Blog**: ADK 관련 최신 소식
- **DataCamp Tutorial**: ADK 가이드 및 데모 프로젝트
- **Stack Overflow**: `google-adk` 태그

## 9.4. 통합 가능한 서비스
- **Google Cloud Services**: BigQuery, Cloud Storage, Vertex AI
- **Monitoring**: Google Cloud Monitoring, Prometheus
- **Databases**: Cloud SQL, Firestore
- **LLM Providers**: Gemini, OpenAI, Anthropic, Mistral

---

# 10. 결론

Google Agent Development Kit (ADK)는 **Google의 공식 AI 에이전트 개발 프레임워크**로, 엔터프라이즈급 AI 애플리케이션 구축에 최적화되어 있습니다.

## ✅ Google ADK를 선택해야 하는 경우
- **Google 생태계** 활용 필요
- **Gemini 모델** 최적 활용
- **엔터프라이즈급** 안정성 필요
- **멀티 언어 지원** (Python, Java)

## 🚀 2025년 핵심 특징
- **공식 Google 지원**: 지속적인 업데이트와 기술 지원
- **모델 중립성**: 다양한 LLM 제공자 지원
- **클라우드 네이티브**: Google Cloud와 완벽한 통합
- **개발자 친화적**: 직관적인 API와 웹 UI

## 💼 비즈니스 가치
- **빠른 개발**: 코드 우선 접근법으로 신속한 프로토타이핑
- **확장성**: 단순한 에이전트부터 복잡한 멀티 에이전트 시스템까지
- **신뢰성**: Google의 인프라와 베스트 프랙티스 적용
- **미래 보장성**: Google의 AI 로드맵과 일치하는 발전 방향

Google ADK는 **안정성과 성능을 중시하는 기업 환경**에서 AI 에이전트를 구축하고자 하는 개발자들에게 최적의 선택입니다.