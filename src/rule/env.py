from re import compile as re_c

from .. import env as __env

ZONE = __env.NAME_RULE

# name
NAME_DOMAIN = "dn"
NAME_IP = "ip"
NAME_IPCIDR_V4 = "ip4"
NAME_IPCIDR_V6 = "ip6"
NAME_IPASN = "ipas"
NAME_IPGEO = "ipgeo"
NAME_SURGE = "s"
NAME_CLASH = "c"
NAME_QUANTUMULT = "q"

# path
PATH_VAR = __env.PATH_VAR_RULE
PATH_VAR_META = PATH_VAR / "list.yml"
PATH_TMP = __env.PATH_TMP_RULE
PATH_OUT = __env.PATH_OUT_RULE

REMOTE_URL = __env.REMOTE_URL_RULE

# getrex.py
REX_COMMENT = re_c("^\\s*($|#|!)")
REX_VAR = [
    (
        re_c("\\\\=dn\\\\"),
        "((?:[a-z0-9\\*\\?](?:[a-z0-9\\-\\*\\?]*[a-z0-9\\*\\?])?\\.)*"
        "(?:[a-z]+|xn--[a-z0-9]+))",
    ),
]

# getvlc.py
VLC_REPO_URL = "https://github.com/v2fly/domain-list-community"
VLC_REPO_PATH = PATH_TMP / "vlc"
VLC_DATA = VLC_REPO_PATH / "data"
VLC_REX_INCL = re_c("^include:([\\w\\-\\!]+)\\s*(?:#.*)?$")
VLC_REX_RULE = (
    (
        re_c(
            "^full:"
            "((?:[a-z0-9\\*\\?](?:[a-z0-9\\-\\*\\?]*[a-z0-9\\*\\?])?\\.)*(?:[a-z]+|xn--[a-z0-9]+))"
            "(?:$|\\s)"
        ),
        "\\1",
    ),
    (
        re_c(
            "^(?:domain:)?"
            "((?:[a-z0-9\\*\\?](?:[a-z0-9\\-\\*\\?]*[a-z0-9\\*\\?])?\\.)*(?:[a-z]+|xn--[a-z0-9]+))"
            "(?:$|\\s)"
        ),
        ".\\1",
    ),
)

# remix.py
MAX_DOMAIN_LEVEL = 10
