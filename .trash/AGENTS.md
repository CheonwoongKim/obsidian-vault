# Repository Guidelines

This repository is an Obsidian-based knowledge workspace. Keep changes surgical, well-documented, and consistent with existing note structure and metadata.

## Project Structure & Module Organization
- Notes: `2.Literature Notes/` (e.g., `Reference/에이전트 시스템 구현 방법론.md`)
- Images/diagrams: place alongside the note or in a nearby `assets/` folder and link relatively.
- Each note begins with YAML frontmatter:
  ```yaml
  title: "..."
  type: reference|note|draft
  tags: [분류/하위분류]
  status: active|draft
  date: YYYY-MM-DD
  updated: YYYY-MM-DD
  source: ["...", "..."]
  ```

## Build, Test, and Development Commands
- Preview/edit: open this vault in Obsidian.
- Optional lint (Markdown):
  - `npx markdownlint-cli2 "**/*.md"` – style/lint checks.
  - `npx markdown-link-check README.md` – link validation (replace file as needed).
- Optional format: `pipx run mdformat .` (or `pip install mdformat`).

## Coding Style & Naming Conventions
- Markdown only; use `#`, `##`, `###` for headings; avoid deep nesting.
- Keep prompts, code, and schemas in fenced blocks with a language hint (e.g., ```json, ```yaml, ```mermaid).
- Korean as primary language; keep technical terms in English where standard.
- Filenames: concise-kebab-case or descriptive Korean; avoid spaces where possible.
- Always preserve and update `updated:` in frontmatter on edits.

## Testing Guidelines
- Run markdown lint and fix reported issues.
- Validate internal links and image paths from Obsidian preview.
- For diagrams, ensure Mermaid blocks render and have readable labels.

## Commit & Pull Request Guidelines
- Commit messages (imperative, concise):
  - `docs: clarify execution vs architecture patterns`
  - `docs(reference): add prompt + I/O examples`
- PRs should include:
  - Summary of changes and rationale
  - Affected paths (e.g., `2.Literature Notes/Reference/...`)
  - Screenshots of rendered diagrams (if changed)
  - Checklist: frontmatter updated, links validated, lint passed

## Security & Content Quality
- Do not add secrets, credentials, or personal data.
- Cite sources in `source:` and inline when helpful.
- Prefer factual, verifiable statements; mark uncertainties explicitly.
