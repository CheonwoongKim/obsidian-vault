---
title: "LangChain 완전 가이드 - 설치와 활용법"
type: resource
category: 개발도구/AI프레임워크
tags: [도구/LangChain, 기술/LLM, 방법론/AI개발]
status: active
date: 2025-09-24
updated: 2025-09-24
source: ["LangChain 공식 문서", "실무 프로젝트 경험", "2025년 최신 업데이트"]
---

## 1. LangChain 개요

**LangChain**은 대화형 AI 애플리케이션 개발을 위한 포괄적인 프레임워크입니다. LLM을 중심으로 한 복잡한 워크플로우, 도구 연동, 메모리 관리, 에이전트 시스템을 구축할 수 있습니다.

### 1.1. 핵심 구성 요소

- **LLMs**: 다양한 언어 모델 통합 (OpenAI, Claude, Gemini 등)
- **Prompts**: 프롬프트 템플릿 관리 및 최적화
- **Chains**: 순차적 작업 체인 구성
- **Agents**: 도구 사용 가능한 자율 에이전트
- **Memory**: 대화 기록 및 상태 관리
- **Tools**: 외부 API, 데이터베이스 연동

### 1.2. 2025년 주요 업데이트

- **LangChain Expression Language (LCEL)**: 파이프라인 구성 언어
- **LangSmith**: 디버깅 및 모니터링 플랫폼
- **LangServe**: 프로덕션 배포 프레임워크
- **Community Extensions**: 700+ 통합 패키지

---

## 2. 설치 및 환경 설정

### 2.1. 기본 설치

```bash
# 가상 환경 생성 (권장)
python -m venv langchain_env
source langchain_env/bin/activate  # macOS/Linux
# langchain_env\Scripts\activate  # Windows

# 기본 LangChain 설치
pip install langchain

# 주요 통합 패키지
pip install langchain-openai      # OpenAI 통합
pip install langchain-anthropic   # Claude 통합
pip install langchain-google-genai # Gemini 통합
pip install langchain-community   # 커뮤니티 통합

# 추가 유용한 패키지
pip install langchainhub          # 프롬프트 허브
pip install langsmith             # 모니터링
pip install langserve            # 서버 배포
```

### 2.2. 환경 변수 설정

**.env 파일:**
```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (Claude)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google (Gemini)
GOOGLE_API_KEY=your_google_api_key_here

# LangSmith (선택사항)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=your_project_name
```

**환경 변수 로드:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
```

---

## 3. 기본 사용법

### 3.1. LLM 기본 사용

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# LLM 초기화
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000
)

# 메시지 생성 및 호출
messages = [
    SystemMessage(content="당신은 도움이 되는 AI 어시스턴트입니다."),
    HumanMessage(content="파이썬에서 리스트와 튜플의 차이점을 설명해주세요.")
]

response = llm.invoke(messages)
print(response.content)
```

### 3.2. 프롬프트 템플릿

```python
from langchain_core.prompts import ChatPromptTemplate

# 템플릿 정의
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 {domain} 전문가입니다."),
    ("human", "{question}에 대해 {style} 스타일로 설명해주세요.")
])

# 메시지 포맷팅
formatted_prompt = prompt.format_messages(
    domain="데이터 사이언스",
    question="머신러닝과 딥러닝의 차이",
    style="초보자도 이해하기 쉬운"
)

response = llm.invoke(formatted_prompt)
print(response.content)
```

### 3.3. LCEL (LangChain Expression Language)

```python
from langchain_core.output_parsers import StrOutputParser

# 파이프라인 체인 구성
chain = prompt | llm | StrOutputParser()

# 스트리밍 실행
for chunk in chain.stream({
    "domain": "웹 개발",
    "question": "React와 Vue.js 비교",
    "style": "실무 개발자 관점에서"
}):
    print(chunk, end="", flush=True)
```

---

## 4. 고급 기능

### 4.1. RAG (Retrieval-Augmented Generation)

```python
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 문서 로드 및 분할
loader = TextLoader("document.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# 벡터 스토어 생성
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()
)

# RAG 체인 구성
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 질문 수행
result = qa_chain.invoke({"query": "문서에서 핵심 내용은 무엇인가요?"})
print(result['result'])
```

### 4.2. 에이전트와 도구

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# 도구 정의
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

tools = [wikipedia]

# 에이전트 프롬프트
from langchain import hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# 에이전트 생성
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 에이전트 실행
result = agent_executor.invoke({
    "input": "2024년 노벨 물리학상 수상자에 대해 알려주세요"
})
print(result['output'])
```

### 4.3. 메모리 관리

```python
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain

# 메모리 초기화 (최근 5개 대화만 기억)
memory = ConversationBufferWindowMemory(k=5)

# 대화 체인 생성
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# 연속 대화
response1 = conversation.invoke({"input": "안녕하세요, 제 이름은 김철수입니다."})
response2 = conversation.invoke({"input": "제 이름을 기억하고 계신가요?"})

print(response1['response'])
print(response2['response'])
```

---

## 5. 실무 패턴

### 5.1. 문서 요약 시스템

```python
from langchain.chains.summarize import load_summarize_chain

# 요약 체인 로드
summarize_chain = load_summarize_chain(
    llm=llm,
    chain_type="map_reduce",  # 긴 문서용
    verbose=True
)

# 문서 요약 실행
summary = summarize_chain.invoke({"input_documents": splits})
print(summary['output_text'])
```

### 5.2. 분류 및 라우팅

```python
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser

# 전문 분야별 프롬프트 정의
prompt_infos = [
    {
        "name": "technical",
        "description": "기술적 질문에 대한 답변",
        "prompt_template": "기술 전문가로서 다음 질문에 답하세요: {input}"
    },
    {
        "name": "business",
        "description": "비즈니스 관련 질문에 대한 답변",
        "prompt_template": "비즈니스 컨설턴트로서 다음 질문에 답하세요: {input}"
    }
]

# 라우터 체인 생성
router_chain = MultiPromptChain.from_prompts(
    llm=llm,
    prompt_infos=prompt_infos
)

# 자동 라우팅 실행
result = router_chain.invoke({"input": "마이크로서비스 아키텍처의 장단점은?"})
print(result['text'])
```

### 5.3. 배치 처리

```python
import asyncio
from langchain_core.runnables import RunnableLambda

# 배치 처리 함수
async def batch_process():
    questions = [
        "파이썬이 뭔가요?",
        "자바스크립트의 특징은?",
        "데이터베이스란 무엇인가요?"
    ]

    # 병렬 처리
    results = await chain.abatch([{"question": q} for q in questions])
    return results

# 실행
results = asyncio.run(batch_process())
for i, result in enumerate(results):
    print(f"질문 {i+1}: {result}")
```

---

## 6. LangSmith 통합

### 6.1. 추적 및 모니터링

```python
from langsmith import Client
import langsmith

# 추적 활성화 (환경변수로 설정 시 자동)
@langsmith.traceable
def my_chain(question: str) -> str:
    response = chain.invoke({"question": question})
    return response

# 실행 (자동으로 LangSmith에 기록됨)
result = my_chain("LangChain이 뭔가요?")
```

### 6.2. 평가 및 테스트

```python
from langsmith.evaluation import evaluate

# 평가 데이터셋
dataset = [
    {"question": "파이썬이란?", "expected": "프로그래밍 언어"},
    {"question": "AI란?", "expected": "인공지능"}
]

# 평가 함수
def relevance_evaluator(run, example):
    # 관련성 점수 계산 로직
    score = calculate_relevance(run.outputs['text'], example.outputs['expected'])
    return {"score": score}

# 평가 실행
results = evaluate(
    my_chain,
    data=dataset,
    evaluators=[relevance_evaluator]
)
```

---

## 7. LangServe 배포

### 7.1. FastAPI 서버 생성

```python
from langserve import add_routes
from fastapi import FastAPI

# FastAPI 앱 생성
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using Langchain"
)

# 체인 라우트 추가
add_routes(
    app,
    chain,
    path="/chat"
)

# 서버 실행: uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7.2. 클라이언트 사용

```python
from langserve import RemoteRunnable

# 원격 체인 연결
remote_chain = RemoteRunnable("http://localhost:8000/chat/")

# 원격 실행
result = remote_chain.invoke({"question": "안녕하세요"})
print(result)
```

---

## 8. 성능 최적화

### 8.1. 캐싱

```python
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache

# SQLite 캐시 설정
set_llm_cache(SQLiteCache(database_path=".langchain.db"))

# 동일한 질문은 캐시에서 빠르게 응답
response1 = llm.invoke([HumanMessage(content="안녕하세요")])
response2 = llm.invoke([HumanMessage(content="안녕하세요")])  # 캐시에서 반환
```

### 8.2. 스트리밍

```python
# 스트리밍 응답
for chunk in llm.stream([HumanMessage(content="긴 이야기를 들려주세요")]):
    print(chunk.content, end="", flush=True)
```

### 8.3. 토큰 최적화

```python
from langchain.callbacks import get_openai_callback

# 토큰 사용량 추적
with get_openai_callback() as cb:
    result = chain.invoke({"question": "설명해주세요"})
    print(f"총 토큰: {cb.total_tokens}")
    print(f"비용: ${cb.total_cost:.4f}")
```

---

## 9. 트러블슈팅

### 9.1. 일반적인 오류들

**1. API 키 오류**
```python
# 환경 변수 확인
import os
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY")[:10] + "...")
```

**2. 토큰 한계 초과**
```python
from langchain.text_splitter import TokenTextSplitter

# 토큰 기반 분할
splitter = TokenTextSplitter(
    model_name="gpt-4",
    chunk_size=3000,
    chunk_overlap=100
)
```

**3. 메모리 부족**
```python
# 배치 크기 조정
batch_size = 5
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    results = chain.batch(batch)
```

### 9.2. 디버깅 팁

```python
# 상세 로깅 활성화
import logging
logging.basicConfig(level=logging.DEBUG)

# 중간 단계 출력
chain = prompt | llm | StrOutputParser()
chain.invoke({"question": "테스트"}, verbose=True)
```

---

## 10. 베스트 프랙티스

### 10.1. 프롬프트 엔지니어링

```python
# 구조화된 프롬프트
system_prompt = """
당신은 전문적인 {domain} 컨설턴트입니다.

답변 형식:
1. 핵심 요약 (2-3줄)
2. 상세 설명
3. 실무 적용 팁
4. 추가 참고사항

답변은 정확하고 실용적이어야 합니다.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}")
])
```

### 10.2. 에러 처리

```python
from langchain_core.runnables import RunnableLambda

def safe_invoke(inputs):
    try:
        return chain.invoke(inputs)
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

safe_chain = RunnableLambda(safe_invoke)
```

### 10.3. 설정 관리

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000

    class Config:
        env_file = ".env"

settings = Settings()
llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model=settings.model_name,
    temperature=settings.temperature
)
```

---

## 11. 실습 프로젝트

### 11.1. 고객 지원 챗봇

```python
from langchain.memory import ConversationSummaryBufferMemory

class CustomerSupportBot:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.3)
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=1000
        )
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory
        )

    def respond(self, message: str) -> str:
        prompt = f"""
        고객 지원 담당자로서 친절하고 도움이 되는 답변을 제공하세요.
        문제 해결에 집중하고, 필요시 추가 정보를 요청하세요.

        고객 메시지: {message}
        """
        return self.conversation.invoke({"input": prompt})['response']

# 사용 예시
bot = CustomerSupportBot()
response = bot.respond("로그인이 안 됩니다")
print(response)
```

### 11.2. 문서 QA 시스템

```python
class DocumentQA:
    def __init__(self, document_path: str):
        # 문서 로드
        loader = TextLoader(document_path)
        documents = loader.load()

        # 벡터화
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)

        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=OpenAIEmbeddings()
        )

        # QA 체인
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(temperature=0),
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True
        )

    def ask(self, question: str):
        result = self.qa_chain.invoke({"query": question})
        return {
            "answer": result['result'],
            "sources": [doc.page_content[:200] + "..."
                       for doc in result['source_documents']]
        }

# 사용 예시
qa_system = DocumentQA("company_handbook.txt")
result = qa_system.ask("휴가 정책은 어떻게 되나요?")
print(result['answer'])
```

---

## 12. 참고 자료

### 12.1. 공식 문서
- **LangChain 문서**: https://python.langchain.com/
- **LangSmith**: https://smith.langchain.com/
- **LangServe**: https://python.langchain.com/docs/langserve

### 12.2. 커뮤니티
- **GitHub**: https://github.com/langchain-ai/langchain
- **Discord**: https://discord.gg/langchain
- **Twitter**: @LangChainAI

### 12.3. 추가 리소스
- **LangChain Hub**: https://smith.langchain.com/hub
- **Templates**: https://github.com/langchain-ai/langchain-templates
- **Cookbook**: https://github.com/langchain-ai/langchain-cookbook

---

## 13. 체크리스트

**기본 설정:**
- [ ] Python 3.8+ 설치 확인
- [ ] 가상 환경 생성 및 활성화
- [ ] LangChain 및 관련 패키지 설치
- [ ] API 키 설정 (.env 파일)

**기본 사용법:**
- [ ] LLM 기본 호출 테스트
- [ ] 프롬프트 템플릿 작성
- [ ] LCEL 체인 구성
- [ ] 스트리밍 응답 구현

**고급 기능:**
- [ ] RAG 시스템 구축
- [ ] 에이전트 및 도구 연동
- [ ] 메모리 관리 구현
- [ ] 배치 처리 최적화

**프로덕션:**
- [ ] LangSmith 연동
- [ ] LangServe 배포
- [ ] 성능 모니터링
- [ ] 에러 처리 및 로깅

**2025년 9월 기준 최신 정보와 실무 경험을 바탕으로 작성된 종합 가이드입니다.**