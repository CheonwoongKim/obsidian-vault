---
title: "Projects Archive"
type: guide
section: archive/projects
updated: 2025-09-20
---


## 원칙
- 완료/중단 즉시 이동, 완료 정보(frontmatter 및 본문) 기록
- 연도별 폴더에 보관: `7.Archive/4.projects/YYYY/`

## 필수 Frontmatter (권장)
```yaml
type: project
status: completed|cancelled
completed: YYYY-MM-DD
updated: YYYY-MM-DD
```

## 목록 (최근 완료 순)
```dataview
TABLE completed, status, updated
FROM "7.Archive/4.projects"
WHERE type = "project"
SORT completed desc
```

