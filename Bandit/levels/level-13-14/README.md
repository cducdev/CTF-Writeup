# Bandit Level 13 → 14 Writeup

## Goal

> The password for the next level is stored in `/etc/bandit_pass/bandit14` and can only be read by user `bandit14`. For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level. Look at the commands that logged you into previous bandit levels, and find out how to use the key for this level.
> If you need help with this level: a hint file can be found in the home directory.
> Make sure to read the error messages as they are informative.

## Solution

I first copied `sshkey.private` from the server to my local machine with `scp`. The port option for `scp` is an uppercase `-P`:

```bash
$ scp -P 2220 bandit13@bandit.labs.overthewire.org:~/sshkey.private .
```

I then tried to connect to `bandit14` with the downloaded private SSH key:

```bash
$ ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0640 for 'sshkey.private' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "sshkey.private": bad permissions
```

From the error message, I understood that OpenSSH rejected the key because it was accessible by the group. The permission `0640` means that the owner can read and write, the group can read, and others have no permission. I changed it to `0600` so that only the owner could read and write the key:

```bash
$ chmod 600 sshkey.private
```

I retried the SSH connection with the same key:

```bash
$ ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
```

After logging in as `bandit14`, I retrieved the password from the file specified in the challenge:

```bash
bandit14@bandit:~$ cat /etc/bandit_pass/bandit14
aaWecNkG4FhxJQxz07uiwzVP6bJiYS65
```

## Password

```text
aaWecNkG4FhxJQxz07uiwzVP6bJiYS65
```
