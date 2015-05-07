__author__ = 'TPei'


class StringParser:

    def __init__(self, d, rest):
        '''
        initializes a string parser for certain commands
        :param d: command dictionary e.g.: '@': 'users' ...
        :param rest: dict key under which the rest of the string will be returned
        :return:
        '''

        self.commands = {}
        self.data = {}

        for key, value in d.items():
            self.commands[key] = value
            self.data[value] = []
            self.rest = rest

    def parse(self, string):
        '''
        parse a string for given commands
        :param string:
        :return:
        '''
        split = string.split()

        remove = []

        for string in split:
            for key, value in self.commands.items():
                if string.startswith(key):
                    self.data[value].append(string[1:])
                    remove.append(string)

        for r in remove:
            split.remove(r)

        reassembled = " ".join(split)

        data = self.data.copy()
        data[self.rest] = reassembled

        self.clean()

        return data

    def clean(self):
        '''
        clean gathered data, but keep commands and rest name
        :return:
        '''
        for key, value in self.data.items():
            self.data[key] = []
