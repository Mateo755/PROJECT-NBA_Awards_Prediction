# 🏀 NBA Awards Prediction Project

## Cel projektu
National Basketball Association (NBA) - amerykańsko-kanadyjska liga koszykarska, o charakterze profesjonalnym. Tworzy ją 30 zespołów, w tym: 29 ze Stanów Zjednoczonych i jeden z Kanady. [...] NBA jest jedną z pięciu największych północnoamerykańskich zawodowych lig sportowych (oprócz niej NFL, NHL, MLS i MLB). Gracze NBA są najlepiej opłacanymi sportowcami świata (w średniej rocznych zarobków). [wiki](https://pl.wikipedia.org/wiki/National_Basketball_Association).

W trakcie sezonu zasadniczego zespoły rozgrywają 82 spotkania. W każdym z nich zbierane są bardzo szczegółowe statystyki dotyczące przbiegu gry a także występów poszczególnych zawodników. Celem projektu jest wykorzystanie ich do predykcji listy zawodników, którzy otrzyjmą nagrody za sezon zasadniczy. Lista nagród - [wiki](https://en.wikipedia.org/wiki/List_of_NBA_awards). W ramach zadania należy wytypować zawodników nominowanych do All-NBA Team (trzy piątki) oraz All-Rookie Team (dwie piątki).


## 📁 Struktura projektu

```
.
├── data_aggregation/               # Skrypty do budowy bazy danych z webscrapingu
├── databases/                      # Utworzone bazy danych 
├── debug/                          # Pliki do debugowania webscrappingu
├── features_info/                  # Analizy cech: F-score, mutual info
├── gt_results/                     # Prawdziwe wyniki predykcyjne dla sezonów (ground truth)
├── raport/                         # Raporty opisowe z procesu tworzenia algorytmu predykcyjnego 
├── project_description.md          # Wymagania projektowe
├── results/                        # Uzyskane wyniki predykcji
├── saved_models/                   # Zapisane finalne modele/klasyfikatory
├── separated_models_testing/       # Testy modeli klasyfikujących osobno All-NBA i All-Rookie
├── testing_data_sources/           # Pierwsze testy pozyskiwania danych                   
├── evaluate_model_results.py       # Plik weryfikujący uzyskane wyniki z klasyfikatorów
├── calc_score.py                   # Plik dostarczony do weryfikacji klasyfikatorów
├── feature_engineering.ipynb       # Inżynieria cech (PCA, Correlation, Feature Importance)
├── models_creation.ipynb           # Tworzenie klasyfikatorów
├── models_combining.ipynb          # Rozbudowa modeli - stacking, voting, ensemble models
├── final_nba_clf_training.py       # Plik do trenowania finalnego modelu
├── final_nba_clf_prediction.py     # Predykcja końcowa
├── requirements.txt                # Używane biblioteki podczas projektu
```

## Setup środowiska (Python 3.12)

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/Mateo755/PROJECT-NBA_Awards_Prediction
cd PROJECT-NBA_Awards_Prediction
```

### 2. Utworzenie środowiska wirtualnego

```bash
python3.12 -m venv .venv
source .venv/bin/activate   # (Linux/macOS)
.venv\Scripts\activate    # (Windows)
```

### 3. Instalacja zależności

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. (Opcjonalnie) Uruchomienie panelu MLflow

Jeśli chcesz śledzić eksperymenty:

```bash
# 1 metoda
mlflow ui 
# 2 metoda
mlflow server --host 127.0.0.1 --port 8080
```

## Uruchamianie skryptów

Trenowanie modelu:
```bash
python final_nba_clf_training.py
```

Finalna predykcja:
```bash
python final_nba_clf_prediction.py  <path_arg>
```

Ewaluacja wyników:
```bash
python evaluate_model_results.py
```
Ewaluacja wyników (2 możliwe pliki ground truth do podania):
```bash
python calc_score.py <results_dir> <ground_truth> <ground_truth> <output_path_filename>

# Przykład:
python calc_score.py ./results/ ./gt_results/real_results_season2025.json ./gt_results/real_results_season2025.json calc_score_output.csv
```

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


## Dokumentacja projektu

Szczegółowe informacje dotyczące działania projektu znajdują się w poniższych raportach:

- 📄 [`dataset_preparation_info.md`](raport/dataset_preparation_info.md)  
  → Szczegółowy opis procesu budowy zbioru danych na podstawie webscrapingu, przetwarzania statystyk zawodników i drużyn oraz tworzenia etykiet.

- 📄 [`models_testing_info.md`](raport/models_testing_info.md)  
  → Podsumowanie wyników testowania różnych architektur modelowych, w tym stacking, voting, oraz wpływu zakresu danych i metod balansowania klas.

- 📄 [`feature_engineering_info.md`](raport/feature_engineering_info.md)  
  → Dokumentacja dotycząca selekcji cech, redukcji wymiarowości (PCA), analizy korelacji i zastosowania metod takich jak Mutual Information czy Boruta.

Każdy raport zawiera dane przykładowe, wyniki testów oraz uzasadnienie wyboru ostatecznego modelu predykcyjnego.

📁 Raporty pomocnicze znajdują się w katalogu `raport/` (opis datasetu, porównania modeli, inżynierii cech).