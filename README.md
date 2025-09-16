

## Wymagania
biblioteka openai, wraz z kluczem API (model GPT-4o-mini)

python 3.10+ ( realizowane - wersja 3.13)

``pip install openai``


## Konfiguracja

- Plik z opisem świata gry w folderze `data/` (domyślnie `data/fantasy.md`) w formacie tekstowym lub markdown.  
- W pliku `main.py` wpisz swój klucz API OpenAI:

OPENAI_API_KEY = "klucz_api"

## Przykładowe uruchomienia

Plik z danymi z przykładową komunikacją z openai w pliku `test_runs.txt`

Testy integracyjne do sprawdzenia poprawności założeń:

``python test_run.py``


## Użytkowanie

### Tryb interaktywny

``python main.py --interactive``

Dostępne komendy (wpisuj w konsoli):  
- `story-understanding <pytanie>` — zadaj pytanie dotyczące świata gry  
- `generate-hero` — wygeneruj unikalne imię bohatera - zapisuje do pliku names_generated.json
- `generate-details <nazwa>` — wygeneruj szczegóły postaci o podanym imieniu  
- `exit` — zamyka program



## Obserwacje i wnioski

Do wykonania punktu z generowaniem unikalnych nazw bohaterów wykorzystałem plik json, w którym po wygenerowaniu danego bohatera
umieszczam tą zawartość w pliku, a podczas wysłania zapytania do api, sprawdzam aby wygenerowało inne niż podane w pliku.