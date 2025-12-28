from pathlib import Path


def write_index(dire: Path, link: str) -> str:
    """generate index.html for dire"""
    html = ""
    # iterate through dir for link tree
    for file in sorted(dire.iterdir(), key=lambda x: x.name):
        fname = file.name
        # skip hidden files
        if fname[0] == "." or fname == "index.html":
            continue
        # add file link
        if file.is_file():
            html += "<li>" '<a href="' + link + fname + '">' + fname + "</a>" "</li>"
        # add dir links
        if file.is_dir():
            html += (
                "<li>"
                '<a href="' + link + fname + '">' + fname + "/"
                "</a>"
                "<ul>" + write_index(file, link + fname + "/") + "</ul>"
                "</li>"
            )
    # write index
    with open(dire / "index.html", "tw", encoding="utf-8") as out:
        out.write(
            "<!DOCTYPE html>"
            '<html lang="en">'
            "<head>"
            '<meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            "<title>Index</title>"
            "</head>"
            "<body>"
            "<h2>Index</h2>"
            "<ul>" + html + "</ul>"
            "</body>"
            "</html>"
        )
    return html
