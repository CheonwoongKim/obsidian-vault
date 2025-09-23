---
title: "🗃️ Archive & Promotion Candidates"
type: dashboard
created: 2025-09-20
updated: 2025-09-21
---


## 🔼 Literature → Permanent 승격 후보 (인링크 ≥ 3)
```dataview
TABLE length(file.inlinks) as "Inlinks", date, updated
FROM "2.Literature Notes"
WHERE type = "literature" AND length(file.inlinks) >= 3
SORT length(file.inlinks) desc
```

## 📝 Literature - 완료 표기된 아카이브 후보(status=finalized)
```dataview
TABLE date, updated, length(file.outlinks) as "Outlinks"
FROM "2.Literature Notes"
WHERE type = "literature" AND status = "finalized"
SORT date desc
```

## 📚 Resources - 365일 이상 미갱신
```dataview
TABLE file.mtime as "Last Update"
FROM "6.Resources"
WHERE file.mtime < (date(today) - dur(365 days))
SORT file.mtime asc
```

## 🏠 Areas - 비활성(status=inactive)
```dataview
TABLE updated
FROM "5.Areas"
WHERE type = "area" AND status = "inactive"
SORT updated desc
```

---

Checklist
- [ ] Literature 승격 기준 충족 시 Permanent로 이동 + 연결 업데이트
- [ ] Literature finalized는 7.Archive/7.literature/ 로 이동
- [ ] 오래된 Resources 정리 또는 7.Archive/6.resources/ 이동
- [ ] 비활성 Areas는 7.Archive/5.areas/ 이동
