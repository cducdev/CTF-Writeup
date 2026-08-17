# Bandit Level 30 → 31 Writeup

## Goal

> There is a git repository at `ssh://bandit30-git@bandit.labs.overthewire.org/home/bandit30-git/repo` via the port `2220`. The password for the user `bandit30-git` is the same as for the user `bandit30`.
> From your local machine, clone the repository and find the password for the next level.

## Solution

I first cloned the repository using the password from the previous level:

```bash
git clone ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/repo
```

After cloning, I checked the `README.md` file:

```bash
$ cd repo
$ cat README.md
just an epmty file... muahaha
```

The file did not contain the password, so I checked whether the repository had any Git tags:

```bash
$ git tag
secret
```

The tag name looked interesting, so I used `git show` to display its content:

```bash
$ git show secret
82NkymblpGBYmIXG6ZQ8YldBYstHpfUf
```

## Password

```text
82NkymblpGBYmIXG6ZQ8YldBYstHpfUf
```
