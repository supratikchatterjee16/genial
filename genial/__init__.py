import sys
import argparse
import logging

from genial.chat import serve_chat

# initiate logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setLevel(logging.DEBUG)
stdoutHandler.setFormatter(formatter)
logger.addHandler(stdoutHandler)


class ArgsParser(argparse.ArgumentParser):
    '''replacement class to handle default error response'''
    def error(self, message):# Modified to show help text on error
        sys.stderr.write('\033[0;31merror: %s\n\n\033[0m' % message)
        self.print_help()
        sys.exit(2)

def run():
    primary_parser = ArgsParser()
    subparser = primary_parser.add_subparsers(title="commands", dest="command")

    chat_subparser = subparser.add_parser("chat", help="Starts a chat agent in a CLI unless mentioned otherwise")
    stt_subparser = subparser.add_parser("stt", help="Starts the Speech-to-text engine[planned]")
    tts_subparser = subparser.add_parser("tts", help="Starts the Text-to-speech engine[planned]")

    args = primary_parser.parse_args()

    if args.command == 'load':
        serve_chat()