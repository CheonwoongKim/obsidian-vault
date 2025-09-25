---
title: "RAG - 평가 및 모니터링 가이드"
type: reference
category: AI/RAG
tags: [RAG, 평가, RAGAS, 모니터링, 메트릭]
date: 2025-09-24
updated: 2025-09-24
source: "기존 종합 가이드 재구성"
status: active
---

## 🔗 관련 가이드

### RAG 시스템 전체 가이드 시리즈
1. **[[[RAG] 01 문서 파싱(Document Parsing) 완전 가이드]]** - 문서 전처리 및 파싱 기법
2. **[[[RAG] 02 청킹(Chunking) 전략 가이드]]** - 효과적인 문서 분할 방법론
3. **[[[RAG] 03 임베딩(Embedding) 최적화 가이드]]** - 벡터 임베딩 모델 선택 및 튜닝
4. **[[[RAG] 04 리트리버(Retriever) 최적화 가이드]]** - 검색 시스템 성능 개선
5. **[[프롬프트] 11 Retrieval Augmented Generation (RAG) 프롬프팅]]** - RAG 프롬프팅 기법
6. **RAG - 평가 및 모니터링 가이드** ← **현재 가이드**

### 추가 참고 가이드
- **[[프롬프트 엔지니어링 - 마스터 가이드]]** - 전체 프롬프팅 기법 개요
- **[[LangChain 완전 가이드 - 설치와 활용법]]** - RAG 구현 프레임워크
- **[[LlamaIndex 완전 가이드 - RAG와 데이터 연결]]** - RAG 특화 프레임워크
- **[[Haystack 완전 가이드 - RAG 및 검색 시스템]]** - 엔터프라이즈 RAG 솔루션

---

# 평가 및 모니터링 가이드

“개선했는가?”를 수치로 증명하기 위한 가이드입니다. 오프라인/온라인 모두 다룹니다.

## 0. 환경 준비(설치)
```bash
pip install --upgrade ragas datasets sentence-transformers scikit-learn
```

도구 설명(간단)
- ragas: RAG 품질을 계량화하는 평가 라이브러리(충실도/관련성/정밀/재현)
- datasets: 평가용 데이터셋을 구조화해 다루는 유틸
- sentence-transformers: 임베딩 기반 보완 지표(의미적 유사도) 계산에 사용
- scikit-learn: ROC/PR 등 보조 평가와 통계 유틸

### 5분 완성 RAG 평가 시스템 구축 (사업적 필수)
**상황**: RAG 시스템을 만들었으나 성능을 수치로 증명할 방법이 없음

```python
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness, context_recall, context_precision
from datasets import Dataset
import pandas as pd

def setup_rag_evaluation(rag_pipeline, test_dataset_path):
    """5분이면 완성되는 RAG 평가 시스템"""
    print("RAG 평가 시스템 구축 시작...")

    # Step 1: 평가 데이터 로드
    df = pd.read_csv(test_dataset_path)  # columns: question, ground_truth
    print(f"✓ 평가 데이터 로드: {len(df)}개 샘플")

    # Step 2: RAG 시스템으로 답변 생성
    results = []
    for _, row in df.iterrows():
        response = rag_pipeline.invoke({"question": row['question']})
        results.append({
            'question': row['question'],
            'answer': response['answer'],
            'contexts': [doc.page_content for doc in response['context']],
            'ground_truth': row['ground_truth']
        })
    print("✓ RAG 시스템 응답 생성 완료")

    # Step 3: RAGAS 평가 실행
    dataset = Dataset.from_list(results)
    evaluation_result = evaluate(
        dataset,
        metrics=[context_precision, context_recall, faithfulness, answer_relevancy]
    )
    print("✓ RAGAS 평가 완료")

    # Step 4: 결과 대시보드 표시
    print("\n=== RAG 성능 리포트 ===")
    for metric, score in evaluation_result.items():
        status = "✓ 우수" if score > 0.8 else "⚠ 개선필요" if score > 0.6 else "❌ 심각"
        print(f"{metric}: {score:.3f} {status}")

    return evaluation_result

# 사용 예시
eval_result = setup_rag_evaluation(your_rag_pipeline, "test_qa_pairs.csv")

# 알림 기준 설정
if eval_result['faithfulness'] < 0.7:
    print("⚠ 경고: 충실도가 낮습니다. 리랭킹 강화 및 컨텍스트 필터링 검토 필요")
```

**예상 결과 해석**:
- 충실도 0.8+ → 답변이 컨텍스트에 사실적으로 근거
- 답변 관련성 0.8+ → 질문에 정확하게 대답
- 컨텍스트 정밀도 0.8+ → 검색된 문서가 관련성 높음

## 1. 핵심 지표(RAGAS)와 보완 지표
- 충실도(Faithfulness): 답변 ↔ 컨텍스트 일치도
- 답변 관련성(Answer Relevancy): 답변 ↔ 질문 일치도
- 컨텍스트 정밀도(Context Precision): 상위 컨텍스트의 관련성 비율
- 컨텍스트 재현율(Context Recall): 필요한 정보의 검색 누락 여부
- (보완) 사용자 피드백 점수, 클릭/채택률, 에스컬레이션 비율

## 2. 오프라인 평가(파이프라인 변경 전)
데이터셋 스키마(예)
```json
{
  "question": "...",
  "contexts": ["...","..."],
  "answer": "생성된 답변",
  "ground_truth": "참조 정답"
}
```

RAGAS 실행 스니펫
```python
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness, context_recall, context_precision

result = evaluate(dataset, metrics=[context_precision, context_recall, faithfulness, answer_relevancy])
print("precision=", result["context_precision"], "recall=", result["context_recall"])
```

주의
- RAGAS 지표는 서로 보완적입니다. 하나만 올라도 전체 품질이 상승하지 않을 수 있습니다.
- 지표가 개선되어도 응답 지연이 늘면 사용자 체감 품질은 악화될 수 있습니다.

의미적 유사도(보완 지표)
```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('all-MiniLM-L6-v2')
def semantic_sim(a,b):
    e = model.encode([a,b]); return float(cosine_similarity([e[0]],[e[1]])[0][0])
```

## 3. 온라인 모니터링(배포 후)
- 지표 대시보드: 응답시간, 오류율, 컨텍스트/답변 길이, 상기 품질 지표(샘플링)
- 알림: 임계값(예: 평균 응답시간>5s, 충실도<0.7) 초과 시 Slack/메일 알림
- 프라이버시: 로그 마스킹, 보존기간(30/90/180일), 접근 제어

간단 로깅 스니펫
```python
def track(query, answer, context, t):
  log = {"q":query, "a_len":len(answer), "c_len":len(context), "latency":t}
  print(log)  # 실제로는 로그 수집기로 전송
```

## 4. 실험 설계(A/B)
- 단일 변수 변경(예: 오버랩 10%→20%) → 최소 200–500케이스 샘플 → 통계검정
- 목표/가설/중지 기준(지표 역전/지연 초과) 명시

## 5. 운영 엑셀런스 체크리스트

### 평가 데이터 품질 관리
- [ ] **골든 데이터셋 유지**: 최소 200개 이상, 월 1회 업데이트
- [ ] **다양성 보장**: 도메인별/난이도별 균등 분포 (20% easy, 60% medium, 20% hard)
- [ ] **정답 라벨 검수**: 전문가 2명 이상 교차 검증
- [ ] **실제 사용자 쿼리 반영**: 월간 Top 20 실제 질문 추가

### 성능 모니터링 운영
- [ ] **일간 자동 평가**: RAGAS 4지표 + 응답시간 자동 측정
- [ ] **알림 기준 설정**: 충실도 <0.7, 응답시간 >3초 시 Slack 알림
- [ ] **주간 트렌드 분석**: 7일 이동평균으로 성능 추세 모니터링
- [ ] **월간 비교 리포트**: 전월 대비 개선/악화 지표 요약

### A/B 테스트 체계
- [ ] **실험 설계 테플릿**: 가설-메트릭-성공기준-위험도 명시
- [ ] **실험 로그 보존**: 변경사항, 성능 데이터, 롱백 절차 90일 보관
- [ ] **통계적 유의성 검증**: 최소 샘플 384개/그룹 (95% 신뢰구간)
- [ ] **땡백 계획**: 성능 악화 시 15분 내 이전 버전 복원 가능

### 비즈니스 연계
- [ ] **ROI 계산**: 성능 개선 → 사용자 만족도 → 비즈니스 영향 수치화
- [ ] **사용자 피드백 연계**: 5점 척도 + 정성적 피드백 수집 체계
- [ ] **경쟁사 벤치마크**: 동일 데이터셋으로 경쟁 서비스 성능 비교
- [ ] **비용 효율성**: 성능 단위당 인프라/운영 비용 추적

### 비상 체계 (중요도 최고)
- [ ] **성능 저하 대응**: 충실도 0.6 미만 시 30분 내 원인 분석 완료
- [ ] **서비스 장애 대응**: 평가 시스템 다운 시 수동 모니터링 전환
- [ ] **단계별 롤백**: 개별 컴포넌트 단위 롤백 후 전체 파이프라인 롤백
- [ ] **상에서 운영진 대기**: 주요 성능 지표 악화 시 24/7 대응 체계

### 성능 문제 진단 및 즉시 해결책

**가장 흔한 4대 문제와 해결 로드맵**

#### 문제 1: 충실도 낮음 (faithfulness < 0.7)
```
증상: 답변이 검색된 문서와 다른 내용 포함
원인: 리트리버가 관련성 낮은 문서 반환 또는 LLM 할루시네이션

즉시 해결책 (1시간 내):
1. 리랭커 임계값 높여서 Top-3만 사용
2. 프롬프트에 "컨텍스트에만 근거하여 답변" 지시 강화
3. 핵심 정보 누락 방지용 컨텍스트 처리 크기 증가

근본 해결책 (1주일):
- 하이브리드 검색 가중치 재튜닝
- 청킹 전략 개선 (더 긴 컨텍스트 반영)
- LLM 모델 업그레이드 검토
```

#### 문제 2: 답변 관련성 낮음 (answer_relevancy < 0.7)
```
증상: 질문에 대한 직접적 답변 대신 일반적/부정확 답변
원인: 1) 쿼리 모호성, 2) 검색 품질 문제, 3) LLM 이해도 부족

즉시 해결책:
1. 쿼리 재작성 및 의도 명확화 가이드 제공
2. 검색 범위 확대 (Top-k 5✔3, 메타데이터 필터 완화)
3. Few-shot 프롬프트로 답변 양식 예시 제공

중기 해결책:
- 셀프 쿼리 기능 도입 (사용자 질문 의도 파악)
- 도메인 특화 파인튜닝된 임베딩 모델 도입
```

#### 문제 3: 컨텍스트 정밀도 낮음 (context_precision < 0.6)
```
증상: 검색 결과에 관련없는 문서 많이 포함
원인: 검색 노이즈 과다, BM25 오버피팅, 메타데이터 필터 미적용

즉시 해결책:
1. 메타데이터 필터로 검색 범위 30-50% 축소
2. 리랭커 강화 (크로스 인코더 적용)
3. 하이브리드 가중치에서 벡터 비중 증가

예방 전략:
- 청킹 전략 개선으로 노이즈 초기 차단
- 상품/서비스별 전용 인덱스 구축
```

#### 문제 4: 컨텍스트 재현율 낮음 (context_recall < 0.6)
```
증상: 질문에 답하기 위해 필요한 정보를 찾지 못함
원인: Top-k 부족, 청킹 과도한 분할, 오버랩 부족

즉시 해결책:
1. Top-k를 5에서 10으로 증가
2. 청킹 오버랩 10%에서 20%로 증가
3. 검색 거리 임계값 완화 (threshold 하향)

장기 해결책:
- Parent Document Retriever 도입 (작은 청크로 검색, 큰 문서로 응답)
- 계층적 검색 전략 (coarse-to-fine)
```

### 성능 개선 우선순위
1. **충실도 문제** → 비즈니스 영향 가장 큼 (30분 내 해결 필수)
2. **컨텍스트 정밀도** → 사용자 경험 직결 (1시간 내)
3. **답변 관련성** → 만족도 직결 (1일 내)
4. **컨텍스트 재현율** → 완성도 개선 (1주 내)

---

## 6. RAGAS 외 보완 평가 도구

도구를 병행하면 지표 신뢰도가 높아집니다.

### 6.1 TruLens (trulens-eval)
- 특징: Groundedness/관련성 등 LLM·임베딩 기반 피드백 + 대시보드
- 설치: `pip install trulens-eval`
- 예시(개념)
```python
from trulens_eval import Tru, Feedback
tru = Tru()
fb = Feedback(provider="openai", feedback_type="groundedness")
tru.run_feedback_functions(feedback_functions=[fb])
```

### 6.2 DeepEval
- 특징: Hallucination/Faithfulness/Answer Relevancy 등 RAG 지표 제공
- 설치: `pip install deepeval`
- 예시(개념)
```python
from deepeval.metrics import FaithfulnessMetric
metric = FaithfulnessMetric()
score = metric.measure(prediction="답변", references=["컨텍스트"], input="질문")
```

### 6.3 LangChain Evaluators / LangSmith Evals
- 특징: criteria/LLM-as-judge/유사도 기반 평가기. LangSmith로 실험 관리
- 설치: `pip install langchain langsmith`
- 예시
```python
from langchain.evaluation import load_evaluator
evaluator = load_evaluator("criteria", criteria="conciseness,coherence,groundedness")
res = evaluator.evaluate_strings(prediction="답변", input="질문", reference="컨텍스트")
```

### 6.4 LlamaIndex Evaluation
- 특징: Hallucination/Faithfulness 등 제공, LlamaIndex 파이프라인에 적합
- 설치: `pip install llama-index`
- 예시(개념)
```python
from llama_index.core.evaluation import FaithfulnessEvaluator
ev = FaithfulnessEvaluator()
score = ev.evaluate(response="답변", contexts=["컨텍스트"]).score
```

### 6.5 promptfoo (CLI 기반 리그레션 테스트)
- 특징: YAML 테스트 케이스 정의 → CLI 일괄 평가/리포트
- 설치: `npm i -g promptfoo`
- 예시
```bash
promptfoo init
promptfoo eval
```

## 부록 A. 용어 빠른 이해
- 충실도(Faithfulness): 답변이 컨텍스트에 사실적으로 근거하는 정도
- 답변 관련성(Answer Relevancy): 답변이 질문 의도와 맞는 정도
- 컨텍스트 정밀/재현(Context Precision/Recall): 검색된 컨텍스트의 정확성/누락 없음
- A/B 테스트: 두 설정을 동시 운영해 통계적으로 우월한 쪽을 선택하는 방법
- 임계값(Threshold): 알림 또는 롤백을 트리거하는 기준값
