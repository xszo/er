import re
from base64 import b64decode
from copy import deepcopy

import yaml

from ..lib.net import get as net_get
from .env import (
    NAME_DOMAIN,
    NAME_IPCIDR_V4,
    NAME_IPCIDR_V6,
    PATH_TMP,
    REX_COMMENT,
    REX_VAR,
)


class getrex:
    """get link text and use rex to format"""

    __data: dict[str, dict[str, list[str]]] = {
        NAME_DOMAIN: {},
        NAME_IPCIDR_V4: {},
        NAME_IPCIDR_V6: {},
    }
    __rex_var: list[tuple[re.Pattern, str]] = deepcopy(REX_VAR)
    __no: list[str] = []

    def __init__(self) -> None:
        PATH_TMP.mkdir(parents=True, exist_ok=True)

    def __del__(self) -> None:
        # dump no match line
        with open(PATH_TMP / "no-rex.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(self.__no, file)

    def get(self) -> dict:
        return self.__data

    def add(self, link: str, patten: dict, pre: list) -> None:
        # download file
        dat = net_get(link)
        # use pre processor
        if "b64" in pre:
            # b64 decode
            dat = b64decode(dat).decode("utf-8")
        # match patten
        self.__add_patten(dat.splitlines(), self.__compile_patten(patten))

    def add_var(self, dat: dict) -> None:
        # compile var
        for name, line in dat.items():
            self.__rex_var.append((re.compile("\\\\=" + name + "\\\\"), line))

    def __compile_patten(self, rex: dict) -> tuple:
        res = []
        for name, ls in rex.items():
            for line in ls:
                # insert var
                for v in self.__rex_var:
                    line = re.sub(v[0], v[1], line)
                # format type code
                match ((line := line.split("  "))[0]):
                    case "d":
                        ty = NAME_DOMAIN
                    case "4":
                        ty = NAME_IPCIDR_V4
                    case "6":
                        ty = NAME_IPCIDR_V6
                    case _:
                        continue
                # format match rules, into: type name, match: patten expand
                res.append((ty, name, re.compile(line[1]), line[2]))
                # create data entry
                if name not in self.__data[ty]:
                    self.__data[ty][name] = []
        return tuple(res)

    def __add_patten(self, dat: tuple | list, rex: tuple | list) -> None:
        for line in dat:
            # skip comment
            if re.match(REX_COMMENT, line):
                continue
            line = line.lower()
            # match patten and categorize
            for pat in rex:
                if lma := re.match(pat[2], line):
                    self.__data[pat[0]][pat[1]].append(lma.expand(pat[3]))
                    break
            else:
                self.__no.append(line)
