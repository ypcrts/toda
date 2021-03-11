from .model import Manifest
import logging
from os.path import exists, lexists
from os import remove
from pprint import pprint
from os import symlink, makedirs, chdir
from os.path import join, dirname, basename, lexists, exists, isdir, islink
from shutil import rmtree


log = logging.getLogger(__name__)
log.setLevel(logging.WARN)
log.addHandler(logging.StreamHandler())


def _deploy_one(dest, src, force):
    # type: str, str, bool -> bool
    """
    :assumptions: manifest has already been parsed and validated.
    """

    destdir = dirname(dest)
    destname = basename(dest)

    if lexists(dest) or exists(dest):
        if not force:
            log.info("skipped (exists): %s" % dest)
            return
        if isdir(dest) and not islink(dest):
            rmtree(dest)
        else:
            remove(dest)

    if not isdir(destdir):
        makedirs(destdir, 0o755)

    chdir(destdir)
    if src in Manifest.SRC_MACROS:
        if src == Manifest.DELETE_MACRO:
            if lexists(dest):
                remove(dest)
        else:
            assert False
            log.critical("{:s} is an invalid macro".format(src))
            return False
        return True
    assert exists(src), "Manifest src `{:}` does not exist on the filesystem".format(
        src
    )
    try:
        # XXX: Following line's kwarg is useless. [ypcrts // 20180120]
        # symlink(src, destname, target_is_directory=isdir(src))
        # XXX: No kwargs in py3. Should be unnecessary per docs:
        #     "If the target is present, the type of the symlink will be created to match."
        #      - https://docs.python.org/3.6/library/os.html
        symlink(src, destname)
        log.warning("linked %s" % dest)
    except OSError as e:
        log.error("failure - %s :: %s" % (e, dest))


class Actions:
    def __init__(self, manifest, args):
        self.manifest = manifest
        self.args = args
        self._assert_symlink_works()

    def install(self):
        for section in self.args.section:
            for (dest, src) in self.manifest.iter_section(section):
                log.debug("installing {s}".format(dest))
                _deploy_one(dest, src, force=self.args.force)

    def purge(self):
        for section in self.args.section:
            for (dest, _) in self.manifest.iter_section(section):
                if lexists(dest) or exists(dest):
                    log.warning("purged %s" % dest)
                    remove(dest)

    def inspect(self):
        print("inspecting...")
        pprint(
            dict(
                (
                    key,
                    self.manifest[key].get("@include", None),
                )
                for key in self.manifest.keys()
            )
        )

    def _assert_symlink_works(self):
        if self.args.no_preflight:
            return True
        nonce = "symlinknonce-lkjho8ho98hp923h4iouh90sa0d98u9d8j1p92d8"
        target = nonce + ".target"
        try:
            symlink(nonce, target)
        except OSError:
            raise
        finally:
            if lexists(target):
                remove(target)
