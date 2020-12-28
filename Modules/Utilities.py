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
        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "?" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + text + " Answer with Y (means yes) or N (means no): [Y/n]" + colors.ENDC, end=" ")
        answer = input()
        if answer == "" or answer == "y" or answer == "yes" or answer == "Y":
            return True
        elif answer == "n" or answer == "no" or answer == "N":
            return False
        else:
            utilities.Question(0, text)

    # line counter
    def file_len(self, fname):
            with open(fname) as f:
                for i, l in enumerate(f):
                    pass
            return i + 1
