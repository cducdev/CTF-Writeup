# Bandit Level 27 → 28 Writeup

## Goal

> There is a git repository at ssh://bandit27-git@bandit.labs.overthewire.org/home/bandit27-git/repo via the port 2220. The password for the user bandit27-git is the same as for the user bandit27.
> From your local machine (not the OverTheWire machine!), clone the repository and find the password for the next level. This needs git installed locally on your machine.

## Solution

I cloned the repository using the password from the previous level:

```bash
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo
```

After cloning, I entered the repository and read the `README` file:

```bash
$ cd repo
$ cat README
The password to the next level is: y8Yd2ssKcpHpud7UvOSOxwamRMzIGIeQ
```

## Password

```text
y8Yd2ssKcpHpud7UvOSOxwamRMzIGIeQ
```
