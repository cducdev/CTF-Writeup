# Bandit Level 8 → 9 Writeup

## Goal

> The password for the next level is stored in the file `data.txt` and is the only line of text that occurs only once

## Solution

The `uniq` command compares adjacent lines in the input. With the `-u` option, it prints only the lines that occur exactly once. Because duplicate lines must be next to each other for `uniq` to detect them, the input has to be sorted first. Therefore, we will combine the `sort` command with `|` (pipe) to sort the data and then pass it to `uniq`.

```bash
bandit8@bandit:~$ sort data.txt | uniq -u
EjmOSvuAu7sGAHqHVcBDPirRe9T03kxl
```

## Password

```text
EjmOSvuAu7sGAHqHVcBDPirRe9T03kxl
```
