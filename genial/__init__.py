import sys
import argparse
import logging

from genial.chat import serve_chat
from genial.asr import serve_asr
from genial.tts import serve_tts

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
    stt_subparser = subparser.add_parser("asr", help="Starts the Automatic Speech Recognition engine")
    tts_subparser = subparser.add_parser("tts", help="Starts the Text-to-speech engine")
    server_subparser = subparser.add_parser("server", help="Start the dirstributed server.")

    

    tts_subparser.add_argument("-f", "--file", help="Filepath to voice recording", type=str, nargs=1, required=True)

    args = primary_parser.parse_args()

    if args.command == 'chat':
        serve_chat()
    elif args.command == 'asr':
        serve_asr()
    elif args.command == 'tts':
        serve_tts()
    elif args.command == 'server':
        pass
    else :
        primary_parser.print_help()