from django.shortcuts import render
from django.http import HttpResponse
from copy import copy
from mediawiki_dump.tokenizer import tokenize
import math
import numpy as np

import nltk
nltk.download('punkt')


def search(request):
    query = request.GET.get("q", "")
    print(tokenize(query))

    return HttpResponse(query)

def count(request):
    # c = 0
    # with open("/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/db/core/chesswiki.xml", "r") as file:
    #     c = WikiParser(file).count()

    return HttpResponse()