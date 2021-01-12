#!/usr/bin/env python
import requests
from signal import signal, SIGINT
from sys import exit
import re
from Modules.Attacker import attacker
from Modules.Rotater import rotater
import sys, getopt
import random

try:
    import readline
except:
    pass

# init completer
class completer_class(object):

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None

# text to complete
completer = completer_class(["set ", "help", "values", "help", "exit", "run", "threads ", "target ", "wordlist ", "proxylist ", "username ", "error_identifier ", "method ", "username_parameter ", "password_parameter ", "custom_request ", "cookies ", "options", "True", "False", "proxylooping ", "proxychange "])
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

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

# build info
build_version = "b1.3.0"

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
        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "BruteProxy.py is not starting to be safe. Please remove all unnecessary arguments.")
        exit(0)

print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Starting BruteProxy..." + colors.ENDC)

# load current latest version from our CDN (preparation for updater module)
try:
    latest_version = requests.get("https://esec.sk/cdn/bruteproxy/latest_version.txt").text
except:
    print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.WARNING + "Couldn't get latest version from esec.sk CDN" + colors.ENDC)

# decide on version type (outdated, latest, dev)
try:
    if build_version.endswith("dev"):
        # using dev version
        version_type = "dev"
    elif build_version == latest_version:
        # using latest version
        version_type = "latest"
    else:
        # outdated version
        version_type = "outdated"
except:
    version_type = "unknown"
    print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.WARNING + "Couldn't determine version type" + colors.ENDC)

# exit handler
def handler(signal_received, frame):
    try:
        attacker.spinner__done = True
        print("\r", end = "")
    except:
        print("", end = "")

    print(colors.OKCYAN + "\n\n[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Terminating all threads and doing cleanup, please wait..." + colors.ENDC)
    try:
        rotater.run = False
        attacker.threads__run = False
        for threadNumToKill in range(0, attacker.threadsCount):
            attacker.attack_threads[threadNumToKill].join()
    except:
        print("", end = "")
    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Exitting..." + colors.ENDC)
    sys.exit(0)

# exit handler init
signal(SIGINT, handler)

# set some default values
attack__target = "(unset)"
attack__wordlist = "(unset)"
attack__username = "(unset)"
attack__proxylist = "(unset)"
attack__errIdentifier = "(unset)"
attack__method = "post"
attack__usernameParameterName = "username"
attack__passwordParameterName = "password"
attack__custom_request = "False"
attack__cookies = "False"
attack__mt_threads = 4
attack__proxylooping = "False"
attack__proxychange = 10

# DANGEROUS, EDIT ONLY FOR OVERCLOCKING
threads_maximum = 100

errIdentifier_argList = []

# some regxes (it was pain, ngl)
run__target_pattern_ip = re.compile(r"^^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(:([0-9])([0-9])?([0-9])?([0-9])?([0-9])?)?(\/.*)?$")
run__target_pattern_domain = re.compile(r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
run__proxylist_pattern = re.compile(r"(.*).\.txt$")
run__wordlist_pattern = re.compile(r"(.*).\.txt$")

# --- ~~~ ---
# | HELPERS SECTION |
# --- ~~~ ---

# run command: checking some entered values
def cmd__run_check(attack__target, attack__wordlist, attack__proxylist):
    if attack__target != "(unset)" and (run__target_pattern_ip.match(attack__target) or run__target_pattern_domain.match(attack__target)):
        # target matched, proceed
        if attack__wordlist != "(unset)" and run__wordlist_pattern.match(attack__wordlist):
            # wordlist matched, proceed to last
            if attack__mt_threads <= threads_maximum and attack__mt_threads > 0:
                # this check is done only if user enabled proxy looping feature
                if attack__proxylooping == "True":
                    if attack__proxylist != "(unset)" and run__proxylist_pattern.match(attack__proxylist):
                        # proxylist matched, proceed to check number
                        if attack__proxychange >= 1:
                            # everything matched, return 400 as everything is OK
                            # ps. we do not need to check username, since it can be anything :)
                            return 400
                        else:
                            # proxychange value is smaller than 1, code 360
                            return 360
                    else:
                        # proxylist not set or regex not matched oof
                        return 200
                else:
                    # everything matched, return 400 as everything is OK
                    # ps. we do not need to check username, since it can be anything :)
                    return 400
            else:
                # too high or low threads count
                return 350
        else:
            # wordlist not set or regex not matched oof
            return 300
    else:
        # target not set or regex not matched oof
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
    print(colors.OKCYAN + "[] " + colors.ENDC + " ")
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "MULTI-THREADING:" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "threads: " + colors.ENDC + "Sets number of threads that BruteProxy will run on during attack. Max. is 100 threads.")

# exit
def cmd__exit():
    try:
        attacker.spinner__done = True
        print("\r", end = "")
    except:
        print("", end = "")

    print(colors.OKCYAN + "\n\n[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Terminating all threads and doing cleanup, please wait..." + colors.ENDC)
    try:
        attacker.threads__run = False
        rotater.run = False
        for threadNumToKill in range(0, attacker.threadsCount):
            attacker.attack_threads[threadNumToKill].join()
    except:
        print("", end = "")
    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Exitting..." + colors.ENDC)
    sys.exit(0)

# set
def cmd__set(param, value):
    if param == "options":
        # required options are username, password wordlist, proxylist, error_identifier and URL address
        print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + colors.UNDERLINE + "\"set\" command usage:" + colors.ENDC + " set [parameter to set] [value to be set up]")
        print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + colors.UNDERLINE + "Exmple:" + colors.ENDC + " set target http://my-vuln-site.com " + colors.BOLD + "or " + colors.ENDC + "set wordlist /home/wordlists/wl.txt")
        print(colors.OKCYAN + "[] " + colors.ENDC + " ")
        print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "REQUIRED PARAMETERS BEFORE RUNNING ATTACK:" + colors.ENDC)
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "target: " + colors.ENDC + "Sets the target URL od IPv4 address, ie. http://vuln-site.com or http://183.192.21.22/login")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "wordlist: " + colors.ENDC + "Sets the wordlist to use for bruteforce, ie. /home/wordlists/wl.txt")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "username: " + colors.ENDC + "Sets the username that will be bruteforced, ie. admin")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "error_identifier: " + colors.ENDC + "Identifies error message (unsuccessful login try)")
        print(colors.OKCYAN + "[]" + colors.ENDC)
        print(colors.OKCYAN + "[]" + colors.ENDC)
        print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "ADDITIONAL PARAMETERS:" + colors.ENDC)
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "method: " + colors.ENDC + "Sets the method to use while brute-forcing. Supported are get or post.")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "username_parameter: " + colors.ENDC + "Sets the request parameter name for username input")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "password_parameter: " + colors.ENDC + "Sets the request parameter name for password input")
        print(colors.OKCYAN + "[]" + colors.ENDC)
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "custom_request: " + colors.ENDC + "If you want to use a custom request, set this to \"True\" and MAKE SURE you've read wiki.")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "cookies: " + colors.ENDC + "If you want to use some cookies, set this to \"True\" and MAKE SURE you've read wiki.")
        print(colors.OKCYAN + "[]" + colors.ENDC)
        print(colors.OKCYAN + "[]" + colors.ENDC)
        print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "PROXY LOOPING FEATURE:" + colors.ENDC)
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "proxylooping: " + colors.ENDC + "This must be set to \"True\" if you want to use this feature. Default is \"False\"")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "proxylist: " + colors.ENDC + "Sets the proxylist that will be used while bruteforcing, ie. /proxies/proxylist.txt")
        print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "proxychange: " + colors.ENDC + "This number determines after how many attempts will be proxy changed")
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
    elif param == "method":
        if value == "get" or value == "post":
            global attack__method
            attack__method = value
            print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"method\" was set to " + colors.OKCYAN + value + colors.ENDC)
        else:
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unknown value for attack method, supported methods are \"get\" and \"post\"" + colors.ENDC)
    elif param == "custom_request":
        if value == "True" or value == "False":
            global attack__custom_request
            attack__custom_request = value
            print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"custom_request\" was set to " + colors.OKCYAN + value + colors.ENDC)
        else:
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unknown value for custom request, supported values are \"True\" and \"False\"" + colors.ENDC)
    elif param == "cookies":
        if value == "True" or value == "False":
            global attack__cookies
            attack__cookies = value
            print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"cookies\" was set to " + colors.OKCYAN + value + colors.ENDC)
        else:
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unknown value for cookies, supported values are \"True\" and \"False\"" + colors.ENDC)
    elif param == "proxychange":
        try:
            global attack__proxychange
            attack__proxychange = int(value)
            print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"proxychange\" was set to " + colors.OKCYAN + value + colors.ENDC)
        except:
            # convertion was unsuccessful
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Enter only number" + colors.ENDC)
    elif param == "proxylooping":
        if value == "True" or value == "False":
            global attack__proxylooping
            attack__proxylooping = value
            print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Parameter \"proxylooping\" was set to " + colors.OKCYAN + value + colors.ENDC)
        else:
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unknown value for proxylooping, supported values are \"True\" and \"False\"" + colors.ENDC)
    else:
        print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unknown parameter, you can display all parameters by \"set options\"" + colors.ENDC)

# values
def cmd__values():
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + colors.UNDERLINE + "Currently set up values:" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + " ")
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "REQUIRED PARAMETERS BEFORE RUNNING ATTACK:" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "target: " + colors.ENDC + attack__target)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "wordlist: " + colors.ENDC + attack__wordlist)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "username: " + colors.ENDC + attack__username)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "error_identifier: " + colors.ENDC + attack__errIdentifier)
    print(colors.OKCYAN + "[]" + colors.ENDC)
    print(colors.OKCYAN + "[]" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "ADDITIONAL PARAMETERS:" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "method: " + colors.ENDC + attack__method)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "username_parameter: " + colors.ENDC + attack__usernameParameterName)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "password_parameter: " + colors.ENDC + attack__passwordParameterName)
    print(colors.OKCYAN + "[]" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "custom_request: " + colors.ENDC + attack__custom_request)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "cookies: " + colors.ENDC + attack__cookies)
    print(colors.OKCYAN + "[]" + colors.ENDC)
    print(colors.OKCYAN + "[]" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "MULTI-THREADING:" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "threads: " + colors.ENDC + str(attack__mt_threads))
    print(colors.OKCYAN + "[]" + colors.ENDC)
    print(colors.OKCYAN + "[]" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + colors.BOLD + "PROXY LOOPING:" + colors.ENDC)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "proxylooping: " + colors.ENDC + attack__proxylooping)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "proxylist: " + colors.ENDC + attack__proxylist)
    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "proxychange: " + colors.ENDC + str(attack__proxychange))

# run
def cmd__run():
    # this will be messy, so prepare
    # firstly, let's check if all paramtere are fulfilled and compare them with regex (pain in the ass) if everything's alright

    # run the check
    cmd__run_check_result = cmd__run_check(attack__target, attack__wordlist, attack__proxylist)
    if cmd__run_check_result == 400 and attack__username != "(unset)":
        # everything's fine, proceed to actual bruteforce class
        attacker.setup(0, attack__method, attack__custom_request, attack__cookies, attack__mt_threads, attack__proxylooping, attack__proxylist, attack__proxychange)
        attacker.attack(0, attack__target, attack__username, attack__wordlist, attack__errIdentifier, attack__usernameParameterName, attack__passwordParameterName)
    else:
        # we've got something wrong, let's tell it to the user
        if cmd__run_check_result == 100:
            # 100 means problem with target
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Not set or wrong target format, ensure that it is starting with http:// or https:// and it's valid URL/IPv4" + colors.ENDC)
        elif cmd__run_check_result == 200:
            # 200 means problem with proxylist
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Not set or wrong proxylist format, ensure that it is ending with .txt and it's full path" + colors.ENDC)
        elif cmd__run_check_result == 300:
            # 300 means problem with wordlist
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Not set or wrong wordlist format, ensure that it is ending with .txt and it's full path" + colors.ENDC)
        elif cmd__run_check_result == 350:
            # 350 means problem with threads count
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Too low or too high threads count. Mimimum is 1 one maximum is 100" + colors.ENDC)    
        elif attack__username == "(unset)":
            # username is empty, fix that please
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Username not set" + colors.ENDC)
        elif cmd__run_check_result == 360:
            # 360 means problem with proxychange number
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "proxychange value is too low (under 1)" + colors.ENDC)
        else:
            # oops, this is bad
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unexpected error, ensure that everything is set up correctly by typing \"values\"" + colors.ENDC)

# threads
def cmd__threads(count):
    # we are converting string to int, error handle that in case of wrong string input
    try:
        global attack__mt_threads
        attack__mt_threads = int(count)
        print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Threads count changed to " + colors.OKCYAN + count + colors.ENDC)
    except:
        # convertion was unsuccessful
        print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Enter only number, from 1 to 100" + colors.ENDC)


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
        if i[0] == "set" and len(i) > 3:
            if i[1] == "error_identifier":
                # special case in error_identifier, must join whole value in one string
                for item in range(2, len(i)):
                    # if it is last, dont put space at the end
                    if item == len(i):
                        errIdentifier_argList.append(i[item])
                    else:
                        errIdentifier_argList.append(i[item] + " ")

                i[2] = "".join(errIdentifier_argList)
            else:
                print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Missing or too many arguments, try \"help\" or \"set options\"" + colors.ENDC)
        else:
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

        if i[0] == "threads" and len(i) != 2:
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Missing or too many arguments, try \"help\"" + colors.ENDC)
            cmdListener__base()

        switcher = {"help": lambda: cmd__help(), "exit": lambda: cmd__exit(), "set": lambda: cmd__set(i[1],i[2]), "values": lambda: cmd__values(), "run": lambda: cmd__run(), "threads": lambda: cmd__threads(i[1])}
        func = switcher.get(i[0],lambda: unknown_command())
        func()
        cmdListener__base()

    rawCmd = input(colors.BOLD + "BP.py>  " + colors.ENDC)
    pharsedCmd = rawCmd.split()
    if rawCmd != "":
        executor__base(pharsedCmd)
    else:
        cmdListener__base()

# random motd, just for fun
motd_num = random.randint(1, 100)

print(" ")

# pick some motd
if motd_num <= 50:
    print(colors.BOLD + colors.FAIL + "    ____             __   " + colors.OKGREEN + "    ____                                     ")
    print(colors.BOLD + colors.FAIL + "   / __ )_______  __/ /____" + colors.OKGREEN + "  / __ \_________  _  ____  __ " + colors.WHITE + colors.BOLD + " ____  __  __")
    print(colors.BOLD + colors.FAIL + "  / __  / ___/ / / / __/ _ " + "\\" + colors.OKGREEN + "/ /_/ / ___/ __ \| |/_/ / / / " + colors.WHITE + colors.BOLD + "/ __ \/ / / /")
    print(colors.BOLD + colors.FAIL + " / /_/ / /  / /_/ / /_/  __" + colors.OKGREEN + "/ ____/ /  / /_/ />  </ /_/ / " + colors.WHITE + colors.BOLD + "/ /_/ / /_/ / ")
    print(colors.BOLD + colors.FAIL + "/_____/_/   \__,_/\__/\___" + colors.OKGREEN + "/_/   /_/   \____/_/|_|\__, " + colors.WHITE + colors.BOLD + "(_) .___/\__, /  ")
    print(colors.OKGREEN + "                                                /____/ " + colors.WHITE + colors.BOLD + "/_/    /____/   " + colors.ENDC)
elif motd_num > 50:
    print(colors.BOLD + colors.FAIL + " ____                .          " + colors.OKGREEN + " .___                                             " + colors.ENDC)
    print(colors.BOLD + colors.FAIL + " /   \  .___  ,   . _/_     ___ " + colors.OKGREEN + " /   \ .___    __.  _  .- ,    . " + colors.WHITE + colors.BOLD + "   \,___, ,    . " + colors.ENDC)
    print(colors.BOLD + colors.FAIL + " |,_-<  /   \ |   |  |    .'   `" + colors.OKGREEN + " |,_-' /   \ .'   \  \,'  |    ` " + colors.WHITE + colors.BOLD + "   |    \ |    ` " + colors.ENDC)
    print(colors.BOLD + colors.FAIL + " |    ` |   ' |   |  |    |----'" + colors.OKGREEN + " |     |   ' |    |  /\   |    | " + colors.WHITE + colors.BOLD + "   |    | |    | " + colors.ENDC)
    print(colors.BOLD + colors.FAIL + " `----' /     `._/|  \__/ `.___," + colors.OKGREEN + " /     /      `._.' /  \   `---|." + colors.WHITE + colors.BOLD + " / |`---'  `---|." + colors.ENDC)
    print(colors.BOLD + colors.OKGREEN + "                                                           \___/  " + colors.WHITE + colors.BOLD + "  \       \___/" + colors.ENDC)
print(" ")
print(colors.DARK_CYAN + "BruteProxy.py framework for bruteforcing\nvia HTTP(S) requests with looping proxies.")
print(colors.DARK_CYAN + "Exit by typing \"exit\" command or by pressing Ctrl+C")
print(colors.DARK_CYAN + "Illegal usage is strongly restricted.")
print(colors.DARK_CYAN + "(c) Anton Pernisch 2021" + colors.ENDC)
print(" ")
if version_type == "latest":
    print(colors.DARK_CYAN + "Using version: " + colors.BOLD + build_version + " (latest)" + colors.ENDC)
elif version_type == "outdated":
    print(colors.DARK_CYAN + "Using version: " + colors.BOLD + build_version + " (outdated, latest version is " + latest_version + ")" + colors.ENDC)
    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Note that you are using outdated version, you're missing bugfixes and new features." + colors.ENDC)
elif version_type == "dev":
    print(colors.DARK_CYAN + "Using version: " + colors.BOLD + build_version + " (pre-release)" + colors.ENDC)
    print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.WARNING + "Please note that you are using pre-release that is still in development." + colors.ENDC)
else:
    print(colors.DARK_CYAN + "Using version: " + colors.BOLD + build_version + colors.ENDC)
print(" ")
print(" ")
print(" ")
cmdListener__base()
