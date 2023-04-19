from django.shortcuts import render
from django.http import HttpResponse
from copy import copy
from mediawiki_dump.tokenizer import tokenize
import math
import numpy as np
from django.core.cache import cache
import db.init

import nltk
nltk.download('punkt')


def search(request):
    query = request.GET.get("q", "")
    k = int(request.GET.get("k", "0"))
    # print(tokenize(query), k)
    if cache.get("sparse_matrix") is None:
        db.init.load()
    print(cache.get("sparse_matrix"))

    return HttpResponse(query)

def count(request):
    # c = 0
    # with open("/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/db/core/chesswiki.xml", "r") as file:
    #     c = WikiParser(file).count()

    return HttpResponse()