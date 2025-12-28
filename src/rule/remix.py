from .env import MAX_DOMAIN_LEVEL, NAME_DOMAIN


class remix:
    """remix rulesets"""

    __pool: dict[str, dict[str, set[str]]] = {NAME_DOMAIN: {}}
    """rule pool, {type: {name: [list]}}"""
    __pool_domain: dict[str, set[str]] = {}

    def add(self, dat: dict) -> None:
        """add item to pool"""
        for ty, ls in dat.items():
            # sync type
            if ty not in self.__pool:
                self.__pool[ty] = {}
            # loop add
            for key, val in ls.items():
                # add domain
                if ty == NAME_DOMAIN:
                    self.__pool_domain[key] = set(val)
                # add ruleset
                else:
                    self.__pool[ty][key] = set(val)

    def get(self, name: list | tuple) -> dict:
        """get items from pool"""
        res = {NAME_DOMAIN: {}}
        # get pool
        for ty, ls in self.__pool.items():
            res[ty] = {}
            for key in name:
                if key in ls and len(ls[key]) > 0:
                    res[ty][key] = tuple(sorted(ls[key]))
        # get domain
        for key in name:
            if key in self.__pool_domain and len(self.__pool_domain[key]) > 0:
                res[NAME_DOMAIN][key] = tuple(sorted(self.__pool_domain[key]))
        return res

    def mix(self, name: str, cmd: list) -> None:
        """mix rules: new ruleset, from rulesets"""
        # add new set
        for ls in self.__pool.values():
            ls[name] = set()
        self.__pool_domain[name] = set()
        # mix common ruleset
        excl_ls = []
        for line in cmd:
            # include then exclude
            if line[0] == "-":
                excl_ls.append(line[1:])
                continue
            # do include
            for ls in self.__pool.values():
                if line in ls:
                    ls[name].update(ls[line])
            if line in self.__pool_domain:
                self.__pool_domain[name].update(self.__pool_domain[line])
        # optimize domain
        self.__pool_domain[name] = self.__domain_minify(self.__pool_domain[name])
        # do exclude
        excl_dn = set()
        for line in excl_ls:
            # diff
            for ls in self.__pool:
                if name in ls:
                    ls[name].difference_update(ls[line])
            # store domain diff
            if line in self.__pool_domain:
                excl_dn.update(self.__pool_domain[line])
        # calc domain diff
        if len(excl_dn) > 0:
            self.__pool_domain[name] = self.__domain_diff(
                self.__pool_domain[name], excl_dn
            )

    def __domain_minify(self, mess: set) -> set:
        """minify domain set by combining suffix"""
        res = set()
        # loop from root level domain
        for i in range(1, MAX_DOMAIN_LEVEL):
            # add current level suffix
            suffix = set(x for x in mess if x[0] == "." and x.count(".") == i)
            res.update(suffix)
            # remove children
            mess = set(
                x for x in mess if ("." + ".".join(x.split(".")[-i:])) not in suffix
            )
        res.update(mess)
        return res

    def __domain_diff(self, mess: set, rm: set) -> set:
        """cal domain set mess - rm"""
        for i in range(1, MAX_DOMAIN_LEVEL):
            # remove parent
            mess.difference_update(
                set("." + ".".join(x.split(".")[-i:]) for x in rm if x.count(".") >= i)
            )
            # remove children
            suffix = set(x[1:] for x in rm if x[0] == "." and x.count(".") == i)
            mess = set(x for x in mess if ".".join(x.split(".")[-i:]) not in suffix)
        return mess
