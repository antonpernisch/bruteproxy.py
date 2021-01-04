# BruteProxy proxy rotater module for proxy looping
import linecache
from Modules.Utilities import utilities
import time
import json

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

class rotater:

    def prepareDicts(self):
        # count the lines in proxylist by file_len() utility
        rotater.proxylist_len = utilities.file_len(0, rotater.proxylist)
        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.DARK_CYAN + "Loaded " + colors.BOLD + str(rotater.proxylist_len) + colors.ENDC + colors.DARK_CYAN+ " proxies from file" + colors.ENDC)

    def setup(self, proxylist, proxychange):
        rotater.proxylist = proxylist
        rotater.proxychange = proxychange

        rotater.currentProxyLine = 2

        rotater.run = True
        rotater.pause = False

        try:
            rotater.currentProxyRaw = linecache.getline(rotater.proxylist, 1).strip().split(" ")
            rotater.currentProxy = json.loads("{\"" + rotater.currentProxyRaw[0] + "\": \"" + rotater.currentProxyRaw[1] + "\"}")
        except:
            print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "] " + colors.ENDC + colors.WARNING + "Proxy format can not be understand, please end the attack" + colors.ENDC)

        # prepare dict
        rotater.prepareDicts(0)

    def rotate(self):
        from Modules.Attacker import attacker

        # main thread loop
        while rotater.run:
            if rotater.pause:
                time.sleep(0.1)
                continue
            if attacker.attempt >= rotater.proxychange:
                # we must change the proxy
                try:
                    rotater.currentProxyRaw = linecache.getline(rotater.proxylist, rotater.currentProxyLine).strip().split(" ")
                    rotater.currentProxy = json.loads("{\"" + rotater.currentProxyRaw[0] + "\": \"" + rotater.currentProxyRaw[1] + "\"}")
                except:
                    print(colors.OKCYAN + "[" + colors.WARNING + colors.BOLD + "!" + colors.ENDC + colors.OKCYAN + "] " + colors.ENDC + colors.WARNING + "Proxy format can not be understand, please end the attack" + colors.ENDC)

                # check if we have reached the end of file, go to the start if so and if no, just increse the currentProxyLine
                if rotater.currentProxyLine == rotater.proxylist_len:
                    rotater.currentProxyLine = 1
                else:
                    rotater.currentProxyLine = rotater.currentProxyLine + 1

                # reset the attempt
                attacker.attempt = 0

        print(colors.OKCYAN + "[" + colors.OKBLUE + colors.BOLD + "i" + colors.ENDC + colors.OKCYAN + "]" + " " + colors.ENDC + colors.OKCYAN + "Proxy-looping thread is terminated" + colors.ENDC)
        return
