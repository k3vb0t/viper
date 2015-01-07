# This file is part of Viper - https://github.com/botherder/viper
# See the file 'LICENSE' for copying permission.

import argparse


class ArgumentErrorCallback(Exception):

    def __init__(self, message, level=''):
        self.message = message.strip() + '\n'
        self.level = level.strip()

    def __str__(self):
        return '{}: {}'.format(self.level, self.message)

    def get(self):
        return self.level, self.message


class ArgumentParser(argparse.ArgumentParser):

    def print_usage(self):
        raise ArgumentErrorCallback(self.format_usage())

    def print_help(self):
        raise ArgumentErrorCallback(self.format_help())

    def error(self, message):
        raise ArgumentErrorCallback(message, 'error')

    def exit(self, status, message=None):
        if message is not None:
            raise ArgumentErrorCallback(message)


class Module(object):
    cmd = ''
    description = ''
    args = []
    authors = []
    output = []

    def __init__(self):
        self.parser = ArgumentParser(prog=self.cmd, description=self.description)

    def set_args(self, args):
        self.args = args

    def log(self, event_type, event_data):
        self.output.append(dict(
            type=event_type,
            data=event_data
        ))

    def usage(self):
        self.log('', self.parser.format_usage())

    def help(self):
        self.log('', self.parser.format_help())

    def run(self):
        self.parsed_args = None
        if len(self.args) == 0:
            self.usage()
        else:
            try:
                self.parsed_args = self.parser.parse_args(self.args)
            except ArgumentErrorCallback as e:
                self.log(*e.get())
