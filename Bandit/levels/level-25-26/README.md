# Bandit Level 25 → 26 Writeup

## Goal

> Logging in to bandit26 from bandit25 should be fairly easy… The shell for user bandit26 is not `/bin/bash`, but something else. Find out what it is, how it works and how to break out of it.

## Solution

At first, I did not have any clear idea for this level. However, I noticed that all levels so far were on the same server, just with different users. From that, I tried to connect Unix users with the information about shells mentioned in the challenge statement.

After looking around on the internet, I found that Unix systems have a file that stores basic user account information. This file is `/etc/passwd`, and each line in this file has the following format:

```yaml
username:password:UID:GID:description:home_directory:login_shell
```

The `login_shell` field represents the program that is executed when we log in as that user.

Combining this with the challenge statement, I thought that the `login_shell` of the `bandit26` user might not be `/bin/bash`, but another program.

To check this, I logged in as `bandit25` and read the content of `/etc/passwd`:

```bash
bandit25@bandit:~$ cat /etc/passwd | grep bandit26
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
```

As we can see, the value of the `login_shell` field is `/usr/bin/showtext`. So I checked what this file does:

```bash
bandit25@bandit:~$ cat /usr/bin/showtext
#!/bin/sh

export TERM=linux

exec more ~/text.txt
exit 0
```

This is a shell script. It sets the `TERM` variable to `linux`, then uses `exec` to replace the current process with the `more` command and opens `~/text.txt`.

At first, I thought about changing the `login_shell` of `bandit26` in `/etc/passwd` back to `/bin/bash`. To check whether that was possible, I looked at the permissions of `/etc/passwd`:

```bash
bandit25@bandit:~$ ls -la /etc/* 2> /dev/null | grep passwd
-rw-r--r-- 1 root root   11191 Jun 24 15:02 /etc/passwd
```

However, `/etc/passwd` is owned by `root` and I only have read permission, so I cannot edit it directly.

While exploring the `more` command, I noticed that it only shows content that fits the current screen. If the content is longer than the screen, `more` stays open and lets us scroll through it, similar to how we read manual pages with `man`.

This gave me another idea. If I make my terminal very small before logging in as `bandit26`, the text file will not fit on the screen, so `more` will stay open instead of exiting immediately.

While inside `more`, I pressed `v` to open the current file in Vim. After entering Vim, I could resize the terminal back to normal.

If I use `:shell` immediately, Vim will use the current default shell, which is still `/usr/bin/showtext`. Because of that, I first changed the shell option to `/bin/bash`:

```vim
:set shell=/bin/bash
```

Then I used `:shell` to spawn an interactive Bash shell as `bandit26`:

```vim
:shell
```

Now I could read the password for `bandit26`:

```bash
bandit26@bandit:~$ cat /etc/bandit_pass/bandit26
jHdv2ELQhT22BkprMNDjybZDAkw1zeBJ
```

## Password

```text
jHdv2ELQhT22BkprMNDjybZDAkw1zeBJ
```
