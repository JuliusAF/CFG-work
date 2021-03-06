from Error import InputError
from src.cfg import CFG
from src.parser import parse_user_input, parse_file


class Menu:
    def __init__(self):
        self.options = []

    def add_option(self, s):
        self.options.append(s)

    def parse_input(self, i):
        try:
            x = int(i)
            if x >= len(self.options)+1 or x < 0:
                raise InputError(i, "The provided number is not in the range of acceptable values for the given menu "
                                    "option")
            else:
                return x
        except ValueError:
            raise InputError(i, "The provided input was not a number")

    def __str__(self):
        ret = ""
        for x in range(len(self.options)):
            ret += str(x+1) + ". " + str(self.options[x]) + "\n"

        return ret


class LoadMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        # setup
        Menu.add_option(self, "Load from specified file")
        Menu.add_option(self, "Input through command line")

    def load_cfg(self):
        while True:
            print(self)
            try:
                t = input()
                userinput = Menu.parse_input(self, t)
                cfg = CFG()
                if userinput == 1:
                    print("Please input the file name of the CFG\n")
                    file = input()
                    parse_file(cfg, file)
                elif userinput == 2:
                    print("Please input production rules one by one\nType 'end' to exit\n")
                    parse_user_input(cfg)

                return cfg
            except InputError as e:
                print(e)



