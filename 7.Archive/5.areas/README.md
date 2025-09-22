---
title: "Areas Archive"
type: guide
section: archive/areas
updated: 2025-09-20
---


## 원칙
- 더 이상 관리하지 않는 영역을 비활성 처리 후 보관
- 이동 경로: `7.Archive/5.areas/`

## 권장 Frontmatter
```yaml
type: area
status: inactive
updated: YYYY-MM-DD
archived: YYYY-MM-DD
```

## 비활성 영역 목록 (최근 순)
```dataview
TABLE updated, archived
FROM "7.Archive/5.areas"
WHERE type = "area"
SORT (choice(archived, date(archived), date("1900-01-01"))) desc
```

