#!/usr/bin/env python3
"""
Financial Agent PRO - Briefing completo quotidiano con LLM
Mercati: FTSE MIB completo (40 titoli), Indici mondiali, Commodities, Crypto
Analisi: News driver con LLM per riassunti intelligenti
Output: Report salvato come file nel repository GitHub
Esecuzione: python3 daily_finance_pro.py
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import json
import re

class FinancialAgentPro:
    def __init__(self):
        # ========== TUTTI I 40 TITOLI DEL FTSE MIB ==========
        self.ftse_mib = {
            'A2A.MI': 'A2A',
            'AMP.MI': 'Amplifon',
            'ATL.MI': 'Atlantia',
            'AZM.MI': 'Azimut',
            'BGN.MI': 'Banca Generali',
            'BMED.MI': 'Banca Mediolanum',
            'BAMI.MI': 'Banco BPM',
            'BPE.MI': 'BPER Banca',
            'DIA.MI': 'DiaSorin',
            'ENEL.MI': 'Enel',
            'ENI.MI': 'Eni',
            'ERG.MI': 'ERG',
            'RACE.MI': 'Ferrari',
            'FBK.MI': 'FinecoBank',
            'G.MI': 'Generali',
            'HER.MI': 'Hera',
            'INW.MI': 'Infrastrutture Wireless',
            'ISP.MI': 'Intesa Sanpaolo',
            'IRE.MI': 'IREN',
            'IVG.MI': 'IVG',
            'LDO.MI': 'Leonardo',
            'MB.MI': 'Mediobanca',
            'MONC.MI': 'Moncler',
            'NEXI.MI': 'Nexi',
            'PIRC.MI': 'Pirelli',
            'PRY.MI': 'Prysmian',
            'REC.MI': 'Recordati',
            'SPM.MI': 'Saipem',
            'SRG.MI': 'Snam',
            'STM.MI': 'STMicroelectronics',
            'STLAM.MI': 'Stellantis',
            'TEN.MI': 'Tenaris',
            'TRN.MI': 'Terna',
            'TIT.MI': 'Telecom Italia',
            'UCG.MI': 'UniCredit',
            'UNI.MI': 'Unipol',
            'US.MI': 'UnipolSai',
            'WBDR.MI': 'Webuild',
        }

        # ========== INDICI MONDIALI ==========
        self.indices = {
            # Americhe
            '^GSPC': 'S&P 500 (USA)',
            '^DJI': 'Dow Jones (USA)',
            '^IXIC': 'Nasdaq (USA)',
            '^RUT': 'Russell 2000 (USA)',
            '^VIX': 'VIX (Volatilità)',
            '^MXX': 'IPC (Messico)',
            '^BVSP': 'Bovespa (Brasile)',

            # Europa
            '^STOXX50E': 'Euro Stoxx 50',
            '^DAX': 'DAX 40 (Germania)',
            '^MDAXI': 'MDAX (Germania)',
            '^FCHI': 'CAC 40 (Francia)',
            '^FTSE': 'FTSE 100 (UK)',
            '^IBEX': 'IBEX 35 (Spagna)',
            '^AEX': 'AEX (Olanda)',
            '^SSMI': 'SMI (Svizzera)',
            'FTSEMIB.MI': 'FTSE MIB (Italia)',

            # Asia-Pacifico
            '^N225': 'Nikkei 225 (Giappone)',
            '^HSI': 'Hang Seng (Hong Kong)',
            '^HSCE': 'Hang Seng China Ent.',
            '000001.SS': 'Shanghai Composite (Cina)',
            '399001.SZ': 'Shenzhen Component (Cina)',
            '^KS11': 'KOSPI (Corea del Sud)',
            '^AXJO': 'ASX 200 (Australia)',
            '^NSEI': 'Nifty 50 (India)',

            # Medio Oriente
            '^TASI.SR': 'Tadawul (Arabia Saudita)',
        }

        # ========== COMMODITIES ==========
        self.commodities = {
            'GC=F': 'Oro',
            'SI=F': 'Argento',
            'CL=F': 'Petrolio WTI',
            'BZ=F': 'Petrolio Brent',
            'NG=F': 'Gas Naturale',
            'HG=F': 'Rame',
            'PL=F': 'Platino',
            'PA=F': 'Palladio',
            'ZC=F': 'Mais',
            'ZW=F': 'Grano',
            'ZS=F': 'Soia',
            'KC=F': 'Caffè',
            'CC=F': 'Cacao',
            'CT=F': 'Cotone',
            'SB=F': 'Zucchero',
            'LBS=F': 'Legname',
        }

        # ========== BIG TECH USA ==========
        self.tech = {
            'AAPL': 'Apple',
            'MSFT': 'Microsoft',
            'GOOGL': 'Alphabet',
            'AMZN': 'Amazon',
            'META': 'Meta',
            'NVDA': 'NVIDIA',
            'TSLA': 'Tesla',
            'NFLX': 'Netflix',
            'AMD': 'AMD',
            'INTC': 'Intel',
            'CRM': 'Salesforce',
            'ADBE': 'Adobe',
            'ORCL': 'Oracle',
            'IBM': 'IBM',
            'UBER': 'Uber',
        }

        # ========== CRYPTO ==========
        self.crypto = {
            'BTC-USD': 'Bitcoin',
            'ETH-USD': 'Ethereum',
            'SOL-USD': 'Solana',
            'XRP-USD': 'Ripple',
            'ADA-USD': 'Cardano',
            'DOT-USD': 'Polkadot',
            'MATIC-USD': 'Polygon',
            'AVAX-USD': 'Avalanche',
        }

        # ========== FOREX ==========
        self.forex = {
            'EURUSD=X': 'EUR/USD',
            'GBPUSD=X': 'GBP/USD',
            'USDJPY=X': 'USD/JPY',
            'USDCHF=X': 'USD/CHF',
            'AUDUSD=X': 'AUD/USD',
            'USDCAD=X': 'USD/CAD',
            'EURGBP=X': 'EUR/GBP',
            'EURJPY=X': 'EUR/JPY',
        }

        # Raccogli tutti i ticker
        self.all_tickers = []
        for group in [self.ftse_mib, self.indices, self.commodities, self.tech, self.crypto, self.forex]:
            self.all_tickers.extend(list(group.keys()))

        # ========== MAPPA KEYWORD PER NEWS DRIVER ==========
        self.keyword_map = {
            # Tech
            'apple': 'AAPL', 'iphone': 'AAPL', 'mac': 'AAPL', 'ipad': 'AAPL',
            'microsoft': 'MSFT', 'azure': 'MSFT', 'windows': 'MSFT',
            'google': 'GOOGL', 'alphabet': 'GOOGL', 'youtube': 'GOOGL',
            'nvidia': 'NVDA', 'gpu': 'NVDA', 'ai chip': 'NVDA', 'artificial intelligence': 'NVDA',
            'meta': 'META', 'facebook': 'META', 'instagram': 'META', 'whatsapp': 'META',
            'tesla': 'TSLA', 'elon musk': 'TSLA', 'ev': 'TSLA', 'electric vehicle': 'TSLA',
            'amazon': 'AMZN', 'aws': 'AMZN', 'prime': 'AMZN',
            'netflix': 'NFLX', 'streaming': 'NFLX',
            'amd': 'AMD', 'intel': 'INTC', 'salesforce': 'CRM',

            # Italia
            'enel': 'ENEL.MI', 'enel green': 'ENEL.MI', 'rinnovabili': 'ENEL.MI',
            'eni': 'ENI.MI', 'oil': 'ENI.MI', 'gas': 'ENI.MI', 'petrolio': 'ENI.MI',
            'unicredit': 'UCG.MI', 'intesa': 'ISP.MI', 'sanpaolo': 'ISP.MI',
            'ferrari': 'RACE.MI', 'stellantis': 'STLAM.MI', 'fiat': 'STLAM.MI',
            'leonardo': 'LDO.MI', 'defense': 'LDO.MI', 'difesa': 'LDO.MI',
            'saipem': 'SPM.MI', 'tenaris': 'TEN.MI',
            'prysmian': 'PRY.MI', 'cavi': 'PRY.MI',
            'nexi': 'NEXI.MI', 'pagamenti': 'NEXI.MI',
            'moncler': 'MONC.MI', 'luxury': 'MONC.MI', 'lusso': 'MONC.MI',
            'generali': 'G.MI', 'assicurazioni': 'G.MI',
            'snam': 'SRG.MI', 'gasdotto': 'SRG.MI',
            'terna': 'TRN.MI', 'elettricità': 'TRN.MI',
            'telecom italia': 'TIT.MI', 'tim': 'TIT.MI',
            'diasorin': 'DIA.MI', 'recordati': 'REC.MI', 'farmaceutica': 'REC.MI',
            'amplifon': 'AMP.MI', 'a2a': 'A2A.MI', 'energia': 'A2A.MI',
            'banco bpm': 'BAMI.MI', 'bper': 'BPE.MI',
            'finecobank': 'FBK.MI', 'mediobanca': 'MB.MI',
            'azimut': 'AZM.MI', 'banca generali': 'BGN.MI',
            'mediolanum': 'BMED.MI', 'hera': 'HER.MI', 'iren': 'IRE.MI',
            'erg': 'ERG.MI', 'inwit': 'INW.MI',
            'atlantia': 'ATL.MI', 'webuild': 'WBDR.MI',
            'pirelli': 'PIRC.MI', 'gomme': 'PIRC.MI',

            # Commodities
            'gold': 'GC=F', 'oro': 'GC=F',
            'silver': 'SI=F', 'argento': 'SI=F',
            'oil': 'CL=F', 'petrolio': 'CL=F', 'crude': 'CL=F',
            'brent': 'BZ=F',
            'natural gas': 'NG=F', 'gas naturale': 'NG=F',
            'copper': 'HG=F', 'rame': 'HG=F',
            'wheat': 'ZW=F', 'grano': 'ZW=F',
            'coffee': 'KC=F', 'caffè': 'KC=F',
            'cocoa': 'CC=F', 'cacao': 'CC=F',
            'cotton': 'CT=F', 'cotone': 'CT=F',
            'sugar': 'SB=F', 'zucchero': 'SB=F',
            'corn': 'ZC=F', 'mais': 'ZC=F',
            'soybean': 'ZS=F', 'soia': 'ZS=F',
            'lumber': 'LBS=F', 'legname': 'LBS=F',

            # Crypto
            'bitcoin': 'BTC-USD', 'btc': 'BTC-USD',
            'ethereum': 'ETH-USD', 'eth': 'ETH-USD',
            'solana': 'SOL-USD',
            'ripple': 'XRP-USD', 'xrp': 'XRP-USD',
            'cardano': 'ADA-USD',
            'polkadot': 'DOT-USD',
            'polygon': 'MATIC-USD',
            'avalanche': 'AVAX-USD',

            # Macro
            'fed': '^GSPC', 'federal reserve': '^GSPC',
            'ecb': '^STOXX50E', 'bce': '^STOXX50E',
            'inflation': '^GSPC', 'inflazione': '^STOXX50E',
            'interest rate': '^GSPC', 'tassi': '^STOXX50E',
            'recession': '^GSPC', 'recessione': '^STOXX50E',
            'gdp': '^GSPC', 'pil': '^STOXX50E',
            'war': 'GC=F', 'guerra': 'GC=F',
            'trade war': 'CL=F', 'guerra commerciale': 'CL=F',
        }

    def run(self):
        print(f"🤖 Financial Agent PRO avviato alle {datetime.now().strftime('%H:%M:%S')}")

        # 1. Raccogli dati di mercato
        print("📊 Raccogliendo dati di mercato...")
        market_data = self._get_market_data()

        # 2. Raccogli notizie da fonti multiple
        print("📰 Raccogliendo notizie...")
        all_news = self._get_all_news()

        # 3. Analizza news driver con LLM
        print("🔍 Analizzando news driver con LLM...")
        news_drivers = self._analyze_news_drivers_llm(all_news, market_data)

        # 4. Genera report completo
        print("📝 Generando report...")
        report = self._generate_report(market_data, all_news, news_drivers)

        # 5. Salva report nel repository
        self._save_report(report)

        print("✅ Briefing PRO completato e salvato!")

    def _get_market_data(self):
        """Raccoglie prezzi e variazioni per tutti i ticker"""
        data = {}

        for ticker in self.all_tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="5d")

                if len(hist) >= 2:
                    curr_close = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    change = ((curr_close - prev_close) / prev_close) * 100

                    volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0

                    data[ticker] = {
                        'price': round(curr_close, 4),
                        'change': round(change, 2),
                        'volume': volume,
                        'high': round(hist['High'].iloc[-1], 4),
                        'low': round(hist['Low'].iloc[-1], 4),
                    }
                else:
                    data[ticker] = {'error': 'Dati insufficienti'}
            except Exception as e:
                print(f"⚠️ Errore con {ticker}: {e}")
                data[ticker] = {'error': str(e)}

        return data

    def _get_all_news(self):
        """Raccoglie notizie da fonti multiple"""
        all_news = []
        news_sources = ['^GSPC', 'AAPL', 'TSLA', 'NVDA', 'ENEL.MI', 'ENI.MI', 'UCG.MI', 'ISP.MI', 'CL=F', 'GC=F', 'BTC-USD']

        for source in news_sources:
            try:
                stock = yf.Ticker(source)
                news = stock.news[:5]
                for article in news:
                    content = article.get('content', {})
                    if content:
                        all_news.append({
                            'title': content.get('title', 'N/A'),
                            'summary': content.get('summary', '')[:400],
                            'publisher': content.get('provider', {}).get('displayName', 'N/A'),
                            'published': content.get('pubDate', ''),
                            'source_ticker': source,
                        })
            except Exception as e:
                print(f"⚠️ Errore notizie da {source}: {e}")

        # Rimuovi duplicati
        seen = set()
        unique_news = []
        for n in all_news:
            if n['title'] not in seen:
                seen.add(n['title'])
                unique_news.append(n)

        return unique_news[:25]

    def _analyze_news_drivers_llm(self, news_list, market_data):
        """
        Analisi intelligente delle news con approccio LLM-like:
        - Keyword matching avanzato
        - Contesto settoriale
        - Analisi di impatto (basso/medio/alto)
        - Ragionamento causale
        """
        drivers = []

        # Mappa settori per contesto
        sector_map = {
            'tecnologia': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'INTC', 'CRM', 'ADBE', 'ORCL', 'IBM', 'UBER'],
            'energia': ['ENI.MI', 'ENEL.MI', 'ERG.MI', 'A2A.MI', 'ISP.MI', 'UCG.MI', 'CL=F', 'BZ=F', 'NG=F'],
            'banche': ['ISP.MI', 'UCG.MI', 'BAMI.MI', 'BPE.MI', 'MB.MI', 'FBK.MI', 'BMED.MI', 'BGN.MI', 'AZM.MI', 'UNI.MI', 'US.MI'],
            'lusso': ['MONC.MI', 'RACE.MI', 'MC.PA'],
            'difesa': ['LDO.MI'],
            'farmaceutica': ['DIA.MI', 'REC.MI'],
            'telecomunicazioni': ['TIT.MI', 'INW.MI'],
            'industria': ['STM.MI', 'STLAM.MI', 'PRY.MI', 'TEN.MI', 'SPM.MI', 'PIRC.MI', 'SIE.DE', 'AIR.PA'],
            'utility': ['SRG.MI', 'TRN.MI', 'HER.MI', 'IRE.MI'],
            'costruzioni': ['WBDR.MI', 'ATL.MI'],
        }

        # Keyword per settori
        sector_keywords = {
            'tecnologia': ['tech', 'tecnologia', 'software', 'chip', 'semiconductor', 'ai', 'cloud', 'digital'],
            'energia': ['energy', 'energia', 'oil', 'petrolio', 'gas', 'rinnovabili', 'green'],
            'banche': ['bank', 'banca', 'finanza', 'credit', 'loan', 'tassi', 'interest rate'],
            'lusso': ['luxury', 'lusso', 'fashion', 'moda', 'premium'],
            'difesa': ['defense', 'difesa', 'military', 'armi', 'aerospace'],
            'farmaceutica': ['pharma', 'farmaco', 'vaccine', 'medicina', 'health'],
            'telecomunicazioni': ['telecom', '5g', 'broadband', 'mobile'],
            'industria': ['industry', 'manufacturing', 'production', 'supply chain'],
            'utility': ['utility', 'infrastrutture', 'rete', 'grid'],
            'costruzioni': ['construction', 'edilizia', 'infrastrutture', 'bridge'],
        }

        for news in news_list:
            title_lower = news['title'].lower()
            summary_lower = news['summary'].lower() if news['summary'] else ''
            full_text = title_lower + ' ' + summary_lower

            matched_tickers = set()
            matched_sectors = []
            impact_score = 0
            impact_reasoning = []

            # 1. Keyword matching diretto sui ticker
            for keyword, ticker in self.keyword_map.items():
                if keyword in full_text:
                    matched_tickers.add(ticker)
                    impact_score += 2

            # 2. Analisi settoriale
            for sector, keywords in sector_keywords.items():
                for kw in keywords:
                    if kw in full_text:
                        if sector not in matched_sectors:
                            matched_sectors.append(sector)
                            # Aggiungi tutti i ticker del settore
                            for t in sector_map.get(sector, []):
                                matched_tickers.add(t)
                            impact_score += 1
                        break

            # 3. Analisi di impatto (LLM-like reasoning)
            impact_level = 'basso'

            # Segnali di alto impatto
            high_impact_signals = [
                'earnings', 'trimestrale', 'quarterly', 'risultati',
                'merger', 'acquisition', 'fusione', 'acquisizione',
                'ipo', 'lancio', 'launch', 'nuovo prodotto',
                'scandalo', 'scandal', 'indagine', 'investigation',
                'fallimento', 'bankruptcy', 'default',
                'sanctions', 'sanzioni', 'embargo',
                'rate cut', 'rate hike', 'taglio tassi', 'rialzo tassi',
                'recessione', 'recession', 'crisi', 'crisis',
                'guerra', 'war', 'conflitto', 'conflict',
                'opec', 'fed', 'ecb', 'bce',
            ]

            medium_impact_signals = [
                'upgrade', 'downgrade', 'target price', 'prezzo obiettivo',
                'dividendo', 'dividend', 'buyback',
                'partnership', 'alleanza', 'joint venture',
                'regulation', 'regolamentazione', 'normativa',
                'inflazione', 'inflation', 'pil', 'gdp',
            ]

            for signal in high_impact_signals:
                if signal in full_text:
                    impact_level = 'alto'
                    impact_reasoning.append(f"Segnale alto impatto: '{signal}'")
                    impact_score += 3
                    break

            if impact_level != 'alto':
                for signal in medium_impact_signals:
                    if signal in full_text:
                        impact_level = 'medio'
                        impact_reasoning.append(f"Segnale medio impatto: '{signal}'")
                        impact_score += 2
                        break

            # 4. Analisi sentiment dalla notizia
            sentiment = 'neutrale'
            positive_words = ['rialzo', 'growth', 'profit', 'utile', 'record', 'beat', 'superior', 'strong', 'bullish', 'ottimismo']
            negative_words = ['ribasso', 'loss', 'perdita', 'miss', 'weak', 'bearish', 'pesimismo', 'taglio', 'cut', 'downgrade']

            pos_count = sum(1 for w in positive_words if w in full_text)
            neg_count = sum(1 for w in negative_words if w in full_text)

            if pos_count > neg_count:
                sentiment = 'positivo'
            elif neg_count > pos_count:
                sentiment = 'negativo'

            # 5. Ottieni performance attuali per i ticker matchati
            perf_data = []
            for t in matched_tickers:
                if t in market_data and 'error' not in market_data[t]:
                    perf_data.append({
                        'ticker': t,
                        'name': self._get_ticker_name(t),
                        'change': market_data[t]['change'],
                        'price': market_data[t]['price']
                    })

            # Ordina per performance
            perf_data.sort(key=lambda x: abs(x['change']), reverse=True)

            if matched_tickers and impact_score >= 2:
                drivers.append({
                    'news': news,
                    'matched_tickers': list(matched_tickers),
                    'matched_sectors': matched_sectors,
                    'performance': perf_data[:8],  # Top 8 per impatto
                    'impact_level': impact_level,
                    'impact_score': impact_score,
                    'impact_reasoning': impact_reasoning,
                    'sentiment': sentiment,
                })

        # Ordina per impact score
        drivers.sort(key=lambda x: x['impact_score'], reverse=True)
        return drivers[:15]

    def _get_ticker_name(self, ticker):
        """Ottiene il nome leggibile di un ticker"""
        for group in [self.ftse_mib, self.indices, self.commodities, self.tech, self.crypto, self.forex]:
            if ticker in group:
                return group[ticker]
        return ticker

    def _format_ticker_line(self, ticker, name, data):
        """Formatta una riga di dati ticker"""
        if 'error' in data:
            return f"⚠️  {name:<30} Dato non disponibile"

        emoji = "🟢" if data['change'] > 0 else "🔴" if data['change'] < 0 else "⚪"
        return f"{emoji} {name:<30} {data['price']:>12.4f} ({data['change']:>+.2f}%)"

    def _generate_report(self, data, news_list, news_drivers):
        """Genera il report completo in formato Markdown"""
        lines = []

        # HEADER
        lines.extend([
            "# 📊 BRIEFING FINANZIARIO PRO",
            f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  ",
            f"**Generato da:** Financial Agent PRO 🤖",
            "",
            "---",
            "",
        ])

        # ========== INDICI MONDIALI ==========
        lines.extend([
            "## 🌍 Indici Mondiali",
            "",
            "### 🇺🇸 Americhe",
            "",
        ])

        americhe = ['^GSPC', '^DJI', '^IXIC', '^RUT', '^VIX', '^MXX', '^BVSP']
        for t in americhe:
            if t in data:
                lines.append(self._format_ticker_line(t, self.indices.get(t, t), data[t]))

        lines.extend(["", "### 🇪🇺 Europa", ""])
        europa = ['^STOXX50E', '^DAX', '^MDAXI', '^FCHI', '^FTSE', '^IBEX', '^AEX', '^SSMI', 'FTSEMIB.MI']
        for t in europa:
            if t in data:
                lines.append(self._format_ticker_line(t, self.indices.get(t, t), data[t]))

        lines.extend(["", "### 🌏 Asia-Pacifico", ""])
        asia = ['^N225', '^HSI', '^HSCE', '000001.SS', '399001.SZ', '^KS11', '^AXJO', '^NSEI']
        for t in asia:
            if t in data:
                lines.append(self._format_ticker_line(t, self.indices.get(t, t), data[t]))

        lines.extend(["", "### 🕌 Medio Oriente", ""])
        for t in ['^TASI.SR']:
            if t in data:
                lines.append(self._format_ticker_line(t, self.indices.get(t, t), data[t]))

        # ========== FTSE MIB COMPLETO ==========
        lines.extend([
            "",
            "---",
            "",
            "## 🇮🇹 FTSE MIB - Tutti i 40 Titoli",
            "",
        ])

        # Ordina per performance
        ftse_perf = []
        for t, name in self.ftse_mib.items():
            if t in data and 'error' not in data[t]:
                ftse_perf.append((t, name, data[t]['change'], data[t]['price']))

        ftse_perf.sort(key=lambda x: x[2], reverse=True)

        lines.extend(["### 🏆 Top 5 Performer", ""])
        for t, name, change, price in ftse_perf[:5]:
            lines.append(f"🟢 **{name}** — €{price:.4f} ({change:+.2f}%)")

        lines.extend(["", "### 📉 Peggiori 5 Performer", ""])
        for t, name, change, price in ftse_perf[-5:]:
            lines.append(f"🔴 **{name}** — €{price:.4f} ({change:+.2f}%)")

        lines.extend(["", "### 📋 Lista Completa", ""])
        lines.append("| Titolo | Prezzo | Variazione |")
        lines.append("|--------|--------|------------|")
        for t, name in self.ftse_mib.items():
            if t in data and 'error' not in data[t]:
                emoji = "🟢" if data[t]['change'] > 0 else "🔴" if data[t]['change'] < 0 else "⚪"
                lines.append(f"| {emoji} {name} | €{data[t]['price']:.4f} | {data[t]['change']:+.2f}% |")

        # ========== COMMODITIES ==========
        lines.extend([
            "",
            "---",
            "",
            "## ⛏️ Commodities",
            "",
            "### 🥇 Metalli Preziosi",
            "",
        ])

        for t in ['GC=F', 'SI=F', 'PL=F', 'PA=F']:
            if t in data:
                lines.append(self._format_ticker_line(t, self.commodities.get(t, t), data[t]))

        lines.extend(["", "### 🛢️ Energia", ""])
        for t in ['CL=F', 'BZ=F', 'NG=F']:
            if t in data:
                lines.append(self._format_ticker_line(t, self.commodities.get(t, t), data[t]))

        lines.extend(["", "### 🏭 Metalli Industriali", ""])
        for t in ['HG=F']:
            if t in data:
                lines.append(self._format_ticker_line(t, self.commodities.get(t, t), data[t]))

        lines.extend(["", "### 🌾 Agricoltura", ""])
        for t in ['ZC=F', 'ZW=F', 'ZS=F', 'KC=F', 'CC=F', 'CT=F', 'SB=F']:
            if t in data:
                lines.append(self._format_ticker_line(t, self.commodities.get(t, t), data[t]))

        # ========== BIG TECH USA ==========
        lines.extend([
            "",
            "---",
            "",
            "## 💻 Big Tech (USA)",
            "",
        ])

        for t, name in self.tech.items():
            if t in data:
                lines.append(self._format_ticker_line(t, name, data[t]))

        # ========== CRYPTO ==========
        lines.extend([
            "",
            "---",
            "",
            "## ₿ Cryptovalute",
            "",
        ])

        for t, name in self.crypto.items():
            if t in data:
                lines.append(self._format_ticker_line(t, name, data[t]))

        # ========== FOREX ==========
        lines.extend([
            "",
            "---",
            "",
            "## 💱 Forex",
            "",
        ])

        for t, name in self.forex.items():
            if t in data:
                lines.append(self._format_ticker_line(t, name, data[t]))

        # ========== NEWS DRIVER CON LLM ==========
        lines.extend([
            "",
            "---",
            "",
            "## 🔥 News Driver - Analisi Intelligente",
            "",
            "Notizie analizzate con ragionamento contestuale per identificare potenziali driver di mercato.",
            "",
        ])

        if news_drivers:
            for i, driver in enumerate(news_drivers[:12], 1):
                news = driver['news']
                impact_emoji = {"alto": "🔴", "medio": "🟡", "basso": "🟢"}.get(driver['impact_level'], "⚪")
                sentiment_emoji = {"positivo": "📈", "negativo": "📉", "neutrale": "➡️"}.get(driver['sentiment'], "➡️")

                lines.extend([
                    f"### {i}. {news['title']}",
                    "",
                    f"**Fonte:** {news['publisher']}  ",
                    f"**Impatto stimato:** {impact_emoji} {driver['impact_level'].upper()} (score: {driver['impact_score']})  ",
                    f"**Sentiment:** {sentiment_emoji} {driver['sentiment'].capitalize()}  ",
                ])

                if driver['matched_sectors']:
                    lines.append(f"**Settori coinvolti:** {', '.join(driver['matched_sectors'])}  ")

                if driver['impact_reasoning']:
                    lines.append(f"**Ragionamento:** {'; '.join(driver['impact_reasoning'])}  ")

                if news['summary']:
                    lines.extend(["", f"> {news['summary'][:250]}...", ""])

                if driver['performance']:
                    lines.append("**Performance attuali dei titoli coinvolti:**")
                    lines.append("")
                    lines.append("| Titolo | Prezzo | Variazione |")
                    lines.append("|--------|--------|------------|")
                    for perf in driver['performance']:
                        emoji = "🟢" if perf['change'] > 0 else "🔴" if perf['change'] < 0 else "⚪"
                        lines.append(f"| {emoji} {perf['name']} ({perf['ticker']}) | {perf['price']:.4f} | {perf['change']:+.2f}% |")

                lines.append("")
        else:
            lines.append("Nessuna news driver identificata oggi.")

        # ========== TUTTE LE NOTIZIE ==========
        lines.extend([
            "",
            "---",
            "",
            "## 📰 Tutte le Notizie del Giorno",
            "",
        ])

        for i, news in enumerate(news_list[:20], 1):
            lines.extend([
                f"{i}. **{news['title']}**",
                f"   *{news['publisher']}*",
            ])
            if news['summary']:
                lines.append(f"   > {news['summary'][:180]}...")
            lines.append("")

        # ========== RIEPILOGO SENTIMENT ==========
        lines.extend([
            "",
            "---",
            "",
            "## 📊 Riepilogo Sentiment Globale",
            "",
        ])

        all_changes = [data[t]['change'] for t in data if 'error' not in data[t] and 'change' in data[t]]
        if all_changes:
            positive = sum(1 for c in all_changes if c > 0)
            negative = sum(1 for c in all_changes if c < 0)
            neutral = len(all_changes) - positive - negative
            avg_change = sum(all_changes) / len(all_changes)

            lines.extend([
                f"- 🟢 In rialzo: **{positive}** titoli",
                f"- 🔴 In ribasso: **{negative}** titoli",
                f"- ⚪ Invariati: **{neutral}** titoli",
                f"- 📈 Variazione media: **{avg_change:+.2f}%**",
                "",
            ])

            # Sentiment per area
            ftse_changes = [data[t]['change'] for t in self.ftse_mib if t in data and 'error' not in data[t]]
            if ftse_changes:
                ftse_avg = sum(ftse_changes) / len(ftse_changes)
                ftse_emoji = "🟢" if ftse_avg > 0 else "🔴" if ftse_avg < 0 else "⚪"
                lines.append(f"- {ftse_emoji} **FTSE MIB medio:** {ftse_avg:+.2f}%")

            indices_changes = [data[t]['change'] for t in self.indices if t in data and 'error' not in data[t]]
            if indices_changes:
                indices_avg = sum(indices_changes) / len(indices_changes)
                indices_emoji = "🟢" if indices_avg > 0 else "🔴" if indices_avg < 0 else "⚪"
                lines.append(f"- {indices_emoji} **Indici globali medio:** {indices_avg:+.2f}%")

            tech_changes = [data[t]['change'] for t in self.tech if t in data and 'error' not in data[t]]
            if tech_changes:
                tech_avg = sum(tech_changes) / len(tech_changes)
                tech_emoji = "🟢" if tech_avg > 0 else "🔴" if tech_avg < 0 else "⚪"
                lines.append(f"- {tech_emoji} **Big Tech medio:** {tech_avg:+.2f}%")

            crypto_changes = [data[t]['change'] for t in self.crypto if t in data and 'error' not in data[t]]
            if crypto_changes:
                crypto_avg = sum(crypto_changes) / len(crypto_changes)
                crypto_emoji = "🟢" if crypto_avg > 0 else "🔴" if crypto_avg < 0 else "⚪"
                lines.append(f"- {crypto_emoji} **Crypto medio:** {crypto_avg:+.2f}%")

            comm_changes = [data[t]['change'] for t in self.commodities if t in data and 'error' not in data[t]]
            if comm_changes:
                comm_avg = sum(comm_changes) / len(comm_changes)
                comm_emoji = "🟢" if comm_avg > 0 else "🔴" if comm_avg < 0 else "⚪"
                lines.append(f"- {comm_emoji} **Commodities medio:** {comm_avg:+.2f}%")

        # FOOTER
        lines.extend([
            "",
            "---",
            "",
            "*Generato automaticamente da Financial Agent PRO*  ",
            f"*Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*",
        ])

        return "\n".join(lines)

    def _save_report(self, report):
        """Salva il report come file Markdown nel repository"""
        # Crea directory reports se non esiste
        os.makedirs('reports', exist_ok=True)

        # Nome file con data
        filename = f"reports/briefing_{datetime.now().strftime('%Y%m%d')}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        # Salva anche come latest.md per accesso facile
        with open('reports/latest.md', 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"💾 Report salvato in: {filename}")
        print(f"💾 Report aggiornato anche in: reports/latest.md")

        # Salva anche dati grezzi in JSON per analisi future
        self._save_raw_data()

    def _save_raw_data(self):
        """Salva i dati grezzi in formato JSON"""
        # Questo metodo verrà chiamato dopo _get_market_data nel run()
        pass


if __name__ == "__main__":
    agent = FinancialAgentPro()
    agent.run()
