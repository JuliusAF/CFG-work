class Error(Exception):
    pass


class InputError(Error):

    def __init__(self, i, message):
        self.input = i
        self.message = message

    def __str__(self):
        return "Input error from: " + self.input + "\n" + self.message + "\n"
