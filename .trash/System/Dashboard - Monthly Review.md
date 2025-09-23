---
title: "🗓️ Monthly Review Dashboard"
type: dashboard
created: 2025-09-20
updated: 2025-09-21
---


## 🎯 이번 달 목표 점검 (Areas 기반)
```dataview
TABLE area, priority, updated
FROM "5.Areas"
WHERE type = "area" AND status = "active"
SORT priority asc, updated desc
```

## 📁 이번 달 마감 예정 프로젝트
```dataview
TABLE due, status, updated
FROM "4.Projects"
WHERE type = "project" AND due AND month(date(due)) = month(date(today)) AND year(date(due)) = year(date(today))
SORT date(due) asc
```

## 📝 이번 달 작성/갱신 Literature
```dataview
TABLE date, updated
FROM "2.Literature Notes"
WHERE type = "literature" AND (month(date(date)) = month(date(today)) OR month(date(updated)) = month(date(today)))
SORT (choice(updated, date(updated), date(date))) desc
```

## 💎 신규/갱신 Permanent Notes (최근 30일)
```dataview
TABLE updated
FROM "3.Permanent Notes"
WHERE type = "permanent" AND updated >= date(today) - dur(30 days)
SORT updated desc
```

## 📚 오래된 Resources (갱신 180일 경과)
```dataview
TABLE file.mtime as "Last Update", category
FROM "6.Resources"
WHERE file.mtime < (date(today) - dur(180 days))
SORT file.mtime asc
```

## 🗃️ 승격/보관 후보 요약
```dataview
TABLE length(file.inlinks) as "Inlinks", date, updated
FROM "2.Literature Notes"
WHERE type = "literature" AND length(file.inlinks) >= 3
SORT length(file.inlinks) desc
```

---

## ✅ 월간 체크리스트
- [ ] Areas 건강검진 (상태, 목표, 표준 점검)
- [ ] Literature 승격 후보 → Permanent로 재작성
- [ ] Projects 일정/마감 재정렬 및 다음 달 계획
- [ ] 오래된 Resources 업데이트/Archive 이동
- [ ] 태그/링크 정리(고아 노트 여부 점검)
