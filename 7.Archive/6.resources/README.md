---
title: "Resources Archive"
type: guide
section: archive/resources
updated: 2025-09-20
---


## 원칙
- 관심 소멸·정보 구식·활용 낮음 → 보관
- 이동 경로: `7.Archive/6.resources/`

## 권장 Frontmatter
```yaml
type: resource
status: archived
updated: YYYY-MM-DD
archived: YYYY-MM-DD
```

## 오래된 자료 목록 (보관본)
```dataview
TABLE archived, updated, category
FROM "7.Archive/6.resources"
WHERE type = "resource"
SORT archived desc
```

