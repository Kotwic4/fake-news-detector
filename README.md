# fake-news-detector

Combating fake news and detecting false informations is extremely crucial, because of huge
manipulation possibilities. It should not be surprising then that this area is the subject of
research for many scientists.

Goal of this project was to invent a binary classificator, which task was to indicate if
information is false or not. Fake news can be detected based on article content or its social
context. In this project we have focused on prediction from news content. Our solution was
based on context word embeddings from one of the best language model currently available - Flair.

Presented mechanism was evaluated on a dataset called FakeNewsNet, and the result was
compared to many other results.FakeNewsNet contains set of real and fake news from
politic and gossip area, however during this project we focused only on political news from
PolitiFact.

Project created by Radomir Krawczykiewicz and Grzegorz Wątor

## Results

We have achived very good results on PolitiFact from FakeNewsNet:

| Model          | Accuracy | Precision | Recall | F1    |
| -------------- |:--------:|:---------:|:------:| :----:|
| Flair Title    | 0.816    | 0.761     | 0.805  | 0.782 |
| Flair Url      | 0.804    | 0.733     | 0.860  | 0.791 |
| Flair Mix      | 0.759    | 0.648     | 0.908  | 0.756 |
| AutoKeras Mix  | 0.863    | 0.811     | 0.918  | 0.861 |



## Documentation

One can get more information from a short [presentation](Presentation.pdf)(in english) or full [documenation](Dokumentacja.pdf)(in polish)

## Installation

One needs to have installed Python on one's computer, then one can just install dependencies using pip:

```
pip install -r requirements.txt
```

## Starting 

```
jupyter notebook
```

## Dataset

We have used [FakeNewsNet](https://github.com/KaiDMML/FakeNewsNet) as our dataset.

To evalute on dataset one needs to download it firsts.

For full data one needs to use [script]https://github.com/KaiDMML/FakeNewsNet/blob/master/code/main.py) provided by FakeNewsNet.

If one wants to use just CSV data one download them from github, seperate for [fake](https://github.com/KaiDMML/FakeNewsNet/blob/master/dataset/politifact_fake.csv) and [real](https://github.com/KaiDMML/FakeNewsNet/blob/master/dataset/politifact_real.csv)


Colab notebook have cell, which is downloading CSV file from github.

## Baza danych
1. Wystartuj instancje bazy danych PostgreSQL. W zależności od potrzeb może ona być uruchomiona lokalnie bądź na zdalnym serwerze (w ramach tego projektu była urchamiania instancja bazy danych na AWS).
2. Wykonaj polecenia SQL znajdujące się w pliku table_create.sql . Powinny zostać utworzone 3 tabele - dla artukułów, użytkowników oraz tweetów.
3. Otwórz plik data_extractor.py
4. Ustaw zmienną PATH_TO_DATA_DIRECTORY na folder wskazujący dane z portalu politifact (ścieżka powinna dokładnie wskazywać folder politifact!). Poradnik skąd pobrać dane znajdziesz w innym rozdziale tej instrukcji.
5. Ustaw zmienną CONN zgodnie z informacjami o dostępie do bazy danych na której działasz (ustaw host, dbname, user oraz password)
6. Uruchom skrypt
7. W rezultacie wykonania skryptu dane powinny zostać w odpowiedni sposób wrzucone do bazy danych.

## References

### Papers
* [Fake News Detection on Social Media: A Data Mining Perspective](https://www.kdd.org/exploration_files/19-1-Article2.pdf)
* [FakeNewsNet: A Data Repository with News Content, Social Context and Spatiotemporal Information for Studying Fake News on Social Media](https://arxiv.org/pdf/1809.01286.pdf)

### Libraries
* [FakeNewsNet](https://github.com/KaiDMML/FakeNewsNet)
* [flair](https://github.com/flairNLP/flair)
* [autokeras](https://github.com/keras-team/autokeras)
* [vaderSentiment](https://github.com/cjhutto/vaderSentiment)
