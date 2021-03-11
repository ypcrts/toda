import logging

log = logging.getLogger(__name__)
log.setLevel(logging.WARN)
log.addHandler(logging.StreamHandler())


def nop(f):
    """
    syscall nop function used with `--dry-run`
    """
    name = f.__name__

    def _nop(*a, **k):
        log.debug("nop: %s %s %s" % (name, a, k))

    return _nop
