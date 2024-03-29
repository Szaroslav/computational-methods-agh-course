from io import TextIOWrapper
from functools import reduce
import re

class WikiParser:
    ARTICLE_NAME = "page"
    CONTENT_NAME = "text"
    OPENING_ARTICLE_TAG, CLOSING_ARTICLE_TAG = f"<{ARTICLE_NAME}", f"</{ARTICLE_NAME}>"
    OPENING_CONTENT_TAG, CLOSING_CONTENT_TAG = f"<{CONTENT_NAME}", f"</{CONTENT_NAME}>"

    def __init__(self, file: TextIOWrapper):
        self._file = file
        self._read_mode = False
        self.i = 0

    def parse_line(self) -> list[str] | None:
        line = self._file.readline()
        if line == '':
            self._file.close()
            return None

        opening_idx: int = line.find(WikiParser.OPENING_CONTENT_TAG)
        closing_idx: int = line.find(WikiParser.CLOSING_CONTENT_TAG)

        words = []

        if opening_idx >= 0 or self._read_mode:
            self._read_mode = True

            # if opening_idx < 0 and closing_idx < 0:
            i, j = 0, len(line)
            if opening_idx >= 0:
                i = opening_idx
            if closing_idx >= 0:
                j = closing_idx + len(WikiParser.CLOSING_ARTICLE_TAG)
            substr = line[i:j]

            
            words = substr \
                    .replace(", ", " ") \
                    .replace(". ", " ") \
                    .replace("|", " ") \
                    .replace("{{clear}}", "") \
                    .replace("[[", "") \
                    .replace("]]", "") \
                    .replace("{{", "") \
                    .replace("}}", "") \
                    .replace("'''", "") \
                    .replace("==", "") \
                    .replace("===", "") \
                    .lower() \
                    .split()
            # words += list(filter(lambda x: x.isalnum() and not x.isdigit(), ws))

        if closing_idx >= 0:
            self._read_mode = False

        if len(words) > 1 or len(words) == 1 and not words[0]:
            return words
        return []

    def parse_document(self) -> tuple[str, str] | tuple[None, None]:
        doc = self.get_document()

        if doc is None:
            return None, None
        
        opening_idx: int = doc.find(WikiParser.OPENING_CONTENT_TAG)
        closing_idx: int = doc.find(WikiParser.CLOSING_CONTENT_TAG)
        i, j = doc.find(">", opening_idx) + 1, closing_idx + len(WikiParser.CLOSING_CONTENT_TAG)
        
        return doc[i:j], doc

    def get_document(self) -> str | None:
        doc = ""

        while True:
            line = self._file.readline()
            if line == '':
                self._file.close()
                return None
            
            opening_idx: int = line.find(WikiParser.OPENING_ARTICLE_TAG)
            closing_idx: int = line.find(WikiParser.CLOSING_ARTICLE_TAG)

            i, j = 0, len(line)
            if self._read_mode and closing_idx >= 0:
                j = closing_idx + len(WikiParser.CLOSING_ARTICLE_TAG)
            elif opening_idx >= 0:
                self._read_mode = True
                if closing_idx >= 0:
                    j = closing_idx + len(WikiParser.CLOSING_ARTICLE_TAG)
            
            substr = line[i:j]
            doc += substr

            if closing_idx >= 0:
                self._read_mode = False
                self._file.seek(self._file.tell() - len(line) + closing_idx + len(WikiParser.OPENING_ARTICLE_TAG))
                return doc

        return None

    def count(self):
        res = 0
        for line in self._file:
            if WikiParser.OPENING_ARTICLE_TAG in line:
                res += 1

        return res