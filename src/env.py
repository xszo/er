from pathlib import Path

# name
NAME_NET = "net"
NAME_RULE = "rule"

# path
PATH_VAR = Path("var/")
PATH_VAR_NET = PATH_VAR / NAME_NET
PATH_VAR_RULE = PATH_VAR / NAME_RULE

PATH_TMP = Path("tmp/")
PATH_TMP_NET = PATH_TMP / NAME_NET
PATH_TMP_RULE = PATH_TMP / NAME_RULE

PATH_OUT = Path("out/")
PATH_OUT_NET = PATH_OUT / NAME_NET
PATH_OUT_RULE = PATH_OUT / NAME_RULE

# remote
REMOTE_URL = "https://xszo.github.io/er/"
REMOTE_URL_NULL = "https://xszo.github.io/er/null"
REMOTE_URL_NET = REMOTE_URL + NAME_NET + "/"
REMOTE_URL_RULE = REMOTE_URL + NAME_RULE + "/"

REMOTE_INTERVAL = 604800
