---
title: "MOC - Prompt Engineering"
type: moc
updated: 2025-09-20
---


## 📚 Resources (Prompts)
```dataview
TABLE updated
FROM "6.Resources/AI 개발/Prompt Engineering/Prompt"
WHERE type = "resource"
SORT updated desc
```

## 💎 Permanent Notes (연결된 프롬프트 주제)
```dataview
TABLE updated
FROM "3.Permanent Notes"
WHERE type = "permanent" AND (contains(file.name, "프롬프트") OR contains(tags, "prompt"))
SORT updated desc
```

## 📝 Literature (보관 포함)
```dataview
TABLE date, updated
FROM "2.Literature Notes" OR "7.Archive/7.literature"
WHERE type = "literature" AND (contains(file.name, "프롬프트") OR contains(tags, "prompt"))
SORT (choice(updated, date(updated), date(date))) desc
```

## 🔗 관련 주제 허브
- [[../MOCs/MOC - AI 마케팅.md|MOC - AI 마케팅]]
