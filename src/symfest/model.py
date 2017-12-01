from . import iteritems
import os
import logging
from os.path import normpath, join, basename, dirname, expanduser

log = logging.getLogger(__name__)
log.setLevel(logging.WARN)
log.addHandler(logging.StreamHandler())


class IllegalSyntax(Exception):
    pass


class Manifest(dict):
    DELETE_MACRO = "@delete"
    INCLUDE_MACRO = "@include"
    SRC_MACROS = {DELETE_MACRO}
    DEST_MACROS = {INCLUDE_MACRO}
    INIT_KWARGS = {"path", "force", "startdir"}

    def __init__(self, **kw):
        for key in kw.keys():
            if key not in self.INIT_KWARGS:
                raise ValueError("{s} is an invalid keyword-argument".format(key))
        path = kw.get("path")
        self._startdir = kw.get("startdir")
        if not self._startdir:
            self._startdir = os.getcwd()
        if not path:
            return
        with open(path, "r") as fp:
            self._parse(fp)

    @staticmethod
    def _parse_line_comment(line):
        return not line or len(line) and line[0] == "#"

    @staticmethod
    def _parse_line_section_declaration(line):
        has_prefix = line and len(line) and line[0] == "$"
        if not has_prefix:
            return None
        if line[-1] in "@*:":
            raise IllegalSyntax(
                "section name {:s} cannot end in {:s}".format(line[:-1], line[-1])
            )
        return line.strip("$").strip()

    @staticmethod
    def _parse_part_macro(part):
        return part and isinstance(part, str) and part.startswith("@")

    @staticmethod
    def _is_macro_or_parsed(rubberducky):
        return rubberducky and (
            not isinstance(rubberducky, str) or rubberducky.startswith("@")
        )

    @staticmethod
    def _parse_part_terminal_glob(part):
        return part and isinstance(part, str) and part.endswith("*")

    def _parse(self, fp):
        section = None
        for (i, line) in enumerate(fp, 1):
            line = line.strip()
            if self._parse_line_comment(line):
                continue

            new_section = self._parse_line_section_declaration(line)
            if new_section:
                if new_section in self:
                    raise IllegalSyntax(
                        "line {:d}: duplicate section declaration".format(i)
                    )
                section = self[new_section] = dict()
                continue
            elif section is None:
                raise IllegalSyntax(
                    "line {:d}: target definition before "
                    "section declaration".format(i)
                )

            paths = line.split(":", 2)
            unparsed_separators = paths[-1].find(":") > -1
            if unparsed_separators:
                raise IllegalSyntax("line {:d}: multiple colons".format(i))

            dest, src = paths = map(lambda p: p.strip(), paths)
            dest_is_macro = self._parse_part_macro(dest)
            src_is_macro = self._parse_part_macro(src)

            if dest_is_macro:
                if dest not in self.DEST_MACROS:
                    raise IllegalSyntax("line {:d}: invalid {:}".format(i, dest))

            if dest == self.INCLUDE_MACRO:
                src = set(src.split(" "))
            elif src_is_macro:
                if src not in self.SRC_MACROS:
                    raise IllegalSyntax("line {:d}: invalid {:}".format(i, src))

            if not (dest_is_macro or src_is_macro):
                if dest in section:
                    raise IllegalSyntax(
                        "line {:d}: target redefinition `{:}` "
                        "in same section".format(i, dest)
                    )

                has_glob = self._parse_part_terminal_glob(src)
                assert has_glob ^ (
                    not dest.endswith("/")
                ), "line {:d}: glob dest must be directory " "ending with `/`".format(i)

            section[dest] = src

    def iter_section(self, section_name, included=None):
        # recursive base case
        if not included:
            included = set()
        included.add(section_name)
        for (dest, src) in iteritems(self[section_name]):
            if not self._is_macro_or_parsed(src):
                src = normpath(join(self._startdir, expanduser(src)))
            if not self._is_macro_or_parsed(dest):
                dest = normpath(expanduser(dest))
            else:
                if dest == self.INCLUDE_MACRO:
                    included.update(src)
                    for sn in src:
                        assert (
                            sn != section_name
                        ), "cannot include `{:}` inside itself" "!".format(section_name)
                        assert sn in self, (
                            "cannot include `{:}` "
                            "dependency `{:}` does not exist".format(section_name, sn)
                        )
                        for s in self.iter_section(sn, included):
                            yield s
                    continue
                else:
                    assert False

            dest = normpath(dest)
            has_glob = self._parse_part_terminal_glob(src)
            if not has_glob:
                yield dest, src
                continue

            src = src.strip("*")
            names = os.listdir(src)
            for name in names:
                yield (
                    join(dest, name),
                    join(src, name),
                )
