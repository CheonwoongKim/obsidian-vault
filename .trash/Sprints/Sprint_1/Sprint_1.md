## User Stories

| User Story          | US-1. 사용자는 광고 계정을 통합 관리하고 싶어 한다.                                              |
| ------------------- | ----------------------------------------------------------------------------- |
| Acceptance Criteria |                                                                               |
| AC-1                | Meta Ads 광고 계정 연동(캠페인 생성, 수정, 삭제, 데이터 조회)이 되어야 함                              |
| Prototype&Design    | [link](https://8yvkd3.axshare.com/#id=nzmugc&p=__co9ma_2_0_0_credentials&g=1) |
| Additional Detail   | Facebook 로그인을 통해 Ads_management, Ads_read 권한 부여                               |


| User Story          | US-2. 사용자는 여러 매체 광고 캠페인을 일괄 생성하고 싶어 한다.                                                                                                              |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Acceptance Criteria |                                                                                                                                                       |
| AC-1                | Ads Campaign 을 API 방식으로 솔루션 내에서 생성할 수 있어야 함                                                                                                           |
| AC-2                | Ads Camapaign 을 사용자 or AI 선택적으로 생성할 수 있어야 함                                                                                                           |
| AC-3                | AI가 Ads Campaign 생성 시, 세부 내용을 사용자가 수정할 수 있어야 함                                                                                                        |
| Prototype&Design    | [link](https://8yvkd3.axshare.com/#id=j3cplt&p=__co9ma_1_0_0_campaign&g=1)                                                                            |
| Additional Detail   | - AI Agent 가 Meta Feed Campaign을 생성 후 내부 시스템에 등록<br>- 사용자가 Campaign 확인 후 Campaign 수정 or 실행<br>- AI Agent 가 Meta Feed Campaign을 생성하여, Meta API 연동하여 실행 |

## Requirements

| id            | requirement                                                                                                                                                                                                                                                |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mktg_req_0001 | 광고 계정을 연동하여 솔루션 내부에서 API로 캠페인 생성, 수정, 삭제 등이 가능해야 함<br>- 페이스북 로그인을 통해 광고주의 광고 계정 권한 부여 후 API로 캠페인 생성, 수정, 삭제<br>- 연동된 광고 계정 수정, 삭제 <br>- 연동된 광고 계정을 사용자가 확인 가능(연동일시, 최근 업데이트일시)                                                                             |
| mktg_req_0002 | 메타 Feed 캠페인을 생성할 수 있어야 함<br>- 목표, 예산, 기한, 웹사이트 URL 입력하여 Meta Feed 캠페인 생성 요청<br>- 사용자의 캠페인 생성 요청에 따라 AI Agent가 캠페인 생성<br>- 캠페인 상태 값 표시(generate \| ready \| active \| inactive \| error \| warnin)<br>- 캠페인 생성 후 사용자가 수정 가능<br>- 사용자가 최종 승인 후 캠페인 일정에 따라 실행 |
| mktg_req_0003 | 캠페인 중지/실행 할 수 있어야 함<br>- 캠페인 실행 후 사용자가 캠페인을 중지 가능<br>- 중지된 캠페인을 재실행 가능                                                                                                                                                                                     |
| mktg_req_0004 | 캠페인 생성 요청 시 AI Agent가 사용자 요청에 맞는 캠페인을 세팅해서 제공해야 함<br>- 사용자 요청을 확인하여 AI Agent 가 캠페인 생성<br>- Meta Marketing API 에 요청 양식에 맞춰 캠페인 생성                                                                                                                           |

