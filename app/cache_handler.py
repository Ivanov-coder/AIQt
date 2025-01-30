import json


class CacheHandler:
    r"""
    The base class for handling chat logs etc.
    """

    def __init__(
        self,
        *,
        filename: str,
        ID: str,
        content: str,
        role: str = "user",
        isRolePlay: bool = False,
        image: str | bytes = None,
    ) -> None:
        self.filename = filename
        self.ID = ID
        self.content = content
        self.role = role
        self.isRolePlay = isRolePlay
        self.image = image


class CacheReader(CacheHandler):
    r"""
    The class is for reading the chatlog.
    """

    def load_data(self) -> dict:
        r"""
        Load chatlog
        """
        with open(self.filename, "r", encoding="utf-8") as jf:
            contents = json.load(jf)

        return contents


class CacheWriter(CacheHandler):
    r"""
    The class is for writing the chatlog as well as wave files.
    """

    def __init__(self):
        pass

    def write_cache(self) -> None:
        r"""
        Writing chatlogs in the cache file
        """

        cache = self._load_data(self.filename, self.ID)
        # cache = []
        log = {  # Ensure that log is list
            "role": self.role,
            "content": self.content,
        }

        # Append prompt and ensure no repetitions
        if self.isRolePlay and len(cache) == 0:
            cache.append(
                {
                    "role": "system",
                    "content": self.PERSONA
                    + f"Though you can speak other languages, you always speak {self.LANG}",  # 这一部分用于加上人格及设置语言
                },
            )
        cache.append(log)
        # print(cache)
        with open(self.filename, "w", encoding="utf-8") as jf:
            json.dump(cache, jf, indent=4, ensure_ascii=False)

def handle_cache():
    