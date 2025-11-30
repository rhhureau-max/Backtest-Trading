# 📊 Analyse Détaillée: Stratégie Sweep + FVG Multi-Timeframe

---

## 🎯 Vue d'Ensemble de la Stratégie


Cette stratégie combine la détection de **Liquidity Sweeps** sur le timeframe 15 minutes 
avec les **Fair Value Gaps (FVG)** sur 5 minutes pour trouver des entrées précises sur 1 minute.

### Logique de la Stratégie

1. **Détection du Sweep (15m)**: Identifier quand le prix dépasse un swing high/low puis revient
2. **Formation du FVG (5m)**: Attendre un retracement qui crée un FVG
3. **Confirmation du Retournement (5m)**: Le prix doit commencer à revenir vers la tendance originale
4. **Entrée (1m)**: Entrer quand le prix comble et clôture au-delà du FVG 5m
5. **Stop Loss**: Au-dessus du FVG comblé (short) / En-dessous du FVG comblé (long)
6. **Take Profits**: 1RR, 2RR, 3RR, 4RR, 15RR


## 📈 Résumé des Résultats

| Métrique | Valeur |
|----------|--------|
| Nombre total de trades | 2033 |
| Trades gagnants | 212 |
| Trades perdants | 1819 |
| Win Rate | 10.4% |
| PnL Total (points) | 29259.35 |
| Gain moyen | 419.49 pts |
| Perte moyenne | -32.81 pts |


### 🎯 Analyse des Take Profits

| Take Profit | Atteints | Taux |
|-------------|----------|------|
| TP 1RR | 1441 | 70.9% |
| TP 2RR | 998 | 49.1% |
| TP 3RR | 746 | 36.7% |
| TP 4RR | 595 | 29.3% |
| TP 15RR | 212 | 10.4% |
| Stop Loss | 1819 | 89.5% |


### 📊 Analyse par Direction

| Direction | Trades | Gagnants | Win Rate |
|-----------|--------|----------|----------|
| LONG | 1047 | 122 | 11.7% |
| SHORT | 986 | 90 | 9.1% |


## 📝 Détail des Trades

### Trade #1 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-02 07:15:00
- **FVG 5m**: 22093.10 - 22099.02
- **Entrée**: 22091.81 @ 2025-01-02 07:54:00
- **Stop Loss**: 22110.07
- **Risk**: 18.27 points
- **TP 1RR**: 22073.54 ✅
- **TP 2RR**: 22055.27 ✅
- **TP 3RR**: 22037.01 ✅
- **TP 4RR**: 22018.74 ✅
- **TP 15RR**: 21817.81 ✅
- **PnL**: 273.99 points (15.0R)
- **MFE**: 293.57 points
- **MAE**: 16.24 points

### Trade #2 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-02 08:30:00
- **FVG 5m**: 22031.24 - 22065.00
- **Entrée**: 22020.15 @ 2025-01-02 09:19:00
- **Stop Loss**: 22076.03
- **Risk**: 55.88 points
- **TP 1RR**: 21964.28 ✅
- **TP 2RR**: 21908.40 ✅
- **TP 3RR**: 21852.52 ✅
- **TP 4RR**: 21796.64 ✅
- **TP 15RR**: 21181.96 ❌
- **PnL**: -55.88 points (-1.0R)
- **MFE**: 386.61 points
- **MAE**: 60.57 points

### Trade #3 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-02 09:15:00
- **FVG 5m**: 21892.83 - 21918.35
- **Entrée**: 21876.08 @ 2025-01-02 10:03:00
- **Stop Loss**: 21929.31
- **Risk**: 53.23 points
- **TP 1RR**: 21822.85 ❌
- **TP 2RR**: 21769.62 ❌
- **TP 3RR**: 21716.39 ❌
- **TP 4RR**: 21663.16 ❌
- **TP 15RR**: 21077.65 ❌
- **PnL**: -53.23 points (-1.0R)
- **MFE**: 33.76 points
- **MAE**: 58.51 points

### Trade #4 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-02 14:00:00
- **FVG 5m**: 21790.76 - 21794.12
- **Entrée**: 21797.47 @ 2025-01-02 14:11:00
- **Stop Loss**: 21779.87
- **Risk**: 17.60 points
- **TP 1RR**: 21815.06 ✅
- **TP 2RR**: 21832.66 ✅
- **TP 3RR**: 21850.26 ✅
- **TP 4RR**: 21867.85 ❌
- **TP 15RR**: 22061.42 ❌
- **PnL**: -17.60 points (-1.0R)
- **MFE**: 54.64 points
- **MAE**: 23.20 points

### Trade #5 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-02 14:45:00
- **FVG 5m**: 21823.50 - 21849.79
- **Entrée**: 21850.30 @ 2025-01-02 18:09:00
- **Stop Loss**: 21812.59
- **Risk**: 37.72 points
- **TP 1RR**: 21888.02 ✅
- **TP 2RR**: 21925.74 ✅
- **TP 3RR**: 21963.45 ✅
- **TP 4RR**: 22001.17 ✅
- **TP 15RR**: 22416.06 ✅
- **PnL**: 565.75 points (15.0R)
- **MFE**: 568.06 points
- **MAE**: 2.06 points

### Trade #6 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 02:15:00
- **FVG 5m**: 21890.00 - 21905.46
- **Entrée**: 21889.74 @ 2025-01-03 02:28:00
- **Stop Loss**: 21916.41
- **Risk**: 26.67 points
- **TP 1RR**: 21863.06 ❌
- **TP 2RR**: 21836.39 ❌
- **TP 3RR**: 21809.71 ❌
- **TP 4RR**: 21783.04 ❌
- **TP 15RR**: 21489.61 ❌
- **PnL**: -26.67 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 30.41 points

### Trade #7 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 02:15:00
- **FVG 5m**: 21890.00 - 21905.46
- **Entrée**: 21889.74 @ 2025-01-03 02:28:00
- **Stop Loss**: 21916.41
- **Risk**: 26.67 points
- **TP 1RR**: 21863.06 ❌
- **TP 2RR**: 21836.39 ❌
- **TP 3RR**: 21809.71 ❌
- **TP 4RR**: 21783.04 ❌
- **TP 15RR**: 21489.61 ❌
- **PnL**: -26.67 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 30.41 points

### Trade #8 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 09:00:00
- **FVG 5m**: 22030.21 - 22049.79
- **Entrée**: 22028.40 @ 2025-01-03 09:12:00
- **Stop Loss**: 22060.82
- **Risk**: 32.42 points
- **TP 1RR**: 21995.98 ✅
- **TP 2RR**: 21963.57 ✅
- **TP 3RR**: 21931.15 ✅
- **TP 4RR**: 21898.73 ❌
- **TP 15RR**: 21542.14 ❌
- **PnL**: -32.42 points (-1.0R)
- **MFE**: 108.51 points
- **MAE**: 32.73 points

### Trade #9 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 15:00:00
- **FVG 5m**: 22182.79 - 22185.37
- **Entrée**: 22177.89 @ 2025-01-05 17:32:00
- **Stop Loss**: 22196.46
- **Risk**: 18.57 points
- **TP 1RR**: 22159.33 ❌
- **TP 2RR**: 22140.76 ❌
- **TP 3RR**: 22122.19 ❌
- **TP 4RR**: 22103.62 ❌
- **TP 15RR**: 21899.38 ❌
- **PnL**: -18.57 points (-1.0R)
- **MFE**: 10.31 points
- **MAE**: 18.82 points

### Trade #10 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 15:00:00
- **FVG 5m**: 22182.79 - 22185.37
- **Entrée**: 22177.89 @ 2025-01-05 17:32:00
- **Stop Loss**: 22196.46
- **Risk**: 18.57 points
- **TP 1RR**: 22159.33 ❌
- **TP 2RR**: 22140.76 ❌
- **TP 3RR**: 22122.19 ❌
- **TP 4RR**: 22103.62 ❌
- **TP 15RR**: 21899.38 ❌
- **PnL**: -18.57 points (-1.0R)
- **MFE**: 10.31 points
- **MAE**: 18.82 points

### Trade #11 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 01:00:00
- **FVG 5m**: 22392.33 - 22401.10
- **Entrée**: 22403.16 @ 2025-01-07 02:34:00
- **Stop Loss**: 22381.14
- **Risk**: 22.02 points
- **TP 1RR**: 22425.18 ✅
- **TP 2RR**: 22447.20 ✅
- **TP 3RR**: 22469.22 ✅
- **TP 4RR**: 22491.24 ❌
- **TP 15RR**: 22733.48 ❌
- **PnL**: -22.02 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 36.08 points

### Trade #12 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22382.54 - 22422.49
- **Entrée**: 22382.02 @ 2025-01-07 08:59:00
- **Stop Loss**: 22433.70
- **Risk**: 51.68 points
- **TP 1RR**: 22330.35 ✅
- **TP 2RR**: 22278.67 ✅
- **TP 3RR**: 22226.99 ✅
- **TP 4RR**: 22175.32 ✅
- **TP 15RR**: 21606.87 ✅
- **PnL**: 775.15 points (15.0R)
- **MFE**: 792.30 points
- **MAE**: 0.52 points

### Trade #13 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22382.54 - 22422.49
- **Entrée**: 22382.02 @ 2025-01-07 08:59:00
- **Stop Loss**: 22433.70
- **Risk**: 51.68 points
- **TP 1RR**: 22330.35 ✅
- **TP 2RR**: 22278.67 ✅
- **TP 3RR**: 22226.99 ✅
- **TP 4RR**: 22175.32 ✅
- **TP 15RR**: 21606.87 ✅
- **PnL**: 775.15 points (15.0R)
- **MFE**: 792.30 points
- **MAE**: 0.52 points

### Trade #14 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22382.54 - 22422.49
- **Entrée**: 22382.02 @ 2025-01-07 08:59:00
- **Stop Loss**: 22433.70
- **Risk**: 51.68 points
- **TP 1RR**: 22330.35 ✅
- **TP 2RR**: 22278.67 ✅
- **TP 3RR**: 22226.99 ✅
- **TP 4RR**: 22175.32 ✅
- **TP 15RR**: 21606.87 ✅
- **PnL**: 775.15 points (15.0R)
- **MFE**: 792.30 points
- **MAE**: 0.52 points

### Trade #15 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22118.61 - 22152.38
- **Entrée**: 22170.93 @ 2025-01-07 09:55:00
- **Stop Loss**: 22107.55
- **Risk**: 63.38 points
- **TP 1RR**: 22234.31 ✅
- **TP 2RR**: 22297.70 ❌
- **TP 3RR**: 22361.08 ❌
- **TP 4RR**: 22424.46 ❌
- **TP 15RR**: 23121.65 ❌
- **PnL**: -63.38 points (-1.0R)
- **MFE**: 70.36 points
- **MAE**: 67.01 points

### Trade #16 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22118.61 - 22152.38
- **Entrée**: 22170.93 @ 2025-01-07 09:55:00
- **Stop Loss**: 22107.55
- **Risk**: 63.38 points
- **TP 1RR**: 22234.31 ✅
- **TP 2RR**: 22297.70 ❌
- **TP 3RR**: 22361.08 ❌
- **TP 4RR**: 22424.46 ❌
- **TP 15RR**: 23121.65 ❌
- **PnL**: -63.38 points (-1.0R)
- **MFE**: 70.36 points
- **MAE**: 67.01 points

### Trade #17 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 09:30:00
- **FVG 5m**: 22122.22 - 22164.23
- **Entrée**: 22119.90 @ 2025-01-07 10:53:00
- **Stop Loss**: 22175.31
- **Risk**: 55.41 points
- **TP 1RR**: 22064.49 ✅
- **TP 2RR**: 22009.07 ❌
- **TP 3RR**: 21953.66 ❌
- **TP 4RR**: 21898.25 ❌
- **TP 15RR**: 21288.70 ❌
- **PnL**: -55.41 points (-1.0R)
- **MFE**: 70.62 points
- **MAE**: 56.70 points

### Trade #18 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 09:30:00
- **FVG 5m**: 22122.22 - 22164.23
- **Entrée**: 22119.90 @ 2025-01-07 10:53:00
- **Stop Loss**: 22175.31
- **Risk**: 55.41 points
- **TP 1RR**: 22064.49 ✅
- **TP 2RR**: 22009.07 ❌
- **TP 3RR**: 21953.66 ❌
- **TP 4RR**: 21898.25 ❌
- **TP 15RR**: 21288.70 ❌
- **PnL**: -55.41 points (-1.0R)
- **MFE**: 70.62 points
- **MAE**: 56.70 points

### Trade #19 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 09:30:00
- **FVG 5m**: 22122.22 - 22164.23
- **Entrée**: 22119.90 @ 2025-01-07 10:53:00
- **Stop Loss**: 22175.31
- **Risk**: 55.41 points
- **TP 1RR**: 22064.49 ✅
- **TP 2RR**: 22009.07 ❌
- **TP 3RR**: 21953.66 ❌
- **TP 4RR**: 21898.25 ❌
- **TP 15RR**: 21288.70 ❌
- **PnL**: -55.41 points (-1.0R)
- **MFE**: 70.62 points
- **MAE**: 56.70 points

### Trade #20 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 09:45:00
- **FVG 5m**: 22171.19 - 22187.94
- **Entrée**: 22188.20 @ 2025-01-07 09:57:00
- **Stop Loss**: 22160.11
- **Risk**: 28.10 points
- **TP 1RR**: 22216.30 ✅
- **TP 2RR**: 22244.40 ❌
- **TP 3RR**: 22272.49 ❌
- **TP 4RR**: 22300.59 ❌
- **TP 15RR**: 22609.65 ❌
- **PnL**: -28.10 points (-1.0R)
- **MFE**: 37.37 points
- **MAE**: 29.12 points

### Trade #21 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 09:45:00
- **FVG 5m**: 22171.19 - 22187.94
- **Entrée**: 22188.20 @ 2025-01-07 09:57:00
- **Stop Loss**: 22160.11
- **Risk**: 28.10 points
- **TP 1RR**: 22216.30 ✅
- **TP 2RR**: 22244.40 ❌
- **TP 3RR**: 22272.49 ❌
- **TP 4RR**: 22300.59 ❌
- **TP 15RR**: 22609.65 ❌
- **PnL**: -28.10 points (-1.0R)
- **MFE**: 37.37 points
- **MAE**: 29.12 points

### Trade #22 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 10:45:00
- **FVG 5m**: 22103.15 - 22108.04
- **Entrée**: 22101.60 @ 2025-01-07 11:22:00
- **Stop Loss**: 22119.10
- **Risk**: 17.50 points
- **TP 1RR**: 22084.10 ✅
- **TP 2RR**: 22066.61 ❌
- **TP 3RR**: 22049.11 ❌
- **TP 4RR**: 22031.61 ❌
- **TP 15RR**: 21839.14 ❌
- **PnL**: -17.50 points (-1.0R)
- **MFE**: 28.35 points
- **MAE**: 18.82 points

### Trade #23 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 11:45:00
- **FVG 5m**: 22079.44 - 22102.63
- **Entrée**: 22109.08 @ 2025-01-07 11:59:00
- **Stop Loss**: 22068.40
- **Risk**: 40.68 points
- **TP 1RR**: 22149.76 ✅
- **TP 2RR**: 22190.44 ❌
- **TP 3RR**: 22231.12 ❌
- **TP 4RR**: 22271.80 ❌
- **TP 15RR**: 22719.28 ❌
- **PnL**: -40.68 points (-1.0R)
- **MFE**: 74.49 points
- **MAE**: 42.27 points

### Trade #24 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 15:00:00
- **FVG 5m**: 22041.29 - 22046.19
- **Entrée**: 22047.22 @ 2025-01-07 17:54:00
- **Stop Loss**: 22030.27
- **Risk**: 16.95 points
- **TP 1RR**: 22064.17 ✅
- **TP 2RR**: 22081.11 ✅
- **TP 3RR**: 22098.06 ✅
- **TP 4RR**: 22115.01 ❌
- **TP 15RR**: 22301.45 ❌
- **PnL**: -16.95 points (-1.0R)
- **MFE**: 53.61 points
- **MAE**: 18.04 points

### Trade #25 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 01:45:00
- **FVG 5m**: 22064.23 - 22068.09
- **Entrée**: 22072.22 @ 2025-01-08 02:48:00
- **Stop Loss**: 22053.20
- **Risk**: 19.02 points
- **TP 1RR**: 22091.24 ✅
- **TP 2RR**: 22110.26 ✅
- **TP 3RR**: 22129.28 ❌
- **TP 4RR**: 22148.31 ❌
- **TP 15RR**: 22357.55 ❌
- **PnL**: -19.02 points (-1.0R)
- **MFE**: 40.21 points
- **MAE**: 19.33 points

### Trade #26 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 05:00:00
- **FVG 5m**: 22097.73 - 22101.86
- **Entrée**: 22096.45 @ 2025-01-08 05:12:00
- **Stop Loss**: 22112.91
- **Risk**: 16.46 points
- **TP 1RR**: 22079.98 ✅
- **TP 2RR**: 22063.52 ✅
- **TP 3RR**: 22047.06 ✅
- **TP 4RR**: 22030.59 ✅
- **TP 15RR**: 21849.49 ✅
- **PnL**: 246.95 points (15.0R)
- **MFE**: 263.41 points
- **MAE**: 1.29 points

### Trade #27 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 05:00:00
- **FVG 5m**: 22097.73 - 22101.86
- **Entrée**: 22096.45 @ 2025-01-08 05:12:00
- **Stop Loss**: 22112.91
- **Risk**: 16.46 points
- **TP 1RR**: 22079.98 ✅
- **TP 2RR**: 22063.52 ✅
- **TP 3RR**: 22047.06 ✅
- **TP 4RR**: 22030.59 ✅
- **TP 15RR**: 21849.49 ✅
- **PnL**: 246.95 points (15.0R)
- **MFE**: 263.41 points
- **MAE**: 1.29 points

### Trade #28 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 05:15:00
- **FVG 5m**: 21981.49 - 21997.22
- **Entrée**: 22002.37 @ 2025-01-08 05:48:00
- **Stop Loss**: 21970.50
- **Risk**: 31.87 points
- **TP 1RR**: 22034.24 ✅
- **TP 2RR**: 22066.11 ❌
- **TP 3RR**: 22097.97 ❌
- **TP 4RR**: 22129.84 ❌
- **TP 15RR**: 22480.39 ❌
- **PnL**: -31.87 points (-1.0R)
- **MFE**: 31.96 points
- **MAE**: 33.51 points

### Trade #29 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 05:45:00
- **FVG 5m**: 21913.97 - 21923.76
- **Entrée**: 21934.84 @ 2025-01-08 06:37:00
- **Stop Loss**: 21903.01
- **Risk**: 31.83 points
- **TP 1RR**: 21966.68 ✅
- **TP 2RR**: 21998.51 ✅
- **TP 3RR**: 22030.34 ✅
- **TP 4RR**: 22062.18 ✅
- **TP 15RR**: 22412.35 ❌
- **PnL**: -31.83 points (-1.0R)
- **MFE**: 134.28 points
- **MAE**: 38.66 points

### Trade #30 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 06:30:00
- **FVG 5m**: 21922.47 - 21947.99
- **Entrée**: 21958.04 @ 2025-01-08 07:08:00
- **Stop Loss**: 21911.51
- **Risk**: 46.53 points
- **TP 1RR**: 22004.57 ✅
- **TP 2RR**: 22051.10 ✅
- **TP 3RR**: 22097.63 ❌
- **TP 4RR**: 22144.16 ❌
- **TP 15RR**: 22655.98 ❌
- **PnL**: -46.53 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 61.86 points

### Trade #31 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 09:00:00
- **FVG 5m**: 21959.33 - 22004.95
- **Entrée**: 21957.27 @ 2025-01-08 09:12:00
- **Stop Loss**: 22015.95
- **Risk**: 58.68 points
- **TP 1RR**: 21898.58 ✅
- **TP 2RR**: 21839.90 ❌
- **TP 3RR**: 21781.21 ❌
- **TP 4RR**: 21722.53 ❌
- **TP 15RR**: 21077.00 ❌
- **PnL**: -58.68 points (-1.0R)
- **MFE**: 68.82 points
- **MAE**: 59.02 points

### Trade #32 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 11:15:00
- **FVG 5m**: 21875.05 - 21894.63
- **Entrée**: 21857.00 @ 2025-01-08 11:28:00
- **Stop Loss**: 21905.58
- **Risk**: 48.58 points
- **TP 1RR**: 21808.43 ❌
- **TP 2RR**: 21759.85 ❌
- **TP 3RR**: 21711.27 ❌
- **TP 4RR**: 21662.69 ❌
- **TP 15RR**: 21128.34 ❌
- **PnL**: -48.58 points (-1.0R)
- **MFE**: 35.31 points
- **MAE**: 51.03 points

### Trade #33 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21934.44
- **Risk**: 44.74 points
- **TP 1RR**: 22023.91 ✅
- **TP 2RR**: 22068.65 ✅
- **TP 3RR**: 22113.38 ❌
- **TP 4RR**: 22158.12 ❌
- **TP 15RR**: 22650.23 ❌
- **PnL**: -44.74 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 49.49 points

### Trade #34 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21934.44
- **Risk**: 44.74 points
- **TP 1RR**: 22023.91 ✅
- **TP 2RR**: 22068.65 ✅
- **TP 3RR**: 22113.38 ❌
- **TP 4RR**: 22158.12 ❌
- **TP 15RR**: 22650.23 ❌
- **PnL**: -44.74 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 49.49 points

### Trade #35 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21934.44
- **Risk**: 44.74 points
- **TP 1RR**: 22023.91 ✅
- **TP 2RR**: 22068.65 ✅
- **TP 3RR**: 22113.38 ❌
- **TP 4RR**: 22158.12 ❌
- **TP 15RR**: 22650.23 ❌
- **PnL**: -44.74 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 49.49 points

### Trade #36 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21934.44
- **Risk**: 44.74 points
- **TP 1RR**: 22023.91 ✅
- **TP 2RR**: 22068.65 ✅
- **TP 3RR**: 22113.38 ❌
- **TP 4RR**: 22158.12 ❌
- **TP 15RR**: 22650.23 ❌
- **PnL**: -44.74 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 49.49 points

### Trade #37 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21934.44
- **Risk**: 44.74 points
- **TP 1RR**: 22023.91 ✅
- **TP 2RR**: 22068.65 ✅
- **TP 3RR**: 22113.38 ❌
- **TP 4RR**: 22158.12 ❌
- **TP 15RR**: 22650.23 ❌
- **PnL**: -44.74 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 49.49 points

### Trade #38 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21934.44
- **Risk**: 44.74 points
- **TP 1RR**: 22023.91 ✅
- **TP 2RR**: 22068.65 ✅
- **TP 3RR**: 22113.38 ❌
- **TP 4RR**: 22158.12 ❌
- **TP 15RR**: 22650.23 ❌
- **PnL**: -44.74 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 49.49 points

### Trade #39 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21934.44
- **Risk**: 44.74 points
- **TP 1RR**: 22023.91 ✅
- **TP 2RR**: 22068.65 ✅
- **TP 3RR**: 22113.38 ❌
- **TP 4RR**: 22158.12 ❌
- **TP 15RR**: 22650.23 ❌
- **PnL**: -44.74 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 49.49 points

### Trade #40 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 13:15:00
- **FVG 5m**: 22011.13 - 22013.45
- **Entrée**: 22007.27 @ 2025-01-08 13:36:00
- **Stop Loss**: 22024.46
- **Risk**: 17.19 points
- **TP 1RR**: 21990.07 ❌
- **TP 2RR**: 21972.88 ❌
- **TP 3RR**: 21955.69 ❌
- **TP 4RR**: 21938.50 ❌
- **TP 15RR**: 21749.38 ❌
- **PnL**: -17.19 points (-1.0R)
- **MFE**: 2.32 points
- **MAE**: 27.84 points

### Trade #41 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 13:30:00
- **FVG 5m**: 21999.28 - 22013.45
- **Entrée**: 21983.56 @ 2025-01-08 15:35:00
- **Stop Loss**: 22024.46
- **Risk**: 40.90 points
- **TP 1RR**: 21942.65 ✅
- **TP 2RR**: 21901.75 ✅
- **TP 3RR**: 21860.84 ✅
- **TP 4RR**: 21819.94 ❌
- **TP 15RR**: 21369.98 ❌
- **PnL**: -40.90 points (-1.0R)
- **MFE**: 148.20 points
- **MAE**: 43.30 points

### Trade #42 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 02:15:00
- **FVG 5m**: 21922.47 - 21935.10
- **Entrée**: 21938.45 @ 2025-01-09 02:29:00
- **Stop Loss**: 21911.51
- **Risk**: 26.94 points
- **TP 1RR**: 21965.39 ✅
- **TP 2RR**: 21992.33 ✅
- **TP 3RR**: 22019.27 ❌
- **TP 4RR**: 22046.22 ❌
- **TP 15RR**: 22342.57 ❌
- **PnL**: -26.94 points (-1.0R)
- **MFE**: 56.70 points
- **MAE**: 35.05 points

### Trade #43 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 02:30:00
- **FVG 5m**: 21953.66 - 21957.52
- **Entrée**: 21964.74 @ 2025-01-09 03:37:00
- **Stop Loss**: 21942.68
- **Risk**: 22.06 points
- **TP 1RR**: 21986.80 ✅
- **TP 2RR**: 22008.86 ❌
- **TP 3RR**: 22030.92 ❌
- **TP 4RR**: 22052.98 ❌
- **TP 15RR**: 22295.64 ❌
- **PnL**: -22.06 points (-1.0R)
- **MFE**: 30.41 points
- **MAE**: 22.68 points

### Trade #44 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 08:00:00
- **FVG 5m**: 21859.07 - 21864.99
- **Entrée**: 21866.28 @ 2025-01-09 18:48:00
- **Stop Loss**: 21848.14
- **Risk**: 18.15 points
- **TP 1RR**: 21884.43 ✅
- **TP 2RR**: 21902.58 ✅
- **TP 3RR**: 21920.72 ✅
- **TP 4RR**: 21938.87 ✅
- **TP 15RR**: 22138.48 ❌
- **PnL**: -18.15 points (-1.0R)
- **MFE**: 168.05 points
- **MAE**: 143.56 points

### Trade #45 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 19:00:00
- **FVG 5m**: 21925.31 - 21929.69
- **Entrée**: 21934.33 @ 2025-01-09 20:52:00
- **Stop Loss**: 21914.34
- **Risk**: 19.98 points
- **TP 1RR**: 21954.31 ✅
- **TP 2RR**: 21974.29 ✅
- **TP 3RR**: 21994.28 ❌
- **TP 4RR**: 22014.26 ❌
- **TP 15RR**: 22234.08 ❌
- **PnL**: -19.98 points (-1.0R)
- **MFE**: 54.64 points
- **MAE**: 29.38 points

### Trade #46 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-09 23:30:00
- **FVG 5m**: 21941.03 - 21944.12
- **Entrée**: 21936.90 @ 2025-01-10 00:25:00
- **Stop Loss**: 21955.09
- **Risk**: 18.19 points
- **TP 1RR**: 21918.72 ✅
- **TP 2RR**: 21900.53 ✅
- **TP 3RR**: 21882.34 ❌
- **TP 4RR**: 21864.15 ❌
- **TP 15RR**: 21664.07 ❌
- **PnL**: -18.19 points (-1.0R)
- **MFE**: 45.62 points
- **MAE**: 22.17 points

### Trade #47 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 05:15:00
- **FVG 5m**: 21970.67 - 21973.76
- **Entrée**: 21969.12 @ 2025-01-10 06:04:00
- **Stop Loss**: 21984.75
- **Risk**: 15.63 points
- **TP 1RR**: 21953.50 ✅
- **TP 2RR**: 21937.87 ✅
- **TP 3RR**: 21922.24 ✅
- **TP 4RR**: 21906.62 ✅
- **TP 15RR**: 21734.73 ✅
- **PnL**: 234.39 points (15.0R)
- **MFE**: 246.40 points
- **MAE**: 14.69 points

### Trade #48 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 05:45:00
- **FVG 5m**: 21970.67 - 21973.76
- **Entrée**: 21969.12 @ 2025-01-10 06:04:00
- **Stop Loss**: 21984.75
- **Risk**: 15.63 points
- **TP 1RR**: 21953.50 ✅
- **TP 2RR**: 21937.87 ✅
- **TP 3RR**: 21922.24 ✅
- **TP 4RR**: 21906.62 ✅
- **TP 15RR**: 21734.73 ✅
- **PnL**: 234.39 points (15.0R)
- **MFE**: 246.40 points
- **MAE**: 14.69 points

### Trade #49 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 05:45:00
- **FVG 5m**: 21970.67 - 21973.76
- **Entrée**: 21969.12 @ 2025-01-10 06:04:00
- **Stop Loss**: 21984.75
- **Risk**: 15.63 points
- **TP 1RR**: 21953.50 ✅
- **TP 2RR**: 21937.87 ✅
- **TP 3RR**: 21922.24 ✅
- **TP 4RR**: 21906.62 ✅
- **TP 15RR**: 21734.73 ✅
- **PnL**: 234.39 points (15.0R)
- **MFE**: 246.40 points
- **MAE**: 14.69 points

### Trade #50 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 06:00:00
- **FVG 5m**: 21966.03 - 21970.67
- **Entrée**: 21959.59 @ 2025-01-10 07:11:00
- **Stop Loss**: 21981.65
- **Risk**: 22.07 points
- **TP 1RR**: 21937.52 ✅
- **TP 2RR**: 21915.45 ✅
- **TP 3RR**: 21893.38 ✅
- **TP 4RR**: 21871.31 ✅
- **TP 15RR**: 21628.56 ✅
- **PnL**: 331.02 points (15.0R)
- **MFE**: 338.41 points
- **MAE**: 20.62 points

### Trade #51 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-10 08:00:00
- **FVG 5m**: 21564.98 - 21583.28
- **Entrée**: 21586.89 @ 2025-01-10 09:18:00
- **Stop Loss**: 21554.20
- **Risk**: 32.69 points
- **TP 1RR**: 21619.58 ✅
- **TP 2RR**: 21652.27 ✅
- **TP 3RR**: 21684.96 ✅
- **TP 4RR**: 21717.65 ✅
- **TP 15RR**: 22077.25 ❌
- **PnL**: -32.69 points (-1.0R)
- **MFE**: 190.73 points
- **MAE**: 42.27 points

### Trade #52 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-10 08:00:00
- **FVG 5m**: 21564.98 - 21583.28
- **Entrée**: 21586.89 @ 2025-01-10 09:18:00
- **Stop Loss**: 21554.20
- **Risk**: 32.69 points
- **TP 1RR**: 21619.58 ✅
- **TP 2RR**: 21652.27 ✅
- **TP 3RR**: 21684.96 ✅
- **TP 4RR**: 21717.65 ✅
- **TP 15RR**: 22077.25 ❌
- **PnL**: -32.69 points (-1.0R)
- **MFE**: 190.73 points
- **MAE**: 42.27 points

### Trade #53 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-10 08:15:00
- **FVG 5m**: 21564.98 - 21583.28
- **Entrée**: 21586.89 @ 2025-01-10 09:18:00
- **Stop Loss**: 21554.20
- **Risk**: 32.69 points
- **TP 1RR**: 21619.58 ✅
- **TP 2RR**: 21652.27 ✅
- **TP 3RR**: 21684.96 ✅
- **TP 4RR**: 21717.65 ✅
- **TP 15RR**: 22077.25 ❌
- **PnL**: -32.69 points (-1.0R)
- **MFE**: 190.73 points
- **MAE**: 42.27 points

### Trade #54 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-10 09:15:00
- **FVG 5m**: 21585.09 - 21600.04
- **Entrée**: 21603.39 @ 2025-01-10 11:29:00
- **Stop Loss**: 21574.29
- **Risk**: 29.09 points
- **TP 1RR**: 21632.48 ✅
- **TP 2RR**: 21661.57 ✅
- **TP 3RR**: 21690.66 ✅
- **TP 4RR**: 21719.76 ✅
- **TP 15RR**: 22039.77 ❌
- **PnL**: -29.09 points (-1.0R)
- **MFE**: 228.87 points
- **MAE**: 32.48 points

### Trade #55 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-12 21:15:00
- **FVG 5m**: 21528.90 - 21533.54
- **Entrée**: 21536.12 @ 2025-01-12 22:01:00
- **Stop Loss**: 21518.13
- **Risk**: 17.98 points
- **TP 1RR**: 21554.10 ❌
- **TP 2RR**: 21572.08 ❌
- **TP 3RR**: 21590.06 ❌
- **TP 4RR**: 21608.04 ❌
- **TP 15RR**: 21805.83 ❌
- **PnL**: -17.98 points (-1.0R)
- **MFE**: 12.63 points
- **MAE**: 18.56 points

### Trade #56 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 01:15:00
- **FVG 5m**: 21539.72 - 21542.30
- **Entrée**: 21545.39 @ 2025-01-13 02:04:00
- **Stop Loss**: 21528.95
- **Risk**: 16.44 points
- **TP 1RR**: 21561.83 ❌
- **TP 2RR**: 21578.27 ❌
- **TP 3RR**: 21594.72 ❌
- **TP 4RR**: 21611.16 ❌
- **TP 15RR**: 21792.00 ❌
- **PnL**: -16.44 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 18.30 points

### Trade #57 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 08:30:00
- **FVG 5m**: 21424.51 - 21432.76
- **Entrée**: 21435.85 @ 2025-01-13 08:53:00
- **Stop Loss**: 21413.80
- **Risk**: 22.05 points
- **TP 1RR**: 21457.91 ✅
- **TP 2RR**: 21479.96 ✅
- **TP 3RR**: 21502.01 ❌
- **TP 4RR**: 21524.07 ❌
- **TP 15RR**: 21766.65 ❌
- **PnL**: -22.05 points (-1.0R)
- **MFE**: 65.47 points
- **MAE**: 22.68 points

### Trade #58 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-13 09:45:00
- **FVG 5m**: 21433.28 - 21437.40
- **Entrée**: 21429.15 @ 2025-01-13 10:04:00
- **Stop Loss**: 21448.12
- **Risk**: 18.97 points
- **TP 1RR**: 21410.19 ✅
- **TP 2RR**: 21391.22 ✅
- **TP 3RR**: 21372.25 ❌
- **TP 4RR**: 21353.29 ❌
- **TP 15RR**: 21144.66 ❌
- **PnL**: -18.97 points (-1.0R)
- **MFE**: 43.04 points
- **MAE**: 19.07 points

### Trade #59 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 11:45:00
- **FVG 5m**: 21514.21 - 21524.78
- **Entrée**: 21528.13 @ 2025-01-13 11:58:00
- **Stop Loss**: 21503.45
- **Risk**: 24.68 points
- **TP 1RR**: 21552.80 ❌
- **TP 2RR**: 21577.48 ❌
- **TP 3RR**: 21602.15 ❌
- **TP 4RR**: 21626.83 ❌
- **TP 15RR**: 21898.25 ❌
- **PnL**: -24.68 points (-1.0R)
- **MFE**: 19.07 points
- **MAE**: 25.77 points

### Trade #60 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 11:45:00
- **FVG 5m**: 21514.21 - 21524.78
- **Entrée**: 21528.13 @ 2025-01-13 11:58:00
- **Stop Loss**: 21503.45
- **Risk**: 24.68 points
- **TP 1RR**: 21552.80 ❌
- **TP 2RR**: 21577.48 ❌
- **TP 3RR**: 21602.15 ❌
- **TP 4RR**: 21626.83 ❌
- **TP 15RR**: 21898.25 ❌
- **PnL**: -24.68 points (-1.0R)
- **MFE**: 19.07 points
- **MAE**: 25.77 points

### Trade #61 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-13 12:30:00
- **FVG 5m**: 21506.48 - 21512.92
- **Entrée**: 21496.68 @ 2025-01-13 13:14:00
- **Stop Loss**: 21523.68
- **Risk**: 26.99 points
- **TP 1RR**: 21469.69 ❌
- **TP 2RR**: 21442.69 ❌
- **TP 3RR**: 21415.70 ❌
- **TP 4RR**: 21388.70 ❌
- **TP 15RR**: 21091.77 ❌
- **PnL**: -26.99 points (-1.0R)
- **MFE**: 16.24 points
- **MAE**: 29.12 points

### Trade #62 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 14:45:00
- **FVG 5m**: 21635.35 - 21661.64
- **Entrée**: 21679.68 @ 2025-01-13 17:00:00
- **Stop Loss**: 21624.53
- **Risk**: 55.15 points
- **TP 1RR**: 21734.83 ✅
- **TP 2RR**: 21789.98 ✅
- **TP 3RR**: 21845.13 ❌
- **TP 4RR**: 21900.27 ❌
- **TP 15RR**: 22506.92 ❌
- **PnL**: -55.15 points (-1.0R)
- **MFE**: 118.82 points
- **MAE**: 58.25 points

### Trade #63 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 15:15:00
- **FVG 5m**: 21635.35 - 21661.64
- **Entrée**: 21679.68 @ 2025-01-13 17:00:00
- **Stop Loss**: 21624.53
- **Risk**: 55.15 points
- **TP 1RR**: 21734.83 ✅
- **TP 2RR**: 21789.98 ✅
- **TP 3RR**: 21845.13 ❌
- **TP 4RR**: 21900.27 ❌
- **TP 15RR**: 22506.92 ❌
- **PnL**: -55.15 points (-1.0R)
- **MFE**: 118.82 points
- **MAE**: 58.25 points

### Trade #64 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 00:30:00
- **FVG 5m**: 21691.53 - 21694.88
- **Entrée**: 21687.41 @ 2025-01-14 01:01:00
- **Stop Loss**: 21705.73
- **Risk**: 18.32 points
- **TP 1RR**: 21669.09 ❌
- **TP 2RR**: 21650.77 ❌
- **TP 3RR**: 21632.44 ❌
- **TP 4RR**: 21614.12 ❌
- **TP 15RR**: 21412.58 ❌
- **PnL**: -18.32 points (-1.0R)
- **MFE**: 15.21 points
- **MAE**: 22.17 points

### Trade #65 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 01:00:00
- **FVG 5m**: 21779.17 - 21781.49
- **Entrée**: 21778.91 @ 2025-01-14 02:58:00
- **Stop Loss**: 21792.38
- **Risk**: 13.47 points
- **TP 1RR**: 21765.44 ✅
- **TP 2RR**: 21751.97 ✅
- **TP 3RR**: 21738.50 ✅
- **TP 4RR**: 21725.04 ✅
- **TP 15RR**: 21576.89 ❌
- **PnL**: -13.47 points (-1.0R)
- **MFE**: 186.35 points
- **MAE**: 14.18 points

### Trade #66 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 05:15:00
- **FVG 5m**: 21680.71 - 21689.47
- **Entrée**: 21675.04 @ 2025-01-14 06:07:00
- **Stop Loss**: 21700.32
- **Risk**: 25.28 points
- **TP 1RR**: 21649.76 ✅
- **TP 2RR**: 21624.48 ✅
- **TP 3RR**: 21599.20 ✅
- **TP 4RR**: 21573.93 ❌
- **TP 15RR**: 21295.86 ❌
- **PnL**: -25.28 points (-1.0R)
- **MFE**: 82.48 points
- **MAE**: 113.41 points

### Trade #67 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 06:15:00
- **FVG 5m**: 21611.38 - 21695.14
- **Entrée**: 21713.44 @ 2025-01-14 07:38:00
- **Stop Loss**: 21600.57
- **Risk**: 112.87 points
- **TP 1RR**: 21826.31 ❌
- **TP 2RR**: 21939.18 ❌
- **TP 3RR**: 22052.06 ❌
- **TP 4RR**: 22164.93 ❌
- **TP 15RR**: 23406.51 ❌
- **PnL**: -112.87 points (-1.0R)
- **MFE**: 70.62 points
- **MAE**: 116.50 points

### Trade #68 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 06:30:00
- **FVG 5m**: 21611.38 - 21695.14
- **Entrée**: 21713.44 @ 2025-01-14 07:38:00
- **Stop Loss**: 21600.57
- **Risk**: 112.87 points
- **TP 1RR**: 21826.31 ❌
- **TP 2RR**: 21939.18 ❌
- **TP 3RR**: 22052.06 ❌
- **TP 4RR**: 22164.93 ❌
- **TP 15RR**: 23406.51 ❌
- **PnL**: -112.87 points (-1.0R)
- **MFE**: 70.62 points
- **MAE**: 116.50 points

### Trade #69 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 07:30:00
- **FVG 5m**: 21731.74 - 21737.15
- **Entrée**: 21708.54 @ 2025-01-14 08:47:00
- **Stop Loss**: 21748.02
- **Risk**: 39.48 points
- **TP 1RR**: 21669.07 ✅
- **TP 2RR**: 21629.59 ✅
- **TP 3RR**: 21590.11 ❌
- **TP 4RR**: 21550.63 ❌
- **TP 15RR**: 21116.38 ❌
- **PnL**: -39.48 points (-1.0R)
- **MFE**: 93.04 points
- **MAE**: 42.01 points

### Trade #70 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 07:30:00
- **FVG 5m**: 21704.16 - 21714.22
- **Entrée**: 21716.28 @ 2025-01-14 08:17:00
- **Stop Loss**: 21693.31
- **Risk**: 22.97 points
- **TP 1RR**: 21739.24 ✅
- **TP 2RR**: 21762.21 ❌
- **TP 3RR**: 21785.18 ❌
- **TP 4RR**: 21808.14 ❌
- **TP 15RR**: 22060.77 ❌
- **PnL**: -22.97 points (-1.0R)
- **MFE**: 27.32 points
- **MAE**: 27.58 points

### Trade #71 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 10:00:00
- **FVG 5m**: 21510.60 - 21525.03
- **Entrée**: 21506.99 @ 2025-01-14 10:41:00
- **Stop Loss**: 21535.80
- **Risk**: 28.80 points
- **TP 1RR**: 21478.19 ✅
- **TP 2RR**: 21449.38 ✅
- **TP 3RR**: 21420.58 ❌
- **TP 4RR**: 21391.77 ❌
- **TP 15RR**: 21074.92 ❌
- **PnL**: -28.80 points (-1.0R)
- **MFE**: 71.39 points
- **MAE**: 29.38 points

### Trade #72 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 11:00:00
- **FVG 5m**: 21479.93 - 21493.33
- **Entrée**: 21503.38 @ 2025-01-14 11:42:00
- **Stop Loss**: 21469.19
- **Risk**: 34.19 points
- **TP 1RR**: 21537.58 ✅
- **TP 2RR**: 21571.77 ✅
- **TP 3RR**: 21605.97 ✅
- **TP 4RR**: 21640.16 ✅
- **TP 15RR**: 22016.30 ❌
- **PnL**: -34.19 points (-1.0R)
- **MFE**: 160.57 points
- **MAE**: 48.97 points

### Trade #73 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 12:30:00
- **FVG 5m**: 21604.68 - 21619.88
- **Entrée**: 21629.93 @ 2025-01-14 12:43:00
- **Stop Loss**: 21593.87
- **Risk**: 36.06 points
- **TP 1RR**: 21665.99 ❌
- **TP 2RR**: 21702.06 ❌
- **TP 3RR**: 21738.12 ❌
- **TP 4RR**: 21774.18 ❌
- **TP 15RR**: 22170.85 ❌
- **PnL**: -36.06 points (-1.0R)
- **MFE**: 34.02 points
- **MAE**: 39.95 points

### Trade #74 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 02:00:00
- **FVG 5m**: 21576.58 - 21581.22
- **Entrée**: 21581.99 @ 2025-01-15 02:23:00
- **Stop Loss**: 21565.79
- **Risk**: 16.20 points
- **TP 1RR**: 21598.19 ✅
- **TP 2RR**: 21614.40 ✅
- **TP 3RR**: 21630.60 ✅
- **TP 4RR**: 21646.80 ✅
- **TP 15RR**: 21825.01 ✅
- **PnL**: 243.01 points (15.0R)
- **MFE**: 293.83 points
- **MAE**: 7.73 points

### Trade #75 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 02:15:00
- **FVG 5m**: 21584.06 - 21588.44
- **Entrée**: 21589.21 @ 2025-01-15 02:30:00
- **Stop Loss**: 21573.26
- **Risk**: 15.95 points
- **TP 1RR**: 21605.16 ✅
- **TP 2RR**: 21621.10 ✅
- **TP 3RR**: 21637.05 ✅
- **TP 4RR**: 21653.00 ✅
- **TP 15RR**: 21828.41 ✅
- **PnL**: 239.20 points (15.0R)
- **MFE**: 286.61 points
- **MAE**: 14.95 points

### Trade #76 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 06:15:00
- **FVG 5m**: 21931.75 - 21937.16
- **Entrée**: 21916.03 @ 2025-01-15 08:10:00
- **Stop Loss**: 21948.13
- **Risk**: 32.10 points
- **TP 1RR**: 21883.92 ✅
- **TP 2RR**: 21851.82 ✅
- **TP 3RR**: 21819.72 ❌
- **TP 4RR**: 21787.61 ❌
- **TP 15RR**: 21434.48 ❌
- **PnL**: -32.10 points (-1.0R)
- **MFE**: 73.20 points
- **MAE**: 35.83 points

### Trade #77 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 07:30:00
- **FVG 5m**: 21932.26 - 21946.44
- **Entrée**: 21962.16 @ 2025-01-15 08:43:00
- **Stop Loss**: 21921.30
- **Risk**: 40.86 points
- **TP 1RR**: 22003.03 ✅
- **TP 2RR**: 22043.89 ✅
- **TP 3RR**: 22084.76 ❌
- **TP 4RR**: 22125.62 ❌
- **TP 15RR**: 22575.13 ❌
- **PnL**: -40.86 points (-1.0R)
- **MFE**: 108.77 points
- **MAE**: 47.68 points

### Trade #78 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 07:30:00
- **FVG 5m**: 21932.26 - 21946.44
- **Entrée**: 21962.16 @ 2025-01-15 08:43:00
- **Stop Loss**: 21921.30
- **Risk**: 40.86 points
- **TP 1RR**: 22003.03 ✅
- **TP 2RR**: 22043.89 ✅
- **TP 3RR**: 22084.76 ❌
- **TP 4RR**: 22125.62 ❌
- **TP 15RR**: 22575.13 ❌
- **PnL**: -40.86 points (-1.0R)
- **MFE**: 108.77 points
- **MAE**: 47.68 points

### Trade #79 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 07:30:00
- **FVG 5m**: 21932.26 - 21946.44
- **Entrée**: 21962.16 @ 2025-01-15 08:43:00
- **Stop Loss**: 21921.30
- **Risk**: 40.86 points
- **TP 1RR**: 22003.03 ✅
- **TP 2RR**: 22043.89 ✅
- **TP 3RR**: 22084.76 ❌
- **TP 4RR**: 22125.62 ❌
- **TP 15RR**: 22575.13 ❌
- **PnL**: -40.86 points (-1.0R)
- **MFE**: 108.77 points
- **MAE**: 47.68 points

### Trade #80 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 08:45:00
- **FVG 5m**: 21976.60 - 21986.65
- **Entrée**: 21955.46 @ 2025-01-15 10:31:00
- **Stop Loss**: 21997.64
- **Risk**: 42.18 points
- **TP 1RR**: 21913.28 ✅
- **TP 2RR**: 21871.10 ❌
- **TP 3RR**: 21828.92 ❌
- **TP 4RR**: 21786.74 ❌
- **TP 15RR**: 21322.76 ❌
- **PnL**: -42.18 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 46.65 points

### Trade #81 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 09:00:00
- **FVG 5m**: 21976.60 - 21986.65
- **Entrée**: 21955.46 @ 2025-01-15 10:31:00
- **Stop Loss**: 21997.64
- **Risk**: 42.18 points
- **TP 1RR**: 21913.28 ✅
- **TP 2RR**: 21871.10 ❌
- **TP 3RR**: 21828.92 ❌
- **TP 4RR**: 21786.74 ❌
- **TP 15RR**: 21322.76 ❌
- **PnL**: -42.18 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 46.65 points

### Trade #82 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 09:30:00
- **FVG 5m**: 21976.60 - 21986.65
- **Entrée**: 21955.46 @ 2025-01-15 10:31:00
- **Stop Loss**: 21997.64
- **Risk**: 42.18 points
- **TP 1RR**: 21913.28 ✅
- **TP 2RR**: 21871.10 ❌
- **TP 3RR**: 21828.92 ❌
- **TP 4RR**: 21786.74 ❌
- **TP 15RR**: 21322.76 ❌
- **PnL**: -42.18 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 46.65 points

### Trade #83 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 09:45:00
- **FVG 5m**: 21976.60 - 21986.65
- **Entrée**: 21955.46 @ 2025-01-15 10:31:00
- **Stop Loss**: 21997.64
- **Risk**: 42.18 points
- **TP 1RR**: 21913.28 ✅
- **TP 2RR**: 21871.10 ❌
- **TP 3RR**: 21828.92 ❌
- **TP 4RR**: 21786.74 ❌
- **TP 15RR**: 21322.76 ❌
- **PnL**: -42.18 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 46.65 points

### Trade #84 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 23:30:00
- **FVG 5m**: 22038.20 - 22050.83
- **Entrée**: 22060.10 @ 2025-01-16 00:13:00
- **Stop Loss**: 22027.18
- **Risk**: 32.93 points
- **TP 1RR**: 22093.03 ✅
- **TP 2RR**: 22125.96 ✅
- **TP 3RR**: 22158.89 ✅
- **TP 4RR**: 22191.81 ✅
- **TP 15RR**: 22554.01 ❌
- **PnL**: -32.93 points (-1.0R)
- **MFE**: 175.01 points
- **MAE**: 57.73 points

### Trade #85 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 00:00:00
- **FVG 5m**: 22038.20 - 22050.83
- **Entrée**: 22060.10 @ 2025-01-16 00:13:00
- **Stop Loss**: 22027.18
- **Risk**: 32.93 points
- **TP 1RR**: 22093.03 ✅
- **TP 2RR**: 22125.96 ✅
- **TP 3RR**: 22158.89 ✅
- **TP 4RR**: 22191.81 ✅
- **TP 15RR**: 22554.01 ❌
- **PnL**: -32.93 points (-1.0R)
- **MFE**: 175.01 points
- **MAE**: 57.73 points

### Trade #86 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 02:00:00
- **FVG 5m**: 22189.23 - 22205.21
- **Entrée**: 22174.54 @ 2025-01-16 03:03:00
- **Stop Loss**: 22216.32
- **Risk**: 41.77 points
- **TP 1RR**: 22132.77 ✅
- **TP 2RR**: 22090.99 ✅
- **TP 3RR**: 22049.22 ✅
- **TP 4RR**: 22007.45 ✅
- **TP 15RR**: 21547.93 ❌
- **PnL**: -41.77 points (-1.0R)
- **MFE**: 346.66 points
- **MAE**: 49.49 points

### Trade #87 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 06:45:00
- **FVG 5m**: 22117.07 - 22153.15
- **Entrée**: 22114.75 @ 2025-01-16 08:31:00
- **Stop Loss**: 22164.23
- **Risk**: 49.48 points
- **TP 1RR**: 22065.27 ✅
- **TP 2RR**: 22015.79 ✅
- **TP 3RR**: 21966.31 ✅
- **TP 4RR**: 21916.83 ✅
- **TP 15RR**: 21372.54 ❌
- **PnL**: -49.48 points (-1.0R)
- **MFE**: 286.87 points
- **MAE**: 50.78 points

### Trade #88 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 06:45:00
- **FVG 5m**: 22117.07 - 22153.15
- **Entrée**: 22114.75 @ 2025-01-16 08:31:00
- **Stop Loss**: 22164.23
- **Risk**: 49.48 points
- **TP 1RR**: 22065.27 ✅
- **TP 2RR**: 22015.79 ✅
- **TP 3RR**: 21966.31 ✅
- **TP 4RR**: 21916.83 ✅
- **TP 15RR**: 21372.54 ❌
- **PnL**: -49.48 points (-1.0R)
- **MFE**: 286.87 points
- **MAE**: 50.78 points

### Trade #89 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 06:45:00
- **FVG 5m**: 22117.07 - 22153.15
- **Entrée**: 22114.75 @ 2025-01-16 08:31:00
- **Stop Loss**: 22164.23
- **Risk**: 49.48 points
- **TP 1RR**: 22065.27 ✅
- **TP 2RR**: 22015.79 ✅
- **TP 3RR**: 21966.31 ✅
- **TP 4RR**: 21916.83 ✅
- **TP 15RR**: 21372.54 ❌
- **PnL**: -49.48 points (-1.0R)
- **MFE**: 286.87 points
- **MAE**: 50.78 points

### Trade #90 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 07:15:00
- **FVG 5m**: 22135.11 - 22137.43
- **Entrée**: 22143.36 @ 2025-01-16 08:13:00
- **Stop Loss**: 22124.04
- **Risk**: 19.32 points
- **TP 1RR**: 22162.67 ✅
- **TP 2RR**: 22181.99 ❌
- **TP 3RR**: 22201.30 ❌
- **TP 4RR**: 22220.62 ❌
- **TP 15RR**: 22433.08 ❌
- **PnL**: -19.32 points (-1.0R)
- **MFE**: 22.68 points
- **MAE**: 28.87 points

### Trade #91 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 09:00:00
- **FVG 5m**: 22053.15 - 22079.18
- **Entrée**: 22088.20 @ 2025-01-16 09:59:00
- **Stop Loss**: 22042.12
- **Risk**: 46.08 points
- **TP 1RR**: 22134.28 ✅
- **TP 2RR**: 22180.36 ❌
- **TP 3RR**: 22226.44 ❌
- **TP 4RR**: 22272.52 ❌
- **TP 15RR**: 22779.39 ❌
- **PnL**: -46.08 points (-1.0R)
- **MFE**: 51.55 points
- **MAE**: 55.93 points

### Trade #92 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 09:45:00
- **FVG 5m**: 22053.15 - 22079.18
- **Entrée**: 22088.20 @ 2025-01-16 09:59:00
- **Stop Loss**: 22042.12
- **Risk**: 46.08 points
- **TP 1RR**: 22134.28 ✅
- **TP 2RR**: 22180.36 ❌
- **TP 3RR**: 22226.44 ❌
- **TP 4RR**: 22272.52 ❌
- **TP 15RR**: 22779.39 ❌
- **PnL**: -46.08 points (-1.0R)
- **MFE**: 51.55 points
- **MAE**: 55.93 points

### Trade #93 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 10:30:00
- **FVG 5m**: 22041.03 - 22052.11
- **Entrée**: 22062.42 @ 2025-01-16 10:58:00
- **Stop Loss**: 22030.01
- **Risk**: 32.41 points
- **TP 1RR**: 22094.84 ❌
- **TP 2RR**: 22127.25 ❌
- **TP 3RR**: 22159.66 ❌
- **TP 4RR**: 22192.08 ❌
- **TP 15RR**: 22548.62 ❌
- **PnL**: -32.41 points (-1.0R)
- **MFE**: 27.06 points
- **MAE**: 34.54 points

### Trade #94 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 13:00:00
- **FVG 5m**: 22022.73 - 22030.46
- **Entrée**: 22030.98 @ 2025-01-16 13:56:00
- **Stop Loss**: 22011.72
- **Risk**: 19.26 points
- **TP 1RR**: 22050.24 ✅
- **TP 2RR**: 22069.50 ❌
- **TP 3RR**: 22088.76 ❌
- **TP 4RR**: 22108.02 ❌
- **TP 15RR**: 22319.87 ❌
- **PnL**: -19.26 points (-1.0R)
- **MFE**: 27.32 points
- **MAE**: 26.29 points

### Trade #95 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 19:30:00
- **FVG 5m**: 21915.00 - 21922.47
- **Entrée**: 21923.50 @ 2025-01-16 19:43:00
- **Stop Loss**: 21904.04
- **Risk**: 19.46 points
- **TP 1RR**: 21942.96 ✅
- **TP 2RR**: 21962.43 ✅
- **TP 3RR**: 21981.89 ✅
- **TP 4RR**: 22001.35 ✅
- **TP 15RR**: 22215.45 ✅
- **PnL**: 291.94 points (15.0R)
- **MFE**: 300.53 points
- **MAE**: 19.07 points

### Trade #96 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-17 08:15:00
- **FVG 5m**: 22199.03 - 22208.05
- **Entrée**: 22209.85 @ 2025-01-17 09:32:00
- **Stop Loss**: 22187.93
- **Risk**: 21.92 points
- **TP 1RR**: 22231.78 ✅
- **TP 2RR**: 22253.70 ✅
- **TP 3RR**: 22275.63 ✅
- **TP 4RR**: 22297.55 ✅
- **TP 15RR**: 22538.72 ❌
- **PnL**: -21.92 points (-1.0R)
- **MFE**: 243.31 points
- **MAE**: 41.75 points

### Trade #97 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-17 08:15:00
- **FVG 5m**: 22199.03 - 22208.05
- **Entrée**: 22209.85 @ 2025-01-17 09:32:00
- **Stop Loss**: 22187.93
- **Risk**: 21.92 points
- **TP 1RR**: 22231.78 ✅
- **TP 2RR**: 22253.70 ✅
- **TP 3RR**: 22275.63 ✅
- **TP 4RR**: 22297.55 ✅
- **TP 15RR**: 22538.72 ❌
- **PnL**: -21.92 points (-1.0R)
- **MFE**: 243.31 points
- **MAE**: 41.75 points

### Trade #98 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-17 08:30:00
- **FVG 5m**: 22199.03 - 22217.33
- **Entrée**: 22192.84 @ 2025-01-17 09:21:00
- **Stop Loss**: 22228.44
- **Risk**: 35.59 points
- **TP 1RR**: 22157.25 ✅
- **TP 2RR**: 22121.65 ❌
- **TP 3RR**: 22086.06 ❌
- **TP 4RR**: 22050.46 ❌
- **TP 15RR**: 21658.93 ❌
- **PnL**: -35.59 points (-1.0R)
- **MFE**: 46.39 points
- **MAE**: 39.95 points

### Trade #99 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-17 08:30:00
- **FVG 5m**: 22199.03 - 22217.33
- **Entrée**: 22192.84 @ 2025-01-17 09:21:00
- **Stop Loss**: 22228.44
- **Risk**: 35.59 points
- **TP 1RR**: 22157.25 ✅
- **TP 2RR**: 22121.65 ❌
- **TP 3RR**: 22086.06 ❌
- **TP 4RR**: 22050.46 ❌
- **TP 15RR**: 21658.93 ❌
- **PnL**: -35.59 points (-1.0R)
- **MFE**: 46.39 points
- **MAE**: 39.95 points

### Trade #100 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-17 12:00:00
- **FVG 5m**: 22317.85 - 22324.55
- **Entrée**: 22326.87 @ 2025-01-17 12:12:00
- **Stop Loss**: 22306.69
- **Risk**: 20.18 points
- **TP 1RR**: 22347.05 ❌
- **TP 2RR**: 22367.23 ❌
- **TP 3RR**: 22387.41 ❌
- **TP 4RR**: 22407.59 ❌
- **TP 15RR**: 22629.57 ❌
- **PnL**: -20.18 points (-1.0R)
- **MFE**: 16.24 points
- **MAE**: 26.03 points

### Trade #101 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 06:15:00
- **FVG 5m**: 22345.94 - 22351.35
- **Entrée**: 22333.57 @ 2025-01-20 08:14:00
- **Stop Loss**: 22362.53
- **Risk**: 28.96 points
- **TP 1RR**: 22304.61 ❌
- **TP 2RR**: 22275.65 ❌
- **TP 3RR**: 22246.69 ❌
- **TP 4RR**: 22217.73 ❌
- **TP 15RR**: 21899.17 ❌
- **PnL**: -28.96 points (-1.0R)
- **MFE**: 3.61 points
- **MAE**: 38.92 points

### Trade #102 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 07:30:00
- **FVG 5m**: 22325.06 - 22338.98
- **Entrée**: 22344.65 @ 2025-01-20 07:53:00
- **Stop Loss**: 22313.90
- **Risk**: 30.75 points
- **TP 1RR**: 22375.40 ✅
- **TP 2RR**: 22406.15 ✅
- **TP 3RR**: 22436.90 ✅
- **TP 4RR**: 22467.65 ❌
- **TP 15RR**: 22805.91 ❌
- **PnL**: -30.75 points (-1.0R)
- **MFE**: 108.51 points
- **MAE**: 33.25 points

### Trade #103 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 07:45:00
- **FVG 5m**: 22348.00 - 22356.51
- **Entrée**: 22362.69 @ 2025-01-20 07:58:00
- **Stop Loss**: 22336.83
- **Risk**: 25.87 points
- **TP 1RR**: 22388.56 ❌
- **TP 2RR**: 22414.42 ❌
- **TP 3RR**: 22440.29 ❌
- **TP 4RR**: 22466.15 ❌
- **TP 15RR**: 22750.67 ❌
- **PnL**: -25.87 points (-1.0R)
- **MFE**: 13.14 points
- **MAE**: 29.38 points

### Trade #104 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 08:00:00
- **FVG 5m**: 22345.94 - 22351.35
- **Entrée**: 22333.57 @ 2025-01-20 08:14:00
- **Stop Loss**: 22362.53
- **Risk**: 28.96 points
- **TP 1RR**: 22304.61 ❌
- **TP 2RR**: 22275.65 ❌
- **TP 3RR**: 22246.69 ❌
- **TP 4RR**: 22217.73 ❌
- **TP 15RR**: 21899.17 ❌
- **PnL**: -28.96 points (-1.0R)
- **MFE**: 3.61 points
- **MAE**: 38.92 points

### Trade #105 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 08:00:00
- **FVG 5m**: 22345.94 - 22351.35
- **Entrée**: 22333.57 @ 2025-01-20 08:14:00
- **Stop Loss**: 22362.53
- **Risk**: 28.96 points
- **TP 1RR**: 22304.61 ❌
- **TP 2RR**: 22275.65 ❌
- **TP 3RR**: 22246.69 ❌
- **TP 4RR**: 22217.73 ❌
- **TP 15RR**: 21899.17 ❌
- **PnL**: -28.96 points (-1.0R)
- **MFE**: 3.61 points
- **MAE**: 38.92 points

### Trade #106 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 11:15:00
- **FVG 5m**: 22391.56 - 22399.29
- **Entrée**: 22407.54 @ 2025-01-20 17:16:00
- **Stop Loss**: 22380.36
- **Risk**: 27.18 points
- **TP 1RR**: 22434.72 ❌
- **TP 2RR**: 22461.89 ❌
- **TP 3RR**: 22489.07 ❌
- **TP 4RR**: 22516.24 ❌
- **TP 15RR**: 22815.18 ❌
- **PnL**: -27.18 points (-1.0R)
- **MFE**: 3.61 points
- **MAE**: 28.35 points

### Trade #107 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 18:15:00
- **FVG 5m**: 22369.14 - 22382.28
- **Entrée**: 22368.88 @ 2025-01-20 18:38:00
- **Stop Loss**: 22393.47
- **Risk**: 24.59 points
- **TP 1RR**: 22344.29 ✅
- **TP 2RR**: 22319.69 ✅
- **TP 3RR**: 22295.10 ✅
- **TP 4RR**: 22270.50 ✅
- **TP 15RR**: 21999.97 ❌
- **PnL**: -24.59 points (-1.0R)
- **MFE**: 329.14 points
- **MAE**: 27.58 points

### Trade #108 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 19:00:00
- **FVG 5m**: 22274.29 - 22290.53
- **Entrée**: 22293.88 @ 2025-01-20 21:12:00
- **Stop Loss**: 22263.15
- **Risk**: 30.73 points
- **TP 1RR**: 22324.60 ❌
- **TP 2RR**: 22355.33 ❌
- **TP 3RR**: 22386.05 ❌
- **TP 4RR**: 22416.78 ❌
- **TP 15RR**: 22754.76 ❌
- **PnL**: -30.73 points (-1.0R)
- **MFE**: 24.23 points
- **MAE**: 38.15 points

### Trade #109 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 19:00:00
- **FVG 5m**: 22274.29 - 22290.53
- **Entrée**: 22293.88 @ 2025-01-20 21:12:00
- **Stop Loss**: 22263.15
- **Risk**: 30.73 points
- **TP 1RR**: 22324.60 ❌
- **TP 2RR**: 22355.33 ❌
- **TP 3RR**: 22386.05 ❌
- **TP 4RR**: 22416.78 ❌
- **TP 15RR**: 22754.76 ❌
- **PnL**: -30.73 points (-1.0R)
- **MFE**: 24.23 points
- **MAE**: 38.15 points

### Trade #110 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 19:00:00
- **FVG 5m**: 22274.29 - 22290.53
- **Entrée**: 22293.88 @ 2025-01-20 21:12:00
- **Stop Loss**: 22263.15
- **Risk**: 30.73 points
- **TP 1RR**: 22324.60 ❌
- **TP 2RR**: 22355.33 ❌
- **TP 3RR**: 22386.05 ❌
- **TP 4RR**: 22416.78 ❌
- **TP 15RR**: 22754.76 ❌
- **PnL**: -30.73 points (-1.0R)
- **MFE**: 24.23 points
- **MAE**: 38.15 points

### Trade #111 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 19:00:00
- **FVG 5m**: 22274.29 - 22290.53
- **Entrée**: 22293.88 @ 2025-01-20 21:12:00
- **Stop Loss**: 22263.15
- **Risk**: 30.73 points
- **TP 1RR**: 22324.60 ❌
- **TP 2RR**: 22355.33 ❌
- **TP 3RR**: 22386.05 ❌
- **TP 4RR**: 22416.78 ❌
- **TP 15RR**: 22754.76 ❌
- **PnL**: -30.73 points (-1.0R)
- **MFE**: 24.23 points
- **MAE**: 38.15 points

### Trade #112 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 22:00:00
- **FVG 5m**: 22266.81 - 22269.91
- **Entrée**: 22271.19 @ 2025-01-21 00:08:00
- **Stop Loss**: 22255.68
- **Risk**: 15.52 points
- **TP 1RR**: 22286.71 ✅
- **TP 2RR**: 22302.22 ❌
- **TP 3RR**: 22317.74 ❌
- **TP 4RR**: 22333.25 ❌
- **TP 15RR**: 22503.92 ❌
- **PnL**: -15.52 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 16.24 points

### Trade #113 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-21 09:15:00
- **FVG 5m**: 22304.19 - 22307.28
- **Entrée**: 22309.34 @ 2025-01-21 10:06:00
- **Stop Loss**: 22293.03
- **Risk**: 16.31 points
- **TP 1RR**: 22325.65 ✅
- **TP 2RR**: 22341.95 ❌
- **TP 3RR**: 22358.26 ❌
- **TP 4RR**: 22374.57 ❌
- **TP 15RR**: 22553.94 ❌
- **PnL**: -16.31 points (-1.0R)
- **MFE**: 17.53 points
- **MAE**: 19.59 points

### Trade #114 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-21 09:15:00
- **FVG 5m**: 22304.19 - 22307.28
- **Entrée**: 22309.34 @ 2025-01-21 10:06:00
- **Stop Loss**: 22293.03
- **Risk**: 16.31 points
- **TP 1RR**: 22325.65 ✅
- **TP 2RR**: 22341.95 ❌
- **TP 3RR**: 22358.26 ❌
- **TP 4RR**: 22374.57 ❌
- **TP 15RR**: 22553.94 ❌
- **PnL**: -16.31 points (-1.0R)
- **MFE**: 17.53 points
- **MAE**: 19.59 points

### Trade #115 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-21 10:00:00
- **FVG 5m**: 22299.03 - 22303.67
- **Entrée**: 22307.28 @ 2025-01-21 10:49:00
- **Stop Loss**: 22287.88
- **Risk**: 19.40 points
- **TP 1RR**: 22326.68 ✅
- **TP 2RR**: 22346.07 ✅
- **TP 3RR**: 22365.47 ✅
- **TP 4RR**: 22384.87 ✅
- **TP 15RR**: 22598.24 ✅
- **PnL**: 290.96 points (15.0R)
- **MFE**: 291.51 points
- **MAE**: 3.61 points

### Trade #116 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-21 13:00:00
- **FVG 5m**: 22419.91 - 22425.07
- **Entrée**: 22418.88 @ 2025-01-21 13:14:00
- **Stop Loss**: 22436.28
- **Risk**: 17.40 points
- **TP 1RR**: 22401.48 ✅
- **TP 2RR**: 22384.08 ✅
- **TP 3RR**: 22366.69 ❌
- **TP 4RR**: 22349.29 ❌
- **TP 15RR**: 22157.91 ❌
- **PnL**: -17.40 points (-1.0R)
- **MFE**: 50.00 points
- **MAE**: 30.41 points

### Trade #117 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-21 17:00:00
- **FVG 5m**: 22502.13 - 22510.64
- **Entrée**: 22501.62 @ 2025-01-21 19:01:00
- **Stop Loss**: 22521.89
- **Risk**: 20.28 points
- **TP 1RR**: 22481.34 ❌
- **TP 2RR**: 22461.06 ❌
- **TP 3RR**: 22440.79 ❌
- **TP 4RR**: 22420.51 ❌
- **TP 15RR**: 22197.47 ❌
- **PnL**: -20.28 points (-1.0R)
- **MFE**: 14.69 points
- **MAE**: 22.68 points

### Trade #118 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-22 00:45:00
- **FVG 5m**: 22534.86 - 22537.44
- **Entrée**: 22534.35 @ 2025-01-22 01:47:00
- **Stop Loss**: 22548.71
- **Risk**: 14.36 points
- **TP 1RR**: 22519.99 ❌
- **TP 2RR**: 22505.63 ❌
- **TP 3RR**: 22491.26 ❌
- **TP 4RR**: 22476.90 ❌
- **TP 15RR**: 22318.92 ❌
- **PnL**: -14.36 points (-1.0R)
- **MFE**: 11.60 points
- **MAE**: 17.01 points

### Trade #119 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 02:00:00
- **FVG 5m**: 22575.07 - 22583.32
- **Entrée**: 22574.56 @ 2025-01-23 02:31:00
- **Stop Loss**: 22594.61
- **Risk**: 20.05 points
- **TP 1RR**: 22554.50 ✅
- **TP 2RR**: 22534.45 ✅
- **TP 3RR**: 22514.39 ❌
- **TP 4RR**: 22494.34 ❌
- **TP 15RR**: 22273.73 ❌
- **PnL**: -20.05 points (-1.0R)
- **MFE**: 42.27 points
- **MAE**: 23.71 points

### Trade #120 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 02:45:00
- **FVG 5m**: 22546.72 - 22549.81
- **Entrée**: 22558.06 @ 2025-01-23 03:22:00
- **Stop Loss**: 22535.45
- **Risk**: 22.61 points
- **TP 1RR**: 22580.68 ✅
- **TP 2RR**: 22603.29 ✅
- **TP 3RR**: 22625.90 ✅
- **TP 4RR**: 22648.52 ✅
- **TP 15RR**: 22897.27 ❌
- **PnL**: -22.61 points (-1.0R)
- **MFE**: 203.87 points
- **MAE**: 24.74 points

### Trade #121 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 03:15:00
- **FVG 5m**: 22565.28 - 22569.66
- **Entrée**: 22571.72 @ 2025-01-23 05:42:00
- **Stop Loss**: 22554.00
- **Risk**: 17.73 points
- **TP 1RR**: 22589.45 ❌
- **TP 2RR**: 22607.17 ❌
- **TP 3RR**: 22624.90 ❌
- **TP 4RR**: 22642.63 ❌
- **TP 15RR**: 22837.61 ❌
- **PnL**: -17.73 points (-1.0R)
- **MFE**: 11.60 points
- **MAE**: 19.33 points

### Trade #122 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 07:00:00
- **FVG 5m**: 22569.40 - 22572.24
- **Entrée**: 22568.11 @ 2025-01-23 08:07:00
- **Stop Loss**: 22583.52
- **Risk**: 15.41 points
- **TP 1RR**: 22552.70 ✅
- **TP 2RR**: 22537.29 ❌
- **TP 3RR**: 22521.88 ❌
- **TP 4RR**: 22506.47 ❌
- **TP 15RR**: 22336.96 ❌
- **PnL**: -15.41 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 17.27 points

### Trade #123 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 07:30:00
- **FVG 5m**: 22569.40 - 22572.24
- **Entrée**: 22568.11 @ 2025-01-23 08:07:00
- **Stop Loss**: 22583.52
- **Risk**: 15.41 points
- **TP 1RR**: 22552.70 ✅
- **TP 2RR**: 22537.29 ❌
- **TP 3RR**: 22521.88 ❌
- **TP 4RR**: 22506.47 ❌
- **TP 15RR**: 22336.96 ❌
- **PnL**: -15.41 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 17.27 points

### Trade #124 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 10:00:00
- **FVG 5m**: 22614.25 - 22623.53
- **Entrée**: 22628.42 @ 2025-01-23 10:29:00
- **Stop Loss**: 22602.94
- **Risk**: 25.48 points
- **TP 1RR**: 22653.91 ❌
- **TP 2RR**: 22679.39 ❌
- **TP 3RR**: 22704.87 ❌
- **TP 4RR**: 22730.36 ❌
- **TP 15RR**: 23010.67 ❌
- **PnL**: -25.48 points (-1.0R)
- **MFE**: 23.45 points
- **MAE**: 29.38 points

### Trade #125 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 12:30:00
- **FVG 5m**: 22615.80 - 22625.07
- **Entrée**: 22615.28 @ 2025-01-23 13:07:00
- **Stop Loss**: 22636.39
- **Risk**: 21.11 points
- **TP 1RR**: 22594.17 ❌
- **TP 2RR**: 22573.07 ❌
- **TP 3RR**: 22551.96 ❌
- **TP 4RR**: 22530.85 ❌
- **TP 15RR**: 22298.68 ❌
- **PnL**: -21.11 points (-1.0R)
- **MFE**: 12.63 points
- **MAE**: 23.45 points

### Trade #126 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 12:30:00
- **FVG 5m**: 22615.80 - 22625.07
- **Entrée**: 22615.28 @ 2025-01-23 13:07:00
- **Stop Loss**: 22636.39
- **Risk**: 21.11 points
- **TP 1RR**: 22594.17 ❌
- **TP 2RR**: 22573.07 ❌
- **TP 3RR**: 22551.96 ❌
- **TP 4RR**: 22530.85 ❌
- **TP 15RR**: 22298.68 ❌
- **PnL**: -21.11 points (-1.0R)
- **MFE**: 12.63 points
- **MAE**: 23.45 points

### Trade #127 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 12:30:00
- **FVG 5m**: 22615.80 - 22625.07
- **Entrée**: 22615.28 @ 2025-01-23 13:07:00
- **Stop Loss**: 22636.39
- **Risk**: 21.11 points
- **TP 1RR**: 22594.17 ❌
- **TP 2RR**: 22573.07 ❌
- **TP 3RR**: 22551.96 ❌
- **TP 4RR**: 22530.85 ❌
- **TP 15RR**: 22298.68 ❌
- **PnL**: -21.11 points (-1.0R)
- **MFE**: 12.63 points
- **MAE**: 23.45 points

### Trade #128 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 22:15:00
- **FVG 5m**: 22686.16 - 22688.99
- **Entrée**: 22683.84 @ 2025-01-23 23:54:00
- **Stop Loss**: 22700.34
- **Risk**: 16.50 points
- **TP 1RR**: 22667.34 ✅
- **TP 2RR**: 22650.84 ❌
- **TP 3RR**: 22634.34 ❌
- **TP 4RR**: 22617.84 ❌
- **TP 15RR**: 22436.35 ❌
- **PnL**: -16.50 points (-1.0R)
- **MFE**: 31.70 points
- **MAE**: 17.01 points

### Trade #129 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 02:00:00
- **FVG 5m**: 22668.12 - 22676.11
- **Entrée**: 22676.36 @ 2025-01-24 03:02:00
- **Stop Loss**: 22656.78
- **Risk**: 19.58 points
- **TP 1RR**: 22695.95 ✅
- **TP 2RR**: 22715.53 ✅
- **TP 3RR**: 22735.11 ✅
- **TP 4RR**: 22754.69 ✅
- **TP 15RR**: 22970.09 ❌
- **PnL**: -19.58 points (-1.0R)
- **MFE**: 85.57 points
- **MAE**: 21.91 points

### Trade #130 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 09:00:00
- **FVG 5m**: 22704.72 - 22707.29
- **Entrée**: 22702.91 @ 2025-01-24 10:54:00
- **Stop Loss**: 22718.65
- **Risk**: 15.74 points
- **TP 1RR**: 22687.18 ✅
- **TP 2RR**: 22671.44 ✅
- **TP 3RR**: 22655.71 ✅
- **TP 4RR**: 22639.97 ✅
- **TP 15RR**: 22466.88 ✅
- **PnL**: 236.03 points (15.0R)
- **MFE**: 340.99 points
- **MAE**: 1.80 points

### Trade #131 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 09:00:00
- **FVG 5m**: 22704.72 - 22707.29
- **Entrée**: 22702.91 @ 2025-01-24 10:54:00
- **Stop Loss**: 22718.65
- **Risk**: 15.74 points
- **TP 1RR**: 22687.18 ✅
- **TP 2RR**: 22671.44 ✅
- **TP 3RR**: 22655.71 ✅
- **TP 4RR**: 22639.97 ✅
- **TP 15RR**: 22466.88 ✅
- **PnL**: 236.03 points (15.0R)
- **MFE**: 340.99 points
- **MAE**: 1.80 points

### Trade #132 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 09:00:00
- **FVG 5m**: 22704.72 - 22707.29
- **Entrée**: 22702.91 @ 2025-01-24 10:54:00
- **Stop Loss**: 22718.65
- **Risk**: 15.74 points
- **TP 1RR**: 22687.18 ✅
- **TP 2RR**: 22671.44 ✅
- **TP 3RR**: 22655.71 ✅
- **TP 4RR**: 22639.97 ✅
- **TP 15RR**: 22466.88 ✅
- **PnL**: 236.03 points (15.0R)
- **MFE**: 340.99 points
- **MAE**: 1.80 points

### Trade #133 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 10:00:00
- **FVG 5m**: 22679.46 - 22683.58
- **Entrée**: 22684.10 @ 2025-01-24 10:24:00
- **Stop Loss**: 22668.12
- **Risk**: 15.98 points
- **TP 1RR**: 22700.08 ✅
- **TP 2RR**: 22716.06 ✅
- **TP 3RR**: 22732.03 ❌
- **TP 4RR**: 22748.01 ❌
- **TP 15RR**: 22923.78 ❌
- **PnL**: -15.98 points (-1.0R)
- **MFE**: 34.02 points
- **MAE**: 22.17 points

### Trade #134 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 10:45:00
- **FVG 5m**: 22674.30 - 22702.65
- **Entrée**: 22667.34 @ 2025-01-24 10:58:00
- **Stop Loss**: 22714.01
- **Risk**: 46.66 points
- **TP 1RR**: 22620.68 ✅
- **TP 2RR**: 22574.02 ✅
- **TP 3RR**: 22527.36 ✅
- **TP 4RR**: 22480.70 ✅
- **TP 15RR**: 21967.41 ✅
- **PnL**: 699.93 points (15.0R)
- **MFE**: 714.72 points
- **MAE**: 22.42 points

### Trade #135 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 12:30:00
- **FVG 5m**: 22568.11 - 22573.27
- **Entrée**: 22550.07 @ 2025-01-24 12:56:00
- **Stop Loss**: 22584.55
- **Risk**: 34.48 points
- **TP 1RR**: 22515.59 ❌
- **TP 2RR**: 22481.10 ❌
- **TP 3RR**: 22446.62 ❌
- **TP 4RR**: 22412.14 ❌
- **TP 15RR**: 22032.82 ❌
- **PnL**: -34.48 points (-1.0R)
- **MFE**: 29.64 points
- **MAE**: 37.11 points

### Trade #136 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 13:00:00
- **FVG 5m**: 22558.83 - 22567.86
- **Entrée**: 22571.21 @ 2025-01-24 14:52:00
- **Stop Loss**: 22547.56
- **Risk**: 23.65 points
- **TP 1RR**: 22594.86 ✅
- **TP 2RR**: 22618.51 ❌
- **TP 3RR**: 22642.16 ❌
- **TP 4RR**: 22665.81 ❌
- **TP 15RR**: 22925.97 ❌
- **PnL**: -23.65 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 209.29 points

### Trade #137 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 13:15:00
- **FVG 5m**: 22558.83 - 22567.86
- **Entrée**: 22571.21 @ 2025-01-24 14:52:00
- **Stop Loss**: 22547.56
- **Risk**: 23.65 points
- **TP 1RR**: 22594.86 ✅
- **TP 2RR**: 22618.51 ❌
- **TP 3RR**: 22642.16 ❌
- **TP 4RR**: 22665.81 ❌
- **TP 15RR**: 22925.97 ❌
- **PnL**: -23.65 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 209.29 points

### Trade #138 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 14:00:00
- **FVG 5m**: 22558.83 - 22567.86
- **Entrée**: 22571.21 @ 2025-01-24 14:52:00
- **Stop Loss**: 22547.56
- **Risk**: 23.65 points
- **TP 1RR**: 22594.86 ✅
- **TP 2RR**: 22618.51 ❌
- **TP 3RR**: 22642.16 ❌
- **TP 4RR**: 22665.81 ❌
- **TP 15RR**: 22925.97 ❌
- **PnL**: -23.65 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 209.29 points

### Trade #139 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 14:45:00
- **FVG 5m**: 22329.96 - 22336.15
- **Entrée**: 22339.50 @ 2025-01-26 17:47:00
- **Stop Loss**: 22318.79
- **Risk**: 20.70 points
- **TP 1RR**: 22360.20 ❌
- **TP 2RR**: 22380.90 ❌
- **TP 3RR**: 22401.60 ❌
- **TP 4RR**: 22422.30 ❌
- **TP 15RR**: 22650.02 ❌
- **PnL**: -20.70 points (-1.0R)
- **MFE**: 13.66 points
- **MAE**: 21.39 points

### Trade #140 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-26 19:30:00
- **FVG 5m**: 22181.50 - 22188.72
- **Entrée**: 22189.23 @ 2025-01-26 20:23:00
- **Stop Loss**: 22170.41
- **Risk**: 18.82 points
- **TP 1RR**: 22208.06 ✅
- **TP 2RR**: 22226.88 ✅
- **TP 3RR**: 22245.70 ❌
- **TP 4RR**: 22264.53 ❌
- **TP 15RR**: 22471.58 ❌
- **PnL**: -18.82 points (-1.0R)
- **MFE**: 41.50 points
- **MAE**: 20.62 points

### Trade #141 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 00:30:00
- **FVG 5m**: 22047.99 - 22050.31
- **Entrée**: 22046.70 @ 2025-01-27 01:06:00
- **Stop Loss**: 22061.34
- **Risk**: 14.63 points
- **TP 1RR**: 22032.07 ✅
- **TP 2RR**: 22017.43 ✅
- **TP 3RR**: 22002.80 ✅
- **TP 4RR**: 21988.17 ✅
- **TP 15RR**: 21827.20 ✅
- **PnL**: 219.50 points (15.0R)
- **MFE**: 224.49 points
- **MAE**: 3.61 points

### Trade #142 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 01:45:00
- **FVG 5m**: 21969.64 - 21991.55
- **Entrée**: 21962.68 @ 2025-01-27 01:56:00
- **Stop Loss**: 22002.54
- **Risk**: 39.86 points
- **TP 1RR**: 21922.82 ✅
- **TP 2RR**: 21882.95 ✅
- **TP 3RR**: 21843.09 ✅
- **TP 4RR**: 21803.23 ✅
- **TP 15RR**: 21364.74 ❌
- **PnL**: -39.86 points (-1.0R)
- **MFE**: 555.95 points
- **MAE**: 53.35 points

### Trade #143 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 02:00:00
- **FVG 5m**: 21919.38 - 21926.85
- **Entrée**: 21909.84 @ 2025-01-27 02:12:00
- **Stop Loss**: 21937.82
- **Risk**: 27.97 points
- **TP 1RR**: 21881.87 ✅
- **TP 2RR**: 21853.89 ✅
- **TP 3RR**: 21825.92 ✅
- **TP 4RR**: 21797.94 ✅
- **TP 15RR**: 21490.23 ✅
- **PnL**: 419.62 points (15.0R)
- **MFE**: 441.00 points
- **MAE**: 23.71 points

### Trade #144 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 03:45:00
- **FVG 5m**: 21804.42 - 21810.10
- **Entrée**: 21791.28 @ 2025-01-27 04:02:00
- **Stop Loss**: 21821.00
- **Risk**: 29.72 points
- **TP 1RR**: 21761.56 ✅
- **TP 2RR**: 21731.84 ✅
- **TP 3RR**: 21702.12 ✅
- **TP 4RR**: 21672.40 ✅
- **TP 15RR**: 21345.48 ❌
- **PnL**: -29.72 points (-1.0R)
- **MFE**: 384.55 points
- **MAE**: 34.28 points

### Trade #145 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:00:00
- **FVG 5m**: 21744.89 - 21765.76
- **Entrée**: 21741.54 @ 2025-01-27 04:16:00
- **Stop Loss**: 21776.65
- **Risk**: 35.11 points
- **TP 1RR**: 21706.43 ✅
- **TP 2RR**: 21671.31 ✅
- **TP 3RR**: 21636.20 ✅
- **TP 4RR**: 21601.09 ✅
- **TP 15RR**: 21214.88 ❌
- **PnL**: -35.11 points (-1.0R)
- **MFE**: 334.81 points
- **MAE**: 36.08 points

### Trade #146 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:00:00
- **FVG 5m**: 21744.89 - 21765.76
- **Entrée**: 21741.54 @ 2025-01-27 04:16:00
- **Stop Loss**: 21776.65
- **Risk**: 35.11 points
- **TP 1RR**: 21706.43 ✅
- **TP 2RR**: 21671.31 ✅
- **TP 3RR**: 21636.20 ✅
- **TP 4RR**: 21601.09 ✅
- **TP 15RR**: 21214.88 ❌
- **PnL**: -35.11 points (-1.0R)
- **MFE**: 334.81 points
- **MAE**: 36.08 points

### Trade #147 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:30:00
- **FVG 5m**: 21610.60 - 21642.05
- **Entrée**: 21594.11 @ 2025-01-27 04:44:00
- **Stop Loss**: 21652.87
- **Risk**: 58.76 points
- **TP 1RR**: 21535.35 ✅
- **TP 2RR**: 21476.59 ✅
- **TP 3RR**: 21417.82 ✅
- **TP 4RR**: 21359.06 ❌
- **TP 15RR**: 20712.69 ❌
- **PnL**: -58.76 points (-1.0R)
- **MFE**: 187.38 points
- **MAE**: 67.01 points

### Trade #148 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:30:00
- **FVG 5m**: 21610.60 - 21642.05
- **Entrée**: 21594.11 @ 2025-01-27 04:44:00
- **Stop Loss**: 21652.87
- **Risk**: 58.76 points
- **TP 1RR**: 21535.35 ✅
- **TP 2RR**: 21476.59 ✅
- **TP 3RR**: 21417.82 ✅
- **TP 4RR**: 21359.06 ❌
- **TP 15RR**: 20712.69 ❌
- **PnL**: -58.76 points (-1.0R)
- **MFE**: 187.38 points
- **MAE**: 67.01 points

### Trade #149 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:30:00
- **FVG 5m**: 21610.60 - 21642.05
- **Entrée**: 21594.11 @ 2025-01-27 04:44:00
- **Stop Loss**: 21652.87
- **Risk**: 58.76 points
- **TP 1RR**: 21535.35 ✅
- **TP 2RR**: 21476.59 ✅
- **TP 3RR**: 21417.82 ✅
- **TP 4RR**: 21359.06 ❌
- **TP 15RR**: 20712.69 ❌
- **PnL**: -58.76 points (-1.0R)
- **MFE**: 187.38 points
- **MAE**: 67.01 points

### Trade #150 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 04:45:00
- **FVG 5m**: 21616.27 - 21635.09
- **Entrée**: 21643.08 @ 2025-01-27 05:34:00
- **Stop Loss**: 21605.47
- **Risk**: 37.61 points
- **TP 1RR**: 21680.69 ✅
- **TP 2RR**: 21718.31 ✅
- **TP 3RR**: 21755.92 ✅
- **TP 4RR**: 21793.53 ✅
- **TP 15RR**: 22207.28 ✅
- **PnL**: 564.20 points (15.0R)
- **MFE**: 568.06 points
- **MAE**: 22.17 points

### Trade #151 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 05:00:00
- **FVG 5m**: 21616.27 - 21635.09
- **Entrée**: 21643.08 @ 2025-01-27 05:34:00
- **Stop Loss**: 21605.47
- **Risk**: 37.61 points
- **TP 1RR**: 21680.69 ✅
- **TP 2RR**: 21718.31 ✅
- **TP 3RR**: 21755.92 ✅
- **TP 4RR**: 21793.53 ✅
- **TP 15RR**: 22207.28 ✅
- **PnL**: 564.20 points (15.0R)
- **MFE**: 568.06 points
- **MAE**: 22.17 points

### Trade #152 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 08:30:00
- **FVG 5m**: 21979.17 - 22011.13
- **Entrée**: 22011.39 @ 2025-01-27 09:28:00
- **Stop Loss**: 21968.18
- **Risk**: 43.21 points
- **TP 1RR**: 22054.60 ✅
- **TP 2RR**: 22097.81 ❌
- **TP 3RR**: 22141.01 ❌
- **TP 4RR**: 22184.22 ❌
- **TP 15RR**: 22659.50 ❌
- **PnL**: -43.21 points (-1.0R)
- **MFE**: 70.36 points
- **MAE**: 50.52 points

### Trade #153 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 08:30:00
- **FVG 5m**: 21979.17 - 22011.13
- **Entrée**: 22011.39 @ 2025-01-27 09:28:00
- **Stop Loss**: 21968.18
- **Risk**: 43.21 points
- **TP 1RR**: 22054.60 ✅
- **TP 2RR**: 22097.81 ❌
- **TP 3RR**: 22141.01 ❌
- **TP 4RR**: 22184.22 ❌
- **TP 15RR**: 22659.50 ❌
- **PnL**: -43.21 points (-1.0R)
- **MFE**: 70.36 points
- **MAE**: 50.52 points

### Trade #154 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 08:45:00
- **FVG 5m**: 21979.17 - 22011.13
- **Entrée**: 22011.39 @ 2025-01-27 09:28:00
- **Stop Loss**: 21968.18
- **Risk**: 43.21 points
- **TP 1RR**: 22054.60 ✅
- **TP 2RR**: 22097.81 ❌
- **TP 3RR**: 22141.01 ❌
- **TP 4RR**: 22184.22 ❌
- **TP 15RR**: 22659.50 ❌
- **PnL**: -43.21 points (-1.0R)
- **MFE**: 70.36 points
- **MAE**: 50.52 points

### Trade #155 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 09:45:00
- **FVG 5m**: 21986.65 - 21993.35
- **Entrée**: 21978.92 @ 2025-01-27 09:57:00
- **Stop Loss**: 22004.35
- **Risk**: 25.43 points
- **TP 1RR**: 21953.49 ✅
- **TP 2RR**: 21928.06 ✅
- **TP 3RR**: 21902.63 ✅
- **TP 4RR**: 21877.20 ✅
- **TP 15RR**: 21597.46 ❌
- **PnL**: -25.43 points (-1.0R)
- **MFE**: 230.68 points
- **MAE**: 39.95 points

### Trade #156 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 09:45:00
- **FVG 5m**: 21986.65 - 21993.35
- **Entrée**: 21978.92 @ 2025-01-27 09:57:00
- **Stop Loss**: 22004.35
- **Risk**: 25.43 points
- **TP 1RR**: 21953.49 ✅
- **TP 2RR**: 21928.06 ✅
- **TP 3RR**: 21902.63 ✅
- **TP 4RR**: 21877.20 ✅
- **TP 15RR**: 21597.46 ❌
- **PnL**: -25.43 points (-1.0R)
- **MFE**: 230.68 points
- **MAE**: 39.95 points

### Trade #157 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 14:00:00
- **FVG 5m**: 21897.21 - 21908.81
- **Entrée**: 21911.13 @ 2025-01-27 14:57:00
- **Stop Loss**: 21886.26
- **Risk**: 24.87 points
- **TP 1RR**: 21936.00 ✅
- **TP 2RR**: 21960.86 ✅
- **TP 3RR**: 21985.73 ✅
- **TP 4RR**: 22010.60 ✅
- **TP 15RR**: 22284.13 ❌
- **PnL**: -24.87 points (-1.0R)
- **MFE**: 107.74 points
- **MAE**: 25.77 points

### Trade #158 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 19:45:00
- **FVG 5m**: 21917.06 - 21954.69
- **Entrée**: 21895.67 @ 2025-01-27 19:59:00
- **Stop Loss**: 21965.67
- **Risk**: 70.00 points
- **TP 1RR**: 21825.67 ❌
- **TP 2RR**: 21755.67 ❌
- **TP 3RR**: 21685.66 ❌
- **TP 4RR**: 21615.66 ❌
- **TP 15RR**: 20845.66 ❌
- **PnL**: -70.00 points (-1.0R)
- **MFE**: 19.59 points
- **MAE**: 73.20 points

### Trade #159 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 20:00:00
- **FVG 5m**: 21938.19 - 21944.38
- **Entrée**: 21947.73 @ 2025-01-27 20:11:00
- **Stop Loss**: 21927.22
- **Risk**: 20.51 points
- **TP 1RR**: 21968.23 ✅
- **TP 2RR**: 21988.74 ✅
- **TP 3RR**: 22009.25 ❌
- **TP 4RR**: 22029.75 ❌
- **TP 15RR**: 22255.31 ❌
- **PnL**: -20.51 points (-1.0R)
- **MFE**: 44.59 points
- **MAE**: 21.13 points

### Trade #160 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 02:00:00
- **FVG 5m**: 22025.82 - 22030.98
- **Entrée**: 22022.99 @ 2025-01-28 03:29:00
- **Stop Loss**: 22042.00
- **Risk**: 19.01 points
- **TP 1RR**: 22003.98 ❌
- **TP 2RR**: 21984.98 ❌
- **TP 3RR**: 21965.97 ❌
- **TP 4RR**: 21946.97 ❌
- **TP 15RR**: 21737.91 ❌
- **PnL**: -19.01 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 23.45 points

### Trade #161 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 02:00:00
- **FVG 5m**: 22025.82 - 22030.98
- **Entrée**: 22022.99 @ 2025-01-28 03:29:00
- **Stop Loss**: 22042.00
- **Risk**: 19.01 points
- **TP 1RR**: 22003.98 ❌
- **TP 2RR**: 21984.98 ❌
- **TP 3RR**: 21965.97 ❌
- **TP 4RR**: 21946.97 ❌
- **TP 15RR**: 21737.91 ❌
- **PnL**: -19.01 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 23.45 points

### Trade #162 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 02:00:00
- **FVG 5m**: 22025.82 - 22030.98
- **Entrée**: 22022.99 @ 2025-01-28 03:29:00
- **Stop Loss**: 22042.00
- **Risk**: 19.01 points
- **TP 1RR**: 22003.98 ❌
- **TP 2RR**: 21984.98 ❌
- **TP 3RR**: 21965.97 ❌
- **TP 4RR**: 21946.97 ❌
- **TP 15RR**: 21737.91 ❌
- **PnL**: -19.01 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 23.45 points

### Trade #163 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 05:30:00
- **FVG 5m**: 21981.49 - 21995.15
- **Entrée**: 21972.21 @ 2025-01-28 06:02:00
- **Stop Loss**: 22006.15
- **Risk**: 33.94 points
- **TP 1RR**: 21938.28 ✅
- **TP 2RR**: 21904.34 ❌
- **TP 3RR**: 21870.40 ❌
- **TP 4RR**: 21836.47 ❌
- **TP 15RR**: 21463.17 ❌
- **PnL**: -33.94 points (-1.0R)
- **MFE**: 56.19 points
- **MAE**: 34.80 points

### Trade #164 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 08:45:00
- **FVG 5m**: 21923.76 - 21940.00
- **Entrée**: 21942.32 @ 2025-01-28 08:57:00
- **Stop Loss**: 21912.80
- **Risk**: 29.52 points
- **TP 1RR**: 21971.84 ✅
- **TP 2RR**: 22001.36 ✅
- **TP 3RR**: 22030.87 ✅
- **TP 4RR**: 22060.39 ✅
- **TP 15RR**: 22385.11 ✅
- **PnL**: 442.79 points (15.0R)
- **MFE**: 445.64 points
- **MAE**: 12.63 points

### Trade #165 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 08:45:00
- **FVG 5m**: 21923.76 - 21940.00
- **Entrée**: 21942.32 @ 2025-01-28 08:57:00
- **Stop Loss**: 21912.80
- **Risk**: 29.52 points
- **TP 1RR**: 21971.84 ✅
- **TP 2RR**: 22001.36 ✅
- **TP 3RR**: 22030.87 ✅
- **TP 4RR**: 22060.39 ✅
- **TP 15RR**: 22385.11 ✅
- **PnL**: 442.79 points (15.0R)
- **MFE**: 445.64 points
- **MAE**: 12.63 points

### Trade #166 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 08:45:00
- **FVG 5m**: 21923.76 - 21940.00
- **Entrée**: 21942.32 @ 2025-01-28 08:57:00
- **Stop Loss**: 21912.80
- **Risk**: 29.52 points
- **TP 1RR**: 21971.84 ✅
- **TP 2RR**: 22001.36 ✅
- **TP 3RR**: 22030.87 ✅
- **TP 4RR**: 22060.39 ✅
- **TP 15RR**: 22385.11 ✅
- **PnL**: 442.79 points (15.0R)
- **MFE**: 445.64 points
- **MAE**: 12.63 points

### Trade #167 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 10:15:00
- **FVG 5m**: 22235.63 - 22237.95
- **Entrée**: 22229.18 @ 2025-01-28 12:22:00
- **Stop Loss**: 22249.07
- **Risk**: 19.88 points
- **TP 1RR**: 22209.30 ✅
- **TP 2RR**: 22189.42 ✅
- **TP 3RR**: 22169.54 ❌
- **TP 4RR**: 22149.65 ❌
- **TP 15RR**: 21930.95 ❌
- **PnL**: -19.88 points (-1.0R)
- **MFE**: 49.49 points
- **MAE**: 28.87 points

### Trade #168 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 10:15:00
- **FVG 5m**: 22235.63 - 22237.95
- **Entrée**: 22229.18 @ 2025-01-28 12:22:00
- **Stop Loss**: 22249.07
- **Risk**: 19.88 points
- **TP 1RR**: 22209.30 ✅
- **TP 2RR**: 22189.42 ✅
- **TP 3RR**: 22169.54 ❌
- **TP 4RR**: 22149.65 ❌
- **TP 15RR**: 21930.95 ❌
- **PnL**: -19.88 points (-1.0R)
- **MFE**: 49.49 points
- **MAE**: 28.87 points

### Trade #169 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 11:00:00
- **FVG 5m**: 22194.13 - 22212.69
- **Entrée**: 22212.95 @ 2025-01-28 13:18:00
- **Stop Loss**: 22183.03
- **Risk**: 29.91 points
- **TP 1RR**: 22242.86 ✅
- **TP 2RR**: 22272.77 ✅
- **TP 3RR**: 22302.68 ✅
- **TP 4RR**: 22332.59 ✅
- **TP 15RR**: 22661.63 ❌
- **PnL**: -29.91 points (-1.0R)
- **MFE**: 155.93 points
- **MAE**: 32.22 points

### Trade #170 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 12:15:00
- **FVG 5m**: 22208.82 - 22216.55
- **Entrée**: 22205.21 @ 2025-01-28 12:39:00
- **Stop Loss**: 22227.66
- **Risk**: 22.45 points
- **TP 1RR**: 22182.76 ✅
- **TP 2RR**: 22160.32 ❌
- **TP 3RR**: 22137.87 ❌
- **TP 4RR**: 22115.42 ❌
- **TP 15RR**: 21868.48 ❌
- **PnL**: -22.45 points (-1.0R)
- **MFE**: 25.52 points
- **MAE**: 23.97 points

### Trade #171 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 07:00:00
- **FVG 5m**: 22275.32 - 22277.90
- **Entrée**: 22268.88 @ 2025-01-29 08:29:00
- **Stop Loss**: 22289.04
- **Risk**: 20.16 points
- **TP 1RR**: 22248.72 ✅
- **TP 2RR**: 22228.56 ✅
- **TP 3RR**: 22208.40 ✅
- **TP 4RR**: 22188.24 ✅
- **TP 15RR**: 21966.48 ❌
- **PnL**: -20.16 points (-1.0R)
- **MFE**: 240.22 points
- **MAE**: 22.42 points

### Trade #172 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 07:00:00
- **FVG 5m**: 22275.32 - 22277.90
- **Entrée**: 22268.88 @ 2025-01-29 08:29:00
- **Stop Loss**: 22289.04
- **Risk**: 20.16 points
- **TP 1RR**: 22248.72 ✅
- **TP 2RR**: 22228.56 ✅
- **TP 3RR**: 22208.40 ✅
- **TP 4RR**: 22188.24 ✅
- **TP 15RR**: 21966.48 ❌
- **PnL**: -20.16 points (-1.0R)
- **MFE**: 240.22 points
- **MAE**: 22.42 points

### Trade #173 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 07:30:00
- **FVG 5m**: 22275.32 - 22277.90
- **Entrée**: 22268.88 @ 2025-01-29 08:29:00
- **Stop Loss**: 22289.04
- **Risk**: 20.16 points
- **TP 1RR**: 22248.72 ✅
- **TP 2RR**: 22228.56 ✅
- **TP 3RR**: 22208.40 ✅
- **TP 4RR**: 22188.24 ✅
- **TP 15RR**: 21966.48 ❌
- **PnL**: -20.16 points (-1.0R)
- **MFE**: 240.22 points
- **MAE**: 22.42 points

### Trade #174 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-29 07:45:00
- **FVG 5m**: 22254.44 - 22269.13
- **Entrée**: 22271.45 @ 2025-01-29 07:59:00
- **Stop Loss**: 22243.31
- **Risk**: 28.14 points
- **TP 1RR**: 22299.59 ❌
- **TP 2RR**: 22327.73 ❌
- **TP 3RR**: 22355.87 ❌
- **TP 4RR**: 22384.01 ❌
- **TP 15RR**: 22693.53 ❌
- **PnL**: -28.14 points (-1.0R)
- **MFE**: 25.26 points
- **MAE**: 38.92 points

### Trade #175 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 09:30:00
- **FVG 5m**: 22176.09 - 22185.37
- **Entrée**: 22172.22 @ 2025-01-29 11:47:00
- **Stop Loss**: 22196.46
- **Risk**: 24.24 points
- **TP 1RR**: 22147.98 ✅
- **TP 2RR**: 22123.75 ✅
- **TP 3RR**: 22099.51 ✅
- **TP 4RR**: 22075.27 ✅
- **TP 15RR**: 21808.66 ❌
- **PnL**: -24.24 points (-1.0R)
- **MFE**: 143.56 points
- **MAE**: 36.34 points

### Trade #176 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-29 12:00:00
- **FVG 5m**: 22122.22 - 22143.10
- **Entrée**: 22150.57 @ 2025-01-29 12:28:00
- **Stop Loss**: 22111.16
- **Risk**: 39.41 points
- **TP 1RR**: 22189.98 ❌
- **TP 2RR**: 22229.40 ❌
- **TP 3RR**: 22268.81 ❌
- **TP 4RR**: 22308.22 ❌
- **TP 15RR**: 22741.76 ❌
- **PnL**: -39.41 points (-1.0R)
- **MFE**: 31.70 points
- **MAE**: 84.28 points

### Trade #177 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 13:45:00
- **FVG 5m**: 22213.72 - 22236.14
- **Entrée**: 22211.66 @ 2025-01-29 14:37:00
- **Stop Loss**: 22247.26
- **Risk**: 35.60 points
- **TP 1RR**: 22176.05 ✅
- **TP 2RR**: 22140.45 ✅
- **TP 3RR**: 22104.85 ✅
- **TP 4RR**: 22069.24 ✅
- **TP 15RR**: 21677.60 ❌
- **PnL**: -35.60 points (-1.0R)
- **MFE**: 162.38 points
- **MAE**: 42.79 points

### Trade #178 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-29 14:15:00
- **FVG 5m**: 22232.79 - 22236.14
- **Entrée**: 22259.85 @ 2025-01-29 14:28:00
- **Stop Loss**: 22221.67
- **Risk**: 38.18 points
- **TP 1RR**: 22298.03 ❌
- **TP 2RR**: 22336.21 ❌
- **TP 3RR**: 22374.39 ❌
- **TP 4RR**: 22412.57 ❌
- **TP 15RR**: 22832.54 ❌
- **PnL**: -38.18 points (-1.0R)
- **MFE**: 9.79 points
- **MAE**: 45.10 points

### Trade #179 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 02:15:00
- **FVG 5m**: 22355.48 - 22368.36
- **Entrée**: 22353.16 @ 2025-01-30 03:02:00
- **Stop Loss**: 22379.55
- **Risk**: 26.39 points
- **TP 1RR**: 22326.77 ✅
- **TP 2RR**: 22300.37 ✅
- **TP 3RR**: 22273.98 ✅
- **TP 4RR**: 22247.59 ✅
- **TP 15RR**: 21957.29 ❌
- **PnL**: -26.39 points (-1.0R)
- **MFE**: 110.83 points
- **MAE**: 35.57 points

### Trade #180 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 02:45:00
- **FVG 5m**: 22296.45 - 22302.12
- **Entrée**: 22303.67 @ 2025-01-30 04:31:00
- **Stop Loss**: 22285.31
- **Risk**: 18.36 points
- **TP 1RR**: 22322.04 ✅
- **TP 2RR**: 22340.40 ✅
- **TP 3RR**: 22358.77 ❌
- **TP 4RR**: 22377.13 ❌
- **TP 15RR**: 22579.15 ❌
- **PnL**: -18.36 points (-1.0R)
- **MFE**: 38.15 points
- **MAE**: 20.62 points

### Trade #181 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22326.35 - 22332.02
- **Entrée**: 22325.84 @ 2025-01-30 03:33:00
- **Stop Loss**: 22343.19
- **Risk**: 17.35 points
- **TP 1RR**: 22308.48 ✅
- **TP 2RR**: 22291.13 ✅
- **TP 3RR**: 22273.78 ✅
- **TP 4RR**: 22256.43 ✅
- **TP 15RR**: 22065.56 ❌
- **PnL**: -17.35 points (-1.0R)
- **MFE**: 83.51 points
- **MAE**: 24.49 points

### Trade #182 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22326.35 - 22332.02
- **Entrée**: 22325.84 @ 2025-01-30 03:33:00
- **Stop Loss**: 22343.19
- **Risk**: 17.35 points
- **TP 1RR**: 22308.48 ✅
- **TP 2RR**: 22291.13 ✅
- **TP 3RR**: 22273.78 ✅
- **TP 4RR**: 22256.43 ✅
- **TP 15RR**: 22065.56 ❌
- **PnL**: -17.35 points (-1.0R)
- **MFE**: 83.51 points
- **MAE**: 24.49 points

### Trade #183 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22326.35 - 22332.02
- **Entrée**: 22325.84 @ 2025-01-30 03:33:00
- **Stop Loss**: 22343.19
- **Risk**: 17.35 points
- **TP 1RR**: 22308.48 ✅
- **TP 2RR**: 22291.13 ✅
- **TP 3RR**: 22273.78 ✅
- **TP 4RR**: 22256.43 ✅
- **TP 15RR**: 22065.56 ❌
- **PnL**: -17.35 points (-1.0R)
- **MFE**: 83.51 points
- **MAE**: 24.49 points

### Trade #184 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22326.35 - 22332.02
- **Entrée**: 22325.84 @ 2025-01-30 03:33:00
- **Stop Loss**: 22343.19
- **Risk**: 17.35 points
- **TP 1RR**: 22308.48 ✅
- **TP 2RR**: 22291.13 ✅
- **TP 3RR**: 22273.78 ✅
- **TP 4RR**: 22256.43 ✅
- **TP 15RR**: 22065.56 ❌
- **PnL**: -17.35 points (-1.0R)
- **MFE**: 83.51 points
- **MAE**: 24.49 points

### Trade #185 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 04:15:00
- **FVG 5m**: 22296.45 - 22302.12
- **Entrée**: 22303.67 @ 2025-01-30 04:31:00
- **Stop Loss**: 22285.31
- **Risk**: 18.36 points
- **TP 1RR**: 22322.04 ✅
- **TP 2RR**: 22340.40 ✅
- **TP 3RR**: 22358.77 ❌
- **TP 4RR**: 22377.13 ❌
- **TP 15RR**: 22579.15 ❌
- **PnL**: -18.36 points (-1.0R)
- **MFE**: 38.15 points
- **MAE**: 20.62 points

### Trade #186 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 06:30:00
- **FVG 5m**: 22302.64 - 22312.95
- **Entrée**: 22313.98 @ 2025-01-30 07:53:00
- **Stop Loss**: 22291.49
- **Risk**: 22.49 points
- **TP 1RR**: 22336.47 ✅
- **TP 2RR**: 22358.96 ❌
- **TP 3RR**: 22381.46 ❌
- **TP 4RR**: 22403.95 ❌
- **TP 15RR**: 22651.36 ❌
- **PnL**: -22.49 points (-1.0R)
- **MFE**: 36.34 points
- **MAE**: 26.55 points

### Trade #187 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 06:45:00
- **FVG 5m**: 22302.64 - 22312.95
- **Entrée**: 22313.98 @ 2025-01-30 07:53:00
- **Stop Loss**: 22291.49
- **Risk**: 22.49 points
- **TP 1RR**: 22336.47 ✅
- **TP 2RR**: 22358.96 ❌
- **TP 3RR**: 22381.46 ❌
- **TP 4RR**: 22403.95 ❌
- **TP 15RR**: 22651.36 ❌
- **PnL**: -22.49 points (-1.0R)
- **MFE**: 36.34 points
- **MAE**: 26.55 points

### Trade #188 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 08:45:00
- **FVG 5m**: 22347.49 - 22355.48
- **Entrée**: 22335.89 @ 2025-01-30 08:58:00
- **Stop Loss**: 22366.65
- **Risk**: 30.77 points
- **TP 1RR**: 22305.12 ✅
- **TP 2RR**: 22274.36 ✅
- **TP 3RR**: 22243.59 ✅
- **TP 4RR**: 22212.82 ✅
- **TP 15RR**: 21874.40 ❌
- **PnL**: -30.77 points (-1.0R)
- **MFE**: 253.10 points
- **MAE**: 36.08 points

### Trade #189 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 09:00:00
- **FVG 5m**: 22210.37 - 22215.01
- **Entrée**: 22198.25 @ 2025-01-30 09:29:00
- **Stop Loss**: 22226.11
- **Risk**: 27.86 points
- **TP 1RR**: 22170.39 ✅
- **TP 2RR**: 22142.53 ❌
- **TP 3RR**: 22114.67 ❌
- **TP 4RR**: 22086.81 ❌
- **TP 15RR**: 21780.34 ❌
- **PnL**: -27.86 points (-1.0R)
- **MFE**: 30.41 points
- **MAE**: 40.21 points

### Trade #190 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 10:45:00
- **FVG 5m**: 22247.74 - 22255.99
- **Entrée**: 22262.69 @ 2025-01-30 12:38:00
- **Stop Loss**: 22236.62
- **Risk**: 26.07 points
- **TP 1RR**: 22288.76 ✅
- **TP 2RR**: 22314.84 ✅
- **TP 3RR**: 22340.91 ✅
- **TP 4RR**: 22366.98 ✅
- **TP 15RR**: 22653.78 ❌
- **PnL**: -26.07 points (-1.0R)
- **MFE**: 109.28 points
- **MAE**: 35.05 points

### Trade #191 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 14:30:00
- **FVG 5m**: 22369.65 - 22375.84
- **Entrée**: 22366.82 @ 2025-01-30 17:18:00
- **Stop Loss**: 22387.03
- **Risk**: 20.21 points
- **TP 1RR**: 22346.61 ✅
- **TP 2RR**: 22326.40 ❌
- **TP 3RR**: 22306.19 ❌
- **TP 4RR**: 22285.98 ❌
- **TP 15RR**: 22063.68 ❌
- **PnL**: -20.21 points (-1.0R)
- **MFE**: 36.08 points
- **MAE**: 26.03 points

### Trade #192 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 14:30:00
- **FVG 5m**: 22369.65 - 22375.84
- **Entrée**: 22366.82 @ 2025-01-30 17:18:00
- **Stop Loss**: 22387.03
- **Risk**: 20.21 points
- **TP 1RR**: 22346.61 ✅
- **TP 2RR**: 22326.40 ❌
- **TP 3RR**: 22306.19 ❌
- **TP 4RR**: 22285.98 ❌
- **TP 15RR**: 22063.68 ❌
- **PnL**: -20.21 points (-1.0R)
- **MFE**: 36.08 points
- **MAE**: 26.03 points

### Trade #193 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 17:15:00
- **FVG 5m**: 22348.26 - 22353.41
- **Entrée**: 22344.65 @ 2025-01-30 17:27:00
- **Stop Loss**: 22364.59
- **Risk**: 19.94 points
- **TP 1RR**: 22324.71 ❌
- **TP 2RR**: 22304.77 ❌
- **TP 3RR**: 22284.83 ❌
- **TP 4RR**: 22264.89 ❌
- **TP 15RR**: 22045.55 ❌
- **PnL**: -19.94 points (-1.0R)
- **MFE**: 13.92 points
- **MAE**: 22.42 points

### Trade #194 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 01:15:00
- **FVG 5m**: 22446.97 - 22453.68
- **Entrée**: 22441.82 @ 2025-01-31 02:44:00
- **Stop Loss**: 22464.90
- **Risk**: 23.08 points
- **TP 1RR**: 22418.74 ✅
- **TP 2RR**: 22395.65 ❌
- **TP 3RR**: 22372.57 ❌
- **TP 4RR**: 22349.49 ❌
- **TP 15RR**: 22095.58 ❌
- **PnL**: -23.08 points (-1.0R)
- **MFE**: 25.77 points
- **MAE**: 24.74 points

### Trade #195 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 02:00:00
- **FVG 5m**: 22446.97 - 22453.68
- **Entrée**: 22441.82 @ 2025-01-31 02:44:00
- **Stop Loss**: 22464.90
- **Risk**: 23.08 points
- **TP 1RR**: 22418.74 ✅
- **TP 2RR**: 22395.65 ❌
- **TP 3RR**: 22372.57 ❌
- **TP 4RR**: 22349.49 ❌
- **TP 15RR**: 22095.58 ❌
- **PnL**: -23.08 points (-1.0R)
- **MFE**: 25.77 points
- **MAE**: 24.74 points

### Trade #196 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 06:00:00
- **FVG 5m**: 22459.60 - 22465.27
- **Entrée**: 22457.28 @ 2025-01-31 06:59:00
- **Stop Loss**: 22476.51
- **Risk**: 19.22 points
- **TP 1RR**: 22438.06 ✅
- **TP 2RR**: 22418.84 ❌
- **TP 3RR**: 22399.62 ❌
- **TP 4RR**: 22380.39 ❌
- **TP 15RR**: 22168.94 ❌
- **PnL**: -19.22 points (-1.0R)
- **MFE**: 27.84 points
- **MAE**: 20.10 points

### Trade #197 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 07:30:00
- **FVG 5m**: 22583.58 - 22598.27
- **Entrée**: 22599.56 @ 2025-01-31 09:33:00
- **Stop Loss**: 22572.29
- **Risk**: 27.27 points
- **TP 1RR**: 22626.83 ❌
- **TP 2RR**: 22654.10 ❌
- **TP 3RR**: 22681.37 ❌
- **TP 4RR**: 22708.64 ❌
- **TP 15RR**: 23008.63 ❌
- **PnL**: -27.27 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 28.35 points

### Trade #198 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 08:45:00
- **FVG 5m**: 22583.58 - 22598.27
- **Entrée**: 22599.56 @ 2025-01-31 09:33:00
- **Stop Loss**: 22572.29
- **Risk**: 27.27 points
- **TP 1RR**: 22626.83 ❌
- **TP 2RR**: 22654.10 ❌
- **TP 3RR**: 22681.37 ❌
- **TP 4RR**: 22708.64 ❌
- **TP 15RR**: 23008.63 ❌
- **PnL**: -27.27 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 28.35 points

### Trade #199 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 08:45:00
- **FVG 5m**: 22583.58 - 22598.27
- **Entrée**: 22599.56 @ 2025-01-31 09:33:00
- **Stop Loss**: 22572.29
- **Risk**: 27.27 points
- **TP 1RR**: 22626.83 ❌
- **TP 2RR**: 22654.10 ❌
- **TP 3RR**: 22681.37 ❌
- **TP 4RR**: 22708.64 ❌
- **TP 15RR**: 23008.63 ❌
- **PnL**: -27.27 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 28.35 points

### Trade #200 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 12:30:00
- **FVG 5m**: 22352.38 - 22375.32
- **Entrée**: 22336.15 @ 2025-01-31 13:37:00
- **Stop Loss**: 22386.51
- **Risk**: 50.36 points
- **TP 1RR**: 22285.78 ✅
- **TP 2RR**: 22235.42 ✅
- **TP 3RR**: 22185.05 ✅
- **TP 4RR**: 22134.69 ✅
- **TP 15RR**: 21580.68 ❌
- **PnL**: -50.36 points (-1.0R)
- **MFE**: 744.62 points
- **MAE**: 55.67 points

### Trade #201 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 12:30:00
- **FVG 5m**: 22352.38 - 22375.32
- **Entrée**: 22336.15 @ 2025-01-31 13:37:00
- **Stop Loss**: 22386.51
- **Risk**: 50.36 points
- **TP 1RR**: 22285.78 ✅
- **TP 2RR**: 22235.42 ✅
- **TP 3RR**: 22185.05 ✅
- **TP 4RR**: 22134.69 ✅
- **TP 15RR**: 21580.68 ❌
- **PnL**: -50.36 points (-1.0R)
- **MFE**: 744.62 points
- **MAE**: 55.67 points

### Trade #202 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 12:30:00
- **FVG 5m**: 22302.64 - 22321.45
- **Entrée**: 22326.35 @ 2025-01-31 13:51:00
- **Stop Loss**: 22291.49
- **Risk**: 34.86 points
- **TP 1RR**: 22361.22 ❌
- **TP 2RR**: 22396.08 ❌
- **TP 3RR**: 22430.94 ❌
- **TP 4RR**: 22465.81 ❌
- **TP 15RR**: 22849.30 ❌
- **PnL**: -34.86 points (-1.0R)
- **MFE**: 12.89 points
- **MAE**: 37.89 points

### Trade #203 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 12:30:00
- **FVG 5m**: 22302.64 - 22321.45
- **Entrée**: 22326.35 @ 2025-01-31 13:51:00
- **Stop Loss**: 22291.49
- **Risk**: 34.86 points
- **TP 1RR**: 22361.22 ❌
- **TP 2RR**: 22396.08 ❌
- **TP 3RR**: 22430.94 ❌
- **TP 4RR**: 22465.81 ❌
- **TP 15RR**: 22849.30 ❌
- **PnL**: -34.86 points (-1.0R)
- **MFE**: 12.89 points
- **MAE**: 37.89 points

### Trade #204 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 13:00:00
- **FVG 5m**: 22352.38 - 22375.32
- **Entrée**: 22336.15 @ 2025-01-31 13:37:00
- **Stop Loss**: 22386.51
- **Risk**: 50.36 points
- **TP 1RR**: 22285.78 ✅
- **TP 2RR**: 22235.42 ✅
- **TP 3RR**: 22185.05 ✅
- **TP 4RR**: 22134.69 ✅
- **TP 15RR**: 21580.68 ❌
- **PnL**: -50.36 points (-1.0R)
- **MFE**: 744.62 points
- **MAE**: 55.67 points

### Trade #205 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 13:00:00
- **FVG 5m**: 22302.64 - 22321.45
- **Entrée**: 22326.35 @ 2025-01-31 13:51:00
- **Stop Loss**: 22291.49
- **Risk**: 34.86 points
- **TP 1RR**: 22361.22 ❌
- **TP 2RR**: 22396.08 ❌
- **TP 3RR**: 22430.94 ❌
- **TP 4RR**: 22465.81 ❌
- **TP 15RR**: 22849.30 ❌
- **PnL**: -34.86 points (-1.0R)
- **MFE**: 12.89 points
- **MAE**: 37.89 points

### Trade #206 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 13:15:00
- **FVG 5m**: 22352.38 - 22375.32
- **Entrée**: 22336.15 @ 2025-01-31 13:37:00
- **Stop Loss**: 22386.51
- **Risk**: 50.36 points
- **TP 1RR**: 22285.78 ✅
- **TP 2RR**: 22235.42 ✅
- **TP 3RR**: 22185.05 ✅
- **TP 4RR**: 22134.69 ✅
- **TP 15RR**: 21580.68 ❌
- **PnL**: -50.36 points (-1.0R)
- **MFE**: 744.62 points
- **MAE**: 55.67 points

### Trade #207 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-02 17:45:00
- **FVG 5m**: 21774.01 - 21777.88
- **Entrée**: 21786.64 @ 2025-02-02 19:22:00
- **Stop Loss**: 21763.12
- **Risk**: 23.52 points
- **TP 1RR**: 21810.16 ❌
- **TP 2RR**: 21833.67 ❌
- **TP 3RR**: 21857.19 ❌
- **TP 4RR**: 21880.71 ❌
- **TP 15RR**: 22139.39 ❌
- **PnL**: -23.52 points (-1.0R)
- **MFE**: 18.30 points
- **MAE**: 32.99 points

### Trade #208 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 02:00:00
- **FVG 5m**: 21844.12 - 21872.98
- **Entrée**: 21876.85 @ 2025-02-03 02:18:00
- **Stop Loss**: 21833.19
- **Risk**: 43.66 points
- **TP 1RR**: 21920.51 ❌
- **TP 2RR**: 21964.16 ❌
- **TP 3RR**: 22007.82 ❌
- **TP 4RR**: 22051.47 ❌
- **TP 15RR**: 22531.68 ❌
- **PnL**: -43.66 points (-1.0R)
- **MFE**: 33.25 points
- **MAE**: 54.90 points

### Trade #209 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 05:15:00
- **FVG 5m**: 21881.75 - 21884.58
- **Entrée**: 21881.49 @ 2025-02-03 05:36:00
- **Stop Loss**: 21895.52
- **Risk**: 14.04 points
- **TP 1RR**: 21867.45 ✅
- **TP 2RR**: 21853.42 ✅
- **TP 3RR**: 21839.38 ✅
- **TP 4RR**: 21825.35 ✅
- **TP 15RR**: 21670.96 ❌
- **PnL**: -14.04 points (-1.0R)
- **MFE**: 70.88 points
- **MAE**: 23.97 points

### Trade #210 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 08:30:00
- **FVG 5m**: 21896.70 - 21910.10
- **Entrée**: 21854.94 @ 2025-02-03 08:52:00
- **Stop Loss**: 21921.05
- **Risk**: 66.11 points
- **TP 1RR**: 21788.83 ✅
- **TP 2RR**: 21722.72 ❌
- **TP 3RR**: 21656.61 ❌
- **TP 4RR**: 21590.50 ❌
- **TP 15RR**: 20863.27 ❌
- **PnL**: -66.11 points (-1.0R)
- **MFE**: 87.89 points
- **MAE**: 135.31 points

### Trade #211 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 08:45:00
- **FVG 5m**: 21797.72 - 21811.64
- **Entrée**: 21783.55 @ 2025-02-03 09:14:00
- **Stop Loss**: 21822.55
- **Risk**: 39.00 points
- **TP 1RR**: 21744.55 ❌
- **TP 2RR**: 21705.55 ❌
- **TP 3RR**: 21666.55 ❌
- **TP 4RR**: 21627.55 ❌
- **TP 15RR**: 21198.55 ❌
- **PnL**: -39.00 points (-1.0R)
- **MFE**: 16.50 points
- **MAE**: 77.06 points

### Trade #212 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:30:00
- **FVG 5m**: 22035.36 - 22039.23
- **Entrée**: 22040.52 @ 2025-02-03 11:49:00
- **Stop Loss**: 22024.34
- **Risk**: 16.17 points
- **TP 1RR**: 22056.69 ✅
- **TP 2RR**: 22072.86 ✅
- **TP 3RR**: 22089.03 ✅
- **TP 4RR**: 22105.21 ❌
- **TP 15RR**: 22283.10 ❌
- **PnL**: -16.17 points (-1.0R)
- **MFE**: 48.97 points
- **MAE**: 38.66 points

### Trade #213 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:30:00
- **FVG 5m**: 22035.36 - 22039.23
- **Entrée**: 22040.52 @ 2025-02-03 11:49:00
- **Stop Loss**: 22024.34
- **Risk**: 16.17 points
- **TP 1RR**: 22056.69 ✅
- **TP 2RR**: 22072.86 ✅
- **TP 3RR**: 22089.03 ✅
- **TP 4RR**: 22105.21 ❌
- **TP 15RR**: 22283.10 ❌
- **PnL**: -16.17 points (-1.0R)
- **MFE**: 48.97 points
- **MAE**: 38.66 points

### Trade #214 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:30:00
- **FVG 5m**: 22035.36 - 22039.23
- **Entrée**: 22040.52 @ 2025-02-03 11:49:00
- **Stop Loss**: 22024.34
- **Risk**: 16.17 points
- **TP 1RR**: 22056.69 ✅
- **TP 2RR**: 22072.86 ✅
- **TP 3RR**: 22089.03 ✅
- **TP 4RR**: 22105.21 ❌
- **TP 15RR**: 22283.10 ❌
- **PnL**: -16.17 points (-1.0R)
- **MFE**: 48.97 points
- **MAE**: 38.66 points

### Trade #215 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 14:00:00
- **FVG 5m**: 22132.79 - 22146.19
- **Entrée**: 22130.98 @ 2025-02-03 14:27:00
- **Stop Loss**: 22157.26
- **Risk**: 26.28 points
- **TP 1RR**: 22104.70 ✅
- **TP 2RR**: 22078.42 ✅
- **TP 3RR**: 22052.14 ✅
- **TP 4RR**: 22025.86 ❌
- **TP 15RR**: 21736.79 ❌
- **PnL**: -26.28 points (-1.0R)
- **MFE**: 80.42 points
- **MAE**: 37.89 points

### Trade #216 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 15:30:00
- **FVG 5m**: 22221.45 - 22232.79
- **Entrée**: 22242.84 @ 2025-02-03 17:06:00
- **Stop Loss**: 22210.34
- **Risk**: 32.50 points
- **TP 1RR**: 22275.35 ❌
- **TP 2RR**: 22307.85 ❌
- **TP 3RR**: 22340.35 ❌
- **TP 4RR**: 22372.86 ❌
- **TP 15RR**: 22730.39 ❌
- **PnL**: -32.50 points (-1.0R)
- **MFE**: 10.31 points
- **MAE**: 33.76 points

### Trade #217 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 23:30:00
- **FVG 5m**: 22033.56 - 22036.13
- **Entrée**: 22046.19 @ 2025-02-04 00:48:00
- **Stop Loss**: 22022.54
- **Risk**: 23.65 points
- **TP 1RR**: 22069.83 ✅
- **TP 2RR**: 22093.48 ❌
- **TP 3RR**: 22117.12 ❌
- **TP 4RR**: 22140.77 ❌
- **TP 15RR**: 22400.88 ❌
- **PnL**: -23.65 points (-1.0R)
- **MFE**: 42.01 points
- **MAE**: 27.32 points

### Trade #218 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-04 00:45:00
- **FVG 5m**: 22004.95 - 22022.47
- **Entrée**: 22024.54 @ 2025-02-04 02:59:00
- **Stop Loss**: 21993.95
- **Risk**: 30.59 points
- **TP 1RR**: 22055.13 ✅
- **TP 2RR**: 22085.72 ✅
- **TP 3RR**: 22116.31 ✅
- **TP 4RR**: 22146.90 ✅
- **TP 15RR**: 22483.40 ✅
- **PnL**: 458.86 points (15.0R)
- **MFE**: 459.81 points
- **MAE**: 7.22 points

### Trade #219 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-04 06:30:00
- **FVG 5m**: 22096.70 - 22100.05
- **Entrée**: 22093.10 @ 2025-02-04 08:14:00
- **Stop Loss**: 22111.10
- **Risk**: 18.01 points
- **TP 1RR**: 22075.09 ✅
- **TP 2RR**: 22057.08 ❌
- **TP 3RR**: 22039.07 ❌
- **TP 4RR**: 22021.06 ❌
- **TP 15RR**: 21822.96 ❌
- **PnL**: -18.01 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 27.06 points

### Trade #220 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-04 08:30:00
- **FVG 5m**: 22189.49 - 22212.43
- **Entrée**: 22214.23 @ 2025-02-04 08:54:00
- **Stop Loss**: 22178.40
- **Risk**: 35.84 points
- **TP 1RR**: 22250.07 ✅
- **TP 2RR**: 22285.91 ✅
- **TP 3RR**: 22321.75 ✅
- **TP 4RR**: 22357.59 ✅
- **TP 15RR**: 22751.80 ❌
- **PnL**: -35.84 points (-1.0R)
- **MFE**: 151.55 points
- **MAE**: 40.21 points

### Trade #221 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-04 11:15:00
- **FVG 5m**: 22241.55 - 22244.91
- **Entrée**: 22240.27 @ 2025-02-04 11:28:00
- **Stop Loss**: 22256.03
- **Risk**: 15.76 points
- **TP 1RR**: 22224.50 ✅
- **TP 2RR**: 22208.74 ❌
- **TP 3RR**: 22192.98 ❌
- **TP 4RR**: 22177.22 ❌
- **TP 15RR**: 22003.84 ❌
- **PnL**: -15.76 points (-1.0R)
- **MFE**: 22.94 points
- **MAE**: 19.85 points

### Trade #222 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-04 15:00:00
- **FVG 5m**: 22263.46 - 22268.36
- **Entrée**: 22254.18 @ 2025-02-04 15:38:00
- **Stop Loss**: 22279.49
- **Risk**: 25.31 points
- **TP 1RR**: 22228.87 ✅
- **TP 2RR**: 22203.56 ❌
- **TP 3RR**: 22178.25 ❌
- **TP 4RR**: 22152.94 ❌
- **TP 15RR**: 21874.53 ❌
- **PnL**: -25.31 points (-1.0R)
- **MFE**: 36.86 points
- **MAE**: 26.81 points

### Trade #223 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-05 02:15:00
- **FVG 5m**: 22141.81 - 22149.03
- **Entrée**: 22152.38 @ 2025-02-05 03:02:00
- **Stop Loss**: 22130.74
- **Risk**: 21.64 points
- **TP 1RR**: 22174.01 ❌
- **TP 2RR**: 22195.65 ❌
- **TP 3RR**: 22217.29 ❌
- **TP 4RR**: 22238.93 ❌
- **TP 15RR**: 22476.95 ❌
- **PnL**: -21.64 points (-1.0R)
- **MFE**: 19.59 points
- **MAE**: 23.20 points

### Trade #224 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 02:30:00
- **FVG 5m**: 22146.45 - 22150.57
- **Entrée**: 22143.10 @ 2025-02-05 02:41:00
- **Stop Loss**: 22161.65
- **Risk**: 18.55 points
- **TP 1RR**: 22124.55 ✅
- **TP 2RR**: 22106.00 ❌
- **TP 3RR**: 22087.45 ❌
- **TP 4RR**: 22068.90 ❌
- **TP 15RR**: 21864.85 ❌
- **PnL**: -18.55 points (-1.0R)
- **MFE**: 27.58 points
- **MAE**: 21.39 points

### Trade #225 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-05 08:15:00
- **FVG 5m**: 22251.61 - 22282.79
- **Entrée**: 22290.53 @ 2025-02-05 10:29:00
- **Stop Loss**: 22240.48
- **Risk**: 50.04 points
- **TP 1RR**: 22340.57 ✅
- **TP 2RR**: 22390.62 ✅
- **TP 3RR**: 22440.66 ✅
- **TP 4RR**: 22490.70 ✅
- **TP 15RR**: 23041.20 ❌
- **PnL**: -50.04 points (-1.0R)
- **MFE**: 357.75 points
- **MAE**: 56.70 points

### Trade #226 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-05 08:15:00
- **FVG 5m**: 22251.61 - 22282.79
- **Entrée**: 22290.53 @ 2025-02-05 10:29:00
- **Stop Loss**: 22240.48
- **Risk**: 50.04 points
- **TP 1RR**: 22340.57 ✅
- **TP 2RR**: 22390.62 ✅
- **TP 3RR**: 22440.66 ✅
- **TP 4RR**: 22490.70 ✅
- **TP 15RR**: 23041.20 ❌
- **PnL**: -50.04 points (-1.0R)
- **MFE**: 357.75 points
- **MAE**: 56.70 points

### Trade #227 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 12:15:00
- **FVG 5m**: 22393.11 - 22403.67
- **Entrée**: 22391.82 @ 2025-02-05 14:39:00
- **Stop Loss**: 22414.88
- **Risk**: 23.06 points
- **TP 1RR**: 22368.76 ✅
- **TP 2RR**: 22345.70 ❌
- **TP 3RR**: 22322.64 ❌
- **TP 4RR**: 22299.59 ❌
- **TP 15RR**: 22045.95 ❌
- **PnL**: -23.06 points (-1.0R)
- **MFE**: 30.41 points
- **MAE**: 25.52 points

### Trade #228 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 12:15:00
- **FVG 5m**: 22393.11 - 22403.67
- **Entrée**: 22391.82 @ 2025-02-05 14:39:00
- **Stop Loss**: 22414.88
- **Risk**: 23.06 points
- **TP 1RR**: 22368.76 ✅
- **TP 2RR**: 22345.70 ❌
- **TP 3RR**: 22322.64 ❌
- **TP 4RR**: 22299.59 ❌
- **TP 15RR**: 22045.95 ❌
- **PnL**: -23.06 points (-1.0R)
- **MFE**: 30.41 points
- **MAE**: 25.52 points

### Trade #229 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 06:45:00
- **FVG 5m**: 22451.61 - 22462.18
- **Entrée**: 22463.21 @ 2025-02-06 08:44:00
- **Stop Loss**: 22440.39
- **Risk**: 22.82 points
- **TP 1RR**: 22486.04 ✅
- **TP 2RR**: 22508.86 ❌
- **TP 3RR**: 22531.68 ❌
- **TP 4RR**: 22554.51 ❌
- **TP 15RR**: 22805.58 ❌
- **PnL**: -22.82 points (-1.0R)
- **MFE**: 36.34 points
- **MAE**: 24.23 points

### Trade #230 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 07:45:00
- **FVG 5m**: 22451.61 - 22462.18
- **Entrée**: 22463.21 @ 2025-02-06 08:44:00
- **Stop Loss**: 22440.39
- **Risk**: 22.82 points
- **TP 1RR**: 22486.04 ✅
- **TP 2RR**: 22508.86 ❌
- **TP 3RR**: 22531.68 ❌
- **TP 4RR**: 22554.51 ❌
- **TP 15RR**: 22805.58 ❌
- **PnL**: -22.82 points (-1.0R)
- **MFE**: 36.34 points
- **MAE**: 24.23 points

### Trade #231 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 07:45:00
- **FVG 5m**: 22451.61 - 22462.18
- **Entrée**: 22463.21 @ 2025-02-06 08:44:00
- **Stop Loss**: 22440.39
- **Risk**: 22.82 points
- **TP 1RR**: 22486.04 ✅
- **TP 2RR**: 22508.86 ❌
- **TP 3RR**: 22531.68 ❌
- **TP 4RR**: 22554.51 ❌
- **TP 15RR**: 22805.58 ❌
- **PnL**: -22.82 points (-1.0R)
- **MFE**: 36.34 points
- **MAE**: 24.23 points

### Trade #232 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 08:45:00
- **FVG 5m**: 22481.00 - 22506.77
- **Entrée**: 22472.49 @ 2025-02-06 09:24:00
- **Stop Loss**: 22518.02
- **Risk**: 45.53 points
- **TP 1RR**: 22426.96 ✅
- **TP 2RR**: 22381.43 ❌
- **TP 3RR**: 22335.89 ❌
- **TP 4RR**: 22290.36 ❌
- **TP 15RR**: 21789.50 ❌
- **PnL**: -45.53 points (-1.0R)
- **MFE**: 59.02 points
- **MAE**: 45.62 points

### Trade #233 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 08:45:00
- **FVG 5m**: 22481.00 - 22506.77
- **Entrée**: 22472.49 @ 2025-02-06 09:24:00
- **Stop Loss**: 22518.02
- **Risk**: 45.53 points
- **TP 1RR**: 22426.96 ✅
- **TP 2RR**: 22381.43 ❌
- **TP 3RR**: 22335.89 ❌
- **TP 4RR**: 22290.36 ❌
- **TP 15RR**: 21789.50 ❌
- **PnL**: -45.53 points (-1.0R)
- **MFE**: 59.02 points
- **MAE**: 45.62 points

### Trade #234 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 09:15:00
- **FVG 5m**: 22466.56 - 22469.14
- **Entrée**: 22464.24 @ 2025-02-06 10:33:00
- **Stop Loss**: 22480.38
- **Risk**: 16.13 points
- **TP 1RR**: 22448.11 ✅
- **TP 2RR**: 22431.98 ✅
- **TP 3RR**: 22415.85 ❌
- **TP 4RR**: 22399.72 ❌
- **TP 15RR**: 22222.27 ❌
- **PnL**: -16.13 points (-1.0R)
- **MFE**: 42.79 points
- **MAE**: 17.78 points

### Trade #235 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 09:15:00
- **FVG 5m**: 22466.56 - 22469.14
- **Entrée**: 22464.24 @ 2025-02-06 10:33:00
- **Stop Loss**: 22480.38
- **Risk**: 16.13 points
- **TP 1RR**: 22448.11 ✅
- **TP 2RR**: 22431.98 ✅
- **TP 3RR**: 22415.85 ❌
- **TP 4RR**: 22399.72 ❌
- **TP 15RR**: 22222.27 ❌
- **PnL**: -16.13 points (-1.0R)
- **MFE**: 42.79 points
- **MAE**: 17.78 points

### Trade #236 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 09:15:00
- **FVG 5m**: 22466.56 - 22469.14
- **Entrée**: 22464.24 @ 2025-02-06 10:33:00
- **Stop Loss**: 22480.38
- **Risk**: 16.13 points
- **TP 1RR**: 22448.11 ✅
- **TP 2RR**: 22431.98 ✅
- **TP 3RR**: 22415.85 ❌
- **TP 4RR**: 22399.72 ❌
- **TP 15RR**: 22222.27 ❌
- **PnL**: -16.13 points (-1.0R)
- **MFE**: 42.79 points
- **MAE**: 17.78 points

### Trade #237 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 13:30:00
- **FVG 5m**: 22426.87 - 22433.83
- **Entrée**: 22435.38 @ 2025-02-06 14:14:00
- **Stop Loss**: 22415.66
- **Risk**: 19.72 points
- **TP 1RR**: 22455.10 ✅
- **TP 2RR**: 22474.81 ✅
- **TP 3RR**: 22494.53 ✅
- **TP 4RR**: 22514.25 ✅
- **TP 15RR**: 22731.16 ❌
- **PnL**: -19.72 points (-1.0R)
- **MFE**: 212.89 points
- **MAE**: 30.16 points

### Trade #238 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 21:00:00
- **FVG 5m**: 22540.02 - 22542.34
- **Entrée**: 22537.96 @ 2025-02-06 22:29:00
- **Stop Loss**: 22553.61
- **Risk**: 15.65 points
- **TP 1RR**: 22522.30 ✅
- **TP 2RR**: 22506.65 ✅
- **TP 3RR**: 22491.00 ❌
- **TP 4RR**: 22475.35 ❌
- **TP 15RR**: 22303.17 ❌
- **PnL**: -15.65 points (-1.0R)
- **MFE**: 35.83 points
- **MAE**: 15.72 points

### Trade #239 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-07 07:30:00
- **FVG 5m**: 22583.32 - 22616.05
- **Entrée**: 22582.29 @ 2025-02-07 08:59:00
- **Stop Loss**: 22627.36
- **Risk**: 45.07 points
- **TP 1RR**: 22537.22 ✅
- **TP 2RR**: 22492.14 ✅
- **TP 3RR**: 22447.07 ✅
- **TP 4RR**: 22402.00 ✅
- **TP 15RR**: 21906.21 ❌
- **PnL**: -45.07 points (-1.0R)
- **MFE**: 501.05 points
- **MAE**: 47.42 points

### Trade #240 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 07:30:00
- **FVG 5m**: 22572.24 - 22604.97
- **Entrée**: 22607.29 @ 2025-02-07 08:31:00
- **Stop Loss**: 22560.95
- **Risk**: 46.34 points
- **TP 1RR**: 22653.63 ❌
- **TP 2RR**: 22699.97 ❌
- **TP 3RR**: 22746.31 ❌
- **TP 4RR**: 22792.65 ❌
- **TP 15RR**: 23302.37 ❌
- **PnL**: -46.34 points (-1.0R)
- **MFE**: 40.98 points
- **MAE**: 152.84 points

### Trade #241 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 07:30:00
- **FVG 5m**: 22572.24 - 22604.97
- **Entrée**: 22607.29 @ 2025-02-07 08:31:00
- **Stop Loss**: 22560.95
- **Risk**: 46.34 points
- **TP 1RR**: 22653.63 ❌
- **TP 2RR**: 22699.97 ❌
- **TP 3RR**: 22746.31 ❌
- **TP 4RR**: 22792.65 ❌
- **TP 15RR**: 23302.37 ❌
- **PnL**: -46.34 points (-1.0R)
- **MFE**: 40.98 points
- **MAE**: 152.84 points

### Trade #242 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 07:30:00
- **FVG 5m**: 22572.24 - 22604.97
- **Entrée**: 22607.29 @ 2025-02-07 08:31:00
- **Stop Loss**: 22560.95
- **Risk**: 46.34 points
- **TP 1RR**: 22653.63 ❌
- **TP 2RR**: 22699.97 ❌
- **TP 3RR**: 22746.31 ❌
- **TP 4RR**: 22792.65 ❌
- **TP 15RR**: 23302.37 ❌
- **PnL**: -46.34 points (-1.0R)
- **MFE**: 40.98 points
- **MAE**: 152.84 points

### Trade #243 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-07 09:00:00
- **FVG 5m**: 22399.03 - 22407.54
- **Entrée**: 22324.55 @ 2025-02-07 09:53:00
- **Stop Loss**: 22418.74
- **Risk**: 94.20 points
- **TP 1RR**: 22230.35 ❌
- **TP 2RR**: 22136.15 ❌
- **TP 3RR**: 22041.96 ❌
- **TP 4RR**: 21947.76 ❌
- **TP 15RR**: 20911.60 ❌
- **PnL**: -94.20 points (-1.0R)
- **MFE**: 42.27 points
- **MAE**: 108.51 points

### Trade #244 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 09:45:00
- **FVG 5m**: 22348.26 - 22357.02
- **Entrée**: 22358.05 @ 2025-02-07 12:04:00
- **Stop Loss**: 22337.09
- **Risk**: 20.97 points
- **TP 1RR**: 22379.02 ✅
- **TP 2RR**: 22399.99 ✅
- **TP 3RR**: 22420.96 ❌
- **TP 4RR**: 22441.93 ❌
- **TP 15RR**: 22672.58 ❌
- **PnL**: -20.97 points (-1.0R)
- **MFE**: 45.62 points
- **MAE**: 29.38 points

### Trade #245 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 09:45:00
- **FVG 5m**: 22348.26 - 22357.02
- **Entrée**: 22358.05 @ 2025-02-07 12:04:00
- **Stop Loss**: 22337.09
- **Risk**: 20.97 points
- **TP 1RR**: 22379.02 ✅
- **TP 2RR**: 22399.99 ✅
- **TP 3RR**: 22420.96 ❌
- **TP 4RR**: 22441.93 ❌
- **TP 15RR**: 22672.58 ❌
- **PnL**: -20.97 points (-1.0R)
- **MFE**: 45.62 points
- **MAE**: 29.38 points

### Trade #246 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-07 13:00:00
- **FVG 5m**: 22266.04 - 22270.42
- **Entrée**: 22251.86 @ 2025-02-07 14:01:00
- **Stop Loss**: 22281.56
- **Risk**: 29.69 points
- **TP 1RR**: 22222.17 ✅
- **TP 2RR**: 22192.48 ❌
- **TP 3RR**: 22162.79 ❌
- **TP 4RR**: 22133.09 ❌
- **TP 15RR**: 21806.48 ❌
- **PnL**: -29.69 points (-1.0R)
- **MFE**: 31.70 points
- **MAE**: 31.96 points

### Trade #247 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-09 17:00:00
- **FVG 5m**: 22223.77 - 22239.49
- **Entrée**: 22240.01 @ 2025-02-09 17:33:00
- **Stop Loss**: 22212.66
- **Risk**: 27.35 points
- **TP 1RR**: 22267.36 ✅
- **TP 2RR**: 22294.71 ✅
- **TP 3RR**: 22322.06 ✅
- **TP 4RR**: 22349.41 ✅
- **TP 15RR**: 22650.25 ❌
- **PnL**: -27.35 points (-1.0R)
- **MFE**: 331.97 points
- **MAE**: 29.90 points

### Trade #248 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-09 17:00:00
- **FVG 5m**: 22223.77 - 22239.49
- **Entrée**: 22240.01 @ 2025-02-09 17:33:00
- **Stop Loss**: 22212.66
- **Risk**: 27.35 points
- **TP 1RR**: 22267.36 ✅
- **TP 2RR**: 22294.71 ✅
- **TP 3RR**: 22322.06 ✅
- **TP 4RR**: 22349.41 ✅
- **TP 15RR**: 22650.25 ❌
- **PnL**: -27.35 points (-1.0R)
- **MFE**: 331.97 points
- **MAE**: 29.90 points

### Trade #249 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-10 06:00:00
- **FVG 5m**: 22401.61 - 22408.06
- **Entrée**: 22400.84 @ 2025-02-10 06:32:00
- **Stop Loss**: 22419.26
- **Risk**: 18.42 points
- **TP 1RR**: 22382.42 ❌
- **TP 2RR**: 22364.00 ❌
- **TP 3RR**: 22345.58 ❌
- **TP 4RR**: 22327.16 ❌
- **TP 15RR**: 22124.53 ❌
- **PnL**: -18.42 points (-1.0R)
- **MFE**: 6.19 points
- **MAE**: 19.33 points

### Trade #250 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-10 08:30:00
- **FVG 5m**: 22470.69 - 22488.73
- **Entrée**: 22488.99 @ 2025-02-10 09:01:00
- **Stop Loss**: 22459.45
- **Risk**: 29.53 points
- **TP 1RR**: 22518.52 ✅
- **TP 2RR**: 22548.06 ✅
- **TP 3RR**: 22577.59 ❌
- **TP 4RR**: 22607.13 ❌
- **TP 15RR**: 22932.01 ❌
- **PnL**: -29.53 points (-1.0R)
- **MFE**: 82.99 points
- **MAE**: 36.86 points

### Trade #251 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 01:45:00
- **FVG 5m**: 22413.21 - 22431.25
- **Entrée**: 22408.31 @ 2025-02-11 01:58:00
- **Stop Loss**: 22442.47
- **Risk**: 34.15 points
- **TP 1RR**: 22374.16 ❌
- **TP 2RR**: 22340.00 ❌
- **TP 3RR**: 22305.85 ❌
- **TP 4RR**: 22271.69 ❌
- **TP 15RR**: 21895.99 ❌
- **PnL**: -34.15 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 37.11 points

### Trade #252 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 03:00:00
- **FVG 5m**: 22409.34 - 22415.01
- **Entrée**: 22417.33 @ 2025-02-11 05:04:00
- **Stop Loss**: 22398.14
- **Risk**: 19.19 points
- **TP 1RR**: 22436.53 ✅
- **TP 2RR**: 22455.72 ❌
- **TP 3RR**: 22474.92 ❌
- **TP 4RR**: 22494.11 ❌
- **TP 15RR**: 22705.25 ❌
- **PnL**: -19.19 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 30.93 points

### Trade #253 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 08:30:00
- **FVG 5m**: 22491.56 - 22506.26
- **Entrée**: 22516.56 @ 2025-02-11 09:28:00
- **Stop Loss**: 22480.32
- **Risk**: 36.25 points
- **TP 1RR**: 22552.81 ❌
- **TP 2RR**: 22589.06 ❌
- **TP 3RR**: 22625.31 ❌
- **TP 4RR**: 22661.55 ❌
- **TP 15RR**: 23060.27 ❌
- **PnL**: -36.25 points (-1.0R)
- **MFE**: 32.22 points
- **MAE**: 38.66 points

### Trade #254 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 08:30:00
- **FVG 5m**: 22491.56 - 22506.26
- **Entrée**: 22516.56 @ 2025-02-11 09:28:00
- **Stop Loss**: 22480.32
- **Risk**: 36.25 points
- **TP 1RR**: 22552.81 ❌
- **TP 2RR**: 22589.06 ❌
- **TP 3RR**: 22625.31 ❌
- **TP 4RR**: 22661.55 ❌
- **TP 15RR**: 23060.27 ❌
- **PnL**: -36.25 points (-1.0R)
- **MFE**: 32.22 points
- **MAE**: 38.66 points

### Trade #255 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 08:30:00
- **FVG 5m**: 22491.56 - 22506.26
- **Entrée**: 22516.56 @ 2025-02-11 09:28:00
- **Stop Loss**: 22480.32
- **Risk**: 36.25 points
- **TP 1RR**: 22552.81 ❌
- **TP 2RR**: 22589.06 ❌
- **TP 3RR**: 22625.31 ❌
- **TP 4RR**: 22661.55 ❌
- **TP 15RR**: 23060.27 ❌
- **PnL**: -36.25 points (-1.0R)
- **MFE**: 32.22 points
- **MAE**: 38.66 points

### Trade #256 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 08:45:00
- **FVG 5m**: 22526.87 - 22533.83
- **Entrée**: 22526.36 @ 2025-02-11 09:57:00
- **Stop Loss**: 22545.10
- **Risk**: 18.74 points
- **TP 1RR**: 22507.62 ✅
- **TP 2RR**: 22488.88 ✅
- **TP 3RR**: 22470.13 ✅
- **TP 4RR**: 22451.39 ✅
- **TP 15RR**: 22245.24 ✅
- **PnL**: 281.12 points (15.0R)
- **MFE**: 293.83 points
- **MAE**: 3.87 points

### Trade #257 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 09:15:00
- **FVG 5m**: 22491.56 - 22506.26
- **Entrée**: 22516.56 @ 2025-02-11 09:28:00
- **Stop Loss**: 22480.32
- **Risk**: 36.25 points
- **TP 1RR**: 22552.81 ❌
- **TP 2RR**: 22589.06 ❌
- **TP 3RR**: 22625.31 ❌
- **TP 4RR**: 22661.55 ❌
- **TP 15RR**: 23060.27 ❌
- **PnL**: -36.25 points (-1.0R)
- **MFE**: 32.22 points
- **MAE**: 38.66 points

### Trade #258 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 10:45:00
- **FVG 5m**: 22466.82 - 22472.49
- **Entrée**: 22465.27 @ 2025-02-11 10:58:00
- **Stop Loss**: 22483.73
- **Risk**: 18.45 points
- **TP 1RR**: 22446.82 ✅
- **TP 2RR**: 22428.37 ✅
- **TP 3RR**: 22409.92 ✅
- **TP 4RR**: 22391.46 ✅
- **TP 15RR**: 22188.48 ❌
- **PnL**: -18.45 points (-1.0R)
- **MFE**: 77.06 points
- **MAE**: 22.68 points

### Trade #259 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 10:45:00
- **FVG 5m**: 22466.82 - 22472.49
- **Entrée**: 22465.27 @ 2025-02-11 10:58:00
- **Stop Loss**: 22483.73
- **Risk**: 18.45 points
- **TP 1RR**: 22446.82 ✅
- **TP 2RR**: 22428.37 ✅
- **TP 3RR**: 22409.92 ✅
- **TP 4RR**: 22391.46 ✅
- **TP 15RR**: 22188.48 ❌
- **PnL**: -18.45 points (-1.0R)
- **MFE**: 77.06 points
- **MAE**: 22.68 points

### Trade #260 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 03:30:00
- **FVG 5m**: 22442.59 - 22446.46
- **Entrée**: 22448.78 @ 2025-02-12 04:21:00
- **Stop Loss**: 22431.37
- **Risk**: 17.41 points
- **TP 1RR**: 22466.19 ✅
- **TP 2RR**: 22483.59 ✅
- **TP 3RR**: 22501.00 ✅
- **TP 4RR**: 22518.41 ✅
- **TP 15RR**: 22709.89 ❌
- **PnL**: -17.41 points (-1.0R)
- **MFE**: 77.84 points
- **MAE**: 216.25 points

### Trade #261 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 03:30:00
- **FVG 5m**: 22442.59 - 22446.46
- **Entrée**: 22448.78 @ 2025-02-12 04:21:00
- **Stop Loss**: 22431.37
- **Risk**: 17.41 points
- **TP 1RR**: 22466.19 ✅
- **TP 2RR**: 22483.59 ✅
- **TP 3RR**: 22501.00 ✅
- **TP 4RR**: 22518.41 ✅
- **TP 15RR**: 22709.89 ❌
- **PnL**: -17.41 points (-1.0R)
- **MFE**: 77.84 points
- **MAE**: 216.25 points

### Trade #262 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:00:00
- **FVG 5m**: 22501.62 - 22504.71
- **Entrée**: 22494.14 @ 2025-02-12 07:21:00
- **Stop Loss**: 22515.96
- **Risk**: 21.82 points
- **TP 1RR**: 22472.32 ❌
- **TP 2RR**: 22450.50 ❌
- **TP 3RR**: 22428.68 ❌
- **TP 4RR**: 22406.86 ❌
- **TP 15RR**: 22166.84 ❌
- **PnL**: -21.82 points (-1.0R)
- **MFE**: 261.61 points
- **MAE**: 32.48 points

### Trade #263 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:30:00
- **FVG 5m**: 22303.93 - 22340.27
- **Entrée**: 22292.85 @ 2025-02-12 09:03:00
- **Stop Loss**: 22351.44
- **Risk**: 58.59 points
- **TP 1RR**: 22234.25 ❌
- **TP 2RR**: 22175.66 ❌
- **TP 3RR**: 22117.06 ❌
- **TP 4RR**: 22058.47 ❌
- **TP 15RR**: 21413.93 ❌
- **PnL**: -58.59 points (-1.0R)
- **MFE**: 44.07 points
- **MAE**: 60.05 points

### Trade #264 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:30:00
- **FVG 5m**: 22303.93 - 22340.27
- **Entrée**: 22292.85 @ 2025-02-12 09:03:00
- **Stop Loss**: 22351.44
- **Risk**: 58.59 points
- **TP 1RR**: 22234.25 ❌
- **TP 2RR**: 22175.66 ❌
- **TP 3RR**: 22117.06 ❌
- **TP 4RR**: 22058.47 ❌
- **TP 15RR**: 21413.93 ❌
- **PnL**: -58.59 points (-1.0R)
- **MFE**: 44.07 points
- **MAE**: 60.05 points

### Trade #265 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:30:00
- **FVG 5m**: 22303.93 - 22340.27
- **Entrée**: 22292.85 @ 2025-02-12 09:03:00
- **Stop Loss**: 22351.44
- **Risk**: 58.59 points
- **TP 1RR**: 22234.25 ❌
- **TP 2RR**: 22175.66 ❌
- **TP 3RR**: 22117.06 ❌
- **TP 4RR**: 22058.47 ❌
- **TP 15RR**: 21413.93 ❌
- **PnL**: -58.59 points (-1.0R)
- **MFE**: 44.07 points
- **MAE**: 60.05 points

### Trade #266 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 08:30:00
- **FVG 5m**: 22296.71 - 22321.45
- **Entrée**: 22331.76 @ 2025-02-12 08:44:00
- **Stop Loss**: 22285.56
- **Risk**: 46.20 points
- **TP 1RR**: 22377.97 ❌
- **TP 2RR**: 22424.17 ❌
- **TP 3RR**: 22470.37 ❌
- **TP 4RR**: 22516.57 ❌
- **TP 15RR**: 23024.78 ❌
- **PnL**: -46.20 points (-1.0R)
- **MFE**: 41.24 points
- **MAE**: 50.26 points

### Trade #267 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 08:30:00
- **FVG 5m**: 22296.71 - 22321.45
- **Entrée**: 22331.76 @ 2025-02-12 08:44:00
- **Stop Loss**: 22285.56
- **Risk**: 46.20 points
- **TP 1RR**: 22377.97 ❌
- **TP 2RR**: 22424.17 ❌
- **TP 3RR**: 22470.37 ❌
- **TP 4RR**: 22516.57 ❌
- **TP 15RR**: 23024.78 ❌
- **PnL**: -46.20 points (-1.0R)
- **MFE**: 41.24 points
- **MAE**: 50.26 points

### Trade #268 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 08:45:00
- **FVG 5m**: 22293.88 - 22338.72
- **Entrée**: 22343.36 @ 2025-02-12 09:19:00
- **Stop Loss**: 22282.73
- **Risk**: 60.63 points
- **TP 1RR**: 22404.00 ✅
- **TP 2RR**: 22464.63 ✅
- **TP 3RR**: 22525.26 ✅
- **TP 4RR**: 22585.90 ✅
- **TP 15RR**: 23252.86 ❌
- **PnL**: -60.63 points (-1.0R)
- **MFE**: 667.55 points
- **MAE**: 69.33 points

### Trade #269 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 09:30:00
- **FVG 5m**: 22340.79 - 22348.78
- **Entrée**: 22354.19 @ 2025-02-12 10:31:00
- **Stop Loss**: 22329.61
- **Risk**: 24.57 points
- **TP 1RR**: 22378.76 ✅
- **TP 2RR**: 22403.33 ✅
- **TP 3RR**: 22427.91 ✅
- **TP 4RR**: 22452.48 ✅
- **TP 15RR**: 22722.78 ✅
- **PnL**: 368.59 points (15.0R)
- **MFE**: 371.66 points
- **MAE**: 13.92 points

### Trade #270 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 10:45:00
- **FVG 5m**: 22425.84 - 22448.01
- **Entrée**: 22452.64 @ 2025-02-12 10:58:00
- **Stop Loss**: 22414.63
- **Risk**: 38.02 points
- **TP 1RR**: 22490.66 ✅
- **TP 2RR**: 22528.68 ✅
- **TP 3RR**: 22566.70 ✅
- **TP 4RR**: 22604.72 ✅
- **TP 15RR**: 23022.92 ❌
- **PnL**: -38.02 points (-1.0R)
- **MFE**: 558.27 points
- **MAE**: 41.24 points

### Trade #271 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 11:45:00
- **FVG 5m**: 22478.16 - 22480.74
- **Entrée**: 22483.06 @ 2025-02-12 13:37:00
- **Stop Loss**: 22466.92
- **Risk**: 16.14 points
- **TP 1RR**: 22499.19 ✅
- **TP 2RR**: 22515.33 ❌
- **TP 3RR**: 22531.47 ❌
- **TP 4RR**: 22547.60 ❌
- **TP 15RR**: 22725.10 ❌
- **PnL**: -16.14 points (-1.0R)
- **MFE**: 32.22 points
- **MAE**: 17.01 points

### Trade #272 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 19:15:00
- **FVG 5m**: 22565.28 - 22568.37
- **Entrée**: 22556.77 @ 2025-02-12 20:05:00
- **Stop Loss**: 22579.66
- **Risk**: 22.88 points
- **TP 1RR**: 22533.89 ❌
- **TP 2RR**: 22511.01 ❌
- **TP 3RR**: 22488.12 ❌
- **TP 4RR**: 22465.24 ❌
- **TP 15RR**: 22213.53 ❌
- **PnL**: -22.88 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 22.94 points

### Trade #273 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 19:45:00
- **FVG 5m**: 22565.28 - 22568.37
- **Entrée**: 22556.77 @ 2025-02-12 20:05:00
- **Stop Loss**: 22579.66
- **Risk**: 22.88 points
- **TP 1RR**: 22533.89 ❌
- **TP 2RR**: 22511.01 ❌
- **TP 3RR**: 22488.12 ❌
- **TP 4RR**: 22465.24 ❌
- **TP 15RR**: 22213.53 ❌
- **PnL**: -22.88 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 22.94 points

### Trade #274 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 01:30:00
- **FVG 5m**: 22505.22 - 22518.63
- **Entrée**: 22504.71 @ 2025-02-13 02:14:00
- **Stop Loss**: 22529.89
- **Risk**: 25.18 points
- **TP 1RR**: 22479.53 ✅
- **TP 2RR**: 22454.35 ✅
- **TP 3RR**: 22429.18 ✅
- **TP 4RR**: 22404.00 ❌
- **TP 15RR**: 22127.05 ❌
- **PnL**: -25.18 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 28.35 points

### Trade #275 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 02:00:00
- **FVG 5m**: 22505.22 - 22518.63
- **Entrée**: 22504.71 @ 2025-02-13 02:14:00
- **Stop Loss**: 22529.89
- **Risk**: 25.18 points
- **TP 1RR**: 22479.53 ✅
- **TP 2RR**: 22454.35 ✅
- **TP 3RR**: 22429.18 ✅
- **TP 4RR**: 22404.00 ❌
- **TP 15RR**: 22127.05 ❌
- **PnL**: -25.18 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 28.35 points

### Trade #276 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 02:00:00
- **FVG 5m**: 22505.22 - 22518.63
- **Entrée**: 22504.71 @ 2025-02-13 02:14:00
- **Stop Loss**: 22529.89
- **Risk**: 25.18 points
- **TP 1RR**: 22479.53 ✅
- **TP 2RR**: 22454.35 ✅
- **TP 3RR**: 22429.18 ✅
- **TP 4RR**: 22404.00 ❌
- **TP 15RR**: 22127.05 ❌
- **PnL**: -25.18 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 28.35 points

### Trade #277 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 02:00:00
- **FVG 5m**: 22505.22 - 22518.63
- **Entrée**: 22504.71 @ 2025-02-13 02:14:00
- **Stop Loss**: 22529.89
- **Risk**: 25.18 points
- **TP 1RR**: 22479.53 ✅
- **TP 2RR**: 22454.35 ✅
- **TP 3RR**: 22429.18 ✅
- **TP 4RR**: 22404.00 ❌
- **TP 15RR**: 22127.05 ❌
- **PnL**: -25.18 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 28.35 points

### Trade #278 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 02:30:00
- **FVG 5m**: 22462.70 - 22470.43
- **Entrée**: 22476.61 @ 2025-02-13 03:12:00
- **Stop Loss**: 22451.47
- **Risk**: 25.15 points
- **TP 1RR**: 22501.76 ✅
- **TP 2RR**: 22526.91 ✅
- **TP 3RR**: 22552.06 ✅
- **TP 4RR**: 22577.21 ✅
- **TP 15RR**: 22853.86 ✅
- **PnL**: 377.24 points (15.0R)
- **MFE**: 381.72 points
- **MAE**: 14.69 points

### Trade #279 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 03:30:00
- **FVG 5m**: 22512.96 - 22523.52
- **Entrée**: 22507.54 @ 2025-02-13 05:46:00
- **Stop Loss**: 22534.79
- **Risk**: 27.24 points
- **TP 1RR**: 22480.30 ✅
- **TP 2RR**: 22453.06 ❌
- **TP 3RR**: 22425.82 ❌
- **TP 4RR**: 22398.58 ❌
- **TP 15RR**: 22098.92 ❌
- **PnL**: -27.24 points (-1.0R)
- **MFE**: 44.85 points
- **MAE**: 71.39 points

### Trade #280 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 07:30:00
- **FVG 5m**: 22572.75 - 22592.08
- **Entrée**: 22593.37 @ 2025-02-13 08:56:00
- **Stop Loss**: 22561.47
- **Risk**: 31.91 points
- **TP 1RR**: 22625.28 ✅
- **TP 2RR**: 22657.18 ❌
- **TP 3RR**: 22689.09 ❌
- **TP 4RR**: 22720.99 ❌
- **TP 15RR**: 23071.96 ❌
- **PnL**: -31.91 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 39.18 points

### Trade #281 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 08:30:00
- **FVG 5m**: 22686.42 - 22699.30
- **Entrée**: 22682.55 @ 2025-02-13 10:28:00
- **Stop Loss**: 22710.65
- **Risk**: 28.10 points
- **TP 1RR**: 22654.45 ✅
- **TP 2RR**: 22626.34 ✅
- **TP 3RR**: 22598.24 ✅
- **TP 4RR**: 22570.14 ✅
- **TP 15RR**: 22261.01 ❌
- **PnL**: -28.10 points (-1.0R)
- **MFE**: 114.18 points
- **MAE**: 33.25 points

### Trade #282 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 08:30:00
- **FVG 5m**: 22686.42 - 22699.30
- **Entrée**: 22682.55 @ 2025-02-13 10:28:00
- **Stop Loss**: 22710.65
- **Risk**: 28.10 points
- **TP 1RR**: 22654.45 ✅
- **TP 2RR**: 22626.34 ✅
- **TP 3RR**: 22598.24 ✅
- **TP 4RR**: 22570.14 ✅
- **TP 15RR**: 22261.01 ❌
- **PnL**: -28.10 points (-1.0R)
- **MFE**: 114.18 points
- **MAE**: 33.25 points

### Trade #283 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 08:30:00
- **FVG 5m**: 22686.42 - 22699.30
- **Entrée**: 22682.55 @ 2025-02-13 10:28:00
- **Stop Loss**: 22710.65
- **Risk**: 28.10 points
- **TP 1RR**: 22654.45 ✅
- **TP 2RR**: 22626.34 ✅
- **TP 3RR**: 22598.24 ✅
- **TP 4RR**: 22570.14 ✅
- **TP 15RR**: 22261.01 ❌
- **PnL**: -28.10 points (-1.0R)
- **MFE**: 114.18 points
- **MAE**: 33.25 points

### Trade #284 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 09:15:00
- **FVG 5m**: 22676.11 - 22710.90
- **Entrée**: 22713.99 @ 2025-02-13 09:39:00
- **Stop Loss**: 22664.77
- **Risk**: 49.23 points
- **TP 1RR**: 22763.22 ❌
- **TP 2RR**: 22812.45 ❌
- **TP 3RR**: 22861.67 ❌
- **TP 4RR**: 22910.90 ❌
- **TP 15RR**: 23452.39 ❌
- **PnL**: -49.23 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 49.49 points

### Trade #285 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 10:45:00
- **FVG 5m**: 22649.56 - 22655.75
- **Entrée**: 22641.57 @ 2025-02-13 11:57:00
- **Stop Loss**: 22667.07
- **Risk**: 25.50 points
- **TP 1RR**: 22616.07 ✅
- **TP 2RR**: 22590.56 ✅
- **TP 3RR**: 22565.06 ❌
- **TP 4RR**: 22539.55 ❌
- **TP 15RR**: 22259.01 ❌
- **PnL**: -25.50 points (-1.0R)
- **MFE**: 73.20 points
- **MAE**: 32.22 points

### Trade #286 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 10:45:00
- **FVG 5m**: 22649.56 - 22655.75
- **Entrée**: 22641.57 @ 2025-02-13 11:57:00
- **Stop Loss**: 22667.07
- **Risk**: 25.50 points
- **TP 1RR**: 22616.07 ✅
- **TP 2RR**: 22590.56 ✅
- **TP 3RR**: 22565.06 ❌
- **TP 4RR**: 22539.55 ❌
- **TP 15RR**: 22259.01 ❌
- **PnL**: -25.50 points (-1.0R)
- **MFE**: 73.20 points
- **MAE**: 32.22 points

### Trade #287 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 12:30:00
- **FVG 5m**: 22658.32 - 22668.89
- **Entrée**: 22669.15 @ 2025-02-13 12:57:00
- **Stop Loss**: 22646.99
- **Risk**: 22.15 points
- **TP 1RR**: 22691.30 ✅
- **TP 2RR**: 22713.46 ✅
- **TP 3RR**: 22735.61 ✅
- **TP 4RR**: 22757.77 ✅
- **TP 15RR**: 23001.46 ✅
- **PnL**: 332.31 points (15.0R)
- **MFE**: 334.55 points
- **MAE**: 0.26 points

### Trade #288 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 12:45:00
- **FVG 5m**: 22658.32 - 22668.89
- **Entrée**: 22669.15 @ 2025-02-13 12:57:00
- **Stop Loss**: 22646.99
- **Risk**: 22.15 points
- **TP 1RR**: 22691.30 ✅
- **TP 2RR**: 22713.46 ✅
- **TP 3RR**: 22735.61 ✅
- **TP 4RR**: 22757.77 ✅
- **TP 15RR**: 23001.46 ✅
- **PnL**: 332.31 points (15.0R)
- **MFE**: 334.55 points
- **MAE**: 0.26 points

### Trade #289 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 13:45:00
- **FVG 5m**: 22764.25 - 22766.57
- **Entrée**: 22761.93 @ 2025-02-13 15:19:00
- **Stop Loss**: 22777.96
- **Risk**: 16.02 points
- **TP 1RR**: 22745.91 ❌
- **TP 2RR**: 22729.89 ❌
- **TP 3RR**: 22713.87 ❌
- **TP 4RR**: 22697.84 ❌
- **TP 15RR**: 22521.60 ❌
- **PnL**: -16.02 points (-1.0R)
- **MFE**: 8.51 points
- **MAE**: 19.59 points

### Trade #290 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 15:00:00
- **FVG 5m**: 22764.25 - 22766.57
- **Entrée**: 22761.93 @ 2025-02-13 15:19:00
- **Stop Loss**: 22777.96
- **Risk**: 16.02 points
- **TP 1RR**: 22745.91 ❌
- **TP 2RR**: 22729.89 ❌
- **TP 3RR**: 22713.87 ❌
- **TP 4RR**: 22697.84 ❌
- **TP 15RR**: 22521.60 ❌
- **PnL**: -16.02 points (-1.0R)
- **MFE**: 8.51 points
- **MAE**: 19.59 points

### Trade #291 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 15:45:00
- **FVG 5m**: 22769.41 - 22779.46
- **Entrée**: 22766.57 @ 2025-02-13 17:34:00
- **Stop Loss**: 22790.85
- **Risk**: 24.28 points
- **TP 1RR**: 22742.30 ❌
- **TP 2RR**: 22718.02 ❌
- **TP 3RR**: 22693.74 ❌
- **TP 4RR**: 22669.47 ❌
- **TP 15RR**: 22402.42 ❌
- **PnL**: -24.28 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 29.12 points

### Trade #292 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-14 06:00:00
- **FVG 5m**: 22748.02 - 22759.36
- **Entrée**: 22760.39 @ 2025-02-14 06:12:00
- **Stop Loss**: 22736.64
- **Risk**: 23.75 points
- **TP 1RR**: 22784.13 ✅
- **TP 2RR**: 22807.88 ✅
- **TP 3RR**: 22831.63 ✅
- **TP 4RR**: 22855.37 ✅
- **TP 15RR**: 23116.57 ❌
- **PnL**: -23.75 points (-1.0R)
- **MFE**: 250.52 points
- **MAE**: 37.89 points

### Trade #293 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-14 07:30:00
- **FVG 5m**: 22794.93 - 22804.46
- **Entrée**: 22807.30 @ 2025-02-14 08:47:00
- **Stop Loss**: 22783.53
- **Risk**: 23.77 points
- **TP 1RR**: 22831.07 ❌
- **TP 2RR**: 22854.84 ❌
- **TP 3RR**: 22878.60 ❌
- **TP 4RR**: 22902.37 ❌
- **TP 15RR**: 23163.83 ❌
- **PnL**: -23.77 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 23.97 points

### Trade #294 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-17 02:15:00
- **FVG 5m**: 22927.66 - 22933.33
- **Entrée**: 22926.89 @ 2025-02-17 02:28:00
- **Stop Loss**: 22944.80
- **Risk**: 17.91 points
- **TP 1RR**: 22908.98 ❌
- **TP 2RR**: 22891.07 ❌
- **TP 3RR**: 22873.16 ❌
- **TP 4RR**: 22855.25 ❌
- **TP 15RR**: 22658.24 ❌
- **PnL**: -17.91 points (-1.0R)
- **MFE**: 13.66 points
- **MAE**: 20.10 points

### Trade #295 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 05:30:00
- **FVG 5m**: 22965.29 - 22968.39
- **Entrée**: 22964.78 @ 2025-02-18 05:42:00
- **Stop Loss**: 22979.87
- **Risk**: 15.09 points
- **TP 1RR**: 22949.68 ❌
- **TP 2RR**: 22934.59 ❌
- **TP 3RR**: 22919.50 ❌
- **TP 4RR**: 22904.41 ❌
- **TP 15RR**: 22738.39 ❌
- **PnL**: -15.09 points (-1.0R)
- **MFE**: 7.99 points
- **MAE**: 15.21 points

### Trade #296 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22957.56 - 22994.42
- **Entrée**: 22954.98 @ 2025-02-18 08:28:00
- **Stop Loss**: 23005.92
- **Risk**: 50.93 points
- **TP 1RR**: 22904.05 ✅
- **TP 2RR**: 22853.12 ✅
- **TP 3RR**: 22802.19 ✅
- **TP 4RR**: 22751.26 ✅
- **TP 15RR**: 22191.01 ✅
- **PnL**: 763.98 points (15.0R)
- **MFE**: 774.26 points
- **MAE**: 35.31 points

### Trade #297 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22957.56 - 22994.42
- **Entrée**: 22954.98 @ 2025-02-18 08:28:00
- **Stop Loss**: 23005.92
- **Risk**: 50.93 points
- **TP 1RR**: 22904.05 ✅
- **TP 2RR**: 22853.12 ✅
- **TP 3RR**: 22802.19 ✅
- **TP 4RR**: 22751.26 ✅
- **TP 15RR**: 22191.01 ✅
- **PnL**: 763.98 points (15.0R)
- **MFE**: 774.26 points
- **MAE**: 35.31 points

### Trade #298 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22957.56 - 22994.42
- **Entrée**: 22954.98 @ 2025-02-18 08:28:00
- **Stop Loss**: 23005.92
- **Risk**: 50.93 points
- **TP 1RR**: 22904.05 ✅
- **TP 2RR**: 22853.12 ✅
- **TP 3RR**: 22802.19 ✅
- **TP 4RR**: 22751.26 ✅
- **TP 15RR**: 22191.01 ✅
- **PnL**: 763.98 points (15.0R)
- **MFE**: 774.26 points
- **MAE**: 35.31 points

### Trade #299 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22957.56 - 22994.42
- **Entrée**: 22954.98 @ 2025-02-18 08:28:00
- **Stop Loss**: 23005.92
- **Risk**: 50.93 points
- **TP 1RR**: 22904.05 ✅
- **TP 2RR**: 22853.12 ✅
- **TP 3RR**: 22802.19 ✅
- **TP 4RR**: 22751.26 ✅
- **TP 15RR**: 22191.01 ✅
- **PnL**: 763.98 points (15.0R)
- **MFE**: 774.26 points
- **MAE**: 35.31 points

### Trade #300 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:30:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22902.51
- **Risk**: 29.23 points
- **TP 1RR**: 22844.05 ✅
- **TP 2RR**: 22814.82 ✅
- **TP 3RR**: 22785.59 ❌
- **TP 4RR**: 22756.36 ❌
- **TP 15RR**: 22434.83 ❌
- **PnL**: -29.23 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 30.67 points

### Trade #301 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 08:45:00
- **FVG 5m**: 22854.46 - 22856.78
- **Entrée**: 22859.36 @ 2025-02-18 09:52:00
- **Stop Loss**: 22843.04
- **Risk**: 16.32 points
- **TP 1RR**: 22875.69 ✅
- **TP 2RR**: 22892.01 ✅
- **TP 3RR**: 22908.33 ❌
- **TP 4RR**: 22924.66 ❌
- **TP 15RR**: 23104.23 ❌
- **PnL**: -16.32 points (-1.0R)
- **MFE**: 44.33 points
- **MAE**: 21.39 points

### Trade #302 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 08:45:00
- **FVG 5m**: 22854.46 - 22856.78
- **Entrée**: 22859.36 @ 2025-02-18 09:52:00
- **Stop Loss**: 22843.04
- **Risk**: 16.32 points
- **TP 1RR**: 22875.69 ✅
- **TP 2RR**: 22892.01 ✅
- **TP 3RR**: 22908.33 ❌
- **TP 4RR**: 22924.66 ❌
- **TP 15RR**: 23104.23 ❌
- **PnL**: -16.32 points (-1.0R)
- **MFE**: 44.33 points
- **MAE**: 21.39 points

### Trade #303 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22902.51
- **Risk**: 29.23 points
- **TP 1RR**: 22844.05 ✅
- **TP 2RR**: 22814.82 ✅
- **TP 3RR**: 22785.59 ❌
- **TP 4RR**: 22756.36 ❌
- **TP 15RR**: 22434.83 ❌
- **PnL**: -29.23 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 30.67 points

### Trade #304 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22902.51
- **Risk**: 29.23 points
- **TP 1RR**: 22844.05 ✅
- **TP 2RR**: 22814.82 ✅
- **TP 3RR**: 22785.59 ❌
- **TP 4RR**: 22756.36 ❌
- **TP 15RR**: 22434.83 ❌
- **PnL**: -29.23 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 30.67 points

### Trade #305 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22902.51
- **Risk**: 29.23 points
- **TP 1RR**: 22844.05 ✅
- **TP 2RR**: 22814.82 ✅
- **TP 3RR**: 22785.59 ❌
- **TP 4RR**: 22756.36 ❌
- **TP 15RR**: 22434.83 ❌
- **PnL**: -29.23 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 30.67 points

### Trade #306 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22902.51
- **Risk**: 29.23 points
- **TP 1RR**: 22844.05 ✅
- **TP 2RR**: 22814.82 ✅
- **TP 3RR**: 22785.59 ❌
- **TP 4RR**: 22756.36 ❌
- **TP 15RR**: 22434.83 ❌
- **PnL**: -29.23 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 30.67 points

### Trade #307 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22902.51
- **Risk**: 29.23 points
- **TP 1RR**: 22844.05 ✅
- **TP 2RR**: 22814.82 ✅
- **TP 3RR**: 22785.59 ❌
- **TP 4RR**: 22756.36 ❌
- **TP 15RR**: 22434.83 ❌
- **PnL**: -29.23 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 30.67 points

### Trade #308 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 13:15:00
- **FVG 5m**: 22849.31 - 22855.75
- **Entrée**: 22861.68 @ 2025-02-18 13:49:00
- **Stop Loss**: 22837.88
- **Risk**: 23.80 points
- **TP 1RR**: 22885.48 ✅
- **TP 2RR**: 22909.27 ✅
- **TP 3RR**: 22933.07 ✅
- **TP 4RR**: 22956.87 ✅
- **TP 15RR**: 23218.62 ❌
- **PnL**: -23.80 points (-1.0R)
- **MFE**: 119.85 points
- **MAE**: 28.61 points

### Trade #309 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 14:45:00
- **FVG 5m**: 22886.42 - 22921.99
- **Entrée**: 22927.41 @ 2025-02-18 14:59:00
- **Stop Loss**: 22874.98
- **Risk**: 52.42 points
- **TP 1RR**: 22979.83 ✅
- **TP 2RR**: 23032.25 ❌
- **TP 3RR**: 23084.68 ❌
- **TP 4RR**: 23137.10 ❌
- **TP 15RR**: 23713.77 ❌
- **PnL**: -52.42 points (-1.0R)
- **MFE**: 54.13 points
- **MAE**: 61.08 points

### Trade #310 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 14:45:00
- **FVG 5m**: 22886.42 - 22921.99
- **Entrée**: 22927.41 @ 2025-02-18 14:59:00
- **Stop Loss**: 22874.98
- **Risk**: 52.42 points
- **TP 1RR**: 22979.83 ✅
- **TP 2RR**: 23032.25 ❌
- **TP 3RR**: 23084.68 ❌
- **TP 4RR**: 23137.10 ❌
- **TP 15RR**: 23713.77 ❌
- **PnL**: -52.42 points (-1.0R)
- **MFE**: 54.13 points
- **MAE**: 61.08 points

### Trade #311 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 02:30:00
- **FVG 5m**: 22904.21 - 22906.53
- **Entrée**: 22907.30 @ 2025-02-19 04:53:00
- **Stop Loss**: 22892.76
- **Risk**: 14.55 points
- **TP 1RR**: 22921.85 ❌
- **TP 2RR**: 22936.39 ❌
- **TP 3RR**: 22950.94 ❌
- **TP 4RR**: 22965.48 ❌
- **TP 15RR**: 23125.48 ❌
- **PnL**: -14.55 points (-1.0R)
- **MFE**: 6.44 points
- **MAE**: 14.95 points

### Trade #312 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 07:15:00
- **FVG 5m**: 22884.36 - 22890.03
- **Entrée**: 22891.84 @ 2025-02-19 07:48:00
- **Stop Loss**: 22872.92
- **Risk**: 18.92 points
- **TP 1RR**: 22910.75 ❌
- **TP 2RR**: 22929.67 ❌
- **TP 3RR**: 22948.59 ❌
- **TP 4RR**: 22967.50 ❌
- **TP 15RR**: 23175.59 ❌
- **PnL**: -18.92 points (-1.0R)
- **MFE**: 15.72 points
- **MAE**: 22.94 points

### Trade #313 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 12:00:00
- **FVG 5m**: 22935.40 - 22938.75
- **Entrée**: 22934.36 @ 2025-02-19 12:48:00
- **Stop Loss**: 22950.22
- **Risk**: 15.85 points
- **TP 1RR**: 22918.51 ✅
- **TP 2RR**: 22902.66 ❌
- **TP 3RR**: 22886.81 ❌
- **TP 4RR**: 22870.96 ❌
- **TP 15RR**: 22696.60 ❌
- **PnL**: -15.85 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 25.52 points

### Trade #314 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22923.67
- **Risk**: 35.95 points
- **TP 1RR**: 22995.58 ❌
- **TP 2RR**: 23031.53 ❌
- **TP 3RR**: 23067.48 ❌
- **TP 4RR**: 23103.43 ❌
- **TP 15RR**: 23498.92 ❌
- **PnL**: -35.95 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 43.82 points

### Trade #315 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22923.67
- **Risk**: 35.95 points
- **TP 1RR**: 22995.58 ❌
- **TP 2RR**: 23031.53 ❌
- **TP 3RR**: 23067.48 ❌
- **TP 4RR**: 23103.43 ❌
- **TP 15RR**: 23498.92 ❌
- **PnL**: -35.95 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 43.82 points

### Trade #316 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22923.67
- **Risk**: 35.95 points
- **TP 1RR**: 22995.58 ❌
- **TP 2RR**: 23031.53 ❌
- **TP 3RR**: 23067.48 ❌
- **TP 4RR**: 23103.43 ❌
- **TP 15RR**: 23498.92 ❌
- **PnL**: -35.95 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 43.82 points

### Trade #317 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22923.67
- **Risk**: 35.95 points
- **TP 1RR**: 22995.58 ❌
- **TP 2RR**: 23031.53 ❌
- **TP 3RR**: 23067.48 ❌
- **TP 4RR**: 23103.43 ❌
- **TP 15RR**: 23498.92 ❌
- **PnL**: -35.95 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 43.82 points

### Trade #318 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22923.67
- **Risk**: 35.95 points
- **TP 1RR**: 22995.58 ❌
- **TP 2RR**: 23031.53 ❌
- **TP 3RR**: 23067.48 ❌
- **TP 4RR**: 23103.43 ❌
- **TP 15RR**: 23498.92 ❌
- **PnL**: -35.95 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 43.82 points

### Trade #319 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22923.67
- **Risk**: 35.95 points
- **TP 1RR**: 22995.58 ❌
- **TP 2RR**: 23031.53 ❌
- **TP 3RR**: 23067.48 ❌
- **TP 4RR**: 23103.43 ❌
- **TP 15RR**: 23498.92 ❌
- **PnL**: -35.95 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 43.82 points

### Trade #320 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 13:15:00
- **FVG 5m**: 22973.03 - 22982.56
- **Entrée**: 22970.71 @ 2025-02-19 14:02:00
- **Stop Loss**: 22994.05
- **Risk**: 23.35 points
- **TP 1RR**: 22947.36 ✅
- **TP 2RR**: 22924.01 ✅
- **TP 3RR**: 22900.66 ✅
- **TP 4RR**: 22877.32 ✅
- **TP 15RR**: 22620.49 ✅
- **PnL**: 350.21 points (15.0R)
- **MFE**: 350.53 points
- **MAE**: 4.90 points

### Trade #321 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 14:00:00
- **FVG 5m**: 22944.42 - 22947.77
- **Entrée**: 22938.23 @ 2025-02-19 14:26:00
- **Stop Loss**: 22959.24
- **Risk**: 21.01 points
- **TP 1RR**: 22917.22 ✅
- **TP 2RR**: 22896.21 ✅
- **TP 3RR**: 22875.20 ✅
- **TP 4RR**: 22854.19 ✅
- **TP 15RR**: 22623.08 ✅
- **PnL**: 315.15 points (15.0R)
- **MFE**: 318.05 points
- **MAE**: 9.54 points

### Trade #322 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 14:15:00
- **FVG 5m**: 22944.42 - 22947.77
- **Entrée**: 22938.23 @ 2025-02-19 14:26:00
- **Stop Loss**: 22959.24
- **Risk**: 21.01 points
- **TP 1RR**: 22917.22 ✅
- **TP 2RR**: 22896.21 ✅
- **TP 3RR**: 22875.20 ✅
- **TP 4RR**: 22854.19 ✅
- **TP 15RR**: 22623.08 ✅
- **PnL**: 315.15 points (15.0R)
- **MFE**: 318.05 points
- **MAE**: 9.54 points

### Trade #323 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 01:15:00
- **FVG 5m**: 22852.40 - 22861.94
- **Entrée**: 22868.90 @ 2025-02-20 02:28:00
- **Stop Loss**: 22840.98
- **Risk**: 27.92 points
- **TP 1RR**: 22896.82 ✅
- **TP 2RR**: 22924.74 ❌
- **TP 3RR**: 22952.66 ❌
- **TP 4RR**: 22980.58 ❌
- **TP 15RR**: 23287.72 ❌
- **PnL**: -27.92 points (-1.0R)
- **MFE**: 44.85 points
- **MAE**: 32.48 points

### Trade #324 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 06:45:00
- **FVG 5m**: 22886.68 - 22889.52
- **Entrée**: 22891.06 @ 2025-02-20 07:59:00
- **Stop Loss**: 22875.24
- **Risk**: 15.82 points
- **TP 1RR**: 22906.89 ✅
- **TP 2RR**: 22922.71 ❌
- **TP 3RR**: 22938.54 ❌
- **TP 4RR**: 22954.36 ❌
- **TP 15RR**: 23128.44 ❌
- **PnL**: -15.82 points (-1.0R)
- **MFE**: 22.68 points
- **MAE**: 24.23 points

### Trade #325 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-20 08:45:00
- **FVG 5m**: 22719.92 - 22722.50
- **Entrée**: 22714.77 @ 2025-02-20 08:58:00
- **Stop Loss**: 22733.86
- **Risk**: 19.09 points
- **TP 1RR**: 22695.67 ✅
- **TP 2RR**: 22676.58 ✅
- **TP 3RR**: 22657.49 ✅
- **TP 4RR**: 22638.39 ✅
- **TP 15RR**: 22428.37 ❌
- **PnL**: -19.09 points (-1.0R)
- **MFE**: 84.02 points
- **MAE**: 32.48 points

### Trade #326 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 10:00:00
- **FVG 5m**: 22724.30 - 22744.92
- **Entrée**: 22747.24 @ 2025-02-20 11:04:00
- **Stop Loss**: 22712.94
- **Risk**: 34.30 points
- **TP 1RR**: 22781.54 ✅
- **TP 2RR**: 22815.85 ❌
- **TP 3RR**: 22850.15 ❌
- **TP 4RR**: 22884.45 ❌
- **TP 15RR**: 23261.76 ❌
- **PnL**: -34.30 points (-1.0R)
- **MFE**: 35.05 points
- **MAE**: 37.11 points

### Trade #327 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 11:30:00
- **FVG 5m**: 22737.96 - 22745.44
- **Entrée**: 22746.73 @ 2025-02-20 12:57:00
- **Stop Loss**: 22726.60
- **Risk**: 20.13 points
- **TP 1RR**: 22766.86 ✅
- **TP 2RR**: 22786.99 ✅
- **TP 3RR**: 22807.12 ✅
- **TP 4RR**: 22827.26 ✅
- **TP 15RR**: 23048.71 ❌
- **PnL**: -20.13 points (-1.0R)
- **MFE**: 187.64 points
- **MAE**: 27.84 points

### Trade #328 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-20 13:15:00
- **FVG 5m**: 22780.75 - 22786.16
- **Entrée**: 22777.66 @ 2025-02-20 13:27:00
- **Stop Loss**: 22797.56
- **Risk**: 19.90 points
- **TP 1RR**: 22757.76 ✅
- **TP 2RR**: 22737.86 ❌
- **TP 3RR**: 22717.96 ❌
- **TP 4RR**: 22698.06 ❌
- **TP 15RR**: 22479.18 ❌
- **PnL**: -19.90 points (-1.0R)
- **MFE**: 38.66 points
- **MAE**: 21.91 points

### Trade #329 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 13:45:00
- **FVG 5m**: 22824.82 - 22828.69
- **Entrée**: 22831.53 @ 2025-02-20 17:02:00
- **Stop Loss**: 22813.41
- **Risk**: 18.11 points
- **TP 1RR**: 22849.64 ✅
- **TP 2RR**: 22867.75 ❌
- **TP 3RR**: 22885.87 ❌
- **TP 4RR**: 22903.98 ❌
- **TP 15RR**: 23103.23 ❌
- **PnL**: -18.11 points (-1.0R)
- **MFE**: 29.64 points
- **MAE**: 18.30 points

### Trade #330 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 14:45:00
- **FVG 5m**: 22824.82 - 22828.69
- **Entrée**: 22831.53 @ 2025-02-20 17:02:00
- **Stop Loss**: 22813.41
- **Risk**: 18.11 points
- **TP 1RR**: 22849.64 ✅
- **TP 2RR**: 22867.75 ❌
- **TP 3RR**: 22885.87 ❌
- **TP 4RR**: 22903.98 ❌
- **TP 15RR**: 23103.23 ❌
- **PnL**: -18.11 points (-1.0R)
- **MFE**: 29.64 points
- **MAE**: 18.30 points

### Trade #331 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 02:15:00
- **FVG 5m**: 22837.20 - 22841.06
- **Entrée**: 22845.19 @ 2025-02-21 03:19:00
- **Stop Loss**: 22825.78
- **Risk**: 19.41 points
- **TP 1RR**: 22864.59 ✅
- **TP 2RR**: 22884.00 ✅
- **TP 3RR**: 22903.41 ✅
- **TP 4RR**: 22922.82 ✅
- **TP 15RR**: 23136.31 ❌
- **PnL**: -19.41 points (-1.0R)
- **MFE**: 89.18 points
- **MAE**: 26.03 points

### Trade #332 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 02:15:00
- **FVG 5m**: 22837.20 - 22841.06
- **Entrée**: 22845.19 @ 2025-02-21 03:19:00
- **Stop Loss**: 22825.78
- **Risk**: 19.41 points
- **TP 1RR**: 22864.59 ✅
- **TP 2RR**: 22884.00 ✅
- **TP 3RR**: 22903.41 ✅
- **TP 4RR**: 22922.82 ✅
- **TP 15RR**: 23136.31 ❌
- **PnL**: -19.41 points (-1.0R)
- **MFE**: 89.18 points
- **MAE**: 26.03 points

### Trade #333 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 06:00:00
- **FVG 5m**: 22870.19 - 22880.24
- **Entrée**: 22881.27 @ 2025-02-21 06:19:00
- **Stop Loss**: 22858.75
- **Risk**: 22.52 points
- **TP 1RR**: 22903.79 ✅
- **TP 2RR**: 22926.31 ✅
- **TP 3RR**: 22948.82 ❌
- **TP 4RR**: 22971.34 ❌
- **TP 15RR**: 23219.04 ❌
- **PnL**: -22.52 points (-1.0R)
- **MFE**: 53.09 points
- **MAE**: 37.11 points

### Trade #334 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 06:15:00
- **FVG 5m**: 22896.73 - 22900.34
- **Entrée**: 22903.69 @ 2025-02-21 06:42:00
- **Stop Loss**: 22885.29
- **Risk**: 18.41 points
- **TP 1RR**: 22922.10 ✅
- **TP 2RR**: 22940.51 ❌
- **TP 3RR**: 22958.91 ❌
- **TP 4RR**: 22977.32 ❌
- **TP 15RR**: 23179.80 ❌
- **PnL**: -18.41 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 20.10 points

### Trade #335 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 07:45:00
- **FVG 5m**: 22875.08 - 22900.08
- **Entrée**: 22872.76 @ 2025-02-21 08:29:00
- **Stop Loss**: 22911.53
- **Risk**: 38.77 points
- **TP 1RR**: 22833.99 ✅
- **TP 2RR**: 22795.22 ✅
- **TP 3RR**: 22756.45 ✅
- **TP 4RR**: 22717.68 ✅
- **TP 15RR**: 22291.20 ✅
- **PnL**: 581.56 points (15.0R)
- **MFE**: 598.73 points
- **MAE**: 2.32 points

### Trade #336 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 07:45:00
- **FVG 5m**: 22875.08 - 22900.08
- **Entrée**: 22872.76 @ 2025-02-21 08:29:00
- **Stop Loss**: 22911.53
- **Risk**: 38.77 points
- **TP 1RR**: 22833.99 ✅
- **TP 2RR**: 22795.22 ✅
- **TP 3RR**: 22756.45 ✅
- **TP 4RR**: 22717.68 ✅
- **TP 15RR**: 22291.20 ✅
- **PnL**: 581.56 points (15.0R)
- **MFE**: 598.73 points
- **MAE**: 2.32 points

### Trade #337 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:15:00
- **FVG 5m**: 22875.08 - 22900.08
- **Entrée**: 22872.76 @ 2025-02-21 08:29:00
- **Stop Loss**: 22911.53
- **Risk**: 38.77 points
- **TP 1RR**: 22833.99 ✅
- **TP 2RR**: 22795.22 ✅
- **TP 3RR**: 22756.45 ✅
- **TP 4RR**: 22717.68 ✅
- **TP 15RR**: 22291.20 ✅
- **PnL**: 581.56 points (15.0R)
- **MFE**: 598.73 points
- **MAE**: 2.32 points

### Trade #338 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:30:00
- **FVG 5m**: 22721.73 - 22747.76
- **Entrée**: 22717.09 @ 2025-02-21 09:23:00
- **Stop Loss**: 22759.13
- **Risk**: 42.05 points
- **TP 1RR**: 22675.04 ✅
- **TP 2RR**: 22633.00 ✅
- **TP 3RR**: 22590.95 ✅
- **TP 4RR**: 22548.91 ✅
- **TP 15RR**: 22086.41 ✅
- **PnL**: 630.68 points (15.0R)
- **MFE**: 630.69 points
- **MAE**: 4.64 points

### Trade #339 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:30:00
- **FVG 5m**: 22721.73 - 22747.76
- **Entrée**: 22717.09 @ 2025-02-21 09:23:00
- **Stop Loss**: 22759.13
- **Risk**: 42.05 points
- **TP 1RR**: 22675.04 ✅
- **TP 2RR**: 22633.00 ✅
- **TP 3RR**: 22590.95 ✅
- **TP 4RR**: 22548.91 ✅
- **TP 15RR**: 22086.41 ✅
- **PnL**: 630.68 points (15.0R)
- **MFE**: 630.69 points
- **MAE**: 4.64 points

### Trade #340 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:30:00
- **FVG 5m**: 22721.73 - 22747.76
- **Entrée**: 22717.09 @ 2025-02-21 09:23:00
- **Stop Loss**: 22759.13
- **Risk**: 42.05 points
- **TP 1RR**: 22675.04 ✅
- **TP 2RR**: 22633.00 ✅
- **TP 3RR**: 22590.95 ✅
- **TP 4RR**: 22548.91 ✅
- **TP 15RR**: 22086.41 ✅
- **PnL**: 630.68 points (15.0R)
- **MFE**: 630.69 points
- **MAE**: 4.64 points

### Trade #341 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 11:45:00
- **FVG 5m**: 22531.00 - 22535.38
- **Entrée**: 22529.19 @ 2025-02-21 11:56:00
- **Stop Loss**: 22546.65
- **Risk**: 17.45 points
- **TP 1RR**: 22511.74 ✅
- **TP 2RR**: 22494.29 ✅
- **TP 3RR**: 22476.83 ✅
- **TP 4RR**: 22459.38 ✅
- **TP 15RR**: 22267.39 ✅
- **PnL**: 261.80 points (15.0R)
- **MFE**: 273.21 points
- **MAE**: 3.61 points

### Trade #342 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-23 19:30:00
- **FVG 5m**: 22421.20 - 22426.87
- **Entrée**: 22433.57 @ 2025-02-23 20:05:00
- **Stop Loss**: 22409.99
- **Risk**: 23.58 points
- **TP 1RR**: 22457.15 ✅
- **TP 2RR**: 22480.74 ❌
- **TP 3RR**: 22504.32 ❌
- **TP 4RR**: 22527.90 ❌
- **TP 15RR**: 22787.31 ❌
- **PnL**: -23.58 points (-1.0R)
- **MFE**: 43.04 points
- **MAE**: 29.12 points

### Trade #343 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 02:15:00
- **FVG 5m**: 22413.21 - 22417.59
- **Entrée**: 22418.37 @ 2025-02-24 02:42:00
- **Stop Loss**: 22402.00
- **Risk**: 16.36 points
- **TP 1RR**: 22434.73 ✅
- **TP 2RR**: 22451.09 ✅
- **TP 3RR**: 22467.45 ✅
- **TP 4RR**: 22483.81 ✅
- **TP 15RR**: 22663.79 ❌
- **PnL**: -16.36 points (-1.0R)
- **MFE**: 70.11 points
- **MAE**: 23.97 points

### Trade #344 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 02:45:00
- **FVG 5m**: 22453.42 - 22457.03
- **Entrée**: 22459.86 @ 2025-02-24 03:01:00
- **Stop Loss**: 22442.19
- **Risk**: 17.67 points
- **TP 1RR**: 22477.53 ✅
- **TP 2RR**: 22495.20 ❌
- **TP 3RR**: 22512.87 ❌
- **TP 4RR**: 22530.54 ❌
- **TP 15RR**: 22724.92 ❌
- **PnL**: -17.67 points (-1.0R)
- **MFE**: 28.61 points
- **MAE**: 18.82 points

### Trade #345 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 02:45:00
- **FVG 5m**: 22453.42 - 22457.03
- **Entrée**: 22459.86 @ 2025-02-24 03:01:00
- **Stop Loss**: 22442.19
- **Risk**: 17.67 points
- **TP 1RR**: 22477.53 ✅
- **TP 2RR**: 22495.20 ❌
- **TP 3RR**: 22512.87 ❌
- **TP 4RR**: 22530.54 ❌
- **TP 15RR**: 22724.92 ❌
- **PnL**: -17.67 points (-1.0R)
- **MFE**: 28.61 points
- **MAE**: 18.82 points

### Trade #346 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-24 03:30:00
- **FVG 5m**: 22451.10 - 22453.42
- **Entrée**: 22450.33 @ 2025-02-24 05:44:00
- **Stop Loss**: 22464.64
- **Risk**: 14.32 points
- **TP 1RR**: 22436.01 ✅
- **TP 2RR**: 22421.69 ✅
- **TP 3RR**: 22407.37 ❌
- **TP 4RR**: 22393.05 ❌
- **TP 15RR**: 22235.53 ❌
- **PnL**: -14.32 points (-1.0R)
- **MFE**: 37.63 points
- **MAE**: 15.72 points

### Trade #347 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-24 08:00:00
- **FVG 5m**: 22392.59 - 22403.93
- **Entrée**: 22384.60 @ 2025-02-24 08:37:00
- **Stop Loss**: 22415.13
- **Risk**: 30.53 points
- **TP 1RR**: 22354.07 ✅
- **TP 2RR**: 22323.54 ✅
- **TP 3RR**: 22293.00 ✅
- **TP 4RR**: 22262.47 ✅
- **TP 15RR**: 21926.61 ✅
- **PnL**: 457.99 points (15.0R)
- **MFE**: 474.24 points
- **MAE**: 20.88 points

### Trade #348 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 08:30:00
- **FVG 5m**: 22214.75 - 22221.19
- **Entrée**: 22225.57 @ 2025-02-24 10:24:00
- **Stop Loss**: 22203.64
- **Risk**: 21.93 points
- **TP 1RR**: 22247.51 ✅
- **TP 2RR**: 22269.44 ✅
- **TP 3RR**: 22291.37 ✅
- **TP 4RR**: 22313.30 ✅
- **TP 15RR**: 22554.56 ❌
- **PnL**: -21.93 points (-1.0R)
- **MFE**: 105.67 points
- **MAE**: 32.48 points

### Trade #349 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 09:00:00
- **FVG 5m**: 22214.75 - 22221.19
- **Entrée**: 22225.57 @ 2025-02-24 10:24:00
- **Stop Loss**: 22203.64
- **Risk**: 21.93 points
- **TP 1RR**: 22247.51 ✅
- **TP 2RR**: 22269.44 ✅
- **TP 3RR**: 22291.37 ✅
- **TP 4RR**: 22313.30 ✅
- **TP 15RR**: 22554.56 ❌
- **PnL**: -21.93 points (-1.0R)
- **MFE**: 105.67 points
- **MAE**: 32.48 points

### Trade #350 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 15:00:00
- **FVG 5m**: 22089.23 - 22093.87
- **Entrée**: 22105.21 @ 2025-02-24 17:00:00
- **Stop Loss**: 22078.18
- **Risk**: 27.02 points
- **TP 1RR**: 22132.23 ❌
- **TP 2RR**: 22159.26 ❌
- **TP 3RR**: 22186.28 ❌
- **TP 4RR**: 22213.31 ❌
- **TP 15RR**: 22510.58 ❌
- **PnL**: -27.02 points (-1.0R)
- **MFE**: 9.28 points
- **MAE**: 48.20 points

### Trade #351 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 18:00:00
- **FVG 5m**: 22084.85 - 22096.19
- **Entrée**: 22112.17 @ 2025-02-24 18:27:00
- **Stop Loss**: 22073.81
- **Risk**: 38.36 points
- **TP 1RR**: 22150.53 ❌
- **TP 2RR**: 22188.89 ❌
- **TP 3RR**: 22227.26 ❌
- **TP 4RR**: 22265.62 ❌
- **TP 15RR**: 22687.61 ❌
- **PnL**: -38.36 points (-1.0R)
- **MFE**: 1.29 points
- **MAE**: 39.95 points

### Trade #352 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 18:00:00
- **FVG 5m**: 22084.85 - 22096.19
- **Entrée**: 22112.17 @ 2025-02-24 18:27:00
- **Stop Loss**: 22073.81
- **Risk**: 38.36 points
- **TP 1RR**: 22150.53 ❌
- **TP 2RR**: 22188.89 ❌
- **TP 3RR**: 22227.26 ❌
- **TP 4RR**: 22265.62 ❌
- **TP 15RR**: 22687.61 ❌
- **PnL**: -38.36 points (-1.0R)
- **MFE**: 1.29 points
- **MAE**: 39.95 points

### Trade #353 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 20:15:00
- **FVG 5m**: 22089.49 - 22094.38
- **Entrée**: 22098.25 @ 2025-02-24 22:17:00
- **Stop Loss**: 22078.44
- **Risk**: 19.81 points
- **TP 1RR**: 22118.06 ❌
- **TP 2RR**: 22137.87 ❌
- **TP 3RR**: 22157.67 ❌
- **TP 4RR**: 22177.48 ❌
- **TP 15RR**: 22395.37 ❌
- **PnL**: -19.81 points (-1.0R)
- **MFE**: 10.83 points
- **MAE**: 21.65 points

### Trade #354 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 01:00:00
- **FVG 5m**: 21990.00 - 22009.84
- **Entrée**: 22013.97 @ 2025-02-25 02:04:00
- **Stop Loss**: 21979.00
- **Risk**: 34.96 points
- **TP 1RR**: 22048.93 ✅
- **TP 2RR**: 22083.90 ❌
- **TP 3RR**: 22118.86 ❌
- **TP 4RR**: 22153.83 ❌
- **TP 15RR**: 22538.44 ❌
- **PnL**: -34.96 points (-1.0R)
- **MFE**: 53.87 points
- **MAE**: 38.15 points

### Trade #355 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 01:30:00
- **FVG 5m**: 21990.00 - 22009.84
- **Entrée**: 22013.97 @ 2025-02-25 02:04:00
- **Stop Loss**: 21979.00
- **Risk**: 34.96 points
- **TP 1RR**: 22048.93 ✅
- **TP 2RR**: 22083.90 ❌
- **TP 3RR**: 22118.86 ❌
- **TP 4RR**: 22153.83 ❌
- **TP 15RR**: 22538.44 ❌
- **PnL**: -34.96 points (-1.0R)
- **MFE**: 53.87 points
- **MAE**: 38.15 points

### Trade #356 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 05:00:00
- **FVG 5m**: 21982.78 - 21985.36
- **Entrée**: 21986.65 @ 2025-02-25 05:29:00
- **Stop Loss**: 21971.79
- **Risk**: 14.86 points
- **TP 1RR**: 22001.51 ✅
- **TP 2RR**: 22016.36 ✅
- **TP 3RR**: 22031.22 ✅
- **TP 4RR**: 22046.08 ✅
- **TP 15RR**: 22209.51 ❌
- **PnL**: -14.86 points (-1.0R)
- **MFE**: 129.39 points
- **MAE**: 15.98 points

### Trade #357 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 06:45:00
- **FVG 5m**: 22063.46 - 22082.01
- **Entrée**: 22084.59 @ 2025-02-25 06:58:00
- **Stop Loss**: 22052.42
- **Risk**: 32.17 points
- **TP 1RR**: 22116.76 ❌
- **TP 2RR**: 22148.92 ❌
- **TP 3RR**: 22181.09 ❌
- **TP 4RR**: 22213.26 ❌
- **TP 15RR**: 22567.09 ❌
- **PnL**: -32.17 points (-1.0R)
- **MFE**: 31.44 points
- **MAE**: 36.34 points

### Trade #358 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 10:45:00
- **FVG 5m**: 21788.70 - 21805.46
- **Entrée**: 21813.96 @ 2025-02-25 10:56:00
- **Stop Loss**: 21777.81
- **Risk**: 36.15 points
- **TP 1RR**: 21850.11 ✅
- **TP 2RR**: 21886.27 ❌
- **TP 3RR**: 21922.42 ❌
- **TP 4RR**: 21958.57 ❌
- **TP 15RR**: 22356.26 ❌
- **PnL**: -36.15 points (-1.0R)
- **MFE**: 45.36 points
- **MAE**: 41.75 points

### Trade #359 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 05:45:00
- **FVG 5m**: 21944.38 - 21951.08
- **Entrée**: 21938.45 @ 2025-02-26 06:49:00
- **Stop Loss**: 21962.06
- **Risk**: 23.60 points
- **TP 1RR**: 21914.85 ❌
- **TP 2RR**: 21891.24 ❌
- **TP 3RR**: 21867.64 ❌
- **TP 4RR**: 21844.03 ❌
- **TP 15RR**: 21584.38 ❌
- **PnL**: -23.60 points (-1.0R)
- **MFE**: 20.62 points
- **MAE**: 27.32 points

### Trade #360 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:00:00
- **FVG 5m**: 21915.51 - 21929.94
- **Entrée**: 21913.19 @ 2025-02-26 08:13:00
- **Stop Loss**: 21940.91
- **Risk**: 27.72 points
- **TP 1RR**: 21885.47 ✅
- **TP 2RR**: 21857.76 ✅
- **TP 3RR**: 21830.04 ❌
- **TP 4RR**: 21802.32 ❌
- **TP 15RR**: 21497.42 ❌
- **PnL**: -27.72 points (-1.0R)
- **MFE**: 68.04 points
- **MAE**: 28.61 points

### Trade #361 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:00:00
- **FVG 5m**: 21915.51 - 21929.94
- **Entrée**: 21913.19 @ 2025-02-26 08:13:00
- **Stop Loss**: 21940.91
- **Risk**: 27.72 points
- **TP 1RR**: 21885.47 ✅
- **TP 2RR**: 21857.76 ✅
- **TP 3RR**: 21830.04 ❌
- **TP 4RR**: 21802.32 ❌
- **TP 15RR**: 21497.42 ❌
- **PnL**: -27.72 points (-1.0R)
- **MFE**: 68.04 points
- **MAE**: 28.61 points

### Trade #362 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:00:00
- **FVG 5m**: 21915.51 - 21929.94
- **Entrée**: 21913.19 @ 2025-02-26 08:13:00
- **Stop Loss**: 21940.91
- **Risk**: 27.72 points
- **TP 1RR**: 21885.47 ✅
- **TP 2RR**: 21857.76 ✅
- **TP 3RR**: 21830.04 ❌
- **TP 4RR**: 21802.32 ❌
- **TP 15RR**: 21497.42 ❌
- **PnL**: -27.72 points (-1.0R)
- **MFE**: 68.04 points
- **MAE**: 28.61 points

### Trade #363 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 08:30:00
- **FVG 5m**: 21972.47 - 21975.82
- **Entrée**: 21989.74 @ 2025-02-26 09:12:00
- **Stop Loss**: 21961.49
- **Risk**: 28.25 points
- **TP 1RR**: 22018.00 ✅
- **TP 2RR**: 22046.25 ❌
- **TP 3RR**: 22074.51 ❌
- **TP 4RR**: 22102.76 ❌
- **TP 15RR**: 22413.56 ❌
- **PnL**: -28.25 points (-1.0R)
- **MFE**: 45.10 points
- **MAE**: 37.37 points

### Trade #364 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 08:30:00
- **FVG 5m**: 21972.47 - 21975.82
- **Entrée**: 21989.74 @ 2025-02-26 09:12:00
- **Stop Loss**: 21961.49
- **Risk**: 28.25 points
- **TP 1RR**: 22018.00 ✅
- **TP 2RR**: 22046.25 ❌
- **TP 3RR**: 22074.51 ❌
- **TP 4RR**: 22102.76 ❌
- **TP 15RR**: 22413.56 ❌
- **PnL**: -28.25 points (-1.0R)
- **MFE**: 45.10 points
- **MAE**: 37.37 points

### Trade #365 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 09:15:00
- **FVG 5m**: 22037.94 - 22041.80
- **Entrée**: 22034.07 @ 2025-02-26 10:57:00
- **Stop Loss**: 22052.83
- **Risk**: 18.75 points
- **TP 1RR**: 22015.32 ✅
- **TP 2RR**: 21996.57 ✅
- **TP 3RR**: 21977.81 ❌
- **TP 4RR**: 21959.06 ❌
- **TP 15RR**: 21752.78 ❌
- **PnL**: -18.75 points (-1.0R)
- **MFE**: 39.69 points
- **MAE**: 22.42 points

### Trade #366 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 09:15:00
- **FVG 5m**: 22037.94 - 22041.80
- **Entrée**: 22034.07 @ 2025-02-26 10:57:00
- **Stop Loss**: 22052.83
- **Risk**: 18.75 points
- **TP 1RR**: 22015.32 ✅
- **TP 2RR**: 21996.57 ✅
- **TP 3RR**: 21977.81 ❌
- **TP 4RR**: 21959.06 ❌
- **TP 15RR**: 21752.78 ❌
- **PnL**: -18.75 points (-1.0R)
- **MFE**: 39.69 points
- **MAE**: 22.42 points

### Trade #367 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 09:15:00
- **FVG 5m**: 22037.94 - 22041.80
- **Entrée**: 22034.07 @ 2025-02-26 10:57:00
- **Stop Loss**: 22052.83
- **Risk**: 18.75 points
- **TP 1RR**: 22015.32 ✅
- **TP 2RR**: 21996.57 ✅
- **TP 3RR**: 21977.81 ❌
- **TP 4RR**: 21959.06 ❌
- **TP 15RR**: 21752.78 ❌
- **PnL**: -18.75 points (-1.0R)
- **MFE**: 39.69 points
- **MAE**: 22.42 points

### Trade #368 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 13:15:00
- **FVG 5m**: 21789.22 - 21798.75
- **Entrée**: 21802.11 @ 2025-02-26 14:23:00
- **Stop Loss**: 21778.32
- **Risk**: 23.78 points
- **TP 1RR**: 21825.89 ✅
- **TP 2RR**: 21849.67 ✅
- **TP 3RR**: 21873.45 ✅
- **TP 4RR**: 21897.23 ❌
- **TP 15RR**: 22158.83 ❌
- **PnL**: -23.78 points (-1.0R)
- **MFE**: 183.77 points
- **MAE**: 95.11 points

### Trade #369 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 13:15:00
- **FVG 5m**: 21789.22 - 21798.75
- **Entrée**: 21802.11 @ 2025-02-26 14:23:00
- **Stop Loss**: 21778.32
- **Risk**: 23.78 points
- **TP 1RR**: 21825.89 ✅
- **TP 2RR**: 21849.67 ✅
- **TP 3RR**: 21873.45 ✅
- **TP 4RR**: 21897.23 ❌
- **TP 15RR**: 22158.83 ❌
- **PnL**: -23.78 points (-1.0R)
- **MFE**: 183.77 points
- **MAE**: 95.11 points

### Trade #370 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 14:30:00
- **FVG 5m**: 21822.72 - 21841.02
- **Entrée**: 21841.54 @ 2025-02-26 14:43:00
- **Stop Loss**: 21811.81
- **Risk**: 29.73 points
- **TP 1RR**: 21871.27 ✅
- **TP 2RR**: 21900.99 ❌
- **TP 3RR**: 21930.72 ❌
- **TP 4RR**: 21960.45 ❌
- **TP 15RR**: 22287.44 ❌
- **PnL**: -29.73 points (-1.0R)
- **MFE**: 144.34 points
- **MAE**: 134.54 points

### Trade #371 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-27 07:45:00
- **FVG 5m**: 21968.61 - 21980.72
- **Entrée**: 21968.35 @ 2025-02-27 08:39:00
- **Stop Loss**: 21991.71
- **Risk**: 23.36 points
- **TP 1RR**: 21944.99 ✅
- **TP 2RR**: 21921.62 ✅
- **TP 3RR**: 21898.26 ✅
- **TP 4RR**: 21874.90 ✅
- **TP 15RR**: 21617.92 ✅
- **PnL**: 350.43 points (15.0R)
- **MFE**: 402.33 points
- **MAE**: 0.26 points

### Trade #372 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-27 08:30:00
- **FVG 5m**: 21889.48 - 21960.87
- **Entrée**: 21879.17 @ 2025-02-27 08:42:00
- **Stop Loss**: 21971.85
- **Risk**: 92.68 points
- **TP 1RR**: 21786.49 ✅
- **TP 2RR**: 21693.80 ✅
- **TP 3RR**: 21601.12 ✅
- **TP 4RR**: 21508.43 ✅
- **TP 15RR**: 20488.90 ✅
- **PnL**: 1390.27 points (15.0R)
- **MFE**: 1405.98 points
- **MAE**: 10.31 points

### Trade #373 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21651.32
- **Risk**: 61.86 points
- **TP 1RR**: 21775.05 ✅
- **TP 2RR**: 21836.91 ❌
- **TP 3RR**: 21898.78 ❌
- **TP 4RR**: 21960.64 ❌
- **TP 15RR**: 22641.14 ❌
- **PnL**: -61.86 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 68.56 points

### Trade #374 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21651.32
- **Risk**: 61.86 points
- **TP 1RR**: 21775.05 ✅
- **TP 2RR**: 21836.91 ❌
- **TP 3RR**: 21898.78 ❌
- **TP 4RR**: 21960.64 ❌
- **TP 15RR**: 22641.14 ❌
- **PnL**: -61.86 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 68.56 points

### Trade #375 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21651.32
- **Risk**: 61.86 points
- **TP 1RR**: 21775.05 ✅
- **TP 2RR**: 21836.91 ❌
- **TP 3RR**: 21898.78 ❌
- **TP 4RR**: 21960.64 ❌
- **TP 15RR**: 22641.14 ❌
- **PnL**: -61.86 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 68.56 points

### Trade #376 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21651.32
- **Risk**: 61.86 points
- **TP 1RR**: 21775.05 ✅
- **TP 2RR**: 21836.91 ❌
- **TP 3RR**: 21898.78 ❌
- **TP 4RR**: 21960.64 ❌
- **TP 15RR**: 22641.14 ❌
- **PnL**: -61.86 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 68.56 points

### Trade #377 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21651.32
- **Risk**: 61.86 points
- **TP 1RR**: 21775.05 ✅
- **TP 2RR**: 21836.91 ❌
- **TP 3RR**: 21898.78 ❌
- **TP 4RR**: 21960.64 ❌
- **TP 15RR**: 22641.14 ❌
- **PnL**: -61.86 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 68.56 points

### Trade #378 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21651.32
- **Risk**: 61.86 points
- **TP 1RR**: 21775.05 ✅
- **TP 2RR**: 21836.91 ❌
- **TP 3RR**: 21898.78 ❌
- **TP 4RR**: 21960.64 ❌
- **TP 15RR**: 22641.14 ❌
- **PnL**: -61.86 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 68.56 points

### Trade #379 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:15:00
- **FVG 5m**: 21717.05 - 21767.05
- **Entrée**: 21774.01 @ 2025-02-27 10:14:00
- **Stop Loss**: 21706.19
- **Risk**: 67.82 points
- **TP 1RR**: 21841.83 ❌
- **TP 2RR**: 21909.65 ❌
- **TP 3RR**: 21977.47 ❌
- **TP 4RR**: 22045.29 ❌
- **TP 15RR**: 22791.30 ❌
- **PnL**: -67.82 points (-1.0R)
- **MFE**: 40.98 points
- **MAE**: 68.30 points

### Trade #380 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 19:30:00
- **FVG 5m**: 21266.52 - 21269.35
- **Entrée**: 21270.64 @ 2025-02-27 20:28:00
- **Stop Loss**: 21255.88
- **Risk**: 14.76 points
- **TP 1RR**: 21285.40 ❌
- **TP 2RR**: 21300.16 ❌
- **TP 3RR**: 21314.91 ❌
- **TP 4RR**: 21329.67 ❌
- **TP 15RR**: 21492.00 ❌
- **PnL**: -14.76 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 20.88 points

### Trade #381 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 21:45:00
- **FVG 5m**: 21212.65 - 21232.24
- **Entrée**: 21238.94 @ 2025-02-27 22:24:00
- **Stop Loss**: 21202.04
- **Risk**: 36.90 points
- **TP 1RR**: 21275.84 ✅
- **TP 2RR**: 21312.73 ❌
- **TP 3RR**: 21349.63 ❌
- **TP 4RR**: 21386.52 ❌
- **TP 15RR**: 21792.38 ❌
- **PnL**: -36.90 points (-1.0R)
- **MFE**: 46.14 points
- **MAE**: 37.89 points

### Trade #382 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 06:00:00
- **FVG 5m**: 21248.99 - 21260.59
- **Entrée**: 21241.00 @ 2025-02-28 06:31:00
- **Stop Loss**: 21271.22
- **Risk**: 30.22 points
- **TP 1RR**: 21210.78 ✅
- **TP 2RR**: 21180.56 ❌
- **TP 3RR**: 21150.35 ❌
- **TP 4RR**: 21120.13 ❌
- **TP 15RR**: 20787.72 ❌
- **PnL**: -30.22 points (-1.0R)
- **MFE**: 42.79 points
- **MAE**: 34.80 points

### Trade #383 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 06:00:00
- **FVG 5m**: 21248.99 - 21260.59
- **Entrée**: 21241.00 @ 2025-02-28 06:31:00
- **Stop Loss**: 21271.22
- **Risk**: 30.22 points
- **TP 1RR**: 21210.78 ✅
- **TP 2RR**: 21180.56 ❌
- **TP 3RR**: 21150.35 ❌
- **TP 4RR**: 21120.13 ❌
- **TP 15RR**: 20787.72 ❌
- **PnL**: -30.22 points (-1.0R)
- **MFE**: 42.79 points
- **MAE**: 34.80 points

### Trade #384 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 08:30:00
- **FVG 5m**: 21339.20 - 21347.45
- **Entrée**: 21354.15 @ 2025-02-28 09:24:00
- **Stop Loss**: 21328.53
- **Risk**: 25.62 points
- **TP 1RR**: 21379.77 ✅
- **TP 2RR**: 21405.39 ✅
- **TP 3RR**: 21431.01 ❌
- **TP 4RR**: 21456.62 ❌
- **TP 15RR**: 21738.43 ❌
- **PnL**: -25.62 points (-1.0R)
- **MFE**: 67.27 points
- **MAE**: 27.32 points

### Trade #385 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 08:30:00
- **FVG 5m**: 21339.20 - 21347.45
- **Entrée**: 21354.15 @ 2025-02-28 09:24:00
- **Stop Loss**: 21328.53
- **Risk**: 25.62 points
- **TP 1RR**: 21379.77 ✅
- **TP 2RR**: 21405.39 ✅
- **TP 3RR**: 21431.01 ❌
- **TP 4RR**: 21456.62 ❌
- **TP 15RR**: 21738.43 ❌
- **PnL**: -25.62 points (-1.0R)
- **MFE**: 67.27 points
- **MAE**: 27.32 points

### Trade #386 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 09:15:00
- **FVG 5m**: 21363.94 - 21370.39
- **Entrée**: 21373.22 @ 2025-02-28 09:26:00
- **Stop Loss**: 21353.26
- **Risk**: 19.96 points
- **TP 1RR**: 21393.18 ✅
- **TP 2RR**: 21413.14 ✅
- **TP 3RR**: 21433.11 ❌
- **TP 4RR**: 21453.07 ❌
- **TP 15RR**: 21672.63 ❌
- **PnL**: -19.96 points (-1.0R)
- **MFE**: 48.20 points
- **MAE**: 41.50 points

### Trade #387 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 09:15:00
- **FVG 5m**: 21363.94 - 21370.39
- **Entrée**: 21373.22 @ 2025-02-28 09:26:00
- **Stop Loss**: 21353.26
- **Risk**: 19.96 points
- **TP 1RR**: 21393.18 ✅
- **TP 2RR**: 21413.14 ✅
- **TP 3RR**: 21433.11 ❌
- **TP 4RR**: 21453.07 ❌
- **TP 15RR**: 21672.63 ❌
- **PnL**: -19.96 points (-1.0R)
- **MFE**: 48.20 points
- **MAE**: 41.50 points

### Trade #388 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 09:15:00
- **FVG 5m**: 21363.94 - 21370.39
- **Entrée**: 21373.22 @ 2025-02-28 09:26:00
- **Stop Loss**: 21353.26
- **Risk**: 19.96 points
- **TP 1RR**: 21393.18 ✅
- **TP 2RR**: 21413.14 ✅
- **TP 3RR**: 21433.11 ❌
- **TP 4RR**: 21453.07 ❌
- **TP 15RR**: 21672.63 ❌
- **PnL**: -19.96 points (-1.0R)
- **MFE**: 48.20 points
- **MAE**: 41.50 points

### Trade #389 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 10:15:00
- **FVG 5m**: 21269.87 - 21308.53
- **Entrée**: 21265.23 @ 2025-02-28 11:43:00
- **Stop Loss**: 21319.18
- **Risk**: 53.95 points
- **TP 1RR**: 21211.27 ✅
- **TP 2RR**: 21157.32 ✅
- **TP 3RR**: 21103.36 ❌
- **TP 4RR**: 21049.41 ❌
- **TP 15RR**: 20455.91 ❌
- **PnL**: -53.95 points (-1.0R)
- **MFE**: 146.65 points
- **MAE**: 62.63 points

### Trade #390 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 10:15:00
- **FVG 5m**: 21269.87 - 21308.53
- **Entrée**: 21265.23 @ 2025-02-28 11:43:00
- **Stop Loss**: 21319.18
- **Risk**: 53.95 points
- **TP 1RR**: 21211.27 ✅
- **TP 2RR**: 21157.32 ✅
- **TP 3RR**: 21103.36 ❌
- **TP 4RR**: 21049.41 ❌
- **TP 15RR**: 20455.91 ❌
- **PnL**: -53.95 points (-1.0R)
- **MFE**: 146.65 points
- **MAE**: 62.63 points

### Trade #391 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 10:15:00
- **FVG 5m**: 21269.87 - 21308.53
- **Entrée**: 21265.23 @ 2025-02-28 11:43:00
- **Stop Loss**: 21319.18
- **Risk**: 53.95 points
- **TP 1RR**: 21211.27 ✅
- **TP 2RR**: 21157.32 ✅
- **TP 3RR**: 21103.36 ❌
- **TP 4RR**: 21049.41 ❌
- **TP 15RR**: 20455.91 ❌
- **PnL**: -53.95 points (-1.0R)
- **MFE**: 146.65 points
- **MAE**: 62.63 points

### Trade #392 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 14:15:00
- **FVG 5m**: 21412.40 - 21419.87
- **Entrée**: 21426.06 @ 2025-02-28 14:49:00
- **Stop Loss**: 21401.69
- **Risk**: 24.37 points
- **TP 1RR**: 21450.43 ✅
- **TP 2RR**: 21474.79 ✅
- **TP 3RR**: 21499.16 ✅
- **TP 4RR**: 21523.53 ✅
- **TP 15RR**: 21791.56 ❌
- **PnL**: -24.37 points (-1.0R)
- **MFE**: 348.98 points
- **MAE**: 32.48 points

### Trade #393 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 14:45:00
- **FVG 5m**: 21525.55 - 21530.45
- **Entrée**: 21535.08 @ 2025-02-28 15:04:00
- **Stop Loss**: 21514.79
- **Risk**: 20.30 points
- **TP 1RR**: 21555.38 ❌
- **TP 2RR**: 21575.68 ❌
- **TP 3RR**: 21595.98 ❌
- **TP 4RR**: 21616.28 ❌
- **TP 15RR**: 21839.57 ❌
- **PnL**: -20.30 points (-1.0R)
- **MFE**: 0.77 points
- **MAE**: 20.62 points

### Trade #394 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 14:45:00
- **FVG 5m**: 21525.55 - 21530.45
- **Entrée**: 21535.08 @ 2025-02-28 15:04:00
- **Stop Loss**: 21514.79
- **Risk**: 20.30 points
- **TP 1RR**: 21555.38 ❌
- **TP 2RR**: 21575.68 ❌
- **TP 3RR**: 21595.98 ❌
- **TP 4RR**: 21616.28 ❌
- **TP 15RR**: 21839.57 ❌
- **PnL**: -20.30 points (-1.0R)
- **MFE**: 0.77 points
- **MAE**: 20.62 points

### Trade #395 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-02 23:00:00
- **FVG 5m**: 21632.25 - 21635.35
- **Entrée**: 21640.50 @ 2025-03-02 23:37:00
- **Stop Loss**: 21621.44
- **Risk**: 19.06 points
- **TP 1RR**: 21659.57 ❌
- **TP 2RR**: 21678.63 ❌
- **TP 3RR**: 21697.69 ❌
- **TP 4RR**: 21716.76 ❌
- **TP 15RR**: 21926.46 ❌
- **PnL**: -19.06 points (-1.0R)
- **MFE**: 11.34 points
- **MAE**: 19.85 points

### Trade #396 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 01:15:00
- **FVG 5m**: 21600.04 - 21613.70
- **Entrée**: 21585.09 @ 2025-03-03 02:19:00
- **Stop Loss**: 21624.50
- **Risk**: 39.42 points
- **TP 1RR**: 21545.67 ✅
- **TP 2RR**: 21506.25 ❌
- **TP 3RR**: 21466.84 ❌
- **TP 4RR**: 21427.42 ❌
- **TP 15RR**: 20993.84 ❌
- **PnL**: -39.42 points (-1.0R)
- **MFE**: 50.26 points
- **MAE**: 40.98 points

### Trade #397 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 08:30:00
- **FVG 5m**: 21564.73 - 21576.07
- **Entrée**: 21555.19 @ 2025-03-03 08:54:00
- **Stop Loss**: 21586.85
- **Risk**: 31.67 points
- **TP 1RR**: 21523.52 ✅
- **TP 2RR**: 21491.86 ✅
- **TP 3RR**: 21460.19 ✅
- **TP 4RR**: 21428.53 ✅
- **TP 15RR**: 21080.21 ❌
- **PnL**: -31.67 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 33.25 points

### Trade #398 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 08:30:00
- **FVG 5m**: 21564.73 - 21576.07
- **Entrée**: 21555.19 @ 2025-03-03 08:54:00
- **Stop Loss**: 21586.85
- **Risk**: 31.67 points
- **TP 1RR**: 21523.52 ✅
- **TP 2RR**: 21491.86 ✅
- **TP 3RR**: 21460.19 ✅
- **TP 4RR**: 21428.53 ✅
- **TP 15RR**: 21080.21 ❌
- **PnL**: -31.67 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 33.25 points

### Trade #399 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 08:30:00
- **FVG 5m**: 21564.73 - 21576.07
- **Entrée**: 21555.19 @ 2025-03-03 08:54:00
- **Stop Loss**: 21586.85
- **Risk**: 31.67 points
- **TP 1RR**: 21523.52 ✅
- **TP 2RR**: 21491.86 ✅
- **TP 3RR**: 21460.19 ✅
- **TP 4RR**: 21428.53 ✅
- **TP 15RR**: 21080.21 ❌
- **PnL**: -31.67 points (-1.0R)
- **MFE**: 152.33 points
- **MAE**: 33.25 points

### Trade #400 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 08:45:00
- **FVG 5m**: 21486.63 - 21526.58
- **Entrée**: 21530.19 @ 2025-03-03 09:21:00
- **Stop Loss**: 21475.89
- **Risk**: 54.30 points
- **TP 1RR**: 21584.49 ✅
- **TP 2RR**: 21638.79 ✅
- **TP 3RR**: 21693.09 ❌
- **TP 4RR**: 21747.39 ❌
- **TP 15RR**: 22344.71 ❌
- **PnL**: -54.30 points (-1.0R)
- **MFE**: 109.02 points
- **MAE**: 61.86 points

### Trade #401 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 09:15:00
- **FVG 5m**: 21511.63 - 21541.27
- **Entrée**: 21548.23 @ 2025-03-03 10:49:00
- **Stop Loss**: 21500.87
- **Risk**: 47.36 points
- **TP 1RR**: 21595.58 ✅
- **TP 2RR**: 21642.94 ❌
- **TP 3RR**: 21690.30 ❌
- **TP 4RR**: 21737.65 ❌
- **TP 15RR**: 22258.56 ❌
- **PnL**: -47.36 points (-1.0R)
- **MFE**: 65.47 points
- **MAE**: 68.82 points

### Trade #402 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 09:15:00
- **FVG 5m**: 21511.63 - 21541.27
- **Entrée**: 21548.23 @ 2025-03-03 10:49:00
- **Stop Loss**: 21500.87
- **Risk**: 47.36 points
- **TP 1RR**: 21595.58 ✅
- **TP 2RR**: 21642.94 ❌
- **TP 3RR**: 21690.30 ❌
- **TP 4RR**: 21737.65 ❌
- **TP 15RR**: 22258.56 ❌
- **PnL**: -47.36 points (-1.0R)
- **MFE**: 65.47 points
- **MAE**: 68.82 points

### Trade #403 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 12:00:00
- **FVG 5m**: 21352.86 - 21366.01
- **Entrée**: 21325.80 @ 2025-03-03 12:28:00
- **Stop Loss**: 21376.69
- **Risk**: 50.89 points
- **TP 1RR**: 21274.91 ❌
- **TP 2RR**: 21224.02 ❌
- **TP 3RR**: 21173.13 ❌
- **TP 4RR**: 21122.24 ❌
- **TP 15RR**: 20562.44 ❌
- **PnL**: -50.89 points (-1.0R)
- **MFE**: 32.99 points
- **MAE**: 87.37 points

### Trade #404 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 13:30:00
- **FVG 5m**: 21063.93 - 21097.96
- **Entrée**: 21099.50 @ 2025-03-03 14:58:00
- **Stop Loss**: 21053.40
- **Risk**: 46.10 points
- **TP 1RR**: 21145.60 ✅
- **TP 2RR**: 21191.70 ✅
- **TP 3RR**: 21237.80 ❌
- **TP 4RR**: 21283.90 ❌
- **TP 15RR**: 21791.01 ❌
- **PnL**: -46.10 points (-1.0R)
- **MFE**: 130.16 points
- **MAE**: 50.52 points

### Trade #405 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 14:00:00
- **FVG 5m**: 21063.93 - 21097.96
- **Entrée**: 21099.50 @ 2025-03-03 14:58:00
- **Stop Loss**: 21053.40
- **Risk**: 46.10 points
- **TP 1RR**: 21145.60 ✅
- **TP 2RR**: 21191.70 ✅
- **TP 3RR**: 21237.80 ❌
- **TP 4RR**: 21283.90 ❌
- **TP 15RR**: 21791.01 ❌
- **PnL**: -46.10 points (-1.0R)
- **MFE**: 130.16 points
- **MAE**: 50.52 points

### Trade #406 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 15:00:00
- **FVG 5m**: 21139.19 - 21161.62
- **Entrée**: 21162.13 @ 2025-03-03 18:19:00
- **Stop Loss**: 21128.62
- **Risk**: 33.51 points
- **TP 1RR**: 21195.64 ❌
- **TP 2RR**: 21229.15 ❌
- **TP 3RR**: 21262.66 ❌
- **TP 4RR**: 21296.17 ❌
- **TP 15RR**: 21664.76 ❌
- **PnL**: -33.51 points (-1.0R)
- **MFE**: 16.50 points
- **MAE**: 54.13 points

### Trade #407 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 23:00:00
- **FVG 5m**: 21177.08 - 21189.71
- **Entrée**: 21171.67 @ 2025-03-04 00:09:00
- **Stop Loss**: 21200.31
- **Risk**: 28.64 points
- **TP 1RR**: 21143.03 ❌
- **TP 2RR**: 21114.40 ❌
- **TP 3RR**: 21085.76 ❌
- **TP 4RR**: 21057.12 ❌
- **TP 15RR**: 20742.12 ❌
- **PnL**: -28.64 points (-1.0R)
- **MFE**: 12.37 points
- **MAE**: 35.31 points

### Trade #408 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-04 02:00:00
- **FVG 5m**: 21167.29 - 21176.05
- **Entrée**: 21187.13 @ 2025-03-04 02:31:00
- **Stop Loss**: 21156.70
- **Risk**: 30.43 points
- **TP 1RR**: 21217.56 ❌
- **TP 2RR**: 21247.99 ❌
- **TP 3RR**: 21278.42 ❌
- **TP 4RR**: 21308.85 ❌
- **TP 15RR**: 21643.58 ❌
- **PnL**: -30.43 points (-1.0R)
- **MFE**: 13.14 points
- **MAE**: 37.11 points

### Trade #409 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-04 07:30:00
- **FVG 5m**: 20977.33 - 21000.79
- **Entrée**: 21004.14 @ 2025-03-04 08:02:00
- **Stop Loss**: 20966.84
- **Risk**: 37.29 points
- **TP 1RR**: 21041.43 ❌
- **TP 2RR**: 21078.72 ❌
- **TP 3RR**: 21116.02 ❌
- **TP 4RR**: 21153.31 ❌
- **TP 15RR**: 21563.54 ❌
- **PnL**: -37.29 points (-1.0R)
- **MFE**: 26.03 points
- **MAE**: 38.15 points

### Trade #410 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-04 12:00:00
- **FVG 5m**: 21049.50 - 21062.90
- **Entrée**: 21066.77 @ 2025-03-04 12:39:00
- **Stop Loss**: 21038.97
- **Risk**: 27.79 points
- **TP 1RR**: 21094.56 ✅
- **TP 2RR**: 21122.36 ✅
- **TP 3RR**: 21150.15 ✅
- **TP 4RR**: 21177.94 ✅
- **TP 15RR**: 21483.67 ❌
- **PnL**: -27.79 points (-1.0R)
- **MFE**: 307.74 points
- **MAE**: 68.82 points

### Trade #411 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-04 12:15:00
- **FVG 5m**: 21229.92 - 21308.79
- **Entrée**: 21196.15 @ 2025-03-04 14:33:00
- **Stop Loss**: 21319.44
- **Risk**: 123.29 points
- **TP 1RR**: 21072.87 ✅
- **TP 2RR**: 20949.58 ✅
- **TP 3RR**: 20826.29 ❌
- **TP 4RR**: 20703.00 ❌
- **TP 15RR**: 19346.84 ❌
- **PnL**: -123.29 points (-1.0R)
- **MFE**: 355.17 points
- **MAE**: 131.71 points

### Trade #412 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-04 13:00:00
- **FVG 5m**: 21229.92 - 21308.79
- **Entrée**: 21196.15 @ 2025-03-04 14:33:00
- **Stop Loss**: 21319.44
- **Risk**: 123.29 points
- **TP 1RR**: 21072.87 ✅
- **TP 2RR**: 20949.58 ✅
- **TP 3RR**: 20826.29 ❌
- **TP 4RR**: 20703.00 ❌
- **TP 15RR**: 19346.84 ❌
- **PnL**: -123.29 points (-1.0R)
- **MFE**: 355.17 points
- **MAE**: 131.71 points

### Trade #413 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-04 13:15:00
- **FVG 5m**: 21229.92 - 21308.79
- **Entrée**: 21196.15 @ 2025-03-04 14:33:00
- **Stop Loss**: 21319.44
- **Risk**: 123.29 points
- **TP 1RR**: 21072.87 ✅
- **TP 2RR**: 20949.58 ✅
- **TP 3RR**: 20826.29 ❌
- **TP 4RR**: 20703.00 ❌
- **TP 15RR**: 19346.84 ❌
- **PnL**: -123.29 points (-1.0R)
- **MFE**: 355.17 points
- **MAE**: 131.71 points

### Trade #414 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-04 14:45:00
- **FVG 5m**: 21183.78 - 21194.87
- **Entrée**: 21174.50 @ 2025-03-04 15:32:00
- **Stop Loss**: 21205.46
- **Risk**: 30.96 points
- **TP 1RR**: 21143.55 ✅
- **TP 2RR**: 21112.59 ❌
- **TP 3RR**: 21081.63 ❌
- **TP 4RR**: 21050.67 ❌
- **TP 15RR**: 20710.12 ❌
- **PnL**: -30.96 points (-1.0R)
- **MFE**: 57.22 points
- **MAE**: 31.44 points

### Trade #415 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-05 02:30:00
- **FVG 5m**: 21211.36 - 21237.91
- **Entrée**: 21209.04 @ 2025-03-05 04:12:00
- **Stop Loss**: 21248.53
- **Risk**: 39.49 points
- **TP 1RR**: 21169.56 ✅
- **TP 2RR**: 21130.07 ✅
- **TP 3RR**: 21090.58 ✅
- **TP 4RR**: 21051.10 ✅
- **TP 15RR**: 20616.75 ❌
- **PnL**: -39.49 points (-1.0R)
- **MFE**: 368.06 points
- **MAE**: 45.36 points

### Trade #416 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-05 04:00:00
- **FVG 5m**: 21211.36 - 21237.91
- **Entrée**: 21209.04 @ 2025-03-05 04:12:00
- **Stop Loss**: 21248.53
- **Risk**: 39.49 points
- **TP 1RR**: 21169.56 ✅
- **TP 2RR**: 21130.07 ✅
- **TP 3RR**: 21090.58 ✅
- **TP 4RR**: 21051.10 ✅
- **TP 15RR**: 20616.75 ❌
- **PnL**: -39.49 points (-1.0R)
- **MFE**: 368.06 points
- **MAE**: 45.36 points

### Trade #417 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 06:30:00
- **FVG 5m**: 21052.85 - 21070.12
- **Entrée**: 21071.92 @ 2025-03-05 08:14:00
- **Stop Loss**: 21042.32
- **Risk**: 29.60 points
- **TP 1RR**: 21101.52 ❌
- **TP 2RR**: 21131.12 ❌
- **TP 3RR**: 21160.72 ❌
- **TP 4RR**: 21190.32 ❌
- **TP 15RR**: 21515.91 ❌
- **PnL**: -29.60 points (-1.0R)
- **MFE**: 27.58 points
- **MAE**: 42.01 points

### Trade #418 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 06:30:00
- **FVG 5m**: 21052.85 - 21070.12
- **Entrée**: 21071.92 @ 2025-03-05 08:14:00
- **Stop Loss**: 21042.32
- **Risk**: 29.60 points
- **TP 1RR**: 21101.52 ❌
- **TP 2RR**: 21131.12 ❌
- **TP 3RR**: 21160.72 ❌
- **TP 4RR**: 21190.32 ❌
- **TP 15RR**: 21515.91 ❌
- **PnL**: -29.60 points (-1.0R)
- **MFE**: 27.58 points
- **MAE**: 42.01 points

### Trade #419 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 08:30:00
- **FVG 5m**: 20994.34 - 21051.05
- **Entrée**: 21053.37 @ 2025-03-05 09:02:00
- **Stop Loss**: 20983.85
- **Risk**: 69.52 points
- **TP 1RR**: 21122.89 ✅
- **TP 2RR**: 21192.41 ❌
- **TP 3RR**: 21261.93 ❌
- **TP 4RR**: 21331.45 ❌
- **TP 15RR**: 22096.17 ❌
- **PnL**: -69.52 points (-1.0R)
- **MFE**: 78.35 points
- **MAE**: 125.26 points

### Trade #420 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 11:15:00
- **FVG 5m**: 21132.75 - 21172.96
- **Entrée**: 21174.25 @ 2025-03-05 11:52:00
- **Stop Loss**: 21122.18
- **Risk**: 52.06 points
- **TP 1RR**: 21226.31 ❌
- **TP 2RR**: 21278.37 ❌
- **TP 3RR**: 21330.43 ❌
- **TP 4RR**: 21382.50 ❌
- **TP 15RR**: 21955.19 ❌
- **PnL**: -52.06 points (-1.0R)
- **MFE**: 48.71 points
- **MAE**: 62.89 points

### Trade #421 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 11:15:00
- **FVG 5m**: 21132.75 - 21172.96
- **Entrée**: 21174.25 @ 2025-03-05 11:52:00
- **Stop Loss**: 21122.18
- **Risk**: 52.06 points
- **TP 1RR**: 21226.31 ❌
- **TP 2RR**: 21278.37 ❌
- **TP 3RR**: 21330.43 ❌
- **TP 4RR**: 21382.50 ❌
- **TP 15RR**: 21955.19 ❌
- **PnL**: -52.06 points (-1.0R)
- **MFE**: 48.71 points
- **MAE**: 62.89 points

### Trade #422 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-05 15:00:00
- **FVG 5m**: 21246.67 - 21256.21
- **Entrée**: 21235.33 @ 2025-03-05 17:31:00
- **Stop Loss**: 21266.84
- **Risk**: 31.51 points
- **TP 1RR**: 21203.83 ❌
- **TP 2RR**: 21172.32 ❌
- **TP 3RR**: 21140.82 ❌
- **TP 4RR**: 21109.31 ❌
- **TP 15RR**: 20762.75 ❌
- **PnL**: -31.51 points (-1.0R)
- **MFE**: 8.76 points
- **MAE**: 35.57 points

### Trade #423 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-06 01:00:00
- **FVG 5m**: 21266.26 - 21271.42
- **Entrée**: 21261.36 @ 2025-03-06 01:15:00
- **Stop Loss**: 21282.05
- **Risk**: 20.69 points
- **TP 1RR**: 21240.68 ✅
- **TP 2RR**: 21219.99 ✅
- **TP 3RR**: 21199.30 ✅
- **TP 4RR**: 21178.61 ✅
- **TP 15RR**: 20951.05 ✅
- **PnL**: 310.31 points (15.0R)
- **MFE**: 323.72 points
- **MAE**: 13.40 points

### Trade #424 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-06 08:00:00
- **FVG 5m**: 20951.30 - 20986.35
- **Entrée**: 20989.45 @ 2025-03-06 09:04:00
- **Stop Loss**: 20940.82
- **Risk**: 48.62 points
- **TP 1RR**: 21038.07 ✅
- **TP 2RR**: 21086.69 ✅
- **TP 3RR**: 21135.31 ✅
- **TP 4RR**: 21183.93 ❌
- **TP 15RR**: 21718.77 ❌
- **PnL**: -48.62 points (-1.0R)
- **MFE**: 159.03 points
- **MAE**: 67.79 points

### Trade #425 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-06 12:45:00
- **FVG 5m**: 20669.85 - 20678.09
- **Entrée**: 20680.41 @ 2025-03-06 13:41:00
- **Stop Loss**: 20659.51
- **Risk**: 20.90 points
- **TP 1RR**: 20701.32 ✅
- **TP 2RR**: 20722.22 ✅
- **TP 3RR**: 20743.12 ✅
- **TP 4RR**: 20764.02 ✅
- **TP 15RR**: 20993.95 ❌
- **PnL**: -20.90 points (-1.0R)
- **MFE**: 152.84 points
- **MAE**: 34.02 points

### Trade #426 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-06 19:00:00
- **FVG 5m**: 20816.76 - 20822.43
- **Entrée**: 20823.72 @ 2025-03-06 20:14:00
- **Stop Loss**: 20806.35
- **Risk**: 17.37 points
- **TP 1RR**: 20841.09 ✅
- **TP 2RR**: 20858.45 ❌
- **TP 3RR**: 20875.82 ❌
- **TP 4RR**: 20893.19 ❌
- **TP 15RR**: 21084.23 ❌
- **PnL**: -17.37 points (-1.0R)
- **MFE**: 19.33 points
- **MAE**: 17.78 points

### Trade #427 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 01:00:00
- **FVG 5m**: 20772.17 - 20780.93
- **Entrée**: 20781.71 @ 2025-03-07 01:46:00
- **Stop Loss**: 20761.78
- **Risk**: 19.92 points
- **TP 1RR**: 20801.63 ✅
- **TP 2RR**: 20821.55 ✅
- **TP 3RR**: 20841.47 ✅
- **TP 4RR**: 20861.40 ❌
- **TP 15RR**: 21080.54 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 72.68 points
- **MAE**: 26.81 points

### Trade #428 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 01:00:00
- **FVG 5m**: 20772.17 - 20780.93
- **Entrée**: 20781.71 @ 2025-03-07 01:46:00
- **Stop Loss**: 20761.78
- **Risk**: 19.92 points
- **TP 1RR**: 20801.63 ✅
- **TP 2RR**: 20821.55 ✅
- **TP 3RR**: 20841.47 ✅
- **TP 4RR**: 20861.40 ❌
- **TP 15RR**: 21080.54 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 72.68 points
- **MAE**: 26.81 points

### Trade #429 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 03:15:00
- **FVG 5m**: 20810.32 - 20821.91
- **Entrée**: 20808.77 @ 2025-03-07 04:04:00
- **Stop Loss**: 20832.32
- **Risk**: 23.56 points
- **TP 1RR**: 20785.21 ✅
- **TP 2RR**: 20761.66 ✅
- **TP 3RR**: 20738.10 ✅
- **TP 4RR**: 20714.55 ✅
- **TP 15RR**: 20455.43 ❌
- **PnL**: -23.56 points (-1.0R)
- **MFE**: 126.04 points
- **MAE**: 67.27 points

### Trade #430 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 06:45:00
- **FVG 5m**: 20744.33 - 20768.82
- **Entrée**: 20798.97 @ 2025-03-07 07:39:00
- **Stop Loss**: 20733.96
- **Risk**: 65.01 points
- **TP 1RR**: 20863.99 ❌
- **TP 2RR**: 20929.00 ❌
- **TP 3RR**: 20994.01 ❌
- **TP 4RR**: 21059.03 ❌
- **TP 15RR**: 21774.18 ❌
- **PnL**: -65.01 points (-1.0R)
- **MFE**: 6.19 points
- **MAE**: 65.21 points

### Trade #431 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20740.98 - 20759.80
- **Entrée**: 20740.47 @ 2025-03-07 09:13:00
- **Stop Loss**: 20770.18
- **Risk**: 29.71 points
- **TP 1RR**: 20710.76 ✅
- **TP 2RR**: 20681.05 ✅
- **TP 3RR**: 20651.34 ✅
- **TP 4RR**: 20621.63 ✅
- **TP 15RR**: 20294.81 ❌
- **PnL**: -29.71 points (-1.0R)
- **MFE**: 362.90 points
- **MAE**: 31.96 points

### Trade #432 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20740.98 - 20759.80
- **Entrée**: 20740.47 @ 2025-03-07 09:13:00
- **Stop Loss**: 20770.18
- **Risk**: 29.71 points
- **TP 1RR**: 20710.76 ✅
- **TP 2RR**: 20681.05 ✅
- **TP 3RR**: 20651.34 ✅
- **TP 4RR**: 20621.63 ✅
- **TP 15RR**: 20294.81 ❌
- **PnL**: -29.71 points (-1.0R)
- **MFE**: 362.90 points
- **MAE**: 31.96 points

### Trade #433 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20740.98 - 20759.80
- **Entrée**: 20740.47 @ 2025-03-07 09:13:00
- **Stop Loss**: 20770.18
- **Risk**: 29.71 points
- **TP 1RR**: 20710.76 ✅
- **TP 2RR**: 20681.05 ✅
- **TP 3RR**: 20651.34 ✅
- **TP 4RR**: 20621.63 ✅
- **TP 15RR**: 20294.81 ❌
- **PnL**: -29.71 points (-1.0R)
- **MFE**: 362.90 points
- **MAE**: 31.96 points

### Trade #434 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20740.98 - 20759.80
- **Entrée**: 20740.47 @ 2025-03-07 09:13:00
- **Stop Loss**: 20770.18
- **Risk**: 29.71 points
- **TP 1RR**: 20710.76 ✅
- **TP 2RR**: 20681.05 ✅
- **TP 3RR**: 20651.34 ✅
- **TP 4RR**: 20621.63 ✅
- **TP 15RR**: 20294.81 ❌
- **PnL**: -29.71 points (-1.0R)
- **MFE**: 362.90 points
- **MAE**: 31.96 points

### Trade #435 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 09:45:00
- **FVG 5m**: 20431.18 - 20440.20
- **Entrée**: 20444.32 @ 2025-03-07 10:59:00
- **Stop Loss**: 20420.96
- **Risk**: 23.36 points
- **TP 1RR**: 20467.68 ✅
- **TP 2RR**: 20491.04 ✅
- **TP 3RR**: 20514.40 ❌
- **TP 4RR**: 20537.76 ❌
- **TP 15RR**: 20794.73 ❌
- **PnL**: -23.36 points (-1.0R)
- **MFE**: 67.53 points
- **MAE**: 25.26 points

### Trade #436 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 13:15:00
- **FVG 5m**: 20831.71 - 20841.24
- **Entrée**: 20862.38 @ 2025-03-07 14:08:00
- **Stop Loss**: 20821.29
- **Risk**: 41.09 points
- **TP 1RR**: 20903.47 ❌
- **TP 2RR**: 20944.55 ❌
- **TP 3RR**: 20985.64 ❌
- **TP 4RR**: 21026.73 ❌
- **TP 15RR**: 21478.69 ❌
- **PnL**: -41.09 points (-1.0R)
- **MFE**: 19.33 points
- **MAE**: 64.95 points

### Trade #437 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 14:45:00
- **FVG 5m**: 20840.21 - 20846.14
- **Entrée**: 20839.18 @ 2025-03-07 15:09:00
- **Stop Loss**: 20856.56
- **Risk**: 17.38 points
- **TP 1RR**: 20821.80 ✅
- **TP 2RR**: 20804.42 ✅
- **TP 3RR**: 20787.04 ✅
- **TP 4RR**: 20769.65 ✅
- **TP 15RR**: 20578.45 ✅
- **PnL**: 260.73 points (15.0R)
- **MFE**: 289.70 points
- **MAE**: 8.76 points

### Trade #438 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 14:45:00
- **FVG 5m**: 20840.21 - 20846.14
- **Entrée**: 20839.18 @ 2025-03-07 15:09:00
- **Stop Loss**: 20856.56
- **Risk**: 17.38 points
- **TP 1RR**: 20821.80 ✅
- **TP 2RR**: 20804.42 ✅
- **TP 3RR**: 20787.04 ✅
- **TP 4RR**: 20769.65 ✅
- **TP 15RR**: 20578.45 ✅
- **PnL**: 260.73 points (15.0R)
- **MFE**: 289.70 points
- **MAE**: 8.76 points

### Trade #439 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-09 20:30:00
- **FVG 5m**: 20743.56 - 20750.52
- **Entrée**: 20752.32 @ 2025-03-09 20:57:00
- **Stop Loss**: 20733.19
- **Risk**: 19.13 points
- **TP 1RR**: 20771.46 ✅
- **TP 2RR**: 20790.59 ❌
- **TP 3RR**: 20809.73 ❌
- **TP 4RR**: 20828.86 ❌
- **TP 15RR**: 21039.35 ❌
- **PnL**: -19.13 points (-1.0R)
- **MFE**: 28.35 points
- **MAE**: 20.62 points

### Trade #440 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-10 01:00:00
- **FVG 5m**: 20739.18 - 20742.27
- **Entrée**: 20744.59 @ 2025-03-10 02:01:00
- **Stop Loss**: 20728.81
- **Risk**: 15.78 points
- **TP 1RR**: 20760.37 ✅
- **TP 2RR**: 20776.16 ❌
- **TP 3RR**: 20791.94 ❌
- **TP 4RR**: 20807.72 ❌
- **TP 15RR**: 20981.32 ❌
- **PnL**: -15.78 points (-1.0R)
- **MFE**: 20.10 points
- **MAE**: 21.13 points

### Trade #441 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-10 08:45:00
- **FVG 5m**: 20244.57 - 20264.42
- **Entrée**: 20270.09 @ 2025-03-10 10:31:00
- **Stop Loss**: 20234.45
- **Risk**: 35.64 points
- **TP 1RR**: 20305.73 ✅
- **TP 2RR**: 20341.37 ❌
- **TP 3RR**: 20377.01 ❌
- **TP 4RR**: 20412.64 ❌
- **TP 15RR**: 20804.67 ❌
- **PnL**: -35.64 points (-1.0R)
- **MFE**: 43.04 points
- **MAE**: 46.91 points

### Trade #442 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-10 18:30:00
- **FVG 5m**: 19876.26 - 19890.95
- **Entrée**: 19905.64 @ 2025-03-10 18:43:00
- **Stop Loss**: 19866.32
- **Risk**: 39.32 points
- **TP 1RR**: 19944.96 ❌
- **TP 2RR**: 19984.28 ❌
- **TP 3RR**: 20023.60 ❌
- **TP 4RR**: 20062.93 ❌
- **TP 15RR**: 20495.45 ❌
- **PnL**: -39.32 points (-1.0R)
- **MFE**: 22.94 points
- **MAE**: 54.13 points

### Trade #443 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 02:45:00
- **FVG 5m**: 20052.30 - 20071.37
- **Entrée**: 20072.92 @ 2025-03-11 02:56:00
- **Stop Loss**: 20042.27
- **Risk**: 30.65 points
- **TP 1RR**: 20103.56 ✅
- **TP 2RR**: 20134.21 ✅
- **TP 3RR**: 20164.85 ✅
- **TP 4RR**: 20195.50 ❌
- **TP 15RR**: 20532.60 ❌
- **PnL**: -30.65 points (-1.0R)
- **MFE**: 118.56 points
- **MAE**: 30.67 points

### Trade #444 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 03:00:00
- **FVG 5m**: 20112.87 - 20131.94
- **Entrée**: 20136.06 @ 2025-03-11 03:11:00
- **Stop Loss**: 20102.81
- **Risk**: 33.25 points
- **TP 1RR**: 20169.32 ✅
- **TP 2RR**: 20202.57 ❌
- **TP 3RR**: 20235.82 ❌
- **TP 4RR**: 20269.08 ❌
- **TP 15RR**: 20634.86 ❌
- **PnL**: -33.25 points (-1.0R)
- **MFE**: 52.06 points
- **MAE**: 35.57 points

### Trade #445 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 03:30:00
- **FVG 5m**: 20144.05 - 20146.12
- **Entrée**: 20138.13 @ 2025-03-11 05:09:00
- **Stop Loss**: 20156.19
- **Risk**: 18.06 points
- **TP 1RR**: 20120.06 ❌
- **TP 2RR**: 20102.00 ❌
- **TP 3RR**: 20083.94 ❌
- **TP 4RR**: 20065.87 ❌
- **TP 15RR**: 19867.18 ❌
- **PnL**: -18.06 points (-1.0R)
- **MFE**: 7.99 points
- **MAE**: 20.62 points

### Trade #446 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 06:00:00
- **FVG 5m**: 20137.87 - 20154.88
- **Entrée**: 20130.39 @ 2025-03-11 07:09:00
- **Stop Loss**: 20164.96
- **Risk**: 34.56 points
- **TP 1RR**: 20095.83 ✅
- **TP 2RR**: 20061.27 ✅
- **TP 3RR**: 20026.70 ✅
- **TP 4RR**: 19992.14 ✅
- **TP 15RR**: 19611.95 ❌
- **PnL**: -34.56 points (-1.0R)
- **MFE**: 144.34 points
- **MAE**: 63.40 points

### Trade #447 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 07:00:00
- **FVG 5m**: 20115.19 - 20129.62
- **Entrée**: 20109.26 @ 2025-03-11 07:11:00
- **Stop Loss**: 20139.68
- **Risk**: 30.43 points
- **TP 1RR**: 20078.83 ✅
- **TP 2RR**: 20048.41 ✅
- **TP 3RR**: 20017.98 ✅
- **TP 4RR**: 19987.55 ✅
- **TP 15RR**: 19652.86 ❌
- **PnL**: -30.43 points (-1.0R)
- **MFE**: 123.20 points
- **MAE**: 35.83 points

### Trade #448 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 08:30:00
- **FVG 5m**: 19975.49 - 20037.35
- **Entrée**: 20047.40 @ 2025-03-11 10:07:00
- **Stop Loss**: 19965.50
- **Risk**: 81.90 points
- **TP 1RR**: 20129.30 ✅
- **TP 2RR**: 20211.20 ❌
- **TP 3RR**: 20293.09 ❌
- **TP 4RR**: 20374.99 ❌
- **TP 15RR**: 21275.87 ❌
- **PnL**: -81.90 points (-1.0R)
- **MFE**: 102.07 points
- **MAE**: 88.41 points

### Trade #449 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 08:45:00
- **FVG 5m**: 19995.08 - 20000.23
- **Entrée**: 19989.15 @ 2025-03-11 09:24:00
- **Stop Loss**: 20010.23
- **Risk**: 21.08 points
- **TP 1RR**: 19968.07 ✅
- **TP 2RR**: 19946.98 ✅
- **TP 3RR**: 19925.90 ✅
- **TP 4RR**: 19904.82 ✅
- **TP 15RR**: 19672.91 ❌
- **PnL**: -21.08 points (-1.0R)
- **MFE**: 128.10 points
- **MAE**: 30.16 points

### Trade #450 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 08:45:00
- **FVG 5m**: 19995.08 - 20000.23
- **Entrée**: 19989.15 @ 2025-03-11 09:24:00
- **Stop Loss**: 20010.23
- **Risk**: 21.08 points
- **TP 1RR**: 19968.07 ✅
- **TP 2RR**: 19946.98 ✅
- **TP 3RR**: 19925.90 ✅
- **TP 4RR**: 19904.82 ✅
- **TP 15RR**: 19672.91 ❌
- **PnL**: -21.08 points (-1.0R)
- **MFE**: 128.10 points
- **MAE**: 30.16 points

### Trade #451 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 12:30:00
- **FVG 5m**: 19849.20 - 19881.93
- **Entrée**: 19894.56 @ 2025-03-11 12:44:00
- **Stop Loss**: 19839.27
- **Risk**: 55.29 points
- **TP 1RR**: 19949.85 ✅
- **TP 2RR**: 20005.13 ✅
- **TP 3RR**: 20060.42 ✅
- **TP 4RR**: 20115.71 ✅
- **TP 15RR**: 20723.87 ❌
- **PnL**: -55.29 points (-1.0R)
- **MFE**: 506.98 points
- **MAE**: 55.93 points

### Trade #452 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 14:00:00
- **FVG 5m**: 20186.07 - 20211.07
- **Entrée**: 20184.52 @ 2025-03-11 14:14:00
- **Stop Loss**: 20221.17
- **Risk**: 36.65 points
- **TP 1RR**: 20147.87 ✅
- **TP 2RR**: 20111.21 ✅
- **TP 3RR**: 20074.56 ✅
- **TP 4RR**: 20037.91 ✅
- **TP 15RR**: 19634.73 ❌
- **PnL**: -36.65 points (-1.0R)
- **MFE**: 212.89 points
- **MAE**: 217.02 points

### Trade #453 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 14:30:00
- **FVG 5m**: 20088.64 - 20109.26
- **Entrée**: 20088.12 @ 2025-03-11 14:51:00
- **Stop Loss**: 20119.31
- **Risk**: 31.19 points
- **TP 1RR**: 20056.93 ✅
- **TP 2RR**: 20025.74 ✅
- **TP 3RR**: 19994.56 ✅
- **TP 4RR**: 19963.37 ❌
- **TP 15RR**: 19620.28 ❌
- **PnL**: -31.19 points (-1.0R)
- **MFE**: 116.50 points
- **MAE**: 32.22 points

### Trade #454 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-12 02:30:00
- **FVG 5m**: 20026.01 - 20047.66
- **Entrée**: 20048.43 @ 2025-03-12 02:43:00
- **Stop Loss**: 20015.99
- **Risk**: 32.44 points
- **TP 1RR**: 20080.87 ✅
- **TP 2RR**: 20113.30 ✅
- **TP 3RR**: 20145.74 ✅
- **TP 4RR**: 20178.18 ✅
- **TP 15RR**: 20534.98 ❌
- **PnL**: -32.44 points (-1.0R)
- **MFE**: 353.11 points
- **MAE**: 35.31 points

### Trade #455 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-12 03:00:00
- **FVG 5m**: 20147.40 - 20155.39
- **Entrée**: 20143.02 @ 2025-03-12 05:07:00
- **Stop Loss**: 20165.47
- **Risk**: 22.45 points
- **TP 1RR**: 20120.57 ❌
- **TP 2RR**: 20098.12 ❌
- **TP 3RR**: 20075.67 ❌
- **TP 4RR**: 20053.23 ❌
- **TP 15RR**: 19806.28 ❌
- **PnL**: -22.45 points (-1.0R)
- **MFE**: 14.18 points
- **MAE**: 23.71 points

### Trade #456 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-12 03:00:00
- **FVG 5m**: 20147.40 - 20155.39
- **Entrée**: 20143.02 @ 2025-03-12 05:07:00
- **Stop Loss**: 20165.47
- **Risk**: 22.45 points
- **TP 1RR**: 20120.57 ❌
- **TP 2RR**: 20098.12 ❌
- **TP 3RR**: 20075.67 ❌
- **TP 4RR**: 20053.23 ❌
- **TP 15RR**: 19806.28 ❌
- **PnL**: -22.45 points (-1.0R)
- **MFE**: 14.18 points
- **MAE**: 23.71 points

### Trade #457 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-12 07:30:00
- **FVG 5m**: 20310.04 - 20312.36
- **Entrée**: 20309.52 @ 2025-03-12 08:11:00
- **Stop Loss**: 20322.51
- **Risk**: 12.99 points
- **TP 1RR**: 20296.53 ✅
- **TP 2RR**: 20283.54 ✅
- **TP 3RR**: 20270.55 ❌
- **TP 4RR**: 20257.56 ❌
- **TP 15RR**: 20114.65 ❌
- **PnL**: -12.99 points (-1.0R)
- **MFE**: 35.31 points
- **MAE**: 17.01 points

### Trade #458 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-12 09:45:00
- **FVG 5m**: 20092.76 - 20105.65
- **Entrée**: 20078.84 @ 2025-03-12 09:59:00
- **Stop Loss**: 20115.70
- **Risk**: 36.86 points
- **TP 1RR**: 20041.99 ✅
- **TP 2RR**: 20005.13 ✅
- **TP 3RR**: 19968.27 ❌
- **TP 4RR**: 19931.41 ❌
- **TP 15RR**: 19525.98 ❌
- **PnL**: -36.86 points (-1.0R)
- **MFE**: 82.99 points
- **MAE**: 46.65 points

### Trade #459 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-12 22:30:00
- **FVG 5m**: 20134.26 - 20140.19
- **Entrée**: 20143.28 @ 2025-03-12 23:07:00
- **Stop Loss**: 20124.19
- **Risk**: 19.09 points
- **TP 1RR**: 20162.37 ❌
- **TP 2RR**: 20181.46 ❌
- **TP 3RR**: 20200.54 ❌
- **TP 4RR**: 20219.63 ❌
- **TP 15RR**: 20429.60 ❌
- **PnL**: -19.09 points (-1.0R)
- **MFE**: 6.70 points
- **MAE**: 26.81 points

### Trade #460 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 04:30:00
- **FVG 5m**: 20181.94 - 20184.26
- **Entrée**: 20187.61 @ 2025-03-13 04:44:00
- **Stop Loss**: 20171.85
- **Risk**: 15.76 points
- **TP 1RR**: 20203.37 ✅
- **TP 2RR**: 20219.13 ✅
- **TP 3RR**: 20234.90 ✅
- **TP 4RR**: 20250.66 ❌
- **TP 15RR**: 20424.03 ❌
- **PnL**: -15.76 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 21.65 points

### Trade #461 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-13 07:00:00
- **FVG 5m**: 20018.79 - 20061.06
- **Entrée**: 20005.13 @ 2025-03-13 08:54:00
- **Stop Loss**: 20071.09
- **Risk**: 65.96 points
- **TP 1RR**: 19939.17 ✅
- **TP 2RR**: 19873.21 ❌
- **TP 3RR**: 19807.25 ❌
- **TP 4RR**: 19741.29 ❌
- **TP 15RR**: 19015.72 ❌
- **PnL**: -65.96 points (-1.0R)
- **MFE**: 82.22 points
- **MAE**: 81.19 points

### Trade #462 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20042.01
- **Risk**: 38.38 points
- **TP 1RR**: 20118.77 ✅
- **TP 2RR**: 20157.15 ✅
- **TP 3RR**: 20195.52 ❌
- **TP 4RR**: 20233.90 ❌
- **TP 15RR**: 20656.06 ❌
- **PnL**: -38.38 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 39.43 points

### Trade #463 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20042.01
- **Risk**: 38.38 points
- **TP 1RR**: 20118.77 ✅
- **TP 2RR**: 20157.15 ✅
- **TP 3RR**: 20195.52 ❌
- **TP 4RR**: 20233.90 ❌
- **TP 15RR**: 20656.06 ❌
- **PnL**: -38.38 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 39.43 points

### Trade #464 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20042.01
- **Risk**: 38.38 points
- **TP 1RR**: 20118.77 ✅
- **TP 2RR**: 20157.15 ✅
- **TP 3RR**: 20195.52 ❌
- **TP 4RR**: 20233.90 ❌
- **TP 15RR**: 20656.06 ❌
- **PnL**: -38.38 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 39.43 points

### Trade #465 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20042.01
- **Risk**: 38.38 points
- **TP 1RR**: 20118.77 ✅
- **TP 2RR**: 20157.15 ✅
- **TP 3RR**: 20195.52 ❌
- **TP 4RR**: 20233.90 ❌
- **TP 15RR**: 20656.06 ❌
- **PnL**: -38.38 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 39.43 points

### Trade #466 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20042.01
- **Risk**: 38.38 points
- **TP 1RR**: 20118.77 ✅
- **TP 2RR**: 20157.15 ✅
- **TP 3RR**: 20195.52 ❌
- **TP 4RR**: 20233.90 ❌
- **TP 15RR**: 20656.06 ❌
- **PnL**: -38.38 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 39.43 points

### Trade #467 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 20042.01
- **Risk**: 38.38 points
- **TP 1RR**: 20118.77 ✅
- **TP 2RR**: 20157.15 ✅
- **TP 3RR**: 20195.52 ❌
- **TP 4RR**: 20233.90 ❌
- **TP 15RR**: 20656.06 ❌
- **PnL**: -38.38 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 39.43 points

### Trade #468 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 10:30:00
- **FVG 5m**: 19916.47 - 19933.99
- **Entrée**: 19941.21 @ 2025-03-13 11:31:00
- **Stop Loss**: 19906.51
- **Risk**: 34.70 points
- **TP 1RR**: 19975.91 ✅
- **TP 2RR**: 20010.61 ❌
- **TP 3RR**: 20045.32 ❌
- **TP 4RR**: 20080.02 ❌
- **TP 15RR**: 20461.73 ❌
- **PnL**: -34.70 points (-1.0R)
- **MFE**: 50.00 points
- **MAE**: 41.75 points

### Trade #469 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 12:15:00
- **FVG 5m**: 19820.07 - 19835.02
- **Entrée**: 19845.33 @ 2025-03-13 13:02:00
- **Stop Loss**: 19810.16
- **Risk**: 35.17 points
- **TP 1RR**: 19880.50 ✅
- **TP 2RR**: 19915.67 ✅
- **TP 3RR**: 19950.84 ✅
- **TP 4RR**: 19986.01 ✅
- **TP 15RR**: 20372.86 ❌
- **PnL**: -35.17 points (-1.0R)
- **MFE**: 151.55 points
- **MAE**: 44.59 points

### Trade #470 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 05:45:00
- **FVG 5m**: 20083.74 - 20094.57
- **Entrée**: 20081.94 @ 2025-03-14 08:14:00
- **Stop Loss**: 20104.61
- **Risk**: 22.68 points
- **TP 1RR**: 20059.26 ✅
- **TP 2RR**: 20036.58 ❌
- **TP 3RR**: 20013.91 ❌
- **TP 4RR**: 19991.23 ❌
- **TP 15RR**: 19741.79 ❌
- **PnL**: -22.68 points (-1.0R)
- **MFE**: 28.87 points
- **MAE**: 33.76 points

### Trade #471 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 05:45:00
- **FVG 5m**: 20083.74 - 20094.57
- **Entrée**: 20081.94 @ 2025-03-14 08:14:00
- **Stop Loss**: 20104.61
- **Risk**: 22.68 points
- **TP 1RR**: 20059.26 ✅
- **TP 2RR**: 20036.58 ❌
- **TP 3RR**: 20013.91 ❌
- **TP 4RR**: 19991.23 ❌
- **TP 15RR**: 19741.79 ❌
- **PnL**: -22.68 points (-1.0R)
- **MFE**: 28.87 points
- **MAE**: 33.76 points

### Trade #472 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 08:45:00
- **FVG 5m**: 20150.50 - 20181.94
- **Entrée**: 20094.05 @ 2025-03-14 09:00:00
- **Stop Loss**: 20192.03
- **Risk**: 97.98 points
- **TP 1RR**: 19996.07 ❌
- **TP 2RR**: 19898.09 ❌
- **TP 3RR**: 19800.11 ❌
- **TP 4RR**: 19702.13 ❌
- **TP 15RR**: 18624.34 ❌
- **PnL**: -97.98 points (-1.0R)
- **MFE**: 46.65 points
- **MAE**: 103.10 points

### Trade #473 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 10:00:00
- **FVG 5m**: 20261.84 - 20272.67
- **Entrée**: 20259.52 @ 2025-03-14 11:08:00
- **Stop Loss**: 20282.80
- **Risk**: 23.28 points
- **TP 1RR**: 20236.24 ✅
- **TP 2RR**: 20212.96 ✅
- **TP 3RR**: 20189.68 ❌
- **TP 4RR**: 20166.40 ❌
- **TP 15RR**: 19910.30 ❌
- **PnL**: -23.28 points (-1.0R)
- **MFE**: 47.94 points
- **MAE**: 23.71 points

### Trade #474 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 11:45:00
- **FVG 5m**: 20251.53 - 20257.46
- **Entrée**: 20239.68 @ 2025-03-14 13:13:00
- **Stop Loss**: 20267.59
- **Risk**: 27.91 points
- **TP 1RR**: 20211.76 ❌
- **TP 2RR**: 20183.85 ❌
- **TP 3RR**: 20155.94 ❌
- **TP 4RR**: 20128.02 ❌
- **TP 15RR**: 19820.98 ❌
- **PnL**: -27.91 points (-1.0R)
- **MFE**: 20.10 points
- **MAE**: 32.22 points

### Trade #475 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 14:45:00
- **FVG 5m**: 20285.81 - 20313.91
- **Entrée**: 20280.14 @ 2025-03-14 15:03:00
- **Stop Loss**: 20324.06
- **Risk**: 43.92 points
- **TP 1RR**: 20236.22 ✅
- **TP 2RR**: 20192.30 ✅
- **TP 3RR**: 20148.38 ❌
- **TP 4RR**: 20104.46 ❌
- **TP 15RR**: 19621.32 ❌
- **PnL**: -43.92 points (-1.0R)
- **MFE**: 124.23 points
- **MAE**: 47.42 points

### Trade #476 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 14:45:00
- **FVG 5m**: 20285.81 - 20313.91
- **Entrée**: 20280.14 @ 2025-03-14 15:03:00
- **Stop Loss**: 20324.06
- **Risk**: 43.92 points
- **TP 1RR**: 20236.22 ✅
- **TP 2RR**: 20192.30 ✅
- **TP 3RR**: 20148.38 ❌
- **TP 4RR**: 20104.46 ❌
- **TP 15RR**: 19621.32 ❌
- **PnL**: -43.92 points (-1.0R)
- **MFE**: 124.23 points
- **MAE**: 47.42 points

### Trade #477 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-16 17:00:00
- **FVG 5m**: 20176.01 - 20179.36
- **Entrée**: 20182.46 @ 2025-03-16 18:16:00
- **Stop Loss**: 20165.93
- **Risk**: 16.53 points
- **TP 1RR**: 20198.99 ✅
- **TP 2RR**: 20215.52 ✅
- **TP 3RR**: 20232.05 ✅
- **TP 4RR**: 20248.58 ❌
- **TP 15RR**: 20430.43 ❌
- **PnL**: -16.53 points (-1.0R)
- **MFE**: 53.87 points
- **MAE**: 22.17 points

### Trade #478 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-16 17:00:00
- **FVG 5m**: 20176.01 - 20179.36
- **Entrée**: 20182.46 @ 2025-03-16 18:16:00
- **Stop Loss**: 20165.93
- **Risk**: 16.53 points
- **TP 1RR**: 20198.99 ✅
- **TP 2RR**: 20215.52 ✅
- **TP 3RR**: 20232.05 ✅
- **TP 4RR**: 20248.58 ❌
- **TP 15RR**: 20430.43 ❌
- **PnL**: -16.53 points (-1.0R)
- **MFE**: 53.87 points
- **MAE**: 22.17 points

### Trade #479 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-17 02:45:00
- **FVG 5m**: 20237.87 - 20243.28
- **Entrée**: 20246.89 @ 2025-03-17 05:08:00
- **Stop Loss**: 20227.75
- **Risk**: 19.14 points
- **TP 1RR**: 20266.03 ✅
- **TP 2RR**: 20285.17 ✅
- **TP 3RR**: 20304.31 ✅
- **TP 4RR**: 20323.45 ✅
- **TP 15RR**: 20533.99 ✅
- **PnL**: 287.10 points (15.0R)
- **MFE**: 292.79 points
- **MAE**: 10.31 points

### Trade #480 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-17 08:00:00
- **FVG 5m**: 20328.08 - 20340.19
- **Entrée**: 20327.31 @ 2025-03-17 08:19:00
- **Stop Loss**: 20350.36
- **Risk**: 23.06 points
- **TP 1RR**: 20304.25 ✅
- **TP 2RR**: 20281.19 ❌
- **TP 3RR**: 20258.14 ❌
- **TP 4RR**: 20235.08 ❌
- **TP 15RR**: 19981.45 ❌
- **PnL**: -23.06 points (-1.0R)
- **MFE**: 34.54 points
- **MAE**: 34.28 points

### Trade #481 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-17 09:15:00
- **FVG 5m**: 20345.35 - 20382.72
- **Entrée**: 20326.53 @ 2025-03-17 09:29:00
- **Stop Loss**: 20392.91
- **Risk**: 66.38 points
- **TP 1RR**: 20260.16 ✅
- **TP 2RR**: 20193.78 ❌
- **TP 3RR**: 20127.40 ❌
- **TP 4RR**: 20061.02 ❌
- **TP 15RR**: 19330.85 ❌
- **PnL**: -66.38 points (-1.0R)
- **MFE**: 89.95 points
- **MAE**: 68.56 points

### Trade #482 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-17 14:45:00
- **FVG 5m**: 20448.45 - 20474.74
- **Entrée**: 20446.13 @ 2025-03-17 14:59:00
- **Stop Loss**: 20484.97
- **Risk**: 38.85 points
- **TP 1RR**: 20407.28 ✅
- **TP 2RR**: 20368.43 ✅
- **TP 3RR**: 20329.59 ✅
- **TP 4RR**: 20290.74 ✅
- **TP 15RR**: 19863.43 ❌
- **PnL**: -38.85 points (-1.0R)
- **MFE**: 447.73 points
- **MAE**: 42.94 points

### Trade #483 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-17 20:00:00
- **FVG 5m**: 20366.48 - 20369.84
- **Entrée**: 20370.09 @ 2025-03-17 21:04:00
- **Stop Loss**: 20356.30
- **Risk**: 13.79 points
- **TP 1RR**: 20383.88 ❌
- **TP 2RR**: 20397.68 ❌
- **TP 3RR**: 20411.47 ❌
- **TP 4RR**: 20425.26 ❌
- **TP 15RR**: 20576.97 ❌
- **PnL**: -13.79 points (-1.0R)
- **MFE**: 10.31 points
- **MAE**: 20.88 points

### Trade #484 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-18 08:30:00
- **FVG 5m**: 20144.52 - 20164.41
- **Entrée**: 20108.56 @ 2025-03-18 08:44:00
- **Stop Loss**: 20174.50
- **Risk**: 65.93 points
- **TP 1RR**: 20042.63 ✅
- **TP 2RR**: 19976.70 ❌
- **TP 3RR**: 19910.76 ❌
- **TP 4RR**: 19844.83 ❌
- **TP 15RR**: 19119.57 ❌
- **PnL**: -65.93 points (-1.0R)
- **MFE**: 110.17 points
- **MAE**: 72.68 points

### Trade #485 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-18 10:00:00
- **FVG 5m**: 20061.38 - 20070.82
- **Entrée**: 20077.70 @ 2025-03-18 11:02:00
- **Stop Loss**: 20051.35
- **Risk**: 26.35 points
- **TP 1RR**: 20104.06 ✅
- **TP 2RR**: 20130.41 ✅
- **TP 3RR**: 20156.76 ❌
- **TP 4RR**: 20183.11 ❌
- **TP 15RR**: 20472.99 ❌
- **PnL**: -26.35 points (-1.0R)
- **MFE**: 72.94 points
- **MAE**: 29.33 points

### Trade #486 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-18 13:45:00
- **FVG 5m**: 20113.66 - 20117.49
- **Entrée**: 20112.90 @ 2025-03-18 15:16:00
- **Stop Loss**: 20127.55
- **Risk**: 14.65 points
- **TP 1RR**: 20098.25 ✅
- **TP 2RR**: 20083.60 ✅
- **TP 3RR**: 20068.95 ✅
- **TP 4RR**: 20054.30 ❌
- **TP 15RR**: 19893.16 ❌
- **PnL**: -14.65 points (-1.0R)
- **MFE**: 51.26 points
- **MAE**: 22.44 points

### Trade #487 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-18 19:45:00
- **FVG 5m**: 20166.20 - 20169.00
- **Entrée**: 20163.90 @ 2025-03-18 21:49:00
- **Stop Loss**: 20179.09
- **Risk**: 15.19 points
- **TP 1RR**: 20148.72 ✅
- **TP 2RR**: 20133.53 ✅
- **TP 3RR**: 20118.35 ✅
- **TP 4RR**: 20103.16 ✅
- **TP 15RR**: 19936.13 ❌
- **PnL**: -15.19 points (-1.0R)
- **MFE**: 108.64 points
- **MAE**: 15.30 points

### Trade #488 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 02:15:00
- **FVG 5m**: 20075.15 - 20082.30
- **Entrée**: 20096.83 @ 2025-03-19 03:05:00
- **Stop Loss**: 20065.12
- **Risk**: 31.71 points
- **TP 1RR**: 20128.55 ✅
- **TP 2RR**: 20160.26 ✅
- **TP 3RR**: 20191.98 ✅
- **TP 4RR**: 20223.69 ✅
- **TP 15RR**: 20572.55 ❌
- **PnL**: -31.71 points (-1.0R)
- **MFE**: 451.14 points
- **MAE**: 33.41 points

### Trade #489 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 04:45:00
- **FVG 5m**: 20169.26 - 20173.34
- **Entrée**: 20176.91 @ 2025-03-19 06:39:00
- **Stop Loss**: 20159.17
- **Risk**: 17.74 points
- **TP 1RR**: 20194.65 ❌
- **TP 2RR**: 20212.38 ❌
- **TP 3RR**: 20230.12 ❌
- **TP 4RR**: 20247.85 ❌
- **TP 15RR**: 20442.94 ❌
- **PnL**: -17.74 points (-1.0R)
- **MFE**: 10.71 points
- **MAE**: 31.88 points

### Trade #490 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 08:30:00
- **FVG 5m**: 20233.02 - 20236.84
- **Entrée**: 20232.25 @ 2025-03-19 09:42:00
- **Stop Loss**: 20246.96
- **Risk**: 14.71 points
- **TP 1RR**: 20217.54 ✅
- **TP 2RR**: 20202.83 ✅
- **TP 3RR**: 20188.12 ✅
- **TP 4RR**: 20173.42 ❌
- **TP 15RR**: 20011.62 ❌
- **PnL**: -14.71 points (-1.0R)
- **MFE**: 46.41 points
- **MAE**: 18.11 points

### Trade #491 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 08:30:00
- **FVG 5m**: 20233.02 - 20236.84
- **Entrée**: 20232.25 @ 2025-03-19 09:42:00
- **Stop Loss**: 20246.96
- **Risk**: 14.71 points
- **TP 1RR**: 20217.54 ✅
- **TP 2RR**: 20202.83 ✅
- **TP 3RR**: 20188.12 ✅
- **TP 4RR**: 20173.42 ❌
- **TP 15RR**: 20011.62 ❌
- **PnL**: -14.71 points (-1.0R)
- **MFE**: 46.41 points
- **MAE**: 18.11 points

### Trade #492 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 09:00:00
- **FVG 5m**: 20220.01 - 20255.71
- **Entrée**: 20258.52 @ 2025-03-19 10:09:00
- **Stop Loss**: 20209.90
- **Risk**: 48.62 points
- **TP 1RR**: 20307.14 ✅
- **TP 2RR**: 20355.76 ❌
- **TP 3RR**: 20404.38 ❌
- **TP 4RR**: 20452.99 ❌
- **TP 15RR**: 20987.80 ❌
- **PnL**: -48.62 points (-1.0R)
- **MFE**: 79.82 points
- **MAE**: 50.75 points

### Trade #493 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 11:00:00
- **FVG 5m**: 20299.07 - 20307.23
- **Entrée**: 20295.24 @ 2025-03-19 11:13:00
- **Stop Loss**: 20317.38
- **Risk**: 22.14 points
- **TP 1RR**: 20273.10 ✅
- **TP 2RR**: 20250.96 ✅
- **TP 3RR**: 20228.82 ✅
- **TP 4RR**: 20206.68 ✅
- **TP 15RR**: 19963.14 ❌
- **PnL**: -22.14 points (-1.0R)
- **MFE**: 128.79 points
- **MAE**: 33.92 points

### Trade #494 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 13:30:00
- **FVG 5m**: 20408.98 - 20423.01
- **Entrée**: 20423.78 @ 2025-03-19 13:57:00
- **Stop Loss**: 20398.78
- **Risk**: 25.00 points
- **TP 1RR**: 20448.77 ✅
- **TP 2RR**: 20473.77 ✅
- **TP 3RR**: 20498.76 ✅
- **TP 4RR**: 20523.76 ✅
- **TP 15RR**: 20798.72 ❌
- **PnL**: -25.00 points (-1.0R)
- **MFE**: 124.20 points
- **MAE**: 30.60 points

### Trade #495 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 13:30:00
- **FVG 5m**: 20408.98 - 20423.01
- **Entrée**: 20423.78 @ 2025-03-19 13:57:00
- **Stop Loss**: 20398.78
- **Risk**: 25.00 points
- **TP 1RR**: 20448.77 ✅
- **TP 2RR**: 20473.77 ✅
- **TP 3RR**: 20498.76 ✅
- **TP 4RR**: 20523.76 ✅
- **TP 15RR**: 20798.72 ❌
- **PnL**: -25.00 points (-1.0R)
- **MFE**: 124.20 points
- **MAE**: 30.60 points

### Trade #496 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 14:15:00
- **FVG 5m**: 20379.15 - 20397.25
- **Entrée**: 20367.16 @ 2025-03-19 14:52:00
- **Stop Loss**: 20407.45
- **Risk**: 40.29 points
- **TP 1RR**: 20326.87 ❌
- **TP 2RR**: 20286.58 ❌
- **TP 3RR**: 20246.28 ❌
- **TP 4RR**: 20205.99 ❌
- **TP 15RR**: 19762.78 ❌
- **PnL**: -40.29 points (-1.0R)
- **MFE**: 31.62 points
- **MAE**: 40.80 points

### Trade #497 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 14:15:00
- **FVG 5m**: 20379.15 - 20397.25
- **Entrée**: 20367.16 @ 2025-03-19 14:52:00
- **Stop Loss**: 20407.45
- **Risk**: 40.29 points
- **TP 1RR**: 20326.87 ❌
- **TP 2RR**: 20286.58 ❌
- **TP 3RR**: 20246.28 ❌
- **TP 4RR**: 20205.99 ❌
- **TP 15RR**: 19762.78 ❌
- **PnL**: -40.29 points (-1.0R)
- **MFE**: 31.62 points
- **MAE**: 40.80 points

### Trade #498 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 05:00:00
- **FVG 5m**: 20264.89 - 20297.03
- **Entrée**: 20254.69 @ 2025-03-20 05:12:00
- **Stop Loss**: 20307.18
- **Risk**: 52.48 points
- **TP 1RR**: 20202.21 ✅
- **TP 2RR**: 20149.73 ✅
- **TP 3RR**: 20097.24 ❌
- **TP 4RR**: 20044.76 ❌
- **TP 15RR**: 19467.45 ❌
- **PnL**: -52.48 points (-1.0R)
- **MFE**: 122.67 points
- **MAE**: 53.05 points

### Trade #499 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-20 05:15:00
- **FVG 5m**: 20190.43 - 20204.45
- **Entrée**: 20205.73 @ 2025-03-20 05:52:00
- **Stop Loss**: 20180.33
- **Risk**: 25.40 points
- **TP 1RR**: 20231.12 ✅
- **TP 2RR**: 20256.52 ✅
- **TP 3RR**: 20281.92 ❌
- **TP 4RR**: 20307.32 ❌
- **TP 15RR**: 20586.68 ❌
- **PnL**: -25.40 points (-1.0R)
- **MFE**: 55.60 points
- **MAE**: 27.80 points

### Trade #500 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 09:15:00
- **FVG 5m**: 20473.51 - 20486.26
- **Entrée**: 20463.56 @ 2025-03-20 09:52:00
- **Stop Loss**: 20496.50
- **Risk**: 32.94 points
- **TP 1RR**: 20430.62 ✅
- **TP 2RR**: 20397.68 ✅
- **TP 3RR**: 20364.74 ✅
- **TP 4RR**: 20331.80 ✅
- **TP 15RR**: 19969.45 ❌
- **PnL**: -32.94 points (-1.0R)
- **MFE**: 467.21 points
- **MAE**: 39.53 points

### Trade #501 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-20 09:15:00
- **FVG 5m**: 20406.18 - 20416.89
- **Entrée**: 20424.29 @ 2025-03-20 10:42:00
- **Stop Loss**: 20395.98
- **Risk**: 28.31 points
- **TP 1RR**: 20452.60 ✅
- **TP 2RR**: 20480.91 ❌
- **TP 3RR**: 20509.22 ❌
- **TP 4RR**: 20537.53 ❌
- **TP 15RR**: 20848.93 ❌
- **PnL**: -28.31 points (-1.0R)
- **MFE**: 34.68 points
- **MAE**: 30.60 points

### Trade #502 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 09:45:00
- **FVG 5m**: 20406.18 - 20425.05
- **Entrée**: 20403.12 @ 2025-03-20 10:33:00
- **Stop Loss**: 20435.26
- **Risk**: 32.14 points
- **TP 1RR**: 20370.97 ✅
- **TP 2RR**: 20338.83 ❌
- **TP 3RR**: 20306.68 ❌
- **TP 4RR**: 20274.54 ❌
- **TP 15RR**: 19920.95 ❌
- **PnL**: -32.14 points (-1.0R)
- **MFE**: 36.72 points
- **MAE**: 38.51 points

### Trade #503 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 12:15:00
- **FVG 5m**: 20256.73 - 20266.68
- **Entrée**: 20248.32 @ 2025-03-20 12:54:00
- **Stop Loss**: 20276.81
- **Risk**: 28.50 points
- **TP 1RR**: 20219.82 ❌
- **TP 2RR**: 20191.33 ❌
- **TP 3RR**: 20162.83 ❌
- **TP 4RR**: 20134.34 ❌
- **TP 15RR**: 19820.89 ❌
- **PnL**: -28.50 points (-1.0R)
- **MFE**: 15.05 points
- **MAE**: 30.35 points

### Trade #504 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 00:45:00
- **FVG 5m**: 20272.54 - 20281.73
- **Entrée**: 20285.30 @ 2025-03-21 01:54:00
- **Stop Loss**: 20262.41
- **Risk**: 22.89 points
- **TP 1RR**: 20308.18 ❌
- **TP 2RR**: 20331.07 ❌
- **TP 3RR**: 20353.96 ❌
- **TP 4RR**: 20376.85 ❌
- **TP 15RR**: 20628.61 ❌
- **PnL**: -22.89 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 23.21 points

### Trade #505 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 01:30:00
- **FVG 5m**: 20272.54 - 20281.73
- **Entrée**: 20285.30 @ 2025-03-21 01:54:00
- **Stop Loss**: 20262.41
- **Risk**: 22.89 points
- **TP 1RR**: 20308.18 ❌
- **TP 2RR**: 20331.07 ❌
- **TP 3RR**: 20353.96 ❌
- **TP 4RR**: 20376.85 ❌
- **TP 15RR**: 20628.61 ❌
- **PnL**: -22.89 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 23.21 points

### Trade #506 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 03:45:00
- **FVG 5m**: 20196.04 - 20214.40
- **Entrée**: 20221.03 @ 2025-03-21 05:04:00
- **Stop Loss**: 20185.94
- **Risk**: 35.09 points
- **TP 1RR**: 20256.12 ❌
- **TP 2RR**: 20291.21 ❌
- **TP 3RR**: 20326.30 ❌
- **TP 4RR**: 20361.39 ❌
- **TP 15RR**: 20747.39 ❌
- **PnL**: -35.09 points (-1.0R)
- **MFE**: 23.21 points
- **MAE**: 38.00 points

### Trade #507 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 05:00:00
- **FVG 5m**: 20198.33 - 20207.00
- **Entrée**: 20213.12 @ 2025-03-21 07:02:00
- **Stop Loss**: 20188.23
- **Risk**: 24.89 points
- **TP 1RR**: 20238.01 ❌
- **TP 2RR**: 20262.91 ❌
- **TP 3RR**: 20287.80 ❌
- **TP 4RR**: 20312.69 ❌
- **TP 15RR**: 20586.48 ❌
- **PnL**: -24.89 points (-1.0R)
- **MFE**: 15.56 points
- **MAE**: 26.01 points

### Trade #508 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 08:30:00
- **FVG 5m**: 20055.26 - 20058.32
- **Entrée**: 20068.01 @ 2025-03-21 08:45:00
- **Stop Loss**: 20045.23
- **Risk**: 22.78 points
- **TP 1RR**: 20090.79 ✅
- **TP 2RR**: 20113.57 ✅
- **TP 3RR**: 20136.35 ✅
- **TP 4RR**: 20159.13 ✅
- **TP 15RR**: 20409.70 ✅
- **PnL**: 341.68 points (15.0R)
- **MFE**: 408.04 points
- **MAE**: 9.69 points

### Trade #509 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 08:30:00
- **FVG 5m**: 20055.26 - 20058.32
- **Entrée**: 20068.01 @ 2025-03-21 08:45:00
- **Stop Loss**: 20045.23
- **Risk**: 22.78 points
- **TP 1RR**: 20090.79 ✅
- **TP 2RR**: 20113.57 ✅
- **TP 3RR**: 20136.35 ✅
- **TP 4RR**: 20159.13 ✅
- **TP 15RR**: 20409.70 ✅
- **PnL**: 341.68 points (15.0R)
- **MFE**: 408.04 points
- **MAE**: 9.69 points

### Trade #510 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 08:45:00
- **FVG 5m**: 20132.28 - 20134.83
- **Entrée**: 20142.48 @ 2025-03-21 09:22:00
- **Stop Loss**: 20122.21
- **Risk**: 20.27 points
- **TP 1RR**: 20162.75 ✅
- **TP 2RR**: 20183.02 ❌
- **TP 3RR**: 20203.28 ❌
- **TP 4RR**: 20223.55 ❌
- **TP 15RR**: 20446.49 ❌
- **PnL**: -20.27 points (-1.0R)
- **MFE**: 28.56 points
- **MAE**: 21.68 points

### Trade #511 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 09:15:00
- **FVG 5m**: 20149.62 - 20179.97
- **Entrée**: 20182.27 @ 2025-03-21 09:58:00
- **Stop Loss**: 20139.55
- **Risk**: 42.72 points
- **TP 1RR**: 20224.98 ❌
- **TP 2RR**: 20267.70 ❌
- **TP 3RR**: 20310.42 ❌
- **TP 4RR**: 20353.14 ❌
- **TP 15RR**: 20823.04 ❌
- **PnL**: -42.72 points (-1.0R)
- **MFE**: 28.05 points
- **MAE**: 54.07 points

### Trade #512 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 09:45:00
- **FVG 5m**: 20149.62 - 20179.97
- **Entrée**: 20182.27 @ 2025-03-21 09:58:00
- **Stop Loss**: 20139.55
- **Risk**: 42.72 points
- **TP 1RR**: 20224.98 ❌
- **TP 2RR**: 20267.70 ❌
- **TP 3RR**: 20310.42 ❌
- **TP 4RR**: 20353.14 ❌
- **TP 15RR**: 20823.04 ❌
- **PnL**: -42.72 points (-1.0R)
- **MFE**: 28.05 points
- **MAE**: 54.07 points

### Trade #513 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 09:45:00
- **FVG 5m**: 20149.62 - 20179.97
- **Entrée**: 20182.27 @ 2025-03-21 09:58:00
- **Stop Loss**: 20139.55
- **Risk**: 42.72 points
- **TP 1RR**: 20224.98 ❌
- **TP 2RR**: 20267.70 ❌
- **TP 3RR**: 20310.42 ❌
- **TP 4RR**: 20353.14 ❌
- **TP 15RR**: 20823.04 ❌
- **PnL**: -42.72 points (-1.0R)
- **MFE**: 28.05 points
- **MAE**: 54.07 points

### Trade #514 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-21 11:30:00
- **FVG 5m**: 20253.42 - 20260.81
- **Entrée**: 20251.89 @ 2025-03-21 12:11:00
- **Stop Loss**: 20270.94
- **Risk**: 19.06 points
- **TP 1RR**: 20232.83 ✅
- **TP 2RR**: 20213.78 ✅
- **TP 3RR**: 20194.72 ❌
- **TP 4RR**: 20175.66 ❌
- **TP 15RR**: 19966.04 ❌
- **PnL**: -19.06 points (-1.0R)
- **MFE**: 52.54 points
- **MAE**: 23.72 points

### Trade #515 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-21 11:30:00
- **FVG 5m**: 20253.42 - 20260.81
- **Entrée**: 20251.89 @ 2025-03-21 12:11:00
- **Stop Loss**: 20270.94
- **Risk**: 19.06 points
- **TP 1RR**: 20232.83 ✅
- **TP 2RR**: 20213.78 ✅
- **TP 3RR**: 20194.72 ❌
- **TP 4RR**: 20175.66 ❌
- **TP 15RR**: 19966.04 ❌
- **PnL**: -19.06 points (-1.0R)
- **MFE**: 52.54 points
- **MAE**: 23.72 points

### Trade #516 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-23 20:30:00
- **FVG 5m**: 20514.31 - 20517.37
- **Entrée**: 20514.05 @ 2025-03-23 22:29:00
- **Stop Loss**: 20527.63
- **Risk**: 13.57 points
- **TP 1RR**: 20500.48 ✅
- **TP 2RR**: 20486.91 ❌
- **TP 3RR**: 20473.33 ❌
- **TP 4RR**: 20459.76 ❌
- **TP 15RR**: 20310.44 ❌
- **PnL**: -13.57 points (-1.0R)
- **MFE**: 14.03 points
- **MAE**: 15.05 points

### Trade #517 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-24 08:45:00
- **FVG 5m**: 20728.53 - 20732.87
- **Entrée**: 20735.16 @ 2025-03-24 09:16:00
- **Stop Loss**: 20718.17
- **Risk**: 16.99 points
- **TP 1RR**: 20752.16 ✅
- **TP 2RR**: 20769.15 ✅
- **TP 3RR**: 20786.15 ✅
- **TP 4RR**: 20803.14 ❌
- **TP 15RR**: 20990.09 ❌
- **PnL**: -16.99 points (-1.0R)
- **MFE**: 55.34 points
- **MAE**: 17.85 points

### Trade #518 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 11:15:00
- **FVG 5m**: 20757.09 - 20765.26
- **Entrée**: 20752.25 @ 2025-03-24 11:26:00
- **Stop Loss**: 20775.64
- **Risk**: 23.39 points
- **TP 1RR**: 20728.86 ✅
- **TP 2RR**: 20705.47 ❌
- **TP 3RR**: 20682.08 ❌
- **TP 4RR**: 20658.69 ❌
- **TP 15RR**: 20401.41 ❌
- **PnL**: -23.39 points (-1.0R)
- **MFE**: 35.70 points
- **MAE**: 30.09 points

### Trade #519 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 14:00:00
- **FVG 5m**: 20770.36 - 20773.16
- **Entrée**: 20769.08 @ 2025-03-24 15:54:00
- **Stop Loss**: 20783.55
- **Risk**: 14.47 points
- **TP 1RR**: 20754.61 ✅
- **TP 2RR**: 20740.15 ❌
- **TP 3RR**: 20725.68 ❌
- **TP 4RR**: 20711.21 ❌
- **TP 15RR**: 20552.08 ❌
- **PnL**: -14.47 points (-1.0R)
- **MFE**: 26.27 points
- **MAE**: 15.30 points

### Trade #520 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 14:15:00
- **FVG 5m**: 20770.36 - 20773.16
- **Entrée**: 20769.08 @ 2025-03-24 15:54:00
- **Stop Loss**: 20783.55
- **Risk**: 14.47 points
- **TP 1RR**: 20754.61 ✅
- **TP 2RR**: 20740.15 ❌
- **TP 3RR**: 20725.68 ❌
- **TP 4RR**: 20711.21 ❌
- **TP 15RR**: 20552.08 ❌
- **PnL**: -14.47 points (-1.0R)
- **MFE**: 26.27 points
- **MAE**: 15.30 points

### Trade #521 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 14:45:00
- **FVG 5m**: 20770.36 - 20773.16
- **Entrée**: 20769.08 @ 2025-03-24 15:54:00
- **Stop Loss**: 20783.55
- **Risk**: 14.47 points
- **TP 1RR**: 20754.61 ✅
- **TP 2RR**: 20740.15 ❌
- **TP 3RR**: 20725.68 ❌
- **TP 4RR**: 20711.21 ❌
- **TP 15RR**: 20552.08 ❌
- **PnL**: -14.47 points (-1.0R)
- **MFE**: 26.27 points
- **MAE**: 15.30 points

### Trade #522 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-25 04:30:00
- **FVG 5m**: 20742.81 - 20755.82
- **Entrée**: 20760.41 @ 2025-03-25 05:20:00
- **Stop Loss**: 20732.44
- **Risk**: 27.97 points
- **TP 1RR**: 20788.38 ✅
- **TP 2RR**: 20816.35 ✅
- **TP 3RR**: 20844.31 ✅
- **TP 4RR**: 20872.28 ✅
- **TP 15RR**: 21179.93 ❌
- **PnL**: -27.97 points (-1.0R)
- **MFE**: 189.23 points
- **MAE**: 45.14 points

### Trade #523 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-25 04:45:00
- **FVG 5m**: 20742.81 - 20755.82
- **Entrée**: 20760.41 @ 2025-03-25 05:20:00
- **Stop Loss**: 20732.44
- **Risk**: 27.97 points
- **TP 1RR**: 20788.38 ✅
- **TP 2RR**: 20816.35 ✅
- **TP 3RR**: 20844.31 ✅
- **TP 4RR**: 20872.28 ✅
- **TP 15RR**: 21179.93 ❌
- **PnL**: -27.97 points (-1.0R)
- **MFE**: 189.23 points
- **MAE**: 45.14 points

### Trade #524 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-25 05:00:00
- **FVG 5m**: 20742.81 - 20755.82
- **Entrée**: 20760.41 @ 2025-03-25 05:20:00
- **Stop Loss**: 20732.44
- **Risk**: 27.97 points
- **TP 1RR**: 20788.38 ✅
- **TP 2RR**: 20816.35 ✅
- **TP 3RR**: 20844.31 ✅
- **TP 4RR**: 20872.28 ✅
- **TP 15RR**: 21179.93 ❌
- **PnL**: -27.97 points (-1.0R)
- **MFE**: 189.23 points
- **MAE**: 45.14 points

### Trade #525 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 06:00:00
- **FVG 5m**: 20823.15 - 20834.88
- **Entrée**: 20822.89 @ 2025-03-25 07:54:00
- **Stop Loss**: 20845.30
- **Risk**: 22.40 points
- **TP 1RR**: 20800.49 ❌
- **TP 2RR**: 20778.08 ❌
- **TP 3RR**: 20755.68 ❌
- **TP 4RR**: 20733.28 ❌
- **TP 15RR**: 20486.84 ❌
- **PnL**: -22.40 points (-1.0R)
- **MFE**: 10.46 points
- **MAE**: 22.70 points

### Trade #526 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 10:45:00
- **FVG 5m**: 20871.35 - 20878.23
- **Entrée**: 20869.56 @ 2025-03-25 12:14:00
- **Stop Loss**: 20888.67
- **Risk**: 19.11 points
- **TP 1RR**: 20850.45 ✅
- **TP 2RR**: 20831.34 ✅
- **TP 3RR**: 20812.23 ✅
- **TP 4RR**: 20793.12 ❌
- **TP 15RR**: 20582.91 ❌
- **PnL**: -19.11 points (-1.0R)
- **MFE**: 57.38 points
- **MAE**: 27.29 points

### Trade #527 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 21:00:00
- **FVG 5m**: 20893.28 - 20907.56
- **Entrée**: 20890.98 @ 2025-03-25 21:24:00
- **Stop Loss**: 20918.01
- **Risk**: 27.03 points
- **TP 1RR**: 20863.95 ✅
- **TP 2RR**: 20836.92 ✅
- **TP 3RR**: 20809.89 ✅
- **TP 4RR**: 20782.86 ✅
- **TP 15RR**: 20485.53 ✅
- **PnL**: 405.46 points (15.0R)
- **MFE**: 410.85 points
- **MAE**: 19.38 points

### Trade #528 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 21:15:00
- **FVG 5m**: 20893.28 - 20895.57
- **Entrée**: 20892.51 @ 2025-03-25 22:32:00
- **Stop Loss**: 20906.02
- **Risk**: 13.51 points
- **TP 1RR**: 20879.01 ❌
- **TP 2RR**: 20865.50 ❌
- **TP 3RR**: 20851.99 ❌
- **TP 4RR**: 20838.48 ❌
- **TP 15RR**: 20689.89 ❌
- **PnL**: -13.51 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 14.03 points

### Trade #529 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 03:00:00
- **FVG 5m**: 20867.52 - 20872.11
- **Entrée**: 20873.13 @ 2025-03-26 03:26:00
- **Stop Loss**: 20857.09
- **Risk**: 16.04 points
- **TP 1RR**: 20889.18 ❌
- **TP 2RR**: 20905.22 ❌
- **TP 3RR**: 20921.26 ❌
- **TP 4RR**: 20937.31 ❌
- **TP 15RR**: 21113.80 ❌
- **PnL**: -16.04 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 16.83 points

### Trade #530 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 05:00:00
- **FVG 5m**: 20873.64 - 20877.21
- **Entrée**: 20881.55 @ 2025-03-26 05:56:00
- **Stop Loss**: 20863.20
- **Risk**: 18.34 points
- **TP 1RR**: 20899.89 ✅
- **TP 2RR**: 20918.23 ❌
- **TP 3RR**: 20936.58 ❌
- **TP 4RR**: 20954.92 ❌
- **TP 15RR**: 21156.69 ❌
- **PnL**: -18.34 points (-1.0R)
- **MFE**: 23.46 points
- **MAE**: 19.38 points

### Trade #531 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 05:45:00
- **FVG 5m**: 20873.64 - 20877.21
- **Entrée**: 20881.55 @ 2025-03-26 05:56:00
- **Stop Loss**: 20863.20
- **Risk**: 18.34 points
- **TP 1RR**: 20899.89 ✅
- **TP 2RR**: 20918.23 ❌
- **TP 3RR**: 20936.58 ❌
- **TP 4RR**: 20954.92 ❌
- **TP 15RR**: 21156.69 ❌
- **PnL**: -18.34 points (-1.0R)
- **MFE**: 23.46 points
- **MAE**: 19.38 points

### Trade #532 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 08:45:00
- **FVG 5m**: 20765.51 - 20768.06
- **Entrée**: 20753.01 @ 2025-03-26 08:56:00
- **Stop Loss**: 20778.44
- **Risk**: 25.43 points
- **TP 1RR**: 20727.58 ✅
- **TP 2RR**: 20702.15 ✅
- **TP 3RR**: 20676.72 ✅
- **TP 4RR**: 20651.29 ✅
- **TP 15RR**: 20371.56 ✅
- **PnL**: 381.46 points (15.0R)
- **MFE**: 388.15 points
- **MAE**: 12.50 points

### Trade #533 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 10:45:00
- **FVG 5m**: 20559.96 - 20575.77
- **Entrée**: 20559.19 @ 2025-03-26 11:54:00
- **Stop Loss**: 20586.06
- **Risk**: 26.86 points
- **TP 1RR**: 20532.33 ✅
- **TP 2RR**: 20505.47 ✅
- **TP 3RR**: 20478.60 ✅
- **TP 4RR**: 20451.74 ✅
- **TP 15RR**: 20156.23 ❌
- **PnL**: -26.86 points (-1.0R)
- **MFE**: 221.11 points
- **MAE**: 28.82 points

### Trade #534 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 11:00:00
- **FVG 5m**: 20506.40 - 20518.65
- **Entrée**: 20524.77 @ 2025-03-26 13:12:00
- **Stop Loss**: 20496.15
- **Risk**: 28.62 points
- **TP 1RR**: 20553.38 ❌
- **TP 2RR**: 20582.00 ❌
- **TP 3RR**: 20610.61 ❌
- **TP 4RR**: 20639.23 ❌
- **TP 15RR**: 20953.99 ❌
- **PnL**: -28.62 points (-1.0R)
- **MFE**: 26.78 points
- **MAE**: 29.33 points

### Trade #535 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 11:45:00
- **FVG 5m**: 20505.13 - 20517.12
- **Entrée**: 20503.09 @ 2025-03-26 12:32:00
- **Stop Loss**: 20527.37
- **Risk**: 24.29 points
- **TP 1RR**: 20478.80 ❌
- **TP 2RR**: 20454.52 ❌
- **TP 3RR**: 20430.23 ❌
- **TP 4RR**: 20405.95 ❌
- **TP 15RR**: 20138.81 ❌
- **PnL**: -24.29 points (-1.0R)
- **MFE**: 22.95 points
- **MAE**: 30.86 points

### Trade #536 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 11:45:00
- **FVG 5m**: 20505.13 - 20517.12
- **Entrée**: 20503.09 @ 2025-03-26 12:32:00
- **Stop Loss**: 20527.37
- **Risk**: 24.29 points
- **TP 1RR**: 20478.80 ❌
- **TP 2RR**: 20454.52 ❌
- **TP 3RR**: 20430.23 ❌
- **TP 4RR**: 20405.95 ❌
- **TP 15RR**: 20138.81 ❌
- **PnL**: -24.29 points (-1.0R)
- **MFE**: 22.95 points
- **MAE**: 30.86 points

### Trade #537 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 11:45:00
- **FVG 5m**: 20505.13 - 20517.12
- **Entrée**: 20503.09 @ 2025-03-26 12:32:00
- **Stop Loss**: 20527.37
- **Risk**: 24.29 points
- **TP 1RR**: 20478.80 ❌
- **TP 2RR**: 20454.52 ❌
- **TP 3RR**: 20430.23 ❌
- **TP 4RR**: 20405.95 ❌
- **TP 15RR**: 20138.81 ❌
- **PnL**: -24.29 points (-1.0R)
- **MFE**: 22.95 points
- **MAE**: 30.86 points

### Trade #538 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 12:15:00
- **FVG 5m**: 20505.13 - 20517.12
- **Entrée**: 20503.09 @ 2025-03-26 12:32:00
- **Stop Loss**: 20527.37
- **Risk**: 24.29 points
- **TP 1RR**: 20478.80 ❌
- **TP 2RR**: 20454.52 ❌
- **TP 3RR**: 20430.23 ❌
- **TP 4RR**: 20405.95 ❌
- **TP 15RR**: 20138.81 ❌
- **PnL**: -24.29 points (-1.0R)
- **MFE**: 22.95 points
- **MAE**: 30.86 points

### Trade #539 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 12:30:00
- **FVG 5m**: 20525.28 - 20527.83
- **Entrée**: 20518.90 @ 2025-03-26 13:34:00
- **Stop Loss**: 20538.09
- **Risk**: 19.19 points
- **TP 1RR**: 20499.71 ✅
- **TP 2RR**: 20480.52 ✅
- **TP 3RR**: 20461.33 ✅
- **TP 4RR**: 20442.14 ❌
- **TP 15RR**: 20231.05 ❌
- **PnL**: -19.19 points (-1.0R)
- **MFE**: 70.90 points
- **MAE**: 20.91 points

### Trade #540 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 12:30:00
- **FVG 5m**: 20506.40 - 20518.65
- **Entrée**: 20524.77 @ 2025-03-26 13:12:00
- **Stop Loss**: 20496.15
- **Risk**: 28.62 points
- **TP 1RR**: 20553.38 ❌
- **TP 2RR**: 20582.00 ❌
- **TP 3RR**: 20610.61 ❌
- **TP 4RR**: 20639.23 ❌
- **TP 15RR**: 20953.99 ❌
- **PnL**: -28.62 points (-1.0R)
- **MFE**: 26.78 points
- **MAE**: 29.33 points

### Trade #541 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 12:30:00
- **FVG 5m**: 20506.40 - 20518.65
- **Entrée**: 20524.77 @ 2025-03-26 13:12:00
- **Stop Loss**: 20496.15
- **Risk**: 28.62 points
- **TP 1RR**: 20553.38 ❌
- **TP 2RR**: 20582.00 ❌
- **TP 3RR**: 20610.61 ❌
- **TP 4RR**: 20639.23 ❌
- **TP 15RR**: 20953.99 ❌
- **PnL**: -28.62 points (-1.0R)
- **MFE**: 26.78 points
- **MAE**: 29.33 points

### Trade #542 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 18:30:00
- **FVG 5m**: 20446.98 - 20451.06
- **Entrée**: 20451.32 @ 2025-03-26 18:42:00
- **Stop Loss**: 20436.76
- **Risk**: 14.56 points
- **TP 1RR**: 20465.88 ✅
- **TP 2RR**: 20480.44 ✅
- **TP 3RR**: 20495.00 ✅
- **TP 4RR**: 20509.55 ✅
- **TP 15RR**: 20669.70 ❌
- **PnL**: -14.56 points (-1.0R)
- **MFE**: 101.50 points
- **MAE**: 17.60 points

### Trade #543 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 08:45:00
- **FVG 5m**: 20499.77 - 20510.74
- **Entrée**: 20525.28 @ 2025-03-27 09:29:00
- **Stop Loss**: 20489.52
- **Risk**: 35.75 points
- **TP 1RR**: 20561.03 ✅
- **TP 2RR**: 20596.78 ✅
- **TP 3RR**: 20632.53 ❌
- **TP 4RR**: 20668.29 ❌
- **TP 15RR**: 21061.56 ❌
- **PnL**: -35.75 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 36.21 points

### Trade #544 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 08:45:00
- **FVG 5m**: 20499.77 - 20510.74
- **Entrée**: 20525.28 @ 2025-03-27 09:29:00
- **Stop Loss**: 20489.52
- **Risk**: 35.75 points
- **TP 1RR**: 20561.03 ✅
- **TP 2RR**: 20596.78 ✅
- **TP 3RR**: 20632.53 ❌
- **TP 4RR**: 20668.29 ❌
- **TP 15RR**: 21061.56 ❌
- **PnL**: -35.75 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 36.21 points

### Trade #545 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 08:45:00
- **FVG 5m**: 20499.77 - 20510.74
- **Entrée**: 20525.28 @ 2025-03-27 09:29:00
- **Stop Loss**: 20489.52
- **Risk**: 35.75 points
- **TP 1RR**: 20561.03 ✅
- **TP 2RR**: 20596.78 ✅
- **TP 3RR**: 20632.53 ❌
- **TP 4RR**: 20668.29 ❌
- **TP 15RR**: 21061.56 ❌
- **PnL**: -35.75 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 36.21 points

### Trade #546 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:15:00
- **FVG 5m**: 20540.07 - 20543.64
- **Entrée**: 20538.54 @ 2025-03-27 10:29:00
- **Stop Loss**: 20553.91
- **Risk**: 15.37 points
- **TP 1RR**: 20523.16 ✅
- **TP 2RR**: 20507.79 ✅
- **TP 3RR**: 20492.42 ✅
- **TP 4RR**: 20477.05 ✅
- **TP 15RR**: 20307.95 ❌
- **PnL**: -15.37 points (-1.0R)
- **MFE**: 96.65 points
- **MAE**: 22.44 points

### Trade #547 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:15:00
- **FVG 5m**: 20540.07 - 20543.64
- **Entrée**: 20538.54 @ 2025-03-27 10:29:00
- **Stop Loss**: 20553.91
- **Risk**: 15.37 points
- **TP 1RR**: 20523.16 ✅
- **TP 2RR**: 20507.79 ✅
- **TP 3RR**: 20492.42 ✅
- **TP 4RR**: 20477.05 ✅
- **TP 15RR**: 20307.95 ❌
- **PnL**: -15.37 points (-1.0R)
- **MFE**: 96.65 points
- **MAE**: 22.44 points

### Trade #548 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:15:00
- **FVG 5m**: 20540.07 - 20543.64
- **Entrée**: 20538.54 @ 2025-03-27 10:29:00
- **Stop Loss**: 20553.91
- **Risk**: 15.37 points
- **TP 1RR**: 20523.16 ✅
- **TP 2RR**: 20507.79 ✅
- **TP 3RR**: 20492.42 ✅
- **TP 4RR**: 20477.05 ✅
- **TP 15RR**: 20307.95 ❌
- **PnL**: -15.37 points (-1.0R)
- **MFE**: 96.65 points
- **MAE**: 22.44 points

### Trade #549 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:30:00
- **FVG 5m**: 20455.65 - 20481.41
- **Entrée**: 20450.30 @ 2025-03-27 11:49:00
- **Stop Loss**: 20491.65
- **Risk**: 41.35 points
- **TP 1RR**: 20408.94 ✅
- **TP 2RR**: 20367.59 ❌
- **TP 3RR**: 20326.24 ❌
- **TP 4RR**: 20284.88 ❌
- **TP 15RR**: 19829.99 ❌
- **PnL**: -41.35 points (-1.0R)
- **MFE**: 47.18 points
- **MAE**: 41.57 points

### Trade #550 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 15:00:00
- **FVG 5m**: 20407.71 - 20411.79
- **Entrée**: 20412.04 @ 2025-03-27 15:37:00
- **Stop Loss**: 20397.50
- **Risk**: 14.54 points
- **TP 1RR**: 20426.58 ❌
- **TP 2RR**: 20441.12 ❌
- **TP 3RR**: 20455.66 ❌
- **TP 4RR**: 20470.20 ❌
- **TP 15RR**: 20630.13 ❌
- **PnL**: -14.54 points (-1.0R)
- **MFE**: 9.44 points
- **MAE**: 19.38 points

### Trade #551 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 01:45:00
- **FVG 5m**: 20335.03 - 20337.83
- **Entrée**: 20334.26 @ 2025-03-28 01:56:00
- **Stop Loss**: 20348.00
- **Risk**: 13.74 points
- **TP 1RR**: 20320.52 ✅
- **TP 2RR**: 20306.78 ✅
- **TP 3RR**: 20293.04 ✅
- **TP 4RR**: 20279.30 ✅
- **TP 15RR**: 20128.17 ❌
- **PnL**: -13.74 points (-1.0R)
- **MFE**: 90.02 points
- **MAE**: 18.11 points

### Trade #552 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 02:30:00
- **FVG 5m**: 20287.08 - 20290.40
- **Entrée**: 20266.68 @ 2025-03-28 02:47:00
- **Stop Loss**: 20300.54
- **Risk**: 33.86 points
- **TP 1RR**: 20232.82 ❌
- **TP 2RR**: 20198.95 ❌
- **TP 3RR**: 20165.09 ❌
- **TP 4RR**: 20131.23 ❌
- **TP 15RR**: 19758.74 ❌
- **PnL**: -33.86 points (-1.0R)
- **MFE**: 22.44 points
- **MAE**: 41.06 points

### Trade #553 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 02:30:00
- **FVG 5m**: 20287.08 - 20290.40
- **Entrée**: 20266.68 @ 2025-03-28 02:47:00
- **Stop Loss**: 20300.54
- **Risk**: 33.86 points
- **TP 1RR**: 20232.82 ❌
- **TP 2RR**: 20198.95 ❌
- **TP 3RR**: 20165.09 ❌
- **TP 4RR**: 20131.23 ❌
- **TP 15RR**: 19758.74 ❌
- **PnL**: -33.86 points (-1.0R)
- **MFE**: 22.44 points
- **MAE**: 41.06 points

### Trade #554 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 05:00:00
- **FVG 5m**: 20330.18 - 20337.58
- **Entrée**: 20339.62 @ 2025-03-28 05:11:00
- **Stop Loss**: 20320.02
- **Risk**: 19.60 points
- **TP 1RR**: 20359.22 ✅
- **TP 2RR**: 20378.82 ❌
- **TP 3RR**: 20398.42 ❌
- **TP 4RR**: 20418.02 ❌
- **TP 15RR**: 20633.63 ❌
- **PnL**: -19.60 points (-1.0R)
- **MFE**: 31.62 points
- **MAE**: 22.70 points

### Trade #555 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 05:00:00
- **FVG 5m**: 20330.18 - 20337.58
- **Entrée**: 20339.62 @ 2025-03-28 05:11:00
- **Stop Loss**: 20320.02
- **Risk**: 19.60 points
- **TP 1RR**: 20359.22 ✅
- **TP 2RR**: 20378.82 ❌
- **TP 3RR**: 20398.42 ❌
- **TP 4RR**: 20418.02 ❌
- **TP 15RR**: 20633.63 ❌
- **PnL**: -19.60 points (-1.0R)
- **MFE**: 31.62 points
- **MAE**: 22.70 points

### Trade #556 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 05:30:00
- **FVG 5m**: 20335.54 - 20340.38
- **Entrée**: 20341.91 @ 2025-03-28 06:17:00
- **Stop Loss**: 20325.37
- **Risk**: 16.54 points
- **TP 1RR**: 20358.46 ❌
- **TP 2RR**: 20375.00 ❌
- **TP 3RR**: 20391.54 ❌
- **TP 4RR**: 20408.09 ❌
- **TP 15RR**: 20590.06 ❌
- **PnL**: -16.54 points (-1.0R)
- **MFE**: 10.97 points
- **MAE**: 18.62 points

### Trade #557 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 07:30:00
- **FVG 5m**: 20269.74 - 20278.16
- **Entrée**: 20263.11 @ 2025-03-28 07:59:00
- **Stop Loss**: 20288.29
- **Risk**: 25.19 points
- **TP 1RR**: 20237.92 ❌
- **TP 2RR**: 20212.74 ❌
- **TP 3RR**: 20187.55 ❌
- **TP 4RR**: 20162.37 ❌
- **TP 15RR**: 19885.32 ❌
- **PnL**: -25.19 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 45.65 points

### Trade #558 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 09:30:00
- **FVG 5m**: 19976.20 - 19978.75
- **Entrée**: 19981.56 @ 2025-03-28 10:19:00
- **Stop Loss**: 19966.22
- **Risk**: 15.34 points
- **TP 1RR**: 19996.90 ❌
- **TP 2RR**: 20012.25 ❌
- **TP 3RR**: 20027.59 ❌
- **TP 4RR**: 20042.93 ❌
- **TP 15RR**: 20211.71 ❌
- **PnL**: -15.34 points (-1.0R)
- **MFE**: 12.75 points
- **MAE**: 21.42 points

### Trade #559 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 09:30:00
- **FVG 5m**: 19976.20 - 19978.75
- **Entrée**: 19981.56 @ 2025-03-28 10:19:00
- **Stop Loss**: 19966.22
- **Risk**: 15.34 points
- **TP 1RR**: 19996.90 ❌
- **TP 2RR**: 20012.25 ❌
- **TP 3RR**: 20027.59 ❌
- **TP 4RR**: 20042.93 ❌
- **TP 15RR**: 20211.71 ❌
- **PnL**: -15.34 points (-1.0R)
- **MFE**: 12.75 points
- **MAE**: 21.42 points

### Trade #560 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 09:30:00
- **FVG 5m**: 19976.20 - 19978.75
- **Entrée**: 19981.56 @ 2025-03-28 10:19:00
- **Stop Loss**: 19966.22
- **Risk**: 15.34 points
- **TP 1RR**: 19996.90 ❌
- **TP 2RR**: 20012.25 ❌
- **TP 3RR**: 20027.59 ❌
- **TP 4RR**: 20042.93 ❌
- **TP 15RR**: 20211.71 ❌
- **PnL**: -15.34 points (-1.0R)
- **MFE**: 12.75 points
- **MAE**: 21.42 points

### Trade #561 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 10:00:00
- **FVG 5m**: 19976.20 - 19978.75
- **Entrée**: 19981.56 @ 2025-03-28 10:19:00
- **Stop Loss**: 19966.22
- **Risk**: 15.34 points
- **TP 1RR**: 19996.90 ❌
- **TP 2RR**: 20012.25 ❌
- **TP 3RR**: 20027.59 ❌
- **TP 4RR**: 20042.93 ❌
- **TP 15RR**: 20211.71 ❌
- **PnL**: -15.34 points (-1.0R)
- **MFE**: 12.75 points
- **MAE**: 21.42 points

### Trade #562 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 14:45:00
- **FVG 5m**: 19692.87 - 19701.54
- **Entrée**: 19709.19 @ 2025-03-30 17:42:00
- **Stop Loss**: 19683.02
- **Risk**: 26.17 points
- **TP 1RR**: 19735.36 ❌
- **TP 2RR**: 19761.53 ❌
- **TP 3RR**: 19787.70 ❌
- **TP 4RR**: 19813.86 ❌
- **TP 15RR**: 20101.71 ❌
- **PnL**: -26.17 points (-1.0R)
- **MFE**: 1.79 points
- **MAE**: 26.78 points

### Trade #563 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-31 03:15:00
- **FVG 5m**: 19589.58 - 19595.96
- **Entrée**: 19577.60 @ 2025-03-31 04:00:00
- **Stop Loss**: 19605.76
- **Risk**: 28.16 points
- **TP 1RR**: 19549.44 ✅
- **TP 2RR**: 19521.28 ❌
- **TP 3RR**: 19493.12 ❌
- **TP 4RR**: 19464.96 ❌
- **TP 15RR**: 19155.20 ❌
- **PnL**: -28.16 points (-1.0R)
- **MFE**: 28.82 points
- **MAE**: 31.37 points

### Trade #564 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 04:15:00
- **FVG 5m**: 19590.60 - 19601.32
- **Entrée**: 19608.71 @ 2025-03-31 04:28:00
- **Stop Loss**: 19580.81
- **Risk**: 27.90 points
- **TP 1RR**: 19636.61 ❌
- **TP 2RR**: 19664.52 ❌
- **TP 3RR**: 19692.42 ❌
- **TP 4RR**: 19720.32 ❌
- **TP 15RR**: 20027.24 ❌
- **PnL**: -27.90 points (-1.0R)
- **MFE**: 11.22 points
- **MAE**: 32.39 points

### Trade #565 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 06:45:00
- **FVG 5m**: 19550.31 - 19558.98
- **Entrée**: 19569.95 @ 2025-03-31 07:31:00
- **Stop Loss**: 19540.54
- **Risk**: 29.41 points
- **TP 1RR**: 19599.36 ✅
- **TP 2RR**: 19628.77 ❌
- **TP 3RR**: 19658.18 ❌
- **TP 4RR**: 19687.60 ❌
- **TP 15RR**: 20011.13 ❌
- **PnL**: -29.41 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 54.58 points

### Trade #566 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 06:45:00
- **FVG 5m**: 19550.31 - 19558.98
- **Entrée**: 19569.95 @ 2025-03-31 07:31:00
- **Stop Loss**: 19540.54
- **Risk**: 29.41 points
- **TP 1RR**: 19599.36 ✅
- **TP 2RR**: 19628.77 ❌
- **TP 3RR**: 19658.18 ❌
- **TP 4RR**: 19687.60 ❌
- **TP 15RR**: 20011.13 ❌
- **PnL**: -29.41 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 54.58 points

### Trade #567 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 07:15:00
- **FVG 5m**: 19550.31 - 19558.98
- **Entrée**: 19569.95 @ 2025-03-31 07:31:00
- **Stop Loss**: 19540.54
- **Risk**: 29.41 points
- **TP 1RR**: 19599.36 ✅
- **TP 2RR**: 19628.77 ❌
- **TP 3RR**: 19658.18 ❌
- **TP 4RR**: 19687.60 ❌
- **TP 15RR**: 20011.13 ❌
- **PnL**: -29.41 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 54.58 points

### Trade #568 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 09:00:00
- **FVG 5m**: 19471.00 - 19490.12
- **Entrée**: 19518.94 @ 2025-03-31 09:33:00
- **Stop Loss**: 19461.26
- **Risk**: 57.68 points
- **TP 1RR**: 19576.62 ✅
- **TP 2RR**: 19634.30 ✅
- **TP 3RR**: 19691.98 ✅
- **TP 4RR**: 19749.66 ✅
- **TP 15RR**: 20384.15 ✅
- **PnL**: 865.21 points (15.0R)
- **MFE**: 866.32 points
- **MAE**: 42.59 points

### Trade #569 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-31 10:30:00
- **FVG 5m**: 19593.92 - 19603.87
- **Entrée**: 19592.13 @ 2025-03-31 11:07:00
- **Stop Loss**: 19613.67
- **Risk**: 21.53 points
- **TP 1RR**: 19570.60 ✅
- **TP 2RR**: 19549.07 ❌
- **TP 3RR**: 19527.54 ❌
- **TP 4RR**: 19506.00 ❌
- **TP 15RR**: 19269.14 ❌
- **PnL**: -21.53 points (-1.0R)
- **MFE**: 32.39 points
- **MAE**: 32.64 points

### Trade #570 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-31 11:30:00
- **FVG 5m**: 19633.96 - 19668.64
- **Entrée**: 19626.31 @ 2025-03-31 12:19:00
- **Stop Loss**: 19678.48
- **Risk**: 52.17 points
- **TP 1RR**: 19574.14 ❌
- **TP 2RR**: 19521.97 ❌
- **TP 3RR**: 19469.80 ❌
- **TP 4RR**: 19417.63 ❌
- **TP 15RR**: 18843.78 ❌
- **PnL**: -52.17 points (-1.0R)
- **MFE**: 32.64 points
- **MAE**: 60.19 points

### Trade #571 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-31 11:30:00
- **FVG 5m**: 19633.96 - 19668.64
- **Entrée**: 19626.31 @ 2025-03-31 12:19:00
- **Stop Loss**: 19678.48
- **Risk**: 52.17 points
- **TP 1RR**: 19574.14 ❌
- **TP 2RR**: 19521.97 ❌
- **TP 3RR**: 19469.80 ❌
- **TP 4RR**: 19417.63 ❌
- **TP 15RR**: 18843.78 ❌
- **PnL**: -52.17 points (-1.0R)
- **MFE**: 32.64 points
- **MAE**: 60.19 points

### Trade #572 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 13:15:00
- **FVG 5m**: 19761.47 - 19769.12
- **Entrée**: 19780.60 @ 2025-03-31 13:31:00
- **Stop Loss**: 19751.59
- **Risk**: 29.01 points
- **TP 1RR**: 19809.61 ❌
- **TP 2RR**: 19838.61 ❌
- **TP 3RR**: 19867.62 ❌
- **TP 4RR**: 19896.63 ❌
- **TP 15RR**: 20215.71 ❌
- **PnL**: -29.01 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 42.59 points

### Trade #573 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 20:15:00
- **FVG 5m**: 19705.37 - 19721.69
- **Entrée**: 19722.45 @ 2025-03-31 20:44:00
- **Stop Loss**: 19695.51
- **Risk**: 26.94 points
- **TP 1RR**: 19749.39 ✅
- **TP 2RR**: 19776.33 ✅
- **TP 3RR**: 19803.27 ✅
- **TP 4RR**: 19830.21 ✅
- **TP 15RR**: 20126.54 ❌
- **PnL**: -26.94 points (-1.0R)
- **MFE**: 180.81 points
- **MAE**: 33.66 points

### Trade #574 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 00:30:00
- **FVG 5m**: 19758.41 - 19764.53
- **Entrée**: 19755.35 @ 2025-04-01 00:44:00
- **Stop Loss**: 19774.41
- **Risk**: 19.06 points
- **TP 1RR**: 19736.29 ❌
- **TP 2RR**: 19717.23 ❌
- **TP 3RR**: 19698.16 ❌
- **TP 4RR**: 19679.10 ❌
- **TP 15RR**: 19469.40 ❌
- **PnL**: -19.06 points (-1.0R)
- **MFE**: 16.58 points
- **MAE**: 23.72 points

### Trade #575 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 04:00:00
- **FVG 5m**: 19860.93 - 19877.25
- **Entrée**: 19846.14 @ 2025-04-01 05:01:00
- **Stop Loss**: 19887.19
- **Risk**: 41.05 points
- **TP 1RR**: 19805.09 ✅
- **TP 2RR**: 19764.04 ✅
- **TP 3RR**: 19722.99 ✅
- **TP 4RR**: 19681.93 ✅
- **TP 15RR**: 19230.36 ❌
- **PnL**: -41.05 points (-1.0R)
- **MFE**: 197.65 points
- **MAE**: 41.06 points

### Trade #576 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 04:45:00
- **FVG 5m**: 19860.93 - 19877.25
- **Entrée**: 19846.14 @ 2025-04-01 05:01:00
- **Stop Loss**: 19887.19
- **Risk**: 41.05 points
- **TP 1RR**: 19805.09 ✅
- **TP 2RR**: 19764.04 ✅
- **TP 3RR**: 19722.99 ✅
- **TP 4RR**: 19681.93 ✅
- **TP 15RR**: 19230.36 ❌
- **PnL**: -41.05 points (-1.0R)
- **MFE**: 197.65 points
- **MAE**: 41.06 points

### Trade #577 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 06:30:00
- **FVG 5m**: 19763.77 - 19770.14
- **Entrée**: 19771.42 @ 2025-04-01 07:54:00
- **Stop Loss**: 19753.89
- **Risk**: 17.53 points
- **TP 1RR**: 19788.95 ✅
- **TP 2RR**: 19806.48 ❌
- **TP 3RR**: 19824.02 ❌
- **TP 4RR**: 19841.55 ❌
- **TP 15RR**: 20034.41 ❌
- **PnL**: -17.53 points (-1.0R)
- **MFE**: 30.60 points
- **MAE**: 34.94 points

### Trade #578 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 09:15:00
- **FVG 5m**: 19759.69 - 19788.00
- **Entrée**: 19796.16 @ 2025-04-01 09:38:00
- **Stop Loss**: 19749.81
- **Risk**: 46.35 points
- **TP 1RR**: 19842.50 ✅
- **TP 2RR**: 19888.85 ✅
- **TP 3RR**: 19935.20 ✅
- **TP 4RR**: 19981.55 ✅
- **TP 15RR**: 20491.38 ❌
- **PnL**: -46.35 points (-1.0R)
- **MFE**: 296.85 points
- **MAE**: 51.77 points

### Trade #579 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 09:15:00
- **FVG 5m**: 19759.69 - 19788.00
- **Entrée**: 19796.16 @ 2025-04-01 09:38:00
- **Stop Loss**: 19749.81
- **Risk**: 46.35 points
- **TP 1RR**: 19842.50 ✅
- **TP 2RR**: 19888.85 ✅
- **TP 3RR**: 19935.20 ✅
- **TP 4RR**: 19981.55 ✅
- **TP 15RR**: 20491.38 ❌
- **PnL**: -46.35 points (-1.0R)
- **MFE**: 296.85 points
- **MAE**: 51.77 points

### Trade #580 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 10:00:00
- **FVG 5m**: 19948.15 - 19964.47
- **Entrée**: 19976.46 @ 2025-04-01 10:14:00
- **Stop Loss**: 19938.18
- **Risk**: 38.28 points
- **TP 1RR**: 20014.74 ❌
- **TP 2RR**: 20053.02 ❌
- **TP 3RR**: 20091.31 ❌
- **TP 4RR**: 20129.59 ❌
- **TP 15RR**: 20550.69 ❌
- **PnL**: -38.28 points (-1.0R)
- **MFE**: 21.93 points
- **MAE**: 41.82 points

### Trade #581 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 11:30:00
- **FVG 5m**: 19906.58 - 19919.84
- **Entrée**: 19903.52 @ 2025-04-01 12:58:00
- **Stop Loss**: 19929.80
- **Risk**: 26.28 points
- **TP 1RR**: 19877.24 ✅
- **TP 2RR**: 19850.96 ✅
- **TP 3RR**: 19824.68 ✅
- **TP 4RR**: 19798.40 ✅
- **TP 15RR**: 19509.30 ❌
- **PnL**: -26.28 points (-1.0R)
- **MFE**: 128.79 points
- **MAE**: 32.90 points

### Trade #582 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 14:30:00
- **FVG 5m**: 19968.55 - 19984.88
- **Entrée**: 20004.77 @ 2025-04-01 14:54:00
- **Stop Loss**: 19958.57
- **Risk**: 46.20 points
- **TP 1RR**: 20050.97 ✅
- **TP 2RR**: 20097.16 ❌
- **TP 3RR**: 20143.36 ❌
- **TP 4RR**: 20189.56 ❌
- **TP 15RR**: 20697.74 ❌
- **PnL**: -46.20 points (-1.0R)
- **MFE**: 88.24 points
- **MAE**: 54.83 points

### Trade #583 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 17:45:00
- **FVG 5m**: 20013.95 - 20036.14
- **Entrée**: 20011.40 @ 2025-04-01 19:01:00
- **Stop Loss**: 20046.15
- **Risk**: 34.76 points
- **TP 1RR**: 19976.64 ✅
- **TP 2RR**: 19941.89 ✅
- **TP 3RR**: 19907.13 ✅
- **TP 4RR**: 19872.38 ✅
- **TP 15RR**: 19490.06 ❌
- **PnL**: -34.76 points (-1.0R)
- **MFE**: 306.54 points
- **MAE**: 50.75 points

### Trade #584 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 01:00:00
- **FVG 5m**: 19961.16 - 19966.00
- **Entrée**: 19971.36 @ 2025-04-02 01:17:00
- **Stop Loss**: 19951.18
- **Risk**: 20.18 points
- **TP 1RR**: 19991.54 ❌
- **TP 2RR**: 20011.72 ❌
- **TP 3RR**: 20031.90 ❌
- **TP 4RR**: 20052.09 ❌
- **TP 15RR**: 20274.08 ❌
- **PnL**: -20.18 points (-1.0R)
- **MFE**: 12.24 points
- **MAE**: 21.93 points

### Trade #585 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 01:00:00
- **FVG 5m**: 19961.16 - 19966.00
- **Entrée**: 19971.36 @ 2025-04-02 01:17:00
- **Stop Loss**: 19951.18
- **Risk**: 20.18 points
- **TP 1RR**: 19991.54 ❌
- **TP 2RR**: 20011.72 ❌
- **TP 3RR**: 20031.90 ❌
- **TP 4RR**: 20052.09 ❌
- **TP 15RR**: 20274.08 ❌
- **PnL**: -20.18 points (-1.0R)
- **MFE**: 12.24 points
- **MAE**: 21.93 points

### Trade #586 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 07:00:00
- **FVG 5m**: 19731.89 - 19802.28
- **Entrée**: 19808.40 @ 2025-04-02 08:34:00
- **Stop Loss**: 19722.02
- **Risk**: 86.37 points
- **TP 1RR**: 19894.77 ✅
- **TP 2RR**: 19981.14 ✅
- **TP 3RR**: 20067.52 ✅
- **TP 4RR**: 20153.89 ✅
- **TP 15RR**: 21104.00 ❌
- **PnL**: -86.37 points (-1.0R)
- **MFE**: 638.84 points
- **MAE**: 98.19 points

### Trade #587 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 08:30:00
- **FVG 5m**: 19911.43 - 19915.51
- **Entrée**: 19922.65 @ 2025-04-02 08:44:00
- **Stop Loss**: 19901.47
- **Risk**: 21.18 points
- **TP 1RR**: 19943.83 ✅
- **TP 2RR**: 19965.00 ✅
- **TP 3RR**: 19986.18 ✅
- **TP 4RR**: 20007.36 ✅
- **TP 15RR**: 20240.30 ❌
- **PnL**: -21.18 points (-1.0R)
- **MFE**: 92.57 points
- **MAE**: 22.95 points

### Trade #588 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 08:45:00
- **FVG 5m**: 20072.60 - 20079.75
- **Entrée**: 20063.17 @ 2025-04-02 10:44:00
- **Stop Loss**: 20089.78
- **Risk**: 26.62 points
- **TP 1RR**: 20036.55 ✅
- **TP 2RR**: 20009.94 ✅
- **TP 3RR**: 19983.32 ❌
- **TP 4RR**: 19956.70 ❌
- **TP 15RR**: 19663.92 ❌
- **PnL**: -26.62 points (-1.0R)
- **MFE**: 57.38 points
- **MAE**: 37.49 points

### Trade #589 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 09:00:00
- **FVG 5m**: 20072.60 - 20079.75
- **Entrée**: 20063.17 @ 2025-04-02 10:44:00
- **Stop Loss**: 20089.78
- **Risk**: 26.62 points
- **TP 1RR**: 20036.55 ✅
- **TP 2RR**: 20009.94 ✅
- **TP 3RR**: 19983.32 ❌
- **TP 4RR**: 19956.70 ❌
- **TP 15RR**: 19663.92 ❌
- **PnL**: -26.62 points (-1.0R)
- **MFE**: 57.38 points
- **MAE**: 37.49 points

### Trade #590 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 09:00:00
- **FVG 5m**: 20072.60 - 20079.75
- **Entrée**: 20063.17 @ 2025-04-02 10:44:00
- **Stop Loss**: 20089.78
- **Risk**: 26.62 points
- **TP 1RR**: 20036.55 ✅
- **TP 2RR**: 20009.94 ✅
- **TP 3RR**: 19983.32 ❌
- **TP 4RR**: 19956.70 ❌
- **TP 15RR**: 19663.92 ❌
- **PnL**: -26.62 points (-1.0R)
- **MFE**: 57.38 points
- **MAE**: 37.49 points

### Trade #591 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 10:15:00
- **FVG 5m**: 20072.60 - 20079.75
- **Entrée**: 20063.17 @ 2025-04-02 10:44:00
- **Stop Loss**: 20089.78
- **Risk**: 26.62 points
- **TP 1RR**: 20036.55 ✅
- **TP 2RR**: 20009.94 ✅
- **TP 3RR**: 19983.32 ❌
- **TP 4RR**: 19956.70 ❌
- **TP 15RR**: 19663.92 ❌
- **PnL**: -26.62 points (-1.0R)
- **MFE**: 57.38 points
- **MAE**: 37.49 points

### Trade #592 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 10:15:00
- **FVG 5m**: 20074.64 - 20078.72
- **Entrée**: 20091.48 @ 2025-04-02 10:29:00
- **Stop Loss**: 20064.61
- **Risk**: 26.87 points
- **TP 1RR**: 20118.35 ❌
- **TP 2RR**: 20145.21 ❌
- **TP 3RR**: 20172.08 ❌
- **TP 4RR**: 20198.95 ❌
- **TP 15RR**: 20494.51 ❌
- **PnL**: -26.87 points (-1.0R)
- **MFE**: 17.85 points
- **MAE**: 30.60 points

### Trade #593 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 11:45:00
- **FVG 5m**: 20220.01 - 20228.94
- **Entrée**: 20234.80 @ 2025-04-02 12:04:00
- **Stop Loss**: 20209.90
- **Risk**: 24.90 points
- **TP 1RR**: 20259.70 ✅
- **TP 2RR**: 20284.60 ✅
- **TP 3RR**: 20309.51 ❌
- **TP 4RR**: 20334.41 ❌
- **TP 15RR**: 20608.32 ❌
- **PnL**: -24.90 points (-1.0R)
- **MFE**: 55.34 points
- **MAE**: 26.52 points

### Trade #594 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 12:00:00
- **FVG 5m**: 20049.40 - 20076.68
- **Entrée**: 20084.85 @ 2025-04-02 13:37:00
- **Stop Loss**: 20039.37
- **Risk**: 45.47 points
- **TP 1RR**: 20130.32 ❌
- **TP 2RR**: 20175.79 ❌
- **TP 3RR**: 20221.27 ❌
- **TP 4RR**: 20266.74 ❌
- **TP 15RR**: 20766.95 ❌
- **PnL**: -45.47 points (-1.0R)
- **MFE**: 25.76 points
- **MAE**: 53.56 points

### Trade #595 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:00:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20287.53
- **Risk**: 505.40 points
- **TP 1RR**: 19276.73 ✅
- **TP 2RR**: 18771.33 ✅
- **TP 3RR**: 18265.93 ✅
- **TP 4RR**: 17760.53 ✅
- **TP 15RR**: 12201.14 ❌
- **PnL**: -505.40 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 510.56 points

### Trade #596 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:00:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20287.53
- **Risk**: 505.40 points
- **TP 1RR**: 19276.73 ✅
- **TP 2RR**: 18771.33 ✅
- **TP 3RR**: 18265.93 ✅
- **TP 4RR**: 17760.53 ✅
- **TP 15RR**: 12201.14 ❌
- **PnL**: -505.40 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 510.56 points

### Trade #597 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:15:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20287.53
- **Risk**: 505.40 points
- **TP 1RR**: 19276.73 ✅
- **TP 2RR**: 18771.33 ✅
- **TP 3RR**: 18265.93 ✅
- **TP 4RR**: 17760.53 ✅
- **TP 15RR**: 12201.14 ❌
- **PnL**: -505.40 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 510.56 points

### Trade #598 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:15:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20287.53
- **Risk**: 505.40 points
- **TP 1RR**: 19276.73 ✅
- **TP 2RR**: 18771.33 ✅
- **TP 3RR**: 18265.93 ✅
- **TP 4RR**: 17760.53 ✅
- **TP 15RR**: 12201.14 ❌
- **PnL**: -505.40 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 510.56 points

### Trade #599 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:15:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20287.53
- **Risk**: 505.40 points
- **TP 1RR**: 19276.73 ✅
- **TP 2RR**: 18771.33 ✅
- **TP 3RR**: 18265.93 ✅
- **TP 4RR**: 17760.53 ✅
- **TP 15RR**: 12201.14 ❌
- **PnL**: -505.40 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 510.56 points

### Trade #600 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 19:15:00
- **FVG 5m**: 19441.67 - 19472.02
- **Entrée**: 19473.55 @ 2025-04-02 20:48:00
- **Stop Loss**: 19431.95
- **Risk**: 41.60 points
- **TP 1RR**: 19515.15 ✅
- **TP 2RR**: 19556.75 ❌
- **TP 3RR**: 19598.35 ❌
- **TP 4RR**: 19639.94 ❌
- **TP 15RR**: 20097.53 ❌
- **PnL**: -41.60 points (-1.0R)
- **MFE**: 61.72 points
- **MAE**: 44.63 points

### Trade #601 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-03 03:30:00
- **FVG 5m**: 19526.59 - 19531.18
- **Entrée**: 19522.00 @ 2025-04-03 03:43:00
- **Stop Loss**: 19540.95
- **Risk**: 18.95 points
- **TP 1RR**: 19503.06 ❌
- **TP 2RR**: 19484.11 ❌
- **TP 3RR**: 19465.16 ❌
- **TP 4RR**: 19446.22 ❌
- **TP 15RR**: 19237.80 ❌
- **PnL**: -18.95 points (-1.0R)
- **MFE**: 16.32 points
- **MAE**: 23.72 points

### Trade #602 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 06:00:00
- **FVG 5m**: 19380.97 - 19397.29
- **Entrée**: 19405.20 @ 2025-04-03 07:09:00
- **Stop Loss**: 19371.28
- **Risk**: 33.92 points
- **TP 1RR**: 19439.12 ✅
- **TP 2RR**: 19473.04 ❌
- **TP 3RR**: 19506.95 ❌
- **TP 4RR**: 19540.87 ❌
- **TP 15RR**: 19913.97 ❌
- **PnL**: -33.92 points (-1.0R)
- **MFE**: 39.27 points
- **MAE**: 39.27 points

### Trade #603 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 08:00:00
- **FVG 5m**: 19263.66 - 19291.46
- **Entrée**: 19302.68 @ 2025-04-03 08:27:00
- **Stop Loss**: 19254.03
- **Risk**: 48.65 points
- **TP 1RR**: 19351.33 ✅
- **TP 2RR**: 19399.98 ✅
- **TP 3RR**: 19448.63 ✅
- **TP 4RR**: 19497.28 ❌
- **TP 15RR**: 20032.44 ❌
- **PnL**: -48.65 points (-1.0R)
- **MFE**: 155.06 points
- **MAE**: 54.07 points

### Trade #604 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-03 08:30:00
- **FVG 5m**: 19332.77 - 19339.40
- **Entrée**: 19306.76 @ 2025-04-03 09:03:00
- **Stop Loss**: 19349.07
- **Risk**: 42.31 points
- **TP 1RR**: 19264.45 ✅
- **TP 2RR**: 19222.13 ✅
- **TP 3RR**: 19179.82 ✅
- **TP 4RR**: 19137.51 ✅
- **TP 15RR**: 18672.06 ❌
- **PnL**: -42.31 points (-1.0R)
- **MFE**: 210.40 points
- **MAE**: 49.73 points

### Trade #605 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 08:30:00
- **FVG 5m**: 19163.95 - 19173.13
- **Entrée**: 19176.95 @ 2025-04-03 10:11:00
- **Stop Loss**: 19154.36
- **Risk**: 22.59 points
- **TP 1RR**: 19199.54 ✅
- **TP 2RR**: 19222.13 ✅
- **TP 3RR**: 19244.72 ✅
- **TP 4RR**: 19267.31 ✅
- **TP 15RR**: 19515.78 ❌
- **PnL**: -22.59 points (-1.0R)
- **MFE**: 192.54 points
- **MAE**: 26.78 points

### Trade #606 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 10:15:00
- **FVG 5m**: 19264.43 - 19274.88
- **Entrée**: 19276.67 @ 2025-04-03 10:38:00
- **Stop Loss**: 19254.79
- **Risk**: 21.87 points
- **TP 1RR**: 19298.54 ✅
- **TP 2RR**: 19320.41 ❌
- **TP 3RR**: 19342.29 ❌
- **TP 4RR**: 19364.16 ❌
- **TP 15RR**: 19604.77 ❌
- **PnL**: -21.87 points (-1.0R)
- **MFE**: 38.76 points
- **MAE**: 26.27 points

### Trade #607 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 10:30:00
- **FVG 5m**: 19310.08 - 19314.67
- **Entrée**: 19325.89 @ 2025-04-03 11:13:00
- **Stop Loss**: 19300.42
- **Risk**: 25.47 points
- **TP 1RR**: 19351.35 ✅
- **TP 2RR**: 19376.82 ❌
- **TP 3RR**: 19402.29 ❌
- **TP 4RR**: 19427.75 ❌
- **TP 15RR**: 19707.89 ❌
- **PnL**: -25.47 points (-1.0R)
- **MFE**: 40.80 points
- **MAE**: 27.54 points

### Trade #608 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 14:30:00
- **FVG 5m**: 19023.17 - 19029.80
- **Entrée**: 19046.12 @ 2025-04-03 17:00:00
- **Stop Loss**: 19013.66
- **Risk**: 32.46 points
- **TP 1RR**: 19078.59 ❌
- **TP 2RR**: 19111.05 ❌
- **TP 3RR**: 19143.52 ❌
- **TP 4RR**: 19175.98 ❌
- **TP 15RR**: 19533.08 ❌
- **PnL**: -32.46 points (-1.0R)
- **MFE**: 27.80 points
- **MAE**: 36.72 points

### Trade #609 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-04 00:30:00
- **FVG 5m**: 18989.00 - 18995.37
- **Entrée**: 18999.20 @ 2025-04-04 00:44:00
- **Stop Loss**: 18979.50
- **Risk**: 19.70 points
- **TP 1RR**: 19018.89 ✅
- **TP 2RR**: 19038.59 ✅
- **TP 3RR**: 19058.29 ❌
- **TP 4RR**: 19077.98 ❌
- **TP 15RR**: 19294.63 ❌
- **PnL**: -19.70 points (-1.0R)
- **MFE**: 52.03 points
- **MAE**: 20.66 points

### Trade #610 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-04 09:45:00
- **FVG 5m**: 18265.74 - 18279.26
- **Entrée**: 18330.27 @ 2025-04-04 10:01:00
- **Stop Loss**: 18256.61
- **Risk**: 73.65 points
- **TP 1RR**: 18403.92 ✅
- **TP 2RR**: 18477.57 ✅
- **TP 3RR**: 18551.23 ❌
- **TP 4RR**: 18624.88 ❌
- **TP 15RR**: 19435.08 ❌
- **PnL**: -73.65 points (-1.0R)
- **MFE**: 182.60 points
- **MAE**: 95.89 points

### Trade #611 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-04 12:15:00
- **FVG 5m**: 18111.45 - 18134.41
- **Entrée**: 18149.20 @ 2025-04-04 12:37:00
- **Stop Loss**: 18102.40
- **Risk**: 46.80 points
- **TP 1RR**: 18196.00 ✅
- **TP 2RR**: 18242.80 ✅
- **TP 3RR**: 18289.60 ❌
- **TP 4RR**: 18336.39 ❌
- **TP 15RR**: 18851.19 ❌
- **PnL**: -46.80 points (-1.0R)
- **MFE**: 123.94 points
- **MAE**: 58.91 points

### Trade #612 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-07 02:45:00
- **FVG 5m**: 16968.43 - 17003.62
- **Entrée**: 17006.93 @ 2025-04-07 02:57:00
- **Stop Loss**: 16959.94
- **Risk**: 46.99 points
- **TP 1RR**: 17053.93 ✅
- **TP 2RR**: 17100.92 ✅
- **TP 3RR**: 17147.91 ✅
- **TP 4RR**: 17194.91 ✅
- **TP 15RR**: 17711.83 ✅
- **PnL**: 704.90 points (15.0R)
- **MFE**: 903.05 points
- **MAE**: 19.13 points

### Trade #613 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 03:15:00
- **FVG 5m**: 17127.56 - 17147.96
- **Entrée**: 17120.93 @ 2025-04-07 04:16:00
- **Stop Loss**: 17156.54
- **Risk**: 35.61 points
- **TP 1RR**: 17085.32 ✅
- **TP 2RR**: 17049.72 ❌
- **TP 3RR**: 17014.11 ❌
- **TP 4RR**: 16978.50 ❌
- **TP 15RR**: 16586.83 ❌
- **PnL**: -35.61 points (-1.0R)
- **MFE**: 42.08 points
- **MAE**: 49.48 points

### Trade #614 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 07:00:00
- **FVG 5m**: 17475.16 - 17495.31
- **Entrée**: 17469.30 @ 2025-04-07 08:01:00
- **Stop Loss**: 17504.06
- **Risk**: 34.76 points
- **TP 1RR**: 17434.54 ✅
- **TP 2RR**: 17399.78 ✅
- **TP 3RR**: 17365.02 ✅
- **TP 4RR**: 17330.26 ✅
- **TP 15RR**: 16947.89 ❌
- **PnL**: -34.76 points (-1.0R)
- **MFE**: 460.58 points
- **MAE**: 57.64 points

### Trade #615 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 08:45:00
- **FVG 5m**: 18055.09 - 18270.08
- **Entrée**: 18054.84 @ 2025-04-07 09:22:00
- **Stop Loss**: 18279.21
- **Risk**: 224.38 points
- **TP 1RR**: 17830.46 ✅
- **TP 2RR**: 17606.08 ✅
- **TP 3RR**: 17381.71 ❌
- **TP 4RR**: 17157.33 ❌
- **TP 15RR**: 14689.18 ❌
- **PnL**: -224.38 points (-1.0R)
- **MFE**: 560.29 points
- **MAE**: 259.87 points

### Trade #616 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 09:15:00
- **FVG 5m**: 17748.81 - 17837.04
- **Entrée**: 17632.77 @ 2025-04-07 10:14:00
- **Stop Loss**: 17845.96
- **Risk**: 213.19 points
- **TP 1RR**: 17419.57 ❌
- **TP 2RR**: 17206.38 ❌
- **TP 3RR**: 16993.18 ❌
- **TP 4RR**: 16779.99 ❌
- **TP 15RR**: 14434.85 ❌
- **PnL**: -213.19 points (-1.0R)
- **MFE**: 138.22 points
- **MAE**: 244.06 points

### Trade #617 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 09:15:00
- **FVG 5m**: 17748.81 - 17837.04
- **Entrée**: 17632.77 @ 2025-04-07 10:14:00
- **Stop Loss**: 17845.96
- **Risk**: 213.19 points
- **TP 1RR**: 17419.57 ❌
- **TP 2RR**: 17206.38 ❌
- **TP 3RR**: 16993.18 ❌
- **TP 4RR**: 16779.99 ❌
- **TP 15RR**: 14434.85 ❌
- **PnL**: -213.19 points (-1.0R)
- **MFE**: 138.22 points
- **MAE**: 244.06 points

### Trade #618 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 09:15:00
- **FVG 5m**: 17748.81 - 17837.04
- **Entrée**: 17632.77 @ 2025-04-07 10:14:00
- **Stop Loss**: 17845.96
- **Risk**: 213.19 points
- **TP 1RR**: 17419.57 ❌
- **TP 2RR**: 17206.38 ❌
- **TP 3RR**: 16993.18 ❌
- **TP 4RR**: 16779.99 ❌
- **TP 15RR**: 14434.85 ❌
- **PnL**: -213.19 points (-1.0R)
- **MFE**: 138.22 points
- **MAE**: 244.06 points

### Trade #619 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 18:30:00
- **FVG 5m**: 18070.90 - 18142.82
- **Entrée**: 18069.88 @ 2025-04-07 19:59:00
- **Stop Loss**: 18151.89
- **Risk**: 82.01 points
- **TP 1RR**: 17987.87 ❌
- **TP 2RR**: 17905.87 ❌
- **TP 3RR**: 17823.86 ❌
- **TP 4RR**: 17741.85 ❌
- **TP 15RR**: 16839.75 ❌
- **PnL**: -82.01 points (-1.0R)
- **MFE**: 52.28 points
- **MAE**: 97.68 points

### Trade #620 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 19:15:00
- **FVG 5m**: 18070.90 - 18142.82
- **Entrée**: 18069.88 @ 2025-04-07 19:59:00
- **Stop Loss**: 18151.89
- **Risk**: 82.01 points
- **TP 1RR**: 17987.87 ❌
- **TP 2RR**: 17905.87 ❌
- **TP 3RR**: 17823.86 ❌
- **TP 4RR**: 17741.85 ❌
- **TP 15RR**: 16839.75 ❌
- **PnL**: -82.01 points (-1.0R)
- **MFE**: 52.28 points
- **MAE**: 97.68 points

### Trade #621 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 05:00:00
- **FVG 5m**: 18110.43 - 18119.87
- **Entrée**: 18120.63 @ 2025-04-08 05:34:00
- **Stop Loss**: 18101.38
- **Risk**: 19.26 points
- **TP 1RR**: 18139.89 ✅
- **TP 2RR**: 18159.15 ✅
- **TP 3RR**: 18178.40 ✅
- **TP 4RR**: 18197.66 ✅
- **TP 15RR**: 18409.48 ✅
- **PnL**: 288.84 points (15.0R)
- **MFE**: 295.32 points
- **MAE**: 3.57 points

### Trade #622 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-08 11:30:00
- **FVG 5m**: 18047.95 - 18084.67
- **Entrée**: 18041.83 @ 2025-04-08 11:58:00
- **Stop Loss**: 18093.72
- **Risk**: 51.89 points
- **TP 1RR**: 17989.94 ✅
- **TP 2RR**: 17938.06 ✅
- **TP 3RR**: 17886.17 ✅
- **TP 4RR**: 17834.28 ❌
- **TP 15RR**: 17263.53 ❌
- **PnL**: -51.89 points (-1.0R)
- **MFE**: 201.98 points
- **MAE**: 76.76 points

### Trade #623 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-08 11:30:00
- **FVG 5m**: 18047.95 - 18084.67
- **Entrée**: 18041.83 @ 2025-04-08 11:58:00
- **Stop Loss**: 18093.72
- **Risk**: 51.89 points
- **TP 1RR**: 17989.94 ✅
- **TP 2RR**: 17938.06 ✅
- **TP 3RR**: 17886.17 ✅
- **TP 4RR**: 17834.28 ❌
- **TP 15RR**: 17263.53 ❌
- **PnL**: -51.89 points (-1.0R)
- **MFE**: 201.98 points
- **MAE**: 76.76 points

### Trade #624 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 11:30:00
- **FVG 5m**: 17908.96 - 17955.38
- **Entrée**: 17961.75 @ 2025-04-08 12:38:00
- **Stop Loss**: 17900.01
- **Risk**: 61.74 points
- **TP 1RR**: 18023.50 ✅
- **TP 2RR**: 18085.24 ✅
- **TP 3RR**: 18146.99 ❌
- **TP 4RR**: 18208.73 ❌
- **TP 15RR**: 18887.93 ❌
- **PnL**: -61.74 points (-1.0R)
- **MFE**: 156.84 points
- **MAE**: 68.35 points

### Trade #625 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 12:30:00
- **FVG 5m**: 17415.23 - 17470.57
- **Entrée**: 17473.12 @ 2025-04-08 14:51:00
- **Stop Loss**: 17406.52
- **Risk**: 66.60 points
- **TP 1RR**: 17539.72 ✅
- **TP 2RR**: 17606.32 ✅
- **TP 3RR**: 17672.92 ✅
- **TP 4RR**: 17739.52 ❌
- **TP 15RR**: 18472.10 ❌
- **PnL**: -66.60 points (-1.0R)
- **MFE**: 206.32 points
- **MAE**: 70.13 points

### Trade #626 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 12:30:00
- **FVG 5m**: 17415.23 - 17470.57
- **Entrée**: 17473.12 @ 2025-04-08 14:51:00
- **Stop Loss**: 17406.52
- **Risk**: 66.60 points
- **TP 1RR**: 17539.72 ✅
- **TP 2RR**: 17606.32 ✅
- **TP 3RR**: 17672.92 ✅
- **TP 4RR**: 17739.52 ❌
- **TP 15RR**: 18472.10 ❌
- **PnL**: -66.60 points (-1.0R)
- **MFE**: 206.32 points
- **MAE**: 70.13 points

### Trade #627 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 14:15:00
- **FVG 5m**: 17415.23 - 17470.57
- **Entrée**: 17473.12 @ 2025-04-08 14:51:00
- **Stop Loss**: 17406.52
- **Risk**: 66.60 points
- **TP 1RR**: 17539.72 ✅
- **TP 2RR**: 17606.32 ✅
- **TP 3RR**: 17672.92 ✅
- **TP 4RR**: 17739.52 ❌
- **TP 15RR**: 18472.10 ❌
- **PnL**: -66.60 points (-1.0R)
- **MFE**: 206.32 points
- **MAE**: 70.13 points

### Trade #628 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 18:45:00
- **FVG 5m**: 17256.09 - 17281.60
- **Entrée**: 17284.91 @ 2025-04-08 20:34:00
- **Stop Loss**: 17247.47
- **Risk**: 37.45 points
- **TP 1RR**: 17322.36 ✅
- **TP 2RR**: 17359.80 ✅
- **TP 3RR**: 17397.25 ✅
- **TP 4RR**: 17434.70 ✅
- **TP 15RR**: 17846.60 ❌
- **PnL**: -37.45 points (-1.0R)
- **MFE**: 268.54 points
- **MAE**: 42.08 points

### Trade #629 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 00:15:00
- **FVG 5m**: 17151.53 - 17165.56
- **Entrée**: 17168.11 @ 2025-04-09 00:49:00
- **Stop Loss**: 17142.96
- **Risk**: 25.15 points
- **TP 1RR**: 17193.26 ✅
- **TP 2RR**: 17218.42 ✅
- **TP 3RR**: 17243.57 ✅
- **TP 4RR**: 17268.72 ✅
- **TP 15RR**: 17545.40 ✅
- **PnL**: 377.29 points (15.0R)
- **MFE**: 583.50 points
- **MAE**: 2.55 points

### Trade #630 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 05:15:00
- **FVG 5m**: 17597.57 - 17625.63
- **Entrée**: 17594.77 @ 2025-04-09 05:59:00
- **Stop Loss**: 17634.44
- **Risk**: 39.67 points
- **TP 1RR**: 17555.10 ✅
- **TP 2RR**: 17515.43 ✅
- **TP 3RR**: 17475.76 ✅
- **TP 4RR**: 17436.09 ✅
- **TP 15RR**: 16999.70 ❌
- **PnL**: -39.67 points (-1.0R)
- **MFE**: 388.15 points
- **MAE**: 57.38 points

### Trade #631 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 07:45:00
- **FVG 5m**: 17565.44 - 17579.47
- **Entrée**: 17657.76 @ 2025-04-09 08:31:00
- **Stop Loss**: 17556.66
- **Risk**: 101.10 points
- **TP 1RR**: 17758.86 ✅
- **TP 2RR**: 17859.97 ✅
- **TP 3RR**: 17961.07 ❌
- **TP 4RR**: 18062.17 ❌
- **TP 15RR**: 19174.29 ❌
- **PnL**: -101.10 points (-1.0R)
- **MFE**: 293.54 points
- **MAE**: 105.84 points

### Trade #632 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 08:30:00
- **FVG 5m**: 17741.66 - 17747.28
- **Entrée**: 17725.34 @ 2025-04-09 09:49:00
- **Stop Loss**: 17756.15
- **Risk**: 30.81 points
- **TP 1RR**: 17694.54 ✅
- **TP 2RR**: 17663.73 ✅
- **TP 3RR**: 17632.93 ✅
- **TP 4RR**: 17602.12 ✅
- **TP 15RR**: 17263.25 ❌
- **PnL**: -30.81 points (-1.0R)
- **MFE**: 173.42 points
- **MAE**: 51.26 points

### Trade #633 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 08:30:00
- **FVG 5m**: 17741.66 - 17747.28
- **Entrée**: 17725.34 @ 2025-04-09 09:49:00
- **Stop Loss**: 17756.15
- **Risk**: 30.81 points
- **TP 1RR**: 17694.54 ✅
- **TP 2RR**: 17663.73 ✅
- **TP 3RR**: 17632.93 ✅
- **TP 4RR**: 17602.12 ✅
- **TP 15RR**: 17263.25 ❌
- **PnL**: -30.81 points (-1.0R)
- **MFE**: 173.42 points
- **MAE**: 51.26 points

### Trade #634 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 08:45:00
- **FVG 5m**: 17660.31 - 17676.89
- **Entrée**: 17716.67 @ 2025-04-09 10:06:00
- **Stop Loss**: 17651.48
- **Risk**: 65.19 points
- **TP 1RR**: 17781.86 ✅
- **TP 2RR**: 17847.05 ❌
- **TP 3RR**: 17912.24 ❌
- **TP 4RR**: 17977.44 ❌
- **TP 15RR**: 18694.54 ❌
- **PnL**: -65.19 points (-1.0R)
- **MFE**: 96.40 points
- **MAE**: 90.28 points

### Trade #635 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 12:15:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19299.36 @ 2025-04-09 13:42:00
- **Stop Loss**: 19352.39
- **Risk**: 53.03 points
- **TP 1RR**: 19246.34 ✅
- **TP 2RR**: 19193.31 ✅
- **TP 3RR**: 19140.29 ❌
- **TP 4RR**: 19087.26 ❌
- **TP 15RR**: 18503.98 ❌
- **PnL**: -53.03 points (-1.0R)
- **MFE**: 118.84 points
- **MAE**: 67.33 points

### Trade #636 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 12:15:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19299.36 @ 2025-04-09 13:42:00
- **Stop Loss**: 19352.39
- **Risk**: 53.03 points
- **TP 1RR**: 19246.34 ✅
- **TP 2RR**: 19193.31 ✅
- **TP 3RR**: 19140.29 ❌
- **TP 4RR**: 19087.26 ❌
- **TP 15RR**: 18503.98 ❌
- **PnL**: -53.03 points (-1.0R)
- **MFE**: 118.84 points
- **MAE**: 67.33 points

### Trade #637 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 12:15:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19299.36 @ 2025-04-09 13:42:00
- **Stop Loss**: 19352.39
- **Risk**: 53.03 points
- **TP 1RR**: 19246.34 ✅
- **TP 2RR**: 19193.31 ✅
- **TP 3RR**: 19140.29 ❌
- **TP 4RR**: 19087.26 ❌
- **TP 15RR**: 18503.98 ❌
- **PnL**: -53.03 points (-1.0R)
- **MFE**: 118.84 points
- **MAE**: 67.33 points

### Trade #638 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 12:30:00
- **FVG 5m**: 19124.93 - 19231.53
- **Entrée**: 19243.77 @ 2025-04-09 12:58:00
- **Stop Loss**: 19115.36
- **Risk**: 128.40 points
- **TP 1RR**: 19372.17 ✅
- **TP 2RR**: 19500.58 ❌
- **TP 3RR**: 19628.98 ❌
- **TP 4RR**: 19757.39 ❌
- **TP 15RR**: 21169.84 ❌
- **PnL**: -128.40 points (-1.0R)
- **MFE**: 252.73 points
- **MAE**: 148.17 points

### Trade #639 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 13:00:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19299.36 @ 2025-04-09 13:42:00
- **Stop Loss**: 19352.39
- **Risk**: 53.03 points
- **TP 1RR**: 19246.34 ✅
- **TP 2RR**: 19193.31 ✅
- **TP 3RR**: 19140.29 ❌
- **TP 4RR**: 19087.26 ❌
- **TP 15RR**: 18503.98 ❌
- **PnL**: -53.03 points (-1.0R)
- **MFE**: 118.84 points
- **MAE**: 67.33 points

### Trade #640 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 13:15:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19299.36 @ 2025-04-09 13:42:00
- **Stop Loss**: 19352.39
- **Risk**: 53.03 points
- **TP 1RR**: 19246.34 ✅
- **TP 2RR**: 19193.31 ✅
- **TP 3RR**: 19140.29 ❌
- **TP 4RR**: 19087.26 ❌
- **TP 15RR**: 18503.98 ❌
- **PnL**: -53.03 points (-1.0R)
- **MFE**: 118.84 points
- **MAE**: 67.33 points

### Trade #641 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 14:15:00
- **FVG 5m**: 19664.82 - 19719.65
- **Entrée**: 19654.36 @ 2025-04-09 17:02:00
- **Stop Loss**: 19729.51
- **Risk**: 75.15 points
- **TP 1RR**: 19579.21 ❌
- **TP 2RR**: 19504.07 ❌
- **TP 3RR**: 19428.92 ❌
- **TP 4RR**: 19353.78 ❌
- **TP 15RR**: 18527.16 ❌
- **PnL**: -75.15 points (-1.0R)
- **MFE**: 25.25 points
- **MAE**: 93.85 points

### Trade #642 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 14:45:00
- **FVG 5m**: 19717.61 - 19719.65
- **Entrée**: 19722.71 @ 2025-04-09 15:53:00
- **Stop Loss**: 19707.75
- **Risk**: 14.96 points
- **TP 1RR**: 19737.67 ✅
- **TP 2RR**: 19752.63 ❌
- **TP 3RR**: 19767.59 ❌
- **TP 4RR**: 19782.55 ❌
- **TP 15RR**: 19947.10 ❌
- **PnL**: -14.96 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 69.11 points

### Trade #643 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 14:45:00
- **FVG 5m**: 19717.61 - 19719.65
- **Entrée**: 19722.71 @ 2025-04-09 15:53:00
- **Stop Loss**: 19707.75
- **Risk**: 14.96 points
- **TP 1RR**: 19737.67 ✅
- **TP 2RR**: 19752.63 ❌
- **TP 3RR**: 19767.59 ❌
- **TP 4RR**: 19782.55 ❌
- **TP 15RR**: 19947.10 ❌
- **PnL**: -14.96 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 69.11 points

### Trade #644 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 15:45:00
- **FVG 5m**: 19664.82 - 19697.72
- **Entrée**: 19702.82 @ 2025-04-09 17:13:00
- **Stop Loss**: 19654.98
- **Risk**: 47.83 points
- **TP 1RR**: 19750.65 ✅
- **TP 2RR**: 19798.48 ❌
- **TP 3RR**: 19846.31 ❌
- **TP 4RR**: 19894.14 ❌
- **TP 15RR**: 20420.29 ❌
- **PnL**: -47.83 points (-1.0R)
- **MFE**: 70.39 points
- **MAE**: 55.34 points

### Trade #645 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-10 10:45:00
- **FVG 5m**: 18474.10 - 18536.58
- **Entrée**: 18454.21 @ 2025-04-10 11:18:00
- **Stop Loss**: 18545.85
- **Risk**: 91.64 points
- **TP 1RR**: 18362.57 ✅
- **TP 2RR**: 18270.92 ❌
- **TP 3RR**: 18179.28 ❌
- **TP 4RR**: 18087.64 ❌
- **TP 15RR**: 17079.58 ❌
- **PnL**: -91.64 points (-1.0R)
- **MFE**: 174.95 points
- **MAE**: 103.80 points

### Trade #646 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-10 10:45:00
- **FVG 5m**: 18474.10 - 18536.58
- **Entrée**: 18454.21 @ 2025-04-10 11:18:00
- **Stop Loss**: 18545.85
- **Risk**: 91.64 points
- **TP 1RR**: 18362.57 ✅
- **TP 2RR**: 18270.92 ❌
- **TP 3RR**: 18179.28 ❌
- **TP 4RR**: 18087.64 ❌
- **TP 15RR**: 17079.58 ❌
- **PnL**: -91.64 points (-1.0R)
- **MFE**: 174.95 points
- **MAE**: 103.80 points

### Trade #647 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-10 20:00:00
- **FVG 5m**: 18602.12 - 18621.76
- **Entrée**: 18637.57 @ 2025-04-10 20:11:00
- **Stop Loss**: 18592.82
- **Risk**: 44.75 points
- **TP 1RR**: 18682.32 ✅
- **TP 2RR**: 18727.07 ✅
- **TP 3RR**: 18771.82 ✅
- **TP 4RR**: 18816.57 ✅
- **TP 15RR**: 19308.82 ✅
- **PnL**: 671.25 points (15.0R)
- **MFE**: 999.45 points
- **MAE**: 26.01 points

### Trade #648 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-11 02:00:00
- **FVG 5m**: 18952.78 - 18973.44
- **Entrée**: 18947.43 @ 2025-04-11 02:58:00
- **Stop Loss**: 18982.93
- **Risk**: 35.50 points
- **TP 1RR**: 18911.93 ✅
- **TP 2RR**: 18876.43 ✅
- **TP 3RR**: 18840.93 ✅
- **TP 4RR**: 18805.43 ❌
- **TP 15RR**: 18414.94 ❌
- **PnL**: -35.50 points (-1.0R)
- **MFE**: 120.12 points
- **MAE**: 42.33 points

### Trade #649 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-11 02:15:00
- **FVG 5m**: 18952.78 - 18973.44
- **Entrée**: 18947.43 @ 2025-04-11 02:58:00
- **Stop Loss**: 18982.93
- **Risk**: 35.50 points
- **TP 1RR**: 18911.93 ✅
- **TP 2RR**: 18876.43 ✅
- **TP 3RR**: 18840.93 ✅
- **TP 4RR**: 18805.43 ❌
- **TP 15RR**: 18414.94 ❌
- **PnL**: -35.50 points (-1.0R)
- **MFE**: 120.12 points
- **MAE**: 42.33 points

### Trade #650 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-11 04:15:00
- **FVG 5m**: 18829.35 - 18835.22
- **Entrée**: 18839.04 @ 2025-04-11 04:34:00
- **Stop Loss**: 18819.94
- **Risk**: 19.11 points
- **TP 1RR**: 18858.15 ✅
- **TP 2RR**: 18877.25 ✅
- **TP 3RR**: 18896.36 ✅
- **TP 4RR**: 18915.47 ✅
- **TP 15RR**: 19125.63 ❌
- **PnL**: -19.11 points (-1.0R)
- **MFE**: 239.72 points
- **MAE**: 41.06 points

### Trade #651 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-11 09:30:00
- **FVG 5m**: 18846.69 - 18863.78
- **Entrée**: 18867.61 @ 2025-04-11 09:44:00
- **Stop Loss**: 18837.27
- **Risk**: 30.34 points
- **TP 1RR**: 18897.94 ✅
- **TP 2RR**: 18928.28 ❌
- **TP 3RR**: 18958.61 ❌
- **TP 4RR**: 18988.95 ❌
- **TP 15RR**: 19322.64 ❌
- **PnL**: -30.34 points (-1.0R)
- **MFE**: 50.50 points
- **MAE**: 41.57 points

### Trade #652 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-13 17:00:00
- **FVG 5m**: 19416.17 - 19435.80
- **Entrée**: 19395.76 @ 2025-04-13 17:17:00
- **Stop Loss**: 19445.52
- **Risk**: 49.76 points
- **TP 1RR**: 19346.01 ✅
- **TP 2RR**: 19296.25 ❌
- **TP 3RR**: 19246.49 ❌
- **TP 4RR**: 19196.74 ❌
- **TP 15RR**: 18649.41 ❌
- **PnL**: -49.76 points (-1.0R)
- **MFE**: 83.65 points
- **MAE**: 54.07 points

### Trade #653 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-13 17:15:00
- **FVG 5m**: 19400.87 - 19408.01
- **Entrée**: 19396.78 @ 2025-04-13 18:31:00
- **Stop Loss**: 19417.71
- **Risk**: 20.93 points
- **TP 1RR**: 19375.86 ✅
- **TP 2RR**: 19354.93 ❌
- **TP 3RR**: 19334.01 ❌
- **TP 4RR**: 19313.08 ❌
- **TP 15RR**: 19082.91 ❌
- **PnL**: -20.93 points (-1.0R)
- **MFE**: 30.09 points
- **MAE**: 24.48 points

### Trade #654 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-13 17:15:00
- **FVG 5m**: 19400.87 - 19408.01
- **Entrée**: 19396.78 @ 2025-04-13 18:31:00
- **Stop Loss**: 19417.71
- **Risk**: 20.93 points
- **TP 1RR**: 19375.86 ✅
- **TP 2RR**: 19354.93 ❌
- **TP 3RR**: 19334.01 ❌
- **TP 4RR**: 19313.08 ❌
- **TP 15RR**: 19082.91 ❌
- **PnL**: -20.93 points (-1.0R)
- **MFE**: 30.09 points
- **MAE**: 24.48 points

### Trade #655 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-13 17:30:00
- **FVG 5m**: 19392.45 - 19395.25
- **Entrée**: 19404.95 @ 2025-04-13 18:11:00
- **Stop Loss**: 19382.75
- **Risk**: 22.19 points
- **TP 1RR**: 19427.14 ✅
- **TP 2RR**: 19449.33 ❌
- **TP 3RR**: 19471.52 ❌
- **TP 4RR**: 19493.72 ❌
- **TP 15RR**: 19737.83 ❌
- **PnL**: -22.19 points (-1.0R)
- **MFE**: 31.37 points
- **MAE**: 27.29 points

### Trade #656 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-14 04:15:00
- **FVG 5m**: 19514.86 - 19522.00
- **Entrée**: 19512.31 @ 2025-04-14 06:41:00
- **Stop Loss**: 19531.76
- **Risk**: 19.45 points
- **TP 1RR**: 19492.86 ✅
- **TP 2RR**: 19473.41 ✅
- **TP 3RR**: 19453.96 ✅
- **TP 4RR**: 19434.50 ❌
- **TP 15RR**: 19220.53 ❌
- **PnL**: -19.45 points (-1.0R)
- **MFE**: 66.05 points
- **MAE**: 20.66 points

### Trade #657 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 04:45:00
- **FVG 5m**: 19450.60 - 19455.95
- **Entrée**: 19463.35 @ 2025-04-14 05:27:00
- **Stop Loss**: 19440.87
- **Risk**: 22.48 points
- **TP 1RR**: 19485.82 ✅
- **TP 2RR**: 19508.30 ✅
- **TP 3RR**: 19530.78 ✅
- **TP 4RR**: 19553.25 ✅
- **TP 15RR**: 19800.50 ❌
- **PnL**: -22.48 points (-1.0R)
- **MFE**: 179.79 points
- **MAE**: 52.54 points

### Trade #658 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-14 07:30:00
- **FVG 5m**: 19579.64 - 19612.28
- **Entrée**: 19569.18 @ 2025-04-14 08:33:00
- **Stop Loss**: 19622.09
- **Risk**: 52.91 points
- **TP 1RR**: 19516.28 ✅
- **TP 2RR**: 19463.37 ✅
- **TP 3RR**: 19410.47 ✅
- **TP 4RR**: 19357.56 ✅
- **TP 15RR**: 18775.60 ✅
- **PnL**: 793.58 points (15.0R)
- **MFE**: 803.08 points
- **MAE**: 28.05 points

### Trade #659 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 08:30:00
- **FVG 5m**: 19485.02 - 19488.85
- **Entrée**: 19519.20 @ 2025-04-14 09:03:00
- **Stop Loss**: 19475.28
- **Risk**: 43.92 points
- **TP 1RR**: 19563.11 ❌
- **TP 2RR**: 19607.03 ❌
- **TP 3RR**: 19650.95 ❌
- **TP 4RR**: 19694.86 ❌
- **TP 15RR**: 20177.94 ❌
- **PnL**: -43.92 points (-1.0R)
- **MFE**: 42.33 points
- **MAE**: 60.19 points

### Trade #660 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 09:00:00
- **FVG 5m**: 19493.69 - 19498.29
- **Entrée**: 19510.53 @ 2025-04-14 09:26:00
- **Stop Loss**: 19483.95
- **Risk**: 26.58 points
- **TP 1RR**: 19537.11 ✅
- **TP 2RR**: 19563.68 ✅
- **TP 3RR**: 19590.26 ❌
- **TP 4RR**: 19616.84 ❌
- **TP 15RR**: 19909.21 ❌
- **PnL**: -26.58 points (-1.0R)
- **MFE**: 68.35 points
- **MAE**: 40.80 points

### Trade #661 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 13:00:00
- **FVG 5m**: 19354.20 - 19363.89
- **Entrée**: 19376.38 @ 2025-04-14 13:26:00
- **Stop Loss**: 19344.52
- **Risk**: 31.86 points
- **TP 1RR**: 19408.25 ✅
- **TP 2RR**: 19440.11 ✅
- **TP 3RR**: 19471.98 ✅
- **TP 4RR**: 19503.84 ❌
- **TP 15RR**: 19854.35 ❌
- **PnL**: -31.86 points (-1.0R)
- **MFE**: 102.52 points
- **MAE**: 33.92 points

### Trade #662 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 13:15:00
- **FVG 5m**: 19409.79 - 19421.01
- **Entrée**: 19425.35 @ 2025-04-14 14:04:00
- **Stop Loss**: 19400.09
- **Risk**: 25.26 points
- **TP 1RR**: 19450.61 ✅
- **TP 2RR**: 19475.87 ✅
- **TP 3RR**: 19501.13 ❌
- **TP 4RR**: 19526.39 ❌
- **TP 15RR**: 19804.27 ❌
- **PnL**: -25.26 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 27.29 points

### Trade #663 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 06:30:00
- **FVG 5m**: 19282.28 - 19303.96
- **Entrée**: 19278.45 @ 2025-04-15 06:47:00
- **Stop Loss**: 19313.61
- **Risk**: 35.15 points
- **TP 1RR**: 19243.30 ✅
- **TP 2RR**: 19208.14 ❌
- **TP 3RR**: 19172.99 ❌
- **TP 4RR**: 19137.83 ❌
- **TP 15RR**: 18751.13 ❌
- **PnL**: -35.15 points (-1.0R)
- **MFE**: 64.01 points
- **MAE**: 35.19 points

### Trade #664 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 06:30:00
- **FVG 5m**: 19282.28 - 19303.96
- **Entrée**: 19278.45 @ 2025-04-15 06:47:00
- **Stop Loss**: 19313.61
- **Risk**: 35.15 points
- **TP 1RR**: 19243.30 ✅
- **TP 2RR**: 19208.14 ❌
- **TP 3RR**: 19172.99 ❌
- **TP 4RR**: 19137.83 ❌
- **TP 15RR**: 18751.13 ❌
- **PnL**: -35.15 points (-1.0R)
- **MFE**: 64.01 points
- **MAE**: 35.19 points

### Trade #665 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 07:30:00
- **FVG 5m**: 19309.82 - 19316.96
- **Entrée**: 19327.93 @ 2025-04-15 08:00:00
- **Stop Loss**: 19300.17
- **Risk**: 27.76 points
- **TP 1RR**: 19355.69 ✅
- **TP 2RR**: 19383.45 ✅
- **TP 3RR**: 19411.21 ✅
- **TP 4RR**: 19438.97 ✅
- **TP 15RR**: 19744.35 ❌
- **PnL**: -27.76 points (-1.0R)
- **MFE**: 201.73 points
- **MAE**: 39.27 points

### Trade #666 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 08:45:00
- **FVG 5m**: 19416.68 - 19461.31
- **Entrée**: 19393.98 @ 2025-04-15 09:18:00
- **Stop Loss**: 19471.04
- **Risk**: 77.06 points
- **TP 1RR**: 19316.92 ✅
- **TP 2RR**: 19239.86 ❌
- **TP 3RR**: 19162.81 ❌
- **TP 4RR**: 19085.75 ❌
- **TP 15RR**: 18238.12 ❌
- **PnL**: -77.06 points (-1.0R)
- **MFE**: 89.00 points
- **MAE**: 78.80 points

### Trade #667 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 12:15:00
- **FVG 5m**: 19342.46 - 19344.76
- **Entrée**: 19349.60 @ 2025-04-15 12:39:00
- **Stop Loss**: 19332.79
- **Risk**: 16.81 points
- **TP 1RR**: 19366.42 ✅
- **TP 2RR**: 19383.23 ❌
- **TP 3RR**: 19400.04 ❌
- **TP 4RR**: 19416.85 ❌
- **TP 15RR**: 19601.78 ❌
- **PnL**: -16.81 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 17.60 points

### Trade #668 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 17:15:00
- **FVG 5m**: 19123.91 - 19136.15
- **Entrée**: 19136.91 @ 2025-04-15 17:29:00
- **Stop Loss**: 19114.34
- **Risk**: 22.57 points
- **TP 1RR**: 19159.48 ❌
- **TP 2RR**: 19182.05 ❌
- **TP 3RR**: 19204.62 ❌
- **TP 4RR**: 19227.19 ❌
- **TP 15RR**: 19475.44 ❌
- **PnL**: -22.57 points (-1.0R)
- **MFE**: 17.34 points
- **MAE**: 26.27 points

### Trade #669 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 22:00:00
- **FVG 5m**: 19076.98 - 19083.10
- **Entrée**: 19084.38 @ 2025-04-15 22:11:00
- **Stop Loss**: 19067.44
- **Risk**: 16.93 points
- **TP 1RR**: 19101.31 ❌
- **TP 2RR**: 19118.25 ❌
- **TP 3RR**: 19135.18 ❌
- **TP 4RR**: 19152.11 ❌
- **TP 15RR**: 19338.39 ❌
- **PnL**: -16.93 points (-1.0R)
- **MFE**: 13.52 points
- **MAE**: 23.46 points

### Trade #670 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 03:15:00
- **FVG 5m**: 18926.01 - 19029.80
- **Entrée**: 19110.14 @ 2025-04-16 03:27:00
- **Stop Loss**: 18916.54
- **Risk**: 193.59 points
- **TP 1RR**: 19303.73 ❌
- **TP 2RR**: 19497.32 ❌
- **TP 3RR**: 19690.91 ❌
- **TP 4RR**: 19884.50 ❌
- **TP 15RR**: 22014.01 ❌
- **PnL**: -193.59 points (-1.0R)
- **MFE**: 130.32 points
- **MAE**: 200.45 points

### Trade #671 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 03:30:00
- **FVG 5m**: 19101.46 - 19122.38
- **Entrée**: 19151.70 @ 2025-04-16 03:46:00
- **Stop Loss**: 19091.91
- **Risk**: 59.79 points
- **TP 1RR**: 19211.50 ❌
- **TP 2RR**: 19271.29 ❌
- **TP 3RR**: 19331.08 ❌
- **TP 4RR**: 19390.87 ❌
- **TP 15RR**: 20048.57 ❌
- **PnL**: -59.79 points (-1.0R)
- **MFE**: 9.44 points
- **MAE**: 66.05 points

### Trade #672 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 03:45:00
- **FVG 5m**: 19072.14 - 19076.22
- **Entrée**: 19070.61 @ 2025-04-16 05:34:00
- **Stop Loss**: 19085.75
- **Risk**: 15.15 points
- **TP 1RR**: 19055.46 ✅
- **TP 2RR**: 19040.31 ✅
- **TP 3RR**: 19025.16 ❌
- **TP 4RR**: 19010.01 ❌
- **TP 15RR**: 18843.38 ❌
- **PnL**: -15.15 points (-1.0R)
- **MFE**: 44.37 points
- **MAE**: 17.85 points

### Trade #673 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 07:30:00
- **FVG 5m**: 18940.29 - 18975.23
- **Entrée**: 18985.43 @ 2025-04-16 09:24:00
- **Stop Loss**: 18930.82
- **Risk**: 54.61 points
- **TP 1RR**: 19040.04 ✅
- **TP 2RR**: 19094.65 ✅
- **TP 3RR**: 19149.26 ❌
- **TP 4RR**: 19203.87 ❌
- **TP 15RR**: 19804.57 ❌
- **PnL**: -54.61 points (-1.0R)
- **MFE**: 126.24 points
- **MAE**: 62.48 points

### Trade #674 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 10:15:00
- **FVG 5m**: 19033.88 - 19045.61
- **Entrée**: 19029.55 @ 2025-04-16 10:42:00
- **Stop Loss**: 19055.14
- **Risk**: 25.59 points
- **TP 1RR**: 19003.96 ✅
- **TP 2RR**: 18978.37 ✅
- **TP 3RR**: 18952.78 ✅
- **TP 4RR**: 18927.19 ✅
- **TP 15RR**: 18645.71 ✅
- **PnL**: 383.84 points (15.0R)
- **MFE**: 389.68 points
- **MAE**: 6.38 points

### Trade #675 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 14:45:00
- **FVG 5m**: 18743.66 - 18765.08
- **Entrée**: 18766.62 @ 2025-04-16 17:01:00
- **Stop Loss**: 18734.29
- **Risk**: 32.32 points
- **TP 1RR**: 18798.94 ❌
- **TP 2RR**: 18831.26 ❌
- **TP 3RR**: 18863.59 ❌
- **TP 4RR**: 18895.91 ❌
- **TP 15RR**: 19251.48 ❌
- **PnL**: -32.32 points (-1.0R)
- **MFE**: 30.60 points
- **MAE**: 36.98 points

### Trade #676 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 19:15:00
- **FVG 5m**: 18855.36 - 18860.72
- **Entrée**: 18854.09 @ 2025-04-16 21:33:00
- **Stop Loss**: 18870.15
- **Risk**: 16.06 points
- **TP 1RR**: 18838.03 ✅
- **TP 2RR**: 18821.97 ❌
- **TP 3RR**: 18805.91 ❌
- **TP 4RR**: 18789.84 ❌
- **TP 15RR**: 18613.17 ❌
- **PnL**: -16.06 points (-1.0R)
- **MFE**: 29.33 points
- **MAE**: 19.38 points

### Trade #677 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 21:15:00
- **FVG 5m**: 18855.36 - 18860.72
- **Entrée**: 18854.09 @ 2025-04-16 21:33:00
- **Stop Loss**: 18870.15
- **Risk**: 16.06 points
- **TP 1RR**: 18838.03 ✅
- **TP 2RR**: 18821.97 ❌
- **TP 3RR**: 18805.91 ❌
- **TP 4RR**: 18789.84 ❌
- **TP 15RR**: 18613.17 ❌
- **PnL**: -16.06 points (-1.0R)
- **MFE**: 29.33 points
- **MAE**: 19.38 points

### Trade #678 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 06:15:00
- **FVG 5m**: 18862.50 - 18880.61
- **Entrée**: 18886.99 @ 2025-04-17 06:28:00
- **Stop Loss**: 18853.07
- **Risk**: 33.91 points
- **TP 1RR**: 18920.90 ✅
- **TP 2RR**: 18954.81 ✅
- **TP 3RR**: 18988.73 ✅
- **TP 4RR**: 19022.64 ❌
- **TP 15RR**: 19395.69 ❌
- **PnL**: -33.91 points (-1.0R)
- **MFE**: 111.70 points
- **MAE**: 34.43 points

### Trade #679 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 06:15:00
- **FVG 5m**: 18862.50 - 18880.61
- **Entrée**: 18886.99 @ 2025-04-17 06:28:00
- **Stop Loss**: 18853.07
- **Risk**: 33.91 points
- **TP 1RR**: 18920.90 ✅
- **TP 2RR**: 18954.81 ✅
- **TP 3RR**: 18988.73 ✅
- **TP 4RR**: 19022.64 ❌
- **TP 15RR**: 19395.69 ❌
- **PnL**: -33.91 points (-1.0R)
- **MFE**: 111.70 points
- **MAE**: 34.43 points

### Trade #680 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 06:15:00
- **FVG 5m**: 18862.50 - 18880.61
- **Entrée**: 18886.99 @ 2025-04-17 06:28:00
- **Stop Loss**: 18853.07
- **Risk**: 33.91 points
- **TP 1RR**: 18920.90 ✅
- **TP 2RR**: 18954.81 ✅
- **TP 3RR**: 18988.73 ✅
- **TP 4RR**: 19022.64 ❌
- **TP 15RR**: 19395.69 ❌
- **PnL**: -33.91 points (-1.0R)
- **MFE**: 111.70 points
- **MAE**: 34.43 points

### Trade #681 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 07:00:00
- **FVG 5m**: 18911.72 - 18926.01
- **Entrée**: 18949.72 @ 2025-04-17 07:33:00
- **Stop Loss**: 18902.27
- **Risk**: 47.45 points
- **TP 1RR**: 18997.18 ❌
- **TP 2RR**: 19044.63 ❌
- **TP 3RR**: 19092.09 ❌
- **TP 4RR**: 19139.54 ❌
- **TP 15RR**: 19661.55 ❌
- **PnL**: -47.45 points (-1.0R)
- **MFE**: 15.81 points
- **MAE**: 50.75 points

### Trade #682 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 08:45:00
- **FVG 5m**: 18673.53 - 18703.11
- **Entrée**: 18706.68 @ 2025-04-17 09:41:00
- **Stop Loss**: 18664.19
- **Risk**: 42.49 points
- **TP 1RR**: 18749.17 ❌
- **TP 2RR**: 18791.66 ❌
- **TP 3RR**: 18834.15 ❌
- **TP 4RR**: 18876.64 ❌
- **TP 15RR**: 19344.04 ❌
- **PnL**: -42.49 points (-1.0R)
- **MFE**: 28.56 points
- **MAE**: 42.84 points

### Trade #683 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 09:30:00
- **FVG 5m**: 18673.53 - 18703.11
- **Entrée**: 18706.68 @ 2025-04-17 09:41:00
- **Stop Loss**: 18664.19
- **Risk**: 42.49 points
- **TP 1RR**: 18749.17 ❌
- **TP 2RR**: 18791.66 ❌
- **TP 3RR**: 18834.15 ❌
- **TP 4RR**: 18876.64 ❌
- **TP 15RR**: 19344.04 ❌
- **PnL**: -42.49 points (-1.0R)
- **MFE**: 28.56 points
- **MAE**: 42.84 points

### Trade #684 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-20 17:00:00
- **FVG 5m**: 18665.88 - 18676.85
- **Entrée**: 18683.73 @ 2025-04-20 18:04:00
- **Stop Loss**: 18656.55
- **Risk**: 27.18 points
- **TP 1RR**: 18710.92 ❌
- **TP 2RR**: 18738.10 ❌
- **TP 3RR**: 18765.29 ❌
- **TP 4RR**: 18792.47 ❌
- **TP 15RR**: 19091.50 ❌
- **PnL**: -27.18 points (-1.0R)
- **MFE**: 12.24 points
- **MAE**: 30.86 points

### Trade #685 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-20 22:15:00
- **FVG 5m**: 18592.94 - 18597.02
- **Entrée**: 18597.79 @ 2025-04-20 23:08:00
- **Stop Loss**: 18583.65
- **Risk**: 14.14 points
- **TP 1RR**: 18611.93 ✅
- **TP 2RR**: 18626.07 ❌
- **TP 3RR**: 18640.21 ❌
- **TP 4RR**: 18654.36 ❌
- **TP 15RR**: 18809.92 ❌
- **PnL**: -14.14 points (-1.0R)
- **MFE**: 15.05 points
- **MAE**: 14.79 points

### Trade #686 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-21 07:15:00
- **FVG 5m**: 18475.89 - 18488.38
- **Entrée**: 18492.97 @ 2025-04-21 08:29:00
- **Stop Loss**: 18466.65
- **Risk**: 26.32 points
- **TP 1RR**: 18519.30 ✅
- **TP 2RR**: 18545.62 ❌
- **TP 3RR**: 18571.95 ❌
- **TP 4RR**: 18598.27 ❌
- **TP 15RR**: 18887.84 ❌
- **PnL**: -26.32 points (-1.0R)
- **MFE**: 37.23 points
- **MAE**: 35.70 points

### Trade #687 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-21 09:15:00
- **FVG 5m**: 18165.01 - 18169.09
- **Entrée**: 18180.05 @ 2025-04-21 11:01:00
- **Stop Loss**: 18155.93
- **Risk**: 24.13 points
- **TP 1RR**: 18204.18 ✅
- **TP 2RR**: 18228.31 ✅
- **TP 3RR**: 18252.44 ❌
- **TP 4RR**: 18276.57 ❌
- **TP 15RR**: 18541.99 ❌
- **PnL**: -24.13 points (-1.0R)
- **MFE**: 54.32 points
- **MAE**: 25.50 points

### Trade #688 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-22 01:45:00
- **FVG 5m**: 18443.50 - 18448.09
- **Entrée**: 18451.91 @ 2025-04-22 03:27:00
- **Stop Loss**: 18434.28
- **Risk**: 17.64 points
- **TP 1RR**: 18469.55 ✅
- **TP 2RR**: 18487.19 ✅
- **TP 3RR**: 18504.83 ❌
- **TP 4RR**: 18522.46 ❌
- **TP 15RR**: 18716.48 ❌
- **PnL**: -17.64 points (-1.0R)
- **MFE**: 35.96 points
- **MAE**: 30.35 points

### Trade #689 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-22 01:45:00
- **FVG 5m**: 18443.50 - 18448.09
- **Entrée**: 18451.91 @ 2025-04-22 03:27:00
- **Stop Loss**: 18434.28
- **Risk**: 17.64 points
- **TP 1RR**: 18469.55 ✅
- **TP 2RR**: 18487.19 ✅
- **TP 3RR**: 18504.83 ❌
- **TP 4RR**: 18522.46 ❌
- **TP 15RR**: 18716.48 ❌
- **PnL**: -17.64 points (-1.0R)
- **MFE**: 35.96 points
- **MAE**: 30.35 points

### Trade #690 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-22 08:30:00
- **FVG 5m**: 18519.49 - 18576.37
- **Entrée**: 18577.13 @ 2025-04-22 08:44:00
- **Stop Loss**: 18510.23
- **Risk**: 66.90 points
- **TP 1RR**: 18644.03 ✅
- **TP 2RR**: 18710.92 ✅
- **TP 3RR**: 18777.82 ✅
- **TP 4RR**: 18844.71 ✅
- **TP 15RR**: 19580.57 ✅
- **PnL**: 1003.44 points (15.0R)
- **MFE**: 1012.45 points
- **MAE**: 12.24 points

### Trade #691 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 11:45:00
- **FVG 5m**: 18757.69 - 18813.03
- **Entrée**: 18753.10 @ 2025-04-22 12:11:00
- **Stop Loss**: 18822.44
- **Risk**: 69.34 points
- **TP 1RR**: 18683.76 ✅
- **TP 2RR**: 18614.42 ✅
- **TP 3RR**: 18545.09 ❌
- **TP 4RR**: 18475.75 ❌
- **TP 15RR**: 17713.03 ❌
- **PnL**: -69.34 points (-1.0R)
- **MFE**: 175.71 points
- **MAE**: 358.31 points

### Trade #692 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 12:15:00
- **FVG 5m**: 18622.53 - 18624.57
- **Entrée**: 18616.91 @ 2025-04-22 12:48:00
- **Stop Loss**: 18633.88
- **Risk**: 16.96 points
- **TP 1RR**: 18599.95 ✅
- **TP 2RR**: 18582.99 ✅
- **TP 3RR**: 18566.03 ❌
- **TP 4RR**: 18549.06 ❌
- **TP 15RR**: 18362.47 ❌
- **PnL**: -16.96 points (-1.0R)
- **MFE**: 39.53 points
- **MAE**: 18.87 points

### Trade #693 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 12:45:00
- **FVG 5m**: 18733.97 - 18739.84
- **Entrée**: 18732.44 @ 2025-04-22 14:07:00
- **Stop Loss**: 18749.21
- **Risk**: 16.77 points
- **TP 1RR**: 18715.68 ✅
- **TP 2RR**: 18698.91 ✅
- **TP 3RR**: 18682.14 ✅
- **TP 4RR**: 18665.38 ✅
- **TP 15RR**: 18480.96 ❌
- **PnL**: -16.77 points (-1.0R)
- **MFE**: 125.22 points
- **MAE**: 28.31 points

### Trade #694 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 12:45:00
- **FVG 5m**: 18733.97 - 18739.84
- **Entrée**: 18732.44 @ 2025-04-22 14:07:00
- **Stop Loss**: 18749.21
- **Risk**: 16.77 points
- **TP 1RR**: 18715.68 ✅
- **TP 2RR**: 18698.91 ✅
- **TP 3RR**: 18682.14 ✅
- **TP 4RR**: 18665.38 ✅
- **TP 15RR**: 18480.96 ❌
- **PnL**: -16.77 points (-1.0R)
- **MFE**: 125.22 points
- **MAE**: 28.31 points

### Trade #695 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 17:00:00
- **FVG 5m**: 19142.01 - 19158.08
- **Entrée**: 19134.87 @ 2025-04-22 18:17:00
- **Stop Loss**: 19167.66
- **Risk**: 32.79 points
- **TP 1RR**: 19102.09 ✅
- **TP 2RR**: 19069.30 ✅
- **TP 3RR**: 19036.51 ✅
- **TP 4RR**: 19003.73 ✅
- **TP 15RR**: 18643.08 ❌
- **PnL**: -32.79 points (-1.0R)
- **MFE**: 136.69 points
- **MAE**: 33.41 points

### Trade #696 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 20:30:00
- **FVG 5m**: 19054.28 - 19057.34
- **Entrée**: 19048.42 @ 2025-04-22 22:01:00
- **Stop Loss**: 19066.87
- **Risk**: 18.45 points
- **TP 1RR**: 19029.96 ❌
- **TP 2RR**: 19011.51 ❌
- **TP 3RR**: 18993.06 ❌
- **TP 4RR**: 18974.60 ❌
- **TP 15RR**: 18771.60 ❌
- **PnL**: -18.45 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 21.93 points

### Trade #697 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 03:00:00
- **FVG 5m**: 19174.15 - 19194.80
- **Entrée**: 19200.41 @ 2025-04-23 03:14:00
- **Stop Loss**: 19164.56
- **Risk**: 35.85 points
- **TP 1RR**: 19236.27 ✅
- **TP 2RR**: 19272.12 ✅
- **TP 3RR**: 19307.98 ✅
- **TP 4RR**: 19343.83 ✅
- **TP 15RR**: 19738.24 ❌
- **PnL**: -35.85 points (-1.0R)
- **MFE**: 350.41 points
- **MAE**: 41.06 points

### Trade #698 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 03:30:00
- **FVG 5m**: 19208.58 - 19217.76
- **Entrée**: 19219.54 @ 2025-04-23 04:56:00
- **Stop Loss**: 19198.97
- **Risk**: 20.57 points
- **TP 1RR**: 19240.11 ✅
- **TP 2RR**: 19260.68 ✅
- **TP 3RR**: 19281.25 ✅
- **TP 4RR**: 19301.82 ✅
- **TP 15RR**: 19528.10 ✅
- **PnL**: 308.56 points (15.0R)
- **MFE**: 309.86 points
- **MAE**: 1.79 points

### Trade #699 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 05:15:00
- **FVG 5m**: 19267.74 - 19277.94
- **Entrée**: 19278.20 @ 2025-04-23 05:44:00
- **Stop Loss**: 19258.11
- **Risk**: 20.09 points
- **TP 1RR**: 19298.29 ✅
- **TP 2RR**: 19318.38 ✅
- **TP 3RR**: 19338.47 ❌
- **TP 4RR**: 19358.56 ❌
- **TP 15RR**: 19579.55 ❌
- **PnL**: -20.09 points (-1.0R)
- **MFE**: 47.69 points
- **MAE**: 20.91 points

### Trade #700 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 05:30:00
- **FVG 5m**: 19267.74 - 19277.94
- **Entrée**: 19278.20 @ 2025-04-23 05:44:00
- **Stop Loss**: 19258.11
- **Risk**: 20.09 points
- **TP 1RR**: 19298.29 ✅
- **TP 2RR**: 19318.38 ✅
- **TP 3RR**: 19338.47 ❌
- **TP 4RR**: 19358.56 ❌
- **TP 15RR**: 19579.55 ❌
- **PnL**: -20.09 points (-1.0R)
- **MFE**: 47.69 points
- **MAE**: 20.91 points

### Trade #701 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 06:45:00
- **FVG 5m**: 19301.66 - 19330.48
- **Entrée**: 19278.71 @ 2025-04-23 08:08:00
- **Stop Loss**: 19340.14
- **Risk**: 61.44 points
- **TP 1RR**: 19217.27 ❌
- **TP 2RR**: 19155.84 ❌
- **TP 3RR**: 19094.40 ❌
- **TP 4RR**: 19032.97 ❌
- **TP 15RR**: 18357.17 ❌
- **PnL**: -61.44 points (-1.0R)
- **MFE**: 10.46 points
- **MAE**: 67.33 points

### Trade #702 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 08:00:00
- **FVG 5m**: 19471.51 - 19486.81
- **Entrée**: 19468.70 @ 2025-04-23 09:51:00
- **Stop Loss**: 19496.55
- **Risk**: 27.85 points
- **TP 1RR**: 19440.85 ✅
- **TP 2RR**: 19413.00 ✅
- **TP 3RR**: 19385.15 ✅
- **TP 4RR**: 19357.30 ✅
- **TP 15RR**: 19050.95 ✅
- **PnL**: 417.75 points (15.0R)
- **MFE**: 428.70 points
- **MAE**: 20.15 points

### Trade #703 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 08:30:00
- **FVG 5m**: 19471.51 - 19486.81
- **Entrée**: 19468.70 @ 2025-04-23 09:51:00
- **Stop Loss**: 19496.55
- **Risk**: 27.85 points
- **TP 1RR**: 19440.85 ✅
- **TP 2RR**: 19413.00 ✅
- **TP 3RR**: 19385.15 ✅
- **TP 4RR**: 19357.30 ✅
- **TP 15RR**: 19050.95 ✅
- **PnL**: 417.75 points (15.0R)
- **MFE**: 428.70 points
- **MAE**: 20.15 points

### Trade #704 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 09:30:00
- **FVG 5m**: 19471.51 - 19486.81
- **Entrée**: 19468.70 @ 2025-04-23 09:51:00
- **Stop Loss**: 19496.55
- **Risk**: 27.85 points
- **TP 1RR**: 19440.85 ✅
- **TP 2RR**: 19413.00 ✅
- **TP 3RR**: 19385.15 ✅
- **TP 4RR**: 19357.30 ✅
- **TP 15RR**: 19050.95 ✅
- **PnL**: 417.75 points (15.0R)
- **MFE**: 428.70 points
- **MAE**: 20.15 points

### Trade #705 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 10:15:00
- **FVG 5m**: 19230.51 - 19263.41
- **Entrée**: 19202.45 @ 2025-04-23 10:48:00
- **Stop Loss**: 19273.04
- **Risk**: 70.58 points
- **TP 1RR**: 19131.87 ✅
- **TP 2RR**: 19061.29 ❌
- **TP 3RR**: 18990.71 ❌
- **TP 4RR**: 18920.12 ❌
- **TP 15RR**: 18143.71 ❌
- **PnL**: -70.58 points (-1.0R)
- **MFE**: 78.55 points
- **MAE**: 71.92 points

### Trade #706 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 10:45:00
- **FVG 5m**: 19160.12 - 19202.20
- **Entrée**: 19214.44 @ 2025-04-23 11:29:00
- **Stop Loss**: 19150.54
- **Risk**: 63.90 points
- **TP 1RR**: 19278.34 ✅
- **TP 2RR**: 19342.24 ✅
- **TP 3RR**: 19406.14 ❌
- **TP 4RR**: 19470.04 ❌
- **TP 15RR**: 20172.95 ❌
- **PnL**: -63.90 points (-1.0R)
- **MFE**: 133.12 points
- **MAE**: 67.58 points

### Trade #707 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 10:45:00
- **FVG 5m**: 19160.12 - 19202.20
- **Entrée**: 19214.44 @ 2025-04-23 11:29:00
- **Stop Loss**: 19150.54
- **Risk**: 63.90 points
- **TP 1RR**: 19278.34 ✅
- **TP 2RR**: 19342.24 ✅
- **TP 3RR**: 19406.14 ❌
- **TP 4RR**: 19470.04 ❌
- **TP 15RR**: 20172.95 ❌
- **PnL**: -63.90 points (-1.0R)
- **MFE**: 133.12 points
- **MAE**: 67.58 points

### Trade #708 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 14:15:00
- **FVG 5m**: 19249.89 - 19251.93
- **Entrée**: 19244.79 @ 2025-04-23 15:41:00
- **Stop Loss**: 19261.56
- **Risk**: 16.77 points
- **TP 1RR**: 19228.02 ✅
- **TP 2RR**: 19211.26 ✅
- **TP 3RR**: 19194.49 ✅
- **TP 4RR**: 19177.72 ✅
- **TP 15RR**: 18993.29 ✅
- **PnL**: 251.50 points (15.0R)
- **MFE**: 262.93 points
- **MAE**: 10.46 points

### Trade #709 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 14:30:00
- **FVG 5m**: 19157.32 - 19162.16
- **Entrée**: 19164.20 @ 2025-04-23 14:49:00
- **Stop Loss**: 19147.74
- **Risk**: 16.46 points
- **TP 1RR**: 19180.67 ✅
- **TP 2RR**: 19197.13 ✅
- **TP 3RR**: 19213.59 ✅
- **TP 4RR**: 19230.06 ✅
- **TP 15RR**: 19411.17 ❌
- **PnL**: -16.46 points (-1.0R)
- **MFE**: 143.32 points
- **MAE**: 22.44 points

### Trade #710 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 23:30:00
- **FVG 5m**: 19120.08 - 19137.17
- **Entrée**: 19145.07 @ 2025-04-23 23:42:00
- **Stop Loss**: 19110.52
- **Risk**: 34.55 points
- **TP 1RR**: 19179.63 ❌
- **TP 2RR**: 19214.18 ❌
- **TP 3RR**: 19248.73 ❌
- **TP 4RR**: 19283.28 ❌
- **TP 15RR**: 19663.36 ❌
- **PnL**: -34.55 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 43.35 points

### Trade #711 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 23:30:00
- **FVG 5m**: 19120.08 - 19137.17
- **Entrée**: 19145.07 @ 2025-04-23 23:42:00
- **Stop Loss**: 19110.52
- **Risk**: 34.55 points
- **TP 1RR**: 19179.63 ❌
- **TP 2RR**: 19214.18 ❌
- **TP 3RR**: 19248.73 ❌
- **TP 4RR**: 19283.28 ❌
- **TP 15RR**: 19663.36 ❌
- **PnL**: -34.55 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 43.35 points

### Trade #712 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-24 02:00:00
- **FVG 5m**: 18990.53 - 19004.55
- **Entrée**: 19013.23 @ 2025-04-24 04:00:00
- **Stop Loss**: 18981.03
- **Risk**: 32.19 points
- **TP 1RR**: 19045.42 ✅
- **TP 2RR**: 19077.61 ✅
- **TP 3RR**: 19109.80 ✅
- **TP 4RR**: 19142.00 ✅
- **TP 15RR**: 19496.11 ✅
- **PnL**: 482.89 points (15.0R)
- **MFE**: 483.02 points
- **MAE**: 6.38 points

### Trade #713 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-24 02:00:00
- **FVG 5m**: 18990.53 - 19004.55
- **Entrée**: 19013.23 @ 2025-04-24 04:00:00
- **Stop Loss**: 18981.03
- **Risk**: 32.19 points
- **TP 1RR**: 19045.42 ✅
- **TP 2RR**: 19077.61 ✅
- **TP 3RR**: 19109.80 ✅
- **TP 4RR**: 19142.00 ✅
- **TP 15RR**: 19496.11 ✅
- **PnL**: 482.89 points (15.0R)
- **MFE**: 483.02 points
- **MAE**: 6.38 points

### Trade #714 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-24 03:45:00
- **FVG 5m**: 18990.53 - 19004.55
- **Entrée**: 19013.23 @ 2025-04-24 04:00:00
- **Stop Loss**: 18981.03
- **Risk**: 32.19 points
- **TP 1RR**: 19045.42 ✅
- **TP 2RR**: 19077.61 ✅
- **TP 3RR**: 19109.80 ✅
- **TP 4RR**: 19142.00 ✅
- **TP 15RR**: 19496.11 ✅
- **PnL**: 482.89 points (15.0R)
- **MFE**: 483.02 points
- **MAE**: 6.38 points

### Trade #715 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 06:00:00
- **FVG 5m**: 19133.09 - 19150.17
- **Entrée**: 19127.48 @ 2025-04-24 06:18:00
- **Stop Loss**: 19159.75
- **Risk**: 32.27 points
- **TP 1RR**: 19095.20 ❌
- **TP 2RR**: 19062.93 ❌
- **TP 3RR**: 19030.66 ❌
- **TP 4RR**: 18998.39 ❌
- **TP 15RR**: 18643.39 ❌
- **PnL**: -32.27 points (-1.0R)
- **MFE**: 21.42 points
- **MAE**: 66.56 points

### Trade #716 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 06:00:00
- **FVG 5m**: 19133.09 - 19150.17
- **Entrée**: 19127.48 @ 2025-04-24 06:18:00
- **Stop Loss**: 19159.75
- **Risk**: 32.27 points
- **TP 1RR**: 19095.20 ❌
- **TP 2RR**: 19062.93 ❌
- **TP 3RR**: 19030.66 ❌
- **TP 4RR**: 18998.39 ❌
- **TP 15RR**: 18643.39 ❌
- **PnL**: -32.27 points (-1.0R)
- **MFE**: 21.42 points
- **MAE**: 66.56 points

### Trade #717 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 08:00:00
- **FVG 5m**: 19514.61 - 19526.85
- **Entrée**: 19513.84 @ 2025-04-24 09:43:00
- **Stop Loss**: 19536.61
- **Risk**: 22.77 points
- **TP 1RR**: 19491.07 ✅
- **TP 2RR**: 19468.30 ❌
- **TP 3RR**: 19445.53 ❌
- **TP 4RR**: 19422.76 ❌
- **TP 15RR**: 19172.30 ❌
- **PnL**: -22.77 points (-1.0R)
- **MFE**: 42.84 points
- **MAE**: 31.37 points

### Trade #718 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 09:30:00
- **FVG 5m**: 19514.61 - 19526.85
- **Entrée**: 19513.84 @ 2025-04-24 09:43:00
- **Stop Loss**: 19536.61
- **Risk**: 22.77 points
- **TP 1RR**: 19491.07 ✅
- **TP 2RR**: 19468.30 ❌
- **TP 3RR**: 19445.53 ❌
- **TP 4RR**: 19422.76 ❌
- **TP 15RR**: 19172.30 ❌
- **PnL**: -22.77 points (-1.0R)
- **MFE**: 42.84 points
- **MAE**: 31.37 points

### Trade #719 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 11:30:00
- **FVG 5m**: 19682.67 - 19695.93
- **Entrée**: 19681.14 @ 2025-04-24 13:59:00
- **Stop Loss**: 19705.78
- **Risk**: 24.64 points
- **TP 1RR**: 19656.50 ✅
- **TP 2RR**: 19631.86 ✅
- **TP 3RR**: 19607.22 ❌
- **TP 4RR**: 19582.58 ❌
- **TP 15RR**: 19311.55 ❌
- **PnL**: -24.64 points (-1.0R)
- **MFE**: 73.70 points
- **MAE**: 29.33 points

### Trade #720 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 11:30:00
- **FVG 5m**: 19682.67 - 19695.93
- **Entrée**: 19681.14 @ 2025-04-24 13:59:00
- **Stop Loss**: 19705.78
- **Risk**: 24.64 points
- **TP 1RR**: 19656.50 ✅
- **TP 2RR**: 19631.86 ✅
- **TP 3RR**: 19607.22 ❌
- **TP 4RR**: 19582.58 ❌
- **TP 15RR**: 19311.55 ❌
- **PnL**: -24.64 points (-1.0R)
- **MFE**: 73.70 points
- **MAE**: 29.33 points

### Trade #721 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-24 22:15:00
- **FVG 5m**: 19805.34 - 19810.69
- **Entrée**: 19819.87 @ 2025-04-24 22:34:00
- **Stop Loss**: 19795.43
- **Risk**: 24.44 points
- **TP 1RR**: 19844.31 ✅
- **TP 2RR**: 19868.75 ✅
- **TP 3RR**: 19893.19 ❌
- **TP 4RR**: 19917.63 ❌
- **TP 15RR**: 20186.46 ❌
- **PnL**: -24.44 points (-1.0R)
- **MFE**: 69.62 points
- **MAE**: 28.05 points

### Trade #722 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 23:15:00
- **FVG 5m**: 19820.89 - 19842.57
- **Entrée**: 19810.95 @ 2025-04-24 23:27:00
- **Stop Loss**: 19852.49
- **Risk**: 41.54 points
- **TP 1RR**: 19769.40 ❌
- **TP 2RR**: 19727.86 ❌
- **TP 3RR**: 19686.31 ❌
- **TP 4RR**: 19644.77 ❌
- **TP 15RR**: 19187.78 ❌
- **PnL**: -41.54 points (-1.0R)
- **MFE**: 29.58 points
- **MAE**: 58.91 points

### Trade #723 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-25 04:15:00
- **FVG 5m**: 19770.91 - 19778.81
- **Entrée**: 19780.85 @ 2025-04-25 04:51:00
- **Stop Loss**: 19761.02
- **Risk**: 19.83 points
- **TP 1RR**: 19800.69 ❌
- **TP 2RR**: 19820.52 ❌
- **TP 3RR**: 19840.35 ❌
- **TP 4RR**: 19860.18 ❌
- **TP 15RR**: 20078.33 ❌
- **PnL**: -19.83 points (-1.0R)
- **MFE**: 9.95 points
- **MAE**: 21.42 points

### Trade #724 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-25 04:15:00
- **FVG 5m**: 19770.91 - 19778.81
- **Entrée**: 19780.85 @ 2025-04-25 04:51:00
- **Stop Loss**: 19761.02
- **Risk**: 19.83 points
- **TP 1RR**: 19800.69 ❌
- **TP 2RR**: 19820.52 ❌
- **TP 3RR**: 19840.35 ❌
- **TP 4RR**: 19860.18 ❌
- **TP 15RR**: 20078.33 ❌
- **PnL**: -19.83 points (-1.0R)
- **MFE**: 9.95 points
- **MAE**: 21.42 points

### Trade #725 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-25 15:30:00
- **FVG 5m**: 19917.04 - 19941.27
- **Entrée**: 19896.13 @ 2025-04-27 17:00:00
- **Stop Loss**: 19951.24
- **Risk**: 55.11 points
- **TP 1RR**: 19841.02 ✅
- **TP 2RR**: 19785.91 ✅
- **TP 3RR**: 19730.80 ❌
- **TP 4RR**: 19675.69 ❌
- **TP 15RR**: 19069.47 ❌
- **PnL**: -55.11 points (-1.0R)
- **MFE**: 114.00 points
- **MAE**: 55.34 points

### Trade #726 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-27 20:15:00
- **FVG 5m**: 19822.17 - 19827.01
- **Entrée**: 19807.12 @ 2025-04-27 21:55:00
- **Stop Loss**: 19836.93
- **Risk**: 29.81 points
- **TP 1RR**: 19777.32 ❌
- **TP 2RR**: 19747.51 ❌
- **TP 3RR**: 19717.71 ❌
- **TP 4RR**: 19687.90 ❌
- **TP 15RR**: 19360.04 ❌
- **PnL**: -29.81 points (-1.0R)
- **MFE**: 21.93 points
- **MAE**: 30.60 points

### Trade #727 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 04:45:00
- **FVG 5m**: 19913.21 - 19919.84
- **Entrée**: 19911.17 @ 2025-04-28 04:56:00
- **Stop Loss**: 19929.80
- **Risk**: 18.63 points
- **TP 1RR**: 19892.54 ✅
- **TP 2RR**: 19873.91 ✅
- **TP 3RR**: 19855.28 ❌
- **TP 4RR**: 19836.65 ❌
- **TP 15RR**: 19631.71 ❌
- **PnL**: -18.63 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 19.13 points

### Trade #728 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 08:45:00
- **FVG 5m**: 19897.66 - 19928.26
- **Entrée**: 19882.35 @ 2025-04-28 08:57:00
- **Stop Loss**: 19938.22
- **Risk**: 55.87 points
- **TP 1RR**: 19826.49 ✅
- **TP 2RR**: 19770.62 ✅
- **TP 3RR**: 19714.75 ✅
- **TP 4RR**: 19658.88 ✅
- **TP 15RR**: 19044.32 ❌
- **PnL**: -55.87 points (-1.0R)
- **MFE**: 237.94 points
- **MAE**: 77.02 points

### Trade #729 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 08:45:00
- **FVG 5m**: 19897.66 - 19928.26
- **Entrée**: 19882.35 @ 2025-04-28 08:57:00
- **Stop Loss**: 19938.22
- **Risk**: 55.87 points
- **TP 1RR**: 19826.49 ✅
- **TP 2RR**: 19770.62 ✅
- **TP 3RR**: 19714.75 ✅
- **TP 4RR**: 19658.88 ✅
- **TP 15RR**: 19044.32 ❌
- **PnL**: -55.87 points (-1.0R)
- **MFE**: 237.94 points
- **MAE**: 77.02 points

### Trade #730 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 10:00:00
- **FVG 5m**: 19745.92 - 19788.25
- **Entrée**: 19742.86 @ 2025-04-28 10:24:00
- **Stop Loss**: 19798.14
- **Risk**: 55.29 points
- **TP 1RR**: 19687.57 ✅
- **TP 2RR**: 19632.28 ❌
- **TP 3RR**: 19576.99 ❌
- **TP 4RR**: 19521.70 ❌
- **TP 15RR**: 18913.52 ❌
- **PnL**: -55.29 points (-1.0R)
- **MFE**: 98.44 points
- **MAE**: 65.29 points

### Trade #731 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 10:15:00
- **FVG 5m**: 19711.74 - 19721.18
- **Entrée**: 19705.37 @ 2025-04-28 11:01:00
- **Stop Loss**: 19731.04
- **Risk**: 25.67 points
- **TP 1RR**: 19679.69 ✅
- **TP 2RR**: 19654.02 ❌
- **TP 3RR**: 19628.35 ❌
- **TP 4RR**: 19602.68 ❌
- **TP 15RR**: 19320.28 ❌
- **PnL**: -25.67 points (-1.0R)
- **MFE**: 50.50 points
- **MAE**: 26.27 points

### Trade #732 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:00:00
- **FVG 5m**: 19779.58 - 19785.19
- **Entrée**: 19793.61 @ 2025-04-28 13:24:00
- **Stop Loss**: 19769.69
- **Risk**: 23.92 points
- **TP 1RR**: 19817.52 ✅
- **TP 2RR**: 19841.44 ✅
- **TP 3RR**: 19865.35 ✅
- **TP 4RR**: 19889.27 ✅
- **TP 15RR**: 20152.35 ❌
- **PnL**: -23.92 points (-1.0R)
- **MFE**: 232.07 points
- **MAE**: 26.01 points

### Trade #733 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:15:00
- **FVG 5m**: 19803.81 - 19806.10
- **Entrée**: 19808.40 @ 2025-04-28 13:39:00
- **Stop Loss**: 19793.90
- **Risk**: 14.49 points
- **TP 1RR**: 19822.89 ✅
- **TP 2RR**: 19837.38 ✅
- **TP 3RR**: 19851.87 ✅
- **TP 4RR**: 19866.37 ✅
- **TP 15RR**: 20025.78 ❌
- **PnL**: -14.49 points (-1.0R)
- **MFE**: 217.28 points
- **MAE**: 15.56 points

### Trade #734 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:15:00
- **FVG 5m**: 19803.81 - 19806.10
- **Entrée**: 19808.40 @ 2025-04-28 13:39:00
- **Stop Loss**: 19793.90
- **Risk**: 14.49 points
- **TP 1RR**: 19822.89 ✅
- **TP 2RR**: 19837.38 ✅
- **TP 3RR**: 19851.87 ✅
- **TP 4RR**: 19866.37 ✅
- **TP 15RR**: 20025.78 ❌
- **PnL**: -14.49 points (-1.0R)
- **MFE**: 217.28 points
- **MAE**: 15.56 points

### Trade #735 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:15:00
- **FVG 5m**: 19803.81 - 19806.10
- **Entrée**: 19808.40 @ 2025-04-28 13:39:00
- **Stop Loss**: 19793.90
- **Risk**: 14.49 points
- **TP 1RR**: 19822.89 ✅
- **TP 2RR**: 19837.38 ✅
- **TP 3RR**: 19851.87 ✅
- **TP 4RR**: 19866.37 ✅
- **TP 15RR**: 20025.78 ❌
- **PnL**: -14.49 points (-1.0R)
- **MFE**: 217.28 points
- **MAE**: 15.56 points

### Trade #736 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 21:00:00
- **FVG 5m**: 19959.37 - 19966.00
- **Entrée**: 19966.26 @ 2025-04-28 23:24:00
- **Stop Loss**: 19949.39
- **Risk**: 16.87 points
- **TP 1RR**: 19983.12 ✅
- **TP 2RR**: 19999.99 ❌
- **TP 3RR**: 20016.85 ❌
- **TP 4RR**: 20033.72 ❌
- **TP 15RR**: 20219.24 ❌
- **PnL**: -16.87 points (-1.0R)
- **MFE**: 25.25 points
- **MAE**: 17.60 points

### Trade #737 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 21:30:00
- **FVG 5m**: 19971.61 - 20001.45
- **Entrée**: 19964.73 @ 2025-04-28 21:45:00
- **Stop Loss**: 20011.45
- **Risk**: 46.72 points
- **TP 1RR**: 19918.00 ❌
- **TP 2RR**: 19871.28 ❌
- **TP 3RR**: 19824.55 ❌
- **TP 4RR**: 19777.83 ❌
- **TP 15RR**: 19263.86 ❌
- **PnL**: -46.72 points (-1.0R)
- **MFE**: 46.67 points
- **MAE**: 49.48 points

### Trade #738 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 03:00:00
- **FVG 5m**: 19981.82 - 19984.62
- **Entrée**: 19978.24 @ 2025-04-29 03:56:00
- **Stop Loss**: 19994.61
- **Risk**: 16.37 points
- **TP 1RR**: 19961.88 ✅
- **TP 2RR**: 19945.51 ✅
- **TP 3RR**: 19929.14 ✅
- **TP 4RR**: 19912.77 ✅
- **TP 15RR**: 19732.73 ❌
- **PnL**: -16.37 points (-1.0R)
- **MFE**: 210.65 points
- **MAE**: 17.09 points

### Trade #739 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-29 07:30:00
- **FVG 5m**: 19841.55 - 19860.42
- **Entrée**: 19863.48 @ 2025-04-29 08:44:00
- **Stop Loss**: 19831.63
- **Risk**: 31.85 points
- **TP 1RR**: 19895.34 ✅
- **TP 2RR**: 19927.19 ✅
- **TP 3RR**: 19959.04 ✅
- **TP 4RR**: 19990.89 ✅
- **TP 15RR**: 20341.28 ❌
- **PnL**: -31.85 points (-1.0R)
- **MFE**: 220.85 points
- **MAE**: 47.18 points

### Trade #740 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-29 08:30:00
- **FVG 5m**: 19841.55 - 19860.42
- **Entrée**: 19863.48 @ 2025-04-29 08:44:00
- **Stop Loss**: 19831.63
- **Risk**: 31.85 points
- **TP 1RR**: 19895.34 ✅
- **TP 2RR**: 19927.19 ✅
- **TP 3RR**: 19959.04 ✅
- **TP 4RR**: 19990.89 ✅
- **TP 15RR**: 20341.28 ❌
- **PnL**: -31.85 points (-1.0R)
- **MFE**: 220.85 points
- **MAE**: 47.18 points

### Trade #741 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-29 08:30:00
- **FVG 5m**: 19841.55 - 19860.42
- **Entrée**: 19863.48 @ 2025-04-29 08:44:00
- **Stop Loss**: 19831.63
- **Risk**: 31.85 points
- **TP 1RR**: 19895.34 ✅
- **TP 2RR**: 19927.19 ✅
- **TP 3RR**: 19959.04 ✅
- **TP 4RR**: 19990.89 ✅
- **TP 15RR**: 20341.28 ❌
- **PnL**: -31.85 points (-1.0R)
- **MFE**: 220.85 points
- **MAE**: 47.18 points

### Trade #742 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20007.06 - 20024.40
- **Entrée**: 19976.46 @ 2025-04-29 15:30:00
- **Stop Loss**: 20034.42
- **Risk**: 57.96 points
- **TP 1RR**: 19918.50 ✅
- **TP 2RR**: 19860.55 ✅
- **TP 3RR**: 19802.59 ✅
- **TP 4RR**: 19744.63 ✅
- **TP 15RR**: 19107.10 ❌
- **PnL**: -57.96 points (-1.0R)
- **MFE**: 488.63 points
- **MAE**: 66.82 points

### Trade #743 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20007.06 - 20024.40
- **Entrée**: 19976.46 @ 2025-04-29 15:30:00
- **Stop Loss**: 20034.42
- **Risk**: 57.96 points
- **TP 1RR**: 19918.50 ✅
- **TP 2RR**: 19860.55 ✅
- **TP 3RR**: 19802.59 ✅
- **TP 4RR**: 19744.63 ✅
- **TP 15RR**: 19107.10 ❌
- **PnL**: -57.96 points (-1.0R)
- **MFE**: 488.63 points
- **MAE**: 66.82 points

### Trade #744 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20007.06 - 20024.40
- **Entrée**: 19976.46 @ 2025-04-29 15:30:00
- **Stop Loss**: 20034.42
- **Risk**: 57.96 points
- **TP 1RR**: 19918.50 ✅
- **TP 2RR**: 19860.55 ✅
- **TP 3RR**: 19802.59 ✅
- **TP 4RR**: 19744.63 ✅
- **TP 15RR**: 19107.10 ❌
- **PnL**: -57.96 points (-1.0R)
- **MFE**: 488.63 points
- **MAE**: 66.82 points

### Trade #745 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20007.06 - 20024.40
- **Entrée**: 19976.46 @ 2025-04-29 15:30:00
- **Stop Loss**: 20034.42
- **Risk**: 57.96 points
- **TP 1RR**: 19918.50 ✅
- **TP 2RR**: 19860.55 ✅
- **TP 3RR**: 19802.59 ✅
- **TP 4RR**: 19744.63 ✅
- **TP 15RR**: 19107.10 ❌
- **PnL**: -57.96 points (-1.0R)
- **MFE**: 488.63 points
- **MAE**: 66.82 points

### Trade #746 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 01:00:00
- **FVG 5m**: 19979.77 - 19985.39
- **Entrée**: 19986.15 @ 2025-04-30 03:09:00
- **Stop Loss**: 19969.78
- **Risk**: 16.37 points
- **TP 1RR**: 20002.52 ✅
- **TP 2RR**: 20018.88 ❌
- **TP 3RR**: 20035.25 ❌
- **TP 4RR**: 20051.61 ❌
- **TP 15RR**: 20231.63 ❌
- **PnL**: -16.37 points (-1.0R)
- **MFE**: 31.11 points
- **MAE**: 16.58 points

### Trade #747 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 08:15:00
- **FVG 5m**: 19578.87 - 19583.21
- **Entrée**: 19586.52 @ 2025-04-30 09:08:00
- **Stop Loss**: 19569.08
- **Risk**: 17.44 points
- **TP 1RR**: 19603.96 ✅
- **TP 2RR**: 19621.40 ✅
- **TP 3RR**: 19638.85 ✅
- **TP 4RR**: 19656.29 ✅
- **TP 15RR**: 19848.13 ✅
- **PnL**: 261.60 points (15.0R)
- **MFE**: 269.05 points
- **MAE**: 3.32 points

### Trade #748 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 09:00:00
- **FVG 5m**: 19611.52 - 19621.72
- **Entrée**: 19627.84 @ 2025-04-30 09:13:00
- **Stop Loss**: 19601.71
- **Risk**: 26.13 points
- **TP 1RR**: 19653.97 ✅
- **TP 2RR**: 19680.09 ✅
- **TP 3RR**: 19706.22 ✅
- **TP 4RR**: 19732.35 ✅
- **TP 15RR**: 20019.75 ✅
- **PnL**: 391.91 points (15.0R)
- **MFE**: 402.18 points
- **MAE**: 6.12 points

### Trade #749 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 09:00:00
- **FVG 5m**: 19611.52 - 19621.72
- **Entrée**: 19627.84 @ 2025-04-30 09:13:00
- **Stop Loss**: 19601.71
- **Risk**: 26.13 points
- **TP 1RR**: 19653.97 ✅
- **TP 2RR**: 19680.09 ✅
- **TP 3RR**: 19706.22 ✅
- **TP 4RR**: 19732.35 ✅
- **TP 15RR**: 20019.75 ✅
- **PnL**: 391.91 points (15.0R)
- **MFE**: 402.18 points
- **MAE**: 6.12 points

### Trade #750 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 09:00:00
- **FVG 5m**: 19611.52 - 19621.72
- **Entrée**: 19627.84 @ 2025-04-30 09:13:00
- **Stop Loss**: 19601.71
- **Risk**: 26.13 points
- **TP 1RR**: 19653.97 ✅
- **TP 2RR**: 19680.09 ✅
- **TP 3RR**: 19706.22 ✅
- **TP 4RR**: 19732.35 ✅
- **TP 15RR**: 20019.75 ✅
- **PnL**: 391.91 points (15.0R)
- **MFE**: 402.18 points
- **MAE**: 6.12 points

### Trade #751 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 10:00:00
- **FVG 5m**: 19779.83 - 19804.32
- **Entrée**: 19805.85 @ 2025-04-30 11:37:00
- **Stop Loss**: 19769.94
- **Risk**: 35.90 points
- **TP 1RR**: 19841.75 ✅
- **TP 2RR**: 19877.65 ❌
- **TP 3RR**: 19913.55 ❌
- **TP 4RR**: 19949.46 ❌
- **TP 15RR**: 20344.39 ❌
- **PnL**: -35.90 points (-1.0R)
- **MFE**: 38.25 points
- **MAE**: 69.11 points

### Trade #752 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 12:30:00
- **FVG 5m**: 19875.72 - 19890.52
- **Entrée**: 19919.84 @ 2025-04-30 13:07:00
- **Stop Loss**: 19865.79
- **Risk**: 54.06 points
- **TP 1RR**: 19973.90 ❌
- **TP 2RR**: 20027.96 ❌
- **TP 3RR**: 20082.02 ❌
- **TP 4RR**: 20136.07 ❌
- **TP 15RR**: 20730.70 ❌
- **PnL**: -54.06 points (-1.0R)
- **MFE**: 35.96 points
- **MAE**: 66.05 points

### Trade #753 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 12:30:00
- **FVG 5m**: 19875.72 - 19890.52
- **Entrée**: 19919.84 @ 2025-04-30 13:07:00
- **Stop Loss**: 19865.79
- **Risk**: 54.06 points
- **TP 1RR**: 19973.90 ❌
- **TP 2RR**: 20027.96 ❌
- **TP 3RR**: 20082.02 ❌
- **TP 4RR**: 20136.07 ❌
- **TP 15RR**: 20730.70 ❌
- **PnL**: -54.06 points (-1.0R)
- **MFE**: 35.96 points
- **MAE**: 66.05 points

### Trade #754 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 13:00:00
- **FVG 5m**: 19866.80 - 19878.78
- **Entrée**: 19863.48 @ 2025-04-30 13:36:00
- **Stop Loss**: 19888.72
- **Risk**: 25.24 points
- **TP 1RR**: 19838.24 ❌
- **TP 2RR**: 19813.00 ❌
- **TP 3RR**: 19787.76 ❌
- **TP 4RR**: 19762.52 ❌
- **TP 15RR**: 19484.87 ❌
- **PnL**: -25.24 points (-1.0R)
- **MFE**: 24.99 points
- **MAE**: 28.82 points

### Trade #755 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 13:00:00
- **FVG 5m**: 19866.80 - 19888.48
- **Entrée**: 19893.83 @ 2025-04-30 13:48:00
- **Stop Loss**: 19856.86
- **Risk**: 36.97 points
- **TP 1RR**: 19930.80 ✅
- **TP 2RR**: 19967.76 ✅
- **TP 3RR**: 20004.73 ✅
- **TP 4RR**: 20041.70 ✅
- **TP 15RR**: 20448.32 ✅
- **PnL**: 554.49 points (15.0R)
- **MFE**: 555.96 points
- **MAE**: 35.19 points

### Trade #756 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 14:45:00
- **FVG 5m**: 20290.14 - 20297.54
- **Entrée**: 20288.36 @ 2025-04-30 18:07:00
- **Stop Loss**: 20307.69
- **Risk**: 19.33 points
- **TP 1RR**: 20269.03 ✅
- **TP 2RR**: 20249.70 ❌
- **TP 3RR**: 20230.37 ❌
- **TP 4RR**: 20211.04 ❌
- **TP 15RR**: 19998.41 ❌
- **PnL**: -19.33 points (-1.0R)
- **MFE**: 20.91 points
- **MAE**: 23.46 points

### Trade #757 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 19:15:00
- **FVG 5m**: 20330.69 - 20339.87
- **Entrée**: 20315.13 @ 2025-04-30 20:09:00
- **Stop Loss**: 20350.04
- **Risk**: 34.91 points
- **TP 1RR**: 20280.23 ❌
- **TP 2RR**: 20245.32 ❌
- **TP 3RR**: 20210.41 ❌
- **TP 4RR**: 20175.50 ❌
- **TP 15RR**: 19791.52 ❌
- **PnL**: -34.91 points (-1.0R)
- **MFE**: 4.08 points
- **MAE**: 36.21 points

### Trade #758 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 23:00:00
- **FVG 5m**: 20343.70 - 20345.99
- **Entrée**: 20340.89 @ 2025-04-30 23:24:00
- **Stop Loss**: 20356.17
- **Risk**: 15.27 points
- **TP 1RR**: 20325.62 ❌
- **TP 2RR**: 20310.34 ❌
- **TP 3RR**: 20295.07 ❌
- **TP 4RR**: 20279.80 ❌
- **TP 15RR**: 20111.79 ❌
- **PnL**: -15.27 points (-1.0R)
- **MFE**: 5.87 points
- **MAE**: 17.34 points

### Trade #759 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 07:45:00
- **FVG 5m**: 20366.39 - 20368.43
- **Entrée**: 20321.76 @ 2025-05-01 08:31:00
- **Stop Loss**: 20378.62
- **Risk**: 56.85 points
- **TP 1RR**: 20264.91 ❌
- **TP 2RR**: 20208.06 ❌
- **TP 3RR**: 20151.20 ❌
- **TP 4RR**: 20094.35 ❌
- **TP 15RR**: 19468.95 ❌
- **PnL**: -56.85 points (-1.0R)
- **MFE**: 8.16 points
- **MAE**: 57.64 points

### Trade #760 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 07:45:00
- **FVG 5m**: 20366.39 - 20368.43
- **Entrée**: 20321.76 @ 2025-05-01 08:31:00
- **Stop Loss**: 20378.62
- **Risk**: 56.85 points
- **TP 1RR**: 20264.91 ❌
- **TP 2RR**: 20208.06 ❌
- **TP 3RR**: 20151.20 ❌
- **TP 4RR**: 20094.35 ❌
- **TP 15RR**: 19468.95 ❌
- **PnL**: -56.85 points (-1.0R)
- **MFE**: 8.16 points
- **MAE**: 57.64 points

### Trade #761 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 08:30:00
- **FVG 5m**: 20335.54 - 20337.83
- **Entrée**: 20357.47 @ 2025-05-01 09:17:00
- **Stop Loss**: 20325.37
- **Risk**: 32.10 points
- **TP 1RR**: 20389.57 ✅
- **TP 2RR**: 20421.67 ✅
- **TP 3RR**: 20453.77 ✅
- **TP 4RR**: 20485.87 ✅
- **TP 15RR**: 20838.97 ❌
- **PnL**: -32.10 points (-1.0R)
- **MFE**: 172.91 points
- **MAE**: 42.08 points

### Trade #762 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 08:30:00
- **FVG 5m**: 20335.54 - 20337.83
- **Entrée**: 20357.47 @ 2025-05-01 09:17:00
- **Stop Loss**: 20325.37
- **Risk**: 32.10 points
- **TP 1RR**: 20389.57 ✅
- **TP 2RR**: 20421.67 ✅
- **TP 3RR**: 20453.77 ✅
- **TP 4RR**: 20485.87 ✅
- **TP 15RR**: 20838.97 ❌
- **PnL**: -32.10 points (-1.0R)
- **MFE**: 172.91 points
- **MAE**: 42.08 points

### Trade #763 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 08:30:00
- **FVG 5m**: 20335.54 - 20337.83
- **Entrée**: 20357.47 @ 2025-05-01 09:17:00
- **Stop Loss**: 20325.37
- **Risk**: 32.10 points
- **TP 1RR**: 20389.57 ✅
- **TP 2RR**: 20421.67 ✅
- **TP 3RR**: 20453.77 ✅
- **TP 4RR**: 20485.87 ✅
- **TP 15RR**: 20838.97 ❌
- **PnL**: -32.10 points (-1.0R)
- **MFE**: 172.91 points
- **MAE**: 42.08 points

### Trade #764 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 09:30:00
- **FVG 5m**: 20431.43 - 20433.98
- **Entrée**: 20426.07 @ 2025-05-01 10:49:00
- **Stop Loss**: 20444.19
- **Risk**: 18.12 points
- **TP 1RR**: 20407.95 ✅
- **TP 2RR**: 20389.83 ✅
- **TP 3RR**: 20371.70 ✅
- **TP 4RR**: 20353.58 ✅
- **TP 15RR**: 20154.23 ❌
- **PnL**: -18.12 points (-1.0R)
- **MFE**: 115.78 points
- **MAE**: 21.68 points

### Trade #765 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 09:30:00
- **FVG 5m**: 20431.43 - 20433.98
- **Entrée**: 20426.07 @ 2025-05-01 10:49:00
- **Stop Loss**: 20444.19
- **Risk**: 18.12 points
- **TP 1RR**: 20407.95 ✅
- **TP 2RR**: 20389.83 ✅
- **TP 3RR**: 20371.70 ✅
- **TP 4RR**: 20353.58 ✅
- **TP 15RR**: 20154.23 ❌
- **PnL**: -18.12 points (-1.0R)
- **MFE**: 115.78 points
- **MAE**: 21.68 points

### Trade #766 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 10:30:00
- **FVG 5m**: 20431.43 - 20433.98
- **Entrée**: 20426.07 @ 2025-05-01 10:49:00
- **Stop Loss**: 20444.19
- **Risk**: 18.12 points
- **TP 1RR**: 20407.95 ✅
- **TP 2RR**: 20389.83 ✅
- **TP 3RR**: 20371.70 ✅
- **TP 4RR**: 20353.58 ✅
- **TP 15RR**: 20154.23 ❌
- **PnL**: -18.12 points (-1.0R)
- **MFE**: 115.78 points
- **MAE**: 21.68 points

### Trade #767 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 19:15:00
- **FVG 5m**: 20233.27 - 20260.81
- **Entrée**: 20265.15 @ 2025-05-01 19:29:00
- **Stop Loss**: 20223.15
- **Risk**: 41.99 points
- **TP 1RR**: 20307.14 ✅
- **TP 2RR**: 20349.14 ✅
- **TP 3RR**: 20391.13 ✅
- **TP 4RR**: 20433.13 ✅
- **TP 15RR**: 20895.07 ❌
- **PnL**: -41.99 points (-1.0R)
- **MFE**: 419.26 points
- **MAE**: 42.33 points

### Trade #768 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 23:15:00
- **FVG 5m**: 20352.88 - 20366.65
- **Entrée**: 20350.33 @ 2025-05-02 00:38:00
- **Stop Loss**: 20376.83
- **Risk**: 26.51 points
- **TP 1RR**: 20323.82 ✅
- **TP 2RR**: 20297.32 ✅
- **TP 3RR**: 20270.81 ✅
- **TP 4RR**: 20244.31 ❌
- **TP 15RR**: 19952.75 ❌
- **PnL**: -26.51 points (-1.0R)
- **MFE**: 86.96 points
- **MAE**: 78.80 points

### Trade #769 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 01:15:00
- **FVG 5m**: 20307.99 - 20314.37
- **Entrée**: 20316.41 @ 2025-05-02 01:42:00
- **Stop Loss**: 20297.84
- **Risk**: 18.57 points
- **TP 1RR**: 20334.98 ✅
- **TP 2RR**: 20353.55 ✅
- **TP 3RR**: 20372.12 ❌
- **TP 4RR**: 20390.69 ❌
- **TP 15RR**: 20594.96 ❌
- **PnL**: -18.57 points (-1.0R)
- **MFE**: 44.37 points
- **MAE**: 20.15 points

### Trade #770 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 01:15:00
- **FVG 5m**: 20307.99 - 20314.37
- **Entrée**: 20316.41 @ 2025-05-02 01:42:00
- **Stop Loss**: 20297.84
- **Risk**: 18.57 points
- **TP 1RR**: 20334.98 ✅
- **TP 2RR**: 20353.55 ✅
- **TP 3RR**: 20372.12 ❌
- **TP 4RR**: 20390.69 ❌
- **TP 15RR**: 20594.96 ❌
- **PnL**: -18.57 points (-1.0R)
- **MFE**: 44.37 points
- **MAE**: 20.15 points

### Trade #771 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 04:00:00
- **FVG 5m**: 20299.83 - 20303.91
- **Entrée**: 20305.44 @ 2025-05-02 04:14:00
- **Stop Loss**: 20289.68
- **Risk**: 15.76 points
- **TP 1RR**: 20321.20 ❌
- **TP 2RR**: 20336.96 ❌
- **TP 3RR**: 20352.72 ❌
- **TP 4RR**: 20368.49 ❌
- **TP 15RR**: 20541.85 ❌
- **PnL**: -15.76 points (-1.0R)
- **MFE**: 7.65 points
- **MAE**: 16.58 points

### Trade #772 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 11:00:00
- **FVG 5m**: 20632.90 - 20647.69
- **Entrée**: 20648.96 @ 2025-05-02 13:04:00
- **Stop Loss**: 20622.58
- **Risk**: 26.38 points
- **TP 1RR**: 20675.35 ✅
- **TP 2RR**: 20701.73 ❌
- **TP 3RR**: 20728.11 ❌
- **TP 4RR**: 20754.50 ❌
- **TP 15RR**: 21044.71 ❌
- **PnL**: -26.38 points (-1.0R)
- **MFE**: 35.45 points
- **MAE**: 33.92 points

### Trade #773 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 11:00:00
- **FVG 5m**: 20632.90 - 20647.69
- **Entrée**: 20648.96 @ 2025-05-02 13:04:00
- **Stop Loss**: 20622.58
- **Risk**: 26.38 points
- **TP 1RR**: 20675.35 ✅
- **TP 2RR**: 20701.73 ❌
- **TP 3RR**: 20728.11 ❌
- **TP 4RR**: 20754.50 ❌
- **TP 15RR**: 21044.71 ❌
- **PnL**: -26.38 points (-1.0R)
- **MFE**: 35.45 points
- **MAE**: 33.92 points

### Trade #774 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-02 13:30:00
- **FVG 5m**: 20641.06 - 20659.16
- **Entrée**: 20634.43 @ 2025-05-02 13:48:00
- **Stop Loss**: 20669.49
- **Risk**: 35.07 points
- **TP 1RR**: 20599.36 ✅
- **TP 2RR**: 20564.29 ✅
- **TP 3RR**: 20529.23 ✅
- **TP 4RR**: 20494.16 ✅
- **TP 15RR**: 20108.42 ✅
- **PnL**: 526.01 points (15.0R)
- **MFE**: 551.88 points
- **MAE**: 8.16 points

### Trade #775 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-02 14:00:00
- **FVG 5m**: 20573.48 - 20596.94
- **Entrée**: 20558.68 @ 2025-05-04 17:01:00
- **Stop Loss**: 20607.24
- **Risk**: 48.55 points
- **TP 1RR**: 20510.13 ✅
- **TP 2RR**: 20461.58 ✅
- **TP 3RR**: 20413.03 ✅
- **TP 4RR**: 20364.47 ✅
- **TP 15RR**: 19830.40 ❌
- **PnL**: -48.55 points (-1.0R)
- **MFE**: 484.29 points
- **MAE**: 52.28 points

### Trade #776 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-04 17:30:00
- **FVG 5m**: 20526.55 - 20537.52
- **Entrée**: 20520.43 @ 2025-05-04 17:44:00
- **Stop Loss**: 20547.79
- **Risk**: 27.36 points
- **TP 1RR**: 20493.07 ✅
- **TP 2RR**: 20465.72 ✅
- **TP 3RR**: 20438.36 ✅
- **TP 4RR**: 20411.01 ✅
- **TP 15RR**: 20110.10 ❌
- **PnL**: -27.36 points (-1.0R)
- **MFE**: 153.02 points
- **MAE**: 28.05 points

### Trade #777 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-04 17:30:00
- **FVG 5m**: 20526.55 - 20537.52
- **Entrée**: 20520.43 @ 2025-05-04 17:44:00
- **Stop Loss**: 20547.79
- **Risk**: 27.36 points
- **TP 1RR**: 20493.07 ✅
- **TP 2RR**: 20465.72 ✅
- **TP 3RR**: 20438.36 ✅
- **TP 4RR**: 20411.01 ✅
- **TP 15RR**: 20110.10 ❌
- **PnL**: -27.36 points (-1.0R)
- **MFE**: 153.02 points
- **MAE**: 28.05 points

### Trade #778 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-04 22:30:00
- **FVG 5m**: 20444.18 - 20453.36
- **Entrée**: 20461.52 @ 2025-05-05 00:01:00
- **Stop Loss**: 20433.96
- **Risk**: 27.56 points
- **TP 1RR**: 20489.08 ✅
- **TP 2RR**: 20516.65 ❌
- **TP 3RR**: 20544.21 ❌
- **TP 4RR**: 20571.77 ❌
- **TP 15RR**: 20874.98 ❌
- **PnL**: -27.56 points (-1.0R)
- **MFE**: 41.31 points
- **MAE**: 28.05 points

### Trade #779 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-05 01:45:00
- **FVG 5m**: 20451.06 - 20463.56
- **Entrée**: 20442.14 @ 2025-05-05 03:30:00
- **Stop Loss**: 20473.79
- **Risk**: 31.65 points
- **TP 1RR**: 20410.48 ✅
- **TP 2RR**: 20378.83 ✅
- **TP 3RR**: 20347.18 ❌
- **TP 4RR**: 20315.52 ❌
- **TP 15RR**: 19967.33 ❌
- **PnL**: -31.65 points (-1.0R)
- **MFE**: 74.72 points
- **MAE**: 32.39 points

### Trade #780 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-05 03:45:00
- **FVG 5m**: 20407.20 - 20410.77
- **Entrée**: 20415.10 @ 2025-05-05 04:21:00
- **Stop Loss**: 20397.00
- **Risk**: 18.11 points
- **TP 1RR**: 20433.21 ❌
- **TP 2RR**: 20451.32 ❌
- **TP 3RR**: 20469.43 ❌
- **TP 4RR**: 20487.54 ❌
- **TP 15RR**: 20686.75 ❌
- **PnL**: -18.11 points (-1.0R)
- **MFE**: 15.81 points
- **MAE**: 23.46 points

### Trade #781 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-05 06:45:00
- **FVG 5m**: 20393.17 - 20398.02
- **Entrée**: 20400.31 @ 2025-05-05 07:09:00
- **Stop Loss**: 20382.98
- **Risk**: 17.34 points
- **TP 1RR**: 20417.65 ❌
- **TP 2RR**: 20434.99 ❌
- **TP 3RR**: 20452.33 ❌
- **TP 4RR**: 20469.66 ❌
- **TP 15RR**: 20660.37 ❌
- **PnL**: -17.34 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 17.60 points

### Trade #782 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-05 08:30:00
- **FVG 5m**: 20452.08 - 20455.40
- **Entrée**: 20457.69 @ 2025-05-05 08:56:00
- **Stop Loss**: 20441.86
- **Risk**: 15.84 points
- **TP 1RR**: 20473.53 ✅
- **TP 2RR**: 20489.37 ✅
- **TP 3RR**: 20505.20 ✅
- **TP 4RR**: 20521.04 ❌
- **TP 15RR**: 20695.24 ❌
- **PnL**: -15.84 points (-1.0R)
- **MFE**: 57.64 points
- **MAE**: 21.42 points

### Trade #783 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-05 21:00:00
- **FVG 5m**: 20345.99 - 20353.90
- **Entrée**: 20344.46 @ 2025-05-05 22:04:00
- **Stop Loss**: 20364.08
- **Risk**: 19.61 points
- **TP 1RR**: 20324.85 ❌
- **TP 2RR**: 20305.24 ❌
- **TP 3RR**: 20285.62 ❌
- **TP 4RR**: 20266.01 ❌
- **TP 15RR**: 20050.27 ❌
- **PnL**: -19.61 points (-1.0R)
- **MFE**: 11.48 points
- **MAE**: 21.42 points

### Trade #784 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 03:30:00
- **FVG 5m**: 20263.62 - 20270.25
- **Entrée**: 20271.78 @ 2025-05-06 03:42:00
- **Stop Loss**: 20253.49
- **Risk**: 18.29 points
- **TP 1RR**: 20290.07 ❌
- **TP 2RR**: 20308.37 ❌
- **TP 3RR**: 20326.66 ❌
- **TP 4RR**: 20344.95 ❌
- **TP 15RR**: 20546.17 ❌
- **PnL**: -18.29 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 20.15 points

### Trade #785 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 06:45:00
- **FVG 5m**: 20215.67 - 20224.09
- **Entrée**: 20227.66 @ 2025-05-06 07:48:00
- **Stop Loss**: 20205.57
- **Risk**: 22.09 points
- **TP 1RR**: 20249.75 ❌
- **TP 2RR**: 20271.85 ❌
- **TP 3RR**: 20293.94 ❌
- **TP 4RR**: 20316.04 ❌
- **TP 15RR**: 20559.07 ❌
- **PnL**: -22.09 points (-1.0R)
- **MFE**: 18.36 points
- **MAE**: 24.48 points

### Trade #786 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 09:00:00
- **FVG 5m**: 20244.49 - 20267.19
- **Entrée**: 20277.90 @ 2025-05-06 09:20:00
- **Stop Loss**: 20234.37
- **Risk**: 43.53 points
- **TP 1RR**: 20321.43 ✅
- **TP 2RR**: 20364.96 ✅
- **TP 3RR**: 20408.49 ✅
- **TP 4RR**: 20452.02 ❌
- **TP 15RR**: 20930.86 ❌
- **PnL**: -43.53 points (-1.0R)
- **MFE**: 150.98 points
- **MAE**: 46.67 points

### Trade #787 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 09:00:00
- **FVG 5m**: 20244.49 - 20267.19
- **Entrée**: 20277.90 @ 2025-05-06 09:20:00
- **Stop Loss**: 20234.37
- **Risk**: 43.53 points
- **TP 1RR**: 20321.43 ✅
- **TP 2RR**: 20364.96 ✅
- **TP 3RR**: 20408.49 ✅
- **TP 4RR**: 20452.02 ❌
- **TP 15RR**: 20930.86 ❌
- **PnL**: -43.53 points (-1.0R)
- **MFE**: 150.98 points
- **MAE**: 46.67 points

### Trade #788 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 09:30:00
- **FVG 5m**: 20311.31 - 20359.25
- **Entrée**: 20389.09 @ 2025-05-06 11:13:00
- **Stop Loss**: 20301.15
- **Risk**: 87.94 points
- **TP 1RR**: 20477.03 ❌
- **TP 2RR**: 20564.97 ❌
- **TP 3RR**: 20652.91 ❌
- **TP 4RR**: 20740.85 ❌
- **TP 15RR**: 21708.17 ❌
- **PnL**: -87.94 points (-1.0R)
- **MFE**: 39.78 points
- **MAE**: 97.16 points

### Trade #789 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 09:45:00
- **FVG 5m**: 20319.47 - 20336.05
- **Entrée**: 20311.31 @ 2025-05-06 10:42:00
- **Stop Loss**: 20346.21
- **Risk**: 34.91 points
- **TP 1RR**: 20276.40 ❌
- **TP 2RR**: 20241.50 ❌
- **TP 3RR**: 20206.59 ❌
- **TP 4RR**: 20171.69 ❌
- **TP 15RR**: 19787.73 ❌
- **PnL**: -34.91 points (-1.0R)
- **MFE**: 29.07 points
- **MAE**: 37.74 points

### Trade #790 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 10:15:00
- **FVG 5m**: 20311.31 - 20359.25
- **Entrée**: 20389.09 @ 2025-05-06 11:13:00
- **Stop Loss**: 20301.15
- **Risk**: 87.94 points
- **TP 1RR**: 20477.03 ❌
- **TP 2RR**: 20564.97 ❌
- **TP 3RR**: 20652.91 ❌
- **TP 4RR**: 20740.85 ❌
- **TP 15RR**: 21708.17 ❌
- **PnL**: -87.94 points (-1.0R)
- **MFE**: 39.78 points
- **MAE**: 97.16 points

### Trade #791 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 11:00:00
- **FVG 5m**: 20311.31 - 20359.25
- **Entrée**: 20389.09 @ 2025-05-06 11:13:00
- **Stop Loss**: 20301.15
- **Risk**: 87.94 points
- **TP 1RR**: 20477.03 ❌
- **TP 2RR**: 20564.97 ❌
- **TP 3RR**: 20652.91 ❌
- **TP 4RR**: 20740.85 ❌
- **TP 15RR**: 21708.17 ❌
- **PnL**: -87.94 points (-1.0R)
- **MFE**: 39.78 points
- **MAE**: 97.16 points

### Trade #792 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 11:00:00
- **FVG 5m**: 20311.31 - 20359.25
- **Entrée**: 20389.09 @ 2025-05-06 11:13:00
- **Stop Loss**: 20301.15
- **Risk**: 87.94 points
- **TP 1RR**: 20477.03 ❌
- **TP 2RR**: 20564.97 ❌
- **TP 3RR**: 20652.91 ❌
- **TP 4RR**: 20740.85 ❌
- **TP 15RR**: 21708.17 ❌
- **PnL**: -87.94 points (-1.0R)
- **MFE**: 39.78 points
- **MAE**: 97.16 points

### Trade #793 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 11:15:00
- **FVG 5m**: 20307.23 - 20311.82
- **Entrée**: 20300.09 @ 2025-05-06 11:44:00
- **Stop Loss**: 20321.97
- **Risk**: 21.89 points
- **TP 1RR**: 20278.20 ✅
- **TP 2RR**: 20256.31 ✅
- **TP 3RR**: 20234.43 ❌
- **TP 4RR**: 20212.54 ❌
- **TP 15RR**: 19971.78 ❌
- **PnL**: -21.89 points (-1.0R)
- **MFE**: 63.76 points
- **MAE**: 30.35 points

### Trade #794 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 11:15:00
- **FVG 5m**: 20307.23 - 20311.82
- **Entrée**: 20300.09 @ 2025-05-06 11:44:00
- **Stop Loss**: 20321.97
- **Risk**: 21.89 points
- **TP 1RR**: 20278.20 ✅
- **TP 2RR**: 20256.31 ✅
- **TP 3RR**: 20234.43 ❌
- **TP 4RR**: 20212.54 ❌
- **TP 15RR**: 19971.78 ❌
- **PnL**: -21.89 points (-1.0R)
- **MFE**: 63.76 points
- **MAE**: 30.35 points

### Trade #795 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 15:30:00
- **FVG 5m**: 20255.71 - 20452.85
- **Entrée**: 20468.92 @ 2025-05-06 17:01:00
- **Stop Loss**: 20245.59
- **Risk**: 223.33 points
- **TP 1RR**: 20692.24 ❌
- **TP 2RR**: 20915.57 ❌
- **TP 3RR**: 21138.90 ❌
- **TP 4RR**: 21362.23 ❌
- **TP 15RR**: 23818.86 ❌
- **PnL**: -223.33 points (-1.0R)
- **MFE**: 69.62 points
- **MAE**: 228.25 points

### Trade #796 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 19:00:00
- **FVG 5m**: 20478.10 - 20484.73
- **Entrée**: 20474.27 @ 2025-05-06 20:13:00
- **Stop Loss**: 20494.97
- **Risk**: 20.70 points
- **TP 1RR**: 20453.57 ✅
- **TP 2RR**: 20432.87 ✅
- **TP 3RR**: 20412.18 ✅
- **TP 4RR**: 20391.48 ✅
- **TP 15RR**: 20163.79 ✅
- **PnL**: 310.48 points (15.0R)
- **MFE**: 347.09 points
- **MAE**: 3.83 points

### Trade #797 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 22:00:00
- **FVG 5m**: 20403.63 - 20409.49
- **Entrée**: 20412.04 @ 2025-05-06 22:33:00
- **Stop Loss**: 20393.43
- **Risk**: 18.62 points
- **TP 1RR**: 20430.66 ✅
- **TP 2RR**: 20449.28 ❌
- **TP 3RR**: 20467.90 ❌
- **TP 4RR**: 20486.51 ❌
- **TP 15RR**: 20691.31 ❌
- **PnL**: -18.62 points (-1.0R)
- **MFE**: 26.27 points
- **MAE**: 21.17 points

### Trade #798 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 01:45:00
- **FVG 5m**: 20396.49 - 20400.31
- **Entrée**: 20405.41 @ 2025-05-07 02:20:00
- **Stop Loss**: 20386.29
- **Risk**: 19.12 points
- **TP 1RR**: 20424.54 ✅
- **TP 2RR**: 20443.66 ❌
- **TP 3RR**: 20462.79 ❌
- **TP 4RR**: 20481.91 ❌
- **TP 15RR**: 20692.28 ❌
- **PnL**: -19.12 points (-1.0R)
- **MFE**: 22.19 points
- **MAE**: 19.89 points

### Trade #799 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 09:15:00
- **FVG 5m**: 20228.94 - 20237.35
- **Entrée**: 20240.16 @ 2025-05-07 11:39:00
- **Stop Loss**: 20218.82
- **Risk**: 21.34 points
- **TP 1RR**: 20261.49 ✅
- **TP 2RR**: 20282.83 ✅
- **TP 3RR**: 20304.16 ✅
- **TP 4RR**: 20325.50 ✅
- **TP 15RR**: 20560.19 ❌
- **PnL**: -21.34 points (-1.0R)
- **MFE**: 86.20 points
- **MAE**: 33.92 points

### Trade #800 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 09:15:00
- **FVG 5m**: 20228.94 - 20237.35
- **Entrée**: 20240.16 @ 2025-05-07 11:39:00
- **Stop Loss**: 20218.82
- **Risk**: 21.34 points
- **TP 1RR**: 20261.49 ✅
- **TP 2RR**: 20282.83 ✅
- **TP 3RR**: 20304.16 ✅
- **TP 4RR**: 20325.50 ✅
- **TP 15RR**: 20560.19 ❌
- **PnL**: -21.34 points (-1.0R)
- **MFE**: 86.20 points
- **MAE**: 33.92 points

### Trade #801 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 10:00:00
- **FVG 5m**: 20228.94 - 20237.35
- **Entrée**: 20240.16 @ 2025-05-07 11:39:00
- **Stop Loss**: 20218.82
- **Risk**: 21.34 points
- **TP 1RR**: 20261.49 ✅
- **TP 2RR**: 20282.83 ✅
- **TP 3RR**: 20304.16 ✅
- **TP 4RR**: 20325.50 ✅
- **TP 15RR**: 20560.19 ❌
- **PnL**: -21.34 points (-1.0R)
- **MFE**: 86.20 points
- **MAE**: 33.92 points

### Trade #802 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 13:15:00
- **FVG 5m**: 20186.35 - 20190.17
- **Entrée**: 20191.96 @ 2025-05-07 13:31:00
- **Stop Loss**: 20176.25
- **Risk**: 15.70 points
- **TP 1RR**: 20207.66 ✅
- **TP 2RR**: 20223.36 ✅
- **TP 3RR**: 20239.07 ✅
- **TP 4RR**: 20254.77 ✅
- **TP 15RR**: 20427.51 ❌
- **PnL**: -15.70 points (-1.0R)
- **MFE**: 66.31 points
- **MAE**: 31.37 points

### Trade #803 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 13:30:00
- **FVG 5m**: 20194.25 - 20243.47
- **Entrée**: 20260.05 @ 2025-05-07 13:56:00
- **Stop Loss**: 20184.15
- **Risk**: 75.89 points
- **TP 1RR**: 20335.94 ❌
- **TP 2RR**: 20411.84 ❌
- **TP 3RR**: 20487.73 ❌
- **TP 4RR**: 20563.62 ❌
- **TP 15RR**: 21398.46 ❌
- **PnL**: -75.89 points (-1.0R)
- **MFE**: 43.10 points
- **MAE**: 79.57 points

### Trade #804 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:30:00
- **FVG 5m**: 20338.60 - 20358.74
- **Entrée**: 20332.22 @ 2025-05-07 17:00:00
- **Stop Loss**: 20368.92
- **Risk**: 36.70 points
- **TP 1RR**: 20295.52 ❌
- **TP 2RR**: 20258.82 ❌
- **TP 3RR**: 20222.11 ❌
- **TP 4RR**: 20185.41 ❌
- **TP 15RR**: 19781.69 ❌
- **PnL**: -36.70 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 38.00 points

### Trade #805 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:30:00
- **FVG 5m**: 20338.60 - 20358.74
- **Entrée**: 20332.22 @ 2025-05-07 17:00:00
- **Stop Loss**: 20368.92
- **Risk**: 36.70 points
- **TP 1RR**: 20295.52 ❌
- **TP 2RR**: 20258.82 ❌
- **TP 3RR**: 20222.11 ❌
- **TP 4RR**: 20185.41 ❌
- **TP 15RR**: 19781.69 ❌
- **PnL**: -36.70 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 38.00 points

### Trade #806 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:30:00
- **FVG 5m**: 20338.60 - 20358.74
- **Entrée**: 20332.22 @ 2025-05-07 17:00:00
- **Stop Loss**: 20368.92
- **Risk**: 36.70 points
- **TP 1RR**: 20295.52 ❌
- **TP 2RR**: 20258.82 ❌
- **TP 3RR**: 20222.11 ❌
- **TP 4RR**: 20185.41 ❌
- **TP 15RR**: 19781.69 ❌
- **PnL**: -36.70 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 38.00 points

### Trade #807 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:45:00
- **FVG 5m**: 20338.60 - 20358.74
- **Entrée**: 20332.22 @ 2025-05-07 17:00:00
- **Stop Loss**: 20368.92
- **Risk**: 36.70 points
- **TP 1RR**: 20295.52 ❌
- **TP 2RR**: 20258.82 ❌
- **TP 3RR**: 20222.11 ❌
- **TP 4RR**: 20185.41 ❌
- **TP 15RR**: 19781.69 ❌
- **PnL**: -36.70 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 38.00 points

### Trade #808 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 06:30:00
- **FVG 5m**: 20604.59 - 20611.22
- **Entrée**: 20603.06 @ 2025-05-08 06:43:00
- **Stop Loss**: 20621.53
- **Risk**: 18.47 points
- **TP 1RR**: 20584.59 ❌
- **TP 2RR**: 20566.13 ❌
- **TP 3RR**: 20547.66 ❌
- **TP 4RR**: 20529.19 ❌
- **TP 15RR**: 20326.06 ❌
- **PnL**: -18.47 points (-1.0R)
- **MFE**: 12.24 points
- **MAE**: 19.89 points

### Trade #809 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 07:30:00
- **FVG 5m**: 20543.13 - 20563.27
- **Entrée**: 20531.40 @ 2025-05-08 08:32:00
- **Stop Loss**: 20573.56
- **Risk**: 42.16 points
- **TP 1RR**: 20489.24 ✅
- **TP 2RR**: 20447.08 ✅
- **TP 3RR**: 20404.92 ✅
- **TP 4RR**: 20362.76 ❌
- **TP 15RR**: 19899.00 ❌
- **PnL**: -42.16 points (-1.0R)
- **MFE**: 150.72 points
- **MAE**: 44.12 points

### Trade #810 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 08:30:00
- **FVG 5m**: 20499.01 - 20503.09
- **Entrée**: 20483.20 @ 2025-05-08 08:48:00
- **Stop Loss**: 20513.34
- **Risk**: 30.14 points
- **TP 1RR**: 20453.05 ❌
- **TP 2RR**: 20422.91 ❌
- **TP 3RR**: 20392.77 ❌
- **TP 4RR**: 20362.62 ❌
- **TP 15RR**: 20031.04 ❌
- **PnL**: -30.14 points (-1.0R)
- **MFE**: 18.87 points
- **MAE**: 33.66 points

### Trade #811 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 08:30:00
- **FVG 5m**: 20499.01 - 20503.09
- **Entrée**: 20483.20 @ 2025-05-08 08:48:00
- **Stop Loss**: 20513.34
- **Risk**: 30.14 points
- **TP 1RR**: 20453.05 ❌
- **TP 2RR**: 20422.91 ❌
- **TP 3RR**: 20392.77 ❌
- **TP 4RR**: 20362.62 ❌
- **TP 15RR**: 20031.04 ❌
- **PnL**: -30.14 points (-1.0R)
- **MFE**: 18.87 points
- **MAE**: 33.66 points

### Trade #812 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-08 10:15:00
- **FVG 5m**: 20605.10 - 20623.21
- **Entrée**: 20623.72 @ 2025-05-08 10:39:00
- **Stop Loss**: 20594.80
- **Risk**: 28.92 points
- **TP 1RR**: 20652.64 ✅
- **TP 2RR**: 20681.55 ✅
- **TP 3RR**: 20710.47 ✅
- **TP 4RR**: 20739.39 ✅
- **TP 15RR**: 21057.51 ❌
- **PnL**: -28.92 points (-1.0R)
- **MFE**: 122.41 points
- **MAE**: 42.59 points

### Trade #813 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 10:45:00
- **FVG 5m**: 20730.57 - 20734.65
- **Entrée**: 20719.10 @ 2025-05-08 12:02:00
- **Stop Loss**: 20745.02
- **Risk**: 25.92 points
- **TP 1RR**: 20693.17 ✅
- **TP 2RR**: 20667.25 ✅
- **TP 3RR**: 20641.32 ✅
- **TP 4RR**: 20615.40 ✅
- **TP 15RR**: 20330.24 ❌
- **PnL**: -25.92 points (-1.0R)
- **MFE**: 257.83 points
- **MAE**: 167.30 points

### Trade #814 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 12:45:00
- **FVG 5m**: 20668.60 - 20673.45
- **Entrée**: 20665.03 @ 2025-05-08 12:57:00
- **Stop Loss**: 20683.78
- **Risk**: 18.75 points
- **TP 1RR**: 20646.28 ✅
- **TP 2RR**: 20627.53 ❌
- **TP 3RR**: 20608.77 ❌
- **TP 4RR**: 20590.02 ❌
- **TP 15RR**: 20383.74 ❌
- **PnL**: -18.75 points (-1.0R)
- **MFE**: 23.97 points
- **MAE**: 20.40 points

### Trade #815 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-08 20:15:00
- **FVG 5m**: 20563.02 - 20568.63
- **Entrée**: 20569.14 @ 2025-05-08 21:11:00
- **Stop Loss**: 20552.74
- **Risk**: 16.40 points
- **TP 1RR**: 20585.54 ✅
- **TP 2RR**: 20601.94 ✅
- **TP 3RR**: 20618.35 ❌
- **TP 4RR**: 20634.75 ❌
- **TP 15RR**: 20815.17 ❌
- **PnL**: -16.40 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 17.34 points

### Trade #816 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-09 02:45:00
- **FVG 5m**: 20608.16 - 20613.00
- **Entrée**: 20607.90 @ 2025-05-09 02:56:00
- **Stop Loss**: 20623.31
- **Risk**: 15.41 points
- **TP 1RR**: 20592.50 ✅
- **TP 2RR**: 20577.09 ✅
- **TP 3RR**: 20561.68 ❌
- **TP 4RR**: 20546.28 ❌
- **TP 15RR**: 20376.80 ❌
- **PnL**: -15.41 points (-1.0R)
- **MFE**: 37.49 points
- **MAE**: 17.60 points

### Trade #817 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-09 02:45:00
- **FVG 5m**: 20608.16 - 20613.00
- **Entrée**: 20607.90 @ 2025-05-09 02:56:00
- **Stop Loss**: 20623.31
- **Risk**: 15.41 points
- **TP 1RR**: 20592.50 ✅
- **TP 2RR**: 20577.09 ✅
- **TP 3RR**: 20561.68 ❌
- **TP 4RR**: 20546.28 ❌
- **TP 15RR**: 20376.80 ❌
- **PnL**: -15.41 points (-1.0R)
- **MFE**: 37.49 points
- **MAE**: 17.60 points

### Trade #818 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 06:00:00
- **FVG 5m**: 20643.35 - 20648.20
- **Entrée**: 20650.24 @ 2025-05-09 06:13:00
- **Stop Loss**: 20633.03
- **Risk**: 17.21 points
- **TP 1RR**: 20667.45 ❌
- **TP 2RR**: 20684.65 ❌
- **TP 3RR**: 20701.86 ❌
- **TP 4RR**: 20719.07 ❌
- **TP 15RR**: 20908.35 ❌
- **PnL**: -17.21 points (-1.0R)
- **MFE**: 46.41 points
- **MAE**: 92.83 points

### Trade #819 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-09 06:15:00
- **FVG 5m**: 20619.89 - 20643.61
- **Entrée**: 20568.89 @ 2025-05-09 06:26:00
- **Stop Loss**: 20653.93
- **Risk**: 85.04 points
- **TP 1RR**: 20483.84 ❌
- **TP 2RR**: 20398.80 ❌
- **TP 3RR**: 20313.75 ❌
- **TP 4RR**: 20228.71 ❌
- **TP 15RR**: 19293.22 ❌
- **PnL**: -85.04 points (-1.0R)
- **MFE**: 23.97 points
- **MAE**: 94.36 points

### Trade #820 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 06:15:00
- **FVG 5m**: 20596.43 - 20602.04
- **Entrée**: 20602.80 @ 2025-05-09 06:44:00
- **Stop Loss**: 20586.13
- **Risk**: 16.67 points
- **TP 1RR**: 20619.48 ✅
- **TP 2RR**: 20636.15 ✅
- **TP 3RR**: 20652.83 ✅
- **TP 4RR**: 20669.50 ✅
- **TP 15RR**: 20852.91 ❌
- **PnL**: -16.67 points (-1.0R)
- **MFE**: 84.67 points
- **MAE**: 20.15 points

### Trade #821 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 06:15:00
- **FVG 5m**: 20596.43 - 20602.04
- **Entrée**: 20602.80 @ 2025-05-09 06:44:00
- **Stop Loss**: 20586.13
- **Risk**: 16.67 points
- **TP 1RR**: 20619.48 ✅
- **TP 2RR**: 20636.15 ✅
- **TP 3RR**: 20652.83 ✅
- **TP 4RR**: 20669.50 ✅
- **TP 15RR**: 20852.91 ❌
- **PnL**: -16.67 points (-1.0R)
- **MFE**: 84.67 points
- **MAE**: 20.15 points

### Trade #822 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 06:15:00
- **FVG 5m**: 20596.43 - 20602.04
- **Entrée**: 20602.80 @ 2025-05-09 06:44:00
- **Stop Loss**: 20586.13
- **Risk**: 16.67 points
- **TP 1RR**: 20619.48 ✅
- **TP 2RR**: 20636.15 ✅
- **TP 3RR**: 20652.83 ✅
- **TP 4RR**: 20669.50 ✅
- **TP 15RR**: 20852.91 ❌
- **PnL**: -16.67 points (-1.0R)
- **MFE**: 84.67 points
- **MAE**: 20.15 points

### Trade #823 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 09:15:00
- **FVG 5m**: 20551.80 - 20563.27
- **Entrée**: 20568.63 @ 2025-05-09 10:04:00
- **Stop Loss**: 20541.52
- **Risk**: 27.11 points
- **TP 1RR**: 20595.74 ❌
- **TP 2RR**: 20622.85 ❌
- **TP 3RR**: 20649.95 ❌
- **TP 4RR**: 20677.06 ❌
- **TP 15RR**: 20975.24 ❌
- **PnL**: -27.11 points (-1.0R)
- **MFE**: 13.26 points
- **MAE**: 34.43 points

### Trade #824 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 09:30:00
- **FVG 5m**: 20551.80 - 20563.27
- **Entrée**: 20568.63 @ 2025-05-09 10:04:00
- **Stop Loss**: 20541.52
- **Risk**: 27.11 points
- **TP 1RR**: 20595.74 ❌
- **TP 2RR**: 20622.85 ❌
- **TP 3RR**: 20649.95 ❌
- **TP 4RR**: 20677.06 ❌
- **TP 15RR**: 20975.24 ❌
- **PnL**: -27.11 points (-1.0R)
- **MFE**: 13.26 points
- **MAE**: 34.43 points

### Trade #825 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 09:45:00
- **FVG 5m**: 20551.80 - 20563.27
- **Entrée**: 20568.63 @ 2025-05-09 10:04:00
- **Stop Loss**: 20541.52
- **Risk**: 27.11 points
- **TP 1RR**: 20595.74 ❌
- **TP 2RR**: 20622.85 ❌
- **TP 3RR**: 20649.95 ❌
- **TP 4RR**: 20677.06 ❌
- **TP 15RR**: 20975.24 ❌
- **PnL**: -27.11 points (-1.0R)
- **MFE**: 13.26 points
- **MAE**: 34.43 points

### Trade #826 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-11 17:30:00
- **FVG 5m**: 20827.74 - 20830.54
- **Entrée**: 20843.04 @ 2025-05-11 18:03:00
- **Stop Loss**: 20817.32
- **Risk**: 25.72 points
- **TP 1RR**: 20868.75 ✅
- **TP 2RR**: 20894.47 ✅
- **TP 3RR**: 20920.18 ✅
- **TP 4RR**: 20945.90 ✅
- **TP 15RR**: 21228.77 ✅
- **PnL**: 385.73 points (15.0R)
- **MFE**: 390.45 points
- **MAE**: 12.50 points

### Trade #827 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-11 18:15:00
- **FVG 5m**: 20865.99 - 20885.37
- **Entrée**: 20864.72 @ 2025-05-11 18:53:00
- **Stop Loss**: 20895.82
- **Risk**: 31.10 points
- **TP 1RR**: 20833.62 ❌
- **TP 2RR**: 20802.52 ❌
- **TP 3RR**: 20771.42 ❌
- **TP 4RR**: 20740.32 ❌
- **TP 15RR**: 20398.22 ❌
- **PnL**: -31.10 points (-1.0R)
- **MFE**: 12.75 points
- **MAE**: 40.29 points

### Trade #828 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-11 19:45:00
- **FVG 5m**: 20936.63 - 20948.62
- **Entrée**: 20935.10 @ 2025-05-11 20:38:00
- **Stop Loss**: 20959.09
- **Risk**: 23.99 points
- **TP 1RR**: 20911.11 ❌
- **TP 2RR**: 20887.12 ❌
- **TP 3RR**: 20863.13 ❌
- **TP 4RR**: 20839.14 ❌
- **TP 15RR**: 20575.24 ❌
- **PnL**: -23.99 points (-1.0R)
- **MFE**: 19.38 points
- **MAE**: 24.99 points

### Trade #829 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-11 19:45:00
- **FVG 5m**: 20936.63 - 20948.62
- **Entrée**: 20935.10 @ 2025-05-11 20:38:00
- **Stop Loss**: 20959.09
- **Risk**: 23.99 points
- **TP 1RR**: 20911.11 ❌
- **TP 2RR**: 20887.12 ❌
- **TP 3RR**: 20863.13 ❌
- **TP 4RR**: 20839.14 ❌
- **TP 15RR**: 20575.24 ❌
- **PnL**: -23.99 points (-1.0R)
- **MFE**: 19.38 points
- **MAE**: 24.99 points

### Trade #830 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-11 19:45:00
- **FVG 5m**: 20936.63 - 20948.62
- **Entrée**: 20935.10 @ 2025-05-11 20:38:00
- **Stop Loss**: 20959.09
- **Risk**: 23.99 points
- **TP 1RR**: 20911.11 ❌
- **TP 2RR**: 20887.12 ❌
- **TP 3RR**: 20863.13 ❌
- **TP 4RR**: 20839.14 ❌
- **TP 15RR**: 20575.24 ❌
- **PnL**: -23.99 points (-1.0R)
- **MFE**: 19.38 points
- **MAE**: 24.99 points

### Trade #831 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-11 20:30:00
- **FVG 5m**: 20933.83 - 20938.42
- **Entrée**: 20931.79 @ 2025-05-11 22:29:00
- **Stop Loss**: 20948.89
- **Risk**: 17.10 points
- **TP 1RR**: 20914.69 ❌
- **TP 2RR**: 20897.59 ❌
- **TP 3RR**: 20880.49 ❌
- **TP 4RR**: 20863.39 ❌
- **TP 15RR**: 20675.29 ❌
- **PnL**: -17.10 points (-1.0R)
- **MFE**: 7.65 points
- **MAE**: 18.36 points

### Trade #832 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 02:00:00
- **FVG 5m**: 21296.48 - 21311.27
- **Entrée**: 21312.03 @ 2025-05-12 02:23:00
- **Stop Loss**: 21285.83
- **Risk**: 26.20 points
- **TP 1RR**: 21338.24 ✅
- **TP 2RR**: 21364.44 ❌
- **TP 3RR**: 21390.65 ❌
- **TP 4RR**: 21416.85 ❌
- **TP 15RR**: 21705.10 ❌
- **PnL**: -26.20 points (-1.0R)
- **MFE**: 39.53 points
- **MAE**: 26.78 points

### Trade #833 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 02:00:00
- **FVG 5m**: 21296.48 - 21311.27
- **Entrée**: 21312.03 @ 2025-05-12 02:23:00
- **Stop Loss**: 21285.83
- **Risk**: 26.20 points
- **TP 1RR**: 21338.24 ✅
- **TP 2RR**: 21364.44 ❌
- **TP 3RR**: 21390.65 ❌
- **TP 4RR**: 21416.85 ❌
- **TP 15RR**: 21705.10 ❌
- **PnL**: -26.20 points (-1.0R)
- **MFE**: 39.53 points
- **MAE**: 26.78 points

### Trade #834 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 02:00:00
- **FVG 5m**: 21296.48 - 21311.27
- **Entrée**: 21312.03 @ 2025-05-12 02:23:00
- **Stop Loss**: 21285.83
- **Risk**: 26.20 points
- **TP 1RR**: 21338.24 ✅
- **TP 2RR**: 21364.44 ❌
- **TP 3RR**: 21390.65 ❌
- **TP 4RR**: 21416.85 ❌
- **TP 15RR**: 21705.10 ❌
- **PnL**: -26.20 points (-1.0R)
- **MFE**: 39.53 points
- **MAE**: 26.78 points

### Trade #835 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 02:30:00
- **FVG 5m**: 21232.97 - 21239.86
- **Entrée**: 21217.42 @ 2025-05-12 02:54:00
- **Stop Loss**: 21250.48
- **Risk**: 33.06 points
- **TP 1RR**: 21184.35 ❌
- **TP 2RR**: 21151.29 ❌
- **TP 3RR**: 21118.23 ❌
- **TP 4RR**: 21085.17 ❌
- **TP 15RR**: 20721.48 ❌
- **PnL**: -33.06 points (-1.0R)
- **MFE**: 15.30 points
- **MAE**: 36.47 points

### Trade #836 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 02:30:00
- **FVG 5m**: 21232.97 - 21239.86
- **Entrée**: 21217.42 @ 2025-05-12 02:54:00
- **Stop Loss**: 21250.48
- **Risk**: 33.06 points
- **TP 1RR**: 21184.35 ❌
- **TP 2RR**: 21151.29 ❌
- **TP 3RR**: 21118.23 ❌
- **TP 4RR**: 21085.17 ❌
- **TP 15RR**: 20721.48 ❌
- **PnL**: -33.06 points (-1.0R)
- **MFE**: 15.30 points
- **MAE**: 36.47 points

### Trade #837 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 05:30:00
- **FVG 5m**: 21353.60 - 21357.17
- **Entrée**: 21350.80 @ 2025-05-12 05:43:00
- **Stop Loss**: 21367.85
- **Risk**: 17.05 points
- **TP 1RR**: 21333.74 ❌
- **TP 2RR**: 21316.69 ❌
- **TP 3RR**: 21299.63 ❌
- **TP 4RR**: 21282.58 ❌
- **TP 15RR**: 21094.98 ❌
- **PnL**: -17.05 points (-1.0R)
- **MFE**: 13.52 points
- **MAE**: 30.35 points

### Trade #838 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 05:30:00
- **FVG 5m**: 21353.60 - 21357.17
- **Entrée**: 21350.80 @ 2025-05-12 05:43:00
- **Stop Loss**: 21367.85
- **Risk**: 17.05 points
- **TP 1RR**: 21333.74 ❌
- **TP 2RR**: 21316.69 ❌
- **TP 3RR**: 21299.63 ❌
- **TP 4RR**: 21282.58 ❌
- **TP 15RR**: 21094.98 ❌
- **PnL**: -17.05 points (-1.0R)
- **MFE**: 13.52 points
- **MAE**: 30.35 points

### Trade #839 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 05:30:00
- **FVG 5m**: 21353.60 - 21357.17
- **Entrée**: 21350.80 @ 2025-05-12 05:43:00
- **Stop Loss**: 21367.85
- **Risk**: 17.05 points
- **TP 1RR**: 21333.74 ❌
- **TP 2RR**: 21316.69 ❌
- **TP 3RR**: 21299.63 ❌
- **TP 4RR**: 21282.58 ❌
- **TP 15RR**: 21094.98 ❌
- **PnL**: -17.05 points (-1.0R)
- **MFE**: 13.52 points
- **MAE**: 30.35 points

### Trade #840 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 12:00:00
- **FVG 5m**: 21336.26 - 21340.34
- **Entrée**: 21344.68 @ 2025-05-12 13:18:00
- **Stop Loss**: 21325.59
- **Risk**: 19.08 points
- **TP 1RR**: 21363.76 ✅
- **TP 2RR**: 21382.84 ❌
- **TP 3RR**: 21401.93 ❌
- **TP 4RR**: 21421.01 ❌
- **TP 15RR**: 21630.94 ❌
- **PnL**: -19.08 points (-1.0R)
- **MFE**: 19.89 points
- **MAE**: 20.66 points

### Trade #841 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 17:00:00
- **FVG 5m**: 21344.68 - 21353.60
- **Entrée**: 21341.36 @ 2025-05-12 17:31:00
- **Stop Loss**: 21364.28
- **Risk**: 22.92 points
- **TP 1RR**: 21318.44 ❌
- **TP 2RR**: 21295.52 ❌
- **TP 3RR**: 21272.61 ❌
- **TP 4RR**: 21249.69 ❌
- **TP 15RR**: 20997.59 ❌
- **PnL**: -22.92 points (-1.0R)
- **MFE**: 7.65 points
- **MAE**: 23.21 points

### Trade #842 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-13 07:30:00
- **FVG 5m**: 21429.09 - 21431.89
- **Entrée**: 21418.63 @ 2025-05-13 07:41:00
- **Stop Loss**: 21442.61
- **Risk**: 23.98 points
- **TP 1RR**: 21394.66 ❌
- **TP 2RR**: 21370.68 ❌
- **TP 3RR**: 21346.70 ❌
- **TP 4RR**: 21322.72 ❌
- **TP 15RR**: 21058.97 ❌
- **PnL**: -23.98 points (-1.0R)
- **MFE**: 19.64 points
- **MAE**: 24.48 points

### Trade #843 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-13 07:30:00
- **FVG 5m**: 21429.09 - 21431.89
- **Entrée**: 21418.63 @ 2025-05-13 07:41:00
- **Stop Loss**: 21442.61
- **Risk**: 23.98 points
- **TP 1RR**: 21394.66 ❌
- **TP 2RR**: 21370.68 ❌
- **TP 3RR**: 21346.70 ❌
- **TP 4RR**: 21322.72 ❌
- **TP 15RR**: 21058.97 ❌
- **PnL**: -23.98 points (-1.0R)
- **MFE**: 19.64 points
- **MAE**: 24.48 points

### Trade #844 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-13 18:00:00
- **FVG 5m**: 21704.01 - 21715.74
- **Entrée**: 21719.05 @ 2025-05-13 18:37:00
- **Stop Loss**: 21693.16
- **Risk**: 25.90 points
- **TP 1RR**: 21744.95 ❌
- **TP 2RR**: 21770.85 ❌
- **TP 3RR**: 21796.75 ❌
- **TP 4RR**: 21822.65 ❌
- **TP 15RR**: 22107.53 ❌
- **PnL**: -25.90 points (-1.0R)
- **MFE**: 10.20 points
- **MAE**: 26.27 points

### Trade #845 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 02:15:00
- **FVG 5m**: 21722.37 - 21730.02
- **Entrée**: 21719.82 @ 2025-05-14 03:02:00
- **Stop Loss**: 21740.88
- **Risk**: 21.07 points
- **TP 1RR**: 21698.75 ✅
- **TP 2RR**: 21677.69 ✅
- **TP 3RR**: 21656.62 ❌
- **TP 4RR**: 21635.55 ❌
- **TP 15RR**: 21403.83 ❌
- **PnL**: -21.07 points (-1.0R)
- **MFE**: 54.58 points
- **MAE**: 35.19 points

### Trade #846 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 06:30:00
- **FVG 5m**: 21783.07 - 21788.17
- **Entrée**: 21782.30 @ 2025-05-14 06:44:00
- **Stop Loss**: 21799.06
- **Risk**: 16.76 points
- **TP 1RR**: 21765.54 ✅
- **TP 2RR**: 21748.78 ✅
- **TP 3RR**: 21732.02 ❌
- **TP 4RR**: 21715.26 ❌
- **TP 15RR**: 21530.90 ❌
- **PnL**: -16.76 points (-1.0R)
- **MFE**: 42.08 points
- **MAE**: 20.66 points

### Trade #847 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 06:45:00
- **FVG 5m**: 21772.10 - 21777.96
- **Entrée**: 21771.08 @ 2025-05-14 07:37:00
- **Stop Loss**: 21788.85
- **Risk**: 17.77 points
- **TP 1RR**: 21753.30 ✅
- **TP 2RR**: 21735.53 ❌
- **TP 3RR**: 21717.75 ❌
- **TP 4RR**: 21699.98 ❌
- **TP 15RR**: 21504.46 ❌
- **PnL**: -17.77 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 24.74 points

### Trade #848 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 06:45:00
- **FVG 5m**: 21772.10 - 21777.96
- **Entrée**: 21771.08 @ 2025-05-14 07:37:00
- **Stop Loss**: 21788.85
- **Risk**: 17.77 points
- **TP 1RR**: 21753.30 ✅
- **TP 2RR**: 21735.53 ❌
- **TP 3RR**: 21717.75 ❌
- **TP 4RR**: 21699.98 ❌
- **TP 15RR**: 21504.46 ❌
- **PnL**: -17.77 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 24.74 points

### Trade #849 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 07:30:00
- **FVG 5m**: 21759.60 - 21765.21
- **Entrée**: 21753.99 @ 2025-05-14 07:41:00
- **Stop Loss**: 21776.10
- **Risk**: 22.10 points
- **TP 1RR**: 21731.89 ❌
- **TP 2RR**: 21709.78 ❌
- **TP 3RR**: 21687.68 ❌
- **TP 4RR**: 21665.58 ❌
- **TP 15RR**: 21422.44 ❌
- **PnL**: -22.10 points (-1.0R)
- **MFE**: 13.77 points
- **MAE**: 23.21 points

### Trade #850 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 07:30:00
- **FVG 5m**: 21759.60 - 21765.21
- **Entrée**: 21753.99 @ 2025-05-14 07:41:00
- **Stop Loss**: 21776.10
- **Risk**: 22.10 points
- **TP 1RR**: 21731.89 ❌
- **TP 2RR**: 21709.78 ❌
- **TP 3RR**: 21687.68 ❌
- **TP 4RR**: 21665.58 ❌
- **TP 15RR**: 21422.44 ❌
- **PnL**: -22.10 points (-1.0R)
- **MFE**: 13.77 points
- **MAE**: 23.21 points

### Trade #851 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 08:30:00
- **FVG 5m**: 21774.65 - 21797.35
- **Entrée**: 21770.57 @ 2025-05-14 08:44:00
- **Stop Loss**: 21808.25
- **Risk**: 37.68 points
- **TP 1RR**: 21732.89 ✅
- **TP 2RR**: 21695.22 ❌
- **TP 3RR**: 21657.54 ❌
- **TP 4RR**: 21619.86 ❌
- **TP 15RR**: 21205.42 ❌
- **PnL**: -37.68 points (-1.0R)
- **MFE**: 69.11 points
- **MAE**: 45.90 points

### Trade #852 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-14 10:15:00
- **FVG 5m**: 21810.86 - 21813.92
- **Entrée**: 21814.94 @ 2025-05-14 11:29:00
- **Stop Loss**: 21799.96
- **Risk**: 14.99 points
- **TP 1RR**: 21829.93 ✅
- **TP 2RR**: 21844.92 ✅
- **TP 3RR**: 21859.90 ❌
- **TP 4RR**: 21874.89 ❌
- **TP 15RR**: 22039.73 ❌
- **PnL**: -14.99 points (-1.0R)
- **MFE**: 35.19 points
- **MAE**: 19.13 points

### Trade #853 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 22:00:00
- **FVG 5m**: 21823.10 - 21828.20
- **Entrée**: 21821.32 @ 2025-05-14 22:29:00
- **Stop Loss**: 21839.12
- **Risk**: 17.80 points
- **TP 1RR**: 21803.52 ✅
- **TP 2RR**: 21785.72 ✅
- **TP 3RR**: 21767.92 ✅
- **TP 4RR**: 21750.12 ✅
- **TP 15RR**: 21554.32 ❌
- **PnL**: -17.80 points (-1.0R)
- **MFE**: 203.26 points
- **MAE**: 25.50 points

### Trade #854 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 00:45:00
- **FVG 5m**: 21767.51 - 21775.67
- **Entrée**: 21777.71 @ 2025-05-15 01:13:00
- **Stop Loss**: 21756.62
- **Risk**: 21.08 points
- **TP 1RR**: 21798.79 ✅
- **TP 2RR**: 21819.88 ❌
- **TP 3RR**: 21840.96 ❌
- **TP 4RR**: 21862.05 ❌
- **TP 15RR**: 22093.98 ❌
- **PnL**: -21.08 points (-1.0R)
- **MFE**: 22.44 points
- **MAE**: 24.74 points

### Trade #855 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 03:15:00
- **FVG 5m**: 21635.41 - 21637.70
- **Entrée**: 21638.47 @ 2025-05-15 04:16:00
- **Stop Loss**: 21624.59
- **Risk**: 13.88 points
- **TP 1RR**: 21652.34 ✅
- **TP 2RR**: 21666.22 ✅
- **TP 3RR**: 21680.10 ✅
- **TP 4RR**: 21693.98 ✅
- **TP 15RR**: 21846.64 ✅
- **PnL**: 208.17 points (15.0R)
- **MFE**: 208.36 points
- **MAE**: 8.16 points

### Trade #856 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 04:15:00
- **FVG 5m**: 21656.32 - 21664.73
- **Entrée**: 21669.58 @ 2025-05-15 04:28:00
- **Stop Loss**: 21645.49
- **Risk**: 24.09 points
- **TP 1RR**: 21693.67 ✅
- **TP 2RR**: 21717.76 ✅
- **TP 3RR**: 21741.85 ✅
- **TP 4RR**: 21765.94 ✅
- **TP 15RR**: 22030.92 ❌
- **PnL**: -24.09 points (-1.0R)
- **MFE**: 293.03 points
- **MAE**: 33.92 points

### Trade #857 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 04:45:00
- **FVG 5m**: 21683.86 - 21692.79
- **Entrée**: 21696.10 @ 2025-05-15 06:01:00
- **Stop Loss**: 21673.02
- **Risk**: 23.08 points
- **TP 1RR**: 21719.18 ✅
- **TP 2RR**: 21742.27 ❌
- **TP 3RR**: 21765.35 ❌
- **TP 4RR**: 21788.43 ❌
- **TP 15RR**: 22042.35 ❌
- **PnL**: -23.08 points (-1.0R)
- **MFE**: 33.41 points
- **MAE**: 32.90 points

### Trade #858 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 04:45:00
- **FVG 5m**: 21683.86 - 21692.79
- **Entrée**: 21696.10 @ 2025-05-15 06:01:00
- **Stop Loss**: 21673.02
- **Risk**: 23.08 points
- **TP 1RR**: 21719.18 ✅
- **TP 2RR**: 21742.27 ❌
- **TP 3RR**: 21765.35 ❌
- **TP 4RR**: 21788.43 ❌
- **TP 15RR**: 22042.35 ❌
- **PnL**: -23.08 points (-1.0R)
- **MFE**: 33.41 points
- **MAE**: 32.90 points

### Trade #859 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 06:00:00
- **FVG 5m**: 21707.07 - 21713.70
- **Entrée**: 21714.97 @ 2025-05-15 06:26:00
- **Stop Loss**: 21696.21
- **Risk**: 18.76 points
- **TP 1RR**: 21733.73 ❌
- **TP 2RR**: 21752.49 ❌
- **TP 3RR**: 21771.25 ❌
- **TP 4RR**: 21790.01 ❌
- **TP 15RR**: 21996.36 ❌
- **PnL**: -18.76 points (-1.0R)
- **MFE**: 14.54 points
- **MAE**: 19.64 points

### Trade #860 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 10:00:00
- **FVG 5m**: 21809.84 - 21818.26
- **Entrée**: 21820.55 @ 2025-05-15 10:17:00
- **Stop Loss**: 21798.94
- **Risk**: 21.62 points
- **TP 1RR**: 21842.17 ✅
- **TP 2RR**: 21863.79 ✅
- **TP 3RR**: 21885.40 ✅
- **TP 4RR**: 21907.02 ✅
- **TP 15RR**: 22144.79 ❌
- **PnL**: -21.62 points (-1.0R)
- **MFE**: 142.05 points
- **MAE**: 25.50 points

### Trade #861 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-15 10:15:00
- **FVG 5m**: 21934.81 - 21940.42
- **Entrée**: 21933.28 @ 2025-05-15 12:32:00
- **Stop Loss**: 21951.39
- **Risk**: 18.11 points
- **TP 1RR**: 21915.16 ✅
- **TP 2RR**: 21897.05 ✅
- **TP 3RR**: 21878.94 ✅
- **TP 4RR**: 21860.83 ✅
- **TP 15RR**: 21661.61 ✅
- **PnL**: 271.66 points (15.0R)
- **MFE**: 273.39 points
- **MAE**: 11.22 points

### Trade #862 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-15 15:00:00
- **FVG 5m**: 21826.42 - 21830.50
- **Entrée**: 21814.69 @ 2025-05-15 17:00:00
- **Stop Loss**: 21841.42
- **Risk**: 26.73 points
- **TP 1RR**: 21787.96 ❌
- **TP 2RR**: 21761.23 ❌
- **TP 3RR**: 21734.51 ❌
- **TP 4RR**: 21707.78 ❌
- **TP 15RR**: 21413.79 ❌
- **PnL**: -26.73 points (-1.0R)
- **MFE**: 5.36 points
- **MAE**: 29.84 points

### Trade #863 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 02:00:00
- **FVG 5m**: 21815.71 - 21821.57
- **Entrée**: 21824.12 @ 2025-05-16 02:12:00
- **Stop Loss**: 21804.80
- **Risk**: 19.32 points
- **TP 1RR**: 21843.45 ✅
- **TP 2RR**: 21862.77 ✅
- **TP 3RR**: 21882.10 ✅
- **TP 4RR**: 21901.42 ✅
- **TP 15RR**: 22113.98 ❌
- **PnL**: -19.32 points (-1.0R)
- **MFE**: 112.98 points
- **MAE**: 19.38 points

### Trade #864 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 02:45:00
- **FVG 5m**: 21884.06 - 21888.65
- **Entrée**: 21882.02 @ 2025-05-16 04:33:00
- **Stop Loss**: 21899.59
- **Risk**: 17.58 points
- **TP 1RR**: 21864.44 ✅
- **TP 2RR**: 21846.87 ❌
- **TP 3RR**: 21829.29 ❌
- **TP 4RR**: 21811.72 ❌
- **TP 15RR**: 21618.39 ❌
- **PnL**: -17.58 points (-1.0R)
- **MFE**: 20.66 points
- **MAE**: 18.11 points

### Trade #865 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 06:15:00
- **FVG 5m**: 21878.19 - 21885.33
- **Entrée**: 21887.12 @ 2025-05-16 08:06:00
- **Stop Loss**: 21867.25
- **Risk**: 19.87 points
- **TP 1RR**: 21906.98 ✅
- **TP 2RR**: 21926.85 ✅
- **TP 3RR**: 21946.71 ❌
- **TP 4RR**: 21966.58 ❌
- **TP 15RR**: 22185.09 ❌
- **PnL**: -19.87 points (-1.0R)
- **MFE**: 49.99 points
- **MAE**: 23.46 points

### Trade #866 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 07:30:00
- **FVG 5m**: 21845.04 - 21858.55
- **Entrée**: 21843.25 @ 2025-05-16 09:29:00
- **Stop Loss**: 21869.48
- **Risk**: 26.23 points
- **TP 1RR**: 21817.02 ✅
- **TP 2RR**: 21790.79 ✅
- **TP 3RR**: 21764.56 ✅
- **TP 4RR**: 21738.33 ❌
- **TP 15RR**: 21449.79 ❌
- **PnL**: -26.23 points (-1.0R)
- **MFE**: 94.36 points
- **MAE**: 31.11 points

### Trade #867 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 08:30:00
- **FVG 5m**: 21845.04 - 21858.55
- **Entrée**: 21843.25 @ 2025-05-16 09:29:00
- **Stop Loss**: 21869.48
- **Risk**: 26.23 points
- **TP 1RR**: 21817.02 ✅
- **TP 2RR**: 21790.79 ✅
- **TP 3RR**: 21764.56 ✅
- **TP 4RR**: 21738.33 ❌
- **TP 15RR**: 21449.79 ❌
- **PnL**: -26.23 points (-1.0R)
- **MFE**: 94.36 points
- **MAE**: 31.11 points

### Trade #868 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 08:30:00
- **FVG 5m**: 21845.04 - 21858.55
- **Entrée**: 21843.25 @ 2025-05-16 09:29:00
- **Stop Loss**: 21869.48
- **Risk**: 26.23 points
- **TP 1RR**: 21817.02 ✅
- **TP 2RR**: 21790.79 ✅
- **TP 3RR**: 21764.56 ✅
- **TP 4RR**: 21738.33 ❌
- **TP 15RR**: 21449.79 ❌
- **PnL**: -26.23 points (-1.0R)
- **MFE**: 94.36 points
- **MAE**: 31.11 points

### Trade #869 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 09:45:00
- **FVG 5m**: 21830.50 - 21839.43
- **Entrée**: 21846.31 @ 2025-05-16 10:31:00
- **Stop Loss**: 21819.58
- **Risk**: 26.73 points
- **TP 1RR**: 21873.04 ✅
- **TP 2RR**: 21899.77 ✅
- **TP 3RR**: 21926.49 ✅
- **TP 4RR**: 21953.22 ❌
- **TP 15RR**: 22247.21 ❌
- **PnL**: -26.73 points (-1.0R)
- **MFE**: 98.19 points
- **MAE**: 29.84 points

### Trade #870 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 09:45:00
- **FVG 5m**: 21830.50 - 21839.43
- **Entrée**: 21846.31 @ 2025-05-16 10:31:00
- **Stop Loss**: 21819.58
- **Risk**: 26.73 points
- **TP 1RR**: 21873.04 ✅
- **TP 2RR**: 21899.77 ✅
- **TP 3RR**: 21926.49 ✅
- **TP 4RR**: 21953.22 ❌
- **TP 15RR**: 22247.21 ❌
- **PnL**: -26.73 points (-1.0R)
- **MFE**: 98.19 points
- **MAE**: 29.84 points

### Trade #871 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-18 17:00:00
- **FVG 5m**: 21763.94 - 21767.76
- **Entrée**: 21769.55 @ 2025-05-18 17:46:00
- **Stop Loss**: 21753.06
- **Risk**: 16.49 points
- **TP 1RR**: 21786.04 ✅
- **TP 2RR**: 21802.53 ✅
- **TP 3RR**: 21819.03 ✅
- **TP 4RR**: 21835.52 ✅
- **TP 15RR**: 22016.94 ❌
- **PnL**: -16.49 points (-1.0R)
- **MFE**: 79.06 points
- **MAE**: 22.70 points

### Trade #872 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-18 19:45:00
- **FVG 5m**: 21707.83 - 21710.64
- **Entrée**: 21714.21 @ 2025-05-18 21:21:00
- **Stop Loss**: 21696.98
- **Risk**: 17.23 points
- **TP 1RR**: 21731.44 ❌
- **TP 2RR**: 21748.67 ❌
- **TP 3RR**: 21765.90 ❌
- **TP 4RR**: 21783.13 ❌
- **TP 15RR**: 21972.65 ❌
- **PnL**: -17.23 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 18.87 points

### Trade #873 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 02:15:00
- **FVG 5m**: 21566.80 - 21571.14
- **Entrée**: 21574.45 @ 2025-05-19 04:16:00
- **Stop Loss**: 21556.02
- **Risk**: 18.43 points
- **TP 1RR**: 21592.89 ✅
- **TP 2RR**: 21611.32 ❌
- **TP 3RR**: 21629.76 ❌
- **TP 4RR**: 21648.19 ❌
- **TP 15RR**: 21850.97 ❌
- **PnL**: -18.43 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 19.13 points

### Trade #874 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 02:15:00
- **FVG 5m**: 21566.80 - 21571.14
- **Entrée**: 21574.45 @ 2025-05-19 04:16:00
- **Stop Loss**: 21556.02
- **Risk**: 18.43 points
- **TP 1RR**: 21592.89 ✅
- **TP 2RR**: 21611.32 ❌
- **TP 3RR**: 21629.76 ❌
- **TP 4RR**: 21648.19 ❌
- **TP 15RR**: 21850.97 ❌
- **PnL**: -18.43 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 19.13 points

### Trade #875 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 08:30:00
- **FVG 5m**: 21740.48 - 21745.32
- **Entrée**: 21745.58 @ 2025-05-19 08:42:00
- **Stop Loss**: 21729.61
- **Risk**: 15.97 points
- **TP 1RR**: 21761.55 ✅
- **TP 2RR**: 21777.52 ✅
- **TP 3RR**: 21793.49 ✅
- **TP 4RR**: 21809.46 ✅
- **TP 15RR**: 21985.14 ✅
- **PnL**: 239.56 points (15.0R)
- **MFE**: 249.93 points
- **MAE**: 2.04 points

### Trade #876 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 08:30:00
- **FVG 5m**: 21740.48 - 21745.32
- **Entrée**: 21745.58 @ 2025-05-19 08:42:00
- **Stop Loss**: 21729.61
- **Risk**: 15.97 points
- **TP 1RR**: 21761.55 ✅
- **TP 2RR**: 21777.52 ✅
- **TP 3RR**: 21793.49 ✅
- **TP 4RR**: 21809.46 ✅
- **TP 15RR**: 21985.14 ✅
- **PnL**: 239.56 points (15.0R)
- **MFE**: 249.93 points
- **MAE**: 2.04 points

### Trade #877 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 09:15:00
- **FVG 5m**: 21844.02 - 21856.77
- **Entrée**: 21835.09 @ 2025-05-19 09:26:00
- **Stop Loss**: 21867.70
- **Risk**: 32.61 points
- **TP 1RR**: 21802.48 ❌
- **TP 2RR**: 21769.88 ❌
- **TP 3RR**: 21737.27 ❌
- **TP 4RR**: 21704.67 ❌
- **TP 15RR**: 21346.01 ❌
- **PnL**: -32.61 points (-1.0R)
- **MFE**: 28.82 points
- **MAE**: 47.43 points

### Trade #878 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 12:15:00
- **FVG 5m**: 21910.58 - 21924.86
- **Entrée**: 21910.32 @ 2025-05-19 13:14:00
- **Stop Loss**: 21935.82
- **Risk**: 25.50 points
- **TP 1RR**: 21884.82 ✅
- **TP 2RR**: 21859.33 ❌
- **TP 3RR**: 21833.83 ❌
- **TP 4RR**: 21808.33 ❌
- **TP 15RR**: 21527.84 ❌
- **PnL**: -25.50 points (-1.0R)
- **MFE**: 29.33 points
- **MAE**: 28.82 points

### Trade #879 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 12:45:00
- **FVG 5m**: 21910.58 - 21924.86
- **Entrée**: 21910.32 @ 2025-05-19 13:14:00
- **Stop Loss**: 21935.82
- **Risk**: 25.50 points
- **TP 1RR**: 21884.82 ✅
- **TP 2RR**: 21859.33 ❌
- **TP 3RR**: 21833.83 ❌
- **TP 4RR**: 21808.33 ❌
- **TP 15RR**: 21527.84 ❌
- **PnL**: -25.50 points (-1.0R)
- **MFE**: 29.33 points
- **MAE**: 28.82 points

### Trade #880 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 12:45:00
- **FVG 5m**: 21910.58 - 21924.86
- **Entrée**: 21910.32 @ 2025-05-19 13:14:00
- **Stop Loss**: 21935.82
- **Risk**: 25.50 points
- **TP 1RR**: 21884.82 ✅
- **TP 2RR**: 21859.33 ❌
- **TP 3RR**: 21833.83 ❌
- **TP 4RR**: 21808.33 ❌
- **TP 15RR**: 21527.84 ❌
- **PnL**: -25.50 points (-1.0R)
- **MFE**: 29.33 points
- **MAE**: 28.82 points

### Trade #881 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 19:00:00
- **FVG 5m**: 21962.60 - 21967.96
- **Entrée**: 21961.33 @ 2025-05-19 19:49:00
- **Stop Loss**: 21978.94
- **Risk**: 17.61 points
- **TP 1RR**: 21943.71 ✅
- **TP 2RR**: 21926.10 ✅
- **TP 3RR**: 21908.48 ✅
- **TP 4RR**: 21890.87 ✅
- **TP 15RR**: 21697.11 ✅
- **PnL**: 264.22 points (15.0R)
- **MFE**: 268.29 points
- **MAE**: 1.28 points

### Trade #882 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 22:30:00
- **FVG 5m**: 21865.95 - 21875.89
- **Entrée**: 21876.66 @ 2025-05-19 23:53:00
- **Stop Loss**: 21855.02
- **Risk**: 21.64 points
- **TP 1RR**: 21898.30 ✅
- **TP 2RR**: 21919.95 ❌
- **TP 3RR**: 21941.59 ❌
- **TP 4RR**: 21963.24 ❌
- **TP 15RR**: 22201.32 ❌
- **PnL**: -21.64 points (-1.0R)
- **MFE**: 42.33 points
- **MAE**: 29.84 points

### Trade #883 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-20 01:30:00
- **FVG 5m**: 21876.66 - 21887.12
- **Entrée**: 21890.43 @ 2025-05-20 02:22:00
- **Stop Loss**: 21865.72
- **Risk**: 24.71 points
- **TP 1RR**: 21915.14 ❌
- **TP 2RR**: 21939.85 ❌
- **TP 3RR**: 21964.56 ❌
- **TP 4RR**: 21989.27 ❌
- **TP 15RR**: 22261.08 ❌
- **PnL**: -24.71 points (-1.0R)
- **MFE**: 22.44 points
- **MAE**: 24.99 points

### Trade #884 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-20 08:45:00
- **FVG 5m**: 21824.12 - 21826.67
- **Entrée**: 21829.99 @ 2025-05-20 09:17:00
- **Stop Loss**: 21813.21
- **Risk**: 16.78 points
- **TP 1RR**: 21846.77 ✅
- **TP 2RR**: 21863.55 ❌
- **TP 3RR**: 21880.32 ❌
- **TP 4RR**: 21897.10 ❌
- **TP 15RR**: 22081.66 ❌
- **PnL**: -16.78 points (-1.0R)
- **MFE**: 27.80 points
- **MAE**: 21.68 points

### Trade #885 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-20 13:30:00
- **FVG 5m**: 21787.66 - 21791.74
- **Entrée**: 21794.03 @ 2025-05-20 14:19:00
- **Stop Loss**: 21776.76
- **Risk**: 17.27 points
- **TP 1RR**: 21811.30 ✅
- **TP 2RR**: 21828.57 ✅
- **TP 3RR**: 21845.84 ✅
- **TP 4RR**: 21863.11 ✅
- **TP 15RR**: 22053.07 ❌
- **PnL**: -17.27 points (-1.0R)
- **MFE**: 89.26 points
- **MAE**: 22.95 points

### Trade #886 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 02:45:00
- **FVG 5m**: 21739.71 - 21742.01
- **Entrée**: 21742.77 @ 2025-05-21 03:51:00
- **Stop Loss**: 21728.84
- **Risk**: 13.93 points
- **TP 1RR**: 21756.70 ✅
- **TP 2RR**: 21770.63 ❌
- **TP 3RR**: 21784.56 ❌
- **TP 4RR**: 21798.49 ❌
- **TP 15RR**: 21951.72 ❌
- **PnL**: -13.93 points (-1.0R)
- **MFE**: 22.19 points
- **MAE**: 18.87 points

### Trade #887 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 04:30:00
- **FVG 5m**: 21709.36 - 21723.13
- **Entrée**: 21703.75 @ 2025-05-21 04:42:00
- **Stop Loss**: 21734.00
- **Risk**: 30.24 points
- **TP 1RR**: 21673.51 ✅
- **TP 2RR**: 21643.26 ❌
- **TP 3RR**: 21613.02 ❌
- **TP 4RR**: 21582.78 ❌
- **TP 15RR**: 21250.10 ❌
- **PnL**: -30.24 points (-1.0R)
- **MFE**: 47.18 points
- **MAE**: 34.17 points

### Trade #888 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 05:45:00
- **FVG 5m**: 21732.57 - 21737.93
- **Entrée**: 21742.52 @ 2025-05-21 06:08:00
- **Stop Loss**: 21721.70
- **Risk**: 20.81 points
- **TP 1RR**: 21763.33 ✅
- **TP 2RR**: 21784.14 ✅
- **TP 3RR**: 21804.95 ❌
- **TP 4RR**: 21825.77 ❌
- **TP 15RR**: 22054.70 ❌
- **PnL**: -20.81 points (-1.0R)
- **MFE**: 42.59 points
- **MAE**: 22.44 points

### Trade #889 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 05:45:00
- **FVG 5m**: 21732.57 - 21737.93
- **Entrée**: 21742.52 @ 2025-05-21 06:08:00
- **Stop Loss**: 21721.70
- **Risk**: 20.81 points
- **TP 1RR**: 21763.33 ✅
- **TP 2RR**: 21784.14 ✅
- **TP 3RR**: 21804.95 ❌
- **TP 4RR**: 21825.77 ❌
- **TP 15RR**: 22054.70 ❌
- **PnL**: -20.81 points (-1.0R)
- **MFE**: 42.59 points
- **MAE**: 22.44 points

### Trade #890 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 11:45:00
- **FVG 5m**: 21955.97 - 21974.33
- **Entrée**: 21955.72 @ 2025-05-21 11:56:00
- **Stop Loss**: 21985.32
- **Risk**: 29.60 points
- **TP 1RR**: 21926.11 ✅
- **TP 2RR**: 21896.51 ✅
- **TP 3RR**: 21866.91 ✅
- **TP 4RR**: 21837.30 ✅
- **TP 15RR**: 21511.66 ✅
- **PnL**: 444.06 points (15.0R)
- **MFE**: 445.28 points
- **MAE**: 8.16 points

### Trade #891 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21889.41 - 21897.57
- **Entrée**: 21886.10 @ 2025-05-21 12:11:00
- **Stop Loss**: 21908.52
- **Risk**: 22.42 points
- **TP 1RR**: 21863.67 ✅
- **TP 2RR**: 21841.25 ✅
- **TP 3RR**: 21818.82 ✅
- **TP 4RR**: 21796.40 ✅
- **TP 15RR**: 21549.72 ✅
- **PnL**: 336.37 points (15.0R)
- **MFE**: 350.66 points
- **MAE**: 17.60 points

### Trade #892 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21889.41 - 21897.57
- **Entrée**: 21886.10 @ 2025-05-21 12:11:00
- **Stop Loss**: 21908.52
- **Risk**: 22.42 points
- **TP 1RR**: 21863.67 ✅
- **TP 2RR**: 21841.25 ✅
- **TP 3RR**: 21818.82 ✅
- **TP 4RR**: 21796.40 ✅
- **TP 15RR**: 21549.72 ✅
- **PnL**: 336.37 points (15.0R)
- **MFE**: 350.66 points
- **MAE**: 17.60 points

### Trade #893 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21889.41 - 21897.57
- **Entrée**: 21886.10 @ 2025-05-21 12:11:00
- **Stop Loss**: 21908.52
- **Risk**: 22.42 points
- **TP 1RR**: 21863.67 ✅
- **TP 2RR**: 21841.25 ✅
- **TP 3RR**: 21818.82 ✅
- **TP 4RR**: 21796.40 ✅
- **TP 15RR**: 21549.72 ✅
- **PnL**: 336.37 points (15.0R)
- **MFE**: 350.66 points
- **MAE**: 17.60 points

### Trade #894 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21889.41 - 21897.57
- **Entrée**: 21886.10 @ 2025-05-21 12:11:00
- **Stop Loss**: 21908.52
- **Risk**: 22.42 points
- **TP 1RR**: 21863.67 ✅
- **TP 2RR**: 21841.25 ✅
- **TP 3RR**: 21818.82 ✅
- **TP 4RR**: 21796.40 ✅
- **TP 15RR**: 21549.72 ✅
- **PnL**: 336.37 points (15.0R)
- **MFE**: 350.66 points
- **MAE**: 17.60 points

### Trade #895 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21654.28 - 21675.44
- **Entrée**: 21637.70 @ 2025-05-21 13:49:00
- **Stop Loss**: 21686.28
- **Risk**: 48.58 points
- **TP 1RR**: 21589.12 ✅
- **TP 2RR**: 21540.54 ✅
- **TP 3RR**: 21491.96 ✅
- **TP 4RR**: 21443.37 ❌
- **TP 15RR**: 20908.98 ❌
- **PnL**: -48.58 points (-1.0R)
- **MFE**: 174.69 points
- **MAE**: 49.73 points

### Trade #896 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21654.28 - 21675.44
- **Entrée**: 21637.70 @ 2025-05-21 13:49:00
- **Stop Loss**: 21686.28
- **Risk**: 48.58 points
- **TP 1RR**: 21589.12 ✅
- **TP 2RR**: 21540.54 ✅
- **TP 3RR**: 21491.96 ✅
- **TP 4RR**: 21443.37 ❌
- **TP 15RR**: 20908.98 ❌
- **PnL**: -48.58 points (-1.0R)
- **MFE**: 174.69 points
- **MAE**: 49.73 points

### Trade #897 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21654.28 - 21675.44
- **Entrée**: 21637.70 @ 2025-05-21 13:49:00
- **Stop Loss**: 21686.28
- **Risk**: 48.58 points
- **TP 1RR**: 21589.12 ✅
- **TP 2RR**: 21540.54 ✅
- **TP 3RR**: 21491.96 ✅
- **TP 4RR**: 21443.37 ❌
- **TP 15RR**: 20908.98 ❌
- **PnL**: -48.58 points (-1.0R)
- **MFE**: 174.69 points
- **MAE**: 49.73 points

### Trade #898 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21654.28 - 21675.44
- **Entrée**: 21637.70 @ 2025-05-21 13:49:00
- **Stop Loss**: 21686.28
- **Risk**: 48.58 points
- **TP 1RR**: 21589.12 ✅
- **TP 2RR**: 21540.54 ✅
- **TP 3RR**: 21491.96 ✅
- **TP 4RR**: 21443.37 ❌
- **TP 15RR**: 20908.98 ❌
- **PnL**: -48.58 points (-1.0R)
- **MFE**: 174.69 points
- **MAE**: 49.73 points

### Trade #899 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 12:30:00
- **FVG 5m**: 21535.43 - 21560.17
- **Entrée**: 21560.94 @ 2025-05-21 14:32:00
- **Stop Loss**: 21524.67
- **Risk**: 36.27 points
- **TP 1RR**: 21597.21 ✅
- **TP 2RR**: 21633.48 ✅
- **TP 3RR**: 21669.75 ✅
- **TP 4RR**: 21706.02 ❌
- **TP 15RR**: 22104.99 ❌
- **PnL**: -36.27 points (-1.0R)
- **MFE**: 109.66 points
- **MAE**: 61.97 points

### Trade #900 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 12:30:00
- **FVG 5m**: 21535.43 - 21560.17
- **Entrée**: 21560.94 @ 2025-05-21 14:32:00
- **Stop Loss**: 21524.67
- **Risk**: 36.27 points
- **TP 1RR**: 21597.21 ✅
- **TP 2RR**: 21633.48 ✅
- **TP 3RR**: 21669.75 ✅
- **TP 4RR**: 21706.02 ❌
- **TP 15RR**: 22104.99 ❌
- **PnL**: -36.27 points (-1.0R)
- **MFE**: 109.66 points
- **MAE**: 61.97 points

### Trade #901 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 14:00:00
- **FVG 5m**: 21535.43 - 21560.17
- **Entrée**: 21560.94 @ 2025-05-21 14:32:00
- **Stop Loss**: 21524.67
- **Risk**: 36.27 points
- **TP 1RR**: 21597.21 ✅
- **TP 2RR**: 21633.48 ✅
- **TP 3RR**: 21669.75 ✅
- **TP 4RR**: 21706.02 ❌
- **TP 15RR**: 22104.99 ❌
- **PnL**: -36.27 points (-1.0R)
- **MFE**: 109.66 points
- **MAE**: 61.97 points

### Trade #902 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 01:00:00
- **FVG 5m**: 21628.01 - 21633.87
- **Entrée**: 21627.24 @ 2025-05-22 02:12:00
- **Stop Loss**: 21644.69
- **Risk**: 17.45 points
- **TP 1RR**: 21609.80 ✅
- **TP 2RR**: 21592.35 ❌
- **TP 3RR**: 21574.90 ❌
- **TP 4RR**: 21557.45 ❌
- **TP 15RR**: 21365.53 ❌
- **PnL**: -17.45 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 22.44 points

### Trade #903 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 02:00:00
- **FVG 5m**: 21628.01 - 21633.87
- **Entrée**: 21627.24 @ 2025-05-22 02:12:00
- **Stop Loss**: 21644.69
- **Risk**: 17.45 points
- **TP 1RR**: 21609.80 ✅
- **TP 2RR**: 21592.35 ❌
- **TP 3RR**: 21574.90 ❌
- **TP 4RR**: 21557.45 ❌
- **TP 15RR**: 21365.53 ❌
- **PnL**: -17.45 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 22.44 points

### Trade #904 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 06:00:00
- **FVG 5m**: 21636.43 - 21640.76
- **Entrée**: 21631.83 @ 2025-05-22 06:11:00
- **Stop Loss**: 21651.58
- **Risk**: 19.75 points
- **TP 1RR**: 21612.09 ✅
- **TP 2RR**: 21592.34 ✅
- **TP 3RR**: 21572.60 ✅
- **TP 4RR**: 21552.85 ✅
- **TP 15RR**: 21335.64 ❌
- **PnL**: -19.75 points (-1.0R)
- **MFE**: 168.83 points
- **MAE**: 21.68 points

### Trade #905 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:30:00
- **FVG 5m**: 21542.83 - 21545.64
- **Entrée**: 21555.07 @ 2025-05-22 07:43:00
- **Stop Loss**: 21532.06
- **Risk**: 23.01 points
- **TP 1RR**: 21578.08 ✅
- **TP 2RR**: 21601.10 ✅
- **TP 3RR**: 21624.11 ✅
- **TP 4RR**: 21647.12 ✅
- **TP 15RR**: 21900.26 ❌
- **PnL**: -23.01 points (-1.0R)
- **MFE**: 211.42 points
- **MAE**: 29.33 points

### Trade #906 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:45:00
- **FVG 5m**: 21600.72 - 21617.30
- **Entrée**: 21635.41 @ 2025-05-22 08:00:00
- **Stop Loss**: 21589.92
- **Risk**: 45.48 points
- **TP 1RR**: 21680.89 ❌
- **TP 2RR**: 21726.37 ❌
- **TP 3RR**: 21771.86 ❌
- **TP 4RR**: 21817.34 ❌
- **TP 15RR**: 22317.66 ❌
- **PnL**: -45.48 points (-1.0R)
- **MFE**: 18.11 points
- **MAE**: 46.67 points

### Trade #907 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:45:00
- **FVG 5m**: 21600.72 - 21617.30
- **Entrée**: 21635.41 @ 2025-05-22 08:00:00
- **Stop Loss**: 21589.92
- **Risk**: 45.48 points
- **TP 1RR**: 21680.89 ❌
- **TP 2RR**: 21726.37 ❌
- **TP 3RR**: 21771.86 ❌
- **TP 4RR**: 21817.34 ❌
- **TP 15RR**: 22317.66 ❌
- **PnL**: -45.48 points (-1.0R)
- **MFE**: 18.11 points
- **MAE**: 46.67 points

### Trade #908 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:45:00
- **FVG 5m**: 21600.72 - 21617.30
- **Entrée**: 21635.41 @ 2025-05-22 08:00:00
- **Stop Loss**: 21589.92
- **Risk**: 45.48 points
- **TP 1RR**: 21680.89 ❌
- **TP 2RR**: 21726.37 ❌
- **TP 3RR**: 21771.86 ❌
- **TP 4RR**: 21817.34 ❌
- **TP 15RR**: 22317.66 ❌
- **PnL**: -45.48 points (-1.0R)
- **MFE**: 18.11 points
- **MAE**: 46.67 points

### Trade #909 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 09:15:00
- **FVG 5m**: 21708.34 - 21713.70
- **Entrée**: 21708.09 @ 2025-05-22 11:21:00
- **Stop Loss**: 21724.55
- **Risk**: 16.47 points
- **TP 1RR**: 21691.62 ✅
- **TP 2RR**: 21675.15 ✅
- **TP 3RR**: 21658.69 ✅
- **TP 4RR**: 21642.22 ✅
- **TP 15RR**: 21461.08 ❌
- **PnL**: -16.47 points (-1.0R)
- **MFE**: 85.69 points
- **MAE**: 23.46 points

### Trade #910 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 14:00:00
- **FVG 5m**: 21714.97 - 21722.11
- **Entrée**: 21712.93 @ 2025-05-22 14:38:00
- **Stop Loss**: 21732.98
- **Risk**: 20.04 points
- **TP 1RR**: 21692.89 ✅
- **TP 2RR**: 21672.85 ✅
- **TP 3RR**: 21652.81 ✅
- **TP 4RR**: 21632.77 ✅
- **TP 15RR**: 21412.30 ✅
- **PnL**: 300.63 points (15.0R)
- **MFE**: 400.65 points
- **MAE**: 10.97 points

### Trade #911 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 19:45:00
- **FVG 5m**: 21587.72 - 21595.37
- **Entrée**: 21597.41 @ 2025-05-22 21:03:00
- **Stop Loss**: 21576.92
- **Risk**: 20.48 points
- **TP 1RR**: 21617.89 ✅
- **TP 2RR**: 21638.38 ❌
- **TP 3RR**: 21658.86 ❌
- **TP 4RR**: 21679.35 ❌
- **TP 15RR**: 21904.68 ❌
- **PnL**: -20.48 points (-1.0R)
- **MFE**: 37.49 points
- **MAE**: 24.99 points

### Trade #912 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 23:45:00
- **FVG 5m**: 21579.04 - 21586.19
- **Entrée**: 21587.46 @ 2025-05-23 00:02:00
- **Stop Loss**: 21568.25
- **Risk**: 19.21 points
- **TP 1RR**: 21606.67 ✅
- **TP 2RR**: 21625.87 ❌
- **TP 3RR**: 21645.08 ❌
- **TP 4RR**: 21664.28 ❌
- **TP 15RR**: 21875.54 ❌
- **PnL**: -19.21 points (-1.0R)
- **MFE**: 19.89 points
- **MAE**: 19.38 points

### Trade #913 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-23 00:00:00
- **FVG 5m**: 21536.20 - 21541.56
- **Entrée**: 21546.15 @ 2025-05-23 01:26:00
- **Stop Loss**: 21525.43
- **Risk**: 20.71 points
- **TP 1RR**: 21566.86 ✅
- **TP 2RR**: 21587.57 ✅
- **TP 3RR**: 21608.29 ✅
- **TP 4RR**: 21629.00 ✅
- **TP 15RR**: 21856.86 ❌
- **PnL**: -20.71 points (-1.0R)
- **MFE**: 111.70 points
- **MAE**: 53.05 points

### Trade #914 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 03:30:00
- **FVG 5m**: 21608.63 - 21611.69
- **Entrée**: 21604.29 @ 2025-05-23 04:01:00
- **Stop Loss**: 21622.49
- **Risk**: 18.20 points
- **TP 1RR**: 21586.09 ✅
- **TP 2RR**: 21567.89 ✅
- **TP 3RR**: 21549.69 ✅
- **TP 4RR**: 21531.49 ✅
- **TP 15RR**: 21331.27 ✅
- **PnL**: 273.02 points (15.0R)
- **MFE**: 292.01 points
- **MAE**: 13.77 points

### Trade #915 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 03:30:00
- **FVG 5m**: 21608.63 - 21611.69
- **Entrée**: 21604.29 @ 2025-05-23 04:01:00
- **Stop Loss**: 21622.49
- **Risk**: 18.20 points
- **TP 1RR**: 21586.09 ✅
- **TP 2RR**: 21567.89 ✅
- **TP 3RR**: 21549.69 ✅
- **TP 4RR**: 21531.49 ✅
- **TP 15RR**: 21331.27 ✅
- **PnL**: 273.02 points (15.0R)
- **MFE**: 292.01 points
- **MAE**: 13.77 points

### Trade #916 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-23 04:30:00
- **FVG 5m**: 21592.05 - 21606.59
- **Entrée**: 21609.90 @ 2025-05-23 04:55:00
- **Stop Loss**: 21581.25
- **Risk**: 28.65 points
- **TP 1RR**: 21638.55 ❌
- **TP 2RR**: 21667.20 ❌
- **TP 3RR**: 21695.85 ❌
- **TP 4RR**: 21724.49 ❌
- **TP 15RR**: 22039.62 ❌
- **PnL**: -28.65 points (-1.0R)
- **MFE**: 7.40 points
- **MAE**: 29.58 points

### Trade #917 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 06:30:00
- **FVG 5m**: 21371.96 - 21500.24
- **Entrée**: 21365.33 @ 2025-05-23 06:44:00
- **Stop Loss**: 21510.99
- **Risk**: 145.66 points
- **TP 1RR**: 21219.67 ✅
- **TP 2RR**: 21074.01 ❌
- **TP 3RR**: 20928.36 ❌
- **TP 4RR**: 20782.70 ❌
- **TP 15RR**: 19180.45 ❌
- **PnL**: -145.66 points (-1.0R)
- **MFE**: 221.62 points
- **MAE**: 182.09 points

### Trade #918 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 06:30:00
- **FVG 5m**: 21371.96 - 21500.24
- **Entrée**: 21365.33 @ 2025-05-23 06:44:00
- **Stop Loss**: 21510.99
- **Risk**: 145.66 points
- **TP 1RR**: 21219.67 ✅
- **TP 2RR**: 21074.01 ❌
- **TP 3RR**: 20928.36 ❌
- **TP 4RR**: 20782.70 ❌
- **TP 15RR**: 19180.45 ❌
- **PnL**: -145.66 points (-1.0R)
- **MFE**: 221.62 points
- **MAE**: 182.09 points

### Trade #919 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 06:45:00
- **FVG 5m**: 21258.99 - 21268.42
- **Entrée**: 21243.68 @ 2025-05-23 06:57:00
- **Stop Loss**: 21279.06
- **Risk**: 35.37 points
- **TP 1RR**: 21208.31 ✅
- **TP 2RR**: 21172.94 ✅
- **TP 3RR**: 21137.57 ❌
- **TP 4RR**: 21102.20 ❌
- **TP 15RR**: 20713.11 ❌
- **PnL**: -35.37 points (-1.0R)
- **MFE**: 99.97 points
- **MAE**: 52.03 points

### Trade #920 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-23 06:45:00
- **FVG 5m**: 21201.35 - 21209.00
- **Entrée**: 21215.63 @ 2025-05-23 07:28:00
- **Stop Loss**: 21190.75
- **Risk**: 24.88 points
- **TP 1RR**: 21240.51 ✅
- **TP 2RR**: 21265.40 ❌
- **TP 3RR**: 21290.28 ❌
- **TP 4RR**: 21315.16 ❌
- **TP 15RR**: 21588.86 ❌
- **PnL**: -24.88 points (-1.0R)
- **MFE**: 41.82 points
- **MAE**: 29.84 points

### Trade #921 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-23 06:45:00
- **FVG 5m**: 21201.35 - 21209.00
- **Entrée**: 21215.63 @ 2025-05-23 07:28:00
- **Stop Loss**: 21190.75
- **Risk**: 24.88 points
- **TP 1RR**: 21240.51 ✅
- **TP 2RR**: 21265.40 ❌
- **TP 3RR**: 21290.28 ❌
- **TP 4RR**: 21315.16 ❌
- **TP 15RR**: 21588.86 ❌
- **PnL**: -24.88 points (-1.0R)
- **MFE**: 41.82 points
- **MAE**: 29.84 points

### Trade #922 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 10:30:00
- **FVG 5m**: 21379.61 - 21387.01
- **Entrée**: 21366.86 @ 2025-05-23 10:52:00
- **Stop Loss**: 21397.70
- **Risk**: 30.84 points
- **TP 1RR**: 21336.02 ❌
- **TP 2RR**: 21305.18 ❌
- **TP 3RR**: 21274.34 ❌
- **TP 4RR**: 21243.50 ❌
- **TP 15RR**: 20904.25 ❌
- **PnL**: -30.84 points (-1.0R)
- **MFE**: 28.56 points
- **MAE**: 32.64 points

### Trade #923 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 14:45:00
- **FVG 5m**: 21370.94 - 21380.12
- **Entrée**: 21370.18 @ 2025-05-23 15:03:00
- **Stop Loss**: 21390.81
- **Risk**: 20.64 points
- **TP 1RR**: 21349.54 ❌
- **TP 2RR**: 21328.91 ❌
- **TP 3RR**: 21308.27 ❌
- **TP 4RR**: 21287.63 ❌
- **TP 15RR**: 21060.64 ❌
- **PnL**: -20.64 points (-1.0R)
- **MFE**: 18.62 points
- **MAE**: 39.53 points

### Trade #924 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-25 17:00:00
- **FVG 5m**: 21543.85 - 21551.50
- **Entrée**: 21555.58 @ 2025-05-25 17:19:00
- **Stop Loss**: 21533.08
- **Risk**: 22.50 points
- **TP 1RR**: 21578.08 ✅
- **TP 2RR**: 21600.59 ✅
- **TP 3RR**: 21623.09 ✅
- **TP 4RR**: 21645.59 ✅
- **TP 15RR**: 21893.13 ✅
- **PnL**: 337.55 points (15.0R)
- **MFE**: 340.46 points
- **MAE**: 4.08 points

### Trade #925 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-25 17:15:00
- **FVG 5m**: 21580.57 - 21587.72
- **Entrée**: 21588.23 @ 2025-05-25 17:46:00
- **Stop Loss**: 21569.78
- **Risk**: 18.44 points
- **TP 1RR**: 21606.67 ✅
- **TP 2RR**: 21625.11 ✅
- **TP 3RR**: 21643.55 ✅
- **TP 4RR**: 21661.99 ✅
- **TP 15RR**: 21864.84 ❌
- **PnL**: -18.44 points (-1.0R)
- **MFE**: 147.92 points
- **MAE**: 21.68 points

### Trade #926 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-26 01:30:00
- **FVG 5m**: 21680.29 - 21695.59
- **Entrée**: 21676.97 @ 2025-05-26 03:53:00
- **Stop Loss**: 21706.44
- **Risk**: 29.46 points
- **TP 1RR**: 21647.51 ❌
- **TP 2RR**: 21618.04 ❌
- **TP 3RR**: 21588.58 ❌
- **TP 4RR**: 21559.12 ❌
- **TP 15RR**: 21235.00 ❌
- **PnL**: -29.46 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 30.86 points

### Trade #927 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-26 01:30:00
- **FVG 5m**: 21680.29 - 21695.59
- **Entrée**: 21676.97 @ 2025-05-26 03:53:00
- **Stop Loss**: 21706.44
- **Risk**: 29.46 points
- **TP 1RR**: 21647.51 ❌
- **TP 2RR**: 21618.04 ❌
- **TP 3RR**: 21588.58 ❌
- **TP 4RR**: 21559.12 ❌
- **TP 15RR**: 21235.00 ❌
- **PnL**: -29.46 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 30.86 points

### Trade #928 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-26 01:30:00
- **FVG 5m**: 21680.29 - 21695.59
- **Entrée**: 21676.97 @ 2025-05-26 03:53:00
- **Stop Loss**: 21706.44
- **Risk**: 29.46 points
- **TP 1RR**: 21647.51 ❌
- **TP 2RR**: 21618.04 ❌
- **TP 3RR**: 21588.58 ❌
- **TP 4RR**: 21559.12 ❌
- **TP 15RR**: 21235.00 ❌
- **PnL**: -29.46 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 30.86 points

### Trade #929 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-26 08:45:00
- **FVG 5m**: 21674.68 - 21691.00
- **Entrée**: 21674.17 @ 2025-05-26 09:33:00
- **Stop Loss**: 21701.85
- **Risk**: 27.68 points
- **TP 1RR**: 21646.49 ✅
- **TP 2RR**: 21618.81 ❌
- **TP 3RR**: 21591.14 ❌
- **TP 4RR**: 21563.46 ❌
- **TP 15RR**: 21259.01 ❌
- **PnL**: -27.68 points (-1.0R)
- **MFE**: 32.13 points
- **MAE**: 28.56 points

### Trade #930 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-26 10:15:00
- **FVG 5m**: 21668.05 - 21680.29
- **Entrée**: 21680.54 @ 2025-05-26 10:29:00
- **Stop Loss**: 21657.21
- **Risk**: 23.33 points
- **TP 1RR**: 21703.88 ✅
- **TP 2RR**: 21727.21 ❌
- **TP 3RR**: 21750.54 ❌
- **TP 4RR**: 21773.87 ❌
- **TP 15RR**: 22030.50 ❌
- **PnL**: -23.33 points (-1.0R)
- **MFE**: 41.57 points
- **MAE**: 25.76 points

### Trade #931 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-27 00:15:00
- **FVG 5m**: 21608.88 - 21612.96
- **Entrée**: 21617.04 @ 2025-05-27 00:27:00
- **Stop Loss**: 21598.08
- **Risk**: 18.97 points
- **TP 1RR**: 21636.01 ✅
- **TP 2RR**: 21654.97 ✅
- **TP 3RR**: 21673.94 ✅
- **TP 4RR**: 21692.90 ✅
- **TP 15RR**: 21901.52 ✅
- **PnL**: 284.48 points (15.0R)
- **MFE**: 285.37 points
- **MAE**: 4.08 points

### Trade #932 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-27 01:00:00
- **FVG 5m**: 21647.14 - 21655.81
- **Entrée**: 21657.34 @ 2025-05-27 01:19:00
- **Stop Loss**: 21636.31
- **Risk**: 21.02 points
- **TP 1RR**: 21678.36 ✅
- **TP 2RR**: 21699.39 ✅
- **TP 3RR**: 21720.41 ✅
- **TP 4RR**: 21741.44 ✅
- **TP 15RR**: 21972.71 ❌
- **PnL**: -21.02 points (-1.0R)
- **MFE**: 131.85 points
- **MAE**: 26.01 points

### Trade #933 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 02:45:00
- **FVG 5m**: 21765.98 - 21770.31
- **Entrée**: 21760.37 @ 2025-05-27 02:57:00
- **Stop Loss**: 21781.20
- **Risk**: 20.83 points
- **TP 1RR**: 21739.54 ✅
- **TP 2RR**: 21718.71 ❌
- **TP 3RR**: 21697.87 ❌
- **TP 4RR**: 21677.04 ❌
- **TP 15RR**: 21447.90 ❌
- **PnL**: -20.83 points (-1.0R)
- **MFE**: 33.66 points
- **MAE**: 21.17 points

### Trade #934 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 03:15:00
- **FVG 5m**: 21737.93 - 21744.56
- **Entrée**: 21736.91 @ 2025-05-27 03:49:00
- **Stop Loss**: 21755.43
- **Risk**: 18.52 points
- **TP 1RR**: 21718.38 ❌
- **TP 2RR**: 21699.86 ❌
- **TP 3RR**: 21681.34 ❌
- **TP 4RR**: 21662.81 ❌
- **TP 15RR**: 21459.06 ❌
- **PnL**: -18.52 points (-1.0R)
- **MFE**: 10.20 points
- **MAE**: 23.97 points

### Trade #935 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 05:45:00
- **FVG 5m**: 21730.78 - 21734.36
- **Entrée**: 21722.62 @ 2025-05-27 06:00:00
- **Stop Loss**: 21745.22
- **Risk**: 22.60 points
- **TP 1RR**: 21700.03 ✅
- **TP 2RR**: 21677.43 ✅
- **TP 3RR**: 21654.83 ✅
- **TP 4RR**: 21632.23 ✅
- **TP 15RR**: 21383.65 ❌
- **PnL**: -22.60 points (-1.0R)
- **MFE**: 103.80 points
- **MAE**: 34.68 points

### Trade #936 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 07:15:00
- **FVG 5m**: 21712.42 - 21731.04
- **Entrée**: 21694.32 @ 2025-05-27 08:27:00
- **Stop Loss**: 21741.91
- **Risk**: 47.59 points
- **TP 1RR**: 21646.73 ✅
- **TP 2RR**: 21599.14 ❌
- **TP 3RR**: 21551.55 ❌
- **TP 4RR**: 21503.96 ❌
- **TP 15RR**: 20980.48 ❌
- **PnL**: -47.59 points (-1.0R)
- **MFE**: 75.49 points
- **MAE**: 62.99 points

### Trade #937 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 13:30:00
- **FVG 5m**: 21875.64 - 21879.21
- **Entrée**: 21873.85 @ 2025-05-27 13:59:00
- **Stop Loss**: 21890.15
- **Risk**: 16.30 points
- **TP 1RR**: 21857.56 ✅
- **TP 2RR**: 21841.26 ❌
- **TP 3RR**: 21824.97 ❌
- **TP 4RR**: 21808.67 ❌
- **TP 15RR**: 21629.43 ❌
- **PnL**: -16.30 points (-1.0R)
- **MFE**: 29.07 points
- **MAE**: 23.72 points

### Trade #938 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 03:30:00
- **FVG 5m**: 21861.36 - 21863.91
- **Entrée**: 21864.67 @ 2025-05-28 05:01:00
- **Stop Loss**: 21850.43
- **Risk**: 14.25 points
- **TP 1RR**: 21878.92 ✅
- **TP 2RR**: 21893.17 ✅
- **TP 3RR**: 21907.41 ✅
- **TP 4RR**: 21921.66 ✅
- **TP 15RR**: 22078.36 ❌
- **PnL**: -14.25 points (-1.0R)
- **MFE**: 136.44 points
- **MAE**: 33.15 points

### Trade #939 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 10:15:00
- **FVG 5m**: 21902.16 - 21905.22
- **Entrée**: 21907.77 @ 2025-05-28 12:03:00
- **Stop Loss**: 21891.21
- **Risk**: 16.56 points
- **TP 1RR**: 21924.33 ❌
- **TP 2RR**: 21940.90 ❌
- **TP 3RR**: 21957.46 ❌
- **TP 4RR**: 21974.02 ❌
- **TP 15RR**: 22156.20 ❌
- **PnL**: -16.56 points (-1.0R)
- **MFE**: 14.79 points
- **MAE**: 20.15 points

### Trade #940 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 13:45:00
- **FVG 5m**: 21907.01 - 21913.64
- **Entrée**: 21917.21 @ 2025-05-28 14:04:00
- **Stop Loss**: 21896.05
- **Risk**: 21.15 points
- **TP 1RR**: 21938.36 ✅
- **TP 2RR**: 21959.52 ❌
- **TP 3RR**: 21980.67 ❌
- **TP 4RR**: 22001.83 ❌
- **TP 15RR**: 22234.53 ❌
- **PnL**: -21.15 points (-1.0R)
- **MFE**: 29.58 points
- **MAE**: 24.48 points

### Trade #941 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 13:45:00
- **FVG 5m**: 21907.01 - 21913.64
- **Entrée**: 21917.21 @ 2025-05-28 14:04:00
- **Stop Loss**: 21896.05
- **Risk**: 21.15 points
- **TP 1RR**: 21938.36 ✅
- **TP 2RR**: 21959.52 ❌
- **TP 3RR**: 21980.67 ❌
- **TP 4RR**: 22001.83 ❌
- **TP 15RR**: 22234.53 ❌
- **PnL**: -21.15 points (-1.0R)
- **MFE**: 29.58 points
- **MAE**: 24.48 points

### Trade #942 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 15:15:00
- **FVG 5m**: 21892.47 - 21905.48
- **Entrée**: 21907.26 @ 2025-05-28 15:37:00
- **Stop Loss**: 21881.53
- **Risk**: 25.74 points
- **TP 1RR**: 21933.00 ✅
- **TP 2RR**: 21958.74 ✅
- **TP 3RR**: 21984.48 ✅
- **TP 4RR**: 22010.21 ✅
- **TP 15RR**: 22293.33 ✅
- **PnL**: 386.07 points (15.0R)
- **MFE**: 387.64 points
- **MAE**: 5.61 points

### Trade #943 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-28 20:00:00
- **FVG 5m**: 22215.59 - 22217.88
- **Entrée**: 22213.55 @ 2025-05-28 20:13:00
- **Stop Loss**: 22228.99
- **Risk**: 15.44 points
- **TP 1RR**: 22198.11 ✅
- **TP 2RR**: 22182.66 ❌
- **TP 3RR**: 22167.22 ❌
- **TP 4RR**: 22151.77 ❌
- **TP 15RR**: 21981.88 ❌
- **PnL**: -15.44 points (-1.0R)
- **MFE**: 23.21 points
- **MAE**: 15.56 points

### Trade #944 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 02:15:00
- **FVG 5m**: 22235.99 - 22239.82
- **Entrée**: 22241.60 @ 2025-05-29 02:38:00
- **Stop Loss**: 22224.87
- **Risk**: 16.73 points
- **TP 1RR**: 22258.33 ✅
- **TP 2RR**: 22275.06 ✅
- **TP 3RR**: 22291.79 ✅
- **TP 4RR**: 22308.52 ❌
- **TP 15RR**: 22492.53 ❌
- **PnL**: -16.73 points (-1.0R)
- **MFE**: 56.62 points
- **MAE**: 17.85 points

### Trade #945 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 03:00:00
- **FVG 5m**: 22230.13 - 22254.61
- **Entrée**: 22227.58 @ 2025-05-29 03:28:00
- **Stop Loss**: 22265.74
- **Risk**: 38.16 points
- **TP 1RR**: 22189.42 ✅
- **TP 2RR**: 22151.26 ✅
- **TP 3RR**: 22113.10 ✅
- **TP 4RR**: 22074.94 ✅
- **TP 15RR**: 21655.17 ✅
- **PnL**: 572.40 points (15.0R)
- **MFE**: 574.57 points
- **MAE**: 29.58 points

### Trade #946 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 03:00:00
- **FVG 5m**: 22230.13 - 22254.61
- **Entrée**: 22227.58 @ 2025-05-29 03:28:00
- **Stop Loss**: 22265.74
- **Risk**: 38.16 points
- **TP 1RR**: 22189.42 ✅
- **TP 2RR**: 22151.26 ✅
- **TP 3RR**: 22113.10 ✅
- **TP 4RR**: 22074.94 ✅
- **TP 15RR**: 21655.17 ✅
- **PnL**: 572.40 points (15.0R)
- **MFE**: 574.57 points
- **MAE**: 29.58 points

### Trade #947 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 03:00:00
- **FVG 5m**: 22230.13 - 22254.61
- **Entrée**: 22227.58 @ 2025-05-29 03:28:00
- **Stop Loss**: 22265.74
- **Risk**: 38.16 points
- **TP 1RR**: 22189.42 ✅
- **TP 2RR**: 22151.26 ✅
- **TP 3RR**: 22113.10 ✅
- **TP 4RR**: 22074.94 ✅
- **TP 15RR**: 21655.17 ✅
- **PnL**: 572.40 points (15.0R)
- **MFE**: 574.57 points
- **MAE**: 29.58 points

### Trade #948 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 06:45:00
- **FVG 5m**: 22082.98 - 22087.82
- **Entrée**: 22078.64 @ 2025-05-29 07:39:00
- **Stop Loss**: 22098.87
- **Risk**: 20.22 points
- **TP 1RR**: 22058.42 ❌
- **TP 2RR**: 22038.19 ❌
- **TP 3RR**: 22017.97 ❌
- **TP 4RR**: 21997.74 ❌
- **TP 15RR**: 21775.27 ❌
- **PnL**: -20.22 points (-1.0R)
- **MFE**: 16.32 points
- **MAE**: 22.44 points

### Trade #949 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 06:45:00
- **FVG 5m**: 22082.98 - 22087.82
- **Entrée**: 22078.64 @ 2025-05-29 07:39:00
- **Stop Loss**: 22098.87
- **Risk**: 20.22 points
- **TP 1RR**: 22058.42 ❌
- **TP 2RR**: 22038.19 ❌
- **TP 3RR**: 22017.97 ❌
- **TP 4RR**: 21997.74 ❌
- **TP 15RR**: 21775.27 ❌
- **PnL**: -20.22 points (-1.0R)
- **MFE**: 16.32 points
- **MAE**: 22.44 points

### Trade #950 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 06:45:00
- **FVG 5m**: 22082.98 - 22087.82
- **Entrée**: 22078.64 @ 2025-05-29 07:39:00
- **Stop Loss**: 22098.87
- **Risk**: 20.22 points
- **TP 1RR**: 22058.42 ❌
- **TP 2RR**: 22038.19 ❌
- **TP 3RR**: 22017.97 ❌
- **TP 4RR**: 21997.74 ❌
- **TP 15RR**: 21775.27 ❌
- **PnL**: -20.22 points (-1.0R)
- **MFE**: 16.32 points
- **MAE**: 22.44 points

### Trade #951 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22004.97
- **Risk**: 45.68 points
- **TP 1RR**: 21913.61 ✅
- **TP 2RR**: 21867.93 ✅
- **TP 3RR**: 21822.25 ✅
- **TP 4RR**: 21776.57 ✅
- **TP 15RR**: 21274.08 ❌
- **PnL**: -45.68 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 47.94 points

### Trade #952 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22004.97
- **Risk**: 45.68 points
- **TP 1RR**: 21913.61 ✅
- **TP 2RR**: 21867.93 ✅
- **TP 3RR**: 21822.25 ✅
- **TP 4RR**: 21776.57 ✅
- **TP 15RR**: 21274.08 ❌
- **PnL**: -45.68 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 47.94 points

### Trade #953 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22004.97
- **Risk**: 45.68 points
- **TP 1RR**: 21913.61 ✅
- **TP 2RR**: 21867.93 ✅
- **TP 3RR**: 21822.25 ✅
- **TP 4RR**: 21776.57 ✅
- **TP 15RR**: 21274.08 ❌
- **PnL**: -45.68 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 47.94 points

### Trade #954 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22004.97
- **Risk**: 45.68 points
- **TP 1RR**: 21913.61 ✅
- **TP 2RR**: 21867.93 ✅
- **TP 3RR**: 21822.25 ✅
- **TP 4RR**: 21776.57 ✅
- **TP 15RR**: 21274.08 ❌
- **PnL**: -45.68 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 47.94 points

### Trade #955 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22004.97
- **Risk**: 45.68 points
- **TP 1RR**: 21913.61 ✅
- **TP 2RR**: 21867.93 ✅
- **TP 3RR**: 21822.25 ✅
- **TP 4RR**: 21776.57 ✅
- **TP 15RR**: 21274.08 ❌
- **PnL**: -45.68 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 47.94 points

### Trade #956 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22004.97
- **Risk**: 45.68 points
- **TP 1RR**: 21913.61 ✅
- **TP 2RR**: 21867.93 ✅
- **TP 3RR**: 21822.25 ✅
- **TP 4RR**: 21776.57 ✅
- **TP 15RR**: 21274.08 ❌
- **PnL**: -45.68 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 47.94 points

### Trade #957 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 09:00:00
- **FVG 5m**: 21890.94 - 21913.89
- **Entrée**: 21877.94 @ 2025-05-29 10:32:00
- **Stop Loss**: 21924.85
- **Risk**: 46.92 points
- **TP 1RR**: 21831.02 ✅
- **TP 2RR**: 21784.10 ✅
- **TP 3RR**: 21737.19 ✅
- **TP 4RR**: 21690.27 ✅
- **TP 15RR**: 21174.20 ❌
- **PnL**: -46.92 points (-1.0R)
- **MFE**: 382.79 points
- **MAE**: 50.75 points

### Trade #958 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 11:00:00
- **FVG 5m**: 21801.43 - 21835.86
- **Entrée**: 21836.62 @ 2025-05-29 11:14:00
- **Stop Loss**: 21790.53
- **Risk**: 46.09 points
- **TP 1RR**: 21882.72 ✅
- **TP 2RR**: 21928.81 ❌
- **TP 3RR**: 21974.90 ❌
- **TP 4RR**: 22021.00 ❌
- **TP 15RR**: 22528.04 ❌
- **PnL**: -46.09 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 59.42 points

### Trade #959 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 11:00:00
- **FVG 5m**: 21801.43 - 21835.86
- **Entrée**: 21836.62 @ 2025-05-29 11:14:00
- **Stop Loss**: 21790.53
- **Risk**: 46.09 points
- **TP 1RR**: 21882.72 ✅
- **TP 2RR**: 21928.81 ❌
- **TP 3RR**: 21974.90 ❌
- **TP 4RR**: 22021.00 ❌
- **TP 15RR**: 22528.04 ❌
- **PnL**: -46.09 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 59.42 points

### Trade #960 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 20:00:00
- **FVG 5m**: 21740.22 - 21744.56
- **Entrée**: 21747.62 @ 2025-05-29 20:34:00
- **Stop Loss**: 21729.35
- **Risk**: 18.27 points
- **TP 1RR**: 21765.88 ✅
- **TP 2RR**: 21784.15 ✅
- **TP 3RR**: 21802.41 ✅
- **TP 4RR**: 21820.68 ✅
- **TP 15RR**: 22021.60 ❌
- **PnL**: -18.27 points (-1.0R)
- **MFE**: 104.05 points
- **MAE**: 36.98 points

### Trade #961 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 20:15:00
- **FVG 5m**: 21740.22 - 21744.56
- **Entrée**: 21747.62 @ 2025-05-29 20:34:00
- **Stop Loss**: 21729.35
- **Risk**: 18.27 points
- **TP 1RR**: 21765.88 ✅
- **TP 2RR**: 21784.15 ✅
- **TP 3RR**: 21802.41 ✅
- **TP 4RR**: 21820.68 ✅
- **TP 15RR**: 22021.60 ❌
- **PnL**: -18.27 points (-1.0R)
- **MFE**: 104.05 points
- **MAE**: 36.98 points

### Trade #962 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 07:00:00
- **FVG 5m**: 21743.79 - 21763.68
- **Entrée**: 21773.63 @ 2025-05-30 07:33:00
- **Stop Loss**: 21732.92
- **Risk**: 40.71 points
- **TP 1RR**: 21814.34 ✅
- **TP 2RR**: 21855.05 ❌
- **TP 3RR**: 21895.76 ❌
- **TP 4RR**: 21936.47 ❌
- **TP 15RR**: 22384.28 ❌
- **PnL**: -40.71 points (-1.0R)
- **MFE**: 46.92 points
- **MAE**: 41.82 points

### Trade #963 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 07:30:00
- **FVG 5m**: 21767.25 - 21787.40
- **Entrée**: 21789.95 @ 2025-05-30 08:16:00
- **Stop Loss**: 21756.37
- **Risk**: 33.58 points
- **TP 1RR**: 21823.53 ❌
- **TP 2RR**: 21857.11 ❌
- **TP 3RR**: 21890.69 ❌
- **TP 4RR**: 21924.27 ❌
- **TP 15RR**: 22293.67 ❌
- **PnL**: -33.58 points (-1.0R)
- **MFE**: 30.60 points
- **MAE**: 50.24 points

### Trade #964 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 07:30:00
- **FVG 5m**: 21767.25 - 21787.40
- **Entrée**: 21789.95 @ 2025-05-30 08:16:00
- **Stop Loss**: 21756.37
- **Risk**: 33.58 points
- **TP 1RR**: 21823.53 ❌
- **TP 2RR**: 21857.11 ❌
- **TP 3RR**: 21890.69 ❌
- **TP 4RR**: 21924.27 ❌
- **TP 15RR**: 22293.67 ❌
- **PnL**: -33.58 points (-1.0R)
- **MFE**: 30.60 points
- **MAE**: 50.24 points

### Trade #965 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 07:30:00
- **FVG 5m**: 21767.25 - 21787.40
- **Entrée**: 21789.95 @ 2025-05-30 08:16:00
- **Stop Loss**: 21756.37
- **Risk**: 33.58 points
- **TP 1RR**: 21823.53 ❌
- **TP 2RR**: 21857.11 ❌
- **TP 3RR**: 21890.69 ❌
- **TP 4RR**: 21924.27 ❌
- **TP 15RR**: 22293.67 ❌
- **PnL**: -33.58 points (-1.0R)
- **MFE**: 30.60 points
- **MAE**: 50.24 points

### Trade #966 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 11:15:00
- **FVG 5m**: 21604.80 - 21670.60
- **Entrée**: 21601.23 @ 2025-05-30 11:29:00
- **Stop Loss**: 21681.43
- **Risk**: 80.20 points
- **TP 1RR**: 21521.03 ✅
- **TP 2RR**: 21440.83 ❌
- **TP 3RR**: 21360.62 ❌
- **TP 4RR**: 21280.42 ❌
- **TP 15RR**: 20398.20 ❌
- **PnL**: -80.20 points (-1.0R)
- **MFE**: 106.09 points
- **MAE**: 103.54 points

### Trade #967 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 12:00:00
- **FVG 5m**: 21633.36 - 21654.53
- **Entrée**: 21657.08 @ 2025-05-30 13:09:00
- **Stop Loss**: 21622.55
- **Risk**: 34.53 points
- **TP 1RR**: 21691.62 ✅
- **TP 2RR**: 21726.15 ✅
- **TP 3RR**: 21760.68 ✅
- **TP 4RR**: 21795.22 ✅
- **TP 15RR**: 22175.09 ❌
- **PnL**: -34.53 points (-1.0R)
- **MFE**: 207.34 points
- **MAE**: 37.49 points

### Trade #968 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 13:00:00
- **FVG 5m**: 21670.60 - 21690.49
- **Entrée**: 21690.75 @ 2025-05-30 13:18:00
- **Stop Loss**: 21659.76
- **Risk**: 30.98 points
- **TP 1RR**: 21721.73 ✅
- **TP 2RR**: 21752.71 ✅
- **TP 3RR**: 21783.69 ✅
- **TP 4RR**: 21814.68 ✅
- **TP 15RR**: 22155.48 ❌
- **PnL**: -30.98 points (-1.0R)
- **MFE**: 173.67 points
- **MAE**: 31.37 points

### Trade #969 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 13:00:00
- **FVG 5m**: 21670.60 - 21690.49
- **Entrée**: 21690.75 @ 2025-05-30 13:18:00
- **Stop Loss**: 21659.76
- **Risk**: 30.98 points
- **TP 1RR**: 21721.73 ✅
- **TP 2RR**: 21752.71 ✅
- **TP 3RR**: 21783.69 ✅
- **TP 4RR**: 21814.68 ✅
- **TP 15RR**: 22155.48 ❌
- **PnL**: -30.98 points (-1.0R)
- **MFE**: 173.67 points
- **MAE**: 31.37 points

### Trade #970 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 13:00:00
- **FVG 5m**: 21670.60 - 21690.49
- **Entrée**: 21690.75 @ 2025-05-30 13:18:00
- **Stop Loss**: 21659.76
- **Risk**: 30.98 points
- **TP 1RR**: 21721.73 ✅
- **TP 2RR**: 21752.71 ✅
- **TP 3RR**: 21783.69 ✅
- **TP 4RR**: 21814.68 ✅
- **TP 15RR**: 22155.48 ❌
- **PnL**: -30.98 points (-1.0R)
- **MFE**: 173.67 points
- **MAE**: 31.37 points

### Trade #971 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 14:45:00
- **FVG 5m**: 21788.68 - 21792.76
- **Entrée**: 21772.86 @ 2025-05-30 15:03:00
- **Stop Loss**: 21803.65
- **Risk**: 30.79 points
- **TP 1RR**: 21742.08 ❌
- **TP 2RR**: 21711.29 ❌
- **TP 3RR**: 21680.50 ❌
- **TP 4RR**: 21649.71 ❌
- **TP 15RR**: 21311.04 ❌
- **PnL**: -30.79 points (-1.0R)
- **MFE**: 14.03 points
- **MAE**: 31.11 points

### Trade #972 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 14:45:00
- **FVG 5m**: 21788.68 - 21792.76
- **Entrée**: 21772.86 @ 2025-05-30 15:03:00
- **Stop Loss**: 21803.65
- **Risk**: 30.79 points
- **TP 1RR**: 21742.08 ❌
- **TP 2RR**: 21711.29 ❌
- **TP 3RR**: 21680.50 ❌
- **TP 4RR**: 21649.71 ❌
- **TP 15RR**: 21311.04 ❌
- **PnL**: -30.79 points (-1.0R)
- **MFE**: 14.03 points
- **MAE**: 31.11 points

### Trade #973 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 14:45:00
- **FVG 5m**: 21788.68 - 21792.76
- **Entrée**: 21772.86 @ 2025-05-30 15:03:00
- **Stop Loss**: 21803.65
- **Risk**: 30.79 points
- **TP 1RR**: 21742.08 ❌
- **TP 2RR**: 21711.29 ❌
- **TP 3RR**: 21680.50 ❌
- **TP 4RR**: 21649.71 ❌
- **TP 15RR**: 21311.04 ❌
- **PnL**: -30.79 points (-1.0R)
- **MFE**: 14.03 points
- **MAE**: 31.11 points

### Trade #974 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-02 06:00:00
- **FVG 5m**: 21691.00 - 21695.59
- **Entrée**: 21700.44 @ 2025-06-02 06:15:00
- **Stop Loss**: 21680.16
- **Risk**: 20.28 points
- **TP 1RR**: 21720.72 ❌
- **TP 2RR**: 21741.00 ❌
- **TP 3RR**: 21761.28 ❌
- **TP 4RR**: 21781.56 ❌
- **TP 15RR**: 22004.66 ❌
- **PnL**: -20.28 points (-1.0R)
- **MFE**: 19.13 points
- **MAE**: 22.44 points

### Trade #975 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 07:15:00
- **FVG 5m**: 21811.37 - 21836.62
- **Entrée**: 21810.35 @ 2025-06-02 08:49:00
- **Stop Loss**: 21847.54
- **Risk**: 37.19 points
- **TP 1RR**: 21773.17 ✅
- **TP 2RR**: 21735.98 ✅
- **TP 3RR**: 21698.80 ✅
- **TP 4RR**: 21661.61 ❌
- **TP 15RR**: 21252.56 ❌
- **PnL**: -37.19 points (-1.0R)
- **MFE**: 148.68 points
- **MAE**: 39.02 points

### Trade #976 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 08:30:00
- **FVG 5m**: 21811.37 - 21836.62
- **Entrée**: 21810.35 @ 2025-06-02 08:49:00
- **Stop Loss**: 21847.54
- **Risk**: 37.19 points
- **TP 1RR**: 21773.17 ✅
- **TP 2RR**: 21735.98 ✅
- **TP 3RR**: 21698.80 ✅
- **TP 4RR**: 21661.61 ❌
- **TP 15RR**: 21252.56 ❌
- **PnL**: -37.19 points (-1.0R)
- **MFE**: 148.68 points
- **MAE**: 39.02 points

### Trade #977 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 08:30:00
- **FVG 5m**: 21811.37 - 21836.62
- **Entrée**: 21810.35 @ 2025-06-02 08:49:00
- **Stop Loss**: 21847.54
- **Risk**: 37.19 points
- **TP 1RR**: 21773.17 ✅
- **TP 2RR**: 21735.98 ✅
- **TP 3RR**: 21698.80 ✅
- **TP 4RR**: 21661.61 ❌
- **TP 15RR**: 21252.56 ❌
- **PnL**: -37.19 points (-1.0R)
- **MFE**: 148.68 points
- **MAE**: 39.02 points

### Trade #978 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 19:15:00
- **FVG 5m**: 21903.44 - 21905.73
- **Entrée**: 21902.16 @ 2025-06-02 21:14:00
- **Stop Loss**: 21916.69
- **Risk**: 14.52 points
- **TP 1RR**: 21887.64 ✅
- **TP 2RR**: 21873.12 ✅
- **TP 3RR**: 21858.59 ✅
- **TP 4RR**: 21844.07 ✅
- **TP 15RR**: 21684.31 ❌
- **PnL**: -14.52 points (-1.0R)
- **MFE**: 72.68 points
- **MAE**: 14.79 points

### Trade #979 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-03 02:45:00
- **FVG 5m**: 21847.33 - 21854.47
- **Entrée**: 21856.00 @ 2025-06-03 03:32:00
- **Stop Loss**: 21836.41
- **Risk**: 19.59 points
- **TP 1RR**: 21875.60 ✅
- **TP 2RR**: 21895.19 ✅
- **TP 3RR**: 21914.79 ✅
- **TP 4RR**: 21934.38 ✅
- **TP 15RR**: 22149.92 ✅
- **PnL**: 293.92 points (15.0R)
- **MFE**: 294.56 points
- **MAE**: 7.65 points

### Trade #980 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-03 09:15:00
- **FVG 5m**: 22050.33 - 22060.53
- **Entrée**: 22065.63 @ 2025-06-03 09:47:00
- **Stop Loss**: 22039.31
- **Risk**: 26.33 points
- **TP 1RR**: 22091.96 ✅
- **TP 2RR**: 22118.29 ✅
- **TP 3RR**: 22144.61 ✅
- **TP 4RR**: 22170.94 ✅
- **TP 15RR**: 22460.54 ❌
- **PnL**: -26.33 points (-1.0R)
- **MFE**: 310.37 points
- **MAE**: 35.45 points

### Trade #981 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-03 13:00:00
- **FVG 5m**: 22133.73 - 22138.32
- **Entrée**: 22127.61 @ 2025-06-03 14:42:00
- **Stop Loss**: 22149.39
- **Risk**: 21.78 points
- **TP 1RR**: 22105.83 ✅
- **TP 2RR**: 22084.05 ❌
- **TP 3RR**: 22062.26 ❌
- **TP 4RR**: 22040.48 ❌
- **TP 15RR**: 21800.90 ❌
- **PnL**: -21.78 points (-1.0R)
- **MFE**: 27.03 points
- **MAE**: 24.74 points

### Trade #982 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 01:15:00
- **FVG 5m**: 22120.21 - 22123.02
- **Entrée**: 22117.91 @ 2025-06-04 02:09:00
- **Stop Loss**: 22134.08
- **Risk**: 16.16 points
- **TP 1RR**: 22101.75 ❌
- **TP 2RR**: 22085.59 ❌
- **TP 3RR**: 22069.43 ❌
- **TP 4RR**: 22053.27 ❌
- **TP 15RR**: 21875.48 ❌
- **PnL**: -16.16 points (-1.0R)
- **MFE**: 7.65 points
- **MAE**: 16.83 points

### Trade #983 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 03:45:00
- **FVG 5m**: 22170.96 - 22184.73
- **Entrée**: 22164.58 @ 2025-06-04 05:20:00
- **Stop Loss**: 22195.82
- **Risk**: 31.24 points
- **TP 1RR**: 22133.35 ❌
- **TP 2RR**: 22102.11 ❌
- **TP 3RR**: 22070.87 ❌
- **TP 4RR**: 22039.63 ❌
- **TP 15RR**: 21695.99 ❌
- **PnL**: -31.24 points (-1.0R)
- **MFE**: 8.16 points
- **MAE**: 37.49 points

### Trade #984 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 05:00:00
- **FVG 5m**: 22164.07 - 22166.88
- **Entrée**: 22167.64 @ 2025-06-04 05:44:00
- **Stop Loss**: 22152.99
- **Risk**: 14.65 points
- **TP 1RR**: 22182.30 ✅
- **TP 2RR**: 22196.95 ✅
- **TP 3RR**: 22211.60 ❌
- **TP 4RR**: 22226.25 ❌
- **TP 15RR**: 22387.43 ❌
- **PnL**: -14.65 points (-1.0R)
- **MFE**: 36.98 points
- **MAE**: 20.15 points

### Trade #985 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22184.85
- **Risk**: 45.77 points
- **TP 1RR**: 22093.31 ✅
- **TP 2RR**: 22047.54 ❌
- **TP 3RR**: 22001.77 ❌
- **TP 4RR**: 21956.00 ❌
- **TP 15RR**: 21452.53 ❌
- **PnL**: -45.77 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 49.22 points

### Trade #986 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22184.85
- **Risk**: 45.77 points
- **TP 1RR**: 22093.31 ✅
- **TP 2RR**: 22047.54 ❌
- **TP 3RR**: 22001.77 ❌
- **TP 4RR**: 21956.00 ❌
- **TP 15RR**: 21452.53 ❌
- **PnL**: -45.77 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 49.22 points

### Trade #987 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22184.85
- **Risk**: 45.77 points
- **TP 1RR**: 22093.31 ✅
- **TP 2RR**: 22047.54 ❌
- **TP 3RR**: 22001.77 ❌
- **TP 4RR**: 21956.00 ❌
- **TP 15RR**: 21452.53 ❌
- **PnL**: -45.77 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 49.22 points

### Trade #988 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22168.92 - 22186.26
- **Entrée**: 22192.38 @ 2025-06-04 08:34:00
- **Stop Loss**: 22157.84
- **Risk**: 34.55 points
- **TP 1RR**: 22226.93 ✅
- **TP 2RR**: 22261.48 ❌
- **TP 3RR**: 22296.02 ❌
- **TP 4RR**: 22330.57 ❌
- **TP 15RR**: 22710.59 ❌
- **PnL**: -34.55 points (-1.0R)
- **MFE**: 39.02 points
- **MAE**: 66.31 points

### Trade #989 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22168.92 - 22186.26
- **Entrée**: 22192.38 @ 2025-06-04 08:34:00
- **Stop Loss**: 22157.84
- **Risk**: 34.55 points
- **TP 1RR**: 22226.93 ✅
- **TP 2RR**: 22261.48 ❌
- **TP 3RR**: 22296.02 ❌
- **TP 4RR**: 22330.57 ❌
- **TP 15RR**: 22710.59 ❌
- **PnL**: -34.55 points (-1.0R)
- **MFE**: 39.02 points
- **MAE**: 66.31 points

### Trade #990 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 08:15:00
- **FVG 5m**: 22168.92 - 22186.26
- **Entrée**: 22192.38 @ 2025-06-04 08:34:00
- **Stop Loss**: 22157.84
- **Risk**: 34.55 points
- **TP 1RR**: 22226.93 ✅
- **TP 2RR**: 22261.48 ❌
- **TP 3RR**: 22296.02 ❌
- **TP 4RR**: 22330.57 ❌
- **TP 15RR**: 22710.59 ❌
- **PnL**: -34.55 points (-1.0R)
- **MFE**: 39.02 points
- **MAE**: 66.31 points

### Trade #991 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 08:30:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22184.85
- **Risk**: 45.77 points
- **TP 1RR**: 22093.31 ✅
- **TP 2RR**: 22047.54 ❌
- **TP 3RR**: 22001.77 ❌
- **TP 4RR**: 21956.00 ❌
- **TP 15RR**: 21452.53 ❌
- **PnL**: -45.77 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 49.22 points

### Trade #992 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 08:30:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22184.85
- **Risk**: 45.77 points
- **TP 1RR**: 22093.31 ✅
- **TP 2RR**: 22047.54 ❌
- **TP 3RR**: 22001.77 ❌
- **TP 4RR**: 21956.00 ❌
- **TP 15RR**: 21452.53 ❌
- **PnL**: -45.77 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 49.22 points

### Trade #993 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 08:30:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22184.85
- **Risk**: 45.77 points
- **TP 1RR**: 22093.31 ✅
- **TP 2RR**: 22047.54 ❌
- **TP 3RR**: 22001.77 ❌
- **TP 4RR**: 21956.00 ❌
- **TP 15RR**: 21452.53 ❌
- **PnL**: -45.77 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 49.22 points

### Trade #994 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 09:00:00
- **FVG 5m**: 22171.98 - 22192.89
- **Entrée**: 22198.50 @ 2025-06-04 09:59:00
- **Stop Loss**: 22160.89
- **Risk**: 37.61 points
- **TP 1RR**: 22236.11 ❌
- **TP 2RR**: 22273.72 ❌
- **TP 3RR**: 22311.33 ❌
- **TP 4RR**: 22348.94 ❌
- **TP 15RR**: 22762.63 ❌
- **PnL**: -37.61 points (-1.0R)
- **MFE**: 23.97 points
- **MAE**: 44.63 points

### Trade #995 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 09:00:00
- **FVG 5m**: 22171.98 - 22192.89
- **Entrée**: 22198.50 @ 2025-06-04 09:59:00
- **Stop Loss**: 22160.89
- **Risk**: 37.61 points
- **TP 1RR**: 22236.11 ❌
- **TP 2RR**: 22273.72 ❌
- **TP 3RR**: 22311.33 ❌
- **TP 4RR**: 22348.94 ❌
- **TP 15RR**: 22762.63 ❌
- **PnL**: -37.61 points (-1.0R)
- **MFE**: 23.97 points
- **MAE**: 44.63 points

### Trade #996 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 02:45:00
- **FVG 5m**: 22248.49 - 22256.90
- **Entrée**: 22248.23 @ 2025-06-05 03:47:00
- **Stop Loss**: 22268.03
- **Risk**: 19.80 points
- **TP 1RR**: 22228.43 ✅
- **TP 2RR**: 22208.63 ✅
- **TP 3RR**: 22188.84 ✅
- **TP 4RR**: 22169.04 ✅
- **TP 15RR**: 21951.24 ❌
- **PnL**: -19.80 points (-1.0R)
- **MFE**: 99.21 points
- **MAE**: 90.02 points

### Trade #997 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 03:45:00
- **FVG 5m**: 22215.59 - 22218.14
- **Entrée**: 22208.96 @ 2025-06-05 04:14:00
- **Stop Loss**: 22229.25
- **Risk**: 20.29 points
- **TP 1RR**: 22188.67 ❌
- **TP 2RR**: 22168.38 ❌
- **TP 3RR**: 22148.09 ❌
- **TP 4RR**: 22127.80 ❌
- **TP 15RR**: 21904.61 ❌
- **PnL**: -20.29 points (-1.0R)
- **MFE**: 7.40 points
- **MAE**: 20.66 points

### Trade #998 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 03:45:00
- **FVG 5m**: 22215.59 - 22218.14
- **Entrée**: 22208.96 @ 2025-06-05 04:14:00
- **Stop Loss**: 22229.25
- **Risk**: 20.29 points
- **TP 1RR**: 22188.67 ❌
- **TP 2RR**: 22168.38 ❌
- **TP 3RR**: 22148.09 ❌
- **TP 4RR**: 22127.80 ❌
- **TP 15RR**: 21904.61 ❌
- **PnL**: -20.29 points (-1.0R)
- **MFE**: 7.40 points
- **MAE**: 20.66 points

### Trade #999 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 04:00:00
- **FVG 5m**: 22215.59 - 22218.14
- **Entrée**: 22208.96 @ 2025-06-05 04:14:00
- **Stop Loss**: 22229.25
- **Risk**: 20.29 points
- **TP 1RR**: 22188.67 ❌
- **TP 2RR**: 22168.38 ❌
- **TP 3RR**: 22148.09 ❌
- **TP 4RR**: 22127.80 ❌
- **TP 15RR**: 21904.61 ❌
- **PnL**: -20.29 points (-1.0R)
- **MFE**: 7.40 points
- **MAE**: 20.66 points

### Trade #1000 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 05:30:00
- **FVG 5m**: 22205.13 - 22223.50
- **Entrée**: 22200.80 @ 2025-06-05 05:42:00
- **Stop Loss**: 22234.61
- **Risk**: 33.81 points
- **TP 1RR**: 22166.99 ✅
- **TP 2RR**: 22133.18 ❌
- **TP 3RR**: 22099.37 ❌
- **TP 4RR**: 22065.56 ❌
- **TP 15RR**: 21693.66 ❌
- **PnL**: -33.81 points (-1.0R)
- **MFE**: 51.77 points
- **MAE**: 137.46 points

### Trade #1001 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 05:30:00
- **FVG 5m**: 22205.13 - 22223.50
- **Entrée**: 22200.80 @ 2025-06-05 05:42:00
- **Stop Loss**: 22234.61
- **Risk**: 33.81 points
- **TP 1RR**: 22166.99 ✅
- **TP 2RR**: 22133.18 ❌
- **TP 3RR**: 22099.37 ❌
- **TP 4RR**: 22065.56 ❌
- **TP 15RR**: 21693.66 ❌
- **PnL**: -33.81 points (-1.0R)
- **MFE**: 51.77 points
- **MAE**: 137.46 points

### Trade #1002 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 07:30:00
- **FVG 5m**: 22214.57 - 22250.27
- **Entrée**: 22285.21 @ 2025-06-05 07:49:00
- **Stop Loss**: 22203.46
- **Risk**: 81.75 points
- **TP 1RR**: 22366.96 ❌
- **TP 2RR**: 22448.71 ❌
- **TP 3RR**: 22530.46 ❌
- **TP 4RR**: 22612.21 ❌
- **TP 15RR**: 23511.46 ❌
- **PnL**: -81.75 points (-1.0R)
- **MFE**: 21.68 points
- **MAE**: 86.20 points

### Trade #1003 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 07:30:00
- **FVG 5m**: 22214.57 - 22250.27
- **Entrée**: 22285.21 @ 2025-06-05 07:49:00
- **Stop Loss**: 22203.46
- **Risk**: 81.75 points
- **TP 1RR**: 22366.96 ❌
- **TP 2RR**: 22448.71 ❌
- **TP 3RR**: 22530.46 ❌
- **TP 4RR**: 22612.21 ❌
- **TP 15RR**: 23511.46 ❌
- **PnL**: -81.75 points (-1.0R)
- **MFE**: 21.68 points
- **MAE**: 86.20 points

### Trade #1004 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 07:30:00
- **FVG 5m**: 22214.57 - 22250.27
- **Entrée**: 22285.21 @ 2025-06-05 07:49:00
- **Stop Loss**: 22203.46
- **Risk**: 81.75 points
- **TP 1RR**: 22366.96 ❌
- **TP 2RR**: 22448.71 ❌
- **TP 3RR**: 22530.46 ❌
- **TP 4RR**: 22612.21 ❌
- **TP 15RR**: 23511.46 ❌
- **PnL**: -81.75 points (-1.0R)
- **MFE**: 21.68 points
- **MAE**: 86.20 points

### Trade #1005 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 08:45:00
- **FVG 5m**: 22171.98 - 22211.25
- **Entrée**: 22211.76 @ 2025-06-05 09:24:00
- **Stop Loss**: 22160.89
- **Risk**: 50.87 points
- **TP 1RR**: 22262.63 ❌
- **TP 2RR**: 22313.50 ❌
- **TP 3RR**: 22364.37 ❌
- **TP 4RR**: 22415.24 ❌
- **TP 15RR**: 22974.82 ❌
- **PnL**: -50.87 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 71.41 points

### Trade #1006 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 10:15:00
- **FVG 5m**: 22144.18 - 22164.84
- **Entrée**: 22169.69 @ 2025-06-05 12:08:00
- **Stop Loss**: 22133.11
- **Risk**: 36.57 points
- **TP 1RR**: 22206.26 ✅
- **TP 2RR**: 22242.83 ❌
- **TP 3RR**: 22279.41 ❌
- **TP 4RR**: 22315.98 ❌
- **TP 15RR**: 22718.31 ❌
- **PnL**: -36.57 points (-1.0R)
- **MFE**: 58.15 points
- **MAE**: 40.55 points

### Trade #1007 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 11:00:00
- **FVG 5m**: 22307.40 - 22322.45
- **Entrée**: 22306.63 @ 2025-06-05 11:14:00
- **Stop Loss**: 22333.61
- **Risk**: 26.97 points
- **TP 1RR**: 22279.66 ✅
- **TP 2RR**: 22252.69 ✅
- **TP 3RR**: 22225.72 ✅
- **TP 4RR**: 22198.74 ✅
- **TP 15RR**: 21902.04 ❌
- **PnL**: -26.97 points (-1.0R)
- **MFE**: 403.96 points
- **MAE**: 33.66 points

### Trade #1008 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 11:00:00
- **FVG 5m**: 22307.40 - 22322.45
- **Entrée**: 22306.63 @ 2025-06-05 11:14:00
- **Stop Loss**: 22333.61
- **Risk**: 26.97 points
- **TP 1RR**: 22279.66 ✅
- **TP 2RR**: 22252.69 ✅
- **TP 3RR**: 22225.72 ✅
- **TP 4RR**: 22198.74 ✅
- **TP 15RR**: 21902.04 ❌
- **PnL**: -26.97 points (-1.0R)
- **MFE**: 403.96 points
- **MAE**: 33.66 points

### Trade #1009 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 12:00:00
- **FVG 5m**: 22174.79 - 22193.91
- **Entrée**: 22194.93 @ 2025-06-05 12:14:00
- **Stop Loss**: 22163.70
- **Risk**: 31.23 points
- **TP 1RR**: 22226.17 ✅
- **TP 2RR**: 22257.40 ❌
- **TP 3RR**: 22288.64 ❌
- **TP 4RR**: 22319.87 ❌
- **TP 15RR**: 22663.45 ❌
- **PnL**: -31.23 points (-1.0R)
- **MFE**: 32.90 points
- **MAE**: 37.23 points

### Trade #1010 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 13:15:00
- **FVG 5m**: 21991.93 - 22006.72
- **Entrée**: 22013.35 @ 2025-06-05 14:26:00
- **Stop Loss**: 21980.94
- **Risk**: 32.42 points
- **TP 1RR**: 22045.77 ✅
- **TP 2RR**: 22078.19 ✅
- **TP 3RR**: 22110.61 ✅
- **TP 4RR**: 22143.03 ❌
- **TP 15RR**: 22499.63 ❌
- **PnL**: -32.42 points (-1.0R)
- **MFE**: 97.42 points
- **MAE**: 66.56 points

### Trade #1011 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 13:15:00
- **FVG 5m**: 21991.93 - 22006.72
- **Entrée**: 22013.35 @ 2025-06-05 14:26:00
- **Stop Loss**: 21980.94
- **Risk**: 32.42 points
- **TP 1RR**: 22045.77 ✅
- **TP 2RR**: 22078.19 ✅
- **TP 3RR**: 22110.61 ✅
- **TP 4RR**: 22143.03 ❌
- **TP 15RR**: 22499.63 ❌
- **PnL**: -32.42 points (-1.0R)
- **MFE**: 97.42 points
- **MAE**: 66.56 points

### Trade #1012 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 15:30:00
- **FVG 5m**: 21931.24 - 21966.68
- **Entrée**: 21920.01 @ 2025-06-05 17:00:00
- **Stop Loss**: 21977.67
- **Risk**: 57.65 points
- **TP 1RR**: 21862.36 ❌
- **TP 2RR**: 21804.71 ❌
- **TP 3RR**: 21747.05 ❌
- **TP 4RR**: 21689.40 ❌
- **TP 15RR**: 21055.22 ❌
- **PnL**: -57.65 points (-1.0R)
- **MFE**: 3.57 points
- **MAE**: 62.48 points

### Trade #1013 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 17:00:00
- **FVG 5m**: 21934.81 - 21940.16
- **Entrée**: 21940.67 @ 2025-06-05 17:14:00
- **Stop Loss**: 21923.84
- **Risk**: 16.83 points
- **TP 1RR**: 21957.50 ✅
- **TP 2RR**: 21974.34 ✅
- **TP 3RR**: 21991.17 ✅
- **TP 4RR**: 22008.00 ✅
- **TP 15RR**: 22193.17 ✅
- **PnL**: 252.50 points (15.0R)
- **MFE**: 264.97 points
- **MAE**: 0.51 points

### Trade #1014 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 17:00:00
- **FVG 5m**: 21934.81 - 21940.16
- **Entrée**: 21940.67 @ 2025-06-05 17:14:00
- **Stop Loss**: 21923.84
- **Risk**: 16.83 points
- **TP 1RR**: 21957.50 ✅
- **TP 2RR**: 21974.34 ✅
- **TP 3RR**: 21991.17 ✅
- **TP 4RR**: 22008.00 ✅
- **TP 15RR**: 22193.17 ✅
- **PnL**: 252.50 points (15.0R)
- **MFE**: 264.97 points
- **MAE**: 0.51 points

### Trade #1015 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-06 11:45:00
- **FVG 5m**: 22203.35 - 22222.22
- **Entrée**: 22223.24 @ 2025-06-06 12:19:00
- **Stop Loss**: 22192.25
- **Risk**: 30.99 points
- **TP 1RR**: 22254.23 ✅
- **TP 2RR**: 22285.23 ✅
- **TP 3RR**: 22316.22 ❌
- **TP 4RR**: 22347.22 ❌
- **TP 15RR**: 22688.15 ❌
- **PnL**: -30.99 points (-1.0R)
- **MFE**: 90.02 points
- **MAE**: 32.90 points

### Trade #1016 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-09 08:30:00
- **FVG 5m**: 22235.74 - 22238.54
- **Entrée**: 22242.37 @ 2025-06-09 08:49:00
- **Stop Loss**: 22224.62
- **Risk**: 17.75 points
- **TP 1RR**: 22260.12 ❌
- **TP 2RR**: 22277.86 ❌
- **TP 3RR**: 22295.61 ❌
- **TP 4RR**: 22313.36 ❌
- **TP 15RR**: 22508.60 ❌
- **PnL**: -17.75 points (-1.0R)
- **MFE**: 16.07 points
- **MAE**: 19.13 points

### Trade #1017 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-09 09:30:00
- **FVG 5m**: 22301.53 - 22304.85
- **Entrée**: 22297.71 @ 2025-06-09 09:44:00
- **Stop Loss**: 22316.00
- **Risk**: 18.29 points
- **TP 1RR**: 22279.42 ✅
- **TP 2RR**: 22261.12 ✅
- **TP 3RR**: 22242.83 ❌
- **TP 4RR**: 22224.54 ❌
- **TP 15RR**: 22023.31 ❌
- **PnL**: -18.29 points (-1.0R)
- **MFE**: 46.16 points
- **MAE**: 23.46 points

### Trade #1018 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-09 09:30:00
- **FVG 5m**: 22301.53 - 22304.85
- **Entrée**: 22297.71 @ 2025-06-09 09:44:00
- **Stop Loss**: 22316.00
- **Risk**: 18.29 points
- **TP 1RR**: 22279.42 ✅
- **TP 2RR**: 22261.12 ✅
- **TP 3RR**: 22242.83 ❌
- **TP 4RR**: 22224.54 ❌
- **TP 15RR**: 22023.31 ❌
- **PnL**: -18.29 points (-1.0R)
- **MFE**: 46.16 points
- **MAE**: 23.46 points

### Trade #1019 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-09 14:45:00
- **FVG 5m**: 22274.25 - 22276.54
- **Entrée**: 22273.74 @ 2025-06-09 17:28:00
- **Stop Loss**: 22287.68
- **Risk**: 13.94 points
- **TP 1RR**: 22259.79 ✅
- **TP 2RR**: 22245.85 ❌
- **TP 3RR**: 22231.91 ❌
- **TP 4RR**: 22217.96 ❌
- **TP 15RR**: 22064.58 ❌
- **PnL**: -13.94 points (-1.0R)
- **MFE**: 19.89 points
- **MAE**: 14.03 points

### Trade #1020 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 00:15:00
- **FVG 5m**: 22228.85 - 22260.47
- **Entrée**: 22226.56 @ 2025-06-10 00:28:00
- **Stop Loss**: 22271.60
- **Risk**: 45.05 points
- **TP 1RR**: 22181.51 ❌
- **TP 2RR**: 22136.46 ❌
- **TP 3RR**: 22091.41 ❌
- **TP 4RR**: 22046.36 ❌
- **TP 15RR**: 21550.82 ❌
- **PnL**: -45.05 points (-1.0R)
- **MFE**: 32.64 points
- **MAE**: 55.34 points

### Trade #1021 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 00:15:00
- **FVG 5m**: 22228.85 - 22260.47
- **Entrée**: 22226.56 @ 2025-06-10 00:28:00
- **Stop Loss**: 22271.60
- **Risk**: 45.05 points
- **TP 1RR**: 22181.51 ❌
- **TP 2RR**: 22136.46 ❌
- **TP 3RR**: 22091.41 ❌
- **TP 4RR**: 22046.36 ❌
- **TP 15RR**: 21550.82 ❌
- **PnL**: -45.05 points (-1.0R)
- **MFE**: 32.64 points
- **MAE**: 55.34 points

### Trade #1022 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 00:15:00
- **FVG 5m**: 22228.85 - 22260.47
- **Entrée**: 22226.56 @ 2025-06-10 00:28:00
- **Stop Loss**: 22271.60
- **Risk**: 45.05 points
- **TP 1RR**: 22181.51 ❌
- **TP 2RR**: 22136.46 ❌
- **TP 3RR**: 22091.41 ❌
- **TP 4RR**: 22046.36 ❌
- **TP 15RR**: 21550.82 ❌
- **PnL**: -45.05 points (-1.0R)
- **MFE**: 32.64 points
- **MAE**: 55.34 points

### Trade #1023 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 00:30:00
- **FVG 5m**: 22242.37 - 22247.98
- **Entrée**: 22248.49 @ 2025-06-10 02:16:00
- **Stop Loss**: 22231.25
- **Risk**: 17.24 points
- **TP 1RR**: 22265.73 ❌
- **TP 2RR**: 22282.97 ❌
- **TP 3RR**: 22300.21 ❌
- **TP 4RR**: 22317.46 ❌
- **TP 15RR**: 22507.12 ❌
- **PnL**: -17.24 points (-1.0R)
- **MFE**: 16.58 points
- **MAE**: 23.72 points

### Trade #1024 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 00:30:00
- **FVG 5m**: 22242.37 - 22247.98
- **Entrée**: 22248.49 @ 2025-06-10 02:16:00
- **Stop Loss**: 22231.25
- **Risk**: 17.24 points
- **TP 1RR**: 22265.73 ❌
- **TP 2RR**: 22282.97 ❌
- **TP 3RR**: 22300.21 ❌
- **TP 4RR**: 22317.46 ❌
- **TP 15RR**: 22507.12 ❌
- **PnL**: -17.24 points (-1.0R)
- **MFE**: 16.58 points
- **MAE**: 23.72 points

### Trade #1025 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 02:30:00
- **FVG 5m**: 22208.19 - 22213.04
- **Entrée**: 22206.92 @ 2025-06-10 02:43:00
- **Stop Loss**: 22224.15
- **Risk**: 17.23 points
- **TP 1RR**: 22189.69 ✅
- **TP 2RR**: 22172.46 ✅
- **TP 3RR**: 22155.24 ❌
- **TP 4RR**: 22138.01 ❌
- **TP 15RR**: 21948.51 ❌
- **PnL**: -17.23 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 20.15 points

### Trade #1026 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 02:30:00
- **FVG 5m**: 22208.19 - 22213.04
- **Entrée**: 22206.92 @ 2025-06-10 02:43:00
- **Stop Loss**: 22224.15
- **Risk**: 17.23 points
- **TP 1RR**: 22189.69 ✅
- **TP 2RR**: 22172.46 ✅
- **TP 3RR**: 22155.24 ❌
- **TP 4RR**: 22138.01 ❌
- **TP 15RR**: 21948.51 ❌
- **PnL**: -17.23 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 20.15 points

### Trade #1027 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 02:30:00
- **FVG 5m**: 22208.19 - 22213.04
- **Entrée**: 22206.92 @ 2025-06-10 02:43:00
- **Stop Loss**: 22224.15
- **Risk**: 17.23 points
- **TP 1RR**: 22189.69 ✅
- **TP 2RR**: 22172.46 ✅
- **TP 3RR**: 22155.24 ❌
- **TP 4RR**: 22138.01 ❌
- **TP 15RR**: 21948.51 ❌
- **PnL**: -17.23 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 20.15 points

### Trade #1028 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 02:45:00
- **FVG 5m**: 22220.18 - 22230.13
- **Entrée**: 22231.15 @ 2025-06-10 02:56:00
- **Stop Loss**: 22209.07
- **Risk**: 22.08 points
- **TP 1RR**: 22253.22 ❌
- **TP 2RR**: 22275.30 ❌
- **TP 3RR**: 22297.37 ❌
- **TP 4RR**: 22319.45 ❌
- **TP 15RR**: 22562.29 ❌
- **PnL**: -22.08 points (-1.0R)
- **MFE**: 21.93 points
- **MAE**: 23.97 points

### Trade #1029 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 02:45:00
- **FVG 5m**: 22220.18 - 22230.13
- **Entrée**: 22231.15 @ 2025-06-10 02:56:00
- **Stop Loss**: 22209.07
- **Risk**: 22.08 points
- **TP 1RR**: 22253.22 ❌
- **TP 2RR**: 22275.30 ❌
- **TP 3RR**: 22297.37 ❌
- **TP 4RR**: 22319.45 ❌
- **TP 15RR**: 22562.29 ❌
- **PnL**: -22.08 points (-1.0R)
- **MFE**: 21.93 points
- **MAE**: 23.97 points

### Trade #1030 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 08:30:00
- **FVG 5m**: 22254.61 - 22293.63
- **Entrée**: 22235.99 @ 2025-06-10 10:32:00
- **Stop Loss**: 22304.77
- **Risk**: 68.78 points
- **TP 1RR**: 22167.21 ❌
- **TP 2RR**: 22098.43 ❌
- **TP 3RR**: 22029.64 ❌
- **TP 4RR**: 21960.86 ❌
- **TP 15RR**: 21204.25 ❌
- **PnL**: -68.78 points (-1.0R)
- **MFE**: 56.11 points
- **MAE**: 71.41 points

### Trade #1031 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 10:30:00
- **FVG 5m**: 22254.61 - 22277.31
- **Entrée**: 22281.90 @ 2025-06-10 10:44:00
- **Stop Loss**: 22243.48
- **Risk**: 38.42 points
- **TP 1RR**: 22320.31 ✅
- **TP 2RR**: 22358.73 ✅
- **TP 3RR**: 22397.14 ✅
- **TP 4RR**: 22435.56 ✅
- **TP 15RR**: 22858.12 ❌
- **PnL**: -38.42 points (-1.0R)
- **MFE**: 268.54 points
- **MAE**: 53.05 points

### Trade #1032 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 10:30:00
- **FVG 5m**: 22254.61 - 22277.31
- **Entrée**: 22281.90 @ 2025-06-10 10:44:00
- **Stop Loss**: 22243.48
- **Risk**: 38.42 points
- **TP 1RR**: 22320.31 ✅
- **TP 2RR**: 22358.73 ✅
- **TP 3RR**: 22397.14 ✅
- **TP 4RR**: 22435.56 ✅
- **TP 15RR**: 22858.12 ❌
- **PnL**: -38.42 points (-1.0R)
- **MFE**: 268.54 points
- **MAE**: 53.05 points

### Trade #1033 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 12:15:00
- **FVG 5m**: 22333.67 - 22347.18
- **Entrée**: 22330.35 @ 2025-06-10 12:29:00
- **Stop Loss**: 22358.36
- **Risk**: 28.01 points
- **TP 1RR**: 22302.35 ✅
- **TP 2RR**: 22274.34 ✅
- **TP 3RR**: 22246.34 ❌
- **TP 4RR**: 22218.33 ❌
- **TP 15RR**: 21910.27 ❌
- **PnL**: -28.01 points (-1.0R)
- **MFE**: 70.90 points
- **MAE**: 30.86 points

### Trade #1034 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 14:00:00
- **FVG 5m**: 22386.97 - 22394.62
- **Entrée**: 22405.58 @ 2025-06-10 15:18:00
- **Stop Loss**: 22375.77
- **Risk**: 29.81 points
- **TP 1RR**: 22435.39 ❌
- **TP 2RR**: 22465.21 ❌
- **TP 3RR**: 22495.02 ❌
- **TP 4RR**: 22524.83 ❌
- **TP 15RR**: 22852.74 ❌
- **PnL**: -29.81 points (-1.0R)
- **MFE**: 20.15 points
- **MAE**: 33.41 points

### Trade #1035 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 18:15:00
- **FVG 5m**: 22401.76 - 22407.88
- **Entrée**: 22401.25 @ 2025-06-10 18:36:00
- **Stop Loss**: 22419.08
- **Risk**: 17.83 points
- **TP 1RR**: 22383.41 ✅
- **TP 2RR**: 22365.58 ✅
- **TP 3RR**: 22347.74 ✅
- **TP 4RR**: 22329.91 ✅
- **TP 15RR**: 22133.73 ❌
- **PnL**: -17.83 points (-1.0R)
- **MFE**: 95.89 points
- **MAE**: 33.66 points

### Trade #1036 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 00:00:00
- **FVG 5m**: 22329.08 - 22333.16
- **Entrée**: 22333.92 @ 2025-06-11 00:14:00
- **Stop Loss**: 22317.91
- **Risk**: 16.01 points
- **TP 1RR**: 22349.93 ❌
- **TP 2RR**: 22365.94 ❌
- **TP 3RR**: 22381.95 ❌
- **TP 4RR**: 22397.96 ❌
- **TP 15RR**: 22574.07 ❌
- **PnL**: -16.01 points (-1.0R)
- **MFE**: 6.63 points
- **MAE**: 16.07 points

### Trade #1037 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 00:00:00
- **FVG 5m**: 22329.08 - 22333.16
- **Entrée**: 22333.92 @ 2025-06-11 00:14:00
- **Stop Loss**: 22317.91
- **Risk**: 16.01 points
- **TP 1RR**: 22349.93 ❌
- **TP 2RR**: 22365.94 ❌
- **TP 3RR**: 22381.95 ❌
- **TP 4RR**: 22397.96 ❌
- **TP 15RR**: 22574.07 ❌
- **PnL**: -16.01 points (-1.0R)
- **MFE**: 6.63 points
- **MAE**: 16.07 points

### Trade #1038 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 04:30:00
- **FVG 5m**: 22364.78 - 22368.35
- **Entrée**: 22363.25 @ 2025-06-11 06:01:00
- **Stop Loss**: 22379.53
- **Risk**: 16.28 points
- **TP 1RR**: 22346.97 ✅
- **TP 2RR**: 22330.68 ✅
- **TP 3RR**: 22314.40 ❌
- **TP 4RR**: 22298.11 ❌
- **TP 15RR**: 22118.98 ❌
- **PnL**: -16.28 points (-1.0R)
- **MFE**: 41.31 points
- **MAE**: 18.11 points

### Trade #1039 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 06:00:00
- **FVG 5m**: 22346.42 - 22356.11
- **Entrée**: 22336.73 @ 2025-06-11 06:15:00
- **Stop Loss**: 22367.29
- **Risk**: 30.56 points
- **TP 1RR**: 22306.17 ❌
- **TP 2RR**: 22275.61 ❌
- **TP 3RR**: 22245.05 ❌
- **TP 4RR**: 22214.49 ❌
- **TP 15RR**: 21878.33 ❌
- **PnL**: -30.56 points (-1.0R)
- **MFE**: 14.79 points
- **MAE**: 31.11 points

### Trade #1040 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 07:00:00
- **FVG 5m**: 22480.31 - 22488.98
- **Entrée**: 22468.07 @ 2025-06-11 07:49:00
- **Stop Loss**: 22500.22
- **Risk**: 32.16 points
- **TP 1RR**: 22435.91 ✅
- **TP 2RR**: 22403.75 ✅
- **TP 3RR**: 22371.60 ✅
- **TP 4RR**: 22339.44 ❌
- **TP 15RR**: 21985.72 ❌
- **PnL**: -32.16 points (-1.0R)
- **MFE**: 111.70 points
- **MAE**: 32.64 points

### Trade #1041 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 07:00:00
- **FVG 5m**: 22400.48 - 22500.96
- **Entrée**: 22502.49 @ 2025-06-11 07:34:00
- **Stop Loss**: 22389.28
- **Risk**: 113.21 points
- **TP 1RR**: 22615.70 ❌
- **TP 2RR**: 22728.92 ❌
- **TP 3RR**: 22842.13 ❌
- **TP 4RR**: 22955.34 ❌
- **TP 15RR**: 24200.66 ❌
- **PnL**: -113.21 points (-1.0R)
- **MFE**: 35.96 points
- **MAE**: 140.77 points

### Trade #1042 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 07:45:00
- **FVG 5m**: 22444.86 - 22456.33
- **Entrée**: 22418.08 @ 2025-06-11 08:31:00
- **Stop Loss**: 22467.56
- **Risk**: 49.48 points
- **TP 1RR**: 22368.60 ✅
- **TP 2RR**: 22319.12 ❌
- **TP 3RR**: 22269.63 ❌
- **TP 4RR**: 22220.15 ❌
- **TP 15RR**: 21675.85 ❌
- **PnL**: -49.48 points (-1.0R)
- **MFE**: 61.72 points
- **MAE**: 52.28 points

### Trade #1043 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 07:45:00
- **FVG 5m**: 22444.86 - 22456.33
- **Entrée**: 22418.08 @ 2025-06-11 08:31:00
- **Stop Loss**: 22467.56
- **Risk**: 49.48 points
- **TP 1RR**: 22368.60 ✅
- **TP 2RR**: 22319.12 ❌
- **TP 3RR**: 22269.63 ❌
- **TP 4RR**: 22220.15 ❌
- **TP 15RR**: 21675.85 ❌
- **PnL**: -49.48 points (-1.0R)
- **MFE**: 61.72 points
- **MAE**: 52.28 points

### Trade #1044 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 07:45:00
- **FVG 5m**: 22444.86 - 22456.33
- **Entrée**: 22418.08 @ 2025-06-11 08:31:00
- **Stop Loss**: 22467.56
- **Risk**: 49.48 points
- **TP 1RR**: 22368.60 ✅
- **TP 2RR**: 22319.12 ❌
- **TP 3RR**: 22269.63 ❌
- **TP 4RR**: 22220.15 ❌
- **TP 15RR**: 21675.85 ❌
- **PnL**: -49.48 points (-1.0R)
- **MFE**: 61.72 points
- **MAE**: 52.28 points

### Trade #1045 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 08:30:00
- **FVG 5m**: 22478.52 - 22498.67
- **Entrée**: 22441.54 @ 2025-06-11 10:09:00
- **Stop Loss**: 22509.92
- **Risk**: 68.38 points
- **TP 1RR**: 22373.17 ✅
- **TP 2RR**: 22304.79 ✅
- **TP 3RR**: 22236.42 ✅
- **TP 4RR**: 22168.04 ✅
- **TP 15RR**: 21415.91 ❌
- **PnL**: -68.38 points (-1.0R)
- **MFE**: 661.20 points
- **MAE**: 68.46 points

### Trade #1046 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 08:30:00
- **FVG 5m**: 22478.52 - 22498.67
- **Entrée**: 22441.54 @ 2025-06-11 10:09:00
- **Stop Loss**: 22509.92
- **Risk**: 68.38 points
- **TP 1RR**: 22373.17 ✅
- **TP 2RR**: 22304.79 ✅
- **TP 3RR**: 22236.42 ✅
- **TP 4RR**: 22168.04 ✅
- **TP 15RR**: 21415.91 ❌
- **PnL**: -68.38 points (-1.0R)
- **MFE**: 661.20 points
- **MAE**: 68.46 points

### Trade #1047 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 13:15:00
- **FVG 5m**: 22335.20 - 22342.59
- **Entrée**: 22344.12 @ 2025-06-11 15:17:00
- **Stop Loss**: 22324.03
- **Risk**: 20.09 points
- **TP 1RR**: 22364.22 ❌
- **TP 2RR**: 22384.31 ❌
- **TP 3RR**: 22404.40 ❌
- **TP 4RR**: 22424.50 ❌
- **TP 15RR**: 22645.53 ❌
- **PnL**: -20.09 points (-1.0R)
- **MFE**: 7.14 points
- **MAE**: 20.40 points

### Trade #1048 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 13:30:00
- **FVG 5m**: 22335.20 - 22342.59
- **Entrée**: 22344.12 @ 2025-06-11 15:17:00
- **Stop Loss**: 22324.03
- **Risk**: 20.09 points
- **TP 1RR**: 22364.22 ❌
- **TP 2RR**: 22384.31 ❌
- **TP 3RR**: 22404.40 ❌
- **TP 4RR**: 22424.50 ❌
- **TP 15RR**: 22645.53 ❌
- **PnL**: -20.09 points (-1.0R)
- **MFE**: 7.14 points
- **MAE**: 20.40 points

### Trade #1049 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 13:30:00
- **FVG 5m**: 22335.20 - 22342.59
- **Entrée**: 22344.12 @ 2025-06-11 15:17:00
- **Stop Loss**: 22324.03
- **Risk**: 20.09 points
- **TP 1RR**: 22364.22 ❌
- **TP 2RR**: 22384.31 ❌
- **TP 3RR**: 22404.40 ❌
- **TP 4RR**: 22424.50 ❌
- **TP 15RR**: 22645.53 ❌
- **PnL**: -20.09 points (-1.0R)
- **MFE**: 7.14 points
- **MAE**: 20.40 points

### Trade #1050 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22179.25
- **Risk**: 20.79 points
- **TP 1RR**: 22220.82 ✅
- **TP 2RR**: 22241.61 ✅
- **TP 3RR**: 22262.39 ✅
- **TP 4RR**: 22283.18 ❌
- **TP 15RR**: 22511.83 ❌
- **PnL**: -20.79 points (-1.0R)
- **MFE**: 82.37 points
- **MAE**: 31.11 points

### Trade #1051 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22179.25
- **Risk**: 20.79 points
- **TP 1RR**: 22220.82 ✅
- **TP 2RR**: 22241.61 ✅
- **TP 3RR**: 22262.39 ✅
- **TP 4RR**: 22283.18 ❌
- **TP 15RR**: 22511.83 ❌
- **PnL**: -20.79 points (-1.0R)
- **MFE**: 82.37 points
- **MAE**: 31.11 points

### Trade #1052 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22179.25
- **Risk**: 20.79 points
- **TP 1RR**: 22220.82 ✅
- **TP 2RR**: 22241.61 ✅
- **TP 3RR**: 22262.39 ✅
- **TP 4RR**: 22283.18 ❌
- **TP 15RR**: 22511.83 ❌
- **PnL**: -20.79 points (-1.0R)
- **MFE**: 82.37 points
- **MAE**: 31.11 points

### Trade #1053 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22179.25
- **Risk**: 20.79 points
- **TP 1RR**: 22220.82 ✅
- **TP 2RR**: 22241.61 ✅
- **TP 3RR**: 22262.39 ✅
- **TP 4RR**: 22283.18 ❌
- **TP 15RR**: 22511.83 ❌
- **PnL**: -20.79 points (-1.0R)
- **MFE**: 82.37 points
- **MAE**: 31.11 points

### Trade #1054 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22179.25
- **Risk**: 20.79 points
- **TP 1RR**: 22220.82 ✅
- **TP 2RR**: 22241.61 ✅
- **TP 3RR**: 22262.39 ✅
- **TP 4RR**: 22283.18 ❌
- **TP 15RR**: 22511.83 ❌
- **PnL**: -20.79 points (-1.0R)
- **MFE**: 82.37 points
- **MAE**: 31.11 points

### Trade #1055 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:45:00
- **FVG 5m**: 22251.04 - 22263.28
- **Entrée**: 22264.81 @ 2025-06-12 04:34:00
- **Stop Loss**: 22239.91
- **Risk**: 24.90 points
- **TP 1RR**: 22289.71 ❌
- **TP 2RR**: 22314.60 ❌
- **TP 3RR**: 22339.50 ❌
- **TP 4RR**: 22364.40 ❌
- **TP 15RR**: 22638.26 ❌
- **PnL**: -24.90 points (-1.0R)
- **MFE**: 17.60 points
- **MAE**: 29.58 points

### Trade #1056 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 08:00:00
- **FVG 5m**: 22372.69 - 22381.36
- **Entrée**: 22369.37 @ 2025-06-12 10:17:00
- **Stop Loss**: 22392.55
- **Risk**: 23.18 points
- **TP 1RR**: 22346.19 ✅
- **TP 2RR**: 22323.02 ✅
- **TP 3RR**: 22299.84 ❌
- **TP 4RR**: 22276.66 ❌
- **TP 15RR**: 22021.72 ❌
- **PnL**: -23.18 points (-1.0R)
- **MFE**: 48.45 points
- **MAE**: 23.46 points

### Trade #1057 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 08:45:00
- **FVG 5m**: 22372.69 - 22381.36
- **Entrée**: 22369.37 @ 2025-06-12 10:17:00
- **Stop Loss**: 22392.55
- **Risk**: 23.18 points
- **TP 1RR**: 22346.19 ✅
- **TP 2RR**: 22323.02 ✅
- **TP 3RR**: 22299.84 ❌
- **TP 4RR**: 22276.66 ❌
- **TP 15RR**: 22021.72 ❌
- **PnL**: -23.18 points (-1.0R)
- **MFE**: 48.45 points
- **MAE**: 23.46 points

### Trade #1058 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 09:00:00
- **FVG 5m**: 22343.10 - 22348.20
- **Entrée**: 22354.58 @ 2025-06-12 09:14:00
- **Stop Loss**: 22331.93
- **Risk**: 22.65 points
- **TP 1RR**: 22377.23 ✅
- **TP 2RR**: 22399.87 ✅
- **TP 3RR**: 22422.52 ❌
- **TP 4RR**: 22445.17 ❌
- **TP 15RR**: 22694.29 ❌
- **PnL**: -22.65 points (-1.0R)
- **MFE**: 64.52 points
- **MAE**: 33.66 points

### Trade #1059 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 09:15:00
- **FVG 5m**: 22368.86 - 22375.75
- **Entrée**: 22380.85 @ 2025-06-12 09:37:00
- **Stop Loss**: 22357.68
- **Risk**: 23.17 points
- **TP 1RR**: 22404.02 ✅
- **TP 2RR**: 22427.19 ❌
- **TP 3RR**: 22450.36 ❌
- **TP 4RR**: 22473.53 ❌
- **TP 15RR**: 22728.41 ❌
- **PnL**: -23.17 points (-1.0R)
- **MFE**: 38.25 points
- **MAE**: 25.76 points

### Trade #1060 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 13:30:00
- **FVG 5m**: 22376.26 - 22379.06
- **Entrée**: 22371.67 @ 2025-06-12 14:27:00
- **Stop Loss**: 22390.25
- **Risk**: 18.59 points
- **TP 1RR**: 22353.08 ✅
- **TP 2RR**: 22334.50 ✅
- **TP 3RR**: 22315.91 ✅
- **TP 4RR**: 22297.32 ✅
- **TP 15RR**: 22092.89 ✅
- **PnL**: 278.78 points (15.0R)
- **MFE**: 299.15 points
- **MAE**: 17.60 points

### Trade #1061 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 19:00:00
- **FVG 5m**: 21981.73 - 21987.34
- **Entrée**: 21990.66 @ 2025-06-12 20:37:00
- **Stop Loss**: 21970.74
- **Risk**: 19.92 points
- **TP 1RR**: 22010.57 ✅
- **TP 2RR**: 22030.49 ✅
- **TP 3RR**: 22050.41 ✅
- **TP 4RR**: 22070.32 ❌
- **TP 15RR**: 22289.41 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 63.25 points
- **MAE**: 20.40 points

### Trade #1062 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 19:00:00
- **FVG 5m**: 21981.73 - 21987.34
- **Entrée**: 21990.66 @ 2025-06-12 20:37:00
- **Stop Loss**: 21970.74
- **Risk**: 19.92 points
- **TP 1RR**: 22010.57 ✅
- **TP 2RR**: 22030.49 ✅
- **TP 3RR**: 22050.41 ✅
- **TP 4RR**: 22070.32 ❌
- **TP 15RR**: 22289.41 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 63.25 points
- **MAE**: 20.40 points

### Trade #1063 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 19:00:00
- **FVG 5m**: 21981.73 - 21987.34
- **Entrée**: 21990.66 @ 2025-06-12 20:37:00
- **Stop Loss**: 21970.74
- **Risk**: 19.92 points
- **TP 1RR**: 22010.57 ✅
- **TP 2RR**: 22030.49 ✅
- **TP 3RR**: 22050.41 ✅
- **TP 4RR**: 22070.32 ❌
- **TP 15RR**: 22289.41 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 63.25 points
- **MAE**: 20.40 points

### Trade #1064 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 19:15:00
- **FVG 5m**: 22008.76 - 22024.32
- **Entrée**: 21976.89 @ 2025-06-12 19:52:00
- **Stop Loss**: 22035.33
- **Risk**: 58.45 points
- **TP 1RR**: 21918.44 ❌
- **TP 2RR**: 21859.99 ❌
- **TP 3RR**: 21801.54 ❌
- **TP 4RR**: 21743.10 ❌
- **TP 15RR**: 21100.18 ❌
- **PnL**: -58.45 points (-1.0R)
- **MFE**: 55.85 points
- **MAE**: 64.01 points

### Trade #1065 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 19:15:00
- **FVG 5m**: 22008.76 - 22024.32
- **Entrée**: 21976.89 @ 2025-06-12 19:52:00
- **Stop Loss**: 22035.33
- **Risk**: 58.45 points
- **TP 1RR**: 21918.44 ❌
- **TP 2RR**: 21859.99 ❌
- **TP 3RR**: 21801.54 ❌
- **TP 4RR**: 21743.10 ❌
- **TP 15RR**: 21100.18 ❌
- **PnL**: -58.45 points (-1.0R)
- **MFE**: 55.85 points
- **MAE**: 64.01 points

### Trade #1066 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 19:15:00
- **FVG 5m**: 22008.76 - 22024.32
- **Entrée**: 21976.89 @ 2025-06-12 19:52:00
- **Stop Loss**: 22035.33
- **Risk**: 58.45 points
- **TP 1RR**: 21918.44 ❌
- **TP 2RR**: 21859.99 ❌
- **TP 3RR**: 21801.54 ❌
- **TP 4RR**: 21743.10 ❌
- **TP 15RR**: 21100.18 ❌
- **PnL**: -58.45 points (-1.0R)
- **MFE**: 55.85 points
- **MAE**: 64.01 points

### Trade #1067 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 21:30:00
- **FVG 5m**: 21993.46 - 22003.92
- **Entrée**: 22006.21 @ 2025-06-12 22:51:00
- **Stop Loss**: 21982.47
- **Risk**: 23.75 points
- **TP 1RR**: 22029.96 ❌
- **TP 2RR**: 22053.71 ❌
- **TP 3RR**: 22077.46 ❌
- **TP 4RR**: 22101.21 ❌
- **TP 15RR**: 22362.43 ❌
- **PnL**: -23.75 points (-1.0R)
- **MFE**: 10.71 points
- **MAE**: 24.23 points

### Trade #1068 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-13 01:15:00
- **FVG 5m**: 22065.63 - 22071.75
- **Entrée**: 22055.94 @ 2025-06-13 03:21:00
- **Stop Loss**: 22082.79
- **Risk**: 26.85 points
- **TP 1RR**: 22029.10 ✅
- **TP 2RR**: 22002.25 ❌
- **TP 3RR**: 21975.40 ❌
- **TP 4RR**: 21948.55 ❌
- **TP 15RR**: 21653.23 ❌
- **PnL**: -26.85 points (-1.0R)
- **MFE**: 45.14 points
- **MAE**: 37.23 points

### Trade #1069 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22109.50 - 22142.40
- **Entrée**: 22151.58 @ 2025-06-13 09:39:00
- **Stop Loss**: 22098.44
- **Risk**: 53.13 points
- **TP 1RR**: 22204.71 ✅
- **TP 2RR**: 22257.85 ✅
- **TP 3RR**: 22310.98 ❌
- **TP 4RR**: 22364.11 ❌
- **TP 15RR**: 22948.59 ❌
- **PnL**: -53.13 points (-1.0R)
- **MFE**: 142.56 points
- **MAE**: 60.19 points

### Trade #1070 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22109.50 - 22142.40
- **Entrée**: 22151.58 @ 2025-06-13 09:39:00
- **Stop Loss**: 22098.44
- **Risk**: 53.13 points
- **TP 1RR**: 22204.71 ✅
- **TP 2RR**: 22257.85 ✅
- **TP 3RR**: 22310.98 ❌
- **TP 4RR**: 22364.11 ❌
- **TP 15RR**: 22948.59 ❌
- **PnL**: -53.13 points (-1.0R)
- **MFE**: 142.56 points
- **MAE**: 60.19 points

### Trade #1071 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22109.50 - 22142.40
- **Entrée**: 22151.58 @ 2025-06-13 09:39:00
- **Stop Loss**: 22098.44
- **Risk**: 53.13 points
- **TP 1RR**: 22204.71 ✅
- **TP 2RR**: 22257.85 ✅
- **TP 3RR**: 22310.98 ❌
- **TP 4RR**: 22364.11 ❌
- **TP 15RR**: 22948.59 ❌
- **PnL**: -53.13 points (-1.0R)
- **MFE**: 142.56 points
- **MAE**: 60.19 points

### Trade #1072 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22109.50 - 22142.40
- **Entrée**: 22151.58 @ 2025-06-13 09:39:00
- **Stop Loss**: 22098.44
- **Risk**: 53.13 points
- **TP 1RR**: 22204.71 ✅
- **TP 2RR**: 22257.85 ✅
- **TP 3RR**: 22310.98 ❌
- **TP 4RR**: 22364.11 ❌
- **TP 15RR**: 22948.59 ❌
- **PnL**: -53.13 points (-1.0R)
- **MFE**: 142.56 points
- **MAE**: 60.19 points

### Trade #1073 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-13 09:00:00
- **FVG 5m**: 22135.77 - 22157.95
- **Entrée**: 22130.67 @ 2025-06-13 09:13:00
- **Stop Loss**: 22169.03
- **Risk**: 38.37 points
- **TP 1RR**: 22092.30 ✅
- **TP 2RR**: 22053.93 ✅
- **TP 3RR**: 22015.57 ❌
- **TP 4RR**: 21977.20 ❌
- **TP 15RR**: 21555.16 ❌
- **PnL**: -38.37 points (-1.0R)
- **MFE**: 79.06 points
- **MAE**: 39.27 points

### Trade #1074 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-13 12:00:00
- **FVG 5m**: 22229.36 - 22242.62
- **Entrée**: 22225.28 @ 2025-06-13 12:11:00
- **Stop Loss**: 22253.74
- **Risk**: 28.46 points
- **TP 1RR**: 22196.82 ✅
- **TP 2RR**: 22168.35 ❌
- **TP 3RR**: 22139.89 ❌
- **TP 4RR**: 22111.43 ❌
- **TP 15RR**: 21798.33 ❌
- **PnL**: -28.46 points (-1.0R)
- **MFE**: 31.88 points
- **MAE**: 34.17 points

### Trade #1075 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-15 17:00:00
- **FVG 5m**: 22054.16 - 22058.49
- **Entrée**: 22064.10 @ 2025-06-15 17:23:00
- **Stop Loss**: 22043.13
- **Risk**: 20.97 points
- **TP 1RR**: 22085.08 ✅
- **TP 2RR**: 22106.05 ✅
- **TP 3RR**: 22127.02 ✅
- **TP 4RR**: 22148.00 ✅
- **TP 15RR**: 22378.70 ✅
- **PnL**: 314.60 points (15.0R)
- **MFE**: 325.72 points
- **MAE**: 17.34 points

### Trade #1076 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-15 17:00:00
- **FVG 5m**: 22054.16 - 22058.49
- **Entrée**: 22064.10 @ 2025-06-15 17:23:00
- **Stop Loss**: 22043.13
- **Risk**: 20.97 points
- **TP 1RR**: 22085.08 ✅
- **TP 2RR**: 22106.05 ✅
- **TP 3RR**: 22127.02 ✅
- **TP 4RR**: 22148.00 ✅
- **TP 15RR**: 22378.70 ✅
- **PnL**: 314.60 points (15.0R)
- **MFE**: 325.72 points
- **MAE**: 17.34 points

### Trade #1077 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-15 21:15:00
- **FVG 5m**: 22132.20 - 22136.28
- **Entrée**: 22131.43 @ 2025-06-15 22:29:00
- **Stop Loss**: 22147.34
- **Risk**: 15.91 points
- **TP 1RR**: 22115.52 ✅
- **TP 2RR**: 22099.60 ❌
- **TP 3RR**: 22083.69 ❌
- **TP 4RR**: 22067.78 ❌
- **TP 15RR**: 21892.73 ❌
- **PnL**: -15.91 points (-1.0R)
- **MFE**: 25.76 points
- **MAE**: 18.29 points

### Trade #1078 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-16 08:45:00
- **FVG 5m**: 22422.90 - 22426.68
- **Entrée**: 22432.24 @ 2025-06-16 10:17:00
- **Stop Loss**: 22411.68
- **Risk**: 20.55 points
- **TP 1RR**: 22452.79 ❌
- **TP 2RR**: 22473.34 ❌
- **TP 3RR**: 22493.90 ❌
- **TP 4RR**: 22514.45 ❌
- **TP 15RR**: 22740.53 ❌
- **PnL**: -20.55 points (-1.0R)
- **MFE**: 9.85 points
- **MAE**: 23.23 points

### Trade #1079 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-16 09:45:00
- **FVG 5m**: 22423.91 - 22426.68
- **Entrée**: 22410.52 @ 2025-06-16 10:26:00
- **Stop Loss**: 22437.90
- **Risk**: 27.37 points
- **TP 1RR**: 22383.15 ✅
- **TP 2RR**: 22355.78 ✅
- **TP 3RR**: 22328.41 ✅
- **TP 4RR**: 22301.04 ✅
- **TP 15RR**: 21999.95 ✅
- **PnL**: 410.58 points (15.0R)
- **MFE**: 412.04 points
- **MAE**: 21.21 points

### Trade #1080 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-16 10:15:00
- **FVG 5m**: 22423.91 - 22426.68
- **Entrée**: 22410.52 @ 2025-06-16 10:26:00
- **Stop Loss**: 22437.90
- **Risk**: 27.37 points
- **TP 1RR**: 22383.15 ✅
- **TP 2RR**: 22355.78 ✅
- **TP 3RR**: 22328.41 ✅
- **TP 4RR**: 22301.04 ✅
- **TP 15RR**: 21999.95 ✅
- **PnL**: 410.58 points (15.0R)
- **MFE**: 412.04 points
- **MAE**: 21.21 points

### Trade #1081 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-16 18:30:00
- **FVG 5m**: 22270.65 - 22275.20
- **Entrée**: 22256.51 @ 2025-06-16 18:48:00
- **Stop Loss**: 22286.33
- **Risk**: 29.82 points
- **TP 1RR**: 22226.69 ✅
- **TP 2RR**: 22196.87 ❌
- **TP 3RR**: 22167.05 ❌
- **TP 4RR**: 22137.23 ❌
- **TP 15RR**: 21809.20 ❌
- **PnL**: -29.82 points (-1.0R)
- **MFE**: 31.05 points
- **MAE**: 32.06 points

### Trade #1082 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-16 22:00:00
- **FVG 5m**: 22279.74 - 22289.08
- **Entrée**: 22277.47 @ 2025-06-16 23:33:00
- **Stop Loss**: 22300.23
- **Risk**: 22.76 points
- **TP 1RR**: 22254.71 ❌
- **TP 2RR**: 22231.95 ❌
- **TP 3RR**: 22209.19 ❌
- **TP 4RR**: 22186.44 ❌
- **TP 15RR**: 21936.09 ❌
- **PnL**: -22.76 points (-1.0R)
- **MFE**: 6.82 points
- **MAE**: 23.99 points

### Trade #1083 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 02:15:00
- **FVG 5m**: 22256.26 - 22259.04
- **Entrée**: 22263.84 @ 2025-06-17 04:44:00
- **Stop Loss**: 22245.13
- **Risk**: 18.70 points
- **TP 1RR**: 22282.54 ❌
- **TP 2RR**: 22301.24 ❌
- **TP 3RR**: 22319.94 ❌
- **TP 4RR**: 22338.65 ❌
- **TP 15RR**: 22544.37 ❌
- **PnL**: -18.70 points (-1.0R)
- **MFE**: 6.06 points
- **MAE**: 19.69 points

### Trade #1084 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 03:15:00
- **FVG 5m**: 22256.26 - 22259.04
- **Entrée**: 22263.84 @ 2025-06-17 04:44:00
- **Stop Loss**: 22245.13
- **Risk**: 18.70 points
- **TP 1RR**: 22282.54 ❌
- **TP 2RR**: 22301.24 ❌
- **TP 3RR**: 22319.94 ❌
- **TP 4RR**: 22338.65 ❌
- **TP 15RR**: 22544.37 ❌
- **PnL**: -18.70 points (-1.0R)
- **MFE**: 6.06 points
- **MAE**: 19.69 points

### Trade #1085 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-17 05:30:00
- **FVG 5m**: 22278.98 - 22293.63
- **Entrée**: 22275.95 @ 2025-06-17 07:49:00
- **Stop Loss**: 22304.77
- **Risk**: 28.82 points
- **TP 1RR**: 22247.13 ❌
- **TP 2RR**: 22218.31 ❌
- **TP 3RR**: 22189.49 ❌
- **TP 4RR**: 22160.67 ❌
- **TP 15RR**: 21843.65 ❌
- **PnL**: -28.82 points (-1.0R)
- **MFE**: 24.74 points
- **MAE**: 47.47 points

### Trade #1086 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 05:45:00
- **FVG 5m**: 22273.18 - 22284.79
- **Entrée**: 22285.80 @ 2025-06-17 06:56:00
- **Stop Loss**: 22262.04
- **Risk**: 23.76 points
- **TP 1RR**: 22309.56 ✅
- **TP 2RR**: 22333.32 ❌
- **TP 3RR**: 22357.08 ❌
- **TP 4RR**: 22380.84 ❌
- **TP 15RR**: 22642.21 ❌
- **PnL**: -23.76 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 27.52 points

### Trade #1087 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 05:45:00
- **FVG 5m**: 22273.18 - 22284.79
- **Entrée**: 22285.80 @ 2025-06-17 06:56:00
- **Stop Loss**: 22262.04
- **Risk**: 23.76 points
- **TP 1RR**: 22309.56 ✅
- **TP 2RR**: 22333.32 ❌
- **TP 3RR**: 22357.08 ❌
- **TP 4RR**: 22380.84 ❌
- **TP 15RR**: 22642.21 ❌
- **PnL**: -23.76 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 27.52 points

### Trade #1088 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-17 07:30:00
- **FVG 5m**: 22278.98 - 22293.63
- **Entrée**: 22275.95 @ 2025-06-17 07:49:00
- **Stop Loss**: 22304.77
- **Risk**: 28.82 points
- **TP 1RR**: 22247.13 ❌
- **TP 2RR**: 22218.31 ❌
- **TP 3RR**: 22189.49 ❌
- **TP 4RR**: 22160.67 ❌
- **TP 15RR**: 21843.65 ❌
- **PnL**: -28.82 points (-1.0R)
- **MFE**: 24.74 points
- **MAE**: 47.47 points

### Trade #1089 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-17 09:15:00
- **FVG 5m**: 22314.08 - 22318.12
- **Entrée**: 22312.56 @ 2025-06-17 09:39:00
- **Stop Loss**: 22329.28
- **Risk**: 16.71 points
- **TP 1RR**: 22295.85 ✅
- **TP 2RR**: 22279.14 ❌
- **TP 3RR**: 22262.42 ❌
- **TP 4RR**: 22245.71 ❌
- **TP 15RR**: 22061.86 ❌
- **PnL**: -16.71 points (-1.0R)
- **MFE**: 23.99 points
- **MAE**: 18.68 points

### Trade #1090 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-17 09:15:00
- **FVG 5m**: 22314.08 - 22318.12
- **Entrée**: 22312.56 @ 2025-06-17 09:39:00
- **Stop Loss**: 22329.28
- **Risk**: 16.71 points
- **TP 1RR**: 22295.85 ✅
- **TP 2RR**: 22279.14 ❌
- **TP 3RR**: 22262.42 ❌
- **TP 4RR**: 22245.71 ❌
- **TP 15RR**: 22061.86 ❌
- **PnL**: -16.71 points (-1.0R)
- **MFE**: 23.99 points
- **MAE**: 18.68 points

### Trade #1091 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 12:00:00
- **FVG 5m**: 22194.15 - 22196.68
- **Entrée**: 22199.20 @ 2025-06-17 14:21:00
- **Stop Loss**: 22183.06
- **Risk**: 16.15 points
- **TP 1RR**: 22215.35 ❌
- **TP 2RR**: 22231.49 ❌
- **TP 3RR**: 22247.64 ❌
- **TP 4RR**: 22263.79 ❌
- **TP 15RR**: 22441.40 ❌
- **PnL**: -16.15 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 20.20 points

### Trade #1092 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 12:30:00
- **FVG 5m**: 22194.15 - 22196.68
- **Entrée**: 22199.20 @ 2025-06-17 14:21:00
- **Stop Loss**: 22183.06
- **Risk**: 16.15 points
- **TP 1RR**: 22215.35 ❌
- **TP 2RR**: 22231.49 ❌
- **TP 3RR**: 22247.64 ❌
- **TP 4RR**: 22263.79 ❌
- **TP 15RR**: 22441.40 ❌
- **PnL**: -16.15 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 20.20 points

### Trade #1093 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 12:45:00
- **FVG 5m**: 22194.15 - 22196.68
- **Entrée**: 22199.20 @ 2025-06-17 14:21:00
- **Stop Loss**: 22183.06
- **Risk**: 16.15 points
- **TP 1RR**: 22215.35 ❌
- **TP 2RR**: 22231.49 ❌
- **TP 3RR**: 22247.64 ❌
- **TP 4RR**: 22263.79 ❌
- **TP 15RR**: 22441.40 ❌
- **PnL**: -16.15 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 20.20 points

### Trade #1094 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 17:30:00
- **FVG 5m**: 22182.54 - 22192.38
- **Entrée**: 22195.92 @ 2025-06-17 19:36:00
- **Stop Loss**: 22171.45
- **Risk**: 24.47 points
- **TP 1RR**: 22220.39 ✅
- **TP 2RR**: 22244.86 ❌
- **TP 3RR**: 22269.34 ❌
- **TP 4RR**: 22293.81 ❌
- **TP 15RR**: 22563.01 ❌
- **PnL**: -24.47 points (-1.0R)
- **MFE**: 32.82 points
- **MAE**: 26.76 points

### Trade #1095 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 01:00:00
- **FVG 5m**: 22235.81 - 22241.87
- **Entrée**: 22243.89 @ 2025-06-18 03:04:00
- **Stop Loss**: 22224.69
- **Risk**: 19.20 points
- **TP 1RR**: 22263.09 ❌
- **TP 2RR**: 22282.28 ❌
- **TP 3RR**: 22301.48 ❌
- **TP 4RR**: 22320.68 ❌
- **TP 15RR**: 22531.85 ❌
- **PnL**: -19.20 points (-1.0R)
- **MFE**: 10.86 points
- **MAE**: 20.20 points

### Trade #1096 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-18 07:15:00
- **FVG 5m**: 22213.34 - 22223.19
- **Entrée**: 22210.82 @ 2025-06-18 08:29:00
- **Stop Loss**: 22234.30
- **Risk**: 23.48 points
- **TP 1RR**: 22187.33 ✅
- **TP 2RR**: 22163.85 ✅
- **TP 3RR**: 22140.37 ❌
- **TP 4RR**: 22116.88 ❌
- **TP 15RR**: 21858.57 ❌
- **PnL**: -23.48 points (-1.0R)
- **MFE**: 67.41 points
- **MAE**: 29.54 points

### Trade #1097 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 08:30:00
- **FVG 5m**: 22184.31 - 22188.85
- **Entrée**: 22192.38 @ 2025-06-18 08:41:00
- **Stop Loss**: 22173.21
- **Risk**: 19.17 points
- **TP 1RR**: 22211.56 ✅
- **TP 2RR**: 22230.73 ✅
- **TP 3RR**: 22249.90 ✅
- **TP 4RR**: 22269.07 ✅
- **TP 15RR**: 22479.96 ❌
- **PnL**: -19.17 points (-1.0R)
- **MFE**: 124.22 points
- **MAE**: 23.23 points

### Trade #1098 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 08:30:00
- **FVG 5m**: 22184.31 - 22188.85
- **Entrée**: 22192.38 @ 2025-06-18 08:41:00
- **Stop Loss**: 22173.21
- **Risk**: 19.17 points
- **TP 1RR**: 22211.56 ✅
- **TP 2RR**: 22230.73 ✅
- **TP 3RR**: 22249.90 ✅
- **TP 4RR**: 22269.07 ✅
- **TP 15RR**: 22479.96 ❌
- **PnL**: -19.17 points (-1.0R)
- **MFE**: 124.22 points
- **MAE**: 23.23 points

### Trade #1099 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-18 10:00:00
- **FVG 5m**: 22218.39 - 22238.08
- **Entrée**: 22216.62 @ 2025-06-18 12:22:00
- **Stop Loss**: 22249.20
- **Risk**: 32.58 points
- **TP 1RR**: 22184.04 ✅
- **TP 2RR**: 22151.46 ❌
- **TP 3RR**: 22118.88 ❌
- **TP 4RR**: 22086.30 ❌
- **TP 15RR**: 21727.93 ❌
- **PnL**: -32.58 points (-1.0R)
- **MFE**: 59.84 points
- **MAE**: 33.07 points

### Trade #1100 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-18 11:15:00
- **FVG 5m**: 22218.39 - 22238.08
- **Entrée**: 22216.62 @ 2025-06-18 12:22:00
- **Stop Loss**: 22249.20
- **Risk**: 32.58 points
- **TP 1RR**: 22184.04 ✅
- **TP 2RR**: 22151.46 ❌
- **TP 3RR**: 22118.88 ❌
- **TP 4RR**: 22086.30 ❌
- **TP 15RR**: 21727.93 ❌
- **PnL**: -32.58 points (-1.0R)
- **MFE**: 59.84 points
- **MAE**: 33.07 points

### Trade #1101 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 14:00:00
- **FVG 5m**: 22179.00 - 22182.54
- **Entrée**: 22184.81 @ 2025-06-18 15:38:00
- **Stop Loss**: 22167.91
- **Risk**: 16.90 points
- **TP 1RR**: 22201.71 ❌
- **TP 2RR**: 22218.60 ❌
- **TP 3RR**: 22235.50 ❌
- **TP 4RR**: 22252.40 ❌
- **TP 15RR**: 22438.26 ❌
- **PnL**: -16.90 points (-1.0R)
- **MFE**: 10.10 points
- **MAE**: 27.52 points

### Trade #1102 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 19:15:00
- **FVG 5m**: 22103.26 - 22106.04
- **Entrée**: 22109.83 @ 2025-06-18 19:28:00
- **Stop Loss**: 22092.21
- **Risk**: 17.62 points
- **TP 1RR**: 22127.44 ❌
- **TP 2RR**: 22145.06 ❌
- **TP 3RR**: 22162.67 ❌
- **TP 4RR**: 22180.29 ❌
- **TP 15RR**: 22374.07 ❌
- **PnL**: -17.62 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 86.09 points

### Trade #1103 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 19:15:00
- **FVG 5m**: 22103.26 - 22106.04
- **Entrée**: 22109.83 @ 2025-06-18 19:28:00
- **Stop Loss**: 22092.21
- **Risk**: 17.62 points
- **TP 1RR**: 22127.44 ❌
- **TP 2RR**: 22145.06 ❌
- **TP 3RR**: 22162.67 ❌
- **TP 4RR**: 22180.29 ❌
- **TP 15RR**: 22374.07 ❌
- **PnL**: -17.62 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 86.09 points

### Trade #1104 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 08:15:00
- **FVG 5m**: 21915.17 - 21917.69
- **Entrée**: 21918.95 @ 2025-06-19 09:07:00
- **Stop Loss**: 21904.21
- **Risk**: 14.74 points
- **TP 1RR**: 21933.70 ✅
- **TP 2RR**: 21948.44 ❌
- **TP 3RR**: 21963.19 ❌
- **TP 4RR**: 21977.93 ❌
- **TP 15RR**: 22140.12 ❌
- **PnL**: -14.74 points (-1.0R)
- **MFE**: 25.75 points
- **MAE**: 14.90 points

### Trade #1105 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-19 08:45:00
- **FVG 5m**: 21919.71 - 21921.98
- **Entrée**: 21919.46 @ 2025-06-19 10:34:00
- **Stop Loss**: 21932.94
- **Risk**: 13.49 points
- **TP 1RR**: 21905.97 ✅
- **TP 2RR**: 21892.49 ❌
- **TP 3RR**: 21879.00 ❌
- **TP 4RR**: 21865.52 ❌
- **TP 15RR**: 21717.17 ❌
- **PnL**: -13.49 points (-1.0R)
- **MFE**: 13.89 points
- **MAE**: 14.64 points

### Trade #1106 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 09:00:00
- **FVG 5m**: 21923.25 - 21931.58
- **Entrée**: 21932.08 @ 2025-06-19 09:54:00
- **Stop Loss**: 21912.28
- **Risk**: 19.80 points
- **TP 1RR**: 21951.88 ✅
- **TP 2RR**: 21971.68 ❌
- **TP 3RR**: 21991.48 ❌
- **TP 4RR**: 22011.28 ❌
- **TP 15RR**: 22229.06 ❌
- **PnL**: -19.80 points (-1.0R)
- **MFE**: 23.99 points
- **MAE**: 25.00 points

### Trade #1107 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 09:00:00
- **FVG 5m**: 21923.25 - 21931.58
- **Entrée**: 21932.08 @ 2025-06-19 09:54:00
- **Stop Loss**: 21912.28
- **Risk**: 19.80 points
- **TP 1RR**: 21951.88 ✅
- **TP 2RR**: 21971.68 ❌
- **TP 3RR**: 21991.48 ❌
- **TP 4RR**: 22011.28 ❌
- **TP 15RR**: 22229.06 ❌
- **PnL**: -19.80 points (-1.0R)
- **MFE**: 23.99 points
- **MAE**: 25.00 points

### Trade #1108 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 09:45:00
- **FVG 5m**: 21919.71 - 21928.30
- **Entrée**: 21928.80 @ 2025-06-19 10:44:00
- **Stop Loss**: 21908.75
- **Risk**: 20.05 points
- **TP 1RR**: 21948.85 ❌
- **TP 2RR**: 21968.90 ❌
- **TP 3RR**: 21988.95 ❌
- **TP 4RR**: 22009.00 ❌
- **TP 15RR**: 22229.53 ❌
- **PnL**: -20.05 points (-1.0R)
- **MFE**: 11.11 points
- **MAE**: 22.47 points

### Trade #1109 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 17:00:00
- **FVG 5m**: 22067.41 - 22082.05
- **Entrée**: 22087.61 @ 2025-06-19 17:33:00
- **Stop Loss**: 22056.38
- **Risk**: 31.23 points
- **TP 1RR**: 22118.84 ✅
- **TP 2RR**: 22150.07 ✅
- **TP 3RR**: 22181.30 ✅
- **TP 4RR**: 22212.53 ✅
- **TP 15RR**: 22556.08 ❌
- **PnL**: -31.23 points (-1.0R)
- **MFE**: 262.07 points
- **MAE**: 50.24 points

### Trade #1110 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-19 17:30:00
- **FVG 5m**: 22104.78 - 22107.55
- **Entrée**: 22099.22 @ 2025-06-19 18:04:00
- **Stop Loss**: 22118.61
- **Risk**: 19.39 points
- **TP 1RR**: 22079.84 ❌
- **TP 2RR**: 22060.45 ❌
- **TP 3RR**: 22041.06 ❌
- **TP 4RR**: 22021.68 ❌
- **TP 15RR**: 21808.44 ❌
- **PnL**: -19.39 points (-1.0R)
- **MFE**: 10.35 points
- **MAE**: 22.22 points

### Trade #1111 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 19:00:00
- **FVG 5m**: 22080.03 - 22088.62
- **Entrée**: 22090.64 @ 2025-06-19 20:16:00
- **Stop Loss**: 22068.99
- **Risk**: 21.64 points
- **TP 1RR**: 22112.28 ❌
- **TP 2RR**: 22133.93 ❌
- **TP 3RR**: 22155.57 ❌
- **TP 4RR**: 22177.21 ❌
- **TP 15RR**: 22415.30 ❌
- **PnL**: -21.64 points (-1.0R)
- **MFE**: 11.11 points
- **MAE**: 24.24 points

### Trade #1112 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 03:15:00
- **FVG 5m**: 22132.04 - 22137.85
- **Entrée**: 22130.28 @ 2025-06-20 03:28:00
- **Stop Loss**: 22148.92
- **Risk**: 18.64 points
- **TP 1RR**: 22111.63 ✅
- **TP 2RR**: 22092.99 ✅
- **TP 3RR**: 22074.35 ❌
- **TP 4RR**: 22055.70 ❌
- **TP 15RR**: 21850.63 ❌
- **PnL**: -18.64 points (-1.0R)
- **MFE**: 54.79 points
- **MAE**: 19.95 points

### Trade #1113 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 04:00:00
- **FVG 5m**: 22104.27 - 22109.32
- **Entrée**: 22110.08 @ 2025-06-20 04:14:00
- **Stop Loss**: 22093.22
- **Risk**: 16.86 points
- **TP 1RR**: 22126.94 ✅
- **TP 2RR**: 22143.80 ✅
- **TP 3RR**: 22160.65 ✅
- **TP 4RR**: 22177.51 ✅
- **TP 15RR**: 22362.96 ❌
- **PnL**: -16.86 points (-1.0R)
- **MFE**: 239.60 points
- **MAE**: 26.76 points

### Trade #1114 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 04:00:00
- **FVG 5m**: 22104.27 - 22109.32
- **Entrée**: 22110.08 @ 2025-06-20 04:14:00
- **Stop Loss**: 22093.22
- **Risk**: 16.86 points
- **TP 1RR**: 22126.94 ✅
- **TP 2RR**: 22143.80 ✅
- **TP 3RR**: 22160.65 ✅
- **TP 4RR**: 22177.51 ✅
- **TP 15RR**: 22362.96 ❌
- **PnL**: -16.86 points (-1.0R)
- **MFE**: 239.60 points
- **MAE**: 26.76 points

### Trade #1115 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 08:15:00
- **FVG 5m**: 22286.56 - 22317.87
- **Entrée**: 22284.29 @ 2025-06-20 08:49:00
- **Stop Loss**: 22329.02
- **Risk**: 44.74 points
- **TP 1RR**: 22239.55 ✅
- **TP 2RR**: 22194.81 ✅
- **TP 3RR**: 22150.07 ✅
- **TP 4RR**: 22105.33 ✅
- **TP 15RR**: 21613.21 ❌
- **PnL**: -44.74 points (-1.0R)
- **MFE**: 503.94 points
- **MAE**: 85.08 points

### Trade #1116 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 08:45:00
- **FVG 5m**: 22244.90 - 22250.71
- **Entrée**: 22243.39 @ 2025-06-20 08:58:00
- **Stop Loss**: 22261.83
- **Risk**: 18.45 points
- **TP 1RR**: 22224.94 ✅
- **TP 2RR**: 22206.49 ✅
- **TP 3RR**: 22188.04 ✅
- **TP 4RR**: 22169.60 ✅
- **TP 15RR**: 21966.68 ✅
- **PnL**: 276.71 points (15.0R)
- **MFE**: 463.04 points
- **MAE**: 5.05 points

### Trade #1117 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:15:00
- **FVG 5m**: 22097.20 - 22141.89
- **Entrée**: 22069.43 @ 2025-06-20 09:45:00
- **Stop Loss**: 22152.96
- **Risk**: 83.53 points
- **TP 1RR**: 21985.90 ✅
- **TP 2RR**: 21902.37 ✅
- **TP 3RR**: 21818.83 ✅
- **TP 4RR**: 21735.30 ❌
- **TP 15RR**: 20816.46 ❌
- **PnL**: -83.53 points (-1.0R)
- **MFE**: 289.08 points
- **MAE**: 86.85 points

### Trade #1118 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:15:00
- **FVG 5m**: 22097.20 - 22141.89
- **Entrée**: 22069.43 @ 2025-06-20 09:45:00
- **Stop Loss**: 22152.96
- **Risk**: 83.53 points
- **TP 1RR**: 21985.90 ✅
- **TP 2RR**: 21902.37 ✅
- **TP 3RR**: 21818.83 ✅
- **TP 4RR**: 21735.30 ❌
- **TP 15RR**: 20816.46 ❌
- **PnL**: -83.53 points (-1.0R)
- **MFE**: 289.08 points
- **MAE**: 86.85 points

### Trade #1119 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:15:00
- **FVG 5m**: 22097.20 - 22141.89
- **Entrée**: 22069.43 @ 2025-06-20 09:45:00
- **Stop Loss**: 22152.96
- **Risk**: 83.53 points
- **TP 1RR**: 21985.90 ✅
- **TP 2RR**: 21902.37 ✅
- **TP 3RR**: 21818.83 ✅
- **TP 4RR**: 21735.30 ❌
- **TP 15RR**: 20816.46 ❌
- **PnL**: -83.53 points (-1.0R)
- **MFE**: 289.08 points
- **MAE**: 86.85 points

### Trade #1120 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:45:00
- **FVG 5m**: 22081.04 - 22112.60
- **Entrée**: 22073.22 @ 2025-06-20 10:54:00
- **Stop Loss**: 22123.66
- **Risk**: 50.44 points
- **TP 1RR**: 22022.77 ❌
- **TP 2RR**: 21972.33 ❌
- **TP 3RR**: 21921.89 ❌
- **TP 4RR**: 21871.45 ❌
- **TP 15RR**: 21316.58 ❌
- **PnL**: -50.44 points (-1.0R)
- **MFE**: 23.73 points
- **MAE**: 60.59 points

### Trade #1121 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 10:00:00
- **FVG 5m**: 22038.37 - 22062.86
- **Entrée**: 22069.68 @ 2025-06-20 10:14:00
- **Stop Loss**: 22027.36
- **Risk**: 42.33 points
- **TP 1RR**: 22112.01 ✅
- **TP 2RR**: 22154.33 ❌
- **TP 3RR**: 22196.66 ❌
- **TP 4RR**: 22238.99 ❌
- **TP 15RR**: 22704.57 ❌
- **PnL**: -42.33 points (-1.0R)
- **MFE**: 69.43 points
- **MAE**: 58.07 points

### Trade #1122 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 11:15:00
- **FVG 5m**: 22028.28 - 22038.88
- **Entrée**: 22041.66 @ 2025-06-20 12:53:00
- **Stop Loss**: 22017.26
- **Risk**: 24.40 points
- **TP 1RR**: 22066.05 ✅
- **TP 2RR**: 22090.45 ✅
- **TP 3RR**: 22114.84 ✅
- **TP 4RR**: 22139.24 ❌
- **TP 15RR**: 22407.59 ❌
- **PnL**: -24.40 points (-1.0R)
- **MFE**: 76.25 points
- **MAE**: 32.06 points

### Trade #1123 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 12:30:00
- **FVG 5m**: 22028.28 - 22038.88
- **Entrée**: 22041.66 @ 2025-06-20 12:53:00
- **Stop Loss**: 22017.26
- **Risk**: 24.40 points
- **TP 1RR**: 22066.05 ✅
- **TP 2RR**: 22090.45 ✅
- **TP 3RR**: 22114.84 ✅
- **TP 4RR**: 22139.24 ❌
- **TP 15RR**: 22407.59 ❌
- **PnL**: -24.40 points (-1.0R)
- **MFE**: 76.25 points
- **MAE**: 32.06 points

### Trade #1124 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-22 17:00:00
- **FVG 5m**: 21943.19 - 21953.04
- **Entrée**: 21955.31 @ 2025-06-22 17:28:00
- **Stop Loss**: 21932.22
- **Risk**: 23.09 points
- **TP 1RR**: 21978.40 ✅
- **TP 2RR**: 22001.49 ✅
- **TP 3RR**: 22024.58 ❌
- **TP 4RR**: 22047.67 ❌
- **TP 15RR**: 22301.67 ❌
- **PnL**: -23.09 points (-1.0R)
- **MFE**: 47.47 points
- **MAE**: 25.25 points

### Trade #1125 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-22 17:00:00
- **FVG 5m**: 21943.19 - 21953.04
- **Entrée**: 21955.31 @ 2025-06-22 17:28:00
- **Stop Loss**: 21932.22
- **Risk**: 23.09 points
- **TP 1RR**: 21978.40 ✅
- **TP 2RR**: 22001.49 ✅
- **TP 3RR**: 22024.58 ❌
- **TP 4RR**: 22047.67 ❌
- **TP 15RR**: 22301.67 ❌
- **PnL**: -23.09 points (-1.0R)
- **MFE**: 47.47 points
- **MAE**: 25.25 points

### Trade #1126 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-22 17:00:00
- **FVG 5m**: 21943.19 - 21953.04
- **Entrée**: 21955.31 @ 2025-06-22 17:28:00
- **Stop Loss**: 21932.22
- **Risk**: 23.09 points
- **TP 1RR**: 21978.40 ✅
- **TP 2RR**: 22001.49 ✅
- **TP 3RR**: 22024.58 ❌
- **TP 4RR**: 22047.67 ❌
- **TP 15RR**: 22301.67 ❌
- **PnL**: -23.09 points (-1.0R)
- **MFE**: 47.47 points
- **MAE**: 25.25 points

### Trade #1127 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-22 17:15:00
- **FVG 5m**: 21935.36 - 21940.16
- **Entrée**: 21935.11 @ 2025-06-22 19:18:00
- **Stop Loss**: 21951.13
- **Risk**: 16.02 points
- **TP 1RR**: 21919.09 ❌
- **TP 2RR**: 21903.07 ❌
- **TP 3RR**: 21887.05 ❌
- **TP 4RR**: 21871.03 ❌
- **TP 15RR**: 21694.82 ❌
- **PnL**: -16.02 points (-1.0R)
- **MFE**: 13.13 points
- **MAE**: 19.19 points

### Trade #1128 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 04:15:00
- **FVG 5m**: 22074.98 - 22083.32
- **Entrée**: 22066.90 @ 2025-06-23 05:41:00
- **Stop Loss**: 22094.36
- **Risk**: 27.45 points
- **TP 1RR**: 22039.45 ✅
- **TP 2RR**: 22012.00 ✅
- **TP 3RR**: 21984.55 ❌
- **TP 4RR**: 21957.09 ❌
- **TP 15RR**: 21655.12 ❌
- **PnL**: -27.45 points (-1.0R)
- **MFE**: 76.25 points
- **MAE**: 28.53 points

### Trade #1129 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 04:15:00
- **FVG 5m**: 22074.98 - 22083.32
- **Entrée**: 22066.90 @ 2025-06-23 05:41:00
- **Stop Loss**: 22094.36
- **Risk**: 27.45 points
- **TP 1RR**: 22039.45 ✅
- **TP 2RR**: 22012.00 ✅
- **TP 3RR**: 21984.55 ❌
- **TP 4RR**: 21957.09 ❌
- **TP 15RR**: 21655.12 ❌
- **PnL**: -27.45 points (-1.0R)
- **MFE**: 76.25 points
- **MAE**: 28.53 points

### Trade #1130 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 08:30:00
- **FVG 5m**: 22102.50 - 22109.83
- **Entrée**: 22112.60 @ 2025-06-23 08:47:00
- **Stop Loss**: 22091.45
- **Risk**: 21.15 points
- **TP 1RR**: 22133.75 ✅
- **TP 2RR**: 22154.90 ✅
- **TP 3RR**: 22176.05 ✅
- **TP 4RR**: 22197.20 ✅
- **TP 15RR**: 22429.86 ❌
- **PnL**: -21.15 points (-1.0R)
- **MFE**: 123.46 points
- **MAE**: 26.26 points

### Trade #1131 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 10:45:00
- **FVG 5m**: 22107.30 - 22124.97
- **Entrée**: 22106.04 @ 2025-06-23 11:24:00
- **Stop Loss**: 22136.04
- **Risk**: 30.00 points
- **TP 1RR**: 22076.04 ✅
- **TP 2RR**: 22046.04 ✅
- **TP 3RR**: 22016.04 ✅
- **TP 4RR**: 21986.05 ✅
- **TP 15RR**: 21656.07 ❌
- **PnL**: -30.00 points (-1.0R)
- **MFE**: 152.50 points
- **MAE**: 39.13 points

### Trade #1132 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 11:30:00
- **FVG 5m**: 22033.07 - 22058.83
- **Entrée**: 22069.68 @ 2025-06-23 11:41:00
- **Stop Loss**: 22022.06
- **Risk**: 47.63 points
- **TP 1RR**: 22117.31 ✅
- **TP 2RR**: 22164.93 ✅
- **TP 3RR**: 22212.56 ✅
- **TP 4RR**: 22260.18 ✅
- **TP 15RR**: 22784.06 ✅
- **PnL**: 714.38 points (15.0R)
- **MFE**: 715.77 points
- **MAE**: 32.06 points

### Trade #1133 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 11:30:00
- **FVG 5m**: 22033.07 - 22058.83
- **Entrée**: 22069.68 @ 2025-06-23 11:41:00
- **Stop Loss**: 22022.06
- **Risk**: 47.63 points
- **TP 1RR**: 22117.31 ✅
- **TP 2RR**: 22164.93 ✅
- **TP 3RR**: 22212.56 ✅
- **TP 4RR**: 22260.18 ✅
- **TP 15RR**: 22784.06 ✅
- **PnL**: 714.38 points (15.0R)
- **MFE**: 715.77 points
- **MAE**: 32.06 points

### Trade #1134 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 17:00:00
- **FVG 5m**: 22382.75 - 22390.33
- **Entrée**: 22394.11 @ 2025-06-23 17:14:00
- **Stop Loss**: 22371.56
- **Risk**: 22.55 points
- **TP 1RR**: 22416.67 ✅
- **TP 2RR**: 22439.22 ✅
- **TP 3RR**: 22461.77 ✅
- **TP 4RR**: 22484.32 ✅
- **TP 15RR**: 22732.41 ✅
- **PnL**: 338.29 points (15.0R)
- **MFE**: 338.32 points
- **MAE**: 6.56 points

### Trade #1135 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 17:00:00
- **FVG 5m**: 22382.75 - 22390.33
- **Entrée**: 22394.11 @ 2025-06-23 17:14:00
- **Stop Loss**: 22371.56
- **Risk**: 22.55 points
- **TP 1RR**: 22416.67 ✅
- **TP 2RR**: 22439.22 ✅
- **TP 3RR**: 22461.77 ✅
- **TP 4RR**: 22484.32 ✅
- **TP 15RR**: 22732.41 ✅
- **PnL**: 338.29 points (15.0R)
- **MFE**: 338.32 points
- **MAE**: 6.56 points

### Trade #1136 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 17:30:00
- **FVG 5m**: 22459.25 - 22462.03
- **Entrée**: 22456.98 @ 2025-06-23 18:30:00
- **Stop Loss**: 22473.26
- **Risk**: 16.28 points
- **TP 1RR**: 22440.70 ✅
- **TP 2RR**: 22424.42 ✅
- **TP 3RR**: 22408.14 ❌
- **TP 4RR**: 22391.86 ❌
- **TP 15RR**: 22212.77 ❌
- **PnL**: -16.28 points (-1.0R)
- **MFE**: 43.17 points
- **MAE**: 25.50 points

### Trade #1137 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-24 02:15:00
- **FVG 5m**: 22551.41 - 22567.56
- **Entrée**: 22546.10 @ 2025-06-24 02:29:00
- **Stop Loss**: 22578.85
- **Risk**: 32.74 points
- **TP 1RR**: 22513.36 ✅
- **TP 2RR**: 22480.62 ✅
- **TP 3RR**: 22447.87 ❌
- **TP 4RR**: 22415.13 ❌
- **TP 15RR**: 22054.94 ❌
- **PnL**: -32.74 points (-1.0R)
- **MFE**: 73.98 points
- **MAE**: 35.35 points

### Trade #1138 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-24 05:00:00
- **FVG 5m**: 22510.25 - 22523.13
- **Entrée**: 22506.46 @ 2025-06-24 07:13:00
- **Stop Loss**: 22534.39
- **Risk**: 27.92 points
- **TP 1RR**: 22478.54 ❌
- **TP 2RR**: 22450.62 ❌
- **TP 3RR**: 22422.69 ❌
- **TP 4RR**: 22394.77 ❌
- **TP 15RR**: 22087.59 ❌
- **PnL**: -27.92 points (-1.0R)
- **MFE**: 27.52 points
- **MAE**: 29.29 points

### Trade #1139 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-24 06:00:00
- **FVG 5m**: 22510.25 - 22523.13
- **Entrée**: 22506.46 @ 2025-06-24 07:13:00
- **Stop Loss**: 22534.39
- **Risk**: 27.92 points
- **TP 1RR**: 22478.54 ❌
- **TP 2RR**: 22450.62 ❌
- **TP 3RR**: 22422.69 ❌
- **TP 4RR**: 22394.77 ❌
- **TP 15RR**: 22087.59 ❌
- **PnL**: -27.92 points (-1.0R)
- **MFE**: 27.52 points
- **MAE**: 29.29 points

### Trade #1140 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-24 11:30:00
- **FVG 5m**: 22625.63 - 22628.92
- **Entrée**: 22630.68 @ 2025-06-24 12:42:00
- **Stop Loss**: 22614.32
- **Risk**: 16.36 points
- **TP 1RR**: 22647.05 ✅
- **TP 2RR**: 22663.41 ✅
- **TP 3RR**: 22679.77 ❌
- **TP 4RR**: 22696.13 ❌
- **TP 15RR**: 22876.12 ❌
- **PnL**: -16.36 points (-1.0R)
- **MFE**: 39.89 points
- **MAE**: 18.68 points

### Trade #1141 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-25 04:15:00
- **FVG 5m**: 22657.19 - 22659.47
- **Entrée**: 22654.67 @ 2025-06-25 04:28:00
- **Stop Loss**: 22670.80
- **Risk**: 16.13 points
- **TP 1RR**: 22638.54 ✅
- **TP 2RR**: 22622.41 ❌
- **TP 3RR**: 22606.29 ❌
- **TP 4RR**: 22590.16 ❌
- **TP 15RR**: 22412.77 ❌
- **PnL**: -16.13 points (-1.0R)
- **MFE**: 19.19 points
- **MAE**: 16.16 points

### Trade #1142 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-25 04:15:00
- **FVG 5m**: 22657.19 - 22659.47
- **Entrée**: 22654.67 @ 2025-06-25 04:28:00
- **Stop Loss**: 22670.80
- **Risk**: 16.13 points
- **TP 1RR**: 22638.54 ✅
- **TP 2RR**: 22622.41 ❌
- **TP 3RR**: 22606.29 ❌
- **TP 4RR**: 22590.16 ❌
- **TP 15RR**: 22412.77 ❌
- **PnL**: -16.13 points (-1.0R)
- **MFE**: 19.19 points
- **MAE**: 16.16 points

### Trade #1143 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-25 10:30:00
- **FVG 5m**: 22655.68 - 22673.35
- **Entrée**: 22655.17 @ 2025-06-25 12:33:00
- **Stop Loss**: 22684.69
- **Risk**: 29.51 points
- **TP 1RR**: 22625.66 ✅
- **TP 2RR**: 22596.14 ❌
- **TP 3RR**: 22566.63 ❌
- **TP 4RR**: 22537.11 ❌
- **TP 15RR**: 22212.45 ❌
- **PnL**: -29.51 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 33.07 points

### Trade #1144 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-25 12:30:00
- **FVG 5m**: 22646.84 - 22651.89
- **Entrée**: 22655.17 @ 2025-06-25 14:02:00
- **Stop Loss**: 22635.52
- **Risk**: 19.66 points
- **TP 1RR**: 22674.83 ✅
- **TP 2RR**: 22694.48 ✅
- **TP 3RR**: 22714.14 ✅
- **TP 4RR**: 22733.79 ✅
- **TP 15RR**: 22950.00 ✅
- **PnL**: 294.83 points (15.0R)
- **MFE**: 294.89 points
- **MAE**: 12.88 points

### Trade #1145 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-25 12:30:00
- **FVG 5m**: 22646.84 - 22651.89
- **Entrée**: 22655.17 @ 2025-06-25 14:02:00
- **Stop Loss**: 22635.52
- **Risk**: 19.66 points
- **TP 1RR**: 22674.83 ✅
- **TP 2RR**: 22694.48 ✅
- **TP 3RR**: 22714.14 ✅
- **TP 4RR**: 22733.79 ✅
- **TP 15RR**: 22950.00 ✅
- **PnL**: 294.83 points (15.0R)
- **MFE**: 294.89 points
- **MAE**: 12.88 points

### Trade #1146 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 03:15:00
- **FVG 5m**: 22776.87 - 22779.39
- **Entrée**: 22780.65 @ 2025-06-26 05:06:00
- **Stop Loss**: 22765.48
- **Risk**: 15.18 points
- **TP 1RR**: 22795.83 ✅
- **TP 2RR**: 22811.01 ❌
- **TP 3RR**: 22826.18 ❌
- **TP 4RR**: 22841.36 ❌
- **TP 15RR**: 23008.29 ❌
- **PnL**: -15.18 points (-1.0R)
- **MFE**: 28.02 points
- **MAE**: 19.69 points

### Trade #1147 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 07:30:00
- **FVG 5m**: 22762.22 - 22767.78
- **Entrée**: 22775.86 @ 2025-06-26 08:20:00
- **Stop Loss**: 22750.84
- **Risk**: 25.01 points
- **TP 1RR**: 22800.87 ❌
- **TP 2RR**: 22825.89 ❌
- **TP 3RR**: 22850.90 ❌
- **TP 4RR**: 22875.92 ❌
- **TP 15RR**: 23151.08 ❌
- **PnL**: -25.01 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 38.88 points

### Trade #1148 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-26 08:30:00
- **FVG 5m**: 22805.65 - 22823.32
- **Entrée**: 22802.37 @ 2025-06-26 10:28:00
- **Stop Loss**: 22834.73
- **Risk**: 32.37 points
- **TP 1RR**: 22770.00 ❌
- **TP 2RR**: 22737.63 ❌
- **TP 3RR**: 22705.27 ❌
- **TP 4RR**: 22672.90 ❌
- **TP 15RR**: 22316.86 ❌
- **PnL**: -32.37 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 40.40 points

### Trade #1149 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-26 09:30:00
- **FVG 5m**: 22805.65 - 22823.32
- **Entrée**: 22802.37 @ 2025-06-26 10:28:00
- **Stop Loss**: 22834.73
- **Risk**: 32.37 points
- **TP 1RR**: 22770.00 ❌
- **TP 2RR**: 22737.63 ❌
- **TP 3RR**: 22705.27 ❌
- **TP 4RR**: 22672.90 ❌
- **TP 15RR**: 22316.86 ❌
- **PnL**: -32.37 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 40.40 points

### Trade #1150 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-26 09:30:00
- **FVG 5m**: 22805.65 - 22823.32
- **Entrée**: 22802.37 @ 2025-06-26 10:28:00
- **Stop Loss**: 22834.73
- **Risk**: 32.37 points
- **TP 1RR**: 22770.00 ❌
- **TP 2RR**: 22737.63 ❌
- **TP 3RR**: 22705.27 ❌
- **TP 4RR**: 22672.90 ❌
- **TP 15RR**: 22316.86 ❌
- **PnL**: -32.37 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 40.40 points

### Trade #1151 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 12:00:00
- **FVG 5m**: 22872.81 - 22881.39
- **Entrée**: 22884.67 @ 2025-06-26 13:08:00
- **Stop Loss**: 22861.37
- **Risk**: 23.30 points
- **TP 1RR**: 22907.98 ✅
- **TP 2RR**: 22931.28 ✅
- **TP 3RR**: 22954.58 ✅
- **TP 4RR**: 22977.89 ✅
- **TP 15RR**: 23234.22 ❌
- **PnL**: -23.30 points (-1.0R)
- **MFE**: 166.89 points
- **MAE**: 26.26 points

### Trade #1152 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 12:00:00
- **FVG 5m**: 22872.81 - 22881.39
- **Entrée**: 22884.67 @ 2025-06-26 13:08:00
- **Stop Loss**: 22861.37
- **Risk**: 23.30 points
- **TP 1RR**: 22907.98 ✅
- **TP 2RR**: 22931.28 ✅
- **TP 3RR**: 22954.58 ✅
- **TP 4RR**: 22977.89 ✅
- **TP 15RR**: 23234.22 ❌
- **PnL**: -23.30 points (-1.0R)
- **MFE**: 166.89 points
- **MAE**: 26.26 points

### Trade #1153 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-26 18:00:00
- **FVG 5m**: 22904.11 - 22907.65
- **Entrée**: 22902.35 @ 2025-06-26 18:11:00
- **Stop Loss**: 22919.10
- **Risk**: 16.76 points
- **TP 1RR**: 22885.59 ✅
- **TP 2RR**: 22868.84 ❌
- **TP 3RR**: 22852.08 ❌
- **TP 4RR**: 22835.32 ❌
- **TP 15RR**: 22651.01 ❌
- **PnL**: -16.76 points (-1.0R)
- **MFE**: 17.67 points
- **MAE**: 17.93 points

### Trade #1154 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:00:00
- **FVG 5m**: 22984.65 - 22992.23
- **Entrée**: 22982.38 @ 2025-06-27 07:15:00
- **Stop Loss**: 23003.72
- **Risk**: 21.34 points
- **TP 1RR**: 22961.04 ✅
- **TP 2RR**: 22939.70 ✅
- **TP 3RR**: 22918.35 ✅
- **TP 4RR**: 22897.01 ❌
- **TP 15RR**: 22662.24 ❌
- **PnL**: -21.34 points (-1.0R)
- **MFE**: 72.46 points
- **MAE**: 35.85 points

### Trade #1155 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:00:00
- **FVG 5m**: 22984.65 - 22992.23
- **Entrée**: 22982.38 @ 2025-06-27 07:15:00
- **Stop Loss**: 23003.72
- **Risk**: 21.34 points
- **TP 1RR**: 22961.04 ✅
- **TP 2RR**: 22939.70 ✅
- **TP 3RR**: 22918.35 ✅
- **TP 4RR**: 22897.01 ❌
- **TP 15RR**: 22662.24 ❌
- **PnL**: -21.34 points (-1.0R)
- **MFE**: 72.46 points
- **MAE**: 35.85 points

### Trade #1156 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:30:00
- **FVG 5m**: 22943.25 - 22952.84
- **Entrée**: 22942.24 @ 2025-06-27 08:01:00
- **Stop Loss**: 22964.32
- **Risk**: 22.08 points
- **TP 1RR**: 22920.16 ✅
- **TP 2RR**: 22898.08 ❌
- **TP 3RR**: 22876.00 ❌
- **TP 4RR**: 22853.92 ❌
- **TP 15RR**: 22611.03 ❌
- **PnL**: -22.08 points (-1.0R)
- **MFE**: 32.32 points
- **MAE**: 25.75 points

### Trade #1157 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:30:00
- **FVG 5m**: 22943.25 - 22952.84
- **Entrée**: 22942.24 @ 2025-06-27 08:01:00
- **Stop Loss**: 22964.32
- **Risk**: 22.08 points
- **TP 1RR**: 22920.16 ✅
- **TP 2RR**: 22898.08 ❌
- **TP 3RR**: 22876.00 ❌
- **TP 4RR**: 22853.92 ❌
- **TP 15RR**: 22611.03 ❌
- **PnL**: -22.08 points (-1.0R)
- **MFE**: 32.32 points
- **MAE**: 25.75 points

### Trade #1158 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 08:00:00
- **FVG 5m**: 23000.81 - 23012.17
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23023.68
- **Risk**: 32.21 points
- **TP 1RR**: 22959.26 ❌
- **TP 2RR**: 22927.05 ❌
- **TP 3RR**: 22894.84 ❌
- **TP 4RR**: 22862.63 ❌
- **TP 15RR**: 22508.33 ❌
- **PnL**: -32.21 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 36.61 points

### Trade #1159 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 08:00:00
- **FVG 5m**: 23000.81 - 23012.17
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23023.68
- **Risk**: 32.21 points
- **TP 1RR**: 22959.26 ❌
- **TP 2RR**: 22927.05 ❌
- **TP 3RR**: 22894.84 ❌
- **TP 4RR**: 22862.63 ❌
- **TP 15RR**: 22508.33 ❌
- **PnL**: -32.21 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 36.61 points

### Trade #1160 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 08:00:00
- **FVG 5m**: 23000.81 - 23012.17
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23023.68
- **Risk**: 32.21 points
- **TP 1RR**: 22959.26 ❌
- **TP 2RR**: 22927.05 ❌
- **TP 3RR**: 22894.84 ❌
- **TP 4RR**: 22862.63 ❌
- **TP 15RR**: 22508.33 ❌
- **PnL**: -32.21 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 36.61 points

### Trade #1161 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 08:30:00
- **FVG 5m**: 22971.27 - 22989.96
- **Entrée**: 22991.22 @ 2025-06-27 08:56:00
- **Stop Loss**: 22959.79
- **Risk**: 31.43 points
- **TP 1RR**: 23022.65 ✅
- **TP 2RR**: 23054.08 ❌
- **TP 3RR**: 23085.51 ❌
- **TP 4RR**: 23116.94 ❌
- **TP 15RR**: 23462.69 ❌
- **PnL**: -31.43 points (-1.0R)
- **MFE**: 60.34 points
- **MAE**: 39.13 points

### Trade #1162 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 08:30:00
- **FVG 5m**: 22971.27 - 22989.96
- **Entrée**: 22991.22 @ 2025-06-27 08:56:00
- **Stop Loss**: 22959.79
- **Risk**: 31.43 points
- **TP 1RR**: 23022.65 ✅
- **TP 2RR**: 23054.08 ❌
- **TP 3RR**: 23085.51 ❌
- **TP 4RR**: 23116.94 ❌
- **TP 15RR**: 23462.69 ❌
- **PnL**: -31.43 points (-1.0R)
- **MFE**: 60.34 points
- **MAE**: 39.13 points

### Trade #1163 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 09:15:00
- **FVG 5m**: 23000.81 - 23012.17
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23023.68
- **Risk**: 32.21 points
- **TP 1RR**: 22959.26 ❌
- **TP 2RR**: 22927.05 ❌
- **TP 3RR**: 22894.84 ❌
- **TP 4RR**: 22862.63 ❌
- **TP 15RR**: 22508.33 ❌
- **PnL**: -32.21 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 36.61 points

### Trade #1164 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 09:15:00
- **FVG 5m**: 23000.81 - 23012.17
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23023.68
- **Risk**: 32.21 points
- **TP 1RR**: 22959.26 ❌
- **TP 2RR**: 22927.05 ❌
- **TP 3RR**: 22894.84 ❌
- **TP 4RR**: 22862.63 ❌
- **TP 15RR**: 22508.33 ❌
- **PnL**: -32.21 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 36.61 points

### Trade #1165 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 09:15:00
- **FVG 5m**: 23000.81 - 23012.17
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23023.68
- **Risk**: 32.21 points
- **TP 1RR**: 22959.26 ❌
- **TP 2RR**: 22927.05 ❌
- **TP 3RR**: 22894.84 ❌
- **TP 4RR**: 22862.63 ❌
- **TP 15RR**: 22508.33 ❌
- **PnL**: -32.21 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 36.61 points

### Trade #1166 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 13:30:00
- **FVG 5m**: 22842.26 - 22857.91
- **Entrée**: 22826.10 @ 2025-06-27 13:52:00
- **Stop Loss**: 22869.34
- **Risk**: 43.24 points
- **TP 1RR**: 22782.86 ❌
- **TP 2RR**: 22739.62 ❌
- **TP 3RR**: 22696.38 ❌
- **TP 4RR**: 22653.14 ❌
- **TP 15RR**: 22177.49 ❌
- **PnL**: -43.24 points (-1.0R)
- **MFE**: 2.27 points
- **MAE**: 45.95 points

### Trade #1167 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:00:00
- **FVG 5m**: 22916.99 - 22923.30
- **Entrée**: 22931.89 @ 2025-06-27 14:40:00
- **Stop Loss**: 22905.53
- **Risk**: 26.35 points
- **TP 1RR**: 22958.24 ✅
- **TP 2RR**: 22984.60 ✅
- **TP 3RR**: 23010.95 ✅
- **TP 4RR**: 23037.31 ✅
- **TP 15RR**: 23327.21 ❌
- **PnL**: -26.35 points (-1.0R)
- **MFE**: 230.01 points
- **MAE**: 32.82 points

### Trade #1168 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:00:00
- **FVG 5m**: 22916.99 - 22923.30
- **Entrée**: 22931.89 @ 2025-06-27 14:40:00
- **Stop Loss**: 22905.53
- **Risk**: 26.35 points
- **TP 1RR**: 22958.24 ✅
- **TP 2RR**: 22984.60 ✅
- **TP 3RR**: 23010.95 ✅
- **TP 4RR**: 23037.31 ✅
- **TP 15RR**: 23327.21 ❌
- **PnL**: -26.35 points (-1.0R)
- **MFE**: 230.01 points
- **MAE**: 32.82 points

### Trade #1169 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:30:00
- **FVG 5m**: 22945.52 - 22959.91
- **Entrée**: 22962.18 @ 2025-06-27 14:54:00
- **Stop Loss**: 22934.05
- **Risk**: 28.14 points
- **TP 1RR**: 22990.32 ✅
- **TP 2RR**: 23018.46 ✅
- **TP 3RR**: 23046.59 ✅
- **TP 4RR**: 23074.73 ✅
- **TP 15RR**: 23384.23 ❌
- **PnL**: -28.14 points (-1.0R)
- **MFE**: 199.71 points
- **MAE**: 29.54 points

### Trade #1170 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:30:00
- **FVG 5m**: 22945.52 - 22959.91
- **Entrée**: 22962.18 @ 2025-06-27 14:54:00
- **Stop Loss**: 22934.05
- **Risk**: 28.14 points
- **TP 1RR**: 22990.32 ✅
- **TP 2RR**: 23018.46 ✅
- **TP 3RR**: 23046.59 ✅
- **TP 4RR**: 23074.73 ✅
- **TP 15RR**: 23384.23 ❌
- **PnL**: -28.14 points (-1.0R)
- **MFE**: 199.71 points
- **MAE**: 29.54 points

### Trade #1171 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-29 17:45:00
- **FVG 5m**: 23046.01 - 23053.83
- **Entrée**: 23042.22 @ 2025-06-29 18:37:00
- **Stop Loss**: 23065.36
- **Risk**: 23.14 points
- **TP 1RR**: 23019.08 ❌
- **TP 2RR**: 22995.94 ❌
- **TP 3RR**: 22972.80 ❌
- **TP 4RR**: 22949.66 ❌
- **TP 15RR**: 22695.11 ❌
- **PnL**: -23.14 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 24.49 points

### Trade #1172 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-29 17:45:00
- **FVG 5m**: 23046.01 - 23053.83
- **Entrée**: 23042.22 @ 2025-06-29 18:37:00
- **Stop Loss**: 23065.36
- **Risk**: 23.14 points
- **TP 1RR**: 23019.08 ❌
- **TP 2RR**: 22995.94 ❌
- **TP 3RR**: 22972.80 ❌
- **TP 4RR**: 22949.66 ❌
- **TP 15RR**: 22695.11 ❌
- **PnL**: -23.14 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 24.49 points

### Trade #1173 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 01:30:00
- **FVG 5m**: 23094.73 - 23101.55
- **Entrée**: 23094.23 @ 2025-06-30 02:02:00
- **Stop Loss**: 23113.10
- **Risk**: 18.87 points
- **TP 1RR**: 23075.36 ❌
- **TP 2RR**: 23056.48 ❌
- **TP 3RR**: 23037.61 ❌
- **TP 4RR**: 23018.74 ❌
- **TP 15RR**: 22811.14 ❌
- **PnL**: -18.87 points (-1.0R)
- **MFE**: 18.68 points
- **MAE**: 20.70 points

### Trade #1174 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 08:30:00
- **FVG 5m**: 23041.97 - 23054.84
- **Entrée**: 23037.67 @ 2025-06-30 10:13:00
- **Stop Loss**: 23066.37
- **Risk**: 28.70 points
- **TP 1RR**: 23008.98 ❌
- **TP 2RR**: 22980.28 ❌
- **TP 3RR**: 22951.59 ❌
- **TP 4RR**: 22922.89 ❌
- **TP 15RR**: 22607.24 ❌
- **PnL**: -28.70 points (-1.0R)
- **MFE**: 10.35 points
- **MAE**: 28.78 points

### Trade #1175 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 08:45:00
- **FVG 5m**: 23078.07 - 23084.13
- **Entrée**: 23087.92 @ 2025-06-30 11:04:00
- **Stop Loss**: 23066.53
- **Risk**: 21.39 points
- **TP 1RR**: 23109.30 ❌
- **TP 2RR**: 23130.69 ❌
- **TP 3RR**: 23152.07 ❌
- **TP 4RR**: 23173.46 ❌
- **TP 15RR**: 23408.70 ❌
- **PnL**: -21.39 points (-1.0R)
- **MFE**: 6.06 points
- **MAE**: 29.79 points

### Trade #1176 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 11:30:00
- **FVG 5m**: 23049.54 - 23052.32
- **Entrée**: 23053.58 @ 2025-06-30 13:16:00
- **Stop Loss**: 23038.02
- **Risk**: 15.56 points
- **TP 1RR**: 23069.14 ❌
- **TP 2RR**: 23084.71 ❌
- **TP 3RR**: 23100.27 ❌
- **TP 4RR**: 23115.84 ❌
- **TP 15RR**: 23287.05 ❌
- **PnL**: -15.56 points (-1.0R)
- **MFE**: 13.89 points
- **MAE**: 21.21 points

### Trade #1177 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 12:45:00
- **FVG 5m**: 23049.54 - 23052.32
- **Entrée**: 23053.58 @ 2025-06-30 13:16:00
- **Stop Loss**: 23038.02
- **Risk**: 15.56 points
- **TP 1RR**: 23069.14 ❌
- **TP 2RR**: 23084.71 ❌
- **TP 3RR**: 23100.27 ❌
- **TP 4RR**: 23115.84 ❌
- **TP 15RR**: 23287.05 ❌
- **PnL**: -15.56 points (-1.0R)
- **MFE**: 13.89 points
- **MAE**: 21.21 points

### Trade #1178 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 13:30:00
- **FVG 5m**: 23045.50 - 23050.30
- **Entrée**: 23050.55 @ 2025-06-30 13:54:00
- **Stop Loss**: 23033.98
- **Risk**: 16.57 points
- **TP 1RR**: 23067.12 ✅
- **TP 2RR**: 23083.70 ✅
- **TP 3RR**: 23100.27 ✅
- **TP 4RR**: 23116.84 ✅
- **TP 15RR**: 23299.13 ❌
- **PnL**: -16.57 points (-1.0R)
- **MFE**: 111.34 points
- **MAE**: 17.42 points

### Trade #1179 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 14:00:00
- **FVG 5m**: 23092.97 - 23101.30
- **Entrée**: 23103.82 @ 2025-06-30 14:21:00
- **Stop Loss**: 23081.42
- **Risk**: 22.40 points
- **TP 1RR**: 23126.23 ✅
- **TP 2RR**: 23148.63 ✅
- **TP 3RR**: 23171.03 ❌
- **TP 4RR**: 23193.43 ❌
- **TP 15RR**: 23439.87 ❌
- **PnL**: -22.40 points (-1.0R)
- **MFE**: 58.07 points
- **MAE**: 24.74 points

### Trade #1180 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 14:45:00
- **FVG 5m**: 23089.43 - 23091.96
- **Entrée**: 23088.67 @ 2025-06-30 17:54:00
- **Stop Loss**: 23103.50
- **Risk**: 14.83 points
- **TP 1RR**: 23073.85 ✅
- **TP 2RR**: 23059.02 ❌
- **TP 3RR**: 23044.19 ❌
- **TP 4RR**: 23029.36 ❌
- **TP 15RR**: 22866.25 ❌
- **PnL**: -14.83 points (-1.0R)
- **MFE**: 16.16 points
- **MAE**: 15.15 points

### Trade #1181 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 14:45:00
- **FVG 5m**: 23089.43 - 23091.96
- **Entrée**: 23088.67 @ 2025-06-30 17:54:00
- **Stop Loss**: 23103.50
- **Risk**: 14.83 points
- **TP 1RR**: 23073.85 ✅
- **TP 2RR**: 23059.02 ❌
- **TP 3RR**: 23044.19 ❌
- **TP 4RR**: 23029.36 ❌
- **TP 15RR**: 22866.25 ❌
- **PnL**: -14.83 points (-1.0R)
- **MFE**: 16.16 points
- **MAE**: 15.15 points

### Trade #1182 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 15:00:00
- **FVG 5m**: 23089.43 - 23091.96
- **Entrée**: 23088.67 @ 2025-06-30 17:54:00
- **Stop Loss**: 23103.50
- **Risk**: 14.83 points
- **TP 1RR**: 23073.85 ✅
- **TP 2RR**: 23059.02 ❌
- **TP 3RR**: 23044.19 ❌
- **TP 4RR**: 23029.36 ❌
- **TP 15RR**: 22866.25 ❌
- **PnL**: -14.83 points (-1.0R)
- **MFE**: 16.16 points
- **MAE**: 15.15 points

### Trade #1183 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 03:15:00
- **FVG 5m**: 23047.02 - 23056.36
- **Entrée**: 23056.86 @ 2025-07-01 04:59:00
- **Stop Loss**: 23035.49
- **Risk**: 21.37 points
- **TP 1RR**: 23078.23 ❌
- **TP 2RR**: 23099.60 ❌
- **TP 3RR**: 23120.97 ❌
- **TP 4RR**: 23142.34 ❌
- **TP 15RR**: 23377.41 ❌
- **PnL**: -21.37 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 22.22 points

### Trade #1184 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 04:45:00
- **FVG 5m**: 23047.02 - 23056.36
- **Entrée**: 23056.86 @ 2025-07-01 04:59:00
- **Stop Loss**: 23035.49
- **Risk**: 21.37 points
- **TP 1RR**: 23078.23 ❌
- **TP 2RR**: 23099.60 ❌
- **TP 3RR**: 23120.97 ❌
- **TP 4RR**: 23142.34 ❌
- **TP 15RR**: 23377.41 ❌
- **PnL**: -21.37 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 22.22 points

### Trade #1185 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 08:00:00
- **FVG 5m**: 22867.00 - 22890.99
- **Entrée**: 22892.25 @ 2025-07-01 10:24:00
- **Stop Loss**: 22855.57
- **Risk**: 36.68 points
- **TP 1RR**: 22928.93 ❌
- **TP 2RR**: 22965.61 ❌
- **TP 3RR**: 23002.29 ❌
- **TP 4RR**: 23038.97 ❌
- **TP 15RR**: 23442.46 ❌
- **PnL**: -36.68 points (-1.0R)
- **MFE**: 27.52 points
- **MAE**: 45.45 points

### Trade #1186 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 09:00:00
- **FVG 5m**: 22867.00 - 22890.99
- **Entrée**: 22892.25 @ 2025-07-01 10:24:00
- **Stop Loss**: 22855.57
- **Risk**: 36.68 points
- **TP 1RR**: 22928.93 ❌
- **TP 2RR**: 22965.61 ❌
- **TP 3RR**: 23002.29 ❌
- **TP 4RR**: 23038.97 ❌
- **TP 15RR**: 23442.46 ❌
- **PnL**: -36.68 points (-1.0R)
- **MFE**: 27.52 points
- **MAE**: 45.45 points

### Trade #1187 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 02:00:00
- **FVG 5m**: 22978.85 - 22984.65
- **Entrée**: 22976.58 @ 2025-07-02 02:18:00
- **Stop Loss**: 22996.15
- **Risk**: 19.57 points
- **TP 1RR**: 22957.00 ✅
- **TP 2RR**: 22937.43 ✅
- **TP 3RR**: 22917.86 ✅
- **TP 4RR**: 22898.29 ✅
- **TP 15RR**: 22683.00 ❌
- **PnL**: -19.57 points (-1.0R)
- **MFE**: 170.93 points
- **MAE**: 36.36 points

### Trade #1188 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 02:30:00
- **FVG 5m**: 22956.88 - 22962.18
- **Entrée**: 22955.87 @ 2025-07-02 02:43:00
- **Stop Loss**: 22973.67
- **Risk**: 17.79 points
- **TP 1RR**: 22938.08 ✅
- **TP 2RR**: 22920.29 ✅
- **TP 3RR**: 22902.49 ✅
- **TP 4RR**: 22884.70 ✅
- **TP 15RR**: 22688.98 ❌
- **PnL**: -17.79 points (-1.0R)
- **MFE**: 150.22 points
- **MAE**: 21.71 points

### Trade #1189 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 07:00:00
- **FVG 5m**: 22841.00 - 22864.48
- **Entrée**: 22878.11 @ 2025-07-02 08:04:00
- **Stop Loss**: 22829.58
- **Risk**: 48.53 points
- **TP 1RR**: 22926.64 ✅
- **TP 2RR**: 22975.18 ✅
- **TP 3RR**: 23023.71 ✅
- **TP 4RR**: 23072.25 ✅
- **TP 15RR**: 23606.13 ✅
- **PnL**: 728.02 points (15.0R)
- **MFE**: 735.97 points
- **MAE**: 20.20 points

### Trade #1190 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 07:30:00
- **FVG 5m**: 22841.00 - 22864.48
- **Entrée**: 22878.11 @ 2025-07-02 08:04:00
- **Stop Loss**: 22829.58
- **Risk**: 48.53 points
- **TP 1RR**: 22926.64 ✅
- **TP 2RR**: 22975.18 ✅
- **TP 3RR**: 23023.71 ✅
- **TP 4RR**: 23072.25 ✅
- **TP 15RR**: 23606.13 ✅
- **PnL**: 728.02 points (15.0R)
- **MFE**: 735.97 points
- **MAE**: 20.20 points

### Trade #1191 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 08:15:00
- **FVG 5m**: 22872.56 - 22875.58
- **Entrée**: 22878.87 @ 2025-07-02 08:28:00
- **Stop Loss**: 22861.12
- **Risk**: 17.75 points
- **TP 1RR**: 22896.62 ✅
- **TP 2RR**: 22914.36 ✅
- **TP 3RR**: 22932.11 ✅
- **TP 4RR**: 22949.86 ✅
- **TP 15RR**: 23145.09 ✅
- **PnL**: 266.22 points (15.0R)
- **MFE**: 267.12 points
- **MAE**: 4.04 points

### Trade #1192 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 09:15:00
- **FVG 5m**: 22994.25 - 23015.20
- **Entrée**: 23015.71 @ 2025-07-02 09:28:00
- **Stop Loss**: 22982.75
- **Risk**: 32.96 points
- **TP 1RR**: 23048.67 ✅
- **TP 2RR**: 23081.62 ✅
- **TP 3RR**: 23114.58 ✅
- **TP 4RR**: 23147.54 ✅
- **TP 15RR**: 23510.07 ✅
- **PnL**: 494.36 points (15.0R)
- **MFE**: 494.60 points
- **MAE**: 19.19 points

### Trade #1193 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 21:30:00
- **FVG 5m**: 23069.23 - 23071.76
- **Entrée**: 23072.26 @ 2025-07-02 21:47:00
- **Stop Loss**: 23057.70
- **Risk**: 14.56 points
- **TP 1RR**: 23086.83 ✅
- **TP 2RR**: 23101.39 ✅
- **TP 3RR**: 23115.96 ✅
- **TP 4RR**: 23130.52 ❌
- **TP 15RR**: 23290.73 ❌
- **PnL**: -14.56 points (-1.0R)
- **MFE**: 55.54 points
- **MAE**: 16.16 points

### Trade #1194 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 22:45:00
- **FVG 5m**: 23094.48 - 23097.01
- **Entrée**: 23094.23 @ 2025-07-02 23:32:00
- **Stop Loss**: 23108.55
- **Risk**: 14.33 points
- **TP 1RR**: 23079.90 ✅
- **TP 2RR**: 23065.58 ❌
- **TP 3RR**: 23051.25 ❌
- **TP 4RR**: 23036.93 ❌
- **TP 15RR**: 22879.34 ❌
- **PnL**: -14.33 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 22.47 points

### Trade #1195 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 22:45:00
- **FVG 5m**: 23094.48 - 23097.01
- **Entrée**: 23094.23 @ 2025-07-02 23:32:00
- **Stop Loss**: 23108.55
- **Risk**: 14.33 points
- **TP 1RR**: 23079.90 ✅
- **TP 2RR**: 23065.58 ❌
- **TP 3RR**: 23051.25 ❌
- **TP 4RR**: 23036.93 ❌
- **TP 15RR**: 22879.34 ❌
- **PnL**: -14.33 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 22.47 points

### Trade #1196 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-03 02:45:00
- **FVG 5m**: 23081.86 - 23085.90
- **Entrée**: 23079.84 @ 2025-07-03 04:57:00
- **Stop Loss**: 23097.44
- **Risk**: 17.60 points
- **TP 1RR**: 23062.24 ✅
- **TP 2RR**: 23044.63 ❌
- **TP 3RR**: 23027.03 ❌
- **TP 4RR**: 23009.43 ❌
- **TP 15RR**: 22815.80 ❌
- **PnL**: -17.60 points (-1.0R)
- **MFE**: 23.73 points
- **MAE**: 20.96 points

### Trade #1197 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-03 03:45:00
- **FVG 5m**: 23081.86 - 23085.90
- **Entrée**: 23079.84 @ 2025-07-03 04:57:00
- **Stop Loss**: 23097.44
- **Risk**: 17.60 points
- **TP 1RR**: 23062.24 ✅
- **TP 2RR**: 23044.63 ❌
- **TP 3RR**: 23027.03 ❌
- **TP 4RR**: 23009.43 ❌
- **TP 15RR**: 22815.80 ❌
- **PnL**: -17.60 points (-1.0R)
- **MFE**: 23.73 points
- **MAE**: 20.96 points

### Trade #1198 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-04 03:45:00
- **FVG 5m**: 23156.09 - 23160.88
- **Entrée**: 23152.80 @ 2025-07-04 05:44:00
- **Stop Loss**: 23172.46
- **Risk**: 19.66 points
- **TP 1RR**: 23133.14 ✅
- **TP 2RR**: 23113.48 ✅
- **TP 3RR**: 23093.82 ❌
- **TP 4RR**: 23074.16 ❌
- **TP 15RR**: 22857.91 ❌
- **PnL**: -19.66 points (-1.0R)
- **MFE**: 44.18 points
- **MAE**: 19.95 points

### Trade #1199 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-04 06:00:00
- **FVG 5m**: 23142.45 - 23147.75
- **Entrée**: 23148.76 @ 2025-07-04 06:14:00
- **Stop Loss**: 23130.88
- **Risk**: 17.88 points
- **TP 1RR**: 23166.65 ✅
- **TP 2RR**: 23184.53 ❌
- **TP 3RR**: 23202.41 ❌
- **TP 4RR**: 23220.30 ❌
- **TP 15RR**: 23417.01 ❌
- **PnL**: -17.88 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 26.01 points

### Trade #1200 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-06 17:00:00
- **FVG 5m**: 23203.80 - 23212.89
- **Entrée**: 23213.65 @ 2025-07-06 18:15:00
- **Stop Loss**: 23192.20
- **Risk**: 21.45 points
- **TP 1RR**: 23235.10 ❌
- **TP 2RR**: 23256.55 ❌
- **TP 3RR**: 23278.00 ❌
- **TP 4RR**: 23299.44 ❌
- **TP 15RR**: 23535.38 ❌
- **PnL**: -21.45 points (-1.0R)
- **MFE**: 19.95 points
- **MAE**: 22.22 points

### Trade #1201 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-06 20:00:00
- **FVG 5m**: 23180.32 - 23185.63
- **Entrée**: 23178.56 @ 2025-07-06 21:31:00
- **Stop Loss**: 23197.22
- **Risk**: 18.66 points
- **TP 1RR**: 23159.89 ❌
- **TP 2RR**: 23141.23 ❌
- **TP 3RR**: 23122.57 ❌
- **TP 4RR**: 23103.91 ❌
- **TP 15RR**: 22898.62 ❌
- **PnL**: -18.66 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 19.19 points

### Trade #1202 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-07 07:15:00
- **FVG 5m**: 23182.60 - 23189.92
- **Entrée**: 23180.32 @ 2025-07-07 07:54:00
- **Stop Loss**: 23201.51
- **Risk**: 21.19 points
- **TP 1RR**: 23159.13 ✅
- **TP 2RR**: 23137.95 ❌
- **TP 3RR**: 23116.76 ❌
- **TP 4RR**: 23095.57 ❌
- **TP 15RR**: 22862.49 ❌
- **PnL**: -21.19 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 22.98 points

### Trade #1203 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-07 07:15:00
- **FVG 5m**: 23182.60 - 23189.92
- **Entrée**: 23180.32 @ 2025-07-07 07:54:00
- **Stop Loss**: 23201.51
- **Risk**: 21.19 points
- **TP 1RR**: 23159.13 ✅
- **TP 2RR**: 23137.95 ❌
- **TP 3RR**: 23116.76 ❌
- **TP 4RR**: 23095.57 ❌
- **TP 15RR**: 22862.49 ❌
- **PnL**: -21.19 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 22.98 points

### Trade #1204 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 08:30:00
- **FVG 5m**: 23144.72 - 23155.33
- **Entrée**: 23160.63 @ 2025-07-07 10:57:00
- **Stop Loss**: 23133.15
- **Risk**: 27.48 points
- **TP 1RR**: 23188.11 ✅
- **TP 2RR**: 23215.59 ❌
- **TP 3RR**: 23243.07 ❌
- **TP 4RR**: 23270.54 ❌
- **TP 15RR**: 23572.81 ❌
- **PnL**: -27.48 points (-1.0R)
- **MFE**: 29.29 points
- **MAE**: 33.58 points

### Trade #1205 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 08:30:00
- **FVG 5m**: 23144.72 - 23155.33
- **Entrée**: 23160.63 @ 2025-07-07 10:57:00
- **Stop Loss**: 23133.15
- **Risk**: 27.48 points
- **TP 1RR**: 23188.11 ✅
- **TP 2RR**: 23215.59 ❌
- **TP 3RR**: 23243.07 ❌
- **TP 4RR**: 23270.54 ❌
- **TP 15RR**: 23572.81 ❌
- **PnL**: -27.48 points (-1.0R)
- **MFE**: 29.29 points
- **MAE**: 33.58 points

### Trade #1206 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 11:15:00
- **FVG 5m**: 23033.13 - 23046.26
- **Entrée**: 23050.05 @ 2025-07-07 13:37:00
- **Stop Loss**: 23021.61
- **Risk**: 28.43 points
- **TP 1RR**: 23078.48 ✅
- **TP 2RR**: 23106.91 ✅
- **TP 3RR**: 23135.34 ✅
- **TP 4RR**: 23163.78 ✅
- **TP 15RR**: 23476.53 ✅
- **PnL**: 426.49 points (15.0R)
- **MFE**: 427.44 points
- **MAE**: 21.21 points

### Trade #1207 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 11:15:00
- **FVG 5m**: 23033.13 - 23046.26
- **Entrée**: 23050.05 @ 2025-07-07 13:37:00
- **Stop Loss**: 23021.61
- **Risk**: 28.43 points
- **TP 1RR**: 23078.48 ✅
- **TP 2RR**: 23106.91 ✅
- **TP 3RR**: 23135.34 ✅
- **TP 4RR**: 23163.78 ✅
- **TP 15RR**: 23476.53 ✅
- **PnL**: 426.49 points (15.0R)
- **MFE**: 427.44 points
- **MAE**: 21.21 points

### Trade #1208 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 11:15:00
- **FVG 5m**: 23033.13 - 23046.26
- **Entrée**: 23050.05 @ 2025-07-07 13:37:00
- **Stop Loss**: 23021.61
- **Risk**: 28.43 points
- **TP 1RR**: 23078.48 ✅
- **TP 2RR**: 23106.91 ✅
- **TP 3RR**: 23135.34 ✅
- **TP 4RR**: 23163.78 ✅
- **TP 15RR**: 23476.53 ✅
- **PnL**: 426.49 points (15.0R)
- **MFE**: 427.44 points
- **MAE**: 21.21 points

### Trade #1209 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 11:15:00
- **FVG 5m**: 23033.13 - 23046.26
- **Entrée**: 23050.05 @ 2025-07-07 13:37:00
- **Stop Loss**: 23021.61
- **Risk**: 28.43 points
- **TP 1RR**: 23078.48 ✅
- **TP 2RR**: 23106.91 ✅
- **TP 3RR**: 23135.34 ✅
- **TP 4RR**: 23163.78 ✅
- **TP 15RR**: 23476.53 ✅
- **PnL**: 426.49 points (15.0R)
- **MFE**: 427.44 points
- **MAE**: 21.21 points

### Trade #1210 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-07 11:45:00
- **FVG 5m**: 23056.11 - 23091.45
- **Entrée**: 23050.30 @ 2025-07-07 13:19:00
- **Stop Loss**: 23103.00
- **Risk**: 52.70 points
- **TP 1RR**: 22997.60 ❌
- **TP 2RR**: 22944.90 ❌
- **TP 3RR**: 22892.20 ❌
- **TP 4RR**: 22839.50 ❌
- **TP 15RR**: 22259.81 ❌
- **PnL**: -52.70 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 54.79 points

### Trade #1211 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23052.07 - 23069.23
- **Entrée**: 23073.27 @ 2025-07-07 13:42:00
- **Stop Loss**: 23040.54
- **Risk**: 32.73 points
- **TP 1RR**: 23106.01 ✅
- **TP 2RR**: 23138.74 ❌
- **TP 3RR**: 23171.48 ❌
- **TP 4RR**: 23204.21 ❌
- **TP 15RR**: 23564.28 ❌
- **PnL**: -32.73 points (-1.0R)
- **MFE**: 44.69 points
- **MAE**: 35.60 points

### Trade #1212 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23052.07 - 23069.23
- **Entrée**: 23073.27 @ 2025-07-07 13:42:00
- **Stop Loss**: 23040.54
- **Risk**: 32.73 points
- **TP 1RR**: 23106.01 ✅
- **TP 2RR**: 23138.74 ❌
- **TP 3RR**: 23171.48 ❌
- **TP 4RR**: 23204.21 ❌
- **TP 15RR**: 23564.28 ❌
- **PnL**: -32.73 points (-1.0R)
- **MFE**: 44.69 points
- **MAE**: 35.60 points

### Trade #1213 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23052.07 - 23069.23
- **Entrée**: 23073.27 @ 2025-07-07 13:42:00
- **Stop Loss**: 23040.54
- **Risk**: 32.73 points
- **TP 1RR**: 23106.01 ✅
- **TP 2RR**: 23138.74 ❌
- **TP 3RR**: 23171.48 ❌
- **TP 4RR**: 23204.21 ❌
- **TP 15RR**: 23564.28 ❌
- **PnL**: -32.73 points (-1.0R)
- **MFE**: 44.69 points
- **MAE**: 35.60 points

### Trade #1214 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23052.07 - 23069.23
- **Entrée**: 23073.27 @ 2025-07-07 13:42:00
- **Stop Loss**: 23040.54
- **Risk**: 32.73 points
- **TP 1RR**: 23106.01 ✅
- **TP 2RR**: 23138.74 ❌
- **TP 3RR**: 23171.48 ❌
- **TP 4RR**: 23204.21 ❌
- **TP 15RR**: 23564.28 ❌
- **PnL**: -32.73 points (-1.0R)
- **MFE**: 44.69 points
- **MAE**: 35.60 points

### Trade #1215 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 19:30:00
- **FVG 5m**: 23114.17 - 23117.96
- **Entrée**: 23121.50 @ 2025-07-07 19:41:00
- **Stop Loss**: 23102.62
- **Risk**: 18.88 points
- **TP 1RR**: 23140.38 ✅
- **TP 2RR**: 23159.25 ✅
- **TP 3RR**: 23178.13 ✅
- **TP 4RR**: 23197.01 ✅
- **TP 15RR**: 23404.68 ❌
- **PnL**: -18.88 points (-1.0R)
- **MFE**: 78.77 points
- **MAE**: 22.72 points

### Trade #1216 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 21:15:00
- **FVG 5m**: 23136.14 - 23141.44
- **Entrée**: 23141.69 @ 2025-07-07 21:26:00
- **Stop Loss**: 23124.57
- **Risk**: 17.12 points
- **TP 1RR**: 23158.82 ✅
- **TP 2RR**: 23175.94 ✅
- **TP 3RR**: 23193.06 ✅
- **TP 4RR**: 23210.18 ❌
- **TP 15RR**: 23398.53 ❌
- **PnL**: -17.12 points (-1.0R)
- **MFE**: 58.57 points
- **MAE**: 20.45 points

### Trade #1217 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 06:30:00
- **FVG 5m**: 23167.45 - 23173.51
- **Entrée**: 23175.78 @ 2025-07-08 07:13:00
- **Stop Loss**: 23155.86
- **Risk**: 19.92 points
- **TP 1RR**: 23195.69 ❌
- **TP 2RR**: 23215.61 ❌
- **TP 3RR**: 23235.53 ❌
- **TP 4RR**: 23255.44 ❌
- **TP 15RR**: 23474.51 ❌
- **PnL**: -19.92 points (-1.0R)
- **MFE**: 6.82 points
- **MAE**: 21.97 points

### Trade #1218 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-08 08:15:00
- **FVG 5m**: 23143.71 - 23158.11
- **Entrée**: 23142.20 @ 2025-07-08 08:32:00
- **Stop Loss**: 23169.68
- **Risk**: 27.49 points
- **TP 1RR**: 23114.71 ✅
- **TP 2RR**: 23087.23 ✅
- **TP 3RR**: 23059.74 ❌
- **TP 4RR**: 23032.26 ❌
- **TP 15RR**: 22729.92 ❌
- **PnL**: -27.49 points (-1.0R)
- **MFE**: 66.91 points
- **MAE**: 27.77 points

### Trade #1219 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 08:30:00
- **FVG 5m**: 23103.32 - 23143.97
- **Entrée**: 23149.52 @ 2025-07-08 09:34:00
- **Stop Loss**: 23091.77
- **Risk**: 57.75 points
- **TP 1RR**: 23207.28 ❌
- **TP 2RR**: 23265.03 ❌
- **TP 3RR**: 23322.79 ❌
- **TP 4RR**: 23380.54 ❌
- **TP 15RR**: 24015.84 ❌
- **PnL**: -57.75 points (-1.0R)
- **MFE**: 20.45 points
- **MAE**: 68.93 points

### Trade #1220 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-08 08:45:00
- **FVG 5m**: 23138.66 - 23142.96
- **Entrée**: 23137.15 @ 2025-07-08 09:48:00
- **Stop Loss**: 23154.53
- **Risk**: 17.38 points
- **TP 1RR**: 23119.77 ✅
- **TP 2RR**: 23102.39 ✅
- **TP 3RR**: 23085.01 ✅
- **TP 4RR**: 23067.64 ✅
- **TP 15RR**: 22876.47 ❌
- **PnL**: -17.38 points (-1.0R)
- **MFE**: 69.94 points
- **MAE**: 17.67 points

### Trade #1221 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 09:30:00
- **FVG 5m**: 23151.54 - 23172.75
- **Entrée**: 23174.26 @ 2025-07-08 11:24:00
- **Stop Loss**: 23139.97
- **Risk**: 34.30 points
- **TP 1RR**: 23208.56 ❌
- **TP 2RR**: 23242.86 ❌
- **TP 3RR**: 23277.16 ❌
- **TP 4RR**: 23311.46 ❌
- **TP 15RR**: 23688.74 ❌
- **PnL**: -34.30 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 59.58 points

### Trade #1222 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 09:30:00
- **FVG 5m**: 23151.54 - 23172.75
- **Entrée**: 23174.26 @ 2025-07-08 11:24:00
- **Stop Loss**: 23139.97
- **Risk**: 34.30 points
- **TP 1RR**: 23208.56 ❌
- **TP 2RR**: 23242.86 ❌
- **TP 3RR**: 23277.16 ❌
- **TP 4RR**: 23311.46 ❌
- **TP 15RR**: 23688.74 ❌
- **PnL**: -34.30 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 59.58 points

### Trade #1223 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 09:30:00
- **FVG 5m**: 23151.54 - 23172.75
- **Entrée**: 23174.26 @ 2025-07-08 11:24:00
- **Stop Loss**: 23139.97
- **Risk**: 34.30 points
- **TP 1RR**: 23208.56 ❌
- **TP 2RR**: 23242.86 ❌
- **TP 3RR**: 23277.16 ❌
- **TP 4RR**: 23311.46 ❌
- **TP 15RR**: 23688.74 ❌
- **PnL**: -34.30 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 59.58 points

### Trade #1224 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 19:30:00
- **FVG 5m**: 23112.15 - 23116.70
- **Entrée**: 23116.95 @ 2025-07-08 20:59:00
- **Stop Loss**: 23100.60
- **Risk**: 16.35 points
- **TP 1RR**: 23133.30 ❌
- **TP 2RR**: 23149.66 ❌
- **TP 3RR**: 23166.01 ❌
- **TP 4RR**: 23182.36 ❌
- **TP 15RR**: 23362.25 ❌
- **PnL**: -16.35 points (-1.0R)
- **MFE**: 11.36 points
- **MAE**: 18.18 points

### Trade #1225 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 20:30:00
- **FVG 5m**: 23112.15 - 23116.70
- **Entrée**: 23116.95 @ 2025-07-08 20:59:00
- **Stop Loss**: 23100.60
- **Risk**: 16.35 points
- **TP 1RR**: 23133.30 ❌
- **TP 2RR**: 23149.66 ❌
- **TP 3RR**: 23166.01 ❌
- **TP 4RR**: 23182.36 ❌
- **TP 15RR**: 23362.25 ❌
- **PnL**: -16.35 points (-1.0R)
- **MFE**: 11.36 points
- **MAE**: 18.18 points

### Trade #1226 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 04:45:00
- **FVG 5m**: 23146.24 - 23149.52
- **Entrée**: 23145.99 @ 2025-07-09 05:01:00
- **Stop Loss**: 23161.10
- **Risk**: 15.11 points
- **TP 1RR**: 23130.88 ❌
- **TP 2RR**: 23115.77 ❌
- **TP 3RR**: 23100.66 ❌
- **TP 4RR**: 23085.55 ❌
- **TP 15RR**: 22919.35 ❌
- **PnL**: -15.11 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 15.65 points

### Trade #1227 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 07:45:00
- **FVG 5m**: 23277.53 - 23297.22
- **Entrée**: 23277.02 @ 2025-07-09 09:29:00
- **Stop Loss**: 23308.87
- **Risk**: 31.85 points
- **TP 1RR**: 23245.17 ✅
- **TP 2RR**: 23213.33 ✅
- **TP 3RR**: 23181.48 ✅
- **TP 4RR**: 23149.63 ✅
- **TP 15RR**: 22799.32 ❌
- **PnL**: -31.85 points (-1.0R)
- **MFE**: 130.28 points
- **MAE**: 41.66 points

### Trade #1228 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 07:45:00
- **FVG 5m**: 23277.53 - 23297.22
- **Entrée**: 23277.02 @ 2025-07-09 09:29:00
- **Stop Loss**: 23308.87
- **Risk**: 31.85 points
- **TP 1RR**: 23245.17 ✅
- **TP 2RR**: 23213.33 ✅
- **TP 3RR**: 23181.48 ✅
- **TP 4RR**: 23149.63 ✅
- **TP 15RR**: 22799.32 ❌
- **PnL**: -31.85 points (-1.0R)
- **MFE**: 130.28 points
- **MAE**: 41.66 points

### Trade #1229 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-09 08:30:00
- **FVG 5m**: 23278.79 - 23283.08
- **Entrée**: 23285.35 @ 2025-07-09 08:42:00
- **Stop Loss**: 23267.15
- **Risk**: 18.20 points
- **TP 1RR**: 23303.56 ✅
- **TP 2RR**: 23321.76 ✅
- **TP 3RR**: 23339.96 ✅
- **TP 4RR**: 23358.17 ❌
- **TP 15RR**: 23558.41 ❌
- **PnL**: -18.20 points (-1.0R)
- **MFE**: 55.54 points
- **MAE**: 21.21 points

### Trade #1230 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-09 08:30:00
- **FVG 5m**: 23278.79 - 23283.08
- **Entrée**: 23285.35 @ 2025-07-09 08:42:00
- **Stop Loss**: 23267.15
- **Risk**: 18.20 points
- **TP 1RR**: 23303.56 ✅
- **TP 2RR**: 23321.76 ✅
- **TP 3RR**: 23339.96 ✅
- **TP 4RR**: 23358.17 ❌
- **TP 15RR**: 23558.41 ❌
- **PnL**: -18.20 points (-1.0R)
- **MFE**: 55.54 points
- **MAE**: 21.21 points

### Trade #1231 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:15:00
- **FVG 5m**: 23277.53 - 23297.22
- **Entrée**: 23277.02 @ 2025-07-09 09:29:00
- **Stop Loss**: 23308.87
- **Risk**: 31.85 points
- **TP 1RR**: 23245.17 ✅
- **TP 2RR**: 23213.33 ✅
- **TP 3RR**: 23181.48 ✅
- **TP 4RR**: 23149.63 ✅
- **TP 15RR**: 22799.32 ❌
- **PnL**: -31.85 points (-1.0R)
- **MFE**: 130.28 points
- **MAE**: 41.66 points

### Trade #1232 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:30:00
- **FVG 5m**: 23193.20 - 23201.53
- **Entrée**: 23189.16 @ 2025-07-09 09:48:00
- **Stop Loss**: 23213.13
- **Risk**: 23.97 points
- **TP 1RR**: 23165.19 ✅
- **TP 2RR**: 23141.22 ❌
- **TP 3RR**: 23117.24 ❌
- **TP 4RR**: 23093.27 ❌
- **TP 15RR**: 22829.58 ❌
- **PnL**: -23.97 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 28.53 points

### Trade #1233 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:30:00
- **FVG 5m**: 23193.20 - 23201.53
- **Entrée**: 23189.16 @ 2025-07-09 09:48:00
- **Stop Loss**: 23213.13
- **Risk**: 23.97 points
- **TP 1RR**: 23165.19 ✅
- **TP 2RR**: 23141.22 ❌
- **TP 3RR**: 23117.24 ❌
- **TP 4RR**: 23093.27 ❌
- **TP 15RR**: 22829.58 ❌
- **PnL**: -23.97 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 28.53 points

### Trade #1234 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23188.66 - 23203.80
- **Entrée**: 23186.38 @ 2025-07-09 10:51:00
- **Stop Loss**: 23215.41
- **Risk**: 29.02 points
- **TP 1RR**: 23157.36 ❌
- **TP 2RR**: 23128.34 ❌
- **TP 3RR**: 23099.31 ❌
- **TP 4RR**: 23070.29 ❌
- **TP 15RR**: 22751.04 ❌
- **PnL**: -29.02 points (-1.0R)
- **MFE**: 22.22 points
- **MAE**: 29.54 points

### Trade #1235 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23188.66 - 23203.80
- **Entrée**: 23186.38 @ 2025-07-09 10:51:00
- **Stop Loss**: 23215.41
- **Risk**: 29.02 points
- **TP 1RR**: 23157.36 ❌
- **TP 2RR**: 23128.34 ❌
- **TP 3RR**: 23099.31 ❌
- **TP 4RR**: 23070.29 ❌
- **TP 15RR**: 22751.04 ❌
- **PnL**: -29.02 points (-1.0R)
- **MFE**: 22.22 points
- **MAE**: 29.54 points

### Trade #1236 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23188.66 - 23203.80
- **Entrée**: 23186.38 @ 2025-07-09 10:51:00
- **Stop Loss**: 23215.41
- **Risk**: 29.02 points
- **TP 1RR**: 23157.36 ❌
- **TP 2RR**: 23128.34 ❌
- **TP 3RR**: 23099.31 ❌
- **TP 4RR**: 23070.29 ❌
- **TP 15RR**: 22751.04 ❌
- **PnL**: -29.02 points (-1.0R)
- **MFE**: 22.22 points
- **MAE**: 29.54 points

### Trade #1237 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23188.66 - 23203.80
- **Entrée**: 23186.38 @ 2025-07-09 10:51:00
- **Stop Loss**: 23215.41
- **Risk**: 29.02 points
- **TP 1RR**: 23157.36 ❌
- **TP 2RR**: 23128.34 ❌
- **TP 3RR**: 23099.31 ❌
- **TP 4RR**: 23070.29 ❌
- **TP 15RR**: 22751.04 ❌
- **PnL**: -29.02 points (-1.0R)
- **MFE**: 22.22 points
- **MAE**: 29.54 points

### Trade #1238 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 07:30:00
- **FVG 5m**: 23271.21 - 23291.41
- **Entrée**: 23263.89 @ 2025-07-10 08:33:00
- **Stop Loss**: 23303.06
- **Risk**: 39.17 points
- **TP 1RR**: 23224.73 ✅
- **TP 2RR**: 23185.56 ✅
- **TP 3RR**: 23146.40 ✅
- **TP 4RR**: 23107.23 ✅
- **TP 15RR**: 22676.41 ❌
- **PnL**: -39.17 points (-1.0R)
- **MFE**: 235.06 points
- **MAE**: 43.93 points

### Trade #1239 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 08:30:00
- **FVG 5m**: 23238.39 - 23251.27
- **Entrée**: 23231.32 @ 2025-07-10 08:48:00
- **Stop Loss**: 23262.89
- **Risk**: 31.57 points
- **TP 1RR**: 23199.75 ✅
- **TP 2RR**: 23168.18 ✅
- **TP 3RR**: 23136.61 ✅
- **TP 4RR**: 23105.04 ❌
- **TP 15RR**: 22757.75 ❌
- **PnL**: -31.57 points (-1.0R)
- **MFE**: 103.26 points
- **MAE**: 32.32 points

### Trade #1240 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 08:30:00
- **FVG 5m**: 23238.39 - 23251.27
- **Entrée**: 23231.32 @ 2025-07-10 08:48:00
- **Stop Loss**: 23262.89
- **Risk**: 31.57 points
- **TP 1RR**: 23199.75 ✅
- **TP 2RR**: 23168.18 ✅
- **TP 3RR**: 23136.61 ✅
- **TP 4RR**: 23105.04 ❌
- **TP 15RR**: 22757.75 ❌
- **PnL**: -31.57 points (-1.0R)
- **MFE**: 103.26 points
- **MAE**: 32.32 points

### Trade #1241 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 08:45:00
- **FVG 5m**: 23188.66 - 23195.47
- **Entrée**: 23170.48 @ 2025-07-10 08:58:00
- **Stop Loss**: 23207.07
- **Risk**: 36.59 points
- **TP 1RR**: 23133.88 ✅
- **TP 2RR**: 23097.29 ❌
- **TP 3RR**: 23060.70 ❌
- **TP 4RR**: 23024.11 ❌
- **TP 15RR**: 22621.58 ❌
- **PnL**: -36.59 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 36.86 points

### Trade #1242 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 09:00:00
- **FVG 5m**: 23158.36 - 23166.69
- **Entrée**: 23171.23 @ 2025-07-10 09:11:00
- **Stop Loss**: 23146.78
- **Risk**: 24.46 points
- **TP 1RR**: 23195.69 ❌
- **TP 2RR**: 23220.15 ❌
- **TP 3RR**: 23244.60 ❌
- **TP 4RR**: 23269.06 ❌
- **TP 15RR**: 23538.07 ❌
- **PnL**: -24.46 points (-1.0R)
- **MFE**: 24.24 points
- **MAE**: 31.31 points

### Trade #1243 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 09:00:00
- **FVG 5m**: 23158.36 - 23166.69
- **Entrée**: 23171.23 @ 2025-07-10 09:11:00
- **Stop Loss**: 23146.78
- **Risk**: 24.46 points
- **TP 1RR**: 23195.69 ❌
- **TP 2RR**: 23220.15 ❌
- **TP 3RR**: 23244.60 ❌
- **TP 4RR**: 23269.06 ❌
- **TP 15RR**: 23538.07 ❌
- **PnL**: -24.46 points (-1.0R)
- **MFE**: 24.24 points
- **MAE**: 31.31 points

### Trade #1244 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 10:15:00
- **FVG 5m**: 23207.84 - 23214.16
- **Entrée**: 23218.95 @ 2025-07-10 10:26:00
- **Stop Loss**: 23196.24
- **Risk**: 22.71 points
- **TP 1RR**: 23241.67 ✅
- **TP 2RR**: 23264.38 ❌
- **TP 3RR**: 23287.09 ❌
- **TP 4RR**: 23309.80 ❌
- **TP 15RR**: 23559.65 ❌
- **PnL**: -22.71 points (-1.0R)
- **MFE**: 34.59 points
- **MAE**: 27.52 points

### Trade #1245 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 10:15:00
- **FVG 5m**: 23207.84 - 23214.16
- **Entrée**: 23218.95 @ 2025-07-10 10:26:00
- **Stop Loss**: 23196.24
- **Risk**: 22.71 points
- **TP 1RR**: 23241.67 ✅
- **TP 2RR**: 23264.38 ❌
- **TP 3RR**: 23287.09 ❌
- **TP 4RR**: 23309.80 ❌
- **TP 15RR**: 23559.65 ❌
- **PnL**: -22.71 points (-1.0R)
- **MFE**: 34.59 points
- **MAE**: 27.52 points

### Trade #1246 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 14:45:00
- **FVG 5m**: 23236.63 - 23244.45
- **Entrée**: 23246.98 @ 2025-07-10 15:36:00
- **Stop Loss**: 23225.01
- **Risk**: 21.97 points
- **TP 1RR**: 23268.95 ✅
- **TP 2RR**: 23290.92 ❌
- **TP 3RR**: 23312.89 ❌
- **TP 4RR**: 23334.86 ❌
- **TP 15RR**: 23576.52 ❌
- **PnL**: -21.97 points (-1.0R)
- **MFE**: 30.04 points
- **MAE**: 36.10 points

### Trade #1247 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 19:00:00
- **FVG 5m**: 23188.40 - 23228.29
- **Entrée**: 23187.14 @ 2025-07-10 19:19:00
- **Stop Loss**: 23239.91
- **Risk**: 52.77 points
- **TP 1RR**: 23134.37 ✅
- **TP 2RR**: 23081.60 ✅
- **TP 3RR**: 23028.84 ❌
- **TP 4RR**: 22976.07 ❌
- **TP 15RR**: 22395.62 ❌
- **PnL**: -52.77 points (-1.0R)
- **MFE**: 129.52 points
- **MAE**: 54.79 points

### Trade #1248 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23126.55 - 23131.34
- **Entrée**: 23116.95 @ 2025-07-10 19:33:00
- **Stop Loss**: 23142.91
- **Risk**: 25.96 points
- **TP 1RR**: 23091.00 ✅
- **TP 2RR**: 23065.04 ❌
- **TP 3RR**: 23039.08 ❌
- **TP 4RR**: 23013.12 ❌
- **TP 15RR**: 22727.60 ❌
- **PnL**: -25.96 points (-1.0R)
- **MFE**: 39.39 points
- **MAE**: 29.79 points

### Trade #1249 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23126.55 - 23131.34
- **Entrée**: 23116.95 @ 2025-07-10 19:33:00
- **Stop Loss**: 23142.91
- **Risk**: 25.96 points
- **TP 1RR**: 23091.00 ✅
- **TP 2RR**: 23065.04 ❌
- **TP 3RR**: 23039.08 ❌
- **TP 4RR**: 23013.12 ❌
- **TP 15RR**: 22727.60 ❌
- **PnL**: -25.96 points (-1.0R)
- **MFE**: 39.39 points
- **MAE**: 29.79 points

### Trade #1250 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23123.01 - 23128.82
- **Entrée**: 23130.33 @ 2025-07-10 20:14:00
- **Stop Loss**: 23111.45
- **Risk**: 18.88 points
- **TP 1RR**: 23149.22 ✅
- **TP 2RR**: 23168.10 ✅
- **TP 3RR**: 23186.98 ✅
- **TP 4RR**: 23205.87 ❌
- **TP 15RR**: 23413.58 ❌
- **PnL**: -18.88 points (-1.0R)
- **MFE**: 73.98 points
- **MAE**: 19.19 points

### Trade #1251 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23123.01 - 23128.82
- **Entrée**: 23130.33 @ 2025-07-10 20:14:00
- **Stop Loss**: 23111.45
- **Risk**: 18.88 points
- **TP 1RR**: 23149.22 ✅
- **TP 2RR**: 23168.10 ✅
- **TP 3RR**: 23186.98 ✅
- **TP 4RR**: 23205.87 ❌
- **TP 15RR**: 23413.58 ❌
- **PnL**: -18.88 points (-1.0R)
- **MFE**: 73.98 points
- **MAE**: 19.19 points

### Trade #1252 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23123.01 - 23128.82
- **Entrée**: 23130.33 @ 2025-07-10 20:14:00
- **Stop Loss**: 23111.45
- **Risk**: 18.88 points
- **TP 1RR**: 23149.22 ✅
- **TP 2RR**: 23168.10 ✅
- **TP 3RR**: 23186.98 ✅
- **TP 4RR**: 23205.87 ❌
- **TP 15RR**: 23413.58 ❌
- **PnL**: -18.88 points (-1.0R)
- **MFE**: 73.98 points
- **MAE**: 19.19 points

### Trade #1253 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 20:00:00
- **FVG 5m**: 23123.01 - 23128.82
- **Entrée**: 23130.33 @ 2025-07-10 20:14:00
- **Stop Loss**: 23111.45
- **Risk**: 18.88 points
- **TP 1RR**: 23149.22 ✅
- **TP 2RR**: 23168.10 ✅
- **TP 3RR**: 23186.98 ✅
- **TP 4RR**: 23205.87 ❌
- **TP 15RR**: 23413.58 ❌
- **PnL**: -18.88 points (-1.0R)
- **MFE**: 73.98 points
- **MAE**: 19.19 points

### Trade #1254 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-11 05:00:00
- **FVG 5m**: 23125.28 - 23129.07
- **Entrée**: 23130.08 @ 2025-07-11 06:27:00
- **Stop Loss**: 23113.72
- **Risk**: 16.36 points
- **TP 1RR**: 23146.44 ✅
- **TP 2RR**: 23162.80 ❌
- **TP 3RR**: 23179.16 ❌
- **TP 4RR**: 23195.52 ❌
- **TP 15RR**: 23375.48 ❌
- **PnL**: -16.36 points (-1.0R)
- **MFE**: 20.96 points
- **MAE**: 18.18 points

### Trade #1255 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-11 08:30:00
- **FVG 5m**: 23164.42 - 23175.78
- **Entrée**: 23142.70 @ 2025-07-11 10:14:00
- **Stop Loss**: 23187.37
- **Risk**: 44.66 points
- **TP 1RR**: 23098.04 ❌
- **TP 2RR**: 23053.38 ❌
- **TP 3RR**: 23008.72 ❌
- **TP 4RR**: 22964.06 ❌
- **TP 15RR**: 22472.77 ❌
- **PnL**: -44.66 points (-1.0R)
- **MFE**: 7.07 points
- **MAE**: 50.24 points

### Trade #1256 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-11 09:15:00
- **FVG 5m**: 23178.56 - 23185.88
- **Entrée**: 23188.15 @ 2025-07-11 10:34:00
- **Stop Loss**: 23166.97
- **Risk**: 21.18 points
- **TP 1RR**: 23209.33 ✅
- **TP 2RR**: 23230.52 ✅
- **TP 3RR**: 23251.70 ❌
- **TP 4RR**: 23272.88 ❌
- **TP 15RR**: 23505.90 ❌
- **PnL**: -21.18 points (-1.0R)
- **MFE**: 61.35 points
- **MAE**: 37.11 points

### Trade #1257 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-11 09:45:00
- **FVG 5m**: 23164.42 - 23175.78
- **Entrée**: 23142.70 @ 2025-07-11 10:14:00
- **Stop Loss**: 23187.37
- **Risk**: 44.66 points
- **TP 1RR**: 23098.04 ❌
- **TP 2RR**: 23053.38 ❌
- **TP 3RR**: 23008.72 ❌
- **TP 4RR**: 22964.06 ❌
- **TP 15RR**: 22472.77 ❌
- **PnL**: -44.66 points (-1.0R)
- **MFE**: 7.07 points
- **MAE**: 50.24 points

### Trade #1258 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-11 14:00:00
- **FVG 5m**: 23205.32 - 23210.37
- **Entrée**: 23211.38 @ 2025-07-11 14:18:00
- **Stop Loss**: 23193.72
- **Risk**: 17.66 points
- **TP 1RR**: 23229.04 ❌
- **TP 2RR**: 23246.70 ❌
- **TP 3RR**: 23264.36 ❌
- **TP 4RR**: 23282.03 ❌
- **TP 15RR**: 23476.31 ❌
- **PnL**: -17.66 points (-1.0R)
- **MFE**: 13.63 points
- **MAE**: 17.67 points

### Trade #1259 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-13 17:00:00
- **FVG 5m**: 23076.30 - 23087.66
- **Entrée**: 23089.43 @ 2025-07-13 17:34:00
- **Stop Loss**: 23064.77
- **Risk**: 24.67 points
- **TP 1RR**: 23114.10 ✅
- **TP 2RR**: 23138.77 ❌
- **TP 3RR**: 23163.43 ❌
- **TP 4RR**: 23188.10 ❌
- **TP 15RR**: 23459.44 ❌
- **PnL**: -24.67 points (-1.0R)
- **MFE**: 27.77 points
- **MAE**: 25.75 points

### Trade #1260 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-13 17:15:00
- **FVG 5m**: 23076.30 - 23087.66
- **Entrée**: 23089.43 @ 2025-07-13 17:34:00
- **Stop Loss**: 23064.77
- **Risk**: 24.67 points
- **TP 1RR**: 23114.10 ✅
- **TP 2RR**: 23138.77 ❌
- **TP 3RR**: 23163.43 ❌
- **TP 4RR**: 23188.10 ❌
- **TP 15RR**: 23459.44 ❌
- **PnL**: -24.67 points (-1.0R)
- **MFE**: 27.77 points
- **MAE**: 25.75 points

### Trade #1261 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-13 17:30:00
- **FVG 5m**: 23085.90 - 23088.67
- **Entrée**: 23093.22 @ 2025-07-13 18:53:00
- **Stop Loss**: 23074.35
- **Risk**: 18.86 points
- **TP 1RR**: 23112.08 ❌
- **TP 2RR**: 23130.95 ❌
- **TP 3RR**: 23149.81 ❌
- **TP 4RR**: 23168.68 ❌
- **TP 15RR**: 23376.19 ❌
- **PnL**: -18.86 points (-1.0R)
- **MFE**: 11.11 points
- **MAE**: 19.44 points

### Trade #1262 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-13 18:00:00
- **FVG 5m**: 23085.90 - 23088.67
- **Entrée**: 23093.22 @ 2025-07-13 18:53:00
- **Stop Loss**: 23074.35
- **Risk**: 18.86 points
- **TP 1RR**: 23112.08 ❌
- **TP 2RR**: 23130.95 ❌
- **TP 3RR**: 23149.81 ❌
- **TP 4RR**: 23168.68 ❌
- **TP 15RR**: 23376.19 ❌
- **PnL**: -18.86 points (-1.0R)
- **MFE**: 11.11 points
- **MAE**: 19.44 points

### Trade #1263 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 02:30:00
- **FVG 5m**: 23069.74 - 23080.60
- **Entrée**: 23082.36 @ 2025-07-14 02:44:00
- **Stop Loss**: 23058.20
- **Risk**: 24.16 points
- **TP 1RR**: 23106.52 ✅
- **TP 2RR**: 23130.68 ✅
- **TP 3RR**: 23154.84 ✅
- **TP 4RR**: 23179.00 ✅
- **TP 15RR**: 23444.74 ✅
- **PnL**: 362.38 points (15.0R)
- **MFE**: 364.32 points
- **MAE**: 13.89 points

### Trade #1264 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 02:30:00
- **FVG 5m**: 23069.74 - 23080.60
- **Entrée**: 23082.36 @ 2025-07-14 02:44:00
- **Stop Loss**: 23058.20
- **Risk**: 24.16 points
- **TP 1RR**: 23106.52 ✅
- **TP 2RR**: 23130.68 ✅
- **TP 3RR**: 23154.84 ✅
- **TP 4RR**: 23179.00 ✅
- **TP 15RR**: 23444.74 ✅
- **PnL**: 362.38 points (15.0R)
- **MFE**: 364.32 points
- **MAE**: 13.89 points

### Trade #1265 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 08:15:00
- **FVG 5m**: 23166.94 - 23170.48
- **Entrée**: 23172.24 @ 2025-07-14 09:14:00
- **Stop Loss**: 23155.36
- **Risk**: 16.89 points
- **TP 1RR**: 23189.13 ✅
- **TP 2RR**: 23206.02 ✅
- **TP 3RR**: 23222.90 ❌
- **TP 4RR**: 23239.79 ❌
- **TP 15RR**: 23425.53 ❌
- **PnL**: -16.89 points (-1.0R)
- **MFE**: 44.69 points
- **MAE**: 18.18 points

### Trade #1266 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 08:15:00
- **FVG 5m**: 23166.94 - 23170.48
- **Entrée**: 23172.24 @ 2025-07-14 09:14:00
- **Stop Loss**: 23155.36
- **Risk**: 16.89 points
- **TP 1RR**: 23189.13 ✅
- **TP 2RR**: 23206.02 ✅
- **TP 3RR**: 23222.90 ❌
- **TP 4RR**: 23239.79 ❌
- **TP 15RR**: 23425.53 ❌
- **PnL**: -16.89 points (-1.0R)
- **MFE**: 44.69 points
- **MAE**: 18.18 points

### Trade #1267 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 08:30:00
- **FVG 5m**: 23172.24 - 23185.63
- **Entrée**: 23162.15 @ 2025-07-14 09:28:00
- **Stop Loss**: 23197.22
- **Risk**: 35.07 points
- **TP 1RR**: 23127.07 ❌
- **TP 2RR**: 23092.00 ❌
- **TP 3RR**: 23056.93 ❌
- **TP 4RR**: 23021.85 ❌
- **TP 15RR**: 22636.05 ❌
- **PnL**: -35.07 points (-1.0R)
- **MFE**: 12.12 points
- **MAE**: 35.60 points

### Trade #1268 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 08:30:00
- **FVG 5m**: 23172.24 - 23185.63
- **Entrée**: 23162.15 @ 2025-07-14 09:28:00
- **Stop Loss**: 23197.22
- **Risk**: 35.07 points
- **TP 1RR**: 23127.07 ❌
- **TP 2RR**: 23092.00 ❌
- **TP 3RR**: 23056.93 ❌
- **TP 4RR**: 23021.85 ❌
- **TP 15RR**: 22636.05 ❌
- **PnL**: -35.07 points (-1.0R)
- **MFE**: 12.12 points
- **MAE**: 35.60 points

### Trade #1269 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 08:45:00
- **FVG 5m**: 23166.94 - 23170.48
- **Entrée**: 23172.24 @ 2025-07-14 09:14:00
- **Stop Loss**: 23155.36
- **Risk**: 16.89 points
- **TP 1RR**: 23189.13 ✅
- **TP 2RR**: 23206.02 ✅
- **TP 3RR**: 23222.90 ❌
- **TP 4RR**: 23239.79 ❌
- **TP 15RR**: 23425.53 ❌
- **PnL**: -16.89 points (-1.0R)
- **MFE**: 44.69 points
- **MAE**: 18.18 points

### Trade #1270 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 12:30:00
- **FVG 5m**: 23275.25 - 23279.55
- **Entrée**: 23273.49 @ 2025-07-14 14:08:00
- **Stop Loss**: 23291.19
- **Risk**: 17.70 points
- **TP 1RR**: 23255.79 ✅
- **TP 2RR**: 23238.09 ✅
- **TP 3RR**: 23220.39 ❌
- **TP 4RR**: 23202.69 ❌
- **TP 15RR**: 23008.00 ❌
- **PnL**: -17.70 points (-1.0R)
- **MFE**: 49.74 points
- **MAE**: 34.34 points

### Trade #1271 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 19:00:00
- **FVG 5m**: 23233.85 - 23240.16
- **Entrée**: 23240.41 @ 2025-07-14 20:39:00
- **Stop Loss**: 23222.23
- **Risk**: 18.18 points
- **TP 1RR**: 23258.59 ✅
- **TP 2RR**: 23276.78 ✅
- **TP 3RR**: 23294.96 ✅
- **TP 4RR**: 23313.14 ✅
- **TP 15RR**: 23513.13 ❌
- **PnL**: -18.18 points (-1.0R)
- **MFE**: 212.33 points
- **MAE**: 38.12 points

### Trade #1272 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 06:15:00
- **FVG 5m**: 23399.22 - 23402.00
- **Entrée**: 23398.46 @ 2025-07-15 06:44:00
- **Stop Loss**: 23413.70
- **Risk**: 15.24 points
- **TP 1RR**: 23383.23 ✅
- **TP 2RR**: 23367.99 ✅
- **TP 3RR**: 23352.76 ❌
- **TP 4RR**: 23337.52 ❌
- **TP 15RR**: 23169.93 ❌
- **PnL**: -15.24 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 31.31 points

### Trade #1273 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 07:30:00
- **FVG 5m**: 23415.13 - 23428.00
- **Entrée**: 23401.49 @ 2025-07-15 08:33:00
- **Stop Loss**: 23439.72
- **Risk**: 38.22 points
- **TP 1RR**: 23363.27 ✅
- **TP 2RR**: 23325.04 ✅
- **TP 3RR**: 23286.82 ✅
- **TP 4RR**: 23248.60 ✅
- **TP 15RR**: 22828.13 ❌
- **PnL**: -38.22 points (-1.0R)
- **MFE**: 339.83 points
- **MAE**: 38.38 points

### Trade #1274 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 07:30:00
- **FVG 5m**: 23415.13 - 23428.00
- **Entrée**: 23401.49 @ 2025-07-15 08:33:00
- **Stop Loss**: 23439.72
- **Risk**: 38.22 points
- **TP 1RR**: 23363.27 ✅
- **TP 2RR**: 23325.04 ✅
- **TP 3RR**: 23286.82 ✅
- **TP 4RR**: 23248.60 ✅
- **TP 15RR**: 22828.13 ❌
- **PnL**: -38.22 points (-1.0R)
- **MFE**: 339.83 points
- **MAE**: 38.38 points

### Trade #1275 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 09:45:00
- **FVG 5m**: 23359.83 - 23365.14
- **Entrée**: 23354.03 @ 2025-07-15 11:54:00
- **Stop Loss**: 23376.82
- **Risk**: 22.79 points
- **TP 1RR**: 23331.24 ✅
- **TP 2RR**: 23308.44 ❌
- **TP 3RR**: 23285.65 ❌
- **TP 4RR**: 23262.86 ❌
- **TP 15RR**: 23012.15 ❌
- **PnL**: -22.79 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 24.24 points

### Trade #1276 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 11:45:00
- **FVG 5m**: 23349.73 - 23357.06
- **Entrée**: 23359.08 @ 2025-07-15 12:34:00
- **Stop Loss**: 23338.06
- **Risk**: 21.02 points
- **TP 1RR**: 23380.09 ✅
- **TP 2RR**: 23401.11 ✅
- **TP 3RR**: 23422.13 ❌
- **TP 4RR**: 23443.14 ❌
- **TP 15RR**: 23674.32 ❌
- **PnL**: -21.02 points (-1.0R)
- **MFE**: 50.50 points
- **MAE**: 26.76 points

### Trade #1277 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 12:30:00
- **FVG 5m**: 23373.97 - 23381.80
- **Entrée**: 23386.34 @ 2025-07-15 12:54:00
- **Stop Loss**: 23362.29
- **Risk**: 24.06 points
- **TP 1RR**: 23410.40 ❌
- **TP 2RR**: 23434.46 ❌
- **TP 3RR**: 23458.52 ❌
- **TP 4RR**: 23482.58 ❌
- **TP 15RR**: 23747.22 ❌
- **PnL**: -24.06 points (-1.0R)
- **MFE**: 23.23 points
- **MAE**: 32.32 points

### Trade #1278 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 14:45:00
- **FVG 5m**: 23287.88 - 23316.91
- **Entrée**: 23280.30 @ 2025-07-15 14:59:00
- **Stop Loss**: 23328.57
- **Risk**: 48.27 points
- **TP 1RR**: 23232.04 ✅
- **TP 2RR**: 23183.77 ✅
- **TP 3RR**: 23135.50 ✅
- **TP 4RR**: 23087.23 ✅
- **TP 15RR**: 22556.29 ❌
- **PnL**: -48.27 points (-1.0R)
- **MFE**: 218.64 points
- **MAE**: 48.48 points

### Trade #1279 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 17:00:00
- **FVG 5m**: 23236.63 - 23243.95
- **Entrée**: 23235.87 @ 2025-07-15 17:12:00
- **Stop Loss**: 23255.57
- **Risk**: 19.70 points
- **TP 1RR**: 23216.17 ✅
- **TP 2RR**: 23196.47 ❌
- **TP 3RR**: 23176.76 ❌
- **TP 4RR**: 23157.06 ❌
- **TP 15RR**: 22940.35 ❌
- **PnL**: -19.70 points (-1.0R)
- **MFE**: 34.59 points
- **MAE**: 19.95 points

### Trade #1280 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 17:00:00
- **FVG 5m**: 23236.63 - 23243.95
- **Entrée**: 23235.87 @ 2025-07-15 17:12:00
- **Stop Loss**: 23255.57
- **Risk**: 19.70 points
- **TP 1RR**: 23216.17 ✅
- **TP 2RR**: 23196.47 ❌
- **TP 3RR**: 23176.76 ❌
- **TP 4RR**: 23157.06 ❌
- **TP 15RR**: 22940.35 ❌
- **PnL**: -19.70 points (-1.0R)
- **MFE**: 34.59 points
- **MAE**: 19.95 points

### Trade #1281 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 17:00:00
- **FVG 5m**: 23236.63 - 23243.95
- **Entrée**: 23235.87 @ 2025-07-15 17:12:00
- **Stop Loss**: 23255.57
- **Risk**: 19.70 points
- **TP 1RR**: 23216.17 ✅
- **TP 2RR**: 23196.47 ❌
- **TP 3RR**: 23176.76 ❌
- **TP 4RR**: 23157.06 ❌
- **TP 15RR**: 22940.35 ❌
- **PnL**: -19.70 points (-1.0R)
- **MFE**: 34.59 points
- **MAE**: 19.95 points

### Trade #1282 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 17:45:00
- **FVG 5m**: 23222.99 - 23228.80
- **Entrée**: 23230.57 @ 2025-07-15 18:35:00
- **Stop Loss**: 23211.38
- **Risk**: 19.19 points
- **TP 1RR**: 23249.75 ❌
- **TP 2RR**: 23268.94 ❌
- **TP 3RR**: 23288.12 ❌
- **TP 4RR**: 23307.31 ❌
- **TP 15RR**: 23518.35 ❌
- **PnL**: -19.19 points (-1.0R)
- **MFE**: 17.42 points
- **MAE**: 19.95 points

### Trade #1283 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 19:30:00
- **FVG 5m**: 23232.08 - 23239.15
- **Entrée**: 23240.16 @ 2025-07-15 20:08:00
- **Stop Loss**: 23220.46
- **Risk**: 19.70 points
- **TP 1RR**: 23259.86 ✅
- **TP 2RR**: 23279.55 ❌
- **TP 3RR**: 23299.25 ❌
- **TP 4RR**: 23318.94 ❌
- **TP 15RR**: 23535.59 ❌
- **PnL**: -19.70 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 20.70 points

### Trade #1284 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-16 00:45:00
- **FVG 5m**: 23190.93 - 23199.26
- **Entrée**: 23199.76 @ 2025-07-16 02:19:00
- **Stop Loss**: 23179.33
- **Risk**: 20.43 points
- **TP 1RR**: 23220.20 ✅
- **TP 2RR**: 23240.63 ✅
- **TP 3RR**: 23261.06 ✅
- **TP 4RR**: 23281.49 ✅
- **TP 15RR**: 23506.25 ❌
- **PnL**: -20.43 points (-1.0R)
- **MFE**: 118.41 points
- **MAE**: 21.21 points

### Trade #1285 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-16 02:15:00
- **FVG 5m**: 23218.70 - 23221.98
- **Entrée**: 23222.99 @ 2025-07-16 03:33:00
- **Stop Loss**: 23207.09
- **Risk**: 15.90 points
- **TP 1RR**: 23238.89 ✅
- **TP 2RR**: 23254.79 ❌
- **TP 3RR**: 23270.70 ❌
- **TP 4RR**: 23286.60 ❌
- **TP 15RR**: 23461.51 ❌
- **PnL**: -15.90 points (-1.0R)
- **MFE**: 19.69 points
- **MAE**: 15.91 points

### Trade #1286 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-16 02:15:00
- **FVG 5m**: 23218.70 - 23221.98
- **Entrée**: 23222.99 @ 2025-07-16 03:33:00
- **Stop Loss**: 23207.09
- **Risk**: 15.90 points
- **TP 1RR**: 23238.89 ✅
- **TP 2RR**: 23254.79 ❌
- **TP 3RR**: 23270.70 ❌
- **TP 4RR**: 23286.60 ❌
- **TP 15RR**: 23461.51 ❌
- **PnL**: -15.90 points (-1.0R)
- **MFE**: 19.69 points
- **MAE**: 15.91 points

### Trade #1287 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23213.40 - 23224.25
- **Entrée**: 23202.79 @ 2025-07-16 08:51:00
- **Stop Loss**: 23235.87
- **Risk**: 33.07 points
- **TP 1RR**: 23169.72 ❌
- **TP 2RR**: 23136.65 ❌
- **TP 3RR**: 23103.58 ❌
- **TP 4RR**: 23070.50 ❌
- **TP 15RR**: 22706.70 ❌
- **PnL**: -33.07 points (-1.0R)
- **MFE**: 26.76 points
- **MAE**: 33.58 points

### Trade #1288 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23213.40 - 23224.25
- **Entrée**: 23202.79 @ 2025-07-16 08:51:00
- **Stop Loss**: 23235.87
- **Risk**: 33.07 points
- **TP 1RR**: 23169.72 ❌
- **TP 2RR**: 23136.65 ❌
- **TP 3RR**: 23103.58 ❌
- **TP 4RR**: 23070.50 ❌
- **TP 15RR**: 22706.70 ❌
- **PnL**: -33.07 points (-1.0R)
- **MFE**: 26.76 points
- **MAE**: 33.58 points

### Trade #1289 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23213.40 - 23224.25
- **Entrée**: 23202.79 @ 2025-07-16 08:51:00
- **Stop Loss**: 23235.87
- **Risk**: 33.07 points
- **TP 1RR**: 23169.72 ❌
- **TP 2RR**: 23136.65 ❌
- **TP 3RR**: 23103.58 ❌
- **TP 4RR**: 23070.50 ❌
- **TP 15RR**: 22706.70 ❌
- **PnL**: -33.07 points (-1.0R)
- **MFE**: 26.76 points
- **MAE**: 33.58 points

### Trade #1290 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23213.40 - 23224.25
- **Entrée**: 23202.79 @ 2025-07-16 08:51:00
- **Stop Loss**: 23235.87
- **Risk**: 33.07 points
- **TP 1RR**: 23169.72 ❌
- **TP 2RR**: 23136.65 ❌
- **TP 3RR**: 23103.58 ❌
- **TP 4RR**: 23070.50 ❌
- **TP 15RR**: 22706.70 ❌
- **PnL**: -33.07 points (-1.0R)
- **MFE**: 26.76 points
- **MAE**: 33.58 points

### Trade #1291 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-16 10:15:00
- **FVG 5m**: 23125.03 - 23146.24
- **Entrée**: 23148.01 @ 2025-07-16 10:42:00
- **Stop Loss**: 23113.47
- **Risk**: 34.54 points
- **TP 1RR**: 23182.54 ✅
- **TP 2RR**: 23217.08 ✅
- **TP 3RR**: 23251.62 ✅
- **TP 4RR**: 23286.16 ✅
- **TP 15RR**: 23666.07 ✅
- **PnL**: 518.07 points (15.0R)
- **MFE**: 518.84 points
- **MAE**: 7.83 points

### Trade #1292 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 14:00:00
- **FVG 5m**: 23304.04 - 23307.07
- **Entrée**: 23303.53 @ 2025-07-16 14:59:00
- **Stop Loss**: 23318.72
- **Risk**: 15.19 points
- **TP 1RR**: 23288.34 ✅
- **TP 2RR**: 23273.16 ✅
- **TP 3RR**: 23257.97 ✅
- **TP 4RR**: 23242.78 ❌
- **TP 15RR**: 23075.71 ❌
- **PnL**: -15.19 points (-1.0R)
- **MFE**: 58.57 points
- **MAE**: 18.94 points

### Trade #1293 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-17 06:00:00
- **FVG 5m**: 23318.18 - 23321.96
- **Entrée**: 23324.74 @ 2025-07-17 07:02:00
- **Stop Loss**: 23306.52
- **Risk**: 18.22 points
- **TP 1RR**: 23342.96 ❌
- **TP 2RR**: 23361.19 ❌
- **TP 3RR**: 23379.41 ❌
- **TP 4RR**: 23397.63 ❌
- **TP 15RR**: 23598.09 ❌
- **PnL**: -18.22 points (-1.0R)
- **MFE**: 5.81 points
- **MAE**: 20.20 points

### Trade #1294 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-17 07:00:00
- **FVG 5m**: 23318.68 - 23321.96
- **Entrée**: 23315.40 @ 2025-07-17 07:14:00
- **Stop Loss**: 23333.62
- **Risk**: 18.23 points
- **TP 1RR**: 23297.17 ❌
- **TP 2RR**: 23278.95 ❌
- **TP 3RR**: 23260.72 ❌
- **TP 4RR**: 23242.50 ❌
- **TP 15RR**: 23042.02 ❌
- **PnL**: -18.23 points (-1.0R)
- **MFE**: 13.63 points
- **MAE**: 33.83 points

### Trade #1295 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 02:00:00
- **FVG 5m**: 23510.81 - 23518.39
- **Entrée**: 23507.78 @ 2025-07-18 02:12:00
- **Stop Loss**: 23530.15
- **Risk**: 22.36 points
- **TP 1RR**: 23485.42 ✅
- **TP 2RR**: 23463.06 ❌
- **TP 3RR**: 23440.70 ❌
- **TP 4RR**: 23418.33 ❌
- **TP 15RR**: 23172.34 ❌
- **PnL**: -22.36 points (-1.0R)
- **MFE**: 26.26 points
- **MAE**: 43.93 points

### Trade #1296 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 02:00:00
- **FVG 5m**: 23510.81 - 23518.39
- **Entrée**: 23507.78 @ 2025-07-18 02:12:00
- **Stop Loss**: 23530.15
- **Risk**: 22.36 points
- **TP 1RR**: 23485.42 ✅
- **TP 2RR**: 23463.06 ❌
- **TP 3RR**: 23440.70 ❌
- **TP 4RR**: 23418.33 ❌
- **TP 15RR**: 23172.34 ❌
- **PnL**: -22.36 points (-1.0R)
- **MFE**: 26.26 points
- **MAE**: 43.93 points

### Trade #1297 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 02:00:00
- **FVG 5m**: 23510.81 - 23518.39
- **Entrée**: 23507.78 @ 2025-07-18 02:12:00
- **Stop Loss**: 23530.15
- **Risk**: 22.36 points
- **TP 1RR**: 23485.42 ✅
- **TP 2RR**: 23463.06 ❌
- **TP 3RR**: 23440.70 ❌
- **TP 4RR**: 23418.33 ❌
- **TP 15RR**: 23172.34 ❌
- **PnL**: -22.36 points (-1.0R)
- **MFE**: 26.26 points
- **MAE**: 43.93 points

### Trade #1298 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-18 08:15:00
- **FVG 5m**: 23447.70 - 23454.51
- **Entrée**: 23457.29 @ 2025-07-18 10:31:00
- **Stop Loss**: 23435.97
- **Risk**: 21.32 points
- **TP 1RR**: 23478.61 ✅
- **TP 2RR**: 23499.93 ❌
- **TP 3RR**: 23521.24 ❌
- **TP 4RR**: 23542.56 ❌
- **TP 15RR**: 23777.06 ❌
- **PnL**: -21.32 points (-1.0R)
- **MFE**: 27.27 points
- **MAE**: 21.46 points

### Trade #1299 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-20 18:45:00
- **FVG 5m**: 23485.82 - 23488.85
- **Entrée**: 23490.36 @ 2025-07-20 20:03:00
- **Stop Loss**: 23474.08
- **Risk**: 16.29 points
- **TP 1RR**: 23506.65 ✅
- **TP 2RR**: 23522.94 ❌
- **TP 3RR**: 23539.23 ❌
- **TP 4RR**: 23555.51 ❌
- **TP 15RR**: 23734.68 ❌
- **PnL**: -16.29 points (-1.0R)
- **MFE**: 17.42 points
- **MAE**: 17.67 points

### Trade #1300 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-21 07:45:00
- **FVG 5m**: 23472.94 - 23481.27
- **Entrée**: 23470.67 @ 2025-07-21 07:56:00
- **Stop Loss**: 23493.02
- **Risk**: 22.34 points
- **TP 1RR**: 23448.33 ❌
- **TP 2RR**: 23425.98 ❌
- **TP 3RR**: 23403.64 ❌
- **TP 4RR**: 23381.29 ❌
- **TP 15RR**: 23135.50 ❌
- **PnL**: -22.34 points (-1.0R)
- **MFE**: 16.92 points
- **MAE**: 46.46 points

### Trade #1301 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-21 08:15:00
- **FVG 5m**: 23476.73 - 23485.57
- **Entrée**: 23485.82 @ 2025-07-21 08:29:00
- **Stop Loss**: 23464.99
- **Risk**: 20.83 points
- **TP 1RR**: 23506.65 ✅
- **TP 2RR**: 23527.47 ✅
- **TP 3RR**: 23548.30 ✅
- **TP 4RR**: 23569.13 ✅
- **TP 15RR**: 23798.23 ❌
- **PnL**: -20.83 points (-1.0R)
- **MFE**: 170.93 points
- **MAE**: 23.73 points

### Trade #1302 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-21 08:15:00
- **FVG 5m**: 23476.73 - 23485.57
- **Entrée**: 23485.82 @ 2025-07-21 08:29:00
- **Stop Loss**: 23464.99
- **Risk**: 20.83 points
- **TP 1RR**: 23506.65 ✅
- **TP 2RR**: 23527.47 ✅
- **TP 3RR**: 23548.30 ✅
- **TP 4RR**: 23569.13 ✅
- **TP 15RR**: 23798.23 ❌
- **PnL**: -20.83 points (-1.0R)
- **MFE**: 170.93 points
- **MAE**: 23.73 points

### Trade #1303 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-21 08:30:00
- **FVG 5m**: 23561.56 - 23568.88
- **Entrée**: 23576.71 @ 2025-07-21 08:42:00
- **Stop Loss**: 23549.78
- **Risk**: 26.93 points
- **TP 1RR**: 23603.64 ✅
- **TP 2RR**: 23630.57 ✅
- **TP 3RR**: 23657.50 ❌
- **TP 4RR**: 23684.43 ❌
- **TP 15RR**: 23980.65 ❌
- **PnL**: -26.93 points (-1.0R)
- **MFE**: 80.03 points
- **MAE**: 28.78 points

### Trade #1304 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23540.35 - 23546.92
- **Entrée**: 23537.07 @ 2025-07-22 03:04:00
- **Stop Loss**: 23558.69
- **Risk**: 21.62 points
- **TP 1RR**: 23515.45 ✅
- **TP 2RR**: 23493.83 ❌
- **TP 3RR**: 23472.21 ❌
- **TP 4RR**: 23450.59 ❌
- **TP 15RR**: 23212.77 ❌
- **PnL**: -21.62 points (-1.0R)
- **MFE**: 39.13 points
- **MAE**: 23.48 points

### Trade #1305 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23540.35 - 23546.92
- **Entrée**: 23537.07 @ 2025-07-22 03:04:00
- **Stop Loss**: 23558.69
- **Risk**: 21.62 points
- **TP 1RR**: 23515.45 ✅
- **TP 2RR**: 23493.83 ❌
- **TP 3RR**: 23472.21 ❌
- **TP 4RR**: 23450.59 ❌
- **TP 15RR**: 23212.77 ❌
- **PnL**: -21.62 points (-1.0R)
- **MFE**: 39.13 points
- **MAE**: 23.48 points

### Trade #1306 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23540.35 - 23546.92
- **Entrée**: 23537.07 @ 2025-07-22 03:04:00
- **Stop Loss**: 23558.69
- **Risk**: 21.62 points
- **TP 1RR**: 23515.45 ✅
- **TP 2RR**: 23493.83 ❌
- **TP 3RR**: 23472.21 ❌
- **TP 4RR**: 23450.59 ❌
- **TP 15RR**: 23212.77 ❌
- **PnL**: -21.62 points (-1.0R)
- **MFE**: 39.13 points
- **MAE**: 23.48 points

### Trade #1307 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23514.60 - 23523.94
- **Entrée**: 23524.70 @ 2025-07-22 05:02:00
- **Stop Loss**: 23502.84
- **Risk**: 21.86 points
- **TP 1RR**: 23546.56 ✅
- **TP 2RR**: 23568.41 ✅
- **TP 3RR**: 23590.27 ❌
- **TP 4RR**: 23612.13 ❌
- **TP 15RR**: 23852.55 ❌
- **PnL**: -21.86 points (-1.0R)
- **MFE**: 56.30 points
- **MAE**: 21.97 points

### Trade #1308 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 07:15:00
- **FVG 5m**: 23371.20 - 23394.93
- **Entrée**: 23406.29 @ 2025-07-22 09:09:00
- **Stop Loss**: 23359.51
- **Risk**: 46.78 points
- **TP 1RR**: 23453.07 ✅
- **TP 2RR**: 23499.85 ✅
- **TP 3RR**: 23546.63 ✅
- **TP 4RR**: 23593.41 ✅
- **TP 15RR**: 24107.99 ❌
- **PnL**: -46.78 points (-1.0R)
- **MFE**: 674.87 points
- **MAE**: 49.99 points

### Trade #1309 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 09:00:00
- **FVG 5m**: 23402.25 - 23430.78
- **Entrée**: 23432.04 @ 2025-07-22 09:34:00
- **Stop Loss**: 23390.55
- **Risk**: 41.49 points
- **TP 1RR**: 23473.54 ❌
- **TP 2RR**: 23515.03 ❌
- **TP 3RR**: 23556.52 ❌
- **TP 4RR**: 23598.02 ❌
- **TP 15RR**: 24054.44 ❌
- **PnL**: -41.49 points (-1.0R)
- **MFE**: 35.35 points
- **MAE**: 43.17 points

### Trade #1310 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 09:30:00
- **FVG 5m**: 23410.58 - 23416.14
- **Entrée**: 23418.41 @ 2025-07-22 11:51:00
- **Stop Loss**: 23398.88
- **Risk**: 19.53 points
- **TP 1RR**: 23437.94 ✅
- **TP 2RR**: 23457.47 ✅
- **TP 3RR**: 23477.00 ✅
- **TP 4RR**: 23496.54 ✅
- **TP 15RR**: 23711.39 ❌
- **PnL**: -19.53 points (-1.0R)
- **MFE**: 95.94 points
- **MAE**: 24.24 points

### Trade #1311 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 09:45:00
- **FVG 5m**: 23410.58 - 23416.14
- **Entrée**: 23418.41 @ 2025-07-22 11:51:00
- **Stop Loss**: 23398.88
- **Risk**: 19.53 points
- **TP 1RR**: 23437.94 ✅
- **TP 2RR**: 23457.47 ✅
- **TP 3RR**: 23477.00 ✅
- **TP 4RR**: 23496.54 ✅
- **TP 15RR**: 23711.39 ❌
- **PnL**: -19.53 points (-1.0R)
- **MFE**: 95.94 points
- **MAE**: 24.24 points

### Trade #1312 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 12:15:00
- **FVG 5m**: 23454.26 - 23466.38
- **Entrée**: 23477.49 @ 2025-07-22 12:28:00
- **Stop Loss**: 23442.53
- **Risk**: 34.95 points
- **TP 1RR**: 23512.44 ❌
- **TP 2RR**: 23547.40 ❌
- **TP 3RR**: 23582.35 ❌
- **TP 4RR**: 23617.31 ❌
- **TP 15RR**: 24001.81 ❌
- **PnL**: -34.95 points (-1.0R)
- **MFE**: 0.50 points
- **MAE**: 38.38 points

### Trade #1313 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 12:15:00
- **FVG 5m**: 23454.26 - 23466.38
- **Entrée**: 23477.49 @ 2025-07-22 12:28:00
- **Stop Loss**: 23442.53
- **Risk**: 34.95 points
- **TP 1RR**: 23512.44 ❌
- **TP 2RR**: 23547.40 ❌
- **TP 3RR**: 23582.35 ❌
- **TP 4RR**: 23617.31 ❌
- **TP 15RR**: 24001.81 ❌
- **PnL**: -34.95 points (-1.0R)
- **MFE**: 0.50 points
- **MAE**: 38.38 points

### Trade #1314 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 14:00:00
- **FVG 5m**: 23453.75 - 23460.82
- **Entrée**: 23451.99 @ 2025-07-22 14:59:00
- **Stop Loss**: 23472.55
- **Risk**: 20.57 points
- **TP 1RR**: 23431.42 ✅
- **TP 2RR**: 23410.85 ✅
- **TP 3RR**: 23390.29 ❌
- **TP 4RR**: 23369.72 ❌
- **TP 15RR**: 23143.48 ❌
- **PnL**: -20.57 points (-1.0R)
- **MFE**: 52.26 points
- **MAE**: 20.70 points

### Trade #1315 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 18:45:00
- **FVG 5m**: 23442.39 - 23450.47
- **Entrée**: 23454.76 @ 2025-07-22 20:15:00
- **Stop Loss**: 23430.67
- **Risk**: 24.09 points
- **TP 1RR**: 23478.86 ✅
- **TP 2RR**: 23502.95 ✅
- **TP 3RR**: 23527.04 ❌
- **TP 4RR**: 23551.13 ❌
- **TP 15RR**: 23816.15 ❌
- **PnL**: -24.09 points (-1.0R)
- **MFE**: 59.58 points
- **MAE**: 29.29 points

### Trade #1316 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 19:00:00
- **FVG 5m**: 23462.59 - 23472.19
- **Entrée**: 23461.58 @ 2025-07-22 21:14:00
- **Stop Loss**: 23483.92
- **Risk**: 22.34 points
- **TP 1RR**: 23439.24 ❌
- **TP 2RR**: 23416.90 ❌
- **TP 3RR**: 23394.56 ❌
- **TP 4RR**: 23372.22 ❌
- **TP 15RR**: 23126.48 ❌
- **PnL**: -22.34 points (-1.0R)
- **MFE**: 5.55 points
- **MAE**: 22.98 points

### Trade #1317 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 08:15:00
- **FVG 5m**: 23415.13 - 23418.66
- **Entrée**: 23421.44 @ 2025-07-23 09:51:00
- **Stop Loss**: 23403.42
- **Risk**: 18.02 points
- **TP 1RR**: 23439.46 ✅
- **TP 2RR**: 23457.48 ✅
- **TP 3RR**: 23475.50 ✅
- **TP 4RR**: 23493.52 ✅
- **TP 15RR**: 23691.73 ✅
- **PnL**: 270.29 points (15.0R)
- **MFE**: 275.96 points
- **MAE**: 12.88 points

### Trade #1318 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 09:15:00
- **FVG 5m**: 23415.13 - 23418.66
- **Entrée**: 23421.44 @ 2025-07-23 09:51:00
- **Stop Loss**: 23403.42
- **Risk**: 18.02 points
- **TP 1RR**: 23439.46 ✅
- **TP 2RR**: 23457.48 ✅
- **TP 3RR**: 23475.50 ✅
- **TP 4RR**: 23493.52 ✅
- **TP 15RR**: 23691.73 ✅
- **PnL**: 270.29 points (15.0R)
- **MFE**: 275.96 points
- **MAE**: 12.88 points

### Trade #1319 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 09:15:00
- **FVG 5m**: 23415.13 - 23418.66
- **Entrée**: 23421.44 @ 2025-07-23 09:51:00
- **Stop Loss**: 23403.42
- **Risk**: 18.02 points
- **TP 1RR**: 23439.46 ✅
- **TP 2RR**: 23457.48 ✅
- **TP 3RR**: 23475.50 ✅
- **TP 4RR**: 23493.52 ✅
- **TP 15RR**: 23691.73 ✅
- **PnL**: 270.29 points (15.0R)
- **MFE**: 275.96 points
- **MAE**: 12.88 points

### Trade #1320 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 09:45:00
- **FVG 5m**: 23448.20 - 23473.45
- **Entrée**: 23492.64 @ 2025-07-23 10:54:00
- **Stop Loss**: 23436.48
- **Risk**: 56.16 points
- **TP 1RR**: 23548.80 ❌
- **TP 2RR**: 23604.96 ❌
- **TP 3RR**: 23661.12 ❌
- **TP 4RR**: 23717.28 ❌
- **TP 15RR**: 24335.03 ❌
- **PnL**: -56.16 points (-1.0R)
- **MFE**: 31.56 points
- **MAE**: 70.19 points

### Trade #1321 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23469.66 - 23473.45
- **Entrée**: 23467.39 @ 2025-07-23 11:12:00
- **Stop Loss**: 23485.18
- **Risk**: 17.80 points
- **TP 1RR**: 23449.59 ✅
- **TP 2RR**: 23431.80 ✅
- **TP 3RR**: 23414.00 ❌
- **TP 4RR**: 23396.20 ❌
- **TP 15RR**: 23200.45 ❌
- **PnL**: -17.80 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 23.99 points

### Trade #1322 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23469.66 - 23473.45
- **Entrée**: 23467.39 @ 2025-07-23 11:12:00
- **Stop Loss**: 23485.18
- **Risk**: 17.80 points
- **TP 1RR**: 23449.59 ✅
- **TP 2RR**: 23431.80 ✅
- **TP 3RR**: 23414.00 ❌
- **TP 4RR**: 23396.20 ❌
- **TP 15RR**: 23200.45 ❌
- **PnL**: -17.80 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 23.99 points

### Trade #1323 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23469.66 - 23473.45
- **Entrée**: 23467.39 @ 2025-07-23 11:12:00
- **Stop Loss**: 23485.18
- **Risk**: 17.80 points
- **TP 1RR**: 23449.59 ✅
- **TP 2RR**: 23431.80 ✅
- **TP 3RR**: 23414.00 ❌
- **TP 4RR**: 23396.20 ❌
- **TP 15RR**: 23200.45 ❌
- **PnL**: -17.80 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 23.99 points

### Trade #1324 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23458.05 - 23461.08
- **Entrée**: 23462.59 @ 2025-07-23 12:23:00
- **Stop Loss**: 23446.32
- **Risk**: 16.27 points
- **TP 1RR**: 23478.87 ✅
- **TP 2RR**: 23495.14 ✅
- **TP 3RR**: 23511.41 ✅
- **TP 4RR**: 23527.69 ✅
- **TP 15RR**: 23706.70 ✅
- **PnL**: 244.10 points (15.0R)
- **MFE**: 245.91 points
- **MAE**: 7.07 points

### Trade #1325 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23458.05 - 23461.08
- **Entrée**: 23462.59 @ 2025-07-23 12:23:00
- **Stop Loss**: 23446.32
- **Risk**: 16.27 points
- **TP 1RR**: 23478.87 ✅
- **TP 2RR**: 23495.14 ✅
- **TP 3RR**: 23511.41 ✅
- **TP 4RR**: 23527.69 ✅
- **TP 15RR**: 23706.70 ✅
- **PnL**: 244.10 points (15.0R)
- **MFE**: 245.91 points
- **MAE**: 7.07 points

### Trade #1326 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23458.05 - 23461.08
- **Entrée**: 23462.59 @ 2025-07-23 12:23:00
- **Stop Loss**: 23446.32
- **Risk**: 16.27 points
- **TP 1RR**: 23478.87 ✅
- **TP 2RR**: 23495.14 ✅
- **TP 3RR**: 23511.41 ✅
- **TP 4RR**: 23527.69 ✅
- **TP 15RR**: 23706.70 ✅
- **PnL**: 244.10 points (15.0R)
- **MFE**: 245.91 points
- **MAE**: 7.07 points

### Trade #1327 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 15:00:00
- **FVG 5m**: 23584.79 - 23609.03
- **Entrée**: 23611.80 @ 2025-07-23 15:12:00
- **Stop Loss**: 23573.00
- **Risk**: 38.81 points
- **TP 1RR**: 23650.61 ✅
- **TP 2RR**: 23689.42 ❌
- **TP 3RR**: 23728.23 ❌
- **TP 4RR**: 23767.03 ❌
- **TP 15RR**: 24193.91 ❌
- **PnL**: -38.81 points (-1.0R)
- **MFE**: 42.92 points
- **MAE**: 39.64 points

### Trade #1328 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-23 15:15:00
- **FVG 5m**: 23630.24 - 23634.28
- **Entrée**: 23626.45 @ 2025-07-23 17:02:00
- **Stop Loss**: 23646.09
- **Risk**: 19.64 points
- **TP 1RR**: 23606.80 ❌
- **TP 2RR**: 23587.16 ❌
- **TP 3RR**: 23567.52 ❌
- **TP 4RR**: 23547.87 ❌
- **TP 15RR**: 23331.79 ❌
- **PnL**: -19.64 points (-1.0R)
- **MFE**: 12.88 points
- **MAE**: 20.45 points

### Trade #1329 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 07:30:00
- **FVG 5m**: 23581.26 - 23586.30
- **Entrée**: 23574.19 @ 2025-07-24 07:44:00
- **Stop Loss**: 23598.10
- **Risk**: 23.91 points
- **TP 1RR**: 23550.27 ❌
- **TP 2RR**: 23526.36 ❌
- **TP 3RR**: 23502.45 ❌
- **TP 4RR**: 23478.54 ❌
- **TP 15RR**: 23215.51 ❌
- **PnL**: -23.91 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 25.75 points

### Trade #1330 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 07:30:00
- **FVG 5m**: 23581.26 - 23586.30
- **Entrée**: 23574.19 @ 2025-07-24 07:44:00
- **Stop Loss**: 23598.10
- **Risk**: 23.91 points
- **TP 1RR**: 23550.27 ❌
- **TP 2RR**: 23526.36 ❌
- **TP 3RR**: 23502.45 ❌
- **TP 4RR**: 23478.54 ❌
- **TP 15RR**: 23215.51 ❌
- **PnL**: -23.91 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 25.75 points

### Trade #1331 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 07:45:00
- **FVG 5m**: 23590.34 - 23598.42
- **Entrée**: 23598.93 @ 2025-07-24 08:24:00
- **Stop Loss**: 23578.55
- **Risk**: 20.38 points
- **TP 1RR**: 23619.31 ✅
- **TP 2RR**: 23639.69 ❌
- **TP 3RR**: 23660.07 ❌
- **TP 4RR**: 23680.45 ❌
- **TP 15RR**: 23904.62 ❌
- **PnL**: -20.38 points (-1.0R)
- **MFE**: 32.32 points
- **MAE**: 24.49 points

### Trade #1332 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 08:15:00
- **FVG 5m**: 23574.19 - 23579.24
- **Entrée**: 23580.25 @ 2025-07-24 09:36:00
- **Stop Loss**: 23562.40
- **Risk**: 17.85 points
- **TP 1RR**: 23598.09 ✅
- **TP 2RR**: 23615.94 ✅
- **TP 3RR**: 23633.78 ✅
- **TP 4RR**: 23651.63 ✅
- **TP 15RR**: 23847.94 ❌
- **PnL**: -17.85 points (-1.0R)
- **MFE**: 93.67 points
- **MAE**: 18.43 points

### Trade #1333 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 08:15:00
- **FVG 5m**: 23574.19 - 23579.24
- **Entrée**: 23580.25 @ 2025-07-24 09:36:00
- **Stop Loss**: 23562.40
- **Risk**: 17.85 points
- **TP 1RR**: 23598.09 ✅
- **TP 2RR**: 23615.94 ✅
- **TP 3RR**: 23633.78 ✅
- **TP 4RR**: 23651.63 ✅
- **TP 15RR**: 23847.94 ❌
- **PnL**: -17.85 points (-1.0R)
- **MFE**: 93.67 points
- **MAE**: 18.43 points

### Trade #1334 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 09:00:00
- **FVG 5m**: 23603.47 - 23618.37
- **Entrée**: 23601.45 @ 2025-07-24 11:01:00
- **Stop Loss**: 23630.18
- **Risk**: 28.73 points
- **TP 1RR**: 23572.73 ✅
- **TP 2RR**: 23544.00 ❌
- **TP 3RR**: 23515.28 ❌
- **TP 4RR**: 23486.55 ❌
- **TP 15RR**: 23170.58 ❌
- **PnL**: -28.73 points (-1.0R)
- **MFE**: 30.30 points
- **MAE**: 30.30 points

### Trade #1335 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 12:00:00
- **FVG 5m**: 23623.42 - 23630.99
- **Entrée**: 23633.27 @ 2025-07-24 12:12:00
- **Stop Loss**: 23611.61
- **Risk**: 21.66 points
- **TP 1RR**: 23654.92 ✅
- **TP 2RR**: 23676.58 ❌
- **TP 3RR**: 23698.24 ❌
- **TP 4RR**: 23719.90 ❌
- **TP 15RR**: 23958.14 ❌
- **PnL**: -21.66 points (-1.0R)
- **MFE**: 21.71 points
- **MAE**: 25.25 points

### Trade #1336 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 12:15:00
- **FVG 5m**: 23635.03 - 23637.81
- **Entrée**: 23633.01 @ 2025-07-24 13:43:00
- **Stop Loss**: 23649.63
- **Risk**: 16.62 points
- **TP 1RR**: 23616.40 ✅
- **TP 2RR**: 23599.78 ❌
- **TP 3RR**: 23583.16 ❌
- **TP 4RR**: 23566.55 ❌
- **TP 15RR**: 23383.77 ❌
- **PnL**: -16.62 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 19.44 points

### Trade #1337 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 12:15:00
- **FVG 5m**: 23635.03 - 23637.81
- **Entrée**: 23633.01 @ 2025-07-24 13:43:00
- **Stop Loss**: 23649.63
- **Risk**: 16.62 points
- **TP 1RR**: 23616.40 ✅
- **TP 2RR**: 23599.78 ❌
- **TP 3RR**: 23583.16 ❌
- **TP 4RR**: 23566.55 ❌
- **TP 15RR**: 23383.77 ❌
- **PnL**: -16.62 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 19.44 points

### Trade #1338 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 12:15:00
- **FVG 5m**: 23635.03 - 23637.81
- **Entrée**: 23633.01 @ 2025-07-24 13:43:00
- **Stop Loss**: 23649.63
- **Risk**: 16.62 points
- **TP 1RR**: 23616.40 ✅
- **TP 2RR**: 23599.78 ❌
- **TP 3RR**: 23583.16 ❌
- **TP 4RR**: 23566.55 ❌
- **TP 15RR**: 23383.77 ❌
- **PnL**: -16.62 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 19.44 points

### Trade #1339 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 12:15:00
- **FVG 5m**: 23635.03 - 23637.81
- **Entrée**: 23633.01 @ 2025-07-24 13:43:00
- **Stop Loss**: 23649.63
- **Risk**: 16.62 points
- **TP 1RR**: 23616.40 ✅
- **TP 2RR**: 23599.78 ❌
- **TP 3RR**: 23583.16 ❌
- **TP 4RR**: 23566.55 ❌
- **TP 15RR**: 23383.77 ❌
- **PnL**: -16.62 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 19.44 points

### Trade #1340 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-25 03:15:00
- **FVG 5m**: 23595.14 - 23601.20
- **Entrée**: 23601.45 @ 2025-07-25 03:29:00
- **Stop Loss**: 23583.34
- **Risk**: 18.11 points
- **TP 1RR**: 23619.56 ✅
- **TP 2RR**: 23637.67 ❌
- **TP 3RR**: 23655.78 ❌
- **TP 4RR**: 23673.89 ❌
- **TP 15RR**: 23873.10 ❌
- **PnL**: -18.11 points (-1.0R)
- **MFE**: 21.46 points
- **MAE**: 23.48 points

### Trade #1341 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-25 08:30:00
- **FVG 5m**: 23596.91 - 23604.48
- **Entrée**: 23608.27 @ 2025-07-25 08:47:00
- **Stop Loss**: 23585.11
- **Risk**: 23.16 points
- **TP 1RR**: 23631.43 ✅
- **TP 2RR**: 23654.59 ✅
- **TP 3RR**: 23677.75 ✅
- **TP 4RR**: 23700.91 ✅
- **TP 15RR**: 23955.67 ✅
- **PnL**: 347.40 points (15.0R)
- **MFE**: 371.14 points
- **MAE**: 20.45 points

### Trade #1342 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:15:00
- **FVG 5m**: 23659.52 - 23667.10
- **Entrée**: 23659.27 @ 2025-07-25 14:51:00
- **Stop Loss**: 23678.93
- **Risk**: 19.66 points
- **TP 1RR**: 23639.61 ✅
- **TP 2RR**: 23619.95 ❌
- **TP 3RR**: 23600.29 ❌
- **TP 4RR**: 23580.63 ❌
- **TP 15RR**: 23364.37 ❌
- **PnL**: -19.66 points (-1.0R)
- **MFE**: 20.45 points
- **MAE**: 19.69 points

### Trade #1343 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:45:00
- **FVG 5m**: 23745.62 - 23750.16
- **Entrée**: 23745.36 @ 2025-07-27 17:49:00
- **Stop Loss**: 23762.04
- **Risk**: 16.67 points
- **TP 1RR**: 23728.69 ❌
- **TP 2RR**: 23712.02 ❌
- **TP 3RR**: 23695.35 ❌
- **TP 4RR**: 23678.68 ❌
- **TP 15RR**: 23495.28 ❌
- **PnL**: -16.67 points (-1.0R)
- **MFE**: 4.54 points
- **MAE**: 18.68 points

### Trade #1344 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:45:00
- **FVG 5m**: 23745.62 - 23750.16
- **Entrée**: 23745.36 @ 2025-07-27 17:49:00
- **Stop Loss**: 23762.04
- **Risk**: 16.67 points
- **TP 1RR**: 23728.69 ❌
- **TP 2RR**: 23712.02 ❌
- **TP 3RR**: 23695.35 ❌
- **TP 4RR**: 23678.68 ❌
- **TP 15RR**: 23495.28 ❌
- **PnL**: -16.67 points (-1.0R)
- **MFE**: 4.54 points
- **MAE**: 18.68 points

### Trade #1345 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:45:00
- **FVG 5m**: 23745.62 - 23750.16
- **Entrée**: 23745.36 @ 2025-07-27 17:49:00
- **Stop Loss**: 23762.04
- **Risk**: 16.67 points
- **TP 1RR**: 23728.69 ❌
- **TP 2RR**: 23712.02 ❌
- **TP 3RR**: 23695.35 ❌
- **TP 4RR**: 23678.68 ❌
- **TP 15RR**: 23495.28 ❌
- **PnL**: -16.67 points (-1.0R)
- **MFE**: 4.54 points
- **MAE**: 18.68 points

### Trade #1346 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:45:00
- **FVG 5m**: 23745.62 - 23750.16
- **Entrée**: 23745.36 @ 2025-07-27 17:49:00
- **Stop Loss**: 23762.04
- **Risk**: 16.67 points
- **TP 1RR**: 23728.69 ❌
- **TP 2RR**: 23712.02 ❌
- **TP 3RR**: 23695.35 ❌
- **TP 4RR**: 23678.68 ❌
- **TP 15RR**: 23495.28 ❌
- **PnL**: -16.67 points (-1.0R)
- **MFE**: 4.54 points
- **MAE**: 18.68 points

### Trade #1347 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-25 15:00:00
- **FVG 5m**: 23657.25 - 23664.32
- **Entrée**: 23666.34 @ 2025-07-25 15:14:00
- **Stop Loss**: 23645.42
- **Risk**: 20.92 points
- **TP 1RR**: 23687.26 ✅
- **TP 2RR**: 23708.18 ✅
- **TP 3RR**: 23729.09 ✅
- **TP 4RR**: 23750.01 ✅
- **TP 15RR**: 23980.11 ❌
- **PnL**: -20.92 points (-1.0R)
- **MFE**: 220.41 points
- **MAE**: 34.34 points

### Trade #1348 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-28 08:30:00
- **FVG 5m**: 23702.95 - 23709.77
- **Entrée**: 23713.05 @ 2025-07-28 10:29:00
- **Stop Loss**: 23691.10
- **Risk**: 21.95 points
- **TP 1RR**: 23735.00 ✅
- **TP 2RR**: 23756.95 ❌
- **TP 3RR**: 23778.90 ❌
- **TP 4RR**: 23800.85 ❌
- **TP 15RR**: 24042.31 ❌
- **PnL**: -21.95 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 25.75 points

### Trade #1349 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-28 10:15:00
- **FVG 5m**: 23702.95 - 23709.77
- **Entrée**: 23713.05 @ 2025-07-28 10:29:00
- **Stop Loss**: 23691.10
- **Risk**: 21.95 points
- **TP 1RR**: 23735.00 ✅
- **TP 2RR**: 23756.95 ❌
- **TP 3RR**: 23778.90 ❌
- **TP 4RR**: 23800.85 ❌
- **TP 15RR**: 24042.31 ❌
- **PnL**: -21.95 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 25.75 points

### Trade #1350 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23794.37
- **Risk**: 30.07 points
- **TP 1RR**: 23734.23 ✅
- **TP 2RR**: 23704.16 ✅
- **TP 3RR**: 23674.09 ✅
- **TP 4RR**: 23644.02 ❌
- **TP 15RR**: 23313.26 ❌
- **PnL**: -30.07 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 40.65 points

### Trade #1351 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23794.37
- **Risk**: 30.07 points
- **TP 1RR**: 23734.23 ✅
- **TP 2RR**: 23704.16 ✅
- **TP 3RR**: 23674.09 ✅
- **TP 4RR**: 23644.02 ❌
- **TP 15RR**: 23313.26 ❌
- **PnL**: -30.07 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 40.65 points

### Trade #1352 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23794.37
- **Risk**: 30.07 points
- **TP 1RR**: 23734.23 ✅
- **TP 2RR**: 23704.16 ✅
- **TP 3RR**: 23674.09 ✅
- **TP 4RR**: 23644.02 ❌
- **TP 15RR**: 23313.26 ❌
- **PnL**: -30.07 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 40.65 points

### Trade #1353 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23794.37
- **Risk**: 30.07 points
- **TP 1RR**: 23734.23 ✅
- **TP 2RR**: 23704.16 ✅
- **TP 3RR**: 23674.09 ✅
- **TP 4RR**: 23644.02 ❌
- **TP 15RR**: 23313.26 ❌
- **PnL**: -30.07 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 40.65 points

### Trade #1354 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:15:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23794.37
- **Risk**: 30.07 points
- **TP 1RR**: 23734.23 ✅
- **TP 2RR**: 23704.16 ✅
- **TP 3RR**: 23674.09 ✅
- **TP 4RR**: 23644.02 ❌
- **TP 15RR**: 23313.26 ❌
- **PnL**: -30.07 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 40.65 points

### Trade #1355 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:30:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23794.37
- **Risk**: 30.07 points
- **TP 1RR**: 23734.23 ✅
- **TP 2RR**: 23704.16 ✅
- **TP 3RR**: 23674.09 ✅
- **TP 4RR**: 23644.02 ❌
- **TP 15RR**: 23313.26 ❌
- **PnL**: -30.07 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 40.65 points

### Trade #1356 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:30:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23794.37
- **Risk**: 30.07 points
- **TP 1RR**: 23734.23 ✅
- **TP 2RR**: 23704.16 ✅
- **TP 3RR**: 23674.09 ✅
- **TP 4RR**: 23644.02 ❌
- **TP 15RR**: 23313.26 ❌
- **PnL**: -30.07 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 40.65 points

### Trade #1357 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 10:15:00
- **FVG 5m**: 23724.16 - 23734.00
- **Entrée**: 23723.40 @ 2025-07-29 12:38:00
- **Stop Loss**: 23745.87
- **Risk**: 22.47 points
- **TP 1RR**: 23700.93 ✅
- **TP 2RR**: 23678.46 ✅
- **TP 3RR**: 23655.99 ✅
- **TP 4RR**: 23633.52 ❌
- **TP 15RR**: 23386.33 ❌
- **PnL**: -22.47 points (-1.0R)
- **MFE**: 70.19 points
- **MAE**: 26.01 points

### Trade #1358 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 10:30:00
- **FVG 5m**: 23724.16 - 23734.00
- **Entrée**: 23723.40 @ 2025-07-29 12:38:00
- **Stop Loss**: 23745.87
- **Risk**: 22.47 points
- **TP 1RR**: 23700.93 ✅
- **TP 2RR**: 23678.46 ✅
- **TP 3RR**: 23655.99 ✅
- **TP 4RR**: 23633.52 ❌
- **TP 15RR**: 23386.33 ❌
- **PnL**: -22.47 points (-1.0R)
- **MFE**: 70.19 points
- **MAE**: 26.01 points

### Trade #1359 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 12:15:00
- **FVG 5m**: 23724.16 - 23734.00
- **Entrée**: 23723.40 @ 2025-07-29 12:38:00
- **Stop Loss**: 23745.87
- **Risk**: 22.47 points
- **TP 1RR**: 23700.93 ✅
- **TP 2RR**: 23678.46 ✅
- **TP 3RR**: 23655.99 ✅
- **TP 4RR**: 23633.52 ❌
- **TP 15RR**: 23386.33 ❌
- **PnL**: -22.47 points (-1.0R)
- **MFE**: 70.19 points
- **MAE**: 26.01 points

### Trade #1360 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-29 14:30:00
- **FVG 5m**: 23685.78 - 23691.59
- **Entrée**: 23693.35 @ 2025-07-29 17:02:00
- **Stop Loss**: 23673.94
- **Risk**: 19.42 points
- **TP 1RR**: 23712.77 ✅
- **TP 2RR**: 23732.19 ✅
- **TP 3RR**: 23751.61 ✅
- **TP 4RR**: 23771.02 ✅
- **TP 15RR**: 23984.61 ❌
- **PnL**: -19.42 points (-1.0R)
- **MFE**: 129.77 points
- **MAE**: 24.74 points

### Trade #1361 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-29 14:30:00
- **FVG 5m**: 23685.78 - 23691.59
- **Entrée**: 23693.35 @ 2025-07-29 17:02:00
- **Stop Loss**: 23673.94
- **Risk**: 19.42 points
- **TP 1RR**: 23712.77 ✅
- **TP 2RR**: 23732.19 ✅
- **TP 3RR**: 23751.61 ✅
- **TP 4RR**: 23771.02 ✅
- **TP 15RR**: 23984.61 ❌
- **PnL**: -19.42 points (-1.0R)
- **MFE**: 129.77 points
- **MAE**: 24.74 points

### Trade #1362 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-29 14:30:00
- **FVG 5m**: 23685.78 - 23691.59
- **Entrée**: 23693.35 @ 2025-07-29 17:02:00
- **Stop Loss**: 23673.94
- **Risk**: 19.42 points
- **TP 1RR**: 23712.77 ✅
- **TP 2RR**: 23732.19 ✅
- **TP 3RR**: 23751.61 ✅
- **TP 4RR**: 23771.02 ✅
- **TP 15RR**: 23984.61 ❌
- **PnL**: -19.42 points (-1.0R)
- **MFE**: 129.77 points
- **MAE**: 24.74 points

### Trade #1363 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 02:15:00
- **FVG 5m**: 23718.60 - 23724.41
- **Entrée**: 23724.91 @ 2025-07-30 02:29:00
- **Stop Loss**: 23706.74
- **Risk**: 18.17 points
- **TP 1RR**: 23743.09 ✅
- **TP 2RR**: 23761.26 ❌
- **TP 3RR**: 23779.43 ❌
- **TP 4RR**: 23797.60 ❌
- **TP 15RR**: 23997.48 ❌
- **PnL**: -18.17 points (-1.0R)
- **MFE**: 20.45 points
- **MAE**: 30.30 points

### Trade #1364 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 08:30:00
- **FVG 5m**: 23725.67 - 23728.70
- **Entrée**: 23733.75 @ 2025-07-30 10:41:00
- **Stop Loss**: 23713.81
- **Risk**: 19.94 points
- **TP 1RR**: 23753.69 ✅
- **TP 2RR**: 23773.63 ✅
- **TP 3RR**: 23793.58 ✅
- **TP 4RR**: 23813.52 ✅
- **TP 15RR**: 24032.88 ❌
- **PnL**: -19.94 points (-1.0R)
- **MFE**: 89.38 points
- **MAE**: 20.20 points

### Trade #1365 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 08:45:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23717.09 @ 2025-07-30 10:11:00
- **Stop Loss**: 23746.38
- **Risk**: 29.29 points
- **TP 1RR**: 23687.80 ❌
- **TP 2RR**: 23658.51 ❌
- **TP 3RR**: 23629.22 ❌
- **TP 4RR**: 23599.93 ❌
- **TP 15RR**: 23277.77 ❌
- **PnL**: -29.29 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 34.84 points

### Trade #1366 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 08:45:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23717.09 @ 2025-07-30 10:11:00
- **Stop Loss**: 23746.38
- **Risk**: 29.29 points
- **TP 1RR**: 23687.80 ❌
- **TP 2RR**: 23658.51 ❌
- **TP 3RR**: 23629.22 ❌
- **TP 4RR**: 23599.93 ❌
- **TP 15RR**: 23277.77 ❌
- **PnL**: -29.29 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 34.84 points

### Trade #1367 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 09:30:00
- **FVG 5m**: 23725.67 - 23728.70
- **Entrée**: 23733.75 @ 2025-07-30 10:41:00
- **Stop Loss**: 23713.81
- **Risk**: 19.94 points
- **TP 1RR**: 23753.69 ✅
- **TP 2RR**: 23773.63 ✅
- **TP 3RR**: 23793.58 ✅
- **TP 4RR**: 23813.52 ✅
- **TP 15RR**: 24032.88 ❌
- **PnL**: -19.94 points (-1.0R)
- **MFE**: 89.38 points
- **MAE**: 20.20 points

### Trade #1368 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 09:45:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23717.09 @ 2025-07-30 10:11:00
- **Stop Loss**: 23746.38
- **Risk**: 29.29 points
- **TP 1RR**: 23687.80 ❌
- **TP 2RR**: 23658.51 ❌
- **TP 3RR**: 23629.22 ❌
- **TP 4RR**: 23599.93 ❌
- **TP 15RR**: 23277.77 ❌
- **PnL**: -29.29 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 34.84 points

### Trade #1369 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 09:45:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23717.09 @ 2025-07-30 10:11:00
- **Stop Loss**: 23746.38
- **Risk**: 29.29 points
- **TP 1RR**: 23687.80 ❌
- **TP 2RR**: 23658.51 ❌
- **TP 3RR**: 23629.22 ❌
- **TP 4RR**: 23599.93 ❌
- **TP 15RR**: 23277.77 ❌
- **PnL**: -29.29 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 34.84 points

### Trade #1370 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 10:45:00
- **FVG 5m**: 23746.37 - 23749.66
- **Entrée**: 23754.45 @ 2025-07-30 11:03:00
- **Stop Loss**: 23734.50
- **Risk**: 19.95 points
- **TP 1RR**: 23774.41 ✅
- **TP 2RR**: 23794.36 ✅
- **TP 3RR**: 23814.31 ✅
- **TP 4RR**: 23834.26 ❌
- **TP 15RR**: 24053.74 ❌
- **PnL**: -19.95 points (-1.0R)
- **MFE**: 68.67 points
- **MAE**: 40.90 points

### Trade #1371 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 12:30:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23686.81
- **Risk**: 17.40 points
- **TP 1RR**: 23721.61 ✅
- **TP 2RR**: 23739.02 ✅
- **TP 3RR**: 23756.42 ✅
- **TP 4RR**: 23773.83 ✅
- **TP 15RR**: 23965.27 ✅
- **PnL**: 261.06 points (15.0R)
- **MFE**: 275.20 points
- **MAE**: 2.52 points

### Trade #1372 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:00:00
- **FVG 5m**: 23731.48 - 23745.36
- **Entrée**: 23716.58 @ 2025-07-30 13:54:00
- **Stop Loss**: 23757.24
- **Risk**: 40.65 points
- **TP 1RR**: 23675.93 ✅
- **TP 2RR**: 23635.27 ✅
- **TP 3RR**: 23594.62 ✅
- **TP 4RR**: 23553.96 ❌
- **TP 15RR**: 23106.76 ❌
- **PnL**: -40.65 points (-1.0R)
- **MFE**: 128.76 points
- **MAE**: 132.55 points

### Trade #1373 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:45:00
- **FVG 5m**: 23655.99 - 23711.28
- **Entrée**: 23644.63 @ 2025-07-30 13:59:00
- **Stop Loss**: 23723.14
- **Risk**: 78.51 points
- **TP 1RR**: 23566.12 ❌
- **TP 2RR**: 23487.61 ❌
- **TP 3RR**: 23409.10 ❌
- **TP 4RR**: 23330.59 ❌
- **TP 15RR**: 22466.99 ❌
- **PnL**: -78.51 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 84.58 points

### Trade #1374 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:45:00
- **FVG 5m**: 23655.99 - 23711.28
- **Entrée**: 23644.63 @ 2025-07-30 13:59:00
- **Stop Loss**: 23723.14
- **Risk**: 78.51 points
- **TP 1RR**: 23566.12 ❌
- **TP 2RR**: 23487.61 ❌
- **TP 3RR**: 23409.10 ❌
- **TP 4RR**: 23330.59 ❌
- **TP 15RR**: 22466.99 ❌
- **PnL**: -78.51 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 84.58 points

### Trade #1375 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:45:00
- **FVG 5m**: 23655.99 - 23711.28
- **Entrée**: 23644.63 @ 2025-07-30 13:59:00
- **Stop Loss**: 23723.14
- **Risk**: 78.51 points
- **TP 1RR**: 23566.12 ❌
- **TP 2RR**: 23487.61 ❌
- **TP 3RR**: 23409.10 ❌
- **TP 4RR**: 23330.59 ❌
- **TP 15RR**: 22466.99 ❌
- **PnL**: -78.51 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 84.58 points

### Trade #1376 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:00:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23686.81
- **Risk**: 17.40 points
- **TP 1RR**: 23721.61 ✅
- **TP 2RR**: 23739.02 ✅
- **TP 3RR**: 23756.42 ✅
- **TP 4RR**: 23773.83 ✅
- **TP 15RR**: 23965.27 ✅
- **PnL**: 261.06 points (15.0R)
- **MFE**: 275.20 points
- **MAE**: 2.52 points

### Trade #1377 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:00:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23686.81
- **Risk**: 17.40 points
- **TP 1RR**: 23721.61 ✅
- **TP 2RR**: 23739.02 ✅
- **TP 3RR**: 23756.42 ✅
- **TP 4RR**: 23773.83 ✅
- **TP 15RR**: 23965.27 ✅
- **PnL**: 261.06 points (15.0R)
- **MFE**: 275.20 points
- **MAE**: 2.52 points

### Trade #1378 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:00:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23686.81
- **Risk**: 17.40 points
- **TP 1RR**: 23721.61 ✅
- **TP 2RR**: 23739.02 ✅
- **TP 3RR**: 23756.42 ✅
- **TP 4RR**: 23773.83 ✅
- **TP 15RR**: 23965.27 ✅
- **PnL**: 261.06 points (15.0R)
- **MFE**: 275.20 points
- **MAE**: 2.52 points

### Trade #1379 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:00:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23686.81
- **Risk**: 17.40 points
- **TP 1RR**: 23721.61 ✅
- **TP 2RR**: 23739.02 ✅
- **TP 3RR**: 23756.42 ✅
- **TP 4RR**: 23773.83 ✅
- **TP 15RR**: 23965.27 ✅
- **PnL**: 261.06 points (15.0R)
- **MFE**: 275.20 points
- **MAE**: 2.52 points

### Trade #1380 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:45:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23686.81
- **Risk**: 17.40 points
- **TP 1RR**: 23721.61 ✅
- **TP 2RR**: 23739.02 ✅
- **TP 3RR**: 23756.42 ✅
- **TP 4RR**: 23773.83 ✅
- **TP 15RR**: 23965.27 ✅
- **PnL**: 261.06 points (15.0R)
- **MFE**: 275.20 points
- **MAE**: 2.52 points

### Trade #1381 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:45:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23686.81
- **Risk**: 17.40 points
- **TP 1RR**: 23721.61 ✅
- **TP 2RR**: 23739.02 ✅
- **TP 3RR**: 23756.42 ✅
- **TP 4RR**: 23773.83 ✅
- **TP 15RR**: 23965.27 ✅
- **PnL**: 261.06 points (15.0R)
- **MFE**: 275.20 points
- **MAE**: 2.52 points

### Trade #1382 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 03:00:00
- **FVG 5m**: 24026.88 - 24033.19
- **Entrée**: 24026.37 @ 2025-07-31 04:32:00
- **Stop Loss**: 24045.20
- **Risk**: 18.83 points
- **TP 1RR**: 24007.54 ✅
- **TP 2RR**: 23988.70 ✅
- **TP 3RR**: 23969.87 ❌
- **TP 4RR**: 23951.04 ❌
- **TP 15RR**: 23743.87 ❌
- **PnL**: -18.83 points (-1.0R)
- **MFE**: 38.38 points
- **MAE**: 21.46 points

### Trade #1383 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 07:00:00
- **FVG 5m**: 24012.48 - 24017.28
- **Entrée**: 24022.58 @ 2025-07-31 07:17:00
- **Stop Loss**: 24000.48
- **Risk**: 22.11 points
- **TP 1RR**: 24044.69 ✅
- **TP 2RR**: 24066.79 ❌
- **TP 3RR**: 24088.90 ❌
- **TP 4RR**: 24111.00 ❌
- **TP 15RR**: 24354.16 ❌
- **PnL**: -22.11 points (-1.0R)
- **MFE**: 25.25 points
- **MAE**: 29.79 points

### Trade #1384 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 08:30:00
- **FVG 5m**: 23889.02 - 23894.33
- **Entrée**: 23883.72 @ 2025-07-31 09:21:00
- **Stop Loss**: 23906.27
- **Risk**: 22.55 points
- **TP 1RR**: 23861.17 ✅
- **TP 2RR**: 23838.62 ✅
- **TP 3RR**: 23816.07 ✅
- **TP 4RR**: 23793.52 ✅
- **TP 15RR**: 23545.45 ✅
- **PnL**: 338.27 points (15.0R)
- **MFE**: 347.41 points
- **MAE**: 7.32 points

### Trade #1385 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 09:45:00
- **FVG 5m**: 23747.13 - 23773.64
- **Entrée**: 23745.36 @ 2025-07-31 10:13:00
- **Stop Loss**: 23785.53
- **Risk**: 40.16 points
- **TP 1RR**: 23705.20 ❌
- **TP 2RR**: 23665.04 ❌
- **TP 3RR**: 23624.87 ❌
- **TP 4RR**: 23584.71 ❌
- **TP 15RR**: 23142.90 ❌
- **PnL**: -40.16 points (-1.0R)
- **MFE**: 29.54 points
- **MAE**: 46.20 points

### Trade #1386 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 13:00:00
- **FVG 5m**: 23649.42 - 23652.71
- **Entrée**: 23642.61 @ 2025-07-31 14:12:00
- **Stop Loss**: 23664.53
- **Risk**: 21.93 points
- **TP 1RR**: 23620.68 ✅
- **TP 2RR**: 23598.76 ✅
- **TP 3RR**: 23576.83 ✅
- **TP 4RR**: 23554.91 ✅
- **TP 15RR**: 23313.73 ❌
- **PnL**: -21.93 points (-1.0R)
- **MFE**: 111.85 points
- **MAE**: 48.48 points

### Trade #1387 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 13:15:00
- **FVG 5m**: 23626.45 - 23646.14
- **Entrée**: 23647.40 @ 2025-07-31 13:28:00
- **Stop Loss**: 23614.64
- **Risk**: 32.77 points
- **TP 1RR**: 23680.17 ✅
- **TP 2RR**: 23712.94 ❌
- **TP 3RR**: 23745.71 ❌
- **TP 4RR**: 23778.48 ❌
- **TP 15RR**: 24138.93 ❌
- **PnL**: -32.77 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 33.58 points

### Trade #1388 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 13:15:00
- **FVG 5m**: 23626.45 - 23646.14
- **Entrée**: 23647.40 @ 2025-07-31 13:28:00
- **Stop Loss**: 23614.64
- **Risk**: 32.77 points
- **TP 1RR**: 23680.17 ✅
- **TP 2RR**: 23712.94 ❌
- **TP 3RR**: 23745.71 ❌
- **TP 4RR**: 23778.48 ❌
- **TP 15RR**: 24138.93 ❌
- **PnL**: -32.77 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 33.58 points

### Trade #1389 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 13:15:00
- **FVG 5m**: 23626.45 - 23646.14
- **Entrée**: 23647.40 @ 2025-07-31 13:28:00
- **Stop Loss**: 23614.64
- **Risk**: 32.77 points
- **TP 1RR**: 23680.17 ✅
- **TP 2RR**: 23712.94 ❌
- **TP 3RR**: 23745.71 ❌
- **TP 4RR**: 23778.48 ❌
- **TP 15RR**: 24138.93 ❌
- **PnL**: -32.77 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 33.58 points

### Trade #1390 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 15:15:00
- **FVG 5m**: 23555.76 - 23563.58
- **Entrée**: 23581.00 @ 2025-07-31 15:31:00
- **Stop Loss**: 23543.98
- **Risk**: 37.03 points
- **TP 1RR**: 23618.03 ❌
- **TP 2RR**: 23655.05 ❌
- **TP 3RR**: 23692.08 ❌
- **TP 4RR**: 23729.10 ❌
- **TP 15RR**: 24136.38 ❌
- **PnL**: -37.03 points (-1.0R)
- **MFE**: 8.33 points
- **MAE**: 50.24 points

### Trade #1391 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 17:30:00
- **FVG 5m**: 23501.73 - 23505.51
- **Entrée**: 23498.70 @ 2025-07-31 19:21:00
- **Stop Loss**: 23517.27
- **Risk**: 18.57 points
- **TP 1RR**: 23480.13 ✅
- **TP 2RR**: 23461.56 ❌
- **TP 3RR**: 23442.99 ❌
- **TP 4RR**: 23424.42 ❌
- **TP 15RR**: 23220.15 ❌
- **PnL**: -18.57 points (-1.0R)
- **MFE**: 37.11 points
- **MAE**: 19.19 points

### Trade #1392 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 17:30:00
- **FVG 5m**: 23501.73 - 23505.51
- **Entrée**: 23498.70 @ 2025-07-31 19:21:00
- **Stop Loss**: 23517.27
- **Risk**: 18.57 points
- **TP 1RR**: 23480.13 ✅
- **TP 2RR**: 23461.56 ❌
- **TP 3RR**: 23442.99 ❌
- **TP 4RR**: 23424.42 ❌
- **TP 15RR**: 23220.15 ❌
- **PnL**: -18.57 points (-1.0R)
- **MFE**: 37.11 points
- **MAE**: 19.19 points

### Trade #1393 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 18:00:00
- **FVG 5m**: 23519.40 - 23527.73
- **Entrée**: 23528.99 @ 2025-07-31 20:14:00
- **Stop Loss**: 23507.64
- **Risk**: 21.35 points
- **TP 1RR**: 23550.35 ✅
- **TP 2RR**: 23571.70 ✅
- **TP 3RR**: 23593.05 ❌
- **TP 4RR**: 23614.41 ❌
- **TP 15RR**: 23849.30 ❌
- **PnL**: -21.35 points (-1.0R)
- **MFE**: 44.69 points
- **MAE**: 23.73 points

### Trade #1394 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 02:30:00
- **FVG 5m**: 23323.22 - 23331.81
- **Entrée**: 23340.65 @ 2025-08-01 03:47:00
- **Stop Loss**: 23311.56
- **Risk**: 29.08 points
- **TP 1RR**: 23369.73 ❌
- **TP 2RR**: 23398.81 ❌
- **TP 3RR**: 23427.89 ❌
- **TP 4RR**: 23456.98 ❌
- **TP 15RR**: 23776.88 ❌
- **PnL**: -29.08 points (-1.0R)
- **MFE**: 28.78 points
- **MAE**: 29.29 points

### Trade #1395 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 02:45:00
- **FVG 5m**: 23323.22 - 23331.81
- **Entrée**: 23340.65 @ 2025-08-01 03:47:00
- **Stop Loss**: 23311.56
- **Risk**: 29.08 points
- **TP 1RR**: 23369.73 ❌
- **TP 2RR**: 23398.81 ❌
- **TP 3RR**: 23427.89 ❌
- **TP 4RR**: 23456.98 ❌
- **TP 15RR**: 23776.88 ❌
- **PnL**: -29.08 points (-1.0R)
- **MFE**: 28.78 points
- **MAE**: 29.29 points

### Trade #1396 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-01 03:15:00
- **FVG 5m**: 23331.81 - 23356.80
- **Entrée**: 23316.66 @ 2025-08-01 03:27:00
- **Stop Loss**: 23368.48
- **Risk**: 51.82 points
- **TP 1RR**: 23264.84 ❌
- **TP 2RR**: 23213.02 ❌
- **TP 3RR**: 23161.19 ❌
- **TP 4RR**: 23109.37 ❌
- **TP 15RR**: 22539.33 ❌
- **PnL**: -51.82 points (-1.0R)
- **MFE**: 25.75 points
- **MAE**: 52.77 points

### Trade #1397 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-01 03:15:00
- **FVG 5m**: 23331.81 - 23356.80
- **Entrée**: 23316.66 @ 2025-08-01 03:27:00
- **Stop Loss**: 23368.48
- **Risk**: 51.82 points
- **TP 1RR**: 23264.84 ❌
- **TP 2RR**: 23213.02 ❌
- **TP 3RR**: 23161.19 ❌
- **TP 4RR**: 23109.37 ❌
- **TP 15RR**: 22539.33 ❌
- **PnL**: -51.82 points (-1.0R)
- **MFE**: 25.75 points
- **MAE**: 52.77 points

### Trade #1398 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 03:45:00
- **FVG 5m**: 23285.35 - 23289.90
- **Entrée**: 23293.43 @ 2025-08-01 06:01:00
- **Stop Loss**: 23273.71
- **Risk**: 19.72 points
- **TP 1RR**: 23313.15 ✅
- **TP 2RR**: 23332.88 ✅
- **TP 3RR**: 23352.60 ✅
- **TP 4RR**: 23372.32 ✅
- **TP 15RR**: 23589.26 ❌
- **PnL**: -19.72 points (-1.0R)
- **MFE**: 103.52 points
- **MAE**: 27.52 points

### Trade #1399 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 06:00:00
- **FVG 5m**: 23307.07 - 23323.73
- **Entrée**: 23324.23 @ 2025-08-01 06:13:00
- **Stop Loss**: 23295.41
- **Risk**: 28.82 points
- **TP 1RR**: 23353.06 ✅
- **TP 2RR**: 23381.88 ❌
- **TP 3RR**: 23410.70 ❌
- **TP 4RR**: 23439.52 ❌
- **TP 15RR**: 23756.56 ❌
- **PnL**: -28.82 points (-1.0R)
- **MFE**: 47.21 points
- **MAE**: 31.31 points

### Trade #1400 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 06:00:00
- **FVG 5m**: 23307.07 - 23323.73
- **Entrée**: 23324.23 @ 2025-08-01 06:13:00
- **Stop Loss**: 23295.41
- **Risk**: 28.82 points
- **TP 1RR**: 23353.06 ✅
- **TP 2RR**: 23381.88 ❌
- **TP 3RR**: 23410.70 ❌
- **TP 4RR**: 23439.52 ❌
- **TP 15RR**: 23756.56 ❌
- **PnL**: -28.82 points (-1.0R)
- **MFE**: 47.21 points
- **MAE**: 31.31 points

### Trade #1401 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 08:15:00
- **FVG 5m**: 23106.60 - 23114.17
- **Entrée**: 23117.46 @ 2025-08-01 09:09:00
- **Stop Loss**: 23095.05
- **Risk**: 22.41 points
- **TP 1RR**: 23139.87 ✅
- **TP 2RR**: 23162.28 ✅
- **TP 3RR**: 23184.69 ✅
- **TP 4RR**: 23207.10 ✅
- **TP 15RR**: 23453.60 ❌
- **PnL**: -22.41 points (-1.0R)
- **MFE**: 156.28 points
- **MAE**: 27.52 points

### Trade #1402 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 09:00:00
- **FVG 5m**: 23127.81 - 23132.35
- **Entrée**: 23145.73 @ 2025-08-01 09:12:00
- **Stop Loss**: 23116.24
- **Risk**: 29.49 points
- **TP 1RR**: 23175.22 ✅
- **TP 2RR**: 23204.71 ✅
- **TP 3RR**: 23234.20 ✅
- **TP 4RR**: 23263.69 ✅
- **TP 15RR**: 23588.08 ❌
- **PnL**: -29.49 points (-1.0R)
- **MFE**: 128.01 points
- **MAE**: 32.32 points

### Trade #1403 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 09:00:00
- **FVG 5m**: 23127.81 - 23132.35
- **Entrée**: 23145.73 @ 2025-08-01 09:12:00
- **Stop Loss**: 23116.24
- **Risk**: 29.49 points
- **TP 1RR**: 23175.22 ✅
- **TP 2RR**: 23204.71 ✅
- **TP 3RR**: 23234.20 ✅
- **TP 4RR**: 23263.69 ✅
- **TP 15RR**: 23588.08 ❌
- **PnL**: -29.49 points (-1.0R)
- **MFE**: 128.01 points
- **MAE**: 32.32 points

### Trade #1404 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 11:00:00
- **FVG 5m**: 23065.19 - 23080.09
- **Entrée**: 23086.40 @ 2025-08-01 13:24:00
- **Stop Loss**: 23053.66
- **Risk**: 32.74 points
- **TP 1RR**: 23119.14 ✅
- **TP 2RR**: 23151.88 ✅
- **TP 3RR**: 23184.62 ❌
- **TP 4RR**: 23217.36 ❌
- **TP 15RR**: 23577.51 ❌
- **PnL**: -32.74 points (-1.0R)
- **MFE**: 85.34 points
- **MAE**: 38.63 points

### Trade #1405 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 11:00:00
- **FVG 5m**: 23065.19 - 23080.09
- **Entrée**: 23086.40 @ 2025-08-01 13:24:00
- **Stop Loss**: 23053.66
- **Risk**: 32.74 points
- **TP 1RR**: 23119.14 ✅
- **TP 2RR**: 23151.88 ✅
- **TP 3RR**: 23184.62 ❌
- **TP 4RR**: 23217.36 ❌
- **TP 15RR**: 23577.51 ❌
- **PnL**: -32.74 points (-1.0R)
- **MFE**: 85.34 points
- **MAE**: 38.63 points

### Trade #1406 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 13:00:00
- **FVG 5m**: 23065.19 - 23080.09
- **Entrée**: 23086.40 @ 2025-08-01 13:24:00
- **Stop Loss**: 23053.66
- **Risk**: 32.74 points
- **TP 1RR**: 23119.14 ✅
- **TP 2RR**: 23151.88 ✅
- **TP 3RR**: 23184.62 ❌
- **TP 4RR**: 23217.36 ❌
- **TP 15RR**: 23577.51 ❌
- **PnL**: -32.74 points (-1.0R)
- **MFE**: 85.34 points
- **MAE**: 38.63 points

### Trade #1407 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 13:00:00
- **FVG 5m**: 23065.19 - 23080.09
- **Entrée**: 23086.40 @ 2025-08-01 13:24:00
- **Stop Loss**: 23053.66
- **Risk**: 32.74 points
- **TP 1RR**: 23119.14 ✅
- **TP 2RR**: 23151.88 ✅
- **TP 3RR**: 23184.62 ❌
- **TP 4RR**: 23217.36 ❌
- **TP 15RR**: 23577.51 ❌
- **PnL**: -32.74 points (-1.0R)
- **MFE**: 85.34 points
- **MAE**: 38.63 points

### Trade #1408 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 13:00:00
- **FVG 5m**: 23065.19 - 23080.09
- **Entrée**: 23086.40 @ 2025-08-01 13:24:00
- **Stop Loss**: 23053.66
- **Risk**: 32.74 points
- **TP 1RR**: 23119.14 ✅
- **TP 2RR**: 23151.88 ✅
- **TP 3RR**: 23184.62 ❌
- **TP 4RR**: 23217.36 ❌
- **TP 15RR**: 23577.51 ❌
- **PnL**: -32.74 points (-1.0R)
- **MFE**: 85.34 points
- **MAE**: 38.63 points

### Trade #1409 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 02:30:00
- **FVG 5m**: 23265.91 - 23270.46
- **Entrée**: 23270.71 @ 2025-08-04 03:14:00
- **Stop Loss**: 23254.28
- **Risk**: 16.43 points
- **TP 1RR**: 23287.14 ✅
- **TP 2RR**: 23303.57 ✅
- **TP 3RR**: 23320.00 ✅
- **TP 4RR**: 23336.43 ✅
- **TP 15RR**: 23517.16 ✅
- **PnL**: 246.45 points (15.0R)
- **MFE**: 263.08 points
- **MAE**: 11.36 points

### Trade #1410 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 03:00:00
- **FVG 5m**: 23265.91 - 23270.46
- **Entrée**: 23270.71 @ 2025-08-04 03:14:00
- **Stop Loss**: 23254.28
- **Risk**: 16.43 points
- **TP 1RR**: 23287.14 ✅
- **TP 2RR**: 23303.57 ✅
- **TP 3RR**: 23320.00 ✅
- **TP 4RR**: 23336.43 ✅
- **TP 15RR**: 23517.16 ✅
- **PnL**: 246.45 points (15.0R)
- **MFE**: 263.08 points
- **MAE**: 11.36 points

### Trade #1411 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 08:45:00
- **FVG 5m**: 23457.04 - 23469.66
- **Entrée**: 23474.96 @ 2025-08-04 08:58:00
- **Stop Loss**: 23445.31
- **Risk**: 29.65 points
- **TP 1RR**: 23504.62 ❌
- **TP 2RR**: 23534.27 ❌
- **TP 3RR**: 23563.93 ❌
- **TP 4RR**: 23593.58 ❌
- **TP 15RR**: 23919.78 ❌
- **PnL**: -29.65 points (-1.0R)
- **MFE**: 19.69 points
- **MAE**: 31.05 points

### Trade #1412 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 08:45:00
- **FVG 5m**: 23457.04 - 23469.66
- **Entrée**: 23474.96 @ 2025-08-04 08:58:00
- **Stop Loss**: 23445.31
- **Risk**: 29.65 points
- **TP 1RR**: 23504.62 ❌
- **TP 2RR**: 23534.27 ❌
- **TP 3RR**: 23563.93 ❌
- **TP 4RR**: 23593.58 ❌
- **TP 15RR**: 23919.78 ❌
- **PnL**: -29.65 points (-1.0R)
- **MFE**: 19.69 points
- **MAE**: 31.05 points

### Trade #1413 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-04 11:15:00
- **FVG 5m**: 23498.70 - 23501.47
- **Entrée**: 23496.93 @ 2025-08-04 12:41:00
- **Stop Loss**: 23513.22
- **Risk**: 16.30 points
- **TP 1RR**: 23480.63 ✅
- **TP 2RR**: 23464.34 ❌
- **TP 3RR**: 23448.04 ❌
- **TP 4RR**: 23431.75 ❌
- **TP 15RR**: 23252.50 ❌
- **PnL**: -16.30 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 17.42 points

### Trade #1414 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-04 14:15:00
- **FVG 5m**: 23499.20 - 23510.31
- **Entrée**: 23496.93 @ 2025-08-04 14:29:00
- **Stop Loss**: 23522.06
- **Risk**: 25.14 points
- **TP 1RR**: 23471.79 ❌
- **TP 2RR**: 23446.66 ❌
- **TP 3RR**: 23421.52 ❌
- **TP 4RR**: 23396.38 ❌
- **TP 15RR**: 23119.88 ❌
- **PnL**: -25.14 points (-1.0R)
- **MFE**: 13.38 points
- **MAE**: 30.04 points

### Trade #1415 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 14:45:00
- **FVG 5m**: 23539.60 - 23558.03
- **Entrée**: 23560.80 @ 2025-08-04 15:08:00
- **Stop Loss**: 23527.83
- **Risk**: 32.98 points
- **TP 1RR**: 23593.78 ✅
- **TP 2RR**: 23626.76 ✅
- **TP 3RR**: 23659.74 ❌
- **TP 4RR**: 23692.72 ❌
- **TP 15RR**: 24055.47 ❌
- **PnL**: -32.98 points (-1.0R)
- **MFE**: 75.24 points
- **MAE**: 34.08 points

### Trade #1416 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-04 17:00:00
- **FVG 5m**: 23560.05 - 23567.87
- **Entrée**: 23557.52 @ 2025-08-04 18:21:00
- **Stop Loss**: 23579.66
- **Risk**: 22.14 points
- **TP 1RR**: 23535.39 ❌
- **TP 2RR**: 23513.25 ❌
- **TP 3RR**: 23491.12 ❌
- **TP 4RR**: 23468.98 ❌
- **TP 15RR**: 23225.49 ❌
- **PnL**: -22.14 points (-1.0R)
- **MFE**: 12.88 points
- **MAE**: 27.01 points

### Trade #1417 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 03:15:00
- **FVG 5m**: 23568.13 - 23573.18
- **Entrée**: 23573.43 @ 2025-08-05 04:33:00
- **Stop Loss**: 23556.34
- **Risk**: 17.09 points
- **TP 1RR**: 23590.51 ✅
- **TP 2RR**: 23607.60 ✅
- **TP 3RR**: 23624.69 ✅
- **TP 4RR**: 23641.77 ❌
- **TP 15RR**: 23829.72 ❌
- **PnL**: -17.09 points (-1.0R)
- **MFE**: 62.61 points
- **MAE**: 37.62 points

### Trade #1418 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-05 06:15:00
- **FVG 5m**: 23609.53 - 23614.08
- **Entrée**: 23608.52 @ 2025-08-05 06:27:00
- **Stop Loss**: 23625.88
- **Risk**: 17.36 points
- **TP 1RR**: 23591.16 ❌
- **TP 2RR**: 23573.80 ❌
- **TP 3RR**: 23556.44 ❌
- **TP 4RR**: 23539.08 ❌
- **TP 15RR**: 23348.10 ❌
- **PnL**: -17.36 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 19.44 points

### Trade #1419 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 10:00:00
- **FVG 5m**: 23395.18 - 23402.50
- **Entrée**: 23405.28 @ 2025-08-05 11:04:00
- **Stop Loss**: 23383.48
- **Risk**: 21.80 points
- **TP 1RR**: 23427.08 ✅
- **TP 2RR**: 23448.87 ✅
- **TP 3RR**: 23470.67 ❌
- **TP 4RR**: 23492.47 ❌
- **TP 15RR**: 23732.23 ❌
- **PnL**: -21.80 points (-1.0R)
- **MFE**: 49.99 points
- **MAE**: 28.28 points

### Trade #1420 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-05 10:30:00
- **FVG 5m**: 23398.72 - 23419.92
- **Entrée**: 23391.65 @ 2025-08-05 11:41:00
- **Stop Loss**: 23431.63
- **Risk**: 39.99 points
- **TP 1RR**: 23351.66 ❌
- **TP 2RR**: 23311.67 ❌
- **TP 3RR**: 23271.68 ❌
- **TP 4RR**: 23231.70 ❌
- **TP 15RR**: 22791.84 ❌
- **PnL**: -39.99 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 42.42 points

### Trade #1421 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-05 17:00:00
- **FVG 5m**: 23306.56 - 23309.59
- **Entrée**: 23303.78 @ 2025-08-05 18:49:00
- **Stop Loss**: 23321.25
- **Risk**: 17.46 points
- **TP 1RR**: 23286.32 ✅
- **TP 2RR**: 23268.86 ❌
- **TP 3RR**: 23251.40 ❌
- **TP 4RR**: 23233.94 ❌
- **TP 15RR**: 23041.86 ❌
- **PnL**: -17.46 points (-1.0R)
- **MFE**: 25.75 points
- **MAE**: 19.69 points

### Trade #1422 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 20:30:00
- **FVG 5m**: 23350.74 - 23353.77
- **Entrée**: 23355.04 @ 2025-08-05 20:51:00
- **Stop Loss**: 23339.07
- **Risk**: 15.97 points
- **TP 1RR**: 23371.00 ✅
- **TP 2RR**: 23386.97 ✅
- **TP 3RR**: 23402.94 ✅
- **TP 4RR**: 23418.91 ✅
- **TP 15RR**: 23594.55 ❌
- **PnL**: -15.97 points (-1.0R)
- **MFE**: 102.00 points
- **MAE**: 17.42 points

### Trade #1423 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 20:30:00
- **FVG 5m**: 23350.74 - 23353.77
- **Entrée**: 23355.04 @ 2025-08-05 20:51:00
- **Stop Loss**: 23339.07
- **Risk**: 15.97 points
- **TP 1RR**: 23371.00 ✅
- **TP 2RR**: 23386.97 ✅
- **TP 3RR**: 23402.94 ✅
- **TP 4RR**: 23418.91 ✅
- **TP 15RR**: 23594.55 ❌
- **PnL**: -15.97 points (-1.0R)
- **MFE**: 102.00 points
- **MAE**: 17.42 points

### Trade #1424 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-06 03:30:00
- **FVG 5m**: 23403.01 - 23410.08
- **Entrée**: 23393.16 @ 2025-08-06 03:42:00
- **Stop Loss**: 23421.78
- **Risk**: 28.62 points
- **TP 1RR**: 23364.54 ✅
- **TP 2RR**: 23335.92 ❌
- **TP 3RR**: 23307.30 ❌
- **TP 4RR**: 23278.68 ❌
- **TP 15RR**: 22963.85 ❌
- **PnL**: -28.62 points (-1.0R)
- **MFE**: 57.06 points
- **MAE**: 33.33 points

### Trade #1425 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 06:00:00
- **FVG 5m**: 23385.59 - 23399.22
- **Entrée**: 23402.50 @ 2025-08-06 07:19:00
- **Stop Loss**: 23373.89
- **Risk**: 28.61 points
- **TP 1RR**: 23431.11 ✅
- **TP 2RR**: 23459.72 ✅
- **TP 3RR**: 23488.33 ✅
- **TP 4RR**: 23516.94 ✅
- **TP 15RR**: 23831.63 ✅
- **PnL**: 429.13 points (15.0R)
- **MFE**: 432.49 points
- **MAE**: 26.51 points

### Trade #1426 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-06 08:45:00
- **FVG 5m**: 23467.64 - 23490.36
- **Entrée**: 23463.60 @ 2025-08-06 09:13:00
- **Stop Loss**: 23502.11
- **Risk**: 38.51 points
- **TP 1RR**: 23425.09 ✅
- **TP 2RR**: 23386.59 ❌
- **TP 3RR**: 23348.08 ❌
- **TP 4RR**: 23309.57 ❌
- **TP 15RR**: 22885.99 ❌
- **PnL**: -38.51 points (-1.0R)
- **MFE**: 69.94 points
- **MAE**: 45.95 points

### Trade #1427 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-06 09:00:00
- **FVG 5m**: 23467.64 - 23490.36
- **Entrée**: 23463.60 @ 2025-08-06 09:13:00
- **Stop Loss**: 23502.11
- **Risk**: 38.51 points
- **TP 1RR**: 23425.09 ✅
- **TP 2RR**: 23386.59 ❌
- **TP 3RR**: 23348.08 ❌
- **TP 4RR**: 23309.57 ❌
- **TP 15RR**: 22885.99 ❌
- **PnL**: -38.51 points (-1.0R)
- **MFE**: 69.94 points
- **MAE**: 45.95 points

### Trade #1428 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 09:30:00
- **FVG 5m**: 23491.63 - 23495.41
- **Entrée**: 23499.96 @ 2025-08-06 09:57:00
- **Stop Loss**: 23479.88
- **Risk**: 20.08 points
- **TP 1RR**: 23520.04 ✅
- **TP 2RR**: 23540.11 ✅
- **TP 3RR**: 23560.19 ✅
- **TP 4RR**: 23580.27 ✅
- **TP 15RR**: 23801.12 ✅
- **PnL**: 301.16 points (15.0R)
- **MFE**: 307.52 points
- **MAE**: 11.61 points

### Trade #1429 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 09:30:00
- **FVG 5m**: 23491.63 - 23495.41
- **Entrée**: 23499.96 @ 2025-08-06 09:57:00
- **Stop Loss**: 23479.88
- **Risk**: 20.08 points
- **TP 1RR**: 23520.04 ✅
- **TP 2RR**: 23540.11 ✅
- **TP 3RR**: 23560.19 ✅
- **TP 4RR**: 23580.27 ✅
- **TP 15RR**: 23801.12 ✅
- **PnL**: 301.16 points (15.0R)
- **MFE**: 307.52 points
- **MAE**: 11.61 points

### Trade #1430 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 10:15:00
- **FVG 5m**: 23569.64 - 23576.46
- **Entrée**: 23576.96 @ 2025-08-06 10:46:00
- **Stop Loss**: 23557.86
- **Risk**: 19.11 points
- **TP 1RR**: 23596.07 ✅
- **TP 2RR**: 23615.18 ✅
- **TP 3RR**: 23634.28 ✅
- **TP 4RR**: 23653.39 ✅
- **TP 15RR**: 23863.56 ✅
- **PnL**: 286.60 points (15.0R)
- **MFE**: 296.15 points
- **MAE**: 7.07 points

### Trade #1431 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 10:15:00
- **FVG 5m**: 23569.64 - 23576.46
- **Entrée**: 23576.96 @ 2025-08-06 10:46:00
- **Stop Loss**: 23557.86
- **Risk**: 19.11 points
- **TP 1RR**: 23596.07 ✅
- **TP 2RR**: 23615.18 ✅
- **TP 3RR**: 23634.28 ✅
- **TP 4RR**: 23653.39 ✅
- **TP 15RR**: 23863.56 ✅
- **PnL**: 286.60 points (15.0R)
- **MFE**: 296.15 points
- **MAE**: 7.07 points

### Trade #1432 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 19:15:00
- **FVG 5m**: 23710.52 - 23718.10
- **Entrée**: 23720.37 @ 2025-08-06 19:26:00
- **Stop Loss**: 23698.67
- **Risk**: 21.70 points
- **TP 1RR**: 23742.07 ✅
- **TP 2RR**: 23763.77 ❌
- **TP 3RR**: 23785.47 ❌
- **TP 4RR**: 23807.18 ❌
- **TP 15RR**: 24045.90 ❌
- **PnL**: -21.70 points (-1.0R)
- **MFE**: 23.73 points
- **MAE**: 24.49 points

### Trade #1433 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-06 23:15:00
- **FVG 5m**: 23719.11 - 23724.66
- **Entrée**: 23718.10 @ 2025-08-06 23:28:00
- **Stop Loss**: 23736.52
- **Risk**: 18.43 points
- **TP 1RR**: 23699.67 ✅
- **TP 2RR**: 23681.24 ❌
- **TP 3RR**: 23662.82 ❌
- **TP 4RR**: 23644.39 ❌
- **TP 15RR**: 23441.70 ❌
- **PnL**: -18.43 points (-1.0R)
- **MFE**: 31.31 points
- **MAE**: 27.77 points

### Trade #1434 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 02:15:00
- **FVG 5m**: 23781.72 - 23789.04
- **Entrée**: 23780.21 @ 2025-08-07 03:36:00
- **Stop Loss**: 23800.94
- **Risk**: 20.73 points
- **TP 1RR**: 23759.48 ❌
- **TP 2RR**: 23738.74 ❌
- **TP 3RR**: 23718.01 ❌
- **TP 4RR**: 23697.28 ❌
- **TP 15RR**: 23469.24 ❌
- **PnL**: -20.73 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 24.49 points

### Trade #1435 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 06:00:00
- **FVG 5m**: 23832.72 - 23841.81
- **Entrée**: 23830.20 @ 2025-08-07 06:34:00
- **Stop Loss**: 23853.73
- **Risk**: 23.53 points
- **TP 1RR**: 23806.66 ❌
- **TP 2RR**: 23783.13 ❌
- **TP 3RR**: 23759.59 ❌
- **TP 4RR**: 23736.06 ❌
- **TP 15RR**: 23477.17 ❌
- **PnL**: -23.53 points (-1.0R)
- **MFE**: 20.96 points
- **MAE**: 31.31 points

### Trade #1436 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 09:00:00
- **FVG 5m**: 23810.76 - 23823.63
- **Entrée**: 23797.88 @ 2025-08-07 09:24:00
- **Stop Loss**: 23835.54
- **Risk**: 37.66 points
- **TP 1RR**: 23760.22 ✅
- **TP 2RR**: 23722.55 ✅
- **TP 3RR**: 23684.89 ✅
- **TP 4RR**: 23647.22 ✅
- **TP 15RR**: 23232.91 ❌
- **PnL**: -37.66 points (-1.0R)
- **MFE**: 237.83 points
- **MAE**: 38.12 points

### Trade #1437 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-07 09:30:00
- **FVG 5m**: 23661.54 - 23689.31
- **Entrée**: 23697.90 @ 2025-08-07 11:52:00
- **Stop Loss**: 23649.71
- **Risk**: 48.19 points
- **TP 1RR**: 23746.09 ❌
- **TP 2RR**: 23794.27 ❌
- **TP 3RR**: 23842.46 ❌
- **TP 4RR**: 23890.65 ❌
- **TP 15RR**: 24420.71 ❌
- **PnL**: -48.19 points (-1.0R)
- **MFE**: 22.72 points
- **MAE**: 51.00 points

### Trade #1438 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 10:15:00
- **FVG 5m**: 23764.05 - 23771.37
- **Entrée**: 23763.29 @ 2025-08-07 10:30:00
- **Stop Loss**: 23783.26
- **Risk**: 19.96 points
- **TP 1RR**: 23743.33 ✅
- **TP 2RR**: 23723.36 ✅
- **TP 3RR**: 23703.40 ✅
- **TP 4RR**: 23683.43 ✅
- **TP 15RR**: 23463.82 ❌
- **PnL**: -19.96 points (-1.0R)
- **MFE**: 203.24 points
- **MAE**: 21.21 points

### Trade #1439 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 11:30:00
- **FVG 5m**: 23661.54 - 23696.64
- **Entrée**: 23657.76 @ 2025-08-07 11:41:00
- **Stop Loss**: 23708.49
- **Risk**: 50.73 points
- **TP 1RR**: 23607.03 ❌
- **TP 2RR**: 23556.30 ❌
- **TP 3RR**: 23505.57 ❌
- **TP 4RR**: 23454.84 ❌
- **TP 15RR**: 22896.81 ❌
- **PnL**: -50.73 points (-1.0R)
- **MFE**: 36.10 points
- **MAE**: 56.05 points

### Trade #1440 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-07 11:45:00
- **FVG 5m**: 23610.29 - 23629.98
- **Entrée**: 23630.74 @ 2025-08-07 13:54:00
- **Stop Loss**: 23598.48
- **Risk**: 32.26 points
- **TP 1RR**: 23663.00 ✅
- **TP 2RR**: 23695.25 ✅
- **TP 3RR**: 23727.51 ✅
- **TP 4RR**: 23759.76 ✅
- **TP 15RR**: 24114.58 ✅
- **PnL**: 483.84 points (15.0R)
- **MFE**: 486.77 points
- **MAE**: 19.44 points

### Trade #1441 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 13:00:00
- **FVG 5m**: 23592.11 - 23610.04
- **Entrée**: 23581.76 @ 2025-08-07 13:13:00
- **Stop Loss**: 23621.84
- **Risk**: 40.08 points
- **TP 1RR**: 23541.68 ❌
- **TP 2RR**: 23501.60 ❌
- **TP 3RR**: 23461.51 ❌
- **TP 4RR**: 23421.43 ❌
- **TP 15RR**: 22980.53 ❌
- **PnL**: -40.08 points (-1.0R)
- **MFE**: 21.71 points
- **MAE**: 48.48 points

### Trade #1442 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 13:00:00
- **FVG 5m**: 23592.11 - 23610.04
- **Entrée**: 23581.76 @ 2025-08-07 13:13:00
- **Stop Loss**: 23621.84
- **Risk**: 40.08 points
- **TP 1RR**: 23541.68 ❌
- **TP 2RR**: 23501.60 ❌
- **TP 3RR**: 23461.51 ❌
- **TP 4RR**: 23421.43 ❌
- **TP 15RR**: 22980.53 ❌
- **PnL**: -40.08 points (-1.0R)
- **MFE**: 21.71 points
- **MAE**: 48.48 points

### Trade #1443 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 13:00:00
- **FVG 5m**: 23592.11 - 23610.04
- **Entrée**: 23581.76 @ 2025-08-07 13:13:00
- **Stop Loss**: 23621.84
- **Risk**: 40.08 points
- **TP 1RR**: 23541.68 ❌
- **TP 2RR**: 23501.60 ❌
- **TP 3RR**: 23461.51 ❌
- **TP 4RR**: 23421.43 ❌
- **TP 15RR**: 22980.53 ❌
- **PnL**: -40.08 points (-1.0R)
- **MFE**: 21.71 points
- **MAE**: 48.48 points

### Trade #1444 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-07 13:45:00
- **FVG 5m**: 23632.26 - 23644.37
- **Entrée**: 23648.92 @ 2025-08-07 14:31:00
- **Stop Loss**: 23620.44
- **Risk**: 28.48 points
- **TP 1RR**: 23677.40 ✅
- **TP 2RR**: 23705.88 ✅
- **TP 3RR**: 23734.36 ✅
- **TP 4RR**: 23762.84 ✅
- **TP 15RR**: 24076.11 ✅
- **PnL**: 427.19 points (15.0R)
- **MFE**: 437.54 points
- **MAE**: 9.59 points

### Trade #1445 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-07 14:45:00
- **FVG 5m**: 23694.62 - 23732.24
- **Entrée**: 23733.75 @ 2025-08-07 14:59:00
- **Stop Loss**: 23682.77
- **Risk**: 50.98 points
- **TP 1RR**: 23784.73 ✅
- **TP 2RR**: 23835.71 ✅
- **TP 3RR**: 23886.69 ✅
- **TP 4RR**: 23937.67 ✅
- **TP 15RR**: 24498.47 ❌
- **PnL**: -50.98 points (-1.0R)
- **MFE**: 573.12 points
- **MAE**: 51.51 points

### Trade #1446 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-08 07:00:00
- **FVG 5m**: 23782.23 - 23787.28
- **Entrée**: 23779.95 @ 2025-08-08 07:13:00
- **Stop Loss**: 23799.17
- **Risk**: 19.22 points
- **TP 1RR**: 23760.74 ✅
- **TP 2RR**: 23741.52 ❌
- **TP 3RR**: 23722.31 ❌
- **TP 4RR**: 23703.09 ❌
- **TP 15RR**: 23491.72 ❌
- **PnL**: -19.22 points (-1.0R)
- **MFE**: 28.78 points
- **MAE**: 24.74 points

### Trade #1447 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-08 09:45:00
- **FVG 5m**: 23887.00 - 23894.33
- **Entrée**: 23884.23 @ 2025-08-08 10:32:00
- **Stop Loss**: 23906.27
- **Risk**: 22.05 points
- **TP 1RR**: 23862.18 ✅
- **TP 2RR**: 23840.13 ❌
- **TP 3RR**: 23818.09 ❌
- **TP 4RR**: 23796.04 ❌
- **TP 15RR**: 23553.53 ❌
- **PnL**: -22.05 points (-1.0R)
- **MFE**: 38.38 points
- **MAE**: 26.76 points

### Trade #1448 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-08 13:00:00
- **FVG 5m**: 23936.24 - 23939.77
- **Entrée**: 23930.18 @ 2025-08-08 14:31:00
- **Stop Loss**: 23951.74
- **Risk**: 21.56 points
- **TP 1RR**: 23908.61 ❌
- **TP 2RR**: 23887.05 ❌
- **TP 3RR**: 23865.49 ❌
- **TP 4RR**: 23843.92 ❌
- **TP 15RR**: 23606.72 ❌
- **PnL**: -21.56 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 24.74 points

### Trade #1449 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-08 14:45:00
- **FVG 5m**: 23954.92 - 23964.77
- **Entrée**: 23971.08 @ 2025-08-08 15:03:00
- **Stop Loss**: 23942.94
- **Risk**: 28.14 points
- **TP 1RR**: 23999.21 ✅
- **TP 2RR**: 24027.35 ❌
- **TP 3RR**: 24055.49 ❌
- **TP 4RR**: 24083.62 ❌
- **TP 15RR**: 24393.12 ❌
- **PnL**: -28.14 points (-1.0R)
- **MFE**: 35.09 points
- **MAE**: 29.29 points

### Trade #1450 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-08 15:00:00
- **FVG 5m**: 23976.63 - 23984.96
- **Entrée**: 23987.24 @ 2025-08-08 15:13:00
- **Stop Loss**: 23964.64
- **Risk**: 22.59 points
- **TP 1RR**: 24009.83 ❌
- **TP 2RR**: 24032.42 ❌
- **TP 3RR**: 24055.01 ❌
- **TP 4RR**: 24077.61 ❌
- **TP 15RR**: 24326.12 ❌
- **PnL**: -22.59 points (-1.0R)
- **MFE**: 18.94 points
- **MAE**: 26.26 points

### Trade #1451 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-10 17:00:00
- **FVG 5m**: 23950.63 - 23955.93
- **Entrée**: 23949.87 @ 2025-08-10 18:24:00
- **Stop Loss**: 23967.91
- **Risk**: 18.04 points
- **TP 1RR**: 23931.83 ❌
- **TP 2RR**: 23913.80 ❌
- **TP 3RR**: 23895.76 ❌
- **TP 4RR**: 23877.72 ❌
- **TP 15RR**: 23679.31 ❌
- **PnL**: -18.04 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 20.70 points

### Trade #1452 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 02:30:00
- **FVG 5m**: 23950.12 - 23954.92
- **Entrée**: 23947.85 @ 2025-08-11 02:51:00
- **Stop Loss**: 23966.90
- **Risk**: 19.05 points
- **TP 1RR**: 23928.80 ✅
- **TP 2RR**: 23909.76 ✅
- **TP 3RR**: 23890.71 ❌
- **TP 4RR**: 23871.66 ❌
- **TP 15RR**: 23662.15 ❌
- **PnL**: -19.05 points (-1.0R)
- **MFE**: 45.70 points
- **MAE**: 22.98 points

### Trade #1453 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 03:30:00
- **FVG 5m**: 23954.41 - 23956.94
- **Entrée**: 23961.23 @ 2025-08-11 04:30:00
- **Stop Loss**: 23942.44
- **Risk**: 18.79 points
- **TP 1RR**: 23980.03 ✅
- **TP 2RR**: 23998.82 ❌
- **TP 3RR**: 24017.61 ❌
- **TP 4RR**: 24036.41 ❌
- **TP 15RR**: 24243.14 ❌
- **PnL**: -18.79 points (-1.0R)
- **MFE**: 30.30 points
- **MAE**: 20.20 points

### Trade #1454 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 08:30:00
- **FVG 5m**: 23965.02 - 23975.12
- **Entrée**: 23982.19 @ 2025-08-11 10:14:00
- **Stop Loss**: 23953.04
- **Risk**: 29.15 points
- **TP 1RR**: 24011.34 ❌
- **TP 2RR**: 24040.49 ❌
- **TP 3RR**: 24069.64 ❌
- **TP 4RR**: 24098.79 ❌
- **TP 15RR**: 24419.45 ❌
- **PnL**: -29.15 points (-1.0R)
- **MFE**: 4.54 points
- **MAE**: 31.31 points

### Trade #1455 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24011.61
- **Risk**: 24.37 points
- **TP 1RR**: 23962.87 ✅
- **TP 2RR**: 23938.49 ✅
- **TP 3RR**: 23914.12 ✅
- **TP 4RR**: 23889.75 ✅
- **TP 15RR**: 23621.67 ❌
- **PnL**: -24.37 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 33.33 points

### Trade #1456 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24011.61
- **Risk**: 24.37 points
- **TP 1RR**: 23962.87 ✅
- **TP 2RR**: 23938.49 ✅
- **TP 3RR**: 23914.12 ✅
- **TP 4RR**: 23889.75 ✅
- **TP 15RR**: 23621.67 ❌
- **PnL**: -24.37 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 33.33 points

### Trade #1457 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24011.61
- **Risk**: 24.37 points
- **TP 1RR**: 23962.87 ✅
- **TP 2RR**: 23938.49 ✅
- **TP 3RR**: 23914.12 ✅
- **TP 4RR**: 23889.75 ✅
- **TP 15RR**: 23621.67 ❌
- **PnL**: -24.37 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 33.33 points

### Trade #1458 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24011.61
- **Risk**: 24.37 points
- **TP 1RR**: 23962.87 ✅
- **TP 2RR**: 23938.49 ✅
- **TP 3RR**: 23914.12 ✅
- **TP 4RR**: 23889.75 ✅
- **TP 15RR**: 23621.67 ❌
- **PnL**: -24.37 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 33.33 points

### Trade #1459 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24011.61
- **Risk**: 24.37 points
- **TP 1RR**: 23962.87 ✅
- **TP 2RR**: 23938.49 ✅
- **TP 3RR**: 23914.12 ✅
- **TP 4RR**: 23889.75 ✅
- **TP 15RR**: 23621.67 ❌
- **PnL**: -24.37 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 33.33 points

### Trade #1460 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 14:45:00
- **FVG 5m**: 23860.49 - 23870.85
- **Entrée**: 23871.60 @ 2025-08-11 17:53:00
- **Stop Loss**: 23848.56
- **Risk**: 23.04 points
- **TP 1RR**: 23894.64 ✅
- **TP 2RR**: 23917.68 ❌
- **TP 3RR**: 23940.72 ❌
- **TP 4RR**: 23963.76 ❌
- **TP 15RR**: 24217.19 ❌
- **PnL**: -23.04 points (-1.0R)
- **MFE**: 39.64 points
- **MAE**: 36.61 points

### Trade #1461 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 19:15:00
- **FVG 5m**: 23877.91 - 23885.24
- **Entrée**: 23886.50 @ 2025-08-11 20:38:00
- **Stop Loss**: 23865.98
- **Risk**: 20.52 points
- **TP 1RR**: 23907.02 ✅
- **TP 2RR**: 23927.54 ❌
- **TP 3RR**: 23948.07 ❌
- **TP 4RR**: 23968.59 ❌
- **TP 15RR**: 24194.35 ❌
- **PnL**: -20.52 points (-1.0R)
- **MFE**: 24.74 points
- **MAE**: 31.56 points

### Trade #1462 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-12 00:00:00
- **FVG 5m**: 23850.90 - 23858.22
- **Entrée**: 23861.25 @ 2025-08-12 00:53:00
- **Stop Loss**: 23838.97
- **Risk**: 22.28 points
- **TP 1RR**: 23883.53 ✅
- **TP 2RR**: 23905.80 ✅
- **TP 3RR**: 23928.08 ✅
- **TP 4RR**: 23950.36 ✅
- **TP 15RR**: 24195.41 ✅
- **PnL**: 334.15 points (15.0R)
- **MFE**: 346.14 points
- **MAE**: 18.94 points

### Trade #1463 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-12 00:00:00
- **FVG 5m**: 23850.90 - 23858.22
- **Entrée**: 23861.25 @ 2025-08-12 00:53:00
- **Stop Loss**: 23838.97
- **Risk**: 22.28 points
- **TP 1RR**: 23883.53 ✅
- **TP 2RR**: 23905.80 ✅
- **TP 3RR**: 23928.08 ✅
- **TP 4RR**: 23950.36 ✅
- **TP 15RR**: 24195.41 ✅
- **PnL**: 334.15 points (15.0R)
- **MFE**: 346.14 points
- **MAE**: 18.94 points

### Trade #1464 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-12 07:30:00
- **FVG 5m**: 23984.46 - 24002.89
- **Entrée**: 23980.42 @ 2025-08-12 08:04:00
- **Stop Loss**: 24014.89
- **Risk**: 34.47 points
- **TP 1RR**: 23945.95 ✅
- **TP 2RR**: 23911.48 ❌
- **TP 3RR**: 23877.00 ❌
- **TP 4RR**: 23842.53 ❌
- **TP 15RR**: 23463.34 ❌
- **PnL**: -34.47 points (-1.0R)
- **MFE**: 35.35 points
- **MAE**: 37.11 points

### Trade #1465 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-12 07:30:00
- **FVG 5m**: 23984.46 - 24002.89
- **Entrée**: 23980.42 @ 2025-08-12 08:04:00
- **Stop Loss**: 24014.89
- **Risk**: 34.47 points
- **TP 1RR**: 23945.95 ✅
- **TP 2RR**: 23911.48 ❌
- **TP 3RR**: 23877.00 ❌
- **TP 4RR**: 23842.53 ❌
- **TP 15RR**: 23463.34 ❌
- **PnL**: -34.47 points (-1.0R)
- **MFE**: 35.35 points
- **MAE**: 37.11 points

### Trade #1466 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-13 09:15:00
- **FVG 5m**: 24182.15 - 24192.25
- **Entrée**: 24174.57 @ 2025-08-13 10:03:00
- **Stop Loss**: 24204.34
- **Risk**: 29.77 points
- **TP 1RR**: 24144.80 ✅
- **TP 2RR**: 24115.03 ✅
- **TP 3RR**: 24085.27 ✅
- **TP 4RR**: 24055.50 ✅
- **TP 15RR**: 23728.03 ❌
- **PnL**: -29.77 points (-1.0R)
- **MFE**: 145.68 points
- **MAE**: 38.88 points

### Trade #1467 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-13 09:15:00
- **FVG 5m**: 24182.15 - 24192.25
- **Entrée**: 24174.57 @ 2025-08-13 10:03:00
- **Stop Loss**: 24204.34
- **Risk**: 29.77 points
- **TP 1RR**: 24144.80 ✅
- **TP 2RR**: 24115.03 ✅
- **TP 3RR**: 24085.27 ✅
- **TP 4RR**: 24055.50 ✅
- **TP 15RR**: 23728.03 ❌
- **PnL**: -29.77 points (-1.0R)
- **MFE**: 145.68 points
- **MAE**: 38.88 points

### Trade #1468 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-13 10:15:00
- **FVG 5m**: 24147.56 - 24158.92
- **Entrée**: 24159.93 @ 2025-08-13 12:19:00
- **Stop Loss**: 24135.48
- **Risk**: 24.45 points
- **TP 1RR**: 24184.38 ✅
- **TP 2RR**: 24208.82 ❌
- **TP 3RR**: 24233.27 ❌
- **TP 4RR**: 24257.71 ❌
- **TP 15RR**: 24526.61 ❌
- **PnL**: -24.45 points (-1.0R)
- **MFE**: 31.56 points
- **MAE**: 36.10 points

### Trade #1469 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-13 10:30:00
- **FVG 5m**: 24147.56 - 24158.92
- **Entrée**: 24159.93 @ 2025-08-13 12:19:00
- **Stop Loss**: 24135.48
- **Risk**: 24.45 points
- **TP 1RR**: 24184.38 ✅
- **TP 2RR**: 24208.82 ❌
- **TP 3RR**: 24233.27 ❌
- **TP 4RR**: 24257.71 ❌
- **TP 15RR**: 24526.61 ❌
- **PnL**: -24.45 points (-1.0R)
- **MFE**: 31.56 points
- **MAE**: 36.10 points

### Trade #1470 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24223.29
- **Risk**: 38.11 points
- **TP 1RR**: 24147.07 ✅
- **TP 2RR**: 24108.96 ✅
- **TP 3RR**: 24070.85 ✅
- **TP 4RR**: 24032.74 ✅
- **TP 15RR**: 23613.52 ✅
- **PnL**: 571.66 points (15.0R)
- **MFE**: 573.63 points
- **MAE**: 32.32 points

### Trade #1471 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24223.29
- **Risk**: 38.11 points
- **TP 1RR**: 24147.07 ✅
- **TP 2RR**: 24108.96 ✅
- **TP 3RR**: 24070.85 ✅
- **TP 4RR**: 24032.74 ✅
- **TP 15RR**: 23613.52 ✅
- **PnL**: 571.66 points (15.0R)
- **MFE**: 573.63 points
- **MAE**: 32.32 points

### Trade #1472 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24223.29
- **Risk**: 38.11 points
- **TP 1RR**: 24147.07 ✅
- **TP 2RR**: 24108.96 ✅
- **TP 3RR**: 24070.85 ✅
- **TP 4RR**: 24032.74 ✅
- **TP 15RR**: 23613.52 ✅
- **PnL**: 571.66 points (15.0R)
- **MFE**: 573.63 points
- **MAE**: 32.32 points

### Trade #1473 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24223.29
- **Risk**: 38.11 points
- **TP 1RR**: 24147.07 ✅
- **TP 2RR**: 24108.96 ✅
- **TP 3RR**: 24070.85 ✅
- **TP 4RR**: 24032.74 ✅
- **TP 15RR**: 23613.52 ✅
- **PnL**: 571.66 points (15.0R)
- **MFE**: 573.63 points
- **MAE**: 32.32 points

### Trade #1474 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24181.16
- **Risk**: 31.03 points
- **TP 1RR**: 24243.22 ✅
- **TP 2RR**: 24274.26 ❌
- **TP 3RR**: 24305.29 ❌
- **TP 4RR**: 24336.32 ❌
- **TP 15RR**: 24677.68 ❌
- **PnL**: -31.03 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 34.59 points

### Trade #1475 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24181.16
- **Risk**: 31.03 points
- **TP 1RR**: 24243.22 ✅
- **TP 2RR**: 24274.26 ❌
- **TP 3RR**: 24305.29 ❌
- **TP 4RR**: 24336.32 ❌
- **TP 15RR**: 24677.68 ❌
- **PnL**: -31.03 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 34.59 points

### Trade #1476 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24181.16
- **Risk**: 31.03 points
- **TP 1RR**: 24243.22 ✅
- **TP 2RR**: 24274.26 ❌
- **TP 3RR**: 24305.29 ❌
- **TP 4RR**: 24336.32 ❌
- **TP 15RR**: 24677.68 ❌
- **PnL**: -31.03 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 34.59 points

### Trade #1477 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24181.16
- **Risk**: 31.03 points
- **TP 1RR**: 24243.22 ✅
- **TP 2RR**: 24274.26 ❌
- **TP 3RR**: 24305.29 ❌
- **TP 4RR**: 24336.32 ❌
- **TP 15RR**: 24677.68 ❌
- **PnL**: -31.03 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 34.59 points

### Trade #1478 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24181.16
- **Risk**: 31.03 points
- **TP 1RR**: 24243.22 ✅
- **TP 2RR**: 24274.26 ❌
- **TP 3RR**: 24305.29 ❌
- **TP 4RR**: 24336.32 ❌
- **TP 15RR**: 24677.68 ❌
- **PnL**: -31.03 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 34.59 points

### Trade #1479 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24181.16
- **Risk**: 31.03 points
- **TP 1RR**: 24243.22 ✅
- **TP 2RR**: 24274.26 ❌
- **TP 3RR**: 24305.29 ❌
- **TP 4RR**: 24336.32 ❌
- **TP 15RR**: 24677.68 ❌
- **PnL**: -31.03 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 34.59 points

### Trade #1480 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 09:45:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24223.29
- **Risk**: 38.11 points
- **TP 1RR**: 24147.07 ✅
- **TP 2RR**: 24108.96 ✅
- **TP 3RR**: 24070.85 ✅
- **TP 4RR**: 24032.74 ✅
- **TP 15RR**: 23613.52 ✅
- **PnL**: 571.66 points (15.0R)
- **MFE**: 573.63 points
- **MAE**: 32.32 points

### Trade #1481 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 09:45:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24223.29
- **Risk**: 38.11 points
- **TP 1RR**: 24147.07 ✅
- **TP 2RR**: 24108.96 ✅
- **TP 3RR**: 24070.85 ✅
- **TP 4RR**: 24032.74 ✅
- **TP 15RR**: 23613.52 ✅
- **PnL**: 571.66 points (15.0R)
- **MFE**: 573.63 points
- **MAE**: 32.32 points

### Trade #1482 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 09:45:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24223.29
- **Risk**: 38.11 points
- **TP 1RR**: 24147.07 ✅
- **TP 2RR**: 24108.96 ✅
- **TP 3RR**: 24070.85 ✅
- **TP 4RR**: 24032.74 ✅
- **TP 15RR**: 23613.52 ✅
- **PnL**: 571.66 points (15.0R)
- **MFE**: 573.63 points
- **MAE**: 32.32 points

### Trade #1483 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-15 04:00:00
- **FVG 5m**: 24131.15 - 24135.94
- **Entrée**: 24137.71 @ 2025-08-15 05:31:00
- **Stop Loss**: 24119.08
- **Risk**: 18.63 points
- **TP 1RR**: 24156.34 ✅
- **TP 2RR**: 24174.97 ❌
- **TP 3RR**: 24193.60 ❌
- **TP 4RR**: 24212.23 ❌
- **TP 15RR**: 24417.16 ❌
- **PnL**: -18.63 points (-1.0R)
- **MFE**: 26.51 points
- **MAE**: 40.90 points

### Trade #1484 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-15 08:45:00
- **FVG 5m**: 24054.14 - 24063.48
- **Entrée**: 24049.35 @ 2025-08-15 09:46:00
- **Stop Loss**: 24075.52
- **Risk**: 26.17 points
- **TP 1RR**: 24023.18 ✅
- **TP 2RR**: 23997.00 ✅
- **TP 3RR**: 23970.83 ✅
- **TP 4RR**: 23944.66 ❌
- **TP 15RR**: 23656.79 ❌
- **PnL**: -26.17 points (-1.0R)
- **MFE**: 79.78 points
- **MAE**: 28.28 points

### Trade #1485 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-15 08:45:00
- **FVG 5m**: 24054.14 - 24063.48
- **Entrée**: 24049.35 @ 2025-08-15 09:46:00
- **Stop Loss**: 24075.52
- **Risk**: 26.17 points
- **TP 1RR**: 24023.18 ✅
- **TP 2RR**: 23997.00 ✅
- **TP 3RR**: 23970.83 ✅
- **TP 4RR**: 23944.66 ❌
- **TP 15RR**: 23656.79 ❌
- **PnL**: -26.17 points (-1.0R)
- **MFE**: 79.78 points
- **MAE**: 28.28 points

### Trade #1486 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-15 08:45:00
- **FVG 5m**: 24050.10 - 24077.12
- **Entrée**: 24077.62 @ 2025-08-15 09:03:00
- **Stop Loss**: 24038.08
- **Risk**: 39.54 points
- **TP 1RR**: 24117.17 ✅
- **TP 2RR**: 24156.71 ❌
- **TP 3RR**: 24196.26 ❌
- **TP 4RR**: 24235.80 ❌
- **TP 15RR**: 24670.80 ❌
- **PnL**: -39.54 points (-1.0R)
- **MFE**: 39.89 points
- **MAE**: 40.40 points

### Trade #1487 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 03:30:00
- **FVG 5m**: 24012.23 - 24020.06
- **Entrée**: 24021.57 @ 2025-08-18 05:42:00
- **Stop Loss**: 24000.23
- **Risk**: 21.35 points
- **TP 1RR**: 24042.92 ❌
- **TP 2RR**: 24064.27 ❌
- **TP 3RR**: 24085.62 ❌
- **TP 4RR**: 24106.96 ❌
- **TP 15RR**: 24341.79 ❌
- **PnL**: -21.35 points (-1.0R)
- **MFE**: 6.06 points
- **MAE**: 23.48 points

### Trade #1488 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 03:30:00
- **FVG 5m**: 24012.23 - 24020.06
- **Entrée**: 24021.57 @ 2025-08-18 05:42:00
- **Stop Loss**: 24000.23
- **Risk**: 21.35 points
- **TP 1RR**: 24042.92 ❌
- **TP 2RR**: 24064.27 ❌
- **TP 3RR**: 24085.62 ❌
- **TP 4RR**: 24106.96 ❌
- **TP 15RR**: 24341.79 ❌
- **PnL**: -21.35 points (-1.0R)
- **MFE**: 6.06 points
- **MAE**: 23.48 points

### Trade #1489 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-18 08:30:00
- **FVG 5m**: 24004.40 - 24007.69
- **Entrée**: 23987.24 @ 2025-08-18 08:51:00
- **Stop Loss**: 24019.69
- **Risk**: 32.45 points
- **TP 1RR**: 23954.78 ❌
- **TP 2RR**: 23922.33 ❌
- **TP 3RR**: 23889.87 ❌
- **TP 4RR**: 23857.42 ❌
- **TP 15RR**: 23500.42 ❌
- **PnL**: -32.45 points (-1.0R)
- **MFE**: 17.17 points
- **MAE**: 36.86 points

### Trade #1490 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 09:45:00
- **FVG 5m**: 23989.26 - 23992.29
- **Entrée**: 23993.04 @ 2025-08-18 12:13:00
- **Stop Loss**: 23977.26
- **Risk**: 15.78 points
- **TP 1RR**: 24008.83 ✅
- **TP 2RR**: 24024.61 ✅
- **TP 3RR**: 24040.39 ✅
- **TP 4RR**: 24056.17 ✅
- **TP 15RR**: 24229.77 ❌
- **PnL**: -15.78 points (-1.0R)
- **MFE**: 81.04 points
- **MAE**: 15.91 points

### Trade #1491 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 09:45:00
- **FVG 5m**: 23989.26 - 23992.29
- **Entrée**: 23993.04 @ 2025-08-18 12:13:00
- **Stop Loss**: 23977.26
- **Risk**: 15.78 points
- **TP 1RR**: 24008.83 ✅
- **TP 2RR**: 24024.61 ✅
- **TP 3RR**: 24040.39 ✅
- **TP 4RR**: 24056.17 ✅
- **TP 15RR**: 24229.77 ❌
- **PnL**: -15.78 points (-1.0R)
- **MFE**: 81.04 points
- **MAE**: 15.91 points

### Trade #1492 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 09:45:00
- **FVG 5m**: 23989.26 - 23992.29
- **Entrée**: 23993.04 @ 2025-08-18 12:13:00
- **Stop Loss**: 23977.26
- **Risk**: 15.78 points
- **TP 1RR**: 24008.83 ✅
- **TP 2RR**: 24024.61 ✅
- **TP 3RR**: 24040.39 ✅
- **TP 4RR**: 24056.17 ✅
- **TP 15RR**: 24229.77 ❌
- **PnL**: -15.78 points (-1.0R)
- **MFE**: 81.04 points
- **MAE**: 15.91 points

### Trade #1493 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 20:30:00
- **FVG 5m**: 24000.87 - 24010.46
- **Entrée**: 24012.48 @ 2025-08-18 22:24:00
- **Stop Loss**: 23988.87
- **Risk**: 23.61 points
- **TP 1RR**: 24036.10 ❌
- **TP 2RR**: 24059.71 ❌
- **TP 3RR**: 24083.33 ❌
- **TP 4RR**: 24106.94 ❌
- **TP 15RR**: 24366.70 ❌
- **PnL**: -23.61 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 24.74 points

### Trade #1494 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 02:30:00
- **FVG 5m**: 23993.04 - 23998.60
- **Entrée**: 24000.37 @ 2025-08-19 02:42:00
- **Stop Loss**: 23981.05
- **Risk**: 19.32 points
- **TP 1RR**: 24019.68 ✅
- **TP 2RR**: 24039.00 ❌
- **TP 3RR**: 24058.32 ❌
- **TP 4RR**: 24077.64 ❌
- **TP 15RR**: 24290.14 ❌
- **PnL**: -19.32 points (-1.0R)
- **MFE**: 19.44 points
- **MAE**: 19.69 points

### Trade #1495 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 03:00:00
- **FVG 5m**: 23992.29 - 23996.07
- **Entrée**: 23984.21 @ 2025-08-19 03:11:00
- **Stop Loss**: 24008.07
- **Risk**: 23.86 points
- **TP 1RR**: 23960.34 ❌
- **TP 2RR**: 23936.48 ❌
- **TP 3RR**: 23912.61 ❌
- **TP 4RR**: 23888.75 ❌
- **TP 15RR**: 23626.24 ❌
- **PnL**: -23.86 points (-1.0R)
- **MFE**: 3.53 points
- **MAE**: 27.77 points

### Trade #1496 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23812.56
- **Risk**: 38.66 points
- **TP 1RR**: 23735.23 ❌
- **TP 2RR**: 23696.57 ❌
- **TP 3RR**: 23657.91 ❌
- **TP 4RR**: 23619.24 ❌
- **TP 15RR**: 23193.95 ❌
- **PnL**: -38.66 points (-1.0R)
- **MFE**: 26.51 points
- **MAE**: 43.93 points

### Trade #1497 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23812.56
- **Risk**: 38.66 points
- **TP 1RR**: 23735.23 ❌
- **TP 2RR**: 23696.57 ❌
- **TP 3RR**: 23657.91 ❌
- **TP 4RR**: 23619.24 ❌
- **TP 15RR**: 23193.95 ❌
- **PnL**: -38.66 points (-1.0R)
- **MFE**: 26.51 points
- **MAE**: 43.93 points

### Trade #1498 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23812.56
- **Risk**: 38.66 points
- **TP 1RR**: 23735.23 ❌
- **TP 2RR**: 23696.57 ❌
- **TP 3RR**: 23657.91 ❌
- **TP 4RR**: 23619.24 ❌
- **TP 15RR**: 23193.95 ❌
- **PnL**: -38.66 points (-1.0R)
- **MFE**: 26.51 points
- **MAE**: 43.93 points

### Trade #1499 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23812.56
- **Risk**: 38.66 points
- **TP 1RR**: 23735.23 ❌
- **TP 2RR**: 23696.57 ❌
- **TP 3RR**: 23657.91 ❌
- **TP 4RR**: 23619.24 ❌
- **TP 15RR**: 23193.95 ❌
- **PnL**: -38.66 points (-1.0R)
- **MFE**: 26.51 points
- **MAE**: 43.93 points

### Trade #1500 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23812.56
- **Risk**: 38.66 points
- **TP 1RR**: 23735.23 ❌
- **TP 2RR**: 23696.57 ❌
- **TP 3RR**: 23657.91 ❌
- **TP 4RR**: 23619.24 ❌
- **TP 15RR**: 23193.95 ❌
- **PnL**: -38.66 points (-1.0R)
- **MFE**: 26.51 points
- **MAE**: 43.93 points

### Trade #1501 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 10:00:00
- **FVG 5m**: 23711.03 - 23715.57
- **Entrée**: 23722.39 @ 2025-08-19 12:28:00
- **Stop Loss**: 23699.17
- **Risk**: 23.22 points
- **TP 1RR**: 23745.61 ✅
- **TP 2RR**: 23768.82 ❌
- **TP 3RR**: 23792.04 ❌
- **TP 4RR**: 23815.26 ❌
- **TP 15RR**: 24070.64 ❌
- **PnL**: -23.22 points (-1.0R)
- **MFE**: 27.77 points
- **MAE**: 28.28 points

### Trade #1502 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 12:45:00
- **FVG 5m**: 23674.67 - 23686.79
- **Entrée**: 23694.87 @ 2025-08-19 14:24:00
- **Stop Loss**: 23662.83
- **Risk**: 32.04 points
- **TP 1RR**: 23726.90 ❌
- **TP 2RR**: 23758.94 ❌
- **TP 3RR**: 23790.98 ❌
- **TP 4RR**: 23823.01 ❌
- **TP 15RR**: 24175.40 ❌
- **PnL**: -32.04 points (-1.0R)
- **MFE**: 25.25 points
- **MAE**: 36.61 points

### Trade #1503 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 14:15:00
- **FVG 5m**: 23695.12 - 23702.95
- **Entrée**: 23714.56 @ 2025-08-19 15:00:00
- **Stop Loss**: 23683.27
- **Risk**: 31.29 points
- **TP 1RR**: 23745.85 ❌
- **TP 2RR**: 23777.14 ❌
- **TP 3RR**: 23808.43 ❌
- **TP 4RR**: 23839.72 ❌
- **TP 15RR**: 24183.89 ❌
- **PnL**: -31.29 points (-1.0R)
- **MFE**: 5.55 points
- **MAE**: 32.32 points

### Trade #1504 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 18:15:00
- **FVG 5m**: 23641.60 - 23646.39
- **Entrée**: 23646.90 @ 2025-08-19 19:46:00
- **Stop Loss**: 23629.78
- **Risk**: 17.12 points
- **TP 1RR**: 23664.02 ❌
- **TP 2RR**: 23681.14 ❌
- **TP 3RR**: 23698.27 ❌
- **TP 4RR**: 23715.39 ❌
- **TP 15RR**: 23903.74 ❌
- **PnL**: -17.12 points (-1.0R)
- **MFE**: 9.85 points
- **MAE**: 23.99 points

### Trade #1505 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-20 03:00:00
- **FVG 5m**: 23626.20 - 23629.73
- **Entrée**: 23625.19 @ 2025-08-20 03:11:00
- **Stop Loss**: 23641.55
- **Risk**: 16.36 points
- **TP 1RR**: 23608.83 ✅
- **TP 2RR**: 23592.47 ❌
- **TP 3RR**: 23576.11 ❌
- **TP 4RR**: 23559.75 ❌
- **TP 15RR**: 23379.79 ❌
- **PnL**: -16.36 points (-1.0R)
- **MFE**: 22.47 points
- **MAE**: 19.44 points

### Trade #1506 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-20 06:15:00
- **FVG 5m**: 23652.45 - 23659.27
- **Entrée**: 23650.18 @ 2025-08-20 06:27:00
- **Stop Loss**: 23671.10
- **Risk**: 20.92 points
- **TP 1RR**: 23629.26 ✅
- **TP 2RR**: 23608.34 ✅
- **TP 3RR**: 23587.42 ✅
- **TP 4RR**: 23566.51 ✅
- **TP 15RR**: 23336.40 ✅
- **PnL**: 313.78 points (15.0R)
- **MFE**: 322.16 points
- **MAE**: 18.18 points

### Trade #1507 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-20 08:45:00
- **FVG 5m**: 23358.07 - 23394.42
- **Entrée**: 23352.51 @ 2025-08-20 09:06:00
- **Stop Loss**: 23406.12
- **Risk**: 53.61 points
- **TP 1RR**: 23298.90 ✅
- **TP 2RR**: 23245.30 ❌
- **TP 3RR**: 23191.69 ❌
- **TP 4RR**: 23138.08 ❌
- **TP 15RR**: 22548.39 ❌
- **PnL**: -53.61 points (-1.0R)
- **MFE**: 89.38 points
- **MAE**: 65.14 points

### Trade #1508 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 09:00:00
- **FVG 5m**: 23289.65 - 23302.52
- **Entrée**: 23305.05 @ 2025-08-20 10:04:00
- **Stop Loss**: 23278.00
- **Risk**: 27.05 points
- **TP 1RR**: 23332.09 ✅
- **TP 2RR**: 23359.14 ✅
- **TP 3RR**: 23386.18 ✅
- **TP 4RR**: 23413.23 ✅
- **TP 15RR**: 23710.73 ✅
- **PnL**: 405.69 points (15.0R)
- **MFE**: 443.35 points
- **MAE**: 2.52 points

### Trade #1509 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 09:45:00
- **FVG 5m**: 23289.65 - 23302.52
- **Entrée**: 23305.05 @ 2025-08-20 10:04:00
- **Stop Loss**: 23278.00
- **Risk**: 27.05 points
- **TP 1RR**: 23332.09 ✅
- **TP 2RR**: 23359.14 ✅
- **TP 3RR**: 23386.18 ✅
- **TP 4RR**: 23413.23 ✅
- **TP 15RR**: 23710.73 ✅
- **PnL**: 405.69 points (15.0R)
- **MFE**: 443.35 points
- **MAE**: 2.52 points

### Trade #1510 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 14:30:00
- **FVG 5m**: 23550.96 - 23553.48
- **Entrée**: 23560.05 @ 2025-08-20 17:09:00
- **Stop Loss**: 23539.18
- **Risk**: 20.86 points
- **TP 1RR**: 23580.91 ❌
- **TP 2RR**: 23601.78 ❌
- **TP 3RR**: 23622.64 ❌
- **TP 4RR**: 23643.51 ❌
- **TP 15RR**: 23873.02 ❌
- **PnL**: -20.86 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 22.98 points

### Trade #1511 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 14:30:00
- **FVG 5m**: 23550.96 - 23553.48
- **Entrée**: 23560.05 @ 2025-08-20 17:09:00
- **Stop Loss**: 23539.18
- **Risk**: 20.86 points
- **TP 1RR**: 23580.91 ❌
- **TP 2RR**: 23601.78 ❌
- **TP 3RR**: 23622.64 ❌
- **TP 4RR**: 23643.51 ❌
- **TP 15RR**: 23873.02 ❌
- **PnL**: -20.86 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 22.98 points

### Trade #1512 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-21 03:45:00
- **FVG 5m**: 23536.31 - 23543.64
- **Entrée**: 23528.99 @ 2025-08-21 03:59:00
- **Stop Loss**: 23555.41
- **Risk**: 26.42 points
- **TP 1RR**: 23502.58 ❌
- **TP 2RR**: 23476.16 ❌
- **TP 3RR**: 23449.75 ❌
- **TP 4RR**: 23423.33 ❌
- **TP 15RR**: 23132.76 ❌
- **PnL**: -26.42 points (-1.0R)
- **MFE**: 8.33 points
- **MAE**: 27.27 points

### Trade #1513 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-21 12:30:00
- **FVG 5m**: 23429.26 - 23432.55
- **Entrée**: 23443.15 @ 2025-08-21 13:55:00
- **Stop Loss**: 23417.55
- **Risk**: 25.60 points
- **TP 1RR**: 23468.75 ✅
- **TP 2RR**: 23494.35 ❌
- **TP 3RR**: 23519.95 ❌
- **TP 4RR**: 23545.55 ❌
- **TP 15RR**: 23827.16 ❌
- **PnL**: -25.60 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 26.51 points

### Trade #1514 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-22 01:45:00
- **FVG 5m**: 23373.47 - 23391.90
- **Entrée**: 23396.44 @ 2025-08-22 02:04:00
- **Stop Loss**: 23361.78
- **Risk**: 34.66 points
- **TP 1RR**: 23431.10 ✅
- **TP 2RR**: 23465.77 ✅
- **TP 3RR**: 23500.43 ✅
- **TP 4RR**: 23535.09 ✅
- **TP 15RR**: 23916.37 ✅
- **PnL**: 519.93 points (15.0R)
- **MFE**: 527.17 points
- **MAE**: 4.54 points

### Trade #1515 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-22 02:45:00
- **FVG 5m**: 23432.80 - 23452.74
- **Entrée**: 23454.01 @ 2025-08-22 03:09:00
- **Stop Loss**: 23421.08
- **Risk**: 32.92 points
- **TP 1RR**: 23486.93 ✅
- **TP 2RR**: 23519.86 ✅
- **TP 3RR**: 23552.78 ✅
- **TP 4RR**: 23585.70 ✅
- **TP 15RR**: 23947.87 ✅
- **PnL**: 493.87 points (15.0R)
- **MFE**: 515.30 points
- **MAE**: 18.68 points

### Trade #1516 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-22 08:45:00
- **FVG 5m**: 23829.44 - 23840.55
- **Entrée**: 23823.63 @ 2025-08-22 10:48:00
- **Stop Loss**: 23852.47
- **Risk**: 28.84 points
- **TP 1RR**: 23794.80 ✅
- **TP 2RR**: 23765.96 ✅
- **TP 3RR**: 23737.12 ❌
- **TP 4RR**: 23708.29 ❌
- **TP 15RR**: 23391.09 ❌
- **PnL**: -28.84 points (-1.0R)
- **MFE**: 83.57 points
- **MAE**: 29.29 points

### Trade #1517 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-24 22:30:00
- **FVG 5m**: 23782.98 - 23788.29
- **Entrée**: 23790.81 @ 2025-08-24 23:18:00
- **Stop Loss**: 23771.09
- **Risk**: 19.72 points
- **TP 1RR**: 23810.53 ❌
- **TP 2RR**: 23830.25 ❌
- **TP 3RR**: 23849.96 ❌
- **TP 4RR**: 23869.68 ❌
- **TP 15RR**: 24086.58 ❌
- **PnL**: -19.72 points (-1.0R)
- **MFE**: 11.11 points
- **MAE**: 19.95 points

### Trade #1518 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 02:00:00
- **FVG 5m**: 23756.73 - 23760.77
- **Entrée**: 23762.28 @ 2025-08-25 02:44:00
- **Stop Loss**: 23744.85
- **Risk**: 17.43 points
- **TP 1RR**: 23779.71 ❌
- **TP 2RR**: 23797.15 ❌
- **TP 3RR**: 23814.58 ❌
- **TP 4RR**: 23832.01 ❌
- **TP 15RR**: 24023.77 ❌
- **PnL**: -17.43 points (-1.0R)
- **MFE**: 8.58 points
- **MAE**: 18.43 points

### Trade #1519 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 08:30:00
- **FVG 5m**: 23728.95 - 23737.79
- **Entrée**: 23743.09 @ 2025-08-25 08:57:00
- **Stop Loss**: 23717.09
- **Risk**: 26.00 points
- **TP 1RR**: 23769.10 ✅
- **TP 2RR**: 23795.10 ✅
- **TP 3RR**: 23821.10 ✅
- **TP 4RR**: 23847.10 ✅
- **TP 15RR**: 24133.14 ❌
- **PnL**: -26.00 points (-1.0R)
- **MFE**: 107.05 points
- **MAE**: 101.24 points

### Trade #1520 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 08:45:00
- **FVG 5m**: 23728.95 - 23737.79
- **Entrée**: 23743.09 @ 2025-08-25 08:57:00
- **Stop Loss**: 23717.09
- **Risk**: 26.00 points
- **TP 1RR**: 23769.10 ✅
- **TP 2RR**: 23795.10 ✅
- **TP 3RR**: 23821.10 ✅
- **TP 4RR**: 23847.10 ✅
- **TP 15RR**: 24133.14 ❌
- **PnL**: -26.00 points (-1.0R)
- **MFE**: 107.05 points
- **MAE**: 101.24 points

### Trade #1521 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 08:45:00
- **FVG 5m**: 23728.95 - 23737.79
- **Entrée**: 23743.09 @ 2025-08-25 08:57:00
- **Stop Loss**: 23717.09
- **Risk**: 26.00 points
- **TP 1RR**: 23769.10 ✅
- **TP 2RR**: 23795.10 ✅
- **TP 3RR**: 23821.10 ✅
- **TP 4RR**: 23847.10 ✅
- **TP 15RR**: 24133.14 ❌
- **PnL**: -26.00 points (-1.0R)
- **MFE**: 107.05 points
- **MAE**: 101.24 points

### Trade #1522 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 11:45:00
- **FVG 5m**: 23808.48 - 23811.01
- **Entrée**: 23808.23 @ 2025-08-25 12:36:00
- **Stop Loss**: 23822.91
- **Risk**: 14.68 points
- **TP 1RR**: 23793.55 ✅
- **TP 2RR**: 23778.87 ✅
- **TP 3RR**: 23764.18 ✅
- **TP 4RR**: 23749.50 ✅
- **TP 15RR**: 23587.99 ❌
- **PnL**: -14.68 points (-1.0R)
- **MFE**: 205.26 points
- **MAE**: 15.40 points

### Trade #1523 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 13:15:00
- **FVG 5m**: 23792.83 - 23799.14
- **Entrée**: 23790.81 @ 2025-08-25 14:20:00
- **Stop Loss**: 23811.04
- **Risk**: 20.23 points
- **TP 1RR**: 23770.58 ✅
- **TP 2RR**: 23750.35 ✅
- **TP 3RR**: 23730.12 ✅
- **TP 4RR**: 23709.89 ✅
- **TP 15RR**: 23487.34 ❌
- **PnL**: -20.23 points (-1.0R)
- **MFE**: 187.84 points
- **MAE**: 21.97 points

### Trade #1524 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 19:00:00
- **FVG 5m**: 23628.22 - 23635.03
- **Entrée**: 23638.82 @ 2025-08-25 19:51:00
- **Stop Loss**: 23616.40
- **Risk**: 22.42 points
- **TP 1RR**: 23661.24 ✅
- **TP 2RR**: 23683.66 ✅
- **TP 3RR**: 23706.07 ✅
- **TP 4RR**: 23728.49 ✅
- **TP 15RR**: 23975.09 ✅
- **PnL**: 336.27 points (15.0R)
- **MFE**: 338.07 points
- **MAE**: 10.86 points

### Trade #1525 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 19:30:00
- **FVG 5m**: 23628.22 - 23653.46
- **Entrée**: 23611.80 @ 2025-08-25 19:42:00
- **Stop Loss**: 23665.29
- **Risk**: 53.49 points
- **TP 1RR**: 23558.32 ❌
- **TP 2RR**: 23504.83 ❌
- **TP 3RR**: 23451.35 ❌
- **TP 4RR**: 23397.86 ❌
- **TP 15RR**: 22809.53 ❌
- **PnL**: -53.49 points (-1.0R)
- **MFE**: 8.84 points
- **MAE**: 54.79 points

### Trade #1526 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 19:30:00
- **FVG 5m**: 23628.22 - 23653.46
- **Entrée**: 23611.80 @ 2025-08-25 19:42:00
- **Stop Loss**: 23665.29
- **Risk**: 53.49 points
- **TP 1RR**: 23558.32 ❌
- **TP 2RR**: 23504.83 ❌
- **TP 3RR**: 23451.35 ❌
- **TP 4RR**: 23397.86 ❌
- **TP 15RR**: 22809.53 ❌
- **PnL**: -53.49 points (-1.0R)
- **MFE**: 8.84 points
- **MAE**: 54.79 points

### Trade #1527 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-26 08:30:00
- **FVG 5m**: 23748.90 - 23752.69
- **Entrée**: 23747.13 @ 2025-08-26 10:28:00
- **Stop Loss**: 23764.56
- **Risk**: 17.43 points
- **TP 1RR**: 23729.70 ✅
- **TP 2RR**: 23712.27 ❌
- **TP 3RR**: 23694.84 ❌
- **TP 4RR**: 23677.41 ❌
- **TP 15RR**: 23485.67 ❌
- **PnL**: -17.43 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 18.68 points

### Trade #1528 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-26 08:45:00
- **FVG 5m**: 23761.52 - 23768.09
- **Entrée**: 23775.16 @ 2025-08-26 09:22:00
- **Stop Loss**: 23749.64
- **Risk**: 25.51 points
- **TP 1RR**: 23800.67 ❌
- **TP 2RR**: 23826.19 ❌
- **TP 3RR**: 23851.70 ❌
- **TP 4RR**: 23877.21 ❌
- **TP 15RR**: 24157.87 ❌
- **PnL**: -25.51 points (-1.0R)
- **MFE**: 6.82 points
- **MAE**: 28.02 points

### Trade #1529 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-26 10:15:00
- **FVG 5m**: 23748.90 - 23752.69
- **Entrée**: 23747.13 @ 2025-08-26 10:28:00
- **Stop Loss**: 23764.56
- **Risk**: 17.43 points
- **TP 1RR**: 23729.70 ✅
- **TP 2RR**: 23712.27 ❌
- **TP 3RR**: 23694.84 ❌
- **TP 4RR**: 23677.41 ❌
- **TP 15RR**: 23485.67 ❌
- **PnL**: -17.43 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 18.68 points

### Trade #1530 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-26 12:45:00
- **FVG 5m**: 23752.69 - 23755.72
- **Entrée**: 23756.98 @ 2025-08-26 13:11:00
- **Stop Loss**: 23740.81
- **Risk**: 16.17 points
- **TP 1RR**: 23773.15 ✅
- **TP 2RR**: 23789.32 ✅
- **TP 3RR**: 23805.48 ✅
- **TP 4RR**: 23821.65 ✅
- **TP 15RR**: 23999.50 ❌
- **PnL**: -16.17 points (-1.0R)
- **MFE**: 106.04 points
- **MAE**: 28.28 points

### Trade #1531 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-26 21:15:00
- **FVG 5m**: 23850.90 - 23853.93
- **Entrée**: 23849.13 @ 2025-08-26 21:29:00
- **Stop Loss**: 23865.86
- **Risk**: 16.72 points
- **TP 1RR**: 23832.41 ✅
- **TP 2RR**: 23815.68 ✅
- **TP 3RR**: 23798.96 ✅
- **TP 4RR**: 23782.24 ✅
- **TP 15RR**: 23598.27 ❌
- **PnL**: -16.72 points (-1.0R)
- **MFE**: 129.02 points
- **MAE**: 18.68 points

### Trade #1532 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 07:15:00
- **FVG 5m**: 23831.71 - 23844.08
- **Entrée**: 23830.70 @ 2025-08-27 07:28:00
- **Stop Loss**: 23856.00
- **Risk**: 25.30 points
- **TP 1RR**: 23805.40 ✅
- **TP 2RR**: 23780.09 ✅
- **TP 3RR**: 23754.79 ✅
- **TP 4RR**: 23729.49 ✅
- **TP 15RR**: 23451.15 ❌
- **PnL**: -25.30 points (-1.0R)
- **MFE**: 110.58 points
- **MAE**: 28.02 points

### Trade #1533 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 09:15:00
- **FVG 5m**: 23839.79 - 23848.88
- **Entrée**: 23849.64 @ 2025-08-27 10:47:00
- **Stop Loss**: 23827.87
- **Risk**: 21.77 points
- **TP 1RR**: 23871.40 ❌
- **TP 2RR**: 23893.17 ❌
- **TP 3RR**: 23914.94 ❌
- **TP 4RR**: 23936.70 ❌
- **TP 15RR**: 24176.13 ❌
- **PnL**: -21.77 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 22.22 points

### Trade #1534 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 09:15:00
- **FVG 5m**: 23839.79 - 23848.88
- **Entrée**: 23849.64 @ 2025-08-27 10:47:00
- **Stop Loss**: 23827.87
- **Risk**: 21.77 points
- **TP 1RR**: 23871.40 ❌
- **TP 2RR**: 23893.17 ❌
- **TP 3RR**: 23914.94 ❌
- **TP 4RR**: 23936.70 ❌
- **TP 15RR**: 24176.13 ❌
- **PnL**: -21.77 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 22.22 points

### Trade #1535 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 10:45:00
- **FVG 5m**: 23812.52 - 23827.17
- **Entrée**: 23828.93 @ 2025-08-27 11:49:00
- **Stop Loss**: 23800.62
- **Risk**: 28.32 points
- **TP 1RR**: 23857.25 ✅
- **TP 2RR**: 23885.57 ✅
- **TP 3RR**: 23913.89 ❌
- **TP 4RR**: 23942.20 ❌
- **TP 15RR**: 24253.69 ❌
- **PnL**: -28.32 points (-1.0R)
- **MFE**: 62.87 points
- **MAE**: 32.57 points

### Trade #1536 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 11:30:00
- **FVG 5m**: 23812.52 - 23827.17
- **Entrée**: 23828.93 @ 2025-08-27 11:49:00
- **Stop Loss**: 23800.62
- **Risk**: 28.32 points
- **TP 1RR**: 23857.25 ✅
- **TP 2RR**: 23885.57 ✅
- **TP 3RR**: 23913.89 ❌
- **TP 4RR**: 23942.20 ❌
- **TP 15RR**: 24253.69 ❌
- **PnL**: -28.32 points (-1.0R)
- **MFE**: 62.87 points
- **MAE**: 32.57 points

### Trade #1537 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 13:45:00
- **FVG 5m**: 23853.42 - 23858.22
- **Entrée**: 23851.40 @ 2025-08-27 14:04:00
- **Stop Loss**: 23870.15
- **Risk**: 18.75 points
- **TP 1RR**: 23832.66 ✅
- **TP 2RR**: 23813.91 ✅
- **TP 3RR**: 23795.17 ✅
- **TP 4RR**: 23776.42 ❌
- **TP 15RR**: 23570.22 ❌
- **PnL**: -18.75 points (-1.0R)
- **MFE**: 64.63 points
- **MAE**: 25.25 points

### Trade #1538 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 13:45:00
- **FVG 5m**: 23853.42 - 23858.22
- **Entrée**: 23851.40 @ 2025-08-27 14:04:00
- **Stop Loss**: 23870.15
- **Risk**: 18.75 points
- **TP 1RR**: 23832.66 ✅
- **TP 2RR**: 23813.91 ✅
- **TP 3RR**: 23795.17 ✅
- **TP 4RR**: 23776.42 ❌
- **TP 15RR**: 23570.22 ❌
- **PnL**: -18.75 points (-1.0R)
- **MFE**: 64.63 points
- **MAE**: 25.25 points

### Trade #1539 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23860.80
- **Risk**: 52.32 points
- **TP 1RR**: 23756.16 ✅
- **TP 2RR**: 23703.84 ❌
- **TP 3RR**: 23651.52 ❌
- **TP 4RR**: 23599.20 ❌
- **TP 15RR**: 23023.67 ❌
- **PnL**: -52.32 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 61.10 points

### Trade #1540 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23860.80
- **Risk**: 52.32 points
- **TP 1RR**: 23756.16 ✅
- **TP 2RR**: 23703.84 ❌
- **TP 3RR**: 23651.52 ❌
- **TP 4RR**: 23599.20 ❌
- **TP 15RR**: 23023.67 ❌
- **PnL**: -52.32 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 61.10 points

### Trade #1541 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23860.80
- **Risk**: 52.32 points
- **TP 1RR**: 23756.16 ✅
- **TP 2RR**: 23703.84 ❌
- **TP 3RR**: 23651.52 ❌
- **TP 4RR**: 23599.20 ❌
- **TP 15RR**: 23023.67 ❌
- **PnL**: -52.32 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 61.10 points

### Trade #1542 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23860.80
- **Risk**: 52.32 points
- **TP 1RR**: 23756.16 ✅
- **TP 2RR**: 23703.84 ❌
- **TP 3RR**: 23651.52 ❌
- **TP 4RR**: 23599.20 ❌
- **TP 15RR**: 23023.67 ❌
- **PnL**: -52.32 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 61.10 points

### Trade #1543 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23860.80
- **Risk**: 52.32 points
- **TP 1RR**: 23756.16 ✅
- **TP 2RR**: 23703.84 ❌
- **TP 3RR**: 23651.52 ❌
- **TP 4RR**: 23599.20 ❌
- **TP 15RR**: 23023.67 ❌
- **PnL**: -52.32 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 61.10 points

### Trade #1544 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23753.44 - 23764.05
- **Entrée**: 23751.42 @ 2025-08-27 17:02:00
- **Stop Loss**: 23775.93
- **Risk**: 24.51 points
- **TP 1RR**: 23726.92 ✅
- **TP 2RR**: 23702.41 ❌
- **TP 3RR**: 23677.91 ❌
- **TP 4RR**: 23653.40 ❌
- **TP 15RR**: 23383.84 ❌
- **PnL**: -24.51 points (-1.0R)
- **MFE**: 31.31 points
- **MAE**: 28.28 points

### Trade #1545 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23753.44 - 23764.05
- **Entrée**: 23751.42 @ 2025-08-27 17:02:00
- **Stop Loss**: 23775.93
- **Risk**: 24.51 points
- **TP 1RR**: 23726.92 ✅
- **TP 2RR**: 23702.41 ❌
- **TP 3RR**: 23677.91 ❌
- **TP 4RR**: 23653.40 ❌
- **TP 15RR**: 23383.84 ❌
- **PnL**: -24.51 points (-1.0R)
- **MFE**: 31.31 points
- **MAE**: 28.28 points

### Trade #1546 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23753.44 - 23764.05
- **Entrée**: 23751.42 @ 2025-08-27 17:02:00
- **Stop Loss**: 23775.93
- **Risk**: 24.51 points
- **TP 1RR**: 23726.92 ✅
- **TP 2RR**: 23702.41 ❌
- **TP 3RR**: 23677.91 ❌
- **TP 4RR**: 23653.40 ❌
- **TP 15RR**: 23383.84 ❌
- **PnL**: -24.51 points (-1.0R)
- **MFE**: 31.31 points
- **MAE**: 28.28 points

### Trade #1547 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23744.86 - 23759.25
- **Entrée**: 23763.80 @ 2025-08-27 17:34:00
- **Stop Loss**: 23732.99
- **Risk**: 30.81 points
- **TP 1RR**: 23794.60 ❌
- **TP 2RR**: 23825.41 ❌
- **TP 3RR**: 23856.22 ❌
- **TP 4RR**: 23887.03 ❌
- **TP 15RR**: 24225.92 ❌
- **PnL**: -30.81 points (-1.0R)
- **MFE**: 5.05 points
- **MAE**: 35.35 points

### Trade #1548 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23744.86 - 23759.25
- **Entrée**: 23763.80 @ 2025-08-27 17:34:00
- **Stop Loss**: 23732.99
- **Risk**: 30.81 points
- **TP 1RR**: 23794.60 ❌
- **TP 2RR**: 23825.41 ❌
- **TP 3RR**: 23856.22 ❌
- **TP 4RR**: 23887.03 ❌
- **TP 15RR**: 24225.92 ❌
- **PnL**: -30.81 points (-1.0R)
- **MFE**: 5.05 points
- **MAE**: 35.35 points

### Trade #1549 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23744.86 - 23759.25
- **Entrée**: 23763.80 @ 2025-08-27 17:34:00
- **Stop Loss**: 23732.99
- **Risk**: 30.81 points
- **TP 1RR**: 23794.60 ❌
- **TP 2RR**: 23825.41 ❌
- **TP 3RR**: 23856.22 ❌
- **TP 4RR**: 23887.03 ❌
- **TP 15RR**: 24225.92 ❌
- **PnL**: -30.81 points (-1.0R)
- **MFE**: 5.05 points
- **MAE**: 35.35 points

### Trade #1550 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 08:45:00
- **FVG 5m**: 23942.04 - 23958.96
- **Entrée**: 23933.96 @ 2025-08-28 10:23:00
- **Stop Loss**: 23970.94
- **Risk**: 36.97 points
- **TP 1RR**: 23896.99 ❌
- **TP 2RR**: 23860.01 ❌
- **TP 3RR**: 23823.04 ❌
- **TP 4RR**: 23786.07 ❌
- **TP 15RR**: 23379.35 ❌
- **PnL**: -36.97 points (-1.0R)
- **MFE**: 34.59 points
- **MAE**: 38.63 points

### Trade #1551 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 08:45:00
- **FVG 5m**: 23942.04 - 23958.96
- **Entrée**: 23933.96 @ 2025-08-28 10:23:00
- **Stop Loss**: 23970.94
- **Risk**: 36.97 points
- **TP 1RR**: 23896.99 ❌
- **TP 2RR**: 23860.01 ❌
- **TP 3RR**: 23823.04 ❌
- **TP 4RR**: 23786.07 ❌
- **TP 15RR**: 23379.35 ❌
- **PnL**: -36.97 points (-1.0R)
- **MFE**: 34.59 points
- **MAE**: 38.63 points

### Trade #1552 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 10:00:00
- **FVG 5m**: 23951.13 - 23958.96
- **Entrée**: 23959.46 @ 2025-08-28 10:11:00
- **Stop Loss**: 23939.16
- **Risk**: 20.31 points
- **TP 1RR**: 23979.77 ✅
- **TP 2RR**: 24000.08 ❌
- **TP 3RR**: 24020.39 ❌
- **TP 4RR**: 24040.69 ❌
- **TP 15RR**: 24264.07 ❌
- **PnL**: -20.31 points (-1.0R)
- **MFE**: 28.53 points
- **MAE**: 26.26 points

### Trade #1553 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 10:00:00
- **FVG 5m**: 23951.13 - 23958.96
- **Entrée**: 23959.46 @ 2025-08-28 10:11:00
- **Stop Loss**: 23939.16
- **Risk**: 20.31 points
- **TP 1RR**: 23979.77 ✅
- **TP 2RR**: 24000.08 ❌
- **TP 3RR**: 24020.39 ❌
- **TP 4RR**: 24040.69 ❌
- **TP 15RR**: 24264.07 ❌
- **PnL**: -20.31 points (-1.0R)
- **MFE**: 28.53 points
- **MAE**: 26.26 points

### Trade #1554 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 11:15:00
- **FVG 5m**: 23979.66 - 23982.94
- **Entrée**: 23986.23 @ 2025-08-28 11:47:00
- **Stop Loss**: 23967.67
- **Risk**: 18.55 points
- **TP 1RR**: 24004.78 ❌
- **TP 2RR**: 24023.34 ❌
- **TP 3RR**: 24041.89 ❌
- **TP 4RR**: 24060.44 ❌
- **TP 15RR**: 24264.54 ❌
- **PnL**: -18.55 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 22.72 points

### Trade #1555 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 11:15:00
- **FVG 5m**: 23979.66 - 23982.94
- **Entrée**: 23986.23 @ 2025-08-28 11:47:00
- **Stop Loss**: 23967.67
- **Risk**: 18.55 points
- **TP 1RR**: 24004.78 ❌
- **TP 2RR**: 24023.34 ❌
- **TP 3RR**: 24041.89 ❌
- **TP 4RR**: 24060.44 ❌
- **TP 15RR**: 24264.54 ❌
- **PnL**: -18.55 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 22.72 points

### Trade #1556 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 11:15:00
- **FVG 5m**: 23979.66 - 23982.94
- **Entrée**: 23986.23 @ 2025-08-28 11:47:00
- **Stop Loss**: 23967.67
- **Risk**: 18.55 points
- **TP 1RR**: 24004.78 ❌
- **TP 2RR**: 24023.34 ❌
- **TP 3RR**: 24041.89 ❌
- **TP 4RR**: 24060.44 ❌
- **TP 15RR**: 24264.54 ❌
- **PnL**: -18.55 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 22.72 points

### Trade #1557 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 11:45:00
- **FVG 5m**: 23976.13 - 23982.94
- **Entrée**: 23973.86 @ 2025-08-28 11:57:00
- **Stop Loss**: 23994.94
- **Risk**: 21.08 points
- **TP 1RR**: 23952.77 ❌
- **TP 2RR**: 23931.69 ❌
- **TP 3RR**: 23910.61 ❌
- **TP 4RR**: 23889.53 ❌
- **TP 15RR**: 23657.65 ❌
- **PnL**: -21.08 points (-1.0R)
- **MFE**: 16.66 points
- **MAE**: 21.97 points

### Trade #1558 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 14:00:00
- **FVG 5m**: 24009.45 - 24015.77
- **Entrée**: 24002.13 @ 2025-08-28 14:59:00
- **Stop Loss**: 24027.77
- **Risk**: 25.64 points
- **TP 1RR**: 23976.49 ✅
- **TP 2RR**: 23950.85 ✅
- **TP 3RR**: 23925.21 ✅
- **TP 4RR**: 23899.57 ✅
- **TP 15RR**: 23617.51 ✅
- **PnL**: 384.62 points (15.0R)
- **MFE**: 388.06 points
- **MAE**: 7.32 points

### Trade #1559 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 14:45:00
- **FVG 5m**: 24009.45 - 24015.77
- **Entrée**: 24002.13 @ 2025-08-28 14:59:00
- **Stop Loss**: 24027.77
- **Risk**: 25.64 points
- **TP 1RR**: 23976.49 ✅
- **TP 2RR**: 23950.85 ✅
- **TP 3RR**: 23925.21 ✅
- **TP 4RR**: 23899.57 ✅
- **TP 15RR**: 23617.51 ✅
- **PnL**: 384.62 points (15.0R)
- **MFE**: 388.06 points
- **MAE**: 7.32 points

### Trade #1560 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-29 08:45:00
- **FVG 5m**: 23723.65 - 23740.06
- **Entrée**: 23714.06 @ 2025-08-29 09:04:00
- **Stop Loss**: 23751.93
- **Risk**: 37.88 points
- **TP 1RR**: 23676.18 ✅
- **TP 2RR**: 23638.31 ✅
- **TP 3RR**: 23600.43 ❌
- **TP 4RR**: 23562.56 ❌
- **TP 15RR**: 23145.93 ❌
- **PnL**: -37.88 points (-1.0R)
- **MFE**: 84.83 points
- **MAE**: 44.18 points

### Trade #1561 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-29 09:00:00
- **FVG 5m**: 23685.28 - 23702.44
- **Entrée**: 23681.99 @ 2025-08-29 09:49:00
- **Stop Loss**: 23714.29
- **Risk**: 32.30 points
- **TP 1RR**: 23649.69 ✅
- **TP 2RR**: 23617.39 ❌
- **TP 3RR**: 23585.09 ❌
- **TP 4RR**: 23552.79 ❌
- **TP 15RR**: 23197.47 ❌
- **PnL**: -32.30 points (-1.0R)
- **MFE**: 34.84 points
- **MAE**: 33.83 points

### Trade #1562 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-29 09:00:00
- **FVG 5m**: 23685.28 - 23702.44
- **Entrée**: 23681.99 @ 2025-08-29 09:49:00
- **Stop Loss**: 23714.29
- **Risk**: 32.30 points
- **TP 1RR**: 23649.69 ✅
- **TP 2RR**: 23617.39 ❌
- **TP 3RR**: 23585.09 ❌
- **TP 4RR**: 23552.79 ❌
- **TP 15RR**: 23197.47 ❌
- **PnL**: -32.30 points (-1.0R)
- **MFE**: 34.84 points
- **MAE**: 33.83 points

### Trade #1563 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 09:15:00
- **FVG 5m**: 23689.57 - 23697.14
- **Entrée**: 23697.39 @ 2025-08-29 10:07:00
- **Stop Loss**: 23677.72
- **Risk**: 19.67 points
- **TP 1RR**: 23717.07 ✅
- **TP 2RR**: 23736.74 ❌
- **TP 3RR**: 23756.41 ❌
- **TP 4RR**: 23776.08 ❌
- **TP 15RR**: 23992.47 ❌
- **PnL**: -19.67 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 29.79 points

### Trade #1564 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 09:45:00
- **FVG 5m**: 23689.57 - 23697.14
- **Entrée**: 23697.39 @ 2025-08-29 10:07:00
- **Stop Loss**: 23677.72
- **Risk**: 19.67 points
- **TP 1RR**: 23717.07 ✅
- **TP 2RR**: 23736.74 ❌
- **TP 3RR**: 23756.41 ❌
- **TP 4RR**: 23776.08 ❌
- **TP 15RR**: 23992.47 ❌
- **PnL**: -19.67 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 29.79 points

### Trade #1565 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 09:45:00
- **FVG 5m**: 23689.57 - 23697.14
- **Entrée**: 23697.39 @ 2025-08-29 10:07:00
- **Stop Loss**: 23677.72
- **Risk**: 19.67 points
- **TP 1RR**: 23717.07 ✅
- **TP 2RR**: 23736.74 ❌
- **TP 3RR**: 23756.41 ❌
- **TP 4RR**: 23776.08 ❌
- **TP 15RR**: 23992.47 ❌
- **PnL**: -19.67 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 29.79 points

### Trade #1566 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 12:15:00
- **FVG 5m**: 23669.37 - 23672.65
- **Entrée**: 23673.66 @ 2025-08-29 12:44:00
- **Stop Loss**: 23657.53
- **Risk**: 16.13 points
- **TP 1RR**: 23689.79 ✅
- **TP 2RR**: 23705.91 ✅
- **TP 3RR**: 23722.04 ✅
- **TP 4RR**: 23738.17 ✅
- **TP 15RR**: 23915.56 ❌
- **PnL**: -16.13 points (-1.0R)
- **MFE**: 112.10 points
- **MAE**: 21.46 points

### Trade #1567 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 12:15:00
- **FVG 5m**: 23669.37 - 23672.65
- **Entrée**: 23673.66 @ 2025-08-29 12:44:00
- **Stop Loss**: 23657.53
- **Risk**: 16.13 points
- **TP 1RR**: 23689.79 ✅
- **TP 2RR**: 23705.91 ✅
- **TP 3RR**: 23722.04 ✅
- **TP 4RR**: 23738.17 ✅
- **TP 15RR**: 23915.56 ❌
- **PnL**: -16.13 points (-1.0R)
- **MFE**: 112.10 points
- **MAE**: 21.46 points

### Trade #1568 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-31 21:00:00
- **FVG 5m**: 23722.39 - 23735.52
- **Entrée**: 23720.87 @ 2025-08-31 21:13:00
- **Stop Loss**: 23747.39
- **Risk**: 26.51 points
- **TP 1RR**: 23694.36 ✅
- **TP 2RR**: 23667.85 ✅
- **TP 3RR**: 23641.34 ✅
- **TP 4RR**: 23614.83 ✅
- **TP 15RR**: 23323.20 ✅
- **PnL**: 397.67 points (15.0R)
- **MFE**: 432.24 points
- **MAE**: 21.46 points

### Trade #1569 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 00:15:00
- **FVG 5m**: 23631.75 - 23652.20
- **Entrée**: 23656.24 @ 2025-09-01 01:39:00
- **Stop Loss**: 23619.93
- **Risk**: 36.31 points
- **TP 1RR**: 23692.55 ✅
- **TP 2RR**: 23728.85 ✅
- **TP 3RR**: 23765.16 ❌
- **TP 4RR**: 23801.46 ❌
- **TP 15RR**: 24200.83 ❌
- **PnL**: -36.31 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 36.86 points

### Trade #1570 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 01:30:00
- **FVG 5m**: 23656.75 - 23677.45
- **Entrée**: 23680.98 @ 2025-09-01 01:43:00
- **Stop Loss**: 23644.92
- **Risk**: 36.07 points
- **TP 1RR**: 23717.05 ✅
- **TP 2RR**: 23753.12 ❌
- **TP 3RR**: 23789.18 ❌
- **TP 4RR**: 23825.25 ❌
- **TP 15RR**: 24221.97 ❌
- **PnL**: -36.07 points (-1.0R)
- **MFE**: 61.35 points
- **MAE**: 40.40 points

### Trade #1571 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 01:30:00
- **FVG 5m**: 23656.75 - 23677.45
- **Entrée**: 23680.98 @ 2025-09-01 01:43:00
- **Stop Loss**: 23644.92
- **Risk**: 36.07 points
- **TP 1RR**: 23717.05 ✅
- **TP 2RR**: 23753.12 ❌
- **TP 3RR**: 23789.18 ❌
- **TP 4RR**: 23825.25 ❌
- **TP 15RR**: 24221.97 ❌
- **PnL**: -36.07 points (-1.0R)
- **MFE**: 61.35 points
- **MAE**: 40.40 points

### Trade #1572 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 08:30:00
- **FVG 5m**: 23724.16 - 23727.44
- **Entrée**: 23728.20 @ 2025-09-01 10:19:00
- **Stop Loss**: 23712.29
- **Risk**: 15.90 points
- **TP 1RR**: 23744.10 ❌
- **TP 2RR**: 23760.00 ❌
- **TP 3RR**: 23775.90 ❌
- **TP 4RR**: 23791.80 ❌
- **TP 15RR**: 23966.72 ❌
- **PnL**: -15.90 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 16.41 points

### Trade #1573 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 01:00:00
- **FVG 5m**: 23523.69 - 23527.48
- **Entrée**: 23536.57 @ 2025-09-02 03:02:00
- **Stop Loss**: 23511.93
- **Risk**: 24.64 points
- **TP 1RR**: 23561.21 ✅
- **TP 2RR**: 23585.84 ❌
- **TP 3RR**: 23610.48 ❌
- **TP 4RR**: 23635.12 ❌
- **TP 15RR**: 23906.14 ❌
- **PnL**: -24.64 points (-1.0R)
- **MFE**: 28.02 points
- **MAE**: 26.51 points

### Trade #1574 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 01:45:00
- **FVG 5m**: 23523.69 - 23527.48
- **Entrée**: 23536.57 @ 2025-09-02 03:02:00
- **Stop Loss**: 23511.93
- **Risk**: 24.64 points
- **TP 1RR**: 23561.21 ✅
- **TP 2RR**: 23585.84 ❌
- **TP 3RR**: 23610.48 ❌
- **TP 4RR**: 23635.12 ❌
- **TP 15RR**: 23906.14 ❌
- **PnL**: -24.64 points (-1.0R)
- **MFE**: 28.02 points
- **MAE**: 26.51 points

### Trade #1575 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 02:15:00
- **FVG 5m**: 23523.69 - 23527.48
- **Entrée**: 23536.57 @ 2025-09-02 03:02:00
- **Stop Loss**: 23511.93
- **Risk**: 24.64 points
- **TP 1RR**: 23561.21 ✅
- **TP 2RR**: 23585.84 ❌
- **TP 3RR**: 23610.48 ❌
- **TP 4RR**: 23635.12 ❌
- **TP 15RR**: 23906.14 ❌
- **PnL**: -24.64 points (-1.0R)
- **MFE**: 28.02 points
- **MAE**: 26.51 points

### Trade #1576 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:30:00
- **FVG 5m**: 23594.89 - 23603.47
- **Entrée**: 23589.33 @ 2025-09-02 02:42:00
- **Stop Loss**: 23615.27
- **Risk**: 25.94 points
- **TP 1RR**: 23563.39 ✅
- **TP 2RR**: 23537.45 ✅
- **TP 3RR**: 23511.51 ✅
- **TP 4RR**: 23485.57 ✅
- **TP 15RR**: 23200.23 ❌
- **PnL**: -25.94 points (-1.0R)
- **MFE**: 336.05 points
- **MAE**: 28.28 points

### Trade #1577 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:30:00
- **FVG 5m**: 23594.89 - 23603.47
- **Entrée**: 23589.33 @ 2025-09-02 02:42:00
- **Stop Loss**: 23615.27
- **Risk**: 25.94 points
- **TP 1RR**: 23563.39 ✅
- **TP 2RR**: 23537.45 ✅
- **TP 3RR**: 23511.51 ✅
- **TP 4RR**: 23485.57 ✅
- **TP 15RR**: 23200.23 ❌
- **PnL**: -25.94 points (-1.0R)
- **MFE**: 336.05 points
- **MAE**: 28.28 points

### Trade #1578 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:30:00
- **FVG 5m**: 23594.89 - 23603.47
- **Entrée**: 23589.33 @ 2025-09-02 02:42:00
- **Stop Loss**: 23615.27
- **Risk**: 25.94 points
- **TP 1RR**: 23563.39 ✅
- **TP 2RR**: 23537.45 ✅
- **TP 3RR**: 23511.51 ✅
- **TP 4RR**: 23485.57 ✅
- **TP 15RR**: 23200.23 ❌
- **PnL**: -25.94 points (-1.0R)
- **MFE**: 336.05 points
- **MAE**: 28.28 points

### Trade #1579 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:45:00
- **FVG 5m**: 23548.94 - 23552.22
- **Entrée**: 23548.18 @ 2025-09-02 04:44:00
- **Stop Loss**: 23564.00
- **Risk**: 15.82 points
- **TP 1RR**: 23532.37 ✅
- **TP 2RR**: 23516.55 ✅
- **TP 3RR**: 23500.73 ✅
- **TP 4RR**: 23484.92 ✅
- **TP 15RR**: 23310.94 ✅
- **PnL**: 237.24 points (15.0R)
- **MFE**: 259.55 points
- **MAE**: 0.76 points

### Trade #1580 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:45:00
- **FVG 5m**: 23548.94 - 23552.22
- **Entrée**: 23548.18 @ 2025-09-02 04:44:00
- **Stop Loss**: 23564.00
- **Risk**: 15.82 points
- **TP 1RR**: 23532.37 ✅
- **TP 2RR**: 23516.55 ✅
- **TP 3RR**: 23500.73 ✅
- **TP 4RR**: 23484.92 ✅
- **TP 15RR**: 23310.94 ✅
- **PnL**: 237.24 points (15.0R)
- **MFE**: 259.55 points
- **MAE**: 0.76 points

### Trade #1581 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 05:15:00
- **FVG 5m**: 23493.65 - 23496.17
- **Entrée**: 23480.52 @ 2025-09-02 05:28:00
- **Stop Loss**: 23507.92
- **Risk**: 27.40 points
- **TP 1RR**: 23453.12 ✅
- **TP 2RR**: 23425.71 ✅
- **TP 3RR**: 23398.31 ✅
- **TP 4RR**: 23370.91 ✅
- **TP 15RR**: 23069.49 ❌
- **PnL**: -27.40 points (-1.0R)
- **MFE**: 227.23 points
- **MAE**: 30.04 points

### Trade #1582 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 06:45:00
- **FVG 5m**: 23429.26 - 23453.00
- **Entrée**: 23424.47 @ 2025-09-02 07:02:00
- **Stop Loss**: 23464.72
- **Risk**: 40.26 points
- **TP 1RR**: 23384.21 ✅
- **TP 2RR**: 23343.96 ✅
- **TP 3RR**: 23303.70 ✅
- **TP 4RR**: 23263.44 ✅
- **TP 15RR**: 22820.62 ❌
- **PnL**: -40.26 points (-1.0R)
- **MFE**: 171.18 points
- **MAE**: 48.98 points

### Trade #1583 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 07:45:00
- **FVG 5m**: 23331.30 - 23356.05
- **Entrée**: 23367.91 @ 2025-09-02 08:36:00
- **Stop Loss**: 23319.64
- **Risk**: 48.27 points
- **TP 1RR**: 23416.19 ✅
- **TP 2RR**: 23464.46 ✅
- **TP 3RR**: 23512.74 ❌
- **TP 4RR**: 23561.01 ❌
- **TP 15RR**: 24092.03 ❌
- **PnL**: -48.27 points (-1.0R)
- **MFE**: 142.65 points
- **MAE**: 49.23 points

### Trade #1584 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 08:30:00
- **FVG 5m**: 23407.30 - 23420.18
- **Entrée**: 23424.47 @ 2025-09-02 08:48:00
- **Stop Loss**: 23395.60
- **Risk**: 28.87 points
- **TP 1RR**: 23453.34 ✅
- **TP 2RR**: 23482.21 ✅
- **TP 3RR**: 23511.08 ❌
- **TP 4RR**: 23539.96 ❌
- **TP 15RR**: 23857.55 ❌
- **PnL**: -28.87 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 42.42 points

### Trade #1585 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 09:00:00
- **FVG 5m**: 23417.65 - 23447.19
- **Entrée**: 23416.64 @ 2025-09-02 09:42:00
- **Stop Loss**: 23458.91
- **Risk**: 42.27 points
- **TP 1RR**: 23374.37 ✅
- **TP 2RR**: 23332.09 ✅
- **TP 3RR**: 23289.82 ✅
- **TP 4RR**: 23247.55 ❌
- **TP 15RR**: 22782.54 ❌
- **PnL**: -42.27 points (-1.0R)
- **MFE**: 161.58 points
- **MAE**: 46.20 points

### Trade #1586 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 09:00:00
- **FVG 5m**: 23417.65 - 23447.19
- **Entrée**: 23416.64 @ 2025-09-02 09:42:00
- **Stop Loss**: 23458.91
- **Risk**: 42.27 points
- **TP 1RR**: 23374.37 ✅
- **TP 2RR**: 23332.09 ✅
- **TP 3RR**: 23289.82 ✅
- **TP 4RR**: 23247.55 ❌
- **TP 15RR**: 22782.54 ❌
- **PnL**: -42.27 points (-1.0R)
- **MFE**: 161.58 points
- **MAE**: 46.20 points

### Trade #1587 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 14:45:00
- **FVG 5m**: 23518.39 - 23568.38
- **Entrée**: 23595.39 @ 2025-09-02 15:09:00
- **Stop Loss**: 23506.63
- **Risk**: 88.76 points
- **TP 1RR**: 23684.16 ✅
- **TP 2RR**: 23772.92 ✅
- **TP 3RR**: 23861.69 ✅
- **TP 4RR**: 23950.45 ✅
- **TP 15RR**: 24926.86 ✅
- **PnL**: 1331.47 points (15.0R)
- **MFE**: 1335.61 points
- **MAE**: 66.40 points

### Trade #1588 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 22:30:00
- **FVG 5m**: 23557.52 - 23560.30
- **Entrée**: 23560.55 @ 2025-09-02 23:17:00
- **Stop Loss**: 23545.74
- **Risk**: 14.81 points
- **TP 1RR**: 23575.36 ❌
- **TP 2RR**: 23590.17 ❌
- **TP 3RR**: 23604.98 ❌
- **TP 4RR**: 23619.79 ❌
- **TP 15RR**: 23782.68 ❌
- **PnL**: -14.81 points (-1.0R)
- **MFE**: 7.32 points
- **MAE**: 18.18 points

### Trade #1589 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-03 03:45:00
- **FVG 5m**: 23639.83 - 23645.64
- **Entrée**: 23647.66 @ 2025-09-03 04:18:00
- **Stop Loss**: 23628.01
- **Risk**: 19.65 points
- **TP 1RR**: 23667.30 ✅
- **TP 2RR**: 23686.95 ✅
- **TP 3RR**: 23706.60 ❌
- **TP 4RR**: 23726.24 ❌
- **TP 15RR**: 23942.36 ❌
- **PnL**: -19.65 points (-1.0R)
- **MFE**: 43.17 points
- **MAE**: 36.86 points

### Trade #1590 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-03 06:30:00
- **FVG 5m**: 23667.10 - 23670.63
- **Entrée**: 23674.67 @ 2025-09-03 08:06:00
- **Stop Loss**: 23655.26
- **Risk**: 19.41 points
- **TP 1RR**: 23694.08 ❌
- **TP 2RR**: 23713.49 ❌
- **TP 3RR**: 23732.89 ❌
- **TP 4RR**: 23752.30 ❌
- **TP 15RR**: 23965.79 ❌
- **PnL**: -19.41 points (-1.0R)
- **MFE**: 14.64 points
- **MAE**: 22.22 points

### Trade #1591 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 08:45:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23719.85
- **Risk**: 16.90 points
- **TP 1RR**: 23686.05 ✅
- **TP 2RR**: 23669.14 ✅
- **TP 3RR**: 23652.24 ✅
- **TP 4RR**: 23635.33 ✅
- **TP 15RR**: 23449.40 ❌
- **PnL**: -16.90 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1592 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:15:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23719.85
- **Risk**: 16.90 points
- **TP 1RR**: 23686.05 ✅
- **TP 2RR**: 23669.14 ✅
- **TP 3RR**: 23652.24 ✅
- **TP 4RR**: 23635.33 ✅
- **TP 15RR**: 23449.40 ❌
- **PnL**: -16.90 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1593 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:15:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23719.85
- **Risk**: 16.90 points
- **TP 1RR**: 23686.05 ✅
- **TP 2RR**: 23669.14 ✅
- **TP 3RR**: 23652.24 ✅
- **TP 4RR**: 23635.33 ✅
- **TP 15RR**: 23449.40 ❌
- **PnL**: -16.90 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1594 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:15:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23719.85
- **Risk**: 16.90 points
- **TP 1RR**: 23686.05 ✅
- **TP 2RR**: 23669.14 ✅
- **TP 3RR**: 23652.24 ✅
- **TP 4RR**: 23635.33 ✅
- **TP 15RR**: 23449.40 ❌
- **PnL**: -16.90 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1595 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:45:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23719.85
- **Risk**: 16.90 points
- **TP 1RR**: 23686.05 ✅
- **TP 2RR**: 23669.14 ✅
- **TP 3RR**: 23652.24 ✅
- **TP 4RR**: 23635.33 ✅
- **TP 15RR**: 23449.40 ❌
- **PnL**: -16.90 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1596 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 10:00:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23719.85
- **Risk**: 16.90 points
- **TP 1RR**: 23686.05 ✅
- **TP 2RR**: 23669.14 ✅
- **TP 3RR**: 23652.24 ✅
- **TP 4RR**: 23635.33 ✅
- **TP 15RR**: 23449.40 ❌
- **PnL**: -16.90 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1597 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 10:00:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23719.85
- **Risk**: 16.90 points
- **TP 1RR**: 23686.05 ✅
- **TP 2RR**: 23669.14 ✅
- **TP 3RR**: 23652.24 ✅
- **TP 4RR**: 23635.33 ✅
- **TP 15RR**: 23449.40 ❌
- **PnL**: -16.90 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1598 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-03 14:30:00
- **FVG 5m**: 23616.60 - 23622.66
- **Entrée**: 23628.47 @ 2025-09-03 14:44:00
- **Stop Loss**: 23604.79
- **Risk**: 23.67 points
- **TP 1RR**: 23652.14 ✅
- **TP 2RR**: 23675.82 ✅
- **TP 3RR**: 23699.49 ✅
- **TP 4RR**: 23723.17 ✅
- **TP 15RR**: 23983.59 ✅
- **PnL**: 355.12 points (15.0R)
- **MFE**: 356.50 points
- **MAE**: 5.81 points

### Trade #1599 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 21:15:00
- **FVG 5m**: 23734.26 - 23745.87
- **Entrée**: 23730.97 @ 2025-09-03 21:29:00
- **Stop Loss**: 23757.74
- **Risk**: 26.77 points
- **TP 1RR**: 23704.20 ✅
- **TP 2RR**: 23677.44 ❌
- **TP 3RR**: 23650.67 ❌
- **TP 4RR**: 23623.90 ❌
- **TP 15RR**: 23329.44 ❌
- **PnL**: -26.77 points (-1.0R)
- **MFE**: 47.72 points
- **MAE**: 28.53 points

### Trade #1600 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 21:45:00
- **FVG 5m**: 23714.81 - 23720.62
- **Entrée**: 23712.80 @ 2025-09-03 21:59:00
- **Stop Loss**: 23732.48
- **Risk**: 19.69 points
- **TP 1RR**: 23693.11 ✅
- **TP 2RR**: 23673.42 ❌
- **TP 3RR**: 23653.73 ❌
- **TP 4RR**: 23634.05 ❌
- **TP 15RR**: 23417.49 ❌
- **PnL**: -19.69 points (-1.0R)
- **MFE**: 21.46 points
- **MAE**: 21.46 points

### Trade #1601 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 22:15:00
- **FVG 5m**: 23704.46 - 23707.24
- **Entrée**: 23703.20 @ 2025-09-03 22:29:00
- **Stop Loss**: 23719.09
- **Risk**: 15.89 points
- **TP 1RR**: 23687.31 ❌
- **TP 2RR**: 23671.41 ❌
- **TP 3RR**: 23655.52 ❌
- **TP 4RR**: 23639.63 ❌
- **TP 15RR**: 23464.80 ❌
- **PnL**: -15.89 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 18.18 points

### Trade #1602 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 05:15:00
- **FVG 5m**: 23724.91 - 23742.08
- **Entrée**: 23722.14 @ 2025-09-04 07:19:00
- **Stop Loss**: 23753.95
- **Risk**: 31.82 points
- **TP 1RR**: 23690.32 ✅
- **TP 2RR**: 23658.50 ❌
- **TP 3RR**: 23626.69 ❌
- **TP 4RR**: 23594.87 ❌
- **TP 15RR**: 23244.89 ❌
- **PnL**: -31.82 points (-1.0R)
- **MFE**: 32.57 points
- **MAE**: 33.83 points

### Trade #1603 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 06:15:00
- **FVG 5m**: 23724.91 - 23742.08
- **Entrée**: 23722.14 @ 2025-09-04 07:19:00
- **Stop Loss**: 23753.95
- **Risk**: 31.82 points
- **TP 1RR**: 23690.32 ✅
- **TP 2RR**: 23658.50 ❌
- **TP 3RR**: 23626.69 ❌
- **TP 4RR**: 23594.87 ❌
- **TP 15RR**: 23244.89 ❌
- **PnL**: -31.82 points (-1.0R)
- **MFE**: 32.57 points
- **MAE**: 33.83 points

### Trade #1604 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 08:30:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23671.39 @ 2025-09-04 09:03:00
- **Stop Loss**: 23703.18
- **Risk**: 31.79 points
- **TP 1RR**: 23639.60 ❌
- **TP 2RR**: 23607.81 ❌
- **TP 3RR**: 23576.02 ❌
- **TP 4RR**: 23544.22 ❌
- **TP 15RR**: 23194.52 ❌
- **PnL**: -31.79 points (-1.0R)
- **MFE**: 18.43 points
- **MAE**: 31.81 points

### Trade #1605 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 08:30:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23671.39 @ 2025-09-04 09:03:00
- **Stop Loss**: 23703.18
- **Risk**: 31.79 points
- **TP 1RR**: 23639.60 ❌
- **TP 2RR**: 23607.81 ❌
- **TP 3RR**: 23576.02 ❌
- **TP 4RR**: 23544.22 ❌
- **TP 15RR**: 23194.52 ❌
- **PnL**: -31.79 points (-1.0R)
- **MFE**: 18.43 points
- **MAE**: 31.81 points

### Trade #1606 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 08:30:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23671.39 @ 2025-09-04 09:03:00
- **Stop Loss**: 23703.18
- **Risk**: 31.79 points
- **TP 1RR**: 23639.60 ❌
- **TP 2RR**: 23607.81 ❌
- **TP 3RR**: 23576.02 ❌
- **TP 4RR**: 23544.22 ❌
- **TP 15RR**: 23194.52 ❌
- **PnL**: -31.79 points (-1.0R)
- **MFE**: 18.43 points
- **MAE**: 31.81 points

### Trade #1607 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 09:15:00
- **FVG 5m**: 23727.19 - 23730.22
- **Entrée**: 23737.29 @ 2025-09-04 09:32:00
- **Stop Loss**: 23715.32
- **Risk**: 21.96 points
- **TP 1RR**: 23759.25 ✅
- **TP 2RR**: 23781.21 ✅
- **TP 3RR**: 23803.17 ✅
- **TP 4RR**: 23825.14 ✅
- **TP 15RR**: 24066.72 ✅
- **PnL**: 329.44 points (15.0R)
- **MFE**: 329.48 points
- **MAE**: 14.14 points

### Trade #1608 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 09:15:00
- **FVG 5m**: 23727.19 - 23730.22
- **Entrée**: 23737.29 @ 2025-09-04 09:32:00
- **Stop Loss**: 23715.32
- **Risk**: 21.96 points
- **TP 1RR**: 23759.25 ✅
- **TP 2RR**: 23781.21 ✅
- **TP 3RR**: 23803.17 ✅
- **TP 4RR**: 23825.14 ✅
- **TP 15RR**: 24066.72 ✅
- **PnL**: 329.44 points (15.0R)
- **MFE**: 329.48 points
- **MAE**: 14.14 points

### Trade #1609 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 09:15:00
- **FVG 5m**: 23727.19 - 23730.22
- **Entrée**: 23737.29 @ 2025-09-04 09:32:00
- **Stop Loss**: 23715.32
- **Risk**: 21.96 points
- **TP 1RR**: 23759.25 ✅
- **TP 2RR**: 23781.21 ✅
- **TP 3RR**: 23803.17 ✅
- **TP 4RR**: 23825.14 ✅
- **TP 15RR**: 24066.72 ✅
- **PnL**: 329.44 points (15.0R)
- **MFE**: 329.48 points
- **MAE**: 14.14 points

### Trade #1610 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 10:15:00
- **FVG 5m**: 23774.15 - 23777.18
- **Entrée**: 23777.43 @ 2025-09-04 11:08:00
- **Stop Loss**: 23762.26
- **Risk**: 15.17 points
- **TP 1RR**: 23792.60 ❌
- **TP 2RR**: 23807.77 ❌
- **TP 3RR**: 23822.94 ❌
- **TP 4RR**: 23838.11 ❌
- **TP 15RR**: 24004.97 ❌
- **PnL**: -15.17 points (-1.0R)
- **MFE**: 8.84 points
- **MAE**: 15.65 points

### Trade #1611 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 12:15:00
- **FVG 5m**: 23838.28 - 23844.34
- **Entrée**: 23845.09 @ 2025-09-04 13:33:00
- **Stop Loss**: 23826.36
- **Risk**: 18.74 points
- **TP 1RR**: 23863.83 ✅
- **TP 2RR**: 23882.56 ✅
- **TP 3RR**: 23901.30 ✅
- **TP 4RR**: 23920.04 ✅
- **TP 15RR**: 24126.13 ✅
- **PnL**: 281.04 points (15.0R)
- **MFE**: 281.26 points
- **MAE**: 6.31 points

### Trade #1612 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 12:45:00
- **FVG 5m**: 23838.28 - 23844.34
- **Entrée**: 23845.09 @ 2025-09-04 13:33:00
- **Stop Loss**: 23826.36
- **Risk**: 18.74 points
- **TP 1RR**: 23863.83 ✅
- **TP 2RR**: 23882.56 ✅
- **TP 3RR**: 23901.30 ✅
- **TP 4RR**: 23920.04 ✅
- **TP 15RR**: 24126.13 ✅
- **PnL**: 281.04 points (15.0R)
- **MFE**: 281.26 points
- **MAE**: 6.31 points

### Trade #1613 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-05 07:30:00
- **FVG 5m**: 24067.02 - 24074.09
- **Entrée**: 24076.36 @ 2025-09-05 07:49:00
- **Stop Loss**: 24054.99
- **Risk**: 21.38 points
- **TP 1RR**: 24097.74 ✅
- **TP 2RR**: 24119.11 ✅
- **TP 3RR**: 24140.49 ❌
- **TP 4RR**: 24161.86 ❌
- **TP 15RR**: 24396.99 ❌
- **PnL**: -21.38 points (-1.0R)
- **MFE**: 62.36 points
- **MAE**: 29.54 points

### Trade #1614 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-05 07:30:00
- **FVG 5m**: 24067.02 - 24074.09
- **Entrée**: 24076.36 @ 2025-09-05 07:49:00
- **Stop Loss**: 24054.99
- **Risk**: 21.38 points
- **TP 1RR**: 24097.74 ✅
- **TP 2RR**: 24119.11 ✅
- **TP 3RR**: 24140.49 ❌
- **TP 4RR**: 24161.86 ❌
- **TP 15RR**: 24396.99 ❌
- **PnL**: -21.38 points (-1.0R)
- **MFE**: 62.36 points
- **MAE**: 29.54 points

### Trade #1615 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-05 07:45:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 24120.29 @ 2025-09-05 08:03:00
- **Stop Loss**: 24099.40
- **Risk**: 20.89 points
- **TP 1RR**: 24141.18 ❌
- **TP 2RR**: 24162.08 ❌
- **TP 3RR**: 24182.97 ❌
- **TP 4RR**: 24203.86 ❌
- **TP 15RR**: 24433.68 ❌
- **PnL**: -20.89 points (-1.0R)
- **MFE**: 18.43 points
- **MAE**: 31.56 points

### Trade #1616 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 08:15:00
- **FVG 5m**: 24092.01 - 24107.42
- **Entrée**: 24089.99 @ 2025-09-05 08:32:00
- **Stop Loss**: 24119.47
- **Risk**: 29.47 points
- **TP 1RR**: 24060.52 ✅
- **TP 2RR**: 24031.05 ❌
- **TP 3RR**: 24001.57 ❌
- **TP 4RR**: 23972.10 ❌
- **TP 15RR**: 23647.88 ❌
- **PnL**: -29.47 points (-1.0R)
- **MFE**: 32.32 points
- **MAE**: 33.83 points

### Trade #1617 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24033.58
- **Risk**: 42.06 points
- **TP 1RR**: 23949.47 ✅
- **TP 2RR**: 23907.42 ✅
- **TP 3RR**: 23865.36 ✅
- **TP 4RR**: 23823.31 ✅
- **TP 15RR**: 23360.70 ❌
- **PnL**: -42.06 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 56.30 points

### Trade #1618 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24033.58
- **Risk**: 42.06 points
- **TP 1RR**: 23949.47 ✅
- **TP 2RR**: 23907.42 ✅
- **TP 3RR**: 23865.36 ✅
- **TP 4RR**: 23823.31 ✅
- **TP 15RR**: 23360.70 ❌
- **PnL**: -42.06 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 56.30 points

### Trade #1619 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24033.58
- **Risk**: 42.06 points
- **TP 1RR**: 23949.47 ✅
- **TP 2RR**: 23907.42 ✅
- **TP 3RR**: 23865.36 ✅
- **TP 4RR**: 23823.31 ✅
- **TP 15RR**: 23360.70 ❌
- **PnL**: -42.06 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 56.30 points

### Trade #1620 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24033.58
- **Risk**: 42.06 points
- **TP 1RR**: 23949.47 ✅
- **TP 2RR**: 23907.42 ✅
- **TP 3RR**: 23865.36 ✅
- **TP 4RR**: 23823.31 ✅
- **TP 15RR**: 23360.70 ❌
- **PnL**: -42.06 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 56.30 points

### Trade #1621 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24033.58
- **Risk**: 42.06 points
- **TP 1RR**: 23949.47 ✅
- **TP 2RR**: 23907.42 ✅
- **TP 3RR**: 23865.36 ✅
- **TP 4RR**: 23823.31 ✅
- **TP 15RR**: 23360.70 ❌
- **PnL**: -42.06 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 56.30 points

### Trade #1622 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24033.58
- **Risk**: 42.06 points
- **TP 1RR**: 23949.47 ✅
- **TP 2RR**: 23907.42 ✅
- **TP 3RR**: 23865.36 ✅
- **TP 4RR**: 23823.31 ✅
- **TP 15RR**: 23360.70 ❌
- **PnL**: -42.06 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 56.30 points

### Trade #1623 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-07 17:30:00
- **FVG 5m**: 23951.89 - 23963.50
- **Entrée**: 23974.11 @ 2025-09-07 17:45:00
- **Stop Loss**: 23939.91
- **Risk**: 34.19 points
- **TP 1RR**: 24008.30 ✅
- **TP 2RR**: 24042.50 ✅
- **TP 3RR**: 24076.69 ✅
- **TP 4RR**: 24110.88 ✅
- **TP 15RR**: 24487.02 ✅
- **PnL**: 512.91 points (15.0R)
- **MFE**: 518.64 points
- **MAE**: 14.64 points

### Trade #1624 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-07 17:30:00
- **FVG 5m**: 23951.89 - 23963.50
- **Entrée**: 23974.11 @ 2025-09-07 17:45:00
- **Stop Loss**: 23939.91
- **Risk**: 34.19 points
- **TP 1RR**: 24008.30 ✅
- **TP 2RR**: 24042.50 ✅
- **TP 3RR**: 24076.69 ✅
- **TP 4RR**: 24110.88 ✅
- **TP 15RR**: 24487.02 ✅
- **PnL**: 512.91 points (15.0R)
- **MFE**: 518.64 points
- **MAE**: 14.64 points

### Trade #1625 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-07 21:00:00
- **FVG 5m**: 23980.17 - 23987.74
- **Entrée**: 23979.41 @ 2025-09-07 21:18:00
- **Stop Loss**: 23999.74
- **Risk**: 20.33 points
- **TP 1RR**: 23959.08 ❌
- **TP 2RR**: 23938.76 ❌
- **TP 3RR**: 23918.43 ❌
- **TP 4RR**: 23898.11 ❌
- **TP 15RR**: 23674.53 ❌
- **PnL**: -20.33 points (-1.0R)
- **MFE**: 19.95 points
- **MAE**: 21.46 points

### Trade #1626 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 08:45:00
- **FVG 5m**: 24066.77 - 24074.85
- **Entrée**: 24064.49 @ 2025-09-08 09:17:00
- **Stop Loss**: 24086.88
- **Risk**: 22.39 points
- **TP 1RR**: 24042.11 ✅
- **TP 2RR**: 24019.72 ❌
- **TP 3RR**: 23997.33 ❌
- **TP 4RR**: 23974.94 ❌
- **TP 15RR**: 23728.66 ❌
- **PnL**: -22.39 points (-1.0R)
- **MFE**: 22.47 points
- **MAE**: 31.31 points

### Trade #1627 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 12:00:00
- **FVG 5m**: 24011.22 - 24022.08
- **Entrée**: 24004.66 @ 2025-09-08 14:12:00
- **Stop Loss**: 24034.09
- **Risk**: 29.43 points
- **TP 1RR**: 23975.23 ❌
- **TP 2RR**: 23945.79 ❌
- **TP 3RR**: 23916.36 ❌
- **TP 4RR**: 23886.93 ❌
- **TP 15RR**: 23563.18 ❌
- **PnL**: -29.43 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 32.32 points

### Trade #1628 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 12:00:00
- **FVG 5m**: 24011.22 - 24022.08
- **Entrée**: 24004.66 @ 2025-09-08 14:12:00
- **Stop Loss**: 24034.09
- **Risk**: 29.43 points
- **TP 1RR**: 23975.23 ❌
- **TP 2RR**: 23945.79 ❌
- **TP 3RR**: 23916.36 ❌
- **TP 4RR**: 23886.93 ❌
- **TP 15RR**: 23563.18 ❌
- **PnL**: -29.43 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 32.32 points

### Trade #1629 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 14:00:00
- **FVG 5m**: 24011.22 - 24022.08
- **Entrée**: 24004.66 @ 2025-09-08 14:12:00
- **Stop Loss**: 24034.09
- **Risk**: 29.43 points
- **TP 1RR**: 23975.23 ❌
- **TP 2RR**: 23945.79 ❌
- **TP 3RR**: 23916.36 ❌
- **TP 4RR**: 23886.93 ❌
- **TP 15RR**: 23563.18 ❌
- **PnL**: -29.43 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 32.32 points

### Trade #1630 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-09 00:15:00
- **FVG 5m**: 24094.03 - 24107.67
- **Entrée**: 24092.27 @ 2025-09-09 02:44:00
- **Stop Loss**: 24119.72
- **Risk**: 27.45 points
- **TP 1RR**: 24064.81 ✅
- **TP 2RR**: 24037.36 ✅
- **TP 3RR**: 24009.90 ✅
- **TP 4RR**: 23982.45 ✅
- **TP 15RR**: 23680.44 ❌
- **PnL**: -27.45 points (-1.0R)
- **MFE**: 131.29 points
- **MAE**: 34.34 points

### Trade #1631 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 06:30:00
- **FVG 5m**: 24073.08 - 24081.41
- **Entrée**: 24081.92 @ 2025-09-09 06:48:00
- **Stop Loss**: 24061.04
- **Risk**: 20.87 points
- **TP 1RR**: 24102.79 ❌
- **TP 2RR**: 24123.66 ❌
- **TP 3RR**: 24144.53 ❌
- **TP 4RR**: 24165.41 ❌
- **TP 15RR**: 24395.01 ❌
- **PnL**: -20.87 points (-1.0R)
- **MFE**: 11.61 points
- **MAE**: 45.95 points

### Trade #1632 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 08:00:00
- **FVG 5m**: 23999.86 - 24021.32
- **Entrée**: 24023.09 @ 2025-09-09 09:54:00
- **Stop Loss**: 23987.86
- **Risk**: 35.23 points
- **TP 1RR**: 24058.32 ❌
- **TP 2RR**: 24093.54 ❌
- **TP 3RR**: 24128.77 ❌
- **TP 4RR**: 24164.00 ❌
- **TP 15RR**: 24551.50 ❌
- **PnL**: -35.23 points (-1.0R)
- **MFE**: 16.41 points
- **MAE**: 35.85 points

### Trade #1633 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-09 08:45:00
- **FVG 5m**: 24048.08 - 24050.86
- **Entrée**: 24037.98 @ 2025-09-09 09:26:00
- **Stop Loss**: 24062.89
- **Risk**: 24.90 points
- **TP 1RR**: 24013.08 ✅
- **TP 2RR**: 23988.18 ✅
- **TP 3RR**: 23963.28 ✅
- **TP 4RR**: 23938.38 ❌
- **TP 15RR**: 23664.46 ❌
- **PnL**: -24.90 points (-1.0R)
- **MFE**: 77.01 points
- **MAE**: 26.26 points

### Trade #1634 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:00:00
- **FVG 5m**: 23999.86 - 24021.32
- **Entrée**: 24023.09 @ 2025-09-09 09:54:00
- **Stop Loss**: 23987.86
- **Risk**: 35.23 points
- **TP 1RR**: 24058.32 ❌
- **TP 2RR**: 24093.54 ❌
- **TP 3RR**: 24128.77 ❌
- **TP 4RR**: 24164.00 ❌
- **TP 15RR**: 24551.50 ❌
- **PnL**: -35.23 points (-1.0R)
- **MFE**: 16.41 points
- **MAE**: 35.85 points

### Trade #1635 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:30:00
- **FVG 5m**: 23999.86 - 24021.32
- **Entrée**: 24023.09 @ 2025-09-09 09:54:00
- **Stop Loss**: 23987.86
- **Risk**: 35.23 points
- **TP 1RR**: 24058.32 ❌
- **TP 2RR**: 24093.54 ❌
- **TP 3RR**: 24128.77 ❌
- **TP 4RR**: 24164.00 ❌
- **TP 15RR**: 24551.50 ❌
- **PnL**: -35.23 points (-1.0R)
- **MFE**: 16.41 points
- **MAE**: 35.85 points

### Trade #1636 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:30:00
- **FVG 5m**: 23999.86 - 24021.32
- **Entrée**: 24023.09 @ 2025-09-09 09:54:00
- **Stop Loss**: 23987.86
- **Risk**: 35.23 points
- **TP 1RR**: 24058.32 ❌
- **TP 2RR**: 24093.54 ❌
- **TP 3RR**: 24128.77 ❌
- **TP 4RR**: 24164.00 ❌
- **TP 15RR**: 24551.50 ❌
- **PnL**: -35.23 points (-1.0R)
- **MFE**: 16.41 points
- **MAE**: 35.85 points

### Trade #1637 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:45:00
- **FVG 5m**: 24011.22 - 24019.30
- **Entrée**: 24027.13 @ 2025-09-09 10:52:00
- **Stop Loss**: 23999.22
- **Risk**: 27.91 points
- **TP 1RR**: 24055.04 ✅
- **TP 2RR**: 24082.95 ✅
- **TP 3RR**: 24110.86 ✅
- **TP 4RR**: 24138.77 ✅
- **TP 15RR**: 24445.80 ✅
- **PnL**: 418.67 points (15.0R)
- **MFE**: 426.12 points
- **MAE**: 10.10 points

### Trade #1638 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:45:00
- **FVG 5m**: 24011.22 - 24019.30
- **Entrée**: 24027.13 @ 2025-09-09 10:52:00
- **Stop Loss**: 23999.22
- **Risk**: 27.91 points
- **TP 1RR**: 24055.04 ✅
- **TP 2RR**: 24082.95 ✅
- **TP 3RR**: 24110.86 ✅
- **TP 4RR**: 24138.77 ✅
- **TP 15RR**: 24445.80 ✅
- **PnL**: 418.67 points (15.0R)
- **MFE**: 426.12 points
- **MAE**: 10.10 points

### Trade #1639 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-09 14:30:00
- **FVG 5m**: 24128.12 - 24135.69
- **Entrée**: 24126.35 @ 2025-09-09 15:54:00
- **Stop Loss**: 24147.76
- **Risk**: 21.41 points
- **TP 1RR**: 24104.94 ❌
- **TP 2RR**: 24083.53 ❌
- **TP 3RR**: 24062.12 ❌
- **TP 4RR**: 24040.71 ❌
- **TP 15RR**: 23805.21 ❌
- **PnL**: -21.41 points (-1.0R)
- **MFE**: 5.05 points
- **MAE**: 21.97 points

### Trade #1640 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 03:15:00
- **FVG 5m**: 24136.95 - 24146.80
- **Entrée**: 24130.64 @ 2025-09-10 03:33:00
- **Stop Loss**: 24158.87
- **Risk**: 28.23 points
- **TP 1RR**: 24102.41 ❌
- **TP 2RR**: 24074.18 ❌
- **TP 3RR**: 24045.95 ❌
- **TP 4RR**: 24017.72 ❌
- **TP 15RR**: 23707.16 ❌
- **PnL**: -28.23 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 29.03 points

### Trade #1641 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 07:30:00
- **FVG 5m**: 24227.59 - 24235.17
- **Entrée**: 24225.32 @ 2025-09-10 08:01:00
- **Stop Loss**: 24247.29
- **Risk**: 21.96 points
- **TP 1RR**: 24203.36 ❌
- **TP 2RR**: 24181.39 ❌
- **TP 3RR**: 24159.43 ❌
- **TP 4RR**: 24137.46 ❌
- **TP 15RR**: 23895.86 ❌
- **PnL**: -21.96 points (-1.0R)
- **MFE**: 10.10 points
- **MAE**: 22.47 points

### Trade #1642 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 07:30:00
- **FVG 5m**: 24227.59 - 24235.17
- **Entrée**: 24225.32 @ 2025-09-10 08:01:00
- **Stop Loss**: 24247.29
- **Risk**: 21.96 points
- **TP 1RR**: 24203.36 ❌
- **TP 2RR**: 24181.39 ❌
- **TP 3RR**: 24159.43 ❌
- **TP 4RR**: 24137.46 ❌
- **TP 15RR**: 23895.86 ❌
- **PnL**: -21.96 points (-1.0R)
- **MFE**: 10.10 points
- **MAE**: 22.47 points

### Trade #1643 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 07:30:00
- **FVG 5m**: 24227.59 - 24235.42
- **Entrée**: 24238.70 @ 2025-09-10 08:12:00
- **Stop Loss**: 24215.48
- **Risk**: 23.22 points
- **TP 1RR**: 24261.93 ❌
- **TP 2RR**: 24285.15 ❌
- **TP 3RR**: 24308.37 ❌
- **TP 4RR**: 24331.59 ❌
- **TP 15RR**: 24587.04 ❌
- **PnL**: -23.22 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 60.34 points

### Trade #1644 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24215.46
- **Risk**: 39.62 points
- **TP 1RR**: 24136.21 ✅
- **TP 2RR**: 24096.59 ✅
- **TP 3RR**: 24056.97 ✅
- **TP 4RR**: 24017.35 ❌
- **TP 15RR**: 23581.51 ❌
- **PnL**: -39.62 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 39.64 points

### Trade #1645 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24215.46
- **Risk**: 39.62 points
- **TP 1RR**: 24136.21 ✅
- **TP 2RR**: 24096.59 ✅
- **TP 3RR**: 24056.97 ✅
- **TP 4RR**: 24017.35 ❌
- **TP 15RR**: 23581.51 ❌
- **PnL**: -39.62 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 39.64 points

### Trade #1646 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24215.46
- **Risk**: 39.62 points
- **TP 1RR**: 24136.21 ✅
- **TP 2RR**: 24096.59 ✅
- **TP 3RR**: 24056.97 ✅
- **TP 4RR**: 24017.35 ❌
- **TP 15RR**: 23581.51 ❌
- **PnL**: -39.62 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 39.64 points

### Trade #1647 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24215.46
- **Risk**: 39.62 points
- **TP 1RR**: 24136.21 ✅
- **TP 2RR**: 24096.59 ✅
- **TP 3RR**: 24056.97 ✅
- **TP 4RR**: 24017.35 ❌
- **TP 15RR**: 23581.51 ❌
- **PnL**: -39.62 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 39.64 points

### Trade #1648 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24215.46
- **Risk**: 39.62 points
- **TP 1RR**: 24136.21 ✅
- **TP 2RR**: 24096.59 ✅
- **TP 3RR**: 24056.97 ✅
- **TP 4RR**: 24017.35 ❌
- **TP 15RR**: 23581.51 ❌
- **PnL**: -39.62 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 39.64 points

### Trade #1649 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 08:45:00
- **FVG 5m**: 24173.06 - 24182.15
- **Entrée**: 24188.96 @ 2025-09-10 09:01:00
- **Stop Loss**: 24160.97
- **Risk**: 27.99 points
- **TP 1RR**: 24216.96 ✅
- **TP 2RR**: 24244.95 ❌
- **TP 3RR**: 24272.94 ❌
- **TP 4RR**: 24300.93 ❌
- **TP 15RR**: 24608.85 ❌
- **PnL**: -27.99 points (-1.0R)
- **MFE**: 39.64 points
- **MAE**: 29.54 points

### Trade #1650 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24153.62 - 24159.93
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24172.01
- **Risk**: 23.19 points
- **TP 1RR**: 24125.63 ✅
- **TP 2RR**: 24102.44 ✅
- **TP 3RR**: 24079.25 ✅
- **TP 4RR**: 24056.07 ✅
- **TP 15RR**: 23800.99 ❌
- **PnL**: -23.19 points (-1.0R)
- **MFE**: 128.26 points
- **MAE**: 23.99 points

### Trade #1651 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24153.62 - 24159.93
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24172.01
- **Risk**: 23.19 points
- **TP 1RR**: 24125.63 ✅
- **TP 2RR**: 24102.44 ✅
- **TP 3RR**: 24079.25 ✅
- **TP 4RR**: 24056.07 ✅
- **TP 15RR**: 23800.99 ❌
- **PnL**: -23.19 points (-1.0R)
- **MFE**: 128.26 points
- **MAE**: 23.99 points

### Trade #1652 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24153.62 - 24159.93
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24172.01
- **Risk**: 23.19 points
- **TP 1RR**: 24125.63 ✅
- **TP 2RR**: 24102.44 ✅
- **TP 3RR**: 24079.25 ✅
- **TP 4RR**: 24056.07 ✅
- **TP 15RR**: 23800.99 ❌
- **PnL**: -23.19 points (-1.0R)
- **MFE**: 128.26 points
- **MAE**: 23.99 points

### Trade #1653 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24153.62 - 24159.93
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24172.01
- **Risk**: 23.19 points
- **TP 1RR**: 24125.63 ✅
- **TP 2RR**: 24102.44 ✅
- **TP 3RR**: 24079.25 ✅
- **TP 4RR**: 24056.07 ✅
- **TP 15RR**: 23800.99 ❌
- **PnL**: -23.19 points (-1.0R)
- **MFE**: 128.26 points
- **MAE**: 23.99 points

### Trade #1654 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 11:45:00
- **FVG 5m**: 24151.85 - 24156.65
- **Entrée**: 24161.44 @ 2025-09-10 11:57:00
- **Stop Loss**: 24139.77
- **Risk**: 21.67 points
- **TP 1RR**: 24183.11 ❌
- **TP 2RR**: 24204.78 ❌
- **TP 3RR**: 24226.45 ❌
- **TP 4RR**: 24248.12 ❌
- **TP 15RR**: 24486.50 ❌
- **PnL**: -21.67 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 29.29 points

### Trade #1655 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 12:15:00
- **FVG 5m**: 24107.67 - 24112.46
- **Entrée**: 24097.32 @ 2025-09-10 13:19:00
- **Stop Loss**: 24124.52
- **Risk**: 27.20 points
- **TP 1RR**: 24070.11 ✅
- **TP 2RR**: 24042.91 ✅
- **TP 3RR**: 24015.70 ❌
- **TP 4RR**: 23988.50 ❌
- **TP 15RR**: 23689.24 ❌
- **PnL**: -27.20 points (-1.0R)
- **MFE**: 76.75 points
- **MAE**: 32.32 points

### Trade #1656 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 12:15:00
- **FVG 5m**: 24107.67 - 24112.46
- **Entrée**: 24097.32 @ 2025-09-10 13:19:00
- **Stop Loss**: 24124.52
- **Risk**: 27.20 points
- **TP 1RR**: 24070.11 ✅
- **TP 2RR**: 24042.91 ✅
- **TP 3RR**: 24015.70 ❌
- **TP 4RR**: 23988.50 ❌
- **TP 15RR**: 23689.24 ❌
- **PnL**: -27.20 points (-1.0R)
- **MFE**: 76.75 points
- **MAE**: 32.32 points

### Trade #1657 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 12:15:00
- **FVG 5m**: 24107.67 - 24112.46
- **Entrée**: 24097.32 @ 2025-09-10 13:19:00
- **Stop Loss**: 24124.52
- **Risk**: 27.20 points
- **TP 1RR**: 24070.11 ✅
- **TP 2RR**: 24042.91 ✅
- **TP 3RR**: 24015.70 ❌
- **TP 4RR**: 23988.50 ❌
- **TP 15RR**: 23689.24 ❌
- **PnL**: -27.20 points (-1.0R)
- **MFE**: 76.75 points
- **MAE**: 32.32 points

### Trade #1658 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 13:15:00
- **FVG 5m**: 24084.69 - 24096.56
- **Entrée**: 24082.17 @ 2025-09-10 13:47:00
- **Stop Loss**: 24108.61
- **Risk**: 26.44 points
- **TP 1RR**: 24055.73 ✅
- **TP 2RR**: 24029.29 ✅
- **TP 3RR**: 24002.85 ❌
- **TP 4RR**: 23976.41 ❌
- **TP 15RR**: 23685.58 ❌
- **PnL**: -26.44 points (-1.0R)
- **MFE**: 61.60 points
- **MAE**: 35.60 points

### Trade #1659 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 14:45:00
- **FVG 5m**: 24099.34 - 24106.66
- **Entrée**: 24107.67 @ 2025-09-10 17:03:00
- **Stop Loss**: 24087.29
- **Risk**: 20.38 points
- **TP 1RR**: 24128.05 ✅
- **TP 2RR**: 24148.43 ✅
- **TP 3RR**: 24168.81 ✅
- **TP 4RR**: 24189.19 ✅
- **TP 15RR**: 24413.39 ❌
- **PnL**: -20.38 points (-1.0R)
- **MFE**: 103.77 points
- **MAE**: 33.58 points

### Trade #1660 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 19:00:00
- **FVG 5m**: 24120.29 - 24123.83
- **Entrée**: 24117.51 @ 2025-09-10 19:15:00
- **Stop Loss**: 24135.89
- **Risk**: 18.37 points
- **TP 1RR**: 24099.14 ❌
- **TP 2RR**: 24080.77 ❌
- **TP 3RR**: 24062.39 ❌
- **TP 4RR**: 24044.02 ❌
- **TP 15RR**: 23841.91 ❌
- **PnL**: -18.37 points (-1.0R)
- **MFE**: 9.59 points
- **MAE**: 19.19 points

### Trade #1661 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 19:30:00
- **FVG 5m**: 24144.02 - 24146.55
- **Entrée**: 24147.31 @ 2025-09-10 21:27:00
- **Stop Loss**: 24131.95
- **Risk**: 15.35 points
- **TP 1RR**: 24162.66 ❌
- **TP 2RR**: 24178.01 ❌
- **TP 3RR**: 24193.37 ❌
- **TP 4RR**: 24208.72 ❌
- **TP 15RR**: 24377.62 ❌
- **PnL**: -15.35 points (-1.0R)
- **MFE**: 8.58 points
- **MAE**: 20.45 points

### Trade #1662 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24183.16 - 24205.12
- **Entrée**: 24172.05 @ 2025-09-11 08:39:00
- **Stop Loss**: 24217.23
- **Risk**: 45.18 points
- **TP 1RR**: 24126.87 ❌
- **TP 2RR**: 24081.70 ❌
- **TP 3RR**: 24036.52 ❌
- **TP 4RR**: 23991.34 ❌
- **TP 15RR**: 23494.40 ❌
- **PnL**: -45.18 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 49.23 points

### Trade #1663 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24149.87
- **Risk**: 24.45 points
- **TP 1RR**: 24198.77 ✅
- **TP 2RR**: 24223.23 ✅
- **TP 3RR**: 24247.68 ❌
- **TP 4RR**: 24272.13 ❌
- **TP 15RR**: 24541.11 ❌
- **PnL**: -24.45 points (-1.0R)
- **MFE**: 60.85 points
- **MAE**: 26.51 points

### Trade #1664 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24149.87
- **Risk**: 24.45 points
- **TP 1RR**: 24198.77 ✅
- **TP 2RR**: 24223.23 ✅
- **TP 3RR**: 24247.68 ❌
- **TP 4RR**: 24272.13 ❌
- **TP 15RR**: 24541.11 ❌
- **PnL**: -24.45 points (-1.0R)
- **MFE**: 60.85 points
- **MAE**: 26.51 points

### Trade #1665 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24149.87
- **Risk**: 24.45 points
- **TP 1RR**: 24198.77 ✅
- **TP 2RR**: 24223.23 ✅
- **TP 3RR**: 24247.68 ❌
- **TP 4RR**: 24272.13 ❌
- **TP 15RR**: 24541.11 ❌
- **PnL**: -24.45 points (-1.0R)
- **MFE**: 60.85 points
- **MAE**: 26.51 points

### Trade #1666 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24149.87
- **Risk**: 24.45 points
- **TP 1RR**: 24198.77 ✅
- **TP 2RR**: 24223.23 ✅
- **TP 3RR**: 24247.68 ❌
- **TP 4RR**: 24272.13 ❌
- **TP 15RR**: 24541.11 ❌
- **PnL**: -24.45 points (-1.0R)
- **MFE**: 60.85 points
- **MAE**: 26.51 points

### Trade #1667 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24149.87
- **Risk**: 24.45 points
- **TP 1RR**: 24198.77 ✅
- **TP 2RR**: 24223.23 ✅
- **TP 3RR**: 24247.68 ❌
- **TP 4RR**: 24272.13 ❌
- **TP 15RR**: 24541.11 ❌
- **PnL**: -24.45 points (-1.0R)
- **MFE**: 60.85 points
- **MAE**: 26.51 points

### Trade #1668 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-11 09:45:00
- **FVG 5m**: 24266.22 - 24274.30
- **Entrée**: 24263.45 @ 2025-09-11 10:38:00
- **Stop Loss**: 24286.44
- **Risk**: 22.99 points
- **TP 1RR**: 24240.45 ✅
- **TP 2RR**: 24217.46 ✅
- **TP 3RR**: 24194.46 ❌
- **TP 4RR**: 24171.47 ❌
- **TP 15RR**: 23918.54 ❌
- **PnL**: -22.99 points (-1.0R)
- **MFE**: 57.06 points
- **MAE**: 23.48 points

### Trade #1669 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 08:30:00
- **FVG 5m**: 24334.39 - 24338.94
- **Entrée**: 24333.13 @ 2025-09-12 10:02:00
- **Stop Loss**: 24351.11
- **Risk**: 17.98 points
- **TP 1RR**: 24315.15 ✅
- **TP 2RR**: 24297.18 ❌
- **TP 3RR**: 24279.20 ❌
- **TP 4RR**: 24261.22 ❌
- **TP 15RR**: 24063.48 ❌
- **PnL**: -17.98 points (-1.0R)
- **MFE**: 22.98 points
- **MAE**: 19.69 points

### Trade #1670 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 08:30:00
- **FVG 5m**: 24334.39 - 24338.94
- **Entrée**: 24333.13 @ 2025-09-12 10:02:00
- **Stop Loss**: 24351.11
- **Risk**: 17.98 points
- **TP 1RR**: 24315.15 ✅
- **TP 2RR**: 24297.18 ❌
- **TP 3RR**: 24279.20 ❌
- **TP 4RR**: 24261.22 ❌
- **TP 15RR**: 24063.48 ❌
- **PnL**: -17.98 points (-1.0R)
- **MFE**: 22.98 points
- **MAE**: 19.69 points

### Trade #1671 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 08:30:00
- **FVG 5m**: 24334.39 - 24338.94
- **Entrée**: 24333.13 @ 2025-09-12 10:02:00
- **Stop Loss**: 24351.11
- **Risk**: 17.98 points
- **TP 1RR**: 24315.15 ✅
- **TP 2RR**: 24297.18 ❌
- **TP 3RR**: 24279.20 ❌
- **TP 4RR**: 24261.22 ❌
- **TP 15RR**: 24063.48 ❌
- **PnL**: -17.98 points (-1.0R)
- **MFE**: 22.98 points
- **MAE**: 19.69 points

### Trade #1672 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 08:30:00
- **FVG 5m**: 24334.39 - 24338.94
- **Entrée**: 24333.13 @ 2025-09-12 10:02:00
- **Stop Loss**: 24351.11
- **Risk**: 17.98 points
- **TP 1RR**: 24315.15 ✅
- **TP 2RR**: 24297.18 ❌
- **TP 3RR**: 24279.20 ❌
- **TP 4RR**: 24261.22 ❌
- **TP 15RR**: 24063.48 ❌
- **PnL**: -17.98 points (-1.0R)
- **MFE**: 22.98 points
- **MAE**: 19.69 points

### Trade #1673 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 14:45:00
- **FVG 5m**: 24350.55 - 24356.86
- **Entrée**: 24349.29 @ 2025-09-12 14:59:00
- **Stop Loss**: 24369.04
- **Risk**: 19.75 points
- **TP 1RR**: 24329.53 ❌
- **TP 2RR**: 24309.78 ❌
- **TP 3RR**: 24290.03 ❌
- **TP 4RR**: 24270.28 ❌
- **TP 15RR**: 24053.00 ❌
- **PnL**: -19.75 points (-1.0R)
- **MFE**: 18.68 points
- **MAE**: 20.45 points

### Trade #1674 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 03:00:00
- **FVG 5m**: 24336.00 - 24340.75
- **Entrée**: 24335.25 @ 2025-09-15 03:56:00
- **Stop Loss**: 24352.92
- **Risk**: 17.67 points
- **TP 1RR**: 24317.58 ❌
- **TP 2RR**: 24299.91 ❌
- **TP 3RR**: 24282.24 ❌
- **TP 4RR**: 24264.57 ❌
- **TP 15RR**: 24070.19 ❌
- **PnL**: -17.67 points (-1.0R)
- **MFE**: 15.25 points
- **MAE**: 18.00 points

### Trade #1675 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-15 03:00:00
- **FVG 5m**: 24336.00 - 24339.75
- **Entrée**: 24340.25 @ 2025-09-15 03:42:00
- **Stop Loss**: 24323.83
- **Risk**: 16.42 points
- **TP 1RR**: 24356.67 ❌
- **TP 2RR**: 24373.09 ❌
- **TP 3RR**: 24389.50 ❌
- **TP 4RR**: 24405.92 ❌
- **TP 15RR**: 24586.52 ❌
- **PnL**: -16.42 points (-1.0R)
- **MFE**: 16.00 points
- **MAE**: 17.00 points

### Trade #1676 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-15 03:00:00
- **FVG 5m**: 24336.00 - 24339.75
- **Entrée**: 24340.25 @ 2025-09-15 03:42:00
- **Stop Loss**: 24323.83
- **Risk**: 16.42 points
- **TP 1RR**: 24356.67 ❌
- **TP 2RR**: 24373.09 ❌
- **TP 3RR**: 24389.50 ❌
- **TP 4RR**: 24405.92 ❌
- **TP 15RR**: 24586.52 ❌
- **PnL**: -16.42 points (-1.0R)
- **MFE**: 16.00 points
- **MAE**: 17.00 points

### Trade #1677 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 07:15:00
- **FVG 5m**: 24392.25 - 24396.50
- **Entrée**: 24388.75 @ 2025-09-15 07:31:00
- **Stop Loss**: 24408.70
- **Risk**: 19.95 points
- **TP 1RR**: 24368.80 ❌
- **TP 2RR**: 24348.85 ❌
- **TP 3RR**: 24328.91 ❌
- **TP 4RR**: 24308.96 ❌
- **TP 15RR**: 24089.53 ❌
- **PnL**: -19.95 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 21.50 points

### Trade #1678 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 07:15:00
- **FVG 5m**: 24392.25 - 24396.50
- **Entrée**: 24388.75 @ 2025-09-15 07:31:00
- **Stop Loss**: 24408.70
- **Risk**: 19.95 points
- **TP 1RR**: 24368.80 ❌
- **TP 2RR**: 24348.85 ❌
- **TP 3RR**: 24328.91 ❌
- **TP 4RR**: 24308.96 ❌
- **TP 15RR**: 24089.53 ❌
- **PnL**: -19.95 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 21.50 points

### Trade #1679 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 15:00:00
- **FVG 5m**: 24537.00 - 24539.50
- **Entrée**: 24530.00 @ 2025-09-15 17:01:00
- **Stop Loss**: 24551.77
- **Risk**: 21.77 points
- **TP 1RR**: 24508.23 ❌
- **TP 2RR**: 24486.46 ❌
- **TP 3RR**: 24464.69 ❌
- **TP 4RR**: 24442.92 ❌
- **TP 15RR**: 24203.45 ❌
- **PnL**: -21.77 points (-1.0R)
- **MFE**: 6.00 points
- **MAE**: 26.25 points

### Trade #1680 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 15:00:00
- **FVG 5m**: 24537.00 - 24539.50
- **Entrée**: 24530.00 @ 2025-09-15 17:01:00
- **Stop Loss**: 24551.77
- **Risk**: 21.77 points
- **TP 1RR**: 24508.23 ❌
- **TP 2RR**: 24486.46 ❌
- **TP 3RR**: 24464.69 ❌
- **TP 4RR**: 24442.92 ❌
- **TP 15RR**: 24203.45 ❌
- **PnL**: -21.77 points (-1.0R)
- **MFE**: 6.00 points
- **MAE**: 26.25 points

### Trade #1681 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-16 08:15:00
- **FVG 5m**: 24578.75 - 24586.00
- **Entrée**: 24570.50 @ 2025-09-16 08:33:00
- **Stop Loss**: 24598.29
- **Risk**: 27.79 points
- **TP 1RR**: 24542.71 ✅
- **TP 2RR**: 24514.91 ✅
- **TP 3RR**: 24487.12 ✅
- **TP 4RR**: 24459.33 ✅
- **TP 15RR**: 24153.60 ❌
- **PnL**: -27.79 points (-1.0R)
- **MFE**: 328.50 points
- **MAE**: 29.25 points

### Trade #1682 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-16 08:45:00
- **FVG 5m**: 24530.00 - 24535.00
- **Entrée**: 24522.25 @ 2025-09-16 10:01:00
- **Stop Loss**: 24547.27
- **Risk**: 25.02 points
- **TP 1RR**: 24497.23 ❌
- **TP 2RR**: 24472.21 ❌
- **TP 3RR**: 24447.20 ❌
- **TP 4RR**: 24422.18 ❌
- **TP 15RR**: 24146.99 ❌
- **PnL**: -25.02 points (-1.0R)
- **MFE**: 23.00 points
- **MAE**: 25.25 points

### Trade #1683 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-16 08:45:00
- **FVG 5m**: 24530.00 - 24535.00
- **Entrée**: 24522.25 @ 2025-09-16 10:01:00
- **Stop Loss**: 24547.27
- **Risk**: 25.02 points
- **TP 1RR**: 24497.23 ❌
- **TP 2RR**: 24472.21 ❌
- **TP 3RR**: 24447.20 ❌
- **TP 4RR**: 24422.18 ❌
- **TP 15RR**: 24146.99 ❌
- **PnL**: -25.02 points (-1.0R)
- **MFE**: 23.00 points
- **MAE**: 25.25 points

### Trade #1684 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-16 14:45:00
- **FVG 5m**: 24535.00 - 24538.25
- **Entrée**: 24531.25 @ 2025-09-16 15:58:00
- **Stop Loss**: 24550.52
- **Risk**: 19.27 points
- **TP 1RR**: 24511.98 ❌
- **TP 2RR**: 24492.71 ❌
- **TP 3RR**: 24473.44 ❌
- **TP 4RR**: 24454.17 ❌
- **TP 15RR**: 24242.21 ❌
- **PnL**: -19.27 points (-1.0R)
- **MFE**: 6.25 points
- **MAE**: 20.50 points

### Trade #1685 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 03:45:00
- **FVG 5m**: 24514.75 - 24517.50
- **Entrée**: 24517.75 @ 2025-09-17 04:04:00
- **Stop Loss**: 24502.49
- **Risk**: 15.26 points
- **TP 1RR**: 24533.01 ❌
- **TP 2RR**: 24548.26 ❌
- **TP 3RR**: 24563.52 ❌
- **TP 4RR**: 24578.78 ❌
- **TP 15RR**: 24746.61 ❌
- **PnL**: -15.26 points (-1.0R)
- **MFE**: 10.75 points
- **MAE**: 16.25 points

### Trade #1686 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 03:45:00
- **FVG 5m**: 24514.75 - 24517.50
- **Entrée**: 24517.75 @ 2025-09-17 04:04:00
- **Stop Loss**: 24502.49
- **Risk**: 15.26 points
- **TP 1RR**: 24533.01 ❌
- **TP 2RR**: 24548.26 ❌
- **TP 3RR**: 24563.52 ❌
- **TP 4RR**: 24578.78 ❌
- **TP 15RR**: 24746.61 ❌
- **PnL**: -15.26 points (-1.0R)
- **MFE**: 10.75 points
- **MAE**: 16.25 points

### Trade #1687 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 06:00:00
- **FVG 5m**: 24496.25 - 24501.25
- **Entrée**: 24501.50 @ 2025-09-17 06:48:00
- **Stop Loss**: 24484.00
- **Risk**: 17.50 points
- **TP 1RR**: 24519.00 ✅
- **TP 2RR**: 24536.50 ✅
- **TP 3RR**: 24553.99 ❌
- **TP 4RR**: 24571.49 ❌
- **TP 15RR**: 24763.97 ❌
- **PnL**: -17.50 points (-1.0R)
- **MFE**: 39.25 points
- **MAE**: 19.75 points

### Trade #1688 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24354.00 - 24382.75
- **Entrée**: 24393.00 @ 2025-09-17 13:59:00
- **Stop Loss**: 24341.82
- **Risk**: 51.18 points
- **TP 1RR**: 24444.18 ✅
- **TP 2RR**: 24495.35 ✅
- **TP 3RR**: 24546.53 ✅
- **TP 4RR**: 24597.71 ✅
- **TP 15RR**: 25160.65 ✅
- **PnL**: 767.65 points (15.0R)
- **MFE**: 768.00 points
- **MAE**: 10.25 points

### Trade #1689 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24354.00 - 24382.75
- **Entrée**: 24393.00 @ 2025-09-17 13:59:00
- **Stop Loss**: 24341.82
- **Risk**: 51.18 points
- **TP 1RR**: 24444.18 ✅
- **TP 2RR**: 24495.35 ✅
- **TP 3RR**: 24546.53 ✅
- **TP 4RR**: 24597.71 ✅
- **TP 15RR**: 25160.65 ✅
- **PnL**: 767.65 points (15.0R)
- **MFE**: 768.00 points
- **MAE**: 10.25 points

### Trade #1690 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24354.00 - 24382.75
- **Entrée**: 24393.00 @ 2025-09-17 13:59:00
- **Stop Loss**: 24341.82
- **Risk**: 51.18 points
- **TP 1RR**: 24444.18 ✅
- **TP 2RR**: 24495.35 ✅
- **TP 3RR**: 24546.53 ✅
- **TP 4RR**: 24597.71 ✅
- **TP 15RR**: 25160.65 ✅
- **PnL**: 767.65 points (15.0R)
- **MFE**: 768.00 points
- **MAE**: 10.25 points

### Trade #1691 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24354.00 - 24382.75
- **Entrée**: 24393.00 @ 2025-09-17 13:59:00
- **Stop Loss**: 24341.82
- **Risk**: 51.18 points
- **TP 1RR**: 24444.18 ✅
- **TP 2RR**: 24495.35 ✅
- **TP 3RR**: 24546.53 ✅
- **TP 4RR**: 24597.71 ✅
- **TP 15RR**: 25160.65 ✅
- **PnL**: 767.65 points (15.0R)
- **MFE**: 768.00 points
- **MAE**: 10.25 points

### Trade #1692 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24501.00 - 24505.50
- **Entrée**: 24506.25 @ 2025-09-17 15:28:00
- **Stop Loss**: 24488.75
- **Risk**: 17.50 points
- **TP 1RR**: 24523.75 ❌
- **TP 2RR**: 24541.25 ❌
- **TP 3RR**: 24558.75 ❌
- **TP 4RR**: 24576.25 ❌
- **TP 15RR**: 24768.76 ❌
- **PnL**: -17.50 points (-1.0R)
- **MFE**: 11.00 points
- **MAE**: 18.75 points

### Trade #1693 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24501.00 - 24505.50
- **Entrée**: 24506.25 @ 2025-09-17 15:28:00
- **Stop Loss**: 24488.75
- **Risk**: 17.50 points
- **TP 1RR**: 24523.75 ❌
- **TP 2RR**: 24541.25 ❌
- **TP 3RR**: 24558.75 ❌
- **TP 4RR**: 24576.25 ❌
- **TP 15RR**: 24768.76 ❌
- **PnL**: -17.50 points (-1.0R)
- **MFE**: 11.00 points
- **MAE**: 18.75 points

### Trade #1694 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24501.00 - 24505.50
- **Entrée**: 24506.25 @ 2025-09-17 15:28:00
- **Stop Loss**: 24488.75
- **Risk**: 17.50 points
- **TP 1RR**: 24523.75 ❌
- **TP 2RR**: 24541.25 ❌
- **TP 3RR**: 24558.75 ❌
- **TP 4RR**: 24576.25 ❌
- **TP 15RR**: 24768.76 ❌
- **PnL**: -17.50 points (-1.0R)
- **MFE**: 11.00 points
- **MAE**: 18.75 points

### Trade #1695 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24501.00 - 24505.50
- **Entrée**: 24506.25 @ 2025-09-17 15:28:00
- **Stop Loss**: 24488.75
- **Risk**: 17.50 points
- **TP 1RR**: 24523.75 ❌
- **TP 2RR**: 24541.25 ❌
- **TP 3RR**: 24558.75 ❌
- **TP 4RR**: 24576.25 ❌
- **TP 15RR**: 24768.76 ❌
- **PnL**: -17.50 points (-1.0R)
- **MFE**: 11.00 points
- **MAE**: 18.75 points

### Trade #1696 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 20:00:00
- **FVG 5m**: 24593.00 - 24596.50
- **Entrée**: 24597.00 @ 2025-09-17 21:13:00
- **Stop Loss**: 24580.70
- **Risk**: 16.30 points
- **TP 1RR**: 24613.30 ✅
- **TP 2RR**: 24629.59 ✅
- **TP 3RR**: 24645.89 ✅
- **TP 4RR**: 24662.19 ✅
- **TP 15RR**: 24841.45 ✅
- **PnL**: 244.45 points (15.0R)
- **MFE**: 253.50 points
- **MAE**: 10.50 points

### Trade #1697 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 07:30:00
- **FVG 5m**: 24716.00 - 24729.75
- **Entrée**: 24713.25 @ 2025-09-18 07:53:00
- **Stop Loss**: 24742.11
- **Risk**: 28.86 points
- **TP 1RR**: 24684.39 ✅
- **TP 2RR**: 24655.52 ✅
- **TP 3RR**: 24626.66 ✅
- **TP 4RR**: 24597.79 ❌
- **TP 15RR**: 24280.28 ❌
- **PnL**: -28.86 points (-1.0R)
- **MFE**: 114.50 points
- **MAE**: 34.50 points

### Trade #1698 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 08:30:00
- **FVG 5m**: 24657.75 - 24666.50
- **Entrée**: 24656.75 @ 2025-09-18 08:49:00
- **Stop Loss**: 24678.83
- **Risk**: 22.08 points
- **TP 1RR**: 24634.67 ❌
- **TP 2RR**: 24612.58 ❌
- **TP 3RR**: 24590.50 ❌
- **TP 4RR**: 24568.42 ❌
- **TP 15RR**: 24325.50 ❌
- **PnL**: -22.08 points (-1.0R)
- **MFE**: 1.00 points
- **MAE**: 35.75 points

### Trade #1699 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 08:30:00
- **FVG 5m**: 24657.75 - 24666.50
- **Entrée**: 24656.75 @ 2025-09-18 08:49:00
- **Stop Loss**: 24678.83
- **Risk**: 22.08 points
- **TP 1RR**: 24634.67 ❌
- **TP 2RR**: 24612.58 ❌
- **TP 3RR**: 24590.50 ❌
- **TP 4RR**: 24568.42 ❌
- **TP 15RR**: 24325.50 ❌
- **PnL**: -22.08 points (-1.0R)
- **MFE**: 1.00 points
- **MAE**: 35.75 points

### Trade #1700 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 08:45:00
- **FVG 5m**: 24698.50 - 24721.75
- **Entrée**: 24722.00 @ 2025-09-18 09:04:00
- **Stop Loss**: 24686.15
- **Risk**: 35.85 points
- **TP 1RR**: 24757.85 ✅
- **TP 2RR**: 24793.70 ✅
- **TP 3RR**: 24829.55 ❌
- **TP 4RR**: 24865.40 ❌
- **TP 15RR**: 25259.74 ❌
- **PnL**: -35.85 points (-1.0R)
- **MFE**: 94.00 points
- **MAE**: 37.00 points

### Trade #1701 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 08:45:00
- **FVG 5m**: 24698.50 - 24721.75
- **Entrée**: 24722.00 @ 2025-09-18 09:04:00
- **Stop Loss**: 24686.15
- **Risk**: 35.85 points
- **TP 1RR**: 24757.85 ✅
- **TP 2RR**: 24793.70 ✅
- **TP 3RR**: 24829.55 ❌
- **TP 4RR**: 24865.40 ❌
- **TP 15RR**: 25259.74 ❌
- **PnL**: -35.85 points (-1.0R)
- **MFE**: 94.00 points
- **MAE**: 37.00 points

### Trade #1702 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 09:30:00
- **FVG 5m**: 24777.00 - 24781.00
- **Entrée**: 24772.75 @ 2025-09-18 10:42:00
- **Stop Loss**: 24793.39
- **Risk**: 20.64 points
- **TP 1RR**: 24752.11 ✅
- **TP 2RR**: 24731.47 ✅
- **TP 3RR**: 24710.83 ❌
- **TP 4RR**: 24690.19 ❌
- **TP 15RR**: 24463.14 ❌
- **PnL**: -20.64 points (-1.0R)
- **MFE**: 52.00 points
- **MAE**: 23.25 points

### Trade #1703 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 22:00:00
- **FVG 5m**: 24721.50 - 24730.00
- **Entrée**: 24730.75 @ 2025-09-18 22:11:00
- **Stop Loss**: 24709.14
- **Risk**: 21.61 points
- **TP 1RR**: 24752.36 ❌
- **TP 2RR**: 24773.97 ❌
- **TP 3RR**: 24795.58 ❌
- **TP 4RR**: 24817.19 ❌
- **TP 15RR**: 25054.91 ❌
- **PnL**: -21.61 points (-1.0R)
- **MFE**: 6.75 points
- **MAE**: 26.25 points

### Trade #1704 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 23:15:00
- **FVG 5m**: 24696.00 - 24702.75
- **Entrée**: 24703.00 @ 2025-09-18 23:28:00
- **Stop Loss**: 24683.65
- **Risk**: 19.35 points
- **TP 1RR**: 24722.35 ✅
- **TP 2RR**: 24741.70 ❌
- **TP 3RR**: 24761.04 ❌
- **TP 4RR**: 24780.39 ❌
- **TP 15RR**: 24993.22 ❌
- **PnL**: -19.35 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 23.75 points

### Trade #1705 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 23:15:00
- **FVG 5m**: 24696.00 - 24702.75
- **Entrée**: 24703.00 @ 2025-09-18 23:28:00
- **Stop Loss**: 24683.65
- **Risk**: 19.35 points
- **TP 1RR**: 24722.35 ✅
- **TP 2RR**: 24741.70 ❌
- **TP 3RR**: 24761.04 ❌
- **TP 4RR**: 24780.39 ❌
- **TP 15RR**: 24993.22 ❌
- **PnL**: -19.35 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 23.75 points

### Trade #1706 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-19 02:15:00
- **FVG 5m**: 24715.25 - 24719.50
- **Entrée**: 24720.50 @ 2025-09-19 04:23:00
- **Stop Loss**: 24702.89
- **Risk**: 17.61 points
- **TP 1RR**: 24738.11 ❌
- **TP 2RR**: 24755.72 ❌
- **TP 3RR**: 24773.32 ❌
- **TP 4RR**: 24790.93 ❌
- **TP 15RR**: 24984.61 ❌
- **PnL**: -17.61 points (-1.0R)
- **MFE**: 9.25 points
- **MAE**: 20.25 points

### Trade #1707 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-19 02:15:00
- **FVG 5m**: 24715.25 - 24719.50
- **Entrée**: 24720.50 @ 2025-09-19 04:23:00
- **Stop Loss**: 24702.89
- **Risk**: 17.61 points
- **TP 1RR**: 24738.11 ❌
- **TP 2RR**: 24755.72 ❌
- **TP 3RR**: 24773.32 ❌
- **TP 4RR**: 24790.93 ❌
- **TP 15RR**: 24984.61 ❌
- **PnL**: -17.61 points (-1.0R)
- **MFE**: 9.25 points
- **MAE**: 20.25 points

### Trade #1708 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 08:15:00
- **FVG 5m**: 24761.75 - 24765.00
- **Entrée**: 24759.75 @ 2025-09-19 08:32:00
- **Stop Loss**: 24777.38
- **Risk**: 17.63 points
- **TP 1RR**: 24742.12 ✅
- **TP 2RR**: 24724.49 ❌
- **TP 3RR**: 24706.85 ❌
- **TP 4RR**: 24689.22 ❌
- **TP 15RR**: 24495.26 ❌
- **PnL**: -17.63 points (-1.0R)
- **MFE**: 22.25 points
- **MAE**: 22.25 points

### Trade #1709 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 08:45:00
- **FVG 5m**: 24760.75 - 24766.25
- **Entrée**: 24759.00 @ 2025-09-19 09:41:00
- **Stop Loss**: 24778.63
- **Risk**: 19.63 points
- **TP 1RR**: 24739.37 ✅
- **TP 2RR**: 24719.73 ✅
- **TP 3RR**: 24700.10 ❌
- **TP 4RR**: 24680.47 ❌
- **TP 15RR**: 24464.50 ❌
- **PnL**: -19.63 points (-1.0R)
- **MFE**: 51.00 points
- **MAE**: 20.75 points

### Trade #1710 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 10:00:00
- **FVG 5m**: 24811.25 - 24817.25
- **Entrée**: 24806.75 @ 2025-09-19 12:10:00
- **Stop Loss**: 24829.66
- **Risk**: 22.91 points
- **TP 1RR**: 24783.84 ❌
- **TP 2RR**: 24760.93 ❌
- **TP 3RR**: 24738.02 ❌
- **TP 4RR**: 24715.12 ❌
- **TP 15RR**: 24463.12 ❌
- **PnL**: -22.91 points (-1.0R)
- **MFE**: 11.25 points
- **MAE**: 26.25 points

### Trade #1711 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 10:00:00
- **FVG 5m**: 24811.25 - 24817.25
- **Entrée**: 24806.75 @ 2025-09-19 12:10:00
- **Stop Loss**: 24829.66
- **Risk**: 22.91 points
- **TP 1RR**: 24783.84 ❌
- **TP 2RR**: 24760.93 ❌
- **TP 3RR**: 24738.02 ❌
- **TP 4RR**: 24715.12 ❌
- **TP 15RR**: 24463.12 ❌
- **PnL**: -22.91 points (-1.0R)
- **MFE**: 11.25 points
- **MAE**: 26.25 points

### Trade #1712 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-19 10:30:00
- **FVG 5m**: 24735.00 - 24744.00
- **Entrée**: 24747.50 @ 2025-09-19 10:43:00
- **Stop Loss**: 24722.63
- **Risk**: 24.87 points
- **TP 1RR**: 24772.37 ✅
- **TP 2RR**: 24797.24 ✅
- **TP 3RR**: 24822.10 ✅
- **TP 4RR**: 24846.97 ✅
- **TP 15RR**: 25120.51 ❌
- **PnL**: -24.87 points (-1.0R)
- **MFE**: 279.75 points
- **MAE**: 26.75 points

### Trade #1713 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 12:45:00
- **FVG 5m**: 24816.00 - 24820.00
- **Entrée**: 24814.25 @ 2025-09-19 13:47:00
- **Stop Loss**: 24832.41
- **Risk**: 18.16 points
- **TP 1RR**: 24796.09 ❌
- **TP 2RR**: 24777.93 ❌
- **TP 3RR**: 24759.77 ❌
- **TP 4RR**: 24741.61 ❌
- **TP 15RR**: 24541.85 ❌
- **PnL**: -18.16 points (-1.0R)
- **MFE**: 7.00 points
- **MAE**: 23.75 points

### Trade #1714 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-22 02:00:00
- **FVG 5m**: 24791.25 - 24797.25
- **Entrée**: 24785.50 @ 2025-09-22 02:18:00
- **Stop Loss**: 24809.65
- **Risk**: 24.15 points
- **TP 1RR**: 24761.35 ✅
- **TP 2RR**: 24737.20 ❌
- **TP 3RR**: 24713.05 ❌
- **TP 4RR**: 24688.91 ❌
- **TP 15RR**: 24423.27 ❌
- **PnL**: -24.15 points (-1.0R)
- **MFE**: 36.75 points
- **MAE**: 25.25 points

### Trade #1715 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-22 08:30:00
- **FVG 5m**: 24849.00 - 24855.25
- **Entrée**: 24859.00 @ 2025-09-22 08:48:00
- **Stop Loss**: 24836.58
- **Risk**: 22.42 points
- **TP 1RR**: 24881.42 ✅
- **TP 2RR**: 24903.85 ✅
- **TP 3RR**: 24926.27 ✅
- **TP 4RR**: 24948.70 ✅
- **TP 15RR**: 25195.37 ❌
- **PnL**: -22.42 points (-1.0R)
- **MFE**: 168.25 points
- **MAE**: 27.75 points

### Trade #1716 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-22 08:30:00
- **FVG 5m**: 24849.00 - 24855.25
- **Entrée**: 24859.00 @ 2025-09-22 08:48:00
- **Stop Loss**: 24836.58
- **Risk**: 22.42 points
- **TP 1RR**: 24881.42 ✅
- **TP 2RR**: 24903.85 ✅
- **TP 3RR**: 24926.27 ✅
- **TP 4RR**: 24948.70 ✅
- **TP 15RR**: 25195.37 ❌
- **PnL**: -22.42 points (-1.0R)
- **MFE**: 168.25 points
- **MAE**: 27.75 points

### Trade #1717 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-23 11:00:00
- **FVG 5m**: 24930.75 - 24941.75
- **Entrée**: 24944.25 @ 2025-09-23 11:19:00
- **Stop Loss**: 24918.28
- **Risk**: 25.97 points
- **TP 1RR**: 24970.22 ❌
- **TP 2RR**: 24996.18 ❌
- **TP 3RR**: 25022.15 ❌
- **TP 4RR**: 25048.11 ❌
- **TP 15RR**: 25333.73 ❌
- **PnL**: -25.97 points (-1.0R)
- **MFE**: 10.25 points
- **MAE**: 27.25 points

### Trade #1718 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-23 12:15:00
- **FVG 5m**: 24880.00 - 24895.50
- **Entrée**: 24872.50 @ 2025-09-23 12:27:00
- **Stop Loss**: 24907.95
- **Risk**: 35.45 points
- **TP 1RR**: 24837.05 ✅
- **TP 2RR**: 24801.60 ✅
- **TP 3RR**: 24766.16 ❌
- **TP 4RR**: 24730.71 ❌
- **TP 15RR**: 24340.78 ❌
- **PnL**: -35.45 points (-1.0R)
- **MFE**: 92.00 points
- **MAE**: 35.75 points

### Trade #1719 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-23 12:15:00
- **FVG 5m**: 24880.00 - 24895.50
- **Entrée**: 24872.50 @ 2025-09-23 12:27:00
- **Stop Loss**: 24907.95
- **Risk**: 35.45 points
- **TP 1RR**: 24837.05 ✅
- **TP 2RR**: 24801.60 ✅
- **TP 3RR**: 24766.16 ❌
- **TP 4RR**: 24730.71 ❌
- **TP 15RR**: 24340.78 ❌
- **PnL**: -35.45 points (-1.0R)
- **MFE**: 92.00 points
- **MAE**: 35.75 points

### Trade #1720 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 11:15:00
- **FVG 5m**: 24701.00 - 24714.00
- **Entrée**: 24716.75 @ 2025-09-24 12:09:00
- **Stop Loss**: 24688.65
- **Risk**: 28.10 points
- **TP 1RR**: 24744.85 ✅
- **TP 2RR**: 24772.95 ❌
- **TP 3RR**: 24801.05 ❌
- **TP 4RR**: 24829.15 ❌
- **TP 15RR**: 25138.26 ❌
- **PnL**: -28.10 points (-1.0R)
- **MFE**: 42.25 points
- **MAE**: 34.00 points

### Trade #1721 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 12:00:00
- **FVG 5m**: 24728.00 - 24732.00
- **Entrée**: 24740.75 @ 2025-09-24 12:30:00
- **Stop Loss**: 24715.64
- **Risk**: 25.11 points
- **TP 1RR**: 24765.86 ❌
- **TP 2RR**: 24790.98 ❌
- **TP 3RR**: 24816.09 ❌
- **TP 4RR**: 24841.21 ❌
- **TP 15RR**: 25117.46 ❌
- **PnL**: -25.11 points (-1.0R)
- **MFE**: 18.25 points
- **MAE**: 29.50 points

### Trade #1722 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 12:00:00
- **FVG 5m**: 24728.00 - 24732.00
- **Entrée**: 24740.75 @ 2025-09-24 12:30:00
- **Stop Loss**: 24715.64
- **Risk**: 25.11 points
- **TP 1RR**: 24765.86 ❌
- **TP 2RR**: 24790.98 ❌
- **TP 3RR**: 24816.09 ❌
- **TP 4RR**: 24841.21 ❌
- **TP 15RR**: 25117.46 ❌
- **PnL**: -25.11 points (-1.0R)
- **MFE**: 18.25 points
- **MAE**: 29.50 points

### Trade #1723 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 19:00:00
- **FVG 5m**: 24782.75 - 24785.75
- **Entrée**: 24787.50 @ 2025-09-24 20:48:00
- **Stop Loss**: 24770.36
- **Risk**: 17.14 points
- **TP 1RR**: 24804.64 ❌
- **TP 2RR**: 24821.78 ❌
- **TP 3RR**: 24838.92 ❌
- **TP 4RR**: 24856.07 ❌
- **TP 15RR**: 25044.62 ❌
- **PnL**: -17.14 points (-1.0R)
- **MFE**: 6.00 points
- **MAE**: 17.75 points

### Trade #1724 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 02:30:00
- **FVG 5m**: 24740.00 - 24748.25
- **Entrée**: 24751.00 @ 2025-09-25 03:02:00
- **Stop Loss**: 24727.63
- **Risk**: 23.37 points
- **TP 1RR**: 24774.37 ❌
- **TP 2RR**: 24797.74 ❌
- **TP 3RR**: 24821.11 ❌
- **TP 4RR**: 24844.48 ❌
- **TP 15RR**: 25101.55 ❌
- **PnL**: -23.37 points (-1.0R)
- **MFE**: 13.00 points
- **MAE**: 24.75 points

### Trade #1725 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 07:45:00
- **FVG 5m**: 24560.00 - 24576.25
- **Entrée**: 24581.00 @ 2025-09-25 08:19:00
- **Stop Loss**: 24547.72
- **Risk**: 33.28 points
- **TP 1RR**: 24614.28 ❌
- **TP 2RR**: 24647.56 ❌
- **TP 3RR**: 24680.84 ❌
- **TP 4RR**: 24714.12 ❌
- **TP 15RR**: 25080.20 ❌
- **PnL**: -33.28 points (-1.0R)
- **MFE**: 6.00 points
- **MAE**: 49.25 points

### Trade #1726 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-25 08:30:00
- **FVG 5m**: 24613.25 - 24633.75
- **Entrée**: 24612.25 @ 2025-09-25 10:24:00
- **Stop Loss**: 24646.07
- **Risk**: 33.82 points
- **TP 1RR**: 24578.43 ❌
- **TP 2RR**: 24544.62 ❌
- **TP 3RR**: 24510.80 ❌
- **TP 4RR**: 24476.98 ❌
- **TP 15RR**: 24105.00 ❌
- **PnL**: -33.82 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 38.50 points

### Trade #1727 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-25 08:30:00
- **FVG 5m**: 24613.25 - 24633.75
- **Entrée**: 24612.25 @ 2025-09-25 10:24:00
- **Stop Loss**: 24646.07
- **Risk**: 33.82 points
- **TP 1RR**: 24578.43 ❌
- **TP 2RR**: 24544.62 ❌
- **TP 3RR**: 24510.80 ❌
- **TP 4RR**: 24476.98 ❌
- **TP 15RR**: 24105.00 ❌
- **PnL**: -33.82 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 38.50 points

### Trade #1728 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-25 08:30:00
- **FVG 5m**: 24613.25 - 24633.75
- **Entrée**: 24612.25 @ 2025-09-25 10:24:00
- **Stop Loss**: 24646.07
- **Risk**: 33.82 points
- **TP 1RR**: 24578.43 ❌
- **TP 2RR**: 24544.62 ❌
- **TP 3RR**: 24510.80 ❌
- **TP 4RR**: 24476.98 ❌
- **TP 15RR**: 24105.00 ❌
- **PnL**: -33.82 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 38.50 points

### Trade #1729 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-25 08:30:00
- **FVG 5m**: 24613.25 - 24633.75
- **Entrée**: 24612.25 @ 2025-09-25 10:24:00
- **Stop Loss**: 24646.07
- **Risk**: 33.82 points
- **TP 1RR**: 24578.43 ❌
- **TP 2RR**: 24544.62 ❌
- **TP 3RR**: 24510.80 ❌
- **TP 4RR**: 24476.98 ❌
- **TP 15RR**: 24105.00 ❌
- **PnL**: -33.82 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 38.50 points

### Trade #1730 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 09:00:00
- **FVG 5m**: 24569.25 - 24576.50
- **Entrée**: 24579.25 @ 2025-09-25 09:11:00
- **Stop Loss**: 24556.97
- **Risk**: 22.28 points
- **TP 1RR**: 24601.53 ✅
- **TP 2RR**: 24623.82 ✅
- **TP 3RR**: 24646.10 ✅
- **TP 4RR**: 24668.39 ✅
- **TP 15RR**: 24913.52 ❌
- **PnL**: -22.28 points (-1.0R)
- **MFE**: 117.50 points
- **MAE**: 27.25 points

### Trade #1731 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 09:15:00
- **FVG 5m**: 24624.75 - 24633.75
- **Entrée**: 24638.75 @ 2025-09-25 10:11:00
- **Stop Loss**: 24612.44
- **Risk**: 26.31 points
- **TP 1RR**: 24665.06 ❌
- **TP 2RR**: 24691.37 ❌
- **TP 3RR**: 24717.69 ❌
- **TP 4RR**: 24744.00 ❌
- **TP 15RR**: 25033.44 ❌
- **PnL**: -26.31 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 28.50 points

### Trade #1732 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 09:30:00
- **FVG 5m**: 24624.75 - 24633.75
- **Entrée**: 24638.75 @ 2025-09-25 10:11:00
- **Stop Loss**: 24612.44
- **Risk**: 26.31 points
- **TP 1RR**: 24665.06 ❌
- **TP 2RR**: 24691.37 ❌
- **TP 3RR**: 24717.69 ❌
- **TP 4RR**: 24744.00 ❌
- **TP 15RR**: 25033.44 ❌
- **PnL**: -26.31 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 28.50 points

### Trade #1733 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 12:15:00
- **FVG 5m**: 24500.75 - 24530.75
- **Entrée**: 24532.50 @ 2025-09-25 13:14:00
- **Stop Loss**: 24488.50
- **Risk**: 44.00 points
- **TP 1RR**: 24576.50 ✅
- **TP 2RR**: 24620.50 ✅
- **TP 3RR**: 24664.50 ✅
- **TP 4RR**: 24708.50 ✅
- **TP 15RR**: 25192.51 ✅
- **PnL**: 660.01 points (15.0R)
- **MFE**: 661.25 points
- **MAE**: 12.50 points

### Trade #1734 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 03:30:00
- **FVG 5m**: 24623.25 - 24627.75
- **Entrée**: 24620.25 @ 2025-09-26 03:43:00
- **Stop Loss**: 24640.06
- **Risk**: 19.81 points
- **TP 1RR**: 24600.44 ✅
- **TP 2RR**: 24580.62 ✅
- **TP 3RR**: 24560.81 ❌
- **TP 4RR**: 24540.99 ❌
- **TP 15RR**: 24323.04 ❌
- **PnL**: -19.81 points (-1.0R)
- **MFE**: 51.00 points
- **MAE**: 22.75 points

### Trade #1735 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 05:00:00
- **FVG 5m**: 24609.50 - 24612.25
- **Entrée**: 24608.50 @ 2025-09-26 06:17:00
- **Stop Loss**: 24624.56
- **Risk**: 16.06 points
- **TP 1RR**: 24592.44 ✅
- **TP 2RR**: 24576.39 ❌
- **TP 3RR**: 24560.33 ❌
- **TP 4RR**: 24544.28 ❌
- **TP 15RR**: 24367.66 ❌
- **PnL**: -16.06 points (-1.0R)
- **MFE**: 18.00 points
- **MAE**: 17.00 points

### Trade #1736 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 07:30:00
- **FVG 5m**: 24569.00 - 24603.25
- **Entrée**: 24605.25 @ 2025-09-26 09:38:00
- **Stop Loss**: 24556.72
- **Risk**: 48.53 points
- **TP 1RR**: 24653.78 ❌
- **TP 2RR**: 24702.32 ❌
- **TP 3RR**: 24750.85 ❌
- **TP 4RR**: 24799.39 ❌
- **TP 15RR**: 25333.27 ❌
- **PnL**: -48.53 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 55.25 points

### Trade #1737 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 07:45:00
- **FVG 5m**: 24678.25 - 24681.75
- **Entrée**: 24672.75 @ 2025-09-26 08:01:00
- **Stop Loss**: 24694.09
- **Risk**: 21.34 points
- **TP 1RR**: 24651.41 ✅
- **TP 2RR**: 24630.07 ✅
- **TP 3RR**: 24608.73 ✅
- **TP 4RR**: 24587.39 ❌
- **TP 15RR**: 24352.64 ❌
- **PnL**: -21.34 points (-1.0R)
- **MFE**: 75.75 points
- **MAE**: 27.00 points

### Trade #1738 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 08:15:00
- **FVG 5m**: 24636.00 - 24672.50
- **Entrée**: 24618.75 @ 2025-09-26 09:07:00
- **Stop Loss**: 24684.84
- **Risk**: 66.09 points
- **TP 1RR**: 24552.66 ✅
- **TP 2RR**: 24486.58 ❌
- **TP 3RR**: 24420.49 ❌
- **TP 4RR**: 24354.40 ❌
- **TP 15RR**: 23627.46 ❌
- **PnL**: -66.09 points (-1.0R)
- **MFE**: 98.75 points
- **MAE**: 69.75 points

### Trade #1739 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 08:15:00
- **FVG 5m**: 24636.00 - 24672.50
- **Entrée**: 24618.75 @ 2025-09-26 09:07:00
- **Stop Loss**: 24684.84
- **Risk**: 66.09 points
- **TP 1RR**: 24552.66 ✅
- **TP 2RR**: 24486.58 ❌
- **TP 3RR**: 24420.49 ❌
- **TP 4RR**: 24354.40 ❌
- **TP 15RR**: 23627.46 ❌
- **PnL**: -66.09 points (-1.0R)
- **MFE**: 98.75 points
- **MAE**: 69.75 points

### Trade #1740 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 09:30:00
- **FVG 5m**: 24603.50 - 24621.25
- **Entrée**: 24623.00 @ 2025-09-26 11:19:00
- **Stop Loss**: 24591.20
- **Risk**: 31.80 points
- **TP 1RR**: 24654.80 ✅
- **TP 2RR**: 24686.60 ✅
- **TP 3RR**: 24718.41 ✅
- **TP 4RR**: 24750.21 ✅
- **TP 15RR**: 25100.03 ✅
- **PnL**: 477.03 points (15.0R)
- **MFE**: 479.75 points
- **MAE**: 1.75 points

### Trade #1741 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 09:30:00
- **FVG 5m**: 24603.50 - 24621.25
- **Entrée**: 24623.00 @ 2025-09-26 11:19:00
- **Stop Loss**: 24591.20
- **Risk**: 31.80 points
- **TP 1RR**: 24654.80 ✅
- **TP 2RR**: 24686.60 ✅
- **TP 3RR**: 24718.41 ✅
- **TP 4RR**: 24750.21 ✅
- **TP 15RR**: 25100.03 ✅
- **PnL**: 477.03 points (15.0R)
- **MFE**: 479.75 points
- **MAE**: 1.75 points

### Trade #1742 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 09:30:00
- **FVG 5m**: 24603.50 - 24621.25
- **Entrée**: 24623.00 @ 2025-09-26 11:19:00
- **Stop Loss**: 24591.20
- **Risk**: 31.80 points
- **TP 1RR**: 24654.80 ✅
- **TP 2RR**: 24686.60 ✅
- **TP 3RR**: 24718.41 ✅
- **TP 4RR**: 24750.21 ✅
- **TP 15RR**: 25100.03 ✅
- **PnL**: 477.03 points (15.0R)
- **MFE**: 479.75 points
- **MAE**: 1.75 points

### Trade #1743 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-28 19:00:00
- **FVG 5m**: 24795.00 - 24801.75
- **Entrée**: 24802.75 @ 2025-09-28 19:44:00
- **Stop Loss**: 24782.60
- **Risk**: 20.15 points
- **TP 1RR**: 24822.90 ❌
- **TP 2RR**: 24843.04 ❌
- **TP 3RR**: 24863.19 ❌
- **TP 4RR**: 24883.34 ❌
- **TP 15RR**: 25104.96 ❌
- **PnL**: -20.15 points (-1.0R)
- **MFE**: 4.25 points
- **MAE**: 27.25 points

### Trade #1744 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 01:30:00
- **FVG 5m**: 24842.75 - 24847.75
- **Entrée**: 24848.50 @ 2025-09-29 02:23:00
- **Stop Loss**: 24830.33
- **Risk**: 18.17 points
- **TP 1RR**: 24866.67 ✅
- **TP 2RR**: 24884.84 ✅
- **TP 3RR**: 24903.01 ✅
- **TP 4RR**: 24921.19 ✅
- **TP 15RR**: 25121.07 ❌
- **PnL**: -18.17 points (-1.0R)
- **MFE**: 127.00 points
- **MAE**: 23.00 points

### Trade #1745 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-29 10:00:00
- **FVG 5m**: 24894.25 - 24917.75
- **Entrée**: 24884.25 @ 2025-09-29 10:15:00
- **Stop Loss**: 24930.21
- **Risk**: 45.96 points
- **TP 1RR**: 24838.29 ✅
- **TP 2RR**: 24792.33 ✅
- **TP 3RR**: 24746.37 ✅
- **TP 4RR**: 24700.41 ✅
- **TP 15RR**: 24194.87 ❌
- **PnL**: -45.96 points (-1.0R)
- **MFE**: 251.00 points
- **MAE**: 46.75 points

### Trade #1746 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-29 10:00:00
- **FVG 5m**: 24894.25 - 24917.75
- **Entrée**: 24884.25 @ 2025-09-29 10:15:00
- **Stop Loss**: 24930.21
- **Risk**: 45.96 points
- **TP 1RR**: 24838.29 ✅
- **TP 2RR**: 24792.33 ✅
- **TP 3RR**: 24746.37 ✅
- **TP 4RR**: 24700.41 ✅
- **TP 15RR**: 24194.87 ❌
- **PnL**: -45.96 points (-1.0R)
- **MFE**: 251.00 points
- **MAE**: 46.75 points

### Trade #1747 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-29 10:00:00
- **FVG 5m**: 24894.25 - 24917.75
- **Entrée**: 24884.25 @ 2025-09-29 10:15:00
- **Stop Loss**: 24930.21
- **Risk**: 45.96 points
- **TP 1RR**: 24838.29 ✅
- **TP 2RR**: 24792.33 ✅
- **TP 3RR**: 24746.37 ✅
- **TP 4RR**: 24700.41 ✅
- **TP 15RR**: 24194.87 ❌
- **PnL**: -45.96 points (-1.0R)
- **MFE**: 251.00 points
- **MAE**: 46.75 points

### Trade #1748 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 10:30:00
- **FVG 5m**: 24834.00 - 24838.75
- **Entrée**: 24846.50 @ 2025-09-29 12:52:00
- **Stop Loss**: 24821.58
- **Risk**: 24.92 points
- **TP 1RR**: 24871.42 ❌
- **TP 2RR**: 24896.33 ❌
- **TP 3RR**: 24921.25 ❌
- **TP 4RR**: 24946.17 ❌
- **TP 15RR**: 25220.26 ❌
- **PnL**: -24.92 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 33.00 points

### Trade #1749 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 10:45:00
- **FVG 5m**: 24834.00 - 24838.75
- **Entrée**: 24846.50 @ 2025-09-29 12:52:00
- **Stop Loss**: 24821.58
- **Risk**: 24.92 points
- **TP 1RR**: 24871.42 ❌
- **TP 2RR**: 24896.33 ❌
- **TP 3RR**: 24921.25 ❌
- **TP 4RR**: 24946.17 ❌
- **TP 15RR**: 25220.26 ❌
- **PnL**: -24.92 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 33.00 points

### Trade #1750 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 12:00:00
- **FVG 5m**: 24834.00 - 24838.75
- **Entrée**: 24846.50 @ 2025-09-29 12:52:00
- **Stop Loss**: 24821.58
- **Risk**: 24.92 points
- **TP 1RR**: 24871.42 ❌
- **TP 2RR**: 24896.33 ❌
- **TP 3RR**: 24921.25 ❌
- **TP 4RR**: 24946.17 ❌
- **TP 15RR**: 25220.26 ❌
- **PnL**: -24.92 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 33.00 points

### Trade #1751 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 14:15:00
- **FVG 5m**: 24813.75 - 24816.75
- **Entrée**: 24818.75 @ 2025-09-29 14:38:00
- **Stop Loss**: 24801.34
- **Risk**: 17.41 points
- **TP 1RR**: 24836.16 ✅
- **TP 2RR**: 24853.56 ✅
- **TP 3RR**: 24870.97 ❌
- **TP 4RR**: 24888.38 ❌
- **TP 15RR**: 25079.85 ❌
- **PnL**: -17.41 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 25.00 points

### Trade #1752 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 01:30:00
- **FVG 5m**: 24831.75 - 24834.25
- **Entrée**: 24831.00 @ 2025-09-30 01:48:00
- **Stop Loss**: 24846.67
- **Risk**: 15.67 points
- **TP 1RR**: 24815.33 ✅
- **TP 2RR**: 24799.67 ✅
- **TP 3RR**: 24784.00 ✅
- **TP 4RR**: 24768.33 ✅
- **TP 15RR**: 24595.99 ❌
- **PnL**: -15.67 points (-1.0R)
- **MFE**: 108.75 points
- **MAE**: 23.50 points

### Trade #1753 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 02:45:00
- **FVG 5m**: 24801.25 - 24805.00
- **Entrée**: 24814.50 @ 2025-09-30 04:30:00
- **Stop Loss**: 24788.85
- **Risk**: 25.65 points
- **TP 1RR**: 24840.15 ❌
- **TP 2RR**: 24865.80 ❌
- **TP 3RR**: 24891.45 ❌
- **TP 4RR**: 24917.10 ❌
- **TP 15RR**: 25199.26 ❌
- **PnL**: -25.65 points (-1.0R)
- **MFE**: 5.75 points
- **MAE**: 27.75 points

### Trade #1754 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 04:30:00
- **FVG 5m**: 24796.50 - 24803.00
- **Entrée**: 24794.00 @ 2025-09-30 05:13:00
- **Stop Loss**: 24815.40
- **Risk**: 21.40 points
- **TP 1RR**: 24772.60 ❌
- **TP 2RR**: 24751.20 ❌
- **TP 3RR**: 24729.80 ❌
- **TP 4RR**: 24708.39 ❌
- **TP 15RR**: 24472.98 ❌
- **PnL**: -21.40 points (-1.0R)
- **MFE**: 20.00 points
- **MAE**: 21.50 points

### Trade #1755 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 07:15:00
- **FVG 5m**: 24823.50 - 24831.50
- **Entrée**: 24834.75 @ 2025-09-30 07:39:00
- **Stop Loss**: 24811.09
- **Risk**: 23.66 points
- **TP 1RR**: 24858.41 ❌
- **TP 2RR**: 24882.07 ❌
- **TP 3RR**: 24905.74 ❌
- **TP 4RR**: 24929.40 ❌
- **TP 15RR**: 25189.68 ❌
- **PnL**: -23.66 points (-1.0R)
- **MFE**: 10.25 points
- **MAE**: 33.75 points

### Trade #1756 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 07:15:00
- **FVG 5m**: 24823.50 - 24831.50
- **Entrée**: 24834.75 @ 2025-09-30 07:39:00
- **Stop Loss**: 24811.09
- **Risk**: 23.66 points
- **TP 1RR**: 24858.41 ❌
- **TP 2RR**: 24882.07 ❌
- **TP 3RR**: 24905.74 ❌
- **TP 4RR**: 24929.40 ❌
- **TP 15RR**: 25189.68 ❌
- **PnL**: -23.66 points (-1.0R)
- **MFE**: 10.25 points
- **MAE**: 33.75 points

### Trade #1757 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 08:30:00
- **FVG 5m**: 24795.25 - 24817.75
- **Entrée**: 24832.50 @ 2025-09-30 09:48:00
- **Stop Loss**: 24782.85
- **Risk**: 49.65 points
- **TP 1RR**: 24882.15 ❌
- **TP 2RR**: 24931.80 ❌
- **TP 3RR**: 24981.44 ❌
- **TP 4RR**: 25031.09 ❌
- **TP 15RR**: 25577.21 ❌
- **PnL**: -49.65 points (-1.0R)
- **MFE**: 30.25 points
- **MAE**: 49.75 points

### Trade #1758 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 08:30:00
- **FVG 5m**: 24795.25 - 24817.75
- **Entrée**: 24832.50 @ 2025-09-30 09:48:00
- **Stop Loss**: 24782.85
- **Risk**: 49.65 points
- **TP 1RR**: 24882.15 ❌
- **TP 2RR**: 24931.80 ❌
- **TP 3RR**: 24981.44 ❌
- **TP 4RR**: 25031.09 ❌
- **TP 15RR**: 25577.21 ❌
- **PnL**: -49.65 points (-1.0R)
- **MFE**: 30.25 points
- **MAE**: 49.75 points

### Trade #1759 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 08:30:00
- **FVG 5m**: 24795.25 - 24817.75
- **Entrée**: 24832.50 @ 2025-09-30 09:48:00
- **Stop Loss**: 24782.85
- **Risk**: 49.65 points
- **TP 1RR**: 24882.15 ❌
- **TP 2RR**: 24931.80 ❌
- **TP 3RR**: 24981.44 ❌
- **TP 4RR**: 25031.09 ❌
- **TP 15RR**: 25577.21 ❌
- **PnL**: -49.65 points (-1.0R)
- **MFE**: 30.25 points
- **MAE**: 49.75 points

### Trade #1760 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 08:30:00
- **FVG 5m**: 24795.25 - 24817.75
- **Entrée**: 24832.50 @ 2025-09-30 09:48:00
- **Stop Loss**: 24782.85
- **Risk**: 49.65 points
- **TP 1RR**: 24882.15 ❌
- **TP 2RR**: 24931.80 ❌
- **TP 3RR**: 24981.44 ❌
- **TP 4RR**: 25031.09 ❌
- **TP 15RR**: 25577.21 ❌
- **PnL**: -49.65 points (-1.0R)
- **MFE**: 30.25 points
- **MAE**: 49.75 points

### Trade #1761 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 09:45:00
- **FVG 5m**: 24835.50 - 24839.25
- **Entrée**: 24841.75 @ 2025-09-30 09:58:00
- **Stop Loss**: 24823.08
- **Risk**: 18.67 points
- **TP 1RR**: 24860.42 ✅
- **TP 2RR**: 24879.09 ❌
- **TP 3RR**: 24897.75 ❌
- **TP 4RR**: 24916.42 ❌
- **TP 15RR**: 25121.77 ❌
- **PnL**: -18.67 points (-1.0R)
- **MFE**: 21.00 points
- **MAE**: 28.25 points

### Trade #1762 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 10:00:00
- **FVG 5m**: 24833.75 - 24838.25
- **Entrée**: 24828.00 @ 2025-09-30 10:14:00
- **Stop Loss**: 24850.67
- **Risk**: 22.67 points
- **TP 1RR**: 24805.33 ✅
- **TP 2RR**: 24782.66 ✅
- **TP 3RR**: 24759.99 ✅
- **TP 4RR**: 24737.32 ✅
- **TP 15RR**: 24487.96 ❌
- **PnL**: -22.67 points (-1.0R)
- **MFE**: 96.25 points
- **MAE**: 23.75 points

### Trade #1763 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 10:15:00
- **FVG 5m**: 24787.00 - 24791.25
- **Entrée**: 24779.25 @ 2025-09-30 11:58:00
- **Stop Loss**: 24803.65
- **Risk**: 24.40 points
- **TP 1RR**: 24754.85 ✅
- **TP 2RR**: 24730.46 ❌
- **TP 3RR**: 24706.06 ❌
- **TP 4RR**: 24681.67 ❌
- **TP 15RR**: 24413.32 ❌
- **PnL**: -24.40 points (-1.0R)
- **MFE**: 47.50 points
- **MAE**: 28.50 points

### Trade #1764 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 12:15:00
- **FVG 5m**: 24773.00 - 24775.75
- **Entrée**: 24772.50 @ 2025-09-30 12:58:00
- **Stop Loss**: 24788.14
- **Risk**: 15.64 points
- **TP 1RR**: 24756.86 ❌
- **TP 2RR**: 24741.22 ❌
- **TP 3RR**: 24725.59 ❌
- **TP 4RR**: 24709.95 ❌
- **TP 15RR**: 24537.93 ❌
- **PnL**: -15.64 points (-1.0R)
- **MFE**: 10.50 points
- **MAE**: 18.00 points

### Trade #1765 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 12:15:00
- **FVG 5m**: 24773.00 - 24775.75
- **Entrée**: 24772.50 @ 2025-09-30 12:58:00
- **Stop Loss**: 24788.14
- **Risk**: 15.64 points
- **TP 1RR**: 24756.86 ❌
- **TP 2RR**: 24741.22 ❌
- **TP 3RR**: 24725.59 ❌
- **TP 4RR**: 24709.95 ❌
- **TP 15RR**: 24537.93 ❌
- **PnL**: -15.64 points (-1.0R)
- **MFE**: 10.50 points
- **MAE**: 18.00 points

### Trade #1766 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 14:30:00
- **FVG 5m**: 24878.00 - 24892.00
- **Entrée**: 24876.00 @ 2025-09-30 15:03:00
- **Stop Loss**: 24904.45
- **Risk**: 28.45 points
- **TP 1RR**: 24847.55 ✅
- **TP 2RR**: 24819.11 ✅
- **TP 3RR**: 24790.66 ✅
- **TP 4RR**: 24762.22 ✅
- **TP 15RR**: 24449.31 ❌
- **PnL**: -28.45 points (-1.0R)
- **MFE**: 242.75 points
- **MAE**: 30.25 points

### Trade #1767 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 14:30:00
- **FVG 5m**: 24878.00 - 24892.00
- **Entrée**: 24876.00 @ 2025-09-30 15:03:00
- **Stop Loss**: 24904.45
- **Risk**: 28.45 points
- **TP 1RR**: 24847.55 ✅
- **TP 2RR**: 24819.11 ✅
- **TP 3RR**: 24790.66 ✅
- **TP 4RR**: 24762.22 ✅
- **TP 15RR**: 24449.31 ❌
- **PnL**: -28.45 points (-1.0R)
- **MFE**: 242.75 points
- **MAE**: 30.25 points

### Trade #1768 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 14:30:00
- **FVG 5m**: 24878.00 - 24892.00
- **Entrée**: 24876.00 @ 2025-09-30 15:03:00
- **Stop Loss**: 24904.45
- **Risk**: 28.45 points
- **TP 1RR**: 24847.55 ✅
- **TP 2RR**: 24819.11 ✅
- **TP 3RR**: 24790.66 ✅
- **TP 4RR**: 24762.22 ✅
- **TP 15RR**: 24449.31 ❌
- **PnL**: -28.45 points (-1.0R)
- **MFE**: 242.75 points
- **MAE**: 30.25 points

### Trade #1769 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 15:00:00
- **FVG 5m**: 24848.00 - 24852.75
- **Entrée**: 24845.25 @ 2025-09-30 15:34:00
- **Stop Loss**: 24865.18
- **Risk**: 19.93 points
- **TP 1RR**: 24825.32 ❌
- **TP 2RR**: 24805.40 ❌
- **TP 3RR**: 24785.47 ❌
- **TP 4RR**: 24765.54 ❌
- **TP 15RR**: 24546.35 ❌
- **PnL**: -19.93 points (-1.0R)
- **MFE**: 10.50 points
- **MAE**: 26.50 points

### Trade #1770 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 01:30:00
- **FVG 5m**: 24730.50 - 24745.25
- **Entrée**: 24729.00 @ 2025-10-01 01:44:00
- **Stop Loss**: 24757.62
- **Risk**: 28.62 points
- **TP 1RR**: 24700.38 ✅
- **TP 2RR**: 24671.75 ✅
- **TP 3RR**: 24643.13 ✅
- **TP 4RR**: 24614.51 ❌
- **TP 15RR**: 24299.66 ❌
- **PnL**: -28.62 points (-1.0R)
- **MFE**: 95.75 points
- **MAE**: 37.00 points

### Trade #1771 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 01:30:00
- **FVG 5m**: 24730.50 - 24745.25
- **Entrée**: 24729.00 @ 2025-10-01 01:44:00
- **Stop Loss**: 24757.62
- **Risk**: 28.62 points
- **TP 1RR**: 24700.38 ✅
- **TP 2RR**: 24671.75 ✅
- **TP 3RR**: 24643.13 ✅
- **TP 4RR**: 24614.51 ❌
- **TP 15RR**: 24299.66 ❌
- **PnL**: -28.62 points (-1.0R)
- **MFE**: 95.75 points
- **MAE**: 37.00 points

### Trade #1772 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 03:30:00
- **FVG 5m**: 24723.75 - 24732.75
- **Entrée**: 24737.50 @ 2025-10-01 04:08:00
- **Stop Loss**: 24711.39
- **Risk**: 26.11 points
- **TP 1RR**: 24763.61 ✅
- **TP 2RR**: 24789.72 ✅
- **TP 3RR**: 24815.84 ✅
- **TP 4RR**: 24841.95 ✅
- **TP 15RR**: 25129.18 ✅
- **PnL**: 391.68 points (15.0R)
- **MFE**: 392.00 points
- **MAE**: 15.75 points

### Trade #1773 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 03:30:00
- **FVG 5m**: 24723.75 - 24732.75
- **Entrée**: 24737.50 @ 2025-10-01 04:08:00
- **Stop Loss**: 24711.39
- **Risk**: 26.11 points
- **TP 1RR**: 24763.61 ✅
- **TP 2RR**: 24789.72 ✅
- **TP 3RR**: 24815.84 ✅
- **TP 4RR**: 24841.95 ✅
- **TP 15RR**: 25129.18 ✅
- **PnL**: 391.68 points (15.0R)
- **MFE**: 392.00 points
- **MAE**: 15.75 points

### Trade #1774 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 04:00:00
- **FVG 5m**: 24742.00 - 24744.50
- **Entrée**: 24745.25 @ 2025-10-01 04:23:00
- **Stop Loss**: 24729.63
- **Risk**: 15.62 points
- **TP 1RR**: 24760.87 ✅
- **TP 2RR**: 24776.49 ❌
- **TP 3RR**: 24792.11 ❌
- **TP 4RR**: 24807.73 ❌
- **TP 15RR**: 24979.56 ❌
- **PnL**: -15.62 points (-1.0R)
- **MFE**: 21.50 points
- **MAE**: 22.50 points

### Trade #1775 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 04:30:00
- **FVG 5m**: 24742.75 - 24746.75
- **Entrée**: 24742.25 @ 2025-10-01 05:29:00
- **Stop Loss**: 24759.12
- **Risk**: 16.87 points
- **TP 1RR**: 24725.38 ✅
- **TP 2RR**: 24708.50 ❌
- **TP 3RR**: 24691.63 ❌
- **TP 4RR**: 24674.76 ❌
- **TP 15RR**: 24489.15 ❌
- **PnL**: -16.87 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 20.00 points

### Trade #1776 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 08:15:00
- **FVG 5m**: 24781.75 - 24803.25
- **Entrée**: 24773.50 @ 2025-10-01 08:48:00
- **Stop Loss**: 24815.65
- **Risk**: 42.15 points
- **TP 1RR**: 24731.35 ✅
- **TP 2RR**: 24689.20 ❌
- **TP 3RR**: 24647.05 ❌
- **TP 4RR**: 24604.89 ❌
- **TP 15RR**: 24141.23 ❌
- **PnL**: -42.15 points (-1.0R)
- **MFE**: 47.50 points
- **MAE**: 46.00 points

### Trade #1777 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 08:15:00
- **FVG 5m**: 24781.75 - 24803.25
- **Entrée**: 24773.50 @ 2025-10-01 08:48:00
- **Stop Loss**: 24815.65
- **Risk**: 42.15 points
- **TP 1RR**: 24731.35 ✅
- **TP 2RR**: 24689.20 ❌
- **TP 3RR**: 24647.05 ❌
- **TP 4RR**: 24604.89 ❌
- **TP 15RR**: 24141.23 ❌
- **PnL**: -42.15 points (-1.0R)
- **MFE**: 47.50 points
- **MAE**: 46.00 points

### Trade #1778 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 08:30:00
- **FVG 5m**: 24823.25 - 24825.75
- **Entrée**: 24828.00 @ 2025-10-01 09:13:00
- **Stop Loss**: 24810.84
- **Risk**: 17.16 points
- **TP 1RR**: 24845.16 ✅
- **TP 2RR**: 24862.32 ✅
- **TP 3RR**: 24879.48 ✅
- **TP 4RR**: 24896.65 ✅
- **TP 15RR**: 25085.42 ✅
- **PnL**: 257.42 points (15.0R)
- **MFE**: 258.50 points
- **MAE**: 2.25 points

### Trade #1779 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 12:15:00
- **FVG 5m**: 24986.00 - 24993.50
- **Entrée**: 25000.00 @ 2025-10-01 13:05:00
- **Stop Loss**: 24973.51
- **Risk**: 26.49 points
- **TP 1RR**: 25026.49 ✅
- **TP 2RR**: 25052.99 ✅
- **TP 3RR**: 25079.48 ✅
- **TP 4RR**: 25105.97 ✅
- **TP 15RR**: 25397.39 ❌
- **PnL**: -26.49 points (-1.0R)
- **MFE**: 196.50 points
- **MAE**: 30.00 points

### Trade #1780 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 12:45:00
- **FVG 5m**: 24986.00 - 24993.50
- **Entrée**: 25000.00 @ 2025-10-01 13:05:00
- **Stop Loss**: 24973.51
- **Risk**: 26.49 points
- **TP 1RR**: 25026.49 ✅
- **TP 2RR**: 25052.99 ✅
- **TP 3RR**: 25079.48 ✅
- **TP 4RR**: 25105.97 ✅
- **TP 15RR**: 25397.39 ❌
- **PnL**: -26.49 points (-1.0R)
- **MFE**: 196.50 points
- **MAE**: 30.00 points

### Trade #1781 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 12:45:00
- **FVG 5m**: 24986.00 - 24993.50
- **Entrée**: 25000.00 @ 2025-10-01 13:05:00
- **Stop Loss**: 24973.51
- **Risk**: 26.49 points
- **TP 1RR**: 25026.49 ✅
- **TP 2RR**: 25052.99 ✅
- **TP 3RR**: 25079.48 ✅
- **TP 4RR**: 25105.97 ✅
- **TP 15RR**: 25397.39 ❌
- **PnL**: -26.49 points (-1.0R)
- **MFE**: 196.50 points
- **MAE**: 30.00 points

### Trade #1782 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 14:30:00
- **FVG 5m**: 25000.75 - 25010.75
- **Entrée**: 24999.25 @ 2025-10-01 15:01:00
- **Stop Loss**: 25023.26
- **Risk**: 24.01 points
- **TP 1RR**: 24975.24 ❌
- **TP 2RR**: 24951.24 ❌
- **TP 3RR**: 24927.23 ❌
- **TP 4RR**: 24903.23 ❌
- **TP 15RR**: 24639.17 ❌
- **PnL**: -24.01 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 24.25 points

### Trade #1783 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 14:30:00
- **FVG 5m**: 25000.75 - 25010.75
- **Entrée**: 24999.25 @ 2025-10-01 15:01:00
- **Stop Loss**: 25023.26
- **Risk**: 24.01 points
- **TP 1RR**: 24975.24 ❌
- **TP 2RR**: 24951.24 ❌
- **TP 3RR**: 24927.23 ❌
- **TP 4RR**: 24903.23 ❌
- **TP 15RR**: 24639.17 ❌
- **PnL**: -24.01 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 24.25 points

### Trade #1784 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 14:30:00
- **FVG 5m**: 25000.75 - 25010.75
- **Entrée**: 24999.25 @ 2025-10-01 15:01:00
- **Stop Loss**: 25023.26
- **Risk**: 24.01 points
- **TP 1RR**: 24975.24 ❌
- **TP 2RR**: 24951.24 ❌
- **TP 3RR**: 24927.23 ❌
- **TP 4RR**: 24903.23 ❌
- **TP 15RR**: 24639.17 ❌
- **PnL**: -24.01 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 24.25 points

### Trade #1785 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-02 08:30:00
- **FVG 5m**: 25071.50 - 25076.25
- **Entrée**: 25069.25 @ 2025-10-02 08:46:00
- **Stop Loss**: 25088.79
- **Risk**: 19.54 points
- **TP 1RR**: 25049.71 ✅
- **TP 2RR**: 25030.17 ✅
- **TP 3RR**: 25010.64 ❌
- **TP 4RR**: 24991.10 ❌
- **TP 15RR**: 24776.18 ❌
- **PnL**: -19.54 points (-1.0R)
- **MFE**: 55.25 points
- **MAE**: 20.50 points

### Trade #1786 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 08:45:00
- **FVG 5m**: 25038.50 - 25061.50
- **Entrée**: 25062.75 @ 2025-10-02 10:54:00
- **Stop Loss**: 25025.98
- **Risk**: 36.77 points
- **TP 1RR**: 25099.52 ✅
- **TP 2RR**: 25136.29 ✅
- **TP 3RR**: 25173.06 ✅
- **TP 4RR**: 25209.83 ❌
- **TP 15RR**: 25614.29 ❌
- **PnL**: -36.77 points (-1.0R)
- **MFE**: 133.75 points
- **MAE**: 38.50 points

### Trade #1787 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 08:45:00
- **FVG 5m**: 25038.50 - 25061.50
- **Entrée**: 25062.75 @ 2025-10-02 10:54:00
- **Stop Loss**: 25025.98
- **Risk**: 36.77 points
- **TP 1RR**: 25099.52 ✅
- **TP 2RR**: 25136.29 ✅
- **TP 3RR**: 25173.06 ✅
- **TP 4RR**: 25209.83 ❌
- **TP 15RR**: 25614.29 ❌
- **PnL**: -36.77 points (-1.0R)
- **MFE**: 133.75 points
- **MAE**: 38.50 points

### Trade #1788 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 10:45:00
- **FVG 5m**: 25063.75 - 25069.75
- **Entrée**: 25071.00 @ 2025-10-02 11:52:00
- **Stop Loss**: 25051.22
- **Risk**: 19.78 points
- **TP 1RR**: 25090.78 ✅
- **TP 2RR**: 25110.56 ✅
- **TP 3RR**: 25130.35 ✅
- **TP 4RR**: 25150.13 ✅
- **TP 15RR**: 25367.73 ❌
- **PnL**: -19.78 points (-1.0R)
- **MFE**: 125.50 points
- **MAE**: 20.00 points

### Trade #1789 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 17:30:00
- **FVG 5m**: 25085.50 - 25091.25
- **Entrée**: 25092.25 @ 2025-10-02 17:42:00
- **Stop Loss**: 25072.96
- **Risk**: 19.29 points
- **TP 1RR**: 25111.54 ✅
- **TP 2RR**: 25130.84 ✅
- **TP 3RR**: 25150.13 ✅
- **TP 4RR**: 25169.42 ✅
- **TP 15RR**: 25381.64 ❌
- **PnL**: -19.29 points (-1.0R)
- **MFE**: 104.25 points
- **MAE**: 27.50 points

### Trade #1790 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 06:30:00
- **FVG 5m**: 25148.00 - 25153.25
- **Entrée**: 25155.75 @ 2025-10-03 06:43:00
- **Stop Loss**: 25135.43
- **Risk**: 20.32 points
- **TP 1RR**: 25176.07 ❌
- **TP 2RR**: 25196.40 ❌
- **TP 3RR**: 25216.72 ❌
- **TP 4RR**: 25237.05 ❌
- **TP 15RR**: 25460.61 ❌
- **PnL**: -20.32 points (-1.0R)
- **MFE**: 8.00 points
- **MAE**: 21.75 points

### Trade #1791 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-03 07:30:00
- **FVG 5m**: 25117.75 - 25122.00
- **Entrée**: 25114.25 @ 2025-10-03 07:44:00
- **Stop Loss**: 25134.56
- **Risk**: 20.31 points
- **TP 1RR**: 25093.94 ❌
- **TP 2RR**: 25073.63 ❌
- **TP 3RR**: 25053.32 ❌
- **TP 4RR**: 25033.01 ❌
- **TP 15RR**: 24809.58 ❌
- **PnL**: -20.31 points (-1.0R)
- **MFE**: 11.25 points
- **MAE**: 22.25 points

### Trade #1792 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 09:00:00
- **FVG 5m**: 25099.75 - 25105.25
- **Entrée**: 25110.50 @ 2025-10-03 09:37:00
- **Stop Loss**: 25087.20
- **Risk**: 23.30 points
- **TP 1RR**: 25133.80 ✅
- **TP 2RR**: 25157.10 ❌
- **TP 3RR**: 25180.40 ❌
- **TP 4RR**: 25203.70 ❌
- **TP 15RR**: 25460.00 ❌
- **PnL**: -23.30 points (-1.0R)
- **MFE**: 45.50 points
- **MAE**: 27.75 points

### Trade #1793 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 12:00:00
- **FVG 5m**: 24957.50 - 24970.50
- **Entrée**: 24980.75 @ 2025-10-03 13:11:00
- **Stop Loss**: 24945.02
- **Risk**: 35.73 points
- **TP 1RR**: 25016.48 ✅
- **TP 2RR**: 25052.21 ✅
- **TP 3RR**: 25087.94 ✅
- **TP 4RR**: 25123.66 ✅
- **TP 15RR**: 25516.68 ❌
- **PnL**: -35.73 points (-1.0R)
- **MFE**: 413.25 points
- **MAE**: 42.00 points

### Trade #1794 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-03 12:45:00
- **FVG 5m**: 24998.25 - 25001.00
- **Entrée**: 24987.00 @ 2025-10-03 13:49:00
- **Stop Loss**: 25013.50
- **Risk**: 26.50 points
- **TP 1RR**: 24960.50 ❌
- **TP 2RR**: 24934.00 ❌
- **TP 3RR**: 24907.50 ❌
- **TP 4RR**: 24881.00 ❌
- **TP 15RR**: 24589.49 ❌
- **PnL**: -26.50 points (-1.0R)
- **MFE**: 8.00 points
- **MAE**: 30.00 points

### Trade #1795 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 12:45:00
- **FVG 5m**: 24957.50 - 24970.50
- **Entrée**: 24980.75 @ 2025-10-03 13:11:00
- **Stop Loss**: 24945.02
- **Risk**: 35.73 points
- **TP 1RR**: 25016.48 ✅
- **TP 2RR**: 25052.21 ✅
- **TP 3RR**: 25087.94 ✅
- **TP 4RR**: 25123.66 ✅
- **TP 15RR**: 25516.68 ❌
- **PnL**: -35.73 points (-1.0R)
- **MFE**: 413.25 points
- **MAE**: 42.00 points

### Trade #1796 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 00:00:00
- **FVG 5m**: 25090.75 - 25097.25
- **Entrée**: 25088.25 @ 2025-10-06 02:24:00
- **Stop Loss**: 25109.80
- **Risk**: 21.55 points
- **TP 1RR**: 25066.70 ✅
- **TP 2RR**: 25045.15 ❌
- **TP 3RR**: 25023.60 ❌
- **TP 4RR**: 25002.06 ❌
- **TP 15RR**: 24765.02 ❌
- **PnL**: -21.55 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 26.50 points

### Trade #1797 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-06 02:30:00
- **FVG 5m**: 25076.00 - 25079.00
- **Entrée**: 25079.50 @ 2025-10-06 02:51:00
- **Stop Loss**: 25063.46
- **Risk**: 16.04 points
- **TP 1RR**: 25095.54 ✅
- **TP 2RR**: 25111.58 ✅
- **TP 3RR**: 25127.61 ✅
- **TP 4RR**: 25143.65 ✅
- **TP 15RR**: 25320.07 ❌
- **PnL**: -16.04 points (-1.0R)
- **MFE**: 195.50 points
- **MAE**: 26.50 points

### Trade #1798 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-06 02:45:00
- **FVG 5m**: 25093.25 - 25097.25
- **Entrée**: 25106.75 @ 2025-10-06 03:05:00
- **Stop Loss**: 25080.70
- **Risk**: 26.05 points
- **TP 1RR**: 25132.80 ✅
- **TP 2RR**: 25158.84 ✅
- **TP 3RR**: 25184.89 ✅
- **TP 4RR**: 25210.94 ✅
- **TP 15RR**: 25497.45 ❌
- **PnL**: -26.05 points (-1.0R)
- **MFE**: 168.25 points
- **MAE**: 26.25 points

### Trade #1799 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 06:00:00
- **FVG 5m**: 25204.50 - 25211.25
- **Entrée**: 25204.25 @ 2025-10-06 07:32:00
- **Stop Loss**: 25223.86
- **Risk**: 19.61 points
- **TP 1RR**: 25184.64 ✅
- **TP 2RR**: 25165.04 ✅
- **TP 3RR**: 25145.43 ✅
- **TP 4RR**: 25125.83 ✅
- **TP 15RR**: 24910.17 ❌
- **PnL**: -19.61 points (-1.0R)
- **MFE**: 95.75 points
- **MAE**: 25.75 points

### Trade #1800 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 07:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25167.83
- **Risk**: 16.58 points
- **TP 1RR**: 25134.67 ✅
- **TP 2RR**: 25118.09 ✅
- **TP 3RR**: 25101.52 ❌
- **TP 4RR**: 25084.94 ❌
- **TP 15RR**: 24902.59 ❌
- **PnL**: -16.58 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 17.75 points

### Trade #1801 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 07:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25167.83
- **Risk**: 16.58 points
- **TP 1RR**: 25134.67 ✅
- **TP 2RR**: 25118.09 ✅
- **TP 3RR**: 25101.52 ❌
- **TP 4RR**: 25084.94 ❌
- **TP 15RR**: 24902.59 ❌
- **PnL**: -16.58 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 17.75 points

### Trade #1802 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 08:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25167.83
- **Risk**: 16.58 points
- **TP 1RR**: 25134.67 ✅
- **TP 2RR**: 25118.09 ✅
- **TP 3RR**: 25101.52 ❌
- **TP 4RR**: 25084.94 ❌
- **TP 15RR**: 24902.59 ❌
- **PnL**: -16.58 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 17.75 points

### Trade #1803 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 08:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25167.83
- **Risk**: 16.58 points
- **TP 1RR**: 25134.67 ✅
- **TP 2RR**: 25118.09 ✅
- **TP 3RR**: 25101.52 ❌
- **TP 4RR**: 25084.94 ❌
- **TP 15RR**: 24902.59 ❌
- **PnL**: -16.58 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 17.75 points

### Trade #1804 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 08:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25167.83
- **Risk**: 16.58 points
- **TP 1RR**: 25134.67 ✅
- **TP 2RR**: 25118.09 ✅
- **TP 3RR**: 25101.52 ❌
- **TP 4RR**: 25084.94 ❌
- **TP 15RR**: 24902.59 ❌
- **PnL**: -16.58 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 17.75 points

### Trade #1805 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 14:30:00
- **FVG 5m**: 25213.50 - 25217.25
- **Entrée**: 25212.50 @ 2025-10-06 14:42:00
- **Stop Loss**: 25229.86
- **Risk**: 17.36 points
- **TP 1RR**: 25195.14 ✅
- **TP 2RR**: 25177.78 ✅
- **TP 3RR**: 25160.42 ✅
- **TP 4RR**: 25143.07 ✅
- **TP 15RR**: 24952.12 ❌
- **PnL**: -17.36 points (-1.0R)
- **MFE**: 90.00 points
- **MAE**: 19.00 points

### Trade #1806 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 08:00:00
- **FVG 5m**: 25246.50 - 25260.25
- **Entrée**: 25243.75 @ 2025-10-07 08:14:00
- **Stop Loss**: 25272.88
- **Risk**: 29.13 points
- **TP 1RR**: 25214.62 ✅
- **TP 2RR**: 25185.49 ✅
- **TP 3RR**: 25156.36 ✅
- **TP 4RR**: 25127.23 ✅
- **TP 15RR**: 24806.80 ❌
- **PnL**: -29.13 points (-1.0R)
- **MFE**: 259.00 points
- **MAE**: 32.50 points

### Trade #1807 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 08:45:00
- **FVG 5m**: 25147.25 - 25172.25
- **Entrée**: 25144.50 @ 2025-10-07 10:04:00
- **Stop Loss**: 25184.84
- **Risk**: 40.34 points
- **TP 1RR**: 25104.16 ✅
- **TP 2RR**: 25063.83 ✅
- **TP 3RR**: 25023.49 ✅
- **TP 4RR**: 24983.16 ❌
- **TP 15RR**: 24539.46 ❌
- **PnL**: -40.34 points (-1.0R)
- **MFE**: 159.75 points
- **MAE**: 55.50 points

### Trade #1808 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 09:45:00
- **FVG 5m**: 25147.25 - 25172.25
- **Entrée**: 25144.50 @ 2025-10-07 10:04:00
- **Stop Loss**: 25184.84
- **Risk**: 40.34 points
- **TP 1RR**: 25104.16 ✅
- **TP 2RR**: 25063.83 ✅
- **TP 3RR**: 25023.49 ✅
- **TP 4RR**: 24983.16 ❌
- **TP 15RR**: 24539.46 ❌
- **PnL**: -40.34 points (-1.0R)
- **MFE**: 159.75 points
- **MAE**: 55.50 points

### Trade #1809 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-07 10:00:00
- **FVG 5m**: 25056.75 - 25064.25
- **Entrée**: 25067.50 @ 2025-10-07 11:33:00
- **Stop Loss**: 25044.22
- **Risk**: 23.28 points
- **TP 1RR**: 25090.78 ✅
- **TP 2RR**: 25114.06 ❌
- **TP 3RR**: 25137.34 ❌
- **TP 4RR**: 25160.61 ❌
- **TP 15RR**: 25416.68 ❌
- **PnL**: -23.28 points (-1.0R)
- **MFE**: 24.50 points
- **MAE**: 35.00 points

### Trade #1810 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 10:15:00
- **FVG 5m**: 25080.25 - 25095.00
- **Entrée**: 25073.50 @ 2025-10-07 10:28:00
- **Stop Loss**: 25107.55
- **Risk**: 34.05 points
- **TP 1RR**: 25039.45 ✅
- **TP 2RR**: 25005.40 ✅
- **TP 3RR**: 24971.36 ❌
- **TP 4RR**: 24937.31 ❌
- **TP 15RR**: 24562.79 ❌
- **PnL**: -34.05 points (-1.0R)
- **MFE**: 88.75 points
- **MAE**: 35.25 points

### Trade #1811 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-08 03:45:00
- **FVG 5m**: 25094.25 - 25097.00
- **Entrée**: 25093.50 @ 2025-10-08 06:14:00
- **Stop Loss**: 25109.55
- **Risk**: 16.05 points
- **TP 1RR**: 25077.45 ✅
- **TP 2RR**: 25061.40 ✅
- **TP 3RR**: 25045.35 ✅
- **TP 4RR**: 25029.31 ❌
- **TP 15RR**: 24852.77 ❌
- **PnL**: -16.05 points (-1.0R)
- **MFE**: 51.00 points
- **MAE**: 21.75 points

### Trade #1812 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-08 03:45:00
- **FVG 5m**: 25094.25 - 25097.00
- **Entrée**: 25093.50 @ 2025-10-08 06:14:00
- **Stop Loss**: 25109.55
- **Risk**: 16.05 points
- **TP 1RR**: 25077.45 ✅
- **TP 2RR**: 25061.40 ✅
- **TP 3RR**: 25045.35 ✅
- **TP 4RR**: 25029.31 ❌
- **TP 15RR**: 24852.77 ❌
- **PnL**: -16.05 points (-1.0R)
- **MFE**: 51.00 points
- **MAE**: 21.75 points

### Trade #1813 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-08 08:30:00
- **FVG 5m**: 25167.25 - 25174.25
- **Entrée**: 25175.25 @ 2025-10-08 08:57:00
- **Stop Loss**: 25154.67
- **Risk**: 20.58 points
- **TP 1RR**: 25195.83 ✅
- **TP 2RR**: 25216.42 ✅
- **TP 3RR**: 25237.00 ✅
- **TP 4RR**: 25257.58 ✅
- **TP 15RR**: 25484.00 ❌
- **PnL**: -20.58 points (-1.0R)
- **MFE**: 218.75 points
- **MAE**: 47.50 points

### Trade #1814 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-08 08:30:00
- **FVG 5m**: 25167.25 - 25174.25
- **Entrée**: 25175.25 @ 2025-10-08 08:57:00
- **Stop Loss**: 25154.67
- **Risk**: 20.58 points
- **TP 1RR**: 25195.83 ✅
- **TP 2RR**: 25216.42 ✅
- **TP 3RR**: 25237.00 ✅
- **TP 4RR**: 25257.58 ✅
- **TP 15RR**: 25484.00 ❌
- **PnL**: -20.58 points (-1.0R)
- **MFE**: 218.75 points
- **MAE**: 47.50 points

### Trade #1815 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-08 08:45:00
- **FVG 5m**: 25167.25 - 25174.25
- **Entrée**: 25175.25 @ 2025-10-08 08:57:00
- **Stop Loss**: 25154.67
- **Risk**: 20.58 points
- **TP 1RR**: 25195.83 ✅
- **TP 2RR**: 25216.42 ✅
- **TP 3RR**: 25237.00 ✅
- **TP 4RR**: 25257.58 ✅
- **TP 15RR**: 25484.00 ❌
- **PnL**: -20.58 points (-1.0R)
- **MFE**: 218.75 points
- **MAE**: 47.50 points

### Trade #1816 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-09 12:30:00
- **FVG 5m**: 25200.25 - 25203.75
- **Entrée**: 25209.25 @ 2025-10-09 13:11:00
- **Stop Loss**: 25187.65
- **Risk**: 21.60 points
- **TP 1RR**: 25230.85 ✅
- **TP 2RR**: 25252.45 ✅
- **TP 3RR**: 25274.05 ✅
- **TP 4RR**: 25295.65 ✅
- **TP 15RR**: 25533.25 ❌
- **PnL**: -21.60 points (-1.0R)
- **MFE**: 178.75 points
- **MAE**: 27.25 points

### Trade #1817 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-09 14:45:00
- **FVG 5m**: 25282.75 - 25286.50
- **Entrée**: 25287.25 @ 2025-10-09 15:59:00
- **Stop Loss**: 25270.11
- **Risk**: 17.14 points
- **TP 1RR**: 25304.39 ✅
- **TP 2RR**: 25321.53 ✅
- **TP 3RR**: 25338.67 ✅
- **TP 4RR**: 25355.82 ❌
- **TP 15RR**: 25544.37 ❌
- **PnL**: -17.14 points (-1.0R)
- **MFE**: 68.00 points
- **MAE**: 18.00 points

### Trade #1818 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 01:15:00
- **FVG 5m**: 25331.75 - 25336.25
- **Entrée**: 25313.75 @ 2025-10-10 01:36:00
- **Stop Loss**: 25348.92
- **Risk**: 35.17 points
- **TP 1RR**: 25278.58 ✅
- **TP 2RR**: 25243.41 ❌
- **TP 3RR**: 25208.25 ❌
- **TP 4RR**: 25173.08 ❌
- **TP 15RR**: 24786.23 ❌
- **PnL**: -35.17 points (-1.0R)
- **MFE**: 62.75 points
- **MAE**: 58.25 points

### Trade #1819 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 01:15:00
- **FVG 5m**: 25331.75 - 25336.25
- **Entrée**: 25313.75 @ 2025-10-10 01:36:00
- **Stop Loss**: 25348.92
- **Risk**: 35.17 points
- **TP 1RR**: 25278.58 ✅
- **TP 2RR**: 25243.41 ❌
- **TP 3RR**: 25208.25 ❌
- **TP 4RR**: 25173.08 ❌
- **TP 15RR**: 24786.23 ❌
- **PnL**: -35.17 points (-1.0R)
- **MFE**: 62.75 points
- **MAE**: 58.25 points

### Trade #1820 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 04:00:00
- **FVG 5m**: 25268.75 - 25275.50
- **Entrée**: 25276.00 @ 2025-10-10 05:08:00
- **Stop Loss**: 25256.12
- **Risk**: 19.88 points
- **TP 1RR**: 25295.88 ✅
- **TP 2RR**: 25315.77 ✅
- **TP 3RR**: 25335.65 ✅
- **TP 4RR**: 25355.54 ✅
- **TP 15RR**: 25574.27 ❌
- **PnL**: -19.88 points (-1.0R)
- **MFE**: 112.00 points
- **MAE**: 94.00 points

### Trade #1821 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 04:00:00
- **FVG 5m**: 25268.75 - 25275.50
- **Entrée**: 25276.00 @ 2025-10-10 05:08:00
- **Stop Loss**: 25256.12
- **Risk**: 19.88 points
- **TP 1RR**: 25295.88 ✅
- **TP 2RR**: 25315.77 ✅
- **TP 3RR**: 25335.65 ✅
- **TP 4RR**: 25355.54 ✅
- **TP 15RR**: 25574.27 ❌
- **PnL**: -19.88 points (-1.0R)
- **MFE**: 112.00 points
- **MAE**: 94.00 points

### Trade #1822 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 05:45:00
- **FVG 5m**: 25296.50 - 25299.50
- **Entrée**: 25300.25 @ 2025-10-10 05:59:00
- **Stop Loss**: 25283.85
- **Risk**: 16.40 points
- **TP 1RR**: 25316.65 ✅
- **TP 2RR**: 25333.05 ✅
- **TP 3RR**: 25349.44 ✅
- **TP 4RR**: 25365.84 ✅
- **TP 15RR**: 25546.22 ❌
- **PnL**: -16.40 points (-1.0R)
- **MFE**: 87.75 points
- **MAE**: 40.00 points

### Trade #1823 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 08:45:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25342.67
- **Risk**: 148.17 points
- **TP 1RR**: 25046.33 ✅
- **TP 2RR**: 24898.17 ✅
- **TP 3RR**: 24750.00 ✅
- **TP 4RR**: 24601.84 ✅
- **TP 15RR**: 22972.02 ❌
- **PnL**: -148.17 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 151.00 points

### Trade #1824 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25342.67
- **Risk**: 148.17 points
- **TP 1RR**: 25046.33 ✅
- **TP 2RR**: 24898.17 ✅
- **TP 3RR**: 24750.00 ✅
- **TP 4RR**: 24601.84 ✅
- **TP 15RR**: 22972.02 ❌
- **PnL**: -148.17 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 151.00 points

### Trade #1825 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25342.67
- **Risk**: 148.17 points
- **TP 1RR**: 25046.33 ✅
- **TP 2RR**: 24898.17 ✅
- **TP 3RR**: 24750.00 ✅
- **TP 4RR**: 24601.84 ✅
- **TP 15RR**: 22972.02 ❌
- **PnL**: -148.17 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 151.00 points

### Trade #1826 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25342.67
- **Risk**: 148.17 points
- **TP 1RR**: 25046.33 ✅
- **TP 2RR**: 24898.17 ✅
- **TP 3RR**: 24750.00 ✅
- **TP 4RR**: 24601.84 ✅
- **TP 15RR**: 22972.02 ❌
- **PnL**: -148.17 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 151.00 points

### Trade #1827 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25342.67
- **Risk**: 148.17 points
- **TP 1RR**: 25046.33 ✅
- **TP 2RR**: 24898.17 ✅
- **TP 3RR**: 24750.00 ✅
- **TP 4RR**: 24601.84 ✅
- **TP 15RR**: 22972.02 ❌
- **PnL**: -148.17 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 151.00 points

### Trade #1828 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25342.67
- **Risk**: 148.17 points
- **TP 1RR**: 25046.33 ✅
- **TP 2RR**: 24898.17 ✅
- **TP 3RR**: 24750.00 ✅
- **TP 4RR**: 24601.84 ✅
- **TP 15RR**: 22972.02 ❌
- **PnL**: -148.17 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 151.00 points

### Trade #1829 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25342.67
- **Risk**: 148.17 points
- **TP 1RR**: 25046.33 ✅
- **TP 2RR**: 24898.17 ✅
- **TP 3RR**: 24750.00 ✅
- **TP 4RR**: 24601.84 ✅
- **TP 15RR**: 22972.02 ❌
- **PnL**: -148.17 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 151.00 points

### Trade #1830 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 09:45:00
- **FVG 5m**: 24790.00 - 24810.00
- **Entrée**: 24861.25 @ 2025-10-10 10:44:00
- **Stop Loss**: 24777.60
- **Risk**: 83.65 points
- **TP 1RR**: 24944.90 ❌
- **TP 2RR**: 25028.54 ❌
- **TP 3RR**: 25112.19 ❌
- **TP 4RR**: 25195.83 ❌
- **TP 15RR**: 26115.93 ❌
- **PnL**: -83.65 points (-1.0R)
- **MFE**: 47.00 points
- **MAE**: 84.25 points

### Trade #1831 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:00:00
- **FVG 5m**: 24967.25 - 24993.00
- **Entrée**: 24941.25 @ 2025-10-10 10:18:00
- **Stop Loss**: 25005.50
- **Risk**: 64.25 points
- **TP 1RR**: 24877.00 ✅
- **TP 2RR**: 24812.76 ✅
- **TP 3RR**: 24748.51 ✅
- **TP 4RR**: 24684.26 ✅
- **TP 15RR**: 23977.55 ❌
- **PnL**: -64.25 points (-1.0R)
- **MFE**: 782.75 points
- **MAE**: 89.75 points

### Trade #1832 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:00:00
- **FVG 5m**: 24967.25 - 24993.00
- **Entrée**: 24941.25 @ 2025-10-10 10:18:00
- **Stop Loss**: 25005.50
- **Risk**: 64.25 points
- **TP 1RR**: 24877.00 ✅
- **TP 2RR**: 24812.76 ✅
- **TP 3RR**: 24748.51 ✅
- **TP 4RR**: 24684.26 ✅
- **TP 15RR**: 23977.55 ❌
- **PnL**: -64.25 points (-1.0R)
- **MFE**: 782.75 points
- **MAE**: 89.75 points

### Trade #1833 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 10:00:00
- **FVG 5m**: 24790.00 - 24810.00
- **Entrée**: 24861.25 @ 2025-10-10 10:44:00
- **Stop Loss**: 24777.60
- **Risk**: 83.65 points
- **TP 1RR**: 24944.90 ❌
- **TP 2RR**: 25028.54 ❌
- **TP 3RR**: 25112.19 ❌
- **TP 4RR**: 25195.83 ❌
- **TP 15RR**: 26115.93 ❌
- **PnL**: -83.65 points (-1.0R)
- **MFE**: 47.00 points
- **MAE**: 84.25 points

### Trade #1834 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 10:00:00
- **FVG 5m**: 24790.00 - 24810.00
- **Entrée**: 24861.25 @ 2025-10-10 10:44:00
- **Stop Loss**: 24777.60
- **Risk**: 83.65 points
- **TP 1RR**: 24944.90 ❌
- **TP 2RR**: 25028.54 ❌
- **TP 3RR**: 25112.19 ❌
- **TP 4RR**: 25195.83 ❌
- **TP 15RR**: 26115.93 ❌
- **PnL**: -83.65 points (-1.0R)
- **MFE**: 47.00 points
- **MAE**: 84.25 points

### Trade #1835 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 10:00:00
- **FVG 5m**: 24790.00 - 24810.00
- **Entrée**: 24861.25 @ 2025-10-10 10:44:00
- **Stop Loss**: 24777.60
- **Risk**: 83.65 points
- **TP 1RR**: 24944.90 ❌
- **TP 2RR**: 25028.54 ❌
- **TP 3RR**: 25112.19 ❌
- **TP 4RR**: 25195.83 ❌
- **TP 15RR**: 26115.93 ❌
- **PnL**: -83.65 points (-1.0R)
- **MFE**: 47.00 points
- **MAE**: 84.25 points

### Trade #1836 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 10:00:00
- **FVG 5m**: 24790.00 - 24810.00
- **Entrée**: 24861.25 @ 2025-10-10 10:44:00
- **Stop Loss**: 24777.60
- **Risk**: 83.65 points
- **TP 1RR**: 24944.90 ❌
- **TP 2RR**: 25028.54 ❌
- **TP 3RR**: 25112.19 ❌
- **TP 4RR**: 25195.83 ❌
- **TP 15RR**: 26115.93 ❌
- **PnL**: -83.65 points (-1.0R)
- **MFE**: 47.00 points
- **MAE**: 84.25 points

### Trade #1837 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:15:00
- **FVG 5m**: 24790.00 - 24802.50
- **Entrée**: 24780.00 @ 2025-10-10 10:31:00
- **Stop Loss**: 24814.90
- **Risk**: 34.90 points
- **TP 1RR**: 24745.10 ✅
- **TP 2RR**: 24710.20 ✅
- **TP 3RR**: 24675.30 ✅
- **TP 4RR**: 24640.40 ❌
- **TP 15RR**: 24256.48 ❌
- **PnL**: -34.90 points (-1.0R)
- **MFE**: 109.25 points
- **MAE**: 85.25 points

### Trade #1838 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:15:00
- **FVG 5m**: 24790.00 - 24802.50
- **Entrée**: 24780.00 @ 2025-10-10 10:31:00
- **Stop Loss**: 24814.90
- **Risk**: 34.90 points
- **TP 1RR**: 24745.10 ✅
- **TP 2RR**: 24710.20 ✅
- **TP 3RR**: 24675.30 ✅
- **TP 4RR**: 24640.40 ❌
- **TP 15RR**: 24256.48 ❌
- **PnL**: -34.90 points (-1.0R)
- **MFE**: 109.25 points
- **MAE**: 85.25 points

### Trade #1839 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 10:30:00
- **FVG 5m**: 24790.00 - 24810.00
- **Entrée**: 24861.25 @ 2025-10-10 10:44:00
- **Stop Loss**: 24777.60
- **Risk**: 83.65 points
- **TP 1RR**: 24944.90 ❌
- **TP 2RR**: 25028.54 ❌
- **TP 3RR**: 25112.19 ❌
- **TP 4RR**: 25195.83 ❌
- **TP 15RR**: 26115.93 ❌
- **PnL**: -83.65 points (-1.0R)
- **MFE**: 47.00 points
- **MAE**: 84.25 points

### Trade #1840 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 10:30:00
- **FVG 5m**: 24790.00 - 24810.00
- **Entrée**: 24861.25 @ 2025-10-10 10:44:00
- **Stop Loss**: 24777.60
- **Risk**: 83.65 points
- **TP 1RR**: 24944.90 ❌
- **TP 2RR**: 25028.54 ❌
- **TP 3RR**: 25112.19 ❌
- **TP 4RR**: 25195.83 ❌
- **TP 15RR**: 26115.93 ❌
- **PnL**: -83.65 points (-1.0R)
- **MFE**: 47.00 points
- **MAE**: 84.25 points

### Trade #1841 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 12:15:00
- **FVG 5m**: 24688.75 - 24694.25
- **Entrée**: 24695.25 @ 2025-10-10 12:27:00
- **Stop Loss**: 24676.41
- **Risk**: 18.84 points
- **TP 1RR**: 24714.09 ✅
- **TP 2RR**: 24732.94 ✅
- **TP 3RR**: 24751.78 ❌
- **TP 4RR**: 24770.63 ❌
- **TP 15RR**: 24977.92 ❌
- **PnL**: -18.84 points (-1.0R)
- **MFE**: 55.75 points
- **MAE**: 33.50 points

### Trade #1842 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 14:30:00
- **FVG 5m**: 24514.25 - 24520.25
- **Entrée**: 24535.50 @ 2025-10-10 14:44:00
- **Stop Loss**: 24501.99
- **Risk**: 33.51 points
- **TP 1RR**: 24569.01 ❌
- **TP 2RR**: 24602.51 ❌
- **TP 3RR**: 24636.02 ❌
- **TP 4RR**: 24669.53 ❌
- **TP 15RR**: 25038.11 ❌
- **PnL**: -33.51 points (-1.0R)
- **MFE**: 21.25 points
- **MAE**: 41.50 points

### Trade #1843 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 15:00:00
- **FVG 5m**: 24422.00 - 24542.00
- **Entrée**: 24735.50 @ 2025-10-12 17:00:00
- **Stop Loss**: 24409.79
- **Risk**: 325.71 points
- **TP 1RR**: 25061.21 ✅
- **TP 2RR**: 25386.92 ✅
- **TP 3RR**: 25712.63 ✅
- **TP 4RR**: 26038.34 ✅
- **TP 15RR**: 29621.16 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1663.50 points
- **MAE**: 325.50 points

### Trade #1844 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-12 17:00:00
- **FVG 5m**: 24698.00 - 24703.25
- **Entrée**: 24719.25 @ 2025-10-12 17:18:00
- **Stop Loss**: 24685.65
- **Risk**: 33.60 points
- **TP 1RR**: 24752.85 ❌
- **TP 2RR**: 24786.45 ❌
- **TP 3RR**: 24820.05 ❌
- **TP 4RR**: 24853.65 ❌
- **TP 15RR**: 25223.23 ❌
- **PnL**: -33.60 points (-1.0R)
- **MFE**: 20.75 points
- **MAE**: 38.25 points

### Trade #1845 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 02:15:00
- **FVG 5m**: 24859.25 - 24863.25
- **Entrée**: 24867.25 @ 2025-10-13 03:52:00
- **Stop Loss**: 24846.82
- **Risk**: 20.43 points
- **TP 1RR**: 24887.68 ❌
- **TP 2RR**: 24908.11 ❌
- **TP 3RR**: 24928.54 ❌
- **TP 4RR**: 24948.97 ❌
- **TP 15RR**: 25173.69 ❌
- **PnL**: -20.43 points (-1.0R)
- **MFE**: 13.75 points
- **MAE**: 25.50 points

### Trade #1846 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 03:30:00
- **FVG 5m**: 24847.50 - 24859.25
- **Entrée**: 24845.00 @ 2025-10-13 05:43:00
- **Stop Loss**: 24871.68
- **Risk**: 26.68 points
- **TP 1RR**: 24818.32 ✅
- **TP 2RR**: 24791.64 ✅
- **TP 3RR**: 24764.96 ✅
- **TP 4RR**: 24738.28 ✅
- **TP 15RR**: 24444.81 ❌
- **PnL**: -26.68 points (-1.0R)
- **MFE**: 112.00 points
- **MAE**: 30.00 points

### Trade #1847 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 06:00:00
- **FVG 5m**: 24792.00 - 24809.00
- **Entrée**: 24814.25 @ 2025-10-13 07:14:00
- **Stop Loss**: 24779.60
- **Risk**: 34.65 points
- **TP 1RR**: 24848.90 ✅
- **TP 2RR**: 24883.54 ✅
- **TP 3RR**: 24918.19 ❌
- **TP 4RR**: 24952.83 ❌
- **TP 15RR**: 25333.94 ❌
- **PnL**: -34.65 points (-1.0R)
- **MFE**: 75.00 points
- **MAE**: 56.00 points

### Trade #1848 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 06:30:00
- **FVG 5m**: 24792.00 - 24809.00
- **Entrée**: 24814.25 @ 2025-10-13 07:14:00
- **Stop Loss**: 24779.60
- **Risk**: 34.65 points
- **TP 1RR**: 24848.90 ✅
- **TP 2RR**: 24883.54 ✅
- **TP 3RR**: 24918.19 ❌
- **TP 4RR**: 24952.83 ❌
- **TP 15RR**: 25333.94 ❌
- **PnL**: -34.65 points (-1.0R)
- **MFE**: 75.00 points
- **MAE**: 56.00 points

### Trade #1849 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 11:15:00
- **FVG 5m**: 24922.75 - 24945.50
- **Entrée**: 24919.50 @ 2025-10-13 12:12:00
- **Stop Loss**: 24957.97
- **Risk**: 38.47 points
- **TP 1RR**: 24881.03 ❌
- **TP 2RR**: 24842.55 ❌
- **TP 3RR**: 24804.08 ❌
- **TP 4RR**: 24765.61 ❌
- **TP 15RR**: 24342.41 ❌
- **PnL**: -38.47 points (-1.0R)
- **MFE**: 31.00 points
- **MAE**: 45.50 points

### Trade #1850 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 12:00:00
- **FVG 5m**: 24922.75 - 24945.50
- **Entrée**: 24919.50 @ 2025-10-13 12:12:00
- **Stop Loss**: 24957.97
- **Risk**: 38.47 points
- **TP 1RR**: 24881.03 ❌
- **TP 2RR**: 24842.55 ❌
- **TP 3RR**: 24804.08 ❌
- **TP 4RR**: 24765.61 ❌
- **TP 15RR**: 24342.41 ❌
- **PnL**: -38.47 points (-1.0R)
- **MFE**: 31.00 points
- **MAE**: 45.50 points

### Trade #1851 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24987.00 - 24995.50
- **Entrée**: 24998.50 @ 2025-10-13 19:29:00
- **Stop Loss**: 24974.51
- **Risk**: 23.99 points
- **TP 1RR**: 25022.49 ✅
- **TP 2RR**: 25046.49 ❌
- **TP 3RR**: 25070.48 ❌
- **TP 4RR**: 25094.47 ❌
- **TP 15RR**: 25358.40 ❌
- **PnL**: -23.99 points (-1.0R)
- **MFE**: 45.75 points
- **MAE**: 31.50 points

### Trade #1852 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24987.00 - 24995.50
- **Entrée**: 24998.50 @ 2025-10-13 19:29:00
- **Stop Loss**: 24974.51
- **Risk**: 23.99 points
- **TP 1RR**: 25022.49 ✅
- **TP 2RR**: 25046.49 ❌
- **TP 3RR**: 25070.48 ❌
- **TP 4RR**: 25094.47 ❌
- **TP 15RR**: 25358.40 ❌
- **PnL**: -23.99 points (-1.0R)
- **MFE**: 45.75 points
- **MAE**: 31.50 points

### Trade #1853 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24987.00 - 24995.50
- **Entrée**: 24998.50 @ 2025-10-13 19:29:00
- **Stop Loss**: 24974.51
- **Risk**: 23.99 points
- **TP 1RR**: 25022.49 ✅
- **TP 2RR**: 25046.49 ❌
- **TP 3RR**: 25070.48 ❌
- **TP 4RR**: 25094.47 ❌
- **TP 15RR**: 25358.40 ❌
- **PnL**: -23.99 points (-1.0R)
- **MFE**: 45.75 points
- **MAE**: 31.50 points

### Trade #1854 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24987.00 - 24995.50
- **Entrée**: 24998.50 @ 2025-10-13 19:29:00
- **Stop Loss**: 24974.51
- **Risk**: 23.99 points
- **TP 1RR**: 25022.49 ✅
- **TP 2RR**: 25046.49 ❌
- **TP 3RR**: 25070.48 ❌
- **TP 4RR**: 25094.47 ❌
- **TP 15RR**: 25358.40 ❌
- **PnL**: -23.99 points (-1.0R)
- **MFE**: 45.75 points
- **MAE**: 31.50 points

### Trade #1855 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 21:45:00
- **FVG 5m**: 24943.25 - 24953.75
- **Entrée**: 24938.00 @ 2025-10-13 22:04:00
- **Stop Loss**: 24966.23
- **Risk**: 28.23 points
- **TP 1RR**: 24909.77 ✅
- **TP 2RR**: 24881.55 ✅
- **TP 3RR**: 24853.32 ✅
- **TP 4RR**: 24825.09 ✅
- **TP 15RR**: 24514.60 ✅
- **PnL**: 423.40 points (15.0R)
- **MFE**: 426.00 points
- **MAE**: 5.25 points

### Trade #1856 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 21:45:00
- **FVG 5m**: 24943.25 - 24953.75
- **Entrée**: 24938.00 @ 2025-10-13 22:04:00
- **Stop Loss**: 24966.23
- **Risk**: 28.23 points
- **TP 1RR**: 24909.77 ✅
- **TP 2RR**: 24881.55 ✅
- **TP 3RR**: 24853.32 ✅
- **TP 4RR**: 24825.09 ✅
- **TP 15RR**: 24514.60 ✅
- **PnL**: 423.40 points (15.0R)
- **MFE**: 426.00 points
- **MAE**: 5.25 points

### Trade #1857 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-14 00:30:00
- **FVG 5m**: 24702.25 - 24712.00
- **Entrée**: 24702.00 @ 2025-10-14 01:38:00
- **Stop Loss**: 24724.36
- **Risk**: 22.36 points
- **TP 1RR**: 24679.64 ✅
- **TP 2RR**: 24657.29 ✅
- **TP 3RR**: 24634.93 ✅
- **TP 4RR**: 24612.58 ❌
- **TP 15RR**: 24366.66 ❌
- **PnL**: -22.36 points (-1.0R)
- **MFE**: 73.75 points
- **MAE**: 24.00 points

### Trade #1858 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 01:00:00
- **FVG 5m**: 24628.25 - 24630.75
- **Entrée**: 24641.50 @ 2025-10-14 03:11:00
- **Stop Loss**: 24615.94
- **Risk**: 25.56 points
- **TP 1RR**: 24667.06 ✅
- **TP 2RR**: 24692.63 ✅
- **TP 3RR**: 24718.19 ❌
- **TP 4RR**: 24743.76 ❌
- **TP 15RR**: 25024.96 ❌
- **PnL**: -25.56 points (-1.0R)
- **MFE**: 71.50 points
- **MAE**: 27.00 points

### Trade #1859 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 01:00:00
- **FVG 5m**: 24628.25 - 24630.75
- **Entrée**: 24641.50 @ 2025-10-14 03:11:00
- **Stop Loss**: 24615.94
- **Risk**: 25.56 points
- **TP 1RR**: 24667.06 ✅
- **TP 2RR**: 24692.63 ✅
- **TP 3RR**: 24718.19 ❌
- **TP 4RR**: 24743.76 ❌
- **TP 15RR**: 25024.96 ❌
- **PnL**: -25.56 points (-1.0R)
- **MFE**: 71.50 points
- **MAE**: 27.00 points

### Trade #1860 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 06:00:00
- **FVG 5m**: 24605.00 - 24615.50
- **Entrée**: 24620.25 @ 2025-10-14 06:21:00
- **Stop Loss**: 24592.70
- **Risk**: 27.55 points
- **TP 1RR**: 24647.80 ✅
- **TP 2RR**: 24675.36 ❌
- **TP 3RR**: 24702.91 ❌
- **TP 4RR**: 24730.46 ❌
- **TP 15RR**: 25033.54 ❌
- **PnL**: -27.55 points (-1.0R)
- **MFE**: 44.75 points
- **MAE**: 64.75 points

### Trade #1861 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 08:45:00
- **FVG 5m**: 24638.00 - 24686.50
- **Entrée**: 24688.50 @ 2025-10-14 09:24:00
- **Stop Loss**: 24625.68
- **Risk**: 62.82 points
- **TP 1RR**: 24751.32 ✅
- **TP 2RR**: 24814.14 ✅
- **TP 3RR**: 24876.96 ✅
- **TP 4RR**: 24939.78 ✅
- **TP 15RR**: 25630.78 ❌
- **PnL**: -62.82 points (-1.0R)
- **MFE**: 491.00 points
- **MAE**: 69.25 points

### Trade #1862 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 08:45:00
- **FVG 5m**: 24638.00 - 24686.50
- **Entrée**: 24688.50 @ 2025-10-14 09:24:00
- **Stop Loss**: 24625.68
- **Risk**: 62.82 points
- **TP 1RR**: 24751.32 ✅
- **TP 2RR**: 24814.14 ✅
- **TP 3RR**: 24876.96 ✅
- **TP 4RR**: 24939.78 ✅
- **TP 15RR**: 25630.78 ❌
- **PnL**: -62.82 points (-1.0R)
- **MFE**: 491.00 points
- **MAE**: 69.25 points

### Trade #1863 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-14 09:45:00
- **FVG 5m**: 24792.50 - 24795.50
- **Entrée**: 24789.25 @ 2025-10-14 11:04:00
- **Stop Loss**: 24807.90
- **Risk**: 18.65 points
- **TP 1RR**: 24770.60 ✅
- **TP 2RR**: 24751.95 ❌
- **TP 3RR**: 24733.31 ❌
- **TP 4RR**: 24714.66 ❌
- **TP 15RR**: 24509.53 ❌
- **PnL**: -18.65 points (-1.0R)
- **MFE**: 27.25 points
- **MAE**: 18.75 points

### Trade #1864 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 11:30:00
- **FVG 5m**: 24899.00 - 24906.75
- **Entrée**: 24910.50 @ 2025-10-14 12:06:00
- **Stop Loss**: 24886.55
- **Risk**: 23.95 points
- **TP 1RR**: 24934.45 ✅
- **TP 2RR**: 24958.40 ❌
- **TP 3RR**: 24982.35 ❌
- **TP 4RR**: 25006.30 ❌
- **TP 15RR**: 25269.74 ❌
- **PnL**: -23.95 points (-1.0R)
- **MFE**: 27.50 points
- **MAE**: 25.00 points

### Trade #1865 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 11:30:00
- **FVG 5m**: 24899.00 - 24906.75
- **Entrée**: 24910.50 @ 2025-10-14 12:06:00
- **Stop Loss**: 24886.55
- **Risk**: 23.95 points
- **TP 1RR**: 24934.45 ✅
- **TP 2RR**: 24958.40 ❌
- **TP 3RR**: 24982.35 ❌
- **TP 4RR**: 25006.30 ❌
- **TP 15RR**: 25269.74 ❌
- **PnL**: -23.95 points (-1.0R)
- **MFE**: 27.50 points
- **MAE**: 25.00 points

### Trade #1866 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-14 22:30:00
- **FVG 5m**: 24809.00 - 24816.00
- **Entrée**: 24808.25 @ 2025-10-14 22:43:00
- **Stop Loss**: 24828.41
- **Risk**: 20.16 points
- **TP 1RR**: 24788.09 ❌
- **TP 2RR**: 24767.93 ❌
- **TP 3RR**: 24747.78 ❌
- **TP 4RR**: 24727.62 ❌
- **TP 15RR**: 24505.88 ❌
- **PnL**: -20.16 points (-1.0R)
- **MFE**: 11.75 points
- **MAE**: 34.75 points

### Trade #1867 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 08:30:00
- **FVG 5m**: 24987.25 - 25013.00
- **Entrée**: 25021.25 @ 2025-10-15 08:58:00
- **Stop Loss**: 24974.76
- **Risk**: 46.49 points
- **TP 1RR**: 25067.74 ✅
- **TP 2RR**: 25114.24 ✅
- **TP 3RR**: 25160.73 ❌
- **TP 4RR**: 25207.22 ❌
- **TP 15RR**: 25718.65 ❌
- **PnL**: -46.49 points (-1.0R)
- **MFE**: 93.75 points
- **MAE**: 49.25 points

### Trade #1868 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 10:30:00
- **FVG 5m**: 24961.25 - 24967.25
- **Entrée**: 24958.75 @ 2025-10-15 10:41:00
- **Stop Loss**: 24979.73
- **Risk**: 20.98 points
- **TP 1RR**: 24937.77 ✅
- **TP 2RR**: 24916.78 ✅
- **TP 3RR**: 24895.80 ✅
- **TP 4RR**: 24874.82 ❌
- **TP 15RR**: 24644.00 ❌
- **PnL**: -20.98 points (-1.0R)
- **MFE**: 81.50 points
- **MAE**: 21.50 points

### Trade #1869 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 10:30:00
- **FVG 5m**: 24961.25 - 24967.25
- **Entrée**: 24958.75 @ 2025-10-15 10:41:00
- **Stop Loss**: 24979.73
- **Risk**: 20.98 points
- **TP 1RR**: 24937.77 ✅
- **TP 2RR**: 24916.78 ✅
- **TP 3RR**: 24895.80 ✅
- **TP 4RR**: 24874.82 ❌
- **TP 15RR**: 24644.00 ❌
- **PnL**: -20.98 points (-1.0R)
- **MFE**: 81.50 points
- **MAE**: 21.50 points

### Trade #1870 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 10:30:00
- **FVG 5m**: 24961.25 - 24967.25
- **Entrée**: 24958.75 @ 2025-10-15 10:41:00
- **Stop Loss**: 24979.73
- **Risk**: 20.98 points
- **TP 1RR**: 24937.77 ✅
- **TP 2RR**: 24916.78 ✅
- **TP 3RR**: 24895.80 ✅
- **TP 4RR**: 24874.82 ❌
- **TP 15RR**: 24644.00 ❌
- **PnL**: -20.98 points (-1.0R)
- **MFE**: 81.50 points
- **MAE**: 21.50 points

### Trade #1871 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 10:45:00
- **FVG 5m**: 24791.50 - 24805.50
- **Entrée**: 24809.00 @ 2025-10-15 12:36:00
- **Stop Loss**: 24779.10
- **Risk**: 29.90 points
- **TP 1RR**: 24838.90 ✅
- **TP 2RR**: 24868.79 ✅
- **TP 3RR**: 24898.69 ✅
- **TP 4RR**: 24928.58 ✅
- **TP 15RR**: 25257.44 ❌
- **PnL**: -29.90 points (-1.0R)
- **MFE**: 370.50 points
- **MAE**: 53.00 points

### Trade #1872 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 11:45:00
- **FVG 5m**: 24857.75 - 24892.25
- **Entrée**: 24832.75 @ 2025-10-15 12:05:00
- **Stop Loss**: 24904.70
- **Risk**: 71.95 points
- **TP 1RR**: 24760.80 ✅
- **TP 2RR**: 24688.86 ✅
- **TP 3RR**: 24616.91 ❌
- **TP 4RR**: 24544.97 ❌
- **TP 15RR**: 23753.56 ❌
- **PnL**: -71.95 points (-1.0R)
- **MFE**: 169.50 points
- **MAE**: 74.25 points

### Trade #1873 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 12:00:00
- **FVG 5m**: 24750.75 - 24776.00
- **Entrée**: 24723.50 @ 2025-10-15 12:11:00
- **Stop Loss**: 24788.39
- **Risk**: 64.89 points
- **TP 1RR**: 24658.61 ❌
- **TP 2RR**: 24593.72 ❌
- **TP 3RR**: 24528.84 ❌
- **TP 4RR**: 24463.95 ❌
- **TP 15RR**: 23750.18 ❌
- **PnL**: -64.89 points (-1.0R)
- **MFE**: 60.25 points
- **MAE**: 69.50 points

### Trade #1874 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:15:00
- **FVG 5m**: 24791.50 - 24805.50
- **Entrée**: 24809.00 @ 2025-10-15 12:36:00
- **Stop Loss**: 24779.10
- **Risk**: 29.90 points
- **TP 1RR**: 24838.90 ✅
- **TP 2RR**: 24868.79 ✅
- **TP 3RR**: 24898.69 ✅
- **TP 4RR**: 24928.58 ✅
- **TP 15RR**: 25257.44 ❌
- **PnL**: -29.90 points (-1.0R)
- **MFE**: 370.50 points
- **MAE**: 53.00 points

### Trade #1875 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:15:00
- **FVG 5m**: 24791.50 - 24805.50
- **Entrée**: 24809.00 @ 2025-10-15 12:36:00
- **Stop Loss**: 24779.10
- **Risk**: 29.90 points
- **TP 1RR**: 24838.90 ✅
- **TP 2RR**: 24868.79 ✅
- **TP 3RR**: 24898.69 ✅
- **TP 4RR**: 24928.58 ✅
- **TP 15RR**: 25257.44 ❌
- **PnL**: -29.90 points (-1.0R)
- **MFE**: 370.50 points
- **MAE**: 53.00 points

### Trade #1876 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:30:00
- **FVG 5m**: 24825.00 - 24836.75
- **Entrée**: 24838.00 @ 2025-10-15 12:44:00
- **Stop Loss**: 24812.59
- **Risk**: 25.41 points
- **TP 1RR**: 24863.41 ✅
- **TP 2RR**: 24888.82 ✅
- **TP 3RR**: 24914.24 ✅
- **TP 4RR**: 24939.65 ✅
- **TP 15RR**: 25219.19 ❌
- **PnL**: -25.41 points (-1.0R)
- **MFE**: 341.50 points
- **MAE**: 36.50 points

### Trade #1877 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:45:00
- **FVG 5m**: 24926.75 - 24935.75
- **Entrée**: 24939.00 @ 2025-10-15 14:16:00
- **Stop Loss**: 24914.29
- **Risk**: 24.71 points
- **TP 1RR**: 24963.71 ❌
- **TP 2RR**: 24988.43 ❌
- **TP 3RR**: 25013.14 ❌
- **TP 4RR**: 25037.85 ❌
- **TP 15RR**: 25309.70 ❌
- **PnL**: -24.71 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 31.25 points

### Trade #1878 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 13:30:00
- **FVG 5m**: 24934.75 - 24938.75
- **Entrée**: 24933.75 @ 2025-10-15 14:33:00
- **Stop Loss**: 24951.22
- **Risk**: 17.47 points
- **TP 1RR**: 24916.28 ✅
- **TP 2RR**: 24898.81 ✅
- **TP 3RR**: 24881.34 ✅
- **TP 4RR**: 24863.87 ✅
- **TP 15RR**: 24671.71 ❌
- **PnL**: -17.47 points (-1.0R)
- **MFE**: 88.75 points
- **MAE**: 30.50 points

### Trade #1879 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 07:00:00
- **FVG 5m**: 25069.25 - 25072.00
- **Entrée**: 25065.25 @ 2025-10-16 08:22:00
- **Stop Loss**: 25084.54
- **Risk**: 19.29 points
- **TP 1RR**: 25045.96 ✅
- **TP 2RR**: 25026.68 ❌
- **TP 3RR**: 25007.39 ❌
- **TP 4RR**: 24988.11 ❌
- **TP 15RR**: 24775.96 ❌
- **PnL**: -19.29 points (-1.0R)
- **MFE**: 24.75 points
- **MAE**: 40.50 points

### Trade #1880 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 09:45:00
- **FVG 5m**: 25087.50 - 25099.50
- **Entrée**: 25085.25 @ 2025-10-16 10:24:00
- **Stop Loss**: 25112.05
- **Risk**: 26.80 points
- **TP 1RR**: 25058.45 ✅
- **TP 2RR**: 25031.65 ✅
- **TP 3RR**: 25004.85 ✅
- **TP 4RR**: 24978.05 ✅
- **TP 15RR**: 24683.25 ✅
- **PnL**: 402.00 points (15.0R)
- **MFE**: 405.50 points
- **MAE**: 2.25 points

### Trade #1881 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 10:45:00
- **FVG 5m**: 24942.75 - 24952.00
- **Entrée**: 24930.50 @ 2025-10-16 11:18:00
- **Stop Loss**: 24964.48
- **Risk**: 33.98 points
- **TP 1RR**: 24896.52 ✅
- **TP 2RR**: 24862.55 ✅
- **TP 3RR**: 24828.57 ✅
- **TP 4RR**: 24794.60 ✅
- **TP 15RR**: 24420.86 ❌
- **PnL**: -33.98 points (-1.0R)
- **MFE**: 198.50 points
- **MAE**: 34.25 points

### Trade #1882 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 11:15:00
- **FVG 5m**: 24877.75 - 24895.00
- **Entrée**: 24875.25 @ 2025-10-16 11:26:00
- **Stop Loss**: 24907.45
- **Risk**: 32.20 points
- **TP 1RR**: 24843.05 ✅
- **TP 2RR**: 24810.86 ✅
- **TP 3RR**: 24778.66 ✅
- **TP 4RR**: 24746.46 ✅
- **TP 15RR**: 24392.29 ❌
- **PnL**: -32.20 points (-1.0R)
- **MFE**: 143.25 points
- **MAE**: 37.50 points

### Trade #1883 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 11:45:00
- **FVG 5m**: 24728.00 - 24752.50
- **Entrée**: 24762.00 @ 2025-10-16 13:43:00
- **Stop Loss**: 24715.64
- **Risk**: 46.36 points
- **TP 1RR**: 24808.36 ✅
- **TP 2RR**: 24854.73 ❌
- **TP 3RR**: 24901.09 ❌
- **TP 4RR**: 24947.46 ❌
- **TP 15RR**: 25457.46 ❌
- **PnL**: -46.36 points (-1.0R)
- **MFE**: 58.75 points
- **MAE**: 51.50 points

### Trade #1884 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 11:45:00
- **FVG 5m**: 24728.00 - 24752.50
- **Entrée**: 24762.00 @ 2025-10-16 13:43:00
- **Stop Loss**: 24715.64
- **Risk**: 46.36 points
- **TP 1RR**: 24808.36 ✅
- **TP 2RR**: 24854.73 ❌
- **TP 3RR**: 24901.09 ❌
- **TP 4RR**: 24947.46 ❌
- **TP 15RR**: 25457.46 ❌
- **PnL**: -46.36 points (-1.0R)
- **MFE**: 58.75 points
- **MAE**: 51.50 points

### Trade #1885 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 11:45:00
- **FVG 5m**: 24728.00 - 24752.50
- **Entrée**: 24762.00 @ 2025-10-16 13:43:00
- **Stop Loss**: 24715.64
- **Risk**: 46.36 points
- **TP 1RR**: 24808.36 ✅
- **TP 2RR**: 24854.73 ❌
- **TP 3RR**: 24901.09 ❌
- **TP 4RR**: 24947.46 ❌
- **TP 15RR**: 25457.46 ❌
- **PnL**: -46.36 points (-1.0R)
- **MFE**: 58.75 points
- **MAE**: 51.50 points

### Trade #1886 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 13:30:00
- **FVG 5m**: 24728.00 - 24752.50
- **Entrée**: 24762.00 @ 2025-10-16 13:43:00
- **Stop Loss**: 24715.64
- **Risk**: 46.36 points
- **TP 1RR**: 24808.36 ✅
- **TP 2RR**: 24854.73 ❌
- **TP 3RR**: 24901.09 ❌
- **TP 4RR**: 24947.46 ❌
- **TP 15RR**: 25457.46 ❌
- **PnL**: -46.36 points (-1.0R)
- **MFE**: 58.75 points
- **MAE**: 51.50 points

### Trade #1887 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 22:45:00
- **FVG 5m**: 24640.00 - 24658.00
- **Entrée**: 24659.50 @ 2025-10-17 00:54:00
- **Stop Loss**: 24627.68
- **Risk**: 31.82 points
- **TP 1RR**: 24691.32 ❌
- **TP 2RR**: 24723.14 ❌
- **TP 3RR**: 24754.96 ❌
- **TP 4RR**: 24786.78 ❌
- **TP 15RR**: 25136.80 ❌
- **PnL**: -31.82 points (-1.0R)
- **MFE**: 31.25 points
- **MAE**: 36.75 points

### Trade #1888 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 22:45:00
- **FVG 5m**: 24640.00 - 24658.00
- **Entrée**: 24659.50 @ 2025-10-17 00:54:00
- **Stop Loss**: 24627.68
- **Risk**: 31.82 points
- **TP 1RR**: 24691.32 ❌
- **TP 2RR**: 24723.14 ❌
- **TP 3RR**: 24754.96 ❌
- **TP 4RR**: 24786.78 ❌
- **TP 15RR**: 25136.80 ❌
- **PnL**: -31.82 points (-1.0R)
- **MFE**: 31.25 points
- **MAE**: 36.75 points

### Trade #1889 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-17 00:30:00
- **FVG 5m**: 24669.75 - 24677.25
- **Entrée**: 24668.00 @ 2025-10-17 01:11:00
- **Stop Loss**: 24689.59
- **Risk**: 21.59 points
- **TP 1RR**: 24646.41 ✅
- **TP 2RR**: 24624.82 ✅
- **TP 3RR**: 24603.23 ✅
- **TP 4RR**: 24581.65 ✅
- **TP 15RR**: 24344.17 ❌
- **PnL**: -21.59 points (-1.0R)
- **MFE**: 258.00 points
- **MAE**: 52.50 points

### Trade #1890 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-17 00:45:00
- **FVG 5m**: 24674.75 - 24677.25
- **Entrée**: 24677.75 @ 2025-10-17 01:04:00
- **Stop Loss**: 24662.41
- **Risk**: 15.34 points
- **TP 1RR**: 24693.09 ❌
- **TP 2RR**: 24708.42 ❌
- **TP 3RR**: 24723.76 ❌
- **TP 4RR**: 24739.10 ❌
- **TP 15RR**: 24907.81 ❌
- **PnL**: -15.34 points (-1.0R)
- **MFE**: 13.00 points
- **MAE**: 20.25 points

### Trade #1891 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-17 08:45:00
- **FVG 5m**: 24861.75 - 24894.75
- **Entrée**: 24857.75 @ 2025-10-17 09:34:00
- **Stop Loss**: 24907.20
- **Risk**: 49.45 points
- **TP 1RR**: 24808.30 ✅
- **TP 2RR**: 24758.86 ✅
- **TP 3RR**: 24709.41 ✅
- **TP 4RR**: 24659.96 ❌
- **TP 15RR**: 24116.04 ❌
- **PnL**: -49.45 points (-1.0R)
- **MFE**: 182.75 points
- **MAE**: 50.25 points

### Trade #1892 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-17 08:45:00
- **FVG 5m**: 24861.75 - 24894.75
- **Entrée**: 24857.75 @ 2025-10-17 09:34:00
- **Stop Loss**: 24907.20
- **Risk**: 49.45 points
- **TP 1RR**: 24808.30 ✅
- **TP 2RR**: 24758.86 ✅
- **TP 3RR**: 24709.41 ✅
- **TP 4RR**: 24659.96 ❌
- **TP 15RR**: 24116.04 ❌
- **PnL**: -49.45 points (-1.0R)
- **MFE**: 182.75 points
- **MAE**: 50.25 points

### Trade #1893 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-17 13:15:00
- **FVG 5m**: 25011.25 - 25021.00
- **Entrée**: 25023.25 @ 2025-10-17 15:21:00
- **Stop Loss**: 24998.74
- **Risk**: 24.51 points
- **TP 1RR**: 25047.76 ✅
- **TP 2RR**: 25072.26 ✅
- **TP 3RR**: 25096.77 ✅
- **TP 4RR**: 25121.27 ❌
- **TP 15RR**: 25390.83 ❌
- **PnL**: -24.51 points (-1.0R)
- **MFE**: 76.00 points
- **MAE**: 27.25 points

### Trade #1894 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-17 14:00:00
- **FVG 5m**: 25011.25 - 25021.00
- **Entrée**: 25023.25 @ 2025-10-17 15:21:00
- **Stop Loss**: 24998.74
- **Risk**: 24.51 points
- **TP 1RR**: 25047.76 ✅
- **TP 2RR**: 25072.26 ✅
- **TP 3RR**: 25096.77 ✅
- **TP 4RR**: 25121.27 ❌
- **TP 15RR**: 25390.83 ❌
- **PnL**: -24.51 points (-1.0R)
- **MFE**: 76.00 points
- **MAE**: 27.25 points

### Trade #1895 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-19 17:15:00
- **FVG 5m**: 25053.50 - 25056.50
- **Entrée**: 25052.50 @ 2025-10-19 18:01:00
- **Stop Loss**: 25069.03
- **Risk**: 16.53 points
- **TP 1RR**: 25035.97 ✅
- **TP 2RR**: 25019.44 ✅
- **TP 3RR**: 25002.92 ✅
- **TP 4RR**: 24986.39 ✅
- **TP 15RR**: 24804.58 ❌
- **PnL**: -16.53 points (-1.0R)
- **MFE**: 96.75 points
- **MAE**: 17.25 points

### Trade #1896 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-19 19:15:00
- **FVG 5m**: 24983.75 - 24998.25
- **Entrée**: 25004.00 @ 2025-10-19 19:39:00
- **Stop Loss**: 24971.26
- **Risk**: 32.74 points
- **TP 1RR**: 25036.74 ✅
- **TP 2RR**: 25069.48 ✅
- **TP 3RR**: 25102.23 ✅
- **TP 4RR**: 25134.97 ✅
- **TP 15RR**: 25495.13 ❌
- **PnL**: -32.74 points (-1.0R)
- **MFE**: 364.00 points
- **MAE**: 94.00 points

### Trade #1897 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-20 03:45:00
- **FVG 5m**: 25074.25 - 25088.00
- **Entrée**: 25071.50 @ 2025-10-20 05:44:00
- **Stop Loss**: 25100.54
- **Risk**: 29.04 points
- **TP 1RR**: 25042.46 ✅
- **TP 2RR**: 25013.41 ❌
- **TP 3RR**: 24984.37 ❌
- **TP 4RR**: 24955.32 ❌
- **TP 15RR**: 24635.84 ❌
- **PnL**: -29.04 points (-1.0R)
- **MFE**: 33.50 points
- **MAE**: 34.75 points

### Trade #1898 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-20 06:00:00
- **FVG 5m**: 25065.75 - 25069.25
- **Entrée**: 25070.50 @ 2025-10-20 06:12:00
- **Stop Loss**: 25053.22
- **Risk**: 17.28 points
- **TP 1RR**: 25087.78 ✅
- **TP 2RR**: 25105.07 ✅
- **TP 3RR**: 25122.35 ✅
- **TP 4RR**: 25139.63 ✅
- **TP 15RR**: 25329.74 ✅
- **PnL**: 259.24 points (15.0R)
- **MFE**: 265.25 points
- **MAE**: 8.75 points

### Trade #1899 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-20 09:15:00
- **FVG 5m**: 25250.00 - 25266.25
- **Entrée**: 25278.00 @ 2025-10-20 09:27:00
- **Stop Loss**: 25237.38
- **Risk**: 40.62 points
- **TP 1RR**: 25318.62 ✅
- **TP 2RR**: 25359.25 ✅
- **TP 3RR**: 25399.88 ❌
- **TP 4RR**: 25440.50 ❌
- **TP 15RR**: 25887.38 ❌
- **PnL**: -40.62 points (-1.0R)
- **MFE**: 90.00 points
- **MAE**: 44.00 points

### Trade #1900 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-20 09:30:00
- **FVG 5m**: 25287.50 - 25294.75
- **Entrée**: 25295.50 @ 2025-10-20 09:41:00
- **Stop Loss**: 25274.86
- **Risk**: 20.64 points
- **TP 1RR**: 25316.14 ✅
- **TP 2RR**: 25336.79 ✅
- **TP 3RR**: 25357.43 ✅
- **TP 4RR**: 25378.07 ❌
- **TP 15RR**: 25605.16 ❌
- **PnL**: -20.64 points (-1.0R)
- **MFE**: 72.50 points
- **MAE**: 25.50 points

### Trade #1901 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-20 09:30:00
- **FVG 5m**: 25287.50 - 25294.75
- **Entrée**: 25295.50 @ 2025-10-20 09:41:00
- **Stop Loss**: 25274.86
- **Risk**: 20.64 points
- **TP 1RR**: 25316.14 ✅
- **TP 2RR**: 25336.79 ✅
- **TP 3RR**: 25357.43 ✅
- **TP 4RR**: 25378.07 ❌
- **TP 15RR**: 25605.16 ❌
- **PnL**: -20.64 points (-1.0R)
- **MFE**: 72.50 points
- **MAE**: 25.50 points

### Trade #1902 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-20 20:15:00
- **FVG 5m**: 25342.00 - 25345.00
- **Entrée**: 25339.75 @ 2025-10-20 20:27:00
- **Stop Loss**: 25357.67
- **Risk**: 17.92 points
- **TP 1RR**: 25321.83 ❌
- **TP 2RR**: 25303.90 ❌
- **TP 3RR**: 25285.98 ❌
- **TP 4RR**: 25268.06 ❌
- **TP 15RR**: 25070.91 ❌
- **PnL**: -17.92 points (-1.0R)
- **MFE**: 9.75 points
- **MAE**: 18.75 points

### Trade #1903 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-20 20:15:00
- **FVG 5m**: 25342.00 - 25345.00
- **Entrée**: 25339.75 @ 2025-10-20 20:27:00
- **Stop Loss**: 25357.67
- **Risk**: 17.92 points
- **TP 1RR**: 25321.83 ❌
- **TP 2RR**: 25303.90 ❌
- **TP 3RR**: 25285.98 ❌
- **TP 4RR**: 25268.06 ❌
- **TP 15RR**: 25070.91 ❌
- **PnL**: -17.92 points (-1.0R)
- **MFE**: 9.75 points
- **MAE**: 18.75 points

### Trade #1904 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-20 21:30:00
- **FVG 5m**: 25353.00 - 25356.75
- **Entrée**: 25352.50 @ 2025-10-20 21:43:00
- **Stop Loss**: 25369.43
- **Risk**: 16.93 points
- **TP 1RR**: 25335.57 ✅
- **TP 2RR**: 25318.64 ✅
- **TP 3RR**: 25301.71 ✅
- **TP 4RR**: 25284.79 ✅
- **TP 15RR**: 25098.57 ✅
- **PnL**: 253.93 points (15.0R)
- **MFE**: 259.25 points
- **MAE**: 3.25 points

### Trade #1905 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-21 08:30:00
- **FVG 5m**: 25254.00 - 25258.75
- **Entrée**: 25267.25 @ 2025-10-21 09:18:00
- **Stop Loss**: 25241.37
- **Risk**: 25.88 points
- **TP 1RR**: 25293.13 ❌
- **TP 2RR**: 25319.00 ❌
- **TP 3RR**: 25344.88 ❌
- **TP 4RR**: 25370.76 ❌
- **TP 15RR**: 25655.41 ❌
- **PnL**: -25.88 points (-1.0R)
- **MFE**: 18.75 points
- **MAE**: 39.00 points

### Trade #1906 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-21 09:45:00
- **FVG 5m**: 25292.25 - 25307.50
- **Entrée**: 25311.25 @ 2025-10-21 10:47:00
- **Stop Loss**: 25279.60
- **Risk**: 31.65 points
- **TP 1RR**: 25342.90 ✅
- **TP 2RR**: 25374.54 ❌
- **TP 3RR**: 25406.19 ❌
- **TP 4RR**: 25437.83 ❌
- **TP 15RR**: 25785.94 ❌
- **PnL**: -31.65 points (-1.0R)
- **MFE**: 37.25 points
- **MAE**: 33.75 points

### Trade #1907 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-21 20:00:00
- **FVG 5m**: 25245.75 - 25249.75
- **Entrée**: 25252.25 @ 2025-10-21 20:47:00
- **Stop Loss**: 25233.13
- **Risk**: 19.12 points
- **TP 1RR**: 25271.37 ✅
- **TP 2RR**: 25290.50 ✅
- **TP 3RR**: 25309.62 ✅
- **TP 4RR**: 25328.74 ✅
- **TP 15RR**: 25539.09 ❌
- **PnL**: -19.12 points (-1.0R)
- **MFE**: 86.00 points
- **MAE**: 20.75 points

### Trade #1908 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 04:15:00
- **FVG 5m**: 25256.25 - 25259.75
- **Entrée**: 25269.00 @ 2025-10-22 04:55:00
- **Stop Loss**: 25243.62
- **Risk**: 25.38 points
- **TP 1RR**: 25294.38 ✅
- **TP 2RR**: 25319.76 ❌
- **TP 3RR**: 25345.13 ❌
- **TP 4RR**: 25370.51 ❌
- **TP 15RR**: 25649.67 ❌
- **PnL**: -25.38 points (-1.0R)
- **MFE**: 36.50 points
- **MAE**: 32.25 points

### Trade #1909 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 06:00:00
- **FVG 5m**: 25260.00 - 25270.50
- **Entrée**: 25272.00 @ 2025-10-22 08:13:00
- **Stop Loss**: 25247.37
- **Risk**: 24.63 points
- **TP 1RR**: 25296.63 ❌
- **TP 2RR**: 25321.26 ❌
- **TP 3RR**: 25345.89 ❌
- **TP 4RR**: 25370.52 ❌
- **TP 15RR**: 25641.45 ❌
- **PnL**: -24.63 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 58.50 points

### Trade #1910 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 07:00:00
- **FVG 5m**: 25260.00 - 25270.50
- **Entrée**: 25272.00 @ 2025-10-22 08:13:00
- **Stop Loss**: 25247.37
- **Risk**: 24.63 points
- **TP 1RR**: 25296.63 ❌
- **TP 2RR**: 25321.26 ❌
- **TP 3RR**: 25345.89 ❌
- **TP 4RR**: 25370.52 ❌
- **TP 15RR**: 25641.45 ❌
- **PnL**: -24.63 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 58.50 points

### Trade #1911 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 08:30:00
- **FVG 5m**: 25226.50 - 25236.25
- **Entrée**: 25245.25 @ 2025-10-22 08:41:00
- **Stop Loss**: 25213.89
- **Risk**: 31.36 points
- **TP 1RR**: 25276.61 ✅
- **TP 2RR**: 25307.98 ❌
- **TP 3RR**: 25339.34 ❌
- **TP 4RR**: 25370.70 ❌
- **TP 15RR**: 25715.70 ❌
- **PnL**: -31.36 points (-1.0R)
- **MFE**: 44.00 points
- **MAE**: 35.50 points

### Trade #1912 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 08:30:00
- **FVG 5m**: 25226.50 - 25236.25
- **Entrée**: 25245.25 @ 2025-10-22 08:41:00
- **Stop Loss**: 25213.89
- **Risk**: 31.36 points
- **TP 1RR**: 25276.61 ✅
- **TP 2RR**: 25307.98 ❌
- **TP 3RR**: 25339.34 ❌
- **TP 4RR**: 25370.70 ❌
- **TP 15RR**: 25715.70 ❌
- **PnL**: -31.36 points (-1.0R)
- **MFE**: 44.00 points
- **MAE**: 35.50 points

### Trade #1913 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 08:30:00
- **FVG 5m**: 25226.50 - 25236.25
- **Entrée**: 25245.25 @ 2025-10-22 08:41:00
- **Stop Loss**: 25213.89
- **Risk**: 31.36 points
- **TP 1RR**: 25276.61 ✅
- **TP 2RR**: 25307.98 ❌
- **TP 3RR**: 25339.34 ❌
- **TP 4RR**: 25370.70 ❌
- **TP 15RR**: 25715.70 ❌
- **PnL**: -31.36 points (-1.0R)
- **MFE**: 44.00 points
- **MAE**: 35.50 points

### Trade #1914 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 09:15:00
- **FVG 5m**: 25142.25 - 25187.50
- **Entrée**: 25139.25 @ 2025-10-22 09:28:00
- **Stop Loss**: 25200.09
- **Risk**: 60.84 points
- **TP 1RR**: 25078.41 ✅
- **TP 2RR**: 25017.56 ✅
- **TP 3RR**: 24956.72 ✅
- **TP 4RR**: 24895.88 ✅
- **TP 15RR**: 24226.59 ❌
- **PnL**: -60.84 points (-1.0R)
- **MFE**: 334.50 points
- **MAE**: 66.00 points

### Trade #1915 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 09:15:00
- **FVG 5m**: 25142.25 - 25187.50
- **Entrée**: 25139.25 @ 2025-10-22 09:28:00
- **Stop Loss**: 25200.09
- **Risk**: 60.84 points
- **TP 1RR**: 25078.41 ✅
- **TP 2RR**: 25017.56 ✅
- **TP 3RR**: 24956.72 ✅
- **TP 4RR**: 24895.88 ✅
- **TP 15RR**: 24226.59 ❌
- **PnL**: -60.84 points (-1.0R)
- **MFE**: 334.50 points
- **MAE**: 66.00 points

### Trade #1916 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 09:30:00
- **FVG 5m**: 25071.75 - 25115.50
- **Entrée**: 25060.00 @ 2025-10-22 10:22:00
- **Stop Loss**: 25128.06
- **Risk**: 68.06 points
- **TP 1RR**: 24991.94 ❌
- **TP 2RR**: 24923.88 ❌
- **TP 3RR**: 24855.83 ❌
- **TP 4RR**: 24787.77 ❌
- **TP 15RR**: 24039.13 ❌
- **PnL**: -68.06 points (-1.0R)
- **MFE**: 56.75 points
- **MAE**: 71.75 points

### Trade #1917 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 09:45:00
- **FVG 5m**: 25139.00 - 25161.75
- **Entrée**: 25164.50 @ 2025-10-22 09:58:00
- **Stop Loss**: 25126.43
- **Risk**: 38.07 points
- **TP 1RR**: 25202.57 ❌
- **TP 2RR**: 25240.64 ❌
- **TP 3RR**: 25278.71 ❌
- **TP 4RR**: 25316.78 ❌
- **TP 15RR**: 25735.54 ❌
- **PnL**: -38.07 points (-1.0R)
- **MFE**: 27.75 points
- **MAE**: 43.75 points

### Trade #1918 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 10:30:00
- **FVG 5m**: 25043.75 - 25060.25
- **Entrée**: 25063.75 @ 2025-10-22 10:42:00
- **Stop Loss**: 25031.23
- **Risk**: 32.52 points
- **TP 1RR**: 25096.27 ✅
- **TP 2RR**: 25128.79 ✅
- **TP 3RR**: 25161.32 ❌
- **TP 4RR**: 25193.84 ❌
- **TP 15RR**: 25551.58 ❌
- **PnL**: -32.52 points (-1.0R)
- **MFE**: 68.00 points
- **MAE**: 35.50 points

### Trade #1919 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 10:30:00
- **FVG 5m**: 25043.75 - 25060.25
- **Entrée**: 25063.75 @ 2025-10-22 10:42:00
- **Stop Loss**: 25031.23
- **Risk**: 32.52 points
- **TP 1RR**: 25096.27 ✅
- **TP 2RR**: 25128.79 ✅
- **TP 3RR**: 25161.32 ❌
- **TP 4RR**: 25193.84 ❌
- **TP 15RR**: 25551.58 ❌
- **PnL**: -32.52 points (-1.0R)
- **MFE**: 68.00 points
- **MAE**: 35.50 points

### Trade #1920 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 11:30:00
- **FVG 5m**: 24874.25 - 24878.50
- **Entrée**: 24879.75 @ 2025-10-22 13:03:00
- **Stop Loss**: 24861.81
- **Risk**: 17.94 points
- **TP 1RR**: 24897.69 ✅
- **TP 2RR**: 24915.62 ❌
- **TP 3RR**: 24933.56 ❌
- **TP 4RR**: 24951.50 ❌
- **TP 15RR**: 25148.81 ❌
- **PnL**: -17.94 points (-1.0R)
- **MFE**: 28.75 points
- **MAE**: 26.00 points

### Trade #1921 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 12:00:00
- **FVG 5m**: 24942.00 - 24947.25
- **Entrée**: 24933.50 @ 2025-10-22 12:14:00
- **Stop Loss**: 24959.72
- **Risk**: 26.22 points
- **TP 1RR**: 24907.28 ✅
- **TP 2RR**: 24881.05 ✅
- **TP 3RR**: 24854.83 ✅
- **TP 4RR**: 24828.61 ✅
- **TP 15RR**: 24540.15 ❌
- **PnL**: -26.22 points (-1.0R)
- **MFE**: 128.75 points
- **MAE**: 26.50 points

### Trade #1922 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 12:45:00
- **FVG 5m**: 24874.25 - 24878.50
- **Entrée**: 24879.75 @ 2025-10-22 13:03:00
- **Stop Loss**: 24861.81
- **Risk**: 17.94 points
- **TP 1RR**: 24897.69 ✅
- **TP 2RR**: 24915.62 ❌
- **TP 3RR**: 24933.56 ❌
- **TP 4RR**: 24951.50 ❌
- **TP 15RR**: 25148.81 ❌
- **PnL**: -17.94 points (-1.0R)
- **MFE**: 28.75 points
- **MAE**: 26.00 points

### Trade #1923 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 19:00:00
- **FVG 5m**: 24995.50 - 25002.50
- **Entrée**: 25003.25 @ 2025-10-22 19:12:00
- **Stop Loss**: 24983.00
- **Risk**: 20.25 points
- **TP 1RR**: 25023.50 ✅
- **TP 2RR**: 25043.75 ✅
- **TP 3RR**: 25063.99 ✅
- **TP 4RR**: 25084.24 ✅
- **TP 15RR**: 25306.97 ❌
- **PnL**: -20.25 points (-1.0R)
- **MFE**: 124.75 points
- **MAE**: 27.00 points

### Trade #1924 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 23:00:00
- **FVG 5m**: 25074.50 - 25078.25
- **Entrée**: 25072.50 @ 2025-10-22 23:14:00
- **Stop Loss**: 25090.79
- **Risk**: 18.29 points
- **TP 1RR**: 25054.21 ✅
- **TP 2RR**: 25035.92 ❌
- **TP 3RR**: 25017.63 ❌
- **TP 4RR**: 24999.34 ❌
- **TP 15RR**: 24798.16 ❌
- **PnL**: -18.29 points (-1.0R)
- **MFE**: 19.00 points
- **MAE**: 19.75 points

### Trade #1925 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-23 07:30:00
- **FVG 5m**: 24949.75 - 24960.50
- **Entrée**: 24961.50 @ 2025-10-23 07:43:00
- **Stop Loss**: 24937.28
- **Risk**: 24.22 points
- **TP 1RR**: 24985.72 ✅
- **TP 2RR**: 25009.95 ✅
- **TP 3RR**: 25034.17 ✅
- **TP 4RR**: 25058.40 ✅
- **TP 15RR**: 25324.87 ✅
- **PnL**: 363.37 points (15.0R)
- **MFE**: 364.75 points
- **MAE**: 20.75 points

### Trade #1926 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-23 08:30:00
- **FVG 5m**: 25077.50 - 25091.25
- **Entrée**: 25092.25 @ 2025-10-23 08:44:00
- **Stop Loss**: 25064.96
- **Risk**: 27.29 points
- **TP 1RR**: 25119.54 ✅
- **TP 2RR**: 25146.83 ✅
- **TP 3RR**: 25174.12 ✅
- **TP 4RR**: 25201.40 ✅
- **TP 15RR**: 25501.58 ✅
- **PnL**: 409.33 points (15.0R)
- **MFE**: 427.75 points
- **MAE**: 8.25 points

### Trade #1927 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-23 20:15:00
- **FVG 5m**: 25305.00 - 25315.00
- **Entrée**: 25303.75 @ 2025-10-23 20:29:00
- **Stop Loss**: 25327.66
- **Risk**: 23.91 points
- **TP 1RR**: 25279.84 ❌
- **TP 2RR**: 25255.93 ❌
- **TP 3RR**: 25232.03 ❌
- **TP 4RR**: 25208.12 ❌
- **TP 15RR**: 24945.14 ❌
- **PnL**: -23.91 points (-1.0R)
- **MFE**: 6.75 points
- **MAE**: 24.25 points

### Trade #1928 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-24 02:45:00
- **FVG 5m**: 25381.75 - 25388.00
- **Entrée**: 25380.75 @ 2025-10-24 04:47:00
- **Stop Loss**: 25400.69
- **Risk**: 19.94 points
- **TP 1RR**: 25360.81 ❌
- **TP 2RR**: 25340.86 ❌
- **TP 3RR**: 25320.92 ❌
- **TP 4RR**: 25300.97 ❌
- **TP 15RR**: 25081.59 ❌
- **PnL**: -19.94 points (-1.0R)
- **MFE**: 36.75 points
- **MAE**: 139.25 points

### Trade #1929 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-24 11:15:00
- **FVG 5m**: 25550.00 - 25554.00
- **Entrée**: 25549.25 @ 2025-10-24 12:59:00
- **Stop Loss**: 25566.78
- **Risk**: 17.53 points
- **TP 1RR**: 25531.72 ✅
- **TP 2RR**: 25514.20 ✅
- **TP 3RR**: 25496.67 ❌
- **TP 4RR**: 25479.14 ❌
- **TP 15RR**: 25286.35 ❌
- **PnL**: -17.53 points (-1.0R)
- **MFE**: 51.75 points
- **MAE**: 219.00 points

### Trade #1930 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-27 08:15:00
- **FVG 5m**: 25844.50 - 25848.75
- **Entrée**: 25840.50 @ 2025-10-27 09:17:00
- **Stop Loss**: 25861.67
- **Risk**: 21.17 points
- **TP 1RR**: 25819.33 ❌
- **TP 2RR**: 25798.15 ❌
- **TP 3RR**: 25776.98 ❌
- **TP 4RR**: 25755.80 ❌
- **TP 15RR**: 25522.88 ❌
- **PnL**: -21.17 points (-1.0R)
- **MFE**: 17.50 points
- **MAE**: 22.75 points

### Trade #1931 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-27 08:30:00
- **FVG 5m**: 25854.50 - 25862.25
- **Entrée**: 25871.00 @ 2025-10-27 09:03:00
- **Stop Loss**: 25841.57
- **Risk**: 29.43 points
- **TP 1RR**: 25900.43 ❌
- **TP 2RR**: 25929.85 ❌
- **TP 3RR**: 25959.28 ❌
- **TP 4RR**: 25988.71 ❌
- **TP 15RR**: 26312.41 ❌
- **PnL**: -29.43 points (-1.0R)
- **MFE**: 4.75 points
- **MAE**: 33.25 points

### Trade #1932 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 09:00:00
- **FVG 5m**: 26289.50 - 26298.75
- **Entrée**: 26287.75 @ 2025-10-29 09:42:00
- **Stop Loss**: 26311.90
- **Risk**: 24.15 points
- **TP 1RR**: 26263.60 ✅
- **TP 2RR**: 26239.45 ✅
- **TP 3RR**: 26215.30 ✅
- **TP 4RR**: 26191.15 ✅
- **TP 15RR**: 25925.51 ❌
- **PnL**: -24.15 points (-1.0R)
- **MFE**: 238.50 points
- **MAE**: 62.25 points

### Trade #1933 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 09:00:00
- **FVG 5m**: 26289.50 - 26298.75
- **Entrée**: 26287.75 @ 2025-10-29 09:42:00
- **Stop Loss**: 26311.90
- **Risk**: 24.15 points
- **TP 1RR**: 26263.60 ✅
- **TP 2RR**: 26239.45 ✅
- **TP 3RR**: 26215.30 ✅
- **TP 4RR**: 26191.15 ✅
- **TP 15RR**: 25925.51 ❌
- **PnL**: -24.15 points (-1.0R)
- **MFE**: 238.50 points
- **MAE**: 62.25 points

### Trade #1934 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 11:00:00
- **FVG 5m**: 26232.25 - 26242.75
- **Entrée**: 26244.00 @ 2025-10-29 11:23:00
- **Stop Loss**: 26219.13
- **Risk**: 24.87 points
- **TP 1RR**: 26268.87 ❌
- **TP 2RR**: 26293.73 ❌
- **TP 3RR**: 26318.60 ❌
- **TP 4RR**: 26343.46 ❌
- **TP 15RR**: 26616.99 ❌
- **PnL**: -24.87 points (-1.0R)
- **MFE**: 24.25 points
- **MAE**: 25.00 points

### Trade #1935 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 11:15:00
- **FVG 5m**: 26234.50 - 26239.00
- **Entrée**: 26240.50 @ 2025-10-29 12:39:00
- **Stop Loss**: 26221.38
- **Risk**: 19.12 points
- **TP 1RR**: 26259.62 ✅
- **TP 2RR**: 26278.73 ✅
- **TP 3RR**: 26297.85 ❌
- **TP 4RR**: 26316.97 ❌
- **TP 15RR**: 26527.26 ❌
- **PnL**: -19.12 points (-1.0R)
- **MFE**: 49.50 points
- **MAE**: 21.25 points

### Trade #1936 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 12:15:00
- **FVG 5m**: 26234.50 - 26238.25
- **Entrée**: 26227.50 @ 2025-10-29 12:30:00
- **Stop Loss**: 26251.37
- **Risk**: 23.87 points
- **TP 1RR**: 26203.63 ❌
- **TP 2RR**: 26179.76 ❌
- **TP 3RR**: 26155.89 ❌
- **TP 4RR**: 26132.02 ❌
- **TP 15RR**: 25869.46 ❌
- **PnL**: -23.87 points (-1.0R)
- **MFE**: 4.50 points
- **MAE**: 26.75 points

### Trade #1937 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 13:15:00
- **FVG 5m**: 26141.00 - 26164.75
- **Entrée**: 26181.25 @ 2025-10-29 13:51:00
- **Stop Loss**: 26127.93
- **Risk**: 53.32 points
- **TP 1RR**: 26234.57 ❌
- **TP 2RR**: 26287.89 ❌
- **TP 3RR**: 26341.21 ❌
- **TP 4RR**: 26394.53 ❌
- **TP 15RR**: 26981.06 ❌
- **PnL**: -53.32 points (-1.0R)
- **MFE**: 46.75 points
- **MAE**: 69.50 points

### Trade #1938 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 13:30:00
- **FVG 5m**: 26234.50 - 26248.50
- **Entrée**: 26213.00 @ 2025-10-29 15:06:00
- **Stop Loss**: 26261.62
- **Risk**: 48.62 points
- **TP 1RR**: 26164.38 ✅
- **TP 2RR**: 26115.75 ❌
- **TP 3RR**: 26067.13 ❌
- **TP 4RR**: 26018.50 ❌
- **TP 15RR**: 25483.64 ❌
- **PnL**: -48.62 points (-1.0R)
- **MFE**: 53.25 points
- **MAE**: 53.25 points

### Trade #1939 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 13:30:00
- **FVG 5m**: 26234.50 - 26248.50
- **Entrée**: 26213.00 @ 2025-10-29 15:06:00
- **Stop Loss**: 26261.62
- **Risk**: 48.62 points
- **TP 1RR**: 26164.38 ✅
- **TP 2RR**: 26115.75 ❌
- **TP 3RR**: 26067.13 ❌
- **TP 4RR**: 26018.50 ❌
- **TP 15RR**: 25483.64 ❌
- **PnL**: -48.62 points (-1.0R)
- **MFE**: 53.25 points
- **MAE**: 53.25 points

### Trade #1940 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 13:45:00
- **FVG 5m**: 26219.50 - 26224.50
- **Entrée**: 26232.00 @ 2025-10-29 14:48:00
- **Stop Loss**: 26206.39
- **Risk**: 25.61 points
- **TP 1RR**: 26257.61 ✅
- **TP 2RR**: 26283.22 ✅
- **TP 3RR**: 26308.83 ✅
- **TP 4RR**: 26334.44 ✅
- **TP 15RR**: 26616.15 ❌
- **PnL**: -25.61 points (-1.0R)
- **MFE**: 147.75 points
- **MAE**: 62.00 points

### Trade #1941 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 15:00:00
- **FVG 5m**: 26212.50 - 26229.25
- **Entrée**: 26193.50 @ 2025-10-29 17:00:00
- **Stop Loss**: 26242.36
- **Risk**: 48.86 points
- **TP 1RR**: 26144.64 ❌
- **TP 2RR**: 26095.77 ❌
- **TP 3RR**: 26046.91 ❌
- **TP 4RR**: 25998.04 ❌
- **TP 15RR**: 25460.53 ❌
- **PnL**: -48.86 points (-1.0R)
- **MFE**: 39.25 points
- **MAE**: 62.25 points

### Trade #1942 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 15:00:00
- **FVG 5m**: 26212.50 - 26229.25
- **Entrée**: 26193.50 @ 2025-10-29 17:00:00
- **Stop Loss**: 26242.36
- **Risk**: 48.86 points
- **TP 1RR**: 26144.64 ❌
- **TP 2RR**: 26095.77 ❌
- **TP 3RR**: 26046.91 ❌
- **TP 4RR**: 25998.04 ❌
- **TP 15RR**: 25460.53 ❌
- **PnL**: -48.86 points (-1.0R)
- **MFE**: 39.25 points
- **MAE**: 62.25 points

### Trade #1943 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 15:00:00
- **FVG 5m**: 26199.25 - 26222.75
- **Entrée**: 26230.75 @ 2025-10-29 18:22:00
- **Stop Loss**: 26186.15
- **Risk**: 44.60 points
- **TP 1RR**: 26275.35 ❌
- **TP 2RR**: 26319.95 ❌
- **TP 3RR**: 26364.55 ❌
- **TP 4RR**: 26409.15 ❌
- **TP 15RR**: 26899.74 ❌
- **PnL**: -44.60 points (-1.0R)
- **MFE**: 5.00 points
- **MAE**: 68.00 points

### Trade #1944 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 22:15:00
- **FVG 5m**: 26355.00 - 26367.75
- **Entrée**: 26345.25 @ 2025-10-29 23:05:00
- **Stop Loss**: 26380.93
- **Risk**: 35.68 points
- **TP 1RR**: 26309.57 ✅
- **TP 2RR**: 26273.88 ✅
- **TP 3RR**: 26238.20 ✅
- **TP 4RR**: 26202.51 ✅
- **TP 15RR**: 25809.99 ✅
- **PnL**: 535.26 points (15.0R)
- **MFE**: 538.25 points
- **MAE**: 5.50 points

### Trade #1945 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 23:00:00
- **FVG 5m**: 26245.00 - 26303.00
- **Entrée**: 26217.25 @ 2025-10-29 23:13:00
- **Stop Loss**: 26316.15
- **Risk**: 98.90 points
- **TP 1RR**: 26118.35 ❌
- **TP 2RR**: 26019.45 ❌
- **TP 3RR**: 25920.55 ❌
- **TP 4RR**: 25821.64 ❌
- **TP 15RR**: 24733.73 ❌
- **PnL**: -98.90 points (-1.0R)
- **MFE**: 77.25 points
- **MAE**: 102.25 points

### Trade #1946 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26025.75 - 26040.00
- **Entrée**: 26014.75 @ 2025-10-30 09:51:00
- **Stop Loss**: 26053.02
- **Risk**: 38.27 points
- **TP 1RR**: 25976.48 ❌
- **TP 2RR**: 25938.21 ❌
- **TP 3RR**: 25899.94 ❌
- **TP 4RR**: 25861.67 ❌
- **TP 15RR**: 25440.70 ❌
- **PnL**: -38.27 points (-1.0R)
- **MFE**: 35.75 points
- **MAE**: 42.00 points

### Trade #1947 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26025.75 - 26040.00
- **Entrée**: 26014.75 @ 2025-10-30 09:51:00
- **Stop Loss**: 26053.02
- **Risk**: 38.27 points
- **TP 1RR**: 25976.48 ❌
- **TP 2RR**: 25938.21 ❌
- **TP 3RR**: 25899.94 ❌
- **TP 4RR**: 25861.67 ❌
- **TP 15RR**: 25440.70 ❌
- **PnL**: -38.27 points (-1.0R)
- **MFE**: 35.75 points
- **MAE**: 42.00 points

### Trade #1948 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26025.75 - 26040.00
- **Entrée**: 26014.75 @ 2025-10-30 09:51:00
- **Stop Loss**: 26053.02
- **Risk**: 38.27 points
- **TP 1RR**: 25976.48 ❌
- **TP 2RR**: 25938.21 ❌
- **TP 3RR**: 25899.94 ❌
- **TP 4RR**: 25861.67 ❌
- **TP 15RR**: 25440.70 ❌
- **PnL**: -38.27 points (-1.0R)
- **MFE**: 35.75 points
- **MAE**: 42.00 points

### Trade #1949 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26025.75 - 26040.00
- **Entrée**: 26014.75 @ 2025-10-30 09:51:00
- **Stop Loss**: 26053.02
- **Risk**: 38.27 points
- **TP 1RR**: 25976.48 ❌
- **TP 2RR**: 25938.21 ❌
- **TP 3RR**: 25899.94 ❌
- **TP 4RR**: 25861.67 ❌
- **TP 15RR**: 25440.70 ❌
- **PnL**: -38.27 points (-1.0R)
- **MFE**: 35.75 points
- **MAE**: 42.00 points

### Trade #1950 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:30:00
- **FVG 5m**: 25996.00 - 26053.50
- **Entrée**: 26056.00 @ 2025-10-30 08:48:00
- **Stop Loss**: 25983.00
- **Risk**: 73.00 points
- **TP 1RR**: 26129.00 ✅
- **TP 2RR**: 26202.00 ❌
- **TP 3RR**: 26274.99 ❌
- **TP 4RR**: 26347.99 ❌
- **TP 15RR**: 27150.97 ❌
- **PnL**: -73.00 points (-1.0R)
- **MFE**: 126.50 points
- **MAE**: 77.00 points

### Trade #1951 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:30:00
- **FVG 5m**: 25996.00 - 26053.50
- **Entrée**: 26056.00 @ 2025-10-30 08:48:00
- **Stop Loss**: 25983.00
- **Risk**: 73.00 points
- **TP 1RR**: 26129.00 ✅
- **TP 2RR**: 26202.00 ❌
- **TP 3RR**: 26274.99 ❌
- **TP 4RR**: 26347.99 ❌
- **TP 15RR**: 27150.97 ❌
- **PnL**: -73.00 points (-1.0R)
- **MFE**: 126.50 points
- **MAE**: 77.00 points

### Trade #1952 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:45:00
- **FVG 5m**: 26013.75 - 26023.00
- **Entrée**: 26031.50 @ 2025-10-30 11:04:00
- **Stop Loss**: 26000.74
- **Risk**: 30.76 points
- **TP 1RR**: 26062.26 ✅
- **TP 2RR**: 26093.01 ✅
- **TP 3RR**: 26123.77 ❌
- **TP 4RR**: 26154.53 ❌
- **TP 15RR**: 26492.85 ❌
- **PnL**: -30.76 points (-1.0R)
- **MFE**: 65.50 points
- **MAE**: 32.50 points

### Trade #1953 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:45:00
- **FVG 5m**: 26013.75 - 26023.00
- **Entrée**: 26031.50 @ 2025-10-30 11:04:00
- **Stop Loss**: 26000.74
- **Risk**: 30.76 points
- **TP 1RR**: 26062.26 ✅
- **TP 2RR**: 26093.01 ✅
- **TP 3RR**: 26123.77 ❌
- **TP 4RR**: 26154.53 ❌
- **TP 15RR**: 26492.85 ❌
- **PnL**: -30.76 points (-1.0R)
- **MFE**: 65.50 points
- **MAE**: 32.50 points

### Trade #1954 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:00:00
- **FVG 5m**: 26006.00 - 26011.25
- **Entrée**: 26016.25 @ 2025-10-30 15:16:00
- **Stop Loss**: 25993.00
- **Risk**: 23.25 points
- **TP 1RR**: 26039.50 ❌
- **TP 2RR**: 26062.76 ❌
- **TP 3RR**: 26086.01 ❌
- **TP 4RR**: 26109.26 ❌
- **TP 15RR**: 26365.05 ❌
- **PnL**: -23.25 points (-1.0R)
- **MFE**: 23.75 points
- **MAE**: 96.25 points

### Trade #1955 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:00:00
- **FVG 5m**: 26006.00 - 26011.25
- **Entrée**: 26016.25 @ 2025-10-30 15:16:00
- **Stop Loss**: 25993.00
- **Risk**: 23.25 points
- **TP 1RR**: 26039.50 ❌
- **TP 2RR**: 26062.76 ❌
- **TP 3RR**: 26086.01 ❌
- **TP 4RR**: 26109.26 ❌
- **TP 15RR**: 26365.05 ❌
- **PnL**: -23.25 points (-1.0R)
- **MFE**: 23.75 points
- **MAE**: 96.25 points

### Trade #1956 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:00:00
- **FVG 5m**: 26006.00 - 26011.25
- **Entrée**: 26016.25 @ 2025-10-30 15:16:00
- **Stop Loss**: 25993.00
- **Risk**: 23.25 points
- **TP 1RR**: 26039.50 ❌
- **TP 2RR**: 26062.76 ❌
- **TP 3RR**: 26086.01 ❌
- **TP 4RR**: 26109.26 ❌
- **TP 15RR**: 26365.05 ❌
- **PnL**: -23.25 points (-1.0R)
- **MFE**: 23.75 points
- **MAE**: 96.25 points

### Trade #1957 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:45:00
- **FVG 5m**: 26148.75 - 26151.50
- **Entrée**: 26154.50 @ 2025-10-30 18:42:00
- **Stop Loss**: 26135.68
- **Risk**: 18.82 points
- **TP 1RR**: 26173.32 ✅
- **TP 2RR**: 26192.15 ✅
- **TP 3RR**: 26210.97 ✅
- **TP 4RR**: 26229.80 ✅
- **TP 15RR**: 26436.87 ❌
- **PnL**: -18.82 points (-1.0R)
- **MFE**: 119.50 points
- **MAE**: 21.25 points

### Trade #1958 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 18:30:00
- **FVG 5m**: 26148.75 - 26151.50
- **Entrée**: 26154.50 @ 2025-10-30 18:42:00
- **Stop Loss**: 26135.68
- **Risk**: 18.82 points
- **TP 1RR**: 26173.32 ✅
- **TP 2RR**: 26192.15 ✅
- **TP 3RR**: 26210.97 ✅
- **TP 4RR**: 26229.80 ✅
- **TP 15RR**: 26436.87 ❌
- **PnL**: -18.82 points (-1.0R)
- **MFE**: 119.50 points
- **MAE**: 21.25 points

### Trade #1959 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 19:15:00
- **FVG 5m**: 26180.25 - 26185.25
- **Entrée**: 26186.25 @ 2025-10-30 19:27:00
- **Stop Loss**: 26167.16
- **Risk**: 19.09 points
- **TP 1RR**: 26205.34 ✅
- **TP 2RR**: 26224.43 ❌
- **TP 3RR**: 26243.52 ❌
- **TP 4RR**: 26262.61 ❌
- **TP 15RR**: 26472.60 ❌
- **PnL**: -19.09 points (-1.0R)
- **MFE**: 27.25 points
- **MAE**: 21.50 points

### Trade #1960 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 02:30:00
- **FVG 5m**: 26198.50 - 26201.75
- **Entrée**: 26205.50 @ 2025-10-31 02:42:00
- **Stop Loss**: 26185.40
- **Risk**: 20.10 points
- **TP 1RR**: 26225.60 ❌
- **TP 2RR**: 26245.70 ❌
- **TP 3RR**: 26265.80 ❌
- **TP 4RR**: 26285.90 ❌
- **TP 15RR**: 26506.99 ❌
- **PnL**: -20.10 points (-1.0R)
- **MFE**: 14.25 points
- **MAE**: 29.00 points

### Trade #1961 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 03:00:00
- **FVG 5m**: 26174.00 - 26187.25
- **Entrée**: 26160.50 @ 2025-10-31 03:14:00
- **Stop Loss**: 26200.34
- **Risk**: 39.84 points
- **TP 1RR**: 26120.66 ❌
- **TP 2RR**: 26080.81 ❌
- **TP 3RR**: 26040.97 ❌
- **TP 4RR**: 26001.13 ❌
- **TP 15RR**: 25562.85 ❌
- **PnL**: -39.84 points (-1.0R)
- **MFE**: 3.00 points
- **MAE**: 40.25 points

### Trade #1962 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 03:00:00
- **FVG 5m**: 26174.00 - 26187.25
- **Entrée**: 26160.50 @ 2025-10-31 03:14:00
- **Stop Loss**: 26200.34
- **Risk**: 39.84 points
- **TP 1RR**: 26120.66 ❌
- **TP 2RR**: 26080.81 ❌
- **TP 3RR**: 26040.97 ❌
- **TP 4RR**: 26001.13 ❌
- **TP 15RR**: 25562.85 ❌
- **PnL**: -39.84 points (-1.0R)
- **MFE**: 3.00 points
- **MAE**: 40.25 points

### Trade #1963 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 07:45:00
- **FVG 5m**: 26173.75 - 26191.50
- **Entrée**: 26158.75 @ 2025-10-31 08:31:00
- **Stop Loss**: 26204.60
- **Risk**: 45.85 points
- **TP 1RR**: 26112.90 ✅
- **TP 2RR**: 26067.06 ✅
- **TP 3RR**: 26021.21 ✅
- **TP 4RR**: 25975.37 ✅
- **TP 15RR**: 25471.06 ❌
- **PnL**: -45.85 points (-1.0R)
- **MFE**: 270.00 points
- **MAE**: 101.00 points

### Trade #1964 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 09:00:00
- **FVG 5m**: 26158.00 - 26168.75
- **Entrée**: 26157.25 @ 2025-10-31 10:22:00
- **Stop Loss**: 26181.83
- **Risk**: 24.58 points
- **TP 1RR**: 26132.67 ✅
- **TP 2RR**: 26108.08 ✅
- **TP 3RR**: 26083.50 ✅
- **TP 4RR**: 26058.91 ✅
- **TP 15RR**: 25788.48 ❌
- **PnL**: -24.58 points (-1.0R)
- **MFE**: 268.50 points
- **MAE**: 24.75 points

### Trade #1965 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26137.67
- **Risk**: 21.58 points
- **TP 1RR**: 26180.83 ✅
- **TP 2RR**: 26202.40 ❌
- **TP 3RR**: 26223.98 ❌
- **TP 4RR**: 26245.55 ❌
- **TP 15RR**: 26482.88 ❌
- **PnL**: -21.58 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 25.00 points

### Trade #1966 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26137.67
- **Risk**: 21.58 points
- **TP 1RR**: 26180.83 ✅
- **TP 2RR**: 26202.40 ❌
- **TP 3RR**: 26223.98 ❌
- **TP 4RR**: 26245.55 ❌
- **TP 15RR**: 26482.88 ❌
- **PnL**: -21.58 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 25.00 points

### Trade #1967 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26137.67
- **Risk**: 21.58 points
- **TP 1RR**: 26180.83 ✅
- **TP 2RR**: 26202.40 ❌
- **TP 3RR**: 26223.98 ❌
- **TP 4RR**: 26245.55 ❌
- **TP 15RR**: 26482.88 ❌
- **PnL**: -21.58 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 25.00 points

### Trade #1968 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26137.67
- **Risk**: 21.58 points
- **TP 1RR**: 26180.83 ✅
- **TP 2RR**: 26202.40 ❌
- **TP 3RR**: 26223.98 ❌
- **TP 4RR**: 26245.55 ❌
- **TP 15RR**: 26482.88 ❌
- **PnL**: -21.58 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 25.00 points

### Trade #1969 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26137.67
- **Risk**: 21.58 points
- **TP 1RR**: 26180.83 ✅
- **TP 2RR**: 26202.40 ❌
- **TP 3RR**: 26223.98 ❌
- **TP 4RR**: 26245.55 ❌
- **TP 15RR**: 26482.88 ❌
- **PnL**: -21.58 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 25.00 points

### Trade #1970 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 14:15:00
- **FVG 5m**: 25988.50 - 26012.75
- **Entrée**: 26031.25 @ 2025-11-02 17:00:00
- **Stop Loss**: 25975.51
- **Risk**: 55.74 points
- **TP 1RR**: 26086.99 ✅
- **TP 2RR**: 26142.74 ✅
- **TP 3RR**: 26198.48 ✅
- **TP 4RR**: 26254.23 ✅
- **TP 15RR**: 26867.41 ❌
- **PnL**: -55.74 points (-1.0R)
- **MFE**: 234.75 points
- **MAE**: 56.00 points

### Trade #1971 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-03 02:00:00
- **FVG 5m**: 26057.25 - 26063.00
- **Entrée**: 26064.50 @ 2025-11-03 02:26:00
- **Stop Loss**: 26044.22
- **Risk**: 20.28 points
- **TP 1RR**: 26084.78 ✅
- **TP 2RR**: 26105.06 ✅
- **TP 3RR**: 26125.34 ✅
- **TP 4RR**: 26145.61 ✅
- **TP 15RR**: 26368.68 ❌
- **PnL**: -20.28 points (-1.0R)
- **MFE**: 201.50 points
- **MAE**: 23.75 points

### Trade #1972 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:00:00
- **FVG 5m**: 26188.00 - 26226.00
- **Entrée**: 26182.25 @ 2025-11-03 08:38:00
- **Stop Loss**: 26239.11
- **Risk**: 56.86 points
- **TP 1RR**: 26125.39 ✅
- **TP 2RR**: 26068.52 ✅
- **TP 3RR**: 26011.66 ✅
- **TP 4RR**: 25954.80 ✅
- **TP 15RR**: 25329.30 ✅
- **PnL**: 852.95 points (15.0R)
- **MFE**: 854.25 points
- **MAE**: 8.00 points

### Trade #1973 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:30:00
- **FVG 5m**: 26146.25 - 26153.25
- **Entrée**: 26145.00 @ 2025-11-03 08:53:00
- **Stop Loss**: 26166.33
- **Risk**: 21.33 points
- **TP 1RR**: 26123.67 ✅
- **TP 2RR**: 26102.35 ✅
- **TP 3RR**: 26081.02 ✅
- **TP 4RR**: 26059.69 ✅
- **TP 15RR**: 25825.10 ❌
- **PnL**: -21.33 points (-1.0R)
- **MFE**: 129.50 points
- **MAE**: 35.00 points

### Trade #1974 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:30:00
- **FVG 5m**: 26146.25 - 26153.25
- **Entrée**: 26145.00 @ 2025-11-03 08:53:00
- **Stop Loss**: 26166.33
- **Risk**: 21.33 points
- **TP 1RR**: 26123.67 ✅
- **TP 2RR**: 26102.35 ✅
- **TP 3RR**: 26081.02 ✅
- **TP 4RR**: 26059.69 ✅
- **TP 15RR**: 25825.10 ❌
- **PnL**: -21.33 points (-1.0R)
- **MFE**: 129.50 points
- **MAE**: 35.00 points

### Trade #1975 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:30:00
- **FVG 5m**: 26146.25 - 26153.25
- **Entrée**: 26145.00 @ 2025-11-03 08:53:00
- **Stop Loss**: 26166.33
- **Risk**: 21.33 points
- **TP 1RR**: 26123.67 ✅
- **TP 2RR**: 26102.35 ✅
- **TP 3RR**: 26081.02 ✅
- **TP 4RR**: 26059.69 ✅
- **TP 15RR**: 25825.10 ❌
- **PnL**: -21.33 points (-1.0R)
- **MFE**: 129.50 points
- **MAE**: 35.00 points

### Trade #1976 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-03 08:45:00
- **FVG 5m**: 26044.00 - 26070.25
- **Entrée**: 26074.75 @ 2025-11-03 09:39:00
- **Stop Loss**: 26030.98
- **Risk**: 43.77 points
- **TP 1RR**: 26118.52 ✅
- **TP 2RR**: 26162.29 ✅
- **TP 3RR**: 26206.07 ❌
- **TP 4RR**: 26249.84 ❌
- **TP 15RR**: 26731.33 ❌
- **PnL**: -43.77 points (-1.0R)
- **MFE**: 105.25 points
- **MAE**: 49.50 points

### Trade #1977 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 09:15:00
- **FVG 5m**: 26044.00 - 26081.00
- **Entrée**: 26043.75 @ 2025-11-03 09:26:00
- **Stop Loss**: 26094.04
- **Risk**: 50.29 points
- **TP 1RR**: 25993.46 ❌
- **TP 2RR**: 25943.17 ❌
- **TP 3RR**: 25892.88 ❌
- **TP 4RR**: 25842.59 ❌
- **TP 15RR**: 25289.39 ❌
- **PnL**: -50.29 points (-1.0R)
- **MFE**: 28.25 points
- **MAE**: 59.25 points

### Trade #1978 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 11:15:00
- **FVG 5m**: 26149.75 - 26152.50
- **Entrée**: 26144.75 @ 2025-11-03 12:47:00
- **Stop Loss**: 26165.58
- **Risk**: 20.83 points
- **TP 1RR**: 26123.92 ✅
- **TP 2RR**: 26103.10 ✅
- **TP 3RR**: 26082.27 ✅
- **TP 4RR**: 26061.45 ❌
- **TP 15RR**: 25832.36 ❌
- **PnL**: -20.83 points (-1.0R)
- **MFE**: 78.50 points
- **MAE**: 35.25 points

### Trade #1979 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 11:15:00
- **FVG 5m**: 26149.75 - 26152.50
- **Entrée**: 26144.75 @ 2025-11-03 12:47:00
- **Stop Loss**: 26165.58
- **Risk**: 20.83 points
- **TP 1RR**: 26123.92 ✅
- **TP 2RR**: 26103.10 ✅
- **TP 3RR**: 26082.27 ✅
- **TP 4RR**: 26061.45 ❌
- **TP 15RR**: 25832.36 ❌
- **PnL**: -20.83 points (-1.0R)
- **MFE**: 78.50 points
- **MAE**: 35.25 points

### Trade #1980 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 15:00:00
- **FVG 5m**: 26127.50 - 26131.00
- **Entrée**: 26123.75 @ 2025-11-03 15:12:00
- **Stop Loss**: 26144.07
- **Risk**: 20.32 points
- **TP 1RR**: 26103.43 ✅
- **TP 2RR**: 26083.12 ✅
- **TP 3RR**: 26062.80 ✅
- **TP 4RR**: 26042.49 ✅
- **TP 15RR**: 25819.02 ✅
- **PnL**: 304.73 points (15.0R)
- **MFE**: 313.50 points
- **MAE**: 7.25 points

### Trade #1981 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 23:30:00
- **FVG 5m**: 25849.75 - 25873.75
- **Entrée**: 25845.25 @ 2025-11-03 23:45:00
- **Stop Loss**: 25886.69
- **Risk**: 41.44 points
- **TP 1RR**: 25803.81 ✅
- **TP 2RR**: 25762.38 ✅
- **TP 3RR**: 25720.94 ✅
- **TP 4RR**: 25679.50 ✅
- **TP 15RR**: 25223.70 ❌
- **PnL**: -41.44 points (-1.0R)
- **MFE**: 200.25 points
- **MAE**: 48.25 points

### Trade #1982 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 00:00:00
- **FVG 5m**: 25775.00 - 25780.00
- **Entrée**: 25788.25 @ 2025-11-04 00:47:00
- **Stop Loss**: 25762.11
- **Risk**: 26.14 points
- **TP 1RR**: 25814.39 ❌
- **TP 2RR**: 25840.53 ❌
- **TP 3RR**: 25866.66 ❌
- **TP 4RR**: 25892.80 ❌
- **TP 15RR**: 26180.31 ❌
- **PnL**: -26.14 points (-1.0R)
- **MFE**: 11.25 points
- **MAE**: 28.50 points

### Trade #1983 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 00:15:00
- **FVG 5m**: 25766.75 - 25774.00
- **Entrée**: 25762.50 @ 2025-11-04 01:02:00
- **Stop Loss**: 25786.89
- **Risk**: 24.39 points
- **TP 1RR**: 25738.11 ✅
- **TP 2RR**: 25713.73 ❌
- **TP 3RR**: 25689.34 ❌
- **TP 4RR**: 25664.95 ❌
- **TP 15RR**: 25396.70 ❌
- **PnL**: -24.39 points (-1.0R)
- **MFE**: 27.00 points
- **MAE**: 26.50 points

### Trade #1984 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 00:15:00
- **FVG 5m**: 25766.75 - 25774.00
- **Entrée**: 25762.50 @ 2025-11-04 01:02:00
- **Stop Loss**: 25786.89
- **Risk**: 24.39 points
- **TP 1RR**: 25738.11 ✅
- **TP 2RR**: 25713.73 ❌
- **TP 3RR**: 25689.34 ❌
- **TP 4RR**: 25664.95 ❌
- **TP 15RR**: 25396.70 ❌
- **PnL**: -24.39 points (-1.0R)
- **MFE**: 27.00 points
- **MAE**: 26.50 points

### Trade #1985 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 04:15:00
- **FVG 5m**: 25717.25 - 25735.50
- **Entrée**: 25740.50 @ 2025-11-04 04:33:00
- **Stop Loss**: 25704.39
- **Risk**: 36.11 points
- **TP 1RR**: 25776.61 ✅
- **TP 2RR**: 25812.72 ❌
- **TP 3RR**: 25848.83 ❌
- **TP 4RR**: 25884.93 ❌
- **TP 15RR**: 26282.13 ❌
- **PnL**: -36.11 points (-1.0R)
- **MFE**: 52.00 points
- **MAE**: 36.25 points

### Trade #1986 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 08:45:00
- **FVG 5m**: 25855.75 - 25864.00
- **Entrée**: 25875.25 @ 2025-11-04 08:59:00
- **Stop Loss**: 25842.82
- **Risk**: 32.43 points
- **TP 1RR**: 25907.68 ❌
- **TP 2RR**: 25940.11 ❌
- **TP 3RR**: 25972.53 ❌
- **TP 4RR**: 26004.96 ❌
- **TP 15RR**: 26361.67 ❌
- **PnL**: -32.43 points (-1.0R)
- **MFE**: 10.50 points
- **MAE**: 38.25 points

### Trade #1987 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 08:45:00
- **FVG 5m**: 25855.75 - 25864.00
- **Entrée**: 25875.25 @ 2025-11-04 08:59:00
- **Stop Loss**: 25842.82
- **Risk**: 32.43 points
- **TP 1RR**: 25907.68 ❌
- **TP 2RR**: 25940.11 ❌
- **TP 3RR**: 25972.53 ❌
- **TP 4RR**: 26004.96 ❌
- **TP 15RR**: 26361.67 ❌
- **PnL**: -32.43 points (-1.0R)
- **MFE**: 10.50 points
- **MAE**: 38.25 points

### Trade #1988 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 09:45:00
- **FVG 5m**: 25720.50 - 25725.00
- **Entrée**: 25715.00 @ 2025-11-04 11:06:00
- **Stop Loss**: 25737.86
- **Risk**: 22.86 points
- **TP 1RR**: 25692.14 ✅
- **TP 2RR**: 25669.28 ✅
- **TP 3RR**: 25646.41 ✅
- **TP 4RR**: 25623.55 ✅
- **TP 15RR**: 25372.06 ✅
- **PnL**: 342.94 points (15.0R)
- **MFE**: 355.00 points
- **MAE**: 18.75 points

### Trade #1989 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 15:00:00
- **FVG 5m**: 25540.50 - 25573.75
- **Entrée**: 25539.75 @ 2025-11-04 17:03:00
- **Stop Loss**: 25586.54
- **Risk**: 46.79 points
- **TP 1RR**: 25492.96 ✅
- **TP 2RR**: 25446.18 ✅
- **TP 3RR**: 25399.39 ✅
- **TP 4RR**: 25352.60 ✅
- **TP 15RR**: 24837.95 ❌
- **PnL**: -46.79 points (-1.0R)
- **MFE**: 257.75 points
- **MAE**: 48.75 points

### Trade #1990 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 15:15:00
- **FVG 5m**: 25540.50 - 25573.75
- **Entrée**: 25539.75 @ 2025-11-04 17:03:00
- **Stop Loss**: 25586.54
- **Risk**: 46.79 points
- **TP 1RR**: 25492.96 ✅
- **TP 2RR**: 25446.18 ✅
- **TP 3RR**: 25399.39 ✅
- **TP 4RR**: 25352.60 ✅
- **TP 15RR**: 24837.95 ❌
- **PnL**: -46.79 points (-1.0R)
- **MFE**: 257.75 points
- **MAE**: 48.75 points

### Trade #1991 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 15:15:00
- **FVG 5m**: 25540.50 - 25573.75
- **Entrée**: 25539.75 @ 2025-11-04 17:03:00
- **Stop Loss**: 25586.54
- **Risk**: 46.79 points
- **TP 1RR**: 25492.96 ✅
- **TP 2RR**: 25446.18 ✅
- **TP 3RR**: 25399.39 ✅
- **TP 4RR**: 25352.60 ✅
- **TP 15RR**: 24837.95 ❌
- **PnL**: -46.79 points (-1.0R)
- **MFE**: 257.75 points
- **MAE**: 48.75 points

### Trade #1992 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:00:00
- **FVG 5m**: 25352.75 - 25357.25
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25369.93
- **Risk**: 18.43 points
- **TP 1RR**: 25333.07 ✅
- **TP 2RR**: 25314.64 ✅
- **TP 3RR**: 25296.21 ✅
- **TP 4RR**: 25277.79 ❌
- **TP 15RR**: 25075.07 ❌
- **PnL**: -18.43 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 40.25 points

### Trade #1993 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:00:00
- **FVG 5m**: 25352.75 - 25357.25
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25369.93
- **Risk**: 18.43 points
- **TP 1RR**: 25333.07 ✅
- **TP 2RR**: 25314.64 ✅
- **TP 3RR**: 25296.21 ✅
- **TP 4RR**: 25277.79 ❌
- **TP 15RR**: 25075.07 ❌
- **PnL**: -18.43 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 40.25 points

### Trade #1994 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:00:00
- **FVG 5m**: 25352.75 - 25357.25
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25369.93
- **Risk**: 18.43 points
- **TP 1RR**: 25333.07 ✅
- **TP 2RR**: 25314.64 ✅
- **TP 3RR**: 25296.21 ✅
- **TP 4RR**: 25277.79 ❌
- **TP 15RR**: 25075.07 ❌
- **PnL**: -18.43 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 40.25 points

### Trade #1995 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 19:45:00
- **FVG 5m**: 25323.25 - 25338.75
- **Entrée**: 25354.00 @ 2025-11-04 20:37:00
- **Stop Loss**: 25310.59
- **Risk**: 43.41 points
- **TP 1RR**: 25397.41 ✅
- **TP 2RR**: 25440.82 ✅
- **TP 3RR**: 25484.23 ✅
- **TP 4RR**: 25527.65 ✅
- **TP 15RR**: 26005.17 ❌
- **PnL**: -43.41 points (-1.0R)
- **MFE**: 526.00 points
- **MAE**: 50.75 points

### Trade #1996 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 20:30:00
- **FVG 5m**: 25358.75 - 25366.50
- **Entrée**: 25369.00 @ 2025-11-04 20:44:00
- **Stop Loss**: 25346.07
- **Risk**: 22.93 points
- **TP 1RR**: 25391.93 ✅
- **TP 2RR**: 25414.86 ✅
- **TP 3RR**: 25437.79 ✅
- **TP 4RR**: 25460.72 ✅
- **TP 15RR**: 25712.94 ✅
- **PnL**: 343.94 points (15.0R)
- **MFE**: 347.50 points
- **MAE**: 2.50 points

### Trade #1997 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-05 05:30:00
- **FVG 5m**: 25460.25 - 25469.75
- **Entrée**: 25471.00 @ 2025-11-05 05:44:00
- **Stop Loss**: 25447.52
- **Risk**: 23.48 points
- **TP 1RR**: 25494.48 ✅
- **TP 2RR**: 25517.96 ✅
- **TP 3RR**: 25541.44 ✅
- **TP 4RR**: 25564.92 ✅
- **TP 15RR**: 25823.20 ✅
- **PnL**: 352.20 points (15.0R)
- **MFE**: 354.75 points
- **MAE**: 12.75 points

### Trade #1998 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-05 18:30:00
- **FVG 5m**: 25666.00 - 25676.00
- **Entrée**: 25678.50 @ 2025-11-05 20:33:00
- **Stop Loss**: 25653.17
- **Risk**: 25.33 points
- **TP 1RR**: 25703.83 ✅
- **TP 2RR**: 25729.17 ✅
- **TP 3RR**: 25754.50 ❌
- **TP 4RR**: 25779.83 ❌
- **TP 15RR**: 26058.49 ❌
- **PnL**: -25.33 points (-1.0R)
- **MFE**: 64.00 points
- **MAE**: 34.00 points

### Trade #1999 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 07:45:00
- **FVG 5m**: 25774.25 - 25778.50
- **Entrée**: 25774.00 @ 2025-11-06 07:56:00
- **Stop Loss**: 25791.39
- **Risk**: 17.39 points
- **TP 1RR**: 25756.61 ✅
- **TP 2RR**: 25739.22 ✅
- **TP 3RR**: 25721.83 ✅
- **TP 4RR**: 25704.44 ✅
- **TP 15RR**: 25513.16 ✅
- **PnL**: 260.84 points (15.0R)
- **MFE**: 264.00 points
- **MAE**: 1.25 points

### Trade #2000 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 07:45:00
- **FVG 5m**: 25774.25 - 25778.50
- **Entrée**: 25774.00 @ 2025-11-06 07:56:00
- **Stop Loss**: 25791.39
- **Risk**: 17.39 points
- **TP 1RR**: 25756.61 ✅
- **TP 2RR**: 25739.22 ✅
- **TP 3RR**: 25721.83 ✅
- **TP 4RR**: 25704.44 ✅
- **TP 15RR**: 25513.16 ✅
- **PnL**: 260.84 points (15.0R)
- **MFE**: 264.00 points
- **MAE**: 1.25 points

### Trade #2001 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 08:00:00
- **FVG 5m**: 25701.50 - 25704.75
- **Entrée**: 25689.75 @ 2025-11-06 08:24:00
- **Stop Loss**: 25717.60
- **Risk**: 27.85 points
- **TP 1RR**: 25661.90 ✅
- **TP 2RR**: 25634.05 ✅
- **TP 3RR**: 25606.19 ✅
- **TP 4RR**: 25578.34 ✅
- **TP 15RR**: 25271.96 ✅
- **PnL**: 417.79 points (15.0R)
- **MFE**: 449.75 points
- **MAE**: 11.75 points

### Trade #2002 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 09:15:00
- **FVG 5m**: 25283.25 - 25288.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25270.61
- **Risk**: 27.64 points
- **TP 1RR**: 25325.89 ✅
- **TP 2RR**: 25353.53 ✅
- **TP 3RR**: 25381.17 ❌
- **TP 4RR**: 25408.82 ❌
- **TP 15RR**: 25712.87 ❌
- **PnL**: -27.64 points (-1.0R)
- **MFE**: 58.00 points
- **MAE**: 57.00 points

### Trade #2003 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 09:15:00
- **FVG 5m**: 25283.25 - 25288.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25270.61
- **Risk**: 27.64 points
- **TP 1RR**: 25325.89 ✅
- **TP 2RR**: 25353.53 ✅
- **TP 3RR**: 25381.17 ❌
- **TP 4RR**: 25408.82 ❌
- **TP 15RR**: 25712.87 ❌
- **PnL**: -27.64 points (-1.0R)
- **MFE**: 58.00 points
- **MAE**: 57.00 points

### Trade #2004 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 09:30:00
- **FVG 5m**: 25268.00 - 25296.00
- **Entrée**: 25258.00 @ 2025-11-06 10:37:00
- **Stop Loss**: 25308.65
- **Risk**: 50.65 points
- **TP 1RR**: 25207.35 ✅
- **TP 2RR**: 25156.70 ❌
- **TP 3RR**: 25106.06 ❌
- **TP 4RR**: 25055.41 ❌
- **TP 15RR**: 24498.28 ❌
- **PnL**: -50.65 points (-1.0R)
- **MFE**: 56.75 points
- **MAE**: 51.00 points

### Trade #2005 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 10:30:00
- **FVG 5m**: 25294.25 - 25326.25
- **Entrée**: 25291.00 @ 2025-11-06 12:04:00
- **Stop Loss**: 25338.91
- **Risk**: 47.91 points
- **TP 1RR**: 25243.09 ✅
- **TP 2RR**: 25195.17 ❌
- **TP 3RR**: 25147.26 ❌
- **TP 4RR**: 25099.35 ❌
- **TP 15RR**: 24572.30 ❌
- **PnL**: -47.91 points (-1.0R)
- **MFE**: 65.50 points
- **MAE**: 48.00 points

### Trade #2006 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 10:30:00
- **FVG 5m**: 25294.25 - 25326.25
- **Entrée**: 25291.00 @ 2025-11-06 12:04:00
- **Stop Loss**: 25338.91
- **Risk**: 47.91 points
- **TP 1RR**: 25243.09 ✅
- **TP 2RR**: 25195.17 ❌
- **TP 3RR**: 25147.26 ❌
- **TP 4RR**: 25099.35 ❌
- **TP 15RR**: 24572.30 ❌
- **PnL**: -47.91 points (-1.0R)
- **MFE**: 65.50 points
- **MAE**: 48.00 points

### Trade #2007 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 11:15:00
- **FVG 5m**: 25283.25 - 25288.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25270.61
- **Risk**: 27.64 points
- **TP 1RR**: 25325.89 ✅
- **TP 2RR**: 25353.53 ✅
- **TP 3RR**: 25381.17 ❌
- **TP 4RR**: 25408.82 ❌
- **TP 15RR**: 25712.87 ❌
- **PnL**: -27.64 points (-1.0R)
- **MFE**: 58.00 points
- **MAE**: 57.00 points

### Trade #2008 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 11:30:00
- **FVG 5m**: 25283.25 - 25288.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25270.61
- **Risk**: 27.64 points
- **TP 1RR**: 25325.89 ✅
- **TP 2RR**: 25353.53 ✅
- **TP 3RR**: 25381.17 ❌
- **TP 4RR**: 25408.82 ❌
- **TP 15RR**: 25712.87 ❌
- **PnL**: -27.64 points (-1.0R)
- **MFE**: 58.00 points
- **MAE**: 57.00 points

### Trade #2009 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 11:30:00
- **FVG 5m**: 25283.25 - 25288.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25270.61
- **Risk**: 27.64 points
- **TP 1RR**: 25325.89 ✅
- **TP 2RR**: 25353.53 ✅
- **TP 3RR**: 25381.17 ❌
- **TP 4RR**: 25408.82 ❌
- **TP 15RR**: 25712.87 ❌
- **PnL**: -27.64 points (-1.0R)
- **MFE**: 58.00 points
- **MAE**: 57.00 points

### Trade #2010 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 13:15:00
- **FVG 5m**: 25396.50 - 25409.25
- **Entrée**: 25416.75 @ 2025-11-06 13:26:00
- **Stop Loss**: 25383.80
- **Risk**: 32.95 points
- **TP 1RR**: 25449.70 ❌
- **TP 2RR**: 25482.65 ❌
- **TP 3RR**: 25515.59 ❌
- **TP 4RR**: 25548.54 ❌
- **TP 15RR**: 25910.97 ❌
- **PnL**: -32.95 points (-1.0R)
- **MFE**: 21.75 points
- **MAE**: 35.50 points

### Trade #2011 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 19:30:00
- **FVG 5m**: 25233.25 - 25246.50
- **Entrée**: 25252.75 @ 2025-11-06 20:33:00
- **Stop Loss**: 25220.63
- **Risk**: 32.12 points
- **TP 1RR**: 25284.87 ❌
- **TP 2RR**: 25316.98 ❌
- **TP 3RR**: 25349.10 ❌
- **TP 4RR**: 25381.22 ❌
- **TP 15RR**: 25734.50 ❌
- **PnL**: -32.12 points (-1.0R)
- **MFE**: 28.75 points
- **MAE**: 33.00 points

### Trade #2012 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 03:15:00
- **FVG 5m**: 25283.25 - 25292.25
- **Entrée**: 25280.50 @ 2025-11-07 03:27:00
- **Stop Loss**: 25304.90
- **Risk**: 24.40 points
- **TP 1RR**: 25256.10 ✅
- **TP 2RR**: 25231.71 ✅
- **TP 3RR**: 25207.31 ✅
- **TP 4RR**: 25182.92 ✅
- **TP 15RR**: 24914.56 ✅
- **PnL**: 365.94 points (15.0R)
- **MFE**: 392.50 points
- **MAE**: 3.50 points

### Trade #2013 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 04:15:00
- **FVG 5m**: 25120.50 - 25135.50
- **Entrée**: 25138.25 @ 2025-11-07 05:43:00
- **Stop Loss**: 25107.94
- **Risk**: 30.31 points
- **TP 1RR**: 25168.56 ✅
- **TP 2RR**: 25198.87 ❌
- **TP 3RR**: 25229.18 ❌
- **TP 4RR**: 25259.49 ❌
- **TP 15RR**: 25592.90 ❌
- **PnL**: -30.31 points (-1.0R)
- **MFE**: 57.25 points
- **MAE**: 31.50 points

### Trade #2014 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 05:00:00
- **FVG 5m**: 25133.75 - 25176.00
- **Entrée**: 25125.00 @ 2025-11-07 05:14:00
- **Stop Loss**: 25188.59
- **Risk**: 63.59 points
- **TP 1RR**: 25061.41 ❌
- **TP 2RR**: 24997.82 ❌
- **TP 3RR**: 24934.24 ❌
- **TP 4RR**: 24870.65 ❌
- **TP 15RR**: 24171.18 ❌
- **PnL**: -63.59 points (-1.0R)
- **MFE**: 40.75 points
- **MAE**: 66.25 points

### Trade #2015 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 05:45:00
- **FVG 5m**: 25093.50 - 25120.00
- **Entrée**: 25130.00 @ 2025-11-07 07:48:00
- **Stop Loss**: 25080.95
- **Risk**: 49.05 points
- **TP 1RR**: 25179.05 ❌
- **TP 2RR**: 25228.09 ❌
- **TP 3RR**: 25277.14 ❌
- **TP 4RR**: 25326.19 ❌
- **TP 15RR**: 25865.70 ❌
- **PnL**: -49.05 points (-1.0R)
- **MFE**: 12.00 points
- **MAE**: 51.00 points

### Trade #2016 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 06:30:00
- **FVG 5m**: 25113.00 - 25128.00
- **Entrée**: 25107.50 @ 2025-11-07 06:44:00
- **Stop Loss**: 25140.56
- **Risk**: 33.06 points
- **TP 1RR**: 25074.44 ✅
- **TP 2RR**: 25041.37 ❌
- **TP 3RR**: 25008.31 ❌
- **TP 4RR**: 24975.24 ❌
- **TP 15RR**: 24611.54 ❌
- **PnL**: -33.06 points (-1.0R)
- **MFE**: 45.75 points
- **MAE**: 37.25 points

### Trade #2017 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 08:30:00
- **FVG 5m**: 24975.75 - 24983.00
- **Entrée**: 24970.75 @ 2025-11-07 09:01:00
- **Stop Loss**: 24995.49
- **Risk**: 24.74 points
- **TP 1RR**: 24946.01 ✅
- **TP 2RR**: 24921.27 ✅
- **TP 3RR**: 24896.53 ✅
- **TP 4RR**: 24871.78 ❌
- **TP 15RR**: 24599.63 ❌
- **PnL**: -24.74 points (-1.0R)
- **MFE**: 88.75 points
- **MAE**: 29.75 points

### Trade #2018 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 08:30:00
- **FVG 5m**: 24975.75 - 24984.75
- **Entrée**: 25006.50 @ 2025-11-07 09:19:00
- **Stop Loss**: 24963.26
- **Risk**: 43.24 points
- **TP 1RR**: 25049.74 ❌
- **TP 2RR**: 25092.98 ❌
- **TP 3RR**: 25136.21 ❌
- **TP 4RR**: 25179.45 ❌
- **TP 15RR**: 25655.07 ❌
- **PnL**: -43.24 points (-1.0R)
- **MFE**: 32.50 points
- **MAE**: 50.00 points

### Trade #2019 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 11:15:00
- **FVG 5m**: 24805.25 - 24833.75
- **Entrée**: 24841.25 @ 2025-11-07 11:59:00
- **Stop Loss**: 24792.85
- **Risk**: 48.40 points
- **TP 1RR**: 24889.65 ✅
- **TP 2RR**: 24938.06 ✅
- **TP 3RR**: 24986.46 ✅
- **TP 4RR**: 25034.86 ✅
- **TP 15RR**: 25567.29 ✅
- **PnL**: 726.04 points (15.0R)
- **MFE**: 728.25 points
- **MAE**: 20.00 points

### Trade #2020 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 13:30:00
- **FVG 5m**: 25126.75 - 25160.75
- **Entrée**: 25167.75 @ 2025-11-07 14:58:00
- **Stop Loss**: 25114.19
- **Risk**: 53.56 points
- **TP 1RR**: 25221.31 ✅
- **TP 2RR**: 25274.88 ✅
- **TP 3RR**: 25328.44 ✅
- **TP 4RR**: 25382.00 ✅
- **TP 15RR**: 25971.20 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 662.25 points
- **MAE**: 14.25 points

### Trade #2021 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 15:00:00
- **FVG 5m**: 25208.75 - 25212.75
- **Entrée**: 25215.25 @ 2025-11-07 15:34:00
- **Stop Loss**: 25196.15
- **Risk**: 19.10 points
- **TP 1RR**: 25234.35 ✅
- **TP 2RR**: 25253.46 ✅
- **TP 3RR**: 25272.56 ✅
- **TP 4RR**: 25291.67 ✅
- **TP 15RR**: 25501.82 ✅
- **PnL**: 286.57 points (15.0R)
- **MFE**: 288.25 points
- **MAE**: 6.75 points

### Trade #2022 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-09 17:00:00
- **FVG 5m**: 25313.50 - 25335.00
- **Entrée**: 25300.50 @ 2025-11-09 18:03:00
- **Stop Loss**: 25347.67
- **Risk**: 47.17 points
- **TP 1RR**: 25253.33 ❌
- **TP 2RR**: 25206.17 ❌
- **TP 3RR**: 25159.00 ❌
- **TP 4RR**: 25111.83 ❌
- **TP 15RR**: 24592.99 ❌
- **PnL**: -47.17 points (-1.0R)
- **MFE**: 31.50 points
- **MAE**: 53.00 points

### Trade #2023 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-09 17:00:00
- **FVG 5m**: 25313.50 - 25335.00
- **Entrée**: 25300.50 @ 2025-11-09 18:03:00
- **Stop Loss**: 25347.67
- **Risk**: 47.17 points
- **TP 1RR**: 25253.33 ❌
- **TP 2RR**: 25206.17 ❌
- **TP 3RR**: 25159.00 ❌
- **TP 4RR**: 25111.83 ❌
- **TP 15RR**: 24592.99 ❌
- **PnL**: -47.17 points (-1.0R)
- **MFE**: 31.50 points
- **MAE**: 53.00 points

### Trade #2024 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 00:45:00
- **FVG 5m**: 25471.25 - 25477.00
- **Entrée**: 25463.25 @ 2025-11-10 02:12:00
- **Stop Loss**: 25489.74
- **Risk**: 26.49 points
- **TP 1RR**: 25436.76 ❌
- **TP 2RR**: 25410.27 ❌
- **TP 3RR**: 25383.78 ❌
- **TP 4RR**: 25357.30 ❌
- **TP 15RR**: 25065.92 ❌
- **PnL**: -26.49 points (-1.0R)
- **MFE**: 6.25 points
- **MAE**: 28.75 points

### Trade #2025 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-10 08:30:00
- **FVG 5m**: 25499.00 - 25511.25
- **Entrée**: 25513.25 @ 2025-11-10 10:58:00
- **Stop Loss**: 25486.25
- **Risk**: 27.00 points
- **TP 1RR**: 25540.25 ✅
- **TP 2RR**: 25567.25 ✅
- **TP 3RR**: 25594.25 ✅
- **TP 4RR**: 25621.25 ✅
- **TP 15RR**: 25918.24 ❌
- **PnL**: -27.00 points (-1.0R)
- **MFE**: 255.50 points
- **MAE**: 34.75 points

### Trade #2026 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 09:45:00
- **FVG 5m**: 25525.25 - 25539.50
- **Entrée**: 25524.00 @ 2025-11-10 09:59:00
- **Stop Loss**: 25552.27
- **Risk**: 28.27 points
- **TP 1RR**: 25495.73 ✅
- **TP 2RR**: 25467.46 ✅
- **TP 3RR**: 25439.19 ❌
- **TP 4RR**: 25410.92 ❌
- **TP 15RR**: 25099.95 ❌
- **PnL**: -28.27 points (-1.0R)
- **MFE**: 72.00 points
- **MAE**: 31.50 points

### Trade #2027 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-10 10:00:00
- **FVG 5m**: 25499.00 - 25511.25
- **Entrée**: 25513.25 @ 2025-11-10 10:58:00
- **Stop Loss**: 25486.25
- **Risk**: 27.00 points
- **TP 1RR**: 25540.25 ✅
- **TP 2RR**: 25567.25 ✅
- **TP 3RR**: 25594.25 ✅
- **TP 4RR**: 25621.25 ✅
- **TP 15RR**: 25918.24 ❌
- **PnL**: -27.00 points (-1.0R)
- **MFE**: 255.50 points
- **MAE**: 34.75 points

### Trade #2028 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 12:45:00
- **FVG 5m**: 25664.25 - 25667.75
- **Entrée**: 25663.00 @ 2025-11-10 12:56:00
- **Stop Loss**: 25680.58
- **Risk**: 17.58 points
- **TP 1RR**: 25645.42 ✅
- **TP 2RR**: 25627.83 ❌
- **TP 3RR**: 25610.25 ❌
- **TP 4RR**: 25592.66 ❌
- **TP 15RR**: 25399.24 ❌
- **PnL**: -17.58 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 23.00 points

### Trade #2029 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 14:45:00
- **FVG 5m**: 25722.50 - 25729.00
- **Entrée**: 25719.00 @ 2025-11-10 15:51:00
- **Stop Loss**: 25741.86
- **Risk**: 22.86 points
- **TP 1RR**: 25696.14 ❌
- **TP 2RR**: 25673.27 ❌
- **TP 3RR**: 25650.41 ❌
- **TP 4RR**: 25627.54 ❌
- **TP 15RR**: 25376.03 ❌
- **PnL**: -22.86 points (-1.0R)
- **MFE**: 18.00 points
- **MAE**: 23.75 points

### Trade #2030 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-11 08:45:00
- **FVG 5m**: 25587.25 - 25594.50
- **Entrée**: 25607.75 @ 2025-11-11 08:56:00
- **Stop Loss**: 25574.46
- **Risk**: 33.29 points
- **TP 1RR**: 25641.04 ❌
- **TP 2RR**: 25674.34 ❌
- **TP 3RR**: 25707.63 ❌
- **TP 4RR**: 25740.92 ❌
- **TP 15RR**: 26107.15 ❌
- **PnL**: -33.29 points (-1.0R)
- **MFE**: 25.75 points
- **MAE**: 63.25 points

### Trade #2031 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-11 12:30:00
- **FVG 5m**: 25638.25 - 25652.50
- **Entrée**: 25656.75 @ 2025-11-11 12:41:00
- **Stop Loss**: 25625.43
- **Risk**: 31.32 points
- **TP 1RR**: 25688.07 ✅
- **TP 2RR**: 25719.39 ❌
- **TP 3RR**: 25750.71 ❌
- **TP 4RR**: 25782.03 ❌
- **TP 15RR**: 26126.54 ❌
- **PnL**: -31.32 points (-1.0R)
- **MFE**: 39.50 points
- **MAE**: 32.75 points

### Trade #2032 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-11 19:00:00
- **FVG 5m**: 25722.00 - 25728.00
- **Entrée**: 25728.25 @ 2025-11-11 19:54:00
- **Stop Loss**: 25709.14
- **Risk**: 19.11 points
- **TP 1RR**: 25747.36 ✅
- **TP 2RR**: 25766.47 ❌
- **TP 3RR**: 25785.58 ❌
- **TP 4RR**: 25804.69 ❌
- **TP 15RR**: 26014.92 ❌
- **PnL**: -19.11 points (-1.0R)
- **MFE**: 33.25 points
- **MAE**: 19.75 points

### Trade #2033 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-11 19:15:00
- **FVG 5m**: 25728.00 - 25735.00
- **Entrée**: 25722.50 @ 2025-11-11 20:47:00
- **Stop Loss**: 25747.87
- **Risk**: 25.37 points
- **TP 1RR**: 25697.13 ✅
- **TP 2RR**: 25671.76 ❌
- **TP 3RR**: 25646.40 ❌
- **TP 4RR**: 25621.03 ❌
- **TP 15RR**: 25341.99 ❌
- **PnL**: -25.37 points (-1.0R)
- **MFE**: 28.25 points
- **MAE**: 27.25 points


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
| **TP 2** | 2x le risque |
| **TP 3** | 3x le risque |
| **TP 4** | 4x le risque |
| **TP 15** | 15x le risque |

### Gestion de Position Suggérée

- **20%** de la position à TP1 (1RR)
- **20%** de la position à TP2 (2RR)
- **20%** de la position à TP3 (3RR)
- **20%** de la position à TP4 (4RR)
- **20%** de la position à TP15 (15RR)

Ou bien:
- **50%** à TP2 (2RR)
- **50%** runner vers TP15 (15RR)


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

*Rapport généré le 2025-11-30 23:17:14*
