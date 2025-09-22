---
title: "2.Literature Notes - 폴더 가이드"
type: guide
section: literature
updated: 2025-09-20
---

# 📝 2.Literature Notes - 지식 가공소

## 📖 폴더 목적

2.Literature Notes는 **외부 소스의 정보를 개인적 지식으로 변환**하는 핵심 공간입니다. 제텔카스텐 시스템의 두 번째 단계로, 원본 정보에 자신만의 해석과 연결을 추가합니다.

## 📁 하위 폴더 구조

### 📂 Fleeting/ - 순간적 생각
- 잠깐 떠오른 생각이나 감정
- 완성되지 않은 아이디어 조각
- 나중에 발전시킬 예정인 초안
- **태그**: ` #노트/임시`

### 📂 Reference/ - 사실과 데이터
- 통계, 수치, 날짜 등 객관적 정보
- 인용 가능한 사실들
- 나중에 참조할 데이터
- **태그**: ` #참고`

### 📁 메인 폴더 - 개인적 해석
- 책, 논문, 기사를 읽고 나만의 언어로 정리
- 타인의 아이디어에 내 생각을 더한 내용
- 여러 소스를 종합한 개인적 해석

## 📝 작성 가이드

## 📋 Frontmatter 표준 순서

모든 노트의 Frontmatter는 다음 표준 순서를 따릅니다. 자세한 내용은 [[Welcome.md#Frontmatter 사용 원칙]]을 참조하세요.

```yaml
---
title: # 노트의 제목 (필수)
type: # 노트의 대분류 (예: guide, literature, project, area, resource, permanent)
kind: # 노트의 소분류 (예: fleeting, reference - type이 literature일 경우)
section: # 노트가 속한 섹션 (예: inbox - type이 guide일 경우)
tags: # 관련 태그 목록
status: # 노트의 현재 상태 (예: active, pending, done)
date: # 노트 생성일 (YYYY-MM-DD)
updated: # 노트 최종 수정일 (YYYY-MM-DD)
# 기타 특정 노트 유형에만 해당하는 속성 (예: system_version)
---
```

### Literature Notes 4단계 작성법
1. **📖 출처 명시**: 어디서 나온 정보인지 명확히
2. **🔄 재작성**: 복사 금지! 100% 내 언어로 표현
3. **💭 개인 견해**: 나만의 생각과 해석 추가
4. **🔗 연결 고민**: 기존 노트와의 연결점 찾기

### 템플릿 활용
- [[8.Templates/Literature Note Template.md]] - 메인 문헌 노트용
- [[8.Templates/Fleeting Note Template.md]] - 빠른 생각 기록용

## 🔄 다른 폴더로 이동 시점

### → [[3.Permanent Notes]]로 이동
```
✅ 같은 노트를 3번 이상 참조했을 때
✅ 여러 Literature Notes에서 공통 패턴 발견 시
✅ 완전히 내 것이 되었다고 확신할 때
✅ 완전히 이해해서 누구에게든 설명 가능할 때
```

### 이동 과정
1. Literature Notes의 핵심 아이디어 추출
2. 자립적으로 이해 가능한 형태로 재작성
3. 관련 노트들과 연결
4. 원본 Literature Notes는 그대로 유지

## 💡 사용 팁

- **재작성 원칙**: 절대 복사하지 말고 100% 내 언어로
- **연결 우선**: 작성 시 기존 노트와의 연결점 항상 고려
- **주기적 검토**: 주 1회 Fleeting 폴더 정리하여 발전 가능한 것들 메인으로 이동

## 🏷️ 태그 가이드 (권장)
- 영문 태그는 소문자/스네이크케이스 권장: 예) `ai_marketing`, `regtech`, `credit_scoring`
- 도메인 태그와 상태 태그를 분리: 예) `literature`, `ai_marketing` (+ 필요시 `finalized`)
- 기존 태그와의 호환 유지: 기존 대문자 태그는 유지하되, 신규 작성부터 권장 규칙 적용

## 🧾 메타데이터 가이드
- Frontmatter를 단일 진실원천(SSOT)으로 사용
- 본문 상단의 `생성일/타입` 중복 표기는 선택적으로 제거 가능

## 🔗 관련 링크

- [[Welcome.md]] - 전체 시스템 가이드
- [[1.Inbox/]] - 이전 단계
- [[3.Permanent Notes/]] - 다음 단계
- [[8.Templates/]] - 관련 템플릿들

---

*"Literature Notes는 타인의 지식이 나만의 지식으로 변화하는 마법의 공간입니다."*
