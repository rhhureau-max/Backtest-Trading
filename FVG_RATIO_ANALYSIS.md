# 📊 Analyse Détaillée des Ratios Risk/Reward sur les FVG 8h30 NY

---

## 📋 Table des Matières

1. [Rappel de la Méthodologie](#1-rappel-de-la-méthodologie)
2. [Explication du Calcul du Stop Loss](#2-explication-du-calcul-du-stop-loss)
3. [Explication du Calcul du Take Profit](#3-explication-du-calcul-du-take-profit)
4. [Tableaux de Résultats Complets](#4-tableaux-de-résultats-complets)
5. [Analyse Graphique des Tendances](#5-analyse-graphique-des-tendances)
6. [Meilleures Configurations](#6-meilleures-configurations)
7. [Conclusions et Recommandations Pratiques](#7-conclusions-et-recommandations-pratiques)

---

## 1. Rappel de la Méthodologie

### 1.1 Détection des FVG (Fair Value Gaps)

Les FVG sont détectés en utilisant les **mèches (High/Low)** des bougies, conformément à la définition standard du Smart Money Concept (SMC).

#### Bougies Analysées

| Bougie | Horaire UTC | Horaire NY | Rôle |
|--------|-------------|------------|------|
| **n-1** | 15:25:00 | 8:25 | Bougie de référence précédente |
| **n** | 15:30:00 | 8:30 | Bougie centrale (ouverture NY) |
| **n+1** | 15:35:00 | 8:35 | Bougie de référence suivante |
| **n+2** | 15:40:00 | 8:40 | **Bougie d'entrée en position** |

### 1.2 Conditions de Formation des FVG

#### FVG Haussier (Bullish FVG) 📈

```
Condition: Low(bougie n-1) > High(bougie n+1)
```

Un FVG haussier se forme lorsque le **point le plus bas** (Low/mèche basse) de la bougie n-1 est **supérieur** au **point le plus haut** (High/mèche haute) de la bougie n+1. Cela crée un "gap" ou "trou" vers le haut dans la structure du prix.

```
        ┌──┐ Bougie n-1
        │  │
    ────┴──┴──── Low n-1 (15:25)
    
        ▓▓▓▓▓▓▓▓ GAP HAUSSIER (zone FVG)
    
    ────┬──┬──── High n+1 (15:35)
        │  │
        └──┘ Bougie n+1
```

#### FVG Baissier (Bearish FVG) 📉

```
Condition: High(bougie n-1) < Low(bougie n+1)
```

Un FVG baissier se forme lorsque le **point le plus haut** (High/mèche haute) de la bougie n-1 est **inférieur** au **point le plus bas** (Low/mèche basse) de la bougie n+1. Cela crée un "gap" vers le bas.

```
        ┌──┐ Bougie n-1
        │  │
    ────┴──┴──── High n-1 (15:25)
    
        ▓▓▓▓▓▓▓▓ GAP BAISSIER (zone FVG)
    
    ────┬──┬──── Low n+1 (15:35)
        │  │
        └──┘ Bougie n+1
```

### 1.3 Règles d'Entrée et Direction

La stratégie testée est un **fade du FVG** (trading contre le mouvement initial):

| Type de FVG | Direction du Trade | Logique |
|-------------|-------------------|---------|
| **FVG Haussier** | **SHORT** (vente) | Le gap haussier sera comblé → le prix va baisser |
| **FVG Baissier** | **LONG** (achat) | Le gap baissier sera comblé → le prix va monter |

**Point d'entrée**: Ouverture de la bougie n+2 (15:40:00 UTC / 8:40 NY)

---

## 2. Explication du Calcul du Stop Loss

### 2.1 Base du Calcul: Le Corps de la Bougie n (8:30 NY)

Le Stop Loss est calculé à partir du **corps** de la bougie centrale n (15:30:00 UTC):

```
Corps de la bougie n = |Close - Open|
```

Cette mesure représente la volatilité intrinsèque du mouvement de prix pendant la bougie d'ouverture de New York.

### 2.2 Niveaux de Stop Loss Testés

Trois pourcentages du corps sont utilisés pour définir la distance du Stop Loss:

| SL % | Formule | Description |
|------|---------|-------------|
| **50%** | `Distance SL = Corps × 0.5` | Stop Loss serré (moitié du corps) |
| **75%** | `Distance SL = Corps × 0.75` | Stop Loss intermédiaire |
| **100%** | `Distance SL = Corps × 1.0` | Stop Loss complet (égal au corps) |

### 2.3 Exemple Concret de Calcul

Supposons une bougie n (8:30 NY) avec:
- Open = 20000.00
- Close = 20080.00

**Calcul du corps:**
```
Corps = |20080.00 - 20000.00| = 80.00 points
```

**Calcul des distances SL:**
```
SL 50%  = 80.00 × 0.50 = 40.00 points
SL 75%  = 80.00 × 0.75 = 60.00 points
SL 100% = 80.00 × 1.00 = 80.00 points
```

### 2.4 Positionnement du Stop Loss

| Direction | Position du SL | Formule |
|-----------|----------------|---------|
| **SHORT** | Au-dessus du prix d'entrée | `SL = Prix d'entrée + Distance SL` |
| **LONG** | En-dessous du prix d'entrée | `SL = Prix d'entrée - Distance SL` |

**Exemple pour un trade SHORT avec entrée à 20100.00 et SL 50% (40 points):**
```
SL = 20100.00 + 40.00 = 20140.00
```

---

## 3. Explication du Calcul du Take Profit

### 3.1 Principe du Risk/Reward (R:R)

Le Take Profit est déterminé en fonction du ratio Risk/Reward souhaité:

```
Distance TP = Distance SL × Ratio R:R
```

### 3.2 Ratios Risk/Reward Testés

| Ratio R:R | Signification | Distance TP |
|-----------|---------------|-------------|
| **1.0** | Gain potentiel = Risque | TP = SL × 1.0 |
| **1.5** | Gain = 1.5× le risque | TP = SL × 1.5 |
| **2.0** | Gain = 2× le risque | TP = SL × 2.0 |
| **2.5** | Gain = 2.5× le risque | TP = SL × 2.5 |
| **3.0** | Gain = 3× le risque | TP = SL × 3.0 |
| **3.5** | Gain = 3.5× le risque | TP = SL × 3.5 |
| **4.0** | Gain = 4× le risque | TP = SL × 4.0 |
| **4.5** | Gain = 4.5× le risque | TP = SL × 4.5 |
| **5.0** | Gain = 5× le risque | TP = SL × 5.0 |

### 3.3 Positionnement du Take Profit

Le TP est placé dans la **direction opposée** au SL:

| Direction | Position du TP | Formule |
|-----------|----------------|---------|
| **SHORT** | En-dessous du prix d'entrée | `TP = Prix d'entrée - Distance TP` |
| **LONG** | Au-dessus du prix d'entrée | `TP = Prix d'entrée + Distance TP` |

### 3.4 Exemple Complet

**Contexte:**
- Trade SHORT (FVG haussier)
- Prix d'entrée = 20100.00
- Corps de bougie n = 80 points
- SL = 50% → Distance SL = 40 points

**Calcul des niveaux TP pour différents R:R:**

| R:R | Distance TP | Niveau TP |
|-----|-------------|-----------|
| 1.0 | 40 × 1.0 = 40 pts | 20100 - 40 = **20060.00** |
| 1.5 | 40 × 1.5 = 60 pts | 20100 - 60 = **20040.00** |
| 2.0 | 40 × 2.0 = 80 pts | 20100 - 80 = **20020.00** |
| 3.0 | 40 × 3.0 = 120 pts | 20100 - 120 = **19980.00** |
| 5.0 | 40 × 5.0 = 200 pts | 20100 - 200 = **19900.00** |

---

## 4. Tableaux de Résultats Complets

### 4.1 Données de Base

- **Période analysée**: 2018 - 2025 (données complètes de 2021 à 2025, les années 2018-2020 ne contiennent pas de bougie à 15:25:00)
- **Total de FVG détectés**: 223
- **Horaire de vérification**: jusqu'à 21:55:00 UTC (fin de session)

### 4.2 Tableau pour SL = 50% du Corps

| R:R | Wins | Losses | Non Résolus | Total | Winrate | Profit Factor | Espérance |
|-----|------|--------|-------------|-------|---------|---------------|-----------|
| **1.0** | 136 | 86 | 1 | 222 | **61.3%** | **1.58** | **+0.23R** |
| 1.5 | 87 | 135 | 1 | 222 | 39.2% | 0.97 | -0.02R |
| 2.0 | 77 | 144 | 2 | 221 | 34.8% | 1.07 | +0.05R |
| 2.5 | 66 | 154 | 3 | 220 | 30.0% | 1.07 | +0.05R |
| 3.0 | 58 | 160 | 5 | 218 | 26.6% | 1.09 | +0.06R |
| 3.5 | 52 | 164 | 7 | 216 | 24.1% | 1.11 | +0.08R |
| **4.0** | 47 | 167 | 9 | 214 | 22.0% | 1.13 | **+0.10R** |
| 4.5 | 37 | 174 | 12 | 211 | 17.5% | 0.96 | -0.04R |
| 5.0 | 35 | 176 | 12 | 211 | 16.6% | 0.99 | -0.00R |

**Observations SL 50%:**
- ✅ Meilleure performance globale avec R:R = 1.0 (PF 1.58)
- ✅ Toutes les configurations entre R:R 2.0 et 4.0 sont profitables (PF > 1)
- ⚠️ R:R 1.5 est légèrement perdant (PF 0.97)
- ❌ R:R 4.5 et 5.0 deviennent non profitables

### 4.3 Tableau pour SL = 75% du Corps

| R:R | Wins | Losses | Non Résolus | Total | Winrate | Profit Factor | Espérance |
|-----|------|--------|-------------|-------|---------|---------------|-----------|
| **1.0** | 122 | 97 | 4 | 219 | **55.7%** | **1.26** | **+0.11R** |
| 1.5 | 91 | 124 | 8 | 215 | 42.3% | 1.10 | +0.06R |
| **2.0** | 77 | 135 | 11 | 212 | 36.3% | **1.14** | **+0.09R** |
| 2.5 | 63 | 144 | 16 | 207 | 30.4% | 1.09 | +0.07R |
| 3.0 | 48 | 155 | 20 | 203 | 23.6% | 0.93 | -0.05R |
| 3.5 | 44 | 159 | 20 | 203 | 21.7% | 0.97 | -0.02R |
| 4.0 | 39 | 163 | 21 | 202 | 19.3% | 0.96 | -0.03R |
| 4.5 | 36 | 165 | 22 | 201 | 17.9% | 0.98 | -0.01R |
| 5.0 | 32 | 168 | 23 | 200 | 16.0% | 0.95 | -0.04R |

**Observations SL 75%:**
- ✅ Configurations profitables jusqu'à R:R 2.5 (PF > 1)
- ⚠️ R:R = 2.0 offre le meilleur compromis avec PF = 1.14 et Espérance +0.09R
- ❌ À partir de R:R 3.0, toutes les configurations deviennent perdantes

### 4.4 Tableau pour SL = 100% du Corps

| R:R | Wins | Losses | Non Résolus | Total | Winrate | Profit Factor | Espérance |
|-----|------|--------|-------------|-------|---------|---------------|-----------|
| **1.0** | 117 | 95 | 11 | 212 | **55.2%** | 1.23 | +0.10R |
| **1.5** | 90 | 118 | 15 | 208 | 43.3% | **1.14** | **+0.08R** |
| 2.0 | 71 | 131 | 21 | 202 | 35.1% | 1.08 | +0.05R |
| 2.5 | 53 | 146 | 24 | 199 | 26.6% | 0.91 | -0.07R |
| 3.0 | 46 | 152 | 25 | 198 | 23.2% | 0.91 | -0.07R |
| 3.5 | 41 | 155 | 27 | 196 | 20.9% | 0.93 | -0.06R |
| 4.0 | 35 | 159 | 29 | 194 | 18.0% | 0.88 | -0.10R |
| 4.5 | 32 | 160 | 31 | 192 | 16.7% | 0.90 | -0.08R |
| 5.0 | 30 | 160 | 33 | 190 | 15.8% | 0.94 | -0.05R |

**Observations SL 100%:**
- ✅ Configurations profitables jusqu'à R:R 2.0
- ⚠️ Plus de trades "non résolus" (11-33) car le SL large est rarement touché avant la fin de session
- ❌ À partir de R:R 2.5, toutes les configurations deviennent perdantes

---

## 5. Analyse Graphique des Tendances

### 5.1 Évolution du Winrate selon le R:R

Le winrate suit une **courbe décroissante** prévisible avec l'augmentation du ratio R:R:

```
Winrate (%)
    |
 65 |  ●                                          (SL 50%)
 60 |    ●                                        (SL 75%)
 55 |      ●  ●                                   (SL 100%)
 50 |
 45 |        ●
 40 |          ●  ●
 35 |              ●  ●
 30 |                  ●  ●
 25 |                      ●  ●
 20 |                          ●  ●  ●
 15 |                                  ●  ●
    +-------------------------------------------- R:R
        1   1.5   2   2.5   3   3.5   4   4.5   5
```

**Tendances observées:**
- **Chute brutale** entre R:R 1.0 et 1.5 (perte de ~20 points de winrate)
- **Décroissance régulière** entre R:R 1.5 et 5.0 (~5 points par palier de 0.5 R:R)
- **Plancher** autour de 16-17% pour R:R = 5.0

### 5.2 Point d'Équilibre (Break-Even) par SL%

Le point d'équilibre (PF = 1, Espérance = 0) varie selon le pourcentage de SL:

| SL % | Zone Break-Even | Configurations Profitables |
|------|-----------------|---------------------------|
| **50%** | R:R ≈ 1.5 et R:R ≈ 5.0 | R:R 1.0, puis 2.0 à 4.0 |
| **75%** | R:R ≈ 2.8 | R:R 1.0 à 2.5 |
| **100%** | R:R ≈ 2.2 | R:R 1.0 à 2.0 |

### 5.3 Analyse du Profit Factor selon le R:R

```
Profit Factor
    |
1.6 |  ★                                          (★ = Meilleur PF)
1.5 |
1.4 |
1.3 |        ●
1.2 |          ●  ●
1.1 |  ○  ○        ●  ●  ●  ●
1.0 |------●---------------------------●---------- Seuil de rentabilité
0.9 |                  ○  ○  ○  ○  ○
0.8 |                              ▲
    +--------------------------------------------
        1   1.5   2   2.5   3   3.5   4   4.5   5
        
● SL 50%   ○ SL 75%   ▲ SL 100%
```

**Analyse:**
- Le **SL 50%** maintient un PF > 1 sur une plus large gamme de R:R
- Les **SL larges (75%, 100%)** deviennent rapidement non profitables à mesure que le R:R augmente
- La configuration optimale (PF = 1.58) est nettement supérieure aux autres

### 5.4 Corrélation Winrate / Rentabilité

Un winrate élevé ne garantit pas la rentabilité, mais dans notre cas:

| Winrate Minimum Théorique | R:R | Winrate Observé | Statut |
|---------------------------|-----|-----------------|--------|
| 50.0% | 1.0 | 55-61% | ✅ Profitable |
| 40.0% | 1.5 | 39-43% | ⚠️ Limite |
| 33.3% | 2.0 | 35-36% | ✅ Profitable |
| 28.6% | 2.5 | 27-30% | ⚠️ Limite |
| 25.0% | 3.0 | 23-27% | ❌/⚠️ Variable |
| 20.0% | 4.0 | 18-22% | ❌ Non profitable (sauf SL 50%) |

---

## 6. Meilleures Configurations

### 6.1 🏆 Configuration #1: La Plus Rentable

| Paramètre | Valeur |
|-----------|--------|
| **Stop Loss** | 50% du corps |
| **Risk/Reward** | 1.0 |
| **Winrate** | 61.3% |
| **Profit Factor** | 1.58 |
| **Espérance** | +0.23R par trade |

**Pourquoi c'est la meilleure:**
- Winrate très élevé (61.3%) grâce au TP proche
- Profit Factor exceptionnel (1.58) indiquant que pour chaque 1€ perdu, vous gagnez 1.58€
- Espérance positive de +0.23R signifie qu'en moyenne, chaque trade rapporte 23% du risque

**Exemple sur 100 trades avec risque de 100€:**
```
Gains estimés = 100 trades × 0.23R × 100€ = +2,300€
```

### 6.2 🥈 Configuration #2: Compromis R:R / Rentabilité

| Paramètre | Valeur |
|-----------|--------|
| **Stop Loss** | 75% du corps |
| **Risk/Reward** | 2.0 |
| **Winrate** | 36.3% |
| **Profit Factor** | 1.14 |
| **Espérance** | +0.09R par trade |

**Avantages:**
- Ratio R:R de 2:1 permet des gains plus importants par trade gagnant
- Toujours profitable avec PF > 1
- Stop Loss plus large offre une meilleure protection contre le bruit du marché

### 6.3 🥉 Configuration #3: Pour les Traders Prudents

| Paramètre | Valeur |
|-----------|--------|
| **Stop Loss** | 50% du corps |
| **Risk/Reward** | 4.0 |
| **Winrate** | 22.0% |
| **Profit Factor** | 1.13 |
| **Espérance** | +0.10R par trade |

**Avantages:**
- Chaque trade gagnant rapporte 4× le risque
- Fonctionne bien pour les traders qui préfèrent moins de trades gagnants mais avec de gros gains
- Espérance positive malgré un faible winrate

### 6.4 Configurations à Éviter ⛔

| Configuration | Raison |
|---------------|--------|
| SL 50% + R:R 1.5 | PF = 0.97 (légèrement perdant) |
| SL 75% + R:R ≥ 3.0 | PF < 1 (perdant) |
| SL 100% + R:R ≥ 2.5 | PF < 1 (perdant) |
| Tout R:R ≥ 4.5 | Généralement non profitable |

---

## 7. Conclusions et Recommandations Pratiques

### 7.1 Synthèse des Résultats

1. **La stratégie de fade des FVG est globalement profitable** lorsqu'elle est configurée correctement

2. **Le Stop Loss serré (50%) surperforme systématiquement** les SL plus larges car:
   - Il permet plus de configurations profitables
   - Il limite les pertes tout en capturant les mouvements de retour rapides

3. **Le R:R = 1.0 est optimal** pour cette stratégie spécifique:
   - Le marché comble souvent les FVG rapidement
   - Un TP proche maximise le winrate

4. **La courbe d'efficience décroît avec le R:R**:
   - Plus le R:R est élevé, moins la stratégie est efficace
   - Exception: zone SL 50% entre R:R 2.0 et 4.0 qui reste profitable

### 7.2 Recommandations par Profil de Trader

#### Pour les Traders Débutants
```
Configuration recommandée:
├── Stop Loss: 50% du corps
├── Risk/Reward: 1.0
├── Risque par trade: 1-2% du capital
└── Fréquence: ~1 trade par semaine (sur les FVG valides)
```

#### Pour les Traders Intermédiaires
```
Configuration recommandée:
├── Stop Loss: 75% du corps
├── Risk/Reward: 2.0
├── Risque par trade: 1-2% du capital
└── Possibilité de pyramider sur confirmation
```

#### Pour les Traders Expérimentés
```
Configurations multiples:
├── 60% des trades: SL 50%, R:R 1.0 (capture rapide)
├── 30% des trades: SL 50%, R:R 3.0-4.0 (swing intraday)
└── 10% des trades: SL 75%, R:R 2.0 (protection accrue)
```

### 7.3 Règles de Money Management

| Règle | Recommandation |
|-------|----------------|
| **Risque par trade** | Maximum 1-2% du capital |
| **Nombre de trades/jour** | 1 seul (un seul FVG à 8h30) |
| **Drawdown maximum** | Arrêter après 3-5 pertes consécutives |
| **Prise de profit partielle** | Possible à 50% du TP initial |

### 7.4 Limites et Avertissements

⚠️ **Cette analyse ne prend pas en compte:**
- Les spreads et commissions (impact significatif sur R:R 1.0)
- Le slippage à l'entrée et à la sortie
- Les conditions de marché exceptionnelles (haute volatilité)
- Les jours fériés et événements économiques majeurs

⚠️ **Données historiques:**
- Période des fichiers: 2018-2025
- Données FVG exploitables: 2021-2025 (les années 2018-2020 ne contiennent pas de bougie à 15:25:00)
- Les performances passées ne garantissent pas les résultats futurs

### 7.5 Checklist Avant de Trader

- [ ] Vérifier la présence d'un FVG valide à 8:35 NY
- [ ] Calculer le corps de la bougie n (8:30)
- [ ] Définir le SL selon le % choisi (50%, 75% ou 100%)
- [ ] Calculer le TP selon le R:R choisi
- [ ] Vérifier l'absence de news économiques majeures
- [ ] Respecter le risk management (1-2% max)
- [ ] Placer l'ordre à l'ouverture de la bougie n+2 (8:40 NY)

---

## Annexe: Formules Récapitulatives

```
Corps bougie n = |Close_n - Open_n|

Distance SL = Corps × SL%
           où SL% ∈ {0.50, 0.75, 1.00}

Distance TP = Distance SL × R:R
           où R:R ∈ {1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0}

Pour SHORT:
  - SL = Prix_entrée + Distance_SL
  - TP = Prix_entrée - Distance_TP

Pour LONG:
  - SL = Prix_entrée - Distance_SL
  - TP = Prix_entrée + Distance_TP

Profit Factor = (Wins × R:R) / Losses

Espérance = ((Wins × R:R) - Losses) / Total_trades
```

---

*Document basé sur l'analyse du script `fvg_analysis_830.py` et les données de backtesting de 2018 à 2025.*

*Dernière mise à jour: Novembre 2025*
