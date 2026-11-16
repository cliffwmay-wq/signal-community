# Contribute to Signal

Signal is free/open source. Improvements are welcome, especially from people who write differently, communicate in more than one language, or use different professional registers.

## Principles

1. Protect authorship and factual meaning before visual polish.
2. Avoid AI-detector evasion promises and invented authenticity scores.
3. Explain editorial findings with *passage-level evidence*, not a black-box percentage.
4. Keep author profiles and samples private. Never add real user writing to tests without explicit permission.
5. Prefer offline, dependency-light code. No automatic network requests or hidden file rewrites.
6. Write tests for code-point scanning, edge cases in multilingual text, and format parsing; editorial quality also needs qualitative human review.
7. Keep onboarding friendly to first-time Claude users.

## Contribute safely

Create an issue/PR after the project is published to a public repository. State the behavior you are improving, the before/after example (using fabricated or explicitly licensed text), and the risk of unwanted semantic changes. Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts
```

Where available, also run `claude plugin validate --strict .`.

Code and docs are offered under MIT; by contributing, you agree to license your contribution on that basis.
