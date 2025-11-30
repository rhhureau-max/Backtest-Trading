# 📊 Analyse Détaillée: Stratégie Sweep + FVG Multi-Timeframe

---

## 🎯 Vue d'Ensemble de la Stratégie


Cette stratégie combine la détection de **Liquidity Sweeps** sur le timeframe 15 minutes 
avec les **Fair Value Gaps (FVG)** sur 5 minutes pour trouver des entrées précises sur 1 minute.

### Logique de la Stratégie

1. **Détection du Sweep (15m)**: Un swing high (mouvement haussier puis baissier) ou swing low. Seule la mèche casse le swing pour prendre la liquidité.
2. **FVG Précédent (5m)**: Identifier le FVG créé AVANT le sweep (FVG haussier créé pendant la montée, ou FVG baissier créé pendant la descente)
3. **Cassure du FVG (1m)**: Après le sweep, le prix revient et CASSE le FVG précédent
4. **Entrée (1m)**: Entrer quand la bougie 1m clôture au-delà du FVG (en-dessous pour short, au-dessus pour long)
5. **Stop Loss**: Au-dessus du FVG cassé (short) / En-dessous du FVG cassé (long)
6. **Take Profits**: 1RR, 1.5RR, 2RR, 2.5RR, 3RR, 3.5RR, 4RR, 4.5RR, 5RR


## 📈 Résumé des Résultats

| Métrique | Valeur |
|----------|--------|
| Nombre total de trades | 1595 |
| Trades gagnants | 386 |
| Trades perdants | 1208 |
| Win Rate | 24.2% |
| PnL Total (points) | 34993.87 |
| Gain moyen | 262.68 pts |
| Perte moyenne | -54.97 pts |


### 🎯 Analyse des Take Profits (Win Rate par RR)

| RR | Atteints | Win Rate |
|----|----------|----------|
| 1 RR | 1076 | 67.5% |
| 1.5 RR | 918 | 57.6% |
| 2 RR | 806 | 50.5% |
| 2.5 RR | 690 | 43.3% |
| 3 RR | 603 | 37.8% |
| 3.5 RR | 542 | 34.0% |
| 4 RR | 482 | 30.2% |
| 4.5 RR | 426 | 26.7% |
| 5 RR | 386 | 24.2% |
| **Stop Loss** | 1208 | 75.7% |


### 📊 Analyse par Direction

| Direction | Trades | Gagnants | Win Rate |
|-----------|--------|----------|----------|
| LONG | 744 | 174 | 23.4% |
| SHORT | 851 | 212 | 24.9% |


## 📝 Détail des Trades

### Trade #1 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-02 07:15:00
- **FVG 5m**: 22106.76 - 22119.90
- **Entrée**: 22096.70 @ 2025-01-02 07:16:00
- **Stop Loss**: 22130.96
- **Risk**: 34.26 points
- **TP 1RR**: 22062.45 ❌
- **TP 1.5RR**: 22045.32 ❌
- **TP 2RR**: 22028.19 ❌
- **TP 2.5RR**: 22011.06 ❌
- **TP 3RR**: 21993.93 ❌
- **TP 3.5RR**: 21976.81 ❌
- **TP 4RR**: 21959.68 ❌
- **TP 4.5RR**: 21942.55 ❌
- **TP 5RR**: 21925.42 ❌
- **PnL**: -34.26 points (-1.0R)
- **MFE**: 29.64 points
- **MAE**: 34.54 points

### Trade #2 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-02 08:45:00
- **FVG 5m**: 21887.68 - 21923.76
- **Entrée**: 21926.85 @ 2025-01-02 08:48:00
- **Stop Loss**: 21876.73
- **Risk**: 50.12 points
- **TP 1RR**: 21976.97 ✅
- **TP 1.5RR**: 22002.03 ✅
- **TP 2RR**: 22027.09 ✅
- **TP 2.5RR**: 22052.15 ✅
- **TP 3RR**: 22077.21 ✅
- **TP 3.5RR**: 22102.27 ✅
- **TP 4RR**: 22127.33 ❌
- **TP 4.5RR**: 22152.39 ❌
- **TP 5RR**: 22177.45 ❌
- **PnL**: -50.12 points (-1.0R)
- **MFE**: 181.19 points
- **MAE**: 60.31 points

### Trade #3 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-02 08:45:00
- **FVG 5m**: 21887.68 - 21923.76
- **Entrée**: 21926.85 @ 2025-01-02 08:48:00
- **Stop Loss**: 21876.73
- **Risk**: 50.12 points
- **TP 1RR**: 21976.97 ✅
- **TP 1.5RR**: 22002.03 ✅
- **TP 2RR**: 22027.09 ✅
- **TP 2.5RR**: 22052.15 ✅
- **TP 3RR**: 22077.21 ✅
- **TP 3.5RR**: 22102.27 ✅
- **TP 4RR**: 22127.33 ❌
- **TP 4.5RR**: 22152.39 ❌
- **TP 5RR**: 22177.45 ❌
- **PnL**: -50.12 points (-1.0R)
- **MFE**: 181.19 points
- **MAE**: 60.31 points

### Trade #4 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-02 09:15:00
- **FVG 5m**: 21966.29 - 22031.75
- **Entrée**: 21963.97 @ 2025-01-02 09:21:00
- **Stop Loss**: 22042.77
- **Risk**: 78.80 points
- **TP 1RR**: 21885.16 ✅
- **TP 1.5RR**: 21845.76 ✅
- **TP 2RR**: 21806.36 ✅
- **TP 2.5RR**: 21766.96 ✅
- **TP 3RR**: 21727.56 ✅
- **TP 3.5RR**: 21688.16 ✅
- **TP 4RR**: 21648.76 ✅
- **TP 4.5RR**: 21609.36 ❌
- **TP 5RR**: 21569.96 ❌
- **PnL**: -78.80 points (-1.0R)
- **MFE**: 330.42 points
- **MAE**: 116.76 points

### Trade #5 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-02 14:00:00
- **FVG 5m**: 21729.42 - 21750.30
- **Entrée**: 21759.84 @ 2025-01-02 14:03:00
- **Stop Loss**: 21718.56
- **Risk**: 41.28 points
- **TP 1RR**: 21801.11 ✅
- **TP 1.5RR**: 21821.75 ✅
- **TP 2RR**: 21842.39 ✅
- **TP 2.5RR**: 21863.03 ✅
- **TP 3RR**: 21883.67 ✅
- **TP 3.5RR**: 21904.31 ✅
- **TP 4RR**: 21924.95 ✅
- **TP 4.5RR**: 21945.59 ✅
- **TP 5RR**: 21966.23 ✅
- **PnL**: 206.39 points (5.0R)
- **MFE**: 216.25 points
- **MAE**: 3.09 points

### Trade #6 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 09:00:00
- **FVG 5m**: 22024.28 - 22057.01
- **Entrée**: 22011.39 @ 2025-01-03 09:01:00
- **Stop Loss**: 22068.04
- **Risk**: 56.65 points
- **TP 1RR**: 21954.74 ❌
- **TP 1.5RR**: 21926.42 ❌
- **TP 2RR**: 21898.09 ❌
- **TP 2.5RR**: 21869.77 ❌
- **TP 3RR**: 21841.45 ❌
- **TP 3.5RR**: 21813.12 ❌
- **TP 4RR**: 21784.80 ❌
- **TP 4.5RR**: 21756.47 ❌
- **TP 5RR**: 21728.15 ❌
- **PnL**: -56.65 points (-1.0R)
- **MFE**: 3.09 points
- **MAE**: 77.32 points

### Trade #7 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 15:00:00
- **FVG 5m**: 22211.40 - 22213.98
- **Entrée**: 22165.52 @ 2025-01-03 15:01:00
- **Stop Loss**: 22225.08
- **Risk**: 59.56 points
- **TP 1RR**: 22105.96 ❌
- **TP 1.5RR**: 22076.18 ❌
- **TP 2RR**: 22046.40 ❌
- **TP 2.5RR**: 22016.61 ❌
- **TP 3RR**: 21986.83 ❌
- **TP 3.5RR**: 21957.05 ❌
- **TP 4RR**: 21927.27 ❌
- **TP 4.5RR**: 21897.49 ❌
- **TP 5RR**: 21867.71 ❌
- **PnL**: -59.56 points (-1.0R)
- **MFE**: 23.97 points
- **MAE**: 64.69 points

### Trade #8 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 15:00:00
- **FVG 5m**: 22211.40 - 22213.98
- **Entrée**: 22165.52 @ 2025-01-03 15:01:00
- **Stop Loss**: 22225.08
- **Risk**: 59.56 points
- **TP 1RR**: 22105.96 ❌
- **TP 1.5RR**: 22076.18 ❌
- **TP 2RR**: 22046.40 ❌
- **TP 2.5RR**: 22016.61 ❌
- **TP 3RR**: 21986.83 ❌
- **TP 3.5RR**: 21957.05 ❌
- **TP 4RR**: 21927.27 ❌
- **TP 4.5RR**: 21897.49 ❌
- **TP 5RR**: 21867.71 ❌
- **PnL**: -59.56 points (-1.0R)
- **MFE**: 23.97 points
- **MAE**: 64.69 points

### Trade #9 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-06 21:45:00
- **FVG 5m**: 22401.35 - 22410.63
- **Entrée**: 22411.41 @ 2025-01-06 21:47:00
- **Stop Loss**: 22390.15
- **Risk**: 21.25 points
- **TP 1RR**: 22432.66 ❌
- **TP 1.5RR**: 22443.29 ❌
- **TP 2RR**: 22453.91 ❌
- **TP 2.5RR**: 22464.54 ❌
- **TP 3RR**: 22475.16 ❌
- **TP 3.5RR**: 22485.79 ❌
- **TP 4RR**: 22496.42 ❌
- **TP 4.5RR**: 22507.04 ❌
- **TP 5RR**: 22517.67 ❌
- **PnL**: -21.25 points (-1.0R)
- **MFE**: 9.79 points
- **MAE**: 27.06 points

### Trade #10 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 01:00:00
- **FVG 5m**: 22362.69 - 22389.24
- **Entrée**: 22389.76 @ 2025-01-07 01:08:00
- **Stop Loss**: 22351.51
- **Risk**: 38.24 points
- **TP 1RR**: 22428.00 ✅
- **TP 1.5RR**: 22447.12 ✅
- **TP 2RR**: 22466.24 ✅
- **TP 2.5RR**: 22485.37 ❌
- **TP 3RR**: 22504.49 ❌
- **TP 3.5RR**: 22523.61 ❌
- **TP 4RR**: 22542.73 ❌
- **TP 4.5RR**: 22561.85 ❌
- **TP 5RR**: 22580.98 ❌
- **PnL**: -38.24 points (-1.0R)
- **MFE**: 91.50 points
- **MAE**: 68.56 points

### Trade #11 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22453.42 - 22455.74
- **Entrée**: 22438.47 @ 2025-01-07 08:33:00
- **Stop Loss**: 22466.97
- **Risk**: 28.50 points
- **TP 1RR**: 22409.97 ✅
- **TP 1.5RR**: 22395.72 ✅
- **TP 2RR**: 22381.48 ✅
- **TP 2.5RR**: 22367.23 ✅
- **TP 3RR**: 22352.98 ❌
- **TP 3.5RR**: 22338.73 ❌
- **TP 4RR**: 22324.48 ❌
- **TP 4.5RR**: 22310.23 ❌
- **TP 5RR**: 22295.99 ❌
- **PnL**: -28.50 points (-1.0R)
- **MFE**: 71.39 points
- **MAE**: 29.12 points

### Trade #12 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22453.42 - 22455.74
- **Entrée**: 22438.47 @ 2025-01-07 08:33:00
- **Stop Loss**: 22466.97
- **Risk**: 28.50 points
- **TP 1RR**: 22409.97 ✅
- **TP 1.5RR**: 22395.72 ✅
- **TP 2RR**: 22381.48 ✅
- **TP 2.5RR**: 22367.23 ✅
- **TP 3RR**: 22352.98 ❌
- **TP 3.5RR**: 22338.73 ❌
- **TP 4RR**: 22324.48 ❌
- **TP 4.5RR**: 22310.23 ❌
- **TP 5RR**: 22295.99 ❌
- **PnL**: -28.50 points (-1.0R)
- **MFE**: 71.39 points
- **MAE**: 29.12 points

### Trade #13 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22453.42 - 22455.74
- **Entrée**: 22438.47 @ 2025-01-07 08:33:00
- **Stop Loss**: 22466.97
- **Risk**: 28.50 points
- **TP 1RR**: 22409.97 ✅
- **TP 1.5RR**: 22395.72 ✅
- **TP 2RR**: 22381.48 ✅
- **TP 2.5RR**: 22367.23 ✅
- **TP 3RR**: 22352.98 ❌
- **TP 3.5RR**: 22338.73 ❌
- **TP 4RR**: 22324.48 ❌
- **TP 4.5RR**: 22310.23 ❌
- **TP 5RR**: 22295.99 ❌
- **PnL**: -28.50 points (-1.0R)
- **MFE**: 71.39 points
- **MAE**: 29.12 points

### Trade #14 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 09:30:00
- **FVG 5m**: 22453.42 - 22455.74
- **Entrée**: 22183.05 @ 2025-01-07 09:31:00
- **Stop Loss**: 22466.97
- **Risk**: 283.92 points
- **TP 1RR**: 21899.13 ✅
- **TP 1.5RR**: 21757.17 ✅
- **TP 2RR**: 21615.21 ✅
- **TP 2.5RR**: 21473.25 ✅
- **TP 3RR**: 21331.29 ❌
- **TP 3.5RR**: 21189.33 ❌
- **TP 4RR**: 21047.37 ❌
- **TP 4.5RR**: 20905.41 ❌
- **TP 5RR**: 20763.45 ❌
- **PnL**: -283.92 points (-1.0R)
- **MFE**: 848.23 points
- **MAE**: 308.52 points

### Trade #15 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 09:30:00
- **FVG 5m**: 22453.42 - 22455.74
- **Entrée**: 22183.05 @ 2025-01-07 09:31:00
- **Stop Loss**: 22466.97
- **Risk**: 283.92 points
- **TP 1RR**: 21899.13 ✅
- **TP 1.5RR**: 21757.17 ✅
- **TP 2RR**: 21615.21 ✅
- **TP 2.5RR**: 21473.25 ✅
- **TP 3RR**: 21331.29 ❌
- **TP 3.5RR**: 21189.33 ❌
- **TP 4RR**: 21047.37 ❌
- **TP 4.5RR**: 20905.41 ❌
- **TP 5RR**: 20763.45 ❌
- **PnL**: -283.92 points (-1.0R)
- **MFE**: 848.23 points
- **MAE**: 308.52 points

### Trade #16 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 09:30:00
- **FVG 5m**: 22453.42 - 22455.74
- **Entrée**: 22183.05 @ 2025-01-07 09:31:00
- **Stop Loss**: 22466.97
- **Risk**: 283.92 points
- **TP 1RR**: 21899.13 ✅
- **TP 1.5RR**: 21757.17 ✅
- **TP 2RR**: 21615.21 ✅
- **TP 2.5RR**: 21473.25 ✅
- **TP 3RR**: 21331.29 ❌
- **TP 3.5RR**: 21189.33 ❌
- **TP 4RR**: 21047.37 ❌
- **TP 4.5RR**: 20905.41 ❌
- **TP 5RR**: 20763.45 ❌
- **PnL**: -283.92 points (-1.0R)
- **MFE**: 848.23 points
- **MAE**: 308.52 points

### Trade #17 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 09:45:00
- **FVG 5m**: 22124.02 - 22151.60
- **Entrée**: 22152.12 @ 2025-01-07 09:54:00
- **Stop Loss**: 22112.96
- **Risk**: 39.16 points
- **TP 1RR**: 22191.27 ✅
- **TP 1.5RR**: 22210.85 ✅
- **TP 2RR**: 22230.43 ✅
- **TP 2.5RR**: 22250.01 ❌
- **TP 3RR**: 22269.59 ❌
- **TP 3.5RR**: 22289.16 ❌
- **TP 4RR**: 22308.74 ❌
- **TP 4.5RR**: 22328.32 ❌
- **TP 5RR**: 22347.90 ❌
- **PnL**: -39.16 points (-1.0R)
- **MFE**: 89.18 points
- **MAE**: 40.21 points

### Trade #18 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 09:45:00
- **FVG 5m**: 22124.02 - 22151.60
- **Entrée**: 22152.12 @ 2025-01-07 09:54:00
- **Stop Loss**: 22112.96
- **Risk**: 39.16 points
- **TP 1RR**: 22191.27 ✅
- **TP 1.5RR**: 22210.85 ✅
- **TP 2RR**: 22230.43 ✅
- **TP 2.5RR**: 22250.01 ❌
- **TP 3RR**: 22269.59 ❌
- **TP 3.5RR**: 22289.16 ❌
- **TP 4RR**: 22308.74 ❌
- **TP 4.5RR**: 22328.32 ❌
- **TP 5RR**: 22347.90 ❌
- **PnL**: -39.16 points (-1.0R)
- **MFE**: 89.18 points
- **MAE**: 40.21 points

### Trade #19 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 10:45:00
- **FVG 5m**: 22194.90 - 22200.83
- **Entrée**: 22182.53 @ 2025-01-07 10:46:00
- **Stop Loss**: 22211.93
- **Risk**: 29.40 points
- **TP 1RR**: 22153.13 ✅
- **TP 1.5RR**: 22138.43 ✅
- **TP 2RR**: 22123.73 ✅
- **TP 2.5RR**: 22109.03 ✅
- **TP 3RR**: 22094.33 ✅
- **TP 3.5RR**: 22079.63 ✅
- **TP 4RR**: 22064.93 ✅
- **TP 4.5RR**: 22050.23 ✅
- **TP 5RR**: 22035.53 ✅
- **PnL**: 147.00 points (5.0R)
- **MFE**: 149.49 points
- **MAE**: 13.66 points

### Trade #20 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 11:45:00
- **FVG 5m**: 22103.15 - 22108.04
- **Entrée**: 22109.08 @ 2025-01-07 11:59:00
- **Stop Loss**: 22092.10
- **Risk**: 16.98 points
- **TP 1RR**: 22126.06 ✅
- **TP 1.5RR**: 22134.54 ✅
- **TP 2RR**: 22143.03 ✅
- **TP 2.5RR**: 22151.52 ✅
- **TP 3RR**: 22160.01 ✅
- **TP 3.5RR**: 22168.50 ✅
- **TP 4RR**: 22176.99 ✅
- **TP 4.5RR**: 22185.48 ❌
- **TP 5RR**: 22193.97 ❌
- **PnL**: -16.98 points (-1.0R)
- **MFE**: 74.49 points
- **MAE**: 17.78 points

### Trade #21 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 15:00:00
- **FVG 5m**: 22013.71 - 22019.12
- **Entrée**: 22040.00 @ 2025-01-07 15:01:00
- **Stop Loss**: 22002.70
- **Risk**: 37.30 points
- **TP 1RR**: 22077.30 ✅
- **TP 1.5RR**: 22095.95 ✅
- **TP 2RR**: 22114.59 ❌
- **TP 2.5RR**: 22133.24 ❌
- **TP 3RR**: 22151.89 ❌
- **TP 3.5RR**: 22170.54 ❌
- **TP 4RR**: 22189.19 ❌
- **TP 4.5RR**: 22207.83 ❌
- **TP 5RR**: 22226.48 ❌
- **PnL**: -37.30 points (-1.0R)
- **MFE**: 72.43 points
- **MAE**: 49.49 points

### Trade #22 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 01:45:00
- **FVG 5m**: 22054.18 - 22059.33
- **Entrée**: 22060.88 @ 2025-01-08 02:13:00
- **Stop Loss**: 22043.15
- **Risk**: 17.73 points
- **TP 1RR**: 22078.61 ✅
- **TP 1.5RR**: 22087.47 ✅
- **TP 2RR**: 22096.33 ✅
- **TP 2.5RR**: 22105.20 ✅
- **TP 3RR**: 22114.06 ❌
- **TP 3.5RR**: 22122.93 ❌
- **TP 4RR**: 22131.79 ❌
- **TP 4.5RR**: 22140.66 ❌
- **TP 5RR**: 22149.52 ❌
- **PnL**: -17.73 points (-1.0R)
- **MFE**: 51.55 points
- **MAE**: 26.81 points

### Trade #23 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 05:00:00
- **FVG 5m**: 22087.17 - 22093.87
- **Entrée**: 22085.62 @ 2025-01-08 05:19:00
- **Stop Loss**: 22104.92
- **Risk**: 19.29 points
- **TP 1RR**: 22066.33 ✅
- **TP 1.5RR**: 22056.68 ✅
- **TP 2RR**: 22047.03 ✅
- **TP 2.5RR**: 22037.38 ✅
- **TP 3RR**: 22027.74 ✅
- **TP 3.5RR**: 22018.09 ✅
- **TP 4RR**: 22008.44 ✅
- **TP 4.5RR**: 21998.79 ✅
- **TP 5RR**: 21989.15 ✅
- **PnL**: 96.47 points (5.0R)
- **MFE**: 107.74 points
- **MAE**: 1.03 points

### Trade #24 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 05:00:00
- **FVG 5m**: 22087.17 - 22093.87
- **Entrée**: 22085.62 @ 2025-01-08 05:19:00
- **Stop Loss**: 22104.92
- **Risk**: 19.29 points
- **TP 1RR**: 22066.33 ✅
- **TP 1.5RR**: 22056.68 ✅
- **TP 2RR**: 22047.03 ✅
- **TP 2.5RR**: 22037.38 ✅
- **TP 3RR**: 22027.74 ✅
- **TP 3.5RR**: 22018.09 ✅
- **TP 4RR**: 22008.44 ✅
- **TP 4.5RR**: 21998.79 ✅
- **TP 5RR**: 21989.15 ✅
- **PnL**: 96.47 points (5.0R)
- **MFE**: 107.74 points
- **MAE**: 1.03 points

### Trade #25 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 06:15:00
- **FVG 5m**: 21981.49 - 21997.22
- **Entrée**: 21959.84 @ 2025-01-08 06:16:00
- **Stop Loss**: 22008.21
- **Risk**: 48.37 points
- **TP 1RR**: 21911.47 ✅
- **TP 1.5RR**: 21887.29 ✅
- **TP 2RR**: 21863.10 ❌
- **TP 2.5RR**: 21838.92 ❌
- **TP 3RR**: 21814.73 ❌
- **TP 3.5RR**: 21790.54 ❌
- **TP 4RR**: 21766.36 ❌
- **TP 4.5RR**: 21742.17 ❌
- **TP 5RR**: 21717.99 ❌
- **PnL**: -48.37 points (-1.0R)
- **MFE**: 81.19 points
- **MAE**: 55.93 points

### Trade #26 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 06:30:00
- **FVG 5m**: 21927.63 - 21930.72
- **Entrée**: 21934.84 @ 2025-01-08 06:37:00
- **Stop Loss**: 21916.66
- **Risk**: 18.18 points
- **TP 1RR**: 21953.02 ✅
- **TP 1.5RR**: 21962.11 ❌
- **TP 2RR**: 21971.20 ❌
- **TP 2.5RR**: 21980.29 ❌
- **TP 3RR**: 21989.38 ❌
- **TP 3.5RR**: 21998.47 ❌
- **TP 4RR**: 22007.56 ❌
- **TP 4.5RR**: 22016.65 ❌
- **TP 5RR**: 22025.74 ❌
- **PnL**: -18.18 points (-1.0R)
- **MFE**: 22.17 points
- **MAE**: 21.65 points

### Trade #27 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 09:00:00
- **FVG 5m**: 22017.58 - 22019.90
- **Entrée**: 22012.94 @ 2025-01-08 09:08:00
- **Stop Loss**: 22030.91
- **Risk**: 17.97 points
- **TP 1RR**: 21994.97 ✅
- **TP 1.5RR**: 21985.98 ✅
- **TP 2RR**: 21977.00 ✅
- **TP 2.5RR**: 21968.02 ✅
- **TP 3RR**: 21959.03 ✅
- **TP 3.5RR**: 21950.05 ✅
- **TP 4RR**: 21941.06 ✅
- **TP 4.5RR**: 21932.08 ✅
- **TP 5RR**: 21923.09 ✅
- **PnL**: 89.84 points (5.0R)
- **MFE**: 98.46 points
- **MAE**: 16.24 points

### Trade #28 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 11:15:00
- **FVG 5m**: 22032.27 - 22039.23
- **Entrée**: 21948.50 @ 2025-01-08 11:16:00
- **Stop Loss**: 22050.25
- **Risk**: 101.74 points
- **TP 1RR**: 21846.76 ✅
- **TP 1.5RR**: 21795.89 ❌
- **TP 2RR**: 21745.01 ❌
- **TP 2.5RR**: 21694.14 ❌
- **TP 3RR**: 21643.27 ❌
- **TP 3.5RR**: 21592.40 ❌
- **TP 4RR**: 21541.52 ❌
- **TP 4.5RR**: 21490.65 ❌
- **TP 5RR**: 21439.78 ❌
- **PnL**: -101.74 points (-1.0R)
- **MFE**: 126.81 points
- **MAE**: 104.13 points

### Trade #29 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21912.16 - 21930.46
- **Entrée**: 21943.09 @ 2025-01-08 11:58:00
- **Stop Loss**: 21901.20
- **Risk**: 41.89 points
- **TP 1RR**: 21984.97 ✅
- **TP 1.5RR**: 22005.92 ✅
- **TP 2RR**: 22026.86 ✅
- **TP 2.5RR**: 22047.80 ✅
- **TP 3RR**: 22068.75 ✅
- **TP 3.5RR**: 22089.69 ✅
- **TP 4RR**: 22110.63 ❌
- **TP 4.5RR**: 22131.57 ❌
- **TP 5RR**: 22152.52 ❌
- **PnL**: -41.89 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 44.33 points

### Trade #30 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21912.16 - 21930.46
- **Entrée**: 21943.09 @ 2025-01-08 11:58:00
- **Stop Loss**: 21901.20
- **Risk**: 41.89 points
- **TP 1RR**: 21984.97 ✅
- **TP 1.5RR**: 22005.92 ✅
- **TP 2RR**: 22026.86 ✅
- **TP 2.5RR**: 22047.80 ✅
- **TP 3RR**: 22068.75 ✅
- **TP 3.5RR**: 22089.69 ✅
- **TP 4RR**: 22110.63 ❌
- **TP 4.5RR**: 22131.57 ❌
- **TP 5RR**: 22152.52 ❌
- **PnL**: -41.89 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 44.33 points

### Trade #31 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21912.16 - 21930.46
- **Entrée**: 21943.09 @ 2025-01-08 11:58:00
- **Stop Loss**: 21901.20
- **Risk**: 41.89 points
- **TP 1RR**: 21984.97 ✅
- **TP 1.5RR**: 22005.92 ✅
- **TP 2RR**: 22026.86 ✅
- **TP 2.5RR**: 22047.80 ✅
- **TP 3RR**: 22068.75 ✅
- **TP 3.5RR**: 22089.69 ✅
- **TP 4RR**: 22110.63 ❌
- **TP 4.5RR**: 22131.57 ❌
- **TP 5RR**: 22152.52 ❌
- **PnL**: -41.89 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 44.33 points

### Trade #32 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21912.16 - 21930.46
- **Entrée**: 21943.09 @ 2025-01-08 11:58:00
- **Stop Loss**: 21901.20
- **Risk**: 41.89 points
- **TP 1RR**: 21984.97 ✅
- **TP 1.5RR**: 22005.92 ✅
- **TP 2RR**: 22026.86 ✅
- **TP 2.5RR**: 22047.80 ✅
- **TP 3RR**: 22068.75 ✅
- **TP 3.5RR**: 22089.69 ✅
- **TP 4RR**: 22110.63 ❌
- **TP 4.5RR**: 22131.57 ❌
- **TP 5RR**: 22152.52 ❌
- **PnL**: -41.89 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 44.33 points

### Trade #33 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21912.16 - 21930.46
- **Entrée**: 21943.09 @ 2025-01-08 11:58:00
- **Stop Loss**: 21901.20
- **Risk**: 41.89 points
- **TP 1RR**: 21984.97 ✅
- **TP 1.5RR**: 22005.92 ✅
- **TP 2RR**: 22026.86 ✅
- **TP 2.5RR**: 22047.80 ✅
- **TP 3RR**: 22068.75 ✅
- **TP 3.5RR**: 22089.69 ✅
- **TP 4RR**: 22110.63 ❌
- **TP 4.5RR**: 22131.57 ❌
- **TP 5RR**: 22152.52 ❌
- **PnL**: -41.89 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 44.33 points

### Trade #34 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21912.16 - 21930.46
- **Entrée**: 21943.09 @ 2025-01-08 11:58:00
- **Stop Loss**: 21901.20
- **Risk**: 41.89 points
- **TP 1RR**: 21984.97 ✅
- **TP 1.5RR**: 22005.92 ✅
- **TP 2RR**: 22026.86 ✅
- **TP 2.5RR**: 22047.80 ✅
- **TP 3RR**: 22068.75 ✅
- **TP 3.5RR**: 22089.69 ✅
- **TP 4RR**: 22110.63 ❌
- **TP 4.5RR**: 22131.57 ❌
- **TP 5RR**: 22152.52 ❌
- **PnL**: -41.89 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 44.33 points

### Trade #35 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21912.16 - 21930.46
- **Entrée**: 21943.09 @ 2025-01-08 11:58:00
- **Stop Loss**: 21901.20
- **Risk**: 41.89 points
- **TP 1RR**: 21984.97 ✅
- **TP 1.5RR**: 22005.92 ✅
- **TP 2RR**: 22026.86 ✅
- **TP 2.5RR**: 22047.80 ✅
- **TP 3RR**: 22068.75 ✅
- **TP 3.5RR**: 22089.69 ✅
- **TP 4RR**: 22110.63 ❌
- **TP 4.5RR**: 22131.57 ❌
- **TP 5RR**: 22152.52 ❌
- **PnL**: -41.89 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 44.33 points

### Trade #36 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 02:15:00
- **FVG 5m**: 21937.16 - 21940.77
- **Entrée**: 21944.12 @ 2025-01-09 02:30:00
- **Stop Loss**: 21926.19
- **Risk**: 17.93 points
- **TP 1RR**: 21962.05 ✅
- **TP 1.5RR**: 21971.01 ✅
- **TP 2RR**: 21979.98 ✅
- **TP 2.5RR**: 21988.94 ✅
- **TP 3RR**: 21997.90 ❌
- **TP 3.5RR**: 22006.87 ❌
- **TP 4RR**: 22015.83 ❌
- **TP 4.5RR**: 22024.79 ❌
- **TP 5RR**: 22033.76 ❌
- **PnL**: -17.93 points (-1.0R)
- **MFE**: 51.03 points
- **MAE**: 18.30 points

### Trade #37 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 02:30:00
- **FVG 5m**: 21937.16 - 21940.77
- **Entrée**: 21947.21 @ 2025-01-09 02:33:00
- **Stop Loss**: 21926.19
- **Risk**: 21.02 points
- **TP 1RR**: 21968.23 ✅
- **TP 1.5RR**: 21978.74 ✅
- **TP 2RR**: 21989.25 ✅
- **TP 2.5RR**: 21999.76 ❌
- **TP 3RR**: 22010.28 ❌
- **TP 3.5RR**: 22020.79 ❌
- **TP 4RR**: 22031.30 ❌
- **TP 4.5RR**: 22041.81 ❌
- **TP 5RR**: 22052.32 ❌
- **PnL**: -21.02 points (-1.0R)
- **MFE**: 47.94 points
- **MAE**: 21.39 points

### Trade #38 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 19:00:00
- **FVG 5m**: 21863.96 - 21871.70
- **Entrée**: 21872.98 @ 2025-01-09 19:03:00
- **Stop Loss**: 21853.03
- **Risk**: 19.95 points
- **TP 1RR**: 21892.94 ✅
- **TP 1.5RR**: 21902.91 ✅
- **TP 2RR**: 21912.89 ✅
- **TP 2.5RR**: 21922.87 ✅
- **TP 3RR**: 21932.84 ✅
- **TP 3.5RR**: 21942.82 ✅
- **TP 4RR**: 21952.80 ✅
- **TP 4.5RR**: 21962.77 ✅
- **TP 5RR**: 21972.75 ✅
- **PnL**: 99.76 points (5.0R)
- **MFE**: 101.03 points
- **MAE**: 2.06 points

### Trade #39 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-09 23:30:00
- **FVG 5m**: 21957.52 - 21960.62
- **Entrée**: 21953.40 @ 2025-01-10 00:00:00
- **Stop Loss**: 21971.60
- **Risk**: 18.20 points
- **TP 1RR**: 21935.20 ✅
- **TP 1.5RR**: 21926.10 ✅
- **TP 2RR**: 21917.01 ✅
- **TP 2.5RR**: 21907.91 ✅
- **TP 3RR**: 21898.81 ✅
- **TP 3.5RR**: 21889.71 ❌
- **TP 4RR**: 21880.61 ❌
- **TP 4.5RR**: 21871.51 ❌
- **TP 5RR**: 21862.41 ❌
- **PnL**: -18.20 points (-1.0R)
- **MFE**: 62.12 points
- **MAE**: 20.88 points

### Trade #40 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 05:15:00
- **FVG 5m**: 21983.56 - 22005.21
- **Entrée**: 21981.75 @ 2025-01-10 05:53:00
- **Stop Loss**: 22016.21
- **Risk**: 34.46 points
- **TP 1RR**: 21947.29 ✅
- **TP 1.5RR**: 21930.07 ✅
- **TP 2RR**: 21912.84 ✅
- **TP 2.5RR**: 21895.61 ✅
- **TP 3RR**: 21878.38 ✅
- **TP 3.5RR**: 21861.15 ✅
- **TP 4RR**: 21843.92 ✅
- **TP 4.5RR**: 21826.69 ✅
- **TP 5RR**: 21809.47 ✅
- **PnL**: 172.29 points (5.0R)
- **MFE**: 259.03 points
- **MAE**: 10.57 points

### Trade #41 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 05:45:00
- **FVG 5m**: 22006.49 - 22016.03
- **Entrée**: 21998.76 @ 2025-01-10 05:46:00
- **Stop Loss**: 22027.04
- **Risk**: 28.28 points
- **TP 1RR**: 21970.49 ✅
- **TP 1.5RR**: 21956.35 ✅
- **TP 2RR**: 21942.21 ✅
- **TP 2.5RR**: 21928.07 ✅
- **TP 3RR**: 21913.93 ✅
- **TP 3.5RR**: 21899.79 ✅
- **TP 4RR**: 21885.66 ✅
- **TP 4.5RR**: 21871.52 ✅
- **TP 5RR**: 21857.38 ✅
- **PnL**: 141.38 points (5.0R)
- **MFE**: 276.04 points
- **MAE**: 5.15 points

### Trade #42 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 05:45:00
- **FVG 5m**: 22006.49 - 22016.03
- **Entrée**: 21998.76 @ 2025-01-10 05:46:00
- **Stop Loss**: 22027.04
- **Risk**: 28.28 points
- **TP 1RR**: 21970.49 ✅
- **TP 1.5RR**: 21956.35 ✅
- **TP 2RR**: 21942.21 ✅
- **TP 2.5RR**: 21928.07 ✅
- **TP 3RR**: 21913.93 ✅
- **TP 3.5RR**: 21899.79 ✅
- **TP 4RR**: 21885.66 ✅
- **TP 4.5RR**: 21871.52 ✅
- **TP 5RR**: 21857.38 ✅
- **PnL**: 141.38 points (5.0R)
- **MFE**: 276.04 points
- **MAE**: 5.15 points

### Trade #43 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 06:00:00
- **FVG 5m**: 22006.49 - 22016.03
- **Entrée**: 21975.31 @ 2025-01-10 06:01:00
- **Stop Loss**: 22027.04
- **Risk**: 51.73 points
- **TP 1RR**: 21923.58 ✅
- **TP 1.5RR**: 21897.71 ✅
- **TP 2RR**: 21871.85 ✅
- **TP 2.5RR**: 21845.98 ✅
- **TP 3RR**: 21820.11 ✅
- **TP 3.5RR**: 21794.25 ✅
- **TP 4RR**: 21768.38 ✅
- **TP 4.5RR**: 21742.52 ✅
- **TP 5RR**: 21716.65 ✅
- **PnL**: 258.66 points (5.0R)
- **MFE**: 272.43 points
- **MAE**: 8.51 points

### Trade #44 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-10 09:15:00
- **FVG 5m**: 21564.98 - 21577.61
- **Entrée**: 21586.89 @ 2025-01-10 09:18:00
- **Stop Loss**: 21554.20
- **Risk**: 32.69 points
- **TP 1RR**: 21619.58 ✅
- **TP 1.5RR**: 21635.93 ✅
- **TP 2RR**: 21652.27 ✅
- **TP 2.5RR**: 21668.62 ✅
- **TP 3RR**: 21684.96 ✅
- **TP 3.5RR**: 21701.31 ✅
- **TP 4RR**: 21717.65 ✅
- **TP 4.5RR**: 21734.00 ✅
- **TP 5RR**: 21750.34 ✅
- **PnL**: 163.45 points (5.0R)
- **MFE**: 183.00 points
- **MAE**: 5.67 points

### Trade #45 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 01:15:00
- **FVG 5m**: 21528.38 - 21535.08
- **Entrée**: 21535.60 @ 2025-01-13 01:16:00
- **Stop Loss**: 21517.62
- **Risk**: 17.98 points
- **TP 1RR**: 21553.58 ❌
- **TP 1.5RR**: 21562.57 ❌
- **TP 2RR**: 21571.56 ❌
- **TP 2.5RR**: 21580.55 ❌
- **TP 3RR**: 21589.54 ❌
- **TP 3.5RR**: 21598.53 ❌
- **TP 4RR**: 21607.52 ❌
- **TP 4.5RR**: 21616.51 ❌
- **TP 5RR**: 21625.51 ❌
- **PnL**: -17.98 points (-1.0R)
- **MFE**: 6.96 points
- **MAE**: 22.17 points

### Trade #46 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 08:30:00
- **FVG 5m**: 21418.59 - 21422.97
- **Entrée**: 21425.03 @ 2025-01-13 08:44:00
- **Stop Loss**: 21407.88
- **Risk**: 17.15 points
- **TP 1RR**: 21442.18 ❌
- **TP 1.5RR**: 21450.76 ❌
- **TP 2RR**: 21459.33 ❌
- **TP 2.5RR**: 21467.91 ❌
- **TP 3RR**: 21476.49 ❌
- **TP 3.5RR**: 21485.06 ❌
- **TP 4RR**: 21493.64 ❌
- **TP 4.5RR**: 21502.22 ❌
- **TP 5RR**: 21510.79 ❌
- **PnL**: -17.15 points (-1.0R)
- **MFE**: 0.00 points
- **MAE**: 34.28 points

### Trade #47 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-13 09:45:00
- **FVG 5m**: 21419.87 - 21452.61
- **Entrée**: 21413.17 @ 2025-01-13 10:05:00
- **Stop Loss**: 21463.33
- **Risk**: 50.16 points
- **TP 1RR**: 21363.01 ❌
- **TP 1.5RR**: 21337.93 ❌
- **TP 2RR**: 21312.85 ❌
- **TP 2.5RR**: 21287.77 ❌
- **TP 3RR**: 21262.69 ❌
- **TP 3.5RR**: 21237.61 ❌
- **TP 4RR**: 21212.53 ❌
- **TP 4.5RR**: 21187.45 ❌
- **TP 5RR**: 21162.37 ❌
- **PnL**: -50.16 points (-1.0R)
- **MFE**: 27.06 points
- **MAE**: 51.29 points

### Trade #48 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 11:45:00
- **FVG 5m**: 21407.76 - 21414.98
- **Entrée**: 21484.57 @ 2025-01-13 11:46:00
- **Stop Loss**: 21397.06
- **Risk**: 87.51 points
- **TP 1RR**: 21572.08 ✅
- **TP 1.5RR**: 21615.83 ✅
- **TP 2RR**: 21659.59 ✅
- **TP 2.5RR**: 21703.34 ✅
- **TP 3RR**: 21747.10 ✅
- **TP 3.5RR**: 21790.86 ✅
- **TP 4RR**: 21834.61 ✅
- **TP 4.5RR**: 21878.37 ✅
- **TP 5RR**: 21922.12 ✅
- **PnL**: 437.55 points (5.0R)
- **MFE**: 460.58 points
- **MAE**: 67.79 points

### Trade #49 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 11:45:00
- **FVG 5m**: 21407.76 - 21414.98
- **Entrée**: 21484.57 @ 2025-01-13 11:46:00
- **Stop Loss**: 21397.06
- **Risk**: 87.51 points
- **TP 1RR**: 21572.08 ✅
- **TP 1.5RR**: 21615.83 ✅
- **TP 2RR**: 21659.59 ✅
- **TP 2.5RR**: 21703.34 ✅
- **TP 3RR**: 21747.10 ✅
- **TP 3.5RR**: 21790.86 ✅
- **TP 4RR**: 21834.61 ✅
- **TP 4.5RR**: 21878.37 ✅
- **TP 5RR**: 21922.12 ✅
- **PnL**: 437.55 points (5.0R)
- **MFE**: 460.58 points
- **MAE**: 67.79 points

### Trade #50 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-13 12:30:00
- **FVG 5m**: 21514.21 - 21524.78
- **Entrée**: 21510.34 @ 2025-01-13 13:13:00
- **Stop Loss**: 21535.54
- **Risk**: 25.20 points
- **TP 1RR**: 21485.15 ✅
- **TP 1.5RR**: 21472.55 ❌
- **TP 2RR**: 21459.95 ❌
- **TP 2.5RR**: 21447.35 ❌
- **TP 3RR**: 21434.75 ❌
- **TP 3.5RR**: 21422.16 ❌
- **TP 4RR**: 21409.56 ❌
- **TP 4.5RR**: 21396.96 ❌
- **TP 5RR**: 21384.36 ❌
- **PnL**: -25.20 points (-1.0R)
- **MFE**: 29.90 points
- **MAE**: 25.77 points

### Trade #51 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 14:45:00
- **FVG 5m**: 21542.04 - 21546.94
- **Entrée**: 21549.52 @ 2025-01-13 14:46:00
- **Stop Loss**: 21531.27
- **Risk**: 18.25 points
- **TP 1RR**: 21567.76 ✅
- **TP 1.5RR**: 21576.89 ✅
- **TP 2RR**: 21586.01 ✅
- **TP 2.5RR**: 21595.13 ✅
- **TP 3RR**: 21604.25 ✅
- **TP 3.5RR**: 21613.38 ✅
- **TP 4RR**: 21622.50 ✅
- **TP 4.5RR**: 21631.62 ✅
- **TP 5RR**: 21640.75 ✅
- **PnL**: 91.23 points (5.0R)
- **MFE**: 92.53 points
- **MAE**: 11.86 points

### Trade #52 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 15:15:00
- **FVG 5m**: 21542.04 - 21546.94
- **Entrée**: 21626.07 @ 2025-01-13 15:16:00
- **Stop Loss**: 21531.27
- **Risk**: 94.79 points
- **TP 1RR**: 21720.86 ✅
- **TP 1.5RR**: 21768.26 ✅
- **TP 2RR**: 21815.66 ❌
- **TP 2.5RR**: 21863.05 ❌
- **TP 3RR**: 21910.45 ❌
- **TP 3.5RR**: 21957.85 ❌
- **TP 4RR**: 22005.25 ❌
- **TP 4.5RR**: 22052.64 ❌
- **TP 5RR**: 22100.04 ❌
- **PnL**: -94.79 points (-1.0R)
- **MFE**: 172.43 points
- **MAE**: 103.87 points

### Trade #53 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 00:30:00
- **FVG 5m**: 21710.09 - 21712.67
- **Entrée**: 21704.68 @ 2025-01-14 00:31:00
- **Stop Loss**: 21723.53
- **Risk**: 18.85 points
- **TP 1RR**: 21685.83 ✅
- **TP 1.5RR**: 21676.41 ✅
- **TP 2RR**: 21666.99 ❌
- **TP 2.5RR**: 21657.56 ❌
- **TP 3RR**: 21648.14 ❌
- **TP 3.5RR**: 21638.72 ❌
- **TP 4RR**: 21629.29 ❌
- **TP 4.5RR**: 21619.87 ❌
- **TP 5RR**: 21610.45 ❌
- **PnL**: -18.85 points (-1.0R)
- **MFE**: 32.48 points
- **MAE**: 21.39 points

### Trade #54 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 01:00:00
- **FVG 5m**: 21710.09 - 21712.67
- **Entrée**: 21687.41 @ 2025-01-14 01:01:00
- **Stop Loss**: 21723.53
- **Risk**: 36.12 points
- **TP 1RR**: 21651.30 ❌
- **TP 1.5RR**: 21633.24 ❌
- **TP 2RR**: 21615.18 ❌
- **TP 2.5RR**: 21597.12 ❌
- **TP 3RR**: 21579.07 ❌
- **TP 3.5RR**: 21561.01 ❌
- **TP 4RR**: 21542.95 ❌
- **TP 4.5RR**: 21524.89 ❌
- **TP 5RR**: 21506.84 ❌
- **PnL**: -36.12 points (-1.0R)
- **MFE**: 15.21 points
- **MAE**: 38.66 points

### Trade #55 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 06:30:00
- **FVG 5m**: 21680.71 - 21689.47
- **Entrée**: 21770.92 @ 2025-01-14 07:30:00
- **Stop Loss**: 21669.87
- **Risk**: 101.05 points
- **TP 1RR**: 21871.97 ❌
- **TP 1.5RR**: 21922.49 ❌
- **TP 2RR**: 21973.02 ❌
- **TP 2.5RR**: 22023.54 ❌
- **TP 3RR**: 22074.07 ❌
- **TP 3.5RR**: 22124.59 ❌
- **TP 4RR**: 22175.12 ❌
- **TP 4.5RR**: 22225.64 ❌
- **TP 5RR**: 22276.17 ❌
- **PnL**: -101.05 points (-1.0R)
- **MFE**: 22.17 points
- **MAE**: 101.81 points

### Trade #56 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 07:30:00
- **FVG 5m**: 21611.38 - 21617.30
- **Entrée**: 21777.88 @ 2025-01-14 07:31:00
- **Stop Loss**: 21600.57
- **Risk**: 177.31 points
- **TP 1RR**: 21955.18 ❌
- **TP 1.5RR**: 22043.84 ❌
- **TP 2RR**: 22132.49 ❌
- **TP 2.5RR**: 22221.14 ❌
- **TP 3RR**: 22309.80 ❌
- **TP 3.5RR**: 22398.45 ❌
- **TP 4RR**: 22487.10 ❌
- **TP 4.5RR**: 22575.76 ❌
- **TP 5RR**: 22664.41 ❌
- **PnL**: -177.31 points (-1.0R)
- **MFE**: 10.83 points
- **MAE**: 180.93 points

### Trade #57 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 10:00:00
- **FVG 5m**: 21681.48 - 21706.23
- **Entrée**: 21576.84 @ 2025-01-14 10:01:00
- **Stop Loss**: 21717.08
- **Risk**: 140.24 points
- **TP 1RR**: 21436.60 ✅
- **TP 1.5RR**: 21366.48 ❌
- **TP 2RR**: 21296.36 ❌
- **TP 2.5RR**: 21226.24 ❌
- **TP 3RR**: 21156.12 ❌
- **TP 3.5RR**: 21086.00 ❌
- **TP 4RR**: 21015.88 ❌
- **TP 4.5RR**: 20945.76 ❌
- **TP 5RR**: 20875.64 ❌
- **PnL**: -140.24 points (-1.0R)
- **MFE**: 160.06 points
- **MAE**: 298.98 points

### Trade #58 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 12:30:00
- **FVG 5m**: 21479.67 - 21485.34
- **Entrée**: 21582.77 @ 2025-01-14 12:31:00
- **Stop Loss**: 21468.93
- **Risk**: 113.84 points
- **TP 1RR**: 21696.60 ❌
- **TP 1.5RR**: 21753.52 ❌
- **TP 2RR**: 21810.44 ❌
- **TP 2.5RR**: 21867.36 ❌
- **TP 3RR**: 21924.28 ❌
- **TP 3.5RR**: 21981.19 ❌
- **TP 4RR**: 22038.11 ❌
- **TP 4.5RR**: 22095.03 ❌
- **TP 5RR**: 22151.95 ❌
- **PnL**: -113.84 points (-1.0R)
- **MFE**: 81.19 points
- **MAE**: 128.36 points

### Trade #59 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 02:00:00
- **FVG 5m**: 21585.60 - 21591.79
- **Entrée**: 21594.62 @ 2025-01-15 02:25:00
- **Stop Loss**: 21574.81
- **Risk**: 19.81 points
- **TP 1RR**: 21614.44 ❌
- **TP 1.5RR**: 21624.34 ❌
- **TP 2RR**: 21634.25 ❌
- **TP 2.5RR**: 21644.16 ❌
- **TP 3RR**: 21654.06 ❌
- **TP 3.5RR**: 21663.97 ❌
- **TP 4RR**: 21673.88 ❌
- **TP 4.5RR**: 21683.79 ❌
- **TP 5RR**: 21693.69 ❌
- **PnL**: -19.81 points (-1.0R)
- **MFE**: 5.93 points
- **MAE**: 20.36 points

### Trade #60 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 02:15:00
- **FVG 5m**: 21585.60 - 21591.79
- **Entrée**: 21594.62 @ 2025-01-15 02:25:00
- **Stop Loss**: 21574.81
- **Risk**: 19.81 points
- **TP 1RR**: 21614.44 ❌
- **TP 1.5RR**: 21624.34 ❌
- **TP 2RR**: 21634.25 ❌
- **TP 2.5RR**: 21644.16 ❌
- **TP 3RR**: 21654.06 ❌
- **TP 3.5RR**: 21663.97 ❌
- **TP 4RR**: 21673.88 ❌
- **TP 4.5RR**: 21683.79 ❌
- **TP 5RR**: 21693.69 ❌
- **PnL**: -19.81 points (-1.0R)
- **MFE**: 5.93 points
- **MAE**: 20.36 points

### Trade #61 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 07:30:00
- **FVG 5m**: 21643.59 - 21653.65
- **Entrée**: 21849.27 @ 2025-01-15 07:31:00
- **Stop Loss**: 21632.77
- **Risk**: 216.50 points
- **TP 1RR**: 22065.77 ✅
- **TP 1.5RR**: 22174.02 ✅
- **TP 2RR**: 22282.27 ✅
- **TP 2.5RR**: 22390.52 ✅
- **TP 3RR**: 22498.77 ✅
- **TP 3.5RR**: 22607.02 ✅
- **TP 4RR**: 22715.27 ✅
- **TP 4.5RR**: 22823.52 ❌
- **TP 5RR**: 22931.77 ❌
- **PnL**: -216.50 points (-1.0R)
- **MFE**: 928.39 points
- **MAE**: 233.26 points

### Trade #62 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 07:30:00
- **FVG 5m**: 21643.59 - 21653.65
- **Entrée**: 21849.27 @ 2025-01-15 07:31:00
- **Stop Loss**: 21632.77
- **Risk**: 216.50 points
- **TP 1RR**: 22065.77 ✅
- **TP 1.5RR**: 22174.02 ✅
- **TP 2RR**: 22282.27 ✅
- **TP 2.5RR**: 22390.52 ✅
- **TP 3RR**: 22498.77 ✅
- **TP 3.5RR**: 22607.02 ✅
- **TP 4RR**: 22715.27 ✅
- **TP 4.5RR**: 22823.52 ❌
- **TP 5RR**: 22931.77 ❌
- **PnL**: -216.50 points (-1.0R)
- **MFE**: 928.39 points
- **MAE**: 233.26 points

### Trade #63 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 07:30:00
- **FVG 5m**: 21643.59 - 21653.65
- **Entrée**: 21849.27 @ 2025-01-15 07:31:00
- **Stop Loss**: 21632.77
- **Risk**: 216.50 points
- **TP 1RR**: 22065.77 ✅
- **TP 1.5RR**: 22174.02 ✅
- **TP 2RR**: 22282.27 ✅
- **TP 2.5RR**: 22390.52 ✅
- **TP 3RR**: 22498.77 ✅
- **TP 3.5RR**: 22607.02 ✅
- **TP 4RR**: 22715.27 ✅
- **TP 4.5RR**: 22823.52 ❌
- **TP 5RR**: 22931.77 ❌
- **PnL**: -216.50 points (-1.0R)
- **MFE**: 928.39 points
- **MAE**: 233.26 points

### Trade #64 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 09:30:00
- **FVG 5m**: 22000.31 - 22004.69
- **Entrée**: 21989.74 @ 2025-01-15 09:58:00
- **Stop Loss**: 22015.69
- **Risk**: 25.95 points
- **TP 1RR**: 21963.79 ❌
- **TP 1.5RR**: 21950.81 ❌
- **TP 2RR**: 21937.84 ❌
- **TP 2.5RR**: 21924.86 ❌
- **TP 3RR**: 21911.89 ❌
- **TP 3.5RR**: 21898.91 ❌
- **TP 4RR**: 21885.94 ❌
- **TP 4.5RR**: 21872.96 ❌
- **TP 5RR**: 21859.98 ❌
- **PnL**: -25.95 points (-1.0R)
- **MFE**: 11.08 points
- **MAE**: 34.54 points

### Trade #65 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 09:45:00
- **FVG 5m**: 22000.31 - 22004.69
- **Entrée**: 21989.74 @ 2025-01-15 09:58:00
- **Stop Loss**: 22015.69
- **Risk**: 25.95 points
- **TP 1RR**: 21963.79 ❌
- **TP 1.5RR**: 21950.81 ❌
- **TP 2RR**: 21937.84 ❌
- **TP 2.5RR**: 21924.86 ❌
- **TP 3RR**: 21911.89 ❌
- **TP 3.5RR**: 21898.91 ❌
- **TP 4RR**: 21885.94 ❌
- **TP 4.5RR**: 21872.96 ❌
- **TP 5RR**: 21859.98 ❌
- **PnL**: -25.95 points (-1.0R)
- **MFE**: 11.08 points
- **MAE**: 34.54 points

### Trade #66 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 14:30:00
- **FVG 5m**: 22086.91 - 22094.64
- **Entrée**: 22083.04 @ 2025-01-15 14:41:00
- **Stop Loss**: 22105.69
- **Risk**: 22.65 points
- **TP 1RR**: 22060.40 ✅
- **TP 1.5RR**: 22049.07 ✅
- **TP 2RR**: 22037.75 ✅
- **TP 2.5RR**: 22026.43 ❌
- **TP 3RR**: 22015.11 ❌
- **TP 3.5RR**: 22003.78 ❌
- **TP 4RR**: 21992.46 ❌
- **TP 4.5RR**: 21981.14 ❌
- **TP 5RR**: 21969.82 ❌
- **PnL**: -22.65 points (-1.0R)
- **MFE**: 51.55 points
- **MAE**: 28.87 points

### Trade #67 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 14:45:00
- **FVG 5m**: 22086.91 - 22094.64
- **Entrée**: 22080.21 @ 2025-01-15 14:47:00
- **Stop Loss**: 22105.69
- **Risk**: 25.48 points
- **TP 1RR**: 22054.73 ✅
- **TP 1.5RR**: 22041.99 ✅
- **TP 2RR**: 22029.25 ❌
- **TP 2.5RR**: 22016.51 ❌
- **TP 3RR**: 22003.77 ❌
- **TP 3.5RR**: 21991.03 ❌
- **TP 4RR**: 21978.28 ❌
- **TP 4.5RR**: 21965.54 ❌
- **TP 5RR**: 21952.80 ❌
- **PnL**: -25.48 points (-1.0R)
- **MFE**: 48.71 points
- **MAE**: 31.70 points

### Trade #68 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 02:00:00
- **FVG 5m**: 22188.20 - 22192.84
- **Entrée**: 22186.14 @ 2025-01-16 02:09:00
- **Stop Loss**: 22203.94
- **Risk**: 17.80 points
- **TP 1RR**: 22168.34 ❌
- **TP 1.5RR**: 22159.44 ❌
- **TP 2RR**: 22150.54 ❌
- **TP 2.5RR**: 22141.65 ❌
- **TP 3RR**: 22132.75 ❌
- **TP 3.5RR**: 22123.85 ❌
- **TP 4RR**: 22114.95 ❌
- **TP 4.5RR**: 22106.05 ❌
- **TP 5RR**: 22097.15 ❌
- **PnL**: -17.80 points (-1.0R)
- **MFE**: 16.24 points
- **MAE**: 20.88 points

### Trade #69 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 06:45:00
- **FVG 5m**: 22165.52 - 22167.84
- **Entrée**: 22126.09 @ 2025-01-16 06:46:00
- **Stop Loss**: 22178.92
- **Risk**: 52.84 points
- **TP 1RR**: 22073.25 ✅
- **TP 1.5RR**: 22046.83 ✅
- **TP 2RR**: 22020.41 ✅
- **TP 2.5RR**: 21993.99 ✅
- **TP 3RR**: 21967.57 ✅
- **TP 3.5RR**: 21941.15 ✅
- **TP 4RR**: 21914.73 ✅
- **TP 4.5RR**: 21888.32 ✅
- **TP 5RR**: 21861.90 ✅
- **PnL**: 264.19 points (5.0R)
- **MFE**: 272.43 points
- **MAE**: 39.95 points

### Trade #70 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 06:45:00
- **FVG 5m**: 22165.52 - 22167.84
- **Entrée**: 22126.09 @ 2025-01-16 06:46:00
- **Stop Loss**: 22178.92
- **Risk**: 52.84 points
- **TP 1RR**: 22073.25 ✅
- **TP 1.5RR**: 22046.83 ✅
- **TP 2RR**: 22020.41 ✅
- **TP 2.5RR**: 21993.99 ✅
- **TP 3RR**: 21967.57 ✅
- **TP 3.5RR**: 21941.15 ✅
- **TP 4RR**: 21914.73 ✅
- **TP 4.5RR**: 21888.32 ✅
- **TP 5RR**: 21861.90 ✅
- **PnL**: 264.19 points (5.0R)
- **MFE**: 272.43 points
- **MAE**: 39.95 points

### Trade #71 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 06:45:00
- **FVG 5m**: 22165.52 - 22167.84
- **Entrée**: 22126.09 @ 2025-01-16 06:46:00
- **Stop Loss**: 22178.92
- **Risk**: 52.84 points
- **TP 1RR**: 22073.25 ✅
- **TP 1.5RR**: 22046.83 ✅
- **TP 2RR**: 22020.41 ✅
- **TP 2.5RR**: 21993.99 ✅
- **TP 3RR**: 21967.57 ✅
- **TP 3.5RR**: 21941.15 ✅
- **TP 4RR**: 21914.73 ✅
- **TP 4.5RR**: 21888.32 ✅
- **TP 5RR**: 21861.90 ✅
- **PnL**: 264.19 points (5.0R)
- **MFE**: 272.43 points
- **MAE**: 39.95 points

### Trade #72 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 07:15:00
- **FVG 5m**: 22119.39 - 22130.47
- **Entrée**: 22136.91 @ 2025-01-16 07:50:00
- **Stop Loss**: 22108.33
- **Risk**: 28.59 points
- **TP 1RR**: 22165.50 ✅
- **TP 1.5RR**: 22179.79 ❌
- **TP 2RR**: 22194.08 ❌
- **TP 2.5RR**: 22208.38 ❌
- **TP 3RR**: 22222.67 ❌
- **TP 3.5RR**: 22236.96 ❌
- **TP 4RR**: 22251.26 ❌
- **TP 4.5RR**: 22265.55 ❌
- **TP 5RR**: 22279.84 ❌
- **PnL**: -28.59 points (-1.0R)
- **MFE**: 29.12 points
- **MAE**: 38.66 points

### Trade #73 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 13:00:00
- **FVG 5m**: 21994.64 - 21999.54
- **Entrée**: 22000.57 @ 2025-01-16 13:12:00
- **Stop Loss**: 21983.64
- **Risk**: 16.93 points
- **TP 1RR**: 22017.49 ❌
- **TP 1.5RR**: 22025.95 ❌
- **TP 2RR**: 22034.42 ❌
- **TP 2.5RR**: 22042.88 ❌
- **TP 3RR**: 22051.34 ❌
- **TP 3.5RR**: 22059.81 ❌
- **TP 4RR**: 22068.27 ❌
- **TP 4.5RR**: 22076.73 ❌
- **TP 5RR**: 22085.19 ❌
- **PnL**: -16.93 points (-1.0R)
- **MFE**: 7.73 points
- **MAE**: 21.65 points

### Trade #74 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-17 08:15:00
- **FVG 5m**: 21993.61 - 22001.60
- **Entrée**: 22279.70 @ 2025-01-17 08:16:00
- **Stop Loss**: 21982.61
- **Risk**: 297.09 points
- **TP 1RR**: 22576.79 ✅
- **TP 1.5RR**: 22725.34 ✅
- **TP 2RR**: 22873.88 ❌
- **TP 2.5RR**: 23022.43 ❌
- **TP 3RR**: 23170.97 ❌
- **TP 3.5RR**: 23319.52 ❌
- **TP 4RR**: 23468.06 ❌
- **TP 4.5RR**: 23616.61 ❌
- **TP 5RR**: 23765.15 ❌
- **PnL**: -297.09 points (-1.0R)
- **MFE**: 497.96 points
- **MAE**: 300.01 points

### Trade #75 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-17 08:15:00
- **FVG 5m**: 21993.61 - 22001.60
- **Entrée**: 22279.70 @ 2025-01-17 08:16:00
- **Stop Loss**: 21982.61
- **Risk**: 297.09 points
- **TP 1RR**: 22576.79 ✅
- **TP 1.5RR**: 22725.34 ✅
- **TP 2RR**: 22873.88 ❌
- **TP 2.5RR**: 23022.43 ❌
- **TP 3RR**: 23170.97 ❌
- **TP 3.5RR**: 23319.52 ❌
- **TP 4RR**: 23468.06 ❌
- **TP 4.5RR**: 23616.61 ❌
- **TP 5RR**: 23765.15 ❌
- **PnL**: -297.09 points (-1.0R)
- **MFE**: 497.96 points
- **MAE**: 300.01 points

### Trade #76 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-17 08:30:00
- **FVG 5m**: 22257.28 - 22265.52
- **Entrée**: 22252.90 @ 2025-01-17 08:31:00
- **Stop Loss**: 22276.66
- **Risk**: 23.76 points
- **TP 1RR**: 22229.13 ✅
- **TP 1.5RR**: 22217.25 ✅
- **TP 2RR**: 22205.37 ✅
- **TP 2.5RR**: 22193.49 ✅
- **TP 3RR**: 22181.61 ✅
- **TP 3.5RR**: 22169.73 ✅
- **TP 4RR**: 22157.85 ✅
- **TP 4.5RR**: 22145.97 ❌
- **TP 5RR**: 22134.08 ❌
- **PnL**: -23.76 points (-1.0R)
- **MFE**: 106.45 points
- **MAE**: 35.31 points

### Trade #77 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-17 08:30:00
- **FVG 5m**: 22257.28 - 22265.52
- **Entrée**: 22252.90 @ 2025-01-17 08:31:00
- **Stop Loss**: 22276.66
- **Risk**: 23.76 points
- **TP 1RR**: 22229.13 ✅
- **TP 1.5RR**: 22217.25 ✅
- **TP 2RR**: 22205.37 ✅
- **TP 2.5RR**: 22193.49 ✅
- **TP 3RR**: 22181.61 ✅
- **TP 3.5RR**: 22169.73 ✅
- **TP 4RR**: 22157.85 ✅
- **TP 4.5RR**: 22145.97 ❌
- **TP 5RR**: 22134.08 ❌
- **PnL**: -23.76 points (-1.0R)
- **MFE**: 106.45 points
- **MAE**: 35.31 points

### Trade #78 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-17 12:30:00
- **FVG 5m**: 22330.48 - 22333.05
- **Entrée**: 22324.29 @ 2025-01-17 12:31:00
- **Stop Loss**: 22344.22
- **Risk**: 19.93 points
- **TP 1RR**: 22304.36 ✅
- **TP 1.5RR**: 22294.40 ✅
- **TP 2RR**: 22284.43 ✅
- **TP 2.5RR**: 22274.47 ✅
- **TP 3RR**: 22264.50 ✅
- **TP 3.5RR**: 22254.54 ✅
- **TP 4RR**: 22244.57 ✅
- **TP 4.5RR**: 22234.61 ✅
- **TP 5RR**: 22224.64 ✅
- **PnL**: 99.65 points (5.0R)
- **MFE**: 103.35 points
- **MAE**: 6.44 points

### Trade #79 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 06:15:00
- **FVG 5m**: 22287.69 - 22290.01
- **Entrée**: 22276.87 @ 2025-01-20 06:16:00
- **Stop Loss**: 22301.16
- **Risk**: 24.29 points
- **TP 1RR**: 22252.58 ✅
- **TP 1.5RR**: 22240.43 ✅
- **TP 2RR**: 22228.29 ✅
- **TP 2.5RR**: 22216.14 ❌
- **TP 3RR**: 22204.00 ❌
- **TP 3.5RR**: 22191.85 ❌
- **TP 4RR**: 22179.71 ❌
- **TP 4.5RR**: 22167.56 ❌
- **TP 5RR**: 22155.42 ❌
- **PnL**: -24.29 points (-1.0R)
- **MFE**: 71.91 points
- **MAE**: 42.27 points

### Trade #80 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 07:30:00
- **FVG 5m**: 22254.96 - 22257.53
- **Entrée**: 22292.59 @ 2025-01-20 07:31:00
- **Stop Loss**: 22243.83
- **Risk**: 48.76 points
- **TP 1RR**: 22341.35 ✅
- **TP 1.5RR**: 22365.72 ✅
- **TP 2RR**: 22390.10 ✅
- **TP 2.5RR**: 22414.48 ✅
- **TP 3RR**: 22438.86 ✅
- **TP 3.5RR**: 22463.24 ❌
- **TP 4RR**: 22487.62 ❌
- **TP 4.5RR**: 22512.00 ❌
- **TP 5RR**: 22536.38 ❌
- **PnL**: -48.76 points (-1.0R)
- **MFE**: 160.57 points
- **MAE**: 70.62 points

### Trade #81 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 07:45:00
- **FVG 5m**: 22254.96 - 22257.53
- **Entrée**: 22322.49 @ 2025-01-20 07:46:00
- **Stop Loss**: 22243.83
- **Risk**: 78.66 points
- **TP 1RR**: 22401.14 ✅
- **TP 1.5RR**: 22440.47 ✅
- **TP 2RR**: 22479.80 ❌
- **TP 2.5RR**: 22519.12 ❌
- **TP 3RR**: 22558.45 ❌
- **TP 3.5RR**: 22597.78 ❌
- **TP 4RR**: 22637.11 ❌
- **TP 4.5RR**: 22676.44 ❌
- **TP 5RR**: 22715.76 ❌
- **PnL**: -78.66 points (-1.0R)
- **MFE**: 130.67 points
- **MAE**: 100.52 points

### Trade #82 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 11:15:00
- **FVG 5m**: 22349.29 - 22354.96
- **Entrée**: 22367.85 @ 2025-01-20 11:16:00
- **Stop Loss**: 22338.12
- **Risk**: 29.73 points
- **TP 1RR**: 22397.58 ❌
- **TP 1.5RR**: 22412.45 ❌
- **TP 2RR**: 22427.31 ❌
- **TP 2.5RR**: 22442.18 ❌
- **TP 3RR**: 22457.04 ❌
- **TP 3.5RR**: 22471.91 ❌
- **TP 4RR**: 22486.78 ❌
- **TP 4.5RR**: 22501.64 ❌
- **TP 5RR**: 22516.51 ❌
- **PnL**: -29.73 points (-1.0R)
- **MFE**: 15.21 points
- **MAE**: 31.19 points

### Trade #83 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 18:15:00
- **FVG 5m**: 22395.68 - 22402.90
- **Entrée**: 22393.62 @ 2025-01-20 18:17:00
- **Stop Loss**: 22414.10
- **Risk**: 20.48 points
- **TP 1RR**: 22373.14 ✅
- **TP 1.5RR**: 22362.90 ✅
- **TP 2RR**: 22352.66 ✅
- **TP 2.5RR**: 22342.42 ✅
- **TP 3RR**: 22332.18 ✅
- **TP 3.5RR**: 22321.94 ✅
- **TP 4RR**: 22311.70 ✅
- **TP 4.5RR**: 22301.46 ✅
- **TP 5RR**: 22291.22 ✅
- **PnL**: 102.40 points (5.0R)
- **MFE**: 139.70 points
- **MAE**: 4.64 points

### Trade #84 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 18:45:00
- **FVG 5m**: 22395.68 - 22402.90
- **Entrée**: 22374.81 @ 2025-01-20 18:46:00
- **Stop Loss**: 22414.10
- **Risk**: 39.30 points
- **TP 1RR**: 22335.51 ✅
- **TP 1.5RR**: 22315.86 ✅
- **TP 2RR**: 22296.22 ✅
- **TP 2.5RR**: 22276.57 ✅
- **TP 3RR**: 22256.92 ✅
- **TP 3.5RR**: 22237.27 ✅
- **TP 4RR**: 22217.63 ✅
- **TP 4.5RR**: 22197.98 ✅
- **TP 5RR**: 22178.33 ✅
- **PnL**: 196.48 points (5.0R)
- **MFE**: 206.71 points
- **MAE**: 1.29 points

### Trade #85 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 18:45:00
- **FVG 5m**: 22395.68 - 22402.90
- **Entrée**: 22374.81 @ 2025-01-20 18:46:00
- **Stop Loss**: 22414.10
- **Risk**: 39.30 points
- **TP 1RR**: 22335.51 ✅
- **TP 1.5RR**: 22315.86 ✅
- **TP 2RR**: 22296.22 ✅
- **TP 2.5RR**: 22276.57 ✅
- **TP 3RR**: 22256.92 ✅
- **TP 3.5RR**: 22237.27 ✅
- **TP 4RR**: 22217.63 ✅
- **TP 4.5RR**: 22197.98 ✅
- **TP 5RR**: 22178.33 ✅
- **PnL**: 196.48 points (5.0R)
- **MFE**: 206.71 points
- **MAE**: 1.29 points

### Trade #86 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 18:45:00
- **FVG 5m**: 22395.68 - 22402.90
- **Entrée**: 22374.81 @ 2025-01-20 18:46:00
- **Stop Loss**: 22414.10
- **Risk**: 39.30 points
- **TP 1RR**: 22335.51 ✅
- **TP 1.5RR**: 22315.86 ✅
- **TP 2RR**: 22296.22 ✅
- **TP 2.5RR**: 22276.57 ✅
- **TP 3RR**: 22256.92 ✅
- **TP 3.5RR**: 22237.27 ✅
- **TP 4RR**: 22217.63 ✅
- **TP 4.5RR**: 22197.98 ✅
- **TP 5RR**: 22178.33 ✅
- **PnL**: 196.48 points (5.0R)
- **MFE**: 206.71 points
- **MAE**: 1.29 points

### Trade #87 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 18:45:00
- **FVG 5m**: 22395.68 - 22402.90
- **Entrée**: 22374.81 @ 2025-01-20 18:46:00
- **Stop Loss**: 22414.10
- **Risk**: 39.30 points
- **TP 1RR**: 22335.51 ✅
- **TP 1.5RR**: 22315.86 ✅
- **TP 2RR**: 22296.22 ✅
- **TP 2.5RR**: 22276.57 ✅
- **TP 3RR**: 22256.92 ✅
- **TP 3.5RR**: 22237.27 ✅
- **TP 4RR**: 22217.63 ✅
- **TP 4.5RR**: 22197.98 ✅
- **TP 5RR**: 22178.33 ✅
- **PnL**: 196.48 points (5.0R)
- **MFE**: 206.71 points
- **MAE**: 1.29 points

### Trade #88 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 18:45:00
- **FVG 5m**: 22395.68 - 22402.90
- **Entrée**: 22374.81 @ 2025-01-20 18:46:00
- **Stop Loss**: 22414.10
- **Risk**: 39.30 points
- **TP 1RR**: 22335.51 ✅
- **TP 1.5RR**: 22315.86 ✅
- **TP 2RR**: 22296.22 ✅
- **TP 2.5RR**: 22276.57 ✅
- **TP 3RR**: 22256.92 ✅
- **TP 3.5RR**: 22237.27 ✅
- **TP 4RR**: 22217.63 ✅
- **TP 4.5RR**: 22197.98 ✅
- **TP 5RR**: 22178.33 ✅
- **PnL**: 196.48 points (5.0R)
- **MFE**: 206.71 points
- **MAE**: 1.29 points

### Trade #89 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-21 08:30:00
- **FVG 5m**: 22380.99 - 22391.04
- **Entrée**: 22371.71 @ 2025-01-21 08:31:00
- **Stop Loss**: 22402.24
- **Risk**: 30.53 points
- **TP 1RR**: 22341.19 ✅
- **TP 1.5RR**: 22325.92 ✅
- **TP 2RR**: 22310.66 ✅
- **TP 2.5RR**: 22295.40 ✅
- **TP 3RR**: 22280.14 ✅
- **TP 3.5RR**: 22264.87 ✅
- **TP 4RR**: 22249.61 ✅
- **TP 4.5RR**: 22234.35 ✅
- **TP 5RR**: 22219.08 ✅
- **PnL**: 152.63 points (5.0R)
- **MFE**: 166.24 points
- **MAE**: 13.92 points

### Trade #90 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-21 13:00:00
- **FVG 5m**: 22419.40 - 22428.93
- **Entrée**: 22418.88 @ 2025-01-21 13:14:00
- **Stop Loss**: 22440.15
- **Risk**: 21.27 points
- **TP 1RR**: 22397.61 ✅
- **TP 1.5RR**: 22386.98 ✅
- **TP 2RR**: 22376.35 ✅
- **TP 2.5RR**: 22365.71 ❌
- **TP 3RR**: 22355.08 ❌
- **TP 3.5RR**: 22344.45 ❌
- **TP 4RR**: 22333.82 ❌
- **TP 4.5RR**: 22323.18 ❌
- **TP 5RR**: 22312.55 ❌
- **PnL**: -21.27 points (-1.0R)
- **MFE**: 50.00 points
- **MAE**: 30.41 points

### Trade #91 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-21 13:30:00
- **FVG 5m**: 22419.40 - 22428.93
- **Entrée**: 22396.97 @ 2025-01-21 13:31:00
- **Stop Loss**: 22440.15
- **Risk**: 43.17 points
- **TP 1RR**: 22353.80 ❌
- **TP 1.5RR**: 22332.21 ❌
- **TP 2RR**: 22310.62 ❌
- **TP 2.5RR**: 22289.04 ❌
- **TP 3RR**: 22267.45 ❌
- **TP 3.5RR**: 22245.86 ❌
- **TP 4RR**: 22224.28 ❌
- **TP 4.5RR**: 22202.69 ❌
- **TP 5RR**: 22181.10 ❌
- **PnL**: -43.17 points (-1.0R)
- **MFE**: 28.09 points
- **MAE**: 52.32 points

### Trade #92 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-21 14:30:00
- **FVG 5m**: 22419.40 - 22428.93
- **Entrée**: 22409.09 @ 2025-01-21 14:34:00
- **Stop Loss**: 22440.15
- **Risk**: 31.06 points
- **TP 1RR**: 22378.03 ✅
- **TP 1.5RR**: 22362.50 ❌
- **TP 2RR**: 22346.97 ❌
- **TP 2.5RR**: 22331.44 ❌
- **TP 3RR**: 22315.90 ❌
- **TP 3.5RR**: 22300.37 ❌
- **TP 4RR**: 22284.84 ❌
- **TP 4.5RR**: 22269.31 ❌
- **TP 5RR**: 22253.78 ❌
- **PnL**: -31.06 points (-1.0R)
- **MFE**: 39.69 points
- **MAE**: 40.21 points

### Trade #93 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-22 00:45:00
- **FVG 5m**: 22532.03 - 22539.25
- **Entrée**: 22530.23 @ 2025-01-22 00:46:00
- **Stop Loss**: 22550.52
- **Risk**: 20.29 points
- **TP 1RR**: 22509.93 ❌
- **TP 1.5RR**: 22499.79 ❌
- **TP 2RR**: 22489.64 ❌
- **TP 2.5RR**: 22479.50 ❌
- **TP 3RR**: 22469.35 ❌
- **TP 3.5RR**: 22459.21 ❌
- **TP 4RR**: 22449.06 ❌
- **TP 4.5RR**: 22438.92 ❌
- **TP 5RR**: 22428.77 ❌
- **PnL**: -20.29 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 21.13 points

### Trade #94 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 02:45:00
- **FVG 5m**: 22563.73 - 22567.08
- **Entrée**: 22568.63 @ 2025-01-23 03:07:00
- **Stop Loss**: 22552.45
- **Risk**: 16.18 points
- **TP 1RR**: 22584.81 ❌
- **TP 1.5RR**: 22592.90 ❌
- **TP 2RR**: 22600.99 ❌
- **TP 2.5RR**: 22609.08 ❌
- **TP 3RR**: 22617.17 ❌
- **TP 3.5RR**: 22625.26 ❌
- **TP 4RR**: 22633.34 ❌
- **TP 4.5RR**: 22641.43 ❌
- **TP 5RR**: 22649.52 ❌
- **PnL**: -16.18 points (-1.0R)
- **MFE**: 0.77 points
- **MAE**: 18.30 points

### Trade #95 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 03:15:00
- **FVG 5m**: 22563.73 - 22567.08
- **Entrée**: 22569.66 @ 2025-01-23 03:45:00
- **Stop Loss**: 22552.45
- **Risk**: 17.21 points
- **TP 1RR**: 22586.87 ❌
- **TP 1.5RR**: 22595.47 ❌
- **TP 2RR**: 22604.08 ❌
- **TP 2.5RR**: 22612.68 ❌
- **TP 3RR**: 22621.29 ❌
- **TP 3.5RR**: 22629.89 ❌
- **TP 4RR**: 22638.50 ❌
- **TP 4.5RR**: 22647.10 ❌
- **TP 5RR**: 22655.71 ❌
- **PnL**: -17.21 points (-1.0R)
- **MFE**: 15.72 points
- **MAE**: 18.56 points

### Trade #96 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 06:45:00
- **FVG 5m**: 22561.67 - 22563.99
- **Entrée**: 22573.01 @ 2025-01-23 06:46:00
- **Stop Loss**: 22550.39
- **Risk**: 22.62 points
- **TP 1RR**: 22595.63 ✅
- **TP 1.5RR**: 22606.94 ❌
- **TP 2RR**: 22618.25 ❌
- **TP 2.5RR**: 22629.56 ❌
- **TP 3RR**: 22640.87 ❌
- **TP 3.5RR**: 22652.19 ❌
- **TP 4RR**: 22663.50 ❌
- **TP 4.5RR**: 22674.81 ❌
- **TP 5RR**: 22686.12 ❌
- **PnL**: -22.62 points (-1.0R)
- **MFE**: 25.26 points
- **MAE**: 28.35 points

### Trade #97 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 07:00:00
- **FVG 5m**: 22562.96 - 22567.34
- **Entrée**: 22560.38 @ 2025-01-23 07:10:00
- **Stop Loss**: 22578.62
- **Risk**: 18.24 points
- **TP 1RR**: 22542.14 ❌
- **TP 1.5RR**: 22533.02 ❌
- **TP 2RR**: 22523.90 ❌
- **TP 2.5RR**: 22514.77 ❌
- **TP 3RR**: 22505.65 ❌
- **TP 3.5RR**: 22496.53 ❌
- **TP 4RR**: 22487.41 ❌
- **TP 4.5RR**: 22478.29 ❌
- **TP 5RR**: 22469.17 ❌
- **PnL**: -18.24 points (-1.0R)
- **MFE**: 0.77 points
- **MAE**: 18.30 points

### Trade #98 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 07:30:00
- **FVG 5m**: 22562.96 - 22567.34
- **Entrée**: 22562.70 @ 2025-01-23 07:33:00
- **Stop Loss**: 22578.62
- **Risk**: 15.92 points
- **TP 1RR**: 22546.78 ❌
- **TP 1.5RR**: 22538.82 ❌
- **TP 2RR**: 22530.85 ❌
- **TP 2.5RR**: 22522.89 ❌
- **TP 3RR**: 22514.93 ❌
- **TP 3.5RR**: 22506.97 ❌
- **TP 4RR**: 22499.01 ❌
- **TP 4.5RR**: 22491.05 ❌
- **TP 5RR**: 22483.09 ❌
- **PnL**: -15.92 points (-1.0R)
- **MFE**: 3.09 points
- **MAE**: 18.56 points

### Trade #99 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 10:00:00
- **FVG 5m**: 22569.40 - 22572.24
- **Entrée**: 22615.02 @ 2025-01-23 10:01:00
- **Stop Loss**: 22558.12
- **Risk**: 56.90 points
- **TP 1RR**: 22671.93 ✅
- **TP 1.5RR**: 22700.38 ✅
- **TP 2RR**: 22728.83 ✅
- **TP 2.5RR**: 22757.28 ✅
- **TP 3RR**: 22785.74 ❌
- **TP 3.5RR**: 22814.19 ❌
- **TP 4RR**: 22842.64 ❌
- **TP 4.5RR**: 22871.09 ❌
- **TP 5RR**: 22899.55 ❌
- **PnL**: -56.90 points (-1.0R)
- **MFE**: 146.91 points
- **MAE**: 67.79 points

### Trade #100 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 12:30:00
- **FVG 5m**: 22634.87 - 22641.83
- **Entrée**: 22633.58 @ 2025-01-23 12:56:00
- **Stop Loss**: 22653.15
- **Risk**: 19.57 points
- **TP 1RR**: 22614.01 ✅
- **TP 1.5RR**: 22604.23 ✅
- **TP 2RR**: 22594.44 ❌
- **TP 2.5RR**: 22584.66 ❌
- **TP 3RR**: 22574.87 ❌
- **TP 3.5RR**: 22565.09 ❌
- **TP 4RR**: 22555.31 ❌
- **TP 4.5RR**: 22545.52 ❌
- **TP 5RR**: 22535.74 ❌
- **PnL**: -19.57 points (-1.0R)
- **MFE**: 30.93 points
- **MAE**: 24.49 points

### Trade #101 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 12:30:00
- **FVG 5m**: 22634.87 - 22641.83
- **Entrée**: 22633.58 @ 2025-01-23 12:56:00
- **Stop Loss**: 22653.15
- **Risk**: 19.57 points
- **TP 1RR**: 22614.01 ✅
- **TP 1.5RR**: 22604.23 ✅
- **TP 2RR**: 22594.44 ❌
- **TP 2.5RR**: 22584.66 ❌
- **TP 3RR**: 22574.87 ❌
- **TP 3.5RR**: 22565.09 ❌
- **TP 4RR**: 22555.31 ❌
- **TP 4.5RR**: 22545.52 ❌
- **TP 5RR**: 22535.74 ❌
- **PnL**: -19.57 points (-1.0R)
- **MFE**: 30.93 points
- **MAE**: 24.49 points

### Trade #102 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 12:30:00
- **FVG 5m**: 22634.87 - 22641.83
- **Entrée**: 22633.58 @ 2025-01-23 12:56:00
- **Stop Loss**: 22653.15
- **Risk**: 19.57 points
- **TP 1RR**: 22614.01 ✅
- **TP 1.5RR**: 22604.23 ✅
- **TP 2RR**: 22594.44 ❌
- **TP 2.5RR**: 22584.66 ❌
- **TP 3RR**: 22574.87 ❌
- **TP 3.5RR**: 22565.09 ❌
- **TP 4RR**: 22555.31 ❌
- **TP 4.5RR**: 22545.52 ❌
- **TP 5RR**: 22535.74 ❌
- **PnL**: -19.57 points (-1.0R)
- **MFE**: 30.93 points
- **MAE**: 24.49 points

### Trade #103 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 22:15:00
- **FVG 5m**: 22713.48 - 22721.73
- **Entrée**: 22670.95 @ 2025-01-23 22:16:00
- **Stop Loss**: 22733.09
- **Risk**: 62.14 points
- **TP 1RR**: 22608.82 ❌
- **TP 1.5RR**: 22577.75 ❌
- **TP 2RR**: 22546.68 ❌
- **TP 2.5RR**: 22515.61 ❌
- **TP 3RR**: 22484.54 ❌
- **TP 3.5RR**: 22453.48 ❌
- **TP 4RR**: 22422.41 ❌
- **TP 4.5RR**: 22391.34 ❌
- **TP 5RR**: 22360.27 ❌
- **PnL**: -62.14 points (-1.0R)
- **MFE**: 18.82 points
- **MAE**: 62.63 points

### Trade #104 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 02:00:00
- **FVG 5m**: 22671.47 - 22676.11
- **Entrée**: 22678.94 @ 2025-01-24 02:10:00
- **Stop Loss**: 22660.13
- **Risk**: 18.81 points
- **TP 1RR**: 22697.75 ❌
- **TP 1.5RR**: 22707.16 ❌
- **TP 2RR**: 22716.56 ❌
- **TP 2.5RR**: 22725.97 ❌
- **TP 3RR**: 22735.37 ❌
- **TP 3.5RR**: 22744.78 ❌
- **TP 4RR**: 22754.18 ❌
- **TP 4.5RR**: 22763.59 ❌
- **TP 5RR**: 22772.99 ❌
- **PnL**: -18.81 points (-1.0R)
- **MFE**: 10.83 points
- **MAE**: 22.42 points

### Trade #105 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 09:00:00
- **FVG 5m**: 22726.62 - 22730.75
- **Entrée**: 22720.70 @ 2025-01-24 09:02:00
- **Stop Loss**: 22742.11
- **Risk**: 21.42 points
- **TP 1RR**: 22699.28 ✅
- **TP 1.5RR**: 22688.57 ✅
- **TP 2RR**: 22677.86 ✅
- **TP 2.5RR**: 22667.15 ✅
- **TP 3RR**: 22656.44 ✅
- **TP 3.5RR**: 22645.74 ✅
- **TP 4RR**: 22635.03 ✅
- **TP 4.5RR**: 22624.32 ✅
- **TP 5RR**: 22613.61 ✅
- **PnL**: 107.09 points (5.0R)
- **MFE**: 110.83 points
- **MAE**: 0.26 points

### Trade #106 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 09:00:00
- **FVG 5m**: 22726.62 - 22730.75
- **Entrée**: 22720.70 @ 2025-01-24 09:02:00
- **Stop Loss**: 22742.11
- **Risk**: 21.42 points
- **TP 1RR**: 22699.28 ✅
- **TP 1.5RR**: 22688.57 ✅
- **TP 2RR**: 22677.86 ✅
- **TP 2.5RR**: 22667.15 ✅
- **TP 3RR**: 22656.44 ✅
- **TP 3.5RR**: 22645.74 ✅
- **TP 4RR**: 22635.03 ✅
- **TP 4.5RR**: 22624.32 ✅
- **TP 5RR**: 22613.61 ✅
- **PnL**: 107.09 points (5.0R)
- **MFE**: 110.83 points
- **MAE**: 0.26 points

### Trade #107 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 09:00:00
- **FVG 5m**: 22726.62 - 22730.75
- **Entrée**: 22720.70 @ 2025-01-24 09:02:00
- **Stop Loss**: 22742.11
- **Risk**: 21.42 points
- **TP 1RR**: 22699.28 ✅
- **TP 1.5RR**: 22688.57 ✅
- **TP 2RR**: 22677.86 ✅
- **TP 2.5RR**: 22667.15 ✅
- **TP 3RR**: 22656.44 ✅
- **TP 3.5RR**: 22645.74 ✅
- **TP 4RR**: 22635.03 ✅
- **TP 4.5RR**: 22624.32 ✅
- **TP 5RR**: 22613.61 ✅
- **PnL**: 107.09 points (5.0R)
- **MFE**: 110.83 points
- **MAE**: 0.26 points

### Trade #108 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 10:45:00
- **FVG 5m**: 22679.46 - 22683.58
- **Entrée**: 22676.11 @ 2025-01-24 10:56:00
- **Stop Loss**: 22694.92
- **Risk**: 18.82 points
- **TP 1RR**: 22657.29 ✅
- **TP 1.5RR**: 22647.88 ✅
- **TP 2RR**: 22638.47 ✅
- **TP 2.5RR**: 22629.07 ✅
- **TP 3RR**: 22619.66 ✅
- **TP 3.5RR**: 22610.25 ✅
- **TP 4RR**: 22600.84 ✅
- **TP 4.5RR**: 22591.43 ✅
- **TP 5RR**: 22582.03 ✅
- **PnL**: 94.08 points (5.0R)
- **MFE**: 98.72 points
- **MAE**: 13.66 points

### Trade #109 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 12:30:00
- **FVG 5m**: 22679.46 - 22683.58
- **Entrée**: 22623.27 @ 2025-01-24 12:31:00
- **Stop Loss**: 22694.92
- **Risk**: 71.65 points
- **TP 1RR**: 22551.62 ✅
- **TP 1.5RR**: 22515.79 ✅
- **TP 2RR**: 22479.96 ✅
- **TP 2.5RR**: 22444.14 ✅
- **TP 3RR**: 22408.31 ✅
- **TP 3.5RR**: 22372.48 ✅
- **TP 4RR**: 22336.66 ✅
- **TP 4.5RR**: 22300.83 ✅
- **TP 5RR**: 22265.00 ✅
- **PnL**: 358.27 points (5.0R)
- **MFE**: 369.86 points
- **MAE**: 1.03 points

### Trade #110 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 14:00:00
- **FVG 5m**: 22568.11 - 22573.27
- **Entrée**: 22575.59 @ 2025-01-24 14:54:00
- **Stop Loss**: 22556.83
- **Risk**: 18.76 points
- **TP 1RR**: 22594.35 ✅
- **TP 1.5RR**: 22603.73 ❌
- **TP 2RR**: 22613.10 ❌
- **TP 2.5RR**: 22622.48 ❌
- **TP 3RR**: 22631.86 ❌
- **TP 3.5RR**: 22641.24 ❌
- **TP 4RR**: 22650.62 ❌
- **TP 4.5RR**: 22660.00 ❌
- **TP 5RR**: 22669.38 ❌
- **PnL**: -18.76 points (-1.0R)
- **MFE**: 22.42 points
- **MAE**: 213.67 points

### Trade #111 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 14:45:00
- **FVG 5m**: 22568.11 - 22573.27
- **Entrée**: 22575.59 @ 2025-01-24 14:54:00
- **Stop Loss**: 22556.83
- **Risk**: 18.76 points
- **TP 1RR**: 22594.35 ✅
- **TP 1.5RR**: 22603.73 ❌
- **TP 2RR**: 22613.10 ❌
- **TP 2.5RR**: 22622.48 ❌
- **TP 3RR**: 22631.86 ❌
- **TP 3.5RR**: 22641.24 ❌
- **TP 4RR**: 22650.62 ❌
- **TP 4.5RR**: 22660.00 ❌
- **TP 5RR**: 22669.38 ❌
- **PnL**: -18.76 points (-1.0R)
- **MFE**: 22.42 points
- **MAE**: 213.67 points

### Trade #112 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 00:30:00
- **FVG 5m**: 22157.02 - 22161.40
- **Entrée**: 22074.28 @ 2025-01-27 00:31:00
- **Stop Loss**: 22172.48
- **Risk**: 98.20 points
- **TP 1RR**: 21976.08 ✅
- **TP 1.5RR**: 21926.98 ✅
- **TP 2RR**: 21877.89 ✅
- **TP 2.5RR**: 21828.79 ✅
- **TP 3RR**: 21779.69 ✅
- **TP 3.5RR**: 21730.59 ✅
- **TP 4RR**: 21681.49 ✅
- **TP 4.5RR**: 21632.39 ✅
- **TP 5RR**: 21583.29 ✅
- **PnL**: 490.99 points (5.0R)
- **MFE**: 496.15 points
- **MAE**: 1.29 points

### Trade #113 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 01:45:00
- **FVG 5m**: 22039.49 - 22049.54
- **Entrée**: 21995.41 @ 2025-01-27 01:46:00
- **Stop Loss**: 22060.56
- **Risk**: 65.15 points
- **TP 1RR**: 21930.26 ✅
- **TP 1.5RR**: 21897.69 ✅
- **TP 2RR**: 21865.11 ✅
- **TP 2.5RR**: 21832.54 ✅
- **TP 3RR**: 21799.96 ✅
- **TP 3.5RR**: 21767.38 ✅
- **TP 4RR**: 21734.81 ✅
- **TP 4.5RR**: 21702.23 ✅
- **TP 5RR**: 21669.66 ✅
- **PnL**: 325.75 points (5.0R)
- **MFE**: 336.35 points
- **MAE**: 22.17 points

### Trade #114 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 02:00:00
- **FVG 5m**: 22039.49 - 22049.54
- **Entrée**: 21962.68 @ 2025-01-27 02:01:00
- **Stop Loss**: 22060.56
- **Risk**: 97.88 points
- **TP 1RR**: 21864.79 ✅
- **TP 1.5RR**: 21815.85 ✅
- **TP 2RR**: 21766.91 ✅
- **TP 2.5RR**: 21717.97 ✅
- **TP 3RR**: 21669.03 ✅
- **TP 3.5RR**: 21620.09 ✅
- **TP 4RR**: 21571.14 ✅
- **TP 4.5RR**: 21522.20 ✅
- **TP 5RR**: 21473.26 ✅
- **PnL**: 489.42 points (5.0R)
- **MFE**: 493.83 points
- **MAE**: 9.79 points

### Trade #115 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 05:00:00
- **FVG 5m**: 21566.27 - 21592.56
- **Entrée**: 21608.54 @ 2025-01-27 05:07:00
- **Stop Loss**: 21555.49
- **Risk**: 53.05 points
- **TP 1RR**: 21661.59 ❌
- **TP 1.5RR**: 21688.12 ❌
- **TP 2RR**: 21714.65 ❌
- **TP 2.5RR**: 21741.17 ❌
- **TP 3RR**: 21767.70 ❌
- **TP 3.5RR**: 21794.23 ❌
- **TP 4RR**: 21820.75 ❌
- **TP 4.5RR**: 21847.28 ❌
- **TP 5RR**: 21873.81 ❌
- **PnL**: -53.05 points (-1.0R)
- **MFE**: 52.58 points
- **MAE**: 79.13 points

### Trade #116 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 09:45:00
- **FVG 5m**: 21979.17 - 22011.13
- **Entrée**: 21978.92 @ 2025-01-27 09:57:00
- **Stop Loss**: 22022.14
- **Risk**: 43.22 points
- **TP 1RR**: 21935.69 ✅
- **TP 1.5RR**: 21914.08 ✅
- **TP 2RR**: 21892.47 ✅
- **TP 2.5RR**: 21870.86 ✅
- **TP 3RR**: 21849.25 ✅
- **TP 3.5RR**: 21827.63 ✅
- **TP 4RR**: 21806.02 ✅
- **TP 4.5RR**: 21784.41 ✅
- **TP 5RR**: 21762.80 ✅
- **PnL**: 216.12 points (5.0R)
- **MFE**: 224.24 points
- **MAE**: 14.18 points

### Trade #117 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 09:45:00
- **FVG 5m**: 21979.17 - 22011.13
- **Entrée**: 21978.92 @ 2025-01-27 09:57:00
- **Stop Loss**: 22022.14
- **Risk**: 43.22 points
- **TP 1RR**: 21935.69 ✅
- **TP 1.5RR**: 21914.08 ✅
- **TP 2RR**: 21892.47 ✅
- **TP 2.5RR**: 21870.86 ✅
- **TP 3RR**: 21849.25 ✅
- **TP 3.5RR**: 21827.63 ✅
- **TP 4RR**: 21806.02 ✅
- **TP 4.5RR**: 21784.41 ✅
- **TP 5RR**: 21762.80 ✅
- **PnL**: 216.12 points (5.0R)
- **MFE**: 224.24 points
- **MAE**: 14.18 points

### Trade #118 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 14:00:00
- **FVG 5m**: 21782.00 - 21819.37
- **Entrée**: 21828.14 @ 2025-01-27 14:08:00
- **Stop Loss**: 21771.11
- **Risk**: 57.03 points
- **TP 1RR**: 21885.16 ✅
- **TP 1.5RR**: 21913.68 ✅
- **TP 2RR**: 21942.19 ✅
- **TP 2.5RR**: 21970.70 ✅
- **TP 3RR**: 21999.22 ✅
- **TP 3.5RR**: 22027.73 ✅
- **TP 4RR**: 22056.24 ✅
- **TP 4.5RR**: 22084.76 ✅
- **TP 5RR**: 22113.27 ✅
- **PnL**: 285.13 points (5.0R)
- **MFE**: 294.86 points
- **MAE**: 26.03 points

### Trade #119 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 19:45:00
- **FVG 5m**: 21955.46 - 21966.29
- **Entrée**: 21950.82 @ 2025-01-27 19:47:00
- **Stop Loss**: 21977.27
- **Risk**: 26.45 points
- **TP 1RR**: 21924.37 ✅
- **TP 1.5RR**: 21911.15 ✅
- **TP 2RR**: 21897.93 ✅
- **TP 2.5RR**: 21884.70 ✅
- **TP 3RR**: 21871.48 ❌
- **TP 3.5RR**: 21858.26 ❌
- **TP 4RR**: 21845.03 ❌
- **TP 4.5RR**: 21831.81 ❌
- **TP 5RR**: 21818.58 ❌
- **PnL**: -26.45 points (-1.0R)
- **MFE**: 74.75 points
- **MAE**: 29.38 points

### Trade #120 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 02:00:00
- **FVG 5m**: 21963.45 - 21970.93
- **Entrée**: 21962.94 @ 2025-01-28 02:12:00
- **Stop Loss**: 21981.91
- **Risk**: 18.98 points
- **TP 1RR**: 21943.96 ❌
- **TP 1.5RR**: 21934.47 ❌
- **TP 2RR**: 21924.99 ❌
- **TP 2.5RR**: 21915.50 ❌
- **TP 3RR**: 21906.01 ❌
- **TP 3.5RR**: 21896.52 ❌
- **TP 4RR**: 21887.03 ❌
- **TP 4.5RR**: 21877.55 ❌
- **TP 5RR**: 21868.06 ❌
- **PnL**: -18.98 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 20.88 points

### Trade #121 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 02:00:00
- **FVG 5m**: 21963.45 - 21970.93
- **Entrée**: 21962.94 @ 2025-01-28 02:12:00
- **Stop Loss**: 21981.91
- **Risk**: 18.98 points
- **TP 1RR**: 21943.96 ❌
- **TP 1.5RR**: 21934.47 ❌
- **TP 2RR**: 21924.99 ❌
- **TP 2.5RR**: 21915.50 ❌
- **TP 3RR**: 21906.01 ❌
- **TP 3.5RR**: 21896.52 ❌
- **TP 4RR**: 21887.03 ❌
- **TP 4.5RR**: 21877.55 ❌
- **TP 5RR**: 21868.06 ❌
- **PnL**: -18.98 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 20.88 points

### Trade #122 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 02:00:00
- **FVG 5m**: 21963.45 - 21970.93
- **Entrée**: 21962.94 @ 2025-01-28 02:12:00
- **Stop Loss**: 21981.91
- **Risk**: 18.98 points
- **TP 1RR**: 21943.96 ❌
- **TP 1.5RR**: 21934.47 ❌
- **TP 2RR**: 21924.99 ❌
- **TP 2.5RR**: 21915.50 ❌
- **TP 3RR**: 21906.01 ❌
- **TP 3.5RR**: 21896.52 ❌
- **TP 4RR**: 21887.03 ❌
- **TP 4.5RR**: 21877.55 ❌
- **TP 5RR**: 21868.06 ❌
- **PnL**: -18.98 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 20.88 points

### Trade #123 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 05:30:00
- **FVG 5m**: 22059.59 - 22063.97
- **Entrée**: 22026.86 @ 2025-01-28 05:31:00
- **Stop Loss**: 22075.00
- **Risk**: 48.15 points
- **TP 1RR**: 21978.71 ✅
- **TP 1.5RR**: 21954.64 ✅
- **TP 2RR**: 21930.56 ✅
- **TP 2.5RR**: 21906.49 ✅
- **TP 3RR**: 21882.42 ✅
- **TP 3.5RR**: 21858.34 ✅
- **TP 4RR**: 21834.27 ✅
- **TP 4.5RR**: 21810.20 ❌
- **TP 5RR**: 21786.12 ❌
- **PnL**: -48.15 points (-1.0R)
- **MFE**: 212.12 points
- **MAE**: 73.20 points

### Trade #124 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 08:45:00
- **FVG 5m**: 21889.22 - 21898.76
- **Entrée**: 21909.84 @ 2025-01-28 08:52:00
- **Stop Loss**: 21878.28
- **Risk**: 31.56 points
- **TP 1RR**: 21941.41 ✅
- **TP 1.5RR**: 21957.19 ✅
- **TP 2RR**: 21972.97 ✅
- **TP 2.5RR**: 21988.75 ✅
- **TP 3RR**: 22004.53 ✅
- **TP 3.5RR**: 22020.31 ✅
- **TP 4RR**: 22036.10 ✅
- **TP 4.5RR**: 22051.88 ✅
- **TP 5RR**: 22067.66 ✅
- **PnL**: 157.82 points (5.0R)
- **MFE**: 159.80 points
- **MAE**: 20.10 points

### Trade #125 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 08:45:00
- **FVG 5m**: 21889.22 - 21898.76
- **Entrée**: 21909.84 @ 2025-01-28 08:52:00
- **Stop Loss**: 21878.28
- **Risk**: 31.56 points
- **TP 1RR**: 21941.41 ✅
- **TP 1.5RR**: 21957.19 ✅
- **TP 2RR**: 21972.97 ✅
- **TP 2.5RR**: 21988.75 ✅
- **TP 3RR**: 22004.53 ✅
- **TP 3.5RR**: 22020.31 ✅
- **TP 4RR**: 22036.10 ✅
- **TP 4.5RR**: 22051.88 ✅
- **TP 5RR**: 22067.66 ✅
- **PnL**: 157.82 points (5.0R)
- **MFE**: 159.80 points
- **MAE**: 20.10 points

### Trade #126 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 08:45:00
- **FVG 5m**: 21889.22 - 21898.76
- **Entrée**: 21909.84 @ 2025-01-28 08:52:00
- **Stop Loss**: 21878.28
- **Risk**: 31.56 points
- **TP 1RR**: 21941.41 ✅
- **TP 1.5RR**: 21957.19 ✅
- **TP 2RR**: 21972.97 ✅
- **TP 2.5RR**: 21988.75 ✅
- **TP 3RR**: 22004.53 ✅
- **TP 3.5RR**: 22020.31 ✅
- **TP 4RR**: 22036.10 ✅
- **TP 4.5RR**: 22051.88 ✅
- **TP 5RR**: 22067.66 ✅
- **PnL**: 157.82 points (5.0R)
- **MFE**: 159.80 points
- **MAE**: 20.10 points

### Trade #127 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 11:00:00
- **FVG 5m**: 22089.23 - 22100.05
- **Entrée**: 22158.05 @ 2025-01-28 11:01:00
- **Stop Loss**: 22078.18
- **Risk**: 79.86 points
- **TP 1RR**: 22237.91 ✅
- **TP 1.5RR**: 22277.84 ✅
- **TP 2RR**: 22317.77 ✅
- **TP 2.5RR**: 22357.70 ✅
- **TP 3RR**: 22397.63 ❌
- **TP 3.5RR**: 22437.56 ❌
- **TP 4RR**: 22477.49 ❌
- **TP 4.5RR**: 22517.42 ❌
- **TP 5RR**: 22557.35 ❌
- **PnL**: -79.86 points (-1.0R)
- **MFE**: 210.83 points
- **MAE**: 88.41 points

### Trade #128 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 07:00:00
- **FVG 5m**: 22343.10 - 22348.26
- **Entrée**: 22316.82 @ 2025-01-29 07:01:00
- **Stop Loss**: 22359.43
- **Risk**: 42.62 points
- **TP 1RR**: 22274.20 ✅
- **TP 1.5RR**: 22252.89 ✅
- **TP 2RR**: 22231.58 ✅
- **TP 2.5RR**: 22210.27 ✅
- **TP 3RR**: 22188.96 ✅
- **TP 3.5RR**: 22167.65 ✅
- **TP 4RR**: 22146.34 ✅
- **TP 4.5RR**: 22125.03 ✅
- **TP 5RR**: 22103.72 ✅
- **PnL**: 213.09 points (5.0R)
- **MFE**: 228.10 points
- **MAE**: 0.00 points

### Trade #129 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 07:00:00
- **FVG 5m**: 22343.10 - 22348.26
- **Entrée**: 22316.82 @ 2025-01-29 07:01:00
- **Stop Loss**: 22359.43
- **Risk**: 42.62 points
- **TP 1RR**: 22274.20 ✅
- **TP 1.5RR**: 22252.89 ✅
- **TP 2RR**: 22231.58 ✅
- **TP 2.5RR**: 22210.27 ✅
- **TP 3RR**: 22188.96 ✅
- **TP 3.5RR**: 22167.65 ✅
- **TP 4RR**: 22146.34 ✅
- **TP 4.5RR**: 22125.03 ✅
- **TP 5RR**: 22103.72 ✅
- **PnL**: 213.09 points (5.0R)
- **MFE**: 228.10 points
- **MAE**: 0.00 points

### Trade #130 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 07:30:00
- **FVG 5m**: 22343.10 - 22348.26
- **Entrée**: 22249.80 @ 2025-01-29 07:31:00
- **Stop Loss**: 22359.43
- **Risk**: 109.63 points
- **TP 1RR**: 22140.17 ✅
- **TP 1.5RR**: 22085.36 ✅
- **TP 2RR**: 22030.54 ✅
- **TP 2.5RR**: 21975.72 ❌
- **TP 3RR**: 21920.91 ❌
- **TP 3.5RR**: 21866.09 ❌
- **TP 4RR**: 21811.28 ❌
- **TP 4.5RR**: 21756.46 ❌
- **TP 5RR**: 21701.65 ❌
- **PnL**: -109.63 points (-1.0R)
- **MFE**: 221.14 points
- **MAE**: 111.86 points

### Trade #131 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 09:30:00
- **FVG 5m**: 22254.44 - 22269.13
- **Entrée**: 22169.39 @ 2025-01-29 09:31:00
- **Stop Loss**: 22280.27
- **Risk**: 110.88 points
- **TP 1RR**: 22058.51 ✅
- **TP 1.5RR**: 22003.07 ❌
- **TP 2RR**: 21947.63 ❌
- **TP 2.5RR**: 21892.19 ❌
- **TP 3RR**: 21836.75 ❌
- **TP 3.5RR**: 21781.30 ❌
- **TP 4RR**: 21725.86 ❌
- **TP 4.5RR**: 21670.42 ❌
- **TP 5RR**: 21614.98 ❌
- **PnL**: -110.88 points (-1.0R)
- **MFE**: 140.73 points
- **MAE**: 116.50 points

### Trade #132 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 13:45:00
- **FVG 5m**: 22142.07 - 22145.16
- **Entrée**: 22135.11 @ 2025-01-29 14:17:00
- **Stop Loss**: 22156.23
- **Risk**: 21.12 points
- **TP 1RR**: 22113.98 ❌
- **TP 1.5RR**: 22103.42 ❌
- **TP 2RR**: 22092.86 ❌
- **TP 2.5RR**: 22082.30 ❌
- **TP 3RR**: 22071.73 ❌
- **TP 3.5RR**: 22061.17 ❌
- **TP 4RR**: 22050.61 ❌
- **TP 4.5RR**: 22040.05 ❌
- **TP 5RR**: 22029.48 ❌
- **PnL**: -21.12 points (-1.0R)
- **MFE**: 7.73 points
- **MAE**: 34.02 points

### Trade #133 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-29 14:15:00
- **FVG 5m**: 22136.65 - 22143.10
- **Entrée**: 22156.50 @ 2025-01-29 14:16:00
- **Stop Loss**: 22125.59
- **Risk**: 30.91 points
- **TP 1RR**: 22187.41 ✅
- **TP 1.5RR**: 22202.87 ✅
- **TP 2RR**: 22218.33 ✅
- **TP 2.5RR**: 22233.79 ✅
- **TP 3RR**: 22249.24 ✅
- **TP 3.5RR**: 22264.70 ✅
- **TP 4RR**: 22280.16 ❌
- **TP 4.5RR**: 22295.61 ❌
- **TP 5RR**: 22311.07 ❌
- **PnL**: -30.91 points (-1.0R)
- **MFE**: 113.15 points
- **MAE**: 42.01 points

### Trade #134 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 02:15:00
- **FVG 5m**: 22341.56 - 22345.94
- **Entrée**: 22339.50 @ 2025-01-30 03:05:00
- **Stop Loss**: 22357.11
- **Risk**: 17.62 points
- **TP 1RR**: 22321.88 ✅
- **TP 1.5RR**: 22313.07 ✅
- **TP 2RR**: 22304.26 ✅
- **TP 2.5RR**: 22295.46 ✅
- **TP 3RR**: 22286.65 ✅
- **TP 3.5RR**: 22277.84 ✅
- **TP 4RR**: 22269.03 ✅
- **TP 4.5RR**: 22260.22 ✅
- **TP 5RR**: 22251.41 ✅
- **PnL**: 88.08 points (5.0R)
- **MFE**: 97.17 points
- **MAE**: 15.98 points

### Trade #135 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 02:45:00
- **FVG 5m**: 22299.55 - 22308.83
- **Entrée**: 22362.95 @ 2025-01-30 02:46:00
- **Stop Loss**: 22288.40
- **Risk**: 74.55 points
- **TP 1RR**: 22437.51 ❌
- **TP 1.5RR**: 22474.78 ❌
- **TP 2RR**: 22512.06 ❌
- **TP 2.5RR**: 22549.34 ❌
- **TP 3RR**: 22586.61 ❌
- **TP 3.5RR**: 22623.89 ❌
- **TP 4RR**: 22661.17 ❌
- **TP 4.5RR**: 22698.44 ❌
- **TP 5RR**: 22735.72 ❌
- **PnL**: -74.55 points (-1.0R)
- **MFE**: 12.63 points
- **MAE**: 80.93 points

### Trade #136 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22358.05 - 22368.11
- **Entrée**: 22355.99 @ 2025-01-30 03:01:00
- **Stop Loss**: 22379.29
- **Risk**: 23.30 points
- **TP 1RR**: 22332.69 ✅
- **TP 1.5RR**: 22321.05 ✅
- **TP 2RR**: 22309.40 ✅
- **TP 2.5RR**: 22297.75 ✅
- **TP 3RR**: 22286.10 ✅
- **TP 3.5RR**: 22274.45 ✅
- **TP 4RR**: 22262.80 ✅
- **TP 4.5RR**: 22251.15 ✅
- **TP 5RR**: 22239.50 ❌
- **PnL**: -23.30 points (-1.0R)
- **MFE**: 113.66 points
- **MAE**: 32.73 points

### Trade #137 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22358.05 - 22368.11
- **Entrée**: 22355.99 @ 2025-01-30 03:01:00
- **Stop Loss**: 22379.29
- **Risk**: 23.30 points
- **TP 1RR**: 22332.69 ✅
- **TP 1.5RR**: 22321.05 ✅
- **TP 2RR**: 22309.40 ✅
- **TP 2.5RR**: 22297.75 ✅
- **TP 3RR**: 22286.10 ✅
- **TP 3.5RR**: 22274.45 ✅
- **TP 4RR**: 22262.80 ✅
- **TP 4.5RR**: 22251.15 ✅
- **TP 5RR**: 22239.50 ❌
- **PnL**: -23.30 points (-1.0R)
- **MFE**: 113.66 points
- **MAE**: 32.73 points

### Trade #138 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22358.05 - 22368.11
- **Entrée**: 22355.99 @ 2025-01-30 03:01:00
- **Stop Loss**: 22379.29
- **Risk**: 23.30 points
- **TP 1RR**: 22332.69 ✅
- **TP 1.5RR**: 22321.05 ✅
- **TP 2RR**: 22309.40 ✅
- **TP 2.5RR**: 22297.75 ✅
- **TP 3RR**: 22286.10 ✅
- **TP 3.5RR**: 22274.45 ✅
- **TP 4RR**: 22262.80 ✅
- **TP 4.5RR**: 22251.15 ✅
- **TP 5RR**: 22239.50 ❌
- **PnL**: -23.30 points (-1.0R)
- **MFE**: 113.66 points
- **MAE**: 32.73 points

### Trade #139 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22358.05 - 22368.11
- **Entrée**: 22355.99 @ 2025-01-30 03:01:00
- **Stop Loss**: 22379.29
- **Risk**: 23.30 points
- **TP 1RR**: 22332.69 ✅
- **TP 1.5RR**: 22321.05 ✅
- **TP 2RR**: 22309.40 ✅
- **TP 2.5RR**: 22297.75 ✅
- **TP 3RR**: 22286.10 ✅
- **TP 3.5RR**: 22274.45 ✅
- **TP 4RR**: 22262.80 ✅
- **TP 4.5RR**: 22251.15 ✅
- **TP 5RR**: 22239.50 ❌
- **PnL**: -23.30 points (-1.0R)
- **MFE**: 113.66 points
- **MAE**: 32.73 points

### Trade #140 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 04:15:00
- **FVG 5m**: 22311.66 - 22314.75
- **Entrée**: 22318.10 @ 2025-01-30 05:11:00
- **Stop Loss**: 22300.50
- **Risk**: 17.60 points
- **TP 1RR**: 22335.70 ✅
- **TP 1.5RR**: 22344.50 ❌
- **TP 2RR**: 22353.30 ❌
- **TP 2.5RR**: 22362.10 ❌
- **TP 3RR**: 22370.90 ❌
- **TP 3.5RR**: 22379.70 ❌
- **TP 4RR**: 22388.50 ❌
- **TP 4.5RR**: 22397.30 ❌
- **TP 5RR**: 22406.10 ❌
- **PnL**: -17.60 points (-1.0R)
- **MFE**: 23.71 points
- **MAE**: 31.44 points

### Trade #141 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 06:30:00
- **FVG 5m**: 22259.34 - 22283.05
- **Entrée**: 22285.63 @ 2025-01-30 06:37:00
- **Stop Loss**: 22248.21
- **Risk**: 37.42 points
- **TP 1RR**: 22323.05 ✅
- **TP 1.5RR**: 22341.76 ✅
- **TP 2RR**: 22360.47 ✅
- **TP 2.5RR**: 22379.18 ✅
- **TP 3RR**: 22397.89 ✅
- **TP 3.5RR**: 22416.60 ✅
- **TP 4RR**: 22435.31 ❌
- **TP 4.5RR**: 22454.02 ❌
- **TP 5RR**: 22472.72 ❌
- **PnL**: -37.42 points (-1.0R)
- **MFE**: 136.60 points
- **MAE**: 44.59 points

### Trade #142 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 06:45:00
- **FVG 5m**: 22259.34 - 22283.05
- **Entrée**: 22293.10 @ 2025-01-30 06:46:00
- **Stop Loss**: 22248.21
- **Risk**: 44.89 points
- **TP 1RR**: 22338.00 ✅
- **TP 1.5RR**: 22360.44 ✅
- **TP 2RR**: 22382.89 ✅
- **TP 2.5RR**: 22405.34 ✅
- **TP 3RR**: 22427.78 ❌
- **TP 3.5RR**: 22450.23 ❌
- **TP 4RR**: 22472.68 ❌
- **TP 4.5RR**: 22495.13 ❌
- **TP 5RR**: 22517.57 ❌
- **PnL**: -44.89 points (-1.0R)
- **MFE**: 129.13 points
- **MAE**: 52.06 points

### Trade #143 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 08:45:00
- **FVG 5m**: 22302.64 - 22312.95
- **Entrée**: 22267.59 @ 2025-01-30 09:02:00
- **Stop Loss**: 22324.11
- **Risk**: 56.52 points
- **TP 1RR**: 22211.07 ✅
- **TP 1.5RR**: 22182.81 ✅
- **TP 2RR**: 22154.55 ✅
- **TP 2.5RR**: 22126.29 ✅
- **TP 3RR**: 22098.03 ✅
- **TP 3.5RR**: 22069.77 ❌
- **TP 4RR**: 22041.51 ❌
- **TP 4.5RR**: 22013.25 ❌
- **TP 5RR**: 21984.99 ❌
- **PnL**: -56.52 points (-1.0R)
- **MFE**: 184.80 points
- **MAE**: 62.37 points

### Trade #144 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 09:00:00
- **FVG 5m**: 22331.76 - 22355.48
- **Entrée**: 22318.10 @ 2025-01-30 09:01:00
- **Stop Loss**: 22366.65
- **Risk**: 48.55 points
- **TP 1RR**: 22269.55 ✅
- **TP 1.5RR**: 22245.28 ✅
- **TP 2RR**: 22221.00 ✅
- **TP 2.5RR**: 22196.73 ✅
- **TP 3RR**: 22172.45 ✅
- **TP 3.5RR**: 22148.18 ✅
- **TP 4RR**: 22123.90 ✅
- **TP 4.5RR**: 22099.63 ✅
- **TP 5RR**: 22075.35 ❌
- **PnL**: -48.55 points (-1.0R)
- **MFE**: 235.32 points
- **MAE**: 53.87 points

### Trade #145 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 10:45:00
- **FVG 5m**: 22153.66 - 22171.45
- **Entrée**: 22227.89 @ 2025-01-30 10:46:00
- **Stop Loss**: 22142.59
- **Risk**: 85.31 points
- **TP 1RR**: 22313.20 ✅
- **TP 1.5RR**: 22355.85 ✅
- **TP 2RR**: 22398.51 ✅
- **TP 2.5RR**: 22441.16 ✅
- **TP 3RR**: 22483.81 ✅
- **TP 3.5RR**: 22526.47 ✅
- **TP 4RR**: 22569.12 ✅
- **TP 4.5RR**: 22611.77 ✅
- **TP 5RR**: 22654.43 ❌
- **PnL**: -85.31 points (-1.0R)
- **MFE**: 418.31 points
- **MAE**: 636.36 points

### Trade #146 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 14:30:00
- **FVG 5m**: 22316.30 - 22326.09
- **Entrée**: 22303.41 @ 2025-01-30 14:37:00
- **Stop Loss**: 22337.26
- **Risk**: 33.84 points
- **TP 1RR**: 22269.57 ✅
- **TP 1.5RR**: 22252.65 ✅
- **TP 2RR**: 22235.72 ✅
- **TP 2.5RR**: 22218.80 ✅
- **TP 3RR**: 22201.88 ✅
- **TP 3.5RR**: 22184.96 ❌
- **TP 4RR**: 22168.04 ❌
- **TP 4.5RR**: 22151.11 ❌
- **TP 5RR**: 22134.19 ❌
- **PnL**: -33.84 points (-1.0R)
- **MFE**: 113.66 points
- **MAE**: 37.63 points

### Trade #147 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 14:30:00
- **FVG 5m**: 22316.30 - 22326.09
- **Entrée**: 22303.41 @ 2025-01-30 14:37:00
- **Stop Loss**: 22337.26
- **Risk**: 33.84 points
- **TP 1RR**: 22269.57 ✅
- **TP 1.5RR**: 22252.65 ✅
- **TP 2RR**: 22235.72 ✅
- **TP 2.5RR**: 22218.80 ✅
- **TP 3RR**: 22201.88 ✅
- **TP 3.5RR**: 22184.96 ❌
- **TP 4RR**: 22168.04 ❌
- **TP 4.5RR**: 22151.11 ❌
- **TP 5RR**: 22134.19 ❌
- **PnL**: -33.84 points (-1.0R)
- **MFE**: 113.66 points
- **MAE**: 37.63 points

### Trade #148 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 02:00:00
- **FVG 5m**: 22455.22 - 22465.02
- **Entrée**: 22454.19 @ 2025-01-31 02:01:00
- **Stop Loss**: 22476.25
- **Risk**: 22.06 points
- **TP 1RR**: 22432.13 ✅
- **TP 1.5RR**: 22421.10 ✅
- **TP 2RR**: 22410.08 ❌
- **TP 2.5RR**: 22399.05 ❌
- **TP 3RR**: 22388.02 ❌
- **TP 3.5RR**: 22376.99 ❌
- **TP 4RR**: 22365.96 ❌
- **TP 4.5RR**: 22354.93 ❌
- **TP 5RR**: 22343.90 ❌
- **PnL**: -22.06 points (-1.0R)
- **MFE**: 38.15 points
- **MAE**: 26.29 points

### Trade #149 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 07:30:00
- **FVG 5m**: 22459.60 - 22465.27
- **Entrée**: 22472.75 @ 2025-01-31 07:48:00
- **Stop Loss**: 22448.37
- **Risk**: 24.37 points
- **TP 1RR**: 22497.12 ❌
- **TP 1.5RR**: 22509.31 ❌
- **TP 2RR**: 22521.50 ❌
- **TP 2.5RR**: 22533.69 ❌
- **TP 3RR**: 22545.87 ❌
- **TP 3.5RR**: 22558.06 ❌
- **TP 4RR**: 22570.25 ❌
- **TP 4.5RR**: 22582.43 ❌
- **TP 5RR**: 22594.62 ❌
- **PnL**: -24.37 points (-1.0R)
- **MFE**: 11.34 points
- **MAE**: 26.29 points

### Trade #150 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 08:45:00
- **FVG 5m**: 22450.07 - 22458.32
- **Entrée**: 22492.59 @ 2025-01-31 08:46:00
- **Stop Loss**: 22438.84
- **Risk**: 53.75 points
- **TP 1RR**: 22546.35 ✅
- **TP 1.5RR**: 22573.22 ✅
- **TP 2RR**: 22600.10 ✅
- **TP 2.5RR**: 22626.98 ✅
- **TP 3RR**: 22653.85 ❌
- **TP 3.5RR**: 22680.73 ❌
- **TP 4RR**: 22707.60 ❌
- **TP 4.5RR**: 22734.48 ❌
- **TP 5RR**: 22761.36 ❌
- **PnL**: -53.75 points (-1.0R)
- **MFE**: 153.61 points
- **MAE**: 75.52 points

### Trade #151 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 08:45:00
- **FVG 5m**: 22450.07 - 22458.32
- **Entrée**: 22492.59 @ 2025-01-31 08:46:00
- **Stop Loss**: 22438.84
- **Risk**: 53.75 points
- **TP 1RR**: 22546.35 ✅
- **TP 1.5RR**: 22573.22 ✅
- **TP 2RR**: 22600.10 ✅
- **TP 2.5RR**: 22626.98 ✅
- **TP 3RR**: 22653.85 ❌
- **TP 3.5RR**: 22680.73 ❌
- **TP 4RR**: 22707.60 ❌
- **TP 4.5RR**: 22734.48 ❌
- **TP 5RR**: 22761.36 ❌
- **PnL**: -53.75 points (-1.0R)
- **MFE**: 153.61 points
- **MAE**: 75.52 points

### Trade #152 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 12:30:00
- **FVG 5m**: 22591.83 - 22597.24
- **Entrée**: 22488.99 @ 2025-01-31 12:31:00
- **Stop Loss**: 22608.54
- **Risk**: 119.55 points
- **TP 1RR**: 22369.44 ✅
- **TP 1.5RR**: 22309.66 ✅
- **TP 2RR**: 22249.89 ✅
- **TP 2.5RR**: 22190.11 ✅
- **TP 3RR**: 22130.34 ✅
- **TP 3.5RR**: 22070.56 ✅
- **TP 4RR**: 22010.79 ✅
- **TP 4.5RR**: 21951.01 ✅
- **TP 5RR**: 21891.24 ✅
- **PnL**: 597.75 points (5.0R)
- **MFE**: 897.46 points
- **MAE**: 14.18 points

### Trade #153 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 12:30:00
- **FVG 5m**: 22591.83 - 22597.24
- **Entrée**: 22488.99 @ 2025-01-31 12:31:00
- **Stop Loss**: 22608.54
- **Risk**: 119.55 points
- **TP 1RR**: 22369.44 ✅
- **TP 1.5RR**: 22309.66 ✅
- **TP 2RR**: 22249.89 ✅
- **TP 2.5RR**: 22190.11 ✅
- **TP 3RR**: 22130.34 ✅
- **TP 3.5RR**: 22070.56 ✅
- **TP 4RR**: 22010.79 ✅
- **TP 4.5RR**: 21951.01 ✅
- **TP 5RR**: 21891.24 ✅
- **PnL**: 597.75 points (5.0R)
- **MFE**: 897.46 points
- **MAE**: 14.18 points

### Trade #154 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 13:00:00
- **FVG 5m**: 22591.83 - 22597.24
- **Entrée**: 22444.91 @ 2025-01-31 13:01:00
- **Stop Loss**: 22608.54
- **Risk**: 163.62 points
- **TP 1RR**: 22281.29 ✅
- **TP 1.5RR**: 22199.48 ✅
- **TP 2RR**: 22117.66 ✅
- **TP 2.5RR**: 22035.85 ✅
- **TP 3RR**: 21954.04 ✅
- **TP 3.5RR**: 21872.23 ✅
- **TP 4RR**: 21790.42 ✅
- **TP 4.5RR**: 21708.61 ✅
- **TP 5RR**: 21626.79 ✅
- **PnL**: 818.12 points (5.0R)
- **MFE**: 853.38 points
- **MAE**: 11.34 points

### Trade #155 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 13:15:00
- **FVG 5m**: 22591.83 - 22597.24
- **Entrée**: 22407.28 @ 2025-01-31 13:16:00
- **Stop Loss**: 22608.54
- **Risk**: 201.25 points
- **TP 1RR**: 22206.03 ✅
- **TP 1.5RR**: 22105.40 ✅
- **TP 2RR**: 22004.77 ✅
- **TP 2.5RR**: 21904.15 ✅
- **TP 3RR**: 21803.52 ✅
- **TP 3.5RR**: 21702.89 ✅
- **TP 4RR**: 21602.27 ✅
- **TP 4.5RR**: 21501.64 ❌
- **TP 5RR**: 21401.01 ❌
- **PnL**: -201.25 points (-1.0R)
- **MFE**: 815.75 points
- **MAE**: 201.81 points

### Trade #156 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 05:15:00
- **FVG 5m**: 21890.51 - 21909.33
- **Entrée**: 21888.71 @ 2025-02-03 05:28:00
- **Stop Loss**: 21920.28
- **Risk**: 31.57 points
- **TP 1RR**: 21857.13 ✅
- **TP 1.5RR**: 21841.35 ✅
- **TP 2RR**: 21825.56 ✅
- **TP 2.5RR**: 21809.77 ❌
- **TP 3RR**: 21793.98 ❌
- **TP 3.5RR**: 21778.20 ❌
- **TP 4RR**: 21762.41 ❌
- **TP 4.5RR**: 21746.62 ❌
- **TP 5RR**: 21730.84 ❌
- **PnL**: -31.57 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 58.51 points

### Trade #157 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 08:30:00
- **FVG 5m**: 21838.45 - 21856.23
- **Entrée**: 21835.35 @ 2025-02-03 08:53:00
- **Stop Loss**: 21867.16
- **Risk**: 31.81 points
- **TP 1RR**: 21803.55 ❌
- **TP 1.5RR**: 21787.65 ❌
- **TP 2RR**: 21771.74 ❌
- **TP 2.5RR**: 21755.84 ❌
- **TP 3RR**: 21739.94 ❌
- **TP 3.5RR**: 21724.04 ❌
- **TP 4RR**: 21708.13 ❌
- **TP 4.5RR**: 21692.23 ❌
- **TP 5RR**: 21676.33 ❌
- **PnL**: -31.81 points (-1.0R)
- **MFE**: 6.70 points
- **MAE**: 52.06 points

### Trade #158 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 08:45:00
- **FVG 5m**: 21838.45 - 21856.23
- **Entrée**: 21835.35 @ 2025-02-03 08:53:00
- **Stop Loss**: 21867.16
- **Risk**: 31.81 points
- **TP 1RR**: 21803.55 ❌
- **TP 1.5RR**: 21787.65 ❌
- **TP 2RR**: 21771.74 ❌
- **TP 2.5RR**: 21755.84 ❌
- **TP 3RR**: 21739.94 ❌
- **TP 3.5RR**: 21724.04 ❌
- **TP 4RR**: 21708.13 ❌
- **TP 4.5RR**: 21692.23 ❌
- **TP 5RR**: 21676.33 ❌
- **PnL**: -31.81 points (-1.0R)
- **MFE**: 6.70 points
- **MAE**: 52.06 points

### Trade #159 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:15:00
- **FVG 5m**: 21896.70 - 21910.10
- **Entrée**: 21973.25 @ 2025-02-03 09:24:00
- **Stop Loss**: 21885.75
- **Risk**: 87.50 points
- **TP 1RR**: 22060.74 ✅
- **TP 1.5RR**: 22104.49 ✅
- **TP 2RR**: 22148.24 ✅
- **TP 2.5RR**: 22191.99 ✅
- **TP 3RR**: 22235.74 ✅
- **TP 3.5RR**: 22279.49 ✅
- **TP 4RR**: 22323.24 ✅
- **TP 4.5RR**: 22366.98 ✅
- **TP 5RR**: 22410.73 ✅
- **PnL**: 437.49 points (5.0R)
- **MFE**: 442.54 points
- **MAE**: 72.94 points

### Trade #160 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:15:00
- **FVG 5m**: 21896.70 - 21910.10
- **Entrée**: 21973.25 @ 2025-02-03 09:24:00
- **Stop Loss**: 21885.75
- **Risk**: 87.50 points
- **TP 1RR**: 22060.74 ✅
- **TP 1.5RR**: 22104.49 ✅
- **TP 2RR**: 22148.24 ✅
- **TP 2.5RR**: 22191.99 ✅
- **TP 3RR**: 22235.74 ✅
- **TP 3.5RR**: 22279.49 ✅
- **TP 4RR**: 22323.24 ✅
- **TP 4.5RR**: 22366.98 ✅
- **TP 5RR**: 22410.73 ✅
- **PnL**: 437.49 points (5.0R)
- **MFE**: 442.54 points
- **MAE**: 72.94 points

### Trade #161 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:30:00
- **FVG 5m**: 21797.72 - 21811.64
- **Entrée**: 22007.53 @ 2025-02-03 09:31:00
- **Stop Loss**: 21786.82
- **Risk**: 220.70 points
- **TP 1RR**: 22228.23 ✅
- **TP 1.5RR**: 22338.58 ✅
- **TP 2RR**: 22448.93 ✅
- **TP 2.5RR**: 22559.28 ✅
- **TP 3RR**: 22669.63 ✅
- **TP 3.5RR**: 22779.98 ✅
- **TP 4RR**: 22890.33 ✅
- **TP 4.5RR**: 23000.68 ✅
- **TP 5RR**: 23111.03 ❌
- **PnL**: -220.70 points (-1.0R)
- **MFE**: 1003.39 points
- **MAE**: 240.99 points

### Trade #162 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:30:00
- **FVG 5m**: 21797.72 - 21811.64
- **Entrée**: 22007.53 @ 2025-02-03 09:31:00
- **Stop Loss**: 21786.82
- **Risk**: 220.70 points
- **TP 1RR**: 22228.23 ✅
- **TP 1.5RR**: 22338.58 ✅
- **TP 2RR**: 22448.93 ✅
- **TP 2.5RR**: 22559.28 ✅
- **TP 3RR**: 22669.63 ✅
- **TP 3.5RR**: 22779.98 ✅
- **TP 4RR**: 22890.33 ✅
- **TP 4.5RR**: 23000.68 ✅
- **TP 5RR**: 23111.03 ❌
- **PnL**: -220.70 points (-1.0R)
- **MFE**: 1003.39 points
- **MAE**: 240.99 points

### Trade #163 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:30:00
- **FVG 5m**: 21797.72 - 21811.64
- **Entrée**: 22007.53 @ 2025-02-03 09:31:00
- **Stop Loss**: 21786.82
- **Risk**: 220.70 points
- **TP 1RR**: 22228.23 ✅
- **TP 1.5RR**: 22338.58 ✅
- **TP 2RR**: 22448.93 ✅
- **TP 2.5RR**: 22559.28 ✅
- **TP 3RR**: 22669.63 ✅
- **TP 3.5RR**: 22779.98 ✅
- **TP 4RR**: 22890.33 ✅
- **TP 4.5RR**: 23000.68 ✅
- **TP 5RR**: 23111.03 ❌
- **PnL**: -220.70 points (-1.0R)
- **MFE**: 1003.39 points
- **MAE**: 240.99 points

### Trade #164 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 14:00:00
- **FVG 5m**: 22142.84 - 22165.78
- **Entrée**: 22139.23 @ 2025-02-03 14:06:00
- **Stop Loss**: 22176.86
- **Risk**: 37.63 points
- **TP 1RR**: 22101.60 ✅
- **TP 1.5RR**: 22082.79 ✅
- **TP 2RR**: 22063.97 ✅
- **TP 2.5RR**: 22045.16 ❌
- **TP 3RR**: 22026.34 ❌
- **TP 3.5RR**: 22007.53 ❌
- **TP 4RR**: 21988.71 ❌
- **TP 4.5RR**: 21969.89 ❌
- **TP 5RR**: 21951.08 ❌
- **PnL**: -37.63 points (-1.0R)
- **MFE**: 88.66 points
- **MAE**: 43.04 points

### Trade #165 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 15:30:00
- **FVG 5m**: 22103.15 - 22114.23
- **Entrée**: 22171.96 @ 2025-02-03 15:31:00
- **Stop Loss**: 22092.10
- **Risk**: 79.87 points
- **TP 1RR**: 22251.83 ✅
- **TP 1.5RR**: 22291.77 ❌
- **TP 2RR**: 22331.70 ❌
- **TP 2.5RR**: 22371.64 ❌
- **TP 3RR**: 22411.57 ❌
- **TP 3.5RR**: 22451.50 ❌
- **TP 4RR**: 22491.44 ❌
- **TP 4.5RR**: 22531.37 ❌
- **TP 5RR**: 22571.31 ❌
- **PnL**: -79.87 points (-1.0R)
- **MFE**: 96.91 points
- **MAE**: 82.48 points

### Trade #166 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 19:00:00
- **FVG 5m**: 22221.45 - 22232.79
- **Entrée**: 22199.80 @ 2025-02-03 19:01:00
- **Stop Loss**: 22243.91
- **Risk**: 44.11 points
- **TP 1RR**: 22155.69 ✅
- **TP 1.5RR**: 22133.64 ✅
- **TP 2RR**: 22111.59 ✅
- **TP 2.5RR**: 22089.53 ✅
- **TP 3RR**: 22067.48 ✅
- **TP 3.5RR**: 22045.42 ✅
- **TP 4RR**: 22023.37 ✅
- **TP 4.5RR**: 22001.32 ✅
- **TP 5RR**: 21979.26 ✅
- **PnL**: 220.54 points (5.0R)
- **MFE**: 233.26 points
- **MAE**: 7.22 points

### Trade #167 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 23:30:00
- **FVG 5m**: 22009.59 - 22058.04
- **Entrée**: 22064.23 @ 2025-02-03 23:50:00
- **Stop Loss**: 21998.58
- **Risk**: 65.65 points
- **TP 1RR**: 22129.87 ❌
- **TP 1.5RR**: 22162.70 ❌
- **TP 2RR**: 22195.52 ❌
- **TP 2.5RR**: 22228.34 ❌
- **TP 3RR**: 22261.17 ❌
- **TP 3.5RR**: 22293.99 ❌
- **TP 4RR**: 22326.81 ❌
- **TP 4.5RR**: 22359.64 ❌
- **TP 5RR**: 22392.46 ❌
- **PnL**: -65.65 points (-1.0R)
- **MFE**: 8.76 points
- **MAE**: 66.24 points

### Trade #168 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-04 00:45:00
- **FVG 5m**: 22009.59 - 22058.04
- **Entrée**: 22062.94 @ 2025-02-04 00:59:00
- **Stop Loss**: 21998.58
- **Risk**: 64.36 points
- **TP 1RR**: 22127.30 ❌
- **TP 1.5RR**: 22159.48 ❌
- **TP 2RR**: 22191.65 ❌
- **TP 2.5RR**: 22223.83 ❌
- **TP 3RR**: 22256.01 ❌
- **TP 3.5RR**: 22288.19 ❌
- **TP 4RR**: 22320.37 ❌
- **TP 4.5RR**: 22352.55 ❌
- **TP 5RR**: 22384.73 ❌
- **PnL**: -64.36 points (-1.0R)
- **MFE**: 25.26 points
- **MAE**: 68.82 points

### Trade #169 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-04 08:30:00
- **FVG 5m**: 22096.70 - 22100.05
- **Entrée**: 22115.26 @ 2025-02-04 08:32:00
- **Stop Loss**: 22085.66
- **Risk**: 29.61 points
- **TP 1RR**: 22144.87 ✅
- **TP 1.5RR**: 22159.67 ✅
- **TP 2RR**: 22174.47 ✅
- **TP 2.5RR**: 22189.28 ✅
- **TP 3RR**: 22204.08 ✅
- **TP 3.5RR**: 22218.88 ✅
- **TP 4RR**: 22233.68 ✅
- **TP 4.5RR**: 22248.49 ✅
- **TP 5RR**: 22263.29 ✅
- **PnL**: 148.03 points (5.0R)
- **MFE**: 160.06 points
- **MAE**: 8.25 points

### Trade #170 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-04 11:15:00
- **FVG 5m**: 22330.48 - 22333.57
- **Entrée**: 22283.57 @ 2025-02-04 11:16:00
- **Stop Loss**: 22344.74
- **Risk**: 61.17 points
- **TP 1RR**: 22222.40 ✅
- **TP 1.5RR**: 22191.81 ❌
- **TP 2RR**: 22161.23 ❌
- **TP 2.5RR**: 22130.64 ❌
- **TP 3RR**: 22100.06 ❌
- **TP 3.5RR**: 22069.48 ❌
- **TP 4RR**: 22038.89 ❌
- **TP 4.5RR**: 22008.31 ❌
- **TP 5RR**: 21977.72 ❌
- **PnL**: -61.17 points (-1.0R)
- **MFE**: 66.24 points
- **MAE**: 64.69 points

### Trade #171 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-04 15:00:00
- **FVG 5m**: 22327.12 - 22335.63
- **Entrée**: 22301.61 @ 2025-02-04 15:01:00
- **Stop Loss**: 22346.80
- **Risk**: 45.19 points
- **TP 1RR**: 22256.42 ✅
- **TP 1.5RR**: 22233.82 ✅
- **TP 2RR**: 22211.23 ✅
- **TP 2.5RR**: 22188.63 ✅
- **TP 3RR**: 22166.04 ✅
- **TP 3.5RR**: 22143.44 ✅
- **TP 4RR**: 22120.85 ✅
- **TP 4.5RR**: 22098.25 ✅
- **TP 5RR**: 22075.66 ❌
- **PnL**: -45.19 points (-1.0R)
- **MFE**: 208.26 points
- **MAE**: 50.52 points

### Trade #172 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-05 02:15:00
- **FVG 5m**: 22168.61 - 22180.99
- **Entrée**: 22181.24 @ 2025-02-05 02:16:00
- **Stop Loss**: 22157.53
- **Risk**: 23.71 points
- **TP 1RR**: 22204.96 ✅
- **TP 1.5RR**: 22216.81 ❌
- **TP 2RR**: 22228.67 ❌
- **TP 2.5RR**: 22240.53 ❌
- **TP 3RR**: 22252.38 ❌
- **TP 3.5RR**: 22264.24 ❌
- **TP 4RR**: 22276.10 ❌
- **TP 4.5RR**: 22287.95 ❌
- **TP 5RR**: 22299.81 ❌
- **PnL**: -23.71 points (-1.0R)
- **MFE**: 26.55 points
- **MAE**: 30.67 points

### Trade #173 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 02:30:00
- **FVG 5m**: 22183.30 - 22190.78
- **Entrée**: 22182.27 @ 2025-02-05 02:36:00
- **Stop Loss**: 22201.87
- **Risk**: 19.60 points
- **TP 1RR**: 22162.67 ✅
- **TP 1.5RR**: 22152.87 ✅
- **TP 2RR**: 22143.07 ✅
- **TP 2.5RR**: 22133.27 ✅
- **TP 3RR**: 22123.47 ✅
- **TP 3.5RR**: 22113.67 ✅
- **TP 4RR**: 22103.87 ✅
- **TP 4.5RR**: 22094.07 ✅
- **TP 5RR**: 22084.27 ❌
- **PnL**: -19.60 points (-1.0R)
- **MFE**: 88.92 points
- **MAE**: 38.92 points

### Trade #174 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 07:30:00
- **FVG 5m**: 22178.67 - 22182.79
- **Entrée**: 22176.09 @ 2025-02-05 07:35:00
- **Stop Loss**: 22193.88
- **Risk**: 17.79 points
- **TP 1RR**: 22158.30 ❌
- **TP 1.5RR**: 22149.40 ❌
- **TP 2RR**: 22140.50 ❌
- **TP 2.5RR**: 22131.61 ❌
- **TP 3RR**: 22122.71 ❌
- **TP 3.5RR**: 22113.81 ❌
- **TP 4RR**: 22104.92 ❌
- **TP 4.5RR**: 22096.02 ❌
- **TP 5RR**: 22087.12 ❌
- **PnL**: -17.79 points (-1.0R)
- **MFE**: 1.29 points
- **MAE**: 27.84 points

### Trade #175 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 12:15:00
- **FVG 5m**: 22391.82 - 22400.32
- **Entrée**: 22381.51 @ 2025-02-05 12:16:00
- **Stop Loss**: 22411.52
- **Risk**: 30.02 points
- **TP 1RR**: 22351.49 ✅
- **TP 1.5RR**: 22336.49 ❌
- **TP 2RR**: 22321.48 ❌
- **TP 2.5RR**: 22306.47 ❌
- **TP 3RR**: 22291.46 ❌
- **TP 3.5RR**: 22276.45 ❌
- **TP 4RR**: 22261.45 ❌
- **TP 4.5RR**: 22246.44 ❌
- **TP 5RR**: 22231.43 ❌
- **PnL**: -30.02 points (-1.0R)
- **MFE**: 38.40 points
- **MAE**: 32.48 points

### Trade #176 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 12:15:00
- **FVG 5m**: 22391.82 - 22400.32
- **Entrée**: 22381.51 @ 2025-02-05 12:16:00
- **Stop Loss**: 22411.52
- **Risk**: 30.02 points
- **TP 1RR**: 22351.49 ✅
- **TP 1.5RR**: 22336.49 ❌
- **TP 2RR**: 22321.48 ❌
- **TP 2.5RR**: 22306.47 ❌
- **TP 3RR**: 22291.46 ❌
- **TP 3.5RR**: 22276.45 ❌
- **TP 4RR**: 22261.45 ❌
- **TP 4.5RR**: 22246.44 ❌
- **TP 5RR**: 22231.43 ❌
- **PnL**: -30.02 points (-1.0R)
- **MFE**: 38.40 points
- **MAE**: 32.48 points

### Trade #177 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 06:45:00
- **FVG 5m**: 22405.99 - 22412.44
- **Entrée**: 22424.04 @ 2025-02-06 06:46:00
- **Stop Loss**: 22394.79
- **Risk**: 29.24 points
- **TP 1RR**: 22453.28 ✅
- **TP 1.5RR**: 22467.90 ✅
- **TP 2RR**: 22482.53 ✅
- **TP 2.5RR**: 22497.15 ✅
- **TP 3RR**: 22511.77 ✅
- **TP 3.5RR**: 22526.39 ❌
- **TP 4RR**: 22541.02 ❌
- **TP 4.5RR**: 22555.64 ❌
- **TP 5RR**: 22570.26 ❌
- **PnL**: -29.24 points (-1.0R)
- **MFE**: 101.29 points
- **MAE**: 40.21 points

### Trade #178 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 07:45:00
- **FVG 5m**: 22405.99 - 22412.44
- **Entrée**: 22431.25 @ 2025-02-06 07:46:00
- **Stop Loss**: 22394.79
- **Risk**: 36.46 points
- **TP 1RR**: 22467.71 ✅
- **TP 1.5RR**: 22485.94 ✅
- **TP 2RR**: 22504.18 ✅
- **TP 2.5RR**: 22522.41 ✅
- **TP 3RR**: 22540.64 ❌
- **TP 3.5RR**: 22558.87 ❌
- **TP 4RR**: 22577.10 ❌
- **TP 4.5RR**: 22595.33 ❌
- **TP 5RR**: 22613.56 ❌
- **PnL**: -36.46 points (-1.0R)
- **MFE**: 94.08 points
- **MAE**: 47.42 points

### Trade #179 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 07:45:00
- **FVG 5m**: 22405.99 - 22412.44
- **Entrée**: 22431.25 @ 2025-02-06 07:46:00
- **Stop Loss**: 22394.79
- **Risk**: 36.46 points
- **TP 1RR**: 22467.71 ✅
- **TP 1.5RR**: 22485.94 ✅
- **TP 2RR**: 22504.18 ✅
- **TP 2.5RR**: 22522.41 ✅
- **TP 3RR**: 22540.64 ❌
- **TP 3.5RR**: 22558.87 ❌
- **TP 4RR**: 22577.10 ❌
- **TP 4.5RR**: 22595.33 ❌
- **TP 5RR**: 22613.56 ❌
- **PnL**: -36.46 points (-1.0R)
- **MFE**: 94.08 points
- **MAE**: 47.42 points

### Trade #180 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 09:15:00
- **FVG 5m**: 22471.46 - 22485.64
- **Entrée**: 22470.17 @ 2025-02-06 09:25:00
- **Stop Loss**: 22496.88
- **Risk**: 26.71 points
- **TP 1RR**: 22443.46 ❌
- **TP 1.5RR**: 22430.11 ❌
- **TP 2RR**: 22416.76 ❌
- **TP 2.5RR**: 22403.40 ❌
- **TP 3RR**: 22390.05 ❌
- **TP 3.5RR**: 22376.70 ❌
- **TP 4RR**: 22363.34 ❌
- **TP 4.5RR**: 22349.99 ❌
- **TP 5RR**: 22336.63 ❌
- **PnL**: -26.71 points (-1.0R)
- **MFE**: 17.53 points
- **MAE**: 28.61 points

### Trade #181 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 09:15:00
- **FVG 5m**: 22471.46 - 22485.64
- **Entrée**: 22470.17 @ 2025-02-06 09:25:00
- **Stop Loss**: 22496.88
- **Risk**: 26.71 points
- **TP 1RR**: 22443.46 ❌
- **TP 1.5RR**: 22430.11 ❌
- **TP 2RR**: 22416.76 ❌
- **TP 2.5RR**: 22403.40 ❌
- **TP 3RR**: 22390.05 ❌
- **TP 3.5RR**: 22376.70 ❌
- **TP 4RR**: 22363.34 ❌
- **TP 4.5RR**: 22349.99 ❌
- **TP 5RR**: 22336.63 ❌
- **PnL**: -26.71 points (-1.0R)
- **MFE**: 17.53 points
- **MAE**: 28.61 points

### Trade #182 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 09:15:00
- **FVG 5m**: 22471.46 - 22485.64
- **Entrée**: 22470.17 @ 2025-02-06 09:25:00
- **Stop Loss**: 22496.88
- **Risk**: 26.71 points
- **TP 1RR**: 22443.46 ❌
- **TP 1.5RR**: 22430.11 ❌
- **TP 2RR**: 22416.76 ❌
- **TP 2.5RR**: 22403.40 ❌
- **TP 3RR**: 22390.05 ❌
- **TP 3.5RR**: 22376.70 ❌
- **TP 4RR**: 22363.34 ❌
- **TP 4.5RR**: 22349.99 ❌
- **TP 5RR**: 22336.63 ❌
- **PnL**: -26.71 points (-1.0R)
- **MFE**: 17.53 points
- **MAE**: 28.61 points

### Trade #183 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 13:30:00
- **FVG 5m**: 22461.41 - 22465.53
- **Entrée**: 22466.31 @ 2025-02-06 14:25:00
- **Stop Loss**: 22450.18
- **Risk**: 16.13 points
- **TP 1RR**: 22482.43 ✅
- **TP 1.5RR**: 22490.50 ✅
- **TP 2RR**: 22498.56 ✅
- **TP 2.5RR**: 22506.62 ✅
- **TP 3RR**: 22514.69 ✅
- **TP 3.5RR**: 22522.75 ✅
- **TP 4RR**: 22530.82 ✅
- **TP 4.5RR**: 22538.88 ✅
- **TP 5RR**: 22546.94 ✅
- **PnL**: 80.64 points (5.0R)
- **MFE**: 93.56 points
- **MAE**: 4.90 points

### Trade #184 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 15:00:00
- **FVG 5m**: 22509.61 - 22533.06
- **Entrée**: 22452.64 @ 2025-02-06 15:01:00
- **Stop Loss**: 22544.33
- **Risk**: 91.68 points
- **TP 1RR**: 22360.96 ❌
- **TP 1.5RR**: 22315.12 ❌
- **TP 2RR**: 22269.28 ❌
- **TP 2.5RR**: 22223.44 ❌
- **TP 3RR**: 22177.60 ❌
- **TP 3.5RR**: 22131.76 ❌
- **TP 4RR**: 22085.92 ❌
- **TP 4.5RR**: 22040.08 ❌
- **TP 5RR**: 21994.24 ❌
- **PnL**: -91.68 points (-1.0R)
- **MFE**: 17.01 points
- **MAE**: 92.79 points

### Trade #185 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 15:00:00
- **FVG 5m**: 22509.61 - 22533.06
- **Entrée**: 22452.64 @ 2025-02-06 15:01:00
- **Stop Loss**: 22544.33
- **Risk**: 91.68 points
- **TP 1RR**: 22360.96 ❌
- **TP 1.5RR**: 22315.12 ❌
- **TP 2RR**: 22269.28 ❌
- **TP 2.5RR**: 22223.44 ❌
- **TP 3RR**: 22177.60 ❌
- **TP 3.5RR**: 22131.76 ❌
- **TP 4RR**: 22085.92 ❌
- **TP 4.5RR**: 22040.08 ❌
- **TP 5RR**: 21994.24 ❌
- **PnL**: -91.68 points (-1.0R)
- **MFE**: 17.01 points
- **MAE**: 92.79 points

### Trade #186 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 21:00:00
- **FVG 5m**: 22549.30 - 22565.79
- **Entrée**: 22545.69 @ 2025-02-06 21:43:00
- **Stop Loss**: 22577.08
- **Risk**: 31.39 points
- **TP 1RR**: 22514.30 ✅
- **TP 1.5RR**: 22498.61 ❌
- **TP 2RR**: 22482.92 ❌
- **TP 2.5RR**: 22467.22 ❌
- **TP 3RR**: 22451.53 ❌
- **TP 3.5RR**: 22435.84 ❌
- **TP 4RR**: 22420.14 ❌
- **TP 4.5RR**: 22404.45 ❌
- **TP 5RR**: 22388.76 ❌
- **PnL**: -31.39 points (-1.0R)
- **MFE**: 80.67 points
- **MAE**: 63.40 points

### Trade #187 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-07 09:00:00
- **FVG 5m**: 22572.24 - 22604.97
- **Entrée**: 22495.17 @ 2025-02-07 09:01:00
- **Stop Loss**: 22616.27
- **Risk**: 121.10 points
- **TP 1RR**: 22374.07 ✅
- **TP 1.5RR**: 22313.52 ✅
- **TP 2RR**: 22252.97 ✅
- **TP 2.5RR**: 22192.42 ✅
- **TP 3RR**: 22131.87 ✅
- **TP 3.5RR**: 22071.32 ❌
- **TP 4RR**: 22010.77 ❌
- **TP 4.5RR**: 21950.22 ❌
- **TP 5RR**: 21889.67 ❌
- **PnL**: -121.10 points (-1.0R)
- **MFE**: 413.93 points
- **MAE**: 134.54 points

### Trade #188 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-07 13:00:00
- **FVG 5m**: 22364.24 - 22373.52
- **Entrée**: 22299.03 @ 2025-02-07 13:01:00
- **Stop Loss**: 22384.71
- **Risk**: 85.67 points
- **TP 1RR**: 22213.36 ✅
- **TP 1.5RR**: 22170.52 ✅
- **TP 2RR**: 22127.68 ✅
- **TP 2.5RR**: 22084.85 ✅
- **TP 3RR**: 22042.01 ❌
- **TP 3.5RR**: 21999.17 ❌
- **TP 4RR**: 21956.33 ❌
- **TP 4.5RR**: 21913.50 ❌
- **TP 5RR**: 21870.66 ❌
- **PnL**: -85.67 points (-1.0R)
- **MFE**: 217.79 points
- **MAE**: 90.21 points

### Trade #189 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-09 17:00:00
- **FVG 5m**: 22266.04 - 22270.42
- **Entrée**: 22276.09 @ 2025-02-09 17:46:00
- **Stop Loss**: 22254.91
- **Risk**: 21.18 points
- **TP 1RR**: 22297.28 ✅
- **TP 1.5RR**: 22307.87 ✅
- **TP 2RR**: 22318.46 ✅
- **TP 2.5RR**: 22329.05 ✅
- **TP 3RR**: 22339.65 ✅
- **TP 3.5RR**: 22350.24 ✅
- **TP 4RR**: 22360.83 ✅
- **TP 4.5RR**: 22371.42 ✅
- **TP 5RR**: 22382.02 ✅
- **PnL**: 105.92 points (5.0R)
- **MFE**: 106.45 points
- **MAE**: 5.93 points

### Trade #190 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-09 17:00:00
- **FVG 5m**: 22266.04 - 22270.42
- **Entrée**: 22276.09 @ 2025-02-09 17:46:00
- **Stop Loss**: 22254.91
- **Risk**: 21.18 points
- **TP 1RR**: 22297.28 ✅
- **TP 1.5RR**: 22307.87 ✅
- **TP 2RR**: 22318.46 ✅
- **TP 2.5RR**: 22329.05 ✅
- **TP 3RR**: 22339.65 ✅
- **TP 3.5RR**: 22350.24 ✅
- **TP 4RR**: 22360.83 ✅
- **TP 4.5RR**: 22371.42 ✅
- **TP 5RR**: 22382.02 ✅
- **PnL**: 105.92 points (5.0R)
- **MFE**: 106.45 points
- **MAE**: 5.93 points

### Trade #191 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-10 08:30:00
- **FVG 5m**: 22443.62 - 22451.61
- **Entrée**: 22458.32 @ 2025-02-10 08:42:00
- **Stop Loss**: 22432.40
- **Risk**: 25.91 points
- **TP 1RR**: 22484.23 ✅
- **TP 1.5RR**: 22497.18 ❌
- **TP 2RR**: 22510.14 ❌
- **TP 2.5RR**: 22523.10 ❌
- **TP 3RR**: 22536.05 ❌
- **TP 3.5RR**: 22549.01 ❌
- **TP 4RR**: 22561.97 ❌
- **TP 4.5RR**: 22574.92 ❌
- **TP 5RR**: 22587.88 ❌
- **PnL**: -25.91 points (-1.0R)
- **MFE**: 26.03 points
- **MAE**: 32.99 points

### Trade #192 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 03:00:00
- **FVG 5m**: 22413.21 - 22431.25
- **Entrée**: 22447.49 @ 2025-02-11 03:01:00
- **Stop Loss**: 22402.00
- **Risk**: 45.49 points
- **TP 1RR**: 22492.98 ❌
- **TP 1.5RR**: 22515.72 ❌
- **TP 2RR**: 22538.46 ❌
- **TP 2.5RR**: 22561.21 ❌
- **TP 3RR**: 22583.95 ❌
- **TP 3.5RR**: 22606.69 ❌
- **TP 4RR**: 22629.44 ❌
- **TP 4.5RR**: 22652.18 ❌
- **TP 5RR**: 22674.92 ❌
- **PnL**: -45.49 points (-1.0R)
- **MFE**: 19.33 points
- **MAE**: 46.65 points

### Trade #193 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 05:00:00
- **FVG 5m**: 22409.34 - 22414.50
- **Entrée**: 22417.33 @ 2025-02-11 05:04:00
- **Stop Loss**: 22398.14
- **Risk**: 19.19 points
- **TP 1RR**: 22436.53 ✅
- **TP 1.5RR**: 22446.13 ❌
- **TP 2RR**: 22455.72 ❌
- **TP 2.5RR**: 22465.32 ❌
- **TP 3RR**: 22474.92 ❌
- **TP 3.5RR**: 22484.52 ❌
- **TP 4RR**: 22494.11 ❌
- **TP 4.5RR**: 22503.71 ❌
- **TP 5RR**: 22513.31 ❌
- **PnL**: -19.19 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 30.93 points

### Trade #194 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 08:30:00
- **FVG 5m**: 22384.86 - 22388.73
- **Entrée**: 22408.06 @ 2025-02-11 08:31:00
- **Stop Loss**: 22373.67
- **Risk**: 34.39 points
- **TP 1RR**: 22442.44 ✅
- **TP 1.5RR**: 22459.64 ✅
- **TP 2RR**: 22476.83 ✅
- **TP 2.5RR**: 22494.03 ✅
- **TP 3RR**: 22511.22 ✅
- **TP 3.5RR**: 22528.42 ✅
- **TP 4RR**: 22545.61 ✅
- **TP 4.5RR**: 22562.81 ❌
- **TP 5RR**: 22580.00 ❌
- **PnL**: -34.39 points (-1.0R)
- **MFE**: 140.73 points
- **MAE**: 175.52 points

### Trade #195 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 08:30:00
- **FVG 5m**: 22384.86 - 22388.73
- **Entrée**: 22408.06 @ 2025-02-11 08:31:00
- **Stop Loss**: 22373.67
- **Risk**: 34.39 points
- **TP 1RR**: 22442.44 ✅
- **TP 1.5RR**: 22459.64 ✅
- **TP 2RR**: 22476.83 ✅
- **TP 2.5RR**: 22494.03 ✅
- **TP 3RR**: 22511.22 ✅
- **TP 3.5RR**: 22528.42 ✅
- **TP 4RR**: 22545.61 ✅
- **TP 4.5RR**: 22562.81 ❌
- **TP 5RR**: 22580.00 ❌
- **PnL**: -34.39 points (-1.0R)
- **MFE**: 140.73 points
- **MAE**: 175.52 points

### Trade #196 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 08:30:00
- **FVG 5m**: 22384.86 - 22388.73
- **Entrée**: 22408.06 @ 2025-02-11 08:31:00
- **Stop Loss**: 22373.67
- **Risk**: 34.39 points
- **TP 1RR**: 22442.44 ✅
- **TP 1.5RR**: 22459.64 ✅
- **TP 2RR**: 22476.83 ✅
- **TP 2.5RR**: 22494.03 ✅
- **TP 3RR**: 22511.22 ✅
- **TP 3.5RR**: 22528.42 ✅
- **TP 4RR**: 22545.61 ✅
- **TP 4.5RR**: 22562.81 ❌
- **TP 5RR**: 22580.00 ❌
- **PnL**: -34.39 points (-1.0R)
- **MFE**: 140.73 points
- **MAE**: 175.52 points

### Trade #197 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 09:15:00
- **FVG 5m**: 22384.86 - 22388.73
- **Entrée**: 22475.07 @ 2025-02-11 09:16:00
- **Stop Loss**: 22373.67
- **Risk**: 101.40 points
- **TP 1RR**: 22576.47 ❌
- **TP 1.5RR**: 22627.17 ❌
- **TP 2RR**: 22677.87 ❌
- **TP 2.5RR**: 22728.57 ❌
- **TP 3RR**: 22779.27 ❌
- **TP 3.5RR**: 22829.98 ❌
- **TP 4RR**: 22880.68 ❌
- **TP 4.5RR**: 22931.38 ❌
- **TP 5RR**: 22982.08 ❌
- **PnL**: -101.40 points (-1.0R)
- **MFE**: 73.71 points
- **MAE**: 242.53 points

### Trade #198 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 10:45:00
- **FVG 5m**: 22529.45 - 22533.83
- **Entrée**: 22511.93 @ 2025-02-11 10:46:00
- **Stop Loss**: 22545.10
- **Risk**: 33.17 points
- **TP 1RR**: 22478.75 ✅
- **TP 1.5RR**: 22462.16 ✅
- **TP 2RR**: 22445.58 ✅
- **TP 2.5RR**: 22428.99 ✅
- **TP 3RR**: 22412.40 ✅
- **TP 3.5RR**: 22395.81 ✅
- **TP 4RR**: 22379.23 ✅
- **TP 4.5RR**: 22362.64 ✅
- **TP 5RR**: 22346.05 ✅
- **PnL**: 165.87 points (5.0R)
- **MFE**: 279.39 points
- **MAE**: 14.69 points

### Trade #199 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 10:45:00
- **FVG 5m**: 22529.45 - 22533.83
- **Entrée**: 22511.93 @ 2025-02-11 10:46:00
- **Stop Loss**: 22545.10
- **Risk**: 33.17 points
- **TP 1RR**: 22478.75 ✅
- **TP 1.5RR**: 22462.16 ✅
- **TP 2RR**: 22445.58 ✅
- **TP 2.5RR**: 22428.99 ✅
- **TP 3RR**: 22412.40 ✅
- **TP 3.5RR**: 22395.81 ✅
- **TP 4RR**: 22379.23 ✅
- **TP 4.5RR**: 22362.64 ✅
- **TP 5RR**: 22346.05 ✅
- **PnL**: 165.87 points (5.0R)
- **MFE**: 279.39 points
- **MAE**: 14.69 points

### Trade #200 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 11:00:00
- **FVG 5m**: 22529.45 - 22533.83
- **Entrée**: 22455.74 @ 2025-02-11 11:01:00
- **Stop Loss**: 22545.10
- **Risk**: 89.36 points
- **TP 1RR**: 22366.38 ✅
- **TP 1.5RR**: 22321.69 ✅
- **TP 2RR**: 22277.01 ✅
- **TP 2.5RR**: 22232.33 ✅
- **TP 3RR**: 22187.65 ✅
- **TP 3.5RR**: 22142.97 ❌
- **TP 4RR**: 22098.29 ❌
- **TP 4.5RR**: 22053.61 ❌
- **TP 5RR**: 22008.92 ❌
- **PnL**: -89.36 points (-1.0R)
- **MFE**: 278.88 points
- **MAE**: 90.73 points

### Trade #201 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:00:00
- **FVG 5m**: 22489.24 - 22492.85
- **Entrée**: 22260.63 @ 2025-02-12 07:30:00
- **Stop Loss**: 22504.10
- **Risk**: 243.47 points
- **TP 1RR**: 22017.16 ❌
- **TP 1.5RR**: 21895.42 ❌
- **TP 2RR**: 21773.68 ❌
- **TP 2.5RR**: 21651.95 ❌
- **TP 3RR**: 21530.21 ❌
- **TP 3.5RR**: 21408.48 ❌
- **TP 4RR**: 21286.74 ❌
- **TP 4.5RR**: 21165.01 ❌
- **TP 5RR**: 21043.27 ❌
- **PnL**: -243.47 points (-1.0R)
- **MFE**: 83.77 points
- **MAE**: 254.65 points

### Trade #202 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:30:00
- **FVG 5m**: 22489.24 - 22492.85
- **Entrée**: 22263.72 @ 2025-02-12 07:31:00
- **Stop Loss**: 22504.10
- **Risk**: 240.38 points
- **TP 1RR**: 22023.34 ❌
- **TP 1.5RR**: 21903.15 ❌
- **TP 2RR**: 21782.96 ❌
- **TP 2.5RR**: 21662.77 ❌
- **TP 3RR**: 21542.58 ❌
- **TP 3.5RR**: 21422.39 ❌
- **TP 4RR**: 21302.21 ❌
- **TP 4.5RR**: 21182.02 ❌
- **TP 5RR**: 21061.83 ❌
- **PnL**: -240.38 points (-1.0R)
- **MFE**: 86.86 points
- **MAE**: 251.56 points

### Trade #203 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:30:00
- **FVG 5m**: 22489.24 - 22492.85
- **Entrée**: 22263.72 @ 2025-02-12 07:31:00
- **Stop Loss**: 22504.10
- **Risk**: 240.38 points
- **TP 1RR**: 22023.34 ❌
- **TP 1.5RR**: 21903.15 ❌
- **TP 2RR**: 21782.96 ❌
- **TP 2.5RR**: 21662.77 ❌
- **TP 3RR**: 21542.58 ❌
- **TP 3.5RR**: 21422.39 ❌
- **TP 4RR**: 21302.21 ❌
- **TP 4.5RR**: 21182.02 ❌
- **TP 5RR**: 21061.83 ❌
- **PnL**: -240.38 points (-1.0R)
- **MFE**: 86.86 points
- **MAE**: 251.56 points

### Trade #204 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:30:00
- **FVG 5m**: 22489.24 - 22492.85
- **Entrée**: 22263.72 @ 2025-02-12 07:31:00
- **Stop Loss**: 22504.10
- **Risk**: 240.38 points
- **TP 1RR**: 22023.34 ❌
- **TP 1.5RR**: 21903.15 ❌
- **TP 2RR**: 21782.96 ❌
- **TP 2.5RR**: 21662.77 ❌
- **TP 3RR**: 21542.58 ❌
- **TP 3.5RR**: 21422.39 ❌
- **TP 4RR**: 21302.21 ❌
- **TP 4.5RR**: 21182.02 ❌
- **TP 5RR**: 21061.83 ❌
- **PnL**: -240.38 points (-1.0R)
- **MFE**: 86.86 points
- **MAE**: 251.56 points

### Trade #205 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 09:30:00
- **FVG 5m**: 22303.93 - 22340.27
- **Entrée**: 22378.42 @ 2025-02-12 09:31:00
- **Stop Loss**: 22292.78
- **Risk**: 85.64 points
- **TP 1RR**: 22464.05 ✅
- **TP 1.5RR**: 22506.87 ✅
- **TP 2RR**: 22549.69 ✅
- **TP 2.5RR**: 22592.51 ✅
- **TP 3RR**: 22635.33 ✅
- **TP 3.5RR**: 22678.15 ✅
- **TP 4RR**: 22720.97 ✅
- **TP 4.5RR**: 22763.79 ✅
- **TP 5RR**: 22806.61 ✅
- **PnL**: 428.20 points (5.0R)
- **MFE**: 429.40 points
- **MAE**: 62.12 points

### Trade #206 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 10:45:00
- **FVG 5m**: 22355.73 - 22358.57
- **Entrée**: 22397.75 @ 2025-02-12 10:46:00
- **Stop Loss**: 22344.56
- **Risk**: 53.19 points
- **TP 1RR**: 22450.94 ✅
- **TP 1.5RR**: 22477.53 ✅
- **TP 2RR**: 22504.13 ✅
- **TP 2.5RR**: 22530.72 ✅
- **TP 3RR**: 22557.32 ✅
- **TP 3.5RR**: 22583.91 ✅
- **TP 4RR**: 22610.51 ✅
- **TP 4.5RR**: 22637.10 ✅
- **TP 5RR**: 22663.69 ✅
- **PnL**: 265.95 points (5.0R)
- **MFE**: 273.72 points
- **MAE**: 10.31 points

### Trade #207 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 11:45:00
- **FVG 5m**: 22355.73 - 22358.57
- **Entrée**: 22458.83 @ 2025-02-12 11:46:00
- **Stop Loss**: 22344.56
- **Risk**: 114.27 points
- **TP 1RR**: 22573.11 ✅
- **TP 1.5RR**: 22630.24 ✅
- **TP 2RR**: 22687.38 ✅
- **TP 2.5RR**: 22744.52 ✅
- **TP 3RR**: 22801.65 ✅
- **TP 3.5RR**: 22858.79 ✅
- **TP 4RR**: 22915.93 ✅
- **TP 4.5RR**: 22973.07 ✅
- **TP 5RR**: 23030.20 ❌
- **PnL**: -114.27 points (-1.0R)
- **MFE**: 552.08 points
- **MAE**: 117.27 points

### Trade #208 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 19:15:00
- **FVG 5m**: 22564.50 - 22576.36
- **Entrée**: 22564.25 @ 2025-02-12 19:26:00
- **Stop Loss**: 22587.65
- **Risk**: 23.40 points
- **TP 1RR**: 22540.85 ❌
- **TP 1.5RR**: 22529.14 ❌
- **TP 2RR**: 22517.44 ❌
- **TP 2.5RR**: 22505.74 ❌
- **TP 3RR**: 22494.04 ❌
- **TP 3.5RR**: 22482.34 ❌
- **TP 4RR**: 22470.64 ❌
- **TP 4.5RR**: 22458.94 ❌
- **TP 5RR**: 22447.24 ❌
- **PnL**: -23.40 points (-1.0R)
- **MFE**: 6.44 points
- **MAE**: 29.12 points

### Trade #209 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 19:45:00
- **FVG 5m**: 22570.43 - 22578.94
- **Entrée**: 22570.18 @ 2025-02-12 19:53:00
- **Stop Loss**: 22590.23
- **Risk**: 20.05 points
- **TP 1RR**: 22550.12 ✅
- **TP 1.5RR**: 22540.10 ❌
- **TP 2RR**: 22530.07 ❌
- **TP 2.5RR**: 22520.04 ❌
- **TP 3RR**: 22510.02 ❌
- **TP 3.5RR**: 22499.99 ❌
- **TP 4RR**: 22489.96 ❌
- **TP 4.5RR**: 22479.94 ❌
- **TP 5RR**: 22469.91 ❌
- **PnL**: -20.05 points (-1.0R)
- **MFE**: 21.65 points
- **MAE**: 20.88 points

### Trade #210 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 01:30:00
- **FVG 5m**: 22580.23 - 22585.38
- **Entrée**: 22558.32 @ 2025-02-13 01:31:00
- **Stop Loss**: 22596.67
- **Risk**: 38.36 points
- **TP 1RR**: 22519.96 ✅
- **TP 1.5RR**: 22500.79 ✅
- **TP 2RR**: 22481.61 ✅
- **TP 2.5RR**: 22462.43 ✅
- **TP 3RR**: 22443.25 ✅
- **TP 3.5RR**: 22424.07 ❌
- **TP 4RR**: 22404.90 ❌
- **TP 4.5RR**: 22385.72 ❌
- **TP 5RR**: 22366.54 ❌
- **PnL**: -38.36 points (-1.0R)
- **MFE**: 131.71 points
- **MAE**: 40.21 points

### Trade #211 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 02:00:00
- **FVG 5m**: 22580.23 - 22585.38
- **Entrée**: 22525.07 @ 2025-02-13 02:01:00
- **Stop Loss**: 22596.67
- **Risk**: 71.60 points
- **TP 1RR**: 22453.47 ✅
- **TP 1.5RR**: 22417.66 ❌
- **TP 2RR**: 22381.86 ❌
- **TP 2.5RR**: 22346.06 ❌
- **TP 3RR**: 22310.26 ❌
- **TP 3.5RR**: 22274.46 ❌
- **TP 4RR**: 22238.65 ❌
- **TP 4.5RR**: 22202.85 ❌
- **TP 5RR**: 22167.05 ❌
- **PnL**: -71.60 points (-1.0R)
- **MFE**: 98.46 points
- **MAE**: 73.46 points

### Trade #212 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 02:00:00
- **FVG 5m**: 22580.23 - 22585.38
- **Entrée**: 22525.07 @ 2025-02-13 02:01:00
- **Stop Loss**: 22596.67
- **Risk**: 71.60 points
- **TP 1RR**: 22453.47 ✅
- **TP 1.5RR**: 22417.66 ❌
- **TP 2RR**: 22381.86 ❌
- **TP 2.5RR**: 22346.06 ❌
- **TP 3RR**: 22310.26 ❌
- **TP 3.5RR**: 22274.46 ❌
- **TP 4RR**: 22238.65 ❌
- **TP 4.5RR**: 22202.85 ❌
- **TP 5RR**: 22167.05 ❌
- **PnL**: -71.60 points (-1.0R)
- **MFE**: 98.46 points
- **MAE**: 73.46 points

### Trade #213 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 02:00:00
- **FVG 5m**: 22580.23 - 22585.38
- **Entrée**: 22525.07 @ 2025-02-13 02:01:00
- **Stop Loss**: 22596.67
- **Risk**: 71.60 points
- **TP 1RR**: 22453.47 ✅
- **TP 1.5RR**: 22417.66 ❌
- **TP 2RR**: 22381.86 ❌
- **TP 2.5RR**: 22346.06 ❌
- **TP 3RR**: 22310.26 ❌
- **TP 3.5RR**: 22274.46 ❌
- **TP 4RR**: 22238.65 ❌
- **TP 4.5RR**: 22202.85 ❌
- **TP 5RR**: 22167.05 ❌
- **PnL**: -71.60 points (-1.0R)
- **MFE**: 98.46 points
- **MAE**: 73.46 points

### Trade #214 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 02:30:00
- **FVG 5m**: 22466.56 - 22481.77
- **Entrée**: 22484.60 @ 2025-02-13 03:16:00
- **Stop Loss**: 22455.33
- **Risk**: 29.28 points
- **TP 1RR**: 22513.88 ✅
- **TP 1.5RR**: 22528.52 ✅
- **TP 2RR**: 22543.16 ✅
- **TP 2.5RR**: 22557.79 ✅
- **TP 3RR**: 22572.43 ✅
- **TP 3.5RR**: 22587.07 ✅
- **TP 4RR**: 22601.71 ✅
- **TP 4.5RR**: 22616.34 ✅
- **TP 5RR**: 22630.98 ✅
- **PnL**: 146.38 points (5.0R)
- **MFE**: 160.06 points
- **MAE**: 22.68 points

### Trade #215 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 07:30:00
- **FVG 5m**: 22512.96 - 22523.52
- **Entrée**: 22539.76 @ 2025-02-13 07:33:00
- **Stop Loss**: 22501.70
- **Risk**: 38.06 points
- **TP 1RR**: 22577.82 ✅
- **TP 1.5RR**: 22596.85 ✅
- **TP 2RR**: 22615.88 ✅
- **TP 2.5RR**: 22634.92 ✅
- **TP 3RR**: 22653.95 ✅
- **TP 3.5RR**: 22672.98 ✅
- **TP 4RR**: 22692.01 ✅
- **TP 4.5RR**: 22711.04 ✅
- **TP 5RR**: 22730.07 ✅
- **PnL**: 190.31 points (5.0R)
- **MFE**: 191.50 points
- **MAE**: 28.87 points

### Trade #216 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 10:45:00
- **FVG 5m**: 22676.11 - 22710.90
- **Entrée**: 22674.82 @ 2025-02-13 10:51:00
- **Stop Loss**: 22722.26
- **Risk**: 47.44 points
- **TP 1RR**: 22627.38 ✅
- **TP 1.5RR**: 22603.66 ✅
- **TP 2RR**: 22579.94 ✅
- **TP 2.5RR**: 22556.22 ❌
- **TP 3RR**: 22532.50 ❌
- **TP 3.5RR**: 22508.78 ❌
- **TP 4RR**: 22485.06 ❌
- **TP 4.5RR**: 22461.34 ❌
- **TP 5RR**: 22437.62 ❌
- **PnL**: -47.44 points (-1.0R)
- **MFE**: 106.45 points
- **MAE**: 53.87 points

### Trade #217 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 10:45:00
- **FVG 5m**: 22676.11 - 22710.90
- **Entrée**: 22674.82 @ 2025-02-13 10:51:00
- **Stop Loss**: 22722.26
- **Risk**: 47.44 points
- **TP 1RR**: 22627.38 ✅
- **TP 1.5RR**: 22603.66 ✅
- **TP 2RR**: 22579.94 ✅
- **TP 2.5RR**: 22556.22 ❌
- **TP 3RR**: 22532.50 ❌
- **TP 3.5RR**: 22508.78 ❌
- **TP 4RR**: 22485.06 ❌
- **TP 4.5RR**: 22461.34 ❌
- **TP 5RR**: 22437.62 ❌
- **PnL**: -47.44 points (-1.0R)
- **MFE**: 106.45 points
- **MAE**: 53.87 points

### Trade #218 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 12:30:00
- **FVG 5m**: 22649.56 - 22655.75
- **Entrée**: 22669.15 @ 2025-02-13 12:57:00
- **Stop Loss**: 22638.23
- **Risk**: 30.91 points
- **TP 1RR**: 22700.06 ✅
- **TP 1.5RR**: 22715.52 ✅
- **TP 2RR**: 22730.97 ✅
- **TP 2.5RR**: 22746.43 ✅
- **TP 3RR**: 22761.89 ✅
- **TP 3.5RR**: 22777.34 ✅
- **TP 4RR**: 22792.80 ✅
- **TP 4.5RR**: 22808.26 ✅
- **TP 5RR**: 22823.71 ✅
- **PnL**: 154.57 points (5.0R)
- **MFE**: 155.68 points
- **MAE**: 0.26 points

### Trade #219 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 12:45:00
- **FVG 5m**: 22649.56 - 22655.75
- **Entrée**: 22669.15 @ 2025-02-13 12:57:00
- **Stop Loss**: 22638.23
- **Risk**: 30.91 points
- **TP 1RR**: 22700.06 ✅
- **TP 1.5RR**: 22715.52 ✅
- **TP 2RR**: 22730.97 ✅
- **TP 2.5RR**: 22746.43 ✅
- **TP 3RR**: 22761.89 ✅
- **TP 3.5RR**: 22777.34 ✅
- **TP 4RR**: 22792.80 ✅
- **TP 4.5RR**: 22808.26 ✅
- **TP 5RR**: 22823.71 ✅
- **PnL**: 154.57 points (5.0R)
- **MFE**: 155.68 points
- **MAE**: 0.26 points

### Trade #220 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 23:30:00
- **FVG 5m**: 22821.73 - 22824.57
- **Entrée**: 22821.22 @ 2025-02-13 23:31:00
- **Stop Loss**: 22835.98
- **Risk**: 14.76 points
- **TP 1RR**: 22806.45 ✅
- **TP 1.5RR**: 22799.07 ✅
- **TP 2RR**: 22791.69 ❌
- **TP 2.5RR**: 22784.31 ❌
- **TP 3RR**: 22776.93 ❌
- **TP 3.5RR**: 22769.55 ❌
- **TP 4RR**: 22762.16 ❌
- **TP 4.5RR**: 22754.78 ❌
- **TP 5RR**: 22747.40 ❌
- **PnL**: -14.76 points (-1.0R)
- **MFE**: 24.23 points
- **MAE**: 17.78 points

### Trade #221 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-14 03:00:00
- **FVG 5m**: 22803.17 - 22815.55
- **Entrée**: 22819.67 @ 2025-02-14 03:04:00
- **Stop Loss**: 22791.77
- **Risk**: 27.90 points
- **TP 1RR**: 22847.57 ❌
- **TP 1.5RR**: 22861.51 ❌
- **TP 2RR**: 22875.46 ❌
- **TP 2.5RR**: 22889.41 ❌
- **TP 3RR**: 22903.36 ❌
- **TP 3.5RR**: 22917.31 ❌
- **TP 4RR**: 22931.26 ❌
- **TP 4.5RR**: 22945.21 ❌
- **TP 5RR**: 22959.15 ❌
- **PnL**: -27.90 points (-1.0R)
- **MFE**: 12.37 points
- **MAE**: 29.90 points

### Trade #222 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-14 06:00:00
- **FVG 5m**: 22736.68 - 22739.77
- **Entrée**: 22754.72 @ 2025-02-14 06:01:00
- **Stop Loss**: 22725.31
- **Risk**: 29.41 points
- **TP 1RR**: 22784.13 ✅
- **TP 1.5RR**: 22798.83 ✅
- **TP 2RR**: 22813.54 ✅
- **TP 2.5RR**: 22828.24 ✅
- **TP 3RR**: 22842.95 ✅
- **TP 3.5RR**: 22857.65 ✅
- **TP 4RR**: 22872.36 ✅
- **TP 4.5RR**: 22887.06 ✅
- **TP 5RR**: 22901.77 ✅
- **PnL**: 147.05 points (5.0R)
- **MFE**: 148.97 points
- **MAE**: 15.46 points

### Trade #223 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-14 07:30:00
- **FVG 5m**: 22736.68 - 22739.77
- **Entrée**: 22781.52 @ 2025-02-14 07:31:00
- **Stop Loss**: 22725.31
- **Risk**: 56.22 points
- **TP 1RR**: 22837.74 ✅
- **TP 1.5RR**: 22865.85 ✅
- **TP 2RR**: 22893.95 ✅
- **TP 2.5RR**: 22922.06 ✅
- **TP 3RR**: 22950.17 ✅
- **TP 3.5RR**: 22978.28 ✅
- **TP 4RR**: 23006.38 ✅
- **TP 4.5RR**: 23034.49 ❌
- **TP 5RR**: 23062.60 ❌
- **PnL**: -56.22 points (-1.0R)
- **MFE**: 229.39 points
- **MAE**: 59.02 points

### Trade #224 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-17 02:15:00
- **FVG 5m**: 22929.72 - 22932.30
- **Entrée**: 22926.89 @ 2025-02-17 02:28:00
- **Stop Loss**: 22943.77
- **Risk**: 16.88 points
- **TP 1RR**: 22910.01 ❌
- **TP 1.5RR**: 22901.57 ❌
- **TP 2RR**: 22893.13 ❌
- **TP 2.5RR**: 22884.69 ❌
- **TP 3RR**: 22876.25 ❌
- **TP 3.5RR**: 22867.81 ❌
- **TP 4RR**: 22859.37 ❌
- **TP 4.5RR**: 22850.94 ❌
- **TP 5RR**: 22842.50 ❌
- **PnL**: -16.88 points (-1.0R)
- **MFE**: 13.66 points
- **MAE**: 20.10 points

### Trade #225 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22968.64 @ 2025-02-18 08:27:00
- **Stop Loss**: 22994.57
- **Risk**: 25.93 points
- **TP 1RR**: 22942.72 ✅
- **TP 1.5RR**: 22929.76 ✅
- **TP 2RR**: 22916.79 ✅
- **TP 2.5RR**: 22903.83 ✅
- **TP 3RR**: 22890.87 ✅
- **TP 3.5RR**: 22877.91 ✅
- **TP 4RR**: 22864.94 ✅
- **TP 4.5RR**: 22851.98 ✅
- **TP 5RR**: 22839.02 ✅
- **PnL**: 129.63 points (5.0R)
- **MFE**: 131.71 points
- **MAE**: 0.00 points

### Trade #226 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22968.64 @ 2025-02-18 08:27:00
- **Stop Loss**: 22994.57
- **Risk**: 25.93 points
- **TP 1RR**: 22942.72 ✅
- **TP 1.5RR**: 22929.76 ✅
- **TP 2RR**: 22916.79 ✅
- **TP 2.5RR**: 22903.83 ✅
- **TP 3RR**: 22890.87 ✅
- **TP 3.5RR**: 22877.91 ✅
- **TP 4RR**: 22864.94 ✅
- **TP 4.5RR**: 22851.98 ✅
- **TP 5RR**: 22839.02 ✅
- **PnL**: 129.63 points (5.0R)
- **MFE**: 131.71 points
- **MAE**: 0.00 points

### Trade #227 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22968.64 @ 2025-02-18 08:27:00
- **Stop Loss**: 22994.57
- **Risk**: 25.93 points
- **TP 1RR**: 22942.72 ✅
- **TP 1.5RR**: 22929.76 ✅
- **TP 2RR**: 22916.79 ✅
- **TP 2.5RR**: 22903.83 ✅
- **TP 3RR**: 22890.87 ✅
- **TP 3.5RR**: 22877.91 ✅
- **TP 4RR**: 22864.94 ✅
- **TP 4.5RR**: 22851.98 ✅
- **TP 5RR**: 22839.02 ✅
- **PnL**: 129.63 points (5.0R)
- **MFE**: 131.71 points
- **MAE**: 0.00 points

### Trade #228 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22968.64 @ 2025-02-18 08:27:00
- **Stop Loss**: 22994.57
- **Risk**: 25.93 points
- **TP 1RR**: 22942.72 ✅
- **TP 1.5RR**: 22929.76 ✅
- **TP 2RR**: 22916.79 ✅
- **TP 2.5RR**: 22903.83 ✅
- **TP 3RR**: 22890.87 ✅
- **TP 3.5RR**: 22877.91 ✅
- **TP 4RR**: 22864.94 ✅
- **TP 4.5RR**: 22851.98 ✅
- **TP 5RR**: 22839.02 ✅
- **PnL**: 129.63 points (5.0R)
- **MFE**: 131.71 points
- **MAE**: 0.00 points

### Trade #229 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:30:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22921.22 @ 2025-02-18 08:31:00
- **Stop Loss**: 22994.57
- **Risk**: 73.35 points
- **TP 1RR**: 22847.87 ✅
- **TP 1.5RR**: 22811.19 ✅
- **TP 2RR**: 22774.52 ✅
- **TP 2.5RR**: 22737.85 ✅
- **TP 3RR**: 22701.17 ✅
- **TP 3.5RR**: 22664.50 ✅
- **TP 4RR**: 22627.82 ✅
- **TP 4.5RR**: 22591.15 ✅
- **TP 5RR**: 22554.47 ✅
- **PnL**: 366.75 points (5.0R)
- **MFE**: 371.15 points
- **MAE**: 69.07 points

### Trade #230 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22853.69 @ 2025-02-18 09:16:00
- **Stop Loss**: 22994.57
- **Risk**: 140.88 points
- **TP 1RR**: 22712.81 ✅
- **TP 1.5RR**: 22642.37 ✅
- **TP 2RR**: 22571.94 ✅
- **TP 2.5RR**: 22501.50 ✅
- **TP 3RR**: 22431.06 ✅
- **TP 3.5RR**: 22360.62 ✅
- **TP 4RR**: 22290.18 ✅
- **TP 4.5RR**: 22219.74 ✅
- **TP 5RR**: 22149.30 ✅
- **PnL**: 704.39 points (5.0R)
- **MFE**: 709.05 points
- **MAE**: 136.60 points

### Trade #231 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22853.69 @ 2025-02-18 09:16:00
- **Stop Loss**: 22994.57
- **Risk**: 140.88 points
- **TP 1RR**: 22712.81 ✅
- **TP 1.5RR**: 22642.37 ✅
- **TP 2RR**: 22571.94 ✅
- **TP 2.5RR**: 22501.50 ✅
- **TP 3RR**: 22431.06 ✅
- **TP 3.5RR**: 22360.62 ✅
- **TP 4RR**: 22290.18 ✅
- **TP 4.5RR**: 22219.74 ✅
- **TP 5RR**: 22149.30 ✅
- **PnL**: 704.39 points (5.0R)
- **MFE**: 709.05 points
- **MAE**: 136.60 points

### Trade #232 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22853.69 @ 2025-02-18 09:16:00
- **Stop Loss**: 22994.57
- **Risk**: 140.88 points
- **TP 1RR**: 22712.81 ✅
- **TP 1.5RR**: 22642.37 ✅
- **TP 2RR**: 22571.94 ✅
- **TP 2.5RR**: 22501.50 ✅
- **TP 3RR**: 22431.06 ✅
- **TP 3.5RR**: 22360.62 ✅
- **TP 4RR**: 22290.18 ✅
- **TP 4.5RR**: 22219.74 ✅
- **TP 5RR**: 22149.30 ✅
- **PnL**: 704.39 points (5.0R)
- **MFE**: 709.05 points
- **MAE**: 136.60 points

### Trade #233 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22853.69 @ 2025-02-18 09:16:00
- **Stop Loss**: 22994.57
- **Risk**: 140.88 points
- **TP 1RR**: 22712.81 ✅
- **TP 1.5RR**: 22642.37 ✅
- **TP 2RR**: 22571.94 ✅
- **TP 2.5RR**: 22501.50 ✅
- **TP 3RR**: 22431.06 ✅
- **TP 3.5RR**: 22360.62 ✅
- **TP 4RR**: 22290.18 ✅
- **TP 4.5RR**: 22219.74 ✅
- **TP 5RR**: 22149.30 ✅
- **PnL**: 704.39 points (5.0R)
- **MFE**: 709.05 points
- **MAE**: 136.60 points

### Trade #234 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22971.22 - 22983.08
- **Entrée**: 22853.69 @ 2025-02-18 09:16:00
- **Stop Loss**: 22994.57
- **Risk**: 140.88 points
- **TP 1RR**: 22712.81 ✅
- **TP 1.5RR**: 22642.37 ✅
- **TP 2RR**: 22571.94 ✅
- **TP 2.5RR**: 22501.50 ✅
- **TP 3RR**: 22431.06 ✅
- **TP 3.5RR**: 22360.62 ✅
- **TP 4RR**: 22290.18 ✅
- **TP 4.5RR**: 22219.74 ✅
- **TP 5RR**: 22149.30 ✅
- **PnL**: 704.39 points (5.0R)
- **MFE**: 709.05 points
- **MAE**: 136.60 points

### Trade #235 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 13:15:00
- **FVG 5m**: 22819.41 - 22840.80
- **Entrée**: 22841.32 @ 2025-02-18 13:24:00
- **Stop Loss**: 22808.00
- **Risk**: 33.32 points
- **TP 1RR**: 22874.64 ✅
- **TP 1.5RR**: 22891.30 ✅
- **TP 2RR**: 22907.95 ✅
- **TP 2.5RR**: 22924.61 ✅
- **TP 3RR**: 22941.27 ✅
- **TP 3.5RR**: 22957.93 ✅
- **TP 4RR**: 22974.59 ✅
- **TP 4.5RR**: 22991.25 ❌
- **TP 5RR**: 23007.91 ❌
- **PnL**: -33.32 points (-1.0R)
- **MFE**: 140.21 points
- **MAE**: 34.28 points

### Trade #236 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 14:45:00
- **FVG 5m**: 22819.41 - 22840.80
- **Entrée**: 22852.40 @ 2025-02-18 14:46:00
- **Stop Loss**: 22808.00
- **Risk**: 44.40 points
- **TP 1RR**: 22896.80 ✅
- **TP 1.5RR**: 22919.00 ✅
- **TP 2RR**: 22941.20 ✅
- **TP 2.5RR**: 22963.40 ✅
- **TP 3RR**: 22985.60 ❌
- **TP 3.5RR**: 23007.80 ❌
- **TP 4RR**: 23030.00 ❌
- **TP 4.5RR**: 23052.21 ❌
- **TP 5RR**: 23074.41 ❌
- **PnL**: -44.40 points (-1.0R)
- **MFE**: 129.13 points
- **MAE**: 45.36 points

### Trade #237 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 14:45:00
- **FVG 5m**: 22819.41 - 22840.80
- **Entrée**: 22852.40 @ 2025-02-18 14:46:00
- **Stop Loss**: 22808.00
- **Risk**: 44.40 points
- **TP 1RR**: 22896.80 ✅
- **TP 1.5RR**: 22919.00 ✅
- **TP 2RR**: 22941.20 ✅
- **TP 2.5RR**: 22963.40 ✅
- **TP 3RR**: 22985.60 ❌
- **TP 3.5RR**: 23007.80 ❌
- **TP 4RR**: 23030.00 ❌
- **TP 4.5RR**: 23052.21 ❌
- **TP 5RR**: 23074.41 ❌
- **PnL**: -44.40 points (-1.0R)
- **MFE**: 129.13 points
- **MAE**: 45.36 points

### Trade #238 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 02:30:00
- **FVG 5m**: 22946.22 - 22954.21
- **Entrée**: 22956.79 @ 2025-02-19 02:32:00
- **Stop Loss**: 22934.75
- **Risk**: 22.04 points
- **TP 1RR**: 22978.83 ❌
- **TP 1.5RR**: 22989.85 ❌
- **TP 2RR**: 23000.87 ❌
- **TP 2.5RR**: 23011.89 ❌
- **TP 3RR**: 23022.91 ❌
- **TP 3.5RR**: 23033.93 ❌
- **TP 4RR**: 23044.95 ❌
- **TP 4.5RR**: 23055.97 ❌
- **TP 5RR**: 23066.99 ❌
- **PnL**: -22.04 points (-1.0R)
- **MFE**: 8.76 points
- **MAE**: 25.26 points

### Trade #239 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 12:00:00
- **FVG 5m**: 22925.86 - 22932.82
- **Entrée**: 22919.16 @ 2025-02-19 12:02:00
- **Stop Loss**: 22944.28
- **Risk**: 25.13 points
- **TP 1RR**: 22894.03 ✅
- **TP 1.5RR**: 22881.47 ❌
- **TP 2RR**: 22868.90 ❌
- **TP 2.5RR**: 22856.34 ❌
- **TP 3RR**: 22843.78 ❌
- **TP 3.5RR**: 22831.21 ❌
- **TP 4RR**: 22818.65 ❌
- **TP 4.5RR**: 22806.09 ❌
- **TP 5RR**: 22793.52 ❌
- **PnL**: -25.13 points (-1.0R)
- **MFE**: 36.86 points
- **MAE**: 29.38 points

### Trade #240 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.40 - 22938.75
- **Entrée**: 22939.52 @ 2025-02-19 13:13:00
- **Stop Loss**: 22923.93
- **Risk**: 15.59 points
- **TP 1RR**: 22955.11 ✅
- **TP 1.5RR**: 22962.91 ✅
- **TP 2RR**: 22970.70 ✅
- **TP 2.5RR**: 22978.50 ✅
- **TP 3RR**: 22986.29 ✅
- **TP 3.5RR**: 22994.09 ❌
- **TP 4RR**: 23001.89 ❌
- **TP 4.5RR**: 23009.68 ❌
- **TP 5RR**: 23017.48 ❌
- **PnL**: -15.59 points (-1.0R)
- **MFE**: 50.78 points
- **MAE**: 23.71 points

### Trade #241 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.40 - 22938.75
- **Entrée**: 22939.52 @ 2025-02-19 13:13:00
- **Stop Loss**: 22923.93
- **Risk**: 15.59 points
- **TP 1RR**: 22955.11 ✅
- **TP 1.5RR**: 22962.91 ✅
- **TP 2RR**: 22970.70 ✅
- **TP 2.5RR**: 22978.50 ✅
- **TP 3RR**: 22986.29 ✅
- **TP 3.5RR**: 22994.09 ❌
- **TP 4RR**: 23001.89 ❌
- **TP 4.5RR**: 23009.68 ❌
- **TP 5RR**: 23017.48 ❌
- **PnL**: -15.59 points (-1.0R)
- **MFE**: 50.78 points
- **MAE**: 23.71 points

### Trade #242 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.40 - 22938.75
- **Entrée**: 22939.52 @ 2025-02-19 13:13:00
- **Stop Loss**: 22923.93
- **Risk**: 15.59 points
- **TP 1RR**: 22955.11 ✅
- **TP 1.5RR**: 22962.91 ✅
- **TP 2RR**: 22970.70 ✅
- **TP 2.5RR**: 22978.50 ✅
- **TP 3RR**: 22986.29 ✅
- **TP 3.5RR**: 22994.09 ❌
- **TP 4RR**: 23001.89 ❌
- **TP 4.5RR**: 23009.68 ❌
- **TP 5RR**: 23017.48 ❌
- **PnL**: -15.59 points (-1.0R)
- **MFE**: 50.78 points
- **MAE**: 23.71 points

### Trade #243 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.40 - 22938.75
- **Entrée**: 22939.52 @ 2025-02-19 13:13:00
- **Stop Loss**: 22923.93
- **Risk**: 15.59 points
- **TP 1RR**: 22955.11 ✅
- **TP 1.5RR**: 22962.91 ✅
- **TP 2RR**: 22970.70 ✅
- **TP 2.5RR**: 22978.50 ✅
- **TP 3RR**: 22986.29 ✅
- **TP 3.5RR**: 22994.09 ❌
- **TP 4RR**: 23001.89 ❌
- **TP 4.5RR**: 23009.68 ❌
- **TP 5RR**: 23017.48 ❌
- **PnL**: -15.59 points (-1.0R)
- **MFE**: 50.78 points
- **MAE**: 23.71 points

### Trade #244 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.40 - 22938.75
- **Entrée**: 22939.52 @ 2025-02-19 13:13:00
- **Stop Loss**: 22923.93
- **Risk**: 15.59 points
- **TP 1RR**: 22955.11 ✅
- **TP 1.5RR**: 22962.91 ✅
- **TP 2RR**: 22970.70 ✅
- **TP 2.5RR**: 22978.50 ✅
- **TP 3RR**: 22986.29 ✅
- **TP 3.5RR**: 22994.09 ❌
- **TP 4RR**: 23001.89 ❌
- **TP 4.5RR**: 23009.68 ❌
- **TP 5RR**: 23017.48 ❌
- **PnL**: -15.59 points (-1.0R)
- **MFE**: 50.78 points
- **MAE**: 23.71 points

### Trade #245 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.40 - 22938.75
- **Entrée**: 22939.52 @ 2025-02-19 13:13:00
- **Stop Loss**: 22923.93
- **Risk**: 15.59 points
- **TP 1RR**: 22955.11 ✅
- **TP 1.5RR**: 22962.91 ✅
- **TP 2RR**: 22970.70 ✅
- **TP 2.5RR**: 22978.50 ✅
- **TP 3RR**: 22986.29 ✅
- **TP 3.5RR**: 22994.09 ❌
- **TP 4RR**: 23001.89 ❌
- **TP 4.5RR**: 23009.68 ❌
- **TP 5RR**: 23017.48 ❌
- **PnL**: -15.59 points (-1.0R)
- **MFE**: 50.78 points
- **MAE**: 23.71 points

### Trade #246 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 14:00:00
- **FVG 5m**: 22976.38 - 22982.56
- **Entrée**: 22970.71 @ 2025-02-19 14:02:00
- **Stop Loss**: 22994.05
- **Risk**: 23.35 points
- **TP 1RR**: 22947.36 ✅
- **TP 1.5RR**: 22935.68 ✅
- **TP 2RR**: 22924.01 ✅
- **TP 2.5RR**: 22912.34 ✅
- **TP 3RR**: 22900.66 ✅
- **TP 3.5RR**: 22888.99 ✅
- **TP 4RR**: 22877.32 ✅
- **TP 4.5RR**: 22865.64 ✅
- **TP 5RR**: 22853.97 ✅
- **PnL**: 116.74 points (5.0R)
- **MFE**: 122.69 points
- **MAE**: 4.90 points

### Trade #247 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 14:15:00
- **FVG 5m**: 22976.38 - 22982.56
- **Entrée**: 22964.26 @ 2025-02-19 14:16:00
- **Stop Loss**: 22994.05
- **Risk**: 29.79 points
- **TP 1RR**: 22934.47 ✅
- **TP 1.5RR**: 22919.58 ✅
- **TP 2RR**: 22904.68 ✅
- **TP 2.5RR**: 22889.78 ✅
- **TP 3RR**: 22874.89 ✅
- **TP 3.5RR**: 22859.99 ✅
- **TP 4RR**: 22845.10 ✅
- **TP 4.5RR**: 22830.20 ✅
- **TP 5RR**: 22815.31 ✅
- **PnL**: 148.95 points (5.0R)
- **MFE**: 150.01 points
- **MAE**: 9.02 points

### Trade #248 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 01:15:00
- **FVG 5m**: 22837.45 - 22843.64
- **Entrée**: 22844.41 @ 2025-02-20 01:16:00
- **Stop Loss**: 22826.03
- **Risk**: 18.38 points
- **TP 1RR**: 22862.79 ✅
- **TP 1.5RR**: 22871.98 ✅
- **TP 2RR**: 22881.17 ✅
- **TP 2.5RR**: 22890.36 ✅
- **TP 3RR**: 22899.55 ✅
- **TP 3.5RR**: 22908.73 ✅
- **TP 4RR**: 22917.92 ❌
- **TP 4.5RR**: 22927.11 ❌
- **TP 5RR**: 22936.30 ❌
- **PnL**: -18.38 points (-1.0R)
- **MFE**: 69.33 points
- **MAE**: 20.10 points

### Trade #249 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-20 05:45:00
- **FVG 5m**: 22883.33 - 22891.32
- **Entrée**: 22874.57 @ 2025-02-20 05:46:00
- **Stop Loss**: 22902.77
- **Risk**: 28.20 points
- **TP 1RR**: 22846.37 ❌
- **TP 1.5RR**: 22832.27 ❌
- **TP 2RR**: 22818.17 ❌
- **TP 2.5RR**: 22804.07 ❌
- **TP 3RR**: 22789.97 ❌
- **TP 3.5RR**: 22775.87 ❌
- **TP 4RR**: 22761.77 ❌
- **TP 4.5RR**: 22747.67 ❌
- **TP 5RR**: 22733.57 ❌
- **PnL**: -28.20 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 29.90 points

### Trade #250 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 06:45:00
- **FVG 5m**: 22871.48 - 22877.40
- **Entrée**: 22888.49 @ 2025-02-20 06:46:00
- **Stop Loss**: 22860.04
- **Risk**: 28.45 points
- **TP 1RR**: 22916.93 ❌
- **TP 1.5RR**: 22931.16 ❌
- **TP 2RR**: 22945.38 ❌
- **TP 2.5RR**: 22959.60 ❌
- **TP 3RR**: 22973.83 ❌
- **TP 3.5RR**: 22988.05 ❌
- **TP 4RR**: 23002.27 ❌
- **TP 4.5RR**: 23016.50 ❌
- **TP 5RR**: 23030.72 ❌
- **PnL**: -28.45 points (-1.0R)
- **MFE**: 25.26 points
- **MAE**: 30.16 points

### Trade #251 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-20 08:45:00
- **FVG 5m**: 22892.35 - 22898.28
- **Entrée**: 22846.22 @ 2025-02-20 08:46:00
- **Stop Loss**: 22909.73
- **Risk**: 63.51 points
- **TP 1RR**: 22782.70 ✅
- **TP 1.5RR**: 22750.95 ✅
- **TP 2RR**: 22719.19 ✅
- **TP 2.5RR**: 22687.43 ✅
- **TP 3RR**: 22655.68 ✅
- **TP 3.5RR**: 22623.92 ❌
- **TP 4RR**: 22592.16 ❌
- **TP 4.5RR**: 22560.41 ❌
- **TP 5RR**: 22528.65 ❌
- **PnL**: -63.51 points (-1.0R)
- **MFE**: 215.47 points
- **MAE**: 67.27 points

### Trade #252 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 10:00:00
- **FVG 5m**: 22710.39 - 22736.42
- **Entrée**: 22736.68 @ 2025-02-20 10:09:00
- **Stop Loss**: 22699.03
- **Risk**: 37.64 points
- **TP 1RR**: 22774.32 ❌
- **TP 1.5RR**: 22793.14 ❌
- **TP 2RR**: 22811.97 ❌
- **TP 2.5RR**: 22830.79 ❌
- **TP 3RR**: 22849.61 ❌
- **TP 3.5RR**: 22868.43 ❌
- **TP 4RR**: 22887.26 ❌
- **TP 4.5RR**: 22906.08 ❌
- **TP 5RR**: 22924.90 ❌
- **PnL**: -37.64 points (-1.0R)
- **MFE**: 23.45 points
- **MAE**: 38.92 points

### Trade #253 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 11:30:00
- **FVG 5m**: 22710.39 - 22736.42
- **Entrée**: 22768.38 @ 2025-02-20 11:31:00
- **Stop Loss**: 22699.03
- **Risk**: 69.35 points
- **TP 1RR**: 22837.73 ✅
- **TP 1.5RR**: 22872.40 ✅
- **TP 2RR**: 22907.07 ✅
- **TP 2.5RR**: 22941.75 ❌
- **TP 3RR**: 22976.42 ❌
- **TP 3.5RR**: 23011.09 ❌
- **TP 4RR**: 23045.77 ❌
- **TP 4.5RR**: 23080.44 ❌
- **TP 5RR**: 23115.11 ❌
- **PnL**: -69.35 points (-1.0R)
- **MFE**: 165.99 points
- **MAE**: 71.65 points

### Trade #254 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 13:45:00
- **FVG 5m**: 22764.25 - 22774.31
- **Entrée**: 22775.85 @ 2025-02-20 13:46:00
- **Stop Loss**: 22752.87
- **Risk**: 22.98 points
- **TP 1RR**: 22798.83 ✅
- **TP 1.5RR**: 22810.32 ✅
- **TP 2RR**: 22821.81 ✅
- **TP 2.5RR**: 22833.30 ✅
- **TP 3RR**: 22844.79 ✅
- **TP 3.5RR**: 22856.28 ✅
- **TP 4RR**: 22867.77 ✅
- **TP 4.5RR**: 22879.27 ✅
- **TP 5RR**: 22890.76 ✅
- **PnL**: 114.90 points (5.0R)
- **MFE**: 121.40 points
- **MAE**: 7.47 points

### Trade #255 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 14:45:00
- **FVG 5m**: 22764.25 - 22774.31
- **Entrée**: 22807.81 @ 2025-02-20 14:46:00
- **Stop Loss**: 22752.87
- **Risk**: 54.94 points
- **TP 1RR**: 22862.75 ✅
- **TP 1.5RR**: 22890.22 ✅
- **TP 2RR**: 22917.69 ✅
- **TP 2.5RR**: 22945.16 ❌
- **TP 3RR**: 22972.63 ❌
- **TP 3.5RR**: 23000.10 ❌
- **TP 4RR**: 23027.57 ❌
- **TP 4.5RR**: 23055.04 ❌
- **TP 5RR**: 23082.52 ❌
- **PnL**: -54.94 points (-1.0R)
- **MFE**: 126.55 points
- **MAE**: 78.10 points

### Trade #256 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 07:45:00
- **FVG 5m**: 22896.73 - 22900.34
- **Entrée**: 22891.58 @ 2025-02-21 08:27:00
- **Stop Loss**: 22911.79
- **Risk**: 20.21 points
- **TP 1RR**: 22871.37 ✅
- **TP 1.5RR**: 22861.26 ✅
- **TP 2RR**: 22851.15 ✅
- **TP 2.5RR**: 22841.05 ✅
- **TP 3RR**: 22830.94 ✅
- **TP 3.5RR**: 22820.83 ✅
- **TP 4RR**: 22810.73 ✅
- **TP 4.5RR**: 22800.62 ✅
- **TP 5RR**: 22790.51 ✅
- **PnL**: 101.07 points (5.0R)
- **MFE**: 109.54 points
- **MAE**: 4.12 points

### Trade #257 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 07:45:00
- **FVG 5m**: 22896.73 - 22900.34
- **Entrée**: 22891.58 @ 2025-02-21 08:27:00
- **Stop Loss**: 22911.79
- **Risk**: 20.21 points
- **TP 1RR**: 22871.37 ✅
- **TP 1.5RR**: 22861.26 ✅
- **TP 2RR**: 22851.15 ✅
- **TP 2.5RR**: 22841.05 ✅
- **TP 3RR**: 22830.94 ✅
- **TP 3.5RR**: 22820.83 ✅
- **TP 4RR**: 22810.73 ✅
- **TP 4.5RR**: 22800.62 ✅
- **TP 5RR**: 22790.51 ✅
- **PnL**: 101.07 points (5.0R)
- **MFE**: 109.54 points
- **MAE**: 4.12 points

### Trade #258 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:15:00
- **FVG 5m**: 22912.97 - 22922.25
- **Entrée**: 22911.94 @ 2025-02-21 08:19:00
- **Stop Loss**: 22933.71
- **Risk**: 21.77 points
- **TP 1RR**: 22890.17 ✅
- **TP 1.5RR**: 22879.28 ✅
- **TP 2RR**: 22868.40 ✅
- **TP 2.5RR**: 22857.51 ✅
- **TP 3RR**: 22846.63 ✅
- **TP 3.5RR**: 22835.74 ✅
- **TP 4RR**: 22824.86 ✅
- **TP 4.5RR**: 22813.97 ✅
- **TP 5RR**: 22803.09 ✅
- **PnL**: 108.85 points (5.0R)
- **MFE**: 115.47 points
- **MAE**: 3.87 points

### Trade #259 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:30:00
- **FVG 5m**: 22912.97 - 22922.25
- **Entrée**: 22824.82 @ 2025-02-21 08:31:00
- **Stop Loss**: 22933.71
- **Risk**: 108.89 points
- **TP 1RR**: 22715.94 ✅
- **TP 1.5RR**: 22661.49 ✅
- **TP 2RR**: 22607.05 ✅
- **TP 2.5RR**: 22552.61 ✅
- **TP 3RR**: 22498.16 ✅
- **TP 3.5RR**: 22443.72 ✅
- **TP 4RR**: 22389.27 ✅
- **TP 4.5RR**: 22334.83 ✅
- **TP 5RR**: 22280.39 ✅
- **PnL**: 544.44 points (5.0R)
- **MFE**: 550.79 points
- **MAE**: 37.89 points

### Trade #260 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:30:00
- **FVG 5m**: 22912.97 - 22922.25
- **Entrée**: 22824.82 @ 2025-02-21 08:31:00
- **Stop Loss**: 22933.71
- **Risk**: 108.89 points
- **TP 1RR**: 22715.94 ✅
- **TP 1.5RR**: 22661.49 ✅
- **TP 2RR**: 22607.05 ✅
- **TP 2.5RR**: 22552.61 ✅
- **TP 3RR**: 22498.16 ✅
- **TP 3.5RR**: 22443.72 ✅
- **TP 4RR**: 22389.27 ✅
- **TP 4.5RR**: 22334.83 ✅
- **TP 5RR**: 22280.39 ✅
- **PnL**: 544.44 points (5.0R)
- **MFE**: 550.79 points
- **MAE**: 37.89 points

### Trade #261 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:30:00
- **FVG 5m**: 22912.97 - 22922.25
- **Entrée**: 22824.82 @ 2025-02-21 08:31:00
- **Stop Loss**: 22933.71
- **Risk**: 108.89 points
- **TP 1RR**: 22715.94 ✅
- **TP 1.5RR**: 22661.49 ✅
- **TP 2RR**: 22607.05 ✅
- **TP 2.5RR**: 22552.61 ✅
- **TP 3RR**: 22498.16 ✅
- **TP 3.5RR**: 22443.72 ✅
- **TP 4RR**: 22389.27 ✅
- **TP 4.5RR**: 22334.83 ✅
- **TP 5RR**: 22280.39 ✅
- **PnL**: 544.44 points (5.0R)
- **MFE**: 550.79 points
- **MAE**: 37.89 points

### Trade #262 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 12:30:00
- **FVG 5m**: 22488.99 - 22493.37
- **Entrée**: 22515.79 @ 2025-02-21 12:37:00
- **Stop Loss**: 22477.74
- **Risk**: 38.05 points
- **TP 1RR**: 22553.84 ❌
- **TP 1.5RR**: 22572.87 ❌
- **TP 2RR**: 22591.89 ❌
- **TP 2.5RR**: 22610.92 ❌
- **TP 3RR**: 22629.94 ❌
- **TP 3.5RR**: 22648.97 ❌
- **TP 4RR**: 22667.99 ❌
- **TP 4.5RR**: 22687.01 ❌
- **TP 5RR**: 22706.04 ❌
- **PnL**: -38.05 points (-1.0R)
- **MFE**: 10.57 points
- **MAE**: 46.65 points

### Trade #263 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 12:30:00
- **FVG 5m**: 22488.99 - 22493.37
- **Entrée**: 22515.79 @ 2025-02-21 12:37:00
- **Stop Loss**: 22477.74
- **Risk**: 38.05 points
- **TP 1RR**: 22553.84 ❌
- **TP 1.5RR**: 22572.87 ❌
- **TP 2RR**: 22591.89 ❌
- **TP 2.5RR**: 22610.92 ❌
- **TP 3RR**: 22629.94 ❌
- **TP 3.5RR**: 22648.97 ❌
- **TP 4RR**: 22667.99 ❌
- **TP 4.5RR**: 22687.01 ❌
- **TP 5RR**: 22706.04 ❌
- **PnL**: -38.05 points (-1.0R)
- **MFE**: 10.57 points
- **MAE**: 46.65 points

### Trade #264 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-23 19:30:00
- **FVG 5m**: 22434.09 - 22438.21
- **Entrée**: 22438.47 @ 2025-02-23 20:10:00
- **Stop Loss**: 22422.87
- **Risk**: 15.60 points
- **TP 1RR**: 22454.07 ✅
- **TP 1.5RR**: 22461.87 ✅
- **TP 2RR**: 22469.67 ✅
- **TP 2.5RR**: 22477.47 ❌
- **TP 3RR**: 22485.27 ❌
- **TP 3.5RR**: 22493.06 ❌
- **TP 4RR**: 22500.86 ❌
- **TP 4.5RR**: 22508.66 ❌
- **TP 5RR**: 22516.46 ❌
- **PnL**: -15.60 points (-1.0R)
- **MFE**: 38.15 points
- **MAE**: 15.72 points

### Trade #265 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 02:15:00
- **FVG 5m**: 22400.07 - 22422.49
- **Entrée**: 22426.61 @ 2025-02-24 02:45:00
- **Stop Loss**: 22388.87
- **Risk**: 37.75 points
- **TP 1RR**: 22464.36 ✅
- **TP 1.5RR**: 22483.23 ✅
- **TP 2RR**: 22502.11 ❌
- **TP 2.5RR**: 22520.98 ❌
- **TP 3RR**: 22539.86 ❌
- **TP 3.5RR**: 22558.73 ❌
- **TP 4RR**: 22577.60 ❌
- **TP 4.5RR**: 22596.48 ❌
- **TP 5RR**: 22615.35 ❌
- **PnL**: -37.75 points (-1.0R)
- **MFE**: 61.86 points
- **MAE**: 55.93 points

### Trade #266 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 02:45:00
- **FVG 5m**: 22400.07 - 22422.49
- **Entrée**: 22438.21 @ 2025-02-24 02:46:00
- **Stop Loss**: 22388.87
- **Risk**: 49.35 points
- **TP 1RR**: 22487.56 ✅
- **TP 1.5RR**: 22512.23 ❌
- **TP 2RR**: 22536.90 ❌
- **TP 2.5RR**: 22561.58 ❌
- **TP 3RR**: 22586.25 ❌
- **TP 3.5RR**: 22610.92 ❌
- **TP 4RR**: 22635.59 ❌
- **TP 4.5RR**: 22660.27 ❌
- **TP 5RR**: 22684.94 ❌
- **PnL**: -49.35 points (-1.0R)
- **MFE**: 50.26 points
- **MAE**: 67.53 points

### Trade #267 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 02:45:00
- **FVG 5m**: 22400.07 - 22422.49
- **Entrée**: 22438.21 @ 2025-02-24 02:46:00
- **Stop Loss**: 22388.87
- **Risk**: 49.35 points
- **TP 1RR**: 22487.56 ✅
- **TP 1.5RR**: 22512.23 ❌
- **TP 2RR**: 22536.90 ❌
- **TP 2.5RR**: 22561.58 ❌
- **TP 3RR**: 22586.25 ❌
- **TP 3.5RR**: 22610.92 ❌
- **TP 4RR**: 22635.59 ❌
- **TP 4.5RR**: 22660.27 ❌
- **TP 5RR**: 22684.94 ❌
- **PnL**: -49.35 points (-1.0R)
- **MFE**: 50.26 points
- **MAE**: 67.53 points

### Trade #268 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-24 03:30:00
- **FVG 5m**: 22453.42 - 22457.03
- **Entrée**: 22452.64 @ 2025-02-24 03:56:00
- **Stop Loss**: 22468.26
- **Risk**: 15.61 points
- **TP 1RR**: 22437.03 ✅
- **TP 1.5RR**: 22429.23 ✅
- **TP 2RR**: 22421.42 ✅
- **TP 2.5RR**: 22413.62 ✅
- **TP 3RR**: 22405.81 ❌
- **TP 3.5RR**: 22398.01 ❌
- **TP 4RR**: 22390.20 ❌
- **TP 4.5RR**: 22382.40 ❌
- **TP 5RR**: 22374.59 ❌
- **PnL**: -15.61 points (-1.0R)
- **MFE**: 39.95 points
- **MAE**: 18.56 points

### Trade #269 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-24 08:00:00
- **FVG 5m**: 22437.95 - 22440.79
- **Entrée**: 22437.18 @ 2025-02-24 08:21:00
- **Stop Loss**: 22452.01
- **Risk**: 14.83 points
- **TP 1RR**: 22422.35 ✅
- **TP 1.5RR**: 22414.94 ✅
- **TP 2RR**: 22407.52 ✅
- **TP 2.5RR**: 22400.11 ❌
- **TP 3RR**: 22392.69 ❌
- **TP 3.5RR**: 22385.28 ❌
- **TP 4RR**: 22377.87 ❌
- **TP 4.5RR**: 22370.45 ❌
- **TP 5RR**: 22363.04 ❌
- **PnL**: -14.83 points (-1.0R)
- **MFE**: 33.25 points
- **MAE**: 39.69 points

### Trade #270 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 08:30:00
- **FVG 5m**: 22434.86 - 22438.21
- **Entrée**: 22455.22 @ 2025-02-24 08:32:00
- **Stop Loss**: 22423.64
- **Risk**: 31.58 points
- **TP 1RR**: 22486.80 ❌
- **TP 1.5RR**: 22502.59 ❌
- **TP 2RR**: 22518.38 ❌
- **TP 2.5RR**: 22534.17 ❌
- **TP 3RR**: 22549.96 ❌
- **TP 3.5RR**: 22565.75 ❌
- **TP 4RR**: 22581.54 ❌
- **TP 4.5RR**: 22597.33 ❌
- **TP 5RR**: 22613.12 ❌
- **PnL**: -31.58 points (-1.0R)
- **MFE**: 0.77 points
- **MAE**: 43.82 points

### Trade #271 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 18:00:00
- **FVG 5m**: 22052.63 - 22060.10
- **Entrée**: 22066.29 @ 2025-02-24 18:02:00
- **Stop Loss**: 22041.60
- **Risk**: 24.69 points
- **TP 1RR**: 22090.98 ✅
- **TP 1.5RR**: 22103.32 ✅
- **TP 2RR**: 22115.66 ✅
- **TP 2.5RR**: 22128.01 ❌
- **TP 3RR**: 22140.35 ❌
- **TP 3.5RR**: 22152.69 ❌
- **TP 4RR**: 22165.04 ❌
- **TP 4.5RR**: 22177.38 ❌
- **TP 5RR**: 22189.72 ❌
- **PnL**: -24.69 points (-1.0R)
- **MFE**: 51.81 points
- **MAE**: 27.06 points

### Trade #272 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 18:00:00
- **FVG 5m**: 22052.63 - 22060.10
- **Entrée**: 22066.29 @ 2025-02-24 18:02:00
- **Stop Loss**: 22041.60
- **Risk**: 24.69 points
- **TP 1RR**: 22090.98 ✅
- **TP 1.5RR**: 22103.32 ✅
- **TP 2RR**: 22115.66 ✅
- **TP 2.5RR**: 22128.01 ❌
- **TP 3RR**: 22140.35 ❌
- **TP 3.5RR**: 22152.69 ❌
- **TP 4RR**: 22165.04 ❌
- **TP 4.5RR**: 22177.38 ❌
- **TP 5RR**: 22189.72 ❌
- **PnL**: -24.69 points (-1.0R)
- **MFE**: 51.81 points
- **MAE**: 27.06 points

### Trade #273 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 05:00:00
- **FVG 5m**: 21971.18 - 21975.05
- **Entrée**: 21979.17 @ 2025-02-25 05:03:00
- **Stop Loss**: 21960.20
- **Risk**: 18.98 points
- **TP 1RR**: 21998.15 ✅
- **TP 1.5RR**: 22007.64 ✅
- **TP 2RR**: 22017.12 ✅
- **TP 2.5RR**: 22026.61 ✅
- **TP 3RR**: 22036.10 ✅
- **TP 3.5RR**: 22045.59 ✅
- **TP 4RR**: 22055.08 ✅
- **TP 4.5RR**: 22064.56 ✅
- **TP 5RR**: 22074.05 ✅
- **PnL**: 94.88 points (5.0R)
- **MFE**: 100.52 points
- **MAE**: 16.75 points

### Trade #274 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 06:45:00
- **FVG 5m**: 21971.18 - 21975.05
- **Entrée**: 22029.69 @ 2025-02-25 06:46:00
- **Stop Loss**: 21960.20
- **Risk**: 69.49 points
- **TP 1RR**: 22099.18 ✅
- **TP 1.5RR**: 22133.93 ❌
- **TP 2RR**: 22168.68 ❌
- **TP 2.5RR**: 22203.42 ❌
- **TP 3RR**: 22238.17 ❌
- **TP 3.5RR**: 22272.92 ❌
- **TP 4RR**: 22307.66 ❌
- **TP 4.5RR**: 22342.41 ❌
- **TP 5RR**: 22377.16 ❌
- **PnL**: -69.49 points (-1.0R)
- **MFE**: 86.34 points
- **MAE**: 84.02 points

### Trade #275 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 10:45:00
- **FVG 5m**: 21759.84 - 21789.73
- **Entrée**: 21813.96 @ 2025-02-25 10:56:00
- **Stop Loss**: 21748.96
- **Risk**: 65.01 points
- **TP 1RR**: 21878.97 ✅
- **TP 1.5RR**: 21911.47 ✅
- **TP 2RR**: 21943.97 ✅
- **TP 2.5RR**: 21976.48 ✅
- **TP 3RR**: 22008.98 ✅
- **TP 3.5RR**: 22041.48 ✅
- **TP 4RR**: 22073.98 ❌
- **TP 4.5RR**: 22106.49 ❌
- **TP 5RR**: 22138.99 ❌
- **PnL**: -65.01 points (-1.0R)
- **MFE**: 258.26 points
- **MAE**: 77.32 points

### Trade #276 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 02:00:00
- **FVG 5m**: 21941.03 - 21944.89
- **Entrée**: 21940.25 @ 2025-02-26 02:05:00
- **Stop Loss**: 21955.87
- **Risk**: 15.61 points
- **TP 1RR**: 21924.64 ✅
- **TP 1.5RR**: 21916.84 ❌
- **TP 2RR**: 21909.03 ❌
- **TP 2.5RR**: 21901.23 ❌
- **TP 3RR**: 21893.42 ❌
- **TP 3.5RR**: 21885.61 ❌
- **TP 4RR**: 21877.81 ❌
- **TP 4.5RR**: 21870.00 ❌
- **TP 5RR**: 21862.20 ❌
- **PnL**: -15.61 points (-1.0R)
- **MFE**: 18.56 points
- **MAE**: 15.98 points

### Trade #277 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 05:45:00
- **FVG 5m**: 21967.32 - 21975.82
- **Entrée**: 21962.42 @ 2025-02-26 05:51:00
- **Stop Loss**: 21986.81
- **Risk**: 24.39 points
- **TP 1RR**: 21938.03 ✅
- **TP 1.5RR**: 21925.83 ✅
- **TP 2RR**: 21913.64 ❌
- **TP 2.5RR**: 21901.44 ❌
- **TP 3RR**: 21889.25 ❌
- **TP 3.5RR**: 21877.05 ❌
- **TP 4RR**: 21864.86 ❌
- **TP 4.5RR**: 21852.66 ❌
- **TP 5RR**: 21840.47 ❌
- **PnL**: -24.39 points (-1.0R)
- **MFE**: 44.59 points
- **MAE**: 26.03 points

### Trade #278 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:00:00
- **FVG 5m**: 21961.90 - 21969.12
- **Entrée**: 21938.71 @ 2025-02-26 08:01:00
- **Stop Loss**: 21980.11
- **Risk**: 41.40 points
- **TP 1RR**: 21897.31 ✅
- **TP 1.5RR**: 21876.61 ✅
- **TP 2RR**: 21855.91 ✅
- **TP 2.5RR**: 21835.21 ❌
- **TP 3RR**: 21814.51 ❌
- **TP 3.5RR**: 21793.81 ❌
- **TP 4RR**: 21773.12 ❌
- **TP 4.5RR**: 21752.42 ❌
- **TP 5RR**: 21731.72 ❌
- **PnL**: -41.40 points (-1.0R)
- **MFE**: 93.56 points
- **MAE**: 41.75 points

### Trade #279 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:00:00
- **FVG 5m**: 21961.90 - 21969.12
- **Entrée**: 21938.71 @ 2025-02-26 08:01:00
- **Stop Loss**: 21980.11
- **Risk**: 41.40 points
- **TP 1RR**: 21897.31 ✅
- **TP 1.5RR**: 21876.61 ✅
- **TP 2RR**: 21855.91 ✅
- **TP 2.5RR**: 21835.21 ❌
- **TP 3RR**: 21814.51 ❌
- **TP 3.5RR**: 21793.81 ❌
- **TP 4RR**: 21773.12 ❌
- **TP 4.5RR**: 21752.42 ❌
- **TP 5RR**: 21731.72 ❌
- **PnL**: -41.40 points (-1.0R)
- **MFE**: 93.56 points
- **MAE**: 41.75 points

### Trade #280 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:00:00
- **FVG 5m**: 21961.90 - 21969.12
- **Entrée**: 21938.71 @ 2025-02-26 08:01:00
- **Stop Loss**: 21980.11
- **Risk**: 41.40 points
- **TP 1RR**: 21897.31 ✅
- **TP 1.5RR**: 21876.61 ✅
- **TP 2RR**: 21855.91 ✅
- **TP 2.5RR**: 21835.21 ❌
- **TP 3RR**: 21814.51 ❌
- **TP 3.5RR**: 21793.81 ❌
- **TP 4RR**: 21773.12 ❌
- **TP 4.5RR**: 21752.42 ❌
- **TP 5RR**: 21731.72 ❌
- **PnL**: -41.40 points (-1.0R)
- **MFE**: 93.56 points
- **MAE**: 41.75 points

### Trade #281 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:15:00
- **FVG 5m**: 21961.90 - 21969.12
- **Entrée**: 21901.85 @ 2025-02-26 08:16:00
- **Stop Loss**: 21980.11
- **Risk**: 78.26 points
- **TP 1RR**: 21823.60 ❌
- **TP 1.5RR**: 21784.47 ❌
- **TP 2RR**: 21745.34 ❌
- **TP 2.5RR**: 21706.21 ❌
- **TP 3RR**: 21667.09 ❌
- **TP 3.5RR**: 21627.96 ❌
- **TP 4RR**: 21588.83 ❌
- **TP 4.5RR**: 21549.70 ❌
- **TP 5RR**: 21510.58 ❌
- **PnL**: -78.26 points (-1.0R)
- **MFE**: 56.70 points
- **MAE**: 78.61 points

### Trade #282 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 08:30:00
- **FVG 5m**: 21915.51 - 21929.94
- **Entrée**: 21935.62 @ 2025-02-26 08:49:00
- **Stop Loss**: 21904.55
- **Risk**: 31.06 points
- **TP 1RR**: 21966.68 ✅
- **TP 1.5RR**: 21982.21 ✅
- **TP 2RR**: 21997.74 ✅
- **TP 2.5RR**: 22013.27 ✅
- **TP 3RR**: 22028.80 ✅
- **TP 3.5RR**: 22044.33 ✅
- **TP 4RR**: 22059.86 ✅
- **TP 4.5RR**: 22075.39 ❌
- **TP 5RR**: 22090.92 ❌
- **PnL**: -31.06 points (-1.0R)
- **MFE**: 136.60 points
- **MAE**: 37.89 points

### Trade #283 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 08:30:00
- **FVG 5m**: 21915.51 - 21929.94
- **Entrée**: 21935.62 @ 2025-02-26 08:49:00
- **Stop Loss**: 21904.55
- **Risk**: 31.06 points
- **TP 1RR**: 21966.68 ✅
- **TP 1.5RR**: 21982.21 ✅
- **TP 2RR**: 21997.74 ✅
- **TP 2.5RR**: 22013.27 ✅
- **TP 3RR**: 22028.80 ✅
- **TP 3.5RR**: 22044.33 ✅
- **TP 4RR**: 22059.86 ✅
- **TP 4.5RR**: 22075.39 ❌
- **TP 5RR**: 22090.92 ❌
- **PnL**: -31.06 points (-1.0R)
- **MFE**: 136.60 points
- **MAE**: 37.89 points

### Trade #284 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 09:15:00
- **FVG 5m**: 21961.90 - 21969.12
- **Entrée**: 21958.30 @ 2025-02-26 09:28:00
- **Stop Loss**: 21980.11
- **Risk**: 21.81 points
- **TP 1RR**: 21936.49 ✅
- **TP 1.5RR**: 21925.58 ❌
- **TP 2RR**: 21914.68 ❌
- **TP 2.5RR**: 21903.77 ❌
- **TP 3RR**: 21892.87 ❌
- **TP 3.5RR**: 21881.96 ❌
- **TP 4RR**: 21871.06 ❌
- **TP 4.5RR**: 21860.15 ❌
- **TP 5RR**: 21849.25 ❌
- **PnL**: -21.81 points (-1.0R)
- **MFE**: 28.61 points
- **MAE**: 23.45 points

### Trade #285 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 09:15:00
- **FVG 5m**: 21961.90 - 21969.12
- **Entrée**: 21958.30 @ 2025-02-26 09:28:00
- **Stop Loss**: 21980.11
- **Risk**: 21.81 points
- **TP 1RR**: 21936.49 ✅
- **TP 1.5RR**: 21925.58 ❌
- **TP 2RR**: 21914.68 ❌
- **TP 2.5RR**: 21903.77 ❌
- **TP 3RR**: 21892.87 ❌
- **TP 3.5RR**: 21881.96 ❌
- **TP 4RR**: 21871.06 ❌
- **TP 4.5RR**: 21860.15 ❌
- **TP 5RR**: 21849.25 ❌
- **PnL**: -21.81 points (-1.0R)
- **MFE**: 28.61 points
- **MAE**: 23.45 points

### Trade #286 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 09:15:00
- **FVG 5m**: 21961.90 - 21969.12
- **Entrée**: 21958.30 @ 2025-02-26 09:28:00
- **Stop Loss**: 21980.11
- **Risk**: 21.81 points
- **TP 1RR**: 21936.49 ✅
- **TP 1.5RR**: 21925.58 ❌
- **TP 2RR**: 21914.68 ❌
- **TP 2.5RR**: 21903.77 ❌
- **TP 3RR**: 21892.87 ❌
- **TP 3.5RR**: 21881.96 ❌
- **TP 4RR**: 21871.06 ❌
- **TP 4.5RR**: 21860.15 ❌
- **TP 5RR**: 21849.25 ❌
- **PnL**: -21.81 points (-1.0R)
- **MFE**: 28.61 points
- **MAE**: 23.45 points

### Trade #287 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 14:30:00
- **FVG 5m**: 21769.37 - 21786.64
- **Entrée**: 21790.51 @ 2025-02-26 14:31:00
- **Stop Loss**: 21758.49
- **Risk**: 32.02 points
- **TP 1RR**: 21822.53 ✅
- **TP 1.5RR**: 21838.54 ✅
- **TP 2RR**: 21854.55 ✅
- **TP 2.5RR**: 21870.56 ✅
- **TP 3RR**: 21886.57 ✅
- **TP 3.5RR**: 21902.58 ❌
- **TP 4RR**: 21918.58 ❌
- **TP 4.5RR**: 21934.59 ❌
- **TP 5RR**: 21950.60 ❌
- **PnL**: -32.02 points (-1.0R)
- **MFE**: 195.37 points
- **MAE**: 83.51 points

### Trade #288 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-27 07:45:00
- **FVG 5m**: 21985.10 - 21987.94
- **Entrée**: 21976.34 @ 2025-02-27 07:46:00
- **Stop Loss**: 21998.93
- **Risk**: 22.59 points
- **TP 1RR**: 21953.75 ✅
- **TP 1.5RR**: 21942.45 ✅
- **TP 2RR**: 21931.15 ✅
- **TP 2.5RR**: 21919.86 ❌
- **TP 3RR**: 21908.56 ❌
- **TP 3.5RR**: 21897.27 ❌
- **TP 4RR**: 21885.97 ❌
- **TP 4.5RR**: 21874.67 ❌
- **TP 5RR**: 21863.38 ❌
- **PnL**: -22.59 points (-1.0R)
- **MFE**: 48.97 points
- **MAE**: 37.11 points

### Trade #289 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-27 08:30:00
- **FVG 5m**: 21985.10 - 21989.23
- **Entrée**: 21968.35 @ 2025-02-27 08:39:00
- **Stop Loss**: 22000.22
- **Risk**: 31.87 points
- **TP 1RR**: 21936.48 ✅
- **TP 1.5RR**: 21920.54 ✅
- **TP 2RR**: 21904.61 ✅
- **TP 2.5RR**: 21888.67 ✅
- **TP 3RR**: 21872.73 ✅
- **TP 3.5RR**: 21856.80 ✅
- **TP 4RR**: 21840.86 ✅
- **TP 4.5RR**: 21824.93 ✅
- **TP 5RR**: 21808.99 ✅
- **PnL**: 159.36 points (5.0R)
- **MFE**: 172.43 points
- **MAE**: 0.26 points

### Trade #290 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:15:00
- **FVG 5m**: 21659.57 - 21720.40
- **Entrée**: 21730.97 @ 2025-02-27 09:16:00
- **Stop Loss**: 21648.74
- **Risk**: 82.22 points
- **TP 1RR**: 21813.19 ✅
- **TP 1.5RR**: 21854.30 ❌
- **TP 2RR**: 21895.42 ❌
- **TP 2.5RR**: 21936.53 ❌
- **TP 3RR**: 21977.64 ❌
- **TP 3.5RR**: 22018.75 ❌
- **TP 4RR**: 22059.87 ❌
- **TP 4.5RR**: 22100.98 ❌
- **TP 5RR**: 22142.09 ❌
- **PnL**: -82.22 points (-1.0R)
- **MFE**: 90.47 points
- **MAE**: 86.34 points

### Trade #291 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 21:45:00
- **FVG 5m**: 21213.94 - 21219.35
- **Entrée**: 21226.83 @ 2025-02-27 22:22:00
- **Stop Loss**: 21203.33
- **Risk**: 23.49 points
- **TP 1RR**: 21250.32 ✅
- **TP 1.5RR**: 21262.07 ✅
- **TP 2RR**: 21273.81 ✅
- **TP 2.5RR**: 21285.56 ❌
- **TP 3RR**: 21297.31 ❌
- **TP 3.5RR**: 21309.06 ❌
- **TP 4RR**: 21320.80 ❌
- **TP 4.5RR**: 21332.55 ❌
- **TP 5RR**: 21344.30 ❌
- **PnL**: -23.49 points (-1.0R)
- **MFE**: 58.25 points
- **MAE**: 25.77 points

### Trade #292 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 06:00:00
- **FVG 5m**: 21300.02 - 21303.12
- **Entrée**: 21285.08 @ 2025-02-28 06:01:00
- **Stop Loss**: 21313.77
- **Risk**: 28.69 points
- **TP 1RR**: 21256.38 ✅
- **TP 1.5RR**: 21242.04 ✅
- **TP 2RR**: 21227.69 ✅
- **TP 2.5RR**: 21213.34 ✅
- **TP 3RR**: 21199.00 ✅
- **TP 3.5RR**: 21184.65 ✅
- **TP 4RR**: 21170.30 ✅
- **TP 4.5RR**: 21155.95 ✅
- **TP 5RR**: 21141.61 ✅
- **PnL**: 143.47 points (5.0R)
- **MFE**: 155.16 points
- **MAE**: 19.07 points

### Trade #293 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 06:00:00
- **FVG 5m**: 21300.02 - 21303.12
- **Entrée**: 21285.08 @ 2025-02-28 06:01:00
- **Stop Loss**: 21313.77
- **Risk**: 28.69 points
- **TP 1RR**: 21256.38 ✅
- **TP 1.5RR**: 21242.04 ✅
- **TP 2RR**: 21227.69 ✅
- **TP 2.5RR**: 21213.34 ✅
- **TP 3RR**: 21199.00 ✅
- **TP 3.5RR**: 21184.65 ✅
- **TP 4RR**: 21170.30 ✅
- **TP 4.5RR**: 21155.95 ✅
- **TP 5RR**: 21141.61 ✅
- **PnL**: 143.47 points (5.0R)
- **MFE**: 155.16 points
- **MAE**: 19.07 points

### Trade #294 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 08:30:00
- **FVG 5m**: 21242.81 - 21246.93
- **Entrée**: 21267.29 @ 2025-02-28 08:43:00
- **Stop Loss**: 21232.18
- **Risk**: 35.11 points
- **TP 1RR**: 21302.40 ❌
- **TP 1.5RR**: 21319.95 ❌
- **TP 2RR**: 21337.51 ❌
- **TP 2.5RR**: 21355.06 ❌
- **TP 3RR**: 21372.61 ❌
- **TP 3.5RR**: 21390.17 ❌
- **TP 4RR**: 21407.72 ❌
- **TP 4.5RR**: 21425.27 ❌
- **TP 5RR**: 21442.83 ❌
- **PnL**: -35.11 points (-1.0R)
- **MFE**: 3.35 points
- **MAE**: 54.13 points

### Trade #295 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 08:30:00
- **FVG 5m**: 21242.81 - 21246.93
- **Entrée**: 21267.29 @ 2025-02-28 08:43:00
- **Stop Loss**: 21232.18
- **Risk**: 35.11 points
- **TP 1RR**: 21302.40 ❌
- **TP 1.5RR**: 21319.95 ❌
- **TP 2RR**: 21337.51 ❌
- **TP 2.5RR**: 21355.06 ❌
- **TP 3RR**: 21372.61 ❌
- **TP 3.5RR**: 21390.17 ❌
- **TP 4RR**: 21407.72 ❌
- **TP 4.5RR**: 21425.27 ❌
- **TP 5RR**: 21442.83 ❌
- **PnL**: -35.11 points (-1.0R)
- **MFE**: 3.35 points
- **MAE**: 54.13 points

### Trade #296 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 09:15:00
- **FVG 5m**: 21242.81 - 21246.93
- **Entrée**: 21291.26 @ 2025-02-28 09:16:00
- **Stop Loss**: 21232.18
- **Risk**: 59.08 points
- **TP 1RR**: 21350.34 ✅
- **TP 1.5RR**: 21379.88 ✅
- **TP 2RR**: 21409.41 ✅
- **TP 2.5RR**: 21438.95 ❌
- **TP 3RR**: 21468.49 ❌
- **TP 3.5RR**: 21498.03 ❌
- **TP 4RR**: 21527.57 ❌
- **TP 4.5RR**: 21557.11 ❌
- **TP 5RR**: 21586.65 ❌
- **PnL**: -59.08 points (-1.0R)
- **MFE**: 130.16 points
- **MAE**: 59.54 points

### Trade #297 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 09:15:00
- **FVG 5m**: 21242.81 - 21246.93
- **Entrée**: 21291.26 @ 2025-02-28 09:16:00
- **Stop Loss**: 21232.18
- **Risk**: 59.08 points
- **TP 1RR**: 21350.34 ✅
- **TP 1.5RR**: 21379.88 ✅
- **TP 2RR**: 21409.41 ✅
- **TP 2.5RR**: 21438.95 ❌
- **TP 3RR**: 21468.49 ❌
- **TP 3.5RR**: 21498.03 ❌
- **TP 4RR**: 21527.57 ❌
- **TP 4.5RR**: 21557.11 ❌
- **TP 5RR**: 21586.65 ❌
- **PnL**: -59.08 points (-1.0R)
- **MFE**: 130.16 points
- **MAE**: 59.54 points

### Trade #298 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 09:15:00
- **FVG 5m**: 21242.81 - 21246.93
- **Entrée**: 21291.26 @ 2025-02-28 09:16:00
- **Stop Loss**: 21232.18
- **Risk**: 59.08 points
- **TP 1RR**: 21350.34 ✅
- **TP 1.5RR**: 21379.88 ✅
- **TP 2RR**: 21409.41 ✅
- **TP 2.5RR**: 21438.95 ❌
- **TP 3RR**: 21468.49 ❌
- **TP 3.5RR**: 21498.03 ❌
- **TP 4RR**: 21527.57 ❌
- **TP 4.5RR**: 21557.11 ❌
- **TP 5RR**: 21586.65 ❌
- **PnL**: -59.08 points (-1.0R)
- **MFE**: 130.16 points
- **MAE**: 59.54 points

### Trade #299 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 10:15:00
- **FVG 5m**: 21363.94 - 21370.39
- **Entrée**: 21288.94 @ 2025-02-28 10:16:00
- **Stop Loss**: 21381.07
- **Risk**: 92.13 points
- **TP 1RR**: 21196.81 ❌
- **TP 1.5RR**: 21150.74 ❌
- **TP 2RR**: 21104.68 ❌
- **TP 2.5RR**: 21058.61 ❌
- **TP 3RR**: 21012.55 ❌
- **TP 3.5RR**: 20966.48 ❌
- **TP 4RR**: 20920.42 ❌
- **TP 4.5RR**: 20874.35 ❌
- **TP 5RR**: 20828.28 ❌
- **PnL**: -92.13 points (-1.0R)
- **MFE**: 25.77 points
- **MAE**: 96.91 points

### Trade #300 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 10:15:00
- **FVG 5m**: 21363.94 - 21370.39
- **Entrée**: 21288.94 @ 2025-02-28 10:16:00
- **Stop Loss**: 21381.07
- **Risk**: 92.13 points
- **TP 1RR**: 21196.81 ❌
- **TP 1.5RR**: 21150.74 ❌
- **TP 2RR**: 21104.68 ❌
- **TP 2.5RR**: 21058.61 ❌
- **TP 3RR**: 21012.55 ❌
- **TP 3.5RR**: 20966.48 ❌
- **TP 4RR**: 20920.42 ❌
- **TP 4.5RR**: 20874.35 ❌
- **TP 5RR**: 20828.28 ❌
- **PnL**: -92.13 points (-1.0R)
- **MFE**: 25.77 points
- **MAE**: 96.91 points

### Trade #301 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 10:15:00
- **FVG 5m**: 21363.94 - 21370.39
- **Entrée**: 21288.94 @ 2025-02-28 10:16:00
- **Stop Loss**: 21381.07
- **Risk**: 92.13 points
- **TP 1RR**: 21196.81 ❌
- **TP 1.5RR**: 21150.74 ❌
- **TP 2RR**: 21104.68 ❌
- **TP 2.5RR**: 21058.61 ❌
- **TP 3RR**: 21012.55 ❌
- **TP 3.5RR**: 20966.48 ❌
- **TP 4RR**: 20920.42 ❌
- **TP 4.5RR**: 20874.35 ❌
- **TP 5RR**: 20828.28 ❌
- **PnL**: -92.13 points (-1.0R)
- **MFE**: 25.77 points
- **MAE**: 96.91 points

### Trade #302 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 14:15:00
- **FVG 5m**: 21230.18 - 21254.66
- **Entrée**: 21385.08 @ 2025-02-28 14:16:00
- **Stop Loss**: 21219.56
- **Risk**: 165.52 points
- **TP 1RR**: 21550.60 ✅
- **TP 1.5RR**: 21633.36 ✅
- **TP 2RR**: 21716.11 ✅
- **TP 2.5RR**: 21798.87 ❌
- **TP 3RR**: 21881.63 ❌
- **TP 3.5RR**: 21964.39 ❌
- **TP 4RR**: 22047.15 ❌
- **TP 4.5RR**: 22129.91 ❌
- **TP 5RR**: 22212.67 ❌
- **PnL**: -165.52 points (-1.0R)
- **MFE**: 389.96 points
- **MAE**: 179.39 points

### Trade #303 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 14:45:00
- **FVG 5m**: 21230.18 - 21254.66
- **Entrée**: 21400.03 @ 2025-02-28 14:46:00
- **Stop Loss**: 21219.56
- **Risk**: 180.47 points
- **TP 1RR**: 21580.50 ✅
- **TP 1.5RR**: 21670.73 ✅
- **TP 2RR**: 21760.96 ✅
- **TP 2.5RR**: 21851.20 ❌
- **TP 3RR**: 21941.43 ❌
- **TP 3.5RR**: 22031.66 ❌
- **TP 4RR**: 22121.90 ❌
- **TP 4.5RR**: 22212.13 ❌
- **TP 5RR**: 22302.36 ❌
- **PnL**: -180.47 points (-1.0R)
- **MFE**: 375.01 points
- **MAE**: 194.34 points

### Trade #304 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 14:45:00
- **FVG 5m**: 21230.18 - 21254.66
- **Entrée**: 21400.03 @ 2025-02-28 14:46:00
- **Stop Loss**: 21219.56
- **Risk**: 180.47 points
- **TP 1RR**: 21580.50 ✅
- **TP 1.5RR**: 21670.73 ✅
- **TP 2RR**: 21760.96 ✅
- **TP 2.5RR**: 21851.20 ❌
- **TP 3RR**: 21941.43 ❌
- **TP 3.5RR**: 22031.66 ❌
- **TP 4RR**: 22121.90 ❌
- **TP 4.5RR**: 22212.13 ❌
- **TP 5RR**: 22302.36 ❌
- **PnL**: -180.47 points (-1.0R)
- **MFE**: 375.01 points
- **MAE**: 194.34 points

### Trade #305 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-02 23:00:00
- **FVG 5m**: 21582.25 - 21587.41
- **Entrée**: 21607.51 @ 2025-03-02 23:01:00
- **Stop Loss**: 21571.46
- **Risk**: 36.05 points
- **TP 1RR**: 21643.56 ✅
- **TP 1.5RR**: 21661.58 ✅
- **TP 2RR**: 21679.61 ❌
- **TP 2.5RR**: 21697.63 ❌
- **TP 3RR**: 21715.66 ❌
- **TP 3.5RR**: 21733.68 ❌
- **TP 4RR**: 21751.71 ❌
- **TP 4.5RR**: 21769.73 ❌
- **TP 5RR**: 21787.76 ❌
- **PnL**: -36.05 points (-1.0R)
- **MFE**: 64.69 points
- **MAE**: 36.34 points

### Trade #306 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 01:15:00
- **FVG 5m**: 21632.25 - 21635.35
- **Entrée**: 21627.36 @ 2025-03-03 01:16:00
- **Stop Loss**: 21646.16
- **Risk**: 18.81 points
- **TP 1RR**: 21608.55 ✅
- **TP 1.5RR**: 21599.14 ✅
- **TP 2RR**: 21589.74 ✅
- **TP 2.5RR**: 21580.34 ✅
- **TP 3RR**: 21570.93 ✅
- **TP 3.5RR**: 21561.53 ✅
- **TP 4RR**: 21552.13 ✅
- **TP 4.5RR**: 21542.72 ✅
- **TP 5RR**: 21533.32 ❌
- **PnL**: -18.81 points (-1.0R)
- **MFE**: 92.53 points
- **MAE**: 21.39 points

### Trade #307 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 08:30:00
- **FVG 5m**: 21725.56 - 21736.64
- **Entrée**: 21716.28 @ 2025-03-03 08:31:00
- **Stop Loss**: 21747.51
- **Risk**: 31.23 points
- **TP 1RR**: 21685.05 ❌
- **TP 1.5RR**: 21669.43 ❌
- **TP 2RR**: 21653.82 ❌
- **TP 2.5RR**: 21638.20 ❌
- **TP 3RR**: 21622.59 ❌
- **TP 3.5RR**: 21606.97 ❌
- **TP 4RR**: 21591.36 ❌
- **TP 4.5RR**: 21575.74 ❌
- **TP 5RR**: 21560.13 ❌
- **PnL**: -31.23 points (-1.0R)
- **MFE**: 1.03 points
- **MAE**: 33.51 points

### Trade #308 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 08:30:00
- **FVG 5m**: 21725.56 - 21736.64
- **Entrée**: 21716.28 @ 2025-03-03 08:31:00
- **Stop Loss**: 21747.51
- **Risk**: 31.23 points
- **TP 1RR**: 21685.05 ❌
- **TP 1.5RR**: 21669.43 ❌
- **TP 2RR**: 21653.82 ❌
- **TP 2.5RR**: 21638.20 ❌
- **TP 3RR**: 21622.59 ❌
- **TP 3.5RR**: 21606.97 ❌
- **TP 4RR**: 21591.36 ❌
- **TP 4.5RR**: 21575.74 ❌
- **TP 5RR**: 21560.13 ❌
- **PnL**: -31.23 points (-1.0R)
- **MFE**: 1.03 points
- **MAE**: 33.51 points

### Trade #309 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 08:30:00
- **FVG 5m**: 21725.56 - 21736.64
- **Entrée**: 21716.28 @ 2025-03-03 08:31:00
- **Stop Loss**: 21747.51
- **Risk**: 31.23 points
- **TP 1RR**: 21685.05 ❌
- **TP 1.5RR**: 21669.43 ❌
- **TP 2RR**: 21653.82 ❌
- **TP 2.5RR**: 21638.20 ❌
- **TP 3RR**: 21622.59 ❌
- **TP 3.5RR**: 21606.97 ❌
- **TP 4RR**: 21591.36 ❌
- **TP 4.5RR**: 21575.74 ❌
- **TP 5RR**: 21560.13 ❌
- **PnL**: -31.23 points (-1.0R)
- **MFE**: 1.03 points
- **MAE**: 33.51 points

### Trade #310 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 09:15:00
- **FVG 5m**: 21519.62 - 21548.23
- **Entrée**: 21552.10 @ 2025-03-03 09:22:00
- **Stop Loss**: 21508.86
- **Risk**: 43.24 points
- **TP 1RR**: 21595.33 ✅
- **TP 1.5RR**: 21616.95 ✅
- **TP 2RR**: 21638.57 ✅
- **TP 2.5RR**: 21660.18 ❌
- **TP 3RR**: 21681.80 ❌
- **TP 3.5RR**: 21703.42 ❌
- **TP 4RR**: 21725.04 ❌
- **TP 4.5RR**: 21746.65 ❌
- **TP 5RR**: 21768.27 ❌
- **PnL**: -43.24 points (-1.0R)
- **MFE**: 87.12 points
- **MAE**: 45.36 points

### Trade #311 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 09:15:00
- **FVG 5m**: 21519.62 - 21548.23
- **Entrée**: 21552.10 @ 2025-03-03 09:22:00
- **Stop Loss**: 21508.86
- **Risk**: 43.24 points
- **TP 1RR**: 21595.33 ✅
- **TP 1.5RR**: 21616.95 ✅
- **TP 2RR**: 21638.57 ✅
- **TP 2.5RR**: 21660.18 ❌
- **TP 3RR**: 21681.80 ❌
- **TP 3.5RR**: 21703.42 ❌
- **TP 4RR**: 21725.04 ❌
- **TP 4.5RR**: 21746.65 ❌
- **TP 5RR**: 21768.27 ❌
- **PnL**: -43.24 points (-1.0R)
- **MFE**: 87.12 points
- **MAE**: 45.36 points

### Trade #312 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 12:00:00
- **FVG 5m**: 21551.32 - 21561.89
- **Entrée**: 21477.61 @ 2025-03-03 12:01:00
- **Stop Loss**: 21572.67
- **Risk**: 95.06 points
- **TP 1RR**: 21382.55 ✅
- **TP 1.5RR**: 21335.01 ✅
- **TP 2RR**: 21287.48 ✅
- **TP 2.5RR**: 21239.95 ✅
- **TP 3RR**: 21192.42 ✅
- **TP 3.5RR**: 21144.89 ✅
- **TP 4RR**: 21097.36 ✅
- **TP 4.5RR**: 21049.83 ✅
- **TP 5RR**: 21002.30 ✅
- **PnL**: 475.31 points (5.0R)
- **MFE**: 478.37 points
- **MAE**: 8.51 points

### Trade #313 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 13:30:00
- **FVG 5m**: 21352.86 - 21366.01
- **Entrée**: 21401.57 @ 2025-03-03 13:31:00
- **Stop Loss**: 21342.19
- **Risk**: 59.39 points
- **TP 1RR**: 21460.96 ✅
- **TP 1.5RR**: 21490.66 ❌
- **TP 2RR**: 21520.35 ❌
- **TP 2.5RR**: 21550.05 ❌
- **TP 3RR**: 21579.74 ❌
- **TP 3.5RR**: 21609.44 ❌
- **TP 4RR**: 21639.13 ❌
- **TP 4.5RR**: 21668.83 ❌
- **TP 5RR**: 21698.52 ❌
- **PnL**: -59.39 points (-1.0R)
- **MFE**: 62.89 points
- **MAE**: 111.09 points

### Trade #314 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 15:00:00
- **FVG 5m**: 20999.24 - 21001.82
- **Entrée**: 21125.28 @ 2025-03-03 15:01:00
- **Stop Loss**: 20988.74
- **Risk**: 136.54 points
- **TP 1RR**: 21261.81 ❌
- **TP 1.5RR**: 21330.08 ❌
- **TP 2RR**: 21398.35 ❌
- **TP 2.5RR**: 21466.61 ❌
- **TP 3RR**: 21534.88 ❌
- **TP 3.5RR**: 21603.15 ❌
- **TP 4RR**: 21671.42 ❌
- **TP 4.5RR**: 21739.68 ❌
- **TP 5RR**: 21807.95 ❌
- **PnL**: -136.54 points (-1.0R)
- **MFE**: 104.39 points
- **MAE**: 147.69 points

### Trade #315 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 19:00:00
- **FVG 5m**: 21152.60 - 21173.22
- **Entrée**: 21148.99 @ 2025-03-03 19:13:00
- **Stop Loss**: 21183.80
- **Risk**: 34.81 points
- **TP 1RR**: 21114.17 ✅
- **TP 1.5RR**: 21096.77 ❌
- **TP 2RR**: 21079.36 ❌
- **TP 2.5RR**: 21061.95 ❌
- **TP 3RR**: 21044.54 ❌
- **TP 3.5RR**: 21027.14 ❌
- **TP 4RR**: 21009.73 ❌
- **TP 4.5RR**: 20992.32 ❌
- **TP 5RR**: 20974.92 ❌
- **PnL**: -34.81 points (-1.0R)
- **MFE**: 48.97 points
- **MAE**: 36.86 points

### Trade #316 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 23:00:00
- **FVG 5m**: 21180.17 - 21189.45
- **Entrée**: 21177.85 @ 2025-03-03 23:02:00
- **Stop Loss**: 21200.05
- **Risk**: 22.19 points
- **TP 1RR**: 21155.66 ❌
- **TP 1.5RR**: 21144.57 ❌
- **TP 2RR**: 21133.47 ❌
- **TP 2.5RR**: 21122.37 ❌
- **TP 3RR**: 21111.28 ❌
- **TP 3.5RR**: 21100.18 ❌
- **TP 4RR**: 21089.08 ❌
- **TP 4.5RR**: 21077.99 ❌
- **TP 5RR**: 21066.89 ❌
- **PnL**: -22.19 points (-1.0R)
- **MFE**: 2.06 points
- **MAE**: 24.74 points

### Trade #317 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-04 02:00:00
- **FVG 5m**: 21150.28 - 21180.17
- **Entrée**: 21187.13 @ 2025-03-04 02:31:00
- **Stop Loss**: 21139.70
- **Risk**: 47.43 points
- **TP 1RR**: 21234.57 ❌
- **TP 1.5RR**: 21258.28 ❌
- **TP 2RR**: 21282.00 ❌
- **TP 2.5RR**: 21305.71 ❌
- **TP 3RR**: 21329.43 ❌
- **TP 3.5RR**: 21353.15 ❌
- **TP 4RR**: 21376.86 ❌
- **TP 4.5RR**: 21400.58 ❌
- **TP 5RR**: 21424.29 ❌
- **PnL**: -47.43 points (-1.0R)
- **MFE**: 13.14 points
- **MAE**: 53.35 points

### Trade #318 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-04 07:30:00
- **FVG 5m**: 20968.31 - 20974.50
- **Entrée**: 20977.85 @ 2025-03-04 07:41:00
- **Stop Loss**: 20957.83
- **Risk**: 20.02 points
- **TP 1RR**: 20997.87 ❌
- **TP 1.5RR**: 21007.88 ❌
- **TP 2RR**: 21017.89 ❌
- **TP 2.5RR**: 21027.90 ❌
- **TP 3RR**: 21037.91 ❌
- **TP 3.5RR**: 21047.92 ❌
- **TP 4RR**: 21057.93 ❌
- **TP 4.5RR**: 21067.94 ❌
- **TP 5RR**: 21077.95 ❌
- **PnL**: -20.02 points (-1.0R)
- **MFE**: 5.67 points
- **MAE**: 22.94 points

### Trade #319 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-04 12:00:00
- **FVG 5m**: 20988.93 - 20991.51
- **Entrée**: 20994.34 @ 2025-03-04 12:03:00
- **Stop Loss**: 20978.44
- **Risk**: 15.91 points
- **TP 1RR**: 21010.25 ❌
- **TP 1.5RR**: 21018.20 ❌
- **TP 2RR**: 21026.16 ❌
- **TP 2.5RR**: 21034.11 ❌
- **TP 3RR**: 21042.06 ❌
- **TP 3.5RR**: 21050.02 ❌
- **TP 4RR**: 21057.97 ❌
- **TP 4.5RR**: 21065.92 ❌
- **TP 5RR**: 21073.88 ❌
- **PnL**: -15.91 points (-1.0R)
- **MFE**: 14.95 points
- **MAE**: 22.94 points

### Trade #320 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-04 12:15:00
- **FVG 5m**: 21002.33 - 21045.89
- **Entrée**: 20987.90 @ 2025-03-04 12:30:00
- **Stop Loss**: 21056.41
- **Risk**: 68.51 points
- **TP 1RR**: 20919.38 ❌
- **TP 1.5RR**: 20885.13 ❌
- **TP 2RR**: 20850.87 ❌
- **TP 2.5RR**: 20816.61 ❌
- **TP 3RR**: 20782.35 ❌
- **TP 3.5RR**: 20748.10 ❌
- **TP 4RR**: 20713.84 ❌
- **TP 4.5RR**: 20679.58 ❌
- **TP 5RR**: 20645.33 ❌
- **PnL**: -68.51 points (-1.0R)
- **MFE**: 6.70 points
- **MAE**: 68.56 points

### Trade #321 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-04 14:45:00
- **FVG 5m**: 21158.52 - 21175.02
- **Entrée**: 21142.80 @ 2025-03-04 14:46:00
- **Stop Loss**: 21185.61
- **Risk**: 42.81 points
- **TP 1RR**: 21100.00 ✅
- **TP 1.5RR**: 21078.59 ✅
- **TP 2RR**: 21057.19 ✅
- **TP 2.5RR**: 21035.79 ✅
- **TP 3RR**: 21014.39 ✅
- **TP 3.5RR**: 20992.98 ✅
- **TP 4RR**: 20971.58 ✅
- **TP 4.5RR**: 20950.18 ❌
- **TP 5RR**: 20928.78 ❌
- **PnL**: -42.81 points (-1.0R)
- **MFE**: 189.18 points
- **MAE**: 63.92 points

### Trade #322 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-05 02:30:00
- **FVG 5m**: 21180.43 - 21195.12
- **Entrée**: 21176.57 @ 2025-03-05 02:56:00
- **Stop Loss**: 21205.72
- **Risk**: 29.15 points
- **TP 1RR**: 21147.41 ❌
- **TP 1.5RR**: 21132.83 ❌
- **TP 2RR**: 21118.26 ❌
- **TP 2.5RR**: 21103.68 ❌
- **TP 3RR**: 21089.10 ❌
- **TP 3.5RR**: 21074.52 ❌
- **TP 4RR**: 21059.95 ❌
- **TP 4.5RR**: 21045.37 ❌
- **TP 5RR**: 21030.79 ❌
- **PnL**: -29.15 points (-1.0R)
- **MFE**: 24.23 points
- **MAE**: 30.93 points

### Trade #323 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-05 04:00:00
- **FVG 5m**: 21207.24 - 21223.99
- **Entrée**: 21206.98 @ 2025-03-05 04:14:00
- **Stop Loss**: 21234.60
- **Risk**: 27.62 points
- **TP 1RR**: 21179.36 ✅
- **TP 1.5RR**: 21165.55 ✅
- **TP 2RR**: 21151.73 ✅
- **TP 2.5RR**: 21137.92 ✅
- **TP 3RR**: 21124.11 ✅
- **TP 3.5RR**: 21110.30 ✅
- **TP 4RR**: 21096.49 ✅
- **TP 4.5RR**: 21082.68 ✅
- **TP 5RR**: 21068.87 ✅
- **PnL**: 138.11 points (5.0R)
- **MFE**: 142.27 points
- **MAE**: 19.07 points

### Trade #324 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 08:30:00
- **FVG 5m**: 21052.08 - 21057.23
- **Entrée**: 21065.74 @ 2025-03-05 08:41:00
- **Stop Loss**: 21041.55
- **Risk**: 24.19 points
- **TP 1RR**: 21089.92 ❌
- **TP 1.5RR**: 21102.02 ❌
- **TP 2RR**: 21114.11 ❌
- **TP 2.5RR**: 21126.20 ❌
- **TP 3RR**: 21138.30 ❌
- **TP 3.5RR**: 21150.39 ❌
- **TP 4RR**: 21162.48 ❌
- **TP 4.5RR**: 21174.58 ❌
- **TP 5RR**: 21186.67 ❌
- **PnL**: -24.19 points (-1.0R)
- **MFE**: 23.45 points
- **MAE**: 29.12 points

### Trade #325 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 11:15:00
- **FVG 5m**: 20934.80 - 20945.63
- **Entrée**: 21019.60 @ 2025-03-05 11:16:00
- **Stop Loss**: 20924.34
- **Risk**: 95.26 points
- **TP 1RR**: 21114.87 ✅
- **TP 1.5RR**: 21162.50 ✅
- **TP 2RR**: 21210.13 ✅
- **TP 2.5RR**: 21257.76 ✅
- **TP 3RR**: 21305.39 ✅
- **TP 3.5RR**: 21353.03 ✅
- **TP 4RR**: 21400.66 ❌
- **TP 4.5RR**: 21448.29 ❌
- **TP 5RR**: 21495.92 ❌
- **PnL**: -95.26 points (-1.0R)
- **MFE**: 347.18 points
- **MAE**: 129.90 points

### Trade #326 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 11:15:00
- **FVG 5m**: 20934.80 - 20945.63
- **Entrée**: 21019.60 @ 2025-03-05 11:16:00
- **Stop Loss**: 20924.34
- **Risk**: 95.26 points
- **TP 1RR**: 21114.87 ✅
- **TP 1.5RR**: 21162.50 ✅
- **TP 2RR**: 21210.13 ✅
- **TP 2.5RR**: 21257.76 ✅
- **TP 3RR**: 21305.39 ✅
- **TP 3.5RR**: 21353.03 ✅
- **TP 4RR**: 21400.66 ❌
- **TP 4.5RR**: 21448.29 ❌
- **TP 5RR**: 21495.92 ❌
- **PnL**: -95.26 points (-1.0R)
- **MFE**: 347.18 points
- **MAE**: 129.90 points

### Trade #327 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-05 15:00:00
- **FVG 5m**: 21254.40 - 21307.50
- **Entrée**: 21236.10 @ 2025-03-05 15:05:00
- **Stop Loss**: 21318.15
- **Risk**: 82.05 points
- **TP 1RR**: 21154.06 ✅
- **TP 1.5RR**: 21113.03 ✅
- **TP 2RR**: 21072.01 ✅
- **TP 2.5RR**: 21030.98 ✅
- **TP 3RR**: 20989.96 ✅
- **TP 3.5RR**: 20948.94 ✅
- **TP 4RR**: 20907.91 ✅
- **TP 4.5RR**: 20866.89 ✅
- **TP 5RR**: 20825.86 ✅
- **PnL**: 410.24 points (5.0R)
- **MFE**: 425.02 points
- **MAE**: 50.78 points

### Trade #328 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-06 01:00:00
- **FVG 5m**: 21244.09 - 21255.95
- **Entrée**: 21242.03 @ 2025-03-06 01:40:00
- **Stop Loss**: 21266.58
- **Risk**: 24.55 points
- **TP 1RR**: 21217.49 ✅
- **TP 1.5RR**: 21205.21 ✅
- **TP 2RR**: 21192.94 ✅
- **TP 2.5RR**: 21180.67 ✅
- **TP 3RR**: 21168.39 ✅
- **TP 3.5RR**: 21156.12 ✅
- **TP 4RR**: 21143.85 ✅
- **TP 4.5RR**: 21131.58 ✅
- **TP 5RR**: 21119.30 ✅
- **PnL**: 122.73 points (5.0R)
- **MFE**: 139.70 points
- **MAE**: 1.29 points

### Trade #329 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-06 08:00:00
- **FVG 5m**: 20980.68 - 20986.61
- **Entrée**: 21000.53 @ 2025-03-06 08:08:00
- **Stop Loss**: 20970.19
- **Risk**: 30.34 points
- **TP 1RR**: 21030.87 ❌
- **TP 1.5RR**: 21046.03 ❌
- **TP 2RR**: 21061.20 ❌
- **TP 2.5RR**: 21076.37 ❌
- **TP 3RR**: 21091.54 ❌
- **TP 3.5RR**: 21106.71 ❌
- **TP 4RR**: 21121.87 ❌
- **TP 4.5RR**: 21137.04 ❌
- **TP 5RR**: 21152.21 ❌
- **PnL**: -30.34 points (-1.0R)
- **MFE**: 2.06 points
- **MAE**: 34.54 points

### Trade #330 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-06 12:45:00
- **FVG 5m**: 20698.71 - 20742.53
- **Entrée**: 20759.80 @ 2025-03-06 12:52:00
- **Stop Loss**: 20688.36
- **Risk**: 71.43 points
- **TP 1RR**: 20831.23 ❌
- **TP 1.5RR**: 20866.95 ❌
- **TP 2RR**: 20902.67 ❌
- **TP 2.5RR**: 20938.38 ❌
- **TP 3RR**: 20974.10 ❌
- **TP 3.5RR**: 21009.82 ❌
- **TP 4RR**: 21045.53 ❌
- **TP 4.5RR**: 21081.25 ❌
- **TP 5RR**: 21116.97 ❌
- **PnL**: -71.43 points (-1.0R)
- **MFE**: 5.93 points
- **MAE**: 74.75 points

### Trade #331 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-06 19:00:00
- **FVG 5m**: 20799.23 - 20813.41
- **Entrée**: 20820.88 @ 2025-03-06 19:08:00
- **Stop Loss**: 20788.83
- **Risk**: 32.05 points
- **TP 1RR**: 20852.93 ❌
- **TP 1.5RR**: 20868.96 ❌
- **TP 2RR**: 20884.98 ❌
- **TP 2.5RR**: 20901.01 ❌
- **TP 3RR**: 20917.03 ❌
- **TP 3.5RR**: 20933.06 ❌
- **TP 4RR**: 20949.08 ❌
- **TP 4.5RR**: 20965.11 ❌
- **TP 5RR**: 20981.13 ❌
- **PnL**: -32.05 points (-1.0R)
- **MFE**: 25.26 points
- **MAE**: 33.25 points

### Trade #332 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 01:00:00
- **FVG 5m**: 20783.25 - 20786.86
- **Entrée**: 20788.15 @ 2025-03-07 01:06:00
- **Stop Loss**: 20772.86
- **Risk**: 15.29 points
- **TP 1RR**: 20803.44 ❌
- **TP 1.5RR**: 20811.08 ❌
- **TP 2RR**: 20818.73 ❌
- **TP 2.5RR**: 20826.37 ❌
- **TP 3RR**: 20834.02 ❌
- **TP 3.5RR**: 20841.66 ❌
- **TP 4RR**: 20849.30 ❌
- **TP 4.5RR**: 20856.95 ❌
- **TP 5RR**: 20864.59 ❌
- **PnL**: -15.29 points (-1.0R)
- **MFE**: 13.40 points
- **MAE**: 16.24 points

### Trade #333 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 01:00:00
- **FVG 5m**: 20783.25 - 20786.86
- **Entrée**: 20788.15 @ 2025-03-07 01:06:00
- **Stop Loss**: 20772.86
- **Risk**: 15.29 points
- **TP 1RR**: 20803.44 ❌
- **TP 1.5RR**: 20811.08 ❌
- **TP 2RR**: 20818.73 ❌
- **TP 2.5RR**: 20826.37 ❌
- **TP 3RR**: 20834.02 ❌
- **TP 3.5RR**: 20841.66 ❌
- **TP 4RR**: 20849.30 ❌
- **TP 4.5RR**: 20856.95 ❌
- **TP 5RR**: 20864.59 ❌
- **PnL**: -15.29 points (-1.0R)
- **MFE**: 13.40 points
- **MAE**: 16.24 points

### Trade #334 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 03:15:00
- **FVG 5m**: 20822.94 - 20833.00
- **Entrée**: 20821.40 @ 2025-03-07 03:25:00
- **Stop Loss**: 20843.41
- **Risk**: 22.01 points
- **TP 1RR**: 20799.38 ✅
- **TP 1.5RR**: 20788.38 ✅
- **TP 2RR**: 20777.37 ✅
- **TP 2.5RR**: 20766.36 ✅
- **TP 3RR**: 20755.35 ✅
- **TP 3.5RR**: 20744.35 ✅
- **TP 4RR**: 20733.34 ✅
- **TP 4.5RR**: 20722.33 ✅
- **TP 5RR**: 20711.32 ✅
- **PnL**: 110.07 points (5.0R)
- **MFE**: 110.31 points
- **MAE**: 21.91 points

### Trade #335 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 06:45:00
- **FVG 5m**: 20811.35 - 20816.24
- **Entrée**: 20844.34 @ 2025-03-07 07:30:00
- **Stop Loss**: 20800.94
- **Risk**: 43.40 points
- **TP 1RR**: 20887.73 ✅
- **TP 1.5RR**: 20909.43 ❌
- **TP 2RR**: 20931.13 ❌
- **TP 2.5RR**: 20952.83 ❌
- **TP 3RR**: 20974.53 ❌
- **TP 3.5RR**: 20996.23 ❌
- **TP 4RR**: 21017.92 ❌
- **TP 4.5RR**: 21039.62 ❌
- **TP 5RR**: 21061.32 ❌
- **PnL**: -43.40 points (-1.0R)
- **MFE**: 57.22 points
- **MAE**: 46.39 points

### Trade #336 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20809.28 - 20816.24
- **Entrée**: 20802.07 @ 2025-03-07 07:33:00
- **Stop Loss**: 20826.65
- **Risk**: 24.58 points
- **TP 1RR**: 20777.48 ❌
- **TP 1.5RR**: 20765.19 ❌
- **TP 2RR**: 20752.90 ❌
- **TP 2.5RR**: 20740.61 ❌
- **TP 3RR**: 20728.32 ❌
- **TP 3.5RR**: 20716.02 ❌
- **TP 4RR**: 20703.73 ❌
- **TP 4.5RR**: 20691.44 ❌
- **TP 5RR**: 20679.15 ❌
- **PnL**: -24.58 points (-1.0R)
- **MFE**: 18.30 points
- **MAE**: 29.90 points

### Trade #337 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20809.28 - 20816.24
- **Entrée**: 20802.07 @ 2025-03-07 07:33:00
- **Stop Loss**: 20826.65
- **Risk**: 24.58 points
- **TP 1RR**: 20777.48 ❌
- **TP 1.5RR**: 20765.19 ❌
- **TP 2RR**: 20752.90 ❌
- **TP 2.5RR**: 20740.61 ❌
- **TP 3RR**: 20728.32 ❌
- **TP 3.5RR**: 20716.02 ❌
- **TP 4RR**: 20703.73 ❌
- **TP 4.5RR**: 20691.44 ❌
- **TP 5RR**: 20679.15 ❌
- **PnL**: -24.58 points (-1.0R)
- **MFE**: 18.30 points
- **MAE**: 29.90 points

### Trade #338 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20809.28 - 20816.24
- **Entrée**: 20802.07 @ 2025-03-07 07:33:00
- **Stop Loss**: 20826.65
- **Risk**: 24.58 points
- **TP 1RR**: 20777.48 ❌
- **TP 1.5RR**: 20765.19 ❌
- **TP 2RR**: 20752.90 ❌
- **TP 2.5RR**: 20740.61 ❌
- **TP 3RR**: 20728.32 ❌
- **TP 3.5RR**: 20716.02 ❌
- **TP 4RR**: 20703.73 ❌
- **TP 4.5RR**: 20691.44 ❌
- **TP 5RR**: 20679.15 ❌
- **PnL**: -24.58 points (-1.0R)
- **MFE**: 18.30 points
- **MAE**: 29.90 points

### Trade #339 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20809.28 - 20816.24
- **Entrée**: 20802.07 @ 2025-03-07 07:33:00
- **Stop Loss**: 20826.65
- **Risk**: 24.58 points
- **TP 1RR**: 20777.48 ❌
- **TP 1.5RR**: 20765.19 ❌
- **TP 2RR**: 20752.90 ❌
- **TP 2.5RR**: 20740.61 ❌
- **TP 3RR**: 20728.32 ❌
- **TP 3.5RR**: 20716.02 ❌
- **TP 4RR**: 20703.73 ❌
- **TP 4.5RR**: 20691.44 ❌
- **TP 5RR**: 20679.15 ❌
- **PnL**: -24.58 points (-1.0R)
- **MFE**: 18.30 points
- **MAE**: 29.90 points

### Trade #340 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 14:45:00
- **FVG 5m**: 20831.71 - 20841.24
- **Entrée**: 20804.13 @ 2025-03-07 14:46:00
- **Stop Loss**: 20851.67
- **Risk**: 47.54 points
- **TP 1RR**: 20756.59 ❌
- **TP 1.5RR**: 20732.83 ❌
- **TP 2RR**: 20709.06 ❌
- **TP 2.5RR**: 20685.29 ❌
- **TP 3RR**: 20661.52 ❌
- **TP 3.5RR**: 20637.76 ❌
- **TP 4RR**: 20613.99 ❌
- **TP 4.5RR**: 20590.22 ❌
- **TP 5RR**: 20566.45 ❌
- **PnL**: -47.54 points (-1.0R)
- **MFE**: 6.44 points
- **MAE**: 72.43 points

### Trade #341 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 14:45:00
- **FVG 5m**: 20831.71 - 20841.24
- **Entrée**: 20804.13 @ 2025-03-07 14:46:00
- **Stop Loss**: 20851.67
- **Risk**: 47.54 points
- **TP 1RR**: 20756.59 ❌
- **TP 1.5RR**: 20732.83 ❌
- **TP 2RR**: 20709.06 ❌
- **TP 2.5RR**: 20685.29 ❌
- **TP 3RR**: 20661.52 ❌
- **TP 3.5RR**: 20637.76 ❌
- **TP 4RR**: 20613.99 ❌
- **TP 4.5RR**: 20590.22 ❌
- **TP 5RR**: 20566.45 ❌
- **PnL**: -47.54 points (-1.0R)
- **MFE**: 6.44 points
- **MAE**: 72.43 points

### Trade #342 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-09 20:30:00
- **FVG 5m**: 20650.77 - 20662.11
- **Entrée**: 20713.15 @ 2025-03-09 20:31:00
- **Stop Loss**: 20640.45
- **Risk**: 72.70 points
- **TP 1RR**: 20785.85 ❌
- **TP 1.5RR**: 20822.20 ❌
- **TP 2RR**: 20858.54 ❌
- **TP 2.5RR**: 20894.89 ❌
- **TP 3RR**: 20931.24 ❌
- **TP 3.5RR**: 20967.59 ❌
- **TP 4RR**: 21003.94 ❌
- **TP 4.5RR**: 21040.29 ❌
- **TP 5RR**: 21076.64 ❌
- **PnL**: -72.70 points (-1.0R)
- **MFE**: 67.53 points
- **MAE**: 74.49 points

### Trade #343 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-10 01:00:00
- **FVG 5m**: 20710.57 - 20723.71
- **Entrée**: 20724.49 @ 2025-03-10 01:01:00
- **Stop Loss**: 20700.21
- **Risk**: 24.27 points
- **TP 1RR**: 20748.76 ✅
- **TP 1.5RR**: 20760.90 ✅
- **TP 2RR**: 20773.03 ❌
- **TP 2.5RR**: 20785.17 ❌
- **TP 3RR**: 20797.31 ❌
- **TP 3.5RR**: 20809.44 ❌
- **TP 4RR**: 20821.58 ❌
- **TP 4.5RR**: 20833.72 ❌
- **TP 5RR**: 20845.85 ❌
- **PnL**: -24.27 points (-1.0R)
- **MFE**: 40.21 points
- **MAE**: 36.08 points

### Trade #344 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 02:45:00
- **FVG 5m**: 20046.37 - 20062.35
- **Entrée**: 20066.22 @ 2025-03-11 02:55:00
- **Stop Loss**: 20036.35
- **Risk**: 29.87 points
- **TP 1RR**: 20096.08 ✅
- **TP 1.5RR**: 20111.02 ✅
- **TP 2RR**: 20125.95 ✅
- **TP 2.5RR**: 20140.89 ✅
- **TP 3RR**: 20155.82 ✅
- **TP 3.5RR**: 20170.76 ✅
- **TP 4RR**: 20185.69 ✅
- **TP 4.5RR**: 20200.63 ❌
- **TP 5RR**: 20215.56 ❌
- **PnL**: -29.87 points (-1.0R)
- **MFE**: 125.26 points
- **MAE**: 50.78 points

### Trade #345 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 03:00:00
- **FVG 5m**: 20046.37 - 20062.35
- **Entrée**: 20086.58 @ 2025-03-11 03:01:00
- **Stop Loss**: 20036.35
- **Risk**: 50.23 points
- **TP 1RR**: 20136.81 ✅
- **TP 1.5RR**: 20161.92 ✅
- **TP 2RR**: 20187.04 ✅
- **TP 2.5RR**: 20212.15 ❌
- **TP 3RR**: 20237.27 ❌
- **TP 3.5RR**: 20262.39 ❌
- **TP 4RR**: 20287.50 ❌
- **TP 4.5RR**: 20312.62 ❌
- **TP 5RR**: 20337.73 ❌
- **PnL**: -50.23 points (-1.0R)
- **MFE**: 104.90 points
- **MAE**: 71.14 points

### Trade #346 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 07:00:00
- **FVG 5m**: 20143.02 - 20159.78
- **Entrée**: 20130.39 @ 2025-03-11 07:09:00
- **Stop Loss**: 20169.86
- **Risk**: 39.46 points
- **TP 1RR**: 20090.93 ✅
- **TP 1.5RR**: 20071.20 ✅
- **TP 2RR**: 20051.47 ✅
- **TP 2.5RR**: 20031.74 ✅
- **TP 3RR**: 20012.01 ✅
- **TP 3.5RR**: 19992.27 ✅
- **TP 4RR**: 19972.54 ❌
- **TP 4.5RR**: 19952.81 ❌
- **TP 5RR**: 19933.08 ❌
- **PnL**: -39.46 points (-1.0R)
- **MFE**: 144.34 points
- **MAE**: 63.40 points

### Trade #347 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 08:30:00
- **FVG 5m**: 20097.14 - 20100.50
- **Entrée**: 20131.94 @ 2025-03-11 08:37:00
- **Stop Loss**: 20087.10
- **Risk**: 44.84 points
- **TP 1RR**: 20176.78 ❌
- **TP 1.5RR**: 20199.21 ❌
- **TP 2RR**: 20221.63 ❌
- **TP 2.5RR**: 20244.05 ❌
- **TP 3RR**: 20266.47 ❌
- **TP 3.5RR**: 20288.89 ❌
- **TP 4RR**: 20311.31 ❌
- **TP 4.5RR**: 20333.74 ❌
- **TP 5RR**: 20356.16 ❌
- **PnL**: -44.84 points (-1.0R)
- **MFE**: 5.67 points
- **MAE**: 49.49 points

### Trade #348 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 08:45:00
- **FVG 5m**: 20063.12 - 20081.94
- **Entrée**: 20061.32 @ 2025-03-11 09:02:00
- **Stop Loss**: 20091.98
- **Risk**: 30.66 points
- **TP 1RR**: 20030.66 ✅
- **TP 1.5RR**: 20015.33 ✅
- **TP 2RR**: 20000.00 ✅
- **TP 2.5RR**: 19984.67 ✅
- **TP 3RR**: 19969.34 ✅
- **TP 3.5RR**: 19954.01 ✅
- **TP 4RR**: 19938.68 ❌
- **TP 4.5RR**: 19923.35 ❌
- **TP 5RR**: 19908.02 ❌
- **PnL**: -30.66 points (-1.0R)
- **MFE**: 108.77 points
- **MAE**: 31.19 points

### Trade #349 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 08:45:00
- **FVG 5m**: 20063.12 - 20081.94
- **Entrée**: 20061.32 @ 2025-03-11 09:02:00
- **Stop Loss**: 20091.98
- **Risk**: 30.66 points
- **TP 1RR**: 20030.66 ✅
- **TP 1.5RR**: 20015.33 ✅
- **TP 2RR**: 20000.00 ✅
- **TP 2.5RR**: 19984.67 ✅
- **TP 3RR**: 19969.34 ✅
- **TP 3.5RR**: 19954.01 ✅
- **TP 4RR**: 19938.68 ❌
- **TP 4.5RR**: 19923.35 ❌
- **TP 5RR**: 19908.02 ❌
- **PnL**: -30.66 points (-1.0R)
- **MFE**: 108.77 points
- **MAE**: 31.19 points

### Trade #350 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 12:30:00
- **FVG 5m**: 19850.23 - 19868.79
- **Entrée**: 19881.67 @ 2025-03-11 12:41:00
- **Stop Loss**: 19840.30
- **Risk**: 41.37 points
- **TP 1RR**: 19923.04 ✅
- **TP 1.5RR**: 19943.73 ✅
- **TP 2RR**: 19964.41 ✅
- **TP 2.5RR**: 19985.10 ✅
- **TP 3RR**: 20005.78 ✅
- **TP 3.5RR**: 20026.47 ✅
- **TP 4RR**: 20047.15 ✅
- **TP 4.5RR**: 20067.84 ✅
- **TP 5RR**: 20088.52 ✅
- **PnL**: 206.85 points (5.0R)
- **MFE**: 210.32 points
- **MAE**: 21.65 points

### Trade #351 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 14:00:00
- **FVG 5m**: 20216.74 - 20221.12
- **Entrée**: 20170.86 @ 2025-03-11 14:02:00
- **Stop Loss**: 20231.23
- **Risk**: 60.37 points
- **TP 1RR**: 20110.49 ❌
- **TP 1.5RR**: 20080.30 ❌
- **TP 2RR**: 20050.12 ❌
- **TP 2.5RR**: 20019.93 ❌
- **TP 3RR**: 19989.75 ❌
- **TP 3.5RR**: 19959.56 ❌
- **TP 4RR**: 19929.38 ❌
- **TP 4.5RR**: 19899.19 ❌
- **TP 5RR**: 19869.01 ❌
- **PnL**: -60.37 points (-1.0R)
- **MFE**: 3.61 points
- **MAE**: 77.84 points

### Trade #352 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 14:30:00
- **FVG 5m**: 20216.74 - 20221.12
- **Entrée**: 20161.84 @ 2025-03-11 14:31:00
- **Stop Loss**: 20231.23
- **Risk**: 69.39 points
- **TP 1RR**: 20092.45 ✅
- **TP 1.5RR**: 20057.75 ✅
- **TP 2RR**: 20023.06 ✅
- **TP 2.5RR**: 19988.36 ✅
- **TP 3RR**: 19953.66 ❌
- **TP 3.5RR**: 19918.97 ❌
- **TP 4RR**: 19884.27 ❌
- **TP 4.5RR**: 19849.58 ❌
- **TP 5RR**: 19814.88 ❌
- **PnL**: -69.39 points (-1.0R)
- **MFE**: 190.21 points
- **MAE**: 239.70 points

### Trade #353 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-12 02:30:00
- **FVG 5m**: 20018.28 - 20028.07
- **Entrée**: 20028.59 @ 2025-03-12 02:33:00
- **Stop Loss**: 20008.27
- **Risk**: 20.32 points
- **TP 1RR**: 20048.90 ❌
- **TP 1.5RR**: 20059.06 ❌
- **TP 2RR**: 20069.22 ❌
- **TP 2.5RR**: 20079.38 ❌
- **TP 3RR**: 20089.54 ❌
- **TP 3.5RR**: 20099.70 ❌
- **TP 4RR**: 20109.86 ❌
- **TP 4.5RR**: 20120.02 ❌
- **TP 5RR**: 20130.18 ❌
- **PnL**: -20.32 points (-1.0R)
- **MFE**: 0.00 points
- **MAE**: 31.19 points

### Trade #354 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-12 03:00:00
- **FVG 5m**: 20062.35 - 20071.37
- **Entrée**: 20058.23 @ 2025-03-12 03:13:00
- **Stop Loss**: 20081.41
- **Risk**: 23.18 points
- **TP 1RR**: 20035.04 ❌
- **TP 1.5RR**: 20023.45 ❌
- **TP 2RR**: 20011.86 ❌
- **TP 2.5RR**: 20000.27 ❌
- **TP 3RR**: 19988.68 ❌
- **TP 3.5RR**: 19977.09 ❌
- **TP 4RR**: 19965.50 ❌
- **TP 4.5RR**: 19953.91 ❌
- **TP 5RR**: 19942.32 ❌
- **PnL**: -23.18 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 26.29 points

### Trade #355 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-12 03:00:00
- **FVG 5m**: 20062.35 - 20071.37
- **Entrée**: 20058.23 @ 2025-03-12 03:13:00
- **Stop Loss**: 20081.41
- **Risk**: 23.18 points
- **TP 1RR**: 20035.04 ❌
- **TP 1.5RR**: 20023.45 ❌
- **TP 2RR**: 20011.86 ❌
- **TP 2.5RR**: 20000.27 ❌
- **TP 3RR**: 19988.68 ❌
- **TP 3.5RR**: 19977.09 ❌
- **TP 4RR**: 19965.50 ❌
- **TP 4.5RR**: 19953.91 ❌
- **TP 5RR**: 19942.32 ❌
- **PnL**: -23.18 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 26.29 points

### Trade #356 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-12 09:45:00
- **FVG 5m**: 20304.88 - 20310.04
- **Entrée**: 20121.89 @ 2025-03-12 09:46:00
- **Stop Loss**: 20320.19
- **Risk**: 198.31 points
- **TP 1RR**: 19923.58 ❌
- **TP 1.5RR**: 19824.43 ❌
- **TP 2RR**: 19725.27 ❌
- **TP 2.5RR**: 19626.12 ❌
- **TP 3RR**: 19526.97 ❌
- **TP 3.5RR**: 19427.82 ❌
- **TP 4RR**: 19328.66 ❌
- **TP 4.5RR**: 19229.51 ❌
- **TP 5RR**: 19130.36 ❌
- **PnL**: -198.31 points (-1.0R)
- **MFE**: 126.04 points
- **MAE**: 200.52 points

### Trade #357 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 04:30:00
- **FVG 5m**: 20038.64 - 20043.79
- **Entrée**: 20149.21 @ 2025-03-13 04:31:00
- **Stop Loss**: 20028.62
- **Risk**: 120.59 points
- **TP 1RR**: 20269.80 ❌
- **TP 1.5RR**: 20330.09 ❌
- **TP 2RR**: 20390.39 ❌
- **TP 2.5RR**: 20450.68 ❌
- **TP 3RR**: 20510.98 ❌
- **TP 3.5RR**: 20571.27 ❌
- **TP 4RR**: 20631.57 ❌
- **TP 4.5RR**: 20691.87 ❌
- **TP 5RR**: 20752.16 ❌
- **PnL**: -120.59 points (-1.0R)
- **MFE**: 89.69 points
- **MAE**: 121.40 points

### Trade #358 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-13 07:00:00
- **FVG 5m**: 20200.24 - 20204.88
- **Entrée**: 20130.65 @ 2025-03-13 07:01:00
- **Stop Loss**: 20214.98
- **Risk**: 84.33 points
- **TP 1RR**: 20046.32 ✅
- **TP 1.5RR**: 20004.15 ✅
- **TP 2RR**: 19961.99 ✅
- **TP 2.5RR**: 19919.82 ✅
- **TP 3RR**: 19877.65 ✅
- **TP 3.5RR**: 19835.49 ✅
- **TP 4RR**: 19793.32 ✅
- **TP 4.5RR**: 19751.16 ❌
- **TP 5RR**: 19708.99 ❌
- **PnL**: -84.33 points (-1.0R)
- **MFE**: 367.02 points
- **MAE**: 94.08 points

### Trade #359 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20018.79 - 20061.06
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20008.78
- **Risk**: 71.61 points
- **TP 1RR**: 20152.00 ✅
- **TP 1.5RR**: 20187.81 ❌
- **TP 2RR**: 20223.61 ❌
- **TP 2.5RR**: 20259.42 ❌
- **TP 3RR**: 20295.22 ❌
- **TP 3.5RR**: 20331.02 ❌
- **TP 4RR**: 20366.83 ❌
- **TP 4.5RR**: 20402.63 ❌
- **TP 5RR**: 20438.44 ❌
- **PnL**: -71.61 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 77.58 points

### Trade #360 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20018.79 - 20061.06
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20008.78
- **Risk**: 71.61 points
- **TP 1RR**: 20152.00 ✅
- **TP 1.5RR**: 20187.81 ❌
- **TP 2RR**: 20223.61 ❌
- **TP 2.5RR**: 20259.42 ❌
- **TP 3RR**: 20295.22 ❌
- **TP 3.5RR**: 20331.02 ❌
- **TP 4RR**: 20366.83 ❌
- **TP 4.5RR**: 20402.63 ❌
- **TP 5RR**: 20438.44 ❌
- **PnL**: -71.61 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 77.58 points

### Trade #361 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20018.79 - 20061.06
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20008.78
- **Risk**: 71.61 points
- **TP 1RR**: 20152.00 ✅
- **TP 1.5RR**: 20187.81 ❌
- **TP 2RR**: 20223.61 ❌
- **TP 2.5RR**: 20259.42 ❌
- **TP 3RR**: 20295.22 ❌
- **TP 3.5RR**: 20331.02 ❌
- **TP 4RR**: 20366.83 ❌
- **TP 4.5RR**: 20402.63 ❌
- **TP 5RR**: 20438.44 ❌
- **PnL**: -71.61 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 77.58 points

### Trade #362 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20018.79 - 20061.06
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20008.78
- **Risk**: 71.61 points
- **TP 1RR**: 20152.00 ✅
- **TP 1.5RR**: 20187.81 ❌
- **TP 2RR**: 20223.61 ❌
- **TP 2.5RR**: 20259.42 ❌
- **TP 3RR**: 20295.22 ❌
- **TP 3.5RR**: 20331.02 ❌
- **TP 4RR**: 20366.83 ❌
- **TP 4.5RR**: 20402.63 ❌
- **TP 5RR**: 20438.44 ❌
- **PnL**: -71.61 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 77.58 points

### Trade #363 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20018.79 - 20061.06
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20008.78
- **Risk**: 71.61 points
- **TP 1RR**: 20152.00 ✅
- **TP 1.5RR**: 20187.81 ❌
- **TP 2RR**: 20223.61 ❌
- **TP 2.5RR**: 20259.42 ❌
- **TP 3RR**: 20295.22 ❌
- **TP 3.5RR**: 20331.02 ❌
- **TP 4RR**: 20366.83 ❌
- **TP 4.5RR**: 20402.63 ❌
- **TP 5RR**: 20438.44 ❌
- **PnL**: -71.61 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 77.58 points

### Trade #364 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20018.79 - 20061.06
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20008.78
- **Risk**: 71.61 points
- **TP 1RR**: 20152.00 ✅
- **TP 1.5RR**: 20187.81 ❌
- **TP 2RR**: 20223.61 ❌
- **TP 2.5RR**: 20259.42 ❌
- **TP 3RR**: 20295.22 ❌
- **TP 3.5RR**: 20331.02 ❌
- **TP 4RR**: 20366.83 ❌
- **TP 4.5RR**: 20402.63 ❌
- **TP 5RR**: 20438.44 ❌
- **PnL**: -71.61 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 77.58 points

### Trade #365 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 08:45:00
- **FVG 5m**: 20085.80 - 20134.52
- **Entrée**: 20078.84 @ 2025-03-14 09:12:00
- **Stop Loss**: 20144.58
- **Risk**: 65.74 points
- **TP 1RR**: 20013.11 ❌
- **TP 1.5RR**: 19980.24 ❌
- **TP 2RR**: 19947.37 ❌
- **TP 2.5RR**: 19914.50 ❌
- **TP 3RR**: 19881.63 ❌
- **TP 3.5RR**: 19848.76 ❌
- **TP 4RR**: 19815.89 ❌
- **TP 4.5RR**: 19783.02 ❌
- **TP 5RR**: 19750.15 ❌
- **PnL**: -65.74 points (-1.0R)
- **MFE**: 31.44 points
- **MAE**: 78.61 points

### Trade #366 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 11:45:00
- **FVG 5m**: 20244.31 - 20262.36
- **Entrée**: 20240.19 @ 2025-03-14 12:36:00
- **Stop Loss**: 20272.49
- **Risk**: 32.30 points
- **TP 1RR**: 20207.89 ❌
- **TP 1.5RR**: 20191.75 ❌
- **TP 2RR**: 20175.60 ❌
- **TP 2.5RR**: 20159.45 ❌
- **TP 3RR**: 20143.30 ❌
- **TP 3.5RR**: 20127.15 ❌
- **TP 4RR**: 20111.00 ❌
- **TP 4.5RR**: 20094.85 ❌
- **TP 5RR**: 20078.71 ❌
- **PnL**: -32.30 points (-1.0R)
- **MFE**: 12.89 points
- **MAE**: 35.05 points

### Trade #367 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 14:45:00
- **FVG 5m**: 20275.76 - 20279.37
- **Entrée**: 20275.24 @ 2025-03-14 15:05:00
- **Stop Loss**: 20289.51
- **Risk**: 14.26 points
- **TP 1RR**: 20260.98 ✅
- **TP 1.5RR**: 20253.85 ✅
- **TP 2RR**: 20246.72 ❌
- **TP 2.5RR**: 20239.58 ❌
- **TP 3RR**: 20232.45 ❌
- **TP 3.5RR**: 20225.32 ❌
- **TP 4RR**: 20218.19 ❌
- **TP 4.5RR**: 20211.06 ❌
- **TP 5RR**: 20203.93 ❌
- **PnL**: -14.26 points (-1.0R)
- **MFE**: 26.29 points
- **MAE**: 20.62 points

### Trade #368 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 14:45:00
- **FVG 5m**: 20275.76 - 20279.37
- **Entrée**: 20275.24 @ 2025-03-14 15:05:00
- **Stop Loss**: 20289.51
- **Risk**: 14.26 points
- **TP 1RR**: 20260.98 ✅
- **TP 1.5RR**: 20253.85 ✅
- **TP 2RR**: 20246.72 ❌
- **TP 2.5RR**: 20239.58 ❌
- **TP 3RR**: 20232.45 ❌
- **TP 3.5RR**: 20225.32 ❌
- **TP 4RR**: 20218.19 ❌
- **TP 4.5RR**: 20211.06 ❌
- **TP 5RR**: 20203.93 ❌
- **PnL**: -14.26 points (-1.0R)
- **MFE**: 26.29 points
- **MAE**: 20.62 points

### Trade #369 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-17 02:45:00
- **FVG 5m**: 20172.92 - 20174.98
- **Entrée**: 20181.94 @ 2025-03-17 02:46:00
- **Stop Loss**: 20162.83
- **Risk**: 19.11 points
- **TP 1RR**: 20201.05 ✅
- **TP 1.5RR**: 20210.60 ✅
- **TP 2RR**: 20220.16 ✅
- **TP 2.5RR**: 20229.71 ✅
- **TP 3RR**: 20239.26 ✅
- **TP 3.5RR**: 20248.82 ✅
- **TP 4RR**: 20258.37 ✅
- **TP 4.5RR**: 20267.92 ✅
- **TP 5RR**: 20277.48 ✅
- **PnL**: 95.54 points (5.0R)
- **MFE**: 96.65 points
- **MAE**: 6.70 points

### Trade #370 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-17 08:00:00
- **FVG 5m**: 20361.07 - 20365.45
- **Entrée**: 20340.71 @ 2025-03-17 08:01:00
- **Stop Loss**: 20375.64
- **Risk**: 34.93 points
- **TP 1RR**: 20305.78 ✅
- **TP 1.5RR**: 20288.32 ❌
- **TP 2RR**: 20270.86 ❌
- **TP 2.5RR**: 20253.40 ❌
- **TP 3RR**: 20235.93 ❌
- **TP 3.5RR**: 20218.47 ❌
- **TP 4RR**: 20201.01 ❌
- **TP 4.5RR**: 20183.54 ❌
- **TP 5RR**: 20166.08 ❌
- **PnL**: -34.93 points (-1.0R)
- **MFE**: 47.94 points
- **MAE**: 44.85 points

### Trade #371 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-17 09:15:00
- **FVG 5m**: 20371.90 - 20418.81
- **Entrée**: 20359.01 @ 2025-03-17 09:27:00
- **Stop Loss**: 20429.02
- **Risk**: 70.01 points
- **TP 1RR**: 20289.00 ✅
- **TP 1.5RR**: 20254.00 ✅
- **TP 2RR**: 20219.00 ❌
- **TP 2.5RR**: 20184.00 ❌
- **TP 3RR**: 20148.99 ❌
- **TP 3.5RR**: 20113.99 ❌
- **TP 4RR**: 20078.99 ❌
- **TP 4.5RR**: 20043.99 ❌
- **TP 5RR**: 20008.98 ❌
- **PnL**: -70.01 points (-1.0R)
- **MFE**: 122.43 points
- **MAE**: 72.68 points

### Trade #372 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-17 14:45:00
- **FVG 5m**: 20517.78 - 20526.54
- **Entrée**: 20508.76 @ 2025-03-17 14:50:00
- **Stop Loss**: 20536.81
- **Risk**: 28.05 points
- **TP 1RR**: 20480.71 ✅
- **TP 1.5RR**: 20466.69 ✅
- **TP 2RR**: 20452.66 ✅
- **TP 2.5RR**: 20438.64 ✅
- **TP 3RR**: 20424.62 ✅
- **TP 3.5RR**: 20410.59 ✅
- **TP 4RR**: 20396.57 ✅
- **TP 4.5RR**: 20382.54 ✅
- **TP 5RR**: 20368.52 ✅
- **PnL**: 140.24 points (5.0R)
- **MFE**: 140.73 points
- **MAE**: 7.47 points

### Trade #373 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-18 08:30:00
- **FVG 5m**: 20366.65 - 20370.22
- **Entrée**: 20258.26 @ 2025-03-18 08:31:00
- **Stop Loss**: 20380.41
- **Risk**: 122.14 points
- **TP 1RR**: 20136.12 ✅
- **TP 1.5RR**: 20075.05 ✅
- **TP 2RR**: 20013.98 ✅
- **TP 2.5RR**: 19952.91 ❌
- **TP 3RR**: 19891.84 ❌
- **TP 3.5RR**: 19830.77 ❌
- **TP 4RR**: 19769.70 ❌
- **TP 4.5RR**: 19708.63 ❌
- **TP 5RR**: 19647.56 ❌
- **PnL**: -122.14 points (-1.0R)
- **MFE**: 259.87 points
- **MAE**: 124.20 points

### Trade #374 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-18 19:30:00
- **FVG 5m**: 20096.58 - 20106.52
- **Entrée**: 20157.78 @ 2025-03-18 19:31:00
- **Stop Loss**: 20086.53
- **Risk**: 71.25 points
- **TP 1RR**: 20229.04 ❌
- **TP 1.5RR**: 20264.66 ❌
- **TP 2RR**: 20300.29 ❌
- **TP 2.5RR**: 20335.92 ❌
- **TP 3RR**: 20371.55 ❌
- **TP 3.5RR**: 20407.17 ❌
- **TP 4RR**: 20442.80 ❌
- **TP 4.5RR**: 20478.43 ❌
- **TP 5RR**: 20514.06 ❌
- **PnL**: -71.25 points (-1.0R)
- **MFE**: 37.74 points
- **MAE**: 78.04 points

### Trade #375 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 04:45:00
- **FVG 5m**: 20085.36 - 20109.58
- **Entrée**: 20150.90 @ 2025-03-19 04:46:00
- **Stop Loss**: 20075.31
- **Risk**: 75.58 points
- **TP 1RR**: 20226.48 ✅
- **TP 1.5RR**: 20264.27 ✅
- **TP 2RR**: 20302.07 ✅
- **TP 2.5RR**: 20339.86 ✅
- **TP 3RR**: 20377.65 ✅
- **TP 3.5RR**: 20415.44 ✅
- **TP 4RR**: 20453.24 ✅
- **TP 4.5RR**: 20491.03 ✅
- **TP 5RR**: 20528.82 ✅
- **PnL**: 377.92 points (5.0R)
- **MFE**: 383.05 points
- **MAE**: 48.45 points

### Trade #376 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 08:30:00
- **FVG 5m**: 20169.26 - 20173.34
- **Entrée**: 20168.75 @ 2025-03-19 08:34:00
- **Stop Loss**: 20183.43
- **Risk**: 14.68 points
- **TP 1RR**: 20154.07 ❌
- **TP 1.5RR**: 20146.73 ❌
- **TP 2RR**: 20139.39 ❌
- **TP 2.5RR**: 20132.06 ❌
- **TP 3RR**: 20124.72 ❌
- **TP 3.5RR**: 20117.38 ❌
- **TP 4RR**: 20110.04 ❌
- **TP 4.5RR**: 20102.70 ❌
- **TP 5RR**: 20095.36 ❌
- **PnL**: -14.68 points (-1.0R)
- **MFE**: 2.30 points
- **MAE**: 17.34 points

### Trade #377 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 08:30:00
- **FVG 5m**: 20169.26 - 20173.34
- **Entrée**: 20168.75 @ 2025-03-19 08:34:00
- **Stop Loss**: 20183.43
- **Risk**: 14.68 points
- **TP 1RR**: 20154.07 ❌
- **TP 1.5RR**: 20146.73 ❌
- **TP 2RR**: 20139.39 ❌
- **TP 2.5RR**: 20132.06 ❌
- **TP 3RR**: 20124.72 ❌
- **TP 3.5RR**: 20117.38 ❌
- **TP 4RR**: 20110.04 ❌
- **TP 4.5RR**: 20102.70 ❌
- **TP 5RR**: 20095.36 ❌
- **PnL**: -14.68 points (-1.0R)
- **MFE**: 2.30 points
- **MAE**: 17.34 points

### Trade #378 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 11:00:00
- **FVG 5m**: 20305.19 - 20308.25
- **Entrée**: 20302.64 @ 2025-03-19 11:10:00
- **Stop Loss**: 20318.40
- **Risk**: 15.76 points
- **TP 1RR**: 20286.87 ✅
- **TP 1.5RR**: 20278.99 ✅
- **TP 2RR**: 20271.11 ✅
- **TP 2.5RR**: 20263.23 ✅
- **TP 3RR**: 20255.34 ✅
- **TP 3.5RR**: 20247.46 ✅
- **TP 4RR**: 20239.58 ✅
- **TP 4.5RR**: 20231.70 ✅
- **TP 5RR**: 20223.81 ✅
- **PnL**: 78.82 points (5.0R)
- **MFE**: 81.35 points
- **MAE**: 10.97 points

### Trade #379 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 13:30:00
- **FVG 5m**: 20228.43 - 20233.78
- **Entrée**: 20328.14 @ 2025-03-19 13:31:00
- **Stop Loss**: 20218.31
- **Risk**: 109.83 points
- **TP 1RR**: 20437.97 ✅
- **TP 1.5RR**: 20492.88 ✅
- **TP 2RR**: 20547.80 ✅
- **TP 2.5RR**: 20602.71 ❌
- **TP 3RR**: 20657.63 ❌
- **TP 3.5RR**: 20712.54 ❌
- **TP 4RR**: 20767.46 ❌
- **TP 4.5RR**: 20822.37 ❌
- **TP 5RR**: 20877.29 ❌
- **PnL**: -109.83 points (-1.0R)
- **MFE**: 219.83 points
- **MAE**: 114.00 points

### Trade #380 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 13:30:00
- **FVG 5m**: 20228.43 - 20233.78
- **Entrée**: 20328.14 @ 2025-03-19 13:31:00
- **Stop Loss**: 20218.31
- **Risk**: 109.83 points
- **TP 1RR**: 20437.97 ✅
- **TP 1.5RR**: 20492.88 ✅
- **TP 2RR**: 20547.80 ✅
- **TP 2.5RR**: 20602.71 ❌
- **TP 3RR**: 20657.63 ❌
- **TP 3.5RR**: 20712.54 ❌
- **TP 4RR**: 20767.46 ❌
- **TP 4.5RR**: 20822.37 ❌
- **TP 5RR**: 20877.29 ❌
- **PnL**: -109.83 points (-1.0R)
- **MFE**: 219.83 points
- **MAE**: 114.00 points

### Trade #381 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 14:15:00
- **FVG 5m**: 20432.45 - 20455.14
- **Entrée**: 20424.80 @ 2025-03-19 14:22:00
- **Stop Loss**: 20465.37
- **Risk**: 40.58 points
- **TP 1RR**: 20384.22 ✅
- **TP 1.5RR**: 20363.93 ✅
- **TP 2RR**: 20343.64 ✅
- **TP 2.5RR**: 20323.36 ❌
- **TP 3RR**: 20303.07 ❌
- **TP 3.5RR**: 20282.78 ❌
- **TP 4RR**: 20262.49 ❌
- **TP 4.5RR**: 20242.20 ❌
- **TP 5RR**: 20221.92 ❌
- **PnL**: -40.58 points (-1.0R)
- **MFE**: 89.26 points
- **MAE**: 57.13 points

### Trade #382 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 14:15:00
- **FVG 5m**: 20432.45 - 20455.14
- **Entrée**: 20424.80 @ 2025-03-19 14:22:00
- **Stop Loss**: 20465.37
- **Risk**: 40.58 points
- **TP 1RR**: 20384.22 ✅
- **TP 1.5RR**: 20363.93 ✅
- **TP 2RR**: 20343.64 ✅
- **TP 2.5RR**: 20323.36 ❌
- **TP 3RR**: 20303.07 ❌
- **TP 3.5RR**: 20282.78 ❌
- **TP 4RR**: 20262.49 ❌
- **TP 4.5RR**: 20242.20 ❌
- **TP 5RR**: 20221.92 ❌
- **PnL**: -40.58 points (-1.0R)
- **MFE**: 89.26 points
- **MAE**: 57.13 points

### Trade #383 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-20 09:15:00
- **FVG 5m**: 20212.87 - 20225.88
- **Entrée**: 20424.80 @ 2025-03-20 09:16:00
- **Stop Loss**: 20202.76
- **Risk**: 222.03 points
- **TP 1RR**: 20646.83 ❌
- **TP 1.5RR**: 20757.85 ❌
- **TP 2RR**: 20868.86 ❌
- **TP 2.5RR**: 20979.88 ❌
- **TP 3RR**: 21090.90 ❌
- **TP 3.5RR**: 21201.91 ❌
- **TP 4RR**: 21312.93 ❌
- **TP 4.5RR**: 21423.95 ❌
- **TP 5RR**: 21534.96 ❌
- **PnL**: -222.03 points (-1.0R)
- **MFE**: 84.41 points
- **MAE**: 222.89 points

### Trade #384 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 09:45:00
- **FVG 5m**: 20448.26 - 20452.59
- **Entrée**: 20446.47 @ 2025-03-20 09:59:00
- **Stop Loss**: 20462.82
- **Risk**: 16.35 points
- **TP 1RR**: 20430.13 ✅
- **TP 1.5RR**: 20421.95 ✅
- **TP 2RR**: 20413.78 ✅
- **TP 2.5RR**: 20405.61 ❌
- **TP 3RR**: 20397.43 ❌
- **TP 3.5RR**: 20389.26 ❌
- **TP 4RR**: 20381.09 ❌
- **TP 4.5RR**: 20372.91 ❌
- **TP 5RR**: 20364.74 ❌
- **PnL**: -16.35 points (-1.0R)
- **MFE**: 35.19 points
- **MAE**: 17.09 points

### Trade #385 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 12:15:00
- **FVG 5m**: 20302.64 - 20307.74
- **Entrée**: 20301.62 @ 2025-03-20 12:16:00
- **Stop Loss**: 20317.89
- **Risk**: 16.27 points
- **TP 1RR**: 20285.34 ✅
- **TP 1.5RR**: 20277.21 ✅
- **TP 2RR**: 20269.07 ✅
- **TP 2.5RR**: 20260.93 ✅
- **TP 3RR**: 20252.79 ✅
- **TP 3.5RR**: 20244.66 ✅
- **TP 4RR**: 20236.52 ✅
- **TP 4.5RR**: 20228.38 ✅
- **TP 5RR**: 20220.25 ✅
- **PnL**: 81.37 points (5.0R)
- **MFE**: 86.96 points
- **MAE**: 12.50 points

### Trade #386 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 00:45:00
- **FVG 5m**: 20245.51 - 20262.34
- **Entrée**: 20262.60 @ 2025-03-21 01:36:00
- **Stop Loss**: 20235.39
- **Risk**: 27.21 points
- **TP 1RR**: 20289.81 ✅
- **TP 1.5RR**: 20303.41 ❌
- **TP 2RR**: 20317.02 ❌
- **TP 2.5RR**: 20330.62 ❌
- **TP 3RR**: 20344.23 ❌
- **TP 3.5RR**: 20357.83 ❌
- **TP 4RR**: 20371.44 ❌
- **TP 4.5RR**: 20385.04 ❌
- **TP 5RR**: 20398.65 ❌
- **PnL**: -27.21 points (-1.0R)
- **MFE**: 34.43 points
- **MAE**: 28.05 points

### Trade #387 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 01:30:00
- **FVG 5m**: 20245.51 - 20262.34
- **Entrée**: 20262.60 @ 2025-03-21 01:36:00
- **Stop Loss**: 20235.39
- **Risk**: 27.21 points
- **TP 1RR**: 20289.81 ✅
- **TP 1.5RR**: 20303.41 ❌
- **TP 2RR**: 20317.02 ❌
- **TP 2.5RR**: 20330.62 ❌
- **TP 3RR**: 20344.23 ❌
- **TP 3.5RR**: 20357.83 ❌
- **TP 4RR**: 20371.44 ❌
- **TP 4.5RR**: 20385.04 ❌
- **TP 5RR**: 20398.65 ❌
- **PnL**: -27.21 points (-1.0R)
- **MFE**: 34.43 points
- **MAE**: 28.05 points

### Trade #388 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 05:00:00
- **FVG 5m**: 20200.37 - 20202.92
- **Entrée**: 20211.85 @ 2025-03-21 05:01:00
- **Stop Loss**: 20190.27
- **Risk**: 21.58 points
- **TP 1RR**: 20233.43 ✅
- **TP 1.5RR**: 20244.21 ✅
- **TP 2RR**: 20255.00 ❌
- **TP 2.5RR**: 20265.79 ❌
- **TP 3RR**: 20276.58 ❌
- **TP 3.5RR**: 20287.37 ❌
- **TP 4RR**: 20298.15 ❌
- **TP 4.5RR**: 20308.94 ❌
- **TP 5RR**: 20319.73 ❌
- **PnL**: -21.58 points (-1.0R)
- **MFE**: 32.39 points
- **MAE**: 28.82 points

### Trade #389 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 08:30:00
- **FVG 5m**: 20078.21 - 20080.51
- **Entrée**: 20090.71 @ 2025-03-21 08:42:00
- **Stop Loss**: 20068.18
- **Risk**: 22.54 points
- **TP 1RR**: 20113.25 ❌
- **TP 1.5RR**: 20124.51 ❌
- **TP 2RR**: 20135.78 ❌
- **TP 2.5RR**: 20147.05 ❌
- **TP 3RR**: 20158.32 ❌
- **TP 3.5RR**: 20169.59 ❌
- **TP 4RR**: 20180.85 ❌
- **TP 4.5RR**: 20192.12 ❌
- **TP 5RR**: 20203.39 ❌
- **PnL**: -22.54 points (-1.0R)
- **MFE**: 7.91 points
- **MAE**: 23.46 points

### Trade #390 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 08:30:00
- **FVG 5m**: 20078.21 - 20080.51
- **Entrée**: 20090.71 @ 2025-03-21 08:42:00
- **Stop Loss**: 20068.18
- **Risk**: 22.54 points
- **TP 1RR**: 20113.25 ❌
- **TP 1.5RR**: 20124.51 ❌
- **TP 2RR**: 20135.78 ❌
- **TP 2.5RR**: 20147.05 ❌
- **TP 3RR**: 20158.32 ❌
- **TP 3.5RR**: 20169.59 ❌
- **TP 4RR**: 20180.85 ❌
- **TP 4.5RR**: 20192.12 ❌
- **TP 5RR**: 20203.39 ❌
- **PnL**: -22.54 points (-1.0R)
- **MFE**: 7.91 points
- **MAE**: 23.46 points

### Trade #391 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 08:45:00
- **FVG 5m**: 20078.21 - 20080.51
- **Entrée**: 20087.65 @ 2025-03-21 08:46:00
- **Stop Loss**: 20068.18
- **Risk**: 19.48 points
- **TP 1RR**: 20107.13 ✅
- **TP 1.5RR**: 20116.86 ✅
- **TP 2RR**: 20126.60 ✅
- **TP 2.5RR**: 20136.34 ✅
- **TP 3RR**: 20146.08 ✅
- **TP 3.5RR**: 20155.81 ❌
- **TP 4RR**: 20165.55 ❌
- **TP 4.5RR**: 20175.29 ❌
- **TP 5RR**: 20185.03 ❌
- **PnL**: -19.48 points (-1.0R)
- **MFE**: 61.72 points
- **MAE**: 19.89 points

### Trade #392 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 09:15:00
- **FVG 5m**: 20078.21 - 20080.51
- **Entrée**: 20102.44 @ 2025-03-21 09:16:00
- **Stop Loss**: 20068.18
- **Risk**: 34.27 points
- **TP 1RR**: 20136.71 ✅
- **TP 1.5RR**: 20153.84 ✅
- **TP 2RR**: 20170.98 ✅
- **TP 2.5RR**: 20188.11 ✅
- **TP 3RR**: 20205.24 ✅
- **TP 3.5RR**: 20222.38 ✅
- **TP 4RR**: 20239.51 ✅
- **TP 4.5RR**: 20256.64 ✅
- **TP 5RR**: 20273.78 ✅
- **PnL**: 171.33 points (5.0R)
- **MFE**: 184.64 points
- **MAE**: 27.54 points

### Trade #393 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 09:45:00
- **FVG 5m**: 20078.21 - 20080.51
- **Entrée**: 20137.64 @ 2025-03-21 09:46:00
- **Stop Loss**: 20068.18
- **Risk**: 69.46 points
- **TP 1RR**: 20207.10 ✅
- **TP 1.5RR**: 20241.83 ✅
- **TP 2RR**: 20276.56 ✅
- **TP 2.5RR**: 20311.29 ✅
- **TP 3RR**: 20346.02 ✅
- **TP 3.5RR**: 20380.75 ✅
- **TP 4RR**: 20415.48 ✅
- **TP 4.5RR**: 20450.21 ✅
- **TP 5RR**: 20484.94 ✅
- **PnL**: 347.30 points (5.0R)
- **MFE**: 365.45 points
- **MAE**: 62.74 points

### Trade #394 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 09:45:00
- **FVG 5m**: 20078.21 - 20080.51
- **Entrée**: 20137.64 @ 2025-03-21 09:46:00
- **Stop Loss**: 20068.18
- **Risk**: 69.46 points
- **TP 1RR**: 20207.10 ✅
- **TP 1.5RR**: 20241.83 ✅
- **TP 2RR**: 20276.56 ✅
- **TP 2.5RR**: 20311.29 ✅
- **TP 3RR**: 20346.02 ✅
- **TP 3.5RR**: 20380.75 ✅
- **TP 4RR**: 20415.48 ✅
- **TP 4.5RR**: 20450.21 ✅
- **TP 5RR**: 20484.94 ✅
- **PnL**: 347.30 points (5.0R)
- **MFE**: 365.45 points
- **MAE**: 62.74 points

### Trade #395 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-23 20:30:00
- **FVG 5m**: 20519.16 - 20525.79
- **Entrée**: 20511.50 @ 2025-03-23 20:31:00
- **Stop Loss**: 20536.05
- **Risk**: 24.54 points
- **TP 1RR**: 20486.96 ❌
- **TP 1.5RR**: 20474.69 ❌
- **TP 2RR**: 20462.42 ❌
- **TP 2.5RR**: 20450.14 ❌
- **TP 3RR**: 20437.87 ❌
- **TP 3.5RR**: 20425.60 ❌
- **TP 4RR**: 20413.33 ❌
- **TP 4.5RR**: 20401.05 ❌
- **TP 5RR**: 20388.78 ❌
- **PnL**: -24.54 points (-1.0R)
- **MFE**: 11.48 points
- **MAE**: 24.74 points

### Trade #396 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 08:15:00
- **FVG 5m**: 20682.63 - 20685.94
- **Entrée**: 20681.35 @ 2025-03-24 08:16:00
- **Stop Loss**: 20696.29
- **Risk**: 14.93 points
- **TP 1RR**: 20666.42 ✅
- **TP 1.5RR**: 20658.95 ✅
- **TP 2RR**: 20651.49 ✅
- **TP 2.5RR**: 20644.02 ✅
- **TP 3RR**: 20636.55 ✅
- **TP 3.5RR**: 20629.08 ❌
- **TP 4RR**: 20621.62 ❌
- **TP 4.5RR**: 20614.15 ❌
- **TP 5RR**: 20606.68 ❌
- **PnL**: -14.93 points (-1.0R)
- **MFE**: 45.39 points
- **MAE**: 16.07 points

### Trade #397 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 11:15:00
- **FVG 5m**: 20767.55 - 20770.87
- **Entrée**: 20761.69 @ 2025-03-24 11:25:00
- **Stop Loss**: 20781.25
- **Risk**: 19.57 points
- **TP 1RR**: 20742.12 ✅
- **TP 1.5RR**: 20732.34 ✅
- **TP 2RR**: 20722.55 ✅
- **TP 2.5RR**: 20712.77 ❌
- **TP 3RR**: 20702.99 ❌
- **TP 3.5RR**: 20693.20 ❌
- **TP 4RR**: 20683.42 ❌
- **TP 4.5RR**: 20673.64 ❌
- **TP 5RR**: 20663.85 ❌
- **PnL**: -19.57 points (-1.0R)
- **MFE**: 45.14 points
- **MAE**: 20.66 points

### Trade #398 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 14:15:00
- **FVG 5m**: 20778.77 - 20784.38
- **Entrée**: 20777.24 @ 2025-03-24 14:30:00
- **Stop Loss**: 20794.77
- **Risk**: 17.53 points
- **TP 1RR**: 20759.71 ❌
- **TP 1.5RR**: 20750.94 ❌
- **TP 2RR**: 20742.18 ❌
- **TP 2.5RR**: 20733.41 ❌
- **TP 3RR**: 20724.64 ❌
- **TP 3.5RR**: 20715.88 ❌
- **TP 4RR**: 20707.11 ❌
- **TP 4.5RR**: 20698.34 ❌
- **TP 5RR**: 20689.58 ❌
- **PnL**: -17.53 points (-1.0R)
- **MFE**: 7.14 points
- **MAE**: 21.93 points

### Trade #399 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 14:45:00
- **FVG 5m**: 20778.77 - 20784.38
- **Entrée**: 20775.20 @ 2025-03-24 14:59:00
- **Stop Loss**: 20794.77
- **Risk**: 19.57 points
- **TP 1RR**: 20755.63 ✅
- **TP 1.5RR**: 20745.84 ✅
- **TP 2RR**: 20736.06 ✅
- **TP 2.5RR**: 20726.27 ✅
- **TP 3RR**: 20716.48 ✅
- **TP 3.5RR**: 20706.70 ✅
- **TP 4RR**: 20696.91 ❌
- **TP 4.5RR**: 20687.12 ❌
- **TP 5RR**: 20677.34 ❌
- **PnL**: -19.57 points (-1.0R)
- **MFE**: 74.21 points
- **MAE**: 26.52 points

### Trade #400 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-25 04:30:00
- **FVG 5m**: 20727.26 - 20732.10
- **Entrée**: 20732.87 @ 2025-03-25 04:32:00
- **Stop Loss**: 20716.89
- **Risk**: 15.97 points
- **TP 1RR**: 20748.84 ✅
- **TP 1.5RR**: 20756.83 ✅
- **TP 2RR**: 20764.82 ✅
- **TP 2.5RR**: 20772.80 ✅
- **TP 3RR**: 20780.79 ✅
- **TP 3.5RR**: 20788.78 ✅
- **TP 4RR**: 20796.76 ✅
- **TP 4.5RR**: 20804.75 ✅
- **TP 5RR**: 20812.74 ✅
- **PnL**: 79.87 points (5.0R)
- **MFE**: 81.35 points
- **MAE**: 3.57 points

### Trade #401 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-25 04:45:00
- **FVG 5m**: 20727.26 - 20732.10
- **Entrée**: 20741.03 @ 2025-03-25 04:46:00
- **Stop Loss**: 20716.89
- **Risk**: 24.14 points
- **TP 1RR**: 20765.16 ✅
- **TP 1.5RR**: 20777.23 ✅
- **TP 2RR**: 20789.30 ✅
- **TP 2.5RR**: 20801.37 ✅
- **TP 3RR**: 20813.43 ✅
- **TP 3.5RR**: 20825.50 ✅
- **TP 4RR**: 20837.57 ✅
- **TP 4.5RR**: 20849.64 ✅
- **TP 5RR**: 20861.70 ✅
- **PnL**: 120.68 points (5.0R)
- **MFE**: 124.96 points
- **MAE**: 11.73 points

### Trade #402 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-25 05:00:00
- **FVG 5m**: 20727.26 - 20732.10
- **Entrée**: 20753.27 @ 2025-03-25 05:01:00
- **Stop Loss**: 20716.89
- **Risk**: 36.38 points
- **TP 1RR**: 20789.65 ✅
- **TP 1.5RR**: 20807.83 ✅
- **TP 2RR**: 20826.02 ✅
- **TP 2.5RR**: 20844.21 ✅
- **TP 3RR**: 20862.40 ✅
- **TP 3.5RR**: 20880.59 ✅
- **TP 4RR**: 20898.77 ✅
- **TP 4.5RR**: 20916.96 ✅
- **TP 5RR**: 20935.15 ✅
- **PnL**: 181.88 points (5.0R)
- **MFE**: 182.09 points
- **MAE**: 23.97 points

### Trade #403 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 07:45:00
- **FVG 5m**: 20837.17 - 20845.08
- **Entrée**: 20833.09 @ 2025-03-25 07:50:00
- **Stop Loss**: 20855.50
- **Risk**: 22.41 points
- **TP 1RR**: 20810.68 ✅
- **TP 1.5RR**: 20799.48 ✅
- **TP 2RR**: 20788.28 ✅
- **TP 2.5RR**: 20777.07 ✅
- **TP 3RR**: 20765.87 ❌
- **TP 3.5RR**: 20754.66 ❌
- **TP 4RR**: 20743.46 ❌
- **TP 4.5RR**: 20732.25 ❌
- **TP 5RR**: 20721.05 ❌
- **PnL**: -22.41 points (-1.0R)
- **MFE**: 61.97 points
- **MAE**: 32.90 points

### Trade #404 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 10:45:00
- **FVG 5m**: 20876.45 - 20885.37
- **Entrée**: 20863.95 @ 2025-03-25 10:46:00
- **Stop Loss**: 20895.82
- **Risk**: 31.86 points
- **TP 1RR**: 20832.09 ✅
- **TP 1.5RR**: 20816.15 ✅
- **TP 2RR**: 20800.22 ❌
- **TP 2.5RR**: 20784.29 ❌
- **TP 3RR**: 20768.36 ❌
- **TP 3.5RR**: 20752.42 ❌
- **TP 4RR**: 20736.49 ❌
- **TP 4.5RR**: 20720.56 ❌
- **TP 5RR**: 20704.63 ❌
- **PnL**: -31.86 points (-1.0R)
- **MFE**: 51.77 points
- **MAE**: 32.90 points

### Trade #405 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 21:00:00
- **FVG 5m**: 20934.85 - 20941.22
- **Entrée**: 20923.88 @ 2025-03-25 21:01:00
- **Stop Loss**: 20951.69
- **Risk**: 27.81 points
- **TP 1RR**: 20896.07 ✅
- **TP 1.5RR**: 20882.16 ✅
- **TP 2RR**: 20868.26 ✅
- **TP 2.5RR**: 20854.35 ✅
- **TP 3RR**: 20840.44 ✅
- **TP 3.5RR**: 20826.54 ✅
- **TP 4RR**: 20812.63 ✅
- **TP 4.5RR**: 20798.73 ✅
- **TP 5RR**: 20784.82 ✅
- **PnL**: 139.06 points (5.0R)
- **MFE**: 155.82 points
- **MAE**: 1.53 points

### Trade #406 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 21:15:00
- **FVG 5m**: 20934.85 - 20941.22
- **Entrée**: 20911.90 @ 2025-03-25 21:16:00
- **Stop Loss**: 20951.69
- **Risk**: 39.80 points
- **TP 1RR**: 20872.10 ✅
- **TP 1.5RR**: 20852.20 ✅
- **TP 2RR**: 20832.30 ✅
- **TP 2.5RR**: 20812.40 ✅
- **TP 3RR**: 20792.50 ✅
- **TP 3.5RR**: 20772.60 ✅
- **TP 4RR**: 20752.70 ✅
- **TP 4.5RR**: 20732.80 ✅
- **TP 5RR**: 20712.90 ✅
- **PnL**: 198.99 points (5.0R)
- **MFE**: 204.53 points
- **MAE**: 0.77 points

### Trade #407 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 03:00:00
- **FVG 5m**: 20878.49 - 20881.29
- **Entrée**: 20890.47 @ 2025-03-26 03:01:00
- **Stop Loss**: 20868.05
- **Risk**: 22.43 points
- **TP 1RR**: 20912.90 ❌
- **TP 1.5RR**: 20924.11 ❌
- **TP 2RR**: 20935.32 ❌
- **TP 2.5RR**: 20946.54 ❌
- **TP 3RR**: 20957.75 ❌
- **TP 3.5RR**: 20968.96 ❌
- **TP 4RR**: 20980.18 ❌
- **TP 4.5RR**: 20991.39 ❌
- **TP 5RR**: 21002.60 ❌
- **PnL**: -22.43 points (-1.0R)
- **MFE**: 0.77 points
- **MAE**: 38.76 points

### Trade #408 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 05:00:00
- **FVG 5m**: 20851.96 - 20856.04
- **Entrée**: 20857.58 @ 2025-03-26 05:08:00
- **Stop Loss**: 20841.54
- **Risk**: 16.04 points
- **TP 1RR**: 20873.61 ✅
- **TP 1.5RR**: 20881.63 ✅
- **TP 2RR**: 20889.65 ✅
- **TP 2.5RR**: 20897.67 ✅
- **TP 3RR**: 20905.68 ❌
- **TP 3.5RR**: 20913.70 ❌
- **TP 4RR**: 20921.72 ❌
- **TP 4.5RR**: 20929.74 ❌
- **TP 5RR**: 20937.76 ❌
- **PnL**: -16.04 points (-1.0R)
- **MFE**: 47.43 points
- **MAE**: 32.13 points

### Trade #409 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 05:45:00
- **FVG 5m**: 20851.96 - 20856.04
- **Entrée**: 20873.39 @ 2025-03-26 05:46:00
- **Stop Loss**: 20841.54
- **Risk**: 31.85 points
- **TP 1RR**: 20905.23 ❌
- **TP 1.5RR**: 20921.16 ❌
- **TP 2RR**: 20937.08 ❌
- **TP 2.5RR**: 20953.01 ❌
- **TP 3RR**: 20968.93 ❌
- **TP 3.5RR**: 20984.86 ❌
- **TP 4RR**: 21000.78 ❌
- **TP 4.5RR**: 21016.70 ❌
- **TP 5RR**: 21032.63 ❌
- **PnL**: -31.85 points (-1.0R)
- **MFE**: 31.62 points
- **MAE**: 47.94 points

### Trade #410 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 08:45:00
- **FVG 5m**: 20878.23 - 20883.33
- **Entrée**: 20829.52 @ 2025-03-26 08:46:00
- **Stop Loss**: 20893.77
- **Risk**: 64.25 points
- **TP 1RR**: 20765.27 ✅
- **TP 1.5RR**: 20733.14 ✅
- **TP 2RR**: 20701.02 ✅
- **TP 2.5RR**: 20668.89 ✅
- **TP 3RR**: 20636.77 ✅
- **TP 3.5RR**: 20604.64 ✅
- **TP 4RR**: 20572.51 ✅
- **TP 4.5RR**: 20540.39 ✅
- **TP 5RR**: 20508.26 ✅
- **PnL**: 321.26 points (5.0R)
- **MFE**: 323.88 points
- **MAE**: 5.10 points

### Trade #411 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 09:45:00
- **FVG 5m**: 20689.51 - 20702.01
- **Entrée**: 20707.62 @ 2025-03-26 09:52:00
- **Stop Loss**: 20679.17
- **Risk**: 28.45 points
- **TP 1RR**: 20736.07 ❌
- **TP 1.5RR**: 20750.30 ❌
- **TP 2RR**: 20764.52 ❌
- **TP 2.5RR**: 20778.75 ❌
- **TP 3RR**: 20792.97 ❌
- **TP 3.5RR**: 20807.20 ❌
- **TP 4RR**: 20821.43 ❌
- **TP 4.5RR**: 20835.65 ❌
- **TP 5RR**: 20849.88 ❌
- **PnL**: -28.45 points (-1.0R)
- **MFE**: 21.42 points
- **MAE**: 31.88 points

### Trade #412 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 18:30:00
- **FVG 5m**: 20439.59 - 20445.20
- **Entrée**: 20445.71 @ 2025-03-26 18:32:00
- **Stop Loss**: 20429.37
- **Risk**: 16.34 points
- **TP 1RR**: 20462.05 ✅
- **TP 1.5RR**: 20470.22 ✅
- **TP 2RR**: 20478.39 ✅
- **TP 2.5RR**: 20486.56 ✅
- **TP 3RR**: 20494.73 ✅
- **TP 3.5RR**: 20502.90 ✅
- **TP 4RR**: 20511.07 ✅
- **TP 4.5RR**: 20519.24 ✅
- **TP 5RR**: 20527.41 ✅
- **PnL**: 81.70 points (5.0R)
- **MFE**: 82.37 points
- **MAE**: 4.85 points

### Trade #413 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 08:45:00
- **FVG 5m**: 20406.69 - 20413.57
- **Entrée**: 20417.91 @ 2025-03-27 08:49:00
- **Stop Loss**: 20396.49
- **Risk**: 21.42 points
- **TP 1RR**: 20439.33 ✅
- **TP 1.5RR**: 20450.05 ✅
- **TP 2RR**: 20460.76 ✅
- **TP 2.5RR**: 20471.47 ✅
- **TP 3RR**: 20482.18 ✅
- **TP 3.5RR**: 20492.90 ✅
- **TP 4RR**: 20503.61 ✅
- **TP 4.5RR**: 20514.32 ✅
- **TP 5RR**: 20525.03 ✅
- **PnL**: 107.12 points (5.0R)
- **MFE**: 108.64 points
- **MAE**: 15.56 points

### Trade #414 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 08:45:00
- **FVG 5m**: 20406.69 - 20413.57
- **Entrée**: 20417.91 @ 2025-03-27 08:49:00
- **Stop Loss**: 20396.49
- **Risk**: 21.42 points
- **TP 1RR**: 20439.33 ✅
- **TP 1.5RR**: 20450.05 ✅
- **TP 2RR**: 20460.76 ✅
- **TP 2.5RR**: 20471.47 ✅
- **TP 3RR**: 20482.18 ✅
- **TP 3.5RR**: 20492.90 ✅
- **TP 4RR**: 20503.61 ✅
- **TP 4.5RR**: 20514.32 ✅
- **TP 5RR**: 20525.03 ✅
- **PnL**: 107.12 points (5.0R)
- **MFE**: 108.64 points
- **MAE**: 15.56 points

### Trade #415 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 08:45:00
- **FVG 5m**: 20406.69 - 20413.57
- **Entrée**: 20417.91 @ 2025-03-27 08:49:00
- **Stop Loss**: 20396.49
- **Risk**: 21.42 points
- **TP 1RR**: 20439.33 ✅
- **TP 1.5RR**: 20450.05 ✅
- **TP 2RR**: 20460.76 ✅
- **TP 2.5RR**: 20471.47 ✅
- **TP 3RR**: 20482.18 ✅
- **TP 3.5RR**: 20492.90 ✅
- **TP 4RR**: 20503.61 ✅
- **TP 4.5RR**: 20514.32 ✅
- **TP 5RR**: 20525.03 ✅
- **PnL**: 107.12 points (5.0R)
- **MFE**: 108.64 points
- **MAE**: 15.56 points

### Trade #416 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:15:00
- **FVG 5m**: 20573.22 - 20575.77
- **Entrée**: 20548.48 @ 2025-03-27 10:16:00
- **Stop Loss**: 20586.06
- **Risk**: 37.58 points
- **TP 1RR**: 20510.91 ✅
- **TP 1.5RR**: 20492.12 ✅
- **TP 2RR**: 20473.33 ✅
- **TP 2.5RR**: 20454.54 ✅
- **TP 3RR**: 20435.76 ✅
- **TP 3.5RR**: 20416.97 ✅
- **TP 4RR**: 20398.18 ✅
- **TP 4.5RR**: 20379.39 ✅
- **TP 5RR**: 20360.60 ✅
- **PnL**: 187.88 points (5.0R)
- **MFE**: 191.27 points
- **MAE**: 26.52 points

### Trade #417 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:15:00
- **FVG 5m**: 20573.22 - 20575.77
- **Entrée**: 20548.48 @ 2025-03-27 10:16:00
- **Stop Loss**: 20586.06
- **Risk**: 37.58 points
- **TP 1RR**: 20510.91 ✅
- **TP 1.5RR**: 20492.12 ✅
- **TP 2RR**: 20473.33 ✅
- **TP 2.5RR**: 20454.54 ✅
- **TP 3RR**: 20435.76 ✅
- **TP 3.5RR**: 20416.97 ✅
- **TP 4RR**: 20398.18 ✅
- **TP 4.5RR**: 20379.39 ✅
- **TP 5RR**: 20360.60 ✅
- **PnL**: 187.88 points (5.0R)
- **MFE**: 191.27 points
- **MAE**: 26.52 points

### Trade #418 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:15:00
- **FVG 5m**: 20573.22 - 20575.77
- **Entrée**: 20548.48 @ 2025-03-27 10:16:00
- **Stop Loss**: 20586.06
- **Risk**: 37.58 points
- **TP 1RR**: 20510.91 ✅
- **TP 1.5RR**: 20492.12 ✅
- **TP 2RR**: 20473.33 ✅
- **TP 2.5RR**: 20454.54 ✅
- **TP 3RR**: 20435.76 ✅
- **TP 3.5RR**: 20416.97 ✅
- **TP 4RR**: 20398.18 ✅
- **TP 4.5RR**: 20379.39 ✅
- **TP 5RR**: 20360.60 ✅
- **PnL**: 187.88 points (5.0R)
- **MFE**: 191.27 points
- **MAE**: 26.52 points

### Trade #419 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:30:00
- **FVG 5m**: 20573.22 - 20575.77
- **Entrée**: 20512.27 @ 2025-03-27 10:31:00
- **Stop Loss**: 20586.06
- **Risk**: 73.79 points
- **TP 1RR**: 20438.48 ✅
- **TP 1.5RR**: 20401.59 ✅
- **TP 2RR**: 20364.69 ✅
- **TP 2.5RR**: 20327.80 ✅
- **TP 3RR**: 20290.90 ✅
- **TP 3.5RR**: 20254.01 ✅
- **TP 4RR**: 20217.11 ✅
- **TP 4.5RR**: 20180.22 ✅
- **TP 5RR**: 20143.32 ✅
- **PnL**: 368.95 points (5.0R)
- **MFE**: 370.04 points
- **MAE**: 48.71 points

### Trade #420 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 21:00:00
- **FVG 5m**: 20380.17 - 20383.48
- **Entrée**: 20385.78 @ 2025-03-27 21:08:00
- **Stop Loss**: 20369.98
- **Risk**: 15.80 points
- **TP 1RR**: 20401.58 ❌
- **TP 1.5RR**: 20409.48 ❌
- **TP 2RR**: 20417.38 ❌
- **TP 2.5RR**: 20425.28 ❌
- **TP 3RR**: 20433.18 ❌
- **TP 3.5RR**: 20441.08 ❌
- **TP 4RR**: 20448.98 ❌
- **TP 4.5RR**: 20456.88 ❌
- **TP 5RR**: 20464.78 ❌
- **PnL**: -15.80 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 16.07 points

### Trade #421 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 01:45:00
- **FVG 5m**: 20395.21 - 20397.76
- **Entrée**: 20377.36 @ 2025-03-28 01:46:00
- **Stop Loss**: 20407.96
- **Risk**: 30.60 points
- **TP 1RR**: 20346.76 ✅
- **TP 1.5RR**: 20331.46 ✅
- **TP 2RR**: 20316.16 ✅
- **TP 2.5RR**: 20300.86 ✅
- **TP 3RR**: 20285.56 ✅
- **TP 3.5RR**: 20270.26 ✅
- **TP 4RR**: 20254.96 ✅
- **TP 4.5RR**: 20239.66 ✅
- **TP 5RR**: 20224.36 ✅
- **PnL**: 153.00 points (5.0R)
- **MFE**: 165.00 points
- **MAE**: 1.53 points

### Trade #422 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 02:30:00
- **FVG 5m**: 20395.21 - 20397.76
- **Entrée**: 20323.81 @ 2025-03-28 02:31:00
- **Stop Loss**: 20407.96
- **Risk**: 84.16 points
- **TP 1RR**: 20239.65 ✅
- **TP 1.5RR**: 20197.57 ✅
- **TP 2RR**: 20155.49 ✅
- **TP 2.5RR**: 20113.41 ✅
- **TP 3RR**: 20071.34 ✅
- **TP 3.5RR**: 20029.26 ✅
- **TP 4RR**: 19987.18 ✅
- **TP 4.5RR**: 19945.10 ✅
- **TP 5RR**: 19903.02 ✅
- **PnL**: 420.78 points (5.0R)
- **MFE**: 423.09 points
- **MAE**: 47.43 points

### Trade #423 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 02:30:00
- **FVG 5m**: 20395.21 - 20397.76
- **Entrée**: 20323.81 @ 2025-03-28 02:31:00
- **Stop Loss**: 20407.96
- **Risk**: 84.16 points
- **TP 1RR**: 20239.65 ✅
- **TP 1.5RR**: 20197.57 ✅
- **TP 2RR**: 20155.49 ✅
- **TP 2.5RR**: 20113.41 ✅
- **TP 3RR**: 20071.34 ✅
- **TP 3.5RR**: 20029.26 ✅
- **TP 4RR**: 19987.18 ✅
- **TP 4.5RR**: 19945.10 ✅
- **TP 5RR**: 19903.02 ✅
- **PnL**: 420.78 points (5.0R)
- **MFE**: 423.09 points
- **MAE**: 47.43 points

### Trade #424 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 05:00:00
- **FVG 5m**: 20310.03 - 20313.60
- **Entrée**: 20315.13 @ 2025-03-28 05:02:00
- **Stop Loss**: 20299.88
- **Risk**: 15.26 points
- **TP 1RR**: 20330.39 ✅
- **TP 1.5RR**: 20338.02 ✅
- **TP 2RR**: 20345.65 ✅
- **TP 2.5RR**: 20353.27 ✅
- **TP 3RR**: 20360.90 ✅
- **TP 3.5RR**: 20368.53 ✅
- **TP 4RR**: 20376.16 ❌
- **TP 4.5RR**: 20383.78 ❌
- **TP 5RR**: 20391.41 ❌
- **PnL**: -15.26 points (-1.0R)
- **MFE**: 56.11 points
- **MAE**: 24.99 points

### Trade #425 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 05:00:00
- **FVG 5m**: 20310.03 - 20313.60
- **Entrée**: 20315.13 @ 2025-03-28 05:02:00
- **Stop Loss**: 20299.88
- **Risk**: 15.26 points
- **TP 1RR**: 20330.39 ✅
- **TP 1.5RR**: 20338.02 ✅
- **TP 2RR**: 20345.65 ✅
- **TP 2.5RR**: 20353.27 ✅
- **TP 3RR**: 20360.90 ✅
- **TP 3.5RR**: 20368.53 ✅
- **TP 4RR**: 20376.16 ❌
- **TP 4.5RR**: 20383.78 ❌
- **TP 5RR**: 20391.41 ❌
- **PnL**: -15.26 points (-1.0R)
- **MFE**: 56.11 points
- **MAE**: 24.99 points

### Trade #426 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 05:30:00
- **FVG 5m**: 20310.03 - 20313.60
- **Entrée**: 20352.88 @ 2025-03-28 05:31:00
- **Stop Loss**: 20299.88
- **Risk**: 53.00 points
- **TP 1RR**: 20405.88 ❌
- **TP 1.5RR**: 20432.38 ❌
- **TP 2RR**: 20458.88 ❌
- **TP 2.5RR**: 20485.38 ❌
- **TP 3RR**: 20511.88 ❌
- **TP 3.5RR**: 20538.38 ❌
- **TP 4RR**: 20564.88 ❌
- **TP 4.5RR**: 20591.38 ❌
- **TP 5RR**: 20617.88 ❌
- **PnL**: -53.00 points (-1.0R)
- **MFE**: 18.36 points
- **MAE**: 62.74 points

### Trade #427 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 07:30:00
- **FVG 5m**: 20335.54 - 20340.38
- **Entrée**: 20296.01 @ 2025-03-28 07:31:00
- **Stop Loss**: 20350.55
- **Risk**: 54.54 points
- **TP 1RR**: 20241.46 ❌
- **TP 1.5RR**: 20214.19 ❌
- **TP 2RR**: 20186.92 ❌
- **TP 2.5RR**: 20159.65 ❌
- **TP 3RR**: 20132.37 ❌
- **TP 3.5RR**: 20105.10 ❌
- **TP 4RR**: 20077.83 ❌
- **TP 4.5RR**: 20050.56 ❌
- **TP 5RR**: 20023.28 ❌
- **PnL**: -54.54 points (-1.0R)
- **MFE**: 44.63 points
- **MAE**: 71.41 points

### Trade #428 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 14:45:00
- **FVG 5m**: 19838.75 - 19846.40
- **Entrée**: 19861.70 @ 2025-03-28 14:54:00
- **Stop Loss**: 19828.83
- **Risk**: 32.87 points
- **TP 1RR**: 19894.57 ❌
- **TP 1.5RR**: 19911.01 ❌
- **TP 2RR**: 19927.44 ❌
- **TP 2.5RR**: 19943.88 ❌
- **TP 3RR**: 19960.31 ❌
- **TP 3.5RR**: 19976.75 ❌
- **TP 4RR**: 19993.18 ❌
- **TP 4.5RR**: 20009.62 ❌
- **TP 5RR**: 20026.06 ❌
- **PnL**: -32.87 points (-1.0R)
- **MFE**: 11.48 points
- **MAE**: 33.92 points

### Trade #429 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-31 03:15:00
- **FVG 5m**: 19612.03 - 19614.83
- **Entrée**: 19610.50 @ 2025-03-31 03:24:00
- **Stop Loss**: 19624.64
- **Risk**: 14.14 points
- **TP 1RR**: 19596.35 ❌
- **TP 1.5RR**: 19589.28 ❌
- **TP 2RR**: 19582.21 ❌
- **TP 2.5RR**: 19575.14 ❌
- **TP 3RR**: 19568.07 ❌
- **TP 3.5RR**: 19561.00 ❌
- **TP 4RR**: 19553.93 ❌
- **TP 4.5RR**: 19546.85 ❌
- **TP 5RR**: 19539.78 ❌
- **PnL**: -14.14 points (-1.0R)
- **MFE**: 8.16 points
- **MAE**: 16.32 points

### Trade #430 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 04:15:00
- **FVG 5m**: 19580.66 - 19588.82
- **Entrée**: 19592.64 @ 2025-03-31 04:25:00
- **Stop Loss**: 19570.87
- **Risk**: 21.78 points
- **TP 1RR**: 19614.42 ✅
- **TP 1.5RR**: 19625.31 ❌
- **TP 2RR**: 19636.20 ❌
- **TP 2.5RR**: 19647.09 ❌
- **TP 3RR**: 19657.97 ❌
- **TP 3.5RR**: 19668.86 ❌
- **TP 4RR**: 19679.75 ❌
- **TP 4.5RR**: 19690.64 ❌
- **TP 5RR**: 19701.53 ❌
- **PnL**: -21.78 points (-1.0R)
- **MFE**: 27.29 points
- **MAE**: 25.50 points

### Trade #431 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 06:45:00
- **FVG 5m**: 19537.05 - 19550.31
- **Entrée**: 19553.12 @ 2025-03-31 06:49:00
- **Stop Loss**: 19527.28
- **Risk**: 25.84 points
- **TP 1RR**: 19578.95 ✅
- **TP 1.5RR**: 19591.87 ✅
- **TP 2RR**: 19604.79 ✅
- **TP 2.5RR**: 19617.70 ✅
- **TP 3RR**: 19630.62 ❌
- **TP 3.5RR**: 19643.54 ❌
- **TP 4RR**: 19656.46 ❌
- **TP 4.5RR**: 19669.37 ❌
- **TP 5RR**: 19682.29 ❌
- **PnL**: -25.84 points (-1.0R)
- **MFE**: 70.39 points
- **MAE**: 37.74 points

### Trade #432 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 06:45:00
- **FVG 5m**: 19537.05 - 19550.31
- **Entrée**: 19553.12 @ 2025-03-31 06:49:00
- **Stop Loss**: 19527.28
- **Risk**: 25.84 points
- **TP 1RR**: 19578.95 ✅
- **TP 1.5RR**: 19591.87 ✅
- **TP 2RR**: 19604.79 ✅
- **TP 2.5RR**: 19617.70 ✅
- **TP 3RR**: 19630.62 ❌
- **TP 3.5RR**: 19643.54 ❌
- **TP 4RR**: 19656.46 ❌
- **TP 4.5RR**: 19669.37 ❌
- **TP 5RR**: 19682.29 ❌
- **PnL**: -25.84 points (-1.0R)
- **MFE**: 70.39 points
- **MAE**: 37.74 points

### Trade #433 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 07:15:00
- **FVG 5m**: 19537.05 - 19550.31
- **Entrée**: 19565.36 @ 2025-03-31 07:25:00
- **Stop Loss**: 19527.28
- **Risk**: 38.08 points
- **TP 1RR**: 19603.43 ✅
- **TP 1.5RR**: 19622.47 ✅
- **TP 2RR**: 19641.51 ❌
- **TP 2.5RR**: 19660.55 ❌
- **TP 3RR**: 19679.59 ❌
- **TP 3.5RR**: 19698.62 ❌
- **TP 4RR**: 19717.66 ❌
- **TP 4.5RR**: 19736.70 ❌
- **TP 5RR**: 19755.74 ❌
- **PnL**: -38.08 points (-1.0R)
- **MFE**: 58.15 points
- **MAE**: 49.99 points

### Trade #434 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 09:00:00
- **FVG 5m**: 19478.14 - 19545.21
- **Entrée**: 19547.51 @ 2025-03-31 09:08:00
- **Stop Loss**: 19468.40
- **Risk**: 79.11 points
- **TP 1RR**: 19626.61 ❌
- **TP 1.5RR**: 19666.16 ❌
- **TP 2RR**: 19705.72 ❌
- **TP 2.5RR**: 19745.27 ❌
- **TP 3RR**: 19784.82 ❌
- **TP 3.5RR**: 19824.38 ❌
- **TP 4RR**: 19863.93 ❌
- **TP 4.5RR**: 19903.48 ❌
- **TP 5RR**: 19943.04 ❌
- **PnL**: -79.11 points (-1.0R)
- **MFE**: 5.61 points
- **MAE**: 80.59 points

### Trade #435 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 13:15:00
- **FVG 5m**: 19633.96 - 19668.64
- **Entrée**: 19729.59 @ 2025-03-31 13:16:00
- **Stop Loss**: 19624.14
- **Risk**: 105.45 points
- **TP 1RR**: 19835.05 ✅
- **TP 1.5RR**: 19887.77 ✅
- **TP 2RR**: 19940.50 ✅
- **TP 2.5RR**: 19993.22 ✅
- **TP 3RR**: 20045.95 ✅
- **TP 3.5RR**: 20098.68 ✅
- **TP 4RR**: 20151.40 ✅
- **TP 4.5RR**: 20204.13 ✅
- **TP 5RR**: 20256.85 ✅
- **PnL**: 527.26 points (5.0R)
- **MFE**: 535.81 points
- **MAE**: 81.10 points

### Trade #436 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 13:30:00
- **FVG 5m**: 19633.96 - 19668.64
- **Entrée**: 19780.60 @ 2025-03-31 13:31:00
- **Stop Loss**: 19624.14
- **Risk**: 156.46 points
- **TP 1RR**: 19937.06 ✅
- **TP 1.5RR**: 20015.28 ✅
- **TP 2RR**: 20093.51 ✅
- **TP 2.5RR**: 20171.74 ✅
- **TP 3RR**: 20249.97 ✅
- **TP 3.5RR**: 20328.20 ✅
- **TP 4RR**: 20406.43 ✅
- **TP 4.5RR**: 20484.66 ❌
- **TP 5RR**: 20562.88 ❌
- **PnL**: -156.46 points (-1.0R)
- **MFE**: 666.64 points
- **MAE**: 278.49 points

### Trade #437 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 14:00:00
- **FVG 5m**: 19633.96 - 19668.64
- **Entrée**: 19768.87 @ 2025-03-31 14:01:00
- **Stop Loss**: 19624.14
- **Risk**: 144.73 points
- **TP 1RR**: 19913.59 ✅
- **TP 1.5RR**: 19985.96 ✅
- **TP 2RR**: 20058.32 ✅
- **TP 2.5RR**: 20130.68 ✅
- **TP 3RR**: 20203.05 ✅
- **TP 3.5RR**: 20275.41 ✅
- **TP 4RR**: 20347.77 ✅
- **TP 4.5RR**: 20420.13 ✅
- **TP 5RR**: 20492.50 ❌
- **PnL**: -144.73 points (-1.0R)
- **MFE**: 678.37 points
- **MAE**: 266.76 points

### Trade #438 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 20:15:00
- **FVG 5m**: 19731.89 - 19733.93
- **Entrée**: 19735.46 @ 2025-03-31 21:02:00
- **Stop Loss**: 19722.02
- **Risk**: 13.44 points
- **TP 1RR**: 19748.90 ✅
- **TP 1.5RR**: 19755.61 ✅
- **TP 2RR**: 19762.33 ✅
- **TP 2.5RR**: 19769.05 ✅
- **TP 3RR**: 19775.77 ✅
- **TP 3.5RR**: 19782.49 ✅
- **TP 4RR**: 19789.20 ✅
- **TP 4.5RR**: 19795.92 ✅
- **TP 5RR**: 19802.64 ✅
- **PnL**: 67.18 points (5.0R)
- **MFE**: 67.58 points
- **MAE**: 11.73 points

### Trade #439 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 00:30:00
- **FVG 5m**: 19756.88 - 19766.32
- **Entrée**: 19755.35 @ 2025-04-01 00:44:00
- **Stop Loss**: 19776.20
- **Risk**: 20.85 points
- **TP 1RR**: 19734.50 ❌
- **TP 1.5RR**: 19724.08 ❌
- **TP 2RR**: 19713.65 ❌
- **TP 2.5RR**: 19703.23 ❌
- **TP 3RR**: 19692.80 ❌
- **TP 3.5RR**: 19682.38 ❌
- **TP 4RR**: 19671.95 ❌
- **TP 4.5RR**: 19661.53 ❌
- **TP 5RR**: 19651.11 ❌
- **PnL**: -20.85 points (-1.0R)
- **MFE**: 16.58 points
- **MAE**: 23.72 points

### Trade #440 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 02:30:00
- **FVG 5m**: 19827.27 - 19847.42
- **Entrée**: 19805.59 @ 2025-04-01 02:31:00
- **Stop Loss**: 19857.34
- **Risk**: 51.75 points
- **TP 1RR**: 19753.84 ❌
- **TP 1.5RR**: 19727.97 ❌
- **TP 2RR**: 19702.10 ❌
- **TP 2.5RR**: 19676.22 ❌
- **TP 3RR**: 19650.35 ❌
- **TP 3.5RR**: 19624.47 ❌
- **TP 4RR**: 19598.60 ❌
- **TP 4.5RR**: 19572.73 ❌
- **TP 5RR**: 19546.85 ❌
- **PnL**: -51.75 points (-1.0R)
- **MFE**: 35.19 points
- **MAE**: 53.05 points

### Trade #441 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 04:45:00
- **FVG 5m**: 19869.35 - 19871.39
- **Entrée**: 19863.74 @ 2025-04-01 05:00:00
- **Stop Loss**: 19881.32
- **Risk**: 17.59 points
- **TP 1RR**: 19846.15 ✅
- **TP 1.5RR**: 19837.36 ✅
- **TP 2RR**: 19828.56 ✅
- **TP 2.5RR**: 19819.77 ✅
- **TP 3RR**: 19810.98 ✅
- **TP 3.5RR**: 19802.19 ✅
- **TP 4RR**: 19793.39 ✅
- **TP 4.5RR**: 19784.60 ✅
- **TP 5RR**: 19775.81 ✅
- **PnL**: 87.93 points (5.0R)
- **MFE**: 98.95 points
- **MAE**: 2.81 points

### Trade #442 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 10:00:00
- **FVG 5m**: 19712.76 - 19715.06
- **Entrée**: 19917.04 @ 2025-04-01 10:01:00
- **Stop Loss**: 19702.91
- **Risk**: 214.13 points
- **TP 1RR**: 20131.17 ✅
- **TP 1.5RR**: 20238.24 ✅
- **TP 2RR**: 20345.30 ✅
- **TP 2.5RR**: 20452.37 ❌
- **TP 3RR**: 20559.44 ❌
- **TP 3.5RR**: 20666.50 ❌
- **TP 4RR**: 20773.57 ❌
- **TP 4.5RR**: 20880.63 ❌
- **TP 5RR**: 20987.70 ❌
- **PnL**: -214.13 points (-1.0R)
- **MFE**: 530.20 points
- **MAE**: 263.19 points

### Trade #443 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 11:30:00
- **FVG 5m**: 19948.15 - 19964.47
- **Entrée**: 19940.25 @ 2025-04-01 11:31:00
- **Stop Loss**: 19974.46
- **Risk**: 34.21 points
- **TP 1RR**: 19906.04 ✅
- **TP 1.5RR**: 19888.93 ✅
- **TP 2RR**: 19871.83 ❌
- **TP 2.5RR**: 19854.72 ❌
- **TP 3RR**: 19837.62 ❌
- **TP 3.5RR**: 19820.51 ❌
- **TP 4RR**: 19803.41 ❌
- **TP 4.5RR**: 19786.30 ❌
- **TP 5RR**: 19769.20 ❌
- **PnL**: -34.21 points (-1.0R)
- **MFE**: 51.77 points
- **MAE**: 48.45 points

### Trade #444 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 14:30:00
- **FVG 5m**: 19851.24 - 19892.81
- **Entrée**: 19894.60 @ 2025-04-01 14:31:00
- **Stop Loss**: 19841.32
- **Risk**: 53.28 points
- **TP 1RR**: 19947.88 ✅
- **TP 1.5RR**: 19974.52 ✅
- **TP 2RR**: 20001.16 ✅
- **TP 2.5RR**: 20027.80 ✅
- **TP 3RR**: 20054.44 ✅
- **TP 3.5RR**: 20081.08 ✅
- **TP 4RR**: 20107.72 ❌
- **TP 4.5RR**: 20134.36 ❌
- **TP 5RR**: 20161.00 ❌
- **PnL**: -53.28 points (-1.0R)
- **MFE**: 198.41 points
- **MAE**: 57.13 points

### Trade #445 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 01:00:00
- **FVG 5m**: 19964.22 - 19967.53
- **Entrée**: 19971.36 @ 2025-04-02 01:17:00
- **Stop Loss**: 19954.24
- **Risk**: 17.12 points
- **TP 1RR**: 19988.48 ❌
- **TP 1.5RR**: 19997.04 ❌
- **TP 2RR**: 20005.60 ❌
- **TP 2.5RR**: 20014.17 ❌
- **TP 3RR**: 20022.73 ❌
- **TP 3.5RR**: 20031.29 ❌
- **TP 4RR**: 20039.85 ❌
- **TP 4.5RR**: 20048.41 ❌
- **TP 5RR**: 20056.97 ❌
- **PnL**: -17.12 points (-1.0R)
- **MFE**: 12.24 points
- **MAE**: 19.13 points

### Trade #446 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 01:00:00
- **FVG 5m**: 19964.22 - 19967.53
- **Entrée**: 19971.36 @ 2025-04-02 01:17:00
- **Stop Loss**: 19954.24
- **Risk**: 17.12 points
- **TP 1RR**: 19988.48 ❌
- **TP 1.5RR**: 19997.04 ❌
- **TP 2RR**: 20005.60 ❌
- **TP 2.5RR**: 20014.17 ❌
- **TP 3RR**: 20022.73 ❌
- **TP 3.5RR**: 20031.29 ❌
- **TP 4RR**: 20039.85 ❌
- **TP 4.5RR**: 20048.41 ❌
- **TP 5RR**: 20056.97 ❌
- **PnL**: -17.12 points (-1.0R)
- **MFE**: 12.24 points
- **MAE**: 19.13 points

### Trade #447 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 08:30:00
- **FVG 5m**: 19731.89 - 19735.71
- **Entrée**: 19746.17 @ 2025-04-02 08:31:00
- **Stop Loss**: 19722.02
- **Risk**: 24.15 points
- **TP 1RR**: 19770.32 ✅
- **TP 1.5RR**: 19782.39 ✅
- **TP 2RR**: 19794.47 ✅
- **TP 2.5RR**: 19806.54 ✅
- **TP 3RR**: 19818.61 ✅
- **TP 3.5RR**: 19830.69 ✅
- **TP 4RR**: 19842.76 ✅
- **TP 4.5RR**: 19854.83 ✅
- **TP 5RR**: 19866.91 ✅
- **PnL**: 120.74 points (5.0R)
- **MFE**: 154.29 points
- **MAE**: 20.91 points

### Trade #448 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 09:00:00
- **FVG 5m**: 19911.43 - 19915.51
- **Entrée**: 19903.27 @ 2025-04-02 09:10:00
- **Stop Loss**: 19925.47
- **Risk**: 22.20 points
- **TP 1RR**: 19881.07 ❌
- **TP 1.5RR**: 19869.97 ❌
- **TP 2RR**: 19858.87 ❌
- **TP 2.5RR**: 19847.77 ❌
- **TP 3RR**: 19836.67 ❌
- **TP 3.5RR**: 19825.57 ❌
- **TP 4RR**: 19814.47 ❌
- **TP 4.5RR**: 19803.37 ❌
- **TP 5RR**: 19792.27 ❌
- **PnL**: -22.20 points (-1.0R)
- **MFE**: 20.15 points
- **MAE**: 32.64 points

### Trade #449 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 09:00:00
- **FVG 5m**: 19911.43 - 19915.51
- **Entrée**: 19903.27 @ 2025-04-02 09:10:00
- **Stop Loss**: 19925.47
- **Risk**: 22.20 points
- **TP 1RR**: 19881.07 ❌
- **TP 1.5RR**: 19869.97 ❌
- **TP 2RR**: 19858.87 ❌
- **TP 2.5RR**: 19847.77 ❌
- **TP 3RR**: 19836.67 ❌
- **TP 3.5RR**: 19825.57 ❌
- **TP 4RR**: 19814.47 ❌
- **TP 4.5RR**: 19803.37 ❌
- **TP 5RR**: 19792.27 ❌
- **PnL**: -22.20 points (-1.0R)
- **MFE**: 20.15 points
- **MAE**: 32.64 points

### Trade #450 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 10:15:00
- **FVG 5m**: 19731.89 - 19735.71
- **Entrée**: 19985.90 @ 2025-04-02 10:16:00
- **Stop Loss**: 19722.02
- **Risk**: 263.87 points
- **TP 1RR**: 20249.77 ✅
- **TP 1.5RR**: 20381.70 ✅
- **TP 2RR**: 20513.64 ❌
- **TP 2.5RR**: 20645.58 ❌
- **TP 3RR**: 20777.51 ❌
- **TP 3.5RR**: 20909.45 ❌
- **TP 4RR**: 21041.38 ❌
- **TP 4.5RR**: 21173.32 ❌
- **TP 5RR**: 21305.26 ❌
- **PnL**: -263.87 points (-1.0R)
- **MFE**: 461.34 points
- **MAE**: 275.68 points

### Trade #451 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 11:45:00
- **FVG 5m**: 20049.40 - 20060.87
- **Entrée**: 20158.04 @ 2025-04-02 11:46:00
- **Stop Loss**: 20039.37
- **Risk**: 118.67 points
- **TP 1RR**: 20276.70 ✅
- **TP 1.5RR**: 20336.04 ❌
- **TP 2RR**: 20395.37 ❌
- **TP 2.5RR**: 20454.70 ❌
- **TP 3RR**: 20514.04 ❌
- **TP 3.5RR**: 20573.37 ❌
- **TP 4RR**: 20632.70 ❌
- **TP 4.5RR**: 20692.03 ❌
- **TP 5RR**: 20751.37 ❌
- **PnL**: -118.67 points (-1.0R)
- **MFE**: 132.10 points
- **MAE**: 121.65 points

### Trade #452 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 12:00:00
- **FVG 5m**: 20049.40 - 20060.87
- **Entrée**: 20219.24 @ 2025-04-02 12:01:00
- **Stop Loss**: 20039.37
- **Risk**: 179.87 points
- **TP 1RR**: 20399.12 ❌
- **TP 1.5RR**: 20489.05 ❌
- **TP 2RR**: 20578.99 ❌
- **TP 2.5RR**: 20668.92 ❌
- **TP 3RR**: 20758.86 ❌
- **TP 3.5RR**: 20848.80 ❌
- **TP 4RR**: 20938.73 ❌
- **TP 4.5RR**: 21028.67 ❌
- **TP 5RR**: 21118.61 ❌
- **PnL**: -179.87 points (-1.0R)
- **MFE**: 70.90 points
- **MAE**: 182.85 points

### Trade #453 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:00:00
- **FVG 5m**: 20095.05 - 20117.49
- **Entrée**: 19996.10 @ 2025-04-02 15:27:00
- **Stop Loss**: 20127.55
- **Risk**: 131.45 points
- **TP 1RR**: 19864.65 ✅
- **TP 1.5RR**: 19798.92 ✅
- **TP 2RR**: 19733.19 ✅
- **TP 2.5RR**: 19667.47 ✅
- **TP 3RR**: 19601.74 ✅
- **TP 3.5RR**: 19536.02 ✅
- **TP 4RR**: 19470.29 ✅
- **TP 4.5RR**: 19404.57 ✅
- **TP 5RR**: 19338.84 ✅
- **PnL**: 657.26 points (5.0R)
- **MFE**: 694.69 points
- **MAE**: 8.93 points

### Trade #454 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:00:00
- **FVG 5m**: 20095.05 - 20117.49
- **Entrée**: 19996.10 @ 2025-04-02 15:27:00
- **Stop Loss**: 20127.55
- **Risk**: 131.45 points
- **TP 1RR**: 19864.65 ✅
- **TP 1.5RR**: 19798.92 ✅
- **TP 2RR**: 19733.19 ✅
- **TP 2.5RR**: 19667.47 ✅
- **TP 3RR**: 19601.74 ✅
- **TP 3.5RR**: 19536.02 ✅
- **TP 4RR**: 19470.29 ✅
- **TP 4.5RR**: 19404.57 ✅
- **TP 5RR**: 19338.84 ✅
- **PnL**: 657.26 points (5.0R)
- **MFE**: 694.69 points
- **MAE**: 8.93 points

### Trade #455 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:15:00
- **FVG 5m**: 20095.05 - 20117.49
- **Entrée**: 19996.10 @ 2025-04-02 15:27:00
- **Stop Loss**: 20127.55
- **Risk**: 131.45 points
- **TP 1RR**: 19864.65 ✅
- **TP 1.5RR**: 19798.92 ✅
- **TP 2RR**: 19733.19 ✅
- **TP 2.5RR**: 19667.47 ✅
- **TP 3RR**: 19601.74 ✅
- **TP 3.5RR**: 19536.02 ✅
- **TP 4RR**: 19470.29 ✅
- **TP 4.5RR**: 19404.57 ✅
- **TP 5RR**: 19338.84 ✅
- **PnL**: 657.26 points (5.0R)
- **MFE**: 694.69 points
- **MAE**: 8.93 points

### Trade #456 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:15:00
- **FVG 5m**: 20095.05 - 20117.49
- **Entrée**: 19996.10 @ 2025-04-02 15:27:00
- **Stop Loss**: 20127.55
- **Risk**: 131.45 points
- **TP 1RR**: 19864.65 ✅
- **TP 1.5RR**: 19798.92 ✅
- **TP 2RR**: 19733.19 ✅
- **TP 2.5RR**: 19667.47 ✅
- **TP 3RR**: 19601.74 ✅
- **TP 3.5RR**: 19536.02 ✅
- **TP 4RR**: 19470.29 ✅
- **TP 4.5RR**: 19404.57 ✅
- **TP 5RR**: 19338.84 ✅
- **PnL**: 657.26 points (5.0R)
- **MFE**: 694.69 points
- **MAE**: 8.93 points

### Trade #457 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:15:00
- **FVG 5m**: 20095.05 - 20117.49
- **Entrée**: 19996.10 @ 2025-04-02 15:27:00
- **Stop Loss**: 20127.55
- **Risk**: 131.45 points
- **TP 1RR**: 19864.65 ✅
- **TP 1.5RR**: 19798.92 ✅
- **TP 2RR**: 19733.19 ✅
- **TP 2.5RR**: 19667.47 ✅
- **TP 3RR**: 19601.74 ✅
- **TP 3.5RR**: 19536.02 ✅
- **TP 4RR**: 19470.29 ✅
- **TP 4.5RR**: 19404.57 ✅
- **TP 5RR**: 19338.84 ✅
- **PnL**: 657.26 points (5.0R)
- **MFE**: 694.69 points
- **MAE**: 8.93 points

### Trade #458 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 08:00:00
- **FVG 5m**: 19298.60 - 19307.02
- **Entrée**: 19375.87 @ 2025-04-03 08:30:00
- **Stop Loss**: 19288.95
- **Risk**: 86.92 points
- **TP 1RR**: 19462.79 ❌
- **TP 1.5RR**: 19506.26 ❌
- **TP 2RR**: 19549.72 ❌
- **TP 2.5RR**: 19593.18 ❌
- **TP 3RR**: 19636.64 ❌
- **TP 3.5RR**: 19680.10 ❌
- **TP 4RR**: 19723.56 ❌
- **TP 4.5RR**: 19767.02 ❌
- **TP 5RR**: 19810.48 ❌
- **PnL**: -86.92 points (-1.0R)
- **MFE**: 81.86 points
- **MAE**: 93.08 points

### Trade #459 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-03 08:30:00
- **FVG 5m**: 19380.97 - 19397.29
- **Entrée**: 19380.46 @ 2025-04-03 08:40:00
- **Stop Loss**: 19406.99
- **Risk**: 26.53 points
- **TP 1RR**: 19353.93 ❌
- **TP 1.5RR**: 19340.67 ❌
- **TP 2RR**: 19327.40 ❌
- **TP 2.5RR**: 19314.14 ❌
- **TP 3RR**: 19300.87 ❌
- **TP 3.5RR**: 19287.61 ❌
- **TP 4RR**: 19274.34 ❌
- **TP 4.5RR**: 19261.08 ❌
- **TP 5RR**: 19247.81 ❌
- **PnL**: -26.53 points (-1.0R)
- **MFE**: 16.83 points
- **MAE**: 29.33 points

### Trade #460 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 08:30:00
- **FVG 5m**: 19298.60 - 19307.02
- **Entrée**: 19384.54 @ 2025-04-03 08:31:00
- **Stop Loss**: 19288.95
- **Risk**: 95.59 points
- **TP 1RR**: 19480.14 ❌
- **TP 1.5RR**: 19527.93 ❌
- **TP 2RR**: 19575.73 ❌
- **TP 2.5RR**: 19623.53 ❌
- **TP 3RR**: 19671.32 ❌
- **TP 3.5RR**: 19719.12 ❌
- **TP 4RR**: 19766.92 ❌
- **TP 4.5RR**: 19814.71 ❌
- **TP 5RR**: 19862.51 ❌
- **PnL**: -95.59 points (-1.0R)
- **MFE**: 73.19 points
- **MAE**: 101.76 points

### Trade #461 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 10:15:00
- **FVG 5m**: 19171.85 - 19209.85
- **Entrée**: 19217.50 @ 2025-04-03 10:17:00
- **Stop Loss**: 19162.27
- **Risk**: 55.24 points
- **TP 1RR**: 19272.74 ✅
- **TP 1.5RR**: 19300.35 ✅
- **TP 2RR**: 19327.97 ✅
- **TP 2.5RR**: 19355.59 ✅
- **TP 3RR**: 19383.21 ❌
- **TP 3.5RR**: 19410.83 ❌
- **TP 4RR**: 19438.44 ❌
- **TP 4.5RR**: 19466.06 ❌
- **TP 5RR**: 19493.68 ❌
- **PnL**: -55.24 points (-1.0R)
- **MFE**: 152.00 points
- **MAE**: 57.13 points

### Trade #462 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 10:30:00
- **FVG 5m**: 19171.85 - 19209.85
- **Entrée**: 19229.49 @ 2025-04-03 10:32:00
- **Stop Loss**: 19162.27
- **Risk**: 67.22 points
- **TP 1RR**: 19296.71 ✅
- **TP 1.5RR**: 19330.32 ✅
- **TP 2RR**: 19363.93 ✅
- **TP 2.5RR**: 19397.54 ❌
- **TP 3RR**: 19431.15 ❌
- **TP 3.5RR**: 19464.76 ❌
- **TP 4RR**: 19498.38 ❌
- **TP 4.5RR**: 19531.99 ❌
- **TP 5RR**: 19565.60 ❌
- **PnL**: -67.22 points (-1.0R)
- **MFE**: 140.01 points
- **MAE**: 69.11 points

### Trade #463 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-04 00:30:00
- **FVG 5m**: 18860.46 - 18869.14
- **Entrée**: 18958.65 @ 2025-04-04 00:31:00
- **Stop Loss**: 18851.03
- **Risk**: 107.62 points
- **TP 1RR**: 19066.27 ❌
- **TP 1.5RR**: 19120.07 ❌
- **TP 2RR**: 19173.88 ❌
- **TP 2.5RR**: 19227.69 ❌
- **TP 3RR**: 19281.50 ❌
- **TP 3.5RR**: 19335.30 ❌
- **TP 4RR**: 19389.11 ❌
- **TP 4.5RR**: 19442.92 ❌
- **TP 5RR**: 19496.73 ❌
- **PnL**: -107.62 points (-1.0R)
- **MFE**: 92.57 points
- **MAE**: 124.96 points

### Trade #464 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-04 09:45:00
- **FVG 5m**: 18400.40 - 18404.22
- **Entrée**: 18411.87 @ 2025-04-04 10:04:00
- **Stop Loss**: 18391.20
- **Risk**: 20.68 points
- **TP 1RR**: 18432.55 ❌
- **TP 1.5RR**: 18442.89 ❌
- **TP 2RR**: 18453.23 ❌
- **TP 2.5RR**: 18463.56 ❌
- **TP 3RR**: 18473.90 ❌
- **TP 3.5RR**: 18484.24 ❌
- **TP 4RR**: 18494.58 ❌
- **TP 4.5RR**: 18504.92 ❌
- **TP 5RR**: 18515.26 ❌
- **PnL**: -20.68 points (-1.0R)
- **MFE**: 20.40 points
- **MAE**: 62.23 points

### Trade #465 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-04 12:15:00
- **FVG 5m**: 18173.93 - 18243.81
- **Entrée**: 18248.15 @ 2025-04-04 13:01:00
- **Stop Loss**: 18164.85
- **Risk**: 83.30 points
- **TP 1RR**: 18331.45 ❌
- **TP 1.5RR**: 18373.10 ❌
- **TP 2RR**: 18414.75 ❌
- **TP 2.5RR**: 18456.40 ❌
- **TP 3RR**: 18498.05 ❌
- **TP 3.5RR**: 18539.70 ❌
- **TP 4RR**: 18581.35 ❌
- **TP 4.5RR**: 18622.99 ❌
- **TP 5RR**: 18664.64 ❌
- **PnL**: -83.30 points (-1.0R)
- **MFE**: 24.99 points
- **MAE**: 94.61 points

### Trade #466 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-07 02:45:00
- **FVG 5m**: 16880.44 - 16896.76
- **Entrée**: 16964.09 @ 2025-04-07 02:46:00
- **Stop Loss**: 16872.00
- **Risk**: 92.09 points
- **TP 1RR**: 17056.18 ✅
- **TP 1.5RR**: 17102.22 ✅
- **TP 2RR**: 17148.27 ✅
- **TP 2.5RR**: 17194.31 ✅
- **TP 3RR**: 17240.36 ✅
- **TP 3.5RR**: 17286.40 ✅
- **TP 4RR**: 17332.44 ✅
- **TP 4.5RR**: 17378.49 ✅
- **TP 5RR**: 17424.53 ✅
- **PnL**: 460.44 points (5.0R)
- **MFE**: 482.76 points
- **MAE**: 43.86 points

### Trade #467 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 07:00:00
- **FVG 5m**: 17481.54 - 17524.38
- **Entrée**: 17444.30 @ 2025-04-07 07:01:00
- **Stop Loss**: 17533.14
- **Risk**: 88.84 points
- **TP 1RR**: 17355.46 ✅
- **TP 1.5RR**: 17311.04 ✅
- **TP 2RR**: 17266.62 ❌
- **TP 2.5RR**: 17222.20 ❌
- **TP 3RR**: 17177.78 ❌
- **TP 3.5RR**: 17133.36 ❌
- **TP 4RR**: 17088.94 ❌
- **TP 4.5RR**: 17044.52 ❌
- **TP 5RR**: 17000.10 ❌
- **PnL**: -88.84 points (-1.0R)
- **MFE**: 142.56 points
- **MAE**: 104.82 points

### Trade #468 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 08:45:00
- **FVG 5m**: 17373.92 - 17470.57
- **Entrée**: 17163.78 @ 2025-04-07 08:46:00
- **Stop Loss**: 17479.31
- **Risk**: 315.53 points
- **TP 1RR**: 16848.24 ❌
- **TP 1.5RR**: 16690.48 ❌
- **TP 2RR**: 16532.71 ❌
- **TP 2.5RR**: 16374.95 ❌
- **TP 3RR**: 16217.18 ❌
- **TP 3.5RR**: 16059.41 ❌
- **TP 4RR**: 15901.65 ❌
- **TP 4.5RR**: 15743.88 ❌
- **TP 5RR**: 15586.12 ❌
- **PnL**: -315.53 points (-1.0R)
- **MFE**: 10.46 points
- **MAE**: 330.51 points

### Trade #469 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 18:30:00
- **FVG 5m**: 18086.97 - 18090.80
- **Entrée**: 18084.93 @ 2025-04-07 18:41:00
- **Stop Loss**: 18099.84
- **Risk**: 14.91 points
- **TP 1RR**: 18070.02 ❌
- **TP 1.5RR**: 18062.56 ❌
- **TP 2RR**: 18055.11 ❌
- **TP 2.5RR**: 18047.65 ❌
- **TP 3RR**: 18040.20 ❌
- **TP 3.5RR**: 18032.74 ❌
- **TP 4RR**: 18025.29 ❌
- **TP 4.5RR**: 18017.83 ❌
- **TP 5RR**: 18010.37 ❌
- **PnL**: -14.91 points (-1.0R)
- **MFE**: 2.81 points
- **MAE**: 19.89 points

### Trade #470 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 19:15:00
- **FVG 5m**: 18120.89 - 18126.24
- **Entrée**: 18107.12 @ 2025-04-07 19:57:00
- **Stop Loss**: 18135.31
- **Risk**: 28.19 points
- **TP 1RR**: 18078.93 ✅
- **TP 1.5RR**: 18064.83 ✅
- **TP 2RR**: 18050.74 ✅
- **TP 2.5RR**: 18036.64 ✅
- **TP 3RR**: 18022.55 ✅
- **TP 3.5RR**: 18008.45 ❌
- **TP 4RR**: 17994.36 ❌
- **TP 4.5RR**: 17980.26 ❌
- **TP 5RR**: 17966.17 ❌
- **PnL**: -28.19 points (-1.0R)
- **MFE**: 89.51 points
- **MAE**: 44.63 points

### Trade #471 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 05:00:00
- **FVG 5m**: 18111.96 - 18120.63
- **Entrée**: 18129.81 @ 2025-04-08 05:35:00
- **Stop Loss**: 18102.91
- **Risk**: 26.91 points
- **TP 1RR**: 18156.72 ✅
- **TP 1.5RR**: 18170.18 ✅
- **TP 2RR**: 18183.63 ✅
- **TP 2.5RR**: 18197.08 ✅
- **TP 3RR**: 18210.54 ✅
- **TP 3.5RR**: 18223.99 ✅
- **TP 4RR**: 18237.45 ✅
- **TP 4.5RR**: 18250.90 ✅
- **TP 5RR**: 18264.35 ✅
- **PnL**: 134.54 points (5.0R)
- **MFE**: 184.89 points
- **MAE**: 12.75 points

### Trade #472 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-08 11:30:00
- **FVG 5m**: 18411.87 - 18441.71
- **Entrée**: 18215.50 @ 2025-04-08 11:31:00
- **Stop Loss**: 18450.93
- **Risk**: 235.43 points
- **TP 1RR**: 17980.07 ✅
- **TP 1.5RR**: 17862.36 ✅
- **TP 2RR**: 17744.65 ✅
- **TP 2.5RR**: 17626.93 ✅
- **TP 3RR**: 17509.22 ✅
- **TP 3.5RR**: 17391.50 ✅
- **TP 4RR**: 17273.79 ✅
- **TP 4.5RR**: 17156.07 ✅
- **TP 5RR**: 17038.36 ❌
- **PnL**: -235.43 points (-1.0R)
- **MFE**: 1144.05 points
- **MAE**: 264.46 points

### Trade #473 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-08 11:30:00
- **FVG 5m**: 18411.87 - 18441.71
- **Entrée**: 18215.50 @ 2025-04-08 11:31:00
- **Stop Loss**: 18450.93
- **Risk**: 235.43 points
- **TP 1RR**: 17980.07 ✅
- **TP 1.5RR**: 17862.36 ✅
- **TP 2RR**: 17744.65 ✅
- **TP 2.5RR**: 17626.93 ✅
- **TP 3RR**: 17509.22 ✅
- **TP 3.5RR**: 17391.50 ✅
- **TP 4RR**: 17273.79 ✅
- **TP 4.5RR**: 17156.07 ✅
- **TP 5RR**: 17038.36 ❌
- **PnL**: -235.43 points (-1.0R)
- **MFE**: 1144.05 points
- **MAE**: 264.46 points

### Trade #474 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 12:30:00
- **FVG 5m**: 17969.15 - 17977.82
- **Entrée**: 18007.40 @ 2025-04-08 12:40:00
- **Stop Loss**: 17960.16
- **Risk**: 47.24 points
- **TP 1RR**: 18054.64 ✅
- **TP 1.5RR**: 18078.26 ✅
- **TP 2RR**: 18101.88 ✅
- **TP 2.5RR**: 18125.50 ❌
- **TP 3RR**: 18149.12 ❌
- **TP 3.5RR**: 18172.74 ❌
- **TP 4RR**: 18196.36 ❌
- **TP 4.5RR**: 18219.98 ❌
- **TP 5RR**: 18243.59 ❌
- **PnL**: -47.24 points (-1.0R)
- **MFE**: 111.19 points
- **MAE**: 52.03 points

### Trade #475 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 12:30:00
- **FVG 5m**: 17969.15 - 17977.82
- **Entrée**: 18007.40 @ 2025-04-08 12:40:00
- **Stop Loss**: 17960.16
- **Risk**: 47.24 points
- **TP 1RR**: 18054.64 ✅
- **TP 1.5RR**: 18078.26 ✅
- **TP 2RR**: 18101.88 ✅
- **TP 2.5RR**: 18125.50 ❌
- **TP 3RR**: 18149.12 ❌
- **TP 3.5RR**: 18172.74 ❌
- **TP 4RR**: 18196.36 ❌
- **TP 4.5RR**: 18219.98 ❌
- **TP 5RR**: 18243.59 ❌
- **PnL**: -47.24 points (-1.0R)
- **MFE**: 111.19 points
- **MAE**: 52.03 points

### Trade #476 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 18:45:00
- **FVG 5m**: 17240.03 - 17258.90
- **Entrée**: 17275.22 @ 2025-04-08 18:46:00
- **Stop Loss**: 17231.41
- **Risk**: 43.81 points
- **TP 1RR**: 17319.04 ✅
- **TP 1.5RR**: 17340.94 ✅
- **TP 2RR**: 17362.85 ❌
- **TP 2.5RR**: 17384.76 ❌
- **TP 3RR**: 17406.66 ❌
- **TP 3.5RR**: 17428.57 ❌
- **TP 4RR**: 17450.48 ❌
- **TP 4.5RR**: 17472.38 ❌
- **TP 5RR**: 17494.29 ❌
- **PnL**: -43.81 points (-1.0R)
- **MFE**: 70.64 points
- **MAE**: 53.56 points

### Trade #477 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 00:15:00
- **FVG 5m**: 17183.41 - 17216.57
- **Entrée**: 17225.75 @ 2025-04-09 00:58:00
- **Stop Loss**: 17174.82
- **Risk**: 50.93 points
- **TP 1RR**: 17276.67 ✅
- **TP 1.5RR**: 17302.14 ✅
- **TP 2RR**: 17327.60 ✅
- **TP 2.5RR**: 17353.06 ✅
- **TP 3RR**: 17378.52 ✅
- **TP 3.5RR**: 17403.99 ✅
- **TP 4RR**: 17429.45 ✅
- **TP 4.5RR**: 17454.91 ✅
- **TP 5RR**: 17480.38 ✅
- **PnL**: 254.63 points (5.0R)
- **MFE**: 525.86 points
- **MAE**: 9.95 points

### Trade #478 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 05:15:00
- **FVG 5m**: 17604.21 - 17620.78
- **Entrée**: 17581.25 @ 2025-04-09 05:16:00
- **Stop Loss**: 17629.59
- **Risk**: 48.34 points
- **TP 1RR**: 17532.91 ✅
- **TP 1.5RR**: 17508.74 ✅
- **TP 2RR**: 17484.57 ✅
- **TP 2.5RR**: 17460.40 ❌
- **TP 3RR**: 17436.23 ❌
- **TP 3.5RR**: 17412.07 ❌
- **TP 4RR**: 17387.90 ❌
- **TP 4.5RR**: 17363.73 ❌
- **TP 5RR**: 17339.56 ❌
- **PnL**: -48.34 points (-1.0R)
- **MFE**: 107.11 points
- **MAE**: 72.94 points

### Trade #479 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 07:45:00
- **FVG 5m**: 17288.23 - 17322.15
- **Entrée**: 17378.00 @ 2025-04-09 07:46:00
- **Stop Loss**: 17279.58
- **Risk**: 98.41 points
- **TP 1RR**: 17476.41 ✅
- **TP 1.5RR**: 17525.62 ✅
- **TP 2RR**: 17574.82 ✅
- **TP 2.5RR**: 17624.03 ✅
- **TP 3RR**: 17673.24 ✅
- **TP 3.5RR**: 17722.44 ✅
- **TP 4RR**: 17771.65 ✅
- **TP 4.5RR**: 17820.86 ✅
- **TP 5RR**: 17870.06 ✅
- **PnL**: 492.07 points (5.0R)
- **MFE**: 528.92 points
- **MAE**: 20.66 points

### Trade #480 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 08:45:00
- **FVG 5m**: 17288.23 - 17322.15
- **Entrée**: 17708.51 @ 2025-04-09 08:46:00
- **Stop Loss**: 17279.58
- **Risk**: 428.93 points
- **TP 1RR**: 18137.44 ✅
- **TP 1.5RR**: 18351.90 ✅
- **TP 2RR**: 18566.37 ✅
- **TP 2.5RR**: 18780.83 ✅
- **TP 3RR**: 18995.29 ✅
- **TP 3.5RR**: 19209.76 ✅
- **TP 4RR**: 19424.22 ✅
- **TP 4.5RR**: 19638.68 ✅
- **TP 5RR**: 19853.15 ✅
- **PnL**: 2144.64 points (5.0R)
- **MFE**: 2145.79 points
- **MAE**: 156.59 points

### Trade #481 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 12:15:00
- **FVG 5m**: 17867.90 - 17877.59
- **Entrée**: 17862.80 @ 2025-04-09 12:18:00
- **Stop Loss**: 17886.53
- **Risk**: 23.73 points
- **TP 1RR**: 17839.07 ❌
- **TP 1.5RR**: 17827.21 ❌
- **TP 2RR**: 17815.34 ❌
- **TP 2.5RR**: 17803.48 ❌
- **TP 3RR**: 17791.61 ❌
- **TP 3.5RR**: 17779.75 ❌
- **TP 4RR**: 17767.88 ❌
- **TP 4.5RR**: 17756.02 ❌
- **TP 5RR**: 17744.15 ❌
- **PnL**: -23.73 points (-1.0R)
- **MFE**: 56.87 points
- **MAE**: 556.72 points

### Trade #482 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 12:15:00
- **FVG 5m**: 17867.90 - 17877.59
- **Entrée**: 17862.80 @ 2025-04-09 12:18:00
- **Stop Loss**: 17886.53
- **Risk**: 23.73 points
- **TP 1RR**: 17839.07 ❌
- **TP 1.5RR**: 17827.21 ❌
- **TP 2RR**: 17815.34 ❌
- **TP 2.5RR**: 17803.48 ❌
- **TP 3RR**: 17791.61 ❌
- **TP 3.5RR**: 17779.75 ❌
- **TP 4RR**: 17767.88 ❌
- **TP 4.5RR**: 17756.02 ❌
- **TP 5RR**: 17744.15 ❌
- **PnL**: -23.73 points (-1.0R)
- **MFE**: 56.87 points
- **MAE**: 556.72 points

### Trade #483 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 12:15:00
- **FVG 5m**: 17867.90 - 17877.59
- **Entrée**: 17862.80 @ 2025-04-09 12:18:00
- **Stop Loss**: 17886.53
- **Risk**: 23.73 points
- **TP 1RR**: 17839.07 ❌
- **TP 1.5RR**: 17827.21 ❌
- **TP 2RR**: 17815.34 ❌
- **TP 2.5RR**: 17803.48 ❌
- **TP 3RR**: 17791.61 ❌
- **TP 3.5RR**: 17779.75 ❌
- **TP 4RR**: 17767.88 ❌
- **TP 4.5RR**: 17756.02 ❌
- **TP 5RR**: 17744.15 ❌
- **PnL**: -23.73 points (-1.0R)
- **MFE**: 56.87 points
- **MAE**: 556.72 points

### Trade #484 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 12:30:00
- **FVG 5m**: 17678.16 - 17682.50
- **Entrée**: 18986.19 @ 2025-04-09 12:31:00
- **Stop Loss**: 17669.32
- **Risk**: 1316.87 points
- **TP 1RR**: 20303.06 ✅
- **TP 1.5RR**: 20961.50 ✅
- **TP 2RR**: 21619.93 ✅
- **TP 2.5RR**: 22278.36 ✅
- **TP 3RR**: 22936.80 ✅
- **TP 3.5RR**: 23595.23 ✅
- **TP 4RR**: 24253.67 ✅
- **TP 4.5RR**: 24912.10 ✅
- **TP 5RR**: 25570.54 ✅
- **PnL**: 6584.34 points (5.0R)
- **MFE**: 6584.56 points
- **MAE**: 930.34 points

### Trade #485 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 13:15:00
- **FVG 5m**: 19124.93 - 19231.53
- **Entrée**: 19113.96 @ 2025-04-09 14:00:00
- **Stop Loss**: 19241.14
- **Risk**: 127.18 points
- **TP 1RR**: 18986.78 ❌
- **TP 1.5RR**: 18923.19 ❌
- **TP 2RR**: 18859.60 ❌
- **TP 2.5RR**: 18796.00 ❌
- **TP 3RR**: 18732.41 ❌
- **TP 3.5RR**: 18668.82 ❌
- **TP 4RR**: 18605.23 ❌
- **TP 4.5RR**: 18541.64 ❌
- **TP 5RR**: 18478.05 ❌
- **PnL**: -127.18 points (-1.0R)
- **MFE**: 0.00 points
- **MAE**: 144.60 points

### Trade #486 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 14:45:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19558.98 @ 2025-04-09 14:46:00
- **Stop Loss**: 19302.97
- **Risk**: 256.01 points
- **TP 1RR**: 19814.99 ❌
- **TP 1.5RR**: 19943.00 ❌
- **TP 2RR**: 20071.00 ❌
- **TP 2.5RR**: 20199.01 ❌
- **TP 3RR**: 20327.02 ❌
- **TP 3.5RR**: 20455.02 ❌
- **TP 4RR**: 20583.03 ❌
- **TP 4.5RR**: 20711.03 ❌
- **TP 5RR**: 20839.04 ❌
- **PnL**: -256.01 points (-1.0R)
- **MFE**: 217.54 points
- **MAE**: 260.89 points

### Trade #487 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 14:45:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19558.98 @ 2025-04-09 14:46:00
- **Stop Loss**: 19302.97
- **Risk**: 256.01 points
- **TP 1RR**: 19814.99 ❌
- **TP 1.5RR**: 19943.00 ❌
- **TP 2RR**: 20071.00 ❌
- **TP 2.5RR**: 20199.01 ❌
- **TP 3RR**: 20327.02 ❌
- **TP 3.5RR**: 20455.02 ❌
- **TP 4RR**: 20583.03 ❌
- **TP 4.5RR**: 20711.03 ❌
- **TP 5RR**: 20839.04 ❌
- **PnL**: -256.01 points (-1.0R)
- **MFE**: 217.54 points
- **MAE**: 260.89 points

### Trade #488 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 15:45:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19703.58 @ 2025-04-09 15:46:00
- **Stop Loss**: 19302.97
- **Risk**: 400.61 points
- **TP 1RR**: 20104.19 ❌
- **TP 1.5RR**: 20304.50 ❌
- **TP 2RR**: 20504.80 ❌
- **TP 2.5RR**: 20705.11 ❌
- **TP 3RR**: 20905.42 ❌
- **TP 3.5RR**: 21105.72 ❌
- **TP 4RR**: 21306.03 ❌
- **TP 4.5RR**: 21506.33 ❌
- **TP 5RR**: 21706.64 ❌
- **PnL**: -400.61 points (-1.0R)
- **MFE**: 69.62 points
- **MAE**: 405.49 points

### Trade #489 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-10 20:00:00
- **FVG 5m**: 18542.19 - 18575.35
- **Entrée**: 18578.92 @ 2025-04-10 20:03:00
- **Stop Loss**: 18532.92
- **Risk**: 45.99 points
- **TP 1RR**: 18624.91 ✅
- **TP 1.5RR**: 18647.91 ✅
- **TP 2RR**: 18670.91 ✅
- **TP 2.5RR**: 18693.90 ✅
- **TP 3RR**: 18716.90 ✅
- **TP 3.5RR**: 18739.90 ✅
- **TP 4RR**: 18762.90 ✅
- **TP 4.5RR**: 18785.89 ✅
- **TP 5RR**: 18808.89 ✅
- **PnL**: 229.97 points (5.0R)
- **MFE**: 241.51 points
- **MAE**: 38.25 points

### Trade #490 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-11 02:00:00
- **FVG 5m**: 19085.91 - 19126.97
- **Entrée**: 19039.24 @ 2025-04-11 02:01:00
- **Stop Loss**: 19136.53
- **Risk**: 97.29 points
- **TP 1RR**: 18941.95 ✅
- **TP 1.5RR**: 18893.30 ✅
- **TP 2RR**: 18844.65 ✅
- **TP 2.5RR**: 18796.01 ✅
- **TP 3RR**: 18747.36 ✅
- **TP 3.5RR**: 18698.71 ✅
- **TP 4RR**: 18650.07 ✅
- **TP 4.5RR**: 18601.42 ❌
- **TP 5RR**: 18552.78 ❌
- **PnL**: -97.29 points (-1.0R)
- **MFE**: 401.92 points
- **MAE**: 106.09 points

### Trade #491 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-11 02:15:00
- **FVG 5m**: 19085.91 - 19126.97
- **Entrée**: 19003.28 @ 2025-04-11 02:16:00
- **Stop Loss**: 19136.53
- **Risk**: 133.25 points
- **TP 1RR**: 18870.03 ✅
- **TP 1.5RR**: 18803.40 ✅
- **TP 2RR**: 18736.78 ✅
- **TP 2.5RR**: 18670.15 ✅
- **TP 3RR**: 18603.53 ❌
- **TP 3.5RR**: 18536.90 ❌
- **TP 4RR**: 18470.27 ❌
- **TP 4.5RR**: 18403.65 ❌
- **TP 5RR**: 18337.02 ❌
- **PnL**: -133.25 points (-1.0R)
- **MFE**: 365.96 points
- **MAE**: 142.05 points

### Trade #492 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-11 04:15:00
- **FVG 5m**: 18832.67 - 18857.40
- **Entrée**: 18887.24 @ 2025-04-11 04:35:00
- **Stop Loss**: 18823.25
- **Risk**: 63.99 points
- **TP 1RR**: 18951.23 ✅
- **TP 1.5RR**: 18983.23 ✅
- **TP 2RR**: 19015.23 ✅
- **TP 2.5RR**: 19047.22 ✅
- **TP 3RR**: 19079.22 ❌
- **TP 3.5RR**: 19111.21 ❌
- **TP 4RR**: 19143.21 ❌
- **TP 4.5RR**: 19175.21 ❌
- **TP 5RR**: 19207.20 ❌
- **PnL**: -63.99 points (-1.0R)
- **MFE**: 191.52 points
- **MAE**: 89.26 points

### Trade #493 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-11 09:30:00
- **FVG 5m**: 18755.65 - 18776.05
- **Entrée**: 18800.79 @ 2025-04-11 09:33:00
- **Stop Loss**: 18746.27
- **Risk**: 54.52 points
- **TP 1RR**: 18855.31 ✅
- **TP 1.5RR**: 18882.56 ✅
- **TP 2RR**: 18909.82 ✅
- **TP 2.5RR**: 18937.08 ✅
- **TP 3RR**: 18964.34 ❌
- **TP 3.5RR**: 18991.60 ❌
- **TP 4RR**: 19018.86 ❌
- **TP 4.5RR**: 19046.12 ❌
- **TP 5RR**: 19073.38 ❌
- **PnL**: -54.52 points (-1.0R)
- **MFE**: 148.43 points
- **MAE**: 80.84 points

### Trade #494 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-11 12:15:00
- **FVG 5m**: 19062.70 - 19080.04
- **Entrée**: 19024.45 @ 2025-04-11 12:18:00
- **Stop Loss**: 19089.58
- **Risk**: 65.14 points
- **TP 1RR**: 18959.31 ❌
- **TP 1.5RR**: 18926.74 ❌
- **TP 2RR**: 18894.18 ❌
- **TP 2.5RR**: 18861.61 ❌
- **TP 3RR**: 18829.04 ❌
- **TP 3.5RR**: 18796.47 ❌
- **TP 4RR**: 18763.90 ❌
- **TP 4.5RR**: 18731.34 ❌
- **TP 5RR**: 18698.77 ❌
- **PnL**: -65.14 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 71.92 points

### Trade #495 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-11 12:15:00
- **FVG 5m**: 19062.70 - 19080.04
- **Entrée**: 19024.45 @ 2025-04-11 12:18:00
- **Stop Loss**: 19089.58
- **Risk**: 65.14 points
- **TP 1RR**: 18959.31 ❌
- **TP 1.5RR**: 18926.74 ❌
- **TP 2RR**: 18894.18 ❌
- **TP 2.5RR**: 18861.61 ❌
- **TP 3RR**: 18829.04 ❌
- **TP 3.5RR**: 18796.47 ❌
- **TP 4RR**: 18763.90 ❌
- **TP 4.5RR**: 18731.34 ❌
- **TP 5RR**: 18698.77 ❌
- **PnL**: -65.14 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 71.92 points

### Trade #496 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-14 01:30:00
- **FVG 5m**: 19469.98 - 19498.54
- **Entrée**: 19461.56 @ 2025-04-14 02:13:00
- **Stop Loss**: 19508.29
- **Risk**: 46.73 points
- **TP 1RR**: 19414.83 ❌
- **TP 1.5RR**: 19391.47 ❌
- **TP 2RR**: 19368.11 ❌
- **TP 2.5RR**: 19344.74 ❌
- **TP 3RR**: 19321.38 ❌
- **TP 3.5RR**: 19298.01 ❌
- **TP 4RR**: 19274.65 ❌
- **TP 4.5RR**: 19251.29 ❌
- **TP 5RR**: 19227.92 ❌
- **PnL**: -46.73 points (-1.0R)
- **MFE**: 2.81 points
- **MAE**: 48.71 points

### Trade #497 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-14 04:15:00
- **FVG 5m**: 19511.80 - 19521.75
- **Entrée**: 19490.63 @ 2025-04-14 04:16:00
- **Stop Loss**: 19531.51
- **Risk**: 40.87 points
- **TP 1RR**: 19449.76 ✅
- **TP 1.5RR**: 19429.32 ✅
- **TP 2RR**: 19408.89 ✅
- **TP 2.5RR**: 19388.45 ❌
- **TP 3RR**: 19368.01 ❌
- **TP 3.5RR**: 19347.58 ❌
- **TP 4RR**: 19327.14 ❌
- **TP 4.5RR**: 19306.70 ❌
- **TP 5RR**: 19286.26 ❌
- **PnL**: -40.87 points (-1.0R)
- **MFE**: 84.16 points
- **MAE**: 43.35 points

### Trade #498 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 08:30:00
- **FVG 5m**: 19461.31 - 19494.71
- **Entrée**: 19583.46 @ 2025-04-14 08:31:00
- **Stop Loss**: 19451.58
- **Risk**: 131.89 points
- **TP 1RR**: 19715.35 ❌
- **TP 1.5RR**: 19781.30 ❌
- **TP 2RR**: 19847.24 ❌
- **TP 2.5RR**: 19913.18 ❌
- **TP 3RR**: 19979.13 ❌
- **TP 3.5RR**: 20045.07 ❌
- **TP 4RR**: 20111.02 ❌
- **TP 4.5RR**: 20176.96 ❌
- **TP 5RR**: 20242.91 ❌
- **PnL**: -131.89 points (-1.0R)
- **MFE**: 42.59 points
- **MAE**: 141.79 points

### Trade #499 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 09:00:00
- **FVG 5m**: 19468.70 - 19479.92
- **Entrée**: 19484.77 @ 2025-04-14 09:02:00
- **Stop Loss**: 19458.97
- **Risk**: 25.80 points
- **TP 1RR**: 19510.57 ✅
- **TP 1.5RR**: 19523.47 ✅
- **TP 2RR**: 19536.37 ✅
- **TP 2.5RR**: 19549.27 ✅
- **TP 3RR**: 19562.17 ❌
- **TP 3.5RR**: 19575.07 ❌
- **TP 4RR**: 19587.97 ❌
- **TP 4.5RR**: 19600.87 ❌
- **TP 5RR**: 19613.77 ❌
- **PnL**: -25.80 points (-1.0R)
- **MFE**: 76.76 points
- **MAE**: 26.52 points

### Trade #500 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-14 10:45:00
- **FVG 5m**: 19493.69 - 19498.29
- **Entrée**: 19226.17 @ 2025-04-14 10:46:00
- **Stop Loss**: 19508.03
- **Risk**: 281.86 points
- **TP 1RR**: 18944.31 ❌
- **TP 1.5RR**: 18803.38 ❌
- **TP 2RR**: 18662.45 ❌
- **TP 2.5RR**: 18521.52 ❌
- **TP 3RR**: 18380.59 ❌
- **TP 3.5RR**: 18239.65 ❌
- **TP 4RR**: 18098.72 ❌
- **TP 4.5RR**: 17957.79 ❌
- **TP 5RR**: 17816.86 ❌
- **PnL**: -281.86 points (-1.0R)
- **MFE**: 111.96 points
- **MAE**: 290.22 points

### Trade #501 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-14 10:45:00
- **FVG 5m**: 19493.69 - 19498.29
- **Entrée**: 19226.17 @ 2025-04-14 10:46:00
- **Stop Loss**: 19508.03
- **Risk**: 281.86 points
- **TP 1RR**: 18944.31 ❌
- **TP 1.5RR**: 18803.38 ❌
- **TP 2RR**: 18662.45 ❌
- **TP 2.5RR**: 18521.52 ❌
- **TP 3RR**: 18380.59 ❌
- **TP 3.5RR**: 18239.65 ❌
- **TP 4RR**: 18098.72 ❌
- **TP 4.5RR**: 17957.79 ❌
- **TP 5RR**: 17816.86 ❌
- **PnL**: -281.86 points (-1.0R)
- **MFE**: 111.96 points
- **MAE**: 290.22 points

### Trade #502 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 13:00:00
- **FVG 5m**: 19228.21 - 19248.10
- **Entrée**: 19342.72 @ 2025-04-14 13:01:00
- **Stop Loss**: 19218.60
- **Risk**: 124.12 points
- **TP 1RR**: 19466.84 ✅
- **TP 1.5RR**: 19528.90 ❌
- **TP 2RR**: 19590.96 ❌
- **TP 2.5RR**: 19653.02 ❌
- **TP 3RR**: 19715.08 ❌
- **TP 3.5RR**: 19777.14 ❌
- **TP 4RR**: 19839.20 ❌
- **TP 4.5RR**: 19901.26 ❌
- **TP 5RR**: 19963.32 ❌
- **PnL**: -124.12 points (-1.0R)
- **MFE**: 136.18 points
- **MAE**: 125.73 points

### Trade #503 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 06:30:00
- **FVG 5m**: 19386.84 - 19392.96
- **Entrée**: 19363.63 @ 2025-04-15 06:31:00
- **Stop Loss**: 19402.66
- **Risk**: 39.02 points
- **TP 1RR**: 19324.61 ✅
- **TP 1.5RR**: 19305.09 ✅
- **TP 2RR**: 19285.58 ✅
- **TP 2.5RR**: 19266.07 ✅
- **TP 3RR**: 19246.56 ✅
- **TP 3.5RR**: 19227.05 ✅
- **TP 4RR**: 19207.53 ❌
- **TP 4.5RR**: 19188.02 ❌
- **TP 5RR**: 19168.51 ❌
- **PnL**: -39.02 points (-1.0R)
- **MFE**: 149.19 points
- **MAE**: 47.43 points

### Trade #504 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 06:30:00
- **FVG 5m**: 19386.84 - 19392.96
- **Entrée**: 19363.63 @ 2025-04-15 06:31:00
- **Stop Loss**: 19402.66
- **Risk**: 39.02 points
- **TP 1RR**: 19324.61 ✅
- **TP 1.5RR**: 19305.09 ✅
- **TP 2RR**: 19285.58 ✅
- **TP 2.5RR**: 19266.07 ✅
- **TP 3RR**: 19246.56 ✅
- **TP 3.5RR**: 19227.05 ✅
- **TP 4RR**: 19207.53 ❌
- **TP 4.5RR**: 19188.02 ❌
- **TP 5RR**: 19168.51 ❌
- **PnL**: -39.02 points (-1.0R)
- **MFE**: 149.19 points
- **MAE**: 47.43 points

### Trade #505 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 07:30:00
- **FVG 5m**: 19252.18 - 19265.70
- **Entrée**: 19271.31 @ 2025-04-15 07:37:00
- **Stop Loss**: 19242.56
- **Risk**: 28.75 points
- **TP 1RR**: 19300.06 ✅
- **TP 1.5RR**: 19314.44 ✅
- **TP 2RR**: 19328.82 ✅
- **TP 2.5RR**: 19343.19 ✅
- **TP 3RR**: 19357.57 ✅
- **TP 3.5RR**: 19371.95 ✅
- **TP 4RR**: 19386.32 ✅
- **TP 4.5RR**: 19400.70 ✅
- **TP 5RR**: 19415.08 ✅
- **PnL**: 143.77 points (5.0R)
- **MFE**: 157.61 points
- **MAE**: 4.59 points

### Trade #506 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 08:45:00
- **FVG 5m**: 19343.23 - 19349.86
- **Entrée**: 19336.34 @ 2025-04-15 09:25:00
- **Stop Loss**: 19359.53
- **Risk**: 23.19 points
- **TP 1RR**: 19313.15 ❌
- **TP 1.5RR**: 19301.56 ❌
- **TP 2RR**: 19289.96 ❌
- **TP 2.5RR**: 19278.37 ❌
- **TP 3RR**: 19266.77 ❌
- **TP 3.5RR**: 19255.17 ❌
- **TP 4RR**: 19243.58 ❌
- **TP 4.5RR**: 19231.98 ❌
- **TP 5RR**: 19220.39 ❌
- **PnL**: -23.19 points (-1.0R)
- **MFE**: 21.42 points
- **MAE**: 34.17 points

### Trade #507 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 09:15:00
- **FVG 5m**: 19343.23 - 19349.86
- **Entrée**: 19336.34 @ 2025-04-15 09:25:00
- **Stop Loss**: 19359.53
- **Risk**: 23.19 points
- **TP 1RR**: 19313.15 ❌
- **TP 1.5RR**: 19301.56 ❌
- **TP 2RR**: 19289.96 ❌
- **TP 2.5RR**: 19278.37 ❌
- **TP 3RR**: 19266.77 ❌
- **TP 3.5RR**: 19255.17 ❌
- **TP 4RR**: 19243.58 ❌
- **TP 4.5RR**: 19231.98 ❌
- **TP 5RR**: 19220.39 ❌
- **PnL**: -23.19 points (-1.0R)
- **MFE**: 21.42 points
- **MAE**: 34.17 points

### Trade #508 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 09:15:00
- **FVG 5m**: 19343.23 - 19349.86
- **Entrée**: 19336.34 @ 2025-04-15 09:25:00
- **Stop Loss**: 19359.53
- **Risk**: 23.19 points
- **TP 1RR**: 19313.15 ❌
- **TP 1.5RR**: 19301.56 ❌
- **TP 2RR**: 19289.96 ❌
- **TP 2.5RR**: 19278.37 ❌
- **TP 3RR**: 19266.77 ❌
- **TP 3.5RR**: 19255.17 ❌
- **TP 4RR**: 19243.58 ❌
- **TP 4.5RR**: 19231.98 ❌
- **TP 5RR**: 19220.39 ❌
- **PnL**: -23.19 points (-1.0R)
- **MFE**: 21.42 points
- **MAE**: 34.17 points

### Trade #509 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 22:00:00
- **FVG 5m**: 19072.14 - 19076.22
- **Entrée**: 19080.55 @ 2025-04-15 22:10:00
- **Stop Loss**: 19062.60
- **Risk**: 17.95 points
- **TP 1RR**: 19098.50 ❌
- **TP 1.5RR**: 19107.48 ❌
- **TP 2RR**: 19116.46 ❌
- **TP 2.5RR**: 19125.43 ❌
- **TP 3RR**: 19134.41 ❌
- **TP 3.5RR**: 19143.38 ❌
- **TP 4RR**: 19152.36 ❌
- **TP 4.5RR**: 19161.34 ❌
- **TP 5RR**: 19170.31 ❌
- **PnL**: -17.95 points (-1.0R)
- **MFE**: 17.34 points
- **MAE**: 19.64 points

### Trade #510 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 03:15:00
- **FVG 5m**: 18905.09 - 18914.53
- **Entrée**: 18924.99 @ 2025-04-16 03:22:00
- **Stop Loss**: 18895.64
- **Risk**: 29.34 points
- **TP 1RR**: 18954.33 ✅
- **TP 1.5RR**: 18969.00 ✅
- **TP 2RR**: 18983.68 ✅
- **TP 2.5RR**: 18998.35 ✅
- **TP 3RR**: 19013.02 ✅
- **TP 3.5RR**: 19027.69 ✅
- **TP 4RR**: 19042.36 ✅
- **TP 4.5RR**: 19057.04 ✅
- **TP 5RR**: 19071.71 ✅
- **PnL**: 146.72 points (5.0R)
- **MFE**: 187.70 points
- **MAE**: 13.01 points

### Trade #511 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 03:30:00
- **FVG 5m**: 18905.09 - 18914.53
- **Entrée**: 19047.40 @ 2025-04-16 03:31:00
- **Stop Loss**: 18895.64
- **Risk**: 151.76 points
- **TP 1RR**: 19199.16 ✅
- **TP 1.5RR**: 19275.03 ❌
- **TP 2RR**: 19350.91 ❌
- **TP 2.5RR**: 19426.79 ❌
- **TP 3RR**: 19502.67 ❌
- **TP 3.5RR**: 19578.55 ❌
- **TP 4RR**: 19654.43 ❌
- **TP 4.5RR**: 19730.31 ❌
- **TP 5RR**: 19806.18 ❌
- **PnL**: -151.76 points (-1.0R)
- **MFE**: 193.05 points
- **MAE**: 166.02 points

### Trade #512 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 03:45:00
- **FVG 5m**: 19088.71 - 19091.52
- **Entrée**: 19088.46 @ 2025-04-16 03:59:00
- **Stop Loss**: 19101.06
- **Risk**: 12.61 points
- **TP 1RR**: 19075.85 ❌
- **TP 1.5RR**: 19069.55 ❌
- **TP 2RR**: 19063.25 ❌
- **TP 2.5RR**: 19056.94 ❌
- **TP 3RR**: 19050.64 ❌
- **TP 3.5RR**: 19044.34 ❌
- **TP 4RR**: 19038.03 ❌
- **TP 4.5RR**: 19031.73 ❌
- **TP 5RR**: 19025.43 ❌
- **PnL**: -12.61 points (-1.0R)
- **MFE**: 0.00 points
- **MAE**: 22.70 points

### Trade #513 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 10:15:00
- **FVG 5m**: 18940.29 - 18975.23
- **Entrée**: 18926.26 @ 2025-04-16 11:06:00
- **Stop Loss**: 18984.71
- **Risk**: 58.45 points
- **TP 1RR**: 18867.81 ❌
- **TP 1.5RR**: 18838.58 ❌
- **TP 2RR**: 18809.36 ❌
- **TP 2.5RR**: 18780.13 ❌
- **TP 3RR**: 18750.90 ❌
- **TP 3.5RR**: 18721.68 ❌
- **TP 4RR**: 18692.45 ❌
- **TP 4.5RR**: 18663.22 ❌
- **TP 5RR**: 18634.00 ❌
- **PnL**: -58.45 points (-1.0R)
- **MFE**: 1.53 points
- **MAE**: 64.52 points

### Trade #514 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 14:45:00
- **FVG 5m**: 18511.08 - 18523.06
- **Entrée**: 18611.56 @ 2025-04-16 14:46:00
- **Stop Loss**: 18501.82
- **Risk**: 109.74 points
- **TP 1RR**: 18721.29 ✅
- **TP 1.5RR**: 18776.16 ✅
- **TP 2RR**: 18831.03 ✅
- **TP 2.5RR**: 18885.90 ✅
- **TP 3RR**: 18940.77 ✅
- **TP 3.5RR**: 18995.63 ✅
- **TP 4RR**: 19050.50 ❌
- **TP 4.5RR**: 19105.37 ❌
- **TP 5RR**: 19160.24 ❌
- **PnL**: -109.74 points (-1.0R)
- **MFE**: 416.20 points
- **MAE**: 111.96 points

### Trade #515 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 21:15:00
- **FVG 5m**: 18847.97 - 18852.81
- **Entrée**: 18832.41 @ 2025-04-16 21:39:00
- **Stop Loss**: 18862.24
- **Risk**: 29.83 points
- **TP 1RR**: 18802.58 ❌
- **TP 1.5RR**: 18787.67 ❌
- **TP 2RR**: 18772.75 ❌
- **TP 2.5RR**: 18757.84 ❌
- **TP 3RR**: 18742.93 ❌
- **TP 3.5RR**: 18728.01 ❌
- **TP 4RR**: 18713.10 ❌
- **TP 4.5RR**: 18698.18 ❌
- **TP 5RR**: 18683.27 ❌
- **PnL**: -29.83 points (-1.0R)
- **MFE**: 4.85 points
- **MAE**: 32.90 points

### Trade #516 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 06:15:00
- **FVG 5m**: 18867.35 - 18874.75
- **Entrée**: 18876.02 @ 2025-04-17 06:27:00
- **Stop Loss**: 18857.92
- **Risk**: 18.10 points
- **TP 1RR**: 18894.13 ✅
- **TP 1.5RR**: 18903.18 ✅
- **TP 2RR**: 18912.23 ✅
- **TP 2.5RR**: 18921.28 ✅
- **TP 3RR**: 18930.33 ✅
- **TP 3.5RR**: 18939.39 ✅
- **TP 4RR**: 18948.44 ✅
- **TP 4.5RR**: 18957.49 ✅
- **TP 5RR**: 18966.54 ✅
- **PnL**: 90.52 points (5.0R)
- **MFE**: 122.67 points
- **MAE**: 17.85 points

### Trade #517 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 06:15:00
- **FVG 5m**: 18867.35 - 18874.75
- **Entrée**: 18876.02 @ 2025-04-17 06:27:00
- **Stop Loss**: 18857.92
- **Risk**: 18.10 points
- **TP 1RR**: 18894.13 ✅
- **TP 1.5RR**: 18903.18 ✅
- **TP 2RR**: 18912.23 ✅
- **TP 2.5RR**: 18921.28 ✅
- **TP 3RR**: 18930.33 ✅
- **TP 3.5RR**: 18939.39 ✅
- **TP 4RR**: 18948.44 ✅
- **TP 4.5RR**: 18957.49 ✅
- **TP 5RR**: 18966.54 ✅
- **PnL**: 90.52 points (5.0R)
- **MFE**: 122.67 points
- **MAE**: 17.85 points

### Trade #518 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 06:15:00
- **FVG 5m**: 18867.35 - 18874.75
- **Entrée**: 18876.02 @ 2025-04-17 06:27:00
- **Stop Loss**: 18857.92
- **Risk**: 18.10 points
- **TP 1RR**: 18894.13 ✅
- **TP 1.5RR**: 18903.18 ✅
- **TP 2RR**: 18912.23 ✅
- **TP 2.5RR**: 18921.28 ✅
- **TP 3RR**: 18930.33 ✅
- **TP 3.5RR**: 18939.39 ✅
- **TP 4RR**: 18948.44 ✅
- **TP 4.5RR**: 18957.49 ✅
- **TP 5RR**: 18966.54 ✅
- **PnL**: 90.52 points (5.0R)
- **MFE**: 122.67 points
- **MAE**: 17.85 points

### Trade #519 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 07:00:00
- **FVG 5m**: 18867.35 - 18874.75
- **Entrée**: 18909.17 @ 2025-04-17 07:01:00
- **Stop Loss**: 18857.92
- **Risk**: 51.26 points
- **TP 1RR**: 18960.43 ✅
- **TP 1.5RR**: 18986.06 ✅
- **TP 2RR**: 19011.69 ❌
- **TP 2.5RR**: 19037.32 ❌
- **TP 3RR**: 19062.95 ❌
- **TP 3.5RR**: 19088.58 ❌
- **TP 4RR**: 19114.21 ❌
- **TP 4.5RR**: 19139.84 ❌
- **TP 5RR**: 19165.46 ❌
- **PnL**: -51.26 points (-1.0R)
- **MFE**: 89.51 points
- **MAE**: 52.03 points

### Trade #520 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 08:45:00
- **FVG 5m**: 18803.59 - 18854.34
- **Entrée**: 18856.89 @ 2025-04-17 08:52:00
- **Stop Loss**: 18794.19
- **Risk**: 62.70 points
- **TP 1RR**: 18919.60 ❌
- **TP 1.5RR**: 18950.95 ❌
- **TP 2RR**: 18982.30 ❌
- **TP 2.5RR**: 19013.65 ❌
- **TP 3RR**: 19045.00 ❌
- **TP 3.5RR**: 19076.35 ❌
- **TP 4RR**: 19107.70 ❌
- **TP 4.5RR**: 19139.05 ❌
- **TP 5RR**: 19170.41 ❌
- **PnL**: -62.70 points (-1.0R)
- **MFE**: 23.72 points
- **MAE**: 64.52 points

### Trade #521 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-21 08:30:00
- **FVG 5m**: 18485.58 - 18509.80
- **Entrée**: 18514.14 @ 2025-04-21 08:32:00
- **Stop Loss**: 18476.33
- **Risk**: 37.81 points
- **TP 1RR**: 18551.94 ❌
- **TP 1.5RR**: 18570.85 ❌
- **TP 2RR**: 18589.75 ❌
- **TP 2.5RR**: 18608.65 ❌
- **TP 3RR**: 18627.56 ❌
- **TP 3.5RR**: 18646.46 ❌
- **TP 4RR**: 18665.36 ❌
- **TP 4.5RR**: 18684.26 ❌
- **TP 5RR**: 18703.17 ❌
- **PnL**: -37.81 points (-1.0R)
- **MFE**: 9.44 points
- **MAE**: 56.87 points

### Trade #522 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 03:00:00
- **FVG 5m**: 18453.70 - 18486.85
- **Entrée**: 18434.57 @ 2025-04-22 03:01:00
- **Stop Loss**: 18496.09
- **Risk**: 61.52 points
- **TP 1RR**: 18373.05 ❌
- **TP 1.5RR**: 18342.29 ❌
- **TP 2RR**: 18311.52 ❌
- **TP 2.5RR**: 18280.76 ❌
- **TP 3RR**: 18250.00 ❌
- **TP 3.5RR**: 18219.24 ❌
- **TP 4RR**: 18188.48 ❌
- **TP 4.5RR**: 18157.71 ❌
- **TP 5RR**: 18126.95 ❌
- **PnL**: -61.52 points (-1.0R)
- **MFE**: 28.05 points
- **MAE**: 67.58 points

### Trade #523 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-22 08:30:00
- **FVG 5m**: 18428.96 - 18435.34
- **Entrée**: 18503.94 @ 2025-04-22 08:31:00
- **Stop Loss**: 18419.75
- **Risk**: 84.19 points
- **TP 1RR**: 18588.13 ✅
- **TP 1.5RR**: 18630.23 ✅
- **TP 2RR**: 18672.32 ✅
- **TP 2.5RR**: 18714.42 ✅
- **TP 3RR**: 18756.51 ✅
- **TP 3.5RR**: 18798.61 ✅
- **TP 4RR**: 18840.71 ✅
- **TP 4.5RR**: 18882.80 ✅
- **TP 5RR**: 18924.90 ✅
- **PnL**: 420.96 points (5.0R)
- **MFE**: 607.47 points
- **MAE**: 39.53 points

### Trade #524 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 11:45:00
- **FVG 5m**: 18844.40 - 18855.62
- **Entrée**: 18834.45 @ 2025-04-22 11:46:00
- **Stop Loss**: 18865.05
- **Risk**: 30.59 points
- **TP 1RR**: 18803.86 ✅
- **TP 1.5RR**: 18788.56 ✅
- **TP 2RR**: 18773.26 ✅
- **TP 2.5RR**: 18757.96 ✅
- **TP 3RR**: 18742.67 ✅
- **TP 3.5RR**: 18727.37 ✅
- **TP 4RR**: 18712.07 ✅
- **TP 4.5RR**: 18696.77 ✅
- **TP 5RR**: 18681.48 ✅
- **PnL**: 152.97 points (5.0R)
- **MFE**: 169.59 points
- **MAE**: 30.35 points

### Trade #525 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 12:15:00
- **FVG 5m**: 18844.40 - 18855.62
- **Entrée**: 18700.31 @ 2025-04-22 12:16:00
- **Stop Loss**: 18865.05
- **Risk**: 164.74 points
- **TP 1RR**: 18535.57 ❌
- **TP 1.5RR**: 18453.20 ❌
- **TP 2RR**: 18370.83 ❌
- **TP 2.5RR**: 18288.46 ❌
- **TP 3RR**: 18206.09 ❌
- **TP 3.5RR**: 18123.72 ❌
- **TP 4RR**: 18041.35 ❌
- **TP 4.5RR**: 17958.98 ❌
- **TP 5RR**: 17876.61 ❌
- **PnL**: -164.74 points (-1.0R)
- **MFE**: 122.92 points
- **MAE**: 411.10 points

### Trade #526 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 12:45:00
- **FVG 5m**: 18844.40 - 18855.62
- **Entrée**: 18632.47 @ 2025-04-22 12:46:00
- **Stop Loss**: 18865.05
- **Risk**: 232.58 points
- **TP 1RR**: 18399.90 ❌
- **TP 1.5RR**: 18283.61 ❌
- **TP 2RR**: 18167.32 ❌
- **TP 2.5RR**: 18051.03 ❌
- **TP 3RR**: 17934.74 ❌
- **TP 3.5RR**: 17818.46 ❌
- **TP 4RR**: 17702.17 ❌
- **TP 4.5RR**: 17585.88 ❌
- **TP 5RR**: 17469.59 ❌
- **PnL**: -232.58 points (-1.0R)
- **MFE**: 55.09 points
- **MAE**: 478.94 points

### Trade #527 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 12:45:00
- **FVG 5m**: 18844.40 - 18855.62
- **Entrée**: 18632.47 @ 2025-04-22 12:46:00
- **Stop Loss**: 18865.05
- **Risk**: 232.58 points
- **TP 1RR**: 18399.90 ❌
- **TP 1.5RR**: 18283.61 ❌
- **TP 2RR**: 18167.32 ❌
- **TP 2.5RR**: 18051.03 ❌
- **TP 3RR**: 17934.74 ❌
- **TP 3.5RR**: 17818.46 ❌
- **TP 4RR**: 17702.17 ❌
- **TP 4.5RR**: 17585.88 ❌
- **TP 5RR**: 17469.59 ❌
- **PnL**: -232.58 points (-1.0R)
- **MFE**: 55.09 points
- **MAE**: 478.94 points

### Trade #528 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 20:30:00
- **FVG 5m**: 19124.67 - 19127.22
- **Entrée**: 19063.72 @ 2025-04-22 20:31:00
- **Stop Loss**: 19136.79
- **Risk**: 73.07 points
- **TP 1RR**: 18990.66 ❌
- **TP 1.5RR**: 18954.12 ❌
- **TP 2RR**: 18917.59 ❌
- **TP 2.5RR**: 18881.06 ❌
- **TP 3RR**: 18844.53 ❌
- **TP 3.5RR**: 18807.99 ❌
- **TP 4RR**: 18771.46 ❌
- **TP 4.5RR**: 18734.93 ❌
- **TP 5RR**: 18698.39 ❌
- **PnL**: -73.07 points (-1.0R)
- **MFE**: 65.54 points
- **MAE**: 76.76 points

### Trade #529 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 01:45:00
- **FVG 5m**: 19125.18 - 19133.09
- **Entrée**: 19119.06 @ 2025-04-23 01:46:00
- **Stop Loss**: 19142.65
- **Risk**: 23.59 points
- **TP 1RR**: 19095.47 ❌
- **TP 1.5RR**: 19083.67 ❌
- **TP 2RR**: 19071.88 ❌
- **TP 2.5RR**: 19060.08 ❌
- **TP 3RR**: 19048.28 ❌
- **TP 3.5RR**: 19036.49 ❌
- **TP 4RR**: 19024.69 ❌
- **TP 4.5RR**: 19012.89 ❌
- **TP 5RR**: 19001.10 ❌
- **PnL**: -23.59 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 24.99 points

### Trade #530 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 03:00:00
- **FVG 5m**: 19121.61 - 19126.97
- **Entrée**: 19160.63 @ 2025-04-23 03:01:00
- **Stop Loss**: 19112.05
- **Risk**: 48.58 points
- **TP 1RR**: 19209.21 ✅
- **TP 1.5RR**: 19233.50 ✅
- **TP 2RR**: 19257.79 ✅
- **TP 2.5RR**: 19282.08 ✅
- **TP 3RR**: 19306.37 ✅
- **TP 3.5RR**: 19330.66 ✅
- **TP 4RR**: 19354.95 ✅
- **TP 4.5RR**: 19379.24 ✅
- **TP 5RR**: 19403.53 ✅
- **PnL**: 242.90 points (5.0R)
- **MFE**: 307.05 points
- **MAE**: 4.85 points

### Trade #531 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 03:30:00
- **FVG 5m**: 19121.61 - 19126.97
- **Entrée**: 19199.65 @ 2025-04-23 03:31:00
- **Stop Loss**: 19112.05
- **Risk**: 87.60 points
- **TP 1RR**: 19287.25 ✅
- **TP 1.5RR**: 19331.05 ✅
- **TP 2RR**: 19374.85 ✅
- **TP 2.5RR**: 19418.65 ✅
- **TP 3RR**: 19462.45 ✅
- **TP 3.5RR**: 19506.25 ✅
- **TP 4RR**: 19550.04 ✅
- **TP 4.5RR**: 19593.84 ❌
- **TP 5RR**: 19637.64 ❌
- **PnL**: -87.60 points (-1.0R)
- **MFE**: 351.17 points
- **MAE**: 91.55 points

### Trade #532 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 06:45:00
- **FVG 5m**: 19280.75 - 19286.36
- **Entrée**: 19271.31 @ 2025-04-23 06:46:00
- **Stop Loss**: 19296.00
- **Risk**: 24.69 points
- **TP 1RR**: 19246.62 ✅
- **TP 1.5RR**: 19234.28 ❌
- **TP 2RR**: 19221.93 ❌
- **TP 2.5RR**: 19209.59 ❌
- **TP 3RR**: 19197.24 ❌
- **TP 3.5RR**: 19184.90 ❌
- **TP 4RR**: 19172.55 ❌
- **TP 4.5RR**: 19160.21 ❌
- **TP 5RR**: 19147.86 ❌
- **PnL**: -24.69 points (-1.0R)
- **MFE**: 34.43 points
- **MAE**: 25.50 points

### Trade #533 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 08:00:00
- **FVG 5m**: 19319.00 - 19322.32
- **Entrée**: 19312.63 @ 2025-04-23 08:05:00
- **Stop Loss**: 19331.98
- **Risk**: 19.35 points
- **TP 1RR**: 19293.27 ✅
- **TP 1.5RR**: 19283.60 ✅
- **TP 2RR**: 19273.92 ✅
- **TP 2.5RR**: 19264.25 ❌
- **TP 3RR**: 19254.57 ❌
- **TP 3.5RR**: 19244.89 ❌
- **TP 4RR**: 19235.22 ❌
- **TP 4.5RR**: 19225.54 ❌
- **TP 5RR**: 19215.87 ❌
- **PnL**: -19.35 points (-1.0R)
- **MFE**: 44.37 points
- **MAE**: 19.64 points

### Trade #534 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 09:30:00
- **FVG 5m**: 19301.66 - 19318.24
- **Entrée**: 19289.67 @ 2025-04-23 10:27:00
- **Stop Loss**: 19327.90
- **Risk**: 38.22 points
- **TP 1RR**: 19251.45 ✅
- **TP 1.5RR**: 19232.34 ✅
- **TP 2RR**: 19213.23 ❌
- **TP 2.5RR**: 19194.12 ❌
- **TP 3RR**: 19175.01 ❌
- **TP 3.5RR**: 19155.90 ❌
- **TP 4RR**: 19136.79 ❌
- **TP 4.5RR**: 19117.67 ❌
- **TP 5RR**: 19098.56 ❌
- **PnL**: -38.22 points (-1.0R)
- **MFE**: 57.38 points
- **MAE**: 44.88 points

### Trade #535 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 10:15:00
- **FVG 5m**: 19448.30 - 19476.61
- **Entrée**: 19412.09 @ 2025-04-23 10:16:00
- **Stop Loss**: 19486.35
- **Risk**: 74.26 points
- **TP 1RR**: 19337.83 ✅
- **TP 1.5RR**: 19300.70 ✅
- **TP 2RR**: 19263.57 ✅
- **TP 2.5RR**: 19226.44 ✅
- **TP 3RR**: 19189.31 ✅
- **TP 3.5RR**: 19152.18 ✅
- **TP 4RR**: 19115.05 ✅
- **TP 4.5RR**: 19077.92 ✅
- **TP 5RR**: 19040.79 ✅
- **PnL**: 371.30 points (5.0R)
- **MFE**: 372.08 points
- **MAE**: 6.63 points

### Trade #536 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 14:15:00
- **FVG 5m**: 19281.77 - 19301.15
- **Entrée**: 19192.51 @ 2025-04-23 14:16:00
- **Stop Loss**: 19310.80
- **Risk**: 118.29 points
- **TP 1RR**: 19074.22 ✅
- **TP 1.5RR**: 19015.07 ✅
- **TP 2RR**: 18955.93 ❌
- **TP 2.5RR**: 18896.78 ❌
- **TP 3RR**: 18837.63 ❌
- **TP 3.5RR**: 18778.49 ❌
- **TP 4RR**: 18719.34 ❌
- **TP 4.5RR**: 18660.20 ❌
- **TP 5RR**: 18601.05 ❌
- **PnL**: -118.29 points (-1.0R)
- **MFE**: 223.91 points
- **MAE**: 119.35 points

### Trade #537 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 14:30:00
- **FVG 5m**: 19195.06 - 19197.10
- **Entrée**: 19202.71 @ 2025-04-23 14:50:00
- **Stop Loss**: 19185.46
- **Risk**: 17.25 points
- **TP 1RR**: 19219.96 ❌
- **TP 1.5RR**: 19228.58 ❌
- **TP 2RR**: 19237.21 ❌
- **TP 2.5RR**: 19245.83 ❌
- **TP 3RR**: 19254.45 ❌
- **TP 3.5RR**: 19263.08 ❌
- **TP 4RR**: 19271.70 ❌
- **TP 4.5RR**: 19280.33 ❌
- **TP 5RR**: 19288.95 ❌
- **PnL**: -17.25 points (-1.0R)
- **MFE**: 3.57 points
- **MAE**: 21.17 points

### Trade #538 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 23:30:00
- **FVG 5m**: 19116.77 - 19120.08
- **Entrée**: 19121.61 @ 2025-04-23 23:40:00
- **Stop Loss**: 19107.21
- **Risk**: 14.40 points
- **TP 1RR**: 19136.02 ✅
- **TP 1.5RR**: 19143.22 ✅
- **TP 2RR**: 19150.42 ✅
- **TP 2.5RR**: 19157.62 ✅
- **TP 3RR**: 19164.82 ❌
- **TP 3.5RR**: 19172.03 ❌
- **TP 4RR**: 19179.23 ❌
- **TP 4.5RR**: 19186.43 ❌
- **TP 5RR**: 19193.63 ❌
- **PnL**: -14.40 points (-1.0R)
- **MFE**: 37.74 points
- **MAE**: 19.89 points

### Trade #539 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 23:30:00
- **FVG 5m**: 19116.77 - 19120.08
- **Entrée**: 19121.61 @ 2025-04-23 23:40:00
- **Stop Loss**: 19107.21
- **Risk**: 14.40 points
- **TP 1RR**: 19136.02 ✅
- **TP 1.5RR**: 19143.22 ✅
- **TP 2RR**: 19150.42 ✅
- **TP 2.5RR**: 19157.62 ✅
- **TP 3RR**: 19164.82 ❌
- **TP 3.5RR**: 19172.03 ❌
- **TP 4RR**: 19179.23 ❌
- **TP 4.5RR**: 19186.43 ❌
- **TP 5RR**: 19193.63 ❌
- **PnL**: -14.40 points (-1.0R)
- **MFE**: 37.74 points
- **MAE**: 19.89 points

### Trade #540 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 03:30:00
- **FVG 5m**: 19116.00 - 19123.65
- **Entrée**: 19014.25 @ 2025-04-24 03:31:00
- **Stop Loss**: 19133.21
- **Risk**: 118.97 points
- **TP 1RR**: 18895.28 ❌
- **TP 1.5RR**: 18835.79 ❌
- **TP 2RR**: 18776.31 ❌
- **TP 2.5RR**: 18716.83 ❌
- **TP 3RR**: 18657.34 ❌
- **TP 3.5RR**: 18597.86 ❌
- **TP 4RR**: 18538.37 ❌
- **TP 4.5RR**: 18478.89 ❌
- **TP 5RR**: 18419.41 ❌
- **PnL**: -118.97 points (-1.0R)
- **MFE**: 45.65 points
- **MAE**: 121.39 points

### Trade #541 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-24 03:45:00
- **FVG 5m**: 19017.56 - 19020.62
- **Entrée**: 19022.41 @ 2025-04-24 04:14:00
- **Stop Loss**: 19008.05
- **Risk**: 14.35 points
- **TP 1RR**: 19036.76 ✅
- **TP 1.5RR**: 19043.94 ✅
- **TP 2RR**: 19051.11 ✅
- **TP 2.5RR**: 19058.29 ✅
- **TP 3RR**: 19065.47 ✅
- **TP 3.5RR**: 19072.65 ✅
- **TP 4RR**: 19079.82 ✅
- **TP 4.5RR**: 19087.00 ✅
- **TP 5RR**: 19094.18 ✅
- **PnL**: 71.77 points (5.0R)
- **MFE**: 78.80 points
- **MAE**: 10.20 points

### Trade #542 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 06:00:00
- **FVG 5m**: 19169.30 - 19188.43
- **Entrée**: 19161.65 @ 2025-04-24 06:03:00
- **Stop Loss**: 19198.02
- **Risk**: 36.37 points
- **TP 1RR**: 19125.28 ✅
- **TP 1.5RR**: 19107.09 ✅
- **TP 2RR**: 19088.91 ❌
- **TP 2.5RR**: 19070.72 ❌
- **TP 3RR**: 19052.53 ❌
- **TP 3.5RR**: 19034.35 ❌
- **TP 4RR**: 19016.16 ❌
- **TP 4.5RR**: 18997.98 ❌
- **TP 5RR**: 18979.79 ❌
- **PnL**: -36.37 points (-1.0R)
- **MFE**: 55.60 points
- **MAE**: 39.53 points

### Trade #543 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 06:00:00
- **FVG 5m**: 19169.30 - 19188.43
- **Entrée**: 19161.65 @ 2025-04-24 06:03:00
- **Stop Loss**: 19198.02
- **Risk**: 36.37 points
- **TP 1RR**: 19125.28 ✅
- **TP 1.5RR**: 19107.09 ✅
- **TP 2RR**: 19088.91 ❌
- **TP 2.5RR**: 19070.72 ❌
- **TP 3RR**: 19052.53 ❌
- **TP 3.5RR**: 19034.35 ❌
- **TP 4RR**: 19016.16 ❌
- **TP 4.5RR**: 18997.98 ❌
- **TP 5RR**: 18979.79 ❌
- **PnL**: -36.37 points (-1.0R)
- **MFE**: 55.60 points
- **MAE**: 39.53 points

### Trade #544 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 08:00:00
- **FVG 5m**: 19208.32 - 19225.92
- **Entrée**: 19207.81 @ 2025-04-24 08:06:00
- **Stop Loss**: 19235.53
- **Risk**: 27.72 points
- **TP 1RR**: 19180.09 ❌
- **TP 1.5RR**: 19166.23 ❌
- **TP 2RR**: 19152.37 ❌
- **TP 2.5RR**: 19138.51 ❌
- **TP 3RR**: 19124.65 ❌
- **TP 3.5RR**: 19110.79 ❌
- **TP 4RR**: 19096.93 ❌
- **TP 4.5RR**: 19083.07 ❌
- **TP 5RR**: 19069.21 ❌
- **PnL**: -27.72 points (-1.0R)
- **MFE**: 5.36 points
- **MAE**: 36.21 points

### Trade #545 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-24 22:15:00
- **FVG 5m**: 19775.75 - 19781.87
- **Entrée**: 19797.43 @ 2025-04-24 22:21:00
- **Stop Loss**: 19765.87
- **Risk**: 31.57 points
- **TP 1RR**: 19829.00 ✅
- **TP 1.5RR**: 19844.78 ✅
- **TP 2RR**: 19860.56 ✅
- **TP 2.5RR**: 19876.34 ✅
- **TP 3RR**: 19892.13 ❌
- **TP 3.5RR**: 19907.91 ❌
- **TP 4RR**: 19923.69 ❌
- **TP 4.5RR**: 19939.47 ❌
- **TP 5RR**: 19955.26 ❌
- **PnL**: -31.57 points (-1.0R)
- **MFE**: 92.06 points
- **MAE**: 34.68 points

### Trade #546 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 23:15:00
- **FVG 5m**: 19840.28 - 19862.97
- **Entrée**: 19832.62 @ 2025-04-24 23:25:00
- **Stop Loss**: 19872.90
- **Risk**: 40.28 points
- **TP 1RR**: 19792.35 ✅
- **TP 1.5RR**: 19772.21 ✅
- **TP 2RR**: 19752.07 ✅
- **TP 2.5RR**: 19731.93 ✅
- **TP 3RR**: 19711.79 ✅
- **TP 3.5RR**: 19691.65 ✅
- **TP 4RR**: 19671.51 ✅
- **TP 4.5RR**: 19651.37 ✅
- **TP 5RR**: 19631.23 ✅
- **PnL**: 201.40 points (5.0R)
- **MFE**: 203.26 points
- **MAE**: 37.23 points

### Trade #547 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-25 12:30:00
- **FVG 5m**: 19913.21 - 19921.37
- **Entrée**: 19905.82 @ 2025-04-25 12:31:00
- **Stop Loss**: 19931.33
- **Risk**: 25.52 points
- **TP 1RR**: 19880.30 ❌
- **TP 1.5RR**: 19867.54 ❌
- **TP 2RR**: 19854.78 ❌
- **TP 2.5RR**: 19842.02 ❌
- **TP 3RR**: 19829.27 ❌
- **TP 3.5RR**: 19816.51 ❌
- **TP 4RR**: 19803.75 ❌
- **TP 4.5RR**: 19790.99 ❌
- **TP 5RR**: 19778.23 ❌
- **PnL**: -25.52 points (-1.0R)
- **MFE**: 0.77 points
- **MAE**: 29.07 points

### Trade #548 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-25 12:30:00
- **FVG 5m**: 19913.21 - 19921.37
- **Entrée**: 19905.82 @ 2025-04-25 12:31:00
- **Stop Loss**: 19931.33
- **Risk**: 25.52 points
- **TP 1RR**: 19880.30 ❌
- **TP 1.5RR**: 19867.54 ❌
- **TP 2RR**: 19854.78 ❌
- **TP 2.5RR**: 19842.02 ❌
- **TP 3RR**: 19829.27 ❌
- **TP 3.5RR**: 19816.51 ❌
- **TP 4RR**: 19803.75 ❌
- **TP 4.5RR**: 19790.99 ❌
- **TP 5RR**: 19778.23 ❌
- **PnL**: -25.52 points (-1.0R)
- **MFE**: 0.77 points
- **MAE**: 29.07 points

### Trade #549 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-25 15:30:00
- **FVG 5m**: 19937.19 - 19945.35
- **Entrée**: 19935.66 @ 2025-04-25 15:44:00
- **Stop Loss**: 19955.32
- **Risk**: 19.66 points
- **TP 1RR**: 19915.99 ✅
- **TP 1.5RR**: 19906.16 ✅
- **TP 2RR**: 19896.33 ✅
- **TP 2.5RR**: 19886.50 ✅
- **TP 3RR**: 19876.66 ✅
- **TP 3.5RR**: 19866.83 ✅
- **TP 4RR**: 19857.00 ✅
- **TP 4.5RR**: 19847.17 ✅
- **TP 5RR**: 19837.34 ✅
- **PnL**: 98.32 points (5.0R)
- **MFE**: 99.72 points
- **MAE**: 14.03 points

### Trade #550 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-27 20:15:00
- **FVG 5m**: 19844.36 - 19850.99
- **Entrée**: 19822.17 @ 2025-04-27 20:16:00
- **Stop Loss**: 19860.91
- **Risk**: 38.74 points
- **TP 1RR**: 19783.43 ✅
- **TP 1.5RR**: 19764.05 ❌
- **TP 2RR**: 19744.68 ❌
- **TP 2.5RR**: 19725.31 ❌
- **TP 3RR**: 19705.94 ❌
- **TP 3.5RR**: 19686.57 ❌
- **TP 4RR**: 19667.19 ❌
- **TP 4.5RR**: 19647.82 ❌
- **TP 5RR**: 19628.45 ❌
- **PnL**: -38.74 points (-1.0R)
- **MFE**: 40.04 points
- **MAE**: 40.04 points

### Trade #551 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 04:45:00
- **FVG 5m**: 19903.01 - 19914.74
- **Entrée**: 19902.25 @ 2025-04-28 05:00:00
- **Stop Loss**: 19924.70
- **Risk**: 22.45 points
- **TP 1RR**: 19879.79 ✅
- **TP 1.5RR**: 19868.57 ✅
- **TP 2RR**: 19857.34 ❌
- **TP 2.5RR**: 19846.11 ❌
- **TP 3RR**: 19834.89 ❌
- **TP 3.5RR**: 19823.66 ❌
- **TP 4RR**: 19812.43 ❌
- **TP 4.5RR**: 19801.21 ❌
- **TP 5RR**: 19789.98 ❌
- **PnL**: -22.45 points (-1.0R)
- **MFE**: 44.63 points
- **MAE**: 23.72 points

### Trade #552 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 08:45:00
- **FVG 5m**: 19921.88 - 19926.73
- **Entrée**: 19910.66 @ 2025-04-28 08:55:00
- **Stop Loss**: 19936.69
- **Risk**: 26.03 points
- **TP 1RR**: 19884.63 ✅
- **TP 1.5RR**: 19871.62 ✅
- **TP 2RR**: 19858.60 ✅
- **TP 2.5RR**: 19845.59 ✅
- **TP 3RR**: 19832.57 ✅
- **TP 3.5RR**: 19819.56 ✅
- **TP 4RR**: 19806.54 ✅
- **TP 4.5RR**: 19793.53 ✅
- **TP 5RR**: 19780.51 ✅
- **PnL**: 130.15 points (5.0R)
- **MFE**: 135.93 points
- **MAE**: 21.42 points

### Trade #553 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 08:45:00
- **FVG 5m**: 19921.88 - 19926.73
- **Entrée**: 19910.66 @ 2025-04-28 08:55:00
- **Stop Loss**: 19936.69
- **Risk**: 26.03 points
- **TP 1RR**: 19884.63 ✅
- **TP 1.5RR**: 19871.62 ✅
- **TP 2RR**: 19858.60 ✅
- **TP 2.5RR**: 19845.59 ✅
- **TP 3RR**: 19832.57 ✅
- **TP 3.5RR**: 19819.56 ✅
- **TP 4RR**: 19806.54 ✅
- **TP 4.5RR**: 19793.53 ✅
- **TP 5RR**: 19780.51 ✅
- **PnL**: 130.15 points (5.0R)
- **MFE**: 135.93 points
- **MAE**: 21.42 points

### Trade #554 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 10:00:00
- **FVG 5m**: 19917.55 - 19952.74
- **Entrée**: 19883.88 @ 2025-04-28 10:01:00
- **Stop Loss**: 19962.72
- **Risk**: 78.83 points
- **TP 1RR**: 19805.05 ✅
- **TP 1.5RR**: 19765.63 ✅
- **TP 2RR**: 19726.22 ✅
- **TP 2.5RR**: 19686.80 ✅
- **TP 3RR**: 19647.38 ✅
- **TP 3.5RR**: 19607.97 ❌
- **TP 4RR**: 19568.55 ❌
- **TP 4.5RR**: 19529.13 ❌
- **TP 5RR**: 19489.72 ❌
- **PnL**: -78.83 points (-1.0R)
- **MFE**: 239.47 points
- **MAE**: 88.49 points

### Trade #555 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 10:15:00
- **FVG 5m**: 19917.55 - 19952.74
- **Entrée**: 19802.28 @ 2025-04-28 10:16:00
- **Stop Loss**: 19962.72
- **Risk**: 160.44 points
- **TP 1RR**: 19641.83 ❌
- **TP 1.5RR**: 19561.61 ❌
- **TP 2RR**: 19481.39 ❌
- **TP 2.5RR**: 19401.17 ❌
- **TP 3RR**: 19320.95 ❌
- **TP 3.5RR**: 19240.73 ❌
- **TP 4RR**: 19160.51 ❌
- **TP 4.5RR**: 19080.29 ❌
- **TP 5RR**: 19000.07 ❌
- **PnL**: -160.44 points (-1.0R)
- **MFE**: 157.86 points
- **MAE**: 170.10 points

### Trade #556 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:00:00
- **FVG 5m**: 19691.09 - 19694.91
- **Entrée**: 19760.71 @ 2025-04-28 13:01:00
- **Stop Loss**: 19681.24
- **Risk**: 79.47 points
- **TP 1RR**: 19840.17 ✅
- **TP 1.5RR**: 19879.91 ✅
- **TP 2RR**: 19919.64 ✅
- **TP 2.5RR**: 19959.38 ✅
- **TP 3RR**: 19999.11 ✅
- **TP 3.5RR**: 20038.84 ✅
- **TP 4RR**: 20078.58 ✅
- **TP 4.5RR**: 20118.31 ❌
- **TP 5RR**: 20158.05 ❌
- **PnL**: -79.47 points (-1.0R)
- **MFE**: 323.63 points
- **MAE**: 85.18 points

### Trade #557 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:15:00
- **FVG 5m**: 19691.09 - 19694.91
- **Entrée**: 19756.63 @ 2025-04-28 13:16:00
- **Stop Loss**: 19681.24
- **Risk**: 75.39 points
- **TP 1RR**: 19832.01 ✅
- **TP 1.5RR**: 19869.71 ✅
- **TP 2RR**: 19907.40 ✅
- **TP 2.5RR**: 19945.10 ✅
- **TP 3RR**: 19982.79 ✅
- **TP 3.5RR**: 20020.48 ✅
- **TP 4RR**: 20058.18 ✅
- **TP 4.5RR**: 20095.87 ❌
- **TP 5RR**: 20133.56 ❌
- **PnL**: -75.39 points (-1.0R)
- **MFE**: 327.71 points
- **MAE**: 81.10 points

### Trade #558 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:15:00
- **FVG 5m**: 19691.09 - 19694.91
- **Entrée**: 19756.63 @ 2025-04-28 13:16:00
- **Stop Loss**: 19681.24
- **Risk**: 75.39 points
- **TP 1RR**: 19832.01 ✅
- **TP 1.5RR**: 19869.71 ✅
- **TP 2RR**: 19907.40 ✅
- **TP 2.5RR**: 19945.10 ✅
- **TP 3RR**: 19982.79 ✅
- **TP 3.5RR**: 20020.48 ✅
- **TP 4RR**: 20058.18 ✅
- **TP 4.5RR**: 20095.87 ❌
- **TP 5RR**: 20133.56 ❌
- **PnL**: -75.39 points (-1.0R)
- **MFE**: 327.71 points
- **MAE**: 81.10 points

### Trade #559 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:15:00
- **FVG 5m**: 19691.09 - 19694.91
- **Entrée**: 19756.63 @ 2025-04-28 13:16:00
- **Stop Loss**: 19681.24
- **Risk**: 75.39 points
- **TP 1RR**: 19832.01 ✅
- **TP 1.5RR**: 19869.71 ✅
- **TP 2RR**: 19907.40 ✅
- **TP 2.5RR**: 19945.10 ✅
- **TP 3RR**: 19982.79 ✅
- **TP 3.5RR**: 20020.48 ✅
- **TP 4RR**: 20058.18 ✅
- **TP 4.5RR**: 20095.87 ❌
- **TP 5RR**: 20133.56 ❌
- **PnL**: -75.39 points (-1.0R)
- **MFE**: 327.71 points
- **MAE**: 81.10 points

### Trade #560 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 21:00:00
- **FVG 5m**: 19906.07 - 19915.51
- **Entrée**: 19996.35 @ 2025-04-28 21:01:00
- **Stop Loss**: 19896.12
- **Risk**: 100.23 points
- **TP 1RR**: 20096.58 ❌
- **TP 1.5RR**: 20146.70 ❌
- **TP 2RR**: 20196.82 ❌
- **TP 2.5RR**: 20246.93 ❌
- **TP 3RR**: 20297.05 ❌
- **TP 3.5RR**: 20347.16 ❌
- **TP 4RR**: 20397.28 ❌
- **TP 4.5RR**: 20447.40 ❌
- **TP 5RR**: 20497.51 ❌
- **PnL**: -100.23 points (-1.0R)
- **MFE**: 29.33 points
- **MAE**: 106.09 points

### Trade #561 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 21:30:00
- **FVG 5m**: 19978.75 - 19982.07
- **Entrée**: 19978.50 @ 2025-04-28 21:43:00
- **Stop Loss**: 19992.06
- **Risk**: 13.56 points
- **TP 1RR**: 19964.94 ✅
- **TP 1.5RR**: 19958.16 ✅
- **TP 2RR**: 19951.38 ✅
- **TP 2.5RR**: 19944.60 ✅
- **TP 3RR**: 19937.82 ✅
- **TP 3.5RR**: 19931.03 ✅
- **TP 4RR**: 19924.25 ✅
- **TP 4.5RR**: 19917.47 ❌
- **TP 5RR**: 19910.69 ❌
- **PnL**: -13.56 points (-1.0R)
- **MFE**: 60.44 points
- **MAE**: 17.85 points

### Trade #562 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 03:00:00
- **FVG 5m**: 20001.20 - 20003.75
- **Entrée**: 19981.05 @ 2025-04-29 03:01:00
- **Stop Loss**: 20013.75
- **Risk**: 32.70 points
- **TP 1RR**: 19948.35 ✅
- **TP 1.5RR**: 19932.00 ✅
- **TP 2RR**: 19915.65 ✅
- **TP 2.5RR**: 19899.30 ✅
- **TP 3RR**: 19882.95 ✅
- **TP 3.5RR**: 19866.60 ✅
- **TP 4RR**: 19850.25 ✅
- **TP 4.5RR**: 19833.90 ✅
- **TP 5RR**: 19817.55 ✅
- **PnL**: 163.50 points (5.0R)
- **MFE**: 172.65 points
- **MAE**: 12.50 points

### Trade #563 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-29 07:30:00
- **FVG 5m**: 19873.17 - 19878.53
- **Entrée**: 19881.84 @ 2025-04-29 07:31:00
- **Stop Loss**: 19863.24
- **Risk**: 18.61 points
- **TP 1RR**: 19900.45 ✅
- **TP 1.5RR**: 19909.76 ✅
- **TP 2RR**: 19919.06 ✅
- **TP 2.5RR**: 19928.36 ✅
- **TP 3RR**: 19937.67 ❌
- **TP 3.5RR**: 19946.97 ❌
- **TP 4RR**: 19956.27 ❌
- **TP 4.5RR**: 19965.58 ❌
- **TP 5RR**: 19974.88 ❌
- **PnL**: -18.61 points (-1.0R)
- **MFE**: 48.97 points
- **MAE**: 19.64 points

### Trade #564 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-29 08:30:00
- **FVG 5m**: 19812.99 - 19836.45
- **Entrée**: 19845.89 @ 2025-04-29 08:31:00
- **Stop Loss**: 19803.08
- **Risk**: 42.80 points
- **TP 1RR**: 19888.69 ❌
- **TP 1.5RR**: 19910.09 ❌
- **TP 2RR**: 19931.50 ❌
- **TP 2.5RR**: 19952.90 ❌
- **TP 3RR**: 19974.30 ❌
- **TP 3.5RR**: 19995.70 ❌
- **TP 4RR**: 20017.11 ❌
- **TP 4.5RR**: 20038.51 ❌
- **TP 5RR**: 20059.91 ❌
- **PnL**: -42.80 points (-1.0R)
- **MFE**: 16.83 points
- **MAE**: 42.84 points

### Trade #565 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-29 08:30:00
- **FVG 5m**: 19812.99 - 19836.45
- **Entrée**: 19845.89 @ 2025-04-29 08:31:00
- **Stop Loss**: 19803.08
- **Risk**: 42.80 points
- **TP 1RR**: 19888.69 ❌
- **TP 1.5RR**: 19910.09 ❌
- **TP 2RR**: 19931.50 ❌
- **TP 2.5RR**: 19952.90 ❌
- **TP 3RR**: 19974.30 ❌
- **TP 3.5RR**: 19995.70 ❌
- **TP 4RR**: 20017.11 ❌
- **TP 4.5RR**: 20038.51 ❌
- **TP 5RR**: 20059.91 ❌
- **PnL**: -42.80 points (-1.0R)
- **MFE**: 16.83 points
- **MAE**: 42.84 points

### Trade #566 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20037.41 - 20053.99
- **Entrée**: 20023.64 @ 2025-04-29 15:16:00
- **Stop Loss**: 20064.01
- **Risk**: 40.38 points
- **TP 1RR**: 19983.26 ✅
- **TP 1.5RR**: 19963.08 ✅
- **TP 2RR**: 19942.89 ✅
- **TP 2.5RR**: 19922.70 ✅
- **TP 3RR**: 19902.51 ✅
- **TP 3.5RR**: 19882.33 ✅
- **TP 4RR**: 19862.14 ✅
- **TP 4.5RR**: 19841.95 ✅
- **TP 5RR**: 19821.76 ✅
- **PnL**: 201.88 points (5.0R)
- **MFE**: 207.34 points
- **MAE**: 14.28 points

### Trade #567 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20037.41 - 20053.99
- **Entrée**: 20023.64 @ 2025-04-29 15:16:00
- **Stop Loss**: 20064.01
- **Risk**: 40.38 points
- **TP 1RR**: 19983.26 ✅
- **TP 1.5RR**: 19963.08 ✅
- **TP 2RR**: 19942.89 ✅
- **TP 2.5RR**: 19922.70 ✅
- **TP 3RR**: 19902.51 ✅
- **TP 3.5RR**: 19882.33 ✅
- **TP 4RR**: 19862.14 ✅
- **TP 4.5RR**: 19841.95 ✅
- **TP 5RR**: 19821.76 ✅
- **PnL**: 201.88 points (5.0R)
- **MFE**: 207.34 points
- **MAE**: 14.28 points

### Trade #568 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20037.41 - 20053.99
- **Entrée**: 20023.64 @ 2025-04-29 15:16:00
- **Stop Loss**: 20064.01
- **Risk**: 40.38 points
- **TP 1RR**: 19983.26 ✅
- **TP 1.5RR**: 19963.08 ✅
- **TP 2RR**: 19942.89 ✅
- **TP 2.5RR**: 19922.70 ✅
- **TP 3RR**: 19902.51 ✅
- **TP 3.5RR**: 19882.33 ✅
- **TP 4RR**: 19862.14 ✅
- **TP 4.5RR**: 19841.95 ✅
- **TP 5RR**: 19821.76 ✅
- **PnL**: 201.88 points (5.0R)
- **MFE**: 207.34 points
- **MAE**: 14.28 points

### Trade #569 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20037.41 - 20053.99
- **Entrée**: 20023.64 @ 2025-04-29 15:16:00
- **Stop Loss**: 20064.01
- **Risk**: 40.38 points
- **TP 1RR**: 19983.26 ✅
- **TP 1.5RR**: 19963.08 ✅
- **TP 2RR**: 19942.89 ✅
- **TP 2.5RR**: 19922.70 ✅
- **TP 3RR**: 19902.51 ✅
- **TP 3.5RR**: 19882.33 ✅
- **TP 4RR**: 19862.14 ✅
- **TP 4.5RR**: 19841.95 ✅
- **TP 5RR**: 19821.76 ✅
- **PnL**: 201.88 points (5.0R)
- **MFE**: 207.34 points
- **MAE**: 14.28 points

### Trade #570 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 01:00:00
- **FVG 5m**: 19909.90 - 19912.96
- **Entrée**: 19936.68 @ 2025-04-30 01:01:00
- **Stop Loss**: 19899.94
- **Risk**: 36.73 points
- **TP 1RR**: 19973.41 ✅
- **TP 1.5RR**: 19991.77 ✅
- **TP 2RR**: 20010.14 ✅
- **TP 2.5RR**: 20028.51 ❌
- **TP 3RR**: 20046.87 ❌
- **TP 3.5RR**: 20065.24 ❌
- **TP 4RR**: 20083.61 ❌
- **TP 4.5RR**: 20101.97 ❌
- **TP 5RR**: 20120.34 ❌
- **PnL**: -36.73 points (-1.0R)
- **MFE**: 80.59 points
- **MAE**: 38.00 points

### Trade #571 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 08:15:00
- **FVG 5m**: 19662.27 - 19668.39
- **Entrée**: 19679.86 @ 2025-04-30 08:25:00
- **Stop Loss**: 19652.44
- **Risk**: 27.43 points
- **TP 1RR**: 19707.29 ❌
- **TP 1.5RR**: 19721.01 ❌
- **TP 2RR**: 19734.72 ❌
- **TP 2.5RR**: 19748.43 ❌
- **TP 3RR**: 19762.15 ❌
- **TP 3.5RR**: 19775.86 ❌
- **TP 4RR**: 19789.58 ❌
- **TP 4.5RR**: 19803.29 ❌
- **TP 5RR**: 19817.00 ❌
- **PnL**: -27.43 points (-1.0R)
- **MFE**: 15.81 points
- **MAE**: 56.87 points

### Trade #572 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 09:00:00
- **FVG 5m**: 19594.69 - 19616.87
- **Entrée**: 19627.84 @ 2025-04-30 09:13:00
- **Stop Loss**: 19584.89
- **Risk**: 42.95 points
- **TP 1RR**: 19670.79 ✅
- **TP 1.5RR**: 19692.26 ✅
- **TP 2RR**: 19713.74 ✅
- **TP 2.5RR**: 19735.22 ✅
- **TP 3RR**: 19756.69 ✅
- **TP 3.5RR**: 19778.17 ✅
- **TP 4RR**: 19799.64 ✅
- **TP 4.5RR**: 19821.12 ✅
- **TP 5RR**: 19842.59 ✅
- **PnL**: 214.75 points (5.0R)
- **MFE**: 218.30 points
- **MAE**: 6.12 points

### Trade #573 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 09:00:00
- **FVG 5m**: 19594.69 - 19616.87
- **Entrée**: 19627.84 @ 2025-04-30 09:13:00
- **Stop Loss**: 19584.89
- **Risk**: 42.95 points
- **TP 1RR**: 19670.79 ✅
- **TP 1.5RR**: 19692.26 ✅
- **TP 2RR**: 19713.74 ✅
- **TP 2.5RR**: 19735.22 ✅
- **TP 3RR**: 19756.69 ✅
- **TP 3.5RR**: 19778.17 ✅
- **TP 4RR**: 19799.64 ✅
- **TP 4.5RR**: 19821.12 ✅
- **TP 5RR**: 19842.59 ✅
- **PnL**: 214.75 points (5.0R)
- **MFE**: 218.30 points
- **MAE**: 6.12 points

### Trade #574 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 09:00:00
- **FVG 5m**: 19594.69 - 19616.87
- **Entrée**: 19627.84 @ 2025-04-30 09:13:00
- **Stop Loss**: 19584.89
- **Risk**: 42.95 points
- **TP 1RR**: 19670.79 ✅
- **TP 1.5RR**: 19692.26 ✅
- **TP 2RR**: 19713.74 ✅
- **TP 2.5RR**: 19735.22 ✅
- **TP 3RR**: 19756.69 ✅
- **TP 3.5RR**: 19778.17 ✅
- **TP 4RR**: 19799.64 ✅
- **TP 4.5RR**: 19821.12 ✅
- **TP 5RR**: 19842.59 ✅
- **PnL**: 214.75 points (5.0R)
- **MFE**: 218.30 points
- **MAE**: 6.12 points

### Trade #575 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 10:00:00
- **FVG 5m**: 19594.69 - 19616.87
- **Entrée**: 19754.33 @ 2025-04-30 10:01:00
- **Stop Loss**: 19584.89
- **Risk**: 169.44 points
- **TP 1RR**: 19923.78 ✅
- **TP 1.5RR**: 20008.50 ✅
- **TP 2RR**: 20093.22 ✅
- **TP 2.5RR**: 20177.94 ✅
- **TP 3RR**: 20262.66 ✅
- **TP 3.5RR**: 20347.38 ✅
- **TP 4RR**: 20432.11 ✅
- **TP 4.5RR**: 20516.83 ✅
- **TP 5RR**: 20601.55 ✅
- **PnL**: 847.22 points (5.0R)
- **MFE**: 849.75 points
- **MAE**: 28.56 points

### Trade #576 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 12:30:00
- **FVG 5m**: 19780.60 - 19815.79
- **Entrée**: 19852.26 @ 2025-04-30 12:31:00
- **Stop Loss**: 19770.71
- **Risk**: 81.55 points
- **TP 1RR**: 19933.81 ✅
- **TP 1.5RR**: 19974.59 ✅
- **TP 2RR**: 20015.37 ✅
- **TP 2.5RR**: 20056.14 ✅
- **TP 3RR**: 20096.92 ✅
- **TP 3.5RR**: 20137.70 ✅
- **TP 4RR**: 20178.47 ✅
- **TP 4.5RR**: 20219.25 ✅
- **TP 5RR**: 20260.03 ✅
- **PnL**: 407.76 points (5.0R)
- **MFE**: 416.20 points
- **MAE**: 13.77 points

### Trade #577 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 12:30:00
- **FVG 5m**: 19780.60 - 19815.79
- **Entrée**: 19852.26 @ 2025-04-30 12:31:00
- **Stop Loss**: 19770.71
- **Risk**: 81.55 points
- **TP 1RR**: 19933.81 ✅
- **TP 1.5RR**: 19974.59 ✅
- **TP 2RR**: 20015.37 ✅
- **TP 2.5RR**: 20056.14 ✅
- **TP 3RR**: 20096.92 ✅
- **TP 3.5RR**: 20137.70 ✅
- **TP 4RR**: 20178.47 ✅
- **TP 4.5RR**: 20219.25 ✅
- **TP 5RR**: 20260.03 ✅
- **PnL**: 407.76 points (5.0R)
- **MFE**: 416.20 points
- **MAE**: 13.77 points

### Trade #578 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 13:00:00
- **FVG 5m**: 19854.05 - 19873.68
- **Entrée**: 19852.26 @ 2025-04-30 13:39:00
- **Stop Loss**: 19883.62
- **Risk**: 31.36 points
- **TP 1RR**: 19820.90 ❌
- **TP 1.5RR**: 19805.22 ❌
- **TP 2RR**: 19789.54 ❌
- **TP 2.5RR**: 19773.86 ❌
- **TP 3RR**: 19758.18 ❌
- **TP 3.5RR**: 19742.51 ❌
- **TP 4RR**: 19726.83 ❌
- **TP 4.5RR**: 19711.15 ❌
- **TP 5RR**: 19695.47 ❌
- **PnL**: -31.36 points (-1.0R)
- **MFE**: 13.77 points
- **MAE**: 31.88 points

### Trade #579 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 13:00:00
- **FVG 5m**: 19780.60 - 19815.79
- **Entrée**: 19856.34 @ 2025-04-30 13:01:00
- **Stop Loss**: 19770.71
- **Risk**: 85.63 points
- **TP 1RR**: 19941.98 ✅
- **TP 1.5RR**: 19984.79 ✅
- **TP 2RR**: 20027.61 ✅
- **TP 2.5RR**: 20070.42 ✅
- **TP 3RR**: 20113.24 ✅
- **TP 3.5RR**: 20156.06 ✅
- **TP 4RR**: 20198.87 ✅
- **TP 4.5RR**: 20241.69 ✅
- **TP 5RR**: 20284.51 ✅
- **PnL**: 428.17 points (5.0R)
- **MFE**: 429.46 points
- **MAE**: 17.85 points

### Trade #580 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 13:30:00
- **FVG 5m**: 19875.72 - 19890.52
- **Entrée**: 19870.88 @ 2025-04-30 13:35:00
- **Stop Loss**: 19900.46
- **Risk**: 29.58 points
- **TP 1RR**: 19841.30 ✅
- **TP 1.5RR**: 19826.51 ❌
- **TP 2RR**: 19811.71 ❌
- **TP 2.5RR**: 19796.92 ❌
- **TP 3RR**: 19782.13 ❌
- **TP 3.5RR**: 19767.34 ❌
- **TP 4RR**: 19752.55 ❌
- **TP 4.5RR**: 19737.76 ❌
- **TP 5RR**: 19722.97 ❌
- **PnL**: -29.58 points (-1.0R)
- **MFE**: 32.39 points
- **MAE**: 45.90 points

### Trade #581 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 19:15:00
- **FVG 5m**: 20320.74 - 20327.12
- **Entrée**: 20319.47 @ 2025-04-30 19:32:00
- **Stop Loss**: 20337.28
- **Risk**: 17.81 points
- **TP 1RR**: 20301.66 ❌
- **TP 1.5RR**: 20292.75 ❌
- **TP 2RR**: 20283.84 ❌
- **TP 2.5RR**: 20274.93 ❌
- **TP 3RR**: 20266.03 ❌
- **TP 3.5RR**: 20257.12 ❌
- **TP 4RR**: 20248.21 ❌
- **TP 4.5RR**: 20239.31 ❌
- **TP 5RR**: 20230.40 ❌
- **PnL**: -17.81 points (-1.0R)
- **MFE**: 2.04 points
- **MAE**: 17.85 points

### Trade #582 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 23:00:00
- **FVG 5m**: 20348.29 - 20356.19
- **Entrée**: 20345.48 @ 2025-04-30 23:23:00
- **Stop Loss**: 20366.37
- **Risk**: 20.89 points
- **TP 1RR**: 20324.59 ❌
- **TP 1.5RR**: 20314.15 ❌
- **TP 2RR**: 20303.70 ❌
- **TP 2.5RR**: 20293.26 ❌
- **TP 3RR**: 20282.81 ❌
- **TP 3.5RR**: 20272.37 ❌
- **TP 4RR**: 20261.93 ❌
- **TP 4.5RR**: 20251.48 ❌
- **TP 5RR**: 20241.04 ❌
- **PnL**: -20.89 points (-1.0R)
- **MFE**: 19.64 points
- **MAE**: 22.95 points

### Trade #583 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 02:30:00
- **FVG 5m**: 20323.04 - 20325.85
- **Entrée**: 20352.37 @ 2025-05-01 02:31:00
- **Stop Loss**: 20312.88
- **Risk**: 39.49 points
- **TP 1RR**: 20391.86 ✅
- **TP 1.5RR**: 20411.60 ✅
- **TP 2RR**: 20431.35 ✅
- **TP 2.5RR**: 20451.09 ❌
- **TP 3RR**: 20470.84 ❌
- **TP 3.5RR**: 20490.58 ❌
- **TP 4RR**: 20510.33 ❌
- **TP 4.5RR**: 20530.07 ❌
- **TP 5RR**: 20549.82 ❌
- **PnL**: -39.49 points (-1.0R)
- **MFE**: 86.20 points
- **MAE**: 49.22 points

### Trade #584 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 07:45:00
- **FVG 5m**: 20408.22 - 20413.06
- **Entrée**: 20379.66 @ 2025-05-01 07:46:00
- **Stop Loss**: 20423.27
- **Risk**: 43.61 points
- **TP 1RR**: 20336.04 ✅
- **TP 1.5RR**: 20314.23 ✅
- **TP 2RR**: 20292.43 ✅
- **TP 2.5RR**: 20270.62 ✅
- **TP 3RR**: 20248.81 ❌
- **TP 3.5RR**: 20227.00 ❌
- **TP 4RR**: 20205.20 ❌
- **TP 4.5RR**: 20183.39 ❌
- **TP 5RR**: 20161.58 ❌
- **PnL**: -43.61 points (-1.0R)
- **MFE**: 120.37 points
- **MAE**: 47.94 points

### Trade #585 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 07:45:00
- **FVG 5m**: 20408.22 - 20413.06
- **Entrée**: 20379.66 @ 2025-05-01 07:46:00
- **Stop Loss**: 20423.27
- **Risk**: 43.61 points
- **TP 1RR**: 20336.04 ✅
- **TP 1.5RR**: 20314.23 ✅
- **TP 2RR**: 20292.43 ✅
- **TP 2.5RR**: 20270.62 ✅
- **TP 3RR**: 20248.81 ❌
- **TP 3.5RR**: 20227.00 ❌
- **TP 4RR**: 20205.20 ❌
- **TP 4.5RR**: 20183.39 ❌
- **TP 5RR**: 20161.58 ❌
- **PnL**: -43.61 points (-1.0R)
- **MFE**: 120.37 points
- **MAE**: 47.94 points

### Trade #586 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 10:30:00
- **FVG 5m**: 20479.88 - 20482.94
- **Entrée**: 20466.36 @ 2025-05-01 10:31:00
- **Stop Loss**: 20493.18
- **Risk**: 26.82 points
- **TP 1RR**: 20439.55 ✅
- **TP 1.5RR**: 20426.14 ✅
- **TP 2RR**: 20412.73 ✅
- **TP 2.5RR**: 20399.32 ✅
- **TP 3RR**: 20385.91 ✅
- **TP 3.5RR**: 20372.50 ✅
- **TP 4RR**: 20359.09 ✅
- **TP 4.5RR**: 20345.68 ✅
- **TP 5RR**: 20332.27 ✅
- **PnL**: 134.09 points (5.0R)
- **MFE**: 150.98 points
- **MAE**: 10.71 points

### Trade #587 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 19:15:00
- **FVG 5m**: 20202.16 - 20208.53
- **Entrée**: 20212.61 @ 2025-05-01 19:17:00
- **Stop Loss**: 20192.06
- **Risk**: 20.56 points
- **TP 1RR**: 20233.17 ✅
- **TP 1.5RR**: 20243.45 ✅
- **TP 2RR**: 20253.73 ✅
- **TP 2.5RR**: 20264.01 ✅
- **TP 3RR**: 20274.29 ✅
- **TP 3.5RR**: 20284.56 ✅
- **TP 4RR**: 20294.84 ✅
- **TP 4.5RR**: 20305.12 ✅
- **TP 5RR**: 20315.40 ✅
- **PnL**: 102.79 points (5.0R)
- **MFE**: 109.15 points
- **MAE**: 14.54 points

### Trade #588 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 23:15:00
- **FVG 5m**: 20382.72 - 20384.76
- **Entrée**: 20376.85 @ 2025-05-01 23:21:00
- **Stop Loss**: 20394.95
- **Risk**: 18.10 points
- **TP 1RR**: 20358.75 ❌
- **TP 1.5RR**: 20349.70 ❌
- **TP 2RR**: 20340.65 ❌
- **TP 2.5RR**: 20331.61 ❌
- **TP 3RR**: 20322.56 ❌
- **TP 3.5RR**: 20313.51 ❌
- **TP 4RR**: 20304.46 ❌
- **TP 4.5RR**: 20295.41 ❌
- **TP 5RR**: 20286.36 ❌
- **PnL**: -18.10 points (-1.0R)
- **MFE**: 9.95 points
- **MAE**: 19.13 points

### Trade #589 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 01:15:00
- **FVG 5m**: 20343.95 - 20346.50
- **Entrée**: 20348.80 @ 2025-05-02 02:02:00
- **Stop Loss**: 20333.78
- **Risk**: 15.02 points
- **TP 1RR**: 20363.82 ❌
- **TP 1.5RR**: 20371.32 ❌
- **TP 2RR**: 20378.83 ❌
- **TP 2.5RR**: 20386.34 ❌
- **TP 3RR**: 20393.85 ❌
- **TP 3.5RR**: 20401.36 ❌
- **TP 4RR**: 20408.87 ❌
- **TP 4.5RR**: 20416.38 ❌
- **TP 5RR**: 20423.89 ❌
- **PnL**: -15.02 points (-1.0R)
- **MFE**: 1.02 points
- **MAE**: 16.83 points

### Trade #590 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 01:15:00
- **FVG 5m**: 20343.95 - 20346.50
- **Entrée**: 20348.80 @ 2025-05-02 02:02:00
- **Stop Loss**: 20333.78
- **Risk**: 15.02 points
- **TP 1RR**: 20363.82 ❌
- **TP 1.5RR**: 20371.32 ❌
- **TP 2RR**: 20378.83 ❌
- **TP 2.5RR**: 20386.34 ❌
- **TP 3RR**: 20393.85 ❌
- **TP 3.5RR**: 20401.36 ❌
- **TP 4RR**: 20408.87 ❌
- **TP 4.5RR**: 20416.38 ❌
- **TP 5RR**: 20423.89 ❌
- **PnL**: -15.02 points (-1.0R)
- **MFE**: 1.02 points
- **MAE**: 16.83 points

### Trade #591 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 04:00:00
- **FVG 5m**: 20296.77 - 20309.78
- **Entrée**: 20312.33 @ 2025-05-02 04:20:00
- **Stop Loss**: 20286.62
- **Risk**: 25.70 points
- **TP 1RR**: 20338.03 ✅
- **TP 1.5RR**: 20350.89 ✅
- **TP 2RR**: 20363.74 ✅
- **TP 2.5RR**: 20376.59 ✅
- **TP 3RR**: 20389.44 ✅
- **TP 3.5RR**: 20402.30 ✅
- **TP 4RR**: 20415.15 ✅
- **TP 4.5RR**: 20428.00 ✅
- **TP 5RR**: 20440.85 ✅
- **PnL**: 128.52 points (5.0R)
- **MFE**: 137.97 points
- **MAE**: 23.46 points

### Trade #592 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 11:00:00
- **FVG 5m**: 20566.08 - 20572.97
- **Entrée**: 20622.19 @ 2025-05-02 11:01:00
- **Stop Loss**: 20555.80
- **Risk**: 66.39 points
- **TP 1RR**: 20688.57 ❌
- **TP 1.5RR**: 20721.77 ❌
- **TP 2RR**: 20754.96 ❌
- **TP 2.5RR**: 20788.16 ❌
- **TP 3RR**: 20821.35 ❌
- **TP 3.5RR**: 20854.55 ❌
- **TP 4RR**: 20887.74 ❌
- **TP 4.5RR**: 20920.94 ❌
- **TP 5RR**: 20954.13 ❌
- **PnL**: -66.39 points (-1.0R)
- **MFE**: 62.23 points
- **MAE**: 82.12 points

### Trade #593 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 11:00:00
- **FVG 5m**: 20566.08 - 20572.97
- **Entrée**: 20622.19 @ 2025-05-02 11:01:00
- **Stop Loss**: 20555.80
- **Risk**: 66.39 points
- **TP 1RR**: 20688.57 ❌
- **TP 1.5RR**: 20721.77 ❌
- **TP 2RR**: 20754.96 ❌
- **TP 2.5RR**: 20788.16 ❌
- **TP 3RR**: 20821.35 ❌
- **TP 3.5RR**: 20854.55 ❌
- **TP 4RR**: 20887.74 ❌
- **TP 4.5RR**: 20920.94 ❌
- **TP 5RR**: 20954.13 ❌
- **PnL**: -66.39 points (-1.0R)
- **MFE**: 62.23 points
- **MAE**: 82.12 points

### Trade #594 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-02 13:30:00
- **FVG 5m**: 20632.90 - 20647.69
- **Entrée**: 20618.62 @ 2025-05-02 13:49:00
- **Stop Loss**: 20658.01
- **Risk**: 39.40 points
- **TP 1RR**: 20579.22 ✅
- **TP 1.5RR**: 20559.52 ✅
- **TP 2RR**: 20539.82 ✅
- **TP 2.5RR**: 20520.12 ✅
- **TP 3RR**: 20500.42 ✅
- **TP 3.5RR**: 20480.73 ✅
- **TP 4RR**: 20461.03 ✅
- **TP 4.5RR**: 20441.33 ✅
- **TP 5RR**: 20421.63 ✅
- **PnL**: 196.98 points (5.0R)
- **MFE**: 221.36 points
- **MAE**: 23.97 points

### Trade #595 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-02 14:00:00
- **FVG 5m**: 20661.97 - 20664.27
- **Entrée**: 20616.07 @ 2025-05-02 14:01:00
- **Stop Loss**: 20674.60
- **Risk**: 58.53 points
- **TP 1RR**: 20557.53 ✅
- **TP 1.5RR**: 20528.27 ✅
- **TP 2RR**: 20499.00 ✅
- **TP 2.5RR**: 20469.74 ✅
- **TP 3RR**: 20440.47 ✅
- **TP 3.5RR**: 20411.20 ✅
- **TP 4RR**: 20381.94 ✅
- **TP 4.5RR**: 20352.67 ✅
- **TP 5RR**: 20323.40 ✅
- **PnL**: 292.66 points (5.0R)
- **MFE**: 302.97 points
- **MAE**: 26.27 points

### Trade #596 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-04 20:45:00
- **FVG 5m**: 20489.06 - 20492.63
- **Entrée**: 20430.41 @ 2025-05-04 20:46:00
- **Stop Loss**: 20502.88
- **Risk**: 72.47 points
- **TP 1RR**: 20357.93 ❌
- **TP 1.5RR**: 20321.70 ❌
- **TP 2RR**: 20285.46 ❌
- **TP 2.5RR**: 20249.22 ❌
- **TP 3RR**: 20212.99 ❌
- **TP 3.5RR**: 20176.75 ❌
- **TP 4RR**: 20140.52 ❌
- **TP 4.5RR**: 20104.28 ❌
- **TP 5RR**: 20068.04 ❌
- **PnL**: -72.47 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 84.92 points

### Trade #597 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-04 22:30:00
- **FVG 5m**: 20410.00 - 20422.50
- **Entrée**: 20433.47 @ 2025-05-04 22:31:00
- **Stop Loss**: 20399.80
- **Risk**: 33.67 points
- **TP 1RR**: 20467.13 ✅
- **TP 1.5RR**: 20483.97 ✅
- **TP 2RR**: 20500.80 ✅
- **TP 2.5RR**: 20517.63 ❌
- **TP 3RR**: 20534.47 ❌
- **TP 3.5RR**: 20551.30 ❌
- **TP 4RR**: 20568.14 ❌
- **TP 4.5RR**: 20584.97 ❌
- **TP 5RR**: 20601.80 ❌
- **PnL**: -33.67 points (-1.0R)
- **MFE**: 69.37 points
- **MAE**: 38.76 points

### Trade #598 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-05 01:45:00
- **FVG 5m**: 20489.06 - 20491.36
- **Entrée**: 20483.45 @ 2025-05-05 01:46:00
- **Stop Loss**: 20501.60
- **Risk**: 18.15 points
- **TP 1RR**: 20465.30 ✅
- **TP 1.5RR**: 20456.22 ✅
- **TP 2RR**: 20447.15 ✅
- **TP 2.5RR**: 20438.07 ✅
- **TP 3RR**: 20429.00 ✅
- **TP 3.5RR**: 20419.92 ✅
- **TP 4RR**: 20410.85 ✅
- **TP 4.5RR**: 20401.77 ✅
- **TP 5RR**: 20392.69 ✅
- **PnL**: 90.76 points (5.0R)
- **MFE**: 104.56 points
- **MAE**: 0.00 points

### Trade #599 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-05 06:45:00
- **FVG 5m**: 20383.74 - 20389.86
- **Entrée**: 20390.11 @ 2025-05-05 06:47:00
- **Stop Loss**: 20373.54
- **Risk**: 16.57 points
- **TP 1RR**: 20406.68 ❌
- **TP 1.5RR**: 20414.96 ❌
- **TP 2RR**: 20423.25 ❌
- **TP 2.5RR**: 20431.53 ❌
- **TP 3RR**: 20439.81 ❌
- **TP 3.5RR**: 20448.10 ❌
- **TP 4RR**: 20456.38 ❌
- **TP 4.5RR**: 20464.67 ❌
- **TP 5RR**: 20472.95 ❌
- **PnL**: -16.57 points (-1.0R)
- **MFE**: 0.77 points
- **MAE**: 19.38 points

### Trade #600 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-05 08:30:00
- **FVG 5m**: 20383.74 - 20389.86
- **Entrée**: 20419.18 @ 2025-05-05 08:31:00
- **Stop Loss**: 20373.54
- **Risk**: 45.64 points
- **TP 1RR**: 20464.83 ✅
- **TP 1.5RR**: 20487.65 ✅
- **TP 2RR**: 20510.47 ✅
- **TP 2.5RR**: 20533.29 ✅
- **TP 3RR**: 20556.11 ✅
- **TP 3.5RR**: 20578.93 ✅
- **TP 4RR**: 20601.75 ❌
- **TP 4.5RR**: 20624.57 ❌
- **TP 5RR**: 20647.39 ❌
- **PnL**: -45.64 points (-1.0R)
- **MFE**: 178.26 points
- **MAE**: 55.60 points

### Trade #601 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-05 10:15:00
- **FVG 5m**: 20495.95 - 20500.28
- **Entrée**: 20490.85 @ 2025-05-05 10:16:00
- **Stop Loss**: 20510.53
- **Risk**: 19.69 points
- **TP 1RR**: 20471.16 ❌
- **TP 1.5RR**: 20461.32 ❌
- **TP 2RR**: 20451.48 ❌
- **TP 2.5RR**: 20441.63 ❌
- **TP 3RR**: 20431.79 ❌
- **TP 3.5RR**: 20421.95 ❌
- **TP 4RR**: 20412.10 ❌
- **TP 4.5RR**: 20402.26 ❌
- **TP 5RR**: 20392.42 ❌
- **PnL**: -19.69 points (-1.0R)
- **MFE**: 4.08 points
- **MAE**: 20.15 points

### Trade #602 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 01:00:00
- **FVG 5m**: 20340.64 - 20342.93
- **Entrée**: 20343.19 @ 2025-05-06 01:05:00
- **Stop Loss**: 20330.47
- **Risk**: 12.72 points
- **TP 1RR**: 20355.91 ✅
- **TP 1.5RR**: 20362.27 ✅
- **TP 2RR**: 20368.63 ✅
- **TP 2.5RR**: 20374.99 ✅
- **TP 3RR**: 20381.35 ❌
- **TP 3.5RR**: 20387.71 ❌
- **TP 4RR**: 20394.07 ❌
- **TP 4.5RR**: 20400.43 ❌
- **TP 5RR**: 20406.79 ❌
- **PnL**: -12.72 points (-1.0R)
- **MFE**: 33.15 points
- **MAE**: 20.66 points

### Trade #603 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 03:30:00
- **FVG 5m**: 20256.48 - 20271.27
- **Entrée**: 20271.78 @ 2025-05-06 03:42:00
- **Stop Loss**: 20246.35
- **Risk**: 25.43 points
- **TP 1RR**: 20297.21 ❌
- **TP 1.5RR**: 20309.92 ❌
- **TP 2RR**: 20322.64 ❌
- **TP 2.5RR**: 20335.35 ❌
- **TP 3RR**: 20348.07 ❌
- **TP 3.5RR**: 20360.78 ❌
- **TP 4RR**: 20373.50 ❌
- **TP 4.5RR**: 20386.21 ❌
- **TP 5RR**: 20398.93 ❌
- **PnL**: -25.43 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 26.01 points

### Trade #604 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 09:00:00
- **FVG 5m**: 20180.99 - 20195.02
- **Entrée**: 20198.33 @ 2025-05-06 09:05:00
- **Stop Loss**: 20170.90
- **Risk**: 27.43 points
- **TP 1RR**: 20225.76 ✅
- **TP 1.5RR**: 20239.48 ✅
- **TP 2RR**: 20253.20 ✅
- **TP 2.5RR**: 20266.91 ✅
- **TP 3RR**: 20280.63 ✅
- **TP 3.5RR**: 20294.35 ✅
- **TP 4RR**: 20308.06 ✅
- **TP 4.5RR**: 20321.78 ✅
- **TP 5RR**: 20335.49 ✅
- **PnL**: 137.16 points (5.0R)
- **MFE**: 140.26 points
- **MAE**: 16.32 points

### Trade #605 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 09:00:00
- **FVG 5m**: 20180.99 - 20195.02
- **Entrée**: 20198.33 @ 2025-05-06 09:05:00
- **Stop Loss**: 20170.90
- **Risk**: 27.43 points
- **TP 1RR**: 20225.76 ✅
- **TP 1.5RR**: 20239.48 ✅
- **TP 2RR**: 20253.20 ✅
- **TP 2.5RR**: 20266.91 ✅
- **TP 3RR**: 20280.63 ✅
- **TP 3.5RR**: 20294.35 ✅
- **TP 4RR**: 20308.06 ✅
- **TP 4.5RR**: 20321.78 ✅
- **TP 5RR**: 20335.49 ✅
- **PnL**: 137.16 points (5.0R)
- **MFE**: 140.26 points
- **MAE**: 16.32 points

### Trade #606 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 09:30:00
- **FVG 5m**: 20180.99 - 20195.02
- **Entrée**: 20286.83 @ 2025-05-06 09:31:00
- **Stop Loss**: 20170.90
- **Risk**: 115.93 points
- **TP 1RR**: 20402.75 ✅
- **TP 1.5RR**: 20460.72 ✅
- **TP 2RR**: 20518.68 ✅
- **TP 2.5RR**: 20576.64 ❌
- **TP 3RR**: 20634.61 ❌
- **TP 3.5RR**: 20692.57 ❌
- **TP 4RR**: 20750.53 ❌
- **TP 4.5RR**: 20808.50 ❌
- **TP 5RR**: 20866.46 ❌
- **PnL**: -115.93 points (-1.0R)
- **MFE**: 251.71 points
- **MAE**: 159.65 points

### Trade #607 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 10:15:00
- **FVG 5m**: 20180.99 - 20195.02
- **Entrée**: 20305.19 @ 2025-05-06 10:16:00
- **Stop Loss**: 20170.90
- **Risk**: 134.29 points
- **TP 1RR**: 20439.48 ✅
- **TP 1.5RR**: 20506.62 ✅
- **TP 2RR**: 20573.76 ❌
- **TP 2.5RR**: 20640.91 ❌
- **TP 3RR**: 20708.05 ❌
- **TP 3.5RR**: 20775.20 ❌
- **TP 4RR**: 20842.34 ❌
- **TP 4.5RR**: 20909.49 ❌
- **TP 5RR**: 20976.63 ❌
- **PnL**: -134.29 points (-1.0R)
- **MFE**: 233.35 points
- **MAE**: 178.01 points

### Trade #608 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 11:00:00
- **FVG 5m**: 20319.47 - 20336.05
- **Entrée**: 20347.01 @ 2025-05-06 11:12:00
- **Stop Loss**: 20309.31
- **Risk**: 37.70 points
- **TP 1RR**: 20384.72 ✅
- **TP 1.5RR**: 20403.57 ✅
- **TP 2RR**: 20422.42 ✅
- **TP 2.5RR**: 20441.27 ❌
- **TP 3RR**: 20460.12 ❌
- **TP 3.5RR**: 20478.97 ❌
- **TP 4RR**: 20497.82 ❌
- **TP 4.5RR**: 20516.67 ❌
- **TP 5RR**: 20535.53 ❌
- **PnL**: -37.70 points (-1.0R)
- **MFE**: 81.86 points
- **MAE**: 39.53 points

### Trade #609 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 11:00:00
- **FVG 5m**: 20319.47 - 20336.05
- **Entrée**: 20347.01 @ 2025-05-06 11:12:00
- **Stop Loss**: 20309.31
- **Risk**: 37.70 points
- **TP 1RR**: 20384.72 ✅
- **TP 1.5RR**: 20403.57 ✅
- **TP 2RR**: 20422.42 ✅
- **TP 2.5RR**: 20441.27 ❌
- **TP 3RR**: 20460.12 ❌
- **TP 3.5RR**: 20478.97 ❌
- **TP 4RR**: 20497.82 ❌
- **TP 4.5RR**: 20516.67 ❌
- **TP 5RR**: 20535.53 ❌
- **PnL**: -37.70 points (-1.0R)
- **MFE**: 81.86 points
- **MAE**: 39.53 points

### Trade #610 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 11:15:00
- **FVG 5m**: 20270.25 - 20280.71
- **Entrée**: 20269.48 @ 2025-05-06 11:56:00
- **Stop Loss**: 20290.85
- **Risk**: 21.36 points
- **TP 1RR**: 20248.12 ❌
- **TP 1.5RR**: 20237.44 ❌
- **TP 2RR**: 20226.76 ❌
- **TP 2.5RR**: 20216.08 ❌
- **TP 3RR**: 20205.40 ❌
- **TP 3.5RR**: 20194.72 ❌
- **TP 4RR**: 20184.04 ❌
- **TP 4.5RR**: 20173.36 ❌
- **TP 5RR**: 20162.68 ❌
- **PnL**: -21.36 points (-1.0R)
- **MFE**: 9.95 points
- **MAE**: 39.53 points

### Trade #611 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 11:15:00
- **FVG 5m**: 20270.25 - 20280.71
- **Entrée**: 20269.48 @ 2025-05-06 11:56:00
- **Stop Loss**: 20290.85
- **Risk**: 21.36 points
- **TP 1RR**: 20248.12 ❌
- **TP 1.5RR**: 20237.44 ❌
- **TP 2RR**: 20226.76 ❌
- **TP 2.5RR**: 20216.08 ❌
- **TP 3RR**: 20205.40 ❌
- **TP 3.5RR**: 20194.72 ❌
- **TP 4RR**: 20184.04 ❌
- **TP 4.5RR**: 20173.36 ❌
- **TP 5RR**: 20162.68 ❌
- **PnL**: -21.36 points (-1.0R)
- **MFE**: 9.95 points
- **MAE**: 39.53 points

### Trade #612 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 15:30:00
- **FVG 5m**: 20278.41 - 20308.76
- **Entrée**: 20352.11 @ 2025-05-06 17:00:00
- **Stop Loss**: 20268.27
- **Risk**: 83.84 points
- **TP 1RR**: 20435.95 ✅
- **TP 1.5RR**: 20477.88 ✅
- **TP 2RR**: 20519.80 ✅
- **TP 2.5RR**: 20561.72 ❌
- **TP 3RR**: 20603.64 ❌
- **TP 3.5RR**: 20645.56 ❌
- **TP 4RR**: 20687.48 ❌
- **TP 4.5RR**: 20729.40 ❌
- **TP 5RR**: 20771.32 ❌
- **PnL**: -83.84 points (-1.0R)
- **MFE**: 186.42 points
- **MAE**: 86.71 points

### Trade #613 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 19:00:00
- **FVG 5m**: 20450.04 - 20452.85
- **Entrée**: 20448.00 @ 2025-05-06 19:05:00
- **Stop Loss**: 20463.07
- **Risk**: 15.07 points
- **TP 1RR**: 20432.93 ✅
- **TP 1.5RR**: 20425.40 ✅
- **TP 2RR**: 20417.86 ✅
- **TP 2.5RR**: 20410.32 ✅
- **TP 3RR**: 20402.79 ❌
- **TP 3.5RR**: 20395.25 ❌
- **TP 4RR**: 20387.72 ❌
- **TP 4.5RR**: 20380.18 ❌
- **TP 5RR**: 20372.64 ❌
- **PnL**: -15.07 points (-1.0R)
- **MFE**: 40.55 points
- **MAE**: 16.58 points

### Trade #614 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 22:00:00
- **FVG 5m**: 20406.94 - 20417.40
- **Entrée**: 20418.42 @ 2025-05-06 22:12:00
- **Stop Loss**: 20396.74
- **Risk**: 21.68 points
- **TP 1RR**: 20440.10 ❌
- **TP 1.5RR**: 20450.94 ❌
- **TP 2RR**: 20461.78 ❌
- **TP 2.5RR**: 20472.62 ❌
- **TP 3RR**: 20483.46 ❌
- **TP 3.5RR**: 20494.30 ❌
- **TP 4RR**: 20505.14 ❌
- **TP 4.5RR**: 20515.98 ❌
- **TP 5RR**: 20526.82 ❌
- **PnL**: -21.68 points (-1.0R)
- **MFE**: 5.87 points
- **MAE**: 22.70 points

### Trade #615 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 01:45:00
- **FVG 5m**: 20374.30 - 20379.91
- **Entrée**: 20380.93 @ 2025-05-07 01:48:00
- **Stop Loss**: 20364.11
- **Risk**: 16.82 points
- **TP 1RR**: 20397.75 ✅
- **TP 1.5RR**: 20406.16 ✅
- **TP 2RR**: 20414.57 ✅
- **TP 2.5RR**: 20422.98 ✅
- **TP 3RR**: 20431.38 ✅
- **TP 3.5RR**: 20439.79 ❌
- **TP 4RR**: 20448.20 ❌
- **TP 4.5RR**: 20456.61 ❌
- **TP 5RR**: 20465.02 ❌
- **PnL**: -16.82 points (-1.0R)
- **MFE**: 52.03 points
- **MAE**: 23.46 points

### Trade #616 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 09:15:00
- **FVG 5m**: 20297.03 - 20305.70
- **Entrée**: 20339.36 @ 2025-05-07 09:16:00
- **Stop Loss**: 20286.88
- **Risk**: 52.48 points
- **TP 1RR**: 20391.84 ❌
- **TP 1.5RR**: 20418.09 ❌
- **TP 2RR**: 20444.33 ❌
- **TP 2.5RR**: 20470.57 ❌
- **TP 3RR**: 20496.81 ❌
- **TP 3.5RR**: 20523.05 ❌
- **TP 4RR**: 20549.29 ❌
- **TP 4.5RR**: 20575.53 ❌
- **TP 5RR**: 20601.78 ❌
- **PnL**: -52.48 points (-1.0R)
- **MFE**: 39.53 points
- **MAE**: 57.89 points

### Trade #617 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 09:15:00
- **FVG 5m**: 20297.03 - 20305.70
- **Entrée**: 20339.36 @ 2025-05-07 09:16:00
- **Stop Loss**: 20286.88
- **Risk**: 52.48 points
- **TP 1RR**: 20391.84 ❌
- **TP 1.5RR**: 20418.09 ❌
- **TP 2RR**: 20444.33 ❌
- **TP 2.5RR**: 20470.57 ❌
- **TP 3RR**: 20496.81 ❌
- **TP 3.5RR**: 20523.05 ❌
- **TP 4RR**: 20549.29 ❌
- **TP 4.5RR**: 20575.53 ❌
- **TP 5RR**: 20601.78 ❌
- **PnL**: -52.48 points (-1.0R)
- **MFE**: 39.53 points
- **MAE**: 57.89 points

### Trade #618 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 13:15:00
- **FVG 5m**: 20140.95 - 20192.47
- **Entrée**: 20212.87 @ 2025-05-07 13:32:00
- **Stop Loss**: 20130.88
- **Risk**: 81.99 points
- **TP 1RR**: 20294.86 ✅
- **TP 1.5RR**: 20335.85 ✅
- **TP 2RR**: 20376.84 ✅
- **TP 2.5RR**: 20417.84 ✅
- **TP 3RR**: 20458.83 ✅
- **TP 3.5RR**: 20499.83 ✅
- **TP 4RR**: 20540.82 ✅
- **TP 4.5RR**: 20581.81 ✅
- **TP 5RR**: 20622.81 ✅
- **PnL**: 409.94 points (5.0R)
- **MFE**: 419.01 points
- **MAE**: 71.41 points

### Trade #619 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 13:30:00
- **FVG 5m**: 20140.95 - 20192.47
- **Entrée**: 20212.87 @ 2025-05-07 13:32:00
- **Stop Loss**: 20130.88
- **Risk**: 81.99 points
- **TP 1RR**: 20294.86 ✅
- **TP 1.5RR**: 20335.85 ✅
- **TP 2RR**: 20376.84 ✅
- **TP 2.5RR**: 20417.84 ✅
- **TP 3RR**: 20458.83 ✅
- **TP 3.5RR**: 20499.83 ✅
- **TP 4RR**: 20540.82 ✅
- **TP 4.5RR**: 20581.81 ✅
- **TP 5RR**: 20622.81 ✅
- **PnL**: 409.94 points (5.0R)
- **MFE**: 419.01 points
- **MAE**: 71.41 points

### Trade #620 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:30:00
- **FVG 5m**: 20194.25 - 20243.47
- **Entrée**: 20179.21 @ 2025-05-07 14:32:00
- **Stop Loss**: 20253.59
- **Risk**: 74.39 points
- **TP 1RR**: 20104.82 ❌
- **TP 1.5RR**: 20067.62 ❌
- **TP 2RR**: 20030.43 ❌
- **TP 2.5RR**: 19993.23 ❌
- **TP 3RR**: 19956.04 ❌
- **TP 3.5RR**: 19918.85 ❌
- **TP 4RR**: 19881.65 ❌
- **TP 4.5RR**: 19844.46 ❌
- **TP 5RR**: 19807.26 ❌
- **PnL**: -74.39 points (-1.0R)
- **MFE**: 17.85 points
- **MAE**: 132.87 points

### Trade #621 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:30:00
- **FVG 5m**: 20194.25 - 20243.47
- **Entrée**: 20179.21 @ 2025-05-07 14:32:00
- **Stop Loss**: 20253.59
- **Risk**: 74.39 points
- **TP 1RR**: 20104.82 ❌
- **TP 1.5RR**: 20067.62 ❌
- **TP 2RR**: 20030.43 ❌
- **TP 2.5RR**: 19993.23 ❌
- **TP 3RR**: 19956.04 ❌
- **TP 3.5RR**: 19918.85 ❌
- **TP 4RR**: 19881.65 ❌
- **TP 4.5RR**: 19844.46 ❌
- **TP 5RR**: 19807.26 ❌
- **PnL**: -74.39 points (-1.0R)
- **MFE**: 17.85 points
- **MAE**: 132.87 points

### Trade #622 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:30:00
- **FVG 5m**: 20194.25 - 20243.47
- **Entrée**: 20179.21 @ 2025-05-07 14:32:00
- **Stop Loss**: 20253.59
- **Risk**: 74.39 points
- **TP 1RR**: 20104.82 ❌
- **TP 1.5RR**: 20067.62 ❌
- **TP 2RR**: 20030.43 ❌
- **TP 2.5RR**: 19993.23 ❌
- **TP 3RR**: 19956.04 ❌
- **TP 3.5RR**: 19918.85 ❌
- **TP 4RR**: 19881.65 ❌
- **TP 4.5RR**: 19844.46 ❌
- **TP 5RR**: 19807.26 ❌
- **PnL**: -74.39 points (-1.0R)
- **MFE**: 17.85 points
- **MAE**: 132.87 points

### Trade #623 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 06:30:00
- **FVG 5m**: 20652.28 - 20654.83
- **Entrée**: 20626.78 @ 2025-05-08 06:31:00
- **Stop Loss**: 20665.16
- **Risk**: 38.38 points
- **TP 1RR**: 20588.40 ✅
- **TP 1.5RR**: 20569.21 ✅
- **TP 2RR**: 20550.02 ✅
- **TP 2.5RR**: 20530.83 ✅
- **TP 3RR**: 20511.64 ✅
- **TP 3.5RR**: 20492.45 ✅
- **TP 4RR**: 20473.26 ✅
- **TP 4.5RR**: 20454.06 ✅
- **TP 5RR**: 20434.87 ✅
- **PnL**: 191.90 points (5.0R)
- **MFE**: 199.18 points
- **MAE**: 9.18 points

### Trade #624 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 07:30:00
- **FVG 5m**: 20610.45 - 20613.51
- **Entrée**: 20601.53 @ 2025-05-08 07:35:00
- **Stop Loss**: 20623.82
- **Risk**: 22.29 points
- **TP 1RR**: 20579.24 ✅
- **TP 1.5RR**: 20568.09 ✅
- **TP 2RR**: 20556.94 ✅
- **TP 2.5RR**: 20545.80 ✅
- **TP 3RR**: 20534.65 ✅
- **TP 3.5RR**: 20523.50 ✅
- **TP 4RR**: 20512.36 ✅
- **TP 4.5RR**: 20501.21 ✅
- **TP 5RR**: 20490.06 ✅
- **PnL**: 111.46 points (5.0R)
- **MFE**: 120.37 points
- **MAE**: 7.14 points

### Trade #625 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 08:30:00
- **FVG 5m**: 20575.01 - 20584.95
- **Entrée**: 20547.97 @ 2025-05-08 08:31:00
- **Stop Loss**: 20595.24
- **Risk**: 47.27 points
- **TP 1RR**: 20500.70 ✅
- **TP 1.5RR**: 20477.07 ✅
- **TP 2RR**: 20453.43 ✅
- **TP 2.5RR**: 20429.80 ✅
- **TP 3RR**: 20406.16 ✅
- **TP 3.5RR**: 20382.52 ✅
- **TP 4RR**: 20358.89 ❌
- **TP 4.5RR**: 20335.25 ❌
- **TP 5RR**: 20311.62 ❌
- **PnL**: -47.27 points (-1.0R)
- **MFE**: 167.30 points
- **MAE**: 54.32 points

### Trade #626 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 08:30:00
- **FVG 5m**: 20575.01 - 20584.95
- **Entrée**: 20547.97 @ 2025-05-08 08:31:00
- **Stop Loss**: 20595.24
- **Risk**: 47.27 points
- **TP 1RR**: 20500.70 ✅
- **TP 1.5RR**: 20477.07 ✅
- **TP 2RR**: 20453.43 ✅
- **TP 2.5RR**: 20429.80 ✅
- **TP 3RR**: 20406.16 ✅
- **TP 3.5RR**: 20382.52 ✅
- **TP 4RR**: 20358.89 ❌
- **TP 4.5RR**: 20335.25 ❌
- **TP 5RR**: 20311.62 ❌
- **PnL**: -47.27 points (-1.0R)
- **MFE**: 167.30 points
- **MAE**: 54.32 points

### Trade #627 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 09:00:00
- **FVG 5m**: 20575.01 - 20584.95
- **Entrée**: 20525.02 @ 2025-05-08 09:01:00
- **Stop Loss**: 20595.24
- **Risk**: 70.22 points
- **TP 1RR**: 20454.80 ✅
- **TP 1.5RR**: 20419.69 ✅
- **TP 2RR**: 20384.57 ✅
- **TP 2.5RR**: 20349.46 ❌
- **TP 3RR**: 20314.35 ❌
- **TP 3.5RR**: 20279.24 ❌
- **TP 4RR**: 20244.13 ❌
- **TP 4.5RR**: 20209.01 ❌
- **TP 5RR**: 20173.90 ❌
- **PnL**: -70.22 points (-1.0R)
- **MFE**: 144.34 points
- **MAE**: 77.27 points

### Trade #628 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-08 10:15:00
- **FVG 5m**: 20499.01 - 20503.09
- **Entrée**: 20505.64 @ 2025-05-08 10:18:00
- **Stop Loss**: 20488.76
- **Risk**: 16.88 points
- **TP 1RR**: 20522.52 ✅
- **TP 1.5RR**: 20530.96 ✅
- **TP 2RR**: 20539.40 ✅
- **TP 2.5RR**: 20547.84 ✅
- **TP 3RR**: 20556.28 ✅
- **TP 3.5RR**: 20564.72 ✅
- **TP 4RR**: 20573.16 ✅
- **TP 4.5RR**: 20581.60 ✅
- **TP 5RR**: 20590.04 ✅
- **PnL**: 84.40 points (5.0R)
- **MFE**: 96.65 points
- **MAE**: 8.42 points

### Trade #629 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-08 20:15:00
- **FVG 5m**: 20526.81 - 20529.87
- **Entrée**: 20539.30 @ 2025-05-08 20:16:00
- **Stop Loss**: 20516.54
- **Risk**: 22.76 points
- **TP 1RR**: 20562.06 ✅
- **TP 1.5RR**: 20573.44 ✅
- **TP 2RR**: 20584.82 ✅
- **TP 2.5RR**: 20596.20 ✅
- **TP 3RR**: 20607.58 ✅
- **TP 3.5RR**: 20618.96 ✅
- **TP 4RR**: 20630.34 ✅
- **TP 4.5RR**: 20641.72 ✅
- **TP 5RR**: 20653.10 ✅
- **PnL**: 113.80 points (5.0R)
- **MFE**: 114.51 points
- **MAE**: 10.46 points

### Trade #630 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-09 02:45:00
- **FVG 5m**: 20603.31 - 20610.20
- **Entrée**: 20600.25 @ 2025-05-09 02:58:00
- **Stop Loss**: 20620.50
- **Risk**: 20.25 points
- **TP 1RR**: 20580.00 ✅
- **TP 1.5RR**: 20569.88 ❌
- **TP 2RR**: 20559.75 ❌
- **TP 2.5RR**: 20549.63 ❌
- **TP 3RR**: 20539.50 ❌
- **TP 3.5RR**: 20529.37 ❌
- **TP 4RR**: 20519.25 ❌
- **TP 4.5RR**: 20509.12 ❌
- **TP 5RR**: 20499.00 ❌
- **PnL**: -20.25 points (-1.0R)
- **MFE**: 29.84 points
- **MAE**: 21.17 points

### Trade #631 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-09 02:45:00
- **FVG 5m**: 20603.31 - 20610.20
- **Entrée**: 20600.25 @ 2025-05-09 02:58:00
- **Stop Loss**: 20620.50
- **Risk**: 20.25 points
- **TP 1RR**: 20580.00 ✅
- **TP 1.5RR**: 20569.88 ❌
- **TP 2RR**: 20559.75 ❌
- **TP 2.5RR**: 20549.63 ❌
- **TP 3RR**: 20539.50 ❌
- **TP 3.5RR**: 20529.37 ❌
- **TP 4RR**: 20519.25 ❌
- **TP 4.5RR**: 20509.12 ❌
- **TP 5RR**: 20499.00 ❌
- **PnL**: -20.25 points (-1.0R)
- **MFE**: 29.84 points
- **MAE**: 21.17 points

### Trade #632 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 06:00:00
- **FVG 5m**: 20591.33 - 20594.39
- **Entrée**: 20635.19 @ 2025-05-09 06:01:00
- **Stop Loss**: 20581.03
- **Risk**: 54.16 points
- **TP 1RR**: 20689.35 ❌
- **TP 1.5RR**: 20716.43 ❌
- **TP 2RR**: 20743.51 ❌
- **TP 2.5RR**: 20770.59 ❌
- **TP 3RR**: 20797.67 ❌
- **TP 3.5RR**: 20824.75 ❌
- **TP 4RR**: 20851.83 ❌
- **TP 4.5RR**: 20878.91 ❌
- **TP 5RR**: 20905.99 ❌
- **PnL**: -54.16 points (-1.0R)
- **MFE**: 61.46 points
- **MAE**: 77.78 points

### Trade #633 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-09 06:15:00
- **FVG 5m**: 20629.33 - 20636.47
- **Entrée**: 20568.89 @ 2025-05-09 06:26:00
- **Stop Loss**: 20646.79
- **Risk**: 77.90 points
- **TP 1RR**: 20490.99 ❌
- **TP 1.5RR**: 20452.04 ❌
- **TP 2RR**: 20413.09 ❌
- **TP 2.5RR**: 20374.13 ❌
- **TP 3RR**: 20335.18 ❌
- **TP 3.5RR**: 20296.23 ❌
- **TP 4RR**: 20257.28 ❌
- **TP 4.5RR**: 20218.33 ❌
- **TP 5RR**: 20179.38 ❌
- **PnL**: -77.90 points (-1.0R)
- **MFE**: 23.97 points
- **MAE**: 94.36 points

### Trade #634 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 09:45:00
- **FVG 5m**: 20516.35 - 20521.71
- **Entrée**: 20522.22 @ 2025-05-09 09:48:00
- **Stop Loss**: 20506.09
- **Risk**: 16.12 points
- **TP 1RR**: 20538.34 ✅
- **TP 1.5RR**: 20546.40 ✅
- **TP 2RR**: 20554.46 ❌
- **TP 2.5RR**: 20562.53 ❌
- **TP 3RR**: 20570.59 ❌
- **TP 3.5RR**: 20578.65 ❌
- **TP 4RR**: 20586.71 ❌
- **TP 4.5RR**: 20594.77 ❌
- **TP 5RR**: 20602.83 ❌
- **PnL**: -16.12 points (-1.0R)
- **MFE**: 24.74 points
- **MAE**: 20.40 points

### Trade #635 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-11 17:30:00
- **FVG 5m**: 20835.39 - 20855.02
- **Entrée**: 20869.05 @ 2025-05-11 18:16:00
- **Stop Loss**: 20824.97
- **Risk**: 44.08 points
- **TP 1RR**: 20913.13 ✅
- **TP 1.5RR**: 20935.17 ✅
- **TP 2RR**: 20957.21 ✅
- **TP 2.5RR**: 20979.25 ✅
- **TP 3RR**: 21001.29 ✅
- **TP 3.5RR**: 21023.34 ✅
- **TP 4RR**: 21045.38 ✅
- **TP 4.5RR**: 21067.42 ✅
- **TP 5RR**: 21089.46 ✅
- **PnL**: 220.41 points (5.0R)
- **MFE**: 328.22 points
- **MAE**: 17.09 points

### Trade #636 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-11 20:30:00
- **FVG 5m**: 20933.57 - 20949.89
- **Entrée**: 20930.26 @ 2025-05-11 20:40:00
- **Stop Loss**: 20960.37
- **Risk**: 30.11 points
- **TP 1RR**: 20900.15 ❌
- **TP 1.5RR**: 20885.09 ❌
- **TP 2RR**: 20870.03 ❌
- **TP 2.5RR**: 20854.98 ❌
- **TP 3RR**: 20839.92 ❌
- **TP 3.5RR**: 20824.87 ❌
- **TP 4RR**: 20809.81 ❌
- **TP 4.5RR**: 20794.75 ❌
- **TP 5RR**: 20779.70 ❌
- **PnL**: -30.11 points (-1.0R)
- **MFE**: 14.54 points
- **MAE**: 34.17 points

### Trade #637 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 02:00:00
- **FVG 5m**: 20984.07 - 20990.70
- **Entrée**: 21188.34 @ 2025-05-12 02:01:00
- **Stop Loss**: 20973.58
- **Risk**: 214.77 points
- **TP 1RR**: 21403.11 ✅
- **TP 1.5RR**: 21510.50 ✅
- **TP 2RR**: 21617.88 ✅
- **TP 2.5RR**: 21725.26 ✅
- **TP 3RR**: 21832.65 ✅
- **TP 3.5RR**: 21940.03 ✅
- **TP 4RR**: 22047.42 ✅
- **TP 4.5RR**: 22154.80 ✅
- **TP 5RR**: 22262.18 ✅
- **PnL**: 1073.84 points (5.0R)
- **MFE**: 1084.12 points
- **MAE**: 82.37 points

### Trade #638 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 02:00:00
- **FVG 5m**: 20984.07 - 20990.70
- **Entrée**: 21188.34 @ 2025-05-12 02:01:00
- **Stop Loss**: 20973.58
- **Risk**: 214.77 points
- **TP 1RR**: 21403.11 ✅
- **TP 1.5RR**: 21510.50 ✅
- **TP 2RR**: 21617.88 ✅
- **TP 2.5RR**: 21725.26 ✅
- **TP 3RR**: 21832.65 ✅
- **TP 3.5RR**: 21940.03 ✅
- **TP 4RR**: 22047.42 ✅
- **TP 4.5RR**: 22154.80 ✅
- **TP 5RR**: 22262.18 ✅
- **PnL**: 1073.84 points (5.0R)
- **MFE**: 1084.12 points
- **MAE**: 82.37 points

### Trade #639 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 02:00:00
- **FVG 5m**: 20984.07 - 20990.70
- **Entrée**: 21188.34 @ 2025-05-12 02:01:00
- **Stop Loss**: 20973.58
- **Risk**: 214.77 points
- **TP 1RR**: 21403.11 ✅
- **TP 1.5RR**: 21510.50 ✅
- **TP 2RR**: 21617.88 ✅
- **TP 2.5RR**: 21725.26 ✅
- **TP 3RR**: 21832.65 ✅
- **TP 3.5RR**: 21940.03 ✅
- **TP 4RR**: 22047.42 ✅
- **TP 4.5RR**: 22154.80 ✅
- **TP 5RR**: 22262.18 ✅
- **PnL**: 1073.84 points (5.0R)
- **MFE**: 1084.12 points
- **MAE**: 82.37 points

### Trade #640 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 02:30:00
- **FVG 5m**: 21296.48 - 21311.27
- **Entrée**: 21291.37 @ 2025-05-12 02:35:00
- **Stop Loss**: 21321.92
- **Risk**: 30.55 points
- **TP 1RR**: 21260.83 ✅
- **TP 1.5RR**: 21245.55 ✅
- **TP 2RR**: 21230.28 ✅
- **TP 2.5RR**: 21215.01 ✅
- **TP 3RR**: 21199.73 ✅
- **TP 3.5RR**: 21184.46 ❌
- **TP 4RR**: 21169.18 ❌
- **TP 4.5RR**: 21153.91 ❌
- **TP 5RR**: 21138.64 ❌
- **PnL**: -30.55 points (-1.0R)
- **MFE**: 94.87 points
- **MAE**: 31.62 points

### Trade #641 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 02:30:00
- **FVG 5m**: 21296.48 - 21311.27
- **Entrée**: 21291.37 @ 2025-05-12 02:35:00
- **Stop Loss**: 21321.92
- **Risk**: 30.55 points
- **TP 1RR**: 21260.83 ✅
- **TP 1.5RR**: 21245.55 ✅
- **TP 2RR**: 21230.28 ✅
- **TP 2.5RR**: 21215.01 ✅
- **TP 3RR**: 21199.73 ✅
- **TP 3.5RR**: 21184.46 ❌
- **TP 4RR**: 21169.18 ❌
- **TP 4.5RR**: 21153.91 ❌
- **TP 5RR**: 21138.64 ❌
- **PnL**: -30.55 points (-1.0R)
- **MFE**: 94.87 points
- **MAE**: 31.62 points

### Trade #642 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 17:00:00
- **FVG 5m**: 21371.45 - 21374.51
- **Entrée**: 21359.72 @ 2025-05-12 17:01:00
- **Stop Loss**: 21385.20
- **Risk**: 25.48 points
- **TP 1RR**: 21334.24 ✅
- **TP 1.5RR**: 21321.50 ❌
- **TP 2RR**: 21308.76 ❌
- **TP 2.5RR**: 21296.02 ❌
- **TP 3RR**: 21283.29 ❌
- **TP 3.5RR**: 21270.55 ❌
- **TP 4RR**: 21257.81 ❌
- **TP 4.5RR**: 21245.07 ❌
- **TP 5RR**: 21232.33 ❌
- **PnL**: -25.48 points (-1.0R)
- **MFE**: 26.01 points
- **MAE**: 29.84 points

### Trade #643 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 02:15:00
- **FVG 5m**: 21753.99 - 21767.25
- **Entrée**: 21751.95 @ 2025-05-14 02:21:00
- **Stop Loss**: 21778.14
- **Risk**: 26.19 points
- **TP 1RR**: 21725.77 ✅
- **TP 1.5RR**: 21712.67 ✅
- **TP 2RR**: 21699.58 ✅
- **TP 2.5RR**: 21686.49 ✅
- **TP 3RR**: 21673.40 ✅
- **TP 3.5RR**: 21660.30 ❌
- **TP 4RR**: 21647.21 ❌
- **TP 4.5RR**: 21634.12 ❌
- **TP 5RR**: 21621.03 ❌
- **PnL**: -26.19 points (-1.0R)
- **MFE**: 86.71 points
- **MAE**: 26.52 points

### Trade #644 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 06:30:00
- **FVG 5m**: 21779.75 - 21784.34
- **Entrée**: 21777.45 @ 2025-05-14 06:45:00
- **Stop Loss**: 21795.23
- **Risk**: 17.78 points
- **TP 1RR**: 21759.68 ❌
- **TP 1.5RR**: 21750.79 ❌
- **TP 2RR**: 21741.90 ❌
- **TP 2.5RR**: 21733.01 ❌
- **TP 3RR**: 21724.12 ❌
- **TP 3.5RR**: 21715.23 ❌
- **TP 4RR**: 21706.34 ❌
- **TP 4.5RR**: 21697.45 ❌
- **TP 5RR**: 21688.57 ❌
- **PnL**: -17.78 points (-1.0R)
- **MFE**: 15.56 points
- **MAE**: 17.85 points

### Trade #645 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 06:45:00
- **FVG 5m**: 21779.75 - 21784.34
- **Entrée**: 21778.73 @ 2025-05-14 06:47:00
- **Stop Loss**: 21795.23
- **Risk**: 16.50 points
- **TP 1RR**: 21762.23 ✅
- **TP 1.5RR**: 21753.98 ❌
- **TP 2RR**: 21745.72 ❌
- **TP 2.5RR**: 21737.47 ❌
- **TP 3RR**: 21729.22 ❌
- **TP 3.5RR**: 21720.97 ❌
- **TP 4RR**: 21712.72 ❌
- **TP 4.5RR**: 21704.47 ❌
- **TP 5RR**: 21696.22 ❌
- **PnL**: -16.50 points (-1.0R)
- **MFE**: 16.83 points
- **MAE**: 16.58 points

### Trade #646 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 06:45:00
- **FVG 5m**: 21779.75 - 21784.34
- **Entrée**: 21778.73 @ 2025-05-14 06:47:00
- **Stop Loss**: 21795.23
- **Risk**: 16.50 points
- **TP 1RR**: 21762.23 ✅
- **TP 1.5RR**: 21753.98 ❌
- **TP 2RR**: 21745.72 ❌
- **TP 2.5RR**: 21737.47 ❌
- **TP 3RR**: 21729.22 ❌
- **TP 3.5RR**: 21720.97 ❌
- **TP 4RR**: 21712.72 ❌
- **TP 4.5RR**: 21704.47 ❌
- **TP 5RR**: 21696.22 ❌
- **PnL**: -16.50 points (-1.0R)
- **MFE**: 16.83 points
- **MAE**: 16.58 points

### Trade #647 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 07:30:00
- **FVG 5m**: 21779.75 - 21784.34
- **Entrée**: 21778.73 @ 2025-05-14 07:34:00
- **Stop Loss**: 21795.23
- **Risk**: 16.50 points
- **TP 1RR**: 21762.23 ✅
- **TP 1.5RR**: 21753.98 ✅
- **TP 2RR**: 21745.72 ✅
- **TP 2.5RR**: 21737.47 ❌
- **TP 3RR**: 21729.22 ❌
- **TP 3.5RR**: 21720.97 ❌
- **TP 4RR**: 21712.72 ❌
- **TP 4.5RR**: 21704.47 ❌
- **TP 5RR**: 21696.22 ❌
- **PnL**: -16.50 points (-1.0R)
- **MFE**: 38.51 points
- **MAE**: 17.09 points

### Trade #648 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 07:30:00
- **FVG 5m**: 21779.75 - 21784.34
- **Entrée**: 21778.73 @ 2025-05-14 07:34:00
- **Stop Loss**: 21795.23
- **Risk**: 16.50 points
- **TP 1RR**: 21762.23 ✅
- **TP 1.5RR**: 21753.98 ✅
- **TP 2RR**: 21745.72 ✅
- **TP 2.5RR**: 21737.47 ❌
- **TP 3RR**: 21729.22 ❌
- **TP 3.5RR**: 21720.97 ❌
- **TP 4RR**: 21712.72 ❌
- **TP 4.5RR**: 21704.47 ❌
- **TP 5RR**: 21696.22 ❌
- **PnL**: -16.50 points (-1.0R)
- **MFE**: 38.51 points
- **MAE**: 17.09 points

### Trade #649 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 08:30:00
- **FVG 5m**: 21753.23 - 21762.92
- **Entrée**: 21749.91 @ 2025-05-14 08:46:00
- **Stop Loss**: 21773.80
- **Risk**: 23.89 points
- **TP 1RR**: 21726.02 ✅
- **TP 1.5RR**: 21714.08 ✅
- **TP 2RR**: 21702.14 ✅
- **TP 2.5RR**: 21690.19 ❌
- **TP 3RR**: 21678.25 ❌
- **TP 3.5RR**: 21666.30 ❌
- **TP 4RR**: 21654.36 ❌
- **TP 4.5RR**: 21642.42 ❌
- **TP 5RR**: 21630.47 ❌
- **PnL**: -23.89 points (-1.0R)
- **MFE**: 48.45 points
- **MAE**: 28.31 points

### Trade #650 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-14 10:15:00
- **FVG 5m**: 21762.15 - 21780.00
- **Entrée**: 21785.62 @ 2025-05-14 10:20:00
- **Stop Loss**: 21751.27
- **Risk**: 34.34 points
- **TP 1RR**: 21819.96 ✅
- **TP 1.5RR**: 21837.13 ✅
- **TP 2RR**: 21854.30 ❌
- **TP 2.5RR**: 21871.47 ❌
- **TP 3RR**: 21888.65 ❌
- **TP 3.5RR**: 21905.82 ❌
- **TP 4RR**: 21922.99 ❌
- **TP 4.5RR**: 21940.16 ❌
- **TP 5RR**: 21957.33 ❌
- **PnL**: -34.34 points (-1.0R)
- **MFE**: 64.52 points
- **MAE**: 35.45 points

### Trade #651 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 11:30:00
- **FVG 5m**: 21779.75 - 21787.40
- **Entrée**: 21778.73 @ 2025-05-14 12:06:00
- **Stop Loss**: 21798.29
- **Risk**: 19.56 points
- **TP 1RR**: 21759.17 ✅
- **TP 1.5RR**: 21749.38 ✅
- **TP 2RR**: 21739.60 ✅
- **TP 2.5RR**: 21729.82 ✅
- **TP 3RR**: 21720.04 ✅
- **TP 3.5RR**: 21710.25 ✅
- **TP 4RR**: 21700.47 ❌
- **TP 4.5RR**: 21690.69 ❌
- **TP 5RR**: 21680.91 ❌
- **PnL**: -19.56 points (-1.0R)
- **MFE**: 69.37 points
- **MAE**: 20.15 points

### Trade #652 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 22:00:00
- **FVG 5m**: 21831.52 - 21838.15
- **Entrée**: 21823.36 @ 2025-05-14 22:11:00
- **Stop Loss**: 21849.07
- **Risk**: 25.71 points
- **TP 1RR**: 21797.65 ✅
- **TP 1.5RR**: 21784.79 ✅
- **TP 2RR**: 21771.94 ✅
- **TP 2.5RR**: 21759.08 ✅
- **TP 3RR**: 21746.23 ✅
- **TP 3.5RR**: 21733.37 ✅
- **TP 4RR**: 21720.52 ✅
- **TP 4.5RR**: 21707.66 ✅
- **TP 5RR**: 21694.81 ✅
- **PnL**: 128.55 points (5.0R)
- **MFE**: 130.57 points
- **MAE**: 8.67 points

### Trade #653 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 00:45:00
- **FVG 5m**: 21761.64 - 21766.23
- **Entrée**: 21766.49 @ 2025-05-15 01:08:00
- **Stop Loss**: 21750.76
- **Risk**: 15.73 points
- **TP 1RR**: 21782.21 ✅
- **TP 1.5RR**: 21790.08 ✅
- **TP 2RR**: 21797.94 ✅
- **TP 2.5RR**: 21805.80 ❌
- **TP 3RR**: 21813.67 ❌
- **TP 3.5RR**: 21821.53 ❌
- **TP 4RR**: 21829.39 ❌
- **TP 4.5RR**: 21837.26 ❌
- **TP 5RR**: 21845.12 ❌
- **PnL**: -15.73 points (-1.0R)
- **MFE**: 33.66 points
- **MAE**: 19.89 points

### Trade #654 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 01:15:00
- **FVG 5m**: 21761.64 - 21766.23
- **Entrée**: 21778.22 @ 2025-05-15 01:16:00
- **Stop Loss**: 21750.76
- **Risk**: 27.46 points
- **TP 1RR**: 21805.68 ❌
- **TP 1.5RR**: 21819.41 ❌
- **TP 2RR**: 21833.13 ❌
- **TP 2.5RR**: 21846.86 ❌
- **TP 3RR**: 21860.59 ❌
- **TP 3.5RR**: 21874.32 ❌
- **TP 4RR**: 21888.05 ❌
- **TP 4.5RR**: 21901.78 ❌
- **TP 5RR**: 21915.51 ❌
- **PnL**: -27.46 points (-1.0R)
- **MFE**: 21.93 points
- **MAE**: 31.62 points

### Trade #655 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 10:00:00
- **FVG 5m**: 21708.09 - 21714.21
- **Entrée**: 21764.96 @ 2025-05-15 10:01:00
- **Stop Loss**: 21697.23
- **Risk**: 67.72 points
- **TP 1RR**: 21832.68 ✅
- **TP 1.5RR**: 21866.55 ✅
- **TP 2RR**: 21900.41 ✅
- **TP 2.5RR**: 21934.27 ✅
- **TP 3RR**: 21968.13 ❌
- **TP 3.5RR**: 22002.00 ❌
- **TP 4RR**: 22035.86 ❌
- **TP 4.5RR**: 22069.72 ❌
- **TP 5RR**: 22103.58 ❌
- **PnL**: -67.72 points (-1.0R)
- **MFE**: 197.65 points
- **MAE**: 68.09 points

### Trade #656 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-15 15:00:00
- **FVG 5m**: 21842.74 - 21847.08
- **Entrée**: 21839.17 @ 2025-05-15 15:09:00
- **Stop Loss**: 21858.00
- **Risk**: 18.83 points
- **TP 1RR**: 21820.34 ✅
- **TP 1.5RR**: 21810.93 ✅
- **TP 2RR**: 21801.51 ❌
- **TP 2.5RR**: 21792.10 ❌
- **TP 3RR**: 21782.68 ❌
- **TP 3.5RR**: 21773.27 ❌
- **TP 4RR**: 21763.85 ❌
- **TP 4.5RR**: 21754.44 ❌
- **TP 5RR**: 21745.02 ❌
- **PnL**: -18.83 points (-1.0R)
- **MFE**: 29.84 points
- **MAE**: 19.13 points

### Trade #657 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 02:00:00
- **FVG 5m**: 21819.02 - 21828.97
- **Entrée**: 21831.27 @ 2025-05-16 02:17:00
- **Stop Loss**: 21808.11
- **Risk**: 23.15 points
- **TP 1RR**: 21854.42 ✅
- **TP 1.5RR**: 21865.99 ✅
- **TP 2RR**: 21877.57 ✅
- **TP 2.5RR**: 21889.14 ✅
- **TP 3RR**: 21900.72 ✅
- **TP 3.5RR**: 21912.29 ✅
- **TP 4RR**: 21923.87 ✅
- **TP 4.5RR**: 21935.44 ✅
- **TP 5RR**: 21947.02 ❌
- **PnL**: -23.15 points (-1.0R)
- **MFE**: 105.84 points
- **MAE**: 26.52 points

### Trade #658 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 06:15:00
- **FVG 5m**: 21884.06 - 21888.65
- **Entrée**: 21889.92 @ 2025-05-16 06:16:00
- **Stop Loss**: 21873.11
- **Risk**: 16.81 points
- **TP 1RR**: 21906.73 ✅
- **TP 1.5RR**: 21915.13 ✅
- **TP 2RR**: 21923.54 ✅
- **TP 2.5RR**: 21931.94 ✅
- **TP 3RR**: 21940.34 ❌
- **TP 3.5RR**: 21948.75 ❌
- **TP 4RR**: 21957.15 ❌
- **TP 4.5RR**: 21965.56 ❌
- **TP 5RR**: 21973.96 ❌
- **PnL**: -16.81 points (-1.0R)
- **MFE**: 43.35 points
- **MAE**: 18.62 points

### Trade #659 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 07:30:00
- **FVG 5m**: 21889.67 - 21896.81
- **Entrée**: 21888.39 @ 2025-05-16 07:38:00
- **Stop Loss**: 21907.76
- **Risk**: 19.36 points
- **TP 1RR**: 21869.03 ✅
- **TP 1.5RR**: 21859.34 ✅
- **TP 2RR**: 21849.66 ❌
- **TP 2.5RR**: 21839.98 ❌
- **TP 3RR**: 21830.30 ❌
- **TP 3.5RR**: 21820.62 ❌
- **TP 4RR**: 21810.93 ❌
- **TP 4.5RR**: 21801.25 ❌
- **TP 5RR**: 21791.57 ❌
- **PnL**: -19.36 points (-1.0R)
- **MFE**: 34.43 points
- **MAE**: 21.93 points

### Trade #660 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 08:30:00
- **FVG 5m**: 21878.19 - 21885.33
- **Entrée**: 21856.00 @ 2025-05-16 08:31:00
- **Stop Loss**: 21896.27
- **Risk**: 40.27 points
- **TP 1RR**: 21815.73 ✅
- **TP 1.5RR**: 21795.60 ✅
- **TP 2RR**: 21775.46 ✅
- **TP 2.5RR**: 21755.33 ✅
- **TP 3RR**: 21735.19 ❌
- **TP 3.5RR**: 21715.06 ❌
- **TP 4RR**: 21694.92 ❌
- **TP 4.5RR**: 21674.78 ❌
- **TP 5RR**: 21654.65 ❌
- **PnL**: -40.27 points (-1.0R)
- **MFE**: 107.11 points
- **MAE**: 40.29 points

### Trade #661 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 08:30:00
- **FVG 5m**: 21878.19 - 21885.33
- **Entrée**: 21856.00 @ 2025-05-16 08:31:00
- **Stop Loss**: 21896.27
- **Risk**: 40.27 points
- **TP 1RR**: 21815.73 ✅
- **TP 1.5RR**: 21795.60 ✅
- **TP 2RR**: 21775.46 ✅
- **TP 2.5RR**: 21755.33 ✅
- **TP 3RR**: 21735.19 ❌
- **TP 3.5RR**: 21715.06 ❌
- **TP 4RR**: 21694.92 ❌
- **TP 4.5RR**: 21674.78 ❌
- **TP 5RR**: 21654.65 ❌
- **PnL**: -40.27 points (-1.0R)
- **MFE**: 107.11 points
- **MAE**: 40.29 points

### Trade #662 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 09:45:00
- **FVG 5m**: 21822.34 - 21838.66
- **Entrée**: 21846.31 @ 2025-05-16 10:30:00
- **Stop Loss**: 21811.43
- **Risk**: 34.88 points
- **TP 1RR**: 21881.20 ✅
- **TP 1.5RR**: 21898.64 ✅
- **TP 2RR**: 21916.08 ✅
- **TP 2.5RR**: 21933.52 ✅
- **TP 3RR**: 21950.96 ❌
- **TP 3.5RR**: 21968.40 ❌
- **TP 4RR**: 21985.85 ❌
- **TP 4.5RR**: 22003.29 ❌
- **TP 5RR**: 22020.73 ❌
- **PnL**: -34.88 points (-1.0R)
- **MFE**: 98.19 points
- **MAE**: 134.65 points

### Trade #663 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 09:45:00
- **FVG 5m**: 21822.34 - 21838.66
- **Entrée**: 21846.31 @ 2025-05-16 10:30:00
- **Stop Loss**: 21811.43
- **Risk**: 34.88 points
- **TP 1RR**: 21881.20 ✅
- **TP 1.5RR**: 21898.64 ✅
- **TP 2RR**: 21916.08 ✅
- **TP 2.5RR**: 21933.52 ✅
- **TP 3RR**: 21950.96 ❌
- **TP 3.5RR**: 21968.40 ❌
- **TP 4RR**: 21985.85 ❌
- **TP 4.5RR**: 22003.29 ❌
- **TP 5RR**: 22020.73 ❌
- **PnL**: -34.88 points (-1.0R)
- **MFE**: 98.19 points
- **MAE**: 134.65 points

### Trade #664 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-18 19:45:00
- **FVG 5m**: 21721.09 - 21727.47
- **Entrée**: 21728.23 @ 2025-05-18 19:53:00
- **Stop Loss**: 21710.23
- **Risk**: 18.00 points
- **TP 1RR**: 21746.24 ❌
- **TP 1.5RR**: 21755.24 ❌
- **TP 2RR**: 21764.24 ❌
- **TP 2.5RR**: 21773.24 ❌
- **TP 3RR**: 21782.24 ❌
- **TP 3.5RR**: 21791.24 ❌
- **TP 4RR**: 21800.24 ❌
- **TP 4.5RR**: 21809.24 ❌
- **TP 5RR**: 21818.24 ❌
- **PnL**: -18.00 points (-1.0R)
- **MFE**: 7.14 points
- **MAE**: 20.40 points

### Trade #665 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 02:15:00
- **FVG 5m**: 21638.98 - 21643.06
- **Entrée**: 21643.82 @ 2025-05-19 02:30:00
- **Stop Loss**: 21628.16
- **Risk**: 15.66 points
- **TP 1RR**: 21659.49 ❌
- **TP 1.5RR**: 21667.32 ❌
- **TP 2RR**: 21675.15 ❌
- **TP 2.5RR**: 21682.98 ❌
- **TP 3RR**: 21690.82 ❌
- **TP 3.5RR**: 21698.65 ❌
- **TP 4RR**: 21706.48 ❌
- **TP 4.5RR**: 21714.31 ❌
- **TP 5RR**: 21722.15 ❌
- **PnL**: -15.66 points (-1.0R)
- **MFE**: 1.28 points
- **MAE**: 18.87 points

### Trade #666 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 02:15:00
- **FVG 5m**: 21638.98 - 21643.06
- **Entrée**: 21643.82 @ 2025-05-19 02:30:00
- **Stop Loss**: 21628.16
- **Risk**: 15.66 points
- **TP 1RR**: 21659.49 ❌
- **TP 1.5RR**: 21667.32 ❌
- **TP 2RR**: 21675.15 ❌
- **TP 2.5RR**: 21682.98 ❌
- **TP 3RR**: 21690.82 ❌
- **TP 3.5RR**: 21698.65 ❌
- **TP 4RR**: 21706.48 ❌
- **TP 4.5RR**: 21714.31 ❌
- **TP 5RR**: 21722.15 ❌
- **PnL**: -15.66 points (-1.0R)
- **MFE**: 1.28 points
- **MAE**: 18.87 points

### Trade #667 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 08:30:00
- **FVG 5m**: 21613.73 - 21617.55
- **Entrée**: 21667.28 @ 2025-05-19 08:31:00
- **Stop Loss**: 21602.92
- **Risk**: 64.36 points
- **TP 1RR**: 21731.65 ✅
- **TP 1.5RR**: 21763.83 ✅
- **TP 2RR**: 21796.01 ✅
- **TP 2.5RR**: 21828.19 ✅
- **TP 3RR**: 21860.37 ✅
- **TP 3.5RR**: 21892.55 ✅
- **TP 4RR**: 21924.73 ✅
- **TP 4.5RR**: 21956.91 ✅
- **TP 5RR**: 21989.10 ✅
- **PnL**: 321.81 points (5.0R)
- **MFE**: 328.22 points
- **MAE**: 16.58 points

### Trade #668 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 08:30:00
- **FVG 5m**: 21613.73 - 21617.55
- **Entrée**: 21667.28 @ 2025-05-19 08:31:00
- **Stop Loss**: 21602.92
- **Risk**: 64.36 points
- **TP 1RR**: 21731.65 ✅
- **TP 1.5RR**: 21763.83 ✅
- **TP 2RR**: 21796.01 ✅
- **TP 2.5RR**: 21828.19 ✅
- **TP 3RR**: 21860.37 ✅
- **TP 3.5RR**: 21892.55 ✅
- **TP 4RR**: 21924.73 ✅
- **TP 4.5RR**: 21956.91 ✅
- **TP 5RR**: 21989.10 ✅
- **PnL**: 321.81 points (5.0R)
- **MFE**: 328.22 points
- **MAE**: 16.58 points

### Trade #669 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 09:15:00
- **FVG 5m**: 21834.84 - 21842.23
- **Entrée**: 21823.61 @ 2025-05-19 09:27:00
- **Stop Loss**: 21853.15
- **Risk**: 29.54 points
- **TP 1RR**: 21794.08 ❌
- **TP 1.5RR**: 21779.31 ❌
- **TP 2RR**: 21764.54 ❌
- **TP 2.5RR**: 21749.77 ❌
- **TP 3RR**: 21735.00 ❌
- **TP 3.5RR**: 21720.23 ❌
- **TP 4RR**: 21705.46 ❌
- **TP 4.5RR**: 21690.69 ❌
- **TP 5RR**: 21675.92 ❌
- **PnL**: -29.54 points (-1.0R)
- **MFE**: 17.34 points
- **MAE**: 35.19 points

### Trade #670 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 12:15:00
- **FVG 5m**: 21957.50 - 21962.35
- **Entrée**: 21957.25 @ 2025-05-19 12:16:00
- **Stop Loss**: 21973.33
- **Risk**: 16.08 points
- **TP 1RR**: 21941.17 ❌
- **TP 1.5RR**: 21933.13 ❌
- **TP 2RR**: 21925.08 ❌
- **TP 2.5RR**: 21917.04 ❌
- **TP 3RR**: 21909.00 ❌
- **TP 3.5RR**: 21900.96 ❌
- **TP 4RR**: 21892.92 ❌
- **TP 4.5RR**: 21884.88 ❌
- **TP 5RR**: 21876.84 ❌
- **PnL**: -16.08 points (-1.0R)
- **MFE**: 7.91 points
- **MAE**: 19.64 points

### Trade #671 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 12:45:00
- **FVG 5m**: 21957.50 - 21962.35
- **Entrée**: 21950.36 @ 2025-05-19 12:46:00
- **Stop Loss**: 21973.33
- **Risk**: 22.97 points
- **TP 1RR**: 21927.40 ✅
- **TP 1.5RR**: 21915.91 ✅
- **TP 2RR**: 21904.43 ✅
- **TP 2.5RR**: 21892.94 ✅
- **TP 3RR**: 21881.46 ✅
- **TP 3.5RR**: 21869.98 ❌
- **TP 4RR**: 21858.49 ❌
- **TP 4.5RR**: 21847.01 ❌
- **TP 5RR**: 21835.53 ❌
- **PnL**: -22.97 points (-1.0R)
- **MFE**: 75.74 points
- **MAE**: 25.50 points

### Trade #672 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 12:45:00
- **FVG 5m**: 21957.50 - 21962.35
- **Entrée**: 21950.36 @ 2025-05-19 12:46:00
- **Stop Loss**: 21973.33
- **Risk**: 22.97 points
- **TP 1RR**: 21927.40 ✅
- **TP 1.5RR**: 21915.91 ✅
- **TP 2RR**: 21904.43 ✅
- **TP 2.5RR**: 21892.94 ✅
- **TP 3RR**: 21881.46 ✅
- **TP 3.5RR**: 21869.98 ❌
- **TP 4RR**: 21858.49 ❌
- **TP 4.5RR**: 21847.01 ❌
- **TP 5RR**: 21835.53 ❌
- **PnL**: -22.97 points (-1.0R)
- **MFE**: 75.74 points
- **MAE**: 25.50 points

### Trade #673 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 19:00:00
- **FVG 5m**: 21964.90 - 21981.22
- **Entrée**: 21964.64 @ 2025-05-19 19:48:00
- **Stop Loss**: 21992.21
- **Risk**: 27.57 points
- **TP 1RR**: 21937.08 ✅
- **TP 1.5RR**: 21923.29 ✅
- **TP 2RR**: 21909.51 ✅
- **TP 2.5RR**: 21895.73 ✅
- **TP 3RR**: 21881.94 ✅
- **TP 3.5RR**: 21868.16 ✅
- **TP 4RR**: 21854.37 ✅
- **TP 4.5RR**: 21840.59 ✅
- **TP 5RR**: 21826.81 ✅
- **PnL**: 137.84 points (5.0R)
- **MFE**: 140.77 points
- **MAE**: 0.26 points

### Trade #674 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-20 01:30:00
- **FVG 5m**: 21849.88 - 21862.63
- **Entrée**: 21864.16 @ 2025-05-20 02:12:00
- **Stop Loss**: 21838.96
- **Risk**: 25.21 points
- **TP 1RR**: 21889.37 ✅
- **TP 1.5RR**: 21901.97 ✅
- **TP 2RR**: 21914.58 ✅
- **TP 2.5RR**: 21927.18 ❌
- **TP 3RR**: 21939.78 ❌
- **TP 3.5RR**: 21952.39 ❌
- **TP 4RR**: 21964.99 ❌
- **TP 4.5RR**: 21977.59 ❌
- **TP 5RR**: 21990.20 ❌
- **PnL**: -25.21 points (-1.0R)
- **MFE**: 51.52 points
- **MAE**: 27.80 points

### Trade #675 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-20 08:45:00
- **FVG 5m**: 21868.75 - 21871.56
- **Entrée**: 21872.32 @ 2025-05-20 09:40:00
- **Stop Loss**: 21857.82
- **Risk**: 14.50 points
- **TP 1RR**: 21886.83 ❌
- **TP 1.5RR**: 21894.08 ❌
- **TP 2RR**: 21901.33 ❌
- **TP 2.5RR**: 21908.59 ❌
- **TP 3RR**: 21915.84 ❌
- **TP 3.5RR**: 21923.09 ❌
- **TP 4RR**: 21930.34 ❌
- **TP 4.5RR**: 21937.60 ❌
- **TP 5RR**: 21944.85 ❌
- **PnL**: -14.50 points (-1.0R)
- **MFE**: 9.95 points
- **MAE**: 14.54 points

### Trade #676 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 02:45:00
- **FVG 5m**: 21737.93 - 21742.52
- **Entrée**: 21765.98 @ 2025-05-21 02:46:00
- **Stop Loss**: 21727.06
- **Risk**: 38.92 points
- **TP 1RR**: 21804.90 ❌
- **TP 1.5RR**: 21824.36 ❌
- **TP 2RR**: 21843.82 ❌
- **TP 2.5RR**: 21863.28 ❌
- **TP 3RR**: 21882.74 ❌
- **TP 3.5RR**: 21902.20 ❌
- **TP 4RR**: 21921.67 ❌
- **TP 4.5RR**: 21941.13 ❌
- **TP 5RR**: 21960.59 ❌
- **PnL**: -38.92 points (-1.0R)
- **MFE**: 11.99 points
- **MAE**: 46.16 points

### Trade #677 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 04:30:00
- **FVG 5m**: 21739.71 - 21742.01
- **Entrée**: 21720.07 @ 2025-05-21 04:31:00
- **Stop Loss**: 21752.88
- **Risk**: 32.80 points
- **TP 1RR**: 21687.27 ✅
- **TP 1.5RR**: 21670.87 ✅
- **TP 2RR**: 21654.47 ❌
- **TP 2.5RR**: 21638.07 ❌
- **TP 3RR**: 21621.66 ❌
- **TP 3.5RR**: 21605.26 ❌
- **TP 4RR**: 21588.86 ❌
- **TP 4.5RR**: 21572.46 ❌
- **TP 5RR**: 21556.06 ❌
- **PnL**: -32.80 points (-1.0R)
- **MFE**: 63.50 points
- **MAE**: 40.55 points

### Trade #678 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 05:45:00
- **FVG 5m**: 21677.74 - 21684.63
- **Entrée**: 21709.36 @ 2025-05-21 05:46:00
- **Stop Loss**: 21666.90
- **Risk**: 42.46 points
- **TP 1RR**: 21751.82 ✅
- **TP 1.5RR**: 21773.06 ✅
- **TP 2RR**: 21794.29 ✅
- **TP 2.5RR**: 21815.52 ✅
- **TP 3RR**: 21836.75 ✅
- **TP 3.5RR**: 21857.98 ✅
- **TP 4RR**: 21879.21 ✅
- **TP 4.5RR**: 21900.44 ✅
- **TP 5RR**: 21921.67 ✅
- **PnL**: 212.31 points (5.0R)
- **MFE**: 235.13 points
- **MAE**: 19.38 points

### Trade #679 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 05:45:00
- **FVG 5m**: 21677.74 - 21684.63
- **Entrée**: 21709.36 @ 2025-05-21 05:46:00
- **Stop Loss**: 21666.90
- **Risk**: 42.46 points
- **TP 1RR**: 21751.82 ✅
- **TP 1.5RR**: 21773.06 ✅
- **TP 2RR**: 21794.29 ✅
- **TP 2.5RR**: 21815.52 ✅
- **TP 3RR**: 21836.75 ✅
- **TP 3.5RR**: 21857.98 ✅
- **TP 4RR**: 21879.21 ✅
- **TP 4.5RR**: 21900.44 ✅
- **TP 5RR**: 21921.67 ✅
- **PnL**: 212.31 points (5.0R)
- **MFE**: 235.13 points
- **MAE**: 19.38 points

### Trade #680 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 11:45:00
- **FVG 5m**: 21910.32 - 21928.94
- **Entrée**: 21902.93 @ 2025-05-21 12:09:00
- **Stop Loss**: 21939.90
- **Risk**: 36.98 points
- **TP 1RR**: 21865.95 ✅
- **TP 1.5RR**: 21847.46 ✅
- **TP 2RR**: 21828.97 ✅
- **TP 2.5RR**: 21810.48 ✅
- **TP 3RR**: 21792.00 ✅
- **TP 3.5RR**: 21773.51 ✅
- **TP 4RR**: 21755.02 ✅
- **TP 4.5RR**: 21736.53 ✅
- **TP 5RR**: 21718.04 ✅
- **PnL**: 184.89 points (5.0R)
- **MFE**: 193.82 points
- **MAE**: 0.77 points

### Trade #681 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21910.32 - 21928.94
- **Entrée**: 21902.93 @ 2025-05-21 12:09:00
- **Stop Loss**: 21939.90
- **Risk**: 36.98 points
- **TP 1RR**: 21865.95 ✅
- **TP 1.5RR**: 21847.46 ✅
- **TP 2RR**: 21828.97 ✅
- **TP 2.5RR**: 21810.48 ✅
- **TP 3RR**: 21792.00 ✅
- **TP 3.5RR**: 21773.51 ✅
- **TP 4RR**: 21755.02 ✅
- **TP 4.5RR**: 21736.53 ✅
- **TP 5RR**: 21718.04 ✅
- **PnL**: 184.89 points (5.0R)
- **MFE**: 193.82 points
- **MAE**: 0.77 points

### Trade #682 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21910.32 - 21928.94
- **Entrée**: 21902.93 @ 2025-05-21 12:09:00
- **Stop Loss**: 21939.90
- **Risk**: 36.98 points
- **TP 1RR**: 21865.95 ✅
- **TP 1.5RR**: 21847.46 ✅
- **TP 2RR**: 21828.97 ✅
- **TP 2.5RR**: 21810.48 ✅
- **TP 3RR**: 21792.00 ✅
- **TP 3.5RR**: 21773.51 ✅
- **TP 4RR**: 21755.02 ✅
- **TP 4.5RR**: 21736.53 ✅
- **TP 5RR**: 21718.04 ✅
- **PnL**: 184.89 points (5.0R)
- **MFE**: 193.82 points
- **MAE**: 0.77 points

### Trade #683 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21910.32 - 21928.94
- **Entrée**: 21902.93 @ 2025-05-21 12:09:00
- **Stop Loss**: 21939.90
- **Risk**: 36.98 points
- **TP 1RR**: 21865.95 ✅
- **TP 1.5RR**: 21847.46 ✅
- **TP 2RR**: 21828.97 ✅
- **TP 2.5RR**: 21810.48 ✅
- **TP 3RR**: 21792.00 ✅
- **TP 3.5RR**: 21773.51 ✅
- **TP 4RR**: 21755.02 ✅
- **TP 4.5RR**: 21736.53 ✅
- **TP 5RR**: 21718.04 ✅
- **PnL**: 184.89 points (5.0R)
- **MFE**: 193.82 points
- **MAE**: 0.77 points

### Trade #684 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21910.32 - 21928.94
- **Entrée**: 21902.93 @ 2025-05-21 12:09:00
- **Stop Loss**: 21939.90
- **Risk**: 36.98 points
- **TP 1RR**: 21865.95 ✅
- **TP 1.5RR**: 21847.46 ✅
- **TP 2RR**: 21828.97 ✅
- **TP 2.5RR**: 21810.48 ✅
- **TP 3RR**: 21792.00 ✅
- **TP 3.5RR**: 21773.51 ✅
- **TP 4RR**: 21755.02 ✅
- **TP 4.5RR**: 21736.53 ✅
- **TP 5RR**: 21718.04 ✅
- **PnL**: 184.89 points (5.0R)
- **MFE**: 193.82 points
- **MAE**: 0.77 points

### Trade #685 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21910.32 - 21928.94
- **Entrée**: 21850.14 @ 2025-05-21 12:16:00
- **Stop Loss**: 21939.90
- **Risk**: 89.77 points
- **TP 1RR**: 21760.37 ✅
- **TP 1.5RR**: 21715.49 ✅
- **TP 2RR**: 21670.60 ✅
- **TP 2.5RR**: 21625.72 ✅
- **TP 3RR**: 21580.83 ✅
- **TP 3.5RR**: 21535.95 ✅
- **TP 4RR**: 21491.07 ✅
- **TP 4.5RR**: 21446.18 ✅
- **TP 5RR**: 21401.30 ✅
- **PnL**: 448.84 points (5.0R)
- **MFE**: 537.85 points
- **MAE**: 0.00 points

### Trade #686 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21910.32 - 21928.94
- **Entrée**: 21850.14 @ 2025-05-21 12:16:00
- **Stop Loss**: 21939.90
- **Risk**: 89.77 points
- **TP 1RR**: 21760.37 ✅
- **TP 1.5RR**: 21715.49 ✅
- **TP 2RR**: 21670.60 ✅
- **TP 2.5RR**: 21625.72 ✅
- **TP 3RR**: 21580.83 ✅
- **TP 3.5RR**: 21535.95 ✅
- **TP 4RR**: 21491.07 ✅
- **TP 4.5RR**: 21446.18 ✅
- **TP 5RR**: 21401.30 ✅
- **PnL**: 448.84 points (5.0R)
- **MFE**: 537.85 points
- **MAE**: 0.00 points

### Trade #687 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21910.32 - 21928.94
- **Entrée**: 21850.14 @ 2025-05-21 12:16:00
- **Stop Loss**: 21939.90
- **Risk**: 89.77 points
- **TP 1RR**: 21760.37 ✅
- **TP 1.5RR**: 21715.49 ✅
- **TP 2RR**: 21670.60 ✅
- **TP 2.5RR**: 21625.72 ✅
- **TP 3RR**: 21580.83 ✅
- **TP 3.5RR**: 21535.95 ✅
- **TP 4RR**: 21491.07 ✅
- **TP 4.5RR**: 21446.18 ✅
- **TP 5RR**: 21401.30 ✅
- **PnL**: 448.84 points (5.0R)
- **MFE**: 537.85 points
- **MAE**: 0.00 points

### Trade #688 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21910.32 - 21928.94
- **Entrée**: 21850.14 @ 2025-05-21 12:16:00
- **Stop Loss**: 21939.90
- **Risk**: 89.77 points
- **TP 1RR**: 21760.37 ✅
- **TP 1.5RR**: 21715.49 ✅
- **TP 2RR**: 21670.60 ✅
- **TP 2.5RR**: 21625.72 ✅
- **TP 3RR**: 21580.83 ✅
- **TP 3.5RR**: 21535.95 ✅
- **TP 4RR**: 21491.07 ✅
- **TP 4.5RR**: 21446.18 ✅
- **TP 5RR**: 21401.30 ✅
- **PnL**: 448.84 points (5.0R)
- **MFE**: 537.85 points
- **MAE**: 0.00 points

### Trade #689 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 14:00:00
- **FVG 5m**: 21630.81 - 21633.11
- **Entrée**: 21634.13 @ 2025-05-21 14:50:00
- **Stop Loss**: 21620.00
- **Risk**: 14.13 points
- **TP 1RR**: 21648.26 ❌
- **TP 1.5RR**: 21655.33 ❌
- **TP 2RR**: 21662.39 ❌
- **TP 2.5RR**: 21669.46 ❌
- **TP 3RR**: 21676.52 ❌
- **TP 3.5RR**: 21683.59 ❌
- **TP 4RR**: 21690.65 ❌
- **TP 4.5RR**: 21697.72 ❌
- **TP 5RR**: 21704.78 ❌
- **PnL**: -14.13 points (-1.0R)
- **MFE**: 12.50 points
- **MAE**: 35.19 points

### Trade #690 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 14:30:00
- **FVG 5m**: 21573.94 - 21590.52
- **Entrée**: 21596.90 @ 2025-05-21 14:38:00
- **Stop Loss**: 21563.16
- **Risk**: 33.74 points
- **TP 1RR**: 21630.64 ✅
- **TP 1.5RR**: 21647.51 ✅
- **TP 2RR**: 21664.37 ❌
- **TP 2.5RR**: 21681.24 ❌
- **TP 3RR**: 21698.11 ❌
- **TP 3.5RR**: 21714.98 ❌
- **TP 4RR**: 21731.85 ❌
- **TP 4.5RR**: 21748.72 ❌
- **TP 5RR**: 21765.59 ❌
- **PnL**: -33.74 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 35.96 points

### Trade #691 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 14:30:00
- **FVG 5m**: 21573.94 - 21590.52
- **Entrée**: 21596.90 @ 2025-05-21 14:38:00
- **Stop Loss**: 21563.16
- **Risk**: 33.74 points
- **TP 1RR**: 21630.64 ✅
- **TP 1.5RR**: 21647.51 ✅
- **TP 2RR**: 21664.37 ❌
- **TP 2.5RR**: 21681.24 ❌
- **TP 3RR**: 21698.11 ❌
- **TP 3.5RR**: 21714.98 ❌
- **TP 4RR**: 21731.85 ❌
- **TP 4.5RR**: 21748.72 ❌
- **TP 5RR**: 21765.59 ❌
- **PnL**: -33.74 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 35.96 points

### Trade #692 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 01:00:00
- **FVG 5m**: 21593.84 - 21618.32
- **Entrée**: 21592.05 @ 2025-05-22 01:28:00
- **Stop Loss**: 21629.13
- **Risk**: 37.08 points
- **TP 1RR**: 21554.97 ❌
- **TP 1.5RR**: 21536.44 ❌
- **TP 2RR**: 21517.90 ❌
- **TP 2.5RR**: 21499.36 ❌
- **TP 3RR**: 21480.82 ❌
- **TP 3.5RR**: 21462.28 ❌
- **TP 4RR**: 21443.74 ❌
- **TP 4.5RR**: 21425.20 ❌
- **TP 5RR**: 21406.67 ❌
- **PnL**: -37.08 points (-1.0R)
- **MFE**: 0.00 points
- **MAE**: 38.25 points

### Trade #693 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 06:00:00
- **FVG 5m**: 21619.08 - 21622.40
- **Entrée**: 21615.51 @ 2025-05-22 06:16:00
- **Stop Loss**: 21633.21
- **Risk**: 17.70 points
- **TP 1RR**: 21597.82 ❌
- **TP 1.5RR**: 21588.97 ❌
- **TP 2RR**: 21580.12 ❌
- **TP 2.5RR**: 21571.27 ❌
- **TP 3RR**: 21562.42 ❌
- **TP 3.5RR**: 21553.57 ❌
- **TP 4RR**: 21544.73 ❌
- **TP 4.5RR**: 21535.88 ❌
- **TP 5RR**: 21527.03 ❌
- **PnL**: -17.70 points (-1.0R)
- **MFE**: 2.04 points
- **MAE**: 17.85 points

### Trade #694 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:30:00
- **FVG 5m**: 21495.40 - 21515.80
- **Entrée**: 21516.82 @ 2025-05-22 07:35:00
- **Stop Loss**: 21484.65
- **Risk**: 32.17 points
- **TP 1RR**: 21548.99 ✅
- **TP 1.5RR**: 21565.07 ✅
- **TP 2RR**: 21581.16 ✅
- **TP 2.5RR**: 21597.24 ✅
- **TP 3RR**: 21613.33 ✅
- **TP 3.5RR**: 21629.41 ✅
- **TP 4RR**: 21645.50 ✅
- **TP 4.5RR**: 21661.58 ✅
- **TP 5RR**: 21677.67 ✅
- **PnL**: 160.85 points (5.0R)
- **MFE**: 170.61 points
- **MAE**: 3.32 points

### Trade #695 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:45:00
- **FVG 5m**: 21495.40 - 21515.80
- **Entrée**: 21558.39 @ 2025-05-22 07:46:00
- **Stop Loss**: 21484.65
- **Risk**: 73.74 points
- **TP 1RR**: 21632.13 ✅
- **TP 1.5RR**: 21669.00 ✅
- **TP 2RR**: 21705.87 ✅
- **TP 2.5RR**: 21742.74 ✅
- **TP 3RR**: 21779.60 ❌
- **TP 3.5RR**: 21816.47 ❌
- **TP 4RR**: 21853.34 ❌
- **TP 4.5RR**: 21890.21 ❌
- **TP 5RR**: 21927.08 ❌
- **PnL**: -73.74 points (-1.0R)
- **MFE**: 208.10 points
- **MAE**: 77.02 points

### Trade #696 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:45:00
- **FVG 5m**: 21495.40 - 21515.80
- **Entrée**: 21558.39 @ 2025-05-22 07:46:00
- **Stop Loss**: 21484.65
- **Risk**: 73.74 points
- **TP 1RR**: 21632.13 ✅
- **TP 1.5RR**: 21669.00 ✅
- **TP 2RR**: 21705.87 ✅
- **TP 2.5RR**: 21742.74 ✅
- **TP 3RR**: 21779.60 ❌
- **TP 3.5RR**: 21816.47 ❌
- **TP 4RR**: 21853.34 ❌
- **TP 4.5RR**: 21890.21 ❌
- **TP 5RR**: 21927.08 ❌
- **PnL**: -73.74 points (-1.0R)
- **MFE**: 208.10 points
- **MAE**: 77.02 points

### Trade #697 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:45:00
- **FVG 5m**: 21495.40 - 21515.80
- **Entrée**: 21558.39 @ 2025-05-22 07:46:00
- **Stop Loss**: 21484.65
- **Risk**: 73.74 points
- **TP 1RR**: 21632.13 ✅
- **TP 1.5RR**: 21669.00 ✅
- **TP 2RR**: 21705.87 ✅
- **TP 2.5RR**: 21742.74 ✅
- **TP 3RR**: 21779.60 ❌
- **TP 3.5RR**: 21816.47 ❌
- **TP 4RR**: 21853.34 ❌
- **TP 4.5RR**: 21890.21 ❌
- **TP 5RR**: 21927.08 ❌
- **PnL**: -73.74 points (-1.0R)
- **MFE**: 208.10 points
- **MAE**: 77.02 points

### Trade #698 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 09:15:00
- **FVG 5m**: 21689.22 - 21707.07
- **Entrée**: 21688.71 @ 2025-05-22 09:18:00
- **Stop Loss**: 21717.92
- **Risk**: 29.22 points
- **TP 1RR**: 21659.49 ✅
- **TP 1.5RR**: 21644.88 ✅
- **TP 2RR**: 21630.27 ✅
- **TP 2.5RR**: 21615.67 ✅
- **TP 3RR**: 21601.06 ✅
- **TP 3.5RR**: 21586.45 ❌
- **TP 4RR**: 21571.84 ❌
- **TP 4.5RR**: 21557.24 ❌
- **TP 5RR**: 21542.63 ❌
- **PnL**: -29.22 points (-1.0R)
- **MFE**: 96.65 points
- **MAE**: 31.11 points

### Trade #699 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 14:00:00
- **FVG 5m**: 21675.44 - 21680.29
- **Entrée**: 21668.30 @ 2025-05-22 14:45:00
- **Stop Loss**: 21691.13
- **Risk**: 22.83 points
- **TP 1RR**: 21645.48 ❌
- **TP 1.5RR**: 21634.06 ❌
- **TP 2RR**: 21622.65 ❌
- **TP 2.5RR**: 21611.24 ❌
- **TP 3RR**: 21599.82 ❌
- **TP 3.5RR**: 21588.41 ❌
- **TP 4RR**: 21577.00 ❌
- **TP 4.5RR**: 21565.58 ❌
- **TP 5RR**: 21554.17 ❌
- **PnL**: -22.83 points (-1.0R)
- **MFE**: 10.71 points
- **MAE**: 23.97 points

### Trade #700 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 19:45:00
- **FVG 5m**: 21586.44 - 21592.56
- **Entrée**: 21618.06 @ 2025-05-22 19:46:00
- **Stop Loss**: 21575.65
- **Risk**: 42.42 points
- **TP 1RR**: 21660.48 ❌
- **TP 1.5RR**: 21681.69 ❌
- **TP 2RR**: 21702.90 ❌
- **TP 2.5RR**: 21724.10 ❌
- **TP 3RR**: 21745.31 ❌
- **TP 3.5RR**: 21766.52 ❌
- **TP 4RR**: 21787.73 ❌
- **TP 4.5RR**: 21808.94 ❌
- **TP 5RR**: 21830.15 ❌
- **PnL**: -42.42 points (-1.0R)
- **MFE**: 16.83 points
- **MAE**: 45.65 points

### Trade #701 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 23:45:00
- **FVG 5m**: 21587.46 - 21591.80
- **Entrée**: 21592.82 @ 2025-05-23 00:07:00
- **Stop Loss**: 21576.67
- **Risk**: 16.15 points
- **TP 1RR**: 21608.96 ❌
- **TP 1.5RR**: 21617.04 ❌
- **TP 2RR**: 21625.11 ❌
- **TP 2.5RR**: 21633.19 ❌
- **TP 3RR**: 21641.26 ❌
- **TP 3.5RR**: 21649.34 ❌
- **TP 4RR**: 21657.41 ❌
- **TP 4.5RR**: 21665.49 ❌
- **TP 5RR**: 21673.56 ❌
- **PnL**: -16.15 points (-1.0R)
- **MFE**: 14.54 points
- **MAE**: 17.60 points

### Trade #702 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-23 00:00:00
- **FVG 5m**: 21587.46 - 21591.80
- **Entrée**: 21592.82 @ 2025-05-23 00:07:00
- **Stop Loss**: 21576.67
- **Risk**: 16.15 points
- **TP 1RR**: 21608.96 ❌
- **TP 1.5RR**: 21617.04 ❌
- **TP 2RR**: 21625.11 ❌
- **TP 2.5RR**: 21633.19 ❌
- **TP 3RR**: 21641.26 ❌
- **TP 3.5RR**: 21649.34 ❌
- **TP 4RR**: 21657.41 ❌
- **TP 4.5RR**: 21665.49 ❌
- **TP 5RR**: 21673.56 ❌
- **PnL**: -16.15 points (-1.0R)
- **MFE**: 14.54 points
- **MAE**: 17.60 points

### Trade #703 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 03:30:00
- **FVG 5m**: 21626.73 - 21632.85
- **Entrée**: 21625.20 @ 2025-05-23 03:35:00
- **Stop Loss**: 21643.67
- **Risk**: 18.47 points
- **TP 1RR**: 21606.74 ✅
- **TP 1.5RR**: 21597.50 ✅
- **TP 2RR**: 21588.27 ✅
- **TP 2.5RR**: 21579.04 ✅
- **TP 3RR**: 21569.80 ✅
- **TP 3.5RR**: 21560.57 ✅
- **TP 4RR**: 21551.34 ✅
- **TP 4.5RR**: 21542.10 ✅
- **TP 5RR**: 21532.87 ✅
- **PnL**: 92.34 points (5.0R)
- **MFE**: 132.10 points
- **MAE**: 7.14 points

### Trade #704 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 03:30:00
- **FVG 5m**: 21626.73 - 21632.85
- **Entrée**: 21625.20 @ 2025-05-23 03:35:00
- **Stop Loss**: 21643.67
- **Risk**: 18.47 points
- **TP 1RR**: 21606.74 ✅
- **TP 1.5RR**: 21597.50 ✅
- **TP 2RR**: 21588.27 ✅
- **TP 2.5RR**: 21579.04 ✅
- **TP 3RR**: 21569.80 ✅
- **TP 3.5RR**: 21560.57 ✅
- **TP 4RR**: 21551.34 ✅
- **TP 4.5RR**: 21542.10 ✅
- **TP 5RR**: 21532.87 ✅
- **PnL**: 92.34 points (5.0R)
- **MFE**: 132.10 points
- **MAE**: 7.14 points

### Trade #705 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-23 04:30:00
- **FVG 5m**: 21583.63 - 21595.62
- **Entrée**: 21596.13 @ 2025-05-23 04:51:00
- **Stop Loss**: 21572.84
- **Risk**: 23.29 points
- **TP 1RR**: 21619.42 ❌
- **TP 1.5RR**: 21631.06 ❌
- **TP 2RR**: 21642.71 ❌
- **TP 2.5RR**: 21654.35 ❌
- **TP 3RR**: 21666.00 ❌
- **TP 3.5RR**: 21677.64 ❌
- **TP 4RR**: 21689.28 ❌
- **TP 4.5RR**: 21700.93 ❌
- **TP 5RR**: 21712.57 ❌
- **PnL**: -23.29 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 26.27 points

### Trade #706 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 06:30:00
- **FVG 5m**: 21592.05 - 21606.59
- **Entrée**: 21524.98 @ 2025-05-23 06:31:00
- **Stop Loss**: 21617.39
- **Risk**: 92.41 points
- **TP 1RR**: 21432.57 ✅
- **TP 1.5RR**: 21386.36 ✅
- **TP 2RR**: 21340.16 ✅
- **TP 2.5RR**: 21293.95 ✅
- **TP 3RR**: 21247.74 ✅
- **TP 3.5RR**: 21201.54 ✅
- **TP 4RR**: 21155.33 ✅
- **TP 4.5RR**: 21109.13 ❌
- **TP 5RR**: 21062.92 ❌
- **PnL**: -92.41 points (-1.0R)
- **MFE**: 381.26 points
- **MAE**: 104.05 points

### Trade #707 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 06:30:00
- **FVG 5m**: 21592.05 - 21606.59
- **Entrée**: 21524.98 @ 2025-05-23 06:31:00
- **Stop Loss**: 21617.39
- **Risk**: 92.41 points
- **TP 1RR**: 21432.57 ✅
- **TP 1.5RR**: 21386.36 ✅
- **TP 2RR**: 21340.16 ✅
- **TP 2.5RR**: 21293.95 ✅
- **TP 3RR**: 21247.74 ✅
- **TP 3.5RR**: 21201.54 ✅
- **TP 4RR**: 21155.33 ✅
- **TP 4.5RR**: 21109.13 ❌
- **TP 5RR**: 21062.92 ❌
- **PnL**: -92.41 points (-1.0R)
- **MFE**: 381.26 points
- **MAE**: 104.05 points

### Trade #708 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 06:45:00
- **FVG 5m**: 21592.05 - 21606.59
- **Entrée**: 21312.03 @ 2025-05-23 06:46:00
- **Stop Loss**: 21617.39
- **Risk**: 305.36 points
- **TP 1RR**: 21006.67 ❌
- **TP 1.5RR**: 20853.99 ❌
- **TP 2RR**: 20701.31 ❌
- **TP 2.5RR**: 20548.64 ❌
- **TP 3RR**: 20395.96 ❌
- **TP 3.5RR**: 20243.28 ❌
- **TP 4RR**: 20090.60 ❌
- **TP 4.5RR**: 19937.92 ❌
- **TP 5RR**: 19785.24 ❌
- **PnL**: -305.36 points (-1.0R)
- **MFE**: 168.32 points
- **MAE**: 317.00 points

### Trade #709 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 10:30:00
- **FVG 5m**: 21363.29 - 21368.90
- **Entrée**: 21356.15 @ 2025-05-23 10:59:00
- **Stop Loss**: 21379.59
- **Risk**: 23.44 points
- **TP 1RR**: 21332.72 ❌
- **TP 1.5RR**: 21321.00 ❌
- **TP 2RR**: 21309.28 ❌
- **TP 2.5RR**: 21297.56 ❌
- **TP 3RR**: 21285.84 ❌
- **TP 3.5RR**: 21274.13 ❌
- **TP 4RR**: 21262.41 ❌
- **TP 4.5RR**: 21250.69 ❌
- **TP 5RR**: 21238.97 ❌
- **PnL**: -23.44 points (-1.0R)
- **MFE**: 2.55 points
- **MAE**: 29.33 points

### Trade #710 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 14:45:00
- **FVG 5m**: 21440.31 - 21442.86
- **Entrée**: 21436.23 @ 2025-05-23 14:48:00
- **Stop Loss**: 21453.58
- **Risk**: 17.35 points
- **TP 1RR**: 21418.88 ✅
- **TP 1.5RR**: 21410.20 ✅
- **TP 2RR**: 21401.53 ✅
- **TP 2.5RR**: 21392.85 ✅
- **TP 3RR**: 21384.17 ✅
- **TP 3.5RR**: 21375.50 ✅
- **TP 4RR**: 21366.82 ✅
- **TP 4.5RR**: 21358.15 ✅
- **TP 5RR**: 21349.47 ❌
- **PnL**: -17.35 points (-1.0R)
- **MFE**: 84.67 points
- **MAE**: 46.67 points

### Trade #711 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-25 17:00:00
- **FVG 5m**: 21370.94 - 21380.12
- **Entrée**: 21406.65 @ 2025-05-25 17:01:00
- **Stop Loss**: 21360.26
- **Risk**: 46.39 points
- **TP 1RR**: 21453.04 ✅
- **TP 1.5RR**: 21476.23 ✅
- **TP 2RR**: 21499.42 ✅
- **TP 2.5RR**: 21522.62 ✅
- **TP 3RR**: 21545.81 ✅
- **TP 3.5RR**: 21569.01 ✅
- **TP 4RR**: 21592.20 ✅
- **TP 4.5RR**: 21615.40 ✅
- **TP 5RR**: 21638.59 ✅
- **PnL**: 231.95 points (5.0R)
- **MFE**: 249.42 points
- **MAE**: 8.42 points

### Trade #712 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-25 17:15:00
- **FVG 5m**: 21370.94 - 21380.12
- **Entrée**: 21528.04 @ 2025-05-25 17:16:00
- **Stop Loss**: 21360.26
- **Risk**: 167.78 points
- **TP 1RR**: 21695.82 ✅
- **TP 1.5RR**: 21779.71 ✅
- **TP 2RR**: 21863.60 ✅
- **TP 2.5RR**: 21947.49 ✅
- **TP 3RR**: 22031.38 ✅
- **TP 3.5RR**: 22115.27 ✅
- **TP 4RR**: 22199.17 ✅
- **TP 4.5RR**: 22283.06 ✅
- **TP 5RR**: 22366.95 ✅
- **PnL**: 838.91 points (5.0R)
- **MFE**: 840.06 points
- **MAE**: 32.90 points

### Trade #713 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-26 08:45:00
- **FVG 5m**: 21695.85 - 21721.35
- **Entrée**: 21695.59 @ 2025-05-26 09:06:00
- **Stop Loss**: 21732.21
- **Risk**: 36.62 points
- **TP 1RR**: 21658.97 ✅
- **TP 1.5RR**: 21640.66 ✅
- **TP 2RR**: 21622.35 ✅
- **TP 2.5RR**: 21604.05 ✅
- **TP 3RR**: 21585.74 ✅
- **TP 3.5RR**: 21567.43 ✅
- **TP 4RR**: 21549.12 ❌
- **TP 4.5RR**: 21530.81 ❌
- **TP 5RR**: 21512.50 ❌
- **PnL**: -36.62 points (-1.0R)
- **MFE**: 129.04 points
- **MAE**: 48.97 points

### Trade #714 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-26 10:15:00
- **FVG 5m**: 21674.68 - 21691.00
- **Entrée**: 21691.51 @ 2025-05-26 10:34:00
- **Stop Loss**: 21663.84
- **Risk**: 27.67 points
- **TP 1RR**: 21719.18 ✅
- **TP 1.5RR**: 21733.01 ❌
- **TP 2RR**: 21746.85 ❌
- **TP 2.5RR**: 21760.68 ❌
- **TP 3RR**: 21774.52 ❌
- **TP 3.5RR**: 21788.35 ❌
- **TP 4RR**: 21802.19 ❌
- **TP 4.5RR**: 21816.02 ❌
- **TP 5RR**: 21829.86 ❌
- **PnL**: -27.67 points (-1.0R)
- **MFE**: 30.60 points
- **MAE**: 30.35 points

### Trade #715 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-27 00:15:00
- **FVG 5m**: 21587.97 - 21590.78
- **Entrée**: 21594.60 @ 2025-05-27 00:16:00
- **Stop Loss**: 21577.18
- **Risk**: 17.42 points
- **TP 1RR**: 21612.03 ✅
- **TP 1.5RR**: 21620.74 ✅
- **TP 2RR**: 21629.45 ✅
- **TP 2.5RR**: 21638.16 ✅
- **TP 3RR**: 21646.87 ✅
- **TP 3.5RR**: 21655.59 ✅
- **TP 4RR**: 21664.30 ✅
- **TP 4.5RR**: 21673.01 ✅
- **TP 5RR**: 21681.72 ✅
- **PnL**: 87.12 points (5.0R)
- **MFE**: 87.22 points
- **MAE**: 2.04 points

### Trade #716 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-27 01:00:00
- **FVG 5m**: 21587.97 - 21590.78
- **Entrée**: 21632.34 @ 2025-05-27 01:01:00
- **Stop Loss**: 21577.18
- **Risk**: 55.17 points
- **TP 1RR**: 21687.51 ✅
- **TP 1.5RR**: 21715.10 ✅
- **TP 2RR**: 21742.68 ✅
- **TP 2.5RR**: 21770.27 ✅
- **TP 3RR**: 21797.85 ✅
- **TP 3.5RR**: 21825.43 ✅
- **TP 4RR**: 21853.02 ✅
- **TP 4.5RR**: 21880.60 ✅
- **TP 5RR**: 21908.19 ✅
- **PnL**: 275.84 points (5.0R)
- **MFE**: 277.47 points
- **MAE**: 13.52 points

### Trade #717 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 03:15:00
- **FVG 5m**: 21752.97 - 21770.31
- **Entrée**: 21751.70 @ 2025-05-27 03:20:00
- **Stop Loss**: 21781.20
- **Risk**: 29.50 points
- **TP 1RR**: 21722.19 ❌
- **TP 1.5RR**: 21707.44 ❌
- **TP 2RR**: 21692.69 ❌
- **TP 2.5RR**: 21677.94 ❌
- **TP 3RR**: 21663.19 ❌
- **TP 3.5RR**: 21648.44 ❌
- **TP 4RR**: 21633.69 ❌
- **TP 4.5RR**: 21618.94 ❌
- **TP 5RR**: 21604.19 ❌
- **PnL**: -29.50 points (-1.0R)
- **MFE**: 24.99 points
- **MAE**: 29.84 points

### Trade #718 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 05:45:00
- **FVG 5m**: 21753.74 - 21762.41
- **Entrée**: 21747.62 @ 2025-05-27 05:46:00
- **Stop Loss**: 21773.29
- **Risk**: 25.67 points
- **TP 1RR**: 21721.94 ✅
- **TP 1.5RR**: 21709.11 ✅
- **TP 2RR**: 21696.27 ✅
- **TP 2.5RR**: 21683.43 ✅
- **TP 3RR**: 21670.60 ✅
- **TP 3.5RR**: 21657.76 ✅
- **TP 4RR**: 21644.93 ✅
- **TP 4.5RR**: 21632.09 ✅
- **TP 5RR**: 21619.25 ✅
- **PnL**: 128.36 points (5.0R)
- **MFE**: 128.79 points
- **MAE**: 1.02 points

### Trade #719 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 07:15:00
- **FVG 5m**: 21718.03 - 21720.33
- **Entrée**: 21709.36 @ 2025-05-27 07:16:00
- **Stop Loss**: 21731.19
- **Risk**: 21.83 points
- **TP 1RR**: 21687.54 ❌
- **TP 1.5RR**: 21676.62 ❌
- **TP 2RR**: 21665.71 ❌
- **TP 2.5RR**: 21654.80 ❌
- **TP 3RR**: 21643.88 ❌
- **TP 3.5RR**: 21632.97 ❌
- **TP 4RR**: 21622.06 ❌
- **TP 4.5RR**: 21611.14 ❌
- **TP 5RR**: 21600.23 ❌
- **PnL**: -21.83 points (-1.0R)
- **MFE**: 17.34 points
- **MAE**: 23.97 points

### Trade #720 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 08:30:00
- **FVG 5m**: 21728.49 - 21731.04
- **Entrée**: 21667.54 @ 2025-05-27 08:31:00
- **Stop Loss**: 21741.91
- **Risk**: 74.37 points
- **TP 1RR**: 21593.17 ❌
- **TP 1.5RR**: 21555.99 ❌
- **TP 2RR**: 21518.80 ❌
- **TP 2.5RR**: 21481.62 ❌
- **TP 3RR**: 21444.44 ❌
- **TP 3.5RR**: 21407.25 ❌
- **TP 4RR**: 21370.07 ❌
- **TP 4.5RR**: 21332.89 ❌
- **TP 5RR**: 21295.70 ❌
- **PnL**: -74.37 points (-1.0R)
- **MFE**: 48.71 points
- **MAE**: 89.77 points

### Trade #721 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 13:30:00
- **FVG 5m**: 21882.78 - 21885.59
- **Entrée**: 21882.53 @ 2025-05-27 13:41:00
- **Stop Loss**: 21896.53
- **Risk**: 14.00 points
- **TP 1RR**: 21868.52 ✅
- **TP 1.5RR**: 21861.52 ✅
- **TP 2RR**: 21854.52 ✅
- **TP 2.5RR**: 21847.52 ✅
- **TP 3RR**: 21840.52 ❌
- **TP 3.5RR**: 21833.51 ❌
- **TP 4RR**: 21826.51 ❌
- **TP 4.5RR**: 21819.51 ❌
- **TP 5RR**: 21812.51 ❌
- **PnL**: -14.00 points (-1.0R)
- **MFE**: 37.74 points
- **MAE**: 15.05 points

### Trade #722 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-28 08:45:00
- **FVG 5m**: 21958.78 - 21971.27
- **Entrée**: 21956.99 @ 2025-05-28 08:46:00
- **Stop Loss**: 21982.26
- **Risk**: 25.27 points
- **TP 1RR**: 21931.73 ✅
- **TP 1.5RR**: 21919.09 ✅
- **TP 2RR**: 21906.46 ✅
- **TP 2.5RR**: 21893.83 ✅
- **TP 3RR**: 21881.19 ✅
- **TP 3.5RR**: 21868.56 ✅
- **TP 4RR**: 21855.92 ✅
- **TP 4.5RR**: 21843.29 ✅
- **TP 5RR**: 21830.66 ✅
- **PnL**: 126.34 points (5.0R)
- **MFE**: 147.41 points
- **MAE**: 0.00 points

### Trade #723 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-28 08:45:00
- **FVG 5m**: 21958.78 - 21971.27
- **Entrée**: 21956.99 @ 2025-05-28 08:46:00
- **Stop Loss**: 21982.26
- **Risk**: 25.27 points
- **TP 1RR**: 21931.73 ✅
- **TP 1.5RR**: 21919.09 ✅
- **TP 2RR**: 21906.46 ✅
- **TP 2.5RR**: 21893.83 ✅
- **TP 3RR**: 21881.19 ✅
- **TP 3.5RR**: 21868.56 ✅
- **TP 4RR**: 21855.92 ✅
- **TP 4.5RR**: 21843.29 ✅
- **TP 5RR**: 21830.66 ✅
- **PnL**: 126.34 points (5.0R)
- **MFE**: 147.41 points
- **MAE**: 0.00 points

### Trade #724 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-28 08:45:00
- **FVG 5m**: 21958.78 - 21971.27
- **Entrée**: 21956.99 @ 2025-05-28 08:46:00
- **Stop Loss**: 21982.26
- **Risk**: 25.27 points
- **TP 1RR**: 21931.73 ✅
- **TP 1.5RR**: 21919.09 ✅
- **TP 2RR**: 21906.46 ✅
- **TP 2.5RR**: 21893.83 ✅
- **TP 3RR**: 21881.19 ✅
- **TP 3.5RR**: 21868.56 ✅
- **TP 4RR**: 21855.92 ✅
- **TP 4.5RR**: 21843.29 ✅
- **TP 5RR**: 21830.66 ✅
- **PnL**: 126.34 points (5.0R)
- **MFE**: 147.41 points
- **MAE**: 0.00 points

### Trade #725 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-28 08:45:00
- **FVG 5m**: 21958.78 - 21971.27
- **Entrée**: 21956.99 @ 2025-05-28 08:46:00
- **Stop Loss**: 21982.26
- **Risk**: 25.27 points
- **TP 1RR**: 21931.73 ✅
- **TP 1.5RR**: 21919.09 ✅
- **TP 2RR**: 21906.46 ✅
- **TP 2.5RR**: 21893.83 ✅
- **TP 3RR**: 21881.19 ✅
- **TP 3.5RR**: 21868.56 ✅
- **TP 4RR**: 21855.92 ✅
- **TP 4.5RR**: 21843.29 ✅
- **TP 5RR**: 21830.66 ✅
- **PnL**: 126.34 points (5.0R)
- **MFE**: 147.41 points
- **MAE**: 0.00 points

### Trade #726 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-28 09:15:00
- **FVG 5m**: 21958.78 - 21971.27
- **Entrée**: 21891.96 @ 2025-05-28 09:16:00
- **Stop Loss**: 21982.26
- **Risk**: 90.30 points
- **TP 1RR**: 21801.66 ✅
- **TP 1.5RR**: 21756.51 ✅
- **TP 2RR**: 21711.36 ❌
- **TP 2.5RR**: 21666.21 ❌
- **TP 3RR**: 21621.07 ❌
- **TP 3.5RR**: 21575.92 ❌
- **TP 4RR**: 21530.77 ❌
- **TP 4.5RR**: 21485.62 ❌
- **TP 5RR**: 21440.47 ❌
- **PnL**: -90.30 points (-1.0R)
- **MFE**: 142.05 points
- **MAE**: 97.42 points

### Trade #727 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 13:45:00
- **FVG 5m**: 21917.21 - 21919.50
- **Entrée**: 21926.39 @ 2025-05-28 14:06:00
- **Stop Loss**: 21906.25
- **Risk**: 20.14 points
- **TP 1RR**: 21946.53 ✅
- **TP 1.5RR**: 21956.60 ❌
- **TP 2RR**: 21966.67 ❌
- **TP 2.5RR**: 21976.74 ❌
- **TP 3RR**: 21986.81 ❌
- **TP 3.5RR**: 21996.88 ❌
- **TP 4RR**: 22006.95 ❌
- **TP 4.5RR**: 22017.02 ❌
- **TP 5RR**: 22027.09 ❌
- **PnL**: -20.14 points (-1.0R)
- **MFE**: 20.40 points
- **MAE**: 33.66 points

### Trade #728 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 13:45:00
- **FVG 5m**: 21917.21 - 21919.50
- **Entrée**: 21926.39 @ 2025-05-28 14:06:00
- **Stop Loss**: 21906.25
- **Risk**: 20.14 points
- **TP 1RR**: 21946.53 ✅
- **TP 1.5RR**: 21956.60 ❌
- **TP 2RR**: 21966.67 ❌
- **TP 2.5RR**: 21976.74 ❌
- **TP 3RR**: 21986.81 ❌
- **TP 3.5RR**: 21996.88 ❌
- **TP 4RR**: 22006.95 ❌
- **TP 4.5RR**: 22017.02 ❌
- **TP 5RR**: 22027.09 ❌
- **PnL**: -20.14 points (-1.0R)
- **MFE**: 20.40 points
- **MAE**: 33.66 points

### Trade #729 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 15:15:00
- **FVG 5m**: 21819.79 - 21838.41
- **Entrée**: 21882.02 @ 2025-05-28 15:21:00
- **Stop Loss**: 21808.88
- **Risk**: 73.14 points
- **TP 1RR**: 21955.15 ✅
- **TP 1.5RR**: 21991.72 ✅
- **TP 2RR**: 22028.29 ✅
- **TP 2.5RR**: 22064.86 ✅
- **TP 3RR**: 22101.42 ✅
- **TP 3.5RR**: 22137.99 ✅
- **TP 4RR**: 22174.56 ✅
- **TP 4.5RR**: 22211.13 ✅
- **TP 5RR**: 22247.70 ✅
- **PnL**: 365.68 points (5.0R)
- **MFE**: 372.59 points
- **MAE**: 16.07 points

### Trade #730 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-28 20:00:00
- **FVG 5m**: 22212.02 - 22234.21
- **Entrée**: 22209.98 @ 2025-05-28 20:15:00
- **Stop Loss**: 22245.32
- **Risk**: 35.34 points
- **TP 1RR**: 22174.63 ❌
- **TP 1.5RR**: 22156.96 ❌
- **TP 2RR**: 22139.29 ❌
- **TP 2.5RR**: 22121.62 ❌
- **TP 3RR**: 22103.95 ❌
- **TP 3.5RR**: 22086.27 ❌
- **TP 4RR**: 22068.60 ❌
- **TP 4.5RR**: 22050.93 ❌
- **TP 5RR**: 22033.26 ❌
- **PnL**: -35.34 points (-1.0R)
- **MFE**: 19.64 points
- **MAE**: 43.61 points

### Trade #731 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 02:15:00
- **FVG 5m**: 22220.69 - 22226.81
- **Entrée**: 22230.13 @ 2025-05-29 02:29:00
- **Stop Loss**: 22209.58
- **Risk**: 20.55 points
- **TP 1RR**: 22250.67 ✅
- **TP 1.5RR**: 22260.95 ✅
- **TP 2RR**: 22271.22 ✅
- **TP 2.5RR**: 22281.49 ✅
- **TP 3RR**: 22291.77 ✅
- **TP 3.5RR**: 22302.04 ❌
- **TP 4RR**: 22312.31 ❌
- **TP 4.5RR**: 22322.58 ❌
- **TP 5RR**: 22332.86 ❌
- **PnL**: -20.55 points (-1.0R)
- **MFE**: 68.09 points
- **MAE**: 35.70 points

### Trade #732 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 03:00:00
- **FVG 5m**: 22254.61 - 22260.47
- **Entrée**: 22254.10 @ 2025-05-29 03:18:00
- **Stop Loss**: 22271.60
- **Risk**: 17.51 points
- **TP 1RR**: 22236.59 ✅
- **TP 1.5RR**: 22227.84 ✅
- **TP 2RR**: 22219.09 ✅
- **TP 2.5RR**: 22210.33 ✅
- **TP 3RR**: 22201.58 ✅
- **TP 3.5RR**: 22192.83 ✅
- **TP 4RR**: 22184.08 ✅
- **TP 4.5RR**: 22175.32 ✅
- **TP 5RR**: 22166.57 ✅
- **PnL**: 87.53 points (5.0R)
- **MFE**: 88.49 points
- **MAE**: 7.65 points

### Trade #733 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 03:00:00
- **FVG 5m**: 22254.61 - 22260.47
- **Entrée**: 22254.10 @ 2025-05-29 03:18:00
- **Stop Loss**: 22271.60
- **Risk**: 17.51 points
- **TP 1RR**: 22236.59 ✅
- **TP 1.5RR**: 22227.84 ✅
- **TP 2RR**: 22219.09 ✅
- **TP 2.5RR**: 22210.33 ✅
- **TP 3RR**: 22201.58 ✅
- **TP 3.5RR**: 22192.83 ✅
- **TP 4RR**: 22184.08 ✅
- **TP 4.5RR**: 22175.32 ✅
- **TP 5RR**: 22166.57 ✅
- **PnL**: 87.53 points (5.0R)
- **MFE**: 88.49 points
- **MAE**: 7.65 points

### Trade #734 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 03:00:00
- **FVG 5m**: 22254.61 - 22260.47
- **Entrée**: 22254.10 @ 2025-05-29 03:18:00
- **Stop Loss**: 22271.60
- **Risk**: 17.51 points
- **TP 1RR**: 22236.59 ✅
- **TP 1.5RR**: 22227.84 ✅
- **TP 2RR**: 22219.09 ✅
- **TP 2.5RR**: 22210.33 ✅
- **TP 3RR**: 22201.58 ✅
- **TP 3.5RR**: 22192.83 ✅
- **TP 4RR**: 22184.08 ✅
- **TP 4.5RR**: 22175.32 ✅
- **TP 5RR**: 22166.57 ✅
- **PnL**: 87.53 points (5.0R)
- **MFE**: 88.49 points
- **MAE**: 7.65 points

### Trade #735 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 22106.69 - 22113.83
- **Entrée**: 22046.51 @ 2025-05-29 08:31:00
- **Stop Loss**: 22124.89
- **Risk**: 78.38 points
- **TP 1RR**: 21968.12 ✅
- **TP 1.5RR**: 21928.93 ✅
- **TP 2RR**: 21889.74 ✅
- **TP 2.5RR**: 21850.55 ✅
- **TP 3RR**: 21811.36 ✅
- **TP 3.5RR**: 21772.16 ✅
- **TP 4RR**: 21732.97 ✅
- **TP 4.5RR**: 21693.78 ✅
- **TP 5RR**: 21654.59 ✅
- **PnL**: 391.92 points (5.0R)
- **MFE**: 393.51 points
- **MAE**: 6.12 points

### Trade #736 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 22106.69 - 22113.83
- **Entrée**: 22046.51 @ 2025-05-29 08:31:00
- **Stop Loss**: 22124.89
- **Risk**: 78.38 points
- **TP 1RR**: 21968.12 ✅
- **TP 1.5RR**: 21928.93 ✅
- **TP 2RR**: 21889.74 ✅
- **TP 2.5RR**: 21850.55 ✅
- **TP 3RR**: 21811.36 ✅
- **TP 3.5RR**: 21772.16 ✅
- **TP 4RR**: 21732.97 ✅
- **TP 4.5RR**: 21693.78 ✅
- **TP 5RR**: 21654.59 ✅
- **PnL**: 391.92 points (5.0R)
- **MFE**: 393.51 points
- **MAE**: 6.12 points

### Trade #737 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 22106.69 - 22113.83
- **Entrée**: 22046.51 @ 2025-05-29 08:31:00
- **Stop Loss**: 22124.89
- **Risk**: 78.38 points
- **TP 1RR**: 21968.12 ✅
- **TP 1.5RR**: 21928.93 ✅
- **TP 2RR**: 21889.74 ✅
- **TP 2.5RR**: 21850.55 ✅
- **TP 3RR**: 21811.36 ✅
- **TP 3.5RR**: 21772.16 ✅
- **TP 4RR**: 21732.97 ✅
- **TP 4.5RR**: 21693.78 ✅
- **TP 5RR**: 21654.59 ✅
- **PnL**: 391.92 points (5.0R)
- **MFE**: 393.51 points
- **MAE**: 6.12 points

### Trade #738 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 22106.69 - 22113.83
- **Entrée**: 22046.51 @ 2025-05-29 08:31:00
- **Stop Loss**: 22124.89
- **Risk**: 78.38 points
- **TP 1RR**: 21968.12 ✅
- **TP 1.5RR**: 21928.93 ✅
- **TP 2RR**: 21889.74 ✅
- **TP 2.5RR**: 21850.55 ✅
- **TP 3RR**: 21811.36 ✅
- **TP 3.5RR**: 21772.16 ✅
- **TP 4RR**: 21732.97 ✅
- **TP 4.5RR**: 21693.78 ✅
- **TP 5RR**: 21654.59 ✅
- **PnL**: 391.92 points (5.0R)
- **MFE**: 393.51 points
- **MAE**: 6.12 points

### Trade #739 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 22106.69 - 22113.83
- **Entrée**: 22046.51 @ 2025-05-29 08:31:00
- **Stop Loss**: 22124.89
- **Risk**: 78.38 points
- **TP 1RR**: 21968.12 ✅
- **TP 1.5RR**: 21928.93 ✅
- **TP 2RR**: 21889.74 ✅
- **TP 2.5RR**: 21850.55 ✅
- **TP 3RR**: 21811.36 ✅
- **TP 3.5RR**: 21772.16 ✅
- **TP 4RR**: 21732.97 ✅
- **TP 4.5RR**: 21693.78 ✅
- **TP 5RR**: 21654.59 ✅
- **PnL**: 391.92 points (5.0R)
- **MFE**: 393.51 points
- **MAE**: 6.12 points

### Trade #740 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 22106.69 - 22113.83
- **Entrée**: 22046.51 @ 2025-05-29 08:31:00
- **Stop Loss**: 22124.89
- **Risk**: 78.38 points
- **TP 1RR**: 21968.12 ✅
- **TP 1.5RR**: 21928.93 ✅
- **TP 2RR**: 21889.74 ✅
- **TP 2.5RR**: 21850.55 ✅
- **TP 3RR**: 21811.36 ✅
- **TP 3.5RR**: 21772.16 ✅
- **TP 4RR**: 21732.97 ✅
- **TP 4.5RR**: 21693.78 ✅
- **TP 5RR**: 21654.59 ✅
- **PnL**: 391.92 points (5.0R)
- **MFE**: 393.51 points
- **MAE**: 6.12 points

### Trade #741 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 09:00:00
- **FVG 5m**: 22106.69 - 22113.83
- **Entrée**: 21947.05 @ 2025-05-29 09:01:00
- **Stop Loss**: 22124.89
- **Risk**: 177.84 points
- **TP 1RR**: 21769.20 ✅
- **TP 1.5RR**: 21680.28 ✅
- **TP 2RR**: 21591.36 ✅
- **TP 2.5RR**: 21502.44 ✅
- **TP 3RR**: 21413.51 ❌
- **TP 3.5RR**: 21324.59 ❌
- **TP 4RR**: 21235.67 ❌
- **TP 4.5RR**: 21146.75 ❌
- **TP 5RR**: 21057.83 ❌
- **PnL**: -177.84 points (-1.0R)
- **MFE**: 451.91 points
- **MAE**: 180.05 points

### Trade #742 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 20:00:00
- **FVG 5m**: 21760.62 - 21769.04
- **Entrée**: 21775.41 @ 2025-05-29 20:01:00
- **Stop Loss**: 21749.74
- **Risk**: 25.67 points
- **TP 1RR**: 21801.09 ❌
- **TP 1.5RR**: 21813.92 ❌
- **TP 2RR**: 21826.76 ❌
- **TP 2.5RR**: 21839.59 ❌
- **TP 3RR**: 21852.43 ❌
- **TP 3.5RR**: 21865.27 ❌
- **TP 4RR**: 21878.10 ❌
- **TP 4.5RR**: 21890.94 ❌
- **TP 5RR**: 21903.77 ❌
- **PnL**: -25.67 points (-1.0R)
- **MFE**: 0.00 points
- **MAE**: 40.80 points

### Trade #743 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 20:15:00
- **FVG 5m**: 21760.62 - 21769.04
- **Entrée**: 21771.59 @ 2025-05-29 20:57:00
- **Stop Loss**: 21749.74
- **Risk**: 21.85 points
- **TP 1RR**: 21793.44 ✅
- **TP 1.5RR**: 21804.36 ✅
- **TP 2RR**: 21815.28 ✅
- **TP 2.5RR**: 21826.21 ✅
- **TP 3RR**: 21837.13 ✅
- **TP 3.5RR**: 21848.05 ❌
- **TP 4RR**: 21858.97 ❌
- **TP 4.5RR**: 21869.90 ❌
- **TP 5RR**: 21880.82 ❌
- **PnL**: -21.85 points (-1.0R)
- **MFE**: 71.15 points
- **MAE**: 24.74 points

### Trade #744 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 01:15:00
- **FVG 5m**: 21819.28 - 21832.54
- **Entrée**: 21815.20 @ 2025-05-30 01:16:00
- **Stop Loss**: 21843.46
- **Risk**: 28.26 points
- **TP 1RR**: 21786.94 ✅
- **TP 1.5RR**: 21772.81 ✅
- **TP 2RR**: 21758.68 ✅
- **TP 2.5RR**: 21744.55 ❌
- **TP 3RR**: 21730.42 ❌
- **TP 3.5RR**: 21716.30 ❌
- **TP 4RR**: 21702.17 ❌
- **TP 4.5RR**: 21688.04 ❌
- **TP 5RR**: 21673.91 ❌
- **PnL**: -28.26 points (-1.0R)
- **MFE**: 68.35 points
- **MAE**: 35.19 points

### Trade #745 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 07:00:00
- **FVG 5m**: 21831.78 - 21836.88
- **Entrée**: 21838.66 @ 2025-05-30 07:03:00
- **Stop Loss**: 21820.86
- **Risk**: 17.80 points
- **TP 1RR**: 21856.46 ❌
- **TP 1.5RR**: 21865.36 ❌
- **TP 2RR**: 21874.26 ❌
- **TP 2.5RR**: 21883.16 ❌
- **TP 3RR**: 21892.07 ❌
- **TP 3.5RR**: 21900.97 ❌
- **TP 4RR**: 21909.87 ❌
- **TP 4.5RR**: 21918.77 ❌
- **TP 5RR**: 21927.67 ❌
- **PnL**: -17.80 points (-1.0R)
- **MFE**: 11.99 points
- **MAE**: 128.02 points

### Trade #746 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 11:15:00
- **FVG 5m**: 21753.99 - 21765.47
- **Entrée**: 21721.86 @ 2025-05-30 11:16:00
- **Stop Loss**: 21776.35
- **Risk**: 54.49 points
- **TP 1RR**: 21667.37 ✅
- **TP 1.5RR**: 21640.12 ✅
- **TP 2RR**: 21612.87 ✅
- **TP 2.5RR**: 21585.63 ✅
- **TP 3RR**: 21558.38 ✅
- **TP 3.5RR**: 21531.14 ✅
- **TP 4RR**: 21503.89 ✅
- **TP 4.5RR**: 21476.64 ❌
- **TP 5RR**: 21449.40 ❌
- **PnL**: -54.49 points (-1.0R)
- **MFE**: 226.72 points
- **MAE**: 61.21 points

### Trade #747 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 12:00:00
- **FVG 5m**: 21544.87 - 21547.42
- **Entrée**: 21554.82 @ 2025-05-30 12:02:00
- **Stop Loss**: 21534.10
- **Risk**: 20.72 points
- **TP 1RR**: 21575.54 ✅
- **TP 1.5RR**: 21585.89 ✅
- **TP 2RR**: 21596.25 ✅
- **TP 2.5RR**: 21606.61 ✅
- **TP 3RR**: 21616.97 ✅
- **TP 3.5RR**: 21627.33 ✅
- **TP 4RR**: 21637.69 ✅
- **TP 4.5RR**: 21648.05 ✅
- **TP 5RR**: 21658.41 ✅
- **PnL**: 103.59 points (5.0R)
- **MFE**: 107.11 points
- **MAE**: 8.42 points

### Trade #748 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 13:00:00
- **FVG 5m**: 21544.87 - 21547.42
- **Entrée**: 21621.38 @ 2025-05-30 13:01:00
- **Stop Loss**: 21534.10
- **Risk**: 87.28 points
- **TP 1RR**: 21708.66 ✅
- **TP 1.5RR**: 21752.30 ✅
- **TP 2RR**: 21795.94 ✅
- **TP 2.5RR**: 21839.58 ✅
- **TP 3RR**: 21883.22 ✅
- **TP 3.5RR**: 21926.86 ✅
- **TP 4RR**: 21970.50 ✅
- **TP 4.5RR**: 22014.14 ✅
- **TP 5RR**: 22057.78 ✅
- **PnL**: 436.40 points (5.0R)
- **MFE**: 438.65 points
- **MAE**: 32.90 points

### Trade #749 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 13:00:00
- **FVG 5m**: 21544.87 - 21547.42
- **Entrée**: 21621.38 @ 2025-05-30 13:01:00
- **Stop Loss**: 21534.10
- **Risk**: 87.28 points
- **TP 1RR**: 21708.66 ✅
- **TP 1.5RR**: 21752.30 ✅
- **TP 2RR**: 21795.94 ✅
- **TP 2.5RR**: 21839.58 ✅
- **TP 3RR**: 21883.22 ✅
- **TP 3.5RR**: 21926.86 ✅
- **TP 4RR**: 21970.50 ✅
- **TP 4.5RR**: 22014.14 ✅
- **TP 5RR**: 22057.78 ✅
- **PnL**: 436.40 points (5.0R)
- **MFE**: 438.65 points
- **MAE**: 32.90 points

### Trade #750 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 13:00:00
- **FVG 5m**: 21544.87 - 21547.42
- **Entrée**: 21621.38 @ 2025-05-30 13:01:00
- **Stop Loss**: 21534.10
- **Risk**: 87.28 points
- **TP 1RR**: 21708.66 ✅
- **TP 1.5RR**: 21752.30 ✅
- **TP 2RR**: 21795.94 ✅
- **TP 2.5RR**: 21839.58 ✅
- **TP 3RR**: 21883.22 ✅
- **TP 3.5RR**: 21926.86 ✅
- **TP 4RR**: 21970.50 ✅
- **TP 4.5RR**: 22014.14 ✅
- **TP 5RR**: 22057.78 ✅
- **PnL**: 436.40 points (5.0R)
- **MFE**: 438.65 points
- **MAE**: 32.90 points

### Trade #751 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-02 06:00:00
- **FVG 5m**: 21641.02 - 21646.88
- **Entrée**: 21671.62 @ 2025-06-02 06:01:00
- **Stop Loss**: 21630.20
- **Risk**: 41.42 points
- **TP 1RR**: 21713.04 ✅
- **TP 1.5RR**: 21733.75 ✅
- **TP 2RR**: 21754.47 ✅
- **TP 2.5RR**: 21775.18 ✅
- **TP 3RR**: 21795.89 ✅
- **TP 3.5RR**: 21816.60 ✅
- **TP 4RR**: 21837.31 ✅
- **TP 4.5RR**: 21858.03 ✅
- **TP 5RR**: 21878.74 ✅
- **PnL**: 207.12 points (5.0R)
- **MFE**: 210.65 points
- **MAE**: 4.85 points

### Trade #752 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 07:15:00
- **FVG 5m**: 21691.00 - 21695.59
- **Entrée**: 21678.76 @ 2025-06-02 07:20:00
- **Stop Loss**: 21706.44
- **Risk**: 27.68 points
- **TP 1RR**: 21651.08 ❌
- **TP 1.5RR**: 21637.24 ❌
- **TP 2RR**: 21623.40 ❌
- **TP 2.5RR**: 21609.56 ❌
- **TP 3RR**: 21595.72 ❌
- **TP 3.5RR**: 21581.88 ❌
- **TP 4RR**: 21568.04 ❌
- **TP 4.5RR**: 21554.20 ❌
- **TP 5RR**: 21540.36 ❌
- **PnL**: -27.68 points (-1.0R)
- **MFE**: 11.99 points
- **MAE**: 29.07 points

### Trade #753 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 08:30:00
- **FVG 5m**: 21692.28 - 21702.73
- **Entrée**: 21669.58 @ 2025-06-02 09:00:00
- **Stop Loss**: 21713.58
- **Risk**: 44.00 points
- **TP 1RR**: 21625.57 ❌
- **TP 1.5RR**: 21603.57 ❌
- **TP 2RR**: 21581.57 ❌
- **TP 2.5RR**: 21559.57 ❌
- **TP 3RR**: 21537.56 ❌
- **TP 3.5RR**: 21515.56 ❌
- **TP 4RR**: 21493.56 ❌
- **TP 4.5RR**: 21471.56 ❌
- **TP 5RR**: 21449.55 ❌
- **PnL**: -44.00 points (-1.0R)
- **MFE**: 7.91 points
- **MAE**: 51.01 points

### Trade #754 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 08:30:00
- **FVG 5m**: 21692.28 - 21702.73
- **Entrée**: 21669.58 @ 2025-06-02 09:00:00
- **Stop Loss**: 21713.58
- **Risk**: 44.00 points
- **TP 1RR**: 21625.57 ❌
- **TP 1.5RR**: 21603.57 ❌
- **TP 2RR**: 21581.57 ❌
- **TP 2.5RR**: 21559.57 ❌
- **TP 3RR**: 21537.56 ❌
- **TP 3.5RR**: 21515.56 ❌
- **TP 4RR**: 21493.56 ❌
- **TP 4.5RR**: 21471.56 ❌
- **TP 5RR**: 21449.55 ❌
- **PnL**: -44.00 points (-1.0R)
- **MFE**: 7.91 points
- **MAE**: 51.01 points

### Trade #755 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 08:45:00
- **FVG 5m**: 21720.07 - 21827.69
- **Entrée**: 21669.58 @ 2025-06-02 09:00:00
- **Stop Loss**: 21838.61
- **Risk**: 169.03 points
- **TP 1RR**: 21500.55 ❌
- **TP 1.5RR**: 21416.03 ❌
- **TP 2RR**: 21331.52 ❌
- **TP 2.5RR**: 21247.00 ❌
- **TP 3RR**: 21162.49 ❌
- **TP 3.5RR**: 21077.97 ❌
- **TP 4RR**: 20993.46 ❌
- **TP 4.5RR**: 20908.94 ❌
- **TP 5RR**: 20824.43 ❌
- **PnL**: -169.03 points (-1.0R)
- **MFE**: 7.91 points
- **MAE**: 175.71 points

### Trade #756 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 12:00:00
- **FVG 5m**: 21860.59 - 21873.60
- **Entrée**: 21857.79 @ 2025-06-02 12:50:00
- **Stop Loss**: 21884.54
- **Risk**: 26.75 points
- **TP 1RR**: 21831.04 ❌
- **TP 1.5RR**: 21817.67 ❌
- **TP 2RR**: 21804.29 ❌
- **TP 2.5RR**: 21790.92 ❌
- **TP 3RR**: 21777.54 ❌
- **TP 3.5RR**: 21764.17 ❌
- **TP 4RR**: 21750.79 ❌
- **TP 4.5RR**: 21737.42 ❌
- **TP 5RR**: 21724.05 ❌
- **PnL**: -26.75 points (-1.0R)
- **MFE**: 1.79 points
- **MAE**: 31.88 points

### Trade #757 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-02 21:30:00
- **FVG 5m**: 21895.79 - 21899.61
- **Entrée**: 21901.14 @ 2025-06-02 21:35:00
- **Stop Loss**: 21884.84
- **Risk**: 16.30 points
- **TP 1RR**: 21917.45 ❌
- **TP 1.5RR**: 21925.60 ❌
- **TP 2RR**: 21933.75 ❌
- **TP 2.5RR**: 21941.90 ❌
- **TP 3RR**: 21950.05 ❌
- **TP 3.5RR**: 21958.20 ❌
- **TP 4RR**: 21966.36 ❌
- **TP 4.5RR**: 21974.51 ❌
- **TP 5RR**: 21982.66 ❌
- **PnL**: -16.30 points (-1.0R)
- **MFE**: 5.61 points
- **MAE**: 17.34 points

### Trade #758 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-03 02:45:00
- **FVG 5m**: 21851.16 - 21871.56
- **Entrée**: 21872.58 @ 2025-06-03 03:03:00
- **Stop Loss**: 21840.23
- **Risk**: 32.35 points
- **TP 1RR**: 21904.93 ❌
- **TP 1.5RR**: 21921.10 ❌
- **TP 2RR**: 21937.28 ❌
- **TP 2.5RR**: 21953.45 ❌
- **TP 3RR**: 21969.62 ❌
- **TP 3.5RR**: 21985.80 ❌
- **TP 4RR**: 22001.97 ❌
- **TP 4.5RR**: 22018.14 ❌
- **TP 5RR**: 22034.32 ❌
- **PnL**: -32.35 points (-1.0R)
- **MFE**: 3.06 points
- **MAE**: 34.94 points

### Trade #759 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-03 08:30:00
- **FVG 5m**: 21969.74 - 21973.06
- **Entrée**: 21965.15 @ 2025-06-03 08:34:00
- **Stop Loss**: 21984.05
- **Risk**: 18.89 points
- **TP 1RR**: 21946.26 ✅
- **TP 1.5RR**: 21936.82 ❌
- **TP 2RR**: 21927.37 ❌
- **TP 2.5RR**: 21917.92 ❌
- **TP 3RR**: 21908.48 ❌
- **TP 3.5RR**: 21899.03 ❌
- **TP 4RR**: 21889.58 ❌
- **TP 4.5RR**: 21880.14 ❌
- **TP 5RR**: 21870.69 ❌
- **PnL**: -18.89 points (-1.0R)
- **MFE**: 22.95 points
- **MAE**: 27.54 points

### Trade #760 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-03 09:15:00
- **FVG 5m**: 21953.42 - 21960.56
- **Entrée**: 22050.84 @ 2025-06-03 09:16:00
- **Stop Loss**: 21942.45
- **Risk**: 108.40 points
- **TP 1RR**: 22159.24 ✅
- **TP 1.5RR**: 22213.44 ✅
- **TP 2RR**: 22267.64 ✅
- **TP 2.5RR**: 22321.83 ✅
- **TP 3RR**: 22376.03 ❌
- **TP 3.5RR**: 22430.23 ❌
- **TP 4RR**: 22484.43 ❌
- **TP 4.5RR**: 22538.63 ❌
- **TP 5RR**: 22592.83 ❌
- **PnL**: -108.40 points (-1.0R)
- **MFE**: 325.16 points
- **MAE**: 115.02 points

### Trade #761 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-03 13:00:00
- **FVG 5m**: 22145.97 - 22162.29
- **Entrée**: 22137.30 @ 2025-06-03 13:01:00
- **Stop Loss**: 22173.37
- **Risk**: 36.07 points
- **TP 1RR**: 22101.22 ✅
- **TP 1.5RR**: 22083.19 ✅
- **TP 2RR**: 22065.15 ❌
- **TP 2.5RR**: 22047.11 ❌
- **TP 3RR**: 22029.08 ❌
- **TP 3.5RR**: 22011.04 ❌
- **TP 4RR**: 21993.00 ❌
- **TP 4.5RR**: 21974.96 ❌
- **TP 5RR**: 21956.93 ❌
- **PnL**: -36.07 points (-1.0R)
- **MFE**: 66.56 points
- **MAE**: 38.00 points

### Trade #762 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 01:15:00
- **FVG 5m**: 22131.18 - 22143.16
- **Entrée**: 22129.65 @ 2025-06-04 01:17:00
- **Stop Loss**: 22154.23
- **Risk**: 24.59 points
- **TP 1RR**: 22105.06 ❌
- **TP 1.5RR**: 22092.76 ❌
- **TP 2RR**: 22080.47 ❌
- **TP 2.5RR**: 22068.18 ❌
- **TP 3RR**: 22055.88 ❌
- **TP 3.5RR**: 22043.59 ❌
- **TP 4RR**: 22031.29 ❌
- **TP 4.5RR**: 22019.00 ❌
- **TP 5RR**: 22006.71 ❌
- **PnL**: -24.59 points (-1.0R)
- **MFE**: 19.38 points
- **MAE**: 25.50 points

### Trade #763 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 03:45:00
- **FVG 5m**: 22158.97 - 22161.78
- **Entrée**: 22154.38 @ 2025-06-04 03:56:00
- **Stop Loss**: 22172.86
- **Risk**: 18.48 points
- **TP 1RR**: 22135.91 ❌
- **TP 1.5RR**: 22126.67 ❌
- **TP 2RR**: 22117.43 ❌
- **TP 2.5RR**: 22108.19 ❌
- **TP 3RR**: 22098.95 ❌
- **TP 3.5RR**: 22089.72 ❌
- **TP 4RR**: 22080.48 ❌
- **TP 4.5RR**: 22071.24 ❌
- **TP 5RR**: 22062.00 ❌
- **PnL**: -18.48 points (-1.0R)
- **MFE**: 4.08 points
- **MAE**: 19.38 points

### Trade #764 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 05:00:00
- **FVG 5m**: 22163.05 - 22165.35
- **Entrée**: 22171.73 @ 2025-06-04 05:01:00
- **Stop Loss**: 22151.97
- **Risk**: 19.75 points
- **TP 1RR**: 22191.48 ✅
- **TP 1.5RR**: 22201.35 ✅
- **TP 2RR**: 22211.23 ❌
- **TP 2.5RR**: 22221.11 ❌
- **TP 3RR**: 22230.98 ❌
- **TP 3.5RR**: 22240.86 ❌
- **TP 4RR**: 22250.73 ❌
- **TP 4.5RR**: 22260.61 ❌
- **TP 5RR**: 22270.49 ❌
- **PnL**: -19.75 points (-1.0R)
- **MFE**: 32.90 points
- **MAE**: 24.23 points

### Trade #765 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22181.42 - 22185.75
- **Entrée**: 22148.77 @ 2025-06-04 07:16:00
- **Stop Loss**: 22196.84
- **Risk**: 48.07 points
- **TP 1RR**: 22100.70 ✅
- **TP 1.5RR**: 22076.67 ❌
- **TP 2RR**: 22052.63 ❌
- **TP 2.5RR**: 22028.59 ❌
- **TP 3RR**: 22004.56 ❌
- **TP 3.5RR**: 21980.52 ❌
- **TP 4RR**: 21956.49 ❌
- **TP 4.5RR**: 21932.45 ❌
- **TP 5RR**: 21908.41 ❌
- **PnL**: -48.07 points (-1.0R)
- **MFE**: 58.15 points
- **MAE**: 66.05 points

### Trade #766 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22181.42 - 22185.75
- **Entrée**: 22148.77 @ 2025-06-04 07:16:00
- **Stop Loss**: 22196.84
- **Risk**: 48.07 points
- **TP 1RR**: 22100.70 ✅
- **TP 1.5RR**: 22076.67 ❌
- **TP 2RR**: 22052.63 ❌
- **TP 2.5RR**: 22028.59 ❌
- **TP 3RR**: 22004.56 ❌
- **TP 3.5RR**: 21980.52 ❌
- **TP 4RR**: 21956.49 ❌
- **TP 4.5RR**: 21932.45 ❌
- **TP 5RR**: 21908.41 ❌
- **PnL**: -48.07 points (-1.0R)
- **MFE**: 58.15 points
- **MAE**: 66.05 points

### Trade #767 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22181.42 - 22185.75
- **Entrée**: 22148.77 @ 2025-06-04 07:16:00
- **Stop Loss**: 22196.84
- **Risk**: 48.07 points
- **TP 1RR**: 22100.70 ✅
- **TP 1.5RR**: 22076.67 ❌
- **TP 2RR**: 22052.63 ❌
- **TP 2.5RR**: 22028.59 ❌
- **TP 3RR**: 22004.56 ❌
- **TP 3.5RR**: 21980.52 ❌
- **TP 4RR**: 21956.49 ❌
- **TP 4.5RR**: 21932.45 ❌
- **TP 5RR**: 21908.41 ❌
- **PnL**: -48.07 points (-1.0R)
- **MFE**: 58.15 points
- **MAE**: 66.05 points

### Trade #768 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 08:15:00
- **FVG 5m**: 22126.08 - 22139.08
- **Entrée**: 22142.65 @ 2025-06-04 08:16:00
- **Stop Loss**: 22115.01
- **Risk**: 27.64 points
- **TP 1RR**: 22170.29 ✅
- **TP 1.5RR**: 22184.11 ✅
- **TP 2RR**: 22197.93 ✅
- **TP 2.5RR**: 22211.75 ✅
- **TP 3RR**: 22225.57 ✅
- **TP 3.5RR**: 22239.39 ❌
- **TP 4RR**: 22253.21 ❌
- **TP 4.5RR**: 22267.03 ❌
- **TP 5RR**: 22280.85 ❌
- **PnL**: -27.64 points (-1.0R)
- **MFE**: 88.75 points
- **MAE**: 36.47 points

### Trade #769 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 08:30:00
- **FVG 5m**: 22181.42 - 22185.75
- **Entrée**: 22180.91 @ 2025-06-04 08:31:00
- **Stop Loss**: 22196.84
- **Risk**: 15.94 points
- **TP 1RR**: 22164.97 ❌
- **TP 1.5RR**: 22157.00 ❌
- **TP 2RR**: 22149.03 ❌
- **TP 2.5RR**: 22141.06 ❌
- **TP 3RR**: 22133.09 ❌
- **TP 3.5RR**: 22125.12 ❌
- **TP 4RR**: 22117.15 ❌
- **TP 4.5RR**: 22109.18 ❌
- **TP 5RR**: 22101.21 ❌
- **PnL**: -15.94 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 33.92 points

### Trade #770 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 08:30:00
- **FVG 5m**: 22181.42 - 22185.75
- **Entrée**: 22180.91 @ 2025-06-04 08:31:00
- **Stop Loss**: 22196.84
- **Risk**: 15.94 points
- **TP 1RR**: 22164.97 ❌
- **TP 1.5RR**: 22157.00 ❌
- **TP 2RR**: 22149.03 ❌
- **TP 2.5RR**: 22141.06 ❌
- **TP 3RR**: 22133.09 ❌
- **TP 3.5RR**: 22125.12 ❌
- **TP 4RR**: 22117.15 ❌
- **TP 4.5RR**: 22109.18 ❌
- **TP 5RR**: 22101.21 ❌
- **PnL**: -15.94 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 33.92 points

### Trade #771 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 08:30:00
- **FVG 5m**: 22181.42 - 22185.75
- **Entrée**: 22180.91 @ 2025-06-04 08:31:00
- **Stop Loss**: 22196.84
- **Risk**: 15.94 points
- **TP 1RR**: 22164.97 ❌
- **TP 1.5RR**: 22157.00 ❌
- **TP 2RR**: 22149.03 ❌
- **TP 2.5RR**: 22141.06 ❌
- **TP 3RR**: 22133.09 ❌
- **TP 3.5RR**: 22125.12 ❌
- **TP 4RR**: 22117.15 ❌
- **TP 4.5RR**: 22109.18 ❌
- **TP 5RR**: 22101.21 ❌
- **PnL**: -15.94 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 33.92 points

### Trade #772 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 09:00:00
- **FVG 5m**: 22126.08 - 22139.08
- **Entrée**: 22176.57 @ 2025-06-04 09:01:00
- **Stop Loss**: 22115.01
- **Risk**: 61.56 points
- **TP 1RR**: 22238.13 ❌
- **TP 1.5RR**: 22268.91 ❌
- **TP 2RR**: 22299.69 ❌
- **TP 2.5RR**: 22330.47 ❌
- **TP 3RR**: 22361.25 ❌
- **TP 3.5RR**: 22392.02 ❌
- **TP 4RR**: 22422.80 ❌
- **TP 4.5RR**: 22453.58 ❌
- **TP 5RR**: 22484.36 ❌
- **PnL**: -61.56 points (-1.0R)
- **MFE**: 1.02 points
- **MAE**: 70.39 points

### Trade #773 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 09:00:00
- **FVG 5m**: 22126.08 - 22139.08
- **Entrée**: 22176.57 @ 2025-06-04 09:01:00
- **Stop Loss**: 22115.01
- **Risk**: 61.56 points
- **TP 1RR**: 22238.13 ❌
- **TP 1.5RR**: 22268.91 ❌
- **TP 2RR**: 22299.69 ❌
- **TP 2.5RR**: 22330.47 ❌
- **TP 3RR**: 22361.25 ❌
- **TP 3.5RR**: 22392.02 ❌
- **TP 4RR**: 22422.80 ❌
- **TP 4.5RR**: 22453.58 ❌
- **TP 5RR**: 22484.36 ❌
- **PnL**: -61.56 points (-1.0R)
- **MFE**: 1.02 points
- **MAE**: 70.39 points

### Trade #774 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 10:30:00
- **FVG 5m**: 22171.98 - 22192.89
- **Entrée**: 22169.17 @ 2025-06-04 11:07:00
- **Stop Loss**: 22203.99
- **Risk**: 34.81 points
- **TP 1RR**: 22134.36 ❌
- **TP 1.5RR**: 22116.95 ❌
- **TP 2RR**: 22099.55 ❌
- **TP 2.5RR**: 22082.14 ❌
- **TP 3RR**: 22064.73 ❌
- **TP 3.5RR**: 22047.33 ❌
- **TP 4RR**: 22029.92 ❌
- **TP 4.5RR**: 22012.51 ❌
- **TP 5RR**: 21995.11 ❌
- **PnL**: -34.81 points (-1.0R)
- **MFE**: 26.78 points
- **MAE**: 34.94 points

### Trade #775 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 03:45:00
- **FVG 5m**: 22266.59 - 22268.89
- **Entrée**: 22253.08 @ 2025-06-05 03:46:00
- **Stop Loss**: 22280.02
- **Risk**: 26.95 points
- **TP 1RR**: 22226.13 ✅
- **TP 1.5RR**: 22212.66 ✅
- **TP 2RR**: 22199.19 ✅
- **TP 2.5RR**: 22185.71 ✅
- **TP 3RR**: 22172.24 ✅
- **TP 3.5RR**: 22158.77 ✅
- **TP 4RR**: 22145.29 ❌
- **TP 4.5RR**: 22131.82 ❌
- **TP 5RR**: 22118.35 ❌
- **PnL**: -26.95 points (-1.0R)
- **MFE**: 104.05 points
- **MAE**: 85.18 points

### Trade #776 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 03:45:00
- **FVG 5m**: 22266.59 - 22268.89
- **Entrée**: 22253.08 @ 2025-06-05 03:46:00
- **Stop Loss**: 22280.02
- **Risk**: 26.95 points
- **TP 1RR**: 22226.13 ✅
- **TP 1.5RR**: 22212.66 ✅
- **TP 2RR**: 22199.19 ✅
- **TP 2.5RR**: 22185.71 ✅
- **TP 3RR**: 22172.24 ✅
- **TP 3.5RR**: 22158.77 ✅
- **TP 4RR**: 22145.29 ❌
- **TP 4.5RR**: 22131.82 ❌
- **TP 5RR**: 22118.35 ❌
- **PnL**: -26.95 points (-1.0R)
- **MFE**: 104.05 points
- **MAE**: 85.18 points

### Trade #777 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 04:00:00
- **FVG 5m**: 22266.59 - 22268.89
- **Entrée**: 22220.44 @ 2025-06-05 04:01:00
- **Stop Loss**: 22280.02
- **Risk**: 59.59 points
- **TP 1RR**: 22160.85 ✅
- **TP 1.5RR**: 22131.05 ❌
- **TP 2RR**: 22101.26 ❌
- **TP 2.5RR**: 22071.46 ❌
- **TP 3RR**: 22041.67 ❌
- **TP 3.5RR**: 22011.87 ❌
- **TP 4RR**: 21982.08 ❌
- **TP 4.5RR**: 21952.28 ❌
- **TP 5RR**: 21922.49 ❌
- **PnL**: -59.59 points (-1.0R)
- **MFE**: 71.41 points
- **MAE**: 117.82 points

### Trade #778 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 05:30:00
- **FVG 5m**: 22228.34 - 22231.40
- **Entrée**: 22225.54 @ 2025-06-05 05:35:00
- **Stop Loss**: 22242.52
- **Risk**: 16.98 points
- **TP 1RR**: 22208.55 ✅
- **TP 1.5RR**: 22200.06 ✅
- **TP 2RR**: 22191.57 ✅
- **TP 2.5RR**: 22183.08 ✅
- **TP 3RR**: 22174.59 ✅
- **TP 3.5RR**: 22166.10 ✅
- **TP 4RR**: 22157.61 ✅
- **TP 4.5RR**: 22149.12 ✅
- **TP 5RR**: 22140.63 ❌
- **PnL**: -16.98 points (-1.0R)
- **MFE**: 76.51 points
- **MAE**: 112.72 points

### Trade #779 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 05:30:00
- **FVG 5m**: 22228.34 - 22231.40
- **Entrée**: 22225.54 @ 2025-06-05 05:35:00
- **Stop Loss**: 22242.52
- **Risk**: 16.98 points
- **TP 1RR**: 22208.55 ✅
- **TP 1.5RR**: 22200.06 ✅
- **TP 2RR**: 22191.57 ✅
- **TP 2.5RR**: 22183.08 ✅
- **TP 3RR**: 22174.59 ✅
- **TP 3.5RR**: 22166.10 ✅
- **TP 4RR**: 22157.61 ✅
- **TP 4.5RR**: 22149.12 ✅
- **TP 5RR**: 22140.63 ❌
- **PnL**: -16.98 points (-1.0R)
- **MFE**: 76.51 points
- **MAE**: 112.72 points

### Trade #780 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 07:30:00
- **FVG 5m**: 22205.13 - 22223.50
- **Entrée**: 22285.21 @ 2025-06-05 07:49:00
- **Stop Loss**: 22194.03
- **Risk**: 91.18 points
- **TP 1RR**: 22376.39 ❌
- **TP 1.5RR**: 22421.98 ❌
- **TP 2RR**: 22467.57 ❌
- **TP 2.5RR**: 22513.16 ❌
- **TP 3RR**: 22558.75 ❌
- **TP 3.5RR**: 22604.34 ❌
- **TP 4RR**: 22649.94 ❌
- **TP 4.5RR**: 22695.53 ❌
- **TP 5RR**: 22741.12 ❌
- **PnL**: -91.18 points (-1.0R)
- **MFE**: 21.68 points
- **MAE**: 108.13 points

### Trade #781 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 07:30:00
- **FVG 5m**: 22205.13 - 22223.50
- **Entrée**: 22285.21 @ 2025-06-05 07:49:00
- **Stop Loss**: 22194.03
- **Risk**: 91.18 points
- **TP 1RR**: 22376.39 ❌
- **TP 1.5RR**: 22421.98 ❌
- **TP 2RR**: 22467.57 ❌
- **TP 2.5RR**: 22513.16 ❌
- **TP 3RR**: 22558.75 ❌
- **TP 3.5RR**: 22604.34 ❌
- **TP 4RR**: 22649.94 ❌
- **TP 4.5RR**: 22695.53 ❌
- **TP 5RR**: 22741.12 ❌
- **PnL**: -91.18 points (-1.0R)
- **MFE**: 21.68 points
- **MAE**: 108.13 points

### Trade #782 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 07:30:00
- **FVG 5m**: 22205.13 - 22223.50
- **Entrée**: 22285.21 @ 2025-06-05 07:49:00
- **Stop Loss**: 22194.03
- **Risk**: 91.18 points
- **TP 1RR**: 22376.39 ❌
- **TP 1.5RR**: 22421.98 ❌
- **TP 2RR**: 22467.57 ❌
- **TP 2.5RR**: 22513.16 ❌
- **TP 3RR**: 22558.75 ❌
- **TP 3.5RR**: 22604.34 ❌
- **TP 4RR**: 22649.94 ❌
- **TP 4.5RR**: 22695.53 ❌
- **TP 5RR**: 22741.12 ❌
- **PnL**: -91.18 points (-1.0R)
- **MFE**: 21.68 points
- **MAE**: 108.13 points

### Trade #783 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 07:45:00
- **FVG 5m**: 22194.68 - 22208.19
- **Entrée**: 22191.87 @ 2025-06-05 07:48:00
- **Stop Loss**: 22219.30
- **Risk**: 27.43 points
- **TP 1RR**: 22164.45 ❌
- **TP 1.5RR**: 22150.73 ❌
- **TP 2RR**: 22137.02 ❌
- **TP 2.5RR**: 22123.31 ❌
- **TP 3RR**: 22109.59 ❌
- **TP 3.5RR**: 22095.88 ❌
- **TP 4RR**: 22082.17 ❌
- **TP 4.5RR**: 22068.46 ❌
- **TP 5RR**: 22054.74 ❌
- **PnL**: -27.43 points (-1.0R)
- **MFE**: 0.26 points
- **MAE**: 146.39 points

### Trade #784 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 07:45:00
- **FVG 5m**: 22194.68 - 22208.19
- **Entrée**: 22191.87 @ 2025-06-05 07:48:00
- **Stop Loss**: 22219.30
- **Risk**: 27.43 points
- **TP 1RR**: 22164.45 ❌
- **TP 1.5RR**: 22150.73 ❌
- **TP 2RR**: 22137.02 ❌
- **TP 2.5RR**: 22123.31 ❌
- **TP 3RR**: 22109.59 ❌
- **TP 3.5RR**: 22095.88 ❌
- **TP 4RR**: 22082.17 ❌
- **TP 4.5RR**: 22068.46 ❌
- **TP 5RR**: 22054.74 ❌
- **PnL**: -27.43 points (-1.0R)
- **MFE**: 0.26 points
- **MAE**: 146.39 points

### Trade #785 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 07:45:00
- **FVG 5m**: 22194.68 - 22208.19
- **Entrée**: 22191.87 @ 2025-06-05 07:48:00
- **Stop Loss**: 22219.30
- **Risk**: 27.43 points
- **TP 1RR**: 22164.45 ❌
- **TP 1.5RR**: 22150.73 ❌
- **TP 2RR**: 22137.02 ❌
- **TP 2.5RR**: 22123.31 ❌
- **TP 3RR**: 22109.59 ❌
- **TP 3.5RR**: 22095.88 ❌
- **TP 4RR**: 22082.17 ❌
- **TP 4.5RR**: 22068.46 ❌
- **TP 5RR**: 22054.74 ❌
- **PnL**: -27.43 points (-1.0R)
- **MFE**: 0.26 points
- **MAE**: 146.39 points

### Trade #786 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 08:45:00
- **FVG 5m**: 22200.54 - 22207.43
- **Entrée**: 22211.76 @ 2025-06-05 09:24:00
- **Stop Loss**: 22189.44
- **Risk**: 22.32 points
- **TP 1RR**: 22234.09 ✅
- **TP 1.5RR**: 22245.25 ❌
- **TP 2RR**: 22256.41 ❌
- **TP 2.5RR**: 22267.57 ❌
- **TP 3RR**: 22278.73 ❌
- **TP 3.5RR**: 22289.89 ❌
- **TP 4RR**: 22301.05 ❌
- **TP 4.5RR**: 22312.21 ❌
- **TP 5RR**: 22323.37 ❌
- **PnL**: -22.32 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 36.47 points

### Trade #787 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 11:00:00
- **FVG 5m**: 22314.79 - 22346.16
- **Entrée**: 22306.63 @ 2025-06-05 11:14:00
- **Stop Loss**: 22357.34
- **Risk**: 50.70 points
- **TP 1RR**: 22255.93 ✅
- **TP 1.5RR**: 22230.58 ✅
- **TP 2RR**: 22205.23 ✅
- **TP 2.5RR**: 22179.88 ✅
- **TP 3RR**: 22154.53 ✅
- **TP 3.5RR**: 22129.18 ✅
- **TP 4RR**: 22103.83 ✅
- **TP 4.5RR**: 22078.47 ✅
- **TP 5RR**: 22053.12 ✅
- **PnL**: 253.51 points (5.0R)
- **MFE**: 265.99 points
- **MAE**: 4.59 points

### Trade #788 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 11:00:00
- **FVG 5m**: 22314.79 - 22346.16
- **Entrée**: 22306.63 @ 2025-06-05 11:14:00
- **Stop Loss**: 22357.34
- **Risk**: 50.70 points
- **TP 1RR**: 22255.93 ✅
- **TP 1.5RR**: 22230.58 ✅
- **TP 2RR**: 22205.23 ✅
- **TP 2.5RR**: 22179.88 ✅
- **TP 3RR**: 22154.53 ✅
- **TP 3.5RR**: 22129.18 ✅
- **TP 4RR**: 22103.83 ✅
- **TP 4.5RR**: 22078.47 ✅
- **TP 5RR**: 22053.12 ✅
- **PnL**: 253.51 points (5.0R)
- **MFE**: 265.99 points
- **MAE**: 4.59 points

### Trade #789 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 13:15:00
- **FVG 5m**: 22143.93 - 22157.70
- **Entrée**: 22158.21 @ 2025-06-05 13:35:00
- **Stop Loss**: 22132.86
- **Risk**: 25.35 points
- **TP 1RR**: 22183.56 ❌
- **TP 1.5RR**: 22196.24 ❌
- **TP 2RR**: 22208.92 ❌
- **TP 2.5RR**: 22221.59 ❌
- **TP 3RR**: 22234.27 ❌
- **TP 3.5RR**: 22246.95 ❌
- **TP 4RR**: 22259.62 ❌
- **TP 4.5RR**: 22272.30 ❌
- **TP 5RR**: 22284.98 ❌
- **PnL**: -25.35 points (-1.0R)
- **MFE**: 18.62 points
- **MAE**: 29.07 points

### Trade #790 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 13:15:00
- **FVG 5m**: 22143.93 - 22157.70
- **Entrée**: 22158.21 @ 2025-06-05 13:35:00
- **Stop Loss**: 22132.86
- **Risk**: 25.35 points
- **TP 1RR**: 22183.56 ❌
- **TP 1.5RR**: 22196.24 ❌
- **TP 2RR**: 22208.92 ❌
- **TP 2.5RR**: 22221.59 ❌
- **TP 3RR**: 22234.27 ❌
- **TP 3.5RR**: 22246.95 ❌
- **TP 4RR**: 22259.62 ❌
- **TP 4.5RR**: 22272.30 ❌
- **TP 5RR**: 22284.98 ❌
- **PnL**: -25.35 points (-1.0R)
- **MFE**: 18.62 points
- **MAE**: 29.07 points

### Trade #791 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 15:30:00
- **FVG 5m**: 22023.30 - 22041.15
- **Entrée**: 22005.70 @ 2025-06-05 15:31:00
- **Stop Loss**: 22052.17
- **Risk**: 46.47 points
- **TP 1RR**: 21959.23 ✅
- **TP 1.5RR**: 21936.00 ✅
- **TP 2RR**: 21912.76 ✅
- **TP 2.5RR**: 21889.53 ❌
- **TP 3RR**: 21866.30 ❌
- **TP 3.5RR**: 21843.06 ❌
- **TP 4RR**: 21819.83 ❌
- **TP 4.5RR**: 21796.59 ❌
- **TP 5RR**: 21773.36 ❌
- **PnL**: -46.47 points (-1.0R)
- **MFE**: 103.03 points
- **MAE**: 46.67 points

### Trade #792 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 17:00:00
- **FVG 5m**: 21974.08 - 21986.07
- **Entrée**: 21990.15 @ 2025-06-05 17:54:00
- **Stop Loss**: 21963.09
- **Risk**: 27.05 points
- **TP 1RR**: 22017.20 ✅
- **TP 1.5RR**: 22030.73 ✅
- **TP 2RR**: 22044.25 ✅
- **TP 2.5RR**: 22057.78 ✅
- **TP 3RR**: 22071.31 ✅
- **TP 3.5RR**: 22084.83 ✅
- **TP 4RR**: 22098.36 ✅
- **TP 4.5RR**: 22111.89 ✅
- **TP 5RR**: 22125.42 ✅
- **PnL**: 135.27 points (5.0R)
- **MFE**: 136.44 points
- **MAE**: 17.09 points

### Trade #793 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 17:00:00
- **FVG 5m**: 21974.08 - 21986.07
- **Entrée**: 21990.15 @ 2025-06-05 17:54:00
- **Stop Loss**: 21963.09
- **Risk**: 27.05 points
- **TP 1RR**: 22017.20 ✅
- **TP 1.5RR**: 22030.73 ✅
- **TP 2RR**: 22044.25 ✅
- **TP 2.5RR**: 22057.78 ✅
- **TP 3RR**: 22071.31 ✅
- **TP 3.5RR**: 22084.83 ✅
- **TP 4RR**: 22098.36 ✅
- **TP 4.5RR**: 22111.89 ✅
- **TP 5RR**: 22125.42 ✅
- **PnL**: 135.27 points (5.0R)
- **MFE**: 136.44 points
- **MAE**: 17.09 points

### Trade #794 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 20:45:00
- **FVG 5m**: 22010.29 - 22018.71
- **Entrée**: 22010.04 @ 2025-06-05 21:10:00
- **Stop Loss**: 22029.72
- **Risk**: 19.68 points
- **TP 1RR**: 21990.36 ❌
- **TP 1.5RR**: 21980.52 ❌
- **TP 2RR**: 21970.68 ❌
- **TP 2.5RR**: 21960.84 ❌
- **TP 3RR**: 21951.00 ❌
- **TP 3.5RR**: 21941.16 ❌
- **TP 4RR**: 21931.32 ❌
- **TP 4.5RR**: 21921.48 ❌
- **TP 5RR**: 21911.64 ❌
- **PnL**: -19.68 points (-1.0R)
- **MFE**: 3.83 points
- **MAE**: 20.40 points

### Trade #795 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-06 11:45:00
- **FVG 5m**: 22235.74 - 22242.62
- **Entrée**: 22243.90 @ 2025-06-06 12:38:00
- **Stop Loss**: 22224.62
- **Risk**: 19.28 points
- **TP 1RR**: 22263.18 ✅
- **TP 1.5RR**: 22272.82 ✅
- **TP 2RR**: 22282.46 ✅
- **TP 2.5RR**: 22292.09 ✅
- **TP 3RR**: 22301.73 ✅
- **TP 3.5RR**: 22311.37 ✅
- **TP 4RR**: 22321.01 ❌
- **TP 4.5RR**: 22330.65 ❌
- **TP 5RR**: 22340.29 ❌
- **PnL**: -19.28 points (-1.0R)
- **MFE**: 69.37 points
- **MAE**: 21.42 points

### Trade #796 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-09 08:30:00
- **FVG 5m**: 22241.35 - 22244.66
- **Entrée**: 22248.23 @ 2025-06-09 08:51:00
- **Stop Loss**: 22230.23
- **Risk**: 18.01 points
- **TP 1RR**: 22266.24 ❌
- **TP 1.5RR**: 22275.24 ❌
- **TP 2RR**: 22284.25 ❌
- **TP 2.5RR**: 22293.25 ❌
- **TP 3RR**: 22302.25 ❌
- **TP 3.5RR**: 22311.26 ❌
- **TP 4RR**: 22320.26 ❌
- **TP 4.5RR**: 22329.26 ❌
- **TP 5RR**: 22338.26 ❌
- **PnL**: -18.01 points (-1.0R)
- **MFE**: 10.20 points
- **MAE**: 24.99 points

### Trade #797 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-09 09:30:00
- **FVG 5m**: 22266.59 - 22278.58
- **Entrée**: 22266.34 @ 2025-06-09 10:19:00
- **Stop Loss**: 22289.72
- **Risk**: 23.38 points
- **TP 1RR**: 22242.96 ❌
- **TP 1.5RR**: 22231.27 ❌
- **TP 2RR**: 22219.58 ❌
- **TP 2.5RR**: 22207.89 ❌
- **TP 3RR**: 22196.20 ❌
- **TP 3.5RR**: 22184.51 ❌
- **TP 4RR**: 22172.82 ❌
- **TP 4.5RR**: 22161.13 ❌
- **TP 5RR**: 22149.44 ❌
- **PnL**: -23.38 points (-1.0R)
- **MFE**: 14.79 points
- **MAE**: 23.46 points

### Trade #798 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-09 09:30:00
- **FVG 5m**: 22266.59 - 22278.58
- **Entrée**: 22266.34 @ 2025-06-09 10:19:00
- **Stop Loss**: 22289.72
- **Risk**: 23.38 points
- **TP 1RR**: 22242.96 ❌
- **TP 1.5RR**: 22231.27 ❌
- **TP 2RR**: 22219.58 ❌
- **TP 2.5RR**: 22207.89 ❌
- **TP 3RR**: 22196.20 ❌
- **TP 3.5RR**: 22184.51 ❌
- **TP 4RR**: 22172.82 ❌
- **TP 4.5RR**: 22161.13 ❌
- **TP 5RR**: 22149.44 ❌
- **PnL**: -23.38 points (-1.0R)
- **MFE**: 14.79 points
- **MAE**: 23.46 points

### Trade #799 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-09 14:45:00
- **FVG 5m**: 22292.86 - 22297.71
- **Entrée**: 22268.64 @ 2025-06-09 14:46:00
- **Stop Loss**: 22308.86
- **Risk**: 40.22 points
- **TP 1RR**: 22228.41 ❌
- **TP 1.5RR**: 22208.30 ❌
- **TP 2RR**: 22188.19 ❌
- **TP 2.5RR**: 22168.08 ❌
- **TP 3RR**: 22147.97 ❌
- **TP 3.5RR**: 22127.86 ❌
- **TP 4RR**: 22107.75 ❌
- **TP 4.5RR**: 22087.64 ❌
- **TP 5RR**: 22067.53 ❌
- **PnL**: -40.22 points (-1.0R)
- **MFE**: 33.66 points
- **MAE**: 40.29 points

### Trade #800 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 00:15:00
- **FVG 5m**: 22380.08 - 22382.38
- **Entrée**: 22352.79 @ 2025-06-10 00:16:00
- **Stop Loss**: 22393.57
- **Risk**: 40.77 points
- **TP 1RR**: 22312.02 ✅
- **TP 1.5RR**: 22291.63 ✅
- **TP 2RR**: 22271.25 ✅
- **TP 2.5RR**: 22250.86 ✅
- **TP 3RR**: 22230.47 ✅
- **TP 3.5RR**: 22210.08 ✅
- **TP 4RR**: 22189.70 ✅
- **TP 4.5RR**: 22169.31 ✅
- **TP 5RR**: 22148.92 ❌
- **PnL**: -40.77 points (-1.0R)
- **MFE**: 183.87 points
- **MAE**: 56.11 points

### Trade #801 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 00:15:00
- **FVG 5m**: 22380.08 - 22382.38
- **Entrée**: 22352.79 @ 2025-06-10 00:16:00
- **Stop Loss**: 22393.57
- **Risk**: 40.77 points
- **TP 1RR**: 22312.02 ✅
- **TP 1.5RR**: 22291.63 ✅
- **TP 2RR**: 22271.25 ✅
- **TP 2.5RR**: 22250.86 ✅
- **TP 3RR**: 22230.47 ✅
- **TP 3.5RR**: 22210.08 ✅
- **TP 4RR**: 22189.70 ✅
- **TP 4.5RR**: 22169.31 ✅
- **TP 5RR**: 22148.92 ❌
- **PnL**: -40.77 points (-1.0R)
- **MFE**: 183.87 points
- **MAE**: 56.11 points

### Trade #802 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 00:15:00
- **FVG 5m**: 22380.08 - 22382.38
- **Entrée**: 22352.79 @ 2025-06-10 00:16:00
- **Stop Loss**: 22393.57
- **Risk**: 40.77 points
- **TP 1RR**: 22312.02 ✅
- **TP 1.5RR**: 22291.63 ✅
- **TP 2RR**: 22271.25 ✅
- **TP 2.5RR**: 22250.86 ✅
- **TP 3RR**: 22230.47 ✅
- **TP 3.5RR**: 22210.08 ✅
- **TP 4RR**: 22189.70 ✅
- **TP 4.5RR**: 22169.31 ✅
- **TP 5RR**: 22148.92 ❌
- **PnL**: -40.77 points (-1.0R)
- **MFE**: 183.87 points
- **MAE**: 56.11 points

### Trade #803 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 02:30:00
- **FVG 5m**: 22242.37 - 22247.98
- **Entrée**: 22238.03 @ 2025-06-10 02:32:00
- **Stop Loss**: 22259.10
- **Risk**: 21.07 points
- **TP 1RR**: 22216.96 ✅
- **TP 1.5RR**: 22206.43 ✅
- **TP 2RR**: 22195.89 ✅
- **TP 2.5RR**: 22185.36 ✅
- **TP 3RR**: 22174.82 ✅
- **TP 3.5RR**: 22164.29 ❌
- **TP 4RR**: 22153.75 ❌
- **TP 4.5RR**: 22143.22 ❌
- **TP 5RR**: 22132.68 ❌
- **PnL**: -21.07 points (-1.0R)
- **MFE**: 69.11 points
- **MAE**: 22.70 points

### Trade #804 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 02:30:00
- **FVG 5m**: 22242.37 - 22247.98
- **Entrée**: 22238.03 @ 2025-06-10 02:32:00
- **Stop Loss**: 22259.10
- **Risk**: 21.07 points
- **TP 1RR**: 22216.96 ✅
- **TP 1.5RR**: 22206.43 ✅
- **TP 2RR**: 22195.89 ✅
- **TP 2.5RR**: 22185.36 ✅
- **TP 3RR**: 22174.82 ✅
- **TP 3.5RR**: 22164.29 ❌
- **TP 4RR**: 22153.75 ❌
- **TP 4.5RR**: 22143.22 ❌
- **TP 5RR**: 22132.68 ❌
- **PnL**: -21.07 points (-1.0R)
- **MFE**: 69.11 points
- **MAE**: 22.70 points

### Trade #805 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 02:30:00
- **FVG 5m**: 22242.37 - 22247.98
- **Entrée**: 22238.03 @ 2025-06-10 02:32:00
- **Stop Loss**: 22259.10
- **Risk**: 21.07 points
- **TP 1RR**: 22216.96 ✅
- **TP 1.5RR**: 22206.43 ✅
- **TP 2RR**: 22195.89 ✅
- **TP 2.5RR**: 22185.36 ✅
- **TP 3RR**: 22174.82 ✅
- **TP 3.5RR**: 22164.29 ❌
- **TP 4RR**: 22153.75 ❌
- **TP 4.5RR**: 22143.22 ❌
- **TP 5RR**: 22132.68 ❌
- **PnL**: -21.07 points (-1.0R)
- **MFE**: 69.11 points
- **MAE**: 22.70 points

### Trade #806 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 02:45:00
- **FVG 5m**: 22217.12 - 22224.77
- **Entrée**: 22226.81 @ 2025-06-10 02:55:00
- **Stop Loss**: 22206.01
- **Risk**: 20.80 points
- **TP 1RR**: 22247.61 ✅
- **TP 1.5RR**: 22258.01 ❌
- **TP 2RR**: 22268.41 ❌
- **TP 2.5RR**: 22278.81 ❌
- **TP 3RR**: 22289.21 ❌
- **TP 3.5RR**: 22299.61 ❌
- **TP 4RR**: 22310.01 ❌
- **TP 4.5RR**: 22320.41 ❌
- **TP 5RR**: 22330.81 ❌
- **PnL**: -20.80 points (-1.0R)
- **MFE**: 26.27 points
- **MAE**: 28.56 points

### Trade #807 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 02:45:00
- **FVG 5m**: 22217.12 - 22224.77
- **Entrée**: 22226.81 @ 2025-06-10 02:55:00
- **Stop Loss**: 22206.01
- **Risk**: 20.80 points
- **TP 1RR**: 22247.61 ✅
- **TP 1.5RR**: 22258.01 ❌
- **TP 2RR**: 22268.41 ❌
- **TP 2.5RR**: 22278.81 ❌
- **TP 3RR**: 22289.21 ❌
- **TP 3.5RR**: 22299.61 ❌
- **TP 4RR**: 22310.01 ❌
- **TP 4.5RR**: 22320.41 ❌
- **TP 5RR**: 22330.81 ❌
- **PnL**: -20.80 points (-1.0R)
- **MFE**: 26.27 points
- **MAE**: 28.56 points

### Trade #808 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 08:30:00
- **FVG 5m**: 22282.92 - 22288.02
- **Entrée**: 22279.35 @ 2025-06-10 08:31:00
- **Stop Loss**: 22299.16
- **Risk**: 19.81 points
- **TP 1RR**: 22259.53 ❌
- **TP 1.5RR**: 22249.62 ❌
- **TP 2RR**: 22239.72 ❌
- **TP 2.5RR**: 22229.81 ❌
- **TP 3RR**: 22219.90 ❌
- **TP 3.5RR**: 22209.99 ❌
- **TP 4RR**: 22200.09 ❌
- **TP 4.5RR**: 22190.18 ❌
- **TP 5RR**: 22180.27 ❌
- **PnL**: -19.81 points (-1.0R)
- **MFE**: 15.81 points
- **MAE**: 20.15 points

### Trade #809 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 12:15:00
- **FVG 5m**: 22316.84 - 22333.41
- **Entrée**: 22309.44 @ 2025-06-10 12:40:00
- **Stop Loss**: 22344.58
- **Risk**: 35.14 points
- **TP 1RR**: 22274.30 ✅
- **TP 1.5RR**: 22256.73 ❌
- **TP 2RR**: 22239.16 ❌
- **TP 2.5RR**: 22221.59 ❌
- **TP 3RR**: 22204.02 ❌
- **TP 3.5RR**: 22186.45 ❌
- **TP 4RR**: 22168.88 ❌
- **TP 4.5RR**: 22151.31 ❌
- **TP 5RR**: 22133.74 ❌
- **PnL**: -35.14 points (-1.0R)
- **MFE**: 49.99 points
- **MAE**: 39.02 points

### Trade #810 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 14:00:00
- **FVG 5m**: 22301.53 - 22309.18
- **Entrée**: 22392.32 @ 2025-06-10 14:01:00
- **Stop Loss**: 22290.38
- **Risk**: 101.94 points
- **TP 1RR**: 22494.26 ✅
- **TP 1.5RR**: 22545.23 ✅
- **TP 2RR**: 22596.20 ❌
- **TP 2.5RR**: 22647.17 ❌
- **TP 3RR**: 22698.14 ❌
- **TP 3.5RR**: 22749.11 ❌
- **TP 4RR**: 22800.08 ❌
- **TP 4.5RR**: 22851.05 ❌
- **TP 5RR**: 22902.02 ❌
- **PnL**: -101.94 points (-1.0R)
- **MFE**: 158.12 points
- **MAE**: 122.16 points

### Trade #811 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 18:15:00
- **FVG 5m**: 22394.87 - 22414.51
- **Entrée**: 22392.58 @ 2025-06-10 18:42:00
- **Stop Loss**: 22425.72
- **Risk**: 33.14 points
- **TP 1RR**: 22359.44 ✅
- **TP 1.5RR**: 22342.87 ✅
- **TP 2RR**: 22326.30 ✅
- **TP 2.5RR**: 22309.73 ✅
- **TP 3RR**: 22293.16 ❌
- **TP 3.5RR**: 22276.59 ❌
- **TP 4RR**: 22260.02 ❌
- **TP 4.5RR**: 22243.45 ❌
- **TP 5RR**: 22226.88 ❌
- **PnL**: -33.14 points (-1.0R)
- **MFE**: 87.22 points
- **MAE**: 42.33 points

### Trade #812 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 19:15:00
- **FVG 5m**: 22391.05 - 22399.97
- **Entrée**: 22390.03 @ 2025-06-10 19:16:00
- **Stop Loss**: 22411.17
- **Risk**: 21.15 points
- **TP 1RR**: 22368.88 ✅
- **TP 1.5RR**: 22358.31 ✅
- **TP 2RR**: 22347.74 ✅
- **TP 2.5RR**: 22337.16 ✅
- **TP 3RR**: 22326.59 ✅
- **TP 3.5RR**: 22316.02 ✅
- **TP 4RR**: 22305.44 ✅
- **TP 4.5RR**: 22294.87 ❌
- **TP 5RR**: 22284.30 ❌
- **PnL**: -21.15 points (-1.0R)
- **MFE**: 84.67 points
- **MAE**: 44.88 points

### Trade #813 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 04:30:00
- **FVG 5m**: 22378.04 - 22389.77
- **Entrée**: 22376.51 @ 2025-06-11 04:33:00
- **Stop Loss**: 22400.97
- **Risk**: 24.46 points
- **TP 1RR**: 22352.06 ✅
- **TP 1.5RR**: 22339.83 ✅
- **TP 2RR**: 22327.60 ✅
- **TP 2.5RR**: 22315.37 ❌
- **TP 3RR**: 22303.14 ❌
- **TP 3.5RR**: 22290.91 ❌
- **TP 4RR**: 22278.69 ❌
- **TP 4.5RR**: 22266.46 ❌
- **TP 5RR**: 22254.23 ❌
- **PnL**: -24.46 points (-1.0R)
- **MFE**: 54.58 points
- **MAE**: 58.40 points

### Trade #814 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 07:00:00
- **FVG 5m**: 22337.75 - 22346.42
- **Entrée**: 22376.00 @ 2025-06-11 07:01:00
- **Stop Loss**: 22326.58
- **Risk**: 49.42 points
- **TP 1RR**: 22425.42 ✅
- **TP 1.5RR**: 22450.14 ✅
- **TP 2RR**: 22474.85 ✅
- **TP 2.5RR**: 22499.56 ✅
- **TP 3RR**: 22524.27 ✅
- **TP 3.5RR**: 22548.98 ✅
- **TP 4RR**: 22573.69 ❌
- **TP 4.5RR**: 22598.40 ❌
- **TP 5RR**: 22623.12 ❌
- **PnL**: -49.42 points (-1.0R)
- **MFE**: 174.44 points
- **MAE**: 67.84 points

### Trade #815 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 08:30:00
- **FVG 5m**: 22400.48 - 22500.96
- **Entrée**: 22364.78 @ 2025-06-11 08:46:00
- **Stop Loss**: 22512.21
- **Risk**: 147.43 points
- **TP 1RR**: 22217.35 ✅
- **TP 1.5RR**: 22143.63 ✅
- **TP 2RR**: 22069.91 ✅
- **TP 2.5RR**: 21996.19 ✅
- **TP 3RR**: 21922.48 ✅
- **TP 3.5RR**: 21848.76 ✅
- **TP 4RR**: 21775.04 ❌
- **TP 4.5RR**: 21701.32 ❌
- **TP 5RR**: 21627.61 ❌
- **PnL**: -147.43 points (-1.0R)
- **MFE**: 584.44 points
- **MAE**: 148.75 points

### Trade #816 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 08:30:00
- **FVG 5m**: 22400.48 - 22500.96
- **Entrée**: 22364.78 @ 2025-06-11 08:46:00
- **Stop Loss**: 22512.21
- **Risk**: 147.43 points
- **TP 1RR**: 22217.35 ✅
- **TP 1.5RR**: 22143.63 ✅
- **TP 2RR**: 22069.91 ✅
- **TP 2.5RR**: 21996.19 ✅
- **TP 3RR**: 21922.48 ✅
- **TP 3.5RR**: 21848.76 ✅
- **TP 4RR**: 21775.04 ❌
- **TP 4.5RR**: 21701.32 ❌
- **TP 5RR**: 21627.61 ❌
- **PnL**: -147.43 points (-1.0R)
- **MFE**: 584.44 points
- **MAE**: 148.75 points

### Trade #817 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 13:30:00
- **FVG 5m**: 22281.39 - 22290.57
- **Entrée**: 22308.16 @ 2025-06-11 13:31:00
- **Stop Loss**: 22270.25
- **Risk**: 37.92 points
- **TP 1RR**: 22346.08 ✅
- **TP 1.5RR**: 22365.04 ❌
- **TP 2RR**: 22384.00 ❌
- **TP 2.5RR**: 22402.96 ❌
- **TP 3RR**: 22421.92 ❌
- **TP 3.5RR**: 22440.88 ❌
- **TP 4RR**: 22459.84 ❌
- **TP 4.5RR**: 22478.80 ❌
- **TP 5RR**: 22497.76 ❌
- **PnL**: -37.92 points (-1.0R)
- **MFE**: 46.67 points
- **MAE**: 42.33 points

### Trade #818 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 13:30:00
- **FVG 5m**: 22281.39 - 22290.57
- **Entrée**: 22308.16 @ 2025-06-11 13:31:00
- **Stop Loss**: 22270.25
- **Risk**: 37.92 points
- **TP 1RR**: 22346.08 ✅
- **TP 1.5RR**: 22365.04 ❌
- **TP 2RR**: 22384.00 ❌
- **TP 2.5RR**: 22402.96 ❌
- **TP 3RR**: 22421.92 ❌
- **TP 3.5RR**: 22440.88 ❌
- **TP 4RR**: 22459.84 ❌
- **TP 4.5RR**: 22478.80 ❌
- **TP 5RR**: 22497.76 ❌
- **PnL**: -37.92 points (-1.0R)
- **MFE**: 46.67 points
- **MAE**: 42.33 points

### Trade #819 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22218.65 - 22224.26
- **Entrée**: 22228.60 @ 2025-06-12 03:50:00
- **Stop Loss**: 22207.54
- **Risk**: 21.06 points
- **TP 1RR**: 22249.65 ✅
- **TP 1.5RR**: 22260.18 ✅
- **TP 2RR**: 22270.71 ✅
- **TP 2.5RR**: 22281.23 ✅
- **TP 3RR**: 22291.76 ❌
- **TP 3.5RR**: 22302.29 ❌
- **TP 4RR**: 22312.82 ❌
- **TP 4.5RR**: 22323.35 ❌
- **TP 5RR**: 22333.87 ❌
- **PnL**: -21.06 points (-1.0R)
- **MFE**: 53.81 points
- **MAE**: 31.88 points

### Trade #820 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22218.65 - 22224.26
- **Entrée**: 22228.60 @ 2025-06-12 03:50:00
- **Stop Loss**: 22207.54
- **Risk**: 21.06 points
- **TP 1RR**: 22249.65 ✅
- **TP 1.5RR**: 22260.18 ✅
- **TP 2RR**: 22270.71 ✅
- **TP 2.5RR**: 22281.23 ✅
- **TP 3RR**: 22291.76 ❌
- **TP 3.5RR**: 22302.29 ❌
- **TP 4RR**: 22312.82 ❌
- **TP 4.5RR**: 22323.35 ❌
- **TP 5RR**: 22333.87 ❌
- **PnL**: -21.06 points (-1.0R)
- **MFE**: 53.81 points
- **MAE**: 31.88 points

### Trade #821 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22218.65 - 22224.26
- **Entrée**: 22228.60 @ 2025-06-12 03:50:00
- **Stop Loss**: 22207.54
- **Risk**: 21.06 points
- **TP 1RR**: 22249.65 ✅
- **TP 1.5RR**: 22260.18 ✅
- **TP 2RR**: 22270.71 ✅
- **TP 2.5RR**: 22281.23 ✅
- **TP 3RR**: 22291.76 ❌
- **TP 3.5RR**: 22302.29 ❌
- **TP 4RR**: 22312.82 ❌
- **TP 4.5RR**: 22323.35 ❌
- **TP 5RR**: 22333.87 ❌
- **PnL**: -21.06 points (-1.0R)
- **MFE**: 53.81 points
- **MAE**: 31.88 points

### Trade #822 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22218.65 - 22224.26
- **Entrée**: 22228.60 @ 2025-06-12 03:50:00
- **Stop Loss**: 22207.54
- **Risk**: 21.06 points
- **TP 1RR**: 22249.65 ✅
- **TP 1.5RR**: 22260.18 ✅
- **TP 2RR**: 22270.71 ✅
- **TP 2.5RR**: 22281.23 ✅
- **TP 3RR**: 22291.76 ❌
- **TP 3.5RR**: 22302.29 ❌
- **TP 4RR**: 22312.82 ❌
- **TP 4.5RR**: 22323.35 ❌
- **TP 5RR**: 22333.87 ❌
- **PnL**: -21.06 points (-1.0R)
- **MFE**: 53.81 points
- **MAE**: 31.88 points

### Trade #823 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22218.65 - 22224.26
- **Entrée**: 22228.60 @ 2025-06-12 03:50:00
- **Stop Loss**: 22207.54
- **Risk**: 21.06 points
- **TP 1RR**: 22249.65 ✅
- **TP 1.5RR**: 22260.18 ✅
- **TP 2RR**: 22270.71 ✅
- **TP 2.5RR**: 22281.23 ✅
- **TP 3RR**: 22291.76 ❌
- **TP 3.5RR**: 22302.29 ❌
- **TP 4RR**: 22312.82 ❌
- **TP 4.5RR**: 22323.35 ❌
- **TP 5RR**: 22333.87 ❌
- **PnL**: -21.06 points (-1.0R)
- **MFE**: 53.81 points
- **MAE**: 31.88 points

### Trade #824 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:45:00
- **FVG 5m**: 22218.65 - 22224.26
- **Entrée**: 22228.60 @ 2025-06-12 03:50:00
- **Stop Loss**: 22207.54
- **Risk**: 21.06 points
- **TP 1RR**: 22249.65 ✅
- **TP 1.5RR**: 22260.18 ✅
- **TP 2RR**: 22270.71 ✅
- **TP 2.5RR**: 22281.23 ✅
- **TP 3RR**: 22291.76 ❌
- **TP 3.5RR**: 22302.29 ❌
- **TP 4RR**: 22312.82 ❌
- **TP 4.5RR**: 22323.35 ❌
- **TP 5RR**: 22333.87 ❌
- **PnL**: -21.06 points (-1.0R)
- **MFE**: 53.81 points
- **MAE**: 31.88 points

### Trade #825 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 09:00:00
- **FVG 5m**: 22186.52 - 22202.07
- **Entrée**: 22306.12 @ 2025-06-12 09:01:00
- **Stop Loss**: 22175.42
- **Risk**: 130.70 points
- **TP 1RR**: 22436.82 ❌
- **TP 1.5RR**: 22502.17 ❌
- **TP 2RR**: 22567.53 ❌
- **TP 2.5RR**: 22632.88 ❌
- **TP 3RR**: 22698.23 ❌
- **TP 3.5RR**: 22763.58 ❌
- **TP 4RR**: 22828.93 ❌
- **TP 4.5RR**: 22894.28 ❌
- **TP 5RR**: 22959.63 ❌
- **PnL**: -130.70 points (-1.0R)
- **MFE**: 112.98 points
- **MAE**: 170.87 points

### Trade #826 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 09:15:00
- **FVG 5m**: 22186.52 - 22202.07
- **Entrée**: 22356.11 @ 2025-06-12 09:16:00
- **Stop Loss**: 22175.42
- **Risk**: 180.69 points
- **TP 1RR**: 22536.79 ❌
- **TP 1.5RR**: 22627.14 ❌
- **TP 2RR**: 22717.48 ❌
- **TP 2.5RR**: 22807.82 ❌
- **TP 3RR**: 22898.17 ❌
- **TP 3.5RR**: 22988.51 ❌
- **TP 4RR**: 23078.85 ❌
- **TP 4.5RR**: 23169.19 ❌
- **TP 5RR**: 23259.54 ❌
- **PnL**: -180.69 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 220.85 points

### Trade #827 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 13:30:00
- **FVG 5m**: 22390.03 - 22397.42
- **Entrée**: 22355.34 @ 2025-06-12 13:31:00
- **Stop Loss**: 22408.62
- **Risk**: 53.28 points
- **TP 1RR**: 22302.07 ✅
- **TP 1.5RR**: 22275.43 ✅
- **TP 2RR**: 22248.79 ✅
- **TP 2.5RR**: 22222.15 ✅
- **TP 3RR**: 22195.51 ✅
- **TP 3.5RR**: 22168.87 ✅
- **TP 4RR**: 22142.23 ✅
- **TP 4.5RR**: 22115.59 ✅
- **TP 5RR**: 22088.95 ✅
- **PnL**: 266.39 points (5.0R)
- **MFE**: 282.82 points
- **MAE**: 39.02 points

### Trade #828 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 19:15:00
- **FVG 5m**: 22313.52 - 22317.35
- **Entrée**: 22109.24 @ 2025-06-12 19:16:00
- **Stop Loss**: 22328.50
- **Risk**: 219.26 points
- **TP 1RR**: 21889.98 ❌
- **TP 1.5RR**: 21780.35 ❌
- **TP 2RR**: 21670.72 ❌
- **TP 2.5RR**: 21561.09 ❌
- **TP 3RR**: 21451.46 ❌
- **TP 3.5RR**: 21341.83 ❌
- **TP 4RR**: 21232.20 ❌
- **TP 4.5RR**: 21122.57 ❌
- **TP 5RR**: 21012.94 ❌
- **PnL**: -219.26 points (-1.0R)
- **MFE**: 206.57 points
- **MAE**: 219.73 points

### Trade #829 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 19:15:00
- **FVG 5m**: 22313.52 - 22317.35
- **Entrée**: 22109.24 @ 2025-06-12 19:16:00
- **Stop Loss**: 22328.50
- **Risk**: 219.26 points
- **TP 1RR**: 21889.98 ❌
- **TP 1.5RR**: 21780.35 ❌
- **TP 2RR**: 21670.72 ❌
- **TP 2.5RR**: 21561.09 ❌
- **TP 3RR**: 21451.46 ❌
- **TP 3.5RR**: 21341.83 ❌
- **TP 4RR**: 21232.20 ❌
- **TP 4.5RR**: 21122.57 ❌
- **TP 5RR**: 21012.94 ❌
- **PnL**: -219.26 points (-1.0R)
- **MFE**: 206.57 points
- **MAE**: 219.73 points

### Trade #830 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 19:15:00
- **FVG 5m**: 22313.52 - 22317.35
- **Entrée**: 22109.24 @ 2025-06-12 19:16:00
- **Stop Loss**: 22328.50
- **Risk**: 219.26 points
- **TP 1RR**: 21889.98 ❌
- **TP 1.5RR**: 21780.35 ❌
- **TP 2RR**: 21670.72 ❌
- **TP 2.5RR**: 21561.09 ❌
- **TP 3RR**: 21451.46 ❌
- **TP 3.5RR**: 21341.83 ❌
- **TP 4RR**: 21232.20 ❌
- **TP 4.5RR**: 21122.57 ❌
- **TP 5RR**: 21012.94 ❌
- **PnL**: -219.26 points (-1.0R)
- **MFE**: 206.57 points
- **MAE**: 219.73 points

### Trade #831 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-13 01:15:00
- **FVG 5m**: 22003.92 - 22028.40
- **Entrée**: 22003.15 @ 2025-06-13 01:40:00
- **Stop Loss**: 22039.41
- **Risk**: 36.26 points
- **TP 1RR**: 21966.89 ❌
- **TP 1.5RR**: 21948.76 ❌
- **TP 2RR**: 21930.63 ❌
- **TP 2.5RR**: 21912.50 ❌
- **TP 3RR**: 21894.37 ❌
- **TP 3.5RR**: 21876.24 ❌
- **TP 4RR**: 21858.11 ❌
- **TP 4.5RR**: 21839.97 ❌
- **TP 5RR**: 21821.84 ❌
- **PnL**: -36.26 points (-1.0R)
- **MFE**: 4.59 points
- **MAE**: 37.49 points

### Trade #832 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22107.46 - 22119.70
- **Entrée**: 22199.27 @ 2025-06-13 08:31:00
- **Stop Loss**: 22096.40
- **Risk**: 102.86 points
- **TP 1RR**: 22302.13 ❌
- **TP 1.5RR**: 22353.56 ❌
- **TP 2RR**: 22404.99 ❌
- **TP 2.5RR**: 22456.43 ❌
- **TP 3RR**: 22507.86 ❌
- **TP 3.5RR**: 22559.29 ❌
- **TP 4RR**: 22610.72 ❌
- **TP 4.5RR**: 22662.15 ❌
- **TP 5RR**: 22713.58 ❌
- **PnL**: -102.86 points (-1.0R)
- **MFE**: 33.66 points
- **MAE**: 111.96 points

### Trade #833 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22107.46 - 22119.70
- **Entrée**: 22199.27 @ 2025-06-13 08:31:00
- **Stop Loss**: 22096.40
- **Risk**: 102.86 points
- **TP 1RR**: 22302.13 ❌
- **TP 1.5RR**: 22353.56 ❌
- **TP 2RR**: 22404.99 ❌
- **TP 2.5RR**: 22456.43 ❌
- **TP 3RR**: 22507.86 ❌
- **TP 3.5RR**: 22559.29 ❌
- **TP 4RR**: 22610.72 ❌
- **TP 4.5RR**: 22662.15 ❌
- **TP 5RR**: 22713.58 ❌
- **PnL**: -102.86 points (-1.0R)
- **MFE**: 33.66 points
- **MAE**: 111.96 points

### Trade #834 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22107.46 - 22119.70
- **Entrée**: 22199.27 @ 2025-06-13 08:31:00
- **Stop Loss**: 22096.40
- **Risk**: 102.86 points
- **TP 1RR**: 22302.13 ❌
- **TP 1.5RR**: 22353.56 ❌
- **TP 2RR**: 22404.99 ❌
- **TP 2.5RR**: 22456.43 ❌
- **TP 3RR**: 22507.86 ❌
- **TP 3.5RR**: 22559.29 ❌
- **TP 4RR**: 22610.72 ❌
- **TP 4.5RR**: 22662.15 ❌
- **TP 5RR**: 22713.58 ❌
- **PnL**: -102.86 points (-1.0R)
- **MFE**: 33.66 points
- **MAE**: 111.96 points

### Trade #835 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22107.46 - 22119.70
- **Entrée**: 22199.27 @ 2025-06-13 08:31:00
- **Stop Loss**: 22096.40
- **Risk**: 102.86 points
- **TP 1RR**: 22302.13 ❌
- **TP 1.5RR**: 22353.56 ❌
- **TP 2RR**: 22404.99 ❌
- **TP 2.5RR**: 22456.43 ❌
- **TP 3RR**: 22507.86 ❌
- **TP 3.5RR**: 22559.29 ❌
- **TP 4RR**: 22610.72 ❌
- **TP 4.5RR**: 22662.15 ❌
- **TP 5RR**: 22713.58 ❌
- **PnL**: -102.86 points (-1.0R)
- **MFE**: 33.66 points
- **MAE**: 111.96 points

### Trade #836 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-13 09:00:00
- **FVG 5m**: 22117.15 - 22165.60
- **Entrée**: 22092.16 @ 2025-06-13 09:20:00
- **Stop Loss**: 22176.69
- **Risk**: 84.53 points
- **TP 1RR**: 22007.63 ❌
- **TP 1.5RR**: 21965.36 ❌
- **TP 2RR**: 21923.10 ❌
- **TP 2.5RR**: 21880.83 ❌
- **TP 3RR**: 21838.57 ❌
- **TP 3.5RR**: 21796.30 ❌
- **TP 4RR**: 21754.04 ❌
- **TP 4.5RR**: 21711.77 ❌
- **TP 5RR**: 21669.51 ❌
- **PnL**: -84.53 points (-1.0R)
- **MFE**: 40.55 points
- **MAE**: 94.36 points

### Trade #837 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-13 09:15:00
- **FVG 5m**: 22117.15 - 22165.60
- **Entrée**: 22092.16 @ 2025-06-13 09:20:00
- **Stop Loss**: 22176.69
- **Risk**: 84.53 points
- **TP 1RR**: 22007.63 ❌
- **TP 1.5RR**: 21965.36 ❌
- **TP 2RR**: 21923.10 ❌
- **TP 2.5RR**: 21880.83 ❌
- **TP 3RR**: 21838.57 ❌
- **TP 3.5RR**: 21796.30 ❌
- **TP 4RR**: 21754.04 ❌
- **TP 4.5RR**: 21711.77 ❌
- **TP 5RR**: 21669.51 ❌
- **PnL**: -84.53 points (-1.0R)
- **MFE**: 40.55 points
- **MAE**: 94.36 points

### Trade #838 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-13 12:00:00
- **FVG 5m**: 22250.53 - 22261.24
- **Entrée**: 22243.90 @ 2025-06-13 12:07:00
- **Stop Loss**: 22272.37
- **Risk**: 28.47 points
- **TP 1RR**: 22215.43 ✅
- **TP 1.5RR**: 22201.19 ✅
- **TP 2RR**: 22186.95 ✅
- **TP 2.5RR**: 22172.72 ✅
- **TP 3RR**: 22158.48 ✅
- **TP 3.5RR**: 22144.24 ✅
- **TP 4RR**: 22130.01 ✅
- **TP 4.5RR**: 22115.77 ✅
- **TP 5RR**: 22101.54 ✅
- **PnL**: 142.36 points (5.0R)
- **MFE**: 144.09 points
- **MAE**: 15.56 points

### Trade #839 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-15 17:00:00
- **FVG 5m**: 22077.62 - 22088.59
- **Entrée**: 22111.79 @ 2025-06-15 17:44:00
- **Stop Loss**: 22066.58
- **Risk**: 45.21 points
- **TP 1RR**: 22157.01 ❌
- **TP 1.5RR**: 22179.61 ❌
- **TP 2RR**: 22202.22 ❌
- **TP 2.5RR**: 22224.82 ❌
- **TP 3RR**: 22247.43 ❌
- **TP 3.5RR**: 22270.04 ❌
- **TP 4RR**: 22292.64 ❌
- **TP 4.5RR**: 22315.25 ❌
- **TP 5RR**: 22337.86 ❌
- **PnL**: -45.21 points (-1.0R)
- **MFE**: 2.30 points
- **MAE**: 46.67 points

### Trade #840 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-15 17:00:00
- **FVG 5m**: 22077.62 - 22088.59
- **Entrée**: 22111.79 @ 2025-06-15 17:44:00
- **Stop Loss**: 22066.58
- **Risk**: 45.21 points
- **TP 1RR**: 22157.01 ❌
- **TP 1.5RR**: 22179.61 ❌
- **TP 2RR**: 22202.22 ❌
- **TP 2.5RR**: 22224.82 ❌
- **TP 3RR**: 22247.43 ❌
- **TP 3.5RR**: 22270.04 ❌
- **TP 4RR**: 22292.64 ❌
- **TP 4.5RR**: 22315.25 ❌
- **TP 5RR**: 22337.86 ❌
- **PnL**: -45.21 points (-1.0R)
- **MFE**: 2.30 points
- **MAE**: 46.67 points

### Trade #841 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-16 08:45:00
- **FVG 5m**: 22262.32 - 22266.61
- **Entrée**: 22307.01 @ 2025-06-16 08:46:00
- **Stop Loss**: 22251.19
- **Risk**: 55.82 points
- **TP 1RR**: 22362.83 ✅
- **TP 1.5RR**: 22390.74 ✅
- **TP 2RR**: 22418.65 ✅
- **TP 2.5RR**: 22446.56 ❌
- **TP 3RR**: 22474.47 ❌
- **TP 3.5RR**: 22502.38 ❌
- **TP 4RR**: 22530.29 ❌
- **TP 4.5RR**: 22558.20 ❌
- **TP 5RR**: 22586.11 ❌
- **PnL**: -55.82 points (-1.0R)
- **MFE**: 135.07 points
- **MAE**: 68.42 points

### Trade #842 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-16 10:45:00
- **FVG 5m**: 22422.90 - 22426.68
- **Entrée**: 22422.64 @ 2025-06-16 10:47:00
- **Stop Loss**: 22437.90
- **Risk**: 15.25 points
- **TP 1RR**: 22407.39 ✅
- **TP 1.5RR**: 22399.76 ✅
- **TP 2RR**: 22392.14 ✅
- **TP 2.5RR**: 22384.51 ✅
- **TP 3RR**: 22376.88 ✅
- **TP 3.5RR**: 22369.26 ✅
- **TP 4RR**: 22361.63 ✅
- **TP 4.5RR**: 22354.00 ✅
- **TP 5RR**: 22346.38 ✅
- **PnL**: 76.26 points (5.0R)
- **MFE**: 79.02 points
- **MAE**: 9.09 points

### Trade #843 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 03:15:00
- **FVG 5m**: 22249.44 - 22259.29
- **Entrée**: 22262.57 @ 2025-06-17 03:16:00
- **Stop Loss**: 22238.32
- **Risk**: 24.25 points
- **TP 1RR**: 22286.83 ✅
- **TP 1.5RR**: 22298.95 ✅
- **TP 2RR**: 22311.08 ❌
- **TP 2.5RR**: 22323.21 ❌
- **TP 3RR**: 22335.33 ❌
- **TP 3.5RR**: 22347.46 ❌
- **TP 4RR**: 22359.59 ❌
- **TP 4.5RR**: 22371.71 ❌
- **TP 5RR**: 22383.84 ❌
- **PnL**: -24.25 points (-1.0R)
- **MFE**: 40.14 points
- **MAE**: 28.78 points

### Trade #844 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-17 05:30:00
- **FVG 5m**: 22257.27 - 22260.55
- **Entrée**: 22247.93 @ 2025-06-17 05:31:00
- **Stop Loss**: 22271.68
- **Risk**: 23.75 points
- **TP 1RR**: 22224.18 ✅
- **TP 1.5RR**: 22212.30 ❌
- **TP 2RR**: 22200.42 ❌
- **TP 2.5RR**: 22188.54 ❌
- **TP 3RR**: 22176.67 ❌
- **TP 3.5RR**: 22164.79 ❌
- **TP 4RR**: 22152.91 ❌
- **TP 4.5RR**: 22141.04 ❌
- **TP 5RR**: 22129.16 ❌
- **PnL**: -23.75 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 26.01 points

### Trade #845 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 05:45:00
- **FVG 5m**: 22234.04 - 22244.14
- **Entrée**: 22244.65 @ 2025-06-17 05:51:00
- **Stop Loss**: 22222.93
- **Risk**: 21.72 points
- **TP 1RR**: 22266.37 ✅
- **TP 1.5RR**: 22277.23 ✅
- **TP 2RR**: 22288.09 ✅
- **TP 2.5RR**: 22298.95 ✅
- **TP 3RR**: 22309.81 ✅
- **TP 3.5RR**: 22320.67 ✅
- **TP 4RR**: 22331.53 ✅
- **TP 4.5RR**: 22342.39 ✅
- **TP 5RR**: 22353.25 ✅
- **PnL**: 108.61 points (5.0R)
- **MFE**: 109.57 points
- **MAE**: 2.02 points

### Trade #846 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 05:45:00
- **FVG 5m**: 22234.04 - 22244.14
- **Entrée**: 22244.65 @ 2025-06-17 05:51:00
- **Stop Loss**: 22222.93
- **Risk**: 21.72 points
- **TP 1RR**: 22266.37 ✅
- **TP 1.5RR**: 22277.23 ✅
- **TP 2RR**: 22288.09 ✅
- **TP 2.5RR**: 22298.95 ✅
- **TP 3RR**: 22309.81 ✅
- **TP 3.5RR**: 22320.67 ✅
- **TP 4RR**: 22331.53 ✅
- **TP 4.5RR**: 22342.39 ✅
- **TP 5RR**: 22353.25 ✅
- **PnL**: 108.61 points (5.0R)
- **MFE**: 109.57 points
- **MAE**: 2.02 points

### Trade #847 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-17 07:30:00
- **FVG 5m**: 22273.18 - 22284.79
- **Entrée**: 22272.17 @ 2025-06-17 07:52:00
- **Stop Loss**: 22295.93
- **Risk**: 23.77 points
- **TP 1RR**: 22248.40 ❌
- **TP 1.5RR**: 22236.52 ❌
- **TP 2RR**: 22224.63 ❌
- **TP 2.5RR**: 22212.75 ❌
- **TP 3RR**: 22200.87 ❌
- **TP 3.5RR**: 22188.99 ❌
- **TP 4RR**: 22177.10 ❌
- **TP 4.5RR**: 22165.22 ❌
- **TP 5RR**: 22153.34 ❌
- **PnL**: -23.77 points (-1.0R)
- **MFE**: 20.96 points
- **MAE**: 51.25 points

### Trade #848 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 01:00:00
- **FVG 5m**: 22176.23 - 22189.61
- **Entrée**: 22205.26 @ 2025-06-18 01:01:00
- **Stop Loss**: 22165.14
- **Risk**: 40.12 points
- **TP 1RR**: 22245.38 ✅
- **TP 1.5RR**: 22265.45 ✅
- **TP 2RR**: 22285.51 ❌
- **TP 2.5RR**: 22305.57 ❌
- **TP 3RR**: 22325.63 ❌
- **TP 3.5RR**: 22345.69 ❌
- **TP 4RR**: 22365.75 ❌
- **TP 4.5RR**: 22385.81 ❌
- **TP 5RR**: 22405.88 ❌
- **PnL**: -40.12 points (-1.0R)
- **MFE**: 79.53 points
- **MAE**: 40.65 points

### Trade #849 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-18 07:15:00
- **FVG 5m**: 22224.45 - 22231.27
- **Entrée**: 22218.39 @ 2025-06-18 07:17:00
- **Stop Loss**: 22242.38
- **Risk**: 23.99 points
- **TP 1RR**: 22194.40 ✅
- **TP 1.5RR**: 22182.40 ✅
- **TP 2RR**: 22170.41 ✅
- **TP 2.5RR**: 22158.41 ✅
- **TP 3RR**: 22146.41 ✅
- **TP 3.5RR**: 22134.42 ❌
- **TP 4RR**: 22122.42 ❌
- **TP 4.5RR**: 22110.43 ❌
- **TP 5RR**: 22098.43 ❌
- **PnL**: -23.99 points (-1.0R)
- **MFE**: 74.99 points
- **MAE**: 24.49 points

### Trade #850 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 08:30:00
- **FVG 5m**: 22226.97 - 22231.27
- **Entrée**: 22235.81 @ 2025-06-18 08:52:00
- **Stop Loss**: 22215.86
- **Risk**: 19.95 points
- **TP 1RR**: 22255.76 ❌
- **TP 1.5RR**: 22265.74 ❌
- **TP 2RR**: 22275.71 ❌
- **TP 2.5RR**: 22285.69 ❌
- **TP 3RR**: 22295.66 ❌
- **TP 3.5RR**: 22305.64 ❌
- **TP 4RR**: 22315.61 ❌
- **TP 4.5RR**: 22325.59 ❌
- **TP 5RR**: 22335.56 ❌
- **PnL**: -19.95 points (-1.0R)
- **MFE**: 8.33 points
- **MAE**: 22.98 points

### Trade #851 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 08:30:00
- **FVG 5m**: 22226.97 - 22231.27
- **Entrée**: 22235.81 @ 2025-06-18 08:52:00
- **Stop Loss**: 22215.86
- **Risk**: 19.95 points
- **TP 1RR**: 22255.76 ❌
- **TP 1.5RR**: 22265.74 ❌
- **TP 2RR**: 22275.71 ❌
- **TP 2.5RR**: 22285.69 ❌
- **TP 3RR**: 22295.66 ❌
- **TP 3.5RR**: 22305.64 ❌
- **TP 4RR**: 22315.61 ❌
- **TP 4.5RR**: 22325.59 ❌
- **TP 5RR**: 22335.56 ❌
- **PnL**: -19.95 points (-1.0R)
- **MFE**: 8.33 points
- **MAE**: 22.98 points

### Trade #852 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 08:15:00
- **FVG 5m**: 21981.82 - 21990.40
- **Entrée**: 21995.20 @ 2025-06-19 08:23:00
- **Stop Loss**: 21970.83
- **Risk**: 24.37 points
- **TP 1RR**: 22019.57 ❌
- **TP 1.5RR**: 22031.76 ❌
- **TP 2RR**: 22043.95 ❌
- **TP 2.5RR**: 22056.13 ❌
- **TP 3RR**: 22068.32 ❌
- **TP 3.5RR**: 22080.50 ❌
- **TP 4RR**: 22092.69 ❌
- **TP 4.5RR**: 22104.88 ❌
- **TP 5RR**: 22117.06 ❌
- **PnL**: -24.37 points (-1.0R)
- **MFE**: 7.32 points
- **MAE**: 24.74 points

### Trade #853 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-19 08:45:00
- **FVG 5m**: 21990.91 - 21993.69
- **Entrée**: 21924.00 @ 2025-06-19 08:46:00
- **Stop Loss**: 22004.68
- **Risk**: 80.68 points
- **TP 1RR**: 21843.32 ❌
- **TP 1.5RR**: 21802.98 ❌
- **TP 2RR**: 21762.64 ❌
- **TP 2.5RR**: 21722.30 ❌
- **TP 3RR**: 21681.96 ❌
- **TP 3.5RR**: 21641.62 ❌
- **TP 4RR**: 21601.28 ❌
- **TP 4.5RR**: 21560.94 ❌
- **TP 5RR**: 21520.60 ❌
- **PnL**: -80.68 points (-1.0R)
- **MFE**: 59.33 points
- **MAE**: 103.77 points

### Trade #854 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 09:00:00
- **FVG 5m**: 21905.82 - 21927.54
- **Entrée**: 21929.56 @ 2025-06-19 09:15:00
- **Stop Loss**: 21894.87
- **Risk**: 34.69 points
- **TP 1RR**: 21964.24 ❌
- **TP 1.5RR**: 21981.59 ❌
- **TP 2RR**: 21998.93 ❌
- **TP 2.5RR**: 22016.27 ❌
- **TP 3RR**: 22033.61 ❌
- **TP 3.5RR**: 22050.96 ❌
- **TP 4RR**: 22068.30 ❌
- **TP 4.5RR**: 22085.64 ❌
- **TP 5RR**: 22102.99 ❌
- **PnL**: -34.69 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 36.61 points

### Trade #855 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 09:00:00
- **FVG 5m**: 21905.82 - 21927.54
- **Entrée**: 21929.56 @ 2025-06-19 09:15:00
- **Stop Loss**: 21894.87
- **Risk**: 34.69 points
- **TP 1RR**: 21964.24 ❌
- **TP 1.5RR**: 21981.59 ❌
- **TP 2RR**: 21998.93 ❌
- **TP 2.5RR**: 22016.27 ❌
- **TP 3RR**: 22033.61 ❌
- **TP 3.5RR**: 22050.96 ❌
- **TP 4RR**: 22068.30 ❌
- **TP 4.5RR**: 22085.64 ❌
- **TP 5RR**: 22102.99 ❌
- **PnL**: -34.69 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 36.61 points

### Trade #856 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 09:45:00
- **FVG 5m**: 21905.82 - 21927.54
- **Entrée**: 21932.08 @ 2025-06-19 09:54:00
- **Stop Loss**: 21894.87
- **Risk**: 37.21 points
- **TP 1RR**: 21969.29 ❌
- **TP 1.5RR**: 21987.90 ❌
- **TP 2RR**: 22006.50 ❌
- **TP 2.5RR**: 22025.11 ❌
- **TP 3RR**: 22043.71 ❌
- **TP 3.5RR**: 22062.32 ❌
- **TP 4RR**: 22080.92 ❌
- **TP 4.5RR**: 22099.53 ❌
- **TP 5RR**: 22118.13 ❌
- **PnL**: -37.21 points (-1.0R)
- **MFE**: 23.99 points
- **MAE**: 38.63 points

### Trade #857 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 17:00:00
- **FVG 5m**: 21924.26 - 21928.30
- **Entrée**: 22038.37 @ 2025-06-19 17:01:00
- **Stop Loss**: 21913.29
- **Risk**: 125.08 points
- **TP 1RR**: 22163.46 ✅
- **TP 1.5RR**: 22226.00 ✅
- **TP 2RR**: 22288.54 ✅
- **TP 2.5RR**: 22351.08 ❌
- **TP 3RR**: 22413.62 ❌
- **TP 3.5RR**: 22476.16 ❌
- **TP 4RR**: 22538.70 ❌
- **TP 4.5RR**: 22601.24 ❌
- **TP 5RR**: 22663.78 ❌
- **PnL**: -125.08 points (-1.0R)
- **MFE**: 311.30 points
- **MAE**: 258.03 points

### Trade #858 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 19:00:00
- **FVG 5m**: 22104.78 - 22107.55
- **Entrée**: 22108.31 @ 2025-06-19 19:01:00
- **Stop Loss**: 22093.72
- **Risk**: 14.59 points
- **TP 1RR**: 22122.90 ✅
- **TP 1.5RR**: 22130.19 ✅
- **TP 2RR**: 22137.48 ✅
- **TP 2.5RR**: 22144.78 ✅
- **TP 3RR**: 22152.07 ❌
- **TP 3.5RR**: 22159.37 ❌
- **TP 4RR**: 22166.66 ❌
- **TP 4.5RR**: 22173.95 ❌
- **TP 5RR**: 22181.25 ❌
- **PnL**: -14.59 points (-1.0R)
- **MFE**: 36.86 points
- **MAE**: 16.16 points

### Trade #859 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 03:15:00
- **FVG 5m**: 22133.05 - 22135.58
- **Entrée**: 22130.28 @ 2025-06-20 03:28:00
- **Stop Loss**: 22146.65
- **Risk**: 16.37 points
- **TP 1RR**: 22113.91 ✅
- **TP 1.5RR**: 22105.72 ✅
- **TP 2RR**: 22097.54 ✅
- **TP 2.5RR**: 22089.35 ✅
- **TP 3RR**: 22081.17 ✅
- **TP 3.5RR**: 22072.98 ❌
- **TP 4RR**: 22064.80 ❌
- **TP 4.5RR**: 22056.61 ❌
- **TP 5RR**: 22048.43 ❌
- **PnL**: -16.37 points (-1.0R)
- **MFE**: 54.79 points
- **MAE**: 16.66 points

### Trade #860 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 04:00:00
- **FVG 5m**: 22093.67 - 22099.98
- **Entrée**: 22103.77 @ 2025-06-20 04:09:00
- **Stop Loss**: 22082.62
- **Risk**: 21.15 points
- **TP 1RR**: 22124.91 ✅
- **TP 1.5RR**: 22135.48 ✅
- **TP 2RR**: 22146.06 ✅
- **TP 2.5RR**: 22156.63 ✅
- **TP 3RR**: 22167.20 ✅
- **TP 3.5RR**: 22177.78 ✅
- **TP 4RR**: 22188.35 ✅
- **TP 4.5RR**: 22198.92 ✅
- **TP 5RR**: 22209.50 ✅
- **PnL**: 105.73 points (5.0R)
- **MFE**: 117.15 points
- **MAE**: 9.34 points

### Trade #861 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 04:00:00
- **FVG 5m**: 22093.67 - 22099.98
- **Entrée**: 22103.77 @ 2025-06-20 04:09:00
- **Stop Loss**: 22082.62
- **Risk**: 21.15 points
- **TP 1RR**: 22124.91 ✅
- **TP 1.5RR**: 22135.48 ✅
- **TP 2RR**: 22146.06 ✅
- **TP 2.5RR**: 22156.63 ✅
- **TP 3RR**: 22167.20 ✅
- **TP 3.5RR**: 22177.78 ✅
- **TP 4RR**: 22188.35 ✅
- **TP 4.5RR**: 22198.92 ✅
- **TP 5RR**: 22209.50 ✅
- **PnL**: 105.73 points (5.0R)
- **MFE**: 117.15 points
- **MAE**: 9.34 points

### Trade #862 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 08:15:00
- **FVG 5m**: 22208.04 - 22210.31
- **Entrée**: 22200.72 @ 2025-06-20 09:08:00
- **Stop Loss**: 22221.42
- **Risk**: 20.70 points
- **TP 1RR**: 22180.02 ❌
- **TP 1.5RR**: 22169.67 ❌
- **TP 2RR**: 22159.32 ❌
- **TP 2.5RR**: 22148.97 ❌
- **TP 3RR**: 22138.62 ❌
- **TP 3.5RR**: 22128.27 ❌
- **TP 4RR**: 22117.92 ❌
- **TP 4.5RR**: 22107.57 ❌
- **TP 5RR**: 22097.22 ❌
- **PnL**: -20.70 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 21.46 points

### Trade #863 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 08:45:00
- **FVG 5m**: 22256.26 - 22265.86
- **Entrée**: 22255.50 @ 2025-06-20 08:55:00
- **Stop Loss**: 22276.99
- **Risk**: 21.48 points
- **TP 1RR**: 22234.02 ✅
- **TP 1.5RR**: 22223.28 ✅
- **TP 2RR**: 22212.54 ✅
- **TP 2.5RR**: 22201.79 ✅
- **TP 3RR**: 22191.05 ✅
- **TP 3.5RR**: 22180.31 ✅
- **TP 4RR**: 22169.57 ✅
- **TP 4.5RR**: 22158.82 ✅
- **TP 5RR**: 22148.08 ✅
- **PnL**: 107.42 points (5.0R)
- **MFE**: 125.23 points
- **MAE**: 7.07 points

### Trade #864 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:15:00
- **FVG 5m**: 22256.26 - 22265.86
- **Entrée**: 22198.70 @ 2025-06-20 09:16:00
- **Stop Loss**: 22276.99
- **Risk**: 78.29 points
- **TP 1RR**: 22120.41 ✅
- **TP 1.5RR**: 22081.26 ✅
- **TP 2RR**: 22042.11 ✅
- **TP 2.5RR**: 22002.97 ✅
- **TP 3RR**: 21963.82 ✅
- **TP 3.5RR**: 21924.68 ✅
- **TP 4RR**: 21885.53 ✅
- **TP 4.5RR**: 21846.38 ✅
- **TP 5RR**: 21807.24 ✅
- **PnL**: 391.46 points (5.0R)
- **MFE**: 418.35 points
- **MAE**: 22.98 points

### Trade #865 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:15:00
- **FVG 5m**: 22256.26 - 22265.86
- **Entrée**: 22198.70 @ 2025-06-20 09:16:00
- **Stop Loss**: 22276.99
- **Risk**: 78.29 points
- **TP 1RR**: 22120.41 ✅
- **TP 1.5RR**: 22081.26 ✅
- **TP 2RR**: 22042.11 ✅
- **TP 2.5RR**: 22002.97 ✅
- **TP 3RR**: 21963.82 ✅
- **TP 3.5RR**: 21924.68 ✅
- **TP 4RR**: 21885.53 ✅
- **TP 4.5RR**: 21846.38 ✅
- **TP 5RR**: 21807.24 ✅
- **PnL**: 391.46 points (5.0R)
- **MFE**: 418.35 points
- **MAE**: 22.98 points

### Trade #866 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:15:00
- **FVG 5m**: 22256.26 - 22265.86
- **Entrée**: 22198.70 @ 2025-06-20 09:16:00
- **Stop Loss**: 22276.99
- **Risk**: 78.29 points
- **TP 1RR**: 22120.41 ✅
- **TP 1.5RR**: 22081.26 ✅
- **TP 2RR**: 22042.11 ✅
- **TP 2.5RR**: 22002.97 ✅
- **TP 3RR**: 21963.82 ✅
- **TP 3.5RR**: 21924.68 ✅
- **TP 4RR**: 21885.53 ✅
- **TP 4.5RR**: 21846.38 ✅
- **TP 5RR**: 21807.24 ✅
- **PnL**: 391.46 points (5.0R)
- **MFE**: 418.35 points
- **MAE**: 22.98 points

### Trade #867 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:45:00
- **FVG 5m**: 22256.26 - 22265.86
- **Entrée**: 22079.78 @ 2025-06-20 09:46:00
- **Stop Loss**: 22276.99
- **Risk**: 197.21 points
- **TP 1RR**: 21882.57 ✅
- **TP 1.5RR**: 21783.97 ✅
- **TP 2RR**: 21685.37 ❌
- **TP 2.5RR**: 21586.76 ❌
- **TP 3RR**: 21488.16 ❌
- **TP 3.5RR**: 21389.55 ❌
- **TP 4RR**: 21290.95 ❌
- **TP 4.5RR**: 21192.35 ❌
- **TP 5RR**: 21093.74 ❌
- **PnL**: -197.21 points (-1.0R)
- **MFE**: 299.44 points
- **MAE**: 200.21 points

### Trade #868 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 10:00:00
- **FVG 5m**: 22069.18 - 22083.32
- **Entrée**: 22087.86 @ 2025-06-20 10:19:00
- **Stop Loss**: 22058.14
- **Risk**: 29.72 points
- **TP 1RR**: 22117.58 ✅
- **TP 1.5RR**: 22132.44 ✅
- **TP 2RR**: 22147.30 ❌
- **TP 2.5RR**: 22162.15 ❌
- **TP 3RR**: 22177.01 ❌
- **TP 3.5RR**: 22191.87 ❌
- **TP 4RR**: 22206.73 ❌
- **TP 4.5RR**: 22221.59 ❌
- **TP 5RR**: 22236.45 ❌
- **PnL**: -29.72 points (-1.0R)
- **MFE**: 51.25 points
- **MAE**: 31.31 points

### Trade #869 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 11:15:00
- **FVG 5m**: 22081.04 - 22112.60
- **Entrée**: 22116.14 @ 2025-06-20 11:57:00
- **Stop Loss**: 22070.00
- **Risk**: 46.13 points
- **TP 1RR**: 22162.27 ❌
- **TP 1.5RR**: 22185.34 ❌
- **TP 2RR**: 22208.41 ❌
- **TP 2.5RR**: 22231.47 ❌
- **TP 3RR**: 22254.54 ❌
- **TP 3.5RR**: 22277.61 ❌
- **TP 4RR**: 22300.68 ❌
- **TP 4.5RR**: 22323.74 ❌
- **TP 5RR**: 22346.81 ❌
- **PnL**: -46.13 points (-1.0R)
- **MFE**: 5.55 points
- **MAE**: 52.52 points

### Trade #870 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 12:30:00
- **FVG 5m**: 22070.69 - 22074.98
- **Entrée**: 22076.75 @ 2025-06-20 13:07:00
- **Stop Loss**: 22059.66
- **Risk**: 17.09 points
- **TP 1RR**: 22093.85 ✅
- **TP 1.5RR**: 22102.39 ✅
- **TP 2RR**: 22110.94 ✅
- **TP 2.5RR**: 22119.49 ❌
- **TP 3RR**: 22128.04 ❌
- **TP 3.5RR**: 22136.58 ❌
- **TP 4RR**: 22145.13 ❌
- **TP 4.5RR**: 22153.68 ❌
- **TP 5RR**: 22162.22 ❌
- **PnL**: -17.09 points (-1.0R)
- **MFE**: 41.15 points
- **MAE**: 47.21 points

### Trade #871 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-22 17:15:00
- **FVG 5m**: 22049.48 - 22055.04
- **Entrée**: 21937.89 @ 2025-06-22 17:16:00
- **Stop Loss**: 22066.07
- **Risk**: 128.18 points
- **TP 1RR**: 21809.71 ❌
- **TP 1.5RR**: 21745.62 ❌
- **TP 2RR**: 21681.54 ❌
- **TP 2.5RR**: 21617.45 ❌
- **TP 3RR**: 21553.36 ❌
- **TP 3.5RR**: 21489.27 ❌
- **TP 4RR**: 21425.18 ❌
- **TP 4.5RR**: 21361.10 ❌
- **TP 5RR**: 21297.01 ❌
- **PnL**: -128.18 points (-1.0R)
- **MFE**: 22.72 points
- **MAE**: 140.38 points

### Trade #872 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 04:15:00
- **FVG 5m**: 22116.39 - 22134.32
- **Entrée**: 22114.87 @ 2025-06-23 04:30:00
- **Stop Loss**: 22145.38
- **Risk**: 30.51 points
- **TP 1RR**: 22084.37 ✅
- **TP 1.5RR**: 22069.11 ✅
- **TP 2RR**: 22053.86 ✅
- **TP 2.5RR**: 22038.61 ✅
- **TP 3RR**: 22023.35 ✅
- **TP 3.5RR**: 22008.10 ✅
- **TP 4RR**: 21992.84 ✅
- **TP 4.5RR**: 21977.59 ✅
- **TP 5RR**: 21962.34 ❌
- **PnL**: -30.51 points (-1.0R)
- **MFE**: 140.88 points
- **MAE**: 30.80 points

### Trade #873 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 04:15:00
- **FVG 5m**: 22116.39 - 22134.32
- **Entrée**: 22114.87 @ 2025-06-23 04:30:00
- **Stop Loss**: 22145.38
- **Risk**: 30.51 points
- **TP 1RR**: 22084.37 ✅
- **TP 1.5RR**: 22069.11 ✅
- **TP 2RR**: 22053.86 ✅
- **TP 2.5RR**: 22038.61 ✅
- **TP 3RR**: 22023.35 ✅
- **TP 3.5RR**: 22008.10 ✅
- **TP 4RR**: 21992.84 ✅
- **TP 4.5RR**: 21977.59 ✅
- **TP 5RR**: 21962.34 ❌
- **PnL**: -30.51 points (-1.0R)
- **MFE**: 140.88 points
- **MAE**: 30.80 points

### Trade #874 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 08:30:00
- **FVG 5m**: 22022.22 - 22026.00
- **Entrée**: 22036.86 @ 2025-06-23 08:31:00
- **Stop Loss**: 22011.20
- **Risk**: 25.65 points
- **TP 1RR**: 22062.51 ❌
- **TP 1.5RR**: 22075.34 ❌
- **TP 2RR**: 22088.17 ❌
- **TP 2.5RR**: 22101.00 ❌
- **TP 3RR**: 22113.82 ❌
- **TP 3.5RR**: 22126.65 ❌
- **TP 4RR**: 22139.48 ❌
- **TP 4.5RR**: 22152.31 ❌
- **TP 5RR**: 22165.13 ❌
- **PnL**: -25.65 points (-1.0R)
- **MFE**: 4.54 points
- **MAE**: 36.86 points

### Trade #875 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 10:45:00
- **FVG 5m**: 22145.68 - 22174.46
- **Entrée**: 22142.65 @ 2025-06-23 11:06:00
- **Stop Loss**: 22185.55
- **Risk**: 42.90 points
- **TP 1RR**: 22099.75 ✅
- **TP 1.5RR**: 22078.30 ✅
- **TP 2RR**: 22056.85 ✅
- **TP 2.5RR**: 22035.40 ✅
- **TP 3RR**: 22013.95 ✅
- **TP 3.5RR**: 21992.50 ✅
- **TP 4RR**: 21971.05 ✅
- **TP 4.5RR**: 21949.60 ❌
- **TP 5RR**: 21928.15 ❌
- **PnL**: -42.90 points (-1.0R)
- **MFE**: 189.10 points
- **MAE**: 45.95 points

### Trade #876 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 11:30:00
- **FVG 5m**: 22107.30 - 22124.97
- **Entrée**: 22128.51 @ 2025-06-23 12:09:00
- **Stop Loss**: 22096.25
- **Risk**: 32.26 points
- **TP 1RR**: 22160.77 ✅
- **TP 1.5RR**: 22176.90 ✅
- **TP 2RR**: 22193.03 ✅
- **TP 2.5RR**: 22209.16 ✅
- **TP 3RR**: 22225.29 ✅
- **TP 3.5RR**: 22241.42 ✅
- **TP 4RR**: 22257.55 ✅
- **TP 4.5RR**: 22273.69 ✅
- **TP 5RR**: 22289.82 ✅
- **PnL**: 161.31 points (5.0R)
- **MFE**: 168.91 points
- **MAE**: 7.07 points

### Trade #877 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 11:30:00
- **FVG 5m**: 22107.30 - 22124.97
- **Entrée**: 22128.51 @ 2025-06-23 12:09:00
- **Stop Loss**: 22096.25
- **Risk**: 32.26 points
- **TP 1RR**: 22160.77 ✅
- **TP 1.5RR**: 22176.90 ✅
- **TP 2RR**: 22193.03 ✅
- **TP 2.5RR**: 22209.16 ✅
- **TP 3RR**: 22225.29 ✅
- **TP 3.5RR**: 22241.42 ✅
- **TP 4RR**: 22257.55 ✅
- **TP 4.5RR**: 22273.69 ✅
- **TP 5RR**: 22289.82 ✅
- **PnL**: 161.31 points (5.0R)
- **MFE**: 168.91 points
- **MAE**: 7.07 points

### Trade #878 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 17:30:00
- **FVG 5m**: 22400.17 - 22416.08
- **Entrée**: 22398.66 @ 2025-06-23 17:45:00
- **Stop Loss**: 22427.29
- **Risk**: 28.63 points
- **TP 1RR**: 22370.03 ❌
- **TP 1.5RR**: 22355.71 ❌
- **TP 2RR**: 22341.40 ❌
- **TP 2.5RR**: 22327.09 ❌
- **TP 3RR**: 22312.77 ❌
- **TP 3.5RR**: 22298.46 ❌
- **TP 4RR**: 22284.14 ❌
- **TP 4.5RR**: 22269.83 ❌
- **TP 5RR**: 22255.51 ❌
- **PnL**: -28.63 points (-1.0R)
- **MFE**: 7.83 points
- **MAE**: 37.62 points

### Trade #879 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 21:00:00
- **FVG 5m**: 22472.38 - 22480.71
- **Entrée**: 22469.10 @ 2025-06-23 21:05:00
- **Stop Loss**: 22491.95
- **Risk**: 22.85 points
- **TP 1RR**: 22446.24 ✅
- **TP 1.5RR**: 22434.82 ❌
- **TP 2RR**: 22423.39 ❌
- **TP 2.5RR**: 22411.96 ❌
- **TP 3RR**: 22400.54 ❌
- **TP 3.5RR**: 22389.11 ❌
- **TP 4RR**: 22377.68 ❌
- **TP 4.5RR**: 22366.25 ❌
- **TP 5RR**: 22354.83 ❌
- **PnL**: -22.85 points (-1.0R)
- **MFE**: 33.83 points
- **MAE**: 32.57 points

### Trade #880 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-24 02:15:00
- **FVG 5m**: 22557.21 - 22575.14
- **Entrée**: 22546.10 @ 2025-06-24 02:29:00
- **Stop Loss**: 22586.43
- **Risk**: 40.32 points
- **TP 1RR**: 22505.78 ✅
- **TP 1.5RR**: 22485.62 ✅
- **TP 2RR**: 22465.46 ❌
- **TP 2.5RR**: 22445.30 ❌
- **TP 3RR**: 22425.14 ❌
- **TP 3.5RR**: 22404.98 ❌
- **TP 4RR**: 22384.81 ❌
- **TP 4.5RR**: 22364.65 ❌
- **TP 5RR**: 22344.49 ❌
- **PnL**: -40.32 points (-1.0R)
- **MFE**: 73.98 points
- **MAE**: 46.46 points

### Trade #881 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-24 05:00:00
- **FVG 5m**: 22545.60 - 22554.44
- **Entrée**: 22543.07 @ 2025-06-24 05:01:00
- **Stop Loss**: 22565.71
- **Risk**: 22.64 points
- **TP 1RR**: 22520.44 ✅
- **TP 1.5RR**: 22509.12 ✅
- **TP 2RR**: 22497.80 ✅
- **TP 2.5RR**: 22486.48 ✅
- **TP 3RR**: 22475.16 ✅
- **TP 3.5RR**: 22463.84 ❌
- **TP 4RR**: 22452.52 ❌
- **TP 4.5RR**: 22441.20 ❌
- **TP 5RR**: 22429.88 ❌
- **PnL**: -22.64 points (-1.0R)
- **MFE**: 70.95 points
- **MAE**: 26.51 points

### Trade #882 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-24 06:00:00
- **FVG 5m**: 22545.60 - 22554.44
- **Entrée**: 22516.56 @ 2025-06-24 06:01:00
- **Stop Loss**: 22565.71
- **Risk**: 49.15 points
- **TP 1RR**: 22467.42 ❌
- **TP 1.5RR**: 22442.84 ❌
- **TP 2RR**: 22418.27 ❌
- **TP 2.5RR**: 22393.69 ❌
- **TP 3RR**: 22369.12 ❌
- **TP 3.5RR**: 22344.54 ❌
- **TP 4RR**: 22319.97 ❌
- **TP 4.5RR**: 22295.40 ❌
- **TP 5RR**: 22270.82 ❌
- **PnL**: -49.15 points (-1.0R)
- **MFE**: 44.44 points
- **MAE**: 53.02 points

### Trade #883 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-25 04:15:00
- **FVG 5m**: 22646.08 - 22649.87
- **Entrée**: 22645.83 @ 2025-06-25 04:56:00
- **Stop Loss**: 22661.20
- **Risk**: 15.36 points
- **TP 1RR**: 22630.47 ❌
- **TP 1.5RR**: 22622.78 ❌
- **TP 2RR**: 22615.10 ❌
- **TP 2.5RR**: 22607.42 ❌
- **TP 3RR**: 22599.74 ❌
- **TP 3.5RR**: 22592.06 ❌
- **TP 4RR**: 22584.37 ❌
- **TP 4.5RR**: 22576.69 ❌
- **TP 5RR**: 22569.01 ❌
- **PnL**: -15.36 points (-1.0R)
- **MFE**: 10.35 points
- **MAE**: 18.94 points

### Trade #884 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-25 04:15:00
- **FVG 5m**: 22646.08 - 22649.87
- **Entrée**: 22645.83 @ 2025-06-25 04:56:00
- **Stop Loss**: 22661.20
- **Risk**: 15.36 points
- **TP 1RR**: 22630.47 ❌
- **TP 1.5RR**: 22622.78 ❌
- **TP 2RR**: 22615.10 ❌
- **TP 2.5RR**: 22607.42 ❌
- **TP 3RR**: 22599.74 ❌
- **TP 3.5RR**: 22592.06 ❌
- **TP 4RR**: 22584.37 ❌
- **TP 4.5RR**: 22576.69 ❌
- **TP 5RR**: 22569.01 ❌
- **PnL**: -15.36 points (-1.0R)
- **MFE**: 10.35 points
- **MAE**: 18.94 points

### Trade #885 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-25 10:30:00
- **FVG 5m**: 22729.65 - 22739.75
- **Entrée**: 22677.14 @ 2025-06-25 10:31:00
- **Stop Loss**: 22751.12
- **Risk**: 73.98 points
- **TP 1RR**: 22603.15 ❌
- **TP 1.5RR**: 22566.16 ❌
- **TP 2RR**: 22529.17 ❌
- **TP 2.5RR**: 22492.18 ❌
- **TP 3RR**: 22455.19 ❌
- **TP 3.5RR**: 22418.20 ❌
- **TP 4RR**: 22381.20 ❌
- **TP 4.5RR**: 22344.21 ❌
- **TP 5RR**: 22307.22 ❌
- **PnL**: -73.98 points (-1.0R)
- **MFE**: 66.91 points
- **MAE**: 79.02 points

### Trade #886 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-26 08:30:00
- **FVG 5m**: 22762.22 - 22767.78
- **Entrée**: 22761.72 @ 2025-06-26 08:32:00
- **Stop Loss**: 22779.16
- **Risk**: 17.44 points
- **TP 1RR**: 22744.27 ✅
- **TP 1.5RR**: 22735.55 ✅
- **TP 2RR**: 22726.83 ✅
- **TP 2.5RR**: 22718.11 ✅
- **TP 3RR**: 22709.39 ✅
- **TP 3.5RR**: 22700.67 ✅
- **TP 4RR**: 22691.94 ❌
- **TP 4.5RR**: 22683.22 ❌
- **TP 5RR**: 22674.50 ❌
- **PnL**: -17.44 points (-1.0R)
- **MFE**: 63.12 points
- **MAE**: 30.80 points

### Trade #887 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 12:00:00
- **FVG 5m**: 22805.65 - 22823.32
- **Entrée**: 22834.43 @ 2025-06-26 12:01:00
- **Stop Loss**: 22794.25
- **Risk**: 40.19 points
- **TP 1RR**: 22874.62 ✅
- **TP 1.5RR**: 22894.71 ✅
- **TP 2RR**: 22914.80 ✅
- **TP 2.5RR**: 22934.89 ✅
- **TP 3RR**: 22954.99 ✅
- **TP 3.5RR**: 22975.08 ✅
- **TP 4RR**: 22995.17 ✅
- **TP 4.5RR**: 23015.26 ✅
- **TP 5RR**: 23035.36 ✅
- **PnL**: 200.93 points (5.0R)
- **MFE**: 207.03 points
- **MAE**: 4.29 points

### Trade #888 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 12:00:00
- **FVG 5m**: 22805.65 - 22823.32
- **Entrée**: 22834.43 @ 2025-06-26 12:01:00
- **Stop Loss**: 22794.25
- **Risk**: 40.19 points
- **TP 1RR**: 22874.62 ✅
- **TP 1.5RR**: 22894.71 ✅
- **TP 2RR**: 22914.80 ✅
- **TP 2.5RR**: 22934.89 ✅
- **TP 3RR**: 22954.99 ✅
- **TP 3.5RR**: 22975.08 ✅
- **TP 4RR**: 22995.17 ✅
- **TP 4.5RR**: 23015.26 ✅
- **TP 5RR**: 23035.36 ✅
- **PnL**: 200.93 points (5.0R)
- **MFE**: 207.03 points
- **MAE**: 4.29 points

### Trade #889 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-26 18:00:00
- **FVG 5m**: 22898.06 - 22905.12
- **Entrée**: 22895.78 @ 2025-06-26 18:15:00
- **Stop Loss**: 22916.58
- **Risk**: 20.79 points
- **TP 1RR**: 22874.99 ❌
- **TP 1.5RR**: 22864.59 ❌
- **TP 2RR**: 22854.19 ❌
- **TP 2.5RR**: 22843.80 ❌
- **TP 3RR**: 22833.40 ❌
- **TP 3.5RR**: 22823.00 ❌
- **TP 4RR**: 22812.61 ❌
- **TP 4.5RR**: 22802.21 ❌
- **TP 5RR**: 22791.81 ❌
- **PnL**: -20.79 points (-1.0R)
- **MFE**: 1.01 points
- **MAE**: 20.96 points

### Trade #890 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:00:00
- **FVG 5m**: 22961.93 - 22970.52
- **Entrée**: 22957.13 @ 2025-06-27 07:42:00
- **Stop Loss**: 22982.00
- **Risk**: 24.87 points
- **TP 1RR**: 22932.27 ✅
- **TP 1.5RR**: 22919.83 ✅
- **TP 2RR**: 22907.40 ❌
- **TP 2.5RR**: 22894.97 ❌
- **TP 3RR**: 22882.54 ❌
- **TP 3.5RR**: 22870.10 ❌
- **TP 4RR**: 22857.67 ❌
- **TP 4.5RR**: 22845.24 ❌
- **TP 5RR**: 22832.80 ❌
- **PnL**: -24.87 points (-1.0R)
- **MFE**: 47.21 points
- **MAE**: 26.51 points

### Trade #891 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:00:00
- **FVG 5m**: 22961.93 - 22970.52
- **Entrée**: 22957.13 @ 2025-06-27 07:42:00
- **Stop Loss**: 22982.00
- **Risk**: 24.87 points
- **TP 1RR**: 22932.27 ✅
- **TP 1.5RR**: 22919.83 ✅
- **TP 2RR**: 22907.40 ❌
- **TP 2.5RR**: 22894.97 ❌
- **TP 3RR**: 22882.54 ❌
- **TP 3.5RR**: 22870.10 ❌
- **TP 4RR**: 22857.67 ❌
- **TP 4.5RR**: 22845.24 ❌
- **TP 5RR**: 22832.80 ❌
- **PnL**: -24.87 points (-1.0R)
- **MFE**: 47.21 points
- **MAE**: 26.51 points

### Trade #892 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:30:00
- **FVG 5m**: 22984.65 - 22987.94
- **Entrée**: 22972.79 @ 2025-06-27 07:31:00
- **Stop Loss**: 22999.43
- **Risk**: 26.64 points
- **TP 1RR**: 22946.15 ✅
- **TP 1.5RR**: 22932.82 ✅
- **TP 2RR**: 22919.50 ✅
- **TP 2.5RR**: 22906.18 ❌
- **TP 3RR**: 22892.86 ❌
- **TP 3.5RR**: 22879.54 ❌
- **TP 4RR**: 22866.22 ❌
- **TP 4.5RR**: 22852.90 ❌
- **TP 5RR**: 22839.58 ❌
- **PnL**: -26.64 points (-1.0R)
- **MFE**: 62.87 points
- **MAE**: 45.45 points

### Trade #893 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:30:00
- **FVG 5m**: 22984.65 - 22987.94
- **Entrée**: 22972.79 @ 2025-06-27 07:31:00
- **Stop Loss**: 22999.43
- **Risk**: 26.64 points
- **TP 1RR**: 22946.15 ✅
- **TP 1.5RR**: 22932.82 ✅
- **TP 2RR**: 22919.50 ✅
- **TP 2.5RR**: 22906.18 ❌
- **TP 3RR**: 22892.86 ❌
- **TP 3.5RR**: 22879.54 ❌
- **TP 4RR**: 22866.22 ❌
- **TP 4.5RR**: 22852.90 ❌
- **TP 5RR**: 22839.58 ❌
- **PnL**: -26.64 points (-1.0R)
- **MFE**: 62.87 points
- **MAE**: 45.45 points

### Trade #894 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 08:00:00
- **FVG 5m**: 22984.65 - 22987.94
- **Entrée**: 22942.24 @ 2025-06-27 08:01:00
- **Stop Loss**: 22999.43
- **Risk**: 57.19 points
- **TP 1RR**: 22885.05 ❌
- **TP 1.5RR**: 22856.45 ❌
- **TP 2RR**: 22827.85 ❌
- **TP 2.5RR**: 22799.26 ❌
- **TP 3RR**: 22770.66 ❌
- **TP 3.5RR**: 22742.07 ❌
- **TP 4RR**: 22713.47 ❌
- **TP 4.5RR**: 22684.87 ❌
- **TP 5RR**: 22656.28 ❌
- **PnL**: -57.19 points (-1.0R)
- **MFE**: 32.32 points
- **MAE**: 76.00 points

### Trade #895 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 08:00:00
- **FVG 5m**: 22984.65 - 22987.94
- **Entrée**: 22942.24 @ 2025-06-27 08:01:00
- **Stop Loss**: 22999.43
- **Risk**: 57.19 points
- **TP 1RR**: 22885.05 ❌
- **TP 1.5RR**: 22856.45 ❌
- **TP 2RR**: 22827.85 ❌
- **TP 2.5RR**: 22799.26 ❌
- **TP 3RR**: 22770.66 ❌
- **TP 3.5RR**: 22742.07 ❌
- **TP 4RR**: 22713.47 ❌
- **TP 4.5RR**: 22684.87 ❌
- **TP 5RR**: 22656.28 ❌
- **PnL**: -57.19 points (-1.0R)
- **MFE**: 32.32 points
- **MAE**: 76.00 points

### Trade #896 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 08:00:00
- **FVG 5m**: 22984.65 - 22987.94
- **Entrée**: 22942.24 @ 2025-06-27 08:01:00
- **Stop Loss**: 22999.43
- **Risk**: 57.19 points
- **TP 1RR**: 22885.05 ❌
- **TP 1.5RR**: 22856.45 ❌
- **TP 2RR**: 22827.85 ❌
- **TP 2.5RR**: 22799.26 ❌
- **TP 3RR**: 22770.66 ❌
- **TP 3.5RR**: 22742.07 ❌
- **TP 4RR**: 22713.47 ❌
- **TP 4.5RR**: 22684.87 ❌
- **TP 5RR**: 22656.28 ❌
- **PnL**: -57.19 points (-1.0R)
- **MFE**: 32.32 points
- **MAE**: 76.00 points

### Trade #897 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 08:30:00
- **FVG 5m**: 22943.25 - 22952.84
- **Entrée**: 22958.40 @ 2025-06-27 08:37:00
- **Stop Loss**: 22931.78
- **Risk**: 26.62 points
- **TP 1RR**: 22985.02 ✅
- **TP 1.5RR**: 22998.33 ✅
- **TP 2RR**: 23011.64 ✅
- **TP 2.5RR**: 23024.95 ✅
- **TP 3RR**: 23038.26 ✅
- **TP 3.5RR**: 23051.57 ❌
- **TP 4RR**: 23064.88 ❌
- **TP 4.5RR**: 23078.19 ❌
- **TP 5RR**: 23091.50 ❌
- **PnL**: -26.62 points (-1.0R)
- **MFE**: 93.16 points
- **MAE**: 29.54 points

### Trade #898 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 08:30:00
- **FVG 5m**: 22943.25 - 22952.84
- **Entrée**: 22958.40 @ 2025-06-27 08:37:00
- **Stop Loss**: 22931.78
- **Risk**: 26.62 points
- **TP 1RR**: 22985.02 ✅
- **TP 1.5RR**: 22998.33 ✅
- **TP 2RR**: 23011.64 ✅
- **TP 2.5RR**: 23024.95 ✅
- **TP 3RR**: 23038.26 ✅
- **TP 3.5RR**: 23051.57 ❌
- **TP 4RR**: 23064.88 ❌
- **TP 4.5RR**: 23078.19 ❌
- **TP 5RR**: 23091.50 ❌
- **PnL**: -26.62 points (-1.0R)
- **MFE**: 93.16 points
- **MAE**: 29.54 points

### Trade #899 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 09:15:00
- **FVG 5m**: 22995.51 - 23018.49
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23030.00
- **Risk**: 38.52 points
- **TP 1RR**: 22952.95 ❌
- **TP 1.5RR**: 22933.69 ❌
- **TP 2RR**: 22914.42 ❌
- **TP 2.5RR**: 22895.16 ❌
- **TP 3RR**: 22875.90 ❌
- **TP 3.5RR**: 22856.64 ❌
- **TP 4RR**: 22837.37 ❌
- **TP 4.5RR**: 22818.11 ❌
- **TP 5RR**: 22798.85 ❌
- **PnL**: -38.52 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 40.40 points

### Trade #900 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 09:15:00
- **FVG 5m**: 22995.51 - 23018.49
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23030.00
- **Risk**: 38.52 points
- **TP 1RR**: 22952.95 ❌
- **TP 1.5RR**: 22933.69 ❌
- **TP 2RR**: 22914.42 ❌
- **TP 2.5RR**: 22895.16 ❌
- **TP 3RR**: 22875.90 ❌
- **TP 3.5RR**: 22856.64 ❌
- **TP 4RR**: 22837.37 ❌
- **TP 4.5RR**: 22818.11 ❌
- **TP 5RR**: 22798.85 ❌
- **PnL**: -38.52 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 40.40 points

### Trade #901 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 09:15:00
- **FVG 5m**: 22995.51 - 23018.49
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23030.00
- **Risk**: 38.52 points
- **TP 1RR**: 22952.95 ❌
- **TP 1.5RR**: 22933.69 ❌
- **TP 2RR**: 22914.42 ❌
- **TP 2.5RR**: 22895.16 ❌
- **TP 3RR**: 22875.90 ❌
- **TP 3.5RR**: 22856.64 ❌
- **TP 4RR**: 22837.37 ❌
- **TP 4.5RR**: 22818.11 ❌
- **TP 5RR**: 22798.85 ❌
- **PnL**: -38.52 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 40.40 points

### Trade #902 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:00:00
- **FVG 5m**: 22842.26 - 22857.91
- **Entrée**: 22863.47 @ 2025-06-27 14:04:00
- **Stop Loss**: 22830.84
- **Risk**: 32.63 points
- **TP 1RR**: 22896.10 ✅
- **TP 1.5RR**: 22912.41 ✅
- **TP 2RR**: 22928.72 ✅
- **TP 2.5RR**: 22945.04 ✅
- **TP 3RR**: 22961.35 ✅
- **TP 3.5RR**: 22977.67 ✅
- **TP 4RR**: 22993.98 ✅
- **TP 4.5RR**: 23010.30 ✅
- **TP 5RR**: 23026.61 ✅
- **PnL**: 163.15 points (5.0R)
- **MFE**: 169.16 points
- **MAE**: 14.90 points

### Trade #903 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:00:00
- **FVG 5m**: 22842.26 - 22857.91
- **Entrée**: 22863.47 @ 2025-06-27 14:04:00
- **Stop Loss**: 22830.84
- **Risk**: 32.63 points
- **TP 1RR**: 22896.10 ✅
- **TP 1.5RR**: 22912.41 ✅
- **TP 2RR**: 22928.72 ✅
- **TP 2.5RR**: 22945.04 ✅
- **TP 3RR**: 22961.35 ✅
- **TP 3.5RR**: 22977.67 ✅
- **TP 4RR**: 22993.98 ✅
- **TP 4.5RR**: 23010.30 ✅
- **TP 5RR**: 23026.61 ✅
- **PnL**: 163.15 points (5.0R)
- **MFE**: 169.16 points
- **MAE**: 14.90 points

### Trade #904 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:30:00
- **FVG 5m**: 22842.26 - 22857.91
- **Entrée**: 22906.39 @ 2025-06-27 14:31:00
- **Stop Loss**: 22830.84
- **Risk**: 75.55 points
- **TP 1RR**: 22981.94 ✅
- **TP 1.5RR**: 23019.71 ✅
- **TP 2RR**: 23057.49 ✅
- **TP 2.5RR**: 23095.26 ✅
- **TP 3RR**: 23133.04 ✅
- **TP 3.5RR**: 23170.81 ❌
- **TP 4RR**: 23208.59 ❌
- **TP 4.5RR**: 23246.36 ❌
- **TP 5RR**: 23284.14 ❌
- **PnL**: -75.55 points (-1.0R)
- **MFE**: 255.51 points
- **MAE**: 81.80 points

### Trade #905 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:30:00
- **FVG 5m**: 22842.26 - 22857.91
- **Entrée**: 22906.39 @ 2025-06-27 14:31:00
- **Stop Loss**: 22830.84
- **Risk**: 75.55 points
- **TP 1RR**: 22981.94 ✅
- **TP 1.5RR**: 23019.71 ✅
- **TP 2RR**: 23057.49 ✅
- **TP 2.5RR**: 23095.26 ✅
- **TP 3RR**: 23133.04 ✅
- **TP 3.5RR**: 23170.81 ❌
- **TP 4RR**: 23208.59 ❌
- **TP 4.5RR**: 23246.36 ❌
- **TP 5RR**: 23284.14 ❌
- **PnL**: -75.55 points (-1.0R)
- **MFE**: 255.51 points
- **MAE**: 81.80 points

### Trade #906 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 01:30:00
- **FVG 5m**: 23113.16 - 23118.97
- **Entrée**: 23112.41 @ 2025-06-30 01:38:00
- **Stop Loss**: 23130.53
- **Risk**: 18.12 points
- **TP 1RR**: 23094.28 ✅
- **TP 1.5RR**: 23085.22 ✅
- **TP 2RR**: 23076.16 ✅
- **TP 2.5RR**: 23067.10 ❌
- **TP 3RR**: 23058.04 ❌
- **TP 3.5RR**: 23048.97 ❌
- **TP 4RR**: 23039.91 ❌
- **TP 4.5RR**: 23030.85 ❌
- **TP 5RR**: 23021.79 ❌
- **PnL**: -18.12 points (-1.0R)
- **MFE**: 36.86 points
- **MAE**: 18.18 points

### Trade #907 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 08:30:00
- **FVG 5m**: 23120.99 - 23124.27
- **Entrée**: 23074.54 @ 2025-06-30 08:31:00
- **Stop Loss**: 23135.84
- **Risk**: 61.30 points
- **TP 1RR**: 23013.24 ✅
- **TP 1.5RR**: 22982.59 ❌
- **TP 2RR**: 22951.94 ❌
- **TP 2.5RR**: 22921.29 ❌
- **TP 3RR**: 22890.64 ❌
- **TP 3.5RR**: 22859.99 ❌
- **TP 4RR**: 22829.34 ❌
- **TP 4.5RR**: 22798.69 ❌
- **TP 5RR**: 22768.04 ❌
- **PnL**: -61.30 points (-1.0R)
- **MFE**: 67.92 points
- **MAE**: 62.11 points

### Trade #908 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 11:30:00
- **FVG 5m**: 23071.51 - 23079.59
- **Entrée**: 23080.34 @ 2025-06-30 11:35:00
- **Stop Loss**: 23059.97
- **Risk**: 20.37 points
- **TP 1RR**: 23100.72 ❌
- **TP 1.5RR**: 23110.90 ❌
- **TP 2RR**: 23121.09 ❌
- **TP 2.5RR**: 23131.27 ❌
- **TP 3RR**: 23141.46 ❌
- **TP 3.5RR**: 23151.65 ❌
- **TP 4RR**: 23161.83 ❌
- **TP 4.5RR**: 23172.02 ❌
- **TP 5RR**: 23182.20 ❌
- **PnL**: -20.37 points (-1.0R)
- **MFE**: 12.62 points
- **MAE**: 20.70 points

### Trade #909 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 13:30:00
- **FVG 5m**: 23075.80 - 23079.59
- **Entrée**: 23082.11 @ 2025-06-30 14:00:00
- **Stop Loss**: 23064.26
- **Risk**: 17.85 points
- **TP 1RR**: 23099.96 ✅
- **TP 1.5RR**: 23108.88 ✅
- **TP 2RR**: 23117.81 ✅
- **TP 2.5RR**: 23126.73 ✅
- **TP 3RR**: 23135.66 ✅
- **TP 3.5RR**: 23144.58 ✅
- **TP 4RR**: 23153.51 ✅
- **TP 4.5RR**: 23162.43 ❌
- **TP 5RR**: 23171.36 ❌
- **PnL**: -17.85 points (-1.0R)
- **MFE**: 79.78 points
- **MAE**: 18.18 points

### Trade #910 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 14:00:00
- **FVG 5m**: 23034.64 - 23043.23
- **Entrée**: 23081.10 @ 2025-06-30 14:01:00
- **Stop Loss**: 23023.13
- **Risk**: 57.97 points
- **TP 1RR**: 23139.07 ✅
- **TP 1.5RR**: 23168.06 ❌
- **TP 2RR**: 23197.05 ❌
- **TP 2.5RR**: 23226.03 ❌
- **TP 3RR**: 23255.02 ❌
- **TP 3.5RR**: 23284.01 ❌
- **TP 4RR**: 23312.99 ❌
- **TP 4.5RR**: 23341.98 ❌
- **TP 5RR**: 23370.96 ❌
- **PnL**: -57.97 points (-1.0R)
- **MFE**: 80.79 points
- **MAE**: 58.32 points

### Trade #911 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 14:45:00
- **FVG 5m**: 23092.97 - 23101.30
- **Entrée**: 23080.85 @ 2025-06-30 15:13:00
- **Stop Loss**: 23112.85
- **Risk**: 32.00 points
- **TP 1RR**: 23048.85 ❌
- **TP 1.5RR**: 23032.85 ❌
- **TP 2RR**: 23016.85 ❌
- **TP 2.5RR**: 23000.84 ❌
- **TP 3RR**: 22984.84 ❌
- **TP 3.5RR**: 22968.84 ❌
- **TP 4RR**: 22952.84 ❌
- **TP 4.5RR**: 22936.84 ❌
- **TP 5RR**: 22920.84 ❌
- **PnL**: -32.00 points (-1.0R)
- **MFE**: 2.02 points
- **MAE**: 32.57 points

### Trade #912 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 14:45:00
- **FVG 5m**: 23092.97 - 23101.30
- **Entrée**: 23080.85 @ 2025-06-30 15:13:00
- **Stop Loss**: 23112.85
- **Risk**: 32.00 points
- **TP 1RR**: 23048.85 ❌
- **TP 1.5RR**: 23032.85 ❌
- **TP 2RR**: 23016.85 ❌
- **TP 2.5RR**: 23000.84 ❌
- **TP 3RR**: 22984.84 ❌
- **TP 3.5RR**: 22968.84 ❌
- **TP 4RR**: 22952.84 ❌
- **TP 4.5RR**: 22936.84 ❌
- **TP 5RR**: 22920.84 ❌
- **PnL**: -32.00 points (-1.0R)
- **MFE**: 2.02 points
- **MAE**: 32.57 points

### Trade #913 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 15:00:00
- **FVG 5m**: 23092.97 - 23101.30
- **Entrée**: 23080.85 @ 2025-06-30 15:13:00
- **Stop Loss**: 23112.85
- **Risk**: 32.00 points
- **TP 1RR**: 23048.85 ❌
- **TP 1.5RR**: 23032.85 ❌
- **TP 2RR**: 23016.85 ❌
- **TP 2.5RR**: 23000.84 ❌
- **TP 3RR**: 22984.84 ❌
- **TP 3.5RR**: 22968.84 ❌
- **TP 4RR**: 22952.84 ❌
- **TP 4.5RR**: 22936.84 ❌
- **TP 5RR**: 22920.84 ❌
- **PnL**: -32.00 points (-1.0R)
- **MFE**: 2.02 points
- **MAE**: 32.57 points

### Trade #914 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 03:15:00
- **FVG 5m**: 23072.01 - 23077.57
- **Entrée**: 23078.58 @ 2025-07-01 03:30:00
- **Stop Loss**: 23060.48
- **Risk**: 18.10 points
- **TP 1RR**: 23096.68 ❌
- **TP 1.5RR**: 23105.73 ❌
- **TP 2RR**: 23114.78 ❌
- **TP 2.5RR**: 23123.83 ❌
- **TP 3RR**: 23132.88 ❌
- **TP 3.5RR**: 23141.93 ❌
- **TP 4RR**: 23150.98 ❌
- **TP 4.5RR**: 23160.03 ❌
- **TP 5RR**: 23169.08 ❌
- **PnL**: -18.10 points (-1.0R)
- **MFE**: 6.06 points
- **MAE**: 18.68 points

### Trade #915 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 04:45:00
- **FVG 5m**: 23057.37 - 23060.40
- **Entrée**: 23060.90 @ 2025-07-01 05:01:00
- **Stop Loss**: 23045.84
- **Risk**: 15.06 points
- **TP 1RR**: 23075.97 ❌
- **TP 1.5RR**: 23083.50 ❌
- **TP 2RR**: 23091.03 ❌
- **TP 2.5RR**: 23098.56 ❌
- **TP 3RR**: 23106.09 ❌
- **TP 3.5RR**: 23113.62 ❌
- **TP 4RR**: 23121.16 ❌
- **TP 4.5RR**: 23128.69 ❌
- **TP 5RR**: 23136.22 ❌
- **PnL**: -15.06 points (-1.0R)
- **MFE**: 13.89 points
- **MAE**: 18.68 points

### Trade #916 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 08:00:00
- **FVG 5m**: 23001.32 - 23017.22
- **Entrée**: 23022.78 @ 2025-07-01 08:01:00
- **Stop Loss**: 22989.82
- **Risk**: 32.96 points
- **TP 1RR**: 23055.74 ✅
- **TP 1.5RR**: 23072.22 ✅
- **TP 2RR**: 23088.70 ❌
- **TP 2.5RR**: 23105.18 ❌
- **TP 3RR**: 23121.66 ❌
- **TP 3.5RR**: 23138.14 ❌
- **TP 4RR**: 23154.62 ❌
- **TP 4.5RR**: 23171.10 ❌
- **TP 5RR**: 23187.58 ❌
- **PnL**: -32.96 points (-1.0R)
- **MFE**: 51.76 points
- **MAE**: 39.89 points

### Trade #917 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 09:00:00
- **FVG 5m**: 23027.32 - 23034.14
- **Entrée**: 23038.18 @ 2025-07-01 09:01:00
- **Stop Loss**: 23015.81
- **Risk**: 22.37 points
- **TP 1RR**: 23060.55 ❌
- **TP 1.5RR**: 23071.73 ❌
- **TP 2RR**: 23082.92 ❌
- **TP 2.5RR**: 23094.10 ❌
- **TP 3RR**: 23105.29 ❌
- **TP 3.5RR**: 23116.47 ❌
- **TP 4RR**: 23127.66 ❌
- **TP 4.5RR**: 23138.84 ❌
- **TP 5RR**: 23150.03 ❌
- **PnL**: -22.37 points (-1.0R)
- **MFE**: 7.32 points
- **MAE**: 24.74 points

### Trade #918 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 23:15:00
- **FVG 5m**: 22963.70 - 22967.23
- **Entrée**: 22969.51 @ 2025-07-01 23:16:00
- **Stop Loss**: 22952.22
- **Risk**: 17.29 points
- **TP 1RR**: 22986.79 ✅
- **TP 1.5RR**: 22995.44 ✅
- **TP 2RR**: 23004.08 ✅
- **TP 2.5RR**: 23012.73 ❌
- **TP 3RR**: 23021.37 ❌
- **TP 3.5RR**: 23030.02 ❌
- **TP 4RR**: 23038.66 ❌
- **TP 4.5RR**: 23047.31 ❌
- **TP 5RR**: 23055.95 ❌
- **PnL**: -17.29 points (-1.0R)
- **MFE**: 37.37 points
- **MAE**: 19.44 points

### Trade #919 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 08:15:00
- **FVG 5m**: 22886.69 - 22910.17
- **Entrée**: 22920.78 @ 2025-07-02 08:36:00
- **Stop Loss**: 22875.25
- **Risk**: 45.53 points
- **TP 1RR**: 22966.31 ✅
- **TP 1.5RR**: 22989.07 ✅
- **TP 2RR**: 23011.83 ✅
- **TP 2.5RR**: 23034.60 ✅
- **TP 3RR**: 23057.36 ✅
- **TP 3.5RR**: 23080.12 ✅
- **TP 4RR**: 23102.89 ✅
- **TP 4.5RR**: 23125.65 ✅
- **TP 5RR**: 23148.42 ✅
- **PnL**: 227.64 points (5.0R)
- **MFE**: 234.30 points
- **MAE**: 17.17 points

### Trade #920 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 17:00:00
- **FVG 5m**: 23070.75 - 23074.03
- **Entrée**: 23067.97 @ 2025-07-02 17:07:00
- **Stop Loss**: 23085.57
- **Risk**: 17.60 points
- **TP 1RR**: 23050.38 ❌
- **TP 1.5RR**: 23041.58 ❌
- **TP 2RR**: 23032.78 ❌
- **TP 2.5RR**: 23023.98 ❌
- **TP 3RR**: 23015.18 ❌
- **TP 3.5RR**: 23006.38 ❌
- **TP 4RR**: 22997.59 ❌
- **TP 4.5RR**: 22988.79 ❌
- **TP 5RR**: 22979.99 ❌
- **PnL**: -17.60 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 18.43 points

### Trade #921 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 17:00:00
- **FVG 5m**: 23070.75 - 23074.03
- **Entrée**: 23067.97 @ 2025-07-02 17:07:00
- **Stop Loss**: 23085.57
- **Risk**: 17.60 points
- **TP 1RR**: 23050.38 ❌
- **TP 1.5RR**: 23041.58 ❌
- **TP 2RR**: 23032.78 ❌
- **TP 2.5RR**: 23023.98 ❌
- **TP 3RR**: 23015.18 ❌
- **TP 3.5RR**: 23006.38 ❌
- **TP 4RR**: 22997.59 ❌
- **TP 4.5RR**: 22988.79 ❌
- **TP 5RR**: 22979.99 ❌
- **PnL**: -17.60 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 18.43 points

### Trade #922 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 17:00:00
- **FVG 5m**: 23070.75 - 23074.03
- **Entrée**: 23067.97 @ 2025-07-02 17:07:00
- **Stop Loss**: 23085.57
- **Risk**: 17.60 points
- **TP 1RR**: 23050.38 ❌
- **TP 1.5RR**: 23041.58 ❌
- **TP 2RR**: 23032.78 ❌
- **TP 2.5RR**: 23023.98 ❌
- **TP 3RR**: 23015.18 ❌
- **TP 3.5RR**: 23006.38 ❌
- **TP 4RR**: 22997.59 ❌
- **TP 4.5RR**: 22988.79 ❌
- **TP 5RR**: 22979.99 ❌
- **PnL**: -17.60 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 18.43 points

### Trade #923 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 17:00:00
- **FVG 5m**: 23070.75 - 23074.03
- **Entrée**: 23067.97 @ 2025-07-02 17:07:00
- **Stop Loss**: 23085.57
- **Risk**: 17.60 points
- **TP 1RR**: 23050.38 ❌
- **TP 1.5RR**: 23041.58 ❌
- **TP 2RR**: 23032.78 ❌
- **TP 2.5RR**: 23023.98 ❌
- **TP 3RR**: 23015.18 ❌
- **TP 3.5RR**: 23006.38 ❌
- **TP 4RR**: 22997.59 ❌
- **TP 4.5RR**: 22988.79 ❌
- **TP 5RR**: 22979.99 ❌
- **PnL**: -17.60 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 18.43 points

### Trade #924 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-03 02:45:00
- **FVG 5m**: 23113.92 - 23122.76
- **Entrée**: 23113.67 @ 2025-07-03 02:55:00
- **Stop Loss**: 23134.32
- **Risk**: 20.65 points
- **TP 1RR**: 23093.02 ✅
- **TP 1.5RR**: 23082.69 ✅
- **TP 2RR**: 23072.37 ✅
- **TP 2.5RR**: 23062.04 ✅
- **TP 3RR**: 23051.72 ❌
- **TP 3.5RR**: 23041.39 ❌
- **TP 4RR**: 23031.07 ❌
- **TP 4.5RR**: 23020.74 ❌
- **TP 5RR**: 23010.42 ❌
- **PnL**: -20.65 points (-1.0R)
- **MFE**: 57.56 points
- **MAE**: 32.32 points

### Trade #925 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-03 03:45:00
- **FVG 5m**: 23113.92 - 23122.76
- **Entrée**: 23099.28 @ 2025-07-03 03:46:00
- **Stop Loss**: 23134.32
- **Risk**: 35.04 points
- **TP 1RR**: 23064.24 ✅
- **TP 1.5RR**: 23046.72 ❌
- **TP 2RR**: 23029.20 ❌
- **TP 2.5RR**: 23011.67 ❌
- **TP 3RR**: 22994.15 ❌
- **TP 3.5RR**: 22976.63 ❌
- **TP 4RR**: 22959.11 ❌
- **TP 4.5RR**: 22941.59 ❌
- **TP 5RR**: 22924.07 ❌
- **PnL**: -35.04 points (-1.0R)
- **MFE**: 43.17 points
- **MAE**: 46.71 points

### Trade #926 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-04 03:45:00
- **FVG 5m**: 23168.71 - 23179.82
- **Entrée**: 23162.65 @ 2025-07-04 03:52:00
- **Stop Loss**: 23191.41
- **Risk**: 28.76 points
- **TP 1RR**: 23133.89 ✅
- **TP 1.5RR**: 23119.51 ✅
- **TP 2RR**: 23105.13 ❌
- **TP 2.5RR**: 23090.75 ❌
- **TP 3RR**: 23076.38 ❌
- **TP 3.5RR**: 23062.00 ❌
- **TP 4RR**: 23047.62 ❌
- **TP 4.5RR**: 23033.24 ❌
- **TP 5RR**: 23018.86 ❌
- **PnL**: -28.76 points (-1.0R)
- **MFE**: 54.03 points
- **MAE**: 74.99 points

### Trade #927 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-04 06:00:00
- **FVG 5m**: 23134.63 - 23141.69
- **Entrée**: 23143.71 @ 2025-07-04 06:01:00
- **Stop Loss**: 23123.06
- **Risk**: 20.66 points
- **TP 1RR**: 23164.37 ✅
- **TP 1.5RR**: 23174.70 ❌
- **TP 2RR**: 23185.03 ❌
- **TP 2.5RR**: 23195.36 ❌
- **TP 3RR**: 23205.68 ❌
- **TP 3.5RR**: 23216.01 ❌
- **TP 4RR**: 23226.34 ❌
- **TP 4.5RR**: 23236.67 ❌
- **TP 5RR**: 23247.00 ❌
- **PnL**: -20.66 points (-1.0R)
- **MFE**: 26.26 points
- **MAE**: 20.96 points

### Trade #928 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-06 17:00:00
- **FVG 5m**: 23140.43 - 23147.50
- **Entrée**: 23229.30 @ 2025-07-06 17:01:00
- **Stop Loss**: 23128.86
- **Risk**: 100.44 points
- **TP 1RR**: 23329.75 ❌
- **TP 1.5RR**: 23379.97 ❌
- **TP 2RR**: 23430.19 ❌
- **TP 2.5RR**: 23480.41 ❌
- **TP 3RR**: 23530.63 ❌
- **TP 3.5RR**: 23580.85 ❌
- **TP 4RR**: 23631.07 ❌
- **TP 4.5RR**: 23681.29 ❌
- **TP 5RR**: 23731.51 ❌
- **PnL**: -100.44 points (-1.0R)
- **MFE**: 20.70 points
- **MAE**: 102.00 points

### Trade #929 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-06 20:00:00
- **FVG 5m**: 23203.80 - 23212.89
- **Entrée**: 23192.69 @ 2025-07-06 20:01:00
- **Stop Loss**: 23224.50
- **Risk**: 31.80 points
- **TP 1RR**: 23160.89 ✅
- **TP 1.5RR**: 23144.99 ✅
- **TP 2RR**: 23129.09 ❌
- **TP 2.5RR**: 23113.18 ❌
- **TP 3RR**: 23097.28 ❌
- **TP 3.5RR**: 23081.38 ❌
- **TP 4RR**: 23065.48 ❌
- **TP 4.5RR**: 23049.57 ❌
- **TP 5RR**: 23033.67 ❌
- **PnL**: -31.80 points (-1.0R)
- **MFE**: 57.56 points
- **MAE**: 32.06 points

### Trade #930 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-07 07:15:00
- **FVG 5m**: 23197.24 - 23201.53
- **Entrée**: 23196.99 @ 2025-07-07 07:43:00
- **Stop Loss**: 23213.13
- **Risk**: 16.15 points
- **TP 1RR**: 23180.84 ✅
- **TP 1.5RR**: 23172.77 ✅
- **TP 2RR**: 23164.70 ✅
- **TP 2.5RR**: 23156.62 ✅
- **TP 3RR**: 23148.55 ✅
- **TP 3.5RR**: 23140.48 ✅
- **TP 4RR**: 23132.41 ✅
- **TP 4.5RR**: 23124.33 ✅
- **TP 5RR**: 23116.26 ✅
- **PnL**: 80.73 points (5.0R)
- **MFE**: 81.55 points
- **MAE**: 8.08 points

### Trade #931 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-07 07:15:00
- **FVG 5m**: 23197.24 - 23201.53
- **Entrée**: 23196.99 @ 2025-07-07 07:43:00
- **Stop Loss**: 23213.13
- **Risk**: 16.15 points
- **TP 1RR**: 23180.84 ✅
- **TP 1.5RR**: 23172.77 ✅
- **TP 2RR**: 23164.70 ✅
- **TP 2.5RR**: 23156.62 ✅
- **TP 3RR**: 23148.55 ✅
- **TP 3.5RR**: 23140.48 ✅
- **TP 4RR**: 23132.41 ✅
- **TP 4.5RR**: 23124.33 ✅
- **TP 5RR**: 23116.26 ✅
- **PnL**: 80.73 points (5.0R)
- **MFE**: 81.55 points
- **MAE**: 8.08 points

### Trade #932 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 08:30:00
- **FVG 5m**: 23182.60 - 23189.92
- **Entrée**: 23198.25 @ 2025-07-07 08:51:00
- **Stop Loss**: 23171.00
- **Risk**: 27.24 points
- **TP 1RR**: 23225.49 ❌
- **TP 1.5RR**: 23239.12 ❌
- **TP 2RR**: 23252.74 ❌
- **TP 2.5RR**: 23266.36 ❌
- **TP 3RR**: 23279.98 ❌
- **TP 3.5RR**: 23293.61 ❌
- **TP 4RR**: 23307.23 ❌
- **TP 4.5RR**: 23320.85 ❌
- **TP 5RR**: 23334.47 ❌
- **PnL**: -27.24 points (-1.0R)
- **MFE**: 6.82 points
- **MAE**: 29.03 points

### Trade #933 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 08:30:00
- **FVG 5m**: 23182.60 - 23189.92
- **Entrée**: 23198.25 @ 2025-07-07 08:51:00
- **Stop Loss**: 23171.00
- **Risk**: 27.24 points
- **TP 1RR**: 23225.49 ❌
- **TP 1.5RR**: 23239.12 ❌
- **TP 2RR**: 23252.74 ❌
- **TP 2.5RR**: 23266.36 ❌
- **TP 3RR**: 23279.98 ❌
- **TP 3.5RR**: 23293.61 ❌
- **TP 4RR**: 23307.23 ❌
- **TP 4.5RR**: 23320.85 ❌
- **TP 5RR**: 23334.47 ❌
- **PnL**: -27.24 points (-1.0R)
- **MFE**: 6.82 points
- **MAE**: 29.03 points

### Trade #934 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-07 11:45:00
- **FVG 5m**: 23164.67 - 23174.77
- **Entrée**: 23098.27 @ 2025-07-07 11:46:00
- **Stop Loss**: 23186.36
- **Risk**: 88.09 points
- **TP 1RR**: 23010.18 ✅
- **TP 1.5RR**: 22966.14 ❌
- **TP 2RR**: 22922.09 ❌
- **TP 2.5RR**: 22878.05 ❌
- **TP 3RR**: 22834.01 ❌
- **TP 3.5RR**: 22789.96 ❌
- **TP 4RR**: 22745.92 ❌
- **TP 4.5RR**: 22701.87 ❌
- **TP 5RR**: 22657.83 ❌
- **PnL**: -88.09 points (-1.0R)
- **MFE**: 92.91 points
- **MAE**: 90.64 points

### Trade #935 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23056.11 - 23091.45
- **Entrée**: 23099.78 @ 2025-07-07 13:55:00
- **Stop Loss**: 23044.58
- **Risk**: 55.21 points
- **TP 1RR**: 23154.99 ❌
- **TP 1.5RR**: 23182.59 ❌
- **TP 2RR**: 23210.20 ❌
- **TP 2.5RR**: 23237.80 ❌
- **TP 3RR**: 23265.40 ❌
- **TP 3.5RR**: 23293.01 ❌
- **TP 4RR**: 23320.61 ❌
- **TP 4.5RR**: 23348.21 ❌
- **TP 5RR**: 23375.82 ❌
- **PnL**: -55.21 points (-1.0R)
- **MFE**: 18.18 points
- **MAE**: 56.05 points

### Trade #936 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23056.11 - 23091.45
- **Entrée**: 23099.78 @ 2025-07-07 13:55:00
- **Stop Loss**: 23044.58
- **Risk**: 55.21 points
- **TP 1RR**: 23154.99 ❌
- **TP 1.5RR**: 23182.59 ❌
- **TP 2RR**: 23210.20 ❌
- **TP 2.5RR**: 23237.80 ❌
- **TP 3RR**: 23265.40 ❌
- **TP 3.5RR**: 23293.01 ❌
- **TP 4RR**: 23320.61 ❌
- **TP 4.5RR**: 23348.21 ❌
- **TP 5RR**: 23375.82 ❌
- **PnL**: -55.21 points (-1.0R)
- **MFE**: 18.18 points
- **MAE**: 56.05 points

### Trade #937 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23056.11 - 23091.45
- **Entrée**: 23099.78 @ 2025-07-07 13:55:00
- **Stop Loss**: 23044.58
- **Risk**: 55.21 points
- **TP 1RR**: 23154.99 ❌
- **TP 1.5RR**: 23182.59 ❌
- **TP 2RR**: 23210.20 ❌
- **TP 2.5RR**: 23237.80 ❌
- **TP 3RR**: 23265.40 ❌
- **TP 3.5RR**: 23293.01 ❌
- **TP 4RR**: 23320.61 ❌
- **TP 4.5RR**: 23348.21 ❌
- **TP 5RR**: 23375.82 ❌
- **PnL**: -55.21 points (-1.0R)
- **MFE**: 18.18 points
- **MAE**: 56.05 points

### Trade #938 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23056.11 - 23091.45
- **Entrée**: 23099.78 @ 2025-07-07 13:55:00
- **Stop Loss**: 23044.58
- **Risk**: 55.21 points
- **TP 1RR**: 23154.99 ❌
- **TP 1.5RR**: 23182.59 ❌
- **TP 2RR**: 23210.20 ❌
- **TP 2.5RR**: 23237.80 ❌
- **TP 3RR**: 23265.40 ❌
- **TP 3.5RR**: 23293.01 ❌
- **TP 4RR**: 23320.61 ❌
- **TP 4.5RR**: 23348.21 ❌
- **TP 5RR**: 23375.82 ❌
- **PnL**: -55.21 points (-1.0R)
- **MFE**: 18.18 points
- **MAE**: 56.05 points

### Trade #939 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 19:30:00
- **FVG 5m**: 23050.80 - 23058.38
- **Entrée**: 23108.62 @ 2025-07-07 19:31:00
- **Stop Loss**: 23039.28
- **Risk**: 69.34 points
- **TP 1RR**: 23177.96 ✅
- **TP 1.5RR**: 23212.63 ✅
- **TP 2RR**: 23247.30 ✅
- **TP 2.5RR**: 23281.98 ✅
- **TP 3RR**: 23316.65 ✅
- **TP 3.5RR**: 23351.32 ❌
- **TP 4RR**: 23385.99 ❌
- **TP 4.5RR**: 23420.66 ❌
- **TP 5RR**: 23455.33 ❌
- **PnL**: -69.34 points (-1.0R)
- **MFE**: 232.28 points
- **MAE**: 79.78 points

### Trade #940 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 21:15:00
- **FVG 5m**: 23120.49 - 23138.92
- **Entrée**: 23141.69 @ 2025-07-07 21:26:00
- **Stop Loss**: 23108.93
- **Risk**: 32.77 points
- **TP 1RR**: 23174.46 ✅
- **TP 1.5RR**: 23190.85 ✅
- **TP 2RR**: 23207.23 ❌
- **TP 2.5RR**: 23223.62 ❌
- **TP 3RR**: 23240.00 ❌
- **TP 3.5RR**: 23256.38 ❌
- **TP 4RR**: 23272.77 ❌
- **TP 4.5RR**: 23289.15 ❌
- **TP 5RR**: 23305.54 ❌
- **PnL**: -32.77 points (-1.0R)
- **MFE**: 58.57 points
- **MAE**: 34.08 points

### Trade #941 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 06:30:00
- **FVG 5m**: 23145.99 - 23150.03
- **Entrée**: 23172.24 @ 2025-07-08 06:31:00
- **Stop Loss**: 23134.41
- **Risk**: 37.83 points
- **TP 1RR**: 23210.07 ❌
- **TP 1.5RR**: 23228.99 ❌
- **TP 2RR**: 23247.91 ❌
- **TP 2.5RR**: 23266.82 ❌
- **TP 3RR**: 23285.74 ❌
- **TP 3.5RR**: 23304.65 ❌
- **TP 4RR**: 23323.57 ❌
- **TP 4.5RR**: 23342.48 ❌
- **TP 5RR**: 23361.40 ❌
- **PnL**: -37.83 points (-1.0R)
- **MFE**: 12.12 points
- **MAE**: 47.47 points

### Trade #942 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-08 08:15:00
- **FVG 5m**: 23167.70 - 23174.26
- **Entrée**: 23166.44 @ 2025-07-08 08:19:00
- **Stop Loss**: 23185.85
- **Risk**: 19.41 points
- **TP 1RR**: 23147.02 ✅
- **TP 1.5RR**: 23137.32 ✅
- **TP 2RR**: 23127.61 ✅
- **TP 2.5RR**: 23117.90 ✅
- **TP 3RR**: 23108.20 ✅
- **TP 3.5RR**: 23098.49 ✅
- **TP 4RR**: 23088.78 ✅
- **TP 4.5RR**: 23079.07 ✅
- **TP 5RR**: 23069.37 ✅
- **PnL**: 97.07 points (5.0R)
- **MFE**: 98.72 points
- **MAE**: 9.09 points

### Trade #943 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-08 08:45:00
- **FVG 5m**: 23167.70 - 23174.26
- **Entrée**: 23134.63 @ 2025-07-08 08:46:00
- **Stop Loss**: 23185.85
- **Risk**: 51.23 points
- **TP 1RR**: 23083.40 ✅
- **TP 1.5RR**: 23057.79 ❌
- **TP 2RR**: 23032.17 ❌
- **TP 2.5RR**: 23006.56 ❌
- **TP 3RR**: 22980.95 ❌
- **TP 3.5RR**: 22955.33 ❌
- **TP 4RR**: 22929.72 ❌
- **TP 4.5RR**: 22904.11 ❌
- **TP 5RR**: 22878.50 ❌
- **PnL**: -51.23 points (-1.0R)
- **MFE**: 67.41 points
- **MAE**: 53.02 points

### Trade #944 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 09:30:00
- **FVG 5m**: 23143.71 - 23158.11
- **Entrée**: 23165.68 @ 2025-07-08 09:38:00
- **Stop Loss**: 23132.14
- **Risk**: 33.54 points
- **TP 1RR**: 23199.22 ❌
- **TP 1.5RR**: 23215.99 ❌
- **TP 2RR**: 23232.75 ❌
- **TP 2.5RR**: 23249.52 ❌
- **TP 3RR**: 23266.29 ❌
- **TP 3.5RR**: 23283.06 ❌
- **TP 4RR**: 23299.83 ❌
- **TP 4.5RR**: 23316.60 ❌
- **TP 5RR**: 23333.37 ❌
- **PnL**: -33.54 points (-1.0R)
- **MFE**: 4.29 points
- **MAE**: 52.52 points

### Trade #945 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 09:30:00
- **FVG 5m**: 23143.71 - 23158.11
- **Entrée**: 23165.68 @ 2025-07-08 09:38:00
- **Stop Loss**: 23132.14
- **Risk**: 33.54 points
- **TP 1RR**: 23199.22 ❌
- **TP 1.5RR**: 23215.99 ❌
- **TP 2RR**: 23232.75 ❌
- **TP 2.5RR**: 23249.52 ❌
- **TP 3RR**: 23266.29 ❌
- **TP 3.5RR**: 23283.06 ❌
- **TP 4RR**: 23299.83 ❌
- **TP 4.5RR**: 23316.60 ❌
- **TP 5RR**: 23333.37 ❌
- **PnL**: -33.54 points (-1.0R)
- **MFE**: 4.29 points
- **MAE**: 52.52 points

### Trade #946 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 09:30:00
- **FVG 5m**: 23143.71 - 23158.11
- **Entrée**: 23165.68 @ 2025-07-08 09:38:00
- **Stop Loss**: 23132.14
- **Risk**: 33.54 points
- **TP 1RR**: 23199.22 ❌
- **TP 1.5RR**: 23215.99 ❌
- **TP 2RR**: 23232.75 ❌
- **TP 2.5RR**: 23249.52 ❌
- **TP 3RR**: 23266.29 ❌
- **TP 3.5RR**: 23283.06 ❌
- **TP 4RR**: 23299.83 ❌
- **TP 4.5RR**: 23316.60 ❌
- **TP 5RR**: 23333.37 ❌
- **PnL**: -33.54 points (-1.0R)
- **MFE**: 4.29 points
- **MAE**: 52.52 points

### Trade #947 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 19:30:00
- **FVG 5m**: 23107.11 - 23109.88
- **Entrée**: 23111.40 @ 2025-07-08 20:04:00
- **Stop Loss**: 23095.55
- **Risk**: 15.85 points
- **TP 1RR**: 23127.24 ❌
- **TP 1.5RR**: 23135.17 ❌
- **TP 2RR**: 23143.09 ❌
- **TP 2.5RR**: 23151.01 ❌
- **TP 3RR**: 23158.93 ❌
- **TP 3.5RR**: 23166.86 ❌
- **TP 4RR**: 23174.78 ❌
- **TP 4.5RR**: 23182.70 ❌
- **TP 5RR**: 23190.63 ❌
- **PnL**: -15.85 points (-1.0R)
- **MFE**: 6.82 points
- **MAE**: 17.93 points

### Trade #948 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 20:30:00
- **FVG 5m**: 23107.11 - 23109.88
- **Entrée**: 23110.14 @ 2025-07-08 20:51:00
- **Stop Loss**: 23095.55
- **Risk**: 14.58 points
- **TP 1RR**: 23124.72 ✅
- **TP 1.5RR**: 23132.01 ❌
- **TP 2RR**: 23139.30 ❌
- **TP 2.5RR**: 23146.59 ❌
- **TP 3RR**: 23153.88 ❌
- **TP 3.5RR**: 23161.18 ❌
- **TP 4RR**: 23168.47 ❌
- **TP 4.5RR**: 23175.76 ❌
- **TP 5RR**: 23183.05 ❌
- **PnL**: -14.58 points (-1.0R)
- **MFE**: 18.18 points
- **MAE**: 15.15 points

### Trade #949 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:15:00
- **FVG 5m**: 23292.93 - 23305.05
- **Entrée**: 23282.32 @ 2025-07-09 09:27:00
- **Stop Loss**: 23316.70
- **Risk**: 34.38 points
- **TP 1RR**: 23247.95 ✅
- **TP 1.5RR**: 23230.76 ✅
- **TP 2RR**: 23213.57 ✅
- **TP 2.5RR**: 23196.39 ✅
- **TP 3RR**: 23179.20 ✅
- **TP 3.5RR**: 23162.01 ✅
- **TP 4RR**: 23144.82 ❌
- **TP 4.5RR**: 23127.63 ❌
- **TP 5RR**: 23110.45 ❌
- **PnL**: -34.38 points (-1.0R)
- **MFE**: 135.58 points
- **MAE**: 36.36 points

### Trade #950 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:30:00
- **FVG 5m**: 23292.93 - 23305.05
- **Entrée**: 23229.05 @ 2025-07-09 09:31:00
- **Stop Loss**: 23316.70
- **Risk**: 87.65 points
- **TP 1RR**: 23141.40 ❌
- **TP 1.5RR**: 23097.58 ❌
- **TP 2RR**: 23053.76 ❌
- **TP 2.5RR**: 23009.93 ❌
- **TP 3RR**: 22966.11 ❌
- **TP 3.5RR**: 22922.28 ❌
- **TP 4RR**: 22878.46 ❌
- **TP 4.5RR**: 22834.64 ❌
- **TP 5RR**: 22790.81 ❌
- **PnL**: -87.65 points (-1.0R)
- **MFE**: 82.31 points
- **MAE**: 89.63 points

### Trade #951 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:30:00
- **FVG 5m**: 23292.93 - 23305.05
- **Entrée**: 23229.05 @ 2025-07-09 09:31:00
- **Stop Loss**: 23316.70
- **Risk**: 87.65 points
- **TP 1RR**: 23141.40 ❌
- **TP 1.5RR**: 23097.58 ❌
- **TP 2RR**: 23053.76 ❌
- **TP 2.5RR**: 23009.93 ❌
- **TP 3RR**: 22966.11 ❌
- **TP 3.5RR**: 22922.28 ❌
- **TP 4RR**: 22878.46 ❌
- **TP 4.5RR**: 22834.64 ❌
- **TP 5RR**: 22790.81 ❌
- **PnL**: -87.65 points (-1.0R)
- **MFE**: 82.31 points
- **MAE**: 89.63 points

### Trade #952 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23292.93 - 23305.05
- **Entrée**: 23224.25 @ 2025-07-09 09:46:00
- **Stop Loss**: 23316.70
- **Risk**: 92.44 points
- **TP 1RR**: 23131.81 ❌
- **TP 1.5RR**: 23085.59 ❌
- **TP 2RR**: 23039.36 ❌
- **TP 2.5RR**: 22993.14 ❌
- **TP 3RR**: 22946.92 ❌
- **TP 3.5RR**: 22900.70 ❌
- **TP 4RR**: 22854.47 ❌
- **TP 4.5RR**: 22808.25 ❌
- **TP 5RR**: 22762.03 ❌
- **PnL**: -92.44 points (-1.0R)
- **MFE**: 77.51 points
- **MAE**: 94.43 points

### Trade #953 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23292.93 - 23305.05
- **Entrée**: 23224.25 @ 2025-07-09 09:46:00
- **Stop Loss**: 23316.70
- **Risk**: 92.44 points
- **TP 1RR**: 23131.81 ❌
- **TP 1.5RR**: 23085.59 ❌
- **TP 2RR**: 23039.36 ❌
- **TP 2.5RR**: 22993.14 ❌
- **TP 3RR**: 22946.92 ❌
- **TP 3.5RR**: 22900.70 ❌
- **TP 4RR**: 22854.47 ❌
- **TP 4.5RR**: 22808.25 ❌
- **TP 5RR**: 22762.03 ❌
- **PnL**: -92.44 points (-1.0R)
- **MFE**: 77.51 points
- **MAE**: 94.43 points

### Trade #954 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23292.93 - 23305.05
- **Entrée**: 23224.25 @ 2025-07-09 09:46:00
- **Stop Loss**: 23316.70
- **Risk**: 92.44 points
- **TP 1RR**: 23131.81 ❌
- **TP 1.5RR**: 23085.59 ❌
- **TP 2RR**: 23039.36 ❌
- **TP 2.5RR**: 22993.14 ❌
- **TP 3RR**: 22946.92 ❌
- **TP 3.5RR**: 22900.70 ❌
- **TP 4RR**: 22854.47 ❌
- **TP 4.5RR**: 22808.25 ❌
- **TP 5RR**: 22762.03 ❌
- **PnL**: -92.44 points (-1.0R)
- **MFE**: 77.51 points
- **MAE**: 94.43 points

### Trade #955 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23292.93 - 23305.05
- **Entrée**: 23224.25 @ 2025-07-09 09:46:00
- **Stop Loss**: 23316.70
- **Risk**: 92.44 points
- **TP 1RR**: 23131.81 ❌
- **TP 1.5RR**: 23085.59 ❌
- **TP 2RR**: 23039.36 ❌
- **TP 2.5RR**: 22993.14 ❌
- **TP 3RR**: 22946.92 ❌
- **TP 3.5RR**: 22900.70 ❌
- **TP 4RR**: 22854.47 ❌
- **TP 4.5RR**: 22808.25 ❌
- **TP 5RR**: 22762.03 ❌
- **PnL**: -92.44 points (-1.0R)
- **MFE**: 77.51 points
- **MAE**: 94.43 points

### Trade #956 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 04:15:00
- **FVG 5m**: 23257.08 - 23260.36
- **Entrée**: 23255.31 @ 2025-07-10 04:22:00
- **Stop Loss**: 23271.99
- **Risk**: 16.68 points
- **TP 1RR**: 23238.63 ❌
- **TP 1.5RR**: 23230.29 ❌
- **TP 2RR**: 23221.95 ❌
- **TP 2.5RR**: 23213.61 ❌
- **TP 3RR**: 23205.27 ❌
- **TP 3.5RR**: 23196.93 ❌
- **TP 4RR**: 23188.59 ❌
- **TP 4.5RR**: 23180.25 ❌
- **TP 5RR**: 23171.91 ❌
- **PnL**: -16.68 points (-1.0R)
- **MFE**: 15.40 points
- **MAE**: 17.67 points

### Trade #957 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 08:30:00
- **FVG 5m**: 23288.64 - 23291.41
- **Entrée**: 23286.36 @ 2025-07-10 08:31:00
- **Stop Loss**: 23303.06
- **Risk**: 16.70 points
- **TP 1RR**: 23269.67 ✅
- **TP 1.5RR**: 23261.32 ✅
- **TP 2RR**: 23252.97 ✅
- **TP 2.5RR**: 23244.63 ✅
- **TP 3RR**: 23236.28 ✅
- **TP 3.5RR**: 23227.93 ✅
- **TP 4RR**: 23219.58 ✅
- **TP 4.5RR**: 23211.23 ✅
- **TP 5RR**: 23202.89 ✅
- **PnL**: 83.48 points (5.0R)
- **MFE**: 90.89 points
- **MAE**: 0.50 points

### Trade #958 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 08:30:00
- **FVG 5m**: 23288.64 - 23291.41
- **Entrée**: 23286.36 @ 2025-07-10 08:31:00
- **Stop Loss**: 23303.06
- **Risk**: 16.70 points
- **TP 1RR**: 23269.67 ✅
- **TP 1.5RR**: 23261.32 ✅
- **TP 2RR**: 23252.97 ✅
- **TP 2.5RR**: 23244.63 ✅
- **TP 3RR**: 23236.28 ✅
- **TP 3.5RR**: 23227.93 ✅
- **TP 4RR**: 23219.58 ✅
- **TP 4.5RR**: 23211.23 ✅
- **TP 5RR**: 23202.89 ✅
- **PnL**: 83.48 points (5.0R)
- **MFE**: 90.89 points
- **MAE**: 0.50 points

### Trade #959 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 08:45:00
- **FVG 5m**: 23288.64 - 23291.41
- **Entrée**: 23250.01 @ 2025-07-10 08:46:00
- **Stop Loss**: 23303.06
- **Risk**: 53.05 points
- **TP 1RR**: 23196.95 ✅
- **TP 1.5RR**: 23170.43 ✅
- **TP 2RR**: 23143.90 ✅
- **TP 2.5RR**: 23117.38 ✅
- **TP 3RR**: 23090.85 ✅
- **TP 3.5RR**: 23064.33 ✅
- **TP 4RR**: 23037.80 ✅
- **TP 4.5RR**: 23011.27 ❌
- **TP 5RR**: 22984.75 ❌
- **PnL**: -53.05 points (-1.0R)
- **MFE**: 221.17 points
- **MAE**: 57.82 points

### Trade #960 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 10:15:00
- **FVG 5m**: 23158.36 - 23165.43
- **Entrée**: 23188.91 @ 2025-07-10 10:16:00
- **Stop Loss**: 23146.78
- **Risk**: 42.13 points
- **TP 1RR**: 23231.04 ✅
- **TP 1.5RR**: 23252.10 ✅
- **TP 2RR**: 23273.17 ✅
- **TP 2.5RR**: 23294.23 ❌
- **TP 3RR**: 23315.29 ❌
- **TP 3.5RR**: 23336.36 ❌
- **TP 4RR**: 23357.42 ❌
- **TP 4.5RR**: 23378.49 ❌
- **TP 5RR**: 23399.55 ❌
- **PnL**: -42.13 points (-1.0R)
- **MFE**: 89.38 points
- **MAE**: 47.97 points

### Trade #961 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 10:15:00
- **FVG 5m**: 23158.36 - 23165.43
- **Entrée**: 23188.91 @ 2025-07-10 10:16:00
- **Stop Loss**: 23146.78
- **Risk**: 42.13 points
- **TP 1RR**: 23231.04 ✅
- **TP 1.5RR**: 23252.10 ✅
- **TP 2RR**: 23273.17 ✅
- **TP 2.5RR**: 23294.23 ❌
- **TP 3RR**: 23315.29 ❌
- **TP 3.5RR**: 23336.36 ❌
- **TP 4RR**: 23357.42 ❌
- **TP 4.5RR**: 23378.49 ❌
- **TP 5RR**: 23399.55 ❌
- **PnL**: -42.13 points (-1.0R)
- **MFE**: 89.38 points
- **MAE**: 47.97 points

### Trade #962 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 19:00:00
- **FVG 5m**: 23264.15 - 23269.45
- **Entrée**: 23253.29 @ 2025-07-10 19:01:00
- **Stop Loss**: 23281.08
- **Risk**: 27.79 points
- **TP 1RR**: 23225.50 ✅
- **TP 1.5RR**: 23211.60 ✅
- **TP 2RR**: 23197.70 ✅
- **TP 2.5RR**: 23183.81 ✅
- **TP 3RR**: 23169.91 ✅
- **TP 3.5RR**: 23156.01 ✅
- **TP 4RR**: 23142.12 ✅
- **TP 4.5RR**: 23128.22 ✅
- **TP 5RR**: 23114.32 ✅
- **PnL**: 138.97 points (5.0R)
- **MFE**: 155.78 points
- **MAE**: 9.59 points

### Trade #963 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23264.15 - 23269.45
- **Entrée**: 23213.90 @ 2025-07-10 19:16:00
- **Stop Loss**: 23281.08
- **Risk**: 67.18 points
- **TP 1RR**: 23146.72 ✅
- **TP 1.5RR**: 23113.13 ✅
- **TP 2RR**: 23079.54 ✅
- **TP 2.5RR**: 23045.95 ✅
- **TP 3RR**: 23012.36 ❌
- **TP 3.5RR**: 22978.77 ❌
- **TP 4RR**: 22945.18 ❌
- **TP 4.5RR**: 22911.60 ❌
- **TP 5RR**: 22878.01 ❌
- **PnL**: -67.18 points (-1.0R)
- **MFE**: 185.06 points
- **MAE**: 67.92 points

### Trade #964 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23264.15 - 23269.45
- **Entrée**: 23213.90 @ 2025-07-10 19:16:00
- **Stop Loss**: 23281.08
- **Risk**: 67.18 points
- **TP 1RR**: 23146.72 ✅
- **TP 1.5RR**: 23113.13 ✅
- **TP 2RR**: 23079.54 ✅
- **TP 2.5RR**: 23045.95 ✅
- **TP 3RR**: 23012.36 ❌
- **TP 3.5RR**: 22978.77 ❌
- **TP 4RR**: 22945.18 ❌
- **TP 4.5RR**: 22911.60 ❌
- **TP 5RR**: 22878.01 ❌
- **PnL**: -67.18 points (-1.0R)
- **MFE**: 185.06 points
- **MAE**: 67.92 points

### Trade #965 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 20:00:00
- **FVG 5m**: 23126.55 - 23131.34
- **Entrée**: 23137.65 @ 2025-07-10 20:15:00
- **Stop Loss**: 23114.98
- **Risk**: 22.67 points
- **TP 1RR**: 23160.33 ✅
- **TP 1.5RR**: 23171.66 ✅
- **TP 2RR**: 23183.00 ✅
- **TP 2.5RR**: 23194.34 ✅
- **TP 3RR**: 23205.67 ❌
- **TP 3.5RR**: 23217.01 ❌
- **TP 4RR**: 23228.34 ❌
- **TP 4.5RR**: 23239.68 ❌
- **TP 5RR**: 23251.02 ❌
- **PnL**: -22.67 points (-1.0R)
- **MFE**: 66.65 points
- **MAE**: 26.51 points

### Trade #966 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-11 08:30:00
- **FVG 5m**: 23125.03 - 23130.84
- **Entrée**: 23121.50 @ 2025-07-11 08:37:00
- **Stop Loss**: 23142.40
- **Risk**: 20.91 points
- **TP 1RR**: 23100.59 ✅
- **TP 1.5RR**: 23090.14 ✅
- **TP 2RR**: 23079.68 ❌
- **TP 2.5RR**: 23069.23 ❌
- **TP 3RR**: 23058.78 ❌
- **TP 3.5RR**: 23048.32 ❌
- **TP 4RR**: 23037.87 ❌
- **TP 4.5RR**: 23027.41 ❌
- **TP 5RR**: 23016.96 ❌
- **PnL**: -20.91 points (-1.0R)
- **MFE**: 32.06 points
- **MAE**: 37.87 points

### Trade #967 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-11 09:15:00
- **FVG 5m**: 23124.78 - 23136.14
- **Entrée**: 23211.88 @ 2025-07-11 09:16:00
- **Stop Loss**: 23113.22
- **Risk**: 98.67 points
- **TP 1RR**: 23310.55 ❌
- **TP 1.5RR**: 23359.88 ❌
- **TP 2RR**: 23409.22 ❌
- **TP 2.5RR**: 23458.55 ❌
- **TP 3RR**: 23507.88 ❌
- **TP 3.5RR**: 23557.22 ❌
- **TP 4RR**: 23606.55 ❌
- **TP 4.5RR**: 23655.88 ❌
- **TP 5RR**: 23705.22 ❌
- **PnL**: -98.67 points (-1.0R)
- **MFE**: 37.62 points
- **MAE**: 183.05 points

### Trade #968 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 02:30:00
- **FVG 5m**: 23043.73 - 23049.04
- **Entrée**: 23051.06 @ 2025-07-14 02:31:00
- **Stop Loss**: 23032.21
- **Risk**: 18.84 points
- **TP 1RR**: 23069.90 ✅
- **TP 1.5RR**: 23079.32 ✅
- **TP 2RR**: 23088.74 ✅
- **TP 2.5RR**: 23098.16 ✅
- **TP 3RR**: 23107.59 ✅
- **TP 3.5RR**: 23117.01 ✅
- **TP 4RR**: 23126.43 ✅
- **TP 4.5RR**: 23135.85 ✅
- **TP 5RR**: 23145.27 ✅
- **PnL**: 94.22 points (5.0R)
- **MFE**: 97.46 points
- **MAE**: 0.00 points

### Trade #969 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 02:30:00
- **FVG 5m**: 23043.73 - 23049.04
- **Entrée**: 23051.06 @ 2025-07-14 02:31:00
- **Stop Loss**: 23032.21
- **Risk**: 18.84 points
- **TP 1RR**: 23069.90 ✅
- **TP 1.5RR**: 23079.32 ✅
- **TP 2RR**: 23088.74 ✅
- **TP 2.5RR**: 23098.16 ✅
- **TP 3RR**: 23107.59 ✅
- **TP 3.5RR**: 23117.01 ✅
- **TP 4RR**: 23126.43 ✅
- **TP 4.5RR**: 23135.85 ✅
- **TP 5RR**: 23145.27 ✅
- **PnL**: 94.22 points (5.0R)
- **MFE**: 97.46 points
- **MAE**: 0.00 points

### Trade #970 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 08:15:00
- **FVG 5m**: 23101.55 - 23111.40
- **Entrée**: 23126.04 @ 2025-07-14 08:16:00
- **Stop Loss**: 23090.00
- **Risk**: 36.04 points
- **TP 1RR**: 23162.08 ✅
- **TP 1.5RR**: 23180.10 ✅
- **TP 2RR**: 23198.12 ✅
- **TP 2.5RR**: 23216.14 ❌
- **TP 3RR**: 23234.16 ❌
- **TP 3.5RR**: 23252.18 ❌
- **TP 4RR**: 23270.20 ❌
- **TP 4.5RR**: 23288.23 ❌
- **TP 5RR**: 23306.25 ❌
- **PnL**: -36.04 points (-1.0R)
- **MFE**: 80.79 points
- **MAE**: 45.45 points

### Trade #971 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 08:15:00
- **FVG 5m**: 23101.55 - 23111.40
- **Entrée**: 23126.04 @ 2025-07-14 08:16:00
- **Stop Loss**: 23090.00
- **Risk**: 36.04 points
- **TP 1RR**: 23162.08 ✅
- **TP 1.5RR**: 23180.10 ✅
- **TP 2RR**: 23198.12 ✅
- **TP 2.5RR**: 23216.14 ❌
- **TP 3RR**: 23234.16 ❌
- **TP 3.5RR**: 23252.18 ❌
- **TP 4RR**: 23270.20 ❌
- **TP 4.5RR**: 23288.23 ❌
- **TP 5RR**: 23306.25 ❌
- **PnL**: -36.04 points (-1.0R)
- **MFE**: 80.79 points
- **MAE**: 45.45 points

### Trade #972 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 08:30:00
- **FVG 5m**: 23133.62 - 23145.48
- **Entrée**: 23105.09 @ 2025-07-14 08:42:00
- **Stop Loss**: 23157.05
- **Risk**: 51.97 points
- **TP 1RR**: 23053.12 ❌
- **TP 1.5RR**: 23027.13 ❌
- **TP 2RR**: 23001.15 ❌
- **TP 2.5RR**: 22975.16 ❌
- **TP 3RR**: 22949.18 ❌
- **TP 3.5RR**: 22923.19 ❌
- **TP 4RR**: 22897.21 ❌
- **TP 4.5RR**: 22871.23 ❌
- **TP 5RR**: 22845.24 ❌
- **PnL**: -51.97 points (-1.0R)
- **MFE**: 36.61 points
- **MAE**: 57.06 points

### Trade #973 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 08:30:00
- **FVG 5m**: 23133.62 - 23145.48
- **Entrée**: 23105.09 @ 2025-07-14 08:42:00
- **Stop Loss**: 23157.05
- **Risk**: 51.97 points
- **TP 1RR**: 23053.12 ❌
- **TP 1.5RR**: 23027.13 ❌
- **TP 2RR**: 23001.15 ❌
- **TP 2.5RR**: 22975.16 ❌
- **TP 3RR**: 22949.18 ❌
- **TP 3.5RR**: 22923.19 ❌
- **TP 4RR**: 22897.21 ❌
- **TP 4.5RR**: 22871.23 ❌
- **TP 5RR**: 22845.24 ❌
- **PnL**: -51.97 points (-1.0R)
- **MFE**: 36.61 points
- **MAE**: 57.06 points

### Trade #974 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 21:15:00
- **FVG 5m**: 23345.19 - 23365.14
- **Entrée**: 23335.34 @ 2025-07-14 21:16:00
- **Stop Loss**: 23376.82
- **Risk**: 41.47 points
- **TP 1RR**: 23293.87 ✅
- **TP 1.5RR**: 23273.13 ✅
- **TP 2RR**: 23252.39 ❌
- **TP 2.5RR**: 23231.66 ❌
- **TP 3RR**: 23210.92 ❌
- **TP 3.5RR**: 23190.18 ❌
- **TP 4RR**: 23169.44 ❌
- **TP 4.5RR**: 23148.71 ❌
- **TP 5RR**: 23127.97 ❌
- **PnL**: -41.47 points (-1.0R)
- **MFE**: 67.41 points
- **MAE**: 42.42 points

### Trade #975 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 21:15:00
- **FVG 5m**: 23345.19 - 23365.14
- **Entrée**: 23335.34 @ 2025-07-14 21:16:00
- **Stop Loss**: 23376.82
- **Risk**: 41.47 points
- **TP 1RR**: 23293.87 ✅
- **TP 1.5RR**: 23273.13 ✅
- **TP 2RR**: 23252.39 ❌
- **TP 2.5RR**: 23231.66 ❌
- **TP 3RR**: 23210.92 ❌
- **TP 3.5RR**: 23190.18 ❌
- **TP 4RR**: 23169.44 ❌
- **TP 4.5RR**: 23148.71 ❌
- **TP 5RR**: 23127.97 ❌
- **PnL**: -41.47 points (-1.0R)
- **MFE**: 67.41 points
- **MAE**: 42.42 points

### Trade #976 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 06:15:00
- **FVG 5m**: 23399.47 - 23405.53
- **Entrée**: 23398.46 @ 2025-07-15 06:44:00
- **Stop Loss**: 23417.23
- **Risk**: 18.77 points
- **TP 1RR**: 23379.69 ✅
- **TP 1.5RR**: 23370.30 ✅
- **TP 2RR**: 23360.92 ❌
- **TP 2.5RR**: 23351.53 ❌
- **TP 3RR**: 23342.15 ❌
- **TP 3.5RR**: 23332.76 ❌
- **TP 4RR**: 23323.37 ❌
- **TP 4.5RR**: 23313.99 ❌
- **TP 5RR**: 23304.60 ❌
- **PnL**: -18.77 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 31.31 points

### Trade #977 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 07:30:00
- **FVG 5m**: 23399.47 - 23405.53
- **Entrée**: 23392.40 @ 2025-07-15 07:40:00
- **Stop Loss**: 23417.23
- **Risk**: 24.83 points
- **TP 1RR**: 23367.57 ❌
- **TP 1.5RR**: 23355.16 ❌
- **TP 2RR**: 23342.74 ❌
- **TP 2.5RR**: 23330.32 ❌
- **TP 3RR**: 23317.91 ❌
- **TP 3.5RR**: 23305.49 ❌
- **TP 4RR**: 23293.08 ❌
- **TP 4.5RR**: 23280.66 ❌
- **TP 5RR**: 23268.25 ❌
- **PnL**: -24.83 points (-1.0R)
- **MFE**: 5.55 points
- **MAE**: 25.75 points

### Trade #978 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 07:30:00
- **FVG 5m**: 23399.47 - 23405.53
- **Entrée**: 23392.40 @ 2025-07-15 07:40:00
- **Stop Loss**: 23417.23
- **Risk**: 24.83 points
- **TP 1RR**: 23367.57 ❌
- **TP 1.5RR**: 23355.16 ❌
- **TP 2RR**: 23342.74 ❌
- **TP 2.5RR**: 23330.32 ❌
- **TP 3RR**: 23317.91 ❌
- **TP 3.5RR**: 23305.49 ❌
- **TP 4RR**: 23293.08 ❌
- **TP 4.5RR**: 23280.66 ❌
- **TP 5RR**: 23268.25 ❌
- **PnL**: -24.83 points (-1.0R)
- **MFE**: 5.55 points
- **MAE**: 25.75 points

### Trade #979 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 09:45:00
- **FVG 5m**: 23397.45 - 23400.48
- **Entrée**: 23384.32 @ 2025-07-15 09:46:00
- **Stop Loss**: 23412.18
- **Risk**: 27.86 points
- **TP 1RR**: 23356.47 ✅
- **TP 1.5RR**: 23342.54 ✅
- **TP 2RR**: 23328.61 ✅
- **TP 2.5RR**: 23314.68 ✅
- **TP 3RR**: 23300.75 ✅
- **TP 3.5RR**: 23286.82 ✅
- **TP 4RR**: 23272.89 ✅
- **TP 4.5RR**: 23258.96 ✅
- **TP 5RR**: 23245.03 ✅
- **PnL**: 139.29 points (5.0R)
- **MFE**: 142.65 points
- **MAE**: 26.26 points

### Trade #980 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 11:45:00
- **FVG 5m**: 23353.02 - 23367.66
- **Entrée**: 23370.94 @ 2025-07-15 11:46:00
- **Stop Loss**: 23341.34
- **Risk**: 29.60 points
- **TP 1RR**: 23400.55 ❌
- **TP 1.5RR**: 23415.35 ❌
- **TP 2RR**: 23430.15 ❌
- **TP 2.5RR**: 23444.95 ❌
- **TP 3RR**: 23459.75 ❌
- **TP 3.5RR**: 23474.55 ❌
- **TP 4RR**: 23489.35 ❌
- **TP 4.5RR**: 23504.15 ❌
- **TP 5RR**: 23518.95 ❌
- **PnL**: -29.60 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 41.41 points

### Trade #981 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 12:30:00
- **FVG 5m**: 23359.83 - 23365.14
- **Entrée**: 23372.46 @ 2025-07-15 12:36:00
- **Stop Loss**: 23348.15
- **Risk**: 24.30 points
- **TP 1RR**: 23396.76 ✅
- **TP 1.5RR**: 23408.91 ✅
- **TP 2RR**: 23421.06 ❌
- **TP 2.5RR**: 23433.22 ❌
- **TP 3RR**: 23445.37 ❌
- **TP 3.5RR**: 23457.52 ❌
- **TP 4RR**: 23469.67 ❌
- **TP 4.5RR**: 23481.82 ❌
- **TP 5RR**: 23493.98 ❌
- **PnL**: -24.30 points (-1.0R)
- **MFE**: 37.11 points
- **MAE**: 29.03 points

### Trade #982 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 14:45:00
- **FVG 5m**: 23386.85 - 23390.89
- **Entrée**: 23331.81 @ 2025-07-15 14:46:00
- **Stop Loss**: 23402.58
- **Risk**: 70.77 points
- **TP 1RR**: 23261.03 ✅
- **TP 1.5RR**: 23225.65 ✅
- **TP 2RR**: 23190.26 ✅
- **TP 2.5RR**: 23154.87 ✅
- **TP 3RR**: 23119.48 ✅
- **TP 3.5RR**: 23084.10 ✅
- **TP 4RR**: 23048.71 ❌
- **TP 4.5RR**: 23013.32 ❌
- **TP 5RR**: 22977.93 ❌
- **PnL**: -70.77 points (-1.0R)
- **MFE**: 270.15 points
- **MAE**: 72.97 points

### Trade #983 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 17:00:00
- **FVG 5m**: 23325.75 - 23329.54
- **Entrée**: 23256.07 @ 2025-07-15 17:01:00
- **Stop Loss**: 23341.20
- **Risk**: 85.14 points
- **TP 1RR**: 23170.93 ✅
- **TP 1.5RR**: 23128.36 ✅
- **TP 2RR**: 23085.80 ✅
- **TP 2.5RR**: 23043.23 ❌
- **TP 3RR**: 23000.66 ❌
- **TP 3.5RR**: 22958.09 ❌
- **TP 4RR**: 22915.53 ❌
- **TP 4.5RR**: 22872.96 ❌
- **TP 5RR**: 22830.39 ❌
- **PnL**: -85.14 points (-1.0R)
- **MFE**: 194.41 points
- **MAE**: 97.20 points

### Trade #984 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 17:00:00
- **FVG 5m**: 23325.75 - 23329.54
- **Entrée**: 23256.07 @ 2025-07-15 17:01:00
- **Stop Loss**: 23341.20
- **Risk**: 85.14 points
- **TP 1RR**: 23170.93 ✅
- **TP 1.5RR**: 23128.36 ✅
- **TP 2RR**: 23085.80 ✅
- **TP 2.5RR**: 23043.23 ❌
- **TP 3RR**: 23000.66 ❌
- **TP 3.5RR**: 22958.09 ❌
- **TP 4RR**: 22915.53 ❌
- **TP 4.5RR**: 22872.96 ❌
- **TP 5RR**: 22830.39 ❌
- **PnL**: -85.14 points (-1.0R)
- **MFE**: 194.41 points
- **MAE**: 97.20 points

### Trade #985 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 17:00:00
- **FVG 5m**: 23325.75 - 23329.54
- **Entrée**: 23256.07 @ 2025-07-15 17:01:00
- **Stop Loss**: 23341.20
- **Risk**: 85.14 points
- **TP 1RR**: 23170.93 ✅
- **TP 1.5RR**: 23128.36 ✅
- **TP 2RR**: 23085.80 ✅
- **TP 2.5RR**: 23043.23 ❌
- **TP 3RR**: 23000.66 ❌
- **TP 3.5RR**: 22958.09 ❌
- **TP 4RR**: 22915.53 ❌
- **TP 4.5RR**: 22872.96 ❌
- **TP 5RR**: 22830.39 ❌
- **PnL**: -85.14 points (-1.0R)
- **MFE**: 194.41 points
- **MAE**: 97.20 points

### Trade #986 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 17:45:00
- **FVG 5m**: 23219.96 - 23234.35
- **Entrée**: 23236.12 @ 2025-07-15 17:55:00
- **Stop Loss**: 23208.35
- **Risk**: 27.77 points
- **TP 1RR**: 23263.89 ❌
- **TP 1.5RR**: 23277.77 ❌
- **TP 2RR**: 23291.66 ❌
- **TP 2.5RR**: 23305.54 ❌
- **TP 3RR**: 23319.43 ❌
- **TP 3.5RR**: 23333.31 ❌
- **TP 4RR**: 23347.19 ❌
- **TP 4.5RR**: 23361.08 ❌
- **TP 5RR**: 23374.96 ❌
- **PnL**: -27.77 points (-1.0R)
- **MFE**: 7.32 points
- **MAE**: 28.53 points

### Trade #987 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 19:30:00
- **FVG 5m**: 23228.55 - 23233.85
- **Entrée**: 23235.11 @ 2025-07-15 19:38:00
- **Stop Loss**: 23216.93
- **Risk**: 18.18 points
- **TP 1RR**: 23253.29 ✅
- **TP 1.5RR**: 23262.38 ✅
- **TP 2RR**: 23271.47 ✅
- **TP 2.5RR**: 23280.56 ❌
- **TP 3RR**: 23289.65 ❌
- **TP 3.5RR**: 23298.74 ❌
- **TP 4RR**: 23307.83 ❌
- **TP 4.5RR**: 23316.91 ❌
- **TP 5RR**: 23326.00 ❌
- **PnL**: -18.18 points (-1.0R)
- **MFE**: 38.38 points
- **MAE**: 18.68 points

### Trade #988 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23261.62 - 23289.90
- **Entrée**: 23255.06 @ 2025-07-16 08:34:00
- **Stop Loss**: 23301.54
- **Risk**: 46.49 points
- **TP 1RR**: 23208.57 ✅
- **TP 1.5RR**: 23185.33 ✅
- **TP 2RR**: 23162.08 ✅
- **TP 2.5RR**: 23138.84 ✅
- **TP 3RR**: 23115.60 ✅
- **TP 3.5RR**: 23092.35 ✅
- **TP 4RR**: 23069.11 ✅
- **TP 4.5RR**: 23045.87 ❌
- **TP 5RR**: 23022.62 ❌
- **PnL**: -46.49 points (-1.0R)
- **MFE**: 193.40 points
- **MAE**: 47.47 points

### Trade #989 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23261.62 - 23289.90
- **Entrée**: 23255.06 @ 2025-07-16 08:34:00
- **Stop Loss**: 23301.54
- **Risk**: 46.49 points
- **TP 1RR**: 23208.57 ✅
- **TP 1.5RR**: 23185.33 ✅
- **TP 2RR**: 23162.08 ✅
- **TP 2.5RR**: 23138.84 ✅
- **TP 3RR**: 23115.60 ✅
- **TP 3.5RR**: 23092.35 ✅
- **TP 4RR**: 23069.11 ✅
- **TP 4.5RR**: 23045.87 ❌
- **TP 5RR**: 23022.62 ❌
- **PnL**: -46.49 points (-1.0R)
- **MFE**: 193.40 points
- **MAE**: 47.47 points

### Trade #990 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23261.62 - 23289.90
- **Entrée**: 23255.06 @ 2025-07-16 08:34:00
- **Stop Loss**: 23301.54
- **Risk**: 46.49 points
- **TP 1RR**: 23208.57 ✅
- **TP 1.5RR**: 23185.33 ✅
- **TP 2RR**: 23162.08 ✅
- **TP 2.5RR**: 23138.84 ✅
- **TP 3RR**: 23115.60 ✅
- **TP 3.5RR**: 23092.35 ✅
- **TP 4RR**: 23069.11 ✅
- **TP 4.5RR**: 23045.87 ❌
- **TP 5RR**: 23022.62 ❌
- **PnL**: -46.49 points (-1.0R)
- **MFE**: 193.40 points
- **MAE**: 47.47 points

### Trade #991 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23261.62 - 23289.90
- **Entrée**: 23255.06 @ 2025-07-16 08:34:00
- **Stop Loss**: 23301.54
- **Risk**: 46.49 points
- **TP 1RR**: 23208.57 ✅
- **TP 1.5RR**: 23185.33 ✅
- **TP 2RR**: 23162.08 ✅
- **TP 2.5RR**: 23138.84 ✅
- **TP 3RR**: 23115.60 ✅
- **TP 3.5RR**: 23092.35 ✅
- **TP 4RR**: 23069.11 ✅
- **TP 4.5RR**: 23045.87 ❌
- **TP 5RR**: 23022.62 ❌
- **PnL**: -46.49 points (-1.0R)
- **MFE**: 193.40 points
- **MAE**: 47.47 points

### Trade #992 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-16 10:15:00
- **FVG 5m**: 23213.40 - 23224.25
- **Entrée**: 23234.10 @ 2025-07-16 10:55:00
- **Stop Loss**: 23201.79
- **Risk**: 32.31 points
- **TP 1RR**: 23266.41 ❌
- **TP 1.5RR**: 23282.57 ❌
- **TP 2RR**: 23298.72 ❌
- **TP 2.5RR**: 23314.88 ❌
- **TP 3RR**: 23331.03 ❌
- **TP 3.5RR**: 23347.18 ❌
- **TP 4RR**: 23363.34 ❌
- **TP 4.5RR**: 23379.49 ❌
- **TP 5RR**: 23395.65 ❌
- **PnL**: -32.31 points (-1.0R)
- **MFE**: 18.18 points
- **MAE**: 35.35 points

### Trade #993 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 02:00:00
- **FVG 5m**: 23526.97 - 23533.54
- **Entrée**: 23516.37 @ 2025-07-18 02:01:00
- **Stop Loss**: 23545.30
- **Risk**: 28.94 points
- **TP 1RR**: 23487.43 ✅
- **TP 1.5RR**: 23472.97 ❌
- **TP 2RR**: 23458.50 ❌
- **TP 2.5RR**: 23444.03 ❌
- **TP 3RR**: 23429.56 ❌
- **TP 3.5RR**: 23415.10 ❌
- **TP 4RR**: 23400.63 ❌
- **TP 4.5RR**: 23386.16 ❌
- **TP 5RR**: 23371.69 ❌
- **PnL**: -28.94 points (-1.0R)
- **MFE**: 34.84 points
- **MAE**: 35.35 points

### Trade #994 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 02:00:00
- **FVG 5m**: 23526.97 - 23533.54
- **Entrée**: 23516.37 @ 2025-07-18 02:01:00
- **Stop Loss**: 23545.30
- **Risk**: 28.94 points
- **TP 1RR**: 23487.43 ✅
- **TP 1.5RR**: 23472.97 ❌
- **TP 2RR**: 23458.50 ❌
- **TP 2.5RR**: 23444.03 ❌
- **TP 3RR**: 23429.56 ❌
- **TP 3.5RR**: 23415.10 ❌
- **TP 4RR**: 23400.63 ❌
- **TP 4.5RR**: 23386.16 ❌
- **TP 5RR**: 23371.69 ❌
- **PnL**: -28.94 points (-1.0R)
- **MFE**: 34.84 points
- **MAE**: 35.35 points

### Trade #995 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 02:00:00
- **FVG 5m**: 23526.97 - 23533.54
- **Entrée**: 23516.37 @ 2025-07-18 02:01:00
- **Stop Loss**: 23545.30
- **Risk**: 28.94 points
- **TP 1RR**: 23487.43 ✅
- **TP 1.5RR**: 23472.97 ❌
- **TP 2RR**: 23458.50 ❌
- **TP 2.5RR**: 23444.03 ❌
- **TP 3RR**: 23429.56 ❌
- **TP 3.5RR**: 23415.10 ❌
- **TP 4RR**: 23400.63 ❌
- **TP 4.5RR**: 23386.16 ❌
- **TP 5RR**: 23371.69 ❌
- **PnL**: -28.94 points (-1.0R)
- **MFE**: 34.84 points
- **MAE**: 35.35 points

### Trade #996 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 08:30:00
- **FVG 5m**: 23501.98 - 23506.02
- **Entrée**: 23491.37 @ 2025-07-18 08:38:00
- **Stop Loss**: 23517.77
- **Risk**: 26.40 points
- **TP 1RR**: 23464.98 ❌
- **TP 1.5RR**: 23451.78 ❌
- **TP 2RR**: 23438.58 ❌
- **TP 2.5RR**: 23425.38 ❌
- **TP 3RR**: 23412.18 ❌
- **TP 3.5RR**: 23398.99 ❌
- **TP 4RR**: 23385.79 ❌
- **TP 4.5RR**: 23372.59 ❌
- **TP 5RR**: 23359.39 ❌
- **PnL**: -26.40 points (-1.0R)
- **MFE**: 3.79 points
- **MAE**: 27.01 points

### Trade #997 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 08:30:00
- **FVG 5m**: 23501.98 - 23506.02
- **Entrée**: 23491.37 @ 2025-07-18 08:38:00
- **Stop Loss**: 23517.77
- **Risk**: 26.40 points
- **TP 1RR**: 23464.98 ❌
- **TP 1.5RR**: 23451.78 ❌
- **TP 2RR**: 23438.58 ❌
- **TP 2.5RR**: 23425.38 ❌
- **TP 3RR**: 23412.18 ❌
- **TP 3.5RR**: 23398.99 ❌
- **TP 4RR**: 23385.79 ❌
- **TP 4.5RR**: 23372.59 ❌
- **TP 5RR**: 23359.39 ❌
- **PnL**: -26.40 points (-1.0R)
- **MFE**: 3.79 points
- **MAE**: 27.01 points

### Trade #998 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 08:30:00
- **FVG 5m**: 23501.98 - 23506.02
- **Entrée**: 23491.37 @ 2025-07-18 08:38:00
- **Stop Loss**: 23517.77
- **Risk**: 26.40 points
- **TP 1RR**: 23464.98 ❌
- **TP 1.5RR**: 23451.78 ❌
- **TP 2RR**: 23438.58 ❌
- **TP 2.5RR**: 23425.38 ❌
- **TP 3RR**: 23412.18 ❌
- **TP 3.5RR**: 23398.99 ❌
- **TP 4RR**: 23385.79 ❌
- **TP 4.5RR**: 23372.59 ❌
- **TP 5RR**: 23359.39 ❌
- **PnL**: -26.40 points (-1.0R)
- **MFE**: 3.79 points
- **MAE**: 27.01 points

### Trade #999 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 09:15:00
- **FVG 5m**: 23501.98 - 23506.02
- **Entrée**: 23449.97 @ 2025-07-18 09:16:00
- **Stop Loss**: 23517.77
- **Risk**: 67.80 points
- **TP 1RR**: 23382.17 ❌
- **TP 1.5RR**: 23348.26 ❌
- **TP 2RR**: 23314.36 ❌
- **TP 2.5RR**: 23280.46 ❌
- **TP 3RR**: 23246.56 ❌
- **TP 3.5RR**: 23212.66 ❌
- **TP 4RR**: 23178.76 ❌
- **TP 4.5RR**: 23144.86 ❌
- **TP 5RR**: 23110.95 ❌
- **PnL**: -67.80 points (-1.0R)
- **MFE**: 51.00 points
- **MAE**: 68.67 points

### Trade #1000 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-20 18:45:00
- **FVG 5m**: 23446.69 - 23450.98
- **Entrée**: 23476.98 @ 2025-07-20 18:46:00
- **Stop Loss**: 23434.96
- **Risk**: 42.02 points
- **TP 1RR**: 23519.00 ✅
- **TP 1.5RR**: 23540.01 ✅
- **TP 2RR**: 23561.02 ✅
- **TP 2.5RR**: 23582.03 ✅
- **TP 3RR**: 23603.04 ✅
- **TP 3.5RR**: 23624.05 ✅
- **TP 4RR**: 23645.06 ✅
- **TP 4.5RR**: 23666.07 ❌
- **TP 5RR**: 23687.08 ❌
- **PnL**: -42.02 points (-1.0R)
- **MFE**: 179.76 points
- **MAE**: 43.17 points

### Trade #1001 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-21 08:15:00
- **FVG 5m**: 23472.94 - 23481.27
- **Entrée**: 23482.28 @ 2025-07-21 08:27:00
- **Stop Loss**: 23461.21
- **Risk**: 21.08 points
- **TP 1RR**: 23503.36 ✅
- **TP 1.5RR**: 23513.90 ✅
- **TP 2RR**: 23524.44 ✅
- **TP 2.5RR**: 23534.98 ✅
- **TP 3RR**: 23545.52 ✅
- **TP 3.5RR**: 23556.06 ✅
- **TP 4RR**: 23566.60 ✅
- **TP 4.5RR**: 23577.14 ✅
- **TP 5RR**: 23587.68 ✅
- **PnL**: 105.39 points (5.0R)
- **MFE**: 120.18 points
- **MAE**: 3.79 points

### Trade #1002 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-21 08:15:00
- **FVG 5m**: 23472.94 - 23481.27
- **Entrée**: 23482.28 @ 2025-07-21 08:27:00
- **Stop Loss**: 23461.21
- **Risk**: 21.08 points
- **TP 1RR**: 23503.36 ✅
- **TP 1.5RR**: 23513.90 ✅
- **TP 2RR**: 23524.44 ✅
- **TP 2.5RR**: 23534.98 ✅
- **TP 3RR**: 23545.52 ✅
- **TP 3.5RR**: 23556.06 ✅
- **TP 4RR**: 23566.60 ✅
- **TP 4.5RR**: 23577.14 ✅
- **TP 5RR**: 23587.68 ✅
- **PnL**: 105.39 points (5.0R)
- **MFE**: 120.18 points
- **MAE**: 3.79 points

### Trade #1003 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-21 08:30:00
- **FVG 5m**: 23472.94 - 23481.27
- **Entrée**: 23520.66 @ 2025-07-21 08:31:00
- **Stop Loss**: 23461.21
- **Risk**: 59.45 points
- **TP 1RR**: 23580.12 ✅
- **TP 1.5RR**: 23609.84 ✅
- **TP 2RR**: 23639.57 ✅
- **TP 2.5RR**: 23669.30 ❌
- **TP 3RR**: 23699.02 ❌
- **TP 3.5RR**: 23728.75 ❌
- **TP 4RR**: 23758.48 ❌
- **TP 4.5RR**: 23788.21 ❌
- **TP 5RR**: 23817.93 ❌
- **PnL**: -59.45 points (-1.0R)
- **MFE**: 136.08 points
- **MAE**: 64.13 points

### Trade #1004 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23548.94 - 23553.99
- **Entrée**: 23548.69 @ 2025-07-22 02:54:00
- **Stop Loss**: 23565.76
- **Risk**: 17.08 points
- **TP 1RR**: 23531.61 ✅
- **TP 1.5RR**: 23523.07 ✅
- **TP 2RR**: 23514.53 ✅
- **TP 2.5RR**: 23505.99 ✅
- **TP 3RR**: 23497.45 ❌
- **TP 3.5RR**: 23488.91 ❌
- **TP 4RR**: 23480.37 ❌
- **TP 4.5RR**: 23471.83 ❌
- **TP 5RR**: 23463.29 ❌
- **PnL**: -17.08 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 17.17 points

### Trade #1005 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23548.94 - 23553.99
- **Entrée**: 23548.69 @ 2025-07-22 02:54:00
- **Stop Loss**: 23565.76
- **Risk**: 17.08 points
- **TP 1RR**: 23531.61 ✅
- **TP 1.5RR**: 23523.07 ✅
- **TP 2RR**: 23514.53 ✅
- **TP 2.5RR**: 23505.99 ✅
- **TP 3RR**: 23497.45 ❌
- **TP 3.5RR**: 23488.91 ❌
- **TP 4RR**: 23480.37 ❌
- **TP 4.5RR**: 23471.83 ❌
- **TP 5RR**: 23463.29 ❌
- **PnL**: -17.08 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 17.17 points

### Trade #1006 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23548.94 - 23553.99
- **Entrée**: 23548.69 @ 2025-07-22 02:54:00
- **Stop Loss**: 23565.76
- **Risk**: 17.08 points
- **TP 1RR**: 23531.61 ✅
- **TP 1.5RR**: 23523.07 ✅
- **TP 2RR**: 23514.53 ✅
- **TP 2.5RR**: 23505.99 ✅
- **TP 3RR**: 23497.45 ❌
- **TP 3.5RR**: 23488.91 ❌
- **TP 4RR**: 23480.37 ❌
- **TP 4.5RR**: 23471.83 ❌
- **TP 5RR**: 23463.29 ❌
- **PnL**: -17.08 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 17.17 points

### Trade #1007 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 03:45:00
- **FVG 5m**: 23548.94 - 23553.99
- **Entrée**: 23510.31 @ 2025-07-22 03:46:00
- **Stop Loss**: 23565.76
- **Risk**: 55.46 points
- **TP 1RR**: 23454.85 ❌
- **TP 1.5RR**: 23427.13 ❌
- **TP 2RR**: 23399.40 ❌
- **TP 2.5RR**: 23371.67 ❌
- **TP 3RR**: 23343.94 ❌
- **TP 3.5RR**: 23316.22 ❌
- **TP 4RR**: 23288.49 ❌
- **TP 4.5RR**: 23260.76 ❌
- **TP 5RR**: 23233.03 ❌
- **PnL**: -55.46 points (-1.0R)
- **MFE**: 12.37 points
- **MAE**: 55.54 points

### Trade #1008 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 08:45:00
- **FVG 5m**: 23541.62 - 23547.93
- **Entrée**: 23462.59 @ 2025-07-22 08:46:00
- **Stop Loss**: 23559.70
- **Risk**: 97.11 points
- **TP 1RR**: 23365.48 ✅
- **TP 1.5RR**: 23316.93 ❌
- **TP 2RR**: 23268.37 ❌
- **TP 2.5RR**: 23219.81 ❌
- **TP 3RR**: 23171.26 ❌
- **TP 3.5RR**: 23122.70 ❌
- **TP 4RR**: 23074.15 ❌
- **TP 4.5RR**: 23025.59 ❌
- **TP 5RR**: 22977.04 ❌
- **PnL**: -97.11 points (-1.0R)
- **MFE**: 125.73 points
- **MAE**: 157.04 points

### Trade #1009 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 08:45:00
- **FVG 5m**: 23541.62 - 23547.93
- **Entrée**: 23462.59 @ 2025-07-22 08:46:00
- **Stop Loss**: 23559.70
- **Risk**: 97.11 points
- **TP 1RR**: 23365.48 ✅
- **TP 1.5RR**: 23316.93 ❌
- **TP 2RR**: 23268.37 ❌
- **TP 2.5RR**: 23219.81 ❌
- **TP 3RR**: 23171.26 ❌
- **TP 3.5RR**: 23122.70 ❌
- **TP 4RR**: 23074.15 ❌
- **TP 4.5RR**: 23025.59 ❌
- **TP 5RR**: 22977.04 ❌
- **PnL**: -97.11 points (-1.0R)
- **MFE**: 125.73 points
- **MAE**: 157.04 points

### Trade #1010 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 09:00:00
- **FVG 5m**: 23402.25 - 23440.37
- **Entrée**: 23448.45 @ 2025-07-22 09:35:00
- **Stop Loss**: 23390.55
- **Risk**: 57.90 points
- **TP 1RR**: 23506.36 ❌
- **TP 1.5RR**: 23535.31 ❌
- **TP 2RR**: 23564.26 ❌
- **TP 2.5RR**: 23593.21 ❌
- **TP 3RR**: 23622.17 ❌
- **TP 3.5RR**: 23651.12 ❌
- **TP 4RR**: 23680.07 ❌
- **TP 4.5RR**: 23709.02 ❌
- **TP 5RR**: 23737.97 ❌
- **PnL**: -57.90 points (-1.0R)
- **MFE**: 18.94 points
- **MAE**: 59.58 points

### Trade #1011 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 09:30:00
- **FVG 5m**: 23402.25 - 23440.37
- **Entrée**: 23448.45 @ 2025-07-22 09:35:00
- **Stop Loss**: 23390.55
- **Risk**: 57.90 points
- **TP 1RR**: 23506.36 ❌
- **TP 1.5RR**: 23535.31 ❌
- **TP 2RR**: 23564.26 ❌
- **TP 2.5RR**: 23593.21 ❌
- **TP 3RR**: 23622.17 ❌
- **TP 3.5RR**: 23651.12 ❌
- **TP 4RR**: 23680.07 ❌
- **TP 4.5RR**: 23709.02 ❌
- **TP 5RR**: 23737.97 ❌
- **PnL**: -57.90 points (-1.0R)
- **MFE**: 18.94 points
- **MAE**: 59.58 points

### Trade #1012 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 09:45:00
- **FVG 5m**: 23402.25 - 23440.37
- **Entrée**: 23445.93 @ 2025-07-22 09:46:00
- **Stop Loss**: 23390.55
- **Risk**: 55.38 points
- **TP 1RR**: 23501.31 ❌
- **TP 1.5RR**: 23529.00 ❌
- **TP 2RR**: 23556.69 ❌
- **TP 2.5RR**: 23584.38 ❌
- **TP 3RR**: 23612.07 ❌
- **TP 3.5RR**: 23639.76 ❌
- **TP 4RR**: 23667.45 ❌
- **TP 4.5RR**: 23695.14 ❌
- **TP 5RR**: 23722.83 ❌
- **PnL**: -55.38 points (-1.0R)
- **MFE**: 21.46 points
- **MAE**: 57.06 points

### Trade #1013 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 12:15:00
- **FVG 5m**: 23419.67 - 23432.29
- **Entrée**: 23437.85 @ 2025-07-22 12:16:00
- **Stop Loss**: 23407.96
- **Risk**: 29.89 points
- **TP 1RR**: 23467.74 ✅
- **TP 1.5RR**: 23482.68 ❌
- **TP 2RR**: 23497.63 ❌
- **TP 2.5RR**: 23512.57 ❌
- **TP 3RR**: 23527.51 ❌
- **TP 3.5RR**: 23542.46 ❌
- **TP 4RR**: 23557.40 ❌
- **TP 4.5RR**: 23572.35 ❌
- **TP 5RR**: 23587.29 ❌
- **PnL**: -29.89 points (-1.0R)
- **MFE**: 43.17 points
- **MAE**: 37.37 points

### Trade #1014 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 12:15:00
- **FVG 5m**: 23419.67 - 23432.29
- **Entrée**: 23437.85 @ 2025-07-22 12:16:00
- **Stop Loss**: 23407.96
- **Risk**: 29.89 points
- **TP 1RR**: 23467.74 ✅
- **TP 1.5RR**: 23482.68 ❌
- **TP 2RR**: 23497.63 ❌
- **TP 2.5RR**: 23512.57 ❌
- **TP 3RR**: 23527.51 ❌
- **TP 3.5RR**: 23542.46 ❌
- **TP 4RR**: 23557.40 ❌
- **TP 4.5RR**: 23572.35 ❌
- **TP 5RR**: 23587.29 ❌
- **PnL**: -29.89 points (-1.0R)
- **MFE**: 43.17 points
- **MAE**: 37.37 points

### Trade #1015 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 14:00:00
- **FVG 5m**: 23472.69 - 23475.47
- **Entrée**: 23472.19 @ 2025-07-22 14:04:00
- **Stop Loss**: 23487.21
- **Risk**: 15.02 points
- **TP 1RR**: 23457.17 ✅
- **TP 1.5RR**: 23449.66 ✅
- **TP 2RR**: 23442.15 ✅
- **TP 2.5RR**: 23434.64 ✅
- **TP 3RR**: 23427.13 ✅
- **TP 3.5RR**: 23419.62 ✅
- **TP 4RR**: 23412.11 ✅
- **TP 4.5RR**: 23404.60 ✅
- **TP 5RR**: 23397.09 ❌
- **PnL**: -15.02 points (-1.0R)
- **MFE**: 72.46 points
- **MAE**: 20.45 points

### Trade #1016 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 19:00:00
- **FVG 5m**: 23476.48 - 23485.57
- **Entrée**: 23474.21 @ 2025-07-22 19:03:00
- **Stop Loss**: 23497.31
- **Risk**: 23.10 points
- **TP 1RR**: 23451.10 ✅
- **TP 1.5RR**: 23439.55 ✅
- **TP 2RR**: 23428.00 ❌
- **TP 2.5RR**: 23416.44 ❌
- **TP 3RR**: 23404.89 ❌
- **TP 3.5RR**: 23393.34 ❌
- **TP 4RR**: 23381.79 ❌
- **TP 4.5RR**: 23370.24 ❌
- **TP 5RR**: 23358.68 ❌
- **PnL**: -23.10 points (-1.0R)
- **MFE**: 45.95 points
- **MAE**: 25.25 points

### Trade #1017 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 08:15:00
- **FVG 5m**: 23482.03 - 23485.31
- **Entrée**: 23493.39 @ 2025-07-23 08:23:00
- **Stop Loss**: 23470.29
- **Risk**: 23.10 points
- **TP 1RR**: 23516.50 ❌
- **TP 1.5RR**: 23528.05 ❌
- **TP 2RR**: 23539.60 ❌
- **TP 2.5RR**: 23551.15 ❌
- **TP 3RR**: 23562.70 ❌
- **TP 3.5RR**: 23574.25 ❌
- **TP 4RR**: 23585.80 ❌
- **TP 4.5RR**: 23597.35 ❌
- **TP 5RR**: 23608.91 ❌
- **PnL**: -23.10 points (-1.0R)
- **MFE**: 7.83 points
- **MAE**: 39.89 points

### Trade #1018 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 09:45:00
- **FVG 5m**: 23400.99 - 23404.27
- **Entrée**: 23408.06 @ 2025-07-23 09:46:00
- **Stop Loss**: 23389.29
- **Risk**: 18.77 points
- **TP 1RR**: 23426.83 ✅
- **TP 1.5RR**: 23436.21 ✅
- **TP 2RR**: 23445.60 ✅
- **TP 2.5RR**: 23454.98 ✅
- **TP 3RR**: 23464.37 ✅
- **TP 3.5RR**: 23473.75 ✅
- **TP 4RR**: 23483.14 ✅
- **TP 4.5RR**: 23492.52 ✅
- **TP 5RR**: 23501.91 ✅
- **PnL**: 93.85 points (5.0R)
- **MFE**: 111.59 points
- **MAE**: 6.82 points

### Trade #1019 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23400.99 - 23404.27
- **Entrée**: 23435.32 @ 2025-07-23 10:46:00
- **Stop Loss**: 23389.29
- **Risk**: 46.04 points
- **TP 1RR**: 23481.36 ✅
- **TP 1.5RR**: 23504.38 ✅
- **TP 2RR**: 23527.40 ✅
- **TP 2.5RR**: 23550.42 ✅
- **TP 3RR**: 23573.44 ✅
- **TP 3.5RR**: 23596.45 ✅
- **TP 4RR**: 23619.47 ✅
- **TP 4.5RR**: 23642.49 ✅
- **TP 5RR**: 23665.51 ✅
- **PnL**: 230.19 points (5.0R)
- **MFE**: 231.52 points
- **MAE**: 12.88 points

### Trade #1020 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23400.99 - 23404.27
- **Entrée**: 23435.32 @ 2025-07-23 10:46:00
- **Stop Loss**: 23389.29
- **Risk**: 46.04 points
- **TP 1RR**: 23481.36 ✅
- **TP 1.5RR**: 23504.38 ✅
- **TP 2RR**: 23527.40 ✅
- **TP 2.5RR**: 23550.42 ✅
- **TP 3RR**: 23573.44 ✅
- **TP 3.5RR**: 23596.45 ✅
- **TP 4RR**: 23619.47 ✅
- **TP 4.5RR**: 23642.49 ✅
- **TP 5RR**: 23665.51 ✅
- **PnL**: 230.19 points (5.0R)
- **MFE**: 231.52 points
- **MAE**: 12.88 points

### Trade #1021 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23400.99 - 23404.27
- **Entrée**: 23435.32 @ 2025-07-23 10:46:00
- **Stop Loss**: 23389.29
- **Risk**: 46.04 points
- **TP 1RR**: 23481.36 ✅
- **TP 1.5RR**: 23504.38 ✅
- **TP 2RR**: 23527.40 ✅
- **TP 2.5RR**: 23550.42 ✅
- **TP 3RR**: 23573.44 ✅
- **TP 3.5RR**: 23596.45 ✅
- **TP 4RR**: 23619.47 ✅
- **TP 4.5RR**: 23642.49 ✅
- **TP 5RR**: 23665.51 ✅
- **PnL**: 230.19 points (5.0R)
- **MFE**: 231.52 points
- **MAE**: 12.88 points

### Trade #1022 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 01:30:00
- **FVG 5m**: 23611.05 - 23614.08
- **Entrée**: 23602.72 @ 2025-07-24 01:31:00
- **Stop Loss**: 23625.88
- **Risk**: 23.17 points
- **TP 1RR**: 23579.55 ✅
- **TP 1.5RR**: 23567.96 ❌
- **TP 2RR**: 23556.38 ❌
- **TP 2.5RR**: 23544.79 ❌
- **TP 3RR**: 23533.21 ❌
- **TP 3.5RR**: 23521.63 ❌
- **TP 4RR**: 23510.04 ❌
- **TP 4.5RR**: 23498.46 ❌
- **TP 5RR**: 23486.87 ❌
- **PnL**: -23.17 points (-1.0R)
- **MFE**: 24.74 points
- **MAE**: 25.00 points

### Trade #1023 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 07:45:00
- **FVG 5m**: 23614.58 - 23617.36
- **Entrée**: 23622.16 @ 2025-07-24 08:30:00
- **Stop Loss**: 23602.77
- **Risk**: 19.38 points
- **TP 1RR**: 23641.54 ❌
- **TP 1.5RR**: 23651.23 ❌
- **TP 2RR**: 23660.92 ❌
- **TP 2.5RR**: 23670.61 ❌
- **TP 3RR**: 23680.30 ❌
- **TP 3.5RR**: 23689.99 ❌
- **TP 4RR**: 23699.68 ❌
- **TP 4.5RR**: 23709.37 ❌
- **TP 5RR**: 23719.06 ❌
- **PnL**: -19.38 points (-1.0R)
- **MFE**: 3.03 points
- **MAE**: 41.66 points

### Trade #1024 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 08:15:00
- **FVG 5m**: 23581.26 - 23586.30
- **Entrée**: 23588.83 @ 2025-07-24 08:17:00
- **Stop Loss**: 23569.46
- **Risk**: 19.36 points
- **TP 1RR**: 23608.19 ✅
- **TP 1.5RR**: 23617.88 ✅
- **TP 2RR**: 23627.56 ✅
- **TP 2.5RR**: 23637.24 ❌
- **TP 3RR**: 23646.92 ❌
- **TP 3.5RR**: 23656.61 ❌
- **TP 4RR**: 23666.29 ❌
- **TP 4.5RR**: 23675.97 ❌
- **TP 5RR**: 23685.65 ❌
- **PnL**: -19.36 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 20.70 points

### Trade #1025 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 08:15:00
- **FVG 5m**: 23581.26 - 23586.30
- **Entrée**: 23588.83 @ 2025-07-24 08:17:00
- **Stop Loss**: 23569.46
- **Risk**: 19.36 points
- **TP 1RR**: 23608.19 ✅
- **TP 1.5RR**: 23617.88 ✅
- **TP 2RR**: 23627.56 ✅
- **TP 2.5RR**: 23637.24 ❌
- **TP 3RR**: 23646.92 ❌
- **TP 3.5RR**: 23656.61 ❌
- **TP 4RR**: 23666.29 ❌
- **TP 4.5RR**: 23675.97 ❌
- **TP 5RR**: 23685.65 ❌
- **PnL**: -19.36 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 20.70 points

### Trade #1026 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 09:00:00
- **FVG 5m**: 23590.34 - 23598.42
- **Entrée**: 23582.27 @ 2025-07-24 09:01:00
- **Stop Loss**: 23610.22
- **Risk**: 27.96 points
- **TP 1RR**: 23554.31 ✅
- **TP 1.5RR**: 23540.33 ✅
- **TP 2RR**: 23526.35 ❌
- **TP 2.5RR**: 23512.37 ❌
- **TP 3RR**: 23498.39 ❌
- **TP 3.5RR**: 23484.41 ❌
- **TP 4RR**: 23470.43 ❌
- **TP 4.5RR**: 23456.46 ❌
- **TP 5RR**: 23442.48 ❌
- **PnL**: -27.96 points (-1.0R)
- **MFE**: 53.27 points
- **MAE**: 29.54 points

### Trade #1027 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 12:00:00
- **FVG 5m**: 23588.32 - 23591.35
- **Entrée**: 23601.20 @ 2025-07-24 12:01:00
- **Stop Loss**: 23576.53
- **Risk**: 24.67 points
- **TP 1RR**: 23625.87 ✅
- **TP 1.5RR**: 23638.21 ✅
- **TP 2RR**: 23650.54 ✅
- **TP 2.5RR**: 23662.88 ✅
- **TP 3RR**: 23675.21 ❌
- **TP 3.5RR**: 23687.55 ❌
- **TP 4RR**: 23699.88 ❌
- **TP 4.5RR**: 23712.22 ❌
- **TP 5RR**: 23724.55 ❌
- **PnL**: -24.67 points (-1.0R)
- **MFE**: 72.71 points
- **MAE**: 27.01 points

### Trade #1028 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-25 08:30:00
- **FVG 5m**: 23604.23 - 23607.77
- **Entrée**: 23608.27 @ 2025-07-25 08:47:00
- **Stop Loss**: 23592.43
- **Risk**: 15.84 points
- **TP 1RR**: 23624.11 ✅
- **TP 1.5RR**: 23632.03 ✅
- **TP 2RR**: 23639.95 ✅
- **TP 2.5RR**: 23647.87 ✅
- **TP 3RR**: 23655.80 ✅
- **TP 3.5RR**: 23663.72 ✅
- **TP 4RR**: 23671.64 ✅
- **TP 4.5RR**: 23679.56 ✅
- **TP 5RR**: 23687.48 ✅
- **PnL**: 79.21 points (5.0R)
- **MFE**: 81.04 points
- **MAE**: 3.79 points

### Trade #1029 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 08:45:00
- **FVG 5m**: 23602.97 - 23607.26
- **Entrée**: 23600.44 @ 2025-07-25 08:46:00
- **Stop Loss**: 23619.06
- **Risk**: 18.62 points
- **TP 1RR**: 23581.82 ❌
- **TP 1.5RR**: 23572.51 ❌
- **TP 2RR**: 23563.20 ❌
- **TP 2.5RR**: 23553.89 ❌
- **TP 3RR**: 23544.58 ❌
- **TP 3.5RR**: 23535.27 ❌
- **TP 4RR**: 23525.96 ❌
- **TP 4.5RR**: 23516.65 ❌
- **TP 5RR**: 23507.34 ❌
- **PnL**: -18.62 points (-1.0R)
- **MFE**: 5.05 points
- **MAE**: 25.25 points

### Trade #1030 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:15:00
- **FVG 5m**: 23678.96 - 23682.50
- **Entrée**: 23678.71 @ 2025-07-25 14:24:00
- **Stop Loss**: 23694.34
- **Risk**: 15.63 points
- **TP 1RR**: 23663.08 ✅
- **TP 1.5RR**: 23655.27 ✅
- **TP 2RR**: 23647.45 ✅
- **TP 2.5RR**: 23639.64 ✅
- **TP 3RR**: 23631.83 ❌
- **TP 3.5RR**: 23624.01 ❌
- **TP 4RR**: 23616.20 ❌
- **TP 4.5RR**: 23608.38 ❌
- **TP 5RR**: 23600.57 ❌
- **PnL**: -15.63 points (-1.0R)
- **MFE**: 39.89 points
- **MAE**: 112.86 points

### Trade #1031 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:45:00
- **FVG 5m**: 23678.96 - 23682.50
- **Entrée**: 23674.42 @ 2025-07-25 14:46:00
- **Stop Loss**: 23694.34
- **Risk**: 19.92 points
- **TP 1RR**: 23654.50 ✅
- **TP 1.5RR**: 23644.54 ✅
- **TP 2RR**: 23634.58 ❌
- **TP 2.5RR**: 23624.62 ❌
- **TP 3RR**: 23614.66 ❌
- **TP 3.5RR**: 23604.70 ❌
- **TP 4RR**: 23594.74 ❌
- **TP 4.5RR**: 23584.78 ❌
- **TP 5RR**: 23574.82 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 35.60 points
- **MAE**: 117.15 points

### Trade #1032 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:45:00
- **FVG 5m**: 23678.96 - 23682.50
- **Entrée**: 23674.42 @ 2025-07-25 14:46:00
- **Stop Loss**: 23694.34
- **Risk**: 19.92 points
- **TP 1RR**: 23654.50 ✅
- **TP 1.5RR**: 23644.54 ✅
- **TP 2RR**: 23634.58 ❌
- **TP 2.5RR**: 23624.62 ❌
- **TP 3RR**: 23614.66 ❌
- **TP 3.5RR**: 23604.70 ❌
- **TP 4RR**: 23594.74 ❌
- **TP 4.5RR**: 23584.78 ❌
- **TP 5RR**: 23574.82 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 35.60 points
- **MAE**: 117.15 points

### Trade #1033 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:45:00
- **FVG 5m**: 23678.96 - 23682.50
- **Entrée**: 23674.42 @ 2025-07-25 14:46:00
- **Stop Loss**: 23694.34
- **Risk**: 19.92 points
- **TP 1RR**: 23654.50 ✅
- **TP 1.5RR**: 23644.54 ✅
- **TP 2RR**: 23634.58 ❌
- **TP 2.5RR**: 23624.62 ❌
- **TP 3RR**: 23614.66 ❌
- **TP 3.5RR**: 23604.70 ❌
- **TP 4RR**: 23594.74 ❌
- **TP 4.5RR**: 23584.78 ❌
- **TP 5RR**: 23574.82 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 35.60 points
- **MAE**: 117.15 points

### Trade #1034 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:45:00
- **FVG 5m**: 23678.96 - 23682.50
- **Entrée**: 23674.42 @ 2025-07-25 14:46:00
- **Stop Loss**: 23694.34
- **Risk**: 19.92 points
- **TP 1RR**: 23654.50 ✅
- **TP 1.5RR**: 23644.54 ✅
- **TP 2RR**: 23634.58 ❌
- **TP 2.5RR**: 23624.62 ❌
- **TP 3RR**: 23614.66 ❌
- **TP 3.5RR**: 23604.70 ❌
- **TP 4RR**: 23594.74 ❌
- **TP 4.5RR**: 23584.78 ❌
- **TP 5RR**: 23574.82 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 35.60 points
- **MAE**: 117.15 points

### Trade #1035 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-25 15:00:00
- **FVG 5m**: 23659.52 - 23667.10
- **Entrée**: 23668.86 @ 2025-07-25 15:16:00
- **Stop Loss**: 23647.69
- **Risk**: 21.17 points
- **TP 1RR**: 23690.04 ✅
- **TP 1.5RR**: 23700.62 ✅
- **TP 2RR**: 23711.21 ✅
- **TP 2.5RR**: 23721.79 ✅
- **TP 3RR**: 23732.38 ✅
- **TP 3.5RR**: 23742.96 ✅
- **TP 4RR**: 23753.55 ✅
- **TP 4.5RR**: 23764.14 ✅
- **TP 5RR**: 23774.72 ✅
- **PnL**: 105.86 points (5.0R)
- **MFE**: 122.70 points
- **MAE**: 7.32 points

### Trade #1036 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-28 08:30:00
- **FVG 5m**: 23720.12 - 23728.95
- **Entrée**: 23729.96 @ 2025-07-28 08:35:00
- **Stop Loss**: 23708.26
- **Risk**: 21.71 points
- **TP 1RR**: 23751.67 ❌
- **TP 1.5RR**: 23762.52 ❌
- **TP 2RR**: 23773.38 ❌
- **TP 2.5RR**: 23784.23 ❌
- **TP 3RR**: 23795.08 ❌
- **TP 3.5RR**: 23805.94 ❌
- **TP 4RR**: 23816.79 ❌
- **TP 4.5RR**: 23827.64 ❌
- **TP 5RR**: 23838.50 ❌
- **PnL**: -21.71 points (-1.0R)
- **MFE**: 7.83 points
- **MAE**: 26.51 points

### Trade #1037 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-28 10:15:00
- **FVG 5m**: 23720.12 - 23728.95
- **Entrée**: 23730.97 @ 2025-07-28 10:52:00
- **Stop Loss**: 23708.26
- **Risk**: 22.72 points
- **TP 1RR**: 23753.69 ❌
- **TP 1.5RR**: 23765.05 ❌
- **TP 2RR**: 23776.41 ❌
- **TP 2.5RR**: 23787.76 ❌
- **TP 3RR**: 23799.12 ❌
- **TP 3.5RR**: 23810.48 ❌
- **TP 4RR**: 23821.84 ❌
- **TP 4.5RR**: 23833.20 ❌
- **TP 5RR**: 23844.56 ❌
- **PnL**: -22.72 points (-1.0R)
- **MFE**: 1.77 points
- **MAE**: 23.99 points

### Trade #1038 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23823.38 @ 2025-07-29 08:49:00
- **Stop Loss**: 23871.67
- **Risk**: 48.29 points
- **TP 1RR**: 23775.09 ✅
- **TP 1.5RR**: 23750.95 ✅
- **TP 2RR**: 23726.81 ✅
- **TP 2.5RR**: 23702.66 ✅
- **TP 3RR**: 23678.52 ✅
- **TP 3.5RR**: 23654.38 ✅
- **TP 4RR**: 23630.23 ✅
- **TP 4.5RR**: 23606.09 ✅
- **TP 5RR**: 23581.95 ❌
- **PnL**: -48.29 points (-1.0R)
- **MFE**: 235.56 points
- **MAE**: 51.51 points

### Trade #1039 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23823.38 @ 2025-07-29 08:49:00
- **Stop Loss**: 23871.67
- **Risk**: 48.29 points
- **TP 1RR**: 23775.09 ✅
- **TP 1.5RR**: 23750.95 ✅
- **TP 2RR**: 23726.81 ✅
- **TP 2.5RR**: 23702.66 ✅
- **TP 3RR**: 23678.52 ✅
- **TP 3.5RR**: 23654.38 ✅
- **TP 4RR**: 23630.23 ✅
- **TP 4.5RR**: 23606.09 ✅
- **TP 5RR**: 23581.95 ❌
- **PnL**: -48.29 points (-1.0R)
- **MFE**: 235.56 points
- **MAE**: 51.51 points

### Trade #1040 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23823.38 @ 2025-07-29 08:49:00
- **Stop Loss**: 23871.67
- **Risk**: 48.29 points
- **TP 1RR**: 23775.09 ✅
- **TP 1.5RR**: 23750.95 ✅
- **TP 2RR**: 23726.81 ✅
- **TP 2.5RR**: 23702.66 ✅
- **TP 3RR**: 23678.52 ✅
- **TP 3.5RR**: 23654.38 ✅
- **TP 4RR**: 23630.23 ✅
- **TP 4.5RR**: 23606.09 ✅
- **TP 5RR**: 23581.95 ❌
- **PnL**: -48.29 points (-1.0R)
- **MFE**: 235.56 points
- **MAE**: 51.51 points

### Trade #1041 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23823.38 @ 2025-07-29 08:49:00
- **Stop Loss**: 23871.67
- **Risk**: 48.29 points
- **TP 1RR**: 23775.09 ✅
- **TP 1.5RR**: 23750.95 ✅
- **TP 2RR**: 23726.81 ✅
- **TP 2.5RR**: 23702.66 ✅
- **TP 3RR**: 23678.52 ✅
- **TP 3.5RR**: 23654.38 ✅
- **TP 4RR**: 23630.23 ✅
- **TP 4.5RR**: 23606.09 ✅
- **TP 5RR**: 23581.95 ❌
- **PnL**: -48.29 points (-1.0R)
- **MFE**: 235.56 points
- **MAE**: 51.51 points

### Trade #1042 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:15:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23803.69 @ 2025-07-29 09:16:00
- **Stop Loss**: 23871.67
- **Risk**: 67.98 points
- **TP 1RR**: 23735.71 ✅
- **TP 1.5RR**: 23701.72 ✅
- **TP 2RR**: 23667.73 ✅
- **TP 2.5RR**: 23633.74 ✅
- **TP 3RR**: 23599.75 ✅
- **TP 3.5RR**: 23565.76 ❌
- **TP 4RR**: 23531.77 ❌
- **TP 4.5RR**: 23497.78 ❌
- **TP 5RR**: 23463.79 ❌
- **PnL**: -67.98 points (-1.0R)
- **MFE**: 215.87 points
- **MAE**: 71.20 points

### Trade #1043 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:30:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23791.06 @ 2025-07-29 09:31:00
- **Stop Loss**: 23871.67
- **Risk**: 80.60 points
- **TP 1RR**: 23710.46 ✅
- **TP 1.5RR**: 23670.16 ✅
- **TP 2RR**: 23629.86 ✅
- **TP 2.5RR**: 23589.55 ✅
- **TP 3RR**: 23549.25 ❌
- **TP 3.5RR**: 23508.95 ❌
- **TP 4RR**: 23468.65 ❌
- **TP 4.5RR**: 23428.35 ❌
- **TP 5RR**: 23388.05 ❌
- **PnL**: -80.60 points (-1.0R)
- **MFE**: 203.24 points
- **MAE**: 83.82 points

### Trade #1044 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:30:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23791.06 @ 2025-07-29 09:31:00
- **Stop Loss**: 23871.67
- **Risk**: 80.60 points
- **TP 1RR**: 23710.46 ✅
- **TP 1.5RR**: 23670.16 ✅
- **TP 2RR**: 23629.86 ✅
- **TP 2.5RR**: 23589.55 ✅
- **TP 3RR**: 23549.25 ❌
- **TP 3.5RR**: 23508.95 ❌
- **TP 4RR**: 23468.65 ❌
- **TP 4.5RR**: 23428.35 ❌
- **TP 5RR**: 23388.05 ❌
- **PnL**: -80.60 points (-1.0R)
- **MFE**: 203.24 points
- **MAE**: 83.82 points

### Trade #1045 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:45:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23797.37 @ 2025-07-29 09:46:00
- **Stop Loss**: 23871.67
- **Risk**: 74.29 points
- **TP 1RR**: 23723.08 ✅
- **TP 1.5RR**: 23685.94 ✅
- **TP 2RR**: 23648.79 ✅
- **TP 2.5RR**: 23611.65 ✅
- **TP 3RR**: 23574.50 ❌
- **TP 3.5RR**: 23537.35 ❌
- **TP 4RR**: 23500.21 ❌
- **TP 4.5RR**: 23463.06 ❌
- **TP 5RR**: 23425.92 ❌
- **PnL**: -74.29 points (-1.0R)
- **MFE**: 209.56 points
- **MAE**: 77.51 points

### Trade #1046 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:45:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23797.37 @ 2025-07-29 09:46:00
- **Stop Loss**: 23871.67
- **Risk**: 74.29 points
- **TP 1RR**: 23723.08 ✅
- **TP 1.5RR**: 23685.94 ✅
- **TP 2RR**: 23648.79 ✅
- **TP 2.5RR**: 23611.65 ✅
- **TP 3RR**: 23574.50 ❌
- **TP 3.5RR**: 23537.35 ❌
- **TP 4RR**: 23500.21 ❌
- **TP 4.5RR**: 23463.06 ❌
- **TP 5RR**: 23425.92 ❌
- **PnL**: -74.29 points (-1.0R)
- **MFE**: 209.56 points
- **MAE**: 77.51 points

### Trade #1047 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:45:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23797.37 @ 2025-07-29 09:46:00
- **Stop Loss**: 23871.67
- **Risk**: 74.29 points
- **TP 1RR**: 23723.08 ✅
- **TP 1.5RR**: 23685.94 ✅
- **TP 2RR**: 23648.79 ✅
- **TP 2.5RR**: 23611.65 ✅
- **TP 3RR**: 23574.50 ❌
- **TP 3.5RR**: 23537.35 ❌
- **TP 4RR**: 23500.21 ❌
- **TP 4.5RR**: 23463.06 ❌
- **TP 5RR**: 23425.92 ❌
- **PnL**: -74.29 points (-1.0R)
- **MFE**: 209.56 points
- **MAE**: 77.51 points

### Trade #1048 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 10:15:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23736.53 @ 2025-07-29 10:16:00
- **Stop Loss**: 23871.67
- **Risk**: 135.14 points
- **TP 1RR**: 23601.39 ✅
- **TP 1.5RR**: 23533.82 ❌
- **TP 2RR**: 23466.25 ❌
- **TP 2.5RR**: 23398.68 ❌
- **TP 3RR**: 23331.11 ❌
- **TP 3.5RR**: 23263.54 ❌
- **TP 4RR**: 23195.98 ❌
- **TP 4.5RR**: 23128.41 ❌
- **TP 5RR**: 23060.84 ❌
- **PnL**: -135.14 points (-1.0R)
- **MFE**: 148.71 points
- **MAE**: 138.36 points

### Trade #1049 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 10:30:00
- **FVG 5m**: 23835.75 - 23859.74
- **Entrée**: 23688.05 @ 2025-07-29 10:31:00
- **Stop Loss**: 23871.67
- **Risk**: 183.61 points
- **TP 1RR**: 23504.44 ❌
- **TP 1.5RR**: 23412.63 ❌
- **TP 2RR**: 23320.83 ❌
- **TP 2.5RR**: 23229.02 ❌
- **TP 3RR**: 23137.21 ❌
- **TP 3.5RR**: 23045.41 ❌
- **TP 4RR**: 22953.60 ❌
- **TP 4.5RR**: 22861.79 ❌
- **TP 5RR**: 22769.98 ❌
- **PnL**: -183.61 points (-1.0R)
- **MFE**: 100.23 points
- **MAE**: 186.83 points

### Trade #1050 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 12:15:00
- **FVG 5m**: 23720.62 - 23732.24
- **Entrée**: 23715.57 @ 2025-07-29 12:41:00
- **Stop Loss**: 23744.10
- **Risk**: 28.53 points
- **TP 1RR**: 23687.04 ✅
- **TP 1.5RR**: 23672.78 ✅
- **TP 2RR**: 23658.51 ✅
- **TP 2.5RR**: 23644.25 ❌
- **TP 3RR**: 23629.98 ❌
- **TP 3.5RR**: 23615.72 ❌
- **TP 4RR**: 23601.45 ❌
- **TP 4.5RR**: 23587.19 ❌
- **TP 5RR**: 23572.92 ❌
- **PnL**: -28.53 points (-1.0R)
- **MFE**: 62.36 points
- **MAE**: 29.79 points

### Trade #1051 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 02:15:00
- **FVG 5m**: 23719.86 - 23726.43
- **Entrée**: 23727.44 @ 2025-07-30 02:30:00
- **Stop Loss**: 23708.00
- **Risk**: 19.43 points
- **TP 1RR**: 23746.87 ❌
- **TP 1.5RR**: 23756.59 ❌
- **TP 2RR**: 23766.31 ❌
- **TP 2.5RR**: 23776.02 ❌
- **TP 3RR**: 23785.74 ❌
- **TP 3.5RR**: 23795.46 ❌
- **TP 4RR**: 23805.18 ❌
- **TP 4.5RR**: 23814.89 ❌
- **TP 5RR**: 23824.61 ❌
- **PnL**: -19.43 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 32.82 points

### Trade #1052 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 08:30:00
- **FVG 5m**: 23715.82 - 23721.88
- **Entrée**: 23730.72 @ 2025-07-30 08:35:00
- **Stop Loss**: 23703.97
- **Risk**: 26.75 points
- **TP 1RR**: 23757.47 ✅
- **TP 1.5RR**: 23770.85 ❌
- **TP 2RR**: 23784.23 ❌
- **TP 2.5RR**: 23797.61 ❌
- **TP 3RR**: 23810.98 ❌
- **TP 3.5RR**: 23824.36 ❌
- **TP 4RR**: 23837.74 ❌
- **TP 4.5RR**: 23851.11 ❌
- **TP 5RR**: 23864.49 ❌
- **PnL**: -26.75 points (-1.0R)
- **MFE**: 28.53 points
- **MAE**: 26.76 points

### Trade #1053 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 08:45:00
- **FVG 5m**: 23737.54 - 23743.85
- **Entrée**: 23723.90 @ 2025-07-30 08:47:00
- **Stop Loss**: 23755.72
- **Risk**: 31.82 points
- **TP 1RR**: 23692.09 ❌
- **TP 1.5RR**: 23676.18 ❌
- **TP 2RR**: 23660.27 ❌
- **TP 2.5RR**: 23644.36 ❌
- **TP 3RR**: 23628.45 ❌
- **TP 3.5RR**: 23612.54 ❌
- **TP 4RR**: 23596.63 ❌
- **TP 4.5RR**: 23580.73 ❌
- **TP 5RR**: 23564.82 ❌
- **PnL**: -31.82 points (-1.0R)
- **MFE**: 24.49 points
- **MAE**: 33.07 points

### Trade #1054 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 08:45:00
- **FVG 5m**: 23737.54 - 23743.85
- **Entrée**: 23723.90 @ 2025-07-30 08:47:00
- **Stop Loss**: 23755.72
- **Risk**: 31.82 points
- **TP 1RR**: 23692.09 ❌
- **TP 1.5RR**: 23676.18 ❌
- **TP 2RR**: 23660.27 ❌
- **TP 2.5RR**: 23644.36 ❌
- **TP 3RR**: 23628.45 ❌
- **TP 3.5RR**: 23612.54 ❌
- **TP 4RR**: 23596.63 ❌
- **TP 4.5RR**: 23580.73 ❌
- **TP 5RR**: 23564.82 ❌
- **PnL**: -31.82 points (-1.0R)
- **MFE**: 24.49 points
- **MAE**: 33.07 points

### Trade #1055 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 09:30:00
- **FVG 5m**: 23715.82 - 23721.88
- **Entrée**: 23755.46 @ 2025-07-30 09:31:00
- **Stop Loss**: 23703.97
- **Risk**: 51.50 points
- **TP 1RR**: 23806.96 ✅
- **TP 1.5RR**: 23832.71 ❌
- **TP 2RR**: 23858.46 ❌
- **TP 2.5RR**: 23884.21 ❌
- **TP 3RR**: 23909.95 ❌
- **TP 3.5RR**: 23935.70 ❌
- **TP 4RR**: 23961.45 ❌
- **TP 4.5RR**: 23987.20 ❌
- **TP 5RR**: 24012.95 ❌
- **PnL**: -51.50 points (-1.0R)
- **MFE**: 67.66 points
- **MAE**: 79.28 points

### Trade #1056 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 10:45:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23735.52 @ 2025-07-30 10:49:00
- **Stop Loss**: 23715.83
- **Risk**: 19.69 points
- **TP 1RR**: 23755.21 ✅
- **TP 1.5RR**: 23765.05 ✅
- **TP 2RR**: 23774.90 ✅
- **TP 2.5RR**: 23784.74 ✅
- **TP 3RR**: 23794.59 ✅
- **TP 3.5RR**: 23804.44 ✅
- **TP 4RR**: 23814.28 ✅
- **TP 4.5RR**: 23824.13 ❌
- **TP 5RR**: 23833.97 ❌
- **PnL**: -19.69 points (-1.0R)
- **MFE**: 87.61 points
- **MAE**: 21.97 points

### Trade #1057 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 12:30:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23757.99 @ 2025-07-30 12:31:00
- **Stop Loss**: 23715.83
- **Risk**: 42.16 points
- **TP 1RR**: 23800.15 ✅
- **TP 1.5RR**: 23821.23 ✅
- **TP 2RR**: 23842.31 ❌
- **TP 2.5RR**: 23863.39 ❌
- **TP 3RR**: 23884.47 ❌
- **TP 3.5RR**: 23905.55 ❌
- **TP 4RR**: 23926.63 ❌
- **TP 4.5RR**: 23947.71 ❌
- **TP 5RR**: 23968.79 ❌
- **PnL**: -42.16 points (-1.0R)
- **MFE**: 65.14 points
- **MAE**: 44.44 points

### Trade #1058 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:00:00
- **FVG 5m**: 23769.85 - 23775.91
- **Entrée**: 23761.27 @ 2025-07-30 13:01:00
- **Stop Loss**: 23787.80
- **Risk**: 26.53 points
- **TP 1RR**: 23734.74 ❌
- **TP 1.5RR**: 23721.47 ❌
- **TP 2RR**: 23708.21 ❌
- **TP 2.5RR**: 23694.94 ❌
- **TP 3RR**: 23681.68 ❌
- **TP 3.5RR**: 23668.41 ❌
- **TP 4RR**: 23655.14 ❌
- **TP 4.5RR**: 23641.88 ❌
- **TP 5RR**: 23628.61 ❌
- **PnL**: -26.53 points (-1.0R)
- **MFE**: 17.42 points
- **MAE**: 28.28 points

### Trade #1059 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:45:00
- **FVG 5m**: 23769.85 - 23775.91
- **Entrée**: 23751.17 @ 2025-07-30 13:48:00
- **Stop Loss**: 23787.80
- **Risk**: 36.63 points
- **TP 1RR**: 23714.54 ✅
- **TP 1.5RR**: 23696.23 ✅
- **TP 2RR**: 23677.91 ✅
- **TP 2.5RR**: 23659.60 ✅
- **TP 3RR**: 23641.28 ✅
- **TP 3.5RR**: 23622.96 ✅
- **TP 4RR**: 23604.65 ✅
- **TP 4.5RR**: 23586.33 ❌
- **TP 5RR**: 23568.02 ❌
- **PnL**: -36.63 points (-1.0R)
- **MFE**: 163.35 points
- **MAE**: 97.96 points

### Trade #1060 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:45:00
- **FVG 5m**: 23769.85 - 23775.91
- **Entrée**: 23751.17 @ 2025-07-30 13:48:00
- **Stop Loss**: 23787.80
- **Risk**: 36.63 points
- **TP 1RR**: 23714.54 ✅
- **TP 1.5RR**: 23696.23 ✅
- **TP 2RR**: 23677.91 ✅
- **TP 2.5RR**: 23659.60 ✅
- **TP 3RR**: 23641.28 ✅
- **TP 3.5RR**: 23622.96 ✅
- **TP 4RR**: 23604.65 ✅
- **TP 4.5RR**: 23586.33 ❌
- **TP 5RR**: 23568.02 ❌
- **PnL**: -36.63 points (-1.0R)
- **MFE**: 163.35 points
- **MAE**: 97.96 points

### Trade #1061 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:45:00
- **FVG 5m**: 23769.85 - 23775.91
- **Entrée**: 23751.17 @ 2025-07-30 13:48:00
- **Stop Loss**: 23787.80
- **Risk**: 36.63 points
- **TP 1RR**: 23714.54 ✅
- **TP 1.5RR**: 23696.23 ✅
- **TP 2RR**: 23677.91 ✅
- **TP 2.5RR**: 23659.60 ✅
- **TP 3RR**: 23641.28 ✅
- **TP 3.5RR**: 23622.96 ✅
- **TP 4RR**: 23604.65 ✅
- **TP 4.5RR**: 23586.33 ❌
- **TP 5RR**: 23568.02 ❌
- **PnL**: -36.63 points (-1.0R)
- **MFE**: 163.35 points
- **MAE**: 97.96 points

### Trade #1062 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:45:00
- **FVG 5m**: 23637.81 - 23644.12
- **Entrée**: 23660.79 @ 2025-07-30 14:46:00
- **Stop Loss**: 23625.99
- **Risk**: 34.79 points
- **TP 1RR**: 23695.58 ✅
- **TP 1.5RR**: 23712.98 ✅
- **TP 2RR**: 23730.37 ✅
- **TP 2.5RR**: 23747.77 ✅
- **TP 3RR**: 23765.17 ✅
- **TP 3.5RR**: 23782.56 ✅
- **TP 4RR**: 23799.96 ✅
- **TP 4.5RR**: 23817.36 ✅
- **TP 5RR**: 23834.76 ✅
- **PnL**: 173.97 points (5.0R)
- **MFE**: 188.35 points
- **MAE**: 14.14 points

### Trade #1063 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:45:00
- **FVG 5m**: 23637.81 - 23644.12
- **Entrée**: 23660.79 @ 2025-07-30 14:46:00
- **Stop Loss**: 23625.99
- **Risk**: 34.79 points
- **TP 1RR**: 23695.58 ✅
- **TP 1.5RR**: 23712.98 ✅
- **TP 2RR**: 23730.37 ✅
- **TP 2.5RR**: 23747.77 ✅
- **TP 3RR**: 23765.17 ✅
- **TP 3.5RR**: 23782.56 ✅
- **TP 4RR**: 23799.96 ✅
- **TP 4.5RR**: 23817.36 ✅
- **TP 5RR**: 23834.76 ✅
- **PnL**: 173.97 points (5.0R)
- **MFE**: 188.35 points
- **MAE**: 14.14 points

### Trade #1064 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 03:00:00
- **FVG 5m**: 24056.16 - 24067.27
- **Entrée**: 24052.88 @ 2025-07-31 03:02:00
- **Stop Loss**: 24079.31
- **Risk**: 26.42 points
- **TP 1RR**: 24026.46 ✅
- **TP 1.5RR**: 24013.24 ✅
- **TP 2RR**: 24000.03 ✅
- **TP 2.5RR**: 23986.82 ✅
- **TP 3RR**: 23973.61 ✅
- **TP 3.5RR**: 23960.39 ✅
- **TP 4RR**: 23947.18 ✅
- **TP 4.5RR**: 23933.97 ✅
- **TP 5RR**: 23920.76 ✅
- **PnL**: 132.12 points (5.0R)
- **MFE**: 159.31 points
- **MAE**: 5.30 points

### Trade #1065 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 07:00:00
- **FVG 5m**: 24011.22 - 24018.04
- **Entrée**: 24021.57 @ 2025-07-31 07:10:00
- **Stop Loss**: 23999.22
- **Risk**: 22.36 points
- **TP 1RR**: 24043.93 ✅
- **TP 1.5RR**: 24055.11 ❌
- **TP 2RR**: 24066.29 ❌
- **TP 2.5RR**: 24077.47 ❌
- **TP 3RR**: 24088.64 ❌
- **TP 3.5RR**: 24099.82 ❌
- **TP 4RR**: 24111.00 ❌
- **TP 4.5RR**: 24122.18 ❌
- **TP 5RR**: 24133.36 ❌
- **PnL**: -22.36 points (-1.0R)
- **MFE**: 26.26 points
- **MAE**: 28.78 points

### Trade #1066 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 08:30:00
- **FVG 5m**: 24012.48 - 24017.28
- **Entrée**: 23899.88 @ 2025-07-31 08:31:00
- **Stop Loss**: 24029.29
- **Risk**: 129.41 points
- **TP 1RR**: 23770.47 ✅
- **TP 1.5RR**: 23705.76 ✅
- **TP 2RR**: 23641.06 ✅
- **TP 2.5RR**: 23576.35 ✅
- **TP 3RR**: 23511.65 ✅
- **TP 3.5RR**: 23446.94 ✅
- **TP 4RR**: 23382.24 ✅
- **TP 4.5RR**: 23317.54 ✅
- **TP 5RR**: 23252.83 ✅
- **PnL**: 647.05 points (5.0R)
- **MFE**: 648.36 points
- **MAE**: 39.89 points

### Trade #1067 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 09:45:00
- **FVG 5m**: 23895.59 - 23905.18
- **Entrée**: 23822.12 @ 2025-07-31 09:46:00
- **Stop Loss**: 23917.13
- **Risk**: 95.02 points
- **TP 1RR**: 23727.10 ✅
- **TP 1.5RR**: 23679.59 ✅
- **TP 2RR**: 23632.08 ✅
- **TP 2.5RR**: 23584.57 ✅
- **TP 3RR**: 23537.07 ✅
- **TP 3.5RR**: 23489.56 ✅
- **TP 4RR**: 23442.05 ✅
- **TP 4.5RR**: 23394.54 ✅
- **TP 5RR**: 23347.03 ✅
- **PnL**: 475.09 points (5.0R)
- **MFE**: 477.18 points
- **MAE**: 28.78 points

### Trade #1068 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 13:00:00
- **FVG 5m**: 23692.34 - 23695.12
- **Entrée**: 23638.31 @ 2025-07-31 13:01:00
- **Stop Loss**: 23706.97
- **Risk**: 68.65 points
- **TP 1RR**: 23569.66 ✅
- **TP 1.5RR**: 23535.33 ✅
- **TP 2RR**: 23501.01 ✅
- **TP 2.5RR**: 23466.68 ✅
- **TP 3RR**: 23432.35 ✅
- **TP 3.5RR**: 23398.02 ✅
- **TP 4RR**: 23363.70 ✅
- **TP 4.5RR**: 23329.37 ✅
- **TP 5RR**: 23295.04 ✅
- **PnL**: 343.27 points (5.0R)
- **MFE**: 345.13 points
- **MAE**: 59.84 points

### Trade #1069 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 13:15:00
- **FVG 5m**: 23635.03 - 23681.99
- **Entrée**: 23685.53 @ 2025-07-31 13:40:00
- **Stop Loss**: 23623.22
- **Risk**: 62.31 points
- **TP 1RR**: 23747.84 ❌
- **TP 1.5RR**: 23779.00 ❌
- **TP 2RR**: 23810.15 ❌
- **TP 2.5RR**: 23841.31 ❌
- **TP 3RR**: 23872.47 ❌
- **TP 3.5RR**: 23903.62 ❌
- **TP 4RR**: 23934.78 ❌
- **TP 4.5RR**: 23965.93 ❌
- **TP 5RR**: 23997.09 ❌
- **PnL**: -62.31 points (-1.0R)
- **MFE**: 12.62 points
- **MAE**: 71.70 points

### Trade #1070 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 13:15:00
- **FVG 5m**: 23635.03 - 23681.99
- **Entrée**: 23685.53 @ 2025-07-31 13:40:00
- **Stop Loss**: 23623.22
- **Risk**: 62.31 points
- **TP 1RR**: 23747.84 ❌
- **TP 1.5RR**: 23779.00 ❌
- **TP 2RR**: 23810.15 ❌
- **TP 2.5RR**: 23841.31 ❌
- **TP 3RR**: 23872.47 ❌
- **TP 3.5RR**: 23903.62 ❌
- **TP 4RR**: 23934.78 ❌
- **TP 4.5RR**: 23965.93 ❌
- **TP 5RR**: 23997.09 ❌
- **PnL**: -62.31 points (-1.0R)
- **MFE**: 12.62 points
- **MAE**: 71.70 points

### Trade #1071 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 13:15:00
- **FVG 5m**: 23635.03 - 23681.99
- **Entrée**: 23685.53 @ 2025-07-31 13:40:00
- **Stop Loss**: 23623.22
- **Risk**: 62.31 points
- **TP 1RR**: 23747.84 ❌
- **TP 1.5RR**: 23779.00 ❌
- **TP 2RR**: 23810.15 ❌
- **TP 2.5RR**: 23841.31 ❌
- **TP 3RR**: 23872.47 ❌
- **TP 3.5RR**: 23903.62 ❌
- **TP 4RR**: 23934.78 ❌
- **TP 4.5RR**: 23965.93 ❌
- **TP 5RR**: 23997.09 ❌
- **PnL**: -62.31 points (-1.0R)
- **MFE**: 12.62 points
- **MAE**: 71.70 points

### Trade #1072 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 17:30:00
- **FVG 5m**: 23555.76 - 23563.58
- **Entrée**: 23538.84 @ 2025-07-31 17:31:00
- **Stop Loss**: 23575.36
- **Risk**: 36.52 points
- **TP 1RR**: 23502.31 ✅
- **TP 1.5RR**: 23484.05 ✅
- **TP 2RR**: 23465.79 ✅
- **TP 2.5RR**: 23447.53 ✅
- **TP 3RR**: 23429.27 ✅
- **TP 3.5RR**: 23411.00 ✅
- **TP 4RR**: 23392.74 ✅
- **TP 4.5RR**: 23374.48 ✅
- **TP 5RR**: 23356.22 ✅
- **PnL**: 182.62 points (5.0R)
- **MFE**: 193.90 points
- **MAE**: 34.84 points

### Trade #1073 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 17:30:00
- **FVG 5m**: 23555.76 - 23563.58
- **Entrée**: 23538.84 @ 2025-07-31 17:31:00
- **Stop Loss**: 23575.36
- **Risk**: 36.52 points
- **TP 1RR**: 23502.31 ✅
- **TP 1.5RR**: 23484.05 ✅
- **TP 2RR**: 23465.79 ✅
- **TP 2.5RR**: 23447.53 ✅
- **TP 3RR**: 23429.27 ✅
- **TP 3.5RR**: 23411.00 ✅
- **TP 4RR**: 23392.74 ✅
- **TP 4.5RR**: 23374.48 ✅
- **TP 5RR**: 23356.22 ✅
- **PnL**: 182.62 points (5.0R)
- **MFE**: 193.90 points
- **MAE**: 34.84 points

### Trade #1074 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 18:00:00
- **FVG 5m**: 23510.31 - 23536.31
- **Entrée**: 23536.57 @ 2025-07-31 18:12:00
- **Stop Loss**: 23498.55
- **Risk**: 38.01 points
- **TP 1RR**: 23574.58 ❌
- **TP 1.5RR**: 23593.59 ❌
- **TP 2RR**: 23612.59 ❌
- **TP 2.5RR**: 23631.60 ❌
- **TP 3RR**: 23650.60 ❌
- **TP 3.5RR**: 23669.61 ❌
- **TP 4RR**: 23688.62 ❌
- **TP 4.5RR**: 23707.62 ❌
- **TP 5RR**: 23726.63 ❌
- **PnL**: -38.01 points (-1.0R)
- **MFE**: 3.79 points
- **MAE**: 43.68 points

### Trade #1075 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 03:45:00
- **FVG 5m**: 23331.81 - 23356.80
- **Entrée**: 23362.86 @ 2025-08-01 04:04:00
- **Stop Loss**: 23320.14
- **Risk**: 42.72 points
- **TP 1RR**: 23405.58 ❌
- **TP 1.5RR**: 23426.94 ❌
- **TP 2RR**: 23448.30 ❌
- **TP 2.5RR**: 23469.66 ❌
- **TP 3RR**: 23491.02 ❌
- **TP 3.5RR**: 23512.39 ❌
- **TP 4RR**: 23533.75 ❌
- **TP 4.5RR**: 23555.11 ❌
- **TP 5RR**: 23576.47 ❌
- **PnL**: -42.72 points (-1.0R)
- **MFE**: 6.56 points
- **MAE**: 48.48 points

### Trade #1076 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-01 05:45:00
- **FVG 5m**: 23323.22 - 23331.81
- **Entrée**: 23298.48 @ 2025-08-01 05:46:00
- **Stop Loss**: 23343.47
- **Risk**: 44.99 points
- **TP 1RR**: 23253.49 ❌
- **TP 1.5RR**: 23230.99 ❌
- **TP 2RR**: 23208.50 ❌
- **TP 2.5RR**: 23186.00 ❌
- **TP 3RR**: 23163.50 ❌
- **TP 3.5RR**: 23141.01 ❌
- **TP 4RR**: 23118.51 ❌
- **TP 4.5RR**: 23096.01 ❌
- **TP 5RR**: 23073.52 ❌
- **PnL**: -44.99 points (-1.0R)
- **MFE**: 38.88 points
- **MAE**: 52.77 points

### Trade #1077 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 06:00:00
- **FVG 5m**: 23308.83 - 23312.12
- **Entrée**: 23314.39 @ 2025-08-01 06:10:00
- **Stop Loss**: 23297.18
- **Risk**: 17.21 points
- **TP 1RR**: 23331.60 ✅
- **TP 1.5RR**: 23340.20 ✅
- **TP 2RR**: 23348.81 ✅
- **TP 2.5RR**: 23357.41 ✅
- **TP 3RR**: 23366.01 ✅
- **TP 3.5RR**: 23374.62 ❌
- **TP 4RR**: 23383.22 ❌
- **TP 4.5RR**: 23391.83 ❌
- **TP 5RR**: 23400.43 ❌
- **PnL**: -17.21 points (-1.0R)
- **MFE**: 57.06 points
- **MAE**: 21.46 points

### Trade #1078 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 06:00:00
- **FVG 5m**: 23308.83 - 23312.12
- **Entrée**: 23314.39 @ 2025-08-01 06:10:00
- **Stop Loss**: 23297.18
- **Risk**: 17.21 points
- **TP 1RR**: 23331.60 ✅
- **TP 1.5RR**: 23340.20 ✅
- **TP 2RR**: 23348.81 ✅
- **TP 2.5RR**: 23357.41 ✅
- **TP 3RR**: 23366.01 ✅
- **TP 3.5RR**: 23374.62 ❌
- **TP 4RR**: 23383.22 ❌
- **TP 4.5RR**: 23391.83 ❌
- **TP 5RR**: 23400.43 ❌
- **PnL**: -17.21 points (-1.0R)
- **MFE**: 57.06 points
- **MAE**: 21.46 points

### Trade #1079 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 09:00:00
- **FVG 5m**: 23135.89 - 23144.98
- **Entrée**: 23145.73 @ 2025-08-01 09:12:00
- **Stop Loss**: 23124.32
- **Risk**: 21.41 points
- **TP 1RR**: 23167.15 ✅
- **TP 1.5RR**: 23177.86 ✅
- **TP 2RR**: 23188.56 ✅
- **TP 2.5RR**: 23199.27 ✅
- **TP 3RR**: 23209.98 ✅
- **TP 3.5RR**: 23220.68 ✅
- **TP 4RR**: 23231.39 ✅
- **TP 4.5RR**: 23242.10 ✅
- **TP 5RR**: 23252.81 ❌
- **PnL**: -21.41 points (-1.0R)
- **MFE**: 105.03 points
- **MAE**: 22.98 points

### Trade #1080 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 09:00:00
- **FVG 5m**: 23135.89 - 23144.98
- **Entrée**: 23145.73 @ 2025-08-01 09:12:00
- **Stop Loss**: 23124.32
- **Risk**: 21.41 points
- **TP 1RR**: 23167.15 ✅
- **TP 1.5RR**: 23177.86 ✅
- **TP 2RR**: 23188.56 ✅
- **TP 2.5RR**: 23199.27 ✅
- **TP 3RR**: 23209.98 ✅
- **TP 3.5RR**: 23220.68 ✅
- **TP 4RR**: 23231.39 ✅
- **TP 4.5RR**: 23242.10 ✅
- **TP 5RR**: 23252.81 ❌
- **PnL**: -21.41 points (-1.0R)
- **MFE**: 105.03 points
- **MAE**: 22.98 points

### Trade #1081 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 11:00:00
- **FVG 5m**: 23135.89 - 23144.98
- **Entrée**: 23239.91 @ 2025-08-01 11:01:00
- **Stop Loss**: 23124.32
- **Risk**: 115.59 points
- **TP 1RR**: 23355.50 ❌
- **TP 1.5RR**: 23413.29 ❌
- **TP 2RR**: 23471.08 ❌
- **TP 2.5RR**: 23528.88 ❌
- **TP 3RR**: 23586.67 ❌
- **TP 3.5RR**: 23644.47 ❌
- **TP 4RR**: 23702.26 ❌
- **TP 4.5RR**: 23760.05 ❌
- **TP 5RR**: 23817.85 ❌
- **PnL**: -115.59 points (-1.0R)
- **MFE**: 33.83 points
- **MAE**: 121.19 points

### Trade #1082 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 11:00:00
- **FVG 5m**: 23135.89 - 23144.98
- **Entrée**: 23239.91 @ 2025-08-01 11:01:00
- **Stop Loss**: 23124.32
- **Risk**: 115.59 points
- **TP 1RR**: 23355.50 ❌
- **TP 1.5RR**: 23413.29 ❌
- **TP 2RR**: 23471.08 ❌
- **TP 2.5RR**: 23528.88 ❌
- **TP 3RR**: 23586.67 ❌
- **TP 3.5RR**: 23644.47 ❌
- **TP 4RR**: 23702.26 ❌
- **TP 4.5RR**: 23760.05 ❌
- **TP 5RR**: 23817.85 ❌
- **PnL**: -115.59 points (-1.0R)
- **MFE**: 33.83 points
- **MAE**: 121.19 points

### Trade #1083 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 13:00:00
- **FVG 5m**: 23126.55 - 23142.70
- **Entrée**: 23145.23 @ 2025-08-01 13:39:00
- **Stop Loss**: 23114.98
- **Risk**: 30.25 points
- **TP 1RR**: 23175.48 ❌
- **TP 1.5RR**: 23190.60 ❌
- **TP 2RR**: 23205.72 ❌
- **TP 2.5RR**: 23220.85 ❌
- **TP 3RR**: 23235.97 ❌
- **TP 3.5RR**: 23251.09 ❌
- **TP 4RR**: 23266.22 ❌
- **TP 4.5RR**: 23281.34 ❌
- **TP 5RR**: 23296.46 ❌
- **PnL**: -30.25 points (-1.0R)
- **MFE**: 24.74 points
- **MAE**: 50.50 points

### Trade #1084 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 13:00:00
- **FVG 5m**: 23126.55 - 23142.70
- **Entrée**: 23145.23 @ 2025-08-01 13:39:00
- **Stop Loss**: 23114.98
- **Risk**: 30.25 points
- **TP 1RR**: 23175.48 ❌
- **TP 1.5RR**: 23190.60 ❌
- **TP 2RR**: 23205.72 ❌
- **TP 2.5RR**: 23220.85 ❌
- **TP 3RR**: 23235.97 ❌
- **TP 3.5RR**: 23251.09 ❌
- **TP 4RR**: 23266.22 ❌
- **TP 4.5RR**: 23281.34 ❌
- **TP 5RR**: 23296.46 ❌
- **PnL**: -30.25 points (-1.0R)
- **MFE**: 24.74 points
- **MAE**: 50.50 points

### Trade #1085 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 13:00:00
- **FVG 5m**: 23126.55 - 23142.70
- **Entrée**: 23145.23 @ 2025-08-01 13:39:00
- **Stop Loss**: 23114.98
- **Risk**: 30.25 points
- **TP 1RR**: 23175.48 ❌
- **TP 1.5RR**: 23190.60 ❌
- **TP 2RR**: 23205.72 ❌
- **TP 2.5RR**: 23220.85 ❌
- **TP 3RR**: 23235.97 ❌
- **TP 3.5RR**: 23251.09 ❌
- **TP 4RR**: 23266.22 ❌
- **TP 4.5RR**: 23281.34 ❌
- **TP 5RR**: 23296.46 ❌
- **PnL**: -30.25 points (-1.0R)
- **MFE**: 24.74 points
- **MAE**: 50.50 points

### Trade #1086 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-03 20:00:00
- **FVG 5m**: 23166.18 - 23170.98
- **Entrée**: 23165.68 @ 2025-08-03 20:07:00
- **Stop Loss**: 23182.57
- **Risk**: 16.89 points
- **TP 1RR**: 23148.79 ❌
- **TP 1.5RR**: 23140.35 ❌
- **TP 2RR**: 23131.90 ❌
- **TP 2.5RR**: 23123.46 ❌
- **TP 3RR**: 23115.02 ❌
- **TP 3.5RR**: 23106.57 ❌
- **TP 4RR**: 23098.13 ❌
- **TP 4.5RR**: 23089.69 ❌
- **TP 5RR**: 23081.24 ❌
- **PnL**: -16.89 points (-1.0R)
- **MFE**: 6.82 points
- **MAE**: 18.94 points

### Trade #1087 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 02:30:00
- **FVG 5m**: 23212.64 - 23217.69
- **Entrée**: 23251.52 @ 2025-08-04 02:31:00
- **Stop Loss**: 23201.03
- **Risk**: 50.49 points
- **TP 1RR**: 23302.01 ✅
- **TP 1.5RR**: 23327.25 ✅
- **TP 2RR**: 23352.50 ✅
- **TP 2.5RR**: 23377.74 ✅
- **TP 3RR**: 23402.98 ✅
- **TP 3.5RR**: 23428.23 ✅
- **TP 4RR**: 23453.47 ✅
- **TP 4.5RR**: 23478.72 ✅
- **TP 5RR**: 23503.96 ✅
- **PnL**: 252.44 points (5.0R)
- **MFE**: 253.23 points
- **MAE**: 17.93 points

### Trade #1088 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 03:00:00
- **FVG 5m**: 23212.64 - 23217.69
- **Entrée**: 23245.46 @ 2025-08-04 03:01:00
- **Stop Loss**: 23201.03
- **Risk**: 44.43 points
- **TP 1RR**: 23289.89 ✅
- **TP 1.5RR**: 23312.10 ✅
- **TP 2RR**: 23334.32 ✅
- **TP 2.5RR**: 23356.53 ✅
- **TP 3RR**: 23378.75 ✅
- **TP 3.5RR**: 23400.96 ✅
- **TP 4RR**: 23423.17 ✅
- **TP 4.5RR**: 23445.39 ✅
- **TP 5RR**: 23467.60 ✅
- **PnL**: 222.14 points (5.0R)
- **MFE**: 222.68 points
- **MAE**: 0.76 points

### Trade #1089 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-04 06:00:00
- **FVG 5m**: 23279.55 - 23282.07
- **Entrée**: 23278.28 @ 2025-08-04 06:01:00
- **Stop Loss**: 23293.71
- **Risk**: 15.43 points
- **TP 1RR**: 23262.86 ✅
- **TP 1.5RR**: 23255.14 ❌
- **TP 2RR**: 23247.43 ❌
- **TP 2.5RR**: 23239.71 ❌
- **TP 3RR**: 23232.00 ❌
- **TP 3.5RR**: 23224.29 ❌
- **TP 4RR**: 23216.57 ❌
- **TP 4.5RR**: 23208.86 ❌
- **TP 5RR**: 23201.14 ❌
- **PnL**: -15.43 points (-1.0R)
- **MFE**: 18.68 points
- **MAE**: 15.65 points

### Trade #1090 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 14:45:00
- **FVG 5m**: 23499.20 - 23510.31
- **Entrée**: 23510.56 @ 2025-08-04 14:50:00
- **Stop Loss**: 23487.45
- **Risk**: 23.11 points
- **TP 1RR**: 23533.67 ✅
- **TP 1.5RR**: 23545.23 ✅
- **TP 2RR**: 23556.78 ✅
- **TP 2.5RR**: 23568.34 ✅
- **TP 3RR**: 23579.89 ✅
- **TP 3.5RR**: 23591.45 ✅
- **TP 4RR**: 23603.01 ✅
- **TP 4.5RR**: 23614.56 ✅
- **TP 5RR**: 23626.12 ✅
- **PnL**: 115.56 points (5.0R)
- **MFE**: 115.63 points
- **MAE**: 5.05 points

### Trade #1091 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-04 17:00:00
- **FVG 5m**: 23569.14 - 23572.17
- **Entrée**: 23566.36 @ 2025-08-04 17:06:00
- **Stop Loss**: 23583.95
- **Risk**: 17.59 points
- **TP 1RR**: 23548.77 ✅
- **TP 1.5RR**: 23539.97 ❌
- **TP 2RR**: 23531.17 ❌
- **TP 2.5RR**: 23522.38 ❌
- **TP 3RR**: 23513.58 ❌
- **TP 3.5RR**: 23504.78 ❌
- **TP 4RR**: 23495.99 ❌
- **TP 4.5RR**: 23487.19 ❌
- **TP 5RR**: 23478.39 ❌
- **PnL**: -17.59 points (-1.0R)
- **MFE**: 21.71 points
- **MAE**: 18.18 points

### Trade #1092 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-05 03:00:00
- **FVG 5m**: 23607.77 - 23610.79
- **Entrée**: 23557.02 @ 2025-08-05 03:01:00
- **Stop Loss**: 23622.60
- **Risk**: 65.58 points
- **TP 1RR**: 23491.43 ❌
- **TP 1.5RR**: 23458.64 ❌
- **TP 2RR**: 23425.85 ❌
- **TP 2.5RR**: 23393.06 ❌
- **TP 3RR**: 23360.27 ❌
- **TP 3.5RR**: 23327.48 ❌
- **TP 4RR**: 23294.69 ❌
- **TP 4.5RR**: 23261.89 ❌
- **TP 5RR**: 23229.10 ❌
- **PnL**: -65.58 points (-1.0R)
- **MFE**: 13.63 points
- **MAE**: 66.40 points

### Trade #1093 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-05 06:15:00
- **FVG 5m**: 23604.99 - 23608.02
- **Entrée**: 23597.67 @ 2025-08-05 06:30:00
- **Stop Loss**: 23619.82
- **Risk**: 22.16 points
- **TP 1RR**: 23575.51 ❌
- **TP 1.5RR**: 23564.43 ❌
- **TP 2RR**: 23553.36 ❌
- **TP 2.5RR**: 23542.28 ❌
- **TP 3RR**: 23531.20 ❌
- **TP 3.5RR**: 23520.12 ❌
- **TP 4RR**: 23509.04 ❌
- **TP 4.5RR**: 23497.97 ❌
- **TP 5RR**: 23486.89 ❌
- **PnL**: -22.16 points (-1.0R)
- **MFE**: 4.29 points
- **MAE**: 24.74 points

### Trade #1094 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-05 10:30:00
- **FVG 5m**: 23417.15 - 23425.98
- **Entrée**: 23404.77 @ 2025-08-05 10:31:00
- **Stop Loss**: 23437.70
- **Risk**: 32.92 points
- **TP 1RR**: 23371.85 ✅
- **TP 1.5RR**: 23355.39 ✅
- **TP 2RR**: 23338.93 ❌
- **TP 2.5RR**: 23322.47 ❌
- **TP 3RR**: 23306.01 ❌
- **TP 3.5RR**: 23289.55 ❌
- **TP 4RR**: 23273.09 ❌
- **TP 4.5RR**: 23256.63 ❌
- **TP 5RR**: 23240.17 ❌
- **PnL**: -32.92 points (-1.0R)
- **MFE**: 62.36 points
- **MAE**: 34.59 points

### Trade #1095 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 20:30:00
- **FVG 5m**: 23297.72 - 23301.51
- **Entrée**: 23313.88 @ 2025-08-05 20:31:00
- **Stop Loss**: 23286.08
- **Risk**: 27.81 points
- **TP 1RR**: 23341.69 ✅
- **TP 1.5RR**: 23355.59 ✅
- **TP 2RR**: 23369.50 ✅
- **TP 2.5RR**: 23383.40 ✅
- **TP 3RR**: 23397.31 ✅
- **TP 3.5RR**: 23411.21 ✅
- **TP 4RR**: 23425.11 ✅
- **TP 4.5RR**: 23439.02 ✅
- **TP 5RR**: 23452.92 ✅
- **PnL**: 139.04 points (5.0R)
- **MFE**: 140.12 points
- **MAE**: 0.00 points

### Trade #1096 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 20:30:00
- **FVG 5m**: 23297.72 - 23301.51
- **Entrée**: 23313.88 @ 2025-08-05 20:31:00
- **Stop Loss**: 23286.08
- **Risk**: 27.81 points
- **TP 1RR**: 23341.69 ✅
- **TP 1.5RR**: 23355.59 ✅
- **TP 2RR**: 23369.50 ✅
- **TP 2.5RR**: 23383.40 ✅
- **TP 3RR**: 23397.31 ✅
- **TP 3.5RR**: 23411.21 ✅
- **TP 4RR**: 23425.11 ✅
- **TP 4.5RR**: 23439.02 ✅
- **TP 5RR**: 23452.92 ✅
- **PnL**: 139.04 points (5.0R)
- **MFE**: 140.12 points
- **MAE**: 0.00 points

### Trade #1097 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 06:00:00
- **FVG 5m**: 23383.06 - 23388.62
- **Entrée**: 23397.71 @ 2025-08-06 06:01:00
- **Stop Loss**: 23371.37
- **Risk**: 26.34 points
- **TP 1RR**: 23424.04 ✅
- **TP 1.5RR**: 23437.21 ❌
- **TP 2RR**: 23450.38 ❌
- **TP 2.5RR**: 23463.54 ❌
- **TP 3RR**: 23476.71 ❌
- **TP 3.5RR**: 23489.88 ❌
- **TP 4RR**: 23503.05 ❌
- **TP 4.5RR**: 23516.21 ❌
- **TP 5RR**: 23529.38 ❌
- **PnL**: -26.34 points (-1.0R)
- **MFE**: 28.78 points
- **MAE**: 28.28 points

### Trade #1098 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 09:30:00
- **FVG 5m**: 23467.64 - 23490.36
- **Entrée**: 23496.17 @ 2025-08-06 09:45:00
- **Stop Loss**: 23455.91
- **Risk**: 40.26 points
- **TP 1RR**: 23536.43 ✅
- **TP 1.5RR**: 23556.57 ✅
- **TP 2RR**: 23576.70 ✅
- **TP 2.5RR**: 23596.83 ✅
- **TP 3RR**: 23616.96 ✅
- **TP 3.5RR**: 23637.09 ✅
- **TP 4RR**: 23657.23 ✅
- **TP 4.5RR**: 23677.36 ✅
- **TP 5RR**: 23697.49 ✅
- **PnL**: 201.32 points (5.0R)
- **MFE**: 202.23 points
- **MAE**: 39.64 points

### Trade #1099 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 09:30:00
- **FVG 5m**: 23467.64 - 23490.36
- **Entrée**: 23496.17 @ 2025-08-06 09:45:00
- **Stop Loss**: 23455.91
- **Risk**: 40.26 points
- **TP 1RR**: 23536.43 ✅
- **TP 1.5RR**: 23556.57 ✅
- **TP 2RR**: 23576.70 ✅
- **TP 2.5RR**: 23596.83 ✅
- **TP 3RR**: 23616.96 ✅
- **TP 3.5RR**: 23637.09 ✅
- **TP 4RR**: 23657.23 ✅
- **TP 4.5RR**: 23677.36 ✅
- **TP 5RR**: 23697.49 ✅
- **PnL**: 201.32 points (5.0R)
- **MFE**: 202.23 points
- **MAE**: 39.64 points

### Trade #1100 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 10:15:00
- **FVG 5m**: 23467.64 - 23490.36
- **Entrée**: 23532.53 @ 2025-08-06 10:16:00
- **Stop Loss**: 23455.91
- **Risk**: 76.62 points
- **TP 1RR**: 23609.15 ✅
- **TP 1.5RR**: 23647.46 ✅
- **TP 2RR**: 23685.77 ✅
- **TP 2.5RR**: 23724.08 ✅
- **TP 3RR**: 23762.39 ✅
- **TP 3.5RR**: 23800.70 ✅
- **TP 4RR**: 23839.01 ✅
- **TP 4.5RR**: 23877.32 ✅
- **TP 5RR**: 23915.63 ✅
- **PnL**: 383.10 points (5.0R)
- **MFE**: 385.53 points
- **MAE**: 3.28 points

### Trade #1101 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 10:15:00
- **FVG 5m**: 23467.64 - 23490.36
- **Entrée**: 23532.53 @ 2025-08-06 10:16:00
- **Stop Loss**: 23455.91
- **Risk**: 76.62 points
- **TP 1RR**: 23609.15 ✅
- **TP 1.5RR**: 23647.46 ✅
- **TP 2RR**: 23685.77 ✅
- **TP 2.5RR**: 23724.08 ✅
- **TP 3RR**: 23762.39 ✅
- **TP 3.5RR**: 23800.70 ✅
- **TP 4RR**: 23839.01 ✅
- **TP 4.5RR**: 23877.32 ✅
- **TP 5RR**: 23915.63 ✅
- **PnL**: 383.10 points (5.0R)
- **MFE**: 385.53 points
- **MAE**: 3.28 points

### Trade #1102 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 06:00:00
- **FVG 5m**: 23846.61 - 23849.13
- **Entrée**: 23845.85 @ 2025-08-07 06:06:00
- **Stop Loss**: 23861.06
- **Risk**: 15.21 points
- **TP 1RR**: 23830.64 ✅
- **TP 1.5RR**: 23823.04 ✅
- **TP 2RR**: 23815.44 ✅
- **TP 2.5RR**: 23807.83 ❌
- **TP 3RR**: 23800.23 ❌
- **TP 3.5RR**: 23792.63 ❌
- **TP 4RR**: 23785.02 ❌
- **TP 4.5RR**: 23777.42 ❌
- **TP 5RR**: 23769.82 ❌
- **PnL**: -15.21 points (-1.0R)
- **MFE**: 36.61 points
- **MAE**: 15.65 points

### Trade #1103 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 13:00:00
- **FVG 5m**: 23661.54 - 23689.31
- **Entrée**: 23636.55 @ 2025-08-07 13:01:00
- **Stop Loss**: 23701.16
- **Risk**: 64.61 points
- **TP 1RR**: 23571.94 ✅
- **TP 1.5RR**: 23539.63 ❌
- **TP 2RR**: 23507.32 ❌
- **TP 2.5RR**: 23475.02 ❌
- **TP 3RR**: 23442.71 ❌
- **TP 3.5RR**: 23410.40 ❌
- **TP 4RR**: 23378.10 ❌
- **TP 4.5RR**: 23345.79 ❌
- **TP 5RR**: 23313.49 ❌
- **PnL**: -64.61 points (-1.0R)
- **MFE**: 76.50 points
- **MAE**: 68.17 points

### Trade #1104 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 13:00:00
- **FVG 5m**: 23661.54 - 23689.31
- **Entrée**: 23636.55 @ 2025-08-07 13:01:00
- **Stop Loss**: 23701.16
- **Risk**: 64.61 points
- **TP 1RR**: 23571.94 ✅
- **TP 1.5RR**: 23539.63 ❌
- **TP 2RR**: 23507.32 ❌
- **TP 2.5RR**: 23475.02 ❌
- **TP 3RR**: 23442.71 ❌
- **TP 3.5RR**: 23410.40 ❌
- **TP 4RR**: 23378.10 ❌
- **TP 4.5RR**: 23345.79 ❌
- **TP 5RR**: 23313.49 ❌
- **PnL**: -64.61 points (-1.0R)
- **MFE**: 76.50 points
- **MAE**: 68.17 points

### Trade #1105 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 13:00:00
- **FVG 5m**: 23661.54 - 23689.31
- **Entrée**: 23636.55 @ 2025-08-07 13:01:00
- **Stop Loss**: 23701.16
- **Risk**: 64.61 points
- **TP 1RR**: 23571.94 ✅
- **TP 1.5RR**: 23539.63 ❌
- **TP 2RR**: 23507.32 ❌
- **TP 2.5RR**: 23475.02 ❌
- **TP 3RR**: 23442.71 ❌
- **TP 3.5RR**: 23410.40 ❌
- **TP 4RR**: 23378.10 ❌
- **TP 4.5RR**: 23345.79 ❌
- **TP 5RR**: 23313.49 ❌
- **PnL**: -64.61 points (-1.0R)
- **MFE**: 76.50 points
- **MAE**: 68.17 points

### Trade #1106 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-07 13:45:00
- **FVG 5m**: 23592.11 - 23610.04
- **Entrée**: 23612.31 @ 2025-08-07 13:52:00
- **Stop Loss**: 23580.32
- **Risk**: 31.99 points
- **TP 1RR**: 23644.30 ✅
- **TP 1.5RR**: 23660.30 ✅
- **TP 2RR**: 23676.30 ✅
- **TP 2.5RR**: 23692.30 ✅
- **TP 3RR**: 23708.29 ✅
- **TP 3.5RR**: 23724.29 ✅
- **TP 4RR**: 23740.29 ✅
- **TP 4.5RR**: 23756.28 ✅
- **TP 5RR**: 23772.28 ✅
- **PnL**: 159.97 points (5.0R)
- **MFE**: 161.58 points
- **MAE**: 1.01 points

### Trade #1107 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-07 14:45:00
- **FVG 5m**: 23592.11 - 23610.04
- **Entrée**: 23677.70 @ 2025-08-07 14:46:00
- **Stop Loss**: 23580.32
- **Risk**: 97.39 points
- **TP 1RR**: 23775.09 ✅
- **TP 1.5RR**: 23823.78 ✅
- **TP 2RR**: 23872.47 ✅
- **TP 2.5RR**: 23921.16 ✅
- **TP 3RR**: 23969.86 ✅
- **TP 3.5RR**: 24018.55 ✅
- **TP 4RR**: 24067.24 ✅
- **TP 4.5RR**: 24115.94 ✅
- **TP 5RR**: 24164.63 ✅
- **PnL**: 486.93 points (5.0R)
- **MFE**: 487.03 points
- **MAE**: 4.29 points

### Trade #1108 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-08 07:00:00
- **FVG 5m**: 23807.73 - 23811.51
- **Entrée**: 23803.94 @ 2025-08-08 07:02:00
- **Stop Loss**: 23823.42
- **Risk**: 19.48 points
- **TP 1RR**: 23784.46 ✅
- **TP 1.5RR**: 23774.72 ✅
- **TP 2RR**: 23764.98 ✅
- **TP 2.5RR**: 23755.24 ✅
- **TP 3RR**: 23745.50 ❌
- **TP 3.5RR**: 23735.76 ❌
- **TP 4RR**: 23726.02 ❌
- **TP 4.5RR**: 23716.28 ❌
- **TP 5RR**: 23706.54 ❌
- **PnL**: -19.48 points (-1.0R)
- **MFE**: 52.77 points
- **MAE**: 32.06 points

### Trade #1109 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-08 09:45:00
- **FVG 5m**: 23918.06 - 23921.59
- **Entrée**: 23917.05 @ 2025-08-08 09:47:00
- **Stop Loss**: 23933.55
- **Risk**: 16.51 points
- **TP 1RR**: 23900.54 ✅
- **TP 1.5RR**: 23892.29 ✅
- **TP 2RR**: 23884.04 ✅
- **TP 2.5RR**: 23875.78 ✅
- **TP 3RR**: 23867.53 ✅
- **TP 3.5RR**: 23859.28 ✅
- **TP 4RR**: 23851.03 ✅
- **TP 4.5RR**: 23842.77 ❌
- **TP 5RR**: 23834.52 ❌
- **PnL**: -16.51 points (-1.0R)
- **MFE**: 71.20 points
- **MAE**: 17.67 points

### Trade #1110 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-08 14:45:00
- **FVG 5m**: 23936.24 - 23939.77
- **Entrée**: 23946.59 @ 2025-08-08 14:54:00
- **Stop Loss**: 23924.27
- **Risk**: 22.32 points
- **TP 1RR**: 23968.91 ✅
- **TP 1.5RR**: 23980.07 ✅
- **TP 2RR**: 23991.23 ✅
- **TP 2.5RR**: 24002.39 ✅
- **TP 3RR**: 24013.55 ❌
- **TP 3.5RR**: 24024.71 ❌
- **TP 4RR**: 24035.87 ❌
- **TP 4.5RR**: 24047.03 ❌
- **TP 5RR**: 24058.19 ❌
- **PnL**: -22.32 points (-1.0R)
- **MFE**: 61.86 points
- **MAE**: 22.72 points

### Trade #1111 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-08 15:00:00
- **FVG 5m**: 23936.24 - 23939.77
- **Entrée**: 23964.01 @ 2025-08-08 15:01:00
- **Stop Loss**: 23924.27
- **Risk**: 39.74 points
- **TP 1RR**: 24003.75 ✅
- **TP 1.5RR**: 24023.62 ❌
- **TP 2RR**: 24043.49 ❌
- **TP 2.5RR**: 24063.36 ❌
- **TP 3RR**: 24083.23 ❌
- **TP 3.5RR**: 24103.10 ❌
- **TP 4RR**: 24122.97 ❌
- **TP 4.5RR**: 24142.84 ❌
- **TP 5RR**: 24162.71 ❌
- **PnL**: -39.74 points (-1.0R)
- **MFE**: 44.44 points
- **MAE**: 40.14 points

### Trade #1112 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-10 17:00:00
- **FVG 5m**: 23976.63 - 23984.96
- **Entrée**: 23970.07 @ 2025-08-10 17:02:00
- **Stop Loss**: 23996.96
- **Risk**: 26.89 points
- **TP 1RR**: 23943.18 ✅
- **TP 1.5RR**: 23929.74 ❌
- **TP 2RR**: 23916.29 ❌
- **TP 2.5RR**: 23902.85 ❌
- **TP 3RR**: 23889.40 ❌
- **TP 3.5RR**: 23875.96 ❌
- **TP 4RR**: 23862.51 ❌
- **TP 4.5RR**: 23849.07 ❌
- **TP 5RR**: 23835.63 ❌
- **PnL**: -26.89 points (-1.0R)
- **MFE**: 34.34 points
- **MAE**: 28.02 points

### Trade #1113 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 02:30:00
- **FVG 5m**: 23987.49 - 23990.27
- **Entrée**: 23969.56 @ 2025-08-11 02:31:00
- **Stop Loss**: 24002.26
- **Risk**: 32.70 points
- **TP 1RR**: 23936.87 ✅
- **TP 1.5RR**: 23920.52 ✅
- **TP 2RR**: 23904.17 ✅
- **TP 2.5RR**: 23887.82 ❌
- **TP 3RR**: 23871.47 ❌
- **TP 3.5RR**: 23855.12 ❌
- **TP 4RR**: 23838.77 ❌
- **TP 4.5RR**: 23822.42 ❌
- **TP 5RR**: 23806.07 ❌
- **PnL**: -32.70 points (-1.0R)
- **MFE**: 67.41 points
- **MAE**: 33.07 points

### Trade #1114 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 03:30:00
- **FVG 5m**: 23950.12 - 23954.92
- **Entrée**: 23955.42 @ 2025-08-11 04:26:00
- **Stop Loss**: 23938.15
- **Risk**: 17.28 points
- **TP 1RR**: 23972.70 ✅
- **TP 1.5RR**: 23981.34 ✅
- **TP 2RR**: 23989.98 ✅
- **TP 2.5RR**: 23998.62 ❌
- **TP 3RR**: 24007.26 ❌
- **TP 3.5RR**: 24015.89 ❌
- **TP 4RR**: 24024.53 ❌
- **TP 4.5RR**: 24033.17 ❌
- **TP 5RR**: 24041.81 ❌
- **PnL**: -17.28 points (-1.0R)
- **MFE**: 36.10 points
- **MAE**: 19.95 points

### Trade #1115 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 07:15:00
- **FVG 5m**: 23975.62 - 23981.18
- **Entrée**: 23969.56 @ 2025-08-11 07:23:00
- **Stop Loss**: 23993.17
- **Risk**: 23.60 points
- **TP 1RR**: 23945.96 ✅
- **TP 1.5RR**: 23934.16 ✅
- **TP 2RR**: 23922.35 ✅
- **TP 2.5RR**: 23910.55 ❌
- **TP 3RR**: 23898.75 ❌
- **TP 3.5RR**: 23886.95 ❌
- **TP 4RR**: 23875.15 ❌
- **TP 4.5RR**: 23863.34 ❌
- **TP 5RR**: 23851.54 ❌
- **PnL**: -23.60 points (-1.0R)
- **MFE**: 54.28 points
- **MAE**: 25.00 points

### Trade #1116 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 24004.40 - 24019.81
- **Entrée**: 24002.89 @ 2025-08-11 11:39:00
- **Stop Loss**: 24031.82
- **Risk**: 28.93 points
- **TP 1RR**: 23973.96 ✅
- **TP 1.5RR**: 23959.50 ✅
- **TP 2RR**: 23945.04 ✅
- **TP 2.5RR**: 23930.58 ✅
- **TP 3RR**: 23916.11 ✅
- **TP 3.5RR**: 23901.65 ✅
- **TP 4RR**: 23887.19 ✅
- **TP 4.5RR**: 23872.72 ✅
- **TP 5RR**: 23858.26 ✅
- **PnL**: 144.63 points (5.0R)
- **MFE**: 158.81 points
- **MAE**: 0.50 points

### Trade #1117 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 24004.40 - 24019.81
- **Entrée**: 24002.89 @ 2025-08-11 11:39:00
- **Stop Loss**: 24031.82
- **Risk**: 28.93 points
- **TP 1RR**: 23973.96 ✅
- **TP 1.5RR**: 23959.50 ✅
- **TP 2RR**: 23945.04 ✅
- **TP 2.5RR**: 23930.58 ✅
- **TP 3RR**: 23916.11 ✅
- **TP 3.5RR**: 23901.65 ✅
- **TP 4RR**: 23887.19 ✅
- **TP 4.5RR**: 23872.72 ✅
- **TP 5RR**: 23858.26 ✅
- **PnL**: 144.63 points (5.0R)
- **MFE**: 158.81 points
- **MAE**: 0.50 points

### Trade #1118 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 24004.40 - 24019.81
- **Entrée**: 24002.89 @ 2025-08-11 11:39:00
- **Stop Loss**: 24031.82
- **Risk**: 28.93 points
- **TP 1RR**: 23973.96 ✅
- **TP 1.5RR**: 23959.50 ✅
- **TP 2RR**: 23945.04 ✅
- **TP 2.5RR**: 23930.58 ✅
- **TP 3RR**: 23916.11 ✅
- **TP 3.5RR**: 23901.65 ✅
- **TP 4RR**: 23887.19 ✅
- **TP 4.5RR**: 23872.72 ✅
- **TP 5RR**: 23858.26 ✅
- **PnL**: 144.63 points (5.0R)
- **MFE**: 158.81 points
- **MAE**: 0.50 points

### Trade #1119 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 24004.40 - 24019.81
- **Entrée**: 24002.89 @ 2025-08-11 11:39:00
- **Stop Loss**: 24031.82
- **Risk**: 28.93 points
- **TP 1RR**: 23973.96 ✅
- **TP 1.5RR**: 23959.50 ✅
- **TP 2RR**: 23945.04 ✅
- **TP 2.5RR**: 23930.58 ✅
- **TP 3RR**: 23916.11 ✅
- **TP 3.5RR**: 23901.65 ✅
- **TP 4RR**: 23887.19 ✅
- **TP 4.5RR**: 23872.72 ✅
- **TP 5RR**: 23858.26 ✅
- **PnL**: 144.63 points (5.0R)
- **MFE**: 158.81 points
- **MAE**: 0.50 points

### Trade #1120 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 24004.40 - 24019.81
- **Entrée**: 24002.89 @ 2025-08-11 11:39:00
- **Stop Loss**: 24031.82
- **Risk**: 28.93 points
- **TP 1RR**: 23973.96 ✅
- **TP 1.5RR**: 23959.50 ✅
- **TP 2RR**: 23945.04 ✅
- **TP 2.5RR**: 23930.58 ✅
- **TP 3RR**: 23916.11 ✅
- **TP 3.5RR**: 23901.65 ✅
- **TP 4RR**: 23887.19 ✅
- **TP 4.5RR**: 23872.72 ✅
- **TP 5RR**: 23858.26 ✅
- **PnL**: 144.63 points (5.0R)
- **MFE**: 158.81 points
- **MAE**: 0.50 points

### Trade #1121 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 19:15:00
- **FVG 5m**: 23872.36 - 23875.64
- **Entrée**: 23877.41 @ 2025-08-11 19:17:00
- **Stop Loss**: 23860.42
- **Risk**: 16.99 points
- **TP 1RR**: 23894.40 ✅
- **TP 1.5RR**: 23902.89 ✅
- **TP 2RR**: 23911.38 ❌
- **TP 2.5RR**: 23919.87 ❌
- **TP 3RR**: 23928.37 ❌
- **TP 3.5RR**: 23936.86 ❌
- **TP 4RR**: 23945.35 ❌
- **TP 4.5RR**: 23953.85 ❌
- **TP 5RR**: 23962.34 ❌
- **PnL**: -16.99 points (-1.0R)
- **MFE**: 33.83 points
- **MAE**: 22.47 points

### Trade #1122 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-12 08:45:00
- **FVG 5m**: 23976.38 - 23990.52
- **Entrée**: 23973.60 @ 2025-08-12 08:47:00
- **Stop Loss**: 24002.51
- **Risk**: 28.91 points
- **TP 1RR**: 23944.69 ✅
- **TP 1.5RR**: 23930.24 ✅
- **TP 2RR**: 23915.78 ✅
- **TP 2.5RR**: 23901.32 ✅
- **TP 3RR**: 23886.87 ✅
- **TP 3.5RR**: 23872.41 ✅
- **TP 4RR**: 23857.96 ✅
- **TP 4.5RR**: 23843.50 ❌
- **TP 5RR**: 23829.05 ❌
- **PnL**: -28.91 points (-1.0R)
- **MFE**: 117.65 points
- **MAE**: 33.07 points

### Trade #1123 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-12 08:45:00
- **FVG 5m**: 23976.38 - 23990.52
- **Entrée**: 23973.60 @ 2025-08-12 08:47:00
- **Stop Loss**: 24002.51
- **Risk**: 28.91 points
- **TP 1RR**: 23944.69 ✅
- **TP 1.5RR**: 23930.24 ✅
- **TP 2RR**: 23915.78 ✅
- **TP 2.5RR**: 23901.32 ✅
- **TP 3RR**: 23886.87 ✅
- **TP 3.5RR**: 23872.41 ✅
- **TP 4RR**: 23857.96 ✅
- **TP 4.5RR**: 23843.50 ❌
- **TP 5RR**: 23829.05 ❌
- **PnL**: -28.91 points (-1.0R)
- **MFE**: 117.65 points
- **MAE**: 33.07 points

### Trade #1124 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-12 08:45:00
- **FVG 5m**: 23976.38 - 23990.52
- **Entrée**: 23973.60 @ 2025-08-12 08:47:00
- **Stop Loss**: 24002.51
- **Risk**: 28.91 points
- **TP 1RR**: 23944.69 ✅
- **TP 1.5RR**: 23930.24 ✅
- **TP 2RR**: 23915.78 ✅
- **TP 2.5RR**: 23901.32 ✅
- **TP 3RR**: 23886.87 ✅
- **TP 3.5RR**: 23872.41 ✅
- **TP 4RR**: 23857.96 ✅
- **TP 4.5RR**: 23843.50 ❌
- **TP 5RR**: 23829.05 ❌
- **PnL**: -28.91 points (-1.0R)
- **MFE**: 117.65 points
- **MAE**: 33.07 points

### Trade #1125 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-12 08:45:00
- **FVG 5m**: 23976.38 - 23990.52
- **Entrée**: 23973.60 @ 2025-08-12 08:47:00
- **Stop Loss**: 24002.51
- **Risk**: 28.91 points
- **TP 1RR**: 23944.69 ✅
- **TP 1.5RR**: 23930.24 ✅
- **TP 2RR**: 23915.78 ✅
- **TP 2.5RR**: 23901.32 ✅
- **TP 3RR**: 23886.87 ✅
- **TP 3.5RR**: 23872.41 ✅
- **TP 4RR**: 23857.96 ✅
- **TP 4.5RR**: 23843.50 ❌
- **TP 5RR**: 23829.05 ❌
- **PnL**: -28.91 points (-1.0R)
- **MFE**: 117.65 points
- **MAE**: 33.07 points

### Trade #1126 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-12 08:45:00
- **FVG 5m**: 23976.38 - 23990.52
- **Entrée**: 23973.60 @ 2025-08-12 08:47:00
- **Stop Loss**: 24002.51
- **Risk**: 28.91 points
- **TP 1RR**: 23944.69 ✅
- **TP 1.5RR**: 23930.24 ✅
- **TP 2RR**: 23915.78 ✅
- **TP 2.5RR**: 23901.32 ✅
- **TP 3RR**: 23886.87 ✅
- **TP 3.5RR**: 23872.41 ✅
- **TP 4RR**: 23857.96 ✅
- **TP 4.5RR**: 23843.50 ❌
- **TP 5RR**: 23829.05 ❌
- **PnL**: -28.91 points (-1.0R)
- **MFE**: 117.65 points
- **MAE**: 33.07 points

### Trade #1127 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-13 09:15:00
- **FVG 5m**: 24246.28 - 24249.05
- **Entrée**: 24237.95 @ 2025-08-13 09:16:00
- **Stop Loss**: 24261.18
- **Risk**: 23.23 points
- **TP 1RR**: 24214.71 ✅
- **TP 1.5RR**: 24203.09 ✅
- **TP 2RR**: 24191.48 ✅
- **TP 2.5RR**: 24179.86 ✅
- **TP 3RR**: 24168.24 ✅
- **TP 3.5RR**: 24156.63 ✅
- **TP 4RR**: 24145.01 ✅
- **TP 4.5RR**: 24133.39 ✅
- **TP 5RR**: 24121.78 ✅
- **PnL**: 116.17 points (5.0R)
- **MFE**: 149.47 points
- **MAE**: 4.54 points

### Trade #1128 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-13 09:15:00
- **FVG 5m**: 24246.28 - 24249.05
- **Entrée**: 24237.95 @ 2025-08-13 09:16:00
- **Stop Loss**: 24261.18
- **Risk**: 23.23 points
- **TP 1RR**: 24214.71 ✅
- **TP 1.5RR**: 24203.09 ✅
- **TP 2RR**: 24191.48 ✅
- **TP 2.5RR**: 24179.86 ✅
- **TP 3RR**: 24168.24 ✅
- **TP 3.5RR**: 24156.63 ✅
- **TP 4RR**: 24145.01 ✅
- **TP 4.5RR**: 24133.39 ✅
- **TP 5RR**: 24121.78 ✅
- **PnL**: 116.17 points (5.0R)
- **MFE**: 149.47 points
- **MAE**: 4.54 points

### Trade #1129 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-13 10:15:00
- **FVG 5m**: 24182.15 - 24192.25
- **Entrée**: 24194.27 @ 2025-08-13 10:43:00
- **Stop Loss**: 24170.06
- **Risk**: 24.21 points
- **TP 1RR**: 24218.48 ❌
- **TP 1.5RR**: 24230.58 ❌
- **TP 2RR**: 24242.69 ❌
- **TP 2.5RR**: 24254.79 ❌
- **TP 3RR**: 24266.90 ❌
- **TP 3.5RR**: 24279.00 ❌
- **TP 4RR**: 24291.11 ❌
- **TP 4.5RR**: 24303.21 ❌
- **TP 5RR**: 24315.32 ❌
- **PnL**: -24.21 points (-1.0R)
- **MFE**: 1.26 points
- **MAE**: 24.49 points

### Trade #1130 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-13 10:30:00
- **FVG 5m**: 24182.15 - 24192.25
- **Entrée**: 24194.27 @ 2025-08-13 10:43:00
- **Stop Loss**: 24170.06
- **Risk**: 24.21 points
- **TP 1RR**: 24218.48 ❌
- **TP 1.5RR**: 24230.58 ❌
- **TP 2RR**: 24242.69 ❌
- **TP 2.5RR**: 24254.79 ❌
- **TP 3RR**: 24266.90 ❌
- **TP 3.5RR**: 24279.00 ❌
- **TP 4RR**: 24291.11 ❌
- **TP 4.5RR**: 24303.21 ❌
- **TP 5RR**: 24315.32 ❌
- **PnL**: -24.21 points (-1.0R)
- **MFE**: 1.26 points
- **MAE**: 24.49 points

### Trade #1131 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24192.75 - 24195.28
- **Entrée**: 24105.14 @ 2025-08-14 07:31:00
- **Stop Loss**: 24207.37
- **Risk**: 102.23 points
- **TP 1RR**: 24002.91 ❌
- **TP 1.5RR**: 23951.80 ❌
- **TP 2RR**: 23900.68 ❌
- **TP 2.5RR**: 23849.56 ❌
- **TP 3RR**: 23798.45 ❌
- **TP 3.5RR**: 23747.33 ❌
- **TP 4RR**: 23696.22 ❌
- **TP 4.5RR**: 23645.10 ❌
- **TP 5RR**: 23593.99 ❌
- **PnL**: -102.23 points (-1.0R)
- **MFE**: 76.25 points
- **MAE**: 108.31 points

### Trade #1132 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24192.75 - 24195.28
- **Entrée**: 24105.14 @ 2025-08-14 07:31:00
- **Stop Loss**: 24207.37
- **Risk**: 102.23 points
- **TP 1RR**: 24002.91 ❌
- **TP 1.5RR**: 23951.80 ❌
- **TP 2RR**: 23900.68 ❌
- **TP 2.5RR**: 23849.56 ❌
- **TP 3RR**: 23798.45 ❌
- **TP 3.5RR**: 23747.33 ❌
- **TP 4RR**: 23696.22 ❌
- **TP 4.5RR**: 23645.10 ❌
- **TP 5RR**: 23593.99 ❌
- **PnL**: -102.23 points (-1.0R)
- **MFE**: 76.25 points
- **MAE**: 108.31 points

### Trade #1133 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24192.75 - 24195.28
- **Entrée**: 24105.14 @ 2025-08-14 07:31:00
- **Stop Loss**: 24207.37
- **Risk**: 102.23 points
- **TP 1RR**: 24002.91 ❌
- **TP 1.5RR**: 23951.80 ❌
- **TP 2RR**: 23900.68 ❌
- **TP 2.5RR**: 23849.56 ❌
- **TP 3RR**: 23798.45 ❌
- **TP 3.5RR**: 23747.33 ❌
- **TP 4RR**: 23696.22 ❌
- **TP 4.5RR**: 23645.10 ❌
- **TP 5RR**: 23593.99 ❌
- **PnL**: -102.23 points (-1.0R)
- **MFE**: 76.25 points
- **MAE**: 108.31 points

### Trade #1134 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24192.75 - 24195.28
- **Entrée**: 24105.14 @ 2025-08-14 07:31:00
- **Stop Loss**: 24207.37
- **Risk**: 102.23 points
- **TP 1RR**: 24002.91 ❌
- **TP 1.5RR**: 23951.80 ❌
- **TP 2RR**: 23900.68 ❌
- **TP 2.5RR**: 23849.56 ❌
- **TP 3RR**: 23798.45 ❌
- **TP 3.5RR**: 23747.33 ❌
- **TP 4RR**: 23696.22 ❌
- **TP 4.5RR**: 23645.10 ❌
- **TP 5RR**: 23593.99 ❌
- **PnL**: -102.23 points (-1.0R)
- **MFE**: 76.25 points
- **MAE**: 108.31 points

### Trade #1135 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24062.22 - 24181.90
- **Entrée**: 24188.71 @ 2025-08-14 08:51:00
- **Stop Loss**: 24050.19
- **Risk**: 138.52 points
- **TP 1RR**: 24327.23 ❌
- **TP 1.5RR**: 24396.49 ❌
- **TP 2RR**: 24465.76 ❌
- **TP 2.5RR**: 24535.02 ❌
- **TP 3RR**: 24604.28 ❌
- **TP 3.5RR**: 24673.54 ❌
- **TP 4RR**: 24742.80 ❌
- **TP 4.5RR**: 24812.06 ❌
- **TP 5RR**: 24881.32 ❌
- **PnL**: -138.52 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 140.12 points

### Trade #1136 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24062.22 - 24181.90
- **Entrée**: 24188.71 @ 2025-08-14 08:51:00
- **Stop Loss**: 24050.19
- **Risk**: 138.52 points
- **TP 1RR**: 24327.23 ❌
- **TP 1.5RR**: 24396.49 ❌
- **TP 2RR**: 24465.76 ❌
- **TP 2.5RR**: 24535.02 ❌
- **TP 3RR**: 24604.28 ❌
- **TP 3.5RR**: 24673.54 ❌
- **TP 4RR**: 24742.80 ❌
- **TP 4.5RR**: 24812.06 ❌
- **TP 5RR**: 24881.32 ❌
- **PnL**: -138.52 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 140.12 points

### Trade #1137 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24062.22 - 24181.90
- **Entrée**: 24188.71 @ 2025-08-14 08:51:00
- **Stop Loss**: 24050.19
- **Risk**: 138.52 points
- **TP 1RR**: 24327.23 ❌
- **TP 1.5RR**: 24396.49 ❌
- **TP 2RR**: 24465.76 ❌
- **TP 2.5RR**: 24535.02 ❌
- **TP 3RR**: 24604.28 ❌
- **TP 3.5RR**: 24673.54 ❌
- **TP 4RR**: 24742.80 ❌
- **TP 4.5RR**: 24812.06 ❌
- **TP 5RR**: 24881.32 ❌
- **PnL**: -138.52 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 140.12 points

### Trade #1138 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24062.22 - 24181.90
- **Entrée**: 24188.71 @ 2025-08-14 08:51:00
- **Stop Loss**: 24050.19
- **Risk**: 138.52 points
- **TP 1RR**: 24327.23 ❌
- **TP 1.5RR**: 24396.49 ❌
- **TP 2RR**: 24465.76 ❌
- **TP 2.5RR**: 24535.02 ❌
- **TP 3RR**: 24604.28 ❌
- **TP 3.5RR**: 24673.54 ❌
- **TP 4RR**: 24742.80 ❌
- **TP 4.5RR**: 24812.06 ❌
- **TP 5RR**: 24881.32 ❌
- **PnL**: -138.52 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 140.12 points

### Trade #1139 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24062.22 - 24181.90
- **Entrée**: 24188.71 @ 2025-08-14 08:51:00
- **Stop Loss**: 24050.19
- **Risk**: 138.52 points
- **TP 1RR**: 24327.23 ❌
- **TP 1.5RR**: 24396.49 ❌
- **TP 2RR**: 24465.76 ❌
- **TP 2.5RR**: 24535.02 ❌
- **TP 3RR**: 24604.28 ❌
- **TP 3.5RR**: 24673.54 ❌
- **TP 4RR**: 24742.80 ❌
- **TP 4.5RR**: 24812.06 ❌
- **TP 5RR**: 24881.32 ❌
- **PnL**: -138.52 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 140.12 points

### Trade #1140 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24062.22 - 24181.90
- **Entrée**: 24188.71 @ 2025-08-14 08:51:00
- **Stop Loss**: 24050.19
- **Risk**: 138.52 points
- **TP 1RR**: 24327.23 ❌
- **TP 1.5RR**: 24396.49 ❌
- **TP 2RR**: 24465.76 ❌
- **TP 2.5RR**: 24535.02 ❌
- **TP 3RR**: 24604.28 ❌
- **TP 3.5RR**: 24673.54 ❌
- **TP 4RR**: 24742.80 ❌
- **TP 4.5RR**: 24812.06 ❌
- **TP 5RR**: 24881.32 ❌
- **PnL**: -138.52 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 140.12 points

### Trade #1141 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 09:45:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24211.67
- **Risk**: 26.49 points
- **TP 1RR**: 24158.69 ✅
- **TP 1.5RR**: 24145.44 ✅
- **TP 2RR**: 24132.20 ✅
- **TP 2.5RR**: 24118.95 ✅
- **TP 3RR**: 24105.70 ✅
- **TP 3.5RR**: 24092.46 ❌
- **TP 4RR**: 24079.21 ❌
- **TP 4.5RR**: 24065.97 ❌
- **TP 5RR**: 24052.72 ❌
- **PnL**: -26.49 points (-1.0R)
- **MFE**: 85.84 points
- **MAE**: 27.27 points

### Trade #1142 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 09:45:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24211.67
- **Risk**: 26.49 points
- **TP 1RR**: 24158.69 ✅
- **TP 1.5RR**: 24145.44 ✅
- **TP 2RR**: 24132.20 ✅
- **TP 2.5RR**: 24118.95 ✅
- **TP 3RR**: 24105.70 ✅
- **TP 3.5RR**: 24092.46 ❌
- **TP 4RR**: 24079.21 ❌
- **TP 4.5RR**: 24065.97 ❌
- **TP 5RR**: 24052.72 ❌
- **PnL**: -26.49 points (-1.0R)
- **MFE**: 85.84 points
- **MAE**: 27.27 points

### Trade #1143 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 09:45:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24211.67
- **Risk**: 26.49 points
- **TP 1RR**: 24158.69 ✅
- **TP 1.5RR**: 24145.44 ✅
- **TP 2RR**: 24132.20 ✅
- **TP 2.5RR**: 24118.95 ✅
- **TP 3RR**: 24105.70 ✅
- **TP 3.5RR**: 24092.46 ❌
- **TP 4RR**: 24079.21 ❌
- **TP 4.5RR**: 24065.97 ❌
- **TP 5RR**: 24052.72 ❌
- **PnL**: -26.49 points (-1.0R)
- **MFE**: 85.84 points
- **MAE**: 27.27 points

### Trade #1144 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-15 08:45:00
- **FVG 5m**: 24135.69 - 24138.97
- **Entrée**: 24051.62 @ 2025-08-15 08:46:00
- **Stop Loss**: 24151.04
- **Risk**: 99.43 points
- **TP 1RR**: 23952.19 ✅
- **TP 1.5RR**: 23902.48 ✅
- **TP 2RR**: 23852.77 ✅
- **TP 2.5RR**: 23803.05 ✅
- **TP 3RR**: 23753.34 ✅
- **TP 3.5RR**: 23703.63 ✅
- **TP 4RR**: 23653.91 ✅
- **TP 4.5RR**: 23604.20 ✅
- **TP 5RR**: 23554.49 ✅
- **PnL**: 497.13 points (5.0R)
- **MFE**: 498.39 points
- **MAE**: 66.65 points

### Trade #1145 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-15 08:45:00
- **FVG 5m**: 24135.69 - 24138.97
- **Entrée**: 24051.62 @ 2025-08-15 08:46:00
- **Stop Loss**: 24151.04
- **Risk**: 99.43 points
- **TP 1RR**: 23952.19 ✅
- **TP 1.5RR**: 23902.48 ✅
- **TP 2RR**: 23852.77 ✅
- **TP 2.5RR**: 23803.05 ✅
- **TP 3RR**: 23753.34 ✅
- **TP 3.5RR**: 23703.63 ✅
- **TP 4RR**: 23653.91 ✅
- **TP 4.5RR**: 23604.20 ✅
- **TP 5RR**: 23554.49 ✅
- **PnL**: 497.13 points (5.0R)
- **MFE**: 498.39 points
- **MAE**: 66.65 points

### Trade #1146 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-15 09:00:00
- **FVG 5m**: 24041.77 - 24071.06
- **Entrée**: 24077.62 @ 2025-08-15 09:03:00
- **Stop Loss**: 24029.75
- **Risk**: 47.87 points
- **TP 1RR**: 24125.50 ❌
- **TP 1.5RR**: 24149.43 ❌
- **TP 2RR**: 24173.37 ❌
- **TP 2.5RR**: 24197.30 ❌
- **TP 3RR**: 24221.24 ❌
- **TP 3.5RR**: 24245.18 ❌
- **TP 4RR**: 24269.11 ❌
- **TP 4.5RR**: 24293.05 ❌
- **TP 5RR**: 24316.99 ❌
- **PnL**: -47.87 points (-1.0R)
- **MFE**: 39.89 points
- **MAE**: 52.52 points

### Trade #1147 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-15 09:00:00
- **FVG 5m**: 24041.77 - 24071.06
- **Entrée**: 24077.62 @ 2025-08-15 09:03:00
- **Stop Loss**: 24029.75
- **Risk**: 47.87 points
- **TP 1RR**: 24125.50 ❌
- **TP 1.5RR**: 24149.43 ❌
- **TP 2RR**: 24173.37 ❌
- **TP 2.5RR**: 24197.30 ❌
- **TP 3RR**: 24221.24 ❌
- **TP 3.5RR**: 24245.18 ❌
- **TP 4RR**: 24269.11 ❌
- **TP 4.5RR**: 24293.05 ❌
- **TP 5RR**: 24316.99 ❌
- **PnL**: -47.87 points (-1.0R)
- **MFE**: 39.89 points
- **MAE**: 52.52 points

### Trade #1148 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 03:30:00
- **FVG 5m**: 24010.97 - 24018.29
- **Entrée**: 24020.06 @ 2025-08-18 03:34:00
- **Stop Loss**: 23998.96
- **Risk**: 21.09 points
- **TP 1RR**: 24041.15 ❌
- **TP 1.5RR**: 24051.70 ❌
- **TP 2RR**: 24062.25 ❌
- **TP 2.5RR**: 24072.79 ❌
- **TP 3RR**: 24083.34 ❌
- **TP 3.5RR**: 24093.89 ❌
- **TP 4RR**: 24104.44 ❌
- **TP 4.5RR**: 24114.98 ❌
- **TP 5RR**: 24125.53 ❌
- **PnL**: -21.09 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 22.47 points

### Trade #1149 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 03:30:00
- **FVG 5m**: 24010.97 - 24018.29
- **Entrée**: 24020.06 @ 2025-08-18 03:34:00
- **Stop Loss**: 23998.96
- **Risk**: 21.09 points
- **TP 1RR**: 24041.15 ❌
- **TP 1.5RR**: 24051.70 ❌
- **TP 2RR**: 24062.25 ❌
- **TP 2.5RR**: 24072.79 ❌
- **TP 3RR**: 24083.34 ❌
- **TP 3.5RR**: 24093.89 ❌
- **TP 4RR**: 24104.44 ❌
- **TP 4.5RR**: 24114.98 ❌
- **TP 5RR**: 24125.53 ❌
- **PnL**: -21.09 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 22.47 points

### Trade #1150 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 09:45:00
- **FVG 5m**: 24004.40 - 24007.69
- **Entrée**: 24014.00 @ 2025-08-18 09:53:00
- **Stop Loss**: 23992.40
- **Risk**: 21.60 points
- **TP 1RR**: 24035.60 ❌
- **TP 1.5RR**: 24046.39 ❌
- **TP 2RR**: 24057.19 ❌
- **TP 2.5RR**: 24067.99 ❌
- **TP 3RR**: 24078.79 ❌
- **TP 3.5RR**: 24089.59 ❌
- **TP 4RR**: 24100.38 ❌
- **TP 4.5RR**: 24111.18 ❌
- **TP 5RR**: 24121.98 ❌
- **PnL**: -21.60 points (-1.0R)
- **MFE**: 5.81 points
- **MAE**: 23.73 points

### Trade #1151 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 09:45:00
- **FVG 5m**: 24004.40 - 24007.69
- **Entrée**: 24014.00 @ 2025-08-18 09:53:00
- **Stop Loss**: 23992.40
- **Risk**: 21.60 points
- **TP 1RR**: 24035.60 ❌
- **TP 1.5RR**: 24046.39 ❌
- **TP 2RR**: 24057.19 ❌
- **TP 2.5RR**: 24067.99 ❌
- **TP 3RR**: 24078.79 ❌
- **TP 3.5RR**: 24089.59 ❌
- **TP 4RR**: 24100.38 ❌
- **TP 4.5RR**: 24111.18 ❌
- **TP 5RR**: 24121.98 ❌
- **PnL**: -21.60 points (-1.0R)
- **MFE**: 5.81 points
- **MAE**: 23.73 points

### Trade #1152 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 09:45:00
- **FVG 5m**: 24004.40 - 24007.69
- **Entrée**: 24014.00 @ 2025-08-18 09:53:00
- **Stop Loss**: 23992.40
- **Risk**: 21.60 points
- **TP 1RR**: 24035.60 ❌
- **TP 1.5RR**: 24046.39 ❌
- **TP 2RR**: 24057.19 ❌
- **TP 2.5RR**: 24067.99 ❌
- **TP 3RR**: 24078.79 ❌
- **TP 3.5RR**: 24089.59 ❌
- **TP 4RR**: 24100.38 ❌
- **TP 4.5RR**: 24111.18 ❌
- **TP 5RR**: 24121.98 ❌
- **PnL**: -21.60 points (-1.0R)
- **MFE**: 5.81 points
- **MAE**: 23.73 points

### Trade #1153 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 02:30:00
- **FVG 5m**: 23979.16 - 23989.51
- **Entrée**: 23990.01 @ 2025-08-19 02:38:00
- **Stop Loss**: 23967.17
- **Risk**: 22.85 points
- **TP 1RR**: 24012.86 ✅
- **TP 1.5RR**: 24024.28 ✅
- **TP 2RR**: 24035.71 ✅
- **TP 2.5RR**: 24047.13 ❌
- **TP 3RR**: 24058.55 ❌
- **TP 3.5RR**: 24069.97 ❌
- **TP 4RR**: 24081.40 ❌
- **TP 4.5RR**: 24092.82 ❌
- **TP 5RR**: 24104.24 ❌
- **PnL**: -22.85 points (-1.0R)
- **MFE**: 50.50 points
- **MAE**: 31.31 points

### Trade #1154 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 03:00:00
- **FVG 5m**: 23993.04 - 23998.60
- **Entrée**: 23984.21 @ 2025-08-19 03:11:00
- **Stop Loss**: 24010.60
- **Risk**: 26.39 points
- **TP 1RR**: 23957.82 ❌
- **TP 1.5RR**: 23944.62 ❌
- **TP 2RR**: 23931.43 ❌
- **TP 2.5RR**: 23918.23 ❌
- **TP 3RR**: 23905.04 ❌
- **TP 3.5RR**: 23891.84 ❌
- **TP 4RR**: 23878.65 ❌
- **TP 4.5RR**: 23865.45 ❌
- **TP 5RR**: 23852.25 ❌
- **PnL**: -26.39 points (-1.0R)
- **MFE**: 3.53 points
- **MAE**: 27.77 points

### Trade #1155 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23934.72 - 23941.79
- **Entrée**: 23819.59 @ 2025-08-19 09:46:00
- **Stop Loss**: 23953.76
- **Risk**: 134.17 points
- **TP 1RR**: 23685.42 ✅
- **TP 1.5RR**: 23618.34 ✅
- **TP 2RR**: 23551.25 ✅
- **TP 2.5RR**: 23484.17 ✅
- **TP 3RR**: 23417.08 ✅
- **TP 3.5RR**: 23350.00 ✅
- **TP 4RR**: 23282.92 ✅
- **TP 4.5RR**: 23215.83 ❌
- **TP 5RR**: 23148.75 ❌
- **PnL**: -134.17 points (-1.0R)
- **MFE**: 556.46 points
- **MAE**: 149.72 points

### Trade #1156 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23934.72 - 23941.79
- **Entrée**: 23819.59 @ 2025-08-19 09:46:00
- **Stop Loss**: 23953.76
- **Risk**: 134.17 points
- **TP 1RR**: 23685.42 ✅
- **TP 1.5RR**: 23618.34 ✅
- **TP 2RR**: 23551.25 ✅
- **TP 2.5RR**: 23484.17 ✅
- **TP 3RR**: 23417.08 ✅
- **TP 3.5RR**: 23350.00 ✅
- **TP 4RR**: 23282.92 ✅
- **TP 4.5RR**: 23215.83 ❌
- **TP 5RR**: 23148.75 ❌
- **PnL**: -134.17 points (-1.0R)
- **MFE**: 556.46 points
- **MAE**: 149.72 points

### Trade #1157 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23934.72 - 23941.79
- **Entrée**: 23819.59 @ 2025-08-19 09:46:00
- **Stop Loss**: 23953.76
- **Risk**: 134.17 points
- **TP 1RR**: 23685.42 ✅
- **TP 1.5RR**: 23618.34 ✅
- **TP 2RR**: 23551.25 ✅
- **TP 2.5RR**: 23484.17 ✅
- **TP 3RR**: 23417.08 ✅
- **TP 3.5RR**: 23350.00 ✅
- **TP 4RR**: 23282.92 ✅
- **TP 4.5RR**: 23215.83 ❌
- **TP 5RR**: 23148.75 ❌
- **PnL**: -134.17 points (-1.0R)
- **MFE**: 556.46 points
- **MAE**: 149.72 points

### Trade #1158 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23934.72 - 23941.79
- **Entrée**: 23819.59 @ 2025-08-19 09:46:00
- **Stop Loss**: 23953.76
- **Risk**: 134.17 points
- **TP 1RR**: 23685.42 ✅
- **TP 1.5RR**: 23618.34 ✅
- **TP 2RR**: 23551.25 ✅
- **TP 2.5RR**: 23484.17 ✅
- **TP 3RR**: 23417.08 ✅
- **TP 3.5RR**: 23350.00 ✅
- **TP 4RR**: 23282.92 ✅
- **TP 4.5RR**: 23215.83 ❌
- **TP 5RR**: 23148.75 ❌
- **PnL**: -134.17 points (-1.0R)
- **MFE**: 556.46 points
- **MAE**: 149.72 points

### Trade #1159 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23934.72 - 23941.79
- **Entrée**: 23819.59 @ 2025-08-19 09:46:00
- **Stop Loss**: 23953.76
- **Risk**: 134.17 points
- **TP 1RR**: 23685.42 ✅
- **TP 1.5RR**: 23618.34 ✅
- **TP 2RR**: 23551.25 ✅
- **TP 2.5RR**: 23484.17 ✅
- **TP 3RR**: 23417.08 ✅
- **TP 3.5RR**: 23350.00 ✅
- **TP 4RR**: 23282.92 ✅
- **TP 4.5RR**: 23215.83 ❌
- **TP 5RR**: 23148.75 ❌
- **PnL**: -134.17 points (-1.0R)
- **MFE**: 556.46 points
- **MAE**: 149.72 points

### Trade #1160 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 12:45:00
- **FVG 5m**: 23735.27 - 23738.55
- **Entrée**: 23742.59 @ 2025-08-19 12:57:00
- **Stop Loss**: 23723.40
- **Risk**: 19.19 points
- **TP 1RR**: 23761.78 ❌
- **TP 1.5RR**: 23771.37 ❌
- **TP 2RR**: 23780.97 ❌
- **TP 2.5RR**: 23790.56 ❌
- **TP 3RR**: 23800.16 ❌
- **TP 3.5RR**: 23809.75 ❌
- **TP 4RR**: 23819.35 ❌
- **TP 4.5RR**: 23828.94 ❌
- **TP 5RR**: 23838.53 ❌
- **PnL**: -19.19 points (-1.0R)
- **MFE**: 7.57 points
- **MAE**: 25.00 points

### Trade #1161 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 14:15:00
- **FVG 5m**: 23671.64 - 23690.83
- **Entrée**: 23694.87 @ 2025-08-19 14:24:00
- **Stop Loss**: 23659.81
- **Risk**: 35.06 points
- **TP 1RR**: 23729.93 ❌
- **TP 1.5RR**: 23747.46 ❌
- **TP 2RR**: 23765.00 ❌
- **TP 2.5RR**: 23782.53 ❌
- **TP 3RR**: 23800.06 ❌
- **TP 3.5RR**: 23817.59 ❌
- **TP 4RR**: 23835.12 ❌
- **TP 4.5RR**: 23852.66 ❌
- **TP 5RR**: 23870.19 ❌
- **PnL**: -35.06 points (-1.0R)
- **MFE**: 25.25 points
- **MAE**: 36.61 points

### Trade #1162 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-20 03:00:00
- **FVG 5m**: 23644.37 - 23647.40
- **Entrée**: 23634.53 @ 2025-08-20 03:01:00
- **Stop Loss**: 23659.23
- **Risk**: 24.70 points
- **TP 1RR**: 23609.83 ✅
- **TP 1.5RR**: 23597.48 ❌
- **TP 2RR**: 23585.13 ❌
- **TP 2.5RR**: 23572.78 ❌
- **TP 3RR**: 23560.43 ❌
- **TP 3.5RR**: 23548.08 ❌
- **TP 4RR**: 23535.73 ❌
- **TP 4.5RR**: 23523.38 ❌
- **TP 5RR**: 23511.03 ❌
- **PnL**: -24.70 points (-1.0R)
- **MFE**: 31.81 points
- **MAE**: 24.74 points

### Trade #1163 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-20 06:15:00
- **FVG 5m**: 23659.52 - 23671.64
- **Entrée**: 23656.24 @ 2025-08-20 06:26:00
- **Stop Loss**: 23683.48
- **Risk**: 27.24 points
- **TP 1RR**: 23629.00 ✅
- **TP 1.5RR**: 23615.39 ✅
- **TP 2RR**: 23601.77 ✅
- **TP 2.5RR**: 23588.15 ✅
- **TP 3RR**: 23574.53 ✅
- **TP 3.5RR**: 23560.91 ✅
- **TP 4RR**: 23547.29 ✅
- **TP 4.5RR**: 23533.67 ✅
- **TP 5RR**: 23520.06 ✅
- **PnL**: 136.18 points (5.0R)
- **MFE**: 145.68 points
- **MAE**: 12.12 points

### Trade #1164 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-20 08:45:00
- **FVG 5m**: 23641.34 - 23650.43
- **Entrée**: 23512.33 @ 2025-08-20 08:46:00
- **Stop Loss**: 23662.26
- **Risk**: 149.93 points
- **TP 1RR**: 23362.40 ✅
- **TP 1.5RR**: 23287.43 ✅
- **TP 2RR**: 23212.47 ❌
- **TP 2.5RR**: 23137.51 ❌
- **TP 3RR**: 23062.54 ❌
- **TP 3.5RR**: 22987.58 ❌
- **TP 4RR**: 22912.61 ❌
- **TP 4.5RR**: 22837.65 ❌
- **TP 5RR**: 22762.68 ❌
- **PnL**: -149.93 points (-1.0R)
- **MFE**: 249.19 points
- **MAE**: 187.59 points

### Trade #1165 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 09:45:00
- **FVG 5m**: 23358.07 - 23394.42
- **Entrée**: 23399.72 @ 2025-08-20 10:18:00
- **Stop Loss**: 23346.39
- **Risk**: 53.34 points
- **TP 1RR**: 23453.06 ✅
- **TP 1.5RR**: 23479.73 ✅
- **TP 2RR**: 23506.40 ✅
- **TP 2.5RR**: 23533.07 ✅
- **TP 3RR**: 23559.74 ✅
- **TP 3.5RR**: 23586.41 ✅
- **TP 4RR**: 23613.08 ❌
- **TP 4.5RR**: 23639.74 ❌
- **TP 5RR**: 23666.41 ❌
- **PnL**: -53.34 points (-1.0R)
- **MFE**: 200.97 points
- **MAE**: 56.55 points

### Trade #1166 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 14:30:00
- **FVG 5m**: 23471.93 - 23483.55
- **Entrée**: 23565.60 @ 2025-08-20 14:31:00
- **Stop Loss**: 23460.20
- **Risk**: 105.40 points
- **TP 1RR**: 23671.01 ❌
- **TP 1.5RR**: 23723.71 ❌
- **TP 2RR**: 23776.41 ❌
- **TP 2.5RR**: 23829.11 ❌
- **TP 3RR**: 23881.82 ❌
- **TP 3.5RR**: 23934.52 ❌
- **TP 4RR**: 23987.22 ❌
- **TP 4.5RR**: 24039.92 ❌
- **TP 5RR**: 24092.62 ❌
- **PnL**: -105.40 points (-1.0R)
- **MFE**: 35.09 points
- **MAE**: 106.54 points

### Trade #1167 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 14:30:00
- **FVG 5m**: 23471.93 - 23483.55
- **Entrée**: 23565.60 @ 2025-08-20 14:31:00
- **Stop Loss**: 23460.20
- **Risk**: 105.40 points
- **TP 1RR**: 23671.01 ❌
- **TP 1.5RR**: 23723.71 ❌
- **TP 2RR**: 23776.41 ❌
- **TP 2.5RR**: 23829.11 ❌
- **TP 3RR**: 23881.82 ❌
- **TP 3.5RR**: 23934.52 ❌
- **TP 4RR**: 23987.22 ❌
- **TP 4.5RR**: 24039.92 ❌
- **TP 5RR**: 24092.62 ❌
- **PnL**: -105.40 points (-1.0R)
- **MFE**: 35.09 points
- **MAE**: 106.54 points

### Trade #1168 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-21 03:45:00
- **FVG 5m**: 23564.34 - 23567.62
- **Entrée**: 23558.53 @ 2025-08-21 03:49:00
- **Stop Loss**: 23579.41
- **Risk**: 20.87 points
- **TP 1RR**: 23537.66 ✅
- **TP 1.5RR**: 23527.22 ✅
- **TP 2RR**: 23516.79 ✅
- **TP 2.5RR**: 23506.35 ✅
- **TP 3RR**: 23495.91 ✅
- **TP 3.5RR**: 23485.48 ✅
- **TP 4RR**: 23475.04 ✅
- **TP 4.5RR**: 23464.60 ✅
- **TP 5RR**: 23454.17 ✅
- **PnL**: 104.36 points (5.0R)
- **MFE**: 106.80 points
- **MAE**: 6.82 points

### Trade #1169 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-21 05:45:00
- **FVG 5m**: 23527.48 - 23531.52
- **Entrée**: 23534.55 @ 2025-08-21 05:46:00
- **Stop Loss**: 23515.71
- **Risk**: 18.83 points
- **TP 1RR**: 23553.38 ✅
- **TP 1.5RR**: 23562.80 ✅
- **TP 2RR**: 23572.21 ❌
- **TP 2.5RR**: 23581.63 ❌
- **TP 3RR**: 23591.05 ❌
- **TP 3.5RR**: 23600.46 ❌
- **TP 4RR**: 23609.88 ❌
- **TP 4.5RR**: 23619.30 ❌
- **TP 5RR**: 23628.71 ❌
- **PnL**: -18.83 points (-1.0R)
- **MFE**: 30.80 points
- **MAE**: 22.47 points

### Trade #1170 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-21 09:00:00
- **FVG 5m**: 23459.56 - 23462.09
- **Entrée**: 23488.09 @ 2025-08-21 09:02:00
- **Stop Loss**: 23447.83
- **Risk**: 40.26 points
- **TP 1RR**: 23528.35 ✅
- **TP 1.5RR**: 23548.48 ✅
- **TP 2RR**: 23568.61 ✅
- **TP 2.5RR**: 23588.74 ❌
- **TP 3RR**: 23608.87 ❌
- **TP 3.5RR**: 23629.00 ❌
- **TP 4RR**: 23649.13 ❌
- **TP 4.5RR**: 23669.26 ❌
- **TP 5RR**: 23689.39 ❌
- **PnL**: -40.26 points (-1.0R)
- **MFE**: 91.40 points
- **MAE**: 40.90 points

### Trade #1171 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-21 09:00:00
- **FVG 5m**: 23459.56 - 23462.09
- **Entrée**: 23488.09 @ 2025-08-21 09:02:00
- **Stop Loss**: 23447.83
- **Risk**: 40.26 points
- **TP 1RR**: 23528.35 ✅
- **TP 1.5RR**: 23548.48 ✅
- **TP 2RR**: 23568.61 ✅
- **TP 2.5RR**: 23588.74 ❌
- **TP 3RR**: 23608.87 ❌
- **TP 3.5RR**: 23629.00 ❌
- **TP 4RR**: 23649.13 ❌
- **TP 4.5RR**: 23669.26 ❌
- **TP 5RR**: 23689.39 ❌
- **PnL**: -40.26 points (-1.0R)
- **MFE**: 91.40 points
- **MAE**: 40.90 points

### Trade #1172 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-21 09:00:00
- **FVG 5m**: 23459.56 - 23462.09
- **Entrée**: 23488.09 @ 2025-08-21 09:02:00
- **Stop Loss**: 23447.83
- **Risk**: 40.26 points
- **TP 1RR**: 23528.35 ✅
- **TP 1.5RR**: 23548.48 ✅
- **TP 2RR**: 23568.61 ✅
- **TP 2.5RR**: 23588.74 ❌
- **TP 3RR**: 23608.87 ❌
- **TP 3.5RR**: 23629.00 ❌
- **TP 4RR**: 23649.13 ❌
- **TP 4.5RR**: 23669.26 ❌
- **TP 5RR**: 23689.39 ❌
- **PnL**: -40.26 points (-1.0R)
- **MFE**: 91.40 points
- **MAE**: 40.90 points

### Trade #1173 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-21 12:30:00
- **FVG 5m**: 23372.71 - 23382.30
- **Entrée**: 23396.95 @ 2025-08-21 12:31:00
- **Stop Loss**: 23361.02
- **Risk**: 35.92 points
- **TP 1RR**: 23432.87 ✅
- **TP 1.5RR**: 23450.83 ✅
- **TP 2RR**: 23468.80 ✅
- **TP 2.5RR**: 23486.76 ❌
- **TP 3RR**: 23504.72 ❌
- **TP 3.5RR**: 23522.68 ❌
- **TP 4RR**: 23540.64 ❌
- **TP 4.5RR**: 23558.61 ❌
- **TP 5RR**: 23576.57 ❌
- **PnL**: -35.92 points (-1.0R)
- **MFE**: 88.62 points
- **MAE**: 37.11 points

### Trade #1174 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-22 01:45:00
- **FVG 5m**: 23363.62 - 23376.24
- **Entrée**: 23379.53 @ 2025-08-22 02:00:00
- **Stop Loss**: 23351.94
- **Risk**: 27.59 points
- **TP 1RR**: 23407.11 ✅
- **TP 1.5RR**: 23420.91 ✅
- **TP 2RR**: 23434.70 ✅
- **TP 2.5RR**: 23448.50 ✅
- **TP 3RR**: 23462.29 ✅
- **TP 3.5RR**: 23476.08 ✅
- **TP 4RR**: 23489.88 ✅
- **TP 4.5RR**: 23503.67 ✅
- **TP 5RR**: 23517.47 ✅
- **PnL**: 137.94 points (5.0R)
- **MFE**: 150.98 points
- **MAE**: 3.53 points

### Trade #1175 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-22 02:45:00
- **FVG 5m**: 23350.74 - 23359.83
- **Entrée**: 23405.78 @ 2025-08-22 02:46:00
- **Stop Loss**: 23339.07
- **Risk**: 66.72 points
- **TP 1RR**: 23472.50 ✅
- **TP 1.5RR**: 23505.86 ✅
- **TP 2RR**: 23539.21 ✅
- **TP 2.5RR**: 23572.57 ✅
- **TP 3RR**: 23605.93 ✅
- **TP 3.5RR**: 23639.29 ✅
- **TP 4RR**: 23672.64 ✅
- **TP 4.5RR**: 23706.00 ✅
- **TP 5RR**: 23739.36 ✅
- **PnL**: 333.58 points (5.0R)
- **MFE**: 342.61 points
- **MAE**: 1.01 points

### Trade #1176 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-22 07:30:00
- **FVG 5m**: 23490.36 - 23493.90
- **Entrée**: 23489.86 @ 2025-08-22 07:32:00
- **Stop Loss**: 23505.65
- **Risk**: 15.79 points
- **TP 1RR**: 23474.07 ✅
- **TP 1.5RR**: 23466.18 ✅
- **TP 2RR**: 23458.29 ✅
- **TP 2.5RR**: 23450.39 ✅
- **TP 3RR**: 23442.50 ✅
- **TP 3.5RR**: 23434.61 ❌
- **TP 4RR**: 23426.71 ❌
- **TP 4.5RR**: 23418.82 ❌
- **TP 5RR**: 23410.93 ❌
- **PnL**: -15.79 points (-1.0R)
- **MFE**: 54.53 points
- **MAE**: 26.01 points

### Trade #1177 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-24 22:30:00
- **FVG 5m**: 23763.54 - 23770.61
- **Entrée**: 23772.88 @ 2025-08-24 22:36:00
- **Stop Loss**: 23751.66
- **Risk**: 21.22 points
- **TP 1RR**: 23794.11 ✅
- **TP 1.5RR**: 23804.72 ❌
- **TP 2RR**: 23815.33 ❌
- **TP 2.5RR**: 23825.94 ❌
- **TP 3RR**: 23836.55 ❌
- **TP 3.5RR**: 23847.17 ❌
- **TP 4RR**: 23857.78 ❌
- **TP 4.5RR**: 23868.39 ❌
- **TP 5RR**: 23879.00 ❌
- **PnL**: -21.22 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 31.31 points

### Trade #1178 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 08:30:00
- **FVG 5m**: 23718.35 - 23724.66
- **Entrée**: 23704.97 @ 2025-08-25 08:31:00
- **Stop Loss**: 23736.52
- **Risk**: 31.56 points
- **TP 1RR**: 23673.41 ❌
- **TP 1.5RR**: 23657.64 ❌
- **TP 2RR**: 23641.86 ❌
- **TP 2.5RR**: 23626.08 ❌
- **TP 3RR**: 23610.30 ❌
- **TP 3.5RR**: 23594.52 ❌
- **TP 4RR**: 23578.75 ❌
- **TP 4.5RR**: 23562.97 ❌
- **TP 5RR**: 23547.19 ❌
- **PnL**: -31.56 points (-1.0R)
- **MFE**: 29.54 points
- **MAE**: 39.64 points

### Trade #1179 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 08:30:00
- **FVG 5m**: 23718.35 - 23724.66
- **Entrée**: 23704.97 @ 2025-08-25 08:31:00
- **Stop Loss**: 23736.52
- **Risk**: 31.56 points
- **TP 1RR**: 23673.41 ❌
- **TP 1.5RR**: 23657.64 ❌
- **TP 2RR**: 23641.86 ❌
- **TP 2.5RR**: 23626.08 ❌
- **TP 3RR**: 23610.30 ❌
- **TP 3.5RR**: 23594.52 ❌
- **TP 4RR**: 23578.75 ❌
- **TP 4.5RR**: 23562.97 ❌
- **TP 5RR**: 23547.19 ❌
- **PnL**: -31.56 points (-1.0R)
- **MFE**: 29.54 points
- **MAE**: 39.64 points

### Trade #1180 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 08:30:00
- **FVG 5m**: 23713.05 - 23728.70
- **Entrée**: 23730.72 @ 2025-08-25 08:37:00
- **Stop Loss**: 23701.19
- **Risk**: 29.53 points
- **TP 1RR**: 23760.25 ❌
- **TP 1.5RR**: 23775.02 ❌
- **TP 2RR**: 23789.78 ❌
- **TP 2.5RR**: 23804.55 ❌
- **TP 3RR**: 23819.31 ❌
- **TP 3.5RR**: 23834.08 ❌
- **TP 4RR**: 23848.84 ❌
- **TP 4.5RR**: 23863.61 ❌
- **TP 5RR**: 23878.37 ❌
- **PnL**: -29.53 points (-1.0R)
- **MFE**: 13.89 points
- **MAE**: 29.54 points

### Trade #1181 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 08:45:00
- **FVG 5m**: 23713.05 - 23728.70
- **Entrée**: 23734.51 @ 2025-08-25 08:56:00
- **Stop Loss**: 23701.19
- **Risk**: 33.32 points
- **TP 1RR**: 23767.83 ✅
- **TP 1.5RR**: 23784.48 ✅
- **TP 2RR**: 23801.14 ✅
- **TP 2.5RR**: 23817.80 ✅
- **TP 3RR**: 23834.46 ✅
- **TP 3.5RR**: 23851.12 ❌
- **TP 4RR**: 23867.78 ❌
- **TP 4.5RR**: 23884.43 ❌
- **TP 5RR**: 23901.09 ❌
- **PnL**: -33.32 points (-1.0R)
- **MFE**: 115.63 points
- **MAE**: 92.66 points

### Trade #1182 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 08:45:00
- **FVG 5m**: 23713.05 - 23728.70
- **Entrée**: 23734.51 @ 2025-08-25 08:56:00
- **Stop Loss**: 23701.19
- **Risk**: 33.32 points
- **TP 1RR**: 23767.83 ✅
- **TP 1.5RR**: 23784.48 ✅
- **TP 2RR**: 23801.14 ✅
- **TP 2.5RR**: 23817.80 ✅
- **TP 3RR**: 23834.46 ✅
- **TP 3.5RR**: 23851.12 ❌
- **TP 4RR**: 23867.78 ❌
- **TP 4.5RR**: 23884.43 ❌
- **TP 5RR**: 23901.09 ❌
- **PnL**: -33.32 points (-1.0R)
- **MFE**: 115.63 points
- **MAE**: 92.66 points

### Trade #1183 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 09:00:00
- **FVG 5m**: 23713.05 - 23728.70
- **Entrée**: 23751.93 @ 2025-08-25 09:01:00
- **Stop Loss**: 23701.19
- **Risk**: 50.74 points
- **TP 1RR**: 23802.67 ✅
- **TP 1.5RR**: 23828.04 ✅
- **TP 2RR**: 23853.40 ❌
- **TP 2.5RR**: 23878.77 ❌
- **TP 3RR**: 23904.14 ❌
- **TP 3.5RR**: 23929.51 ❌
- **TP 4RR**: 23954.88 ❌
- **TP 4.5RR**: 23980.25 ❌
- **TP 5RR**: 24005.62 ❌
- **PnL**: -50.74 points (-1.0R)
- **MFE**: 98.21 points
- **MAE**: 110.08 points

### Trade #1184 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 13:15:00
- **FVG 5m**: 23808.48 - 23811.26
- **Entrée**: 23806.72 @ 2025-08-25 13:16:00
- **Stop Loss**: 23823.17
- **Risk**: 16.45 points
- **TP 1RR**: 23790.27 ✅
- **TP 1.5RR**: 23782.04 ✅
- **TP 2RR**: 23773.82 ✅
- **TP 2.5RR**: 23765.59 ✅
- **TP 3RR**: 23757.37 ✅
- **TP 3.5RR**: 23749.14 ✅
- **TP 4RR**: 23740.92 ✅
- **TP 4.5RR**: 23732.69 ✅
- **TP 5RR**: 23724.47 ✅
- **PnL**: 82.25 points (5.0R)
- **MFE**: 85.08 points
- **MAE**: 1.51 points

### Trade #1185 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-26 05:00:00
- **FVG 5m**: 23704.46 - 23708.00
- **Entrée**: 23718.35 @ 2025-08-26 05:01:00
- **Stop Loss**: 23692.61
- **Risk**: 25.74 points
- **TP 1RR**: 23744.09 ❌
- **TP 1.5RR**: 23756.96 ❌
- **TP 2RR**: 23769.83 ❌
- **TP 2.5RR**: 23782.70 ❌
- **TP 3RR**: 23795.56 ❌
- **TP 3.5RR**: 23808.43 ❌
- **TP 4RR**: 23821.30 ❌
- **TP 4.5RR**: 23834.17 ❌
- **TP 5RR**: 23847.04 ❌
- **PnL**: -25.74 points (-1.0R)
- **MFE**: 19.95 points
- **MAE**: 30.04 points

### Trade #1186 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-26 08:45:00
- **FVG 5m**: 23692.09 - 23699.16
- **Entrée**: 23706.99 @ 2025-08-26 08:51:00
- **Stop Loss**: 23680.25
- **Risk**: 26.74 points
- **TP 1RR**: 23733.73 ✅
- **TP 1.5RR**: 23747.10 ✅
- **TP 2RR**: 23760.47 ✅
- **TP 2.5RR**: 23773.84 ✅
- **TP 3RR**: 23787.21 ✅
- **TP 3.5RR**: 23800.59 ✅
- **TP 4RR**: 23813.96 ✅
- **TP 4.5RR**: 23827.33 ✅
- **TP 5RR**: 23840.70 ✅
- **PnL**: 133.71 points (5.0R)
- **MFE**: 136.34 points
- **MAE**: 15.65 points

### Trade #1187 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-26 10:15:00
- **FVG 5m**: 23761.52 - 23768.09
- **Entrée**: 23745.62 @ 2025-08-26 10:16:00
- **Stop Loss**: 23779.97
- **Risk**: 34.35 points
- **TP 1RR**: 23711.26 ❌
- **TP 1.5RR**: 23694.09 ❌
- **TP 2RR**: 23676.91 ❌
- **TP 2.5RR**: 23659.73 ❌
- **TP 3RR**: 23642.55 ❌
- **TP 3.5RR**: 23625.38 ❌
- **TP 4RR**: 23608.20 ❌
- **TP 4.5RR**: 23591.02 ❌
- **TP 5RR**: 23573.85 ❌
- **PnL**: -34.35 points (-1.0R)
- **MFE**: 19.69 points
- **MAE**: 37.87 points

### Trade #1188 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-26 12:45:00
- **FVG 5m**: 23748.90 - 23751.68
- **Entrée**: 23758.49 @ 2025-08-26 13:10:00
- **Stop Loss**: 23737.02
- **Risk**: 21.47 points
- **TP 1RR**: 23779.96 ✅
- **TP 1.5RR**: 23790.70 ✅
- **TP 2RR**: 23801.43 ✅
- **TP 2.5RR**: 23812.16 ✅
- **TP 3RR**: 23822.90 ✅
- **TP 3.5RR**: 23833.63 ✅
- **TP 4RR**: 23844.37 ✅
- **TP 4.5RR**: 23855.10 ✅
- **TP 5RR**: 23865.84 ❌
- **PnL**: -21.47 points (-1.0R)
- **MFE**: 104.53 points
- **MAE**: 29.79 points

### Trade #1189 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-26 14:30:00
- **FVG 5m**: 23783.24 - 23789.55
- **Entrée**: 23782.73 @ 2025-08-26 14:39:00
- **Stop Loss**: 23801.44
- **Risk**: 18.71 points
- **TP 1RR**: 23764.02 ❌
- **TP 1.5RR**: 23754.66 ❌
- **TP 2RR**: 23745.31 ❌
- **TP 2.5RR**: 23735.95 ❌
- **TP 3RR**: 23726.60 ❌
- **TP 3.5RR**: 23717.24 ❌
- **TP 4RR**: 23707.88 ❌
- **TP 4.5RR**: 23698.53 ❌
- **TP 5RR**: 23689.17 ❌
- **PnL**: -18.71 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 38.88 points

### Trade #1190 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-26 14:30:00
- **FVG 5m**: 23783.24 - 23789.55
- **Entrée**: 23782.73 @ 2025-08-26 14:39:00
- **Stop Loss**: 23801.44
- **Risk**: 18.71 points
- **TP 1RR**: 23764.02 ❌
- **TP 1.5RR**: 23754.66 ❌
- **TP 2RR**: 23745.31 ❌
- **TP 2.5RR**: 23735.95 ❌
- **TP 3RR**: 23726.60 ❌
- **TP 3.5RR**: 23717.24 ❌
- **TP 4RR**: 23707.88 ❌
- **TP 4.5RR**: 23698.53 ❌
- **TP 5RR**: 23689.17 ❌
- **PnL**: -18.71 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 38.88 points

### Trade #1191 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 09:15:00
- **FVG 5m**: 23763.54 - 23769.10
- **Entrée**: 23812.52 @ 2025-08-27 09:16:00
- **Stop Loss**: 23751.66
- **Risk**: 60.86 points
- **TP 1RR**: 23873.39 ✅
- **TP 1.5RR**: 23903.82 ✅
- **TP 2RR**: 23934.25 ❌
- **TP 2.5RR**: 23964.68 ❌
- **TP 3RR**: 23995.11 ❌
- **TP 3.5RR**: 24025.54 ❌
- **TP 4RR**: 24055.97 ❌
- **TP 4.5RR**: 24086.40 ❌
- **TP 5RR**: 24116.83 ❌
- **PnL**: -60.86 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 142.40 points

### Trade #1192 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 09:15:00
- **FVG 5m**: 23763.54 - 23769.10
- **Entrée**: 23812.52 @ 2025-08-27 09:16:00
- **Stop Loss**: 23751.66
- **Risk**: 60.86 points
- **TP 1RR**: 23873.39 ✅
- **TP 1.5RR**: 23903.82 ✅
- **TP 2RR**: 23934.25 ❌
- **TP 2.5RR**: 23964.68 ❌
- **TP 3RR**: 23995.11 ❌
- **TP 3.5RR**: 24025.54 ❌
- **TP 4RR**: 24055.97 ❌
- **TP 4.5RR**: 24086.40 ❌
- **TP 5RR**: 24116.83 ❌
- **PnL**: -60.86 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 142.40 points

### Trade #1193 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 10:45:00
- **FVG 5m**: 23763.54 - 23769.10
- **Entrée**: 23833.73 @ 2025-08-27 10:46:00
- **Stop Loss**: 23751.66
- **Risk**: 82.07 points
- **TP 1RR**: 23915.80 ✅
- **TP 1.5RR**: 23956.84 ❌
- **TP 2RR**: 23997.87 ❌
- **TP 2.5RR**: 24038.91 ❌
- **TP 3RR**: 24079.94 ❌
- **TP 3.5RR**: 24120.98 ❌
- **TP 4RR**: 24162.01 ❌
- **TP 4.5RR**: 24203.05 ❌
- **TP 5RR**: 24244.08 ❌
- **PnL**: -82.07 points (-1.0R)
- **MFE**: 89.88 points
- **MAE**: 163.60 points

### Trade #1194 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 11:30:00
- **FVG 5m**: 23802.93 - 23824.64
- **Entrée**: 23826.41 @ 2025-08-27 11:48:00
- **Stop Loss**: 23791.03
- **Risk**: 35.38 points
- **TP 1RR**: 23861.79 ✅
- **TP 1.5RR**: 23879.48 ✅
- **TP 2RR**: 23897.17 ❌
- **TP 2.5RR**: 23914.86 ❌
- **TP 3RR**: 23932.55 ❌
- **TP 3.5RR**: 23950.25 ❌
- **TP 4RR**: 23967.94 ❌
- **TP 4.5RR**: 23985.63 ❌
- **TP 5RR**: 24003.32 ❌
- **PnL**: -35.38 points (-1.0R)
- **MFE**: 65.39 points
- **MAE**: 39.64 points

### Trade #1195 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 13:45:00
- **FVG 5m**: 23862.77 - 23882.21
- **Entrée**: 23862.26 @ 2025-08-27 13:54:00
- **Stop Loss**: 23894.15
- **Risk**: 31.89 points
- **TP 1RR**: 23830.37 ✅
- **TP 1.5RR**: 23814.43 ✅
- **TP 2RR**: 23798.49 ✅
- **TP 2.5RR**: 23782.54 ❌
- **TP 3RR**: 23766.60 ❌
- **TP 3.5RR**: 23750.66 ❌
- **TP 4RR**: 23734.71 ❌
- **TP 4.5RR**: 23718.77 ❌
- **TP 5RR**: 23702.83 ❌
- **PnL**: -31.89 points (-1.0R)
- **MFE**: 75.49 points
- **MAE**: 61.35 points

### Trade #1196 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 13:45:00
- **FVG 5m**: 23862.77 - 23882.21
- **Entrée**: 23862.26 @ 2025-08-27 13:54:00
- **Stop Loss**: 23894.15
- **Risk**: 31.89 points
- **TP 1RR**: 23830.37 ✅
- **TP 1.5RR**: 23814.43 ✅
- **TP 2RR**: 23798.49 ✅
- **TP 2.5RR**: 23782.54 ❌
- **TP 3RR**: 23766.60 ❌
- **TP 3.5RR**: 23750.66 ❌
- **TP 4RR**: 23734.71 ❌
- **TP 4.5RR**: 23718.77 ❌
- **TP 5RR**: 23702.83 ❌
- **PnL**: -31.89 points (-1.0R)
- **MFE**: 75.49 points
- **MAE**: 61.35 points

### Trade #1197 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23840.04 - 23850.39
- **Entrée**: 23790.56 @ 2025-08-27 15:20:00
- **Stop Loss**: 23862.32
- **Risk**: 71.76 points
- **TP 1RR**: 23718.80 ✅
- **TP 1.5RR**: 23682.91 ✅
- **TP 2RR**: 23647.03 ❌
- **TP 2.5RR**: 23611.15 ❌
- **TP 3RR**: 23575.27 ❌
- **TP 3.5RR**: 23539.39 ❌
- **TP 4RR**: 23503.51 ❌
- **TP 4.5RR**: 23467.63 ❌
- **TP 5RR**: 23431.75 ❌
- **PnL**: -71.76 points (-1.0R)
- **MFE**: 123.71 points
- **MAE**: 79.02 points

### Trade #1198 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23840.04 - 23850.39
- **Entrée**: 23790.56 @ 2025-08-27 15:20:00
- **Stop Loss**: 23862.32
- **Risk**: 71.76 points
- **TP 1RR**: 23718.80 ✅
- **TP 1.5RR**: 23682.91 ✅
- **TP 2RR**: 23647.03 ❌
- **TP 2.5RR**: 23611.15 ❌
- **TP 3RR**: 23575.27 ❌
- **TP 3.5RR**: 23539.39 ❌
- **TP 4RR**: 23503.51 ❌
- **TP 4.5RR**: 23467.63 ❌
- **TP 5RR**: 23431.75 ❌
- **PnL**: -71.76 points (-1.0R)
- **MFE**: 123.71 points
- **MAE**: 79.02 points

### Trade #1199 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23840.04 - 23850.39
- **Entrée**: 23790.56 @ 2025-08-27 15:20:00
- **Stop Loss**: 23862.32
- **Risk**: 71.76 points
- **TP 1RR**: 23718.80 ✅
- **TP 1.5RR**: 23682.91 ✅
- **TP 2RR**: 23647.03 ❌
- **TP 2.5RR**: 23611.15 ❌
- **TP 3RR**: 23575.27 ❌
- **TP 3.5RR**: 23539.39 ❌
- **TP 4RR**: 23503.51 ❌
- **TP 4.5RR**: 23467.63 ❌
- **TP 5RR**: 23431.75 ❌
- **PnL**: -71.76 points (-1.0R)
- **MFE**: 123.71 points
- **MAE**: 79.02 points

### Trade #1200 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23840.04 - 23850.39
- **Entrée**: 23790.56 @ 2025-08-27 15:20:00
- **Stop Loss**: 23862.32
- **Risk**: 71.76 points
- **TP 1RR**: 23718.80 ✅
- **TP 1.5RR**: 23682.91 ✅
- **TP 2RR**: 23647.03 ❌
- **TP 2.5RR**: 23611.15 ❌
- **TP 3RR**: 23575.27 ❌
- **TP 3.5RR**: 23539.39 ❌
- **TP 4RR**: 23503.51 ❌
- **TP 4.5RR**: 23467.63 ❌
- **TP 5RR**: 23431.75 ❌
- **PnL**: -71.76 points (-1.0R)
- **MFE**: 123.71 points
- **MAE**: 79.02 points

### Trade #1201 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23840.04 - 23850.39
- **Entrée**: 23790.56 @ 2025-08-27 15:20:00
- **Stop Loss**: 23862.32
- **Risk**: 71.76 points
- **TP 1RR**: 23718.80 ✅
- **TP 1.5RR**: 23682.91 ✅
- **TP 2RR**: 23647.03 ❌
- **TP 2.5RR**: 23611.15 ❌
- **TP 3RR**: 23575.27 ❌
- **TP 3.5RR**: 23539.39 ❌
- **TP 4RR**: 23503.51 ❌
- **TP 4.5RR**: 23467.63 ❌
- **TP 5RR**: 23431.75 ❌
- **PnL**: -71.76 points (-1.0R)
- **MFE**: 123.71 points
- **MAE**: 79.02 points

### Trade #1202 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23840.04 - 23850.39
- **Entrée**: 23790.56 @ 2025-08-27 15:20:00
- **Stop Loss**: 23862.32
- **Risk**: 71.76 points
- **TP 1RR**: 23718.80 ✅
- **TP 1.5RR**: 23682.91 ✅
- **TP 2RR**: 23647.03 ❌
- **TP 2.5RR**: 23611.15 ❌
- **TP 3RR**: 23575.27 ❌
- **TP 3.5RR**: 23539.39 ❌
- **TP 4RR**: 23503.51 ❌
- **TP 4.5RR**: 23467.63 ❌
- **TP 5RR**: 23431.75 ❌
- **PnL**: -71.76 points (-1.0R)
- **MFE**: 123.71 points
- **MAE**: 79.02 points

### Trade #1203 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23840.04 - 23850.39
- **Entrée**: 23790.56 @ 2025-08-27 15:20:00
- **Stop Loss**: 23862.32
- **Risk**: 71.76 points
- **TP 1RR**: 23718.80 ✅
- **TP 1.5RR**: 23682.91 ✅
- **TP 2RR**: 23647.03 ❌
- **TP 2.5RR**: 23611.15 ❌
- **TP 3RR**: 23575.27 ❌
- **TP 3.5RR**: 23539.39 ❌
- **TP 4RR**: 23503.51 ❌
- **TP 4.5RR**: 23467.63 ❌
- **TP 5RR**: 23431.75 ❌
- **PnL**: -71.76 points (-1.0R)
- **MFE**: 123.71 points
- **MAE**: 79.02 points

### Trade #1204 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23840.04 - 23850.39
- **Entrée**: 23790.56 @ 2025-08-27 15:20:00
- **Stop Loss**: 23862.32
- **Risk**: 71.76 points
- **TP 1RR**: 23718.80 ✅
- **TP 1.5RR**: 23682.91 ✅
- **TP 2RR**: 23647.03 ❌
- **TP 2.5RR**: 23611.15 ❌
- **TP 3RR**: 23575.27 ❌
- **TP 3.5RR**: 23539.39 ❌
- **TP 4RR**: 23503.51 ❌
- **TP 4.5RR**: 23467.63 ❌
- **TP 5RR**: 23431.75 ❌
- **PnL**: -71.76 points (-1.0R)
- **MFE**: 123.71 points
- **MAE**: 79.02 points

### Trade #1205 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23829.19 - 23842.32
- **Entrée**: 23851.66 @ 2025-08-27 15:16:00
- **Stop Loss**: 23817.27
- **Risk**: 34.38 points
- **TP 1RR**: 23886.04 ❌
- **TP 1.5RR**: 23903.23 ❌
- **TP 2RR**: 23920.43 ❌
- **TP 2.5RR**: 23937.62 ❌
- **TP 3RR**: 23954.81 ❌
- **TP 3.5RR**: 23972.00 ❌
- **TP 4RR**: 23989.20 ❌
- **TP 4.5RR**: 24006.39 ❌
- **TP 5RR**: 24023.58 ❌
- **PnL**: -34.38 points (-1.0R)
- **MFE**: 71.96 points
- **MAE**: 61.10 points

### Trade #1206 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23829.19 - 23842.32
- **Entrée**: 23851.66 @ 2025-08-27 15:16:00
- **Stop Loss**: 23817.27
- **Risk**: 34.38 points
- **TP 1RR**: 23886.04 ❌
- **TP 1.5RR**: 23903.23 ❌
- **TP 2RR**: 23920.43 ❌
- **TP 2.5RR**: 23937.62 ❌
- **TP 3RR**: 23954.81 ❌
- **TP 3.5RR**: 23972.00 ❌
- **TP 4RR**: 23989.20 ❌
- **TP 4.5RR**: 24006.39 ❌
- **TP 5RR**: 24023.58 ❌
- **PnL**: -34.38 points (-1.0R)
- **MFE**: 71.96 points
- **MAE**: 61.10 points

### Trade #1207 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23829.19 - 23842.32
- **Entrée**: 23851.66 @ 2025-08-27 15:16:00
- **Stop Loss**: 23817.27
- **Risk**: 34.38 points
- **TP 1RR**: 23886.04 ❌
- **TP 1.5RR**: 23903.23 ❌
- **TP 2RR**: 23920.43 ❌
- **TP 2.5RR**: 23937.62 ❌
- **TP 3RR**: 23954.81 ❌
- **TP 3.5RR**: 23972.00 ❌
- **TP 4RR**: 23989.20 ❌
- **TP 4.5RR**: 24006.39 ❌
- **TP 5RR**: 24023.58 ❌
- **PnL**: -34.38 points (-1.0R)
- **MFE**: 71.96 points
- **MAE**: 61.10 points

### Trade #1208 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 08:45:00
- **FVG 5m**: 23886.25 - 23915.03
- **Entrée**: 23852.92 @ 2025-08-28 08:50:00
- **Stop Loss**: 23926.99
- **Risk**: 74.07 points
- **TP 1RR**: 23778.85 ❌
- **TP 1.5RR**: 23741.82 ❌
- **TP 2RR**: 23704.79 ❌
- **TP 2.5RR**: 23667.75 ❌
- **TP 3RR**: 23630.72 ❌
- **TP 3.5RR**: 23593.69 ❌
- **TP 4RR**: 23556.65 ❌
- **TP 4.5RR**: 23519.62 ❌
- **TP 5RR**: 23482.59 ❌
- **PnL**: -74.07 points (-1.0R)
- **MFE**: 46.96 points
- **MAE**: 81.55 points

### Trade #1209 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 08:45:00
- **FVG 5m**: 23886.25 - 23915.03
- **Entrée**: 23852.92 @ 2025-08-28 08:50:00
- **Stop Loss**: 23926.99
- **Risk**: 74.07 points
- **TP 1RR**: 23778.85 ❌
- **TP 1.5RR**: 23741.82 ❌
- **TP 2RR**: 23704.79 ❌
- **TP 2.5RR**: 23667.75 ❌
- **TP 3RR**: 23630.72 ❌
- **TP 3.5RR**: 23593.69 ❌
- **TP 4RR**: 23556.65 ❌
- **TP 4.5RR**: 23519.62 ❌
- **TP 5RR**: 23482.59 ❌
- **PnL**: -74.07 points (-1.0R)
- **MFE**: 46.96 points
- **MAE**: 81.55 points

### Trade #1210 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 10:00:00
- **FVG 5m**: 23863.02 - 23891.55
- **Entrée**: 23953.40 @ 2025-08-28 10:01:00
- **Stop Loss**: 23851.09
- **Risk**: 102.32 points
- **TP 1RR**: 24055.72 ❌
- **TP 1.5RR**: 24106.88 ❌
- **TP 2RR**: 24158.04 ❌
- **TP 2.5RR**: 24209.20 ❌
- **TP 3RR**: 24260.36 ❌
- **TP 3.5RR**: 24311.52 ❌
- **TP 4RR**: 24362.68 ❌
- **TP 4.5RR**: 24413.84 ❌
- **TP 5RR**: 24464.99 ❌
- **PnL**: -102.32 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 107.05 points

### Trade #1211 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 10:00:00
- **FVG 5m**: 23863.02 - 23891.55
- **Entrée**: 23953.40 @ 2025-08-28 10:01:00
- **Stop Loss**: 23851.09
- **Risk**: 102.32 points
- **TP 1RR**: 24055.72 ❌
- **TP 1.5RR**: 24106.88 ❌
- **TP 2RR**: 24158.04 ❌
- **TP 2.5RR**: 24209.20 ❌
- **TP 3RR**: 24260.36 ❌
- **TP 3.5RR**: 24311.52 ❌
- **TP 4RR**: 24362.68 ❌
- **TP 4.5RR**: 24413.84 ❌
- **TP 5RR**: 24464.99 ❌
- **PnL**: -102.32 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 107.05 points

### Trade #1212 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 11:15:00
- **FVG 5m**: 23942.04 - 23958.96
- **Entrée**: 23960.98 @ 2025-08-28 11:16:00
- **Stop Loss**: 23930.07
- **Risk**: 30.91 points
- **TP 1RR**: 23991.89 ✅
- **TP 1.5RR**: 24007.34 ✅
- **TP 2RR**: 24022.79 ✅
- **TP 2.5RR**: 24038.25 ✅
- **TP 3RR**: 24053.70 ❌
- **TP 3.5RR**: 24069.15 ❌
- **TP 4RR**: 24084.61 ❌
- **TP 4.5RR**: 24100.06 ❌
- **TP 5RR**: 24115.51 ❌
- **PnL**: -30.91 points (-1.0R)
- **MFE**: 78.52 points
- **MAE**: 31.05 points

### Trade #1213 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 11:15:00
- **FVG 5m**: 23942.04 - 23958.96
- **Entrée**: 23960.98 @ 2025-08-28 11:16:00
- **Stop Loss**: 23930.07
- **Risk**: 30.91 points
- **TP 1RR**: 23991.89 ✅
- **TP 1.5RR**: 24007.34 ✅
- **TP 2RR**: 24022.79 ✅
- **TP 2.5RR**: 24038.25 ✅
- **TP 3RR**: 24053.70 ❌
- **TP 3.5RR**: 24069.15 ❌
- **TP 4RR**: 24084.61 ❌
- **TP 4.5RR**: 24100.06 ❌
- **TP 5RR**: 24115.51 ❌
- **PnL**: -30.91 points (-1.0R)
- **MFE**: 78.52 points
- **MAE**: 31.05 points

### Trade #1214 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 11:15:00
- **FVG 5m**: 23942.04 - 23958.96
- **Entrée**: 23960.98 @ 2025-08-28 11:16:00
- **Stop Loss**: 23930.07
- **Risk**: 30.91 points
- **TP 1RR**: 23991.89 ✅
- **TP 1.5RR**: 24007.34 ✅
- **TP 2RR**: 24022.79 ✅
- **TP 2.5RR**: 24038.25 ✅
- **TP 3RR**: 24053.70 ❌
- **TP 3.5RR**: 24069.15 ❌
- **TP 4RR**: 24084.61 ❌
- **TP 4.5RR**: 24100.06 ❌
- **TP 5RR**: 24115.51 ❌
- **PnL**: -30.91 points (-1.0R)
- **MFE**: 78.52 points
- **MAE**: 31.05 points

### Trade #1215 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-29 08:45:00
- **FVG 5m**: 23873.37 - 23881.45
- **Entrée**: 23788.29 @ 2025-08-29 08:46:00
- **Stop Loss**: 23893.39
- **Risk**: 105.10 points
- **TP 1RR**: 23683.18 ✅
- **TP 1.5RR**: 23630.63 ✅
- **TP 2RR**: 23578.08 ✅
- **TP 2.5RR**: 23525.52 ✅
- **TP 3RR**: 23472.97 ✅
- **TP 3.5RR**: 23420.42 ✅
- **TP 4RR**: 23367.87 ✅
- **TP 4.5RR**: 23315.32 ✅
- **TP 5RR**: 23262.76 ✅
- **PnL**: 525.52 points (5.0R)
- **MFE**: 535.00 points
- **MAE**: 20.45 points

### Trade #1216 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-29 09:00:00
- **FVG 5m**: 23873.37 - 23881.45
- **Entrée**: 23759.25 @ 2025-08-29 09:01:00
- **Stop Loss**: 23893.39
- **Risk**: 134.14 points
- **TP 1RR**: 23625.11 ✅
- **TP 1.5RR**: 23558.04 ✅
- **TP 2RR**: 23490.97 ✅
- **TP 2.5RR**: 23423.90 ✅
- **TP 3RR**: 23356.83 ✅
- **TP 3.5RR**: 23289.76 ✅
- **TP 4RR**: 23222.69 ❌
- **TP 4.5RR**: 23155.62 ❌
- **TP 5RR**: 23088.56 ❌
- **PnL**: -134.14 points (-1.0R)
- **MFE**: 505.96 points
- **MAE**: 134.82 points

### Trade #1217 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-29 09:00:00
- **FVG 5m**: 23873.37 - 23881.45
- **Entrée**: 23759.25 @ 2025-08-29 09:01:00
- **Stop Loss**: 23893.39
- **Risk**: 134.14 points
- **TP 1RR**: 23625.11 ✅
- **TP 1.5RR**: 23558.04 ✅
- **TP 2RR**: 23490.97 ✅
- **TP 2.5RR**: 23423.90 ✅
- **TP 3RR**: 23356.83 ✅
- **TP 3.5RR**: 23289.76 ✅
- **TP 4RR**: 23222.69 ❌
- **TP 4.5RR**: 23155.62 ❌
- **TP 5RR**: 23088.56 ❌
- **PnL**: -134.14 points (-1.0R)
- **MFE**: 505.96 points
- **MAE**: 134.82 points

### Trade #1218 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 09:15:00
- **FVG 5m**: 23704.72 - 23713.30
- **Entrée**: 23714.06 @ 2025-08-29 09:20:00
- **Stop Loss**: 23692.86
- **Risk**: 21.19 points
- **TP 1RR**: 23735.25 ❌
- **TP 1.5RR**: 23745.85 ❌
- **TP 2RR**: 23756.45 ❌
- **TP 2.5RR**: 23767.04 ❌
- **TP 3RR**: 23777.64 ❌
- **TP 3.5RR**: 23788.24 ❌
- **TP 4RR**: 23798.83 ❌
- **TP 4.5RR**: 23809.43 ❌
- **TP 5RR**: 23820.03 ❌
- **PnL**: -21.19 points (-1.0R)
- **MFE**: 17.42 points
- **MAE**: 34.08 points

### Trade #1219 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 09:45:00
- **FVG 5m**: 23704.72 - 23713.30
- **Entrée**: 23718.10 @ 2025-08-29 10:22:00
- **Stop Loss**: 23692.86
- **Risk**: 25.23 points
- **TP 1RR**: 23743.33 ❌
- **TP 1.5RR**: 23755.95 ❌
- **TP 2RR**: 23768.56 ❌
- **TP 2.5RR**: 23781.18 ❌
- **TP 3RR**: 23793.80 ❌
- **TP 3.5RR**: 23806.41 ❌
- **TP 4RR**: 23819.03 ❌
- **TP 4.5RR**: 23831.65 ❌
- **TP 5RR**: 23844.27 ❌
- **PnL**: -25.23 points (-1.0R)
- **MFE**: 13.38 points
- **MAE**: 27.01 points

### Trade #1220 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 09:45:00
- **FVG 5m**: 23704.72 - 23713.30
- **Entrée**: 23718.10 @ 2025-08-29 10:22:00
- **Stop Loss**: 23692.86
- **Risk**: 25.23 points
- **TP 1RR**: 23743.33 ❌
- **TP 1.5RR**: 23755.95 ❌
- **TP 2RR**: 23768.56 ❌
- **TP 2.5RR**: 23781.18 ❌
- **TP 3RR**: 23793.80 ❌
- **TP 3.5RR**: 23806.41 ❌
- **TP 4RR**: 23819.03 ❌
- **TP 4.5RR**: 23831.65 ❌
- **TP 5RR**: 23844.27 ❌
- **PnL**: -25.23 points (-1.0R)
- **MFE**: 13.38 points
- **MAE**: 27.01 points

### Trade #1221 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-31 21:00:00
- **FVG 5m**: 23768.34 - 23772.38
- **Entrée**: 23744.86 @ 2025-08-31 21:01:00
- **Stop Loss**: 23784.27
- **Risk**: 39.41 points
- **TP 1RR**: 23705.45 ✅
- **TP 1.5RR**: 23685.75 ✅
- **TP 2RR**: 23666.05 ✅
- **TP 2.5RR**: 23646.34 ✅
- **TP 3RR**: 23626.64 ✅
- **TP 3.5RR**: 23606.94 ✅
- **TP 4RR**: 23587.24 ✅
- **TP 4.5RR**: 23567.53 ✅
- **TP 5RR**: 23547.83 ✅
- **PnL**: 197.03 points (5.0R)
- **MFE**: 201.73 points
- **MAE**: 2.27 points

### Trade #1222 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 00:15:00
- **FVG 5m**: 23657.25 - 23664.07
- **Entrée**: 23665.83 @ 2025-09-01 00:26:00
- **Stop Loss**: 23645.42
- **Risk**: 20.41 points
- **TP 1RR**: 23686.25 ❌
- **TP 1.5RR**: 23696.45 ❌
- **TP 2RR**: 23706.66 ❌
- **TP 2.5RR**: 23716.87 ❌
- **TP 3RR**: 23727.07 ❌
- **TP 3.5RR**: 23737.28 ❌
- **TP 4RR**: 23747.49 ❌
- **TP 4.5RR**: 23757.69 ❌
- **TP 5RR**: 23767.90 ❌
- **PnL**: -20.41 points (-1.0R)
- **MFE**: 15.65 points
- **MAE**: 26.51 points

### Trade #1223 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 01:30:00
- **FVG 5m**: 23630.74 - 23639.32
- **Entrée**: 23643.62 @ 2025-09-01 01:37:00
- **Stop Loss**: 23618.93
- **Risk**: 24.69 points
- **TP 1RR**: 23668.31 ✅
- **TP 1.5RR**: 23680.65 ✅
- **TP 2RR**: 23693.00 ✅
- **TP 2.5RR**: 23705.35 ✅
- **TP 3RR**: 23717.69 ✅
- **TP 3.5RR**: 23730.04 ✅
- **TP 4RR**: 23742.38 ❌
- **TP 4.5RR**: 23754.73 ❌
- **TP 5RR**: 23767.07 ❌
- **PnL**: -24.69 points (-1.0R)
- **MFE**: 98.72 points
- **MAE**: 25.25 points

### Trade #1224 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 01:30:00
- **FVG 5m**: 23630.74 - 23639.32
- **Entrée**: 23643.62 @ 2025-09-01 01:37:00
- **Stop Loss**: 23618.93
- **Risk**: 24.69 points
- **TP 1RR**: 23668.31 ✅
- **TP 1.5RR**: 23680.65 ✅
- **TP 2RR**: 23693.00 ✅
- **TP 2.5RR**: 23705.35 ✅
- **TP 3RR**: 23717.69 ✅
- **TP 3.5RR**: 23730.04 ✅
- **TP 4RR**: 23742.38 ❌
- **TP 4.5RR**: 23754.73 ❌
- **TP 5RR**: 23767.07 ❌
- **PnL**: -24.69 points (-1.0R)
- **MFE**: 98.72 points
- **MAE**: 25.25 points

### Trade #1225 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 08:30:00
- **FVG 5m**: 23704.46 - 23710.52
- **Entrée**: 23715.07 @ 2025-09-01 08:40:00
- **Stop Loss**: 23692.61
- **Risk**: 22.46 points
- **TP 1RR**: 23737.52 ✅
- **TP 1.5RR**: 23748.75 ❌
- **TP 2RR**: 23759.98 ❌
- **TP 2.5RR**: 23771.21 ❌
- **TP 3RR**: 23782.44 ❌
- **TP 3.5RR**: 23793.66 ❌
- **TP 4RR**: 23804.89 ❌
- **TP 4.5RR**: 23816.12 ❌
- **TP 5RR**: 23827.35 ❌
- **PnL**: -22.46 points (-1.0R)
- **MFE**: 27.27 points
- **MAE**: 22.98 points

### Trade #1226 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 01:00:00
- **FVG 5m**: 23653.46 - 23660.53
- **Entrée**: 23665.08 @ 2025-09-02 01:07:00
- **Stop Loss**: 23641.64
- **Risk**: 23.44 points
- **TP 1RR**: 23688.52 ❌
- **TP 1.5RR**: 23700.24 ❌
- **TP 2RR**: 23711.96 ❌
- **TP 2.5RR**: 23723.68 ❌
- **TP 3RR**: 23735.40 ❌
- **TP 3.5RR**: 23747.12 ❌
- **TP 4RR**: 23758.84 ❌
- **TP 4.5RR**: 23770.56 ❌
- **TP 5RR**: 23782.28 ❌
- **PnL**: -23.44 points (-1.0R)
- **MFE**: 19.19 points
- **MAE**: 25.25 points

### Trade #1227 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 01:45:00
- **FVG 5m**: 23653.46 - 23660.53
- **Entrée**: 23667.85 @ 2025-09-02 01:46:00
- **Stop Loss**: 23641.64
- **Risk**: 26.22 points
- **TP 1RR**: 23694.07 ❌
- **TP 1.5RR**: 23707.18 ❌
- **TP 2RR**: 23720.29 ❌
- **TP 2.5RR**: 23733.40 ❌
- **TP 3RR**: 23746.51 ❌
- **TP 3.5RR**: 23759.62 ❌
- **TP 4RR**: 23772.73 ❌
- **TP 4.5RR**: 23785.83 ❌
- **TP 5RR**: 23798.94 ❌
- **PnL**: -26.22 points (-1.0R)
- **MFE**: 16.41 points
- **MAE**: 28.02 points

### Trade #1228 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 05:15:00
- **FVG 5m**: 23523.69 - 23527.48
- **Entrée**: 23519.90 @ 2025-09-02 05:18:00
- **Stop Loss**: 23539.24
- **Risk**: 19.34 points
- **TP 1RR**: 23500.57 ✅
- **TP 1.5RR**: 23490.90 ✅
- **TP 2RR**: 23481.23 ✅
- **TP 2.5RR**: 23471.56 ✅
- **TP 3RR**: 23461.89 ✅
- **TP 3.5RR**: 23452.22 ✅
- **TP 4RR**: 23442.55 ✅
- **TP 4.5RR**: 23432.88 ✅
- **TP 5RR**: 23423.21 ✅
- **PnL**: 96.69 points (5.0R)
- **MFE**: 101.50 points
- **MAE**: 0.50 points

### Trade #1229 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 07:45:00
- **FVG 5m**: 23373.72 - 23378.26
- **Entrée**: 23382.05 @ 2025-09-02 08:37:00
- **Stop Loss**: 23362.03
- **Risk**: 20.02 points
- **TP 1RR**: 23402.07 ❌
- **TP 1.5RR**: 23412.08 ❌
- **TP 2RR**: 23422.09 ❌
- **TP 2.5RR**: 23432.10 ❌
- **TP 3RR**: 23442.11 ❌
- **TP 3.5RR**: 23452.12 ❌
- **TP 4RR**: 23462.13 ❌
- **TP 4.5RR**: 23472.14 ❌
- **TP 5RR**: 23482.14 ❌
- **PnL**: -20.02 points (-1.0R)
- **MFE**: 10.10 points
- **MAE**: 22.72 points

### Trade #1230 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 08:30:00
- **FVG 5m**: 23365.14 - 23370.44
- **Entrée**: 23382.05 @ 2025-09-02 08:37:00
- **Stop Loss**: 23353.45
- **Risk**: 28.60 points
- **TP 1RR**: 23410.65 ✅
- **TP 1.5RR**: 23424.95 ✅
- **TP 2RR**: 23439.25 ✅
- **TP 2.5RR**: 23453.55 ✅
- **TP 3RR**: 23467.85 ✅
- **TP 3.5RR**: 23482.15 ✅
- **TP 4RR**: 23496.45 ✅
- **TP 4.5RR**: 23510.74 ❌
- **TP 5RR**: 23525.04 ❌
- **PnL**: -28.60 points (-1.0R)
- **MFE**: 128.51 points
- **MAE**: 30.04 points

### Trade #1231 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 08:45:00
- **FVG 5m**: 23331.30 - 23336.35
- **Entrée**: 23411.34 @ 2025-09-02 08:46:00
- **Stop Loss**: 23319.64
- **Risk**: 91.70 points
- **TP 1RR**: 23503.04 ✅
- **TP 1.5RR**: 23548.89 ❌
- **TP 2RR**: 23594.74 ❌
- **TP 2.5RR**: 23640.59 ❌
- **TP 3RR**: 23686.44 ❌
- **TP 3.5RR**: 23732.29 ❌
- **TP 4RR**: 23778.14 ❌
- **TP 4.5RR**: 23823.99 ❌
- **TP 5RR**: 23869.84 ❌
- **PnL**: -91.70 points (-1.0R)
- **MFE**: 99.22 points
- **MAE**: 92.66 points

### Trade #1232 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 08:45:00
- **FVG 5m**: 23331.30 - 23336.35
- **Entrée**: 23411.34 @ 2025-09-02 08:46:00
- **Stop Loss**: 23319.64
- **Risk**: 91.70 points
- **TP 1RR**: 23503.04 ✅
- **TP 1.5RR**: 23548.89 ❌
- **TP 2RR**: 23594.74 ❌
- **TP 2.5RR**: 23640.59 ❌
- **TP 3RR**: 23686.44 ❌
- **TP 3.5RR**: 23732.29 ❌
- **TP 4RR**: 23778.14 ❌
- **TP 4.5RR**: 23823.99 ❌
- **TP 5RR**: 23869.84 ❌
- **PnL**: -91.70 points (-1.0R)
- **MFE**: 99.22 points
- **MAE**: 92.66 points

### Trade #1233 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 09:00:00
- **FVG 5m**: 23429.77 - 23454.01
- **Entrée**: 23420.43 @ 2025-09-02 09:15:00
- **Stop Loss**: 23465.73
- **Risk**: 45.31 points
- **TP 1RR**: 23375.12 ❌
- **TP 1.5RR**: 23352.47 ❌
- **TP 2RR**: 23329.82 ❌
- **TP 2.5RR**: 23307.16 ❌
- **TP 3RR**: 23284.51 ❌
- **TP 3.5RR**: 23261.86 ❌
- **TP 4RR**: 23239.20 ❌
- **TP 4.5RR**: 23216.55 ❌
- **TP 5RR**: 23193.90 ❌
- **PnL**: -45.31 points (-1.0R)
- **MFE**: 3.79 points
- **MAE**: 46.20 points

### Trade #1234 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 09:00:00
- **FVG 5m**: 23429.77 - 23454.01
- **Entrée**: 23420.43 @ 2025-09-02 09:15:00
- **Stop Loss**: 23465.73
- **Risk**: 45.31 points
- **TP 1RR**: 23375.12 ❌
- **TP 1.5RR**: 23352.47 ❌
- **TP 2RR**: 23329.82 ❌
- **TP 2.5RR**: 23307.16 ❌
- **TP 3RR**: 23284.51 ❌
- **TP 3.5RR**: 23261.86 ❌
- **TP 4RR**: 23239.20 ❌
- **TP 4.5RR**: 23216.55 ❌
- **TP 5RR**: 23193.90 ❌
- **PnL**: -45.31 points (-1.0R)
- **MFE**: 3.79 points
- **MAE**: 46.20 points

### Trade #1235 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 14:45:00
- **FVG 5m**: 23434.31 - 23439.11
- **Entrée**: 23466.13 @ 2025-09-02 14:46:00
- **Stop Loss**: 23422.60
- **Risk**: 43.53 points
- **TP 1RR**: 23509.66 ✅
- **TP 1.5RR**: 23531.42 ✅
- **TP 2RR**: 23553.18 ✅
- **TP 2.5RR**: 23574.95 ✅
- **TP 3RR**: 23596.71 ✅
- **TP 3.5RR**: 23618.48 ✅
- **TP 4RR**: 23640.24 ✅
- **TP 4.5RR**: 23662.01 ✅
- **TP 5RR**: 23683.77 ✅
- **PnL**: 217.65 points (5.0R)
- **MFE**: 218.90 points
- **MAE**: 0.50 points

### Trade #1236 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 15:15:00
- **FVG 5m**: 23434.31 - 23439.11
- **Entrée**: 23586.81 @ 2025-09-02 15:16:00
- **Stop Loss**: 23422.60
- **Risk**: 164.21 points
- **TP 1RR**: 23751.02 ✅
- **TP 1.5RR**: 23833.13 ✅
- **TP 2RR**: 23915.23 ✅
- **TP 2.5RR**: 23997.34 ✅
- **TP 3RR**: 24079.45 ✅
- **TP 3.5RR**: 24161.55 ✅
- **TP 4RR**: 24243.66 ✅
- **TP 4.5RR**: 24325.77 ✅
- **TP 5RR**: 24407.87 ✅
- **PnL**: 821.06 points (5.0R)
- **MFE**: 821.94 points
- **MAE**: 57.82 points

### Trade #1237 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 15:15:00
- **FVG 5m**: 23434.31 - 23439.11
- **Entrée**: 23586.81 @ 2025-09-02 15:16:00
- **Stop Loss**: 23422.60
- **Risk**: 164.21 points
- **TP 1RR**: 23751.02 ✅
- **TP 1.5RR**: 23833.13 ✅
- **TP 2RR**: 23915.23 ✅
- **TP 2.5RR**: 23997.34 ✅
- **TP 3RR**: 24079.45 ✅
- **TP 3.5RR**: 24161.55 ✅
- **TP 4RR**: 24243.66 ✅
- **TP 4.5RR**: 24325.77 ✅
- **TP 5RR**: 24407.87 ✅
- **PnL**: 821.06 points (5.0R)
- **MFE**: 821.94 points
- **MAE**: 57.82 points

### Trade #1238 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 22:30:00
- **FVG 5m**: 23549.95 - 23556.26
- **Entrée**: 23559.04 @ 2025-09-02 22:31:00
- **Stop Loss**: 23538.17
- **Risk**: 20.86 points
- **TP 1RR**: 23579.90 ❌
- **TP 1.5RR**: 23590.33 ❌
- **TP 2RR**: 23600.77 ❌
- **TP 2.5RR**: 23611.20 ❌
- **TP 3RR**: 23621.63 ❌
- **TP 3.5RR**: 23632.06 ❌
- **TP 4RR**: 23642.49 ❌
- **TP 4.5RR**: 23652.93 ❌
- **TP 5RR**: 23663.36 ❌
- **PnL**: -20.86 points (-1.0R)
- **MFE**: 2.27 points
- **MAE**: 30.04 points

### Trade #1239 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-03 03:45:00
- **FVG 5m**: 23642.86 - 23645.38
- **Entrée**: 23645.64 @ 2025-09-03 03:56:00
- **Stop Loss**: 23631.04
- **Risk**: 14.60 points
- **TP 1RR**: 23660.24 ❌
- **TP 1.5RR**: 23667.53 ❌
- **TP 2RR**: 23674.83 ❌
- **TP 2.5RR**: 23682.13 ❌
- **TP 3RR**: 23689.43 ❌
- **TP 3.5RR**: 23696.73 ❌
- **TP 4RR**: 23704.03 ❌
- **TP 4.5RR**: 23711.33 ❌
- **TP 5RR**: 23718.63 ❌
- **PnL**: -14.60 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 15.40 points

### Trade #1240 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-03 06:30:00
- **FVG 5m**: 23639.83 - 23642.86
- **Entrée**: 23646.65 @ 2025-09-03 06:31:00
- **Stop Loss**: 23628.01
- **Risk**: 18.64 points
- **TP 1RR**: 23665.28 ✅
- **TP 1.5RR**: 23674.60 ✅
- **TP 2RR**: 23683.92 ✅
- **TP 2.5RR**: 23693.24 ❌
- **TP 3RR**: 23702.56 ❌
- **TP 3.5RR**: 23711.88 ❌
- **TP 4RR**: 23721.19 ❌
- **TP 4.5RR**: 23730.51 ❌
- **TP 5RR**: 23739.83 ❌
- **PnL**: -18.64 points (-1.0R)
- **MFE**: 42.67 points
- **MAE**: 35.85 points

### Trade #1241 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 08:45:00
- **FVG 5m**: 23667.10 - 23670.63
- **Entrée**: 23622.91 @ 2025-09-03 08:46:00
- **Stop Loss**: 23682.47
- **Risk**: 59.55 points
- **TP 1RR**: 23563.36 ❌
- **TP 1.5RR**: 23533.58 ❌
- **TP 2RR**: 23503.81 ❌
- **TP 2.5RR**: 23474.03 ❌
- **TP 3RR**: 23444.25 ❌
- **TP 3.5RR**: 23414.48 ❌
- **TP 4RR**: 23384.70 ❌
- **TP 4.5RR**: 23354.92 ❌
- **TP 5RR**: 23325.15 ❌
- **PnL**: -59.55 points (-1.0R)
- **MFE**: 21.46 points
- **MAE**: 70.19 points

### Trade #1242 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:15:00
- **FVG 5m**: 23644.37 - 23657.00
- **Entrée**: 23639.83 @ 2025-09-03 09:16:00
- **Stop Loss**: 23668.83
- **Risk**: 29.00 points
- **TP 1RR**: 23610.83 ❌
- **TP 1.5RR**: 23596.33 ❌
- **TP 2RR**: 23581.84 ❌
- **TP 2.5RR**: 23567.34 ❌
- **TP 3RR**: 23552.84 ❌
- **TP 3.5RR**: 23538.34 ❌
- **TP 4RR**: 23523.84 ❌
- **TP 4.5RR**: 23509.34 ❌
- **TP 5RR**: 23494.85 ❌
- **PnL**: -29.00 points (-1.0R)
- **MFE**: 3.03 points
- **MAE**: 37.87 points

### Trade #1243 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:15:00
- **FVG 5m**: 23644.37 - 23657.00
- **Entrée**: 23639.83 @ 2025-09-03 09:16:00
- **Stop Loss**: 23668.83
- **Risk**: 29.00 points
- **TP 1RR**: 23610.83 ❌
- **TP 1.5RR**: 23596.33 ❌
- **TP 2RR**: 23581.84 ❌
- **TP 2.5RR**: 23567.34 ❌
- **TP 3RR**: 23552.84 ❌
- **TP 3.5RR**: 23538.34 ❌
- **TP 4RR**: 23523.84 ❌
- **TP 4.5RR**: 23509.34 ❌
- **TP 5RR**: 23494.85 ❌
- **PnL**: -29.00 points (-1.0R)
- **MFE**: 3.03 points
- **MAE**: 37.87 points

### Trade #1244 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:15:00
- **FVG 5m**: 23644.37 - 23657.00
- **Entrée**: 23639.83 @ 2025-09-03 09:16:00
- **Stop Loss**: 23668.83
- **Risk**: 29.00 points
- **TP 1RR**: 23610.83 ❌
- **TP 1.5RR**: 23596.33 ❌
- **TP 2RR**: 23581.84 ❌
- **TP 2.5RR**: 23567.34 ❌
- **TP 3RR**: 23552.84 ❌
- **TP 3.5RR**: 23538.34 ❌
- **TP 4RR**: 23523.84 ❌
- **TP 4.5RR**: 23509.34 ❌
- **TP 5RR**: 23494.85 ❌
- **PnL**: -29.00 points (-1.0R)
- **MFE**: 3.03 points
- **MAE**: 37.87 points

### Trade #1245 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:45:00
- **FVG 5m**: 23709.26 - 23712.54
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23724.40
- **Risk**: 21.45 points
- **TP 1RR**: 23681.50 ✅
- **TP 1.5RR**: 23670.77 ✅
- **TP 2RR**: 23660.05 ✅
- **TP 2.5RR**: 23649.32 ✅
- **TP 3RR**: 23638.60 ✅
- **TP 3.5RR**: 23627.87 ✅
- **TP 4RR**: 23617.15 ✅
- **TP 4.5RR**: 23606.42 ✅
- **TP 5RR**: 23595.70 ✅
- **PnL**: 107.25 points (5.0R)
- **MFE**: 124.98 points
- **MAE**: 3.53 points

### Trade #1246 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 10:00:00
- **FVG 5m**: 23718.10 - 23728.95
- **Entrée**: 23713.30 @ 2025-09-03 10:16:00
- **Stop Loss**: 23740.82
- **Risk**: 27.52 points
- **TP 1RR**: 23685.78 ✅
- **TP 1.5RR**: 23672.02 ✅
- **TP 2RR**: 23658.26 ✅
- **TP 2.5RR**: 23644.51 ✅
- **TP 3RR**: 23630.75 ✅
- **TP 3.5RR**: 23616.99 ✅
- **TP 4RR**: 23603.23 ✅
- **TP 4.5RR**: 23589.47 ✅
- **TP 5RR**: 23575.71 ✅
- **PnL**: 137.59 points (5.0R)
- **MFE**: 143.91 points
- **MAE**: 7.83 points

### Trade #1247 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 10:00:00
- **FVG 5m**: 23718.10 - 23728.95
- **Entrée**: 23713.30 @ 2025-09-03 10:16:00
- **Stop Loss**: 23740.82
- **Risk**: 27.52 points
- **TP 1RR**: 23685.78 ✅
- **TP 1.5RR**: 23672.02 ✅
- **TP 2RR**: 23658.26 ✅
- **TP 2.5RR**: 23644.51 ✅
- **TP 3RR**: 23630.75 ✅
- **TP 3.5RR**: 23616.99 ✅
- **TP 4RR**: 23603.23 ✅
- **TP 4.5RR**: 23589.47 ✅
- **TP 5RR**: 23575.71 ✅
- **PnL**: 137.59 points (5.0R)
- **MFE**: 143.91 points
- **MAE**: 7.83 points

### Trade #1248 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-03 14:30:00
- **FVG 5m**: 23597.41 - 23607.77
- **Entrée**: 23612.56 @ 2025-09-03 14:37:00
- **Stop Loss**: 23585.61
- **Risk**: 26.95 points
- **TP 1RR**: 23639.51 ✅
- **TP 1.5RR**: 23652.98 ✅
- **TP 2RR**: 23666.46 ✅
- **TP 2.5RR**: 23679.93 ✅
- **TP 3RR**: 23693.40 ✅
- **TP 3.5RR**: 23706.88 ✅
- **TP 4RR**: 23720.35 ✅
- **TP 4.5RR**: 23733.82 ✅
- **TP 5RR**: 23747.30 ✅
- **PnL**: 134.74 points (5.0R)
- **MFE**: 135.33 points
- **MAE**: 4.54 points

### Trade #1249 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 21:15:00
- **FVG 5m**: 23731.98 - 23742.59
- **Entrée**: 23730.97 @ 2025-09-03 21:29:00
- **Stop Loss**: 23754.46
- **Risk**: 23.49 points
- **TP 1RR**: 23707.49 ✅
- **TP 1.5RR**: 23695.75 ✅
- **TP 2RR**: 23684.00 ✅
- **TP 2.5RR**: 23672.26 ❌
- **TP 3RR**: 23660.52 ❌
- **TP 3.5RR**: 23648.78 ❌
- **TP 4RR**: 23637.03 ❌
- **TP 4.5RR**: 23625.29 ❌
- **TP 5RR**: 23613.55 ❌
- **PnL**: -23.49 points (-1.0R)
- **MFE**: 47.72 points
- **MAE**: 26.76 points

### Trade #1250 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 21:45:00
- **FVG 5m**: 23731.98 - 23742.59
- **Entrée**: 23730.97 @ 2025-09-03 21:47:00
- **Stop Loss**: 23754.46
- **Risk**: 23.49 points
- **TP 1RR**: 23707.49 ✅
- **TP 1.5RR**: 23695.75 ✅
- **TP 2RR**: 23684.00 ✅
- **TP 2.5RR**: 23672.26 ❌
- **TP 3RR**: 23660.52 ❌
- **TP 3.5RR**: 23648.78 ❌
- **TP 4RR**: 23637.03 ❌
- **TP 4.5RR**: 23625.29 ❌
- **TP 5RR**: 23613.55 ❌
- **PnL**: -23.49 points (-1.0R)
- **MFE**: 47.72 points
- **MAE**: 26.76 points

### Trade #1251 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 22:15:00
- **FVG 5m**: 23731.98 - 23742.59
- **Entrée**: 23710.02 @ 2025-09-03 22:16:00
- **Stop Loss**: 23754.46
- **Risk**: 44.44 points
- **TP 1RR**: 23665.58 ❌
- **TP 1.5RR**: 23643.36 ❌
- **TP 2RR**: 23621.14 ❌
- **TP 2.5RR**: 23598.92 ❌
- **TP 3RR**: 23576.70 ❌
- **TP 3.5RR**: 23554.48 ❌
- **TP 4RR**: 23532.26 ❌
- **TP 4.5RR**: 23510.03 ❌
- **TP 5RR**: 23487.81 ❌
- **PnL**: -44.44 points (-1.0R)
- **MFE**: 26.76 points
- **MAE**: 47.72 points

### Trade #1252 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 05:15:00
- **FVG 5m**: 23741.83 - 23747.64
- **Entrée**: 23738.80 @ 2025-09-04 05:27:00
- **Stop Loss**: 23759.51
- **Risk**: 20.71 points
- **TP 1RR**: 23718.09 ✅
- **TP 1.5RR**: 23707.73 ✅
- **TP 2RR**: 23697.38 ✅
- **TP 2.5RR**: 23687.02 ❌
- **TP 3RR**: 23676.67 ❌
- **TP 3.5RR**: 23666.31 ❌
- **TP 4RR**: 23655.96 ❌
- **TP 4.5RR**: 23645.60 ❌
- **TP 5RR**: 23635.25 ❌
- **PnL**: -20.71 points (-1.0R)
- **MFE**: 49.23 points
- **MAE**: 32.32 points

### Trade #1253 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 06:15:00
- **FVG 5m**: 23741.83 - 23747.64
- **Entrée**: 23738.55 @ 2025-09-04 06:22:00
- **Stop Loss**: 23759.51
- **Risk**: 20.96 points
- **TP 1RR**: 23717.58 ✅
- **TP 1.5RR**: 23707.10 ✅
- **TP 2RR**: 23696.62 ✅
- **TP 2.5RR**: 23686.14 ❌
- **TP 3RR**: 23675.66 ❌
- **TP 3.5RR**: 23665.18 ❌
- **TP 4RR**: 23654.70 ❌
- **TP 4.5RR**: 23644.21 ❌
- **TP 5RR**: 23633.73 ❌
- **PnL**: -20.96 points (-1.0R)
- **MFE**: 48.98 points
- **MAE**: 32.57 points

### Trade #1254 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 08:30:00
- **FVG 5m**: 23731.48 - 23734.76
- **Entrée**: 23721.88 @ 2025-09-04 08:31:00
- **Stop Loss**: 23746.63
- **Risk**: 24.74 points
- **TP 1RR**: 23697.14 ❌
- **TP 1.5RR**: 23684.77 ❌
- **TP 2RR**: 23672.40 ❌
- **TP 2.5RR**: 23660.03 ❌
- **TP 3RR**: 23647.65 ❌
- **TP 3.5RR**: 23635.28 ❌
- **TP 4RR**: 23622.91 ❌
- **TP 4.5RR**: 23610.54 ❌
- **TP 5RR**: 23598.17 ❌
- **PnL**: -24.74 points (-1.0R)
- **MFE**: 8.58 points
- **MAE**: 34.08 points

### Trade #1255 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 08:30:00
- **FVG 5m**: 23731.48 - 23734.76
- **Entrée**: 23721.88 @ 2025-09-04 08:31:00
- **Stop Loss**: 23746.63
- **Risk**: 24.74 points
- **TP 1RR**: 23697.14 ❌
- **TP 1.5RR**: 23684.77 ❌
- **TP 2RR**: 23672.40 ❌
- **TP 2.5RR**: 23660.03 ❌
- **TP 3RR**: 23647.65 ❌
- **TP 3.5RR**: 23635.28 ❌
- **TP 4RR**: 23622.91 ❌
- **TP 4.5RR**: 23610.54 ❌
- **TP 5RR**: 23598.17 ❌
- **PnL**: -24.74 points (-1.0R)
- **MFE**: 8.58 points
- **MAE**: 34.08 points

### Trade #1256 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 08:30:00
- **FVG 5m**: 23731.48 - 23734.76
- **Entrée**: 23721.88 @ 2025-09-04 08:31:00
- **Stop Loss**: 23746.63
- **Risk**: 24.74 points
- **TP 1RR**: 23697.14 ❌
- **TP 1.5RR**: 23684.77 ❌
- **TP 2RR**: 23672.40 ❌
- **TP 2.5RR**: 23660.03 ❌
- **TP 3RR**: 23647.65 ❌
- **TP 3.5RR**: 23635.28 ❌
- **TP 4RR**: 23622.91 ❌
- **TP 4.5RR**: 23610.54 ❌
- **TP 5RR**: 23598.17 ❌
- **PnL**: -24.74 points (-1.0R)
- **MFE**: 8.58 points
- **MAE**: 34.08 points

### Trade #1257 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 09:15:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23701.18 @ 2025-09-04 09:23:00
- **Stop Loss**: 23674.69
- **Risk**: 26.49 points
- **TP 1RR**: 23727.67 ✅
- **TP 1.5RR**: 23740.91 ✅
- **TP 2RR**: 23754.16 ✅
- **TP 2.5RR**: 23767.40 ✅
- **TP 3RR**: 23780.64 ✅
- **TP 3.5RR**: 23793.89 ✅
- **TP 4RR**: 23807.13 ✅
- **TP 4.5RR**: 23820.37 ✅
- **TP 5RR**: 23833.62 ✅
- **PnL**: 132.43 points (5.0R)
- **MFE**: 140.88 points
- **MAE**: 6.31 points

### Trade #1258 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 09:15:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23701.18 @ 2025-09-04 09:23:00
- **Stop Loss**: 23674.69
- **Risk**: 26.49 points
- **TP 1RR**: 23727.67 ✅
- **TP 1.5RR**: 23740.91 ✅
- **TP 2RR**: 23754.16 ✅
- **TP 2.5RR**: 23767.40 ✅
- **TP 3RR**: 23780.64 ✅
- **TP 3.5RR**: 23793.89 ✅
- **TP 4RR**: 23807.13 ✅
- **TP 4.5RR**: 23820.37 ✅
- **TP 5RR**: 23833.62 ✅
- **PnL**: 132.43 points (5.0R)
- **MFE**: 140.88 points
- **MAE**: 6.31 points

### Trade #1259 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 09:15:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23701.18 @ 2025-09-04 09:23:00
- **Stop Loss**: 23674.69
- **Risk**: 26.49 points
- **TP 1RR**: 23727.67 ✅
- **TP 1.5RR**: 23740.91 ✅
- **TP 2RR**: 23754.16 ✅
- **TP 2.5RR**: 23767.40 ✅
- **TP 3RR**: 23780.64 ✅
- **TP 3.5RR**: 23793.89 ✅
- **TP 4RR**: 23807.13 ✅
- **TP 4.5RR**: 23820.37 ✅
- **TP 5RR**: 23833.62 ✅
- **PnL**: 132.43 points (5.0R)
- **MFE**: 140.88 points
- **MAE**: 6.31 points

### Trade #1260 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 10:15:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23756.98 @ 2025-09-04 10:16:00
- **Stop Loss**: 23674.69
- **Risk**: 82.28 points
- **TP 1RR**: 23839.26 ✅
- **TP 1.5RR**: 23880.40 ✅
- **TP 2RR**: 23921.55 ✅
- **TP 2.5RR**: 23962.69 ✅
- **TP 3RR**: 24003.83 ✅
- **TP 3.5RR**: 24044.97 ✅
- **TP 4RR**: 24086.11 ✅
- **TP 4.5RR**: 24127.26 ✅
- **TP 5RR**: 24168.40 ✅
- **PnL**: 411.42 points (5.0R)
- **MFE**: 413.05 points
- **MAE**: 19.19 points

### Trade #1261 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 11:45:00
- **FVG 5m**: 23774.15 - 23777.18
- **Entrée**: 23771.37 @ 2025-09-04 11:46:00
- **Stop Loss**: 23789.07
- **Risk**: 17.70 points
- **TP 1RR**: 23753.67 ❌
- **TP 1.5RR**: 23744.83 ❌
- **TP 2RR**: 23735.98 ❌
- **TP 2.5RR**: 23727.13 ❌
- **TP 3RR**: 23718.28 ❌
- **TP 3.5RR**: 23709.44 ❌
- **TP 4RR**: 23700.59 ❌
- **TP 4.5RR**: 23691.74 ❌
- **TP 5RR**: 23682.89 ❌
- **PnL**: -17.70 points (-1.0R)
- **MFE**: 2.78 points
- **MAE**: 26.01 points

### Trade #1262 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 11:45:00
- **FVG 5m**: 23774.15 - 23777.18
- **Entrée**: 23771.37 @ 2025-09-04 11:46:00
- **Stop Loss**: 23789.07
- **Risk**: 17.70 points
- **TP 1RR**: 23753.67 ❌
- **TP 1.5RR**: 23744.83 ❌
- **TP 2RR**: 23735.98 ❌
- **TP 2.5RR**: 23727.13 ❌
- **TP 3RR**: 23718.28 ❌
- **TP 3.5RR**: 23709.44 ❌
- **TP 4RR**: 23700.59 ❌
- **TP 4.5RR**: 23691.74 ❌
- **TP 5RR**: 23682.89 ❌
- **PnL**: -17.70 points (-1.0R)
- **MFE**: 2.78 points
- **MAE**: 26.01 points

### Trade #1263 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 12:15:00
- **FVG 5m**: 23767.08 - 23769.60
- **Entrée**: 23792.83 @ 2025-09-04 12:16:00
- **Stop Loss**: 23755.19
- **Risk**: 37.64 points
- **TP 1RR**: 23830.47 ✅
- **TP 1.5RR**: 23849.28 ✅
- **TP 2RR**: 23868.10 ✅
- **TP 2.5RR**: 23886.92 ✅
- **TP 3RR**: 23905.74 ✅
- **TP 3.5RR**: 23924.56 ✅
- **TP 4RR**: 23943.37 ✅
- **TP 4.5RR**: 23962.19 ✅
- **TP 5RR**: 23981.01 ✅
- **PnL**: 188.18 points (5.0R)
- **MFE**: 188.85 points
- **MAE**: 4.29 points

### Trade #1264 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 12:45:00
- **FVG 5m**: 23767.08 - 23769.60
- **Entrée**: 23809.49 @ 2025-09-04 12:46:00
- **Stop Loss**: 23755.19
- **Risk**: 54.30 points
- **TP 1RR**: 23863.79 ✅
- **TP 1.5RR**: 23890.94 ✅
- **TP 2RR**: 23918.09 ✅
- **TP 2.5RR**: 23945.24 ✅
- **TP 3RR**: 23972.39 ✅
- **TP 3.5RR**: 23999.54 ✅
- **TP 4RR**: 24026.69 ✅
- **TP 4.5RR**: 24053.84 ✅
- **TP 5RR**: 24080.99 ✅
- **PnL**: 271.50 points (5.0R)
- **MFE**: 273.68 points
- **MAE**: 1.26 points

### Trade #1265 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 08:15:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 24110.95 @ 2025-09-05 08:29:00
- **Stop Loss**: 24129.83
- **Risk**: 18.88 points
- **TP 1RR**: 24092.07 ❌
- **TP 1.5RR**: 24082.64 ❌
- **TP 2RR**: 24073.20 ❌
- **TP 2.5RR**: 24063.76 ❌
- **TP 3RR**: 24054.32 ❌
- **TP 3.5RR**: 24044.88 ❌
- **TP 4RR**: 24035.45 ❌
- **TP 4.5RR**: 24026.01 ❌
- **TP 5RR**: 24016.57 ❌
- **PnL**: -18.88 points (-1.0R)
- **MFE**: 22.22 points
- **MAE**: 27.77 points

### Trade #1266 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 24051.37 @ 2025-09-05 09:01:00
- **Stop Loss**: 24129.83
- **Risk**: 78.46 points
- **TP 1RR**: 23972.91 ✅
- **TP 1.5RR**: 23933.68 ✅
- **TP 2RR**: 23894.45 ✅
- **TP 2.5RR**: 23855.22 ✅
- **TP 3RR**: 23815.99 ✅
- **TP 3.5RR**: 23776.76 ✅
- **TP 4RR**: 23737.53 ❌
- **TP 4.5RR**: 23698.30 ❌
- **TP 5RR**: 23659.07 ❌
- **PnL**: -78.46 points (-1.0R)
- **MFE**: 313.58 points
- **MAE**: 80.03 points

### Trade #1267 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 24051.37 @ 2025-09-05 09:01:00
- **Stop Loss**: 24129.83
- **Risk**: 78.46 points
- **TP 1RR**: 23972.91 ✅
- **TP 1.5RR**: 23933.68 ✅
- **TP 2RR**: 23894.45 ✅
- **TP 2.5RR**: 23855.22 ✅
- **TP 3RR**: 23815.99 ✅
- **TP 3.5RR**: 23776.76 ✅
- **TP 4RR**: 23737.53 ❌
- **TP 4.5RR**: 23698.30 ❌
- **TP 5RR**: 23659.07 ❌
- **PnL**: -78.46 points (-1.0R)
- **MFE**: 313.58 points
- **MAE**: 80.03 points

### Trade #1268 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 24051.37 @ 2025-09-05 09:01:00
- **Stop Loss**: 24129.83
- **Risk**: 78.46 points
- **TP 1RR**: 23972.91 ✅
- **TP 1.5RR**: 23933.68 ✅
- **TP 2RR**: 23894.45 ✅
- **TP 2.5RR**: 23855.22 ✅
- **TP 3RR**: 23815.99 ✅
- **TP 3.5RR**: 23776.76 ✅
- **TP 4RR**: 23737.53 ❌
- **TP 4.5RR**: 23698.30 ❌
- **TP 5RR**: 23659.07 ❌
- **PnL**: -78.46 points (-1.0R)
- **MFE**: 313.58 points
- **MAE**: 80.03 points

### Trade #1269 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 24051.37 @ 2025-09-05 09:01:00
- **Stop Loss**: 24129.83
- **Risk**: 78.46 points
- **TP 1RR**: 23972.91 ✅
- **TP 1.5RR**: 23933.68 ✅
- **TP 2RR**: 23894.45 ✅
- **TP 2.5RR**: 23855.22 ✅
- **TP 3RR**: 23815.99 ✅
- **TP 3.5RR**: 23776.76 ✅
- **TP 4RR**: 23737.53 ❌
- **TP 4.5RR**: 23698.30 ❌
- **TP 5RR**: 23659.07 ❌
- **PnL**: -78.46 points (-1.0R)
- **MFE**: 313.58 points
- **MAE**: 80.03 points

### Trade #1270 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 24051.37 @ 2025-09-05 09:01:00
- **Stop Loss**: 24129.83
- **Risk**: 78.46 points
- **TP 1RR**: 23972.91 ✅
- **TP 1.5RR**: 23933.68 ✅
- **TP 2RR**: 23894.45 ✅
- **TP 2.5RR**: 23855.22 ✅
- **TP 3RR**: 23815.99 ✅
- **TP 3.5RR**: 23776.76 ✅
- **TP 4RR**: 23737.53 ❌
- **TP 4.5RR**: 23698.30 ❌
- **TP 5RR**: 23659.07 ❌
- **PnL**: -78.46 points (-1.0R)
- **MFE**: 313.58 points
- **MAE**: 80.03 points

### Trade #1271 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 24051.37 @ 2025-09-05 09:01:00
- **Stop Loss**: 24129.83
- **Risk**: 78.46 points
- **TP 1RR**: 23972.91 ✅
- **TP 1.5RR**: 23933.68 ✅
- **TP 2RR**: 23894.45 ✅
- **TP 2.5RR**: 23855.22 ✅
- **TP 3RR**: 23815.99 ✅
- **TP 3.5RR**: 23776.76 ✅
- **TP 4RR**: 23737.53 ❌
- **TP 4.5RR**: 23698.30 ❌
- **TP 5RR**: 23659.07 ❌
- **PnL**: -78.46 points (-1.0R)
- **MFE**: 313.58 points
- **MAE**: 80.03 points

### Trade #1272 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:15:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 23965.02 @ 2025-09-05 09:16:00
- **Stop Loss**: 24129.83
- **Risk**: 164.81 points
- **TP 1RR**: 23800.21 ✅
- **TP 1.5RR**: 23717.81 ❌
- **TP 2RR**: 23635.40 ❌
- **TP 2.5RR**: 23553.00 ❌
- **TP 3RR**: 23470.60 ❌
- **TP 3.5RR**: 23388.19 ❌
- **TP 4RR**: 23305.79 ❌
- **TP 4.5RR**: 23223.39 ❌
- **TP 5RR**: 23140.98 ❌
- **PnL**: -164.81 points (-1.0R)
- **MFE**: 227.23 points
- **MAE**: 166.38 points

### Trade #1273 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:15:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 23965.02 @ 2025-09-05 09:16:00
- **Stop Loss**: 24129.83
- **Risk**: 164.81 points
- **TP 1RR**: 23800.21 ✅
- **TP 1.5RR**: 23717.81 ❌
- **TP 2RR**: 23635.40 ❌
- **TP 2.5RR**: 23553.00 ❌
- **TP 3RR**: 23470.60 ❌
- **TP 3.5RR**: 23388.19 ❌
- **TP 4RR**: 23305.79 ❌
- **TP 4.5RR**: 23223.39 ❌
- **TP 5RR**: 23140.98 ❌
- **PnL**: -164.81 points (-1.0R)
- **MFE**: 227.23 points
- **MAE**: 166.38 points

### Trade #1274 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:15:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 23965.02 @ 2025-09-05 09:16:00
- **Stop Loss**: 24129.83
- **Risk**: 164.81 points
- **TP 1RR**: 23800.21 ✅
- **TP 1.5RR**: 23717.81 ❌
- **TP 2RR**: 23635.40 ❌
- **TP 2.5RR**: 23553.00 ❌
- **TP 3RR**: 23470.60 ❌
- **TP 3.5RR**: 23388.19 ❌
- **TP 4RR**: 23305.79 ❌
- **TP 4.5RR**: 23223.39 ❌
- **TP 5RR**: 23140.98 ❌
- **PnL**: -164.81 points (-1.0R)
- **MFE**: 227.23 points
- **MAE**: 166.38 points

### Trade #1275 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:15:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 23965.02 @ 2025-09-05 09:16:00
- **Stop Loss**: 24129.83
- **Risk**: 164.81 points
- **TP 1RR**: 23800.21 ✅
- **TP 1.5RR**: 23717.81 ❌
- **TP 2RR**: 23635.40 ❌
- **TP 2.5RR**: 23553.00 ❌
- **TP 3RR**: 23470.60 ❌
- **TP 3.5RR**: 23388.19 ❌
- **TP 4RR**: 23305.79 ❌
- **TP 4.5RR**: 23223.39 ❌
- **TP 5RR**: 23140.98 ❌
- **PnL**: -164.81 points (-1.0R)
- **MFE**: 227.23 points
- **MAE**: 166.38 points

### Trade #1276 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-07 17:30:00
- **FVG 5m**: 23898.87 - 23906.70
- **Entrée**: 23938.76 @ 2025-09-07 17:31:00
- **Stop Loss**: 23886.92
- **Risk**: 51.84 points
- **TP 1RR**: 23990.60 ✅
- **TP 1.5RR**: 24016.52 ✅
- **TP 2RR**: 24042.44 ✅
- **TP 2.5RR**: 24068.36 ✅
- **TP 3RR**: 24094.28 ✅
- **TP 3.5RR**: 24120.20 ✅
- **TP 4RR**: 24146.12 ✅
- **TP 4.5RR**: 24172.04 ✅
- **TP 5RR**: 24197.96 ✅
- **PnL**: 259.20 points (5.0R)
- **MFE**: 261.31 points
- **MAE**: 0.00 points

### Trade #1277 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-07 17:30:00
- **FVG 5m**: 23898.87 - 23906.70
- **Entrée**: 23938.76 @ 2025-09-07 17:31:00
- **Stop Loss**: 23886.92
- **Risk**: 51.84 points
- **TP 1RR**: 23990.60 ✅
- **TP 1.5RR**: 24016.52 ✅
- **TP 2RR**: 24042.44 ✅
- **TP 2.5RR**: 24068.36 ✅
- **TP 3RR**: 24094.28 ✅
- **TP 3.5RR**: 24120.20 ✅
- **TP 4RR**: 24146.12 ✅
- **TP 4.5RR**: 24172.04 ✅
- **TP 5RR**: 24197.96 ✅
- **PnL**: 259.20 points (5.0R)
- **MFE**: 261.31 points
- **MAE**: 0.00 points

### Trade #1278 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-07 21:00:00
- **FVG 5m**: 24002.64 - 24007.69
- **Entrée**: 23999.10 @ 2025-09-07 21:01:00
- **Stop Loss**: 24019.69
- **Risk**: 20.59 points
- **TP 1RR**: 23978.51 ✅
- **TP 1.5RR**: 23968.22 ✅
- **TP 2RR**: 23957.93 ❌
- **TP 2.5RR**: 23947.63 ❌
- **TP 3RR**: 23937.34 ❌
- **TP 3.5RR**: 23927.04 ❌
- **TP 4RR**: 23916.75 ❌
- **TP 4.5RR**: 23906.46 ❌
- **TP 5RR**: 23896.16 ❌
- **PnL**: -20.59 points (-1.0R)
- **MFE**: 39.64 points
- **MAE**: 22.47 points

### Trade #1279 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 12:00:00
- **FVG 5m**: 24091.51 - 24103.12
- **Entrée**: 24042.53 @ 2025-09-08 12:01:00
- **Stop Loss**: 24115.17
- **Risk**: 72.65 points
- **TP 1RR**: 23969.88 ❌
- **TP 1.5RR**: 23933.56 ❌
- **TP 2RR**: 23897.24 ❌
- **TP 2.5RR**: 23860.91 ❌
- **TP 3RR**: 23824.59 ❌
- **TP 3.5RR**: 23788.27 ❌
- **TP 4RR**: 23751.95 ❌
- **TP 4.5RR**: 23715.62 ❌
- **TP 5RR**: 23679.30 ❌
- **PnL**: -72.65 points (-1.0R)
- **MFE**: 47.21 points
- **MAE**: 74.23 points

### Trade #1280 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 12:00:00
- **FVG 5m**: 24091.51 - 24103.12
- **Entrée**: 24042.53 @ 2025-09-08 12:01:00
- **Stop Loss**: 24115.17
- **Risk**: 72.65 points
- **TP 1RR**: 23969.88 ❌
- **TP 1.5RR**: 23933.56 ❌
- **TP 2RR**: 23897.24 ❌
- **TP 2.5RR**: 23860.91 ❌
- **TP 3RR**: 23824.59 ❌
- **TP 3.5RR**: 23788.27 ❌
- **TP 4RR**: 23751.95 ❌
- **TP 4.5RR**: 23715.62 ❌
- **TP 5RR**: 23679.30 ❌
- **PnL**: -72.65 points (-1.0R)
- **MFE**: 47.21 points
- **MAE**: 74.23 points

### Trade #1281 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 14:00:00
- **FVG 5m**: 24040.26 - 24043.03
- **Entrée**: 24023.85 @ 2025-09-08 14:01:00
- **Stop Loss**: 24055.06
- **Risk**: 31.21 points
- **TP 1RR**: 23992.64 ❌
- **TP 1.5RR**: 23977.03 ❌
- **TP 2RR**: 23961.43 ❌
- **TP 2.5RR**: 23945.82 ❌
- **TP 3RR**: 23930.22 ❌
- **TP 3.5RR**: 23914.61 ❌
- **TP 4RR**: 23899.01 ❌
- **TP 4.5RR**: 23883.40 ❌
- **TP 5RR**: 23867.80 ❌
- **PnL**: -31.21 points (-1.0R)
- **MFE**: 28.53 points
- **MAE**: 33.33 points

### Trade #1282 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 06:30:00
- **FVG 5m**: 24061.97 - 24064.49
- **Entrée**: 24068.53 @ 2025-09-09 06:32:00
- **Stop Loss**: 24049.94
- **Risk**: 18.60 points
- **TP 1RR**: 24087.13 ✅
- **TP 1.5RR**: 24096.43 ❌
- **TP 2RR**: 24105.72 ❌
- **TP 2.5RR**: 24115.02 ❌
- **TP 3RR**: 24124.32 ❌
- **TP 3.5RR**: 24133.62 ❌
- **TP 4RR**: 24142.92 ❌
- **TP 4.5RR**: 24152.21 ❌
- **TP 5RR**: 24161.51 ❌
- **PnL**: -18.60 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 32.57 points

### Trade #1283 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 08:00:00
- **FVG 5m**: 24061.97 - 24064.49
- **Entrée**: 24070.05 @ 2025-09-09 08:01:00
- **Stop Loss**: 24049.94
- **Risk**: 20.11 points
- **TP 1RR**: 24090.16 ❌
- **TP 1.5RR**: 24100.21 ❌
- **TP 2RR**: 24110.27 ❌
- **TP 2.5RR**: 24120.32 ❌
- **TP 3RR**: 24130.38 ❌
- **TP 3.5RR**: 24140.43 ❌
- **TP 4RR**: 24150.49 ❌
- **TP 4.5RR**: 24160.54 ❌
- **TP 5RR**: 24170.60 ❌
- **PnL**: -20.11 points (-1.0R)
- **MFE**: 2.52 points
- **MAE**: 34.08 points

### Trade #1284 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-09 08:45:00
- **FVG 5m**: 24073.08 - 24081.41
- **Entrée**: 24070.55 @ 2025-09-09 08:46:00
- **Stop Loss**: 24093.45
- **Risk**: 22.90 points
- **TP 1RR**: 24047.66 ✅
- **TP 1.5RR**: 24036.21 ✅
- **TP 2RR**: 24024.76 ✅
- **TP 2.5RR**: 24013.31 ✅
- **TP 3RR**: 24001.86 ✅
- **TP 3.5RR**: 23990.41 ✅
- **TP 4RR**: 23978.96 ✅
- **TP 4.5RR**: 23967.52 ✅
- **TP 5RR**: 23956.07 ❌
- **PnL**: -22.90 points (-1.0R)
- **MFE**: 109.57 points
- **MAE**: 25.25 points

### Trade #1285 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:00:00
- **FVG 5m**: 24064.75 - 24073.84
- **Entrée**: 24079.39 @ 2025-09-09 09:10:00
- **Stop Loss**: 24052.71
- **Risk**: 26.68 points
- **TP 1RR**: 24106.07 ❌
- **TP 1.5RR**: 24119.40 ❌
- **TP 2RR**: 24132.74 ❌
- **TP 2.5RR**: 24146.08 ❌
- **TP 3RR**: 24159.42 ❌
- **TP 3.5RR**: 24172.76 ❌
- **TP 4RR**: 24186.09 ❌
- **TP 4.5RR**: 24199.43 ❌
- **TP 5RR**: 24212.77 ❌
- **PnL**: -26.68 points (-1.0R)
- **MFE**: 7.57 points
- **MAE**: 28.53 points

### Trade #1286 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-09 14:30:00
- **FVG 5m**: 24086.21 - 24090.50
- **Entrée**: 24084.94 @ 2025-09-09 14:37:00
- **Stop Loss**: 24102.54
- **Risk**: 17.60 points
- **TP 1RR**: 24067.35 ❌
- **TP 1.5RR**: 24058.55 ❌
- **TP 2RR**: 24049.75 ❌
- **TP 2.5RR**: 24040.95 ❌
- **TP 3RR**: 24032.15 ❌
- **TP 3.5RR**: 24023.35 ❌
- **TP 4RR**: 24014.55 ❌
- **TP 4.5RR**: 24005.75 ❌
- **TP 5RR**: 23996.95 ❌
- **PnL**: -17.60 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 19.69 points

### Trade #1287 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 03:15:00
- **FVG 5m**: 24165.74 - 24170.03
- **Entrée**: 24159.43 @ 2025-09-10 03:18:00
- **Stop Loss**: 24182.11
- **Risk**: 22.69 points
- **TP 1RR**: 24136.74 ✅
- **TP 1.5RR**: 24125.39 ✅
- **TP 2RR**: 24114.05 ❌
- **TP 2.5RR**: 24102.70 ❌
- **TP 3RR**: 24091.36 ❌
- **TP 3.5RR**: 24080.01 ❌
- **TP 4RR**: 24068.67 ❌
- **TP 4.5RR**: 24057.32 ❌
- **TP 5RR**: 24045.98 ❌
- **PnL**: -22.69 points (-1.0R)
- **MFE**: 40.65 points
- **MAE**: 23.73 points

### Trade #1288 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 07:30:00
- **FVG 5m**: 24184.93 - 24188.46
- **Entrée**: 24179.37 @ 2025-09-10 08:30:00
- **Stop Loss**: 24200.55
- **Risk**: 21.18 points
- **TP 1RR**: 24158.19 ❌
- **TP 1.5RR**: 24147.60 ❌
- **TP 2RR**: 24137.00 ❌
- **TP 2.5RR**: 24126.41 ❌
- **TP 3RR**: 24115.82 ❌
- **TP 3.5RR**: 24105.23 ❌
- **TP 4RR**: 24094.64 ❌
- **TP 4.5RR**: 24084.05 ❌
- **TP 5RR**: 24073.45 ❌
- **PnL**: -21.18 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 25.25 points

### Trade #1289 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 07:30:00
- **FVG 5m**: 24184.93 - 24188.46
- **Entrée**: 24179.37 @ 2025-09-10 08:30:00
- **Stop Loss**: 24200.55
- **Risk**: 21.18 points
- **TP 1RR**: 24158.19 ❌
- **TP 1.5RR**: 24147.60 ❌
- **TP 2RR**: 24137.00 ❌
- **TP 2.5RR**: 24126.41 ❌
- **TP 3RR**: 24115.82 ❌
- **TP 3.5RR**: 24105.23 ❌
- **TP 4RR**: 24094.64 ❌
- **TP 4.5RR**: 24084.05 ❌
- **TP 5RR**: 24073.45 ❌
- **PnL**: -21.18 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 25.25 points

### Trade #1290 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24227.59 - 24235.42
- **Entrée**: 24182.91 @ 2025-09-10 08:31:00
- **Stop Loss**: 24247.54
- **Risk**: 64.63 points
- **TP 1RR**: 24118.27 ✅
- **TP 1.5RR**: 24085.96 ✅
- **TP 2RR**: 24053.64 ✅
- **TP 2.5RR**: 24021.32 ✅
- **TP 3RR**: 23989.01 ❌
- **TP 3.5RR**: 23956.69 ❌
- **TP 4RR**: 23924.37 ❌
- **TP 4.5RR**: 23892.06 ❌
- **TP 5RR**: 23859.74 ❌
- **PnL**: -64.63 points (-1.0R)
- **MFE**: 162.34 points
- **MAE**: 67.92 points

### Trade #1291 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24227.59 - 24235.42
- **Entrée**: 24182.91 @ 2025-09-10 08:31:00
- **Stop Loss**: 24247.54
- **Risk**: 64.63 points
- **TP 1RR**: 24118.27 ✅
- **TP 1.5RR**: 24085.96 ✅
- **TP 2RR**: 24053.64 ✅
- **TP 2.5RR**: 24021.32 ✅
- **TP 3RR**: 23989.01 ❌
- **TP 3.5RR**: 23956.69 ❌
- **TP 4RR**: 23924.37 ❌
- **TP 4.5RR**: 23892.06 ❌
- **TP 5RR**: 23859.74 ❌
- **PnL**: -64.63 points (-1.0R)
- **MFE**: 162.34 points
- **MAE**: 67.92 points

### Trade #1292 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24227.59 - 24235.42
- **Entrée**: 24182.91 @ 2025-09-10 08:31:00
- **Stop Loss**: 24247.54
- **Risk**: 64.63 points
- **TP 1RR**: 24118.27 ✅
- **TP 1.5RR**: 24085.96 ✅
- **TP 2RR**: 24053.64 ✅
- **TP 2.5RR**: 24021.32 ✅
- **TP 3RR**: 23989.01 ❌
- **TP 3.5RR**: 23956.69 ❌
- **TP 4RR**: 23924.37 ❌
- **TP 4.5RR**: 23892.06 ❌
- **TP 5RR**: 23859.74 ❌
- **PnL**: -64.63 points (-1.0R)
- **MFE**: 162.34 points
- **MAE**: 67.92 points

### Trade #1293 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24227.59 - 24235.42
- **Entrée**: 24182.91 @ 2025-09-10 08:31:00
- **Stop Loss**: 24247.54
- **Risk**: 64.63 points
- **TP 1RR**: 24118.27 ✅
- **TP 1.5RR**: 24085.96 ✅
- **TP 2RR**: 24053.64 ✅
- **TP 2.5RR**: 24021.32 ✅
- **TP 3RR**: 23989.01 ❌
- **TP 3.5RR**: 23956.69 ❌
- **TP 4RR**: 23924.37 ❌
- **TP 4.5RR**: 23892.06 ❌
- **TP 5RR**: 23859.74 ❌
- **PnL**: -64.63 points (-1.0R)
- **MFE**: 162.34 points
- **MAE**: 67.92 points

### Trade #1294 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24227.59 - 24235.42
- **Entrée**: 24182.91 @ 2025-09-10 08:31:00
- **Stop Loss**: 24247.54
- **Risk**: 64.63 points
- **TP 1RR**: 24118.27 ✅
- **TP 1.5RR**: 24085.96 ✅
- **TP 2RR**: 24053.64 ✅
- **TP 2.5RR**: 24021.32 ✅
- **TP 3RR**: 23989.01 ❌
- **TP 3.5RR**: 23956.69 ❌
- **TP 4RR**: 23924.37 ❌
- **TP 4.5RR**: 23892.06 ❌
- **TP 5RR**: 23859.74 ❌
- **PnL**: -64.63 points (-1.0R)
- **MFE**: 162.34 points
- **MAE**: 67.92 points

### Trade #1295 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24173.06 - 24182.15
- **Entrée**: 24166.24 @ 2025-09-10 11:17:00
- **Stop Loss**: 24194.24
- **Risk**: 28.00 points
- **TP 1RR**: 24138.24 ✅
- **TP 1.5RR**: 24124.25 ✅
- **TP 2RR**: 24110.25 ✅
- **TP 2.5RR**: 24096.25 ✅
- **TP 3RR**: 24082.25 ✅
- **TP 3.5RR**: 24068.25 ✅
- **TP 4RR**: 24054.25 ✅
- **TP 4.5RR**: 24040.26 ✅
- **TP 5RR**: 24026.26 ✅
- **PnL**: 139.99 points (5.0R)
- **MFE**: 145.68 points
- **MAE**: 11.11 points

### Trade #1296 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24173.06 - 24182.15
- **Entrée**: 24166.24 @ 2025-09-10 11:17:00
- **Stop Loss**: 24194.24
- **Risk**: 28.00 points
- **TP 1RR**: 24138.24 ✅
- **TP 1.5RR**: 24124.25 ✅
- **TP 2RR**: 24110.25 ✅
- **TP 2.5RR**: 24096.25 ✅
- **TP 3RR**: 24082.25 ✅
- **TP 3.5RR**: 24068.25 ✅
- **TP 4RR**: 24054.25 ✅
- **TP 4.5RR**: 24040.26 ✅
- **TP 5RR**: 24026.26 ✅
- **PnL**: 139.99 points (5.0R)
- **MFE**: 145.68 points
- **MAE**: 11.11 points

### Trade #1297 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24173.06 - 24182.15
- **Entrée**: 24166.24 @ 2025-09-10 11:17:00
- **Stop Loss**: 24194.24
- **Risk**: 28.00 points
- **TP 1RR**: 24138.24 ✅
- **TP 1.5RR**: 24124.25 ✅
- **TP 2RR**: 24110.25 ✅
- **TP 2.5RR**: 24096.25 ✅
- **TP 3RR**: 24082.25 ✅
- **TP 3.5RR**: 24068.25 ✅
- **TP 4RR**: 24054.25 ✅
- **TP 4.5RR**: 24040.26 ✅
- **TP 5RR**: 24026.26 ✅
- **PnL**: 139.99 points (5.0R)
- **MFE**: 145.68 points
- **MAE**: 11.11 points

### Trade #1298 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24173.06 - 24182.15
- **Entrée**: 24166.24 @ 2025-09-10 11:17:00
- **Stop Loss**: 24194.24
- **Risk**: 28.00 points
- **TP 1RR**: 24138.24 ✅
- **TP 1.5RR**: 24124.25 ✅
- **TP 2RR**: 24110.25 ✅
- **TP 2.5RR**: 24096.25 ✅
- **TP 3RR**: 24082.25 ✅
- **TP 3.5RR**: 24068.25 ✅
- **TP 4RR**: 24054.25 ✅
- **TP 4.5RR**: 24040.26 ✅
- **TP 5RR**: 24026.26 ✅
- **PnL**: 139.99 points (5.0R)
- **MFE**: 145.68 points
- **MAE**: 11.11 points

### Trade #1299 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 11:45:00
- **FVG 5m**: 24159.93 - 24168.26
- **Entrée**: 24170.03 @ 2025-09-10 12:02:00
- **Stop Loss**: 24147.85
- **Risk**: 22.18 points
- **TP 1RR**: 24192.21 ❌
- **TP 1.5RR**: 24203.30 ❌
- **TP 2RR**: 24214.39 ❌
- **TP 2.5RR**: 24225.48 ❌
- **TP 3RR**: 24236.57 ❌
- **TP 3.5RR**: 24247.66 ❌
- **TP 4RR**: 24258.75 ❌
- **TP 4.5RR**: 24269.83 ❌
- **TP 5RR**: 24280.92 ❌
- **PnL**: -22.18 points (-1.0R)
- **MFE**: 1.26 points
- **MAE**: 22.72 points

### Trade #1300 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 12:15:00
- **FVG 5m**: 24151.85 - 24156.65
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24168.73
- **Risk**: 19.91 points
- **TP 1RR**: 24128.92 ✅
- **TP 1.5RR**: 24118.96 ✅
- **TP 2RR**: 24109.01 ✅
- **TP 2.5RR**: 24099.06 ✅
- **TP 3RR**: 24089.11 ✅
- **TP 3.5RR**: 24079.15 ✅
- **TP 4RR**: 24069.20 ✅
- **TP 4.5RR**: 24059.25 ✅
- **TP 5RR**: 24049.30 ✅
- **PnL**: 99.53 points (5.0R)
- **MFE**: 100.49 points
- **MAE**: 4.80 points

### Trade #1301 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 12:15:00
- **FVG 5m**: 24151.85 - 24156.65
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24168.73
- **Risk**: 19.91 points
- **TP 1RR**: 24128.92 ✅
- **TP 1.5RR**: 24118.96 ✅
- **TP 2RR**: 24109.01 ✅
- **TP 2.5RR**: 24099.06 ✅
- **TP 3RR**: 24089.11 ✅
- **TP 3.5RR**: 24079.15 ✅
- **TP 4RR**: 24069.20 ✅
- **TP 4.5RR**: 24059.25 ✅
- **TP 5RR**: 24049.30 ✅
- **PnL**: 99.53 points (5.0R)
- **MFE**: 100.49 points
- **MAE**: 4.80 points

### Trade #1302 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 12:15:00
- **FVG 5m**: 24151.85 - 24156.65
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24168.73
- **Risk**: 19.91 points
- **TP 1RR**: 24128.92 ✅
- **TP 1.5RR**: 24118.96 ✅
- **TP 2RR**: 24109.01 ✅
- **TP 2.5RR**: 24099.06 ✅
- **TP 3RR**: 24089.11 ✅
- **TP 3.5RR**: 24079.15 ✅
- **TP 4RR**: 24069.20 ✅
- **TP 4.5RR**: 24059.25 ✅
- **TP 5RR**: 24049.30 ✅
- **PnL**: 99.53 points (5.0R)
- **MFE**: 100.49 points
- **MAE**: 4.80 points

### Trade #1303 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 13:15:00
- **FVG 5m**: 24151.85 - 24156.65
- **Entrée**: 24112.72 @ 2025-09-10 13:16:00
- **Stop Loss**: 24168.73
- **Risk**: 56.01 points
- **TP 1RR**: 24056.71 ✅
- **TP 1.5RR**: 24028.70 ✅
- **TP 2RR**: 24000.70 ❌
- **TP 2.5RR**: 23972.69 ❌
- **TP 3RR**: 23944.69 ❌
- **TP 3.5RR**: 23916.69 ❌
- **TP 4RR**: 23888.68 ❌
- **TP 4.5RR**: 23860.68 ❌
- **TP 5RR**: 23832.67 ❌
- **PnL**: -56.01 points (-1.0R)
- **MFE**: 92.15 points
- **MAE**: 56.55 points

### Trade #1304 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 14:45:00
- **FVG 5m**: 24070.30 - 24074.59
- **Entrée**: 24090.50 @ 2025-09-10 14:46:00
- **Stop Loss**: 24058.27
- **Risk**: 32.23 points
- **TP 1RR**: 24122.73 ✅
- **TP 1.5RR**: 24138.85 ✅
- **TP 2RR**: 24154.97 ✅
- **TP 2.5RR**: 24171.08 ✅
- **TP 3RR**: 24187.20 ✅
- **TP 3.5RR**: 24203.32 ✅
- **TP 4RR**: 24219.43 ✅
- **TP 4.5RR**: 24235.55 ✅
- **TP 5RR**: 24251.67 ✅
- **PnL**: 161.17 points (5.0R)
- **MFE**: 163.86 points
- **MAE**: 16.41 points

### Trade #1305 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 19:00:00
- **FVG 5m**: 24123.32 - 24126.60
- **Entrée**: 24122.82 @ 2025-09-10 19:10:00
- **Stop Loss**: 24138.67
- **Risk**: 15.85 points
- **TP 1RR**: 24106.97 ❌
- **TP 1.5RR**: 24099.04 ❌
- **TP 2RR**: 24091.12 ❌
- **TP 2.5RR**: 24083.19 ❌
- **TP 3RR**: 24075.26 ❌
- **TP 3.5RR**: 24067.34 ❌
- **TP 4RR**: 24059.41 ❌
- **TP 4.5RR**: 24051.49 ❌
- **TP 5RR**: 24043.56 ❌
- **PnL**: -15.85 points (-1.0R)
- **MFE**: 14.90 points
- **MAE**: 18.43 points

### Trade #1306 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 19:30:00
- **FVG 5m**: 24120.29 - 24123.83
- **Entrée**: 24127.11 @ 2025-09-10 19:31:00
- **Stop Loss**: 24108.23
- **Risk**: 18.88 points
- **TP 1RR**: 24145.99 ✅
- **TP 1.5RR**: 24155.42 ✅
- **TP 2RR**: 24164.86 ❌
- **TP 2.5RR**: 24174.30 ❌
- **TP 3RR**: 24183.74 ❌
- **TP 3.5RR**: 24193.18 ❌
- **TP 4RR**: 24202.62 ❌
- **TP 4.5RR**: 24212.05 ❌
- **TP 5RR**: 24221.49 ❌
- **PnL**: -18.88 points (-1.0R)
- **MFE**: 28.78 points
- **MAE**: 19.69 points

### Trade #1307 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-11 09:45:00
- **FVG 5m**: 24237.19 - 24244.00
- **Entrée**: 24234.16 @ 2025-09-11 09:50:00
- **Stop Loss**: 24256.13
- **Risk**: 21.97 points
- **TP 1RR**: 24212.19 ❌
- **TP 1.5RR**: 24201.21 ❌
- **TP 2RR**: 24190.22 ❌
- **TP 2.5RR**: 24179.24 ❌
- **TP 3RR**: 24168.25 ❌
- **TP 3.5RR**: 24157.27 ❌
- **TP 4RR**: 24146.28 ❌
- **TP 4.5RR**: 24135.30 ❌
- **TP 5RR**: 24124.32 ❌
- **PnL**: -21.97 points (-1.0R)
- **MFE**: 21.71 points
- **MAE**: 22.22 points

### Trade #1308 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 08:30:00
- **FVG 5m**: 24253.09 - 24257.89
- **Entrée**: 24250.06 @ 2025-09-12 08:37:00
- **Stop Loss**: 24270.02
- **Risk**: 19.96 points
- **TP 1RR**: 24230.11 ❌
- **TP 1.5RR**: 24220.13 ❌
- **TP 2RR**: 24210.15 ❌
- **TP 2.5RR**: 24200.17 ❌
- **TP 3RR**: 24190.20 ❌
- **TP 3.5RR**: 24180.22 ❌
- **TP 4RR**: 24170.24 ❌
- **TP 4.5RR**: 24160.26 ❌
- **TP 5RR**: 24150.29 ❌
- **PnL**: -19.96 points (-1.0R)
- **MFE**: 10.86 points
- **MAE**: 21.71 points

### Trade #1309 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 08:30:00
- **FVG 5m**: 24253.09 - 24257.89
- **Entrée**: 24250.06 @ 2025-09-12 08:37:00
- **Stop Loss**: 24270.02
- **Risk**: 19.96 points
- **TP 1RR**: 24230.11 ❌
- **TP 1.5RR**: 24220.13 ❌
- **TP 2RR**: 24210.15 ❌
- **TP 2.5RR**: 24200.17 ❌
- **TP 3RR**: 24190.20 ❌
- **TP 3.5RR**: 24180.22 ❌
- **TP 4RR**: 24170.24 ❌
- **TP 4.5RR**: 24160.26 ❌
- **TP 5RR**: 24150.29 ❌
- **PnL**: -19.96 points (-1.0R)
- **MFE**: 10.86 points
- **MAE**: 21.71 points

### Trade #1310 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 08:30:00
- **FVG 5m**: 24253.09 - 24257.89
- **Entrée**: 24250.06 @ 2025-09-12 08:37:00
- **Stop Loss**: 24270.02
- **Risk**: 19.96 points
- **TP 1RR**: 24230.11 ❌
- **TP 1.5RR**: 24220.13 ❌
- **TP 2RR**: 24210.15 ❌
- **TP 2.5RR**: 24200.17 ❌
- **TP 3RR**: 24190.20 ❌
- **TP 3.5RR**: 24180.22 ❌
- **TP 4RR**: 24170.24 ❌
- **TP 4.5RR**: 24160.26 ❌
- **TP 5RR**: 24150.29 ❌
- **PnL**: -19.96 points (-1.0R)
- **MFE**: 10.86 points
- **MAE**: 21.71 points

### Trade #1311 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 08:30:00
- **FVG 5m**: 24253.09 - 24257.89
- **Entrée**: 24250.06 @ 2025-09-12 08:37:00
- **Stop Loss**: 24270.02
- **Risk**: 19.96 points
- **TP 1RR**: 24230.11 ❌
- **TP 1.5RR**: 24220.13 ❌
- **TP 2RR**: 24210.15 ❌
- **TP 2.5RR**: 24200.17 ❌
- **TP 3RR**: 24190.20 ❌
- **TP 3.5RR**: 24180.22 ❌
- **TP 4RR**: 24170.24 ❌
- **TP 4.5RR**: 24160.26 ❌
- **TP 5RR**: 24150.29 ❌
- **PnL**: -19.96 points (-1.0R)
- **MFE**: 10.86 points
- **MAE**: 21.71 points

### Trade #1312 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 14:45:00
- **FVG 5m**: 24380.34 - 24389.68
- **Entrée**: 24361.15 @ 2025-09-12 14:46:00
- **Stop Loss**: 24401.88
- **Risk**: 40.72 points
- **TP 1RR**: 24320.43 ✅
- **TP 1.5RR**: 24300.07 ❌
- **TP 2RR**: 24279.70 ❌
- **TP 2.5RR**: 24259.34 ❌
- **TP 3RR**: 24238.98 ❌
- **TP 3.5RR**: 24218.62 ❌
- **TP 4RR**: 24198.25 ❌
- **TP 4.5RR**: 24177.89 ❌
- **TP 5RR**: 24157.53 ❌
- **PnL**: -40.72 points (-1.0R)
- **MFE**: 43.40 points
- **MAE**: 47.60 points

### Trade #1313 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 03:00:00
- **FVG 5m**: 24369.50 - 24373.25
- **Entrée**: 24345.50 @ 2025-09-15 03:01:00
- **Stop Loss**: 24385.44
- **Risk**: 39.94 points
- **TP 1RR**: 24305.56 ❌
- **TP 1.5RR**: 24285.60 ❌
- **TP 2RR**: 24265.63 ❌
- **TP 2.5RR**: 24245.66 ❌
- **TP 3RR**: 24225.69 ❌
- **TP 3.5RR**: 24205.72 ❌
- **TP 4RR**: 24185.75 ❌
- **TP 4.5RR**: 24165.79 ❌
- **TP 5RR**: 24145.82 ❌
- **PnL**: -39.94 points (-1.0R)
- **MFE**: 27.75 points
- **MAE**: 40.25 points

### Trade #1314 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 03:45:00
- **FVG 5m**: 24489.75 - 24501.00
- **Entrée**: 24503.00 @ 2025-09-17 03:46:00
- **Stop Loss**: 24477.51
- **Risk**: 25.49 points
- **TP 1RR**: 24528.49 ✅
- **TP 1.5RR**: 24541.24 ❌
- **TP 2RR**: 24553.99 ❌
- **TP 2.5RR**: 24566.74 ❌
- **TP 3RR**: 24579.48 ❌
- **TP 3.5RR**: 24592.23 ❌
- **TP 4RR**: 24604.98 ❌
- **TP 4.5RR**: 24617.73 ❌
- **TP 5RR**: 24630.47 ❌
- **PnL**: -25.49 points (-1.0R)
- **MFE**: 37.75 points
- **MAE**: 30.75 points

### Trade #1315 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 03:45:00
- **FVG 5m**: 24489.75 - 24501.00
- **Entrée**: 24503.00 @ 2025-09-17 03:46:00
- **Stop Loss**: 24477.51
- **Risk**: 25.49 points
- **TP 1RR**: 24528.49 ✅
- **TP 1.5RR**: 24541.24 ❌
- **TP 2RR**: 24553.99 ❌
- **TP 2.5RR**: 24566.74 ❌
- **TP 3RR**: 24579.48 ❌
- **TP 3.5RR**: 24592.23 ❌
- **TP 4RR**: 24604.98 ❌
- **TP 4.5RR**: 24617.73 ❌
- **TP 5RR**: 24630.47 ❌
- **PnL**: -25.49 points (-1.0R)
- **MFE**: 37.75 points
- **MAE**: 30.75 points

### Trade #1316 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 06:00:00
- **FVG 5m**: 24489.75 - 24501.00
- **Entrée**: 24503.25 @ 2025-09-17 06:08:00
- **Stop Loss**: 24477.51
- **Risk**: 25.74 points
- **TP 1RR**: 24528.99 ✅
- **TP 1.5RR**: 24541.87 ❌
- **TP 2RR**: 24554.74 ❌
- **TP 2.5RR**: 24567.61 ❌
- **TP 3RR**: 24580.48 ❌
- **TP 3.5RR**: 24593.36 ❌
- **TP 4RR**: 24606.23 ❌
- **TP 4.5RR**: 24619.10 ❌
- **TP 5RR**: 24631.97 ❌
- **PnL**: -25.74 points (-1.0R)
- **MFE**: 37.50 points
- **MAE**: 31.00 points

### Trade #1317 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24403.00 - 24409.50
- **Entrée**: 24416.75 @ 2025-09-17 13:23:00
- **Stop Loss**: 24390.80
- **Risk**: 25.95 points
- **TP 1RR**: 24442.70 ❌
- **TP 1.5RR**: 24455.68 ❌
- **TP 2RR**: 24468.65 ❌
- **TP 2.5RR**: 24481.63 ❌
- **TP 3RR**: 24494.60 ❌
- **TP 3.5RR**: 24507.58 ❌
- **TP 4RR**: 24520.56 ❌
- **TP 4.5RR**: 24533.53 ❌
- **TP 5RR**: 24546.51 ❌
- **PnL**: -25.95 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 29.25 points

### Trade #1318 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24403.00 - 24409.50
- **Entrée**: 24416.75 @ 2025-09-17 13:23:00
- **Stop Loss**: 24390.80
- **Risk**: 25.95 points
- **TP 1RR**: 24442.70 ❌
- **TP 1.5RR**: 24455.68 ❌
- **TP 2RR**: 24468.65 ❌
- **TP 2.5RR**: 24481.63 ❌
- **TP 3RR**: 24494.60 ❌
- **TP 3.5RR**: 24507.58 ❌
- **TP 4RR**: 24520.56 ❌
- **TP 4.5RR**: 24533.53 ❌
- **TP 5RR**: 24546.51 ❌
- **PnL**: -25.95 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 29.25 points

### Trade #1319 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24403.00 - 24409.50
- **Entrée**: 24416.75 @ 2025-09-17 13:23:00
- **Stop Loss**: 24390.80
- **Risk**: 25.95 points
- **TP 1RR**: 24442.70 ❌
- **TP 1.5RR**: 24455.68 ❌
- **TP 2RR**: 24468.65 ❌
- **TP 2.5RR**: 24481.63 ❌
- **TP 3RR**: 24494.60 ❌
- **TP 3.5RR**: 24507.58 ❌
- **TP 4RR**: 24520.56 ❌
- **TP 4.5RR**: 24533.53 ❌
- **TP 5RR**: 24546.51 ❌
- **PnL**: -25.95 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 29.25 points

### Trade #1320 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24403.00 - 24409.50
- **Entrée**: 24416.75 @ 2025-09-17 13:23:00
- **Stop Loss**: 24390.80
- **Risk**: 25.95 points
- **TP 1RR**: 24442.70 ❌
- **TP 1.5RR**: 24455.68 ❌
- **TP 2RR**: 24468.65 ❌
- **TP 2.5RR**: 24481.63 ❌
- **TP 3RR**: 24494.60 ❌
- **TP 3.5RR**: 24507.58 ❌
- **TP 4RR**: 24520.56 ❌
- **TP 4.5RR**: 24533.53 ❌
- **TP 5RR**: 24546.51 ❌
- **PnL**: -25.95 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 29.25 points

### Trade #1321 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24388.75 - 24436.25
- **Entrée**: 24472.75 @ 2025-09-17 14:16:00
- **Stop Loss**: 24376.56
- **Risk**: 96.19 points
- **TP 1RR**: 24568.94 ✅
- **TP 1.5RR**: 24617.04 ✅
- **TP 2RR**: 24665.14 ✅
- **TP 2.5RR**: 24713.24 ✅
- **TP 3RR**: 24761.33 ✅
- **TP 3.5RR**: 24809.43 ✅
- **TP 4RR**: 24857.53 ✅
- **TP 4.5RR**: 24905.62 ✅
- **TP 5RR**: 24953.72 ✅
- **PnL**: 480.97 points (5.0R)
- **MFE**: 484.00 points
- **MAE**: 31.50 points

### Trade #1322 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24388.75 - 24436.25
- **Entrée**: 24472.75 @ 2025-09-17 14:16:00
- **Stop Loss**: 24376.56
- **Risk**: 96.19 points
- **TP 1RR**: 24568.94 ✅
- **TP 1.5RR**: 24617.04 ✅
- **TP 2RR**: 24665.14 ✅
- **TP 2.5RR**: 24713.24 ✅
- **TP 3RR**: 24761.33 ✅
- **TP 3.5RR**: 24809.43 ✅
- **TP 4RR**: 24857.53 ✅
- **TP 4.5RR**: 24905.62 ✅
- **TP 5RR**: 24953.72 ✅
- **PnL**: 480.97 points (5.0R)
- **MFE**: 484.00 points
- **MAE**: 31.50 points

### Trade #1323 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24388.75 - 24436.25
- **Entrée**: 24472.75 @ 2025-09-17 14:16:00
- **Stop Loss**: 24376.56
- **Risk**: 96.19 points
- **TP 1RR**: 24568.94 ✅
- **TP 1.5RR**: 24617.04 ✅
- **TP 2RR**: 24665.14 ✅
- **TP 2.5RR**: 24713.24 ✅
- **TP 3RR**: 24761.33 ✅
- **TP 3.5RR**: 24809.43 ✅
- **TP 4RR**: 24857.53 ✅
- **TP 4.5RR**: 24905.62 ✅
- **TP 5RR**: 24953.72 ✅
- **PnL**: 480.97 points (5.0R)
- **MFE**: 484.00 points
- **MAE**: 31.50 points

### Trade #1324 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24388.75 - 24436.25
- **Entrée**: 24472.75 @ 2025-09-17 14:16:00
- **Stop Loss**: 24376.56
- **Risk**: 96.19 points
- **TP 1RR**: 24568.94 ✅
- **TP 1.5RR**: 24617.04 ✅
- **TP 2RR**: 24665.14 ✅
- **TP 2.5RR**: 24713.24 ✅
- **TP 3RR**: 24761.33 ✅
- **TP 3.5RR**: 24809.43 ✅
- **TP 4RR**: 24857.53 ✅
- **TP 4.5RR**: 24905.62 ✅
- **TP 5RR**: 24953.72 ✅
- **PnL**: 480.97 points (5.0R)
- **MFE**: 484.00 points
- **MAE**: 31.50 points

### Trade #1325 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 20:00:00
- **FVG 5m**: 24566.50 - 24571.75
- **Entrée**: 24575.75 @ 2025-09-17 20:05:00
- **Stop Loss**: 24554.22
- **Risk**: 21.53 points
- **TP 1RR**: 24597.28 ✅
- **TP 1.5RR**: 24608.05 ✅
- **TP 2RR**: 24618.82 ✅
- **TP 2.5RR**: 24629.58 ✅
- **TP 3RR**: 24640.35 ✅
- **TP 3.5RR**: 24651.12 ✅
- **TP 4RR**: 24661.88 ✅
- **TP 4.5RR**: 24672.65 ✅
- **TP 5RR**: 24683.42 ✅
- **PnL**: 107.67 points (5.0R)
- **MFE**: 108.00 points
- **MAE**: 8.25 points

### Trade #1326 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 07:30:00
- **FVG 5m**: 24740.50 - 24750.00
- **Entrée**: 24733.75 @ 2025-09-18 07:33:00
- **Stop Loss**: 24762.38
- **Risk**: 28.62 points
- **TP 1RR**: 24705.12 ✅
- **TP 1.5RR**: 24690.81 ✅
- **TP 2RR**: 24676.50 ✅
- **TP 2.5RR**: 24662.19 ✅
- **TP 3RR**: 24647.88 ✅
- **TP 3.5RR**: 24633.56 ✅
- **TP 4RR**: 24619.25 ✅
- **TP 4.5RR**: 24604.94 ✅
- **TP 5RR**: 24590.62 ❌
- **PnL**: -28.62 points (-1.0R)
- **MFE**: 135.00 points
- **MAE**: 33.25 points

### Trade #1327 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 08:30:00
- **FVG 5m**: 24740.50 - 24750.00
- **Entrée**: 24686.50 @ 2025-09-18 08:31:00
- **Stop Loss**: 24762.38
- **Risk**: 75.88 points
- **TP 1RR**: 24610.62 ✅
- **TP 1.5RR**: 24572.69 ❌
- **TP 2RR**: 24534.75 ❌
- **TP 2.5RR**: 24496.81 ❌
- **TP 3RR**: 24458.88 ❌
- **TP 3.5RR**: 24420.94 ❌
- **TP 4RR**: 24383.00 ❌
- **TP 4.5RR**: 24345.06 ❌
- **TP 5RR**: 24307.12 ❌
- **PnL**: -75.88 points (-1.0R)
- **MFE**: 87.75 points
- **MAE**: 80.50 points

### Trade #1328 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 08:30:00
- **FVG 5m**: 24740.50 - 24750.00
- **Entrée**: 24686.50 @ 2025-09-18 08:31:00
- **Stop Loss**: 24762.38
- **Risk**: 75.88 points
- **TP 1RR**: 24610.62 ✅
- **TP 1.5RR**: 24572.69 ❌
- **TP 2RR**: 24534.75 ❌
- **TP 2.5RR**: 24496.81 ❌
- **TP 3RR**: 24458.88 ❌
- **TP 3.5RR**: 24420.94 ❌
- **TP 4RR**: 24383.00 ❌
- **TP 4.5RR**: 24345.06 ❌
- **TP 5RR**: 24307.12 ❌
- **PnL**: -75.88 points (-1.0R)
- **MFE**: 87.75 points
- **MAE**: 80.50 points

### Trade #1329 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 08:45:00
- **FVG 5m**: 24680.00 - 24689.50
- **Entrée**: 24690.25 @ 2025-09-18 08:50:00
- **Stop Loss**: 24667.66
- **Risk**: 22.59 points
- **TP 1RR**: 24712.84 ❌
- **TP 1.5RR**: 24724.14 ❌
- **TP 2RR**: 24735.43 ❌
- **TP 2.5RR**: 24746.72 ❌
- **TP 3RR**: 24758.02 ❌
- **TP 3.5RR**: 24769.32 ❌
- **TP 4RR**: 24780.61 ❌
- **TP 4.5RR**: 24791.90 ❌
- **TP 5RR**: 24803.20 ❌
- **PnL**: -22.59 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 37.00 points

### Trade #1330 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 08:45:00
- **FVG 5m**: 24680.00 - 24689.50
- **Entrée**: 24690.25 @ 2025-09-18 08:50:00
- **Stop Loss**: 24667.66
- **Risk**: 22.59 points
- **TP 1RR**: 24712.84 ❌
- **TP 1.5RR**: 24724.14 ❌
- **TP 2RR**: 24735.43 ❌
- **TP 2.5RR**: 24746.72 ❌
- **TP 3RR**: 24758.02 ❌
- **TP 3.5RR**: 24769.32 ❌
- **TP 4RR**: 24780.61 ❌
- **TP 4.5RR**: 24791.90 ❌
- **TP 5RR**: 24803.20 ❌
- **PnL**: -22.59 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 37.00 points

### Trade #1331 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-19 02:15:00
- **FVG 5m**: 24690.75 - 24701.25
- **Entrée**: 24701.50 @ 2025-09-19 03:12:00
- **Stop Loss**: 24678.40
- **Risk**: 23.10 points
- **TP 1RR**: 24724.60 ✅
- **TP 1.5RR**: 24736.14 ✅
- **TP 2RR**: 24747.69 ✅
- **TP 2.5RR**: 24759.24 ✅
- **TP 3RR**: 24770.79 ✅
- **TP 3.5RR**: 24782.33 ✅
- **TP 4RR**: 24793.88 ✅
- **TP 4.5RR**: 24805.43 ✅
- **TP 5RR**: 24816.98 ✅
- **PnL**: 115.48 points (5.0R)
- **MFE**: 116.00 points
- **MAE**: 4.50 points

### Trade #1332 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-19 02:15:00
- **FVG 5m**: 24690.75 - 24701.25
- **Entrée**: 24701.50 @ 2025-09-19 03:12:00
- **Stop Loss**: 24678.40
- **Risk**: 23.10 points
- **TP 1RR**: 24724.60 ✅
- **TP 1.5RR**: 24736.14 ✅
- **TP 2RR**: 24747.69 ✅
- **TP 2.5RR**: 24759.24 ✅
- **TP 3RR**: 24770.79 ✅
- **TP 3.5RR**: 24782.33 ✅
- **TP 4RR**: 24793.88 ✅
- **TP 4.5RR**: 24805.43 ✅
- **TP 5RR**: 24816.98 ✅
- **PnL**: 115.48 points (5.0R)
- **MFE**: 116.00 points
- **MAE**: 4.50 points

### Trade #1333 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 08:15:00
- **FVG 5m**: 24745.75 - 24748.75
- **Entrée**: 24745.25 @ 2025-09-19 08:37:00
- **Stop Loss**: 24761.12
- **Risk**: 15.87 points
- **TP 1RR**: 24729.38 ❌
- **TP 1.5RR**: 24721.44 ❌
- **TP 2RR**: 24713.50 ❌
- **TP 2.5RR**: 24705.56 ❌
- **TP 3RR**: 24697.63 ❌
- **TP 3.5RR**: 24689.69 ❌
- **TP 4RR**: 24681.75 ❌
- **TP 4.5RR**: 24673.82 ❌
- **TP 5RR**: 24665.88 ❌
- **PnL**: -15.87 points (-1.0R)
- **MFE**: 7.75 points
- **MAE**: 21.50 points

### Trade #1334 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 08:45:00
- **FVG 5m**: 24752.25 - 24755.75
- **Entrée**: 24750.50 @ 2025-09-19 09:45:00
- **Stop Loss**: 24768.13
- **Risk**: 17.63 points
- **TP 1RR**: 24732.87 ❌
- **TP 1.5RR**: 24724.06 ❌
- **TP 2RR**: 24715.24 ❌
- **TP 2.5RR**: 24706.43 ❌
- **TP 3RR**: 24697.62 ❌
- **TP 3.5RR**: 24688.80 ❌
- **TP 4RR**: 24679.99 ❌
- **TP 4.5RR**: 24671.17 ❌
- **TP 5RR**: 24662.36 ❌
- **PnL**: -17.63 points (-1.0R)
- **MFE**: 16.50 points
- **MAE**: 27.75 points

### Trade #1335 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 10:00:00
- **FVG 5m**: 24782.00 - 24787.00
- **Entrée**: 24764.25 @ 2025-09-19 10:01:00
- **Stop Loss**: 24799.39
- **Risk**: 35.14 points
- **TP 1RR**: 24729.11 ✅
- **TP 1.5RR**: 24711.53 ✅
- **TP 2RR**: 24693.96 ❌
- **TP 2.5RR**: 24676.39 ❌
- **TP 3RR**: 24658.82 ❌
- **TP 3.5RR**: 24641.25 ❌
- **TP 4RR**: 24623.68 ❌
- **TP 4.5RR**: 24606.10 ❌
- **TP 5RR**: 24588.53 ❌
- **PnL**: -35.14 points (-1.0R)
- **MFE**: 56.25 points
- **MAE**: 35.25 points

### Trade #1336 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 10:00:00
- **FVG 5m**: 24782.00 - 24787.00
- **Entrée**: 24764.25 @ 2025-09-19 10:01:00
- **Stop Loss**: 24799.39
- **Risk**: 35.14 points
- **TP 1RR**: 24729.11 ✅
- **TP 1.5RR**: 24711.53 ✅
- **TP 2RR**: 24693.96 ❌
- **TP 2.5RR**: 24676.39 ❌
- **TP 3RR**: 24658.82 ❌
- **TP 3.5RR**: 24641.25 ❌
- **TP 4RR**: 24623.68 ❌
- **TP 4.5RR**: 24606.10 ❌
- **TP 5RR**: 24588.53 ❌
- **PnL**: -35.14 points (-1.0R)
- **MFE**: 56.25 points
- **MAE**: 35.25 points

### Trade #1337 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-19 10:30:00
- **FVG 5m**: 24760.75 - 24766.25
- **Entrée**: 24767.50 @ 2025-09-19 10:56:00
- **Stop Loss**: 24748.37
- **Risk**: 19.13 points
- **TP 1RR**: 24786.63 ✅
- **TP 1.5RR**: 24796.20 ✅
- **TP 2RR**: 24805.76 ✅
- **TP 2.5RR**: 24815.33 ✅
- **TP 3RR**: 24824.89 ✅
- **TP 3.5RR**: 24834.46 ✅
- **TP 4RR**: 24844.02 ✅
- **TP 4.5RR**: 24853.59 ✅
- **TP 5RR**: 24863.15 ✅
- **PnL**: 95.65 points (5.0R)
- **MFE**: 102.50 points
- **MAE**: 0.75 points

### Trade #1338 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-21 17:00:00
- **FVG 5m**: 24847.75 - 24856.50
- **Entrée**: 24843.50 @ 2025-09-21 17:05:00
- **Stop Loss**: 24868.93
- **Risk**: 25.43 points
- **TP 1RR**: 24818.07 ❌
- **TP 1.5RR**: 24805.36 ❌
- **TP 2RR**: 24792.64 ❌
- **TP 2.5RR**: 24779.93 ❌
- **TP 3RR**: 24767.22 ❌
- **TP 3.5RR**: 24754.50 ❌
- **TP 4RR**: 24741.79 ❌
- **TP 4.5RR**: 24729.07 ❌
- **TP 5RR**: 24716.36 ❌
- **PnL**: -25.43 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 27.00 points

### Trade #1339 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-23 12:15:00
- **FVG 5m**: 24930.75 - 24941.75
- **Entrée**: 24907.50 @ 2025-09-23 12:16:00
- **Stop Loss**: 24954.22
- **Risk**: 46.72 points
- **TP 1RR**: 24860.78 ✅
- **TP 1.5RR**: 24837.42 ✅
- **TP 2RR**: 24814.06 ✅
- **TP 2.5RR**: 24790.70 ✅
- **TP 3RR**: 24767.34 ✅
- **TP 3.5RR**: 24743.98 ✅
- **TP 4RR**: 24720.62 ✅
- **TP 4.5RR**: 24697.26 ✅
- **TP 5RR**: 24673.90 ✅
- **PnL**: 233.60 points (5.0R)
- **MFE**: 234.50 points
- **MAE**: 6.25 points

### Trade #1340 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-23 12:15:00
- **FVG 5m**: 24930.75 - 24941.75
- **Entrée**: 24907.50 @ 2025-09-23 12:16:00
- **Stop Loss**: 24954.22
- **Risk**: 46.72 points
- **TP 1RR**: 24860.78 ✅
- **TP 1.5RR**: 24837.42 ✅
- **TP 2RR**: 24814.06 ✅
- **TP 2.5RR**: 24790.70 ✅
- **TP 3RR**: 24767.34 ✅
- **TP 3.5RR**: 24743.98 ✅
- **TP 4RR**: 24720.62 ✅
- **TP 4.5RR**: 24697.26 ✅
- **TP 5RR**: 24673.90 ✅
- **PnL**: 233.60 points (5.0R)
- **MFE**: 234.50 points
- **MAE**: 6.25 points

### Trade #1341 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-23 12:30:00
- **FVG 5m**: 24930.75 - 24941.75
- **Entrée**: 24861.50 @ 2025-09-23 12:31:00
- **Stop Loss**: 24954.22
- **Risk**: 92.72 points
- **TP 1RR**: 24768.78 ✅
- **TP 1.5RR**: 24722.42 ✅
- **TP 2RR**: 24676.06 ✅
- **TP 2.5RR**: 24629.70 ✅
- **TP 3RR**: 24583.34 ✅
- **TP 3.5RR**: 24536.98 ✅
- **TP 4RR**: 24490.62 ✅
- **TP 4.5RR**: 24444.26 ✅
- **TP 5RR**: 24397.90 ❌
- **PnL**: -92.72 points (-1.0R)
- **MFE**: 439.00 points
- **MAE**: 94.00 points

### Trade #1342 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-23 12:30:00
- **FVG 5m**: 24930.75 - 24941.75
- **Entrée**: 24861.50 @ 2025-09-23 12:31:00
- **Stop Loss**: 24954.22
- **Risk**: 92.72 points
- **TP 1RR**: 24768.78 ✅
- **TP 1.5RR**: 24722.42 ✅
- **TP 2RR**: 24676.06 ✅
- **TP 2.5RR**: 24629.70 ✅
- **TP 3RR**: 24583.34 ✅
- **TP 3.5RR**: 24536.98 ✅
- **TP 4RR**: 24490.62 ✅
- **TP 4.5RR**: 24444.26 ✅
- **TP 5RR**: 24397.90 ❌
- **PnL**: -92.72 points (-1.0R)
- **MFE**: 439.00 points
- **MAE**: 94.00 points

### Trade #1343 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-24 02:00:00
- **FVG 5m**: 24878.00 - 24883.50
- **Entrée**: 24877.00 @ 2025-09-24 02:03:00
- **Stop Loss**: 24895.94
- **Risk**: 18.94 points
- **TP 1RR**: 24858.06 ✅
- **TP 1.5RR**: 24848.59 ✅
- **TP 2RR**: 24839.12 ❌
- **TP 2.5RR**: 24829.65 ❌
- **TP 3RR**: 24820.17 ❌
- **TP 3.5RR**: 24810.70 ❌
- **TP 4RR**: 24801.23 ❌
- **TP 4.5RR**: 24791.76 ❌
- **TP 5RR**: 24782.29 ❌
- **PnL**: -18.94 points (-1.0R)
- **MFE**: 30.50 points
- **MAE**: 21.00 points

### Trade #1344 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 11:15:00
- **FVG 5m**: 24655.50 - 24667.75
- **Entrée**: 24668.00 @ 2025-09-24 11:20:00
- **Stop Loss**: 24643.17
- **Risk**: 24.83 points
- **TP 1RR**: 24692.83 ✅
- **TP 1.5RR**: 24705.24 ✅
- **TP 2RR**: 24717.66 ✅
- **TP 2.5RR**: 24730.07 ✅
- **TP 3RR**: 24742.48 ✅
- **TP 3.5RR**: 24754.90 ✅
- **TP 4RR**: 24767.31 ✅
- **TP 4.5RR**: 24779.72 ✅
- **TP 5RR**: 24792.14 ✅
- **PnL**: 124.14 points (5.0R)
- **MFE**: 125.50 points
- **MAE**: 1.25 points

### Trade #1345 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 12:00:00
- **FVG 5m**: 24655.50 - 24667.75
- **Entrée**: 24696.75 @ 2025-09-24 12:01:00
- **Stop Loss**: 24643.17
- **Risk**: 53.58 points
- **TP 1RR**: 24750.33 ✅
- **TP 1.5RR**: 24777.12 ✅
- **TP 2RR**: 24803.91 ❌
- **TP 2.5RR**: 24830.69 ❌
- **TP 3RR**: 24857.48 ❌
- **TP 3.5RR**: 24884.27 ❌
- **TP 4RR**: 24911.06 ❌
- **TP 4.5RR**: 24937.85 ❌
- **TP 5RR**: 24964.64 ❌
- **PnL**: -53.58 points (-1.0R)
- **MFE**: 96.75 points
- **MAE**: 57.25 points

### Trade #1346 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 12:00:00
- **FVG 5m**: 24655.50 - 24667.75
- **Entrée**: 24696.75 @ 2025-09-24 12:01:00
- **Stop Loss**: 24643.17
- **Risk**: 53.58 points
- **TP 1RR**: 24750.33 ✅
- **TP 1.5RR**: 24777.12 ✅
- **TP 2RR**: 24803.91 ❌
- **TP 2.5RR**: 24830.69 ❌
- **TP 3RR**: 24857.48 ❌
- **TP 3.5RR**: 24884.27 ❌
- **TP 4RR**: 24911.06 ❌
- **TP 4.5RR**: 24937.85 ❌
- **TP 5RR**: 24964.64 ❌
- **PnL**: -53.58 points (-1.0R)
- **MFE**: 96.75 points
- **MAE**: 57.25 points

### Trade #1347 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 02:30:00
- **FVG 5m**: 24722.75 - 24726.75
- **Entrée**: 24733.25 @ 2025-09-25 02:31:00
- **Stop Loss**: 24710.39
- **Risk**: 22.86 points
- **TP 1RR**: 24756.11 ✅
- **TP 1.5RR**: 24767.54 ❌
- **TP 2RR**: 24778.97 ❌
- **TP 2.5RR**: 24790.40 ❌
- **TP 3RR**: 24801.83 ❌
- **TP 3.5RR**: 24813.26 ❌
- **TP 4RR**: 24824.70 ❌
- **TP 4.5RR**: 24836.13 ❌
- **TP 5RR**: 24847.56 ❌
- **PnL**: -22.86 points (-1.0R)
- **MFE**: 30.75 points
- **MAE**: 26.00 points

### Trade #1348 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 03:00:00
- **FVG 5m**: 24722.75 - 24726.75
- **Entrée**: 24746.75 @ 2025-09-25 03:01:00
- **Stop Loss**: 24710.39
- **Risk**: 36.36 points
- **TP 1RR**: 24783.11 ❌
- **TP 1.5RR**: 24801.29 ❌
- **TP 2RR**: 24819.47 ❌
- **TP 2.5RR**: 24837.65 ❌
- **TP 3RR**: 24855.83 ❌
- **TP 3.5RR**: 24874.01 ❌
- **TP 4RR**: 24892.20 ❌
- **TP 4.5RR**: 24910.38 ❌
- **TP 5RR**: 24928.56 ❌
- **PnL**: -36.36 points (-1.0R)
- **MFE**: 17.25 points
- **MAE**: 39.50 points

### Trade #1349 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-25 08:30:00
- **FVG 5m**: 24560.00 - 24576.25
- **Entrée**: 24540.25 @ 2025-09-25 08:31:00
- **Stop Loss**: 24588.54
- **Risk**: 48.29 points
- **TP 1RR**: 24491.96 ✅
- **TP 1.5RR**: 24467.82 ✅
- **TP 2RR**: 24443.67 ✅
- **TP 2.5RR**: 24419.53 ❌
- **TP 3RR**: 24395.39 ❌
- **TP 3.5RR**: 24371.24 ❌
- **TP 4RR**: 24347.10 ❌
- **TP 4.5RR**: 24322.95 ❌
- **TP 5RR**: 24298.81 ❌
- **PnL**: -48.29 points (-1.0R)
- **MFE**: 117.75 points
- **MAE**: 65.50 points

### Trade #1350 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-25 08:30:00
- **FVG 5m**: 24560.00 - 24576.25
- **Entrée**: 24540.25 @ 2025-09-25 08:31:00
- **Stop Loss**: 24588.54
- **Risk**: 48.29 points
- **TP 1RR**: 24491.96 ✅
- **TP 1.5RR**: 24467.82 ✅
- **TP 2RR**: 24443.67 ✅
- **TP 2.5RR**: 24419.53 ❌
- **TP 3RR**: 24395.39 ❌
- **TP 3.5RR**: 24371.24 ❌
- **TP 4RR**: 24347.10 ❌
- **TP 4.5RR**: 24322.95 ❌
- **TP 5RR**: 24298.81 ❌
- **PnL**: -48.29 points (-1.0R)
- **MFE**: 117.75 points
- **MAE**: 65.50 points

### Trade #1351 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-25 08:30:00
- **FVG 5m**: 24560.00 - 24576.25
- **Entrée**: 24540.25 @ 2025-09-25 08:31:00
- **Stop Loss**: 24588.54
- **Risk**: 48.29 points
- **TP 1RR**: 24491.96 ✅
- **TP 1.5RR**: 24467.82 ✅
- **TP 2RR**: 24443.67 ✅
- **TP 2.5RR**: 24419.53 ❌
- **TP 3RR**: 24395.39 ❌
- **TP 3.5RR**: 24371.24 ❌
- **TP 4RR**: 24347.10 ❌
- **TP 4.5RR**: 24322.95 ❌
- **TP 5RR**: 24298.81 ❌
- **PnL**: -48.29 points (-1.0R)
- **MFE**: 117.75 points
- **MAE**: 65.50 points

### Trade #1352 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-25 08:30:00
- **FVG 5m**: 24560.00 - 24576.25
- **Entrée**: 24540.25 @ 2025-09-25 08:31:00
- **Stop Loss**: 24588.54
- **Risk**: 48.29 points
- **TP 1RR**: 24491.96 ✅
- **TP 1.5RR**: 24467.82 ✅
- **TP 2RR**: 24443.67 ✅
- **TP 2.5RR**: 24419.53 ❌
- **TP 3RR**: 24395.39 ❌
- **TP 3.5RR**: 24371.24 ❌
- **TP 4RR**: 24347.10 ❌
- **TP 4.5RR**: 24322.95 ❌
- **TP 5RR**: 24298.81 ❌
- **PnL**: -48.29 points (-1.0R)
- **MFE**: 117.75 points
- **MAE**: 65.50 points

### Trade #1353 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 09:00:00
- **FVG 5m**: 24477.00 - 24517.00
- **Entrée**: 24518.00 @ 2025-09-25 09:04:00
- **Stop Loss**: 24464.76
- **Risk**: 53.24 points
- **TP 1RR**: 24571.24 ✅
- **TP 1.5RR**: 24597.86 ✅
- **TP 2RR**: 24624.48 ✅
- **TP 2.5RR**: 24651.10 ✅
- **TP 3RR**: 24677.72 ✅
- **TP 3.5RR**: 24704.33 ❌
- **TP 4RR**: 24730.95 ❌
- **TP 4.5RR**: 24757.57 ❌
- **TP 5RR**: 24784.19 ❌
- **PnL**: -53.24 points (-1.0R)
- **MFE**: 178.75 points
- **MAE**: 63.25 points

### Trade #1354 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 09:15:00
- **FVG 5m**: 24477.00 - 24517.00
- **Entrée**: 24603.50 @ 2025-09-25 09:16:00
- **Stop Loss**: 24464.76
- **Risk**: 138.74 points
- **TP 1RR**: 24742.24 ❌
- **TP 1.5RR**: 24811.61 ❌
- **TP 2RR**: 24880.98 ❌
- **TP 2.5RR**: 24950.35 ❌
- **TP 3RR**: 25019.72 ❌
- **TP 3.5RR**: 25089.08 ❌
- **TP 4RR**: 25158.45 ❌
- **TP 4.5RR**: 25227.82 ❌
- **TP 5RR**: 25297.19 ❌
- **PnL**: -138.74 points (-1.0R)
- **MFE**: 93.25 points
- **MAE**: 148.75 points

### Trade #1355 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 09:30:00
- **FVG 5m**: 24477.00 - 24517.00
- **Entrée**: 24612.00 @ 2025-09-25 09:31:00
- **Stop Loss**: 24464.76
- **Risk**: 147.24 points
- **TP 1RR**: 24759.24 ❌
- **TP 1.5RR**: 24832.86 ❌
- **TP 2RR**: 24906.48 ❌
- **TP 2.5RR**: 24980.10 ❌
- **TP 3RR**: 25053.72 ❌
- **TP 3.5RR**: 25127.33 ❌
- **TP 4RR**: 25200.95 ❌
- **TP 4.5RR**: 25274.57 ❌
- **TP 5RR**: 25348.19 ❌
- **PnL**: -147.24 points (-1.0R)
- **MFE**: 84.75 points
- **MAE**: 157.25 points

### Trade #1356 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 03:30:00
- **FVG 5m**: 24646.75 - 24657.00
- **Entrée**: 24635.25 @ 2025-09-26 03:31:00
- **Stop Loss**: 24669.33
- **Risk**: 34.08 points
- **TP 1RR**: 24601.17 ✅
- **TP 1.5RR**: 24584.13 ✅
- **TP 2RR**: 24567.09 ❌
- **TP 2.5RR**: 24550.05 ❌
- **TP 3RR**: 24533.01 ❌
- **TP 3.5RR**: 24515.98 ❌
- **TP 4RR**: 24498.94 ❌
- **TP 4.5RR**: 24481.90 ❌
- **TP 5RR**: 24464.86 ❌
- **PnL**: -34.08 points (-1.0R)
- **MFE**: 66.00 points
- **MAE**: 44.50 points

### Trade #1357 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 05:00:00
- **FVG 5m**: 24604.00 - 24611.50
- **Entrée**: 24601.75 @ 2025-09-26 05:05:00
- **Stop Loss**: 24623.81
- **Risk**: 22.06 points
- **TP 1RR**: 24579.69 ❌
- **TP 1.5RR**: 24568.67 ❌
- **TP 2RR**: 24557.64 ❌
- **TP 2.5RR**: 24546.61 ❌
- **TP 3RR**: 24535.58 ❌
- **TP 3.5RR**: 24524.55 ❌
- **TP 4RR**: 24513.53 ❌
- **TP 4.5RR**: 24502.50 ❌
- **TP 5RR**: 24491.47 ❌
- **PnL**: -22.06 points (-1.0R)
- **MFE**: 18.50 points
- **MAE**: 27.00 points

### Trade #1358 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 07:30:00
- **FVG 5m**: 24609.50 - 24612.25
- **Entrée**: 24695.50 @ 2025-09-26 07:31:00
- **Stop Loss**: 24597.20
- **Risk**: 98.30 points
- **TP 1RR**: 24793.80 ❌
- **TP 1.5RR**: 24842.96 ❌
- **TP 2RR**: 24892.11 ❌
- **TP 2.5RR**: 24941.26 ❌
- **TP 3RR**: 24990.41 ❌
- **TP 3.5RR**: 25039.57 ❌
- **TP 4RR**: 25088.72 ❌
- **TP 4.5RR**: 25137.87 ❌
- **TP 5RR**: 25187.02 ❌
- **PnL**: -98.30 points (-1.0R)
- **MFE**: 52.00 points
- **MAE**: 98.50 points

### Trade #1359 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 07:45:00
- **FVG 5m**: 24706.75 - 24719.75
- **Entrée**: 24703.50 @ 2025-09-26 07:50:00
- **Stop Loss**: 24732.11
- **Risk**: 28.61 points
- **TP 1RR**: 24674.89 ✅
- **TP 1.5RR**: 24660.59 ✅
- **TP 2RR**: 24646.28 ✅
- **TP 2.5RR**: 24631.98 ✅
- **TP 3RR**: 24617.67 ✅
- **TP 3.5RR**: 24603.37 ✅
- **TP 4RR**: 24589.06 ❌
- **TP 4.5RR**: 24574.76 ❌
- **TP 5RR**: 24560.45 ❌
- **PnL**: -28.61 points (-1.0R)
- **MFE**: 106.50 points
- **MAE**: 29.75 points

### Trade #1360 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 08:15:00
- **FVG 5m**: 24706.75 - 24719.75
- **Entrée**: 24679.50 @ 2025-09-26 08:16:00
- **Stop Loss**: 24732.11
- **Risk**: 52.61 points
- **TP 1RR**: 24626.89 ✅
- **TP 1.5RR**: 24600.59 ✅
- **TP 2RR**: 24574.28 ❌
- **TP 2.5RR**: 24547.98 ❌
- **TP 3RR**: 24521.67 ❌
- **TP 3.5RR**: 24495.37 ❌
- **TP 4RR**: 24469.06 ❌
- **TP 4.5RR**: 24442.76 ❌
- **TP 5RR**: 24416.45 ❌
- **PnL**: -52.61 points (-1.0R)
- **MFE**: 82.50 points
- **MAE**: 53.75 points

### Trade #1361 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 08:15:00
- **FVG 5m**: 24706.75 - 24719.75
- **Entrée**: 24679.50 @ 2025-09-26 08:16:00
- **Stop Loss**: 24732.11
- **Risk**: 52.61 points
- **TP 1RR**: 24626.89 ✅
- **TP 1.5RR**: 24600.59 ✅
- **TP 2RR**: 24574.28 ❌
- **TP 2.5RR**: 24547.98 ❌
- **TP 3RR**: 24521.67 ❌
- **TP 3.5RR**: 24495.37 ❌
- **TP 4RR**: 24469.06 ❌
- **TP 4.5RR**: 24442.76 ❌
- **TP 5RR**: 24416.45 ❌
- **PnL**: -52.61 points (-1.0R)
- **MFE**: 82.50 points
- **MAE**: 53.75 points

### Trade #1362 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 09:30:00
- **FVG 5m**: 24573.75 - 24583.25
- **Entrée**: 24605.25 @ 2025-09-26 09:38:00
- **Stop Loss**: 24561.46
- **Risk**: 43.79 points
- **TP 1RR**: 24649.04 ❌
- **TP 1.5RR**: 24670.93 ❌
- **TP 2RR**: 24692.82 ❌
- **TP 2.5RR**: 24714.72 ❌
- **TP 3RR**: 24736.61 ❌
- **TP 3.5RR**: 24758.50 ❌
- **TP 4RR**: 24780.40 ❌
- **TP 4.5RR**: 24802.29 ❌
- **TP 5RR**: 24824.18 ❌
- **PnL**: -43.79 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 55.25 points

### Trade #1363 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 09:30:00
- **FVG 5m**: 24573.75 - 24583.25
- **Entrée**: 24605.25 @ 2025-09-26 09:38:00
- **Stop Loss**: 24561.46
- **Risk**: 43.79 points
- **TP 1RR**: 24649.04 ❌
- **TP 1.5RR**: 24670.93 ❌
- **TP 2RR**: 24692.82 ❌
- **TP 2.5RR**: 24714.72 ❌
- **TP 3RR**: 24736.61 ❌
- **TP 3.5RR**: 24758.50 ❌
- **TP 4RR**: 24780.40 ❌
- **TP 4.5RR**: 24802.29 ❌
- **TP 5RR**: 24824.18 ❌
- **PnL**: -43.79 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 55.25 points

### Trade #1364 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 09:30:00
- **FVG 5m**: 24573.75 - 24583.25
- **Entrée**: 24605.25 @ 2025-09-26 09:38:00
- **Stop Loss**: 24561.46
- **Risk**: 43.79 points
- **TP 1RR**: 24649.04 ❌
- **TP 1.5RR**: 24670.93 ❌
- **TP 2RR**: 24692.82 ❌
- **TP 2.5RR**: 24714.72 ❌
- **TP 3RR**: 24736.61 ❌
- **TP 3.5RR**: 24758.50 ❌
- **TP 4RR**: 24780.40 ❌
- **TP 4.5RR**: 24802.29 ❌
- **TP 5RR**: 24824.18 ❌
- **PnL**: -43.79 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 55.25 points

### Trade #1365 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-28 19:00:00
- **FVG 5m**: 24728.75 - 24731.25
- **Entrée**: 24769.75 @ 2025-09-28 19:01:00
- **Stop Loss**: 24716.39
- **Risk**: 53.36 points
- **TP 1RR**: 24823.11 ✅
- **TP 1.5RR**: 24849.80 ✅
- **TP 2RR**: 24876.48 ✅
- **TP 2.5RR**: 24903.16 ✅
- **TP 3RR**: 24929.84 ✅
- **TP 3.5RR**: 24956.53 ✅
- **TP 4RR**: 24983.21 ❌
- **TP 4.5RR**: 25009.89 ❌
- **TP 5RR**: 25036.57 ❌
- **PnL**: -53.36 points (-1.0R)
- **MFE**: 205.75 points
- **MAE**: 60.75 points

### Trade #1366 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 01:30:00
- **FVG 5m**: 24821.75 - 24825.25
- **Entrée**: 24839.00 @ 2025-09-29 01:31:00
- **Stop Loss**: 24809.34
- **Risk**: 29.66 points
- **TP 1RR**: 24868.66 ✅
- **TP 1.5RR**: 24883.49 ✅
- **TP 2RR**: 24898.32 ✅
- **TP 2.5RR**: 24913.15 ✅
- **TP 3RR**: 24927.98 ✅
- **TP 3.5RR**: 24942.81 ✅
- **TP 4RR**: 24957.64 ✅
- **TP 4.5RR**: 24972.47 ✅
- **TP 5RR**: 24987.30 ❌
- **PnL**: -29.66 points (-1.0R)
- **MFE**: 136.50 points
- **MAE**: 36.25 points

### Trade #1367 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-29 10:00:00
- **FVG 5m**: 24917.25 - 24921.50
- **Entrée**: 24914.75 @ 2025-09-29 10:10:00
- **Stop Loss**: 24933.96
- **Risk**: 19.21 points
- **TP 1RR**: 24895.54 ✅
- **TP 1.5RR**: 24885.93 ✅
- **TP 2RR**: 24876.33 ✅
- **TP 2.5RR**: 24866.72 ✅
- **TP 3RR**: 24857.12 ✅
- **TP 3.5RR**: 24847.51 ✅
- **TP 4RR**: 24837.91 ✅
- **TP 4.5RR**: 24828.30 ✅
- **TP 5RR**: 24818.70 ✅
- **PnL**: 96.05 points (5.0R)
- **MFE**: 100.50 points
- **MAE**: 4.50 points

### Trade #1368 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-29 10:00:00
- **FVG 5m**: 24917.25 - 24921.50
- **Entrée**: 24914.75 @ 2025-09-29 10:10:00
- **Stop Loss**: 24933.96
- **Risk**: 19.21 points
- **TP 1RR**: 24895.54 ✅
- **TP 1.5RR**: 24885.93 ✅
- **TP 2RR**: 24876.33 ✅
- **TP 2.5RR**: 24866.72 ✅
- **TP 3RR**: 24857.12 ✅
- **TP 3.5RR**: 24847.51 ✅
- **TP 4RR**: 24837.91 ✅
- **TP 4.5RR**: 24828.30 ✅
- **TP 5RR**: 24818.70 ✅
- **PnL**: 96.05 points (5.0R)
- **MFE**: 100.50 points
- **MAE**: 4.50 points

### Trade #1369 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-29 10:00:00
- **FVG 5m**: 24917.25 - 24921.50
- **Entrée**: 24914.75 @ 2025-09-29 10:10:00
- **Stop Loss**: 24933.96
- **Risk**: 19.21 points
- **TP 1RR**: 24895.54 ✅
- **TP 1.5RR**: 24885.93 ✅
- **TP 2RR**: 24876.33 ✅
- **TP 2.5RR**: 24866.72 ✅
- **TP 3RR**: 24857.12 ✅
- **TP 3.5RR**: 24847.51 ✅
- **TP 4RR**: 24837.91 ✅
- **TP 4.5RR**: 24828.30 ✅
- **TP 5RR**: 24818.70 ✅
- **PnL**: 96.05 points (5.0R)
- **MFE**: 100.50 points
- **MAE**: 4.50 points

### Trade #1370 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 14:15:00
- **FVG 5m**: 24834.50 - 24837.50
- **Entrée**: 24840.00 @ 2025-09-29 14:50:00
- **Stop Loss**: 24822.08
- **Risk**: 17.92 points
- **TP 1RR**: 24857.92 ❌
- **TP 1.5RR**: 24866.88 ❌
- **TP 2RR**: 24875.83 ❌
- **TP 2.5RR**: 24884.79 ❌
- **TP 3RR**: 24893.75 ❌
- **TP 3.5RR**: 24902.71 ❌
- **TP 4RR**: 24911.67 ❌
- **TP 4.5RR**: 24920.63 ❌
- **TP 5RR**: 24929.59 ❌
- **PnL**: -17.92 points (-1.0R)
- **MFE**: 6.25 points
- **MAE**: 19.75 points

### Trade #1371 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 01:30:00
- **FVG 5m**: 24843.00 - 24846.25
- **Entrée**: 24837.75 @ 2025-09-30 01:40:00
- **Stop Loss**: 24858.67
- **Risk**: 20.92 points
- **TP 1RR**: 24816.83 ✅
- **TP 1.5RR**: 24806.37 ✅
- **TP 2RR**: 24795.90 ✅
- **TP 2.5RR**: 24785.44 ✅
- **TP 3RR**: 24774.98 ✅
- **TP 3.5RR**: 24764.52 ✅
- **TP 4RR**: 24754.06 ✅
- **TP 4.5RR**: 24743.60 ✅
- **TP 5RR**: 24733.13 ✅
- **PnL**: 104.62 points (5.0R)
- **MFE**: 105.75 points
- **MAE**: 7.25 points

### Trade #1372 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 02:30:00
- **FVG 5m**: 24843.00 - 24846.25
- **Entrée**: 24804.00 @ 2025-09-30 02:31:00
- **Stop Loss**: 24858.67
- **Risk**: 54.67 points
- **TP 1RR**: 24749.33 ✅
- **TP 1.5RR**: 24721.99 ❌
- **TP 2RR**: 24694.65 ❌
- **TP 2.5RR**: 24667.32 ❌
- **TP 3RR**: 24639.98 ❌
- **TP 3.5RR**: 24612.64 ❌
- **TP 4RR**: 24585.31 ❌
- **TP 4.5RR**: 24557.97 ❌
- **TP 5RR**: 24530.63 ❌
- **PnL**: -54.67 points (-1.0R)
- **MFE**: 81.75 points
- **MAE**: 55.25 points

### Trade #1373 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 02:45:00
- **FVG 5m**: 24793.50 - 24800.00
- **Entrée**: 24800.25 @ 2025-09-30 03:34:00
- **Stop Loss**: 24781.10
- **Risk**: 19.15 points
- **TP 1RR**: 24819.40 ✅
- **TP 1.5RR**: 24828.97 ❌
- **TP 2RR**: 24838.54 ❌
- **TP 2.5RR**: 24848.12 ❌
- **TP 3RR**: 24857.69 ❌
- **TP 3.5RR**: 24867.26 ❌
- **TP 4RR**: 24876.84 ❌
- **TP 4.5RR**: 24886.41 ❌
- **TP 5RR**: 24895.98 ❌
- **PnL**: -19.15 points (-1.0R)
- **MFE**: 20.00 points
- **MAE**: 20.25 points

### Trade #1374 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 07:15:00
- **FVG 5m**: 24796.50 - 24803.00
- **Entrée**: 24805.75 @ 2025-09-30 07:21:00
- **Stop Loss**: 24784.10
- **Risk**: 21.65 points
- **TP 1RR**: 24827.40 ✅
- **TP 1.5RR**: 24838.22 ✅
- **TP 2RR**: 24849.05 ❌
- **TP 2.5RR**: 24859.87 ❌
- **TP 3RR**: 24870.69 ❌
- **TP 3.5RR**: 24881.52 ❌
- **TP 4RR**: 24892.34 ❌
- **TP 4.5RR**: 24903.17 ❌
- **TP 5RR**: 24913.99 ❌
- **PnL**: -21.65 points (-1.0R)
- **MFE**: 39.25 points
- **MAE**: 34.75 points

### Trade #1375 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 07:15:00
- **FVG 5m**: 24796.50 - 24803.00
- **Entrée**: 24805.75 @ 2025-09-30 07:21:00
- **Stop Loss**: 24784.10
- **Risk**: 21.65 points
- **TP 1RR**: 24827.40 ✅
- **TP 1.5RR**: 24838.22 ✅
- **TP 2RR**: 24849.05 ❌
- **TP 2.5RR**: 24859.87 ❌
- **TP 3RR**: 24870.69 ❌
- **TP 3.5RR**: 24881.52 ❌
- **TP 4RR**: 24892.34 ❌
- **TP 4.5RR**: 24903.17 ❌
- **TP 5RR**: 24913.99 ❌
- **PnL**: -21.65 points (-1.0R)
- **MFE**: 39.25 points
- **MAE**: 34.75 points

### Trade #1376 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 09:45:00
- **FVG 5m**: 24774.25 - 24780.50
- **Entrée**: 24802.50 @ 2025-09-30 09:46:00
- **Stop Loss**: 24761.86
- **Risk**: 40.64 points
- **TP 1RR**: 24843.14 ✅
- **TP 1.5RR**: 24863.46 ❌
- **TP 2RR**: 24883.77 ❌
- **TP 2.5RR**: 24904.09 ❌
- **TP 3RR**: 24924.41 ❌
- **TP 3.5RR**: 24944.73 ❌
- **TP 4RR**: 24965.05 ❌
- **TP 4.5RR**: 24985.37 ❌
- **TP 5RR**: 25005.69 ❌
- **PnL**: -40.64 points (-1.0R)
- **MFE**: 60.25 points
- **MAE**: 47.00 points

### Trade #1377 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 10:00:00
- **FVG 5m**: 24795.25 - 24817.75
- **Entrée**: 24794.50 @ 2025-09-30 10:20:00
- **Stop Loss**: 24830.16
- **Risk**: 35.66 points
- **TP 1RR**: 24758.84 ✅
- **TP 1.5RR**: 24741.01 ❌
- **TP 2RR**: 24723.18 ❌
- **TP 2.5RR**: 24705.35 ❌
- **TP 3RR**: 24687.52 ❌
- **TP 3.5RR**: 24669.69 ❌
- **TP 4RR**: 24651.86 ❌
- **TP 4.5RR**: 24634.04 ❌
- **TP 5RR**: 24616.21 ❌
- **PnL**: -35.66 points (-1.0R)
- **MFE**: 39.00 points
- **MAE**: 49.25 points

### Trade #1378 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 10:15:00
- **FVG 5m**: 24835.50 - 24839.25
- **Entrée**: 24823.50 @ 2025-09-30 10:16:00
- **Stop Loss**: 24851.67
- **Risk**: 28.17 points
- **TP 1RR**: 24795.33 ✅
- **TP 1.5RR**: 24781.25 ✅
- **TP 2RR**: 24767.16 ✅
- **TP 2.5RR**: 24753.08 ✅
- **TP 3RR**: 24738.99 ✅
- **TP 3.5RR**: 24724.91 ❌
- **TP 4RR**: 24710.82 ❌
- **TP 4.5RR**: 24696.74 ❌
- **TP 5RR**: 24682.65 ❌
- **PnL**: -28.17 points (-1.0R)
- **MFE**: 91.75 points
- **MAE**: 28.25 points

### Trade #1379 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 12:15:00
- **FVG 5m**: 24798.25 - 24806.50
- **Entrée**: 24763.50 @ 2025-09-30 12:16:00
- **Stop Loss**: 24818.90
- **Risk**: 55.40 points
- **TP 1RR**: 24708.10 ❌
- **TP 1.5RR**: 24680.40 ❌
- **TP 2RR**: 24652.69 ❌
- **TP 2.5RR**: 24624.99 ❌
- **TP 3RR**: 24597.29 ❌
- **TP 3.5RR**: 24569.59 ❌
- **TP 4RR**: 24541.89 ❌
- **TP 4.5RR**: 24514.19 ❌
- **TP 5RR**: 24486.48 ❌
- **PnL**: -55.40 points (-1.0R)
- **MFE**: 31.75 points
- **MAE**: 65.25 points

### Trade #1380 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 12:15:00
- **FVG 5m**: 24798.25 - 24806.50
- **Entrée**: 24763.50 @ 2025-09-30 12:16:00
- **Stop Loss**: 24818.90
- **Risk**: 55.40 points
- **TP 1RR**: 24708.10 ❌
- **TP 1.5RR**: 24680.40 ❌
- **TP 2RR**: 24652.69 ❌
- **TP 2.5RR**: 24624.99 ❌
- **TP 3RR**: 24597.29 ❌
- **TP 3.5RR**: 24569.59 ❌
- **TP 4RR**: 24541.89 ❌
- **TP 4.5RR**: 24514.19 ❌
- **TP 5RR**: 24486.48 ❌
- **PnL**: -55.40 points (-1.0R)
- **MFE**: 31.75 points
- **MAE**: 65.25 points

### Trade #1381 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 15:00:00
- **FVG 5m**: 24886.00 - 24892.00
- **Entrée**: 24880.75 @ 2025-09-30 15:01:00
- **Stop Loss**: 24904.45
- **Risk**: 23.70 points
- **TP 1RR**: 24857.05 ✅
- **TP 1.5RR**: 24845.21 ✅
- **TP 2RR**: 24833.36 ✅
- **TP 2.5RR**: 24821.51 ✅
- **TP 3RR**: 24809.66 ✅
- **TP 3.5RR**: 24797.81 ✅
- **TP 4RR**: 24785.97 ✅
- **TP 4.5RR**: 24774.12 ✅
- **TP 5RR**: 24762.27 ✅
- **PnL**: 118.48 points (5.0R)
- **MFE**: 119.00 points
- **MAE**: 3.00 points

### Trade #1382 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 03:30:00
- **FVG 5m**: 24686.00 - 24728.00
- **Entrée**: 24730.00 @ 2025-10-01 03:50:00
- **Stop Loss**: 24673.66
- **Risk**: 56.34 points
- **TP 1RR**: 24786.34 ✅
- **TP 1.5RR**: 24814.51 ✅
- **TP 2RR**: 24842.69 ✅
- **TP 2.5RR**: 24870.86 ✅
- **TP 3RR**: 24899.03 ✅
- **TP 3.5RR**: 24927.20 ✅
- **TP 4RR**: 24955.37 ✅
- **TP 4.5RR**: 24983.54 ✅
- **TP 5RR**: 25011.72 ✅
- **PnL**: 281.72 points (5.0R)
- **MFE**: 283.25 points
- **MAE**: 16.25 points

### Trade #1383 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 03:30:00
- **FVG 5m**: 24686.00 - 24728.00
- **Entrée**: 24730.00 @ 2025-10-01 03:50:00
- **Stop Loss**: 24673.66
- **Risk**: 56.34 points
- **TP 1RR**: 24786.34 ✅
- **TP 1.5RR**: 24814.51 ✅
- **TP 2RR**: 24842.69 ✅
- **TP 2.5RR**: 24870.86 ✅
- **TP 3RR**: 24899.03 ✅
- **TP 3.5RR**: 24927.20 ✅
- **TP 4RR**: 24955.37 ✅
- **TP 4.5RR**: 24983.54 ✅
- **TP 5RR**: 25011.72 ✅
- **PnL**: 281.72 points (5.0R)
- **MFE**: 283.25 points
- **MAE**: 16.25 points

### Trade #1384 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 04:00:00
- **FVG 5m**: 24686.00 - 24728.00
- **Entrée**: 24729.00 @ 2025-10-01 04:07:00
- **Stop Loss**: 24673.66
- **Risk**: 55.34 points
- **TP 1RR**: 24784.34 ✅
- **TP 1.5RR**: 24812.01 ✅
- **TP 2RR**: 24839.69 ✅
- **TP 2.5RR**: 24867.36 ✅
- **TP 3RR**: 24895.03 ✅
- **TP 3.5RR**: 24922.70 ✅
- **TP 4RR**: 24950.37 ✅
- **TP 4.5RR**: 24978.04 ✅
- **TP 5RR**: 25005.72 ✅
- **PnL**: 276.72 points (5.0R)
- **MFE**: 281.25 points
- **MAE**: 7.25 points

### Trade #1385 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 04:30:00
- **FVG 5m**: 24742.00 - 24744.50
- **Entrée**: 24740.75 @ 2025-10-01 04:33:00
- **Stop Loss**: 24756.87
- **Risk**: 16.12 points
- **TP 1RR**: 24724.63 ❌
- **TP 1.5RR**: 24716.57 ❌
- **TP 2RR**: 24708.51 ❌
- **TP 2.5RR**: 24700.44 ❌
- **TP 3RR**: 24692.38 ❌
- **TP 3.5RR**: 24684.32 ❌
- **TP 4RR**: 24676.26 ❌
- **TP 4.5RR**: 24668.20 ❌
- **TP 5RR**: 24660.14 ❌
- **PnL**: -16.12 points (-1.0R)
- **MFE**: 2.75 points
- **MAE**: 20.50 points

### Trade #1386 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 06:00:00
- **FVG 5m**: 24742.75 - 24746.75
- **Entrée**: 24753.75 @ 2025-10-01 06:05:00
- **Stop Loss**: 24730.38
- **Risk**: 23.37 points
- **TP 1RR**: 24777.12 ✅
- **TP 1.5RR**: 24788.81 ✅
- **TP 2RR**: 24800.49 ✅
- **TP 2.5RR**: 24812.18 ✅
- **TP 3RR**: 24823.86 ✅
- **TP 3.5RR**: 24835.55 ✅
- **TP 4RR**: 24847.24 ❌
- **TP 4.5RR**: 24858.92 ❌
- **TP 5RR**: 24870.61 ❌
- **PnL**: -23.37 points (-1.0R)
- **MFE**: 87.75 points
- **MAE**: 27.75 points

### Trade #1387 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 08:15:00
- **FVG 5m**: 24738.50 - 24743.50
- **Entrée**: 24737.00 @ 2025-10-01 08:49:00
- **Stop Loss**: 24755.87
- **Risk**: 18.87 points
- **TP 1RR**: 24718.13 ❌
- **TP 1.5RR**: 24708.69 ❌
- **TP 2RR**: 24699.26 ❌
- **TP 2.5RR**: 24689.82 ❌
- **TP 3RR**: 24680.38 ❌
- **TP 3.5RR**: 24670.95 ❌
- **TP 4RR**: 24661.51 ❌
- **TP 4.5RR**: 24652.08 ❌
- **TP 5RR**: 24642.64 ❌
- **PnL**: -18.87 points (-1.0R)
- **MFE**: 11.00 points
- **MAE**: 26.75 points

### Trade #1388 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 08:15:00
- **FVG 5m**: 24738.50 - 24743.50
- **Entrée**: 24737.00 @ 2025-10-01 08:49:00
- **Stop Loss**: 24755.87
- **Risk**: 18.87 points
- **TP 1RR**: 24718.13 ❌
- **TP 1.5RR**: 24708.69 ❌
- **TP 2RR**: 24699.26 ❌
- **TP 2.5RR**: 24689.82 ❌
- **TP 3RR**: 24680.38 ❌
- **TP 3.5RR**: 24670.95 ❌
- **TP 4RR**: 24661.51 ❌
- **TP 4.5RR**: 24652.08 ❌
- **TP 5RR**: 24642.64 ❌
- **PnL**: -18.87 points (-1.0R)
- **MFE**: 11.00 points
- **MAE**: 26.75 points

### Trade #1389 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 08:45:00
- **FVG 5m**: 24784.75 - 24805.25
- **Entrée**: 24773.50 @ 2025-10-01 08:48:00
- **Stop Loss**: 24817.65
- **Risk**: 44.15 points
- **TP 1RR**: 24729.35 ✅
- **TP 1.5RR**: 24707.27 ❌
- **TP 2RR**: 24685.19 ❌
- **TP 2.5RR**: 24663.12 ❌
- **TP 3RR**: 24641.04 ❌
- **TP 3.5RR**: 24618.97 ❌
- **TP 4RR**: 24596.89 ❌
- **TP 4.5RR**: 24574.81 ❌
- **TP 5RR**: 24552.74 ❌
- **PnL**: -44.15 points (-1.0R)
- **MFE**: 47.50 points
- **MAE**: 46.00 points

### Trade #1390 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-02 08:30:00
- **FVG 5m**: 25163.75 - 25173.00
- **Entrée**: 25144.75 @ 2025-10-02 08:31:00
- **Stop Loss**: 25185.59
- **Risk**: 40.84 points
- **TP 1RR**: 25103.91 ✅
- **TP 1.5RR**: 25083.50 ✅
- **TP 2RR**: 25063.08 ✅
- **TP 2.5RR**: 25042.66 ✅
- **TP 3RR**: 25022.24 ✅
- **TP 3.5RR**: 25001.82 ✅
- **TP 4RR**: 24981.40 ❌
- **TP 4.5RR**: 24960.99 ❌
- **TP 5RR**: 24940.57 ❌
- **PnL**: -40.84 points (-1.0R)
- **MFE**: 151.00 points
- **MAE**: 41.25 points

### Trade #1391 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-02 09:45:00
- **FVG 5m**: 25163.75 - 25173.00
- **Entrée**: 25026.50 @ 2025-10-02 09:46:00
- **Stop Loss**: 25185.59
- **Risk**: 159.09 points
- **TP 1RR**: 24867.41 ❌
- **TP 1.5RR**: 24787.87 ❌
- **TP 2RR**: 24708.33 ❌
- **TP 2.5RR**: 24628.78 ❌
- **TP 3RR**: 24549.24 ❌
- **TP 3.5RR**: 24469.70 ❌
- **TP 4RR**: 24390.15 ❌
- **TP 4.5RR**: 24310.61 ❌
- **TP 5RR**: 24231.07 ❌
- **PnL**: -159.09 points (-1.0R)
- **MFE**: 32.75 points
- **MAE**: 159.50 points

### Trade #1392 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-02 09:45:00
- **FVG 5m**: 25163.75 - 25173.00
- **Entrée**: 25026.50 @ 2025-10-02 09:46:00
- **Stop Loss**: 25185.59
- **Risk**: 159.09 points
- **TP 1RR**: 24867.41 ❌
- **TP 1.5RR**: 24787.87 ❌
- **TP 2RR**: 24708.33 ❌
- **TP 2.5RR**: 24628.78 ❌
- **TP 3RR**: 24549.24 ❌
- **TP 3.5RR**: 24469.70 ❌
- **TP 4RR**: 24390.15 ❌
- **TP 4.5RR**: 24310.61 ❌
- **TP 5RR**: 24231.07 ❌
- **PnL**: -159.09 points (-1.0R)
- **MFE**: 32.75 points
- **MAE**: 159.50 points

### Trade #1393 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-02 09:45:00
- **FVG 5m**: 25163.75 - 25173.00
- **Entrée**: 25026.50 @ 2025-10-02 09:46:00
- **Stop Loss**: 25185.59
- **Risk**: 159.09 points
- **TP 1RR**: 24867.41 ❌
- **TP 1.5RR**: 24787.87 ❌
- **TP 2RR**: 24708.33 ❌
- **TP 2.5RR**: 24628.78 ❌
- **TP 3RR**: 24549.24 ❌
- **TP 3.5RR**: 24469.70 ❌
- **TP 4RR**: 24390.15 ❌
- **TP 4.5RR**: 24310.61 ❌
- **TP 5RR**: 24231.07 ❌
- **PnL**: -159.09 points (-1.0R)
- **MFE**: 32.75 points
- **MAE**: 159.50 points

### Trade #1394 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 10:45:00
- **FVG 5m**: 25071.50 - 25076.25
- **Entrée**: 25078.00 @ 2025-10-02 10:57:00
- **Stop Loss**: 25058.96
- **Risk**: 19.04 points
- **TP 1RR**: 25097.04 ❌
- **TP 1.5RR**: 25106.55 ❌
- **TP 2RR**: 25116.07 ❌
- **TP 2.5RR**: 25125.59 ❌
- **TP 3RR**: 25135.11 ❌
- **TP 3.5RR**: 25144.63 ❌
- **TP 4RR**: 25154.14 ❌
- **TP 4.5RR**: 25163.66 ❌
- **TP 5RR**: 25173.18 ❌
- **PnL**: -19.04 points (-1.0R)
- **MFE**: 4.25 points
- **MAE**: 36.50 points

### Trade #1395 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 17:30:00
- **FVG 5m**: 25103.00 - 25106.75
- **Entrée**: 25108.25 @ 2025-10-02 18:10:00
- **Stop Loss**: 25090.45
- **Risk**: 17.80 points
- **TP 1RR**: 25126.05 ✅
- **TP 1.5RR**: 25134.95 ✅
- **TP 2RR**: 25143.85 ✅
- **TP 2.5RR**: 25152.75 ✅
- **TP 3RR**: 25161.65 ✅
- **TP 3.5RR**: 25170.56 ✅
- **TP 4RR**: 25179.46 ✅
- **TP 4.5RR**: 25188.36 ✅
- **TP 5RR**: 25197.26 ❌
- **PnL**: -17.80 points (-1.0R)
- **MFE**: 88.25 points
- **MAE**: 31.75 points

### Trade #1396 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-03 07:30:00
- **FVG 5m**: 25148.00 - 25153.25
- **Entrée**: 25143.00 @ 2025-10-03 07:31:00
- **Stop Loss**: 25165.83
- **Risk**: 22.83 points
- **TP 1RR**: 25120.17 ✅
- **TP 1.5RR**: 25108.76 ✅
- **TP 2RR**: 25097.35 ❌
- **TP 2.5RR**: 25085.93 ❌
- **TP 3RR**: 25074.52 ❌
- **TP 3.5RR**: 25063.11 ❌
- **TP 4RR**: 25051.69 ❌
- **TP 4.5RR**: 25040.28 ❌
- **TP 5RR**: 25028.87 ❌
- **PnL**: -22.83 points (-1.0R)
- **MFE**: 40.00 points
- **MAE**: 25.00 points

### Trade #1397 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 09:00:00
- **FVG 5m**: 25117.75 - 25122.00
- **Entrée**: 25122.25 @ 2025-10-03 09:41:00
- **Stop Loss**: 25105.19
- **Risk**: 17.06 points
- **TP 1RR**: 25139.31 ❌
- **TP 1.5RR**: 25147.84 ❌
- **TP 2RR**: 25156.37 ❌
- **TP 2.5RR**: 25164.90 ❌
- **TP 3RR**: 25173.43 ❌
- **TP 3.5RR**: 25181.96 ❌
- **TP 4RR**: 25190.49 ❌
- **TP 4.5RR**: 25199.01 ❌
- **TP 5RR**: 25207.54 ❌
- **PnL**: -17.06 points (-1.0R)
- **MFE**: 1.00 points
- **MAE**: 20.75 points

### Trade #1398 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-03 12:45:00
- **FVG 5m**: 25137.00 - 25140.50
- **Entrée**: 24987.00 @ 2025-10-03 12:46:00
- **Stop Loss**: 25153.07
- **Risk**: 166.07 points
- **TP 1RR**: 24820.93 ❌
- **TP 1.5RR**: 24737.89 ❌
- **TP 2RR**: 24654.86 ❌
- **TP 2.5RR**: 24571.82 ❌
- **TP 3RR**: 24488.79 ❌
- **TP 3.5RR**: 24405.75 ❌
- **TP 4RR**: 24322.72 ❌
- **TP 4.5RR**: 24239.68 ❌
- **TP 5RR**: 24156.65 ❌
- **PnL**: -166.07 points (-1.0R)
- **MFE**: 63.75 points
- **MAE**: 182.50 points

### Trade #1399 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 13:15:00
- **FVG 5m**: 24990.75 - 25001.75
- **Entrée**: 25006.75 @ 2025-10-03 13:19:00
- **Stop Loss**: 24978.25
- **Risk**: 28.50 points
- **TP 1RR**: 25035.25 ✅
- **TP 1.5RR**: 25049.49 ❌
- **TP 2RR**: 25063.74 ❌
- **TP 2.5RR**: 25077.99 ❌
- **TP 3RR**: 25092.24 ❌
- **TP 3.5RR**: 25106.48 ❌
- **TP 4RR**: 25120.73 ❌
- **TP 4.5RR**: 25134.98 ❌
- **TP 5RR**: 25149.23 ❌
- **PnL**: -28.50 points (-1.0R)
- **MFE**: 37.75 points
- **MAE**: 31.75 points

### Trade #1400 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 13:15:00
- **FVG 5m**: 24990.75 - 25001.75
- **Entrée**: 25006.75 @ 2025-10-03 13:19:00
- **Stop Loss**: 24978.25
- **Risk**: 28.50 points
- **TP 1RR**: 25035.25 ✅
- **TP 1.5RR**: 25049.49 ❌
- **TP 2RR**: 25063.74 ❌
- **TP 2.5RR**: 25077.99 ❌
- **TP 3RR**: 25092.24 ❌
- **TP 3.5RR**: 25106.48 ❌
- **TP 4RR**: 25120.73 ❌
- **TP 4.5RR**: 25134.98 ❌
- **TP 5RR**: 25149.23 ❌
- **PnL**: -28.50 points (-1.0R)
- **MFE**: 37.75 points
- **MAE**: 31.75 points

### Trade #1401 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 13:15:00
- **FVG 5m**: 24990.75 - 25001.75
- **Entrée**: 25006.75 @ 2025-10-03 13:19:00
- **Stop Loss**: 24978.25
- **Risk**: 28.50 points
- **TP 1RR**: 25035.25 ✅
- **TP 1.5RR**: 25049.49 ❌
- **TP 2RR**: 25063.74 ❌
- **TP 2.5RR**: 25077.99 ❌
- **TP 3RR**: 25092.24 ❌
- **TP 3.5RR**: 25106.48 ❌
- **TP 4RR**: 25120.73 ❌
- **TP 4.5RR**: 25134.98 ❌
- **TP 5RR**: 25149.23 ❌
- **PnL**: -28.50 points (-1.0R)
- **MFE**: 37.75 points
- **MAE**: 31.75 points

### Trade #1402 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 13:15:00
- **FVG 5m**: 24990.75 - 25001.75
- **Entrée**: 25006.75 @ 2025-10-03 13:19:00
- **Stop Loss**: 24978.25
- **Risk**: 28.50 points
- **TP 1RR**: 25035.25 ✅
- **TP 1.5RR**: 25049.49 ❌
- **TP 2RR**: 25063.74 ❌
- **TP 2.5RR**: 25077.99 ❌
- **TP 3RR**: 25092.24 ❌
- **TP 3.5RR**: 25106.48 ❌
- **TP 4RR**: 25120.73 ❌
- **TP 4.5RR**: 25134.98 ❌
- **TP 5RR**: 25149.23 ❌
- **PnL**: -28.50 points (-1.0R)
- **MFE**: 37.75 points
- **MAE**: 31.75 points

### Trade #1403 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-03 14:45:00
- **FVG 5m**: 25010.50 - 25017.25
- **Entrée**: 24997.75 @ 2025-10-03 14:50:00
- **Stop Loss**: 25029.76
- **Risk**: 32.01 points
- **TP 1RR**: 24965.74 ❌
- **TP 1.5RR**: 24949.74 ❌
- **TP 2RR**: 24933.73 ❌
- **TP 2.5RR**: 24917.73 ❌
- **TP 3RR**: 24901.72 ❌
- **TP 3.5RR**: 24885.72 ❌
- **TP 4RR**: 24869.72 ❌
- **TP 4.5RR**: 24853.71 ❌
- **TP 5RR**: 24837.71 ❌
- **PnL**: -32.01 points (-1.0R)
- **MFE**: 24.00 points
- **MAE**: 32.75 points

### Trade #1404 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-03 14:45:00
- **FVG 5m**: 25010.50 - 25017.25
- **Entrée**: 24997.75 @ 2025-10-03 14:50:00
- **Stop Loss**: 25029.76
- **Risk**: 32.01 points
- **TP 1RR**: 24965.74 ❌
- **TP 1.5RR**: 24949.74 ❌
- **TP 2RR**: 24933.73 ❌
- **TP 2.5RR**: 24917.73 ❌
- **TP 3RR**: 24901.72 ❌
- **TP 3.5RR**: 24885.72 ❌
- **TP 4RR**: 24869.72 ❌
- **TP 4.5RR**: 24853.71 ❌
- **TP 5RR**: 24837.71 ❌
- **PnL**: -32.01 points (-1.0R)
- **MFE**: 24.00 points
- **MAE**: 32.75 points

### Trade #1405 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 00:00:00
- **FVG 5m**: 25083.00 - 25087.00
- **Entrée**: 25082.25 @ 2025-10-06 00:32:00
- **Stop Loss**: 25099.54
- **Risk**: 17.29 points
- **TP 1RR**: 25064.96 ❌
- **TP 1.5RR**: 25056.31 ❌
- **TP 2RR**: 25047.66 ❌
- **TP 2.5RR**: 25039.02 ❌
- **TP 3RR**: 25030.37 ❌
- **TP 3.5RR**: 25021.72 ❌
- **TP 4RR**: 25013.08 ❌
- **TP 4.5RR**: 25004.43 ❌
- **TP 5RR**: 24995.78 ❌
- **PnL**: -17.29 points (-1.0R)
- **MFE**: 1.75 points
- **MAE**: 22.00 points

### Trade #1406 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-06 02:30:00
- **FVG 5m**: 25090.75 - 25097.25
- **Entrée**: 25106.75 @ 2025-10-06 03:05:00
- **Stop Loss**: 25078.20
- **Risk**: 28.55 points
- **TP 1RR**: 25135.30 ✅
- **TP 1.5RR**: 25149.57 ✅
- **TP 2RR**: 25163.84 ✅
- **TP 2.5RR**: 25178.11 ✅
- **TP 3RR**: 25192.39 ✅
- **TP 3.5RR**: 25206.66 ✅
- **TP 4RR**: 25220.93 ✅
- **TP 4.5RR**: 25235.20 ✅
- **TP 5RR**: 25249.48 ✅
- **PnL**: 142.73 points (5.0R)
- **MFE**: 144.75 points
- **MAE**: 13.00 points

### Trade #1407 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-06 02:45:00
- **FVG 5m**: 25077.00 - 25081.25
- **Entrée**: 25085.50 @ 2025-10-06 02:52:00
- **Stop Loss**: 25064.46
- **Risk**: 21.04 points
- **TP 1RR**: 25106.54 ✅
- **TP 1.5RR**: 25117.06 ✅
- **TP 2RR**: 25127.58 ✅
- **TP 2.5RR**: 25138.10 ✅
- **TP 3RR**: 25148.62 ✅
- **TP 3.5RR**: 25159.13 ✅
- **TP 4RR**: 25169.65 ✅
- **TP 4.5RR**: 25180.17 ✅
- **TP 5RR**: 25190.69 ✅
- **PnL**: 105.19 points (5.0R)
- **MFE**: 106.25 points
- **MAE**: 7.25 points

### Trade #1408 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 06:00:00
- **FVG 5m**: 25150.00 - 25164.25
- **Entrée**: 25149.75 @ 2025-10-06 06:09:00
- **Stop Loss**: 25176.83
- **Risk**: 27.08 points
- **TP 1RR**: 25122.67 ❌
- **TP 1.5RR**: 25109.13 ❌
- **TP 2RR**: 25095.59 ❌
- **TP 2.5RR**: 25082.04 ❌
- **TP 3RR**: 25068.50 ❌
- **TP 3.5RR**: 25054.96 ❌
- **TP 4RR**: 25041.42 ❌
- **TP 4.5RR**: 25027.88 ❌
- **TP 5RR**: 25014.34 ❌
- **PnL**: -27.08 points (-1.0R)
- **MFE**: 21.25 points
- **MAE**: 28.25 points

### Trade #1409 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 07:30:00
- **FVG 5m**: 25207.25 - 25217.00
- **Entrée**: 25205.00 @ 2025-10-06 07:31:00
- **Stop Loss**: 25229.61
- **Risk**: 24.61 points
- **TP 1RR**: 25180.39 ✅
- **TP 1.5RR**: 25168.09 ✅
- **TP 2RR**: 25155.78 ✅
- **TP 2.5RR**: 25143.48 ✅
- **TP 3RR**: 25131.17 ✅
- **TP 3.5RR**: 25118.87 ✅
- **TP 4RR**: 25106.57 ❌
- **TP 4.5RR**: 25094.26 ❌
- **TP 5RR**: 25081.96 ❌
- **PnL**: -24.61 points (-1.0R)
- **MFE**: 96.50 points
- **MAE**: 25.00 points

### Trade #1410 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 07:30:00
- **FVG 5m**: 25207.25 - 25217.00
- **Entrée**: 25205.00 @ 2025-10-06 07:31:00
- **Stop Loss**: 25229.61
- **Risk**: 24.61 points
- **TP 1RR**: 25180.39 ✅
- **TP 1.5RR**: 25168.09 ✅
- **TP 2RR**: 25155.78 ✅
- **TP 2.5RR**: 25143.48 ✅
- **TP 3RR**: 25131.17 ✅
- **TP 3.5RR**: 25118.87 ✅
- **TP 4RR**: 25106.57 ❌
- **TP 4.5RR**: 25094.26 ❌
- **TP 5RR**: 25081.96 ❌
- **PnL**: -24.61 points (-1.0R)
- **MFE**: 96.50 points
- **MAE**: 25.00 points

### Trade #1411 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 08:30:00
- **FVG 5m**: 25207.25 - 25217.00
- **Entrée**: 25192.50 @ 2025-10-06 08:31:00
- **Stop Loss**: 25229.61
- **Risk**: 37.11 points
- **TP 1RR**: 25155.39 ✅
- **TP 1.5RR**: 25136.84 ✅
- **TP 2RR**: 25118.28 ✅
- **TP 2.5RR**: 25099.73 ❌
- **TP 3RR**: 25081.17 ❌
- **TP 3.5RR**: 25062.62 ❌
- **TP 4RR**: 25044.07 ❌
- **TP 4.5RR**: 25025.51 ❌
- **TP 5RR**: 25006.96 ❌
- **PnL**: -37.11 points (-1.0R)
- **MFE**: 84.00 points
- **MAE**: 37.50 points

### Trade #1412 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 08:30:00
- **FVG 5m**: 25207.25 - 25217.00
- **Entrée**: 25192.50 @ 2025-10-06 08:31:00
- **Stop Loss**: 25229.61
- **Risk**: 37.11 points
- **TP 1RR**: 25155.39 ✅
- **TP 1.5RR**: 25136.84 ✅
- **TP 2RR**: 25118.28 ✅
- **TP 2.5RR**: 25099.73 ❌
- **TP 3RR**: 25081.17 ❌
- **TP 3.5RR**: 25062.62 ❌
- **TP 4RR**: 25044.07 ❌
- **TP 4.5RR**: 25025.51 ❌
- **TP 5RR**: 25006.96 ❌
- **PnL**: -37.11 points (-1.0R)
- **MFE**: 84.00 points
- **MAE**: 37.50 points

### Trade #1413 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 08:30:00
- **FVG 5m**: 25207.25 - 25217.00
- **Entrée**: 25192.50 @ 2025-10-06 08:31:00
- **Stop Loss**: 25229.61
- **Risk**: 37.11 points
- **TP 1RR**: 25155.39 ✅
- **TP 1.5RR**: 25136.84 ✅
- **TP 2RR**: 25118.28 ✅
- **TP 2.5RR**: 25099.73 ❌
- **TP 3RR**: 25081.17 ❌
- **TP 3.5RR**: 25062.62 ❌
- **TP 4RR**: 25044.07 ❌
- **TP 4.5RR**: 25025.51 ❌
- **TP 5RR**: 25006.96 ❌
- **PnL**: -37.11 points (-1.0R)
- **MFE**: 84.00 points
- **MAE**: 37.50 points

### Trade #1414 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 14:30:00
- **FVG 5m**: 25201.00 - 25216.75
- **Entrée**: 25198.75 @ 2025-10-06 14:46:00
- **Stop Loss**: 25229.36
- **Risk**: 30.61 points
- **TP 1RR**: 25168.14 ✅
- **TP 1.5RR**: 25152.84 ✅
- **TP 2RR**: 25137.53 ✅
- **TP 2.5RR**: 25122.23 ❌
- **TP 3RR**: 25106.92 ❌
- **TP 3.5RR**: 25091.62 ❌
- **TP 4RR**: 25076.32 ❌
- **TP 4.5RR**: 25061.01 ❌
- **TP 5RR**: 25045.71 ❌
- **PnL**: -30.61 points (-1.0R)
- **MFE**: 76.25 points
- **MAE**: 32.75 points

### Trade #1415 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 08:00:00
- **FVG 5m**: 25235.25 - 25243.00
- **Entrée**: 25235.00 @ 2025-10-07 08:22:00
- **Stop Loss**: 25255.62
- **Risk**: 20.62 points
- **TP 1RR**: 25214.38 ❌
- **TP 1.5RR**: 25204.07 ❌
- **TP 2RR**: 25193.76 ❌
- **TP 2.5RR**: 25183.45 ❌
- **TP 3RR**: 25173.14 ❌
- **TP 3.5RR**: 25162.82 ❌
- **TP 4RR**: 25152.51 ❌
- **TP 4.5RR**: 25142.20 ❌
- **TP 5RR**: 25131.89 ❌
- **PnL**: -20.62 points (-1.0R)
- **MFE**: 18.00 points
- **MAE**: 28.25 points

### Trade #1416 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 08:45:00
- **FVG 5m**: 25257.50 - 25260.25
- **Entrée**: 25240.75 @ 2025-10-07 08:46:00
- **Stop Loss**: 25272.88
- **Risk**: 32.13 points
- **TP 1RR**: 25208.62 ✅
- **TP 1.5RR**: 25192.55 ✅
- **TP 2RR**: 25176.49 ✅
- **TP 2.5RR**: 25160.42 ✅
- **TP 3RR**: 25144.36 ✅
- **TP 3.5RR**: 25128.29 ✅
- **TP 4RR**: 25112.23 ✅
- **TP 4.5RR**: 25096.16 ✅
- **TP 5RR**: 25080.10 ✅
- **PnL**: 160.65 points (5.0R)
- **MFE**: 169.75 points
- **MAE**: 24.00 points

### Trade #1417 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 09:45:00
- **FVG 5m**: 25257.50 - 25260.25
- **Entrée**: 25197.25 @ 2025-10-07 09:46:00
- **Stop Loss**: 25272.88
- **Risk**: 75.63 points
- **TP 1RR**: 25121.62 ✅
- **TP 1.5RR**: 25083.80 ✅
- **TP 2RR**: 25045.99 ✅
- **TP 2.5RR**: 25008.17 ✅
- **TP 3RR**: 24970.36 ❌
- **TP 3.5RR**: 24932.54 ❌
- **TP 4RR**: 24894.73 ❌
- **TP 4.5RR**: 24856.91 ❌
- **TP 5RR**: 24819.10 ❌
- **PnL**: -75.63 points (-1.0R)
- **MFE**: 212.50 points
- **MAE**: 79.00 points

### Trade #1418 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 10:15:00
- **FVG 5m**: 25257.50 - 25260.25
- **Entrée**: 25111.25 @ 2025-10-07 10:16:00
- **Stop Loss**: 25272.88
- **Risk**: 161.63 points
- **TP 1RR**: 24949.62 ❌
- **TP 1.5RR**: 24868.80 ❌
- **TP 2RR**: 24787.99 ❌
- **TP 2.5RR**: 24707.17 ❌
- **TP 3RR**: 24626.36 ❌
- **TP 3.5RR**: 24545.54 ❌
- **TP 4RR**: 24464.73 ❌
- **TP 4.5RR**: 24383.91 ❌
- **TP 5RR**: 24303.10 ❌
- **PnL**: -161.63 points (-1.0R)
- **MFE**: 126.50 points
- **MAE**: 165.00 points

### Trade #1419 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-08 03:45:00
- **FVG 5m**: 25094.75 - 25101.00
- **Entrée**: 25089.00 @ 2025-10-08 03:55:00
- **Stop Loss**: 25113.55
- **Risk**: 24.55 points
- **TP 1RR**: 25064.45 ✅
- **TP 1.5RR**: 25052.17 ✅
- **TP 2RR**: 25039.90 ❌
- **TP 2.5RR**: 25027.62 ❌
- **TP 3RR**: 25015.35 ❌
- **TP 3.5RR**: 25003.07 ❌
- **TP 4RR**: 24990.80 ❌
- **TP 4.5RR**: 24978.52 ❌
- **TP 5RR**: 24966.25 ❌
- **PnL**: -24.55 points (-1.0R)
- **MFE**: 46.50 points
- **MAE**: 26.25 points

### Trade #1420 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-08 03:45:00
- **FVG 5m**: 25094.75 - 25101.00
- **Entrée**: 25089.00 @ 2025-10-08 03:55:00
- **Stop Loss**: 25113.55
- **Risk**: 24.55 points
- **TP 1RR**: 25064.45 ✅
- **TP 1.5RR**: 25052.17 ✅
- **TP 2RR**: 25039.90 ❌
- **TP 2.5RR**: 25027.62 ❌
- **TP 3RR**: 25015.35 ❌
- **TP 3.5RR**: 25003.07 ❌
- **TP 4RR**: 24990.80 ❌
- **TP 4.5RR**: 24978.52 ❌
- **TP 5RR**: 24966.25 ❌
- **PnL**: -24.55 points (-1.0R)
- **MFE**: 46.50 points
- **MAE**: 26.25 points

### Trade #1421 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-08 08:30:00
- **FVG 5m**: 25067.75 - 25078.00
- **Entrée**: 25110.00 @ 2025-10-08 08:31:00
- **Stop Loss**: 25055.22
- **Risk**: 54.78 points
- **TP 1RR**: 25164.78 ✅
- **TP 1.5RR**: 25192.18 ✅
- **TP 2RR**: 25219.57 ✅
- **TP 2.5RR**: 25246.96 ✅
- **TP 3RR**: 25274.35 ✅
- **TP 3.5RR**: 25301.74 ✅
- **TP 4RR**: 25329.14 ✅
- **TP 4.5RR**: 25356.53 ✅
- **TP 5RR**: 25383.92 ✅
- **PnL**: 273.92 points (5.0R)
- **MFE**: 278.00 points
- **MAE**: 0.50 points

### Trade #1422 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-08 08:30:00
- **FVG 5m**: 25067.75 - 25078.00
- **Entrée**: 25110.00 @ 2025-10-08 08:31:00
- **Stop Loss**: 25055.22
- **Risk**: 54.78 points
- **TP 1RR**: 25164.78 ✅
- **TP 1.5RR**: 25192.18 ✅
- **TP 2RR**: 25219.57 ✅
- **TP 2.5RR**: 25246.96 ✅
- **TP 3RR**: 25274.35 ✅
- **TP 3.5RR**: 25301.74 ✅
- **TP 4RR**: 25329.14 ✅
- **TP 4.5RR**: 25356.53 ✅
- **TP 5RR**: 25383.92 ✅
- **PnL**: 273.92 points (5.0R)
- **MFE**: 278.00 points
- **MAE**: 0.50 points

### Trade #1423 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-08 08:45:00
- **FVG 5m**: 25067.75 - 25078.00
- **Entrée**: 25142.75 @ 2025-10-08 08:46:00
- **Stop Loss**: 25055.22
- **Risk**: 87.53 points
- **TP 1RR**: 25230.28 ✅
- **TP 1.5RR**: 25274.05 ✅
- **TP 2RR**: 25317.82 ✅
- **TP 2.5RR**: 25361.58 ✅
- **TP 3RR**: 25405.35 ❌
- **TP 3.5RR**: 25449.12 ❌
- **TP 4RR**: 25492.89 ❌
- **TP 4.5RR**: 25536.65 ❌
- **TP 5RR**: 25580.42 ❌
- **PnL**: -87.53 points (-1.0R)
- **MFE**: 251.25 points
- **MAE**: 88.00 points

### Trade #1424 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 01:15:00
- **FVG 5m**: 25333.75 - 25343.25
- **Entrée**: 25333.25 @ 2025-10-10 01:35:00
- **Stop Loss**: 25355.92
- **Risk**: 22.67 points
- **TP 1RR**: 25310.58 ✅
- **TP 1.5RR**: 25299.24 ✅
- **TP 2RR**: 25287.91 ✅
- **TP 2.5RR**: 25276.57 ✅
- **TP 3RR**: 25265.24 ✅
- **TP 3.5RR**: 25253.90 ✅
- **TP 4RR**: 25242.56 ❌
- **TP 4.5RR**: 25231.23 ❌
- **TP 5RR**: 25219.89 ❌
- **PnL**: -22.67 points (-1.0R)
- **MFE**: 82.25 points
- **MAE**: 38.75 points

### Trade #1425 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 01:15:00
- **FVG 5m**: 25333.75 - 25343.25
- **Entrée**: 25333.25 @ 2025-10-10 01:35:00
- **Stop Loss**: 25355.92
- **Risk**: 22.67 points
- **TP 1RR**: 25310.58 ✅
- **TP 1.5RR**: 25299.24 ✅
- **TP 2RR**: 25287.91 ✅
- **TP 2.5RR**: 25276.57 ✅
- **TP 3RR**: 25265.24 ✅
- **TP 3.5RR**: 25253.90 ✅
- **TP 4RR**: 25242.56 ❌
- **TP 4.5RR**: 25231.23 ❌
- **TP 5RR**: 25219.89 ❌
- **PnL**: -22.67 points (-1.0R)
- **MFE**: 82.25 points
- **MAE**: 38.75 points

### Trade #1426 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 04:00:00
- **FVG 5m**: 25312.25 - 25320.00
- **Entrée**: 25320.50 @ 2025-10-10 04:04:00
- **Stop Loss**: 25299.59
- **Risk**: 20.91 points
- **TP 1RR**: 25341.41 ❌
- **TP 1.5RR**: 25351.86 ❌
- **TP 2RR**: 25362.31 ❌
- **TP 2.5RR**: 25372.77 ❌
- **TP 3RR**: 25383.22 ❌
- **TP 3.5RR**: 25393.67 ❌
- **TP 4RR**: 25404.12 ❌
- **TP 4.5RR**: 25414.58 ❌
- **TP 5RR**: 25425.03 ❌
- **PnL**: -20.91 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 29.75 points

### Trade #1427 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 04:00:00
- **FVG 5m**: 25312.25 - 25320.00
- **Entrée**: 25320.50 @ 2025-10-10 04:04:00
- **Stop Loss**: 25299.59
- **Risk**: 20.91 points
- **TP 1RR**: 25341.41 ❌
- **TP 1.5RR**: 25351.86 ❌
- **TP 2RR**: 25362.31 ❌
- **TP 2.5RR**: 25372.77 ❌
- **TP 3RR**: 25383.22 ❌
- **TP 3.5RR**: 25393.67 ❌
- **TP 4RR**: 25404.12 ❌
- **TP 4.5RR**: 25414.58 ❌
- **TP 5RR**: 25425.03 ❌
- **PnL**: -20.91 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 29.75 points

### Trade #1428 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 05:45:00
- **FVG 5m**: 25265.75 - 25269.25
- **Entrée**: 25285.25 @ 2025-10-10 05:46:00
- **Stop Loss**: 25253.12
- **Risk**: 32.13 points
- **TP 1RR**: 25317.38 ✅
- **TP 1.5RR**: 25333.45 ✅
- **TP 2RR**: 25349.52 ✅
- **TP 2.5RR**: 25365.58 ✅
- **TP 3RR**: 25381.65 ✅
- **TP 3.5RR**: 25397.72 ❌
- **TP 4RR**: 25413.78 ❌
- **TP 4.5RR**: 25429.85 ❌
- **TP 5RR**: 25445.91 ❌
- **PnL**: -32.13 points (-1.0R)
- **MFE**: 102.75 points
- **MAE**: 103.25 points

### Trade #1429 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 08:45:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25340.75 @ 2025-10-10 08:50:00
- **Stop Loss**: 25366.68
- **Risk**: 25.93 points
- **TP 1RR**: 25314.82 ❌
- **TP 1.5RR**: 25301.86 ❌
- **TP 2RR**: 25288.90 ❌
- **TP 2.5RR**: 25275.93 ❌
- **TP 3RR**: 25262.97 ❌
- **TP 3.5RR**: 25250.01 ❌
- **TP 4RR**: 25237.04 ❌
- **TP 4.5RR**: 25224.08 ❌
- **TP 5RR**: 25211.12 ❌
- **PnL**: -25.93 points (-1.0R)
- **MFE**: 15.25 points
- **MAE**: 27.25 points

### Trade #1430 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25323.75 @ 2025-10-10 09:01:00
- **Stop Loss**: 25366.68
- **Risk**: 42.93 points
- **TP 1RR**: 25280.82 ✅
- **TP 1.5RR**: 25259.36 ✅
- **TP 2RR**: 25237.90 ✅
- **TP 2.5RR**: 25216.43 ✅
- **TP 3RR**: 25194.97 ✅
- **TP 3.5RR**: 25173.51 ✅
- **TP 4RR**: 25152.04 ✅
- **TP 4.5RR**: 25130.58 ✅
- **TP 5RR**: 25109.12 ✅
- **PnL**: 214.63 points (5.0R)
- **MFE**: 259.75 points
- **MAE**: 33.00 points

### Trade #1431 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25323.75 @ 2025-10-10 09:01:00
- **Stop Loss**: 25366.68
- **Risk**: 42.93 points
- **TP 1RR**: 25280.82 ✅
- **TP 1.5RR**: 25259.36 ✅
- **TP 2RR**: 25237.90 ✅
- **TP 2.5RR**: 25216.43 ✅
- **TP 3RR**: 25194.97 ✅
- **TP 3.5RR**: 25173.51 ✅
- **TP 4RR**: 25152.04 ✅
- **TP 4.5RR**: 25130.58 ✅
- **TP 5RR**: 25109.12 ✅
- **PnL**: 214.63 points (5.0R)
- **MFE**: 259.75 points
- **MAE**: 33.00 points

### Trade #1432 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25323.75 @ 2025-10-10 09:01:00
- **Stop Loss**: 25366.68
- **Risk**: 42.93 points
- **TP 1RR**: 25280.82 ✅
- **TP 1.5RR**: 25259.36 ✅
- **TP 2RR**: 25237.90 ✅
- **TP 2.5RR**: 25216.43 ✅
- **TP 3RR**: 25194.97 ✅
- **TP 3.5RR**: 25173.51 ✅
- **TP 4RR**: 25152.04 ✅
- **TP 4.5RR**: 25130.58 ✅
- **TP 5RR**: 25109.12 ✅
- **PnL**: 214.63 points (5.0R)
- **MFE**: 259.75 points
- **MAE**: 33.00 points

### Trade #1433 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25323.75 @ 2025-10-10 09:01:00
- **Stop Loss**: 25366.68
- **Risk**: 42.93 points
- **TP 1RR**: 25280.82 ✅
- **TP 1.5RR**: 25259.36 ✅
- **TP 2RR**: 25237.90 ✅
- **TP 2.5RR**: 25216.43 ✅
- **TP 3RR**: 25194.97 ✅
- **TP 3.5RR**: 25173.51 ✅
- **TP 4RR**: 25152.04 ✅
- **TP 4.5RR**: 25130.58 ✅
- **TP 5RR**: 25109.12 ✅
- **PnL**: 214.63 points (5.0R)
- **MFE**: 259.75 points
- **MAE**: 33.00 points

### Trade #1434 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25323.75 @ 2025-10-10 09:01:00
- **Stop Loss**: 25366.68
- **Risk**: 42.93 points
- **TP 1RR**: 25280.82 ✅
- **TP 1.5RR**: 25259.36 ✅
- **TP 2RR**: 25237.90 ✅
- **TP 2.5RR**: 25216.43 ✅
- **TP 3RR**: 25194.97 ✅
- **TP 3.5RR**: 25173.51 ✅
- **TP 4RR**: 25152.04 ✅
- **TP 4.5RR**: 25130.58 ✅
- **TP 5RR**: 25109.12 ✅
- **PnL**: 214.63 points (5.0R)
- **MFE**: 259.75 points
- **MAE**: 33.00 points

### Trade #1435 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25323.75 @ 2025-10-10 09:01:00
- **Stop Loss**: 25366.68
- **Risk**: 42.93 points
- **TP 1RR**: 25280.82 ✅
- **TP 1.5RR**: 25259.36 ✅
- **TP 2RR**: 25237.90 ✅
- **TP 2.5RR**: 25216.43 ✅
- **TP 3RR**: 25194.97 ✅
- **TP 3.5RR**: 25173.51 ✅
- **TP 4RR**: 25152.04 ✅
- **TP 4.5RR**: 25130.58 ✅
- **TP 5RR**: 25109.12 ✅
- **PnL**: 214.63 points (5.0R)
- **MFE**: 259.75 points
- **MAE**: 33.00 points

### Trade #1436 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 09:45:00
- **FVG 5m**: 25305.25 - 25313.25
- **Entrée**: 25338.25 @ 2025-10-10 09:46:00
- **Stop Loss**: 25292.60
- **Risk**: 45.65 points
- **TP 1RR**: 25383.90 ❌
- **TP 1.5RR**: 25406.73 ❌
- **TP 2RR**: 25429.56 ❌
- **TP 2.5RR**: 25452.38 ❌
- **TP 3RR**: 25475.21 ❌
- **TP 3.5RR**: 25498.03 ❌
- **TP 4RR**: 25520.86 ❌
- **TP 4.5RR**: 25543.69 ❌
- **TP 5RR**: 25566.51 ❌
- **PnL**: -45.65 points (-1.0R)
- **MFE**: 18.50 points
- **MAE**: 78.00 points

### Trade #1437 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:00:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25076.25 @ 2025-10-10 10:01:00
- **Stop Loss**: 25366.68
- **Risk**: 290.43 points
- **TP 1RR**: 24785.82 ✅
- **TP 1.5RR**: 24640.61 ✅
- **TP 2RR**: 24495.40 ✅
- **TP 2.5RR**: 24350.18 ✅
- **TP 3RR**: 24204.97 ✅
- **TP 3.5RR**: 24059.76 ❌
- **TP 4RR**: 23914.54 ❌
- **TP 4.5RR**: 23769.33 ❌
- **TP 5RR**: 23624.12 ❌
- **PnL**: -290.43 points (-1.0R)
- **MFE**: 917.75 points
- **MAE**: 291.75 points

### Trade #1438 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:00:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25076.25 @ 2025-10-10 10:01:00
- **Stop Loss**: 25366.68
- **Risk**: 290.43 points
- **TP 1RR**: 24785.82 ✅
- **TP 1.5RR**: 24640.61 ✅
- **TP 2RR**: 24495.40 ✅
- **TP 2.5RR**: 24350.18 ✅
- **TP 3RR**: 24204.97 ✅
- **TP 3.5RR**: 24059.76 ❌
- **TP 4RR**: 23914.54 ❌
- **TP 4.5RR**: 23769.33 ❌
- **TP 5RR**: 23624.12 ❌
- **PnL**: -290.43 points (-1.0R)
- **MFE**: 917.75 points
- **MAE**: 291.75 points

### Trade #1439 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:15:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25016.75 @ 2025-10-10 10:16:00
- **Stop Loss**: 25366.68
- **Risk**: 349.93 points
- **TP 1RR**: 24666.82 ✅
- **TP 1.5RR**: 24491.86 ✅
- **TP 2RR**: 24316.90 ✅
- **TP 2.5RR**: 24141.93 ❌
- **TP 3RR**: 23966.97 ❌
- **TP 3.5RR**: 23792.01 ❌
- **TP 4RR**: 23617.04 ❌
- **TP 4.5RR**: 23442.08 ❌
- **TP 5RR**: 23267.12 ❌
- **PnL**: -349.93 points (-1.0R)
- **MFE**: 858.25 points
- **MAE**: 351.25 points

### Trade #1440 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:15:00
- **FVG 5m**: 25346.75 - 25354.00
- **Entrée**: 25016.75 @ 2025-10-10 10:16:00
- **Stop Loss**: 25366.68
- **Risk**: 349.93 points
- **TP 1RR**: 24666.82 ✅
- **TP 1.5RR**: 24491.86 ✅
- **TP 2RR**: 24316.90 ✅
- **TP 2.5RR**: 24141.93 ❌
- **TP 3RR**: 23966.97 ❌
- **TP 3.5RR**: 23792.01 ❌
- **TP 4RR**: 23617.04 ❌
- **TP 4.5RR**: 23442.08 ❌
- **TP 5RR**: 23267.12 ❌
- **PnL**: -349.93 points (-1.0R)
- **MFE**: 858.25 points
- **MAE**: 351.25 points

### Trade #1441 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 12:15:00
- **FVG 5m**: 24639.25 - 24647.50
- **Entrée**: 24657.50 @ 2025-10-10 12:16:00
- **Stop Loss**: 24626.93
- **Risk**: 30.57 points
- **TP 1RR**: 24688.07 ❌
- **TP 1.5RR**: 24703.35 ❌
- **TP 2RR**: 24718.64 ❌
- **TP 2.5RR**: 24733.92 ❌
- **TP 3RR**: 24749.21 ❌
- **TP 3.5RR**: 24764.49 ❌
- **TP 4RR**: 24779.78 ❌
- **TP 4.5RR**: 24795.06 ❌
- **TP 5RR**: 24810.35 ❌
- **PnL**: -30.57 points (-1.0R)
- **MFE**: 17.00 points
- **MAE**: 36.00 points

### Trade #1442 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 15:00:00
- **FVG 5m**: 24428.50 - 24520.25
- **Entrée**: 24735.50 @ 2025-10-12 17:00:00
- **Stop Loss**: 24416.29
- **Risk**: 319.21 points
- **TP 1RR**: 25054.71 ✅
- **TP 1.5RR**: 25214.32 ❌
- **TP 2RR**: 25373.93 ❌
- **TP 2.5RR**: 25533.54 ❌
- **TP 3RR**: 25693.14 ❌
- **TP 3.5RR**: 25852.75 ❌
- **TP 4RR**: 26012.36 ❌
- **TP 4.5RR**: 26171.96 ❌
- **TP 5RR**: 26331.57 ❌
- **PnL**: -319.21 points (-1.0R)
- **MFE**: 444.00 points
- **MAE**: 320.50 points

### Trade #1443 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 15:45:00
- **FVG 5m**: 24514.25 - 24520.25
- **Entrée**: 24418.00 @ 2025-10-10 15:46:00
- **Stop Loss**: 24532.51
- **Risk**: 114.51 points
- **TP 1RR**: 24303.49 ✅
- **TP 1.5RR**: 24246.23 ✅
- **TP 2RR**: 24188.98 ✅
- **TP 2.5RR**: 24131.72 ❌
- **TP 3RR**: 24074.47 ❌
- **TP 3.5RR**: 24017.21 ❌
- **TP 4RR**: 23959.96 ❌
- **TP 4.5RR**: 23902.70 ❌
- **TP 5RR**: 23845.45 ❌
- **PnL**: -114.51 points (-1.0R)
- **MFE**: 259.50 points
- **MAE**: 329.00 points

### Trade #1444 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 15:45:00
- **FVG 5m**: 24514.25 - 24520.25
- **Entrée**: 24418.00 @ 2025-10-10 15:46:00
- **Stop Loss**: 24532.51
- **Risk**: 114.51 points
- **TP 1RR**: 24303.49 ✅
- **TP 1.5RR**: 24246.23 ✅
- **TP 2RR**: 24188.98 ✅
- **TP 2.5RR**: 24131.72 ❌
- **TP 3RR**: 24074.47 ❌
- **TP 3.5RR**: 24017.21 ❌
- **TP 4RR**: 23959.96 ❌
- **TP 4.5RR**: 23902.70 ❌
- **TP 5RR**: 23845.45 ❌
- **PnL**: -114.51 points (-1.0R)
- **MFE**: 259.50 points
- **MAE**: 329.00 points

### Trade #1445 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-12 17:00:00
- **FVG 5m**: 24246.00 - 24412.75
- **Entrée**: 24727.00 @ 2025-10-12 17:01:00
- **Stop Loss**: 24233.88
- **Risk**: 493.12 points
- **TP 1RR**: 25220.12 ✅
- **TP 1.5RR**: 25466.68 ✅
- **TP 2RR**: 25713.25 ✅
- **TP 2.5RR**: 25959.81 ✅
- **TP 3RR**: 26206.37 ✅
- **TP 3.5RR**: 26452.93 ❌
- **TP 4RR**: 26699.49 ❌
- **TP 4.5RR**: 26946.05 ❌
- **TP 5RR**: 27192.61 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1672.00 points
- **MAE**: 317.00 points

### Trade #1446 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 02:15:00
- **FVG 5m**: 24810.00 - 24816.50
- **Entrée**: 24896.50 @ 2025-10-13 02:16:00
- **Stop Loss**: 24797.60
- **Risk**: 98.90 points
- **TP 1RR**: 24995.40 ❌
- **TP 1.5RR**: 25044.86 ❌
- **TP 2RR**: 25094.31 ❌
- **TP 2.5RR**: 25143.76 ❌
- **TP 3RR**: 25193.21 ❌
- **TP 3.5RR**: 25242.67 ❌
- **TP 4RR**: 25292.12 ❌
- **TP 4.5RR**: 25341.57 ❌
- **TP 5RR**: 25391.02 ❌
- **PnL**: -98.90 points (-1.0R)
- **MFE**: 49.25 points
- **MAE**: 119.50 points

### Trade #1447 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 03:30:00
- **FVG 5m**: 24905.50 - 24916.50
- **Entrée**: 24872.25 @ 2025-10-13 03:31:00
- **Stop Loss**: 24928.96
- **Risk**: 56.71 points
- **TP 1RR**: 24815.54 ✅
- **TP 1.5RR**: 24787.19 ✅
- **TP 2RR**: 24758.83 ✅
- **TP 2.5RR**: 24730.48 ✅
- **TP 3RR**: 24702.13 ❌
- **TP 3.5RR**: 24673.77 ❌
- **TP 4RR**: 24645.42 ❌
- **TP 4.5RR**: 24617.06 ❌
- **TP 5RR**: 24588.71 ❌
- **PnL**: -56.71 points (-1.0R)
- **MFE**: 147.75 points
- **MAE**: 58.00 points

### Trade #1448 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 06:30:00
- **FVG 5m**: 24787.25 - 24802.25
- **Entrée**: 24804.25 @ 2025-10-13 06:54:00
- **Stop Loss**: 24774.86
- **Risk**: 29.39 points
- **TP 1RR**: 24833.64 ❌
- **TP 1.5RR**: 24848.34 ❌
- **TP 2RR**: 24863.04 ❌
- **TP 2.5RR**: 24877.73 ❌
- **TP 3RR**: 24892.43 ❌
- **TP 3.5RR**: 24907.13 ❌
- **TP 4RR**: 24921.82 ❌
- **TP 4.5RR**: 24936.52 ❌
- **TP 5RR**: 24951.22 ❌
- **PnL**: -29.39 points (-1.0R)
- **MFE**: 2.75 points
- **MAE**: 34.75 points

### Trade #1449 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 12:00:00
- **FVG 5m**: 24907.75 - 24917.25
- **Entrée**: 24902.00 @ 2025-10-13 12:18:00
- **Stop Loss**: 24929.71
- **Risk**: 27.71 points
- **TP 1RR**: 24874.29 ❌
- **TP 1.5RR**: 24860.44 ❌
- **TP 2RR**: 24846.58 ❌
- **TP 2.5RR**: 24832.73 ❌
- **TP 3RR**: 24818.87 ❌
- **TP 3.5RR**: 24805.02 ❌
- **TP 4RR**: 24791.17 ❌
- **TP 4.5RR**: 24777.31 ❌
- **TP 5RR**: 24763.46 ❌
- **PnL**: -27.71 points (-1.0R)
- **MFE**: 9.50 points
- **MAE**: 28.25 points

### Trade #1450 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24913.50 - 24919.00
- **Entrée**: 24964.00 @ 2025-10-13 19:16:00
- **Stop Loss**: 24901.04
- **Risk**: 62.96 points
- **TP 1RR**: 25026.96 ✅
- **TP 1.5RR**: 25058.44 ❌
- **TP 2RR**: 25089.91 ❌
- **TP 2.5RR**: 25121.39 ❌
- **TP 3RR**: 25152.87 ❌
- **TP 3.5RR**: 25184.35 ❌
- **TP 4RR**: 25215.83 ❌
- **TP 4.5RR**: 25247.31 ❌
- **TP 5RR**: 25278.78 ❌
- **PnL**: -62.96 points (-1.0R)
- **MFE**: 80.25 points
- **MAE**: 64.00 points

### Trade #1451 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24913.50 - 24919.00
- **Entrée**: 24964.00 @ 2025-10-13 19:16:00
- **Stop Loss**: 24901.04
- **Risk**: 62.96 points
- **TP 1RR**: 25026.96 ✅
- **TP 1.5RR**: 25058.44 ❌
- **TP 2RR**: 25089.91 ❌
- **TP 2.5RR**: 25121.39 ❌
- **TP 3RR**: 25152.87 ❌
- **TP 3.5RR**: 25184.35 ❌
- **TP 4RR**: 25215.83 ❌
- **TP 4.5RR**: 25247.31 ❌
- **TP 5RR**: 25278.78 ❌
- **PnL**: -62.96 points (-1.0R)
- **MFE**: 80.25 points
- **MAE**: 64.00 points

### Trade #1452 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24913.50 - 24919.00
- **Entrée**: 24964.00 @ 2025-10-13 19:16:00
- **Stop Loss**: 24901.04
- **Risk**: 62.96 points
- **TP 1RR**: 25026.96 ✅
- **TP 1.5RR**: 25058.44 ❌
- **TP 2RR**: 25089.91 ❌
- **TP 2.5RR**: 25121.39 ❌
- **TP 3RR**: 25152.87 ❌
- **TP 3.5RR**: 25184.35 ❌
- **TP 4RR**: 25215.83 ❌
- **TP 4.5RR**: 25247.31 ❌
- **TP 5RR**: 25278.78 ❌
- **PnL**: -62.96 points (-1.0R)
- **MFE**: 80.25 points
- **MAE**: 64.00 points

### Trade #1453 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24913.50 - 24919.00
- **Entrée**: 24964.00 @ 2025-10-13 19:16:00
- **Stop Loss**: 24901.04
- **Risk**: 62.96 points
- **TP 1RR**: 25026.96 ✅
- **TP 1.5RR**: 25058.44 ❌
- **TP 2RR**: 25089.91 ❌
- **TP 2.5RR**: 25121.39 ❌
- **TP 3RR**: 25152.87 ❌
- **TP 3.5RR**: 25184.35 ❌
- **TP 4RR**: 25215.83 ❌
- **TP 4.5RR**: 25247.31 ❌
- **TP 5RR**: 25278.78 ❌
- **PnL**: -62.96 points (-1.0R)
- **MFE**: 80.25 points
- **MAE**: 64.00 points

### Trade #1454 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 21:45:00
- **FVG 5m**: 24999.00 - 25017.50
- **Entrée**: 24974.25 @ 2025-10-13 21:46:00
- **Stop Loss**: 25030.01
- **Risk**: 55.76 points
- **TP 1RR**: 24918.49 ✅
- **TP 1.5RR**: 24890.61 ✅
- **TP 2RR**: 24862.73 ✅
- **TP 2.5RR**: 24834.85 ✅
- **TP 3RR**: 24806.97 ✅
- **TP 3.5RR**: 24779.09 ✅
- **TP 4RR**: 24751.21 ✅
- **TP 4.5RR**: 24723.34 ✅
- **TP 5RR**: 24695.46 ✅
- **PnL**: 278.79 points (5.0R)
- **MFE**: 286.25 points
- **MAE**: 2.50 points

### Trade #1455 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 21:45:00
- **FVG 5m**: 24999.00 - 25017.50
- **Entrée**: 24974.25 @ 2025-10-13 21:46:00
- **Stop Loss**: 25030.01
- **Risk**: 55.76 points
- **TP 1RR**: 24918.49 ✅
- **TP 1.5RR**: 24890.61 ✅
- **TP 2RR**: 24862.73 ✅
- **TP 2.5RR**: 24834.85 ✅
- **TP 3RR**: 24806.97 ✅
- **TP 3.5RR**: 24779.09 ✅
- **TP 4RR**: 24751.21 ✅
- **TP 4.5RR**: 24723.34 ✅
- **TP 5RR**: 24695.46 ✅
- **PnL**: 278.79 points (5.0R)
- **MFE**: 286.25 points
- **MAE**: 2.50 points

### Trade #1456 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 06:00:00
- **FVG 5m**: 24533.00 - 24551.25
- **Entrée**: 24564.75 @ 2025-10-14 06:01:00
- **Stop Loss**: 24520.73
- **Risk**: 44.02 points
- **TP 1RR**: 24608.77 ✅
- **TP 1.5RR**: 24630.77 ✅
- **TP 2RR**: 24652.78 ✅
- **TP 2.5RR**: 24674.79 ❌
- **TP 3RR**: 24696.80 ❌
- **TP 3.5RR**: 24718.81 ❌
- **TP 4RR**: 24740.82 ❌
- **TP 4.5RR**: 24762.82 ❌
- **TP 5RR**: 24784.83 ❌
- **PnL**: -44.02 points (-1.0R)
- **MFE**: 100.25 points
- **MAE**: 56.25 points

### Trade #1457 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 08:45:00
- **FVG 5m**: 24519.50 - 24559.50
- **Entrée**: 24564.75 @ 2025-10-14 08:55:00
- **Stop Loss**: 24507.24
- **Risk**: 57.51 points
- **TP 1RR**: 24622.26 ✅
- **TP 1.5RR**: 24651.01 ✅
- **TP 2RR**: 24679.77 ✅
- **TP 2.5RR**: 24708.52 ✅
- **TP 3RR**: 24737.28 ✅
- **TP 3.5RR**: 24766.03 ✅
- **TP 4RR**: 24794.79 ✅
- **TP 4.5RR**: 24823.54 ✅
- **TP 5RR**: 24852.30 ✅
- **PnL**: 287.55 points (5.0R)
- **MFE**: 300.25 points
- **MAE**: 25.00 points

### Trade #1458 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 08:45:00
- **FVG 5m**: 24519.50 - 24559.50
- **Entrée**: 24564.75 @ 2025-10-14 08:55:00
- **Stop Loss**: 24507.24
- **Risk**: 57.51 points
- **TP 1RR**: 24622.26 ✅
- **TP 1.5RR**: 24651.01 ✅
- **TP 2RR**: 24679.77 ✅
- **TP 2.5RR**: 24708.52 ✅
- **TP 3RR**: 24737.28 ✅
- **TP 3.5RR**: 24766.03 ✅
- **TP 4RR**: 24794.79 ✅
- **TP 4.5RR**: 24823.54 ✅
- **TP 5RR**: 24852.30 ✅
- **PnL**: 287.55 points (5.0R)
- **MFE**: 300.25 points
- **MAE**: 25.00 points

### Trade #1459 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 11:30:00
- **FVG 5m**: 24792.50 - 24795.50
- **Entrée**: 24873.50 @ 2025-10-14 11:31:00
- **Stop Loss**: 24780.10
- **Risk**: 93.40 points
- **TP 1RR**: 24966.90 ❌
- **TP 1.5RR**: 25013.59 ❌
- **TP 2RR**: 25060.29 ❌
- **TP 2.5RR**: 25106.99 ❌
- **TP 3RR**: 25153.69 ❌
- **TP 3.5RR**: 25200.39 ❌
- **TP 4RR**: 25247.09 ❌
- **TP 4.5RR**: 25293.78 ❌
- **TP 5RR**: 25340.48 ❌
- **PnL**: -93.40 points (-1.0R)
- **MFE**: 74.00 points
- **MAE**: 99.75 points

### Trade #1460 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 11:30:00
- **FVG 5m**: 24792.50 - 24795.50
- **Entrée**: 24873.50 @ 2025-10-14 11:31:00
- **Stop Loss**: 24780.10
- **Risk**: 93.40 points
- **TP 1RR**: 24966.90 ❌
- **TP 1.5RR**: 25013.59 ❌
- **TP 2RR**: 25060.29 ❌
- **TP 2.5RR**: 25106.99 ❌
- **TP 3RR**: 25153.69 ❌
- **TP 3.5RR**: 25200.39 ❌
- **TP 4RR**: 25247.09 ❌
- **TP 4.5RR**: 25293.78 ❌
- **TP 5RR**: 25340.48 ❌
- **PnL**: -93.40 points (-1.0R)
- **MFE**: 74.00 points
- **MAE**: 99.75 points

### Trade #1461 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-14 22:30:00
- **FVG 5m**: 24835.00 - 24843.00
- **Entrée**: 24825.50 @ 2025-10-14 22:31:00
- **Stop Loss**: 24855.42
- **Risk**: 29.92 points
- **TP 1RR**: 24795.58 ❌
- **TP 1.5RR**: 24780.62 ❌
- **TP 2RR**: 24765.66 ❌
- **TP 2.5RR**: 24750.70 ❌
- **TP 3RR**: 24735.74 ❌
- **TP 3.5RR**: 24720.77 ❌
- **TP 4RR**: 24705.81 ❌
- **TP 4.5RR**: 24690.85 ❌
- **TP 5RR**: 24675.89 ❌
- **PnL**: -29.92 points (-1.0R)
- **MFE**: 29.00 points
- **MAE**: 57.00 points

### Trade #1462 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 06:15:00
- **FVG 5m**: 24964.50 - 24970.75
- **Entrée**: 24951.75 @ 2025-10-15 06:16:00
- **Stop Loss**: 24983.24
- **Risk**: 31.49 points
- **TP 1RR**: 24920.26 ❌
- **TP 1.5RR**: 24904.52 ❌
- **TP 2RR**: 24888.78 ❌
- **TP 2.5RR**: 24873.04 ❌
- **TP 3RR**: 24857.29 ❌
- **TP 3.5RR**: 24841.55 ❌
- **TP 4RR**: 24825.81 ❌
- **TP 4.5RR**: 24810.07 ❌
- **TP 5RR**: 24794.32 ❌
- **PnL**: -31.49 points (-1.0R)
- **MFE**: 14.00 points
- **MAE**: 31.50 points

### Trade #1463 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 08:30:00
- **FVG 5m**: 24951.50 - 24956.75
- **Entrée**: 24967.75 @ 2025-10-15 08:31:00
- **Stop Loss**: 24939.02
- **Risk**: 28.73 points
- **TP 1RR**: 24996.48 ❌
- **TP 1.5RR**: 25010.84 ❌
- **TP 2RR**: 25025.20 ❌
- **TP 2.5RR**: 25039.56 ❌
- **TP 3RR**: 25053.93 ❌
- **TP 3.5RR**: 25068.29 ❌
- **TP 4RR**: 25082.65 ❌
- **TP 4.5RR**: 25097.02 ❌
- **TP 5RR**: 25111.38 ❌
- **PnL**: -28.73 points (-1.0R)
- **MFE**: 26.75 points
- **MAE**: 35.25 points

### Trade #1464 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 10:30:00
- **FVG 5m**: 25043.50 - 25070.25
- **Entrée**: 25034.00 @ 2025-10-15 10:32:00
- **Stop Loss**: 25082.79
- **Risk**: 48.79 points
- **TP 1RR**: 24985.21 ✅
- **TP 1.5RR**: 24960.82 ✅
- **TP 2RR**: 24936.43 ✅
- **TP 2.5RR**: 24912.04 ✅
- **TP 3RR**: 24887.64 ✅
- **TP 3.5RR**: 24863.25 ✅
- **TP 4RR**: 24838.86 ✅
- **TP 4.5RR**: 24814.47 ✅
- **TP 5RR**: 24790.07 ✅
- **PnL**: 243.93 points (5.0R)
- **MFE**: 258.00 points
- **MAE**: 2.50 points

### Trade #1465 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 10:30:00
- **FVG 5m**: 25043.50 - 25070.25
- **Entrée**: 25034.00 @ 2025-10-15 10:32:00
- **Stop Loss**: 25082.79
- **Risk**: 48.79 points
- **TP 1RR**: 24985.21 ✅
- **TP 1.5RR**: 24960.82 ✅
- **TP 2RR**: 24936.43 ✅
- **TP 2.5RR**: 24912.04 ✅
- **TP 3RR**: 24887.64 ✅
- **TP 3.5RR**: 24863.25 ✅
- **TP 4RR**: 24838.86 ✅
- **TP 4.5RR**: 24814.47 ✅
- **TP 5RR**: 24790.07 ✅
- **PnL**: 243.93 points (5.0R)
- **MFE**: 258.00 points
- **MAE**: 2.50 points

### Trade #1466 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 10:30:00
- **FVG 5m**: 25043.50 - 25070.25
- **Entrée**: 25034.00 @ 2025-10-15 10:32:00
- **Stop Loss**: 25082.79
- **Risk**: 48.79 points
- **TP 1RR**: 24985.21 ✅
- **TP 1.5RR**: 24960.82 ✅
- **TP 2RR**: 24936.43 ✅
- **TP 2.5RR**: 24912.04 ✅
- **TP 3RR**: 24887.64 ✅
- **TP 3.5RR**: 24863.25 ✅
- **TP 4RR**: 24838.86 ✅
- **TP 4.5RR**: 24814.47 ✅
- **TP 5RR**: 24790.07 ✅
- **PnL**: 243.93 points (5.0R)
- **MFE**: 258.00 points
- **MAE**: 2.50 points

### Trade #1467 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:15:00
- **FVG 5m**: 24795.25 - 24832.25
- **Entrée**: 24838.00 @ 2025-10-15 12:44:00
- **Stop Loss**: 24782.85
- **Risk**: 55.15 points
- **TP 1RR**: 24893.15 ✅
- **TP 1.5RR**: 24920.72 ✅
- **TP 2RR**: 24948.30 ✅
- **TP 2.5RR**: 24975.87 ✅
- **TP 3RR**: 25003.44 ✅
- **TP 3.5RR**: 25031.02 ✅
- **TP 4RR**: 25058.59 ✅
- **TP 4.5RR**: 25086.16 ✅
- **TP 5RR**: 25113.74 ✅
- **PnL**: 275.74 points (5.0R)
- **MFE**: 285.75 points
- **MAE**: 1.25 points

### Trade #1468 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:15:00
- **FVG 5m**: 24795.25 - 24832.25
- **Entrée**: 24838.00 @ 2025-10-15 12:44:00
- **Stop Loss**: 24782.85
- **Risk**: 55.15 points
- **TP 1RR**: 24893.15 ✅
- **TP 1.5RR**: 24920.72 ✅
- **TP 2RR**: 24948.30 ✅
- **TP 2.5RR**: 24975.87 ✅
- **TP 3RR**: 25003.44 ✅
- **TP 3.5RR**: 25031.02 ✅
- **TP 4RR**: 25058.59 ✅
- **TP 4.5RR**: 25086.16 ✅
- **TP 5RR**: 25113.74 ✅
- **PnL**: 275.74 points (5.0R)
- **MFE**: 285.75 points
- **MAE**: 1.25 points

### Trade #1469 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:30:00
- **FVG 5m**: 24750.75 - 24776.00
- **Entrée**: 24782.75 @ 2025-10-15 12:34:00
- **Stop Loss**: 24738.37
- **Risk**: 44.38 points
- **TP 1RR**: 24827.13 ✅
- **TP 1.5RR**: 24849.31 ✅
- **TP 2RR**: 24871.50 ✅
- **TP 2.5RR**: 24893.69 ✅
- **TP 3RR**: 24915.88 ✅
- **TP 3.5RR**: 24938.06 ✅
- **TP 4RR**: 24960.25 ✅
- **TP 4.5RR**: 24982.44 ✅
- **TP 5RR**: 25004.63 ✅
- **PnL**: 221.88 points (5.0R)
- **MFE**: 222.00 points
- **MAE**: 1.75 points

### Trade #1470 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:45:00
- **FVG 5m**: 24750.75 - 24776.00
- **Entrée**: 24845.00 @ 2025-10-15 12:46:00
- **Stop Loss**: 24738.37
- **Risk**: 106.63 points
- **TP 1RR**: 24951.63 ✅
- **TP 1.5RR**: 25004.94 ✅
- **TP 2RR**: 25058.25 ✅
- **TP 2.5RR**: 25111.56 ✅
- **TP 3RR**: 25164.88 ✅
- **TP 3.5RR**: 25218.19 ❌
- **TP 4RR**: 25271.50 ❌
- **TP 4.5RR**: 25324.81 ❌
- **TP 5RR**: 25378.13 ❌
- **PnL**: -106.63 points (-1.0R)
- **MFE**: 334.50 points
- **MAE**: 113.00 points

### Trade #1471 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 07:00:00
- **FVG 5m**: 25072.00 - 25078.50
- **Entrée**: 25069.50 @ 2025-10-16 07:01:00
- **Stop Loss**: 25091.04
- **Risk**: 21.54 points
- **TP 1RR**: 25047.96 ✅
- **TP 1.5RR**: 25037.19 ✅
- **TP 2RR**: 25026.42 ✅
- **TP 2.5RR**: 25015.65 ❌
- **TP 3RR**: 25004.88 ❌
- **TP 3.5RR**: 24994.11 ❌
- **TP 4RR**: 24983.34 ❌
- **TP 4.5RR**: 24972.57 ❌
- **TP 5RR**: 24961.80 ❌
- **PnL**: -21.54 points (-1.0R)
- **MFE**: 49.50 points
- **MAE**: 25.00 points

### Trade #1472 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 09:45:00
- **FVG 5m**: 25111.75 - 25124.00
- **Entrée**: 25109.25 @ 2025-10-16 09:57:00
- **Stop Loss**: 25136.56
- **Risk**: 27.31 points
- **TP 1RR**: 25081.94 ✅
- **TP 1.5RR**: 25068.28 ✅
- **TP 2RR**: 25054.63 ✅
- **TP 2.5RR**: 25040.97 ✅
- **TP 3RR**: 25027.31 ✅
- **TP 3.5RR**: 25013.66 ✅
- **TP 4RR**: 25000.00 ✅
- **TP 4.5RR**: 24986.35 ✅
- **TP 5RR**: 24972.69 ✅
- **PnL**: 136.56 points (5.0R)
- **MFE**: 140.25 points
- **MAE**: 22.00 points

### Trade #1473 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 10:45:00
- **FVG 5m**: 25111.75 - 25124.00
- **Entrée**: 24969.00 @ 2025-10-16 10:46:00
- **Stop Loss**: 25136.56
- **Risk**: 167.56 points
- **TP 1RR**: 24801.44 ✅
- **TP 1.5RR**: 24717.66 ✅
- **TP 2RR**: 24633.88 ✅
- **TP 2.5RR**: 24550.09 ✅
- **TP 3RR**: 24466.31 ✅
- **TP 3.5RR**: 24382.53 ❌
- **TP 4RR**: 24298.75 ❌
- **TP 4.5RR**: 24214.97 ❌
- **TP 5RR**: 24131.19 ❌
- **PnL**: -167.56 points (-1.0R)
- **MFE**: 559.00 points
- **MAE**: 171.75 points

### Trade #1474 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 11:15:00
- **FVG 5m**: 25111.75 - 25124.00
- **Entrée**: 24960.50 @ 2025-10-16 11:16:00
- **Stop Loss**: 25136.56
- **Risk**: 176.06 points
- **TP 1RR**: 24784.44 ✅
- **TP 1.5RR**: 24696.41 ✅
- **TP 2RR**: 24608.38 ✅
- **TP 2.5RR**: 24520.34 ✅
- **TP 3RR**: 24432.31 ✅
- **TP 3.5RR**: 24344.28 ❌
- **TP 4RR**: 24256.25 ❌
- **TP 4.5RR**: 24168.22 ❌
- **TP 5RR**: 24080.19 ❌
- **PnL**: -176.06 points (-1.0R)
- **MFE**: 550.50 points
- **MAE**: 180.25 points

### Trade #1475 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 11:45:00
- **FVG 5m**: 24827.00 - 24868.50
- **Entrée**: 24886.25 @ 2025-10-16 11:55:00
- **Stop Loss**: 24814.59
- **Risk**: 71.66 points
- **TP 1RR**: 24957.91 ✅
- **TP 1.5RR**: 24993.75 ❌
- **TP 2RR**: 25029.58 ❌
- **TP 2.5RR**: 25065.41 ❌
- **TP 3RR**: 25101.24 ❌
- **TP 3.5RR**: 25137.07 ❌
- **TP 4RR**: 25172.90 ❌
- **TP 4.5RR**: 25208.74 ❌
- **TP 5RR**: 25244.57 ❌
- **PnL**: -71.66 points (-1.0R)
- **MFE**: 80.75 points
- **MAE**: 92.00 points

### Trade #1476 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 11:45:00
- **FVG 5m**: 24827.00 - 24868.50
- **Entrée**: 24886.25 @ 2025-10-16 11:55:00
- **Stop Loss**: 24814.59
- **Risk**: 71.66 points
- **TP 1RR**: 24957.91 ✅
- **TP 1.5RR**: 24993.75 ❌
- **TP 2RR**: 25029.58 ❌
- **TP 2.5RR**: 25065.41 ❌
- **TP 3RR**: 25101.24 ❌
- **TP 3.5RR**: 25137.07 ❌
- **TP 4RR**: 25172.90 ❌
- **TP 4.5RR**: 25208.74 ❌
- **TP 5RR**: 25244.57 ❌
- **PnL**: -71.66 points (-1.0R)
- **MFE**: 80.75 points
- **MAE**: 92.00 points

### Trade #1477 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 11:45:00
- **FVG 5m**: 24827.00 - 24868.50
- **Entrée**: 24886.25 @ 2025-10-16 11:55:00
- **Stop Loss**: 24814.59
- **Risk**: 71.66 points
- **TP 1RR**: 24957.91 ✅
- **TP 1.5RR**: 24993.75 ❌
- **TP 2RR**: 25029.58 ❌
- **TP 2.5RR**: 25065.41 ❌
- **TP 3RR**: 25101.24 ❌
- **TP 3.5RR**: 25137.07 ❌
- **TP 4RR**: 25172.90 ❌
- **TP 4.5RR**: 25208.74 ❌
- **TP 5RR**: 25244.57 ❌
- **PnL**: -71.66 points (-1.0R)
- **MFE**: 80.75 points
- **MAE**: 92.00 points

### Trade #1478 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 13:30:00
- **FVG 5m**: 24726.25 - 24757.00
- **Entrée**: 24762.00 @ 2025-10-16 13:43:00
- **Stop Loss**: 24713.89
- **Risk**: 48.11 points
- **TP 1RR**: 24810.11 ✅
- **TP 1.5RR**: 24834.17 ❌
- **TP 2RR**: 24858.23 ❌
- **TP 2.5RR**: 24882.28 ❌
- **TP 3RR**: 24906.34 ❌
- **TP 3.5RR**: 24930.40 ❌
- **TP 4RR**: 24954.45 ❌
- **TP 4.5RR**: 24978.51 ❌
- **TP 5RR**: 25002.57 ❌
- **PnL**: -48.11 points (-1.0R)
- **MFE**: 58.75 points
- **MAE**: 51.50 points

### Trade #1479 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-17 00:45:00
- **FVG 5m**: 24641.75 - 24648.00
- **Entrée**: 24651.25 @ 2025-10-17 00:53:00
- **Stop Loss**: 24629.43
- **Risk**: 21.82 points
- **TP 1RR**: 24673.07 ✅
- **TP 1.5RR**: 24683.98 ✅
- **TP 2RR**: 24694.89 ❌
- **TP 2.5RR**: 24705.80 ❌
- **TP 3RR**: 24716.71 ❌
- **TP 3.5RR**: 24727.62 ❌
- **TP 4RR**: 24738.53 ❌
- **TP 4.5RR**: 24749.44 ❌
- **TP 5RR**: 24760.35 ❌
- **PnL**: -21.82 points (-1.0R)
- **MFE**: 39.50 points
- **MAE**: 23.25 points

### Trade #1480 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-17 11:30:00
- **FVG 5m**: 24873.50 - 24896.50
- **Entrée**: 24858.25 @ 2025-10-17 12:11:00
- **Stop Loss**: 24908.95
- **Risk**: 50.70 points
- **TP 1RR**: 24807.55 ❌
- **TP 1.5RR**: 24782.20 ❌
- **TP 2RR**: 24756.85 ❌
- **TP 2.5RR**: 24731.50 ❌
- **TP 3RR**: 24706.16 ❌
- **TP 3.5RR**: 24680.81 ❌
- **TP 4RR**: 24655.46 ❌
- **TP 4.5RR**: 24630.11 ❌
- **TP 5RR**: 24604.76 ❌
- **PnL**: -50.70 points (-1.0R)
- **MFE**: 29.25 points
- **MAE**: 52.50 points

### Trade #1481 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-19 19:15:00
- **FVG 5m**: 25007.50 - 25032.25
- **Entrée**: 25032.75 @ 2025-10-19 19:47:00
- **Stop Loss**: 24995.00
- **Risk**: 37.75 points
- **TP 1RR**: 25070.50 ✅
- **TP 1.5RR**: 25089.38 ✅
- **TP 2RR**: 25108.26 ✅
- **TP 2.5RR**: 25127.13 ✅
- **TP 3RR**: 25146.01 ✅
- **TP 3.5RR**: 25164.89 ✅
- **TP 4RR**: 25183.76 ✅
- **TP 4.5RR**: 25202.64 ✅
- **TP 5RR**: 25221.52 ✅
- **PnL**: 188.77 points (5.0R)
- **MFE**: 192.25 points
- **MAE**: 6.00 points

### Trade #1482 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-20 03:45:00
- **FVG 5m**: 25098.50 - 25105.75
- **Entrée**: 25084.25 @ 2025-10-20 03:46:00
- **Stop Loss**: 25118.30
- **Risk**: 34.05 points
- **TP 1RR**: 25050.20 ✅
- **TP 1.5RR**: 25033.17 ❌
- **TP 2RR**: 25016.14 ❌
- **TP 2.5RR**: 24999.12 ❌
- **TP 3RR**: 24982.09 ❌
- **TP 3.5RR**: 24965.06 ❌
- **TP 4RR**: 24948.04 ❌
- **TP 4.5RR**: 24931.01 ❌
- **TP 5RR**: 24913.99 ❌
- **PnL**: -34.05 points (-1.0R)
- **MFE**: 46.25 points
- **MAE**: 37.75 points

### Trade #1483 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-20 06:00:00
- **FVG 5m**: 25060.25 - 25069.75
- **Entrée**: 25070.50 @ 2025-10-20 06:12:00
- **Stop Loss**: 25047.72
- **Risk**: 22.78 points
- **TP 1RR**: 25093.28 ✅
- **TP 1.5RR**: 25104.67 ✅
- **TP 2RR**: 25116.06 ✅
- **TP 2.5RR**: 25127.45 ✅
- **TP 3RR**: 25138.84 ✅
- **TP 3.5RR**: 25150.23 ✅
- **TP 4RR**: 25161.62 ✅
- **TP 4.5RR**: 25173.01 ✅
- **TP 5RR**: 25184.40 ✅
- **PnL**: 113.90 points (5.0R)
- **MFE**: 117.50 points
- **MAE**: 8.75 points

### Trade #1484 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-21 09:45:00
- **FVG 5m**: 25233.25 - 25258.75
- **Entrée**: 25259.50 @ 2025-10-21 09:49:00
- **Stop Loss**: 25220.63
- **Risk**: 38.87 points
- **TP 1RR**: 25298.37 ✅
- **TP 1.5RR**: 25317.80 ✅
- **TP 2RR**: 25337.23 ✅
- **TP 2.5RR**: 25356.67 ❌
- **TP 3RR**: 25376.10 ❌
- **TP 3.5RR**: 25395.53 ❌
- **TP 4RR**: 25414.97 ❌
- **TP 4.5RR**: 25434.40 ❌
- **TP 5RR**: 25453.83 ❌
- **PnL**: -38.87 points (-1.0R)
- **MFE**: 89.00 points
- **MAE**: 45.00 points

### Trade #1485 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-21 10:45:00
- **FVG 5m**: 25275.00 - 25280.50
- **Entrée**: 25297.75 @ 2025-10-21 10:46:00
- **Stop Loss**: 25262.36
- **Risk**: 35.39 points
- **TP 1RR**: 25333.14 ✅
- **TP 1.5RR**: 25350.83 ❌
- **TP 2RR**: 25368.53 ❌
- **TP 2.5RR**: 25386.22 ❌
- **TP 3RR**: 25403.91 ❌
- **TP 3.5RR**: 25421.61 ❌
- **TP 4RR**: 25439.30 ❌
- **TP 4.5RR**: 25456.99 ❌
- **TP 5RR**: 25474.69 ❌
- **PnL**: -35.39 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 39.50 points

### Trade #1486 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-21 11:45:00
- **FVG 5m**: 25292.25 - 25307.50
- **Entrée**: 25289.50 @ 2025-10-21 11:57:00
- **Stop Loss**: 25320.15
- **Risk**: 30.65 points
- **TP 1RR**: 25258.85 ✅
- **TP 1.5RR**: 25243.52 ❌
- **TP 2RR**: 25228.19 ❌
- **TP 2.5RR**: 25212.87 ❌
- **TP 3RR**: 25197.54 ❌
- **TP 3.5RR**: 25182.21 ❌
- **TP 4RR**: 25166.88 ❌
- **TP 4.5RR**: 25151.56 ❌
- **TP 5RR**: 25136.23 ❌
- **PnL**: -30.65 points (-1.0R)
- **MFE**: 39.50 points
- **MAE**: 37.50 points

### Trade #1487 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-21 20:00:00
- **FVG 5m**: 25256.25 - 25262.25
- **Entrée**: 25264.00 @ 2025-10-21 20:56:00
- **Stop Loss**: 25243.62
- **Risk**: 20.38 points
- **TP 1RR**: 25284.38 ✅
- **TP 1.5RR**: 25294.57 ✅
- **TP 2RR**: 25304.76 ✅
- **TP 2.5RR**: 25314.95 ✅
- **TP 3RR**: 25325.13 ✅
- **TP 3.5RR**: 25335.32 ✅
- **TP 4RR**: 25345.51 ❌
- **TP 4.5RR**: 25355.70 ❌
- **TP 5RR**: 25365.89 ❌
- **PnL**: -20.38 points (-1.0R)
- **MFE**: 74.25 points
- **MAE**: 24.25 points

### Trade #1488 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 07:00:00
- **FVG 5m**: 25252.50 - 25260.75
- **Entrée**: 25261.00 @ 2025-10-22 07:21:00
- **Stop Loss**: 25239.87
- **Risk**: 21.13 points
- **TP 1RR**: 25282.13 ❌
- **TP 1.5RR**: 25292.69 ❌
- **TP 2RR**: 25303.25 ❌
- **TP 2.5RR**: 25313.82 ❌
- **TP 3RR**: 25324.38 ❌
- **TP 3.5RR**: 25334.94 ❌
- **TP 4RR**: 25345.51 ❌
- **TP 4.5RR**: 25356.07 ❌
- **TP 5RR**: 25366.63 ❌
- **PnL**: -21.13 points (-1.0R)
- **MFE**: 17.50 points
- **MAE**: 47.50 points

### Trade #1489 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 08:30:00
- **FVG 5m**: 25252.50 - 25260.75
- **Entrée**: 25273.25 @ 2025-10-22 08:51:00
- **Stop Loss**: 25239.87
- **Risk**: 33.38 points
- **TP 1RR**: 25306.63 ❌
- **TP 1.5RR**: 25323.31 ❌
- **TP 2RR**: 25340.00 ❌
- **TP 2.5RR**: 25356.69 ❌
- **TP 3RR**: 25373.38 ❌
- **TP 3.5RR**: 25390.07 ❌
- **TP 4RR**: 25406.76 ❌
- **TP 4.5RR**: 25423.44 ❌
- **TP 5RR**: 25440.13 ❌
- **PnL**: -33.38 points (-1.0R)
- **MFE**: 16.00 points
- **MAE**: 35.25 points

### Trade #1490 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 08:30:00
- **FVG 5m**: 25252.50 - 25260.75
- **Entrée**: 25273.25 @ 2025-10-22 08:51:00
- **Stop Loss**: 25239.87
- **Risk**: 33.38 points
- **TP 1RR**: 25306.63 ❌
- **TP 1.5RR**: 25323.31 ❌
- **TP 2RR**: 25340.00 ❌
- **TP 2.5RR**: 25356.69 ❌
- **TP 3RR**: 25373.38 ❌
- **TP 3.5RR**: 25390.07 ❌
- **TP 4RR**: 25406.76 ❌
- **TP 4.5RR**: 25423.44 ❌
- **TP 5RR**: 25440.13 ❌
- **PnL**: -33.38 points (-1.0R)
- **MFE**: 16.00 points
- **MAE**: 35.25 points

### Trade #1491 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 08:30:00
- **FVG 5m**: 25252.50 - 25260.75
- **Entrée**: 25273.25 @ 2025-10-22 08:51:00
- **Stop Loss**: 25239.87
- **Risk**: 33.38 points
- **TP 1RR**: 25306.63 ❌
- **TP 1.5RR**: 25323.31 ❌
- **TP 2RR**: 25340.00 ❌
- **TP 2.5RR**: 25356.69 ❌
- **TP 3RR**: 25373.38 ❌
- **TP 3.5RR**: 25390.07 ❌
- **TP 4RR**: 25406.76 ❌
- **TP 4.5RR**: 25423.44 ❌
- **TP 5RR**: 25440.13 ❌
- **PnL**: -33.38 points (-1.0R)
- **MFE**: 16.00 points
- **MAE**: 35.25 points

### Trade #1492 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 09:15:00
- **FVG 5m**: 25226.50 - 25236.25
- **Entrée**: 25225.50 @ 2025-10-22 09:16:00
- **Stop Loss**: 25248.87
- **Risk**: 23.37 points
- **TP 1RR**: 25202.13 ✅
- **TP 1.5RR**: 25190.45 ✅
- **TP 2RR**: 25178.76 ✅
- **TP 2.5RR**: 25167.08 ✅
- **TP 3RR**: 25155.40 ✅
- **TP 3.5RR**: 25143.71 ✅
- **TP 4RR**: 25132.03 ✅
- **TP 4.5RR**: 25120.34 ✅
- **TP 5RR**: 25108.66 ✅
- **PnL**: 116.84 points (5.0R)
- **MFE**: 123.25 points
- **MAE**: 19.50 points

### Trade #1493 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 09:15:00
- **FVG 5m**: 25226.50 - 25236.25
- **Entrée**: 25225.50 @ 2025-10-22 09:16:00
- **Stop Loss**: 25248.87
- **Risk**: 23.37 points
- **TP 1RR**: 25202.13 ✅
- **TP 1.5RR**: 25190.45 ✅
- **TP 2RR**: 25178.76 ✅
- **TP 2.5RR**: 25167.08 ✅
- **TP 3RR**: 25155.40 ✅
- **TP 3.5RR**: 25143.71 ✅
- **TP 4RR**: 25132.03 ✅
- **TP 4.5RR**: 25120.34 ✅
- **TP 5RR**: 25108.66 ✅
- **PnL**: 116.84 points (5.0R)
- **MFE**: 123.25 points
- **MAE**: 19.50 points

### Trade #1494 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 09:30:00
- **FVG 5m**: 25226.50 - 25236.25
- **Entrée**: 25102.75 @ 2025-10-22 09:31:00
- **Stop Loss**: 25248.87
- **Risk**: 146.12 points
- **TP 1RR**: 24956.63 ✅
- **TP 1.5RR**: 24883.57 ✅
- **TP 2RR**: 24810.51 ✅
- **TP 2.5RR**: 24737.45 ❌
- **TP 3RR**: 24664.40 ❌
- **TP 3.5RR**: 24591.34 ❌
- **TP 4RR**: 24518.28 ❌
- **TP 4.5RR**: 24445.22 ❌
- **TP 5RR**: 24372.16 ❌
- **PnL**: -146.12 points (-1.0R)
- **MFE**: 298.00 points
- **MAE**: 152.00 points

### Trade #1495 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 10:30:00
- **FVG 5m**: 25071.75 - 25115.50
- **Entrée**: 25121.25 @ 2025-10-22 10:51:00
- **Stop Loss**: 25059.21
- **Risk**: 62.04 points
- **TP 1RR**: 25183.29 ❌
- **TP 1.5RR**: 25214.30 ❌
- **TP 2RR**: 25245.32 ❌
- **TP 2.5RR**: 25276.34 ❌
- **TP 3RR**: 25307.36 ❌
- **TP 3.5RR**: 25338.38 ❌
- **TP 4RR**: 25369.39 ❌
- **TP 4.5RR**: 25400.41 ❌
- **TP 5RR**: 25431.43 ❌
- **PnL**: -62.04 points (-1.0R)
- **MFE**: 10.50 points
- **MAE**: 64.25 points

### Trade #1496 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 10:30:00
- **FVG 5m**: 25071.75 - 25115.50
- **Entrée**: 25121.25 @ 2025-10-22 10:51:00
- **Stop Loss**: 25059.21
- **Risk**: 62.04 points
- **TP 1RR**: 25183.29 ❌
- **TP 1.5RR**: 25214.30 ❌
- **TP 2RR**: 25245.32 ❌
- **TP 2.5RR**: 25276.34 ❌
- **TP 3RR**: 25307.36 ❌
- **TP 3.5RR**: 25338.38 ❌
- **TP 4RR**: 25369.39 ❌
- **TP 4.5RR**: 25400.41 ❌
- **TP 5RR**: 25431.43 ❌
- **PnL**: -62.04 points (-1.0R)
- **MFE**: 10.50 points
- **MAE**: 64.25 points

### Trade #1497 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 12:00:00
- **FVG 5m**: 25074.00 - 25097.25
- **Entrée**: 24981.75 @ 2025-10-22 12:01:00
- **Stop Loss**: 25109.80
- **Risk**: 128.05 points
- **TP 1RR**: 24853.70 ✅
- **TP 1.5RR**: 24789.68 ❌
- **TP 2RR**: 24725.65 ❌
- **TP 2.5RR**: 24661.63 ❌
- **TP 3RR**: 24597.60 ❌
- **TP 3.5RR**: 24533.58 ❌
- **TP 4RR**: 24469.56 ❌
- **TP 4.5RR**: 24405.53 ❌
- **TP 5RR**: 24341.51 ❌
- **PnL**: -128.05 points (-1.0R)
- **MFE**: 177.00 points
- **MAE**: 129.75 points

### Trade #1498 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 12:45:00
- **FVG 5m**: 24863.25 - 24886.25
- **Entrée**: 24895.50 @ 2025-10-22 13:00:00
- **Stop Loss**: 24850.82
- **Risk**: 44.68 points
- **TP 1RR**: 24940.18 ❌
- **TP 1.5RR**: 24962.52 ❌
- **TP 2RR**: 24984.86 ❌
- **TP 2.5RR**: 25007.20 ❌
- **TP 3RR**: 25029.54 ❌
- **TP 3.5RR**: 25051.89 ❌
- **TP 4RR**: 25074.23 ❌
- **TP 4.5RR**: 25096.57 ❌
- **TP 5RR**: 25118.91 ❌
- **PnL**: -44.68 points (-1.0R)
- **MFE**: 15.75 points
- **MAE**: 45.25 points

### Trade #1499 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 19:00:00
- **FVG 5m**: 25012.75 - 25020.75
- **Entrée**: 25025.25 @ 2025-10-22 19:19:00
- **Stop Loss**: 25000.24
- **Risk**: 25.01 points
- **TP 1RR**: 25050.26 ✅
- **TP 1.5RR**: 25062.76 ✅
- **TP 2RR**: 25075.26 ✅
- **TP 2.5RR**: 25087.77 ✅
- **TP 3RR**: 25100.27 ✅
- **TP 3.5RR**: 25112.77 ✅
- **TP 4RR**: 25125.28 ✅
- **TP 4.5RR**: 25137.78 ❌
- **TP 5RR**: 25150.28 ❌
- **PnL**: -25.01 points (-1.0R)
- **MFE**: 102.75 points
- **MAE**: 34.00 points

### Trade #1500 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-23 07:30:00
- **FVG 5m**: 24991.00 - 25005.25
- **Entrée**: 25008.25 @ 2025-10-23 07:59:00
- **Stop Loss**: 24978.50
- **Risk**: 29.75 points
- **TP 1RR**: 25038.00 ❌
- **TP 1.5RR**: 25052.87 ❌
- **TP 2RR**: 25067.74 ❌
- **TP 2.5RR**: 25082.61 ❌
- **TP 3RR**: 25097.49 ❌
- **TP 3.5RR**: 25112.36 ❌
- **TP 4RR**: 25127.23 ❌
- **TP 4.5RR**: 25142.10 ❌
- **TP 5RR**: 25156.98 ❌
- **PnL**: -29.75 points (-1.0R)
- **MFE**: 5.25 points
- **MAE**: 35.00 points

### Trade #1501 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-23 08:30:00
- **FVG 5m**: 24981.25 - 24999.25
- **Entrée**: 25023.00 @ 2025-10-23 08:31:00
- **Stop Loss**: 24968.76
- **Risk**: 54.24 points
- **TP 1RR**: 25077.24 ✅
- **TP 1.5RR**: 25104.36 ✅
- **TP 2RR**: 25131.48 ✅
- **TP 2.5RR**: 25158.60 ✅
- **TP 3RR**: 25185.72 ✅
- **TP 3.5RR**: 25212.84 ✅
- **TP 4RR**: 25239.96 ✅
- **TP 4.5RR**: 25267.08 ✅
- **TP 5RR**: 25294.20 ✅
- **PnL**: 271.20 points (5.0R)
- **MFE**: 273.00 points
- **MAE**: 8.75 points

### Trade #1502 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-23 20:15:00
- **FVG 5m**: 25306.75 - 25310.25
- **Entrée**: 25303.75 @ 2025-10-23 20:29:00
- **Stop Loss**: 25322.91
- **Risk**: 19.16 points
- **TP 1RR**: 25284.59 ❌
- **TP 1.5RR**: 25275.02 ❌
- **TP 2RR**: 25265.44 ❌
- **TP 2.5RR**: 25255.86 ❌
- **TP 3RR**: 25246.28 ❌
- **TP 3.5RR**: 25236.71 ❌
- **TP 4RR**: 25227.13 ❌
- **TP 4.5RR**: 25217.55 ❌
- **TP 5RR**: 25207.97 ❌
- **PnL**: -19.16 points (-1.0R)
- **MFE**: 6.75 points
- **MAE**: 22.50 points

### Trade #1503 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-24 02:45:00
- **FVG 5m**: 25349.00 - 25357.25
- **Entrée**: 25341.25 @ 2025-10-24 02:46:00
- **Stop Loss**: 25369.93
- **Risk**: 28.68 points
- **TP 1RR**: 25312.57 ❌
- **TP 1.5RR**: 25298.23 ❌
- **TP 2RR**: 25283.89 ❌
- **TP 2.5RR**: 25269.55 ❌
- **TP 3RR**: 25255.21 ❌
- **TP 3.5RR**: 25240.87 ❌
- **TP 4RR**: 25226.54 ❌
- **TP 4.5RR**: 25212.20 ❌
- **TP 5RR**: 25197.86 ❌
- **PnL**: -28.68 points (-1.0R)
- **MFE**: 17.25 points
- **MAE**: 30.25 points

### Trade #1504 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-27 08:30:00
- **FVG 5m**: 25829.50 - 25833.75
- **Entrée**: 25846.50 @ 2025-10-27 08:31:00
- **Stop Loss**: 25816.59
- **Risk**: 29.91 points
- **TP 1RR**: 25876.41 ❌
- **TP 1.5RR**: 25891.37 ❌
- **TP 2RR**: 25906.33 ❌
- **TP 2.5RR**: 25921.29 ❌
- **TP 3RR**: 25936.24 ❌
- **TP 3.5RR**: 25951.20 ❌
- **TP 4RR**: 25966.16 ❌
- **TP 4.5RR**: 25981.12 ❌
- **TP 5RR**: 25996.07 ❌
- **PnL**: -29.91 points (-1.0R)
- **MFE**: 5.00 points
- **MAE**: 50.00 points

### Trade #1505 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 04:00:00
- **FVG 5m**: 26282.50 - 26290.25
- **Entrée**: 26263.75 @ 2025-10-29 04:01:00
- **Stop Loss**: 26303.40
- **Risk**: 39.65 points
- **TP 1RR**: 26224.10 ❌
- **TP 1.5RR**: 26204.28 ❌
- **TP 2RR**: 26184.46 ❌
- **TP 2.5RR**: 26164.64 ❌
- **TP 3RR**: 26144.81 ❌
- **TP 3.5RR**: 26124.99 ❌
- **TP 4RR**: 26105.17 ❌
- **TP 4.5RR**: 26085.35 ❌
- **TP 5RR**: 26065.52 ❌
- **PnL**: -39.65 points (-1.0R)
- **MFE**: 37.25 points
- **MAE**: 40.00 points

### Trade #1506 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 09:00:00
- **FVG 5m**: 26254.00 - 26260.00
- **Entrée**: 26252.75 @ 2025-10-29 09:50:00
- **Stop Loss**: 26273.13
- **Risk**: 20.38 points
- **TP 1RR**: 26232.37 ❌
- **TP 1.5RR**: 26222.18 ❌
- **TP 2RR**: 26211.99 ❌
- **TP 2.5RR**: 26201.80 ❌
- **TP 3RR**: 26191.61 ❌
- **TP 3.5RR**: 26181.42 ❌
- **TP 4RR**: 26171.23 ❌
- **TP 4.5RR**: 26161.04 ❌
- **TP 5RR**: 26150.85 ❌
- **PnL**: -20.38 points (-1.0R)
- **MFE**: 1.75 points
- **MAE**: 22.50 points

### Trade #1507 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 09:00:00
- **FVG 5m**: 26254.00 - 26260.00
- **Entrée**: 26252.75 @ 2025-10-29 09:50:00
- **Stop Loss**: 26273.13
- **Risk**: 20.38 points
- **TP 1RR**: 26232.37 ❌
- **TP 1.5RR**: 26222.18 ❌
- **TP 2RR**: 26211.99 ❌
- **TP 2.5RR**: 26201.80 ❌
- **TP 3RR**: 26191.61 ❌
- **TP 3.5RR**: 26181.42 ❌
- **TP 4RR**: 26171.23 ❌
- **TP 4.5RR**: 26161.04 ❌
- **TP 5RR**: 26150.85 ❌
- **PnL**: -20.38 points (-1.0R)
- **MFE**: 1.75 points
- **MAE**: 22.50 points

### Trade #1508 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 11:00:00
- **FVG 5m**: 26248.75 - 26253.25
- **Entrée**: 26253.50 @ 2025-10-29 11:30:00
- **Stop Loss**: 26235.63
- **Risk**: 17.87 points
- **TP 1RR**: 26271.37 ❌
- **TP 1.5RR**: 26280.31 ❌
- **TP 2RR**: 26289.25 ❌
- **TP 2.5RR**: 26298.19 ❌
- **TP 3RR**: 26307.12 ❌
- **TP 3.5RR**: 26316.06 ❌
- **TP 4RR**: 26325.00 ❌
- **TP 4.5RR**: 26333.93 ❌
- **TP 5RR**: 26342.87 ❌
- **PnL**: -17.87 points (-1.0R)
- **MFE**: 14.75 points
- **MAE**: 27.75 points

### Trade #1509 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 11:15:00
- **FVG 5m**: 26248.75 - 26253.25
- **Entrée**: 26253.50 @ 2025-10-29 11:30:00
- **Stop Loss**: 26235.63
- **Risk**: 17.87 points
- **TP 1RR**: 26271.37 ❌
- **TP 1.5RR**: 26280.31 ❌
- **TP 2RR**: 26289.25 ❌
- **TP 2.5RR**: 26298.19 ❌
- **TP 3RR**: 26307.12 ❌
- **TP 3.5RR**: 26316.06 ❌
- **TP 4RR**: 26325.00 ❌
- **TP 4.5RR**: 26333.93 ❌
- **TP 5RR**: 26342.87 ❌
- **PnL**: -17.87 points (-1.0R)
- **MFE**: 14.75 points
- **MAE**: 27.75 points

### Trade #1510 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 12:15:00
- **FVG 5m**: 26232.25 - 26242.75
- **Entrée**: 26227.50 @ 2025-10-29 12:25:00
- **Stop Loss**: 26255.87
- **Risk**: 28.37 points
- **TP 1RR**: 26199.13 ❌
- **TP 1.5RR**: 26184.94 ❌
- **TP 2RR**: 26170.76 ❌
- **TP 2.5RR**: 26156.57 ❌
- **TP 3RR**: 26142.39 ❌
- **TP 3.5RR**: 26128.20 ❌
- **TP 4RR**: 26114.01 ❌
- **TP 4.5RR**: 26099.83 ❌
- **TP 5RR**: 26085.64 ❌
- **PnL**: -28.37 points (-1.0R)
- **MFE**: 8.50 points
- **MAE**: 28.75 points

### Trade #1511 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 13:15:00
- **FVG 5m**: 26234.50 - 26238.25
- **Entrée**: 26240.00 @ 2025-10-29 13:17:00
- **Stop Loss**: 26221.38
- **Risk**: 18.62 points
- **TP 1RR**: 26258.62 ❌
- **TP 1.5RR**: 26267.93 ❌
- **TP 2RR**: 26277.23 ❌
- **TP 2.5RR**: 26286.54 ❌
- **TP 3RR**: 26295.85 ❌
- **TP 3.5RR**: 26305.16 ❌
- **TP 4RR**: 26314.47 ❌
- **TP 4.5RR**: 26323.78 ❌
- **TP 5RR**: 26333.09 ❌
- **PnL**: -18.62 points (-1.0R)
- **MFE**: 17.00 points
- **MAE**: 19.50 points

### Trade #1512 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 13:30:00
- **FVG 5m**: 26234.50 - 26239.00
- **Entrée**: 26152.75 @ 2025-10-29 13:35:00
- **Stop Loss**: 26252.12
- **Risk**: 99.37 points
- **TP 1RR**: 26053.38 ✅
- **TP 1.5RR**: 26003.70 ❌
- **TP 2RR**: 25954.01 ❌
- **TP 2.5RR**: 25904.33 ❌
- **TP 3RR**: 25854.64 ❌
- **TP 3.5RR**: 25804.96 ❌
- **TP 4RR**: 25755.27 ❌
- **TP 4.5RR**: 25705.59 ❌
- **TP 5RR**: 25655.90 ❌
- **PnL**: -99.37 points (-1.0R)
- **MFE**: 103.50 points
- **MAE**: 134.25 points

### Trade #1513 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 13:30:00
- **FVG 5m**: 26234.50 - 26239.00
- **Entrée**: 26152.75 @ 2025-10-29 13:35:00
- **Stop Loss**: 26252.12
- **Risk**: 99.37 points
- **TP 1RR**: 26053.38 ✅
- **TP 1.5RR**: 26003.70 ❌
- **TP 2RR**: 25954.01 ❌
- **TP 2.5RR**: 25904.33 ❌
- **TP 3RR**: 25854.64 ❌
- **TP 3.5RR**: 25804.96 ❌
- **TP 4RR**: 25755.27 ❌
- **TP 4.5RR**: 25705.59 ❌
- **TP 5RR**: 25655.90 ❌
- **PnL**: -99.37 points (-1.0R)
- **MFE**: 103.50 points
- **MAE**: 134.25 points

### Trade #1514 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 15:00:00
- **FVG 5m**: 26238.25 - 26241.50
- **Entrée**: 26213.00 @ 2025-10-29 15:06:00
- **Stop Loss**: 26254.62
- **Risk**: 41.62 points
- **TP 1RR**: 26171.38 ✅
- **TP 1.5RR**: 26150.57 ❌
- **TP 2RR**: 26129.76 ❌
- **TP 2.5RR**: 26108.95 ❌
- **TP 3RR**: 26088.14 ❌
- **TP 3.5RR**: 26067.33 ❌
- **TP 4RR**: 26046.52 ❌
- **TP 4.5RR**: 26025.71 ❌
- **TP 5RR**: 26004.90 ❌
- **PnL**: -41.62 points (-1.0R)
- **MFE**: 53.25 points
- **MAE**: 53.25 points

### Trade #1515 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 15:00:00
- **FVG 5m**: 26238.25 - 26241.50
- **Entrée**: 26213.00 @ 2025-10-29 15:06:00
- **Stop Loss**: 26254.62
- **Risk**: 41.62 points
- **TP 1RR**: 26171.38 ✅
- **TP 1.5RR**: 26150.57 ❌
- **TP 2RR**: 26129.76 ❌
- **TP 2.5RR**: 26108.95 ❌
- **TP 3RR**: 26088.14 ❌
- **TP 3.5RR**: 26067.33 ❌
- **TP 4RR**: 26046.52 ❌
- **TP 4.5RR**: 26025.71 ❌
- **TP 5RR**: 26004.90 ❌
- **PnL**: -41.62 points (-1.0R)
- **MFE**: 53.25 points
- **MAE**: 53.25 points

### Trade #1516 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 15:00:00
- **FVG 5m**: 26136.75 - 26235.75
- **Entrée**: 26319.00 @ 2025-10-29 15:01:00
- **Stop Loss**: 26123.68
- **Risk**: 195.32 points
- **TP 1RR**: 26514.32 ❌
- **TP 1.5RR**: 26611.98 ❌
- **TP 2RR**: 26709.64 ❌
- **TP 2.5RR**: 26807.30 ❌
- **TP 3RR**: 26904.96 ❌
- **TP 3.5RR**: 27002.61 ❌
- **TP 4RR**: 27100.27 ❌
- **TP 4.5RR**: 27197.93 ❌
- **TP 5RR**: 27295.59 ❌
- **PnL**: -195.32 points (-1.0R)
- **MFE**: 80.00 points
- **MAE**: 206.50 points

### Trade #1517 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 22:15:00
- **FVG 5m**: 26357.00 - 26364.25
- **Entrée**: 26356.00 @ 2025-10-29 23:04:00
- **Stop Loss**: 26377.43
- **Risk**: 21.43 points
- **TP 1RR**: 26334.57 ✅
- **TP 1.5RR**: 26323.85 ✅
- **TP 2RR**: 26313.14 ✅
- **TP 2.5RR**: 26302.42 ✅
- **TP 3RR**: 26291.70 ✅
- **TP 3.5RR**: 26280.99 ✅
- **TP 4RR**: 26270.27 ✅
- **TP 4.5RR**: 26259.56 ✅
- **TP 5RR**: 26248.84 ✅
- **PnL**: 107.16 points (5.0R)
- **MFE**: 119.75 points
- **MAE**: 0.00 points

### Trade #1518 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 23:00:00
- **FVG 5m**: 26357.00 - 26364.25
- **Entrée**: 26356.00 @ 2025-10-29 23:04:00
- **Stop Loss**: 26377.43
- **Risk**: 21.43 points
- **TP 1RR**: 26334.57 ✅
- **TP 1.5RR**: 26323.85 ✅
- **TP 2RR**: 26313.14 ✅
- **TP 2.5RR**: 26302.42 ✅
- **TP 3RR**: 26291.70 ✅
- **TP 3.5RR**: 26280.99 ✅
- **TP 4RR**: 26270.27 ✅
- **TP 4.5RR**: 26259.56 ✅
- **TP 5RR**: 26248.84 ✅
- **PnL**: 107.16 points (5.0R)
- **MFE**: 119.75 points
- **MAE**: 0.00 points

### Trade #1519 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26251.00 - 26258.25
- **Entrée**: 26092.50 @ 2025-10-30 08:31:00
- **Stop Loss**: 26271.38
- **Risk**: 178.88 points
- **TP 1RR**: 25913.62 ✅
- **TP 1.5RR**: 25824.18 ❌
- **TP 2RR**: 25734.74 ❌
- **TP 2.5RR**: 25645.30 ❌
- **TP 3RR**: 25555.86 ❌
- **TP 3.5RR**: 25466.42 ❌
- **TP 4RR**: 25376.98 ❌
- **TP 4.5RR**: 25287.54 ❌
- **TP 5RR**: 25198.10 ❌
- **PnL**: -178.88 points (-1.0R)
- **MFE**: 239.50 points
- **MAE**: 181.50 points

### Trade #1520 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26251.00 - 26258.25
- **Entrée**: 26092.50 @ 2025-10-30 08:31:00
- **Stop Loss**: 26271.38
- **Risk**: 178.88 points
- **TP 1RR**: 25913.62 ✅
- **TP 1.5RR**: 25824.18 ❌
- **TP 2RR**: 25734.74 ❌
- **TP 2.5RR**: 25645.30 ❌
- **TP 3RR**: 25555.86 ❌
- **TP 3.5RR**: 25466.42 ❌
- **TP 4RR**: 25376.98 ❌
- **TP 4.5RR**: 25287.54 ❌
- **TP 5RR**: 25198.10 ❌
- **PnL**: -178.88 points (-1.0R)
- **MFE**: 239.50 points
- **MAE**: 181.50 points

### Trade #1521 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26251.00 - 26258.25
- **Entrée**: 26092.50 @ 2025-10-30 08:31:00
- **Stop Loss**: 26271.38
- **Risk**: 178.88 points
- **TP 1RR**: 25913.62 ✅
- **TP 1.5RR**: 25824.18 ❌
- **TP 2RR**: 25734.74 ❌
- **TP 2.5RR**: 25645.30 ❌
- **TP 3RR**: 25555.86 ❌
- **TP 3.5RR**: 25466.42 ❌
- **TP 4RR**: 25376.98 ❌
- **TP 4.5RR**: 25287.54 ❌
- **TP 5RR**: 25198.10 ❌
- **PnL**: -178.88 points (-1.0R)
- **MFE**: 239.50 points
- **MAE**: 181.50 points

### Trade #1522 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26251.00 - 26258.25
- **Entrée**: 26092.50 @ 2025-10-30 08:31:00
- **Stop Loss**: 26271.38
- **Risk**: 178.88 points
- **TP 1RR**: 25913.62 ✅
- **TP 1.5RR**: 25824.18 ❌
- **TP 2RR**: 25734.74 ❌
- **TP 2.5RR**: 25645.30 ❌
- **TP 3RR**: 25555.86 ❌
- **TP 3.5RR**: 25466.42 ❌
- **TP 4RR**: 25376.98 ❌
- **TP 4.5RR**: 25287.54 ❌
- **TP 5RR**: 25198.10 ❌
- **PnL**: -178.88 points (-1.0R)
- **MFE**: 239.50 points
- **MAE**: 181.50 points

### Trade #1523 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26137.50 - 26143.75
- **Entrée**: 26154.25 @ 2025-10-30 09:00:00
- **Stop Loss**: 26124.43
- **Risk**: 29.82 points
- **TP 1RR**: 26184.07 ❌
- **TP 1.5RR**: 26198.98 ❌
- **TP 2RR**: 26213.89 ❌
- **TP 2.5RR**: 26228.80 ❌
- **TP 3RR**: 26243.71 ❌
- **TP 3.5RR**: 26258.62 ❌
- **TP 4RR**: 26273.52 ❌
- **TP 4.5RR**: 26288.43 ❌
- **TP 5RR**: 26303.34 ❌
- **PnL**: -29.82 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 35.50 points

### Trade #1524 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26137.50 - 26143.75
- **Entrée**: 26154.25 @ 2025-10-30 09:00:00
- **Stop Loss**: 26124.43
- **Risk**: 29.82 points
- **TP 1RR**: 26184.07 ❌
- **TP 1.5RR**: 26198.98 ❌
- **TP 2RR**: 26213.89 ❌
- **TP 2.5RR**: 26228.80 ❌
- **TP 3RR**: 26243.71 ❌
- **TP 3.5RR**: 26258.62 ❌
- **TP 4RR**: 26273.52 ❌
- **TP 4.5RR**: 26288.43 ❌
- **TP 5RR**: 26303.34 ❌
- **PnL**: -29.82 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 35.50 points

### Trade #1525 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:45:00
- **FVG 5m**: 25996.00 - 26043.00
- **Entrée**: 26056.00 @ 2025-10-30 08:48:00
- **Stop Loss**: 25983.00
- **Risk**: 73.00 points
- **TP 1RR**: 26129.00 ✅
- **TP 1.5RR**: 26165.50 ✅
- **TP 2RR**: 26202.00 ❌
- **TP 2.5RR**: 26238.49 ❌
- **TP 3RR**: 26274.99 ❌
- **TP 3.5RR**: 26311.49 ❌
- **TP 4RR**: 26347.99 ❌
- **TP 4.5RR**: 26384.49 ❌
- **TP 5RR**: 26420.99 ❌
- **PnL**: -73.00 points (-1.0R)
- **MFE**: 126.50 points
- **MAE**: 77.00 points

### Trade #1526 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:45:00
- **FVG 5m**: 25996.00 - 26043.00
- **Entrée**: 26056.00 @ 2025-10-30 08:48:00
- **Stop Loss**: 25983.00
- **Risk**: 73.00 points
- **TP 1RR**: 26129.00 ✅
- **TP 1.5RR**: 26165.50 ✅
- **TP 2RR**: 26202.00 ❌
- **TP 2.5RR**: 26238.49 ❌
- **TP 3RR**: 26274.99 ❌
- **TP 3.5RR**: 26311.49 ❌
- **TP 4RR**: 26347.99 ❌
- **TP 4.5RR**: 26384.49 ❌
- **TP 5RR**: 26420.99 ❌
- **PnL**: -73.00 points (-1.0R)
- **MFE**: 126.50 points
- **MAE**: 77.00 points

### Trade #1527 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:00:00
- **FVG 5m**: 25940.00 - 25948.00
- **Entrée**: 25978.75 @ 2025-10-30 15:01:00
- **Stop Loss**: 25927.03
- **Risk**: 51.72 points
- **TP 1RR**: 26030.47 ✅
- **TP 1.5RR**: 26056.33 ❌
- **TP 2RR**: 26082.19 ❌
- **TP 2.5RR**: 26108.05 ❌
- **TP 3RR**: 26133.91 ❌
- **TP 3.5RR**: 26159.77 ❌
- **TP 4RR**: 26185.63 ❌
- **TP 4.5RR**: 26211.49 ❌
- **TP 5RR**: 26237.35 ❌
- **PnL**: -51.72 points (-1.0R)
- **MFE**: 61.25 points
- **MAE**: 58.75 points

### Trade #1528 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:00:00
- **FVG 5m**: 25940.00 - 25948.00
- **Entrée**: 25978.75 @ 2025-10-30 15:01:00
- **Stop Loss**: 25927.03
- **Risk**: 51.72 points
- **TP 1RR**: 26030.47 ✅
- **TP 1.5RR**: 26056.33 ❌
- **TP 2RR**: 26082.19 ❌
- **TP 2.5RR**: 26108.05 ❌
- **TP 3RR**: 26133.91 ❌
- **TP 3.5RR**: 26159.77 ❌
- **TP 4RR**: 26185.63 ❌
- **TP 4.5RR**: 26211.49 ❌
- **TP 5RR**: 26237.35 ❌
- **PnL**: -51.72 points (-1.0R)
- **MFE**: 61.25 points
- **MAE**: 58.75 points

### Trade #1529 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:00:00
- **FVG 5m**: 25940.00 - 25948.00
- **Entrée**: 25978.75 @ 2025-10-30 15:01:00
- **Stop Loss**: 25927.03
- **Risk**: 51.72 points
- **TP 1RR**: 26030.47 ✅
- **TP 1.5RR**: 26056.33 ❌
- **TP 2RR**: 26082.19 ❌
- **TP 2.5RR**: 26108.05 ❌
- **TP 3RR**: 26133.91 ❌
- **TP 3.5RR**: 26159.77 ❌
- **TP 4RR**: 26185.63 ❌
- **TP 4.5RR**: 26211.49 ❌
- **TP 5RR**: 26237.35 ❌
- **PnL**: -51.72 points (-1.0R)
- **MFE**: 61.25 points
- **MAE**: 58.75 points

### Trade #1530 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:45:00
- **FVG 5m**: 25940.00 - 25948.00
- **Entrée**: 26142.25 @ 2025-10-30 15:46:00
- **Stop Loss**: 25927.03
- **Risk**: 215.22 points
- **TP 1RR**: 26357.47 ❌
- **TP 1.5RR**: 26465.08 ❌
- **TP 2RR**: 26572.69 ❌
- **TP 2.5RR**: 26680.30 ❌
- **TP 3RR**: 26787.91 ❌
- **TP 3.5RR**: 26895.52 ❌
- **TP 4RR**: 27003.13 ❌
- **TP 4.5RR**: 27110.74 ❌
- **TP 5RR**: 27218.35 ❌
- **PnL**: -215.22 points (-1.0R)
- **MFE**: 131.75 points
- **MAE**: 227.50 points

### Trade #1531 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 18:30:00
- **FVG 5m**: 26137.25 - 26142.00
- **Entrée**: 26147.50 @ 2025-10-30 18:39:00
- **Stop Loss**: 26124.18
- **Risk**: 23.32 points
- **TP 1RR**: 26170.82 ✅
- **TP 1.5RR**: 26182.48 ✅
- **TP 2RR**: 26194.14 ✅
- **TP 2.5RR**: 26205.80 ✅
- **TP 3RR**: 26217.46 ✅
- **TP 3.5RR**: 26229.12 ✅
- **TP 4RR**: 26240.77 ✅
- **TP 4.5RR**: 26252.43 ✅
- **TP 5RR**: 26264.09 ✅
- **PnL**: 116.59 points (5.0R)
- **MFE**: 116.75 points
- **MAE**: 11.00 points

### Trade #1532 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 19:15:00
- **FVG 5m**: 26149.25 - 26160.00
- **Entrée**: 26161.00 @ 2025-10-30 19:17:00
- **Stop Loss**: 26136.18
- **Risk**: 24.82 points
- **TP 1RR**: 26185.82 ✅
- **TP 1.5RR**: 26198.24 ✅
- **TP 2RR**: 26210.65 ✅
- **TP 2.5RR**: 26223.06 ✅
- **TP 3RR**: 26235.47 ✅
- **TP 3.5RR**: 26247.89 ✅
- **TP 4RR**: 26260.30 ✅
- **TP 4.5RR**: 26272.71 ✅
- **TP 5RR**: 26285.12 ❌
- **PnL**: -24.82 points (-1.0R)
- **MFE**: 113.00 points
- **MAE**: 27.75 points

### Trade #1533 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 02:30:00
- **FVG 5m**: 26178.25 - 26187.00
- **Entrée**: 26187.50 @ 2025-10-31 02:36:00
- **Stop Loss**: 26165.16
- **Risk**: 22.34 points
- **TP 1RR**: 26209.84 ✅
- **TP 1.5RR**: 26221.01 ❌
- **TP 2RR**: 26232.18 ❌
- **TP 2.5RR**: 26243.35 ❌
- **TP 3RR**: 26254.52 ❌
- **TP 3.5RR**: 26265.69 ❌
- **TP 4RR**: 26276.86 ❌
- **TP 4.5RR**: 26288.03 ❌
- **TP 5RR**: 26299.20 ❌
- **PnL**: -22.34 points (-1.0R)
- **MFE**: 32.25 points
- **MAE**: 28.25 points

### Trade #1534 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 03:00:00
- **FVG 5m**: 26198.50 - 26201.75
- **Entrée**: 26198.25 @ 2025-10-31 03:05:00
- **Stop Loss**: 26214.85
- **Risk**: 16.60 points
- **TP 1RR**: 26181.65 ✅
- **TP 1.5RR**: 26173.35 ✅
- **TP 2RR**: 26165.05 ✅
- **TP 2.5RR**: 26156.75 ❌
- **TP 3RR**: 26148.45 ❌
- **TP 3.5RR**: 26140.15 ❌
- **TP 4RR**: 26131.85 ❌
- **TP 4.5RR**: 26123.55 ❌
- **TP 5RR**: 26115.25 ❌
- **PnL**: -16.60 points (-1.0R)
- **MFE**: 40.75 points
- **MAE**: 28.25 points

### Trade #1535 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 03:00:00
- **FVG 5m**: 26198.50 - 26201.75
- **Entrée**: 26198.25 @ 2025-10-31 03:05:00
- **Stop Loss**: 26214.85
- **Risk**: 16.60 points
- **TP 1RR**: 26181.65 ✅
- **TP 1.5RR**: 26173.35 ✅
- **TP 2RR**: 26165.05 ✅
- **TP 2.5RR**: 26156.75 ❌
- **TP 3RR**: 26148.45 ❌
- **TP 3.5RR**: 26140.15 ❌
- **TP 4RR**: 26131.85 ❌
- **TP 4.5RR**: 26123.55 ❌
- **TP 5RR**: 26115.25 ❌
- **PnL**: -16.60 points (-1.0R)
- **MFE**: 40.75 points
- **MAE**: 28.25 points

### Trade #1536 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 07:45:00
- **FVG 5m**: 26242.25 - 26256.25
- **Entrée**: 26220.75 @ 2025-10-31 07:46:00
- **Stop Loss**: 26269.38
- **Risk**: 48.63 points
- **TP 1RR**: 26172.12 ✅
- **TP 1.5RR**: 26147.81 ✅
- **TP 2RR**: 26123.49 ✅
- **TP 2.5RR**: 26099.18 ✅
- **TP 3RR**: 26074.87 ✅
- **TP 3.5RR**: 26050.55 ✅
- **TP 4RR**: 26026.24 ✅
- **TP 4.5RR**: 26001.92 ✅
- **TP 5RR**: 25977.61 ✅
- **PnL**: 243.14 points (5.0R)
- **MFE**: 246.00 points
- **MAE**: 10.00 points

### Trade #1537 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 09:00:00
- **FVG 5m**: 26242.25 - 26256.25
- **Entrée**: 26091.25 @ 2025-10-31 09:01:00
- **Stop Loss**: 26269.38
- **Risk**: 178.13 points
- **TP 1RR**: 25913.12 ✅
- **TP 1.5RR**: 25824.06 ✅
- **TP 2RR**: 25734.99 ✅
- **TP 2.5RR**: 25645.93 ✅
- **TP 3RR**: 25556.87 ✅
- **TP 3.5RR**: 25467.80 ✅
- **TP 4RR**: 25378.74 ✅
- **TP 4.5RR**: 25289.67 ✅
- **TP 5RR**: 25200.61 ✅
- **PnL**: 890.64 points (5.0R)
- **MFE**: 893.50 points
- **MAE**: 174.75 points

### Trade #1538 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26133.50 - 26140.25
- **Entrée**: 26145.25 @ 2025-10-31 09:37:00
- **Stop Loss**: 26120.43
- **Risk**: 24.82 points
- **TP 1RR**: 26170.07 ✅
- **TP 1.5RR**: 26182.48 ✅
- **TP 2RR**: 26194.88 ❌
- **TP 2.5RR**: 26207.29 ❌
- **TP 3RR**: 26219.70 ❌
- **TP 3.5RR**: 26232.11 ❌
- **TP 4RR**: 26244.52 ❌
- **TP 4.5RR**: 26256.93 ❌
- **TP 5RR**: 26269.33 ❌
- **PnL**: -24.82 points (-1.0R)
- **MFE**: 37.50 points
- **MAE**: 45.50 points

### Trade #1539 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26133.50 - 26140.25
- **Entrée**: 26145.25 @ 2025-10-31 09:37:00
- **Stop Loss**: 26120.43
- **Risk**: 24.82 points
- **TP 1RR**: 26170.07 ✅
- **TP 1.5RR**: 26182.48 ✅
- **TP 2RR**: 26194.88 ❌
- **TP 2.5RR**: 26207.29 ❌
- **TP 3RR**: 26219.70 ❌
- **TP 3.5RR**: 26232.11 ❌
- **TP 4RR**: 26244.52 ❌
- **TP 4.5RR**: 26256.93 ❌
- **TP 5RR**: 26269.33 ❌
- **PnL**: -24.82 points (-1.0R)
- **MFE**: 37.50 points
- **MAE**: 45.50 points

### Trade #1540 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26133.50 - 26140.25
- **Entrée**: 26145.25 @ 2025-10-31 09:37:00
- **Stop Loss**: 26120.43
- **Risk**: 24.82 points
- **TP 1RR**: 26170.07 ✅
- **TP 1.5RR**: 26182.48 ✅
- **TP 2RR**: 26194.88 ❌
- **TP 2.5RR**: 26207.29 ❌
- **TP 3RR**: 26219.70 ❌
- **TP 3.5RR**: 26232.11 ❌
- **TP 4RR**: 26244.52 ❌
- **TP 4.5RR**: 26256.93 ❌
- **TP 5RR**: 26269.33 ❌
- **PnL**: -24.82 points (-1.0R)
- **MFE**: 37.50 points
- **MAE**: 45.50 points

### Trade #1541 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26133.50 - 26140.25
- **Entrée**: 26145.25 @ 2025-10-31 09:37:00
- **Stop Loss**: 26120.43
- **Risk**: 24.82 points
- **TP 1RR**: 26170.07 ✅
- **TP 1.5RR**: 26182.48 ✅
- **TP 2RR**: 26194.88 ❌
- **TP 2.5RR**: 26207.29 ❌
- **TP 3RR**: 26219.70 ❌
- **TP 3.5RR**: 26232.11 ❌
- **TP 4RR**: 26244.52 ❌
- **TP 4.5RR**: 26256.93 ❌
- **TP 5RR**: 26269.33 ❌
- **PnL**: -24.82 points (-1.0R)
- **MFE**: 37.50 points
- **MAE**: 45.50 points

### Trade #1542 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26133.50 - 26140.25
- **Entrée**: 26145.25 @ 2025-10-31 09:37:00
- **Stop Loss**: 26120.43
- **Risk**: 24.82 points
- **TP 1RR**: 26170.07 ✅
- **TP 1.5RR**: 26182.48 ✅
- **TP 2RR**: 26194.88 ❌
- **TP 2.5RR**: 26207.29 ❌
- **TP 3RR**: 26219.70 ❌
- **TP 3.5RR**: 26232.11 ❌
- **TP 4RR**: 26244.52 ❌
- **TP 4.5RR**: 26256.93 ❌
- **TP 5RR**: 26269.33 ❌
- **PnL**: -24.82 points (-1.0R)
- **MFE**: 37.50 points
- **MAE**: 45.50 points

### Trade #1543 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-03 02:00:00
- **FVG 5m**: 26035.25 - 26046.00
- **Entrée**: 26049.25 @ 2025-11-03 02:11:00
- **Stop Loss**: 26022.23
- **Risk**: 27.02 points
- **TP 1RR**: 26076.27 ✅
- **TP 1.5RR**: 26089.78 ✅
- **TP 2RR**: 26103.29 ✅
- **TP 2.5RR**: 26116.79 ✅
- **TP 3RR**: 26130.30 ✅
- **TP 3.5RR**: 26143.81 ✅
- **TP 4RR**: 26157.32 ✅
- **TP 4.5RR**: 26170.83 ✅
- **TP 5RR**: 26184.34 ✅
- **PnL**: 135.09 points (5.0R)
- **MFE**: 141.25 points
- **MAE**: 9.50 points

### Trade #1544 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:00:00
- **FVG 5m**: 26157.50 - 26160.50
- **Entrée**: 26154.50 @ 2025-11-03 08:49:00
- **Stop Loss**: 26173.58
- **Risk**: 19.08 points
- **TP 1RR**: 26135.42 ✅
- **TP 1.5RR**: 26125.88 ✅
- **TP 2RR**: 26116.34 ✅
- **TP 2.5RR**: 26106.80 ✅
- **TP 3RR**: 26097.26 ✅
- **TP 3.5RR**: 26087.72 ✅
- **TP 4RR**: 26078.18 ✅
- **TP 4.5RR**: 26068.64 ✅
- **TP 5RR**: 26059.10 ✅
- **PnL**: 95.40 points (5.0R)
- **MFE**: 113.75 points
- **MAE**: 4.00 points

### Trade #1545 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:30:00
- **FVG 5m**: 26191.25 - 26206.50
- **Entrée**: 26189.75 @ 2025-11-03 08:37:00
- **Stop Loss**: 26219.60
- **Risk**: 29.85 points
- **TP 1RR**: 26159.90 ✅
- **TP 1.5RR**: 26144.97 ✅
- **TP 2RR**: 26130.04 ✅
- **TP 2.5RR**: 26115.12 ✅
- **TP 3RR**: 26100.19 ✅
- **TP 3.5RR**: 26085.26 ✅
- **TP 4RR**: 26070.34 ✅
- **TP 4.5RR**: 26055.41 ✅
- **TP 5RR**: 26040.48 ✅
- **PnL**: 149.27 points (5.0R)
- **MFE**: 150.75 points
- **MAE**: 8.25 points

### Trade #1546 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:30:00
- **FVG 5m**: 26191.25 - 26206.50
- **Entrée**: 26189.75 @ 2025-11-03 08:37:00
- **Stop Loss**: 26219.60
- **Risk**: 29.85 points
- **TP 1RR**: 26159.90 ✅
- **TP 1.5RR**: 26144.97 ✅
- **TP 2RR**: 26130.04 ✅
- **TP 2.5RR**: 26115.12 ✅
- **TP 3RR**: 26100.19 ✅
- **TP 3.5RR**: 26085.26 ✅
- **TP 4RR**: 26070.34 ✅
- **TP 4.5RR**: 26055.41 ✅
- **TP 5RR**: 26040.48 ✅
- **PnL**: 149.27 points (5.0R)
- **MFE**: 150.75 points
- **MAE**: 8.25 points

### Trade #1547 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:30:00
- **FVG 5m**: 26191.25 - 26206.50
- **Entrée**: 26189.75 @ 2025-11-03 08:37:00
- **Stop Loss**: 26219.60
- **Risk**: 29.85 points
- **TP 1RR**: 26159.90 ✅
- **TP 1.5RR**: 26144.97 ✅
- **TP 2RR**: 26130.04 ✅
- **TP 2.5RR**: 26115.12 ✅
- **TP 3RR**: 26100.19 ✅
- **TP 3.5RR**: 26085.26 ✅
- **TP 4RR**: 26070.34 ✅
- **TP 4.5RR**: 26055.41 ✅
- **TP 5RR**: 26040.48 ✅
- **PnL**: 149.27 points (5.0R)
- **MFE**: 150.75 points
- **MAE**: 8.25 points

### Trade #1548 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 09:15:00
- **FVG 5m**: 26191.25 - 26206.50
- **Entrée**: 26085.50 @ 2025-11-03 09:16:00
- **Stop Loss**: 26219.60
- **Risk**: 134.10 points
- **TP 1RR**: 25951.40 ✅
- **TP 1.5RR**: 25884.35 ✅
- **TP 2RR**: 25817.29 ✅
- **TP 2.5RR**: 25750.24 ✅
- **TP 3RR**: 25683.19 ✅
- **TP 3.5RR**: 25616.14 ✅
- **TP 4RR**: 25549.09 ✅
- **TP 4.5RR**: 25482.04 ✅
- **TP 5RR**: 25414.98 ✅
- **PnL**: 670.52 points (5.0R)
- **MFE**: 671.50 points
- **MAE**: 94.50 points

### Trade #1549 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 15:00:00
- **FVG 5m**: 26103.25 - 26114.00
- **Entrée**: 26094.50 @ 2025-11-03 17:00:00
- **Stop Loss**: 26127.06
- **Risk**: 32.56 points
- **TP 1RR**: 26061.94 ✅
- **TP 1.5RR**: 26045.66 ✅
- **TP 2RR**: 26029.39 ✅
- **TP 2.5RR**: 26013.11 ✅
- **TP 3RR**: 25996.83 ✅
- **TP 3.5RR**: 25980.55 ✅
- **TP 4RR**: 25964.27 ✅
- **TP 4.5RR**: 25947.99 ✅
- **TP 5RR**: 25931.71 ✅
- **PnL**: 162.79 points (5.0R)
- **MFE**: 165.50 points
- **MAE**: 5.50 points

### Trade #1550 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-03 19:15:00
- **FVG 5m**: 25999.50 - 26003.25
- **Entrée**: 26005.25 @ 2025-11-03 19:17:00
- **Stop Loss**: 25986.50
- **Risk**: 18.75 points
- **TP 1RR**: 26024.00 ✅
- **TP 1.5RR**: 26033.37 ❌
- **TP 2RR**: 26042.75 ❌
- **TP 2.5RR**: 26052.12 ❌
- **TP 3RR**: 26061.50 ❌
- **TP 3.5RR**: 26070.87 ❌
- **TP 4RR**: 26080.25 ❌
- **TP 4.5RR**: 26089.62 ❌
- **TP 5RR**: 26099.00 ❌
- **PnL**: -18.75 points (-1.0R)
- **MFE**: 25.75 points
- **MAE**: 21.25 points

### Trade #1551 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-03 19:15:00
- **FVG 5m**: 25999.50 - 26003.25
- **Entrée**: 26005.25 @ 2025-11-03 19:17:00
- **Stop Loss**: 25986.50
- **Risk**: 18.75 points
- **TP 1RR**: 26024.00 ✅
- **TP 1.5RR**: 26033.37 ❌
- **TP 2RR**: 26042.75 ❌
- **TP 2.5RR**: 26052.12 ❌
- **TP 3RR**: 26061.50 ❌
- **TP 3.5RR**: 26070.87 ❌
- **TP 4RR**: 26080.25 ❌
- **TP 4.5RR**: 26089.62 ❌
- **TP 5RR**: 26099.00 ❌
- **PnL**: -18.75 points (-1.0R)
- **MFE**: 25.75 points
- **MAE**: 21.25 points

### Trade #1552 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 04:15:00
- **FVG 5m**: 25680.00 - 25692.50
- **Entrée**: 25696.25 @ 2025-11-04 04:18:00
- **Stop Loss**: 25667.16
- **Risk**: 29.09 points
- **TP 1RR**: 25725.34 ✅
- **TP 1.5RR**: 25739.89 ✅
- **TP 2RR**: 25754.43 ✅
- **TP 2.5RR**: 25768.97 ✅
- **TP 3RR**: 25783.52 ✅
- **TP 3.5RR**: 25798.07 ❌
- **TP 4RR**: 25812.61 ❌
- **TP 4.5RR**: 25827.15 ❌
- **TP 5RR**: 25841.70 ❌
- **PnL**: -29.09 points (-1.0R)
- **MFE**: 96.25 points
- **MAE**: 33.25 points

### Trade #1553 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 08:45:00
- **FVG 5m**: 25704.50 - 25712.00
- **Entrée**: 25761.75 @ 2025-11-04 08:46:00
- **Stop Loss**: 25691.65
- **Risk**: 70.10 points
- **TP 1RR**: 25831.85 ✅
- **TP 1.5RR**: 25866.90 ✅
- **TP 2RR**: 25901.95 ❌
- **TP 2.5RR**: 25937.01 ❌
- **TP 3RR**: 25972.06 ❌
- **TP 3.5RR**: 26007.11 ❌
- **TP 4RR**: 26042.16 ❌
- **TP 4.5RR**: 26077.21 ❌
- **TP 5RR**: 26112.26 ❌
- **PnL**: -70.10 points (-1.0R)
- **MFE**: 131.75 points
- **MAE**: 71.75 points

### Trade #1554 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 08:45:00
- **FVG 5m**: 25704.50 - 25712.00
- **Entrée**: 25761.75 @ 2025-11-04 08:46:00
- **Stop Loss**: 25691.65
- **Risk**: 70.10 points
- **TP 1RR**: 25831.85 ✅
- **TP 1.5RR**: 25866.90 ✅
- **TP 2RR**: 25901.95 ❌
- **TP 2.5RR**: 25937.01 ❌
- **TP 3RR**: 25972.06 ❌
- **TP 3.5RR**: 26007.11 ❌
- **TP 4RR**: 26042.16 ❌
- **TP 4.5RR**: 26077.21 ❌
- **TP 5RR**: 26112.26 ❌
- **PnL**: -70.10 points (-1.0R)
- **MFE**: 131.75 points
- **MAE**: 71.75 points

### Trade #1555 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 09:45:00
- **FVG 5m**: 25855.75 - 25864.00
- **Entrée**: 25838.25 @ 2025-11-04 09:47:00
- **Stop Loss**: 25876.93
- **Risk**: 38.68 points
- **TP 1RR**: 25799.57 ✅
- **TP 1.5RR**: 25780.23 ✅
- **TP 2RR**: 25760.89 ✅
- **TP 2.5RR**: 25741.54 ✅
- **TP 3RR**: 25722.20 ✅
- **TP 3.5RR**: 25702.86 ✅
- **TP 4RR**: 25683.52 ✅
- **TP 4.5RR**: 25664.18 ✅
- **TP 5RR**: 25644.84 ✅
- **PnL**: 193.41 points (5.0R)
- **MFE**: 196.00 points
- **MAE**: 3.75 points

### Trade #1556 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 11:15:00
- **FVG 5m**: 25720.50 - 25725.00
- **Entrée**: 25729.25 @ 2025-11-04 11:26:00
- **Stop Loss**: 25707.64
- **Risk**: 21.61 points
- **TP 1RR**: 25750.86 ❌
- **TP 1.5RR**: 25761.67 ❌
- **TP 2RR**: 25772.47 ❌
- **TP 2.5RR**: 25783.28 ❌
- **TP 3RR**: 25794.08 ❌
- **TP 3.5RR**: 25804.89 ❌
- **TP 4RR**: 25815.69 ❌
- **TP 4.5RR**: 25826.50 ❌
- **TP 5RR**: 25837.30 ❌
- **PnL**: -21.61 points (-1.0R)
- **MFE**: 4.50 points
- **MAE**: 25.50 points

### Trade #1557 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:00:00
- **FVG 5m**: 25570.25 - 25573.75
- **Entrée**: 25384.75 @ 2025-11-04 19:01:00
- **Stop Loss**: 25586.54
- **Risk**: 201.79 points
- **TP 1RR**: 25182.96 ❌
- **TP 1.5RR**: 25082.07 ❌
- **TP 2RR**: 24981.18 ❌
- **TP 2.5RR**: 24880.28 ❌
- **TP 3RR**: 24779.39 ❌
- **TP 3.5RR**: 24678.50 ❌
- **TP 4RR**: 24577.60 ❌
- **TP 4.5RR**: 24476.71 ❌
- **TP 5RR**: 24375.82 ❌
- **PnL**: -201.79 points (-1.0R)
- **MFE**: 102.75 points
- **MAE**: 203.75 points

### Trade #1558 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:00:00
- **FVG 5m**: 25570.25 - 25573.75
- **Entrée**: 25384.75 @ 2025-11-04 19:01:00
- **Stop Loss**: 25586.54
- **Risk**: 201.79 points
- **TP 1RR**: 25182.96 ❌
- **TP 1.5RR**: 25082.07 ❌
- **TP 2RR**: 24981.18 ❌
- **TP 2.5RR**: 24880.28 ❌
- **TP 3RR**: 24779.39 ❌
- **TP 3.5RR**: 24678.50 ❌
- **TP 4RR**: 24577.60 ❌
- **TP 4.5RR**: 24476.71 ❌
- **TP 5RR**: 24375.82 ❌
- **PnL**: -201.79 points (-1.0R)
- **MFE**: 102.75 points
- **MAE**: 203.75 points

### Trade #1559 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:00:00
- **FVG 5m**: 25570.25 - 25573.75
- **Entrée**: 25384.75 @ 2025-11-04 19:01:00
- **Stop Loss**: 25586.54
- **Risk**: 201.79 points
- **TP 1RR**: 25182.96 ❌
- **TP 1.5RR**: 25082.07 ❌
- **TP 2RR**: 24981.18 ❌
- **TP 2.5RR**: 24880.28 ❌
- **TP 3RR**: 24779.39 ❌
- **TP 3.5RR**: 24678.50 ❌
- **TP 4RR**: 24577.60 ❌
- **TP 4.5RR**: 24476.71 ❌
- **TP 5RR**: 24375.82 ❌
- **PnL**: -201.79 points (-1.0R)
- **MFE**: 102.75 points
- **MAE**: 203.75 points

### Trade #1560 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:15:00
- **FVG 5m**: 25570.25 - 25573.75
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25586.54
- **Risk**: 235.04 points
- **TP 1RR**: 25116.46 ❌
- **TP 1.5RR**: 24998.94 ❌
- **TP 2RR**: 24881.43 ❌
- **TP 2.5RR**: 24763.91 ❌
- **TP 3RR**: 24646.39 ❌
- **TP 3.5RR**: 24528.87 ❌
- **TP 4RR**: 24411.35 ❌
- **TP 4.5RR**: 24293.83 ❌
- **TP 5RR**: 24176.32 ❌
- **PnL**: -235.04 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 237.00 points

### Trade #1561 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:15:00
- **FVG 5m**: 25570.25 - 25573.75
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25586.54
- **Risk**: 235.04 points
- **TP 1RR**: 25116.46 ❌
- **TP 1.5RR**: 24998.94 ❌
- **TP 2RR**: 24881.43 ❌
- **TP 2.5RR**: 24763.91 ❌
- **TP 3RR**: 24646.39 ❌
- **TP 3.5RR**: 24528.87 ❌
- **TP 4RR**: 24411.35 ❌
- **TP 4.5RR**: 24293.83 ❌
- **TP 5RR**: 24176.32 ❌
- **PnL**: -235.04 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 237.00 points

### Trade #1562 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:15:00
- **FVG 5m**: 25570.25 - 25573.75
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25586.54
- **Risk**: 235.04 points
- **TP 1RR**: 25116.46 ❌
- **TP 1.5RR**: 24998.94 ❌
- **TP 2RR**: 24881.43 ❌
- **TP 2.5RR**: 24763.91 ❌
- **TP 3RR**: 24646.39 ❌
- **TP 3.5RR**: 24528.87 ❌
- **TP 4RR**: 24411.35 ❌
- **TP 4.5RR**: 24293.83 ❌
- **TP 5RR**: 24176.32 ❌
- **PnL**: -235.04 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 237.00 points

### Trade #1563 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:15:00
- **FVG 5m**: 25570.25 - 25573.75
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25586.54
- **Risk**: 235.04 points
- **TP 1RR**: 25116.46 ❌
- **TP 1.5RR**: 24998.94 ❌
- **TP 2RR**: 24881.43 ❌
- **TP 2.5RR**: 24763.91 ❌
- **TP 3RR**: 24646.39 ❌
- **TP 3.5RR**: 24528.87 ❌
- **TP 4RR**: 24411.35 ❌
- **TP 4.5RR**: 24293.83 ❌
- **TP 5RR**: 24176.32 ❌
- **PnL**: -235.04 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 237.00 points

### Trade #1564 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:15:00
- **FVG 5m**: 25570.25 - 25573.75
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25586.54
- **Risk**: 235.04 points
- **TP 1RR**: 25116.46 ❌
- **TP 1.5RR**: 24998.94 ❌
- **TP 2RR**: 24881.43 ❌
- **TP 2.5RR**: 24763.91 ❌
- **TP 3RR**: 24646.39 ❌
- **TP 3.5RR**: 24528.87 ❌
- **TP 4RR**: 24411.35 ❌
- **TP 4.5RR**: 24293.83 ❌
- **TP 5RR**: 24176.32 ❌
- **PnL**: -235.04 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 237.00 points

### Trade #1565 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 19:45:00
- **FVG 5m**: 25352.75 - 25357.25
- **Entrée**: 25357.75 @ 2025-11-04 20:43:00
- **Stop Loss**: 25340.07
- **Risk**: 17.68 points
- **TP 1RR**: 25375.43 ✅
- **TP 1.5RR**: 25384.26 ✅
- **TP 2RR**: 25393.10 ✅
- **TP 2.5RR**: 25401.94 ✅
- **TP 3RR**: 25410.78 ✅
- **TP 3.5RR**: 25419.62 ✅
- **TP 4RR**: 25428.46 ✅
- **TP 4.5RR**: 25437.29 ✅
- **TP 5RR**: 25446.13 ✅
- **PnL**: 88.38 points (5.0R)
- **MFE**: 89.75 points
- **MAE**: 5.00 points

### Trade #1566 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 20:30:00
- **FVG 5m**: 25352.75 - 25357.25
- **Entrée**: 25357.75 @ 2025-11-04 20:43:00
- **Stop Loss**: 25340.07
- **Risk**: 17.68 points
- **TP 1RR**: 25375.43 ✅
- **TP 1.5RR**: 25384.26 ✅
- **TP 2RR**: 25393.10 ✅
- **TP 2.5RR**: 25401.94 ✅
- **TP 3RR**: 25410.78 ✅
- **TP 3.5RR**: 25419.62 ✅
- **TP 4RR**: 25428.46 ✅
- **TP 4.5RR**: 25437.29 ✅
- **TP 5RR**: 25446.13 ✅
- **PnL**: 88.38 points (5.0R)
- **MFE**: 89.75 points
- **MAE**: 5.00 points

### Trade #1567 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-05 05:30:00
- **FVG 5m**: 25441.75 - 25467.50
- **Entrée**: 25474.25 @ 2025-11-05 05:40:00
- **Stop Loss**: 25429.03
- **Risk**: 45.22 points
- **TP 1RR**: 25519.47 ✅
- **TP 1.5RR**: 25542.08 ✅
- **TP 2RR**: 25564.69 ✅
- **TP 2.5RR**: 25587.30 ✅
- **TP 3RR**: 25609.91 ✅
- **TP 3.5RR**: 25632.52 ✅
- **TP 4RR**: 25655.13 ✅
- **TP 4.5RR**: 25677.74 ✅
- **TP 5RR**: 25700.35 ✅
- **PnL**: 226.10 points (5.0R)
- **MFE**: 242.25 points
- **MAE**: 16.00 points

### Trade #1568 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-05 08:15:00
- **FVG 5m**: 25516.50 - 25524.25
- **Entrée**: 25501.50 @ 2025-11-05 08:34:00
- **Stop Loss**: 25537.01
- **Risk**: 35.51 points
- **TP 1RR**: 25465.99 ❌
- **TP 1.5RR**: 25448.23 ❌
- **TP 2RR**: 25430.48 ❌
- **TP 2.5RR**: 25412.72 ❌
- **TP 3RR**: 25394.96 ❌
- **TP 3.5RR**: 25377.21 ❌
- **TP 4RR**: 25359.45 ❌
- **TP 4.5RR**: 25341.70 ❌
- **TP 5RR**: 25323.94 ❌
- **PnL**: -35.51 points (-1.0R)
- **MFE**: 13.50 points
- **MAE**: 42.25 points

### Trade #1569 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-05 08:15:00
- **FVG 5m**: 25516.50 - 25524.25
- **Entrée**: 25501.50 @ 2025-11-05 08:34:00
- **Stop Loss**: 25537.01
- **Risk**: 35.51 points
- **TP 1RR**: 25465.99 ❌
- **TP 1.5RR**: 25448.23 ❌
- **TP 2RR**: 25430.48 ❌
- **TP 2.5RR**: 25412.72 ❌
- **TP 3RR**: 25394.96 ❌
- **TP 3.5RR**: 25377.21 ❌
- **TP 4RR**: 25359.45 ❌
- **TP 4.5RR**: 25341.70 ❌
- **TP 5RR**: 25323.94 ❌
- **PnL**: -35.51 points (-1.0R)
- **MFE**: 13.50 points
- **MAE**: 42.25 points

### Trade #1570 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 07:45:00
- **FVG 5m**: 25798.00 - 25805.00
- **Entrée**: 25796.75 @ 2025-11-06 07:47:00
- **Stop Loss**: 25817.90
- **Risk**: 21.15 points
- **TP 1RR**: 25775.60 ✅
- **TP 1.5RR**: 25765.02 ✅
- **TP 2RR**: 25754.44 ✅
- **TP 2.5RR**: 25743.87 ✅
- **TP 3RR**: 25733.29 ✅
- **TP 3.5RR**: 25722.72 ✅
- **TP 4RR**: 25712.14 ✅
- **TP 4.5RR**: 25701.56 ✅
- **TP 5RR**: 25690.99 ✅
- **PnL**: 105.76 points (5.0R)
- **MFE**: 112.75 points
- **MAE**: 3.00 points

### Trade #1571 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 07:45:00
- **FVG 5m**: 25798.00 - 25805.00
- **Entrée**: 25796.75 @ 2025-11-06 07:47:00
- **Stop Loss**: 25817.90
- **Risk**: 21.15 points
- **TP 1RR**: 25775.60 ✅
- **TP 1.5RR**: 25765.02 ✅
- **TP 2RR**: 25754.44 ✅
- **TP 2.5RR**: 25743.87 ✅
- **TP 3RR**: 25733.29 ✅
- **TP 3.5RR**: 25722.72 ✅
- **TP 4RR**: 25712.14 ✅
- **TP 4.5RR**: 25701.56 ✅
- **TP 5RR**: 25690.99 ✅
- **PnL**: 105.76 points (5.0R)
- **MFE**: 112.75 points
- **MAE**: 3.00 points

### Trade #1572 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 08:00:00
- **FVG 5m**: 25798.00 - 25805.00
- **Entrée**: 25770.50 @ 2025-11-06 08:01:00
- **Stop Loss**: 25817.90
- **Risk**: 47.40 points
- **TP 1RR**: 25723.10 ✅
- **TP 1.5RR**: 25699.40 ✅
- **TP 2RR**: 25675.69 ✅
- **TP 2.5RR**: 25651.99 ✅
- **TP 3RR**: 25628.29 ✅
- **TP 3.5RR**: 25604.59 ✅
- **TP 4RR**: 25580.89 ✅
- **TP 4.5RR**: 25557.19 ✅
- **TP 5RR**: 25533.49 ✅
- **PnL**: 237.01 points (5.0R)
- **MFE**: 242.25 points
- **MAE**: 3.75 points

### Trade #1573 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 09:15:00
- **FVG 5m**: 25474.00 - 25510.00
- **Entrée**: 25512.00 @ 2025-11-06 09:21:00
- **Stop Loss**: 25461.26
- **Risk**: 50.74 points
- **TP 1RR**: 25562.74 ❌
- **TP 1.5RR**: 25588.11 ❌
- **TP 2RR**: 25613.47 ❌
- **TP 2.5RR**: 25638.84 ❌
- **TP 3RR**: 25664.21 ❌
- **TP 3.5RR**: 25689.58 ❌
- **TP 4RR**: 25714.95 ❌
- **TP 4.5RR**: 25740.32 ❌
- **TP 5RR**: 25765.69 ❌
- **PnL**: -50.74 points (-1.0R)
- **MFE**: 35.00 points
- **MAE**: 75.50 points

### Trade #1574 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 09:15:00
- **FVG 5m**: 25474.00 - 25510.00
- **Entrée**: 25512.00 @ 2025-11-06 09:21:00
- **Stop Loss**: 25461.26
- **Risk**: 50.74 points
- **TP 1RR**: 25562.74 ❌
- **TP 1.5RR**: 25588.11 ❌
- **TP 2RR**: 25613.47 ❌
- **TP 2.5RR**: 25638.84 ❌
- **TP 3RR**: 25664.21 ❌
- **TP 3.5RR**: 25689.58 ❌
- **TP 4RR**: 25714.95 ❌
- **TP 4.5RR**: 25740.32 ❌
- **TP 5RR**: 25765.69 ❌
- **PnL**: -50.74 points (-1.0R)
- **MFE**: 35.00 points
- **MAE**: 75.50 points

### Trade #1575 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 09:30:00
- **FVG 5m**: 25798.00 - 25805.00
- **Entrée**: 25497.00 @ 2025-11-06 09:31:00
- **Stop Loss**: 25817.90
- **Risk**: 320.90 points
- **TP 1RR**: 25176.10 ✅
- **TP 1.5RR**: 25015.65 ✅
- **TP 2RR**: 24855.19 ✅
- **TP 2.5RR**: 24694.74 ❌
- **TP 3RR**: 24534.29 ❌
- **TP 3.5RR**: 24373.84 ❌
- **TP 4RR**: 24213.39 ❌
- **TP 4.5RR**: 24052.94 ❌
- **TP 5RR**: 23892.49 ❌
- **PnL**: -320.90 points (-1.0R)
- **MFE**: 787.75 points
- **MAE**: 321.50 points

### Trade #1576 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 11:15:00
- **FVG 5m**: 25268.00 - 25296.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25255.37
- **Risk**: 42.88 points
- **TP 1RR**: 25341.13 ✅
- **TP 1.5RR**: 25362.58 ❌
- **TP 2RR**: 25384.02 ❌
- **TP 2.5RR**: 25405.46 ❌
- **TP 3RR**: 25426.90 ❌
- **TP 3.5RR**: 25448.34 ❌
- **TP 4RR**: 25469.79 ❌
- **TP 4.5RR**: 25491.23 ❌
- **TP 5RR**: 25512.67 ❌
- **PnL**: -42.88 points (-1.0R)
- **MFE**: 58.00 points
- **MAE**: 57.00 points

### Trade #1577 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 11:30:00
- **FVG 5m**: 25268.00 - 25296.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25255.37
- **Risk**: 42.88 points
- **TP 1RR**: 25341.13 ✅
- **TP 1.5RR**: 25362.58 ❌
- **TP 2RR**: 25384.02 ❌
- **TP 2.5RR**: 25405.46 ❌
- **TP 3RR**: 25426.90 ❌
- **TP 3.5RR**: 25448.34 ❌
- **TP 4RR**: 25469.79 ❌
- **TP 4.5RR**: 25491.23 ❌
- **TP 5RR**: 25512.67 ❌
- **PnL**: -42.88 points (-1.0R)
- **MFE**: 58.00 points
- **MAE**: 57.00 points

### Trade #1578 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 11:30:00
- **FVG 5m**: 25268.00 - 25296.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25255.37
- **Risk**: 42.88 points
- **TP 1RR**: 25341.13 ✅
- **TP 1.5RR**: 25362.58 ❌
- **TP 2RR**: 25384.02 ❌
- **TP 2.5RR**: 25405.46 ❌
- **TP 3RR**: 25426.90 ❌
- **TP 3.5RR**: 25448.34 ❌
- **TP 4RR**: 25469.79 ❌
- **TP 4.5RR**: 25491.23 ❌
- **TP 5RR**: 25512.67 ❌
- **PnL**: -42.88 points (-1.0R)
- **MFE**: 58.00 points
- **MAE**: 57.00 points

### Trade #1579 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 13:15:00
- **FVG 5m**: 25260.25 - 25289.50
- **Entrée**: 25382.50 @ 2025-11-06 13:16:00
- **Stop Loss**: 25247.62
- **Risk**: 134.88 points
- **TP 1RR**: 25517.38 ❌
- **TP 1.5RR**: 25584.82 ❌
- **TP 2RR**: 25652.26 ❌
- **TP 2.5RR**: 25719.70 ❌
- **TP 3RR**: 25787.14 ❌
- **TP 3.5RR**: 25854.58 ❌
- **TP 4RR**: 25922.02 ❌
- **TP 4.5RR**: 25989.46 ❌
- **TP 5RR**: 26056.90 ❌
- **PnL**: -134.88 points (-1.0R)
- **MFE**: 56.00 points
- **MAE**: 138.00 points

### Trade #1580 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 05:00:00
- **FVG 5m**: 25298.00 - 25315.75
- **Entrée**: 25202.00 @ 2025-11-07 05:01:00
- **Stop Loss**: 25328.41
- **Risk**: 126.41 points
- **TP 1RR**: 25075.59 ✅
- **TP 1.5RR**: 25012.39 ✅
- **TP 2RR**: 24949.18 ✅
- **TP 2.5RR**: 24885.98 ✅
- **TP 3RR**: 24822.78 ✅
- **TP 3.5RR**: 24759.57 ✅
- **TP 4RR**: 24696.37 ❌
- **TP 4.5RR**: 24633.16 ❌
- **TP 5RR**: 24569.96 ❌
- **PnL**: -126.41 points (-1.0R)
- **MFE**: 492.75 points
- **MAE**: 189.50 points

### Trade #1581 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 05:45:00
- **FVG 5m**: 25133.75 - 25176.00
- **Entrée**: 25177.00 @ 2025-11-07 05:50:00
- **Stop Loss**: 25121.18
- **Risk**: 55.82 points
- **TP 1RR**: 25232.82 ❌
- **TP 1.5RR**: 25260.73 ❌
- **TP 2RR**: 25288.63 ❌
- **TP 2.5RR**: 25316.54 ❌
- **TP 3RR**: 25344.45 ❌
- **TP 3.5RR**: 25372.36 ❌
- **TP 4RR**: 25400.27 ❌
- **TP 4.5RR**: 25428.18 ❌
- **TP 5RR**: 25456.08 ❌
- **PnL**: -55.82 points (-1.0R)
- **MFE**: 18.50 points
- **MAE**: 58.00 points

### Trade #1582 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 06:30:00
- **FVG 5m**: 25159.50 - 25168.25
- **Entrée**: 25149.25 @ 2025-11-07 06:31:00
- **Stop Loss**: 25180.83
- **Risk**: 31.58 points
- **TP 1RR**: 25117.67 ✅
- **TP 1.5RR**: 25101.87 ✅
- **TP 2RR**: 25086.08 ✅
- **TP 2.5RR**: 25070.29 ✅
- **TP 3RR**: 25054.50 ✅
- **TP 3.5RR**: 25038.71 ✅
- **TP 4RR**: 25022.91 ✅
- **TP 4.5RR**: 25007.12 ✅
- **TP 5RR**: 24991.33 ✅
- **PnL**: 157.92 points (5.0R)
- **MFE**: 201.25 points
- **MAE**: 3.25 points

### Trade #1583 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 08:30:00
- **FVG 5m**: 25093.50 - 25120.00
- **Entrée**: 25063.00 @ 2025-11-07 08:31:00
- **Stop Loss**: 25132.56
- **Risk**: 69.56 points
- **TP 1RR**: 24993.44 ✅
- **TP 1.5RR**: 24958.66 ✅
- **TP 2RR**: 24923.88 ✅
- **TP 2.5RR**: 24889.10 ✅
- **TP 3RR**: 24854.32 ✅
- **TP 3.5RR**: 24819.54 ✅
- **TP 4RR**: 24784.76 ✅
- **TP 4.5RR**: 24749.98 ✅
- **TP 5RR**: 24715.20 ✅
- **PnL**: 347.80 points (5.0R)
- **MFE**: 353.75 points
- **MAE**: 26.25 points

### Trade #1584 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 11:15:00
- **FVG 5m**: 24758.00 - 24766.00
- **Entrée**: 24793.00 @ 2025-11-07 11:16:00
- **Stop Loss**: 24745.62
- **Risk**: 47.38 points
- **TP 1RR**: 24840.38 ✅
- **TP 1.5RR**: 24864.07 ✅
- **TP 2RR**: 24887.76 ✅
- **TP 2.5RR**: 24911.45 ✅
- **TP 3RR**: 24935.14 ✅
- **TP 3.5RR**: 24958.83 ✅
- **TP 4RR**: 24982.52 ✅
- **TP 4.5RR**: 25006.21 ✅
- **TP 5RR**: 25029.90 ✅
- **PnL**: 236.90 points (5.0R)
- **MFE**: 252.75 points
- **MAE**: 36.25 points

### Trade #1585 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 13:30:00
- **FVG 5m**: 24888.25 - 24925.25
- **Entrée**: 24988.50 @ 2025-11-07 13:31:00
- **Stop Loss**: 24875.81
- **Risk**: 112.69 points
- **TP 1RR**: 25101.19 ✅
- **TP 1.5RR**: 25157.54 ✅
- **TP 2RR**: 25213.89 ✅
- **TP 2.5RR**: 25270.24 ✅
- **TP 3RR**: 25326.58 ✅
- **TP 3.5RR**: 25382.93 ✅
- **TP 4RR**: 25439.28 ✅
- **TP 4.5RR**: 25495.62 ✅
- **TP 5RR**: 25551.97 ✅
- **PnL**: 563.47 points (5.0R)
- **MFE**: 574.50 points
- **MAE**: 4.00 points

### Trade #1586 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 15:00:00
- **FVG 5m**: 25076.75 - 25096.50
- **Entrée**: 25184.50 @ 2025-11-07 15:01:00
- **Stop Loss**: 25064.21
- **Risk**: 120.29 points
- **TP 1RR**: 25304.79 ✅
- **TP 1.5RR**: 25364.93 ✅
- **TP 2RR**: 25425.08 ✅
- **TP 2.5RR**: 25485.22 ✅
- **TP 3RR**: 25545.37 ✅
- **TP 3.5RR**: 25605.51 ✅
- **TP 4RR**: 25665.65 ✅
- **TP 4.5RR**: 25725.80 ✅
- **TP 5RR**: 25785.94 ✅
- **PnL**: 601.44 points (5.0R)
- **MFE**: 601.50 points
- **MAE**: 6.25 points

### Trade #1587 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 00:45:00
- **FVG 5m**: 25481.50 - 25486.00
- **Entrée**: 25481.25 @ 2025-11-10 00:55:00
- **Stop Loss**: 25498.74
- **Risk**: 17.49 points
- **TP 1RR**: 25463.76 ✅
- **TP 1.5RR**: 25455.01 ❌
- **TP 2RR**: 25446.26 ❌
- **TP 2.5RR**: 25437.52 ❌
- **TP 3RR**: 25428.77 ❌
- **TP 3.5RR**: 25420.02 ❌
- **TP 4RR**: 25411.28 ❌
- **TP 4.5RR**: 25402.53 ❌
- **TP 5RR**: 25393.79 ❌
- **PnL**: -17.49 points (-1.0R)
- **MFE**: 18.00 points
- **MAE**: 18.00 points

### Trade #1588 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-10 08:30:00
- **FVG 5m**: 25541.50 - 25544.25
- **Entrée**: 25575.00 @ 2025-11-10 08:31:00
- **Stop Loss**: 25528.73
- **Risk**: 46.27 points
- **TP 1RR**: 25621.27 ✅
- **TP 1.5RR**: 25644.41 ✅
- **TP 2RR**: 25667.54 ❌
- **TP 2.5RR**: 25690.68 ❌
- **TP 3RR**: 25713.81 ❌
- **TP 3.5RR**: 25736.95 ❌
- **TP 4RR**: 25760.08 ❌
- **TP 4.5RR**: 25783.22 ❌
- **TP 5RR**: 25806.35 ❌
- **PnL**: -46.27 points (-1.0R)
- **MFE**: 91.50 points
- **MAE**: 58.50 points

### Trade #1589 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 09:45:00
- **FVG 5m**: 25591.75 - 25609.25
- **Entrée**: 25577.75 @ 2025-11-10 09:50:00
- **Stop Loss**: 25622.05
- **Risk**: 44.30 points
- **TP 1RR**: 25533.45 ✅
- **TP 1.5RR**: 25511.29 ✅
- **TP 2RR**: 25489.14 ✅
- **TP 2.5RR**: 25466.99 ✅
- **TP 3RR**: 25444.84 ❌
- **TP 3.5RR**: 25422.68 ❌
- **TP 4RR**: 25400.53 ❌
- **TP 4.5RR**: 25378.38 ❌
- **TP 5RR**: 25356.23 ❌
- **PnL**: -44.30 points (-1.0R)
- **MFE**: 125.75 points
- **MAE**: 55.25 points

### Trade #1590 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 10:15:00
- **FVG 5m**: 25591.75 - 25609.25
- **Entrée**: 25508.25 @ 2025-11-10 10:16:00
- **Stop Loss**: 25622.05
- **Risk**: 113.80 points
- **TP 1RR**: 25394.45 ❌
- **TP 1.5RR**: 25337.54 ❌
- **TP 2RR**: 25280.64 ❌
- **TP 2.5RR**: 25223.74 ❌
- **TP 3RR**: 25166.84 ❌
- **TP 3.5RR**: 25109.93 ❌
- **TP 4RR**: 25053.03 ❌
- **TP 4.5RR**: 24996.13 ❌
- **TP 5RR**: 24939.23 ❌
- **PnL**: -113.80 points (-1.0R)
- **MFE**: 56.25 points
- **MAE**: 124.75 points

### Trade #1591 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 10:15:00
- **FVG 5m**: 25591.75 - 25609.25
- **Entrée**: 25508.25 @ 2025-11-10 10:16:00
- **Stop Loss**: 25622.05
- **Risk**: 113.80 points
- **TP 1RR**: 25394.45 ❌
- **TP 1.5RR**: 25337.54 ❌
- **TP 2RR**: 25280.64 ❌
- **TP 2.5RR**: 25223.74 ❌
- **TP 3RR**: 25166.84 ❌
- **TP 3.5RR**: 25109.93 ❌
- **TP 4RR**: 25053.03 ❌
- **TP 4.5RR**: 24996.13 ❌
- **TP 5RR**: 24939.23 ❌
- **PnL**: -113.80 points (-1.0R)
- **MFE**: 56.25 points
- **MAE**: 124.75 points

### Trade #1592 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 14:45:00
- **FVG 5m**: 25714.75 - 25721.25
- **Entrée**: 25713.00 @ 2025-11-10 14:59:00
- **Stop Loss**: 25734.11
- **Risk**: 21.11 points
- **TP 1RR**: 25691.89 ❌
- **TP 1.5RR**: 25681.33 ❌
- **TP 2RR**: 25670.78 ❌
- **TP 2.5RR**: 25660.22 ❌
- **TP 3RR**: 25649.67 ❌
- **TP 3.5RR**: 25639.11 ❌
- **TP 4RR**: 25628.56 ❌
- **TP 4.5RR**: 25618.00 ❌
- **TP 5RR**: 25607.45 ❌
- **PnL**: -21.11 points (-1.0R)
- **MFE**: 6.00 points
- **MAE**: 22.25 points

### Trade #1593 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-11 08:45:00
- **FVG 5m**: 25592.00 - 25609.75
- **Entrée**: 25619.00 @ 2025-11-11 08:46:00
- **Stop Loss**: 25579.20
- **Risk**: 39.80 points
- **TP 1RR**: 25658.80 ❌
- **TP 1.5RR**: 25678.69 ❌
- **TP 2RR**: 25698.59 ❌
- **TP 2.5RR**: 25718.49 ❌
- **TP 3RR**: 25738.39 ❌
- **TP 3.5RR**: 25758.29 ❌
- **TP 4RR**: 25778.18 ❌
- **TP 4.5RR**: 25798.08 ❌
- **TP 5RR**: 25817.98 ❌
- **PnL**: -39.80 points (-1.0R)
- **MFE**: 4.00 points
- **MAE**: 41.00 points

### Trade #1594 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-11 12:30:00
- **FVG 5m**: 25525.75 - 25548.75
- **Entrée**: 25644.25 @ 2025-11-11 12:31:00
- **Stop Loss**: 25512.99
- **Risk**: 131.26 points
- **TP 1RR**: 25775.51 ✅
- **TP 1.5RR**: 25841.14 ❌
- **TP 2RR**: 25906.78 ❌
- **TP 2.5RR**: 25972.41 ❌
- **TP 3RR**: 26038.04 ❌
- **TP 3.5RR**: 26103.67 ❌
- **TP 4RR**: 26169.30 ❌
- **TP 4.5RR**: 26234.93 ❌
- **TP 5RR**: 26300.56 ❌
- **PnL**: -131.26 points (-1.0R)
- **MFE**: 185.75 points
- **MAE**: 134.50 points

### Trade #1595 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-11 19:00:00
- **FVG 5m**: 25652.75 - 25656.25
- **Entrée**: 25689.75 @ 2025-11-11 19:01:00
- **Stop Loss**: 25639.92
- **Risk**: 49.83 points
- **TP 1RR**: 25739.58 ✅
- **TP 1.5RR**: 25764.49 ✅
- **TP 2RR**: 25789.40 ✅
- **TP 2.5RR**: 25814.32 ✅
- **TP 3RR**: 25839.23 ❌
- **TP 3.5RR**: 25864.14 ❌
- **TP 4RR**: 25889.06 ❌
- **TP 4.5RR**: 25913.97 ❌
- **TP 5RR**: 25938.88 ❌
- **PnL**: -49.83 points (-1.0R)
- **MFE**: 140.25 points
- **MAE**: 52.50 points


## 📋 Règles de la Stratégie


### Conditions d'Entrée

1. **Sweep 15m détecté**:
   - Bullish: Prix casse sous un swing low puis clôture au-dessus
   - Bearish: Prix casse au-dessus d'un swing high puis clôture en-dessous

2. **FVG 5m formé** (dans les 30 bougies suivantes):
   - Pour sweep bullish: FVG bullish (gap up)
   - Pour sweep bearish: FVG bearish (gap down)

3. **Entrée 1m** (dans les 60 bougies suivantes):
   - Le prix doit toucher la zone FVG
   - Puis clôturer au-delà du FVG dans le sens du trade

### Gestion du Trade

| Élément | Placement |
|---------|-----------|
| **Stop Loss** | Au-dessus du FVG comblé (short) / En-dessous du FVG comblé (long) |
| **TP 1** | 1x le risque |
| **TP 1.5** | 1.5x le risque |
| **TP 2** | 2x le risque |
| **TP 2.5** | 2.5x le risque |
| **TP 3** | 3x le risque |
| **TP 3.5** | 3.5x le risque |
| **TP 4** | 4x le risque |
| **TP 4.5** | 4.5x le risque |
| **TP 5** | 5x le risque |

### Gestion de Position Suggérée

Exemple avec sortie progressive:
- **10%** à TP1 (1RR)
- **10%** à TP2 (2RR)
- **20%** à TP3 (3RR)
- **30%** à TP4 (4RR)
- **30%** à TP5 (5RR)


## 💡 Recommandations

⚠️ Le win rate est inférieur à 50%. Considérer des filtres supplémentaires.

✅ Bon taux d'atteinte du TP2 - la stratégie capture bien les mouvements.

⚠️ Taux de SL élevé. Suggestions:
   - Augmenter le buffer du SL
   - Filtrer les setups par volume
   - Attendre confirmation supplémentaire


### Filtres Additionnels Suggérés

1. **Volume**: N'entrer que si le volume du sweep est > 1.5x la moyenne
2. **Session**: Privilégier les sessions Londres et New York
3. **Trend**: Trader dans le sens de la tendance HTF (4H/Daily)
4. **News**: Éviter les 30 minutes avant/après les annonces majeures


---

*Rapport généré le 2025-11-30 23:58:17*
