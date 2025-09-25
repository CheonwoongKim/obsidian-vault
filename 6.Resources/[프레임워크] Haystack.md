---
title: "[프레임워크] Haystack 완전 가이드 - RAG 및 검색 시스템"
type: resource
category: AI/프레임워크
tags: [haystack, RAG, 검색시스템, deepset, AI프레임워크, LLM, 벡터검색]
source: "공식 문서 및 실습 기반 작성"
status: active
updated: 2025-09-24
---

## 🔗 관련 가이드

### AI 프레임워크 시리즈
- **[[프레임워크] LangChain]]** - 종합 AI 애플리케이션 프레임워크
- **[[프레임워크] LlamaIndex]]** - RAG 특화 데이터 연결
- **[프레임워크] Haystack 완전 가이드 - RAG 및 검색 시스템** ← **현재 가이드**
- **[[프레임워크] DSPy]]** - 프롬프트 최적화

### 엔터프라이즈 AI 프레임워크
- **[[프레임워크] Google ADK]]** - 구글 에이전트 개발 플랫폼
- **[[프레임워크] AgentScope]]** - 대규모 에이전트 플랫폼

### RAG 시스템 가이드
- **[[프롬프트] 11 Retrieval Augmented Generation (RAG) 프롬프팅]]** - RAG 프롬프팅 기법
- **[[[RAG] 01 문서 파싱(Document Parsing) 완전 가이드]]** - 문서 전처리 및 파싱
- **[[[RAG] 03 임베딩(Embedding) 최적화 가이드]]** - 벡터 임베딩 모델 선택
- **[[[RAG] 04 리트리버(Retriever) 최적화 가이드]]** - 검색 시스템 성능 개선
- **[[[RAG] 05 평가 및 모니터링 가이드]]** - RAG 성능 측정

### 프롬프트 엔지니어링
- **[[프롬프트 엔지니어링 - 마스터 가이드]]** - 전체 프롬프팅 기법 개요

---

# 1. 개요

Haystack은 deepset에서 개발한 오픈소스 AI 오케스트레이션 프레임워크로, **프로덕션 급 LLM 애플리케이션**을 구축하기 위한 도구입니다. 특히 **RAG(Retrieval-Augmented Generation), 문서 검색, 질의응답 시스템** 구축에 특화되어 있습니다.

## 핵심 특징

### 🎯 전문 분야
- **RAG 시스템**: 문서 기반 질의응답
- **시맨틱 검색**: 벡터 기반 의미 검색
- **문서 처리**: PDF, HTML, 텍스트 등 다양한 포맷 지원
- **에이전틱 워크플로우**: 2025년 트렌드 반영

### 🔧 핵심 구성 요소
- **컴포넌트 기반**: 모듈형 아키텍처
- **파이프라인**: 컴포넌트들을 연결한 워크플로우
- **에이전트**: 자율적 의사결정 및 도구 사용
- **멀티모달**: 텍스트, 이미지, 오디오 지원

---

# 2. 설치 및 환경 설정

## 2.1. 기본 설치

```bash
# 가상환경 생성 (권장)
python3 -m venv haystack_env
source haystack_env/bin/activate  # macOS/Linux
# haystack_env\Scripts\activate  # Windows

# Haystack 설치
pip install haystack-ai

# 추가 의존성 (필요에 따라)
pip install sentence-transformers  # 임베딩 모델용
pip install faiss-cpu  # FAISS 벡터 스토어용
pip install transformers torch  # 로컬 모델용
```

## 2.2. 환경 변수 설정

```bash
# .env 파일 생성
OPENAI_API_KEY=your-openai-key
HUGGINGFACE_API_TOKEN=your-hf-token  # 선택사항
```

## 2.3. 설치 확인

```python
import haystack
print(f"Haystack version: {haystack.__version__}")

# 기본 컴포넌트 import 테스트
from haystack import Document, Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder

print("✅ Haystack 설치 완료")
```

---

# 3. 기본 사용법

## 3.1. 간단한 생성 파이프라인

```python
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder

# 컴포넌트 생성
prompt_builder = PromptBuilder(
    template="Answer the question: {{question}}"
)
llm = OpenAIGenerator(model="gpt-4o-mini")

# 파이프라인 구성
basic_pipeline = Pipeline()
basic_pipeline.add_component("prompt_builder", prompt_builder)
basic_pipeline.add_component("llm", llm)

# 컴포넌트 연결
basic_pipeline.connect("prompt_builder", "llm")

# 실행
result = basic_pipeline.run({
    "prompt_builder": {"question": "What is artificial intelligence?"}
})

print(result["llm"]["replies"][0])
```

## 3.2. 문서 기반 RAG 시스템

```python
import os
from haystack import Document, Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.document_stores.in_memory import InMemoryDocumentStore

# 문서 저장소 생성
document_store = InMemoryDocumentStore()

# 샘플 문서 추가
documents = [
    Document(content="Haystack is an AI orchestration framework for building production-ready LLM applications."),
    Document(content="RAG stands for Retrieval-Augmented Generation, combining retrieval with generation."),
    Document(content="Vector search uses embeddings to find semantically similar content.")
]

document_store.write_documents(documents)

# RAG 파이프라인 구성
rag_pipeline = Pipeline()

# 컴포넌트 추가
retriever = InMemoryBM25Retriever(document_store=document_store)
prompt_builder = PromptBuilder(
    template="""
    Given these documents:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}

    Answer the question: {{ question }}
    """
)
generator = OpenAIGenerator()

rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("generator", generator)

# 연결
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "generator")

# 실행
result = rag_pipeline.run({
    "retriever": {"query": "What is RAG?"},
    "prompt_builder": {"question": "What is RAG?"}
})

print(result["generator"]["replies"][0])
```

---

# 4. 고급 활용법

## 4.1. 벡터 기반 시맨틱 검색

```python
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore

# 임베딩 기반 문서 저장소
document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")

# 문서 임베딩
doc_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
doc_embedder.warm_up()

# 문서 처리
documents_with_embeddings = doc_embedder.run(documents)
document_store.write_documents(documents_with_embeddings["documents"])

# 시맨틱 검색 파이프라인
semantic_pipeline = Pipeline()

text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
retriever = InMemoryEmbeddingRetriever(document_store=document_store)

semantic_pipeline.add_component("text_embedder", text_embedder)
semantic_pipeline.add_component("retriever", retriever)
semantic_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

# 시맨틱 검색 실행
result = semantic_pipeline.run({
    "text_embedder": {"text": "AI framework for applications"}
})

for doc in result["retriever"]["documents"]:
    print(f"Score: {doc.score:.3f} - {doc.content}")
```

## 4.2. 에이전트 시스템 (2025년 신기능)

```python
from haystack.agents import Agent
from haystack.agents.tools import Tool
from haystack.components.generators import OpenAIGenerator

def search_web(query: str) -> str:
    """웹 검색 시뮬레이션"""
    return f"검색 결과: {query}에 대한 정보를 찾았습니다."

def calculate(expression: str) -> str:
    """계산 도구"""
    try:
        result = eval(expression)
        return f"계산 결과: {result}"
    except:
        return "계산 오류가 발생했습니다."

# 도구 정의
tools = [
    Tool(name="search_web", description="Search the web for information", function=search_web),
    Tool(name="calculate", description="Perform mathematical calculations", function=calculate)
]

# 에이전트 생성
agent = Agent(
    generator=OpenAIGenerator(model="gpt-4o"),
    tools=tools,
    system_prompt="You are a helpful assistant that can search the web and perform calculations."
)

# 에이전트 실행
response = agent.run("What's 25 * 4 + 10?")
print(response)
```

## 4.3. 멀티모달 파이프라인

```python
from haystack.components.generators.openai import OpenAIGenerator
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter

# 문서 처리 파이프라인
doc_processing_pipeline = Pipeline()

# 컴포넌트 추가
converter = PyPDFToDocument()
splitter = DocumentSplitter(split_by="sentence", split_length=3)
writer = DocumentWriter(document_store=document_store)

doc_processing_pipeline.add_component("converter", converter)
doc_processing_pipeline.add_component("splitter", splitter)
doc_processing_pipeline.add_component("writer", writer)

# 연결
doc_processing_pipeline.connect("converter", "splitter")
doc_processing_pipeline.connect("splitter", "writer")

# PDF 파일 처리
result = doc_processing_pipeline.run({
    "converter": {"sources": ["path/to/document.pdf"]}
})
```

---

# 5. 실제 프로젝트 예제

## 5.1. 기업 문서 QA 시스템

```python
import os
from pathlib import Path
from haystack import Pipeline, Document
from haystack.components.converters import PyPDFToDocument, TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.document_stores.in_memory import InMemoryDocumentStore

class CorporateQASystem:
    def __init__(self, openai_api_key: str):
        self.document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")
        self.openai_api_key = openai_api_key
        self.indexing_pipeline = None
        self.rag_pipeline = None
        self._setup_pipelines()

    def _setup_pipelines(self):
        """파이프라인 설정"""
        # 문서 인덱싱 파이프라인
        self.indexing_pipeline = Pipeline()

        converter = PyPDFToDocument()
        cleaner = DocumentCleaner()
        splitter = DocumentSplitter(split_by="sentence", split_length=10)
        embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
        writer = DocumentWriter(document_store=self.document_store)

        self.indexing_pipeline.add_component("converter", converter)
        self.indexing_pipeline.add_component("cleaner", cleaner)
        self.indexing_pipeline.add_component("splitter", splitter)
        self.indexing_pipeline.add_component("embedder", embedder)
        self.indexing_pipeline.add_component("writer", writer)

        self.indexing_pipeline.connect("converter", "cleaner")
        self.indexing_pipeline.connect("cleaner", "splitter")
        self.indexing_pipeline.connect("splitter", "embedder")
        self.indexing_pipeline.connect("embedder", "writer")

        # RAG 파이프라인
        self.rag_pipeline = Pipeline()

        text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
        retriever = InMemoryEmbeddingRetriever(document_store=self.document_store, top_k=5)
        prompt_builder = PromptBuilder(
            template="""
            기업 문서를 바탕으로 질문에 답변해주세요.

            관련 문서:
            {% for doc in documents %}
                {{ doc.content }}
            {% endfor %}

            질문: {{ question }}

            답변은 한국어로, 문서에 기반한 정확한 정보만 제공해주세요.
            """
        )
        generator = OpenAIGenerator(api_key=self.openai_api_key, model="gpt-4o-mini")

        self.rag_pipeline.add_component("text_embedder", text_embedder)
        self.rag_pipeline.add_component("retriever", retriever)
        self.rag_pipeline.add_component("prompt_builder", prompt_builder)
        self.rag_pipeline.add_component("generator", generator)

        self.rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        self.rag_pipeline.connect("retriever", "prompt_builder.documents")
        self.rag_pipeline.connect("prompt_builder", "generator")

    def index_documents(self, file_paths: list):
        """문서 인덱싱"""
        for file_path in file_paths:
            result = self.indexing_pipeline.run({
                "converter": {"sources": [file_path]}
            })
        print(f"✅ {len(file_paths)}개 문서 인덱싱 완료")

    def ask_question(self, question: str):
        """질문하기"""
        result = self.rag_pipeline.run({
            "text_embedder": {"text": question},
            "prompt_builder": {"question": question}
        })
        return result["generator"]["replies"][0]

# 사용 예제
if __name__ == "__main__":
    qa_system = CorporateQASystem(openai_api_key="your-api-key")

    # 문서 인덱싱
    document_files = ["company_policy.pdf", "financial_report.pdf", "employee_handbook.pdf"]
    qa_system.index_documents(document_files)

    # 질의응답
    questions = [
        "회사의 휴가 정책은 무엇인가요?",
        "작년 매출은 얼마였나요?",
        "재택근무 규정이 있나요?"
    ]

    for question in questions:
        answer = qa_system.ask_question(question)
        print(f"\n질문: {question}")
        print(f"답변: {answer}")
```

## 5.2. 실시간 뉴스 분석 시스템

```python
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.generators import OpenAIGenerator

class NewsAnalysisSystem:
    def __init__(self, openai_api_key: str):
        self.pipeline = Pipeline()
        self._setup_pipeline(openai_api_key)

    def _setup_pipeline(self, openai_api_key: str):
        """뉴스 분석 파이프라인 설정"""
        fetcher = LinkContentFetcher()
        converter = HTMLToDocument()
        prompt_builder = PromptBuilder(
            template="""
            다음 뉴스 기사를 분석해주세요:

            {{ documents[0].content }}

            다음 항목으로 분석해주세요:
            1. 핵심 내용 요약 (3줄)
            2. 주요 키워드 (5개)
            3. 산업/분야에 미치는 영향
            4. 투자자 관점에서의 시사점

            한국어로 답변해주세요.
            """
        )
        generator = OpenAIGenerator(api_key=openai_api_key, model="gpt-4o")

        self.pipeline.add_component("fetcher", fetcher)
        self.pipeline.add_component("converter", converter)
        self.pipeline.add_component("prompt_builder", prompt_builder)
        self.pipeline.add_component("generator", generator)

        self.pipeline.connect("fetcher", "converter")
        self.pipeline.connect("converter", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder", "generator")

    def analyze_news(self, url: str):
        """뉴스 URL 분석"""
        result = self.pipeline.run({
            "fetcher": {"urls": [url]}
        })
        return result["generator"]["replies"][0]

# 사용 예제
news_analyzer = NewsAnalysisSystem(openai_api_key="your-api-key")
analysis = news_analyzer.analyze_news("https://example-news-site.com/article")
print(analysis)
```

---

# 6. 프로덕션 배포

## 6.1. FastAPI 서버 구성

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI(title="Haystack RAG API", version="1.0.0")

# 전역 변수로 QA 시스템 초기화
qa_system = None

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    sources: list = []

@app.on_event("startup")
async def startup_event():
    """서버 시작시 모델 로드"""
    global qa_system
    qa_system = CorporateQASystem(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # 초기 문서 인덱싱
    document_files = ["docs/policy.pdf", "docs/handbook.pdf"]
    qa_system.index_documents(document_files)
    print("✅ 서버 시작 및 문서 인덱싱 완료")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """질문 처리 엔드포인트"""
    try:
        answer = qa_system.ask_question(request.question)
        return QuestionResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 6.2. Docker 컨테이너화

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 문서 디렉토리 생성
RUN mkdir -p docs

# 서버 실행
EXPOSE 8000
CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  haystack-rag:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./docs:/app/docs
      - ./data:/app/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - haystack-rag
```

## 6.3. 모니터링 및 로깅

```python
import logging
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

# 메트릭 설정
REQUEST_COUNT = Counter('haystack_requests_total', 'Total requests', ['endpoint'])
REQUEST_LATENCY = Histogram('haystack_request_latency_seconds', 'Request latency')

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def add_process_time_header(request, call_next):
    """요청 처리 시간 및 메트릭 수집"""
    start_time = time.time()

    REQUEST_COUNT.labels(endpoint=request.url.path).inc()

    response = await call_next(request)

    process_time = time.time() - start_time
    REQUEST_LATENCY.observe(process_time)

    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Path: {request.url.path} - Process time: {process_time:.4f}s")

    return response

@app.get("/metrics")
async def get_metrics():
    """Prometheus 메트릭 엔드포인트"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

---

# 7. 모범 사례 및 최적화

## 7.1. 성능 최적화

### 7.1.1. 벡터 스토어 최적화
```python
# FAISS 사용으로 대규모 문서 처리
from haystack.document_stores.faiss import FAISSDocumentStore

# 설정
document_store = FAISSDocumentStore(
    faiss_index_factory_str="HNSW32",
    return_embedding=True,
    embedding_dim=384
)

# 배치 처리로 인덱싱 속도 향상
batch_size = 1000
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    document_store.write_documents(batch)
```

### 7.1.2. 캐싱 전략
```python
from functools import lru_cache
import hashlib

class CachedQASystem(CorporateQASystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}

    def ask_question(self, question: str):
        # 질문 해시 생성
        question_hash = hashlib.md5(question.encode()).hexdigest()

        # 캐시 확인
        if question_hash in self.cache:
            return self.cache[question_hash]

        # 답변 생성 및 캐싱
        answer = super().ask_question(question)
        self.cache[question_hash] = answer

        return answer
```

## 7.2. 에러 처리 및 복구

```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

class RobustQASystem(CorporateQASystem):
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def ask_question(self, question: str):
        """재시도 로직이 포함된 질문 처리"""
        try:
            return super().ask_question(question)
        except Exception as e:
            logger.error(f"질문 처리 중 오류: {e}")
            raise

    def health_check(self):
        """시스템 상태 확인"""
        try:
            test_answer = self.ask_question("테스트 질문")
            return {"status": "healthy", "timestamp": time.time()}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e), "timestamp": time.time()}
```

## 7.3. 보안 모범 사례

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=["HS256"]
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@app.post("/ask")
async def ask_question(
    request: QuestionRequest,
    current_user: dict = Depends(verify_token)
):
    """인증이 필요한 질문 엔드포인트"""
    logger.info(f"User {current_user.get('user_id')} asked: {request.question}")

    # 사용자별 질문 제한
    if not check_rate_limit(current_user.get('user_id')):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    return await process_question(request)
```

---

# 8. 트러블슈팅

## 8.1. 일반적인 문제들

### 문제: 임베딩 모델 로드 실패
```bash
# 해결책: 모델 캐시 디렉토리 권한 확인
export TRANSFORMERS_CACHE=/path/to/cache
chmod -R 755 $TRANSFORMERS_CACHE
```

### 문제: 메모리 부족 오류
```python
# 해결책: 배치 크기 줄이기
doc_embedder = SentenceTransformersDocumentEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2",
    batch_size=32  # 기본값 128에서 줄임
)
```

### 문제: OpenAI API 응답 느림
```python
# 해결책: 타임아웃 및 재시도 설정
generator = OpenAIGenerator(
    model="gpt-4o-mini",
    timeout=30,
    max_retries=3
)
```

## 8.2. 디버깅 도구

```python
import logging

# 상세 로깅 활성화
logging.basicConfig(level=logging.DEBUG)
haystack_logger = logging.getLogger("haystack")
haystack_logger.setLevel(logging.DEBUG)

# 파이프라인 시각화
def visualize_pipeline(pipeline):
    """파이프라인 구조 출력"""
    print("Pipeline Structure:")
    for component_name, component in pipeline.graph.nodes(data=True):
        print(f"  - {component_name}: {component['instance'].__class__.__name__}")

    print("\nConnections:")
    for source, target, data in pipeline.graph.edges(data=True):
        print(f"  {source} -> {target}")

visualize_pipeline(rag_pipeline)
```

---

# 9. 추가 리소스

## 9.1. 공식 문서 및 튜토리얼
- **공식 문서**: https://haystack.deepset.ai/
- **GitHub**: https://github.com/deepset-ai/haystack
- **튜토리얼**: https://github.com/deepset-ai/haystack-tutorials
- **DeepLearning.AI 코스**: Building AI Applications with Haystack

## 9.2. 커뮤니티
- **Discord**: Haystack 공식 디스코드 채널
- **GitHub Discussions**: 질문 및 토론
- **Stack Overflow**: `haystack-ai` 태그

## 9.3. 확장 프레임워크
- **Haystack Hub**: 커뮤니티 컴포넌트
- **Deepset Cloud**: 관리형 Haystack 서비스
- **Integration Partners**: Elasticsearch, Pinecone, Weaviate 등

---

# 10. 결론

Haystack은 **RAG 시스템과 검색 기반 AI 애플리케이션**을 구축하는 데 가장 적합한 프레임워크 중 하나입니다. 특히 다음과 같은 경우에 권장됩니다:

## ✅ Haystack을 선택해야 하는 경우
- **문서 기반 QA 시스템** 구축
- **대규모 검색 시스템** 개발
- **RAG 파이프라인** 최적화 필요
- **다양한 문서 형식** 처리 필요

## 🚀 2025년 트렌드 반영
- **에이전틱 워크플로우** 지원
- **멀티모달** 처리 능력
- **프로덕션 최적화** 기능
- **클라우드 네이티브** 아키텍처

Haystack의 모듈형 아키텍처와 풍부한 컴포넌트 생태계는 복잡한 AI 애플리케이션을 효율적으로 구축할 수 있게 해줍니다.