![logo](https://storage.esec.sk/saved_data/282922.png)

[![Build Status](https://travis-ci.com/esec-exploits/bruteproxy.py.svg?branch=main)](https://travis-ci.com/esec-exploits/bruteproxy.py) ![status](https://img.shields.io/badge/status-beta-blue) ![Issues](https://img.shields.io/github/issues/esec-exploits/bruteproxy.py) ![commits](https://img.shields.io/github/commits-since/esec-exploits/bruteproxy.py/b1.1.0)

## What's this about?
Have you ever been brute-forcing and got IP-banned because the website has a limited amount of tries? Well, in most cases, this blocking system identifies you based on your IPv4 address. BruteProxy is (for now) **single-thread brute-forcing script with looping proxies**, that are taken from the provided proxylist. BruteProxy.py has a built-in console and Metasploit-like commands (set, run, etc.) to easily access all its features.

## IMPORTANT
Currently, since BruteProxy is still in development, looping proxies are not included in the release. However, the working prototype is already born and after negotiations with the proxies sponsor, we will be able to release the *b1.2.0* version, which will contain the proxy looping.

## Getting started, usage and wiki
Getting started tutorial: [Getting started with BruteProxy](https://github.com/esec-exploits/bruteproxy.py/wiki/Getting-started)

Everything can be found on GitHub wiki [here](https://github.com/esec-exploits/bruteproxy.py/wiki).

## Contact, Discord & support
Feel free to contact me at Discord server (esecwtf#1901) or at `exploits@esec.sk`. If you have found a bug or have some kind of issue, just create a new issue here on GitHub and I'll review it :)
Contributors are welcome, just submit a pull request and I'll take a look.

**Discord server:** [here](https://discord.gg/ktRUMu2yyF)

## Legal notice
Keep in mind that this tool was made and is maintained for legal activities and only can be used on victims that **agreed and are acknowledged** about this type of attack. BruteProxy developers, contributors, and associated teams, companies, and services are *not* responsible for any damage or legal responsibilities caused by using this tool. BruteProxy is a tool made for white-hat pentesters.

## Current dev-team and license
On **BruteProxy.py** project is curretly working **one** developer(s):
- Anton Pernisch *(100%)*

BruteProxy.py framework is distributed and protected under MIT license.

Copyright 2020 Anton Pernisch

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
