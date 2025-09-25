---
title: "RAG - 문서 파싱(Document Parsing) 완전 가이드"
type: reference
category: AI/RAG
tags: [RAG, 문서파싱, parser, PDF, Word, Excel, OCR]
date: 2025-09-24
updated: 2025-09-24
source: "실무 경험 기반 종합 가이드"
status: active
---

# 문서 파싱(Document Parsing) 완전 가이드

문서 파싱은 RAG 시스템의 첫 관문입니다. "쓰레기가 들어가면 쓰레기가 나온다(GIGO)" - 아무리 좋은 임베딩과 검색기를 써도 파싱이 잘못되면 전체 시스템이 무용지물이 됩니다.

## 🔗 관련 가이드

### RAG 시스템 전체 가이드 시리즈
1. **RAG - 문서 파싱(Document Parsing) 완전 가이드** ← **현재 가이드**
2. **[[[RAG] 02 청킹(Chunking) 전략 가이드]]** - 효과적인 문서 분할 방법론
3. **[[[RAG] 03 임베딩(Embedding) 최적화 가이드]]** - 벡터 임베딩 모델 선택 및 튜닝
4. **[[[RAG] 04 리트리버(Retriever) 최적화 가이드]]** - 검색 시스템 성능 개선
5. **[[프롬프트] 11 Retrieval Augmented Generation (RAG) 프롬프팅]]** - RAG 프롬프팅 기법
6. **[[[RAG] 05 평가 및 모니터링 가이드]]** - RAG 성능 측정 및 운영 모니터링

### 추가 참고 가이드
- **[[프롬프트 엔지니어링 - 마스터 가이드]]** - 전체 프롬프팅 기법 개요
- **[[LangChain 완전 가이드 - 설치와 활용법]]** - RAG 구현 프레임워크
- **[[LlamaIndex 완전 가이드 - RAG와 데이터 연결]]** - RAG 특화 프레임워크
- **[[Haystack 완전 가이드 - RAG 및 검색 시스템]]** - 엔터프라이즈 RAG 솔루션
5. **📊 평가 및 모니터링**: [[[RAG] 05 평가 및 모니터링 가이드]]

**💡 추가 참고**: [[프롬프트] 98 마스터 가이드]] | [[프레임워크] LlamaIndex]]

## 0. 📍 시작하기 전에: 내게 맞는 파서 찾기

### 🤔 어떤 파서를 선택해야 할까요?

**30초 진단으로 최적 파서 찾기:**

```python
def recommend_parser(file_type: str, budget: str, document_language: str, special_needs: list = None) -> str:
    """30초 파서 추천 시스템"""

    # 1단계: 언어별 최우선 추천
    if document_language == '한국어':
        return "🎯 Upstage Layout Analysis (한국어 특화 최강)"

    # 2단계: 예산별 추천
    if budget == '무료만':
        if file_type == 'PDF':
            return "📄 Basic PDF Parser + Robust PDF Parser"
        elif file_type in ['Word', 'Excel']:
            return "📊 Basic Document Parser"
        else:
            return "👁️ EasyOCR (이미지/스캔 문서)"

    # 3단계: 특수 요구사항 고려
    special_needs = special_needs or []
    if '표가 많음' in special_needs:
        return "🔢 AWS Textract 또는 Advanced Table Parser"
    elif '손상된 문서' in special_needs:
        return "🛠️ Robust PDF Parser"
    elif '높은 정확도 필요' in special_needs:
        return "⭐ Azure Document Intelligence"

    # 4단계: 일반적 추천
    return "🎯 Azure Document Intelligence (가성비 최고)"

# 사용 예시
print(recommend_parser('PDF', '월 10만원 이하', '한국어', ['표가 많음']))
# 결과: 🎯 Upstage Layout Analysis (한국어 특화 최강)
```

### 📊 빠른 선택 매트릭스

| 내 상황 | 추천 파서 | 이유 |
|---------|-----------|------|
| **"한국어 문서가 대부분"** | Upstage Layout Analysis | 한국어 최적화, 높은 정확도 |
| **"예산이 없어요"** | Basic Parser + EasyOCR | 무료, 기본 기능 충분 |
| **"표/차트가 많아요"** | AWS Textract | 표 구조 인식 최강 |
| **"최고 품질 필요"** | Claude Vision | AI 이해력 최고 |
| **"빠른 처리 중요"** | Basic PDF Parser | 속도 우선 |
| **"손상된 문서들"** | Robust PDF Parser | 복구 기능 특화 |

### 🚀 추천 시작 경로

#### 경로 1: 🇰🇷 **한국어 문서 중심**
```bash
# 1. Upstage API 키 발급 (https://console.upstage.ai/)
# 2. 필수 패키지 설치
pip install requests pillow

# 3. 바로 사용
upstage_parser = UpstageParser(api_key="your-key")
result = upstage_parser.parse_with_quality_check("문서.pdf")
```

#### 경로 2: 💰 **무료 솔루션**
```bash
# 1. 무료 패키지 설치
pip install pypdf2 python-docx openpyxl easyocr

# 2. 바로 사용
parser = UniversalDocumentParser()
result = parser.parse_document("문서.pdf")
```

#### 경로 3: 🏢 **엔터프라이즈급**
```bash
# 1. Azure/AWS 계정 설정
# 2. 프리미엄 패키지 설치
pip install azure-ai-formrecognizer boto3

# 3. 통합 파서 사용
ultimate_parser = UltimateParserSelector()
result = ultimate_parser.auto_parse_ultimate("문서.pdf", budget='high')
```

---

## 1. 환경 준비 (선택한 파서에 따라)

### 패키지 설치 (선택한 파서에 따라 필요한 것만)

#### 🆓 **무료 솔루션 패키지**
```bash
# 기본 파싱 (PDF, Word, Excel)
pip install --upgrade pypdf2 python-docx openpyxl pandas

# OCR 기능 (이미지/스캔 문서)
pip install --upgrade easyocr pillow

# PDF 복구 기능
pip install --upgrade fitz PyMuPDF pikepdf pdfminer.six

# 고급 테이블 파싱
pip install --upgrade camelot-py[cv] tabula-py
```

#### 💰 **클라우드 API 솔루션**
```bash
# Upstage (한국어 특화)
pip install --upgrade requests

# Azure Document Intelligence
pip install --upgrade azure-ai-formrecognizer

# Google Document AI
pip install --upgrade google-cloud-documentai

# AWS Textract
pip install --upgrade boto3

# Claude Vision
pip install --upgrade anthropic
```

#### 🏢 **전체 통합 설치 (모든 파서)**
```bash
# 한 번에 모든 패키지 설치 (개발/테스트용)
pip install --upgrade pypdf2 python-docx openpyxl pandas \
                     easyocr pillow requests \
                     azure-ai-formrecognizer google-cloud-documentai \
                     boto3 anthropic fitz PyMuPDF \
                     camelot-py[cv] tabula-py
```

### 🏃‍♂️ 5분 완성: 선택한 파서로 바로 시작하기

#### Option A: 한국어 문서 → Upstage 바로 시작
```python
import requests
import base64
from pathlib import Path

class QuickUpstageParser:
    """5분 완성 Upstage 파서"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def parse_korean_document(self, file_path: str) -> str:
        """한국어 문서 파싱 (PDF, 이미지 지원)"""

        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode()

        response = requests.post(
            "https://api.upstage.ai/v1/document-ai/layout-analysis",
            headers=self.headers,
            json={
                "document": {"content": file_content},
                "ocr": {"language": ["ko", "en"]}
            }
        )

        if response.status_code == 200:
            result = response.json()
            return self._extract_text_from_upstage(result)
        else:
            return f"파싱 실패: {response.text}"

# 사용법
parser = QuickUpstageParser(api_key="your-upstage-key")
text = parser.parse_korean_document("한국어문서.pdf")
print(text[:200])  # 첫 200자 확인
```

#### Option B: 무료 솔루션 → 기본 파서 바로 시작

```python
import os
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from docx import Document
import PyPDF2
from openpyxl import load_workbook

class UniversalDocumentParser:
    """5분이면 완성되는 통합 문서 파서"""

    def __init__(self):
        self.supported_formats = {
            '.pdf': self._parse_pdf,
            '.docx': self._parse_docx,
            '.doc': self._parse_doc_legacy,
            '.xlsx': self._parse_excel,
            '.xls': self._parse_excel_legacy,
            '.txt': self._parse_text,
            '.md': self._parse_text,
            '.html': self._parse_html
        }
        print("✓ 통합 문서 파서 초기화 완료")

    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """단일 문서 파싱 메인 함수"""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        extension = path.suffix.lower()
        if extension not in self.supported_formats:
            raise ValueError(f"지원하지 않는 파일 형식: {extension}")

        print(f"📄 파싱 시작: {path.name} ({extension})")

        try:
            result = self.supported_formats[extension](file_path)
            result['metadata'] = {
                'filename': path.name,
                'file_type': extension,
                'file_size': path.stat().st_size,
                'parsing_status': 'success'
            }
            print(f"✓ 파싱 완료: {len(result['text'])}자 추출")
            return result

        except Exception as e:
            print(f"❌ 파싱 실패: {str(e)}")
            return {
                'text': '',
                'metadata': {
                    'filename': path.name,
                    'file_type': extension,
                    'parsing_status': 'failed',
                    'error': str(e)
                }
            }

    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """PDF 파싱 (텍스트 기반)"""
        text_content = []
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text.strip():  # 빈 페이지 건너뛰기
                    text_content.append(f"[페이지 {i+1}]\n{page_text}")

        return {
            'text': '\n\n'.join(text_content),
            'structure': {'pages': len(reader.pages), 'type': 'pdf'}
        }

    def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Word DOCX 파싱"""
        doc = Document(file_path)

        # 본문 텍스트 추출
        paragraphs = []
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text.strip())

        # 테이블 데이터 추출
        tables_data = []
        for table in doc.tables:
            table_text = []
            for row in table.rows:
                row_text = '\t'.join([cell.text.strip() for cell in row.cells])
                table_text.append(row_text)
            if table_text:
                tables_data.append('\n'.join(table_text))

        # 통합 텍스트 구성
        all_text = '\n\n'.join(paragraphs)
        if tables_data:
            all_text += '\n\n[표 데이터]\n' + '\n\n'.join(tables_data)

        return {
            'text': all_text,
            'structure': {
                'paragraphs': len(paragraphs),
                'tables': len(tables_data),
                'type': 'docx'
            }
        }

    def _parse_excel(self, file_path: str) -> Dict[str, Any]:
        """Excel 파싱"""
        workbook = load_workbook(file_path, data_only=True)

        sheets_content = []
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]

            # 시트 데이터를 DataFrame으로 변환
            data = []
            for row in sheet.iter_rows(values_only=True):
                if any(cell is not None for cell in row):  # 빈 행 건너뛰기
                    data.append([str(cell) if cell is not None else '' for cell in row])

            if data:
                # 첫 행을 헤더로 가정
                df = pd.DataFrame(data[1:], columns=data[0])
                sheet_text = f"[시트: {sheet_name}]\n{df.to_string(index=False)}"
                sheets_content.append(sheet_text)

        return {
            'text': '\n\n'.join(sheets_content),
            'structure': {
                'sheets': len(workbook.sheetnames),
                'sheet_names': workbook.sheetnames,
                'type': 'excel'
            }
        }

# 사용 예시
parser = UniversalDocumentParser()

# 단일 문서 파싱
result = parser.parse_document("sample.pdf")
print(f"추출된 텍스트: {result['text'][:200]}...")
print(f"메타데이터: {result['metadata']}")
```

**예상 결과**:
- PDF: 페이지별 구조 보존하며 텍스트 추출
- Word: 단락과 표 데이터 분리 추출
- Excel: 시트별 구조화된 데이터 변환

## 2. 최신 강력한 파서들과 최적 사용법

### 1.1 전체 파서 성능 비교표 (2025년 최신)

| 파서 | 품질 | 속도 | 비용 | 최적 사용 상황 | 특화 기능 |
|------|------|------|------|----------------|-----------|
| **Azure Document Intelligence** | ★★★★★ | ★★★★ | $$ | 프로덕션 엔터프라이즈 | 양식/표/레이아웃 인식, 한글 우수 |
| **Google Document AI** | ★★★★★ | ★★★★ | $$ | 글로벌 서비스 | 다국어, 손글씨 인식 |
| **LlamaIndex (PyMuPDF4LLM)** | ★★★★ | ★★★★★ | Free | 개발/프로토타입 | RAG 최적화, 청킹 통합 |
| **Unstructured** | ★★★★ | ★★★ | $ | 복합 문서 | AI 기반 구조 인식 |
| **LayoutParser** | ★★★★ | ★★★ | Free | 학술/연구 문서 | 딥러닝 레이아웃 분석 |
| **pdfplumber** | ★★★ | ★★★ | Free | 표 중심 문서 | 표 추출 특화 |
| **EasyOCR** | ★★★★ | ★★ | Free | 다국어 OCR | 80+ 언어, 한글 우수 |
| **PyPDF2** | ★★ | ★★★★★ | Free | 단순 텍스트 | 가벼움, 빠름 |

### 1.2 상용 클라우드 파서 (엔터프라이즈급)

#### Azure Document Intelligence (Form Recognizer)
```python
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os

class AzureDocumentParser:
    """Azure DI - 최고 품질의 문서 파싱"""

    def __init__(self):
        # Azure 설정 (환경변수 또는 설정 파일에서)
        self.endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        self.key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        self.client = DocumentAnalysisClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )

    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """Azure DI로 문서 파싱 (최고 품질)"""

        with open(file_path, "rb") as f:
            poller = self.client.begin_analyze_document(
                "prebuilt-layout",  # 범용 레이아웃 모델
                document=f
            )

        result = poller.result()

        # 구조화된 텍스트 재구성
        content = {
            'paragraphs': [],
            'tables': [],
            'key_value_pairs': [],
            'full_text': ''
        }

        # 단락 추출 (읽는 순서 보장)
        for paragraph in result.paragraphs:
            content['paragraphs'].append({
                'text': paragraph.content,
                'role': paragraph.role if hasattr(paragraph, 'role') else None,
                'confidence': getattr(paragraph, 'confidence', 1.0)
            })

        # 표 구조 보존
        for table in result.tables:
            table_data = []
            for row_idx in range(table.row_count):
                row = [''] * table.column_count
                for cell in table.cells:
                    if cell.row_index == row_idx:
                        row[cell.column_index] = cell.content
                table_data.append(row)

            content['tables'].append({
                'data': table_data,
                'formatted': self._format_table_for_rag(table_data)
            })

        # Key-Value 쌍 추출 (양식 문서)
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                content['key_value_pairs'].append({
                    'key': kv_pair.key.content,
                    'value': kv_pair.value.content,
                    'confidence': getattr(kv_pair, 'confidence', 1.0)
                })

        # 전체 텍스트 재구성
        full_text_parts = []

        # 단락별 텍스트
        for para in content['paragraphs']:
            if para['role'] == 'title':
                full_text_parts.append(f"# {para['text']}")
            elif para['role'] == 'sectionHeading':
                full_text_parts.append(f"## {para['text']}")
            else:
                full_text_parts.append(para['text'])

        # 표 데이터 추가
        if content['tables']:
            full_text_parts.append("\n=== 표 데이터 ===")
            for i, table in enumerate(content['tables']):
                full_text_parts.append(f"\n표 {i+1}:\n{table['formatted']}")

        # Key-Value 추가
        if content['key_value_pairs']:
            full_text_parts.append("\n=== 핵심 정보 ===")
            for kv in content['key_value_pairs']:
                full_text_parts.append(f"{kv['key']}: {kv['value']}")

        content['full_text'] = '\n\n'.join(full_text_parts)

        return {
            'text': content['full_text'],
            'structure': content,
            'parsing_method': 'azure_document_intelligence',
            'quality_score': 0.95,  # 상용 서비스 고품질
            'features': ['layout_analysis', 'table_extraction', 'kv_pairs', 'reading_order']
        }

    def _format_table_for_rag(self, table_data: List[List[str]]) -> str:
        """표를 RAG 친화적 텍스트로 변환"""
        if not table_data:
            return ""

        # 헤더 행 처리
        headers = table_data[0] if table_data else []
        rows = table_data[1:] if len(table_data) > 1 else []

        formatted_rows = []
        for row in rows:
            row_text = []
            for header, value in zip(headers, row):
                if value.strip():
                    row_text.append(f"{header}: {value}")
            if row_text:
                formatted_rows.append(" | ".join(row_text))

        return "\n".join(formatted_rows)


# 사용 예시
azure_parser = AzureDocumentParser()
result = azure_parser.parse_document("complex_report.pdf")
print(f"Azure DI 파싱 결과: {len(result['text'])}자")
print(f"구조 요소: {len(result['structure']['tables'])}개 표, {len(result['structure']['paragraphs'])}개 단락")
```

#### Google Document AI
```python
from google.cloud import documentai_v1 as documentai
import os

class GoogleDocumentAIParser:
    """Google Document AI - 글로벌 최적화"""

    def __init__(self):
        # Google Cloud 설정
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = "us"  # 또는 "eu"
        self.processor_id = os.getenv("GOOGLE_DOC_AI_PROCESSOR_ID")

        self.client = documentai.DocumentProcessorServiceClient()
        self.name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"

    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """Google Document AI로 파싱"""

        # 문서 읽기
        with open(file_path, "rb") as image:
            image_content = image.read()

        # Raw document 생성
        raw_document = documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf"  # 파일 타입에 따라 조정
        )

        # 처리 요청
        request = documentai.ProcessRequest(
            name=self.name,
            raw_document=raw_document
        )

        result = self.client.process_document(request=request)
        document = result.document

        # 구조화된 정보 추출
        content = {
            'text': document.text,
            'entities': [],
            'tables': [],
            'form_fields': []
        }

        # 엔티티 추출 (인명, 날짜, 금액 등)
        for entity in document.entities:
            content['entities'].append({
                'type': entity.type_,
                'mention_text': entity.mention_text,
                'confidence': entity.confidence
            })

        # 표 처리
        for page in document.pages:
            for table in page.tables:
                table_text = self._extract_table_text(table, document.text)
                content['tables'].append(table_text)

        # Form fields (Key-Value)
        for page in document.pages:
            for form_field in page.form_fields:
                key_text = self._get_text(form_field.field_name, document.text)
                value_text = self._get_text(form_field.field_value, document.text)
                content['form_fields'].append({
                    'key': key_text,
                    'value': value_text
                })

        return {
            'text': content['text'],
            'structure': content,
            'parsing_method': 'google_document_ai',
            'quality_score': 0.94,
            'features': ['entity_extraction', 'form_processing', 'multilingual']
        }

# 사용 예시 (설정 필요)
# google_parser = GoogleDocumentAIParser()
# result = google_parser.parse_document("multilingual_doc.pdf")
```

### 1.3 LlamaIndex 통합 파서 (RAG 최적화)

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader, UnstructuredReader
import pymupdf4llm

class LlamaIndexParser:
    """LlamaIndex - RAG에 최적화된 파싱"""

    def __init__(self):
        self.parsers = {
            'pymupdf4llm': self._parse_with_pymupdf4llm,
            'unstructured': self._parse_with_unstructured,
            'simple': self._parse_with_simple_reader
        }

    def parse_document(self, file_path: str, method: str = 'pymupdf4llm') -> Dict[str, Any]:
        """LlamaIndex 통합 파싱"""

        if method not in self.parsers:
            raise ValueError(f"지원하지 않는 방법: {method}")

        return self.parsers[method](file_path)

    def _parse_with_pymupdf4llm(self, file_path: str) -> Dict[str, Any]:
        """PyMuPDF4LLM - 마크다운 구조 보존"""

        # 마크다운 형태로 추출 (구조 보존)
        md_text = pymupdf4llm.to_markdown(file_path)

        # LlamaIndex Document 생성
        from llama_index.core import Document
        documents = [Document(text=md_text, metadata={"source": file_path})]

        return {
            'text': md_text,
            'documents': documents,
            'parsing_method': 'pymupdf4llm',
            'quality_score': 0.90,
            'features': ['markdown_structure', 'rag_optimized', 'fast']
        }

    def _parse_with_unstructured(self, file_path: str) -> Dict[str, Any]:
        """Unstructured.io - RAG 에코시스템에 특화된 AI 기반 파싱"""

        # UnstructuredReader 사용 (최신 기능 활용)
        from llama_index.readers.file.unstructured import UnstructuredReader

        loader = UnstructuredReader(
            # 고이 메타데이터 추출 옵션
            include_metadata=True,
            # 다양한 문서 형식 지원 활성화
            mode="paged",  # elements, paged, single
            # RAG 최적화를 위한 취어링 설정
            chunking_strategy="by_title",
            max_characters=4000,
            new_after_n_chars=3800,
            combine_under_n_chars=500
        )

        try:
            documents = loader.load_data(file=file_path)

            # 전체 텍스트 및 메타데이터 추출
            full_text_parts = []
            metadata_collection = []

            for doc in documents:
                full_text_parts.append(doc.text)
                if doc.metadata:
                    metadata_collection.append(doc.metadata)

            full_text = '\n\n'.join(full_text_parts)

            # 문서 요소 유형 분석
            element_stats = self._analyze_document_elements(documents)

            return {
                'text': full_text,
                'documents': documents,
                'parsing_method': 'unstructured_rag_optimized',
                'quality_score': 0.92,  # RAG 에코시스템 특화로 품질 향상
                'features': [
                    'rag_optimized_chunking',
                    'rich_metadata_extraction',
                    'element_type_classification',
                    'multi_format_support',
                    'vector_db_ready'
                ],
                'element_stats': element_stats,
                'metadata_collection': metadata_collection,
                'chunk_count': len(documents)
            }

        except Exception as e:
            return {
                'text': '',
                'documents': [],
                'parsing_method': 'unstructured_failed',
                'error': str(e),
                'quality_score': 0.0
            }

    def _analyze_document_elements(self, documents) -> Dict[str, int]:
        """문서 요소 유형 통계 분석"""
        element_counts = {
            'paragraphs': 0,
            'titles': 0,
            'tables': 0,
            'lists': 0,
            'figures': 0,
            'headers': 0,
            'footers': 0
        }

        for doc in documents:
            text = doc.text.lower()
            metadata = doc.metadata or {}

            # 메타데이터로 요소 유형 확인
            element_type = metadata.get('category', '')
            if element_type:
                if element_type in element_counts:
                    element_counts[element_type] += 1
            else:
                # 텍스트 기반 추정
                if any(keyword in text for keyword in ['표', 'table', '|']):
                    element_counts['tables'] += 1
                elif any(keyword in text for keyword in ['그림', 'figure', 'chart']):
                    element_counts['figures'] += 1
                elif text.strip().endswith(':'):
                    element_counts['titles'] += 1
                else:
                    element_counts['paragraphs'] += 1

        return element_counts

    def parse_directory_batch(self, directory_path: str) -> List[Dict[str, Any]]:
        """디렉토리 배치 처리 (LlamaIndex 최적화)"""

        # SimpleDirectoryReader로 배치 처리
        reader = SimpleDirectoryReader(
            input_dir=directory_path,
            recursive=True,
            required_exts=[".pdf", ".docx", ".txt", ".md"]
        )

        documents = reader.load_data()

        results = []
        for doc in documents:
            results.append({
                'text': doc.text,
                'metadata': doc.metadata,
                'parsing_method': 'llamaindex_batch',
                'quality_score': 0.85
            })

        return results

# 사용 예시
llama_parser = LlamaIndexParser()

# 단일 문서 파싱 (마크다운 구조 보존)
result = llama_parser.parse_document("report.pdf", method='pymupdf4llm')
print(f"마크다운 구조 보존: {result['text'][:200]}...")

# 디렉토리 배치 처리
batch_results = llama_parser.parse_directory_batch("./documents/")
print(f"배치 처리 완료: {len(batch_results)}개 문서")
```

### 1.4 Unstructured.io 전문 파서 (추가 기능)

```python
from unstructured.partition.auto import partition
from unstructured.staging.base import dict_to_elements
from unstructured.chunking.title import chunk_by_title
import os

class UnstructuredAdvancedParser:
    """Unstructured.io 직접 API 활용 (최고 성능)"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # API 사용 시 환경변수 설정
        if api_key:
            os.environ["UNSTRUCTURED_API_KEY"] = api_key

    def parse_with_unstructured_api(self, file_path: str, strategy: str = "hi_res") -> Dict[str, Any]:
        """Unstructured.io API로 최고 품질 파싱"""

        try:
            # 고해상도 파싱 (hi_res) 또는 빠른 파싱 (fast)
            elements = partition(
                filename=file_path,
                strategy=strategy,  # "hi_res", "fast", "ocr_only", "auto"

                # 고급 설정
                include_page_breaks=True,
                infer_table_structure=True,  # 표 구조 인식
                extract_images_in_pdf=True,  # PDF 내 이미지 추출

                # 언어 설정
                languages=["kor", "eng"],

                # OCR 최적화
                ocr_languages="kor+eng",
                pdf_infer_table_structure=True
            )

            # 요소별 분류 및 정리
            categorized_elements = self._categorize_elements(elements)

            # RAG 에 최적화된 청킹
            chunks = chunk_by_title(
                elements,
                max_characters=4000,
                new_after_n_chars=3800,
                combine_under_n_chars=500,
                multipage_sections=True
            )

            # 마크다운 형태로 방출
            full_text = self._elements_to_markdown(elements)
            chunk_texts = [self._elements_to_markdown([chunk]) for chunk in chunks]

            return {
                'text': full_text,
                'chunks': chunk_texts,
                'elements': elements,
                'categorized_elements': categorized_elements,
                'parsing_method': f'unstructured_api_{strategy}',
                'quality_score': 0.95 if strategy == "hi_res" else 0.90,
                'features': [
                    'table_structure_inference',
                    'image_extraction',
                    'element_categorization',
                    'rag_optimized_chunking',
                    'multilingual_ocr',
                    'markdown_output'
                ]
            }

        except Exception as e:
            # 폴백: 로컬 파싱 시도
            return self._fallback_local_parsing(file_path, str(e))

    def _categorize_elements(self, elements) -> Dict[str, List]:
        """요소 유형별 분류"""
        categorized = {
            'titles': [],
            'narratives': [],
            'tables': [],
            'figures': [],
            'lists': [],
            'headers': [],
            'footers': []
        }

        for element in elements:
            element_type = str(type(element).__name__).lower()

            if 'title' in element_type:
                categorized['titles'].append(element)
            elif 'table' in element_type:
                categorized['tables'].append(element)
            elif 'figure' in element_type or 'image' in element_type:
                categorized['figures'].append(element)
            elif 'list' in element_type:
                categorized['lists'].append(element)
            elif 'header' in element_type:
                categorized['headers'].append(element)
            elif 'footer' in element_type:
                categorized['footers'].append(element)
            else:
                categorized['narratives'].append(element)

        return categorized

    def _elements_to_markdown(self, elements) -> str:
        """요소들을 마크다운으로 변환"""
        markdown_parts = []

        for element in elements:
            element_type = str(type(element).__name__)
            text = str(element)

            if 'Title' in element_type:
                # 제목 수준에 따른 마크다운 헤더
                level = getattr(element, 'metadata', {}).get('category_depth', 1)
                markdown_parts.append('#' * min(level, 6) + ' ' + text)
            elif 'Table' in element_type:
                # 표 형태 유지
                if hasattr(element, 'metadata') and 'text_as_html' in element.metadata:
                    # HTML 표를 마크다운으로 변환 시도
                    markdown_parts.append(f"\n{text}\n")
                else:
                    markdown_parts.append(f"\n```\n{text}\n```\n")
            elif 'List' in element_type:
                # 리스트 형태 유지
                lines = text.split('\n')
                formatted_lines = ['- ' + line.strip() for line in lines if line.strip()]
                markdown_parts.append('\n'.join(formatted_lines))
            else:
                # 일반 텍스트
                markdown_parts.append(text)

        return '\n\n'.join(markdown_parts)

    def _fallback_local_parsing(self, file_path: str, error_msg: str) -> Dict[str, Any]:
        """로컬 파싱 폴백"""
        try:
            # 간단한 로컬 파싱
            elements = partition(filename=file_path, strategy="fast")
            full_text = '\n\n'.join([str(el) for el in elements])

            return {
                'text': full_text,
                'elements': elements,
                'parsing_method': 'unstructured_local_fallback',
                'quality_score': 0.75,
                'fallback_reason': error_msg,
                'features': ['local_processing', 'basic_structure']
            }
        except Exception as fallback_error:
            return {
                'text': '',
                'parsing_method': 'unstructured_failed',
                'error': f"API Error: {error_msg}, Local Error: {str(fallback_error)}",
                'quality_score': 0.0
            }

# 사용 예시
unstructured_parser = UnstructuredAdvancedParser(api_key="your-api-key")

# 고품질 파싱 (시간 소요)
hi_res_result = unstructured_parser.parse_with_unstructured_api(
    "complex_document.pdf",
    strategy="hi_res"
)

# 빠른 파싱
fast_result = unstructured_parser.parse_with_unstructured_api(
    "simple_document.pdf",
    strategy="fast"
)

print(f"고품질: {len(hi_res_result['text'])} 문자, 품질: {hi_res_result['quality_score']}")
print(f"빠른 방식: {len(fast_result['text'])} 문자, 품질: {fast_result['quality_score']}")
print(f"추출된 청크 수: {len(hi_res_result.get('chunks', []))}")
```

### 1.5 LayoutParser (딥러닝 레이아웃 분석)

```python
import layoutparser as lp
from PIL import Image
import pdf2image
import cv2
import numpy as np

class LayoutParserProcessor:
    """LayoutParser - 학술/연구 문서 특화"""

    def __init__(self):
        # 사전 훈련된 모델 로드 (PubLayNet - 학술 논문 특화)
        self.model = lp.Detectron2LayoutModel(
            'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
            label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
        )

        # OCR 엔진 (옵션)
        self.ocr_agent = lp.TesseractAgent(languages='kor+eng')

    def parse_pdf_with_layout_analysis(self, pdf_path: str) -> Dict[str, Any]:
        """레이아웃 분석을 통한 고품질 PDF 파싱"""

        # PDF를 이미지로 변환
        images = pdf2image.convert_from_path(pdf_path, dpi=200)

        all_content = {
            'pages': [],
            'full_text': '',
            'structure_summary': {'titles': 0, 'tables': 0, 'figures': 0, 'text_blocks': 0}
        }

        for page_idx, image in enumerate(images):
            page_content = self._analyze_page_layout(image, page_idx + 1)
            all_content['pages'].append(page_content)

            # 구조 통계 업데이트
            for element in page_content['elements']:
                element_type = element['type'].lower()
                if element_type in all_content['structure_summary']:
                    all_content['structure_summary'][element_type] += 1

        # 전체 텍스트 재구성 (읽는 순서 고려)
        text_parts = []
        for page in all_content['pages']:
            text_parts.append(f"=== 페이지 {page['page_number']} ===")

            # 요소들을 Y좌표 기준으로 정렬 (읽는 순서)
            sorted_elements = sorted(page['elements'], key=lambda x: x['bbox'][1])

            for element in sorted_elements:
                if element['type'] == 'Title':
                    text_parts.append(f"# {element['text']}")
                elif element['type'] == 'Text':
                    text_parts.append(element['text'])
                elif element['type'] == 'Table':
                    text_parts.append(f"[표]\n{element['text']}")
                elif element['type'] == 'List':
                    text_parts.append(f"[목록]\n{element['text']}")

        all_content['full_text'] = '\n\n'.join(text_parts)

        return {
            'text': all_content['full_text'],
            'structure': all_content,
            'parsing_method': 'layoutparser_detectron2',
            'quality_score': 0.92,
            'features': ['deep_learning_layout', 'element_classification', 'reading_order']
        }

    def _analyze_page_layout(self, image: Image.Image, page_num: int) -> Dict[str, Any]:
        """단일 페이지 레이아웃 분석"""

        # 이미지를 numpy 배열로 변환
        image_array = np.array(image)

        # 레이아웃 감지
        layout = self.model.detect(image_array)

        page_elements = []
        for block in layout:
            # 각 블록에서 텍스트 추출
            segment_image = block.crop_image(image_array)

            # OCR로 텍스트 추출
            text = self.ocr_agent.detect(segment_image)

            page_elements.append({
                'type': block.type,
                'bbox': block.coordinates,  # [x1, y1, x2, y2]
                'confidence': block.score,
                'text': text
            })

        return {
            'page_number': page_num,
            'elements': page_elements,
            'layout_confidence': np.mean([elem['confidence'] for elem in page_elements])
        }

# 사용 예시
layout_parser = LayoutParserProcessor()
result = layout_parser.parse_pdf_with_layout_analysis("research_paper.pdf")
print(f"레이아웃 분석 결과: {result['structure']['structure_summary']}")
```

### 1.5 EasyOCR (다국어 특화)

```python
import easyocr
from PIL import Image, ImageEnhance
import numpy as np

class EasyOCRProcessor:
    """EasyOCR - 다국어 및 한글 최적화"""

    def __init__(self, languages=['ko', 'en']):
        # EasyOCR 리더 초기화 (GPU 사용 가능 시 자동 감지)
        self.reader = easyocr.Reader(languages, gpu=True)
        self.languages = languages

    def parse_scanned_document(self, image_path: str) -> Dict[str, Any]:
        """스캔 문서 OCR 파싱"""

        # 이미지 로드 및 전처리
        image = Image.open(image_path)
        enhanced_image = self._enhance_image_for_ocr(image)

        # OCR 수행 (상세 정보 포함)
        results = self.reader.readtext(
            np.array(enhanced_image),
            detail=1,  # 좌표 정보 포함
            paragraph=True,  # 단락 단위 그룹핑
            width_ths=0.7,  # 텍스트 블록 폭 임계값
            height_ths=0.7  # 텍스트 블록 높이 임계값
        )

        # 결과 구조화
        structured_content = {
            'text_blocks': [],
            'full_text': '',
            'confidence_stats': []
        }

        for (bbox, text, confidence) in results:
            if confidence > 0.3:  # 낮은 신뢰도 제외
                structured_content['text_blocks'].append({
                    'text': text,
                    'bbox': bbox,
                    'confidence': confidence
                })
                structured_content['confidence_stats'].append(confidence)

        # 읽는 순서대로 텍스트 정렬 (Y좌표 기준)
        sorted_blocks = sorted(
            structured_content['text_blocks'],
            key=lambda x: (x['bbox'][0][1], x['bbox'][0][0])  # Y좌표 우선, 그다음 X좌표
        )

        # 전체 텍스트 재구성
        full_text_parts = []
        for block in sorted_blocks:
            text = block['text'].strip()
            if text:
                # 문장 구분자 추가
                if not text.endswith(('.', '!', '?', '다', '음')):
                    text += '.'
                full_text_parts.append(text)

        structured_content['full_text'] = ' '.join(full_text_parts)

        # 품질 평가
        avg_confidence = np.mean(structured_content['confidence_stats']) if structured_content['confidence_stats'] else 0
        quality_score = min(avg_confidence / 0.9, 1.0)  # 90% 신뢰도를 최고점으로 정규화

        return {
            'text': structured_content['full_text'],
            'structure': structured_content,
            'parsing_method': 'easyocr_multilingual',
            'quality_score': quality_score,
            'features': ['multilingual_ocr', 'paragraph_detection', 'confidence_scoring'],
            'language_detected': self._detect_primary_language(structured_content['full_text'])
        }

    def _enhance_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """OCR 정확도를 위한 이미지 개선"""

        # 그레이스케일 변환
        if image.mode != 'L':
            image = image.convert('L')

        # 해상도 보장 (최소 1200px 폭)
        width, height = image.size
        if width < 1200:
            scale = 1200 / width
            new_size = (int(width * scale), int(height * scale))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        # 대비 강화
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)

        # 선명도 개선
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)

        return image

    def _detect_primary_language(self, text: str) -> str:
        """텍스트 주 언어 감지"""
        korean_chars = len([c for c in text if '\uAC00' <= c <= '\uD7A3'])
        english_chars = len([c for c in text if c.isalpha() and ord(c) < 128])
        total_chars = korean_chars + english_chars

        if total_chars == 0:
            return 'unknown'

        korean_ratio = korean_chars / total_chars
        if korean_ratio > 0.3:
            return 'korean'
        else:
            return 'english'

# 사용 예시
easyocr_processor = EasyOCRProcessor(languages=['ko', 'en', 'ja'])
result = easyocr_processor.parse_scanned_document("scanned_form.jpg")
print(f"OCR 결과: {len(result['text'])}자, 신뢰도: {result['quality_score']:.2f}")
print(f"감지된 언어: {result['language_detected']}")
```

### 1.6 파서 자동 선택 시스템

```python
class SmartParserSelector:
    """문서 특성에 따른 최적 파서 자동 선택"""

    def __init__(self):
        self.parsers = {
            'azure': AzureDocumentParser(),
            'google': GoogleDocumentAIParser(),
            'llamaindex': LlamaIndexParser(),
            'layoutparser': LayoutParserProcessor(),
            'easyocr': EasyOCRProcessor(),
            'universal': UniversalDocumentParser()
        }

    def auto_parse(self, file_path: str, budget: str = 'medium') -> Dict[str, Any]:
        """문서 특성 분석 후 최적 파서 자동 선택"""

        # 1. 문서 기본 정보 분석
        file_info = self._analyze_file_characteristics(file_path)

        # 2. 예산/품질 요구사항에 따른 파서 선택
        selected_parser = self._select_optimal_parser(file_info, budget)

        print(f"선택된 파서: {selected_parser['name']} (이유: {selected_parser['reason']})")

        # 3. 선택된 파서로 실행
        try:
            result = selected_parser['parser'].parse_document(file_path)
            result['auto_selection_info'] = selected_parser
            return result
        except Exception as e:
            print(f"1차 파서 실패: {str(e)}, 폴백 실행")
            # 폴백: 기본 파서 사용
            return self.parsers['universal'].parse_document(file_path)

    def _analyze_file_characteristics(self, file_path: str) -> Dict[str, Any]:
        """파일 특성 분석"""
        from pathlib import Path

        path = Path(file_path)
        file_size = path.stat().st_size
        extension = path.suffix.lower()

        characteristics = {
            'extension': extension,
            'size_mb': file_size / (1024 * 1024),
            'complexity': 'simple',
            'is_scanned': False,
            'has_forms': False
        }

        # PDF의 경우 추가 분석
        if extension == '.pdf':
            characteristics.update(self._analyze_pdf_complexity(file_path))

        return characteristics

    def _select_optimal_parser(self, file_info: Dict[str, Any], budget: str) -> Dict[str, Any]:
        """파서 선택 로직"""

        # 예산별 우선순위
        budget_priority = {
            'low': ['universal', 'llamaindex', 'easyocr'],
            'medium': ['llamaindex', 'layoutparser', 'azure'],
            'high': ['azure', 'google', 'layoutparser'],
            'unlimited': ['azure', 'google']
        }

        candidates = budget_priority.get(budget, budget_priority['medium'])

        # 파일 특성별 최적 매칭
        if file_info['is_scanned']:
            # 스캔 문서 → OCR 특화
            if 'easyocr' in candidates:
                return {
                    'name': 'easyocr',
                    'parser': self.parsers['easyocr'],
                    'reason': '스캔 문서로 판단, OCR 특화 파서 선택'
                }

        elif file_info.get('has_forms', False):
            # 양식 문서 → 상용 클라우드 서비스
            for parser_name in ['azure', 'google']:
                if parser_name in candidates:
                    return {
                        'name': parser_name,
                        'parser': self.parsers[parser_name],
                        'reason': '양식 문서 감지, 고품질 파서 선택'
                    }

        elif file_info['extension'] == '.pdf' and file_info['complexity'] == 'complex':
            # 복잡한 PDF → 레이아웃 분석
            if 'layoutparser' in candidates:
                return {
                    'name': 'layoutparser',
                    'parser': self.parsers['layoutparser'],
                    'reason': '복잡한 레이아웃 감지, 딥러닝 파서 선택'
                }

        # 기본 선택: 첫 번째 후보
        default_parser = candidates[0]
        return {
            'name': default_parser,
            'parser': self.parsers[default_parser],
            'reason': f'{budget} 예산 기준 기본 선택'
        }

# 사용 예시
smart_parser = SmartParserSelector()

# 자동 파서 선택으로 문서 처리
result = smart_parser.auto_parse("complex_report.pdf", budget='high')
print(f"자동 선택 파싱 완료: {result['auto_selection_info']}")
```

### PDF 고급 파싱 전략

```python
import pdfplumber
from unstructured.partition.pdf import partition_pdf
import pytesseract
from PIL import Image
import io

class AdvancedPDFParser:
    """PDF 문서 특성별 최적 파싱"""

    def __init__(self):
        self.strategies = {
            'text_heavy': self._parse_text_pdf,
            'table_heavy': self._parse_table_pdf,
            'mixed_layout': self._parse_complex_pdf,
            'scanned': self._parse_ocr_pdf
        }

    def detect_pdf_type(self, file_path: str) -> str:
        """PDF 특성 자동 감지"""
        with pdfplumber.open(file_path) as pdf:
            first_page = pdf.pages[0]

            # 테이블 밀도 체크
            tables = first_page.find_tables()
            table_density = len(tables) / len(pdf.pages)

            # 텍스트 추출 성공률 체크
            text = first_page.extract_text()
            text_success_rate = len(text.strip()) / (first_page.width * first_page.height) * 1000

            if text_success_rate < 0.1:
                return 'scanned'  # OCR 필요
            elif table_density > 0.5:
                return 'table_heavy'  # 표 중심
            elif len(tables) > 0:
                return 'mixed_layout'  # 복합 레이아웃
            else:
                return 'text_heavy'  # 텍스트 중심

    def _parse_text_pdf(self, file_path: str) -> Dict[str, Any]:
        """텍스트 중심 PDF - 속도 우선"""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text_parts = []

            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    # 페이지 구분자 추가 (청킹 시 유용)
                    text_parts.append(f"=== 페이지 {i+1} ===\n{page_text}")

            return {
                'text': '\n\n'.join(text_parts),
                'parsing_method': 'pypdf2_fast',
                'quality_score': 0.8
            }

    def _parse_table_pdf(self, file_path: str) -> Dict[str, Any]:
        """표 중심 PDF - 구조 보존 우선"""
        with pdfplumber.open(file_path) as pdf:
            content_parts = []

            for i, page in enumerate(pdf.pages):
                page_content = [f"=== 페이지 {i+1} ==="]

                # 표 추출
                tables = page.find_tables()
                if tables:
                    for j, table in enumerate(tables):
                        table_data = table.extract()
                        if table_data:
                            # 표를 읽기 쉬운 형태로 변환
                            df = pd.DataFrame(table_data[1:], columns=table_data[0])
                            table_text = f"\n[표 {j+1}]\n{df.to_string(index=False)}\n"
                            page_content.append(table_text)

                # 표 외 텍스트 추출
                text = page.extract_text()
                if text and text.strip():
                    # 표와 겹치지 않는 텍스트만 추출하는 로직 필요
                    page_content.append(text)

                content_parts.append('\n'.join(page_content))

            return {
                'text': '\n\n'.join(content_parts),
                'parsing_method': 'pdfplumber_table_focused',
                'quality_score': 0.9
            }
```

### 1.2 Office 문서 (Word, Excel, PowerPoint) 최적화

```python
from docx import Document
from docx.shared import Inches
import openpyxl
from pptx import Presentation
import zipfile
import xml.etree.ElementTree as ET

class OfficeDocumentParser:
    """Office 문서 전문 파서"""

    def parse_word_advanced(self, file_path: str) -> Dict[str, Any]:
        """Word 문서 고급 파싱 - 구조 보존"""
        doc = Document(file_path)

        content = {
            'title': '',
            'headings': [],
            'paragraphs': [],
            'tables': [],
            'lists': [],
            'images': [],
            'metadata': {}
        }

        for para in doc.paragraphs:
            if para.text.strip():
                # 제목 레벨 감지
                if para.style.name.startswith('Heading'):
                    level = int(para.style.name.split()[-1])
                    content['headings'].append({
                        'level': level,
                        'text': para.text.strip(),
                        'style': para.style.name
                    })
                elif para.style.name == 'Title':
                    content['title'] = para.text.strip()
                else:
                    # 리스트 항목 감지
                    if para._p.pPr and para._p.pPr.numPr:
                        content['lists'].append(para.text.strip())
                    else:
                        content['paragraphs'].append(para.text.strip())

        # 표 데이터 구조화
        for i, table in enumerate(doc.tables):
            table_data = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)

            if table_data:
                content['tables'].append({
                    'index': i,
                    'headers': table_data[0] if len(table_data) > 1 else [],
                    'rows': table_data[1:] if len(table_data) > 1 else table_data,
                    'formatted': self._format_table_for_rag(table_data)
                })

        # 구조화된 텍스트 재구성
        structured_text = self._reconstruct_word_structure(content)

        return {
            'text': structured_text,
            'structure': content,
            'parsing_method': 'docx_structured',
            'quality_score': 0.95
        }

    def _format_table_for_rag(self, table_data: List[List[str]]) -> str:
        """표를 RAG에 최적화된 텍스트로 변환"""
        if not table_data:
            return ""

        # 첫 행을 헤더로 가정
        headers = table_data[0]
        rows = table_data[1:] if len(table_data) > 1 else []

        formatted_rows = []
        for row in rows:
            # 헤더-값 쌍으로 변환 (검색 정확도 향상)
            row_pairs = []
            for header, value in zip(headers, row):
                if value.strip():  # 빈 값 제외
                    row_pairs.append(f"{header}: {value}")
            if row_pairs:
                formatted_rows.append(" | ".join(row_pairs))

        return "\n".join(formatted_rows)

    def _reconstruct_word_structure(self, content: Dict) -> str:
        """Word 문서 구조를 보존하며 재구성"""
        parts = []

        # 제목
        if content['title']:
            parts.append(f"# {content['title']}\n")

        # 제목 계층 구조 반영
        current_content = []
        for item in content['headings'] + content['paragraphs']:
            if isinstance(item, dict) and 'level' in item:
                # 제목
                prefix = '#' * item['level']
                current_content.append(f"{prefix} {item['text']}")
            else:
                # 일반 단락
                current_content.append(item)

        parts.extend(current_content)

        # 표 데이터 추가
        if content['tables']:
            parts.append("\n## 표 데이터")
            for i, table in enumerate(content['tables']):
                parts.append(f"\n### 표 {i+1}")
                parts.append(table['formatted'])

        # 리스트 항목
        if content['lists']:
            parts.append("\n## 목록 항목")
            for item in content['lists']:
                parts.append(f"• {item}")

        return '\n\n'.join(parts)
```

## 2. 파싱 품질 최적화 전략

### 2.1 텍스트 품질 검증 및 후처리

```python
import re
from typing import Tuple
from collections import Counter

class ParsingQualityController:
    """파싱 품질 관리 전담 클래스"""

    def __init__(self):
        # 한글 문서 특화 정규표현식
        self.korean_patterns = {
            'broken_encoding': re.compile(r'[^\w\s가-힣ㄱ-ㅎㅏ-ㅣ.,!?;:()\[\]{}"\'%\-+=/\\]'),
            'repeated_chars': re.compile(r'(.)\1{4,}'),  # 같은 문자 5회 이상 반복
            'page_break': re.compile(r'=+\s*페이지\s+\d+\s*=+'),
            'header_footer': re.compile(r'^(페이지\s*\d+|Page\s*\d+|\d+\s*페이지).*$', re.MULTILINE),
            'table_separator': re.compile(r'[|\-+]{3,}'),
            'multiple_spaces': re.compile(r'\s{3,}'),
            'multiple_newlines': re.compile(r'\n{3,}')
        }

    def assess_parsing_quality(self, text: str, file_type: str) -> Dict[str, Any]:
        """파싱 품질 종합 평가"""
        if not text or len(text) < 50:
            return {
                'overall_score': 0.0,
                'issues': ['텍스트 길이 부족'],
                'recommendations': ['OCR 또는 다른 파서 시도']
            }

        scores = {}
        issues = []

        # 1. 인코딩 품질 검사
        encoding_score, encoding_issues = self._check_encoding_quality(text)
        scores['encoding'] = encoding_score
        issues.extend(encoding_issues)

        # 2. 구조 보존 품질 검사
        structure_score, structure_issues = self._check_structure_quality(text, file_type)
        scores['structure'] = structure_score
        issues.extend(structure_issues)

        # 3. 내용 완성도 검사
        completeness_score, completeness_issues = self._check_completeness(text)
        scores['completeness'] = completeness_score
        issues.extend(completeness_issues)

        # 종합 점수 계산 (가중평균)
        weights = {'encoding': 0.4, 'structure': 0.3, 'completeness': 0.3}
        overall_score = sum(scores[key] * weights[key] for key in weights)

        return {
            'overall_score': round(overall_score, 2),
            'detailed_scores': scores,
            'issues': issues,
            'recommendations': self._generate_recommendations(scores, issues),
            'text_stats': self._calculate_text_stats(text)
        }

    def _check_encoding_quality(self, text: str) -> Tuple[float, List[str]]:
        """인코딩 품질 검사"""
        issues = []

        # 깨진 문자 비율
        broken_chars = len(self.korean_patterns['broken_encoding'].findall(text))
        broken_ratio = broken_chars / len(text) if text else 0

        if broken_ratio > 0.05:  # 5% 이상
            issues.append(f'깨진 문자 {broken_ratio:.1%} 감지')

        # 한글/영문 비율 검사 (문서 타입별)
        korean_chars = len(re.findall(r'[가-힣]', text))
        total_chars = len(re.sub(r'\s', '', text))
        korean_ratio = korean_chars / total_chars if total_chars else 0

        # 점수 계산 (깨진 문자 적을수록 높은 점수)
        encoding_score = max(0, 1 - broken_ratio * 10)

        return encoding_score, issues

    def _check_structure_quality(self, text: str, file_type: str) -> Tuple[float, List[str]]:
        """문서 구조 보존 품질 검사"""
        issues = []
        score = 1.0

        # PDF 특화 검사
        if file_type == '.pdf':
            # 페이지 구분자 존재 확인
            page_breaks = len(self.korean_patterns['page_break'].findall(text))
            if page_breaks == 0:
                issues.append('페이지 구분자 없음 - 멀티페이지 PDF일 가능성')
                score -= 0.2

            # 표 구조 보존 확인
            table_indicators = len(self.korean_patterns['table_separator'].findall(text))
            if '|' in text and table_indicators == 0:
                issues.append('표 구조가 보존되지 않았을 가능성')
                score -= 0.3

        # Word 문서 특화 검사
        elif file_type == '.docx':
            # 제목 구조 확인
            headings = len(re.findall(r'^#{1,6}\s', text, re.MULTILINE))
            if headings == 0 and '제목' in text:
                issues.append('제목 구조가 평문으로 변환됨')
                score -= 0.2

        return max(0, score), issues

    def auto_fix_common_issues(self, text: str) -> str:
        """일반적인 파싱 문제 자동 수정"""

        # 1. 중복 공백 정리
        text = self.korean_patterns['multiple_spaces'].sub(' ', text)
        text = self.korean_patterns['multiple_newlines'].sub('\n\n', text)

        # 2. 반복 문자 정리 (단, 의미있는 반복은 보존)
        def replace_repeated(match):
            char = match.group(1)
            if char in '-=_':  # 구분선은 3개까지만
                return char * 3
            elif char in '.!?':  # 감탄사는 2개까지
                return char * 2
            else:  # 나머지는 1개로
                return char

        text = self.korean_patterns['repeated_chars'].sub(replace_repeated, text)

        # 3. 헤더/푸터 제거
        text = self.korean_patterns['header_footer'].sub('', text)

        # 4. 문단 구분 개선
        # 한글 문장 끝 + 대문자/한글로 시작하는 경우 문단 구분
        text = re.sub(r'([.!?])\s*([A-Z가-힣])', r'\1\n\n\2', text)

        # 5. 불필요한 줄바꿈 정리
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

        return text.strip()
```

### 2.2 문서 타입별 최적화 레시피

```python
class DocumentTypeOptimizer:
    """문서 타입별 파싱 최적화"""

    def optimize_for_rag(self, text: str, doc_type: str, domain: str = 'general') -> str:
        """RAG 시스템에 최적화된 텍스트 후처리"""

        optimizers = {
            'pdf': self._optimize_pdf_for_rag,
            'docx': self._optimize_word_for_rag,
            'xlsx': self._optimize_excel_for_rag,
            'pptx': self._optimize_ppt_for_rag
        }

        base_optimizer = optimizers.get(doc_type, self._optimize_generic)
        optimized_text = base_optimizer(text)

        # 도메인별 후처리
        if domain == 'legal':
            optimized_text = self._optimize_legal_documents(optimized_text)
        elif domain == 'financial':
            optimized_text = self._optimize_financial_documents(optimized_text)
        elif domain == 'technical':
            optimized_text = self._optimize_technical_documents(optimized_text)

        return optimized_text

    def _optimize_pdf_for_rag(self, text: str) -> str:
        """PDF → RAG 최적화"""

        # PDF 특유의 문제 해결
        # 1. 컬럼 분리된 텍스트 재조합
        text = self._fix_column_breaks(text)

        # 2. 페이지 경계에서 끊어진 문장 복원
        text = self._fix_page_breaks(text)

        # 3. 표 데이터 구조화
        text = self._structure_pdf_tables(text)

        return text

    def _fix_column_breaks(self, text: str) -> str:
        """컬럼으로 분리된 텍스트 재조합"""
        lines = text.split('\n')
        fixed_lines = []

        i = 0
        while i < len(lines):
            current_line = lines[i].strip()

            # 짧은 줄이 연속으로 나오는 경우 (컬럼 분리 의심)
            if len(current_line) < 50 and i + 1 < len(lines):
                next_line = lines[i + 1].strip()

                # 둘 다 완전한 문장이 아닌 경우 합치기
                if (not current_line.endswith(('.', '!', '?', '다', '음')) and
                    not next_line.startswith(('그런데', '하지만', '따라서'))):
                    fixed_lines.append(current_line + ' ' + next_line)
                    i += 2
                else:
                    fixed_lines.append(current_line)
                    i += 1
            else:
                fixed_lines.append(current_line)
                i += 1

        return '\n'.join(fixed_lines)

    def _optimize_excel_for_rag(self, text: str) -> str:
        """Excel → RAG 최적화"""

        # 표 데이터를 자연어 문장으로 변환
        lines = text.split('\n')
        structured_content = []

        current_table = []
        for line in lines:
            if line.startswith('[시트:'):
                # 새 시트 시작
                if current_table:
                    structured_content.append(self._table_to_sentences(current_table))
                    current_table = []
                structured_content.append(f"\n{line}")
            elif '\t' in line or '|' in line:
                # 표 데이터 라인
                current_table.append(line)
            else:
                # 일반 텍스트
                structured_content.append(line)

        if current_table:
            structured_content.append(self._table_to_sentences(current_table))

        return '\n'.join(structured_content)

    def _table_to_sentences(self, table_lines: List[str]) -> str:
        """표 데이터를 검색 친화적 문장으로 변환"""
        if not table_lines:
            return ""

        # 첫 줄을 헤더로 가정
        header_line = table_lines[0]
        headers = re.split(r'\t|\|', header_line)
        headers = [h.strip() for h in headers if h.strip()]

        sentences = []
        for line in table_lines[1:]:
            if not line.strip():
                continue

            values = re.split(r'\t|\|', line)
            values = [v.strip() for v in values]

            # 헤더-값 쌍으로 문장 생성
            row_facts = []
            for header, value in zip(headers, values):
                if value and value != '-' and value != 'N/A':
                    row_facts.append(f"{header}은(는) {value}")

            if row_facts:
                sentences.append('. '.join(row_facts) + '.')

        return '\n'.join(sentences)
```

## 3. OCR 및 이미지 문서 처리

### 3.1 OCR 품질 최적화

```python
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np

class OCRProcessor:
    """OCR 품질 최적화 전담 클래스"""

    def __init__(self):
        # Tesseract 설정 (한글 최적화)
        self.config = {
            'korean': '--oem 1 --psm 3 -l kor',
            'mixed': '--oem 1 --psm 6 -l kor+eng',
            'table': '--oem 1 --psm 6 -c tessedit_create_tsv=1'
        }

    def process_scanned_pdf(self, file_path: str) -> Dict[str, Any]:
        """스캔 PDF OCR 처리"""
        import fitz  # PyMuPDF

        doc = fitz.open(file_path)
        all_text = []
        quality_scores = []

        for page_num in range(doc.page_count):
            page = doc[page_num]

            # PDF 페이지를 이미지로 변환
            pix = page.get_pixmap()
            img_data = pix.tobytes("ppm")

            # PIL Image로 변환
            img = Image.open(io.BytesIO(img_data))

            # 이미지 전처리 및 OCR
            processed_img = self._preprocess_for_ocr(img)
            page_text, confidence = self._extract_text_with_confidence(processed_img)

            if page_text.strip():
                all_text.append(f"=== 페이지 {page_num + 1} ===\n{page_text}")
                quality_scores.append(confidence)

        avg_confidence = np.mean(quality_scores) if quality_scores else 0

        return {
            'text': '\n\n'.join(all_text),
            'parsing_method': 'ocr_tesseract',
            'quality_score': avg_confidence / 100,  # 0-1 범위로 정규화
            'pages_processed': len(quality_scores)
        }

    def _preprocess_for_ocr(self, image: Image.Image) -> Image.Image:
        """OCR 정확도 향상을 위한 이미지 전처리"""

        # 1. 그레이스케일 변환
        if image.mode != 'L':
            image = image.convert('L')

        # 2. 해상도 향상 (너무 작은 이미지)
        width, height = image.size
        if width < 1200:  # 최소 해상도 보장
            scale_factor = 1200 / width
            new_size = (int(width * scale_factor), int(height * scale_factor))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        # 3. 대비 개선
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)

        # 4. 선명도 개선
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.2)

        # 5. 노이즈 제거 (OpenCV 사용)
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 모폴로지 연산으로 노이즈 제거
        kernel = np.ones((2, 2), np.uint8)
        cv_image = cv2.morphologyEx(cv_image, cv2.MORPH_CLOSE, kernel)

        # 다시 PIL Image로 변환
        image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))

        return image

    def _extract_text_with_confidence(self, image: Image.Image) -> Tuple[str, float]:
        """신뢰도와 함께 텍스트 추출"""
        try:
            # 상세 정보와 함께 OCR 실행
            data = pytesseract.image_to_data(
                image,
                config=self.config['mixed'],
                output_type=pytesseract.Output.DICT
            )

            # 신뢰도 기반 텍스트 필터링
            filtered_text = []
            confidences = []

            for i, conf in enumerate(data['conf']):
                if conf > 30:  # 30% 이상 신뢰도만 채택
                    text = data['text'][i].strip()
                    if text:
                        filtered_text.append(text)
                        confidences.append(conf)

            # 문장 재구성
            full_text = ' '.join(filtered_text)
            avg_confidence = np.mean(confidences) if confidences else 0

            # 한글 문장 경계 개선
            full_text = self._improve_korean_sentences(full_text)

            return full_text, avg_confidence

        except Exception as e:
            print(f"OCR 처리 오류: {str(e)}")
            return "", 0.0

    def _improve_korean_sentences(self, text: str) -> str:
        """한글 문장 경계 개선"""
        # OCR에서 자주 발생하는 오류 수정

        # 1. 잘못된 띄어쓰기 부분 수정
        text = re.sub(r'([가-힣])\s+([.!?])', r'\1\2', text)  # "다 ." → "다."
        text = re.sub(r'([.!?])\s*([가-힣A-Z])', r'\1 \2', text)  # 문장 경계

        # 2. 숫자와 단위 붙이기
        text = re.sub(r'(\d+)\s+([%원만개])', r'\1\2', text)

        # 3. 의미 있는 문장 단위로 줄바꿈
        sentences = re.split(r'([.!?])\s+', text)

        reformed_text = []
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else '')
            if len(sentence.strip()) > 10:  # 너무 짧은 문장 제외
                reformed_text.append(sentence.strip())

        return '\n'.join(reformed_text)
```

## 4. 대용량 문서 및 배치 처리

### 4.1 메모리 효율적 처리

```python
import gc
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing as mp
from pathlib import Path

class BatchDocumentProcessor:
    """대용량 배치 문서 처리"""

    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(8, mp.cpu_count())
        self.supported_extensions = {'.pdf', '.docx', '.doc', '.xlsx', '.xls', '.txt', '.md'}

    def process_directory(self, directory_path: str, output_format: str = 'jsonl') -> Dict[str, Any]:
        """디렉토리 내 모든 문서 배치 처리"""

        directory = Path(directory_path)
        if not directory.exists():
            raise ValueError(f"디렉토리를 찾을 수 없습니다: {directory_path}")

        # 지원 파일 목록 수집
        files_to_process = []
        for file_path in directory.rglob('*'):
            if file_path.suffix.lower() in self.supported_extensions:
                files_to_process.append(str(file_path))

        print(f"처리 대상 파일: {len(files_to_process)}개")

        if not files_to_process:
            return {'processed': 0, 'results': []}

        # 병렬 처리
        results = []
        failed_files = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 작업 제출
            future_to_file = {
                executor.submit(self._process_single_file, file_path): file_path
                for file_path in files_to_process
            }

            # 결과 수집
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result(timeout=300)  # 5분 타임아웃
                    if result:
                        results.append(result)
                        print(f"✓ 완료: {Path(file_path).name}")
                    else:
                        failed_files.append(file_path)
                        print(f"❌ 실패: {Path(file_path).name}")

                except Exception as e:
                    failed_files.append(file_path)
                    print(f"❌ 오류: {Path(file_path).name} - {str(e)}")

                # 메모리 관리
                if len(results) % 50 == 0:
                    gc.collect()

        # 결과 저장
        output_file = directory / f"parsing_results.{output_format}"
        self._save_results(results, output_file, output_format)

        return {
            'processed': len(results),
            'failed': len(failed_files),
            'results': results,
            'output_file': str(output_file),
            'failed_files': failed_files
        }

    def _process_single_file(self, file_path: str) -> Dict[str, Any]:
        """단일 파일 처리 (메모리 효율적)"""
        try:
            # 파일 크기 체크
            file_size = Path(file_path).stat().st_size
            if file_size > 100 * 1024 * 1024:  # 100MB 초과
                return self._process_large_file(file_path)
            else:
                return self._process_regular_file(file_path)

        except Exception as e:
            return {
                'file_path': file_path,
                'error': str(e),
                'status': 'failed'
            }

    def _process_large_file(self, file_path: str) -> Dict[str, Any]:
        """대용량 파일 청크 단위 처리"""
        file_path = Path(file_path)

        if file_path.suffix.lower() == '.pdf':
            return self._process_large_pdf(str(file_path))
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            return self._process_large_excel(str(file_path))
        else:
            # 기타 파일은 일반 처리
            return self._process_regular_file(str(file_path))

    def _process_large_pdf(self, file_path: str) -> Dict[str, Any]:
        """대용량 PDF 청크 처리"""
        import PyPDF2

        chunks = []
        chunk_size = 50  # 50페이지씩 처리

        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)

            for start_page in range(0, total_pages, chunk_size):
                end_page = min(start_page + chunk_size, total_pages)

                chunk_text = []
                for page_num in range(start_page, end_page):
                    try:
                        page = reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text.strip():
                            chunk_text.append(f"[페이지 {page_num + 1}]\n{page_text}")
                    except Exception as e:
                        print(f"페이지 {page_num + 1} 처리 오류: {str(e)}")
                        continue

                if chunk_text:
                    chunks.append({
                        'chunk_id': f"{start_page + 1}-{end_page}",
                        'text': '\n\n'.join(chunk_text),
                        'pages': f"{start_page + 1}-{end_page}"
                    })

                # 메모리 정리
                gc.collect()

        return {
            'file_path': file_path,
            'total_pages': total_pages,
            'chunks': chunks,
            'parsing_method': 'chunked_pdf',
            'status': 'success'
        }
```

## 5. 실전 배포 체크리스트

### 배포 전 필수 검증
- [ ] **파싱 정확도**: 샘플 문서 30개 이상으로 95% 이상 텍스트 추출 성공률
- [ ] **성능 기준**: 1MB 문서 기준 30초 이내 처리 완료
- [ ] **메모리 효율성**: 100MB 문서 처리 시 시스템 메모리 2GB 이하 사용
- [ ] **오류 처리**: 파싱 실패 시 적절한 폴백 메커니즘 작동
- [ ] **보안 검증**: 악성 문서에 대한 안전성 테스트 완료

### 운영 중 모니터링 항목
- [ ] **일간 처리 통계**: 성공/실패율, 평균 처리 시간, 파일 타입별 분포
- [ ] **품질 지표**: OCR 신뢰도, 구조 보존율, 텍스트 완성도
- [ ] **시스템 리소스**: CPU/메모리 사용률, 디스크 I/O
- [ ] **오류 패턴**: 자주 실패하는 문서 유형 및 원인 분석

### 성능 최적화 가이드라인

**문제 유형별 해결책**

1. **파싱 속도 느림**: 병렬 처리 스케일링, 가벼운 파서 우선 시도
2. **텍스트 품질 낮음**: OCR 전처리 강화, 도메인별 후처리 적용
3. **메모리 부족**: 청크 단위 처리, 주기적 가비지 컬렉션
4. **특정 문서 실패**: 파서별 fallback 체인, 수동 처리 큐 운영

## 6. 실전 파서 선택 가이드 (2025년 기준)

### 상황별 최종 권장 파서

| 상황 | 1순위 권장 | 2순위 대안 | 선택 이유 |
|------|-----------|-----------|-----------|
| **엔터프라이즈 프로덕션** | Azure DI | Google Doc AI | 한글 지원, 안정성, 양식 처리 |
| **스타트업/중소기업** | LlamaIndex | Unstructured | 비용 효율, RAG 최적화 |
| **학술/연구** | LayoutParser | LlamaIndex | 논문 레이아웃 특화, 무료 |
| **다국어 글로벌** | Google Doc AI | EasyOCR | 80+ 언어, 손글씨 인식 |
| **스캔 문서 중심** | EasyOCR | Azure DI | OCR 품질, 다국어 |
| **개발/프로토타입** | PyMuPDF4LLM | Universal Parser | 빠른 구현, RAG 친화적 |

### 예산별 추천 조합

**무료 조합 (연간 $0)**
```python
# 기본: LlamaIndex + EasyOCR fallback
primary_parser = LlamaIndexParser()
fallback_parser = EasyOCRProcessor()

# 90% 문서는 무료로 처리 가능
```

**스타트업 조합 (연간 ~$2,000)**
```python
# 핵심 문서만 Azure DI (월 500건)
# 나머지는 LlamaIndex
azure_parser = AzureDocumentParser()  # 중요 문서
llamaindex_parser = LlamaIndexParser()  # 일반 문서
```

**엔터프라이즈 조합 (연간 $10,000+)**
```python
# Azure DI + Google Doc AI + LlamaIndex
# 문서 타입별 최적 분산 처리
smart_selector = SmartParserSelector()  # 자동 선택
```

### 한국 기업 특화 권장사항

1. **공공기관/대기업**: Azure Document Intelligence
   - 한글 양식 문서 처리 우수
   - 엔터프라이즈 보안/컴플라이언스
   - Microsoft 에코시스템 통합

2. **IT 스타트업**: LlamaIndex + PyMuPDF4LLM
   - 개발자 친화적, RAG 최적화
   - 빠른 프로토타이핑 지원
   - 커뮤니티 활발

3. **제조/금융**: Azure DI + EasyOCR 조합
   - 기존 시스템과의 안정적 통합
   - OCR로 레거시 문서 처리
   - 규제 요구사항 대응

이제 RAG 시스템의 첫 관문인 문서 파싱에서 최고 품질의 텍스트를 안정적으로 추출할 수 있습니다.

**다음 단계 연결**:
1. **청킹**: 파싱된 텍스트를 검색 최적화 단위로 분할
2. **임베딩**: 청크를 벡터로 변환하여 의미적 검색 준비
3. **리트리버**: 하이브리드 검색으로 정확한 문서 검색
4. **평가**: 파싱 품질이 전체 RAG 성능에 미치는 영향 측정

## 7. API 연동 및 클라우드 배포 가이드

### 7.1 FastAPI 기반 파싱 서비스 구축

```python
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn
import aiofiles
import asyncio
from pathlib import Path
import uuid
from typing import Dict, Any, Optional
import logging

app = FastAPI(
    title="Document Parsing API",
    description="고성능 문서 파싱 REST API 서비스",
    version="1.0.0"
)

# 전역 파서 인스턴스
smart_parser = SmartParserSelector()

# 설정
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

@app.post("/parse/document")
async def parse_document_endpoint(
    file: UploadFile = File(...),
    parser_type: Optional[str] = None,
    budget: str = "medium",
    enhance_quality: bool = True
) -> JSONResponse:
    """문서 파싱 메인 엔드포인트"""

    # 파일 크기 검증
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="파일 크기가 100MB를 초과합니다")

    # 지원 파일 형식 검증
    allowed_extensions = {'.pdf', '.docx', '.doc', '.xlsx', '.xls', '.txt', '.md'}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"지원하지 않는 파일 형식: {file_ext}")

    # 임시 파일 저장
    task_id = str(uuid.uuid4())
    temp_file_path = UPLOAD_DIR / f"{task_id}_{file.filename}"

    try:
        # 비동기 파일 저장
        async with aiofiles.open(temp_file_path, 'wb') as temp_file:
            content = await file.read()
            await temp_file.write(content)

        # 파싱 수행
        if parser_type:
            # 특정 파서 지정
            if parser_type not in smart_parser.parsers:
                raise HTTPException(status_code=400, detail=f"지원하지 않는 파서: {parser_type}")
            result = smart_parser.parsers[parser_type].parse_document(str(temp_file_path))
        else:
            # 자동 파서 선택
            result = smart_parser.auto_parse(str(temp_file_path), budget=budget)

        # 품질 개선 후처리 (옵션)
        if enhance_quality:
            quality_controller = ParsingQualityController()
            result['text'] = quality_controller.auto_fix_common_issues(result['text'])
            result['quality_assessment'] = quality_controller.assess_parsing_quality(
                result['text'],
                file_ext
            )

        # 응답 데이터 구성
        response_data = {
            "task_id": task_id,
            "filename": file.filename,
            "file_size": file.size,
            "parsing_method": result.get('parsing_method', 'unknown'),
            "quality_score": result.get('quality_score', 0),
            "text_length": len(result['text']),
            "text": result['text'],
            "metadata": result.get('structure', {}),
            "processing_info": {
                "auto_selection": result.get('auto_selection_info'),
                "quality_enhancement": enhance_quality
            }
        }

        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        logging.error(f"파싱 오류 (task_id: {task_id}): {str(e)}")
        raise HTTPException(status_code=500, detail=f"파싱 처리 중 오류: {str(e)}")

    finally:
        # 임시 파일 정리
        if temp_file_path.exists():
            temp_file_path.unlink()

@app.post("/parse/batch")
async def batch_parse_endpoint(
    files: list[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None
) -> JSONResponse:
    """배치 파싱 엔드포인트"""

    if len(files) > 50:  # 배치 크기 제한
        raise HTTPException(status_code=400, detail="배치 크기는 50개 파일까지 제한됩니다")

    batch_id = str(uuid.uuid4())
    task_results = []

    for file in files:
        try:
            # 각 파일을 개별 태스크로 처리
            task_id = str(uuid.uuid4())
            temp_file_path = UPLOAD_DIR / f"{task_id}_{file.filename}"

            async with aiofiles.open(temp_file_path, 'wb') as temp_file:
                content = await file.read()
                await temp_file.write(content)

            # 파싱 실행
            result = smart_parser.auto_parse(str(temp_file_path))

            task_results.append({
                "task_id": task_id,
                "filename": file.filename,
                "status": "success",
                "text_length": len(result['text']),
                "quality_score": result.get('quality_score', 0)
            })

            # 임시 파일 정리
            temp_file_path.unlink()

        except Exception as e:
            task_results.append({
                "task_id": task_id,
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })

    return JSONResponse(content={
        "batch_id": batch_id,
        "total_files": len(files),
        "results": task_results,
        "success_count": len([r for r in task_results if r['status'] == 'success']),
        "failure_count": len([r for r in task_results if r['status'] == 'failed'])
    })

@app.get("/health")
async def health_check():
    """서비스 헬스 체크"""
    return {
        "status": "healthy",
        "available_parsers": list(smart_parser.parsers.keys()),
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024)
    }

@app.get("/parsers/info")
async def get_parser_info():
    """사용 가능한 파서 정보"""
    parser_info = {
        "azure": {
            "name": "Azure Document Intelligence",
            "quality": "★★★★★",
            "cost": "$$",
            "features": ["layout_analysis", "form_recognition", "korean_optimized"]
        },
        "google": {
            "name": "Google Document AI",
            "quality": "★★★★★",
            "cost": "$$",
            "features": ["multilingual", "handwriting", "entity_extraction"]
        },
        "llamaindex": {
            "name": "LlamaIndex Parser",
            "quality": "★★★★",
            "cost": "Free",
            "features": ["rag_optimized", "fast", "markdown_structure"]
        },
        "layoutparser": {
            "name": "LayoutParser",
            "quality": "★★★★",
            "cost": "Free",
            "features": ["deep_learning", "academic_papers", "layout_detection"]
        },
        "easyocr": {
            "name": "EasyOCR",
            "quality": "★★★★",
            "cost": "Free",
            "features": ["multilingual_ocr", "80_languages", "scanned_docs"]
        }
    }
    return parser_info

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 7.2 클라이언트 SDK (Python)

```python
import requests
from typing import Dict, Any, List, Optional
import json
from pathlib import Path

class DocumentParsingClient:
    """문서 파싱 API 클라이언트"""

    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def parse_document(
        self,
        file_path: str,
        parser_type: Optional[str] = None,
        budget: str = "medium",
        enhance_quality: bool = True
    ) -> Dict[str, Any]:
        """단일 문서 파싱"""

        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        url = f"{self.base_url}/parse/document"

        # 파라미터 설정
        params = {
            "budget": budget,
            "enhance_quality": enhance_quality
        }
        if parser_type:
            params["parser_type"] = parser_type

        # 파일 업로드
        with open(file_path, 'rb') as f:
            files = {"file": (file_path.name, f, "application/octet-stream")}
            response = self.session.post(url, files=files, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def parse_batch(self, file_paths: List[str]) -> Dict[str, Any]:
        """배치 파싱"""

        url = f"{self.base_url}/parse/batch"

        files = []
        file_handles = []

        try:
            # 여러 파일 준비
            for file_path in file_paths:
                path = Path(file_path)
                if path.exists():
                    f = open(path, 'rb')
                    file_handles.append(f)
                    files.append(("files", (path.name, f, "application/octet-stream")))

            response = self.session.post(url, files=files)

            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()

        finally:
            # 파일 핸들 정리
            for f in file_handles:
                f.close()

    def get_parser_info(self) -> Dict[str, Any]:
        """사용 가능한 파서 정보 조회"""
        url = f"{self.base_url}/parsers/info"
        response = self.session.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def health_check(self) -> Dict[str, Any]:
        """서비스 상태 확인"""
        url = f"{self.base_url}/health"
        response = self.session.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

# 사용 예시
client = DocumentParsingClient(base_url="http://your-api-server.com")

# 단일 문서 파싱
result = client.parse_document(
    file_path="./report.pdf",
    parser_type="azure",  # 특정 파서 지정
    budget="high",
    enhance_quality=True
)

print(f"파싱 완료: {result['text_length']}자 추출")
print(f"품질 점수: {result['quality_score']:.2f}")

# 배치 파싱
batch_result = client.parse_batch([
    "./doc1.pdf",
    "./doc2.docx",
    "./doc3.xlsx"
])

print(f"배치 처리: {batch_result['success_count']}/{batch_result['total_files']} 성공")
```

### 7.3 JavaScript/TypeScript 클라이언트

```typescript
interface ParseResult {
  task_id: string;
  filename: string;
  parsing_method: string;
  quality_score: number;
  text_length: number;
  text: string;
  metadata: any;
}

interface BatchResult {
  batch_id: string;
  total_files: number;
  success_count: number;
  failure_count: number;
  results: Array<{
    task_id: string;
    filename: string;
    status: 'success' | 'failed';
    error?: string;
  }>;
}

class DocumentParsingClient {
  constructor(private baseUrl: string = 'http://localhost:8000', private apiKey?: string) {}

  async parseDocument(
    file: File,
    options: {
      parserType?: string;
      budget?: 'low' | 'medium' | 'high' | 'unlimited';
      enhanceQuality?: boolean;
    } = {}
  ): Promise<ParseResult> {
    const formData = new FormData();
    formData.append('file', file);

    const params = new URLSearchParams();
    if (options.parserType) params.append('parser_type', options.parserType);
    if (options.budget) params.append('budget', options.budget);
    if (options.enhanceQuality !== undefined) {
      params.append('enhance_quality', String(options.enhanceQuality));
    }

    const url = `${this.baseUrl}/parse/document?${params}`;
    const headers: HeadersInit = {};

    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: formData
    });

    if (!response.ok) {
      throw new Error(`파싱 실패: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async parseBatch(files: File[]): Promise<BatchResult> {
    const formData = new FormData();

    files.forEach(file => {
      formData.append('files', file);
    });

    const headers: HeadersInit = {};
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(`${this.baseUrl}/parse/batch`, {
      method: 'POST',
      headers,
      body: formData
    });

    if (!response.ok) {
      throw new Error(`배치 파싱 실패: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<{ status: string; available_parsers: string[] }> {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
}

// React 컴포넌트 사용 예시
function DocumentUploader() {
  const client = new DocumentParsingClient('https://api.yourservice.com');
  const [result, setResult] = useState<ParseResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    try {
      const parseResult = await client.parseDocument(file, {
        budget: 'medium',
        enhanceQuality: true
      });
      setResult(parseResult);
    } catch (error) {
      console.error('파싱 오류:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileUpload} />
      {loading && <p>파싱 중...</p>}
      {result && (
        <div>
          <h3>파싱 결과</h3>
          <p>품질 점수: {result.quality_score.toFixed(2)}</p>
          <p>추출 텍스트: {result.text_length}자</p>
          <textarea value={result.text} readOnly />
        </div>
      )}
    </div>
  );
}
```

### 7.4 Docker 컨테이너화

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-kor \
    tesseract-ocr-eng \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 업로드 디렉토리 생성
RUN mkdir -p uploads

# 포트 노출
EXPOSE 8000

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  document-parser:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    environment:
      - AZURE_FORM_RECOGNIZER_ENDPOINT=${AZURE_ENDPOINT}
      - AZURE_FORM_RECOGNIZER_KEY=${AZURE_KEY}
      - GOOGLE_CLOUD_PROJECT=${GOOGLE_PROJECT}
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - document-parser
    restart: unless-stopped
```

### 7.5 프로덕션 배포 고려사항

```python
# 비동기 처리 및 큐 시스템
from celery import Celery
from redis import Redis

# Celery 설정
celery_app = Celery(
    'document_parsing',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379'
)

@celery_app.task
def async_parse_document(file_path: str, parser_config: dict) -> dict:
    """비동기 문서 파싱 태스크"""
    try:
        smart_parser = SmartParserSelector()
        result = smart_parser.auto_parse(file_path, **parser_config)
        return {
            'status': 'success',
            'result': result
        }
    except Exception as e:
        return {
            'status': 'failed',
            'error': str(e)
        }

# API에서 비동기 처리
@app.post("/parse/async")
async def parse_document_async(file: UploadFile = File(...)):
    """비동기 파싱 요청"""

    # 파일 저장
    task_id = str(uuid.uuid4())
    file_path = f"./uploads/{task_id}_{file.filename}"

    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)

    # Celery 태스크 실행
    task = async_parse_document.delay(file_path, {'budget': 'medium'})

    return {
        'task_id': task_id,
        'celery_task_id': task.id,
        'status': 'processing',
        'check_url': f'/parse/status/{task.id}'
    }

@app.get("/parse/status/{celery_task_id}")
async def get_parsing_status(celery_task_id: str):
    """파싱 상태 조회"""
    task = async_parse_document.AsyncResult(celery_task_id)

    if task.state == 'PENDING':
        return {'status': 'processing', 'progress': 0}
    elif task.state == 'SUCCESS':
        return {'status': 'completed', 'result': task.result}
    else:
        return {'status': 'failed', 'error': str(task.info)}
```

## 9. 추가 강력한 파서 보완 (2025년 최신)

### 9.1 AWS Textract - 아마존의 문서 인식 AI

**특장점**:
- 양식, 표, 텍스트 자동 감지 및 구조화
- 99.5% 이상의 정확도
- 대용량 배치 처리 최적화

```python
import boto3
from typing import Dict, Any, List
import json

class AWSTextractParser:
    """AWS Textract를 이용한 고급 문서 파싱"""

    def __init__(self, region_name='us-east-1'):
        self.textract = boto3.client('textract', region_name=region_name)
        self.s3 = boto3.client('s3', region_name=region_name)

    def parse_document_with_textract(self, file_path: str, s3_bucket: str) -> Dict[str, Any]:
        """AWS Textract로 구조화된 문서 파싱"""

        # S3에 파일 업로드
        s3_key = f"textract-input/{Path(file_path).name}"
        self.s3.upload_file(file_path, s3_bucket, s3_key)

        # Textract 분석 시작
        response = self.textract.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': s3_bucket,
                    'Name': s3_key
                }
            },
            FeatureTypes=[
                'TABLES',  # 표 감지 및 추출
                'FORMS',   # 양식 필드 감지
                'LAYOUT',  # 레이아웃 분석
                'SIGNATURES'  # 서명 감지
            ]
        )

        job_id = response['JobId']

        # 분석 완료 대기
        while True:
            status_response = self.textract.get_document_analysis(JobId=job_id)
            status = status_response['JobStatus']

            if status in ['SUCCEEDED', 'FAILED']:
                break
            time.sleep(2)

        if status == 'FAILED':
            raise Exception("Textract 분석 실패")

        # 결과 처리
        return self._process_textract_results(status_response)

    def _process_textract_results(self, response: Dict) -> Dict[str, Any]:
        """Textract 결과를 구조화된 형태로 변환"""

        blocks = response['Blocks']

        # 블록 유형별 분류
        lines = [block for block in blocks if block['BlockType'] == 'LINE']
        tables = [block for block in blocks if block['BlockType'] == 'TABLE']
        key_values = [block for block in blocks if block['BlockType'] == 'KEY_VALUE_SET']

        # 텍스트 추출
        text_content = []
        for line in lines:
            if 'Text' in line:
                text_content.append(line['Text'])

        # 표 데이터 구조화
        structured_tables = []
        for table in tables:
            table_data = self._extract_table_data(table, blocks)
            if table_data:
                structured_tables.append(table_data)

        # 키-값 쌍 추출 (양식 데이터)
        form_data = {}
        for kv in key_values:
            if kv.get('EntityTypes') == ['KEY']:
                key_text = self._get_text_from_block(kv, blocks)
                # 연결된 VALUE 찾기
                for relation in kv.get('Relationships', []):
                    if relation['Type'] == 'VALUE':
                        value_ids = relation['Ids']
                        value_text = []
                        for value_id in value_ids:
                            value_block = next((b for b in blocks if b['Id'] == value_id), None)
                            if value_block:
                                value_text.append(self._get_text_from_block(value_block, blocks))
                        form_data[key_text] = ' '.join(value_text)

        return {
            'text': '\n'.join(text_content),
            'tables': structured_tables,
            'form_data': form_data,
            'metadata': {
                'parser_type': 'aws_textract',
                'total_blocks': len(blocks),
                'accuracy_confidence': self._calculate_confidence(blocks)
            }
        }

    def _extract_table_data(self, table_block: Dict, all_blocks: List[Dict]) -> List[List[str]]:
        """테이블 데이터를 2차원 배열로 추출"""
        if 'Relationships' not in table_block:
            return []

        cell_map = {}

        # 테이블 셀 매핑
        for relationship in table_block['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell_block = next((b for b in all_blocks if b['Id'] == child_id), None)
                    if cell_block and cell_block['BlockType'] == 'CELL':
                        row = cell_block['RowIndex'] - 1
                        col = cell_block['ColumnIndex'] - 1
                        text = self._get_text_from_block(cell_block, all_blocks)
                        cell_map[(row, col)] = text

        # 2차원 배열로 변환
        if not cell_map:
            return []

        max_row = max(pos[0] for pos in cell_map.keys()) + 1
        max_col = max(pos[1] for pos in cell_map.keys()) + 1

        table_data = []
        for row in range(max_row):
            row_data = []
            for col in range(max_col):
                cell_text = cell_map.get((row, col), '')
                row_data.append(cell_text)
            table_data.append(row_data)

        return table_data

# 사용 예시
textract_parser = AWSTextractParser()
result = textract_parser.parse_document_with_textract("contract.pdf", "my-textract-bucket")
print(f"추출된 양식 데이터: {result['form_data']}")
```

### 9.2 IBM Watson Document Understanding

```python
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import base64

class IBMWatsonDocumentParser:
    """IBM Watson으로 지능형 문서 분석"""

    def __init__(self, api_key: str, service_url: str, project_id: str):
        authenticator = IAMAuthenticator(api_key)
        self.discovery = DiscoveryV2(
            version='2020-08-30',
            authenticator=authenticator
        )
        self.discovery.set_service_url(service_url)
        self.project_id = project_id

    def parse_with_watson(self, file_path: str) -> Dict[str, Any]:
        """Watson Discovery로 문서 분석 및 엔티티 추출"""

        # 문서 업로드 및 분석
        with open(file_path, 'rb') as file:
            file_content = file.read()

        # Watson Discovery에 문서 추가
        response = self.discovery.add_document(
            project_id=self.project_id,
            collection_id='default',
            file=file_content,
            filename=Path(file_path).name,
            file_content_type=self._get_content_type(file_path)
        ).get_result()

        document_id = response['document_id']

        # 문서 처리 완료 대기
        while True:
            doc_status = self.discovery.get_document(
                project_id=self.project_id,
                collection_id='default',
                document_id=document_id
            ).get_result()

            if doc_status['status'] == 'available':
                break
            elif doc_status['status'] == 'failed':
                raise Exception("Watson 문서 처리 실패")
            time.sleep(3)

        # 문서 내용 쿼리
        search_result = self.discovery.query(
            project_id=self.project_id,
            query=f'document_id:{document_id}',
            return_=['text', 'enrichments', 'metadata'],
            count=1
        ).get_result()

        if search_result['matching_results'] > 0:
            doc_data = search_result['results'][0]
            return self._process_watson_results(doc_data)

        return {'text': '', 'entities': [], 'concepts': []}

    def _process_watson_results(self, doc_data: Dict) -> Dict[str, Any]:
        """Watson 결과 구조화"""

        # 기본 텍스트
        text = doc_data.get('text', [''])[0] if doc_data.get('text') else ''

        # 엔리치먼트 정보 (엔티티, 개념, 감정 등)
        enrichments = doc_data.get('enrichments', {})

        # 엔티티 추출
        entities = []
        if 'entities' in enrichments:
            for entity in enrichments['entities']:
                entities.append({
                    'text': entity['text'],
                    'type': entity['type'],
                    'confidence': entity['confidence']
                })

        # 주요 개념 추출
        concepts = []
        if 'concepts' in enrichments:
            for concept in enrichments['concepts']:
                concepts.append({
                    'text': concept['text'],
                    'relevance': concept['relevance']
                })

        # 감정 분석
        sentiment = None
        if 'sentiment' in enrichments:
            sentiment = enrichments['sentiment']['document']

        return {
            'text': text,
            'entities': entities,
            'concepts': concepts,
            'sentiment': sentiment,
            'metadata': {
                'parser_type': 'ibm_watson',
                'language': doc_data.get('language', 'unknown'),
                'enrichments_applied': list(enrichments.keys())
            }
        }
```

### 9.3 Claude Vision - 최신 멀티모달 AI 파싱

```python
import anthropic
from PIL import Image
import base64
import io

class ClaudeVisionParser:
    """Claude의 비전 기능으로 문서 이해 및 파싱"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def parse_with_claude_vision(self, image_path: str, parsing_instruction: str = None) -> Dict[str, Any]:
        """Claude Vision으로 지능형 문서 파싱"""

        # 이미지를 base64로 인코딩
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        # 기본 파싱 지시사항
        if not parsing_instruction:
            parsing_instruction = """
            이 문서를 분석하여 다음 정보를 JSON 형태로 추출해주세요:
            1. 문서의 전체 텍스트 내용
            2. 표가 있다면 구조화된 데이터
            3. 주요 엔티티 (인명, 날짜, 금액, 회사명 등)
            4. 문서의 유형 및 목적
            5. 핵심 요약
            """

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": parsing_instruction
                            }
                        ]
                    }
                ]
            )

            # Claude 응답을 구조화된 데이터로 파싱
            claude_response = response.content[0].text

            # JSON 응답 파싱 시도
            try:
                import json
                parsed_data = json.loads(claude_response)
            except:
                # JSON 파싱 실패 시 텍스트로 반환
                parsed_data = {
                    'text': claude_response,
                    'parsing_status': 'text_only'
                }

            return {
                'claude_analysis': parsed_data,
                'raw_response': claude_response,
                'metadata': {
                    'parser_type': 'claude_vision',
                    'model': 'claude-3-sonnet',
                    'parsing_instruction': parsing_instruction
                }
            }

        except Exception as e:
            return {
                'error': str(e),
                'metadata': {
                    'parser_type': 'claude_vision',
                    'status': 'failed'
                }
            }

    def parse_complex_form(self, image_path: str) -> Dict[str, Any]:
        """복잡한 양식 문서 특화 파싱"""

        specialized_instruction = """
        이 양식 문서를 분석하여 다음과 같은 구조로 정보를 추출해주세요:

        {
            "form_type": "문서 유형 (계약서, 신청서, 보고서 등)",
            "fields": {
                "필드명1": "값1",
                "필드명2": "값2"
            },
            "tables": [
                {
                    "table_title": "표 제목",
                    "headers": ["헤더1", "헤더2"],
                    "rows": [["데이터1", "데이터2"]]
                }
            ],
            "signatures": ["서명 위치 및 정보"],
            "dates": ["문서 내 모든 날짜"],
            "amounts": ["금액 정보"],
            "parties": ["관련 당사자들"],
            "summary": "문서 핵심 요약"
        }

        한국어 문서라면 한국어로, 영어 문서라면 영어로 응답해주세요.
        """

        return self.parse_with_claude_vision(image_path, specialized_instruction)

# 사용 예시
claude_parser = ClaudeVisionParser(api_key="your-claude-api-key")
result = claude_parser.parse_complex_form("contract_scan.jpg")
print(f"Claude 분석 결과: {result['claude_analysis']}")
```

### 9.4 고급 테이블 파싱 전문 라이브러리

```python
import camelot
import tabula
import pandas as pd

class AdvancedTableParser:
    """고급 테이블 파싱 전문 도구들"""

    def __init__(self):
        self.parsers = {
            'camelot': self._parse_with_camelot,
            'tabula': self._parse_with_tabula,
            'combined': self._parse_with_combined_approach
        }

    def extract_tables_advanced(self, pdf_path: str, method: str = 'combined') -> List[pd.DataFrame]:
        """고급 테이블 추출"""

        if method not in self.parsers:
            raise ValueError(f"지원하지 않는 방법: {method}")

        return self.parsers[method](pdf_path)

    def _parse_with_camelot(self, pdf_path: str) -> List[pd.DataFrame]:
        """Camelot으로 고정밀 테이블 추출"""

        # Lattice 방법 (테두리가 있는 표)
        try:
            tables_lattice = camelot.read_pdf(
                pdf_path,
                flavor='lattice',  # 격자 형태 표
                pages='all',
                line_scale=40,
                copy_text=['v']
            )

            tables = []
            for table in tables_lattice:
                if table.accuracy > 80:  # 80% 이상 정확도만 채택
                    df = table.df
                    # 빈 행/열 제거
                    df = df.dropna(how='all').dropna(axis=1, how='all')
                    if not df.empty:
                        tables.append(df)

            # Stream 방법으로 추가 시도 (테두리가 없는 표)
            if not tables:
                tables_stream = camelot.read_pdf(
                    pdf_path,
                    flavor='stream',  # 스트림 형태
                    pages='all',
                    table_areas=None,
                    columns=None,
                    edge_tol=500
                )

                for table in tables_stream:
                    if table.accuracy > 70:
                        df = table.df
                        df = df.dropna(how='all').dropna(axis=1, how='all')
                        if not df.empty:
                            tables.append(df)

            return tables

        except Exception as e:
            print(f"Camelot 파싱 실패: {str(e)}")
            return []

    def _parse_with_tabula(self, pdf_path: str) -> List[pd.DataFrame]:
        """Tabula로 테이블 추출"""

        try:
            # 전체 페이지에서 테이블 추출
            tables = tabula.read_pdf(
                pdf_path,
                pages='all',
                multiple_tables=True,
                pandas_options={'header': None}  # 헤더 자동 감지 비활성화
            )

            # 데이터 정제
            cleaned_tables = []
            for df in tables:
                if isinstance(df, pd.DataFrame) and not df.empty:
                    # NaN이 많은 열/행 제거
                    df = df.dropna(thresh=len(df.columns)*0.5)  # 50% 이상 데이터가 있는 행만
                    df = df.dropna(axis=1, thresh=len(df)*0.3)  # 30% 이상 데이터가 있는 열만

                    if not df.empty and df.shape[0] > 1 and df.shape[1] > 1:
                        cleaned_tables.append(df)

            return cleaned_tables

        except Exception as e:
            print(f"Tabula 파싱 실패: {str(e)}")
            return []

    def _parse_with_combined_approach(self, pdf_path: str) -> List[pd.DataFrame]:
        """Camelot과 Tabula를 조합한 최적 추출"""

        # 먼저 Camelot 시도 (더 정확함)
        camelot_tables = self._parse_with_camelot(pdf_path)

        # Camelot이 실패하거나 결과가 없으면 Tabula 시도
        if not camelot_tables:
            tabula_tables = self._parse_with_tabula(pdf_path)
            return tabula_tables

        # Camelot 결과가 있지만 품질이 낮으면 Tabula도 시도해서 비교
        tabula_tables = self._parse_with_tabula(pdf_path)

        # 두 결과 중 더 나은 것 선택
        if len(tabula_tables) > len(camelot_tables):
            return tabula_tables

        return camelot_tables
```

### 🎯 문서 유형별 파싱 품질 최적화 전략

#### A. **계약서/법률 문서** - 정확성이 생명
```python
class LegalDocumentOptimizer:
    """법률 문서 파싱 품질 최적화"""

    @staticmethod
    def optimize_legal_document_parsing(file_path: str) -> Dict[str, Any]:
        """계약서/법률 문서 최적화 파싱"""

        optimizations = {
            'preprocessing': {
                'dpi_enhancement': 300,  # 고해상도 스캔
                'noise_reduction': True,
                'contrast_adjustment': 1.2
            },
            'parser_settings': {
                'ocr_language': ['ko', 'en'],
                'preserve_formatting': True,
                'extract_signatures': True,
                'detect_tables': True
            },
            'quality_checks': [
                'paragraph_structure_validation',
                'legal_term_recognition',
                'date_format_verification',
                'signature_block_detection'
            ]
        }

        # 1단계: 이미지 전처리 (스캔 문서의 경우)
        if file_path.lower().endswith(('.jpg', '.png', '.tiff')):
            enhanced_image = enhance_image_for_legal_docs(file_path, optimizations['preprocessing'])
            file_path = enhanced_image

        # 2단계: 최적 파서 조합 (정확도 우선)
        parsers_priority = [
            ('aws_textract', {'extract_forms': True, 'extract_signatures': True}),
            ('upstage', {'ocr_model': 'premium', 'preserve_order': True}),
            ('azure', {'enable_forms_recognition': True}),
        ]

        best_result = None
        highest_confidence = 0

        for parser_name, settings in parsers_priority:
            try:
                result = parse_with_parser(parser_name, file_path, settings)

                # 법률 문서 특화 품질 검사
                quality_score = validate_legal_document_quality(result)

                if quality_score > highest_confidence:
                    highest_confidence = quality_score
                    best_result = result

                # 95% 이상 신뢰도면 조기 종료
                if quality_score >= 0.95:
                    break

            except Exception as e:
                continue

        # 3단계: 후처리 및 검증
        if best_result:
            best_result = post_process_legal_document(best_result)
            best_result['quality_report'] = generate_legal_quality_report(best_result)

        return best_result

def validate_legal_document_quality(result: Dict) -> float:
    """법률 문서 품질 검증"""

    text = result.get('text', '')
    quality_indicators = {
        'has_article_numbers': bool(re.search(r'제\s*\d+\s*조|Article\s+\d+', text)),
        'has_signature_blocks': '서명' in text or 'signature' in text.lower(),
        'has_legal_dates': bool(re.search(r'\d{4}년\s*\d{1,2}월\s*\d{1,2}일|\d{4}-\d{2}-\d{2}', text)),
        'proper_paragraph_structure': len(re.findall(r'\n\n', text)) > 3,
        'has_legal_terminology': any(term in text for term in ['계약', '합의', '조항', '당사자', 'contract', 'agreement']),
        'minimal_ocr_errors': sum(1 for char in text if char in '□■◆�') < len(text) * 0.01
    }

    # 가중치 적용 점수 계산
    weights = {
        'has_article_numbers': 0.2,
        'has_signature_blocks': 0.15,
        'has_legal_dates': 0.15,
        'proper_paragraph_structure': 0.2,
        'has_legal_terminology': 0.15,
        'minimal_ocr_errors': 0.15
    }

    total_score = sum(weights[key] * (1 if value else 0) for key, value in quality_indicators.items())
    return total_score
```

#### B. **재무/회계 문서** - 숫자 정확도가 핵심
```python
class FinancialDocumentOptimizer:
    """재무 문서 파싱 품질 최적화"""

    @staticmethod
    def optimize_financial_parsing(file_path: str) -> Dict[str, Any]:
        """재무 문서 최적화 파싱"""

        # 1단계: 테이블 특화 파서 우선 사용
        table_specialized_parsers = [
            ('aws_textract', {
                'feature_types': ['TABLES', 'FORMS', 'QUERIES'],
                'extract_table_structure': True
            }),
            ('advanced_table_parser', {
                'method': 'combined',
                'accuracy_threshold': 85
            }),
            ('upstage', {
                'extract_tables': True,
                'preserve_number_format': True
            })
        ]

        # 2단계: 숫자 데이터 검증 강화
        best_result = None
        highest_numeric_accuracy = 0

        for parser_name, settings in table_specialized_parsers:
            result = parse_with_parser(parser_name, file_path, settings)

            # 숫자 정확도 검사
            numeric_accuracy = validate_financial_numbers(result)

            if numeric_accuracy > highest_numeric_accuracy:
                highest_numeric_accuracy = numeric_accuracy
                best_result = result

        # 3단계: 재무 데이터 후처리
        if best_result:
            best_result = post_process_financial_data(best_result)

        return best_result

def validate_financial_numbers(result: Dict) -> float:
    """재무 데이터 숫자 정확도 검증"""

    text = result.get('text', '')
    tables = result.get('tables', [])

    validation_checks = {
        'currency_format_consistency': validate_currency_formats(text),
        'number_alignment_in_tables': validate_table_number_alignment(tables),
        'calculation_accuracy': validate_calculations(tables),
        'date_format_consistency': validate_date_formats(text),
        'no_mixed_number_formats': validate_number_format_consistency(text)
    }

    # 각 체크의 가중치
    weights = {
        'currency_format_consistency': 0.25,
        'number_alignment_in_tables': 0.25,
        'calculation_accuracy': 0.3,
        'date_format_consistency': 0.1,
        'no_mixed_number_formats': 0.1
    }

    return sum(weights[key] * score for key, score in validation_checks.items())

def validate_calculations(tables: List) -> float:
    """테이블 내 계산 정확도 검증"""
    if not tables:
        return 0.5

    accurate_calculations = 0
    total_calculations = 0

    for table in tables:
        table_data = table.get('data', [])
        if len(table_data) < 2:
            continue

        # 합계 행 찾기
        for row_idx, row in enumerate(table_data):
            if any(keyword in str(cell).lower() for cell in row
                   for keyword in ['합계', '총계', 'total', 'sum']):

                # 숫자 열에서 합계 검증
                for col_idx, cell in enumerate(row):
                    if is_number(cell):
                        column_values = []
                        for prev_row in table_data[:row_idx]:
                            if col_idx < len(prev_row) and is_number(prev_row[col_idx]):
                                column_values.append(float(clean_number(prev_row[col_idx])))

                        if column_values:
                            expected_sum = sum(column_values)
                            actual_sum = float(clean_number(cell))

                            total_calculations += 1
                            if abs(expected_sum - actual_sum) < 0.01:  # 소수점 오차 허용
                                accurate_calculations += 1

    return accurate_calculations / max(total_calculations, 1)
```

#### C. **학술 논문** - 구조와 인용 정확성
```python
class AcademicPaperOptimizer:
    """학술 논문 파싱 품질 최적화"""

    @staticmethod
    def optimize_academic_parsing(file_path: str) -> Dict[str, Any]:
        """학술 논문 최적화 파싱"""

        # 1단계: 레이아웃 분석 중심 파서
        academic_parsers = [
            ('layoutparser', {
                'model': 'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
                'detect_figures': True,
                'detect_tables': True,
                'preserve_reading_order': True
            }),
            ('upstage', {
                'layout': {
                    'extract_figures': True,
                    'extract_tables': True,
                    'preserve_order': True
                }
            }),
            ('azure', {
                'features': ['layout', 'text', 'tables']
            })
        ]

        best_result = None
        highest_structure_score = 0

        for parser_name, settings in academic_parsers:
            result = parse_with_parser(parser_name, file_path, settings)

            # 학술 구조 품질 검사
            structure_score = validate_academic_structure(result)

            if structure_score > highest_structure_score:
                highest_structure_score = structure_score
                best_result = result

        # 2단계: 학술 논문 후처리
        if best_result:
            best_result = enhance_academic_structure(best_result)

        return best_result

def validate_academic_structure(result: Dict) -> float:
    """학술 논문 구조 품질 검증"""

    text = result.get('text', '')

    structure_elements = {
        'has_abstract': bool(re.search(r'abstract|초록|요약', text, re.IGNORECASE)),
        'has_sections': len(re.findall(r'\n[0-9]+\.\s+[A-Z]|\n[IVX]+\.\s+[A-Z]', text)) >= 3,
        'has_references': bool(re.search(r'references|참고문헌|bibliography', text, re.IGNORECASE)),
        'has_figures_tables': '그림' in text or 'figure' in text.lower() or '표' in text or 'table' in text.lower(),
        'proper_citation_format': len(re.findall(r'\[\d+\]|\(\d{4}\)', text)) >= 5,
        'has_conclusion': bool(re.search(r'conclusion|결론|맺음말', text, re.IGNORECASE))
    }

    weights = {
        'has_abstract': 0.2,
        'has_sections': 0.25,
        'has_references': 0.2,
        'has_figures_tables': 0.15,
        'proper_citation_format': 0.1,
        'has_conclusion': 0.1
    }

    return sum(weights[key] * (1 if value else 0) for key, value in structure_elements.items())
```

#### D. **한국어 공문서** - 형식과 정확성
```python
class KoreanOfficialDocOptimizer:
    """한국어 공문서 파싱 품질 최적화"""

    @staticmethod
    def optimize_korean_official_parsing(file_path: str) -> Dict[str, Any]:
        """한국어 공문서 최적화 파싱"""

        # 1단계: 한국어 특화 파서 우선
        korean_optimized_parsers = [
            ('upstage', {
                'ocr': {
                    'model': 'premium',
                    'language': ['ko', 'en'],
                    'enhance_korean': True
                },
                'layout': {
                    'preserve_order': True,
                    'extract_forms': True
                }
            }),
            ('easyocr', {
                'languages': ['ko', 'en'],
                'paragraph': True,
                'width_ths': 0.7,
                'height_ths': 0.7
            }),
            ('azure', {
                'locale': 'ko-KR',
                'extract_forms': True
            })
        ]

        best_result = None
        highest_korean_score = 0

        for parser_name, settings in korean_optimized_parsers:
            result = parse_with_parser(parser_name, file_path, settings)

            # 한국어 공문서 품질 검사
            korean_score = validate_korean_official_quality(result)

            if korean_score > highest_korean_score:
                highest_korean_score = korean_score
                best_result = result

        return best_result

def validate_korean_official_quality(result: Dict) -> float:
    """한국어 공문서 품질 검증"""

    text = result.get('text', '')

    korean_official_checks = {
        'proper_korean_grammar': validate_korean_grammar(text),
        'has_official_format': bool(re.search(r'제\s*\d+\s*호|공고|시행|근거', text)),
        'date_format_korean': bool(re.search(r'\d{4}년\s*\d{1,2}월\s*\d{1,2}일', text)),
        'minimal_hanja_errors': validate_hanja_conversion(text),
        'proper_honorifics': validate_korean_honorifics(text),
        'no_broken_hangul': not bool(re.search(r'[ㄱ-ㅎㅏ-ㅣ]', text))  # 자모 분리 확인
    }

    weights = {
        'proper_korean_grammar': 0.25,
        'has_official_format': 0.2,
        'date_format_korean': 0.15,
        'minimal_hanja_errors': 0.15,
        'proper_honorifics': 0.15,
        'no_broken_hangul': 0.1
    }

    return sum(weights[key] * score for key, score in korean_official_checks.items())
```

### 🔧 문서별 최적화 설정 자동 선택기

```python
class DocumentTypeOptimizer:
    """문서 유형 자동 감지 및 최적화 적용"""

    def __init__(self):
        self.optimizers = {
            'legal': LegalDocumentOptimizer(),
            'financial': FinancialDocumentOptimizer(),
            'academic': AcademicPaperOptimizer(),
            'korean_official': KoreanOfficialDocOptimizer()
        }

    def auto_optimize_parsing(self, file_path: str) -> Dict[str, Any]:
        """문서 유형 자동 감지하여 최적화 파싱"""

        # 1단계: 문서 유형 예측
        doc_type = self.detect_document_type(file_path)

        # 2단계: 해당 유형 최적화 적용
        if doc_type in self.optimizers:
            result = self.optimizers[doc_type].optimize_parsing(file_path)
            result['detected_type'] = doc_type
            result['optimization_applied'] = True
        else:
            # 일반 파싱
            result = self.generic_parsing(file_path)
            result['detected_type'] = 'general'
            result['optimization_applied'] = False

        return result

    def detect_document_type(self, file_path: str) -> str:
        """문서 유형 자동 감지"""

        # 빠른 샘플 텍스트 추출 (첫 2페이지)
        sample_text = self.extract_sample_text(file_path)

        # 키워드 기반 분류
        type_indicators = {
            'legal': ['계약서', '약정서', '합의서', '조항', '당사자', 'contract', 'agreement', '제 조'],
            'financial': ['재무제표', '손익계산서', '대차대조표', '매출', '비용', '자산', 'financial statement'],
            'academic': ['abstract', '초록', 'references', '참고문헌', 'conclusion', '그림', 'figure'],
            'korean_official': ['공고', '시행', '근거', '법령', '고시', '규정', '제 호']
        }

        # 점수 기반 분류
        type_scores = {}
        for doc_type, keywords in type_indicators.items():
            score = sum(1 for keyword in keywords if keyword in sample_text)
            type_scores[doc_type] = score / len(keywords)

        # 최고 점수 유형 반환 (임계값 0.2 이상)
        best_type = max(type_scores, key=type_scores.get)
        if type_scores[best_type] >= 0.2:
            return best_type

        return 'general'

# 사용 예시
optimizer = DocumentTypeOptimizer()
result = optimizer.auto_optimize_parsing("계약서.pdf")
print(f"감지된 문서 유형: {result['detected_type']}")
print(f"최적화 적용: {result['optimization_applied']}")
print(f"품질 점수: {result.get('quality_score', 'N/A')}")
```

### 9.5 PDF 복구 및 손상 파일 처리

```python
import fitz  # PyMuPDF
import pikepdf
from pdfminer.high_level import extract_text
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io

class RobustPDFParser:
    """손상된 PDF도 처리하는 강력한 PDF 파서"""

    def __init__(self):
        self.parsers = [
            ('pymupdf', self._parse_with_pymupdf),
            ('pikepdf', self._parse_with_pikepdf),
            ('pdfminer', self._parse_with_pdfminer),
            ('recovery', self._parse_with_recovery_mode)
        ]

    def parse_robust_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """여러 방법으로 PDF 파싱 시도"""

        results = {}
        final_text = ""
        parsing_success = False

        for parser_name, parser_func in self.parsers:
            try:
                print(f"🔄 {parser_name} 파서로 시도 중...")

                result = parser_func(pdf_path)
                results[parser_name] = result

                if result['success'] and len(result['text']) > len(final_text):
                    final_text = result['text']
                    parsing_success = True
                    print(f"✓ {parser_name} 파서 성공")

            except Exception as e:
                results[parser_name] = {
                    'success': False,
                    'error': str(e),
                    'text': ''
                }
                print(f"❌ {parser_name} 파서 실패: {str(e)}")

        return {
            'text': final_text,
            'success': parsing_success,
            'parser_results': results,
            'metadata': {
                'total_characters': len(final_text),
                'successful_parsers': [name for name, result in results.items() if result.get('success')]
            }
        }

    def _parse_with_pymupdf(self, pdf_path: str) -> Dict[str, Any]:
        """PyMuPDF로 파싱"""
        doc = fitz.open(pdf_path)
        text_parts = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_parts.append(f"[페이지 {page_num + 1}]\n{text}")

        doc.close()
        full_text = '\n\n'.join(text_parts)

        return {
            'success': len(full_text.strip()) > 0,
            'text': full_text,
            'method': 'pymupdf'
        }

    def _parse_with_pikepdf(self, pdf_path: str) -> Dict[str, Any]:
        """pikepdf로 복구 시도"""
        with pikepdf.Pdf.open(pdf_path) as pdf:
            text_parts = []

            for page_num, page in enumerate(pdf.pages):
                # 페이지 내용 추출 시도
                try:
                    if '/Contents' in page:
                        # 간단한 텍스트 추출 (제한적)
                        page_text = str(page.get('/Contents', ''))
                        if page_text:
                            text_parts.append(f"[페이지 {page_num + 1}]\n{page_text}")
                except:
                    continue

            full_text = '\n\n'.join(text_parts)

            return {
                'success': len(full_text.strip()) > 0,
                'text': full_text,
                'method': 'pikepdf'
            }

    def _parse_with_pdfminer(self, pdf_path: str) -> Dict[str, Any]:
        """PDFMiner로 파싱 (더 강력함)"""
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()

        return {
            'success': len(text.strip()) > 0,
            'text': text,
            'method': 'pdfminer'
        }

    def _parse_with_recovery_mode(self, pdf_path: str) -> Dict[str, Any]:
        """복구 모드 (OCR 포함)"""
        try:
            import pdf2image
            import pytesseract

            # PDF를 이미지로 변환
            pages = pdf2image.convert_from_path(pdf_path, dpi=300)

            text_parts = []
            for page_num, page_image in enumerate(pages):
                # OCR로 텍스트 추출
                page_text = pytesseract.image_to_string(page_image, lang='kor+eng')
                if page_text.strip():
                    text_parts.append(f"[페이지 {page_num + 1} - OCR]\n{page_text}")

            full_text = '\n\n'.join(text_parts)

            return {
                'success': len(full_text.strip()) > 0,
                'text': full_text,
                'method': 'recovery_ocr'
            }

        except ImportError:
            return {
                'success': False,
                'text': '',
                'error': 'OCR 라이브러리가 설치되지 않음 (pdf2image, pytesseract)',
                'method': 'recovery_ocr'
            }

# 사용 예시
robust_parser = RobustPDFParser()
result = robust_parser.parse_robust_pdf("damaged_document.pdf")
print(f"파싱 성공: {result['success']}")
print(f"성공한 파서들: {result['metadata']['successful_parsers']}")
```

### 9.6 Upstage Layout Analysis - 한국 AI 기업의 혁신적 파서

**특장점**:
- 한국어 문서에 특화된 레이아웃 분석
- 복잡한 문서 구조 이해 및 순서 보존
- 높은 정확도의 테이블 및 차트 인식

```python
import requests
import base64
from typing import Dict, Any, List
import json

class UpstageParser:
    """Upstage Layout Analysis API를 활용한 문서 파싱"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.upstage.ai/v1/document-ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def parse_with_upstage(self, file_path: str, ocr_model: str = "premium") -> Dict[str, Any]:
        """Upstage Document AI로 문서 파싱"""

        # 파일을 base64로 인코딩
        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')

        # API 요청 페이로드
        payload = {
            "document": {
                "content": file_content,
                "mime_type": self._get_mime_type(file_path)
            },
            "ocr": {
                "model": ocr_model,  # "basic", "premium"
                "force_ocr": False,  # PDF에서 텍스트가 있어도 OCR 강제 실행
                "language": ["ko", "en"]  # 인식할 언어
            },
            "layout": {
                "extract_tables": True,
                "extract_figures": True,
                "preserve_order": True  # 읽는 순서 보존
            }
        }

        try:
            # Layout Analysis API 호출
            response = requests.post(
                f"{self.base_url}/layout-analysis",
                headers=self.headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return self._process_upstage_results(result)
            else:
                raise Exception(f"Upstage API 오류: {response.status_code} - {response.text}")

        except Exception as e:
            return {
                'text': '',
                'success': False,
                'error': str(e),
                'metadata': {
                    'parser_type': 'upstage',
                    'status': 'failed'
                }
            }

    def _process_upstage_results(self, api_result: Dict) -> Dict[str, Any]:
        """Upstage API 결과를 구조화된 형태로 변환"""

        # 페이지별 결과 처리
        pages_content = []
        all_tables = []
        all_figures = []

        for page in api_result.get('pages', []):
            page_num = page.get('page_number', 1)

            # 텍스트 요소 추출 (읽는 순서대로 정렬됨)
            page_text_parts = []

            for element in page.get('elements', []):
                element_type = element.get('type')

                if element_type == 'text':
                    # 일반 텍스트
                    text = element.get('content', '')
                    if text.strip():
                        page_text_parts.append(text)

                elif element_type == 'table':
                    # 표 데이터 구조화
                    table_data = self._extract_upstage_table(element)
                    if table_data:
                        all_tables.append({
                            'page': page_num,
                            'table_id': element.get('id'),
                            'data': table_data,
                            'bbox': element.get('bbox')
                        })
                        # 테이블을 텍스트에도 포함
                        table_text = self._table_to_text(table_data)
                        page_text_parts.append(f"\n[표 {len(all_tables)}]\n{table_text}")

                elif element_type == 'figure':
                    # 그림/차트 정보
                    figure_info = {
                        'page': page_num,
                        'figure_id': element.get('id'),
                        'caption': element.get('caption', ''),
                        'bbox': element.get('bbox')
                    }
                    all_figures.append(figure_info)

                    # 캡션이 있으면 텍스트에 포함
                    if figure_info['caption']:
                        page_text_parts.append(f"\n[그림 {len(all_figures)}: {figure_info['caption']}]")

            # 페이지 텍스트 구성
            page_content = '\n'.join(page_text_parts)
            if page_content.strip():
                pages_content.append(f"[페이지 {page_num}]\n{page_content}")

        # 전체 문서 텍스트 구성
        full_text = '\n\n'.join(pages_content)

        # 품질 평가
        confidence_scores = []
        for page in api_result.get('pages', []):
            for element in page.get('elements', []):
                if 'confidence' in element:
                    confidence_scores.append(element['confidence'])

        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0

        return {
            'text': full_text,
            'success': len(full_text.strip()) > 0,
            'tables': all_tables,
            'figures': all_figures,
            'metadata': {
                'parser_type': 'upstage',
                'total_pages': len(api_result.get('pages', [])),
                'total_tables': len(all_tables),
                'total_figures': len(all_figures),
                'avg_confidence': avg_confidence,
                'preserve_order': True
            }
        }

    def _extract_upstage_table(self, table_element: Dict) -> List[List[str]]:
        """Upstage 테이블 요소에서 2차원 배열 추출"""

        if 'cells' not in table_element:
            return []

        # 셀 정보를 위치 기반으로 매핑
        cell_map = {}
        max_row = 0
        max_col = 0

        for cell in table_element['cells']:
            row = cell.get('row_index', 0)
            col = cell.get('col_index', 0)
            text = cell.get('content', '').strip()

            cell_map[(row, col)] = text
            max_row = max(max_row, row)
            max_col = max(max_col, col)

        # 2차원 배열로 변환
        table_data = []
        for row in range(max_row + 1):
            row_data = []
            for col in range(max_col + 1):
                cell_text = cell_map.get((row, col), '')
                row_data.append(cell_text)
            table_data.append(row_data)

        return table_data if table_data else []

    def _table_to_text(self, table_data: List[List[str]]) -> str:
        """테이블 데이터를 텍스트로 변환"""
        if not table_data:
            return ""

        text_lines = []
        for row in table_data:
            # 탭으로 구분된 행 생성
            line = '\t'.join(row)
            text_lines.append(line)

        return '\n'.join(text_lines)

    def _get_mime_type(self, file_path: str) -> str:
        """파일 확장자에서 MIME 타입 추론"""
        ext = Path(file_path).suffix.lower()
        mime_types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.tiff': 'image/tiff',
            '.bmp': 'image/bmp'
        }
        return mime_types.get(ext, 'application/octet-stream')

    def parse_with_quality_check(self, file_path: str) -> Dict[str, Any]:
        """품질 검사를 포함한 파싱"""

        # 기본 파싱 시도
        result = self.parse_with_upstage(file_path, ocr_model="premium")

        if not result['success']:
            return result

        # 품질 검사 수행
        quality_issues = self._check_parsing_quality(result)
        result['quality_report'] = quality_issues

        # 품질이 낮으면 재시도 옵션 제안
        if len(quality_issues) > 2:
            result['suggestions'] = [
                "OCR 모델을 'premium'에서 'basic'으로 변경해보세요",
                "이미지 해상도를 높여서 다시 시도해보세요",
                "문서가 스캔본이라면 전처리(대비/밝기 조정)를 고려하세요"
            ]

        return result

    def _check_parsing_quality(self, result: Dict[str, Any]) -> List[str]:
        """파싱 품질 검사"""
        issues = []

        text = result.get('text', '')
        metadata = result.get('metadata', {})

        # 1. 텍스트 길이 검사
        if len(text.strip()) < 100:
            issues.append("추출된 텍스트가 너무 짧습니다 (100자 미만)")

        # 2. 신뢰도 검사
        avg_confidence = metadata.get('avg_confidence', 0)
        if avg_confidence < 0.8:
            issues.append(f"평균 신뢰도가 낮습니다 ({avg_confidence:.2f} < 0.8)")

        # 3. 깨진 문자 검사
        broken_chars = ['□', '■', '◆', '�', '???']
        broken_count = sum(text.count(char) for char in broken_chars)
        if broken_count > len(text) * 0.05:  # 5% 이상
            issues.append("깨진 문자가 많이 발견되었습니다")

        # 4. 테이블 완성도 검사
        tables = result.get('tables', [])
        for i, table in enumerate(tables):
            table_data = table.get('data', [])
            if table_data:
                empty_cells = sum(1 for row in table_data for cell in row if not cell.strip())
                total_cells = sum(len(row) for row in table_data)
                if empty_cells > total_cells * 0.3:  # 30% 이상 빈 셀
                    issues.append(f"테이블 {i+1}에 빈 셀이 많습니다 ({empty_cells}/{total_cells})")

        return issues

# 사용 예시
upstage_parser = UpstageParser(api_key="your-upstage-api-key")

# 기본 파싱
result = upstage_parser.parse_with_upstage("document.pdf")
print(f"파싱 성공: {result['success']}")
print(f"테이블 수: {result['metadata']['total_tables']}")

# 품질 검사 포함 파싱
quality_result = upstage_parser.parse_with_quality_check("complex_document.pdf")
if quality_result.get('quality_report'):
    print("품질 이슈:", quality_result['quality_report'])
if quality_result.get('suggestions'):
    print("개선 제안:", quality_result['suggestions'])
```

## 📋 전체 파서 목록 및 활용 가이드

### 파서 종합 비교표 (2025년 최신)

| 파서명 | 유형 | 품질 | 속도 | 비용 | 한국어 | 특화 기능 | 최적 사용 케이스 |
|--------|------|------|------|------|--------|-----------|------------------|
| **Basic (PyPDF2/docx)** | 로컬 | ★★☆ | ★★★★★ | 무료 | ★★☆ | 빠른 처리 | 간단한 텍스트 문서 |
| **Azure Document Intelligence** | 클라우드 | ★★★★★ | ★★★★ | $$ | ★★★★ | 양식/표 인식 | 프로덕션 엔터프라이즈 |
| **Google Document AI** | 클라우드 | ★★★★★ | ★★★★ | $$ | ★★★ | 스키마 정의 | 대용량 일괄 처리 |
| **AWS Textract** | 클라우드 | ★★★★★ | ★★★★ | $$ | ★★★ | 양식 필드 추출 | 정부/금융 문서 |
| **Upstage Layout Analysis** | 클라우드 | ★★★★★ | ★★★★ | $$ | ★★★★★ | 한국어 특화 | 한국어 복합 문서 |
| **LlamaIndex (PyMuPDF4LLM)** | 로컬 | ★★★★ | ★★★★ | 무료 | ★★★ | LLM 통합 | RAG 파이프라인 |
| **LayoutParser** | 로컬 | ★★★★ | ★★★ | 무료 | ★★☆ | 레이아웃 분석 | 학술 논문/뉴스 |
| **EasyOCR** | 로컬 | ★★★ | ★★★ | 무료 | ★★★★ | 다국어 OCR | 스캔 문서/이미지 |
| **IBM Watson** | 클라우드 | ★★★★ | ★★★ | $$$ | ★★☆ | 엔티티 추출 | 분석/인사이트 |
| **Claude Vision** | 클라우드 | ★★★★ | ★★★ | $$$ | ★★★★ | 멀티모달 AI | 복잡한 시각 문서 |
| **Advanced Table Parser** | 로컬 | ★★★★ | ★★★ | 무료 | ★★☆ | 테이블 특화 | 재무/통계 문서 |
| **Robust PDF Parser** | 로컬 | ★★★ | ★★ | 무료 | ★★☆ | 복구 능력 | 손상된 문서 |

### 🎯 상황별 최적 파서 선택 가이드

#### 1. **비용별 선택**
```python
# 무료 솔루션 (예산: $0)
free_parsers = [
    'Basic (PyPDF2/docx)',      # 간단한 문서
    'LlamaIndex',               # RAG 통합
    'EasyOCR',                  # 스캔 문서
    'LayoutParser',             # 레이아웃 분석
    'Advanced Table Parser',    # 테이블 전문
    'Robust PDF Parser'         # 복구 전문
]

# 저비용 클라우드 (예산: ~$100/월)
low_cost_cloud = [
    'Azure Document Intelligence',  # 최고 가성비
    'Upstage Layout Analysis'       # 한국어 특화
]

# 프리미엄 솔루션 (예산: $500+/월)
premium_solutions = [
    'Claude Vision',     # 최고 이해력
    'IBM Watson',        # 분석 특화
    'AWS Textract'       # 엔터프라이즈급
]
```

#### 2. **문서 유형별 최적 선택**
```python
document_type_recommendations = {
    '일반 업무 문서 (Word/PDF)': [
        '1순위: Azure Document Intelligence',
        '2순위: Basic Parser',
        '3순위: LlamaIndex'
    ],

    '한국어 복합 문서': [
        '1순위: Upstage Layout Analysis',
        '2순위: EasyOCR',
        '3순위: Claude Vision'
    ],

    '재무/회계 문서 (표 중심)': [
        '1순위: AWS Textract',
        '2순위: Advanced Table Parser',
        '3순위: Azure Document Intelligence'
    ],

    '스캔 문서/이미지': [
        '1순위: EasyOCR',
        '2순위: Claude Vision',
        '3순위: Google Document AI'
    ],

    '학술 논문/연구 자료': [
        '1순위: LayoutParser',
        '2순위: LlamaIndex',
        '3순위: Claude Vision'
    ],

    '손상된/오래된 문서': [
        '1순위: Robust PDF Parser',
        '2순위: EasyOCR',
        '3순위: Claude Vision'
    ]
}
```

### 🔍 파싱 품질 확인 체크리스트

#### A. **파싱 전 확인사항**
```python
def pre_parsing_checklist(file_path: str) -> Dict[str, Any]:
    """파싱 전 문서 품질 검사"""

    checks = {
        'file_size': os.path.getsize(file_path),
        'file_extension': Path(file_path).suffix.lower(),
        'is_password_protected': False,  # PDF의 경우 확인
        'estimated_pages': 0,
        'file_corruption': False,
        'image_quality': None  # 이미지 파일의 경우
    }

    # PDF 특별 검사
    if checks['file_extension'] == '.pdf':
        try:
            import fitz
            doc = fitz.open(file_path)
            checks['estimated_pages'] = len(doc)
            checks['is_password_protected'] = doc.needs_pass
            checks['has_text_layer'] = any(page.get_text() for page in doc[:3])  # 첫 3페이지 확인
            doc.close()
        except:
            checks['file_corruption'] = True

    # 이미지 품질 검사
    if checks['file_extension'] in ['.jpg', '.png', '.tiff']:
        try:
            from PIL import Image
            img = Image.open(file_path)
            checks['image_quality'] = {
                'resolution': img.size,
                'mode': img.mode,
                'dpi': img.info.get('dpi', 'unknown')
            }
        except:
            checks['file_corruption'] = True

    return checks
```

#### B. **파싱 후 품질 검증**
```python
def post_parsing_quality_check(parsing_result: Dict[str, Any]) -> Dict[str, Any]:
    """파싱 결과 품질 종합 검사"""

    text = parsing_result.get('text', '')
    quality_report = {
        'overall_score': 0,
        'issues': [],
        'recommendations': [],
        'metrics': {}
    }

    # 1. 텍스트 품질 검사
    text_metrics = {
        'total_length': len(text),
        'meaningful_length': len(text.strip()),
        'line_count': len(text.split('\n')),
        'word_count': len(text.split()),
        'korean_ratio': sum(1 for c in text if '가' <= c <= '힣') / max(len(text), 1),
        'special_char_ratio': sum(1 for c in text if not c.isalnum() and c not in ' \n\t.,!?-()[]{}') / max(len(text), 1)
    }
    quality_report['metrics']['text'] = text_metrics

    # 2. 구조 보존 검사
    structure_score = 0
    if '표' in text or 'table' in text.lower():
        structure_score += 2
    if '[페이지' in text or '[Page' in text:
        structure_score += 2
    if '\t' in text or '|' in text:  # 테이블 구조 추정
        structure_score += 1

    # 3. 신뢰도 검사 (메타데이터가 있는 경우)
    confidence_score = 0
    metadata = parsing_result.get('metadata', {})
    if 'avg_confidence' in metadata:
        confidence_score = metadata['avg_confidence'] * 10
    elif 'accuracy_confidence' in metadata:
        confidence_score = metadata['accuracy_confidence'] * 10

    # 4. 종합 점수 계산
    base_score = min(text_metrics['meaningful_length'] / 1000, 5)  # 기본 점수 (최대 5점)
    quality_report['overall_score'] = min(base_score + structure_score + confidence_score, 10)

    # 5. 문제점 및 개선안 제시
    if text_metrics['meaningful_length'] < 100:
        quality_report['issues'].append("추출된 텍스트가 너무 적습니다")
        quality_report['recommendations'].append("다른 파서를 시도하거나 OCR 설정을 변경해보세요")

    if text_metrics['special_char_ratio'] > 0.3:
        quality_report['issues'].append("특수문자나 깨진 문자가 많습니다")
        quality_report['recommendations'].append("이미지 품질을 높이거나 한국어 특화 파서를 사용해보세요")

    if structure_score == 0 and ('표' in text or 'table' in text.lower()):
        quality_report['issues'].append("표 구조가 제대로 추출되지 않았습니다")
        quality_report['recommendations'].append("테이블 전문 파서를 사용해보세요")

    return quality_report
```

### 🚀 파싱 품질 최적화 전략

#### 1. **단계별 품질 향상 접근법**
```python
class QualityOptimizedParsing:
    """품질 최적화된 파싱 전략"""

    def __init__(self):
        self.quality_thresholds = {
            'excellent': 8.5,
            'good': 7.0,
            'acceptable': 5.0,
            'poor': 3.0
        }

    def progressive_parsing(self, file_path: str) -> Dict[str, Any]:
        """점진적 품질 향상 파싱"""

        parsing_attempts = []
        best_result = None

        # 1단계: 빠른 기본 파싱
        basic_result = self._try_basic_parsing(file_path)
        parsing_attempts.append(('basic', basic_result))

        quality_score = self._calculate_quality_score(basic_result)

        if quality_score >= self.quality_thresholds['good']:
            return self._finalize_result(basic_result, parsing_attempts)

        # 2단계: 중급 파서 시도
        advanced_result = self._try_advanced_parsing(file_path)
        parsing_attempts.append(('advanced', advanced_result))

        quality_score = self._calculate_quality_score(advanced_result)

        if quality_score >= self.quality_thresholds['good']:
            return self._finalize_result(advanced_result, parsing_attempts)

        # 3단계: 프리미엄 파서 시도
        premium_result = self._try_premium_parsing(file_path)
        parsing_attempts.append(('premium', premium_result))

        # 최고 품질 결과 선택
        best_result = max(
            [result for _, result in parsing_attempts],
            key=lambda x: self._calculate_quality_score(x)
        )

        return self._finalize_result(best_result, parsing_attempts)

    def _finalize_result(self, result: Dict, attempts: List) -> Dict:
        """최종 결과 정리 및 품질 리포트 추가"""

        result['parsing_attempts'] = len(attempts)
        result['quality_report'] = post_parsing_quality_check(result)
        result['optimization_suggestions'] = self._get_optimization_suggestions(result)

        return result
```

#### 2. **실시간 품질 모니터링**
```python
def setup_quality_monitoring():
    """파싱 품질 실시간 모니터링 설정"""

    quality_metrics = {
        'daily_parsing_count': 0,
        'average_quality_score': 0.0,
        'parser_success_rates': {},
        'common_issues': {},
        'processing_times': []
    }

    def log_parsing_result(parser_name: str, result: Dict, processing_time: float):
        """파싱 결과 로깅"""

        quality_metrics['daily_parsing_count'] += 1
        quality_metrics['processing_times'].append(processing_time)

        # 파서별 성공률 추적
        if parser_name not in quality_metrics['parser_success_rates']:
            quality_metrics['parser_success_rates'][parser_name] = {'success': 0, 'total': 0}

        quality_metrics['parser_success_rates'][parser_name]['total'] += 1
        if result.get('success', False):
            quality_metrics['parser_success_rates'][parser_name]['success'] += 1

        # 품질 점수 평균 업데이트
        if 'quality_report' in result:
            score = result['quality_report']['overall_score']
            current_avg = quality_metrics['average_quality_score']
            count = quality_metrics['daily_parsing_count']
            quality_metrics['average_quality_score'] = ((current_avg * (count-1)) + score) / count

    return log_parsing_result
```

## 10. 통합 파서 선택 시스템 업그레이드

### 10.1 모든 파서를 포함한 스마트 선택기

```python
class UltimateParserSelector:
    """모든 파서를 포함한 최고급 선택 시스템"""

    def __init__(self):
        self.parsers = {
            'basic': UniversalDocumentParser(),
            'azure': AzureDocumentParser(),
            'google': GoogleDocumentAIParser(),
            'llama': LlamaIndexParser(),
            'layout': LayoutParserProcessor(),
            'easyocr': EasyOCRProcessor(),
            'aws_textract': AWSTextractParser(),
            'watson': IBMWatsonDocumentParser(),
            'claude': ClaudeVisionParser(),
            'upstage': UpstageParser(),
            'table_specialist': AdvancedTableParser(),
            'robust_pdf': RobustPDFParser()
        }

        self.parser_matrix = {
            # 파일 유형별 최적 파서 순위
            '.pdf': ['upstage', 'azure', 'aws_textract', 'robust_pdf', 'llama'],
            '.docx': ['azure', 'google', 'upstage', 'basic', 'watson'],
            '.xlsx': ['basic', 'table_specialist', 'azure'],
            '.jpg': ['upstage', 'claude', 'easyocr', 'azure', 'google'],
            '.png': ['upstage', 'claude', 'easyocr', 'azure', 'google'],
            '.tiff': ['easyocr', 'upstage', 'azure', 'google'],

            # 특수 상황별 추천
            'damaged_pdf': ['robust_pdf', 'easyocr'],
            'complex_table': ['upstage', 'table_specialist', 'aws_textract', 'azure'],
            'handwritten': ['easyocr', 'google', 'azure'],
            'multilingual': ['easyocr', 'claude', 'google'],
            'korean_document': ['upstage', 'easyocr', 'claude'],
            'form_document': ['aws_textract', 'upstage', 'azure', 'claude']
        }

    def auto_parse_ultimate(self, file_path: str, budget: str = 'medium', special_needs: List[str] = None) -> Dict[str, Any]:
        """최종 통합 자동 파싱"""

        file_ext = Path(file_path).suffix.lower()
        special_needs = special_needs or []

        # 파서 우선순위 결정
        priority_parsers = []

        # 파일 확장자 기반 추천
        if file_ext in self.parser_matrix:
            priority_parsers.extend(self.parser_matrix[file_ext])

        # 특수 요구사항 반영
        for need in special_needs:
            if need in self.parser_matrix:
                priority_parsers = self.parser_matrix[need] + priority_parsers

        # 예산 고려한 필터링
        if budget == 'low':
            priority_parsers = [p for p in priority_parsers if p in ['basic', 'robust_pdf', 'table_specialist', 'layout', 'easyocr']]
        elif budget == 'high':
            # 모든 파서 사용 가능
            pass
        else:  # medium
            # 유료 서비스 제한적 사용
            premium_parsers = ['azure', 'google', 'aws_textract', 'watson', 'claude', 'upstage']
            limited_premium = [p for p in priority_parsers if p in premium_parsers][:2]  # 최대 2개
            free_parsers = [p for p in priority_parsers if p not in premium_parsers]
            priority_parsers = limited_premium + free_parsers

        # 중복 제거하며 순서 유지
        seen = set()
        unique_parsers = []
        for parser in priority_parsers:
            if parser not in seen and parser in self.parsers:
                seen.add(parser)
                unique_parsers.append(parser)

        # 파싱 시도
        best_result = None
        best_score = 0
        parsing_attempts = []

        for parser_name in unique_parsers[:3]:  # 최대 3개 파서 시도
            try:
                print(f"🔄 {parser_name} 파서로 파싱 시도...")

                # 파서별 특별 처리
                if parser_name == 'claude' and file_ext not in ['.jpg', '.png', '.tiff']:
                    continue  # 이미지가 아니면 Claude Vision 건너뛰기

                start_time = time.time()
                result = self._execute_parser(parser_name, file_path)
                parse_time = time.time() - start_time

                # 결과 점수 계산
                score = self._calculate_result_score(result, parse_time, parser_name)

                parsing_attempts.append({
                    'parser': parser_name,
                    'success': score > 0,
                    'score': score,
                    'time': parse_time,
                    'text_length': len(result.get('text', ''))
                })

                if score > best_score:
                    best_score = score
                    best_result = result
                    best_result['metadata']['selected_parser'] = parser_name

                print(f"✓ {parser_name} 완료 (점수: {score:.2f}, 시간: {parse_time:.2f}초)")

                # 충분히 좋은 결과면 조기 종료
                if score >= 0.9:
                    break

            except Exception as e:
                parsing_attempts.append({
                    'parser': parser_name,
                    'success': False,
                    'error': str(e)
                })
                print(f"❌ {parser_name} 실패: {str(e)}")

        if best_result is None:
            return {
                'text': '',
                'success': False,
                'metadata': {
                    'selected_parser': 'none',
                    'parsing_attempts': parsing_attempts
                }
            }

        best_result['metadata']['parsing_attempts'] = parsing_attempts
        best_result['metadata']['total_attempts'] = len(parsing_attempts)

        return best_result

# 사용 예시
ultimate_parser = UltimateParserSelector()

# 일반 문서
result = ultimate_parser.auto_parse_ultimate("document.pdf")

# 복잡한 표가 있는 문서
result = ultimate_parser.auto_parse_ultimate(
    "financial_report.pdf",
    budget='high',
    special_needs=['complex_table']
)

# 손상된 PDF
result = ultimate_parser.auto_parse_ultimate(
    "old_document.pdf",
    special_needs=['damaged_pdf']
)

print(f"선택된 파서: {result['metadata']['selected_parser']}")
print(f"텍스트 길이: {len(result['text'])} 문자")
```

## 📊 파싱 성공을 위한 체크포인트

### ✅ 파싱 전 체크리스트
- [ ] 파일 형식과 크기 확인
- [ ] 문서 유형에 적합한 파서 선택
- [ ] 예산과 품질 요구사항 고려
- [ ] 한국어 문서의 경우 Upstage 우선 고려
- [ ] 테스트 파일로 먼저 검증

### ✅ 파싱 후 품질 검증
- [ ] 텍스트 추출 완성도 확인 (최소 95%)
- [ ] 테이블/표 구조 보존 여부
- [ ] 읽는 순서의 논리적 흐름
- [ ] 특수문자/깨진 문자 비율 (<5%)
- [ ] 핵심 정보 누락 여부

### ✅ 최적화 체크포인트
- [ ] 여러 파서 결과 비교 검토
- [ ] 품질 점수 8.0 이상 달성
- [ ] 처리 시간 vs 품질 트레이드오프 고려
- [ ] 비용 효율성 검증
- [ ] 확장성 및 유지보수성 고려

---

## 🎯 최종 권장사항

### 🥇 **최고 품질이 필요한 경우**
```python
# 프리미엄 파싱 파이프라인
result = ultimate_parser.auto_parse_ultimate(
    file_path="critical_document.pdf",
    budget='high',
    special_needs=['korean_document', 'complex_table']
)
```

### 💰 **비용 효율적인 솔루션**
```python
# 경제적 파싱 파이프라인
result = ultimate_parser.auto_parse_ultimate(
    file_path="document.pdf",
    budget='low'
)
```

### ⚡ **균형잡힌 접근법 (권장)**
```python
# 품질과 비용의 최적 균형
result = ultimate_parser.auto_parse_ultimate(
    file_path="document.pdf",
    budget='medium',
    special_needs=['korean_document'] if is_korean_doc else None
)
```

이제 문서 파싱을 API 서비스로 배포하고 다양한 클라이언트에서 호출할 수 있는 완전한 시스템을 갖추었습니다. **12개 파서**(Basic, Azure, Google, AWS, Upstage, LlamaIndex, LayoutParser, EasyOCR, Watson, Claude, 테이블 전문, PDF 복구)를 포함한 종합적인 문서 파싱 솔루션으로, 어떤 문서든 최적의 품질로 처리할 수 있습니다.

**핵심 기억사항**: 문서 파싱이 RAG의 모든 후속 단계 품질을 결정합니다. 특히 **한국어 문서**는 Upstage Layout Analysis를 우선 고려하고, **체계적인 품질 검증**을 통해 파싱 품질을 보장하세요. 초기 투자를 통해 파싱 품질을 확보하면 전체 시스템 ROI가 극대화됩니다.