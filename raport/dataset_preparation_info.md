# Raport: Proces tworzenia zbioru danych do predykcji nagród NBA (All-NBA / All-Rookie)

## Cel procesu
Celem procesu było przygotowanie kompletnego zbioru danych, który może zostać wykorzystany do wytrenowania modeli klasyfikujących zawodników do zespołów All-NBA oraz All-Rookie na podstawie ich statystyk z sezonu zasadniczego.

## Web scraping jako źródło danych

Wszystkie dane wykorzystywane w projekcie pochodzą z **web scrapingu** serwisu `basketball-reference.com`. Dane są:
- **samodzielnie pobierane** (bez użycia gotowych plików CSV),
- **niezależnie przetwarzane**,
- automatycznie aktualizowane dla każdego wskazanego sezonu.

Dzięki temu zbiór danych jest w pełni **reprodukowany i niezależny od zewnętrznych repozytoriów** (np. Kaggle), co zapewnia aktualność informacji.

## Struktura modułów

Każda część przetwarzana jest w **osobnym module**:

- `creating_datasets.py`: pozyskanie statystyk zawodników, drużyn, nagród za gracza tygodnia i miesiąca oraz uzyskanie cechy dla debiutantów (kto jest rookie)
- `creating_target_data.py`: pozyskanie drużyn All-NBA i All-Rookie i wygenerowanie etykiet "target"
- `multi_team_simple_average.py`: obsługa problemu w przypadku zawodników grających w wielu zespołach
- `creating_df_full.py`: główny moduł odpowiedzialny za proces budowy finalnego zbioru danych

Dzięki temu kod jest modularny i łatwy w utrzymaniu, a poszczególne funkcje można testować i rozwijać niezależnie.


## Główne kroki procesu

Dane są przetwarzane modułowo – każda kategoria danych pochodzi z osobnej funkcji w module `creating_datasets.py`, co ułatwia organizację i testowanie kodu.

### 1. Pobieranie danych źródłowych
Dla każdego sezonu (np. 2020–2024), wykonywane są następujące operacje:

#### a) Statystyki zawodników (`get_players_stats`)
- Funkcja pobiera i łączy `statystyki per-game oraz advanced` dla każdego zawodnika.
- Dane pobierane są z `basketball-reference.com` przy użyciu `get_table_by_id`.
- Dane obejmują:
```python
['Player', 'Age', 'Team', 'Pos', 'G', 'GS', 'MP_avg', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%','ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'MP_total', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']
```

#### Podział na kategorie:

- **Identyfikacja i kontekst:**
  - `Player` – imię i nazwisko zawodnika
  - `Age` – wiek
  - `Team` – zespół
  - `Pos` – pozycja
  - `G`, `GS` – liczba rozegranych i rozpoczętych meczów

- **Statystyki per game:**
  - `MP_avg` – średnia liczba minut
  - `FG`, `FGA`, `FG%` – celne rzuty z gry, próby, skuteczność
  - `3P`, `3PA`, `3P%` – rzuty za 3 punkty, próby, skuteczność
  - `2P`, `2PA`, `2P%` – rzuty za 2 punkty, próby, skuteczność
  - `FT`, `FTA`, `FT%` – rzuty wolne, próby, skuteczność
  - `ORB`, `DRB`, `TRB` – zbiórki ofensywne, defensywne i łączne
  - `AST`, `STL`, `BLK`, `TOV`, `PF`, `PTS` – asysty, przechwyty, bloki, straty, faule, punkty

- **Zaawansowane metryki (advanced stats):**
  - `MP_total` – całkowita liczba minut
  - `PER` – Player Efficiency Rating
  - `TS%` – True Shooting Percentage
  - `3PAr`, `FTr` – udział rzutów za 3 i rzutów wolnych
  - `ORB%`, `DRB%`, `TRB%` – udział w zbiórkach względem dostępnych w meczu
  - `AST%`, `STL%`, `BLK%`, `TOV%` – wskaźniki procentowe - asysty, przechwyty, bloki, straty, faule, punkty

  - `USG%` – Usage Rate (użycie zawodnika)
  - `OWS`, `DWS`, `WS`, `WS/48` – Win Shares ofensywne, defensywne, łączne, na 48 minut
  - `OBPM`, `DBPM`, `BPM` – Box Plus/Minus (ofensywny, defensywny, łączny)
  - `VORP` – Value Over Replacement Player

Te cechy zapewniają szeroki obraz wkładu zawodnika w grę zespołu.

---
#### b) Statystyki drużyn (`get_teams_stats`)
- Pobierane są dane drużynowe z tabeli 'Advanced Team Stats'.
- Czyszczone są kolumny pomocnicze, a nazwy drużyn są standaryzowane (np. Charlotte Hornets = CHO/CHH w zależności od sezonu).
- Dane obejmują:
```python
['Team', 'W', 'L', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'NRtg', 'Pace','FTr', '3PAr', 'TS%', 'Offense Four Factors eFG%','Offense Four Factors TOV%', 'Offense Four Factors ORB%','Offense Four Factors FT/FGA', 'Defense Four Factors eFG%','Defense Four Factors TOV%', 'Defense Four Factors DRB%','Defense Four Factors FT/FGA']
```

#### Opis wybranych cech:

- **Podstawowe dane drużynowe:**
  - `Team` – skrót identyfikujący drużynę (np. BOS, LAL, CHI)
  - `W`, `L` – liczba zwycięstw i porażek
  - `MOV` – Margin of Victory, średnia różnica punktowa
  - `SOS` – Strength of Schedule, trudność terminarza
  - `SRS` – Simple Rating System (MOV + SOS)

- **Zaawansowane metryki:**
  - `ORtg` – Offensive Rating (punkty na 100 posiadań)
  - `DRtg` – Defensive Rating (stracone punkty na 100 posiadań)
  - `NRtg` – Net Rating (różnica ORtg – DRtg)
  - `Pace` – liczba posiadań piłki na 48 minut

- **Efektywność rzutowa i styl gry:**
  - `TS%` – True Shooting Percentage (uwzględnia FG, 3P i FT)
  - `FTr` – Free Throw Rate (FT / FGA)
  - `3PAr` – udział rzutów za 3 wśród wszystkich rzutów

- **Czynniki ofensywne (Offense Four Factors):**
  - `eFG%` – skuteczność rzutów z wagą dla trójek
  - `TOV%` – procent strat
  - `ORB%` – procent zbiórek ofensywnych
  - `FT/FGA` – liczba rzutów wolnych na próbę z gry

- **Czynniki defensywne (Defense Four Factors):**
  - Analogiczne miary, ale liczone dla przeciwnika (np. `Defense Four Factors eFG%` = jak dobrze przeciwnicy rzucają przeciwko tej drużynie)

Te cechy dostarczają tła kontekstowego dla każdego zawodnika — grając w lepszym lub gorzej zorganizowanym zespole, zawodnik może mieć inne warunki do zdobywania nagród.

---
#### c) Nagrody w sezonie (`get_award_counts`)
- Funkcja przeszukuje zakomentowany HTML w celu wyodrębnienia list graczy:
  - Player of the Week (potw)
  - Player of the Month (potm)
  - Rookie of the Month (rotm)
- Zlicza wystąpienia zawodników i przekształca je w cechy numeryczne.

```python
['Player', 'potw_count', 'potm_count', 'rookie_of_month_count']
```
---
#### d) Rookies (`get_rookie_players`)
- Funkcja pobiera listę zawodników debiutujących w danym sezonie.
- Zwraca data frame debiutantów (zawodnicy w swoim pierwszym sezonie).

---

### 2. Obsługa zawodników grających w wielu drużynach

W module `multi_team_simple_average.py` znajduje się funkcja odpowiedzialna za poprawne przypisywanie statystyk zawodnikom, którzy w trakcie sezonu reprezentowali więcej niż jeden zespół (np. oznaczeni jako `2TM`, `3TM` itd. na Basketball Reference).

#### `resolve_multi_team_simple_average(df_players, df_team_stats)`
- Celem funkcji jest uzupełnienie brakujących wartości statystyk zespołowych dla zawodników grających w wielu drużynach.
- Dla takich zawodników:
  - Jeśli znane są zespoły, w których grali — funkcja oblicza **prostą średnią arytmetyczną** z odpowiednich statystyk.
  - Jeśli brak jest szczegółowych danych — używana jest średnia ligowa.


Funkcja zapobiega utracie przypadków wieloklubowych, które mogą być istotne w kontekście nagród. 

---
### 3. Ustalanie etykiet (targetów)

Wszystkie etykiety klasyfikacyjne (czyli cele modelu) odpowiadają przynależności zawodnika do jednej z pięciu drużyn wyróżnionych po sezonie:

- **All-NBA Teams**: pierwsza, druga lub trzecia piątka (target = 1, 2, 3)
- **All-Rookie Teams**: pierwsza lub druga piątka (target = 4, 5)

**Jeżeli gracz nie był wybrany do tych drużyn, to w kolumnie target ma przypisaną wartość 0**. Dane dotyczące tych nagród są przetwarzane w module `creating_target_data.py` za pomocą następujących funkcji:

#### a) `get_all_nba_team`
- Pobiera zawodników wybranych do All-NBA Teams (1st, 2nd, 3rd).
- Przeszukuje zakomentowane sekcje strony `basketball-reference.com`, wyodrębniając dane o nagrodach.

#### b) `get_all_rookie_team`
- Analogicznie pobiera zawodników nominowanych do All-Rookie Teams (1st, 2nd).
- Dane również pochodzą z zakomentowanej części HTML.

#### c) `build_awards_column`
- Funkcja ta **łączy dane z dwóch niezależnych źródeł**:
  - `get_all_nba_team` — dane o graczach nominowanych do All-NBA Teams (1st, 2nd, 3rd),
  - `get_all_rookie_team` — dane o graczach wybranych do All-Rookie Teams (1st, 2nd).

- Funkcja tworzy finalny DataFrame z dwiema kolumnami: `Player` i `target`, który następnie łączony jest z danymi wejściowymi w procesie budowania pełnego zbioru danych. 
- Target dataset został przygotowany pod klasyfikację wieloklasową, tak żeby `jeden model predykcyjny mógł wyznaczyć jednocześnie All-NBA oraz All-Rookie Teams`. To czy takie podejście będzie najbardziej optymalne okaże się w fazie testów.


### 4. Budowa pełnego zbioru danych

Moduł `creating_df_full.py` odpowiada za zebranie wszystkich danych przetwarzanych w poprzednich etapach i złożenie ich w jeden spójny zbiór cech (`X`) oraz etykiet (`y`).

```python
build_full_dataset(last_season: int, n_seasons: int, return_full=False)
```
- Główna funkcja całego procesu przygotowania danych do trenowania modeli.
- Parametry:
  - `last_season`: ostatni sezon do uwzględnienia (np. 2024),
  - `n_seasons`: ile sezonów wstecz uwzględnić (np. 5),
  - `return_full`: jeśli True, zwraca także pełny DataFrame ze wszystkimi kolumnami.
- Dla każdego sezonu wykonuje:
  1. **Pobranie statystyk zawodników** przy pomocy funkcji `creating_datasets.py`.
  2. **Pozyskanie etykiet (targetów)** przy pomocy funkcji z `creating_target_data.py`.
  3. **Scalenie danych**:
     - uzupełnienie braków dla zawodników z wieloma drużynami `multi_team_simple_average.py`,
     - dołączenie danych  o nagrodach i informacji o rookie,
     - połączenie z etykietami,
     - dołączenie roku sezonu.
      ```python
      #=== 3. Merge danych cech ===
      df = resolve_multi_team_simple_average(df_players, df_teams)
      df = df.merge(df_awards_signals, on="Player", how="left")
      df = df.merge(df_rookies[["Player", "is_rookie"]], on="Player", how="left")
      df = df.merge(df_awards_target, on="Player", how="left")
      df["season"] = season
      ```
  4. **Czyszczenie danych** – brakujące wartości w cechach są wypełniane zerami, a dane konwertowane do typów całkowitych.
      ```python
      # === 4. Czyszczenie ===
      df[["potw_count", "potm_count", "rookie_of_month_count", "is_rookie", "target"]] = \
      df[["potw_count", "potm_count", "rookie_of_month_count", "is_rookie", "target"]].fillna(0).astype(int)
      ```

  5. **Tworzenie finalnych macierzy**:
     - `X`: cechy (bez kolumn identyfikacyjnych takich jak `Player`, `Team`, `season`, `target`),
     - `y`: etykiety do klasyfikacji (`target`).

      ```python
      # === 6. Przygotowanie X i y ===
      drop_cols = ["Player", "Team", "Pos", "season", "target"]
      X = df_full.drop(columns=drop_cols, errors="ignore")
      y = df_full["target"]
      ```

      Do procesu trenowania modelu cechy takie jak `Player`, `Team`, `season`, są odrzucane bo klasyfiaktor ma się uczyć na numerycznych statystykach graczy, a nie to jak mają na imię,w jakiej drużynie grali i dodatkwo w którym sezonie. **`Pos` jest odrzucane ponieważ od sezonu 2024 nie jest ta cecha uwzględniana przy wyborze All-NBA**.  
---
Dzięki tej funkcji cały proces jest w pełni automatyczny i powtarzalny, a zaktualizowanie danych do nowego sezonu sprowadza się do zmiany parametru `last_season`.

Opcjonalnie można również uzyskać pełen DataFrame `df_full`, zawierający wszystkie dane (do analizy czy debugowania).

### Przykład wywołania:
```python
X, y = build_full_dataset(last_season=2024, n_seasons=5)
```

## Zastosowanie
Gotowy zbiór może być użyty do trenowania klasyfikatorów np. Random Forest, XGBoost itp., w celu przewidywania przynależności zawodników do nagrodzonych zespołów All-NBA / All-Rookie.



