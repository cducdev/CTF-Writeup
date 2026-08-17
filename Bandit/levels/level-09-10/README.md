# Bandit Level 9 → 10 Writeup

## Goal

> The password for the next level is stored in the file `data.txt` in one of the few human-readable strings, preceded by several ‘=’ characters.

## Solution

Because `data.txt` contains binary data, displaying it directly with `cat` would also print many unreadable characters. I used the `strings` command to extract the human-readable strings from the file.

The password is preceded by several `=` characters, so I piped the output to `grep -E` to filter the results:

```bash
bandit9@bandit:~$ strings data.txt | grep -E '[=]+.*'
========== the
[==p+
=zW}
========== password
Y========== is
k8c=
yo=-
=A@.
.=O],
=l"C"m
j=9$
========== B0s2khmbT9u0geKuOoVGW3JZKhndE3BG
'=5G
```

The `-E` option enables extended regular expressions. In the pattern `[=]+.*`, `[=]+` matches one or more `=` characters, while `.*` matches the remaining characters on the same line.

The output still contained some unrelated strings because the pattern also matched lines with only one `=` character. Among the output, I found the words `the`, `password`, and `is` next to several `=` characters. The final matching line contained the password for the next level.

## Password

```text
B0s2khmbT9u0geKuOoVGW3JZKhndE3BG
```
