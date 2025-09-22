---
title: "Literature Archive"
type: guide
section: archive/literature
updated: 2025-09-20
---


## 원칙
- 핵심이 Permanent로 승격되고 원문 필요성 낮으면 보관
- 이동 경로: `7.Archive/7.literature/`

## 권장 Frontmatter
```yaml
type: literature
status: archived
updated: YYYY-MM-DD
archived: YYYY-MM-DD
```

## 보관된 Literature (최근 순)
```dataview
TABLE archived, date, updated
FROM "7.Archive/7.literature"
WHERE type = "literature"
SORT archived desc
```

