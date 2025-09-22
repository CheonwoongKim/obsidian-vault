---
title: "Dataview 쿼리 스니펫 모음"
type: guide
tags: [guide, dataview]
date: {{date:YYYY-MM-DD}}
updated: 2025-09-20
---


이 노트는 자주 쓰는 Dataview 쿼리를 모아둔 참고용 스니펫입니다.
사용 전 Community Plugins에서 Dataview 플러그인을 설치/활성화하세요.

## 1) 최근 프로젝트 (활동 순)
```dataview
TABLE file.mtime as "Last Modified"
FROM "4.Projects"
WHERE !contains(file.folder, "7.Archive")
SORT file.mtime desc
LIMIT 20
```

### 활성 프로젝트만 (파일명에 "[프로젝트]" 포함)
```dataview
TABLE file.mtime as "Last Modified"
FROM "4.Projects"
WHERE contains(file.name, "[프로젝트]")
SORT file.mtime desc
```

## 2) 주간 Inbox 처리 대기 항목
```dataview
TABLE file.ctime as "Captured", file.mtime as "Last Update"
FROM "1.Inbox"
WHERE !contains(file.tags, "processed")
SORT file.ctime desc
LIMIT 50
```

## 3) 승격 후보 Literature Notes (인링크 3회 이상)
```dataview
TABLE length(file.inlinks) as "Inlinks"
FROM "2.Literature Notes"
WHERE !contains(file.folder, "Fleeting") AND !contains(file.folder, "Reference")
AND length(file.inlinks) >= 3
SORT length(file.inlinks) desc
```

## 4) 연결 약한 Permanent Notes (보강 대상)
```dataview
TABLE length(file.inlinks) as "Inlinks", length(file.outlinks) as "Outlinks"
FROM "3.Permanent Notes"
WHERE length(file.inlinks) < 2 OR length(file.outlinks) < 2
SORT (length(file.inlinks) + length(file.outlinks)) asc
```

## 5) 180일 이상 갱신 없는 Resources (정리 후보)
```dataview
TABLE file.mtime as "Last Update"
FROM "6.Resources"
WHERE file.mtime < (date(today) - dur(180 days))
SORT file.mtime asc
LIMIT 50
```

## 6) 프로젝트 → 리소스 연결 뷰
```dataview
TABLE file.outlinks as "Outlinks"
FROM "4.Projects"
WHERE length(filter(file.outlinks, (l) => contains(l.path, "6.Resources"))) > 0
SORT file.name asc
```

## 7) Frontmatter 기반 프로젝트 현황
```dataview
TABLE status, kind, due, updated
FROM "4.Projects"
WHERE type = "project"
SORT (choice(due, date(due), date("2100-01-01"))) asc, updated desc
```

### 활성 프로젝트 (status=active)
```dataview
TABLE due, updated
FROM "4.Projects"
WHERE type = "project" AND status = "active"
SORT (choice(due, date(due), date("2100-01-01"))) asc
```

### 기획안만 (kind=proposal)
```dataview
TABLE status, updated
FROM "4.Projects"
WHERE type = "project" AND kind = "proposal"
SORT updated desc
```

### 기한 경과 (overdue)
```dataview
TABLE due, status
FROM "4.Projects"
WHERE type = "project" AND due AND date(due) < date(today) AND status != "completed"
SORT date(due) asc
```

---

Tip: 위 스니펫을 대시보드 노트(예: Weekly Review)에 임베드해 루틴 점검에 활용하세요.
