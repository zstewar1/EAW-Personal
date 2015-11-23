#!/usr/bin/env python3
import argparse
import logging

import conf
import loghelp
import projspeed
import factionchanges

logger = loghelp.get_logger(__name__)

def recursive_delete(path):
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        for child in path.iterdir():
            if child.is_dir():
                recursive_delete(child)
            else:
                child.unlink()
        path.rmdir()

def main(clean=False):
    if clean:
        recursive_delete(conf.outdir)

    conf.outxml.mkdir(parents=True, exist_ok=True)

    projspeed.execute()
    factionchanges.execute()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scripted Mod Maker')
    parser.add_argument('-c', '--clean', default=False, action='store_true')
    parser.add_argument('-v', '--verbose', default=4, action='count')

    args = parser.parse_args()

    if args.verbose == 0:
        loghelp.set_levels(logging.CRITICAL)
    elif args.verbose == 1:
        loghelp.set_levels(logging.ERROR)
    elif args.verbose == 2:
        loghelp.set_levels(logging.WARNING)
    elif args.verbose == 3:
        loghelp.set_levels(logging.INFO)
    elif args.verbose >= 4:
        loghelp.set_levels(logging.DEBUG)

    main(args.clean)
