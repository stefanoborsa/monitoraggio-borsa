#!/usr/bin/env python3
"""
Financial Agent PRO IT - Briefing completo con focus Italia
Mercati: FTSE MIB completo (40 titoli), Indici mondiali, Commodities, Crypto
Analisi: News driver con focus Italia, direzione movimento (BUY/SELL/NEUTRAL)
Output: Report salvato come file Markdown nel repository
Esecuzione: python3 daily_finance_pro_it.py
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import json
import re

class FinancialAgentProIT:
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
            '^GSPC': 'S&P 500 (USA)',
            '^DJI': 'Dow Jones (USA)',
            '^IXIC': 'Nasdaq (USA)',
            '^RUT': 'Russell 2000 (USA)',
            '^VIX': 'VIX (Volatilità)',
            '^MXX': 'IPC (Messico)',
            '^BVSP': 'Bovespa (Brasile)',
            '^STOXX50E': 'Euro Stoxx 50',
            '^DAX': 'DAX 40 (Germania)',
            '^MDAXI': 'MDAX (Germania)',
            '^FCHI': 'CAC 40 (Francia)',
            '^FTSE': 'FTSE 100 (UK)',
            '^IBEX': 'IBEX 35 (Spagna)',
            '^AEX': 'AEX (Olanda)',
            '^SSMI': 'SMI (Svizzera)',
            'FTSEMIB.MI': 'FTSE MIB (Italia)',
            '^N225': 'Nikkei 225 (Giappone)',
            '^HSI': 'Hang Seng (Hong Kong)',
            '^HSCE': 'Hang Seng China Ent.',
            '000001.SS': 'Shanghai Composite (Cina)',
            '399001.SZ': 'Shenzhen Component (Cina)',
            '^KS11': 'KOSPI (Corea del Sud)',
            '^AXJO': 'ASX 200 (Australia)',
            '^NSEI': 'Nifty 50 (India)',
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

        self.all_tickers = []
        for group in [self.ftse_mib, self.indices, self.commodities, self.tech, self.crypto, self.forex]:
            self.all_tickers.extend(list(group.keys()))

        # ========== MAPPA KEYWORD AVANZATA PER NEWS DRIVER ==========
        self.keyword_map = {
            # Tech USA
            'apple': 'AAPL', 'iphone': 'AAPL', 'mac': 'AAPL', 'ipad': 'AAPL',
            'microsoft': 'MSFT', 'azure': 'MSFT', 'windows': 'MSFT',
            'google': 'GOOGL', 'alphabet': 'GOOGL', 'youtube': 'GOOGL',
            'nvidia': 'NVDA', 'gpu': 'NVDA', 'ai chip': 'NVDA',
            'meta': 'META', 'facebook': 'META', 'instagram': 'META',
            'tesla': 'TSLA', 'elon musk': 'TSLA', 'ev': 'TSLA',
            'amazon': 'AMZN', 'aws': 'AMZN',
            'netflix': 'NFLX',
            'amd': 'AMD', 'intel': 'INTC',

            # ITALIA - Aziende
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
            'diasorin': 'DIA.MI', 'recordati': 'REC.MI',
            'amplifon': 'AMP.MI', 'a2a': 'A2A.MI',
            'banco bpm': 'BAMI.MI', 'bper': 'BPE.MI',
            'finecobank': 'FBK.MI', 'mediobanca': 'MB.MI',
            'azimut': 'AZM.MI', 'banca generali': 'BGN.MI',
            'mediolanum': 'BMED.MI', 'hera': 'HER.MI', 'iren': 'IRE.MI',
            'erg': 'ERG.MI', 'inwit': 'INW.MI',
            'atlantia': 'ATL.MI', 'webuild': 'WBDR.MI',
            'pirelli': 'PIRC.MI',

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

        # ========== MAPPA DIREZIONE MOVIMENTO ==========
        # Keyword che indicano BUY (rialzo atteso)
        self.buy_signals = [
            'upgrade', 'upgraded', 'buy', 'acquisto', 'acquistare', 'strong buy',
            'outperform', 'overweight', 'bullish', 'rialzo', 'rialzista',
            'beat', 'superior', 'migliore', 'migliora', 'miglioramento',
            'growth', 'espansione', 'espande', 'record', 'massimo storico',
            'dividendo aumentato', 'aumento dividendo', 'buyback aumentato',
            'fusione', 'acquisizione', 'merger', 'acquisition',
            'lancio', 'launch', 'nuovo prodotto', 'new product',
            'contratto', 'ordine', 'deal', 'accordo',
            'profitto record', 'utile record', 'record profit',
            'supera attese', 'beats estimates', 'above expectations',
            'target price raised', 'prezzo obiettivo rialzato', 'price target up',
            'outlook positivo', 'guidance raised', 'guidance rialzata',
            'espansione internazionale', 'international expansion',
            'innovazione', 'brevetto', 'patent',
            'sottovalutato', 'undervalued', 'bargain',
            'momentum positivo', 'trend rialzista', 'uptrend',
            'supporto tecnico', 'technical support',
            'accumulo', 'accumulation',
        ]

        # Keyword che indicano SELL (ribasso atteso)
        self.sell_signals = [
            'downgrade', 'downgraded', 'sell', 'vendita', 'vendere', 'strong sell',
            'underperform', 'underweight', 'bearish', 'ribasso', 'ribassista',
            'miss', 'inferiore', 'peggio', 'peggioramento', 'delude',
            'loss', 'perdita', 'perdite', 'losses', 'red ink',
            'fallimento', 'bankruptcy', 'default', 'crisi', 'crisis',
            'scandalo', 'scandal', 'indagine', 'investigation', 'inchiesta',
            'licenziamenti', 'layoffs', 'taglio posti', 'job cuts',
            'profit warning', 'allarme utili', 'warning',
            'target price cut', 'prezzo obiettivo tagliato', 'price target down',
            'outlook negativo', 'guidance cut', 'guidance tagliata',
            'recessione', 'recession', 'contrazione', 'contraction',
            'debito elevato', 'high debt', 'leverage',
            'sovrapprezzo', 'overvalued', 'bolla', 'bubble',
            'momentum negativo', 'trend ribassista', 'downtrend',
            'resistenza', 'resistance', 'rifiuto',
            'distribuzione', 'distribution',
            'sanctions', 'sanzioni', 'embargo', 'ban',
            'richiamo', 'recall', 'problema qualità', 'quality issue',
            'causa legale', 'lawsuit', 'litigio',
        ]

        # Keyword NEUTRAL (mantenere/attendere)
        self.neutral_signals = [
            'hold', 'mantenere', 'neutral', 'neutrale',
            'in linea', 'inline', 'as expected', 'come atteso',
            'stable', 'stabile', 'flat', 'laterale',
            'mixed', 'misto', 'mixed results',
            'attesa', 'wait', 'pending', 'in sospeso',
            'valutazione', 'review', 'under review',
            'conferma', 'confirmed', 'unchanged', 'invariato',
            'consolidamento', 'consolidation',
        ]

    def run(self):
        print(f"🤖 Financial Agent PRO IT avviato alle {datetime.now().strftime('%H:%M:%S')}")

        print("📊 Raccogliendo dati di mercato...")
        market_data = self._get_market_data()

        print("📰 Raccogliendo notizie (focus Italia)...")
        all_news = self._get_all_news()

        print("🔍 Analizzando news driver con direzione...")
        news_drivers = self._analyze_news_drivers_advanced(all_news, market_data)

        print("📝 Generando report...")
        report = self._generate_report(market_data, all_news, news_drivers)

        self._save_report(report)

        print("✅ Briefing PRO IT completato e salvato!")

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
        """Raccoglie notizie con FOCUS ITALIA da fonti multiple"""
        all_news = []

        # FONTI CON FOCUS ITALIA (priorità alta)
        italian_sources = [
            'ENEL.MI', 'ENI.MI', 'UCG.MI', 'ISP.MI', 'RACE.MI', 'STLAM.MI',
            'LDO.MI', 'PRY.MI', 'MONC.MI', 'G.MI', 'SRG.MI', 'TRN.MI',
            'TIT.MI', 'STM.MI', 'DIA.MI', 'REC.MI', 'NEXI.MI',
            'BAMI.MI', 'BPE.MI', 'MB.MI', 'FBK.MI', 'BMED.MI',
            'A2A.MI', 'HER.MI', 'IRE.MI', 'ERG.MI', 'AMP.MI',
            'FTSEMIB.MI',
        ]

        # Fonti globali (priorità media)
        global_sources = ['^GSPC', 'AAPL', 'TSLA', 'NVDA', 'CL=F', 'GC=F', 'BTC-USD']

        # PRIORITÀ 1: Notizie italiane
        print("  🇮🇹 Raccogliendo notizie italiane...")
        for source in italian_sources:
            try:
                stock = yf.Ticker(source)
                news = stock.news[:3]
                for article in news:
                    content = article.get('content', {})
                    if content:
                        all_news.append({
                            'title': content.get('title', 'N/A'),
                            'summary': content.get('summary', '')[:500],
                            'publisher': content.get('provider', {}).get('displayName', 'N/A'),
                            'published': content.get('pubDate', ''),
                            'source_ticker': source,
                            'priority': 'high',  # Priorità alta per notizie italiane
                        })
            except Exception as e:
                pass

        # PRIORITÀ 2: Notizie globali
        print("  🌍 Raccogliendo notizie globali...")
        for source in global_sources:
            try:
                stock = yf.Ticker(source)
                news = stock.news[:2]
                for article in news:
                    content = article.get('content', {})
                    if content:
                        all_news.append({
                            'title': content.get('title', 'N/A'),
                            'summary': content.get('summary', '')[:500],
                            'publisher': content.get('provider', {}).get('displayName', 'N/A'),
                            'published': content.get('pubDate', ''),
                            'source_ticker': source,
                            'priority': 'medium',
                        })
            except Exception as e:
                pass

        # Rimuovi duplicati mantenendo priorità alta
        seen = set()
        unique_news = []
        # Ordina per priorità (high prima)
        all_news.sort(key=lambda x: 0 if x['priority'] == 'high' else 1)

        for n in all_news:
            if n['title'] not in seen:
                seen.add(n['title'])
                unique_news.append(n)

        return unique_news[:30]

    def _analyze_direction(self, title, summary):
        """
        Determina la direzione del movimento atteso: BUY / SELL / NEUTRAL
        Basato su analisi linguistica avanzata
        """
        full_text = (title + ' ' + summary).lower()

        buy_score = 0
        sell_score = 0
        neutral_score = 0
        matched_signals = []

        # Analisi BUY signals
        for signal in self.buy_signals:
            if signal in full_text:
                buy_score += 2
                matched_signals.append(f"BUY signal: '{signal}'")

        # Analisi SELL signals
        for signal in self.sell_signals:
            if signal in full_text:
                sell_score += 2
                matched_signals.append(f"SELL signal: '{signal}'")

        # Analisi NEUTRAL signals
        for signal in self.neutral_signals:
            if signal in full_text:
                neutral_score += 1
                matched_signals.append(f"NEUTRAL signal: '{signal}'")

        # Analisi aggiuntiva per contesto
        # Se menziona "trimestrale" o "earnings" senza altri segnali → NEUTRAL (attesa)
        if 'earnings' in full_text or 'trimestrale' in full_text or 'risultati' in full_text:
            if buy_score == 0 and sell_score == 0:
                neutral_score += 2
                matched_signals.append("NEUTRAL: attesa risultati trimestrali")

        # Se menziona "guidance" o "outlook" → dipende dal contesto
        if 'guidance' in full_text or 'outlook' in full_text or 'previsioni' in full_text:
            if 'raise' in full_text or 'rialzata' in full_text or 'up' in full_text or 'aumenta' in full_text:
                buy_score += 3
                matched_signals.append("BUY: guidance rialzata")
            elif 'cut' in full_text or 'tagliata' in full_text or 'down' in full_text or 'riduce' in full_text:
                sell_score += 3
                matched_signals.append("SELL: guidance tagliata")

        # Se menziona "target price" → analizza direzione
        if 'target price' in full_text or 'prezzo obiettivo' in full_text:
            if 'raise' in full_text or 'rialzato' in full_text or 'up' in full_text or 'aumenta' in full_text:
                buy_score += 2
                matched_signals.append("BUY: target price rialzato")
            elif 'cut' in full_text or 'tagliato' in full_text or 'down' in full_text or 'ridotto' in full_text:
                sell_score += 2
                matched_signals.append("SELL: target price tagliato")

        # Determina direzione
        if buy_score > sell_score and buy_score > neutral_score:
            return 'BUY', buy_score, matched_signals
        elif sell_score > buy_score and sell_score > neutral_score:
            return 'SELL', sell_score, matched_signals
        else:
            return 'NEUTRAL', neutral_score, matched_signals

    def _analyze_news_drivers_advanced(self, news_list, market_data):
        """
        Analisi avanzata delle news con focus Italia e direzione movimento
        """
        drivers = []

        # Mappa settori
        sector_map = {
            'tecnologia': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'INTC', 'CRM', 'ADBE', 'ORCL', 'IBM', 'UBER', 'STM.MI'],
            'energia': ['ENI.MI', 'ENEL.MI', 'ERG.MI', 'A2A.MI', 'SRG.MI', 'CL=F', 'BZ=F', 'NG=F'],
            'banche': ['ISP.MI', 'UCG.MI', 'BAMI.MI', 'BPE.MI', 'MB.MI', 'FBK.MI', 'BMED.MI', 'BGN.MI', 'AZM.MI', 'UNI.MI', 'US.MI'],
            'lusso': ['MONC.MI', 'RACE.MI'],
            'difesa': ['LDO.MI'],
            'farmaceutica': ['DIA.MI', 'REC.MI'],
            'telecomunicazioni': ['TIT.MI', 'INW.MI'],
            'industria': ['STM.MI', 'STLAM.MI', 'PRY.MI', 'TEN.MI', 'SPM.MI', 'PIRC.MI'],
            'utility': ['SRG.MI', 'TRN.MI', 'HER.MI', 'IRE.MI', 'A2A.MI'],
            'costruzioni': ['WBDR.MI', 'ATL.MI'],
            'assicurazioni': ['G.MI', 'UNI.MI', 'US.MI'],
        }

        sector_keywords = {
            'tecnologia': ['tech', 'tecnologia', 'software', 'chip', 'semiconductor', 'ai', 'cloud', 'digital', 'tecnologico'],
            'energia': ['energy', 'energia', 'oil', 'petrolio', 'gas', 'rinnovabili', 'green', 'elettricità'],
            'banche': ['bank', 'banca', 'finanza', 'credit', 'loan', 'tassi', 'interest rate', 'bancario'],
            'lusso': ['luxury', 'lusso', 'fashion', 'moda', 'premium', 'alta gamma'],
            'difesa': ['defense', 'difesa', 'military', 'armi', 'aerospace', 'aerospazio'],
            'farmaceutica': ['pharma', 'farmaco', 'vaccine', 'medicina', 'health', 'salute'],
            'telecomunicazioni': ['telecom', '5g', 'broadband', 'mobile', 'telefonia'],
            'industria': ['industry', 'manufacturing', 'production', 'supply chain', 'industriale'],
            'utility': ['utility', 'infrastrutture', 'rete', 'grid', 'distribuzione'],
            'costruzioni': ['construction', 'edilizia', 'infrastrutture', 'bridge', 'ponte'],
            'assicurazioni': ['insurance', 'assicurazione', 'assicurativo', 'premio'],
        }

        for news in news_list:
            title_lower = news['title'].lower()
            summary_lower = news['summary'].lower() if news['summary'] else ''
            full_text = title_lower + ' ' + summary_lower

            matched_tickers = set()
            matched_sectors = []
            impact_score = 0
            impact_reasoning = []

            # 1. Keyword matching diretto
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
                            for t in sector_map.get(sector, []):
                                matched_tickers.add(t)
                            impact_score += 1
                        break

            # 3. Analisi di impatto
            impact_level = 'basso'

            high_impact_signals = [
                'earnings', 'trimestrale', 'quarterly', 'risultati',
                'merger', 'acquisition', 'fusione', 'acquisizione',
                'ipo', 'lancio', 'launch', 'nuovo prodotto',
                'scandalo', 'scandal', 'indagine', 'investigation',
                'fallimento', 'bankruptcy', 'default',
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

            # 4. Analisi direzione movimento (BUY/SELL/NEUTRAL)
            direction, direction_score, direction_signals = self._analyze_direction(news['title'], news['summary'])

            # 5. Ottieni performance attuali
            perf_data = []
            for t in matched_tickers:
                if t in market_data and 'error' not in market_data[t]:
                    perf_data.append({
                        'ticker': t,
                        'name': self._get_ticker_name(t),
                        'change': market_data[t]['change'],
                        'price': market_data[t]['price']
                    })

            perf_data.sort(key=lambda x: abs(x['change']), reverse=True)

            # Filtra: includi solo se ha impatto significativo
            if matched_tickers and (impact_score >= 3 or news['priority'] == 'high'):
                drivers.append({
                    'news': news,
                    'matched_tickers': list(matched_tickers),
                    'matched_sectors': matched_sectors,
                    'performance': perf_data[:6],
                    'impact_level': impact_level,
                    'impact_score': impact_score,
                    'impact_reasoning': impact_reasoning,
                    'direction': direction,
                    'direction_score': direction_score,
                    'direction_signals': direction_signals,
                    'is_italian': news['priority'] == 'high',
                })

        # Ordina: italiani prima, poi per impact score
        drivers.sort(key=lambda x: (0 if x['is_italian'] else 1, -x['impact_score']))
        return drivers[:15]

    def _get_ticker_name(self, ticker):
        for group in [self.ftse_mib, self.indices, self.commodities, self.tech, self.crypto, self.forex]:
            if ticker in group:
                return group[ticker]
        return ticker

    def _format_ticker_line(self, ticker, name, data):
        if 'error' in data:
            return f"⚠️  {name:<30} Dato non disponibile"

        emoji = "🟢" if data['change'] > 0 else "🔴" if data['change'] < 0 else "⚪"
        return f"{emoji} {name:<30} {data['price']:>12.4f} ({data['change']:>+.2f}%)"

    def _generate_report(self, data, news_list, news_drivers):
        lines = []

        # HEADER
        lines.extend([
            "# 📊 BRIEFING FINANZIARIO PRO - EDIZIONE ITALIA",
            f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  ",
            f"**Generato da:** Financial Agent PRO IT 🤖",
            "",
            "---",
            "",
        ])

        # ========== RIEPILOGO RAPIDO FTSE MIB ==========
        lines.extend([
            "## 🇮🇹 Panoramica FTSE MIB",
            "",
        ])

        ftse_perf = []
        for t, name in self.ftse_mib.items():
            if t in data and 'error' not in data[t]:
                ftse_perf.append((t, name, data[t]['change'], data[t]['price']))

        ftse_perf.sort(key=lambda x: x[2], reverse=True)

        lines.extend(["### 🏆 Top 5", ""])
        for t, name, change, price in ftse_perf[:5]:
            lines.append(f"🟢 **{name}** — €{price:.4f} ({change:+.2f}%)")

        lines.extend(["", "### 📉 Peggiori 5", ""])
        for t, name, change, price in ftse_perf[-5:]:
            lines.append(f"🔴 **{name}** — €{price:.4f} ({change:+.2f}%)")

        # ========== NEWS DRIVER ITALIANE (PRIORITÀ ALTA) ==========
        italian_drivers = [d for d in news_drivers if d['is_italian']]
        global_drivers = [d for d in news_drivers if not d['is_italian']]

        lines.extend([
            "",
            "---",
            "",
            "## 🔥 NEWS DRIVER - FOCUS ITALIA",
            "",
            "Analisi intelligente delle notizie con direzione movimento stimata.",
            "",
            "**Legenda direzione:** 🟢 BUY (rialzo atteso) | 🔴 SELL (ribasso atteso) | ⚪ NEUTRAL (attendere)",
            "",
        ])

        if italian_drivers:
            lines.append(f"### 🇮🇹 Notizie Italiane ({len(italian_drivers)})")
            lines.append("")

            for i, driver in enumerate(italian_drivers, 1):
                news = driver['news']

                # Emoji direzione
                direction_emoji = {"BUY": "🟢", "SELL": "🔴", "NEUTRAL": "⚪"}.get(driver['direction'], "⚪")
                impact_emoji = {"alto": "🔴", "medio": "🟡", "basso": "🟢"}.get(driver['impact_level'], "⚪")

                lines.extend([
                    f"#### {i}. {direction_emoji} {driver['direction']} | {news['title']}",
                    "",
                    f"**Fonte:** {news['publisher']}  ",
                    f"**Impatto:** {impact_emoji} {driver['impact_level'].upper()} (score: {driver['impact_score']})  ",
                    f"**Direzione:** {direction_emoji} **{driver['direction']}** (confidenza: {driver['direction_score']})  ",
                ])

                if driver['matched_sectors']:
                    lines.append(f"**Settori:** {', '.join(driver['matched_sectors'])}  ")

                if driver['direction_signals']:
                    lines.append(f"**Ragionamento:** {'; '.join(driver['direction_signals'][:3])}  ")

                if news['summary']:
                    lines.extend(["", f"> {news['summary'][:280]}...", ""])

                if driver['performance']:
                    lines.append("**Performance attuali:**")
                    lines.append("")
                    lines.append("| Titolo | Prezzo | Variazione |")
                    lines.append("|--------|--------|------------|")
                    for perf in driver['performance']:
                        emoji = "🟢" if perf['change'] > 0 else "🔴" if perf['change'] < 0 else "⚪"
                        lines.append(f"| {emoji} {perf['name']} ({perf['ticker']}) | {perf['price']:.4f} | {perf['change']:+.2f}% |")

                lines.append("")
        else:
            lines.append("Nessuna news driver italiana identificata oggi.")
            lines.append("")

        # ========== NEWS DRIVER GLOBALI ==========
        if global_drivers:
            lines.extend([
                "### 🌍 Notizie Globali",
                "",
            ])

            for i, driver in enumerate(global_drivers[:5], 1):
                news = driver['news']
                direction_emoji = {"BUY": "🟢", "SELL": "🔴", "NEUTRAL": "⚪"}.get(driver['direction'], "⚪")
                impact_emoji = {"alto": "🔴", "medio": "🟡", "basso": "🟢"}.get(driver['impact_level'], "⚪")

                lines.extend([
                    f"{i}. {direction_emoji} **{driver['direction']}** | {news['title']}",
                    f"   Impatto: {impact_emoji} {driver['impact_level'].upper()} | Fonte: {news['publisher']}",
                ])

                if driver['performance']:
                    perf_strs = []
                    for perf in driver['performance'][:3]:
                        emoji = "🟢" if perf['change'] > 0 else "🔴"
                        perf_strs.append(f"{emoji} {perf['name']} ({perf['change']:+.2f}%)")
                    lines.append(f"   Titoli: {', '.join(perf_strs)}")

                lines.append("")

        # ========== INDICI MONDIALI ==========
        lines.extend([
            "",
            "---",
            "",
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

        # ========== FTSE MIB COMPLETO ==========
        lines.extend([
            "",
            "---",
            "",
            "## 🇮🇹 FTSE MIB - Tutti i 40 Titoli",
            "",
        ])

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

        # ========== TUTTE LE NOTIZIE ==========
        lines.extend([
            "",
            "---",
            "",
            "## 📰 Tutte le Notizie del Giorno",
            "",
        ])

        # Separa notizie italiane e globali
        italian_news = [n for n in news_list if n['priority'] == 'high']
        global_news = [n for n in news_list if n['priority'] == 'medium']

        if italian_news:
            lines.append("### 🇮🇹 Notizie Italiane")
            lines.append("")
            for i, news in enumerate(italian_news[:10], 1):
                lines.extend([
                    f"{i}. **{news['title']}**",
                    f"   *{news['publisher']}*",
                ])
                if news['summary']:
                    lines.append(f"   > {news['summary'][:150]}...")
                lines.append("")

        if global_news:
            lines.append("### 🌍 Notizie Globali")
            lines.append("")
            for i, news in enumerate(global_news[:10], 1):
                lines.extend([
                    f"{i}. **{news['title']}**",
                    f"   *{news['publisher']}*",
                ])
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

            ftse_changes = [data[t]['change'] for t in self.ftse_mib if t in data and 'error' not in data[t]]
            if ftse_changes:
                ftse_avg = sum(ftse_changes) / len(ftse_changes)
                ftse_emoji = "🟢" if ftse_avg > 0 else "🔴"
                lines.append(f"- {ftse_emoji} **FTSE MIB medio:** {ftse_avg:+.2f}%")

            indices_changes = [data[t]['change'] for t in self.indices if t in data and 'error' not in data[t]]
            if indices_changes:
                indices_avg = sum(indices_changes) / len(indices_changes)
                indices_emoji = "🟢" if indices_avg > 0 else "🔴"
                lines.append(f"- {indices_emoji} **Indici globali medio:** {indices_avg:+.2f}%")

            tech_changes = [data[t]['change'] for t in self.tech if t in data and 'error' not in data[t]]
            if tech_changes:
                tech_avg = sum(tech_changes) / len(tech_changes)
                tech_emoji = "🟢" if tech_avg > 0 else "🔴"
                lines.append(f"- {tech_emoji} **Big Tech medio:** {tech_avg:+.2f}%")

            crypto_changes = [data[t]['change'] for t in self.crypto if t in data and 'error' not in data[t]]
            if crypto_changes:
                crypto_avg = sum(crypto_changes) / len(crypto_changes)
                crypto_emoji = "🟢" if crypto_avg > 0 else "🔴"
                lines.append(f"- {crypto_emoji} **Crypto medio:** {crypto_avg:+.2f}%")

            comm_changes = [data[t]['change'] for t in self.commodities if t in data and 'error' not in data[t]]
            if comm_changes:
                comm_avg = sum(comm_changes) / len(comm_changes)
                comm_emoji = "🟢" if comm_avg > 0 else "🔴"
                lines.append(f"- {comm_emoji} **Commodities medio:** {comm_avg:+.2f}%")

        # FOOTER
        lines.extend([
            "",
            "---",
            "",
            "*Generato automaticamente da Financial Agent PRO IT*  ",
            f"*Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*",
        ])

        return "\n".join(lines)

    def _save_report(self, report):
        os.makedirs('reports', exist_ok=True)

        filename = f"reports/briefing_{datetime.now().strftime('%Y%m%d')}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        with open('reports/latest.md', 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"💾 Report salvato in: {filename}")
        print(f"💾 Report aggiornato anche in: reports/latest.md")


if __name__ == "__main__":
    agent = FinancialAgentProIT()
    agent.run()
