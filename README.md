# Projekt na zajęcia z programowania komputerów. #


## Instrukcja uruchomienia ##

## Aby uruchomić projekt lokalnie na swoim komputerze wykonaj poniższe kroki: ##


### 1. Przygotowanie środowiska wirtualnego ###
Otwórz terminal w głównym folderze projektu (FlaskProjekt) i utwórz środowisko wirtualne: python -m venv venv
Następnie aktywuj środowisko wirtualne:
- Windows (PowerShell): .\\venv\\Scripts\\Activate.ps1
- Windows (CMD): .\\venv\\Scripts\\activate.bat
- Linux / macOS: source venv/bin/activate


### 2. Instalacja wymaganych bibliotek ###
Gdy środowisko jest aktywne (widoczny napis (venv) w terminalu), zainstaluj zależności: pip install -r requirements.txt


### 3. Konfiguracja zmiennych środowiskowych (.env) ###
Utwórz w głównym folderze plik o nazwie .env i uzupełnij go kluczami deweloperskimi z Twitch Developer Portal:
CLIENT_ID = ...
CLIENT_SECRET = ...


### 4. Uruchomienie aplikacji ###
Uruchom serwer deweloperski Flaska: python app.py


### 5. Requirements.txt ###
Wygenerować w terminalu plik 'requirements.txt' komendą (będąc w wirtualnym środowisku 'venv'): pip freeze > requirements.txt