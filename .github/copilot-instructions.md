Purpose
When asked to write git commit messages for this repo, follow these exact rules.

Get data

run this powershell:

powershell -Command "& { Remove-Item diff.txt -ErrorAction SilentlyContinue; '=== git status ===' | Out-File diff.txt -Encoding utf8; git status --porcelain -b | Out-File diff.txt -Append -Encoding utf8; '' | Out-File diff.txt -Append -Encoding utf8; '=== staged diff ===' | Out-File diff.txt -Append -Encoding utf8; git diff --staged | Out-File diff.txt -Append -Encoding utf8; '' | Out-File diff.txt -Append -Encoding utf8; '=== unstaged diff ===' | Out-File diff.txt -Append -Encoding utf8; git diff | Out-File diff.txt -Append -Encoding utf8; '' | Out-File diff.txt -Append -Encoding utf8; '=== untracked files ===' | Out-File diff.txt -Append -Encoding utf8; git ls-files --others --exclude-standard | Out-File diff.txt -Append -Encoding utf8 }"

Input
Read the diff.txt that is at the root of the repo directory.

Rules
```instructions
Purpose
When asked to write git commit messages for this repo, follow these exact rules.

Input
Read the diff.txt that is at the root of the repo directory.

Rules (improved)
- Subject: imperative mood, <=50 characters. Make the subject concise and precise: include a verb and a short scope (file, directory, or component). Do not put implementation details or rationale in the subject.
- Preferred subject format: "Verb(scope): brief summary" or "Verb scope — brief summary". Examples: "Fixes parser: handle empty lines", "Adds data-loader: BMW CSV".
- If you cannot fit a scope within 50 chars, use a short filename or directory name as the scope.
- Context: when useful, state where the action took place using "in/on/at/above/below" phrasing.
- Structure: always produce a single-line subject

Examples
1) Adds a data-loader for ...
2) Fixes(copilot-instructions): clarifies commit-msg rules
2) Fixes code-fence spacing: Step 2 tree
3) Addd commit message guidelines and template
