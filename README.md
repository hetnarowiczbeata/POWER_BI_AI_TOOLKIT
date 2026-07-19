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

- projektowania relacji,
- ukrywania kolumn,
- opisywania tabel,
- optymalizacji kardynalności,
- zmian strukturalnych poza miarami DAX.

Relacje, kolumny i tabele są używane tylko jako kontekst potrzebny do poprawnych formuł DAX.

## Workflow

```text
Power BI PBIP/TMDL
        |
        v
Odczyt modelu semantycznego
        |
        v
Analiza miar i zależności DAX
        |
        v
Propozycje miar DAX
        |
        v
Wybór użytkownika
        |
        v
Kontrolowany zapis miar do TMDL
```

## Uruchomienie

Najprościej:

```powershell
.\run_agent.bat
```

Ręcznie:

```powershell
.\.venv\Scripts\activate
python main.py
```

Po uruchomieniu zobaczysz:

```text
Power BI DAX Agent
Wpisz 'exit' zeby zakonczyc

Ja:
```

## Przykładowe Pytania

```text
Które miary są nieużywane?
```

```text
Wypisz istniejące miary DAX.
```

```text
Jakie miary DAX sugerujesz dla tego modelu?
```

```text
Dodaj miary time intelligence: YTD, MTD i YoY.
```

```text
Jak poprawić DAX dla SLA?
```

## Tryb DAX-Only

Jeżeli zapytasz o relacje, kolumny albo ogólną optymalizację modelu, agent nie będzie już próbował działać jak pełny modeler Power BI. Zamiast tego odpowie z perspektywy DAX albo poprosi o pytanie dotyczące miar.

Przykład:

```text
Które kolumny są nieużywane?
```

Agent potraktuje to jako temat poza głównym trybem i przypomni, że obsługuje miary, formuły DAX, zależności między miarami i użycie miar w raporcie.

## Analiza Użycia Miar

Dla pytania o nieużywane miary agent sprawdza:

- odwołania do miar w innych formułach DAX, np. `[Orders]`,
- użycia miar w definicjach wizualizacji raportu JSON,
- nazwy miar z tabel TMDL.

Wynik ma formę:

```text
Miary bez jawnego uzycia:
1. Nazwa miary (Tabela)
2. Inna miara (Tabela)
```

Uwaga: wynik oznacza brak jawnego użycia w analizowanych plikach. Miara nadal może być potrzebna, jeżeli jest używana poza raportem, w zewnętrznych narzędziach, zakładkach, tooltipach albo ręcznie przez użytkowników.

## Konfiguracja

Konfiguracja znajduje się w:

```text
services/config.py
```

Wymagane wartości:

| Nazwa | Znaczenie |
| --- | --- |
| `MODEL` | nazwa lokalnego modelu LLM |
| `BASE_URL` | adres lokalnego API zgodnego z OpenAI |
| `API_KEY` | klucz dla klienta API, przy lokalnym LLM zwykle placeholder |
| `SCIEZKA` | pełna ścieżka do folderu `.SemanticModel` |

Przykład:

```python
MODEL = "local-model"
BASE_URL = "http://127.0.0.1:8080/v1"
API_KEY = "llama.cpp"
SCIEZKA = r"C:\...\Amazon Delivery-pr.SemanticModel"
```

## Struktura Projektu

| Plik | Rola |
| --- | --- |
| `main.py` | interaktywny program CLI |
| `services/agent.py` | logika agenta DAX, analiza miar i promptowanie LLM |
| `services/tmdlreader.py` | odczyt plików TMDL |
| `services/tmdl_editor.py` | kontrolowany zapis zmian do TMDL |
| `services/llm_client.py` | komunikacja z lokalnym LLM |
| `public/preview.py` | mały publiczny przykład przepływu wyboru sugestii |
| `tests/test_dax_agent.py` | testy regresyjne trybu DAX-only |

## Bezpieczeństwo Zmian

Agent nie zapisuje dowolnego tekstu wygenerowanego przez LLM. Zapis przechodzi przez `services/tmdl_editor.py`, który obsługuje kontrolowane operacje.

W trybie DAX-only najważniejsza operacja to:

| Operacja | Efekt |
| --- | --- |
| `add_measure` | dodaje albo aktualizuje miarę w pliku TMDL |

Przed pierwszą edycją pliku tworzona jest kopia zapasowa w folderze `.backups`.

## Testy

Uruchomienie testów:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Kontrola składni:

```powershell
.\.venv\Scripts\python.exe -m compileall main.py services tests
```

## Ograniczenia

- Parser TMDL jest lekki i opiera się na strukturze tekstowej plików.
- Analiza użycia miar wykrywa jawne referencje, nie gwarantuje pełnej semantycznej walidacji Power BI.
- Formuły DAX wygenerowane przez LLM trzeba sprawdzić w Power BI Desktop.
- Agent działa lokalnie, ale jakość odpowiedzi zależy od użytego modelu LLM.
