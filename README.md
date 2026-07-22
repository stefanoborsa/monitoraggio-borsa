# 📊 Financial Agent PRO

Agent AI che raccoglie dati finanziari globali, analizza le notizie con ragionamento intelligente e pubblica un report completo ogni mattina.

## 🌍 Cosa Analizza

| Sezione | Contenuto | N. Titoli |
|---------|-----------|-----------|
| **Indici Mondiali** | S&P 500, Dow Jones, Nasdaq, Russell 2000, VIX, Euro Stoxx 50, DAX, CAC 40, FTSE 100, IBEX 35, Nikkei 225, Hang Seng, Shanghai, KOSPI, ASX 200, Nifty 50, Tadawul, FTSE MIB | 23 |
| **FTSE MIB Completo** | Tutti i 40 titoli con top/peggiori performer | 40 |
| **Commodities** | Oro, Argento, Platino, Palladio, Petrolio WTI/Brent, Gas Naturale, Rame, Mais, Grano, Soia, Caffè, Cacao, Cotone, Zucchero | 15 |
| **Big Tech USA** | Apple, Microsoft, Google, Amazon, Meta, NVIDIA, Tesla, Netflix, AMD, Intel, Salesforce, Adobe, Oracle, IBM, Uber | 15 |
| **Crypto** | Bitcoin, Ethereum, Solana, Ripple, Cardano, Polkadot, Polygon, Avalanche | 8 |
| **Forex** | EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, EUR/GBP, EUR/JPY | 8 |
| **News Driver** | Notizie analizzate con keyword matching avanzato, contesto settoriale e ragionamento di impatto | Top 12 |
| **Tutte le Notizie** | Ultime 20 notizie da fonti multiple | 20 |

**Totale: ~109 titoli/indici analizzati**

## 🔥 News Driver - Analisi Intelligente

Lo script analizza le notizie con un approccio simile a un LLM:

- **Keyword matching avanzato**: associa notizie a ticker specifici
- **Contesto settoriale**: identifica settori coinvolti (tech, energia, banche, lusso, ecc.)
- **Analisi di impatto**: classifica come basso/medio/alto in base a segnali linguistici
- **Ragionamento causale**: spiega perché una notizia è rilevante
- **Sentiment analysis**: positivo/negativo/neutrale
- **Performance in tempo reale**: mostra come i titoli coinvolti stanno performando

### Esempio

| Notizia | Ticker Matchati | Impatto | Sentiment |
|---------|----------------|---------|-----------|
| "Apple lancia nuovo iPhone con AI" | AAPL, NVDA | 🔴 ALTO | 📈 Positivo |
| "Fed alza i tassi di 25bp" | ^GSPC, ^STOXX50E, ISP.MI, UCG.MI | 🔴 ALTO | 📉 Negativo |
| "Enel accelera sulle rinnovabili" | ENEL.MI, A2A.MI, SRG.MI | 🟡 MEDIO | 📈 Positivo |

## 📁 Struttura del Repository

```
finance-briefing/
├── daily_finance_pro.py          # Script principale
├── .github/
│   └── workflows/
│       └── daily-briefing.yml    # Workflow GitHub Actions
├── reports/
│   ├── latest.md                  # Report sempre aggiornato
│   └── briefing_20260115.md     # Archivio storico
└── README.md                      # Questo file
```

## 🚀 Come Usare

### 1. Clona il repository
```bash
git clone https://github.com/tuousername/finance-briefing.git
cd finance-briefing
```

### 2. Installa le dipendenze
```bash
pip install yfinance pandas
```

### 3. Esegui manualmente
```bash
python daily_finance_pro.py
```

Il report verrà salvato in `reports/briefing_YYYYMMDD.md` e `reports/latest.md`.

## ⚙️ Automazione con GitHub Actions

Il workflow è configurato per eseguirsi automaticamente:
- **Orario**: 8:30 del mattino (CET/CEST), dal lunedì al venerdì
- **Output**: Commit automatico con il nuovo report in `reports/`

### Configurazione

1. Vai su **Settings → Actions → General**
2. Assicurati che "Workflow permissions" sia su "Read and write permissions"
3. Il workflow è già configurato nel file `.github/workflows/daily-briefing.yml`

### Esecuzione Manuale

Puoi avviare il workflow manualmente dalla scheda **Actions** → seleziona "Daily Finance Briefing PRO" → **Run workflow**.

## 📖 Leggere il Report

Dopo ogni esecuzione, il report è disponibile su GitHub:

```
https://github.com/tuousername/finance-briefing/blob/main/reports/latest.md
```

Oppure naviga nella cartella `reports/` per vedere l'archivio storico.

## 🛠️ Personalizzazione

### Aggiungere nuovi titoli

Modifica il dizionario corrispondente in `daily_finance_pro.py`:

```python
self.ftse_mib['NUOVO.MI'] = 'Nome Azienda'
self.tech['TICKER'] = 'Nome Azienda'
```

### Modificare l'orario di esecuzione

Nel file `.github/workflows/daily-briefing.yml`, modifica la riga:

```yaml
- cron: '30 6 * * 1-5'  # 6:30 UTC = 8:30 Italia (CEST)
```

Formato cron: `minuto ora * * giorni_settimana`

### Aggiungere keyword per news driver

Modifica il dizionario `self.keyword_map` in `daily_finance_pro.py`:

```python
'nuova_keyword': 'TICKER',
```

## 📊 Esempio di Output

```markdown
# 📊 BRIEFING FINANZIARIO PRO
**Data:** 22/07/2026 08:30

## 🌍 Indici Mondiali
🟢 S&P 500 (USA)              5,847.20 (+0.45%)
🟢 Dow Jones (USA)           44,123.50 (+0.32%)
...

## 🇮🇹 FTSE MIB - Tutti i 40 Titoli
### 🏆 Top 5 Performer
🟢 **UniCredit** — €32.1045 (+2.10%)
...

## 🔥 News Driver - Analisi Intelligente
### 1. "NVIDIA batte le stime del trimestre"
**Impatto stimato:** 🔴 ALTO (score: 8)
**Sentiment:** 📈 Positivo
**Settori coinvolti:** tecnologia
**Ragionamento:** Segnale alto impatto: 'earnings'

| Titolo | Prezzo | Variazione |
|--------|--------|------------|
| 🟢 NVIDIA (NVDA) | 875.30 | +3.45% |
| 🟢 AMD (AMD) | 142.50 | +1.20% |
```

## ⚠️ Disclaimer

I dati sono forniti da Yahoo Finance tramite la libreria `yfinance` e sono a scopo informativo. Non costituiscono consulenza finanziaria. Verifica sempre i dati prima di prendere decisioni di investimento.

## 📄 Licenza

MIT License - Libero uso e modifica.
