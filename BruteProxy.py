#!/usr/bin/env python
import requests
from signal import signal, SIGINT
from sys import exit
import re
from Modules.Attacker import attacker
import sys, getopt

# build info
build_version = "b1.0.0"

# define colors
# colors in ansi color coding
class colors:
    HEADER = '\033[95m'
    WHITE = '\033[0m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARK_CYAN = '\033[90m'

# version checker handler
if len(sys.argv) > 1:
    # we've got some arguments in terminal, check for version or v argument
    if sys.argv[1] == "-v" or sys.argv[1] == "-version":
        # user requested version, print that and do not start the framework
        print(" ")
        print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "BruteProxy.py framework installed and running on version " + colors.OKCYAN + build_version + colors.ENDC)
        exit(0)
    else:
        print(" ")
        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "You can only use -v or -version parameter, others are not supported")
        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "BruteProxy.py not starting, to be safe. Please remove all unnecessary arguments.")
        exit(0)

# exit handler
def handler(signal_received, frame):
    print("\n")
    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Exitting BruteProxy.py framework...")
    exit(0)

# exit handler init
signal(SIGINT, handler)

# set some default values
attack__target = "(unset)"
attack__wordlist = "(unset)"
attack__username = "(unset)"
attack__proxylist = "(unset)"
attack__errIdentifier = "(unset)"
attack__usernameParameterName = "username"
attack__passwordParameterName = "password"

# some regxes (it was pain, ngl)
run__target_pattern = re.compile("^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
run__proxylist_pattern = re.compile("(.*).\.txt$")
run__wordlist_pattern = re.compile("(.*).\.txt$")

# --- ~~~ ---
# | HELPERS SECTION |
# --- ~~~ ---

# run command: checking some entered values
def cmd__run_check():
    if attack__target != "(unset)" and run__target_pattern.match(attack__target):
        # target matched, proceed
        if attack__proxylist != "(unset)" and run__proxylist_pattern.match(attack__proxylist):
            # proxylist matched, proceed to last, wordlist
            if attack__wordlist != "(unset)" and run__wordlist_pattern.match(attack__wordlist):
                # everything matched, return 400 as everything is OK
                # ps. we do not need to check username, since it can be anything :)
                return 400
            else:
                # wordlist not set or redex not matched oof
                return 300
        else:
            # proxylist not set or redex not matched oof
            return 200
    else:
        # target not set or redex not matched oof
        return 100

# --- ~~~ ---
# | END OF HELPERS SECTION |
# --- ~~~ ---

# --- ~~~ ---
# | COMMANDS SECTION |
# --- ~~~ ---

# help
def cmd__help():
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "Command usage: " + colors.ENDC + "<command> [command's argument] [value]")
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "Exmple: " + colors.ENDC + "set target http://my-vuln-site.com " + colors.BOLD + "or " + colors.ENDC + "run")
    print(colors.OKCYAN + "[] " + colors.ENDC + " ")
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "BASIC COMMANDS:" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "help: " + colors.ENDC + "Displays this help dialog")
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "exit: " + colors.ENDC + "Exits BruteProxy.py framework. Ctrl+C can also be used")
    print(colors.OKCYAN + "[] " + colors.ENDC + " ")
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "EXPLOIT COMMANDS:" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "set: " + colors.ENDC + "Sets chosen parameter to entered value, ie. " + colors.BOLD + "set target http://my-vuln-site.com" + colors.ENDC + "\n" + colors.OKCYAN + "[]" + colors.ENDC + "           (all parameters can be shown by executing \"set options\")")
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "run: " + colors.ENDC + "Executes attack")
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "values: " + colors.ENDC + "Displays all currently set up values")

# exit
def cmd__exit():
    print("")
    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Exitting BruteProxy.py framework...")
    exit(0)

# set
def cmd__set(param, value):
    if param == "options":
        # required options are username, password wordlist, proxylist, error_identifier and URL address
        print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "\"set\" command usage: " + colors.ENDC + "set [parameter to set] [value to be set up]")
        print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "Exmple: " + colors.ENDC + "set target http://my-vuln-site.com " + colors.BOLD + "or " + colors.ENDC + "set wordlist /home/wordlists/wl.txt")
        print(colors.OKCYAN + "[] " + colors.ENDC + " ")
        print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "REQUIRED PARAMETERS BEFORE RUNNING ATTACK:" + colors.ENDC)
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "target: " + colors.ENDC + "Sets the target URL od IPv4 address, ie. http://vuln-site.com or http://183.192.21.22/login")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "wordlist: " + colors.ENDC + "Sets the wordlist to use for bruteforce, ie. /home/wordlists/wl.txt")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "proxylist: " + colors.ENDC + "Sets the proxylist that will be used while bruteforcing, ie. /proxies/proxylist.txt")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "username: " + colors.ENDC + "Sets the username that will be bruteforced, ie. admin")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "error_identifier: " + colors.ENDC + "Identifies error message (unsuccessful login try)")
        print(colors.OKCYAN + "[]" + colors.ENDC)
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "username_parameter: " + colors.ENDC + "Sets the POST parameter name for username input")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "password_parameter: " + colors.ENDC + "Sets the POST parameter name for password input")
    elif param == "target":
        global attack__target
        attack__target = value
        print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"target\" was set to " + colors.OKCYAN + value + colors.ENDC)
    elif param == "wordlist":
        global attack__wordlist
        attack__wordlist = value
        print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"wordlist\" was set to " + colors.OKCYAN + value + colors.ENDC)
    elif param == "proxylist":
        global attack__proxylist
        attack__proxylist = value
        print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"proxylist\" was set to " + colors.OKCYAN + value + colors.ENDC)
    elif param == "username":
        global attack__username
        attack__username = value
        print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"username\" was set to " + colors.OKCYAN + value + colors.ENDC)
    elif param == "error_identifier":
        global attack__errIdentifier
        attack__errIdentifier = value
        print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"error_identifier\" was set to " + colors.OKCYAN + value + colors.ENDC)
    elif param == "username_parameter":
        global attack__usernameParameterName
        attack__usernameParameterName = value
        print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"username_parameter\" was set to " + colors.OKCYAN + value + colors.ENDC)
    elif param == "password_parameter":
        global attack__passwordParameterName
        attack__passwordParameterName = value
        print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"password_parameter\" was set to " + colors.OKCYAN + value + colors.ENDC)
    else:
        print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unknown parameter, you can display all parameters by \"set options\"" + colors.ENDC)

# values
def cmd__values():
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "Currently set up values (all of these must be set before running attack):" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "target: " + colors.ENDC + attack__target)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "wordlist: " + colors.ENDC + attack__wordlist)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "proxylist: " + colors.ENDC + attack__proxylist)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "username: " + colors.ENDC + attack__username)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "error_identifier: " + colors.ENDC + attack__errIdentifier)
    print(colors.OKCYAN + "[]" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "username_parameter: " + colors.ENDC + attack__usernameParameterName)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "password_parameter: " + colors.ENDC + attack__passwordParameterName)

# run
def cmd__run():
    # this will be messy, so prepare
    # firstly, let's check if all paramtere are fulfilled and compare them with regex (pain in the ass) if everything's alright

    # run the check
    cmd__run_check_result = cmd__run_check()

    if(cmd__run_check_result == 400 and attack__username != "(unset)"):
        # everything's fine, proceed to actual bruteforce class
        attacker.attack(0, attack__target, attack__username, attack__wordlist, attack__proxylist, attack__errIdentifier, attack__usernameParameterName, attack__passwordParameterName)
    else:
        # we've got something wrong, let's tell it to the user
        if cmd__run_check_result == 100:
            # 100 means problem with target
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Not set or wrong target format, ensure that it is starting with http:// and it's valid URL/IPv4" + colors.ENDC)
        elif cmd__run_check_result == 200:
            # 200 means problem with proxylist
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Not set or wrong proxylist format, ensure that it is ending with .txt and it's full path" + colors.ENDC)
        elif cmd__run_check_result == 300:
            # 300 means problem with wordlist
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Not set or wrong wordlist format, ensure that it is ending with .txt and it's full path" + colors.ENDC)
        elif attack__username == "(unset)":
            # username is empty, fix that please
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Username not set" + colors.ENDC)
        else:
            # oops, this is bad
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unexpected error, ensure that everything is set up correctly by typing \"values\"" + colors.ENDC)

# --- ~~~ ---
# | END OF COMMANDS SECTION |
# --- ~~~ ---

# unknown command
def unknown_command():
    print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unknown command, try \"help\"" + colors.ENDC)
    cmdListener__base()

# listen for command and pharse it
def cmdListener__base():
    # check for command and execute it
    def executor__base(i):
        if i[0] == "set" and len(i) != 3:
            if len(i) != 2:
                print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Missing or too many arguments, try \"help\" or \"set options\"" + colors.ENDC)
                cmdListener__base()
            elif i[1] != "options":
                print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Missing or too many arguments, try \"help\" or \"set options\"" + colors.ENDC)
                cmdListener__base()
            else:
                # argument IS options, just set the 2 value in list to something, so we don't get an error later on
                i.append("null")

        switcher = {"help": lambda: cmd__help(), "exit": lambda: cmd__exit(), "set": lambda: cmd__set(i[1],i[2]), "values": lambda: cmd__values(), "run": lambda: cmd__run()}
        func = switcher.get(i[0],lambda: unknown_command())
        func()
        cmdListener__base()

    print(colors.BOLD + "BP.py>  " + colors.ENDC, end="")
    rawCmd = input()
    pharsedCmd = rawCmd.split()
    if rawCmd != "":
        executor__base(pharsedCmd)
    else:
        cmdListener__base()

# motd
print(colors.BOLD + colors.FAIL + "    ____             __   " + colors.OKGREEN + "    ____                                     ")
print(colors.BOLD + colors.FAIL + "   / __ )_______  __/ /____" + colors.OKGREEN + "  / __ \_________  _  ____  __ " + colors.WHITE + colors.BOLD + " ____  __  __")
print(colors.BOLD + colors.FAIL + "  / __  / ___/ / / / __/ _ " + "\\" + colors.OKGREEN + "/ /_/ / ___/ __ \| |/_/ / / / " + colors.WHITE + colors.BOLD + "/ __ \/ / / /")
print(colors.BOLD + colors.FAIL + " / /_/ / /  / /_/ / /_/  __" + colors.OKGREEN + "/ ____/ /  / /_/ />  </ /_/ / " + colors.WHITE + colors.BOLD + "/ /_/ / /_/ / ")
print(colors.BOLD + colors.FAIL + "/_____/_/   \__,_/\__/\___" + colors.OKGREEN + "/_/   /_/   \____/_/|_|\__, " + colors.WHITE + colors.BOLD + "(_) .___/\__, /  ")
print(colors.OKGREEN + "                                                /____/ " + colors.WHITE + colors.BOLD + "/_/    /____/   " + colors.ENDC)
print(" ")
print(colors.DARK_CYAN + "BruteProxy.py framework for bruteforcing\nvia HTTP requests with looping proxies.")
print(colors.DARK_CYAN + "Exit by typing \"exit\" command or by pressing Ctrl+C")
print(colors.DARK_CYAN + "Illegal usage is strongly restricted.")
print(colors.DARK_CYAN + "(c) Anton Pernisch 2020" + colors.ENDC)
print(" ")
print(colors.DARK_CYAN + "Using version: " + colors.BOLD + build_version + colors.ENDC)
print(" ")
print(" ")
print(" ")
cmdListener__base()
