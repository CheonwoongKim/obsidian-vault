---
title: "LlamaIndex 완전 가이드 - RAG와 데이터 연결"
type: resource
category: 개발도구/AI프레임워크
tags: [llamaindex, rag구축, 문서검색, 데이터연결, 파이썬]
status: active
date: 2025-09-24
updated: 2025-09-24
source: ["LlamaIndex 공식 문서", "실무 RAG 프로젝트 경험", "2025년 최신 업데이트"]
---

## 🔗 관련 가이드

### AI 프레임워크 시리즈
- **[[프레임워크] LangChain]]** - 종합 AI 애플리케이션 프레임워크
- **[프레임워크] LlamaIndex 완전 가이드 - RAG와 데이터 연결** ← **현재 가이드**
- **[[프레임워크] Haystack]]** - 엔터프라이즈 RAG 솔루션
- **[[프레임워크] DSPy]]** - 프롬프트 최적화 프레임워크

### 멀티 에이전트 프레임워크
- **[[프레임워크] AutoGen]]** - 대화형 멀티 에이전트 시스템
- **[[프레임워크] CrewAI]]** - 역할 기반 작업 분담 시스템
- **[[프레임워크] AgentScope]]** - 대규모 멀티 에이전트 플랫폼

### RAG 시스템 가이드
- **[[프롬프트] 11 Retrieval Augmented Generation (RAG) 프롬프팅]]** - RAG 프롬프팅 기법
- **[[[RAG] 01 문서 파싱(Document Parsing) 완전 가이드]]** - 문서 전처리 및 파싱
- **[[[RAG] 02 청킹(Chunking) 전략 가이드]]** - 효과적인 문서 분할
- **[[[RAG] 03 임베딩(Embedding) 최적화 가이드]]** - 벡터 임베딩 모델 선택
- **[[[RAG] 04 리트리버(Retriever) 최적화 가이드]]** - 검색 시스템 성능 개선
- **[[[RAG] 05 평가 및 모니터링 가이드]]** - RAG 성능 측정 및 모니터링

### 프롬프트 엔지니어링
- **[[프롬프트 엔지니어링 - 마스터 가이드]]** - 전체 프롬프팅 기법 개요

---

## 1. LlamaIndex 개요

**LlamaIndex**(구 GPT Index)는 LLM과 외부 데이터를 연결하는 데 특화된 프레임워크입니다. RAG(Retrieval-Augmented Generation) 시스템 구축의 사실상 표준으로 자리잡고 있습니다.

### 1.1. 핵심 특징

- **데이터 연결**: 다양한 데이터 소스와 LLM 연결
- **유연한 인덱싱**: 벡터, 키워드, 그래프 등 다양한 인덱스
- **고급 검색**: 하이브리드 검색, 재순위, 필터링
- **에이전트 워크플로우**: RAG 기반 에이전트 시스템
- **확장성**: 대규모 데이터셋 처리

### 1.2. 2025년 주요 업데이트

- **Workflows**: 복잡한 멀티 스텝 RAG 파이프라인
- **Multi-Modal**: 텍스트, 이미지, 오디오 통합 처리
- **Production Tools**: 모니터링, 평가, 배포 도구
- **Advanced Indexing**: 그래프 RAG, 계층적 검색

---

## 2. 설치 및 환경 설정

### 2.1. 기본 설치

```bash
# 가상 환경 생성
python -m venv llamaindex_env
source llamaindex_env/bin/activate  # macOS/Linux
# llamaindex_env\Scripts\activate  # Windows

# 기본 LlamaIndex 설치
pip install llama-index

# 주요 통합 패키지
pip install llama-index-llms-openai      # OpenAI 통합
pip install llama-index-llms-anthropic   # Claude 통합
pip install llama-index-llms-ollama      # Ollama 통합
pip install llama-index-embeddings-openai # OpenAI 임베딩

# 벡터 데이터베이스
pip install llama-index-vector-stores-chroma    # Chroma
pip install llama-index-vector-stores-pinecone  # Pinecone
pip install llama-index-vector-stores-qdrant    # Qdrant

# 문서 로더
pip install llama-index-readers-file    # 파일 리더
pip install llama-index-readers-web     # 웹 리더
pip install llama-index-readers-database # DB 리더
```

### 2.2. 환경 변수 설정

**.env 파일:**
```env
# LLM APIs
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_claude_key_here

# Vector Databases
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_environment

QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_key

# Other Services
COHERE_API_KEY=your_cohere_key  # 리랭킹용
HUGGINGFACE_API_TOKEN=your_hf_token
```

### 2.3. 기본 설정

```python
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 기본 설정
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# LLM 설정
Settings.llm = OpenAI(
    model="gpt-4",
    temperature=0.1,
    max_tokens=1000
)

# 임베딩 모델 설정
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-ada-002"
)

# 청크 크기 설정
Settings.chunk_size = 1024
Settings.chunk_overlap = 200
```

---

## 3. 기본 사용법

### 3.1. 간단한 RAG 시스템

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 1. 문서 로드
documents = SimpleDirectoryReader("./data").load_data()
print(f"로드된 문서 수: {len(documents)}")

# 2. 인덱스 생성
index = VectorStoreIndex.from_documents(documents)

# 3. 쿼리 엔진 생성
query_engine = index.as_query_engine(
    similarity_top_k=3,  # 상위 3개 문서 검색
    response_mode="compact"  # 응답 모드
)

# 4. 질문 및 답변
response = query_engine.query("주요 내용을 요약해주세요")
print(response)

# 소스 정보 확인
for node in response.source_nodes:
    print(f"점수: {node.score:.3f}")
    print(f"내용: {node.text[:200]}...")
    print("---")
```

### 3.2. 커스텀 프롬프트

```python
from llama_index.core import PromptTemplate

# 커스텀 QA 프롬프트
qa_prompt_tmpl = """
당신은 전문적인 AI 어시스턴트입니다.

컨텍스트 정보:
{context_str}

질문: {query_str}

답변 규칙:
1. 제공된 컨텍스트만을 기반으로 답변하세요
2. 확실하지 않은 내용은 "제공된 정보로는 확실하지 않습니다"라고 명시하세요
3. 답변은 한국어로 작성하고 구체적인 예시를 포함하세요
4. 출처가 되는 문서나 섹션을 언급하세요

답변:
"""

qa_prompt = PromptTemplate(qa_prompt_tmpl)

# 프롬프트 적용
query_engine = index.as_query_engine(
    text_qa_template=qa_prompt,
    similarity_top_k=5
)

response = query_engine.query("기술 스펙에 대해 설명해주세요")
print(response)
```

### 3.3. 다양한 데이터 소스 연결

```python
from llama_index.readers.file import PyMuPDFReader
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import Document

# PDF 문서 로드
pdf_reader = PyMuPDFReader()
pdf_documents = pdf_reader.load_data("./documents/manual.pdf")

# 웹페이지 로드
web_reader = SimpleWebPageReader()
web_documents = web_reader.load_data([
    "https://example.com/article1",
    "https://example.com/article2"
])

# 텍스트 직접 생성
text_documents = [
    Document(text="사용자 매뉴얼: 이 제품은..."),
    Document(text="기술 사양: 주요 기능은...")
]

# 모든 문서 통합
all_documents = pdf_documents + web_documents + text_documents

# 통합 인덱스 생성
unified_index = VectorStoreIndex.from_documents(all_documents)
```

---

## 4. 고급 검색 기능

### 4.1. 하이브리드 검색 (벡터 + 키워드)

```python
from llama_index.core import VectorStoreIndex, SimpleKeywordTableIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.callbacks import CallbackManager

# 벡터 인덱스 (의미 검색)
vector_index = VectorStoreIndex.from_documents(documents)
vector_query_engine = vector_index.as_query_engine(similarity_top_k=3)

# 키워드 인덱스 (정확한 매치)
keyword_index = SimpleKeywordTableIndex.from_documents(documents)
keyword_query_engine = keyword_index.as_query_engine()

# 쿼리 엔진을 도구로 래핑
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="의미적 유사성을 기반으로 문서를 검색합니다"
)

keyword_tool = QueryEngineTool.from_defaults(
    query_engine=keyword_query_engine,
    description="정확한 키워드 매칭을 통해 문서를 검색합니다"
)

# 하이브리드 쿼리 엔진
hybrid_query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=[vector_tool, keyword_tool],
    use_async=True
)

# 복합 질의 실행
response = hybrid_query_engine.query(
    "API 키 설정 방법과 보안 권장사항에 대해 알려주세요"
)
print(response)
```

### 4.2. 재순위(Re-ranking) 활용

```python
from llama_index.postprocessor.cohere_rerank import CohereRerank

# Cohere 재순위 모델 설정
rerank = CohereRerank(
    api_key=os.getenv("COHERE_API_KEY"),
    top_n=3,  # 최종 3개 결과만 선택
    model="rerank-english-v2.0"
)

# 재순위 적용 쿼리 엔진
query_engine = index.as_query_engine(
    similarity_top_k=10,  # 먼저 10개 검색
    node_postprocessors=[rerank]  # 그 중 3개로 재순위
)

response = query_engine.query("성능 최적화 방법")
print(response)

# 재순위 점수 확인
for node in response.source_nodes:
    print(f"재순위 점수: {node.score:.3f}")
    print(f"내용: {node.text[:150]}...")
    print("---")
```

### 4.3. 필터링 및 메타데이터 검색

```python
from llama_index.core.schema import MetadataMode

# 메타데이터가 있는 문서 생성
documents_with_metadata = []
for i, doc_text in enumerate(["문서1 내용...", "문서2 내용...", "문서3 내용..."]):
    doc = Document(
        text=doc_text,
        metadata={
            "source": f"document_{i+1}.pdf",
            "category": "technical" if i % 2 == 0 else "business",
            "date": "2025-09-24",
            "author": "AI팀" if i < 2 else "비즈니스팀"
        }
    )
    documents_with_metadata.append(doc)

# 메타데이터 포함 인덱스
metadata_index = VectorStoreIndex.from_documents(documents_with_metadata)

# 필터링 쿼리
from llama_index.core.vector_stores.types import MetadataFilters, MetadataFilter

filters = MetadataFilters(
    filters=[
        MetadataFilter(key="category", value="technical"),
        MetadataFilter(key="author", value="AI팀")
    ]
)

filtered_query_engine = metadata_index.as_query_engine(
    filters=filters,
    similarity_top_k=5
)

response = filtered_query_engine.query("기술 문서에서 구현 방법을 찾아주세요")
print(response)
```

---

## 5. 고급 인덱싱 전략

### 5.1. 계층적 인덱싱

```python
from llama_index.core.indices.tree import TreeIndex
from llama_index.core.indices.summary import SummaryIndex

# 트리 인덱스 (계층적 요약)
tree_index = TreeIndex.from_documents(documents)

# 각 레벨별 쿼리 가능
tree_query_engine = tree_index.as_query_engine(
    child_branch_factor=2,  # 자식 노드 수
    response_mode="tree_summarize"
)

# 요약 인덱스
summary_index = SummaryIndex.from_documents(documents)
summary_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize"
)

# 복합 질의
hierarchical_response = tree_query_engine.query(
    "전체 문서의 핵심 내용과 세부 사항을 계층적으로 정리해주세요"
)
print(hierarchical_response)
```

### 5.2. 그래프 RAG

```python
from llama_index.core.indices.knowledge_graph import KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore

# 그래프 저장소 설정
graph_store = SimpleGraphStore()

# 지식 그래프 인덱스
kg_index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    max_triplets_per_chunk=5,  # 청크당 최대 관계 수
    include_embeddings=True
)

# 그래프 기반 쿼리
kg_query_engine = kg_index.as_query_engine(
    include_text=True,
    response_mode="tree_summarize"
)

response = kg_query_engine.query(
    "주요 개념들 간의 관계를 설명해주세요"
)
print(response)

# 그래프 시각화 (옵션)
kg_index.get_networkx_graph().nodes(data=True)
```

### 5.3. 멀티모달 인덱싱

```python
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.readers.file import ImageReader

# 멀티모달 LLM 설정
multi_modal_llm = OpenAIMultiModal(
    model="gpt-4-vision-preview",
    max_tokens=1024
)

# 이미지 로더
image_reader = ImageReader()
image_documents = image_reader.load_data("./images")

# 텍스트와 이미지 통합
combined_documents = documents + image_documents

# 멀티모달 인덱스
mm_index = MultiModalVectorStoreIndex.from_documents(
    combined_documents,
    multi_modal_llm=multi_modal_llm
)

mm_query_engine = mm_index.as_query_engine(
    similarity_top_k=3,
    multi_modal_llm=multi_modal_llm
)

# 이미지와 텍스트를 모두 고려한 질의
response = mm_query_engine.query(
    "이미지의 다이어그램과 텍스트 설명을 비교해서 설명해주세요"
)
print(response)
```

---

## 6. Workflows - 복잡한 RAG 파이프라인

### 6.1. 기본 워크플로우

```python
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step
)
from llama_index.core.llms import ChatMessage

class QueryAnalysisEvent(Event):
    query_type: str
    processed_query: str

class RetrievalEvent(Event):
    retrieved_nodes: list

class RefinementEvent(Event):
    refined_response: str

class AdvancedRAGWorkflow(Workflow):

    @step
    async def query_analysis(self, ev: StartEvent) -> QueryAnalysisEvent:
        """질의 분석 및 전처리"""
        query = ev.query

        # 질의 유형 분류
        analysis_prompt = f"""
        다음 질의를 분석하고 유형을 분류하세요:
        질의: {query}

        유형: factual, comparative, summarization, analytical
        """

        analysis_response = await Settings.llm.achat([
            ChatMessage(role="user", content=analysis_prompt)
        ])

        query_type = analysis_response.message.content.strip().lower()

        return QueryAnalysisEvent(
            query_type=query_type,
            processed_query=query
        )

    @step
    async def retrieval(self, ev: QueryAnalysisEvent) -> RetrievalEvent:
        """검색 전략 결정 및 실행"""
        query_type = ev.query_type
        query = ev.processed_query

        # 질의 유형에 따른 검색 전략
        if query_type == "factual":
            # 정확한 사실 검색
            retriever = index.as_retriever(similarity_top_k=3)
        elif query_type == "comparative":
            # 비교 분석용 다양한 검색
            retriever = index.as_retriever(similarity_top_k=8)
        elif query_type == "summarization":
            # 요약용 광범위 검색
            retriever = index.as_retriever(similarity_top_k=10)
        else:
            # 기본 검색
            retriever = index.as_retriever(similarity_top_k=5)

        nodes = await retriever.aretrieve(query)

        return RetrievalEvent(retrieved_nodes=nodes)

    @step
    async def generate_response(self, ev: RetrievalEvent) -> RefinementEvent:
        """응답 생성"""
        nodes = ev.retrieved_nodes

        # 컨텍스트 구성
        context_str = "\n\n".join([node.text for node in nodes])

        response_prompt = f"""
        컨텍스트를 바탕으로 질문에 답하세요:

        컨텍스트:
        {context_str}

        질문: {ev.processed_query}

        답변:
        """

        response = await Settings.llm.achat([
            ChatMessage(role="user", content=response_prompt)
        ])

        return RefinementEvent(refined_response=response.message.content)

    @step
    async def refine_response(self, ev: RefinementEvent) -> StopEvent:
        """응답 정제 및 검증"""
        response = ev.refined_response

        # 응답 품질 검증
        validation_prompt = f"""
        다음 응답의 품질을 평가하고 필요시 개선하세요:

        응답: {response}

        평가 기준:
        1. 정확성
        2. 완전성
        3. 명확성
        4. 관련성

        개선된 답변:
        """

        refined = await Settings.llm.achat([
            ChatMessage(role="user", content=validation_prompt)
        ])

        return StopEvent(result=refined.message.content)

# 워크플로우 실행
workflow = AdvancedRAGWorkflow(timeout=120)

async def run_advanced_query(query: str):
    result = await workflow.run(query=query)
    return result

# 사용 예시
import asyncio
result = asyncio.run(run_advanced_query(
    "데이터베이스 성능 최적화와 캐싱 전략의 차이점을 비교해주세요"
))
print(result)
```

### 6.2. 멀티 단계 추론 워크플로우

```python
class MultiStepReasoningWorkflow(Workflow):

    @step
    async def decompose_question(self, ev: StartEvent) -> QueryAnalysisEvent:
        """복잡한 질문을 하위 질문으로 분해"""
        query = ev.query

        decomposition_prompt = f"""
        다음 복잡한 질문을 3-5개의 하위 질문으로 분해하세요:

        질문: {query}

        하위 질문들:
        1.
        2.
        3.
        ...
        """

        response = await Settings.llm.achat([
            ChatMessage(role="user", content=decomposition_prompt)
        ])

        return QueryAnalysisEvent(
            query_type="multi_step",
            processed_query=response.message.content
        )

    @step
    async def answer_subquestions(self, ev: QueryAnalysisEvent) -> RetrievalEvent:
        """각 하위 질문에 대해 검색 및 답변"""
        subquestions = ev.processed_query.split('\n')
        subquestions = [q.strip() for q in subquestions if q.strip() and not q.strip().startswith('하위')]

        sub_answers = []
        for subq in subquestions:
            if subq:
                # 각 하위 질문에 대해 검색
                retriever = index.as_retriever(similarity_top_k=3)
                nodes = await retriever.aretrieve(subq)

                # 답변 생성
                context = "\n".join([node.text for node in nodes])
                answer_prompt = f"""
                컨텍스트: {context}
                질문: {subq}
                간단한 답변:
                """

                answer_response = await Settings.llm.achat([
                    ChatMessage(role="user", content=answer_prompt)
                ])

                sub_answers.append({
                    'question': subq,
                    'answer': answer_response.message.content,
                    'sources': nodes
                })

        return RetrievalEvent(retrieved_nodes=sub_answers)

    @step
    async def synthesize_final_answer(self, ev: RetrievalEvent) -> StopEvent:
        """하위 답변들을 종합하여 최종 답변 생성"""
        sub_answers = ev.retrieved_nodes

        synthesis_content = "하위 질문과 답변들:\n"
        for item in sub_answers:
            synthesis_content += f"Q: {item['question']}\nA: {item['answer']}\n\n"

        synthesis_prompt = f"""
        다음 하위 질문들과 답변들을 종합하여 원래 질문에 대한 완전한 답변을 제공하세요:

        {synthesis_content}

        원래 질문: {ev.original_query}

        종합 답변:
        """

        final_response = await Settings.llm.achat([
            ChatMessage(role="user", content=synthesis_prompt)
        ])

        return StopEvent(result=final_response.message.content)

# 복잡한 질문으로 테스트
complex_query = """
클라우드 마이그레이션 프로젝트를 진행할 때 고려해야 할 보안, 성능,
비용 측면의 주요 요소들과 각각의 모범 사례는 무엇인가요?
"""

reasoning_workflow = MultiStepReasoningWorkflow(timeout=180)
result = asyncio.run(reasoning_workflow.run(
    query=complex_query,
    original_query=complex_query
))
print(result)
```

---

## 7. 에이전트 시스템

### 7.1. RAG 기반 에이전트

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, FunctionTool

# 쿼리 엔진을 도구로 변환
query_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="document_search",
    description="기술 문서에서 정보를 검색하고 질문에 답변합니다"
)

# 계산 도구 추가
def calculate(expression: str) -> str:
    """간단한 수학 계산을 수행합니다"""
    try:
        result = eval(expression)
        return f"계산 결과: {result}"
    except Exception as e:
        return f"계산 오류: {str(e)}"

calc_tool = FunctionTool.from_defaults(
    fn=calculate,
    name="calculator",
    description="수학 계산을 수행합니다"
)

# ReAct 에이전트 생성
agent = ReActAgent.from_tools(
    tools=[query_tool, calc_tool],
    llm=Settings.llm,
    verbose=True,
    max_iterations=10
)

# 복합 질의 처리
response = agent.chat("""
기술 문서에서 서버 성능 요구사항을 찾아보고,
만약 CPU 사용률이 80%이고 메모리가 16GB라면
권장되는 최대 동시 사용자 수를 계산해주세요.
""")

print(response)
```

### 7.2. 멀티 문서 에이전트

```python
from llama_index.core.agent import OpenAIAgent
from llama_index.core import StorageContext

class MultiDocumentAgent:
    def __init__(self):
        self.indices = {}
        self.query_engines = {}
        self.tools = []

    def add_document_collection(self, name: str, documents: list, description: str):
        """문서 컬렉션 추가"""
        # 각 문서 컬렉션별로 별도 인덱스 생성
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine(similarity_top_k=3)

        self.indices[name] = index
        self.query_engines[name] = query_engine

        # 도구로 등록
        tool = QueryEngineTool.from_defaults(
            query_engine=query_engine,
            name=f"{name}_search",
            description=description
        )
        self.tools.append(tool)

    def create_agent(self):
        """멀티 도큐먼트 에이전트 생성"""
        return OpenAIAgent.from_tools(
            self.tools,
            llm=Settings.llm,
            verbose=True,
            system_prompt="""
            당신은 여러 문서 컬렉션에 접근할 수 있는 전문 어시스턴트입니다.

            작업 방식:
            1. 질문을 분석하여 어떤 문서 컬렉션이 가장 적절한지 판단
            2. 필요하면 여러 컬렉션을 검색하여 종합적인 답변 제공
            3. 출처를 명확히 표시하고 근거 제시

            답변은 정확하고 도움이 되도록 작성하세요.
            """
        )

# 사용 예시
multi_agent = MultiDocumentAgent()

# 다양한 문서 컬렉션 추가
multi_agent.add_document_collection(
    "technical_docs",
    technical_documents,
    "기술 문서, API 참조, 구현 가이드 검색"
)

multi_agent.add_document_collection(
    "business_docs",
    business_documents,
    "비즈니스 요구사항, 정책, 절차 문서 검색"
)

multi_agent.add_document_collection(
    "user_guides",
    user_guide_documents,
    "사용자 매뉴얼, 튜토리얼, FAQ 검색"
)

# 에이전트 생성 및 사용
agent = multi_agent.create_agent()

response = agent.chat("""
새로운 기능을 구현하려고 하는데,
1) 기술적 요구사항과 API 스펙을 확인하고
2) 비즈니스 정책 준수사항을 검토한 다음
3) 사용자에게 어떻게 설명할지 가이드를 작성해주세요.
""")

print(response)
```

---

## 8. 평가 및 모니터링

### 8.1. RAG 시스템 평가

```python
from llama_index.core.evaluation import (
    RelevancyEvaluator,
    FaithfulnessEvaluator,
    ContextRelevancyEvaluator
)
import pandas as pd

class RAGEvaluator:
    def __init__(self, query_engine):
        self.query_engine = query_engine

        # 평가자 설정
        self.relevancy_evaluator = RelevancyEvaluator(llm=Settings.llm)
        self.faithfulness_evaluator = FaithfulnessEvaluator(llm=Settings.llm)
        self.context_relevancy_evaluator = ContextRelevancyEvaluator(llm=Settings.llm)

    def evaluate_queries(self, test_questions: list):
        """테스트 질문들에 대한 종합 평가"""
        results = []

        for question in test_questions:
            # 응답 생성
            response = self.query_engine.query(question)

            # 관련성 평가
            relevancy_result = self.relevancy_evaluator.evaluate_response(
                query=question,
                response=response
            )

            # 충실성 평가 (환각 여부)
            faithfulness_result = self.faithfulness_evaluator.evaluate_response(
                query=question,
                response=response
            )

            # 컨텍스트 관련성 평가
            context_relevancy_result = self.context_relevancy_evaluator.evaluate_response(
                query=question,
                response=response
            )

            results.append({
                'question': question,
                'response': str(response),
                'relevancy_score': relevancy_result.score,
                'faithfulness_score': faithfulness_result.score,
                'context_relevancy_score': context_relevancy_result.score,
                'source_count': len(response.source_nodes)
            })

        return pd.DataFrame(results)

    def generate_report(self, eval_results: pd.DataFrame):
        """평가 리포트 생성"""
        report = f"""
        RAG 시스템 평가 리포트
        =====================

        전체 질문 수: {len(eval_results)}

        평균 점수:
        - 관련성: {eval_results['relevancy_score'].mean():.3f}
        - 충실성: {eval_results['faithfulness_score'].mean():.3f}
        - 컨텍스트 관련성: {eval_results['context_relevancy_score'].mean():.3f}

        성능 기준:
        - 우수 (0.8 이상): {len(eval_results[eval_results['relevancy_score'] >= 0.8])} 개
        - 양호 (0.6-0.8): {len(eval_results[(eval_results['relevancy_score'] >= 0.6) & (eval_results['relevancy_score'] < 0.8)])} 개
        - 개선 필요 (0.6 미만): {len(eval_results[eval_results['relevancy_score'] < 0.6])} 개

        개선이 필요한 질문들:
        """

        poor_questions = eval_results[eval_results['relevancy_score'] < 0.6]
        for _, row in poor_questions.iterrows():
            report += f"\n- {row['question']} (점수: {row['relevancy_score']:.3f})"

        return report

# 평가 실행
test_questions = [
    "시스템 아키텍처의 주요 구성 요소는 무엇인가요?",
    "성능 최적화 방법에 대해 설명해주세요",
    "보안 설정은 어떻게 구성하나요?",
    "데이터베이스 연결 설정 방법은?",
    "에러 처리는 어떻게 해야 하나요?"
]

evaluator = RAGEvaluator(query_engine)
eval_results = evaluator.evaluate_queries(test_questions)
report = evaluator.generate_report(eval_results)

print(report)
eval_results.to_csv('rag_evaluation_results.csv', index=False)
```

### 8.2. 성능 모니터링

```python
import time
import psutil
from functools import wraps

class RAGPerformanceMonitor:
    def __init__(self):
        self.metrics = []

    def monitor_query(self, func):
        """쿼리 성능 모니터링 데코레이터"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

            try:
                result = func(*args, **kwargs)
                status = "success"
                error = None
            except Exception as e:
                result = None
                status = "error"
                error = str(e)

            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

            metrics = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration_seconds': end_time - start_time,
                'memory_used_mb': end_memory - start_memory,
                'status': status,
                'error': error,
                'query': str(args[0]) if args else "N/A"
            }

            self.metrics.append(metrics)
            return result

        return wrapper

    def get_performance_stats(self):
        """성능 통계 계산"""
        if not self.metrics:
            return "성능 데이터가 없습니다."

        df = pd.DataFrame(self.metrics)
        successful_queries = df[df['status'] == 'success']

        stats = {
            'total_queries': len(df),
            'successful_queries': len(successful_queries),
            'error_rate': len(df[df['status'] == 'error']) / len(df),
            'avg_response_time': successful_queries['duration_seconds'].mean(),
            'p95_response_time': successful_queries['duration_seconds'].quantile(0.95),
            'avg_memory_usage': successful_queries['memory_used_mb'].mean()
        }

        return stats

# 모니터링 적용
monitor = RAGPerformanceMonitor()

@monitor.monitor_query
def monitored_query(question):
    return query_engine.query(question)

# 테스트 쿼리 실행
test_queries = [
    "API 문서에서 인증 방법을 설명해주세요",
    "성능 튜닝 가이드라인은 무엇인가요",
    "에러 로그 분석 방법을 알려주세요"
]

for query in test_queries:
    result = monitored_query(query)
    print(f"Query: {query[:50]}...")
    print(f"Response: {str(result)[:100]}...\n")

# 성능 통계 출력
stats = monitor.get_performance_stats()
print("성능 통계:")
for key, value in stats.items():
    print(f"- {key}: {value}")
```

---

## 9. 프로덕션 배포

### 9.1. FastAPI 서버

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="LlamaIndex RAG API", version="1.0.0")

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3
    include_sources: bool = True

class QueryResponse(BaseModel):
    answer: str
    sources: list = []
    confidence: float = 0.0
    response_time: float = 0.0

# 전역 인덱스 (시작 시 로드)
global_index = None
global_query_engine = None

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 인덱스 로드"""
    global global_index, global_query_engine

    print("인덱스 로딩 중...")
    documents = SimpleDirectoryReader("./data").load_data()
    global_index = VectorStoreIndex.from_documents(documents)
    global_query_engine = global_index.as_query_engine()
    print("인덱스 로딩 완료!")

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """문서 질의 엔드포인트"""
    if not global_query_engine:
        raise HTTPException(status_code=500, detail="인덱스가 준비되지 않았습니다")

    try:
        start_time = time.time()

        # 쿼리 실행
        response = global_query_engine.query(request.question)

        end_time = time.time()
        response_time = end_time - start_time

        # 응답 구성
        sources = []
        if request.include_sources:
            sources = [
                {
                    "text": node.text[:200] + "...",
                    "score": node.score,
                    "metadata": node.metadata
                }
                for node in response.source_nodes
            ]

        return QueryResponse(
            answer=str(response),
            sources=sources,
            confidence=0.85,  # 실제로는 계산된 신뢰도
            response_time=response_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "index_ready": global_index is not None}

@app.get("/stats")
async def get_stats():
    """시스템 통계"""
    if not global_index:
        return {"error": "인덱스가 준비되지 않았습니다"}

    return {
        "document_count": len(global_index.docstore.docs),
        "index_type": "VectorStoreIndex",
        "embedding_model": "text-embedding-ada-002"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 9.2. Docker 배포

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 데이터 디렉토리 생성
RUN mkdir -p /app/data

# 포트 노출
EXPOSE 8000

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  rag-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./data:/app/data:ro
      - ./logs:/app/logs
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

volumes:
  redis_data:
  qdrant_data:
```

---

## 10. 베스트 프랙티스

### 10.1. 데이터 전처리

```python
import re
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import SummaryExtractor, QuestionsAnsweredExtractor

class AdvancedDocumentProcessor:
    def __init__(self):
        self.sentence_splitter = SentenceSplitter(
            chunk_size=1024,
            chunk_overlap=200,
            paragraph_separator="\n\n",
            secondary_chunking_regex="[.!?]+"
        )

        # 메타데이터 추출기
        self.summary_extractor = SummaryExtractor(
            summaries=["prev", "self", "next"],
            llm=Settings.llm
        )

        self.questions_extractor = QuestionsAnsweredExtractor(
            questions=3,
            llm=Settings.llm
        )

    def clean_text(self, text: str) -> str:
        """텍스트 정제"""
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)

        # 여러 공백을 단일 공백으로
        text = re.sub(r'\s+', ' ', text)

        # 특수 문자 정리
        text = re.sub(r'[^\w\s가-힣.,!?()-]', '', text)

        return text.strip()

    def process_documents(self, documents: list):
        """문서 전처리 및 청킹"""
        processed_docs = []

        for doc in documents:
            # 텍스트 정제
            clean_text = self.clean_text(doc.text)
            doc.text = clean_text

            processed_docs.append(doc)

        # 청킹
        nodes = self.sentence_splitter.get_nodes_from_documents(processed_docs)

        # 메타데이터 추출
        nodes = self.summary_extractor.extract(nodes)
        nodes = self.questions_extractor.extract(nodes)

        return nodes

# 사용 예시
processor = AdvancedDocumentProcessor()
processed_nodes = processor.process_documents(documents)

# 처리된 노드로 인덱스 생성
processed_index = VectorStoreIndex(processed_nodes)
```

### 10.2. 캐싱 전략

```python
import redis
import pickle
import hashlib
from typing import Optional

class RAGCache:
    def __init__(self, redis_host='localhost', redis_port=6379, ttl=3600):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=False)
        self.ttl = ttl  # 캐시 TTL (초)

    def _get_cache_key(self, query: str, top_k: int = 3) -> str:
        """쿼리 기반 캐시 키 생성"""
        key_string = f"{query}_{top_k}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def get_cached_response(self, query: str, top_k: int = 3) -> Optional[str]:
        """캐시된 응답 조회"""
        cache_key = self._get_cache_key(query, top_k)

        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                return pickle.loads(cached_data)
        except Exception as e:
            print(f"캐시 조회 오류: {e}")

        return None

    def cache_response(self, query: str, response: str, top_k: int = 3):
        """응답 캐싱"""
        cache_key = self._get_cache_key(query, top_k)

        try:
            cached_data = pickle.dumps(response)
            self.redis_client.setex(cache_key, self.ttl, cached_data)
        except Exception as e:
            print(f"캐시 저장 오류: {e}")

class CachedQueryEngine:
    def __init__(self, query_engine, cache: RAGCache):
        self.query_engine = query_engine
        self.cache = cache

    def query(self, query_str: str):
        """캐시를 활용한 쿼리 실행"""
        # 캐시 조회
        cached_response = self.cache.get_cached_response(query_str)
        if cached_response:
            print("캐시된 응답 반환")
            return cached_response

        # 새로운 쿼리 실행
        print("새로운 쿼리 실행")
        response = self.query_engine.query(query_str)

        # 결과 캐싱
        self.cache.cache_response(query_str, response)

        return response

# 사용 예시
cache = RAGCache(ttl=1800)  # 30분 캐시
cached_engine = CachedQueryEngine(query_engine, cache)

response1 = cached_engine.query("시스템 아키텍처 설명")  # 새로운 쿼리
response2 = cached_engine.query("시스템 아키텍처 설명")  # 캐시된 응답
```

---

## 11. 참고 자료

### 11.1. 공식 문서
- **LlamaIndex 공식 사이트**: https://www.llamaindex.ai/
- **GitHub**: https://github.com/run-llama/llama_index
- **문서**: https://docs.llamaindex.ai/

### 11.2. 커뮤니티
- **Discord**: LlamaIndex Community
- **Twitter**: @llama_index
- **논문**: RAG, 검색 증강 생성 관련 연구

### 11.3. 관련 도구
- **LlamaHub**: https://llamahub.ai/ - 데이터 로더 허브
- **LlamaCloud**: 클라우드 기반 RAG 서비스
- **Vector Databases**: Pinecone, Qdrant, Chroma, Weaviate

---

## 12. 체크리스트

**기본 설정:**
- [ ] Python 3.8+ 환경 준비
- [ ] LlamaIndex 설치 및 의존성 구성
- [ ] LLM 및 임베딩 API 키 설정
- [ ] 기본 RAG 시스템 구축 테스트

**고급 기능:**
- [ ] 하이브리드 검색 (벡터 + 키워드) 구현
- [ ] 재순위 및 필터링 적용
- [ ] 메타데이터 활용 검색 시스템
- [ ] 계층적/그래프 인덱싱 테스트

**워크플로우:**
- [ ] 기본 Workflow 구성
- [ ] 멀티 단계 추론 워크플로우
- [ ] 조건부 분기 로직 구현
- [ ] 에이전트 시스템 통합

**프로덕션:**
- [ ] 성능 평가 시스템 구축
- [ ] 모니터링 및 로깅 구현
- [ ] 캐싱 전략 적용
- [ ] API 서버 배포

**2025년 9월 기준 최신 LlamaIndex 기능과 RAG 베스트 프랙티스를 반영한 종합 가이드입니다.**