---
title: "🔍 Orphan Notes Finder"
type: dashboard
created: 2025-09-20
updated: 2025-09-21
---


## 💎 Permanent (연결 0)
```dataview
TABLE updated
FROM "3.Permanent Notes"
WHERE type = "permanent" AND (length(file.inlinks) + length(file.outlinks)) = 0
SORT updated desc
```

## 📝 Literature (Fleeting/Reference 제외, 연결 0)
```dataview
TABLE date, updated
FROM "2.Literature Notes"
WHERE type = "literature" AND !contains(file.folder, "Fleeting") AND !contains(file.folder, "Reference")
AND (length(file.inlinks) + length(file.outlinks)) = 0
SORT (choice(updated, date(updated), date(date))) desc
```

## 📚 Resources (연결 0)
```dataview
TABLE category, updated
FROM "6.Resources"
WHERE type = "resource" AND (length(file.inlinks) + length(file.outlinks)) = 0
SORT updated desc
```

## 🏠 Areas (연결 0)
```dataview
TABLE priority, updated
FROM "5.Areas"
WHERE type = "area" AND (length(file.inlinks) + length(file.outlinks)) = 0
SORT updated desc
```

---

Checklist
- [ ] 해당 노트를 연결할 상위/관련/하위 노트 탐색 후 링크 추가
- [ ] Literature는 승격 가능성 검토 → Permanent로 재작성
- [ ] Resources는 관련 Projects/Areas에서 참조 링크 추가
- [ ] 필요 없으면 Archive 후보로 이동
