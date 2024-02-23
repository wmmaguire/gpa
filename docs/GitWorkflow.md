# Here is the gist of how to follow a good git branching model
- master: stable release (protected)
- development: unified development branch (protected)
- <initials>/<feature_name>: feature branch

# Here is a list of resourcesful git commands

### navigating branches and viewing status
```
git checkout <existing branch name>
git checkout -b <new branch_name>
git status 
git log
git diff <filename>
```

### update central repo with local changes
```
git add <files/folders>
git commit -m "message (see <git issue number>)"
git push origin <branch>
```
### update local changes with central repo
```
git fetch -p
git branch -D <old/stale branch>
git pull origin <branch name>
```

### merge updates
```
git checkout <source branch>
git rebase -i <target branch>
git merge --no-ff <target branch>
```

### creating a tag
```
git tag <tagname> -a
```

# The general workflow is
1. Create a `feature` branch by branching off of the `development` branch. Make sure that:
	- all changes are covered by unit tests
	- [CHANGELOG.md](CHANGELOG.md) is updated to reflect any changes.
2. Once finished, make sure to rebase your branch with `development` and squash all of your commits to down to one concise commit with a tag linking to its associative issue.
3. Request a merge your feature branch back into `development`  with a reviewer from all code-owners.
4. Upon reaching the release date, `development` will be merged into `master` and a new incremented tag value.
