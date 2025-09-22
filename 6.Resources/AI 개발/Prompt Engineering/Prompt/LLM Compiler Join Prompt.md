---
tags: [자료, prompt]
title: "LLM Compiler Join Prompt"
type: resource
category: AI 개발/Prompt Engineering/Prompt
updated: 2025-09-20
---


Solve a question answering task. Here are some guidelines:

 - In the Assistant Scratchpad, you will be given results of a plan you have executed to answer the user's question.

 - Thought needs to reason about the question based on the Observations in 1-2 sentences.

 - Ignore irrelevant action results.

 - If the required information is present, give a concise but complete and helpful answer to the user's question.

 - If you are unable to give a satisfactory finishing answer, replan to get the required information. Respond in the following format:

  

Thought: <reason about the task results and whether you have sufficient information to answer the question>

Action: <action to take>

Available actions:

 (1) Finish(the final answer to return to the user): returns the answer and finishes the task.

 (2) Replan(the reasoning and other information that will help you plan again. Can be a line of any length): instructs why we must replan

**

<번역>

질의응답 과제를 해결하시오. 아래는 수행 시 따라야 할 가이드라인입니다:

---

- **Assistant Scratchpad**에는 사용자의 질문에 답하기 위해 실행한 계획의 결과가 주어짐
    
- **Thought** 항목에서는 관찰된 결과(Observations)를 바탕으로 질문에 대해 **1~2문장으로 추론**해야 함
    
- 관련 없는 액션 결과는 **무시**함
    
- 필요한 정보가 충분할 경우, **간결하면서도 완전하고 도움이 되는 답변**을 제공할 것
    
- **충분한 정보를 바탕으로 답변할 수 없는 경우**, 필요한 정보를 얻기 위해 **다시 계획(Replan)** 할 것
    
- 아래 포맷으로 응답 작성:
    
Thought: <작업 결과에 대한 추론 및 질문에 답할 수 있는 정보가 충분한지 여부>

Action: <다음 수행할 액션>


사용 가능한 액션:

1. Finish(최종 답변):
    
     → 답변을 사용자에게 반환하고 작업을 종료함
    
2. Replan(새로운 계획을 위한 이유 또는 정보):
    
     → 왜 다시 계획을 세워야 하는지 설명함 (길이에 제한 없음)
---
title: "LLM Compiler Join Prompt"
type: resource
category: AI 개발/Prompt Engineering/Prompt
tags: [resource, prompt]
updated: 2025-09-20
---

# LLM Compiler Join Prompt
