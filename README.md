# BruteProxy.py framework

## What's this about?
Have you ever been brute-forcing and got IP-banned because the website has a limited amount of try? Well, in most cases, this blocking system identifies you based on your IPv4 address. BruteProxy is (for now) **single-thread brote-forcing script with looping proxies**, that are taken from provided proxylist. BruteProxy.py has built-in console and Metasploit-like commands (set, run, etc.) to easily access all it's features.
	
## Installation
Before you start the actual installation, make sure you have installed:
	- Python3
	- requests library for Python
If you don't know what you have installed or not, take a quick peek at the next few lines. If you do, proceed to BruteProxy.py installation from GitHub.

### Python3 installation
**To check if Python3 is installed:**
1. Open terminal on your Linux machine
2. Type:
```sh
$ python3 --version
```
3. If you will get 
```sh
Python 3.x.x
```
as response, Python3 **is** installed. However, if not and you'll get error message that command is unknown, just type:
```sh
$ sudo apt install python3.8
```
and you should be fine. If not, please do a small research on how to install Python3, focus of this README is not an installation of Python3.

### requests installation
1. First things first, make sure you've got a pip command installed. To do so, just type this in CLI:
```sh
$ sudo apt install python3-pip
```
and then
```sh
$ sudo apt-get update
```
2. After installing pip, just execute in CLI:
```sh
$ sudo python3 -m pip install requests
```
3. You are now set up!

### BruteProxy.py installation from GitHub
1. Make sure that you have installed everything mentioned above.
2. Go to your terminal and navigate to directory where BruteProxy.py will be installed (*Note that `git clone` will make it's own directory where it'll put files from GitHub, so keep that in mind*)
3. Once you're in right directory, type:
```sh
$ sudo git clone https://github.com/esec-exploits/bruteproxy.py.git
```
4. When the installation will complete, you've successfully installed BruteProxy.py framework! To continue and learn how to use it, procees to Getting started.

## Getting started
Once you have completed installation from GitHub using `git clone` command, you will notice new folder in your location, name of that folder should be `bruteproxy.py` (don't be confused that name ends with *.py* as if it's Python file, it's folder). Now go ahead and navigate to that folder by executing
```sh
$ cd bruteproxy.py
```
Now to start BruteProxy.py console, type
```sh
$ sudo python3 BruteProxy.py
```

And just like so, you've started BruteProxy.py! Take a look at Basic usage to see how to use it.

## Basic usage
After we have stared BruteProxy.py framework, something like this should come up:

![motd_screenshot](https://i.imgur.com/B4DAl60.png)

Now, typing
```sh
BP.py> help
```
will show every command you can use inside BruteProxy.py console. You can exit the console by pressing Ctrl+C or by typing
```sh
BP.py> exit
```

**Let's take a quick peek on how to set up arguments and start an attack:**
1. Firstly, before you execute attack, you must make sure that all required values are set up correctly. To show what values are currently assigned, execute `values` command, just like so:
```sh
BP.py> values
```
you will get something like this:

![values_screenshot](https://i.imgur.com/ZMY9CZV.png)

We can see that right now (after just starting the framework), all values are unset. Let's fix that using `set` command. Syntax of this command is `set <parameter to set> <value to be set up>`. You can display all availabe parameters by executing `set options`. However, here, we'll show how to set up required parameters, that are essetial before running the attack.

### target
**Usage:**
```sh
BP.py> set target <URL/IPv4 address>
```
target is address of the script that we are attacking. Right now, only possible method is attacking a POST HTTP or HTTPS script, that is working with two POST arguments: `username` as username and `password` as password, however this will change soon and customization will be possible. Note that value here can be URL with domain name or IPv4 address, but both of them **must** start with `http://` or `https://`, otherwise it will give you an error.
Also, make sure that the address of **the script** is there, not the address of the actaul login form. You can get this address by analyzing the login process by tools like Burpsuite etc., you know what I'm talking about...

### wordlist
**Usage:**
```sh
BP.py> set wordlist <path-to-wordlist>
```
wordlist parameter holds the local path to wordlist that will be used in attack. Wordlist **must** be in `.txt` format and every password must be on new line, pretty much a standart wordlist format.

### proxylist
**Usage:**
```sh
BP.py> set proxylist <path-to-proxylist>
```
proxylist parameter holds the local path to proxylist that will be used in attack. Proxylist is what makes this brute-force unique, on each line of `.txt` document, it contains an address of the proxy in this format: `ipv4:port` (for example `101.221.19.2:80`). This proxies will be looped while brute-forcing and will change the machines IPv4 address on webserver each specified time, so the max try limitation on login form will be bypassed. **THIS FEATURE IS IN PRE-DEV DEVELOPMENT, CURRETLY UNRELEASED**

### username
**Usage:**
```sh
BP.py> set username <username>
```
username will be used as username while brute-forcing and trying diffrent passwords from wordlist. Right now, the username stays the same during the whole brute-force process and this will not change very soon.

### error_identifier
**Usage:**
```sh
BP.py> set error_identifier <text>
```
error_identifier will be used when BruteProxy.py will be comparing the response from the server. It is necessary, because the BruteProxy.py can with this identify that tried password was incorrect and can move to next one. Basically, this is some keyword, that will be shown on page if the wrong credetials were written. For example if the wrong password message shown on the attacked page looks like this: `Oops! Password is incorrect! Try again...`, the error_identifier will be `incorrect`.

### Running attack
After we have set up all 5 required parameters (we can make sure and review the parameters by typing `values` command in BruteProxy.py console), let's run the attack by typing:
```sh
BP.py> run
```
Then, we just have to wait. Keep on mind that right now, BruteProxy.py is only sigle-thread brute-forcer, so it can take a while... We are working on adding multi-thread workflow.

## Contact & support
Feel free to contact me on `exploits@esec.sk`. If you have found a bug or have ome kind of issue, just create a new issue here on GitHub and I'll review it :)
Contributors are welcome, just submit a pull request and I'll take a look.

## Current dev-team and license
On **BruteProxy.py** project is curretly working **one** developer: Anton Pernisch *(100%)*

BruteProxy.py framework is distributed and protected under [Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/) license.

![license](https://chooser-beta.creativecommons.org/img/nc.8c3b7ea6.svg)![license](https://chooser-beta.creativecommons.org/img/by.f6aa22c4.svg)![license](https://chooser-beta.creativecommons.org/img/nc.8c3b7ea6.svg)![license](https://chooser-beta.creativecommons.org/img/nd.64831b7b.svg)
