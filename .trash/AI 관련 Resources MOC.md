# 🗺️ MOC - AI 관련 Resources

> [!info] 자동 업데이트 노트
> 이 노트는 [Dataview](https://github.com/blacksmithgu/obsidian-dataview) 플러그인을 사용하여 자동으로 생성됩니다. `6.Resources` 폴더에 새로운 AI 관련 노트를 추가하면 목록이 자동으로 업데이트됩니다.

## 🤖 LLM & 프롬프트 엔지니어링

프롬프트 엔지니어링, LLM 아키텍처, 관련 도구 등 언어 모델에 특화된 모든 자료를 모아봅니다.

```dataview
TABLE WITHOUT ID
  file.link as "자료명",
  category as "카테고리",
  join(file.tags, ", ") as "태그",
  date as "생성일"
FROM "6.Resources"
WHERE contains(file.tags, "llm") OR contains(file.tags, "prompt-engineering") OR contains(file.tags, "prompt_engineering")
SORT date DESC
```

## 🧠 AI/ML 일반

머신러닝 이론, 데이터 분석, AI 프로젝트 방법론 등 범용적인 AI 기술 자료를 모아봅니다.

```dataview
TABLE WITHOUT ID
  file.link as "자료명",
  category as "카테고리",
  join(file.tags, ", ") as "태그",
  date as "생성일"
FROM "6.Resources"
WHERE (contains(file.tags, "ai") OR contains(file.tags, "ml")) AND !(contains(file.tags, "llm") OR contains(file.tags, "prompt-engineering") OR contains(file.tags, "prompt_engineering"))
SORT date DESC
```

## 📈 AI 마케팅

AI를 마케팅에 활용하는 전략, 도구, 사례 분석 자료를 모아봅니다.

```dataview
TABLE WITHOUT ID
  file.link as "자료명",
  category as "카테고리",
  join(file.tags, ", ") as "태그",
  date as "생성일"
FROM "6.Resources"
WHERE contains(file.tags, "ai-marketing") OR contains(file.tags, "ai_marketing")
SORT date DESC
```
