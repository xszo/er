import yaml

from .env import (
    NAME_DOMAIN,
    NAME_IPASN,
    NAME_IPCIDR_V4,
    NAME_IPCIDR_V6,
    NAME_IPGEO,
    PATH_VAR,
    PATH_VAR_META,
)


class load:
    """load rules from var folder"""

    __data: dict[str, dict[str, list[str | int]]] = {
        NAME_DOMAIN: {},
        NAME_IPCIDR_V4: {},
        NAME_IPCIDR_V6: {},
        NAME_IPASN: {},
        NAME_IPGEO: {},
    }

    def __init__(self) -> None:
        # iter var folder
        for item in PATH_VAR.iterdir():
            if item == PATH_VAR_META:
                continue
            # read ruleset
            with open(item, "tr", encoding="utf-8") as file:
                self.__add(item.name.split(".")[0], yaml.safe_load(file))

    def get(self) -> dict:
        return self.__data

    def __add(self, name: str, dat: dict) -> None:
        # format domain
        if "domain" in dat and len(dat["domain"]) > 0:
            self.__data[NAME_DOMAIN][name] = [
                x[1:] if x[0] == "-" else "." + x for x in dat["domain"]
            ]
        # format and divide ipcidr 4 & 6
        if "ipcidr" in dat and len(dat["ipcidr"]) > 0:
            ip4 = []
            ip6 = []
            for x in dat["ipcidr"]:
                if x[0] == "[":
                    ip6.append(x[1:-1])
                elif ":" in x:
                    ip6.append(x)
                else:
                    ip4.append(x)
            if len(ip4) > 0:
                self.__data[NAME_IPCIDR_V4][name] = ip4
            if len(ip6) > 0:
                self.__data[NAME_IPCIDR_V6][name] = ip6
        # format ip
        if "ipgeo" in dat and len(dat["ipgeo"]) > 0:
            self.__data[NAME_IPGEO][name] = dat["ipgeo"]
        if "ipasn" in dat and len(dat["ipasn"]) > 0:
            self.__data[NAME_IPASN][name] = dat["ipasn"]
