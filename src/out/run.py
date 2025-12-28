from ..env import PATH_OUT, REMOTE_URL
from .html import write_index


def run() -> None:
    # add index.html
    write_index(PATH_OUT, REMOTE_URL)
    # add null
    with open(PATH_OUT / "null", "tw", encoding="utf-8") as file:
        file.write("\n")
