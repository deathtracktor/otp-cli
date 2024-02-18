A minimal time-based OTP CLI
============================

A CLI for generating time-based single-use passwords (aka OTP/TOTP).
**Download, build and use at your own risk.**

Installation
------------
```sh
$ git clone git@github.com:deathtracktor/otp-cli.git
$ cd otp-cli
$ python -m venv .venv
$ source .venv/bin/activate
# Windows: .venv\Scripts\activate
$ pip install -r requirements.txt
```

Running the CLI
---------------
```sh
$ python otp.py --help
```

You can also build a single-file executable bundle:
```sh
$ pyinstaller otp.py --onefile --name=otp
```
For Linux/MacOS, set the "executable" permission:
```sh
$ chmod ugo+rx dist/otp
```
Copy the resulting `otp` (or `otp.exe`) from `dist` to a directory listed
in your system `PATH`.
