# Enkel Blockchain med Flask og Dynamisk Vanskelighetsgrad

Dette er et læringsprosjekt som viser hvordan en enkel blokkjede fungerer. Det bruker Python, Flask og dynamisk justering av vanskelighetsgrad for mining. Perfekt for å lære hvordan `hash`, `proof of work` og `blokkvalidering` fungerer i praksis.

Dette prosjektet illustrerer sentrale blockchain-konsepter:

- Hashing og integritet
- Blokkjede-struktur
- Proof of Work
- Manipulering og validering
- Dynamisk vanskelighetsjustering

## Funksjoner

- Legg til blokker via webskjema
- Proof of work med SHA-256 og nonce
- Dynamisk justering av vanskelighetsgrad basert på gjennomsnittlig mining-tid
- Valider og reparer kjeden
- Simuler blokker med feil og observer konsekvenser
- Egne visninger for kjede og logg
- Popup-detaljer for hver blokk
- CSS-basert futuristisk design

## Eksempel på bruk

Når du legger til en blokk:

- Den mines med proof of work
- Nonce justeres til hash starter med X nuller (avhengig av vanskelighetsgrad)
- Tiden registreres og påvirker vanskelighetsgrad neste gang

## Teknologi

- Python 3.x
- Flask
- Poetry for avhengighetsstyring
- HTML + CSS for UI

## Prosjektstruktur

```
blockchain/
│
├── src/
│   └── blockchain/
│       ├── __init__.py
│       ├── blockchain.py       # Logikken for selve blokkjeden
│       └── node.py             # Flask-app og API-endepunkter
│
├── templates/                  # HTML-malene for Flask
│   ├── index.html
│   └── log.html
│
├── static/                     # CSS og annet statisk innhold
│   └── style.css
│
├── pyproject.toml             # Poetry-konfigurasjon
├── README.md
└── .gitignore
```

## Kom i gang

### 1. Klon prosjektet

```bash
git clone https://github.com/dittbrukernavn/blockchain-prosjekt.git
cd blockchain
```

### 2. Installer avhengigheter med Poetry

```bash
poetry install
```

### 3. Start prosjektet

```bash
poetry run python src/blockchain/node.py
```

Applikasjonen kjører da på http://127.0.0.1:5000/.

## Lisens

Dette prosjektet er lisensiert under [MIT-lisensen](LICENSE).

Laget med ❤️ og CPU-varme 🔥 for å forstå hvordan blockchain fungerer!

## Skjermbilder

![Skjermbilde av startskjermen for blokkjeden](images/skjermbilde_blokkjede.png)
![Skjermbilde av loggen for blokkjeden](images/skjermbilde_logg.png)
![Skjermbilde av blokkdetaljer](images/skjermbilde_logg_detaljer.png)
