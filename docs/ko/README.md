# agentkit

[English](../../README.md) | **한국어** | [日本語](../ja/README.md)

여러 프로젝트에 이식해서 쓰는 **AI 코딩 에이전트용 문서 키트**입니다. 규칙(wiki), 역할(agent), 절차(skill), 언어·프레임워크 지식(stack pack)을 단일 원천(SSOT)으로 관리하고, Claude Code·Codex·GitHub Copilot·Cursor·Gemini CLI가 각자 읽는 형식으로 자동 생성합니다.

> 키트 문서의 1차 독자는 **AI 에이전트**입니다. 토큰 효율과 도구 호환성을 위해 에이전트용 문서는 영어로 쓰고, 보고·커밋·PR은 프로젝트 언어(`project.language`)를 따릅니다.

## 핵심 설계

| 원칙 | 구현 |
|---|---|
| **SSOT** | 하나의 사실은 하나의 파일만 소유하고, 나머지는 링크만 겁니다. 카탈로그·섹션 인덱스·도구별 파일은 원본 frontmatter에서 **생성**되므로 어긋날 수 없습니다. `check`가 끊긴 링크, 중복 문장, 오래된 생성물, 설치된 키트의 로컬 수정을 잡습니다. |
| **에이전트를 위한 문서** | 모든 페이지가 `When` / `Route Away When`으로 시작해 잘못 들어온 에이전트가 바로 빠져나갑니다. 진입점 → 섹션 인덱스 → 소유 페이지, 최대 세 단계 안에서 답을 찾고, 파일 유형별 줄 수 예산이 강제됩니다. |
| **대기업 같은 조직** | 관리·실행·품질·진화 평면과 부서로 나뉩니다. 모든 역할은 `Owns`와 맡지 않는 일(그 일을 맡는 이웃 역할)을 명시해 겹치지 않습니다. |
| **세분화된 역할** | 역할은 언어가 아니라 **표면(surface)**으로 정의하고, 언어·프레임워크 지식은 stack pack으로 조합합니다: `역할 카드 × stack pack × 프로젝트 바인딩` → 예) Next.js 프론트엔드 전문가, FastAPI 백엔드 전문가, Unity 에디터 툴 전문가. 프로젝트는 `extends`로 역할을 더 좁힐 수 있습니다. |
| **스킬** | 이슈·PR, 워크트리, 리팩터링, 코드·의존성·스키마 마이그레이션, 리뷰 렌즈, 문서, 번역, 키트 설치·진화 절차. 스킬은 순서만 소유하고 규칙은 위키에 둡니다. |
| **과거에 머물지 않기** | 모든 파일에 `volatility`·`reviewed` 메타데이터가 있어 주기적으로 재검증되고, tech radar가 도구·모델·표준을 감시하며, change intake로 변화를 흡수합니다. `[scaffold]` 규칙은 모델이 성장하면 정리되고, 버전·마이그레이션 노트가 각 프로젝트에 전달됩니다. |

## 작업 흐름

모든 요청은 같은 순서로 진행됩니다([request-lifecycle.md](../../core/wiki/operating-model/request-lifecycle.md)):

**작업 내용 확인 → 이슈 생성 → `develop` 기준 워크트리 생성 → 작업 → `develop`으로 PR → 작업 중 발견한 이슈 등록**.

`develop`은 개발용, `main`은 배포용입니다. `develop → main`은 릴리스를 요청받았을 때 승격(promotion) PR로만 이루어집니다. 프로젝트는 프로필에서 이 기본값을 바꿀 수 있습니다.

## 구조

```text
core/                  이식되는 키트 본체 (프로젝트에서는 .ai/kit/ 에 복사되며 읽기 전용)
  START.md             세션 시작 라우터 (AGENTS.md에 삽입됨)
  wiki/                규칙: principles, operating-model, workflows, evolution, integration, authoring
  agents/<부서>/        역할 카드                    (CATALOG.md 자동 생성)
  skills/<이름>/        절차                         (CATALOG.md 자동 생성)
  stacks/<종류>/        언어·프레임워크·인프라 지식    (CATALOG.md 자동 생성)
  templates/           scaffold 템플릿과 프로젝트 프로필 스키마
tools/agentkit.py      install, update, sync, check, freshness, new
.ai/project/           이 저장소 자신의 오버레이 (키트로 키트를 관리)
```

설치된 프로젝트의 구조와 도구별 생성 파일은 [installation.md](../../core/wiki/integration/installation.md), [tool-adapters.md](../../core/wiki/integration/tool-adapters.md)에 있습니다. 카탈로그: [역할](../../core/agents/CATALOG.md), [스킬](../../core/skills/CATALOG.md), [stack pack](../../core/stacks/CATALOG.md).

## 빠른 시작

요구 사항: Python 3.11+ (표준 라이브러리만 사용), Git. GitHub 스킬은 `gh` CLI를 사용합니다.

```bash
# 1. 이 저장소를 받은 뒤 대상 프로젝트에 설치
python tools/agentkit.py install ../my-project --tools claude,codex,copilot

# 2. 대상 프로젝트에서 .ai/project/profile.toml 편집: 언어, 명령어, 활성 역할, 경로·스택 바인딩
#    (모든 키 설명은 core/templates/project/profile.toml)

# 3. 생성 및 검증
cd ../my-project
python .ai/kit/tools/agentkit.py sync
python .ai/kit/tools/agentkit.py check
```

이미 `AGENTS.md`·`CLAUDE.md`를 직접 쓰고 있던 프로젝트라면 `sync`가 덮어쓰기를 거부합니다. AI 에이전트에게 **`kit-install` 스킬**을 실행하게 하면 프로젝트 고유 내용을 오버레이로 옮기고 프로필을 채워 줍니다.

### 업데이트

```bash
python .ai/kit/tools/agentkit.py update --from https://github.com/doqltl179/ai-agents --ref v0.1.0
```

키트 파일이 로컬에서 수정되어 있으면 업데이트를 거부합니다. 키트는 프로젝트 안에서 읽기 전용이며, 개선 사항은 `kit-upstream-propose` 스킬로 이 저장소에 제안합니다.

## 키트 유지보수

이 저장소를 AI 도구로 열면 생성된 `AGENTS.md`가 키트 유지보수용 진입점이 됩니다(`kit-librarian`, `role-governor`, `trend-scout` 등이 활성화됨).

- 원본을 수정한 뒤: `python tools/agentkit.py sync` → `python tools/agentkit.py check`
- 테스트: `python -m unittest discover -s tools/tests -v`
- 재검증이 필요한 파일: `python tools/agentkit.py freshness`
- CI(`.github/workflows/kit-health.yml`): 푸시·PR마다 테스트와 `check`, 매주 freshness 점검 후 기한이 지난 파일이 있으면 이슈를 엽니다.
- 진화 절차 전체: [evolution/README.md](../../core/wiki/evolution/README.md)

## 라이선스

[MIT](../../LICENSE)
