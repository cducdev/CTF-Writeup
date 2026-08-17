# Bandit Level 17 → 18 Writeup

## Goal

> There are 2 files in the homedirectory: `passwords.old` and `passwords.new`. The password for the next level is in `passwords.new` and is the only line that has been changed between `passwords.old` and `passwords.new`

## Solution

I used the `diff` command to find the difference between the two files:

```bash
bandit17@bandit:~$ diff passwords.new passwords.old
42c42
< OQxXZjELndr90zuhOTDYBEomI0SZITXI
---
> qOg5pVOjPx9x9VccyYBADiT4xxyoUB8D
```

In `diff` output, `<` indicates a line from the first file (passwords.new).
Therefore, the changed line is the password for the next level.

## Password

```text
OQxXZjELndr90zuhOTDYBEomI0SZITXI
```
