---
title: "n8n 워크플로우 자동화 도구"
type: resource
category: 도구/자동화
tags: [tools, workflow, automation, open-source]
status: active
date: 2025-09-20
updated: 2025-09-22
source: https://n8n.io/
---

## 📋 기본 정보

| 항목 | 세부사항 |
|------|----------|
| **도구명** | n8n |
| **공식 사이트** | https://n8n.io/ |
| **깃허브** | https://github.com/n8n-io/n8n |
| **라이선스** | Sustainable Use License |
| **타입** | 워크플로우 자동화 플랫폼 |
| **가격** | 오픈소스 (셀프 호스팅), 클라우드 유료 |

## 🔧 핵심 기능

### 주요 특징
- **시각적 워크플로우 편집기**: 드래그 앤 드롭 방식의 노드 기반 인터페이스
- **600+ 통합**: Slack, Google Sheets, GitHub, OpenAI API 등 다양한 서비스 연동
- **코드 실행**: JavaScript, Python 코드 실행 노드 지원
- **조건부 로직**: if/else, 스위치, 루프 등 복잡한 로직 구현
- **스케줄링**: 크론 기반 자동 실행
- **웹훅 지원**: HTTP 요청 트리거 및 응답

### 지원 통합 (일부)
- **AI/ML**: OpenAI, Anthropic, Hugging Face
- **데이터베이스**: PostgreSQL, MongoDB, MySQL
- **클라우드**: AWS, Google Cloud, Azure
- **협업**: Slack, Discord, Notion, Airtable
- **개발**: GitHub, GitLab, Jenkins

## 💡 활용 사례

### AI 프로젝트 활용
- LLM API 연동 자동화
- 데이터 전처리 파이프라인
- 모델 결과 후처리 및 알림
- 벡터 데이터베이스 업데이트

### 일반 업무 자동화
- 이메일 → 스프레드시트 자동 기록
- GitHub 이슈 → Slack 알림
- CSV 파일 → 데이터베이스 자동 삽입
- 정기 보고서 자동 생성

## 🛠️ 설치 및 설정

### Docker 설치
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  n8nio/n8n
```

### 환경 변수
```env
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=password
N8N_HOST=0.0.0.0
N8N_PORT=5678
```

## 📚 참고 자료

### 공식 문서
- **사용 가이드**: https://docs.n8n.io/
- **노드 레퍼런스**: https://docs.n8n.io/integrations/
- **API 문서**: https://docs.n8n.io/api/

### 커뮤니티
- **포럼**: https://community.n8n.io/
- **Discord**: https://discord.gg/XPKeKXeB
- **YouTube**: https://www.youtube.com/c/n8nio

## 🏷️ 관련 키워드
`workflow-automation` `no-code` `integration` `api-orchestration` `data-pipeline`

