from argparse import ArgumentParser
from subprocess import run

from .net import run as _net
from .rule import run as _rule

# shell arguments
__arg_sh = ArgumentParser()
__arg_sh.add_argument("-a", action="store_true", help="actions runner")
__arg_sh.add_argument("-c", action="store_true", help="code format")
__arg_sh.add_argument("-g", action="store_true", help="generate output")
__arg_sh.add_argument("-i", action="store_true", help="install")
__arg = __arg_sh.parse_args()

# run steps
if __arg.i:
    # init git repo
    run(
        ["git", "submodule", "update", "--init", "--recursive", "--remote"], check=False
    )
    run(["git", "switch", "main"], check=False)
if __arg.a or __arg.g:
    _rule.run()
    _net.run()
if __arg.c:
    # format yaml
    run(["npx", "prettier", ".", "--write"], check=False)
    # format python
    run(["python", "-m", "isort", ".", "--profile=black"], check=False)
    run(["python", "-m", "black", "."], check=False)
