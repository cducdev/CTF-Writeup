# Bandit Level 11 → 12 Writeup

## Goal

> The password for the next level is stored in the file `data.txt`, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions.

## Solution

The description indicates that the contents of `data.txt` were encoded with ROT13. ROT13 replaces each letter with the letter 13 positions after it in the alphabet. Because the alphabet has 26 letters, applying the same rotation again restores the original text.

I used `cat` to read the file and piped the output to the `tr` command:

```bash
bandit11@bandit:~$ cat data.txt | tr 'a-zA-Z' 'n-za-mN-ZA-M'
The password is GROozWPO8QyN0mGrjUkID0WCYkZiQxrN
```

The `tr` command translates characters from the first set, `a-zA-Z`, to the corresponding characters in the second set, `n-za-mN-ZA-M`. This applies ROT13 to both lowercase and uppercase letters and reveals the original text.

## Password

```text
GROozWPO8QyN0mGrjUkID0WCYkZiQxrN
```
