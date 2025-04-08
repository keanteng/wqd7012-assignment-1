# How to use Git:

## Basic:
```bash
git commit -m "message"
git push
git pull
git add .
```

## Branching:
```bash
git branch # see the branches
git status # see anything to commit
git checkout <branchname> # switch branch

Put New Branch On Remote
git push --set-upstream origin <branchname>

Delete Branch On Remote
git push origin --delete <branchname>

Delte Branch On Local
git branch -d <branchname>

Create Branch On Local
git checkout -b <branchname>

Merge branch
git merge <branchname> # make sure you are at the branch and merge the other branch
```

## Creating file
```bash
cat > <filaname>
vim <filename>
touch <filename>
```