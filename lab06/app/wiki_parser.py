from io import TextIOWrapper
from functools import reduce

class WikiParser:
    ARTICLE_NAME = "page"
    CONTENT_NAME = "text"
    OPENING_ARTICLE_TAG, CLOSING_ARTICLE_TAG = f"<{ARTICLE_NAME}", f"</{ARTICLE_NAME}>"
    OPENING_CONTENT_TAG, CLOSING_CONTENT_TAG = f"<{CONTENT_NAME}", f"</{CONTENT_NAME}>"

    def __init__(self, file: TextIOWrapper):
        self._file = file
        self._read_mode = False

    def parse_line(self) -> list[str] | None:
        line = self._file.readline()
        if line == '':
            return None

        opening_idx: int = line.find(WikiParser.OPENING_CONTENT_TAG)
        closing_idx: int = line.find(WikiParser.CLOSING_CONTENT_TAG)

        words = []

        if opening_idx >= 0 or self._read_mode:
            self._read_mode = True

            # if opening_idx < 0 and closing_idx < 0:
            i, j = 0, len(line)
            if opening_idx >= 0 and closing_idx >= 0:
                i, j = line.find(">", opening_idx), closing_idx
            elif opening_idx >= 0 and closing_idx < 0:
                i, j = line.find(">", opening_idx), len(line)
            substr = line[i:j]

            
            words = substr.replace(", ", " ").replace(". ", " ").lower().split()
            words = list(filter(lambda x: x.isalnum() and not x.isdigit(), words))

            # for word in words:
            #     word = word \
            #         .replace("[[", "") \
            #         .replace("]]", "") \
            #         .replace("{{", "") \
            #         .replace("}}", "") \
            #         .replace("''", "") \
            #         .replace("'''", "") \
            #         .replace("(", "") \
            #         .replace(")", "") \
            #         .replace(".", "") \
            #         .replace(",", "") \
            #         .lower()

            #     if not word.isalnum():
            #         continue

            #     if word.find("|") >= 0 or word.find(":") >= 0 or word.find("\"") >= 0 or word.find(";") >= 0:
            #         continue

        if closing_idx >= 0:
            self._read_mode = False

        if len(words) > 1 or len(words) == 1 and not words[0]:
            return words
        return []
