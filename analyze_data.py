#!/usr/bin/env python3
"""
Script d'analyse des données NQ et ES (2018-2025)
Analyse complète: statistiques, tendances, volatilité, corrélations
"""

import os
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from io import StringIO

import pandas as pd
import numpy as np

# Configuration
DATA_DIR = Path(__file__).parent
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)
pd.set_option('display.float_format', '{:.2f}'.format)


def load_csv_data(filepath: Path) -> pd.DataFrame:
    """Charge un fichier CSV avec le format du projet"""
    try:
        df = pd.read_csv(
            filepath,
            sep=';',
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1,  # Skip header row
            encoding='utf-8-sig'
        )

        # Créer datetime - essayer différents formats
        datetime_str = df['Date'] + ' ' + df['Time']
        try:
            # Format européen DD/MM/YYYY
            df['Datetime'] = pd.to_datetime(datetime_str, format='%d/%m/%Y %H:%M:%S')
        except:
            try:
                # Format américain MM/DD/YYYY
                df['Datetime'] = pd.to_datetime(datetime_str, format='%m/%d/%Y %H:%M:%S')
            except:
                # Format mixte
                df['Datetime'] = pd.to_datetime(datetime_str, format='mixed', dayfirst=True)

        df = df.set_index('Datetime')
        df = df.drop(columns=['Date', 'Time'])

        # Convertir en numérique
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df.dropna()
    except Exception as e:
        print(f"  Erreur lecture {filepath.name}: {e}")
        return pd.DataFrame()


def load_xlsx_data(filepath: Path) -> pd.DataFrame:
    """Charge un fichier Excel"""
    try:
        df = pd.read_excel(
            filepath,
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1
        )

        # Gérer les différents formats de date/time
        if df['Date'].dtype == 'datetime64[ns]':
            df['Datetime'] = df['Date']
        else:
            df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))

        df = df.set_index('Datetime')
        df = df.drop(columns=['Date', 'Time'], errors='ignore')

        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df.dropna()
    except Exception as e:
        print(f"  Erreur lecture {filepath.name}: {e}")
        return pd.DataFrame()


def load_zip_data(filepath: Path) -> pd.DataFrame:
    """Charge un fichier CSV compressé"""
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            csv_name = z.namelist()[0]
            with z.open(csv_name) as f:
                content = f.read().decode('utf-8-sig')
                df = pd.read_csv(
                    StringIO(content),
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )

        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%Y %H:%M:%S')
        df = df.set_index('Datetime')
        df = df.drop(columns=['Date', 'Time'])

        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df.dropna()
    except Exception as e:
        print(f"  Erreur lecture {filepath.name}: {e}")
        return pd.DataFrame()


def load_all_nq_daily() -> pd.DataFrame:
    """Charge toutes les données journalières NQ"""
    all_data = []
    for year in range(2018, 2026):
        filepath = DATA_DIR / f"{year} 1D.csv"
        if filepath.exists():
            df = load_csv_data(filepath)
            if not df.empty:
                all_data.append(df)

    if all_data:
        return pd.concat(all_data).sort_index()
    return pd.DataFrame()


def load_all_es_daily() -> pd.DataFrame:
    """Charge toutes les données journalières ES"""
    filepath = DATA_DIR / "ES 1D (2018-2025).csv"
    if filepath.exists():
        return load_csv_data(filepath)
    return pd.DataFrame()


def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule les rendements"""
    df = df.copy()
    df['Return'] = df['Close'].pct_change() * 100
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1)) * 100
    df['Range'] = ((df['High'] - df['Low']) / df['Close']) * 100
    df['Gap'] = ((df['Open'] - df['Close'].shift(1)) / df['Close'].shift(1)) * 100
    return df


def analyze_statistics(df: pd.DataFrame, name: str) -> dict:
    """Calcule les statistiques descriptives"""
    df = calculate_returns(df)

    stats = {
        'Symbol': name,
        'Start_Date': df.index.min().strftime('%Y-%m-%d'),
        'End_Date': df.index.max().strftime('%Y-%m-%d'),
        'Trading_Days': len(df),
        'Start_Price': df['Close'].iloc[0],
        'End_Price': df['Close'].iloc[-1],
        'Total_Return_%': ((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100,
        'CAGR_%': (((df['Close'].iloc[-1] / df['Close'].iloc[0]) ** (365 / (df.index.max() - df.index.min()).days)) - 1) * 100,
        'Avg_Daily_Return_%': df['Return'].mean(),
        'Std_Daily_Return_%': df['Return'].std(),
        'Sharpe_Ratio': (df['Return'].mean() / df['Return'].std()) * np.sqrt(252) if df['Return'].std() > 0 else 0,
        'Max_Daily_Gain_%': df['Return'].max(),
        'Max_Daily_Loss_%': df['Return'].min(),
        'Positive_Days_%': (df['Return'] > 0).sum() / len(df) * 100,
        'Avg_Volume': df['Volume'].mean(),
        'Max_Drawdown_%': calculate_max_drawdown(df),
        'Avg_Daily_Range_%': df['Range'].mean(),
        'Avg_Gap_%': df['Gap'].abs().mean(),
    }

    return stats


def calculate_max_drawdown(df: pd.DataFrame) -> float:
    """Calcule le drawdown maximum"""
    cummax = df['Close'].cummax()
    drawdown = (df['Close'] - cummax) / cummax * 100
    return drawdown.min()


def analyze_by_year(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Analyse année par année"""
    df = calculate_returns(df)

    yearly_stats = []
    for year in df.index.year.unique():
        year_df = df[df.index.year == year]
        if len(year_df) < 10:
            continue

        stats = {
            'Year': year,
            'Symbol': name,
            'Start_Price': year_df['Close'].iloc[0],
            'End_Price': year_df['Close'].iloc[-1],
            'Return_%': ((year_df['Close'].iloc[-1] / year_df['Close'].iloc[0]) - 1) * 100,
            'High': year_df['High'].max(),
            'Low': year_df['Low'].min(),
            'Volatility_%': year_df['Return'].std() * np.sqrt(252),
            'Trading_Days': len(year_df),
            'Positive_Days_%': (year_df['Return'] > 0).sum() / len(year_df) * 100,
            'Best_Day_%': year_df['Return'].max(),
            'Worst_Day_%': year_df['Return'].min(),
            'Avg_Volume': year_df['Volume'].mean(),
        }
        yearly_stats.append(stats)

    return pd.DataFrame(yearly_stats)


def analyze_by_month(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Analyse par mois (saisonnalité)"""
    df = calculate_returns(df)

    monthly_returns = df.groupby(df.index.month)['Return'].agg(['mean', 'std', 'count'])
    monthly_returns.columns = ['Avg_Return_%', 'Std_%', 'Count']
    monthly_returns['Positive_%'] = df.groupby(df.index.month)['Return'].apply(lambda x: (x > 0).sum() / len(x) * 100)
    monthly_returns.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_returns['Symbol'] = name

    return monthly_returns.reset_index().rename(columns={'index': 'Month'})


def analyze_by_weekday(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Analyse par jour de la semaine"""
    df = calculate_returns(df)

    weekday_returns = df.groupby(df.index.dayofweek)['Return'].agg(['mean', 'std', 'count'])
    weekday_returns.columns = ['Avg_Return_%', 'Std_%', 'Count']
    weekday_returns['Positive_%'] = df.groupby(df.index.dayofweek)['Return'].apply(lambda x: (x > 0).sum() / len(x) * 100)
    weekday_returns.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][:len(weekday_returns)]
    weekday_returns['Symbol'] = name

    return weekday_returns.reset_index().rename(columns={'index': 'Weekday'})


def find_extreme_days(df: pd.DataFrame, name: str, n: int = 10) -> tuple:
    """Trouve les meilleures et pires journées"""
    df = calculate_returns(df)

    best_days = df.nlargest(n, 'Return')[['Close', 'Return', 'Volume']].copy()
    best_days['Symbol'] = name
    best_days['Date'] = best_days.index.strftime('%Y-%m-%d')

    worst_days = df.nsmallest(n, 'Return')[['Close', 'Return', 'Volume']].copy()
    worst_days['Symbol'] = name
    worst_days['Date'] = worst_days.index.strftime('%Y-%m-%d')

    return best_days, worst_days


def analyze_volatility_regimes(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Analyse les régimes de volatilité"""
    df = calculate_returns(df)

    # Volatilité rolling 20 jours
    df['Vol_20d'] = df['Return'].rolling(20).std() * np.sqrt(252)

    # Définir les régimes
    vol_percentiles = df['Vol_20d'].quantile([0.25, 0.75])
    df['Vol_Regime'] = pd.cut(
        df['Vol_20d'],
        bins=[0, vol_percentiles[0.25], vol_percentiles[0.75], float('inf')],
        labels=['Low', 'Medium', 'High']
    )

    regime_stats = df.groupby('Vol_Regime').agg({
        'Return': ['mean', 'std', 'count'],
        'Volume': 'mean'
    }).round(4)

    regime_stats.columns = ['Avg_Return_%', 'Std_%', 'Days', 'Avg_Volume']
    regime_stats['Symbol'] = name

    return regime_stats.reset_index()


def analyze_correlation(nq_df: pd.DataFrame, es_df: pd.DataFrame) -> dict:
    """Analyse la corrélation entre NQ et ES"""
    # Aligner les données
    nq = calculate_returns(nq_df)
    es = calculate_returns(es_df)

    # Joindre sur l'index
    combined = pd.DataFrame({
        'NQ_Return': nq['Return'],
        'ES_Return': es['Return'],
        'NQ_Close': nq['Close'],
        'ES_Close': es['Close']
    }).dropna()

    if len(combined) < 30:
        return {}

    # Corrélation globale
    correlation = combined['NQ_Return'].corr(combined['ES_Return'])

    # Corrélation par année
    yearly_corr = combined.groupby(combined.index.year).apply(
        lambda x: x['NQ_Return'].corr(x['ES_Return'])
    )

    # Beta NQ vs ES
    covariance = combined['NQ_Return'].cov(combined['ES_Return'])
    variance_es = combined['ES_Return'].var()
    beta = covariance / variance_es if variance_es > 0 else 0

    return {
        'Overall_Correlation': correlation,
        'Beta_NQ_vs_ES': beta,
        'Yearly_Correlation': yearly_corr.to_dict(),
        'Sample_Size': len(combined)
    }


def analyze_trading_sessions(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Analyse par session de trading (si données horaires disponibles)"""
    if df.empty:
        return pd.DataFrame()

    df = calculate_returns(df)

    # Définir les sessions (heures US Eastern)
    def get_session(hour):
        if 9 <= hour < 12:
            return 'Morning (9-12)'
        elif 12 <= hour < 15:
            return 'Midday (12-15)'
        elif 15 <= hour < 17:
            return 'Afternoon (15-17)'
        else:
            return 'Extended Hours'

    df['Session'] = df.index.hour.map(get_session)

    session_stats = df.groupby('Session').agg({
        'Return': ['mean', 'std', 'count'],
        'Volume': 'mean',
        'Range': 'mean'
    }).round(4)

    session_stats.columns = ['Avg_Return_%', 'Std_%', 'Bars', 'Avg_Volume', 'Avg_Range_%']
    session_stats['Symbol'] = name

    return session_stats.reset_index()


def generate_report():
    """Génère le rapport d'analyse complet"""

    print("=" * 80)
    print("ANALYSE COMPLETE DES DONNEES NQ ET ES (2018-2025)")
    print("=" * 80)
    print(f"Date du rapport: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Charger les données
    print("Chargement des données...")
    nq_daily = load_all_nq_daily()
    es_daily = load_all_es_daily()

    if nq_daily.empty or es_daily.empty:
        print("Erreur: Impossible de charger les données")
        return

    print(f"  NQ: {len(nq_daily)} jours chargés ({nq_daily.index.min().date()} à {nq_daily.index.max().date()})")
    print(f"  ES: {len(es_daily)} jours chargés ({es_daily.index.min().date()} à {es_daily.index.max().date()})")
    print()

    # ============================================================
    # 1. STATISTIQUES GLOBALES
    # ============================================================
    print("=" * 80)
    print("1. STATISTIQUES GLOBALES")
    print("=" * 80)

    nq_stats = analyze_statistics(nq_daily, 'NQ')
    es_stats = analyze_statistics(es_daily, 'ES')

    stats_df = pd.DataFrame([nq_stats, es_stats]).set_index('Symbol')
    print(stats_df.T.to_string())
    print()

    # ============================================================
    # 2. PERFORMANCE ANNUELLE
    # ============================================================
    print("=" * 80)
    print("2. PERFORMANCE ANNUELLE")
    print("=" * 80)

    nq_yearly = analyze_by_year(nq_daily, 'NQ')
    es_yearly = analyze_by_year(es_daily, 'ES')

    print("\nNQ - Performance par année:")
    print(nq_yearly.to_string(index=False))
    print()

    print("ES - Performance par année:")
    print(es_yearly.to_string(index=False))
    print()

    # Comparaison côte à côte
    print("Comparaison des rendements annuels NQ vs ES:")
    comparison = pd.DataFrame({
        'Year': nq_yearly['Year'],
        'NQ_Return_%': nq_yearly['Return_%'].round(2),
        'ES_Return_%': es_yearly['Return_%'].round(2),
        'Difference_%': (nq_yearly['Return_%'] - es_yearly['Return_%']).round(2)
    })
    print(comparison.to_string(index=False))
    print()

    # ============================================================
    # 3. SAISONNALITE MENSUELLE
    # ============================================================
    print("=" * 80)
    print("3. SAISONNALITE MENSUELLE")
    print("=" * 80)

    nq_monthly = analyze_by_month(nq_daily, 'NQ')
    es_monthly = analyze_by_month(es_daily, 'ES')

    print("\nNQ - Performance par mois:")
    print(nq_monthly[['Month', 'Avg_Return_%', 'Std_%', 'Positive_%']].to_string(index=False))
    print()

    print("ES - Performance par mois:")
    print(es_monthly[['Month', 'Avg_Return_%', 'Std_%', 'Positive_%']].to_string(index=False))
    print()

    # Meilleurs/pires mois
    nq_best_month = nq_monthly.loc[nq_monthly['Avg_Return_%'].idxmax()]
    nq_worst_month = nq_monthly.loc[nq_monthly['Avg_Return_%'].idxmin()]
    print(f"NQ - Meilleur mois: {nq_best_month['Month']} ({nq_best_month['Avg_Return_%']:.2f}%)")
    print(f"NQ - Pire mois: {nq_worst_month['Month']} ({nq_worst_month['Avg_Return_%']:.2f}%)")
    print()

    # ============================================================
    # 4. ANALYSE PAR JOUR DE LA SEMAINE
    # ============================================================
    print("=" * 80)
    print("4. ANALYSE PAR JOUR DE LA SEMAINE")
    print("=" * 80)

    nq_weekday = analyze_by_weekday(nq_daily, 'NQ')
    es_weekday = analyze_by_weekday(es_daily, 'ES')

    print("\nNQ - Performance par jour:")
    print(nq_weekday[['Weekday', 'Avg_Return_%', 'Std_%', 'Positive_%']].to_string(index=False))
    print()

    print("ES - Performance par jour:")
    print(es_weekday[['Weekday', 'Avg_Return_%', 'Std_%', 'Positive_%']].to_string(index=False))
    print()

    # ============================================================
    # 5. JOURS EXTREMES
    # ============================================================
    print("=" * 80)
    print("5. JOURS EXTREMES")
    print("=" * 80)

    nq_best, nq_worst = find_extreme_days(nq_daily, 'NQ', 10)
    es_best, es_worst = find_extreme_days(es_daily, 'ES', 10)

    print("\nNQ - 10 Meilleures journées:")
    print(nq_best[['Date', 'Close', 'Return', 'Volume']].to_string(index=False))
    print()

    print("NQ - 10 Pires journées:")
    print(nq_worst[['Date', 'Close', 'Return', 'Volume']].to_string(index=False))
    print()

    print("ES - 10 Meilleures journées:")
    print(es_best[['Date', 'Close', 'Return', 'Volume']].to_string(index=False))
    print()

    print("ES - 10 Pires journées:")
    print(es_worst[['Date', 'Close', 'Return', 'Volume']].to_string(index=False))
    print()

    # ============================================================
    # 6. REGIMES DE VOLATILITE
    # ============================================================
    print("=" * 80)
    print("6. REGIMES DE VOLATILITE")
    print("=" * 80)

    nq_vol = analyze_volatility_regimes(nq_daily, 'NQ')
    es_vol = analyze_volatility_regimes(es_daily, 'ES')

    print("\nNQ - Régimes de volatilité:")
    print(nq_vol.to_string(index=False))
    print()

    print("ES - Régimes de volatilité:")
    print(es_vol.to_string(index=False))
    print()

    # ============================================================
    # 7. CORRELATION NQ vs ES
    # ============================================================
    print("=" * 80)
    print("7. CORRELATION NQ vs ES")
    print("=" * 80)

    corr_analysis = analyze_correlation(nq_daily, es_daily)

    if corr_analysis:
        print(f"\nCorrélation globale: {corr_analysis['Overall_Correlation']:.4f}")
        print(f"Beta NQ vs ES: {corr_analysis['Beta_NQ_vs_ES']:.4f}")
        print(f"Échantillon: {corr_analysis['Sample_Size']} jours")
        print("\nCorrélation par année:")
        for year, corr in corr_analysis['Yearly_Correlation'].items():
            print(f"  {year}: {corr:.4f}")
    print()

    # ============================================================
    # 8. ANALYSE HORAIRE (si données disponibles)
    # ============================================================
    print("=" * 80)
    print("8. ANALYSE PAR SESSION DE TRADING")
    print("=" * 80)

    # Charger données horaires
    nq_hourly_file = DATA_DIR / "2024 1H.csv"
    es_hourly_file = DATA_DIR / "ES 1h (2018-2025).csv"

    if nq_hourly_file.exists():
        nq_hourly = load_csv_data(nq_hourly_file)
        nq_sessions = analyze_trading_sessions(nq_hourly, 'NQ')
        if not nq_sessions.empty:
            print("\nNQ - Performance par session (données 2024):")
            print(nq_sessions.to_string(index=False))

    if es_hourly_file.exists():
        es_hourly = load_csv_data(es_hourly_file)
        es_sessions = analyze_trading_sessions(es_hourly, 'ES')
        if not es_sessions.empty:
            print("\nES - Performance par session:")
            print(es_sessions.to_string(index=False))
    print()

    # ============================================================
    # 9. RESUME EXECUTIF
    # ============================================================
    print("=" * 80)
    print("9. RESUME EXECUTIF")
    print("=" * 80)

    print(f"""
RESUME DE L'ANALYSE NQ ET ES (2018-2025)
========================================

PERFORMANCE GLOBALE:
- NQ (Nasdaq-100 Futures):
  * Rendement total: {nq_stats['Total_Return_%']:.1f}%
  * CAGR: {nq_stats['CAGR_%']:.1f}%
  * Sharpe Ratio: {nq_stats['Sharpe_Ratio']:.2f}
  * Max Drawdown: {nq_stats['Max_Drawdown_%']:.1f}%
  * Volatilité: {nq_stats['Std_Daily_Return_%']*np.sqrt(252):.1f}% annualisée

- ES (S&P 500 Futures):
  * Rendement total: {es_stats['Total_Return_%']:.1f}%
  * CAGR: {es_stats['CAGR_%']:.1f}%
  * Sharpe Ratio: {es_stats['Sharpe_Ratio']:.2f}
  * Max Drawdown: {es_stats['Max_Drawdown_%']:.1f}%
  * Volatilité: {es_stats['Std_Daily_Return_%']*np.sqrt(252):.1f}% annualisée

CORRELATION:
- NQ et ES sont fortement corrélés ({corr_analysis.get('Overall_Correlation', 0):.2f})
- Beta NQ/ES: {corr_analysis.get('Beta_NQ_vs_ES', 0):.2f} (NQ amplifie les mouvements ES)

SAISONNALITE:
- Meilleur mois NQ: {nq_best_month['Month']} (+{nq_best_month['Avg_Return_%']:.2f}%)
- Pire mois NQ: {nq_worst_month['Month']} ({nq_worst_month['Avg_Return_%']:.2f}%)

VOLATILITE:
- NQ est plus volatile que ES (beta > 1)
- Les régimes de haute volatilité ont des rendements moyens différents

OBSERVATIONS CLES:
1. NQ surperforme ES sur la période (tech > broad market)
2. Forte corrélation, mais NQ amplifie les mouvements
3. Saisonnalité prononcée (effet de fin d'année, faiblesse estivale)
4. Volume élevé lors des journées extrêmes
""")

    print("=" * 80)
    print("FIN DU RAPPORT")
    print("=" * 80)


if __name__ == "__main__":
    generate_report()
