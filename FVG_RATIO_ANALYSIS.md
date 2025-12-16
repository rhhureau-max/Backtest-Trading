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

La stratégie testée est une **continuation du FVG** (trading dans la direction du mouvement initial):

| Type de FVG | Direction du Trade | Logique |
|-------------|-------------------|---------|
| **FVG Haussier** | **LONG** (achat) | Le prix va continuer vers le haut |
| **FVG Baissier** | **SHORT** (vente) | Le prix va continuer vers le bas |

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
| **LONG** | En-dessous du prix d'entrée | `SL = Prix d'entrée - Distance SL` |
| **SHORT** | Au-dessus du prix d'entrée | `SL = Prix d'entrée + Distance SL` |

**Exemple pour un trade LONG avec entrée à 20100.00 et SL 50% (40 points):**
```
SL = 20100.00 - 40.00 = 20060.00
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
| **LONG** | Au-dessus du prix d'entrée | `TP = Prix d'entrée + Distance TP` |
| **SHORT** | En-dessous du prix d'entrée | `TP = Prix d'entrée - Distance TP` |

### 3.4 Exemple Complet

**Contexte:**
- Trade LONG (FVG haussier)
- Prix d'entrée = 20100.00
- Corps de bougie n = 80 points
- SL = 50% → Distance SL = 40 points

**Calcul des niveaux TP pour différents R:R:**

| R:R | Distance TP | Niveau TP |
|-----|-------------|-----------|
| 1.0 | 40 × 1.0 = 40 pts | 20100 + 40 = **20140.00** |
| 1.5 | 40 × 1.5 = 60 pts | 20100 + 60 = **20160.00** |
| 2.0 | 40 × 2.0 = 80 pts | 20100 + 80 = **20180.00** |
| 3.0 | 40 × 3.0 = 120 pts | 20100 + 120 = **20220.00** |
| 5.0 | 40 × 5.0 = 200 pts | 20100 + 200 = **20300.00** |

---

## 4. Tableaux de Résultats Complets

### 4.1 Données de Base

- **Période analysée**: 2018 - 2025 (données complètes de 2021 à 2025, les années 2018-2020 ne contiennent pas de bougie à 15:25:00)
- **Total de FVG détectés**: 223
- **Horaire de vérification**: jusqu'à 21:55:00 UTC (fin de session)

### 4.2 Tableau pour SL = 50% du Corps

| R:R | Wins | Losses | Non Résolus | Total | Winrate | Profit Factor | Espérance |
|-----|------|--------|-------------|-------|---------|---------------|-----------|
| **1.0** | 120 | 102 | 1 | 222 | **54.1%** | **1.18** | **+0.08R** |
| 1.5 | 69 | 150 | 4 | 219 | 31.5% | 0.69 | -0.21R |
| 2.0 | 59 | 157 | 7 | 216 | 27.3% | 0.75 | -0.18R |
| 2.5 | 49 | 165 | 9 | 214 | 22.9% | 0.74 | -0.20R |
| 3.0 | 45 | 167 | 11 | 212 | 21.2% | 0.81 | -0.15R |
| 3.5 | 40 | 172 | 11 | 212 | 18.9% | 0.81 | -0.15R |
| 4.0 | 34 | 176 | 13 | 210 | 16.2% | 0.77 | -0.19R |
| 4.5 | 29 | 180 | 14 | 209 | 13.9% | 0.72 | -0.24R |
| 5.0 | 26 | 183 | 14 | 209 | 12.4% | 0.71 | -0.25R |

**Observations SL 50%:**
- ✅ Seule configuration profitable: R:R = 1.0 (PF 1.18, Espérance +0.08R)
- ❌ Toutes les configurations avec R:R > 1 sont perdantes (PF < 1)
- ⚠️ La stratégie de continuation ne fonctionne pas bien sur les FVG à 8h30 NY

### 4.3 Tableau pour SL = 75% du Corps

| R:R | Wins | Losses | Non Résolus | Total | Winrate | Profit Factor | Espérance |
|-----|------|--------|-------------|-------|---------|---------------|-----------|
| 1.0 | 104 | 115 | 4 | 219 | 47.5% | 0.90 | -0.05R |
| 1.5 | 71 | 143 | 9 | 214 | 33.2% | 0.74 | -0.17R |
| 2.0 | 58 | 151 | 14 | 209 | 27.8% | 0.77 | -0.17R |
| 2.5 | 48 | 159 | 16 | 207 | 23.2% | 0.75 | -0.19R |
| 3.0 | 39 | 166 | 18 | 205 | 19.0% | 0.70 | -0.24R |
| 3.5 | 34 | 171 | 18 | 205 | 16.6% | 0.70 | -0.25R |
| 4.0 | 29 | 176 | 18 | 205 | 14.1% | 0.66 | -0.29R |
| 4.5 | 27 | 177 | 19 | 204 | 13.2% | 0.69 | -0.27R |
| 5.0 | 21 | 182 | 20 | 203 | 10.3% | 0.58 | -0.38R |

**Observations SL 75%:**
- ❌ Aucune configuration profitable (tous les PF < 1)
- ⚠️ Le SL plus large ne compense pas les pertes
- ❌ Les espérances sont toutes négatives

### 4.4 Tableau pour SL = 100% du Corps

| R:R | Wins | Losses | Non Résolus | Total | Winrate | Profit Factor | Espérance |
|-----|------|--------|-------------|-------|---------|---------------|-----------|
| 1.0 | 98 | 114 | 11 | 212 | 46.2% | 0.86 | -0.08R |
| 1.5 | 71 | 135 | 17 | 206 | 34.5% | 0.79 | -0.14R |
| 2.0 | 56 | 145 | 22 | 201 | 27.9% | 0.77 | -0.16R |
| 2.5 | 45 | 154 | 24 | 199 | 22.6% | 0.73 | -0.21R |
| 3.0 | 38 | 160 | 25 | 198 | 19.2% | 0.71 | -0.23R |
| 3.5 | 35 | 162 | 26 | 197 | 17.8% | 0.76 | -0.20R |
| 4.0 | 25 | 170 | 28 | 195 | 12.8% | 0.59 | -0.36R |
| 4.5 | 23 | 172 | 28 | 195 | 11.8% | 0.60 | -0.35R |
| 5.0 | 22 | 172 | 29 | 194 | 11.3% | 0.64 | -0.32R |

**Observations SL 100%:**
- ❌ Aucune configuration profitable (tous les PF < 1)
- ⚠️ Plus de trades "non résolus" (11-29) car le SL large est rarement touché avant la fin de session
- ❌ Toutes les espérances sont négatives

---

## 5. Analyse Graphique des Tendances

### 5.1 Évolution du Winrate selon le R:R

Le winrate suit une **courbe décroissante** prévisible avec l'augmentation du ratio R:R:

```
Winrate (%)
    |
 55 |  ●                                          (SL 50%)
 50 |    ●                                        (SL 75%)
 45 |      ●                                      (SL 100%)
 40 |
 35 |        ●  ●
 30 |              ●  ●
 25 |                  ●  ●
 20 |                      ●  ●
 15 |                          ●  ●  ●
 10 |                                  ●  ●
    +-------------------------------------------- R:R
        1   1.5   2   2.5   3   3.5   4   4.5   5
```

**Tendances observées:**
- **Chute brutale** entre R:R 1.0 et 1.5 (perte de ~20 points de winrate)
- **Décroissance régulière** entre R:R 1.5 et 5.0 (~5 points par palier de 0.5 R:R)
- **Plancher** autour de 10-12% pour R:R = 5.0

### 5.2 Point d'Équilibre (Break-Even) par SL%

Le point d'équilibre (PF = 1, Espérance = 0) varie selon le pourcentage de SL:

| SL % | Zone Break-Even | Configurations Profitables |
|------|-----------------|---------------------------|
| **50%** | R:R ≈ 1.2 | R:R 1.0 uniquement |
| **75%** | R:R < 1.0 | Aucune |
| **100%** | R:R < 1.0 | Aucune |

### 5.3 Analyse du Profit Factor selon le R:R

```
Profit Factor
    |
1.2 |  ★                                          (★ = Meilleur PF = 1.18)
1.1 |
1.0 |----------------------------------------------  Seuil de rentabilité
0.9 |  ○  ▲
0.8 |      ●  ○  ▲  ●  ○  ▲  ●  ○
0.7 |          ●  ○  ●  ○  ●  ○  ▲  ▲
0.6 |                              ●  ○  ●  ○  ▲
    +--------------------------------------------
        1   1.5   2   2.5   3   3.5   4   4.5   5
        
● SL 50%   ○ SL 75%   ▲ SL 100%
```

**Analyse:**
- Seul **SL 50% avec R:R 1.0** maintient un PF > 1
- Les **SL larges (75%, 100%)** sont tous non profitables
- La stratégie de continuation ne fonctionne pas bien sur ce setup

### 5.4 Corrélation Winrate / Rentabilité

Un winrate élevé ne garantit pas la rentabilité, mais dans notre cas:

| Winrate Minimum Théorique | R:R | Winrate Observé | Statut |
|---------------------------|-----|-----------------|--------|
| 50.0% | 1.0 | 46-54% | ⚠️ Limite (seul SL 50% profitable) |
| 40.0% | 1.5 | 31-35% | ❌ Non profitable |
| 33.3% | 2.0 | 27-28% | ❌ Non profitable |
| 28.6% | 2.5 | 22-23% | ❌ Non profitable |
| 25.0% | 3.0 | 19-21% | ❌ Non profitable |
| 20.0% | 4.0 | 13-16% | ❌ Non profitable |

---

## 6. Meilleures Configurations

### 6.1 🏆 Configuration #1: La Seule Rentable

| Paramètre | Valeur |
|-----------|--------|
| **Stop Loss** | 50% du corps |
| **Risk/Reward** | 1.0 |
| **Winrate** | 54.1% |
| **Profit Factor** | 1.18 |
| **Espérance** | +0.08R par trade |

**Pourquoi c'est la seule rentable:**
- Winrate légèrement supérieur à 50% (54.1%)
- Profit Factor modeste (1.18) indiquant que pour chaque 1€ perdu, vous gagnez 1.18€
- Espérance positive de +0.08R signifie qu'en moyenne, chaque trade rapporte 8% du risque

**Exemple sur 100 trades avec risque de 100€:**
```
Gains estimés = 100 trades × 0.08R × 100€ = +800€
```

### 6.2 ⚠️ Configurations Non Rentables

Toutes les autres configurations sont perdantes:

| SL % | R:R | PF | Espérance | Statut |
|------|-----|-----|-----------|--------|
| 50% | 1.5+ | < 0.81 | -0.15R à -0.25R | ❌ |
| 75% | Tous | < 0.90 | -0.05R à -0.38R | ❌ |
| 100% | Tous | < 0.86 | -0.08R à -0.36R | ❌ |

### 6.3 Configurations à Éviter ⛔

| Configuration | Raison |
|---------------|--------|
| SL 50% + R:R ≥ 1.5 | PF ≤ 0.81 (perdant) |
| SL 75% + Tous R:R | PF ≤ 0.90 (perdant) |
| SL 100% + Tous R:R | PF ≤ 0.86 (perdant) |
| Tout R:R ≥ 1.5 | Généralement non profitable |

---

## 7. Conclusions et Recommandations Pratiques

### 7.1 Synthèse des Résultats

1. **La stratégie de continuation des FVG n'est pas globalement profitable** avec ce setup
   - Seule la configuration SL 50% + R:R 1.0 est marginalement rentable (PF 1.18)
   - Toutes les autres configurations génèrent des pertes

2. **Le Stop Loss serré (50%) est le seul qui peut être profitable**:
   - Uniquement avec R:R 1.0
   - Winrate de 54.1% juste au-dessus du seuil de 50%

3. **Le R:R = 1.0 est le seul viable** pour cette stratégie:
   - Le marché a tendance à retracer après les FVG plutôt qu'à continuer
   - Les ratios R:R plus élevés ne permettent pas d'atteindre le TP

4. **La courbe d'efficience décroît fortement avec le R:R**:
   - Plus le R:R est élevé, plus les pertes sont importantes
   - Aucune configuration avec R:R ≥ 1.5 n'est profitable

### 7.2 Recommandations par Profil de Trader

#### ⚠️ Avertissement Important
La stratégie de continuation des FVG sur ce setup montre des résultats mitigés. La seule configuration marginalement profitable est présentée ci-dessous.

#### Configuration Unique Recommandée (si utilisée)
```
Configuration recommandée:
├── Stop Loss: 50% du corps
├── Risk/Reward: 1.0
├── Risque par trade: 0.5-1% du capital (conservative)
└── Fréquence: ~1 trade par semaine (sur les FVG valides)
```

**Note**: Avec un PF de seulement 1.18 et une espérance de +0.08R, cette stratégie offre un edge très limité. Considérez d'autres approches (comme le fade du FVG) pour de meilleurs résultats.

### 7.3 Règles de Money Management

| Règle | Recommandation |
|-------|----------------|
| **Risque par trade** | Maximum 0.5-1% du capital (edge limité) |
| **Nombre de trades/jour** | 1 seul (un seul FVG à 8h30) |
| **Drawdown maximum** | Arrêter après 3 pertes consécutives |
| **Prise de profit partielle** | Non recommandée avec R:R 1.0 |

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
- [ ] Définir le SL selon le % choisi (50% recommandé)
- [ ] Calculer le TP selon le R:R choisi (1.0 recommandé)
- [ ] Vérifier l'absence de news économiques majeures
- [ ] Respecter le risk management (0.5-1% max)
- [ ] Placer l'ordre à l'ouverture de la bougie n+2 (8:40 NY)

---

## Annexe: Formules Récapitulatives

```
Corps bougie n = |Close_n - Open_n|

Distance SL = Corps × SL%
           où SL% ∈ {0.50, 0.75, 1.00}

Distance TP = Distance SL × R:R
           où R:R ∈ {1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0}

Pour LONG (FVG haussier):
  - SL = Prix_entrée - Distance_SL
  - TP = Prix_entrée + Distance_TP

Pour SHORT (FVG baissier):
  - SL = Prix_entrée + Distance_SL
  - TP = Prix_entrée - Distance_TP

Profit Factor = (Wins × R:R) / Losses

Espérance = ((Wins × R:R) - Losses) / Total_trades
```

---

*Document basé sur l'analyse du script `fvg_analysis_830.py` et les données de backtesting de 2018 à 2025.*

*Dernière mise à jour: Novembre 2025*
