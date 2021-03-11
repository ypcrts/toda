from __future__ import print_function

import os
import argparse
import logging

from .model import Manifest
from .controller import Actions

log = logging.getLogger(__name__)
log.setLevel(logging.WARN)
log.addHandler(logging.StreamHandler())

def main():
    startdir = os.getcwd()
    parser = argparse.ArgumentParser(
        description="creates symlinks described by a manifest"
    )
    parser.add_argument(
        "action",
        choices=("install", "purge", "inspect"),
        nargs="?",
        type=str,
        default="inspect",
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="nop out all syscalls, verbose"
    )
    parser.add_argument(
        "-m",
        "--manifest",
        type=str,
        help="path to custom manifest file",
        default="./MANIFEST",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="allow clobbering files in target paths",
    )
    parser.add_argument("-v", "--verbose", default=0, action="count")
    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        default=None,
        help="override HOME and USERPROFILE (tilde expansion)",
    )
    parser.add_argument(
        "--no-preflight",
        help="skip the preflight sanity checks",
        action="store_true",
        dest="no_preflight",
    )
    parser.add_argument("section", help="manifest target", type=str, nargs="*")

    args = parser.parse_args()

    if args.dry_run:
        from .nop import nop

        args.verbose = 3
        log.warn("seting up dry run")
        rmtree = nop(rmtree)
        remove = nop(remove)
        makedirs = nop(makedirs)
        symlink = nop(symlink)
        chdir = nop(chdir)

    if args.dir:
        # XXX: monstrosity below
        os.environ["HOME"] = os.environ["USERPROFILE"] = args.dir

    if args.verbose >= 2:
        log.setLevel(logging.DEBUG)
    elif args.verbose >= 1:
        log.setLevel(logging.INFO)

    m = Manifest(path=args.manifest)
    if not args.section:
        args.section = ("default",)
    else:
        args.section = list(map(lambda sn: sn.rstrip("/"), args.section))
        for sn in args.section:
            assert sn in m, "section `{:s}` is not in the manifest".format(sn)

    getattr(Actions(m, args), args.action)()


if __name__ == "__main__":
    main()
