# GEMINI.md - AI Assistant Guide

## 1. Directory Overview

This directory is an Obsidian Vault used for personal knowledge management. It implements a hybrid system combining the **Zettelkasten** method for knowledge creation and the **PARA** method for organizing actionable information. The content is primarily in Korean.

The vault is structured into a 10-folder system:

### Zettelkasten Folders (0-3): 지식 창조의 공간

*   **`0.MOCs/` (Maps of Content)**: 특정 주제에 대한 개요를 제공하고 관련 노트들을 연결하는 '허브' 노트입니다. 지식 네트워크의 입구 역할을 합니다.
*   **`1.Inbox/`**: 처리되지 않은 모든 새로운 정보, 아이디어, 생각을 포착하는 첫 번째 장소입니다.
*   **`2.Literature Notes/`**: 책, 기사, 영상 등 외부 자료를 자신의 언어로 소화하고 개인적인 해석을 더하는 노트입니다. 이 폴더 안에는 다음과 같은 하위 폴더가 있습니다.
    *   **`Fleeting/`**: 정제되지 않은 순간적인 생각이나 임시 메모를 기록합니다.
    *   **`Reference/`**: 문헌 노트를 작성할 때 인용되는 **구체적이고 객관적인 사실 데이터(통계, 날짜, 고유명사 등)**를 저장합니다. 문헌 노트의 '각주'와 같은 역할을 합니다.
*   **`3.Permanent Notes/`**: 문헌 노트에서 충분히 숙성된 아이디어를 자신만의 완전한 지식으로 만들어내는 핵심 공간입니다. 노트는 원자적이고(1노트=1아이디어), 독립적이며, 다른 노트와 긴밀하게 연결됩니다.

### PARA Folders (4-7): 실행과 관리의 공간

*   **`4.Projects/`**: 명확한 목표와 마감일이 있는 구체적인 프로젝트 관련 노트를 관리합니다.
*   **`5.Areas/`**: 건강, 재정, 경력 개발처럼 지속적인 관심과 관리가 필요한 삶의 장기적인 책임 영역을 다룹니다.
*   **`6.Resources/`**: **미래에 활용할 가능성이 있는** 참고 자료의 '개인 도서관'입니다. 당장 처리하지는 않지만, 특정 주제에 관심이 있어 모아두는 기사, 논문, 매뉴얼, 웹사이트 링크 등을 보관합니다. `2.Literature Notes/Reference`가 특정 노트를 뒷받침하는 '사실 조각'이라면, `6.Resources`는 아직 처리되지 않은 '원본 자료 묶음'입니다.
*   **`7.Archive/`**: 완료되었거나 더 이상 활성화되지 않은 프로젝트, 영역, 리소스들을 보관합니다.

### System Folders (8-9)

*   **`8.Templates/`**: This folder contains standardized templates for different types of notes to ensure consistency.
*   **`9.Attachments/`**: This folder is a repository for all non-text files like images, PDFs, etc.

## 2. Key Files

*   **`Welcome.md`**: The main guide to the vault, explaining the Zettelkasten + PARA system, folder structure, and workflows.
*   **`CLAUDE.md`**: A detailed guide for AI assistants, providing context and instructions for interacting with the vault.
*   **`_tag_mapping.json`**: A JSON file that maps tags to their Korean counterparts.
*   **`8.Templates/`**: This directory contains various templates for creating new notes, ensuring consistency across the vault.

## 3. Usage and Workflow

The primary use of this vault is to capture, process, and create knowledge, as well as to manage projects and life areas. The intended workflow is as follows:

1.  **Capture**: New information and ideas are captured in the `1.Inbox`.
2.  **Process**: Information from the inbox is processed into `2.Literature Notes`, where it is summarized and contextualized.
3.  **Synthesize**: Distilled ideas from Literature Notes are turned into `3.Permanent Notes`, which are atomic and densely linked.
4.  **Organize**: Actionable information is organized into `4.Projects`, `5.Areas`, and `6.Resources`.
5.  **Archive**: Completed or inactive items are moved to the `7.Archive`.

## 4. Tagging System

The vault uses a tagging system to categorize and connect notes. The `_tag_mapping.json` file defines the mapping between English and Korean tags. The tags are used to denote the status, type, and topic of a note. For example:

*   `#노트/영구` (permanent note)
*   `#상태/진행중` (status/in-progress)
*   `#주제/AI-마케팅` (topic/AI-marketing)

## 5. Note-Taking Conventions

*   **File Naming**: Files are named in Korean, with a consistent naming convention for different note types (e.g., `[프로젝트] 프로젝트명 - 상태.md`).
*   **Frontmatter**: Each note starts with a YAML frontmatter block containing metadata such as `title`, `type`, `tags`, and `status`.
*   **Templates**: The `8.Templates/` directory provides templates for different note types to ensure consistency.
*   **Linking**: Notes are heavily interlinked to create a network of knowledge, following the Zettelkasten principle.
