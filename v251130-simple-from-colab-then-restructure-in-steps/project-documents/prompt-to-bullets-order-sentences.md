
Task #1
Converted step{step-number}/detailed-tree-step{step-number}-format2.md into the nested markdown bullet style. This keeps the summary-before-tree requirement and uses indented Markdown bullets to show the same run time notes I have in the ASCII version.
The new format mirrors what I now have in CHANGES_step{step-number}_to_step(step-number + 1).md while preserving detailed brackets/notes for each function, helper, and side effect.

Task #2
Consider this example : 
' - config.py creates outputs/ at import time via mkdir(parents=True, exist_ok=True) so the folder exists before any helpers run.'

It is not really clear. The sentence is too long. It should be in multiple parts, but you decide on the parts. Also, logically, the order of items in the sentence is the wrong way round. You must express the order so that clearly matches the order in which the system runs the items at runtime .

In the file, correct the section that uses nested markdown bullets. Rewrite the nested bullet section at the top of detailed-tree-step{step-number}-format2.md so that each sentence is shorter and ordered by run time.
Updated every description to explicitly state the sequence so that the dependency order is crystal clear.