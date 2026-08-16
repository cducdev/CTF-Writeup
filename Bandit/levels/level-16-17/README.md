# Bandit Level 16 → 17 Writeup

## Goal

> The credentials for the next level can be retrieved by submitting the password of the current level to a port on localhost in the range 31000 to 32000. First find out which of these ports have a server listening on them. Then find out which of those speak SSL/TLS and which don’t. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.

## Solution

First, I created a temporary directory so that I could safely store the files generated during this level:

```bash
bandit16@bandit:~$ mktemp -d
/tmp/tmp.hEnnFpvDRU
bandit16@bandit:~$ cd /tmp/tmp.hEnnFpvDRU
```

I used `nmap` to scan ports 31000 through 32000 on localhost. The `-p` option specifies the port range, while `-sV` detects the service running on each open port. I redirected the output to `scan.txt` so that I could inspect it afterward:

```bash
bandit16@bandit:/tmp/tmp.hEnnFpvDRU$ nmap -sV -p 31000-32000 localhost > scan.txt
```

The scan found five open ports:

```text
PORT      STATE SERVICE     VERSION
31046/tcp open  echo
31518/tcp open  ssl/echo
31691/tcp open  echo
31790/tcp open  ssl/unknown
31960/tcp open  echo
```

Three ports were running an echo service, so they would only return whatever I sent. I filtered the scan results to focus on the two ports using SSL/TLS:

```bash
bandit16@bandit:/tmp/tmp.hEnnFpvDRU$ grep -E 'ssl|tls' scan.txt
31518/tcp open  ssl/echo
31790/tcp open  ssl/unknown
```

Port 31518 was identified as `ssl/echo`, while port 31790 was an unknown SSL service. Therefore, port 31790 looked like the most likely target. I submitted the current password with `ncat --ssl`:

```bash
bandit16@bandit:/tmp/tmp.hEnnFpvDRU$ echo kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V | ncat --ssl localhost 31790
Correct!
-----BEGIN OPENSSH PRIVATE KEY-----
[REDACTED]
-----END OPENSSH PRIVATE KEY-----
```

The server returned a private SSH key instead of a password. I ran the command again and used `sed` to save only the key block, then changed its permissions so that only my user could read and write it:

```bash
bandit16@bandit:/tmp/tmp.hEnnFpvDRU$ echo kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V | ncat --ssl localhost 31790 | sed -n '/BEGIN OPENSSH PRIVATE KEY/,/END OPENSSH PRIVATE KEY/p' > sshkey.private
bandit16@bandit:/tmp/tmp.hEnnFpvDRU$ chmod 600 sshkey.private
```

Finally, I used the private key to log into the next level:

```bash
bandit16@bandit:/tmp/tmp.hEnnFpvDRU$ ssh -i sshkey.private bandit17@localhost -p 2220
```

The private key is the credential for Level 17. I stored my local copy in `assets/sshkey.private`, which is excluded from Git rather than publishing it in this writeup.
