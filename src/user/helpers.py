class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def print_ok(message):
    print(bcolors.OK + str(message) + bcolors.RESET)

def print_warning(message):
    print(bcolors.WARNING + str(message) + bcolors.RESET)

def print_fail(message):
    print(bcolors.FAIL + str(message) + bcolors.RESET)