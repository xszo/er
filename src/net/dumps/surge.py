res = {}
__src = {}
__var = {"map-node": {"direct": "DIRECT", "reject": "REJECT"}, "proxy-link": []}


def let(lsrc: dict) -> None:
    global __src
    __src = lsrc
    for item in __src["node"]:
        if "id" in item:
            __var["map-node"][item["id"]] = item["name"]
    for item in __src["proxy"]["link"]:
        __var["proxy-link"].append(item["tag"])


def profile(out, loc: dict) -> None:
    out.writelines(
        [
            "[General]\n",
            "#!include " + loc["base"] + "\n",
            "\n[Proxy]\n",
            "#!include proxy.conf\n",
            "\n[Proxy Group]\n",
            "#!include " + loc["base"] + "\n",
            "\n[Rule]\n",
            "#!include " + loc["base"] + "\n",
        ]
    )


def base(out, loc: dict) -> None:
    global res
    res = [
        "#!MANAGED-CONFIG "
        + loc["up"]
        + " interval="
        + str(__src["misc"]["interval"])
        + " strict=false",
        "\n",
        #
        "[General]",
        "loglevel = warning",
        "wifi-assist = true",
        "internet-test-url = " + __src["misc"]["test"],
        "proxy-test-url = " + __src["misc"]["test"],
        "proxy-test-udp = " + __src["misc"]["t-dns"],
    ]

    if "dns" in __src["misc"]:
        res.append("hijack-dns = *:53")
        res.append("dns-server = " + ", ".join(__src["misc"]["dns"]))
    line = "encrypted-dns-server = "
    if "doh" in __src["misc"]:
        line += ", ".join(__src["misc"]["doh"])
    if "dot" in __src["misc"]:
        line += ", ".join(__src["misc"]["dot"])
    if len(line) > 24:
        res.append(line)

    res.append("\n[Proxy Group]")

    def conv_n(item: dict) -> str:
        line = item["name"]
        if item["type"] == "static":
            line += " = select"
        elif item["type"] == "test":
            line += ' = smart, policy-priority="\\[2\\]:2;\\[4\\]:4;\\[8\\]:8;"'
        else:
            return None
        if "list" in item:
            for val in item["list"]:
                if val[0] == "-":
                    line += ", " + __var["map-node"][val[1:]]
                else:
                    line += ", " + val
        if "regx" in item:
            line += (
                ', include-all-proxies=true, policy-regex-filter="' + item["regx"] + '"'
            )
        return line

    res.extend([conv_n(item) for item in __src["node"]])

    res.append("\n[Rule]")

    res.extend(
        [
            "RULE-SET, "
            + item[2]
            + ", "
            + __var["map-node"][item[3]]
            + ", no-resolve, extended-matching"
            for item in __src["filter"]["dn"]["surge"]
            if item[0] in set([1, 2])
        ]
    )

    res.extend(
        [
            "RULE-SET, " + item[2] + ", " + __var["map-node"][item[3]]
            for item in __src["filter"]["ip"]["surge"]
            if item[0] == 1
        ]
    )

    res.append("FINAL, " + __var["map-node"][__src["filter"]["main"]] + ", dns-failed")

    out.writelines([x + "\n" for x in res])


def proxy(out) -> None:
    global res
    res = [
        "[General]\n",
        "\n",
        "[Rule]\n",
        "FINAL, DIRECT\n",
        "\n",
        "[Proxy]\n",
        "DIRECT = direct\n",
        "\n",
        "[Proxy Group]\n",
        'Proxy = select, include-all-proxies=true, include-other-group="'
        + ", ".join(__var["proxy-link"])
        + '"\n',
    ]
    res.extend(
        [
            item["tag"]
            + " = select, external-policy-name-prefix="
            + item["tag"]
            + '__, policy-path="'
            + item["uri"]
            + '"\n'
            for item in __src["proxy"]["link"]
        ]
    )

    out.writelines(res)
