---
id: shell
title: Shell (Bash, sh, PowerShell)
kind: language
applies_to: ["**/*.sh", "**/*.bash", "**/*.ps1", "**/*.psm1"]
related: [docker, github-actions]
volatility: volatile
reviewed: 2026-10-09
sources: ["https://www.gnu.org/software/bash/manual/", "https://pubs.opengroup.org/onlinepubs/9799919799/", "https://github.com/koalaman/shellcheck/wiki", "https://learn.microsoft.com/en-us/powershell/scripting/overview", "https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands"]
---

# Shell (Bash, sh, PowerShell)

## Detect
- Interpreter from the shebang (`#!/usr/bin/env bash`, `#!/bin/sh`) or extension. A `sh` script must stay POSIX: no arrays, `[[ ]]`, `<<<`, or `function` keyword.
- Target OS and runner: CI image, container base image (`/bin/sh` is often dash or BusyBox, not bash), macOS (BSD tools, bash 3.2), Windows.
- PowerShell edition: `#Requires -Version`/`-PSEdition`, and whether callers run `pwsh` (PowerShell 7) or `powershell` (Windows PowerShell 5.1).
- Lint and format config: `.shellcheckrc`, shfmt settings in `.editorconfig`, `PSScriptAnalyzerSettings.psd1`; Pester tests (`*.Tests.ps1`).

## Conventions
- Bash: start with `set -euo pipefail`. POSIX `sh`: `set -eu`, and add `pipefail` only when every target shell supports it.
- Quote every expansion: `"$var"`, `"$@"`, `"$(cmd)"`. Build argument lists as bash arrays, not strings.
- Use `$(...)` not backticks; `[[ ]]` in bash and `[ ]` in `sh`; `printf` instead of `echo` for arbitrary data; `read -r`; `command -v` instead of `which`.
- Declare function variables `local` in bash; handle `cd` failure (`cd "$dir" || exit 1`).
- Create temp files with `mktemp` and remove them in `trap '...' EXIT`.
- Validate paths before deleting: `rm -rf -- "${target:?}"` aborts when the variable is unset or empty. Never `rm -rf` a variable or glob that was not validated.
- PowerShell: start scripts with `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'`; check `$LASTEXITCODE` after native commands.
- PowerShell: name functions `Verb-Noun` with approved verbs (`Get-Verb`); use `[CmdletBinding()]` and typed `param()` with validation attributes; support `-WhatIf` via `SupportsShouldProcess` in destructive functions; write full cmdlet and parameter names, not aliases.

## Verify
- `commands.lint`, or `shellcheck <file>` (add `-s sh` or `-s bash` when there is no shebang); `bash -n <file>` for syntax; `shfmt -d <file>` when the project uses shfmt.
- PowerShell: `Invoke-ScriptAnalyzer -Path <file>`; `Invoke-Pester` when tests exist.
- Run portable scripts on every target OS and shell, for example through the CI matrix.

## Pitfalls
- Unquoted expansions word-split and glob; `for f in $(ls)` breaks on spaces. Iterate globs directly, or use `find ... -print0` with `while IFS= read -r -d ''`.
- `set -e` does not fire inside `if`/`while` conditions, `&&`/`||` lists, or functions called from them; check critical commands explicitly.
- GNU-only forms fail on BSD/macOS: `sed -i` without a suffix argument, `date -d`, `stat -c`. Use portable alternatives or branch on `uname`.
- CRLF line endings break bash scripts (`$'\r': command not found`); keep LF.
- PowerShell functions return every uncaptured value; assign unwanted results to `$null` or cast to `[void]`.
- PowerShell: put `$null` on the left (`$null -eq $x`); with a collection on the left, the comparison filters elements instead.

## Version Notes
- macOS ships bash 3.2 as `/bin/bash`: associative arrays, `mapfile`/`readarray`, and `${var,,}` need bash 4+ (as of 2026-10, per gnu.org bash manual).
- Pipeline chains (`&&`, `||`), the ternary `? :`, and `??` require PowerShell 7+; Windows PowerShell 5.1 rejects them (as of 2026-10, per learn.microsoft.com).
- PowerShell 7 writes UTF-8 without BOM by default; Windows PowerShell 5.1 does not, so pass `-Encoding` explicitly when 5.1 writes files (as of 2026-10, per learn.microsoft.com about_Character_Encoding).
- PowerShell 7.4+ honors `$PSNativeCommandUseErrorActionPreference = $true` to stop on non-zero native exit codes; elsewhere check `$LASTEXITCODE` (as of 2026-10, per learn.microsoft.com).
