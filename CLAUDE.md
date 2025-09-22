---
title: "CLAUDE 시스템 가이드"
type: system-guide
version: v3.2
updated: 2025-09-21
---

# 시스템 가이드: CLAUDE AI 어시스턴트 작업 안내

## 1. 개요

본 문서는 Claude Code (claude.ai/code)가 이 저장소에서 코드를 포함한 작업을 수행할 때 필요한 지침을 제공합니다. 이 저장소는 개인 노트, 작업 프로젝트, 학습 자료를 포함하는 Obsidian Vault이며, 주로 한국어로 작성된 콘텐츠를 포함합니다.

---

## 2. 저장소 구조

```
MyWorks/
├── 1.Inbox/             # 새로운 아이디어 및 정보 수집 (제텔카스텐 진입점)
├── 2.Literature Notes/  # 문헌 노트 (하위 폴더 포함)
│   ├── Fleeting/        # 빠른 생각 및 임시 메모
│   └── Reference/       # 사실 정보 및 참조 자료
├── 3.Permanent Notes/   # 핵심 지식 노트 (제텔카스텐 본질)
├── 4.Projects/          # 마감일과 결과물이 있는 프로젝트 (PARA)
├── 5.Areas/             # 지속적인 관리 책임 영역 (PARA)
├── 6.Resources/         # 미래 참조 자료 (PARA)
├── 7.Archive/           # 보관된 콘텐츠 및 비활성 항목 (상세 구조는 7.Archive/README.md 참고)
├── 8.Templates/         # 모든 유형의 노트 템플릿
├── 9.Attachments/       # 미디어 파일 및 첨부 파일
├── Welcome.md           # 전체 사용자 가이드 및 시스템 개요
└── CLAUDE.md            # 이 파일 - Claude Code를 위한 기술 지침
```

---

## 3. 9폴더 제텔카스텐 + PARA 시스템

### 3.1. 현재 활성 구조 (최상위 레벨)

**제텔카스텐 핵심 (1-3):**
- **1.Inbox/**: 모든 새로운 정보 및 아이디어의 진입점
- **2.Literature Notes/**: 다양한 노트 유형을 처리하는 영역
  - Fleeting/: 빠른 캡처 및 임시 생각
  - Reference/: 사실 데이터 및 원본 자료
- **3.Permanent Notes/**: 자신의 언어로 정제된 지식 (제텔카스텐 본질)

**PARA 방법론 (4-7):**
- **4.Projects/**: 마감일과 결과물이 있는 프로젝트
- **5.Areas/**: 지속적인 관리 책임 영역
- **6.Resources/**: 주제별로 정리된 미래 참조 자료
- **7.Archive/**: 비활성 항목 및 레거시 콘텐츠

**시스템 지원 (8-9):**
- **8.Templates/**: 모든 노트 유형에 대한 표준화된 노트 구조
- **9.Attachments/**: 미디어 파일 및 첨부 파일

### 3.2. 통합 워크플로우
1. **수집** → 1.Inbox/
2. **처리** → 2.Literature Notes/ (Fleeting 또는 Reference 하위 폴더)
3. **개발** → 3.Permanent Notes/ (연결된 지식)
4. **실행** → 4.Projects/ (마감일이 있는 실행 가능한 항목)
5. **유지** → 5.Areas/ (지속적인 책임)
6. **연구** → 6.Resources/ (미래 참조 자료)
7. **보관** → 7.Archive/ (완료되거나 비활성 콘텐츠)

### 3.3. 주요 시스템 파일
- **Welcome.md**: 전체 사용자 가이드 및 튜토리얼 (최상위 레벨)
- **README.md 파일**: 대부분의 폴더에 위치하며 특정 사용법 설명
- **Templates**: 모든 노트 템플릿이 8.Templates/ 폴더에 위치

### 3.4. 최근 프로젝트 (Archive 보관)

#### AI 마케팅 자동화 플랫폼 (CO9MA)
- **위치**: `7.Archive/4.projects/2025/[프로젝트] AI 마케팅 자동화 플랫폼 - 개발중.md`
- **목적**: 캠페인 기획, 크리에이티브 생성, 실행 및 성과 분석을 포함하는 SaaS 기반 AI 마케팅 자동화 플랫폼
- **상태**: 완료(보관)
- **지원 자료**: `6.Resources/AI 마케팅 에이전트/` 폴더에 상세 기획 및 시장 조사 자료

#### AI 기업여신 심사 자동화
- **위치**: `7.Archive/4.projects/2025/[프로젝트] AI 기업여신 심사 자동화 - 기획중.md`
- **목적**: 생성형 AI를 활용한 여신승인신청서 및 심사의견서 초안 자동 생성 시스템
- **상태**: 완료(보관)
- **지원 자료**: `6.Resources/기업여신 분석/` 폴더에 심사 방법론 및 시장 분석 자료

---

## 4. 개발 노트

- 이 저장소는 주로 **9폴더 제텔카스텐 + PARA 통합 시스템**을 사용하는 지식 관리 저장소입니다.
- **활성 작업 공간**: 루트 레벨의 모든 9개 폴더(1-9)가 완전한 시스템을 구성합니다.
- 콘텐츠는 한국어 비즈니스 문서, 기술 사양 및 프로젝트 요구사항을 포함합니다.
- 마크다운 기반 문서 저장소이므로 전통적인 빌드/테스트/린트 명령은 없습니다.
- 파일은 한국어 명명 규칙을 사용하며 비즈니스별 용어를 포함합니다.
- 레거시 콘텐츠는 깔끔한 활성 시스템 유지를 위해 7.Archive/로 이동되었습니다.

---

## 5. 이 저장소와 함께 작업하기

### 5.1. 주요 워크플로우
1. **여기서 시작**: `Welcome.md`를 읽고 전체 시스템 개요 및 튜토리얼을 확인합니다.
2. **새 콘텐츠**: 항상 `1.Inbox/`로 시작하고 통합 워크플로우를 따릅니다.
3. **템플릿**: `8.Templates/`의 템플릿을 사용하여 일관된 노트 구조를 유지합니다.
4. **활성 작업**: 현재 활동을 위해 1-6번 폴더에 집중합니다.
5. **참조**: `7.Archive/`는 기록 정보로만 사용합니다.

### 5.2. 중요 지침
- **한국어 명명 규칙**: 기존 한국어 파일 및 폴더 이름을 존중합니다.
- **첨부 파일**: 모든 미디어 파일은 `9.Attachments/`에 저장합니다.
- **레거시 콘텐츠**: `7.Archive/`의 자료는 일반적으로 그곳에 유지되어야 합니다.
- **시스템 통합**: 제텔카스텐(1-3)과 PARA(4-7)가 함께 작동함을 이해합니다.
- **PRD 파일**: 보관된 콘텐츠의 제품 요구사항 문서는 상세한 비즈니스 요구사항을 포함합니다.

### 5.3. 파일 구성 우선순위
1. **1.Inbox/**: 모든 새로운 정보의 임시 스테이징 영역
2. **2.Literature Notes/**: 정보의 활성 처리 영역
3. **3.Permanent Notes/**: 장기 지식 저장소
4. **4-6 (Projects/Areas/Resources)**: 현재 실행 가능한 콘텐츠
5. **7.Archive/**: 기록 참조 전용

---

## 6. Obsidian 설정

저장소는 `.obsidian/`에 광범위한 Obsidian 플러그인 구성을 포함합니다.
- **Templater**: `8.Templates/`의 템플릿과 함께 사용하여 일관된 노트 생성
- **Dataview**: 9폴더 시스템 내에서 동적 쿼리 및 구성
- **Execute-code**: 노트에서 코드 스니펫 실행
- 더 나은 제텔카스텐 + PARA 워크플로우를 위한 다양한 UI 개선 플러그인
- **기본 첨부 위치**: `9.Attachments/` (Settings > Files & Links > Default location for new attachments)

---

## 7. Claude Code를 위한 주요 파일

### 7.1. 필수 읽기
- [[Welcome.md|Welcome.md]] (ROOT): 전체 시스템 가이드, 튜토리얼, 사용자 매뉴얼
- **CLAUDE.md** (ROOT): 이 파일 - Claude Code를 위한 기술 지침
 - [[5.Areas/System/Dashboard - Weekly Review.md|Weekly Review Dashboard]]: 주간 점검용 대시보드
 - [[5.Areas/System/Dashboard - Archive Candidates.md|Archive & Promotion Candidates]]: 승격/보관 후보 대시보드
 - [[5.Areas/System/Dashboard - Monthly Review.md|Monthly Review Dashboard]]: 월간 점검용 대시보드
 - [[3.Permanent Notes/MOCs/MOC - AI 마케팅.md|MOC - AI 마케팅]] / [[3.Permanent Notes/MOCs/MOC - 기업여신.md|MOC - 기업여신]] / [[3.Permanent Notes/MOCs/MOC - Prompt Engineering.md|MOC - Prompt Engineering]] / [[3.Permanent Notes/MOCs/MOC - RegTech.md|MOC - RegTech]]
 - [[8.Templates/Tags - Style Guide.md|Tags - Style Guide]]

### 7.2. 시스템 구조
- **폴더 가이드**: 각 번호가 매겨진 폴더(1-9)에는 사용법을 설명하는 README.md 파일이 포함되어 있습니다.
- **템플릿**: `8.Templates/`에는 적절한 구조의 모든 노트 템플릿이 포함되어 있습니다.
- **활성 시스템**: 루트 레벨 폴더 1-9가 완전한 활성 작업 공간을 구성합니다.
- **명명 규칙**: 일관된 파일 명명 규칙이 모든 폴더에 적용되었습니다.
  - Literature Notes: `[분석] 주제 - 날짜.md`
  - Permanent Notes: `주제 핵심개념 - 부제목.md`
  - Projects: `[프로젝트] 프로젝트명 - 상태.md`
  - Areas: `[영역] 책임영역명.md`
- **Archive 관리**: `7.Archive/`는 완료/비활성 콘텐츠의 보관소입니다. 하위 구조: `4.projects/`, `5.areas/`, `6.resources/`, `7.literature/` (각 폴더에 README 포함)

### 7.6. Frontmatter 표준 및 중복 제거 원칙

#### 7.6.1. 기본 원칙 (v3.2 업데이트)
- **단일 정보원**: Frontmatter가 모든 메타데이터의 유일한 정보원
- **본문 중복 금지**: 제목, 날짜, 타입, 카테고리 등을 본문에서 반복 기재하지 않음
- **Obsidian 권장사항 준수**: Frontmatter title이 노트 제목으로 자동 표시됨

#### 7.6.2. 폴더별 표준
- 공통적으로 `type` 필드로 노트 유형을 구분하며 Dataview 쿼리에 활용합니다.
- 폴더별 상세 표준은 각 README 참고:
  - Projects: `4.Projects/README.md` (type, kind, status, start/due/updated/completed 등)
  - Literature: `2.Literature Notes/README.md` (type, kind, status, date/updated, source 등)
  - Areas: `5.Areas/README.md` (type, status, priority, review/next_review 등)
  - Resources: `6.Resources/README.md` (type, category, tags, source, status/updated 등)
- 템플릿은 `8.Templates/`에 준비되어 있으며 Frontmatter가 기본 포함됨.

#### 7.6.3. 금지 패턴 (v3.2에서 완전 제거됨)
```markdown
# ❌ 금지: 본문에서 메타데이터 반복
**생성일**: 2025-09-20
**타입**: Resource Note
**카테고리**: 마케팅/시장 분석

# ❌ 금지: Frontmatter title과 동일한 H1 제목
# 제품 요구사항 정의서 (PRD)
```

### 7.3. 작업 우선순위
1. **항상 Welcome.md를 먼저 읽어** 완전한 이해를 얻습니다.
2. **새 콘텐츠의 진입점**으로 항상 `1.Inbox/`를 사용합니다.
3. Welcome.md에 설명된 **통합 워크플로우**를 따릅니다.
4. **9폴더 시스템을 존중**합니다 - 대체 구조를 만들지 않습니다.
5. 일관성을 위해 `8.Templates/`의 **템플릿을 사용**합니다.

### 7.4. 시스템 철학
이것은 **통합된 제텔카스텐 + PARA 시스템**이며:
- **폴더 1-3**: 지식 생성을 위한 제텔카스텐 방법론
- **폴더 4-7**: 실행 가능한 정보 관리를 위한 PARA 방법론
- **폴더 8-9**: 시스템 지원 및 미디어 저장소
- **두 방법론 간의 시너지 효과**에서 마법이 일어납니다.

### 7.5. 2025년 업데이트 사항

#### v3.2 (2025-09-21) - 시스템 정리 및 중복 제거
- **Frontmatter 정리**: 모든 노트에서 Frontmatter와 본문 간 중복 내용 완전 제거
- **제목 통일**: Frontmatter title을 단일 정보원으로 하여 본문 H1 제목 중복 제거 (96개 파일 처리)
- **메타데이터 표준화**: 생성일, 타입, 카테고리 등 중복 메타데이터 블록 제거
- **구조 간소화**: 노트 가독성 향상 및 Obsidian 권장사항 준수
- **Dataview 최적화**: 중복 제거로 인한 동적 쿼리 정확성 개선

#### v3.1 (2025-09-20) - 기본 시스템 완성
- **프로젝트 상태**: AI 마케팅 자동화와 기업여신 심사 자동화 프로젝트 완료 및 Archive 이동
- **시장 동향 반영**: 2025년 AI 트렌드와 RegTech 동향을 반영한 전략적 포지셔닝
- **명명 규칙 표준화**: 모든 폴더에 일관된 파일 명명 규칙 적용
- **README 완성**: 모든 번호 폴더(1-9)에 상세한 사용 가이드 제공
- **연결성 강화**: 프로젝트-자료-지식 간 체계적 연결 구조 완성
