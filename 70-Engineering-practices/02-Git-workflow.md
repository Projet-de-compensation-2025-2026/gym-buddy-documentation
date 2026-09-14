# Git workflow

Work on a focused branch, review the diff and tests, then integrate into the repository's development branch. Releases are tagged from the reviewed release commit. Preserve unrelated work and never rewrite shared branches as part of an ordinary fix.

Commit messages use one-line Angular Conventional Commits:

```
feat(#23): add user login and registration
fix(#23): reject expired login credentials
test(#23): cover refresh token rotation
chore: correct typo
chore(release): release v1.2.0
```

Use an issue number in the scope only when the commit belongs to that verified issue. A pull request number is not automatically a ticket. Choose a meaningful type (`feat`, `fix`, `refactor`, `test`, `docs`, `build`, `ci`, `perf`, `style`, `chore`, `revert`) and a concise imperative description.

Published-history cleanup requires a reviewed old-to-new commit/ref map, backup bundles, tree/topology verification and coordination of consumer pins and clones. Rewriting commits removes old commit signatures and changes all descendant identifiers. Existing release tags must not move without explicit approval.
