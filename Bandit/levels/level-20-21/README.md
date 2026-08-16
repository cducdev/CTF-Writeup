# Bandit Level 20 → 21 Writeup

## Goal

> There is a setuid binary in the home directory that does the following: it makes a connection to localhost on the port you specify as a command-line argument. It then reads a line of text from the connection and compares it to the password in the previous level (`bandit20`). If the password is correct, it will transmit the password for the next level (`bandit21`).

## Solution

The `suconnect` binary expects another process to be listening on a local port. That process must send the current password to `suconnect`, which will check it and return the password for the next level over the same connection.

I chose port 3101 and started a listener with `nc`. I piped the current password into the listener and added `&` so that it would run in the background, allowing me to use the same terminal for the next command:

```bash
bandit20@bandit:~$ echo 4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA | nc -l -p 3101 &
[1] 138
```

The shell returned the background job number and process ID, which confirmed that the listener was running. I then passed the same port to `suconnect`:

```bash
bandit20@bandit:~$ ./suconnect 3101
Read: 4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA
Password matches, sending next password
bW9kBv5WC3P4yoDyf12LSdGuNz5ka6hY
[1]+  Done                       echo 4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA | nc -l -p 3101
```

The password matched, so `suconnect` sent the password for `bandit21` back through the connection. After the exchange completed, the background `nc` process exited.

## Password

```text
bW9kBv5WC3P4yoDyf12LSdGuNz5ka6hY
```
