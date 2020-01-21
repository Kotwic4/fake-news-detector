# fake-news-detector

## installation

```
pip install -r requirements.txt
```

## Baza danych
1. Wystartuj instancje bazy danych PostgreSQL. W zależności od potrzeb może ona być uruchomiona lokalnie bądź na zdalnym serwerze (w ramach tego projektu była urchamiania instancja bazy danych na AWS).
2. Wykonaj polecenia SQL znajdujące się w pliku table_create.sql . Powinny zostać utworzone 3 tabele - dla artukułów, użytkowników oraz tweetów.
3. Otwórz plik data_extractor.py
4. Ustaw zmienną PATH_TO_DATA_DIRECTORY na folder wskazujący dane z portalu politifact (ścieżka powinna dokładnie wskazywać folder politifact!). Poradnik skąd pobrać dane znajdziesz w innym rozdziale tej instrukcji.
5. Ustaw zmienną CONN zgodnie z informacjami o dostępie do bazy danych na której działasz (ustaw host, dbname, user oraz password)
6. Uruchom skrypt
7. W rezultacie wykonania skryptu dane powinny zostać w odpowiedni sposób wrzucone do bazy danych.

## references

https://github.com/cjhutto/vaderSentiment