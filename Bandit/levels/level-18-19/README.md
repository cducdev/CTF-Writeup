# Bandit Level 18 → 19 Writeup

## Goal

> The password for the next level is stored in a file called `readme` in the homedirectory. Unfortunately, someone has modified `.bashrc` to log you out when you log in with SSH.

## Solution

Normally, SSH starts an interactive shell after a successful login. In this level, that shell immediately logs me out because of the modified `.bashrc` file.

However, SSH can also execute a command directly on the remote server without opening an interactive shell. Because I only needed to read the `readme` file, I passed `cat readme` as the remote command:

```bash
$ ssh bandit18@bandit.labs.overthewire.org -p 2220 'cat readme'
bandit18@bandit.labs.overthewire.org's password:
KpsOfPkcP7i1FlIExk2QEjyt6dw8dxZI
```

The server executed `cat readme`, returned the file contents, and then closed the connection without starting the interactive shell that would log me out.

## Password

```text
KpsOfPkcP7i1FlIExk2QEjyt6dw8dxZI
```
