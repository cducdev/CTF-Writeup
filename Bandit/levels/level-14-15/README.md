# Bandit Level 14 → 15 Writeup

## Goal

> The password for the next level can be retrieved by submitting the password of the current level to port `30000` on localhost.

## Solution

I used `nc` (netcat) to send the current password to `localhost:30000`:

```bash
bandit14@bandit:~$ echo aaWecNkG4FhxJQxz07uiwzVP6bJiYS65 | nc localhost 30000
Correct!
pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7
```

## Password

```text
pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7
```
