---
title: "MOC - 기업여신"
type: moc
updated: 2025-09-20
---


## 💎 Permanent Notes
```dataview
TABLE updated
FROM "3.Permanent Notes"
WHERE type = "permanent" AND (
  contains(tags, "RegTech") OR contains(tags, "loan") OR contains(file.name, "여신")
)
SORT updated desc
```

## 📝 Literature (보관 포함)
```dataview
TABLE date, updated
FROM "2.Literature Notes" OR "7.Archive/7.literature"
WHERE type = "literature" AND (
  contains(file.name, "여신") OR contains(tags, "RegTech") OR contains(tags, "AI_finance")
)
SORT (choice(updated, date(updated), date(date))) desc
```

## 🚀 Projects (보관 포함)
```dataview
TABLE completed, updated
FROM "4.Projects" OR "7.Archive/4.projects"
WHERE type = "project" AND (
  contains(tags, "loan") OR contains(tags, "RegTech") OR contains(file.name, "여신")
)
SORT (choice(completed, date(completed), date(updated))) desc
```

## 📚 Resources
```dataview
TABLE category, updated
FROM "6.Resources"
WHERE type = "resource" AND (
  contains(category, "기업여신 분석") OR contains(file.name, "여신") OR contains(tags, "credit")
)
SORT updated desc
```

## 🏠 Areas
```dataview
TABLE priority, updated
FROM "5.Areas"
WHERE type = "area" AND (
  contains(file.name, "금융") OR contains(file.name, "여신")
)
SORT priority asc, updated desc
```
