#!/usr/bin/env python3
"""
Script de téléchargement de données historiques NQ et ES
Utilise directement l'API Yahoo Finance sans dépendances problématiques
Futures: NQ (Nasdaq-100) et ES (S&P 500)
Timeframes: 1m, 5m, 15m, 1H, 4H, 1D, 1W
Période: 2018 à 2025
"""

import os
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from io import StringIO

import requests
import pandas as pd

# Configuration
DATA_DIR = Path(__file__).parent

# Symboles Yahoo Finance
SYMBOLS = {
    'NQ': 'NQ=F',     # E-mini Nasdaq-100 Futures
    'ES': 'ES=F',     # E-mini S&P 500 Futures
}

# ETFs alternatifs pour historique plus long
SYMBOL_ALTERNATIVES = {
    'NQ': 'QQQ',      # Invesco QQQ Trust (Nasdaq-100)
    'ES': 'SPY',      # SPDR S&P 500 ETF
}

# Intervalles Yahoo Finance et leurs limitations
# - 1m: max 7 jours
# - 2m, 5m, 15m, 30m: max 60 jours
# - 60m, 1h: max 730 jours
# - 1d, 1wk, 1mo: pas de limite
INTERVALS = {
    '1m': {'yahoo': '1m', 'max_days': 7},
    '5m': {'yahoo': '5m', 'max_days': 60},
    '15m': {'yahoo': '15m', 'max_days': 60},
    '1H': {'yahoo': '1h', 'max_days': 730},
    '4H': {'yahoo': '1h', 'max_days': 730, 'aggregate': 4},  # Agrégé depuis 1h
    '1D': {'yahoo': '1d', 'max_days': None},
    '1W': {'yahoo': '1wk', 'max_days': None},
}


class YahooFinanceAPI:
    """Client simple pour l'API Yahoo Finance"""

    BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def download(self, symbol: str, start: datetime, end: datetime, interval: str) -> pd.DataFrame:
        """Télécharge les données historiques"""

        params = {
            'period1': int(start.timestamp()),
            'period2': int(end.timestamp()),
            'interval': interval,
            'includePrePost': 'true',
            'events': 'div,splits',
        }

        url = f"{self.BASE_URL}{symbol}"

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'chart' not in data or 'result' not in data['chart'] or not data['chart']['result']:
                return pd.DataFrame()

            result = data['chart']['result'][0]

            if 'timestamp' not in result:
                return pd.DataFrame()

            timestamps = result['timestamp']
            quotes = result['indicators']['quote'][0]

            df = pd.DataFrame({
                'Datetime': pd.to_datetime(timestamps, unit='s', utc=True),
                'Open': quotes.get('open'),
                'High': quotes.get('high'),
                'Low': quotes.get('low'),
                'Close': quotes.get('close'),
                'Volume': quotes.get('volume'),
            })

            # Convertir en timezone locale et nettoyer
            df['Datetime'] = df['Datetime'].dt.tz_convert('America/New_York').dt.tz_localize(None)
            df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])
            df = df.set_index('Datetime')

            return df

        except Exception as e:
            print(f"  ✗ Erreur API: {e}")
            return pd.DataFrame()


def aggregate_to_4h(df_1h: pd.DataFrame) -> pd.DataFrame:
    """Agrège les données 1H en 4H"""
    if df_1h.empty:
        return pd.DataFrame()

    agg_dict = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }

    df_4h = df_1h.resample('4h').agg(agg_dict).dropna()
    return df_4h


def format_and_save(df: pd.DataFrame, filepath: Path) -> bool:
    """Formate et sauvegarde les données au format CSV du projet"""
    if df.empty:
        return False

    output = df.copy()
    output = output.reset_index()

    # Créer colonnes Date et Time
    output['Date'] = output['Datetime'].dt.strftime('%m/%d/%Y')
    output['Time'] = output['Datetime'].dt.strftime('%H:%M:%S')

    # Réorganiser les colonnes
    output = output[['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']]

    # Sauvegarder avec séparateur ;
    output.to_csv(filepath, sep=';', index=False, header=False)
    print(f"  ✓ Sauvegardé: {filepath.name} ({len(output)} lignes)")
    return True


def download_symbol_data(api: YahooFinanceAPI, symbol: str, ticker: str,
                         interval_name: str, interval_config: dict):
    """Télécharge les données pour un symbole et un intervalle"""

    yahoo_interval = interval_config['yahoo']
    max_days = interval_config.get('max_days')
    aggregate = interval_config.get('aggregate')

    end_date = datetime.now()

    if max_days:
        start_date = end_date - timedelta(days=max_days - 1)
    else:
        start_date = datetime(2018, 1, 1)

    print(f"\n  📊 Téléchargement {interval_name} ({yahoo_interval})...")
    print(f"     Période: {start_date.strftime('%Y-%m-%d')} à {end_date.strftime('%Y-%m-%d')}")

    df = api.download(ticker, start_date, end_date, yahoo_interval)

    if df.empty:
        print(f"  ⚠ Aucune donnée disponible")
        return

    # Agrégation si nécessaire (pour 4H)
    if aggregate:
        df = aggregate_to_4h(df)
        if df.empty:
            return

    # Sauvegarder par année pour NQ, globalement pour ES
    years = df.index.year.unique()

    for year in years:
        year_df = df[df.index.year == year]
        if year_df.empty:
            continue

        if symbol == 'NQ':
            filename = f"{year} {interval_name}.csv"
        else:
            if len(years) > 1:
                filename = f"{symbol} {interval_name.lower()} ({min(years)}-{max(years)}).csv"
            else:
                filename = f"{symbol} {interval_name.lower()} ({year}).csv"

        filepath = DATA_DIR / filename
        format_and_save(year_df, filepath)

        # Pour ES, sauvegarder une seule fois avec toutes les données
        if symbol == 'ES':
            break


def download_all_data(use_alternatives: bool = False):
    """Télécharge toutes les données NQ et ES"""

    symbols = SYMBOL_ALTERNATIVES if use_alternatives else SYMBOLS
    source = "ETFs (QQQ/SPY)" if use_alternatives else "Futures (NQ=F/ES=F)"

    api = YahooFinanceAPI()

    print("\n" + "=" * 60)
    print("TÉLÉCHARGEMENT DES DONNÉES NQ ET ES")
    print(f"Source: {source}")
    print("=" * 60)

    for symbol, ticker in symbols.items():
        print(f"\n{'='*50}")
        print(f"📈 {symbol} ({ticker})")
        print("=" * 50)

        for interval_name, interval_config in INTERVALS.items():
            download_symbol_data(api, symbol, ticker, interval_name, interval_config)
            time.sleep(0.5)  # Rate limiting

        time.sleep(1)


def show_existing_data():
    """Affiche les fichiers de données existants"""
    print("\n📁 FICHIERS DE DONNÉES EXISTANTS:")
    print("-" * 50)

    nq_files = []
    es_files = []
    other_files = []

    for f in sorted(DATA_DIR.glob("*")):
        if f.suffix in ['.csv', '.xlsx', '.zip']:
            size_mb = f.stat().st_size / (1024 * 1024)
            info = f"  {f.name}: {size_mb:.2f} MB"

            if f.name.startswith('ES'):
                es_files.append(info)
            elif f.name[0].isdigit():  # NQ files start with year
                nq_files.append(info)
            else:
                other_files.append(info)

    if nq_files:
        print("\n📊 Données NQ (Nasdaq-100 Futures):")
        for f in nq_files:
            print(f)

    if es_files:
        print("\n📊 Données ES (S&P 500 Futures):")
        for f in es_files:
            print(f)

    if other_files:
        print("\n📊 Autres fichiers:")
        for f in other_files:
            print(f)


def show_limitations():
    """Affiche les limitations de l'API Yahoo Finance"""
    print("\n⚠️  LIMITATIONS DE YAHOO FINANCE:")
    print("-" * 50)
    print("  • Données 1m:  7 derniers jours maximum")
    print("  • Données 5m:  60 derniers jours maximum")
    print("  • Données 15m: 60 derniers jours maximum")
    print("  • Données 1H:  730 derniers jours (2 ans)")
    print("  • Données 4H:  730 derniers jours (agrégé depuis 1H)")
    print("  • Données 1D:  Historique complet depuis 2018")
    print("  • Données 1W:  Historique complet depuis 2018")

    print("\n💡 POUR DES DONNÉES HISTORIQUES COMPLÈTES:")
    print("-" * 50)
    print("  Les données déjà présentes dans ce repo proviennent")
    print("  de sources professionnelles (TradeStation, etc.)")
    print("  ")
    print("  Options recommandées:")
    print("  • TradeStation API")
    print("  • Interactive Brokers API")
    print("  • Polygon.io")
    print("  • Alpha Vantage Premium")


def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("TÉLÉCHARGEMENT DE DONNÉES NQ ET ES")
    print("Yahoo Finance API (direct)")
    print("=" * 60)

    show_existing_data()
    show_limitations()

    print("\n" + "=" * 60)
    print("OPTIONS:")
    print("=" * 60)
    print("1. Télécharger avec Futures (NQ=F, ES=F)")
    print("2. Télécharger avec ETFs (QQQ, SPY) - Plus de données historiques")
    print("3. Afficher les données existantes")
    print("4. Quitter")

    try:
        choice = input("\nChoisissez une option (1-4): ").strip()
    except EOFError:
        choice = '1'

    if choice == '1':
        download_all_data(use_alternatives=False)
        print("\n✅ Téléchargement terminé!")
        show_existing_data()
    elif choice == '2':
        download_all_data(use_alternatives=True)
        print("\n✅ Téléchargement terminé!")
        show_existing_data()
    elif choice == '3':
        show_existing_data()
    else:
        print("\nAu revoir!")


if __name__ == "__main__":
    main()
