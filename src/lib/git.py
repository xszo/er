from pathlib import Path
from subprocess import run


class repo:
    """git repo"""

    err = False
    __link = ""
    __path = Path()

    def __init__(self, loc: Path, url: str) -> None:
        """clone git repo into loc"""
        self.__path = loc
        self.__link = url
        # if loc is occupied
        if self.__path.exists():
            # loc is empty dir
            if self.__path.is_dir() and not any(self.__path.iterdir()):
                self.clone()
            else:
                # get git remote url
                loc_info = run(
                    ["git", "config", "--get", "remote.origin.url"],
                    cwd=self.__path,
                    check=True,
                    capture_output=True,
                )
                # loc is this repo
                if (
                    loc_info.returncode == 0
                    and loc_info.stdout.decode("utf-8") == self.__link + "\n"
                ):
                    self.pull()
                else:
                    self.err = True
        # if loc is empty
        else:
            self.__path.mkdir(parents=True)
            self.clone()

    def clone(self) -> None:
        """git clone"""
        run(
            ["git", "clone", "--depth=1", self.__link, "."],
            cwd=self.__path,
            check=False,
        )

    def pull(self) -> None:
        """git pull"""
        run(["git", "pull", "--depth=1", "-r"], cwd=self.__path, check=False)
