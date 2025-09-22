---
title: "4.Projects - 폴더 가이드"
type: guide
section: projects
updated: 2025-09-20
---


이 폴더는 명확한 마감일과 완료 기준이 있는 프로젝트를 관리하는 공간입니다.

## 정의
- **특징**: 마감일이 정해져 있고 완료 기준이 명확한 작업
- **PARA 방법론**: Projects (프로젝트) - 실행 가능성이 가장 높은 항목
- **예시**: "3월까지 블로그 개설", "다음 주 프레젠테이션 준비"

## 프로젝트 판별법
- **질문 1**: "언제까지 완료할 것인가?" → 답할 수 있으면 Project
- **질문 2**: "완료되었다는 것을 어떻게 알 수 있나?" → 명확하면 Project
- **Areas와 구분**: 끝이 없는 일은 5.Areas로 분류

## 관리 원칙
1. **주간 검토**: 매주 진행 상황 점검
2. **완료 즉시 이동**: 7.Archive로 즉시 이동
3. **중단/연기 시**: 이유와 함께 7.Archive로 이동
4. **지속적 관리 필요 시**: 5.Areas로 재분류

## 노트 템플릿
- `8.Templates/Project Note Template.md` 사용 권장
- 프로젝트 개요, 목표, 실행 계획, 진행 상황 등 체계적 관리

## 연결
- **관련 지식**: [[Permanent Notes]] 및 [[Literature Notes]] 링크
- **참고 자료**: [[Resources]] 폴더의 관련 자료 활용
- **영역 관리**: 관련 [[Areas]]와 연결하여 장기적 관점 유지

자세한 사용법은 [[Welcome.md]]를 참조하세요.

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
