# Security

## Reporting a vulnerability

Report privately through GitHub: open the repository's **Security** tab and use **Report a vulnerability**, which opens a private advisory visible only to the maintainers.

If that option is not available on this repository yet, open a normal issue that says only that you have a security report and asks for a private channel. Do not put the details, a reproduction, or a token in a public issue.

## What is in scope

This repository ships shell hooks, Python scripts and documentation. The things worth reporting:

- a hook that can be made to pass content it should block, or to execute what it reads
- a path that escapes the project boundary in `scripts/context_paths.py`, `scripts/memory.py`, `scripts/init_context.py` or `scripts/golden_set.py`
- a script that writes outside the repository, or reads a file the caller did not name
- anything that would put personal data into a tracked file: the memory layer refuses `raw-evidence`, `people` and `data` paths in code, and a way around that refusal is a finding

## What is not

The gates are quality controls, not a security boundary: each one has a documented per-content override, and a person with write access to the repository can always bypass them. A report that the override works as documented is not a vulnerability.

There is no deployed service here, no credential in the tree, and nothing that runs on a user's machine except the scripts and hooks a person installs deliberately.
