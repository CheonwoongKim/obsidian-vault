#### Input Data(PF)

| **column_en**         | **column_kr** | **example**        |
| --------------------- | ------------- | ------------------ |
| business_name         | 사업장명          | (주)코그넷나인           |
| business_no           | 사업자번호         | 107-87-23907       |
| contact               | 사업장연락처        | 02-6956-0871       |
| manager_name          | 담당자          | 김천웅                |
| branch_name           | 지점명           | OK저축은행 강남구청점       |
| apply_date            | 신청일자          | 2025년 9월 12일       |
| product_name          | 대출상품명         | 종합통장대출 PF          |
| loan_amount           | 대출액           | 120억원              |
| loan_period_months    | 대출기간          | 23개월               |
| interest_rate         | 대출금리          | 6.50%              |
| fee_rate              | 수수료율          | 1.30%              |
| total_rate            | 총수수료율         | 7.80%              |
| repayment_method      | 상환방식          | 만기일시상환(매월후취)       |
| ltv                   | ltv           | 138.70%            |
| guarantor             | 연대보증          | (주)베스핀글로벌          |
| collarteral_type      | 담보종류          | 담보, 신용             |
| region                | 영업구역          | 영업구역내              |
| fund_usage            | 자금용도          | 기존 차입금 상환 및 사업비 등  |
| repayment_source      | 상환재원          | 분양수입금 또는 타 금융기관 대환 |
| credit_class          | 건정성 분류        | 정상(충담금적립률 : 2.0%)  |
| classification_reason | 분류 사유         | 정상                 |
| arranger_fee          | 금융주선수수료       | 정액 180백만원(개별약정)    |
| agent_bank_fee        | 대리은행수수료       | 정률 1.0%(개별약정)      |
| early_repay_fee       | 중도상환수수료       | 없음                 |

대출등록 -> 파일업로드 -> 파싱 -> 후교정 -> 청킹 -> 임베딩 -> 데이터베이스 -> 문서생성 -> 편집 -> 심사요청 -> 심사 -> 완료