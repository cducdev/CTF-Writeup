# Bandit Level 28 → 29 Writeup

## Goal

> There is a git repository at `ssh://bandit28-git@bandit.labs.overthewire.org/home/bandit28-git/repo` via the port `2220`. The password for the user `bandit28-git` is the same as for the user `bandit28`.
> From your local machine, clone the repository and find the password for the next level.

## Solution

I first cloned the repository using the password from the previous level:

```bash
git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo
```

After cloning it, I checked the `README.md` file:

```bash
$ cd repo
$ cat README.md
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx
```

At this point, I only saw `xxxxxxxxxx` instead of the real password, so reading the current file was not enough. Since this is a Git repository, I decided to check the commit history to see whether the password had appeared before:

```bash
$ git log --oneline
83d7740 fix info leak
13bbc4d add missing data
f3334fb initial commit of README.md
```

The latest commit was named `fix info leak`, which suggested that some sensitive information might have been removed from the current version. I then checked the previous commit, `13bbc4d`, with `git show`:

```bash
$ git show 13bbc4d
13bbc4d add missing data
diff --git a/README.md b/README.md
index 7ba2d2f..42331d9 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for level29 of bandit.
 ## credentials

 - username: bandit29
-- password: <TBD>
+- password: Em7eGtqaMySwNFjCpwzzHhLhospOcdt0
```

This password is used to log in as `bandit29` and continue with the next level.

## Password

```text
Em7eGtqaMySwNFjCpwzzHhLhospOcdt0
```
