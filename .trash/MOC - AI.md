# 🗺️ MOC - AI

> [!info] 자동 업데이트 노트
> 이 노트는 [Dataview](https://github.com/blacksmithgu/obsidian-dataview) 플러그인을 사용하여 'ai' 태그가 포함된 모든 노트를 종류별로 자동 분류합니다.

## 💎 핵심 원리 (Permanent Notes)
*AI에 대한 나만의 핵심 원리와 통찰을 모아봅니다.*
```dataview
TABLE WITHOUT ID
  file.link as "핵심 아이디어",
  join(file.tags, ", ") as "관련 태그"
FROM "3.Permanent Notes"
WHERE contains(file.tags, "ai")
SORT file.mtime DESC
```

## 📝 관련 분석 (Literature Notes)
*AI 관련 외부 자료를 읽고 분석/요약한 노트를 모아봅니다.*
```dataview
TABLE WITHOUT ID
  file.link as "분석 노트",
  category as "카테고리",
  date as "작성일"
FROM "2.Literature Notes"
WHERE contains(file.tags, "ai")
SORT date DESC
```

## 📚 참고 자료 (Resources)
*AI 기술, 도구, 아티클 등 원본 참고 자료를 모아봅니다.*
```dataview
TABLE WITHOUT ID
  file.link as "자료명",
  category as "카테고리",
  date as "생성일"
FROM "6.Resources"
WHERE contains(file.tags, "ai")
SORT date DESC
```

## 🔗 하위 MOC
- [[MOC - 프롬프트 엔지니어링]]
