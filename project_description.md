# Projekt - 2024/2025 NBA Awards prediction

## Cel projektu
National Basketball Association (NBA) - amerykańsko-kanadyjska liga koszykarska, o charakterze profesjonalnym. Tworzy ją 30 zespołów, w tym: 29 ze Stanów Zjednoczonych i jeden z Kanady. [...] NBA jest jedną z pięciu największych północnoamerykańskich zawodowych lig sportowych (oprócz niej NFL, NHL, MLS i MLB). Gracze NBA są najlepiej opłacanymi sportowcami świata (w średniej rocznych zarobków). [wiki](https://pl.wikipedia.org/wiki/National_Basketball_Association).

W trakcie sezonu zasadniczego zespoły rozgrywają 82 spotkania. W każdym z nich zbierane są bardzo szczegółowe statystyki dotyczące przbiegu gry a także występów poszczególnych zawodników. Celem projektu jest wykorzystanie ich do predykcji listy zawodników, którzy otrzyjmą nagrody za sezon zasadniczy. Lista nagród - [wiki](https://en.wikipedia.org/wiki/List_of_NBA_awards). W ramach zadania należy wytypować zawodników nominowanych do All-NBA Team (trzy piątki) oraz All-Rookie Team (dwie piątki).


## Dane wejściowe

Dane, na podstawie których powinna zostać przeprowadzona predykcja nie są ograniczone, tj. możliwe jest wykorzystanie wszystkich dostępnych danych dotyczących statystyk z poprzednich sezonów NBA, głosowań na poszczególne nagrody, a także statystyk dotyczących sezonu zasadniczego 2024/2025. Zakazane jest dodawania arbitralnych wag czy cech, które mogłby wpłynąć na model - nie ma zezwolenia na "ręczny" wybór zawodników, ma zrobić to model, a nie Państwa wiedza ekspercka.

Przykładowy klient API www.nba.com w Pythonie do pobierania statystyk:

https://github.com/swar/nba_api

Przydatne informacje dotyczące zaawansowanych statystyk:

https://github.com/JovaniPink/awesome-nba-data?tab=readme-ov-file#advanced-stats-explained

Gotowy zbiór danych (ostatnia aktualizacja 2023-07-06, konieczna ręczna aktualizacja):

https://www.kaggle.com/datasets/wyattowalsh/basketball
https://github.com/wyattowalsh/nbadb

Przykład pobierania (web scraping) danych z basektball-reference.com (na stronie występują limity zapytań, więc proszę pobierać dane, które nie są dostepne w innych lokalizacjach):

https://github.com/JK-Future-GitHub/NBA_Champion/blob/main/nba_html_crawler.ipynb








## Dane Wyjściowe

1) Lista zawodników przypisanych do:

* first all-nba team (5 zawodników)
* second all-nba team (5 zawodników)
* third all-nba team (5 zawodników)
* first rookie all-nba team (5 zawodników)
* second rookie all-nba team (5 zawodników)

W postaci pliku nazwisko_imie.json o formacie:

```
{
  "first all-nba team": [
    "LeBron James",
    "Chris Paul",
    "Mike Conley",
    "Kevin Durant",
    "Stephen Curry"
  ],
  "second all-nba team": [
    "Brook Lopez",
    "Russell Westbrook",
    "James Harden",
    "DeMar DeRozan",
    "Nikola Vucevic"
  ],
  "third all-nba team": [
    "Klay Thompson",
    "Draymond Green",
    "Harrison Barnes",
    "Tobias Harris",
    "Tim Hardaway Jr."
  ],
  "first rookie all-nba team": [
    "Jared McCain",
    "Stephon Castle",
    "Alex Sarr",
    "Zaccharie Risacher",
    "Jaylen Wells"
  ],
  "second rookie all-nba team": [
    "Brandin Podziemski",
    "Justin Edwards",
    "Bub Carrington",
    "Zach Edey",
    "Kel'el Ware"
  ]
}
```

Zagadka - jaki klucz zastosowano, aby dobrać zawodników do first, second, third all-nba team?


2) Opis projektu wraz z kodem

Kod projektów będzie analizowany, jednak opis rozwiązania (użyte metody, jakie cechy, co w preprocessing) również jest wymagany.

Przesłać należy zarówno sam kod dokonujący predykcji (wraz z zapisanym modelem) jak i kod umożliwiający wytrenowanie modelu.




**Uwaga** - bardzo pradopodobne, że wyniki faktycznego głosowania będą znane przed oceną projektu.

## Zbiór danych

W ramach projektu mogą i sugerowane jest korzystanie z jak największego zbioru danych. Wspomniany projekt z API jest sugestią od czego można zacząć. Utworzenie finalnego zbioru leży po Państwa stronie. Możliwe jest współpracowanie całej grupy czy rocznika przy tworzeniu tego zbioru. Używanie tych samych danych uczących **nie będzie traktowane** jako plagiat.

## Termin i miejsce

Termin zaliczenia projektu:

XX.06.2025 10:00

W tygodniach poprzedzających będzie możliwość nadsyłania programów w celu ich przetestowania.

## Wymagania

* Programy należy napisać w języku Python w wersji 3.12.
* Możliwe jest stosowanie zewnętrznych bibliotek.
* Występuję zakaz stosowania głębokich sieci neuronowych, aby moc obliczeniowa nie była decydującym kryterium.
* Należy zweryfikować działanie projektu najpierw na swoim komputerze, a następnie, przesłać go w podanym terminie testu.
* Programy będą oceniane na tej samej maszynie, na której realizowane były testy.
* Komputer do oceny wyposażony jest w 12 rdzeniowy procesor i kartę graficzną NVIDIA z 11GB pamięci RAM. Komputer ma dostęp do internetu.
* Proszę mieć na uwadze, że Państwa program zostanie wykonany tylko jeden raz. W związku z tym jeśli program wykorzystuje wartości losowe zaliczony zostanie jeden wynik (bez sprawdzania, czy jest to najlepszy lub najgorszy możliwy do uzyskania).
* Nieoddanie projektu w terminie oznacza ocenę niedostateczną z przedmiotu.
* Oddanie plagiatu oznacza ocenę niedostateczną bez możliwości poprawy oraz zgłoszenie do komisji dyscyplinarnej.

## Struktura przekazywanego rozwiązania

W ramach rozwiązania należy przesłać archiwum zawierające:

- Nazwiko_Imie.json zawierające Państwa predykcje
- kod źródłowy do przygotowania danych, trenowania modelu oraz wykonania predykcji,
- dodatkowe dane wykorzystywane na którymś z etapów,
- opis rozwiazania,
- inne niezbędne pliki umożliwiające uruchomienie programu.

Programy do predykcji powinny obsługiwać jeden parametr przekazanym w linii poleceń: bezwzględną ścieżką do nieistniejącego pliku wyjściowego (podawaną jako np. `/home/WZUM_projec/Nazwisko_Imie.json`).

## Sposób obliczania wyniku końcowego

Ocena końcowa z przedmiotu będzie średnią z dwóch składowych:

- wyniku predykcji
- oceny rozwiązania (na bazie opisu i kodu)

Obie składowe zostaną uwzględnione w stosunku 1:1, ocena rozwiązania będzie w przedziale 0-100, a wynik predykcji zostanie do takiej skali znormalizowany (na podstawie najwyższego uzyskanego wyniku).

**Składowa 1 - predykcja**

Do oceny modelu zostanie wykorzystana prosta metryka przyznająca punkty w następujący sposób:

Zawodnika w prawidłowej piątce: 10 punktów
Zawodnik jedną piątkę poniżej lub powyżej: 8 punktów
Zawdonik dwie piątki poniżej lub powyżej: 6 punktów

Dodatkowo występuje bonus za każdy kolejny poprawny wybór do piątki o wartości:
2 zawodników - +5
3 zawodników - +10
4 zawodników - +20
5 zawodników - +40

Przykładowy wynik:

```
{
  "first all-nba team": [
    "LeBron James",  # nominowany zawodnik, właściwa piątka +10
    "Chris Paul",  # nominowany zawodnik, druga piątka +8
    "Al Horford",  # nominowany zawodnik, trzecia piątka +6
    "Jeff Green",  # nominowany zawodnik, właściwa piątka +10, drugie poprawnie nominowany do tej piątki, bonus +5
    "Kyle Lowry"   # zawodnik nie był nominowany +0
  ],
  ...
}
```
Za first team all-nba uzyskano 37 punktów.

Państwa nominacje zostaną ocenione dwukrotnie - raz przeciwko oficjalnym wynikom ogłoszonym przez NBA, drugi przeciwko wyborom prowadzącego.

Maksymalna liczba punktów:

(first all-nba) 10+10+10+10+10 + 40 = 90

(second all-nba) 10+10+10+10+10 + 40 = 90

(third all-nba) 10+10+10+10+10 + 40 = 90

(first rookie all-nba) 10+10+10+10+10 + 40 = 90

(second rookie all-nba) 10+10+10+10+10 + 40 = 90

Sumując punkty za wyniki oficjalne i prowadzącego daje razem 900 punktów do zdobycia.

**Składowa 2 - opis rozwiązania**

Liczba punktów w przedziale 0-100 przydzielona na podstawie analizy przesłanego opisu oraz kodu.

## FAQ


## Historia zmian

2025.04.09 - pierwsza wersja


