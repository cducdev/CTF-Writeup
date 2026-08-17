# Bandit Level 31 → 32 Writeup

## Goal

> There is a git repository at `ssh://bandit31-git@bandit.labs.overthewire.org/home/bandit31-git/repo` via the port `2220`. The password for the user `bandit31-git` is the same as for the user `bandit31`.
> From your local machine, clone the repository and find the password for the next level.

## Solution

I first cloned the repository using the password from the previous level:

```bash
git clone ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo
```

After cloning, I read the `README.md` file:

```bash
$ cd repo
$ cat README.md
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master
```

So I needed to create a file named `key.txt` with the required content and push it to the `master` branch. However, I also noticed that the repository had a `.gitignore` file:

```bash
$ cat .gitignore
*.txt
```

This means normal `.txt` files are ignored by Git, so `key.txt` would not be added with a normal `git add`. Because of that, I used `git add -f` to force Git to add it:

```bash
$ echo "May I come in?" > key.txt
$ git add -f key.txt
$ git commit -m "Add key file"
[master <commit-id>] Add key file
 1 file changed, 1 insertion(+)
 create mode 100644 key.txt
```

Then I pushed the commit to the remote repository:

```bash
$ git push origin master
remote: ### Attempting to validate files... ####
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
remote: Well done! Here is the password for the next level:
remote: pWuj5jBQ6IgV0NXwiH6g1pXRF8S1YvbT
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
To ssh://bandit.labs.overthewire.org:2220/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://bandit.labs.overthewire.org:2220/home/bandit31-git/repo'
```

The push was rejected after validation, but that was fine because the remote hook had already checked the file and printed the password for the next level.

## Password

```text
pWuj5jBQ6IgV0NXwiH6g1pXRF8S1YvbT
```
