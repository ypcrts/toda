<!-- vi: ft=markdown tw=80 ts=2 sw=2 sts=2 fdm=expr et: -->

# Symfest

Symfest gives you the power to safely deploy files using symlinks on any
operating system with Python installed.

Symfest requires only core Python, supporting versions 3.4+ and 2.7 in that order.

Multi-platform support for POSIX-compliant systems, Debian GNU/Linux, Windows,
  macOS and BSDs in that order of priority.

It requires admin on Windows, because symlinking is
a privileged operation on Windows. A new devel

### Why did you roll your own manifest file format specification?

I've been questions out of the blue in job interviews for doing this, and it was
suggested that I preemptively defend my choices. So here we go.

Originally I wanted to use JSON, but the syntax is a pain to maintain manually
and it does not have references. Then I thought I'd use YAML to take advantage
of references. When I realized that multi-chain sets with references were not
supported by any YAML spec I reviewed, I judged that relying on an imperfect
file format and implementing my own application layer on top of it would be
harder to interpret for others, and subject to errors in the parser. By working
backwards from my custom spec, I could guarantee that harmony between the parser
and application logic.

My decision eliminated several categories of threats that affect file formats
compatible with diverse range of weak parsers: (1) undefined behaviour in a spec
may cause divergent parser implementations, which may silently lead to
inconsistent state, (2) non-uniform support across parsers for extensions to the
spec may silently lead to inconsistent state, (3) improper parser
implementations may silently lead to inconsistent state, and (4) inconsistent
state has an unmanageable risk from the spec and parser may hit edge cases and
corner cases in application logic resulting in inconsistent code execuion.

I wanted to be able to delete some files, link files, link files in a directory
to target location, include other sections. I didn't want this done in code.
I wanted a file format that only contained primitives, so that way I could look
at an untrusted manifest file and see what it does.

I decided to write my own file spec inspired by the Makefile spec's destination
and source mappings. Unlike Makefiles, my spec does not allow arbitrary command
execution.

### Why did you roll your own management script?

I had used [vcsh](https://github.com/RichiH/vcsh) for about four years. After trying
other options, but I didn't like having to carry around functionally-divided
repos, as repo clone time is a barrier. I found it clunky switching between many
repos. I also wanted native Windows support. I wanted many deployable pieces in
one `dots` repo and then to choose what to pollute the system with. To
complicate it further, I wanted to be able to use the management script with
other repos too and with other destinations.

The result is I have been using this management script on all three major
desktop OSes since 2017 and it makes me happy. I take this script with me
wherever I go, as is the intent of a dotfiles repo.

The `purge` feature allows programmatic cleanup.

### Was rolling your own file spec and management script an efficient use of your time?

Yes. Originally the project took only fifteen minutes.

Since, it has required some tender loving care in maintenance and dives, mostly to
breaking API changes courtesy of ahem, operating systems.
Maintenance is unavoidable in software written to
support multiple versions of operating systems, and multiple
versions of an interpreted programming language famous for the endless breaking
changes in its core library.


## `manifest.py`
```
usage: manifest.py [-h] [-n] [-m MANIFEST] [-f] [-v]
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
