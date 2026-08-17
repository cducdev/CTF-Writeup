# OverTheWire Bandit Writeups

This repository contains my solutions and notes for the [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) wargame.

> **Spoiler warning:** Each writeup contains the password for the next level.

## Progress

| Level | Main concept | Writeup |
| ----- | ------------ | ------- |
| 0 → 1 | Reading a file | [View writeup](./levels/level-00-01/) |
| 1 → 2 | Dashed filenames | [View writeup](./levels/level-01-02/) |
| 2 → 3 | Filenames containing spaces | [View writeup](./levels/level-02-03/) |
| 3 → 4 | Hidden files | [View writeup](./levels/level-03-04/) |
| 4 → 5 | File types and wildcards | [View writeup](./levels/level-04-05/) |
| 5 → 6 | Finding files by properties | [View writeup](./levels/level-05-06/) |
| 6 → 7 | Finding files by owner/group | [View writeup](./levels/level-06-07/) |
| 7 → 8 | Searching text with `grep` | [View writeup](./levels/level-07-08/) |
| 8 → 9 | Sorting and unique lines | [View writeup](./levels/level-08-09/) |
| 9 → 10 | Extracting strings from binary data | [View writeup](./levels/level-09-10/) |
| 10 → 11 | Base64 decoding | [View writeup](./levels/level-10-11/) |
| 11 → 12 | ROT13 with `tr` | [View writeup](./levels/level-11-12/) |
| 12 → 13 | Hexdump and repeated decompression | [View writeup](./levels/level-12-13/) |
| 13 → 14 | SSH private keys | [View writeup](./levels/level-13-14/) |
| 14 → 15 | Sending data with `nc` | [View writeup](./levels/level-14-15/) |
| 15 → 16 | SSL/TLS with `ncat` | [View writeup](./levels/level-15-16/) |
| 16 → 17 | Port scanning and SSH key credentials | [View writeup](./levels/level-16-17/) |
| 17 → 18 | Comparing files with `diff` | [View writeup](./levels/level-17-18/) |
| 18 → 19 | SSH remote commands | [View writeup](./levels/level-18-19/) |
| 19 → 20 | Setuid helper binary | [View writeup](./levels/level-19-20/) |
| 20 → 21 | Netcat listener | [View writeup](./levels/level-20-21/) |
| 21 → 22 | Cron jobs | [View writeup](./levels/level-21-22/) |
| 22 → 23 | Cron-generated file paths | [View writeup](./levels/level-22-23/) |
| 23 → 24 | Cron writable spool execution | [View writeup](./levels/level-23-24/) |
| 24 → 25 | Brute-forcing a PIN | [View writeup](./levels/level-24-25/) |
| 25 → 26 | Escaping `more` through Vim | [View writeup](./levels/level-25-26/) |
| 26 → 27 | Setuid command execution | [View writeup](./levels/level-26-27/) |
| 27 → 28 | Git clone basics | [View writeup](./levels/level-27-28/) |
| 28 → 29 | Git commit history | [View writeup](./levels/level-28-29/) |
| 29 → 30 | Git branches | [View writeup](./levels/level-29-30/) |
| 30 → 31 | Git tags | [View writeup](./levels/level-30-31/) |
| 31 → 32 | Git ignore and push validation | [View writeup](./levels/level-31-32/) |
| 32 → 33 | Uppercase shell escape | [View writeup](./levels/level-32-33/) |

## Repository Structure

```text
Bandit/
├── README.md
├── TEMPLATE.md
├── setup.sh
└── levels/
    └── level-XX-YY/
        ├── README.md
        ├── password.txt
        └── assets/
```

Each level has its own `README.md`. Screenshots and other supporting files are stored in its `assets` directory. Local `password.txt` files and private key files are ignored by Git. Use [TEMPLATE.md](./TEMPLATE.md) or `setup.sh` when adding a new writeup.
