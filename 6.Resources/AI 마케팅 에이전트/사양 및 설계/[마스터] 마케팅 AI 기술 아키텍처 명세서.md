---
tags: [자료, 상태/마스터, 설계/아키텍처]
title: "[마스터] 마케팅 AI 기술 아키텍처 명세서"
type: resource
category: AI 마케팅 에이전트/사양 및 설계
updated: 2025-09-20
---


---

## 1. 개요

본 문서는 AI 마케팅 자동화 솔루션의 기술 아키텍처, 핵심 데이터 모델, 그리고 외부 시스템 연동 방식을 정의합니다. 이 문서는 개발팀이 제품의 기술적 구현 방향을 이해하고 일관성 있는 개발을 진행하는 것을 돕는 것을 목표로 합니다.

---

## 2. 시스템 아키텍처: 에이전트 기반 시스템

솔루션의 핵심 AI 시스템은 특정 작업을 전문적으로 수행하는 여러 하위 에이전트(Agent)들의 협력으로 동작합니다.

| Agent | Description |
| :--- | :--- |
| **Campaign Planner** | 광고 목적 및 예산 기반으로 최적의 캠페인 기획(예산/타겟/입찰/Creative/실행 전략)을 담당합니다. |
| **Copywriter** | 캠페인 전략에 맞춰 광고 카피(제목, 본문, CTA 등)를 생성합니다. |
| **Image Generator** | 캠페인 전략에 맞춰 광고 이미지를 생성합니다. |
| **Audience Builder** | 캠페인에 사용할 타겟 세그먼트를 생성하고 추천합니다. |
| **Compliance Checker** | 생성된 광고 소재가 법률, 산업별 규제, 내부 가이드라인을 준수하는지 검수합니다. |
| **Performance Optimizer** | 집행 중인 캠페인 성과를 분석하여 예산, 입찰, 타겟 등을 자동으로 수정 및 최적화합니다. |
| **Insights Analyzer** | 캠페인 종료 후, 성과를 종합 분석하여 인사이트 리포트를 생성합니다. |

---

## 3. 데이터 모델: 캠페인 구조

솔루션 내에서 관리되는 광고 캠페인의 데이터는 아래와 같은 표준화된 3단계 계층 구조를 따릅니다.

- **1 캠페인** → **N 광고 그룹** → **M 광고/크리에이티브**

### 3.1. 캠페인 (Campaign)
- **설명**: 광고 전략의 최상위 단위.
- **주요 속성**: `목표(Goal)`, `예산(Budget)`, `기간(Schedule)`, `캠페인 유형(Type)`

### 3.2. 광고 그룹 (Ad Group)
- **설명**: 타겟 고객 및 입찰 전략을 구체화하는 단위.
- **주요 속성**: `타겟(Targeting)`, `입찰 전략(Bid Strategy)`, `노출 위치(Placement)`

### 3.3. 광고 (Ad / Creative)
- **설명**: 사용자에게 노출되는 최종 콘텐츠.
- **주요 속성**: `헤드라인/본문(Text)`, `미디어(Media)`, `랜딩 URL(URL)`, `CTA`

---

## 4. 외부 API 연동 명세

AI 에이전트는 아래의 외부 광고 매체 API와 연동하여 캠페인을 자동으로 생성하고 관리합니다.

### 4.1. Meta Marketing API

- **주요 기능**: 캠페인, 광고 세트, 광고 크리에이티브의 생성 및 상태 변경, 성과 데이터 조회.
- **인증 방식**: OAuth 2.0 기반 `access_token` 사용.
- **핵심 Endpoint 예시 (cURL)**:
    - **캠페인 생성**: `POST /act_<AD_ACCOUNT_ID>/campaigns`
    - **광고 세트 생성**: `POST /act_<AD_ACCOUNT_ID>/adsets`
    - **크리에이티브 생성**: `POST /act_<AD_ACCOUNT_ID>/adcreatives`
    - **성과 조회**: `GET /act_<AD_ACCOUNT_ID>/insights`

### 4.2. Naver Search Ad API

- **주요 기능**: 캠페인, 광고 그룹, 광고, 키워드의 생성 및 관리.
- **인증 방식**: API 라이선스와 시크릿 키를 이용한 헤더 인증.
- **핵심 파라미터**:
    - **캠페인 생성**: `campaignTp`, `name`, `dailyBudget`, `useDailyBudget` 등.
    - **광고 그룹 생성**: `nccCampaignId`, `name`, `pcChannelId`, `mobileChannelId`, `bidAmt` 등.
    - **광고 생성**: `nccAdgroupId`, `type`, `ad` (object) 등.
