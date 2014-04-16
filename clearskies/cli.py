#!/usr/bin/env python3

from clearskies.client import ClearSkies
from clearskies.exc import ClientException

import sys
import argparse
import logging

log = logging.getLogger("clearskies.cli")  # __name__ == "__main__" if we're debugging


class CLI(object):
    def __init__(self):
        self.cs = None

    def main(self, args):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)19.19s %(levelname)4.4s %(message)s")
        module_log = logging.getLogger("clearskies")

        parser = argparse.ArgumentParser(description='ClearSkies python interface demo')
        parser.add_argument('-v', '--verbose', action="store_true", default=False)

        subparsers = parser.add_subparsers()

        parser_stop = subparsers.add_parser('stop')
        parser_stop.set_defaults(func=self.stop)

        parser_pause = subparsers.add_parser('pause')
        parser_pause.set_defaults(func=self.pause)

        parser_resume = subparsers.add_parser('resume')
        parser_resume.set_defaults(func=self.resume)

        parser_status = subparsers.add_parser('status', help="Give program status")
        parser_status.set_defaults(func=self.status)

        parser_create_share = subparsers.add_parser('create', help="Create new share")
        parser_create_share.add_argument('path')
        parser_create_share.set_defaults(func=self.create_share)

        parser_list_shares = subparsers.add_parser('list', help="List all shares and sync status")
        parser_list_shares.set_defaults(func=self.list_shares)

        parser_create_access_code = subparsers.add_parser('share', help="Make access code to be given to others")
        parser_create_access_code.add_argument('path')
        parser_create_access_code.add_argument('mode')
        parser_create_access_code.set_defaults(func=self.create_access_code)

        parser_add_share = subparsers.add_parser(
            'attach',
            help="Add access code from someone else, creating new share at [path]"
        )
        parser_add_share.add_argument('code')
        parser_add_share.add_argument('path')
        parser_add_share.set_defaults(func=self.add_share)

        parser_remove_share = subparsers.add_parser('detach', help="Stop syncing path")
        parser_remove_share.add_argument('path')
        parser_remove_share.set_defaults(func=self.remove_share)

        args = parser.parse_args(args[1:])

        self.cs = ClearSkies()

        if args.verbose:
            module_log.setLevel(logging.DEBUG)
        else:
            module_log.setLevel(logging.INFO)

        try:
            self.cs.connect()
        except ClientException as e:
            log.error("Couldn't connect to daemon: %s" % e)
            log.error("Is the daemon running?")
            return

        if hasattr(args, "func"):
            args.func(args)
        else:
            log.error("No command specified, use --help for a list")

    def stop(self, args):
        print(self.cs.stop())

    def pause(self, args):
        print(self.cs.pause())

    def resume(self, args):
        print(self.cs.resume())

    def status(self, args):
        print(self.cs.status())

    def create_share(self, args):
        print(self.cs.create_share(args.path))

    def list_shares(self, args):
        shares = self.cs.list_shares()

        fmt = "%6s %-20s"
        print(fmt % ("Status", "Share"))
        print(fmt % ("~~~~~~", "~~~~~"))
        for share in shares:
            print(fmt % (share["status"], share["path"]))

    def create_access_code(self, args):
        print(self.cs.create_access_code(args.path, args.mode))

    def add_share(self, args):
        print(self.cs.add_share(args.code, args.path))

    def remove_share(self, args):
        print(self.cs.remove_share(args.path))


def main():
    sys.exit(CLI().main(sys.argv))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(CLI().main(sys.argv))
