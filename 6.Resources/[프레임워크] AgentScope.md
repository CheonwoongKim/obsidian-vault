---
title: "[프레임워크] AgentScope 완전 가이드 - 알리바바 멀티 에이전트 플랫폼"
type: resource
category: AI/프레임워크
tags: [agentscope, alibaba, 멀티에이전트, 드래그앤드롭, 비동기, 액터모델]
source: "공식 문서 및 실습 기반 작성"
status: active
updated: 2025-09-24
---

## 🔗 관련 가이드

### 대규모 멀티 에이전트 플랫폼
- **[프레임워크] AgentScope 완전 가이드 - 알리바바 멀티 에이전트 플랫폼** ← **현재 가이드**
- **[[프레임워크] Google ADK]]** - 구글 에이전트 개발 플랫폼
- **[[프레임워크] Haystack]]** - 엔터프라이즈 RAG 솔루션

### 멀티 에이전트 프레임워크
- **[[프레임워크] AutoGen]]** - 대화형 에이전트 시스템
- **[[프레임워크] CrewAI]]** - 역할 기반 작업 분담
- **[[프레임워크] Phidata]]** - 다양한 모달을 활용하는 에이전트

### AI 프레임워크 시리즈
- **[[프레임워크] LangChain]]** - 종합 AI 애플리케이션 프레임워크
- **[[프레임워크] LangGraph]]** - 복잡한 워크플로우 설계
- **[[프레임워크] DSPy]]** - 프롬프트 최적화

### 프롬프트 엔지니어링
- **[[프롬프트 엔지니어링 - 마스터 가이드]]** - 전체 프롬프팅 기법 개요
- **[[프롬프트] 04 ReAct 프롬프팅]]** - 추론과 도구 활용 기법

---

# 1. 개요

AgentScope는 **알리바바에서 개발한 오픈소스 멀티 에이전트 플랫폼**으로, **에이전트 지향 프로그래밍(Agent-Oriented Programming)**을 통해 LLM 기반 애플리케이션을 구축할 수 있는 프레임워크입니다.

## 핵심 특징

### 🎯 혁신적 접근법
- **에이전트 지향 프로그래밍**: 새로운 패러다임의 AI 애플리케이션 개발
- **드래그 앤 드롭 UI**: 코딩 없이 멀티 에이전트 시스템 구성
- **절차 지향 메시지 교환**: 직관적이고 이해하기 쉬운 에이전트 통신
- **완전한 투명성**: 모든 프롬프트, API 호출, 메모리, 워크플로우 가시화

### 🔧 기술적 강점
- **비동기 실행**: v1.0에서 완전한 비동기 지원
- **액터 모델**: 자동 병렬 최적화 및 분산 처리
- **모델 중립적**: 다양한 LLM 제공자 지원
- **견고한 아키텍처**: 사용자 정의 장애 허용 및 재시도 메커니즘

---

# 2. 설치 및 환경 설정

## 2.1. 시스템 요구사항

```bash
# Python 3.10 이상 필요
python --version  # Python 3.10+ 확인

# 가상환경 생성 (권장)
python3 -m venv agentscope_env
source agentscope_env/bin/activate  # macOS/Linux
# agentscope_env\Scripts\activate  # Windows
```

## 2.2. 기본 설치

```bash
# PyPI에서 설치
pip install agentscope

# 런타임 프레임워크 (코어 종속성)
pip install agentscope-runtime

# 샌드박스 종속성 포함 (권장)
pip install "agentscope-runtime[sandbox]"

# 개발 버전 설치
git clone -b main https://github.com/agentscope-ai/agentscope.git
cd agentscope
pip install -e .
```

## 2.3. 환경 변수 설정

```bash
# .env 파일 생성
OPENAI_API_KEY=your-openai-api-key
DASHSCOPE_API_KEY=your-alibaba-key  # 알리바바 DashScope
GOOGLE_API_KEY=your-gemini-key      # Google Gemini
ANTHROPIC_API_KEY=your-claude-key   # Anthropic Claude

# 선택적 설정
AGENTSCOPE_CACHE_DIR=./cache
AGENTSCOPE_LOG_LEVEL=INFO
```

## 2.4. 설치 확인

```python
import agentscope
from agentscope.agents import DialogAgent
from agentscope.models import OpenAIWrapperModel

print(f"✅ AgentScope 설치 완료")
print(f"AgentScope version: {agentscope.__version__}")

# 기본 모델 테스트
model = OpenAIWrapperModel(
    model_type="gpt-4o-mini",
    config_name="test_config"
)

print("✅ 모델 래퍼 생성 성공")
```

---

# 3. 기본 사용법

## 3.1. 간단한 에이전트 생성

```python
import agentscope
from agentscope.agents import DialogAgent
from agentscope.models import OpenAIWrapperModel
from agentscope.message import Msg

# 모델 설정
model_config = {
    "config_name": "openai_config",
    "model_type": "openai_chat",
    "model": "gpt-4o-mini",
    "api_key": "your-openai-api-key"
}

# AgentScope 초기화
agentscope.init(
    model_configs=[model_config],
    project="basic_agent_example"
)

# 에이전트 생성
assistant = DialogAgent(
    name="Assistant",
    model_config_name="openai_config",
    sys_prompt="You are a helpful assistant. Answer questions clearly and concisely."
)

# 에이전트와 대화
user_msg = Msg(name="User", content="What is artificial intelligence?", role="user")
response = assistant(user_msg)

print(f"Assistant: {response.content}")
```

## 3.2. 멀티 에이전트 대화

```python
import agentscope
from agentscope.agents import DialogAgent
from agentscope.pipeline import sequential_pipeline
from agentscope.message import Msg

# 모델 설정
model_configs = [
    {
        "config_name": "openai_config",
        "model_type": "openai_chat",
        "model": "gpt-4o-mini",
        "api_key": "your-openai-api-key"
    }
]

# AgentScope 초기화
agentscope.init(
    model_configs=model_configs,
    project="multi_agent_example"
)

# 여러 에이전트 생성
analyst = DialogAgent(
    name="Market_Analyst",
    model_config_name="openai_config",
    sys_prompt="You are a market analyst. Provide data-driven market insights."
)

strategist = DialogAgent(
    name="Business_Strategist",
    model_config_name="openai_config",
    sys_prompt="You are a business strategist. Create actionable business strategies."
)

consultant = DialogAgent(
    name="Consultant",
    model_config_name="openai_config",
    sys_prompt="You are a consultant. Synthesize insights and provide recommendations."
)

# 순차적 파이프라인 실행
def business_analysis_pipeline():
    """비즈니스 분석 파이프라인"""

    # 초기 질문
    initial_question = Msg(
        name="User",
        content="Analyze the market opportunity for AI-powered customer service automation",
        role="user"
    )

    # 시장 분석
    market_analysis = analyst(initial_question)
    print(f"Market Analysis: {market_analysis.content}")

    # 전략 수립
    strategy_input = Msg(
        name="Market_Analyst",
        content=market_analysis.content,
        role="assistant"
    )
    strategy = strategist(strategy_input)
    print(f"Business Strategy: {strategy.content}")

    # 최종 컨설팅
    consulting_input = Msg(
        name="Business_Strategist",
        content=f"Market Analysis: {market_analysis.content}\n\nStrategy: {strategy.content}",
        role="assistant"
    )
    final_recommendation = consultant(consulting_input)
    print(f"Final Recommendation: {final_recommendation.content}")

    return final_recommendation

# 실행
result = business_analysis_pipeline()
```

## 3.3. 비동기 멀티 에이전트 시스템

```python
import asyncio
import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg

async def async_multi_agent_example():
    """비동기 멀티 에이전트 예제"""

    # 모델 설정
    model_configs = [
        {
            "config_name": "openai_config",
            "model_type": "openai_chat",
            "model": "gpt-4o-mini",
            "api_key": "your-openai-api-key"
        }
    ]

    # AgentScope 초기화
    agentscope.init(
        model_configs=model_configs,
        project="async_multi_agent"
    )

    # 에이전트들 생성
    researcher = DialogAgent(
        name="Researcher",
        model_config_name="openai_config",
        sys_prompt="You are a researcher. Conduct thorough research on given topics."
    )

    writer = DialogAgent(
        name="Writer",
        model_config_name="openai_config",
        sys_prompt="You are a content writer. Create engaging articles."
    )

    reviewer = DialogAgent(
        name="Reviewer",
        model_config_name="openai_config",
        sys_prompt="You are an editor. Review and improve content quality."
    )

    # 병렬 작업 정의
    async def research_task():
        msg = Msg(name="User", content="Research latest trends in AI agents", role="user")
        return await researcher(msg)

    async def writing_task():
        msg = Msg(name="User", content="Write an introduction about AI agent frameworks", role="user")
        return await writer(msg)

    async def review_task(content):
        msg = Msg(name="Writer", content=content, role="assistant")
        return await reviewer(msg)

    # 병렬 실행
    research_result, writing_result = await asyncio.gather(
        research_task(),
        writing_task()
    )

    # 순차 검토
    final_review = await review_task(
        f"Research: {research_result.content}\n\nContent: {writing_result.content}"
    )

    return {
        "research": research_result.content,
        "writing": writing_result.content,
        "review": final_review.content
    }

# 실행
result = asyncio.run(async_multi_agent_example())
print("비동기 멀티 에이전트 결과:", result)
```

---

# 4. 고급 활용법

## 4.1. MsgHub를 활용한 복잡한 통신

```python
import agentscope
from agentscope.agents import DialogAgent
from agentscope.pipeline import MsgHub
from agentscope.message import Msg
from agentscope.models import OpenAIWrapperModel

class TeamCollaborationSystem:
    def __init__(self):
        self.setup_agents()
        self.setup_hub()

    def setup_agents(self):
        """팀 에이전트들 설정"""

        # 모델 설정
        model_configs = [
            {
                "config_name": "openai_config",
                "model_type": "openai_chat",
                "model": "gpt-4o",
                "api_key": "your-openai-api-key"
            }
        ]

        agentscope.init(
            model_configs=model_configs,
            project="team_collaboration"
        )

        # 팀 리더
        self.team_leader = DialogAgent(
            name="Team_Leader",
            model_config_name="openai_config",
            sys_prompt="""You are a team leader. Your responsibilities:
            1. Coordinate team activities
            2. Make final decisions
            3. Delegate tasks appropriately
            4. Ensure project success"""
        )

        # 개발자
        self.developer = DialogAgent(
            name="Developer",
            model_config_name="openai_config",
            sys_prompt="""You are a senior developer. Your expertise:
            1. Technical architecture and implementation
            2. Code quality and best practices
            3. Performance optimization
            4. Technical problem solving"""
        )

        # 디자이너
        self.designer = DialogAgent(
            name="Designer",
            model_config_name="openai_config",
            sys_prompt="""You are a UX/UI designer. Your focus:
            1. User experience and interface design
            2. Visual aesthetics and branding
            3. Usability and accessibility
            4. Design system consistency"""
        )

        # 마케터
        self.marketer = DialogAgent(
            name="Marketer",
            model_config_name="openai_config",
            sys_prompt="""You are a marketing specialist. Your areas:
            1. Market research and user insights
            2. Brand positioning and messaging
            3. Campaign strategy and execution
            4. Growth and conversion optimization"""
        )

    def setup_hub(self):
        """메시지 허브 설정"""
        self.hub = MsgHub(
            participants=[
                self.team_leader,
                self.developer,
                self.designer,
                self.marketer
            ],
            announcement_condition=lambda: True
        )

    def collaborate_on_project(self, project_brief: str):
        """프로젝트 협업 시뮬레이션"""

        # 프로젝트 시작 메시지
        initial_msg = Msg(
            name="Project_Manager",
            content=f"New Project Brief: {project_brief}\n\n"
                   f"Team, please provide your perspectives and initial thoughts on this project.",
            role="user"
        )

        # 허브를 통한 메시지 배포
        self.hub.broadcast(initial_msg)

        # 각 팀원의 응답 수집
        responses = {}

        # 개발자 관점
        dev_response = self.developer(initial_msg)
        responses['developer'] = dev_response.content

        # 디자이너 관점
        design_response = self.designer(initial_msg)
        responses['designer'] = design_response.content

        # 마케터 관점
        marketing_response = self.marketer(initial_msg)
        responses['marketer'] = marketing_response.content

        # 팀 리더가 모든 의견을 종합
        synthesis_msg = Msg(
            name="Team",
            content=f"""Team responses to project brief:

            Developer perspective: {responses['developer']}

            Designer perspective: {responses['designer']}

            Marketing perspective: {responses['marketer']}

            As team leader, please synthesize these perspectives and create a comprehensive project plan.""",
            role="assistant"
        )

        final_plan = self.team_leader(synthesis_msg)

        return {
            'project_brief': project_brief,
            'team_responses': responses,
            'final_plan': final_plan.content
        }

# 사용 예제
team_system = TeamCollaborationSystem()

project_result = team_system.collaborate_on_project(
    "개발 목표: AI 기반 개인화 학습 플랫폼 구축\n"
    "- 타겟: 대학생 및 직장인\n"
    "- 핵심 기능: 개인맞춤 학습경로, 진도추적, AI 튜터\n"
    "- 런칭 목표: 3개월 내"
)

print("=== 프로젝트 협업 결과 ===")
print(f"프로젝트 개요: {project_result['project_brief']}")
print(f"\n개발자 의견: {project_result['team_responses']['developer']}")
print(f"\n디자이너 의견: {project_result['team_responses']['designer']}")
print(f"\n마케터 의견: {project_result['team_responses']['marketer']}")
print(f"\n팀 리더 최종 계획: {project_result['final_plan']}")
```

## 4.2. 내장 도구 활용

```python
import agentscope
from agentscope.agents import DialogAgent
from agentscope.tools import execute_python_code, execute_shell_command, write_text_file
from agentscope.message import Msg

class DataAnalysisAgent:
    def __init__(self):
        self.setup_agent()

    def setup_agent(self):
        """데이터 분석 에이전트 설정"""

        model_configs = [
            {
                "config_name": "openai_config",
                "model_type": "openai_chat",
                "model": "gpt-4o",
                "api_key": "your-openai-api-key"
            }
        ]

        agentscope.init(
            model_configs=model_configs,
            project="data_analysis"
        )

        # 도구가 있는 에이전트
        self.analyst = DialogAgent(
            name="Data_Analyst",
            model_config_name="openai_config",
            sys_prompt="""You are a data analyst with access to programming tools.
            You can execute Python code, shell commands, and write files.

            Available tools:
            - execute_python_code: Run Python code for data analysis
            - execute_shell_command: Run system commands
            - write_text_file: Save results to files

            Always explain your analysis process and interpret results."""
        )

        # 도구 등록
        self.tools = {
            'python': execute_python_code,
            'shell': execute_shell_command,
            'write_file': write_text_file
        }

    def analyze_data(self, data_description: str, analysis_task: str):
        """데이터 분석 수행"""

        # 분석 요청 메시지
        analysis_msg = Msg(
            name="User",
            content=f"""Data Description: {data_description}

            Analysis Task: {analysis_task}

            Please perform the analysis using Python code. Include:
            1. Data exploration and visualization
            2. Statistical analysis
            3. Key insights and findings
            4. Recommendations based on results""",
            role="user"
        )

        # 분석 실행
        response = self.analyst(analysis_msg)

        # Python 코드 실행 (예시)
        analysis_code = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 샘플 데이터 생성 (실제로는 제공된 데이터 사용)
np.random.seed(42)
data = {
    'month': range(1, 13),
    'sales': np.random.normal(100000, 20000, 12),
    'marketing_spend': np.random.normal(10000, 2000, 12),
    'customer_satisfaction': np.random.uniform(3.5, 5.0, 12)
}

df = pd.DataFrame(data)
df['sales'] = df['sales'].clip(lower=50000)  # 최소값 설정

# 기본 통계
print("=== 기본 통계 ===")
print(df.describe())

# 상관관계 분석
print("\\n=== 상관관계 ===")
correlation_matrix = df.corr()
print(correlation_matrix)

# 시각화
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(df['month'], df['sales'], marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')

plt.subplot(1, 3, 2)
plt.scatter(df['marketing_spend'], df['sales'])
plt.title('Marketing Spend vs Sales')
plt.xlabel('Marketing Spend')
plt.ylabel('Sales')

plt.subplot(1, 3, 3)
plt.scatter(df['customer_satisfaction'], df['sales'])
plt.title('Customer Satisfaction vs Sales')
plt.xlabel('Customer Satisfaction')
plt.ylabel('Sales')

plt.tight_layout()
plt.savefig('analysis_results.png', dpi=150, bbox_inches='tight')
plt.show()

# 주요 인사이트
total_sales = df['sales'].sum()
avg_satisfaction = df['customer_satisfaction'].mean()
sales_marketing_corr = df['sales'].corr(df['marketing_spend'])

print(f"\\n=== 주요 인사이트 ===")
print(f"연간 총 매출: ${total_sales:,.0f}")
print(f"평균 고객 만족도: {avg_satisfaction:.2f}/5.0")
print(f"매출-마케팅비용 상관계수: {sales_marketing_corr:.3f}")
"""

        # 코드 실행
        code_result = execute_python_code(analysis_code)

        # 결과 파일 저장
        report_content = f"""
데이터 분석 보고서
==================

분석 요청: {analysis_task}
데이터 설명: {data_description}

AI 분석 결과:
{response.content}

Python 분석 결과:
{code_result}

생성일시: {pd.Timestamp.now()}
"""

        write_text_file("analysis_report.txt", report_content)

        return {
            'ai_analysis': response.content,
            'code_result': code_result,
            'report_saved': True
        }

# 사용 예제
data_analyst = DataAnalysisAgent()

analysis_result = data_analyst.analyze_data(
    data_description="월별 판매 데이터, 마케팅 지출, 고객 만족도 데이터 (12개월)",
    analysis_task="판매 성과 분석 및 마케팅 ROI 평가, 개선 방안 제시"
)

print("=== 분석 결과 ===")
print(analysis_result['ai_analysis'])
print("\n=== 코드 실행 결과 ===")
print(analysis_result['code_result'])
```

---

# 5. 실제 프로젝트 예제

## 5.1. 스마트 고객 서비스 시스템

```python
import agentscope
from agentscope.agents import DialogAgent
from agentscope.pipeline import MsgHub, WhileLoopPipeline
from agentscope.message import Msg
from agentscope.tools import execute_python_code
import json
from datetime import datetime
from typing import Dict, List

class SmartCustomerServiceSystem:
    def __init__(self):
        self.setup_system()
        self.ticket_database = {}
        self.knowledge_base = self.load_knowledge_base()

    def setup_system(self):
        """고객 서비스 시스템 설정"""

        model_configs = [
            {
                "config_name": "openai_config",
                "model_type": "openai_chat",
                "model": "gpt-4o",
                "api_key": "your-openai-api-key"
            }
        ]

        agentscope.init(
            model_configs=model_configs,
            project="smart_customer_service"
        )

        # 1차 접수 에이전트
        self.intake_agent = DialogAgent(
            name="Intake_Specialist",
            model_config_name="openai_config",
            sys_prompt="""당신은 고객 서비스 접수 전문가입니다.

            주요 역할:
            1. 고객을 따뜻하게 맞이하고 문제를 파악
            2. 문의 유형을 분류 (기술지원, 결제, 일반문의, 불만)
            3. 필요한 정보를 수집
            4. 적절한 전문가에게 라우팅 결정
            5. 고객 감정 상태를 파악하고 적절히 응대

            항상 친근하고 전문적으로 응답하세요."""
        )

        # 기술 지원 에이전트
        self.tech_support = DialogAgent(
            name="Tech_Support",
            model_config_name="openai_config",
            sys_prompt="""당신은 기술 지원 전문가입니다.

            전문 분야:
            1. 소프트웨어 문제 해결
            2. 단계별 가이드 제공
            3. 시스템 오류 진단
            4. 성능 최적화 조언

            복잡한 기술 내용을 쉽게 설명하고 실용적인 해결책을 제공하세요."""
        )

        # 결제 지원 에이전트
        self.billing_support = DialogAgent(
            name="Billing_Support",
            model_config_name="openai_config",
            sys_prompt="""당신은 결제 및 계정 전문가입니다.

            담당 업무:
            1. 결제 문제 해결
            2. 계정 정보 관리
            3. 환불 및 취소 처리
            4. 요금제 및 서비스 안내

            정확한 정보를 제공하고 고객의 금전적 우려를 해결하세요."""
        )

        # 에스컬레이션 매니저
        self.escalation_manager = DialogAgent(
            name="Escalation_Manager",
            model_config_name="openai_config",
            sys_prompt="""당신은 고급 문제 해결 매니저입니다.

            책임 영역:
            1. 복잡한 문제 해결
            2. 고객 불만 처리
            3. 정책 예외 결정
            4. 보상 및 해결책 제안

            고객 만족을 최우선으로 하되 회사 이익도 고려하여 균형잡힌 결정을 내리세요."""
        )

        # 품질 보증 에이전트
        self.qa_agent = DialogAgent(
            name="Quality_Assurance",
            model_config_name="openai_config",
            sys_prompt="""당신은 품질 보증 전문가입니다.

            역할:
            1. 서비스 품질 모니터링
            2. 고객 만족도 평가
            3. 프로세스 개선 제안
            4. 팀 성과 분석

            객관적이고 건설적인 피드백을 제공하세요."""
        )

    def load_knowledge_base(self) -> Dict:
        """지식 베이스 로드 (실제로는 데이터베이스에서 로드)"""
        return {
            "faq": [
                {"q": "비밀번호를 잊어버렸어요", "a": "로그인 페이지에서 '비밀번호 찾기'를 클릭하세요."},
                {"q": "환불 요청 방법", "a": "설정 > 구독 관리 > 환불 요청에서 신청 가능합니다."},
                {"q": "앱이 작동하지 않아요", "a": "앱을 완전히 종료 후 재실행하거나 업데이트를 확인하세요."}
            ],
            "policies": {
                "refund_policy": "구매 후 7일 내 100% 환불, 14일 내 50% 환불",
                "support_hours": "평일 09:00-18:00, 주말 10:00-16:00"
            }
        }

    def create_ticket(self, customer_info: Dict, inquiry: str) -> str:
        """고객 티켓 생성"""
        ticket_id = f"CS-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        ticket = {
            "ticket_id": ticket_id,
            "customer_info": customer_info,
            "inquiry": inquiry,
            "status": "open",
            "priority": "normal",
            "created_at": datetime.now().isoformat(),
            "interactions": [],
            "resolution": None,
            "satisfaction_score": None
        }

        self.ticket_database[ticket_id] = ticket
        return ticket_id

    def process_customer_inquiry(self, customer_info: Dict, inquiry: str):
        """고객 문의 처리 메인 플로우"""

        # 티켓 생성
        ticket_id = self.create_ticket(customer_info, inquiry)

        print(f"🎫 티켓 생성: {ticket_id}")
        print(f"👤 고객 정보: {customer_info['name']} ({customer_info['email']})")
        print(f"📝 문의 내용: {inquiry}")

        # 1단계: 접수 처리
        intake_msg = Msg(
            name="Customer",
            content=f"""고객 정보:
            - 이름: {customer_info['name']}
            - 이메일: {customer_info['email']}
            - 회원 등급: {customer_info.get('tier', 'Standard')}

            문의 내용: {inquiry}""",
            role="user"
        )

        intake_response = self.intake_agent(intake_msg)

        # 상호작용 기록
        self.ticket_database[ticket_id]["interactions"].append({
            "agent": "Intake_Specialist",
            "timestamp": datetime.now().isoformat(),
            "response": intake_response.content
        })

        print(f"\n📞 접수 전문가: {intake_response.content}")

        # 2단계: 문의 유형 분류 및 라우팅
        inquiry_type = self.classify_inquiry(inquiry)
        print(f"\n🏷️ 문의 분류: {inquiry_type}")

        # 전문가에게 라우팅
        if inquiry_type == "technical":
            specialist = self.tech_support
            specialist_name = "기술 지원팀"
        elif inquiry_type == "billing":
            specialist = self.billing_support
            specialist_name = "결제 지원팀"
        elif inquiry_type == "escalation":
            specialist = self.escalation_manager
            specialist_name = "매니저"
        else:
            specialist = self.intake_agent
            specialist_name = "일반 상담팀"

        # 전문가 응답
        specialist_msg = Msg(
            name="Intake_Specialist",
            content=f"""접수 내용: {intake_response.content}

            고객 원본 문의: {inquiry}

            전문적인 해결책을 제공해주세요.""",
            role="assistant"
        )

        specialist_response = specialist(specialist_msg)

        # 상호작용 기록
        self.ticket_database[ticket_id]["interactions"].append({
            "agent": specialist_name,
            "timestamp": datetime.now().isoformat(),
            "response": specialist_response.content
        })

        print(f"\n👨‍💼 {specialist_name}: {specialist_response.content}")

        # 3단계: 품질 보증 검토
        qa_msg = Msg(
            name="Service_Team",
            content=f"""서비스 품질 검토 요청:

            고객 문의: {inquiry}
            접수팀 응답: {intake_response.content}
            {specialist_name} 응답: {specialist_response.content}

            서비스 품질을 평가하고 개선점을 제안해주세요.""",
            role="assistant"
        )

        qa_review = self.qa_agent(qa_msg)

        # 최종 티켓 업데이트
        self.ticket_database[ticket_id].update({
            "status": "resolved",
            "resolution": specialist_response.content,
            "qa_review": qa_review.content,
            "resolved_at": datetime.now().isoformat()
        })

        print(f"\n🔍 품질 보증 검토: {qa_review.content}")

        # 결과 반환
        return {
            "ticket_id": ticket_id,
            "inquiry_type": inquiry_type,
            "routed_to": specialist_name,
            "intake_response": intake_response.content,
            "specialist_response": specialist_response.content,
            "qa_review": qa_review.content,
            "status": "resolved"
        }

    def classify_inquiry(self, inquiry: str) -> str:
        """문의 유형 자동 분류"""
        inquiry_lower = inquiry.lower()

        # 기술 문의
        tech_keywords = ["오류", "버그", "작동하지", "설치", "업데이트", "느려", "충돌"]
        if any(keyword in inquiry_lower for keyword in tech_keywords):
            return "technical"

        # 결제 문의
        billing_keywords = ["결제", "환불", "요금", "구독", "카드", "결제실패", "청구"]
        if any(keyword in inquiry_lower for keyword in billing_keywords):
            return "billing"

        # 불만 및 에스컬레이션
        escalation_keywords = ["불만", "화나", "최악", "소송", "해지", "매니저"]
        if any(keyword in inquiry_lower for keyword in escalation_keywords):
            return "escalation"

        return "general"

    def get_service_analytics(self):
        """서비스 분석 대시보드"""
        if not self.ticket_database:
            return "티켓 데이터가 없습니다."

        total_tickets = len(self.ticket_database)
        resolved_tickets = sum(1 for t in self.ticket_database.values() if t["status"] == "resolved")

        # 문의 유형별 통계
        inquiry_types = {}
        for ticket in self.ticket_database.values():
            inquiry_type = self.classify_inquiry(ticket["inquiry"])
            inquiry_types[inquiry_type] = inquiry_types.get(inquiry_type, 0) + 1

        analytics = f"""
📊 고객 서비스 분석 대시보드
================================

📈 전체 통계:
- 총 티켓 수: {total_tickets}
- 해결된 티켓: {resolved_tickets}
- 해결률: {(resolved_tickets/total_tickets*100):.1f}%

📋 문의 유형별 분포:"""

        for inquiry_type, count in inquiry_types.items():
            percentage = (count / total_tickets * 100)
            analytics += f"\n- {inquiry_type}: {count}건 ({percentage:.1f}%)"

        return analytics

# 사용 예제 및 시연
def demonstrate_customer_service():
    """고객 서비스 시스템 시연"""

    cs_system = SmartCustomerServiceSystem()

    # 다양한 고객 문의 시뮬레이션
    test_cases = [
        {
            "customer_info": {
                "name": "김철수",
                "email": "kim@example.com",
                "tier": "Premium"
            },
            "inquiry": "앱이 계속 오류가 나면서 사용할 수 없어요. 로그인도 안 되고 데이터도 사라진 것 같습니다."
        },
        {
            "customer_info": {
                "name": "이영희",
                "email": "lee@example.com",
                "tier": "Standard"
            },
            "inquiry": "이번 달 결제가 두 번 되었는데 환불 받을 수 있나요? 카드 명세서를 확인해보니 중복 결제된 것 같습니다."
        },
        {
            "customer_info": {
                "name": "박민수",
                "email": "park@example.com",
                "tier": "Basic"
            },
            "inquiry": "서비스가 너무 불친절하고 문제가 많아요. 매니저와 통화하고 싶습니다. 구독 해지도 고려 중입니다."
        }
    ]

    print("🎭 스마트 고객 서비스 시스템 시연")
    print("="*50)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎪 시연 #{i}")
        print("-" * 30)

        result = cs_system.process_customer_inquiry(
            test_case["customer_info"],
            test_case["inquiry"]
        )

        print(f"\n✅ 처리 완료 - 티켓 ID: {result['ticket_id']}")
        print(f"🏷️ 분류: {result['inquiry_type']}")
        print(f"👥 담당: {result['routed_to']}")

        if i < len(test_cases):
            print("\n" + "="*50)

    # 분석 대시보드 출력
    print("\n" + cs_system.get_service_analytics())

# 시연 실행
if __name__ == "__main__":
    demonstrate_customer_service()
```

## 5.2. 창작 콘텐츠 제작 스튜디오

```python
import agentscope
from agentscope.agents import DialogAgent
from agentscope.pipeline import sequential_pipeline
from agentscope.message import Msg
from agentscope.tools import write_text_file
import json
from datetime import datetime

class CreativeContentStudio:
    def __init__(self):
        self.setup_creative_team()

    def setup_creative_team(self):
        """창작팀 에이전트들 설정"""

        model_configs = [
            {
                "config_name": "creative_config",
                "model_type": "openai_chat",
                "model": "gpt-4o",
                "api_key": "your-openai-api-key"
            }
        ]

        agentscope.init(
            model_configs=model_configs,
            project="creative_content_studio"
        )

        # 아이디어 기획자
        self.ideator = DialogAgent(
            name="Creative_Ideator",
            model_config_name="creative_config",
            sys_prompt="""당신은 창의적 아이디어 기획자입니다.

            전문 분야:
            1. 트렌드 분석 및 인사이트 도출
            2. 독창적이고 매력적인 아이디어 발굴
            3. 타겟 오디언스 분석
            4. 콘텐츠 컨셉 개발

            항상 참신하고 실현 가능한 아이디어를 제안하세요."""
        )

        # 스토리텔러
        self.storyteller = DialogAgent(
            name="Master_Storyteller",
            model_config_name="creative_config",
            sys_prompt="""당신은 마스터 스토리텔러입니다.

            핵심 능력:
            1. 감동적이고 몰입도 높은 스토리 구성
            2. 캐릭터 개발 및 서사 구조 설계
            3. 다양한 장르와 톤앤매너 구사
            4. 독자 감정 몰입 유도

            인간의 마음을 움직이는 스토리를 만드세요."""
        )

        # 카피라이터
        self.copywriter = DialogAgent(
            name="Expert_Copywriter",
            model_config_name="creative_config",
            sys_prompt="""당신은 전문 카피라이터입니다.

            전문성:
            1. 브랜드 메시지 전달
            2. 설득력 있는 카피 작성
            3. 타겟별 톤앤매너 최적화
            4. 액션 유도 및 전환 최적화

            기억에 남고 행동을 이끄는 카피를 작성하세요."""
        )

        # 비주얼 기획자
        self.visual_planner = DialogAgent(
            name="Visual_Planner",
            model_config_name="creative_config",
            sys_prompt="""당신은 비주얼 기획 전문가입니다.

            전문 영역:
            1. 시각적 콘셉트 개발
            2. 색상, 레이아웃, 타이포그래피 기획
            3. 브랜드 아이덴티티 구현
            4. 멀티미디어 콘텐츠 설계

            시각적으로 임팩트있는 콘텐츠를 기획하세요."""
        )

        # 마케팅 전략가
        self.marketing_strategist = DialogAgent(
            name="Marketing_Strategist",
            model_config_name="creative_config",
            sys_prompt="""당신은 마케팅 전략 전문가입니다.

            핵심 역량:
            1. 시장 분석 및 경쟁사 벤치마킹
            2. 타겟 세분화 및 페르소나 설정
            3. 채널별 최적 전략 수립
            4. 성과 측정 지표 설계

            효과적인 마케팅 전략을 제시하세요."""
        )

        # 품질 관리자
        self.quality_controller = DialogAgent(
            name="Quality_Controller",
            model_config_name="creative_config",
            sys_prompt="""당신은 콘텐츠 품질 관리 전문가입니다.

            검토 항목:
            1. 콘텐츠 일관성 및 품질 평가
            2. 브랜드 가이드라인 준수 확인
            3. 법적/윤리적 이슈 검토
            4. 최종 개선안 제시

            객관적이고 건설적인 피드백을 제공하세요."""
        )

    def create_campaign(self, brief: Dict):
        """캠페인 제작 워크플로우"""

        print(f"🎬 캠페인 제작 시작: {brief['campaign_name']}")
        print(f"🎯 목적: {brief['objective']}")
        print(f"👥 타겟: {brief['target_audience']}")
        print(f"📅 기간: {brief.get('duration', '미정')}")

        # 1단계: 아이디어 기획
        print(f"\n{'='*50}")
        print("1단계: 아이디어 기획")
        print("="*50)

        ideation_msg = Msg(
            name="Client",
            content=f"""캠페인 브리프:

            캠페인명: {brief['campaign_name']}
            목적: {brief['objective']}
            타겟 오디언스: {brief['target_audience']}
            예산: {brief.get('budget', '협의')}
            채널: {brief.get('channels', '멀티채널')}
            핵심 메시지: {brief.get('key_message', '미정')}

            창의적이고 실현 가능한 캠페인 아이디어를 제안해주세요.""",
            role="user"
        )

        creative_concept = self.ideator(ideation_msg)
        print(f"💡 기획 아이디어:\n{creative_concept.content}")

        # 2단계: 스토리텔링
        print(f"\n{'='*50}")
        print("2단계: 스토리텔링")
        print("="*50)

        story_msg = Msg(
            name="Creative_Ideator",
            content=f"창의적 컨셉: {creative_concept.content}\n\n"
                   f"이 컨셉을 바탕으로 {brief['target_audience']}에게 감동을 주는 "
                   f"스토리를 개발해주세요. 브랜드 메시지 '{brief.get('key_message', '')}'를 "
                   f"자연스럽게 녹여내세요.",
            role="assistant"
        )

        story_concept = self.storyteller(story_msg)
        print(f"📖 스토리 컨셉:\n{story_concept.content}")

        # 3단계: 카피 작성
        print(f"\n{'='*50}")
        print("3단계: 카피 작성")
        print("="*50)

        copy_msg = Msg(
            name="Master_Storyteller",
            content=f"스토리 컨셉: {story_concept.content}\n\n"
                   f"이 스토리를 바탕으로 {brief['target_audience']}를 위한 "
                   f"매력적인 카피를 작성해주세요. 다음 요소를 포함하세요:\n"
                   f"- 메인 헤드라인\n"
                   f"- 서브 헤드라인\n"
                   f"- 본문 카피\n"
                   f"- CTA (Call to Action)",
            role="assistant"
        )

        copy_content = self.copywriter(copy_msg)
        print(f"✍️ 카피 콘텐츠:\n{copy_content.content}")

        # 4단계: 비주얼 기획
        print(f"\n{'='*50}")
        print("4단계: 비주얼 기획")
        print("="*50)

        visual_msg = Msg(
            name="Expert_Copywriter",
            content=f"카피 콘텐츠: {copy_content.content}\n\n"
                   f"스토리: {story_concept.content}\n\n"
                   f"이 콘텐츠를 뒷받침하는 비주얼 콘셉트를 기획해주세요:\n"
                   f"- 전체적인 비주얼 톤앤매너\n"
                   f"- 색상 팔레트 제안\n"
                   f"- 레이아웃 구성안\n"
                   f"- 핵심 비주얼 요소\n"
                   f"- 채널별 비주얼 적용 방안",
            role="assistant"
        )

        visual_concept = self.visual_planner(visual_msg)
        print(f"🎨 비주얼 기획:\n{visual_concept.content}")

        # 5단계: 마케팅 전략
        print(f"\n{'='*50}")
        print("5단계: 마케팅 전략")
        print("="*50)

        marketing_msg = Msg(
            name="Visual_Planner",
            content=f"""캠페인 요소 통합:

            창의 컨셉: {creative_concept.content}

            스토리: {story_concept.content}

            카피: {copy_content.content}

            비주얼: {visual_concept.content}

            이를 바탕으로 효과적인 마케팅 전략을 수립해주세요:
            - 타겟 세분화 전략
            - 채널별 실행 계획
            - 론칭 일정 및 단계
            - 성과 측정 KPI
            - 예산 배분 제안""",
            role="assistant"
        )

        marketing_strategy = self.marketing_strategist(marketing_msg)
        print(f"📈 마케팅 전략:\n{marketing_strategy.content}")

        # 6단계: 품질 관리
        print(f"\n{'='*50}")
        print("6단계: 품질 관리")
        print("="*50)

        qc_msg = Msg(
            name="Marketing_Strategist",
            content=f"""캠페인 전체 검토:

            [원본 브리프]
            {json.dumps(brief, ensure_ascii=False, indent=2)}

            [제작 결과물]
            아이디어: {creative_concept.content}

            스토리: {story_concept.content}

            카피: {copy_content.content}

            비주얼: {visual_concept.content}

            마케팅 전략: {marketing_strategy.content}

            전체 캠페인의 품질, 일관성, 실현 가능성을 검토하고
            개선점을 제안해주세요.""",
            role="assistant"
        )

        quality_review = self.quality_controller(qc_msg)
        print(f"🔍 품질 검토:\n{quality_review.content}")

        # 최종 결과물 구성
        campaign_package = {
            "campaign_info": brief,
            "creative_concept": creative_concept.content,
            "story_concept": story_concept.content,
            "copy_content": copy_content.content,
            "visual_concept": visual_concept.content,
            "marketing_strategy": marketing_strategy.content,
            "quality_review": quality_review.content,
            "created_at": datetime.now().isoformat()
        }

        # 결과물 파일 저장
        filename = f"campaign_{brief['campaign_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
        write_text_file(filename, json.dumps(campaign_package, ensure_ascii=False, indent=2))

        print(f"\n🎉 캠페인 제작 완료!")
        print(f"📁 결과물 저장: {filename}")

        return campaign_package

# 사용 예제
def demo_creative_studio():
    """창작 스튜디오 데모"""

    studio = CreativeContentStudio()

    # 캠페인 브리프 예제
    campaign_brief = {
        "campaign_name": "지속 가능한 미래 프로젝트",
        "objective": "환경 보호에 대한 인식 제고 및 친환경 제품 구매 유도",
        "target_audience": "20-40대 환경 의식이 있는 도시 거주자",
        "budget": "5억원",
        "duration": "3개월",
        "channels": ["소셜미디어", "OOH", "디지털 광고", "이벤트"],
        "key_message": "작은 선택이 만드는 큰 변화"
    }

    print("🎭 창작 콘텐츠 스튜디오 데모")
    print("="*60)

    # 캠페인 제작 실행
    result = studio.create_campaign(campaign_brief)

    print("\n🏆 제작 완료 요약")
    print("="*30)
    print(f"캠페인명: {result['campaign_info']['campaign_name']}")
    print(f"제작일: {result['created_at']}")
    print("모든 단계 완료: ✅")

# 데모 실행
if __name__ == "__main__":
    demo_creative_studio()
```

---

# 6. 프로덕션 배포

## 6.1. AgentScope Studio 웹 인터페이스

```bash
# AgentScope Studio 설치 및 실행
pip install agentscope-runtime

# 스튜디오 서버 실행
agentscope-studio --port 8080

# 백그라운드 실행
nohup agentscope-studio --port 8080 --host 0.0.0.0 > studio.log 2>&1 &
```

## 6.2. FastAPI 서버 통합

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
import uvicorn
import asyncio
from typing import Dict, List, Optional

app = FastAPI(title="AgentScope API Server", version="1.0.0")

# 글로벌 변수
agents_registry = {}
active_sessions = {}

class AgentRequest(BaseModel):
    agent_name: str
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict] = None

class AgentResponse(BaseModel):
    response: str
    agent_name: str
    session_id: str
    timestamp: str

class AgentConfig(BaseModel):
    name: str
    model_config_name: str
    sys_prompt: str
    description: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """서버 시작시 초기화"""

    # 모델 설정
    model_configs = [
        {
            "config_name": "default_openai",
            "model_type": "openai_chat",
            "model": "gpt-4o-mini",
            "api_key": "your-openai-api-key"
        }
    ]

    # AgentScope 초기화
    agentscope.init(
        model_configs=model_configs,
        project="agentscope_api_server"
    )

    # 기본 에이전트들 생성
    default_agents = [
        {
            "name": "assistant",
            "model_config_name": "default_openai",
            "sys_prompt": "You are a helpful assistant.",
            "description": "General purpose assistant"
        },
        {
            "name": "analyst",
            "model_config_name": "default_openai",
            "sys_prompt": "You are a data analyst. Provide insights based on data.",
            "description": "Data analysis specialist"
        },
        {
            "name": "writer",
            "model_config_name": "default_openai",
            "sys_prompt": "You are a professional writer. Create engaging content.",
            "description": "Content writing specialist"
        }
    ]

    # 에이전트 등록
    for agent_config in default_agents:
        agent = DialogAgent(
            name=agent_config["name"],
            model_config_name=agent_config["model_config_name"],
            sys_prompt=agent_config["sys_prompt"]
        )
        agents_registry[agent_config["name"]] = agent

    print(f"✅ AgentScope API 서버 시작 - {len(agents_registry)}개 에이전트 로드됨")

@app.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """에이전트와 채팅"""

    try:
        # 에이전트 확인
        if request.agent_name not in agents_registry:
            raise HTTPException(status_code=404, detail=f"Agent '{request.agent_name}' not found")

        agent = agents_registry[request.agent_name]

        # 메시지 생성
        msg = Msg(
            name="User",
            content=request.message,
            role="user"
        )

        # 에이전트 실행
        response = agent(msg)

        # 세션 관리
        session_id = request.session_id or f"session_{len(active_sessions)}"
        if session_id not in active_sessions:
            active_sessions[session_id] = []

        # 대화 이력 저장
        active_sessions[session_id].append({
            "user_message": request.message,
            "agent_response": response.content,
            "agent_name": request.agent_name,
            "timestamp": response.timestamp if hasattr(response, 'timestamp') else str(datetime.now())
        })

        return AgentResponse(
            response=response.content,
            agent_name=request.agent_name,
            session_id=session_id,
            timestamp=str(datetime.now())
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-agent")
async def create_agent(config: AgentConfig):
    """동적 에이전트 생성"""

    try:
        if config.name in agents_registry:
            raise HTTPException(status_code=400, detail=f"Agent '{config.name}' already exists")

        # 새 에이전트 생성
        agent = DialogAgent(
            name=config.name,
            model_config_name=config.model_config_name,
            sys_prompt=config.sys_prompt
        )

        agents_registry[config.name] = agent

        return {
            "message": f"Agent '{config.name}' created successfully",
            "agent_count": len(agents_registry)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """등록된 에이전트 목록"""
    return {
        "agents": list(agents_registry.keys()),
        "total_count": len(agents_registry)
    }

@app.get("/sessions/{session_id}")
async def get_session_history(session_id: str):
    """세션 대화 이력 조회"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "conversation_count": len(active_sessions[session_id]),
        "history": active_sessions[session_id]
    }

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """세션 삭제"""
    if session_id in active_sessions:
        del active_sessions[session_id]
        return {"message": f"Session '{session_id}' deleted"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "agent_count": len(agents_registry),
        "active_sessions": len(active_sessions),
        "framework": "AgentScope"
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
```

## 6.3. Docker 컨테이너 배포

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# AgentScope 설치
RUN pip install agentscope agentscope-runtime

# 애플리케이션 코드 복사
COPY . .

# 환경 변수
ENV PYTHONPATH=/app
ENV AGENTSCOPE_CACHE_DIR=/app/cache
ENV PORT=8000

# 디렉토리 생성
RUN mkdir -p /app/logs /app/cache /app/data

# 포트 노출
EXPOSE 8000 8080

# 헬스체크
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 시작 스크립트
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
```

```bash
# start.sh
#!/bin/bash

echo "🚀 AgentScope 서버 시작 중..."

# 환경 변수 확인
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️ WARNING: OPENAI_API_KEY not set"
fi

# 캐시 디렉토리 권한 설정
chmod -R 755 /app/cache

# 백그라운드에서 AgentScope Studio 실행
echo "🎨 AgentScope Studio 시작 (포트 8080)..."
agentscope-studio --port 8080 --host 0.0.0.0 > /app/logs/studio.log 2>&1 &

# API 서버 실행
echo "🔧 API 서버 시작 (포트 8000)..."
python main.py
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  agentscope-api:
    build: .
    ports:
      - "8000:8000"  # API 서버
      - "8080:8080"  # AgentScope Studio
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - AGENTSCOPE_CACHE_DIR=/app/cache
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./cache:/app/cache
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
      - POSTGRES_DB=agentscope
      - POSTGRES_USER=agentscope
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - agentscope-api
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
```

## 6.4. 클라우드 배포 (AWS/GCP/Azure)

```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentscope-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentscope
  template:
    metadata:
      labels:
        app: agentscope
    spec:
      containers:
      - name: agentscope
        image: your-registry/agentscope:latest
        ports:
        - containerPort: 8000
        - containerPort: 8080
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-key
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: agentscope-service
spec:
  selector:
    app: agentscope
  ports:
  - name: api
    port: 8000
    targetPort: 8000
  - name: studio
    port: 8080
    targetPort: 8080
  type: LoadBalancer
```

---

# 7. 모범 사례 및 최적화

## 7.1. 성능 최적화

### 7.1.1. 비동기 처리 최적화

```python
import asyncio
import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
from concurrent.futures import ThreadPoolExecutor
import time

class OptimizedAgentPool:
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.agents = {}
        self.setup_agents()

    def setup_agents(self):
        """최적화된 에이전트 풀 설정"""

        model_configs = [
            {
                "config_name": "fast_model",
                "model_type": "openai_chat",
                "model": "gpt-4o-mini",  # 빠른 모델
                "api_key": "your-openai-api-key"
            },
            {
                "config_name": "smart_model",
                "model_type": "openai_chat",
                "model": "gpt-4o",  # 성능 중시 모델
                "api_key": "your-openai-api-key"
            }
        ]

        agentscope.init(
            model_configs=model_configs,
            project="optimized_agent_pool"
        )

        # 빠른 응답용 에이전트들
        for i in range(5):
            agent = DialogAgent(
                name=f"fast_agent_{i}",
                model_config_name="fast_model",
                sys_prompt="Provide quick, concise responses."
            )
            self.agents[f"fast_agent_{i}"] = agent

        # 복잡한 작업용 에이전트들
        for i in range(3):
            agent = DialogAgent(
                name=f"smart_agent_{i}",
                model_config_name="smart_model",
                sys_prompt="Provide detailed, thoughtful responses."
            )
            self.agents[f"smart_agent_{i}"] = agent

    async def process_batch_requests(self, requests: List[Dict]):
        """배치 요청 비동기 처리"""

        async def process_single_request(request):
            """단일 요청 처리"""
            agent_type = request.get("agent_type", "fast")

            # 적절한 에이전트 선택
            if agent_type == "fast":
                available_agents = [k for k in self.agents.keys() if k.startswith("fast_")]
            else:
                available_agents = [k for k in self.agents.keys() if k.startswith("smart_")]

            # 라운드 로빈 방식으로 에이전트 선택
            agent_name = available_agents[request["request_id"] % len(available_agents)]
            agent = self.agents[agent_name]

            # 메시지 처리
            msg = Msg(
                name="User",
                content=request["message"],
                role="user"
            )

            start_time = time.time()
            response = agent(msg)
            processing_time = time.time() - start_time

            return {
                "request_id": request["request_id"],
                "agent_used": agent_name,
                "response": response.content,
                "processing_time": processing_time
            }

        # 모든 요청을 병렬 처리
        tasks = [process_single_request(req) for req in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return results

    async def smart_routing(self, requests: List[Dict]):
        """지능형 라우팅 - 요청 복잡도에 따라 에이전트 선택"""

        def analyze_complexity(message: str) -> str:
            """메시지 복잡도 분석"""

            # 간단한 휴리스틱 - 실제로는 더 정교한 분석 필요
            if len(message.split()) > 50:
                return "smart"
            elif any(keyword in message.lower() for keyword in
                    ["analyze", "complex", "detailed", "explain", "research"]):
                return "smart"
            else:
                return "fast"

        # 요청별 복잡도 분석 및 에이전트 타입 설정
        for req in requests:
            if "agent_type" not in req:
                req["agent_type"] = analyze_complexity(req["message"])

        return await self.process_batch_requests(requests)

# 사용 예제
async def performance_test():
    """성능 테스트"""

    agent_pool = OptimizedAgentPool(max_workers=8)

    # 테스트 요청 생성
    test_requests = [
        {
            "request_id": i,
            "message": f"Simple question #{i}: What is AI?" if i % 2 == 0
                      else f"Complex analysis #{i}: Provide a detailed analysis of artificial intelligence trends, market impact, and future implications for businesses.",
            "user_id": f"user_{i % 3}"
        }
        for i in range(20)
    ]

    print(f"🚀 처리 시작: {len(test_requests)}개 요청")
    start_time = time.time()

    # 배치 처리
    results = await agent_pool.smart_routing(test_requests)

    total_time = time.time() - start_time

    print(f"✅ 처리 완료: {total_time:.2f}초")
    print(f"📊 평균 처리 시간: {total_time/len(test_requests):.2f}초/요청")

    # 결과 분석
    fast_count = sum(1 for r in results if "fast_agent" in r["agent_used"])
    smart_count = sum(1 for r in results if "smart_agent" in r["agent_used"])

    print(f"🔄 에이전트 사용 분포:")
    print(f"  - 빠른 에이전트: {fast_count}개")
    print(f"  - 스마트 에이전트: {smart_count}개")

# 실행
if __name__ == "__main__":
    asyncio.run(performance_test())
```

### 7.1.2. 메모리 및 캐싱 최적화

```python
import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
import hashlib
import time
import json
from typing import Dict, Any, Optional
import sqlite3
import threading

class CachedAgentManager:
    def __init__(self, cache_size: int = 1000, cache_ttl: int = 3600):
        self.cache_size = cache_size
        self.cache_ttl = cache_ttl
        self.memory_cache = {}
        self.cache_stats = {"hits": 0, "misses": 0}
        self.lock = threading.Lock()

        # SQLite 기반 영구 캐시
        self.setup_persistent_cache()
        self.setup_agents()

    def setup_persistent_cache(self):
        """영구 캐시 설정"""
        self.db_connection = sqlite3.connect("agent_cache.db", check_same_thread=False)
        cursor = self.db_connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_cache (
                cache_key TEXT PRIMARY KEY,
                agent_name TEXT,
                request_content TEXT,
                response_content TEXT,
                created_at REAL,
                access_count INTEGER DEFAULT 1
            )
        ''')

        # 인덱스 생성
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent_created
            ON agent_cache(agent_name, created_at)
        ''')

        self.db_connection.commit()

    def setup_agents(self):
        """에이전트 설정"""
        model_configs = [
            {
                "config_name": "cached_config",
                "model_type": "openai_chat",
                "model": "gpt-4o-mini",
                "api_key": "your-openai-api-key"
            }
        ]

        agentscope.init(
            model_configs=model_configs,
            project="cached_agent_system"
        )

        self.agents = {
            "general": DialogAgent(
                name="general_agent",
                model_config_name="cached_config",
                sys_prompt="You are a helpful assistant."
            ),
            "analyst": DialogAgent(
                name="analyst_agent",
                model_config_name="cached_config",
                sys_prompt="You are a data analyst."
            )
        }

    def generate_cache_key(self, agent_name: str, message: str) -> str:
        """캐시 키 생성"""
        content = f"{agent_name}:{message}"
        return hashlib.md5(content.encode()).hexdigest()

    def get_from_memory_cache(self, cache_key: str) -> Optional[str]:
        """메모리 캐시에서 조회"""
        with self.lock:
            if cache_key in self.memory_cache:
                entry = self.memory_cache[cache_key]

                # TTL 확인
                if time.time() - entry["timestamp"] < self.cache_ttl:
                    entry["access_count"] += 1
                    self.cache_stats["hits"] += 1
                    return entry["response"]
                else:
                    # 만료된 항목 제거
                    del self.memory_cache[cache_key]

            return None

    def set_memory_cache(self, cache_key: str, response: str):
        """메모리 캐시에 저장"""
        with self.lock:
            # 캐시 크기 제한
            if len(self.memory_cache) >= self.cache_size:
                # LRU 방식으로 오래된 항목 제거
                oldest_key = min(
                    self.memory_cache.keys(),
                    key=lambda k: self.memory_cache[k]["timestamp"]
                )
                del self.memory_cache[oldest_key]

            self.memory_cache[cache_key] = {
                "response": response,
                "timestamp": time.time(),
                "access_count": 1
            }

    def get_from_persistent_cache(self, cache_key: str) -> Optional[str]:
        """영구 캐시에서 조회"""
        cursor = self.db_connection.cursor()

        cursor.execute('''
            SELECT response_content, created_at, access_count
            FROM agent_cache
            WHERE cache_key = ?
        ''', (cache_key,))

        result = cursor.fetchone()

        if result:
            response_content, created_at, access_count = result

            # TTL 확인
            if time.time() - created_at < self.cache_ttl:
                # 액세스 횟수 업데이트
                cursor.execute('''
                    UPDATE agent_cache
                    SET access_count = access_count + 1
                    WHERE cache_key = ?
                ''', (cache_key,))
                self.db_connection.commit()

                self.cache_stats["hits"] += 1
                return response_content

        return None

    def set_persistent_cache(self, cache_key: str, agent_name: str,
                           request: str, response: str):
        """영구 캐시에 저장"""
        cursor = self.db_connection.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO agent_cache
            (cache_key, agent_name, request_content, response_content, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (cache_key, agent_name, request, response, time.time()))

        self.db_connection.commit()

    def process_with_cache(self, agent_name: str, message: str) -> Dict[str, Any]:
        """캐시를 활용한 에이전트 처리"""

        cache_key = self.generate_cache_key(agent_name, message)
        start_time = time.time()

        # 1단계: 메모리 캐시 확인
        cached_response = self.get_from_memory_cache(cache_key)
        if cached_response:
            return {
                "response": cached_response,
                "cache_hit": "memory",
                "processing_time": time.time() - start_time,
                "agent_used": agent_name
            }

        # 2단계: 영구 캐시 확인
        cached_response = self.get_from_persistent_cache(cache_key)
        if cached_response:
            # 메모리 캐시에도 저장
            self.set_memory_cache(cache_key, cached_response)

            return {
                "response": cached_response,
                "cache_hit": "persistent",
                "processing_time": time.time() - start_time,
                "agent_used": agent_name
            }

        # 3단계: 실제 에이전트 실행
        self.cache_stats["misses"] += 1

        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent: {agent_name}")

        agent = self.agents[agent_name]
        msg = Msg(name="User", content=message, role="user")

        response = agent(msg)
        response_content = response.content

        # 양쪽 캐시에 저장
        self.set_memory_cache(cache_key, response_content)
        self.set_persistent_cache(cache_key, agent_name, message, response_content)

        return {
            "response": response_content,
            "cache_hit": "none",
            "processing_time": time.time() - start_time,
            "agent_used": agent_name
        }

    def get_cache_stats(self) -> Dict[str, Any]:
        """캐시 통계 조회"""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM agent_cache")
        persistent_cache_size = cursor.fetchone()[0]

        return {
            "memory_cache_size": len(self.memory_cache),
            "persistent_cache_size": persistent_cache_size,
            "total_hits": self.cache_stats["hits"],
            "total_misses": self.cache_stats["misses"],
            "hit_rate_percent": round(hit_rate, 2),
            "cache_ttl_seconds": self.cache_ttl
        }

    def cleanup_expired_cache(self):
        """만료된 캐시 정리"""
        current_time = time.time()

        # 메모리 캐시 정리
        with self.lock:
            expired_keys = [
                key for key, entry in self.memory_cache.items()
                if current_time - entry["timestamp"] > self.cache_ttl
            ]
            for key in expired_keys:
                del self.memory_cache[key]

        # 영구 캐시 정리
        cursor = self.db_connection.cursor()
        cursor.execute('''
            DELETE FROM agent_cache
            WHERE created_at < ?
        ''', (current_time - self.cache_ttl,))
        self.db_connection.commit()

        print(f"🧹 캐시 정리 완료: 메모리 {len(expired_keys)}개, "
              f"영구 {cursor.rowcount}개 항목 제거")

# 사용 예제 및 벤치마크
def benchmark_cached_system():
    """캐시 시스템 벤치마크"""

    cached_manager = CachedAgentManager(cache_size=100, cache_ttl=1800)

    # 테스트 메시지들
    test_messages = [
        "What is artificial intelligence?",
        "Explain machine learning basics",
        "What are the benefits of AI?",
        "How does deep learning work?",
        "What is artificial intelligence?",  # 중복 (캐시 히트)
        "Explain machine learning basics",   # 중복 (캐시 히트)
    ]

    print("🏁 캐시 시스템 벤치마크 시작")
    print("="*40)

    total_time = 0

    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 요청 #{i}: {message[:30]}...")

        result = cached_manager.process_with_cache("general", message)
        total_time += result["processing_time"]

        print(f"   ⏱️ 처리 시간: {result['processing_time']:.3f}초")
        print(f"   💾 캐시 상태: {result['cache_hit']}")
        print(f"   📤 응답 길이: {len(result['response'])}자")

    print(f"\n📊 벤치마크 결과")
    print("="*25)
    print(f"총 처리 시간: {total_time:.3f}초")
    print(f"평균 처리 시간: {total_time/len(test_messages):.3f}초")

    # 캐시 통계 출력
    stats = cached_manager.get_cache_stats()
    print(f"\n💾 캐시 통계:")
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # 캐시 정리
    cached_manager.cleanup_expired_cache()

# 실행
if __name__ == "__main__":
    benchmark_cached_system()
```

---

# 8. 트러블슈팅

## 8.1. 일반적인 문제들

### 문제: AgentScope 초기화 실패
```python
# 해결책: 올바른 초기화 순서
import agentscope

# ❌ 잘못된 방법
# agent = DialogAgent(...)  # 초기화 전에 생성

# ✅ 올바른 방법
model_configs = [...]
agentscope.init(model_configs=model_configs, project="my_project")
agent = DialogAgent(...)  # 초기화 후에 생성
```

### 문제: 모델 설정 오류
```python
# 해결책: 올바른 모델 설정 형식
model_config = {
    "config_name": "unique_name",  # 고유한 이름 필수
    "model_type": "openai_chat",   # 정확한 타입명
    "model": "gpt-4o-mini",        # 올바른 모델명
    "api_key": "sk-...",           # 유효한 API 키
    # 추가 설정들
    "temperature": 0.7,
    "max_tokens": 1000
}
```

### 문제: 비동기 실행 문제
```python
# 해결책: 올바른 비동기 패턴
import asyncio

async def correct_async_usage():
    # 비동기 메서드 사용
    result = await agent.async_run(message)
    return result

# 실행
result = asyncio.run(correct_async_usage())
```

## 8.2. 디버깅 및 로깅

```python
import logging
import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
import json

# 상세 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agentscope_debug.log'),
        logging.StreamHandler()
    ]
)

class DebuggingAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"AgentScope.{agent_name}")
        self.setup_agent()

    def setup_agent(self):
        """디버깅이 활성화된 에이전트 설정"""

        model_configs = [
            {
                "config_name": "debug_config",
                "model_type": "openai_chat",
                "model": "gpt-4o-mini",
                "api_key": "your-openai-api-key"
            }
        ]

        agentscope.init(
            model_configs=model_configs,
            project="debugging_test",
            logger_level="DEBUG"  # 상세 로깅
        )

        self.agent = DialogAgent(
            name=self.agent_name,
            model_config_name="debug_config",
            sys_prompt="You are a helpful assistant with debugging enabled."
        )

    def debug_run(self, message: str):
        """디버깅 정보와 함께 에이전트 실행"""

        self.logger.info(f"=== 디버깅 시작 ===")
        self.logger.info(f"Agent: {self.agent_name}")
        self.logger.info(f"Input: {message}")

        try:
            # 메시지 생성 로그
            msg = Msg(name="User", content=message, role="user")
            self.logger.debug(f"Message object created: {msg}")

            # 에이전트 실행
            self.logger.info("에이전트 실행 시작...")
            response = self.agent(msg)

            # 응답 로그
            self.logger.info(f"Response received: {len(response.content)} characters")
            self.logger.debug(f"Full response: {response.content}")

            # 메타데이터 로그 (있는 경우)
            if hasattr(response, 'metadata'):
                self.logger.debug(f"Response metadata: {response.metadata}")

            return response

        except Exception as e:
            self.logger.error(f"에이전트 실행 중 오류: {str(e)}")
            self.logger.exception("상세 오류 정보:")
            raise

        finally:
            self.logger.info("=== 디버깅 완료 ===")

# 성능 모니터링 도구
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "total_response_time": 0,
            "error_count": 0,
            "requests_by_agent": {},
            "average_response_length": 0
        }

    def track_request(self, agent_name: str, processing_time: float,
                     response_length: int, success: bool = True):
        """요청 메트릭 추적"""

        self.metrics["total_requests"] += 1
        self.metrics["total_response_time"] += processing_time

        if not success:
            self.metrics["error_count"] += 1

        # 에이전트별 통계
        if agent_name not in self.metrics["requests_by_agent"]:
            self.metrics["requests_by_agent"][agent_name] = {
                "count": 0,
                "total_time": 0,
                "avg_response_length": 0
            }

        agent_stats = self.metrics["requests_by_agent"][agent_name]
        agent_stats["count"] += 1
        agent_stats["total_time"] += processing_time
        agent_stats["avg_response_length"] = (
            (agent_stats["avg_response_length"] * (agent_stats["count"] - 1) + response_length)
            / agent_stats["count"]
        )

        # 전체 평균 응답 길이 계산
        self.metrics["average_response_length"] = (
            (self.metrics["average_response_length"] * (self.metrics["total_requests"] - 1) + response_length)
            / self.metrics["total_requests"]
        )

    def get_performance_report(self) -> str:
        """성능 보고서 생성"""

        if self.metrics["total_requests"] == 0:
            return "성능 데이터가 없습니다."

        avg_response_time = self.metrics["total_response_time"] / self.metrics["total_requests"]
        error_rate = (self.metrics["error_count"] / self.metrics["total_requests"]) * 100

        report = f"""
📊 AgentScope 성능 보고서
{'='*40}

📈 전체 통계:
  - 총 요청 수: {self.metrics['total_requests']}
  - 평균 응답 시간: {avg_response_time:.3f}초
  - 오류율: {error_rate:.1f}%
  - 평균 응답 길이: {self.metrics['average_response_length']:.0f}자

🤖 에이전트별 성능:"""

        for agent_name, stats in self.metrics["requests_by_agent"].items():
            avg_time = stats["total_time"] / stats["count"] if stats["count"] > 0 else 0
            report += f"""
  {agent_name}:
    - 요청 수: {stats['count']}
    - 평균 시간: {avg_time:.3f}초
    - 평균 응답 길이: {stats['avg_response_length']:.0f}자"""

        return report

# 사용 예제
def comprehensive_debugging_demo():
    """종합적인 디버깅 데모"""

    # 디버깅 에이전트 생성
    debug_agent = DebuggingAgent("debug_assistant")

    # 성능 모니터 생성
    monitor = PerformanceMonitor()

    # 테스트 메시지들
    test_messages = [
        "Hello, how are you?",
        "Explain quantum computing",
        "What's the weather like?",  # 에러 유발 가능
        "Tell me a joke"
    ]

    print("🔍 종합 디버깅 데모 시작")
    print("="*30)

    for i, message in enumerate(test_messages, 1):
        print(f"\n🧪 테스트 #{i}: {message}")

        import time
        start_time = time.time()

        try:
            response = debug_agent.debug_run(message)
            processing_time = time.time() - start_time
            success = True

            print(f"✅ 성공: {response.content[:50]}...")

        except Exception as e:
            processing_time = time.time() - start_time
            success = False

            print(f"❌ 실패: {str(e)}")

        # 성능 추적
        monitor.track_request(
            agent_name="debug_assistant",
            processing_time=processing_time,
            response_length=len(response.content) if success and response else 0,
            success=success
        )

    # 성능 보고서 출력
    print("\n" + monitor.get_performance_report())

# 실행
if __name__ == "__main__":
    comprehensive_debugging_demo()
```

---

# 9. 추가 리소스

## 9.1. 공식 문서 및 학습 자료
- **공식 문서**: https://doc.agentscope.io/
- **GitHub 저장소**: https://github.com/agentscope-ai/agentscope
- **논문**: "AgentScope: A Flexible yet Robust Multi-Agent Platform" (arXiv)
- **PyPI 패키지**: https://pypi.org/project/agentscope/

## 9.2. 커뮤니티 및 지원
- **GitHub Issues**: 버그 리포트 및 기능 요청
- **GitHub Discussions**: 커뮤니티 토론 및 질문
- **Medium 블로그**: AgentScope 관련 기술 아티클

## 9.3. 확장 도구 및 통합
- **AgentScope Studio**: 드래그 앤 드롭 개발 환경
- **AgentScope Runtime**: 프로덕션 배포용 런타임
- **모델 지원**: OpenAI, DashScope, Gemini, Anthropic, Ollama
- **배포 옵션**: Docker, Kubernetes, 클라우드 플랫폼

## 9.4. 관련 프레임워크 비교
- **vs LangChain**: 더 직관적인 에이전트 중심 설계
- **vs AutoGen**: 드래그 앤 드롭 UI와 액터 모델 지원
- **vs CrewAI**: 더 유연한 아키텍처와 투명성
- **vs Google ADK**: 오픈소스와 커뮤니티 중심

---

# 10. 결론

AgentScope는 **알리바바에서 개발한 혁신적인 멀티 에이전트 플랫폼**으로, 에이전트 지향 프로그래밍의 새로운 패러다임을 제시합니다.

## ✅ AgentScope를 선택해야 하는 경우
- **드래그 앤 드롭 개발** 선호
- **완전한 투명성** 필요 (모든 내부 과정 가시화)
- **복잡한 멀티 에이전트 시스템** 구축
- **비동기 고성능** 처리 필요

## 🚀 2025년 핵심 혁신
- **에이전트 지향 프로그래밍**: 새로운 개발 패러다임 제시
- **드래그 앤 드롭 UI**: 코딩 없는 에이전트 시스템 구성
- **완전한 비동기 v1.0**: 고성능 병렬 처리 지원
- **AgentScope Studio**: 프로덕션 급 개발 환경

## 💼 독특한 가치 제안
- **제로 코드 개발**: 프로그래밍 경험이 적어도 구축 가능
- **액터 모델**: 자동 병렬 최적화와 분산 처리
- **모듈형 레고 설계**: 유연한 조합과 확장성
- **알리바바 생태계**: 대규모 서비스 검증된 안정성

## 🎯 특별한 적합성
- **연구개발팀**: 빠른 프로토타이핑과 실험
- **비개발자 팀**: 드래그 앤 드롭으로 AI 시스템 구축
- **대규모 시스템**: 액터 모델 기반 확장성
- **교육 기관**: 직관적인 멀티 에이전트 학습 도구

AgentScope는 **직관적이면서도 강력한 멀티 에이전트 시스템**을 구축하고자 하는 모든 개발자와 조직에게 완전히 새로운 경험을 제공하는 혁신적인 플랫폼입니다.