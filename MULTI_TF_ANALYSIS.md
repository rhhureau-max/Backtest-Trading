# 📊 Analyse Multi-Timeframe: HTF FVG Sweep + 15m FVG Strategy

---

## 🎯 Logique de la Stratégie


Cette stratégie combine plusieurs timeframes:

1. **FVG 4H ou 1H**: Identifier un FVG sur le timeframe supérieur
2. **Wick Sweep**: Le prix touche le FVG avec une mèche (pas le corps)
3. **FVG 15m (Premier FVG)**: S'il y a plusieurs FVG 15m pendant le retracement 
   (FVG-FVG, FVG-neutre-FVG, FVG-neutre-neutre-FVG...), seul le PREMIER FVG 
   créé est utilisé comme zone d'intérêt pour l'entrée
4. **Entrée 15m**: Quand le prix casse et clôture au-delà du PREMIER FVG 15m après le sweep
5. **Stop Loss**: Au-dessus/en-dessous du FVG 15m cassé

**Fenêtre d'analyse**: 2:00 AM - 12:00 PM heure de Chicago (≈ 08:00-18:00 UTC)


## 📈 Résumé 2025

| Métrique | Valeur |

|----------|--------|

| Setups détectés | 74 |

| Trades LONG | 37 |

| Trades SHORT | 37 |

| Basés sur FVG 4H | 26 |

| Basés sur FVG 1H | 48 |


## 📝 Détail des Setups


### Setup #55 - 🟢 LONG

- **HTF FVG (4H)**: BEARISH @ 2025-08-15 08:00:00
  - Zone: 24083.68 - 24108.42
- **Sweep**: @ 2025-08-15 12:00:00
- **FVG 15m**: BEARISH @ 2025-08-15 09:45:00
  - Zone: 24050.36 - 24063.48
- **Entrée**: 24075.86 @ 2025-08-15 12:45:00
- **Stop Loss**: 24038.33
- **Risk**: 37.53 points


### Setup #56 - 🔴 SHORT

- **HTF FVG (1H)**: BULLISH @ 2025-08-25 10:00:00
  - Zone: 23807.73 - 23822.37
- **Sweep**: @ 2025-08-25 11:00:00
- **FVG 15m**: BULLISH @ 2025-08-25 10:00:00
  - Zone: 23807.73 - 23814.29
- **Entrée**: 23805.96 @ 2025-08-25 12:30:00
- **Stop Loss**: 23826.20
- **Risk**: 20.24 points


### Setup #57 - 🟢 LONG

- **HTF FVG (4H)**: BEARISH @ 2025-08-29 08:00:00
  - Zone: 23727.94 - 23846.35
- **Sweep**: @ 2025-08-29 12:00:00
- **FVG 15m**: BEARISH @ 2025-08-29 10:30:00
  - Zone: 23691.84 - 23692.85
- **Entrée**: 23699.41 @ 2025-08-29 14:00:00
- **Stop Loss**: 23679.99
- **Risk**: 19.42 points


### Setup #58 - 🟢 LONG

- **HTF FVG (1H)**: BEARISH @ 2025-09-02 10:00:00
  - Zone: 23360.09 - 23364.63
- **Sweep**: @ 2025-09-02 11:00:00
- **FVG 15m**: BEARISH @ 2025-09-02 10:15:00
  - Zone: 23338.12 - 23352.01
- **Entrée**: 23355.29 @ 2025-09-02 11:45:00
- **Stop Loss**: 23326.45
- **Risk**: 28.84 points


### Setup #59 - 🟢 LONG

- **HTF FVG (1H)**: BEARISH @ 2025-09-03 12:00:00
  - Zone: 23597.41 - 23623.17
- **Sweep**: @ 2025-09-03 13:00:00
- **FVG 15m**: BEARISH @ 2025-09-03 12:30:00
  - Zone: 23633.01 - 23646.14
- **Entrée**: 23684.52 @ 2025-09-03 14:45:00
- **Stop Loss**: 23621.20
- **Risk**: 63.32 points


### Setup #60 - 🟢 LONG

- **HTF FVG (4H)**: BEARISH @ 2025-09-05 08:00:00
  - Zone: 23930.93 - 23960.47
- **Sweep**: @ 2025-09-05 12:00:00
- **FVG 15m**: BEARISH @ 2025-09-05 09:45:00
  - Zone: 23807.73 - 23823.38
- **Entrée**: 23880.94 @ 2025-09-05 12:00:00
- **Stop Loss**: 23795.82
- **Risk**: 85.12 points


### Setup #61 - 🔴 SHORT

- **HTF FVG (1H)**: BULLISH @ 2025-09-08 08:00:00
  - Zone: 24015.01 - 24042.02
- **Sweep**: @ 2025-09-08 09:00:00
- **FVG 15m**: BULLISH @ 2025-09-08 08:30:00
  - Zone: 24030.66 - 24049.60
- **Entrée**: 24023.85 @ 2025-09-08 12:00:00
- **Stop Loss**: 24061.62
- **Risk**: 37.78 points


### Setup #62 - 🔴 SHORT

- **HTF FVG (4H)**: BULLISH @ 2025-09-09 12:00:00
  - Zone: 24094.03 - 24110.44
- **Sweep**: @ 2025-09-09 16:00:00
- **FVG 15m**: BULLISH @ 2025-09-09 15:15:00
  - Zone: 24117.01 - 24128.62
- **Entrée**: 24112.97 @ 2025-09-09 18:15:00
- **Stop Loss**: 24140.69
- **Risk**: 27.72 points


### Setup #63 - 🟢 LONG

- **HTF FVG (1H)**: BEARISH @ 2025-09-18 14:00:00
  - Zone: 24722.75 - 24727.75
- **Sweep**: @ 2025-09-18 15:00:00
- **FVG 15m**: BEARISH @ 2025-09-18 14:15:00
  - Zone: 24732.00 - 24743.75
- **Entrée**: 24745.50 @ 2025-09-18 18:30:00
- **Stop Loss**: 24719.63
- **Risk**: 25.87 points


### Setup #64 - 🔴 SHORT

- **HTF FVG (1H)**: BULLISH @ 2025-09-29 08:00:00
  - Zone: 24909.50 - 24917.50
- **Sweep**: @ 2025-09-29 09:00:00
- **FVG 15m**: BULLISH @ 2025-09-29 07:00:00
  - Zone: 24878.25 - 24879.50
- **Entrée**: 24867.00 @ 2025-09-29 10:15:00
- **Stop Loss**: 24891.94
- **Risk**: 24.94 points


### Setup #65 - 🔴 SHORT

- **HTF FVG (1H)**: BULLISH @ 2025-10-06 12:00:00
  - Zone: 25211.50 - 25218.50
- **Sweep**: @ 2025-10-06 13:00:00
- **FVG 15m**: BULLISH @ 2025-10-06 10:45:00
  - Zone: 25181.25 - 25183.25
- **Entrée**: 25177.00 @ 2025-10-06 15:00:00
- **Stop Loss**: 25195.84
- **Risk**: 18.84 points


### Setup #66 - 🟢 LONG

- **HTF FVG (1H)**: BEARISH @ 2025-10-10 14:00:00
  - Zone: 24448.00 - 24572.00
- **Sweep**: @ 2025-10-10 15:00:00
- **FVG 15m**: BEARISH @ 2025-10-10 12:45:00
  - Zone: 24691.50 - 24694.25
- **Entrée**: 24705.00 @ 2025-10-12 18:00:00
- **Stop Loss**: 24679.15
- **Risk**: 25.85 points


### Setup #67 - 🔴 SHORT

- **HTF FVG (1H)**: BULLISH @ 2025-10-14 11:00:00
  - Zone: 24839.25 - 24858.00
- **Sweep**: @ 2025-10-14 12:00:00
- **FVG 15m**: BULLISH @ 2025-10-14 10:30:00
  - Zone: 24731.50 - 24777.00
- **Entrée**: 24718.25 @ 2025-10-14 14:30:00
- **Stop Loss**: 24789.39
- **Risk**: 71.14 points


### Setup #68 - 🟢 LONG

- **HTF FVG (1H)**: BEARISH @ 2025-10-30 13:00:00
  - Zone: 25993.75 - 25999.00
- **Sweep**: @ 2025-10-30 14:00:00
- **FVG 15m**: BEARISH @ 2025-10-30 13:00:00
  - Zone: 26014.00 - 26046.75
- **Entrée**: 26132.25 @ 2025-10-30 15:30:00
- **Stop Loss**: 26000.99
- **Risk**: 131.26 points


### Setup #69 - 🟢 LONG

- **HTF FVG (4H)**: BEARISH @ 2025-10-31 08:00:00
  - Zone: 26118.25 - 26161.75
- **Sweep**: @ 2025-10-31 12:00:00
- **FVG 15m**: BEARISH @ 2025-10-31 10:45:00
  - Zone: 26053.50 - 26073.50
- **Entrée**: 26086.00 @ 2025-10-31 14:15:00
- **Stop Loss**: 26040.47
- **Risk**: 45.53 points


### Setup #70 - 🟢 LONG

- **HTF FVG (1H)**: BEARISH @ 2025-10-31 11:00:00
  - Zone: 25980.75 - 26050.00
- **Sweep**: @ 2025-10-31 12:00:00
- **FVG 15m**: BEARISH @ 2025-10-31 10:45:00
  - Zone: 26053.50 - 26073.50
- **Entrée**: 26086.00 @ 2025-10-31 14:15:00
- **Stop Loss**: 26040.47
- **Risk**: 45.53 points


### Setup #71 - 🔴 SHORT

- **HTF FVG (4H)**: BULLISH @ 2025-11-05 08:00:00
  - Zone: 25596.00 - 25694.50
- **Sweep**: @ 2025-11-05 12:00:00
- **FVG 15m**: BULLISH @ 2025-11-05 10:30:00
  - Zone: 25748.75 - 25758.50
- **Entrée**: 25741.00 @ 2025-11-05 14:45:00
- **Stop Loss**: 25771.38
- **Risk**: 30.38 points


### Setup #72 - 🔴 SHORT

- **HTF FVG (1H)**: BULLISH @ 2025-11-05 11:00:00
  - Zone: 25788.50 - 25804.50
- **Sweep**: @ 2025-11-05 12:00:00
- **FVG 15m**: BULLISH @ 2025-11-05 10:30:00
  - Zone: 25748.75 - 25758.50
- **Entrée**: 25741.00 @ 2025-11-05 14:45:00
- **Stop Loss**: 25771.38
- **Risk**: 30.38 points


### Setup #73 - 🟢 LONG

- **HTF FVG (1H)**: BEARISH @ 2025-11-07 08:00:00
  - Zone: 25045.00 - 25066.75
- **Sweep**: @ 2025-11-07 09:00:00
- **FVG 15m**: BEARISH @ 2025-11-07 08:30:00
  - Zone: 25045.25 - 25075.50
- **Entrée**: 25093.75 @ 2025-11-07 13:30:00
- **Stop Loss**: 25032.73
- **Risk**: 61.02 points


### Setup #74 - 🟢 LONG

- **HTF FVG (1H)**: BEARISH @ 2025-11-07 09:00:00
  - Zone: 24861.00 - 24917.75
- **Sweep**: @ 2025-11-07 10:00:00
- **FVG 15m**: BEARISH @ 2025-11-07 08:30:00
  - Zone: 25045.25 - 25075.50
- **Entrée**: 25093.75 @ 2025-11-07 13:30:00
- **Stop Loss**: 25032.73
- **Risk**: 61.02 points


*... et 54 autres setups*
