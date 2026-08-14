## Bandit Level 0 → 1 Writeup

This level requires us to retrieve the contents of the `readme` file located in the home directory of the SSH server.

Connect to the server with password `bandit0`:

```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```

List all files in long format:

```bash
ls -la
```

You will see a file named `readme`. Display its contents with:

```bash
cat readme
```

![Exploit](./assets/exploit.png)

Password for the next level:

```text
6y2kwnwK6grgvwvpvLaa2T1cpFEKOhNR
```
