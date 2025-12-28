import yaml

from ..lib import var
from .env import (
    NAME_CLASH,
    NAME_DOMAIN,
    NAME_IP,
    NAME_IPASN,
    NAME_IPCIDR_V4,
    NAME_IPCIDR_V6,
    NAME_IPGEO,
    NAME_QUANTUMULT,
    NAME_SURGE,
    PATH_OUT,
    REMOTE_URL,
    ZONE,
)

var.zone(ZONE)


class dump:
    """write rule files and register rule"""

    __data: dict[str, dict[str, list[str]]] = {}
    # rulesets

    def __init__(self) -> None:
        PATH_OUT.mkdir(parents=True, exist_ok=True)

    def dump(self, raw: dict) -> None:
        self.__data = raw
        # call modules and share rule url
        var.add(NAME_DOMAIN, self.__dump_domain())
        var.add(NAME_IP, self.__dump_ip())

    def __dump_domain(self) -> dict:
        res = {}
        for key, val in self.__data[NAME_DOMAIN].items():
            if len(val) == 0:
                continue
            # dump surge
            loc = key + "-" + NAME_DOMAIN + "-" + NAME_SURGE + ".txt"
            with open(
                PATH_OUT / loc,
                "tw",
                encoding="utf-8",
            ) as file:
                file.writelines(
                    [
                        (
                            "DOMAIN-WILDCARD," + x + "\n"
                            if "*" in x or "?" in x
                            else (
                                "DOMAIN-SUFFIX," + x[1:] + "\n"
                                if x[0] == "."
                                else "DOMAIN," + x + "\n"
                            )
                        )
                        for x in val
                    ]
                )
            res[key + "-" + NAME_SURGE] = REMOTE_URL + loc
            # dump clash
            loc = key + "-" + NAME_DOMAIN + "-" + NAME_CLASH + ".yml"
            with open(PATH_OUT / loc, "tw", encoding="utf-8") as file:
                yaml.safe_dump(
                    {"payload": ["+" + x if x[0] == "." else x for x in val]}, file
                )
            res[key + "-" + NAME_CLASH] = REMOTE_URL + loc
            # dump quantumult
            loc = key + "-" + NAME_DOMAIN + "-" + NAME_QUANTUMULT + ".txt"
            with open(
                PATH_OUT / loc,
                "tw",
                encoding="utf-8",
            ) as file:
                file.writelines(
                    [
                        (
                            "host-wildcard," + x + ",proxy\n"
                            if "*" in x or "?" in x
                            else (
                                "host-suffix," + x[1:] + ",proxy\n"
                                if x[0] == "."
                                else "host," + x + ",proxy\n"
                            )
                        )
                        for x in val
                    ]
                )
            res[key + "-" + NAME_QUANTUMULT] = REMOTE_URL + loc
        return res

    def __dump_ip(self) -> dict:
        res = {}
        # convert to {name: {type: [list]}}
        raw = {}
        for ty in (NAME_IPCIDR_V4, NAME_IPCIDR_V6, NAME_IPASN, NAME_IPGEO):
            for key, val in self.__data[ty].items():
                if len(val) == 0:
                    continue
                if key not in raw:
                    raw[key] = {}
                raw[key][ty] = val
        # format data
        for key, val in raw.items():
            dat_s = []
            dat_q = []
            # dump surge & quantumult
            if NAME_IPCIDR_V4 in val:
                dat_s.extend(["IP-CIDR," + x + "\n" for x in val[NAME_IPCIDR_V4]])
                dat_q.extend(["ip-cidr," + x + ",proxy\n" for x in val[NAME_IPCIDR_V4]])
            if NAME_IPCIDR_V6 in val:
                dat_s.extend(["IP-CIDR6," + x + "\n" for x in val[NAME_IPCIDR_V6]])
                dat_q.extend(
                    ["ip6-cidr," + x + ",proxy\n" for x in val[NAME_IPCIDR_V6]]
                )
            if NAME_IPASN in val:
                dat_s.extend(["IP-ASN," + str(x) + "\n" for x in val[NAME_IPASN]])
                dat_q.extend(["ip-asn," + str(x) + ",proxy\n" for x in val[NAME_IPASN]])
            if NAME_IPGEO in val:
                dat_s.extend(["GEOIP," + x.upper() + "\n" for x in val[NAME_IPGEO]])
                dat_q.extend(["geoip," + x + ",proxy\n" for x in val[NAME_IPGEO]])
            # write file
            loc = key + "-" + NAME_IP + "-" + NAME_SURGE + ".txt"
            with open(PATH_OUT / loc, "tw", encoding="utf-8") as file:
                file.writelines(dat_s)
            res[key + "-" + NAME_SURGE] = REMOTE_URL + loc
            loc = key + "-" + NAME_IP + "-" + NAME_QUANTUMULT + ".txt"
            with open(PATH_OUT / loc, "tw", encoding="utf-8") as file:
                file.writelines(dat_q)
            res[key + "-" + NAME_QUANTUMULT] = REMOTE_URL + loc
        return res
