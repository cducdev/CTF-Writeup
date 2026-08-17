# Bandit Level 29 → 30 Writeup

## Goal

> There is a git repository at `ssh://bandit29-git@bandit.labs.overthewire.org/home/bandit29-git/repo` via the port `2220`. The password for the user `bandit29-git` is the same as for the user `bandit29`.
> From your local machine, clone the repository and find the password for the next level.

## Solution

From the previous level, I already got the password for `bandit29`. That password is only used to access this level's Git repository, so I cloned the new repository for `bandit29-git`:

```bash
git clone ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo
```

After cloning, I checked the `README.md` file:

```bash
$ cd repo
$ cat README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: <no passwords in production!>
```

The password was not in the `master` branch. Since this is a Git repository, I checked whether there were other branches:

```bash
$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev
```

The `dev` branch looked interesting, so I checked it out and read the file again:

```bash
$ git checkout dev
Switched to a new branch 'dev'
branch 'dev' set up to track 'origin/dev'.

$ cat README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: jq9Dfg2rXsfYsWMgFuKlXhphjdH7USgX
```

## Password

```text
jq9Dfg2rXsfYsWMgFuKlXhphjdH7USgX
```
