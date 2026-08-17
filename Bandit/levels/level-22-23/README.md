# Bandit Level 22 → 23 Writeup

## Goal

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

## Solution

This level was similar to the previous one, so I first went to `/etc/cron.d/` and looked for the cron configuration related to `bandit23`:

```bash
bandit22@bandit:~$ cd /etc/cron.d/
bandit22@bandit:/etc/cron.d$ ls
behemoth4_cleanup  cronjob_bandit23  leviathan5_cleanup
clean_tmp          cronjob_bandit24  manpage3_resetpw_job
cronjob_bandit22   e2scrub_all       otw-tmp-dir

bandit22@bandit:/etc/cron.d$ cat cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh &> /dev/null
```

The configuration showed that `/usr/bin/cronjob_bandit23.sh` was executed every minute as `bandit23`. I then inspected the script to see what it did:

```bash
bandit22@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

The script stores the current username in `myname`. It then hashes the sentence `I am user $myname` with `md5sum` and uses `cut -d ' ' -f 1` to keep only the hash. Finally, it uses that hash as the name of a file in `/tmp` and copies the user's password into it.

At first, I thought I could simply run the script myself. However, it would run as `bandit22`, so `whoami` would return `bandit22` and the script would only copy the password for the current level. Since the cronjob runs the script as `bandit23`, I needed to calculate the hash using `bandit23` instead:

```bash
bandit22@bandit:/etc/cron.d$ echo "I am user bandit23" | md5sum | cut -d ' ' -f 1
8ca319486bfbbc3663ea0fbe81326349
```

This gave me the name of the file created by the cronjob. I then read that file to get the password for the next level:

```bash
bandit22@bandit:/etc/cron.d$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
gKXDTAXnIz3OBxiPjRZ2uqutUlPZrBsw
```

If the file has not been created yet, I only need to wait until the cronjob runs again at the start of the next minute.

## Password

```text
gKXDTAXnIz3OBxiPjRZ2uqutUlPZrBsw
```
