# Bandit Level 12 → 13 Writeup

## Goal

> The password for the next level is stored in the file `data.txt`, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under `/tmp` in which you can work. Use `mkdir` with a hard-to-guess directory name. Or better, use the command `mktemp -d`. Then copy the datafile using `cp`, and rename it using `mv` (read the manpages!).

## Solution

Because this level requires creating and renaming many files, I first created a temporary working directory and copied `data.txt` into it:

```bash
bandit12@bandit:~$ tmp_dir=$(mktemp -d)
bandit12@bandit:~$ cp data.txt "$tmp_dir/hex_file"
bandit12@bandit:~$ cd "$tmp_dir"
```

The original file is a hexdump, so I used `xxd -r` to reverse it and restore the binary data:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ xxd -r hex_file data_file
```

I initially tried to display `data_file` with `cat`, but the terminal only showed unreadable characters. This indicated that the result was still binary data. Instead of guessing its format, I used `file`:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ file data_file
data_file: gzip compressed data
```

Since the file was gzip-compressed, I renamed it with the `.gz` extension and decompressed it:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ mv data_file compressed.gz
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ gzip -d compressed.gz
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ file compressed
compressed: bzip2 compressed data
```

The next layer was compressed with bzip2:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ mv compressed compressed.bz2
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ bzip2 -d compressed.bz2
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ file compressed
compressed: gzip compressed data
```

After decompressing the next gzip layer, `file` reported a tar archive:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ mv compressed compressed.gz
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ gzip -d compressed.gz
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ file compressed
compressed: POSIX tar archive (GNU)
```

At first, I tried using bzip2 again because I saw `BZh` inside the output of `xxd`, but it did not work. The `file` result showed that the current layer was actually a tar archive, so I extracted it with `tar`:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ mv compressed compressed.tar
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ tar -xf compressed.tar
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ file data5.bin
data5.bin: POSIX tar archive (GNU)
```

The extracted file was another tar archive, so I extracted it again:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ mv data5.bin data5.tar
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ tar -xf data5.tar
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ file data6.bin
data6.bin: bzip2 compressed data
```

I decompressed the bzip2 layer and found one more tar archive:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ mv data6.bin data6.bz2
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ bzip2 -d data6.bz2
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ file data6
data6: POSIX tar archive (GNU)
```

After extracting that archive, the next file was gzip-compressed:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ mv data6 data6.tar
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ tar -xf data6.tar
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ file data8.bin
data8.bin: gzip compressed data
```

I decompressed the final gzip layer and displayed the resulting text file:

```bash
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ mv data8.bin data8.gz
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ gzip -d data8.gz
bandit12@bandit:/tmp/tmp.UUwYRNrfDk$ cat data8
The password is qQYQiHOBPR8zR61qxYqX45quvihF2uzk
```

## Password

```text
qQYQiHOBPR8zR61qxYqX45quvihF2uzk
```
