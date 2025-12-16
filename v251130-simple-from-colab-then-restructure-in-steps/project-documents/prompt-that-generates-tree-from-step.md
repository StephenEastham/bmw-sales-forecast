


Ignore all prior conversations. Work only with the code and files inside the specified "step" folder provided in the current context (for example, `step1` or `step2`). If the context refers to `step1`, apply these instructions to `step1`. If it refers to `step2`, apply the same principles to `step2`, and so on.

Goal
- Produce one consolidated, single prompt-friendly instruction that requests an expanded, learner-friendly ASCII tree for the specified step-folder code and to save that tree as a Markdown file inside the same folder.

Instructions (single self-contained prompt)

Do not rely on or repeat previous conversations. Instead, work only with the code in the step folder specified by the context and produce a single ASCII tree that helps a learner understand that code and how it works.

Requirements
1. Scope and constraint:
   - Only read and reason about files under the step folder named in the context (e.g., `step1`, `step2`).
   - Do not modify source code.
   - Do not rely on or repeat any previous conversation content — treat this as a fresh task.

2. Primary deliverable:
   - A single, unified ASCII tree diagram (one diagram only) describing the specified step folder.
   - Save the result as a Markdown file named `DETAILED_TREE.md` inside that same step folder (e.g., `step1/DETAILED_TREE.md` or `step2/DETAILED_TREE.md`).

3. Depth and detail:
   - Expand the existing diagram to be about three times more detailed than a basic file listing.
   - For each file and folder node include:
     - A one-line bracketed note that explicitly describes exactly what happens at that node at runtime (imports, side-effects on import, functions defined, what functions do when called, IO performed, folder creation, file deletion, network calls that do or don’t happen, etc.).
     - For functions: show signature, short purpose, and the step-by-step side effects (file writes, prints, exceptions handled).
     - For constants and variables: show the exact expression used in code and a precise bracketed explanation of what is computed or what side-effect occurs.
   - Go from purely structural (folder → file) down into behavioral detail (module-level import-time behavior, key statements, and typical runtime flows triggered by `main()` or public functions).

4. Reference example in context (no concrete examples in this prompt):
   - The context provided to the executor will include a past example tree to show the expected style and level of detail. The example is called example-detailed-tree.md. Create a tree that is analogous to the example provided in the context and matches its presentation style (single ASCII tree with bracketed notes).

5. Presentation rules for the ASCII tree:
   - Use a standard ASCII tree format with branches (├─, └─, │) and one node per line.
   - Place the bracketed explanation directly after each node on the same line.
   - Include file nodes, function names, constants, and relevant internal statements as children in the tree (e.g., include key functions like `test_infrastructure()` and list their internal steps as subnodes with bracketed behavior).
   - Keep lines concise but informative — each bracketed note should be a precise sentence or two describing behavior and side-effects.

6. What to explain for each function/module:
   - Import-time side effects (e.g., folder creation).
   - Function-level behavior: inputs, outputs, IO (files created/deleted/zipped), prints/logging, exceptions handled, and return values.
   - Example explanation: for a `clean_outputs()`-style function explain how it iterates an outputs directory, deletes files and directories, and catches exceptions — explicitly note disk-side effects.

7. Final file content expectations:
   - Add a short header to the generated `DETAILED_TREE.md` that states the file was generated from the specified step folder's code and the generation date.
   - Include the single expanded ASCII tree with bracketed explanations (no additional separate trees).
   - Conclude with a succinct summary (3–5 bullets) listing the most important side-effects a learner should be aware of when running the main script in the step folder (for example: outputs/ created, files deleted by cleanup helper, test files written, archive/zip created, and note whether any downloads occur in that step).

8. Formatting guidance (follow the past example in context):
   - Use consistent branch characters and indentation throughout.
   - Keep bracketed notes short, precise, and factual.
   - Mirror the presentation style of the example provided in the context when constructing node labels and notes.
