import yaml

from .dump import dump
from .env import NAME_DOMAIN, PATH_VAR_META
from .getrex import getrex
from .getvlc import getvlc
from .load import load
from .remix import remix


def run() -> None:
    with open(PATH_VAR_META, "tr", encoding="utf-8") as file:
        meta = yaml.safe_load(file)

    data = load().get()

    (rexer := getrex()).add_var(meta["var"])
    for line in meta["rex"]:
        rexer.add(line["url"], line["get"], pre=line["pre"])
    __merge(data, rexer.get())

    vlcer = getvlc()
    for key, val in meta["vlc"].items():
        vlcer.add(key, val)
    __merge(data, {NAME_DOMAIN: vlcer.get()})

    ls = {}
    for line in meta["list"]:
        if len(line := line.split(" ")) > 1:
            ls[line[0]] = line[1:]

    (remixer := remix()).add(data)
    for k, v in ls.items():
        remixer.mix(k, v)
    data = remixer.get(tuple(ls.keys()))

    dump().dump(data)


def __merge(d1: dict, d2: dict) -> None:
    for k1, v1 in d2.items():
        if k1 in d1:
            for k2, v2 in v1.items():
                if k2 in d1[k1]:
                    d1[k1][k2].extend(v2)
                else:
                    d1[k1][k2] = v2
        else:
            d1[k1] = v1
