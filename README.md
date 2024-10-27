# Edupage Verifikácia v Discorde

Edupage Verifikácia v Discorde je Discord bot navrhnutý na automatizáciu procesu overenia študentského statusu v rámci Discord serveru pomocou školského potvrdenia z Edupage. Po úspešnom overení bot zmení prezývku študenta na jeho skutočné meno a pridelí mu rolu na základe jeho školského ročníka. Tento projekt zjednodušuje správu študentských identít a rolí, čo pomáha administrátorom serveru vytvoriť organizovanú komunitu pre študentov a pedagógov.

## Funkcie

- **Automatizované overenie študentov**: Overenie, či je študent zapísaný v škole, pomocou potvrdenia z Edupage.
- **Aktualizácia prezývky na skutočné meno**: Po úspešnom overení bot nastaví študentovi prezývku podľa jeho skutočného mena.
- **Priraďovanie rolí podľa ročníka**: Automatické priraďovanie rolí na základe ročníka študenta, čo zaručuje správne kategorizovanie všetkých členov na serveri.
- **Bezpečné overenie**: Využíva bezpečnostný systém potvrdení Edupage na zabezpečenie študentskej identity.

## Obsah

- [Inštalácia](#Inštalácia)
- [Konfigurácia](#Konfigurácia)
- [Použitie](#Použitie)
- [Licencia](#Licencia)
- [Poďakovanie](#Poďakovanie)

## Inštalácia

### Predpoklady

1. **Python 3.8+**
2. **Knižnica Discord.py**
3. **Prístup k API Edupage** (alebo obdobný systém overenia školy)
   
### Konfigurácia

1. Klonujte repozitár:
   ```bash
   git clone https://github.com/yourusername/edupage-verification-discord.git
   cd edupage-verification-discord```

2. Nainštalujte potrebné knižnice
  ```bash
  pip install -r requirements.txt
  ```
3. Nastavte Konfiguračné súbory
- ```Bot/Bot_data.json```: Tu vkladáte vlastné správy

### Použitie
1. ```python bot.py```
2. Bot automaticky počúva na pripojenie nových členov a vyzve ich na dokončenie procesu overenia pomocou potvrdenia z Edupage.

## Licencia
Distribuované pod licenciou GPL v3.0 . Viac informácií nájdete v súbore LICENSE.

## Poďakovanie
Špeciálne poďakovanie patrí Edupage za poskytovanie systému overovania a všetkým prispievateľom, ktorí pomáhajú vylepšovať tento projekt.