# Wyszukiwarka

## Pozyskanie bazy danych
Na początku pobrałem cały [zbiór Wikipedii z dnia 7.04.2023](https://dumps.wikimedia.org/enwiki/20230401/) w formacie `XML`. Wyłuskałem wszyskie artykuły, które zawierały słowo kluczowe _chess_, po czym przeszedłem do analizy i konwertowania danych.

## Konwertowanie danych
Dane zostały skonwertowane i zapisane w plikach `JSON` według podpunktów 2 - 8, niekoniecznie program to robi zgodnie z kolejnością występującą w treści zestawu.

## Wykorzystany stos
Aplikację chciałem napisać wykorzystując `React`a i `Django`, korzystając z mechanizmu cache'owania danych w pamięci podręcznej.