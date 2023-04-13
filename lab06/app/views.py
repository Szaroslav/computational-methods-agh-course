from django.shortcuts import render
from django.http import HttpResponse
from .wiki_parser import WikiParser

# Create your views here.
def init(request):
    WIKI_FILE_PATH = "/home/szary/Downloads/wiki/"
    CONTENT_TAG_NAME = "text"
    OPENING_TAG, CLOSING_TAG = f"<{CONTENT_TAG_NAME}", f"</{CONTENT_TAG_NAME}>"
    filenames: list[str] = [
        "simplewiki-20230401-pages-articles-multistream.xml",
        # "enwiki-20230401-pages-articles-multistream1.xml-p1p41242",
        # "enwiki-20230401-pages-articles-multistream2.xml-p41243p151573",
        # "enwiki-20230401-pages-articles-multistream3.xml-p151574p311329"
    ]
    count = 0
    bag_of_words = {}

    for filename in filenames:
        with open(f"{WIKI_FILE_PATH}{filename}", "r") as file:
            parser = WikiParser(file)

            while (words := parser.parse_line()) is not None:
                count += 1
                if count == 100000:
                    break
                
                for word in words:
                    if bag_of_words.get(word) is None:
                        bag_of_words[word] = 0
                    bag_of_words[word] += 1
        # with open(f"{WIKI_FILE_PATH}{filename}", "r") as file:
        #     read_mode = False
        #     for i, line in enumerate(file):
        #         if i == 3000000:
        #             break

        #         opening_idx: int = line.find(OPENING_TAG)
        #         closing_idx: int = line.find(CLOSING_TAG)

        #         if opening_idx >= 0 or read_mode:
        #             read_mode = True
        #             if opening_idx < 0 and closing_idx < 0:
        #                 substr = line
        #             elif opening_idx >= 0 and closing_idx >= 0:
        #                 substr = line[opening_idx + len(OPENING_TAG):closing_idx]
        #             elif opening_idx >= 0 and closing_idx < 0:
        #                 substr = line[opening_idx + len(OPENING_TAG):]

        #             words = substr.split()
        #             for word in words:
        #                 word = word \
        #                     .replace("[[", "") \
        #                     .replace("]]", "") \
        #                     .replace("{{", "") \
        #                     .replace("}}", "") \
        #                     .replace("''", "") \
        #                     .replace("'''", "") \
        #                     .replace("(", "") \
        #                     .replace(")", "") \
        #                     .replace(".", "") \
        #                     .replace(",", "") \
        #                     .lower()

        #                 if word.find("|") >= 0 or word.find(":") >= 0 or word.find("\"") >= 0 or word.find(";") >= 0:
        #                     continue
                        
        #                 if bag_of_words.get(word) is None:
        #                     bag_of_words[word] = 0
        #                 bag_of_words[word] += 1

        #         if closing_idx >= 0:
        #             read_mode = False

    return HttpResponse(len(bag_of_words))
