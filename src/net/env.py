from .. import env as __env
from ..rule.env import (
    NAME_CLASH,
    NAME_DOMAIN,
    NAME_IP,
    NAME_SURGE,
)

ZONE = __env.NAME_NET
ZONE_RULE = __env.NAME_RULE

# path
PATH_VAR = __env.PATH_VAR_NET
PATH_VAR_LIST = PATH_VAR / "list.yml"
PATH_VAR_REX = __env.PATH_VAR / "re.yml"
PATH_TMP = __env.PATH_TMP_NET
PATH_OUT = __env.PATH_OUT_NET

# load.py
URI = __env.REMOTE_URL
URI_NET = __env.REMOTE_URL_NET
INT = __env.REMOTE_INTERVAL

# dump.py
REMOTE_URI_NULL = __env.REMOTE_URL_NULL
EXT_QUANTUMULT_PARSER = (
    "https://cdn.jsdelivr.net/gh/KOP-XIAO/QuantumultX@master/Scripts/resource-parser.js"
)
