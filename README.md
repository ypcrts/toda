<!-- vi: ft=markdown tw=80 ts=2 sw=2 sts=2 fdm=expr et: -->

# Toda

Toda ([תודה](https://en.wiktionary.org/wiki/%D7%AA%D7%95%D7%93%D7%94)) gives you
the power to safely deploy files using symlinks on any
operating system with Python installed.

Toda requires only core Python, supporting versions 3.4+ and 2.7 in that order.

Multi-platform support for POSIX-compliant systems, Debian GNU/Linux, Windows,
  macOS and BSDs in that order of priority.

It requires admin on Windows, because symlinking is
a privileged operation on Windows.

### Why did you roll your own dotfiles management script?

I used [vcsh](https://github.com/RichiH/vcsh) for a few years, but I didn't like
having to carry around functionally-divided repos, as repo clone time is
a barrier. I found it clunky switching between many repos. I also wanted native
Windows support. I wanted many deployable pieces in one `dots` repo and then to
choose what to pollute the system with. To complicate it further, I wanted to be
able to use the management script with other repos too and with other
destinations.

The result is I have been using this management script on all three major
desktop OSes since 2017 and it makes me happy. I take this script with me
wherever I go, as is the intent of a dotfiles repo.

The `purge` feature allows programmatic cleanup.

### Why did you roll your own manifest file format specification?

I've asked the blue if I think this was an anti-pattern. It is. But I chose this
path consciously. It was suggested that I preemptively explain my thinking. So
here we go.

Originally I wanted to use JSON, but the syntax is a pain to maintain manually.
Then I thought I'd use YAML to take advantage of references. When I realized
that multi-chain sets with references were not supported by any YAML spec
I reviewed, I judged that relying on an imperfect file format and implementing
my own application layer on top of it would be harder to interpret for others,
and subject to errors in the parser. By working backwards from my custom spec,
I could guarantee that harmony between the parser and application logic.

My decision eliminated categories of threats that affect file formats
compatible with diverse range of weak parsers: (1) undefined behaviour in a spec
may cause divergent parser implementations, which may silently lead to
inconsistent state, (2) non-uniform support across parsers for extensions to the
spec may silently lead to inconsistent state, (3) improper parser
implementations may silently lead to inconsistent state, and (4) inconsistent
state leads to inconsistent code execuion.

I wanted to be able to delete some files, link files, link files in a directory
to target location, include other sections. I didn't want this done in code.
I wanted a file format that only contained primitives, so that way I could look
at an untrusted manifest file and see what it does.

I decided to write my own file spec inspired by the Makefile spec's destination
and source mappings. Unlike Makefiles, my spec does not allow arbitrary command
execution.


### Was rolling your own file spec and dotfiles management script an efficient use of your time?

Yes. Originally the project took only fifteen minutes.

Since, it has required some tender loving care in maintenance and dives, mostly to
breaking API changes courtesy of ahem, operating systems.
Maintenance is unavoidable in software written to
support multiple versions of operating systems, and multiple
versions of an interpreted programming language famous for the endless breaking
changes in its core library.


### Did you create more tech debt for yourself than you bargained for?

Yes, absolutely, but there's no other cross-platform tool that does this job.
The main pain is maintaining Windows support because of new OS changes. 


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
