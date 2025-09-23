---
title: "📊 Weekly Review Dashboard"
type: dashboard
created: 2025-09-20
updated: 2025-09-20
---


## 🔗 Quick Links
- [[8.Templates/Project Note Template.md|Project Template]]
- [[8.Templates/Literature Note Template.md|Literature Template]]
- [[8.Templates/Permanent Note Template.md|Permanent Template]]
- [[8.Templates/Area Note Template.md|Area Template]]
- [[8.Templates/Resource Note Template.md|Resource Template]]
- [[8.Templates/Dataview Queries.md|Dataview Snippets]]
- [[8.Templates/Obsidian 설정 체크리스트.md|Obsidian 설정 체크리스트]]

---

## 🚀 Active Projects
```dataview
TABLE due, updated
FROM "4.Projects"
WHERE type = "project" AND status = "active"
SORT (choice(due, date(due), date("2100-01-01"))) asc
```

## ⏰ Overdue Projects
```dataview
TABLE due, status
FROM "4.Projects"
WHERE type = "project" AND due AND date(due) < date(today) AND status != "completed"
SORT date(due) asc
```

## ✅ Recently Completed (14d)
```dataview
TABLE completed, updated
FROM "7.Archive/4.projects"
WHERE type = "project" AND completed AND date(completed) >= (date(today) - dur(14 days))
SORT completed desc
```

---

## 📥 Inbox (최근 20개)
```dataview
TABLE file.ctime as "Captured"
FROM "1.Inbox"
SORT file.ctime desc
LIMIT 20
```

## 📝 Literature (최근 14일, 진행중)
```dataview
TABLE date, updated
FROM "2.Literature Notes"
WHERE type = "literature" AND (status = "processing" OR !status) AND date AND date(date) >= date(today) - dur(14 days)
SORT date desc
```

## 💎 Permanent Notes (연결 보강 대상)
```dataview
TABLE length(file.inlinks) as "In", length(file.outlinks) as "Out"
FROM "3.Permanent Notes"
WHERE length(file.inlinks) < 2 OR length(file.outlinks) < 2
SORT (length(file.inlinks) + length(file.outlinks)) asc
```

## 📚 Resources (180일 이상 미갱신)
```dataview
TABLE file.mtime as "Last Update"
FROM "6.Resources"
WHERE file.mtime < (date(today) - dur(180 days))
SORT file.mtime asc
LIMIT 50
```

---

## ✅ Review Checklist
- [ ] 1.Inbox 분류 (5분)
- [ ] Literature 연결/승격 검토 (10분)
- [ ] Projects 일정/마감 업데이트 (10분)
- [ ] Areas 월간/분기 리뷰 체크 (5분)
- [ ] Resources 정리 후보 선별 (5분)
