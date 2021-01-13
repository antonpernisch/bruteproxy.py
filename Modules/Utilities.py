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

class utilities:
    def Question(self, text):
        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "?" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + text + " Answer with Y (means yes) or N (means no): " + colors.ENDC + "[Y/n]", end=" ")
        answer = input()
        if answer == "" or answer == "y" or answer == "yes" or answer == "Y":
            return True
        elif answer == "n" or answer == "no" or answer == "N":
            return False
        else:
            utilities.Question(0, text)

    # line counter
    def file_len(self, fname):
        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Decoding lists..." + colors.ENDC)
        try:
            # try with default, utf-8 encoding
            with open(fname) as f:
                for i, l in enumerate(f):
                    pass
        except:
            # problem, lets see if changing the encoding to latin helps
            print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.WARNING + "Couldn't decode selected list with standart UTF-8, trying Latin-1..." + colors.ENDC)
            try:
                i = 0
                with open(fname, encoding="latin-1") as f:
                    for i, l in enumerate(f):
                        pass
            except:
                # couldn't decode the list, die
                print(colors.OKCYAN + "[" + colors.FAIL + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.FAIL + "Couldn't decode selected list" + colors.ENDC)
                exit(0)
        
        return i + 1