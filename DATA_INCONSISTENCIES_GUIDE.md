# Gestion des Incohérences de Données - Guide Technique

## Introduction

Ce document explique en détail comment le framework gère les différents types d'incohérences de données qui peuvent survenir lors du backtesting de stratégies de trading.

## Types d'Incohérences et Solutions

### 1. Jours Fériés et Weekends

#### Problème
Les marchés sont fermés pendant les weekends et jours fériés, créant des trous dans les données.

#### Solution Implémentée
```python
# Le moteur de backtest itère uniquement sur les dates présentes dans les données
dates = pd.Series(df.index.date).unique()

for date in dates:
    # Si aucune donnée n'existe pour cette date, elle est automatiquement ignorée
    session_data = TimeManager.get_session_data(df, date, start_hour, end_hour)
    if len(session_data) == 0:
        continue  # Passe au jour suivant
```

**Impact:** Aucun trade n'est généré les jours sans données. Le comptage des jours de trading est basé uniquement sur les jours avec données disponibles.

**Vérification:**
```python
# Compter les jours uniques avec données
trading_days = df.index.date.nunique()
print(f"Nombre de jours de trading: {trading_days}")
```

---

### 2. Gaps de Prix (Price Gaps)

#### Problème
Un gap se produit quand le prix d'ouverture d'une bougie est significativement différent de la clôture de la bougie précédente. Cela peut:
- Sauter un stop loss
- Sauter un take profit
- Invalider des niveaux de support/résistance

#### Solution Implémentée

**Pour Stop Loss:**
```python
# Dans execute_trade()
if direction == 'LONG':
    if row['Low'] <= stop_loss:
        # Le trade est fermé au niveau du SL, même si le prix a gap en dessous
        exit_price = stop_loss
        return {'result': 'LOSS', 'exit_price': exit_price, ...}
```

**Pour Take Profit:**
```python
if direction == 'LONG':
    if row['High'] >= take_profit:
        # Le trade est fermé au niveau du TP, même si le prix a gap au-dessus
        exit_price = take_profit
        return {'result': 'WIN', 'exit_price': exit_price, ...}
```

**Amélioration Recommandée (Slippage):**
```python
def execute_trade_with_slippage(self, df, signal, slippage_points=2.0):
    """Execute trade with realistic slippage simulation."""
    
    # ... code existant ...
    
    if direction == 'LONG':
        if row['Low'] <= stop_loss:
            # Appliquer slippage sur SL
            actual_exit = stop_loss - slippage_points
            # Mais ne pas dépasser le low réel de la bougie
            actual_exit = max(actual_exit, row['Low'])
            return {'exit_price': actual_exit, ...}
```

**Impact:** 
- Résultats optimistes si gaps favorables
- Peut être pessimiste si gaps défavorables
- Le slippage ajoute du réalisme

---

### 3. Données Manquantes (Missing Data)

#### Problème
Des bougies individuelles peuvent manquer en raison de:
- Problèmes de connexion au flux de données
- Faible liquidité
- Erreurs de fichier

#### Détection
```python
def detect_missing_candles(df, expected_interval_minutes=5):
    """
    Détecter les bougies manquantes dans une série temporelle.
    
    Args:
        df: DataFrame avec index datetime
        expected_interval_minutes: Intervalle attendu entre bougies (5, 15, 60, etc.)
    
    Returns:
        List des timestamps où des bougies manquent
    """
    expected_interval = pd.Timedelta(minutes=expected_interval_minutes)
    missing_periods = []
    
    for i in range(1, len(df)):
        time_diff = df.index[i] - df.index[i-1]
        if time_diff > expected_interval:
            missing_periods.append({
                'after': df.index[i-1],
                'before': df.index[i],
                'gap_duration': time_diff,
                'missing_candles': int(time_diff / expected_interval) - 1
            })
    
    return missing_periods
```

#### Solutions

**Option 1: Supprimer (Recommandé)**
```python
# Supprimer les lignes avec valeurs manquantes
df_clean = df.dropna()
```

**Option 2: Forward Fill (À utiliser avec précaution)**
```python
# Propager la dernière valeur connue
df_filled = df.fillna(method='ffill')
```

⚠️ **Avertissement:** Le forward fill peut créer des artefacts artificiels et fausser les résultats. Utilisez uniquement si les gaps sont très petits (1-2 bougies).

**Option 3: Interpolation (NON recommandé pour OHLCV)**
```python
# NE PAS FAIRE CECI pour des données OHLCV
df_interpolated = df.interpolate()  # ❌ Crée des prix artificiels
```

**Impact:** 
- Le dropna() réduit la taille du dataset mais maintient l'intégrité
- Le forward fill peut masquer des problèmes de données
- L'interpolation crée des prix qui n'ont jamais existé (dangereux)

---

### 4. Valeurs Aberrantes (Outliers)

#### Problème
Des erreurs de données peuvent créer des prix irréalistes (ex: prix négatifs, variations de 100% en une bougie).

#### Détection
```python
def detect_price_outliers(df, std_threshold=5):
    """
    Détecter les valeurs aberrantes dans les prix.
    
    Args:
        df: DataFrame avec colonnes OHLCV
        std_threshold: Nombre d'écarts-types pour considérer comme aberrant
    
    Returns:
        DataFrame avec les lignes suspectes
    """
    # Calculer les variations en pourcentage
    df['price_change_pct'] = df['Close'].pct_change() * 100
    
    # Calculer moyenne et écart-type
    mean = df['price_change_pct'].mean()
    std = df['price_change_pct'].std()
    
    # Identifier les outliers
    outliers = df[
        (df['price_change_pct'] > mean + std_threshold * std) |
        (df['price_change_pct'] < mean - std_threshold * std)
    ]
    
    return outliers

def validate_ohlc_consistency(df):
    """
    Vérifier la cohérence des données OHLC.
    
    Returns:
        DataFrame avec les lignes incohérentes
    """
    inconsistent = df[
        (df['High'] < df['Low']) |  # High < Low (impossible)
        (df['High'] < df['Open']) |  # High < Open (impossible)
        (df['High'] < df['Close']) |  # High < Close (impossible)
        (df['Low'] > df['Open']) |  # Low > Open (impossible)
        (df['Low'] > df['Close']) |  # Low > Close (impossible)
        (df['Close'] <= 0) |  # Prix négatif ou nul
        (df['Open'] <= 0)
    ]
    
    return inconsistent
```

#### Correction
```python
# Supprimer les données incohérentes
df_validated = df[
    (df['High'] >= df['Low']) &
    (df['High'] >= df['Open']) &
    (df['High'] >= df['Close']) &
    (df['Low'] <= df['Open']) &
    (df['Low'] <= df['Close']) &
    (df['Close'] > 0) &
    (df['Open'] > 0)
]
```

---

### 5. Fuseaux Horaires (Timezones)

#### Problème
Les données peuvent être dans différents fuseaux horaires (UTC, Eastern, Paris) et les stratégies nécessitent l'heure de Paris.

#### Solution Implémentée
```python
@staticmethod
def convert_to_paris_time(df: pd.DataFrame) -> pd.DataFrame:
    """Convert datetime index to Paris timezone."""
    df_copy = df.copy()
    
    # Localiser en UTC si naive
    if df_copy.index.tz is None:
        df_copy.index = df_copy.index.tz_localize('UTC')
    
    # Convertir en heure de Paris
    df_copy.index = df_copy.index.tz_convert('Europe/Paris')
    
    return df_copy
```

**Vérification:**
```python
# Vérifier le fuseau horaire
print(f"Timezone: {df.index.tz}")

# Afficher quelques timestamps
print(df.head())
```

**Impact:** 
- Les sessions sont correctement identifiées (Asian 00:00-08:00, London 08:00-12:00 Paris time)
- Les horaires d'été/hiver sont automatiquement gérés par pytz

---

### 6. Changements d'Heure d'Été/Hiver

#### Problème
Les changements d'heure peuvent créer des bougies dupliquées ou manquantes.

#### Solution
```python
# pytz gère automatiquement les changements DST
# Mais il faut être conscient des duplications possibles

# Supprimer les duplicatas (garde le premier)
df = df[~df.index.duplicated(keep='first')]

# Ou garde le dernier
df = df[~df.index.duplicated(keep='last')]
```

---

### 7. Volume Anormal

#### Problème
Volume = 0 ou valeurs irréalistes peuvent indiquer des problèmes de données.

#### Détection et Filtrage
```python
def filter_low_volume_periods(df, min_volume=10):
    """
    Filtrer les périodes de volume anormalement bas.
    
    Args:
        df: DataFrame avec colonne Volume
        min_volume: Volume minimum acceptable
    
    Returns:
        DataFrame filtré
    """
    # Identifier les périodes de faible volume
    low_volume = df[df['Volume'] < min_volume]
    print(f"Trouvé {len(low_volume)} bougies avec volume < {min_volume}")
    
    # Option: Supprimer ces périodes
    df_filtered = df[df['Volume'] >= min_volume]
    
    return df_filtered

def analyze_volume_distribution(df):
    """Analyser la distribution du volume."""
    print(f"Volume moyen: {df['Volume'].mean():.0f}")
    print(f"Volume médian: {df['Volume'].median():.0f}")
    print(f"Volume min: {df['Volume'].min():.0f}")
    print(f"Volume max: {df['Volume'].max():.0f}")
    print(f"Bougies avec Volume=0: {(df['Volume'] == 0).sum()}")
```

---

## Workflow Complet de Nettoyage des Données

```python
def comprehensive_data_cleaning(filepath):
    """
    Pipeline complet de nettoyage des données.
    
    Args:
        filepath: Chemin vers le fichier CSV
    
    Returns:
        DataFrame nettoyé et validé
    """
    print("="*80)
    print("NETTOYAGE DES DONNÉES")
    print("="*80)
    
    # 1. Charger les données
    print("\n[1] Chargement des données...")
    df = DataLoader.load_csv(filepath)
    print(f"    Chargé: {len(df)} lignes")
    
    # 2. Supprimer les valeurs manquantes
    print("\n[2] Suppression des valeurs manquantes...")
    df = df.dropna()
    print(f"    Après nettoyage: {len(df)} lignes")
    
    # 3. Valider la cohérence OHLC
    print("\n[3] Validation de la cohérence OHLC...")
    inconsistent = validate_ohlc_consistency(df)
    if len(inconsistent) > 0:
        print(f"    ⚠️  Trouvé {len(inconsistent)} lignes incohérentes")
        print(inconsistent)
        df = df[
            (df['High'] >= df['Low']) &
            (df['High'] >= df['Open']) &
            (df['High'] >= df['Close']) &
            (df['Low'] <= df['Open']) &
            (df['Low'] <= df['Close']) &
            (df['Close'] > 0) &
            (df['Open'] > 0)
        ]
        print(f"    Après nettoyage: {len(df)} lignes")
    else:
        print("    ✓ Toutes les données sont cohérentes")
    
    # 4. Détecter les bougies manquantes
    print("\n[4] Détection des bougies manquantes...")
    missing = detect_missing_candles(df, expected_interval_minutes=5)
    if missing:
        print(f"    ⚠️  Trouvé {len(missing)} gaps dans les données")
        for gap in missing[:5]:  # Afficher les 5 premiers
            print(f"       Gap de {gap['missing_candles']} bougies après {gap['after']}")
    else:
        print("    ✓ Aucune bougie manquante détectée")
    
    # 5. Supprimer les duplicatas
    print("\n[5] Suppression des duplicatas...")
    before = len(df)
    df = df[~df.index.duplicated(keep='first')]
    after = len(df)
    if before > after:
        print(f"    Supprimé {before - after} duplicatas")
    else:
        print("    ✓ Aucun duplicata trouvé")
    
    # 6. Filtrer le volume anormal
    print("\n[6] Filtrage du volume anormal...")
    zero_volume = (df['Volume'] == 0).sum()
    if zero_volume > 0:
        print(f"    ⚠️  Trouvé {zero_volume} bougies avec Volume=0")
        df = df[df['Volume'] > 0]
        print(f"    Après filtrage: {len(df)} lignes")
    else:
        print("    ✓ Aucun problème de volume détecté")
    
    # 7. Détecter les outliers de prix
    print("\n[7] Détection des outliers de prix...")
    outliers = detect_price_outliers(df, std_threshold=5)
    if len(outliers) > 0:
        print(f"    ⚠️  Trouvé {len(outliers)} outliers potentiels")
        print("    (Ces valeurs peuvent être légitimes dans des marchés volatils)")
    else:
        print("    ✓ Aucun outlier extrême détecté")
    
    # 8. Convertir au fuseau horaire de Paris
    print("\n[8] Conversion au fuseau horaire de Paris...")
    try:
        df = TimeManager.convert_to_paris_time(df)
        print(f"    ✓ Converti en {df.index.tz}")
    except Exception as e:
        print(f"    Note: {e}")
    
    print("\n" + "="*80)
    print(f"NETTOYAGE TERMINÉ - Dataset final: {len(df)} lignes")
    print(f"Période: {df.index.min()} à {df.index.max()}")
    print("="*80 + "\n")
    
    return df
```

---

## Recommandations Best Practices

### 1. Toujours Valider Avant le Backtest
```python
# Avant de lancer un backtest
df = comprehensive_data_cleaning("2024 5m.csv")
```

### 2. Sauvegarder les Données Nettoyées
```python
# Sauvegarder pour réutilisation
df.to_csv("2024_5m_cleaned.csv")
```

### 3. Logger les Problèmes
```python
# Créer un rapport de nettoyage
with open('data_cleaning_report.txt', 'w') as f:
    f.write(f"Date: {datetime.now()}\n")
    f.write(f"Lignes originales: {len(df_original)}\n")
    f.write(f"Lignes après nettoyage: {len(df_clean)}\n")
    f.write(f"Taux de conservation: {len(df_clean)/len(df_original)*100:.2f}%\n")
```

### 4. Comparer Avant/Après
```python
# Comparer les statistiques
print("Avant nettoyage:")
print(df_original.describe())
print("\nAprès nettoyage:")
print(df_clean.describe())
```

---

## Conclusion

La qualité des données est critique pour des résultats de backtest fiables. Ce framework gère automatiquement la plupart des problèmes courants, mais il est recommandé de:

1. ✅ Toujours inspecter visuellement un échantillon de données
2. ✅ Exécuter le pipeline de nettoyage complet
3. ✅ Documenter les problèmes trouvés
4. ✅ Conserver les données originales
5. ✅ Comparer les résultats sur différentes périodes pour détecter les anomalies

**Règle d'or:** Si les données semblent trop parfaites ou les résultats trop bons, investiguez plus en profondeur. La réalité du trading est imparfaite.
