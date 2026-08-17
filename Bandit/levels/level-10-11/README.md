# Bandit Level 10 → 11 Writeup

## Goal

> The password for the next level is stored in the file `data.txt`, which contains base64 encoded data

## Solution

Use `base64` command with `-d` (decode) option to decode the contents of data.txt

```bash
bandit10@bandit:~$ base64 -d data.txt
The password is pYfOY6HwUsDj5rL9UvyhU7MCmv8vN5Ro
```

## Password

```text
pYfOY6HwUsDj5rL9UvyhU7MCmv8vN5Ro
```
