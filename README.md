<!-- vi: ft=markdown tw=80 ts=2 sw=2 sts=2 fdm=expr et: -->

# Toda

Toda ([תודה](https://en.wiktionary.org/wiki/%D7%AA%D7%95%D7%93%D7%94)) gives you
the power to safely deploy files using symlinks on any
operating system with Python installed.

Toda requires only core Python, supporting versions 3.4+ and 2.7. Toda has
multi-platform support for POSIX-compliant systems, Linux (Debian, Ubuntu, etc),
Windows, macOS and BSDs in that order of priority.

Catch22: Toda requires admin rights on Windows. See
[#8](https://github.com/ypcrts/toda/issues/8)

## `toda`
```
usage: toda [-h] [-n] [-m MANIFEST] [-f] [-v]
                   [{install,purge,inspect}] [section [section ...]]

creates symlinks described by a manifest

positional arguments:
  {install,purge,inspect}
  section               manifest target

optional arguments:
  -h, --help            show this help message and exit
  -n, --dry-run         nop out all syscalls, verbose
  -m MANIFEST, --manifest MANIFEST
                        path to custom manifest file
  -f, --force           allow clobbering files in target paths
  -v, --verbose
```

## `MANIFEST` file syntax

- `~/bin/destination_link: ./section/source_file`
  - destination-to-source mapping, with the two arguments delimited by a colon

- `$ bin`
  - defines the `bin` section

- `/bin/sh: @delete`
  deletes /bin/sh

- `@include: bin default`
   - includes `bin` and `default`
   - in each run of `manifest.py` includes are resolved recursively so that they
       are only processed once

### Why did you roll your own dotfiles management script?

See [the wiki](https://github.com/ypcrts/toda/wiki/Why%3F)
