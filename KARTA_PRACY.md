# Karta pracy — warsztat indywidualny, ok. 50 minut

Zaznaczaj kroki w miarę postępu. **Nie musisz zrobić wszystkiego** — fazy F0–F4 to ścieżka
podstawowa, F5 to publikacja, a sekcja „Bez sufitu" jest dla tych, którym zostanie czas
(i nie ma górnej granicy — wybieraj, co Cię ciekawi).

Po fazach **F1, F3 i F4** wpisz na czacie `F1` / `F3` / `F4` — to checkpoint dla prowadzącego.

---

## F0 · Spójrz, zanim włączysz silnik (3 min, bez AI)

- [ ] Otwórz `dane/uczestnicy.csv` i po prostu na niego popatrz. Nie analizuj — popatrz.
- [ ] Zapisz **co najmniej trzy rzeczy**, które są nie tak z tym plikiem.

> To jedyny moment ćwiczenia bez AI — i jest potrzebny. Za chwilę sprawdzisz,
> czy agent zauważył to samo, co Ty.

## F1 · Pamięć projektu (5 min)

- [ ] Uruchom agenta w katalogu repozytorium: `claude`
- [ ] Wydaj polecenie `/init` — agent przeczyta projekt i zaproponuje plik `CLAUDE.md`.
- [ ] **Przeczytaj wygenerowany CLAUDE.md.** Czy agent dobrze zrozumiał, czym jest ten projekt?
- [ ] Dopisz (poproś agenta albo zrób to sam) jedną regułę:
      `Wyniki zapisuj w folderze wyniki/. Komunikaty i raporty po polsku.`
- [ ] Checkpoint: wpisz `F1` na czacie.

## F2 · Plan przed kodem (10 min)

- [ ] Przełącz agenta w **tryb planowania** (Shift+Tab, aż zobaczysz „plan mode").
- [ ] Opisz własnymi słowami CEL (nie technologię!): kto potrzebuje listy, jaka jest reguła
      (≥6 z 8 obecności), co ma powstać. Dodaj: *„Zanim cokolwiek napiszesz, przeanalizuj
      jakość danych w pliku i przedstaw mi plan — z listą problemów, które znalazłeś."*
- [ ] **Przeczytaj plan.** Porównaj z Twoją listą z F0: co agent znalazł, czego nie zauważył,
      co znalazł ponad Twoją listę?
- [ ] Jeśli w planie czegoś brakuje — powiedz mu to. Dopiero potem zaakceptuj plan.

## F3 · Implementacja i konfrontacja (15 min)

- [ ] Pozwól agentowi zaimplementować plan. Obserwuj, o jakie zgody prosi — czytaj, zanim zatwierdzisz.
- [ ] Uruchom wynik. **Ile osób dostaje zaświadczenie?** Zapisz liczbę.
- [ ] Skonfrontuj z rzeczywistością — sprawdź konkretnie:
  - [ ] Czy ktoś występuje w pliku dwa razy? (podpowiedź: patrz na e-maile, nie nazwiska)
  - [ ] Czy wszystkie wiersze mają komplet danych?
  - [ ] Czy obecność jest zapisana wszędzie tak samo?
- [ ] Każ poprawić to, co pominięte, i uruchom ponownie. **Liczba się zmieniła?**
      Jeśli nie — coś wciąż jest przeoczone.
- [ ] Poproś agenta: *„Zapisz ten etap w gicie — commit z opisem po polsku, co zrobiliśmy."*
- [ ] Checkpoint: wpisz `F3` na czacie.

## F4 · Raport dla człowieka (10 min)

Sama liczba nikomu nie wystarczy. Dziekanat musi wiedzieć, **komu odmówić i dlaczego**.

- [ ] Poproś o drugi plik wynikowy: lista osób **nieuprawnionych** z przyczyną
      (za mało obecności / brak danych / duplikat).
- [ ] Przeczytaj raport tak, jakbyś miał(a) wysłać go dziekanatowi. Zrozumiały dla kogoś,
      kto nie widział pliku źródłowego?
- [ ] **Pytanie-pułapka:** czy w danych są przypadki, w których NIE MA jednej poprawnej
      odpowiedzi? Co agent z nimi zrobił — zdecydował po cichu czy zapytał Ciebie?
      To różnica między decyzją techniczną a biznesową.
- [ ] Drugi commit: *„Zapisz ten etap w gicie z opisem."* Obejrzyj historię: `git log --oneline`
- [ ] Checkpoint: wpisz `F4` na czacie.

## F5 · Publikacja na GitHubie (7 min)

Twoja praca zasługuje na dom. Zbudujesz go przez przeglądarkę — dokładnie tak,
jak widzieliśmy na początku spotkania.

- [ ] Na github.com: **+** (prawy górny róg) → *New repository* → nazwa `zaswiadczenia-IMIE`
      (np. `zaswiadczenia-rafal`) → **Private** → *Create repository* (nic nie zaznaczaj poniżej).
- [ ] GitHub pokaże stronę z instrukcjami. Interesuje Cię sekcja „…or push an existing
      repository". Wróć do agenta i poproś:
      *„Podepnij to repozytorium pod adres <wklej adres https z GitHuba> i wypchnij całość."*
- [ ] Przy pierwszym pushu wyskoczy okno logowania GitHuba w przeglądarce — zaloguj się
      i wróć do terminala.
- [ ] Odśwież stronę repozytorium. Widzisz pliki, commity i ich opisy? **To jest ten moment.**
      Wpisz na czacie link do swojego repo (jeśli chcesz się pochwalić) albo samo `F5`.

---

## Bez sufitu — rozszerzenia (dowolna kolejność, dowolnie dużo)

- [ ] **Zaświadczenia:** osobny plik zaświadczenia dla każdej uprawnionej osoby
      (imię, nazwisko, jednostka, liczba obecności).
- [ ] **Zestawienie wg jednostek:** ile zaświadczeń na jednostkę? (Uwaga: najpierw przyjrzyj
      się, jak zapisane są nazwy jednostek. To nie przypadek.)
- [ ] **Testy:** poproś o testy logiki progu. Potem je PRZECZYTAJ: sprawdzają wymaganie,
      czy tylko potwierdzają to, co kod już robi? (Wrócimy do tego na sesji 7.)
- [ ] **Próg jako parametr:** 6 z 8 jest zaszyte w kodzie — niech będzie parametrem.
      Co się dzieje przy progu 0? Przy 9?
- [ ] **README projektu:** niech agent napisze README dla dziekanatu — jak uruchomić,
      co powstaje, jakie decyzje przyjęto przy niejednoznacznych danych.
- [ ] **CLAUDE.md dojrzewa:** dopisz do CLAUDE.md konwencje, które przyjęliście po drodze
      (format raportów, nazwy plików wyników). Zacznij NOWĄ sesję (`/clear`) i sprawdź,
      czy agent je pamięta.
- [ ] **Świeże spojrzenie:** w nowej sesji poproś agenta o krytyczny przegląd własnego
      skryptu. Co znalazł?

---

## Na koniec — do bloku podsumowującego

Zapisz jedno zdanie:

> **W którym momencie agent zrobił coś, czego nie zauważył(a)byś, gdybyś nie czytał(a)
> jego planów i zmian?**

To zdanie powiesz (lub wkleisz na czat) przy omówieniu.
