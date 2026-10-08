# Środowisko w przeglądarce (GitHub Codespaces)

Dla osób, które nie mogą zainstalować oprogramowania na swoim komputerze —
zwykle z powodu braku uprawnień administratora na sprzęcie służbowym.

Wszystko działa w przeglądarce. Na komputerze nie instalujemy niczego.

---

## Co dostajesz

Gotowe środowisko z zainstalowanymi: **Pythonem, Node.js, gitem, Claude Code**
oraz edytorem VS Code w przeglądarce. Repozytorium ćwiczeniowe jest już sklonowane.

## Uruchomienie

1. Wejdź na stronę repozytorium na GitHubie.
2. Zielony przycisk **Code** → zakładka **Codespaces** → **Create codespace on main**.
3. Poczekaj 2–3 minuty. Za pierwszym razem środowisko się buduje; przy kolejnych uruchomieniach startuje w kilkanaście sekund.
4. Gdy w terminalu na dole zobaczysz „Środowisko gotowe” — możesz zaczynać.

## Logowanie do Claude Code

W terminalu wpisz:

```bash
claude
```

Otworzy się link do zalogowania. Zaloguj się na swoje konto Claude (Pro albo Max),
wróć do zakładki z Codespace — narzędzie jest gotowe.

> Zrób to **przed zajęciami**, nie w ich trakcie.

## Sprawdzenie

```bash
git --version
python --version
node --version
claude --version
```

Wszystkie cztery powinny odpowiedzieć numerem wersji.

## Rzeczy, o których warto wiedzieć

| | |
|---|---|
| **Limit darmowy** | Konto GitHub Free daje 120 godzin rdzenia miesięcznie — przy maszynie 2-rdzeniowej to 60 godzin pracy. Na cały cykl wystarcza z zapasem. |
| **Zatrzymywanie** | Codespace zatrzymuje się sam po 30 minutach bezczynności. Możesz go też zatrzymać ręcznie, żeby nie zużywać limitu. |
| **Trwałość plików** | Pliki w katalogu roboczym zostają między sesjami. Zmiany poza nim mogą zniknąć. |
| **Wydajność** | Do zadań tego kursu maszyna 2-rdzeniowa w zupełności wystarcza. |

## Jeśli coś nie działa

Napisz na adres podany w notatce, z informacją, na którym kroku i jaki komunikat się pojawił.
Nie walcz dłużej niż kwadrans.
