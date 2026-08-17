# Bandit Level 15 → 16 Writeup

## Goal

> The password for the next level can be retrieved by submitting the password of the current level to port `30001` on localhost using SSL/TLS encryption.

## Solution

The statement requires us to submit the current password to port 30001 on localhost using SSL/TLS encryption. However, the installed `nc` command does not support SSL/TLS connections, so I used `ncat` with the `--ssl` option instead.

```bash
echo pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7 | ncat --ssl localhost 30001
Correct!
kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V
```

## Password

```text
kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V
```
