# Bandit Level 19 → 20 Writeup

## Goal

> To gain access to the next level, you should use the setuid binary in the home directory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (`/etc/bandit_pass`), after you have used the setuid binary.

## Solution

I first executed the binary without any arguments to see how it worked:

```bash
bandit19@bandit:~$ ./bandit20-do
Run a command as another user.
  Example: ./bandit20-do whoami
```

The setuid bit allows this binary to run with the effective user ID of its owner, `bandit20`. Therefore, any command passed to `bandit20-do` is executed with the permissions of `bandit20` instead of `bandit19`.

I used it to read the password file for `bandit20`:

```bash
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA
```

## Password

```text
4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA
```
