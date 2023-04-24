# Wyszukiwarka

## Pozyskanie bazy danych
Na początku pobrałem cały [zbiór Wikipedii z dnia 7.04.2023](https://dumps.wikimedia.org/enwiki/20230401/) w formacie `XML`. Wyłuskałem wszyskie artykuły, które zawierały słowo kluczowe _chess_, po czym przeszedłem do analizy i konwertowania danych.

## Konwertowanie danych
Dane zostały skonwertowane i zapisane w plikach `JSON` według podpunktów 2 - 8, niekoniecznie program to robi zgodnie z kolejnością występującą w treści zestawu.

## Miara prawdopodobieństwa
Zastosowałem 2 zbliżone miary prawdopodobieństwa w zależności od wystąpienia redukcji szumów, używając algorytmu SVD dla macierzy rzadkich.

### Macierz rzadka (brak redukcji)
$$
\cos\theta_j = \frac{\mathbf{q}^T\mathbf{d}_j}{||\mathbf{q}^T||_2||\mathbf{d}_j||_2}
$$

### Redukcja SVD
$$
\cos\phi_j = \frac{\mathbf{q}^T\mathbf{U}_k\mathbf{s}_j}{||\mathbf{q}^T||_2||\mathbf{s}_j||_2}
$$
gdzie $\mathbf{s}_j$ to wektor kolumnowy macierzy $\mathbf{S}_k = \mathbf{D}_k\mathbf{V}_k^T$, $\mathbf{S}_k \in \mathbb{R}^{k \times n}$

Bardziej szczegółowy opis można znaleźć w książce __Matrix Analysis and Applied Linear Algebra__ Carl D. Meyer - rozdział _5.12. Singular Value Decomposition_, przykład 5.12.4.

## Wykorzystany stos
Aplikację chciałem napisać wykorzystując `React`a i `Django`, korzystając z mechanizmu cache'owania danych w pamięci podręcznej.