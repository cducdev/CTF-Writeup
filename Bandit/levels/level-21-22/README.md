# Bandit Level 21 → 22 Writeup

## Goal

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

## Solution

The challenge pointed me to `/etc/cron.d/`, which contains system-wide cron configurations. I listed the directory and found a file named `cronjob_bandit22`:

```bash
bandit21@bandit:~$ cd /etc/cron.d/
bandit21@bandit:/etc/cron.d$ ls
behemoth4_cleanup  cronjob_bandit23  leviathan5_cleanup
clean_tmp          cronjob_bandit24  manpage3_resetpw_job
cronjob_bandit22   e2scrub_all       otw-tmp-dir

bandit21@bandit:/etc/cron.d$ cat cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
```

The first entry runs the script when the system starts. In the second entry, the five `*` characters mean that the script runs every minute. The user field is `bandit22`, so `/usr/bin/cronjob_bandit22.sh` is executed with the permissions of that user. Both standard output and standard error are redirected to `/dev/null`.

I then inspected the script referenced by the cron configuration:

```bash
bandit21@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

The script changes the temporary file's permissions to `644`, which allows everyone to read it. It then copies the password for `bandit22` into that file. Since the cronjob runs every minute, I could read the generated file directly:

```bash
bandit21@bandit:/etc/cron.d$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
RYVux2rHEm9tiXHmLFzuR7Vhx6AZQMEz
```

## Password

```text
RYVux2rHEm9tiXHmLFzuR7Vhx6AZQMEz
```
