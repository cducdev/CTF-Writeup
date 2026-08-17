# Bandit Level 32 → 33 Writeup

## Goal

> After all this git stuff, it's time for another escape. Good luck!

## Solution

After logging in as `bandit32`, I was dropped into an uppercase shell:

```bash
WELCOME TO THE UPPERCASE SHELL
>>
```

This shell converts normal commands to uppercase, so commands like `ls` or `cat` will not work as expected. I needed a way to spawn a normal shell.

The trick is to use `$0`. In a shell, `$0` expands to the name of the current shell. Since `$0` does not contain lowercase letters, the uppercase shell does not break it:

```bash
>> $0
$
```

After that, I got a normal shell as `bandit32`, so I could read the password for `bandit33`:

```bash
$ cat /etc/bandit_pass/bandit33
u4P2CyPOwPGLe94RdD9Uo2FxFwvnFswM
```

## Password

```text
u4P2CyPOwPGLe94RdD9Uo2FxFwvnFswM
```
