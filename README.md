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

I used [vcsh](https://github.com/RichiH/vcsh) for years, but I didn't like
having to carry around functionally-divided repos, as repo clone time is
a barrier. I found it clunky switching between many repos. I wanted many
deployable pieces in one `dots` repo and then to choose what to pollute the
system with. To complicate it further, I wanted to be able to use the management
script with other repos too and with other destinations.

### Why did you roll your own domain-specific language for the manifest file?

Is this an anti-pattern? It is.

Originally I wanted to use JSON, but the syntax is a pain to maintain manually.
Then I thought I'd use YAML to take advantage of references, but YAML spec
didn't offer all the functionality I wanted.

This eliminated categories of bugs that affect file formats
compatible with diverse range of weak parsers: (1) undefined behaviour in a spec
may promote divergent parser implementations, which may silently lead to
inconsistent state, (2) non-uniform support across parsers for extensions to the
spec may silently lead to inconsistent state, and (3) inconsistent
state leads to inconsistent code execution.



### Was rolling your own dotfiles management script an efficient use of your time?

Yes. Originally the project took only fifteen minutes.

Since, it has required some tender loving care in maintenance and dives, mostly
to breaking API changes courtesy of ahem, operating systems. Maintenance is
unavoidable in software written to support multiple versions of operating
systems, and multiple versions of an interpreted programming language famous for
the endless breaking changes in its core library.


### Did you create more tech debt for yourself than you bargained for?

Yes, absolutely, but there's no other cross-platform tool that does this job.
The main pain is maintaining Windows support because of the Windows 10 user
symlink support which was added in 2016. I haven't figured out how to make that
work well so, `toda` on Windows requires admin.
