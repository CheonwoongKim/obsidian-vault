---
title: "8.Templates - 폴더 가이드"
type: guide
section: templates
updated: 2025-09-20
---

# 🧰 8.Templates - 템플릿과 가이드

이 폴더는 모든 노트 유형의 표준 템플릿과 작성 가이드를 모아 둔 공간입니다. [[Welcome.md]]에 설명된 10폴더 시스템과 함께 사용하세요.

## 구성
- 템플릿
  - [[8.Templates/Fleeting Note Template.md]]
  - [[8.Templates/Literature Note Template.md]]
  - [[8.Templates/Permanent Note Template.md]]
  - [[8.Templates/Project Note Template.md]]
  - [[8.Templates/Area Note Template.md]]
  - [[8.Templates/Resource Note Template.md]]
  - [[8.Templates/MOC Note Template.md]]
- 가이드
  - [[8.Templates/Inbox Guide.md]]
  - [[8.Templates/Literature Notes Guide.md]]
  - [[8.Templates/Permanent Notes Guide.md]]
  - [[8.Templates/Areas Guide.md]]
  - [[8.Templates/Resources Guide.md]]
  - [[8.Templates/Attachments Guide.md]]

## 사용법
- 복사/붙여넣기: 템플릿을 열어 내용 전체를 복사한 뒤 새 노트에 붙여넣기
- Templater: Obsidian Templater 플러그인과 연동하여 단축키로 삽입
- 맞춤화: 기본 섹션과 태그를 상황에 맞게 조정

## 참고
- 첨부파일 정책: [[9.Attachments/README.md]]
- 전체 시스템 개요: [[Welcome.md]]

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

---
```

---

"일관된 템플릿은 빠른 기록과 쉬운 유지보수를 돕습니다."
