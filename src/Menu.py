from Error import InputError


class Menu:
    def __init__(self):
        self.options = []

    def add_option(self, s):
        self.options.append(s)

    def parse_input(self, i):
        try:
            x = int(i)
            if x >= len(self.options) or x < 0:
                raise InputError(i, "The provided number is not in the range of acceptable values for the given menu "
                                    "option")
            else:
                return x
        except ValueError:
            raise InputError(i, "The provided input was not a number")

    def __str__(self):
        ret = ""
        for x in range(len(self.options)):
            ret += str(x) + ". " + str(self.options[x]) + "\n"

        return ret
