Purpose
When asked to write git commit messages for this repo, follow these exact rules.

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
- Preferred subject format: "Verb(scope): brief summary" or "Verb scope — brief summary". Examples: "Fix(parser): handle empty lines", "Add data-loader: BMW CSV".
- If you cannot fit a scope within 50 chars, use a short filename or directory name as the scope.
- Body: optional. Use the body to explain intent, rationale, and any important implementation notes. Wrap at 72 characters.
- Context: when useful, state where the action took place using "in/on/at/above/below" phrasing.
- Footer: use "Fixes #NN" or "Refs #NN" when applicable.
- Structure: always produce a single-line subject, a blank line, then the optional body, a blank line, then the optional footer.

Why this guidance
- Short, structured subjects make commits easy to scan in logs and UIs.
- Reserve details for the body so the subject remains a quick summary.

Examples
1) Add data-loader: BMW CSV
Add a robust loader for the 2010–2024 BMW sales CSV that:
- handles missing lines
- validates headers
Fixes #42

2) Fix code-fence spacing: Step 2 tree
Add a trailing space after the opening Markdown code fence to
standardize formatting and keep behavior-note blocks aligned with
CHANGES_step2_to_step3. No content changes.

3) Add commit message guidelines and template
Add .github/copilot-instructions.md and .gitmessage.txt to
standardize commit messages and provide examples for Copilot.

Generation note
When asked to generate commit messages, follow these rules exactly: produce a concise subject line that matches the preferred format, then the body and footer as separate blocks. Do not place body content in the subject.
```
Add .github/copilot-instructions.md and .gitmessage.txt to standardize commit messages.