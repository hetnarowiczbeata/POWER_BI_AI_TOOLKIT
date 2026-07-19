# Power BI DAX Agent

Lokalny agent CLI do pracy z miarami DAX w modelach Power BI zapisanych jako PBIP/TMDL.

Projekt czyta strukturę modelu semantycznego z plików `.tmdl`, analizuje istniejące miary, wykrywa zależności między miarami i pomaga przygotowywać nowe miary DAX. Obecny tryb działania jest **DAX-only**: agent skupia się na miarach, formułach DAX i użyciu miar w raporcie.

## Co Potrafi

- wypisać istniejące miary DAX w modelu,
- sprawdzić, które miary są używane w innych miarach,
- sprawdzić jawne użycia miar w plikach raportu `.Report/definition/*.json`,
- wskazać miary bez jawnego użycia,
- zaproponować nowe miary DAX,
- przygotować kontrolowane zmiany TMDL dla nowych lub aktualizowanych miar,
- dodać zależne miary automatycznie, jeżeli wybrana miara odwołuje się do innej brakującej propozycji.

## Czego Teraz Nie Robi

Agent nie jest już ogólnym narzędziem do przebudowy całego modelu Power BI.

Nie traktuje jako głównego zadania:

- Python 3.10 lub nowszy
- Power BI Desktop z modelem zapisanym jako PBIP/TMDL
- LM Studio z wlaczonym lokalnym serwerem OpenAI-compatible API
- model LLM, np. `qwen2.5-coder-14b-instruct`

Instalacja zaleznosci:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install openai python-dotenv
```

Konfiguracja lokalna znajduje sie w ignorowanym przez Git pliku `services/config.py`.

Przykladowa zawartosc:

```python
from dotenv import load_dotenv

load_dotenv()

Uruchomienie:

```powershell
.\run_agent.bat
```

albo:

```powershell
.\.venv\Scripts\activate
python main.py
```

W konsoli wpisz pytanie, np.:

```text
Jakie miary DAX warto dodac do tego modelu?
```

Po analizie agent pokaze liste proponowanych zmian. Mozesz wpisac numery, np. `1,3`, `wszystkie` albo `nie`. Obecnie automatycznie obslugiwane sa: dodanie miary, dodanie relacji, ukrycie kolumny i dodanie opisu tabeli.

Aby zakonczyc prace, wpisz:

```text
exit
```

## Dokumentacja

Pelny opis projektu, architektury, konfiguracji i przykladowego modelu znajduje sie w pliku:

- [docs/DOKUMENTACJA.md](docs/DOKUMENTACJA.md)

## Struktura repozytorium

```text
.
|-- main.py
|-- run_agent.bat
|-- services/
|   |-- agent.py
|   |-- tmdl_editor.py
|   |-- llm_client.py
|   |-- tmdlreader.py
|   `-- config.py          # lokalny, ignorowany przez Git
|-- sample-model/
|   `-- Amazon Delivery-pr.SemanticModel/
|       `-- definition/
|           |-- model.tmdl
|           |-- relationships.tmdl
|           `-- tables/
`-- docs/
    `-- DOKUMENTACJA.md
```



Wynik końcowy:


Uruchamianie Power BI AI Agent...

Power BI DAX Agent
Wpisz 'exit' zeby zakonczyc

Ja: jakie miary time intelligence mozna stworzyc

Etap 1: sprawdzam miary i kontekst DAX...

PLAN AGENTA
Analizuje istniejace miary i kontekst dat, zeby zaproponowac miary time intelligence w DAX.

DLACZEGO TE PLIKI
Pliki wybrane lokalnie na podstawie typu pytania, nazw tabel i struktury modelu. LLM zostanie uzyty dopiero do analizy.

WYBRANE PLIKI
- relationships.tmdl
- tables\dim_calendar.tmdl
- tables\fct_data.tmdl
- tables\Miary.tmdl

Etap 2: analizuje DAX...
Laczenie z lokalnym modelem LLM...
Odpowiedz odebrana.

ANALIZA AGENTA
1. Orders PY
Powod: Porównanie zamówień z tym samym okresem w poprzednim roku (Year-over-Year) w celu oceny długoterminowego wzrostu.
DAX: CALCULATE([Orders], SAMEPERIODLASTYEAR('dim_calendar'[Date]))

2. Orders YTD
Powod: Obliczenie skumulowanej liczby zamówień od początku roku do bieżącej daty (Year-to-Date).
DAX: TOTALYTD([Orders], 'dim_calendar'[Date])

3. Orders MTD
Powod: Obliczenie liczby zamówień od początku bieżącego miesiąca (Month-to-Date).
DAX: TOTALMTD([Orders], 'dim_calendar'[Date])

4. Orders YoY
Powod: Bezpośrednia wartość przyrostu zamówień w porównaniu do poprzedniego roku.
DAX: [Orders] - [Orders PY]

5. Orders YoY %
Powod: Procentowy wzrost zamówień w porównaniu do poprzedniego roku, kluczowy wskaźnik efektywności.
DAX: DIVIDE([Orders YoY], [Orders PY], 0)

6. On-time orders YTD
Powod: Skumulowana liczba zamówień dostarczonych na czas od początku roku, niezbędna do oceny spójności SLA.
DAX: TOTALYTD([On-time orders.], 'dim_calendar'[Date])

7. SLA YTD %
Powod: Skumulowany procent zamówień dostarczonych na czas od początku roku, pokazujący długoterminową jakość usługi.
DAX: DIVIDE([On-time orders YTD], [Orders YTD], 0)

Czy przygotowac zmiany miar DAX do TMDL? Wpisz 'tak', zeby wybrac numery zmian, albo 'nie': tak

Etap 3: przygotowuje zmiany miar DAX do TMDL...

PROPONOWANE ZMIANY DO WYBORU

[1] Dodaj Orders PY
    Typ: measure | Ryzyko: low | Operacja: add_measure
    Liczba zamowien w analogicznym okresie poprzedniego roku. Baza dla YoY.

[2] Dodaj Orders YTD
    Typ: measure | Ryzyko: low | Operacja: add_measure
    Skumulowana liczba zamowien od poczatku roku.

[3] Dodaj Orders MTD
    Typ: measure | Ryzyko: low | Operacja: add_measure
    Skumulowana liczba zamowien od poczatku miesiaca.

[4] Dodaj Orders QTD
    Typ: measure | Ryzyko: low | Operacja: add_measure
    Skumulowana liczba zamowien od poczatku kwartalu.

[5] Dodaj Orders YoY
    Typ: measure | Ryzyko: low | Operacja: add_measure
    Roznica liczby zamowien wzgledem poprzedniego roku.

[6] Dodaj Orders YoY %
    Typ: measure | Ryzyko: low | Operacja: add_measure
    Procentowa zmiana liczby zamowien rok do roku.

[7] Dodaj On-time orders YTD
    Typ: measure | Ryzyko: low | Operacja: add_measure
    Skumulowana liczba terminowych zamowien od poczatku roku.

[8] Dodaj SLA YTD %
    Typ: measure | Ryzyko: low | Operacja: add_measure
    SLA liczony narastajaco od poczatku roku.

Ktore zmiany chcesz zaimplementowac? Wpisz numery, np. 1,3, 'wszystkie' albo 'nie': 1,2,3

WYBRANE ZMIANY DO IMPLEMENTACJI
Numery: 1, 2, 3
- [1] Dodaj Orders PY (add_measure)
- [2] Dodaj Orders YTD (add_measure)
- [3] Dodaj Orders MTD (add_measure)

Czy na pewno zaimplementowac wybrane zmiany w TMDL? Wpisz 'tak' albo 'nie': tak

WYNIK ZAPISU TMDL
[1] zastosowano: Zmieniono plik: tables\Miary.tmdl
[2] zastosowano: Zmieniono plik: tables\Miary.tmdl
[3] zastosowano: Zmieniono plik: tables\Miary.tmdl