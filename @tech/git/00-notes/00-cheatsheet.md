# Git cheatsheet

## Inspect

```sh
git status -sb                      # short status with branch and upstream
git log --oneline --graph --all     # the whole DAG at a glance
git log -p -- path/to/file          # history of one file, with diffs
git log -S 'needle'                 # commits that added or removed a string
git blame -w -C path/to/file        # who wrote each line, ignoring whitespace and moves
git diff --staged                   # what the next commit will contain
git show HEAD~2:path/to/file        # a file as it was two commits ago
```

## Change history (local branches only)

```sh
git commit --amend --no-edit        # fold staged changes into the last commit
git commit --fixup <sha>            # mark a fix for an older commit...
git rebase -i --autosquash <base>   # ...and squash it into place
git rebase --onto main old new      # move the commits of new that are not in old onto main
git reset --soft HEAD~1             # undo the commit, keep the changes staged
git restore --staged path           # unstage, keep the change in the working tree
git restore path                    # discard working tree changes to path
```

## Shared branches

```sh
git revert <sha>                    # undo by adding a commit, safe on pushed history
git push --force-with-lease         # force, but refuse if someone pushed meanwhile
git pull --rebase                   # replay local commits on top of the remote
```

## Recover

```sh
git reflog                          # every position HEAD has been in: the undo log
git branch rescue <sha-from-reflog> # bring a "lost" commit back
git fsck --lost-found               # dangling commits and blobs reflog no longer shows
```

## Find the bad commit

```sh
git bisect start <bad> <good>
git bisect run make test            # binary search, driven by the test's exit code
git bisect reset
```

## Work on two things at once

```sh
git worktree add ../hotfix main     # second checkout sharing the same repository
git worktree list
git stash push -m "wip" -- path     # shelve changes to specific paths
git stash pop
```

## Plumbing

```sh
git cat-file -t <sha>               # object type: blob, tree, commit, tag
git cat-file -p <sha>               # object content
git rev-parse HEAD~3^2              # resolve any revision expression to a sha
git ls-tree -r HEAD                 # every blob the current commit points at
```

See [`01-snippets/00-content-addressed-objects`](../01-snippets/00-content-addressed-objects/) for blobs and trees built by hand.
