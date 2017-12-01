import sys

is_windows = sys.platform in (
    "win32",
    "cygwin",
)
# is_linux = sys.platform.startswith('linux')
# is_macos = sys.platform ==  'darwin'
PY3 = sys.version_info >= (
    3,
    0,
    0,
)

if PY3:

    def iteritems(obj):
        return obj.items()


else:
    if is_windows:
        raise EnvironmentError("python 3 required on windows")
    # Due to missing py2 os.symlink: but could call using ctypes

    def iteritems(obj):
        return obj.iteritems()
