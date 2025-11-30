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
5. **Stop Loss**: Au-dessus/en-dessous du niveau de sweep
6. **Take Profits**: 1RR, 2RR, 3RR, 4RR, 15RR


## 📈 Résumé des Résultats

| Métrique | Valeur |
|----------|--------|
| Nombre total de trades | 1855 |
| Trades gagnants | 150 |
| Trades perdants | 1690 |
| Win Rate | 8.1% |
| PnL Total (points) | 37890.08 |
| Gain moyen | 1175.48 pts |
| Perte moyenne | -81.91 pts |


### 🎯 Analyse des Take Profits

| Take Profit | Atteints | Taux |
|-------------|----------|------|
| TP 1RR | 1125 | 60.6% |
| TP 2RR | 775 | 41.8% |
| TP 3RR | 580 | 31.3% |
| TP 4RR | 482 | 26.0% |
| TP 15RR | 150 | 8.1% |
| Stop Loss | 1690 | 91.1% |


### 📊 Analyse par Direction

| Direction | Trades | Gagnants | Win Rate |
|-----------|--------|----------|----------|
| LONG | 942 | 84 | 8.9% |
| SHORT | 913 | 66 | 7.2% |


## 📝 Détail des Trades

### Trade #1 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-02 07:15:00
- **FVG 5m**: 22093.10 - 22099.02
- **Entrée**: 22091.81 @ 2025-01-02 07:54:00
- **Stop Loss**: 22112.65
- **Risk**: 20.84 points
- **TP 1RR**: 22070.96 ✅
- **TP 2RR**: 22050.12 ✅
- **TP 3RR**: 22029.27 ✅
- **TP 4RR**: 22008.43 ✅
- **TP 15RR**: 21779.13 ✅
- **PnL**: 312.67 points (15.0R)
- **MFE**: 320.37 points
- **MAE**: 16.24 points

### Trade #2 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-02 08:30:00
- **FVG 5m**: 22031.24 - 22065.00
- **Entrée**: 22020.15 @ 2025-01-02 09:19:00
- **Stop Loss**: 22045.86
- **Risk**: 25.71 points
- **TP 1RR**: 21994.45 ✅
- **TP 2RR**: 21968.74 ✅
- **TP 3RR**: 21943.03 ✅
- **TP 4RR**: 21917.32 ✅
- **TP 15RR**: 21634.52 ✅
- **PnL**: 385.63 points (15.0R)
- **MFE**: 386.61 points
- **MAE**: 11.08 points

### Trade #3 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-02 09:15:00
- **FVG 5m**: 21892.83 - 21918.35
- **Entrée**: 21876.08 @ 2025-01-02 10:03:00
- **Stop Loss**: 22108.01
- **Risk**: 231.93 points
- **TP 1RR**: 21644.14 ✅
- **TP 2RR**: 21412.21 ❌
- **TP 3RR**: 21180.28 ❌
- **TP 4RR**: 20948.34 ❌
- **TP 15RR**: 18397.08 ❌
- **PnL**: -231.93 points (-1.0R)
- **MFE**: 242.53 points
- **MAE**: 232.23 points

### Trade #4 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-02 14:00:00
- **FVG 5m**: 21790.76 - 21794.12
- **Entrée**: 21797.47 @ 2025-01-02 14:11:00
- **Stop Loss**: 21703.36
- **Risk**: 94.11 points
- **TP 1RR**: 21891.57 ✅
- **TP 2RR**: 21985.68 ✅
- **TP 3RR**: 22079.79 ✅
- **TP 4RR**: 22173.90 ✅
- **TP 15RR**: 23209.08 ❌
- **PnL**: -94.11 points (-1.0R)
- **MFE**: 777.35 points
- **MAE**: 94.59 points

### Trade #5 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-02 14:45:00
- **FVG 5m**: 21823.50 - 21849.79
- **Entrée**: 21850.30 @ 2025-01-02 18:09:00
- **Stop Loss**: 21777.04
- **Risk**: 73.27 points
- **TP 1RR**: 21923.57 ✅
- **TP 2RR**: 21996.84 ✅
- **TP 3RR**: 22070.11 ✅
- **TP 4RR**: 22143.37 ✅
- **TP 15RR**: 22949.31 ❌
- **PnL**: -73.27 points (-1.0R)
- **MFE**: 724.51 points
- **MAE**: 127.58 points

### Trade #6 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 02:15:00
- **FVG 5m**: 21890.00 - 21905.46
- **Entrée**: 21889.74 @ 2025-01-03 02:28:00
- **Stop Loss**: 21943.75
- **Risk**: 54.01 points
- **TP 1RR**: 21835.73 ❌
- **TP 2RR**: 21781.72 ❌
- **TP 3RR**: 21727.71 ❌
- **TP 4RR**: 21673.70 ❌
- **TP 15RR**: 21079.60 ❌
- **PnL**: -54.01 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 54.13 points

### Trade #7 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 02:15:00
- **FVG 5m**: 21890.00 - 21905.46
- **Entrée**: 21889.74 @ 2025-01-03 02:28:00
- **Stop Loss**: 21943.75
- **Risk**: 54.01 points
- **TP 1RR**: 21835.73 ❌
- **TP 2RR**: 21781.72 ❌
- **TP 3RR**: 21727.71 ❌
- **TP 4RR**: 21673.70 ❌
- **TP 15RR**: 21079.60 ❌
- **PnL**: -54.01 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 54.13 points

### Trade #8 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 09:00:00
- **FVG 5m**: 22030.21 - 22049.79
- **Entrée**: 22028.40 @ 2025-01-03 09:12:00
- **Stop Loss**: 22115.75
- **Risk**: 87.34 points
- **TP 1RR**: 21941.06 ✅
- **TP 2RR**: 21853.71 ❌
- **TP 3RR**: 21766.37 ❌
- **TP 4RR**: 21679.03 ❌
- **TP 15RR**: 20718.24 ❌
- **PnL**: -87.34 points (-1.0R)
- **MFE**: 108.51 points
- **MAE**: 89.44 points

### Trade #9 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 15:00:00
- **FVG 5m**: 22182.79 - 22185.37
- **Entrée**: 22177.89 @ 2025-01-05 17:32:00
- **Stop Loss**: 22191.04
- **Risk**: 13.15 points
- **TP 1RR**: 22164.74 ❌
- **TP 2RR**: 22151.59 ❌
- **TP 3RR**: 22138.44 ❌
- **TP 4RR**: 22125.28 ❌
- **TP 15RR**: 21980.61 ❌
- **PnL**: -13.15 points (-1.0R)
- **MFE**: 10.31 points
- **MAE**: 17.78 points

### Trade #10 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-03 15:00:00
- **FVG 5m**: 22182.79 - 22185.37
- **Entrée**: 22177.89 @ 2025-01-05 17:32:00
- **Stop Loss**: 22191.04
- **Risk**: 13.15 points
- **TP 1RR**: 22164.74 ❌
- **TP 2RR**: 22151.59 ❌
- **TP 3RR**: 22138.44 ❌
- **TP 4RR**: 22125.28 ❌
- **TP 15RR**: 21980.61 ❌
- **PnL**: -13.15 points (-1.0R)
- **MFE**: 10.31 points
- **MAE**: 17.78 points

### Trade #11 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 01:00:00
- **FVG 5m**: 22392.33 - 22401.10
- **Entrée**: 22403.16 @ 2025-01-07 02:34:00
- **Stop Loss**: 22348.94
- **Risk**: 54.22 points
- **TP 1RR**: 22457.38 ✅
- **TP 2RR**: 22511.60 ❌
- **TP 3RR**: 22565.83 ❌
- **TP 4RR**: 22620.05 ❌
- **TP 15RR**: 23216.50 ❌
- **PnL**: -54.22 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 81.96 points

### Trade #12 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22382.54 - 22422.49
- **Entrée**: 22382.02 @ 2025-01-07 08:59:00
- **Stop Loss**: 22492.49
- **Risk**: 110.47 points
- **TP 1RR**: 22271.55 ✅
- **TP 2RR**: 22161.08 ✅
- **TP 3RR**: 22050.61 ✅
- **TP 4RR**: 21940.14 ✅
- **TP 15RR**: 20724.96 ❌
- **PnL**: -110.47 points (-1.0R)
- **MFE**: 1047.20 points
- **MAE**: 113.92 points

### Trade #13 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22382.54 - 22422.49
- **Entrée**: 22382.02 @ 2025-01-07 08:59:00
- **Stop Loss**: 22492.49
- **Risk**: 110.47 points
- **TP 1RR**: 22271.55 ✅
- **TP 2RR**: 22161.08 ✅
- **TP 3RR**: 22050.61 ✅
- **TP 4RR**: 21940.14 ✅
- **TP 15RR**: 20724.96 ❌
- **PnL**: -110.47 points (-1.0R)
- **MFE**: 1047.20 points
- **MAE**: 113.92 points

### Trade #14 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 08:30:00
- **FVG 5m**: 22382.54 - 22422.49
- **Entrée**: 22382.02 @ 2025-01-07 08:59:00
- **Stop Loss**: 22492.49
- **Risk**: 110.47 points
- **TP 1RR**: 22271.55 ✅
- **TP 2RR**: 22161.08 ✅
- **TP 3RR**: 22050.61 ✅
- **TP 4RR**: 21940.14 ✅
- **TP 15RR**: 20724.96 ❌
- **PnL**: -110.47 points (-1.0R)
- **MFE**: 1047.20 points
- **MAE**: 113.92 points

### Trade #15 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 09:30:00
- **FVG 5m**: 22122.22 - 22164.23
- **Entrée**: 22119.90 @ 2025-01-07 10:53:00
- **Stop Loss**: 22265.83
- **Risk**: 145.93 points
- **TP 1RR**: 21973.97 ✅
- **TP 2RR**: 21828.05 ✅
- **TP 3RR**: 21682.12 ✅
- **TP 4RR**: 21536.20 ✅
- **TP 15RR**: 19931.01 ❌
- **PnL**: -145.93 points (-1.0R)
- **MFE**: 785.08 points
- **MAE**: 150.01 points

### Trade #16 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 09:30:00
- **FVG 5m**: 22122.22 - 22164.23
- **Entrée**: 22119.90 @ 2025-01-07 10:53:00
- **Stop Loss**: 22265.83
- **Risk**: 145.93 points
- **TP 1RR**: 21973.97 ✅
- **TP 2RR**: 21828.05 ✅
- **TP 3RR**: 21682.12 ✅
- **TP 4RR**: 21536.20 ✅
- **TP 15RR**: 19931.01 ❌
- **PnL**: -145.93 points (-1.0R)
- **MFE**: 785.08 points
- **MAE**: 150.01 points

### Trade #17 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 09:30:00
- **FVG 5m**: 22122.22 - 22164.23
- **Entrée**: 22119.90 @ 2025-01-07 10:53:00
- **Stop Loss**: 22265.83
- **Risk**: 145.93 points
- **TP 1RR**: 21973.97 ✅
- **TP 2RR**: 21828.05 ✅
- **TP 3RR**: 21682.12 ✅
- **TP 4RR**: 21536.20 ✅
- **TP 15RR**: 19931.01 ❌
- **PnL**: -145.93 points (-1.0R)
- **MFE**: 785.08 points
- **MAE**: 150.01 points

### Trade #18 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 09:45:00
- **FVG 5m**: 22171.19 - 22187.94
- **Entrée**: 22188.20 @ 2025-01-07 09:57:00
- **Stop Loss**: 22051.14
- **Risk**: 137.07 points
- **TP 1RR**: 22325.27 ❌
- **TP 2RR**: 22462.34 ❌
- **TP 3RR**: 22599.40 ❌
- **TP 4RR**: 22736.47 ❌
- **TP 15RR**: 24244.20 ❌
- **PnL**: -137.07 points (-1.0R)
- **MFE**: 53.09 points
- **MAE**: 138.92 points

### Trade #19 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 09:45:00
- **FVG 5m**: 22171.19 - 22187.94
- **Entrée**: 22188.20 @ 2025-01-07 09:57:00
- **Stop Loss**: 22051.14
- **Risk**: 137.07 points
- **TP 1RR**: 22325.27 ❌
- **TP 2RR**: 22462.34 ❌
- **TP 3RR**: 22599.40 ❌
- **TP 4RR**: 22736.47 ❌
- **TP 15RR**: 24244.20 ❌
- **PnL**: -137.07 points (-1.0R)
- **MFE**: 53.09 points
- **MAE**: 138.92 points

### Trade #20 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-07 10:45:00
- **FVG 5m**: 22103.15 - 22108.04
- **Entrée**: 22101.60 @ 2025-01-07 11:22:00
- **Stop Loss**: 22207.29
- **Risk**: 105.69 points
- **TP 1RR**: 21995.91 ✅
- **TP 2RR**: 21890.22 ✅
- **TP 3RR**: 21784.53 ✅
- **TP 4RR**: 21678.84 ✅
- **TP 15RR**: 20516.26 ❌
- **PnL**: -105.69 points (-1.0R)
- **MFE**: 766.78 points
- **MAE**: 110.57 points

### Trade #21 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 11:45:00
- **FVG 5m**: 22079.44 - 22102.63
- **Entrée**: 22109.08 @ 2025-01-07 11:59:00
- **Stop Loss**: 22038.25
- **Risk**: 70.82 points
- **TP 1RR**: 22179.90 ✅
- **TP 2RR**: 22250.72 ❌
- **TP 3RR**: 22321.54 ❌
- **TP 4RR**: 22392.36 ❌
- **TP 15RR**: 23171.39 ❌
- **PnL**: -70.82 points (-1.0R)
- **MFE**: 74.49 points
- **MAE**: 76.03 points

### Trade #22 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-07 15:00:00
- **FVG 5m**: 22041.29 - 22046.19
- **Entrée**: 22047.22 @ 2025-01-07 17:54:00
- **Stop Loss**: 22008.63
- **Risk**: 38.59 points
- **TP 1RR**: 22085.81 ✅
- **TP 2RR**: 22124.39 ❌
- **TP 3RR**: 22162.98 ❌
- **TP 4RR**: 22201.57 ❌
- **TP 15RR**: 22626.04 ❌
- **PnL**: -38.59 points (-1.0R)
- **MFE**: 65.21 points
- **MAE**: 56.70 points

### Trade #23 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 01:45:00
- **FVG 5m**: 22064.23 - 22068.09
- **Entrée**: 22072.22 @ 2025-01-08 02:48:00
- **Stop Loss**: 22028.47
- **Risk**: 43.75 points
- **TP 1RR**: 22115.97 ❌
- **TP 2RR**: 22159.72 ❌
- **TP 3RR**: 22203.48 ❌
- **TP 4RR**: 22247.23 ❌
- **TP 15RR**: 22728.51 ❌
- **PnL**: -43.75 points (-1.0R)
- **MFE**: 40.21 points
- **MAE**: 81.70 points

### Trade #24 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 05:00:00
- **FVG 5m**: 22097.73 - 22101.86
- **Entrée**: 22096.45 @ 2025-01-08 05:12:00
- **Stop Loss**: 22123.22
- **Risk**: 26.78 points
- **TP 1RR**: 22069.67 ✅
- **TP 2RR**: 22042.89 ✅
- **TP 3RR**: 22016.11 ✅
- **TP 4RR**: 21989.33 ✅
- **TP 15RR**: 21694.77 ✅
- **PnL**: 401.67 points (15.0R)
- **MFE**: 411.10 points
- **MAE**: 1.29 points

### Trade #25 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 05:00:00
- **FVG 5m**: 22097.73 - 22101.86
- **Entrée**: 22096.45 @ 2025-01-08 05:12:00
- **Stop Loss**: 22123.22
- **Risk**: 26.78 points
- **TP 1RR**: 22069.67 ✅
- **TP 2RR**: 22042.89 ✅
- **TP 3RR**: 22016.11 ✅
- **TP 4RR**: 21989.33 ✅
- **TP 15RR**: 21694.77 ✅
- **PnL**: 401.67 points (15.0R)
- **MFE**: 411.10 points
- **MAE**: 1.29 points

### Trade #26 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 06:30:00
- **FVG 5m**: 21922.47 - 21947.99
- **Entrée**: 21958.04 @ 2025-01-08 07:08:00
- **Stop Loss**: 21867.72
- **Risk**: 90.32 points
- **TP 1RR**: 22048.36 ✅
- **TP 2RR**: 22138.69 ❌
- **TP 3RR**: 22229.01 ❌
- **TP 4RR**: 22319.33 ❌
- **TP 15RR**: 23312.89 ❌
- **PnL**: -90.32 points (-1.0R)
- **MFE**: 124.23 points
- **MAE**: 103.61 points

### Trade #27 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 09:00:00
- **FVG 5m**: 21959.33 - 22004.95
- **Entrée**: 21957.27 @ 2025-01-08 09:12:00
- **Stop Loss**: 22080.16
- **Risk**: 122.89 points
- **TP 1RR**: 21834.37 ❌
- **TP 2RR**: 21711.48 ❌
- **TP 3RR**: 21588.58 ❌
- **TP 4RR**: 21465.69 ❌
- **TP 15RR**: 20113.85 ❌
- **PnL**: -122.89 points (-1.0R)
- **MFE**: 68.82 points
- **MAE**: 123.20 points

### Trade #28 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 11:15:00
- **FVG 5m**: 21875.05 - 21894.63
- **Entrée**: 21857.00 @ 2025-01-08 11:28:00
- **Stop Loss**: 21974.18
- **Risk**: 117.17 points
- **TP 1RR**: 21739.83 ❌
- **TP 2RR**: 21622.66 ❌
- **TP 3RR**: 21505.49 ❌
- **TP 4RR**: 21388.32 ❌
- **TP 15RR**: 20099.44 ❌
- **PnL**: -117.17 points (-1.0R)
- **MFE**: 35.31 points
- **MAE**: 134.54 points

### Trade #29 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21810.78
- **Risk**: 168.39 points
- **TP 1RR**: 22147.56 ❌
- **TP 2RR**: 22315.96 ❌
- **TP 3RR**: 22484.35 ❌
- **TP 4RR**: 22652.74 ❌
- **TP 15RR**: 24505.04 ❌
- **PnL**: -168.39 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 256.45 points

### Trade #30 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21810.78
- **Risk**: 168.39 points
- **TP 1RR**: 22147.56 ❌
- **TP 2RR**: 22315.96 ❌
- **TP 3RR**: 22484.35 ❌
- **TP 4RR**: 22652.74 ❌
- **TP 15RR**: 24505.04 ❌
- **PnL**: -168.39 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 256.45 points

### Trade #31 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21810.78
- **Risk**: 168.39 points
- **TP 1RR**: 22147.56 ❌
- **TP 2RR**: 22315.96 ❌
- **TP 3RR**: 22484.35 ❌
- **TP 4RR**: 22652.74 ❌
- **TP 15RR**: 24505.04 ❌
- **PnL**: -168.39 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 256.45 points

### Trade #32 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21810.78
- **Risk**: 168.39 points
- **TP 1RR**: 22147.56 ❌
- **TP 2RR**: 22315.96 ❌
- **TP 3RR**: 22484.35 ❌
- **TP 4RR**: 22652.74 ❌
- **TP 15RR**: 24505.04 ❌
- **PnL**: -168.39 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 256.45 points

### Trade #33 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21810.78
- **Risk**: 168.39 points
- **TP 1RR**: 22147.56 ❌
- **TP 2RR**: 22315.96 ❌
- **TP 3RR**: 22484.35 ❌
- **TP 4RR**: 22652.74 ❌
- **TP 15RR**: 24505.04 ❌
- **PnL**: -168.39 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 256.45 points

### Trade #34 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21810.78
- **Risk**: 168.39 points
- **TP 1RR**: 22147.56 ❌
- **TP 2RR**: 22315.96 ❌
- **TP 3RR**: 22484.35 ❌
- **TP 4RR**: 22652.74 ❌
- **TP 15RR**: 24505.04 ❌
- **PnL**: -168.39 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 256.45 points

### Trade #35 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-08 11:30:00
- **FVG 5m**: 21945.41 - 21961.90
- **Entrée**: 21979.17 @ 2025-01-08 12:02:00
- **Stop Loss**: 21810.78
- **Risk**: 168.39 points
- **TP 1RR**: 22147.56 ❌
- **TP 2RR**: 22315.96 ❌
- **TP 3RR**: 22484.35 ❌
- **TP 4RR**: 22652.74 ❌
- **TP 15RR**: 24505.04 ❌
- **PnL**: -168.39 points (-1.0R)
- **MFE**: 116.24 points
- **MAE**: 256.45 points

### Trade #36 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 13:15:00
- **FVG 5m**: 22011.13 - 22013.45
- **Entrée**: 22007.27 @ 2025-01-08 13:36:00
- **Stop Loss**: 22106.46
- **Risk**: 99.20 points
- **TP 1RR**: 21908.07 ✅
- **TP 2RR**: 21808.88 ✅
- **TP 3RR**: 21709.68 ✅
- **TP 4RR**: 21610.49 ✅
- **TP 15RR**: 20519.34 ❌
- **PnL**: -99.20 points (-1.0R)
- **MFE**: 672.45 points
- **MAE**: 100.52 points

### Trade #37 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-08 13:30:00
- **FVG 5m**: 21999.28 - 22013.45
- **Entrée**: 21983.56 @ 2025-01-08 15:35:00
- **Stop Loss**: 22092.02
- **Risk**: 108.47 points
- **TP 1RR**: 21875.09 ✅
- **TP 2RR**: 21766.62 ✅
- **TP 3RR**: 21658.15 ✅
- **TP 4RR**: 21549.69 ✅
- **TP 15RR**: 20356.55 ❌
- **PnL**: -108.47 points (-1.0R)
- **MFE**: 648.74 points
- **MAE**: 113.41 points

### Trade #38 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 02:15:00
- **FVG 5m**: 21922.47 - 21935.10
- **Entrée**: 21938.45 @ 2025-01-09 02:29:00
- **Stop Loss**: 21887.55
- **Risk**: 50.90 points
- **TP 1RR**: 21989.35 ✅
- **TP 2RR**: 22040.25 ❌
- **TP 3RR**: 22091.15 ❌
- **TP 4RR**: 22142.05 ❌
- **TP 15RR**: 22701.94 ❌
- **PnL**: -50.90 points (-1.0R)
- **MFE**: 56.70 points
- **MAE**: 70.36 points

### Trade #39 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 02:30:00
- **FVG 5m**: 21953.66 - 21957.52
- **Entrée**: 21964.74 @ 2025-01-09 03:37:00
- **Stop Loss**: 21924.13
- **Risk**: 40.61 points
- **TP 1RR**: 22005.35 ❌
- **TP 2RR**: 22045.96 ❌
- **TP 3RR**: 22086.56 ❌
- **TP 4RR**: 22127.17 ❌
- **TP 15RR**: 22573.86 ❌
- **PnL**: -40.61 points (-1.0R)
- **MFE**: 30.41 points
- **MAE**: 41.24 points

### Trade #40 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-09 19:00:00
- **FVG 5m**: 21925.31 - 21929.69
- **Entrée**: 21934.33 @ 2025-01-09 20:52:00
- **Stop Loss**: 21839.12
- **Risk**: 95.21 points
- **TP 1RR**: 22029.53 ✅
- **TP 2RR**: 22124.74 ❌
- **TP 3RR**: 22219.95 ❌
- **TP 4RR**: 22315.15 ❌
- **TP 15RR**: 23362.42 ❌
- **PnL**: -95.21 points (-1.0R)
- **MFE**: 100.00 points
- **MAE**: 211.61 points

### Trade #41 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-09 23:30:00
- **FVG 5m**: 21941.03 - 21944.12
- **Entrée**: 21936.90 @ 2025-01-10 00:25:00
- **Stop Loss**: 21999.96
- **Risk**: 63.06 points
- **TP 1RR**: 21873.85 ❌
- **TP 2RR**: 21810.79 ❌
- **TP 3RR**: 21747.73 ❌
- **TP 4RR**: 21684.67 ❌
- **TP 15RR**: 20991.03 ❌
- **PnL**: -63.06 points (-1.0R)
- **MFE**: 45.62 points
- **MAE**: 69.59 points

### Trade #42 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 05:15:00
- **FVG 5m**: 21970.67 - 21973.76
- **Entrée**: 21969.12 @ 2025-01-10 06:04:00
- **Stop Loss**: 22038.39
- **Risk**: 69.26 points
- **TP 1RR**: 21899.86 ✅
- **TP 2RR**: 21830.60 ✅
- **TP 3RR**: 21761.33 ✅
- **TP 4RR**: 21692.07 ✅
- **TP 15RR**: 20930.17 ❌
- **PnL**: -69.26 points (-1.0R)
- **MFE**: 634.30 points
- **MAE**: 82.22 points

### Trade #43 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 05:45:00
- **FVG 5m**: 21970.67 - 21973.76
- **Entrée**: 21969.12 @ 2025-01-10 06:04:00
- **Stop Loss**: 22016.21
- **Risk**: 47.09 points
- **TP 1RR**: 21922.04 ✅
- **TP 2RR**: 21874.95 ✅
- **TP 3RR**: 21827.86 ✅
- **TP 4RR**: 21780.78 ✅
- **TP 15RR**: 21262.83 ❌
- **PnL**: -47.09 points (-1.0R)
- **MFE**: 634.30 points
- **MAE**: 52.58 points

### Trade #44 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 05:45:00
- **FVG 5m**: 21970.67 - 21973.76
- **Entrée**: 21969.12 @ 2025-01-10 06:04:00
- **Stop Loss**: 22016.21
- **Risk**: 47.09 points
- **TP 1RR**: 21922.04 ✅
- **TP 2RR**: 21874.95 ✅
- **TP 3RR**: 21827.86 ✅
- **TP 4RR**: 21780.78 ✅
- **TP 15RR**: 21262.83 ❌
- **PnL**: -47.09 points (-1.0R)
- **MFE**: 634.30 points
- **MAE**: 52.58 points

### Trade #45 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-10 06:00:00
- **FVG 5m**: 21966.03 - 21970.67
- **Entrée**: 21959.59 @ 2025-01-10 07:11:00
- **Stop Loss**: 21994.80
- **Risk**: 35.22 points
- **TP 1RR**: 21924.37 ✅
- **TP 2RR**: 21889.15 ✅
- **TP 3RR**: 21853.93 ✅
- **TP 4RR**: 21818.71 ✅
- **TP 15RR**: 21431.29 ✅
- **PnL**: 528.29 points (15.0R)
- **MFE**: 532.24 points
- **MAE**: 20.62 points

### Trade #46 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-10 09:15:00
- **FVG 5m**: 21585.09 - 21600.04
- **Entrée**: 21603.39 @ 2025-01-10 11:29:00
- **Stop Loss**: 21540.29
- **Risk**: 63.10 points
- **TP 1RR**: 21666.48 ✅
- **TP 2RR**: 21729.58 ✅
- **TP 3RR**: 21792.68 ✅
- **TP 4RR**: 21855.77 ❌
- **TP 15RR**: 22549.84 ❌
- **PnL**: -63.10 points (-1.0R)
- **MFE**: 228.87 points
- **MAE**: 68.04 points

### Trade #47 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-12 21:15:00
- **FVG 5m**: 21528.90 - 21533.54
- **Entrée**: 21536.12 @ 2025-01-12 22:01:00
- **Stop Loss**: 21493.66
- **Risk**: 42.45 points
- **TP 1RR**: 21578.57 ❌
- **TP 2RR**: 21621.02 ❌
- **TP 3RR**: 21663.48 ❌
- **TP 4RR**: 21705.93 ❌
- **TP 15RR**: 22172.93 ❌
- **PnL**: -42.45 points (-1.0R)
- **MFE**: 41.75 points
- **MAE**: 48.20 points

### Trade #48 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 01:15:00
- **FVG 5m**: 21539.72 - 21542.30
- **Entrée**: 21545.39 @ 2025-01-13 02:04:00
- **Stop Loss**: 21502.68
- **Risk**: 42.72 points
- **TP 1RR**: 21588.11 ❌
- **TP 2RR**: 21630.83 ❌
- **TP 3RR**: 21673.54 ❌
- **TP 4RR**: 21716.26 ❌
- **TP 15RR**: 22186.14 ❌
- **PnL**: -42.72 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 57.48 points

### Trade #49 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 08:30:00
- **FVG 5m**: 21424.51 - 21432.76
- **Entrée**: 21435.85 @ 2025-01-13 08:53:00
- **Stop Loss**: 21332.40
- **Risk**: 103.46 points
- **TP 1RR**: 21539.31 ✅
- **TP 2RR**: 21642.77 ✅
- **TP 3RR**: 21746.23 ✅
- **TP 4RR**: 21849.69 ✅
- **TP 15RR**: 22987.73 ✅
- **PnL**: 1551.88 points (15.0R)
- **MFE**: 1553.15 points
- **MAE**: 80.16 points

### Trade #50 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-13 09:45:00
- **FVG 5m**: 21433.28 - 21437.40
- **Entrée**: 21429.15 @ 2025-01-13 10:04:00
- **Stop Loss**: 21537.60
- **Risk**: 108.45 points
- **TP 1RR**: 21320.71 ❌
- **TP 2RR**: 21212.26 ❌
- **TP 3RR**: 21103.81 ❌
- **TP 4RR**: 20995.36 ❌
- **TP 15RR**: 19802.44 ❌
- **PnL**: -108.45 points (-1.0R)
- **MFE**: 69.33 points
- **MAE**: 112.89 points

### Trade #51 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 11:45:00
- **FVG 5m**: 21514.21 - 21524.78
- **Entrée**: 21528.13 @ 2025-01-13 11:58:00
- **Stop Loss**: 21451.93
- **Risk**: 76.20 points
- **TP 1RR**: 21604.32 ✅
- **TP 2RR**: 21680.52 ✅
- **TP 3RR**: 21756.72 ✅
- **TP 4RR**: 21832.92 ❌
- **TP 15RR**: 22671.09 ❌
- **PnL**: -76.20 points (-1.0R)
- **MFE**: 270.37 points
- **MAE**: 78.87 points

### Trade #52 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 11:45:00
- **FVG 5m**: 21514.21 - 21524.78
- **Entrée**: 21528.13 @ 2025-01-13 11:58:00
- **Stop Loss**: 21451.93
- **Risk**: 76.20 points
- **TP 1RR**: 21604.32 ✅
- **TP 2RR**: 21680.52 ✅
- **TP 3RR**: 21756.72 ✅
- **TP 4RR**: 21832.92 ❌
- **TP 15RR**: 22671.09 ❌
- **PnL**: -76.20 points (-1.0R)
- **MFE**: 270.37 points
- **MAE**: 78.87 points

### Trade #53 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-13 12:30:00
- **FVG 5m**: 21506.48 - 21512.92
- **Entrée**: 21496.68 @ 2025-01-13 13:14:00
- **Stop Loss**: 21566.74
- **Risk**: 70.06 points
- **TP 1RR**: 21426.62 ❌
- **TP 2RR**: 21356.56 ❌
- **TP 3RR**: 21286.51 ❌
- **TP 4RR**: 21216.45 ❌
- **TP 15RR**: 20445.80 ❌
- **PnL**: -70.06 points (-1.0R)
- **MFE**: 16.24 points
- **MAE**: 71.14 points

### Trade #54 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 14:45:00
- **FVG 5m**: 21635.35 - 21661.64
- **Entrée**: 21679.68 @ 2025-01-13 17:00:00
- **Stop Loss**: 21526.64
- **Risk**: 153.04 points
- **TP 1RR**: 21832.72 ❌
- **TP 2RR**: 21985.76 ❌
- **TP 3RR**: 22138.80 ❌
- **TP 4RR**: 22291.85 ❌
- **TP 15RR**: 23975.31 ❌
- **PnL**: -153.04 points (-1.0R)
- **MFE**: 118.82 points
- **MAE**: 157.48 points

### Trade #55 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-13 15:15:00
- **FVG 5m**: 21635.35 - 21661.64
- **Entrée**: 21679.68 @ 2025-01-13 17:00:00
- **Stop Loss**: 21606.24
- **Risk**: 73.44 points
- **TP 1RR**: 21753.12 ✅
- **TP 2RR**: 21826.56 ❌
- **TP 3RR**: 21900.00 ❌
- **TP 4RR**: 21973.44 ❌
- **TP 15RR**: 22781.27 ❌
- **PnL**: -73.44 points (-1.0R)
- **MFE**: 118.82 points
- **MAE**: 77.06 points

### Trade #56 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 00:30:00
- **FVG 5m**: 21691.53 - 21694.88
- **Entrée**: 21687.41 @ 2025-01-14 01:01:00
- **Stop Loss**: 21722.49
- **Risk**: 35.08 points
- **TP 1RR**: 21652.33 ❌
- **TP 2RR**: 21617.24 ❌
- **TP 3RR**: 21582.16 ❌
- **TP 4RR**: 21547.08 ❌
- **TP 15RR**: 21161.16 ❌
- **PnL**: -35.08 points (-1.0R)
- **MFE**: 15.21 points
- **MAE**: 38.66 points

### Trade #57 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 05:15:00
- **FVG 5m**: 21680.71 - 21689.47
- **Entrée**: 21675.04 @ 2025-01-14 06:07:00
- **Stop Loss**: 21751.63
- **Risk**: 76.59 points
- **TP 1RR**: 21598.44 ✅
- **TP 2RR**: 21521.85 ❌
- **TP 3RR**: 21445.26 ❌
- **TP 4RR**: 21368.66 ❌
- **TP 15RR**: 20526.12 ❌
- **PnL**: -76.59 points (-1.0R)
- **MFE**: 82.48 points
- **MAE**: 113.41 points

### Trade #58 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 06:15:00
- **FVG 5m**: 21611.38 - 21695.14
- **Entrée**: 21713.44 @ 2025-01-14 07:38:00
- **Stop Loss**: 21610.62
- **Risk**: 102.82 points
- **TP 1RR**: 21816.27 ❌
- **TP 2RR**: 21919.09 ❌
- **TP 3RR**: 22021.92 ❌
- **TP 4RR**: 22124.74 ❌
- **TP 15RR**: 23255.81 ❌
- **PnL**: -102.82 points (-1.0R)
- **MFE**: 70.62 points
- **MAE**: 105.42 points

### Trade #59 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 06:30:00
- **FVG 5m**: 21611.38 - 21695.14
- **Entrée**: 21713.44 @ 2025-01-14 07:38:00
- **Stop Loss**: 21640.76
- **Risk**: 72.68 points
- **TP 1RR**: 21786.13 ❌
- **TP 2RR**: 21858.81 ❌
- **TP 3RR**: 21931.49 ❌
- **TP 4RR**: 22004.18 ❌
- **TP 15RR**: 22803.70 ❌
- **PnL**: -72.68 points (-1.0R)
- **MFE**: 70.62 points
- **MAE**: 72.94 points

### Trade #60 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 07:30:00
- **FVG 5m**: 21731.74 - 21737.15
- **Entrée**: 21708.54 @ 2025-01-14 08:47:00
- **Stop Loss**: 21803.98
- **Risk**: 95.44 points
- **TP 1RR**: 21613.11 ✅
- **TP 2RR**: 21517.67 ✅
- **TP 3RR**: 21422.24 ✅
- **TP 4RR**: 21326.80 ❌
- **TP 15RR**: 20277.01 ❌
- **PnL**: -95.44 points (-1.0R)
- **MFE**: 291.76 points
- **MAE**: 167.27 points

### Trade #61 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 07:30:00
- **FVG 5m**: 21704.16 - 21714.22
- **Entrée**: 21716.28 @ 2025-01-14 08:17:00
- **Stop Loss**: 21595.93
- **Risk**: 120.34 points
- **TP 1RR**: 21836.62 ❌
- **TP 2RR**: 21956.96 ❌
- **TP 3RR**: 22077.31 ❌
- **TP 4RR**: 22197.65 ❌
- **TP 15RR**: 23521.43 ❌
- **PnL**: -120.34 points (-1.0R)
- **MFE**: 67.79 points
- **MAE**: 130.67 points

### Trade #62 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-14 10:00:00
- **FVG 5m**: 21510.60 - 21525.03
- **Entrée**: 21506.99 @ 2025-01-14 10:41:00
- **Stop Loss**: 21602.58
- **Risk**: 95.59 points
- **TP 1RR**: 21411.40 ❌
- **TP 2RR**: 21315.81 ❌
- **TP 3RR**: 21220.21 ❌
- **TP 4RR**: 21124.62 ❌
- **TP 15RR**: 20073.10 ❌
- **PnL**: -95.59 points (-1.0R)
- **MFE**: 71.39 points
- **MAE**: 96.91 points

### Trade #63 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 11:00:00
- **FVG 5m**: 21479.93 - 21493.33
- **Entrée**: 21503.38 @ 2025-01-14 11:42:00
- **Stop Loss**: 21441.88
- **Risk**: 61.50 points
- **TP 1RR**: 21564.88 ✅
- **TP 2RR**: 21626.39 ✅
- **TP 3RR**: 21687.89 ❌
- **TP 4RR**: 21749.39 ❌
- **TP 15RR**: 22425.90 ❌
- **PnL**: -61.50 points (-1.0R)
- **MFE**: 160.57 points
- **MAE**: 80.93 points

### Trade #64 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-14 12:30:00
- **FVG 5m**: 21604.68 - 21619.88
- **Entrée**: 21629.93 @ 2025-01-14 12:43:00
- **Stop Loss**: 21563.99
- **Risk**: 65.94 points
- **TP 1RR**: 21695.88 ❌
- **TP 2RR**: 21761.82 ❌
- **TP 3RR**: 21827.77 ❌
- **TP 4RR**: 21893.71 ❌
- **TP 15RR**: 22619.10 ❌
- **PnL**: -65.94 points (-1.0R)
- **MFE**: 34.02 points
- **MAE**: 67.79 points

### Trade #65 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 02:00:00
- **FVG 5m**: 21576.58 - 21581.22
- **Entrée**: 21581.99 @ 2025-01-15 02:23:00
- **Stop Loss**: 21545.70
- **Risk**: 36.29 points
- **TP 1RR**: 21618.29 ✅
- **TP 2RR**: 21654.58 ✅
- **TP 3RR**: 21690.88 ✅
- **TP 4RR**: 21727.17 ✅
- **TP 15RR**: 22126.41 ✅
- **PnL**: 544.42 points (15.0R)
- **MFE**: 547.96 points
- **MAE**: 7.73 points

### Trade #66 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 02:15:00
- **FVG 5m**: 21584.06 - 21588.44
- **Entrée**: 21589.21 @ 2025-01-15 02:30:00
- **Stop Loss**: 21552.40
- **Risk**: 36.81 points
- **TP 1RR**: 21626.02 ✅
- **TP 2RR**: 21662.84 ✅
- **TP 3RR**: 21699.65 ✅
- **TP 4RR**: 21736.46 ✅
- **TP 15RR**: 22141.41 ✅
- **PnL**: 552.20 points (15.0R)
- **MFE**: 561.10 points
- **MAE**: 14.95 points

### Trade #67 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 07:30:00
- **FVG 5m**: 21932.26 - 21946.44
- **Entrée**: 21962.16 @ 2025-01-15 08:43:00
- **Stop Loss**: 21633.55
- **Risk**: 328.62 points
- **TP 1RR**: 22290.78 ✅
- **TP 2RR**: 22619.40 ✅
- **TP 3RR**: 22948.02 ❌
- **TP 4RR**: 23276.63 ❌
- **TP 15RR**: 26891.43 ❌
- **PnL**: -328.62 points (-1.0R)
- **MFE**: 815.49 points
- **MAE**: 328.62 points

### Trade #68 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 07:30:00
- **FVG 5m**: 21932.26 - 21946.44
- **Entrée**: 21962.16 @ 2025-01-15 08:43:00
- **Stop Loss**: 21633.55
- **Risk**: 328.62 points
- **TP 1RR**: 22290.78 ✅
- **TP 2RR**: 22619.40 ✅
- **TP 3RR**: 22948.02 ❌
- **TP 4RR**: 23276.63 ❌
- **TP 15RR**: 26891.43 ❌
- **PnL**: -328.62 points (-1.0R)
- **MFE**: 815.49 points
- **MAE**: 328.62 points

### Trade #69 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 07:30:00
- **FVG 5m**: 21932.26 - 21946.44
- **Entrée**: 21962.16 @ 2025-01-15 08:43:00
- **Stop Loss**: 21633.55
- **Risk**: 328.62 points
- **TP 1RR**: 22290.78 ✅
- **TP 2RR**: 22619.40 ✅
- **TP 3RR**: 22948.02 ❌
- **TP 4RR**: 23276.63 ❌
- **TP 15RR**: 26891.43 ❌
- **PnL**: -328.62 points (-1.0R)
- **MFE**: 815.49 points
- **MAE**: 328.62 points

### Trade #70 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 08:45:00
- **FVG 5m**: 21976.60 - 21986.65
- **Entrée**: 21955.46 @ 2025-01-15 10:31:00
- **Stop Loss**: 22016.98
- **Risk**: 61.52 points
- **TP 1RR**: 21893.94 ❌
- **TP 2RR**: 21832.42 ❌
- **TP 3RR**: 21770.90 ❌
- **TP 4RR**: 21709.38 ❌
- **TP 15RR**: 21032.66 ❌
- **PnL**: -61.52 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 62.12 points

### Trade #71 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 09:00:00
- **FVG 5m**: 21976.60 - 21986.65
- **Entrée**: 21955.46 @ 2025-01-15 10:31:00
- **Stop Loss**: 22064.69
- **Risk**: 109.23 points
- **TP 1RR**: 21846.24 ❌
- **TP 2RR**: 21737.01 ❌
- **TP 3RR**: 21627.78 ❌
- **TP 4RR**: 21518.56 ❌
- **TP 15RR**: 20317.07 ❌
- **PnL**: -109.23 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 110.31 points

### Trade #72 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 09:30:00
- **FVG 5m**: 21976.60 - 21986.65
- **Entrée**: 21955.46 @ 2025-01-15 10:31:00
- **Stop Loss**: 22074.49
- **Risk**: 119.03 points
- **TP 1RR**: 21836.44 ❌
- **TP 2RR**: 21717.41 ❌
- **TP 3RR**: 21598.39 ❌
- **TP 4RR**: 21479.36 ❌
- **TP 15RR**: 20170.08 ❌
- **PnL**: -119.03 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 130.16 points

### Trade #73 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-15 09:45:00
- **FVG 5m**: 21976.60 - 21986.65
- **Entrée**: 21955.46 @ 2025-01-15 10:31:00
- **Stop Loss**: 22049.99
- **Risk**: 94.53 points
- **TP 1RR**: 21860.93 ❌
- **TP 2RR**: 21766.41 ❌
- **TP 3RR**: 21671.88 ❌
- **TP 4RR**: 21577.35 ❌
- **TP 15RR**: 20537.54 ❌
- **PnL**: -94.53 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 102.32 points

### Trade #74 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-15 23:30:00
- **FVG 5m**: 22038.20 - 22050.83
- **Entrée**: 22060.10 @ 2025-01-16 00:13:00
- **Stop Loss**: 22004.77
- **Risk**: 55.34 points
- **TP 1RR**: 22115.44 ✅
- **TP 2RR**: 22170.78 ✅
- **TP 3RR**: 22226.12 ✅
- **TP 4RR**: 22281.46 ❌
- **TP 15RR**: 22890.20 ❌
- **PnL**: -55.34 points (-1.0R)
- **MFE**: 175.01 points
- **MAE**: 57.73 points

### Trade #75 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 00:00:00
- **FVG 5m**: 22038.20 - 22050.83
- **Entrée**: 22060.10 @ 2025-01-16 00:13:00
- **Stop Loss**: 22003.22
- **Risk**: 56.89 points
- **TP 1RR**: 22116.99 ✅
- **TP 2RR**: 22173.87 ✅
- **TP 3RR**: 22230.76 ✅
- **TP 4RR**: 22287.64 ❌
- **TP 15RR**: 22913.38 ❌
- **PnL**: -56.89 points (-1.0R)
- **MFE**: 175.01 points
- **MAE**: 57.73 points

### Trade #76 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 02:00:00
- **FVG 5m**: 22189.23 - 22205.21
- **Entrée**: 22174.54 @ 2025-01-16 03:03:00
- **Stop Loss**: 22246.23
- **Risk**: 71.69 points
- **TP 1RR**: 22102.85 ✅
- **TP 2RR**: 22031.17 ✅
- **TP 3RR**: 21959.48 ✅
- **TP 4RR**: 21887.79 ✅
- **TP 15RR**: 21099.24 ❌
- **PnL**: -71.69 points (-1.0R)
- **MFE**: 346.66 points
- **MAE**: 77.32 points

### Trade #77 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 06:45:00
- **FVG 5m**: 22117.07 - 22153.15
- **Entrée**: 22114.75 @ 2025-01-16 08:31:00
- **Stop Loss**: 22151.85
- **Risk**: 37.10 points
- **TP 1RR**: 22077.64 ✅
- **TP 2RR**: 22040.54 ✅
- **TP 3RR**: 22003.44 ✅
- **TP 4RR**: 21966.34 ✅
- **TP 15RR**: 21558.21 ❌
- **PnL**: -37.10 points (-1.0R)
- **MFE**: 286.87 points
- **MAE**: 43.82 points

### Trade #78 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 06:45:00
- **FVG 5m**: 22117.07 - 22153.15
- **Entrée**: 22114.75 @ 2025-01-16 08:31:00
- **Stop Loss**: 22151.85
- **Risk**: 37.10 points
- **TP 1RR**: 22077.64 ✅
- **TP 2RR**: 22040.54 ✅
- **TP 3RR**: 22003.44 ✅
- **TP 4RR**: 21966.34 ✅
- **TP 15RR**: 21558.21 ❌
- **PnL**: -37.10 points (-1.0R)
- **MFE**: 286.87 points
- **MAE**: 43.82 points

### Trade #79 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-16 06:45:00
- **FVG 5m**: 22117.07 - 22153.15
- **Entrée**: 22114.75 @ 2025-01-16 08:31:00
- **Stop Loss**: 22151.85
- **Risk**: 37.10 points
- **TP 1RR**: 22077.64 ✅
- **TP 2RR**: 22040.54 ✅
- **TP 3RR**: 22003.44 ✅
- **TP 4RR**: 21966.34 ✅
- **TP 15RR**: 21558.21 ❌
- **PnL**: -37.10 points (-1.0R)
- **MFE**: 286.87 points
- **MAE**: 43.82 points

### Trade #80 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 07:15:00
- **FVG 5m**: 22135.11 - 22137.43
- **Entrée**: 22143.36 @ 2025-01-16 08:13:00
- **Stop Loss**: 22075.87
- **Risk**: 67.49 points
- **TP 1RR**: 22210.84 ❌
- **TP 2RR**: 22278.33 ❌
- **TP 3RR**: 22345.82 ❌
- **TP 4RR**: 22413.31 ❌
- **TP 15RR**: 23155.69 ❌
- **PnL**: -67.49 points (-1.0R)
- **MFE**: 22.68 points
- **MAE**: 74.75 points

### Trade #81 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 09:00:00
- **FVG 5m**: 22053.15 - 22079.18
- **Entrée**: 22088.20 @ 2025-01-16 09:59:00
- **Stop Loss**: 21985.96
- **Risk**: 102.24 points
- **TP 1RR**: 22190.44 ❌
- **TP 2RR**: 22292.68 ❌
- **TP 3RR**: 22394.92 ❌
- **TP 4RR**: 22497.15 ❌
- **TP 15RR**: 23621.78 ❌
- **PnL**: -102.24 points (-1.0R)
- **MFE**: 51.55 points
- **MAE**: 109.02 points

### Trade #82 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 09:45:00
- **FVG 5m**: 22053.15 - 22079.18
- **Entrée**: 22088.20 @ 2025-01-16 09:59:00
- **Stop Loss**: 21989.31
- **Risk**: 98.89 points
- **TP 1RR**: 22187.09 ❌
- **TP 2RR**: 22285.98 ❌
- **TP 3RR**: 22384.87 ❌
- **TP 4RR**: 22483.76 ❌
- **TP 15RR**: 23571.55 ❌
- **PnL**: -98.89 points (-1.0R)
- **MFE**: 51.55 points
- **MAE**: 109.02 points

### Trade #83 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 10:30:00
- **FVG 5m**: 22041.03 - 22052.11
- **Entrée**: 22062.42 @ 2025-01-16 10:58:00
- **Stop Loss**: 21966.64
- **Risk**: 95.79 points
- **TP 1RR**: 22158.21 ❌
- **TP 2RR**: 22254.00 ❌
- **TP 3RR**: 22349.78 ❌
- **TP 4RR**: 22445.57 ❌
- **TP 15RR**: 23499.21 ❌
- **PnL**: -95.79 points (-1.0R)
- **MFE**: 27.06 points
- **MAE**: 96.65 points

### Trade #84 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 13:00:00
- **FVG 5m**: 22022.73 - 22030.46
- **Entrée**: 22030.98 @ 2025-01-16 13:56:00
- **Stop Loss**: 21925.16
- **Risk**: 105.82 points
- **TP 1RR**: 22136.80 ❌
- **TP 2RR**: 22242.61 ❌
- **TP 3RR**: 22348.43 ❌
- **TP 4RR**: 22454.25 ❌
- **TP 15RR**: 23618.23 ❌
- **PnL**: -105.82 points (-1.0R)
- **MFE**: 27.32 points
- **MAE**: 109.02 points

### Trade #85 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-16 19:30:00
- **FVG 5m**: 21915.00 - 21922.47
- **Entrée**: 21923.50 @ 2025-01-16 19:43:00
- **Stop Loss**: 21894.25
- **Risk**: 29.25 points
- **TP 1RR**: 21952.75 ✅
- **TP 2RR**: 21982.01 ✅
- **TP 3RR**: 22011.26 ✅
- **TP 4RR**: 22040.51 ✅
- **TP 15RR**: 22362.29 ✅
- **PnL**: 438.78 points (15.0R)
- **MFE**: 439.96 points
- **MAE**: 19.07 points

### Trade #86 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-17 08:30:00
- **FVG 5m**: 22199.03 - 22217.33
- **Entrée**: 22192.84 @ 2025-01-17 09:21:00
- **Stop Loss**: 22335.45
- **Risk**: 142.61 points
- **TP 1RR**: 22050.23 ❌
- **TP 2RR**: 21907.62 ❌
- **TP 3RR**: 21765.01 ❌
- **TP 4RR**: 21622.40 ❌
- **TP 15RR**: 20053.69 ❌
- **PnL**: -142.61 points (-1.0R)
- **MFE**: 46.39 points
- **MAE**: 142.79 points

### Trade #87 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-17 08:30:00
- **FVG 5m**: 22199.03 - 22217.33
- **Entrée**: 22192.84 @ 2025-01-17 09:21:00
- **Stop Loss**: 22335.45
- **Risk**: 142.61 points
- **TP 1RR**: 22050.23 ❌
- **TP 2RR**: 21907.62 ❌
- **TP 3RR**: 21765.01 ❌
- **TP 4RR**: 21622.40 ❌
- **TP 15RR**: 20053.69 ❌
- **PnL**: -142.61 points (-1.0R)
- **MFE**: 46.39 points
- **MAE**: 142.79 points

### Trade #88 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-17 12:00:00
- **FVG 5m**: 22317.85 - 22324.55
- **Entrée**: 22326.87 @ 2025-01-17 12:12:00
- **Stop Loss**: 22272.42
- **Risk**: 54.44 points
- **TP 1RR**: 22381.31 ❌
- **TP 2RR**: 22435.75 ❌
- **TP 3RR**: 22490.19 ❌
- **TP 4RR**: 22544.64 ❌
- **TP 15RR**: 23143.50 ❌
- **PnL**: -54.44 points (-1.0R)
- **MFE**: 16.24 points
- **MAE**: 63.66 points

### Trade #89 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 07:30:00
- **FVG 5m**: 22325.06 - 22338.98
- **Entrée**: 22344.65 @ 2025-01-20 07:53:00
- **Stop Loss**: 22193.85
- **Risk**: 150.80 points
- **TP 1RR**: 22495.45 ❌
- **TP 2RR**: 22646.25 ❌
- **TP 3RR**: 22797.05 ❌
- **TP 4RR**: 22947.84 ❌
- **TP 15RR**: 24606.63 ❌
- **PnL**: -150.80 points (-1.0R)
- **MFE**: 108.51 points
- **MAE**: 176.55 points

### Trade #90 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 07:45:00
- **FVG 5m**: 22348.00 - 22356.51
- **Entrée**: 22362.69 @ 2025-01-20 07:58:00
- **Stop Loss**: 22294.58
- **Risk**: 68.11 points
- **TP 1RR**: 22430.81 ✅
- **TP 2RR**: 22498.92 ❌
- **TP 3RR**: 22567.03 ❌
- **TP 4RR**: 22635.15 ❌
- **TP 15RR**: 23384.40 ❌
- **PnL**: -68.11 points (-1.0R)
- **MFE**: 90.47 points
- **MAE**: 73.20 points

### Trade #91 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 08:00:00
- **FVG 5m**: 22345.94 - 22351.35
- **Entrée**: 22333.57 @ 2025-01-20 08:14:00
- **Stop Loss**: 22387.03
- **Risk**: 53.46 points
- **TP 1RR**: 22280.11 ❌
- **TP 2RR**: 22226.65 ❌
- **TP 3RR**: 22173.20 ❌
- **TP 4RR**: 22119.74 ❌
- **TP 15RR**: 21531.71 ❌
- **PnL**: -53.46 points (-1.0R)
- **MFE**: 3.61 points
- **MAE**: 53.61 points

### Trade #92 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 08:00:00
- **FVG 5m**: 22345.94 - 22351.35
- **Entrée**: 22333.57 @ 2025-01-20 08:14:00
- **Stop Loss**: 22387.03
- **Risk**: 53.46 points
- **TP 1RR**: 22280.11 ❌
- **TP 2RR**: 22226.65 ❌
- **TP 3RR**: 22173.20 ❌
- **TP 4RR**: 22119.74 ❌
- **TP 15RR**: 21531.71 ❌
- **PnL**: -53.46 points (-1.0R)
- **MFE**: 3.61 points
- **MAE**: 53.61 points

### Trade #93 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 11:15:00
- **FVG 5m**: 22391.56 - 22399.29
- **Entrée**: 22407.54 @ 2025-01-20 17:16:00
- **Stop Loss**: 22278.35
- **Risk**: 129.19 points
- **TP 1RR**: 22536.73 ❌
- **TP 2RR**: 22665.92 ❌
- **TP 3RR**: 22795.11 ❌
- **TP 4RR**: 22924.30 ❌
- **TP 15RR**: 24345.40 ❌
- **PnL**: -129.19 points (-1.0R)
- **MFE**: 12.11 points
- **MAE**: 153.61 points

### Trade #94 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-20 18:15:00
- **FVG 5m**: 22369.14 - 22382.28
- **Entrée**: 22368.88 @ 2025-01-20 18:38:00
- **Stop Loss**: 22430.86
- **Risk**: 61.98 points
- **TP 1RR**: 22306.89 ✅
- **TP 2RR**: 22244.91 ✅
- **TP 3RR**: 22182.92 ✅
- **TP 4RR**: 22120.94 ✅
- **TP 15RR**: 21439.11 ❌
- **PnL**: -61.98 points (-1.0R)
- **MFE**: 329.14 points
- **MAE**: 63.15 points

### Trade #95 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 19:00:00
- **FVG 5m**: 22274.29 - 22290.53
- **Entrée**: 22293.88 @ 2025-01-20 21:12:00
- **Stop Loss**: 22028.72
- **Risk**: 265.15 points
- **TP 1RR**: 22559.03 ✅
- **TP 2RR**: 22824.18 ❌
- **TP 3RR**: 23089.34 ❌
- **TP 4RR**: 23354.49 ❌
- **TP 15RR**: 26271.17 ❌
- **PnL**: -265.15 points (-1.0R)
- **MFE**: 483.78 points
- **MAE**: 267.28 points

### Trade #96 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 19:00:00
- **FVG 5m**: 22274.29 - 22290.53
- **Entrée**: 22293.88 @ 2025-01-20 21:12:00
- **Stop Loss**: 22028.72
- **Risk**: 265.15 points
- **TP 1RR**: 22559.03 ✅
- **TP 2RR**: 22824.18 ❌
- **TP 3RR**: 23089.34 ❌
- **TP 4RR**: 23354.49 ❌
- **TP 15RR**: 26271.17 ❌
- **PnL**: -265.15 points (-1.0R)
- **MFE**: 483.78 points
- **MAE**: 267.28 points

### Trade #97 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 19:00:00
- **FVG 5m**: 22274.29 - 22290.53
- **Entrée**: 22293.88 @ 2025-01-20 21:12:00
- **Stop Loss**: 22028.72
- **Risk**: 265.15 points
- **TP 1RR**: 22559.03 ✅
- **TP 2RR**: 22824.18 ❌
- **TP 3RR**: 23089.34 ❌
- **TP 4RR**: 23354.49 ❌
- **TP 15RR**: 26271.17 ❌
- **PnL**: -265.15 points (-1.0R)
- **MFE**: 483.78 points
- **MAE**: 267.28 points

### Trade #98 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 19:00:00
- **FVG 5m**: 22274.29 - 22290.53
- **Entrée**: 22293.88 @ 2025-01-20 21:12:00
- **Stop Loss**: 22028.72
- **Risk**: 265.15 points
- **TP 1RR**: 22559.03 ✅
- **TP 2RR**: 22824.18 ❌
- **TP 3RR**: 23089.34 ❌
- **TP 4RR**: 23354.49 ❌
- **TP 15RR**: 26271.17 ❌
- **PnL**: -265.15 points (-1.0R)
- **MFE**: 483.78 points
- **MAE**: 267.28 points

### Trade #99 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-20 22:00:00
- **FVG 5m**: 22266.81 - 22269.91
- **Entrée**: 22271.19 @ 2025-01-21 00:08:00
- **Stop Loss**: 22266.76
- **Risk**: 4.44 points
- **TP 1RR**: 22275.63 ✅
- **TP 2RR**: 22280.07 ✅
- **TP 3RR**: 22284.51 ✅
- **TP 4RR**: 22288.95 ✅
- **TP 15RR**: 22337.76 ❌
- **PnL**: -4.44 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 4.90 points

### Trade #100 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-21 09:15:00
- **FVG 5m**: 22304.19 - 22307.28
- **Entrée**: 22309.34 @ 2025-01-21 10:06:00
- **Stop Loss**: 22181.23
- **Risk**: 128.11 points
- **TP 1RR**: 22437.45 ✅
- **TP 2RR**: 22565.56 ✅
- **TP 3RR**: 22693.67 ✅
- **TP 4RR**: 22821.78 ❌
- **TP 15RR**: 24231.00 ❌
- **PnL**: -128.11 points (-1.0R)
- **MFE**: 468.32 points
- **MAE**: 131.45 points

### Trade #101 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-21 09:15:00
- **FVG 5m**: 22304.19 - 22307.28
- **Entrée**: 22309.34 @ 2025-01-21 10:06:00
- **Stop Loss**: 22181.23
- **Risk**: 128.11 points
- **TP 1RR**: 22437.45 ✅
- **TP 2RR**: 22565.56 ✅
- **TP 3RR**: 22693.67 ✅
- **TP 4RR**: 22821.78 ❌
- **TP 15RR**: 24231.00 ❌
- **PnL**: -128.11 points (-1.0R)
- **MFE**: 468.32 points
- **MAE**: 131.45 points

### Trade #102 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-21 10:00:00
- **FVG 5m**: 22299.03 - 22303.67
- **Entrée**: 22307.28 @ 2025-01-21 10:49:00
- **Stop Loss**: 22250.53
- **Risk**: 56.75 points
- **TP 1RR**: 22364.03 ✅
- **TP 2RR**: 22420.78 ✅
- **TP 3RR**: 22477.53 ✅
- **TP 4RR**: 22534.28 ✅
- **TP 15RR**: 23158.55 ❌
- **PnL**: -56.75 points (-1.0R)
- **MFE**: 470.38 points
- **MAE**: 60.83 points

### Trade #103 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-21 13:00:00
- **FVG 5m**: 22419.91 - 22425.07
- **Entrée**: 22418.88 @ 2025-01-21 13:14:00
- **Stop Loss**: 22448.66
- **Risk**: 29.78 points
- **TP 1RR**: 22389.10 ✅
- **TP 2RR**: 22359.33 ❌
- **TP 3RR**: 22329.55 ❌
- **TP 4RR**: 22299.78 ❌
- **TP 15RR**: 21972.24 ❌
- **PnL**: -29.78 points (-1.0R)
- **MFE**: 50.00 points
- **MAE**: 30.41 points

### Trade #104 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-21 17:00:00
- **FVG 5m**: 22502.13 - 22510.64
- **Entrée**: 22501.62 @ 2025-01-21 19:01:00
- **Stop Loss**: 22507.19
- **Risk**: 5.58 points
- **TP 1RR**: 22496.04 ✅
- **TP 2RR**: 22490.46 ✅
- **TP 3RR**: 22484.88 ❌
- **TP 4RR**: 22479.31 ❌
- **TP 15RR**: 22417.95 ❌
- **PnL**: -5.58 points (-1.0R)
- **MFE**: 14.69 points
- **MAE**: 6.44 points

### Trade #105 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-22 00:45:00
- **FVG 5m**: 22534.86 - 22537.44
- **Entrée**: 22534.35 @ 2025-01-22 01:47:00
- **Stop Loss**: 22544.33
- **Risk**: 9.98 points
- **TP 1RR**: 22524.37 ✅
- **TP 2RR**: 22514.39 ❌
- **TP 3RR**: 22504.42 ❌
- **TP 4RR**: 22494.44 ❌
- **TP 15RR**: 22384.68 ❌
- **PnL**: -9.98 points (-1.0R)
- **MFE**: 11.60 points
- **MAE**: 10.57 points

### Trade #106 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 02:00:00
- **FVG 5m**: 22575.07 - 22583.32
- **Entrée**: 22574.56 @ 2025-01-23 02:31:00
- **Stop Loss**: 22616.27
- **Risk**: 41.72 points
- **TP 1RR**: 22532.84 ✅
- **TP 2RR**: 22491.12 ❌
- **TP 3RR**: 22449.41 ❌
- **TP 4RR**: 22407.69 ❌
- **TP 15RR**: 21948.82 ❌
- **PnL**: -41.72 points (-1.0R)
- **MFE**: 42.27 points
- **MAE**: 43.04 points

### Trade #107 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 02:45:00
- **FVG 5m**: 22546.72 - 22549.81
- **Entrée**: 22558.06 @ 2025-01-23 03:22:00
- **Stop Loss**: 22528.75
- **Risk**: 29.31 points
- **TP 1RR**: 22587.37 ✅
- **TP 2RR**: 22616.69 ✅
- **TP 3RR**: 22646.00 ✅
- **TP 4RR**: 22675.31 ✅
- **TP 15RR**: 22997.74 ❌
- **PnL**: -29.31 points (-1.0R)
- **MFE**: 203.87 points
- **MAE**: 31.96 points

### Trade #108 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 03:15:00
- **FVG 5m**: 22565.28 - 22569.66
- **Entrée**: 22571.72 @ 2025-01-23 05:42:00
- **Stop Loss**: 22521.02
- **Risk**: 50.70 points
- **TP 1RR**: 22622.42 ✅
- **TP 2RR**: 22673.12 ✅
- **TP 3RR**: 22723.82 ✅
- **TP 4RR**: 22774.52 ❌
- **TP 15RR**: 23332.23 ❌
- **PnL**: -50.70 points (-1.0R)
- **MFE**: 190.21 points
- **MAE**: 51.29 points

### Trade #109 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 07:00:00
- **FVG 5m**: 22569.40 - 22572.24
- **Entrée**: 22568.11 @ 2025-01-23 08:07:00
- **Stop Loss**: 22598.74
- **Risk**: 30.62 points
- **TP 1RR**: 22537.49 ❌
- **TP 2RR**: 22506.86 ❌
- **TP 3RR**: 22476.24 ❌
- **TP 4RR**: 22445.62 ❌
- **TP 15RR**: 22108.75 ❌
- **PnL**: -30.62 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 34.80 points

### Trade #110 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 07:30:00
- **FVG 5m**: 22569.40 - 22572.24
- **Entrée**: 22568.11 @ 2025-01-23 08:07:00
- **Stop Loss**: 22609.57
- **Risk**: 41.45 points
- **TP 1RR**: 22526.66 ❌
- **TP 2RR**: 22485.20 ❌
- **TP 3RR**: 22443.75 ❌
- **TP 4RR**: 22402.29 ❌
- **TP 15RR**: 21946.29 ❌
- **PnL**: -41.45 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 44.59 points

### Trade #111 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-23 10:00:00
- **FVG 5m**: 22614.25 - 22623.53
- **Entrée**: 22628.42 @ 2025-01-23 10:29:00
- **Stop Loss**: 22563.53
- **Risk**: 64.90 points
- **TP 1RR**: 22693.32 ✅
- **TP 2RR**: 22758.22 ✅
- **TP 3RR**: 22823.12 ❌
- **TP 4RR**: 22888.02 ❌
- **TP 15RR**: 23601.89 ❌
- **PnL**: -64.90 points (-1.0R)
- **MFE**: 133.51 points
- **MAE**: 81.19 points

### Trade #112 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 12:30:00
- **FVG 5m**: 22615.80 - 22625.07
- **Entrée**: 22615.28 @ 2025-01-23 13:07:00
- **Stop Loss**: 22677.13
- **Risk**: 61.85 points
- **TP 1RR**: 22553.43 ❌
- **TP 2RR**: 22491.58 ❌
- **TP 3RR**: 22429.73 ❌
- **TP 4RR**: 22367.88 ❌
- **TP 15RR**: 21687.53 ❌
- **PnL**: -61.85 points (-1.0R)
- **MFE**: 12.63 points
- **MAE**: 67.01 points

### Trade #113 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 12:30:00
- **FVG 5m**: 22615.80 - 22625.07
- **Entrée**: 22615.28 @ 2025-01-23 13:07:00
- **Stop Loss**: 22677.13
- **Risk**: 61.85 points
- **TP 1RR**: 22553.43 ❌
- **TP 2RR**: 22491.58 ❌
- **TP 3RR**: 22429.73 ❌
- **TP 4RR**: 22367.88 ❌
- **TP 15RR**: 21687.53 ❌
- **PnL**: -61.85 points (-1.0R)
- **MFE**: 12.63 points
- **MAE**: 67.01 points

### Trade #114 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 12:30:00
- **FVG 5m**: 22615.80 - 22625.07
- **Entrée**: 22615.28 @ 2025-01-23 13:07:00
- **Stop Loss**: 22677.13
- **Risk**: 61.85 points
- **TP 1RR**: 22553.43 ❌
- **TP 2RR**: 22491.58 ❌
- **TP 3RR**: 22429.73 ❌
- **TP 4RR**: 22367.88 ❌
- **TP 15RR**: 21687.53 ❌
- **PnL**: -61.85 points (-1.0R)
- **MFE**: 12.63 points
- **MAE**: 67.01 points

### Trade #115 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-23 22:15:00
- **FVG 5m**: 22686.16 - 22688.99
- **Entrée**: 22683.84 @ 2025-01-23 23:54:00
- **Stop Loss**: 22700.08
- **Risk**: 16.24 points
- **TP 1RR**: 22667.60 ✅
- **TP 2RR**: 22651.36 ❌
- **TP 3RR**: 22635.11 ❌
- **TP 4RR**: 22618.87 ❌
- **TP 15RR**: 22440.22 ❌
- **PnL**: -16.24 points (-1.0R)
- **MFE**: 31.70 points
- **MAE**: 16.50 points

### Trade #116 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 02:00:00
- **FVG 5m**: 22668.12 - 22676.11
- **Entrée**: 22676.36 @ 2025-01-24 03:02:00
- **Stop Loss**: 22648.28
- **Risk**: 28.08 points
- **TP 1RR**: 22704.45 ✅
- **TP 2RR**: 22732.53 ✅
- **TP 3RR**: 22760.61 ✅
- **TP 4RR**: 22788.70 ❌
- **TP 15RR**: 23097.61 ❌
- **PnL**: -28.08 points (-1.0R)
- **MFE**: 85.57 points
- **MAE**: 43.56 points

### Trade #117 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 09:00:00
- **FVG 5m**: 22704.72 - 22707.29
- **Entrée**: 22702.91 @ 2025-01-24 10:54:00
- **Stop Loss**: 22765.06
- **Risk**: 62.15 points
- **TP 1RR**: 22640.76 ✅
- **TP 2RR**: 22578.61 ✅
- **TP 3RR**: 22516.46 ✅
- **TP 4RR**: 22454.30 ✅
- **TP 15RR**: 21770.63 ✅
- **PnL**: 932.28 points (15.0R)
- **MFE**: 940.76 points
- **MAE**: 1.80 points

### Trade #118 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 09:00:00
- **FVG 5m**: 22704.72 - 22707.29
- **Entrée**: 22702.91 @ 2025-01-24 10:54:00
- **Stop Loss**: 22765.06
- **Risk**: 62.15 points
- **TP 1RR**: 22640.76 ✅
- **TP 2RR**: 22578.61 ✅
- **TP 3RR**: 22516.46 ✅
- **TP 4RR**: 22454.30 ✅
- **TP 15RR**: 21770.63 ✅
- **PnL**: 932.28 points (15.0R)
- **MFE**: 940.76 points
- **MAE**: 1.80 points

### Trade #119 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 09:00:00
- **FVG 5m**: 22704.72 - 22707.29
- **Entrée**: 22702.91 @ 2025-01-24 10:54:00
- **Stop Loss**: 22765.06
- **Risk**: 62.15 points
- **TP 1RR**: 22640.76 ✅
- **TP 2RR**: 22578.61 ✅
- **TP 3RR**: 22516.46 ✅
- **TP 4RR**: 22454.30 ✅
- **TP 15RR**: 21770.63 ✅
- **PnL**: 932.28 points (15.0R)
- **MFE**: 940.76 points
- **MAE**: 1.80 points

### Trade #120 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 10:00:00
- **FVG 5m**: 22679.46 - 22683.58
- **Entrée**: 22684.10 @ 2025-01-24 10:24:00
- **Stop Loss**: 22639.27
- **Risk**: 44.83 points
- **TP 1RR**: 22728.93 ❌
- **TP 2RR**: 22773.76 ❌
- **TP 3RR**: 22818.59 ❌
- **TP 4RR**: 22863.42 ❌
- **TP 15RR**: 23356.57 ❌
- **PnL**: -44.83 points (-1.0R)
- **MFE**: 34.02 points
- **MAE**: 51.29 points

### Trade #121 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 10:45:00
- **FVG 5m**: 22674.30 - 22702.65
- **Entrée**: 22667.34 @ 2025-01-24 10:58:00
- **Stop Loss**: 22729.48
- **Risk**: 62.13 points
- **TP 1RR**: 22605.21 ✅
- **TP 2RR**: 22543.08 ✅
- **TP 3RR**: 22480.94 ✅
- **TP 4RR**: 22418.81 ✅
- **TP 15RR**: 21735.33 ✅
- **PnL**: 932.01 points (15.0R)
- **MFE**: 942.82 points
- **MAE**: 22.42 points

### Trade #122 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-24 12:30:00
- **FVG 5m**: 22568.11 - 22573.27
- **Entrée**: 22550.07 @ 2025-01-24 12:56:00
- **Stop Loss**: 22638.71
- **Risk**: 88.64 points
- **TP 1RR**: 22461.44 ✅
- **TP 2RR**: 22372.80 ✅
- **TP 3RR**: 22284.16 ✅
- **TP 4RR**: 22195.53 ✅
- **TP 15RR**: 21220.53 ❌
- **PnL**: -88.64 points (-1.0R)
- **MFE**: 1143.34 points
- **MAE**: 92.53 points

### Trade #123 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 13:00:00
- **FVG 5m**: 22558.83 - 22567.86
- **Entrée**: 22571.21 @ 2025-01-24 14:52:00
- **Stop Loss**: 22509.17
- **Risk**: 62.04 points
- **TP 1RR**: 22633.24 ❌
- **TP 2RR**: 22695.28 ❌
- **TP 3RR**: 22757.31 ❌
- **TP 4RR**: 22819.35 ❌
- **TP 15RR**: 23501.74 ❌
- **PnL**: -62.04 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 209.29 points

### Trade #124 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 13:15:00
- **FVG 5m**: 22558.83 - 22567.86
- **Entrée**: 22571.21 @ 2025-01-24 14:52:00
- **Stop Loss**: 22512.78
- **Risk**: 58.43 points
- **TP 1RR**: 22629.63 ❌
- **TP 2RR**: 22688.06 ❌
- **TP 3RR**: 22746.49 ❌
- **TP 4RR**: 22804.92 ❌
- **TP 15RR**: 23447.64 ❌
- **PnL**: -58.43 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 209.29 points

### Trade #125 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-24 14:00:00
- **FVG 5m**: 22558.83 - 22567.86
- **Entrée**: 22571.21 @ 2025-01-24 14:52:00
- **Stop Loss**: 22526.17
- **Risk**: 45.03 points
- **TP 1RR**: 22616.24 ❌
- **TP 2RR**: 22661.27 ❌
- **TP 3RR**: 22706.30 ❌
- **TP 4RR**: 22751.34 ❌
- **TP 15RR**: 23246.70 ❌
- **PnL**: -45.03 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 209.29 points

### Trade #126 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-26 19:30:00
- **FVG 5m**: 22181.50 - 22188.72
- **Entrée**: 22189.23 @ 2025-01-26 20:23:00
- **Stop Loss**: 22166.80
- **Risk**: 22.43 points
- **TP 1RR**: 22211.66 ✅
- **TP 2RR**: 22234.09 ❌
- **TP 3RR**: 22256.52 ❌
- **TP 4RR**: 22278.95 ❌
- **TP 15RR**: 22525.68 ❌
- **PnL**: -22.43 points (-1.0R)
- **MFE**: 41.50 points
- **MAE**: 29.64 points

### Trade #127 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 00:30:00
- **FVG 5m**: 22047.99 - 22050.31
- **Entrée**: 22046.70 @ 2025-01-27 01:06:00
- **Stop Loss**: 22090.73
- **Risk**: 44.03 points
- **TP 1RR**: 22002.67 ✅
- **TP 2RR**: 21958.64 ✅
- **TP 3RR**: 21914.61 ✅
- **TP 4RR**: 21870.58 ✅
- **TP 15RR**: 21386.24 ❌
- **PnL**: -44.03 points (-1.0R)
- **MFE**: 639.97 points
- **MAE**: 53.35 points

### Trade #128 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 01:45:00
- **FVG 5m**: 21969.64 - 21991.55
- **Entrée**: 21962.68 @ 2025-01-27 01:56:00
- **Stop Loss**: 22028.59
- **Risk**: 65.91 points
- **TP 1RR**: 21896.77 ✅
- **TP 2RR**: 21830.86 ✅
- **TP 3RR**: 21764.95 ✅
- **TP 4RR**: 21699.05 ✅
- **TP 15RR**: 20974.06 ❌
- **PnL**: -65.91 points (-1.0R)
- **MFE**: 555.95 points
- **MAE**: 69.33 points

### Trade #129 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 02:00:00
- **FVG 5m**: 21919.38 - 21926.85
- **Entrée**: 21909.84 @ 2025-01-27 02:12:00
- **Stop Loss**: 21983.46
- **Risk**: 73.62 points
- **TP 1RR**: 21836.22 ✅
- **TP 2RR**: 21762.61 ✅
- **TP 3RR**: 21688.99 ✅
- **TP 4RR**: 21615.37 ✅
- **TP 15RR**: 20805.58 ❌
- **PnL**: -73.62 points (-1.0R)
- **MFE**: 503.11 points
- **MAE**: 75.78 points

### Trade #130 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 03:45:00
- **FVG 5m**: 21804.42 - 21810.10
- **Entrée**: 21791.28 @ 2025-01-27 04:02:00
- **Stop Loss**: 21881.34
- **Risk**: 90.06 points
- **TP 1RR**: 21701.22 ✅
- **TP 2RR**: 21611.16 ✅
- **TP 3RR**: 21521.09 ✅
- **TP 4RR**: 21431.03 ✅
- **TP 15RR**: 20440.35 ❌
- **PnL**: -90.06 points (-1.0R)
- **MFE**: 384.55 points
- **MAE**: 122.94 points

### Trade #131 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:00:00
- **FVG 5m**: 21744.89 - 21765.76
- **Entrée**: 21741.54 @ 2025-01-27 04:16:00
- **Stop Loss**: 21836.47
- **Risk**: 94.94 points
- **TP 1RR**: 21646.60 ✅
- **TP 2RR**: 21551.66 ✅
- **TP 3RR**: 21456.73 ✅
- **TP 4RR**: 21361.79 ❌
- **TP 15RR**: 20317.49 ❌
- **PnL**: -94.94 points (-1.0R)
- **MFE**: 334.81 points
- **MAE**: 172.69 points

### Trade #132 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:00:00
- **FVG 5m**: 21744.89 - 21765.76
- **Entrée**: 21741.54 @ 2025-01-27 04:16:00
- **Stop Loss**: 21836.47
- **Risk**: 94.94 points
- **TP 1RR**: 21646.60 ✅
- **TP 2RR**: 21551.66 ✅
- **TP 3RR**: 21456.73 ✅
- **TP 4RR**: 21361.79 ❌
- **TP 15RR**: 20317.49 ❌
- **PnL**: -94.94 points (-1.0R)
- **MFE**: 334.81 points
- **MAE**: 172.69 points

### Trade #133 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:30:00
- **FVG 5m**: 21610.60 - 21642.05
- **Entrée**: 21594.11 @ 2025-01-27 04:44:00
- **Stop Loss**: 21726.36
- **Risk**: 132.25 points
- **TP 1RR**: 21461.85 ✅
- **TP 2RR**: 21329.60 ❌
- **TP 3RR**: 21197.35 ❌
- **TP 4RR**: 21065.09 ❌
- **TP 15RR**: 19610.30 ❌
- **PnL**: -132.25 points (-1.0R)
- **MFE**: 187.38 points
- **MAE**: 140.21 points

### Trade #134 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:30:00
- **FVG 5m**: 21610.60 - 21642.05
- **Entrée**: 21594.11 @ 2025-01-27 04:44:00
- **Stop Loss**: 21726.36
- **Risk**: 132.25 points
- **TP 1RR**: 21461.85 ✅
- **TP 2RR**: 21329.60 ❌
- **TP 3RR**: 21197.35 ❌
- **TP 4RR**: 21065.09 ❌
- **TP 15RR**: 19610.30 ❌
- **PnL**: -132.25 points (-1.0R)
- **MFE**: 187.38 points
- **MAE**: 140.21 points

### Trade #135 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 04:30:00
- **FVG 5m**: 21610.60 - 21642.05
- **Entrée**: 21594.11 @ 2025-01-27 04:44:00
- **Stop Loss**: 21726.36
- **Risk**: 132.25 points
- **TP 1RR**: 21461.85 ✅
- **TP 2RR**: 21329.60 ❌
- **TP 3RR**: 21197.35 ❌
- **TP 4RR**: 21065.09 ❌
- **TP 15RR**: 19610.30 ❌
- **PnL**: -132.25 points (-1.0R)
- **MFE**: 187.38 points
- **MAE**: 140.21 points

### Trade #136 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 04:45:00
- **FVG 5m**: 21616.27 - 21635.09
- **Entrée**: 21643.08 @ 2025-01-27 05:34:00
- **Stop Loss**: 21396.03
- **Risk**: 247.05 points
- **TP 1RR**: 21890.13 ✅
- **TP 2RR**: 22137.18 ✅
- **TP 3RR**: 22384.24 ✅
- **TP 4RR**: 22631.29 ✅
- **TP 15RR**: 25348.86 ❌
- **PnL**: -247.05 points (-1.0R)
- **MFE**: 1367.83 points
- **MAE**: 250.52 points

### Trade #137 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 05:00:00
- **FVG 5m**: 21616.27 - 21635.09
- **Entrée**: 21643.08 @ 2025-01-27 05:34:00
- **Stop Loss**: 21513.76
- **Risk**: 129.32 points
- **TP 1RR**: 21772.40 ✅
- **TP 2RR**: 21901.73 ✅
- **TP 3RR**: 22031.05 ✅
- **TP 4RR**: 22160.37 ✅
- **TP 15RR**: 23582.93 ❌
- **PnL**: -129.32 points (-1.0R)
- **MFE**: 1367.83 points
- **MAE**: 156.45 points

### Trade #138 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 08:30:00
- **FVG 5m**: 21979.17 - 22011.13
- **Entrée**: 22011.39 @ 2025-01-27 09:28:00
- **Stop Loss**: 21751.79
- **Risk**: 259.60 points
- **TP 1RR**: 22270.99 ❌
- **TP 2RR**: 22530.60 ❌
- **TP 3RR**: 22790.20 ❌
- **TP 4RR**: 23049.80 ❌
- **TP 15RR**: 25905.42 ❌
- **PnL**: -259.60 points (-1.0R)
- **MFE**: 70.36 points
- **MAE**: 263.15 points

### Trade #139 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 08:30:00
- **FVG 5m**: 21979.17 - 22011.13
- **Entrée**: 22011.39 @ 2025-01-27 09:28:00
- **Stop Loss**: 21751.79
- **Risk**: 259.60 points
- **TP 1RR**: 22270.99 ❌
- **TP 2RR**: 22530.60 ❌
- **TP 3RR**: 22790.20 ❌
- **TP 4RR**: 23049.80 ❌
- **TP 15RR**: 25905.42 ❌
- **PnL**: -259.60 points (-1.0R)
- **MFE**: 70.36 points
- **MAE**: 263.15 points

### Trade #140 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 08:45:00
- **FVG 5m**: 21979.17 - 22011.13
- **Entrée**: 22011.39 @ 2025-01-27 09:28:00
- **Stop Loss**: 21907.13
- **Risk**: 104.26 points
- **TP 1RR**: 22115.65 ❌
- **TP 2RR**: 22219.91 ❌
- **TP 3RR**: 22324.18 ❌
- **TP 4RR**: 22428.44 ❌
- **TP 15RR**: 23575.31 ❌
- **PnL**: -104.26 points (-1.0R)
- **MFE**: 70.36 points
- **MAE**: 106.19 points

### Trade #141 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 09:45:00
- **FVG 5m**: 21986.65 - 21993.35
- **Entrée**: 21978.92 @ 2025-01-27 09:57:00
- **Stop Loss**: 22075.00
- **Risk**: 96.09 points
- **TP 1RR**: 21882.83 ✅
- **TP 2RR**: 21786.74 ✅
- **TP 3RR**: 21690.66 ❌
- **TP 4RR**: 21594.57 ❌
- **TP 15RR**: 20537.62 ❌
- **PnL**: -96.09 points (-1.0R)
- **MFE**: 230.68 points
- **MAE**: 101.55 points

### Trade #142 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 09:45:00
- **FVG 5m**: 21986.65 - 21993.35
- **Entrée**: 21978.92 @ 2025-01-27 09:57:00
- **Stop Loss**: 22075.00
- **Risk**: 96.09 points
- **TP 1RR**: 21882.83 ✅
- **TP 2RR**: 21786.74 ✅
- **TP 3RR**: 21690.66 ❌
- **TP 4RR**: 21594.57 ❌
- **TP 15RR**: 20537.62 ❌
- **PnL**: -96.09 points (-1.0R)
- **MFE**: 230.68 points
- **MAE**: 101.55 points

### Trade #143 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 14:00:00
- **FVG 5m**: 21897.21 - 21908.81
- **Entrée**: 21911.13 @ 2025-01-27 14:57:00
- **Stop Loss**: 21770.85
- **Risk**: 140.28 points
- **TP 1RR**: 22051.41 ✅
- **TP 2RR**: 22191.68 ✅
- **TP 3RR**: 22331.96 ✅
- **TP 4RR**: 22472.24 ✅
- **TP 15RR**: 24015.29 ❌
- **PnL**: -140.28 points (-1.0R)
- **MFE**: 735.08 points
- **MAE**: 319.60 points

### Trade #144 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-27 19:45:00
- **FVG 5m**: 21917.06 - 21954.69
- **Entrée**: 21895.67 @ 2025-01-27 19:59:00
- **Stop Loss**: 21989.65
- **Risk**: 93.98 points
- **TP 1RR**: 21801.68 ❌
- **TP 2RR**: 21707.70 ❌
- **TP 3RR**: 21613.72 ❌
- **TP 4RR**: 21519.74 ❌
- **TP 15RR**: 20485.93 ❌
- **PnL**: -93.98 points (-1.0R)
- **MFE**: 19.59 points
- **MAE**: 96.65 points

### Trade #145 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-27 20:00:00
- **FVG 5m**: 21938.19 - 21944.38
- **Entrée**: 21947.73 @ 2025-01-27 20:11:00
- **Stop Loss**: 21865.14
- **Risk**: 82.59 points
- **TP 1RR**: 22030.32 ✅
- **TP 2RR**: 22112.91 ❌
- **TP 3RR**: 22195.50 ❌
- **TP 4RR**: 22278.09 ❌
- **TP 15RR**: 23186.58 ❌
- **PnL**: -82.59 points (-1.0R)
- **MFE**: 139.18 points
- **MAE**: 86.86 points

### Trade #146 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 02:00:00
- **FVG 5m**: 22025.82 - 22030.98
- **Entrée**: 22022.99 @ 2025-01-28 03:29:00
- **Stop Loss**: 22035.03
- **Risk**: 12.04 points
- **TP 1RR**: 22010.95 ✅
- **TP 2RR**: 21998.90 ❌
- **TP 3RR**: 21986.86 ❌
- **TP 4RR**: 21974.82 ❌
- **TP 15RR**: 21842.35 ❌
- **PnL**: -12.04 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 16.50 points

### Trade #147 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 02:00:00
- **FVG 5m**: 22025.82 - 22030.98
- **Entrée**: 22022.99 @ 2025-01-28 03:29:00
- **Stop Loss**: 22035.03
- **Risk**: 12.04 points
- **TP 1RR**: 22010.95 ✅
- **TP 2RR**: 21998.90 ❌
- **TP 3RR**: 21986.86 ❌
- **TP 4RR**: 21974.82 ❌
- **TP 15RR**: 21842.35 ❌
- **PnL**: -12.04 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 16.50 points

### Trade #148 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 02:00:00
- **FVG 5m**: 22025.82 - 22030.98
- **Entrée**: 22022.99 @ 2025-01-28 03:29:00
- **Stop Loss**: 22035.03
- **Risk**: 12.04 points
- **TP 1RR**: 22010.95 ✅
- **TP 2RR**: 21998.90 ❌
- **TP 3RR**: 21986.86 ❌
- **TP 4RR**: 21974.82 ❌
- **TP 15RR**: 21842.35 ❌
- **PnL**: -12.04 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 16.50 points

### Trade #149 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 05:30:00
- **FVG 5m**: 21981.49 - 21995.15
- **Entrée**: 21972.21 @ 2025-01-28 06:02:00
- **Stop Loss**: 22045.86
- **Risk**: 73.65 points
- **TP 1RR**: 21898.57 ✅
- **TP 2RR**: 21824.92 ✅
- **TP 3RR**: 21751.27 ❌
- **TP 4RR**: 21677.62 ❌
- **TP 15RR**: 20867.49 ❌
- **PnL**: -73.65 points (-1.0R)
- **MFE**: 157.48 points
- **MAE**: 81.70 points

### Trade #150 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 08:45:00
- **FVG 5m**: 21923.76 - 21940.00
- **Entrée**: 21942.32 @ 2025-01-28 08:57:00
- **Stop Loss**: 21803.83
- **Risk**: 138.49 points
- **TP 1RR**: 22080.81 ✅
- **TP 2RR**: 22219.30 ✅
- **TP 3RR**: 22357.78 ✅
- **TP 4RR**: 22496.27 ✅
- **TP 15RR**: 24019.66 ❌
- **PnL**: -138.49 points (-1.0R)
- **MFE**: 703.89 points
- **MAE**: 350.79 points

### Trade #151 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 08:45:00
- **FVG 5m**: 21923.76 - 21940.00
- **Entrée**: 21942.32 @ 2025-01-28 08:57:00
- **Stop Loss**: 21803.83
- **Risk**: 138.49 points
- **TP 1RR**: 22080.81 ✅
- **TP 2RR**: 22219.30 ✅
- **TP 3RR**: 22357.78 ✅
- **TP 4RR**: 22496.27 ✅
- **TP 15RR**: 24019.66 ❌
- **PnL**: -138.49 points (-1.0R)
- **MFE**: 703.89 points
- **MAE**: 350.79 points

### Trade #152 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 08:45:00
- **FVG 5m**: 21923.76 - 21940.00
- **Entrée**: 21942.32 @ 2025-01-28 08:57:00
- **Stop Loss**: 21803.83
- **Risk**: 138.49 points
- **TP 1RR**: 22080.81 ✅
- **TP 2RR**: 22219.30 ✅
- **TP 3RR**: 22357.78 ✅
- **TP 4RR**: 22496.27 ✅
- **TP 15RR**: 24019.66 ❌
- **PnL**: -138.49 points (-1.0R)
- **MFE**: 703.89 points
- **MAE**: 350.79 points

### Trade #153 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-28 11:00:00
- **FVG 5m**: 22194.13 - 22212.69
- **Entrée**: 22212.95 @ 2025-01-28 13:18:00
- **Stop Loss**: 22124.30
- **Risk**: 88.65 points
- **TP 1RR**: 22301.59 ✅
- **TP 2RR**: 22390.24 ❌
- **TP 3RR**: 22478.89 ❌
- **TP 4RR**: 22567.54 ❌
- **TP 15RR**: 23542.66 ❌
- **PnL**: -88.65 points (-1.0R)
- **MFE**: 155.93 points
- **MAE**: 92.53 points

### Trade #154 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-28 12:15:00
- **FVG 5m**: 22208.82 - 22216.55
- **Entrée**: 22205.21 @ 2025-01-28 12:39:00
- **Stop Loss**: 22263.51
- **Risk**: 58.29 points
- **TP 1RR**: 22146.92 ❌
- **TP 2RR**: 22088.63 ❌
- **TP 3RR**: 22030.33 ❌
- **TP 4RR**: 21972.04 ❌
- **TP 15RR**: 21330.82 ❌
- **PnL**: -58.29 points (-1.0R)
- **MFE**: 25.52 points
- **MAE**: 60.31 points

### Trade #155 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 07:00:00
- **FVG 5m**: 22275.32 - 22277.90
- **Entrée**: 22268.88 @ 2025-01-29 08:29:00
- **Stop Loss**: 22328.75
- **Risk**: 59.87 points
- **TP 1RR**: 22209.00 ✅
- **TP 2RR**: 22149.13 ✅
- **TP 3RR**: 22089.26 ✅
- **TP 4RR**: 22029.39 ✅
- **TP 15RR**: 21370.80 ❌
- **PnL**: -59.87 points (-1.0R)
- **MFE**: 240.22 points
- **MAE**: 61.86 points

### Trade #156 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 07:00:00
- **FVG 5m**: 22275.32 - 22277.90
- **Entrée**: 22268.88 @ 2025-01-29 08:29:00
- **Stop Loss**: 22328.75
- **Risk**: 59.87 points
- **TP 1RR**: 22209.00 ✅
- **TP 2RR**: 22149.13 ✅
- **TP 3RR**: 22089.26 ✅
- **TP 4RR**: 22029.39 ✅
- **TP 15RR**: 21370.80 ❌
- **PnL**: -59.87 points (-1.0R)
- **MFE**: 240.22 points
- **MAE**: 61.86 points

### Trade #157 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 07:30:00
- **FVG 5m**: 22275.32 - 22277.90
- **Entrée**: 22268.88 @ 2025-01-29 08:29:00
- **Stop Loss**: 22270.98
- **Risk**: 2.11 points
- **TP 1RR**: 22266.77 ❌
- **TP 2RR**: 22264.66 ❌
- **TP 3RR**: 22262.55 ❌
- **TP 4RR**: 22260.44 ❌
- **TP 15RR**: 22237.24 ❌
- **PnL**: -2.11 points (-1.0R)
- **MFE**: 21.65 points
- **MAE**: 6.44 points

### Trade #158 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-29 07:45:00
- **FVG 5m**: 22254.44 - 22269.13
- **Entrée**: 22271.45 @ 2025-01-29 07:59:00
- **Stop Loss**: 22220.39
- **Risk**: 51.07 points
- **TP 1RR**: 22322.52 ❌
- **TP 2RR**: 22373.58 ❌
- **TP 3RR**: 22424.65 ❌
- **TP 4RR**: 22475.72 ❌
- **TP 15RR**: 23037.44 ❌
- **PnL**: -51.07 points (-1.0R)
- **MFE**: 25.26 points
- **MAE**: 55.67 points

### Trade #159 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 09:30:00
- **FVG 5m**: 22176.09 - 22185.37
- **Entrée**: 22172.22 @ 2025-01-29 11:47:00
- **Stop Loss**: 22204.45
- **Risk**: 32.23 points
- **TP 1RR**: 22139.99 ✅
- **TP 2RR**: 22107.76 ✅
- **TP 3RR**: 22075.53 ✅
- **TP 4RR**: 22043.30 ✅
- **TP 15RR**: 21688.75 ❌
- **PnL**: -32.23 points (-1.0R)
- **MFE**: 143.56 points
- **MAE**: 36.34 points

### Trade #160 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-29 12:00:00
- **FVG 5m**: 22122.22 - 22143.10
- **Entrée**: 22150.57 @ 2025-01-29 12:28:00
- **Stop Loss**: 22017.65
- **Risk**: 132.93 points
- **TP 1RR**: 22283.50 ✅
- **TP 2RR**: 22416.42 ✅
- **TP 3RR**: 22549.35 ✅
- **TP 4RR**: 22682.28 ❌
- **TP 15RR**: 24144.46 ❌
- **PnL**: -132.93 points (-1.0R)
- **MFE**: 495.64 points
- **MAE**: 559.04 points

### Trade #161 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-29 13:45:00
- **FVG 5m**: 22213.72 - 22236.14
- **Entrée**: 22211.66 @ 2025-01-29 14:37:00
- **Stop Loss**: 22257.32
- **Risk**: 45.66 points
- **TP 1RR**: 22166.00 ✅
- **TP 2RR**: 22120.34 ✅
- **TP 3RR**: 22074.68 ✅
- **TP 4RR**: 22029.01 ❌
- **TP 15RR**: 21526.75 ❌
- **PnL**: -45.66 points (-1.0R)
- **MFE**: 162.38 points
- **MAE**: 55.16 points

### Trade #162 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-29 14:15:00
- **FVG 5m**: 22232.79 - 22236.14
- **Entrée**: 22259.85 @ 2025-01-29 14:28:00
- **Stop Loss**: 22116.31
- **Risk**: 143.54 points
- **TP 1RR**: 22403.40 ❌
- **TP 2RR**: 22546.94 ❌
- **TP 3RR**: 22690.48 ❌
- **TP 4RR**: 22834.03 ❌
- **TP 15RR**: 24413.00 ❌
- **PnL**: -143.54 points (-1.0R)
- **MFE**: 9.79 points
- **MAE**: 145.37 points

### Trade #163 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 02:15:00
- **FVG 5m**: 22355.48 - 22368.36
- **Entrée**: 22353.16 @ 2025-01-30 03:02:00
- **Stop Loss**: 22399.15
- **Risk**: 45.99 points
- **TP 1RR**: 22307.17 ✅
- **TP 2RR**: 22261.18 ✅
- **TP 3RR**: 22215.19 ❌
- **TP 4RR**: 22169.20 ❌
- **TP 15RR**: 21663.32 ❌
- **PnL**: -45.99 points (-1.0R)
- **MFE**: 110.83 points
- **MAE**: 58.77 points

### Trade #164 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22326.35 - 22332.02
- **Entrée**: 22325.84 @ 2025-01-30 03:33:00
- **Stop Loss**: 22384.71
- **Risk**: 58.87 points
- **TP 1RR**: 22266.97 ✅
- **TP 2RR**: 22208.10 ❌
- **TP 3RR**: 22149.23 ❌
- **TP 4RR**: 22090.36 ❌
- **TP 15RR**: 21442.80 ❌
- **PnL**: -58.87 points (-1.0R)
- **MFE**: 83.51 points
- **MAE**: 62.89 points

### Trade #165 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22326.35 - 22332.02
- **Entrée**: 22325.84 @ 2025-01-30 03:33:00
- **Stop Loss**: 22384.71
- **Risk**: 58.87 points
- **TP 1RR**: 22266.97 ✅
- **TP 2RR**: 22208.10 ❌
- **TP 3RR**: 22149.23 ❌
- **TP 4RR**: 22090.36 ❌
- **TP 15RR**: 21442.80 ❌
- **PnL**: -58.87 points (-1.0R)
- **MFE**: 83.51 points
- **MAE**: 62.89 points

### Trade #166 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22326.35 - 22332.02
- **Entrée**: 22325.84 @ 2025-01-30 03:33:00
- **Stop Loss**: 22384.71
- **Risk**: 58.87 points
- **TP 1RR**: 22266.97 ✅
- **TP 2RR**: 22208.10 ❌
- **TP 3RR**: 22149.23 ❌
- **TP 4RR**: 22090.36 ❌
- **TP 15RR**: 21442.80 ❌
- **PnL**: -58.87 points (-1.0R)
- **MFE**: 83.51 points
- **MAE**: 62.89 points

### Trade #167 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 03:00:00
- **FVG 5m**: 22326.35 - 22332.02
- **Entrée**: 22325.84 @ 2025-01-30 03:33:00
- **Stop Loss**: 22384.71
- **Risk**: 58.87 points
- **TP 1RR**: 22266.97 ✅
- **TP 2RR**: 22208.10 ❌
- **TP 3RR**: 22149.23 ❌
- **TP 4RR**: 22090.36 ❌
- **TP 15RR**: 21442.80 ❌
- **PnL**: -58.87 points (-1.0R)
- **MFE**: 83.51 points
- **MAE**: 62.89 points

### Trade #168 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 04:15:00
- **FVG 5m**: 22296.45 - 22302.12
- **Entrée**: 22303.67 @ 2025-01-30 04:31:00
- **Stop Loss**: 22267.01
- **Risk**: 36.66 points
- **TP 1RR**: 22340.33 ✅
- **TP 2RR**: 22376.98 ❌
- **TP 3RR**: 22413.64 ❌
- **TP 4RR**: 22450.29 ❌
- **TP 15RR**: 22853.50 ❌
- **PnL**: -36.66 points (-1.0R)
- **MFE**: 38.15 points
- **MAE**: 49.23 points

### Trade #169 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 06:30:00
- **FVG 5m**: 22302.64 - 22312.95
- **Entrée**: 22313.98 @ 2025-01-30 07:53:00
- **Stop Loss**: 22234.81
- **Risk**: 79.17 points
- **TP 1RR**: 22393.15 ✅
- **TP 2RR**: 22472.31 ❌
- **TP 3RR**: 22551.48 ❌
- **TP 4RR**: 22630.65 ❌
- **TP 15RR**: 23501.48 ❌
- **PnL**: -79.17 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 82.48 points

### Trade #170 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 06:45:00
- **FVG 5m**: 22302.64 - 22312.95
- **Entrée**: 22313.98 @ 2025-01-30 07:53:00
- **Stop Loss**: 22270.36
- **Risk**: 43.62 points
- **TP 1RR**: 22357.60 ❌
- **TP 2RR**: 22401.21 ❌
- **TP 3RR**: 22444.83 ❌
- **TP 4RR**: 22488.44 ❌
- **TP 15RR**: 22968.22 ❌
- **PnL**: -43.62 points (-1.0R)
- **MFE**: 36.34 points
- **MAE**: 48.46 points

### Trade #171 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 08:45:00
- **FVG 5m**: 22347.49 - 22355.48
- **Entrée**: 22335.89 @ 2025-01-30 08:58:00
- **Stop Loss**: 22433.44
- **Risk**: 97.55 points
- **TP 1RR**: 22238.33 ✅
- **TP 2RR**: 22140.78 ✅
- **TP 3RR**: 22043.22 ❌
- **TP 4RR**: 21945.67 ❌
- **TP 15RR**: 20872.57 ❌
- **PnL**: -97.55 points (-1.0R)
- **MFE**: 253.10 points
- **MAE**: 97.68 points

### Trade #172 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 09:00:00
- **FVG 5m**: 22210.37 - 22215.01
- **Entrée**: 22198.25 @ 2025-01-30 09:29:00
- **Stop Loss**: 22358.66
- **Risk**: 160.41 points
- **TP 1RR**: 22037.85 ❌
- **TP 2RR**: 21877.44 ❌
- **TP 3RR**: 21717.04 ❌
- **TP 4RR**: 21556.63 ❌
- **TP 15RR**: 19792.16 ❌
- **PnL**: -160.41 points (-1.0R)
- **MFE**: 115.47 points
- **MAE**: 166.76 points

### Trade #173 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-30 10:45:00
- **FVG 5m**: 22247.74 - 22255.99
- **Entrée**: 22262.69 @ 2025-01-30 12:38:00
- **Stop Loss**: 22197.97
- **Risk**: 64.71 points
- **TP 1RR**: 22327.40 ✅
- **TP 2RR**: 22392.12 ❌
- **TP 3RR**: 22456.83 ❌
- **TP 4RR**: 22521.55 ❌
- **TP 15RR**: 23233.41 ❌
- **PnL**: -64.71 points (-1.0R)
- **MFE**: 109.28 points
- **MAE**: 64.95 points

### Trade #174 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 14:30:00
- **FVG 5m**: 22369.65 - 22375.84
- **Entrée**: 22366.82 @ 2025-01-30 17:18:00
- **Stop Loss**: 22373.36
- **Risk**: 6.54 points
- **TP 1RR**: 22360.28 ✅
- **TP 2RR**: 22353.73 ✅
- **TP 3RR**: 22347.19 ✅
- **TP 4RR**: 22340.65 ✅
- **TP 15RR**: 22268.69 ❌
- **PnL**: -6.54 points (-1.0R)
- **MFE**: 36.08 points
- **MAE**: 7.73 points

### Trade #175 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 14:30:00
- **FVG 5m**: 22369.65 - 22375.84
- **Entrée**: 22366.82 @ 2025-01-30 17:18:00
- **Stop Loss**: 22373.36
- **Risk**: 6.54 points
- **TP 1RR**: 22360.28 ✅
- **TP 2RR**: 22353.73 ✅
- **TP 3RR**: 22347.19 ✅
- **TP 4RR**: 22340.65 ✅
- **TP 15RR**: 22268.69 ❌
- **PnL**: -6.54 points (-1.0R)
- **MFE**: 36.08 points
- **MAE**: 7.73 points

### Trade #176 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-30 17:15:00
- **FVG 5m**: 22348.26 - 22353.41
- **Entrée**: 22344.65 @ 2025-01-30 17:27:00
- **Stop Loss**: 22399.66
- **Risk**: 55.01 points
- **TP 1RR**: 22289.64 ❌
- **TP 2RR**: 22234.63 ❌
- **TP 3RR**: 22179.62 ❌
- **TP 4RR**: 22124.61 ❌
- **TP 15RR**: 21519.50 ❌
- **PnL**: -55.01 points (-1.0R)
- **MFE**: 13.92 points
- **MAE**: 56.19 points

### Trade #177 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 01:15:00
- **FVG 5m**: 22446.97 - 22453.68
- **Entrée**: 22441.82 @ 2025-01-31 02:44:00
- **Stop Loss**: 22493.78
- **Risk**: 51.96 points
- **TP 1RR**: 22389.86 ❌
- **TP 2RR**: 22337.89 ❌
- **TP 3RR**: 22285.93 ❌
- **TP 4RR**: 22233.96 ❌
- **TP 15RR**: 21662.35 ❌
- **PnL**: -51.96 points (-1.0R)
- **MFE**: 25.77 points
- **MAE**: 72.94 points

### Trade #178 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 02:00:00
- **FVG 5m**: 22446.97 - 22453.68
- **Entrée**: 22441.82 @ 2025-01-31 02:44:00
- **Stop Loss**: 22480.63
- **Risk**: 38.81 points
- **TP 1RR**: 22403.01 ❌
- **TP 2RR**: 22364.19 ❌
- **TP 3RR**: 22325.38 ❌
- **TP 4RR**: 22286.57 ❌
- **TP 15RR**: 21859.62 ❌
- **PnL**: -38.81 points (-1.0R)
- **MFE**: 25.77 points
- **MAE**: 43.82 points

### Trade #179 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 06:00:00
- **FVG 5m**: 22459.60 - 22465.27
- **Entrée**: 22457.28 @ 2025-01-31 06:59:00
- **Stop Loss**: 22499.72
- **Risk**: 42.43 points
- **TP 1RR**: 22414.85 ❌
- **TP 2RR**: 22372.42 ❌
- **TP 3RR**: 22329.99 ❌
- **TP 4RR**: 22287.56 ❌
- **TP 15RR**: 21820.82 ❌
- **PnL**: -42.43 points (-1.0R)
- **MFE**: 33.76 points
- **MAE**: 57.48 points

### Trade #180 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 07:30:00
- **FVG 5m**: 22583.58 - 22598.27
- **Entrée**: 22599.56 @ 2025-01-31 09:33:00
- **Stop Loss**: 22418.23
- **Risk**: 181.32 points
- **TP 1RR**: 22780.88 ❌
- **TP 2RR**: 22962.21 ❌
- **TP 3RR**: 23143.53 ❌
- **TP 4RR**: 23324.85 ❌
- **TP 15RR**: 25319.42 ❌
- **PnL**: -181.32 points (-1.0R)
- **MFE**: 46.65 points
- **MAE**: 182.48 points

### Trade #181 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 08:45:00
- **FVG 5m**: 22583.58 - 22598.27
- **Entrée**: 22599.56 @ 2025-01-31 09:33:00
- **Stop Loss**: 22462.29
- **Risk**: 137.27 points
- **TP 1RR**: 22736.83 ❌
- **TP 2RR**: 22874.10 ❌
- **TP 3RR**: 23011.37 ❌
- **TP 4RR**: 23148.65 ❌
- **TP 15RR**: 24658.64 ❌
- **PnL**: -137.27 points (-1.0R)
- **MFE**: 46.65 points
- **MAE**: 143.30 points

### Trade #182 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-01-31 08:45:00
- **FVG 5m**: 22583.58 - 22598.27
- **Entrée**: 22599.56 @ 2025-01-31 09:33:00
- **Stop Loss**: 22462.29
- **Risk**: 137.27 points
- **TP 1RR**: 22736.83 ❌
- **TP 2RR**: 22874.10 ❌
- **TP 3RR**: 23011.37 ❌
- **TP 4RR**: 23148.65 ❌
- **TP 15RR**: 24658.64 ❌
- **PnL**: -137.27 points (-1.0R)
- **MFE**: 46.65 points
- **MAE**: 143.30 points

### Trade #183 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 12:30:00
- **FVG 5m**: 22352.38 - 22375.32
- **Entrée**: 22336.15 @ 2025-01-31 13:37:00
- **Stop Loss**: 22514.41
- **Risk**: 178.27 points
- **TP 1RR**: 22157.88 ✅
- **TP 2RR**: 21979.61 ✅
- **TP 3RR**: 21801.34 ✅
- **TP 4RR**: 21623.07 ✅
- **TP 15RR**: 19662.12 ❌
- **PnL**: -178.27 points (-1.0R)
- **MFE**: 744.62 points
- **MAE**: 180.42 points

### Trade #184 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 12:30:00
- **FVG 5m**: 22352.38 - 22375.32
- **Entrée**: 22336.15 @ 2025-01-31 13:37:00
- **Stop Loss**: 22514.41
- **Risk**: 178.27 points
- **TP 1RR**: 22157.88 ✅
- **TP 2RR**: 21979.61 ✅
- **TP 3RR**: 21801.34 ✅
- **TP 4RR**: 21623.07 ✅
- **TP 15RR**: 19662.12 ❌
- **PnL**: -178.27 points (-1.0R)
- **MFE**: 744.62 points
- **MAE**: 180.42 points

### Trade #185 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 13:00:00
- **FVG 5m**: 22352.38 - 22375.32
- **Entrée**: 22336.15 @ 2025-01-31 13:37:00
- **Stop Loss**: 22467.48
- **Risk**: 131.34 points
- **TP 1RR**: 22204.81 ✅
- **TP 2RR**: 22073.47 ✅
- **TP 3RR**: 21942.14 ✅
- **TP 4RR**: 21810.80 ✅
- **TP 15RR**: 20366.11 ❌
- **PnL**: -131.34 points (-1.0R)
- **MFE**: 744.62 points
- **MAE**: 133.77 points

### Trade #186 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-01-31 13:15:00
- **FVG 5m**: 22352.38 - 22375.32
- **Entrée**: 22336.15 @ 2025-01-31 13:37:00
- **Stop Loss**: 22448.14
- **Risk**: 112.00 points
- **TP 1RR**: 22224.15 ✅
- **TP 2RR**: 22112.15 ✅
- **TP 3RR**: 22000.16 ✅
- **TP 4RR**: 21888.16 ✅
- **TP 15RR**: 20656.21 ❌
- **PnL**: -112.00 points (-1.0R)
- **MFE**: 744.62 points
- **MAE**: 120.62 points

### Trade #187 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-02 17:45:00
- **FVG 5m**: 21774.01 - 21777.88
- **Entrée**: 21786.64 @ 2025-02-02 19:22:00
- **Stop Loss**: 21725.51
- **Risk**: 61.13 points
- **TP 1RR**: 21847.77 ❌
- **TP 2RR**: 21908.90 ❌
- **TP 3RR**: 21970.02 ❌
- **TP 4RR**: 22031.15 ❌
- **TP 15RR**: 22703.56 ❌
- **PnL**: -61.13 points (-1.0R)
- **MFE**: 18.30 points
- **MAE**: 61.86 points

### Trade #188 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 02:00:00
- **FVG 5m**: 21844.12 - 21872.98
- **Entrée**: 21876.85 @ 2025-02-03 02:18:00
- **Stop Loss**: 21761.32
- **Risk**: 115.53 points
- **TP 1RR**: 21992.38 ✅
- **TP 2RR**: 22107.91 ✅
- **TP 3RR**: 22223.44 ✅
- **TP 4RR**: 22338.97 ✅
- **TP 15RR**: 23609.79 ❌
- **PnL**: -115.53 points (-1.0R)
- **MFE**: 1134.06 points
- **MAE**: 135.57 points

### Trade #189 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 05:15:00
- **FVG 5m**: 21881.75 - 21884.58
- **Entrée**: 21881.49 @ 2025-02-03 05:36:00
- **Stop Loss**: 21936.78
- **Risk**: 55.29 points
- **TP 1RR**: 21826.20 ✅
- **TP 2RR**: 21770.90 ❌
- **TP 3RR**: 21715.61 ❌
- **TP 4RR**: 21660.31 ❌
- **TP 15RR**: 21052.07 ❌
- **PnL**: -55.29 points (-1.0R)
- **MFE**: 70.88 points
- **MAE**: 65.72 points

### Trade #190 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 08:30:00
- **FVG 5m**: 21896.70 - 21910.10
- **Entrée**: 21854.94 @ 2025-02-03 08:52:00
- **Stop Loss**: 21985.52
- **Risk**: 130.58 points
- **TP 1RR**: 21724.36 ❌
- **TP 2RR**: 21593.78 ❌
- **TP 3RR**: 21463.20 ❌
- **TP 4RR**: 21332.62 ❌
- **TP 15RR**: 19896.25 ❌
- **PnL**: -130.58 points (-1.0R)
- **MFE**: 87.89 points
- **MAE**: 135.31 points

### Trade #191 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 08:45:00
- **FVG 5m**: 21797.72 - 21811.64
- **Entrée**: 21783.55 @ 2025-02-03 09:14:00
- **Stop Loss**: 21937.56
- **Risk**: 154.01 points
- **TP 1RR**: 21629.54 ❌
- **TP 2RR**: 21475.53 ❌
- **TP 3RR**: 21321.52 ❌
- **TP 4RR**: 21167.51 ❌
- **TP 15RR**: 19473.40 ❌
- **PnL**: -154.01 points (-1.0R)
- **MFE**: 16.50 points
- **MAE**: 206.71 points

### Trade #192 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:30:00
- **FVG 5m**: 22035.36 - 22039.23
- **Entrée**: 22040.52 @ 2025-02-03 11:49:00
- **Stop Loss**: 21970.50
- **Risk**: 70.01 points
- **TP 1RR**: 22110.53 ✅
- **TP 2RR**: 22180.54 ✅
- **TP 3RR**: 22250.56 ✅
- **TP 4RR**: 22320.57 ❌
- **TP 15RR**: 23090.72 ❌
- **PnL**: -70.01 points (-1.0R)
- **MFE**: 228.36 points
- **MAE**: 73.97 points

### Trade #193 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:30:00
- **FVG 5m**: 22035.36 - 22039.23
- **Entrée**: 22040.52 @ 2025-02-03 11:49:00
- **Stop Loss**: 21970.50
- **Risk**: 70.01 points
- **TP 1RR**: 22110.53 ✅
- **TP 2RR**: 22180.54 ✅
- **TP 3RR**: 22250.56 ✅
- **TP 4RR**: 22320.57 ❌
- **TP 15RR**: 23090.72 ❌
- **PnL**: -70.01 points (-1.0R)
- **MFE**: 228.36 points
- **MAE**: 73.97 points

### Trade #194 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 09:30:00
- **FVG 5m**: 22035.36 - 22039.23
- **Entrée**: 22040.52 @ 2025-02-03 11:49:00
- **Stop Loss**: 21970.50
- **Risk**: 70.01 points
- **TP 1RR**: 22110.53 ✅
- **TP 2RR**: 22180.54 ✅
- **TP 3RR**: 22250.56 ✅
- **TP 4RR**: 22320.57 ❌
- **TP 15RR**: 23090.72 ❌
- **PnL**: -70.01 points (-1.0R)
- **MFE**: 228.36 points
- **MAE**: 73.97 points

### Trade #195 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-03 14:00:00
- **FVG 5m**: 22132.79 - 22146.19
- **Entrée**: 22130.98 @ 2025-02-03 14:27:00
- **Stop Loss**: 22183.82
- **Risk**: 52.84 points
- **TP 1RR**: 22078.14 ✅
- **TP 2RR**: 22025.30 ❌
- **TP 3RR**: 21972.46 ❌
- **TP 4RR**: 21919.62 ❌
- **TP 15RR**: 21338.38 ❌
- **PnL**: -52.84 points (-1.0R)
- **MFE**: 80.42 points
- **MAE**: 83.25 points

### Trade #196 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 15:30:00
- **FVG 5m**: 22221.45 - 22232.79
- **Entrée**: 22242.84 @ 2025-02-03 17:06:00
- **Stop Loss**: 22145.42
- **Risk**: 97.42 points
- **TP 1RR**: 22340.26 ❌
- **TP 2RR**: 22437.69 ❌
- **TP 3RR**: 22535.11 ❌
- **TP 4RR**: 22632.53 ❌
- **TP 15RR**: 23704.17 ❌
- **PnL**: -97.42 points (-1.0R)
- **MFE**: 10.31 points
- **MAE**: 97.68 points

### Trade #197 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-03 23:30:00
- **FVG 5m**: 22033.56 - 22036.13
- **Entrée**: 22046.19 @ 2025-02-04 00:48:00
- **Stop Loss**: 21966.90
- **Risk**: 79.29 points
- **TP 1RR**: 22125.48 ✅
- **TP 2RR**: 22204.77 ✅
- **TP 3RR**: 22284.06 ✅
- **TP 4RR**: 22363.35 ✅
- **TP 15RR**: 23235.54 ❌
- **PnL**: -79.29 points (-1.0R)
- **MFE**: 964.73 points
- **MAE**: 80.42 points

### Trade #198 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-04 00:45:00
- **FVG 5m**: 22004.95 - 22022.47
- **Entrée**: 22024.54 @ 2025-02-04 02:59:00
- **Stop Loss**: 22008.37
- **Risk**: 16.16 points
- **TP 1RR**: 22040.70 ✅
- **TP 2RR**: 22056.87 ✅
- **TP 3RR**: 22073.03 ✅
- **TP 4RR**: 22089.19 ✅
- **TP 15RR**: 22267.00 ✅
- **PnL**: 242.47 points (15.0R)
- **MFE**: 250.78 points
- **MAE**: 7.22 points

### Trade #199 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-04 06:30:00
- **FVG 5m**: 22096.70 - 22100.05
- **Entrée**: 22093.10 @ 2025-02-04 08:14:00
- **Stop Loss**: 22175.31
- **Risk**: 82.22 points
- **TP 1RR**: 22010.88 ❌
- **TP 2RR**: 21928.66 ❌
- **TP 3RR**: 21846.44 ❌
- **TP 4RR**: 21764.22 ❌
- **TP 15RR**: 20859.81 ❌
- **PnL**: -82.22 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 96.65 points

### Trade #200 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-04 08:30:00
- **FVG 5m**: 22189.49 - 22212.43
- **Entrée**: 22214.23 @ 2025-02-04 08:54:00
- **Stop Loss**: 22057.06
- **Risk**: 157.17 points
- **TP 1RR**: 22371.41 ✅
- **TP 2RR**: 22528.58 ✅
- **TP 3RR**: 22685.75 ✅
- **TP 4RR**: 22842.93 ✅
- **TP 15RR**: 24571.84 ❌
- **PnL**: -157.17 points (-1.0R)
- **MFE**: 796.68 points
- **MAE**: 157.22 points

### Trade #201 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-04 11:15:00
- **FVG 5m**: 22241.55 - 22244.91
- **Entrée**: 22240.27 @ 2025-02-04 11:28:00
- **Stop Loss**: 22333.65
- **Risk**: 93.38 points
- **TP 1RR**: 22146.89 ❌
- **TP 2RR**: 22053.50 ❌
- **TP 3RR**: 21960.12 ❌
- **TP 4RR**: 21866.74 ❌
- **TP 15RR**: 20839.55 ❌
- **PnL**: -93.38 points (-1.0R)
- **MFE**: 22.94 points
- **MAE**: 96.65 points

### Trade #202 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-04 15:00:00
- **FVG 5m**: 22263.46 - 22268.36
- **Entrée**: 22254.18 @ 2025-02-04 15:38:00
- **Stop Loss**: 22374.65
- **Risk**: 120.46 points
- **TP 1RR**: 22133.72 ✅
- **TP 2RR**: 22013.26 ❌
- **TP 3RR**: 21892.79 ❌
- **TP 4RR**: 21772.33 ❌
- **TP 15RR**: 20447.22 ❌
- **PnL**: -120.46 points (-1.0R)
- **MFE**: 160.83 points
- **MAE**: 121.91 points

### Trade #203 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 02:30:00
- **FVG 5m**: 22146.45 - 22150.57
- **Entrée**: 22143.10 @ 2025-02-05 02:41:00
- **Stop Loss**: 22218.89
- **Risk**: 75.80 points
- **TP 1RR**: 22067.30 ❌
- **TP 2RR**: 21991.50 ❌
- **TP 3RR**: 21915.71 ❌
- **TP 4RR**: 21839.91 ❌
- **TP 15RR**: 21006.14 ❌
- **PnL**: -75.80 points (-1.0R)
- **MFE**: 49.74 points
- **MAE**: 78.10 points

### Trade #204 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-05 08:15:00
- **FVG 5m**: 22251.61 - 22282.79
- **Entrée**: 22290.53 @ 2025-02-05 10:29:00
- **Stop Loss**: 22186.38
- **Risk**: 104.14 points
- **TP 1RR**: 22394.67 ✅
- **TP 2RR**: 22498.81 ✅
- **TP 3RR**: 22602.96 ✅
- **TP 4RR**: 22707.10 ❌
- **TP 15RR**: 23852.68 ❌
- **PnL**: -104.14 points (-1.0R)
- **MFE**: 357.75 points
- **MAE**: 209.29 points

### Trade #205 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-05 08:15:00
- **FVG 5m**: 22251.61 - 22282.79
- **Entrée**: 22290.53 @ 2025-02-05 10:29:00
- **Stop Loss**: 22186.38
- **Risk**: 104.14 points
- **TP 1RR**: 22394.67 ✅
- **TP 2RR**: 22498.81 ✅
- **TP 3RR**: 22602.96 ✅
- **TP 4RR**: 22707.10 ❌
- **TP 15RR**: 23852.68 ❌
- **PnL**: -104.14 points (-1.0R)
- **MFE**: 357.75 points
- **MAE**: 209.29 points

### Trade #206 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 12:15:00
- **FVG 5m**: 22393.11 - 22403.67
- **Entrée**: 22391.82 @ 2025-02-05 14:39:00
- **Stop Loss**: 22395.02
- **Risk**: 3.20 points
- **TP 1RR**: 22388.62 ✅
- **TP 2RR**: 22385.41 ✅
- **TP 3RR**: 22382.21 ✅
- **TP 4RR**: 22379.01 ✅
- **TP 15RR**: 22343.79 ❌
- **PnL**: -3.20 points (-1.0R)
- **MFE**: 30.41 points
- **MAE**: 5.67 points

### Trade #207 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-05 12:15:00
- **FVG 5m**: 22393.11 - 22403.67
- **Entrée**: 22391.82 @ 2025-02-05 14:39:00
- **Stop Loss**: 22395.02
- **Risk**: 3.20 points
- **TP 1RR**: 22388.62 ✅
- **TP 2RR**: 22385.41 ✅
- **TP 3RR**: 22382.21 ✅
- **TP 4RR**: 22379.01 ✅
- **TP 15RR**: 22343.79 ❌
- **PnL**: -3.20 points (-1.0R)
- **MFE**: 30.41 points
- **MAE**: 5.67 points

### Trade #208 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 06:45:00
- **FVG 5m**: 22451.61 - 22462.18
- **Entrée**: 22463.21 @ 2025-02-06 08:44:00
- **Stop Loss**: 22409.47
- **Risk**: 53.74 points
- **TP 1RR**: 22516.95 ✅
- **TP 2RR**: 22570.69 ❌
- **TP 3RR**: 22624.43 ❌
- **TP 4RR**: 22678.16 ❌
- **TP 15RR**: 23269.28 ❌
- **PnL**: -53.74 points (-1.0R)
- **MFE**: 62.12 points
- **MAE**: 79.38 points

### Trade #209 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 07:45:00
- **FVG 5m**: 22451.61 - 22462.18
- **Entrée**: 22463.21 @ 2025-02-06 08:44:00
- **Stop Loss**: 22407.16
- **Risk**: 56.06 points
- **TP 1RR**: 22519.27 ✅
- **TP 2RR**: 22575.32 ❌
- **TP 3RR**: 22631.38 ❌
- **TP 4RR**: 22687.44 ❌
- **TP 15RR**: 23304.06 ❌
- **PnL**: -56.06 points (-1.0R)
- **MFE**: 62.12 points
- **MAE**: 79.38 points

### Trade #210 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 07:45:00
- **FVG 5m**: 22451.61 - 22462.18
- **Entrée**: 22463.21 @ 2025-02-06 08:44:00
- **Stop Loss**: 22407.16
- **Risk**: 56.06 points
- **TP 1RR**: 22519.27 ✅
- **TP 2RR**: 22575.32 ❌
- **TP 3RR**: 22631.38 ❌
- **TP 4RR**: 22687.44 ❌
- **TP 15RR**: 23304.06 ❌
- **PnL**: -56.06 points (-1.0R)
- **MFE**: 62.12 points
- **MAE**: 79.38 points

### Trade #211 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 08:45:00
- **FVG 5m**: 22481.00 - 22506.77
- **Entrée**: 22472.49 @ 2025-02-06 09:24:00
- **Stop Loss**: 22510.80
- **Risk**: 38.31 points
- **TP 1RR**: 22434.18 ❌
- **TP 2RR**: 22395.87 ❌
- **TP 3RR**: 22357.55 ❌
- **TP 4RR**: 22319.24 ❌
- **TP 15RR**: 21897.80 ❌
- **PnL**: -38.31 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 39.69 points

### Trade #212 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 08:45:00
- **FVG 5m**: 22481.00 - 22506.77
- **Entrée**: 22472.49 @ 2025-02-06 09:24:00
- **Stop Loss**: 22510.80
- **Risk**: 38.31 points
- **TP 1RR**: 22434.18 ❌
- **TP 2RR**: 22395.87 ❌
- **TP 3RR**: 22357.55 ❌
- **TP 4RR**: 22319.24 ❌
- **TP 15RR**: 21897.80 ❌
- **PnL**: -38.31 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 39.69 points

### Trade #213 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 09:15:00
- **FVG 5m**: 22466.56 - 22469.14
- **Entrée**: 22464.24 @ 2025-02-06 10:33:00
- **Stop Loss**: 22536.59
- **Risk**: 72.35 points
- **TP 1RR**: 22391.90 ✅
- **TP 2RR**: 22319.55 ❌
- **TP 3RR**: 22247.20 ❌
- **TP 4RR**: 22174.85 ❌
- **TP 15RR**: 21379.03 ❌
- **PnL**: -72.35 points (-1.0R)
- **MFE**: 80.42 points
- **MAE**: 79.90 points

### Trade #214 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 09:15:00
- **FVG 5m**: 22466.56 - 22469.14
- **Entrée**: 22464.24 @ 2025-02-06 10:33:00
- **Stop Loss**: 22536.59
- **Risk**: 72.35 points
- **TP 1RR**: 22391.90 ✅
- **TP 2RR**: 22319.55 ❌
- **TP 3RR**: 22247.20 ❌
- **TP 4RR**: 22174.85 ❌
- **TP 15RR**: 21379.03 ❌
- **PnL**: -72.35 points (-1.0R)
- **MFE**: 80.42 points
- **MAE**: 79.90 points

### Trade #215 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 09:15:00
- **FVG 5m**: 22466.56 - 22469.14
- **Entrée**: 22464.24 @ 2025-02-06 10:33:00
- **Stop Loss**: 22536.59
- **Risk**: 72.35 points
- **TP 1RR**: 22391.90 ✅
- **TP 2RR**: 22319.55 ❌
- **TP 3RR**: 22247.20 ❌
- **TP 4RR**: 22174.85 ❌
- **TP 15RR**: 21379.03 ❌
- **PnL**: -72.35 points (-1.0R)
- **MFE**: 80.42 points
- **MAE**: 79.90 points

### Trade #216 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-06 13:30:00
- **FVG 5m**: 22426.87 - 22433.83
- **Entrée**: 22435.38 @ 2025-02-06 14:14:00
- **Stop Loss**: 22372.64
- **Risk**: 62.74 points
- **TP 1RR**: 22498.12 ✅
- **TP 2RR**: 22560.86 ✅
- **TP 3RR**: 22623.60 ✅
- **TP 4RR**: 22686.34 ❌
- **TP 15RR**: 23376.48 ❌
- **PnL**: -62.74 points (-1.0R)
- **MFE**: 212.89 points
- **MAE**: 67.79 points

### Trade #217 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-06 21:00:00
- **FVG 5m**: 22540.02 - 22542.34
- **Entrée**: 22537.96 @ 2025-02-06 22:29:00
- **Stop Loss**: 22583.78
- **Risk**: 45.82 points
- **TP 1RR**: 22492.13 ❌
- **TP 2RR**: 22446.31 ❌
- **TP 3RR**: 22400.49 ❌
- **TP 4RR**: 22354.66 ❌
- **TP 15RR**: 21850.60 ❌
- **PnL**: -45.82 points (-1.0R)
- **MFE**: 72.94 points
- **MAE**: 71.14 points

### Trade #218 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-07 07:30:00
- **FVG 5m**: 22583.32 - 22616.05
- **Entrée**: 22582.29 @ 2025-02-07 08:59:00
- **Stop Loss**: 22620.40
- **Risk**: 38.11 points
- **TP 1RR**: 22544.18 ✅
- **TP 2RR**: 22506.07 ✅
- **TP 3RR**: 22467.96 ✅
- **TP 4RR**: 22429.85 ✅
- **TP 15RR**: 22010.64 ❌
- **PnL**: -38.11 points (-1.0R)
- **MFE**: 501.05 points
- **MAE**: 47.42 points

### Trade #219 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 07:30:00
- **FVG 5m**: 22572.24 - 22604.97
- **Entrée**: 22607.29 @ 2025-02-07 08:31:00
- **Stop Loss**: 22453.78
- **Risk**: 153.51 points
- **TP 1RR**: 22760.80 ❌
- **TP 2RR**: 22914.30 ❌
- **TP 3RR**: 23067.81 ❌
- **TP 4RR**: 23221.31 ❌
- **TP 15RR**: 24909.88 ❌
- **PnL**: -153.51 points (-1.0R)
- **MFE**: 40.98 points
- **MAE**: 165.21 points

### Trade #220 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 07:30:00
- **FVG 5m**: 22572.24 - 22604.97
- **Entrée**: 22607.29 @ 2025-02-07 08:31:00
- **Stop Loss**: 22453.78
- **Risk**: 153.51 points
- **TP 1RR**: 22760.80 ❌
- **TP 2RR**: 22914.30 ❌
- **TP 3RR**: 23067.81 ❌
- **TP 4RR**: 23221.31 ❌
- **TP 15RR**: 24909.88 ❌
- **PnL**: -153.51 points (-1.0R)
- **MFE**: 40.98 points
- **MAE**: 165.21 points

### Trade #221 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 07:30:00
- **FVG 5m**: 22572.24 - 22604.97
- **Entrée**: 22607.29 @ 2025-02-07 08:31:00
- **Stop Loss**: 22453.78
- **Risk**: 153.51 points
- **TP 1RR**: 22760.80 ❌
- **TP 2RR**: 22914.30 ❌
- **TP 3RR**: 23067.81 ❌
- **TP 4RR**: 23221.31 ❌
- **TP 15RR**: 24909.88 ❌
- **PnL**: -153.51 points (-1.0R)
- **MFE**: 40.98 points
- **MAE**: 165.21 points

### Trade #222 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-07 09:00:00
- **FVG 5m**: 22399.03 - 22407.54
- **Entrée**: 22324.55 @ 2025-02-07 09:53:00
- **Stop Loss**: 22594.61
- **Risk**: 270.06 points
- **TP 1RR**: 22054.48 ❌
- **TP 2RR**: 21784.42 ❌
- **TP 3RR**: 21514.35 ❌
- **TP 4RR**: 21244.29 ❌
- **TP 15RR**: 18273.58 ❌
- **PnL**: -270.06 points (-1.0R)
- **MFE**: 243.31 points
- **MAE**: 278.62 points

### Trade #223 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 09:45:00
- **FVG 5m**: 22348.26 - 22357.02
- **Entrée**: 22358.05 @ 2025-02-07 12:04:00
- **Stop Loss**: 22271.14
- **Risk**: 86.92 points
- **TP 1RR**: 22444.97 ❌
- **TP 2RR**: 22531.89 ❌
- **TP 3RR**: 22618.81 ❌
- **TP 4RR**: 22705.72 ❌
- **TP 15RR**: 23661.81 ❌
- **PnL**: -86.92 points (-1.0R)
- **MFE**: 45.62 points
- **MAE**: 89.95 points

### Trade #224 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-07 09:45:00
- **FVG 5m**: 22348.26 - 22357.02
- **Entrée**: 22358.05 @ 2025-02-07 12:04:00
- **Stop Loss**: 22271.14
- **Risk**: 86.92 points
- **TP 1RR**: 22444.97 ❌
- **TP 2RR**: 22531.89 ❌
- **TP 3RR**: 22618.81 ❌
- **TP 4RR**: 22705.72 ❌
- **TP 15RR**: 23661.81 ❌
- **PnL**: -86.92 points (-1.0R)
- **MFE**: 45.62 points
- **MAE**: 89.95 points

### Trade #225 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-07 13:00:00
- **FVG 5m**: 22266.04 - 22270.42
- **Entrée**: 22251.86 @ 2025-02-07 14:01:00
- **Stop Loss**: 22318.69
- **Risk**: 66.83 points
- **TP 1RR**: 22185.04 ✅
- **TP 2RR**: 22118.21 ✅
- **TP 3RR**: 22051.39 ❌
- **TP 4RR**: 21984.56 ❌
- **TP 15RR**: 21249.47 ❌
- **PnL**: -66.83 points (-1.0R)
- **MFE**: 170.62 points
- **MAE**: 69.07 points

### Trade #226 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-09 17:00:00
- **FVG 5m**: 22223.77 - 22239.49
- **Entrée**: 22240.01 @ 2025-02-09 17:33:00
- **Stop Loss**: 22070.20
- **Risk**: 169.81 points
- **TP 1RR**: 22409.82 ✅
- **TP 2RR**: 22579.63 ✅
- **TP 3RR**: 22749.44 ✅
- **TP 4RR**: 22919.25 ✅
- **TP 15RR**: 24787.15 ❌
- **PnL**: -169.81 points (-1.0R)
- **MFE**: 770.91 points
- **MAE**: 183.00 points

### Trade #227 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-09 17:00:00
- **FVG 5m**: 22223.77 - 22239.49
- **Entrée**: 22240.01 @ 2025-02-09 17:33:00
- **Stop Loss**: 22070.20
- **Risk**: 169.81 points
- **TP 1RR**: 22409.82 ✅
- **TP 2RR**: 22579.63 ✅
- **TP 3RR**: 22749.44 ✅
- **TP 4RR**: 22919.25 ✅
- **TP 15RR**: 24787.15 ❌
- **PnL**: -169.81 points (-1.0R)
- **MFE**: 770.91 points
- **MAE**: 183.00 points

### Trade #228 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-10 06:00:00
- **FVG 5m**: 22401.61 - 22408.06
- **Entrée**: 22400.84 @ 2025-02-10 06:32:00
- **Stop Loss**: 22431.38
- **Risk**: 30.54 points
- **TP 1RR**: 22370.30 ❌
- **TP 2RR**: 22339.76 ❌
- **TP 3RR**: 22309.22 ❌
- **TP 4RR**: 22278.68 ❌
- **TP 15RR**: 21942.73 ❌
- **PnL**: -30.54 points (-1.0R)
- **MFE**: 6.19 points
- **MAE**: 30.93 points

### Trade #229 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-10 08:30:00
- **FVG 5m**: 22470.69 - 22488.73
- **Entrée**: 22488.99 @ 2025-02-10 09:01:00
- **Stop Loss**: 22406.13
- **Risk**: 82.86 points
- **TP 1RR**: 22571.85 ✅
- **TP 2RR**: 22654.71 ❌
- **TP 3RR**: 22737.57 ❌
- **TP 4RR**: 22820.43 ❌
- **TP 15RR**: 23731.90 ❌
- **PnL**: -82.86 points (-1.0R)
- **MFE**: 82.99 points
- **MAE**: 86.09 points

### Trade #230 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 01:45:00
- **FVG 5m**: 22413.21 - 22431.25
- **Entrée**: 22408.31 @ 2025-02-11 01:58:00
- **Stop Loss**: 22450.98
- **Risk**: 42.66 points
- **TP 1RR**: 22365.65 ❌
- **TP 2RR**: 22322.98 ❌
- **TP 3RR**: 22280.32 ❌
- **TP 4RR**: 22237.66 ❌
- **TP 15RR**: 21768.35 ❌
- **PnL**: -42.66 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 43.30 points

### Trade #231 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 08:30:00
- **FVG 5m**: 22491.56 - 22506.26
- **Entrée**: 22516.56 @ 2025-02-11 09:28:00
- **Stop Loss**: 22361.56
- **Risk**: 155.01 points
- **TP 1RR**: 22671.57 ❌
- **TP 2RR**: 22826.58 ❌
- **TP 3RR**: 22981.58 ❌
- **TP 4RR**: 23136.59 ❌
- **TP 15RR**: 24841.66 ❌
- **PnL**: -155.01 points (-1.0R)
- **MFE**: 32.22 points
- **MAE**: 284.03 points

### Trade #232 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 08:30:00
- **FVG 5m**: 22491.56 - 22506.26
- **Entrée**: 22516.56 @ 2025-02-11 09:28:00
- **Stop Loss**: 22361.56
- **Risk**: 155.01 points
- **TP 1RR**: 22671.57 ❌
- **TP 2RR**: 22826.58 ❌
- **TP 3RR**: 22981.58 ❌
- **TP 4RR**: 23136.59 ❌
- **TP 15RR**: 24841.66 ❌
- **PnL**: -155.01 points (-1.0R)
- **MFE**: 32.22 points
- **MAE**: 284.03 points

### Trade #233 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 08:30:00
- **FVG 5m**: 22491.56 - 22506.26
- **Entrée**: 22516.56 @ 2025-02-11 09:28:00
- **Stop Loss**: 22361.56
- **Risk**: 155.01 points
- **TP 1RR**: 22671.57 ❌
- **TP 2RR**: 22826.58 ❌
- **TP 3RR**: 22981.58 ❌
- **TP 4RR**: 23136.59 ❌
- **TP 15RR**: 24841.66 ❌
- **PnL**: -155.01 points (-1.0R)
- **MFE**: 32.22 points
- **MAE**: 284.03 points

### Trade #234 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-11 09:15:00
- **FVG 5m**: 22491.56 - 22506.26
- **Entrée**: 22516.56 @ 2025-02-11 09:28:00
- **Stop Loss**: 22448.37
- **Risk**: 68.19 points
- **TP 1RR**: 22584.76 ❌
- **TP 2RR**: 22652.95 ❌
- **TP 3RR**: 22721.14 ❌
- **TP 4RR**: 22789.33 ❌
- **TP 15RR**: 23539.43 ❌
- **PnL**: -68.19 points (-1.0R)
- **MFE**: 32.22 points
- **MAE**: 73.46 points

### Trade #235 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 10:45:00
- **FVG 5m**: 22466.82 - 22472.49
- **Entrée**: 22465.27 @ 2025-02-11 10:58:00
- **Stop Loss**: 22527.82
- **Risk**: 62.55 points
- **TP 1RR**: 22402.73 ✅
- **TP 2RR**: 22340.18 ✅
- **TP 3RR**: 22277.63 ✅
- **TP 4RR**: 22215.08 ✅
- **TP 15RR**: 21527.04 ❌
- **PnL**: -62.55 points (-1.0R)
- **MFE**: 288.41 points
- **MAE**: 68.56 points

### Trade #236 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-11 10:45:00
- **FVG 5m**: 22466.82 - 22472.49
- **Entrée**: 22465.27 @ 2025-02-11 10:58:00
- **Stop Loss**: 22527.82
- **Risk**: 62.55 points
- **TP 1RR**: 22402.73 ✅
- **TP 2RR**: 22340.18 ✅
- **TP 3RR**: 22277.63 ✅
- **TP 4RR**: 22215.08 ✅
- **TP 15RR**: 21527.04 ❌
- **PnL**: -62.55 points (-1.0R)
- **MFE**: 288.41 points
- **MAE**: 68.56 points

### Trade #237 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 03:30:00
- **FVG 5m**: 22442.59 - 22446.46
- **Entrée**: 22448.78 @ 2025-02-12 04:21:00
- **Stop Loss**: 22416.69
- **Risk**: 32.09 points
- **TP 1RR**: 22480.87 ✅
- **TP 2RR**: 22512.96 ✅
- **TP 3RR**: 22545.05 ❌
- **TP 4RR**: 22577.14 ❌
- **TP 15RR**: 22930.14 ❌
- **PnL**: -32.09 points (-1.0R)
- **MFE**: 77.84 points
- **MAE**: 216.25 points

### Trade #238 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 03:30:00
- **FVG 5m**: 22442.59 - 22446.46
- **Entrée**: 22448.78 @ 2025-02-12 04:21:00
- **Stop Loss**: 22416.69
- **Risk**: 32.09 points
- **TP 1RR**: 22480.87 ✅
- **TP 2RR**: 22512.96 ✅
- **TP 3RR**: 22545.05 ❌
- **TP 4RR**: 22577.14 ❌
- **TP 15RR**: 22930.14 ❌
- **PnL**: -32.09 points (-1.0R)
- **MFE**: 77.84 points
- **MAE**: 216.25 points

### Trade #239 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:00:00
- **FVG 5m**: 22501.62 - 22504.71
- **Entrée**: 22494.14 @ 2025-02-12 07:21:00
- **Stop Loss**: 22536.33
- **Risk**: 42.19 points
- **TP 1RR**: 22451.95 ✅
- **TP 2RR**: 22409.76 ✅
- **TP 3RR**: 22367.57 ✅
- **TP 4RR**: 22325.38 ✅
- **TP 15RR**: 21861.27 ❌
- **PnL**: -42.19 points (-1.0R)
- **MFE**: 317.28 points
- **MAE**: 45.36 points

### Trade #240 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:30:00
- **FVG 5m**: 22303.93 - 22340.27
- **Entrée**: 22292.85 @ 2025-02-12 09:03:00
- **Stop Loss**: 22537.88
- **Risk**: 245.03 points
- **TP 1RR**: 22047.81 ❌
- **TP 2RR**: 21802.78 ❌
- **TP 3RR**: 21557.74 ❌
- **TP 4RR**: 21312.71 ❌
- **TP 15RR**: 18617.32 ❌
- **PnL**: -245.03 points (-1.0R)
- **MFE**: 44.07 points
- **MAE**: 246.66 points

### Trade #241 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:30:00
- **FVG 5m**: 22303.93 - 22340.27
- **Entrée**: 22292.85 @ 2025-02-12 09:03:00
- **Stop Loss**: 22537.88
- **Risk**: 245.03 points
- **TP 1RR**: 22047.81 ❌
- **TP 2RR**: 21802.78 ❌
- **TP 3RR**: 21557.74 ❌
- **TP 4RR**: 21312.71 ❌
- **TP 15RR**: 18617.32 ❌
- **PnL**: -245.03 points (-1.0R)
- **MFE**: 44.07 points
- **MAE**: 246.66 points

### Trade #242 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 07:30:00
- **FVG 5m**: 22303.93 - 22340.27
- **Entrée**: 22292.85 @ 2025-02-12 09:03:00
- **Stop Loss**: 22537.88
- **Risk**: 245.03 points
- **TP 1RR**: 22047.81 ❌
- **TP 2RR**: 21802.78 ❌
- **TP 3RR**: 21557.74 ❌
- **TP 4RR**: 21312.71 ❌
- **TP 15RR**: 18617.32 ❌
- **PnL**: -245.03 points (-1.0R)
- **MFE**: 44.07 points
- **MAE**: 246.66 points

### Trade #243 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 08:30:00
- **FVG 5m**: 22296.71 - 22321.45
- **Entrée**: 22331.76 @ 2025-02-12 08:44:00
- **Stop Loss**: 22192.05
- **Risk**: 139.71 points
- **TP 1RR**: 22471.48 ✅
- **TP 2RR**: 22611.19 ✅
- **TP 3RR**: 22750.91 ✅
- **TP 4RR**: 22890.62 ✅
- **TP 15RR**: 24427.48 ❌
- **PnL**: -139.71 points (-1.0R)
- **MFE**: 679.15 points
- **MAE**: 151.04 points

### Trade #244 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 08:30:00
- **FVG 5m**: 22296.71 - 22321.45
- **Entrée**: 22331.76 @ 2025-02-12 08:44:00
- **Stop Loss**: 22192.05
- **Risk**: 139.71 points
- **TP 1RR**: 22471.48 ✅
- **TP 2RR**: 22611.19 ✅
- **TP 3RR**: 22750.91 ✅
- **TP 4RR**: 22890.62 ✅
- **TP 15RR**: 24427.48 ❌
- **PnL**: -139.71 points (-1.0R)
- **MFE**: 679.15 points
- **MAE**: 151.04 points

### Trade #245 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 08:45:00
- **FVG 5m**: 22293.88 - 22338.72
- **Entrée**: 22343.36 @ 2025-02-12 09:19:00
- **Stop Loss**: 22310.29
- **Risk**: 33.07 points
- **TP 1RR**: 22376.43 ✅
- **TP 2RR**: 22409.50 ✅
- **TP 3RR**: 22442.57 ✅
- **TP 4RR**: 22475.64 ✅
- **TP 15RR**: 22839.39 ✅
- **PnL**: 496.03 points (15.0R)
- **MFE**: 499.25 points
- **MAE**: 27.06 points

### Trade #246 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 10:45:00
- **FVG 5m**: 22425.84 - 22448.01
- **Entrée**: 22452.64 @ 2025-02-12 10:58:00
- **Stop Loss**: 22376.24
- **Risk**: 76.40 points
- **TP 1RR**: 22529.05 ✅
- **TP 2RR**: 22605.45 ✅
- **TP 3RR**: 22681.85 ✅
- **TP 4RR**: 22758.25 ✅
- **TP 15RR**: 23598.68 ❌
- **PnL**: -76.40 points (-1.0R)
- **MFE**: 558.27 points
- **MAE**: 85.57 points

### Trade #247 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-12 11:45:00
- **FVG 5m**: 22478.16 - 22480.74
- **Entrée**: 22483.06 @ 2025-02-12 13:37:00
- **Stop Loss**: 22424.16
- **Risk**: 58.90 points
- **TP 1RR**: 22541.96 ✅
- **TP 2RR**: 22600.86 ✅
- **TP 3RR**: 22659.76 ✅
- **TP 4RR**: 22718.66 ✅
- **TP 15RR**: 23366.56 ❌
- **PnL**: -58.90 points (-1.0R)
- **MFE**: 527.85 points
- **MAE**: 59.54 points

### Trade #248 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 19:15:00
- **FVG 5m**: 22565.28 - 22568.37
- **Entrée**: 22556.77 @ 2025-02-12 20:05:00
- **Stop Loss**: 22588.16
- **Risk**: 31.39 points
- **TP 1RR**: 22525.38 ❌
- **TP 2RR**: 22493.99 ❌
- **TP 3RR**: 22462.60 ❌
- **TP 4RR**: 22431.20 ❌
- **TP 15RR**: 22085.89 ❌
- **PnL**: -31.39 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 34.28 points

### Trade #249 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-12 19:45:00
- **FVG 5m**: 22565.28 - 22568.37
- **Entrée**: 22556.77 @ 2025-02-12 20:05:00
- **Stop Loss**: 22594.61
- **Risk**: 37.84 points
- **TP 1RR**: 22518.93 ❌
- **TP 2RR**: 22481.09 ❌
- **TP 3RR**: 22443.26 ❌
- **TP 4RR**: 22405.42 ❌
- **TP 15RR**: 21989.19 ❌
- **PnL**: -37.84 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 46.39 points

### Trade #250 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 01:30:00
- **FVG 5m**: 22505.22 - 22518.63
- **Entrée**: 22504.71 @ 2025-02-13 02:14:00
- **Stop Loss**: 22575.01
- **Risk**: 70.30 points
- **TP 1RR**: 22434.40 ✅
- **TP 2RR**: 22364.10 ❌
- **TP 3RR**: 22293.79 ❌
- **TP 4RR**: 22223.49 ❌
- **TP 15RR**: 21450.14 ❌
- **PnL**: -70.30 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 74.23 points

### Trade #251 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 02:00:00
- **FVG 5m**: 22505.22 - 22518.63
- **Entrée**: 22504.71 @ 2025-02-13 02:14:00
- **Stop Loss**: 22549.74
- **Risk**: 45.03 points
- **TP 1RR**: 22459.68 ✅
- **TP 2RR**: 22414.64 ❌
- **TP 3RR**: 22369.61 ❌
- **TP 4RR**: 22324.58 ❌
- **TP 15RR**: 21829.21 ❌
- **PnL**: -45.03 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 74.23 points

### Trade #252 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 02:00:00
- **FVG 5m**: 22505.22 - 22518.63
- **Entrée**: 22504.71 @ 2025-02-13 02:14:00
- **Stop Loss**: 22549.74
- **Risk**: 45.03 points
- **TP 1RR**: 22459.68 ✅
- **TP 2RR**: 22414.64 ❌
- **TP 3RR**: 22369.61 ❌
- **TP 4RR**: 22324.58 ❌
- **TP 15RR**: 21829.21 ❌
- **PnL**: -45.03 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 74.23 points

### Trade #253 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 02:00:00
- **FVG 5m**: 22505.22 - 22518.63
- **Entrée**: 22504.71 @ 2025-02-13 02:14:00
- **Stop Loss**: 22549.74
- **Risk**: 45.03 points
- **TP 1RR**: 22459.68 ✅
- **TP 2RR**: 22414.64 ❌
- **TP 3RR**: 22369.61 ❌
- **TP 4RR**: 22324.58 ❌
- **TP 15RR**: 21829.21 ❌
- **PnL**: -45.03 points (-1.0R)
- **MFE**: 78.10 points
- **MAE**: 74.23 points

### Trade #254 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 02:30:00
- **FVG 5m**: 22462.70 - 22470.43
- **Entrée**: 22476.61 @ 2025-02-13 03:12:00
- **Stop Loss**: 22426.99
- **Risk**: 49.62 points
- **TP 1RR**: 22526.24 ✅
- **TP 2RR**: 22575.86 ✅
- **TP 3RR**: 22625.48 ✅
- **TP 4RR**: 22675.11 ✅
- **TP 15RR**: 23220.95 ❌
- **PnL**: -49.62 points (-1.0R)
- **MFE**: 534.30 points
- **MAE**: 50.00 points

### Trade #255 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 03:30:00
- **FVG 5m**: 22512.96 - 22523.52
- **Entrée**: 22507.54 @ 2025-02-13 05:46:00
- **Stop Loss**: 22526.02
- **Risk**: 18.47 points
- **TP 1RR**: 22489.07 ✅
- **TP 2RR**: 22470.60 ✅
- **TP 3RR**: 22452.12 ❌
- **TP 4RR**: 22433.65 ❌
- **TP 15RR**: 22230.43 ❌
- **PnL**: -18.47 points (-1.0R)
- **MFE**: 44.85 points
- **MAE**: 71.39 points

### Trade #256 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 07:30:00
- **FVG 5m**: 22572.75 - 22592.08
- **Entrée**: 22593.37 @ 2025-02-13 08:56:00
- **Stop Loss**: 22450.69
- **Risk**: 142.68 points
- **TP 1RR**: 22736.05 ✅
- **TP 2RR**: 22878.73 ✅
- **TP 3RR**: 23021.41 ❌
- **TP 4RR**: 23164.09 ❌
- **TP 15RR**: 24733.56 ❌
- **PnL**: -142.68 points (-1.0R)
- **MFE**: 417.54 points
- **MAE**: 143.30 points

### Trade #257 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 09:15:00
- **FVG 5m**: 22676.11 - 22710.90
- **Entrée**: 22713.99 @ 2025-02-13 09:39:00
- **Stop Loss**: 22602.17
- **Risk**: 111.83 points
- **TP 1RR**: 22825.82 ❌
- **TP 2RR**: 22937.65 ❌
- **TP 3RR**: 23049.47 ❌
- **TP 4RR**: 23161.30 ❌
- **TP 15RR**: 24391.38 ❌
- **PnL**: -111.83 points (-1.0R)
- **MFE**: 26.81 points
- **MAE**: 145.62 points

### Trade #258 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 10:45:00
- **FVG 5m**: 22649.56 - 22655.75
- **Entrée**: 22641.57 @ 2025-02-13 11:57:00
- **Stop Loss**: 22701.89
- **Risk**: 60.32 points
- **TP 1RR**: 22581.25 ✅
- **TP 2RR**: 22520.94 ❌
- **TP 3RR**: 22460.62 ❌
- **TP 4RR**: 22400.30 ❌
- **TP 15RR**: 21736.83 ❌
- **PnL**: -60.32 points (-1.0R)
- **MFE**: 73.20 points
- **MAE**: 64.95 points

### Trade #259 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 10:45:00
- **FVG 5m**: 22649.56 - 22655.75
- **Entrée**: 22641.57 @ 2025-02-13 11:57:00
- **Stop Loss**: 22701.89
- **Risk**: 60.32 points
- **TP 1RR**: 22581.25 ✅
- **TP 2RR**: 22520.94 ❌
- **TP 3RR**: 22460.62 ❌
- **TP 4RR**: 22400.30 ❌
- **TP 15RR**: 21736.83 ❌
- **PnL**: -60.32 points (-1.0R)
- **MFE**: 73.20 points
- **MAE**: 64.95 points

### Trade #260 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 12:30:00
- **FVG 5m**: 22658.32 - 22668.89
- **Entrée**: 22669.15 @ 2025-02-13 12:57:00
- **Stop Loss**: 22577.18
- **Risk**: 91.97 points
- **TP 1RR**: 22761.12 ✅
- **TP 2RR**: 22853.08 ✅
- **TP 3RR**: 22945.05 ✅
- **TP 4RR**: 23037.02 ❌
- **TP 15RR**: 24048.66 ❌
- **PnL**: -91.97 points (-1.0R)
- **MFE**: 341.77 points
- **MAE**: 98.97 points

### Trade #261 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-13 12:45:00
- **FVG 5m**: 22658.32 - 22668.89
- **Entrée**: 22669.15 @ 2025-02-13 12:57:00
- **Stop Loss**: 22597.02
- **Risk**: 72.13 points
- **TP 1RR**: 22741.28 ✅
- **TP 2RR**: 22813.41 ✅
- **TP 3RR**: 22885.54 ✅
- **TP 4RR**: 22957.67 ✅
- **TP 15RR**: 23751.12 ❌
- **PnL**: -72.13 points (-1.0R)
- **MFE**: 341.77 points
- **MAE**: 82.99 points

### Trade #262 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 13:45:00
- **FVG 5m**: 22764.25 - 22766.57
- **Entrée**: 22761.93 @ 2025-02-13 15:19:00
- **Stop Loss**: 22770.48
- **Risk**: 8.54 points
- **TP 1RR**: 22753.39 ❌
- **TP 2RR**: 22744.85 ❌
- **TP 3RR**: 22736.30 ❌
- **TP 4RR**: 22727.76 ❌
- **TP 15RR**: 22633.77 ❌
- **PnL**: -8.54 points (-1.0R)
- **MFE**: 4.90 points
- **MAE**: 9.02 points

### Trade #263 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 15:00:00
- **FVG 5m**: 22764.25 - 22766.57
- **Entrée**: 22761.93 @ 2025-02-13 15:19:00
- **Stop Loss**: 22806.58
- **Risk**: 44.65 points
- **TP 1RR**: 22717.29 ❌
- **TP 2RR**: 22672.64 ❌
- **TP 3RR**: 22628.00 ❌
- **TP 4RR**: 22583.35 ❌
- **TP 15RR**: 22092.24 ❌
- **PnL**: -44.65 points (-1.0R)
- **MFE**: 8.51 points
- **MAE**: 55.16 points

### Trade #264 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-13 15:45:00
- **FVG 5m**: 22769.41 - 22779.46
- **Entrée**: 22766.57 @ 2025-02-13 17:34:00
- **Stop Loss**: 22786.98
- **Risk**: 20.41 points
- **TP 1RR**: 22746.17 ❌
- **TP 2RR**: 22725.76 ❌
- **TP 3RR**: 22705.35 ❌
- **TP 4RR**: 22684.94 ❌
- **TP 15RR**: 22460.44 ❌
- **PnL**: -20.41 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 22.94 points

### Trade #265 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-14 06:00:00
- **FVG 5m**: 22748.02 - 22759.36
- **Entrée**: 22760.39 @ 2025-02-14 06:12:00
- **Stop Loss**: 22727.88
- **Risk**: 32.50 points
- **TP 1RR**: 22792.89 ✅
- **TP 2RR**: 22825.40 ✅
- **TP 3RR**: 22857.90 ✅
- **TP 4RR**: 22890.41 ✅
- **TP 15RR**: 23247.96 ❌
- **PnL**: -32.50 points (-1.0R)
- **MFE**: 250.52 points
- **MAE**: 37.89 points

### Trade #266 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-14 07:30:00
- **FVG 5m**: 22794.93 - 22804.46
- **Entrée**: 22807.30 @ 2025-02-14 08:47:00
- **Stop Loss**: 22748.75
- **Risk**: 58.55 points
- **TP 1RR**: 22865.84 ✅
- **TP 2RR**: 22924.39 ✅
- **TP 3RR**: 22982.94 ✅
- **TP 4RR**: 23041.48 ❌
- **TP 15RR**: 23685.50 ❌
- **PnL**: -58.55 points (-1.0R)
- **MFE**: 203.62 points
- **MAE**: 84.80 points

### Trade #267 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-17 02:15:00
- **FVG 5m**: 22927.66 - 22933.33
- **Entrée**: 22926.89 @ 2025-02-17 02:28:00
- **Stop Loss**: 22955.63
- **Risk**: 28.74 points
- **TP 1RR**: 22898.15 ❌
- **TP 2RR**: 22869.41 ❌
- **TP 3RR**: 22840.67 ❌
- **TP 4RR**: 22811.93 ❌
- **TP 15RR**: 22495.78 ❌
- **PnL**: -28.74 points (-1.0R)
- **MFE**: 13.66 points
- **MAE**: 30.67 points

### Trade #268 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 05:30:00
- **FVG 5m**: 22965.29 - 22968.39
- **Entrée**: 22964.78 @ 2025-02-18 05:42:00
- **Stop Loss**: 22988.12
- **Risk**: 23.34 points
- **TP 1RR**: 22941.43 ❌
- **TP 2RR**: 22918.09 ❌
- **TP 3RR**: 22894.74 ❌
- **TP 4RR**: 22871.40 ❌
- **TP 15RR**: 22614.61 ❌
- **PnL**: -23.34 points (-1.0R)
- **MFE**: 7.99 points
- **MAE**: 25.77 points

### Trade #269 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22957.56 - 22994.42
- **Entrée**: 22954.98 @ 2025-02-18 08:28:00
- **Stop Loss**: 23016.49
- **Risk**: 61.50 points
- **TP 1RR**: 22893.48 ✅
- **TP 2RR**: 22831.97 ✅
- **TP 3RR**: 22770.47 ✅
- **TP 4RR**: 22708.97 ✅
- **TP 15RR**: 22032.42 ✅
- **PnL**: 922.57 points (15.0R)
- **MFE**: 925.29 points
- **MAE**: 35.31 points

### Trade #270 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22957.56 - 22994.42
- **Entrée**: 22954.98 @ 2025-02-18 08:28:00
- **Stop Loss**: 23016.49
- **Risk**: 61.50 points
- **TP 1RR**: 22893.48 ✅
- **TP 2RR**: 22831.97 ✅
- **TP 3RR**: 22770.47 ✅
- **TP 4RR**: 22708.97 ✅
- **TP 15RR**: 22032.42 ✅
- **PnL**: 922.57 points (15.0R)
- **MFE**: 925.29 points
- **MAE**: 35.31 points

### Trade #271 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22957.56 - 22994.42
- **Entrée**: 22954.98 @ 2025-02-18 08:28:00
- **Stop Loss**: 23016.49
- **Risk**: 61.50 points
- **TP 1RR**: 22893.48 ✅
- **TP 2RR**: 22831.97 ✅
- **TP 3RR**: 22770.47 ✅
- **TP 4RR**: 22708.97 ✅
- **TP 15RR**: 22032.42 ✅
- **PnL**: 922.57 points (15.0R)
- **MFE**: 925.29 points
- **MAE**: 35.31 points

### Trade #272 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:15:00
- **FVG 5m**: 22957.56 - 22994.42
- **Entrée**: 22954.98 @ 2025-02-18 08:28:00
- **Stop Loss**: 23016.49
- **Risk**: 61.50 points
- **TP 1RR**: 22893.48 ✅
- **TP 2RR**: 22831.97 ✅
- **TP 3RR**: 22770.47 ✅
- **TP 4RR**: 22708.97 ✅
- **TP 15RR**: 22032.42 ✅
- **PnL**: 922.57 points (15.0R)
- **MFE**: 925.29 points
- **MAE**: 35.31 points

### Trade #273 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 08:30:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22969.04
- **Risk**: 95.76 points
- **TP 1RR**: 22777.52 ❌
- **TP 2RR**: 22681.76 ❌
- **TP 3RR**: 22586.00 ❌
- **TP 4RR**: 22490.24 ❌
- **TP 15RR**: 21436.87 ❌
- **PnL**: -95.76 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 97.68 points

### Trade #274 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 08:45:00
- **FVG 5m**: 22854.46 - 22856.78
- **Entrée**: 22859.36 @ 2025-02-18 09:52:00
- **Stop Loss**: 22839.95
- **Risk**: 19.42 points
- **TP 1RR**: 22878.78 ✅
- **TP 2RR**: 22898.19 ✅
- **TP 3RR**: 22917.61 ❌
- **TP 4RR**: 22937.02 ❌
- **TP 15RR**: 23150.60 ❌
- **PnL**: -19.42 points (-1.0R)
- **MFE**: 44.33 points
- **MAE**: 21.39 points

### Trade #275 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 08:45:00
- **FVG 5m**: 22854.46 - 22856.78
- **Entrée**: 22859.36 @ 2025-02-18 09:52:00
- **Stop Loss**: 22839.95
- **Risk**: 19.42 points
- **TP 1RR**: 22878.78 ✅
- **TP 2RR**: 22898.19 ✅
- **TP 3RR**: 22917.61 ❌
- **TP 4RR**: 22937.02 ❌
- **TP 15RR**: 23150.60 ❌
- **PnL**: -19.42 points (-1.0R)
- **MFE**: 44.33 points
- **MAE**: 21.39 points

### Trade #276 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22906.38
- **Risk**: 33.10 points
- **TP 1RR**: 22840.18 ✅
- **TP 2RR**: 22807.08 ✅
- **TP 3RR**: 22773.99 ❌
- **TP 4RR**: 22740.89 ❌
- **TP 15RR**: 22376.81 ❌
- **PnL**: -33.10 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 40.72 points

### Trade #277 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22906.38
- **Risk**: 33.10 points
- **TP 1RR**: 22840.18 ✅
- **TP 2RR**: 22807.08 ✅
- **TP 3RR**: 22773.99 ❌
- **TP 4RR**: 22740.89 ❌
- **TP 15RR**: 22376.81 ❌
- **PnL**: -33.10 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 40.72 points

### Trade #278 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22906.38
- **Risk**: 33.10 points
- **TP 1RR**: 22840.18 ✅
- **TP 2RR**: 22807.08 ✅
- **TP 3RR**: 22773.99 ❌
- **TP 4RR**: 22740.89 ❌
- **TP 15RR**: 22376.81 ❌
- **PnL**: -33.10 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 40.72 points

### Trade #279 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22906.38
- **Risk**: 33.10 points
- **TP 1RR**: 22840.18 ✅
- **TP 2RR**: 22807.08 ✅
- **TP 3RR**: 22773.99 ❌
- **TP 4RR**: 22740.89 ❌
- **TP 15RR**: 22376.81 ❌
- **PnL**: -33.10 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 40.72 points

### Trade #280 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-18 09:15:00
- **FVG 5m**: 22877.92 - 22891.06
- **Entrée**: 22873.28 @ 2025-02-18 10:59:00
- **Stop Loss**: 22906.38
- **Risk**: 33.10 points
- **TP 1RR**: 22840.18 ✅
- **TP 2RR**: 22807.08 ✅
- **TP 3RR**: 22773.99 ❌
- **TP 4RR**: 22740.89 ❌
- **TP 15RR**: 22376.81 ❌
- **PnL**: -33.10 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 40.72 points

### Trade #281 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 13:15:00
- **FVG 5m**: 22849.31 - 22855.75
- **Entrée**: 22861.68 @ 2025-02-18 13:49:00
- **Stop Loss**: 22777.60
- **Risk**: 84.08 points
- **TP 1RR**: 22945.76 ✅
- **TP 2RR**: 23029.84 ❌
- **TP 3RR**: 23113.91 ❌
- **TP 4RR**: 23197.99 ❌
- **TP 15RR**: 24122.85 ❌
- **PnL**: -84.08 points (-1.0R)
- **MFE**: 128.61 points
- **MAE**: 88.15 points

### Trade #282 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 14:45:00
- **FVG 5m**: 22886.42 - 22921.99
- **Entrée**: 22927.41 @ 2025-02-18 14:59:00
- **Stop Loss**: 22836.60
- **Risk**: 90.81 points
- **TP 1RR**: 23018.21 ❌
- **TP 2RR**: 23109.02 ❌
- **TP 3RR**: 23199.83 ❌
- **TP 4RR**: 23290.64 ❌
- **TP 15RR**: 24289.53 ❌
- **PnL**: -90.81 points (-1.0R)
- **MFE**: 54.13 points
- **MAE**: 94.33 points

### Trade #283 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-18 14:45:00
- **FVG 5m**: 22886.42 - 22921.99
- **Entrée**: 22927.41 @ 2025-02-18 14:59:00
- **Stop Loss**: 22836.60
- **Risk**: 90.81 points
- **TP 1RR**: 23018.21 ❌
- **TP 2RR**: 23109.02 ❌
- **TP 3RR**: 23199.83 ❌
- **TP 4RR**: 23290.64 ❌
- **TP 15RR**: 24289.53 ❌
- **PnL**: -90.81 points (-1.0R)
- **MFE**: 54.13 points
- **MAE**: 94.33 points

### Trade #284 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 07:15:00
- **FVG 5m**: 22884.36 - 22890.03
- **Entrée**: 22891.84 @ 2025-02-19 07:48:00
- **Stop Loss**: 22854.89
- **Risk**: 36.95 points
- **TP 1RR**: 22928.79 ❌
- **TP 2RR**: 22965.74 ❌
- **TP 3RR**: 23002.69 ❌
- **TP 4RR**: 23039.64 ❌
- **TP 15RR**: 23446.08 ❌
- **PnL**: -36.95 points (-1.0R)
- **MFE**: 17.78 points
- **MAE**: 51.03 points

### Trade #285 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 12:00:00
- **FVG 5m**: 22935.40 - 22938.75
- **Entrée**: 22934.36 @ 2025-02-19 12:48:00
- **Stop Loss**: 22947.89
- **Risk**: 13.53 points
- **TP 1RR**: 22920.83 ✅
- **TP 2RR**: 22907.30 ❌
- **TP 3RR**: 22893.77 ❌
- **TP 4RR**: 22880.24 ❌
- **TP 15RR**: 22731.41 ❌
- **PnL**: -13.53 points (-1.0R)
- **MFE**: 19.85 points
- **MAE**: 25.52 points

### Trade #286 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22903.06
- **Risk**: 56.56 points
- **TP 1RR**: 23016.18 ❌
- **TP 2RR**: 23072.75 ❌
- **TP 3RR**: 23129.31 ❌
- **TP 4RR**: 23185.87 ❌
- **TP 15RR**: 23808.05 ❌
- **PnL**: -56.56 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 66.50 points

### Trade #287 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22903.06
- **Risk**: 56.56 points
- **TP 1RR**: 23016.18 ❌
- **TP 2RR**: 23072.75 ❌
- **TP 3RR**: 23129.31 ❌
- **TP 4RR**: 23185.87 ❌
- **TP 15RR**: 23808.05 ❌
- **PnL**: -56.56 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 66.50 points

### Trade #288 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22903.06
- **Risk**: 56.56 points
- **TP 1RR**: 23016.18 ❌
- **TP 2RR**: 23072.75 ❌
- **TP 3RR**: 23129.31 ❌
- **TP 4RR**: 23185.87 ❌
- **TP 15RR**: 23808.05 ❌
- **PnL**: -56.56 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 66.50 points

### Trade #289 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22903.06
- **Risk**: 56.56 points
- **TP 1RR**: 23016.18 ❌
- **TP 2RR**: 23072.75 ❌
- **TP 3RR**: 23129.31 ❌
- **TP 4RR**: 23185.87 ❌
- **TP 15RR**: 23808.05 ❌
- **PnL**: -56.56 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 66.50 points

### Trade #290 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22903.06
- **Risk**: 56.56 points
- **TP 1RR**: 23016.18 ❌
- **TP 2RR**: 23072.75 ❌
- **TP 3RR**: 23129.31 ❌
- **TP 4RR**: 23185.87 ❌
- **TP 15RR**: 23808.05 ❌
- **PnL**: -56.56 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 66.50 points

### Trade #291 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-19 13:00:00
- **FVG 5m**: 22935.14 - 22954.47
- **Entrée**: 22959.62 @ 2025-02-19 13:14:00
- **Stop Loss**: 22903.06
- **Risk**: 56.56 points
- **TP 1RR**: 23016.18 ❌
- **TP 2RR**: 23072.75 ❌
- **TP 3RR**: 23129.31 ❌
- **TP 4RR**: 23185.87 ❌
- **TP 15RR**: 23808.05 ❌
- **PnL**: -56.56 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 66.50 points

### Trade #292 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 13:15:00
- **FVG 5m**: 22973.03 - 22982.56
- **Entrée**: 22970.71 @ 2025-02-19 14:02:00
- **Stop Loss**: 22989.15
- **Risk**: 18.45 points
- **TP 1RR**: 22952.26 ✅
- **TP 2RR**: 22933.81 ✅
- **TP 3RR**: 22915.36 ✅
- **TP 4RR**: 22896.91 ✅
- **TP 15RR**: 22693.99 ✅
- **PnL**: 276.72 points (15.0R)
- **MFE**: 288.93 points
- **MAE**: 4.90 points

### Trade #293 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 14:00:00
- **FVG 5m**: 22944.42 - 22947.77
- **Entrée**: 22938.23 @ 2025-02-19 14:26:00
- **Stop Loss**: 22997.15
- **Risk**: 58.92 points
- **TP 1RR**: 22879.31 ✅
- **TP 2RR**: 22820.40 ✅
- **TP 3RR**: 22761.48 ✅
- **TP 4RR**: 22702.56 ✅
- **TP 15RR**: 22054.47 ✅
- **PnL**: 883.76 points (15.0R)
- **MFE**: 885.34 points
- **MAE**: 9.54 points

### Trade #294 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-19 14:15:00
- **FVG 5m**: 22944.42 - 22947.77
- **Entrée**: 22938.23 @ 2025-02-19 14:26:00
- **Stop Loss**: 22984.77
- **Risk**: 46.54 points
- **TP 1RR**: 22891.69 ✅
- **TP 2RR**: 22845.15 ✅
- **TP 3RR**: 22798.61 ✅
- **TP 4RR**: 22752.07 ✅
- **TP 15RR**: 22240.14 ✅
- **PnL**: 698.09 points (15.0R)
- **MFE**: 698.22 points
- **MAE**: 9.54 points

### Trade #295 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 01:15:00
- **FVG 5m**: 22852.40 - 22861.94
- **Entrée**: 22868.90 @ 2025-02-20 02:28:00
- **Stop Loss**: 22825.52
- **Risk**: 43.38 points
- **TP 1RR**: 22912.28 ✅
- **TP 2RR**: 22955.65 ❌
- **TP 3RR**: 22999.03 ❌
- **TP 4RR**: 23042.41 ❌
- **TP 15RR**: 23519.57 ❌
- **PnL**: -43.38 points (-1.0R)
- **MFE**: 44.85 points
- **MAE**: 44.59 points

### Trade #296 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 06:45:00
- **FVG 5m**: 22886.68 - 22889.52
- **Entrée**: 22891.06 @ 2025-02-20 07:59:00
- **Stop Loss**: 22869.31
- **Risk**: 21.75 points
- **TP 1RR**: 22912.81 ✅
- **TP 2RR**: 22934.56 ❌
- **TP 3RR**: 22956.31 ❌
- **TP 4RR**: 22978.06 ❌
- **TP 15RR**: 23217.31 ❌
- **PnL**: -21.75 points (-1.0R)
- **MFE**: 22.68 points
- **MAE**: 24.23 points

### Trade #297 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-20 08:45:00
- **FVG 5m**: 22719.92 - 22722.50
- **Entrée**: 22714.77 @ 2025-02-20 08:58:00
- **Stop Loss**: 22871.82
- **Risk**: 157.05 points
- **TP 1RR**: 22557.71 ❌
- **TP 2RR**: 22400.66 ❌
- **TP 3RR**: 22243.61 ❌
- **TP 4RR**: 22086.55 ❌
- **TP 15RR**: 20358.96 ❌
- **PnL**: -157.05 points (-1.0R)
- **MFE**: 84.02 points
- **MAE**: 161.86 points

### Trade #298 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 10:00:00
- **FVG 5m**: 22724.30 - 22744.92
- **Entrée**: 22747.24 @ 2025-02-20 11:04:00
- **Stop Loss**: 22652.92
- **Risk**: 94.32 points
- **TP 1RR**: 22841.57 ✅
- **TP 2RR**: 22935.89 ❌
- **TP 3RR**: 23030.22 ❌
- **TP 4RR**: 23124.54 ❌
- **TP 15RR**: 24162.12 ❌
- **PnL**: -94.32 points (-1.0R)
- **MFE**: 187.12 points
- **MAE**: 102.58 points

### Trade #299 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-20 13:15:00
- **FVG 5m**: 22780.75 - 22786.16
- **Entrée**: 22777.66 @ 2025-02-20 13:27:00
- **Stop Loss**: 22809.42
- **Risk**: 31.76 points
- **TP 1RR**: 22745.90 ✅
- **TP 2RR**: 22714.14 ❌
- **TP 3RR**: 22682.38 ❌
- **TP 4RR**: 22650.61 ❌
- **TP 15RR**: 22301.25 ❌
- **PnL**: -31.76 points (-1.0R)
- **MFE**: 38.66 points
- **MAE**: 35.31 points

### Trade #300 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 13:45:00
- **FVG 5m**: 22824.82 - 22828.69
- **Entrée**: 22831.53 @ 2025-02-20 17:02:00
- **Stop Loss**: 22749.27
- **Risk**: 82.26 points
- **TP 1RR**: 22913.78 ✅
- **TP 2RR**: 22996.04 ❌
- **TP 3RR**: 23078.30 ❌
- **TP 4RR**: 23160.56 ❌
- **TP 15RR**: 24065.41 ❌
- **PnL**: -82.26 points (-1.0R)
- **MFE**: 102.84 points
- **MAE**: 101.81 points

### Trade #301 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-20 14:45:00
- **FVG 5m**: 22824.82 - 22828.69
- **Entrée**: 22831.53 @ 2025-02-20 17:02:00
- **Stop Loss**: 22781.47
- **Risk**: 50.06 points
- **TP 1RR**: 22881.58 ✅
- **TP 2RR**: 22931.64 ✅
- **TP 3RR**: 22981.70 ❌
- **TP 4RR**: 23031.76 ❌
- **TP 15RR**: 23582.39 ❌
- **PnL**: -50.06 points (-1.0R)
- **MFE**: 102.84 points
- **MAE**: 57.48 points

### Trade #302 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 02:15:00
- **FVG 5m**: 22837.20 - 22841.06
- **Entrée**: 22845.19 @ 2025-02-21 03:19:00
- **Stop Loss**: 22776.83
- **Risk**: 68.36 points
- **TP 1RR**: 22913.54 ✅
- **TP 2RR**: 22981.90 ❌
- **TP 3RR**: 23050.25 ❌
- **TP 4RR**: 23118.61 ❌
- **TP 15RR**: 23870.51 ❌
- **PnL**: -68.36 points (-1.0R)
- **MFE**: 89.18 points
- **MAE**: 71.14 points

### Trade #303 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 02:15:00
- **FVG 5m**: 22837.20 - 22841.06
- **Entrée**: 22845.19 @ 2025-02-21 03:19:00
- **Stop Loss**: 22776.83
- **Risk**: 68.36 points
- **TP 1RR**: 22913.54 ✅
- **TP 2RR**: 22981.90 ❌
- **TP 3RR**: 23050.25 ❌
- **TP 4RR**: 23118.61 ❌
- **TP 15RR**: 23870.51 ❌
- **PnL**: -68.36 points (-1.0R)
- **MFE**: 89.18 points
- **MAE**: 71.14 points

### Trade #304 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 06:00:00
- **FVG 5m**: 22870.19 - 22880.24
- **Entrée**: 22881.27 @ 2025-02-21 06:19:00
- **Stop Loss**: 22831.44
- **Risk**: 49.82 points
- **TP 1RR**: 22931.09 ✅
- **TP 2RR**: 22980.92 ❌
- **TP 3RR**: 23030.74 ❌
- **TP 4RR**: 23080.57 ❌
- **TP 15RR**: 23628.64 ❌
- **PnL**: -49.82 points (-1.0R)
- **MFE**: 53.09 points
- **MAE**: 62.12 points

### Trade #305 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-21 06:15:00
- **FVG 5m**: 22896.73 - 22900.34
- **Entrée**: 22903.69 @ 2025-02-21 06:42:00
- **Stop Loss**: 22853.34
- **Risk**: 50.35 points
- **TP 1RR**: 22954.04 ❌
- **TP 2RR**: 23004.40 ❌
- **TP 3RR**: 23054.75 ❌
- **TP 4RR**: 23105.10 ❌
- **TP 15RR**: 23658.96 ❌
- **PnL**: -50.35 points (-1.0R)
- **MFE**: 30.67 points
- **MAE**: 59.54 points

### Trade #306 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 07:45:00
- **FVG 5m**: 22875.08 - 22900.08
- **Entrée**: 22872.76 @ 2025-02-21 08:29:00
- **Stop Loss**: 22945.83
- **Risk**: 73.07 points
- **TP 1RR**: 22799.70 ✅
- **TP 2RR**: 22726.63 ✅
- **TP 3RR**: 22653.56 ✅
- **TP 4RR**: 22580.49 ✅
- **TP 15RR**: 21776.75 ✅
- **PnL**: 1096.01 points (15.0R)
- **MFE**: 1106.23 points
- **MAE**: 2.32 points

### Trade #307 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 07:45:00
- **FVG 5m**: 22875.08 - 22900.08
- **Entrée**: 22872.76 @ 2025-02-21 08:29:00
- **Stop Loss**: 22945.83
- **Risk**: 73.07 points
- **TP 1RR**: 22799.70 ✅
- **TP 2RR**: 22726.63 ✅
- **TP 3RR**: 22653.56 ✅
- **TP 4RR**: 22580.49 ✅
- **TP 15RR**: 21776.75 ✅
- **PnL**: 1096.01 points (15.0R)
- **MFE**: 1106.23 points
- **MAE**: 2.32 points

### Trade #308 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:15:00
- **FVG 5m**: 22875.08 - 22900.08
- **Entrée**: 22872.76 @ 2025-02-21 08:29:00
- **Stop Loss**: 22932.42
- **Risk**: 59.66 points
- **TP 1RR**: 22813.11 ✅
- **TP 2RR**: 22753.45 ✅
- **TP 3RR**: 22693.79 ✅
- **TP 4RR**: 22634.13 ✅
- **TP 15RR**: 21977.89 ✅
- **PnL**: 894.87 points (15.0R)
- **MFE**: 906.99 points
- **MAE**: 2.32 points

### Trade #309 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:30:00
- **FVG 5m**: 22721.73 - 22747.76
- **Entrée**: 22717.09 @ 2025-02-21 09:23:00
- **Stop Loss**: 22886.52
- **Risk**: 169.43 points
- **TP 1RR**: 22547.65 ✅
- **TP 2RR**: 22378.22 ✅
- **TP 3RR**: 22208.79 ✅
- **TP 4RR**: 22039.36 ✅
- **TP 15RR**: 20175.59 ✅
- **PnL**: 2541.50 points (15.0R)
- **MFE**: 2543.14 points
- **MAE**: 4.64 points

### Trade #310 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:30:00
- **FVG 5m**: 22721.73 - 22747.76
- **Entrée**: 22717.09 @ 2025-02-21 09:23:00
- **Stop Loss**: 22886.52
- **Risk**: 169.43 points
- **TP 1RR**: 22547.65 ✅
- **TP 2RR**: 22378.22 ✅
- **TP 3RR**: 22208.79 ✅
- **TP 4RR**: 22039.36 ✅
- **TP 15RR**: 20175.59 ✅
- **PnL**: 2541.50 points (15.0R)
- **MFE**: 2543.14 points
- **MAE**: 4.64 points

### Trade #311 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 08:30:00
- **FVG 5m**: 22721.73 - 22747.76
- **Entrée**: 22717.09 @ 2025-02-21 09:23:00
- **Stop Loss**: 22886.52
- **Risk**: 169.43 points
- **TP 1RR**: 22547.65 ✅
- **TP 2RR**: 22378.22 ✅
- **TP 3RR**: 22208.79 ✅
- **TP 4RR**: 22039.36 ✅
- **TP 15RR**: 20175.59 ✅
- **PnL**: 2541.50 points (15.0R)
- **MFE**: 2543.14 points
- **MAE**: 4.64 points

### Trade #312 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-21 11:45:00
- **FVG 5m**: 22531.00 - 22535.38
- **Entrée**: 22529.19 @ 2025-02-21 11:56:00
- **Stop Loss**: 22585.07
- **Risk**: 55.88 points
- **TP 1RR**: 22473.32 ✅
- **TP 2RR**: 22417.44 ✅
- **TP 3RR**: 22361.57 ✅
- **TP 4RR**: 22305.69 ✅
- **TP 15RR**: 21691.05 ✅
- **PnL**: 838.14 points (15.0R)
- **MFE**: 849.77 points
- **MAE**: 3.61 points

### Trade #313 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-23 19:30:00
- **FVG 5m**: 22421.20 - 22426.87
- **Entrée**: 22433.57 @ 2025-02-23 20:05:00
- **Stop Loss**: 22398.14
- **Risk**: 35.43 points
- **TP 1RR**: 22469.00 ✅
- **TP 2RR**: 22504.44 ❌
- **TP 3RR**: 22539.87 ❌
- **TP 4RR**: 22575.30 ❌
- **TP 15RR**: 22965.06 ❌
- **PnL**: -35.43 points (-1.0R)
- **MFE**: 43.04 points
- **MAE**: 46.39 points

### Trade #314 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 02:15:00
- **FVG 5m**: 22413.21 - 22417.59
- **Entrée**: 22418.37 @ 2025-02-24 02:42:00
- **Stop Loss**: 22361.82
- **Risk**: 56.55 points
- **TP 1RR**: 22474.91 ✅
- **TP 2RR**: 22531.46 ❌
- **TP 3RR**: 22588.01 ❌
- **TP 4RR**: 22644.56 ❌
- **TP 15RR**: 23266.60 ❌
- **PnL**: -56.55 points (-1.0R)
- **MFE**: 70.11 points
- **MAE**: 62.89 points

### Trade #315 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 02:45:00
- **FVG 5m**: 22453.42 - 22457.03
- **Entrée**: 22459.86 @ 2025-02-24 03:01:00
- **Stop Loss**: 22406.38
- **Risk**: 53.48 points
- **TP 1RR**: 22513.34 ❌
- **TP 2RR**: 22566.82 ❌
- **TP 3RR**: 22620.30 ❌
- **TP 4RR**: 22673.78 ❌
- **TP 15RR**: 23262.04 ❌
- **PnL**: -53.48 points (-1.0R)
- **MFE**: 28.61 points
- **MAE**: 55.93 points

### Trade #316 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 02:45:00
- **FVG 5m**: 22453.42 - 22457.03
- **Entrée**: 22459.86 @ 2025-02-24 03:01:00
- **Stop Loss**: 22406.38
- **Risk**: 53.48 points
- **TP 1RR**: 22513.34 ❌
- **TP 2RR**: 22566.82 ❌
- **TP 3RR**: 22620.30 ❌
- **TP 4RR**: 22673.78 ❌
- **TP 15RR**: 23262.04 ❌
- **PnL**: -53.48 points (-1.0R)
- **MFE**: 28.61 points
- **MAE**: 55.93 points

### Trade #317 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-24 03:30:00
- **FVG 5m**: 22451.10 - 22453.42
- **Entrée**: 22450.33 @ 2025-02-24 05:44:00
- **Stop Loss**: 22498.68
- **Risk**: 48.36 points
- **TP 1RR**: 22401.97 ✅
- **TP 2RR**: 22353.61 ✅
- **TP 3RR**: 22305.25 ✅
- **TP 4RR**: 22256.89 ✅
- **TP 15RR**: 21724.95 ✅
- **PnL**: 725.38 points (15.0R)
- **MFE**: 729.67 points
- **MAE**: 30.16 points

### Trade #318 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-24 08:00:00
- **FVG 5m**: 22392.59 - 22403.93
- **Entrée**: 22384.60 @ 2025-02-24 08:37:00
- **Stop Loss**: 22491.72
- **Risk**: 107.12 points
- **TP 1RR**: 22277.48 ✅
- **TP 2RR**: 22170.36 ✅
- **TP 3RR**: 22063.24 ✅
- **TP 4RR**: 21956.12 ✅
- **TP 15RR**: 20777.80 ✅
- **PnL**: 1606.80 points (15.0R)
- **MFE**: 1620.94 points
- **MAE**: 20.88 points

### Trade #319 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 09:00:00
- **FVG 5m**: 22214.75 - 22221.19
- **Entrée**: 22225.57 @ 2025-02-24 10:24:00
- **Stop Loss**: 22089.00
- **Risk**: 136.57 points
- **TP 1RR**: 22362.14 ❌
- **TP 2RR**: 22498.72 ❌
- **TP 3RR**: 22635.29 ❌
- **TP 4RR**: 22771.86 ❌
- **TP 15RR**: 24274.13 ❌
- **PnL**: -136.57 points (-1.0R)
- **MFE**: 105.67 points
- **MAE**: 139.18 points

### Trade #320 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 15:00:00
- **FVG 5m**: 22089.23 - 22093.87
- **Entrée**: 22105.21 @ 2025-02-24 17:00:00
- **Stop Loss**: 22059.38
- **Risk**: 45.83 points
- **TP 1RR**: 22151.04 ❌
- **TP 2RR**: 22196.87 ❌
- **TP 3RR**: 22242.70 ❌
- **TP 4RR**: 22288.53 ❌
- **TP 15RR**: 22792.66 ❌
- **PnL**: -45.83 points (-1.0R)
- **MFE**: 9.28 points
- **MAE**: 48.20 points

### Trade #321 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 18:00:00
- **FVG 5m**: 22084.85 - 22096.19
- **Entrée**: 22112.17 @ 2025-02-24 18:27:00
- **Stop Loss**: 22036.71
- **Risk**: 75.46 points
- **TP 1RR**: 22187.63 ❌
- **TP 2RR**: 22263.09 ❌
- **TP 3RR**: 22338.55 ❌
- **TP 4RR**: 22414.01 ❌
- **TP 15RR**: 23244.06 ❌
- **PnL**: -75.46 points (-1.0R)
- **MFE**: 5.93 points
- **MAE**: 83.77 points

### Trade #322 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 18:00:00
- **FVG 5m**: 22084.85 - 22096.19
- **Entrée**: 22112.17 @ 2025-02-24 18:27:00
- **Stop Loss**: 22036.71
- **Risk**: 75.46 points
- **TP 1RR**: 22187.63 ❌
- **TP 2RR**: 22263.09 ❌
- **TP 3RR**: 22338.55 ❌
- **TP 4RR**: 22414.01 ❌
- **TP 15RR**: 23244.06 ❌
- **PnL**: -75.46 points (-1.0R)
- **MFE**: 5.93 points
- **MAE**: 83.77 points

### Trade #323 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-24 20:15:00
- **FVG 5m**: 22089.49 - 22094.38
- **Entrée**: 22098.25 @ 2025-02-24 22:17:00
- **Stop Loss**: 22048.82
- **Risk**: 49.43 points
- **TP 1RR**: 22147.68 ❌
- **TP 2RR**: 22197.12 ❌
- **TP 3RR**: 22246.55 ❌
- **TP 4RR**: 22295.98 ❌
- **TP 15RR**: 22839.75 ❌
- **PnL**: -49.43 points (-1.0R)
- **MFE**: 10.83 points
- **MAE**: 50.78 points

### Trade #324 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 01:30:00
- **FVG 5m**: 21990.00 - 22009.84
- **Entrée**: 22013.97 @ 2025-02-25 02:04:00
- **Stop Loss**: 21994.98
- **Risk**: 18.99 points
- **TP 1RR**: 22032.96 ✅
- **TP 2RR**: 22051.95 ✅
- **TP 3RR**: 22070.95 ❌
- **TP 4RR**: 22089.94 ❌
- **TP 15RR**: 22298.86 ❌
- **PnL**: -18.99 points (-1.0R)
- **MFE**: 53.87 points
- **MAE**: 20.88 points

### Trade #325 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 05:00:00
- **FVG 5m**: 21982.78 - 21985.36
- **Entrée**: 21986.65 @ 2025-02-25 05:29:00
- **Stop Loss**: 21934.18
- **Risk**: 52.47 points
- **TP 1RR**: 22039.12 ✅
- **TP 2RR**: 22091.59 ✅
- **TP 3RR**: 22144.06 ❌
- **TP 4RR**: 22196.52 ❌
- **TP 15RR**: 22773.68 ❌
- **PnL**: -52.47 points (-1.0R)
- **MFE**: 129.39 points
- **MAE**: 53.87 points

### Trade #326 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 06:45:00
- **FVG 5m**: 22063.46 - 22082.01
- **Entrée**: 22084.59 @ 2025-02-25 06:58:00
- **Stop Loss**: 22013.27
- **Risk**: 71.32 points
- **TP 1RR**: 22155.91 ❌
- **TP 2RR**: 22227.24 ❌
- **TP 3RR**: 22298.56 ❌
- **TP 4RR**: 22369.88 ❌
- **TP 15RR**: 23154.45 ❌
- **PnL**: -71.32 points (-1.0R)
- **MFE**: 31.44 points
- **MAE**: 91.76 points

### Trade #327 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-25 10:45:00
- **FVG 5m**: 21788.70 - 21805.46
- **Entrée**: 21813.96 @ 2025-02-25 10:56:00
- **Stop Loss**: 21701.30
- **Risk**: 112.66 points
- **TP 1RR**: 21926.63 ✅
- **TP 2RR**: 22039.29 ✅
- **TP 3RR**: 22151.95 ❌
- **TP 4RR**: 22264.62 ❌
- **TP 15RR**: 23503.92 ❌
- **PnL**: -112.66 points (-1.0R)
- **MFE**: 258.26 points
- **MAE**: 117.53 points

### Trade #328 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 05:45:00
- **FVG 5m**: 21944.38 - 21951.08
- **Entrée**: 21938.45 @ 2025-02-26 06:49:00
- **Stop Loss**: 21993.00
- **Risk**: 54.55 points
- **TP 1RR**: 21883.90 ❌
- **TP 2RR**: 21829.35 ❌
- **TP 3RR**: 21774.80 ❌
- **TP 4RR**: 21720.25 ❌
- **TP 15RR**: 21120.21 ❌
- **PnL**: -54.55 points (-1.0R)
- **MFE**: 20.62 points
- **MAE**: 54.64 points

### Trade #329 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:00:00
- **FVG 5m**: 21915.51 - 21929.94
- **Entrée**: 21913.19 @ 2025-02-26 08:13:00
- **Stop Loss**: 21956.64
- **Risk**: 43.45 points
- **TP 1RR**: 21869.74 ✅
- **TP 2RR**: 21826.30 ❌
- **TP 3RR**: 21782.85 ❌
- **TP 4RR**: 21739.40 ❌
- **TP 15RR**: 21261.47 ❌
- **PnL**: -43.45 points (-1.0R)
- **MFE**: 68.04 points
- **MAE**: 51.29 points

### Trade #330 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:00:00
- **FVG 5m**: 21915.51 - 21929.94
- **Entrée**: 21913.19 @ 2025-02-26 08:13:00
- **Stop Loss**: 21956.64
- **Risk**: 43.45 points
- **TP 1RR**: 21869.74 ✅
- **TP 2RR**: 21826.30 ❌
- **TP 3RR**: 21782.85 ❌
- **TP 4RR**: 21739.40 ❌
- **TP 15RR**: 21261.47 ❌
- **PnL**: -43.45 points (-1.0R)
- **MFE**: 68.04 points
- **MAE**: 51.29 points

### Trade #331 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 08:00:00
- **FVG 5m**: 21915.51 - 21929.94
- **Entrée**: 21913.19 @ 2025-02-26 08:13:00
- **Stop Loss**: 21956.64
- **Risk**: 43.45 points
- **TP 1RR**: 21869.74 ✅
- **TP 2RR**: 21826.30 ❌
- **TP 3RR**: 21782.85 ❌
- **TP 4RR**: 21739.40 ❌
- **TP 15RR**: 21261.47 ❌
- **PnL**: -43.45 points (-1.0R)
- **MFE**: 68.04 points
- **MAE**: 51.29 points

### Trade #332 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 08:30:00
- **FVG 5m**: 21972.47 - 21975.82
- **Entrée**: 21989.74 @ 2025-02-26 09:12:00
- **Stop Loss**: 21834.23
- **Risk**: 155.52 points
- **TP 1RR**: 22145.26 ❌
- **TP 2RR**: 22300.77 ❌
- **TP 3RR**: 22456.29 ❌
- **TP 4RR**: 22611.80 ❌
- **TP 15RR**: 24322.48 ❌
- **PnL**: -155.52 points (-1.0R)
- **MFE**: 82.48 points
- **MAE**: 163.92 points

### Trade #333 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 08:30:00
- **FVG 5m**: 21972.47 - 21975.82
- **Entrée**: 21989.74 @ 2025-02-26 09:12:00
- **Stop Loss**: 21834.23
- **Risk**: 155.52 points
- **TP 1RR**: 22145.26 ❌
- **TP 2RR**: 22300.77 ❌
- **TP 3RR**: 22456.29 ❌
- **TP 4RR**: 22611.80 ❌
- **TP 15RR**: 24322.48 ❌
- **PnL**: -155.52 points (-1.0R)
- **MFE**: 82.48 points
- **MAE**: 163.92 points

### Trade #334 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 09:15:00
- **FVG 5m**: 22037.94 - 22041.80
- **Entrée**: 22034.07 @ 2025-02-26 10:57:00
- **Stop Loss**: 22045.86
- **Risk**: 11.79 points
- **TP 1RR**: 22022.28 ✅
- **TP 2RR**: 22010.49 ✅
- **TP 3RR**: 21998.70 ✅
- **TP 4RR**: 21986.91 ❌
- **TP 15RR**: 21857.21 ❌
- **PnL**: -11.79 points (-1.0R)
- **MFE**: 39.69 points
- **MAE**: 18.30 points

### Trade #335 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 09:15:00
- **FVG 5m**: 22037.94 - 22041.80
- **Entrée**: 22034.07 @ 2025-02-26 10:57:00
- **Stop Loss**: 22045.86
- **Risk**: 11.79 points
- **TP 1RR**: 22022.28 ✅
- **TP 2RR**: 22010.49 ✅
- **TP 3RR**: 21998.70 ✅
- **TP 4RR**: 21986.91 ❌
- **TP 15RR**: 21857.21 ❌
- **PnL**: -11.79 points (-1.0R)
- **MFE**: 39.69 points
- **MAE**: 18.30 points

### Trade #336 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-26 09:15:00
- **FVG 5m**: 22037.94 - 22041.80
- **Entrée**: 22034.07 @ 2025-02-26 10:57:00
- **Stop Loss**: 22045.86
- **Risk**: 11.79 points
- **TP 1RR**: 22022.28 ✅
- **TP 2RR**: 22010.49 ✅
- **TP 3RR**: 21998.70 ✅
- **TP 4RR**: 21986.91 ❌
- **TP 15RR**: 21857.21 ❌
- **PnL**: -11.79 points (-1.0R)
- **MFE**: 39.69 points
- **MAE**: 18.30 points

### Trade #337 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 13:15:00
- **FVG 5m**: 21789.22 - 21798.75
- **Entrée**: 21802.11 @ 2025-02-26 14:23:00
- **Stop Loss**: 21710.83
- **Risk**: 91.28 points
- **TP 1RR**: 21893.38 ✅
- **TP 2RR**: 21984.66 ❌
- **TP 3RR**: 22075.93 ❌
- **TP 4RR**: 22167.21 ❌
- **TP 15RR**: 23171.25 ❌
- **PnL**: -91.28 points (-1.0R)
- **MFE**: 183.77 points
- **MAE**: 95.11 points

### Trade #338 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 13:15:00
- **FVG 5m**: 21789.22 - 21798.75
- **Entrée**: 21802.11 @ 2025-02-26 14:23:00
- **Stop Loss**: 21710.83
- **Risk**: 91.28 points
- **TP 1RR**: 21893.38 ✅
- **TP 2RR**: 21984.66 ❌
- **TP 3RR**: 22075.93 ❌
- **TP 4RR**: 22167.21 ❌
- **TP 15RR**: 23171.25 ❌
- **PnL**: -91.28 points (-1.0R)
- **MFE**: 183.77 points
- **MAE**: 95.11 points

### Trade #339 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-26 14:30:00
- **FVG 5m**: 21822.72 - 21841.02
- **Entrée**: 21841.54 @ 2025-02-26 14:43:00
- **Stop Loss**: 21771.88
- **Risk**: 69.66 points
- **TP 1RR**: 21911.20 ❌
- **TP 2RR**: 21980.85 ❌
- **TP 3RR**: 22050.51 ❌
- **TP 4RR**: 22120.17 ❌
- **TP 15RR**: 22886.39 ❌
- **PnL**: -69.66 points (-1.0R)
- **MFE**: 144.34 points
- **MAE**: 134.54 points

### Trade #340 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-27 07:45:00
- **FVG 5m**: 21968.61 - 21980.72
- **Entrée**: 21968.35 @ 2025-02-27 08:39:00
- **Stop Loss**: 22040.19
- **Risk**: 71.84 points
- **TP 1RR**: 21896.51 ✅
- **TP 2RR**: 21824.67 ✅
- **TP 3RR**: 21752.82 ✅
- **TP 4RR**: 21680.98 ✅
- **TP 15RR**: 20890.72 ✅
- **PnL**: 1077.62 points (15.0R)
- **MFE**: 1078.91 points
- **MAE**: 0.26 points

### Trade #341 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-27 08:30:00
- **FVG 5m**: 21889.48 - 21960.87
- **Entrée**: 21879.17 @ 2025-02-27 08:42:00
- **Stop Loss**: 22054.12
- **Risk**: 174.95 points
- **TP 1RR**: 21704.22 ✅
- **TP 2RR**: 21529.28 ✅
- **TP 3RR**: 21354.33 ✅
- **TP 4RR**: 21179.39 ✅
- **TP 15RR**: 19254.99 ✅
- **PnL**: 2624.18 points (15.0R)
- **MFE**: 2625.71 points
- **MAE**: 10.31 points

### Trade #342 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21532.56
- **Risk**: 180.62 points
- **TP 1RR**: 21893.81 ❌
- **TP 2RR**: 22074.43 ❌
- **TP 3RR**: 22255.05 ❌
- **TP 4RR**: 22435.68 ❌
- **TP 15RR**: 24422.54 ❌
- **PnL**: -180.62 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 198.20 points

### Trade #343 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21532.56
- **Risk**: 180.62 points
- **TP 1RR**: 21893.81 ❌
- **TP 2RR**: 22074.43 ❌
- **TP 3RR**: 22255.05 ❌
- **TP 4RR**: 22435.68 ❌
- **TP 15RR**: 24422.54 ❌
- **PnL**: -180.62 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 198.20 points

### Trade #344 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21532.56
- **Risk**: 180.62 points
- **TP 1RR**: 21893.81 ❌
- **TP 2RR**: 22074.43 ❌
- **TP 3RR**: 22255.05 ❌
- **TP 4RR**: 22435.68 ❌
- **TP 15RR**: 24422.54 ❌
- **PnL**: -180.62 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 198.20 points

### Trade #345 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21532.56
- **Risk**: 180.62 points
- **TP 1RR**: 21893.81 ❌
- **TP 2RR**: 22074.43 ❌
- **TP 3RR**: 22255.05 ❌
- **TP 4RR**: 22435.68 ❌
- **TP 15RR**: 24422.54 ❌
- **PnL**: -180.62 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 198.20 points

### Trade #346 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21532.56
- **Risk**: 180.62 points
- **TP 1RR**: 21893.81 ❌
- **TP 2RR**: 22074.43 ❌
- **TP 3RR**: 22255.05 ❌
- **TP 4RR**: 22435.68 ❌
- **TP 15RR**: 24422.54 ❌
- **PnL**: -180.62 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 198.20 points

### Trade #347 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:00:00
- **FVG 5m**: 21662.15 - 21705.45
- **Entrée**: 21713.18 @ 2025-02-27 09:13:00
- **Stop Loss**: 21532.56
- **Risk**: 180.62 points
- **TP 1RR**: 21893.81 ❌
- **TP 2RR**: 22074.43 ❌
- **TP 3RR**: 22255.05 ❌
- **TP 4RR**: 22435.68 ❌
- **TP 15RR**: 24422.54 ❌
- **PnL**: -180.62 points (-1.0R)
- **MFE**: 108.25 points
- **MAE**: 198.20 points

### Trade #348 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 09:15:00
- **FVG 5m**: 21717.05 - 21767.05
- **Entrée**: 21774.01 @ 2025-02-27 10:14:00
- **Stop Loss**: 21694.60
- **Risk**: 79.41 points
- **TP 1RR**: 21853.42 ❌
- **TP 2RR**: 21932.84 ❌
- **TP 3RR**: 22012.25 ❌
- **TP 4RR**: 22091.66 ❌
- **TP 15RR**: 22965.19 ❌
- **PnL**: -79.41 points (-1.0R)
- **MFE**: 40.98 points
- **MAE**: 79.90 points

### Trade #349 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 19:30:00
- **FVG 5m**: 21266.52 - 21269.35
- **Entrée**: 21270.64 @ 2025-02-27 20:28:00
- **Stop Loss**: 21163.92
- **Risk**: 106.72 points
- **TP 1RR**: 21377.37 ❌
- **TP 2RR**: 21484.09 ❌
- **TP 3RR**: 21590.82 ❌
- **TP 4RR**: 21697.54 ❌
- **TP 15RR**: 22871.52 ❌
- **PnL**: -106.72 points (-1.0R)
- **MFE**: 14.43 points
- **MAE**: 119.85 points

### Trade #350 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-27 21:45:00
- **FVG 5m**: 21212.65 - 21232.24
- **Entrée**: 21238.94 @ 2025-02-27 22:24:00
- **Stop Loss**: 21140.22
- **Risk**: 98.72 points
- **TP 1RR**: 21337.66 ❌
- **TP 2RR**: 21436.39 ❌
- **TP 3RR**: 21535.11 ❌
- **TP 4RR**: 21633.83 ❌
- **TP 15RR**: 22719.79 ❌
- **PnL**: -98.72 points (-1.0R)
- **MFE**: 85.57 points
- **MAE**: 109.02 points

### Trade #351 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 06:00:00
- **FVG 5m**: 21248.99 - 21260.59
- **Entrée**: 21241.00 @ 2025-02-28 06:31:00
- **Stop Loss**: 21315.32
- **Risk**: 74.31 points
- **TP 1RR**: 21166.69 ✅
- **TP 2RR**: 21092.37 ❌
- **TP 3RR**: 21018.06 ❌
- **TP 4RR**: 20943.74 ❌
- **TP 15RR**: 20126.28 ❌
- **PnL**: -74.31 points (-1.0R)
- **MFE**: 146.91 points
- **MAE**: 74.75 points

### Trade #352 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 06:00:00
- **FVG 5m**: 21248.99 - 21260.59
- **Entrée**: 21241.00 @ 2025-02-28 06:31:00
- **Stop Loss**: 21315.32
- **Risk**: 74.31 points
- **TP 1RR**: 21166.69 ✅
- **TP 2RR**: 21092.37 ❌
- **TP 3RR**: 21018.06 ❌
- **TP 4RR**: 20943.74 ❌
- **TP 15RR**: 20126.28 ❌
- **PnL**: -74.31 points (-1.0R)
- **MFE**: 146.91 points
- **MAE**: 74.75 points

### Trade #353 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 08:30:00
- **FVG 5m**: 21339.20 - 21347.45
- **Entrée**: 21354.15 @ 2025-02-28 09:24:00
- **Stop Loss**: 21083.54
- **Risk**: 270.61 points
- **TP 1RR**: 21624.76 ✅
- **TP 2RR**: 21895.37 ❌
- **TP 3RR**: 22165.98 ❌
- **TP 4RR**: 22436.58 ❌
- **TP 15RR**: 25413.28 ❌
- **PnL**: -270.61 points (-1.0R)
- **MFE**: 420.89 points
- **MAE**: 294.60 points

### Trade #354 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 08:30:00
- **FVG 5m**: 21339.20 - 21347.45
- **Entrée**: 21354.15 @ 2025-02-28 09:24:00
- **Stop Loss**: 21083.54
- **Risk**: 270.61 points
- **TP 1RR**: 21624.76 ✅
- **TP 2RR**: 21895.37 ❌
- **TP 3RR**: 22165.98 ❌
- **TP 4RR**: 22436.58 ❌
- **TP 15RR**: 25413.28 ❌
- **PnL**: -270.61 points (-1.0R)
- **MFE**: 420.89 points
- **MAE**: 294.60 points

### Trade #355 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 09:15:00
- **FVG 5m**: 21363.94 - 21370.39
- **Entrée**: 21373.22 @ 2025-02-28 09:26:00
- **Stop Loss**: 21250.22
- **Risk**: 123.01 points
- **TP 1RR**: 21496.23 ❌
- **TP 2RR**: 21619.23 ❌
- **TP 3RR**: 21742.24 ❌
- **TP 4RR**: 21865.25 ❌
- **TP 15RR**: 23218.31 ❌
- **PnL**: -123.01 points (-1.0R)
- **MFE**: 48.20 points
- **MAE**: 134.54 points

### Trade #356 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 09:15:00
- **FVG 5m**: 21363.94 - 21370.39
- **Entrée**: 21373.22 @ 2025-02-28 09:26:00
- **Stop Loss**: 21250.22
- **Risk**: 123.01 points
- **TP 1RR**: 21496.23 ❌
- **TP 2RR**: 21619.23 ❌
- **TP 3RR**: 21742.24 ❌
- **TP 4RR**: 21865.25 ❌
- **TP 15RR**: 23218.31 ❌
- **PnL**: -123.01 points (-1.0R)
- **MFE**: 48.20 points
- **MAE**: 134.54 points

### Trade #357 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 09:15:00
- **FVG 5m**: 21363.94 - 21370.39
- **Entrée**: 21373.22 @ 2025-02-28 09:26:00
- **Stop Loss**: 21250.22
- **Risk**: 123.01 points
- **TP 1RR**: 21496.23 ❌
- **TP 2RR**: 21619.23 ❌
- **TP 3RR**: 21742.24 ❌
- **TP 4RR**: 21865.25 ❌
- **TP 15RR**: 23218.31 ❌
- **PnL**: -123.01 points (-1.0R)
- **MFE**: 48.20 points
- **MAE**: 134.54 points

### Trade #358 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 10:15:00
- **FVG 5m**: 21269.87 - 21308.53
- **Entrée**: 21265.23 @ 2025-02-28 11:43:00
- **Stop Loss**: 21370.24
- **Risk**: 105.01 points
- **TP 1RR**: 21160.22 ✅
- **TP 2RR**: 21055.20 ❌
- **TP 3RR**: 20950.19 ❌
- **TP 4RR**: 20845.18 ❌
- **TP 15RR**: 19690.03 ❌
- **PnL**: -105.01 points (-1.0R)
- **MFE**: 146.65 points
- **MAE**: 112.38 points

### Trade #359 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 10:15:00
- **FVG 5m**: 21269.87 - 21308.53
- **Entrée**: 21265.23 @ 2025-02-28 11:43:00
- **Stop Loss**: 21370.24
- **Risk**: 105.01 points
- **TP 1RR**: 21160.22 ✅
- **TP 2RR**: 21055.20 ❌
- **TP 3RR**: 20950.19 ❌
- **TP 4RR**: 20845.18 ❌
- **TP 15RR**: 19690.03 ❌
- **PnL**: -105.01 points (-1.0R)
- **MFE**: 146.65 points
- **MAE**: 112.38 points

### Trade #360 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-02-28 10:15:00
- **FVG 5m**: 21269.87 - 21308.53
- **Entrée**: 21265.23 @ 2025-02-28 11:43:00
- **Stop Loss**: 21370.24
- **Risk**: 105.01 points
- **TP 1RR**: 21160.22 ✅
- **TP 2RR**: 21055.20 ❌
- **TP 3RR**: 20950.19 ❌
- **TP 4RR**: 20845.18 ❌
- **TP 15RR**: 19690.03 ❌
- **PnL**: -105.01 points (-1.0R)
- **MFE**: 146.65 points
- **MAE**: 112.38 points

### Trade #361 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 14:15:00
- **FVG 5m**: 21412.40 - 21419.87
- **Entrée**: 21426.06 @ 2025-02-28 14:49:00
- **Stop Loss**: 21318.74
- **Risk**: 107.32 points
- **TP 1RR**: 21533.38 ✅
- **TP 2RR**: 21640.70 ✅
- **TP 3RR**: 21748.01 ✅
- **TP 4RR**: 21855.33 ❌
- **TP 15RR**: 23035.83 ❌
- **PnL**: -107.32 points (-1.0R)
- **MFE**: 348.98 points
- **MAE**: 110.31 points

### Trade #362 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 14:45:00
- **FVG 5m**: 21525.55 - 21530.45
- **Entrée**: 21535.08 @ 2025-02-28 15:04:00
- **Stop Loss**: 21372.58
- **Risk**: 162.50 points
- **TP 1RR**: 21697.59 ✅
- **TP 2RR**: 21860.09 ❌
- **TP 3RR**: 22022.59 ❌
- **TP 4RR**: 22185.09 ❌
- **TP 15RR**: 23972.61 ❌
- **PnL**: -162.50 points (-1.0R)
- **MFE**: 239.96 points
- **MAE**: 167.79 points

### Trade #363 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-02-28 14:45:00
- **FVG 5m**: 21525.55 - 21530.45
- **Entrée**: 21535.08 @ 2025-02-28 15:04:00
- **Stop Loss**: 21372.58
- **Risk**: 162.50 points
- **TP 1RR**: 21697.59 ✅
- **TP 2RR**: 21860.09 ❌
- **TP 3RR**: 22022.59 ❌
- **TP 4RR**: 22185.09 ❌
- **TP 15RR**: 23972.61 ❌
- **PnL**: -162.50 points (-1.0R)
- **MFE**: 239.96 points
- **MAE**: 167.79 points

### Trade #364 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-02 23:00:00
- **FVG 5m**: 21632.25 - 21635.35
- **Entrée**: 21640.50 @ 2025-03-02 23:37:00
- **Stop Loss**: 21582.28
- **Risk**: 58.22 points
- **TP 1RR**: 21698.72 ❌
- **TP 2RR**: 21756.94 ❌
- **TP 3RR**: 21815.16 ❌
- **TP 4RR**: 21873.39 ❌
- **TP 15RR**: 22513.82 ❌
- **PnL**: -58.22 points (-1.0R)
- **MFE**: 31.70 points
- **MAE**: 59.54 points

### Trade #365 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 01:15:00
- **FVG 5m**: 21600.04 - 21613.70
- **Entrée**: 21585.09 @ 2025-03-03 02:19:00
- **Stop Loss**: 21639.98
- **Risk**: 54.89 points
- **TP 1RR**: 21530.20 ❌
- **TP 2RR**: 21475.31 ❌
- **TP 3RR**: 21420.42 ❌
- **TP 4RR**: 21365.53 ❌
- **TP 15RR**: 20761.76 ❌
- **PnL**: -54.89 points (-1.0R)
- **MFE**: 50.26 points
- **MAE**: 57.22 points

### Trade #366 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 08:30:00
- **FVG 5m**: 21564.73 - 21576.07
- **Entrée**: 21555.19 @ 2025-03-03 08:54:00
- **Stop Loss**: 21785.93
- **Risk**: 230.74 points
- **TP 1RR**: 21324.45 ✅
- **TP 2RR**: 21093.71 ✅
- **TP 3RR**: 20862.97 ✅
- **TP 4RR**: 20632.22 ✅
- **TP 15RR**: 18094.07 ✅
- **PnL**: 3461.12 points (15.0R)
- **MFE**: 3485.31 points
- **MAE**: 84.02 points

### Trade #367 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 08:30:00
- **FVG 5m**: 21564.73 - 21576.07
- **Entrée**: 21555.19 @ 2025-03-03 08:54:00
- **Stop Loss**: 21785.93
- **Risk**: 230.74 points
- **TP 1RR**: 21324.45 ✅
- **TP 2RR**: 21093.71 ✅
- **TP 3RR**: 20862.97 ✅
- **TP 4RR**: 20632.22 ✅
- **TP 15RR**: 18094.07 ✅
- **PnL**: 3461.12 points (15.0R)
- **MFE**: 3485.31 points
- **MAE**: 84.02 points

### Trade #368 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 08:30:00
- **FVG 5m**: 21564.73 - 21576.07
- **Entrée**: 21555.19 @ 2025-03-03 08:54:00
- **Stop Loss**: 21785.93
- **Risk**: 230.74 points
- **TP 1RR**: 21324.45 ✅
- **TP 2RR**: 21093.71 ✅
- **TP 3RR**: 20862.97 ✅
- **TP 4RR**: 20632.22 ✅
- **TP 15RR**: 18094.07 ✅
- **PnL**: 3461.12 points (15.0R)
- **MFE**: 3485.31 points
- **MAE**: 84.02 points

### Trade #369 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 08:45:00
- **FVG 5m**: 21486.63 - 21526.58
- **Entrée**: 21530.19 @ 2025-03-03 09:21:00
- **Stop Loss**: 21458.37
- **Risk**: 71.82 points
- **TP 1RR**: 21602.01 ✅
- **TP 2RR**: 21673.83 ❌
- **TP 3RR**: 21745.65 ❌
- **TP 4RR**: 21817.47 ❌
- **TP 15RR**: 22607.48 ❌
- **PnL**: -71.82 points (-1.0R)
- **MFE**: 109.02 points
- **MAE**: 99.49 points

### Trade #370 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 09:15:00
- **FVG 5m**: 21511.63 - 21541.27
- **Entrée**: 21548.23 @ 2025-03-03 10:49:00
- **Stop Loss**: 21439.56
- **Risk**: 108.67 points
- **TP 1RR**: 21656.90 ❌
- **TP 2RR**: 21765.56 ❌
- **TP 3RR**: 21874.23 ❌
- **TP 4RR**: 21982.90 ❌
- **TP 15RR**: 23178.23 ❌
- **PnL**: -108.67 points (-1.0R)
- **MFE**: 65.47 points
- **MAE**: 117.53 points

### Trade #371 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 09:15:00
- **FVG 5m**: 21511.63 - 21541.27
- **Entrée**: 21548.23 @ 2025-03-03 10:49:00
- **Stop Loss**: 21439.56
- **Risk**: 108.67 points
- **TP 1RR**: 21656.90 ❌
- **TP 2RR**: 21765.56 ❌
- **TP 3RR**: 21874.23 ❌
- **TP 4RR**: 21982.90 ❌
- **TP 15RR**: 23178.23 ❌
- **PnL**: -108.67 points (-1.0R)
- **MFE**: 65.47 points
- **MAE**: 117.53 points

### Trade #372 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 12:00:00
- **FVG 5m**: 21352.86 - 21366.01
- **Entrée**: 21325.80 @ 2025-03-03 12:28:00
- **Stop Loss**: 21513.62
- **Risk**: 187.82 points
- **TP 1RR**: 21137.98 ✅
- **TP 2RR**: 20950.16 ✅
- **TP 3RR**: 20762.34 ✅
- **TP 4RR**: 20574.52 ✅
- **TP 15RR**: 18508.50 ✅
- **PnL**: 2817.30 points (15.0R)
- **MFE**: 2821.35 points
- **MAE**: 138.66 points

### Trade #373 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 14:00:00
- **FVG 5m**: 21063.93 - 21097.96
- **Entrée**: 21099.50 @ 2025-03-03 14:58:00
- **Stop Loss**: 21049.02
- **Risk**: 50.48 points
- **TP 1RR**: 21149.98 ✅
- **TP 2RR**: 21200.46 ✅
- **TP 3RR**: 21250.94 ❌
- **TP 4RR**: 21301.42 ❌
- **TP 15RR**: 21856.70 ❌
- **PnL**: -50.48 points (-1.0R)
- **MFE**: 130.16 points
- **MAE**: 50.52 points

### Trade #374 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-03 15:00:00
- **FVG 5m**: 21139.19 - 21161.62
- **Entrée**: 21162.13 @ 2025-03-03 18:19:00
- **Stop Loss**: 21087.41
- **Risk**: 74.73 points
- **TP 1RR**: 21236.86 ❌
- **TP 2RR**: 21311.59 ❌
- **TP 3RR**: 21386.31 ❌
- **TP 4RR**: 21461.04 ❌
- **TP 15RR**: 22283.03 ❌
- **PnL**: -74.73 points (-1.0R)
- **MFE**: 67.53 points
- **MAE**: 77.58 points

### Trade #375 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-03 23:00:00
- **FVG 5m**: 21177.08 - 21189.71
- **Entrée**: 21171.67 @ 2025-03-04 00:09:00
- **Stop Loss**: 21240.28
- **Risk**: 68.61 points
- **TP 1RR**: 21103.06 ✅
- **TP 2RR**: 21034.46 ✅
- **TP 3RR**: 20965.85 ✅
- **TP 4RR**: 20897.24 ✅
- **TP 15RR**: 20142.57 ❌
- **PnL**: -68.61 points (-1.0R)
- **MFE**: 474.76 points
- **MAE**: 84.02 points

### Trade #376 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-04 02:00:00
- **FVG 5m**: 21167.29 - 21176.05
- **Entrée**: 21187.13 @ 2025-03-04 02:31:00
- **Stop Loss**: 21085.86
- **Risk**: 101.27 points
- **TP 1RR**: 21288.41 ❌
- **TP 2RR**: 21389.68 ❌
- **TP 3RR**: 21490.95 ❌
- **TP 4RR**: 21592.23 ❌
- **TP 15RR**: 22706.23 ❌
- **PnL**: -101.27 points (-1.0R)
- **MFE**: 15.98 points
- **MAE**: 102.58 points

### Trade #377 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-04 07:30:00
- **FVG 5m**: 20977.33 - 21000.79
- **Entrée**: 21004.14 @ 2025-03-04 08:02:00
- **Stop Loss**: 20887.24
- **Risk**: 116.90 points
- **TP 1RR**: 21121.03 ❌
- **TP 2RR**: 21237.93 ❌
- **TP 3RR**: 21354.83 ❌
- **TP 4RR**: 21471.72 ❌
- **TP 15RR**: 22757.58 ❌
- **PnL**: -116.90 points (-1.0R)
- **MFE**: 58.51 points
- **MAE**: 150.26 points

### Trade #378 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-04 12:00:00
- **FVG 5m**: 21049.50 - 21062.90
- **Entrée**: 21066.77 @ 2025-03-04 12:39:00
- **Stop Loss**: 20929.23
- **Risk**: 137.54 points
- **TP 1RR**: 21204.30 ✅
- **TP 2RR**: 21341.84 ✅
- **TP 3RR**: 21479.38 ❌
- **TP 4RR**: 21616.91 ❌
- **TP 15RR**: 23129.82 ❌
- **PnL**: -137.54 points (-1.0R)
- **MFE**: 307.74 points
- **MAE**: 150.01 points

### Trade #379 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-04 13:00:00
- **FVG 5m**: 21229.92 - 21308.79
- **Entrée**: 21196.15 @ 2025-03-04 14:33:00
- **Stop Loss**: 21236.41
- **Risk**: 40.25 points
- **TP 1RR**: 21155.90 ✅
- **TP 2RR**: 21115.65 ✅
- **TP 3RR**: 21075.40 ✅
- **TP 4RR**: 21035.14 ✅
- **TP 15RR**: 20592.36 ❌
- **PnL**: -40.25 points (-1.0R)
- **MFE**: 242.53 points
- **MAE**: 45.62 points

### Trade #380 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-04 13:15:00
- **FVG 5m**: 21229.92 - 21308.79
- **Entrée**: 21196.15 @ 2025-03-04 14:33:00
- **Stop Loss**: 21273.54
- **Risk**: 77.39 points
- **TP 1RR**: 21118.77 ✅
- **TP 2RR**: 21041.38 ✅
- **TP 3RR**: 20964.00 ✅
- **TP 4RR**: 20886.61 ✅
- **TP 15RR**: 20035.36 ❌
- **PnL**: -77.39 points (-1.0R)
- **MFE**: 355.17 points
- **MAE**: 95.62 points

### Trade #381 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-04 14:45:00
- **FVG 5m**: 21183.78 - 21194.87
- **Entrée**: 21174.50 @ 2025-03-04 15:32:00
- **Stop Loss**: 21199.79
- **Risk**: 25.29 points
- **TP 1RR**: 21149.22 ✅
- **TP 2RR**: 21123.93 ✅
- **TP 3RR**: 21098.65 ❌
- **TP 4RR**: 21073.36 ❌
- **TP 15RR**: 20795.22 ❌
- **PnL**: -25.29 points (-1.0R)
- **MFE**: 57.22 points
- **MAE**: 31.44 points

### Trade #382 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-05 02:30:00
- **FVG 5m**: 21211.36 - 21237.91
- **Entrée**: 21209.04 @ 2025-03-05 04:12:00
- **Stop Loss**: 21254.20
- **Risk**: 45.16 points
- **TP 1RR**: 21163.88 ✅
- **TP 2RR**: 21118.72 ✅
- **TP 3RR**: 21073.56 ✅
- **TP 4RR**: 21028.41 ✅
- **TP 15RR**: 20531.65 ❌
- **PnL**: -45.16 points (-1.0R)
- **MFE**: 368.06 points
- **MAE**: 45.36 points

### Trade #383 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-05 04:00:00
- **FVG 5m**: 21211.36 - 21237.91
- **Entrée**: 21209.04 @ 2025-03-05 04:12:00
- **Stop Loss**: 21271.22
- **Risk**: 62.18 points
- **TP 1RR**: 21146.86 ✅
- **TP 2RR**: 21084.68 ✅
- **TP 3RR**: 21022.51 ✅
- **TP 4RR**: 20960.33 ✅
- **TP 15RR**: 20276.36 ❌
- **PnL**: -62.18 points (-1.0R)
- **MFE**: 368.06 points
- **MAE**: 82.74 points

### Trade #384 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 08:30:00
- **FVG 5m**: 20994.34 - 21051.05
- **Entrée**: 21053.37 @ 2025-03-05 09:02:00
- **Stop Loss**: 20932.32
- **Risk**: 121.04 points
- **TP 1RR**: 21174.41 ❌
- **TP 2RR**: 21295.45 ❌
- **TP 3RR**: 21416.49 ❌
- **TP 4RR**: 21537.54 ❌
- **TP 15RR**: 22869.00 ❌
- **PnL**: -121.04 points (-1.0R)
- **MFE**: 78.35 points
- **MAE**: 125.26 points

### Trade #385 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 11:15:00
- **FVG 5m**: 21132.75 - 21172.96
- **Entrée**: 21174.25 @ 2025-03-05 11:52:00
- **Stop Loss**: 20984.62
- **Risk**: 189.63 points
- **TP 1RR**: 21363.87 ✅
- **TP 2RR**: 21553.50 ❌
- **TP 3RR**: 21743.13 ❌
- **TP 4RR**: 21932.76 ❌
- **TP 15RR**: 24018.67 ❌
- **PnL**: -189.63 points (-1.0R)
- **MFE**: 192.53 points
- **MAE**: 191.24 points

### Trade #386 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-05 11:15:00
- **FVG 5m**: 21132.75 - 21172.96
- **Entrée**: 21174.25 @ 2025-03-05 11:52:00
- **Stop Loss**: 20984.62
- **Risk**: 189.63 points
- **TP 1RR**: 21363.87 ✅
- **TP 2RR**: 21553.50 ❌
- **TP 3RR**: 21743.13 ❌
- **TP 4RR**: 21932.76 ❌
- **TP 15RR**: 24018.67 ❌
- **PnL**: -189.63 points (-1.0R)
- **MFE**: 192.53 points
- **MAE**: 191.24 points

### Trade #387 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-05 15:00:00
- **FVG 5m**: 21246.67 - 21256.21
- **Entrée**: 21235.33 @ 2025-03-05 17:31:00
- **Stop Loss**: 21313.51
- **Risk**: 78.18 points
- **TP 1RR**: 21157.15 ✅
- **TP 2RR**: 21078.97 ✅
- **TP 3RR**: 21000.79 ✅
- **TP 4RR**: 20922.61 ✅
- **TP 15RR**: 20062.64 ✅
- **PnL**: 1172.70 points (15.0R)
- **MFE**: 1177.88 points
- **MAE**: 51.55 points

### Trade #388 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-06 01:00:00
- **FVG 5m**: 21266.26 - 21271.42
- **Entrée**: 21261.36 @ 2025-03-06 01:15:00
- **Stop Loss**: 21292.11
- **Risk**: 30.74 points
- **TP 1RR**: 21230.62 ✅
- **TP 2RR**: 21199.87 ✅
- **TP 3RR**: 21169.13 ✅
- **TP 4RR**: 21138.38 ✅
- **TP 15RR**: 20800.19 ✅
- **PnL**: 461.17 points (15.0R)
- **MFE**: 466.00 points
- **MAE**: 13.40 points

### Trade #389 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-06 08:00:00
- **FVG 5m**: 20951.30 - 20986.35
- **Entrée**: 20989.45 @ 2025-03-06 09:04:00
- **Stop Loss**: 20923.82
- **Risk**: 65.62 points
- **TP 1RR**: 21055.07 ✅
- **TP 2RR**: 21120.69 ✅
- **TP 3RR**: 21186.32 ❌
- **TP 4RR**: 21251.94 ❌
- **TP 15RR**: 21973.80 ❌
- **PnL**: -65.62 points (-1.0R)
- **MFE**: 159.03 points
- **MAE**: 67.79 points

### Trade #390 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-06 12:45:00
- **FVG 5m**: 20669.85 - 20678.09
- **Entrée**: 20680.41 @ 2025-03-06 13:41:00
- **Stop Loss**: 20670.85
- **Risk**: 9.57 points
- **TP 1RR**: 20689.98 ✅
- **TP 2RR**: 20699.55 ✅
- **TP 3RR**: 20709.12 ✅
- **TP 4RR**: 20718.68 ✅
- **TP 15RR**: 20823.92 ✅
- **PnL**: 143.51 points (15.0R)
- **MFE**: 150.52 points
- **MAE**: 9.02 points

### Trade #391 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-06 19:00:00
- **FVG 5m**: 20816.76 - 20822.43
- **Entrée**: 20823.72 @ 2025-03-06 20:14:00
- **Stop Loss**: 20774.92
- **Risk**: 48.80 points
- **TP 1RR**: 20872.51 ❌
- **TP 2RR**: 20921.31 ❌
- **TP 3RR**: 20970.11 ❌
- **TP 4RR**: 21018.90 ❌
- **TP 15RR**: 21555.66 ❌
- **PnL**: -48.80 points (-1.0R)
- **MFE**: 19.33 points
- **MAE**: 50.78 points

### Trade #392 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 01:00:00
- **FVG 5m**: 20772.17 - 20780.93
- **Entrée**: 20781.71 @ 2025-03-07 01:46:00
- **Stop Loss**: 20732.93
- **Risk**: 48.78 points
- **TP 1RR**: 20830.48 ✅
- **TP 2RR**: 20879.26 ❌
- **TP 3RR**: 20928.03 ❌
- **TP 4RR**: 20976.81 ❌
- **TP 15RR**: 21513.33 ❌
- **PnL**: -48.78 points (-1.0R)
- **MFE**: 72.68 points
- **MAE**: 53.61 points

### Trade #393 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 01:00:00
- **FVG 5m**: 20772.17 - 20780.93
- **Entrée**: 20781.71 @ 2025-03-07 01:46:00
- **Stop Loss**: 20732.93
- **Risk**: 48.78 points
- **TP 1RR**: 20830.48 ✅
- **TP 2RR**: 20879.26 ❌
- **TP 3RR**: 20928.03 ❌
- **TP 4RR**: 20976.81 ❌
- **TP 15RR**: 21513.33 ❌
- **PnL**: -48.78 points (-1.0R)
- **MFE**: 72.68 points
- **MAE**: 53.61 points

### Trade #394 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 03:15:00
- **FVG 5m**: 20810.32 - 20821.91
- **Entrée**: 20808.77 @ 2025-03-07 04:04:00
- **Stop Loss**: 20861.46
- **Risk**: 52.70 points
- **TP 1RR**: 20756.07 ✅
- **TP 2RR**: 20703.38 ❌
- **TP 3RR**: 20650.68 ❌
- **TP 4RR**: 20597.99 ❌
- **TP 15RR**: 20018.34 ❌
- **PnL**: -52.70 points (-1.0R)
- **MFE**: 126.04 points
- **MAE**: 67.27 points

### Trade #395 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 06:45:00
- **FVG 5m**: 20744.33 - 20768.82
- **Entrée**: 20798.97 @ 2025-03-07 07:39:00
- **Stop Loss**: 20706.91
- **Risk**: 92.06 points
- **TP 1RR**: 20891.04 ❌
- **TP 2RR**: 20983.10 ❌
- **TP 3RR**: 21075.16 ❌
- **TP 4RR**: 21167.23 ❌
- **TP 15RR**: 22179.92 ❌
- **PnL**: -92.06 points (-1.0R)
- **MFE**: 6.19 points
- **MAE**: 95.36 points

### Trade #396 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20740.98 - 20759.80
- **Entrée**: 20740.47 @ 2025-03-07 09:13:00
- **Stop Loss**: 20912.01
- **Risk**: 171.54 points
- **TP 1RR**: 20568.93 ✅
- **TP 2RR**: 20397.39 ✅
- **TP 3RR**: 20225.85 ❌
- **TP 4RR**: 20054.31 ❌
- **TP 15RR**: 18167.38 ❌
- **PnL**: -171.54 points (-1.0R)
- **MFE**: 362.90 points
- **MAE**: 173.98 points

### Trade #397 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20740.98 - 20759.80
- **Entrée**: 20740.47 @ 2025-03-07 09:13:00
- **Stop Loss**: 20912.01
- **Risk**: 171.54 points
- **TP 1RR**: 20568.93 ✅
- **TP 2RR**: 20397.39 ✅
- **TP 3RR**: 20225.85 ❌
- **TP 4RR**: 20054.31 ❌
- **TP 15RR**: 18167.38 ❌
- **PnL**: -171.54 points (-1.0R)
- **MFE**: 362.90 points
- **MAE**: 173.98 points

### Trade #398 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20740.98 - 20759.80
- **Entrée**: 20740.47 @ 2025-03-07 09:13:00
- **Stop Loss**: 20912.01
- **Risk**: 171.54 points
- **TP 1RR**: 20568.93 ✅
- **TP 2RR**: 20397.39 ✅
- **TP 3RR**: 20225.85 ❌
- **TP 4RR**: 20054.31 ❌
- **TP 15RR**: 18167.38 ❌
- **PnL**: -171.54 points (-1.0R)
- **MFE**: 362.90 points
- **MAE**: 173.98 points

### Trade #399 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 07:30:00
- **FVG 5m**: 20740.98 - 20759.80
- **Entrée**: 20740.47 @ 2025-03-07 09:13:00
- **Stop Loss**: 20912.01
- **Risk**: 171.54 points
- **TP 1RR**: 20568.93 ✅
- **TP 2RR**: 20397.39 ✅
- **TP 3RR**: 20225.85 ❌
- **TP 4RR**: 20054.31 ❌
- **TP 15RR**: 18167.38 ❌
- **PnL**: -171.54 points (-1.0R)
- **MFE**: 362.90 points
- **MAE**: 173.98 points

### Trade #400 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-07 13:15:00
- **FVG 5m**: 20831.71 - 20841.24
- **Entrée**: 20862.38 @ 2025-03-07 14:08:00
- **Stop Loss**: 20773.63
- **Risk**: 88.75 points
- **TP 1RR**: 20951.12 ❌
- **TP 2RR**: 21039.87 ❌
- **TP 3RR**: 21128.62 ❌
- **TP 4RR**: 21217.36 ❌
- **TP 15RR**: 22193.56 ❌
- **PnL**: -88.75 points (-1.0R)
- **MFE**: 19.33 points
- **MAE**: 103.87 points

### Trade #401 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 14:45:00
- **FVG 5m**: 20840.21 - 20846.14
- **Entrée**: 20839.18 @ 2025-03-07 15:09:00
- **Stop Loss**: 20924.90
- **Risk**: 85.72 points
- **TP 1RR**: 20753.46 ✅
- **TP 2RR**: 20667.75 ✅
- **TP 3RR**: 20582.03 ✅
- **TP 4RR**: 20496.31 ✅
- **TP 15RR**: 19553.42 ❌
- **PnL**: -85.72 points (-1.0R)
- **MFE**: 1107.26 points
- **MAE**: 85.72 points

### Trade #402 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-07 14:45:00
- **FVG 5m**: 20840.21 - 20846.14
- **Entrée**: 20839.18 @ 2025-03-07 15:09:00
- **Stop Loss**: 20924.90
- **Risk**: 85.72 points
- **TP 1RR**: 20753.46 ✅
- **TP 2RR**: 20667.75 ✅
- **TP 3RR**: 20582.03 ✅
- **TP 4RR**: 20496.31 ✅
- **TP 15RR**: 19553.42 ❌
- **PnL**: -85.72 points (-1.0R)
- **MFE**: 1107.26 points
- **MAE**: 85.72 points

### Trade #403 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-09 20:30:00
- **FVG 5m**: 20743.56 - 20750.52
- **Entrée**: 20752.32 @ 2025-03-09 20:57:00
- **Stop Loss**: 20689.65
- **Risk**: 62.67 points
- **TP 1RR**: 20815.00 ❌
- **TP 2RR**: 20877.67 ❌
- **TP 3RR**: 20940.34 ❌
- **TP 4RR**: 21003.01 ❌
- **TP 15RR**: 21692.40 ❌
- **PnL**: -62.67 points (-1.0R)
- **MFE**: 28.35 points
- **MAE**: 63.92 points

### Trade #404 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-10 01:00:00
- **FVG 5m**: 20739.18 - 20742.27
- **Entrée**: 20744.59 @ 2025-03-10 02:01:00
- **Stop Loss**: 20703.31
- **Risk**: 41.29 points
- **TP 1RR**: 20785.88 ❌
- **TP 2RR**: 20827.16 ❌
- **TP 3RR**: 20868.45 ❌
- **TP 4RR**: 20909.73 ❌
- **TP 15RR**: 21363.88 ❌
- **PnL**: -41.29 points (-1.0R)
- **MFE**: 20.10 points
- **MAE**: 41.75 points

### Trade #405 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-10 18:30:00
- **FVG 5m**: 19876.26 - 19890.95
- **Entrée**: 19905.64 @ 2025-03-10 18:43:00
- **Stop Loss**: 19814.80
- **Risk**: 90.84 points
- **TP 1RR**: 19996.49 ❌
- **TP 2RR**: 20087.33 ❌
- **TP 3RR**: 20178.17 ❌
- **TP 4RR**: 20269.02 ❌
- **TP 15RR**: 21268.29 ❌
- **PnL**: -90.84 points (-1.0R)
- **MFE**: 22.94 points
- **MAE**: 105.16 points

### Trade #406 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 02:45:00
- **FVG 5m**: 20052.30 - 20071.37
- **Entrée**: 20072.92 @ 2025-03-11 02:56:00
- **Stop Loss**: 20006.46
- **Risk**: 66.45 points
- **TP 1RR**: 20139.37 ✅
- **TP 2RR**: 20205.82 ❌
- **TP 3RR**: 20272.28 ❌
- **TP 4RR**: 20338.73 ❌
- **TP 15RR**: 21069.72 ❌
- **PnL**: -66.45 points (-1.0R)
- **MFE**: 118.56 points
- **MAE**: 76.81 points

### Trade #407 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 03:00:00
- **FVG 5m**: 20112.87 - 20131.94
- **Entrée**: 20136.06 @ 2025-03-11 03:11:00
- **Stop Loss**: 20061.33
- **Risk**: 74.73 points
- **TP 1RR**: 20210.79 ❌
- **TP 2RR**: 20285.52 ❌
- **TP 3RR**: 20360.25 ❌
- **TP 4RR**: 20434.98 ❌
- **TP 15RR**: 21257.00 ❌
- **PnL**: -74.73 points (-1.0R)
- **MFE**: 55.41 points
- **MAE**: 82.74 points

### Trade #408 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 03:30:00
- **FVG 5m**: 20144.05 - 20146.12
- **Entrée**: 20138.13 @ 2025-03-11 05:09:00
- **Stop Loss**: 20183.52
- **Risk**: 45.40 points
- **TP 1RR**: 20092.73 ✅
- **TP 2RR**: 20047.33 ❌
- **TP 3RR**: 20001.93 ❌
- **TP 4RR**: 19956.54 ❌
- **TP 15RR**: 19457.17 ❌
- **PnL**: -45.40 points (-1.0R)
- **MFE**: 64.69 points
- **MAE**: 46.14 points

### Trade #409 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 06:00:00
- **FVG 5m**: 20137.87 - 20154.88
- **Entrée**: 20130.39 @ 2025-03-11 07:09:00
- **Stop Loss**: 20151.03
- **Risk**: 20.64 points
- **TP 1RR**: 20109.76 ✅
- **TP 2RR**: 20089.12 ✅
- **TP 3RR**: 20068.48 ✅
- **TP 4RR**: 20047.84 ✅
- **TP 15RR**: 19820.82 ❌
- **PnL**: -20.64 points (-1.0R)
- **MFE**: 144.34 points
- **MAE**: 22.94 points

### Trade #410 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 07:00:00
- **FVG 5m**: 20115.19 - 20129.62
- **Entrée**: 20109.26 @ 2025-03-11 07:11:00
- **Stop Loss**: 20201.57
- **Risk**: 92.32 points
- **TP 1RR**: 20016.94 ✅
- **TP 2RR**: 19924.63 ❌
- **TP 3RR**: 19832.31 ❌
- **TP 4RR**: 19740.00 ❌
- **TP 15RR**: 18724.53 ❌
- **PnL**: -92.32 points (-1.0R)
- **MFE**: 123.20 points
- **MAE**: 96.65 points

### Trade #411 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 08:30:00
- **FVG 5m**: 19975.49 - 20037.35
- **Entrée**: 20047.40 @ 2025-03-11 10:07:00
- **Stop Loss**: 19976.06
- **Risk**: 71.34 points
- **TP 1RR**: 20118.74 ✅
- **TP 2RR**: 20190.07 ❌
- **TP 3RR**: 20261.41 ❌
- **TP 4RR**: 20332.74 ❌
- **TP 15RR**: 21117.43 ❌
- **PnL**: -71.34 points (-1.0R)
- **MFE**: 102.07 points
- **MAE**: 88.41 points

### Trade #412 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 08:45:00
- **FVG 5m**: 19995.08 - 20000.23
- **Entrée**: 19989.15 @ 2025-03-11 09:24:00
- **Stop Loss**: 20216.01
- **Risk**: 226.86 points
- **TP 1RR**: 19762.29 ❌
- **TP 2RR**: 19535.42 ❌
- **TP 3RR**: 19308.56 ❌
- **TP 4RR**: 19081.70 ❌
- **TP 15RR**: 16586.20 ❌
- **PnL**: -226.86 points (-1.0R)
- **MFE**: 193.56 points
- **MAE**: 227.59 points

### Trade #413 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 08:45:00
- **FVG 5m**: 19995.08 - 20000.23
- **Entrée**: 19989.15 @ 2025-03-11 09:24:00
- **Stop Loss**: 20216.01
- **Risk**: 226.86 points
- **TP 1RR**: 19762.29 ❌
- **TP 2RR**: 19535.42 ❌
- **TP 3RR**: 19308.56 ❌
- **TP 4RR**: 19081.70 ❌
- **TP 15RR**: 16586.20 ❌
- **PnL**: -226.86 points (-1.0R)
- **MFE**: 193.56 points
- **MAE**: 227.59 points

### Trade #414 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-11 12:30:00
- **FVG 5m**: 19849.20 - 19881.93
- **Entrée**: 19894.56 @ 2025-03-11 12:44:00
- **Stop Loss**: 19785.69
- **Risk**: 108.87 points
- **TP 1RR**: 20003.43 ✅
- **TP 2RR**: 20112.30 ✅
- **TP 3RR**: 20221.17 ✅
- **TP 4RR**: 20330.04 ✅
- **TP 15RR**: 21527.62 ❌
- **PnL**: -108.87 points (-1.0R)
- **MFE**: 506.98 points
- **MAE**: 116.76 points

### Trade #415 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 14:00:00
- **FVG 5m**: 20186.07 - 20211.07
- **Entrée**: 20184.52 @ 2025-03-11 14:14:00
- **Stop Loss**: 20296.99
- **Risk**: 112.47 points
- **TP 1RR**: 20072.05 ✅
- **TP 2RR**: 19959.59 ❌
- **TP 3RR**: 19847.12 ❌
- **TP 4RR**: 19734.65 ❌
- **TP 15RR**: 18497.52 ❌
- **PnL**: -112.47 points (-1.0R)
- **MFE**: 212.89 points
- **MAE**: 217.02 points

### Trade #416 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-11 14:30:00
- **FVG 5m**: 20088.64 - 20109.26
- **Entrée**: 20088.12 @ 2025-03-11 14:51:00
- **Stop Loss**: 20184.04
- **Risk**: 95.91 points
- **TP 1RR**: 19992.21 ✅
- **TP 2RR**: 19896.29 ❌
- **TP 3RR**: 19800.38 ❌
- **TP 4RR**: 19704.46 ❌
- **TP 15RR**: 18649.40 ❌
- **PnL**: -95.91 points (-1.0R)
- **MFE**: 116.50 points
- **MAE**: 98.72 points

### Trade #417 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-12 02:30:00
- **FVG 5m**: 20026.01 - 20047.66
- **Entrée**: 20048.43 @ 2025-03-12 02:43:00
- **Stop Loss**: 19987.40
- **Risk**: 61.03 points
- **TP 1RR**: 20109.46 ✅
- **TP 2RR**: 20170.49 ✅
- **TP 3RR**: 20231.53 ✅
- **TP 4RR**: 20292.56 ✅
- **TP 15RR**: 20963.90 ❌
- **PnL**: -61.03 points (-1.0R)
- **MFE**: 353.11 points
- **MAE**: 87.89 points

### Trade #418 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-12 07:30:00
- **FVG 5m**: 20310.04 - 20312.36
- **Entrée**: 20309.52 @ 2025-03-12 08:11:00
- **Stop Loss**: 20411.74
- **Risk**: 102.21 points
- **TP 1RR**: 20207.31 ✅
- **TP 2RR**: 20105.09 ✅
- **TP 3RR**: 20002.88 ✅
- **TP 4RR**: 19900.67 ✅
- **TP 15RR**: 18776.31 ❌
- **PnL**: -102.21 points (-1.0R)
- **MFE**: 545.90 points
- **MAE**: 109.28 points

### Trade #419 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-12 09:45:00
- **FVG 5m**: 20092.76 - 20105.65
- **Entrée**: 20078.84 @ 2025-03-12 09:59:00
- **Stop Loss**: 20185.59
- **Risk**: 106.74 points
- **TP 1RR**: 19972.10 ❌
- **TP 2RR**: 19865.36 ❌
- **TP 3RR**: 19758.62 ❌
- **TP 4RR**: 19651.88 ❌
- **TP 15RR**: 18477.73 ❌
- **PnL**: -106.74 points (-1.0R)
- **MFE**: 82.99 points
- **MAE**: 113.41 points

### Trade #420 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-12 22:30:00
- **FVG 5m**: 20134.26 - 20140.19
- **Entrée**: 20143.28 @ 2025-03-12 23:07:00
- **Stop Loss**: 20104.10
- **Risk**: 39.18 points
- **TP 1RR**: 20182.46 ❌
- **TP 2RR**: 20221.64 ❌
- **TP 3RR**: 20260.83 ❌
- **TP 4RR**: 20300.01 ❌
- **TP 15RR**: 20731.01 ❌
- **PnL**: -39.18 points (-1.0R)
- **MFE**: 6.70 points
- **MAE**: 40.72 points

### Trade #421 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 04:30:00
- **FVG 5m**: 20181.94 - 20184.26
- **Entrée**: 20187.61 @ 2025-03-13 04:44:00
- **Stop Loss**: 20137.07
- **Risk**: 50.54 points
- **TP 1RR**: 20238.15 ✅
- **TP 2RR**: 20288.69 ❌
- **TP 3RR**: 20339.23 ❌
- **TP 4RR**: 20389.77 ❌
- **TP 15RR**: 20945.70 ❌
- **PnL**: -50.54 points (-1.0R)
- **MFE**: 51.29 points
- **MAE**: 54.64 points

### Trade #422 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-13 07:00:00
- **FVG 5m**: 20018.79 - 20061.06
- **Entrée**: 20005.13 @ 2025-03-13 08:54:00
- **Stop Loss**: 20155.67
- **Risk**: 150.54 points
- **TP 1RR**: 19854.59 ❌
- **TP 2RR**: 19704.05 ❌
- **TP 3RR**: 19553.50 ❌
- **TP 4RR**: 19402.96 ❌
- **TP 15RR**: 17747.00 ❌
- **PnL**: -150.54 points (-1.0R)
- **MFE**: 82.22 points
- **MAE**: 170.88 points

### Trade #423 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 19912.95
- **Risk**: 167.44 points
- **TP 1RR**: 20247.83 ❌
- **TP 2RR**: 20415.27 ❌
- **TP 3RR**: 20582.72 ❌
- **TP 4RR**: 20750.16 ❌
- **TP 15RR**: 22592.01 ❌
- **PnL**: -167.44 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 185.57 points

### Trade #424 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 19912.95
- **Risk**: 167.44 points
- **TP 1RR**: 20247.83 ❌
- **TP 2RR**: 20415.27 ❌
- **TP 3RR**: 20582.72 ❌
- **TP 4RR**: 20750.16 ❌
- **TP 15RR**: 22592.01 ❌
- **PnL**: -167.44 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 185.57 points

### Trade #425 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 19912.95
- **Risk**: 167.44 points
- **TP 1RR**: 20247.83 ❌
- **TP 2RR**: 20415.27 ❌
- **TP 3RR**: 20582.72 ❌
- **TP 4RR**: 20750.16 ❌
- **TP 15RR**: 22592.01 ❌
- **PnL**: -167.44 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 185.57 points

### Trade #426 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 19912.95
- **Risk**: 167.44 points
- **TP 1RR**: 20247.83 ❌
- **TP 2RR**: 20415.27 ❌
- **TP 3RR**: 20582.72 ❌
- **TP 4RR**: 20750.16 ❌
- **TP 15RR**: 22592.01 ❌
- **PnL**: -167.44 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 185.57 points

### Trade #427 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 19912.95
- **Risk**: 167.44 points
- **TP 1RR**: 20247.83 ❌
- **TP 2RR**: 20415.27 ❌
- **TP 3RR**: 20582.72 ❌
- **TP 4RR**: 20750.16 ❌
- **TP 15RR**: 22592.01 ❌
- **PnL**: -167.44 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 185.57 points

### Trade #428 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 09:00:00
- **FVG 5m**: 20052.04 - 20070.34
- **Entrée**: 20080.39 @ 2025-03-13 09:14:00
- **Stop Loss**: 19912.95
- **Risk**: 167.44 points
- **TP 1RR**: 20247.83 ❌
- **TP 2RR**: 20415.27 ❌
- **TP 3RR**: 20582.72 ❌
- **TP 4RR**: 20750.16 ❌
- **TP 15RR**: 22592.01 ❌
- **PnL**: -167.44 points (-1.0R)
- **MFE**: 95.62 points
- **MAE**: 185.57 points

### Trade #429 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 10:30:00
- **FVG 5m**: 19916.47 - 19933.99
- **Entrée**: 19941.21 @ 2025-03-13 11:31:00
- **Stop Loss**: 19863.49
- **Risk**: 77.72 points
- **TP 1RR**: 20018.93 ❌
- **TP 2RR**: 20096.66 ❌
- **TP 3RR**: 20174.38 ❌
- **TP 4RR**: 20252.10 ❌
- **TP 15RR**: 21107.05 ❌
- **PnL**: -77.72 points (-1.0R)
- **MFE**: 50.00 points
- **MAE**: 102.58 points

### Trade #430 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-13 12:15:00
- **FVG 5m**: 19820.07 - 19835.02
- **Entrée**: 19845.33 @ 2025-03-13 13:02:00
- **Stop Loss**: 19762.25
- **Risk**: 83.08 points
- **TP 1RR**: 19928.42 ✅
- **TP 2RR**: 20011.50 ✅
- **TP 3RR**: 20094.58 ✅
- **TP 4RR**: 20177.67 ✅
- **TP 15RR**: 21091.60 ❌
- **PnL**: -83.08 points (-1.0R)
- **MFE**: 1104.31 points
- **MAE**: 83.86 points

### Trade #431 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 05:45:00
- **FVG 5m**: 20083.74 - 20094.57
- **Entrée**: 20081.94 @ 2025-03-14 08:14:00
- **Stop Loss**: 20101.26
- **Risk**: 19.32 points
- **TP 1RR**: 20062.61 ✅
- **TP 2RR**: 20043.29 ❌
- **TP 3RR**: 20023.96 ❌
- **TP 4RR**: 20004.64 ❌
- **TP 15RR**: 19792.07 ❌
- **PnL**: -19.32 points (-1.0R)
- **MFE**: 28.87 points
- **MAE**: 33.76 points

### Trade #432 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 05:45:00
- **FVG 5m**: 20083.74 - 20094.57
- **Entrée**: 20081.94 @ 2025-03-14 08:14:00
- **Stop Loss**: 20101.26
- **Risk**: 19.32 points
- **TP 1RR**: 20062.61 ✅
- **TP 2RR**: 20043.29 ❌
- **TP 3RR**: 20023.96 ❌
- **TP 4RR**: 20004.64 ❌
- **TP 15RR**: 19792.07 ❌
- **PnL**: -19.32 points (-1.0R)
- **MFE**: 28.87 points
- **MAE**: 33.76 points

### Trade #433 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 08:45:00
- **FVG 5m**: 20150.50 - 20181.94
- **Entrée**: 20094.05 @ 2025-03-14 09:00:00
- **Stop Loss**: 20238.45
- **Risk**: 144.40 points
- **TP 1RR**: 19949.65 ❌
- **TP 2RR**: 19805.26 ❌
- **TP 3RR**: 19660.86 ❌
- **TP 4RR**: 19516.46 ❌
- **TP 15RR**: 17928.09 ❌
- **PnL**: -144.40 points (-1.0R)
- **MFE**: 46.65 points
- **MAE**: 155.93 points

### Trade #434 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 10:00:00
- **FVG 5m**: 20261.84 - 20272.67
- **Entrée**: 20259.52 @ 2025-03-14 11:08:00
- **Stop Loss**: 20260.11
- **Risk**: 0.59 points
- **TP 1RR**: 20258.93 ❌
- **TP 2RR**: 20258.34 ❌
- **TP 3RR**: 20257.76 ❌
- **TP 4RR**: 20257.17 ❌
- **TP 15RR**: 20250.69 ❌
- **PnL**: -0.59 points (-1.0R)
- **MFE**: 8.51 points
- **MAE**: 4.90 points

### Trade #435 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 11:45:00
- **FVG 5m**: 20251.53 - 20257.46
- **Entrée**: 20239.68 @ 2025-03-14 13:13:00
- **Stop Loss**: 20328.19
- **Risk**: 88.51 points
- **TP 1RR**: 20151.16 ❌
- **TP 2RR**: 20062.65 ❌
- **TP 3RR**: 19974.14 ❌
- **TP 4RR**: 19885.63 ❌
- **TP 15RR**: 18911.99 ❌
- **PnL**: -88.51 points (-1.0R)
- **MFE**: 20.10 points
- **MAE**: 106.71 points

### Trade #436 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 14:45:00
- **FVG 5m**: 20285.81 - 20313.91
- **Entrée**: 20280.14 @ 2025-03-14 15:03:00
- **Stop Loss**: 20364.03
- **Risk**: 83.89 points
- **TP 1RR**: 20196.25 ✅
- **TP 2RR**: 20112.36 ❌
- **TP 3RR**: 20028.47 ❌
- **TP 4RR**: 19944.58 ❌
- **TP 15RR**: 19021.78 ❌
- **PnL**: -83.89 points (-1.0R)
- **MFE**: 124.23 points
- **MAE**: 94.33 points

### Trade #437 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-14 14:45:00
- **FVG 5m**: 20285.81 - 20313.91
- **Entrée**: 20280.14 @ 2025-03-14 15:03:00
- **Stop Loss**: 20364.03
- **Risk**: 83.89 points
- **TP 1RR**: 20196.25 ✅
- **TP 2RR**: 20112.36 ❌
- **TP 3RR**: 20028.47 ❌
- **TP 4RR**: 19944.58 ❌
- **TP 15RR**: 19021.78 ❌
- **PnL**: -83.89 points (-1.0R)
- **MFE**: 124.23 points
- **MAE**: 94.33 points

### Trade #438 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-17 02:45:00
- **FVG 5m**: 20237.87 - 20243.28
- **Entrée**: 20246.89 @ 2025-03-17 05:08:00
- **Stop Loss**: 20161.80
- **Risk**: 85.09 points
- **TP 1RR**: 20331.98 ✅
- **TP 2RR**: 20417.07 ✅
- **TP 3RR**: 20502.16 ✅
- **TP 4RR**: 20587.25 ❌
- **TP 15RR**: 21523.22 ❌
- **PnL**: -85.09 points (-1.0R)
- **MFE**: 330.42 points
- **MAE**: 94.72 points

### Trade #439 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-17 08:00:00
- **FVG 5m**: 20328.08 - 20340.19
- **Entrée**: 20327.31 @ 2025-03-17 08:19:00
- **Stop Loss**: 20375.89
- **Risk**: 48.59 points
- **TP 1RR**: 20278.72 ❌
- **TP 2RR**: 20230.13 ❌
- **TP 3RR**: 20181.55 ❌
- **TP 4RR**: 20132.96 ❌
- **TP 15RR**: 19598.51 ❌
- **PnL**: -48.59 points (-1.0R)
- **MFE**: 34.54 points
- **MAE**: 58.25 points

### Trade #440 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-17 09:15:00
- **FVG 5m**: 20345.35 - 20382.72
- **Entrée**: 20326.53 @ 2025-03-17 09:29:00
- **Stop Loss**: 20438.04
- **Risk**: 111.51 points
- **TP 1RR**: 20215.03 ❌
- **TP 2RR**: 20103.52 ❌
- **TP 3RR**: 19992.02 ❌
- **TP 4RR**: 19880.51 ❌
- **TP 15RR**: 18653.94 ❌
- **PnL**: -111.51 points (-1.0R)
- **MFE**: 89.95 points
- **MAE**: 112.38 points

### Trade #441 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-17 14:45:00
- **FVG 5m**: 20448.45 - 20474.74
- **Entrée**: 20446.13 @ 2025-03-17 14:59:00
- **Stop Loss**: 20547.12
- **Risk**: 100.99 points
- **TP 1RR**: 20345.13 ✅
- **TP 2RR**: 20244.14 ✅
- **TP 3RR**: 20143.15 ✅
- **TP 4RR**: 20042.15 ✅
- **TP 15RR**: 18931.22 ❌
- **PnL**: -100.99 points (-1.0R)
- **MFE**: 447.73 points
- **MAE**: 101.85 points

### Trade #442 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-18 08:30:00
- **FVG 5m**: 20144.52 - 20164.41
- **Entrée**: 20108.56 @ 2025-03-18 08:44:00
- **Stop Loss**: 20310.49
- **Risk**: 201.93 points
- **TP 1RR**: 19906.63 ❌
- **TP 2RR**: 19704.70 ❌
- **TP 3RR**: 19502.77 ❌
- **TP 4RR**: 19300.84 ❌
- **TP 15RR**: 17079.61 ❌
- **PnL**: -201.93 points (-1.0R)
- **MFE**: 110.17 points
- **MAE**: 209.89 points

### Trade #443 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-18 10:00:00
- **FVG 5m**: 20061.38 - 20070.82
- **Entrée**: 20077.70 @ 2025-03-18 11:02:00
- **Stop Loss**: 19988.39
- **Risk**: 89.31 points
- **TP 1RR**: 20167.02 ✅
- **TP 2RR**: 20256.33 ✅
- **TP 3RR**: 20345.64 ✅
- **TP 4RR**: 20434.95 ✅
- **TP 15RR**: 21417.39 ❌
- **PnL**: -89.31 points (-1.0R)
- **MFE**: 871.93 points
- **MAE**: 93.34 points

### Trade #444 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-18 13:45:00
- **FVG 5m**: 20113.66 - 20117.49
- **Entrée**: 20112.90 @ 2025-03-18 15:16:00
- **Stop Loss**: 20191.34
- **Risk**: 78.44 points
- **TP 1RR**: 20034.46 ❌
- **TP 2RR**: 19956.02 ❌
- **TP 3RR**: 19877.59 ❌
- **TP 4RR**: 19799.15 ❌
- **TP 15RR**: 18936.33 ❌
- **PnL**: -78.44 points (-1.0R)
- **MFE**: 51.26 points
- **MAE**: 82.63 points

### Trade #445 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-18 19:45:00
- **FVG 5m**: 20166.20 - 20169.00
- **Entrée**: 20163.90 @ 2025-03-18 21:49:00
- **Stop Loss**: 20205.62
- **Risk**: 41.72 points
- **TP 1RR**: 20122.18 ✅
- **TP 2RR**: 20080.46 ✅
- **TP 3RR**: 20038.74 ❌
- **TP 4RR**: 19997.02 ❌
- **TP 15RR**: 19538.09 ❌
- **PnL**: -41.72 points (-1.0R)
- **MFE**: 108.64 points
- **MAE**: 44.12 points

### Trade #446 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 02:15:00
- **FVG 5m**: 20075.15 - 20082.30
- **Entrée**: 20096.83 @ 2025-03-19 03:05:00
- **Stop Loss**: 20081.94
- **Risk**: 14.89 points
- **TP 1RR**: 20111.72 ✅
- **TP 2RR**: 20126.61 ✅
- **TP 3RR**: 20141.51 ✅
- **TP 4RR**: 20156.40 ✅
- **TP 15RR**: 20320.20 ✅
- **PnL**: 223.37 points (15.0R)
- **MFE**: 227.48 points
- **MAE**: 13.52 points

### Trade #447 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 04:45:00
- **FVG 5m**: 20169.26 - 20173.34
- **Entrée**: 20176.91 @ 2025-03-19 06:39:00
- **Stop Loss**: 20135.72
- **Risk**: 41.19 points
- **TP 1RR**: 20218.10 ❌
- **TP 2RR**: 20259.28 ❌
- **TP 3RR**: 20300.47 ❌
- **TP 4RR**: 20341.65 ❌
- **TP 15RR**: 20794.70 ❌
- **PnL**: -41.19 points (-1.0R)
- **MFE**: 36.21 points
- **MAE**: 66.05 points

### Trade #448 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 09:00:00
- **FVG 5m**: 20220.01 - 20255.71
- **Entrée**: 20258.52 @ 2025-03-19 10:09:00
- **Stop Loss**: 20211.17
- **Risk**: 47.34 points
- **TP 1RR**: 20305.86 ✅
- **TP 2RR**: 20353.21 ❌
- **TP 3RR**: 20400.55 ❌
- **TP 4RR**: 20447.90 ❌
- **TP 15RR**: 20968.69 ❌
- **PnL**: -47.34 points (-1.0R)
- **MFE**: 79.82 points
- **MAE**: 48.45 points

### Trade #449 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 11:00:00
- **FVG 5m**: 20299.07 - 20307.23
- **Entrée**: 20295.24 @ 2025-03-19 11:13:00
- **Stop Loss**: 20343.66
- **Risk**: 48.42 points
- **TP 1RR**: 20246.82 ✅
- **TP 2RR**: 20198.40 ✅
- **TP 3RR**: 20149.98 ❌
- **TP 4RR**: 20101.56 ❌
- **TP 15RR**: 19568.93 ❌
- **PnL**: -48.42 points (-1.0R)
- **MFE**: 128.79 points
- **MAE**: 59.17 points

### Trade #450 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 13:30:00
- **FVG 5m**: 20408.98 - 20423.01
- **Entrée**: 20423.78 @ 2025-03-19 13:57:00
- **Stop Loss**: 20256.80
- **Risk**: 166.97 points
- **TP 1RR**: 20590.75 ❌
- **TP 2RR**: 20757.72 ❌
- **TP 3RR**: 20924.70 ❌
- **TP 4RR**: 21091.67 ❌
- **TP 15RR**: 22928.39 ❌
- **PnL**: -166.97 points (-1.0R)
- **MFE**: 124.20 points
- **MAE**: 169.59 points

### Trade #451 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-19 13:30:00
- **FVG 5m**: 20408.98 - 20423.01
- **Entrée**: 20423.78 @ 2025-03-19 13:57:00
- **Stop Loss**: 20256.80
- **Risk**: 166.97 points
- **TP 1RR**: 20590.75 ❌
- **TP 2RR**: 20757.72 ❌
- **TP 3RR**: 20924.70 ❌
- **TP 4RR**: 21091.67 ❌
- **TP 15RR**: 22928.39 ❌
- **PnL**: -166.97 points (-1.0R)
- **MFE**: 124.20 points
- **MAE**: 169.59 points

### Trade #452 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 14:15:00
- **FVG 5m**: 20379.15 - 20397.25
- **Entrée**: 20367.16 @ 2025-03-19 14:52:00
- **Stop Loss**: 20526.10
- **Risk**: 158.94 points
- **TP 1RR**: 20208.22 ✅
- **TP 2RR**: 20049.28 ✅
- **TP 3RR**: 19890.34 ❌
- **TP 4RR**: 19731.41 ❌
- **TP 15RR**: 17983.09 ❌
- **PnL**: -158.94 points (-1.0R)
- **MFE**: 370.81 points
- **MAE**: 161.94 points

### Trade #453 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-19 14:15:00
- **FVG 5m**: 20379.15 - 20397.25
- **Entrée**: 20367.16 @ 2025-03-19 14:52:00
- **Stop Loss**: 20526.10
- **Risk**: 158.94 points
- **TP 1RR**: 20208.22 ✅
- **TP 2RR**: 20049.28 ✅
- **TP 3RR**: 19890.34 ❌
- **TP 4RR**: 19731.41 ❌
- **TP 15RR**: 17983.09 ❌
- **PnL**: -158.94 points (-1.0R)
- **MFE**: 370.81 points
- **MAE**: 161.94 points

### Trade #454 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 05:00:00
- **FVG 5m**: 20264.89 - 20297.03
- **Entrée**: 20254.69 @ 2025-03-20 05:12:00
- **Stop Loss**: 20367.39
- **Risk**: 112.70 points
- **TP 1RR**: 20141.99 ✅
- **TP 2RR**: 20029.29 ❌
- **TP 3RR**: 19916.60 ❌
- **TP 4RR**: 19803.90 ❌
- **TP 15RR**: 18564.21 ❌
- **PnL**: -112.70 points (-1.0R)
- **MFE**: 122.67 points
- **MAE**: 126.75 points

### Trade #455 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-20 05:15:00
- **FVG 5m**: 20190.43 - 20204.45
- **Entrée**: 20205.73 @ 2025-03-20 05:52:00
- **Stop Loss**: 20121.96
- **Risk**: 83.77 points
- **TP 1RR**: 20289.50 ✅
- **TP 2RR**: 20373.27 ✅
- **TP 3RR**: 20457.03 ✅
- **TP 4RR**: 20540.80 ❌
- **TP 15RR**: 21462.26 ❌
- **PnL**: -83.77 points (-1.0R)
- **MFE**: 303.48 points
- **MAE**: 100.23 points

### Trade #456 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 09:15:00
- **FVG 5m**: 20473.51 - 20486.26
- **Entrée**: 20463.56 @ 2025-03-20 09:52:00
- **Stop Loss**: 20500.84
- **Risk**: 37.28 points
- **TP 1RR**: 20426.28 ✅
- **TP 2RR**: 20389.00 ✅
- **TP 3RR**: 20351.73 ✅
- **TP 4RR**: 20314.45 ✅
- **TP 15RR**: 19904.39 ❌
- **PnL**: -37.28 points (-1.0R)
- **MFE**: 467.21 points
- **MAE**: 39.53 points

### Trade #457 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-20 09:15:00
- **FVG 5m**: 20406.18 - 20416.89
- **Entrée**: 20424.29 @ 2025-03-20 10:42:00
- **Stop Loss**: 20366.66
- **Risk**: 57.62 points
- **TP 1RR**: 20481.91 ❌
- **TP 2RR**: 20539.53 ❌
- **TP 3RR**: 20597.16 ❌
- **TP 4RR**: 20654.78 ❌
- **TP 15RR**: 21288.64 ❌
- **PnL**: -57.62 points (-1.0R)
- **MFE**: 34.68 points
- **MAE**: 71.15 points

### Trade #458 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 09:45:00
- **FVG 5m**: 20406.18 - 20425.05
- **Entrée**: 20403.12 @ 2025-03-20 10:33:00
- **Stop Loss**: 20519.46
- **Risk**: 116.35 points
- **TP 1RR**: 20286.77 ✅
- **TP 2RR**: 20170.43 ✅
- **TP 3RR**: 20054.08 ✅
- **TP 4RR**: 19937.74 ❌
- **TP 15RR**: 18657.94 ❌
- **PnL**: -116.35 points (-1.0R)
- **MFE**: 406.77 points
- **MAE**: 119.61 points

### Trade #459 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-20 12:15:00
- **FVG 5m**: 20256.73 - 20266.68
- **Entrée**: 20248.32 @ 2025-03-20 12:54:00
- **Stop Loss**: 20339.07
- **Risk**: 90.75 points
- **TP 1RR**: 20157.56 ✅
- **TP 2RR**: 20066.81 ✅
- **TP 3RR**: 19976.06 ❌
- **TP 4RR**: 19885.31 ❌
- **TP 15RR**: 18887.03 ❌
- **PnL**: -90.75 points (-1.0R)
- **MFE**: 251.97 points
- **MAE**: 96.14 points

### Trade #460 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 00:45:00
- **FVG 5m**: 20272.54 - 20281.73
- **Entrée**: 20285.30 @ 2025-03-21 01:54:00
- **Stop Loss**: 20211.43
- **Risk**: 73.87 points
- **TP 1RR**: 20359.16 ❌
- **TP 2RR**: 20433.03 ❌
- **TP 3RR**: 20506.90 ❌
- **TP 4RR**: 20580.77 ❌
- **TP 15RR**: 21393.31 ❌
- **PnL**: -73.87 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 77.78 points

### Trade #461 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 01:30:00
- **FVG 5m**: 20272.54 - 20281.73
- **Entrée**: 20285.30 @ 2025-03-21 01:54:00
- **Stop Loss**: 20238.70
- **Risk**: 46.59 points
- **TP 1RR**: 20331.89 ❌
- **TP 2RR**: 20378.48 ❌
- **TP 3RR**: 20425.08 ❌
- **TP 4RR**: 20471.67 ❌
- **TP 15RR**: 20984.19 ❌
- **PnL**: -46.59 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 49.48 points

### Trade #462 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 03:45:00
- **FVG 5m**: 20196.04 - 20214.40
- **Entrée**: 20221.03 @ 2025-03-21 05:04:00
- **Stop Loss**: 20154.33
- **Risk**: 66.70 points
- **TP 1RR**: 20287.73 ❌
- **TP 2RR**: 20354.43 ❌
- **TP 3RR**: 20421.12 ❌
- **TP 4RR**: 20487.82 ❌
- **TP 15RR**: 21221.50 ❌
- **PnL**: -66.70 points (-1.0R)
- **MFE**: 23.21 points
- **MAE**: 71.66 points

### Trade #463 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 05:00:00
- **FVG 5m**: 20198.33 - 20207.00
- **Entrée**: 20213.12 @ 2025-03-21 07:02:00
- **Stop Loss**: 20184.15
- **Risk**: 28.97 points
- **TP 1RR**: 20242.09 ❌
- **TP 2RR**: 20271.06 ❌
- **TP 3RR**: 20300.03 ❌
- **TP 4RR**: 20329.00 ❌
- **TP 15RR**: 20647.66 ❌
- **PnL**: -28.97 points (-1.0R)
- **MFE**: 15.56 points
- **MAE**: 37.74 points

### Trade #464 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 08:30:00
- **FVG 5m**: 20055.26 - 20058.32
- **Entrée**: 20068.01 @ 2025-03-21 08:45:00
- **Stop Loss**: 19991.71
- **Risk**: 76.31 points
- **TP 1RR**: 20144.32 ✅
- **TP 2RR**: 20220.63 ✅
- **TP 3RR**: 20296.94 ✅
- **TP 4RR**: 20373.24 ✅
- **TP 15RR**: 21212.63 ❌
- **PnL**: -76.31 points (-1.0R)
- **MFE**: 881.63 points
- **MAE**: 83.65 points

### Trade #465 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 08:30:00
- **FVG 5m**: 20055.26 - 20058.32
- **Entrée**: 20068.01 @ 2025-03-21 08:45:00
- **Stop Loss**: 19991.71
- **Risk**: 76.31 points
- **TP 1RR**: 20144.32 ✅
- **TP 2RR**: 20220.63 ✅
- **TP 3RR**: 20296.94 ✅
- **TP 4RR**: 20373.24 ✅
- **TP 15RR**: 21212.63 ❌
- **PnL**: -76.31 points (-1.0R)
- **MFE**: 881.63 points
- **MAE**: 83.65 points

### Trade #466 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 08:45:00
- **FVG 5m**: 20132.28 - 20134.83
- **Entrée**: 20142.48 @ 2025-03-21 09:22:00
- **Stop Loss**: 20048.29
- **Risk**: 94.19 points
- **TP 1RR**: 20236.67 ✅
- **TP 2RR**: 20330.86 ✅
- **TP 3RR**: 20425.04 ✅
- **TP 4RR**: 20519.23 ✅
- **TP 15RR**: 21555.30 ❌
- **PnL**: -94.19 points (-1.0R)
- **MFE**: 807.16 points
- **MAE**: 96.14 points

### Trade #467 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 09:15:00
- **FVG 5m**: 20149.62 - 20179.97
- **Entrée**: 20182.27 @ 2025-03-21 09:58:00
- **Stop Loss**: 20081.94
- **Risk**: 100.33 points
- **TP 1RR**: 20282.59 ❌
- **TP 2RR**: 20382.92 ❌
- **TP 3RR**: 20483.24 ❌
- **TP 4RR**: 20583.57 ❌
- **TP 15RR**: 21687.14 ❌
- **PnL**: -100.33 points (-1.0R)
- **MFE**: 28.05 points
- **MAE**: 101.25 points

### Trade #468 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 09:45:00
- **FVG 5m**: 20149.62 - 20179.97
- **Entrée**: 20182.27 @ 2025-03-21 09:58:00
- **Stop Loss**: 20104.12
- **Risk**: 78.15 points
- **TP 1RR**: 20260.41 ❌
- **TP 2RR**: 20338.56 ❌
- **TP 3RR**: 20416.71 ❌
- **TP 4RR**: 20494.86 ❌
- **TP 15RR**: 21354.50 ❌
- **PnL**: -78.15 points (-1.0R)
- **MFE**: 28.05 points
- **MAE**: 87.98 points

### Trade #469 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-21 09:45:00
- **FVG 5m**: 20149.62 - 20179.97
- **Entrée**: 20182.27 @ 2025-03-21 09:58:00
- **Stop Loss**: 20104.12
- **Risk**: 78.15 points
- **TP 1RR**: 20260.41 ❌
- **TP 2RR**: 20338.56 ❌
- **TP 3RR**: 20416.71 ❌
- **TP 4RR**: 20494.86 ❌
- **TP 15RR**: 21354.50 ❌
- **PnL**: -78.15 points (-1.0R)
- **MFE**: 28.05 points
- **MAE**: 87.98 points

### Trade #470 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-21 11:30:00
- **FVG 5m**: 20253.42 - 20260.81
- **Entrée**: 20251.89 @ 2025-03-21 12:11:00
- **Stop Loss**: 20282.94
- **Risk**: 31.05 points
- **TP 1RR**: 20220.84 ✅
- **TP 2RR**: 20189.79 ❌
- **TP 3RR**: 20158.74 ❌
- **TP 4RR**: 20127.69 ❌
- **TP 15RR**: 19786.16 ❌
- **PnL**: -31.05 points (-1.0R)
- **MFE**: 52.54 points
- **MAE**: 37.74 points

### Trade #471 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-21 11:30:00
- **FVG 5m**: 20253.42 - 20260.81
- **Entrée**: 20251.89 @ 2025-03-21 12:11:00
- **Stop Loss**: 20282.94
- **Risk**: 31.05 points
- **TP 1RR**: 20220.84 ✅
- **TP 2RR**: 20189.79 ❌
- **TP 3RR**: 20158.74 ❌
- **TP 4RR**: 20127.69 ❌
- **TP 15RR**: 19786.16 ❌
- **PnL**: -31.05 points (-1.0R)
- **MFE**: 52.54 points
- **MAE**: 37.74 points

### Trade #472 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-23 20:30:00
- **FVG 5m**: 20514.31 - 20517.37
- **Entrée**: 20514.05 @ 2025-03-23 22:29:00
- **Stop Loss**: 20538.86
- **Risk**: 24.80 points
- **TP 1RR**: 20489.25 ❌
- **TP 2RR**: 20464.45 ❌
- **TP 3RR**: 20439.65 ❌
- **TP 4RR**: 20414.85 ❌
- **TP 15RR**: 20142.04 ❌
- **PnL**: -24.80 points (-1.0R)
- **MFE**: 14.03 points
- **MAE**: 26.52 points

### Trade #473 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-24 08:45:00
- **FVG 5m**: 20728.53 - 20732.87
- **Entrée**: 20735.16 @ 2025-03-24 09:16:00
- **Stop Loss**: 20659.29
- **Risk**: 75.88 points
- **TP 1RR**: 20811.04 ✅
- **TP 2RR**: 20886.92 ✅
- **TP 3RR**: 20962.79 ❌
- **TP 4RR**: 21038.67 ❌
- **TP 15RR**: 21873.31 ❌
- **PnL**: -75.88 points (-1.0R)
- **MFE**: 214.48 points
- **MAE**: 85.43 points

### Trade #474 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 11:15:00
- **FVG 5m**: 20757.09 - 20765.26
- **Entrée**: 20752.25 @ 2025-03-24 11:26:00
- **Stop Loss**: 20795.03
- **Risk**: 42.78 points
- **TP 1RR**: 20709.47 ❌
- **TP 2RR**: 20666.69 ❌
- **TP 3RR**: 20623.91 ❌
- **TP 4RR**: 20581.13 ❌
- **TP 15RR**: 20110.54 ❌
- **PnL**: -42.78 points (-1.0R)
- **MFE**: 35.70 points
- **MAE**: 48.71 points

### Trade #475 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 14:00:00
- **FVG 5m**: 20770.36 - 20773.16
- **Entrée**: 20769.08 @ 2025-03-24 15:54:00
- **Stop Loss**: 20811.87
- **Risk**: 42.79 points
- **TP 1RR**: 20726.29 ✅
- **TP 2RR**: 20683.50 ❌
- **TP 3RR**: 20640.71 ❌
- **TP 4RR**: 20597.92 ❌
- **TP 15RR**: 20127.24 ❌
- **PnL**: -42.79 points (-1.0R)
- **MFE**: 68.09 points
- **MAE**: 45.14 points

### Trade #476 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 14:15:00
- **FVG 5m**: 20770.36 - 20773.16
- **Entrée**: 20769.08 @ 2025-03-24 15:54:00
- **Stop Loss**: 20807.28
- **Risk**: 38.20 points
- **TP 1RR**: 20730.88 ✅
- **TP 2RR**: 20692.69 ❌
- **TP 3RR**: 20654.49 ❌
- **TP 4RR**: 20616.30 ❌
- **TP 15RR**: 20196.14 ❌
- **PnL**: -38.20 points (-1.0R)
- **MFE**: 68.09 points
- **MAE**: 40.29 points

### Trade #477 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-24 14:45:00
- **FVG 5m**: 20770.36 - 20773.16
- **Entrée**: 20769.08 @ 2025-03-24 15:54:00
- **Stop Loss**: 20830.24
- **Risk**: 61.16 points
- **TP 1RR**: 20707.92 ✅
- **TP 2RR**: 20646.76 ❌
- **TP 3RR**: 20585.60 ❌
- **TP 4RR**: 20524.44 ❌
- **TP 15RR**: 19851.68 ❌
- **PnL**: -61.16 points (-1.0R)
- **MFE**: 68.09 points
- **MAE**: 68.09 points

### Trade #478 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-25 04:30:00
- **FVG 5m**: 20742.81 - 20755.82
- **Entrée**: 20760.41 @ 2025-03-25 05:20:00
- **Stop Loss**: 20710.01
- **Risk**: 50.40 points
- **TP 1RR**: 20810.81 ✅
- **TP 2RR**: 20861.21 ✅
- **TP 3RR**: 20911.61 ✅
- **TP 4RR**: 20962.01 ❌
- **TP 15RR**: 21516.40 ❌
- **PnL**: -50.40 points (-1.0R)
- **MFE**: 189.23 points
- **MAE**: 53.05 points

### Trade #479 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-25 04:45:00
- **FVG 5m**: 20742.81 - 20755.82
- **Entrée**: 20760.41 @ 2025-03-25 05:20:00
- **Stop Loss**: 20727.09
- **Risk**: 33.32 points
- **TP 1RR**: 20793.73 ✅
- **TP 2RR**: 20827.05 ✅
- **TP 3RR**: 20860.37 ✅
- **TP 4RR**: 20893.69 ✅
- **TP 15RR**: 21260.23 ❌
- **PnL**: -33.32 points (-1.0R)
- **MFE**: 189.23 points
- **MAE**: 45.14 points

### Trade #480 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-25 05:00:00
- **FVG 5m**: 20742.81 - 20755.82
- **Entrée**: 20760.41 @ 2025-03-25 05:20:00
- **Stop Loss**: 20718.93
- **Risk**: 41.48 points
- **TP 1RR**: 20801.89 ✅
- **TP 2RR**: 20843.37 ✅
- **TP 3RR**: 20884.84 ✅
- **TP 4RR**: 20926.32 ✅
- **TP 15RR**: 21382.58 ❌
- **PnL**: -41.48 points (-1.0R)
- **MFE**: 189.23 points
- **MAE**: 45.14 points

### Trade #481 - ❌ PERDANT

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

### Trade #482 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 21:00:00
- **FVG 5m**: 20893.28 - 20907.56
- **Entrée**: 20890.98 @ 2025-03-25 21:24:00
- **Stop Loss**: 20935.87
- **Risk**: 44.89 points
- **TP 1RR**: 20846.09 ✅
- **TP 2RR**: 20801.20 ✅
- **TP 3RR**: 20756.31 ✅
- **TP 4RR**: 20711.42 ✅
- **TP 15RR**: 20217.61 ✅
- **PnL**: 673.37 points (15.0R)
- **MFE**: 678.62 points
- **MAE**: 19.38 points

### Trade #483 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-25 21:15:00
- **FVG 5m**: 20893.28 - 20895.57
- **Entrée**: 20892.51 @ 2025-03-25 22:32:00
- **Stop Loss**: 20924.39
- **Risk**: 31.88 points
- **TP 1RR**: 20860.63 ✅
- **TP 2RR**: 20828.76 ✅
- **TP 3RR**: 20796.88 ✅
- **TP 4RR**: 20765.00 ✅
- **TP 15RR**: 20414.33 ✅
- **PnL**: 478.19 points (15.0R)
- **MFE**: 480.21 points
- **MAE**: 17.85 points

### Trade #484 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 03:00:00
- **FVG 5m**: 20867.52 - 20872.11
- **Entrée**: 20873.13 @ 2025-03-26 03:26:00
- **Stop Loss**: 20841.28
- **Risk**: 31.85 points
- **TP 1RR**: 20904.98 ❌
- **TP 2RR**: 20936.83 ❌
- **TP 3RR**: 20968.68 ❌
- **TP 4RR**: 21000.52 ❌
- **TP 15RR**: 21350.85 ❌
- **PnL**: -31.85 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 32.90 points

### Trade #485 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 05:00:00
- **FVG 5m**: 20873.64 - 20877.21
- **Entrée**: 20881.55 @ 2025-03-26 05:56:00
- **Stop Loss**: 20829.81
- **Risk**: 51.73 points
- **TP 1RR**: 20933.28 ❌
- **TP 2RR**: 20985.02 ❌
- **TP 3RR**: 21036.75 ❌
- **TP 4RR**: 21088.48 ❌
- **TP 15RR**: 21657.56 ❌
- **PnL**: -51.73 points (-1.0R)
- **MFE**: 23.46 points
- **MAE**: 56.11 points

### Trade #486 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 05:45:00
- **FVG 5m**: 20873.64 - 20877.21
- **Entrée**: 20881.55 @ 2025-03-26 05:56:00
- **Stop Loss**: 20856.58
- **Risk**: 24.97 points
- **TP 1RR**: 20906.52 ❌
- **TP 2RR**: 20931.49 ❌
- **TP 3RR**: 20956.46 ❌
- **TP 4RR**: 20981.43 ❌
- **TP 15RR**: 21256.10 ❌
- **PnL**: -24.97 points (-1.0R)
- **MFE**: 23.46 points
- **MAE**: 25.76 points

### Trade #487 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 08:45:00
- **FVG 5m**: 20765.51 - 20768.06
- **Entrée**: 20753.01 @ 2025-03-26 08:56:00
- **Stop Loss**: 20876.17
- **Risk**: 123.15 points
- **TP 1RR**: 20629.86 ✅
- **TP 2RR**: 20506.71 ✅
- **TP 3RR**: 20383.55 ✅
- **TP 4RR**: 20260.40 ✅
- **TP 15RR**: 18905.70 ✅
- **PnL**: 1847.32 points (15.0R)
- **MFE**: 1859.91 points
- **MAE**: 12.50 points

### Trade #488 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 10:45:00
- **FVG 5m**: 20559.96 - 20575.77
- **Entrée**: 20559.19 @ 2025-03-26 11:54:00
- **Stop Loss**: 20679.45
- **Risk**: 120.25 points
- **TP 1RR**: 20438.94 ✅
- **TP 2RR**: 20318.69 ✅
- **TP 3RR**: 20198.44 ✅
- **TP 4RR**: 20078.19 ✅
- **TP 15RR**: 18755.43 ✅
- **PnL**: 1803.76 points (15.0R)
- **MFE**: 1851.24 points
- **MAE**: 46.41 points

### Trade #489 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 11:45:00
- **FVG 5m**: 20505.13 - 20517.12
- **Entrée**: 20503.09 @ 2025-03-26 12:32:00
- **Stop Loss**: 20614.38
- **Risk**: 111.29 points
- **TP 1RR**: 20391.80 ✅
- **TP 2RR**: 20280.50 ✅
- **TP 3RR**: 20169.21 ✅
- **TP 4RR**: 20057.92 ✅
- **TP 15RR**: 18833.70 ✅
- **PnL**: 1669.39 points (15.0R)
- **MFE**: 1673.99 points
- **MAE**: 102.52 points

### Trade #490 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 11:45:00
- **FVG 5m**: 20505.13 - 20517.12
- **Entrée**: 20503.09 @ 2025-03-26 12:32:00
- **Stop Loss**: 20614.38
- **Risk**: 111.29 points
- **TP 1RR**: 20391.80 ✅
- **TP 2RR**: 20280.50 ✅
- **TP 3RR**: 20169.21 ✅
- **TP 4RR**: 20057.92 ✅
- **TP 15RR**: 18833.70 ✅
- **PnL**: 1669.39 points (15.0R)
- **MFE**: 1673.99 points
- **MAE**: 102.52 points

### Trade #491 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 11:45:00
- **FVG 5m**: 20505.13 - 20517.12
- **Entrée**: 20503.09 @ 2025-03-26 12:32:00
- **Stop Loss**: 20614.38
- **Risk**: 111.29 points
- **TP 1RR**: 20391.80 ✅
- **TP 2RR**: 20280.50 ✅
- **TP 3RR**: 20169.21 ✅
- **TP 4RR**: 20057.92 ✅
- **TP 15RR**: 18833.70 ✅
- **PnL**: 1669.39 points (15.0R)
- **MFE**: 1673.99 points
- **MAE**: 102.52 points

### Trade #492 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 12:15:00
- **FVG 5m**: 20505.13 - 20517.12
- **Entrée**: 20503.09 @ 2025-03-26 12:32:00
- **Stop Loss**: 20562.33
- **Risk**: 59.24 points
- **TP 1RR**: 20443.85 ✅
- **TP 2RR**: 20384.61 ✅
- **TP 3RR**: 20325.37 ❌
- **TP 4RR**: 20266.12 ❌
- **TP 15RR**: 19614.47 ❌
- **PnL**: -59.24 points (-1.0R)
- **MFE**: 165.00 points
- **MAE**: 71.15 points

### Trade #493 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-26 12:30:00
- **FVG 5m**: 20525.28 - 20527.83
- **Entrée**: 20518.90 @ 2025-03-26 13:34:00
- **Stop Loss**: 20544.21
- **Risk**: 25.31 points
- **TP 1RR**: 20493.59 ✅
- **TP 2RR**: 20468.27 ✅
- **TP 3RR**: 20442.96 ✅
- **TP 4RR**: 20417.65 ✅
- **TP 15RR**: 20139.20 ❌
- **PnL**: -25.31 points (-1.0R)
- **MFE**: 113.49 points
- **MAE**: 27.80 points

### Trade #494 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 12:30:00
- **FVG 5m**: 20506.40 - 20518.65
- **Entrée**: 20524.77 @ 2025-03-26 13:12:00
- **Stop Loss**: 20469.90
- **Risk**: 54.87 points
- **TP 1RR**: 20579.64 ❌
- **TP 2RR**: 20634.51 ❌
- **TP 3RR**: 20689.37 ❌
- **TP 4RR**: 20744.24 ❌
- **TP 15RR**: 21347.81 ❌
- **PnL**: -54.87 points (-1.0R)
- **MFE**: 26.78 points
- **MAE**: 67.33 points

### Trade #495 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 12:30:00
- **FVG 5m**: 20506.40 - 20518.65
- **Entrée**: 20524.77 @ 2025-03-26 13:12:00
- **Stop Loss**: 20469.90
- **Risk**: 54.87 points
- **TP 1RR**: 20579.64 ❌
- **TP 2RR**: 20634.51 ❌
- **TP 3RR**: 20689.37 ❌
- **TP 4RR**: 20744.24 ❌
- **TP 15RR**: 21347.81 ❌
- **PnL**: -54.87 points (-1.0R)
- **MFE**: 26.78 points
- **MAE**: 67.33 points

### Trade #496 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-26 18:30:00
- **FVG 5m**: 20446.98 - 20451.06
- **Entrée**: 20451.32 @ 2025-03-26 18:42:00
- **Stop Loss**: 20425.29
- **Risk**: 26.03 points
- **TP 1RR**: 20477.35 ✅
- **TP 2RR**: 20503.38 ✅
- **TP 3RR**: 20529.41 ✅
- **TP 4RR**: 20555.44 ❌
- **TP 15RR**: 20841.76 ❌
- **PnL**: -26.03 points (-1.0R)
- **MFE**: 101.50 points
- **MAE**: 28.82 points

### Trade #497 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 08:45:00
- **FVG 5m**: 20499.77 - 20510.74
- **Entrée**: 20525.28 @ 2025-03-27 09:29:00
- **Stop Loss**: 20351.88
- **Risk**: 173.40 points
- **TP 1RR**: 20698.67 ❌
- **TP 2RR**: 20872.07 ❌
- **TP 3RR**: 21045.47 ❌
- **TP 4RR**: 21218.87 ❌
- **TP 15RR**: 23126.24 ❌
- **PnL**: -173.40 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 178.01 points

### Trade #498 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 08:45:00
- **FVG 5m**: 20499.77 - 20510.74
- **Entrée**: 20525.28 @ 2025-03-27 09:29:00
- **Stop Loss**: 20351.88
- **Risk**: 173.40 points
- **TP 1RR**: 20698.67 ❌
- **TP 2RR**: 20872.07 ❌
- **TP 3RR**: 21045.47 ❌
- **TP 4RR**: 21218.87 ❌
- **TP 15RR**: 23126.24 ❌
- **PnL**: -173.40 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 178.01 points

### Trade #499 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 08:45:00
- **FVG 5m**: 20499.77 - 20510.74
- **Entrée**: 20525.28 @ 2025-03-27 09:29:00
- **Stop Loss**: 20351.88
- **Risk**: 173.40 points
- **TP 1RR**: 20698.67 ❌
- **TP 2RR**: 20872.07 ❌
- **TP 3RR**: 21045.47 ❌
- **TP 4RR**: 21218.87 ❌
- **TP 15RR**: 23126.24 ❌
- **PnL**: -173.40 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 178.01 points

### Trade #500 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:15:00
- **FVG 5m**: 20540.07 - 20543.64
- **Entrée**: 20538.54 @ 2025-03-27 10:29:00
- **Stop Loss**: 20585.29
- **Risk**: 46.76 points
- **TP 1RR**: 20491.78 ✅
- **TP 2RR**: 20445.02 ✅
- **TP 3RR**: 20398.27 ✅
- **TP 4RR**: 20351.51 ✅
- **TP 15RR**: 19837.19 ✅
- **PnL**: 701.34 points (15.0R)
- **MFE**: 702.34 points
- **MAE**: 22.44 points

### Trade #501 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:15:00
- **FVG 5m**: 20540.07 - 20543.64
- **Entrée**: 20538.54 @ 2025-03-27 10:29:00
- **Stop Loss**: 20585.29
- **Risk**: 46.76 points
- **TP 1RR**: 20491.78 ✅
- **TP 2RR**: 20445.02 ✅
- **TP 3RR**: 20398.27 ✅
- **TP 4RR**: 20351.51 ✅
- **TP 15RR**: 19837.19 ✅
- **PnL**: 701.34 points (15.0R)
- **MFE**: 702.34 points
- **MAE**: 22.44 points

### Trade #502 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:15:00
- **FVG 5m**: 20540.07 - 20543.64
- **Entrée**: 20538.54 @ 2025-03-27 10:29:00
- **Stop Loss**: 20585.29
- **Risk**: 46.76 points
- **TP 1RR**: 20491.78 ✅
- **TP 2RR**: 20445.02 ✅
- **TP 3RR**: 20398.27 ✅
- **TP 4RR**: 20351.51 ✅
- **TP 15RR**: 19837.19 ✅
- **PnL**: 701.34 points (15.0R)
- **MFE**: 702.34 points
- **MAE**: 22.44 points

### Trade #503 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-27 10:30:00
- **FVG 5m**: 20455.65 - 20481.41
- **Entrée**: 20450.30 @ 2025-03-27 11:49:00
- **Stop Loss**: 20550.34
- **Risk**: 100.04 points
- **TP 1RR**: 20350.26 ✅
- **TP 2RR**: 20250.22 ✅
- **TP 3RR**: 20150.18 ✅
- **TP 4RR**: 20050.14 ✅
- **TP 15RR**: 18949.71 ✅
- **PnL**: 1500.59 points (15.0R)
- **MFE**: 1501.85 points
- **MAE**: 84.16 points

### Trade #504 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-27 15:00:00
- **FVG 5m**: 20407.71 - 20411.79
- **Entrée**: 20412.04 @ 2025-03-27 15:37:00
- **Stop Loss**: 20381.45
- **Risk**: 30.60 points
- **TP 1RR**: 20442.64 ❌
- **TP 2RR**: 20473.24 ❌
- **TP 3RR**: 20503.84 ❌
- **TP 4RR**: 20534.44 ❌
- **TP 15RR**: 20871.01 ❌
- **PnL**: -30.60 points (-1.0R)
- **MFE**: 9.44 points
- **MAE**: 37.49 points

### Trade #505 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 01:45:00
- **FVG 5m**: 20335.03 - 20337.83
- **Entrée**: 20334.26 @ 2025-03-28 01:56:00
- **Stop Loss**: 20395.97
- **Risk**: 61.71 points
- **TP 1RR**: 20272.55 ✅
- **TP 2RR**: 20210.84 ✅
- **TP 3RR**: 20149.14 ✅
- **TP 4RR**: 20087.43 ✅
- **TP 15RR**: 19408.64 ✅
- **PnL**: 925.62 points (15.0R)
- **MFE**: 939.01 points
- **MAE**: 36.98 points

### Trade #506 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 02:30:00
- **FVG 5m**: 20287.08 - 20290.40
- **Entrée**: 20266.68 @ 2025-03-28 02:47:00
- **Stop Loss**: 20341.62
- **Risk**: 74.94 points
- **TP 1RR**: 20191.74 ❌
- **TP 2RR**: 20116.79 ❌
- **TP 3RR**: 20041.85 ❌
- **TP 4RR**: 19966.91 ❌
- **TP 15RR**: 19142.54 ❌
- **PnL**: -74.94 points (-1.0R)
- **MFE**: 22.44 points
- **MAE**: 85.69 points

### Trade #507 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 02:30:00
- **FVG 5m**: 20287.08 - 20290.40
- **Entrée**: 20266.68 @ 2025-03-28 02:47:00
- **Stop Loss**: 20341.62
- **Risk**: 74.94 points
- **TP 1RR**: 20191.74 ❌
- **TP 2RR**: 20116.79 ❌
- **TP 3RR**: 20041.85 ❌
- **TP 4RR**: 19966.91 ❌
- **TP 15RR**: 19142.54 ❌
- **PnL**: -74.94 points (-1.0R)
- **MFE**: 22.44 points
- **MAE**: 85.69 points

### Trade #508 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 05:00:00
- **FVG 5m**: 20330.18 - 20337.58
- **Entrée**: 20339.62 @ 2025-03-28 05:11:00
- **Stop Loss**: 20296.82
- **Risk**: 42.80 points
- **TP 1RR**: 20382.41 ❌
- **TP 2RR**: 20425.21 ❌
- **TP 3RR**: 20468.01 ❌
- **TP 4RR**: 20510.80 ❌
- **TP 15RR**: 20981.57 ❌
- **PnL**: -42.80 points (-1.0R)
- **MFE**: 31.62 points
- **MAE**: 49.48 points

### Trade #509 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 05:00:00
- **FVG 5m**: 20330.18 - 20337.58
- **Entrée**: 20339.62 @ 2025-03-28 05:11:00
- **Stop Loss**: 20296.82
- **Risk**: 42.80 points
- **TP 1RR**: 20382.41 ❌
- **TP 2RR**: 20425.21 ❌
- **TP 3RR**: 20468.01 ❌
- **TP 4RR**: 20510.80 ❌
- **TP 15RR**: 20981.57 ❌
- **PnL**: -42.80 points (-1.0R)
- **MFE**: 31.62 points
- **MAE**: 49.48 points

### Trade #510 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 05:30:00
- **FVG 5m**: 20335.54 - 20340.38
- **Entrée**: 20341.91 @ 2025-03-28 06:17:00
- **Stop Loss**: 20337.86
- **Risk**: 4.05 points
- **TP 1RR**: 20345.97 ✅
- **TP 2RR**: 20350.02 ✅
- **TP 3RR**: 20354.07 ❌
- **TP 4RR**: 20358.13 ❌
- **TP 15RR**: 20402.71 ❌
- **PnL**: -4.05 points (-1.0R)
- **MFE**: 10.97 points
- **MAE**: 4.59 points

### Trade #511 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-28 07:30:00
- **FVG 5m**: 20269.74 - 20278.16
- **Entrée**: 20263.11 @ 2025-03-28 07:59:00
- **Stop Loss**: 20349.79
- **Risk**: 86.68 points
- **TP 1RR**: 20176.43 ❌
- **TP 2RR**: 20089.75 ❌
- **TP 3RR**: 20003.08 ❌
- **TP 4RR**: 19916.40 ❌
- **TP 15RR**: 18962.94 ❌
- **PnL**: -86.68 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 104.31 points

### Trade #512 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 09:30:00
- **FVG 5m**: 19976.20 - 19978.75
- **Entrée**: 19981.56 @ 2025-03-28 10:19:00
- **Stop Loss**: 19970.29
- **Risk**: 11.27 points
- **TP 1RR**: 19992.83 ✅
- **TP 2RR**: 20004.09 ❌
- **TP 3RR**: 20015.36 ❌
- **TP 4RR**: 20026.62 ❌
- **TP 15RR**: 20150.54 ❌
- **PnL**: -11.27 points (-1.0R)
- **MFE**: 12.75 points
- **MAE**: 21.42 points

### Trade #513 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 09:30:00
- **FVG 5m**: 19976.20 - 19978.75
- **Entrée**: 19981.56 @ 2025-03-28 10:19:00
- **Stop Loss**: 19970.29
- **Risk**: 11.27 points
- **TP 1RR**: 19992.83 ✅
- **TP 2RR**: 20004.09 ❌
- **TP 3RR**: 20015.36 ❌
- **TP 4RR**: 20026.62 ❌
- **TP 15RR**: 20150.54 ❌
- **PnL**: -11.27 points (-1.0R)
- **MFE**: 12.75 points
- **MAE**: 21.42 points

### Trade #514 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 09:30:00
- **FVG 5m**: 19976.20 - 19978.75
- **Entrée**: 19981.56 @ 2025-03-28 10:19:00
- **Stop Loss**: 19970.29
- **Risk**: 11.27 points
- **TP 1RR**: 19992.83 ✅
- **TP 2RR**: 20004.09 ❌
- **TP 3RR**: 20015.36 ❌
- **TP 4RR**: 20026.62 ❌
- **TP 15RR**: 20150.54 ❌
- **PnL**: -11.27 points (-1.0R)
- **MFE**: 12.75 points
- **MAE**: 21.42 points

### Trade #515 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-28 10:00:00
- **FVG 5m**: 19976.20 - 19978.75
- **Entrée**: 19981.56 @ 2025-03-28 10:19:00
- **Stop Loss**: 19938.18
- **Risk**: 43.38 points
- **TP 1RR**: 20024.94 ✅
- **TP 2RR**: 20068.32 ❌
- **TP 3RR**: 20111.71 ❌
- **TP 4RR**: 20155.09 ❌
- **TP 15RR**: 20632.30 ❌
- **PnL**: -43.38 points (-1.0R)
- **MFE**: 45.14 points
- **MAE**: 46.67 points

### Trade #516 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-31 03:15:00
- **FVG 5m**: 19589.58 - 19595.96
- **Entrée**: 19577.60 @ 2025-03-31 04:00:00
- **Stop Loss**: 19668.53
- **Risk**: 90.93 points
- **TP 1RR**: 19486.67 ✅
- **TP 2RR**: 19395.74 ✅
- **TP 3RR**: 19304.82 ❌
- **TP 4RR**: 19213.89 ❌
- **TP 15RR**: 18213.68 ❌
- **PnL**: -90.93 points (-1.0R)
- **MFE**: 219.32 points
- **MAE**: 92.32 points

### Trade #517 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 04:15:00
- **FVG 5m**: 19590.60 - 19601.32
- **Entrée**: 19608.71 @ 2025-03-31 04:28:00
- **Stop Loss**: 19547.93
- **Risk**: 60.78 points
- **TP 1RR**: 19669.50 ❌
- **TP 2RR**: 19730.28 ❌
- **TP 3RR**: 19791.06 ❌
- **TP 4RR**: 19851.85 ❌
- **TP 15RR**: 20520.47 ❌
- **PnL**: -60.78 points (-1.0R)
- **MFE**: 11.22 points
- **MAE**: 61.46 points

### Trade #518 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 06:45:00
- **FVG 5m**: 19550.31 - 19558.98
- **Entrée**: 19569.95 @ 2025-03-31 07:31:00
- **Stop Loss**: 19521.67
- **Risk**: 48.27 points
- **TP 1RR**: 19618.22 ✅
- **TP 2RR**: 19666.50 ❌
- **TP 3RR**: 19714.77 ❌
- **TP 4RR**: 19763.05 ❌
- **TP 15RR**: 20294.07 ❌
- **PnL**: -48.27 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 54.58 points

### Trade #519 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 06:45:00
- **FVG 5m**: 19550.31 - 19558.98
- **Entrée**: 19569.95 @ 2025-03-31 07:31:00
- **Stop Loss**: 19521.67
- **Risk**: 48.27 points
- **TP 1RR**: 19618.22 ✅
- **TP 2RR**: 19666.50 ❌
- **TP 3RR**: 19714.77 ❌
- **TP 4RR**: 19763.05 ❌
- **TP 15RR**: 20294.07 ❌
- **PnL**: -48.27 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 54.58 points

### Trade #520 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 07:15:00
- **FVG 5m**: 19550.31 - 19558.98
- **Entrée**: 19569.95 @ 2025-03-31 07:31:00
- **Stop Loss**: 19523.71
- **Risk**: 46.24 points
- **TP 1RR**: 19616.18 ✅
- **TP 2RR**: 19662.42 ❌
- **TP 3RR**: 19708.65 ❌
- **TP 4RR**: 19754.89 ❌
- **TP 15RR**: 20263.48 ❌
- **PnL**: -46.24 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 54.58 points

### Trade #521 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 09:00:00
- **FVG 5m**: 19471.00 - 19490.12
- **Entrée**: 19518.94 @ 2025-03-31 09:33:00
- **Stop Loss**: 19456.93
- **Risk**: 62.01 points
- **TP 1RR**: 19580.96 ✅
- **TP 2RR**: 19642.97 ✅
- **TP 3RR**: 19704.98 ✅
- **TP 4RR**: 19767.00 ✅
- **TP 15RR**: 20449.15 ❌
- **PnL**: -62.01 points (-1.0R)
- **MFE**: 928.30 points
- **MAE**: 217.54 points

### Trade #522 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-31 10:30:00
- **FVG 5m**: 19593.92 - 19603.87
- **Entrée**: 19592.13 @ 2025-03-31 11:07:00
- **Stop Loss**: 19645.31
- **Risk**: 53.17 points
- **TP 1RR**: 19538.96 ❌
- **TP 2RR**: 19485.79 ❌
- **TP 3RR**: 19432.62 ❌
- **TP 4RR**: 19379.45 ❌
- **TP 15RR**: 18794.55 ❌
- **PnL**: -53.17 points (-1.0R)
- **MFE**: 32.39 points
- **MAE**: 54.58 points

### Trade #523 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-31 11:30:00
- **FVG 5m**: 19633.96 - 19668.64
- **Entrée**: 19626.31 @ 2025-03-31 12:19:00
- **Stop Loss**: 19683.33
- **Risk**: 57.02 points
- **TP 1RR**: 19569.29 ❌
- **TP 2RR**: 19512.28 ❌
- **TP 3RR**: 19455.26 ❌
- **TP 4RR**: 19398.24 ❌
- **TP 15RR**: 18771.06 ❌
- **PnL**: -57.02 points (-1.0R)
- **MFE**: 32.64 points
- **MAE**: 60.19 points

### Trade #524 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-03-31 11:30:00
- **FVG 5m**: 19633.96 - 19668.64
- **Entrée**: 19626.31 @ 2025-03-31 12:19:00
- **Stop Loss**: 19683.33
- **Risk**: 57.02 points
- **TP 1RR**: 19569.29 ❌
- **TP 2RR**: 19512.28 ❌
- **TP 3RR**: 19455.26 ❌
- **TP 4RR**: 19398.24 ❌
- **TP 15RR**: 18771.06 ❌
- **PnL**: -57.02 points (-1.0R)
- **MFE**: 32.64 points
- **MAE**: 60.19 points

### Trade #525 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 13:15:00
- **FVG 5m**: 19761.47 - 19769.12
- **Entrée**: 19780.60 @ 2025-03-31 13:31:00
- **Stop Loss**: 19694.75
- **Risk**: 85.85 points
- **TP 1RR**: 19866.45 ✅
- **TP 2RR**: 19952.30 ❌
- **TP 3RR**: 20038.15 ❌
- **TP 4RR**: 20124.00 ❌
- **TP 15RR**: 21068.35 ❌
- **PnL**: -85.85 points (-1.0R)
- **MFE**: 100.99 points
- **MAE**: 99.97 points

### Trade #526 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-03-31 20:15:00
- **FVG 5m**: 19705.37 - 19721.69
- **Entrée**: 19722.45 @ 2025-03-31 20:44:00
- **Stop Loss**: 19689.14
- **Risk**: 33.31 points
- **TP 1RR**: 19755.77 ✅
- **TP 2RR**: 19789.08 ✅
- **TP 3RR**: 19822.39 ✅
- **TP 4RR**: 19855.70 ✅
- **TP 15RR**: 20222.13 ❌
- **PnL**: -33.31 points (-1.0R)
- **MFE**: 180.81 points
- **MAE**: 33.66 points

### Trade #527 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 00:30:00
- **FVG 5m**: 19758.41 - 19764.53
- **Entrée**: 19755.35 @ 2025-04-01 00:44:00
- **Stop Loss**: 19797.38
- **Risk**: 42.03 points
- **TP 1RR**: 19713.32 ❌
- **TP 2RR**: 19671.30 ❌
- **TP 3RR**: 19629.27 ❌
- **TP 4RR**: 19587.24 ❌
- **TP 15RR**: 19124.95 ❌
- **PnL**: -42.03 points (-1.0R)
- **MFE**: 16.58 points
- **MAE**: 47.69 points

### Trade #528 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 04:00:00
- **FVG 5m**: 19860.93 - 19877.25
- **Entrée**: 19846.14 @ 2025-04-01 05:01:00
- **Stop Loss**: 19891.79
- **Risk**: 45.64 points
- **TP 1RR**: 19800.50 ✅
- **TP 2RR**: 19754.85 ✅
- **TP 3RR**: 19709.21 ✅
- **TP 4RR**: 19663.56 ✅
- **TP 15RR**: 19161.47 ❌
- **PnL**: -45.64 points (-1.0R)
- **MFE**: 197.65 points
- **MAE**: 53.05 points

### Trade #529 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 04:45:00
- **FVG 5m**: 19860.93 - 19877.25
- **Entrée**: 19846.14 @ 2025-04-01 05:01:00
- **Stop Loss**: 19913.22
- **Risk**: 67.08 points
- **TP 1RR**: 19779.06 ✅
- **TP 2RR**: 19711.99 ✅
- **TP 3RR**: 19644.91 ❌
- **TP 4RR**: 19577.83 ❌
- **TP 15RR**: 18839.98 ❌
- **PnL**: -67.08 points (-1.0R)
- **MFE**: 197.65 points
- **MAE**: 70.13 points

### Trade #530 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 06:30:00
- **FVG 5m**: 19763.77 - 19770.14
- **Entrée**: 19771.42 @ 2025-04-01 07:54:00
- **Stop Loss**: 19689.65
- **Risk**: 81.77 points
- **TP 1RR**: 19853.19 ✅
- **TP 2RR**: 19934.95 ❌
- **TP 3RR**: 20016.72 ❌
- **TP 4RR**: 20098.49 ❌
- **TP 15RR**: 20997.93 ❌
- **PnL**: -81.77 points (-1.0R)
- **MFE**: 82.37 points
- **MAE**: 82.63 points

### Trade #531 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 09:15:00
- **FVG 5m**: 19759.69 - 19788.00
- **Entrée**: 19796.16 @ 2025-04-01 09:38:00
- **Stop Loss**: 19638.67
- **Risk**: 157.48 points
- **TP 1RR**: 19953.64 ✅
- **TP 2RR**: 20111.12 ✅
- **TP 3RR**: 20268.61 ✅
- **TP 4RR**: 20426.09 ✅
- **TP 15RR**: 22158.42 ❌
- **PnL**: -157.48 points (-1.0R)
- **MFE**: 651.08 points
- **MAE**: 294.05 points

### Trade #532 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 09:15:00
- **FVG 5m**: 19759.69 - 19788.00
- **Entrée**: 19796.16 @ 2025-04-01 09:38:00
- **Stop Loss**: 19638.67
- **Risk**: 157.48 points
- **TP 1RR**: 19953.64 ✅
- **TP 2RR**: 20111.12 ✅
- **TP 3RR**: 20268.61 ✅
- **TP 4RR**: 20426.09 ✅
- **TP 15RR**: 22158.42 ❌
- **PnL**: -157.48 points (-1.0R)
- **MFE**: 651.08 points
- **MAE**: 294.05 points

### Trade #533 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 10:00:00
- **FVG 5m**: 19948.15 - 19964.47
- **Entrée**: 19976.46 @ 2025-04-01 10:14:00
- **Stop Loss**: 19884.90
- **Risk**: 91.56 points
- **TP 1RR**: 20068.02 ❌
- **TP 2RR**: 20159.57 ❌
- **TP 3RR**: 20251.13 ❌
- **TP 4RR**: 20342.68 ❌
- **TP 15RR**: 21349.80 ❌
- **PnL**: -91.56 points (-1.0R)
- **MFE**: 62.48 points
- **MAE**: 101.50 points

### Trade #534 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 11:30:00
- **FVG 5m**: 19906.58 - 19919.84
- **Entrée**: 19903.52 @ 2025-04-01 12:58:00
- **Stop Loss**: 19973.18
- **Risk**: 69.66 points
- **TP 1RR**: 19833.86 ✅
- **TP 2RR**: 19764.21 ❌
- **TP 3RR**: 19694.55 ❌
- **TP 4RR**: 19624.89 ❌
- **TP 15RR**: 18858.66 ❌
- **PnL**: -69.66 points (-1.0R)
- **MFE**: 128.79 points
- **MAE**: 78.55 points

### Trade #535 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-01 14:30:00
- **FVG 5m**: 19968.55 - 19984.88
- **Entrée**: 20004.77 @ 2025-04-01 14:54:00
- **Stop Loss**: 19845.65
- **Risk**: 159.12 points
- **TP 1RR**: 20163.89 ❌
- **TP 2RR**: 20323.00 ❌
- **TP 3RR**: 20482.12 ❌
- **TP 4RR**: 20641.24 ❌
- **TP 15RR**: 22391.54 ❌
- **PnL**: -159.12 points (-1.0R)
- **MFE**: 88.24 points
- **MAE**: 160.16 points

### Trade #536 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-01 17:45:00
- **FVG 5m**: 20013.95 - 20036.14
- **Entrée**: 20011.40 @ 2025-04-01 19:01:00
- **Stop Loss**: 20063.50
- **Risk**: 52.11 points
- **TP 1RR**: 19959.29 ✅
- **TP 2RR**: 19907.19 ✅
- **TP 3RR**: 19855.08 ✅
- **TP 4RR**: 19802.97 ✅
- **TP 15RR**: 19229.81 ❌
- **PnL**: -52.11 points (-1.0R)
- **MFE**: 306.54 points
- **MAE**: 52.54 points

### Trade #537 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 01:00:00
- **FVG 5m**: 19961.16 - 19966.00
- **Entrée**: 19971.36 @ 2025-04-02 01:17:00
- **Stop Loss**: 19927.73
- **Risk**: 43.63 points
- **TP 1RR**: 20014.99 ❌
- **TP 2RR**: 20058.62 ❌
- **TP 3RR**: 20102.26 ❌
- **TP 4RR**: 20145.89 ❌
- **TP 15RR**: 20625.84 ❌
- **PnL**: -43.63 points (-1.0R)
- **MFE**: 12.24 points
- **MAE**: 44.63 points

### Trade #538 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 01:00:00
- **FVG 5m**: 19961.16 - 19966.00
- **Entrée**: 19971.36 @ 2025-04-02 01:17:00
- **Stop Loss**: 19927.73
- **Risk**: 43.63 points
- **TP 1RR**: 20014.99 ❌
- **TP 2RR**: 20058.62 ❌
- **TP 3RR**: 20102.26 ❌
- **TP 4RR**: 20145.89 ❌
- **TP 15RR**: 20625.84 ❌
- **PnL**: -43.63 points (-1.0R)
- **MFE**: 12.24 points
- **MAE**: 44.63 points

### Trade #539 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 07:00:00
- **FVG 5m**: 19731.89 - 19802.28
- **Entrée**: 19808.40 @ 2025-04-02 08:34:00
- **Stop Loss**: 19751.85
- **Risk**: 56.55 points
- **TP 1RR**: 19864.95 ✅
- **TP 2RR**: 19921.50 ✅
- **TP 3RR**: 19978.05 ✅
- **TP 4RR**: 20034.60 ✅
- **TP 15RR**: 20656.66 ❌
- **PnL**: -56.55 points (-1.0R)
- **MFE**: 638.84 points
- **MAE**: 61.21 points

### Trade #540 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 08:30:00
- **FVG 5m**: 19911.43 - 19915.51
- **Entrée**: 19922.65 @ 2025-04-02 08:44:00
- **Stop Loss**: 19695.00
- **Risk**: 227.64 points
- **TP 1RR**: 20150.29 ✅
- **TP 2RR**: 20377.94 ✅
- **TP 3RR**: 20605.58 ❌
- **TP 4RR**: 20833.23 ❌
- **TP 15RR**: 23337.32 ❌
- **PnL**: -227.64 points (-1.0R)
- **MFE**: 524.59 points
- **MAE**: 268.80 points

### Trade #541 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 10:15:00
- **FVG 5m**: 20072.60 - 20079.75
- **Entrée**: 20063.17 @ 2025-04-02 10:44:00
- **Stop Loss**: 20120.40
- **Risk**: 57.24 points
- **TP 1RR**: 20005.93 ✅
- **TP 2RR**: 19948.70 ❌
- **TP 3RR**: 19891.46 ❌
- **TP 4RR**: 19834.23 ❌
- **TP 15RR**: 19204.64 ❌
- **PnL**: -57.24 points (-1.0R)
- **MFE**: 57.38 points
- **MAE**: 62.23 points

### Trade #542 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 10:15:00
- **FVG 5m**: 20074.64 - 20078.72
- **Entrée**: 20091.48 @ 2025-04-02 10:29:00
- **Stop Loss**: 19962.14
- **Risk**: 129.34 points
- **TP 1RR**: 20220.81 ✅
- **TP 2RR**: 20350.15 ✅
- **TP 3RR**: 20479.49 ❌
- **TP 4RR**: 20608.83 ❌
- **TP 15RR**: 22031.55 ❌
- **PnL**: -129.34 points (-1.0R)
- **MFE**: 355.76 points
- **MAE**: 258.60 points

### Trade #543 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 11:45:00
- **FVG 5m**: 20220.01 - 20228.94
- **Entrée**: 20234.80 @ 2025-04-02 12:04:00
- **Stop Loss**: 20142.86
- **Risk**: 91.94 points
- **TP 1RR**: 20326.74 ❌
- **TP 2RR**: 20418.68 ❌
- **TP 3RR**: 20510.62 ❌
- **TP 4RR**: 20602.56 ❌
- **TP 15RR**: 21613.90 ❌
- **PnL**: -91.94 points (-1.0R)
- **MFE**: 55.34 points
- **MAE**: 100.23 points

### Trade #544 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:00:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20395.46
- **Risk**: 613.33 points
- **TP 1RR**: 19168.80 ✅
- **TP 2RR**: 18555.47 ✅
- **TP 3RR**: 17942.14 ✅
- **TP 4RR**: 17328.81 ✅
- **TP 15RR**: 10582.18 ❌
- **PnL**: -613.33 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 617.93 points

### Trade #545 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:00:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20395.46
- **Risk**: 613.33 points
- **TP 1RR**: 19168.80 ✅
- **TP 2RR**: 18555.47 ✅
- **TP 3RR**: 17942.14 ✅
- **TP 4RR**: 17328.81 ✅
- **TP 15RR**: 10582.18 ❌
- **PnL**: -613.33 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 617.93 points

### Trade #546 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:15:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20457.46
- **Risk**: 675.33 points
- **TP 1RR**: 19106.80 ✅
- **TP 2RR**: 18431.47 ✅
- **TP 3RR**: 17756.13 ✅
- **TP 4RR**: 17080.80 ✅
- **TP 15RR**: 9652.15 ❌
- **PnL**: -675.33 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 679.39 points

### Trade #547 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:15:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20457.46
- **Risk**: 675.33 points
- **TP 1RR**: 19106.80 ✅
- **TP 2RR**: 18431.47 ✅
- **TP 3RR**: 17756.13 ✅
- **TP 4RR**: 17080.80 ✅
- **TP 15RR**: 9652.15 ❌
- **PnL**: -675.33 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 679.39 points

### Trade #548 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-02 15:15:00
- **FVG 5m**: 19833.64 - 20277.39
- **Entrée**: 19782.13 @ 2025-04-02 15:29:00
- **Stop Loss**: 20457.46
- **Risk**: 675.33 points
- **TP 1RR**: 19106.80 ✅
- **TP 2RR**: 18431.47 ✅
- **TP 3RR**: 17756.13 ✅
- **TP 4RR**: 17080.80 ✅
- **TP 15RR**: 9652.15 ❌
- **PnL**: -675.33 points (-1.0R)
- **MFE**: 2991.20 points
- **MAE**: 679.39 points

### Trade #549 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-02 19:15:00
- **FVG 5m**: 19441.67 - 19472.02
- **Entrée**: 19473.55 @ 2025-04-02 20:48:00
- **Stop Loss**: 19313.17
- **Risk**: 160.38 points
- **TP 1RR**: 19633.93 ❌
- **TP 2RR**: 19794.31 ❌
- **TP 3RR**: 19954.69 ❌
- **TP 4RR**: 20115.08 ❌
- **TP 15RR**: 21879.28 ❌
- **PnL**: -160.38 points (-1.0R)
- **MFE**: 89.00 points
- **MAE**: 164.24 points

### Trade #550 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-03 03:30:00
- **FVG 5m**: 19526.59 - 19531.18
- **Entrée**: 19522.00 @ 2025-04-03 03:43:00
- **Stop Loss**: 19569.27
- **Risk**: 47.27 points
- **TP 1RR**: 19474.73 ✅
- **TP 2RR**: 19427.47 ✅
- **TP 3RR**: 19380.20 ✅
- **TP 4RR**: 19332.93 ✅
- **TP 15RR**: 18812.97 ✅
- **PnL**: 709.03 points (15.0R)
- **MFE**: 738.56 points
- **MAE**: 40.55 points

### Trade #551 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 06:00:00
- **FVG 5m**: 19380.97 - 19397.29
- **Entrée**: 19405.20 @ 2025-04-03 07:09:00
- **Stop Loss**: 19333.81
- **Risk**: 71.39 points
- **TP 1RR**: 19476.59 ❌
- **TP 2RR**: 19547.98 ❌
- **TP 3RR**: 19619.36 ❌
- **TP 4RR**: 19690.75 ❌
- **TP 15RR**: 20476.02 ❌
- **PnL**: -71.39 points (-1.0R)
- **MFE**: 39.27 points
- **MAE**: 73.96 points

### Trade #552 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 08:00:00
- **FVG 5m**: 19263.66 - 19291.46
- **Entrée**: 19302.68 @ 2025-04-03 08:27:00
- **Stop Loss**: 19199.23
- **Risk**: 103.45 points
- **TP 1RR**: 19406.13 ✅
- **TP 2RR**: 19509.59 ❌
- **TP 3RR**: 19613.04 ❌
- **TP 4RR**: 19716.50 ❌
- **TP 15RR**: 20854.49 ❌
- **PnL**: -103.45 points (-1.0R)
- **MFE**: 155.06 points
- **MAE**: 109.66 points

### Trade #553 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-03 08:30:00
- **FVG 5m**: 19332.77 - 19339.40
- **Entrée**: 19306.76 @ 2025-04-03 09:03:00
- **Stop Loss**: 19467.46
- **Risk**: 160.70 points
- **TP 1RR**: 19146.06 ✅
- **TP 2RR**: 18985.35 ✅
- **TP 3RR**: 18824.65 ✅
- **TP 4RR**: 18663.94 ✅
- **TP 15RR**: 16896.19 ✅
- **PnL**: 2410.57 points (15.0R)
- **MFE**: 2424.02 points
- **MAE**: 62.74 points

### Trade #554 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 10:15:00
- **FVG 5m**: 19264.43 - 19274.88
- **Entrée**: 19276.67 @ 2025-04-03 10:38:00
- **Stop Loss**: 19162.78
- **Risk**: 113.89 points
- **TP 1RR**: 19390.56 ❌
- **TP 2RR**: 19504.45 ❌
- **TP 3RR**: 19618.34 ❌
- **TP 4RR**: 19732.24 ❌
- **TP 15RR**: 20985.05 ❌
- **PnL**: -113.89 points (-1.0R)
- **MFE**: 92.83 points
- **MAE**: 116.29 points

### Trade #555 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-03 10:30:00
- **FVG 5m**: 19310.08 - 19314.67
- **Entrée**: 19325.89 @ 2025-04-03 11:13:00
- **Stop Loss**: 19183.68
- **Risk**: 142.21 points
- **TP 1RR**: 19468.10 ❌
- **TP 2RR**: 19610.31 ❌
- **TP 3RR**: 19752.52 ❌
- **TP 4RR**: 19894.73 ❌
- **TP 15RR**: 21459.04 ❌
- **PnL**: -142.21 points (-1.0R)
- **MFE**: 43.61 points
- **MAE**: 149.96 points

### Trade #556 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-04 00:30:00
- **FVG 5m**: 18989.00 - 18995.37
- **Entrée**: 18999.20 @ 2025-04-04 00:44:00
- **Stop Loss**: 18935.41
- **Risk**: 63.79 points
- **TP 1RR**: 19062.99 ❌
- **TP 2RR**: 19126.78 ❌
- **TP 3RR**: 19190.58 ❌
- **TP 4RR**: 19254.37 ❌
- **TP 15RR**: 19956.09 ❌
- **PnL**: -63.79 points (-1.0R)
- **MFE**: 52.03 points
- **MAE**: 72.17 points

### Trade #557 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-04 09:45:00
- **FVG 5m**: 18265.74 - 18279.26
- **Entrée**: 18330.27 @ 2025-04-04 10:01:00
- **Stop Loss**: 18001.97
- **Risk**: 328.30 points
- **TP 1RR**: 18658.56 ❌
- **TP 2RR**: 18986.86 ❌
- **TP 3RR**: 19315.16 ❌
- **TP 4RR**: 19643.46 ❌
- **TP 15RR**: 23254.74 ❌
- **PnL**: -328.30 points (-1.0R)
- **MFE**: 182.60 points
- **MAE**: 342.25 points

### Trade #558 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-04 12:15:00
- **FVG 5m**: 18111.45 - 18134.41
- **Entrée**: 18149.20 @ 2025-04-04 12:37:00
- **Stop Loss**: 17965.01
- **Risk**: 184.19 points
- **TP 1RR**: 18333.39 ❌
- **TP 2RR**: 18517.58 ❌
- **TP 3RR**: 18701.77 ❌
- **TP 4RR**: 18885.96 ❌
- **TP 15RR**: 20912.05 ❌
- **PnL**: -184.19 points (-1.0R)
- **MFE**: 123.94 points
- **MAE**: 189.48 points

### Trade #559 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-07 02:45:00
- **FVG 5m**: 16968.43 - 17003.62
- **Entrée**: 17006.93 @ 2025-04-07 02:57:00
- **Stop Loss**: 16911.77
- **Risk**: 95.17 points
- **TP 1RR**: 17102.10 ✅
- **TP 2RR**: 17197.27 ✅
- **TP 3RR**: 17292.44 ✅
- **TP 4RR**: 17387.61 ✅
- **TP 15RR**: 18434.47 ✅
- **PnL**: 1427.54 points (15.0R)
- **MFE**: 1459.52 points
- **MAE**: 19.13 points

### Trade #560 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 03:15:00
- **FVG 5m**: 17127.56 - 17147.96
- **Entrée**: 17120.93 @ 2025-04-07 04:16:00
- **Stop Loss**: 17277.74
- **Risk**: 156.80 points
- **TP 1RR**: 16964.13 ❌
- **TP 2RR**: 16807.32 ❌
- **TP 3RR**: 16650.52 ❌
- **TP 4RR**: 16493.71 ❌
- **TP 15RR**: 14768.86 ❌
- **PnL**: -156.80 points (-1.0R)
- **MFE**: 42.08 points
- **MAE**: 163.22 points

### Trade #561 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 07:00:00
- **FVG 5m**: 17475.16 - 17495.31
- **Entrée**: 17469.30 @ 2025-04-07 08:01:00
- **Stop Loss**: 17500.48
- **Risk**: 31.19 points
- **TP 1RR**: 17438.11 ✅
- **TP 2RR**: 17406.92 ✅
- **TP 3RR**: 17375.73 ✅
- **TP 4RR**: 17344.54 ✅
- **TP 15RR**: 17001.47 ❌
- **PnL**: -31.19 points (-1.0R)
- **MFE**: 460.58 points
- **MAE**: 57.64 points

### Trade #562 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 09:15:00
- **FVG 5m**: 17748.81 - 17837.04
- **Entrée**: 17632.77 @ 2025-04-07 10:14:00
- **Stop Loss**: 18740.02
- **Risk**: 1107.25 points
- **TP 1RR**: 16525.52 ❌
- **TP 2RR**: 15418.26 ❌
- **TP 3RR**: 14311.01 ❌
- **TP 4RR**: 13203.76 ❌
- **TP 15RR**: 1023.97 ❌
- **PnL**: -1107.25 points (-1.0R)
- **MFE**: 561.31 points
- **MAE**: 1173.12 points

### Trade #563 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 09:15:00
- **FVG 5m**: 17748.81 - 17837.04
- **Entrée**: 17632.77 @ 2025-04-07 10:14:00
- **Stop Loss**: 18740.02
- **Risk**: 1107.25 points
- **TP 1RR**: 16525.52 ❌
- **TP 2RR**: 15418.26 ❌
- **TP 3RR**: 14311.01 ❌
- **TP 4RR**: 13203.76 ❌
- **TP 15RR**: 1023.97 ❌
- **PnL**: -1107.25 points (-1.0R)
- **MFE**: 561.31 points
- **MAE**: 1173.12 points

### Trade #564 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 09:15:00
- **FVG 5m**: 17748.81 - 17837.04
- **Entrée**: 17632.77 @ 2025-04-07 10:14:00
- **Stop Loss**: 18740.02
- **Risk**: 1107.25 points
- **TP 1RR**: 16525.52 ❌
- **TP 2RR**: 15418.26 ❌
- **TP 3RR**: 14311.01 ❌
- **TP 4RR**: 13203.76 ❌
- **TP 15RR**: 1023.97 ❌
- **PnL**: -1107.25 points (-1.0R)
- **MFE**: 561.31 points
- **MAE**: 1173.12 points

### Trade #565 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 18:30:00
- **FVG 5m**: 18070.90 - 18142.82
- **Entrée**: 18069.88 @ 2025-04-07 19:59:00
- **Stop Loss**: 18140.67
- **Risk**: 70.78 points
- **TP 1RR**: 17999.10 ❌
- **TP 2RR**: 17928.32 ❌
- **TP 3RR**: 17857.54 ❌
- **TP 4RR**: 17786.75 ❌
- **TP 15RR**: 17008.15 ❌
- **PnL**: -70.78 points (-1.0R)
- **MFE**: 52.28 points
- **MAE**: 81.86 points

### Trade #566 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-07 19:15:00
- **FVG 5m**: 18070.90 - 18142.82
- **Entrée**: 18069.88 @ 2025-04-07 19:59:00
- **Stop Loss**: 18223.59
- **Risk**: 153.71 points
- **TP 1RR**: 17916.18 ❌
- **TP 2RR**: 17762.47 ❌
- **TP 3RR**: 17608.76 ❌
- **TP 4RR**: 17455.05 ❌
- **TP 15RR**: 15764.28 ❌
- **PnL**: -153.71 points (-1.0R)
- **MFE**: 52.28 points
- **MAE**: 155.82 points

### Trade #567 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 05:00:00
- **FVG 5m**: 18110.43 - 18119.87
- **Entrée**: 18120.63 @ 2025-04-08 05:34:00
- **Stop Loss**: 18039.95
- **Risk**: 80.69 points
- **TP 1RR**: 18201.32 ✅
- **TP 2RR**: 18282.01 ✅
- **TP 3RR**: 18362.69 ✅
- **TP 4RR**: 18443.38 ✅
- **TP 15RR**: 19330.94 ❌
- **PnL**: -80.69 points (-1.0R)
- **MFE**: 605.69 points
- **MAE**: 91.30 points

### Trade #568 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-08 11:30:00
- **FVG 5m**: 18047.95 - 18084.67
- **Entrée**: 18041.83 @ 2025-04-08 11:58:00
- **Stop Loss**: 18316.72
- **Risk**: 274.89 points
- **TP 1RR**: 17766.94 ✅
- **TP 2RR**: 17492.05 ✅
- **TP 3RR**: 17217.16 ✅
- **TP 4RR**: 16942.27 ❌
- **TP 15RR**: 13918.46 ❌
- **PnL**: -274.89 points (-1.0R)
- **MFE**: 970.37 points
- **MAE**: 377.69 points

### Trade #569 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-08 11:30:00
- **FVG 5m**: 18047.95 - 18084.67
- **Entrée**: 18041.83 @ 2025-04-08 11:58:00
- **Stop Loss**: 18316.72
- **Risk**: 274.89 points
- **TP 1RR**: 17766.94 ✅
- **TP 2RR**: 17492.05 ✅
- **TP 3RR**: 17217.16 ✅
- **TP 4RR**: 16942.27 ❌
- **TP 15RR**: 13918.46 ❌
- **PnL**: -274.89 points (-1.0R)
- **MFE**: 970.37 points
- **MAE**: 377.69 points

### Trade #570 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 14:15:00
- **FVG 5m**: 17415.23 - 17470.57
- **Entrée**: 17473.12 @ 2025-04-08 14:51:00
- **Stop Loss**: 17472.54
- **Risk**: 0.58 points
- **TP 1RR**: 17473.70 ❌
- **TP 2RR**: 17474.28 ❌
- **TP 3RR**: 17474.86 ❌
- **TP 4RR**: 17475.44 ❌
- **TP 15RR**: 17481.82 ❌
- **PnL**: -0.58 points (-1.0R)
- **MFE**: 34.68 points
- **MAE**: 16.07 points

### Trade #571 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-08 18:45:00
- **FVG 5m**: 17256.09 - 17281.60
- **Entrée**: 17284.91 @ 2025-04-08 20:34:00
- **Stop Loss**: 17217.13
- **Risk**: 67.78 points
- **TP 1RR**: 17352.69 ✅
- **TP 2RR**: 17420.47 ✅
- **TP 3RR**: 17488.25 ✅
- **TP 4RR**: 17556.03 ❌
- **TP 15RR**: 18301.60 ❌
- **PnL**: -67.78 points (-1.0R)
- **MFE**: 268.54 points
- **MAE**: 73.45 points

### Trade #572 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 00:15:00
- **FVG 5m**: 17151.53 - 17165.56
- **Entrée**: 17168.11 @ 2025-04-09 00:49:00
- **Stop Loss**: 17141.68
- **Risk**: 26.43 points
- **TP 1RR**: 17194.54 ✅
- **TP 2RR**: 17220.96 ✅
- **TP 3RR**: 17247.39 ✅
- **TP 4RR**: 17273.82 ✅
- **TP 15RR**: 17564.52 ✅
- **PnL**: 396.40 points (15.0R)
- **MFE**: 583.50 points
- **MAE**: 2.55 points

### Trade #573 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 05:15:00
- **FVG 5m**: 17597.57 - 17625.63
- **Entrée**: 17594.77 @ 2025-04-09 05:59:00
- **Stop Loss**: 17633.16
- **Risk**: 38.40 points
- **TP 1RR**: 17556.37 ✅
- **TP 2RR**: 17517.98 ✅
- **TP 3RR**: 17479.58 ✅
- **TP 4RR**: 17441.19 ✅
- **TP 15RR**: 17018.84 ❌
- **PnL**: -38.40 points (-1.0R)
- **MFE**: 388.15 points
- **MAE**: 57.38 points

### Trade #574 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 07:45:00
- **FVG 5m**: 17565.44 - 17579.47
- **Entrée**: 17657.76 @ 2025-04-09 08:31:00
- **Stop Loss**: 17348.66
- **Risk**: 309.10 points
- **TP 1RR**: 17966.86 ✅
- **TP 2RR**: 18275.96 ✅
- **TP 3RR**: 18585.06 ✅
- **TP 4RR**: 18894.16 ✅
- **TP 15RR**: 22294.25 ✅
- **PnL**: 4636.49 points (15.0R)
- **MFE**: 4637.14 points
- **MAE**: 105.84 points

### Trade #575 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 08:30:00
- **FVG 5m**: 17741.66 - 17747.28
- **Entrée**: 17725.34 @ 2025-04-09 09:49:00
- **Stop Loss**: 17915.88
- **Risk**: 190.53 points
- **TP 1RR**: 17534.81 ❌
- **TP 2RR**: 17344.28 ❌
- **TP 3RR**: 17153.75 ❌
- **TP 4RR**: 16963.21 ❌
- **TP 15RR**: 14867.36 ❌
- **PnL**: -190.53 points (-1.0R)
- **MFE**: 173.42 points
- **MAE**: 200.45 points

### Trade #576 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 08:30:00
- **FVG 5m**: 17741.66 - 17747.28
- **Entrée**: 17725.34 @ 2025-04-09 09:49:00
- **Stop Loss**: 17915.88
- **Risk**: 190.53 points
- **TP 1RR**: 17534.81 ❌
- **TP 2RR**: 17344.28 ❌
- **TP 3RR**: 17153.75 ❌
- **TP 4RR**: 16963.21 ❌
- **TP 15RR**: 14867.36 ❌
- **PnL**: -190.53 points (-1.0R)
- **MFE**: 173.42 points
- **MAE**: 200.45 points

### Trade #577 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 08:45:00
- **FVG 5m**: 17660.31 - 17676.89
- **Entrée**: 17716.67 @ 2025-04-09 10:06:00
- **Stop Loss**: 17642.81
- **Risk**: 73.86 points
- **TP 1RR**: 17790.53 ✅
- **TP 2RR**: 17864.39 ❌
- **TP 3RR**: 17938.24 ❌
- **TP 4RR**: 18012.10 ❌
- **TP 15RR**: 18824.53 ❌
- **PnL**: -73.86 points (-1.0R)
- **MFE**: 96.40 points
- **MAE**: 90.28 points

### Trade #578 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 12:30:00
- **FVG 5m**: 19124.93 - 19231.53
- **Entrée**: 19243.77 @ 2025-04-09 12:58:00
- **Stop Loss**: 18724.35
- **Risk**: 519.42 points
- **TP 1RR**: 19763.19 ✅
- **TP 2RR**: 20282.61 ❌
- **TP 3RR**: 20802.03 ❌
- **TP 4RR**: 21321.45 ❌
- **TP 15RR**: 27035.06 ❌
- **PnL**: -519.42 points (-1.0R)
- **MFE**: 532.75 points
- **MAE**: 530.45 points

### Trade #579 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 13:00:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19299.36 @ 2025-04-09 13:42:00
- **Stop Loss**: 19396.28
- **Risk**: 96.91 points
- **TP 1RR**: 19202.45 ✅
- **TP 2RR**: 19105.54 ✅
- **TP 3RR**: 19008.63 ❌
- **TP 4RR**: 18911.72 ❌
- **TP 15RR**: 17845.68 ❌
- **PnL**: -96.91 points (-1.0R)
- **MFE**: 203.77 points
- **MAE**: 120.37 points

### Trade #580 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-09 13:15:00
- **FVG 5m**: 19312.63 - 19342.72
- **Entrée**: 19299.36 @ 2025-04-09 13:42:00
- **Stop Loss**: 19506.25
- **Risk**: 206.88 points
- **TP 1RR**: 19092.48 ❌
- **TP 2RR**: 18885.60 ❌
- **TP 3RR**: 18678.71 ❌
- **TP 4RR**: 18471.83 ❌
- **TP 15RR**: 16196.11 ❌
- **PnL**: -206.88 points (-1.0R)
- **MFE**: 203.77 points
- **MAE**: 250.69 points

### Trade #581 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 14:45:00
- **FVG 5m**: 19717.61 - 19719.65
- **Entrée**: 19722.71 @ 2025-04-09 15:53:00
- **Stop Loss**: 19517.34
- **Risk**: 205.37 points
- **TP 1RR**: 19928.08 ❌
- **TP 2RR**: 20133.45 ❌
- **TP 3RR**: 20338.81 ❌
- **TP 4RR**: 20544.18 ❌
- **TP 15RR**: 22803.24 ❌
- **PnL**: -205.37 points (-1.0R)
- **MFE**: 50.50 points
- **MAE**: 217.28 points

### Trade #582 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 14:45:00
- **FVG 5m**: 19717.61 - 19719.65
- **Entrée**: 19722.71 @ 2025-04-09 15:53:00
- **Stop Loss**: 19517.34
- **Risk**: 205.37 points
- **TP 1RR**: 19928.08 ❌
- **TP 2RR**: 20133.45 ❌
- **TP 3RR**: 20338.81 ❌
- **TP 4RR**: 20544.18 ❌
- **TP 15RR**: 22803.24 ❌
- **PnL**: -205.37 points (-1.0R)
- **MFE**: 50.50 points
- **MAE**: 217.28 points

### Trade #583 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-09 15:45:00
- **FVG 5m**: 19664.82 - 19697.72
- **Entrée**: 19702.82 @ 2025-04-09 17:13:00
- **Stop Loss**: 19681.75
- **Risk**: 21.07 points
- **TP 1RR**: 19723.88 ❌
- **TP 2RR**: 19744.95 ❌
- **TP 3RR**: 19766.02 ❌
- **TP 4RR**: 19787.08 ❌
- **TP 15RR**: 20018.82 ❌
- **PnL**: -21.07 points (-1.0R)
- **MFE**: 13.01 points
- **MAE**: 22.70 points

### Trade #584 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-10 10:45:00
- **FVG 5m**: 18474.10 - 18536.58
- **Entrée**: 18454.21 @ 2025-04-10 11:18:00
- **Stop Loss**: 18823.46
- **Risk**: 369.25 points
- **TP 1RR**: 18084.96 ❌
- **TP 2RR**: 17715.71 ❌
- **TP 3RR**: 17346.46 ❌
- **TP 4RR**: 16977.21 ❌
- **TP 15RR**: 12915.47 ❌
- **PnL**: -369.25 points (-1.0R)
- **MFE**: 174.95 points
- **MAE**: 412.38 points

### Trade #585 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-10 10:45:00
- **FVG 5m**: 18474.10 - 18536.58
- **Entrée**: 18454.21 @ 2025-04-10 11:18:00
- **Stop Loss**: 18823.46
- **Risk**: 369.25 points
- **TP 1RR**: 18084.96 ❌
- **TP 2RR**: 17715.71 ❌
- **TP 3RR**: 17346.46 ❌
- **TP 4RR**: 16977.21 ❌
- **TP 15RR**: 12915.47 ❌
- **PnL**: -369.25 points (-1.0R)
- **MFE**: 174.95 points
- **MAE**: 412.38 points

### Trade #586 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-10 20:00:00
- **FVG 5m**: 18602.12 - 18621.76
- **Entrée**: 18637.57 @ 2025-04-10 20:11:00
- **Stop Loss**: 18515.59
- **Risk**: 121.98 points
- **TP 1RR**: 18759.56 ✅
- **TP 2RR**: 18881.54 ✅
- **TP 3RR**: 19003.52 ✅
- **TP 4RR**: 19125.51 ✅
- **TP 15RR**: 20467.33 ❌
- **PnL**: -121.98 points (-1.0R)
- **MFE**: 1005.57 points
- **MAE**: 129.04 points

### Trade #587 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-11 02:00:00
- **FVG 5m**: 18952.78 - 18973.44
- **Entrée**: 18947.43 @ 2025-04-11 02:58:00
- **Stop Loss**: 19080.91
- **Risk**: 133.48 points
- **TP 1RR**: 18813.95 ✅
- **TP 2RR**: 18680.47 ✅
- **TP 3RR**: 18546.99 ❌
- **TP 4RR**: 18413.51 ❌
- **TP 15RR**: 16945.25 ❌
- **PnL**: -133.48 points (-1.0R)
- **MFE**: 310.11 points
- **MAE**: 147.41 points

### Trade #588 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-11 02:15:00
- **FVG 5m**: 18952.78 - 18973.44
- **Entrée**: 18947.43 @ 2025-04-11 02:58:00
- **Stop Loss**: 19031.66
- **Risk**: 84.23 points
- **TP 1RR**: 18863.19 ✅
- **TP 2RR**: 18778.96 ✅
- **TP 3RR**: 18694.73 ✅
- **TP 4RR**: 18610.49 ❌
- **TP 15RR**: 17683.92 ❌
- **PnL**: -84.23 points (-1.0R)
- **MFE**: 264.97 points
- **MAE**: 89.77 points

### Trade #589 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-11 04:15:00
- **FVG 5m**: 18829.35 - 18835.22
- **Entrée**: 18839.04 @ 2025-04-11 04:34:00
- **Stop Loss**: 18748.31
- **Risk**: 90.73 points
- **TP 1RR**: 18929.77 ✅
- **TP 2RR**: 19020.51 ✅
- **TP 3RR**: 19111.24 ❌
- **TP 4RR**: 19201.97 ❌
- **TP 15RR**: 20200.03 ❌
- **PnL**: -90.73 points (-1.0R)
- **MFE**: 239.72 points
- **MAE**: 111.45 points

### Trade #590 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-11 09:30:00
- **FVG 5m**: 18846.69 - 18863.78
- **Entrée**: 18867.61 @ 2025-04-11 09:44:00
- **Stop Loss**: 18628.00
- **Risk**: 239.61 points
- **TP 1RR**: 19107.21 ✅
- **TP 2RR**: 19346.82 ✅
- **TP 3RR**: 19586.43 ✅
- **TP 4RR**: 19826.03 ❌
- **TP 15RR**: 22461.72 ❌
- **PnL**: -239.61 points (-1.0R)
- **MFE**: 775.53 points
- **MAE**: 248.91 points

### Trade #591 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-13 17:00:00
- **FVG 5m**: 19416.17 - 19435.80
- **Entrée**: 19395.76 @ 2025-04-13 17:17:00
- **Stop Loss**: 19646.84
- **Risk**: 251.07 points
- **TP 1RR**: 19144.69 ✅
- **TP 2RR**: 18893.62 ✅
- **TP 3RR**: 18642.54 ✅
- **TP 4RR**: 18391.47 ✅
- **TP 15RR**: 15629.66 ❌
- **PnL**: -251.07 points (-1.0R)
- **MFE**: 1339.91 points
- **MAE**: 257.58 points

### Trade #592 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-13 17:15:00
- **FVG 5m**: 19400.87 - 19408.01
- **Entrée**: 19396.78 @ 2025-04-13 18:31:00
- **Stop Loss**: 19457.77
- **Risk**: 60.98 points
- **TP 1RR**: 19335.80 ❌
- **TP 2RR**: 19274.82 ❌
- **TP 3RR**: 19213.83 ❌
- **TP 4RR**: 19152.85 ❌
- **TP 15RR**: 18482.02 ❌
- **PnL**: -60.98 points (-1.0R)
- **MFE**: 30.09 points
- **MAE**: 62.99 points

### Trade #593 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-13 17:15:00
- **FVG 5m**: 19400.87 - 19408.01
- **Entrée**: 19396.78 @ 2025-04-13 18:31:00
- **Stop Loss**: 19457.77
- **Risk**: 60.98 points
- **TP 1RR**: 19335.80 ❌
- **TP 2RR**: 19274.82 ❌
- **TP 3RR**: 19213.83 ❌
- **TP 4RR**: 19152.85 ❌
- **TP 15RR**: 18482.02 ❌
- **PnL**: -60.98 points (-1.0R)
- **MFE**: 30.09 points
- **MAE**: 62.99 points

### Trade #594 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-13 17:30:00
- **FVG 5m**: 19392.45 - 19395.25
- **Entrée**: 19404.95 @ 2025-04-13 18:11:00
- **Stop Loss**: 19302.46
- **Risk**: 102.49 points
- **TP 1RR**: 19507.43 ✅
- **TP 2RR**: 19609.92 ✅
- **TP 3RR**: 19712.40 ❌
- **TP 4RR**: 19814.89 ❌
- **TP 15RR**: 20942.23 ❌
- **PnL**: -102.49 points (-1.0R)
- **MFE**: 238.19 points
- **MAE**: 102.78 points

### Trade #595 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 04:45:00
- **FVG 5m**: 19450.60 - 19455.95
- **Entrée**: 19463.35 @ 2025-04-14 05:27:00
- **Stop Loss**: 19403.40
- **Risk**: 59.95 points
- **TP 1RR**: 19523.29 ✅
- **TP 2RR**: 19583.24 ✅
- **TP 3RR**: 19643.19 ❌
- **TP 4RR**: 19703.13 ❌
- **TP 15RR**: 20362.55 ❌
- **PnL**: -59.95 points (-1.0R)
- **MFE**: 179.79 points
- **MAE**: 79.06 points

### Trade #596 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-14 07:30:00
- **FVG 5m**: 19579.64 - 19612.28
- **Entrée**: 19569.18 @ 2025-04-14 08:33:00
- **Stop Loss**: 19592.24
- **Risk**: 23.05 points
- **TP 1RR**: 19546.13 ❌
- **TP 2RR**: 19523.08 ❌
- **TP 3RR**: 19500.02 ❌
- **TP 4RR**: 19476.97 ❌
- **TP 15RR**: 19223.39 ❌
- **PnL**: -23.05 points (-1.0R)
- **MFE**: 10.97 points
- **MAE**: 28.05 points

### Trade #597 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 08:30:00
- **FVG 5m**: 19485.02 - 19488.85
- **Entrée**: 19519.20 @ 2025-04-14 09:03:00
- **Stop Loss**: 19368.22
- **Risk**: 150.97 points
- **TP 1RR**: 19670.17 ❌
- **TP 2RR**: 19821.14 ❌
- **TP 3RR**: 19972.12 ❌
- **TP 4RR**: 20123.09 ❌
- **TP 15RR**: 21783.80 ❌
- **PnL**: -150.97 points (-1.0R)
- **MFE**: 59.68 points
- **MAE**: 168.57 points

### Trade #598 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 09:00:00
- **FVG 5m**: 19493.69 - 19498.29
- **Entrée**: 19510.53 @ 2025-04-14 09:26:00
- **Stop Loss**: 19402.89
- **Risk**: 107.64 points
- **TP 1RR**: 19618.16 ❌
- **TP 2RR**: 19725.80 ❌
- **TP 3RR**: 19833.44 ❌
- **TP 4RR**: 19941.07 ❌
- **TP 15RR**: 21125.07 ❌
- **PnL**: -107.64 points (-1.0R)
- **MFE**: 68.35 points
- **MAE**: 110.17 points

### Trade #599 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 13:00:00
- **FVG 5m**: 19354.20 - 19363.89
- **Entrée**: 19376.38 @ 2025-04-14 13:26:00
- **Stop Loss**: 19307.05
- **Risk**: 69.33 points
- **TP 1RR**: 19445.72 ✅
- **TP 2RR**: 19515.05 ❌
- **TP 3RR**: 19584.39 ❌
- **TP 4RR**: 19653.72 ❌
- **TP 15RR**: 20416.40 ❌
- **PnL**: -69.33 points (-1.0R)
- **MFE**: 102.52 points
- **MAE**: 71.66 points

### Trade #600 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-14 13:15:00
- **FVG 5m**: 19409.79 - 19421.01
- **Entrée**: 19425.35 @ 2025-04-14 14:04:00
- **Stop Loss**: 19314.95
- **Risk**: 110.40 points
- **TP 1RR**: 19535.75 ❌
- **TP 2RR**: 19646.14 ❌
- **TP 3RR**: 19756.54 ❌
- **TP 4RR**: 19866.94 ❌
- **TP 15RR**: 21081.31 ❌
- **PnL**: -110.40 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 120.63 points

### Trade #601 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 06:30:00
- **FVG 5m**: 19282.28 - 19303.96
- **Entrée**: 19278.45 @ 2025-04-15 06:47:00
- **Stop Loss**: 19377.14
- **Risk**: 98.69 points
- **TP 1RR**: 19179.76 ❌
- **TP 2RR**: 19081.08 ❌
- **TP 3RR**: 18982.39 ❌
- **TP 4RR**: 18883.70 ❌
- **TP 15RR**: 17798.13 ❌
- **PnL**: -98.69 points (-1.0R)
- **MFE**: 64.01 points
- **MAE**: 110.17 points

### Trade #602 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 06:30:00
- **FVG 5m**: 19282.28 - 19303.96
- **Entrée**: 19278.45 @ 2025-04-15 06:47:00
- **Stop Loss**: 19377.14
- **Risk**: 98.69 points
- **TP 1RR**: 19179.76 ❌
- **TP 2RR**: 19081.08 ❌
- **TP 3RR**: 18982.39 ❌
- **TP 4RR**: 18883.70 ❌
- **TP 15RR**: 17798.13 ❌
- **PnL**: -98.69 points (-1.0R)
- **MFE**: 64.01 points
- **MAE**: 110.17 points

### Trade #603 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 07:30:00
- **FVG 5m**: 19309.82 - 19316.96
- **Entrée**: 19327.93 @ 2025-04-15 08:00:00
- **Stop Loss**: 19227.26
- **Risk**: 100.66 points
- **TP 1RR**: 19428.59 ✅
- **TP 2RR**: 19529.25 ✅
- **TP 3RR**: 19629.92 ❌
- **TP 4RR**: 19730.58 ❌
- **TP 15RR**: 20837.87 ❌
- **PnL**: -100.66 points (-1.0R)
- **MFE**: 201.73 points
- **MAE**: 251.97 points

### Trade #604 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-15 08:45:00
- **FVG 5m**: 19416.68 - 19461.31
- **Entrée**: 19393.98 @ 2025-04-15 09:18:00
- **Stop Loss**: 19511.61
- **Risk**: 117.63 points
- **TP 1RR**: 19276.35 ✅
- **TP 2RR**: 19158.73 ✅
- **TP 3RR**: 19041.10 ✅
- **TP 4RR**: 18923.47 ✅
- **TP 15RR**: 17629.57 ❌
- **PnL**: -117.63 points (-1.0R)
- **MFE**: 1338.12 points
- **MAE**: 135.42 points

### Trade #605 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 12:15:00
- **FVG 5m**: 19342.46 - 19344.76
- **Entrée**: 19349.60 @ 2025-04-15 12:39:00
- **Stop Loss**: 19278.50
- **Risk**: 71.11 points
- **TP 1RR**: 19420.71 ❌
- **TP 2RR**: 19491.82 ❌
- **TP 3RR**: 19562.92 ❌
- **TP 4RR**: 19634.03 ❌
- **TP 15RR**: 20416.19 ❌
- **PnL**: -71.11 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 75.49 points

### Trade #606 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 17:15:00
- **FVG 5m**: 19123.91 - 19136.15
- **Entrée**: 19136.91 @ 2025-04-15 17:29:00
- **Stop Loss**: 19085.29
- **Risk**: 51.63 points
- **TP 1RR**: 19188.54 ❌
- **TP 2RR**: 19240.17 ❌
- **TP 3RR**: 19291.79 ❌
- **TP 4RR**: 19343.42 ❌
- **TP 15RR**: 19911.31 ❌
- **PnL**: -51.63 points (-1.0R)
- **MFE**: 17.34 points
- **MAE**: 53.05 points

### Trade #607 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-15 22:00:00
- **FVG 5m**: 19076.98 - 19083.10
- **Entrée**: 19084.38 @ 2025-04-15 22:11:00
- **Stop Loss**: 19055.21
- **Risk**: 29.17 points
- **TP 1RR**: 19113.55 ❌
- **TP 2RR**: 19142.72 ❌
- **TP 3RR**: 19171.89 ❌
- **TP 4RR**: 19201.06 ❌
- **TP 15RR**: 19521.92 ❌
- **PnL**: -29.17 points (-1.0R)
- **MFE**: 13.52 points
- **MAE**: 30.35 points

### Trade #608 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 03:15:00
- **FVG 5m**: 18926.01 - 19029.80
- **Entrée**: 19110.14 @ 2025-04-16 03:27:00
- **Stop Loss**: 18881.11
- **Risk**: 229.02 points
- **TP 1RR**: 19339.16 ❌
- **TP 2RR**: 19568.18 ❌
- **TP 3RR**: 19797.20 ❌
- **TP 4RR**: 20026.23 ❌
- **TP 15RR**: 22545.48 ❌
- **PnL**: -229.02 points (-1.0R)
- **MFE**: 130.32 points
- **MAE**: 270.58 points

### Trade #609 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 03:30:00
- **FVG 5m**: 19101.46 - 19122.38
- **Entrée**: 19151.70 @ 2025-04-16 03:46:00
- **Stop Loss**: 19020.29
- **Risk**: 131.42 points
- **TP 1RR**: 19283.12 ❌
- **TP 2RR**: 19414.54 ❌
- **TP 3RR**: 19545.96 ❌
- **TP 4RR**: 19677.37 ❌
- **TP 15RR**: 21122.97 ❌
- **PnL**: -131.42 points (-1.0R)
- **MFE**: 9.44 points
- **MAE**: 131.59 points

### Trade #610 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 03:45:00
- **FVG 5m**: 19072.14 - 19076.22
- **Entrée**: 19070.61 @ 2025-04-16 05:34:00
- **Stop Loss**: 19192.92
- **Risk**: 122.31 points
- **TP 1RR**: 18948.29 ✅
- **TP 2RR**: 18825.98 ✅
- **TP 3RR**: 18703.67 ✅
- **TP 4RR**: 18581.35 ✅
- **TP 15RR**: 17235.91 ❌
- **PnL**: -122.31 points (-1.0R)
- **MFE**: 1014.75 points
- **MAE**: 131.08 points

### Trade #611 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 10:15:00
- **FVG 5m**: 19033.88 - 19045.61
- **Entrée**: 19029.55 @ 2025-04-16 10:42:00
- **Stop Loss**: 19121.22
- **Risk**: 91.67 points
- **TP 1RR**: 18937.87 ✅
- **TP 2RR**: 18846.20 ✅
- **TP 3RR**: 18754.52 ✅
- **TP 4RR**: 18662.85 ✅
- **TP 15RR**: 17654.43 ❌
- **PnL**: -91.67 points (-1.0R)
- **MFE**: 973.69 points
- **MAE**: 115.78 points

### Trade #612 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-16 14:45:00
- **FVG 5m**: 18743.66 - 18765.08
- **Entrée**: 18766.62 @ 2025-04-16 17:01:00
- **Stop Loss**: 18581.86
- **Risk**: 184.75 points
- **TP 1RR**: 18951.37 ✅
- **TP 2RR**: 19136.12 ❌
- **TP 3RR**: 19320.88 ❌
- **TP 4RR**: 19505.63 ❌
- **TP 15RR**: 21537.92 ❌
- **PnL**: -184.75 points (-1.0R)
- **MFE**: 261.15 points
- **MAE**: 185.91 points

### Trade #613 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-16 21:15:00
- **FVG 5m**: 18855.36 - 18860.72
- **Entrée**: 18854.09 @ 2025-04-16 21:33:00
- **Stop Loss**: 18894.13
- **Risk**: 40.05 points
- **TP 1RR**: 18814.04 ❌
- **TP 2RR**: 18774.00 ❌
- **TP 3RR**: 18733.95 ❌
- **TP 4RR**: 18693.91 ❌
- **TP 15RR**: 18253.41 ❌
- **PnL**: -40.05 points (-1.0R)
- **MFE**: 29.33 points
- **MAE**: 45.39 points

### Trade #614 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 06:15:00
- **FVG 5m**: 18862.50 - 18880.61
- **Entrée**: 18886.99 @ 2025-04-17 06:28:00
- **Stop Loss**: 18819.17
- **Risk**: 67.82 points
- **TP 1RR**: 18954.80 ✅
- **TP 2RR**: 19022.62 ❌
- **TP 3RR**: 19090.43 ❌
- **TP 4RR**: 19158.25 ❌
- **TP 15RR**: 19904.22 ❌
- **PnL**: -67.82 points (-1.0R)
- **MFE**: 111.70 points
- **MAE**: 81.61 points

### Trade #615 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 06:15:00
- **FVG 5m**: 18862.50 - 18880.61
- **Entrée**: 18886.99 @ 2025-04-17 06:28:00
- **Stop Loss**: 18819.17
- **Risk**: 67.82 points
- **TP 1RR**: 18954.80 ✅
- **TP 2RR**: 19022.62 ❌
- **TP 3RR**: 19090.43 ❌
- **TP 4RR**: 19158.25 ❌
- **TP 15RR**: 19904.22 ❌
- **PnL**: -67.82 points (-1.0R)
- **MFE**: 111.70 points
- **MAE**: 81.61 points

### Trade #616 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 06:15:00
- **FVG 5m**: 18862.50 - 18880.61
- **Entrée**: 18886.99 @ 2025-04-17 06:28:00
- **Stop Loss**: 18819.17
- **Risk**: 67.82 points
- **TP 1RR**: 18954.80 ✅
- **TP 2RR**: 19022.62 ❌
- **TP 3RR**: 19090.43 ❌
- **TP 4RR**: 19158.25 ❌
- **TP 15RR**: 19904.22 ❌
- **PnL**: -67.82 points (-1.0R)
- **MFE**: 111.70 points
- **MAE**: 81.61 points

### Trade #617 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 07:00:00
- **FVG 5m**: 18911.72 - 18926.01
- **Entrée**: 18949.72 @ 2025-04-17 07:33:00
- **Stop Loss**: 18877.29
- **Risk**: 72.43 points
- **TP 1RR**: 19022.16 ❌
- **TP 2RR**: 19094.59 ❌
- **TP 3RR**: 19167.03 ❌
- **TP 4RR**: 19239.46 ❌
- **TP 15RR**: 20036.25 ❌
- **PnL**: -72.43 points (-1.0R)
- **MFE**: 15.81 points
- **MAE**: 77.27 points

### Trade #618 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-17 09:30:00
- **FVG 5m**: 18673.53 - 18703.11
- **Entrée**: 18706.68 @ 2025-04-17 09:41:00
- **Stop Loss**: 18619.33
- **Risk**: 87.35 points
- **TP 1RR**: 18794.04 ✅
- **TP 2RR**: 18881.39 ✅
- **TP 3RR**: 18968.74 ❌
- **TP 4RR**: 19056.09 ❌
- **TP 15RR**: 20016.97 ❌
- **PnL**: -87.35 points (-1.0R)
- **MFE**: 191.78 points
- **MAE**: 108.90 points

### Trade #619 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-20 17:00:00
- **FVG 5m**: 18665.88 - 18676.85
- **Entrée**: 18683.73 @ 2025-04-20 18:04:00
- **Stop Loss**: 18588.49
- **Risk**: 95.24 points
- **TP 1RR**: 18778.97 ❌
- **TP 2RR**: 18874.22 ❌
- **TP 3RR**: 18969.46 ❌
- **TP 4RR**: 19064.70 ❌
- **TP 15RR**: 20112.37 ❌
- **PnL**: -95.24 points (-1.0R)
- **MFE**: 64.01 points
- **MAE**: 103.03 points

### Trade #620 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-20 22:15:00
- **FVG 5m**: 18592.94 - 18597.02
- **Entrée**: 18597.79 @ 2025-04-20 23:08:00
- **Stop Loss**: 18572.43
- **Risk**: 25.36 points
- **TP 1RR**: 18623.15 ✅
- **TP 2RR**: 18648.50 ❌
- **TP 3RR**: 18673.86 ❌
- **TP 4RR**: 18699.22 ❌
- **TP 15RR**: 18978.15 ❌
- **PnL**: -25.36 points (-1.0R)
- **MFE**: 26.01 points
- **MAE**: 35.19 points

### Trade #621 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-21 07:15:00
- **FVG 5m**: 18475.89 - 18488.38
- **Entrée**: 18492.97 @ 2025-04-21 08:29:00
- **Stop Loss**: 18455.94
- **Risk**: 37.03 points
- **TP 1RR**: 18530.00 ✅
- **TP 2RR**: 18567.03 ❌
- **TP 3RR**: 18604.06 ❌
- **TP 4RR**: 18641.09 ❌
- **TP 15RR**: 19048.43 ❌
- **PnL**: -37.03 points (-1.0R)
- **MFE**: 37.23 points
- **MAE**: 69.11 points

### Trade #622 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-22 01:45:00
- **FVG 5m**: 18443.50 - 18448.09
- **Entrée**: 18451.91 @ 2025-04-22 03:27:00
- **Stop Loss**: 18400.37
- **Risk**: 51.54 points
- **TP 1RR**: 18503.45 ✅
- **TP 2RR**: 18554.99 ✅
- **TP 3RR**: 18606.53 ✅
- **TP 4RR**: 18658.07 ✅
- **TP 15RR**: 19225.00 ✅
- **PnL**: 773.09 points (15.0R)
- **MFE**: 776.30 points
- **MAE**: 45.39 points

### Trade #623 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-22 01:45:00
- **FVG 5m**: 18443.50 - 18448.09
- **Entrée**: 18451.91 @ 2025-04-22 03:27:00
- **Stop Loss**: 18400.37
- **Risk**: 51.54 points
- **TP 1RR**: 18503.45 ✅
- **TP 2RR**: 18554.99 ✅
- **TP 3RR**: 18606.53 ✅
- **TP 4RR**: 18658.07 ✅
- **TP 15RR**: 19225.00 ✅
- **PnL**: 773.09 points (15.0R)
- **MFE**: 776.30 points
- **MAE**: 45.39 points

### Trade #624 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-22 08:30:00
- **FVG 5m**: 18519.49 - 18576.37
- **Entrée**: 18577.13 @ 2025-04-22 08:44:00
- **Stop Loss**: 18455.18
- **Risk**: 121.95 points
- **TP 1RR**: 18699.08 ✅
- **TP 2RR**: 18821.04 ✅
- **TP 3RR**: 18942.99 ✅
- **TP 4RR**: 19064.95 ✅
- **TP 15RR**: 20406.44 ✅
- **PnL**: 1829.31 points (15.0R)
- **MFE**: 1832.62 points
- **MAE**: 12.24 points

### Trade #625 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 11:45:00
- **FVG 5m**: 18757.69 - 18813.03
- **Entrée**: 18753.10 @ 2025-04-22 12:11:00
- **Stop Loss**: 18859.69
- **Risk**: 106.59 points
- **TP 1RR**: 18646.51 ✅
- **TP 2RR**: 18539.92 ❌
- **TP 3RR**: 18433.33 ❌
- **TP 4RR**: 18326.74 ❌
- **TP 15RR**: 17154.25 ❌
- **PnL**: -106.59 points (-1.0R)
- **MFE**: 175.71 points
- **MAE**: 358.31 points

### Trade #626 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 12:15:00
- **FVG 5m**: 18622.53 - 18624.57
- **Entrée**: 18616.91 @ 2025-04-22 12:48:00
- **Stop Loss**: 18767.07
- **Risk**: 150.15 points
- **TP 1RR**: 18466.76 ❌
- **TP 2RR**: 18316.61 ❌
- **TP 3RR**: 18166.45 ❌
- **TP 4RR**: 18016.30 ❌
- **TP 15RR**: 16364.61 ❌
- **PnL**: -150.15 points (-1.0R)
- **MFE**: 39.53 points
- **MAE**: 150.72 points

### Trade #627 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 17:00:00
- **FVG 5m**: 19142.01 - 19158.08
- **Entrée**: 19134.87 @ 2025-04-22 18:17:00
- **Stop Loss**: 19158.73
- **Risk**: 23.86 points
- **TP 1RR**: 19111.02 ✅
- **TP 2RR**: 19087.16 ✅
- **TP 3RR**: 19063.30 ✅
- **TP 4RR**: 19039.45 ✅
- **TP 15RR**: 18777.03 ❌
- **PnL**: -23.86 points (-1.0R)
- **MFE**: 136.69 points
- **MAE**: 26.27 points

### Trade #628 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-22 20:30:00
- **FVG 5m**: 19054.28 - 19057.34
- **Entrée**: 19048.42 @ 2025-04-22 22:01:00
- **Stop Loss**: 19093.15
- **Risk**: 44.74 points
- **TP 1RR**: 19003.68 ❌
- **TP 2RR**: 18958.95 ❌
- **TP 3RR**: 18914.21 ❌
- **TP 4RR**: 18869.48 ❌
- **TP 15RR**: 18377.39 ❌
- **PnL**: -44.74 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 54.58 points

### Trade #629 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 03:00:00
- **FVG 5m**: 19174.15 - 19194.80
- **Entrée**: 19200.41 @ 2025-04-23 03:14:00
- **Stop Loss**: 19142.89
- **Risk**: 57.52 points
- **TP 1RR**: 19257.94 ✅
- **TP 2RR**: 19315.46 ✅
- **TP 3RR**: 19372.98 ✅
- **TP 4RR**: 19430.50 ✅
- **TP 15RR**: 20063.23 ❌
- **PnL**: -57.52 points (-1.0R)
- **MFE**: 350.41 points
- **MAE**: 65.80 points

### Trade #630 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 03:30:00
- **FVG 5m**: 19208.58 - 19217.76
- **Entrée**: 19219.54 @ 2025-04-23 04:56:00
- **Stop Loss**: 19184.19
- **Risk**: 35.35 points
- **TP 1RR**: 19254.90 ✅
- **TP 2RR**: 19290.25 ✅
- **TP 3RR**: 19325.61 ✅
- **TP 4RR**: 19360.96 ✅
- **TP 15RR**: 19749.86 ❌
- **PnL**: -35.35 points (-1.0R)
- **MFE**: 331.28 points
- **MAE**: 44.37 points

### Trade #631 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 05:15:00
- **FVG 5m**: 19267.74 - 19277.94
- **Entrée**: 19278.20 @ 2025-04-23 05:44:00
- **Stop Loss**: 19214.27
- **Risk**: 63.93 points
- **TP 1RR**: 19342.13 ✅
- **TP 2RR**: 19406.06 ✅
- **TP 3RR**: 19470.00 ✅
- **TP 4RR**: 19533.93 ✅
- **TP 15RR**: 20237.19 ❌
- **PnL**: -63.93 points (-1.0R)
- **MFE**: 272.62 points
- **MAE**: 81.61 points

### Trade #632 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 05:30:00
- **FVG 5m**: 19267.74 - 19277.94
- **Entrée**: 19278.20 @ 2025-04-23 05:44:00
- **Stop Loss**: 19236.19
- **Risk**: 42.01 points
- **TP 1RR**: 19320.21 ✅
- **TP 2RR**: 19362.22 ✅
- **TP 3RR**: 19404.23 ✅
- **TP 4RR**: 19446.24 ✅
- **TP 15RR**: 19908.37 ❌
- **PnL**: -42.01 points (-1.0R)
- **MFE**: 272.62 points
- **MAE**: 45.90 points

### Trade #633 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 06:45:00
- **FVG 5m**: 19301.66 - 19330.48
- **Entrée**: 19278.71 @ 2025-04-23 08:08:00
- **Stop Loss**: 19283.24
- **Risk**: 4.54 points
- **TP 1RR**: 19274.17 ❌
- **TP 2RR**: 19269.64 ❌
- **TP 3RR**: 19265.10 ❌
- **TP 4RR**: 19260.56 ❌
- **TP 15RR**: 19210.66 ❌
- **PnL**: -4.54 points (-1.0R)
- **MFE**: 10.46 points
- **MAE**: 19.64 points

### Trade #634 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 08:30:00
- **FVG 5m**: 19471.51 - 19486.81
- **Entrée**: 19468.70 @ 2025-04-23 09:51:00
- **Stop Loss**: 19506.50
- **Risk**: 37.80 points
- **TP 1RR**: 19430.90 ✅
- **TP 2RR**: 19393.10 ✅
- **TP 3RR**: 19355.30 ✅
- **TP 4RR**: 19317.50 ✅
- **TP 15RR**: 18901.68 ❌
- **PnL**: -37.80 points (-1.0R)
- **MFE**: 500.11 points
- **MAE**: 39.53 points

### Trade #635 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 09:30:00
- **FVG 5m**: 19471.51 - 19486.81
- **Entrée**: 19468.70 @ 2025-04-23 09:51:00
- **Stop Loss**: 19560.60
- **Risk**: 91.89 points
- **TP 1RR**: 19376.81 ✅
- **TP 2RR**: 19284.91 ✅
- **TP 3RR**: 19193.02 ✅
- **TP 4RR**: 19101.13 ✅
- **TP 15RR**: 18090.29 ❌
- **PnL**: -91.89 points (-1.0R)
- **MFE**: 500.11 points
- **MAE**: 96.91 points

### Trade #636 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-23 10:15:00
- **FVG 5m**: 19230.51 - 19263.41
- **Entrée**: 19202.45 @ 2025-04-23 10:48:00
- **Stop Loss**: 19459.04
- **Risk**: 256.59 points
- **TP 1RR**: 18945.86 ❌
- **TP 2RR**: 18689.27 ❌
- **TP 3RR**: 18432.68 ❌
- **TP 4RR**: 18176.09 ❌
- **TP 15RR**: 15353.60 ❌
- **PnL**: -256.59 points (-1.0R)
- **MFE**: 233.86 points
- **MAE**: 258.85 points

### Trade #637 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 10:45:00
- **FVG 5m**: 19160.12 - 19202.20
- **Entrée**: 19214.44 @ 2025-04-23 11:29:00
- **Stop Loss**: 19165.58
- **Risk**: 48.86 points
- **TP 1RR**: 19263.30 ✅
- **TP 2RR**: 19312.16 ✅
- **TP 3RR**: 19361.03 ❌
- **TP 4RR**: 19409.89 ❌
- **TP 15RR**: 19947.37 ❌
- **PnL**: -48.86 points (-1.0R)
- **MFE**: 133.12 points
- **MAE**: 49.48 points

### Trade #638 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 10:45:00
- **FVG 5m**: 19160.12 - 19202.20
- **Entrée**: 19214.44 @ 2025-04-23 11:29:00
- **Stop Loss**: 19165.58
- **Risk**: 48.86 points
- **TP 1RR**: 19263.30 ✅
- **TP 2RR**: 19312.16 ✅
- **TP 3RR**: 19361.03 ❌
- **TP 4RR**: 19409.89 ❌
- **TP 15RR**: 19947.37 ❌
- **PnL**: -48.86 points (-1.0R)
- **MFE**: 133.12 points
- **MAE**: 49.48 points

### Trade #639 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 14:30:00
- **FVG 5m**: 19157.32 - 19162.16
- **Entrée**: 19164.20 @ 2025-04-23 14:49:00
- **Stop Loss**: 19096.76
- **Risk**: 67.44 points
- **TP 1RR**: 19231.65 ✅
- **TP 2RR**: 19299.09 ✅
- **TP 3RR**: 19366.53 ❌
- **TP 4RR**: 19433.98 ❌
- **TP 15RR**: 20175.86 ❌
- **PnL**: -67.44 points (-1.0R)
- **MFE**: 143.32 points
- **MAE**: 69.11 points

### Trade #640 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 23:30:00
- **FVG 5m**: 19120.08 - 19137.17
- **Entrée**: 19145.07 @ 2025-04-23 23:42:00
- **Stop Loss**: 19077.38
- **Risk**: 67.69 points
- **TP 1RR**: 19212.76 ❌
- **TP 2RR**: 19280.45 ❌
- **TP 3RR**: 19348.14 ❌
- **TP 4RR**: 19415.83 ❌
- **TP 15RR**: 20160.42 ❌
- **PnL**: -67.69 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 91.04 points

### Trade #641 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-23 23:30:00
- **FVG 5m**: 19120.08 - 19137.17
- **Entrée**: 19145.07 @ 2025-04-23 23:42:00
- **Stop Loss**: 19077.38
- **Risk**: 67.69 points
- **TP 1RR**: 19212.76 ❌
- **TP 2RR**: 19280.45 ❌
- **TP 3RR**: 19348.14 ❌
- **TP 4RR**: 19415.83 ❌
- **TP 15RR**: 20160.42 ❌
- **PnL**: -67.69 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 91.04 points

### Trade #642 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-24 03:45:00
- **FVG 5m**: 18990.53 - 19004.55
- **Entrée**: 19013.23 @ 2025-04-24 04:00:00
- **Stop Loss**: 18959.11
- **Risk**: 54.11 points
- **TP 1RR**: 19067.34 ✅
- **TP 2RR**: 19121.45 ✅
- **TP 3RR**: 19175.57 ✅
- **TP 4RR**: 19229.68 ✅
- **TP 15RR**: 19824.93 ✅
- **PnL**: 811.71 points (15.0R)
- **MFE**: 812.51 points
- **MAE**: 6.38 points

### Trade #643 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 06:00:00
- **FVG 5m**: 19133.09 - 19150.17
- **Entrée**: 19127.48 @ 2025-04-24 06:18:00
- **Stop Loss**: 19211.04
- **Risk**: 83.56 points
- **TP 1RR**: 19043.92 ❌
- **TP 2RR**: 18960.36 ❌
- **TP 3RR**: 18876.80 ❌
- **TP 4RR**: 18793.24 ❌
- **TP 15RR**: 17874.10 ❌
- **PnL**: -83.56 points (-1.0R)
- **MFE**: 21.42 points
- **MAE**: 87.47 points

### Trade #644 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 06:00:00
- **FVG 5m**: 19133.09 - 19150.17
- **Entrée**: 19127.48 @ 2025-04-24 06:18:00
- **Stop Loss**: 19211.04
- **Risk**: 83.56 points
- **TP 1RR**: 19043.92 ❌
- **TP 2RR**: 18960.36 ❌
- **TP 3RR**: 18876.80 ❌
- **TP 4RR**: 18793.24 ❌
- **TP 15RR**: 17874.10 ❌
- **PnL**: -83.56 points (-1.0R)
- **MFE**: 21.42 points
- **MAE**: 87.47 points

### Trade #645 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 09:30:00
- **FVG 5m**: 19514.61 - 19526.85
- **Entrée**: 19513.84 @ 2025-04-24 09:43:00
- **Stop Loss**: 19575.40
- **Risk**: 61.55 points
- **TP 1RR**: 19452.29 ❌
- **TP 2RR**: 19390.74 ❌
- **TP 3RR**: 19329.18 ❌
- **TP 4RR**: 19267.63 ❌
- **TP 15RR**: 18590.54 ❌
- **PnL**: -61.55 points (-1.0R)
- **MFE**: 42.84 points
- **MAE**: 75.74 points

### Trade #646 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-24 22:15:00
- **FVG 5m**: 19805.34 - 19810.69
- **Entrée**: 19819.87 @ 2025-04-24 22:34:00
- **Stop Loss**: 19752.10
- **Risk**: 67.77 points
- **TP 1RR**: 19887.65 ✅
- **TP 2RR**: 19955.42 ❌
- **TP 3RR**: 20023.19 ❌
- **TP 4RR**: 20090.96 ❌
- **TP 15RR**: 20836.45 ❌
- **PnL**: -67.77 points (-1.0R)
- **MFE**: 69.62 points
- **MAE**: 80.08 points

### Trade #647 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-24 23:15:00
- **FVG 5m**: 19820.89 - 19842.57
- **Entrée**: 19810.95 @ 2025-04-24 23:27:00
- **Stop Loss**: 19899.44
- **Risk**: 88.49 points
- **TP 1RR**: 19722.45 ✅
- **TP 2RR**: 19633.96 ✅
- **TP 3RR**: 19545.47 ❌
- **TP 4RR**: 19456.98 ❌
- **TP 15RR**: 18483.56 ❌
- **PnL**: -88.49 points (-1.0R)
- **MFE**: 208.36 points
- **MAE**: 89.77 points

### Trade #648 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-25 04:15:00
- **FVG 5m**: 19770.91 - 19778.81
- **Entrée**: 19780.85 @ 2025-04-25 04:51:00
- **Stop Loss**: 19723.30
- **Risk**: 57.56 points
- **TP 1RR**: 19838.41 ❌
- **TP 2RR**: 19895.97 ❌
- **TP 3RR**: 19953.52 ❌
- **TP 4RR**: 20011.08 ❌
- **TP 15RR**: 20644.20 ❌
- **PnL**: -57.56 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 77.78 points

### Trade #649 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-25 04:15:00
- **FVG 5m**: 19770.91 - 19778.81
- **Entrée**: 19780.85 @ 2025-04-25 04:51:00
- **Stop Loss**: 19723.30
- **Risk**: 57.56 points
- **TP 1RR**: 19838.41 ❌
- **TP 2RR**: 19895.97 ❌
- **TP 3RR**: 19953.52 ❌
- **TP 4RR**: 20011.08 ❌
- **TP 15RR**: 20644.20 ❌
- **PnL**: -57.56 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 77.78 points

### Trade #650 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-25 15:30:00
- **FVG 5m**: 19917.04 - 19941.27
- **Entrée**: 19896.13 @ 2025-04-27 17:00:00
- **Stop Loss**: 19992.83
- **Risk**: 96.70 points
- **TP 1RR**: 19799.43 ✅
- **TP 2RR**: 19702.73 ❌
- **TP 3RR**: 19606.03 ❌
- **TP 4RR**: 19509.32 ❌
- **TP 15RR**: 18445.62 ❌
- **PnL**: -96.70 points (-1.0R)
- **MFE**: 114.00 points
- **MAE**: 97.16 points

### Trade #651 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-27 20:15:00
- **FVG 5m**: 19822.17 - 19827.01
- **Entrée**: 19807.12 @ 2025-04-27 21:55:00
- **Stop Loss**: 19833.36
- **Risk**: 26.23 points
- **TP 1RR**: 19780.89 ❌
- **TP 2RR**: 19754.66 ❌
- **TP 3RR**: 19728.42 ❌
- **TP 4RR**: 19702.19 ❌
- **TP 15RR**: 19413.62 ❌
- **PnL**: -26.23 points (-1.0R)
- **MFE**: 21.93 points
- **MAE**: 28.05 points

### Trade #652 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 04:45:00
- **FVG 5m**: 19913.21 - 19919.84
- **Entrée**: 19911.17 @ 2025-04-28 04:56:00
- **Stop Loss**: 19942.82
- **Risk**: 31.64 points
- **TP 1RR**: 19879.53 ✅
- **TP 2RR**: 19847.89 ❌
- **TP 3RR**: 19816.24 ❌
- **TP 4RR**: 19784.60 ❌
- **TP 15RR**: 19436.52 ❌
- **PnL**: -31.64 points (-1.0R)
- **MFE**: 53.56 points
- **MAE**: 31.88 points

### Trade #653 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 08:45:00
- **FVG 5m**: 19897.66 - 19928.26
- **Entrée**: 19882.35 @ 2025-04-28 08:57:00
- **Stop Loss**: 20027.53
- **Risk**: 145.17 points
- **TP 1RR**: 19737.18 ✅
- **TP 2RR**: 19592.01 ❌
- **TP 3RR**: 19446.84 ❌
- **TP 4RR**: 19301.66 ❌
- **TP 15RR**: 17704.76 ❌
- **PnL**: -145.17 points (-1.0R)
- **MFE**: 237.94 points
- **MAE**: 154.80 points

### Trade #654 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 08:45:00
- **FVG 5m**: 19897.66 - 19928.26
- **Entrée**: 19882.35 @ 2025-04-28 08:57:00
- **Stop Loss**: 20027.53
- **Risk**: 145.17 points
- **TP 1RR**: 19737.18 ✅
- **TP 2RR**: 19592.01 ❌
- **TP 3RR**: 19446.84 ❌
- **TP 4RR**: 19301.66 ❌
- **TP 15RR**: 17704.76 ❌
- **PnL**: -145.17 points (-1.0R)
- **MFE**: 237.94 points
- **MAE**: 154.80 points

### Trade #655 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 10:00:00
- **FVG 5m**: 19745.92 - 19788.25
- **Entrée**: 19742.86 @ 2025-04-28 10:24:00
- **Stop Loss**: 19897.91
- **Risk**: 155.05 points
- **TP 1RR**: 19587.80 ❌
- **TP 2RR**: 19432.75 ❌
- **TP 3RR**: 19277.69 ❌
- **TP 4RR**: 19122.64 ❌
- **TP 15RR**: 17417.05 ❌
- **PnL**: -155.05 points (-1.0R)
- **MFE**: 98.44 points
- **MAE**: 160.16 points

### Trade #656 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 10:15:00
- **FVG 5m**: 19711.74 - 19721.18
- **Entrée**: 19705.37 @ 2025-04-28 11:01:00
- **Stop Loss**: 19842.80
- **Risk**: 137.43 points
- **TP 1RR**: 19567.94 ❌
- **TP 2RR**: 19430.51 ❌
- **TP 3RR**: 19293.08 ❌
- **TP 4RR**: 19155.65 ❌
- **TP 15RR**: 17643.92 ❌
- **PnL**: -137.43 points (-1.0R)
- **MFE**: 60.95 points
- **MAE**: 144.85 points

### Trade #657 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:00:00
- **FVG 5m**: 19779.58 - 19785.19
- **Entrée**: 19793.61 @ 2025-04-28 13:24:00
- **Stop Loss**: 19736.04
- **Risk**: 57.56 points
- **TP 1RR**: 19851.17 ✅
- **TP 2RR**: 19908.73 ✅
- **TP 3RR**: 19966.29 ✅
- **TP 4RR**: 20023.86 ✅
- **TP 15RR**: 20657.05 ❌
- **PnL**: -57.56 points (-1.0R)
- **MFE**: 290.73 points
- **MAE**: 60.19 points

### Trade #658 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:15:00
- **FVG 5m**: 19803.81 - 19806.10
- **Entrée**: 19808.40 @ 2025-04-28 13:39:00
- **Stop Loss**: 19742.16
- **Risk**: 66.24 points
- **TP 1RR**: 19874.63 ✅
- **TP 2RR**: 19940.87 ✅
- **TP 3RR**: 20007.11 ✅
- **TP 4RR**: 20073.34 ✅
- **TP 15RR**: 20801.95 ❌
- **PnL**: -66.24 points (-1.0R)
- **MFE**: 275.94 points
- **MAE**: 68.35 points

### Trade #659 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:15:00
- **FVG 5m**: 19803.81 - 19806.10
- **Entrée**: 19808.40 @ 2025-04-28 13:39:00
- **Stop Loss**: 19742.16
- **Risk**: 66.24 points
- **TP 1RR**: 19874.63 ✅
- **TP 2RR**: 19940.87 ✅
- **TP 3RR**: 20007.11 ✅
- **TP 4RR**: 20073.34 ✅
- **TP 15RR**: 20801.95 ❌
- **PnL**: -66.24 points (-1.0R)
- **MFE**: 275.94 points
- **MAE**: 68.35 points

### Trade #660 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-28 13:15:00
- **FVG 5m**: 19803.81 - 19806.10
- **Entrée**: 19808.40 @ 2025-04-28 13:39:00
- **Stop Loss**: 19742.16
- **Risk**: 66.24 points
- **TP 1RR**: 19874.63 ✅
- **TP 2RR**: 19940.87 ✅
- **TP 3RR**: 20007.11 ✅
- **TP 4RR**: 20073.34 ✅
- **TP 15RR**: 20801.95 ❌
- **PnL**: -66.24 points (-1.0R)
- **MFE**: 275.94 points
- **MAE**: 68.35 points

### Trade #661 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-28 21:30:00
- **FVG 5m**: 19971.61 - 20001.45
- **Entrée**: 19964.73 @ 2025-04-28 21:45:00
- **Stop Loss**: 20026.76
- **Risk**: 62.03 points
- **TP 1RR**: 19902.69 ✅
- **TP 2RR**: 19840.66 ✅
- **TP 3RR**: 19778.63 ✅
- **TP 4RR**: 19716.59 ❌
- **TP 15RR**: 19034.22 ❌
- **PnL**: -62.03 points (-1.0R)
- **MFE**: 197.14 points
- **MAE**: 72.43 points

### Trade #662 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 03:00:00
- **FVG 5m**: 19981.82 - 19984.62
- **Entrée**: 19978.24 @ 2025-04-29 03:56:00
- **Stop Loss**: 20015.02
- **Risk**: 36.78 points
- **TP 1RR**: 19941.46 ✅
- **TP 2RR**: 19904.68 ✅
- **TP 3RR**: 19867.90 ✅
- **TP 4RR**: 19831.12 ✅
- **TP 15RR**: 19426.54 ❌
- **PnL**: -36.78 points (-1.0R)
- **MFE**: 210.65 points
- **MAE**: 58.91 points

### Trade #663 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-29 08:30:00
- **FVG 5m**: 19841.55 - 19860.42
- **Entrée**: 19863.48 @ 2025-04-29 08:44:00
- **Stop Loss**: 19783.96
- **Risk**: 79.52 points
- **TP 1RR**: 19943.00 ✅
- **TP 2RR**: 20022.52 ✅
- **TP 3RR**: 20102.04 ❌
- **TP 4RR**: 20181.56 ❌
- **TP 15RR**: 21056.27 ❌
- **PnL**: -79.52 points (-1.0R)
- **MFE**: 220.85 points
- **MAE**: 79.82 points

### Trade #664 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-29 08:30:00
- **FVG 5m**: 19841.55 - 19860.42
- **Entrée**: 19863.48 @ 2025-04-29 08:44:00
- **Stop Loss**: 19783.96
- **Risk**: 79.52 points
- **TP 1RR**: 19943.00 ✅
- **TP 2RR**: 20022.52 ✅
- **TP 3RR**: 20102.04 ❌
- **TP 4RR**: 20181.56 ❌
- **TP 15RR**: 21056.27 ❌
- **PnL**: -79.52 points (-1.0R)
- **MFE**: 220.85 points
- **MAE**: 79.82 points

### Trade #665 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20007.06 - 20024.40
- **Entrée**: 19976.46 @ 2025-04-29 15:30:00
- **Stop Loss**: 20047.94
- **Risk**: 71.48 points
- **TP 1RR**: 19904.98 ✅
- **TP 2RR**: 19833.50 ✅
- **TP 3RR**: 19762.02 ✅
- **TP 4RR**: 19690.54 ✅
- **TP 15RR**: 18904.26 ❌
- **PnL**: -71.48 points (-1.0R)
- **MFE**: 488.63 points
- **MAE**: 81.86 points

### Trade #666 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20007.06 - 20024.40
- **Entrée**: 19976.46 @ 2025-04-29 15:30:00
- **Stop Loss**: 20047.94
- **Risk**: 71.48 points
- **TP 1RR**: 19904.98 ✅
- **TP 2RR**: 19833.50 ✅
- **TP 3RR**: 19762.02 ✅
- **TP 4RR**: 19690.54 ✅
- **TP 15RR**: 18904.26 ❌
- **PnL**: -71.48 points (-1.0R)
- **MFE**: 488.63 points
- **MAE**: 81.86 points

### Trade #667 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20007.06 - 20024.40
- **Entrée**: 19976.46 @ 2025-04-29 15:30:00
- **Stop Loss**: 20047.94
- **Risk**: 71.48 points
- **TP 1RR**: 19904.98 ✅
- **TP 2RR**: 19833.50 ✅
- **TP 3RR**: 19762.02 ✅
- **TP 4RR**: 19690.54 ✅
- **TP 15RR**: 18904.26 ❌
- **PnL**: -71.48 points (-1.0R)
- **MFE**: 488.63 points
- **MAE**: 81.86 points

### Trade #668 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-29 15:15:00
- **FVG 5m**: 20007.06 - 20024.40
- **Entrée**: 19976.46 @ 2025-04-29 15:30:00
- **Stop Loss**: 20047.94
- **Risk**: 71.48 points
- **TP 1RR**: 19904.98 ✅
- **TP 2RR**: 19833.50 ✅
- **TP 3RR**: 19762.02 ✅
- **TP 4RR**: 19690.54 ✅
- **TP 15RR**: 18904.26 ❌
- **PnL**: -71.48 points (-1.0R)
- **MFE**: 488.63 points
- **MAE**: 81.86 points

### Trade #669 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 01:00:00
- **FVG 5m**: 19979.77 - 19985.39
- **Entrée**: 19986.15 @ 2025-04-30 03:09:00
- **Stop Loss**: 19916.77
- **Risk**: 69.38 points
- **TP 1RR**: 20055.53 ❌
- **TP 2RR**: 20124.92 ❌
- **TP 3RR**: 20194.30 ❌
- **TP 4RR**: 20263.69 ❌
- **TP 15RR**: 21026.92 ❌
- **PnL**: -69.38 points (-1.0R)
- **MFE**: 31.11 points
- **MAE**: 71.41 points

### Trade #670 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 09:00:00
- **FVG 5m**: 19611.52 - 19621.72
- **Entrée**: 19627.84 @ 2025-04-30 09:13:00
- **Stop Loss**: 19478.09
- **Risk**: 149.75 points
- **TP 1RR**: 19777.59 ✅
- **TP 2RR**: 19927.35 ✅
- **TP 3RR**: 20077.10 ✅
- **TP 4RR**: 20226.85 ✅
- **TP 15RR**: 21874.14 ✅
- **PnL**: 2246.30 points (15.0R)
- **MFE**: 2249.33 points
- **MAE**: 6.12 points

### Trade #671 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 09:00:00
- **FVG 5m**: 19611.52 - 19621.72
- **Entrée**: 19627.84 @ 2025-04-30 09:13:00
- **Stop Loss**: 19478.09
- **Risk**: 149.75 points
- **TP 1RR**: 19777.59 ✅
- **TP 2RR**: 19927.35 ✅
- **TP 3RR**: 20077.10 ✅
- **TP 4RR**: 20226.85 ✅
- **TP 15RR**: 21874.14 ✅
- **PnL**: 2246.30 points (15.0R)
- **MFE**: 2249.33 points
- **MAE**: 6.12 points

### Trade #672 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 09:00:00
- **FVG 5m**: 19611.52 - 19621.72
- **Entrée**: 19627.84 @ 2025-04-30 09:13:00
- **Stop Loss**: 19478.09
- **Risk**: 149.75 points
- **TP 1RR**: 19777.59 ✅
- **TP 2RR**: 19927.35 ✅
- **TP 3RR**: 20077.10 ✅
- **TP 4RR**: 20226.85 ✅
- **TP 15RR**: 21874.14 ✅
- **PnL**: 2246.30 points (15.0R)
- **MFE**: 2249.33 points
- **MAE**: 6.12 points

### Trade #673 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 10:00:00
- **FVG 5m**: 19779.83 - 19804.32
- **Entrée**: 19805.85 @ 2025-04-30 11:37:00
- **Stop Loss**: 19706.22
- **Risk**: 99.63 points
- **TP 1RR**: 19905.47 ✅
- **TP 2RR**: 20005.10 ✅
- **TP 3RR**: 20104.73 ✅
- **TP 4RR**: 20204.36 ✅
- **TP 15RR**: 21300.26 ✅
- **PnL**: 1494.41 points (15.0R)
- **MFE**: 1501.08 points
- **MAE**: 80.08 points

### Trade #674 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 12:30:00
- **FVG 5m**: 19875.72 - 19890.52
- **Entrée**: 19919.84 @ 2025-04-30 13:07:00
- **Stop Loss**: 19828.32
- **Risk**: 91.53 points
- **TP 1RR**: 20011.37 ✅
- **TP 2RR**: 20102.90 ✅
- **TP 3RR**: 20194.43 ✅
- **TP 4RR**: 20285.95 ✅
- **TP 15RR**: 21292.76 ✅
- **PnL**: 1372.91 points (15.0R)
- **MFE**: 1374.85 points
- **MAE**: 81.35 points

### Trade #675 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 12:30:00
- **FVG 5m**: 19875.72 - 19890.52
- **Entrée**: 19919.84 @ 2025-04-30 13:07:00
- **Stop Loss**: 19828.32
- **Risk**: 91.53 points
- **TP 1RR**: 20011.37 ✅
- **TP 2RR**: 20102.90 ✅
- **TP 3RR**: 20194.43 ✅
- **TP 4RR**: 20285.95 ✅
- **TP 15RR**: 21292.76 ✅
- **PnL**: 1372.91 points (15.0R)
- **MFE**: 1374.85 points
- **MAE**: 81.35 points

### Trade #676 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 13:00:00
- **FVG 5m**: 19866.80 - 19878.78
- **Entrée**: 19863.48 @ 2025-04-30 13:36:00
- **Stop Loss**: 19985.68
- **Risk**: 122.20 points
- **TP 1RR**: 19741.28 ❌
- **TP 2RR**: 19619.08 ❌
- **TP 3RR**: 19496.88 ❌
- **TP 4RR**: 19374.69 ❌
- **TP 15RR**: 18030.49 ❌
- **PnL**: -122.20 points (-1.0R)
- **MFE**: 24.99 points
- **MAE**: 166.53 points

### Trade #677 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-04-30 13:00:00
- **FVG 5m**: 19866.80 - 19888.48
- **Entrée**: 19893.83 @ 2025-04-30 13:48:00
- **Stop Loss**: 19837.75
- **Risk**: 56.08 points
- **TP 1RR**: 19949.91 ✅
- **TP 2RR**: 20006.00 ✅
- **TP 3RR**: 20062.08 ✅
- **TP 4RR**: 20118.17 ✅
- **TP 15RR**: 20735.08 ✅
- **PnL**: 841.25 points (15.0R)
- **MFE**: 844.90 points
- **MAE**: 35.19 points

### Trade #678 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 19:15:00
- **FVG 5m**: 20330.69 - 20339.87
- **Entrée**: 20315.13 @ 2025-04-30 20:09:00
- **Stop Loss**: 20367.14
- **Risk**: 52.00 points
- **TP 1RR**: 20263.13 ❌
- **TP 2RR**: 20211.13 ❌
- **TP 3RR**: 20159.13 ❌
- **TP 4RR**: 20107.12 ❌
- **TP 15RR**: 19535.09 ❌
- **PnL**: -52.00 points (-1.0R)
- **MFE**: 7.91 points
- **MAE**: 53.56 points

### Trade #679 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-04-30 23:00:00
- **FVG 5m**: 20343.70 - 20345.99
- **Entrée**: 20340.89 @ 2025-04-30 23:24:00
- **Stop Loss**: 20378.87
- **Risk**: 37.98 points
- **TP 1RR**: 20302.91 ✅
- **TP 2RR**: 20264.93 ❌
- **TP 3RR**: 20226.95 ❌
- **TP 4RR**: 20188.96 ❌
- **TP 15RR**: 19771.16 ❌
- **PnL**: -37.98 points (-1.0R)
- **MFE**: 39.53 points
- **MAE**: 42.33 points

### Trade #680 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 07:45:00
- **FVG 5m**: 20366.39 - 20368.43
- **Entrée**: 20321.76 @ 2025-05-01 08:31:00
- **Stop Loss**: 20398.01
- **Risk**: 76.25 points
- **TP 1RR**: 20245.52 ❌
- **TP 2RR**: 20169.27 ❌
- **TP 3RR**: 20093.03 ❌
- **TP 4RR**: 20016.78 ❌
- **TP 15RR**: 19178.08 ❌
- **PnL**: -76.25 points (-1.0R)
- **MFE**: 33.66 points
- **MAE**: 76.51 points

### Trade #681 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 07:45:00
- **FVG 5m**: 20366.39 - 20368.43
- **Entrée**: 20321.76 @ 2025-05-01 08:31:00
- **Stop Loss**: 20398.01
- **Risk**: 76.25 points
- **TP 1RR**: 20245.52 ❌
- **TP 2RR**: 20169.27 ❌
- **TP 3RR**: 20093.03 ❌
- **TP 4RR**: 20016.78 ❌
- **TP 15RR**: 19178.08 ❌
- **PnL**: -76.25 points (-1.0R)
- **MFE**: 33.66 points
- **MAE**: 76.51 points

### Trade #682 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 08:30:00
- **FVG 5m**: 20335.54 - 20337.83
- **Entrée**: 20357.47 @ 2025-05-01 09:17:00
- **Stop Loss**: 20277.96
- **Risk**: 79.51 points
- **TP 1RR**: 20436.98 ✅
- **TP 2RR**: 20516.49 ✅
- **TP 3RR**: 20596.00 ❌
- **TP 4RR**: 20675.51 ❌
- **TP 15RR**: 21550.14 ❌
- **PnL**: -79.51 points (-1.0R)
- **MFE**: 172.91 points
- **MAE**: 87.47 points

### Trade #683 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 08:30:00
- **FVG 5m**: 20335.54 - 20337.83
- **Entrée**: 20357.47 @ 2025-05-01 09:17:00
- **Stop Loss**: 20277.96
- **Risk**: 79.51 points
- **TP 1RR**: 20436.98 ✅
- **TP 2RR**: 20516.49 ✅
- **TP 3RR**: 20596.00 ❌
- **TP 4RR**: 20675.51 ❌
- **TP 15RR**: 21550.14 ❌
- **PnL**: -79.51 points (-1.0R)
- **MFE**: 172.91 points
- **MAE**: 87.47 points

### Trade #684 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 08:30:00
- **FVG 5m**: 20335.54 - 20337.83
- **Entrée**: 20357.47 @ 2025-05-01 09:17:00
- **Stop Loss**: 20277.96
- **Risk**: 79.51 points
- **TP 1RR**: 20436.98 ✅
- **TP 2RR**: 20516.49 ✅
- **TP 3RR**: 20596.00 ❌
- **TP 4RR**: 20675.51 ❌
- **TP 15RR**: 21550.14 ❌
- **PnL**: -79.51 points (-1.0R)
- **MFE**: 172.91 points
- **MAE**: 87.47 points

### Trade #685 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 09:30:00
- **FVG 5m**: 20431.43 - 20433.98
- **Entrée**: 20426.07 @ 2025-05-01 10:49:00
- **Stop Loss**: 20460.01
- **Risk**: 33.94 points
- **TP 1RR**: 20392.13 ✅
- **TP 2RR**: 20358.19 ✅
- **TP 3RR**: 20324.24 ✅
- **TP 4RR**: 20290.30 ✅
- **TP 15RR**: 19916.94 ❌
- **PnL**: -33.94 points (-1.0R)
- **MFE**: 279.51 points
- **MAE**: 41.57 points

### Trade #686 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 09:30:00
- **FVG 5m**: 20431.43 - 20433.98
- **Entrée**: 20426.07 @ 2025-05-01 10:49:00
- **Stop Loss**: 20460.01
- **Risk**: 33.94 points
- **TP 1RR**: 20392.13 ✅
- **TP 2RR**: 20358.19 ✅
- **TP 3RR**: 20324.24 ✅
- **TP 4RR**: 20290.30 ✅
- **TP 15RR**: 19916.94 ❌
- **PnL**: -33.94 points (-1.0R)
- **MFE**: 279.51 points
- **MAE**: 41.57 points

### Trade #687 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 10:30:00
- **FVG 5m**: 20431.43 - 20433.98
- **Entrée**: 20426.07 @ 2025-05-01 10:49:00
- **Stop Loss**: 20497.78
- **Risk**: 71.71 points
- **TP 1RR**: 20354.37 ✅
- **TP 2RR**: 20282.66 ✅
- **TP 3RR**: 20210.96 ✅
- **TP 4RR**: 20139.25 ❌
- **TP 15RR**: 19350.49 ❌
- **PnL**: -71.71 points (-1.0R)
- **MFE**: 279.51 points
- **MAE**: 75.23 points

### Trade #688 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-01 19:15:00
- **FVG 5m**: 20233.27 - 20260.81
- **Entrée**: 20265.15 @ 2025-05-01 19:29:00
- **Stop Loss**: 20173.45
- **Risk**: 91.70 points
- **TP 1RR**: 20356.85 ✅
- **TP 2RR**: 20448.55 ✅
- **TP 3RR**: 20540.25 ✅
- **TP 4RR**: 20631.95 ✅
- **TP 15RR**: 21640.65 ❌
- **PnL**: -91.70 points (-1.0R)
- **MFE**: 419.26 points
- **MAE**: 110.68 points

### Trade #689 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-01 23:15:00
- **FVG 5m**: 20352.88 - 20366.65
- **Entrée**: 20350.33 @ 2025-05-02 00:38:00
- **Stop Loss**: 20407.20
- **Risk**: 56.87 points
- **TP 1RR**: 20293.46 ✅
- **TP 2RR**: 20236.59 ❌
- **TP 3RR**: 20179.72 ❌
- **TP 4RR**: 20122.85 ❌
- **TP 15RR**: 19497.30 ❌
- **PnL**: -56.87 points (-1.0R)
- **MFE**: 86.96 points
- **MAE**: 78.80 points

### Trade #690 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 01:15:00
- **FVG 5m**: 20307.99 - 20314.37
- **Entrée**: 20316.41 @ 2025-05-02 01:42:00
- **Stop Loss**: 20286.62
- **Risk**: 29.79 points
- **TP 1RR**: 20346.19 ✅
- **TP 2RR**: 20375.98 ❌
- **TP 3RR**: 20405.77 ❌
- **TP 4RR**: 20435.55 ❌
- **TP 15RR**: 20763.19 ❌
- **PnL**: -29.79 points (-1.0R)
- **MFE**: 44.37 points
- **MAE**: 43.61 points

### Trade #691 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 01:15:00
- **FVG 5m**: 20307.99 - 20314.37
- **Entrée**: 20316.41 @ 2025-05-02 01:42:00
- **Stop Loss**: 20286.62
- **Risk**: 29.79 points
- **TP 1RR**: 20346.19 ✅
- **TP 2RR**: 20375.98 ❌
- **TP 3RR**: 20405.77 ❌
- **TP 4RR**: 20435.55 ❌
- **TP 15RR**: 20763.19 ❌
- **PnL**: -29.79 points (-1.0R)
- **MFE**: 44.37 points
- **MAE**: 43.61 points

### Trade #692 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 04:00:00
- **FVG 5m**: 20299.83 - 20303.91
- **Entrée**: 20305.44 @ 2025-05-02 04:14:00
- **Stop Loss**: 20253.23
- **Risk**: 52.21 points
- **TP 1RR**: 20357.65 ✅
- **TP 2RR**: 20409.87 ✅
- **TP 3RR**: 20462.08 ✅
- **TP 4RR**: 20514.29 ✅
- **TP 15RR**: 21088.61 ❌
- **PnL**: -52.21 points (-1.0R)
- **MFE**: 378.97 points
- **MAE**: 53.56 points

### Trade #693 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 11:00:00
- **FVG 5m**: 20632.90 - 20647.69
- **Entrée**: 20648.96 @ 2025-05-02 13:04:00
- **Stop Loss**: 20587.66
- **Risk**: 61.30 points
- **TP 1RR**: 20710.27 ❌
- **TP 2RR**: 20771.57 ❌
- **TP 3RR**: 20832.88 ❌
- **TP 4RR**: 20894.18 ❌
- **TP 15RR**: 21568.53 ❌
- **PnL**: -61.30 points (-1.0R)
- **MFE**: 35.45 points
- **MAE**: 64.01 points

### Trade #694 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-02 11:00:00
- **FVG 5m**: 20632.90 - 20647.69
- **Entrée**: 20648.96 @ 2025-05-02 13:04:00
- **Stop Loss**: 20587.66
- **Risk**: 61.30 points
- **TP 1RR**: 20710.27 ❌
- **TP 2RR**: 20771.57 ❌
- **TP 3RR**: 20832.88 ❌
- **TP 4RR**: 20894.18 ❌
- **TP 15RR**: 21568.53 ❌
- **PnL**: -61.30 points (-1.0R)
- **MFE**: 35.45 points
- **MAE**: 64.01 points

### Trade #695 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-02 13:30:00
- **FVG 5m**: 20641.06 - 20659.16
- **Entrée**: 20634.43 @ 2025-05-02 13:48:00
- **Stop Loss**: 20694.75
- **Risk**: 60.33 points
- **TP 1RR**: 20574.10 ✅
- **TP 2RR**: 20513.77 ✅
- **TP 3RR**: 20453.45 ✅
- **TP 4RR**: 20393.12 ✅
- **TP 15RR**: 19729.52 ❌
- **PnL**: -60.33 points (-1.0R)
- **MFE**: 560.04 points
- **MAE**: 68.35 points

### Trade #696 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-02 14:00:00
- **FVG 5m**: 20573.48 - 20596.94
- **Entrée**: 20558.68 @ 2025-05-04 17:01:00
- **Stop Loss**: 20638.88
- **Risk**: 80.19 points
- **TP 1RR**: 20478.49 ✅
- **TP 2RR**: 20398.30 ✅
- **TP 3RR**: 20318.11 ✅
- **TP 4RR**: 20237.92 ✅
- **TP 15RR**: 19355.81 ❌
- **PnL**: -80.19 points (-1.0R)
- **MFE**: 484.29 points
- **MAE**: 83.90 points

### Trade #697 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-04 17:30:00
- **FVG 5m**: 20526.55 - 20537.52
- **Entrée**: 20520.43 @ 2025-05-04 17:44:00
- **Stop Loss**: 20564.37
- **Risk**: 43.94 points
- **TP 1RR**: 20476.49 ✅
- **TP 2RR**: 20432.55 ✅
- **TP 3RR**: 20388.61 ✅
- **TP 4RR**: 20344.67 ❌
- **TP 15RR**: 19861.32 ❌
- **PnL**: -43.94 points (-1.0R)
- **MFE**: 153.02 points
- **MAE**: 44.88 points

### Trade #698 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-04 17:30:00
- **FVG 5m**: 20526.55 - 20537.52
- **Entrée**: 20520.43 @ 2025-05-04 17:44:00
- **Stop Loss**: 20564.37
- **Risk**: 43.94 points
- **TP 1RR**: 20476.49 ✅
- **TP 2RR**: 20432.55 ✅
- **TP 3RR**: 20388.61 ✅
- **TP 4RR**: 20344.67 ❌
- **TP 15RR**: 19861.32 ❌
- **PnL**: -43.94 points (-1.0R)
- **MFE**: 153.02 points
- **MAE**: 44.88 points

### Trade #699 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-04 22:30:00
- **FVG 5m**: 20444.18 - 20453.36
- **Entrée**: 20461.52 @ 2025-05-05 00:01:00
- **Stop Loss**: 20414.33
- **Risk**: 47.19 points
- **TP 1RR**: 20508.71 ❌
- **TP 2RR**: 20555.90 ❌
- **TP 3RR**: 20603.09 ❌
- **TP 4RR**: 20650.28 ❌
- **TP 15RR**: 21169.39 ❌
- **PnL**: -47.19 points (-1.0R)
- **MFE**: 41.31 points
- **MAE**: 47.43 points

### Trade #700 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-05 01:45:00
- **FVG 5m**: 20451.06 - 20463.56
- **Entrée**: 20442.14 @ 2025-05-05 03:30:00
- **Stop Loss**: 20503.13
- **Risk**: 61.00 points
- **TP 1RR**: 20381.14 ✅
- **TP 2RR**: 20320.14 ❌
- **TP 3RR**: 20259.15 ❌
- **TP 4RR**: 20198.15 ❌
- **TP 15RR**: 19527.19 ❌
- **PnL**: -61.00 points (-1.0R)
- **MFE**: 74.72 points
- **MAE**: 73.19 points

### Trade #701 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-05 03:45:00
- **FVG 5m**: 20407.20 - 20410.77
- **Entrée**: 20415.10 @ 2025-05-05 04:21:00
- **Stop Loss**: 20368.70
- **Risk**: 46.40 points
- **TP 1RR**: 20461.51 ❌
- **TP 2RR**: 20507.91 ❌
- **TP 3RR**: 20554.31 ❌
- **TP 4RR**: 20600.72 ❌
- **TP 15RR**: 21111.15 ❌
- **PnL**: -46.40 points (-1.0R)
- **MFE**: 15.81 points
- **MAE**: 47.69 points

### Trade #702 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-05 06:45:00
- **FVG 5m**: 20393.17 - 20398.02
- **Entrée**: 20400.31 @ 2025-05-05 07:09:00
- **Stop Loss**: 20357.23
- **Risk**: 43.08 points
- **TP 1RR**: 20443.40 ✅
- **TP 2RR**: 20486.48 ✅
- **TP 3RR**: 20529.56 ✅
- **TP 4RR**: 20572.64 ✅
- **TP 15RR**: 21046.54 ❌
- **PnL**: -43.08 points (-1.0R)
- **MFE**: 197.14 points
- **MAE**: 44.63 points

### Trade #703 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-05 08:30:00
- **FVG 5m**: 20452.08 - 20455.40
- **Entrée**: 20457.69 @ 2025-05-05 08:56:00
- **Stop Loss**: 20376.86
- **Risk**: 80.84 points
- **TP 1RR**: 20538.53 ✅
- **TP 2RR**: 20619.37 ❌
- **TP 3RR**: 20700.20 ❌
- **TP 4RR**: 20781.04 ❌
- **TP 15RR**: 21670.23 ❌
- **PnL**: -80.84 points (-1.0R)
- **MFE**: 139.75 points
- **MAE**: 80.84 points

### Trade #704 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-05 21:00:00
- **FVG 5m**: 20345.99 - 20353.90
- **Entrée**: 20344.46 @ 2025-05-05 22:04:00
- **Stop Loss**: 20382.96
- **Risk**: 38.49 points
- **TP 1RR**: 20305.97 ❌
- **TP 2RR**: 20267.47 ❌
- **TP 3RR**: 20228.98 ❌
- **TP 4RR**: 20190.49 ❌
- **TP 15RR**: 19767.05 ❌
- **PnL**: -38.49 points (-1.0R)
- **MFE**: 11.48 points
- **MAE**: 40.80 points

### Trade #705 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 03:30:00
- **FVG 5m**: 20263.62 - 20270.25
- **Entrée**: 20271.78 @ 2025-05-06 03:42:00
- **Stop Loss**: 20220.61
- **Risk**: 51.17 points
- **TP 1RR**: 20322.95 ❌
- **TP 2RR**: 20374.13 ❌
- **TP 3RR**: 20425.30 ❌
- **TP 4RR**: 20476.48 ❌
- **TP 15RR**: 21039.40 ❌
- **PnL**: -51.17 points (-1.0R)
- **MFE**: 36.72 points
- **MAE**: 56.62 points

### Trade #706 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 06:45:00
- **FVG 5m**: 20215.67 - 20224.09
- **Entrée**: 20227.66 @ 2025-05-06 07:48:00
- **Stop Loss**: 20194.10
- **Risk**: 33.56 points
- **TP 1RR**: 20261.22 ❌
- **TP 2RR**: 20294.79 ❌
- **TP 3RR**: 20328.35 ❌
- **TP 4RR**: 20361.92 ❌
- **TP 15RR**: 20731.13 ❌
- **PnL**: -33.56 points (-1.0R)
- **MFE**: 18.36 points
- **MAE**: 34.43 points

### Trade #707 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 09:00:00
- **FVG 5m**: 20244.49 - 20267.19
- **Entrée**: 20277.90 @ 2025-05-06 09:20:00
- **Stop Loss**: 20125.78
- **Risk**: 152.12 points
- **TP 1RR**: 20430.02 ✅
- **TP 2RR**: 20582.14 ❌
- **TP 3RR**: 20734.25 ❌
- **TP 4RR**: 20886.37 ❌
- **TP 15RR**: 22559.66 ❌
- **PnL**: -152.12 points (-1.0R)
- **MFE**: 260.64 points
- **MAE**: 167.81 points

### Trade #708 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 09:00:00
- **FVG 5m**: 20244.49 - 20267.19
- **Entrée**: 20277.90 @ 2025-05-06 09:20:00
- **Stop Loss**: 20125.78
- **Risk**: 152.12 points
- **TP 1RR**: 20430.02 ✅
- **TP 2RR**: 20582.14 ❌
- **TP 3RR**: 20734.25 ❌
- **TP 4RR**: 20886.37 ❌
- **TP 15RR**: 22559.66 ❌
- **PnL**: -152.12 points (-1.0R)
- **MFE**: 260.64 points
- **MAE**: 167.81 points

### Trade #709 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 09:30:00
- **FVG 5m**: 20311.31 - 20359.25
- **Entrée**: 20389.09 @ 2025-05-06 11:13:00
- **Stop Loss**: 20270.82
- **Risk**: 118.27 points
- **TP 1RR**: 20507.36 ❌
- **TP 2RR**: 20625.64 ❌
- **TP 3RR**: 20743.91 ❌
- **TP 4RR**: 20862.18 ❌
- **TP 15RR**: 22163.17 ❌
- **PnL**: -118.27 points (-1.0R)
- **MFE**: 39.78 points
- **MAE**: 119.61 points

### Trade #710 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 09:45:00
- **FVG 5m**: 20319.47 - 20336.05
- **Entrée**: 20311.31 @ 2025-05-06 10:42:00
- **Stop Loss**: 20348.77
- **Risk**: 37.46 points
- **TP 1RR**: 20273.85 ❌
- **TP 2RR**: 20236.39 ❌
- **TP 3RR**: 20198.94 ❌
- **TP 4RR**: 20161.48 ❌
- **TP 15RR**: 19749.45 ❌
- **PnL**: -37.46 points (-1.0R)
- **MFE**: 29.07 points
- **MAE**: 37.74 points

### Trade #711 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 10:15:00
- **FVG 5m**: 20311.31 - 20359.25
- **Entrée**: 20389.09 @ 2025-05-06 11:13:00
- **Stop Loss**: 20290.19
- **Risk**: 98.90 points
- **TP 1RR**: 20487.99 ❌
- **TP 2RR**: 20586.89 ❌
- **TP 3RR**: 20685.79 ❌
- **TP 4RR**: 20784.69 ❌
- **TP 15RR**: 21872.58 ❌
- **PnL**: -98.90 points (-1.0R)
- **MFE**: 39.78 points
- **MAE**: 105.58 points

### Trade #712 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 11:00:00
- **FVG 5m**: 20311.31 - 20359.25
- **Entrée**: 20389.09 @ 2025-05-06 11:13:00
- **Stop Loss**: 20272.09
- **Risk**: 117.00 points
- **TP 1RR**: 20506.09 ❌
- **TP 2RR**: 20623.09 ❌
- **TP 3RR**: 20740.08 ❌
- **TP 4RR**: 20857.08 ❌
- **TP 15RR**: 22144.05 ❌
- **PnL**: -117.00 points (-1.0R)
- **MFE**: 39.78 points
- **MAE**: 117.57 points

### Trade #713 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 11:00:00
- **FVG 5m**: 20311.31 - 20359.25
- **Entrée**: 20389.09 @ 2025-05-06 11:13:00
- **Stop Loss**: 20272.09
- **Risk**: 117.00 points
- **TP 1RR**: 20506.09 ❌
- **TP 2RR**: 20623.09 ❌
- **TP 3RR**: 20740.08 ❌
- **TP 4RR**: 20857.08 ❌
- **TP 15RR**: 22144.05 ❌
- **PnL**: -117.00 points (-1.0R)
- **MFE**: 39.78 points
- **MAE**: 117.57 points

### Trade #714 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 11:15:00
- **FVG 5m**: 20307.23 - 20311.82
- **Entrée**: 20300.09 @ 2025-05-06 11:44:00
- **Stop Loss**: 20420.97
- **Risk**: 120.89 points
- **TP 1RR**: 20179.20 ❌
- **TP 2RR**: 20058.31 ❌
- **TP 3RR**: 19937.43 ❌
- **TP 4RR**: 19816.54 ❌
- **TP 15RR**: 18486.79 ❌
- **PnL**: -120.89 points (-1.0R)
- **MFE**: 102.52 points
- **MAE**: 199.18 points

### Trade #715 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 11:15:00
- **FVG 5m**: 20307.23 - 20311.82
- **Entrée**: 20300.09 @ 2025-05-06 11:44:00
- **Stop Loss**: 20420.97
- **Risk**: 120.89 points
- **TP 1RR**: 20179.20 ❌
- **TP 2RR**: 20058.31 ❌
- **TP 3RR**: 19937.43 ❌
- **TP 4RR**: 19816.54 ❌
- **TP 15RR**: 18486.79 ❌
- **PnL**: -120.89 points (-1.0R)
- **MFE**: 102.52 points
- **MAE**: 199.18 points

### Trade #716 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 15:30:00
- **FVG 5m**: 20255.71 - 20452.85
- **Entrée**: 20468.92 @ 2025-05-06 17:01:00
- **Stop Loss**: 20205.06
- **Risk**: 263.86 points
- **TP 1RR**: 20732.77 ❌
- **TP 2RR**: 20996.63 ❌
- **TP 3RR**: 21260.49 ❌
- **TP 4RR**: 21524.35 ❌
- **TP 15RR**: 24426.80 ❌
- **PnL**: -263.86 points (-1.0R)
- **MFE**: 69.62 points
- **MAE**: 270.84 points

### Trade #717 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-06 19:00:00
- **FVG 5m**: 20478.10 - 20484.73
- **Entrée**: 20474.27 @ 2025-05-06 20:13:00
- **Stop Loss**: 20486.80
- **Risk**: 12.53 points
- **TP 1RR**: 20461.74 ✅
- **TP 2RR**: 20449.20 ✅
- **TP 3RR**: 20436.67 ✅
- **TP 4RR**: 20424.14 ✅
- **TP 15RR**: 20286.27 ✅
- **PnL**: 188.00 points (15.0R)
- **MFE**: 191.01 points
- **MAE**: 3.83 points

### Trade #718 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-06 22:00:00
- **FVG 5m**: 20403.63 - 20409.49
- **Entrée**: 20412.04 @ 2025-05-06 22:33:00
- **Stop Loss**: 20385.78
- **Risk**: 26.26 points
- **TP 1RR**: 20438.31 ✅
- **TP 2RR**: 20464.57 ❌
- **TP 3RR**: 20490.84 ❌
- **TP 4RR**: 20517.10 ❌
- **TP 15RR**: 20806.01 ❌
- **PnL**: -26.26 points (-1.0R)
- **MFE**: 26.27 points
- **MAE**: 26.78 points

### Trade #719 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 01:45:00
- **FVG 5m**: 20396.49 - 20400.31
- **Entrée**: 20405.41 @ 2025-05-07 02:20:00
- **Stop Loss**: 20357.23
- **Risk**: 48.18 points
- **TP 1RR**: 20453.60 ❌
- **TP 2RR**: 20501.78 ❌
- **TP 3RR**: 20549.96 ❌
- **TP 4RR**: 20598.14 ❌
- **TP 15RR**: 21128.15 ❌
- **PnL**: -48.18 points (-1.0R)
- **MFE**: 27.54 points
- **MAE**: 68.35 points

### Trade #720 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 10:00:00
- **FVG 5m**: 20228.94 - 20237.35
- **Entrée**: 20240.16 @ 2025-05-07 11:39:00
- **Stop Loss**: 20176.76
- **Risk**: 63.39 points
- **TP 1RR**: 20303.55 ✅
- **TP 2RR**: 20366.94 ❌
- **TP 3RR**: 20430.34 ❌
- **TP 4RR**: 20493.73 ❌
- **TP 15RR**: 21191.07 ❌
- **PnL**: -63.39 points (-1.0R)
- **MFE**: 86.20 points
- **MAE**: 112.98 points

### Trade #721 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 13:15:00
- **FVG 5m**: 20186.35 - 20190.17
- **Entrée**: 20191.96 @ 2025-05-07 13:31:00
- **Stop Loss**: 20064.35
- **Risk**: 127.60 points
- **TP 1RR**: 20319.56 ✅
- **TP 2RR**: 20447.17 ✅
- **TP 3RR**: 20574.77 ✅
- **TP 4RR**: 20702.37 ✅
- **TP 15RR**: 22106.02 ✅
- **PnL**: 1914.06 points (15.0R)
- **MFE**: 1938.20 points
- **MAE**: 50.50 points

### Trade #722 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-07 13:30:00
- **FVG 5m**: 20194.25 - 20243.47
- **Entrée**: 20260.05 @ 2025-05-07 13:56:00
- **Stop Loss**: 20135.47
- **Risk**: 124.58 points
- **TP 1RR**: 20384.63 ✅
- **TP 2RR**: 20509.21 ✅
- **TP 3RR**: 20633.79 ✅
- **TP 4RR**: 20758.37 ✅
- **TP 15RR**: 22128.74 ✅
- **PnL**: 1868.69 points (15.0R)
- **MFE**: 1870.11 points
- **MAE**: 98.70 points

### Trade #723 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:30:00
- **FVG 5m**: 20338.60 - 20358.74
- **Entrée**: 20332.22 @ 2025-05-07 17:00:00
- **Stop Loss**: 20466.90
- **Risk**: 134.68 points
- **TP 1RR**: 20197.54 ❌
- **TP 2RR**: 20062.86 ❌
- **TP 3RR**: 19928.18 ❌
- **TP 4RR**: 19793.50 ❌
- **TP 15RR**: 18312.00 ❌
- **PnL**: -134.68 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 140.52 points

### Trade #724 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:30:00
- **FVG 5m**: 20338.60 - 20358.74
- **Entrée**: 20332.22 @ 2025-05-07 17:00:00
- **Stop Loss**: 20466.90
- **Risk**: 134.68 points
- **TP 1RR**: 20197.54 ❌
- **TP 2RR**: 20062.86 ❌
- **TP 3RR**: 19928.18 ❌
- **TP 4RR**: 19793.50 ❌
- **TP 15RR**: 18312.00 ❌
- **PnL**: -134.68 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 140.52 points

### Trade #725 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:30:00
- **FVG 5m**: 20338.60 - 20358.74
- **Entrée**: 20332.22 @ 2025-05-07 17:00:00
- **Stop Loss**: 20466.90
- **Risk**: 134.68 points
- **TP 1RR**: 20197.54 ❌
- **TP 2RR**: 20062.86 ❌
- **TP 3RR**: 19928.18 ❌
- **TP 4RR**: 19793.50 ❌
- **TP 15RR**: 18312.00 ❌
- **PnL**: -134.68 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 140.52 points

### Trade #726 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-07 14:45:00
- **FVG 5m**: 20338.60 - 20358.74
- **Entrée**: 20332.22 @ 2025-05-07 17:00:00
- **Stop Loss**: 20444.19
- **Risk**: 111.97 points
- **TP 1RR**: 20220.25 ❌
- **TP 2RR**: 20108.28 ❌
- **TP 3RR**: 19996.30 ❌
- **TP 4RR**: 19884.33 ❌
- **TP 15RR**: 18652.63 ❌
- **PnL**: -111.97 points (-1.0R)
- **MFE**: 21.17 points
- **MAE**: 122.67 points

### Trade #727 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 06:30:00
- **FVG 5m**: 20604.59 - 20611.22
- **Entrée**: 20603.06 @ 2025-05-08 06:43:00
- **Stop Loss**: 20646.28
- **Risk**: 43.22 points
- **TP 1RR**: 20559.84 ✅
- **TP 2RR**: 20516.63 ✅
- **TP 3RR**: 20473.41 ✅
- **TP 4RR**: 20430.19 ✅
- **TP 15RR**: 19954.81 ❌
- **PnL**: -43.22 points (-1.0R)
- **MFE**: 222.38 points
- **MAE**: 49.99 points

### Trade #728 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 07:30:00
- **FVG 5m**: 20543.13 - 20563.27
- **Entrée**: 20531.40 @ 2025-05-08 08:32:00
- **Stop Loss**: 20643.47
- **Risk**: 112.07 points
- **TP 1RR**: 20419.32 ✅
- **TP 2RR**: 20307.25 ❌
- **TP 3RR**: 20195.18 ❌
- **TP 4RR**: 20083.11 ❌
- **TP 15RR**: 18850.32 ❌
- **PnL**: -112.07 points (-1.0R)
- **MFE**: 150.72 points
- **MAE**: 121.65 points

### Trade #729 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 08:30:00
- **FVG 5m**: 20499.01 - 20503.09
- **Entrée**: 20483.20 @ 2025-05-08 08:48:00
- **Stop Loss**: 20589.89
- **Risk**: 106.69 points
- **TP 1RR**: 20376.51 ❌
- **TP 2RR**: 20269.82 ❌
- **TP 3RR**: 20163.13 ❌
- **TP 4RR**: 20056.44 ❌
- **TP 15RR**: 18882.85 ❌
- **PnL**: -106.69 points (-1.0R)
- **MFE**: 102.52 points
- **MAE**: 119.10 points

### Trade #730 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 08:30:00
- **FVG 5m**: 20499.01 - 20503.09
- **Entrée**: 20483.20 @ 2025-05-08 08:48:00
- **Stop Loss**: 20589.89
- **Risk**: 106.69 points
- **TP 1RR**: 20376.51 ❌
- **TP 2RR**: 20269.82 ❌
- **TP 3RR**: 20163.13 ❌
- **TP 4RR**: 20056.44 ❌
- **TP 15RR**: 18882.85 ❌
- **PnL**: -106.69 points (-1.0R)
- **MFE**: 102.52 points
- **MAE**: 119.10 points

### Trade #731 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-08 10:15:00
- **FVG 5m**: 20605.10 - 20623.21
- **Entrée**: 20623.72 @ 2025-05-08 10:39:00
- **Stop Loss**: 20472.45
- **Risk**: 151.27 points
- **TP 1RR**: 20774.99 ❌
- **TP 2RR**: 20926.26 ❌
- **TP 3RR**: 21077.53 ❌
- **TP 4RR**: 21228.80 ❌
- **TP 15RR**: 22892.78 ❌
- **PnL**: -151.27 points (-1.0R)
- **MFE**: 122.41 points
- **MAE**: 160.16 points

### Trade #732 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 10:45:00
- **FVG 5m**: 20730.57 - 20734.65
- **Entrée**: 20719.10 @ 2025-05-08 12:02:00
- **Stop Loss**: 20735.32
- **Risk**: 16.23 points
- **TP 1RR**: 20702.87 ✅
- **TP 2RR**: 20686.64 ✅
- **TP 3RR**: 20670.41 ✅
- **TP 4RR**: 20654.18 ✅
- **TP 15RR**: 20475.67 ❌
- **PnL**: -16.23 points (-1.0R)
- **MFE**: 78.04 points
- **MAE**: 19.64 points

### Trade #733 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-08 12:45:00
- **FVG 5m**: 20668.60 - 20673.45
- **Entrée**: 20665.03 @ 2025-05-08 12:57:00
- **Stop Loss**: 20711.59
- **Risk**: 46.56 points
- **TP 1RR**: 20618.47 ❌
- **TP 2RR**: 20571.90 ❌
- **TP 3RR**: 20525.34 ❌
- **TP 4RR**: 20478.77 ❌
- **TP 15RR**: 19966.57 ❌
- **PnL**: -46.56 points (-1.0R)
- **MFE**: 23.97 points
- **MAE**: 46.92 points

### Trade #734 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-08 20:15:00
- **FVG 5m**: 20563.02 - 20568.63
- **Entrée**: 20569.14 @ 2025-05-08 21:11:00
- **Stop Loss**: 20520.88
- **Risk**: 48.26 points
- **TP 1RR**: 20617.40 ✅
- **TP 2RR**: 20665.67 ✅
- **TP 3RR**: 20713.93 ❌
- **TP 4RR**: 20762.20 ❌
- **TP 15RR**: 21293.11 ❌
- **PnL**: -48.26 points (-1.0R)
- **MFE**: 127.51 points
- **MAE**: 53.05 points

### Trade #735 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-09 02:45:00
- **FVG 5m**: 20608.16 - 20613.00
- **Entrée**: 20607.90 @ 2025-05-09 02:56:00
- **Stop Loss**: 20649.34
- **Risk**: 41.43 points
- **TP 1RR**: 20566.47 ❌
- **TP 2RR**: 20525.04 ❌
- **TP 3RR**: 20483.61 ❌
- **TP 4RR**: 20442.17 ❌
- **TP 15RR**: 19986.41 ❌
- **PnL**: -41.43 points (-1.0R)
- **MFE**: 37.49 points
- **MAE**: 42.84 points

### Trade #736 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-09 02:45:00
- **FVG 5m**: 20608.16 - 20613.00
- **Entrée**: 20607.90 @ 2025-05-09 02:56:00
- **Stop Loss**: 20649.34
- **Risk**: 41.43 points
- **TP 1RR**: 20566.47 ❌
- **TP 2RR**: 20525.04 ❌
- **TP 3RR**: 20483.61 ❌
- **TP 4RR**: 20442.17 ❌
- **TP 15RR**: 19986.41 ❌
- **PnL**: -41.43 points (-1.0R)
- **MFE**: 37.49 points
- **MAE**: 42.84 points

### Trade #737 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 06:00:00
- **FVG 5m**: 20643.35 - 20648.20
- **Entrée**: 20650.24 @ 2025-05-09 06:13:00
- **Stop Loss**: 20613.66
- **Risk**: 36.58 points
- **TP 1RR**: 20686.82 ❌
- **TP 2RR**: 20723.40 ❌
- **TP 3RR**: 20759.98 ❌
- **TP 4RR**: 20796.56 ❌
- **TP 15RR**: 21198.93 ❌
- **PnL**: -36.58 points (-1.0R)
- **MFE**: 46.41 points
- **MAE**: 92.83 points

### Trade #738 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-09 06:15:00
- **FVG 5m**: 20619.89 - 20643.61
- **Entrée**: 20568.89 @ 2025-05-09 06:26:00
- **Stop Loss**: 20707.00
- **Risk**: 138.12 points
- **TP 1RR**: 20430.77 ❌
- **TP 2RR**: 20292.65 ❌
- **TP 3RR**: 20154.54 ❌
- **TP 4RR**: 20016.42 ❌
- **TP 15RR**: 18497.14 ❌
- **PnL**: -138.12 points (-1.0R)
- **MFE**: 107.62 points
- **MAE**: 317.51 points

### Trade #739 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 06:15:00
- **FVG 5m**: 20596.43 - 20602.04
- **Entrée**: 20602.80 @ 2025-05-09 06:44:00
- **Stop Loss**: 20534.64
- **Risk**: 68.16 points
- **TP 1RR**: 20670.97 ✅
- **TP 2RR**: 20739.13 ❌
- **TP 3RR**: 20807.29 ❌
- **TP 4RR**: 20875.46 ❌
- **TP 15RR**: 21625.26 ❌
- **PnL**: -68.16 points (-1.0R)
- **MFE**: 84.67 points
- **MAE**: 78.04 points

### Trade #740 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 06:15:00
- **FVG 5m**: 20596.43 - 20602.04
- **Entrée**: 20602.80 @ 2025-05-09 06:44:00
- **Stop Loss**: 20534.64
- **Risk**: 68.16 points
- **TP 1RR**: 20670.97 ✅
- **TP 2RR**: 20739.13 ❌
- **TP 3RR**: 20807.29 ❌
- **TP 4RR**: 20875.46 ❌
- **TP 15RR**: 21625.26 ❌
- **PnL**: -68.16 points (-1.0R)
- **MFE**: 84.67 points
- **MAE**: 78.04 points

### Trade #741 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 06:15:00
- **FVG 5m**: 20596.43 - 20602.04
- **Entrée**: 20602.80 @ 2025-05-09 06:44:00
- **Stop Loss**: 20534.64
- **Risk**: 68.16 points
- **TP 1RR**: 20670.97 ✅
- **TP 2RR**: 20739.13 ❌
- **TP 3RR**: 20807.29 ❌
- **TP 4RR**: 20875.46 ❌
- **TP 15RR**: 21625.26 ❌
- **PnL**: -68.16 points (-1.0R)
- **MFE**: 84.67 points
- **MAE**: 78.04 points

### Trade #742 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 09:15:00
- **FVG 5m**: 20551.80 - 20563.27
- **Entrée**: 20568.63 @ 2025-05-09 10:04:00
- **Stop Loss**: 20505.84
- **Risk**: 62.79 points
- **TP 1RR**: 20631.42 ❌
- **TP 2RR**: 20694.22 ❌
- **TP 3RR**: 20757.01 ❌
- **TP 4RR**: 20819.80 ❌
- **TP 15RR**: 21510.53 ❌
- **PnL**: -62.79 points (-1.0R)
- **MFE**: 13.26 points
- **MAE**: 68.35 points

### Trade #743 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 09:30:00
- **FVG 5m**: 20551.80 - 20563.27
- **Entrée**: 20568.63 @ 2025-05-09 10:04:00
- **Stop Loss**: 20451.03
- **Risk**: 117.60 points
- **TP 1RR**: 20686.23 ✅
- **TP 2RR**: 20803.82 ✅
- **TP 3RR**: 20921.42 ✅
- **TP 4RR**: 21039.02 ✅
- **TP 15RR**: 22332.58 ✅
- **PnL**: 1763.95 points (15.0R)
- **MFE**: 1769.63 points
- **MAE**: 103.80 points

### Trade #744 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-09 09:45:00
- **FVG 5m**: 20551.80 - 20563.27
- **Entrée**: 20568.63 @ 2025-05-09 10:04:00
- **Stop Loss**: 20486.97
- **Risk**: 81.66 points
- **TP 1RR**: 20650.29 ❌
- **TP 2RR**: 20731.94 ❌
- **TP 3RR**: 20813.60 ❌
- **TP 4RR**: 20895.25 ❌
- **TP 15RR**: 21793.47 ❌
- **PnL**: -81.66 points (-1.0R)
- **MFE**: 13.26 points
- **MAE**: 88.75 points

### Trade #745 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-11 17:30:00
- **FVG 5m**: 20827.74 - 20830.54
- **Entrée**: 20843.04 @ 2025-05-11 18:03:00
- **Stop Loss**: 20776.03
- **Risk**: 67.01 points
- **TP 1RR**: 20910.05 ✅
- **TP 2RR**: 20977.06 ✅
- **TP 3RR**: 21044.07 ✅
- **TP 4RR**: 21111.07 ✅
- **TP 15RR**: 21848.17 ✅
- **PnL**: 1005.14 points (15.0R)
- **MFE**: 1007.10 points
- **MAE**: 12.50 points

### Trade #746 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-11 18:15:00
- **FVG 5m**: 20865.99 - 20885.37
- **Entrée**: 20864.72 @ 2025-05-11 18:53:00
- **Stop Loss**: 20925.92
- **Risk**: 61.21 points
- **TP 1RR**: 20803.51 ❌
- **TP 2RR**: 20742.30 ❌
- **TP 3RR**: 20681.09 ❌
- **TP 4RR**: 20619.88 ❌
- **TP 15RR**: 19946.60 ❌
- **PnL**: -61.21 points (-1.0R)
- **MFE**: 12.75 points
- **MAE**: 68.86 points

### Trade #747 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-11 20:30:00
- **FVG 5m**: 20933.83 - 20938.42
- **Entrée**: 20931.79 @ 2025-05-11 22:29:00
- **Stop Loss**: 20967.77
- **Risk**: 35.98 points
- **TP 1RR**: 20895.81 ❌
- **TP 2RR**: 20859.83 ❌
- **TP 3RR**: 20823.84 ❌
- **TP 4RR**: 20787.86 ❌
- **TP 15RR**: 20392.07 ❌
- **PnL**: -35.98 points (-1.0R)
- **MFE**: 7.65 points
- **MAE**: 36.98 points

### Trade #748 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 02:00:00
- **FVG 5m**: 21296.48 - 21311.27
- **Entrée**: 21312.03 @ 2025-05-12 02:23:00
- **Stop Loss**: 20966.18
- **Risk**: 345.85 points
- **TP 1RR**: 21657.88 ✅
- **TP 2RR**: 22003.73 ✅
- **TP 3RR**: 22349.58 ✅
- **TP 4RR**: 22695.42 ✅
- **TP 15RR**: 26499.75 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 5086.97 points
- **MAE**: 206.06 points

### Trade #749 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 02:00:00
- **FVG 5m**: 21296.48 - 21311.27
- **Entrée**: 21312.03 @ 2025-05-12 02:23:00
- **Stop Loss**: 20966.18
- **Risk**: 345.85 points
- **TP 1RR**: 21657.88 ✅
- **TP 2RR**: 22003.73 ✅
- **TP 3RR**: 22349.58 ✅
- **TP 4RR**: 22695.42 ✅
- **TP 15RR**: 26499.75 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 5086.97 points
- **MAE**: 206.06 points

### Trade #750 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 02:00:00
- **FVG 5m**: 21296.48 - 21311.27
- **Entrée**: 21312.03 @ 2025-05-12 02:23:00
- **Stop Loss**: 20966.18
- **Risk**: 345.85 points
- **TP 1RR**: 21657.88 ✅
- **TP 2RR**: 22003.73 ✅
- **TP 3RR**: 22349.58 ✅
- **TP 4RR**: 22695.42 ✅
- **TP 15RR**: 26499.75 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 5086.97 points
- **MAE**: 206.06 points

### Trade #751 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 02:30:00
- **FVG 5m**: 21232.97 - 21239.86
- **Entrée**: 21217.42 @ 2025-05-12 02:54:00
- **Stop Loss**: 21351.01
- **Risk**: 133.59 points
- **TP 1RR**: 21083.82 ❌
- **TP 2RR**: 20950.23 ❌
- **TP 3RR**: 20816.64 ❌
- **TP 4RR**: 20683.05 ❌
- **TP 15RR**: 19213.52 ❌
- **PnL**: -133.59 points (-1.0R)
- **MFE**: 20.91 points
- **MAE**: 136.18 points

### Trade #752 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 02:30:00
- **FVG 5m**: 21232.97 - 21239.86
- **Entrée**: 21217.42 @ 2025-05-12 02:54:00
- **Stop Loss**: 21351.01
- **Risk**: 133.59 points
- **TP 1RR**: 21083.82 ❌
- **TP 2RR**: 20950.23 ❌
- **TP 3RR**: 20816.64 ❌
- **TP 4RR**: 20683.05 ❌
- **TP 15RR**: 19213.52 ❌
- **PnL**: -133.59 points (-1.0R)
- **MFE**: 20.91 points
- **MAE**: 136.18 points

### Trade #753 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 05:30:00
- **FVG 5m**: 21353.60 - 21357.17
- **Entrée**: 21350.80 @ 2025-05-12 05:43:00
- **Stop Loss**: 21401.53
- **Risk**: 50.73 points
- **TP 1RR**: 21300.06 ❌
- **TP 2RR**: 21249.33 ❌
- **TP 3RR**: 21198.59 ❌
- **TP 4RR**: 21147.86 ❌
- **TP 15RR**: 20589.78 ❌
- **PnL**: -50.73 points (-1.0R)
- **MFE**: 13.52 points
- **MAE**: 54.07 points

### Trade #754 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 05:30:00
- **FVG 5m**: 21353.60 - 21357.17
- **Entrée**: 21350.80 @ 2025-05-12 05:43:00
- **Stop Loss**: 21401.53
- **Risk**: 50.73 points
- **TP 1RR**: 21300.06 ❌
- **TP 2RR**: 21249.33 ❌
- **TP 3RR**: 21198.59 ❌
- **TP 4RR**: 21147.86 ❌
- **TP 15RR**: 20589.78 ❌
- **PnL**: -50.73 points (-1.0R)
- **MFE**: 13.52 points
- **MAE**: 54.07 points

### Trade #755 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 05:30:00
- **FVG 5m**: 21353.60 - 21357.17
- **Entrée**: 21350.80 @ 2025-05-12 05:43:00
- **Stop Loss**: 21401.53
- **Risk**: 50.73 points
- **TP 1RR**: 21300.06 ❌
- **TP 2RR**: 21249.33 ❌
- **TP 3RR**: 21198.59 ❌
- **TP 4RR**: 21147.86 ❌
- **TP 15RR**: 20589.78 ❌
- **PnL**: -50.73 points (-1.0R)
- **MFE**: 13.52 points
- **MAE**: 54.07 points

### Trade #756 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-12 12:00:00
- **FVG 5m**: 21336.26 - 21340.34
- **Entrée**: 21344.68 @ 2025-05-12 13:18:00
- **Stop Loss**: 21281.24
- **Risk**: 63.44 points
- **TP 1RR**: 21408.11 ❌
- **TP 2RR**: 21471.55 ❌
- **TP 3RR**: 21534.98 ❌
- **TP 4RR**: 21598.42 ❌
- **TP 15RR**: 22296.22 ❌
- **PnL**: -63.44 points (-1.0R)
- **MFE**: 19.89 points
- **MAE**: 66.31 points

### Trade #757 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-12 17:00:00
- **FVG 5m**: 21344.68 - 21353.60
- **Entrée**: 21341.36 @ 2025-05-12 17:31:00
- **Stop Loss**: 21395.66
- **Risk**: 54.30 points
- **TP 1RR**: 21287.06 ✅
- **TP 2RR**: 21232.76 ❌
- **TP 3RR**: 21178.45 ❌
- **TP 4RR**: 21124.15 ❌
- **TP 15RR**: 20526.83 ❌
- **PnL**: -54.30 points (-1.0R)
- **MFE**: 104.82 points
- **MAE**: 58.40 points

### Trade #758 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-13 07:30:00
- **FVG 5m**: 21429.09 - 21431.89
- **Entrée**: 21418.63 @ 2025-05-13 07:41:00
- **Stop Loss**: 21500.02
- **Risk**: 81.39 points
- **TP 1RR**: 21337.25 ❌
- **TP 2RR**: 21255.86 ❌
- **TP 3RR**: 21174.47 ❌
- **TP 4RR**: 21093.09 ❌
- **TP 15RR**: 20197.83 ❌
- **PnL**: -81.39 points (-1.0R)
- **MFE**: 24.23 points
- **MAE**: 81.61 points

### Trade #759 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-13 07:30:00
- **FVG 5m**: 21429.09 - 21431.89
- **Entrée**: 21418.63 @ 2025-05-13 07:41:00
- **Stop Loss**: 21500.02
- **Risk**: 81.39 points
- **TP 1RR**: 21337.25 ❌
- **TP 2RR**: 21255.86 ❌
- **TP 3RR**: 21174.47 ❌
- **TP 4RR**: 21093.09 ❌
- **TP 15RR**: 20197.83 ❌
- **PnL**: -81.39 points (-1.0R)
- **MFE**: 24.23 points
- **MAE**: 81.61 points

### Trade #760 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-13 18:00:00
- **FVG 5m**: 21704.01 - 21715.74
- **Entrée**: 21719.05 @ 2025-05-13 18:37:00
- **Stop Loss**: 21668.68
- **Risk**: 50.37 points
- **TP 1RR**: 21769.42 ✅
- **TP 2RR**: 21819.79 ❌
- **TP 3RR**: 21870.16 ❌
- **TP 4RR**: 21920.53 ❌
- **TP 15RR**: 22474.59 ❌
- **PnL**: -50.37 points (-1.0R)
- **MFE**: 66.05 points
- **MAE**: 53.81 points

### Trade #761 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 02:15:00
- **FVG 5m**: 21722.37 - 21730.02
- **Entrée**: 21719.82 @ 2025-05-14 03:02:00
- **Stop Loss**: 21790.13
- **Risk**: 70.31 points
- **TP 1RR**: 21649.51 ❌
- **TP 2RR**: 21579.20 ❌
- **TP 3RR**: 21508.89 ❌
- **TP 4RR**: 21438.58 ❌
- **TP 15RR**: 20665.16 ❌
- **PnL**: -70.31 points (-1.0R)
- **MFE**: 54.58 points
- **MAE**: 75.23 points

### Trade #762 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 06:30:00
- **FVG 5m**: 21783.07 - 21788.17
- **Entrée**: 21782.30 @ 2025-05-14 06:44:00
- **Stop Loss**: 21823.30
- **Risk**: 41.00 points
- **TP 1RR**: 21741.30 ✅
- **TP 2RR**: 21700.30 ❌
- **TP 3RR**: 21659.30 ❌
- **TP 4RR**: 21618.30 ❌
- **TP 15RR**: 21167.31 ❌
- **PnL**: -41.00 points (-1.0R)
- **MFE**: 42.08 points
- **MAE**: 43.35 points

### Trade #763 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 06:45:00
- **FVG 5m**: 21772.10 - 21777.96
- **Entrée**: 21771.08 @ 2025-05-14 07:37:00
- **Stop Loss**: 21798.29
- **Risk**: 27.22 points
- **TP 1RR**: 21743.86 ✅
- **TP 2RR**: 21716.65 ❌
- **TP 3RR**: 21689.43 ❌
- **TP 4RR**: 21662.22 ❌
- **TP 15RR**: 21362.85 ❌
- **PnL**: -27.22 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 31.88 points

### Trade #764 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 06:45:00
- **FVG 5m**: 21772.10 - 21777.96
- **Entrée**: 21771.08 @ 2025-05-14 07:37:00
- **Stop Loss**: 21798.29
- **Risk**: 27.22 points
- **TP 1RR**: 21743.86 ✅
- **TP 2RR**: 21716.65 ❌
- **TP 3RR**: 21689.43 ❌
- **TP 4RR**: 21662.22 ❌
- **TP 15RR**: 21362.85 ❌
- **PnL**: -27.22 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 31.88 points

### Trade #765 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 07:30:00
- **FVG 5m**: 21759.60 - 21765.21
- **Entrée**: 21753.99 @ 2025-05-14 07:41:00
- **Stop Loss**: 21807.74
- **Risk**: 53.74 points
- **TP 1RR**: 21700.25 ❌
- **TP 2RR**: 21646.51 ❌
- **TP 3RR**: 21592.76 ❌
- **TP 4RR**: 21539.02 ❌
- **TP 15RR**: 20947.85 ❌
- **PnL**: -53.74 points (-1.0R)
- **MFE**: 13.77 points
- **MAE**: 71.66 points

### Trade #766 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 07:30:00
- **FVG 5m**: 21759.60 - 21765.21
- **Entrée**: 21753.99 @ 2025-05-14 07:41:00
- **Stop Loss**: 21807.74
- **Risk**: 53.74 points
- **TP 1RR**: 21700.25 ❌
- **TP 2RR**: 21646.51 ❌
- **TP 3RR**: 21592.76 ❌
- **TP 4RR**: 21539.02 ❌
- **TP 15RR**: 20947.85 ❌
- **PnL**: -53.74 points (-1.0R)
- **MFE**: 13.77 points
- **MAE**: 71.66 points

### Trade #767 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 08:30:00
- **FVG 5m**: 21774.65 - 21797.35
- **Entrée**: 21770.57 @ 2025-05-14 08:44:00
- **Stop Loss**: 21846.52
- **Risk**: 75.95 points
- **TP 1RR**: 21694.62 ❌
- **TP 2RR**: 21618.67 ❌
- **TP 3RR**: 21542.72 ❌
- **TP 4RR**: 21466.77 ❌
- **TP 15RR**: 20631.33 ❌
- **PnL**: -75.95 points (-1.0R)
- **MFE**: 69.11 points
- **MAE**: 79.57 points

### Trade #768 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-14 10:15:00
- **FVG 5m**: 21810.86 - 21813.92
- **Entrée**: 21814.94 @ 2025-05-14 11:29:00
- **Stop Loss**: 21752.80
- **Risk**: 62.14 points
- **TP 1RR**: 21877.09 ❌
- **TP 2RR**: 21939.23 ❌
- **TP 3RR**: 22001.37 ❌
- **TP 4RR**: 22063.51 ❌
- **TP 15RR**: 22747.08 ❌
- **PnL**: -62.14 points (-1.0R)
- **MFE**: 35.19 points
- **MAE**: 64.78 points

### Trade #769 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-14 22:00:00
- **FVG 5m**: 21823.10 - 21828.20
- **Entrée**: 21821.32 @ 2025-05-14 22:29:00
- **Stop Loss**: 21851.11
- **Risk**: 29.79 points
- **TP 1RR**: 21791.53 ✅
- **TP 2RR**: 21761.74 ✅
- **TP 3RR**: 21731.94 ✅
- **TP 4RR**: 21702.15 ✅
- **TP 15RR**: 21374.44 ❌
- **PnL**: -29.79 points (-1.0R)
- **MFE**: 203.26 points
- **MAE**: 34.17 points

### Trade #770 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 00:45:00
- **FVG 5m**: 21767.51 - 21775.67
- **Entrée**: 21777.71 @ 2025-05-15 01:13:00
- **Stop Loss**: 21734.96
- **Risk**: 42.75 points
- **TP 1RR**: 21820.46 ❌
- **TP 2RR**: 21863.21 ❌
- **TP 3RR**: 21905.96 ❌
- **TP 4RR**: 21948.71 ❌
- **TP 15RR**: 22418.98 ❌
- **PnL**: -42.75 points (-1.0R)
- **MFE**: 22.44 points
- **MAE**: 46.16 points

### Trade #771 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 04:15:00
- **FVG 5m**: 21656.32 - 21664.73
- **Entrée**: 21669.58 @ 2025-05-15 04:28:00
- **Stop Loss**: 21614.14
- **Risk**: 55.44 points
- **TP 1RR**: 21725.02 ✅
- **TP 2RR**: 21780.46 ✅
- **TP 3RR**: 21835.90 ✅
- **TP 4RR**: 21891.35 ✅
- **TP 15RR**: 22501.21 ❌
- **PnL**: -55.44 points (-1.0R)
- **MFE**: 293.03 points
- **MAE**: 57.38 points

### Trade #772 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 04:45:00
- **FVG 5m**: 21683.86 - 21692.79
- **Entrée**: 21696.10 @ 2025-05-15 06:01:00
- **Stop Loss**: 21652.12
- **Risk**: 43.98 points
- **TP 1RR**: 21740.09 ✅
- **TP 2RR**: 21784.07 ✅
- **TP 3RR**: 21828.06 ✅
- **TP 4RR**: 21872.04 ✅
- **TP 15RR**: 22355.87 ❌
- **PnL**: -43.98 points (-1.0R)
- **MFE**: 266.50 points
- **MAE**: 45.14 points

### Trade #773 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 04:45:00
- **FVG 5m**: 21683.86 - 21692.79
- **Entrée**: 21696.10 @ 2025-05-15 06:01:00
- **Stop Loss**: 21652.12
- **Risk**: 43.98 points
- **TP 1RR**: 21740.09 ✅
- **TP 2RR**: 21784.07 ✅
- **TP 3RR**: 21828.06 ✅
- **TP 4RR**: 21872.04 ✅
- **TP 15RR**: 22355.87 ❌
- **PnL**: -43.98 points (-1.0R)
- **MFE**: 266.50 points
- **MAE**: 45.14 points

### Trade #774 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 06:00:00
- **FVG 5m**: 21707.07 - 21713.70
- **Entrée**: 21714.97 @ 2025-05-15 06:26:00
- **Stop Loss**: 21664.10
- **Risk**: 50.88 points
- **TP 1RR**: 21765.85 ❌
- **TP 2RR**: 21816.73 ❌
- **TP 3RR**: 21867.60 ❌
- **TP 4RR**: 21918.48 ❌
- **TP 15RR**: 22478.12 ❌
- **PnL**: -50.88 points (-1.0R)
- **MFE**: 14.54 points
- **MAE**: 51.77 points

### Trade #775 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-15 10:00:00
- **FVG 5m**: 21809.84 - 21818.26
- **Entrée**: 21820.55 @ 2025-05-15 10:17:00
- **Stop Loss**: 21745.41
- **Risk**: 75.14 points
- **TP 1RR**: 21895.70 ✅
- **TP 2RR**: 21970.84 ❌
- **TP 3RR**: 22045.99 ❌
- **TP 4RR**: 22121.13 ❌
- **TP 15RR**: 22947.73 ❌
- **PnL**: -75.14 points (-1.0R)
- **MFE**: 142.05 points
- **MAE**: 88.49 points

### Trade #776 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-15 15:00:00
- **FVG 5m**: 21826.42 - 21830.50
- **Entrée**: 21814.69 @ 2025-05-15 17:00:00
- **Stop Loss**: 21887.34
- **Risk**: 72.65 points
- **TP 1RR**: 21742.03 ❌
- **TP 2RR**: 21669.38 ❌
- **TP 3RR**: 21596.72 ❌
- **TP 4RR**: 21524.07 ❌
- **TP 15RR**: 20724.87 ❌
- **PnL**: -72.65 points (-1.0R)
- **MFE**: 36.72 points
- **MAE**: 72.68 points

### Trade #777 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 02:00:00
- **FVG 5m**: 21815.71 - 21821.57
- **Entrée**: 21824.12 @ 2025-05-16 02:12:00
- **Stop Loss**: 21780.59
- **Risk**: 43.54 points
- **TP 1RR**: 21867.66 ✅
- **TP 2RR**: 21911.20 ✅
- **TP 3RR**: 21954.74 ❌
- **TP 4RR**: 21998.28 ❌
- **TP 15RR**: 22477.21 ❌
- **PnL**: -43.54 points (-1.0R)
- **MFE**: 112.98 points
- **MAE**: 48.71 points

### Trade #778 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 02:45:00
- **FVG 5m**: 21884.06 - 21888.65
- **Entrée**: 21882.02 @ 2025-05-16 04:33:00
- **Stop Loss**: 21898.31
- **Risk**: 16.30 points
- **TP 1RR**: 21865.72 ✅
- **TP 2RR**: 21849.42 ❌
- **TP 3RR**: 21833.12 ❌
- **TP 4RR**: 21816.82 ❌
- **TP 15RR**: 21637.53 ❌
- **PnL**: -16.30 points (-1.0R)
- **MFE**: 20.66 points
- **MAE**: 18.11 points

### Trade #779 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 06:15:00
- **FVG 5m**: 21878.19 - 21885.33
- **Entrée**: 21887.12 @ 2025-05-16 08:06:00
- **Stop Loss**: 21876.68
- **Risk**: 10.43 points
- **TP 1RR**: 21897.55 ✅
- **TP 2RR**: 21907.98 ✅
- **TP 3RR**: 21918.42 ❌
- **TP 4RR**: 21928.85 ❌
- **TP 15RR**: 22043.62 ❌
- **PnL**: -10.43 points (-1.0R)
- **MFE**: 24.23 points
- **MAE**: 12.24 points

### Trade #780 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 07:30:00
- **FVG 5m**: 21845.04 - 21858.55
- **Entrée**: 21843.25 @ 2025-05-16 09:29:00
- **Stop Loss**: 21941.95
- **Risk**: 98.69 points
- **TP 1RR**: 21744.56 ❌
- **TP 2RR**: 21645.86 ❌
- **TP 3RR**: 21547.17 ❌
- **TP 4RR**: 21448.47 ❌
- **TP 15RR**: 20362.83 ❌
- **PnL**: -98.69 points (-1.0R)
- **MFE**: 94.36 points
- **MAE**: 101.25 points

### Trade #781 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 08:30:00
- **FVG 5m**: 21845.04 - 21858.55
- **Entrée**: 21843.25 @ 2025-05-16 09:29:00
- **Stop Loss**: 21912.60
- **Risk**: 69.35 points
- **TP 1RR**: 21773.90 ✅
- **TP 2RR**: 21704.55 ❌
- **TP 3RR**: 21635.20 ❌
- **TP 4RR**: 21565.84 ❌
- **TP 15RR**: 20802.97 ❌
- **PnL**: -69.35 points (-1.0R)
- **MFE**: 94.36 points
- **MAE**: 73.70 points

### Trade #782 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-16 08:30:00
- **FVG 5m**: 21845.04 - 21858.55
- **Entrée**: 21843.25 @ 2025-05-16 09:29:00
- **Stop Loss**: 21912.60
- **Risk**: 69.35 points
- **TP 1RR**: 21773.90 ✅
- **TP 2RR**: 21704.55 ❌
- **TP 3RR**: 21635.20 ❌
- **TP 4RR**: 21565.84 ❌
- **TP 15RR**: 20802.97 ❌
- **PnL**: -69.35 points (-1.0R)
- **MFE**: 94.36 points
- **MAE**: 73.70 points

### Trade #783 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 09:45:00
- **FVG 5m**: 21830.50 - 21839.43
- **Entrée**: 21846.31 @ 2025-05-16 10:31:00
- **Stop Loss**: 21738.02
- **Risk**: 108.29 points
- **TP 1RR**: 21954.61 ❌
- **TP 2RR**: 22062.90 ❌
- **TP 3RR**: 22171.20 ❌
- **TP 4RR**: 22279.49 ❌
- **TP 15RR**: 23470.73 ❌
- **PnL**: -108.29 points (-1.0R)
- **MFE**: 98.19 points
- **MAE**: 134.65 points

### Trade #784 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-16 09:45:00
- **FVG 5m**: 21830.50 - 21839.43
- **Entrée**: 21846.31 @ 2025-05-16 10:31:00
- **Stop Loss**: 21738.02
- **Risk**: 108.29 points
- **TP 1RR**: 21954.61 ❌
- **TP 2RR**: 22062.90 ❌
- **TP 3RR**: 22171.20 ❌
- **TP 4RR**: 22279.49 ❌
- **TP 15RR**: 23470.73 ❌
- **PnL**: -108.29 points (-1.0R)
- **MFE**: 98.19 points
- **MAE**: 134.65 points

### Trade #785 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-18 17:00:00
- **FVG 5m**: 21763.94 - 21767.76
- **Entrée**: 21769.55 @ 2025-05-18 17:46:00
- **Stop Loss**: 21700.80
- **Risk**: 68.75 points
- **TP 1RR**: 21838.30 ✅
- **TP 2RR**: 21907.04 ❌
- **TP 3RR**: 21975.79 ❌
- **TP 4RR**: 22044.54 ❌
- **TP 15RR**: 22800.75 ❌
- **PnL**: -68.75 points (-1.0R)
- **MFE**: 79.06 points
- **MAE**: 72.68 points

### Trade #786 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-18 19:45:00
- **FVG 5m**: 21707.83 - 21710.64
- **Entrée**: 21714.21 @ 2025-05-18 21:21:00
- **Stop Loss**: 21681.43
- **Risk**: 32.78 points
- **TP 1RR**: 21746.99 ❌
- **TP 2RR**: 21779.76 ❌
- **TP 3RR**: 21812.54 ❌
- **TP 4RR**: 21845.32 ❌
- **TP 15RR**: 22205.88 ❌
- **PnL**: -32.78 points (-1.0R)
- **MFE**: 14.28 points
- **MAE**: 34.43 points

### Trade #787 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 08:30:00
- **FVG 5m**: 21740.48 - 21745.32
- **Entrée**: 21745.58 @ 2025-05-19 08:42:00
- **Stop Loss**: 21617.71
- **Risk**: 127.87 points
- **TP 1RR**: 21873.45 ✅
- **TP 2RR**: 22001.32 ❌
- **TP 3RR**: 22129.19 ❌
- **TP 4RR**: 22257.06 ❌
- **TP 15RR**: 23663.65 ❌
- **PnL**: -127.87 points (-1.0R)
- **MFE**: 250.18 points
- **MAE**: 160.67 points

### Trade #788 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 08:30:00
- **FVG 5m**: 21740.48 - 21745.32
- **Entrée**: 21745.58 @ 2025-05-19 08:42:00
- **Stop Loss**: 21617.71
- **Risk**: 127.87 points
- **TP 1RR**: 21873.45 ✅
- **TP 2RR**: 22001.32 ❌
- **TP 3RR**: 22129.19 ❌
- **TP 4RR**: 22257.06 ❌
- **TP 15RR**: 23663.65 ❌
- **PnL**: -127.87 points (-1.0R)
- **MFE**: 250.18 points
- **MAE**: 160.67 points

### Trade #789 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 09:15:00
- **FVG 5m**: 21844.02 - 21856.77
- **Entrée**: 21835.09 @ 2025-05-19 09:26:00
- **Stop Loss**: 21904.95
- **Risk**: 69.86 points
- **TP 1RR**: 21765.23 ❌
- **TP 2RR**: 21695.37 ❌
- **TP 3RR**: 21625.52 ❌
- **TP 4RR**: 21555.66 ❌
- **TP 15RR**: 20787.22 ❌
- **PnL**: -69.86 points (-1.0R)
- **MFE**: 28.82 points
- **MAE**: 70.13 points

### Trade #790 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 12:15:00
- **FVG 5m**: 21910.58 - 21924.86
- **Entrée**: 21910.32 @ 2025-05-19 13:14:00
- **Stop Loss**: 21987.87
- **Risk**: 77.55 points
- **TP 1RR**: 21832.77 ❌
- **TP 2RR**: 21755.22 ❌
- **TP 3RR**: 21677.67 ❌
- **TP 4RR**: 21600.12 ❌
- **TP 15RR**: 20747.07 ❌
- **PnL**: -77.55 points (-1.0R)
- **MFE**: 35.70 points
- **MAE**: 85.18 points

### Trade #791 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 12:45:00
- **FVG 5m**: 21910.58 - 21924.86
- **Entrée**: 21910.32 @ 2025-05-19 13:14:00
- **Stop Loss**: 21966.70
- **Risk**: 56.37 points
- **TP 1RR**: 21853.95 ❌
- **TP 2RR**: 21797.58 ❌
- **TP 3RR**: 21741.21 ❌
- **TP 4RR**: 21684.83 ❌
- **TP 15RR**: 21064.74 ❌
- **PnL**: -56.37 points (-1.0R)
- **MFE**: 35.70 points
- **MAE**: 65.54 points

### Trade #792 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 12:45:00
- **FVG 5m**: 21910.58 - 21924.86
- **Entrée**: 21910.32 @ 2025-05-19 13:14:00
- **Stop Loss**: 21966.70
- **Risk**: 56.37 points
- **TP 1RR**: 21853.95 ❌
- **TP 2RR**: 21797.58 ❌
- **TP 3RR**: 21741.21 ❌
- **TP 4RR**: 21684.83 ❌
- **TP 15RR**: 21064.74 ❌
- **PnL**: -56.37 points (-1.0R)
- **MFE**: 35.70 points
- **MAE**: 65.54 points

### Trade #793 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-19 19:00:00
- **FVG 5m**: 21962.60 - 21967.96
- **Entrée**: 21961.33 @ 2025-05-19 19:49:00
- **Stop Loss**: 22006.76
- **Risk**: 45.43 points
- **TP 1RR**: 21915.90 ✅
- **TP 2RR**: 21870.48 ✅
- **TP 3RR**: 21825.05 ✅
- **TP 4RR**: 21779.62 ✅
- **TP 15RR**: 21279.93 ✅
- **PnL**: 681.40 points (15.0R)
- **MFE**: 691.63 points
- **MAE**: 30.60 points

### Trade #794 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-19 22:30:00
- **FVG 5m**: 21865.95 - 21875.89
- **Entrée**: 21876.66 @ 2025-05-19 23:53:00
- **Stop Loss**: 21847.37
- **Risk**: 29.29 points
- **TP 1RR**: 21905.95 ✅
- **TP 2RR**: 21935.24 ❌
- **TP 3RR**: 21964.53 ❌
- **TP 4RR**: 21993.82 ❌
- **TP 15RR**: 22316.03 ❌
- **PnL**: -29.29 points (-1.0R)
- **MFE**: 42.33 points
- **MAE**: 29.84 points

### Trade #795 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-20 01:30:00
- **FVG 5m**: 21876.66 - 21887.12
- **Entrée**: 21890.43 @ 2025-05-20 02:22:00
- **Stop Loss**: 21820.35
- **Risk**: 70.08 points
- **TP 1RR**: 21960.51 ❌
- **TP 2RR**: 22030.59 ❌
- **TP 3RR**: 22100.68 ❌
- **TP 4RR**: 22170.76 ❌
- **TP 15RR**: 22941.66 ❌
- **PnL**: -70.08 points (-1.0R)
- **MFE**: 25.25 points
- **MAE**: 96.65 points

### Trade #796 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-20 08:45:00
- **FVG 5m**: 21824.12 - 21826.67
- **Entrée**: 21829.99 @ 2025-05-20 09:17:00
- **Stop Loss**: 21773.19
- **Risk**: 56.80 points
- **TP 1RR**: 21886.79 ✅
- **TP 2RR**: 21943.58 ❌
- **TP 3RR**: 22000.38 ❌
- **TP 4RR**: 22057.18 ❌
- **TP 15RR**: 22681.94 ❌
- **PnL**: -56.80 points (-1.0R)
- **MFE**: 76.00 points
- **MAE**: 58.66 points

### Trade #797 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-20 13:30:00
- **FVG 5m**: 21787.66 - 21791.74
- **Entrée**: 21794.03 @ 2025-05-20 14:19:00
- **Stop Loss**: 21760.96
- **Risk**: 33.07 points
- **TP 1RR**: 21827.10 ✅
- **TP 2RR**: 21860.18 ✅
- **TP 3RR**: 21893.25 ❌
- **TP 4RR**: 21926.32 ❌
- **TP 15RR**: 22290.13 ❌
- **PnL**: -33.07 points (-1.0R)
- **MFE**: 89.26 points
- **MAE**: 37.23 points

### Trade #798 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 04:30:00
- **FVG 5m**: 21709.36 - 21723.13
- **Entrée**: 21703.75 @ 2025-05-21 04:42:00
- **Stop Loss**: 21748.54
- **Risk**: 44.79 points
- **TP 1RR**: 21658.96 ✅
- **TP 2RR**: 21614.18 ❌
- **TP 3RR**: 21569.39 ❌
- **TP 4RR**: 21524.60 ❌
- **TP 15RR**: 21031.94 ❌
- **PnL**: -44.79 points (-1.0R)
- **MFE**: 47.18 points
- **MAE**: 47.69 points

### Trade #799 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 05:45:00
- **FVG 5m**: 21732.57 - 21737.93
- **Entrée**: 21742.52 @ 2025-05-21 06:08:00
- **Stop Loss**: 21692.39
- **Risk**: 50.13 points
- **TP 1RR**: 21792.64 ❌
- **TP 2RR**: 21842.77 ❌
- **TP 3RR**: 21892.89 ❌
- **TP 4RR**: 21943.02 ❌
- **TP 15RR**: 22494.40 ❌
- **PnL**: -50.13 points (-1.0R)
- **MFE**: 42.59 points
- **MAE**: 52.54 points

### Trade #800 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 05:45:00
- **FVG 5m**: 21732.57 - 21737.93
- **Entrée**: 21742.52 @ 2025-05-21 06:08:00
- **Stop Loss**: 21692.39
- **Risk**: 50.13 points
- **TP 1RR**: 21792.64 ❌
- **TP 2RR**: 21842.77 ❌
- **TP 3RR**: 21892.89 ❌
- **TP 4RR**: 21943.02 ❌
- **TP 15RR**: 22494.40 ❌
- **PnL**: -50.13 points (-1.0R)
- **MFE**: 42.59 points
- **MAE**: 52.54 points

### Trade #801 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 11:45:00
- **FVG 5m**: 21955.97 - 21974.33
- **Entrée**: 21955.72 @ 2025-05-21 11:56:00
- **Stop Loss**: 22002.93
- **Risk**: 47.21 points
- **TP 1RR**: 21908.51 ✅
- **TP 2RR**: 21861.30 ✅
- **TP 3RR**: 21814.09 ✅
- **TP 4RR**: 21766.88 ✅
- **TP 15RR**: 21247.57 ✅
- **PnL**: 708.15 points (15.0R)
- **MFE**: 713.56 points
- **MAE**: 8.16 points

### Trade #802 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21889.41 - 21897.57
- **Entrée**: 21886.10 @ 2025-05-21 12:11:00
- **Stop Loss**: 21966.95
- **Risk**: 80.86 points
- **TP 1RR**: 21805.24 ✅
- **TP 2RR**: 21724.39 ✅
- **TP 3RR**: 21643.53 ✅
- **TP 4RR**: 21562.68 ✅
- **TP 15RR**: 20673.27 ❌
- **PnL**: -80.86 points (-1.0R)
- **MFE**: 742.38 points
- **MAE**: 81.10 points

### Trade #803 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21889.41 - 21897.57
- **Entrée**: 21886.10 @ 2025-05-21 12:11:00
- **Stop Loss**: 21966.95
- **Risk**: 80.86 points
- **TP 1RR**: 21805.24 ✅
- **TP 2RR**: 21724.39 ✅
- **TP 3RR**: 21643.53 ✅
- **TP 4RR**: 21562.68 ✅
- **TP 15RR**: 20673.27 ❌
- **PnL**: -80.86 points (-1.0R)
- **MFE**: 742.38 points
- **MAE**: 81.10 points

### Trade #804 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21889.41 - 21897.57
- **Entrée**: 21886.10 @ 2025-05-21 12:11:00
- **Stop Loss**: 21966.95
- **Risk**: 80.86 points
- **TP 1RR**: 21805.24 ✅
- **TP 2RR**: 21724.39 ✅
- **TP 3RR**: 21643.53 ✅
- **TP 4RR**: 21562.68 ✅
- **TP 15RR**: 20673.27 ❌
- **PnL**: -80.86 points (-1.0R)
- **MFE**: 742.38 points
- **MAE**: 81.10 points

### Trade #805 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:00:00
- **FVG 5m**: 21889.41 - 21897.57
- **Entrée**: 21886.10 @ 2025-05-21 12:11:00
- **Stop Loss**: 21966.95
- **Risk**: 80.86 points
- **TP 1RR**: 21805.24 ✅
- **TP 2RR**: 21724.39 ✅
- **TP 3RR**: 21643.53 ✅
- **TP 4RR**: 21562.68 ✅
- **TP 15RR**: 20673.27 ❌
- **PnL**: -80.86 points (-1.0R)
- **MFE**: 742.38 points
- **MAE**: 81.10 points

### Trade #806 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21654.28 - 21675.44
- **Entrée**: 21637.70 @ 2025-05-21 13:49:00
- **Stop Loss**: 21900.36
- **Risk**: 262.66 points
- **TP 1RR**: 21375.04 ✅
- **TP 2RR**: 21112.39 ❌
- **TP 3RR**: 20849.73 ❌
- **TP 4RR**: 20587.08 ❌
- **TP 15RR**: 17697.87 ❌
- **PnL**: -262.66 points (-1.0R)
- **MFE**: 493.99 points
- **MAE**: 264.72 points

### Trade #807 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21654.28 - 21675.44
- **Entrée**: 21637.70 @ 2025-05-21 13:49:00
- **Stop Loss**: 21900.36
- **Risk**: 262.66 points
- **TP 1RR**: 21375.04 ✅
- **TP 2RR**: 21112.39 ❌
- **TP 3RR**: 20849.73 ❌
- **TP 4RR**: 20587.08 ❌
- **TP 15RR**: 17697.87 ❌
- **PnL**: -262.66 points (-1.0R)
- **MFE**: 493.99 points
- **MAE**: 264.72 points

### Trade #808 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21654.28 - 21675.44
- **Entrée**: 21637.70 @ 2025-05-21 13:49:00
- **Stop Loss**: 21900.36
- **Risk**: 262.66 points
- **TP 1RR**: 21375.04 ✅
- **TP 2RR**: 21112.39 ❌
- **TP 3RR**: 20849.73 ❌
- **TP 4RR**: 20587.08 ❌
- **TP 15RR**: 17697.87 ❌
- **PnL**: -262.66 points (-1.0R)
- **MFE**: 493.99 points
- **MAE**: 264.72 points

### Trade #809 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-21 12:15:00
- **FVG 5m**: 21654.28 - 21675.44
- **Entrée**: 21637.70 @ 2025-05-21 13:49:00
- **Stop Loss**: 21900.36
- **Risk**: 262.66 points
- **TP 1RR**: 21375.04 ✅
- **TP 2RR**: 21112.39 ❌
- **TP 3RR**: 20849.73 ❌
- **TP 4RR**: 20587.08 ❌
- **TP 15RR**: 17697.87 ❌
- **PnL**: -262.66 points (-1.0R)
- **MFE**: 493.99 points
- **MAE**: 264.72 points

### Trade #810 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-21 14:00:00
- **FVG 5m**: 21535.43 - 21560.17
- **Entrée**: 21560.94 @ 2025-05-21 14:32:00
- **Stop Loss**: 21505.80
- **Risk**: 55.13 points
- **TP 1RR**: 21616.07 ✅
- **TP 2RR**: 21671.20 ❌
- **TP 3RR**: 21726.34 ❌
- **TP 4RR**: 21781.47 ❌
- **TP 15RR**: 22387.93 ❌
- **PnL**: -55.13 points (-1.0R)
- **MFE**: 109.66 points
- **MAE**: 61.97 points

### Trade #811 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 01:00:00
- **FVG 5m**: 21628.01 - 21633.87
- **Entrée**: 21627.24 @ 2025-05-22 02:12:00
- **Stop Loss**: 21635.25
- **Risk**: 8.01 points
- **TP 1RR**: 21619.24 ✅
- **TP 2RR**: 21611.23 ✅
- **TP 3RR**: 21603.22 ✅
- **TP 4RR**: 21595.22 ❌
- **TP 15RR**: 21507.14 ❌
- **PnL**: -8.01 points (-1.0R)
- **MFE**: 30.86 points
- **MAE**: 9.95 points

### Trade #812 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 02:00:00
- **FVG 5m**: 21628.01 - 21633.87
- **Entrée**: 21627.24 @ 2025-05-22 02:12:00
- **Stop Loss**: 21664.34
- **Risk**: 37.09 points
- **TP 1RR**: 21590.15 ❌
- **TP 2RR**: 21553.06 ❌
- **TP 3RR**: 21515.96 ❌
- **TP 4RR**: 21478.87 ❌
- **TP 15RR**: 21070.83 ❌
- **PnL**: -37.09 points (-1.0R)
- **MFE**: 31.11 points
- **MAE**: 40.29 points

### Trade #813 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 06:00:00
- **FVG 5m**: 21636.43 - 21640.76
- **Entrée**: 21631.83 @ 2025-05-22 06:11:00
- **Stop Loss**: 21681.43
- **Risk**: 49.60 points
- **TP 1RR**: 21582.24 ✅
- **TP 2RR**: 21532.64 ✅
- **TP 3RR**: 21483.04 ✅
- **TP 4RR**: 21433.44 ❌
- **TP 15RR**: 20887.85 ❌
- **PnL**: -49.60 points (-1.0R)
- **MFE**: 168.83 points
- **MAE**: 55.60 points

### Trade #814 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:30:00
- **FVG 5m**: 21542.83 - 21545.64
- **Entrée**: 21555.07 @ 2025-05-22 07:43:00
- **Stop Loss**: 21452.28
- **Risk**: 102.80 points
- **TP 1RR**: 21657.87 ✅
- **TP 2RR**: 21760.66 ✅
- **TP 3RR**: 21863.46 ❌
- **TP 4RR**: 21966.26 ❌
- **TP 15RR**: 23097.01 ❌
- **PnL**: -102.80 points (-1.0R)
- **MFE**: 211.42 points
- **MAE**: 115.53 points

### Trade #815 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:45:00
- **FVG 5m**: 21600.72 - 21617.30
- **Entrée**: 21635.41 @ 2025-05-22 08:00:00
- **Stop Loss**: 21534.86
- **Risk**: 100.54 points
- **TP 1RR**: 21735.95 ✅
- **TP 2RR**: 21836.49 ❌
- **TP 3RR**: 21937.03 ❌
- **TP 4RR**: 22037.57 ❌
- **TP 15RR**: 23143.54 ❌
- **PnL**: -100.54 points (-1.0R)
- **MFE**: 131.08 points
- **MAE**: 101.76 points

### Trade #816 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:45:00
- **FVG 5m**: 21600.72 - 21617.30
- **Entrée**: 21635.41 @ 2025-05-22 08:00:00
- **Stop Loss**: 21534.86
- **Risk**: 100.54 points
- **TP 1RR**: 21735.95 ✅
- **TP 2RR**: 21836.49 ❌
- **TP 3RR**: 21937.03 ❌
- **TP 4RR**: 22037.57 ❌
- **TP 15RR**: 23143.54 ❌
- **PnL**: -100.54 points (-1.0R)
- **MFE**: 131.08 points
- **MAE**: 101.76 points

### Trade #817 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 07:45:00
- **FVG 5m**: 21600.72 - 21617.30
- **Entrée**: 21635.41 @ 2025-05-22 08:00:00
- **Stop Loss**: 21534.86
- **Risk**: 100.54 points
- **TP 1RR**: 21735.95 ✅
- **TP 2RR**: 21836.49 ❌
- **TP 3RR**: 21937.03 ❌
- **TP 4RR**: 22037.57 ❌
- **TP 15RR**: 23143.54 ❌
- **PnL**: -100.54 points (-1.0R)
- **MFE**: 131.08 points
- **MAE**: 101.76 points

### Trade #818 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 09:15:00
- **FVG 5m**: 21708.34 - 21713.70
- **Entrée**: 21708.09 @ 2025-05-22 11:21:00
- **Stop Loss**: 21723.79
- **Risk**: 15.70 points
- **TP 1RR**: 21692.39 ✅
- **TP 2RR**: 21676.68 ✅
- **TP 3RR**: 21660.98 ✅
- **TP 4RR**: 21645.28 ✅
- **TP 15RR**: 21472.56 ❌
- **PnL**: -15.70 points (-1.0R)
- **MFE**: 85.69 points
- **MAE**: 23.46 points

### Trade #819 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-22 14:00:00
- **FVG 5m**: 21714.97 - 21722.11
- **Entrée**: 21712.93 @ 2025-05-22 14:38:00
- **Stop Loss**: 21777.37
- **Risk**: 64.44 points
- **TP 1RR**: 21648.49 ✅
- **TP 2RR**: 21584.06 ✅
- **TP 3RR**: 21519.62 ✅
- **TP 4RR**: 21455.18 ✅
- **TP 15RR**: 20746.35 ❌
- **PnL**: -64.44 points (-1.0R)
- **MFE**: 569.22 points
- **MAE**: 64.78 points

### Trade #820 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 19:45:00
- **FVG 5m**: 21587.72 - 21595.37
- **Entrée**: 21597.41 @ 2025-05-22 21:03:00
- **Stop Loss**: 21593.74
- **Risk**: 3.66 points
- **TP 1RR**: 21601.07 ✅
- **TP 2RR**: 21604.73 ✅
- **TP 3RR**: 21608.39 ✅
- **TP 4RR**: 21612.05 ✅
- **TP 15RR**: 21652.33 ❌
- **PnL**: -3.66 points (-1.0R)
- **MFE**: 37.49 points
- **MAE**: 5.10 points

### Trade #821 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-22 23:45:00
- **FVG 5m**: 21579.04 - 21586.19
- **Entrée**: 21587.46 @ 2025-05-23 00:02:00
- **Stop Loss**: 21555.25
- **Risk**: 32.21 points
- **TP 1RR**: 21619.67 ❌
- **TP 2RR**: 21651.87 ❌
- **TP 3RR**: 21684.08 ❌
- **TP 4RR**: 21716.28 ❌
- **TP 15RR**: 22070.54 ❌
- **PnL**: -32.21 points (-1.0R)
- **MFE**: 19.89 points
- **MAE**: 35.19 points

### Trade #822 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 03:30:00
- **FVG 5m**: 21608.63 - 21611.69
- **Entrée**: 21604.29 @ 2025-05-23 04:01:00
- **Stop Loss**: 21657.70
- **Risk**: 53.41 points
- **TP 1RR**: 21550.88 ✅
- **TP 2RR**: 21497.47 ✅
- **TP 3RR**: 21444.05 ✅
- **TP 4RR**: 21390.64 ✅
- **TP 15RR**: 20803.10 ❌
- **PnL**: -53.41 points (-1.0R)
- **MFE**: 460.58 points
- **MAE**: 56.11 points

### Trade #823 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 03:30:00
- **FVG 5m**: 21608.63 - 21611.69
- **Entrée**: 21604.29 @ 2025-05-23 04:01:00
- **Stop Loss**: 21657.70
- **Risk**: 53.41 points
- **TP 1RR**: 21550.88 ✅
- **TP 2RR**: 21497.47 ✅
- **TP 3RR**: 21444.05 ✅
- **TP 4RR**: 21390.64 ✅
- **TP 15RR**: 20803.10 ❌
- **PnL**: -53.41 points (-1.0R)
- **MFE**: 460.58 points
- **MAE**: 56.11 points

### Trade #824 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-23 04:30:00
- **FVG 5m**: 21592.05 - 21606.59
- **Entrée**: 21609.90 @ 2025-05-23 04:55:00
- **Stop Loss**: 21533.33
- **Risk**: 76.57 points
- **TP 1RR**: 21686.47 ❌
- **TP 2RR**: 21763.04 ❌
- **TP 3RR**: 21839.61 ❌
- **TP 4RR**: 21916.18 ❌
- **TP 15RR**: 22758.43 ❌
- **PnL**: -76.57 points (-1.0R)
- **MFE**: 7.40 points
- **MAE**: 77.02 points

### Trade #825 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 06:30:00
- **FVG 5m**: 21371.96 - 21500.24
- **Entrée**: 21365.33 @ 2025-05-23 06:44:00
- **Stop Loss**: 21550.28
- **Risk**: 184.95 points
- **TP 1RR**: 21180.38 ✅
- **TP 2RR**: 20995.43 ❌
- **TP 3RR**: 20810.47 ❌
- **TP 4RR**: 20625.52 ❌
- **TP 15RR**: 18591.04 ❌
- **PnL**: -184.95 points (-1.0R)
- **MFE**: 221.62 points
- **MAE**: 195.10 points

### Trade #826 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 06:30:00
- **FVG 5m**: 21371.96 - 21500.24
- **Entrée**: 21365.33 @ 2025-05-23 06:44:00
- **Stop Loss**: 21550.28
- **Risk**: 184.95 points
- **TP 1RR**: 21180.38 ✅
- **TP 2RR**: 20995.43 ❌
- **TP 3RR**: 20810.47 ❌
- **TP 4RR**: 20625.52 ❌
- **TP 15RR**: 18591.04 ❌
- **PnL**: -184.95 points (-1.0R)
- **MFE**: 221.62 points
- **MAE**: 195.10 points

### Trade #827 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 06:45:00
- **FVG 5m**: 21258.99 - 21268.42
- **Entrée**: 21243.68 @ 2025-05-23 06:57:00
- **Stop Loss**: 21382.65
- **Risk**: 138.96 points
- **TP 1RR**: 21104.72 ❌
- **TP 2RR**: 20965.76 ❌
- **TP 3RR**: 20826.79 ❌
- **TP 4RR**: 20687.83 ❌
- **TP 15RR**: 19159.22 ❌
- **PnL**: -138.96 points (-1.0R)
- **MFE**: 99.97 points
- **MAE**: 172.65 points

### Trade #828 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-23 06:45:00
- **FVG 5m**: 21201.35 - 21209.00
- **Entrée**: 21215.63 @ 2025-05-23 07:28:00
- **Stop Loss**: 21209.61
- **Risk**: 6.02 points
- **TP 1RR**: 21221.65 ✅
- **TP 2RR**: 21227.67 ✅
- **TP 3RR**: 21233.69 ✅
- **TP 4RR**: 21239.71 ✅
- **TP 15RR**: 21305.93 ❌
- **PnL**: -6.02 points (-1.0R)
- **MFE**: 39.02 points
- **MAE**: 6.63 points

### Trade #829 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-23 06:45:00
- **FVG 5m**: 21201.35 - 21209.00
- **Entrée**: 21215.63 @ 2025-05-23 07:28:00
- **Stop Loss**: 21209.61
- **Risk**: 6.02 points
- **TP 1RR**: 21221.65 ✅
- **TP 2RR**: 21227.67 ✅
- **TP 3RR**: 21233.69 ✅
- **TP 4RR**: 21239.71 ✅
- **TP 15RR**: 21305.93 ❌
- **PnL**: -6.02 points (-1.0R)
- **MFE**: 39.02 points
- **MAE**: 6.63 points

### Trade #830 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 10:30:00
- **FVG 5m**: 21379.61 - 21387.01
- **Entrée**: 21366.86 @ 2025-05-23 10:52:00
- **Stop Loss**: 21441.84
- **Risk**: 74.98 points
- **TP 1RR**: 21291.88 ❌
- **TP 2RR**: 21216.90 ❌
- **TP 3RR**: 21141.92 ❌
- **TP 4RR**: 21066.93 ❌
- **TP 15RR**: 20242.13 ❌
- **PnL**: -74.98 points (-1.0R)
- **MFE**: 28.56 points
- **MAE**: 80.33 points

### Trade #831 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-23 14:45:00
- **FVG 5m**: 21370.94 - 21380.12
- **Entrée**: 21370.18 @ 2025-05-23 15:03:00
- **Stop Loss**: 21479.35
- **Risk**: 109.17 points
- **TP 1RR**: 21261.00 ❌
- **TP 2RR**: 21151.83 ❌
- **TP 3RR**: 21042.65 ❌
- **TP 4RR**: 20933.48 ❌
- **TP 15RR**: 19732.56 ❌
- **PnL**: -109.17 points (-1.0R)
- **MFE**: 18.62 points
- **MAE**: 112.72 points

### Trade #832 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-25 17:00:00
- **FVG 5m**: 21543.85 - 21551.50
- **Entrée**: 21555.58 @ 2025-05-25 17:19:00
- **Stop Loss**: 21364.85
- **Risk**: 190.74 points
- **TP 1RR**: 21746.32 ✅
- **TP 2RR**: 21937.05 ✅
- **TP 3RR**: 22127.79 ✅
- **TP 4RR**: 22318.53 ✅
- **TP 15RR**: 24416.63 ✅
- **PnL**: 2861.04 points (15.0R)
- **MFE**: 2861.92 points
- **MAE**: 60.44 points

### Trade #833 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-25 17:15:00
- **FVG 5m**: 21580.57 - 21587.72
- **Entrée**: 21588.23 @ 2025-05-25 17:46:00
- **Stop Loss**: 21505.29
- **Risk**: 82.93 points
- **TP 1RR**: 21671.16 ✅
- **TP 2RR**: 21754.09 ✅
- **TP 3RR**: 21837.02 ✅
- **TP 4RR**: 21919.95 ✅
- **TP 15RR**: 22832.18 ❌
- **PnL**: -82.93 points (-1.0R)
- **MFE**: 709.99 points
- **MAE**: 85.43 points

### Trade #834 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-26 01:30:00
- **FVG 5m**: 21680.29 - 21695.59
- **Entrée**: 21676.97 @ 2025-05-26 03:53:00
- **Stop Loss**: 21686.54
- **Risk**: 9.56 points
- **TP 1RR**: 21667.41 ✅
- **TP 2RR**: 21657.85 ❌
- **TP 3RR**: 21648.29 ❌
- **TP 4RR**: 21638.72 ❌
- **TP 15RR**: 21533.53 ❌
- **PnL**: -9.56 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 11.22 points

### Trade #835 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-26 01:30:00
- **FVG 5m**: 21680.29 - 21695.59
- **Entrée**: 21676.97 @ 2025-05-26 03:53:00
- **Stop Loss**: 21686.54
- **Risk**: 9.56 points
- **TP 1RR**: 21667.41 ✅
- **TP 2RR**: 21657.85 ❌
- **TP 3RR**: 21648.29 ❌
- **TP 4RR**: 21638.72 ❌
- **TP 15RR**: 21533.53 ❌
- **PnL**: -9.56 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 11.22 points

### Trade #836 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-26 01:30:00
- **FVG 5m**: 21680.29 - 21695.59
- **Entrée**: 21676.97 @ 2025-05-26 03:53:00
- **Stop Loss**: 21686.54
- **Risk**: 9.56 points
- **TP 1RR**: 21667.41 ✅
- **TP 2RR**: 21657.85 ❌
- **TP 3RR**: 21648.29 ❌
- **TP 4RR**: 21638.72 ❌
- **TP 15RR**: 21533.53 ❌
- **PnL**: -9.56 points (-1.0R)
- **MFE**: 11.73 points
- **MAE**: 11.22 points

### Trade #837 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-26 08:45:00
- **FVG 5m**: 21674.68 - 21691.00
- **Entrée**: 21674.17 @ 2025-05-26 09:33:00
- **Stop Loss**: 21743.44
- **Risk**: 69.27 points
- **TP 1RR**: 21604.90 ✅
- **TP 2RR**: 21535.63 ❌
- **TP 3RR**: 21466.37 ❌
- **TP 4RR**: 21397.10 ❌
- **TP 15RR**: 20635.16 ❌
- **PnL**: -69.27 points (-1.0R)
- **MFE**: 107.62 points
- **MAE**: 70.39 points

### Trade #838 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-26 10:15:00
- **FVG 5m**: 21668.05 - 21680.29
- **Entrée**: 21680.54 @ 2025-05-26 10:29:00
- **Stop Loss**: 21641.67
- **Risk**: 38.88 points
- **TP 1RR**: 21719.42 ✅
- **TP 2RR**: 21758.30 ❌
- **TP 3RR**: 21797.18 ❌
- **TP 4RR**: 21836.06 ❌
- **TP 15RR**: 22263.73 ❌
- **PnL**: -38.88 points (-1.0R)
- **MFE**: 41.57 points
- **MAE**: 51.77 points

### Trade #839 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-27 00:15:00
- **FVG 5m**: 21608.88 - 21612.96
- **Entrée**: 21617.04 @ 2025-05-27 00:27:00
- **Stop Loss**: 21581.76
- **Risk**: 35.28 points
- **TP 1RR**: 21652.32 ✅
- **TP 2RR**: 21687.60 ✅
- **TP 3RR**: 21722.88 ✅
- **TP 4RR**: 21758.16 ✅
- **TP 15RR**: 22146.23 ✅
- **PnL**: 529.18 points (15.0R)
- **MFE**: 564.12 points
- **MAE**: 4.08 points

### Trade #840 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-27 01:00:00
- **FVG 5m**: 21647.14 - 21655.81
- **Entrée**: 21657.34 @ 2025-05-27 01:19:00
- **Stop Loss**: 21620.25
- **Risk**: 37.08 points
- **TP 1RR**: 21694.42 ✅
- **TP 2RR**: 21731.50 ✅
- **TP 3RR**: 21768.59 ✅
- **TP 4RR**: 21805.67 ❌
- **TP 15RR**: 22213.59 ❌
- **PnL**: -37.08 points (-1.0R)
- **MFE**: 131.85 points
- **MAE**: 38.51 points

### Trade #841 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 02:45:00
- **FVG 5m**: 21765.98 - 21770.31
- **Entrée**: 21760.37 @ 2025-05-27 02:57:00
- **Stop Loss**: 21800.08
- **Risk**: 39.71 points
- **TP 1RR**: 21720.66 ✅
- **TP 2RR**: 21680.94 ✅
- **TP 3RR**: 21641.23 ✅
- **TP 4RR**: 21601.52 ❌
- **TP 15RR**: 21164.68 ❌
- **PnL**: -39.71 points (-1.0R)
- **MFE**: 141.54 points
- **MAE**: 40.29 points

### Trade #842 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 03:15:00
- **FVG 5m**: 21737.93 - 21744.56
- **Entrée**: 21736.91 @ 2025-05-27 03:49:00
- **Stop Loss**: 21783.50
- **Risk**: 46.59 points
- **TP 1RR**: 21690.32 ✅
- **TP 2RR**: 21643.73 ✅
- **TP 3RR**: 21597.14 ❌
- **TP 4RR**: 21550.55 ❌
- **TP 15RR**: 21038.06 ❌
- **PnL**: -46.59 points (-1.0R)
- **MFE**: 118.08 points
- **MAE**: 47.69 points

### Trade #843 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 05:45:00
- **FVG 5m**: 21730.78 - 21734.36
- **Entrée**: 21722.62 @ 2025-05-27 06:00:00
- **Stop Loss**: 21768.70
- **Risk**: 46.07 points
- **TP 1RR**: 21676.55 ✅
- **TP 2RR**: 21630.48 ✅
- **TP 3RR**: 21584.41 ❌
- **TP 4RR**: 21538.33 ❌
- **TP 15RR**: 21031.54 ❌
- **PnL**: -46.07 points (-1.0R)
- **MFE**: 103.80 points
- **MAE**: 48.97 points

### Trade #844 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 07:15:00
- **FVG 5m**: 21712.42 - 21731.04
- **Entrée**: 21694.32 @ 2025-05-27 08:27:00
- **Stop Loss**: 21744.20
- **Risk**: 49.89 points
- **TP 1RR**: 21644.43 ✅
- **TP 2RR**: 21594.54 ❌
- **TP 3RR**: 21544.66 ❌
- **TP 4RR**: 21494.77 ❌
- **TP 15RR**: 20946.03 ❌
- **PnL**: -49.89 points (-1.0R)
- **MFE**: 75.49 points
- **MAE**: 62.99 points

### Trade #845 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-27 13:30:00
- **FVG 5m**: 21875.64 - 21879.21
- **Entrée**: 21873.85 @ 2025-05-27 13:59:00
- **Stop Loss**: 21910.56
- **Risk**: 36.71 points
- **TP 1RR**: 21837.15 ❌
- **TP 2RR**: 21800.44 ❌
- **TP 3RR**: 21763.73 ❌
- **TP 4RR**: 21727.02 ❌
- **TP 15RR**: 21323.24 ❌
- **PnL**: -36.71 points (-1.0R)
- **MFE**: 29.07 points
- **MAE**: 37.49 points

### Trade #846 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 03:30:00
- **FVG 5m**: 21861.36 - 21863.91
- **Entrée**: 21864.67 @ 2025-05-28 05:01:00
- **Stop Loss**: 21843.55
- **Risk**: 21.13 points
- **TP 1RR**: 21885.80 ✅
- **TP 2RR**: 21906.93 ✅
- **TP 3RR**: 21928.06 ✅
- **TP 4RR**: 21949.19 ✅
- **TP 15RR**: 22181.60 ❌
- **PnL**: -21.13 points (-1.0R)
- **MFE**: 136.44 points
- **MAE**: 33.15 points

### Trade #847 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 10:15:00
- **FVG 5m**: 21902.16 - 21905.22
- **Entrée**: 21907.77 @ 2025-05-28 12:03:00
- **Stop Loss**: 21858.58
- **Risk**: 49.19 points
- **TP 1RR**: 21956.96 ❌
- **TP 2RR**: 22006.15 ❌
- **TP 3RR**: 22055.34 ❌
- **TP 4RR**: 22104.53 ❌
- **TP 15RR**: 22645.60 ❌
- **PnL**: -49.19 points (-1.0R)
- **MFE**: 26.78 points
- **MAE**: 76.25 points

### Trade #848 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 13:45:00
- **FVG 5m**: 21907.01 - 21913.64
- **Entrée**: 21917.21 @ 2025-05-28 14:04:00
- **Stop Loss**: 21820.60
- **Risk**: 96.60 points
- **TP 1RR**: 22013.81 ❌
- **TP 2RR**: 22110.42 ❌
- **TP 3RR**: 22207.02 ❌
- **TP 4RR**: 22303.63 ❌
- **TP 15RR**: 23366.28 ❌
- **PnL**: -96.60 points (-1.0R)
- **MFE**: 29.58 points
- **MAE**: 107.62 points

### Trade #849 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 13:45:00
- **FVG 5m**: 21907.01 - 21913.64
- **Entrée**: 21917.21 @ 2025-05-28 14:04:00
- **Stop Loss**: 21820.60
- **Risk**: 96.60 points
- **TP 1RR**: 22013.81 ❌
- **TP 2RR**: 22110.42 ❌
- **TP 3RR**: 22207.02 ❌
- **TP 4RR**: 22303.63 ❌
- **TP 15RR**: 23366.28 ❌
- **PnL**: -96.60 points (-1.0R)
- **MFE**: 29.58 points
- **MAE**: 107.62 points

### Trade #850 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-28 15:15:00
- **FVG 5m**: 21892.47 - 21905.48
- **Entrée**: 21907.26 @ 2025-05-28 15:37:00
- **Stop Loss**: 21739.04
- **Risk**: 168.23 points
- **TP 1RR**: 22075.49 ✅
- **TP 2RR**: 22243.72 ✅
- **TP 3RR**: 22411.94 ❌
- **TP 4RR**: 22580.17 ❌
- **TP 15RR**: 24430.66 ❌
- **PnL**: -168.23 points (-1.0R)
- **MFE**: 390.96 points
- **MAE**: 178.01 points

### Trade #851 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-28 20:00:00
- **FVG 5m**: 22215.59 - 22217.88
- **Entrée**: 22213.55 @ 2025-05-28 20:13:00
- **Stop Loss**: 22272.11
- **Risk**: 58.57 points
- **TP 1RR**: 22154.98 ❌
- **TP 2RR**: 22096.42 ❌
- **TP 3RR**: 22037.85 ❌
- **TP 4RR**: 21979.29 ❌
- **TP 15RR**: 21335.07 ❌
- **PnL**: -58.57 points (-1.0R)
- **MFE**: 29.84 points
- **MAE**: 75.23 points

### Trade #852 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 02:15:00
- **FVG 5m**: 22235.99 - 22239.82
- **Entrée**: 22241.60 @ 2025-05-29 02:38:00
- **Stop Loss**: 22182.82
- **Risk**: 58.79 points
- **TP 1RR**: 22300.39 ❌
- **TP 2RR**: 22359.18 ❌
- **TP 3RR**: 22417.96 ❌
- **TP 4RR**: 22476.75 ❌
- **TP 15RR**: 23123.41 ❌
- **PnL**: -58.79 points (-1.0R)
- **MFE**: 56.62 points
- **MAE**: 66.05 points

### Trade #853 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 03:00:00
- **FVG 5m**: 22230.13 - 22254.61
- **Entrée**: 22227.58 @ 2025-05-29 03:28:00
- **Stop Loss**: 22309.37
- **Risk**: 81.79 points
- **TP 1RR**: 22145.78 ✅
- **TP 2RR**: 22063.99 ✅
- **TP 3RR**: 21982.20 ✅
- **TP 4RR**: 21900.41 ✅
- **TP 15RR**: 21000.71 ❌
- **PnL**: -81.79 points (-1.0R)
- **MFE**: 732.44 points
- **MAE**: 110.68 points

### Trade #854 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 03:00:00
- **FVG 5m**: 22230.13 - 22254.61
- **Entrée**: 22227.58 @ 2025-05-29 03:28:00
- **Stop Loss**: 22309.37
- **Risk**: 81.79 points
- **TP 1RR**: 22145.78 ✅
- **TP 2RR**: 22063.99 ✅
- **TP 3RR**: 21982.20 ✅
- **TP 4RR**: 21900.41 ✅
- **TP 15RR**: 21000.71 ❌
- **PnL**: -81.79 points (-1.0R)
- **MFE**: 732.44 points
- **MAE**: 110.68 points

### Trade #855 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 03:00:00
- **FVG 5m**: 22230.13 - 22254.61
- **Entrée**: 22227.58 @ 2025-05-29 03:28:00
- **Stop Loss**: 22309.37
- **Risk**: 81.79 points
- **TP 1RR**: 22145.78 ✅
- **TP 2RR**: 22063.99 ✅
- **TP 3RR**: 21982.20 ✅
- **TP 4RR**: 21900.41 ✅
- **TP 15RR**: 21000.71 ❌
- **PnL**: -81.79 points (-1.0R)
- **MFE**: 732.44 points
- **MAE**: 110.68 points

### Trade #856 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 06:45:00
- **FVG 5m**: 22082.98 - 22087.82
- **Entrée**: 22078.64 @ 2025-05-29 07:39:00
- **Stop Loss**: 22149.39
- **Risk**: 70.75 points
- **TP 1RR**: 22007.90 ✅
- **TP 2RR**: 21937.15 ✅
- **TP 3RR**: 21866.40 ✅
- **TP 4RR**: 21795.66 ✅
- **TP 15RR**: 21017.46 ❌
- **PnL**: -70.75 points (-1.0R)
- **MFE**: 583.50 points
- **MAE**: 71.92 points

### Trade #857 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 06:45:00
- **FVG 5m**: 22082.98 - 22087.82
- **Entrée**: 22078.64 @ 2025-05-29 07:39:00
- **Stop Loss**: 22149.39
- **Risk**: 70.75 points
- **TP 1RR**: 22007.90 ✅
- **TP 2RR**: 21937.15 ✅
- **TP 3RR**: 21866.40 ✅
- **TP 4RR**: 21795.66 ✅
- **TP 15RR**: 21017.46 ❌
- **PnL**: -70.75 points (-1.0R)
- **MFE**: 583.50 points
- **MAE**: 71.92 points

### Trade #858 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 06:45:00
- **FVG 5m**: 22082.98 - 22087.82
- **Entrée**: 22078.64 @ 2025-05-29 07:39:00
- **Stop Loss**: 22149.39
- **Risk**: 70.75 points
- **TP 1RR**: 22007.90 ✅
- **TP 2RR**: 21937.15 ✅
- **TP 3RR**: 21866.40 ✅
- **TP 4RR**: 21795.66 ✅
- **TP 15RR**: 21017.46 ❌
- **PnL**: -70.75 points (-1.0R)
- **MFE**: 583.50 points
- **MAE**: 71.92 points

### Trade #859 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22126.68
- **Risk**: 167.39 points
- **TP 1RR**: 21791.90 ✅
- **TP 2RR**: 21624.51 ✅
- **TP 3RR**: 21457.12 ❌
- **TP 4RR**: 21289.73 ❌
- **TP 15RR**: 19448.46 ❌
- **PnL**: -167.39 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 167.81 points

### Trade #860 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22126.68
- **Risk**: 167.39 points
- **TP 1RR**: 21791.90 ✅
- **TP 2RR**: 21624.51 ✅
- **TP 3RR**: 21457.12 ❌
- **TP 4RR**: 21289.73 ❌
- **TP 15RR**: 19448.46 ❌
- **PnL**: -167.39 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 167.81 points

### Trade #861 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22126.68
- **Risk**: 167.39 points
- **TP 1RR**: 21791.90 ✅
- **TP 2RR**: 21624.51 ✅
- **TP 3RR**: 21457.12 ❌
- **TP 4RR**: 21289.73 ❌
- **TP 15RR**: 19448.46 ❌
- **PnL**: -167.39 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 167.81 points

### Trade #862 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22126.68
- **Risk**: 167.39 points
- **TP 1RR**: 21791.90 ✅
- **TP 2RR**: 21624.51 ✅
- **TP 3RR**: 21457.12 ❌
- **TP 4RR**: 21289.73 ❌
- **TP 15RR**: 19448.46 ❌
- **PnL**: -167.39 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 167.81 points

### Trade #863 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22126.68
- **Risk**: 167.39 points
- **TP 1RR**: 21791.90 ✅
- **TP 2RR**: 21624.51 ✅
- **TP 3RR**: 21457.12 ❌
- **TP 4RR**: 21289.73 ❌
- **TP 15RR**: 19448.46 ❌
- **PnL**: -167.39 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 167.81 points

### Trade #864 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 08:30:00
- **FVG 5m**: 21970.51 - 21993.97
- **Entrée**: 21959.29 @ 2025-05-29 08:44:00
- **Stop Loss**: 22126.68
- **Risk**: 167.39 points
- **TP 1RR**: 21791.90 ✅
- **TP 2RR**: 21624.51 ✅
- **TP 3RR**: 21457.12 ❌
- **TP 4RR**: 21289.73 ❌
- **TP 15RR**: 19448.46 ❌
- **PnL**: -167.39 points (-1.0R)
- **MFE**: 464.15 points
- **MAE**: 167.81 points

### Trade #865 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-29 09:00:00
- **FVG 5m**: 21890.94 - 21913.89
- **Entrée**: 21877.94 @ 2025-05-29 10:32:00
- **Stop Loss**: 21977.16
- **Risk**: 99.22 points
- **TP 1RR**: 21778.71 ✅
- **TP 2RR**: 21679.49 ✅
- **TP 3RR**: 21580.27 ✅
- **TP 4RR**: 21481.05 ❌
- **TP 15RR**: 20389.60 ❌
- **PnL**: -99.22 points (-1.0R)
- **MFE**: 382.79 points
- **MAE**: 100.99 points

### Trade #866 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 11:00:00
- **FVG 5m**: 21801.43 - 21835.86
- **Entrée**: 21836.62 @ 2025-05-29 11:14:00
- **Stop Loss**: 21718.39
- **Risk**: 118.23 points
- **TP 1RR**: 21954.85 ❌
- **TP 2RR**: 22073.08 ❌
- **TP 3RR**: 22191.31 ❌
- **TP 4RR**: 22309.54 ❌
- **TP 15RR**: 23610.08 ❌
- **PnL**: -118.23 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 140.52 points

### Trade #867 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 11:00:00
- **FVG 5m**: 21801.43 - 21835.86
- **Entrée**: 21836.62 @ 2025-05-29 11:14:00
- **Stop Loss**: 21718.39
- **Risk**: 118.23 points
- **TP 1RR**: 21954.85 ❌
- **TP 2RR**: 22073.08 ❌
- **TP 3RR**: 22191.31 ❌
- **TP 4RR**: 22309.54 ❌
- **TP 15RR**: 23610.08 ❌
- **PnL**: -118.23 points (-1.0R)
- **MFE**: 80.33 points
- **MAE**: 140.52 points

### Trade #868 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 20:00:00
- **FVG 5m**: 21740.22 - 21744.56
- **Entrée**: 21747.62 @ 2025-05-29 20:34:00
- **Stop Loss**: 21685.25
- **Risk**: 62.36 points
- **TP 1RR**: 21809.98 ✅
- **TP 2RR**: 21872.34 ❌
- **TP 3RR**: 21934.71 ❌
- **TP 4RR**: 21997.07 ❌
- **TP 15RR**: 22683.07 ❌
- **PnL**: -62.36 points (-1.0R)
- **MFE**: 104.05 points
- **MAE**: 94.61 points

### Trade #869 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-29 20:15:00
- **FVG 5m**: 21740.22 - 21744.56
- **Entrée**: 21747.62 @ 2025-05-29 20:34:00
- **Stop Loss**: 21696.98
- **Risk**: 50.64 points
- **TP 1RR**: 21798.25 ✅
- **TP 2RR**: 21848.89 ✅
- **TP 3RR**: 21899.53 ❌
- **TP 4RR**: 21950.17 ❌
- **TP 15RR**: 22507.19 ❌
- **PnL**: -50.64 points (-1.0R)
- **MFE**: 104.05 points
- **MAE**: 94.61 points

### Trade #870 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 07:00:00
- **FVG 5m**: 21743.79 - 21763.68
- **Entrée**: 21773.63 @ 2025-05-30 07:33:00
- **Stop Loss**: 21642.18
- **Risk**: 131.45 points
- **TP 1RR**: 21905.08 ❌
- **TP 2RR**: 22036.54 ❌
- **TP 3RR**: 22167.99 ❌
- **TP 4RR**: 22299.44 ❌
- **TP 15RR**: 23745.44 ❌
- **PnL**: -131.45 points (-1.0R)
- **MFE**: 56.11 points
- **MAE**: 185.66 points

### Trade #871 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 07:30:00
- **FVG 5m**: 21767.25 - 21787.40
- **Entrée**: 21789.95 @ 2025-05-30 08:16:00
- **Stop Loss**: 21706.15
- **Risk**: 83.80 points
- **TP 1RR**: 21873.75 ❌
- **TP 2RR**: 21957.54 ❌
- **TP 3RR**: 22041.34 ❌
- **TP 4RR**: 22125.13 ❌
- **TP 15RR**: 23046.89 ❌
- **PnL**: -83.80 points (-1.0R)
- **MFE**: 30.60 points
- **MAE**: 102.52 points

### Trade #872 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 07:30:00
- **FVG 5m**: 21767.25 - 21787.40
- **Entrée**: 21789.95 @ 2025-05-30 08:16:00
- **Stop Loss**: 21706.15
- **Risk**: 83.80 points
- **TP 1RR**: 21873.75 ❌
- **TP 2RR**: 21957.54 ❌
- **TP 3RR**: 22041.34 ❌
- **TP 4RR**: 22125.13 ❌
- **TP 15RR**: 23046.89 ❌
- **PnL**: -83.80 points (-1.0R)
- **MFE**: 30.60 points
- **MAE**: 102.52 points

### Trade #873 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 07:30:00
- **FVG 5m**: 21767.25 - 21787.40
- **Entrée**: 21789.95 @ 2025-05-30 08:16:00
- **Stop Loss**: 21706.15
- **Risk**: 83.80 points
- **TP 1RR**: 21873.75 ❌
- **TP 2RR**: 21957.54 ❌
- **TP 3RR**: 22041.34 ❌
- **TP 4RR**: 22125.13 ❌
- **TP 15RR**: 23046.89 ❌
- **PnL**: -83.80 points (-1.0R)
- **MFE**: 30.60 points
- **MAE**: 102.52 points

### Trade #874 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 11:15:00
- **FVG 5m**: 21604.80 - 21670.60
- **Entrée**: 21601.23 @ 2025-05-30 11:29:00
- **Stop Loss**: 21768.44
- **Risk**: 167.21 points
- **TP 1RR**: 21434.02 ❌
- **TP 2RR**: 21266.81 ❌
- **TP 3RR**: 21099.60 ❌
- **TP 4RR**: 20932.39 ❌
- **TP 15RR**: 19093.08 ❌
- **PnL**: -167.21 points (-1.0R)
- **MFE**: 106.09 points
- **MAE**: 173.16 points

### Trade #875 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 12:00:00
- **FVG 5m**: 21633.36 - 21654.53
- **Entrée**: 21657.08 @ 2025-05-30 13:09:00
- **Stop Loss**: 21502.24
- **Risk**: 154.85 points
- **TP 1RR**: 21811.93 ✅
- **TP 2RR**: 21966.77 ✅
- **TP 3RR**: 22121.62 ✅
- **TP 4RR**: 22276.47 ✅
- **TP 15RR**: 23979.78 ✅
- **PnL**: 2322.69 points (15.0R)
- **MFE**: 2324.85 points
- **MAE**: 68.60 points

### Trade #876 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 13:00:00
- **FVG 5m**: 21670.60 - 21690.49
- **Entrée**: 21690.75 @ 2025-05-30 13:18:00
- **Stop Loss**: 21589.67
- **Risk**: 101.08 points
- **TP 1RR**: 21791.83 ✅
- **TP 2RR**: 21892.90 ❌
- **TP 3RR**: 21993.98 ❌
- **TP 4RR**: 22095.06 ❌
- **TP 15RR**: 23206.94 ❌
- **PnL**: -101.08 points (-1.0R)
- **MFE**: 173.67 points
- **MAE**: 102.27 points

### Trade #877 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 13:00:00
- **FVG 5m**: 21670.60 - 21690.49
- **Entrée**: 21690.75 @ 2025-05-30 13:18:00
- **Stop Loss**: 21589.67
- **Risk**: 101.08 points
- **TP 1RR**: 21791.83 ✅
- **TP 2RR**: 21892.90 ❌
- **TP 3RR**: 21993.98 ❌
- **TP 4RR**: 22095.06 ❌
- **TP 15RR**: 23206.94 ❌
- **PnL**: -101.08 points (-1.0R)
- **MFE**: 173.67 points
- **MAE**: 102.27 points

### Trade #878 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-05-30 13:00:00
- **FVG 5m**: 21670.60 - 21690.49
- **Entrée**: 21690.75 @ 2025-05-30 13:18:00
- **Stop Loss**: 21589.67
- **Risk**: 101.08 points
- **TP 1RR**: 21791.83 ✅
- **TP 2RR**: 21892.90 ❌
- **TP 3RR**: 21993.98 ❌
- **TP 4RR**: 22095.06 ❌
- **TP 15RR**: 23206.94 ❌
- **PnL**: -101.08 points (-1.0R)
- **MFE**: 173.67 points
- **MAE**: 102.27 points

### Trade #879 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 14:45:00
- **FVG 5m**: 21788.68 - 21792.76
- **Entrée**: 21772.86 @ 2025-05-30 15:03:00
- **Stop Loss**: 21875.35
- **Risk**: 102.49 points
- **TP 1RR**: 21670.38 ✅
- **TP 2RR**: 21567.89 ❌
- **TP 3RR**: 21465.40 ❌
- **TP 4RR**: 21362.92 ❌
- **TP 15RR**: 20235.56 ❌
- **PnL**: -102.49 points (-1.0R)
- **MFE**: 184.38 points
- **MAE**: 109.41 points

### Trade #880 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 14:45:00
- **FVG 5m**: 21788.68 - 21792.76
- **Entrée**: 21772.86 @ 2025-05-30 15:03:00
- **Stop Loss**: 21875.35
- **Risk**: 102.49 points
- **TP 1RR**: 21670.38 ✅
- **TP 2RR**: 21567.89 ❌
- **TP 3RR**: 21465.40 ❌
- **TP 4RR**: 21362.92 ❌
- **TP 15RR**: 20235.56 ❌
- **PnL**: -102.49 points (-1.0R)
- **MFE**: 184.38 points
- **MAE**: 109.41 points

### Trade #881 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-05-30 14:45:00
- **FVG 5m**: 21788.68 - 21792.76
- **Entrée**: 21772.86 @ 2025-05-30 15:03:00
- **Stop Loss**: 21875.35
- **Risk**: 102.49 points
- **TP 1RR**: 21670.38 ✅
- **TP 2RR**: 21567.89 ❌
- **TP 3RR**: 21465.40 ❌
- **TP 4RR**: 21362.92 ❌
- **TP 15RR**: 20235.56 ❌
- **PnL**: -102.49 points (-1.0R)
- **MFE**: 184.38 points
- **MAE**: 109.41 points

### Trade #882 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-02 06:00:00
- **FVG 5m**: 21691.00 - 21695.59
- **Entrée**: 21700.44 @ 2025-06-02 06:15:00
- **Stop Loss**: 21654.92
- **Risk**: 45.52 points
- **TP 1RR**: 21745.95 ✅
- **TP 2RR**: 21791.47 ✅
- **TP 3RR**: 21836.99 ✅
- **TP 4RR**: 21882.50 ✅
- **TP 15RR**: 22383.18 ✅
- **PnL**: 682.75 points (15.0R)
- **MFE**: 683.73 points
- **MAE**: 38.76 points

### Trade #883 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 08:30:00
- **FVG 5m**: 21811.37 - 21836.62
- **Entrée**: 21810.35 @ 2025-06-02 08:49:00
- **Stop Loss**: 21900.36
- **Risk**: 90.00 points
- **TP 1RR**: 21720.35 ✅
- **TP 2RR**: 21630.35 ❌
- **TP 3RR**: 21540.34 ❌
- **TP 4RR**: 21450.34 ❌
- **TP 15RR**: 20460.31 ❌
- **PnL**: -90.00 points (-1.0R)
- **MFE**: 148.68 points
- **MAE**: 92.83 points

### Trade #884 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 08:30:00
- **FVG 5m**: 21811.37 - 21836.62
- **Entrée**: 21810.35 @ 2025-06-02 08:49:00
- **Stop Loss**: 21900.36
- **Risk**: 90.00 points
- **TP 1RR**: 21720.35 ✅
- **TP 2RR**: 21630.35 ❌
- **TP 3RR**: 21540.34 ❌
- **TP 4RR**: 21450.34 ❌
- **TP 15RR**: 20460.31 ❌
- **PnL**: -90.00 points (-1.0R)
- **MFE**: 148.68 points
- **MAE**: 92.83 points

### Trade #885 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-02 19:15:00
- **FVG 5m**: 21903.44 - 21905.73
- **Entrée**: 21902.16 @ 2025-06-02 21:14:00
- **Stop Loss**: 21940.16
- **Risk**: 38.00 points
- **TP 1RR**: 21864.17 ✅
- **TP 2RR**: 21826.17 ❌
- **TP 3RR**: 21788.17 ❌
- **TP 4RR**: 21750.17 ❌
- **TP 15RR**: 21332.20 ❌
- **PnL**: -38.00 points (-1.0R)
- **MFE**: 72.68 points
- **MAE**: 38.25 points

### Trade #886 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-03 02:45:00
- **FVG 5m**: 21847.33 - 21854.47
- **Entrée**: 21856.00 @ 2025-06-03 03:32:00
- **Stop Loss**: 21844.31
- **Risk**: 11.69 points
- **TP 1RR**: 21867.70 ✅
- **TP 2RR**: 21879.39 ✅
- **TP 3RR**: 21891.08 ✅
- **TP 4RR**: 21902.77 ✅
- **TP 15RR**: 22031.39 ✅
- **PnL**: 175.39 points (15.0R)
- **MFE**: 177.50 points
- **MAE**: 7.65 points

### Trade #887 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-03 09:15:00
- **FVG 5m**: 22050.33 - 22060.53
- **Entrée**: 22065.63 @ 2025-06-03 09:47:00
- **Stop Loss**: 22020.19
- **Risk**: 45.44 points
- **TP 1RR**: 22111.08 ✅
- **TP 2RR**: 22156.52 ✅
- **TP 3RR**: 22201.97 ✅
- **TP 4RR**: 22247.41 ✅
- **TP 15RR**: 22747.30 ❌
- **PnL**: -45.44 points (-1.0R)
- **MFE**: 310.37 points
- **MAE**: 68.60 points

### Trade #888 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-03 13:00:00
- **FVG 5m**: 22133.73 - 22138.32
- **Entrée**: 22127.61 @ 2025-06-03 14:42:00
- **Stop Loss**: 22169.54
- **Risk**: 41.94 points
- **TP 1RR**: 22085.67 ❌
- **TP 2RR**: 22043.73 ❌
- **TP 3RR**: 22001.79 ❌
- **TP 4RR**: 21959.86 ❌
- **TP 15RR**: 21498.54 ❌
- **PnL**: -41.94 points (-1.0R)
- **MFE**: 27.03 points
- **MAE**: 47.69 points

### Trade #889 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 01:15:00
- **FVG 5m**: 22120.21 - 22123.02
- **Entrée**: 22117.91 @ 2025-06-04 02:09:00
- **Stop Loss**: 22159.08
- **Risk**: 41.17 points
- **TP 1RR**: 22076.75 ❌
- **TP 2RR**: 22035.58 ❌
- **TP 3RR**: 21994.41 ❌
- **TP 4RR**: 21953.25 ❌
- **TP 15RR**: 21500.41 ❌
- **PnL**: -41.17 points (-1.0R)
- **MFE**: 7.65 points
- **MAE**: 43.86 points

### Trade #890 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 03:45:00
- **FVG 5m**: 22170.96 - 22184.73
- **Entrée**: 22164.58 @ 2025-06-04 05:20:00
- **Stop Loss**: 22184.34
- **Risk**: 19.76 points
- **TP 1RR**: 22144.83 ❌
- **TP 2RR**: 22125.07 ❌
- **TP 3RR**: 22105.31 ❌
- **TP 4RR**: 22085.55 ❌
- **TP 15RR**: 21868.22 ❌
- **PnL**: -19.76 points (-1.0R)
- **MFE**: 8.16 points
- **MAE**: 21.17 points

### Trade #891 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 05:00:00
- **FVG 5m**: 22164.07 - 22166.88
- **Entrée**: 22167.64 @ 2025-06-04 05:44:00
- **Stop Loss**: 22158.09
- **Risk**: 9.55 points
- **TP 1RR**: 22177.20 ✅
- **TP 2RR**: 22186.75 ✅
- **TP 3RR**: 22196.31 ✅
- **TP 4RR**: 22205.86 ❌
- **TP 15RR**: 22310.96 ❌
- **PnL**: -9.55 points (-1.0R)
- **MFE**: 36.98 points
- **MAE**: 20.15 points

### Trade #892 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22206.03
- **Risk**: 66.95 points
- **TP 1RR**: 22072.13 ❌
- **TP 2RR**: 22005.19 ❌
- **TP 3RR**: 21938.24 ❌
- **TP 4RR**: 21871.29 ❌
- **TP 15RR**: 21134.86 ❌
- **PnL**: -66.95 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 67.84 points

### Trade #893 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22206.03
- **Risk**: 66.95 points
- **TP 1RR**: 22072.13 ❌
- **TP 2RR**: 22005.19 ❌
- **TP 3RR**: 21938.24 ❌
- **TP 4RR**: 21871.29 ❌
- **TP 15RR**: 21134.86 ❌
- **PnL**: -66.95 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 67.84 points

### Trade #894 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22206.03
- **Risk**: 66.95 points
- **TP 1RR**: 22072.13 ❌
- **TP 2RR**: 22005.19 ❌
- **TP 3RR**: 21938.24 ❌
- **TP 4RR**: 21871.29 ❌
- **TP 15RR**: 21134.86 ❌
- **PnL**: -66.95 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 67.84 points

### Trade #895 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22168.92 - 22186.26
- **Entrée**: 22192.38 @ 2025-06-04 08:34:00
- **Stop Loss**: 22079.58
- **Risk**: 112.80 points
- **TP 1RR**: 22305.18 ❌
- **TP 2RR**: 22417.98 ❌
- **TP 3RR**: 22530.78 ❌
- **TP 4RR**: 22643.59 ❌
- **TP 15RR**: 23884.39 ❌
- **PnL**: -112.80 points (-1.0R)
- **MFE**: 39.02 points
- **MAE**: 116.29 points

### Trade #896 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 07:15:00
- **FVG 5m**: 22168.92 - 22186.26
- **Entrée**: 22192.38 @ 2025-06-04 08:34:00
- **Stop Loss**: 22079.58
- **Risk**: 112.80 points
- **TP 1RR**: 22305.18 ❌
- **TP 2RR**: 22417.98 ❌
- **TP 3RR**: 22530.78 ❌
- **TP 4RR**: 22643.59 ❌
- **TP 15RR**: 23884.39 ❌
- **PnL**: -112.80 points (-1.0R)
- **MFE**: 39.02 points
- **MAE**: 116.29 points

### Trade #897 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 08:15:00
- **FVG 5m**: 22168.92 - 22186.26
- **Entrée**: 22192.38 @ 2025-06-04 08:34:00
- **Stop Loss**: 22129.03
- **Risk**: 63.35 points
- **TP 1RR**: 22255.73 ❌
- **TP 2RR**: 22319.08 ❌
- **TP 3RR**: 22382.43 ❌
- **TP 4RR**: 22445.78 ❌
- **TP 15RR**: 23142.64 ❌
- **PnL**: -63.35 points (-1.0R)
- **MFE**: 39.02 points
- **MAE**: 66.31 points

### Trade #898 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 08:30:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22242.52
- **Risk**: 103.44 points
- **TP 1RR**: 22035.65 ❌
- **TP 2RR**: 21932.21 ❌
- **TP 3RR**: 21828.78 ❌
- **TP 4RR**: 21725.34 ❌
- **TP 15RR**: 20587.55 ❌
- **PnL**: -103.44 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 106.35 points

### Trade #899 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 08:30:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22242.52
- **Risk**: 103.44 points
- **TP 1RR**: 22035.65 ❌
- **TP 2RR**: 21932.21 ❌
- **TP 3RR**: 21828.78 ❌
- **TP 4RR**: 21725.34 ❌
- **TP 15RR**: 20587.55 ❌
- **PnL**: -103.44 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 106.35 points

### Trade #900 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-04 08:30:00
- **FVG 5m**: 22140.87 - 22173.77
- **Entrée**: 22139.08 @ 2025-06-04 09:03:00
- **Stop Loss**: 22242.52
- **Risk**: 103.44 points
- **TP 1RR**: 22035.65 ❌
- **TP 2RR**: 21932.21 ❌
- **TP 3RR**: 21828.78 ❌
- **TP 4RR**: 21725.34 ❌
- **TP 15RR**: 20587.55 ❌
- **PnL**: -103.44 points (-1.0R)
- **MFE**: 62.99 points
- **MAE**: 106.35 points

### Trade #901 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 09:00:00
- **FVG 5m**: 22171.98 - 22192.89
- **Entrée**: 22198.50 @ 2025-06-04 09:59:00
- **Stop Loss**: 22065.05
- **Risk**: 133.45 points
- **TP 1RR**: 22331.95 ✅
- **TP 2RR**: 22465.40 ❌
- **TP 3RR**: 22598.85 ❌
- **TP 4RR**: 22732.31 ❌
- **TP 15RR**: 24200.26 ❌
- **PnL**: -133.45 points (-1.0R)
- **MFE**: 177.50 points
- **MAE**: 138.22 points

### Trade #902 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-04 09:00:00
- **FVG 5m**: 22171.98 - 22192.89
- **Entrée**: 22198.50 @ 2025-06-04 09:59:00
- **Stop Loss**: 22065.05
- **Risk**: 133.45 points
- **TP 1RR**: 22331.95 ✅
- **TP 2RR**: 22465.40 ❌
- **TP 3RR**: 22598.85 ❌
- **TP 4RR**: 22732.31 ❌
- **TP 15RR**: 24200.26 ❌
- **PnL**: -133.45 points (-1.0R)
- **MFE**: 177.50 points
- **MAE**: 138.22 points

### Trade #903 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 02:45:00
- **FVG 5m**: 22248.49 - 22256.90
- **Entrée**: 22248.23 @ 2025-06-05 03:47:00
- **Stop Loss**: 22281.81
- **Risk**: 33.58 points
- **TP 1RR**: 22214.66 ✅
- **TP 2RR**: 22181.08 ✅
- **TP 3RR**: 22147.50 ❌
- **TP 4RR**: 22113.92 ❌
- **TP 15RR**: 21744.57 ❌
- **PnL**: -33.58 points (-1.0R)
- **MFE**: 99.21 points
- **MAE**: 90.02 points

### Trade #904 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 03:45:00
- **FVG 5m**: 22215.59 - 22218.14
- **Entrée**: 22208.96 @ 2025-06-05 04:14:00
- **Stop Loss**: 22270.58
- **Risk**: 61.62 points
- **TP 1RR**: 22147.33 ❌
- **TP 2RR**: 22085.71 ❌
- **TP 3RR**: 22024.08 ❌
- **TP 4RR**: 21962.46 ❌
- **TP 15RR**: 21284.59 ❌
- **PnL**: -61.62 points (-1.0R)
- **MFE**: 59.93 points
- **MAE**: 129.30 points

### Trade #905 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 03:45:00
- **FVG 5m**: 22215.59 - 22218.14
- **Entrée**: 22208.96 @ 2025-06-05 04:14:00
- **Stop Loss**: 22270.58
- **Risk**: 61.62 points
- **TP 1RR**: 22147.33 ❌
- **TP 2RR**: 22085.71 ❌
- **TP 3RR**: 22024.08 ❌
- **TP 4RR**: 21962.46 ❌
- **TP 15RR**: 21284.59 ❌
- **PnL**: -61.62 points (-1.0R)
- **MFE**: 59.93 points
- **MAE**: 129.30 points

### Trade #906 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 04:00:00
- **FVG 5m**: 22215.59 - 22218.14
- **Entrée**: 22208.96 @ 2025-06-05 04:14:00
- **Stop Loss**: 22240.73
- **Risk**: 31.77 points
- **TP 1RR**: 22177.19 ❌
- **TP 2RR**: 22145.42 ❌
- **TP 3RR**: 22113.64 ❌
- **TP 4RR**: 22081.87 ❌
- **TP 15RR**: 21732.38 ❌
- **PnL**: -31.77 points (-1.0R)
- **MFE**: 7.40 points
- **MAE**: 32.90 points

### Trade #907 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 05:30:00
- **FVG 5m**: 22205.13 - 22223.50
- **Entrée**: 22200.80 @ 2025-06-05 05:42:00
- **Stop Loss**: 22254.25
- **Risk**: 53.46 points
- **TP 1RR**: 22147.34 ❌
- **TP 2RR**: 22093.89 ❌
- **TP 3RR**: 22040.43 ❌
- **TP 4RR**: 21986.97 ❌
- **TP 15RR**: 21398.96 ❌
- **PnL**: -53.46 points (-1.0R)
- **MFE**: 51.77 points
- **MAE**: 137.46 points

### Trade #908 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 05:30:00
- **FVG 5m**: 22205.13 - 22223.50
- **Entrée**: 22200.80 @ 2025-06-05 05:42:00
- **Stop Loss**: 22254.25
- **Risk**: 53.46 points
- **TP 1RR**: 22147.34 ❌
- **TP 2RR**: 22093.89 ❌
- **TP 3RR**: 22040.43 ❌
- **TP 4RR**: 21986.97 ❌
- **TP 15RR**: 21398.96 ❌
- **PnL**: -53.46 points (-1.0R)
- **MFE**: 51.77 points
- **MAE**: 137.46 points

### Trade #909 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 07:30:00
- **FVG 5m**: 22214.57 - 22250.27
- **Entrée**: 22285.21 @ 2025-06-05 07:49:00
- **Stop Loss**: 22137.95
- **Risk**: 147.26 points
- **TP 1RR**: 22432.47 ❌
- **TP 2RR**: 22579.73 ❌
- **TP 3RR**: 22726.99 ❌
- **TP 4RR**: 22874.25 ❌
- **TP 15RR**: 24494.09 ❌
- **PnL**: -147.26 points (-1.0R)
- **MFE**: 21.68 points
- **MAE**: 153.02 points

### Trade #910 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 07:30:00
- **FVG 5m**: 22214.57 - 22250.27
- **Entrée**: 22285.21 @ 2025-06-05 07:49:00
- **Stop Loss**: 22137.95
- **Risk**: 147.26 points
- **TP 1RR**: 22432.47 ❌
- **TP 2RR**: 22579.73 ❌
- **TP 3RR**: 22726.99 ❌
- **TP 4RR**: 22874.25 ❌
- **TP 15RR**: 24494.09 ❌
- **PnL**: -147.26 points (-1.0R)
- **MFE**: 21.68 points
- **MAE**: 153.02 points

### Trade #911 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 07:30:00
- **FVG 5m**: 22214.57 - 22250.27
- **Entrée**: 22285.21 @ 2025-06-05 07:49:00
- **Stop Loss**: 22137.95
- **Risk**: 147.26 points
- **TP 1RR**: 22432.47 ❌
- **TP 2RR**: 22579.73 ❌
- **TP 3RR**: 22726.99 ❌
- **TP 4RR**: 22874.25 ❌
- **TP 15RR**: 24494.09 ❌
- **PnL**: -147.26 points (-1.0R)
- **MFE**: 21.68 points
- **MAE**: 153.02 points

### Trade #912 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 08:45:00
- **FVG 5m**: 22171.98 - 22211.25
- **Entrée**: 22211.76 @ 2025-06-05 09:24:00
- **Stop Loss**: 22116.54
- **Risk**: 95.22 points
- **TP 1RR**: 22306.99 ✅
- **TP 2RR**: 22402.21 ❌
- **TP 3RR**: 22497.43 ❌
- **TP 4RR**: 22592.65 ❌
- **TP 15RR**: 23640.10 ❌
- **PnL**: -95.22 points (-1.0R)
- **MFE**: 164.24 points
- **MAE**: 105.84 points

### Trade #913 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 11:00:00
- **FVG 5m**: 22307.40 - 22322.45
- **Entrée**: 22306.63 @ 2025-06-05 11:14:00
- **Stop Loss**: 22374.94
- **Risk**: 68.31 points
- **TP 1RR**: 22238.33 ✅
- **TP 2RR**: 22170.02 ✅
- **TP 3RR**: 22101.71 ✅
- **TP 4RR**: 22033.40 ✅
- **TP 15RR**: 21282.02 ❌
- **PnL**: -68.31 points (-1.0R)
- **MFE**: 403.96 points
- **MAE**: 77.53 points

### Trade #914 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 11:00:00
- **FVG 5m**: 22307.40 - 22322.45
- **Entrée**: 22306.63 @ 2025-06-05 11:14:00
- **Stop Loss**: 22374.94
- **Risk**: 68.31 points
- **TP 1RR**: 22238.33 ✅
- **TP 2RR**: 22170.02 ✅
- **TP 3RR**: 22101.71 ✅
- **TP 4RR**: 22033.40 ✅
- **TP 15RR**: 21282.02 ❌
- **PnL**: -68.31 points (-1.0R)
- **MFE**: 403.96 points
- **MAE**: 77.53 points

### Trade #915 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 12:00:00
- **FVG 5m**: 22174.79 - 22193.91
- **Entrée**: 22194.93 @ 2025-06-05 12:14:00
- **Stop Loss**: 22083.91
- **Risk**: 111.02 points
- **TP 1RR**: 22305.95 ❌
- **TP 2RR**: 22416.97 ❌
- **TP 3RR**: 22527.99 ❌
- **TP 4RR**: 22639.00 ❌
- **TP 15RR**: 23860.20 ❌
- **PnL**: -111.02 points (-1.0R)
- **MFE**: 32.90 points
- **MAE**: 134.65 points

### Trade #916 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-05 15:30:00
- **FVG 5m**: 21931.24 - 21966.68
- **Entrée**: 21920.01 @ 2025-06-05 17:00:00
- **Stop Loss**: 22026.15
- **Risk**: 106.13 points
- **TP 1RR**: 21813.88 ❌
- **TP 2RR**: 21707.75 ❌
- **TP 3RR**: 21601.62 ❌
- **TP 4RR**: 21495.48 ❌
- **TP 15RR**: 20328.03 ❌
- **PnL**: -106.13 points (-1.0R)
- **MFE**: 3.57 points
- **MAE**: 107.62 points

### Trade #917 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 17:00:00
- **FVG 5m**: 21934.81 - 21940.16
- **Entrée**: 21940.67 @ 2025-06-05 17:14:00
- **Stop Loss**: 21891.72
- **Risk**: 48.95 points
- **TP 1RR**: 21989.62 ✅
- **TP 2RR**: 22038.57 ✅
- **TP 3RR**: 22087.52 ✅
- **TP 4RR**: 22136.47 ✅
- **TP 15RR**: 22674.93 ❌
- **PnL**: -48.95 points (-1.0R)
- **MFE**: 609.77 points
- **MAE**: 74.99 points

### Trade #918 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-05 17:00:00
- **FVG 5m**: 21934.81 - 21940.16
- **Entrée**: 21940.67 @ 2025-06-05 17:14:00
- **Stop Loss**: 21891.72
- **Risk**: 48.95 points
- **TP 1RR**: 21989.62 ✅
- **TP 2RR**: 22038.57 ✅
- **TP 3RR**: 22087.52 ✅
- **TP 4RR**: 22136.47 ✅
- **TP 15RR**: 22674.93 ❌
- **PnL**: -48.95 points (-1.0R)
- **MFE**: 609.77 points
- **MAE**: 74.99 points

### Trade #919 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-06 11:45:00
- **FVG 5m**: 22203.35 - 22222.22
- **Entrée**: 22223.24 @ 2025-06-06 12:19:00
- **Stop Loss**: 22147.64
- **Risk**: 75.60 points
- **TP 1RR**: 22298.84 ✅
- **TP 2RR**: 22374.44 ✅
- **TP 3RR**: 22450.04 ✅
- **TP 4RR**: 22525.64 ✅
- **TP 15RR**: 23357.26 ❌
- **PnL**: -75.60 points (-1.0R)
- **MFE**: 327.20 points
- **MAE**: 87.98 points

### Trade #920 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-09 08:30:00
- **FVG 5m**: 22235.74 - 22238.54
- **Entrée**: 22242.37 @ 2025-06-09 08:49:00
- **Stop Loss**: 22176.95
- **Risk**: 65.41 points
- **TP 1RR**: 22307.78 ✅
- **TP 2RR**: 22373.20 ✅
- **TP 3RR**: 22438.61 ❌
- **TP 4RR**: 22504.03 ❌
- **TP 15RR**: 23223.59 ❌
- **PnL**: -65.41 points (-1.0R)
- **MFE**: 172.65 points
- **MAE**: 73.45 points

### Trade #921 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-09 09:30:00
- **FVG 5m**: 22301.53 - 22304.85
- **Entrée**: 22297.71 @ 2025-06-09 09:44:00
- **Stop Loss**: 22342.03
- **Risk**: 44.32 points
- **TP 1RR**: 22253.39 ✅
- **TP 2RR**: 22209.07 ❌
- **TP 3RR**: 22164.75 ❌
- **TP 4RR**: 22120.43 ❌
- **TP 15RR**: 21632.93 ❌
- **PnL**: -44.32 points (-1.0R)
- **MFE**: 62.74 points
- **MAE**: 44.37 points

### Trade #922 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-09 09:30:00
- **FVG 5m**: 22301.53 - 22304.85
- **Entrée**: 22297.71 @ 2025-06-09 09:44:00
- **Stop Loss**: 22342.03
- **Risk**: 44.32 points
- **TP 1RR**: 22253.39 ✅
- **TP 2RR**: 22209.07 ❌
- **TP 3RR**: 22164.75 ❌
- **TP 4RR**: 22120.43 ❌
- **TP 15RR**: 21632.93 ❌
- **PnL**: -44.32 points (-1.0R)
- **MFE**: 62.74 points
- **MAE**: 44.37 points

### Trade #923 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-09 14:45:00
- **FVG 5m**: 22274.25 - 22276.54
- **Entrée**: 22273.74 @ 2025-06-09 17:28:00
- **Stop Loss**: 22309.62
- **Risk**: 35.89 points
- **TP 1RR**: 22237.85 ❌
- **TP 2RR**: 22201.96 ❌
- **TP 3RR**: 22166.08 ❌
- **TP 4RR**: 22130.19 ❌
- **TP 15RR**: 21735.43 ❌
- **PnL**: -35.89 points (-1.0R)
- **MFE**: 19.89 points
- **MAE**: 37.74 points

### Trade #924 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 00:15:00
- **FVG 5m**: 22228.85 - 22260.47
- **Entrée**: 22226.56 @ 2025-06-10 00:28:00
- **Stop Loss**: 22371.11
- **Risk**: 144.56 points
- **TP 1RR**: 22082.00 ❌
- **TP 2RR**: 21937.44 ❌
- **TP 3RR**: 21792.88 ❌
- **TP 4RR**: 21648.32 ❌
- **TP 15RR**: 20058.18 ❌
- **PnL**: -144.56 points (-1.0R)
- **MFE**: 57.64 points
- **MAE**: 145.11 points

### Trade #925 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 00:15:00
- **FVG 5m**: 22228.85 - 22260.47
- **Entrée**: 22226.56 @ 2025-06-10 00:28:00
- **Stop Loss**: 22371.11
- **Risk**: 144.56 points
- **TP 1RR**: 22082.00 ❌
- **TP 2RR**: 21937.44 ❌
- **TP 3RR**: 21792.88 ❌
- **TP 4RR**: 21648.32 ❌
- **TP 15RR**: 20058.18 ❌
- **PnL**: -144.56 points (-1.0R)
- **MFE**: 57.64 points
- **MAE**: 145.11 points

### Trade #926 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 00:15:00
- **FVG 5m**: 22228.85 - 22260.47
- **Entrée**: 22226.56 @ 2025-06-10 00:28:00
- **Stop Loss**: 22371.11
- **Risk**: 144.56 points
- **TP 1RR**: 22082.00 ❌
- **TP 2RR**: 21937.44 ❌
- **TP 3RR**: 21792.88 ❌
- **TP 4RR**: 21648.32 ❌
- **TP 15RR**: 20058.18 ❌
- **PnL**: -144.56 points (-1.0R)
- **MFE**: 57.64 points
- **MAE**: 145.11 points

### Trade #927 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 00:30:00
- **FVG 5m**: 22242.37 - 22247.98
- **Entrée**: 22248.49 @ 2025-06-10 02:16:00
- **Stop Loss**: 22182.82
- **Risk**: 65.67 points
- **TP 1RR**: 22314.16 ❌
- **TP 2RR**: 22379.83 ❌
- **TP 3RR**: 22445.51 ❌
- **TP 4RR**: 22511.18 ❌
- **TP 15RR**: 23233.58 ❌
- **PnL**: -65.67 points (-1.0R)
- **MFE**: 16.58 points
- **MAE**: 79.57 points

### Trade #928 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 00:30:00
- **FVG 5m**: 22242.37 - 22247.98
- **Entrée**: 22248.49 @ 2025-06-10 02:16:00
- **Stop Loss**: 22182.82
- **Risk**: 65.67 points
- **TP 1RR**: 22314.16 ❌
- **TP 2RR**: 22379.83 ❌
- **TP 3RR**: 22445.51 ❌
- **TP 4RR**: 22511.18 ❌
- **TP 15RR**: 23233.58 ❌
- **PnL**: -65.67 points (-1.0R)
- **MFE**: 16.58 points
- **MAE**: 79.57 points

### Trade #929 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 02:30:00
- **FVG 5m**: 22208.19 - 22213.04
- **Entrée**: 22206.92 @ 2025-06-10 02:43:00
- **Stop Loss**: 22263.95
- **Risk**: 57.03 points
- **TP 1RR**: 22149.89 ❌
- **TP 2RR**: 22092.86 ❌
- **TP 3RR**: 22035.83 ❌
- **TP 4RR**: 21978.79 ❌
- **TP 15RR**: 21351.45 ❌
- **PnL**: -57.03 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 59.68 points

### Trade #930 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 02:30:00
- **FVG 5m**: 22208.19 - 22213.04
- **Entrée**: 22206.92 @ 2025-06-10 02:43:00
- **Stop Loss**: 22263.95
- **Risk**: 57.03 points
- **TP 1RR**: 22149.89 ❌
- **TP 2RR**: 22092.86 ❌
- **TP 3RR**: 22035.83 ❌
- **TP 4RR**: 21978.79 ❌
- **TP 15RR**: 21351.45 ❌
- **PnL**: -57.03 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 59.68 points

### Trade #931 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 02:30:00
- **FVG 5m**: 22208.19 - 22213.04
- **Entrée**: 22206.92 @ 2025-06-10 02:43:00
- **Stop Loss**: 22263.95
- **Risk**: 57.03 points
- **TP 1RR**: 22149.89 ❌
- **TP 2RR**: 22092.86 ❌
- **TP 3RR**: 22035.83 ❌
- **TP 4RR**: 21978.79 ❌
- **TP 15RR**: 21351.45 ❌
- **PnL**: -57.03 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 59.68 points

### Trade #932 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 02:45:00
- **FVG 5m**: 22220.18 - 22230.13
- **Entrée**: 22231.15 @ 2025-06-10 02:56:00
- **Stop Loss**: 22157.84
- **Risk**: 73.31 points
- **TP 1RR**: 22304.46 ✅
- **TP 2RR**: 22377.77 ✅
- **TP 3RR**: 22451.08 ✅
- **TP 4RR**: 22524.39 ✅
- **TP 15RR**: 23330.81 ❌
- **PnL**: -73.31 points (-1.0R)
- **MFE**: 319.29 points
- **MAE**: 81.35 points

### Trade #933 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 02:45:00
- **FVG 5m**: 22220.18 - 22230.13
- **Entrée**: 22231.15 @ 2025-06-10 02:56:00
- **Stop Loss**: 22157.84
- **Risk**: 73.31 points
- **TP 1RR**: 22304.46 ✅
- **TP 2RR**: 22377.77 ✅
- **TP 3RR**: 22451.08 ✅
- **TP 4RR**: 22524.39 ✅
- **TP 15RR**: 23330.81 ❌
- **PnL**: -73.31 points (-1.0R)
- **MFE**: 319.29 points
- **MAE**: 81.35 points

### Trade #934 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 08:30:00
- **FVG 5m**: 22254.61 - 22293.63
- **Entrée**: 22235.99 @ 2025-06-10 10:32:00
- **Stop Loss**: 22337.69
- **Risk**: 101.70 points
- **TP 1RR**: 22134.29 ❌
- **TP 2RR**: 22032.60 ❌
- **TP 3RR**: 21930.90 ❌
- **TP 4RR**: 21829.20 ❌
- **TP 15RR**: 20710.53 ❌
- **PnL**: -101.70 points (-1.0R)
- **MFE**: 56.11 points
- **MAE**: 105.84 points

### Trade #935 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 10:30:00
- **FVG 5m**: 22254.61 - 22277.31
- **Entrée**: 22281.90 @ 2025-06-10 10:44:00
- **Stop Loss**: 22168.80
- **Risk**: 113.10 points
- **TP 1RR**: 22395.00 ✅
- **TP 2RR**: 22508.10 ✅
- **TP 3RR**: 22621.20 ❌
- **TP 4RR**: 22734.30 ❌
- **TP 15RR**: 23978.40 ❌
- **PnL**: -113.10 points (-1.0R)
- **MFE**: 268.54 points
- **MAE**: 122.16 points

### Trade #936 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 10:30:00
- **FVG 5m**: 22254.61 - 22277.31
- **Entrée**: 22281.90 @ 2025-06-10 10:44:00
- **Stop Loss**: 22168.80
- **Risk**: 113.10 points
- **TP 1RR**: 22395.00 ✅
- **TP 2RR**: 22508.10 ✅
- **TP 3RR**: 22621.20 ❌
- **TP 4RR**: 22734.30 ❌
- **TP 15RR**: 23978.40 ❌
- **PnL**: -113.10 points (-1.0R)
- **MFE**: 268.54 points
- **MAE**: 122.16 points

### Trade #937 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 12:15:00
- **FVG 5m**: 22333.67 - 22347.18
- **Entrée**: 22330.35 @ 2025-06-10 12:29:00
- **Stop Loss**: 22378.26
- **Risk**: 47.91 points
- **TP 1RR**: 22282.44 ✅
- **TP 2RR**: 22234.54 ❌
- **TP 3RR**: 22186.63 ❌
- **TP 4RR**: 22138.72 ❌
- **TP 15RR**: 21611.74 ❌
- **PnL**: -47.91 points (-1.0R)
- **MFE**: 70.90 points
- **MAE**: 78.55 points

### Trade #938 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-10 14:00:00
- **FVG 5m**: 22386.97 - 22394.62
- **Entrée**: 22405.58 @ 2025-06-10 15:18:00
- **Stop Loss**: 22377.30
- **Risk**: 28.28 points
- **TP 1RR**: 22433.87 ❌
- **TP 2RR**: 22462.15 ❌
- **TP 3RR**: 22490.43 ❌
- **TP 4RR**: 22518.71 ❌
- **TP 15RR**: 22829.80 ❌
- **PnL**: -28.28 points (-1.0R)
- **MFE**: 20.15 points
- **MAE**: 33.41 points

### Trade #939 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-10 18:15:00
- **FVG 5m**: 22401.76 - 22407.88
- **Entrée**: 22401.25 @ 2025-06-10 18:36:00
- **Stop Loss**: 22456.34
- **Risk**: 55.09 points
- **TP 1RR**: 22346.16 ✅
- **TP 2RR**: 22291.07 ❌
- **TP 3RR**: 22235.99 ❌
- **TP 4RR**: 22180.90 ❌
- **TP 15RR**: 21574.94 ❌
- **PnL**: -55.09 points (-1.0R)
- **MFE**: 95.89 points
- **MAE**: 149.19 points

### Trade #940 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 00:00:00
- **FVG 5m**: 22329.08 - 22333.16
- **Entrée**: 22333.92 @ 2025-06-11 00:14:00
- **Stop Loss**: 22294.21
- **Risk**: 39.72 points
- **TP 1RR**: 22373.64 ✅
- **TP 2RR**: 22413.35 ✅
- **TP 3RR**: 22453.07 ✅
- **TP 4RR**: 22492.78 ✅
- **TP 15RR**: 22929.66 ❌
- **PnL**: -39.72 points (-1.0R)
- **MFE**: 216.52 points
- **MAE**: 63.76 points

### Trade #941 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 00:00:00
- **FVG 5m**: 22329.08 - 22333.16
- **Entrée**: 22333.92 @ 2025-06-11 00:14:00
- **Stop Loss**: 22294.21
- **Risk**: 39.72 points
- **TP 1RR**: 22373.64 ✅
- **TP 2RR**: 22413.35 ✅
- **TP 3RR**: 22453.07 ✅
- **TP 4RR**: 22492.78 ✅
- **TP 15RR**: 22929.66 ❌
- **PnL**: -39.72 points (-1.0R)
- **MFE**: 216.52 points
- **MAE**: 63.76 points

### Trade #942 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 04:30:00
- **FVG 5m**: 22364.78 - 22368.35
- **Entrée**: 22363.25 @ 2025-06-11 06:01:00
- **Stop Loss**: 22396.89
- **Risk**: 33.64 points
- **TP 1RR**: 22329.61 ✅
- **TP 2RR**: 22295.98 ❌
- **TP 3RR**: 22262.34 ❌
- **TP 4RR**: 22228.71 ❌
- **TP 15RR**: 21858.72 ❌
- **PnL**: -33.64 points (-1.0R)
- **MFE**: 41.31 points
- **MAE**: 71.66 points

### Trade #943 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 06:00:00
- **FVG 5m**: 22346.42 - 22356.11
- **Entrée**: 22336.73 @ 2025-06-11 06:15:00
- **Stop Loss**: 22383.11
- **Risk**: 46.38 points
- **TP 1RR**: 22290.35 ❌
- **TP 2RR**: 22243.97 ❌
- **TP 3RR**: 22197.59 ❌
- **TP 4RR**: 22151.21 ❌
- **TP 15RR**: 21641.03 ❌
- **PnL**: -46.38 points (-1.0R)
- **MFE**: 14.79 points
- **MAE**: 98.19 points

### Trade #944 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 07:00:00
- **FVG 5m**: 22400.48 - 22500.96
- **Entrée**: 22502.49 @ 2025-06-11 07:34:00
- **Stop Loss**: 22317.40
- **Risk**: 185.09 points
- **TP 1RR**: 22687.59 ❌
- **TP 2RR**: 22872.68 ❌
- **TP 3RR**: 23057.77 ❌
- **TP 4RR**: 23242.86 ❌
- **TP 15RR**: 25278.88 ❌
- **PnL**: -185.09 points (-1.0R)
- **MFE**: 35.96 points
- **MAE**: 194.33 points

### Trade #945 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 07:45:00
- **FVG 5m**: 22444.86 - 22456.33
- **Entrée**: 22418.08 @ 2025-06-11 08:31:00
- **Stop Loss**: 22514.51
- **Risk**: 96.43 points
- **TP 1RR**: 22321.65 ✅
- **TP 2RR**: 22225.22 ✅
- **TP 3RR**: 22128.79 ✅
- **TP 4RR**: 22032.36 ✅
- **TP 15RR**: 20971.62 ❌
- **PnL**: -96.43 points (-1.0R)
- **MFE**: 637.74 points
- **MAE**: 100.25 points

### Trade #946 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 07:45:00
- **FVG 5m**: 22444.86 - 22456.33
- **Entrée**: 22418.08 @ 2025-06-11 08:31:00
- **Stop Loss**: 22514.51
- **Risk**: 96.43 points
- **TP 1RR**: 22321.65 ✅
- **TP 2RR**: 22225.22 ✅
- **TP 3RR**: 22128.79 ✅
- **TP 4RR**: 22032.36 ✅
- **TP 15RR**: 20971.62 ❌
- **PnL**: -96.43 points (-1.0R)
- **MFE**: 637.74 points
- **MAE**: 100.25 points

### Trade #947 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 07:45:00
- **FVG 5m**: 22444.86 - 22456.33
- **Entrée**: 22418.08 @ 2025-06-11 08:31:00
- **Stop Loss**: 22514.51
- **Risk**: 96.43 points
- **TP 1RR**: 22321.65 ✅
- **TP 2RR**: 22225.22 ✅
- **TP 3RR**: 22128.79 ✅
- **TP 4RR**: 22032.36 ✅
- **TP 15RR**: 20971.62 ❌
- **PnL**: -96.43 points (-1.0R)
- **MFE**: 637.74 points
- **MAE**: 100.25 points

### Trade #948 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 08:30:00
- **FVG 5m**: 22478.52 - 22498.67
- **Entrée**: 22441.54 @ 2025-06-11 10:09:00
- **Stop Loss**: 22479.04
- **Risk**: 37.50 points
- **TP 1RR**: 22404.04 ❌
- **TP 2RR**: 22366.54 ❌
- **TP 3RR**: 22329.04 ❌
- **TP 4RR**: 22291.54 ❌
- **TP 15RR**: 21879.02 ❌
- **PnL**: -37.50 points (-1.0R)
- **MFE**: 13.26 points
- **MAE**: 44.37 points

### Trade #949 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-11 08:30:00
- **FVG 5m**: 22478.52 - 22498.67
- **Entrée**: 22441.54 @ 2025-06-11 10:09:00
- **Stop Loss**: 22479.04
- **Risk**: 37.50 points
- **TP 1RR**: 22404.04 ❌
- **TP 2RR**: 22366.54 ❌
- **TP 3RR**: 22329.04 ❌
- **TP 4RR**: 22291.54 ❌
- **TP 15RR**: 21879.02 ❌
- **PnL**: -37.50 points (-1.0R)
- **MFE**: 13.26 points
- **MAE**: 44.37 points

### Trade #950 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 13:15:00
- **FVG 5m**: 22335.20 - 22342.59
- **Entrée**: 22344.12 @ 2025-06-11 15:17:00
- **Stop Loss**: 22217.74
- **Risk**: 126.39 points
- **TP 1RR**: 22470.51 ❌
- **TP 2RR**: 22596.90 ❌
- **TP 3RR**: 22723.28 ❌
- **TP 4RR**: 22849.67 ❌
- **TP 15RR**: 24239.92 ❌
- **PnL**: -126.39 points (-1.0R)
- **MFE**: 7.14 points
- **MAE**: 130.32 points

### Trade #951 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 13:30:00
- **FVG 5m**: 22335.20 - 22342.59
- **Entrée**: 22344.12 @ 2025-06-11 15:17:00
- **Stop Loss**: 22240.42
- **Risk**: 103.70 points
- **TP 1RR**: 22447.82 ❌
- **TP 2RR**: 22551.52 ❌
- **TP 3RR**: 22655.22 ❌
- **TP 4RR**: 22758.92 ❌
- **TP 15RR**: 23899.63 ❌
- **PnL**: -103.70 points (-1.0R)
- **MFE**: 7.14 points
- **MAE**: 115.02 points

### Trade #952 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-11 13:30:00
- **FVG 5m**: 22335.20 - 22342.59
- **Entrée**: 22344.12 @ 2025-06-11 15:17:00
- **Stop Loss**: 22240.42
- **Risk**: 103.70 points
- **TP 1RR**: 22447.82 ❌
- **TP 2RR**: 22551.52 ❌
- **TP 3RR**: 22655.22 ❌
- **TP 4RR**: 22758.92 ❌
- **TP 15RR**: 23899.63 ❌
- **PnL**: -103.70 points (-1.0R)
- **MFE**: 7.14 points
- **MAE**: 115.02 points

### Trade #953 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22138.72
- **Risk**: 61.32 points
- **TP 1RR**: 22261.35 ✅
- **TP 2RR**: 22322.66 ✅
- **TP 3RR**: 22383.98 ✅
- **TP 4RR**: 22445.29 ❌
- **TP 15RR**: 23119.76 ❌
- **PnL**: -61.32 points (-1.0R)
- **MFE**: 219.07 points
- **MAE**: 64.78 points

### Trade #954 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22138.72
- **Risk**: 61.32 points
- **TP 1RR**: 22261.35 ✅
- **TP 2RR**: 22322.66 ✅
- **TP 3RR**: 22383.98 ✅
- **TP 4RR**: 22445.29 ❌
- **TP 15RR**: 23119.76 ❌
- **PnL**: -61.32 points (-1.0R)
- **MFE**: 219.07 points
- **MAE**: 64.78 points

### Trade #955 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22138.72
- **Risk**: 61.32 points
- **TP 1RR**: 22261.35 ✅
- **TP 2RR**: 22322.66 ✅
- **TP 3RR**: 22383.98 ✅
- **TP 4RR**: 22445.29 ❌
- **TP 15RR**: 23119.76 ❌
- **PnL**: -61.32 points (-1.0R)
- **MFE**: 219.07 points
- **MAE**: 64.78 points

### Trade #956 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22138.72
- **Risk**: 61.32 points
- **TP 1RR**: 22261.35 ✅
- **TP 2RR**: 22322.66 ✅
- **TP 3RR**: 22383.98 ✅
- **TP 4RR**: 22445.29 ❌
- **TP 15RR**: 23119.76 ❌
- **PnL**: -61.32 points (-1.0R)
- **MFE**: 219.07 points
- **MAE**: 64.78 points

### Trade #957 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:00:00
- **FVG 5m**: 22190.34 - 22199.52
- **Entrée**: 22200.03 @ 2025-06-12 03:41:00
- **Stop Loss**: 22138.72
- **Risk**: 61.32 points
- **TP 1RR**: 22261.35 ✅
- **TP 2RR**: 22322.66 ✅
- **TP 3RR**: 22383.98 ✅
- **TP 4RR**: 22445.29 ❌
- **TP 15RR**: 23119.76 ❌
- **PnL**: -61.32 points (-1.0R)
- **MFE**: 219.07 points
- **MAE**: 64.78 points

### Trade #958 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 03:45:00
- **FVG 5m**: 22251.04 - 22263.28
- **Entrée**: 22264.81 @ 2025-06-12 04:34:00
- **Stop Loss**: 22188.42
- **Risk**: 76.39 points
- **TP 1RR**: 22341.20 ❌
- **TP 2RR**: 22417.58 ❌
- **TP 3RR**: 22493.97 ❌
- **TP 4RR**: 22570.36 ❌
- **TP 15RR**: 23410.61 ❌
- **PnL**: -76.39 points (-1.0R)
- **MFE**: 17.60 points
- **MAE**: 76.51 points

### Trade #959 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 09:00:00
- **FVG 5m**: 22343.10 - 22348.20
- **Entrée**: 22354.58 @ 2025-06-12 09:14:00
- **Stop Loss**: 22268.46
- **Risk**: 86.12 points
- **TP 1RR**: 22440.70 ❌
- **TP 2RR**: 22526.81 ❌
- **TP 3RR**: 22612.93 ❌
- **TP 4RR**: 22699.05 ❌
- **TP 15RR**: 23646.34 ❌
- **PnL**: -86.12 points (-1.0R)
- **MFE**: 64.52 points
- **MAE**: 133.89 points

### Trade #960 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 09:15:00
- **FVG 5m**: 22368.86 - 22375.75
- **Entrée**: 22380.85 @ 2025-06-12 09:37:00
- **Stop Loss**: 22331.42
- **Risk**: 49.43 points
- **TP 1RR**: 22430.27 ❌
- **TP 2RR**: 22479.70 ❌
- **TP 3RR**: 22529.12 ❌
- **TP 4RR**: 22578.55 ❌
- **TP 15RR**: 23122.23 ❌
- **PnL**: -49.43 points (-1.0R)
- **MFE**: 38.25 points
- **MAE**: 59.93 points

### Trade #961 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 13:30:00
- **FVG 5m**: 22376.26 - 22379.06
- **Entrée**: 22371.67 @ 2025-06-12 14:27:00
- **Stop Loss**: 22387.19
- **Risk**: 15.52 points
- **TP 1RR**: 22356.14 ✅
- **TP 2RR**: 22340.62 ✅
- **TP 3RR**: 22325.10 ❌
- **TP 4RR**: 22309.57 ❌
- **TP 15RR**: 22138.81 ❌
- **PnL**: -15.52 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 17.60 points

### Trade #962 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 19:15:00
- **FVG 5m**: 22008.76 - 22024.32
- **Entrée**: 21976.89 @ 2025-06-12 19:52:00
- **Stop Loss**: 22158.57
- **Risk**: 181.69 points
- **TP 1RR**: 21795.20 ❌
- **TP 2RR**: 21613.51 ❌
- **TP 3RR**: 21431.83 ❌
- **TP 4RR**: 21250.14 ❌
- **TP 15RR**: 19251.59 ❌
- **PnL**: -181.69 points (-1.0R)
- **MFE**: 74.21 points
- **MAE**: 184.89 points

### Trade #963 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 19:15:00
- **FVG 5m**: 22008.76 - 22024.32
- **Entrée**: 21976.89 @ 2025-06-12 19:52:00
- **Stop Loss**: 22158.57
- **Risk**: 181.69 points
- **TP 1RR**: 21795.20 ❌
- **TP 2RR**: 21613.51 ❌
- **TP 3RR**: 21431.83 ❌
- **TP 4RR**: 21250.14 ❌
- **TP 15RR**: 19251.59 ❌
- **PnL**: -181.69 points (-1.0R)
- **MFE**: 74.21 points
- **MAE**: 184.89 points

### Trade #964 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-12 19:15:00
- **FVG 5m**: 22008.76 - 22024.32
- **Entrée**: 21976.89 @ 2025-06-12 19:52:00
- **Stop Loss**: 22158.57
- **Risk**: 181.69 points
- **TP 1RR**: 21795.20 ❌
- **TP 2RR**: 21613.51 ❌
- **TP 3RR**: 21431.83 ❌
- **TP 4RR**: 21250.14 ❌
- **TP 15RR**: 19251.59 ❌
- **PnL**: -181.69 points (-1.0R)
- **MFE**: 74.21 points
- **MAE**: 184.89 points

### Trade #965 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-12 21:30:00
- **FVG 5m**: 21993.46 - 22003.92
- **Entrée**: 22006.21 @ 2025-06-12 22:51:00
- **Stop Loss**: 21891.72
- **Risk**: 114.49 points
- **TP 1RR**: 22120.71 ✅
- **TP 2RR**: 22235.20 ✅
- **TP 3RR**: 22349.69 ✅
- **TP 4RR**: 22464.18 ❌
- **TP 15RR**: 23723.59 ❌
- **PnL**: -114.49 points (-1.0R)
- **MFE**: 435.87 points
- **MAE**: 140.53 points

### Trade #966 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22109.50 - 22142.40
- **Entrée**: 22151.58 @ 2025-06-13 09:39:00
- **Stop Loss**: 22086.46
- **Risk**: 65.11 points
- **TP 1RR**: 22216.69 ✅
- **TP 2RR**: 22281.81 ✅
- **TP 3RR**: 22346.92 ❌
- **TP 4RR**: 22412.04 ❌
- **TP 15RR**: 23128.29 ❌
- **PnL**: -65.11 points (-1.0R)
- **MFE**: 142.56 points
- **MAE**: 84.41 points

### Trade #967 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22109.50 - 22142.40
- **Entrée**: 22151.58 @ 2025-06-13 09:39:00
- **Stop Loss**: 22086.46
- **Risk**: 65.11 points
- **TP 1RR**: 22216.69 ✅
- **TP 2RR**: 22281.81 ✅
- **TP 3RR**: 22346.92 ❌
- **TP 4RR**: 22412.04 ❌
- **TP 15RR**: 23128.29 ❌
- **PnL**: -65.11 points (-1.0R)
- **MFE**: 142.56 points
- **MAE**: 84.41 points

### Trade #968 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22109.50 - 22142.40
- **Entrée**: 22151.58 @ 2025-06-13 09:39:00
- **Stop Loss**: 22086.46
- **Risk**: 65.11 points
- **TP 1RR**: 22216.69 ✅
- **TP 2RR**: 22281.81 ✅
- **TP 3RR**: 22346.92 ❌
- **TP 4RR**: 22412.04 ❌
- **TP 15RR**: 23128.29 ❌
- **PnL**: -65.11 points (-1.0R)
- **MFE**: 142.56 points
- **MAE**: 84.41 points

### Trade #969 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-13 08:30:00
- **FVG 5m**: 22109.50 - 22142.40
- **Entrée**: 22151.58 @ 2025-06-13 09:39:00
- **Stop Loss**: 22086.46
- **Risk**: 65.11 points
- **TP 1RR**: 22216.69 ✅
- **TP 2RR**: 22281.81 ✅
- **TP 3RR**: 22346.92 ❌
- **TP 4RR**: 22412.04 ❌
- **TP 15RR**: 23128.29 ❌
- **PnL**: -65.11 points (-1.0R)
- **MFE**: 142.56 points
- **MAE**: 84.41 points

### Trade #970 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-13 09:00:00
- **FVG 5m**: 22135.77 - 22157.95
- **Entrée**: 22130.67 @ 2025-06-13 09:13:00
- **Stop Loss**: 22218.79
- **Risk**: 88.12 points
- **TP 1RR**: 22042.54 ❌
- **TP 2RR**: 21954.42 ❌
- **TP 3RR**: 21866.30 ❌
- **TP 4RR**: 21778.18 ❌
- **TP 15RR**: 20808.84 ❌
- **PnL**: -88.12 points (-1.0R)
- **MFE**: 79.06 points
- **MAE**: 112.47 points

### Trade #971 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-13 12:00:00
- **FVG 5m**: 22229.36 - 22242.62
- **Entrée**: 22225.28 @ 2025-06-13 12:11:00
- **Stop Loss**: 22284.87
- **Risk**: 59.59 points
- **TP 1RR**: 22165.69 ✅
- **TP 2RR**: 22106.10 ✅
- **TP 3RR**: 22046.51 ✅
- **TP 4RR**: 21986.91 ✅
- **TP 15RR**: 21331.40 ❌
- **PnL**: -59.59 points (-1.0R)
- **MFE**: 291.24 points
- **MAE**: 75.42 points

### Trade #972 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-15 17:00:00
- **FVG 5m**: 22054.16 - 22058.49
- **Entrée**: 22064.10 @ 2025-06-15 17:23:00
- **Stop Loss**: 21923.07
- **Risk**: 141.03 points
- **TP 1RR**: 22205.13 ✅
- **TP 2RR**: 22346.16 ✅
- **TP 3RR**: 22487.20 ❌
- **TP 4RR**: 22628.23 ❌
- **TP 15RR**: 24179.56 ❌
- **PnL**: -141.03 points (-1.0R)
- **MFE**: 377.98 points
- **MAE**: 152.98 points

### Trade #973 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-15 17:00:00
- **FVG 5m**: 22054.16 - 22058.49
- **Entrée**: 22064.10 @ 2025-06-15 17:23:00
- **Stop Loss**: 21923.07
- **Risk**: 141.03 points
- **TP 1RR**: 22205.13 ✅
- **TP 2RR**: 22346.16 ✅
- **TP 3RR**: 22487.20 ❌
- **TP 4RR**: 22628.23 ❌
- **TP 15RR**: 24179.56 ❌
- **PnL**: -141.03 points (-1.0R)
- **MFE**: 377.98 points
- **MAE**: 152.98 points

### Trade #974 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-15 21:15:00
- **FVG 5m**: 22132.20 - 22136.28
- **Entrée**: 22131.43 @ 2025-06-15 22:29:00
- **Stop Loss**: 22175.41
- **Risk**: 43.98 points
- **TP 1RR**: 22087.45 ❌
- **TP 2RR**: 22043.47 ❌
- **TP 3RR**: 21999.49 ❌
- **TP 4RR**: 21955.51 ❌
- **TP 15RR**: 21471.72 ❌
- **PnL**: -43.98 points (-1.0R)
- **MFE**: 25.76 points
- **MAE**: 44.54 points

### Trade #975 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-16 08:45:00
- **FVG 5m**: 22422.90 - 22426.68
- **Entrée**: 22432.24 @ 2025-06-16 10:17:00
- **Stop Loss**: 22264.82
- **Risk**: 167.42 points
- **TP 1RR**: 22599.66 ❌
- **TP 2RR**: 22767.08 ❌
- **TP 3RR**: 22934.50 ❌
- **TP 4RR**: 23101.92 ❌
- **TP 15RR**: 24943.55 ❌
- **PnL**: -167.42 points (-1.0R)
- **MFE**: 9.85 points
- **MAE**: 193.65 points

### Trade #976 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-16 09:45:00
- **FVG 5m**: 22423.91 - 22426.68
- **Entrée**: 22410.52 @ 2025-06-16 10:26:00
- **Stop Loss**: 22436.63
- **Risk**: 26.11 points
- **TP 1RR**: 22384.42 ✅
- **TP 2RR**: 22358.31 ✅
- **TP 3RR**: 22332.20 ✅
- **TP 4RR**: 22306.09 ✅
- **TP 15RR**: 22018.89 ✅
- **PnL**: 391.63 points (15.0R)
- **MFE**: 404.72 points
- **MAE**: 21.21 points

### Trade #977 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-16 10:15:00
- **FVG 5m**: 22423.91 - 22426.68
- **Entrée**: 22410.52 @ 2025-06-16 10:26:00
- **Stop Loss**: 22453.30
- **Risk**: 42.78 points
- **TP 1RR**: 22367.74 ✅
- **TP 2RR**: 22324.96 ✅
- **TP 3RR**: 22282.18 ✅
- **TP 4RR**: 22239.40 ✅
- **TP 15RR**: 21768.82 ❌
- **PnL**: -42.78 points (-1.0R)
- **MFE**: 630.18 points
- **MAE**: 44.69 points

### Trade #978 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-16 18:30:00
- **FVG 5m**: 22270.65 - 22275.20
- **Entrée**: 22256.51 @ 2025-06-16 18:48:00
- **Stop Loss**: 22317.40
- **Risk**: 60.89 points
- **TP 1RR**: 22195.62 ❌
- **TP 2RR**: 22134.73 ❌
- **TP 3RR**: 22073.84 ❌
- **TP 4RR**: 22012.95 ❌
- **TP 15RR**: 21343.15 ❌
- **PnL**: -60.89 points (-1.0R)
- **MFE**: 31.05 points
- **MAE**: 64.63 points

### Trade #979 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-16 22:00:00
- **FVG 5m**: 22279.74 - 22289.08
- **Entrée**: 22277.47 @ 2025-06-16 23:33:00
- **Stop Loss**: 22344.43
- **Risk**: 66.96 points
- **TP 1RR**: 22210.51 ❌
- **TP 2RR**: 22143.54 ❌
- **TP 3RR**: 22076.58 ❌
- **TP 4RR**: 22009.61 ❌
- **TP 15RR**: 21273.01 ❌
- **PnL**: -66.96 points (-1.0R)
- **MFE**: 63.62 points
- **MAE**: 71.96 points

### Trade #980 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 02:15:00
- **FVG 5m**: 22256.26 - 22259.04
- **Entrée**: 22263.84 @ 2025-06-17 04:44:00
- **Stop Loss**: 22210.81
- **Risk**: 53.02 points
- **TP 1RR**: 22316.86 ✅
- **TP 2RR**: 22369.88 ❌
- **TP 3RR**: 22422.90 ❌
- **TP 4RR**: 22475.92 ❌
- **TP 15RR**: 23059.17 ❌
- **PnL**: -53.02 points (-1.0R)
- **MFE**: 90.39 points
- **MAE**: 56.30 points

### Trade #981 - ❌ PERDANT

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

### Trade #982 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 05:45:00
- **FVG 5m**: 22273.18 - 22284.79
- **Entrée**: 22285.80 @ 2025-06-17 06:56:00
- **Stop Loss**: 22202.74
- **Risk**: 83.06 points
- **TP 1RR**: 22368.86 ❌
- **TP 2RR**: 22451.93 ❌
- **TP 3RR**: 22534.99 ❌
- **TP 4RR**: 22618.05 ❌
- **TP 15RR**: 23531.74 ❌
- **PnL**: -83.06 points (-1.0R)
- **MFE**: 68.42 points
- **MAE**: 96.19 points

### Trade #983 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 05:45:00
- **FVG 5m**: 22273.18 - 22284.79
- **Entrée**: 22285.80 @ 2025-06-17 06:56:00
- **Stop Loss**: 22202.74
- **Risk**: 83.06 points
- **TP 1RR**: 22368.86 ❌
- **TP 2RR**: 22451.93 ❌
- **TP 3RR**: 22534.99 ❌
- **TP 4RR**: 22618.05 ❌
- **TP 15RR**: 23531.74 ❌
- **PnL**: -83.06 points (-1.0R)
- **MFE**: 68.42 points
- **MAE**: 96.19 points

### Trade #984 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-17 07:30:00
- **FVG 5m**: 22278.98 - 22293.63
- **Entrée**: 22275.95 @ 2025-06-17 07:49:00
- **Stop Loss**: 22331.05
- **Risk**: 55.09 points
- **TP 1RR**: 22220.86 ❌
- **TP 2RR**: 22165.77 ❌
- **TP 3RR**: 22110.68 ❌
- **TP 4RR**: 22055.59 ❌
- **TP 15RR**: 21449.59 ❌
- **PnL**: -55.09 points (-1.0R)
- **MFE**: 31.81 points
- **MAE**: 58.07 points

### Trade #985 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-17 09:15:00
- **FVG 5m**: 22314.08 - 22318.12
- **Entrée**: 22312.56 @ 2025-06-17 09:39:00
- **Stop Loss**: 22363.88
- **Risk**: 51.32 points
- **TP 1RR**: 22261.24 ✅
- **TP 2RR**: 22209.92 ✅
- **TP 3RR**: 22158.60 ✅
- **TP 4RR**: 22107.28 ✅
- **TP 15RR**: 21542.76 ❌
- **PnL**: -51.32 points (-1.0R)
- **MFE**: 532.22 points
- **MAE**: 56.81 points

### Trade #986 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-17 09:15:00
- **FVG 5m**: 22314.08 - 22318.12
- **Entrée**: 22312.56 @ 2025-06-17 09:39:00
- **Stop Loss**: 22363.88
- **Risk**: 51.32 points
- **TP 1RR**: 22261.24 ✅
- **TP 2RR**: 22209.92 ✅
- **TP 3RR**: 22158.60 ✅
- **TP 4RR**: 22107.28 ✅
- **TP 15RR**: 21542.76 ❌
- **PnL**: -51.32 points (-1.0R)
- **MFE**: 532.22 points
- **MAE**: 56.81 points

### Trade #987 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 12:30:00
- **FVG 5m**: 22194.15 - 22196.68
- **Entrée**: 22199.20 @ 2025-06-17 14:21:00
- **Stop Loss**: 22196.43
- **Risk**: 2.77 points
- **TP 1RR**: 22201.97 ✅
- **TP 2RR**: 22204.75 ✅
- **TP 3RR**: 22207.52 ✅
- **TP 4RR**: 22210.29 ✅
- **TP 15RR**: 22240.78 ❌
- **PnL**: -2.77 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 8.84 points

### Trade #988 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 12:45:00
- **FVG 5m**: 22194.15 - 22196.68
- **Entrée**: 22199.20 @ 2025-06-17 14:21:00
- **Stop Loss**: 22146.97
- **Risk**: 52.23 points
- **TP 1RR**: 22251.43 ❌
- **TP 2RR**: 22303.67 ❌
- **TP 3RR**: 22355.90 ❌
- **TP 4RR**: 22408.13 ❌
- **TP 15RR**: 22982.69 ❌
- **PnL**: -52.23 points (-1.0R)
- **MFE**: 23.73 points
- **MAE**: 63.37 points

### Trade #989 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-17 17:30:00
- **FVG 5m**: 22182.54 - 22192.38
- **Entrée**: 22195.92 @ 2025-06-17 19:36:00
- **Stop Loss**: 22078.58
- **Risk**: 117.34 points
- **TP 1RR**: 22313.26 ✅
- **TP 2RR**: 22430.59 ❌
- **TP 3RR**: 22547.93 ❌
- **TP 4RR**: 22665.27 ❌
- **TP 15RR**: 23955.98 ❌
- **PnL**: -117.34 points (-1.0R)
- **MFE**: 120.68 points
- **MAE**: 128.51 points

### Trade #990 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 01:00:00
- **FVG 5m**: 22235.81 - 22241.87
- **Entrée**: 22243.89 @ 2025-06-18 03:04:00
- **Stop Loss**: 22188.10
- **Risk**: 55.79 points
- **TP 1RR**: 22299.68 ❌
- **TP 2RR**: 22355.47 ❌
- **TP 3RR**: 22411.25 ❌
- **TP 4RR**: 22467.04 ❌
- **TP 15RR**: 23080.71 ❌
- **PnL**: -55.79 points (-1.0R)
- **MFE**: 40.90 points
- **MAE**: 60.59 points

### Trade #991 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-18 07:15:00
- **FVG 5m**: 22213.34 - 22223.19
- **Entrée**: 22210.82 @ 2025-06-18 08:29:00
- **Stop Loss**: 22248.44
- **Risk**: 37.63 points
- **TP 1RR**: 22173.19 ✅
- **TP 2RR**: 22135.56 ❌
- **TP 3RR**: 22097.93 ❌
- **TP 4RR**: 22060.30 ❌
- **TP 15RR**: 21646.39 ❌
- **PnL**: -37.63 points (-1.0R)
- **MFE**: 67.41 points
- **MAE**: 41.91 points

### Trade #992 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 08:30:00
- **FVG 5m**: 22184.31 - 22188.85
- **Entrée**: 22192.38 @ 2025-06-18 08:41:00
- **Stop Loss**: 22132.33
- **Risk**: 60.05 points
- **TP 1RR**: 22252.44 ✅
- **TP 2RR**: 22312.49 ✅
- **TP 3RR**: 22372.54 ❌
- **TP 4RR**: 22432.59 ❌
- **TP 15RR**: 23093.17 ❌
- **PnL**: -60.05 points (-1.0R)
- **MFE**: 124.22 points
- **MAE**: 66.40 points

### Trade #993 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 08:30:00
- **FVG 5m**: 22184.31 - 22188.85
- **Entrée**: 22192.38 @ 2025-06-18 08:41:00
- **Stop Loss**: 22132.33
- **Risk**: 60.05 points
- **TP 1RR**: 22252.44 ✅
- **TP 2RR**: 22312.49 ✅
- **TP 3RR**: 22372.54 ❌
- **TP 4RR**: 22432.59 ❌
- **TP 15RR**: 23093.17 ❌
- **PnL**: -60.05 points (-1.0R)
- **MFE**: 124.22 points
- **MAE**: 66.40 points

### Trade #994 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-18 10:00:00
- **FVG 5m**: 22218.39 - 22238.08
- **Entrée**: 22216.62 @ 2025-06-18 12:22:00
- **Stop Loss**: 22315.64
- **Risk**: 99.01 points
- **TP 1RR**: 22117.61 ✅
- **TP 2RR**: 22018.59 ✅
- **TP 3RR**: 21919.58 ✅
- **TP 4RR**: 21820.57 ❌
- **TP 15RR**: 20731.41 ❌
- **PnL**: -99.01 points (-1.0R)
- **MFE**: 351.95 points
- **MAE**: 105.28 points

### Trade #995 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-18 11:15:00
- **FVG 5m**: 22218.39 - 22238.08
- **Entrée**: 22216.62 @ 2025-06-18 12:22:00
- **Stop Loss**: 22287.35
- **Risk**: 70.72 points
- **TP 1RR**: 22145.90 ❌
- **TP 2RR**: 22075.18 ❌
- **TP 3RR**: 22004.46 ❌
- **TP 4RR**: 21933.73 ❌
- **TP 15RR**: 21155.79 ❌
- **PnL**: -70.72 points (-1.0R)
- **MFE**: 59.84 points
- **MAE**: 84.58 points

### Trade #996 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 14:00:00
- **FVG 5m**: 22179.00 - 22182.54
- **Entrée**: 22184.81 @ 2025-06-18 15:38:00
- **Stop Loss**: 22087.92
- **Risk**: 96.89 points
- **TP 1RR**: 22281.70 ❌
- **TP 2RR**: 22378.59 ❌
- **TP 3RR**: 22475.48 ❌
- **TP 4RR**: 22572.38 ❌
- **TP 15RR**: 23638.18 ❌
- **PnL**: -96.89 points (-1.0R)
- **MFE**: 10.10 points
- **MAE**: 117.40 points

### Trade #997 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 19:15:00
- **FVG 5m**: 22103.26 - 22106.04
- **Entrée**: 22109.83 @ 2025-06-18 19:28:00
- **Stop Loss**: 22053.35
- **Risk**: 56.48 points
- **TP 1RR**: 22166.30 ❌
- **TP 2RR**: 22222.78 ❌
- **TP 3RR**: 22279.26 ❌
- **TP 4RR**: 22335.74 ❌
- **TP 15RR**: 22956.99 ❌
- **PnL**: -56.48 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 86.09 points

### Trade #998 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-18 19:15:00
- **FVG 5m**: 22103.26 - 22106.04
- **Entrée**: 22109.83 @ 2025-06-18 19:28:00
- **Stop Loss**: 22053.35
- **Risk**: 56.48 points
- **TP 1RR**: 22166.30 ❌
- **TP 2RR**: 22222.78 ❌
- **TP 3RR**: 22279.26 ❌
- **TP 4RR**: 22335.74 ❌
- **TP 15RR**: 22956.99 ❌
- **PnL**: -56.48 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 86.09 points

### Trade #999 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-19 08:45:00
- **FVG 5m**: 21919.71 - 21921.98
- **Entrée**: 21919.46 @ 2025-06-19 10:34:00
- **Stop Loss**: 21953.91
- **Risk**: 34.45 points
- **TP 1RR**: 21885.01 ❌
- **TP 2RR**: 21850.55 ❌
- **TP 3RR**: 21816.10 ❌
- **TP 4RR**: 21781.65 ❌
- **TP 15RR**: 21402.68 ❌
- **PnL**: -34.45 points (-1.0R)
- **MFE**: 29.29 points
- **MAE**: 37.62 points

### Trade #1000 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 09:00:00
- **FVG 5m**: 21923.25 - 21931.58
- **Entrée**: 21932.08 @ 2025-06-19 09:54:00
- **Stop Loss**: 21875.19
- **Risk**: 56.89 points
- **TP 1RR**: 21988.98 ✅
- **TP 2RR**: 22045.87 ✅
- **TP 3RR**: 22102.76 ✅
- **TP 4RR**: 22159.66 ✅
- **TP 15RR**: 22785.49 ❌
- **PnL**: -56.89 points (-1.0R)
- **MFE**: 417.60 points
- **MAE**: 151.74 points

### Trade #1001 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 09:00:00
- **FVG 5m**: 21923.25 - 21931.58
- **Entrée**: 21932.08 @ 2025-06-19 09:54:00
- **Stop Loss**: 21875.19
- **Risk**: 56.89 points
- **TP 1RR**: 21988.98 ✅
- **TP 2RR**: 22045.87 ✅
- **TP 3RR**: 22102.76 ✅
- **TP 4RR**: 22159.66 ✅
- **TP 15RR**: 22785.49 ❌
- **PnL**: -56.89 points (-1.0R)
- **MFE**: 417.60 points
- **MAE**: 151.74 points

### Trade #1002 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 09:45:00
- **FVG 5m**: 21919.71 - 21928.30
- **Entrée**: 21928.80 @ 2025-06-19 10:44:00
- **Stop Loss**: 21884.02
- **Risk**: 44.78 points
- **TP 1RR**: 21973.58 ✅
- **TP 2RR**: 22018.36 ✅
- **TP 3RR**: 22063.14 ✅
- **TP 4RR**: 22107.92 ✅
- **TP 15RR**: 22600.49 ❌
- **PnL**: -44.78 points (-1.0R)
- **MFE**: 420.88 points
- **MAE**: 148.46 points

### Trade #1003 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 17:00:00
- **FVG 5m**: 22067.41 - 22082.05
- **Entrée**: 22087.61 @ 2025-06-19 17:33:00
- **Stop Loss**: 21950.14
- **Risk**: 137.47 points
- **TP 1RR**: 22225.08 ✅
- **TP 2RR**: 22362.55 ❌
- **TP 3RR**: 22500.02 ❌
- **TP 4RR**: 22637.49 ❌
- **TP 15RR**: 24149.67 ❌
- **PnL**: -137.47 points (-1.0R)
- **MFE**: 262.07 points
- **MAE**: 307.26 points

### Trade #1004 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-19 17:30:00
- **FVG 5m**: 22104.78 - 22107.55
- **Entrée**: 22099.22 @ 2025-06-19 18:04:00
- **Stop Loss**: 22144.12
- **Risk**: 44.90 points
- **TP 1RR**: 22054.32 ❌
- **TP 2RR**: 22009.42 ❌
- **TP 3RR**: 21964.53 ❌
- **TP 4RR**: 21919.63 ❌
- **TP 15RR**: 21425.75 ❌
- **PnL**: -44.90 points (-1.0R)
- **MFE**: 12.37 points
- **MAE**: 45.95 points

### Trade #1005 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-19 19:00:00
- **FVG 5m**: 22080.03 - 22088.62
- **Entrée**: 22090.64 @ 2025-06-19 20:16:00
- **Stop Loss**: 22086.15
- **Risk**: 4.48 points
- **TP 1RR**: 22095.12 ✅
- **TP 2RR**: 22099.61 ✅
- **TP 3RR**: 22104.09 ❌
- **TP 4RR**: 22108.57 ❌
- **TP 15RR**: 22157.90 ❌
- **PnL**: -4.48 points (-1.0R)
- **MFE**: 11.11 points
- **MAE**: 9.85 points

### Trade #1006 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 03:15:00
- **FVG 5m**: 22132.04 - 22137.85
- **Entrée**: 22130.28 @ 2025-06-20 03:28:00
- **Stop Loss**: 22174.68
- **Risk**: 44.41 points
- **TP 1RR**: 22085.87 ✅
- **TP 2RR**: 22041.46 ❌
- **TP 3RR**: 21997.05 ❌
- **TP 4RR**: 21952.64 ❌
- **TP 15RR**: 21464.15 ❌
- **PnL**: -44.41 points (-1.0R)
- **MFE**: 54.79 points
- **MAE**: 64.63 points

### Trade #1007 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 04:00:00
- **FVG 5m**: 22104.27 - 22109.32
- **Entrée**: 22110.08 @ 2025-06-20 04:14:00
- **Stop Loss**: 22069.25
- **Risk**: 40.83 points
- **TP 1RR**: 22150.91 ✅
- **TP 2RR**: 22191.74 ✅
- **TP 3RR**: 22232.57 ✅
- **TP 4RR**: 22273.41 ✅
- **TP 15RR**: 22722.56 ❌
- **PnL**: -40.83 points (-1.0R)
- **MFE**: 239.60 points
- **MAE**: 44.18 points

### Trade #1008 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 04:00:00
- **FVG 5m**: 22104.27 - 22109.32
- **Entrée**: 22110.08 @ 2025-06-20 04:14:00
- **Stop Loss**: 22069.25
- **Risk**: 40.83 points
- **TP 1RR**: 22150.91 ✅
- **TP 2RR**: 22191.74 ✅
- **TP 3RR**: 22232.57 ✅
- **TP 4RR**: 22273.41 ✅
- **TP 15RR**: 22722.56 ❌
- **PnL**: -40.83 points (-1.0R)
- **MFE**: 239.60 points
- **MAE**: 44.18 points

### Trade #1009 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 08:15:00
- **FVG 5m**: 22286.56 - 22317.87
- **Entrée**: 22284.29 @ 2025-06-20 08:49:00
- **Stop Loss**: 22333.07
- **Risk**: 48.78 points
- **TP 1RR**: 22235.51 ✅
- **TP 2RR**: 22186.73 ✅
- **TP 3RR**: 22137.95 ✅
- **TP 4RR**: 22089.17 ✅
- **TP 15RR**: 21552.59 ❌
- **PnL**: -48.78 points (-1.0R)
- **MFE**: 503.94 points
- **MAE**: 85.08 points

### Trade #1010 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 08:45:00
- **FVG 5m**: 22244.90 - 22250.71
- **Entrée**: 22243.39 @ 2025-06-20 08:58:00
- **Stop Loss**: 22355.30
- **Risk**: 111.91 points
- **TP 1RR**: 22131.48 ✅
- **TP 2RR**: 22019.57 ✅
- **TP 3RR**: 21907.66 ✅
- **TP 4RR**: 21795.75 ✅
- **TP 15RR**: 20564.74 ❌
- **PnL**: -111.91 points (-1.0R)
- **MFE**: 463.04 points
- **MAE**: 125.99 points

### Trade #1011 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:15:00
- **FVG 5m**: 22097.20 - 22141.89
- **Entrée**: 22069.43 @ 2025-06-20 09:45:00
- **Stop Loss**: 22232.78
- **Risk**: 163.35 points
- **TP 1RR**: 21906.08 ✅
- **TP 2RR**: 21742.72 ❌
- **TP 3RR**: 21579.37 ❌
- **TP 4RR**: 21416.01 ❌
- **TP 15RR**: 19619.12 ❌
- **PnL**: -163.35 points (-1.0R)
- **MFE**: 289.08 points
- **MAE**: 166.63 points

### Trade #1012 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:15:00
- **FVG 5m**: 22097.20 - 22141.89
- **Entrée**: 22069.43 @ 2025-06-20 09:45:00
- **Stop Loss**: 22232.78
- **Risk**: 163.35 points
- **TP 1RR**: 21906.08 ✅
- **TP 2RR**: 21742.72 ❌
- **TP 3RR**: 21579.37 ❌
- **TP 4RR**: 21416.01 ❌
- **TP 15RR**: 19619.12 ❌
- **PnL**: -163.35 points (-1.0R)
- **MFE**: 289.08 points
- **MAE**: 166.63 points

### Trade #1013 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:15:00
- **FVG 5m**: 22097.20 - 22141.89
- **Entrée**: 22069.43 @ 2025-06-20 09:45:00
- **Stop Loss**: 22232.78
- **Risk**: 163.35 points
- **TP 1RR**: 21906.08 ✅
- **TP 2RR**: 21742.72 ❌
- **TP 3RR**: 21579.37 ❌
- **TP 4RR**: 21416.01 ❌
- **TP 15RR**: 19619.12 ❌
- **PnL**: -163.35 points (-1.0R)
- **MFE**: 289.08 points
- **MAE**: 166.63 points

### Trade #1014 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-20 09:45:00
- **FVG 5m**: 22081.04 - 22112.60
- **Entrée**: 22073.22 @ 2025-06-20 10:54:00
- **Stop Loss**: 22108.25
- **Risk**: 35.03 points
- **TP 1RR**: 22038.18 ❌
- **TP 2RR**: 22003.15 ❌
- **TP 3RR**: 21968.11 ❌
- **TP 4RR**: 21933.08 ❌
- **TP 15RR**: 21547.71 ❌
- **PnL**: -35.03 points (-1.0R)
- **MFE**: 23.73 points
- **MAE**: 37.11 points

### Trade #1015 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 10:00:00
- **FVG 5m**: 22038.37 - 22062.86
- **Entrée**: 22069.68 @ 2025-06-20 10:14:00
- **Stop Loss**: 21980.67
- **Risk**: 89.01 points
- **TP 1RR**: 22158.69 ❌
- **TP 2RR**: 22247.70 ❌
- **TP 3RR**: 22336.71 ❌
- **TP 4RR**: 22425.73 ❌
- **TP 15RR**: 23404.85 ❌
- **PnL**: -89.01 points (-1.0R)
- **MFE**: 69.43 points
- **MAE**: 89.12 points

### Trade #1016 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 11:15:00
- **FVG 5m**: 22028.28 - 22038.88
- **Entrée**: 22041.66 @ 2025-06-20 12:53:00
- **Stop Loss**: 22038.46
- **Risk**: 3.20 points
- **TP 1RR**: 22044.85 ❌
- **TP 2RR**: 22048.05 ❌
- **TP 3RR**: 22051.25 ❌
- **TP 4RR**: 22054.45 ❌
- **TP 15RR**: 22089.63 ❌
- **PnL**: -3.20 points (-1.0R)
- **MFE**: 2.78 points
- **MAE**: 6.82 points

### Trade #1017 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-20 12:30:00
- **FVG 5m**: 22028.28 - 22038.88
- **Entrée**: 22041.66 @ 2025-06-20 12:53:00
- **Stop Loss**: 21969.57
- **Risk**: 72.09 points
- **TP 1RR**: 22113.75 ✅
- **TP 2RR**: 22185.84 ❌
- **TP 3RR**: 22257.93 ❌
- **TP 4RR**: 22330.01 ❌
- **TP 15RR**: 23123.00 ❌
- **PnL**: -72.09 points (-1.0R)
- **MFE**: 86.60 points
- **MAE**: 261.31 points

### Trade #1018 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-22 17:00:00
- **FVG 5m**: 21943.19 - 21953.04
- **Entrée**: 21955.31 @ 2025-06-22 17:28:00
- **Stop Loss**: 21769.45
- **Risk**: 185.86 points
- **TP 1RR**: 22141.17 ✅
- **TP 2RR**: 22327.02 ✅
- **TP 3RR**: 22512.88 ✅
- **TP 4RR**: 22698.73 ✅
- **TP 15RR**: 24743.15 ✅
- **PnL**: 2787.84 points (15.0R)
- **MFE**: 2792.94 points
- **MAE**: 33.33 points

### Trade #1019 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-22 17:00:00
- **FVG 5m**: 21943.19 - 21953.04
- **Entrée**: 21955.31 @ 2025-06-22 17:28:00
- **Stop Loss**: 21769.45
- **Risk**: 185.86 points
- **TP 1RR**: 22141.17 ✅
- **TP 2RR**: 22327.02 ✅
- **TP 3RR**: 22512.88 ✅
- **TP 4RR**: 22698.73 ✅
- **TP 15RR**: 24743.15 ✅
- **PnL**: 2787.84 points (15.0R)
- **MFE**: 2792.94 points
- **MAE**: 33.33 points

### Trade #1020 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-22 17:00:00
- **FVG 5m**: 21943.19 - 21953.04
- **Entrée**: 21955.31 @ 2025-06-22 17:28:00
- **Stop Loss**: 21769.45
- **Risk**: 185.86 points
- **TP 1RR**: 22141.17 ✅
- **TP 2RR**: 22327.02 ✅
- **TP 3RR**: 22512.88 ✅
- **TP 4RR**: 22698.73 ✅
- **TP 15RR**: 24743.15 ✅
- **PnL**: 2787.84 points (15.0R)
- **MFE**: 2792.94 points
- **MAE**: 33.33 points

### Trade #1021 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-22 17:15:00
- **FVG 5m**: 21935.36 - 21940.16
- **Entrée**: 21935.11 @ 2025-06-22 19:18:00
- **Stop Loss**: 21978.16
- **Risk**: 43.05 points
- **TP 1RR**: 21892.06 ❌
- **TP 2RR**: 21849.02 ❌
- **TP 3RR**: 21805.97 ❌
- **TP 4RR**: 21762.92 ❌
- **TP 15RR**: 21289.39 ❌
- **PnL**: -43.05 points (-1.0R)
- **MFE**: 13.13 points
- **MAE**: 43.68 points

### Trade #1022 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 04:15:00
- **FVG 5m**: 22074.98 - 22083.32
- **Entrée**: 22066.90 @ 2025-06-23 05:41:00
- **Stop Loss**: 22162.56
- **Risk**: 95.66 points
- **TP 1RR**: 21971.25 ❌
- **TP 2RR**: 21875.59 ❌
- **TP 3RR**: 21779.94 ❌
- **TP 4RR**: 21684.28 ❌
- **TP 15RR**: 20632.08 ❌
- **PnL**: -95.66 points (-1.0R)
- **MFE**: 92.91 points
- **MAE**: 106.80 points

### Trade #1023 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 04:15:00
- **FVG 5m**: 22074.98 - 22083.32
- **Entrée**: 22066.90 @ 2025-06-23 05:41:00
- **Stop Loss**: 22162.56
- **Risk**: 95.66 points
- **TP 1RR**: 21971.25 ❌
- **TP 2RR**: 21875.59 ❌
- **TP 3RR**: 21779.94 ❌
- **TP 4RR**: 21684.28 ❌
- **TP 15RR**: 20632.08 ❌
- **PnL**: -95.66 points (-1.0R)
- **MFE**: 92.91 points
- **MAE**: 106.80 points

### Trade #1024 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 08:30:00
- **FVG 5m**: 22102.50 - 22109.83
- **Entrée**: 22112.60 @ 2025-06-23 08:47:00
- **Stop Loss**: 21963.01
- **Risk**: 149.60 points
- **TP 1RR**: 22262.20 ❌
- **TP 2RR**: 22411.80 ❌
- **TP 3RR**: 22561.39 ❌
- **TP 4RR**: 22710.99 ❌
- **TP 15RR**: 24356.55 ❌
- **PnL**: -149.60 points (-1.0R)
- **MFE**: 123.46 points
- **MAE**: 159.06 points

### Trade #1025 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-23 10:45:00
- **FVG 5m**: 22107.30 - 22124.97
- **Entrée**: 22106.04 @ 2025-06-23 11:24:00
- **Stop Loss**: 22194.13
- **Risk**: 88.10 points
- **TP 1RR**: 22017.94 ✅
- **TP 2RR**: 21929.84 ❌
- **TP 3RR**: 21841.75 ❌
- **TP 4RR**: 21753.65 ❌
- **TP 15RR**: 20784.59 ❌
- **PnL**: -88.10 points (-1.0R)
- **MFE**: 152.50 points
- **MAE**: 94.43 points

### Trade #1026 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 11:30:00
- **FVG 5m**: 22033.07 - 22058.83
- **Entrée**: 22069.68 @ 2025-06-23 11:41:00
- **Stop Loss**: 21942.57
- **Risk**: 127.12 points
- **TP 1RR**: 22196.80 ✅
- **TP 2RR**: 22323.91 ✅
- **TP 3RR**: 22451.03 ✅
- **TP 4RR**: 22578.14 ✅
- **TP 15RR**: 23976.42 ✅
- **PnL**: 1906.74 points (15.0R)
- **MFE**: 1909.73 points
- **MAE**: 32.06 points

### Trade #1027 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 11:30:00
- **FVG 5m**: 22033.07 - 22058.83
- **Entrée**: 22069.68 @ 2025-06-23 11:41:00
- **Stop Loss**: 21942.57
- **Risk**: 127.12 points
- **TP 1RR**: 22196.80 ✅
- **TP 2RR**: 22323.91 ✅
- **TP 3RR**: 22451.03 ✅
- **TP 4RR**: 22578.14 ✅
- **TP 15RR**: 23976.42 ✅
- **PnL**: 1906.74 points (15.0R)
- **MFE**: 1909.73 points
- **MAE**: 32.06 points

### Trade #1028 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 17:00:00
- **FVG 5m**: 22382.75 - 22390.33
- **Entrée**: 22394.11 @ 2025-06-23 17:14:00
- **Stop Loss**: 22273.14
- **Risk**: 120.97 points
- **TP 1RR**: 22515.08 ✅
- **TP 2RR**: 22636.05 ✅
- **TP 3RR**: 22757.02 ✅
- **TP 4RR**: 22877.99 ✅
- **TP 15RR**: 24208.65 ✅
- **PnL**: 1814.54 points (15.0R)
- **MFE**: 1816.06 points
- **MAE**: 6.56 points

### Trade #1029 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-23 17:00:00
- **FVG 5m**: 22382.75 - 22390.33
- **Entrée**: 22394.11 @ 2025-06-23 17:14:00
- **Stop Loss**: 22273.14
- **Risk**: 120.97 points
- **TP 1RR**: 22515.08 ✅
- **TP 2RR**: 22636.05 ✅
- **TP 3RR**: 22757.02 ✅
- **TP 4RR**: 22877.99 ✅
- **TP 15RR**: 24208.65 ✅
- **PnL**: 1814.54 points (15.0R)
- **MFE**: 1816.06 points
- **MAE**: 6.56 points

### Trade #1030 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-24 02:15:00
- **FVG 5m**: 22551.41 - 22567.56
- **Entrée**: 22546.10 @ 2025-06-24 02:29:00
- **Stop Loss**: 22600.82
- **Risk**: 54.72 points
- **TP 1RR**: 22491.38 ✅
- **TP 2RR**: 22436.66 ❌
- **TP 3RR**: 22381.94 ❌
- **TP 4RR**: 22327.22 ❌
- **TP 15RR**: 21725.29 ❌
- **PnL**: -54.72 points (-1.0R)
- **MFE**: 73.98 points
- **MAE**: 56.81 points

### Trade #1031 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-24 05:00:00
- **FVG 5m**: 22510.25 - 22523.13
- **Entrée**: 22506.46 @ 2025-06-24 07:13:00
- **Stop Loss**: 22554.60
- **Risk**: 48.13 points
- **TP 1RR**: 22458.33 ❌
- **TP 2RR**: 22410.20 ❌
- **TP 3RR**: 22362.07 ❌
- **TP 4RR**: 22313.93 ❌
- **TP 15RR**: 21784.47 ❌
- **PnL**: -48.13 points (-1.0R)
- **MFE**: 27.52 points
- **MAE**: 48.22 points

### Trade #1032 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-24 06:00:00
- **FVG 5m**: 22510.25 - 22523.13
- **Entrée**: 22506.46 @ 2025-06-24 07:13:00
- **Stop Loss**: 22528.83
- **Risk**: 22.37 points
- **TP 1RR**: 22484.10 ✅
- **TP 2RR**: 22461.73 ❌
- **TP 3RR**: 22439.36 ❌
- **TP 4RR**: 22416.99 ❌
- **TP 15RR**: 22170.95 ❌
- **PnL**: -22.37 points (-1.0R)
- **MFE**: 27.52 points
- **MAE**: 25.50 points

### Trade #1033 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-24 11:30:00
- **FVG 5m**: 22625.63 - 22628.92
- **Entrée**: 22630.68 @ 2025-06-24 12:42:00
- **Stop Loss**: 22598.68
- **Risk**: 32.01 points
- **TP 1RR**: 22662.69 ✅
- **TP 2RR**: 22694.70 ✅
- **TP 3RR**: 22726.71 ✅
- **TP 4RR**: 22758.72 ✅
- **TP 15RR**: 23110.80 ✅
- **PnL**: 480.12 points (15.0R)
- **MFE**: 480.97 points
- **MAE**: 24.49 points

### Trade #1034 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-25 04:15:00
- **FVG 5m**: 22657.19 - 22659.47
- **Entrée**: 22654.67 @ 2025-06-25 04:28:00
- **Stop Loss**: 22687.97
- **Risk**: 33.30 points
- **TP 1RR**: 22621.36 ❌
- **TP 2RR**: 22588.06 ❌
- **TP 3RR**: 22554.76 ❌
- **TP 4RR**: 22521.45 ❌
- **TP 15RR**: 22155.11 ❌
- **PnL**: -33.30 points (-1.0R)
- **MFE**: 19.19 points
- **MAE**: 36.36 points

### Trade #1035 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-25 04:15:00
- **FVG 5m**: 22657.19 - 22659.47
- **Entrée**: 22654.67 @ 2025-06-25 04:28:00
- **Stop Loss**: 22687.97
- **Risk**: 33.30 points
- **TP 1RR**: 22621.36 ❌
- **TP 2RR**: 22588.06 ❌
- **TP 3RR**: 22554.76 ❌
- **TP 4RR**: 22521.45 ❌
- **TP 15RR**: 22155.11 ❌
- **PnL**: -33.30 points (-1.0R)
- **MFE**: 19.19 points
- **MAE**: 36.36 points

### Trade #1036 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-25 10:30:00
- **FVG 5m**: 22655.68 - 22673.35
- **Entrée**: 22655.17 @ 2025-06-25 12:33:00
- **Stop Loss**: 22697.57
- **Risk**: 42.40 points
- **TP 1RR**: 22612.78 ✅
- **TP 2RR**: 22570.38 ❌
- **TP 3RR**: 22527.98 ❌
- **TP 4RR**: 22485.58 ❌
- **TP 15RR**: 22019.21 ❌
- **PnL**: -42.40 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 52.52 points

### Trade #1037 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-25 12:30:00
- **FVG 5m**: 22646.84 - 22651.89
- **Entrée**: 22655.17 @ 2025-06-25 14:02:00
- **Stop Loss**: 22598.93
- **Risk**: 56.25 points
- **TP 1RR**: 22711.42 ✅
- **TP 2RR**: 22767.67 ✅
- **TP 3RR**: 22823.91 ✅
- **TP 4RR**: 22880.16 ✅
- **TP 15RR**: 23498.86 ✅
- **PnL**: 843.69 points (15.0R)
- **MFE**: 847.31 points
- **MAE**: 12.88 points

### Trade #1038 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-25 12:30:00
- **FVG 5m**: 22646.84 - 22651.89
- **Entrée**: 22655.17 @ 2025-06-25 14:02:00
- **Stop Loss**: 22598.93
- **Risk**: 56.25 points
- **TP 1RR**: 22711.42 ✅
- **TP 2RR**: 22767.67 ✅
- **TP 3RR**: 22823.91 ✅
- **TP 4RR**: 22880.16 ✅
- **TP 15RR**: 23498.86 ✅
- **PnL**: 843.69 points (15.0R)
- **MFE**: 847.31 points
- **MAE**: 12.88 points

### Trade #1039 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 03:15:00
- **FVG 5m**: 22776.87 - 22779.39
- **Entrée**: 22780.65 @ 2025-06-26 05:06:00
- **Stop Loss**: 22761.69
- **Risk**: 18.96 points
- **TP 1RR**: 22799.61 ✅
- **TP 2RR**: 22818.58 ❌
- **TP 3RR**: 22837.54 ❌
- **TP 4RR**: 22856.50 ❌
- **TP 15RR**: 23065.07 ❌
- **PnL**: -18.96 points (-1.0R)
- **MFE**: 28.02 points
- **MAE**: 19.69 points

### Trade #1040 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 07:30:00
- **FVG 5m**: 22762.22 - 22767.78
- **Entrée**: 22775.86 @ 2025-06-26 08:20:00
- **Stop Loss**: 22731.66
- **Risk**: 44.19 points
- **TP 1RR**: 22820.05 ❌
- **TP 2RR**: 22864.24 ❌
- **TP 3RR**: 22908.44 ❌
- **TP 4RR**: 22952.63 ❌
- **TP 15RR**: 23438.76 ❌
- **PnL**: -44.19 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 52.01 points

### Trade #1041 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-26 09:30:00
- **FVG 5m**: 22805.65 - 22823.32
- **Entrée**: 22802.37 @ 2025-06-26 10:28:00
- **Stop Loss**: 22832.46
- **Risk**: 30.09 points
- **TP 1RR**: 22772.27 ❌
- **TP 2RR**: 22742.18 ❌
- **TP 3RR**: 22712.09 ❌
- **TP 4RR**: 22681.99 ❌
- **TP 15RR**: 22350.96 ❌
- **PnL**: -30.09 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 31.56 points

### Trade #1042 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-26 09:30:00
- **FVG 5m**: 22805.65 - 22823.32
- **Entrée**: 22802.37 @ 2025-06-26 10:28:00
- **Stop Loss**: 22832.46
- **Risk**: 30.09 points
- **TP 1RR**: 22772.27 ❌
- **TP 2RR**: 22742.18 ❌
- **TP 3RR**: 22712.09 ❌
- **TP 4RR**: 22681.99 ❌
- **TP 15RR**: 22350.96 ❌
- **PnL**: -30.09 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 31.56 points

### Trade #1043 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 12:00:00
- **FVG 5m**: 22872.81 - 22881.39
- **Entrée**: 22884.67 @ 2025-06-26 13:08:00
- **Stop Loss**: 22809.89
- **Risk**: 74.78 points
- **TP 1RR**: 22959.46 ✅
- **TP 2RR**: 23034.24 ✅
- **TP 3RR**: 23109.02 ✅
- **TP 4RR**: 23183.80 ❌
- **TP 15RR**: 24006.41 ❌
- **PnL**: -74.78 points (-1.0R)
- **MFE**: 277.22 points
- **MAE**: 79.02 points

### Trade #1044 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-26 12:00:00
- **FVG 5m**: 22872.81 - 22881.39
- **Entrée**: 22884.67 @ 2025-06-26 13:08:00
- **Stop Loss**: 22809.89
- **Risk**: 74.78 points
- **TP 1RR**: 22959.46 ✅
- **TP 2RR**: 23034.24 ✅
- **TP 3RR**: 23109.02 ✅
- **TP 4RR**: 23183.80 ❌
- **TP 15RR**: 24006.41 ❌
- **PnL**: -74.78 points (-1.0R)
- **MFE**: 277.22 points
- **MAE**: 79.02 points

### Trade #1045 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-26 18:00:00
- **FVG 5m**: 22904.11 - 22907.65
- **Entrée**: 22902.35 @ 2025-06-26 18:11:00
- **Stop Loss**: 22936.53
- **Risk**: 34.19 points
- **TP 1RR**: 22868.16 ❌
- **TP 2RR**: 22833.98 ❌
- **TP 3RR**: 22799.79 ❌
- **TP 4RR**: 22765.61 ❌
- **TP 15RR**: 22389.57 ❌
- **PnL**: -34.19 points (-1.0R)
- **MFE**: 17.67 points
- **MAE**: 34.59 points

### Trade #1046 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:00:00
- **FVG 5m**: 22984.65 - 22992.23
- **Entrée**: 22982.38 @ 2025-06-27 07:15:00
- **Stop Loss**: 23025.20
- **Risk**: 42.81 points
- **TP 1RR**: 22939.57 ✅
- **TP 2RR**: 22896.75 ❌
- **TP 3RR**: 22853.94 ❌
- **TP 4RR**: 22811.13 ❌
- **TP 15RR**: 22340.17 ❌
- **PnL**: -42.81 points (-1.0R)
- **MFE**: 72.46 points
- **MAE**: 43.43 points

### Trade #1047 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:00:00
- **FVG 5m**: 22984.65 - 22992.23
- **Entrée**: 22982.38 @ 2025-06-27 07:15:00
- **Stop Loss**: 23025.20
- **Risk**: 42.81 points
- **TP 1RR**: 22939.57 ✅
- **TP 2RR**: 22896.75 ❌
- **TP 3RR**: 22853.94 ❌
- **TP 4RR**: 22811.13 ❌
- **TP 15RR**: 22340.17 ❌
- **PnL**: -42.81 points (-1.0R)
- **MFE**: 72.46 points
- **MAE**: 43.43 points

### Trade #1048 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:30:00
- **FVG 5m**: 22943.25 - 22952.84
- **Entrée**: 22942.24 @ 2025-06-27 08:01:00
- **Stop Loss**: 23010.80
- **Risk**: 68.56 points
- **TP 1RR**: 22873.68 ❌
- **TP 2RR**: 22805.12 ❌
- **TP 3RR**: 22736.56 ❌
- **TP 4RR**: 22668.00 ❌
- **TP 15RR**: 21913.85 ❌
- **PnL**: -68.56 points (-1.0R)
- **MFE**: 32.32 points
- **MAE**: 76.00 points

### Trade #1049 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 07:30:00
- **FVG 5m**: 22943.25 - 22952.84
- **Entrée**: 22942.24 @ 2025-06-27 08:01:00
- **Stop Loss**: 23010.80
- **Risk**: 68.56 points
- **TP 1RR**: 22873.68 ❌
- **TP 2RR**: 22805.12 ❌
- **TP 3RR**: 22736.56 ❌
- **TP 4RR**: 22668.00 ❌
- **TP 15RR**: 21913.85 ❌
- **PnL**: -68.56 points (-1.0R)
- **MFE**: 32.32 points
- **MAE**: 76.00 points

### Trade #1050 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 08:30:00
- **FVG 5m**: 22971.27 - 22989.96
- **Entrée**: 22991.22 @ 2025-06-27 08:56:00
- **Stop Loss**: 22898.47
- **Risk**: 92.75 points
- **TP 1RR**: 23083.97 ❌
- **TP 2RR**: 23176.72 ❌
- **TP 3RR**: 23269.48 ❌
- **TP 4RR**: 23362.23 ❌
- **TP 15RR**: 24382.50 ❌
- **PnL**: -92.75 points (-1.0R)
- **MFE**: 60.34 points
- **MAE**: 100.74 points

### Trade #1051 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 08:30:00
- **FVG 5m**: 22971.27 - 22989.96
- **Entrée**: 22991.22 @ 2025-06-27 08:56:00
- **Stop Loss**: 22898.47
- **Risk**: 92.75 points
- **TP 1RR**: 23083.97 ❌
- **TP 2RR**: 23176.72 ❌
- **TP 3RR**: 23269.48 ❌
- **TP 4RR**: 23362.23 ❌
- **TP 15RR**: 24382.50 ❌
- **PnL**: -92.75 points (-1.0R)
- **MFE**: 60.34 points
- **MAE**: 100.74 points

### Trade #1052 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 09:15:00
- **FVG 5m**: 23000.81 - 23012.17
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23053.49
- **Risk**: 62.02 points
- **TP 1RR**: 22929.46 ✅
- **TP 2RR**: 22867.44 ✅
- **TP 3RR**: 22805.42 ❌
- **TP 4RR**: 22743.41 ❌
- **TP 15RR**: 22061.23 ❌
- **PnL**: -62.02 points (-1.0R)
- **MFE**: 167.64 points
- **MAE**: 62.61 points

### Trade #1053 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 09:15:00
- **FVG 5m**: 23000.81 - 23012.17
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23053.49
- **Risk**: 62.02 points
- **TP 1RR**: 22929.46 ✅
- **TP 2RR**: 22867.44 ✅
- **TP 3RR**: 22805.42 ❌
- **TP 4RR**: 22743.41 ❌
- **TP 15RR**: 22061.23 ❌
- **PnL**: -62.02 points (-1.0R)
- **MFE**: 167.64 points
- **MAE**: 62.61 points

### Trade #1054 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 09:15:00
- **FVG 5m**: 23000.81 - 23012.17
- **Entrée**: 22991.47 @ 2025-06-27 09:51:00
- **Stop Loss**: 23053.49
- **Risk**: 62.02 points
- **TP 1RR**: 22929.46 ✅
- **TP 2RR**: 22867.44 ✅
- **TP 3RR**: 22805.42 ❌
- **TP 4RR**: 22743.41 ❌
- **TP 15RR**: 22061.23 ❌
- **PnL**: -62.02 points (-1.0R)
- **MFE**: 167.64 points
- **MAE**: 62.61 points

### Trade #1055 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-27 13:30:00
- **FVG 5m**: 22842.26 - 22857.91
- **Entrée**: 22826.10 @ 2025-06-27 13:52:00
- **Stop Loss**: 22913.04
- **Risk**: 86.94 points
- **TP 1RR**: 22739.16 ❌
- **TP 2RR**: 22652.22 ❌
- **TP 3RR**: 22565.28 ❌
- **TP 4RR**: 22478.34 ❌
- **TP 15RR**: 21521.98 ❌
- **PnL**: -86.94 points (-1.0R)
- **MFE**: 2.27 points
- **MAE**: 89.63 points

### Trade #1056 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:00:00
- **FVG 5m**: 22916.99 - 22923.30
- **Entrée**: 22931.89 @ 2025-06-27 14:40:00
- **Stop Loss**: 22817.71
- **Risk**: 114.17 points
- **TP 1RR**: 23046.06 ✅
- **TP 2RR**: 23160.23 ✅
- **TP 3RR**: 23274.40 ❌
- **TP 4RR**: 23388.58 ❌
- **TP 15RR**: 24644.47 ❌
- **PnL**: -114.17 points (-1.0R)
- **MFE**: 230.01 points
- **MAE**: 118.92 points

### Trade #1057 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:00:00
- **FVG 5m**: 22916.99 - 22923.30
- **Entrée**: 22931.89 @ 2025-06-27 14:40:00
- **Stop Loss**: 22817.71
- **Risk**: 114.17 points
- **TP 1RR**: 23046.06 ✅
- **TP 2RR**: 23160.23 ✅
- **TP 3RR**: 23274.40 ❌
- **TP 4RR**: 23388.58 ❌
- **TP 15RR**: 24644.47 ❌
- **PnL**: -114.17 points (-1.0R)
- **MFE**: 230.01 points
- **MAE**: 118.92 points

### Trade #1058 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:30:00
- **FVG 5m**: 22945.52 - 22959.91
- **Entrée**: 22962.18 @ 2025-06-27 14:54:00
- **Stop Loss**: 22884.34
- **Risk**: 77.85 points
- **TP 1RR**: 23040.03 ✅
- **TP 2RR**: 23117.88 ✅
- **TP 3RR**: 23195.73 ❌
- **TP 4RR**: 23273.58 ❌
- **TP 15RR**: 24129.92 ❌
- **PnL**: -77.85 points (-1.0R)
- **MFE**: 199.71 points
- **MAE**: 80.79 points

### Trade #1059 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-27 14:30:00
- **FVG 5m**: 22945.52 - 22959.91
- **Entrée**: 22962.18 @ 2025-06-27 14:54:00
- **Stop Loss**: 22884.34
- **Risk**: 77.85 points
- **TP 1RR**: 23040.03 ✅
- **TP 2RR**: 23117.88 ✅
- **TP 3RR**: 23195.73 ❌
- **TP 4RR**: 23273.58 ❌
- **TP 15RR**: 24129.92 ❌
- **PnL**: -77.85 points (-1.0R)
- **MFE**: 199.71 points
- **MAE**: 80.79 points

### Trade #1060 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-29 17:45:00
- **FVG 5m**: 23046.01 - 23053.83
- **Entrée**: 23042.22 @ 2025-06-29 18:37:00
- **Stop Loss**: 23080.26
- **Risk**: 38.04 points
- **TP 1RR**: 23004.17 ❌
- **TP 2RR**: 22966.13 ❌
- **TP 3RR**: 22928.09 ❌
- **TP 4RR**: 22890.04 ❌
- **TP 15RR**: 22471.55 ❌
- **PnL**: -38.04 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 40.90 points

### Trade #1061 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-29 17:45:00
- **FVG 5m**: 23046.01 - 23053.83
- **Entrée**: 23042.22 @ 2025-06-29 18:37:00
- **Stop Loss**: 23080.26
- **Risk**: 38.04 points
- **TP 1RR**: 23004.17 ❌
- **TP 2RR**: 22966.13 ❌
- **TP 3RR**: 22928.09 ❌
- **TP 4RR**: 22890.04 ❌
- **TP 15RR**: 22471.55 ❌
- **PnL**: -38.04 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 40.90 points

### Trade #1062 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 01:30:00
- **FVG 5m**: 23094.73 - 23101.55
- **Entrée**: 23094.23 @ 2025-06-30 02:02:00
- **Stop Loss**: 23136.59
- **Risk**: 42.36 points
- **TP 1RR**: 23051.86 ❌
- **TP 2RR**: 23009.50 ❌
- **TP 3RR**: 22967.14 ❌
- **TP 4RR**: 22924.77 ❌
- **TP 15RR**: 22458.76 ❌
- **PnL**: -42.36 points (-1.0R)
- **MFE**: 18.68 points
- **MAE**: 44.44 points

### Trade #1063 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 08:30:00
- **FVG 5m**: 23041.97 - 23054.84
- **Entrée**: 23037.67 @ 2025-06-30 10:13:00
- **Stop Loss**: 23113.61
- **Risk**: 75.93 points
- **TP 1RR**: 22961.74 ❌
- **TP 2RR**: 22885.81 ❌
- **TP 3RR**: 22809.88 ❌
- **TP 4RR**: 22733.94 ❌
- **TP 15RR**: 21898.69 ❌
- **PnL**: -75.93 points (-1.0R)
- **MFE**: 31.05 points
- **MAE**: 80.29 points

### Trade #1064 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 08:45:00
- **FVG 5m**: 23078.07 - 23084.13
- **Entrée**: 23087.92 @ 2025-06-30 11:04:00
- **Stop Loss**: 23008.49
- **Risk**: 79.43 points
- **TP 1RR**: 23167.34 ❌
- **TP 2RR**: 23246.77 ❌
- **TP 3RR**: 23326.20 ❌
- **TP 4RR**: 23405.62 ❌
- **TP 15RR**: 24279.31 ❌
- **PnL**: -79.43 points (-1.0R)
- **MFE**: 6.06 points
- **MAE**: 81.30 points

### Trade #1065 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 11:30:00
- **FVG 5m**: 23049.54 - 23052.32
- **Entrée**: 23053.58 @ 2025-06-30 13:16:00
- **Stop Loss**: 23047.61
- **Risk**: 5.98 points
- **TP 1RR**: 23059.56 ✅
- **TP 2RR**: 23065.53 ✅
- **TP 3RR**: 23071.51 ❌
- **TP 4RR**: 23077.48 ❌
- **TP 15RR**: 23143.21 ❌
- **PnL**: -5.98 points (-1.0R)
- **MFE**: 13.89 points
- **MAE**: 10.35 points

### Trade #1066 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 12:45:00
- **FVG 5m**: 23049.54 - 23052.32
- **Entrée**: 23053.58 @ 2025-06-30 13:16:00
- **Stop Loss**: 23000.42
- **Risk**: 53.16 points
- **TP 1RR**: 23106.74 ✅
- **TP 2RR**: 23159.91 ✅
- **TP 3RR**: 23213.07 ❌
- **TP 4RR**: 23266.24 ❌
- **TP 15RR**: 23851.05 ❌
- **PnL**: -53.16 points (-1.0R)
- **MFE**: 108.31 points
- **MAE**: 67.41 points

### Trade #1067 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 13:30:00
- **FVG 5m**: 23045.50 - 23050.30
- **Entrée**: 23050.55 @ 2025-06-30 13:54:00
- **Stop Loss**: 22995.12
- **Risk**: 55.43 points
- **TP 1RR**: 23105.98 ✅
- **TP 2RR**: 23161.42 ✅
- **TP 3RR**: 23216.85 ❌
- **TP 4RR**: 23272.29 ❌
- **TP 15RR**: 23882.06 ❌
- **PnL**: -55.43 points (-1.0R)
- **MFE**: 111.34 points
- **MAE**: 64.38 points

### Trade #1068 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-06-30 14:00:00
- **FVG 5m**: 23092.97 - 23101.30
- **Entrée**: 23103.82 @ 2025-06-30 14:21:00
- **Stop Loss**: 23063.00
- **Risk**: 40.82 points
- **TP 1RR**: 23144.65 ✅
- **TP 2RR**: 23185.47 ❌
- **TP 3RR**: 23226.30 ❌
- **TP 4RR**: 23267.12 ❌
- **TP 15RR**: 23716.19 ❌
- **PnL**: -40.82 points (-1.0R)
- **MFE**: 58.07 points
- **MAE**: 43.43 points

### Trade #1069 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 14:45:00
- **FVG 5m**: 23089.43 - 23091.96
- **Entrée**: 23088.67 @ 2025-06-30 17:54:00
- **Stop Loss**: 23173.47
- **Risk**: 84.80 points
- **TP 1RR**: 23003.88 ✅
- **TP 2RR**: 22919.08 ✅
- **TP 3RR**: 22834.28 ✅
- **TP 4RR**: 22749.48 ❌
- **TP 15RR**: 21816.69 ❌
- **PnL**: -84.80 points (-1.0R)
- **MFE**: 283.03 points
- **MAE**: 110.08 points

### Trade #1070 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 14:45:00
- **FVG 5m**: 23089.43 - 23091.96
- **Entrée**: 23088.67 @ 2025-06-30 17:54:00
- **Stop Loss**: 23173.47
- **Risk**: 84.80 points
- **TP 1RR**: 23003.88 ✅
- **TP 2RR**: 22919.08 ✅
- **TP 3RR**: 22834.28 ✅
- **TP 4RR**: 22749.48 ❌
- **TP 15RR**: 21816.69 ❌
- **PnL**: -84.80 points (-1.0R)
- **MFE**: 283.03 points
- **MAE**: 110.08 points

### Trade #1071 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-06-30 15:00:00
- **FVG 5m**: 23089.43 - 23091.96
- **Entrée**: 23088.67 @ 2025-06-30 17:54:00
- **Stop Loss**: 23136.09
- **Risk**: 47.41 points
- **TP 1RR**: 23041.26 ❌
- **TP 2RR**: 22993.85 ❌
- **TP 3RR**: 22946.43 ❌
- **TP 4RR**: 22899.02 ❌
- **TP 15RR**: 22377.47 ❌
- **PnL**: -47.41 points (-1.0R)
- **MFE**: 16.16 points
- **MAE**: 52.52 points

### Trade #1072 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 03:15:00
- **FVG 5m**: 23047.02 - 23056.36
- **Entrée**: 23056.86 @ 2025-07-01 04:59:00
- **Stop Loss**: 23042.56
- **Risk**: 14.30 points
- **TP 1RR**: 23071.17 ✅
- **TP 2RR**: 23085.47 ❌
- **TP 3RR**: 23099.78 ❌
- **TP 4RR**: 23114.08 ❌
- **TP 15RR**: 23271.43 ❌
- **PnL**: -14.30 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 14.64 points

### Trade #1073 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-01 04:45:00
- **FVG 5m**: 23047.02 - 23056.36
- **Entrée**: 23056.86 @ 2025-07-01 04:59:00
- **Stop Loss**: 23027.16
- **Risk**: 29.70 points
- **TP 1RR**: 23086.56 ❌
- **TP 2RR**: 23116.26 ❌
- **TP 3RR**: 23145.96 ❌
- **TP 4RR**: 23175.65 ❌
- **TP 15RR**: 23502.33 ❌
- **PnL**: -29.70 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 34.08 points

### Trade #1074 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 02:00:00
- **FVG 5m**: 22978.85 - 22984.65
- **Entrée**: 22976.58 @ 2025-07-02 02:18:00
- **Stop Loss**: 23013.58
- **Risk**: 37.00 points
- **TP 1RR**: 22939.57 ✅
- **TP 2RR**: 22902.57 ✅
- **TP 3RR**: 22865.57 ✅
- **TP 4RR**: 22828.57 ✅
- **TP 15RR**: 22421.56 ❌
- **PnL**: -37.00 points (-1.0R)
- **MFE**: 170.93 points
- **MAE**: 39.13 points

### Trade #1075 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 02:30:00
- **FVG 5m**: 22956.88 - 22962.18
- **Entrée**: 22955.87 @ 2025-07-02 02:43:00
- **Stop Loss**: 22983.01
- **Risk**: 27.14 points
- **TP 1RR**: 22928.73 ✅
- **TP 2RR**: 22901.59 ✅
- **TP 3RR**: 22874.45 ✅
- **TP 4RR**: 22847.32 ✅
- **TP 15RR**: 22548.78 ❌
- **PnL**: -27.14 points (-1.0R)
- **MFE**: 150.22 points
- **MAE**: 31.31 points

### Trade #1076 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 07:00:00
- **FVG 5m**: 22841.00 - 22864.48
- **Entrée**: 22878.11 @ 2025-07-02 08:04:00
- **Stop Loss**: 22858.85
- **Risk**: 19.26 points
- **TP 1RR**: 22897.37 ❌
- **TP 2RR**: 22916.63 ❌
- **TP 3RR**: 22935.90 ❌
- **TP 4RR**: 22955.16 ❌
- **TP 15RR**: 23167.04 ❌
- **PnL**: -19.26 points (-1.0R)
- **MFE**: 5.05 points
- **MAE**: 19.69 points

### Trade #1077 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 07:30:00
- **FVG 5m**: 22841.00 - 22864.48
- **Entrée**: 22878.11 @ 2025-07-02 08:04:00
- **Stop Loss**: 22794.25
- **Risk**: 83.86 points
- **TP 1RR**: 22961.97 ✅
- **TP 2RR**: 23045.84 ✅
- **TP 3RR**: 23129.70 ✅
- **TP 4RR**: 23213.56 ✅
- **TP 15RR**: 24136.06 ✅
- **PnL**: 1257.95 points (15.0R)
- **MFE**: 1258.59 points
- **MAE**: 20.20 points

### Trade #1078 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 08:15:00
- **FVG 5m**: 22872.56 - 22875.58
- **Entrée**: 22878.87 @ 2025-07-02 08:28:00
- **Stop Loss**: 22846.48
- **Risk**: 32.38 points
- **TP 1RR**: 22911.25 ✅
- **TP 2RR**: 22943.64 ✅
- **TP 3RR**: 22976.02 ✅
- **TP 4RR**: 23008.40 ✅
- **TP 15RR**: 23364.63 ✅
- **PnL**: 485.77 points (15.0R)
- **MFE**: 497.63 points
- **MAE**: 4.04 points

### Trade #1079 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 09:15:00
- **FVG 5m**: 22994.25 - 23015.20
- **Entrée**: 23015.71 @ 2025-07-02 09:28:00
- **Stop Loss**: 22967.86
- **Risk**: 47.85 points
- **TP 1RR**: 23063.56 ✅
- **TP 2RR**: 23111.40 ✅
- **TP 3RR**: 23159.25 ✅
- **TP 4RR**: 23207.09 ✅
- **TP 15RR**: 23733.40 ✅
- **PnL**: 717.69 points (15.0R)
- **MFE**: 775.86 points
- **MAE**: 19.19 points

### Trade #1080 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-02 21:30:00
- **FVG 5m**: 23069.23 - 23071.76
- **Entrée**: 23072.26 @ 2025-07-02 21:47:00
- **Stop Loss**: 23041.55
- **Risk**: 30.71 points
- **TP 1RR**: 23102.98 ✅
- **TP 2RR**: 23133.69 ✅
- **TP 3RR**: 23164.41 ✅
- **TP 4RR**: 23195.12 ✅
- **TP 15RR**: 23532.98 ❌
- **PnL**: -30.71 points (-1.0R)
- **MFE**: 259.04 points
- **MAE**: 31.31 points

### Trade #1081 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 22:45:00
- **FVG 5m**: 23094.48 - 23097.01
- **Entrée**: 23094.23 @ 2025-07-02 23:32:00
- **Stop Loss**: 23119.42
- **Risk**: 25.19 points
- **TP 1RR**: 23069.04 ❌
- **TP 2RR**: 23043.85 ❌
- **TP 3RR**: 23018.67 ❌
- **TP 4RR**: 22993.48 ❌
- **TP 15RR**: 22716.41 ❌
- **PnL**: -25.19 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 27.77 points

### Trade #1082 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-02 22:45:00
- **FVG 5m**: 23094.48 - 23097.01
- **Entrée**: 23094.23 @ 2025-07-02 23:32:00
- **Stop Loss**: 23119.42
- **Risk**: 25.19 points
- **TP 1RR**: 23069.04 ❌
- **TP 2RR**: 23043.85 ❌
- **TP 3RR**: 23018.67 ❌
- **TP 4RR**: 22993.48 ❌
- **TP 15RR**: 22716.41 ❌
- **PnL**: -25.19 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 27.77 points

### Trade #1083 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-03 02:45:00
- **FVG 5m**: 23081.86 - 23085.90
- **Entrée**: 23079.84 @ 2025-07-03 04:57:00
- **Stop Loss**: 23138.36
- **Risk**: 58.52 points
- **TP 1RR**: 23021.31 ❌
- **TP 2RR**: 22962.79 ❌
- **TP 3RR**: 22904.27 ❌
- **TP 4RR**: 22845.74 ❌
- **TP 15RR**: 22201.98 ❌
- **PnL**: -58.52 points (-1.0R)
- **MFE**: 23.73 points
- **MAE**: 66.15 points

### Trade #1084 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-03 03:45:00
- **FVG 5m**: 23081.86 - 23085.90
- **Entrée**: 23079.84 @ 2025-07-03 04:57:00
- **Stop Loss**: 23112.09
- **Risk**: 32.25 points
- **TP 1RR**: 23047.58 ❌
- **TP 2RR**: 23015.33 ❌
- **TP 3RR**: 22983.08 ❌
- **TP 4RR**: 22950.82 ❌
- **TP 15RR**: 22596.04 ❌
- **PnL**: -32.25 points (-1.0R)
- **MFE**: 23.73 points
- **MAE**: 66.15 points

### Trade #1085 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-04 03:45:00
- **FVG 5m**: 23156.09 - 23160.88
- **Entrée**: 23152.80 @ 2025-07-04 05:44:00
- **Stop Loss**: 23196.97
- **Risk**: 44.16 points
- **TP 1RR**: 23108.64 ✅
- **TP 2RR**: 23064.48 ❌
- **TP 3RR**: 23020.32 ❌
- **TP 4RR**: 22976.16 ❌
- **TP 15RR**: 22490.37 ❌
- **PnL**: -44.16 points (-1.0R)
- **MFE**: 44.18 points
- **MAE**: 84.83 points

### Trade #1086 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-04 06:00:00
- **FVG 5m**: 23142.45 - 23147.75
- **Entrée**: 23148.76 @ 2025-07-04 06:14:00
- **Stop Loss**: 23113.72
- **Risk**: 35.04 points
- **TP 1RR**: 23183.81 ✅
- **TP 2RR**: 23218.85 ✅
- **TP 3RR**: 23253.89 ✅
- **TP 4RR**: 23288.94 ❌
- **TP 15RR**: 23674.41 ❌
- **PnL**: -35.04 points (-1.0R)
- **MFE**: 107.81 points
- **MAE**: 38.88 points

### Trade #1087 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-06 17:00:00
- **FVG 5m**: 23203.80 - 23212.89
- **Entrée**: 23213.65 @ 2025-07-06 18:15:00
- **Stop Loss**: 23158.64
- **Risk**: 55.01 points
- **TP 1RR**: 23268.66 ❌
- **TP 2RR**: 23323.67 ❌
- **TP 3RR**: 23378.68 ❌
- **TP 4RR**: 23433.69 ❌
- **TP 15RR**: 24038.81 ❌
- **PnL**: -55.01 points (-1.0R)
- **MFE**: 19.95 points
- **MAE**: 60.09 points

### Trade #1088 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-06 20:00:00
- **FVG 5m**: 23180.32 - 23185.63
- **Entrée**: 23178.56 @ 2025-07-06 21:31:00
- **Stop Loss**: 23209.60
- **Risk**: 31.04 points
- **TP 1RR**: 23147.52 ❌
- **TP 2RR**: 23116.48 ❌
- **TP 3RR**: 23085.44 ❌
- **TP 4RR**: 23054.40 ❌
- **TP 15RR**: 22712.96 ❌
- **PnL**: -31.04 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 37.37 points

### Trade #1089 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-07 07:15:00
- **FVG 5m**: 23182.60 - 23189.92
- **Entrée**: 23180.32 @ 2025-07-07 07:54:00
- **Stop Loss**: 23241.17
- **Risk**: 60.85 points
- **TP 1RR**: 23119.48 ✅
- **TP 2RR**: 23058.63 ✅
- **TP 3RR**: 22997.78 ❌
- **TP 4RR**: 22936.93 ❌
- **TP 15RR**: 22267.61 ❌
- **PnL**: -60.85 points (-1.0R)
- **MFE**: 174.97 points
- **MAE**: 62.87 points

### Trade #1090 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-07 07:15:00
- **FVG 5m**: 23182.60 - 23189.92
- **Entrée**: 23180.32 @ 2025-07-07 07:54:00
- **Stop Loss**: 23241.17
- **Risk**: 60.85 points
- **TP 1RR**: 23119.48 ✅
- **TP 2RR**: 23058.63 ✅
- **TP 3RR**: 22997.78 ❌
- **TP 4RR**: 22936.93 ❌
- **TP 15RR**: 22267.61 ❌
- **PnL**: -60.85 points (-1.0R)
- **MFE**: 174.97 points
- **MAE**: 62.87 points

### Trade #1091 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 08:30:00
- **FVG 5m**: 23144.72 - 23155.33
- **Entrée**: 23160.63 @ 2025-07-07 10:57:00
- **Stop Loss**: 23115.74
- **Risk**: 44.89 points
- **TP 1RR**: 23205.52 ❌
- **TP 2RR**: 23250.41 ❌
- **TP 3RR**: 23295.30 ❌
- **TP 4RR**: 23340.19 ❌
- **TP 15RR**: 23833.99 ❌
- **PnL**: -44.89 points (-1.0R)
- **MFE**: 29.29 points
- **MAE**: 66.91 points

### Trade #1092 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 08:30:00
- **FVG 5m**: 23144.72 - 23155.33
- **Entrée**: 23160.63 @ 2025-07-07 10:57:00
- **Stop Loss**: 23115.74
- **Risk**: 44.89 points
- **TP 1RR**: 23205.52 ❌
- **TP 2RR**: 23250.41 ❌
- **TP 3RR**: 23295.30 ❌
- **TP 4RR**: 23340.19 ❌
- **TP 15RR**: 23833.99 ❌
- **PnL**: -44.89 points (-1.0R)
- **MFE**: 29.29 points
- **MAE**: 66.91 points

### Trade #1093 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 11:15:00
- **FVG 5m**: 23033.13 - 23046.26
- **Entrée**: 23050.05 @ 2025-07-07 13:37:00
- **Stop Loss**: 23048.11
- **Risk**: 1.94 points
- **TP 1RR**: 23051.98 ❌
- **TP 2RR**: 23053.92 ❌
- **TP 3RR**: 23055.85 ❌
- **TP 4RR**: 23057.79 ❌
- **TP 15RR**: 23079.08 ❌
- **PnL**: -1.94 points (-1.0R)
- **MFE**: 2.02 points
- **MAE**: 2.78 points

### Trade #1094 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 11:15:00
- **FVG 5m**: 23033.13 - 23046.26
- **Entrée**: 23050.05 @ 2025-07-07 13:37:00
- **Stop Loss**: 23048.11
- **Risk**: 1.94 points
- **TP 1RR**: 23051.98 ❌
- **TP 2RR**: 23053.92 ❌
- **TP 3RR**: 23055.85 ❌
- **TP 4RR**: 23057.79 ❌
- **TP 15RR**: 23079.08 ❌
- **PnL**: -1.94 points (-1.0R)
- **MFE**: 2.02 points
- **MAE**: 2.78 points

### Trade #1095 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 11:15:00
- **FVG 5m**: 23033.13 - 23046.26
- **Entrée**: 23050.05 @ 2025-07-07 13:37:00
- **Stop Loss**: 23048.11
- **Risk**: 1.94 points
- **TP 1RR**: 23051.98 ❌
- **TP 2RR**: 23053.92 ❌
- **TP 3RR**: 23055.85 ❌
- **TP 4RR**: 23057.79 ❌
- **TP 15RR**: 23079.08 ❌
- **PnL**: -1.94 points (-1.0R)
- **MFE**: 2.02 points
- **MAE**: 2.78 points

### Trade #1096 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 11:15:00
- **FVG 5m**: 23033.13 - 23046.26
- **Entrée**: 23050.05 @ 2025-07-07 13:37:00
- **Stop Loss**: 23048.11
- **Risk**: 1.94 points
- **TP 1RR**: 23051.98 ❌
- **TP 2RR**: 23053.92 ❌
- **TP 3RR**: 23055.85 ❌
- **TP 4RR**: 23057.79 ❌
- **TP 15RR**: 23079.08 ❌
- **PnL**: -1.94 points (-1.0R)
- **MFE**: 2.02 points
- **MAE**: 2.78 points

### Trade #1097 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-07 11:45:00
- **FVG 5m**: 23056.11 - 23091.45
- **Entrée**: 23050.30 @ 2025-07-07 13:19:00
- **Stop Loss**: 23134.07
- **Risk**: 83.77 points
- **TP 1RR**: 22966.53 ❌
- **TP 2RR**: 22882.76 ❌
- **TP 3RR**: 22798.99 ❌
- **TP 4RR**: 22715.22 ❌
- **TP 15RR**: 21793.76 ❌
- **PnL**: -83.77 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 85.34 points

### Trade #1098 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23052.07 - 23069.23
- **Entrée**: 23073.27 @ 2025-07-07 13:42:00
- **Stop Loss**: 22993.85
- **Risk**: 79.42 points
- **TP 1RR**: 23152.69 ✅
- **TP 2RR**: 23232.11 ✅
- **TP 3RR**: 23311.53 ✅
- **TP 4RR**: 23390.95 ✅
- **TP 15RR**: 24264.55 ✅
- **PnL**: 1191.28 points (15.0R)
- **MFE**: 1191.69 points
- **MAE**: 72.71 points

### Trade #1099 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23052.07 - 23069.23
- **Entrée**: 23073.27 @ 2025-07-07 13:42:00
- **Stop Loss**: 22993.85
- **Risk**: 79.42 points
- **TP 1RR**: 23152.69 ✅
- **TP 2RR**: 23232.11 ✅
- **TP 3RR**: 23311.53 ✅
- **TP 4RR**: 23390.95 ✅
- **TP 15RR**: 24264.55 ✅
- **PnL**: 1191.28 points (15.0R)
- **MFE**: 1191.69 points
- **MAE**: 72.71 points

### Trade #1100 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23052.07 - 23069.23
- **Entrée**: 23073.27 @ 2025-07-07 13:42:00
- **Stop Loss**: 22993.85
- **Risk**: 79.42 points
- **TP 1RR**: 23152.69 ✅
- **TP 2RR**: 23232.11 ✅
- **TP 3RR**: 23311.53 ✅
- **TP 4RR**: 23390.95 ✅
- **TP 15RR**: 24264.55 ✅
- **PnL**: 1191.28 points (15.0R)
- **MFE**: 1191.69 points
- **MAE**: 72.71 points

### Trade #1101 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 13:30:00
- **FVG 5m**: 23052.07 - 23069.23
- **Entrée**: 23073.27 @ 2025-07-07 13:42:00
- **Stop Loss**: 22993.85
- **Risk**: 79.42 points
- **TP 1RR**: 23152.69 ✅
- **TP 2RR**: 23232.11 ✅
- **TP 3RR**: 23311.53 ✅
- **TP 4RR**: 23390.95 ✅
- **TP 15RR**: 24264.55 ✅
- **PnL**: 1191.28 points (15.0R)
- **MFE**: 1191.69 points
- **MAE**: 72.71 points

### Trade #1102 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 19:30:00
- **FVG 5m**: 23114.17 - 23117.96
- **Entrée**: 23121.50 @ 2025-07-07 19:41:00
- **Stop Loss**: 23092.78
- **Risk**: 28.72 points
- **TP 1RR**: 23150.22 ✅
- **TP 2RR**: 23178.94 ✅
- **TP 3RR**: 23207.66 ❌
- **TP 4RR**: 23236.38 ❌
- **TP 15RR**: 23552.30 ❌
- **PnL**: -28.72 points (-1.0R)
- **MFE**: 78.77 points
- **MAE**: 36.86 points

### Trade #1103 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-07 21:15:00
- **FVG 5m**: 23136.14 - 23141.44
- **Entrée**: 23141.69 @ 2025-07-07 21:26:00
- **Stop Loss**: 23107.92
- **Risk**: 33.78 points
- **TP 1RR**: 23175.47 ✅
- **TP 2RR**: 23209.25 ❌
- **TP 3RR**: 23243.03 ❌
- **TP 4RR**: 23276.81 ❌
- **TP 15RR**: 23648.36 ❌
- **PnL**: -33.78 points (-1.0R)
- **MFE**: 58.57 points
- **MAE**: 34.08 points

### Trade #1104 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 06:30:00
- **FVG 5m**: 23167.45 - 23173.51
- **Entrée**: 23175.78 @ 2025-07-08 07:13:00
- **Stop Loss**: 23156.62
- **Risk**: 19.16 points
- **TP 1RR**: 23194.94 ❌
- **TP 2RR**: 23214.10 ❌
- **TP 3RR**: 23233.25 ❌
- **TP 4RR**: 23252.41 ❌
- **TP 15RR**: 23463.15 ❌
- **PnL**: -19.16 points (-1.0R)
- **MFE**: 6.82 points
- **MAE**: 21.97 points

### Trade #1105 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-08 08:15:00
- **FVG 5m**: 23143.71 - 23158.11
- **Entrée**: 23142.20 @ 2025-07-08 08:32:00
- **Stop Loss**: 23190.15
- **Risk**: 47.95 points
- **TP 1RR**: 23094.25 ✅
- **TP 2RR**: 23046.31 ❌
- **TP 3RR**: 22998.36 ❌
- **TP 4RR**: 22950.42 ❌
- **TP 15RR**: 22423.01 ❌
- **PnL**: -47.95 points (-1.0R)
- **MFE**: 74.99 points
- **MAE**: 47.97 points

### Trade #1106 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 08:30:00
- **FVG 5m**: 23103.32 - 23143.97
- **Entrée**: 23149.52 @ 2025-07-08 09:34:00
- **Stop Loss**: 23104.64
- **Risk**: 44.88 points
- **TP 1RR**: 23194.41 ❌
- **TP 2RR**: 23239.29 ❌
- **TP 3RR**: 23284.18 ❌
- **TP 4RR**: 23329.06 ❌
- **TP 15RR**: 23822.80 ❌
- **PnL**: -44.88 points (-1.0R)
- **MFE**: 20.45 points
- **MAE**: 68.93 points

### Trade #1107 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-08 08:45:00
- **FVG 5m**: 23138.66 - 23142.96
- **Entrée**: 23137.15 @ 2025-07-08 09:48:00
- **Stop Loss**: 23163.62
- **Risk**: 26.47 points
- **TP 1RR**: 23110.68 ✅
- **TP 2RR**: 23084.21 ✅
- **TP 3RR**: 23057.73 ❌
- **TP 4RR**: 23031.26 ❌
- **TP 15RR**: 22740.07 ❌
- **PnL**: -26.47 points (-1.0R)
- **MFE**: 69.94 points
- **MAE**: 37.37 points

### Trade #1108 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 09:30:00
- **FVG 5m**: 23151.54 - 23172.75
- **Entrée**: 23174.26 @ 2025-07-08 11:24:00
- **Stop Loss**: 23086.97
- **Risk**: 87.29 points
- **TP 1RR**: 23261.56 ❌
- **TP 2RR**: 23348.85 ❌
- **TP 3RR**: 23436.14 ❌
- **TP 4RR**: 23523.43 ❌
- **TP 15RR**: 24483.64 ❌
- **PnL**: -87.29 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 90.89 points

### Trade #1109 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 09:30:00
- **FVG 5m**: 23151.54 - 23172.75
- **Entrée**: 23174.26 @ 2025-07-08 11:24:00
- **Stop Loss**: 23086.97
- **Risk**: 87.29 points
- **TP 1RR**: 23261.56 ❌
- **TP 2RR**: 23348.85 ❌
- **TP 3RR**: 23436.14 ❌
- **TP 4RR**: 23523.43 ❌
- **TP 15RR**: 24483.64 ❌
- **PnL**: -87.29 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 90.89 points

### Trade #1110 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 09:30:00
- **FVG 5m**: 23151.54 - 23172.75
- **Entrée**: 23174.26 @ 2025-07-08 11:24:00
- **Stop Loss**: 23086.97
- **Risk**: 87.29 points
- **TP 1RR**: 23261.56 ❌
- **TP 2RR**: 23348.85 ❌
- **TP 3RR**: 23436.14 ❌
- **TP 4RR**: 23523.43 ❌
- **TP 15RR**: 24483.64 ❌
- **PnL**: -87.29 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 90.89 points

### Trade #1111 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 19:30:00
- **FVG 5m**: 23112.15 - 23116.70
- **Entrée**: 23116.95 @ 2025-07-08 20:59:00
- **Stop Loss**: 23078.90
- **Risk**: 38.06 points
- **TP 1RR**: 23155.01 ❌
- **TP 2RR**: 23193.06 ❌
- **TP 3RR**: 23231.12 ❌
- **TP 4RR**: 23269.17 ❌
- **TP 15RR**: 23687.78 ❌
- **PnL**: -38.06 points (-1.0R)
- **MFE**: 11.36 points
- **MAE**: 43.68 points

### Trade #1112 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-08 20:30:00
- **FVG 5m**: 23112.15 - 23116.70
- **Entrée**: 23116.95 @ 2025-07-08 20:59:00
- **Stop Loss**: 23069.06
- **Risk**: 47.90 points
- **TP 1RR**: 23164.85 ✅
- **TP 2RR**: 23212.75 ✅
- **TP 3RR**: 23260.64 ✅
- **TP 4RR**: 23308.54 ✅
- **TP 15RR**: 23835.40 ❌
- **PnL**: -47.90 points (-1.0R)
- **MFE**: 223.95 points
- **MAE**: 59.33 points

### Trade #1113 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 04:45:00
- **FVG 5m**: 23146.24 - 23149.52
- **Entrée**: 23145.99 @ 2025-07-09 05:01:00
- **Stop Loss**: 23178.02
- **Risk**: 32.03 points
- **TP 1RR**: 23113.95 ❌
- **TP 2RR**: 23081.92 ❌
- **TP 3RR**: 23049.89 ❌
- **TP 4RR**: 23017.85 ❌
- **TP 15RR**: 22665.48 ❌
- **PnL**: -32.03 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 33.58 points

### Trade #1114 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-09 08:30:00
- **FVG 5m**: 23278.79 - 23283.08
- **Entrée**: 23285.35 @ 2025-07-09 08:42:00
- **Stop Loss**: 23193.97
- **Risk**: 91.39 points
- **TP 1RR**: 23376.74 ❌
- **TP 2RR**: 23468.12 ❌
- **TP 3RR**: 23559.51 ❌
- **TP 4RR**: 23650.89 ❌
- **TP 15RR**: 24656.13 ❌
- **PnL**: -91.39 points (-1.0R)
- **MFE**: 55.54 points
- **MAE**: 95.44 points

### Trade #1115 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-09 08:30:00
- **FVG 5m**: 23278.79 - 23283.08
- **Entrée**: 23285.35 @ 2025-07-09 08:42:00
- **Stop Loss**: 23193.97
- **Risk**: 91.39 points
- **TP 1RR**: 23376.74 ❌
- **TP 2RR**: 23468.12 ❌
- **TP 3RR**: 23559.51 ❌
- **TP 4RR**: 23650.89 ❌
- **TP 15RR**: 24656.13 ❌
- **PnL**: -91.39 points (-1.0R)
- **MFE**: 55.54 points
- **MAE**: 95.44 points

### Trade #1116 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:15:00
- **FVG 5m**: 23277.53 - 23297.22
- **Entrée**: 23277.02 @ 2025-07-09 09:29:00
- **Stop Loss**: 23335.90
- **Risk**: 58.88 points
- **TP 1RR**: 23218.15 ✅
- **TP 2RR**: 23159.27 ✅
- **TP 3RR**: 23100.40 ✅
- **TP 4RR**: 23041.52 ✅
- **TP 15RR**: 22393.89 ❌
- **PnL**: -58.88 points (-1.0R)
- **MFE**: 248.18 points
- **MAE**: 68.17 points

### Trade #1117 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:30:00
- **FVG 5m**: 23193.20 - 23201.53
- **Entrée**: 23189.16 @ 2025-07-09 09:48:00
- **Stop Loss**: 23289.17
- **Risk**: 100.01 points
- **TP 1RR**: 23089.15 ❌
- **TP 2RR**: 22989.15 ❌
- **TP 3RR**: 22889.14 ❌
- **TP 4RR**: 22789.14 ❌
- **TP 15RR**: 21689.08 ❌
- **PnL**: -100.01 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 103.01 points

### Trade #1118 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:30:00
- **FVG 5m**: 23193.20 - 23201.53
- **Entrée**: 23189.16 @ 2025-07-09 09:48:00
- **Stop Loss**: 23289.17
- **Risk**: 100.01 points
- **TP 1RR**: 23089.15 ❌
- **TP 2RR**: 22989.15 ❌
- **TP 3RR**: 22889.14 ❌
- **TP 4RR**: 22789.14 ❌
- **TP 15RR**: 21689.08 ❌
- **PnL**: -100.01 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 103.01 points

### Trade #1119 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23188.66 - 23203.80
- **Entrée**: 23186.38 @ 2025-07-09 10:51:00
- **Stop Loss**: 23238.90
- **Risk**: 52.51 points
- **TP 1RR**: 23133.87 ❌
- **TP 2RR**: 23081.35 ❌
- **TP 3RR**: 23028.84 ❌
- **TP 4RR**: 22976.32 ❌
- **TP 15RR**: 22398.66 ❌
- **PnL**: -52.51 points (-1.0R)
- **MFE**: 22.22 points
- **MAE**: 60.59 points

### Trade #1120 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23188.66 - 23203.80
- **Entrée**: 23186.38 @ 2025-07-09 10:51:00
- **Stop Loss**: 23238.90
- **Risk**: 52.51 points
- **TP 1RR**: 23133.87 ❌
- **TP 2RR**: 23081.35 ❌
- **TP 3RR**: 23028.84 ❌
- **TP 4RR**: 22976.32 ❌
- **TP 15RR**: 22398.66 ❌
- **PnL**: -52.51 points (-1.0R)
- **MFE**: 22.22 points
- **MAE**: 60.59 points

### Trade #1121 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23188.66 - 23203.80
- **Entrée**: 23186.38 @ 2025-07-09 10:51:00
- **Stop Loss**: 23238.90
- **Risk**: 52.51 points
- **TP 1RR**: 23133.87 ❌
- **TP 2RR**: 23081.35 ❌
- **TP 3RR**: 23028.84 ❌
- **TP 4RR**: 22976.32 ❌
- **TP 15RR**: 22398.66 ❌
- **PnL**: -52.51 points (-1.0R)
- **MFE**: 22.22 points
- **MAE**: 60.59 points

### Trade #1122 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-09 09:45:00
- **FVG 5m**: 23188.66 - 23203.80
- **Entrée**: 23186.38 @ 2025-07-09 10:51:00
- **Stop Loss**: 23238.90
- **Risk**: 52.51 points
- **TP 1RR**: 23133.87 ❌
- **TP 2RR**: 23081.35 ❌
- **TP 3RR**: 23028.84 ❌
- **TP 4RR**: 22976.32 ❌
- **TP 15RR**: 22398.66 ❌
- **PnL**: -52.51 points (-1.0R)
- **MFE**: 22.22 points
- **MAE**: 60.59 points

### Trade #1123 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 07:30:00
- **FVG 5m**: 23271.21 - 23291.41
- **Entrée**: 23263.89 @ 2025-07-10 08:33:00
- **Stop Loss**: 23308.36
- **Risk**: 44.47 points
- **TP 1RR**: 23219.42 ✅
- **TP 2RR**: 23174.95 ✅
- **TP 3RR**: 23130.48 ✅
- **TP 4RR**: 23086.01 ✅
- **TP 15RR**: 22596.84 ❌
- **PnL**: -44.47 points (-1.0R)
- **MFE**: 235.06 points
- **MAE**: 48.73 points

### Trade #1124 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 08:30:00
- **FVG 5m**: 23238.39 - 23251.27
- **Entrée**: 23231.32 @ 2025-07-10 08:48:00
- **Stop Loss**: 23330.34
- **Risk**: 99.02 points
- **TP 1RR**: 23132.31 ✅
- **TP 2RR**: 23033.29 ✅
- **TP 3RR**: 22934.28 ❌
- **TP 4RR**: 22835.26 ❌
- **TP 15RR**: 21746.08 ❌
- **PnL**: -99.02 points (-1.0R)
- **MFE**: 202.49 points
- **MAE**: 103.52 points

### Trade #1125 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 08:30:00
- **FVG 5m**: 23238.39 - 23251.27
- **Entrée**: 23231.32 @ 2025-07-10 08:48:00
- **Stop Loss**: 23330.34
- **Risk**: 99.02 points
- **TP 1RR**: 23132.31 ✅
- **TP 2RR**: 23033.29 ✅
- **TP 3RR**: 22934.28 ❌
- **TP 4RR**: 22835.26 ❌
- **TP 15RR**: 21746.08 ❌
- **PnL**: -99.02 points (-1.0R)
- **MFE**: 202.49 points
- **MAE**: 103.52 points

### Trade #1126 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 08:45:00
- **FVG 5m**: 23188.66 - 23195.47
- **Entrée**: 23170.48 @ 2025-07-10 08:58:00
- **Stop Loss**: 23273.50
- **Risk**: 103.03 points
- **TP 1RR**: 23067.45 ❌
- **TP 2RR**: 22964.42 ❌
- **TP 3RR**: 22861.40 ❌
- **TP 4RR**: 22758.37 ❌
- **TP 15RR**: 21625.07 ❌
- **PnL**: -103.03 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 103.52 points

### Trade #1127 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 09:00:00
- **FVG 5m**: 23158.36 - 23166.69
- **Entrée**: 23171.23 @ 2025-07-10 09:11:00
- **Stop Loss**: 23116.50
- **Risk**: 54.74 points
- **TP 1RR**: 23225.97 ✅
- **TP 2RR**: 23280.71 ❌
- **TP 3RR**: 23335.45 ❌
- **TP 4RR**: 23390.18 ❌
- **TP 15RR**: 23992.30 ❌
- **PnL**: -54.74 points (-1.0R)
- **MFE**: 107.05 points
- **MAE**: 73.72 points

### Trade #1128 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 09:00:00
- **FVG 5m**: 23158.36 - 23166.69
- **Entrée**: 23171.23 @ 2025-07-10 09:11:00
- **Stop Loss**: 23116.50
- **Risk**: 54.74 points
- **TP 1RR**: 23225.97 ✅
- **TP 2RR**: 23280.71 ❌
- **TP 3RR**: 23335.45 ❌
- **TP 4RR**: 23390.18 ❌
- **TP 15RR**: 23992.30 ❌
- **PnL**: -54.74 points (-1.0R)
- **MFE**: 107.05 points
- **MAE**: 73.72 points

### Trade #1129 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 10:15:00
- **FVG 5m**: 23207.84 - 23214.16
- **Entrée**: 23218.95 @ 2025-07-10 10:26:00
- **Stop Loss**: 23167.22
- **Risk**: 51.73 points
- **TP 1RR**: 23270.69 ✅
- **TP 2RR**: 23322.42 ❌
- **TP 3RR**: 23374.15 ❌
- **TP 4RR**: 23425.88 ❌
- **TP 15RR**: 23994.95 ❌
- **PnL**: -51.73 points (-1.0R)
- **MFE**: 59.33 points
- **MAE**: 64.13 points

### Trade #1130 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 10:15:00
- **FVG 5m**: 23207.84 - 23214.16
- **Entrée**: 23218.95 @ 2025-07-10 10:26:00
- **Stop Loss**: 23167.22
- **Risk**: 51.73 points
- **TP 1RR**: 23270.69 ✅
- **TP 2RR**: 23322.42 ❌
- **TP 3RR**: 23374.15 ❌
- **TP 4RR**: 23425.88 ❌
- **TP 15RR**: 23994.95 ❌
- **PnL**: -51.73 points (-1.0R)
- **MFE**: 59.33 points
- **MAE**: 64.13 points

### Trade #1131 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 14:45:00
- **FVG 5m**: 23236.63 - 23244.45
- **Entrée**: 23246.98 @ 2025-07-10 15:36:00
- **Stop Loss**: 23206.84
- **Risk**: 40.14 points
- **TP 1RR**: 23287.12 ❌
- **TP 2RR**: 23327.26 ❌
- **TP 3RR**: 23367.39 ❌
- **TP 4RR**: 23407.53 ❌
- **TP 15RR**: 23849.06 ❌
- **PnL**: -40.14 points (-1.0R)
- **MFE**: 30.04 points
- **MAE**: 46.20 points

### Trade #1132 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 19:00:00
- **FVG 5m**: 23188.40 - 23228.29
- **Entrée**: 23187.14 @ 2025-07-10 19:19:00
- **Stop Loss**: 23285.88
- **Risk**: 98.74 points
- **TP 1RR**: 23088.40 ✅
- **TP 2RR**: 22989.66 ❌
- **TP 3RR**: 22890.92 ❌
- **TP 4RR**: 22792.17 ❌
- **TP 15RR**: 21706.02 ❌
- **PnL**: -98.74 points (-1.0R)
- **MFE**: 158.30 points
- **MAE**: 101.75 points

### Trade #1133 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23126.55 - 23131.34
- **Entrée**: 23116.95 @ 2025-07-10 19:33:00
- **Stop Loss**: 23245.72
- **Risk**: 128.77 points
- **TP 1RR**: 22988.19 ❌
- **TP 2RR**: 22859.42 ❌
- **TP 3RR**: 22730.65 ❌
- **TP 4RR**: 22601.89 ❌
- **TP 15RR**: 21185.46 ❌
- **PnL**: -128.77 points (-1.0R)
- **MFE**: 39.39 points
- **MAE**: 132.55 points

### Trade #1134 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23126.55 - 23131.34
- **Entrée**: 23116.95 @ 2025-07-10 19:33:00
- **Stop Loss**: 23245.72
- **Risk**: 128.77 points
- **TP 1RR**: 22988.19 ❌
- **TP 2RR**: 22859.42 ❌
- **TP 3RR**: 22730.65 ❌
- **TP 4RR**: 22601.89 ❌
- **TP 15RR**: 21185.46 ❌
- **PnL**: -128.77 points (-1.0R)
- **MFE**: 39.39 points
- **MAE**: 132.55 points

### Trade #1135 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23123.01 - 23128.82
- **Entrée**: 23130.33 @ 2025-07-10 20:14:00
- **Stop Loss**: 23046.09
- **Risk**: 84.24 points
- **TP 1RR**: 23214.57 ✅
- **TP 2RR**: 23298.82 ❌
- **TP 3RR**: 23383.06 ❌
- **TP 4RR**: 23467.30 ❌
- **TP 15RR**: 24393.96 ❌
- **PnL**: -84.24 points (-1.0R)
- **MFE**: 119.17 points
- **MAE**: 101.50 points

### Trade #1136 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23123.01 - 23128.82
- **Entrée**: 23130.33 @ 2025-07-10 20:14:00
- **Stop Loss**: 23046.09
- **Risk**: 84.24 points
- **TP 1RR**: 23214.57 ✅
- **TP 2RR**: 23298.82 ❌
- **TP 3RR**: 23383.06 ❌
- **TP 4RR**: 23467.30 ❌
- **TP 15RR**: 24393.96 ❌
- **PnL**: -84.24 points (-1.0R)
- **MFE**: 119.17 points
- **MAE**: 101.50 points

### Trade #1137 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 19:15:00
- **FVG 5m**: 23123.01 - 23128.82
- **Entrée**: 23130.33 @ 2025-07-10 20:14:00
- **Stop Loss**: 23046.09
- **Risk**: 84.24 points
- **TP 1RR**: 23214.57 ✅
- **TP 2RR**: 23298.82 ❌
- **TP 3RR**: 23383.06 ❌
- **TP 4RR**: 23467.30 ❌
- **TP 15RR**: 24393.96 ❌
- **PnL**: -84.24 points (-1.0R)
- **MFE**: 119.17 points
- **MAE**: 101.50 points

### Trade #1138 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-10 20:00:00
- **FVG 5m**: 23123.01 - 23128.82
- **Entrée**: 23130.33 @ 2025-07-10 20:14:00
- **Stop Loss**: 23080.41
- **Risk**: 49.92 points
- **TP 1RR**: 23180.26 ✅
- **TP 2RR**: 23230.18 ❌
- **TP 3RR**: 23280.10 ❌
- **TP 4RR**: 23330.02 ❌
- **TP 15RR**: 23879.17 ❌
- **PnL**: -49.92 points (-1.0R)
- **MFE**: 73.98 points
- **MAE**: 50.75 points

### Trade #1139 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-11 05:00:00
- **FVG 5m**: 23125.28 - 23129.07
- **Entrée**: 23130.08 @ 2025-07-11 06:27:00
- **Stop Loss**: 23066.78
- **Risk**: 63.30 points
- **TP 1RR**: 23193.38 ✅
- **TP 2RR**: 23256.67 ❌
- **TP 3RR**: 23319.97 ❌
- **TP 4RR**: 23383.27 ❌
- **TP 15RR**: 24079.53 ❌
- **PnL**: -63.30 points (-1.0R)
- **MFE**: 119.42 points
- **MAE**: 101.24 points

### Trade #1140 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-11 08:30:00
- **FVG 5m**: 23164.42 - 23175.78
- **Entrée**: 23142.70 @ 2025-07-11 10:14:00
- **Stop Loss**: 23197.22
- **Risk**: 54.51 points
- **TP 1RR**: 23088.19 ❌
- **TP 2RR**: 23033.68 ❌
- **TP 3RR**: 22979.16 ❌
- **TP 4RR**: 22924.65 ❌
- **TP 15RR**: 22325.00 ❌
- **PnL**: -54.51 points (-1.0R)
- **MFE**: 7.07 points
- **MAE**: 56.05 points

### Trade #1141 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-11 09:15:00
- **FVG 5m**: 23178.56 - 23185.88
- **Entrée**: 23188.15 @ 2025-07-11 10:34:00
- **Stop Loss**: 23185.14
- **Risk**: 3.01 points
- **TP 1RR**: 23191.16 ✅
- **TP 2RR**: 23194.18 ✅
- **TP 3RR**: 23197.19 ✅
- **TP 4RR**: 23200.21 ✅
- **TP 15RR**: 23233.36 ✅
- **PnL**: 45.21 points (15.0R)
- **MFE**: 50.50 points
- **MAE**: 2.27 points

### Trade #1142 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-11 09:45:00
- **FVG 5m**: 23164.42 - 23175.78
- **Entrée**: 23142.70 @ 2025-07-11 10:14:00
- **Stop Loss**: 23227.53
- **Risk**: 84.83 points
- **TP 1RR**: 23057.88 ❌
- **TP 2RR**: 22973.05 ❌
- **TP 3RR**: 22888.23 ❌
- **TP 4RR**: 22803.40 ❌
- **TP 15RR**: 21870.31 ❌
- **PnL**: -84.83 points (-1.0R)
- **MFE**: 7.07 points
- **MAE**: 95.94 points

### Trade #1143 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-11 14:00:00
- **FVG 5m**: 23205.32 - 23210.37
- **Entrée**: 23211.38 @ 2025-07-11 14:18:00
- **Stop Loss**: 23139.46
- **Risk**: 71.92 points
- **TP 1RR**: 23283.30 ❌
- **TP 2RR**: 23355.21 ❌
- **TP 3RR**: 23427.13 ❌
- **TP 4RR**: 23499.05 ❌
- **TP 15RR**: 24290.14 ❌
- **PnL**: -71.92 points (-1.0R)
- **MFE**: 13.63 points
- **MAE**: 182.54 points

### Trade #1144 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-13 17:00:00
- **FVG 5m**: 23076.30 - 23087.66
- **Entrée**: 23089.43 @ 2025-07-13 17:34:00
- **Stop Loss**: 23017.32
- **Risk**: 72.11 points
- **TP 1RR**: 23161.54 ✅
- **TP 2RR**: 23233.65 ✅
- **TP 3RR**: 23305.76 ✅
- **TP 4RR**: 23377.87 ✅
- **TP 15RR**: 24171.06 ❌
- **PnL**: -72.11 points (-1.0R)
- **MFE**: 991.73 points
- **MAE**: 88.87 points

### Trade #1145 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-13 17:15:00
- **FVG 5m**: 23076.30 - 23087.66
- **Entrée**: 23089.43 @ 2025-07-13 17:34:00
- **Stop Loss**: 23030.70
- **Risk**: 58.73 points
- **TP 1RR**: 23148.17 ❌
- **TP 2RR**: 23206.90 ❌
- **TP 3RR**: 23265.63 ❌
- **TP 4RR**: 23324.37 ❌
- **TP 15RR**: 23970.44 ❌
- **PnL**: -58.73 points (-1.0R)
- **MFE**: 27.77 points
- **MAE**: 59.33 points

### Trade #1146 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-13 17:30:00
- **FVG 5m**: 23085.90 - 23088.67
- **Entrée**: 23093.22 @ 2025-07-13 18:53:00
- **Stop Loss**: 23059.47
- **Risk**: 33.75 points
- **TP 1RR**: 23126.97 ❌
- **TP 2RR**: 23160.73 ❌
- **TP 3RR**: 23194.48 ❌
- **TP 4RR**: 23228.23 ❌
- **TP 15RR**: 23599.52 ❌
- **PnL**: -33.75 points (-1.0R)
- **MFE**: 12.88 points
- **MAE**: 34.59 points

### Trade #1147 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-13 18:00:00
- **FVG 5m**: 23085.90 - 23088.67
- **Entrée**: 23093.22 @ 2025-07-13 18:53:00
- **Stop Loss**: 23054.67
- **Risk**: 38.55 points
- **TP 1RR**: 23131.77 ❌
- **TP 2RR**: 23170.32 ❌
- **TP 3RR**: 23208.86 ❌
- **TP 4RR**: 23247.41 ❌
- **TP 15RR**: 23671.44 ❌
- **PnL**: -38.55 points (-1.0R)
- **MFE**: 12.88 points
- **MAE**: 40.40 points

### Trade #1148 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 02:30:00
- **FVG 5m**: 23069.74 - 23080.60
- **Entrée**: 23082.36 @ 2025-07-14 02:44:00
- **Stop Loss**: 23026.91
- **Risk**: 55.45 points
- **TP 1RR**: 23137.81 ✅
- **TP 2RR**: 23193.26 ✅
- **TP 3RR**: 23248.71 ✅
- **TP 4RR**: 23304.16 ✅
- **TP 15RR**: 23914.11 ✅
- **PnL**: 831.75 points (15.0R)
- **MFE**: 841.25 points
- **MAE**: 20.70 points

### Trade #1149 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 02:30:00
- **FVG 5m**: 23069.74 - 23080.60
- **Entrée**: 23082.36 @ 2025-07-14 02:44:00
- **Stop Loss**: 23026.91
- **Risk**: 55.45 points
- **TP 1RR**: 23137.81 ✅
- **TP 2RR**: 23193.26 ✅
- **TP 3RR**: 23248.71 ✅
- **TP 4RR**: 23304.16 ✅
- **TP 15RR**: 23914.11 ✅
- **PnL**: 831.75 points (15.0R)
- **MFE**: 841.25 points
- **MAE**: 20.70 points

### Trade #1150 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 08:15:00
- **FVG 5m**: 23166.94 - 23170.48
- **Entrée**: 23172.24 @ 2025-07-14 09:14:00
- **Stop Loss**: 23111.70
- **Risk**: 60.54 points
- **TP 1RR**: 23232.79 ✅
- **TP 2RR**: 23293.33 ✅
- **TP 3RR**: 23353.87 ✅
- **TP 4RR**: 23414.41 ✅
- **TP 15RR**: 24080.37 ❌
- **PnL**: -60.54 points (-1.0R)
- **MFE**: 280.50 points
- **MAE**: 70.95 points

### Trade #1151 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 08:15:00
- **FVG 5m**: 23166.94 - 23170.48
- **Entrée**: 23172.24 @ 2025-07-14 09:14:00
- **Stop Loss**: 23111.70
- **Risk**: 60.54 points
- **TP 1RR**: 23232.79 ✅
- **TP 2RR**: 23293.33 ✅
- **TP 3RR**: 23353.87 ✅
- **TP 4RR**: 23414.41 ✅
- **TP 15RR**: 24080.37 ❌
- **PnL**: -60.54 points (-1.0R)
- **MFE**: 280.50 points
- **MAE**: 70.95 points

### Trade #1152 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 08:30:00
- **FVG 5m**: 23172.24 - 23185.63
- **Entrée**: 23162.15 @ 2025-07-14 09:28:00
- **Stop Loss**: 23218.44
- **Risk**: 56.29 points
- **TP 1RR**: 23105.85 ❌
- **TP 2RR**: 23049.56 ❌
- **TP 3RR**: 22993.27 ❌
- **TP 4RR**: 22936.98 ❌
- **TP 15RR**: 22317.77 ❌
- **PnL**: -56.29 points (-1.0R)
- **MFE**: 12.12 points
- **MAE**: 57.82 points

### Trade #1153 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 08:30:00
- **FVG 5m**: 23172.24 - 23185.63
- **Entrée**: 23162.15 @ 2025-07-14 09:28:00
- **Stop Loss**: 23218.44
- **Risk**: 56.29 points
- **TP 1RR**: 23105.85 ❌
- **TP 2RR**: 23049.56 ❌
- **TP 3RR**: 22993.27 ❌
- **TP 4RR**: 22936.98 ❌
- **TP 15RR**: 22317.77 ❌
- **PnL**: -56.29 points (-1.0R)
- **MFE**: 12.12 points
- **MAE**: 57.82 points

### Trade #1154 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 08:45:00
- **FVG 5m**: 23166.94 - 23170.48
- **Entrée**: 23172.24 @ 2025-07-14 09:14:00
- **Stop Loss**: 23056.94
- **Risk**: 115.30 points
- **TP 1RR**: 23287.55 ✅
- **TP 2RR**: 23402.85 ✅
- **TP 3RR**: 23518.15 ✅
- **TP 4RR**: 23633.45 ✅
- **TP 15RR**: 24901.77 ❌
- **PnL**: -115.30 points (-1.0R)
- **MFE**: 908.91 points
- **MAE**: 128.26 points

### Trade #1155 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-14 12:30:00
- **FVG 5m**: 23275.25 - 23279.55
- **Entrée**: 23273.49 @ 2025-07-14 14:08:00
- **Stop Loss**: 23306.59
- **Risk**: 33.11 points
- **TP 1RR**: 23240.38 ✅
- **TP 2RR**: 23207.27 ❌
- **TP 3RR**: 23174.16 ❌
- **TP 4RR**: 23141.06 ❌
- **TP 15RR**: 22776.87 ❌
- **PnL**: -33.11 points (-1.0R)
- **MFE**: 49.74 points
- **MAE**: 34.34 points

### Trade #1156 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-14 19:00:00
- **FVG 5m**: 23233.85 - 23240.16
- **Entrée**: 23240.41 @ 2025-07-14 20:39:00
- **Stop Loss**: 23213.65
- **Risk**: 26.76 points
- **TP 1RR**: 23267.17 ✅
- **TP 2RR**: 23293.94 ✅
- **TP 3RR**: 23320.70 ✅
- **TP 4RR**: 23347.46 ✅
- **TP 15RR**: 23641.83 ❌
- **PnL**: -26.76 points (-1.0R)
- **MFE**: 212.33 points
- **MAE**: 38.12 points

### Trade #1157 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 06:15:00
- **FVG 5m**: 23399.22 - 23402.00
- **Entrée**: 23398.46 @ 2025-07-15 06:44:00
- **Stop Loss**: 23430.12
- **Risk**: 31.65 points
- **TP 1RR**: 23366.81 ✅
- **TP 2RR**: 23335.15 ❌
- **TP 3RR**: 23303.50 ❌
- **TP 4RR**: 23271.84 ❌
- **TP 15RR**: 22923.64 ❌
- **PnL**: -31.65 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 35.85 points

### Trade #1158 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 07:30:00
- **FVG 5m**: 23415.13 - 23428.00
- **Entrée**: 23401.49 @ 2025-07-15 08:33:00
- **Stop Loss**: 23446.03
- **Risk**: 44.54 points
- **TP 1RR**: 23356.95 ✅
- **TP 2RR**: 23312.41 ✅
- **TP 3RR**: 23267.88 ✅
- **TP 4RR**: 23223.34 ✅
- **TP 15RR**: 22733.41 ❌
- **PnL**: -44.54 points (-1.0R)
- **MFE**: 339.83 points
- **MAE**: 45.19 points

### Trade #1159 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 07:30:00
- **FVG 5m**: 23415.13 - 23428.00
- **Entrée**: 23401.49 @ 2025-07-15 08:33:00
- **Stop Loss**: 23446.03
- **Risk**: 44.54 points
- **TP 1RR**: 23356.95 ✅
- **TP 2RR**: 23312.41 ✅
- **TP 3RR**: 23267.88 ✅
- **TP 4RR**: 23223.34 ✅
- **TP 15RR**: 22733.41 ❌
- **PnL**: -44.54 points (-1.0R)
- **MFE**: 339.83 points
- **MAE**: 45.19 points

### Trade #1160 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 09:45:00
- **FVG 5m**: 23359.83 - 23365.14
- **Entrée**: 23354.03 @ 2025-07-15 11:54:00
- **Stop Loss**: 23405.61
- **Risk**: 51.59 points
- **TP 1RR**: 23302.44 ❌
- **TP 2RR**: 23250.85 ❌
- **TP 3RR**: 23199.26 ❌
- **TP 4RR**: 23147.67 ❌
- **TP 15RR**: 22580.20 ❌
- **PnL**: -51.59 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 53.02 points

### Trade #1161 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 11:45:00
- **FVG 5m**: 23349.73 - 23357.06
- **Entrée**: 23359.08 @ 2025-07-15 12:34:00
- **Stop Loss**: 23299.96
- **Risk**: 59.12 points
- **TP 1RR**: 23418.20 ❌
- **TP 2RR**: 23477.32 ❌
- **TP 3RR**: 23536.44 ❌
- **TP 4RR**: 23595.56 ❌
- **TP 15RR**: 24245.90 ❌
- **PnL**: -59.12 points (-1.0R)
- **MFE**: 50.50 points
- **MAE**: 60.59 points

### Trade #1162 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 12:30:00
- **FVG 5m**: 23373.97 - 23381.80
- **Entrée**: 23386.34 @ 2025-07-15 12:54:00
- **Stop Loss**: 23334.78
- **Risk**: 51.56 points
- **TP 1RR**: 23437.91 ❌
- **TP 2RR**: 23489.47 ❌
- **TP 3RR**: 23541.04 ❌
- **TP 4RR**: 23592.60 ❌
- **TP 15RR**: 24159.81 ❌
- **PnL**: -51.56 points (-1.0R)
- **MFE**: 23.23 points
- **MAE**: 54.03 points

### Trade #1163 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 14:45:00
- **FVG 5m**: 23287.88 - 23316.91
- **Entrée**: 23280.30 @ 2025-07-15 14:59:00
- **Stop Loss**: 23357.37
- **Risk**: 77.06 points
- **TP 1RR**: 23203.24 ✅
- **TP 2RR**: 23126.18 ✅
- **TP 3RR**: 23049.11 ❌
- **TP 4RR**: 22972.05 ❌
- **TP 15RR**: 22124.34 ❌
- **PnL**: -77.06 points (-1.0R)
- **MFE**: 218.64 points
- **MAE**: 77.76 points

### Trade #1164 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 17:00:00
- **FVG 5m**: 23236.63 - 23243.95
- **Entrée**: 23235.87 @ 2025-07-15 17:12:00
- **Stop Loss**: 23274.01
- **Risk**: 38.14 points
- **TP 1RR**: 23197.73 ✅
- **TP 2RR**: 23159.59 ✅
- **TP 3RR**: 23121.44 ❌
- **TP 4RR**: 23083.30 ❌
- **TP 15RR**: 22663.75 ❌
- **PnL**: -38.14 points (-1.0R)
- **MFE**: 79.78 points
- **MAE**: 77.76 points

### Trade #1165 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 17:00:00
- **FVG 5m**: 23236.63 - 23243.95
- **Entrée**: 23235.87 @ 2025-07-15 17:12:00
- **Stop Loss**: 23274.01
- **Risk**: 38.14 points
- **TP 1RR**: 23197.73 ✅
- **TP 2RR**: 23159.59 ✅
- **TP 3RR**: 23121.44 ❌
- **TP 4RR**: 23083.30 ❌
- **TP 15RR**: 22663.75 ❌
- **PnL**: -38.14 points (-1.0R)
- **MFE**: 79.78 points
- **MAE**: 77.76 points

### Trade #1166 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-15 17:00:00
- **FVG 5m**: 23236.63 - 23243.95
- **Entrée**: 23235.87 @ 2025-07-15 17:12:00
- **Stop Loss**: 23274.01
- **Risk**: 38.14 points
- **TP 1RR**: 23197.73 ✅
- **TP 2RR**: 23159.59 ✅
- **TP 3RR**: 23121.44 ❌
- **TP 4RR**: 23083.30 ❌
- **TP 15RR**: 22663.75 ❌
- **PnL**: -38.14 points (-1.0R)
- **MFE**: 79.78 points
- **MAE**: 77.76 points

### Trade #1167 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 17:45:00
- **FVG 5m**: 23222.99 - 23228.80
- **Entrée**: 23230.57 @ 2025-07-15 18:35:00
- **Stop Loss**: 23200.78
- **Risk**: 29.78 points
- **TP 1RR**: 23260.35 ✅
- **TP 2RR**: 23290.13 ❌
- **TP 3RR**: 23319.92 ❌
- **TP 4RR**: 23349.70 ❌
- **TP 15RR**: 23677.33 ❌
- **PnL**: -29.78 points (-1.0R)
- **MFE**: 42.92 points
- **MAE**: 34.34 points

### Trade #1168 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-15 19:30:00
- **FVG 5m**: 23232.08 - 23239.15
- **Entrée**: 23240.16 @ 2025-07-15 20:08:00
- **Stop Loss**: 23198.26
- **Risk**: 41.90 points
- **TP 1RR**: 23282.06 ❌
- **TP 2RR**: 23323.96 ❌
- **TP 3RR**: 23365.87 ❌
- **TP 4RR**: 23407.77 ❌
- **TP 15RR**: 23868.69 ❌
- **PnL**: -41.90 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 43.93 points

### Trade #1169 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-16 02:15:00
- **FVG 5m**: 23218.70 - 23221.98
- **Entrée**: 23222.99 @ 2025-07-16 03:33:00
- **Stop Loss**: 23173.78
- **Risk**: 49.21 points
- **TP 1RR**: 23272.20 ✅
- **TP 2RR**: 23321.41 ❌
- **TP 3RR**: 23370.63 ❌
- **TP 4RR**: 23419.84 ❌
- **TP 15RR**: 23961.17 ❌
- **PnL**: -49.21 points (-1.0R)
- **MFE**: 95.18 points
- **MAE**: 49.99 points

### Trade #1170 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-16 02:15:00
- **FVG 5m**: 23218.70 - 23221.98
- **Entrée**: 23222.99 @ 2025-07-16 03:33:00
- **Stop Loss**: 23173.78
- **Risk**: 49.21 points
- **TP 1RR**: 23272.20 ✅
- **TP 2RR**: 23321.41 ❌
- **TP 3RR**: 23370.63 ❌
- **TP 4RR**: 23419.84 ❌
- **TP 15RR**: 23961.17 ❌
- **PnL**: -49.21 points (-1.0R)
- **MFE**: 95.18 points
- **MAE**: 49.99 points

### Trade #1171 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23213.40 - 23224.25
- **Entrée**: 23202.79 @ 2025-07-16 08:51:00
- **Stop Loss**: 23329.83
- **Risk**: 127.04 points
- **TP 1RR**: 23075.75 ✅
- **TP 2RR**: 22948.71 ❌
- **TP 3RR**: 22821.67 ❌
- **TP 4RR**: 22694.63 ❌
- **TP 15RR**: 21297.18 ❌
- **PnL**: -127.04 points (-1.0R)
- **MFE**: 141.13 points
- **MAE**: 129.77 points

### Trade #1172 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23213.40 - 23224.25
- **Entrée**: 23202.79 @ 2025-07-16 08:51:00
- **Stop Loss**: 23329.83
- **Risk**: 127.04 points
- **TP 1RR**: 23075.75 ✅
- **TP 2RR**: 22948.71 ❌
- **TP 3RR**: 22821.67 ❌
- **TP 4RR**: 22694.63 ❌
- **TP 15RR**: 21297.18 ❌
- **PnL**: -127.04 points (-1.0R)
- **MFE**: 141.13 points
- **MAE**: 129.77 points

### Trade #1173 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23213.40 - 23224.25
- **Entrée**: 23202.79 @ 2025-07-16 08:51:00
- **Stop Loss**: 23329.83
- **Risk**: 127.04 points
- **TP 1RR**: 23075.75 ✅
- **TP 2RR**: 22948.71 ❌
- **TP 3RR**: 22821.67 ❌
- **TP 4RR**: 22694.63 ❌
- **TP 15RR**: 21297.18 ❌
- **PnL**: -127.04 points (-1.0R)
- **MFE**: 141.13 points
- **MAE**: 129.77 points

### Trade #1174 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 08:30:00
- **FVG 5m**: 23213.40 - 23224.25
- **Entrée**: 23202.79 @ 2025-07-16 08:51:00
- **Stop Loss**: 23329.83
- **Risk**: 127.04 points
- **TP 1RR**: 23075.75 ✅
- **TP 2RR**: 22948.71 ❌
- **TP 3RR**: 22821.67 ❌
- **TP 4RR**: 22694.63 ❌
- **TP 15RR**: 21297.18 ❌
- **PnL**: -127.04 points (-1.0R)
- **MFE**: 141.13 points
- **MAE**: 129.77 points

### Trade #1175 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-16 10:15:00
- **FVG 5m**: 23125.03 - 23146.24
- **Entrée**: 23148.01 @ 2025-07-16 10:42:00
- **Stop Loss**: 23113.72
- **Risk**: 34.29 points
- **TP 1RR**: 23182.29 ✅
- **TP 2RR**: 23216.58 ✅
- **TP 3RR**: 23250.86 ✅
- **TP 4RR**: 23285.15 ✅
- **TP 15RR**: 23662.29 ✅
- **PnL**: 514.28 points (15.0R)
- **MFE**: 518.84 points
- **MAE**: 7.83 points

### Trade #1176 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-16 14:00:00
- **FVG 5m**: 23304.04 - 23307.07
- **Entrée**: 23303.53 @ 2025-07-16 14:59:00
- **Stop Loss**: 23323.01
- **Risk**: 19.48 points
- **TP 1RR**: 23284.05 ✅
- **TP 2RR**: 23264.57 ✅
- **TP 3RR**: 23245.08 ✅
- **TP 4RR**: 23225.60 ❌
- **TP 15RR**: 23011.30 ❌
- **PnL**: -19.48 points (-1.0R)
- **MFE**: 58.57 points
- **MAE**: 20.20 points

### Trade #1177 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-17 06:00:00
- **FVG 5m**: 23318.18 - 23321.96
- **Entrée**: 23324.74 @ 2025-07-17 07:02:00
- **Stop Loss**: 23288.85
- **Risk**: 35.89 points
- **TP 1RR**: 23360.63 ✅
- **TP 2RR**: 23396.52 ✅
- **TP 3RR**: 23432.40 ✅
- **TP 4RR**: 23468.29 ✅
- **TP 15RR**: 23863.06 ✅
- **PnL**: 538.32 points (15.0R)
- **MFE**: 540.80 points
- **MAE**: 30.55 points

### Trade #1178 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-17 07:00:00
- **FVG 5m**: 23318.68 - 23321.96
- **Entrée**: 23315.40 @ 2025-07-17 07:14:00
- **Stop Loss**: 23342.21
- **Risk**: 26.81 points
- **TP 1RR**: 23288.58 ❌
- **TP 2RR**: 23261.77 ❌
- **TP 3RR**: 23234.96 ❌
- **TP 4RR**: 23208.14 ❌
- **TP 15RR**: 22913.19 ❌
- **PnL**: -26.81 points (-1.0R)
- **MFE**: 13.63 points
- **MAE**: 33.83 points

### Trade #1179 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 02:00:00
- **FVG 5m**: 23510.81 - 23518.39
- **Entrée**: 23507.78 @ 2025-07-18 02:12:00
- **Stop Loss**: 23535.20
- **Risk**: 27.42 points
- **TP 1RR**: 23480.37 ❌
- **TP 2RR**: 23452.95 ❌
- **TP 3RR**: 23425.54 ❌
- **TP 4RR**: 23398.12 ❌
- **TP 15RR**: 23096.56 ❌
- **PnL**: -27.42 points (-1.0R)
- **MFE**: 26.26 points
- **MAE**: 43.93 points

### Trade #1180 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 02:00:00
- **FVG 5m**: 23510.81 - 23518.39
- **Entrée**: 23507.78 @ 2025-07-18 02:12:00
- **Stop Loss**: 23535.20
- **Risk**: 27.42 points
- **TP 1RR**: 23480.37 ❌
- **TP 2RR**: 23452.95 ❌
- **TP 3RR**: 23425.54 ❌
- **TP 4RR**: 23398.12 ❌
- **TP 15RR**: 23096.56 ❌
- **PnL**: -27.42 points (-1.0R)
- **MFE**: 26.26 points
- **MAE**: 43.93 points

### Trade #1181 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-18 02:00:00
- **FVG 5m**: 23510.81 - 23518.39
- **Entrée**: 23507.78 @ 2025-07-18 02:12:00
- **Stop Loss**: 23535.20
- **Risk**: 27.42 points
- **TP 1RR**: 23480.37 ❌
- **TP 2RR**: 23452.95 ❌
- **TP 3RR**: 23425.54 ❌
- **TP 4RR**: 23398.12 ❌
- **TP 15RR**: 23096.56 ❌
- **PnL**: -27.42 points (-1.0R)
- **MFE**: 26.26 points
- **MAE**: 43.93 points

### Trade #1182 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-20 18:45:00
- **FVG 5m**: 23485.82 - 23488.85
- **Entrée**: 23490.36 @ 2025-07-20 20:03:00
- **Stop Loss**: 23463.23
- **Risk**: 27.14 points
- **TP 1RR**: 23517.50 ✅
- **TP 2RR**: 23544.64 ❌
- **TP 3RR**: 23571.78 ❌
- **TP 4RR**: 23598.92 ❌
- **TP 15RR**: 23897.44 ❌
- **PnL**: -27.14 points (-1.0R)
- **MFE**: 48.98 points
- **MAE**: 33.58 points

### Trade #1183 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-21 07:45:00
- **FVG 5m**: 23472.94 - 23481.27
- **Entrée**: 23470.67 @ 2025-07-21 07:56:00
- **Stop Loss**: 23510.44
- **Risk**: 39.77 points
- **TP 1RR**: 23430.90 ❌
- **TP 2RR**: 23391.12 ❌
- **TP 3RR**: 23351.35 ❌
- **TP 4RR**: 23311.57 ❌
- **TP 15RR**: 22874.06 ❌
- **PnL**: -39.77 points (-1.0R)
- **MFE**: 16.92 points
- **MAE**: 46.46 points

### Trade #1184 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-21 08:15:00
- **FVG 5m**: 23476.73 - 23485.57
- **Entrée**: 23485.82 @ 2025-07-21 08:29:00
- **Stop Loss**: 23446.32
- **Risk**: 39.50 points
- **TP 1RR**: 23525.32 ✅
- **TP 2RR**: 23564.82 ✅
- **TP 3RR**: 23604.32 ✅
- **TP 4RR**: 23643.82 ✅
- **TP 15RR**: 24078.34 ❌
- **PnL**: -39.50 points (-1.0R)
- **MFE**: 170.93 points
- **MAE**: 45.45 points

### Trade #1185 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-21 08:15:00
- **FVG 5m**: 23476.73 - 23485.57
- **Entrée**: 23485.82 @ 2025-07-21 08:29:00
- **Stop Loss**: 23446.32
- **Risk**: 39.50 points
- **TP 1RR**: 23525.32 ✅
- **TP 2RR**: 23564.82 ✅
- **TP 3RR**: 23604.32 ✅
- **TP 4RR**: 23643.82 ✅
- **TP 15RR**: 24078.34 ❌
- **PnL**: -39.50 points (-1.0R)
- **MFE**: 170.93 points
- **MAE**: 45.45 points

### Trade #1186 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-21 08:30:00
- **FVG 5m**: 23561.56 - 23568.88
- **Entrée**: 23576.71 @ 2025-07-21 08:42:00
- **Stop Loss**: 23473.82
- **Risk**: 102.89 points
- **TP 1RR**: 23679.60 ❌
- **TP 2RR**: 23782.48 ❌
- **TP 3RR**: 23885.37 ❌
- **TP 4RR**: 23988.26 ❌
- **TP 15RR**: 25120.01 ❌
- **PnL**: -102.89 points (-1.0R)
- **MFE**: 80.03 points
- **MAE**: 114.62 points

### Trade #1187 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23540.35 - 23546.92
- **Entrée**: 23537.07 @ 2025-07-22 03:04:00
- **Stop Loss**: 23579.91
- **Risk**: 42.84 points
- **TP 1RR**: 23494.23 ❌
- **TP 2RR**: 23451.39 ❌
- **TP 3RR**: 23408.56 ❌
- **TP 4RR**: 23365.72 ❌
- **TP 15RR**: 22894.49 ❌
- **PnL**: -42.84 points (-1.0R)
- **MFE**: 39.13 points
- **MAE**: 43.93 points

### Trade #1188 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23540.35 - 23546.92
- **Entrée**: 23537.07 @ 2025-07-22 03:04:00
- **Stop Loss**: 23579.91
- **Risk**: 42.84 points
- **TP 1RR**: 23494.23 ❌
- **TP 2RR**: 23451.39 ❌
- **TP 3RR**: 23408.56 ❌
- **TP 4RR**: 23365.72 ❌
- **TP 15RR**: 22894.49 ❌
- **PnL**: -42.84 points (-1.0R)
- **MFE**: 39.13 points
- **MAE**: 43.93 points

### Trade #1189 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23540.35 - 23546.92
- **Entrée**: 23537.07 @ 2025-07-22 03:04:00
- **Stop Loss**: 23579.91
- **Risk**: 42.84 points
- **TP 1RR**: 23494.23 ❌
- **TP 2RR**: 23451.39 ❌
- **TP 3RR**: 23408.56 ❌
- **TP 4RR**: 23365.72 ❌
- **TP 15RR**: 22894.49 ❌
- **PnL**: -42.84 points (-1.0R)
- **MFE**: 39.13 points
- **MAE**: 43.93 points

### Trade #1190 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 02:45:00
- **FVG 5m**: 23514.60 - 23523.94
- **Entrée**: 23524.70 @ 2025-07-22 05:02:00
- **Stop Loss**: 23502.09
- **Risk**: 22.61 points
- **TP 1RR**: 23547.31 ✅
- **TP 2RR**: 23569.93 ✅
- **TP 3RR**: 23592.54 ❌
- **TP 4RR**: 23615.15 ❌
- **TP 15RR**: 23863.90 ❌
- **PnL**: -22.61 points (-1.0R)
- **MFE**: 56.30 points
- **MAE**: 22.98 points

### Trade #1191 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 09:00:00
- **FVG 5m**: 23402.25 - 23430.78
- **Entrée**: 23432.04 @ 2025-07-22 09:34:00
- **Stop Loss**: 23325.19
- **Risk**: 106.85 points
- **TP 1RR**: 23538.89 ✅
- **TP 2RR**: 23645.75 ✅
- **TP 3RR**: 23752.60 ✅
- **TP 4RR**: 23859.45 ✅
- **TP 15RR**: 25034.82 ❌
- **PnL**: -106.85 points (-1.0R)
- **MFE**: 649.12 points
- **MAE**: 116.39 points

### Trade #1192 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 09:30:00
- **FVG 5m**: 23410.58 - 23416.14
- **Entrée**: 23418.41 @ 2025-07-22 11:51:00
- **Stop Loss**: 23384.49
- **Risk**: 33.92 points
- **TP 1RR**: 23452.32 ✅
- **TP 2RR**: 23486.24 ✅
- **TP 3RR**: 23520.16 ❌
- **TP 4RR**: 23554.07 ❌
- **TP 15RR**: 23927.15 ❌
- **PnL**: -33.92 points (-1.0R)
- **MFE**: 95.94 points
- **MAE**: 35.09 points

### Trade #1193 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 09:45:00
- **FVG 5m**: 23410.58 - 23416.14
- **Entrée**: 23418.41 @ 2025-07-22 11:51:00
- **Stop Loss**: 23414.27
- **Risk**: 4.14 points
- **TP 1RR**: 23422.55 ✅
- **TP 2RR**: 23426.69 ✅
- **TP 3RR**: 23430.82 ✅
- **TP 4RR**: 23434.96 ✅
- **TP 15RR**: 23480.49 ✅
- **PnL**: 62.08 points (15.0R)
- **MFE**: 62.61 points
- **MAE**: 2.27 points

### Trade #1194 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 12:15:00
- **FVG 5m**: 23454.26 - 23466.38
- **Entrée**: 23477.49 @ 2025-07-22 12:28:00
- **Stop Loss**: 23420.33
- **Risk**: 57.16 points
- **TP 1RR**: 23534.65 ❌
- **TP 2RR**: 23591.81 ❌
- **TP 3RR**: 23648.97 ❌
- **TP 4RR**: 23706.13 ❌
- **TP 15RR**: 24334.91 ❌
- **PnL**: -57.16 points (-1.0R)
- **MFE**: 0.50 points
- **MAE**: 65.90 points

### Trade #1195 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 12:15:00
- **FVG 5m**: 23454.26 - 23466.38
- **Entrée**: 23477.49 @ 2025-07-22 12:28:00
- **Stop Loss**: 23420.33
- **Risk**: 57.16 points
- **TP 1RR**: 23534.65 ❌
- **TP 2RR**: 23591.81 ❌
- **TP 3RR**: 23648.97 ❌
- **TP 4RR**: 23706.13 ❌
- **TP 15RR**: 24334.91 ❌
- **PnL**: -57.16 points (-1.0R)
- **MFE**: 0.50 points
- **MAE**: 65.90 points

### Trade #1196 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 14:00:00
- **FVG 5m**: 23453.75 - 23460.82
- **Entrée**: 23451.99 @ 2025-07-22 14:59:00
- **Stop Loss**: 23499.84
- **Risk**: 47.85 points
- **TP 1RR**: 23404.14 ✅
- **TP 2RR**: 23356.29 ❌
- **TP 3RR**: 23308.44 ❌
- **TP 4RR**: 23260.60 ❌
- **TP 15RR**: 22734.27 ❌
- **PnL**: -47.85 points (-1.0R)
- **MFE**: 52.26 points
- **MAE**: 47.97 points

### Trade #1197 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-22 18:45:00
- **FVG 5m**: 23442.39 - 23450.47
- **Entrée**: 23454.76 @ 2025-07-22 20:15:00
- **Stop Loss**: 23453.38
- **Risk**: 1.38 points
- **TP 1RR**: 23456.15 ✅
- **TP 2RR**: 23457.53 ✅
- **TP 3RR**: 23458.91 ✅
- **TP 4RR**: 23460.29 ✅
- **TP 15RR**: 23475.48 ✅
- **PnL**: 20.72 points (15.0R)
- **MFE**: 21.46 points
- **MAE**: 0.76 points

### Trade #1198 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-22 19:00:00
- **FVG 5m**: 23462.59 - 23472.19
- **Entrée**: 23461.58 @ 2025-07-22 21:14:00
- **Stop Loss**: 23509.18
- **Risk**: 47.60 points
- **TP 1RR**: 23413.98 ❌
- **TP 2RR**: 23366.38 ❌
- **TP 3RR**: 23318.78 ❌
- **TP 4RR**: 23271.18 ❌
- **TP 15RR**: 22747.58 ❌
- **PnL**: -47.60 points (-1.0R)
- **MFE**: 5.55 points
- **MAE**: 47.97 points

### Trade #1199 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 09:15:00
- **FVG 5m**: 23415.13 - 23418.66
- **Entrée**: 23421.44 @ 2025-07-23 09:51:00
- **Stop Loss**: 23366.58
- **Risk**: 54.86 points
- **TP 1RR**: 23476.30 ✅
- **TP 2RR**: 23531.16 ✅
- **TP 3RR**: 23586.03 ✅
- **TP 4RR**: 23640.89 ✅
- **TP 15RR**: 24244.38 ❌
- **PnL**: -54.86 points (-1.0R)
- **MFE**: 659.72 points
- **MAE**: 65.14 points

### Trade #1200 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 09:15:00
- **FVG 5m**: 23415.13 - 23418.66
- **Entrée**: 23421.44 @ 2025-07-23 09:51:00
- **Stop Loss**: 23366.58
- **Risk**: 54.86 points
- **TP 1RR**: 23476.30 ✅
- **TP 2RR**: 23531.16 ✅
- **TP 3RR**: 23586.03 ✅
- **TP 4RR**: 23640.89 ✅
- **TP 15RR**: 24244.38 ❌
- **PnL**: -54.86 points (-1.0R)
- **MFE**: 659.72 points
- **MAE**: 65.14 points

### Trade #1201 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 09:45:00
- **FVG 5m**: 23448.20 - 23473.45
- **Entrée**: 23492.64 @ 2025-07-23 10:54:00
- **Stop Loss**: 23385.75
- **Risk**: 106.88 points
- **TP 1RR**: 23599.52 ✅
- **TP 2RR**: 23706.40 ✅
- **TP 3RR**: 23813.28 ✅
- **TP 4RR**: 23920.16 ✅
- **TP 15RR**: 25095.87 ❌
- **PnL**: -106.88 points (-1.0R)
- **MFE**: 588.52 points
- **MAE**: 110.33 points

### Trade #1202 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23469.66 - 23473.45
- **Entrée**: 23467.39 @ 2025-07-23 11:12:00
- **Stop Loss**: 23535.96
- **Risk**: 68.57 points
- **TP 1RR**: 23398.82 ❌
- **TP 2RR**: 23330.25 ❌
- **TP 3RR**: 23261.68 ❌
- **TP 4RR**: 23193.11 ❌
- **TP 15RR**: 22438.85 ❌
- **PnL**: -68.57 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 70.19 points

### Trade #1203 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23469.66 - 23473.45
- **Entrée**: 23467.39 @ 2025-07-23 11:12:00
- **Stop Loss**: 23535.96
- **Risk**: 68.57 points
- **TP 1RR**: 23398.82 ❌
- **TP 2RR**: 23330.25 ❌
- **TP 3RR**: 23261.68 ❌
- **TP 4RR**: 23193.11 ❌
- **TP 15RR**: 22438.85 ❌
- **PnL**: -68.57 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 70.19 points

### Trade #1204 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23469.66 - 23473.45
- **Entrée**: 23467.39 @ 2025-07-23 11:12:00
- **Stop Loss**: 23535.96
- **Risk**: 68.57 points
- **TP 1RR**: 23398.82 ❌
- **TP 2RR**: 23330.25 ❌
- **TP 3RR**: 23261.68 ❌
- **TP 4RR**: 23193.11 ❌
- **TP 15RR**: 22438.85 ❌
- **PnL**: -68.57 points (-1.0R)
- **MFE**: 44.94 points
- **MAE**: 70.19 points

### Trade #1205 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23458.05 - 23461.08
- **Entrée**: 23462.59 @ 2025-07-23 12:23:00
- **Stop Loss**: 23420.33
- **Risk**: 42.27 points
- **TP 1RR**: 23504.86 ✅
- **TP 2RR**: 23547.12 ✅
- **TP 3RR**: 23589.39 ✅
- **TP 4RR**: 23631.65 ✅
- **TP 15RR**: 24096.58 ❌
- **PnL**: -42.27 points (-1.0R)
- **MFE**: 618.57 points
- **MAE**: 42.67 points

### Trade #1206 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23458.05 - 23461.08
- **Entrée**: 23462.59 @ 2025-07-23 12:23:00
- **Stop Loss**: 23420.33
- **Risk**: 42.27 points
- **TP 1RR**: 23504.86 ✅
- **TP 2RR**: 23547.12 ✅
- **TP 3RR**: 23589.39 ✅
- **TP 4RR**: 23631.65 ✅
- **TP 15RR**: 24096.58 ❌
- **PnL**: -42.27 points (-1.0R)
- **MFE**: 618.57 points
- **MAE**: 42.67 points

### Trade #1207 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 10:45:00
- **FVG 5m**: 23458.05 - 23461.08
- **Entrée**: 23462.59 @ 2025-07-23 12:23:00
- **Stop Loss**: 23420.33
- **Risk**: 42.27 points
- **TP 1RR**: 23504.86 ✅
- **TP 2RR**: 23547.12 ✅
- **TP 3RR**: 23589.39 ✅
- **TP 4RR**: 23631.65 ✅
- **TP 15RR**: 24096.58 ❌
- **PnL**: -42.27 points (-1.0R)
- **MFE**: 618.57 points
- **MAE**: 42.67 points

### Trade #1208 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-23 15:00:00
- **FVG 5m**: 23584.79 - 23609.03
- **Entrée**: 23611.80 @ 2025-07-23 15:12:00
- **Stop Loss**: 23522.28
- **Risk**: 89.53 points
- **TP 1RR**: 23701.33 ✅
- **TP 2RR**: 23790.86 ✅
- **TP 3RR**: 23880.39 ✅
- **TP 4RR**: 23969.92 ✅
- **TP 15RR**: 24954.75 ❌
- **PnL**: -89.53 points (-1.0R)
- **MFE**: 469.35 points
- **MAE**: 90.64 points

### Trade #1209 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-23 15:15:00
- **FVG 5m**: 23630.24 - 23634.28
- **Entrée**: 23626.45 @ 2025-07-23 17:02:00
- **Stop Loss**: 23645.59
- **Risk**: 19.14 points
- **TP 1RR**: 23607.31 ❌
- **TP 2RR**: 23588.17 ❌
- **TP 3RR**: 23569.03 ❌
- **TP 4RR**: 23549.89 ❌
- **TP 15RR**: 23339.37 ❌
- **PnL**: -19.14 points (-1.0R)
- **MFE**: 12.88 points
- **MAE**: 20.45 points

### Trade #1210 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 07:30:00
- **FVG 5m**: 23581.26 - 23586.30
- **Entrée**: 23574.19 @ 2025-07-24 07:44:00
- **Stop Loss**: 23624.12
- **Risk**: 49.93 points
- **TP 1RR**: 23524.26 ❌
- **TP 2RR**: 23474.33 ❌
- **TP 3RR**: 23424.40 ❌
- **TP 4RR**: 23374.47 ❌
- **TP 15RR**: 22825.24 ❌
- **PnL**: -49.93 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 57.06 points

### Trade #1211 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 07:30:00
- **FVG 5m**: 23581.26 - 23586.30
- **Entrée**: 23574.19 @ 2025-07-24 07:44:00
- **Stop Loss**: 23624.12
- **Risk**: 49.93 points
- **TP 1RR**: 23524.26 ❌
- **TP 2RR**: 23474.33 ❌
- **TP 3RR**: 23424.40 ❌
- **TP 4RR**: 23374.47 ❌
- **TP 15RR**: 22825.24 ❌
- **PnL**: -49.93 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 57.06 points

### Trade #1212 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 07:45:00
- **FVG 5m**: 23590.34 - 23598.42
- **Entrée**: 23598.93 @ 2025-07-24 08:24:00
- **Stop Loss**: 23546.50
- **Risk**: 52.43 points
- **TP 1RR**: 23651.36 ❌
- **TP 2RR**: 23703.78 ❌
- **TP 3RR**: 23756.21 ❌
- **TP 4RR**: 23808.64 ❌
- **TP 15RR**: 24385.35 ❌
- **PnL**: -52.43 points (-1.0R)
- **MFE**: 33.83 points
- **MAE**: 58.07 points

### Trade #1213 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 08:15:00
- **FVG 5m**: 23574.19 - 23579.24
- **Entrée**: 23580.25 @ 2025-07-24 09:36:00
- **Stop Loss**: 23567.45
- **Risk**: 12.80 points
- **TP 1RR**: 23593.04 ✅
- **TP 2RR**: 23605.84 ✅
- **TP 3RR**: 23618.64 ✅
- **TP 4RR**: 23631.44 ✅
- **TP 15RR**: 23772.24 ❌
- **PnL**: -12.80 points (-1.0R)
- **MFE**: 93.67 points
- **MAE**: 18.43 points

### Trade #1214 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 08:15:00
- **FVG 5m**: 23574.19 - 23579.24
- **Entrée**: 23580.25 @ 2025-07-24 09:36:00
- **Stop Loss**: 23567.45
- **Risk**: 12.80 points
- **TP 1RR**: 23593.04 ✅
- **TP 2RR**: 23605.84 ✅
- **TP 3RR**: 23618.64 ✅
- **TP 4RR**: 23631.44 ✅
- **TP 15RR**: 23772.24 ❌
- **PnL**: -12.80 points (-1.0R)
- **MFE**: 93.67 points
- **MAE**: 18.43 points

### Trade #1215 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 09:00:00
- **FVG 5m**: 23603.47 - 23618.37
- **Entrée**: 23601.45 @ 2025-07-24 11:01:00
- **Stop Loss**: 23608.45
- **Risk**: 7.00 points
- **TP 1RR**: 23594.45 ✅
- **TP 2RR**: 23587.45 ✅
- **TP 3RR**: 23580.45 ✅
- **TP 4RR**: 23573.45 ✅
- **TP 15RR**: 23496.43 ❌
- **PnL**: -7.00 points (-1.0R)
- **MFE**: 30.30 points
- **MAE**: 8.58 points

### Trade #1216 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-24 12:00:00
- **FVG 5m**: 23623.42 - 23630.99
- **Entrée**: 23633.27 @ 2025-07-24 12:12:00
- **Stop Loss**: 23585.36
- **Risk**: 47.90 points
- **TP 1RR**: 23681.17 ❌
- **TP 2RR**: 23729.07 ❌
- **TP 3RR**: 23776.97 ❌
- **TP 4RR**: 23824.88 ❌
- **TP 15RR**: 24351.80 ❌
- **PnL**: -47.90 points (-1.0R)
- **MFE**: 40.65 points
- **MAE**: 53.27 points

### Trade #1217 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 12:15:00
- **FVG 5m**: 23635.03 - 23637.81
- **Entrée**: 23633.01 @ 2025-07-24 13:43:00
- **Stop Loss**: 23666.81
- **Risk**: 33.79 points
- **TP 1RR**: 23599.22 ✅
- **TP 2RR**: 23565.43 ❌
- **TP 3RR**: 23531.63 ❌
- **TP 4RR**: 23497.84 ❌
- **TP 15RR**: 23126.12 ❌
- **PnL**: -33.79 points (-1.0R)
- **MFE**: 35.35 points
- **MAE**: 33.83 points

### Trade #1218 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 12:15:00
- **FVG 5m**: 23635.03 - 23637.81
- **Entrée**: 23633.01 @ 2025-07-24 13:43:00
- **Stop Loss**: 23666.81
- **Risk**: 33.79 points
- **TP 1RR**: 23599.22 ✅
- **TP 2RR**: 23565.43 ❌
- **TP 3RR**: 23531.63 ❌
- **TP 4RR**: 23497.84 ❌
- **TP 15RR**: 23126.12 ❌
- **PnL**: -33.79 points (-1.0R)
- **MFE**: 35.35 points
- **MAE**: 33.83 points

### Trade #1219 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 12:15:00
- **FVG 5m**: 23635.03 - 23637.81
- **Entrée**: 23633.01 @ 2025-07-24 13:43:00
- **Stop Loss**: 23666.81
- **Risk**: 33.79 points
- **TP 1RR**: 23599.22 ✅
- **TP 2RR**: 23565.43 ❌
- **TP 3RR**: 23531.63 ❌
- **TP 4RR**: 23497.84 ❌
- **TP 15RR**: 23126.12 ❌
- **PnL**: -33.79 points (-1.0R)
- **MFE**: 35.35 points
- **MAE**: 33.83 points

### Trade #1220 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-24 12:15:00
- **FVG 5m**: 23635.03 - 23637.81
- **Entrée**: 23633.01 @ 2025-07-24 13:43:00
- **Stop Loss**: 23666.81
- **Risk**: 33.79 points
- **TP 1RR**: 23599.22 ✅
- **TP 2RR**: 23565.43 ❌
- **TP 3RR**: 23531.63 ❌
- **TP 4RR**: 23497.84 ❌
- **TP 15RR**: 23126.12 ❌
- **PnL**: -33.79 points (-1.0R)
- **MFE**: 35.35 points
- **MAE**: 33.83 points

### Trade #1221 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-25 03:15:00
- **FVG 5m**: 23595.14 - 23601.20
- **Entrée**: 23601.45 @ 2025-07-25 03:29:00
- **Stop Loss**: 23568.20
- **Risk**: 33.25 points
- **TP 1RR**: 23634.70 ❌
- **TP 2RR**: 23667.95 ❌
- **TP 3RR**: 23701.20 ❌
- **TP 4RR**: 23734.46 ❌
- **TP 15RR**: 24100.21 ❌
- **PnL**: -33.25 points (-1.0R)
- **MFE**: 21.46 points
- **MAE**: 39.64 points

### Trade #1222 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-25 08:30:00
- **FVG 5m**: 23596.91 - 23604.48
- **Entrée**: 23608.27 @ 2025-07-25 08:47:00
- **Stop Loss**: 23550.03
- **Risk**: 58.24 points
- **TP 1RR**: 23666.51 ✅
- **TP 2RR**: 23724.74 ✅
- **TP 3RR**: 23782.98 ✅
- **TP 4RR**: 23841.22 ✅
- **TP 15RR**: 24481.82 ❌
- **PnL**: -58.24 points (-1.0R)
- **MFE**: 472.89 points
- **MAE**: 71.96 points

### Trade #1223 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-25 14:15:00
- **FVG 5m**: 23659.52 - 23667.10
- **Entrée**: 23659.27 @ 2025-07-25 14:51:00
- **Stop Loss**: 23699.64
- **Risk**: 40.37 points
- **TP 1RR**: 23618.90 ❌
- **TP 2RR**: 23578.52 ❌
- **TP 3RR**: 23538.15 ❌
- **TP 4RR**: 23497.78 ❌
- **TP 15RR**: 23053.66 ❌
- **PnL**: -40.37 points (-1.0R)
- **MFE**: 20.45 points
- **MAE**: 132.30 points

### Trade #1224 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-25 15:00:00
- **FVG 5m**: 23657.25 - 23664.32
- **Entrée**: 23666.34 @ 2025-07-25 15:14:00
- **Stop Loss**: 23627.00
- **Risk**: 39.34 points
- **TP 1RR**: 23705.68 ✅
- **TP 2RR**: 23745.02 ✅
- **TP 3RR**: 23784.36 ✅
- **TP 4RR**: 23823.70 ✅
- **TP 15RR**: 24256.43 ❌
- **PnL**: -39.34 points (-1.0R)
- **MFE**: 220.41 points
- **MAE**: 78.52 points

### Trade #1225 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-28 08:30:00
- **FVG 5m**: 23702.95 - 23709.77
- **Entrée**: 23713.05 @ 2025-07-28 10:29:00
- **Stop Loss**: 23685.29
- **Risk**: 27.75 points
- **TP 1RR**: 23740.80 ✅
- **TP 2RR**: 23768.56 ❌
- **TP 3RR**: 23796.31 ❌
- **TP 4RR**: 23824.07 ❌
- **TP 15RR**: 24129.37 ❌
- **PnL**: -27.75 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 28.02 points

### Trade #1226 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-28 10:15:00
- **FVG 5m**: 23702.95 - 23709.77
- **Entrée**: 23713.05 @ 2025-07-28 10:29:00
- **Stop Loss**: 23657.03
- **Risk**: 56.02 points
- **TP 1RR**: 23769.07 ✅
- **TP 2RR**: 23825.08 ✅
- **TP 3RR**: 23881.10 ✅
- **TP 4RR**: 23937.12 ❌
- **TP 15RR**: 24553.31 ❌
- **PnL**: -56.02 points (-1.0R)
- **MFE**: 173.70 points
- **MAE**: 59.84 points

### Trade #1227 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23871.67
- **Risk**: 107.37 points
- **TP 1RR**: 23656.93 ✅
- **TP 2RR**: 23549.57 ❌
- **TP 3RR**: 23442.20 ❌
- **TP 4RR**: 23334.84 ❌
- **TP 15RR**: 22153.81 ❌
- **PnL**: -107.37 points (-1.0R)
- **MFE**: 176.48 points
- **MAE**: 110.58 points

### Trade #1228 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23871.67
- **Risk**: 107.37 points
- **TP 1RR**: 23656.93 ✅
- **TP 2RR**: 23549.57 ❌
- **TP 3RR**: 23442.20 ❌
- **TP 4RR**: 23334.84 ❌
- **TP 15RR**: 22153.81 ❌
- **PnL**: -107.37 points (-1.0R)
- **MFE**: 176.48 points
- **MAE**: 110.58 points

### Trade #1229 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23871.67
- **Risk**: 107.37 points
- **TP 1RR**: 23656.93 ✅
- **TP 2RR**: 23549.57 ❌
- **TP 3RR**: 23442.20 ❌
- **TP 4RR**: 23334.84 ❌
- **TP 15RR**: 22153.81 ❌
- **PnL**: -107.37 points (-1.0R)
- **MFE**: 176.48 points
- **MAE**: 110.58 points

### Trade #1230 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 08:45:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23871.67
- **Risk**: 107.37 points
- **TP 1RR**: 23656.93 ✅
- **TP 2RR**: 23549.57 ❌
- **TP 3RR**: 23442.20 ❌
- **TP 4RR**: 23334.84 ❌
- **TP 15RR**: 22153.81 ❌
- **PnL**: -107.37 points (-1.0R)
- **MFE**: 176.48 points
- **MAE**: 110.58 points

### Trade #1231 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:15:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23824.43
- **Risk**: 60.13 points
- **TP 1RR**: 23704.17 ✅
- **TP 2RR**: 23644.04 ✅
- **TP 3RR**: 23583.91 ❌
- **TP 4RR**: 23523.78 ❌
- **TP 15RR**: 22862.36 ❌
- **PnL**: -60.13 points (-1.0R)
- **MFE**: 176.48 points
- **MAE**: 84.83 points

### Trade #1232 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:30:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23821.90
- **Risk**: 57.60 points
- **TP 1RR**: 23706.70 ✅
- **TP 2RR**: 23649.09 ❌
- **TP 3RR**: 23591.49 ❌
- **TP 4RR**: 23533.89 ❌
- **TP 15RR**: 22900.25 ❌
- **PnL**: -57.60 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 58.83 points

### Trade #1233 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 09:30:00
- **FVG 5m**: 23769.10 - 23782.48
- **Entrée**: 23764.30 @ 2025-07-29 09:52:00
- **Stop Loss**: 23821.90
- **Risk**: 57.60 points
- **TP 1RR**: 23706.70 ✅
- **TP 2RR**: 23649.09 ❌
- **TP 3RR**: 23591.49 ❌
- **TP 4RR**: 23533.89 ❌
- **TP 15RR**: 22900.25 ❌
- **PnL**: -57.60 points (-1.0R)
- **MFE**: 111.09 points
- **MAE**: 58.83 points

### Trade #1234 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 10:15:00
- **FVG 5m**: 23724.16 - 23734.00
- **Entrée**: 23723.40 @ 2025-07-29 12:38:00
- **Stop Loss**: 23757.49
- **Risk**: 34.09 points
- **TP 1RR**: 23689.31 ✅
- **TP 2RR**: 23655.22 ✅
- **TP 3RR**: 23621.13 ❌
- **TP 4RR**: 23587.04 ❌
- **TP 15RR**: 23212.04 ❌
- **PnL**: -34.09 points (-1.0R)
- **MFE**: 70.19 points
- **MAE**: 35.85 points

### Trade #1235 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 10:30:00
- **FVG 5m**: 23724.16 - 23734.00
- **Entrée**: 23723.40 @ 2025-07-29 12:38:00
- **Stop Loss**: 23737.53
- **Risk**: 14.14 points
- **TP 1RR**: 23709.26 ✅
- **TP 2RR**: 23695.13 ✅
- **TP 3RR**: 23680.99 ❌
- **TP 4RR**: 23666.86 ❌
- **TP 15RR**: 23511.37 ❌
- **PnL**: -14.14 points (-1.0R)
- **MFE**: 29.03 points
- **MAE**: 16.92 points

### Trade #1236 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-29 12:15:00
- **FVG 5m**: 23724.16 - 23734.00
- **Entrée**: 23723.40 @ 2025-07-29 12:38:00
- **Stop Loss**: 23770.63
- **Risk**: 47.23 points
- **TP 1RR**: 23676.17 ✅
- **TP 2RR**: 23628.95 ❌
- **TP 3RR**: 23581.72 ❌
- **TP 4RR**: 23534.50 ❌
- **TP 15RR**: 23015.01 ❌
- **PnL**: -47.23 points (-1.0R)
- **MFE**: 70.19 points
- **MAE**: 48.22 points

### Trade #1237 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-29 14:30:00
- **FVG 5m**: 23685.78 - 23691.59
- **Entrée**: 23693.35 @ 2025-07-29 17:02:00
- **Stop Loss**: 23641.38
- **Risk**: 51.97 points
- **TP 1RR**: 23745.32 ✅
- **TP 2RR**: 23797.30 ✅
- **TP 3RR**: 23849.27 ❌
- **TP 4RR**: 23901.24 ❌
- **TP 15RR**: 24472.91 ❌
- **PnL**: -51.97 points (-1.0R)
- **MFE**: 129.77 points
- **MAE**: 61.35 points

### Trade #1238 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-29 14:30:00
- **FVG 5m**: 23685.78 - 23691.59
- **Entrée**: 23693.35 @ 2025-07-29 17:02:00
- **Stop Loss**: 23641.38
- **Risk**: 51.97 points
- **TP 1RR**: 23745.32 ✅
- **TP 2RR**: 23797.30 ✅
- **TP 3RR**: 23849.27 ❌
- **TP 4RR**: 23901.24 ❌
- **TP 15RR**: 24472.91 ❌
- **PnL**: -51.97 points (-1.0R)
- **MFE**: 129.77 points
- **MAE**: 61.35 points

### Trade #1239 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-29 14:30:00
- **FVG 5m**: 23685.78 - 23691.59
- **Entrée**: 23693.35 @ 2025-07-29 17:02:00
- **Stop Loss**: 23641.38
- **Risk**: 51.97 points
- **TP 1RR**: 23745.32 ✅
- **TP 2RR**: 23797.30 ✅
- **TP 3RR**: 23849.27 ❌
- **TP 4RR**: 23901.24 ❌
- **TP 15RR**: 24472.91 ❌
- **PnL**: -51.97 points (-1.0R)
- **MFE**: 129.77 points
- **MAE**: 61.35 points

### Trade #1240 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 02:15:00
- **FVG 5m**: 23718.60 - 23724.41
- **Entrée**: 23724.91 @ 2025-07-30 02:29:00
- **Stop Loss**: 23694.63
- **Risk**: 30.28 points
- **TP 1RR**: 23755.20 ❌
- **TP 2RR**: 23785.48 ❌
- **TP 3RR**: 23815.77 ❌
- **TP 4RR**: 23846.05 ❌
- **TP 15RR**: 24179.17 ❌
- **PnL**: -30.28 points (-1.0R)
- **MFE**: 20.45 points
- **MAE**: 30.30 points

### Trade #1241 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 08:30:00
- **FVG 5m**: 23725.67 - 23728.70
- **Entrée**: 23733.75 @ 2025-07-30 10:41:00
- **Stop Loss**: 23671.16
- **Risk**: 62.59 points
- **TP 1RR**: 23796.34 ✅
- **TP 2RR**: 23858.93 ❌
- **TP 3RR**: 23921.52 ❌
- **TP 4RR**: 23984.11 ❌
- **TP 15RR**: 24672.59 ❌
- **PnL**: -62.59 points (-1.0R)
- **MFE**: 89.38 points
- **MAE**: 65.14 points

### Trade #1242 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 08:45:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23717.09 @ 2025-07-30 10:11:00
- **Stop Loss**: 23771.13
- **Risk**: 54.04 points
- **TP 1RR**: 23663.04 ❌
- **TP 2RR**: 23609.00 ❌
- **TP 3RR**: 23554.96 ❌
- **TP 4RR**: 23500.91 ❌
- **TP 15RR**: 22906.44 ❌
- **PnL**: -54.04 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 58.07 points

### Trade #1243 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 08:45:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23717.09 @ 2025-07-30 10:11:00
- **Stop Loss**: 23771.13
- **Risk**: 54.04 points
- **TP 1RR**: 23663.04 ❌
- **TP 2RR**: 23609.00 ❌
- **TP 3RR**: 23554.96 ❌
- **TP 4RR**: 23500.91 ❌
- **TP 15RR**: 22906.44 ❌
- **PnL**: -54.04 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 58.07 points

### Trade #1244 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 09:30:00
- **FVG 5m**: 23725.67 - 23728.70
- **Entrée**: 23733.75 @ 2025-07-30 10:41:00
- **Stop Loss**: 23724.91
- **Risk**: 8.84 points
- **TP 1RR**: 23742.59 ✅
- **TP 2RR**: 23751.43 ✅
- **TP 3RR**: 23760.27 ✅
- **TP 4RR**: 23769.11 ✅
- **TP 15RR**: 23866.33 ❌
- **PnL**: -8.84 points (-1.0R)
- **MFE**: 89.38 points
- **MAE**: 20.20 points

### Trade #1245 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 09:45:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23717.09 @ 2025-07-30 10:11:00
- **Stop Loss**: 23786.29
- **Risk**: 69.20 points
- **TP 1RR**: 23647.89 ❌
- **TP 2RR**: 23578.69 ❌
- **TP 3RR**: 23509.49 ❌
- **TP 4RR**: 23440.29 ❌
- **TP 15RR**: 22679.10 ❌
- **PnL**: -69.20 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 76.00 points

### Trade #1246 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 09:45:00
- **FVG 5m**: 23727.69 - 23734.51
- **Entrée**: 23717.09 @ 2025-07-30 10:11:00
- **Stop Loss**: 23786.29
- **Risk**: 69.20 points
- **TP 1RR**: 23647.89 ❌
- **TP 2RR**: 23578.69 ❌
- **TP 3RR**: 23509.49 ❌
- **TP 4RR**: 23440.29 ❌
- **TP 15RR**: 22679.10 ❌
- **PnL**: -69.20 points (-1.0R)
- **MFE**: 9.09 points
- **MAE**: 76.00 points

### Trade #1247 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 10:45:00
- **FVG 5m**: 23746.37 - 23749.66
- **Entrée**: 23754.45 @ 2025-07-30 11:03:00
- **Stop Loss**: 23716.84
- **Risk**: 37.62 points
- **TP 1RR**: 23792.07 ✅
- **TP 2RR**: 23829.69 ❌
- **TP 3RR**: 23867.30 ❌
- **TP 4RR**: 23904.92 ❌
- **TP 15RR**: 24318.71 ❌
- **PnL**: -37.62 points (-1.0R)
- **MFE**: 68.67 points
- **MAE**: 40.90 points

### Trade #1248 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:00:00
- **FVG 5m**: 23731.48 - 23745.36
- **Entrée**: 23716.58 @ 2025-07-30 13:54:00
- **Stop Loss**: 23804.98
- **Risk**: 88.40 points
- **TP 1RR**: 23628.19 ✅
- **TP 2RR**: 23539.79 ❌
- **TP 3RR**: 23451.39 ❌
- **TP 4RR**: 23363.00 ❌
- **TP 15RR**: 22390.63 ❌
- **PnL**: -88.40 points (-1.0R)
- **MFE**: 128.76 points
- **MAE**: 132.55 points

### Trade #1249 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:45:00
- **FVG 5m**: 23655.99 - 23711.28
- **Entrée**: 23644.63 @ 2025-07-30 13:59:00
- **Stop Loss**: 23808.52
- **Risk**: 163.89 points
- **TP 1RR**: 23480.74 ❌
- **TP 2RR**: 23316.85 ❌
- **TP 3RR**: 23152.96 ❌
- **TP 4RR**: 22989.07 ❌
- **TP 15RR**: 21186.29 ❌
- **PnL**: -163.89 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 204.51 points

### Trade #1250 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:45:00
- **FVG 5m**: 23655.99 - 23711.28
- **Entrée**: 23644.63 @ 2025-07-30 13:59:00
- **Stop Loss**: 23808.52
- **Risk**: 163.89 points
- **TP 1RR**: 23480.74 ❌
- **TP 2RR**: 23316.85 ❌
- **TP 3RR**: 23152.96 ❌
- **TP 4RR**: 22989.07 ❌
- **TP 15RR**: 21186.29 ❌
- **PnL**: -163.89 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 204.51 points

### Trade #1251 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-30 13:45:00
- **FVG 5m**: 23655.99 - 23711.28
- **Entrée**: 23644.63 @ 2025-07-30 13:59:00
- **Stop Loss**: 23808.52
- **Risk**: 163.89 points
- **TP 1RR**: 23480.74 ❌
- **TP 2RR**: 23316.85 ❌
- **TP 3RR**: 23152.96 ❌
- **TP 4RR**: 22989.07 ❌
- **TP 15RR**: 21186.29 ❌
- **PnL**: -163.89 points (-1.0R)
- **MFE**: 56.81 points
- **MAE**: 204.51 points

### Trade #1252 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:00:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23576.03
- **Risk**: 128.19 points
- **TP 1RR**: 23832.40 ✅
- **TP 2RR**: 23960.58 ✅
- **TP 3RR**: 24088.77 ❌
- **TP 4RR**: 24216.95 ❌
- **TP 15RR**: 25626.99 ❌
- **PnL**: -128.19 points (-1.0R)
- **MFE**: 376.95 points
- **MAE**: 139.87 points

### Trade #1253 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:00:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23576.03
- **Risk**: 128.19 points
- **TP 1RR**: 23832.40 ✅
- **TP 2RR**: 23960.58 ✅
- **TP 3RR**: 24088.77 ❌
- **TP 4RR**: 24216.95 ❌
- **TP 15RR**: 25626.99 ❌
- **PnL**: -128.19 points (-1.0R)
- **MFE**: 376.95 points
- **MAE**: 139.87 points

### Trade #1254 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:00:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23576.03
- **Risk**: 128.19 points
- **TP 1RR**: 23832.40 ✅
- **TP 2RR**: 23960.58 ✅
- **TP 3RR**: 24088.77 ❌
- **TP 4RR**: 24216.95 ❌
- **TP 15RR**: 25626.99 ❌
- **PnL**: -128.19 points (-1.0R)
- **MFE**: 376.95 points
- **MAE**: 139.87 points

### Trade #1255 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:00:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23576.03
- **Risk**: 128.19 points
- **TP 1RR**: 23832.40 ✅
- **TP 2RR**: 23960.58 ✅
- **TP 3RR**: 24088.77 ❌
- **TP 4RR**: 24216.95 ❌
- **TP 15RR**: 25626.99 ❌
- **PnL**: -128.19 points (-1.0R)
- **MFE**: 376.95 points
- **MAE**: 139.87 points

### Trade #1256 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:45:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23612.87
- **Risk**: 91.34 points
- **TP 1RR**: 23795.55 ✅
- **TP 2RR**: 23886.90 ✅
- **TP 3RR**: 23978.24 ✅
- **TP 4RR**: 24069.58 ✅
- **TP 15RR**: 25074.35 ❌
- **PnL**: -91.34 points (-1.0R)
- **MFE**: 376.95 points
- **MAE**: 94.17 points

### Trade #1257 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-30 14:45:00
- **FVG 5m**: 23698.66 - 23702.95
- **Entrée**: 23704.21 @ 2025-07-30 14:57:00
- **Stop Loss**: 23612.87
- **Risk**: 91.34 points
- **TP 1RR**: 23795.55 ✅
- **TP 2RR**: 23886.90 ✅
- **TP 3RR**: 23978.24 ✅
- **TP 4RR**: 24069.58 ✅
- **TP 15RR**: 25074.35 ❌
- **PnL**: -91.34 points (-1.0R)
- **MFE**: 376.95 points
- **MAE**: 94.17 points

### Trade #1258 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 03:00:00
- **FVG 5m**: 24026.88 - 24033.19
- **Entrée**: 24026.37 @ 2025-07-31 04:32:00
- **Stop Loss**: 24074.25
- **Risk**: 47.88 points
- **TP 1RR**: 23978.49 ✅
- **TP 2RR**: 23930.60 ✅
- **TP 3RR**: 23882.72 ✅
- **TP 4RR**: 23834.84 ✅
- **TP 15RR**: 23308.13 ✅
- **PnL**: 718.24 points (15.0R)
- **MFE**: 726.88 points
- **MAE**: 21.46 points

### Trade #1259 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 07:00:00
- **FVG 5m**: 24012.48 - 24017.28
- **Entrée**: 24022.58 @ 2025-07-31 07:17:00
- **Stop Loss**: 23979.28
- **Risk**: 43.30 points
- **TP 1RR**: 24065.89 ❌
- **TP 2RR**: 24109.19 ❌
- **TP 3RR**: 24152.49 ❌
- **TP 4RR**: 24195.79 ❌
- **TP 15RR**: 24672.12 ❌
- **PnL**: -43.30 points (-1.0R)
- **MFE**: 25.25 points
- **MAE**: 45.45 points

### Trade #1260 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 08:30:00
- **FVG 5m**: 23889.02 - 23894.33
- **Entrée**: 23883.72 @ 2025-07-31 09:21:00
- **Stop Loss**: 23999.23
- **Risk**: 115.51 points
- **TP 1RR**: 23768.21 ✅
- **TP 2RR**: 23652.70 ✅
- **TP 3RR**: 23537.20 ✅
- **TP 4RR**: 23421.69 ✅
- **TP 15RR**: 22151.09 ❌
- **PnL**: -115.51 points (-1.0R)
- **MFE**: 883.16 points
- **MAE**: 116.64 points

### Trade #1261 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 09:45:00
- **FVG 5m**: 23747.13 - 23773.64
- **Entrée**: 23745.36 @ 2025-07-31 10:13:00
- **Stop Loss**: 23868.13
- **Risk**: 122.77 points
- **TP 1RR**: 23622.60 ✅
- **TP 2RR**: 23499.83 ✅
- **TP 3RR**: 23377.07 ✅
- **TP 4RR**: 23254.30 ✅
- **TP 15RR**: 21903.89 ❌
- **PnL**: -122.77 points (-1.0R)
- **MFE**: 744.80 points
- **MAE**: 127.75 points

### Trade #1262 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 13:00:00
- **FVG 5m**: 23649.42 - 23652.71
- **Entrée**: 23642.61 @ 2025-07-31 14:12:00
- **Stop Loss**: 23662.26
- **Risk**: 19.65 points
- **TP 1RR**: 23622.95 ✅
- **TP 2RR**: 23603.30 ✅
- **TP 3RR**: 23583.65 ✅
- **TP 4RR**: 23564.00 ✅
- **TP 15RR**: 23347.83 ❌
- **PnL**: -19.65 points (-1.0R)
- **MFE**: 111.85 points
- **MAE**: 48.48 points

### Trade #1263 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 13:15:00
- **FVG 5m**: 23626.45 - 23646.14
- **Entrée**: 23647.40 @ 2025-07-31 13:28:00
- **Stop Loss**: 23524.55
- **Risk**: 122.86 points
- **TP 1RR**: 23770.26 ❌
- **TP 2RR**: 23893.12 ❌
- **TP 3RR**: 24015.98 ❌
- **TP 4RR**: 24138.83 ❌
- **TP 15RR**: 25490.27 ❌
- **PnL**: -122.86 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 126.24 points

### Trade #1264 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 13:15:00
- **FVG 5m**: 23626.45 - 23646.14
- **Entrée**: 23647.40 @ 2025-07-31 13:28:00
- **Stop Loss**: 23524.55
- **Risk**: 122.86 points
- **TP 1RR**: 23770.26 ❌
- **TP 2RR**: 23893.12 ❌
- **TP 3RR**: 24015.98 ❌
- **TP 4RR**: 24138.83 ❌
- **TP 15RR**: 25490.27 ❌
- **PnL**: -122.86 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 126.24 points

### Trade #1265 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 13:15:00
- **FVG 5m**: 23626.45 - 23646.14
- **Entrée**: 23647.40 @ 2025-07-31 13:28:00
- **Stop Loss**: 23524.55
- **Risk**: 122.86 points
- **TP 1RR**: 23770.26 ❌
- **TP 2RR**: 23893.12 ❌
- **TP 3RR**: 24015.98 ❌
- **TP 4RR**: 24138.83 ❌
- **TP 15RR**: 25490.27 ❌
- **PnL**: -122.86 points (-1.0R)
- **MFE**: 50.75 points
- **MAE**: 126.24 points

### Trade #1266 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 15:15:00
- **FVG 5m**: 23555.76 - 23563.58
- **Entrée**: 23581.00 @ 2025-07-31 15:31:00
- **Stop Loss**: 23509.41
- **Risk**: 71.60 points
- **TP 1RR**: 23652.60 ❌
- **TP 2RR**: 23724.20 ❌
- **TP 3RR**: 23795.79 ❌
- **TP 4RR**: 23867.39 ❌
- **TP 15RR**: 24654.96 ❌
- **PnL**: -71.60 points (-1.0R)
- **MFE**: 8.33 points
- **MAE**: 71.70 points

### Trade #1267 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 17:30:00
- **FVG 5m**: 23501.73 - 23505.51
- **Entrée**: 23498.70 @ 2025-07-31 19:21:00
- **Stop Loss**: 23558.69
- **Risk**: 60.00 points
- **TP 1RR**: 23438.70 ❌
- **TP 2RR**: 23378.70 ❌
- **TP 3RR**: 23318.71 ❌
- **TP 4RR**: 23258.71 ❌
- **TP 15RR**: 22598.75 ❌
- **PnL**: -60.00 points (-1.0R)
- **MFE**: 37.11 points
- **MAE**: 61.10 points

### Trade #1268 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-07-31 17:30:00
- **FVG 5m**: 23501.73 - 23505.51
- **Entrée**: 23498.70 @ 2025-07-31 19:21:00
- **Stop Loss**: 23558.69
- **Risk**: 60.00 points
- **TP 1RR**: 23438.70 ❌
- **TP 2RR**: 23378.70 ❌
- **TP 3RR**: 23318.71 ❌
- **TP 4RR**: 23258.71 ❌
- **TP 15RR**: 22598.75 ❌
- **PnL**: -60.00 points (-1.0R)
- **MFE**: 37.11 points
- **MAE**: 61.10 points

### Trade #1269 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-07-31 18:00:00
- **FVG 5m**: 23519.40 - 23527.73
- **Entrée**: 23528.99 @ 2025-07-31 20:14:00
- **Stop Loss**: 23483.67
- **Risk**: 45.33 points
- **TP 1RR**: 23574.32 ❌
- **TP 2RR**: 23619.65 ❌
- **TP 3RR**: 23664.97 ❌
- **TP 4RR**: 23710.30 ❌
- **TP 15RR**: 24208.90 ❌
- **PnL**: -45.33 points (-1.0R)
- **MFE**: 44.69 points
- **MAE**: 52.77 points

### Trade #1270 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-01 03:15:00
- **FVG 5m**: 23331.81 - 23356.80
- **Entrée**: 23316.66 @ 2025-08-01 03:27:00
- **Stop Loss**: 23404.86
- **Risk**: 88.20 points
- **TP 1RR**: 23228.46 ✅
- **TP 2RR**: 23140.27 ✅
- **TP 3RR**: 23052.07 ✅
- **TP 4RR**: 22963.87 ❌
- **TP 15RR**: 21993.71 ❌
- **PnL**: -88.20 points (-1.0R)
- **MFE**: 316.10 points
- **MAE**: 93.67 points

### Trade #1271 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-01 03:15:00
- **FVG 5m**: 23331.81 - 23356.80
- **Entrée**: 23316.66 @ 2025-08-01 03:27:00
- **Stop Loss**: 23404.86
- **Risk**: 88.20 points
- **TP 1RR**: 23228.46 ✅
- **TP 2RR**: 23140.27 ✅
- **TP 3RR**: 23052.07 ✅
- **TP 4RR**: 22963.87 ❌
- **TP 15RR**: 21993.71 ❌
- **PnL**: -88.20 points (-1.0R)
- **MFE**: 316.10 points
- **MAE**: 93.67 points

### Trade #1272 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 06:00:00
- **FVG 5m**: 23307.07 - 23323.73
- **Entrée**: 23324.23 @ 2025-08-01 06:13:00
- **Stop Loss**: 23268.16
- **Risk**: 56.08 points
- **TP 1RR**: 23380.31 ✅
- **TP 2RR**: 23436.39 ❌
- **TP 3RR**: 23492.46 ❌
- **TP 4RR**: 23548.54 ❌
- **TP 15RR**: 24165.37 ❌
- **PnL**: -56.08 points (-1.0R)
- **MFE**: 72.71 points
- **MAE**: 58.32 points

### Trade #1273 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 06:00:00
- **FVG 5m**: 23307.07 - 23323.73
- **Entrée**: 23324.23 @ 2025-08-01 06:13:00
- **Stop Loss**: 23268.16
- **Risk**: 56.08 points
- **TP 1RR**: 23380.31 ✅
- **TP 2RR**: 23436.39 ❌
- **TP 3RR**: 23492.46 ❌
- **TP 4RR**: 23548.54 ❌
- **TP 15RR**: 24165.37 ❌
- **PnL**: -56.08 points (-1.0R)
- **MFE**: 72.71 points
- **MAE**: 58.32 points

### Trade #1274 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 09:00:00
- **FVG 5m**: 23127.81 - 23132.35
- **Entrée**: 23145.73 @ 2025-08-01 09:12:00
- **Stop Loss**: 23014.30
- **Risk**: 131.44 points
- **TP 1RR**: 23277.17 ❌
- **TP 2RR**: 23408.61 ❌
- **TP 3RR**: 23540.05 ❌
- **TP 4RR**: 23671.49 ❌
- **TP 15RR**: 25117.32 ❌
- **PnL**: -131.44 points (-1.0R)
- **MFE**: 128.01 points
- **MAE**: 145.17 points

### Trade #1275 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 09:00:00
- **FVG 5m**: 23127.81 - 23132.35
- **Entrée**: 23145.73 @ 2025-08-01 09:12:00
- **Stop Loss**: 23014.30
- **Risk**: 131.44 points
- **TP 1RR**: 23277.17 ❌
- **TP 2RR**: 23408.61 ❌
- **TP 3RR**: 23540.05 ❌
- **TP 4RR**: 23671.49 ❌
- **TP 15RR**: 25117.32 ❌
- **PnL**: -131.44 points (-1.0R)
- **MFE**: 128.01 points
- **MAE**: 145.17 points

### Trade #1276 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 13:00:00
- **FVG 5m**: 23065.19 - 23080.09
- **Entrée**: 23086.40 @ 2025-08-01 13:24:00
- **Stop Loss**: 22989.06
- **Risk**: 97.34 points
- **TP 1RR**: 23183.74 ✅
- **TP 2RR**: 23281.09 ✅
- **TP 3RR**: 23378.43 ✅
- **TP 4RR**: 23475.77 ✅
- **TP 15RR**: 24546.53 ✅
- **PnL**: 1460.13 points (15.0R)
- **MFE**: 1460.60 points
- **MAE**: 38.63 points

### Trade #1277 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 13:00:00
- **FVG 5m**: 23065.19 - 23080.09
- **Entrée**: 23086.40 @ 2025-08-01 13:24:00
- **Stop Loss**: 22989.06
- **Risk**: 97.34 points
- **TP 1RR**: 23183.74 ✅
- **TP 2RR**: 23281.09 ✅
- **TP 3RR**: 23378.43 ✅
- **TP 4RR**: 23475.77 ✅
- **TP 15RR**: 24546.53 ✅
- **PnL**: 1460.13 points (15.0R)
- **MFE**: 1460.60 points
- **MAE**: 38.63 points

### Trade #1278 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-01 13:00:00
- **FVG 5m**: 23065.19 - 23080.09
- **Entrée**: 23086.40 @ 2025-08-01 13:24:00
- **Stop Loss**: 22989.06
- **Risk**: 97.34 points
- **TP 1RR**: 23183.74 ✅
- **TP 2RR**: 23281.09 ✅
- **TP 3RR**: 23378.43 ✅
- **TP 4RR**: 23475.77 ✅
- **TP 15RR**: 24546.53 ✅
- **PnL**: 1460.13 points (15.0R)
- **MFE**: 1460.60 points
- **MAE**: 38.63 points

### Trade #1279 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 02:30:00
- **FVG 5m**: 23265.91 - 23270.46
- **Entrée**: 23270.71 @ 2025-08-04 03:14:00
- **Stop Loss**: 23230.31
- **Risk**: 40.40 points
- **TP 1RR**: 23311.11 ✅
- **TP 2RR**: 23351.52 ✅
- **TP 3RR**: 23391.92 ✅
- **TP 4RR**: 23432.32 ✅
- **TP 15RR**: 23876.76 ✅
- **PnL**: 606.05 points (15.0R)
- **MFE**: 609.48 points
- **MAE**: 11.36 points

### Trade #1280 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 03:00:00
- **FVG 5m**: 23265.91 - 23270.46
- **Entrée**: 23270.71 @ 2025-08-04 03:14:00
- **Stop Loss**: 23222.23
- **Risk**: 48.48 points
- **TP 1RR**: 23319.19 ✅
- **TP 2RR**: 23367.67 ✅
- **TP 3RR**: 23416.14 ✅
- **TP 4RR**: 23464.62 ✅
- **TP 15RR**: 23997.89 ✅
- **PnL**: 727.18 points (15.0R)
- **MFE**: 729.66 points
- **MAE**: 11.36 points

### Trade #1281 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 08:45:00
- **FVG 5m**: 23457.04 - 23469.66
- **Entrée**: 23474.96 @ 2025-08-04 08:58:00
- **Stop Loss**: 23407.46
- **Risk**: 67.51 points
- **TP 1RR**: 23542.47 ✅
- **TP 2RR**: 23609.98 ✅
- **TP 3RR**: 23677.48 ❌
- **TP 4RR**: 23744.99 ❌
- **TP 15RR**: 24487.56 ❌
- **PnL**: -67.51 points (-1.0R)
- **MFE**: 161.08 points
- **MAE**: 67.92 points

### Trade #1282 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 08:45:00
- **FVG 5m**: 23457.04 - 23469.66
- **Entrée**: 23474.96 @ 2025-08-04 08:58:00
- **Stop Loss**: 23407.46
- **Risk**: 67.51 points
- **TP 1RR**: 23542.47 ✅
- **TP 2RR**: 23609.98 ✅
- **TP 3RR**: 23677.48 ❌
- **TP 4RR**: 23744.99 ❌
- **TP 15RR**: 24487.56 ❌
- **PnL**: -67.51 points (-1.0R)
- **MFE**: 161.08 points
- **MAE**: 67.92 points

### Trade #1283 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-04 11:15:00
- **FVG 5m**: 23498.70 - 23501.47
- **Entrée**: 23496.93 @ 2025-08-04 12:41:00
- **Stop Loss**: 23518.78
- **Risk**: 21.85 points
- **TP 1RR**: 23475.08 ✅
- **TP 2RR**: 23453.22 ❌
- **TP 3RR**: 23431.37 ❌
- **TP 4RR**: 23409.52 ❌
- **TP 15RR**: 23169.14 ❌
- **PnL**: -21.85 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 36.86 points

### Trade #1284 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-04 14:15:00
- **FVG 5m**: 23499.20 - 23510.31
- **Entrée**: 23496.93 @ 2025-08-04 14:29:00
- **Stop Loss**: 23545.56
- **Risk**: 48.63 points
- **TP 1RR**: 23448.30 ❌
- **TP 2RR**: 23399.67 ❌
- **TP 3RR**: 23351.04 ❌
- **TP 4RR**: 23302.41 ❌
- **TP 15RR**: 22767.50 ❌
- **PnL**: -48.63 points (-1.0R)
- **MFE**: 13.38 points
- **MAE**: 72.71 points

### Trade #1285 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-04 14:45:00
- **FVG 5m**: 23539.60 - 23558.03
- **Entrée**: 23560.80 @ 2025-08-04 15:08:00
- **Stop Loss**: 23483.67
- **Risk**: 77.14 points
- **TP 1RR**: 23637.94 ❌
- **TP 2RR**: 23715.08 ❌
- **TP 3RR**: 23792.22 ❌
- **TP 4RR**: 23869.36 ❌
- **TP 15RR**: 24717.89 ❌
- **PnL**: -77.14 points (-1.0R)
- **MFE**: 75.24 points
- **MAE**: 78.02 points

### Trade #1286 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-04 17:00:00
- **FVG 5m**: 23560.05 - 23567.87
- **Entrée**: 23557.52 @ 2025-08-04 18:21:00
- **Stop Loss**: 23603.15
- **Risk**: 45.63 points
- **TP 1RR**: 23511.89 ❌
- **TP 2RR**: 23466.27 ❌
- **TP 3RR**: 23420.64 ❌
- **TP 4RR**: 23375.01 ❌
- **TP 15RR**: 22873.11 ❌
- **PnL**: -45.63 points (-1.0R)
- **MFE**: 12.88 points
- **MAE**: 48.48 points

### Trade #1287 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 03:15:00
- **FVG 5m**: 23568.13 - 23573.18
- **Entrée**: 23573.43 @ 2025-08-05 04:33:00
- **Stop Loss**: 23532.12
- **Risk**: 41.31 points
- **TP 1RR**: 23614.74 ✅
- **TP 2RR**: 23656.05 ❌
- **TP 3RR**: 23697.36 ❌
- **TP 4RR**: 23738.67 ❌
- **TP 15RR**: 24193.10 ❌
- **PnL**: -41.31 points (-1.0R)
- **MFE**: 62.61 points
- **MAE**: 46.71 points

### Trade #1288 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-05 06:15:00
- **FVG 5m**: 23609.53 - 23614.08
- **Entrée**: 23608.52 @ 2025-08-05 06:27:00
- **Stop Loss**: 23632.96
- **Risk**: 24.43 points
- **TP 1RR**: 23584.09 ❌
- **TP 2RR**: 23559.65 ❌
- **TP 3RR**: 23535.22 ❌
- **TP 4RR**: 23510.79 ❌
- **TP 15RR**: 23242.01 ❌
- **PnL**: -24.43 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 27.52 points

### Trade #1289 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 10:00:00
- **FVG 5m**: 23395.18 - 23402.50
- **Entrée**: 23405.28 @ 2025-08-05 11:04:00
- **Stop Loss**: 23369.60
- **Risk**: 35.68 points
- **TP 1RR**: 23440.96 ✅
- **TP 2RR**: 23476.63 ❌
- **TP 3RR**: 23512.31 ❌
- **TP 4RR**: 23547.98 ❌
- **TP 15RR**: 23940.42 ❌
- **PnL**: -35.68 points (-1.0R)
- **MFE**: 49.99 points
- **MAE**: 36.86 points

### Trade #1290 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-05 10:30:00
- **FVG 5m**: 23398.72 - 23419.92
- **Entrée**: 23391.65 @ 2025-08-05 11:41:00
- **Stop Loss**: 23428.60
- **Risk**: 36.96 points
- **TP 1RR**: 23354.69 ❌
- **TP 2RR**: 23317.73 ❌
- **TP 3RR**: 23280.78 ❌
- **TP 4RR**: 23243.82 ❌
- **TP 15RR**: 22837.31 ❌
- **PnL**: -36.96 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 42.42 points

### Trade #1291 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-05 17:00:00
- **FVG 5m**: 23306.56 - 23309.59
- **Entrée**: 23303.78 @ 2025-08-05 18:49:00
- **Stop Loss**: 23353.33
- **Risk**: 49.54 points
- **TP 1RR**: 23254.24 ❌
- **TP 2RR**: 23204.70 ❌
- **TP 3RR**: 23155.16 ❌
- **TP 4RR**: 23105.62 ❌
- **TP 15RR**: 22560.65 ❌
- **PnL**: -49.54 points (-1.0R)
- **MFE**: 25.75 points
- **MAE**: 54.03 points

### Trade #1292 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 20:30:00
- **FVG 5m**: 23350.74 - 23353.77
- **Entrée**: 23355.04 @ 2025-08-05 20:51:00
- **Stop Loss**: 23291.12
- **Risk**: 63.91 points
- **TP 1RR**: 23418.95 ✅
- **TP 2RR**: 23482.86 ✅
- **TP 3RR**: 23546.78 ✅
- **TP 4RR**: 23610.69 ✅
- **TP 15RR**: 24313.75 ❌
- **PnL**: -63.91 points (-1.0R)
- **MFE**: 951.83 points
- **MAE**: 69.43 points

### Trade #1293 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-05 20:30:00
- **FVG 5m**: 23350.74 - 23353.77
- **Entrée**: 23355.04 @ 2025-08-05 20:51:00
- **Stop Loss**: 23291.12
- **Risk**: 63.91 points
- **TP 1RR**: 23418.95 ✅
- **TP 2RR**: 23482.86 ✅
- **TP 3RR**: 23546.78 ✅
- **TP 4RR**: 23610.69 ✅
- **TP 15RR**: 24313.75 ❌
- **PnL**: -63.91 points (-1.0R)
- **MFE**: 951.83 points
- **MAE**: 69.43 points

### Trade #1294 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-06 03:30:00
- **FVG 5m**: 23403.01 - 23410.08
- **Entrée**: 23393.16 @ 2025-08-06 03:42:00
- **Stop Loss**: 23432.39
- **Risk**: 39.23 points
- **TP 1RR**: 23353.93 ✅
- **TP 2RR**: 23314.70 ❌
- **TP 3RR**: 23275.47 ❌
- **TP 4RR**: 23236.24 ❌
- **TP 15RR**: 22804.71 ❌
- **PnL**: -39.23 points (-1.0R)
- **MFE**: 57.06 points
- **MAE**: 44.69 points

### Trade #1295 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 06:00:00
- **FVG 5m**: 23385.59 - 23399.22
- **Entrée**: 23402.50 @ 2025-08-06 07:19:00
- **Stop Loss**: 23354.97
- **Risk**: 47.53 points
- **TP 1RR**: 23450.04 ✅
- **TP 2RR**: 23497.57 ✅
- **TP 3RR**: 23545.11 ✅
- **TP 4RR**: 23592.64 ✅
- **TP 15RR**: 24115.53 ✅
- **PnL**: 713.02 points (15.0R)
- **MFE**: 715.01 points
- **MAE**: 26.51 points

### Trade #1296 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-06 08:45:00
- **FVG 5m**: 23467.64 - 23490.36
- **Entrée**: 23463.60 @ 2025-08-06 09:13:00
- **Stop Loss**: 23486.45
- **Risk**: 22.85 points
- **TP 1RR**: 23440.76 ✅
- **TP 2RR**: 23417.91 ✅
- **TP 3RR**: 23395.06 ✅
- **TP 4RR**: 23372.22 ❌
- **TP 15RR**: 23120.91 ❌
- **PnL**: -22.85 points (-1.0R)
- **MFE**: 69.94 points
- **MAE**: 30.04 points

### Trade #1297 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-06 09:00:00
- **FVG 5m**: 23467.64 - 23490.36
- **Entrée**: 23463.60 @ 2025-08-06 09:13:00
- **Stop Loss**: 23527.37
- **Risk**: 63.77 points
- **TP 1RR**: 23399.83 ✅
- **TP 2RR**: 23336.07 ❌
- **TP 3RR**: 23272.30 ❌
- **TP 4RR**: 23208.53 ❌
- **TP 15RR**: 22507.08 ❌
- **PnL**: -63.77 points (-1.0R)
- **MFE**: 69.94 points
- **MAE**: 64.38 points

### Trade #1298 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 09:30:00
- **FVG 5m**: 23491.63 - 23495.41
- **Entrée**: 23499.96 @ 2025-08-06 09:57:00
- **Stop Loss**: 23397.36
- **Risk**: 102.60 points
- **TP 1RR**: 23602.55 ✅
- **TP 2RR**: 23705.15 ✅
- **TP 3RR**: 23807.75 ✅
- **TP 4RR**: 23910.34 ✅
- **TP 15RR**: 25038.90 ❌
- **PnL**: -102.60 points (-1.0R)
- **MFE**: 806.91 points
- **MAE**: 103.26 points

### Trade #1299 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 09:30:00
- **FVG 5m**: 23491.63 - 23495.41
- **Entrée**: 23499.96 @ 2025-08-06 09:57:00
- **Stop Loss**: 23397.36
- **Risk**: 102.60 points
- **TP 1RR**: 23602.55 ✅
- **TP 2RR**: 23705.15 ✅
- **TP 3RR**: 23807.75 ✅
- **TP 4RR**: 23910.34 ✅
- **TP 15RR**: 25038.90 ❌
- **PnL**: -102.60 points (-1.0R)
- **MFE**: 806.91 points
- **MAE**: 103.26 points

### Trade #1300 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 10:15:00
- **FVG 5m**: 23569.64 - 23576.46
- **Entrée**: 23576.96 @ 2025-08-06 10:46:00
- **Stop Loss**: 23510.16
- **Risk**: 66.80 points
- **TP 1RR**: 23643.76 ✅
- **TP 2RR**: 23710.56 ✅
- **TP 3RR**: 23777.37 ✅
- **TP 4RR**: 23844.17 ✅
- **TP 15RR**: 24578.97 ❌
- **PnL**: -66.80 points (-1.0R)
- **MFE**: 729.91 points
- **MAE**: 71.45 points

### Trade #1301 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 10:15:00
- **FVG 5m**: 23569.64 - 23576.46
- **Entrée**: 23576.96 @ 2025-08-06 10:46:00
- **Stop Loss**: 23510.16
- **Risk**: 66.80 points
- **TP 1RR**: 23643.76 ✅
- **TP 2RR**: 23710.56 ✅
- **TP 3RR**: 23777.37 ✅
- **TP 4RR**: 23844.17 ✅
- **TP 15RR**: 24578.97 ❌
- **PnL**: -66.80 points (-1.0R)
- **MFE**: 729.91 points
- **MAE**: 71.45 points

### Trade #1302 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-06 19:15:00
- **FVG 5m**: 23710.52 - 23718.10
- **Entrée**: 23720.37 @ 2025-08-06 19:26:00
- **Stop Loss**: 23682.01
- **Risk**: 38.36 points
- **TP 1RR**: 23758.73 ✅
- **TP 2RR**: 23797.08 ✅
- **TP 3RR**: 23835.44 ✅
- **TP 4RR**: 23873.80 ✅
- **TP 15RR**: 24295.72 ❌
- **PnL**: -38.36 points (-1.0R)
- **MFE**: 185.06 points
- **MAE**: 44.18 points

### Trade #1303 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-06 23:15:00
- **FVG 5m**: 23719.11 - 23724.66
- **Entrée**: 23718.10 @ 2025-08-06 23:28:00
- **Stop Loss**: 23742.08
- **Risk**: 23.98 points
- **TP 1RR**: 23694.11 ✅
- **TP 2RR**: 23670.13 ❌
- **TP 3RR**: 23646.15 ❌
- **TP 4RR**: 23622.16 ❌
- **TP 15RR**: 23358.34 ❌
- **PnL**: -23.98 points (-1.0R)
- **MFE**: 31.31 points
- **MAE**: 27.77 points

### Trade #1304 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 06:00:00
- **FVG 5m**: 23832.72 - 23841.81
- **Entrée**: 23830.20 @ 2025-08-07 06:34:00
- **Stop Loss**: 23885.05
- **Risk**: 54.86 points
- **TP 1RR**: 23775.34 ❌
- **TP 2RR**: 23720.48 ❌
- **TP 3RR**: 23665.62 ❌
- **TP 4RR**: 23610.77 ❌
- **TP 15RR**: 23007.33 ❌
- **PnL**: -54.86 points (-1.0R)
- **MFE**: 26.76 points
- **MAE**: 57.31 points

### Trade #1305 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 09:00:00
- **FVG 5m**: 23810.76 - 23823.63
- **Entrée**: 23797.88 @ 2025-08-07 09:24:00
- **Stop Loss**: 23917.39
- **Risk**: 119.51 points
- **TP 1RR**: 23678.37 ✅
- **TP 2RR**: 23558.86 ❌
- **TP 3RR**: 23439.36 ❌
- **TP 4RR**: 23319.85 ❌
- **TP 15RR**: 22005.27 ❌
- **PnL**: -119.51 points (-1.0R)
- **MFE**: 237.83 points
- **MAE**: 120.18 points

### Trade #1306 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 10:15:00
- **FVG 5m**: 23764.05 - 23771.37
- **Entrée**: 23763.29 @ 2025-08-07 10:30:00
- **Stop Loss**: 23803.72
- **Risk**: 40.43 points
- **TP 1RR**: 23722.86 ✅
- **TP 2RR**: 23682.44 ✅
- **TP 3RR**: 23642.01 ✅
- **TP 4RR**: 23601.59 ✅
- **TP 15RR**: 23156.90 ❌
- **PnL**: -40.43 points (-1.0R)
- **MFE**: 203.24 points
- **MAE**: 41.66 points

### Trade #1307 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 11:30:00
- **FVG 5m**: 23661.54 - 23696.64
- **Entrée**: 23657.76 @ 2025-08-07 11:41:00
- **Stop Loss**: 23752.44
- **Risk**: 94.68 points
- **TP 1RR**: 23563.07 ✅
- **TP 2RR**: 23468.39 ❌
- **TP 3RR**: 23373.71 ❌
- **TP 4RR**: 23279.03 ❌
- **TP 15RR**: 22237.52 ❌
- **PnL**: -94.68 points (-1.0R)
- **MFE**: 97.71 points
- **MAE**: 102.76 points

### Trade #1308 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-07 11:45:00
- **FVG 5m**: 23610.29 - 23629.98
- **Entrée**: 23630.74 @ 2025-08-07 13:54:00
- **Stop Loss**: 23609.84
- **Risk**: 20.90 points
- **TP 1RR**: 23651.64 ✅
- **TP 2RR**: 23672.54 ✅
- **TP 3RR**: 23693.44 ✅
- **TP 4RR**: 23714.34 ✅
- **TP 15RR**: 23944.24 ✅
- **PnL**: 313.50 points (15.0R)
- **MFE**: 319.89 points
- **MAE**: 19.44 points

### Trade #1309 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 13:00:00
- **FVG 5m**: 23592.11 - 23610.04
- **Entrée**: 23581.76 @ 2025-08-07 13:13:00
- **Stop Loss**: 23674.38
- **Risk**: 92.62 points
- **TP 1RR**: 23489.14 ❌
- **TP 2RR**: 23396.51 ❌
- **TP 3RR**: 23303.89 ❌
- **TP 4RR**: 23211.27 ❌
- **TP 15RR**: 22192.41 ❌
- **PnL**: -92.62 points (-1.0R)
- **MFE**: 21.71 points
- **MAE**: 93.67 points

### Trade #1310 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 13:00:00
- **FVG 5m**: 23592.11 - 23610.04
- **Entrée**: 23581.76 @ 2025-08-07 13:13:00
- **Stop Loss**: 23674.38
- **Risk**: 92.62 points
- **TP 1RR**: 23489.14 ❌
- **TP 2RR**: 23396.51 ❌
- **TP 3RR**: 23303.89 ❌
- **TP 4RR**: 23211.27 ❌
- **TP 15RR**: 22192.41 ❌
- **PnL**: -92.62 points (-1.0R)
- **MFE**: 21.71 points
- **MAE**: 93.67 points

### Trade #1311 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-07 13:00:00
- **FVG 5m**: 23592.11 - 23610.04
- **Entrée**: 23581.76 @ 2025-08-07 13:13:00
- **Stop Loss**: 23674.38
- **Risk**: 92.62 points
- **TP 1RR**: 23489.14 ❌
- **TP 2RR**: 23396.51 ❌
- **TP 3RR**: 23303.89 ❌
- **TP 4RR**: 23211.27 ❌
- **TP 15RR**: 22192.41 ❌
- **PnL**: -92.62 points (-1.0R)
- **MFE**: 21.71 points
- **MAE**: 93.67 points

### Trade #1312 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-07 13:45:00
- **FVG 5m**: 23632.26 - 23644.37
- **Entrée**: 23648.92 @ 2025-08-07 14:31:00
- **Stop Loss**: 23568.96
- **Risk**: 79.96 points
- **TP 1RR**: 23728.88 ✅
- **TP 2RR**: 23808.84 ✅
- **TP 3RR**: 23888.80 ✅
- **TP 4RR**: 23968.75 ✅
- **TP 15RR**: 24848.30 ❌
- **PnL**: -79.96 points (-1.0R)
- **MFE**: 657.95 points
- **MAE**: 81.30 points

### Trade #1313 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-07 14:45:00
- **FVG 5m**: 23694.62 - 23732.24
- **Entrée**: 23733.75 @ 2025-08-07 14:59:00
- **Stop Loss**: 23656.78
- **Risk**: 76.97 points
- **TP 1RR**: 23810.72 ✅
- **TP 2RR**: 23887.70 ✅
- **TP 3RR**: 23964.67 ✅
- **TP 4RR**: 24041.64 ✅
- **TP 15RR**: 24888.35 ❌
- **PnL**: -76.97 points (-1.0R)
- **MFE**: 573.12 points
- **MAE**: 88.37 points

### Trade #1314 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-08 07:00:00
- **FVG 5m**: 23782.23 - 23787.28
- **Entrée**: 23779.95 @ 2025-08-08 07:13:00
- **Stop Loss**: 23821.65
- **Risk**: 41.70 points
- **TP 1RR**: 23738.26 ❌
- **TP 2RR**: 23696.56 ❌
- **TP 3RR**: 23654.86 ❌
- **TP 4RR**: 23613.17 ❌
- **TP 15RR**: 23154.50 ❌
- **PnL**: -41.70 points (-1.0R)
- **MFE**: 28.78 points
- **MAE**: 56.05 points

### Trade #1315 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-08 09:45:00
- **FVG 5m**: 23887.00 - 23894.33
- **Entrée**: 23884.23 @ 2025-08-08 10:32:00
- **Stop Loss**: 23936.58
- **Risk**: 52.36 points
- **TP 1RR**: 23831.87 ❌
- **TP 2RR**: 23779.51 ❌
- **TP 3RR**: 23727.15 ❌
- **TP 4RR**: 23674.79 ❌
- **TP 15RR**: 23098.85 ❌
- **PnL**: -52.36 points (-1.0R)
- **MFE**: 38.38 points
- **MAE**: 58.07 points

### Trade #1316 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-08 13:00:00
- **FVG 5m**: 23936.24 - 23939.77
- **Entrée**: 23930.18 @ 2025-08-08 14:31:00
- **Stop Loss**: 23970.94
- **Risk**: 40.76 points
- **TP 1RR**: 23889.42 ❌
- **TP 2RR**: 23848.65 ❌
- **TP 3RR**: 23807.89 ❌
- **TP 4RR**: 23767.13 ❌
- **TP 15RR**: 23318.75 ❌
- **PnL**: -40.76 points (-1.0R)
- **MFE**: 17.93 points
- **MAE**: 41.66 points

### Trade #1317 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-08 14:45:00
- **FVG 5m**: 23954.92 - 23964.77
- **Entrée**: 23971.08 @ 2025-08-08 15:03:00
- **Stop Loss**: 23900.30
- **Risk**: 70.78 points
- **TP 1RR**: 24041.86 ❌
- **TP 2RR**: 24112.64 ❌
- **TP 3RR**: 24183.43 ❌
- **TP 4RR**: 24254.21 ❌
- **TP 15RR**: 25032.82 ❌
- **PnL**: -70.78 points (-1.0R)
- **MFE**: 69.18 points
- **MAE**: 80.03 points

### Trade #1318 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-08 15:00:00
- **FVG 5m**: 23976.63 - 23984.96
- **Entrée**: 23987.24 @ 2025-08-08 15:13:00
- **Stop Loss**: 23935.88
- **Risk**: 51.36 points
- **TP 1RR**: 24038.60 ❌
- **TP 2RR**: 24089.96 ❌
- **TP 3RR**: 24141.32 ❌
- **TP 4RR**: 24192.68 ❌
- **TP 15RR**: 24757.64 ❌
- **PnL**: -51.36 points (-1.0R)
- **MFE**: 18.94 points
- **MAE**: 51.51 points

### Trade #1319 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-10 17:00:00
- **FVG 5m**: 23950.63 - 23955.93
- **Entrée**: 23949.87 @ 2025-08-10 18:24:00
- **Stop Loss**: 24018.18
- **Risk**: 68.31 points
- **TP 1RR**: 23881.56 ❌
- **TP 2RR**: 23813.26 ❌
- **TP 3RR**: 23744.95 ❌
- **TP 4RR**: 23676.65 ❌
- **TP 15RR**: 22925.29 ❌
- **PnL**: -68.31 points (-1.0R)
- **MFE**: 47.72 points
- **MAE**: 77.26 points

### Trade #1320 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 02:30:00
- **FVG 5m**: 23950.12 - 23954.92
- **Entrée**: 23947.85 @ 2025-08-11 02:51:00
- **Stop Loss**: 23990.14
- **Risk**: 42.29 points
- **TP 1RR**: 23905.56 ✅
- **TP 2RR**: 23863.28 ❌
- **TP 3RR**: 23820.99 ❌
- **TP 4RR**: 23778.71 ❌
- **TP 15RR**: 23313.56 ❌
- **PnL**: -42.29 points (-1.0R)
- **MFE**: 45.70 points
- **MAE**: 43.68 points

### Trade #1321 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 03:30:00
- **FVG 5m**: 23954.41 - 23956.94
- **Entrée**: 23961.23 @ 2025-08-11 04:30:00
- **Stop Loss**: 23908.87
- **Risk**: 52.36 points
- **TP 1RR**: 24013.59 ✅
- **TP 2RR**: 24065.94 ❌
- **TP 3RR**: 24118.30 ❌
- **TP 4RR**: 24170.66 ❌
- **TP 15RR**: 24746.58 ❌
- **PnL**: -52.36 points (-1.0R)
- **MFE**: 79.02 points
- **MAE**: 70.19 points

### Trade #1322 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 08:30:00
- **FVG 5m**: 23965.02 - 23975.12
- **Entrée**: 23982.19 @ 2025-08-11 10:14:00
- **Stop Loss**: 23903.32
- **Risk**: 78.86 points
- **TP 1RR**: 24061.05 ❌
- **TP 2RR**: 24139.91 ❌
- **TP 3RR**: 24218.78 ❌
- **TP 4RR**: 24297.64 ❌
- **TP 15RR**: 25165.14 ❌
- **PnL**: -78.86 points (-1.0R)
- **MFE**: 58.07 points
- **MAE**: 91.14 points

### Trade #1323 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24037.12
- **Risk**: 49.88 points
- **TP 1RR**: 23937.35 ✅
- **TP 2RR**: 23887.47 ✅
- **TP 3RR**: 23837.58 ✅
- **TP 4RR**: 23787.70 ❌
- **TP 15RR**: 23238.98 ❌
- **PnL**: -49.88 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 54.28 points

### Trade #1324 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24037.12
- **Risk**: 49.88 points
- **TP 1RR**: 23937.35 ✅
- **TP 2RR**: 23887.47 ✅
- **TP 3RR**: 23837.58 ✅
- **TP 4RR**: 23787.70 ❌
- **TP 15RR**: 23238.98 ❌
- **PnL**: -49.88 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 54.28 points

### Trade #1325 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24037.12
- **Risk**: 49.88 points
- **TP 1RR**: 23937.35 ✅
- **TP 2RR**: 23887.47 ✅
- **TP 3RR**: 23837.58 ✅
- **TP 4RR**: 23787.70 ❌
- **TP 15RR**: 23238.98 ❌
- **PnL**: -49.88 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 54.28 points

### Trade #1326 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24037.12
- **Risk**: 49.88 points
- **TP 1RR**: 23937.35 ✅
- **TP 2RR**: 23887.47 ✅
- **TP 3RR**: 23837.58 ✅
- **TP 4RR**: 23787.70 ❌
- **TP 15RR**: 23238.98 ❌
- **PnL**: -49.88 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 54.28 points

### Trade #1327 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-11 11:30:00
- **FVG 5m**: 23988.75 - 23999.61
- **Entrée**: 23987.24 @ 2025-08-11 11:42:00
- **Stop Loss**: 24037.12
- **Risk**: 49.88 points
- **TP 1RR**: 23937.35 ✅
- **TP 2RR**: 23887.47 ✅
- **TP 3RR**: 23837.58 ✅
- **TP 4RR**: 23787.70 ❌
- **TP 15RR**: 23238.98 ❌
- **PnL**: -49.88 points (-1.0R)
- **MFE**: 166.13 points
- **MAE**: 54.28 points

### Trade #1328 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 14:45:00
- **FVG 5m**: 23860.49 - 23870.85
- **Entrée**: 23871.60 @ 2025-08-11 17:53:00
- **Stop Loss**: 23809.20
- **Risk**: 62.41 points
- **TP 1RR**: 23934.01 ✅
- **TP 2RR**: 23996.41 ✅
- **TP 3RR**: 24058.82 ✅
- **TP 4RR**: 24121.23 ✅
- **TP 15RR**: 24807.69 ❌
- **PnL**: -62.41 points (-1.0R)
- **MFE**: 435.27 points
- **MAE**: 77.01 points

### Trade #1329 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-11 19:15:00
- **FVG 5m**: 23877.91 - 23885.24
- **Entrée**: 23886.50 @ 2025-08-11 20:38:00
- **Stop Loss**: 23857.14
- **Risk**: 29.36 points
- **TP 1RR**: 23915.85 ❌
- **TP 2RR**: 23945.21 ❌
- **TP 3RR**: 23974.56 ❌
- **TP 4RR**: 24003.92 ❌
- **TP 15RR**: 24326.83 ❌
- **PnL**: -29.36 points (-1.0R)
- **MFE**: 24.74 points
- **MAE**: 31.56 points

### Trade #1330 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-12 00:00:00
- **FVG 5m**: 23850.90 - 23858.22
- **Entrée**: 23861.25 @ 2025-08-12 00:53:00
- **Stop Loss**: 23823.08
- **Risk**: 38.17 points
- **TP 1RR**: 23899.43 ✅
- **TP 2RR**: 23937.60 ✅
- **TP 3RR**: 23975.78 ✅
- **TP 4RR**: 24013.95 ✅
- **TP 15RR**: 24433.88 ❌
- **PnL**: -38.17 points (-1.0R)
- **MFE**: 445.62 points
- **MAE**: 51.00 points

### Trade #1331 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-12 00:00:00
- **FVG 5m**: 23850.90 - 23858.22
- **Entrée**: 23861.25 @ 2025-08-12 00:53:00
- **Stop Loss**: 23823.08
- **Risk**: 38.17 points
- **TP 1RR**: 23899.43 ✅
- **TP 2RR**: 23937.60 ✅
- **TP 3RR**: 23975.78 ✅
- **TP 4RR**: 24013.95 ✅
- **TP 15RR**: 24433.88 ❌
- **PnL**: -38.17 points (-1.0R)
- **MFE**: 445.62 points
- **MAE**: 51.00 points

### Trade #1332 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-12 07:30:00
- **FVG 5m**: 23984.46 - 24002.89
- **Entrée**: 23980.42 @ 2025-08-12 08:04:00
- **Stop Loss**: 24070.21
- **Risk**: 89.79 points
- **TP 1RR**: 23890.63 ✅
- **TP 2RR**: 23800.84 ❌
- **TP 3RR**: 23711.04 ❌
- **TP 4RR**: 23621.25 ❌
- **TP 15RR**: 22633.54 ❌
- **PnL**: -89.79 points (-1.0R)
- **MFE**: 124.47 points
- **MAE**: 90.64 points

### Trade #1333 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-12 07:30:00
- **FVG 5m**: 23984.46 - 24002.89
- **Entrée**: 23980.42 @ 2025-08-12 08:04:00
- **Stop Loss**: 24070.21
- **Risk**: 89.79 points
- **TP 1RR**: 23890.63 ✅
- **TP 2RR**: 23800.84 ❌
- **TP 3RR**: 23711.04 ❌
- **TP 4RR**: 23621.25 ❌
- **TP 15RR**: 22633.54 ❌
- **PnL**: -89.79 points (-1.0R)
- **MFE**: 124.47 points
- **MAE**: 90.64 points

### Trade #1334 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-13 09:15:00
- **FVG 5m**: 24182.15 - 24192.25
- **Entrée**: 24174.57 @ 2025-08-13 10:03:00
- **Stop Loss**: 24254.61
- **Risk**: 80.04 points
- **TP 1RR**: 24094.54 ✅
- **TP 2RR**: 24014.50 ✅
- **TP 3RR**: 23934.46 ✅
- **TP 4RR**: 23854.42 ✅
- **TP 15RR**: 22974.01 ❌
- **PnL**: -80.04 points (-1.0R)
- **MFE**: 921.28 points
- **MAE**: 107.81 points

### Trade #1335 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-13 09:15:00
- **FVG 5m**: 24182.15 - 24192.25
- **Entrée**: 24174.57 @ 2025-08-13 10:03:00
- **Stop Loss**: 24254.61
- **Risk**: 80.04 points
- **TP 1RR**: 24094.54 ✅
- **TP 2RR**: 24014.50 ✅
- **TP 3RR**: 23934.46 ✅
- **TP 4RR**: 23854.42 ✅
- **TP 15RR**: 22974.01 ❌
- **PnL**: -80.04 points (-1.0R)
- **MFE**: 921.28 points
- **MAE**: 107.81 points

### Trade #1336 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-13 10:15:00
- **FVG 5m**: 24147.56 - 24158.92
- **Entrée**: 24159.93 @ 2025-08-13 12:19:00
- **Stop Loss**: 24116.81
- **Risk**: 43.12 points
- **TP 1RR**: 24203.05 ❌
- **TP 2RR**: 24246.17 ❌
- **TP 3RR**: 24289.29 ❌
- **TP 4RR**: 24332.41 ❌
- **TP 15RR**: 24806.71 ❌
- **PnL**: -43.12 points (-1.0R)
- **MFE**: 44.18 points
- **MAE**: 71.45 points

### Trade #1337 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-13 10:30:00
- **FVG 5m**: 24147.56 - 24158.92
- **Entrée**: 24159.93 @ 2025-08-13 12:19:00
- **Stop Loss**: 24141.54
- **Risk**: 18.39 points
- **TP 1RR**: 24178.32 ✅
- **TP 2RR**: 24196.71 ❌
- **TP 3RR**: 24215.10 ❌
- **TP 4RR**: 24233.48 ❌
- **TP 15RR**: 24435.76 ❌
- **PnL**: -18.39 points (-1.0R)
- **MFE**: 25.00 points
- **MAE**: 19.95 points

### Trade #1338 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24216.22
- **Risk**: 31.04 points
- **TP 1RR**: 24154.14 ✅
- **TP 2RR**: 24123.10 ✅
- **TP 3RR**: 24092.06 ❌
- **TP 4RR**: 24061.03 ❌
- **TP 15RR**: 23719.61 ❌
- **PnL**: -31.04 points (-1.0R)
- **MFE**: 85.84 points
- **MAE**: 31.05 points

### Trade #1339 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24216.22
- **Risk**: 31.04 points
- **TP 1RR**: 24154.14 ✅
- **TP 2RR**: 24123.10 ✅
- **TP 3RR**: 24092.06 ❌
- **TP 4RR**: 24061.03 ❌
- **TP 15RR**: 23719.61 ❌
- **PnL**: -31.04 points (-1.0R)
- **MFE**: 85.84 points
- **MAE**: 31.05 points

### Trade #1340 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24216.22
- **Risk**: 31.04 points
- **TP 1RR**: 24154.14 ✅
- **TP 2RR**: 24123.10 ✅
- **TP 3RR**: 24092.06 ❌
- **TP 4RR**: 24061.03 ❌
- **TP 15RR**: 23719.61 ❌
- **PnL**: -31.04 points (-1.0R)
- **MFE**: 85.84 points
- **MAE**: 31.05 points

### Trade #1341 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 07:30:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24216.22
- **Risk**: 31.04 points
- **TP 1RR**: 24154.14 ✅
- **TP 2RR**: 24123.10 ✅
- **TP 3RR**: 24092.06 ❌
- **TP 4RR**: 24061.03 ❌
- **TP 15RR**: 23719.61 ❌
- **PnL**: -31.04 points (-1.0R)
- **MFE**: 85.84 points
- **MAE**: 31.05 points

### Trade #1342 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24065.33
- **Risk**: 146.86 points
- **TP 1RR**: 24359.05 ❌
- **TP 2RR**: 24505.91 ❌
- **TP 3RR**: 24652.78 ❌
- **TP 4RR**: 24799.64 ❌
- **TP 15RR**: 26415.11 ❌
- **PnL**: -146.86 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 163.60 points

### Trade #1343 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24065.33
- **Risk**: 146.86 points
- **TP 1RR**: 24359.05 ❌
- **TP 2RR**: 24505.91 ❌
- **TP 3RR**: 24652.78 ❌
- **TP 4RR**: 24799.64 ❌
- **TP 15RR**: 26415.11 ❌
- **PnL**: -146.86 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 163.60 points

### Trade #1344 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24065.33
- **Risk**: 146.86 points
- **TP 1RR**: 24359.05 ❌
- **TP 2RR**: 24505.91 ❌
- **TP 3RR**: 24652.78 ❌
- **TP 4RR**: 24799.64 ❌
- **TP 15RR**: 26415.11 ❌
- **PnL**: -146.86 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 163.60 points

### Trade #1345 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24065.33
- **Risk**: 146.86 points
- **TP 1RR**: 24359.05 ❌
- **TP 2RR**: 24505.91 ❌
- **TP 3RR**: 24652.78 ❌
- **TP 4RR**: 24799.64 ❌
- **TP 15RR**: 26415.11 ❌
- **PnL**: -146.86 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 163.60 points

### Trade #1346 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24065.33
- **Risk**: 146.86 points
- **TP 1RR**: 24359.05 ❌
- **TP 2RR**: 24505.91 ❌
- **TP 3RR**: 24652.78 ❌
- **TP 4RR**: 24799.64 ❌
- **TP 15RR**: 26415.11 ❌
- **PnL**: -146.86 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 163.60 points

### Trade #1347 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-14 08:30:00
- **FVG 5m**: 24193.26 - 24199.57
- **Entrée**: 24212.19 @ 2025-08-14 09:31:00
- **Stop Loss**: 24065.33
- **Risk**: 146.86 points
- **TP 1RR**: 24359.05 ❌
- **TP 2RR**: 24505.91 ❌
- **TP 3RR**: 24652.78 ❌
- **TP 4RR**: 24799.64 ❌
- **TP 15RR**: 26415.11 ❌
- **PnL**: -146.86 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 163.60 points

### Trade #1348 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 09:45:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24257.64
- **Risk**: 72.46 points
- **TP 1RR**: 24112.71 ✅
- **TP 2RR**: 24040.25 ✅
- **TP 3RR**: 23967.78 ✅
- **TP 4RR**: 23895.32 ✅
- **TP 15RR**: 23098.21 ❌
- **PnL**: -72.46 points (-1.0R)
- **MFE**: 931.89 points
- **MAE**: 97.20 points

### Trade #1349 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 09:45:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24257.64
- **Risk**: 72.46 points
- **TP 1RR**: 24112.71 ✅
- **TP 2RR**: 24040.25 ✅
- **TP 3RR**: 23967.78 ✅
- **TP 4RR**: 23895.32 ✅
- **TP 15RR**: 23098.21 ❌
- **PnL**: -72.46 points (-1.0R)
- **MFE**: 931.89 points
- **MAE**: 97.20 points

### Trade #1350 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-14 09:45:00
- **FVG 5m**: 24198.05 - 24211.18
- **Entrée**: 24185.18 @ 2025-08-14 09:57:00
- **Stop Loss**: 24257.64
- **Risk**: 72.46 points
- **TP 1RR**: 24112.71 ✅
- **TP 2RR**: 24040.25 ✅
- **TP 3RR**: 23967.78 ✅
- **TP 4RR**: 23895.32 ✅
- **TP 15RR**: 23098.21 ❌
- **PnL**: -72.46 points (-1.0R)
- **MFE**: 931.89 points
- **MAE**: 97.20 points

### Trade #1351 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-15 04:00:00
- **FVG 5m**: 24131.15 - 24135.94
- **Entrée**: 24137.71 @ 2025-08-15 05:31:00
- **Stop Loss**: 24102.93
- **Risk**: 34.78 points
- **TP 1RR**: 24172.49 ❌
- **TP 2RR**: 24207.27 ❌
- **TP 3RR**: 24242.05 ❌
- **TP 4RR**: 24276.83 ❌
- **TP 15RR**: 24659.42 ❌
- **PnL**: -34.78 points (-1.0R)
- **MFE**: 26.51 points
- **MAE**: 40.90 points

### Trade #1352 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-15 08:45:00
- **FVG 5m**: 24054.14 - 24063.48
- **Entrée**: 24049.35 @ 2025-08-15 09:46:00
- **Stop Loss**: 24102.29
- **Risk**: 52.95 points
- **TP 1RR**: 23996.40 ✅
- **TP 2RR**: 23943.45 ❌
- **TP 3RR**: 23890.51 ❌
- **TP 4RR**: 23837.56 ❌
- **TP 15RR**: 23255.15 ❌
- **PnL**: -52.95 points (-1.0R)
- **MFE**: 79.78 points
- **MAE**: 54.03 points

### Trade #1353 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-15 08:45:00
- **FVG 5m**: 24054.14 - 24063.48
- **Entrée**: 24049.35 @ 2025-08-15 09:46:00
- **Stop Loss**: 24102.29
- **Risk**: 52.95 points
- **TP 1RR**: 23996.40 ✅
- **TP 2RR**: 23943.45 ❌
- **TP 3RR**: 23890.51 ❌
- **TP 4RR**: 23837.56 ❌
- **TP 15RR**: 23255.15 ❌
- **PnL**: -52.95 points (-1.0R)
- **MFE**: 79.78 points
- **MAE**: 54.03 points

### Trade #1354 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-15 08:45:00
- **FVG 5m**: 24050.10 - 24077.12
- **Entrée**: 24077.62 @ 2025-08-15 09:03:00
- **Stop Loss**: 23993.66
- **Risk**: 83.96 points
- **TP 1RR**: 24161.58 ❌
- **TP 2RR**: 24245.54 ❌
- **TP 3RR**: 24329.50 ❌
- **TP 4RR**: 24413.46 ❌
- **TP 15RR**: 25337.00 ❌
- **PnL**: -83.96 points (-1.0R)
- **MFE**: 39.89 points
- **MAE**: 86.35 points

### Trade #1355 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 03:30:00
- **FVG 5m**: 24012.23 - 24020.06
- **Entrée**: 24021.57 @ 2025-08-18 05:42:00
- **Stop Loss**: 23982.31
- **Risk**: 39.26 points
- **TP 1RR**: 24060.84 ❌
- **TP 2RR**: 24100.10 ❌
- **TP 3RR**: 24139.37 ❌
- **TP 4RR**: 24178.63 ❌
- **TP 15RR**: 24610.54 ❌
- **PnL**: -39.26 points (-1.0R)
- **MFE**: 6.06 points
- **MAE**: 39.64 points

### Trade #1356 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 03:30:00
- **FVG 5m**: 24012.23 - 24020.06
- **Entrée**: 24021.57 @ 2025-08-18 05:42:00
- **Stop Loss**: 23982.31
- **Risk**: 39.26 points
- **TP 1RR**: 24060.84 ❌
- **TP 2RR**: 24100.10 ❌
- **TP 3RR**: 24139.37 ❌
- **TP 4RR**: 24178.63 ❌
- **TP 15RR**: 24610.54 ❌
- **PnL**: -39.26 points (-1.0R)
- **MFE**: 6.06 points
- **MAE**: 39.64 points

### Trade #1357 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-18 08:30:00
- **FVG 5m**: 24004.40 - 24007.69
- **Entrée**: 23987.24 @ 2025-08-18 08:51:00
- **Stop Loss**: 24065.16
- **Risk**: 77.92 points
- **TP 1RR**: 23909.31 ❌
- **TP 2RR**: 23831.39 ❌
- **TP 3RR**: 23753.47 ❌
- **TP 4RR**: 23675.55 ❌
- **TP 15RR**: 22818.39 ❌
- **PnL**: -77.92 points (-1.0R)
- **MFE**: 33.33 points
- **MAE**: 86.85 points

### Trade #1358 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 09:45:00
- **FVG 5m**: 23989.26 - 23992.29
- **Entrée**: 23993.04 @ 2025-08-18 12:13:00
- **Stop Loss**: 23941.93
- **Risk**: 51.11 points
- **TP 1RR**: 24044.15 ✅
- **TP 2RR**: 24095.26 ❌
- **TP 3RR**: 24146.38 ❌
- **TP 4RR**: 24197.49 ❌
- **TP 15RR**: 24759.70 ❌
- **PnL**: -51.11 points (-1.0R)
- **MFE**: 81.04 points
- **MAE**: 72.21 points

### Trade #1359 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 09:45:00
- **FVG 5m**: 23989.26 - 23992.29
- **Entrée**: 23993.04 @ 2025-08-18 12:13:00
- **Stop Loss**: 23941.93
- **Risk**: 51.11 points
- **TP 1RR**: 24044.15 ✅
- **TP 2RR**: 24095.26 ❌
- **TP 3RR**: 24146.38 ❌
- **TP 4RR**: 24197.49 ❌
- **TP 15RR**: 24759.70 ❌
- **PnL**: -51.11 points (-1.0R)
- **MFE**: 81.04 points
- **MAE**: 72.21 points

### Trade #1360 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 09:45:00
- **FVG 5m**: 23989.26 - 23992.29
- **Entrée**: 23993.04 @ 2025-08-18 12:13:00
- **Stop Loss**: 23941.93
- **Risk**: 51.11 points
- **TP 1RR**: 24044.15 ✅
- **TP 2RR**: 24095.26 ❌
- **TP 3RR**: 24146.38 ❌
- **TP 4RR**: 24197.49 ❌
- **TP 15RR**: 24759.70 ❌
- **PnL**: -51.11 points (-1.0R)
- **MFE**: 81.04 points
- **MAE**: 72.21 points

### Trade #1361 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-18 20:30:00
- **FVG 5m**: 24000.87 - 24010.46
- **Entrée**: 24012.48 @ 2025-08-18 22:24:00
- **Stop Loss**: 23993.92
- **Risk**: 18.57 points
- **TP 1RR**: 24031.05 ❌
- **TP 2RR**: 24049.62 ❌
- **TP 3RR**: 24068.19 ❌
- **TP 4RR**: 24086.75 ❌
- **TP 15RR**: 24290.99 ❌
- **PnL**: -18.57 points (-1.0R)
- **MFE**: 10.60 points
- **MAE**: 19.44 points

### Trade #1362 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 02:30:00
- **FVG 5m**: 23993.04 - 23998.60
- **Entrée**: 24000.37 @ 2025-08-19 02:42:00
- **Stop Loss**: 23970.95
- **Risk**: 29.41 points
- **TP 1RR**: 24029.78 ✅
- **TP 2RR**: 24059.19 ❌
- **TP 3RR**: 24088.60 ❌
- **TP 4RR**: 24118.01 ❌
- **TP 15RR**: 24441.55 ❌
- **PnL**: -29.41 points (-1.0R)
- **MFE**: 40.14 points
- **MAE**: 29.54 points

### Trade #1363 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 03:00:00
- **FVG 5m**: 23992.29 - 23996.07
- **Entrée**: 23984.21 @ 2025-08-19 03:11:00
- **Stop Loss**: 24031.82
- **Risk**: 47.61 points
- **TP 1RR**: 23936.60 ❌
- **TP 2RR**: 23888.99 ❌
- **TP 3RR**: 23841.38 ❌
- **TP 4RR**: 23793.77 ❌
- **TP 15RR**: 23270.07 ❌
- **PnL**: -47.61 points (-1.0R)
- **MFE**: 3.53 points
- **MAE**: 51.51 points

### Trade #1364 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23845.65
- **Risk**: 71.75 points
- **TP 1RR**: 23702.14 ✅
- **TP 2RR**: 23630.39 ✅
- **TP 3RR**: 23558.63 ✅
- **TP 4RR**: 23486.88 ✅
- **TP 15RR**: 22697.59 ❌
- **PnL**: -71.75 points (-1.0R)
- **MFE**: 510.76 points
- **MAE**: 89.88 points

### Trade #1365 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23845.65
- **Risk**: 71.75 points
- **TP 1RR**: 23702.14 ✅
- **TP 2RR**: 23630.39 ✅
- **TP 3RR**: 23558.63 ✅
- **TP 4RR**: 23486.88 ✅
- **TP 15RR**: 22697.59 ❌
- **PnL**: -71.75 points (-1.0R)
- **MFE**: 510.76 points
- **MAE**: 89.88 points

### Trade #1366 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23845.65
- **Risk**: 71.75 points
- **TP 1RR**: 23702.14 ✅
- **TP 2RR**: 23630.39 ✅
- **TP 3RR**: 23558.63 ✅
- **TP 4RR**: 23486.88 ✅
- **TP 15RR**: 22697.59 ❌
- **PnL**: -71.75 points (-1.0R)
- **MFE**: 510.76 points
- **MAE**: 89.88 points

### Trade #1367 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23845.65
- **Risk**: 71.75 points
- **TP 1RR**: 23702.14 ✅
- **TP 2RR**: 23630.39 ✅
- **TP 3RR**: 23558.63 ✅
- **TP 4RR**: 23486.88 ✅
- **TP 15RR**: 22697.59 ❌
- **PnL**: -71.75 points (-1.0R)
- **MFE**: 510.76 points
- **MAE**: 89.88 points

### Trade #1368 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-19 09:45:00
- **FVG 5m**: 23784.50 - 23800.66
- **Entrée**: 23773.89 @ 2025-08-19 09:59:00
- **Stop Loss**: 23845.65
- **Risk**: 71.75 points
- **TP 1RR**: 23702.14 ✅
- **TP 2RR**: 23630.39 ✅
- **TP 3RR**: 23558.63 ✅
- **TP 4RR**: 23486.88 ✅
- **TP 15RR**: 22697.59 ❌
- **PnL**: -71.75 points (-1.0R)
- **MFE**: 510.76 points
- **MAE**: 89.88 points

### Trade #1369 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 14:15:00
- **FVG 5m**: 23695.12 - 23702.95
- **Entrée**: 23714.56 @ 2025-08-19 15:00:00
- **Stop Loss**: 23647.95
- **Risk**: 66.62 points
- **TP 1RR**: 23781.18 ❌
- **TP 2RR**: 23847.80 ❌
- **TP 3RR**: 23914.41 ❌
- **TP 4RR**: 23981.03 ❌
- **TP 15RR**: 24713.82 ❌
- **PnL**: -66.62 points (-1.0R)
- **MFE**: 5.55 points
- **MAE**: 69.18 points

### Trade #1370 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-19 18:15:00
- **FVG 5m**: 23641.60 - 23646.39
- **Entrée**: 23646.90 @ 2025-08-19 19:46:00
- **Stop Loss**: 23633.56
- **Risk**: 13.34 points
- **TP 1RR**: 23660.24 ❌
- **TP 2RR**: 23673.57 ❌
- **TP 3RR**: 23686.91 ❌
- **TP 4RR**: 23700.25 ❌
- **TP 15RR**: 23846.96 ❌
- **PnL**: -13.34 points (-1.0R)
- **MFE**: 9.85 points
- **MAE**: 13.89 points

### Trade #1371 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-20 03:00:00
- **FVG 5m**: 23626.20 - 23629.73
- **Entrée**: 23625.19 @ 2025-08-20 03:11:00
- **Stop Loss**: 23654.18
- **Risk**: 28.99 points
- **TP 1RR**: 23596.20 ❌
- **TP 2RR**: 23567.21 ❌
- **TP 3RR**: 23538.22 ❌
- **TP 4RR**: 23509.23 ❌
- **TP 15RR**: 23190.34 ❌
- **PnL**: -28.99 points (-1.0R)
- **MFE**: 22.47 points
- **MAE**: 32.06 points

### Trade #1372 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-20 06:15:00
- **FVG 5m**: 23652.45 - 23659.27
- **Entrée**: 23650.18 @ 2025-08-20 06:27:00
- **Stop Loss**: 23688.28
- **Risk**: 38.10 points
- **TP 1RR**: 23612.09 ✅
- **TP 2RR**: 23573.99 ✅
- **TP 3RR**: 23535.89 ✅
- **TP 4RR**: 23497.80 ✅
- **TP 15RR**: 23078.75 ❌
- **PnL**: -38.10 points (-1.0R)
- **MFE**: 387.05 points
- **MAE**: 49.74 points

### Trade #1373 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-20 08:45:00
- **FVG 5m**: 23358.07 - 23394.42
- **Entrée**: 23352.51 @ 2025-08-20 09:06:00
- **Stop Loss**: 23567.03
- **Risk**: 214.52 points
- **TP 1RR**: 23138.00 ❌
- **TP 2RR**: 22923.48 ❌
- **TP 3RR**: 22708.96 ❌
- **TP 4RR**: 22494.45 ❌
- **TP 15RR**: 20134.77 ❌
- **PnL**: -214.52 points (-1.0R)
- **MFE**: 89.38 points
- **MAE**: 231.52 points

### Trade #1374 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 09:45:00
- **FVG 5m**: 23289.65 - 23302.52
- **Entrée**: 23305.05 @ 2025-08-20 10:04:00
- **Stop Loss**: 23251.50
- **Risk**: 53.54 points
- **TP 1RR**: 23358.59 ✅
- **TP 2RR**: 23412.13 ✅
- **TP 3RR**: 23465.67 ✅
- **TP 4RR**: 23519.22 ✅
- **TP 15RR**: 24108.19 ✅
- **PnL**: 803.14 points (15.0R)
- **MFE**: 806.41 points
- **MAE**: 51.76 points

### Trade #1375 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 14:30:00
- **FVG 5m**: 23550.96 - 23553.48
- **Entrée**: 23560.05 @ 2025-08-20 17:09:00
- **Stop Loss**: 23533.13
- **Risk**: 26.92 points
- **TP 1RR**: 23586.97 ❌
- **TP 2RR**: 23613.89 ❌
- **TP 3RR**: 23640.81 ❌
- **TP 4RR**: 23667.73 ❌
- **TP 15RR**: 23963.86 ❌
- **PnL**: -26.92 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 29.03 points

### Trade #1376 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-20 14:30:00
- **FVG 5m**: 23550.96 - 23553.48
- **Entrée**: 23560.05 @ 2025-08-20 17:09:00
- **Stop Loss**: 23533.13
- **Risk**: 26.92 points
- **TP 1RR**: 23586.97 ❌
- **TP 2RR**: 23613.89 ❌
- **TP 3RR**: 23640.81 ❌
- **TP 4RR**: 23667.73 ❌
- **TP 15RR**: 23963.86 ❌
- **PnL**: -26.92 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 29.03 points

### Trade #1377 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-21 03:45:00
- **FVG 5m**: 23536.31 - 23543.64
- **Entrée**: 23528.99 @ 2025-08-21 03:59:00
- **Stop Loss**: 23586.48
- **Risk**: 57.49 points
- **TP 1RR**: 23471.51 ✅
- **TP 2RR**: 23414.02 ✅
- **TP 3RR**: 23356.54 ✅
- **TP 4RR**: 23299.05 ❌
- **TP 15RR**: 22666.71 ❌
- **PnL**: -57.49 points (-1.0R)
- **MFE**: 223.69 points
- **MAE**: 170.93 points

### Trade #1378 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-21 12:30:00
- **FVG 5m**: 23429.26 - 23432.55
- **Entrée**: 23443.15 @ 2025-08-21 13:55:00
- **Stop Loss**: 23358.25
- **Risk**: 84.90 points
- **TP 1RR**: 23528.05 ❌
- **TP 2RR**: 23612.96 ❌
- **TP 3RR**: 23697.86 ❌
- **TP 4RR**: 23782.76 ❌
- **TP 15RR**: 24716.70 ❌
- **PnL**: -84.90 points (-1.0R)
- **MFE**: 42.42 points
- **MAE**: 99.98 points

### Trade #1379 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-22 01:45:00
- **FVG 5m**: 23373.47 - 23391.90
- **Entrée**: 23396.44 @ 2025-08-22 02:04:00
- **Stop Loss**: 23297.43
- **Risk**: 99.01 points
- **TP 1RR**: 23495.45 ✅
- **TP 2RR**: 23594.47 ✅
- **TP 3RR**: 23693.48 ✅
- **TP 4RR**: 23792.49 ✅
- **TP 15RR**: 24881.61 ❌
- **PnL**: -99.01 points (-1.0R)
- **MFE**: 643.06 points
- **MAE**: 107.81 points

### Trade #1380 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-22 02:45:00
- **FVG 5m**: 23432.80 - 23452.74
- **Entrée**: 23454.01 @ 2025-08-22 03:09:00
- **Stop Loss**: 23389.54
- **Risk**: 64.47 points
- **TP 1RR**: 23518.48 ✅
- **TP 2RR**: 23582.94 ✅
- **TP 3RR**: 23647.41 ✅
- **TP 4RR**: 23711.88 ✅
- **TP 15RR**: 24421.03 ❌
- **PnL**: -64.47 points (-1.0R)
- **MFE**: 585.49 points
- **MAE**: 65.14 points

### Trade #1381 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-24 22:30:00
- **FVG 5m**: 23782.98 - 23788.29
- **Entrée**: 23790.81 @ 2025-08-24 23:18:00
- **Stop Loss**: 23752.17
- **Risk**: 38.64 points
- **TP 1RR**: 23829.45 ❌
- **TP 2RR**: 23868.10 ❌
- **TP 3RR**: 23906.74 ❌
- **TP 4RR**: 23945.39 ❌
- **TP 15RR**: 24370.48 ❌
- **PnL**: -38.64 points (-1.0R)
- **MFE**: 11.11 points
- **MAE**: 39.13 points

### Trade #1382 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 02:00:00
- **FVG 5m**: 23756.73 - 23760.77
- **Entrée**: 23762.28 @ 2025-08-25 02:44:00
- **Stop Loss**: 23728.70
- **Risk**: 33.58 points
- **TP 1RR**: 23795.86 ❌
- **TP 2RR**: 23829.45 ❌
- **TP 3RR**: 23863.03 ❌
- **TP 4RR**: 23896.61 ❌
- **TP 15RR**: 24266.03 ❌
- **PnL**: -33.58 points (-1.0R)
- **MFE**: 8.58 points
- **MAE**: 38.38 points

### Trade #1383 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 08:30:00
- **FVG 5m**: 23728.95 - 23737.79
- **Entrée**: 23743.09 @ 2025-08-25 08:57:00
- **Stop Loss**: 23663.59
- **Risk**: 79.50 points
- **TP 1RR**: 23822.59 ✅
- **TP 2RR**: 23902.09 ❌
- **TP 3RR**: 23981.60 ❌
- **TP 4RR**: 24061.10 ❌
- **TP 15RR**: 24935.61 ❌
- **PnL**: -79.50 points (-1.0R)
- **MFE**: 107.05 points
- **MAE**: 101.24 points

### Trade #1384 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 08:45:00
- **FVG 5m**: 23728.95 - 23737.79
- **Entrée**: 23743.09 @ 2025-08-25 08:57:00
- **Stop Loss**: 23668.64
- **Risk**: 74.45 points
- **TP 1RR**: 23817.55 ✅
- **TP 2RR**: 23892.00 ❌
- **TP 3RR**: 23966.46 ❌
- **TP 4RR**: 24040.91 ❌
- **TP 15RR**: 24859.91 ❌
- **PnL**: -74.45 points (-1.0R)
- **MFE**: 107.05 points
- **MAE**: 101.24 points

### Trade #1385 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 08:45:00
- **FVG 5m**: 23728.95 - 23737.79
- **Entrée**: 23743.09 @ 2025-08-25 08:57:00
- **Stop Loss**: 23668.64
- **Risk**: 74.45 points
- **TP 1RR**: 23817.55 ✅
- **TP 2RR**: 23892.00 ❌
- **TP 3RR**: 23966.46 ❌
- **TP 4RR**: 24040.91 ❌
- **TP 15RR**: 24859.91 ❌
- **PnL**: -74.45 points (-1.0R)
- **MFE**: 107.05 points
- **MAE**: 101.24 points

### Trade #1386 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 11:45:00
- **FVG 5m**: 23808.48 - 23811.01
- **Entrée**: 23808.23 @ 2025-08-25 12:36:00
- **Stop Loss**: 23858.53
- **Risk**: 50.30 points
- **TP 1RR**: 23757.93 ✅
- **TP 2RR**: 23707.63 ✅
- **TP 3RR**: 23657.33 ✅
- **TP 4RR**: 23607.03 ✅
- **TP 15RR**: 23053.74 ❌
- **PnL**: -50.30 points (-1.0R)
- **MFE**: 205.26 points
- **MAE**: 50.50 points

### Trade #1387 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 13:15:00
- **FVG 5m**: 23792.83 - 23799.14
- **Entrée**: 23790.81 @ 2025-08-25 14:20:00
- **Stop Loss**: 23829.23
- **Risk**: 38.42 points
- **TP 1RR**: 23752.39 ✅
- **TP 2RR**: 23713.97 ✅
- **TP 3RR**: 23675.55 ✅
- **TP 4RR**: 23637.14 ✅
- **TP 15RR**: 23214.53 ❌
- **PnL**: -38.42 points (-1.0R)
- **MFE**: 187.84 points
- **MAE**: 42.92 points

### Trade #1388 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-25 19:00:00
- **FVG 5m**: 23628.22 - 23635.03
- **Entrée**: 23638.82 @ 2025-08-25 19:51:00
- **Stop Loss**: 23630.03
- **Risk**: 8.79 points
- **TP 1RR**: 23647.61 ❌
- **TP 2RR**: 23656.40 ❌
- **TP 3RR**: 23665.19 ❌
- **TP 4RR**: 23673.98 ❌
- **TP 15RR**: 23770.69 ❌
- **PnL**: -8.79 points (-1.0R)
- **MFE**: 2.78 points
- **MAE**: 9.09 points

### Trade #1389 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 19:30:00
- **FVG 5m**: 23628.22 - 23653.46
- **Entrée**: 23611.80 @ 2025-08-25 19:42:00
- **Stop Loss**: 23720.86
- **Risk**: 109.06 points
- **TP 1RR**: 23502.75 ❌
- **TP 2RR**: 23393.69 ❌
- **TP 3RR**: 23284.63 ❌
- **TP 4RR**: 23175.57 ❌
- **TP 15RR**: 21975.94 ❌
- **PnL**: -109.06 points (-1.0R)
- **MFE**: 8.84 points
- **MAE**: 109.57 points

### Trade #1390 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-25 19:30:00
- **FVG 5m**: 23628.22 - 23653.46
- **Entrée**: 23611.80 @ 2025-08-25 19:42:00
- **Stop Loss**: 23720.86
- **Risk**: 109.06 points
- **TP 1RR**: 23502.75 ❌
- **TP 2RR**: 23393.69 ❌
- **TP 3RR**: 23284.63 ❌
- **TP 4RR**: 23175.57 ❌
- **TP 15RR**: 21975.94 ❌
- **PnL**: -109.06 points (-1.0R)
- **MFE**: 8.84 points
- **MAE**: 109.57 points

### Trade #1391 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-26 08:30:00
- **FVG 5m**: 23748.90 - 23752.69
- **Entrée**: 23747.13 @ 2025-08-26 10:28:00
- **Stop Loss**: 23763.30
- **Risk**: 16.17 points
- **TP 1RR**: 23730.96 ✅
- **TP 2RR**: 23714.80 ❌
- **TP 3RR**: 23698.63 ❌
- **TP 4RR**: 23682.46 ❌
- **TP 15RR**: 23504.61 ❌
- **PnL**: -16.17 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 18.68 points

### Trade #1392 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-26 08:45:00
- **FVG 5m**: 23761.52 - 23768.09
- **Entrée**: 23775.16 @ 2025-08-26 09:22:00
- **Stop Loss**: 23647.19
- **Risk**: 127.97 points
- **TP 1RR**: 23903.13 ✅
- **TP 2RR**: 24031.09 ✅
- **TP 3RR**: 24159.06 ❌
- **TP 4RR**: 24287.03 ❌
- **TP 15RR**: 25694.68 ❌
- **PnL**: -127.97 points (-1.0R)
- **MFE**: 264.34 points
- **MAE**: 128.01 points

### Trade #1393 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-26 10:15:00
- **FVG 5m**: 23748.90 - 23752.69
- **Entrée**: 23747.13 @ 2025-08-26 10:28:00
- **Stop Loss**: 23782.50
- **Risk**: 35.37 points
- **TP 1RR**: 23711.77 ❌
- **TP 2RR**: 23676.40 ❌
- **TP 3RR**: 23641.04 ❌
- **TP 4RR**: 23605.67 ❌
- **TP 15RR**: 23216.65 ❌
- **PnL**: -35.37 points (-1.0R)
- **MFE**: 21.21 points
- **MAE**: 36.36 points

### Trade #1394 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-26 12:45:00
- **FVG 5m**: 23752.69 - 23755.72
- **Entrée**: 23756.98 @ 2025-08-26 13:11:00
- **Stop Loss**: 23699.68
- **Risk**: 57.30 points
- **TP 1RR**: 23814.28 ✅
- **TP 2RR**: 23871.58 ✅
- **TP 3RR**: 23928.88 ❌
- **TP 4RR**: 23986.18 ❌
- **TP 15RR**: 24616.50 ❌
- **PnL**: -57.30 points (-1.0R)
- **MFE**: 166.63 points
- **MAE**: 86.85 points

### Trade #1395 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-26 21:15:00
- **FVG 5m**: 23850.90 - 23853.93
- **Entrée**: 23849.13 @ 2025-08-26 21:29:00
- **Stop Loss**: 23874.44
- **Risk**: 25.31 points
- **TP 1RR**: 23823.82 ✅
- **TP 2RR**: 23798.51 ✅
- **TP 3RR**: 23773.19 ✅
- **TP 4RR**: 23747.88 ✅
- **TP 15RR**: 23469.44 ❌
- **PnL**: -25.31 points (-1.0R)
- **MFE**: 129.02 points
- **MAE**: 26.76 points

### Trade #1396 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 07:15:00
- **FVG 5m**: 23831.71 - 23844.08
- **Entrée**: 23830.70 @ 2025-08-27 07:28:00
- **Stop Loss**: 23866.87
- **Risk**: 36.17 points
- **TP 1RR**: 23794.54 ✅
- **TP 2RR**: 23758.37 ✅
- **TP 3RR**: 23722.21 ✅
- **TP 4RR**: 23686.04 ❌
- **TP 15RR**: 23288.22 ❌
- **PnL**: -36.17 points (-1.0R)
- **MFE**: 110.58 points
- **MAE**: 37.11 points

### Trade #1397 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 09:15:00
- **FVG 5m**: 23839.79 - 23848.88
- **Entrée**: 23849.64 @ 2025-08-27 10:47:00
- **Stop Loss**: 23786.99
- **Risk**: 62.65 points
- **TP 1RR**: 23912.28 ❌
- **TP 2RR**: 23974.93 ❌
- **TP 3RR**: 24037.58 ❌
- **TP 4RR**: 24100.23 ❌
- **TP 15RR**: 24789.34 ❌
- **PnL**: -62.65 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 67.16 points

### Trade #1398 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 09:15:00
- **FVG 5m**: 23839.79 - 23848.88
- **Entrée**: 23849.64 @ 2025-08-27 10:47:00
- **Stop Loss**: 23786.99
- **Risk**: 62.65 points
- **TP 1RR**: 23912.28 ❌
- **TP 2RR**: 23974.93 ❌
- **TP 3RR**: 24037.58 ❌
- **TP 4RR**: 24100.23 ❌
- **TP 15RR**: 24789.34 ❌
- **PnL**: -62.65 points (-1.0R)
- **MFE**: 15.15 points
- **MAE**: 67.16 points

### Trade #1399 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 10:45:00
- **FVG 5m**: 23812.52 - 23827.17
- **Entrée**: 23828.93 @ 2025-08-27 11:49:00
- **Stop Loss**: 23818.53
- **Risk**: 10.40 points
- **TP 1RR**: 23839.33 ✅
- **TP 2RR**: 23849.73 ✅
- **TP 3RR**: 23860.14 ✅
- **TP 4RR**: 23870.54 ✅
- **TP 15RR**: 23984.94 ❌
- **PnL**: -10.40 points (-1.0R)
- **MFE**: 62.87 points
- **MAE**: 32.57 points

### Trade #1400 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 11:30:00
- **FVG 5m**: 23812.52 - 23827.17
- **Entrée**: 23828.93 @ 2025-08-27 11:49:00
- **Stop Loss**: 23763.27
- **Risk**: 65.66 points
- **TP 1RR**: 23894.60 ✅
- **TP 2RR**: 23960.26 ❌
- **TP 3RR**: 24025.93 ❌
- **TP 4RR**: 24091.59 ❌
- **TP 15RR**: 24813.91 ❌
- **PnL**: -65.66 points (-1.0R)
- **MFE**: 94.68 points
- **MAE**: 158.81 points

### Trade #1401 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 13:45:00
- **FVG 5m**: 23853.42 - 23858.22
- **Entrée**: 23851.40 @ 2025-08-27 14:04:00
- **Stop Loss**: 23891.62
- **Risk**: 40.22 points
- **TP 1RR**: 23811.19 ✅
- **TP 2RR**: 23770.97 ❌
- **TP 3RR**: 23730.75 ❌
- **TP 4RR**: 23690.54 ❌
- **TP 15RR**: 23248.15 ❌
- **PnL**: -40.22 points (-1.0R)
- **MFE**: 64.63 points
- **MAE**: 72.21 points

### Trade #1402 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 13:45:00
- **FVG 5m**: 23853.42 - 23858.22
- **Entrée**: 23851.40 @ 2025-08-27 14:04:00
- **Stop Loss**: 23891.62
- **Risk**: 40.22 points
- **TP 1RR**: 23811.19 ✅
- **TP 2RR**: 23770.97 ❌
- **TP 3RR**: 23730.75 ❌
- **TP 4RR**: 23690.54 ❌
- **TP 15RR**: 23248.15 ❌
- **PnL**: -40.22 points (-1.0R)
- **MFE**: 64.63 points
- **MAE**: 72.21 points

### Trade #1403 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23892.88
- **Risk**: 84.40 points
- **TP 1RR**: 23724.08 ✅
- **TP 2RR**: 23639.68 ❌
- **TP 3RR**: 23555.28 ❌
- **TP 4RR**: 23470.88 ❌
- **TP 15RR**: 22542.47 ❌
- **PnL**: -84.40 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 84.58 points

### Trade #1404 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23892.88
- **Risk**: 84.40 points
- **TP 1RR**: 23724.08 ✅
- **TP 2RR**: 23639.68 ❌
- **TP 3RR**: 23555.28 ❌
- **TP 4RR**: 23470.88 ❌
- **TP 15RR**: 22542.47 ❌
- **PnL**: -84.40 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 84.58 points

### Trade #1405 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23892.88
- **Risk**: 84.40 points
- **TP 1RR**: 23724.08 ✅
- **TP 2RR**: 23639.68 ❌
- **TP 3RR**: 23555.28 ❌
- **TP 4RR**: 23470.88 ❌
- **TP 15RR**: 22542.47 ❌
- **PnL**: -84.40 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 84.58 points

### Trade #1406 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23892.88
- **Risk**: 84.40 points
- **TP 1RR**: 23724.08 ✅
- **TP 2RR**: 23639.68 ❌
- **TP 3RR**: 23555.28 ❌
- **TP 4RR**: 23470.88 ❌
- **TP 15RR**: 22542.47 ❌
- **PnL**: -84.40 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 84.58 points

### Trade #1407 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 14:45:00
- **FVG 5m**: 23812.52 - 23848.88
- **Entrée**: 23808.48 @ 2025-08-27 15:29:00
- **Stop Loss**: 23892.88
- **Risk**: 84.40 points
- **TP 1RR**: 23724.08 ✅
- **TP 2RR**: 23639.68 ❌
- **TP 3RR**: 23555.28 ❌
- **TP 4RR**: 23470.88 ❌
- **TP 15RR**: 22542.47 ❌
- **PnL**: -84.40 points (-1.0R)
- **MFE**: 88.37 points
- **MAE**: 84.58 points

### Trade #1408 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23753.44 - 23764.05
- **Entrée**: 23751.42 @ 2025-08-27 17:02:00
- **Stop Loss**: 23935.57
- **Risk**: 184.15 points
- **TP 1RR**: 23567.27 ❌
- **TP 2RR**: 23383.12 ❌
- **TP 3RR**: 23198.97 ❌
- **TP 4RR**: 23014.82 ❌
- **TP 15RR**: 20989.17 ❌
- **PnL**: -184.15 points (-1.0R)
- **MFE**: 31.31 points
- **MAE**: 189.36 points

### Trade #1409 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23753.44 - 23764.05
- **Entrée**: 23751.42 @ 2025-08-27 17:02:00
- **Stop Loss**: 23935.57
- **Risk**: 184.15 points
- **TP 1RR**: 23567.27 ❌
- **TP 2RR**: 23383.12 ❌
- **TP 3RR**: 23198.97 ❌
- **TP 4RR**: 23014.82 ❌
- **TP 15RR**: 20989.17 ❌
- **PnL**: -184.15 points (-1.0R)
- **MFE**: 31.31 points
- **MAE**: 189.36 points

### Trade #1410 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23753.44 - 23764.05
- **Entrée**: 23751.42 @ 2025-08-27 17:02:00
- **Stop Loss**: 23935.57
- **Risk**: 184.15 points
- **TP 1RR**: 23567.27 ❌
- **TP 2RR**: 23383.12 ❌
- **TP 3RR**: 23198.97 ❌
- **TP 4RR**: 23014.82 ❌
- **TP 15RR**: 20989.17 ❌
- **PnL**: -184.15 points (-1.0R)
- **MFE**: 31.31 points
- **MAE**: 189.36 points

### Trade #1411 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23744.86 - 23759.25
- **Entrée**: 23763.80 @ 2025-08-27 17:34:00
- **Stop Loss**: 23655.01
- **Risk**: 108.78 points
- **TP 1RR**: 23872.58 ✅
- **TP 2RR**: 23981.36 ✅
- **TP 3RR**: 24090.15 ❌
- **TP 4RR**: 24198.93 ❌
- **TP 15RR**: 25395.56 ❌
- **PnL**: -108.78 points (-1.0R)
- **MFE**: 275.70 points
- **MAE**: 111.59 points

### Trade #1412 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23744.86 - 23759.25
- **Entrée**: 23763.80 @ 2025-08-27 17:34:00
- **Stop Loss**: 23655.01
- **Risk**: 108.78 points
- **TP 1RR**: 23872.58 ✅
- **TP 2RR**: 23981.36 ✅
- **TP 3RR**: 24090.15 ❌
- **TP 4RR**: 24198.93 ❌
- **TP 15RR**: 25395.56 ❌
- **PnL**: -108.78 points (-1.0R)
- **MFE**: 275.70 points
- **MAE**: 111.59 points

### Trade #1413 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-27 15:15:00
- **FVG 5m**: 23744.86 - 23759.25
- **Entrée**: 23763.80 @ 2025-08-27 17:34:00
- **Stop Loss**: 23655.01
- **Risk**: 108.78 points
- **TP 1RR**: 23872.58 ✅
- **TP 2RR**: 23981.36 ✅
- **TP 3RR**: 24090.15 ❌
- **TP 4RR**: 24198.93 ❌
- **TP 15RR**: 25395.56 ❌
- **PnL**: -108.78 points (-1.0R)
- **MFE**: 275.70 points
- **MAE**: 111.59 points

### Trade #1414 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 08:45:00
- **FVG 5m**: 23942.04 - 23958.96
- **Entrée**: 23933.96 @ 2025-08-28 10:23:00
- **Stop Loss**: 23955.78
- **Risk**: 21.82 points
- **TP 1RR**: 23912.15 ✅
- **TP 2RR**: 23890.33 ❌
- **TP 3RR**: 23868.51 ❌
- **TP 4RR**: 23846.69 ❌
- **TP 15RR**: 23606.69 ❌
- **PnL**: -21.82 points (-1.0R)
- **MFE**: 34.59 points
- **MAE**: 30.04 points

### Trade #1415 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 08:45:00
- **FVG 5m**: 23942.04 - 23958.96
- **Entrée**: 23933.96 @ 2025-08-28 10:23:00
- **Stop Loss**: 23955.78
- **Risk**: 21.82 points
- **TP 1RR**: 23912.15 ✅
- **TP 2RR**: 23890.33 ❌
- **TP 3RR**: 23868.51 ❌
- **TP 4RR**: 23846.69 ❌
- **TP 15RR**: 23606.69 ❌
- **PnL**: -21.82 points (-1.0R)
- **MFE**: 34.59 points
- **MAE**: 30.04 points

### Trade #1416 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 10:00:00
- **FVG 5m**: 23951.13 - 23958.96
- **Entrée**: 23959.46 @ 2025-08-28 10:11:00
- **Stop Loss**: 23919.22
- **Risk**: 40.24 points
- **TP 1RR**: 23999.71 ❌
- **TP 2RR**: 24039.95 ❌
- **TP 3RR**: 24080.19 ❌
- **TP 4RR**: 24120.44 ❌
- **TP 15RR**: 24563.11 ❌
- **PnL**: -40.24 points (-1.0R)
- **MFE**: 28.53 points
- **MAE**: 43.68 points

### Trade #1417 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 10:00:00
- **FVG 5m**: 23951.13 - 23958.96
- **Entrée**: 23959.46 @ 2025-08-28 10:11:00
- **Stop Loss**: 23919.22
- **Risk**: 40.24 points
- **TP 1RR**: 23999.71 ❌
- **TP 2RR**: 24039.95 ❌
- **TP 3RR**: 24080.19 ❌
- **TP 4RR**: 24120.44 ❌
- **TP 15RR**: 24563.11 ❌
- **PnL**: -40.24 points (-1.0R)
- **MFE**: 28.53 points
- **MAE**: 43.68 points

### Trade #1418 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 11:15:00
- **FVG 5m**: 23979.66 - 23982.94
- **Entrée**: 23986.23 @ 2025-08-28 11:47:00
- **Stop Loss**: 23939.16
- **Risk**: 47.07 points
- **TP 1RR**: 24033.30 ✅
- **TP 2RR**: 24080.37 ❌
- **TP 3RR**: 24127.44 ❌
- **TP 4RR**: 24174.51 ❌
- **TP 15RR**: 24692.27 ❌
- **PnL**: -47.07 points (-1.0R)
- **MFE**: 53.27 points
- **MAE**: 48.48 points

### Trade #1419 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 11:15:00
- **FVG 5m**: 23979.66 - 23982.94
- **Entrée**: 23986.23 @ 2025-08-28 11:47:00
- **Stop Loss**: 23939.16
- **Risk**: 47.07 points
- **TP 1RR**: 24033.30 ✅
- **TP 2RR**: 24080.37 ❌
- **TP 3RR**: 24127.44 ❌
- **TP 4RR**: 24174.51 ❌
- **TP 15RR**: 24692.27 ❌
- **PnL**: -47.07 points (-1.0R)
- **MFE**: 53.27 points
- **MAE**: 48.48 points

### Trade #1420 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-28 11:15:00
- **FVG 5m**: 23979.66 - 23982.94
- **Entrée**: 23986.23 @ 2025-08-28 11:47:00
- **Stop Loss**: 23939.16
- **Risk**: 47.07 points
- **TP 1RR**: 24033.30 ✅
- **TP 2RR**: 24080.37 ❌
- **TP 3RR**: 24127.44 ❌
- **TP 4RR**: 24174.51 ❌
- **TP 15RR**: 24692.27 ❌
- **PnL**: -47.07 points (-1.0R)
- **MFE**: 53.27 points
- **MAE**: 48.48 points

### Trade #1421 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 11:45:00
- **FVG 5m**: 23976.13 - 23982.94
- **Entrée**: 23973.86 @ 2025-08-28 11:57:00
- **Stop Loss**: 24008.83
- **Risk**: 34.97 points
- **TP 1RR**: 23938.88 ❌
- **TP 2RR**: 23903.91 ❌
- **TP 3RR**: 23868.93 ❌
- **TP 4RR**: 23833.96 ❌
- **TP 15RR**: 23449.25 ❌
- **PnL**: -34.97 points (-1.0R)
- **MFE**: 16.66 points
- **MAE**: 35.85 points

### Trade #1422 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 14:00:00
- **FVG 5m**: 24009.45 - 24015.77
- **Entrée**: 24002.13 @ 2025-08-28 14:59:00
- **Stop Loss**: 24047.73
- **Risk**: 45.60 points
- **TP 1RR**: 23956.54 ✅
- **TP 2RR**: 23910.94 ✅
- **TP 3RR**: 23865.34 ✅
- **TP 4RR**: 23819.74 ✅
- **TP 15RR**: 23318.18 ✅
- **PnL**: 683.96 points (15.0R)
- **MFE**: 713.50 points
- **MAE**: 7.32 points

### Trade #1423 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-28 14:45:00
- **FVG 5m**: 24009.45 - 24015.77
- **Entrée**: 24002.13 @ 2025-08-28 14:59:00
- **Stop Loss**: 24051.52
- **Risk**: 49.39 points
- **TP 1RR**: 23952.75 ✅
- **TP 2RR**: 23903.36 ✅
- **TP 3RR**: 23853.97 ✅
- **TP 4RR**: 23804.59 ✅
- **TP 15RR**: 23261.34 ✅
- **PnL**: 740.79 points (15.0R)
- **MFE**: 748.84 points
- **MAE**: 7.32 points

### Trade #1424 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-29 08:45:00
- **FVG 5m**: 23723.65 - 23740.06
- **Entrée**: 23714.06 @ 2025-08-29 09:04:00
- **Stop Loss**: 23846.66
- **Risk**: 132.60 points
- **TP 1RR**: 23581.46 ✅
- **TP 2RR**: 23448.86 ✅
- **TP 3RR**: 23316.25 ✅
- **TP 4RR**: 23183.65 ❌
- **TP 15RR**: 21725.04 ❌
- **PnL**: -132.60 points (-1.0R)
- **MFE**: 460.77 points
- **MAE**: 133.56 points

### Trade #1425 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-29 09:00:00
- **FVG 5m**: 23685.28 - 23702.44
- **Entrée**: 23681.99 @ 2025-08-29 09:49:00
- **Stop Loss**: 23796.39
- **Risk**: 114.40 points
- **TP 1RR**: 23567.60 ✅
- **TP 2RR**: 23453.20 ✅
- **TP 3RR**: 23338.80 ✅
- **TP 4RR**: 23224.40 ❌
- **TP 15RR**: 21966.03 ❌
- **PnL**: -114.40 points (-1.0R)
- **MFE**: 428.70 points
- **MAE**: 115.38 points

### Trade #1426 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-29 09:00:00
- **FVG 5m**: 23685.28 - 23702.44
- **Entrée**: 23681.99 @ 2025-08-29 09:49:00
- **Stop Loss**: 23796.39
- **Risk**: 114.40 points
- **TP 1RR**: 23567.60 ✅
- **TP 2RR**: 23453.20 ✅
- **TP 3RR**: 23338.80 ✅
- **TP 4RR**: 23224.40 ❌
- **TP 15RR**: 21966.03 ❌
- **PnL**: -114.40 points (-1.0R)
- **MFE**: 428.70 points
- **MAE**: 115.38 points

### Trade #1427 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 09:15:00
- **FVG 5m**: 23689.57 - 23697.14
- **Entrée**: 23697.39 @ 2025-08-29 10:07:00
- **Stop Loss**: 23648.20
- **Risk**: 49.20 points
- **TP 1RR**: 23746.59 ❌
- **TP 2RR**: 23795.79 ❌
- **TP 3RR**: 23844.98 ❌
- **TP 4RR**: 23894.18 ❌
- **TP 15RR**: 24435.34 ❌
- **PnL**: -49.20 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 49.99 points

### Trade #1428 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 09:45:00
- **FVG 5m**: 23689.57 - 23697.14
- **Entrée**: 23697.39 @ 2025-08-29 10:07:00
- **Stop Loss**: 23635.33
- **Risk**: 62.07 points
- **TP 1RR**: 23759.46 ❌
- **TP 2RR**: 23821.53 ❌
- **TP 3RR**: 23883.59 ❌
- **TP 4RR**: 23945.66 ❌
- **TP 15RR**: 24628.39 ❌
- **PnL**: -62.07 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 63.62 points

### Trade #1429 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 09:45:00
- **FVG 5m**: 23689.57 - 23697.14
- **Entrée**: 23697.39 @ 2025-08-29 10:07:00
- **Stop Loss**: 23635.33
- **Risk**: 62.07 points
- **TP 1RR**: 23759.46 ❌
- **TP 2RR**: 23821.53 ❌
- **TP 3RR**: 23883.59 ❌
- **TP 4RR**: 23945.66 ❌
- **TP 15RR**: 24628.39 ❌
- **PnL**: -62.07 points (-1.0R)
- **MFE**: 34.08 points
- **MAE**: 63.62 points

### Trade #1430 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 12:15:00
- **FVG 5m**: 23669.37 - 23672.65
- **Entrée**: 23673.66 @ 2025-08-29 12:44:00
- **Stop Loss**: 23617.41
- **Risk**: 56.25 points
- **TP 1RR**: 23729.91 ✅
- **TP 2RR**: 23786.16 ❌
- **TP 3RR**: 23842.41 ❌
- **TP 4RR**: 23898.66 ❌
- **TP 15RR**: 24517.42 ❌
- **PnL**: -56.25 points (-1.0R)
- **MFE**: 112.10 points
- **MAE**: 59.58 points

### Trade #1431 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-08-29 12:15:00
- **FVG 5m**: 23669.37 - 23672.65
- **Entrée**: 23673.66 @ 2025-08-29 12:44:00
- **Stop Loss**: 23617.41
- **Risk**: 56.25 points
- **TP 1RR**: 23729.91 ✅
- **TP 2RR**: 23786.16 ❌
- **TP 3RR**: 23842.41 ❌
- **TP 4RR**: 23898.66 ❌
- **TP 15RR**: 24517.42 ❌
- **PnL**: -56.25 points (-1.0R)
- **MFE**: 112.10 points
- **MAE**: 59.58 points

### Trade #1432 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-08-31 21:00:00
- **FVG 5m**: 23722.39 - 23735.52
- **Entrée**: 23720.87 @ 2025-08-31 21:13:00
- **Stop Loss**: 23763.30
- **Risk**: 42.43 points
- **TP 1RR**: 23678.45 ✅
- **TP 2RR**: 23636.02 ✅
- **TP 3RR**: 23593.60 ✅
- **TP 4RR**: 23551.17 ✅
- **TP 15RR**: 23084.49 ❌
- **PnL**: -42.43 points (-1.0R)
- **MFE**: 467.59 points
- **MAE**: 44.18 points

### Trade #1433 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 00:15:00
- **FVG 5m**: 23631.75 - 23652.20
- **Entrée**: 23656.24 @ 2025-09-01 01:39:00
- **Stop Loss**: 23634.07
- **Risk**: 22.17 points
- **TP 1RR**: 23678.42 ✅
- **TP 2RR**: 23700.59 ✅
- **TP 3RR**: 23722.76 ✅
- **TP 4RR**: 23744.94 ❌
- **TP 15RR**: 23988.86 ❌
- **PnL**: -22.17 points (-1.0R)
- **MFE**: 86.09 points
- **MAE**: 23.99 points

### Trade #1434 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 01:30:00
- **FVG 5m**: 23656.75 - 23677.45
- **Entrée**: 23680.98 @ 2025-09-01 01:43:00
- **Stop Loss**: 23595.46
- **Risk**: 85.53 points
- **TP 1RR**: 23766.51 ❌
- **TP 2RR**: 23852.04 ❌
- **TP 3RR**: 23937.56 ❌
- **TP 4RR**: 24023.09 ❌
- **TP 15RR**: 24963.88 ❌
- **PnL**: -85.53 points (-1.0R)
- **MFE**: 61.35 points
- **MAE**: 94.93 points

### Trade #1435 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 01:30:00
- **FVG 5m**: 23656.75 - 23677.45
- **Entrée**: 23680.98 @ 2025-09-01 01:43:00
- **Stop Loss**: 23595.46
- **Risk**: 85.53 points
- **TP 1RR**: 23766.51 ❌
- **TP 2RR**: 23852.04 ❌
- **TP 3RR**: 23937.56 ❌
- **TP 4RR**: 24023.09 ❌
- **TP 15RR**: 24963.88 ❌
- **PnL**: -85.53 points (-1.0R)
- **MFE**: 61.35 points
- **MAE**: 94.93 points

### Trade #1436 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-01 08:30:00
- **FVG 5m**: 23724.16 - 23727.44
- **Entrée**: 23728.20 @ 2025-09-01 10:19:00
- **Stop Loss**: 23662.08
- **Risk**: 66.12 points
- **TP 1RR**: 23794.32 ❌
- **TP 2RR**: 23860.43 ❌
- **TP 3RR**: 23926.55 ❌
- **TP 4RR**: 23992.67 ❌
- **TP 15RR**: 24719.99 ❌
- **PnL**: -66.12 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 67.92 points

### Trade #1437 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:30:00
- **FVG 5m**: 23594.89 - 23603.47
- **Entrée**: 23589.33 @ 2025-09-02 02:42:00
- **Stop Loss**: 23666.30
- **Risk**: 76.97 points
- **TP 1RR**: 23512.37 ✅
- **TP 2RR**: 23435.40 ✅
- **TP 3RR**: 23358.44 ✅
- **TP 4RR**: 23281.47 ✅
- **TP 15RR**: 22434.84 ❌
- **PnL**: -76.97 points (-1.0R)
- **MFE**: 336.05 points
- **MAE**: 77.76 points

### Trade #1438 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:30:00
- **FVG 5m**: 23594.89 - 23603.47
- **Entrée**: 23589.33 @ 2025-09-02 02:42:00
- **Stop Loss**: 23666.30
- **Risk**: 76.97 points
- **TP 1RR**: 23512.37 ✅
- **TP 2RR**: 23435.40 ✅
- **TP 3RR**: 23358.44 ✅
- **TP 4RR**: 23281.47 ✅
- **TP 15RR**: 22434.84 ❌
- **PnL**: -76.97 points (-1.0R)
- **MFE**: 336.05 points
- **MAE**: 77.76 points

### Trade #1439 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:30:00
- **FVG 5m**: 23594.89 - 23603.47
- **Entrée**: 23589.33 @ 2025-09-02 02:42:00
- **Stop Loss**: 23666.30
- **Risk**: 76.97 points
- **TP 1RR**: 23512.37 ✅
- **TP 2RR**: 23435.40 ✅
- **TP 3RR**: 23358.44 ✅
- **TP 4RR**: 23281.47 ✅
- **TP 15RR**: 22434.84 ❌
- **PnL**: -76.97 points (-1.0R)
- **MFE**: 336.05 points
- **MAE**: 77.76 points

### Trade #1440 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:45:00
- **FVG 5m**: 23548.94 - 23552.22
- **Entrée**: 23548.18 @ 2025-09-02 04:44:00
- **Stop Loss**: 23606.69
- **Risk**: 58.51 points
- **TP 1RR**: 23489.68 ✅
- **TP 2RR**: 23431.17 ✅
- **TP 3RR**: 23372.66 ✅
- **TP 4RR**: 23314.16 ✅
- **TP 15RR**: 22670.60 ❌
- **PnL**: -58.51 points (-1.0R)
- **MFE**: 294.89 points
- **MAE**: 66.65 points

### Trade #1441 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 02:45:00
- **FVG 5m**: 23548.94 - 23552.22
- **Entrée**: 23548.18 @ 2025-09-02 04:44:00
- **Stop Loss**: 23606.69
- **Risk**: 58.51 points
- **TP 1RR**: 23489.68 ✅
- **TP 2RR**: 23431.17 ✅
- **TP 3RR**: 23372.66 ✅
- **TP 4RR**: 23314.16 ✅
- **TP 15RR**: 22670.60 ❌
- **PnL**: -58.51 points (-1.0R)
- **MFE**: 294.89 points
- **MAE**: 66.65 points

### Trade #1442 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 05:15:00
- **FVG 5m**: 23493.65 - 23496.17
- **Entrée**: 23480.52 @ 2025-09-02 05:28:00
- **Stop Loss**: 23544.29
- **Risk**: 63.78 points
- **TP 1RR**: 23416.74 ✅
- **TP 2RR**: 23352.96 ✅
- **TP 3RR**: 23289.19 ✅
- **TP 4RR**: 23225.41 ❌
- **TP 15RR**: 22523.87 ❌
- **PnL**: -63.78 points (-1.0R)
- **MFE**: 227.23 points
- **MAE**: 69.68 points

### Trade #1443 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 06:45:00
- **FVG 5m**: 23429.26 - 23453.00
- **Entrée**: 23424.47 @ 2025-09-02 07:02:00
- **Stop Loss**: 23487.96
- **Risk**: 63.50 points
- **TP 1RR**: 23360.97 ✅
- **TP 2RR**: 23297.48 ✅
- **TP 3RR**: 23233.98 ❌
- **TP 4RR**: 23170.48 ❌
- **TP 15RR**: 22472.03 ❌
- **PnL**: -63.50 points (-1.0R)
- **MFE**: 171.18 points
- **MAE**: 66.65 points

### Trade #1444 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 07:45:00
- **FVG 5m**: 23331.30 - 23356.05
- **Entrée**: 23367.91 @ 2025-09-02 08:36:00
- **Stop Loss**: 23276.99
- **Risk**: 90.92 points
- **TP 1RR**: 23458.83 ✅
- **TP 2RR**: 23549.76 ❌
- **TP 3RR**: 23640.68 ❌
- **TP 4RR**: 23731.60 ❌
- **TP 15RR**: 24731.74 ❌
- **PnL**: -90.92 points (-1.0R)
- **MFE**: 142.65 points
- **MAE**: 91.90 points

### Trade #1445 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 08:30:00
- **FVG 5m**: 23407.30 - 23420.18
- **Entrée**: 23424.47 @ 2025-09-02 08:48:00
- **Stop Loss**: 23241.66
- **Risk**: 182.81 points
- **TP 1RR**: 23607.27 ✅
- **TP 2RR**: 23790.08 ✅
- **TP 3RR**: 23972.88 ✅
- **TP 4RR**: 24155.69 ✅
- **TP 15RR**: 26166.55 ✅
- **PnL**: 2742.08 points (15.0R)
- **MFE**: 2747.53 points
- **MAE**: 169.41 points

### Trade #1446 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 09:00:00
- **FVG 5m**: 23417.65 - 23447.19
- **Entrée**: 23416.64 @ 2025-09-02 09:42:00
- **Stop Loss**: 23522.32
- **Risk**: 105.68 points
- **TP 1RR**: 23310.96 ✅
- **TP 2RR**: 23205.29 ❌
- **TP 3RR**: 23099.61 ❌
- **TP 4RR**: 22993.94 ❌
- **TP 15RR**: 21831.50 ❌
- **PnL**: -105.68 points (-1.0R)
- **MFE**: 161.58 points
- **MAE**: 133.56 points

### Trade #1447 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-02 09:00:00
- **FVG 5m**: 23417.65 - 23447.19
- **Entrée**: 23416.64 @ 2025-09-02 09:42:00
- **Stop Loss**: 23522.32
- **Risk**: 105.68 points
- **TP 1RR**: 23310.96 ✅
- **TP 2RR**: 23205.29 ❌
- **TP 3RR**: 23099.61 ❌
- **TP 4RR**: 22993.94 ❌
- **TP 15RR**: 21831.50 ❌
- **PnL**: -105.68 points (-1.0R)
- **MFE**: 161.58 points
- **MAE**: 133.56 points

### Trade #1448 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 14:45:00
- **FVG 5m**: 23518.39 - 23568.38
- **Entrée**: 23595.39 @ 2025-09-02 15:09:00
- **Stop Loss**: 23453.64
- **Risk**: 141.76 points
- **TP 1RR**: 23737.15 ✅
- **TP 2RR**: 23878.91 ✅
- **TP 3RR**: 24020.67 ✅
- **TP 4RR**: 24162.43 ✅
- **TP 15RR**: 25721.76 ✅
- **PnL**: 2126.37 points (15.0R)
- **MFE**: 2172.86 points
- **MAE**: 66.40 points

### Trade #1449 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-02 22:30:00
- **FVG 5m**: 23557.52 - 23560.30
- **Entrée**: 23560.55 @ 2025-09-02 23:17:00
- **Stop Loss**: 23517.23
- **Risk**: 43.32 points
- **TP 1RR**: 23603.88 ✅
- **TP 2RR**: 23647.20 ✅
- **TP 3RR**: 23690.52 ✅
- **TP 4RR**: 23733.85 ✅
- **TP 15RR**: 24210.41 ✅
- **PnL**: 649.86 points (15.0R)
- **MFE**: 721.83 points
- **MAE**: 21.71 points

### Trade #1450 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-03 03:45:00
- **FVG 5m**: 23639.83 - 23645.64
- **Entrée**: 23647.66 @ 2025-09-03 04:18:00
- **Stop Loss**: 23622.96
- **Risk**: 24.69 points
- **TP 1RR**: 23672.35 ✅
- **TP 2RR**: 23697.04 ❌
- **TP 3RR**: 23721.74 ❌
- **TP 4RR**: 23746.43 ❌
- **TP 15RR**: 24018.06 ❌
- **PnL**: -24.69 points (-1.0R)
- **MFE**: 43.17 points
- **MAE**: 36.86 points

### Trade #1451 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-03 06:30:00
- **FVG 5m**: 23667.10 - 23670.63
- **Entrée**: 23674.67 @ 2025-09-03 08:06:00
- **Stop Loss**: 23628.26
- **Risk**: 46.41 points
- **TP 1RR**: 23721.08 ❌
- **TP 2RR**: 23767.49 ❌
- **TP 3RR**: 23813.90 ❌
- **TP 4RR**: 23860.31 ❌
- **TP 15RR**: 24370.81 ❌
- **PnL**: -46.41 points (-1.0R)
- **MFE**: 14.64 points
- **MAE**: 63.88 points

### Trade #1452 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:15:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23716.57
- **Risk**: 13.62 points
- **TP 1RR**: 23689.33 ✅
- **TP 2RR**: 23675.71 ✅
- **TP 3RR**: 23662.09 ✅
- **TP 4RR**: 23648.47 ✅
- **TP 15RR**: 23498.65 ❌
- **PnL**: -13.62 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1453 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:15:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23716.57
- **Risk**: 13.62 points
- **TP 1RR**: 23689.33 ✅
- **TP 2RR**: 23675.71 ✅
- **TP 3RR**: 23662.09 ✅
- **TP 4RR**: 23648.47 ✅
- **TP 15RR**: 23498.65 ❌
- **PnL**: -13.62 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1454 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:15:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23716.57
- **Risk**: 13.62 points
- **TP 1RR**: 23689.33 ✅
- **TP 2RR**: 23675.71 ✅
- **TP 3RR**: 23662.09 ✅
- **TP 4RR**: 23648.47 ✅
- **TP 15RR**: 23498.65 ❌
- **PnL**: -13.62 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 29.54 points

### Trade #1455 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 09:45:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23770.12
- **Risk**: 67.17 points
- **TP 1RR**: 23635.78 ✅
- **TP 2RR**: 23568.61 ✅
- **TP 3RR**: 23501.43 ❌
- **TP 4RR**: 23434.26 ❌
- **TP 15RR**: 22695.38 ❌
- **PnL**: -67.17 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 68.17 points

### Trade #1456 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 10:00:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23761.28
- **Risk**: 58.33 points
- **TP 1RR**: 23644.62 ✅
- **TP 2RR**: 23586.29 ✅
- **TP 3RR**: 23527.96 ❌
- **TP 4RR**: 23469.63 ❌
- **TP 15RR**: 22827.99 ❌
- **PnL**: -58.33 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 62.11 points

### Trade #1457 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 10:00:00
- **FVG 5m**: 23703.45 - 23708.00
- **Entrée**: 23702.95 @ 2025-09-03 10:21:00
- **Stop Loss**: 23761.28
- **Risk**: 58.33 points
- **TP 1RR**: 23644.62 ✅
- **TP 2RR**: 23586.29 ✅
- **TP 3RR**: 23527.96 ❌
- **TP 4RR**: 23469.63 ❌
- **TP 15RR**: 22827.99 ❌
- **PnL**: -58.33 points (-1.0R)
- **MFE**: 153.76 points
- **MAE**: 62.11 points

### Trade #1458 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-03 14:30:00
- **FVG 5m**: 23616.60 - 23622.66
- **Entrée**: 23628.47 @ 2025-09-03 14:44:00
- **Stop Loss**: 23571.99
- **Risk**: 56.48 points
- **TP 1RR**: 23684.95 ✅
- **TP 2RR**: 23741.43 ✅
- **TP 3RR**: 23797.91 ✅
- **TP 4RR**: 23854.39 ✅
- **TP 15RR**: 24475.67 ✅
- **PnL**: 847.20 points (15.0R)
- **MFE**: 853.03 points
- **MAE**: 5.81 points

### Trade #1459 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 21:15:00
- **FVG 5m**: 23734.26 - 23745.87
- **Entrée**: 23730.97 @ 2025-09-03 21:29:00
- **Stop Loss**: 23768.35
- **Risk**: 37.38 points
- **TP 1RR**: 23693.60 ✅
- **TP 2RR**: 23656.22 ❌
- **TP 3RR**: 23618.84 ❌
- **TP 4RR**: 23581.46 ❌
- **TP 15RR**: 23170.30 ❌
- **PnL**: -37.38 points (-1.0R)
- **MFE**: 47.72 points
- **MAE**: 40.14 points

### Trade #1460 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 21:45:00
- **FVG 5m**: 23714.81 - 23720.62
- **Entrée**: 23712.80 @ 2025-09-03 21:59:00
- **Stop Loss**: 23748.14
- **Risk**: 35.35 points
- **TP 1RR**: 23677.45 ❌
- **TP 2RR**: 23642.10 ❌
- **TP 3RR**: 23606.75 ❌
- **TP 4RR**: 23571.40 ❌
- **TP 15RR**: 23182.57 ❌
- **PnL**: -35.35 points (-1.0R)
- **MFE**: 29.54 points
- **MAE**: 38.12 points

### Trade #1461 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-03 22:15:00
- **FVG 5m**: 23704.46 - 23707.24
- **Entrée**: 23703.20 @ 2025-09-03 22:29:00
- **Stop Loss**: 23728.44
- **Risk**: 25.24 points
- **TP 1RR**: 23677.96 ❌
- **TP 2RR**: 23652.72 ❌
- **TP 3RR**: 23627.48 ❌
- **TP 4RR**: 23602.24 ❌
- **TP 15RR**: 23324.61 ❌
- **PnL**: -25.24 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 31.05 points

### Trade #1462 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 05:15:00
- **FVG 5m**: 23724.91 - 23742.08
- **Entrée**: 23722.14 @ 2025-09-04 07:19:00
- **Stop Loss**: 23778.96
- **Risk**: 56.82 points
- **TP 1RR**: 23665.31 ❌
- **TP 2RR**: 23608.49 ❌
- **TP 3RR**: 23551.66 ❌
- **TP 4RR**: 23494.84 ❌
- **TP 15RR**: 22869.77 ❌
- **PnL**: -56.82 points (-1.0R)
- **MFE**: 32.57 points
- **MAE**: 59.33 points

### Trade #1463 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 06:15:00
- **FVG 5m**: 23724.91 - 23742.08
- **Entrée**: 23722.14 @ 2025-09-04 07:19:00
- **Stop Loss**: 23764.56
- **Risk**: 42.43 points
- **TP 1RR**: 23679.71 ❌
- **TP 2RR**: 23637.28 ❌
- **TP 3RR**: 23594.86 ❌
- **TP 4RR**: 23552.43 ❌
- **TP 15RR**: 23085.75 ❌
- **PnL**: -42.43 points (-1.0R)
- **MFE**: 32.57 points
- **MAE**: 48.98 points

### Trade #1464 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 08:30:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23671.39 @ 2025-09-04 09:03:00
- **Stop Loss**: 23793.36
- **Risk**: 121.97 points
- **TP 1RR**: 23549.42 ❌
- **TP 2RR**: 23427.45 ❌
- **TP 3RR**: 23305.48 ❌
- **TP 4RR**: 23183.51 ❌
- **TP 15RR**: 21841.84 ❌
- **PnL**: -121.97 points (-1.0R)
- **MFE**: 29.54 points
- **MAE**: 125.99 points

### Trade #1465 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 08:30:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23671.39 @ 2025-09-04 09:03:00
- **Stop Loss**: 23793.36
- **Risk**: 121.97 points
- **TP 1RR**: 23549.42 ❌
- **TP 2RR**: 23427.45 ❌
- **TP 3RR**: 23305.48 ❌
- **TP 4RR**: 23183.51 ❌
- **TP 15RR**: 21841.84 ❌
- **PnL**: -121.97 points (-1.0R)
- **MFE**: 29.54 points
- **MAE**: 125.99 points

### Trade #1466 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-04 08:30:00
- **FVG 5m**: 23686.54 - 23691.33
- **Entrée**: 23671.39 @ 2025-09-04 09:03:00
- **Stop Loss**: 23793.36
- **Risk**: 121.97 points
- **TP 1RR**: 23549.42 ❌
- **TP 2RR**: 23427.45 ❌
- **TP 3RR**: 23305.48 ❌
- **TP 4RR**: 23183.51 ❌
- **TP 15RR**: 21841.84 ❌
- **PnL**: -121.97 points (-1.0R)
- **MFE**: 29.54 points
- **MAE**: 125.99 points

### Trade #1467 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 09:15:00
- **FVG 5m**: 23727.19 - 23730.22
- **Entrée**: 23737.29 @ 2025-09-04 09:32:00
- **Stop Loss**: 23630.03
- **Risk**: 107.26 points
- **TP 1RR**: 23844.54 ✅
- **TP 2RR**: 23951.80 ✅
- **TP 3RR**: 24059.06 ✅
- **TP 4RR**: 24166.31 ✅
- **TP 15RR**: 25346.14 ✅
- **PnL**: 1608.85 points (15.0R)
- **MFE**: 1610.21 points
- **MAE**: 14.14 points

### Trade #1468 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 09:15:00
- **FVG 5m**: 23727.19 - 23730.22
- **Entrée**: 23737.29 @ 2025-09-04 09:32:00
- **Stop Loss**: 23630.03
- **Risk**: 107.26 points
- **TP 1RR**: 23844.54 ✅
- **TP 2RR**: 23951.80 ✅
- **TP 3RR**: 24059.06 ✅
- **TP 4RR**: 24166.31 ✅
- **TP 15RR**: 25346.14 ✅
- **PnL**: 1608.85 points (15.0R)
- **MFE**: 1610.21 points
- **MAE**: 14.14 points

### Trade #1469 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 09:15:00
- **FVG 5m**: 23727.19 - 23730.22
- **Entrée**: 23737.29 @ 2025-09-04 09:32:00
- **Stop Loss**: 23630.03
- **Risk**: 107.26 points
- **TP 1RR**: 23844.54 ✅
- **TP 2RR**: 23951.80 ✅
- **TP 3RR**: 24059.06 ✅
- **TP 4RR**: 24166.31 ✅
- **TP 15RR**: 25346.14 ✅
- **PnL**: 1608.85 points (15.0R)
- **MFE**: 1610.21 points
- **MAE**: 14.14 points

### Trade #1470 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 10:15:00
- **FVG 5m**: 23774.15 - 23777.18
- **Entrée**: 23777.43 @ 2025-09-04 11:08:00
- **Stop Loss**: 23725.67
- **Risk**: 51.76 points
- **TP 1RR**: 23829.19 ✅
- **TP 2RR**: 23880.95 ✅
- **TP 3RR**: 23932.71 ✅
- **TP 4RR**: 23984.47 ✅
- **TP 15RR**: 24553.83 ✅
- **PnL**: 776.40 points (15.0R)
- **MFE**: 779.32 points
- **MAE**: 39.64 points

### Trade #1471 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 12:15:00
- **FVG 5m**: 23838.28 - 23844.34
- **Entrée**: 23845.09 @ 2025-09-04 13:33:00
- **Stop Loss**: 23772.61
- **Risk**: 72.49 points
- **TP 1RR**: 23917.58 ✅
- **TP 2RR**: 23990.07 ✅
- **TP 3RR**: 24062.55 ✅
- **TP 4RR**: 24135.04 ✅
- **TP 15RR**: 24932.39 ❌
- **PnL**: -72.49 points (-1.0R)
- **MFE**: 293.63 points
- **MAE**: 79.02 points

### Trade #1472 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-04 12:45:00
- **FVG 5m**: 23838.28 - 23844.34
- **Entrée**: 23845.09 @ 2025-09-04 13:33:00
- **Stop Loss**: 23790.52
- **Risk**: 54.57 points
- **TP 1RR**: 23899.66 ✅
- **TP 2RR**: 23954.23 ✅
- **TP 3RR**: 24008.80 ✅
- **TP 4RR**: 24063.37 ✅
- **TP 15RR**: 24663.64 ❌
- **PnL**: -54.57 points (-1.0R)
- **MFE**: 293.63 points
- **MAE**: 61.10 points

### Trade #1473 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-05 07:30:00
- **FVG 5m**: 24067.02 - 24074.09
- **Entrée**: 24076.36 @ 2025-09-05 07:49:00
- **Stop Loss**: 23948.49
- **Risk**: 127.87 points
- **TP 1RR**: 24204.23 ❌
- **TP 2RR**: 24332.09 ❌
- **TP 3RR**: 24459.96 ❌
- **TP 4RR**: 24587.83 ❌
- **TP 15RR**: 25994.36 ❌
- **PnL**: -127.87 points (-1.0R)
- **MFE**: 62.36 points
- **MAE**: 142.90 points

### Trade #1474 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-05 07:30:00
- **FVG 5m**: 24067.02 - 24074.09
- **Entrée**: 24076.36 @ 2025-09-05 07:49:00
- **Stop Loss**: 23948.49
- **Risk**: 127.87 points
- **TP 1RR**: 24204.23 ❌
- **TP 2RR**: 24332.09 ❌
- **TP 3RR**: 24459.96 ❌
- **TP 4RR**: 24587.83 ❌
- **TP 15RR**: 25994.36 ❌
- **PnL**: -127.87 points (-1.0R)
- **MFE**: 62.36 points
- **MAE**: 142.90 points

### Trade #1475 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-05 07:45:00
- **FVG 5m**: 24111.45 - 24117.77
- **Entrée**: 24120.29 @ 2025-09-05 08:03:00
- **Stop Loss**: 24045.40
- **Risk**: 74.90 points
- **TP 1RR**: 24195.19 ❌
- **TP 2RR**: 24270.08 ❌
- **TP 3RR**: 24344.98 ❌
- **TP 4RR**: 24419.87 ❌
- **TP 15RR**: 25243.72 ❌
- **PnL**: -74.90 points (-1.0R)
- **MFE**: 18.43 points
- **MAE**: 80.03 points

### Trade #1476 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 08:15:00
- **FVG 5m**: 24092.01 - 24107.42
- **Entrée**: 24089.99 @ 2025-09-05 08:32:00
- **Stop Loss**: 24145.23
- **Risk**: 55.24 points
- **TP 1RR**: 24034.75 ✅
- **TP 2RR**: 23979.51 ✅
- **TP 3RR**: 23924.27 ✅
- **TP 4RR**: 23869.03 ✅
- **TP 15RR**: 23261.39 ❌
- **PnL**: -55.24 points (-1.0R)
- **MFE**: 352.20 points
- **MAE**: 56.05 points

### Trade #1477 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24101.79
- **Risk**: 110.26 points
- **TP 1RR**: 23881.27 ✅
- **TP 2RR**: 23771.01 ✅
- **TP 3RR**: 23660.75 ❌
- **TP 4RR**: 23550.50 ❌
- **TP 15RR**: 22337.66 ❌
- **PnL**: -110.26 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 110.58 points

### Trade #1478 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24101.79
- **Risk**: 110.26 points
- **TP 1RR**: 23881.27 ✅
- **TP 2RR**: 23771.01 ✅
- **TP 3RR**: 23660.75 ❌
- **TP 4RR**: 23550.50 ❌
- **TP 15RR**: 22337.66 ❌
- **PnL**: -110.26 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 110.58 points

### Trade #1479 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24101.79
- **Risk**: 110.26 points
- **TP 1RR**: 23881.27 ✅
- **TP 2RR**: 23771.01 ✅
- **TP 3RR**: 23660.75 ❌
- **TP 4RR**: 23550.50 ❌
- **TP 15RR**: 22337.66 ❌
- **PnL**: -110.26 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 110.58 points

### Trade #1480 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24101.79
- **Risk**: 110.26 points
- **TP 1RR**: 23881.27 ✅
- **TP 2RR**: 23771.01 ✅
- **TP 3RR**: 23660.75 ❌
- **TP 4RR**: 23550.50 ❌
- **TP 15RR**: 22337.66 ❌
- **PnL**: -110.26 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 110.58 points

### Trade #1481 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24101.79
- **Risk**: 110.26 points
- **TP 1RR**: 23881.27 ✅
- **TP 2RR**: 23771.01 ✅
- **TP 3RR**: 23660.75 ❌
- **TP 4RR**: 23550.50 ❌
- **TP 15RR**: 22337.66 ❌
- **PnL**: -110.26 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 110.58 points

### Trade #1482 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-05 09:00:00
- **FVG 5m**: 23998.85 - 24021.57
- **Entrée**: 23991.53 @ 2025-09-05 09:14:00
- **Stop Loss**: 24101.79
- **Risk**: 110.26 points
- **TP 1RR**: 23881.27 ✅
- **TP 2RR**: 23771.01 ✅
- **TP 3RR**: 23660.75 ❌
- **TP 4RR**: 23550.50 ❌
- **TP 15RR**: 22337.66 ❌
- **PnL**: -110.26 points (-1.0R)
- **MFE**: 253.74 points
- **MAE**: 110.58 points

### Trade #1483 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-07 17:30:00
- **FVG 5m**: 23951.89 - 23963.50
- **Entrée**: 23974.11 @ 2025-09-07 17:45:00
- **Stop Loss**: 23920.48
- **Risk**: 53.62 points
- **TP 1RR**: 24027.73 ✅
- **TP 2RR**: 24081.36 ✅
- **TP 3RR**: 24134.98 ✅
- **TP 4RR**: 24188.61 ✅
- **TP 15RR**: 24778.48 ✅
- **PnL**: 804.37 points (15.0R)
- **MFE**: 805.14 points
- **MAE**: 14.64 points

### Trade #1484 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-07 17:30:00
- **FVG 5m**: 23951.89 - 23963.50
- **Entrée**: 23974.11 @ 2025-09-07 17:45:00
- **Stop Loss**: 23920.48
- **Risk**: 53.62 points
- **TP 1RR**: 24027.73 ✅
- **TP 2RR**: 24081.36 ✅
- **TP 3RR**: 24134.98 ✅
- **TP 4RR**: 24188.61 ✅
- **TP 15RR**: 24778.48 ✅
- **PnL**: 804.37 points (15.0R)
- **MFE**: 805.14 points
- **MAE**: 14.64 points

### Trade #1485 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-07 21:00:00
- **FVG 5m**: 23980.17 - 23987.74
- **Entrée**: 23979.41 @ 2025-09-07 21:18:00
- **Stop Loss**: 24018.43
- **Risk**: 39.02 points
- **TP 1RR**: 23940.39 ❌
- **TP 2RR**: 23901.37 ❌
- **TP 3RR**: 23862.36 ❌
- **TP 4RR**: 23823.34 ❌
- **TP 15RR**: 23394.14 ❌
- **PnL**: -39.02 points (-1.0R)
- **MFE**: 19.95 points
- **MAE**: 39.64 points

### Trade #1486 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 08:45:00
- **FVG 5m**: 24066.77 - 24074.85
- **Entrée**: 24064.49 @ 2025-09-08 09:17:00
- **Stop Loss**: 24124.77
- **Risk**: 60.28 points
- **TP 1RR**: 24004.21 ✅
- **TP 2RR**: 23943.94 ❌
- **TP 3RR**: 23883.66 ❌
- **TP 4RR**: 23823.38 ❌
- **TP 15RR**: 23160.31 ❌
- **PnL**: -60.28 points (-1.0R)
- **MFE**: 103.52 points
- **MAE**: 62.11 points

### Trade #1487 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 12:00:00
- **FVG 5m**: 24011.22 - 24022.08
- **Entrée**: 24004.66 @ 2025-09-08 14:12:00
- **Stop Loss**: 24063.64
- **Risk**: 58.99 points
- **TP 1RR**: 23945.67 ❌
- **TP 2RR**: 23886.68 ❌
- **TP 3RR**: 23827.70 ❌
- **TP 4RR**: 23768.71 ❌
- **TP 15RR**: 23119.86 ❌
- **PnL**: -58.99 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 60.34 points

### Trade #1488 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 12:00:00
- **FVG 5m**: 24011.22 - 24022.08
- **Entrée**: 24004.66 @ 2025-09-08 14:12:00
- **Stop Loss**: 24063.64
- **Risk**: 58.99 points
- **TP 1RR**: 23945.67 ❌
- **TP 2RR**: 23886.68 ❌
- **TP 3RR**: 23827.70 ❌
- **TP 4RR**: 23768.71 ❌
- **TP 15RR**: 23119.86 ❌
- **PnL**: -58.99 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 60.34 points

### Trade #1489 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-08 14:00:00
- **FVG 5m**: 24011.22 - 24022.08
- **Entrée**: 24004.66 @ 2025-09-08 14:12:00
- **Stop Loss**: 24044.19
- **Risk**: 39.54 points
- **TP 1RR**: 23965.12 ❌
- **TP 2RR**: 23925.59 ❌
- **TP 3RR**: 23886.05 ❌
- **TP 4RR**: 23846.51 ❌
- **TP 15RR**: 23411.62 ❌
- **PnL**: -39.54 points (-1.0R)
- **MFE**: 9.34 points
- **MAE**: 42.67 points

### Trade #1490 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 06:30:00
- **FVG 5m**: 24073.08 - 24081.41
- **Entrée**: 24081.92 @ 2025-09-09 06:48:00
- **Stop Loss**: 24044.64
- **Risk**: 37.28 points
- **TP 1RR**: 24119.19 ❌
- **TP 2RR**: 24156.47 ❌
- **TP 3RR**: 24193.74 ❌
- **TP 4RR**: 24231.02 ❌
- **TP 15RR**: 24641.05 ❌
- **PnL**: -37.28 points (-1.0R)
- **MFE**: 11.61 points
- **MAE**: 45.95 points

### Trade #1491 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-09 08:45:00
- **FVG 5m**: 24048.08 - 24050.86
- **Entrée**: 24037.98 @ 2025-09-09 09:26:00
- **Stop Loss**: 24096.99
- **Risk**: 59.00 points
- **TP 1RR**: 23978.98 ✅
- **TP 2RR**: 23919.98 ❌
- **TP 3RR**: 23860.98 ❌
- **TP 4RR**: 23801.97 ❌
- **TP 15RR**: 23152.94 ❌
- **PnL**: -59.00 points (-1.0R)
- **MFE**: 77.01 points
- **MAE**: 59.33 points

### Trade #1492 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:00:00
- **FVG 5m**: 23999.86 - 24021.32
- **Entrée**: 24023.09 @ 2025-09-09 09:54:00
- **Stop Loss**: 24004.77
- **Risk**: 18.32 points
- **TP 1RR**: 24041.41 ❌
- **TP 2RR**: 24059.73 ❌
- **TP 3RR**: 24078.05 ❌
- **TP 4RR**: 24096.37 ❌
- **TP 15RR**: 24297.89 ❌
- **PnL**: -18.32 points (-1.0R)
- **MFE**: 16.41 points
- **MAE**: 18.94 points

### Trade #1493 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:30:00
- **FVG 5m**: 23999.86 - 24021.32
- **Entrée**: 24023.09 @ 2025-09-09 09:54:00
- **Stop Loss**: 23949.00
- **Risk**: 74.09 points
- **TP 1RR**: 24097.18 ✅
- **TP 2RR**: 24171.27 ✅
- **TP 3RR**: 24245.36 ✅
- **TP 4RR**: 24319.45 ✅
- **TP 15RR**: 25134.43 ✅
- **PnL**: 1111.34 points (15.0R)
- **MFE**: 1112.41 points
- **MAE**: 35.85 points

### Trade #1494 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:30:00
- **FVG 5m**: 23999.86 - 24021.32
- **Entrée**: 24023.09 @ 2025-09-09 09:54:00
- **Stop Loss**: 23949.00
- **Risk**: 74.09 points
- **TP 1RR**: 24097.18 ✅
- **TP 2RR**: 24171.27 ✅
- **TP 3RR**: 24245.36 ✅
- **TP 4RR**: 24319.45 ✅
- **TP 15RR**: 25134.43 ✅
- **PnL**: 1111.34 points (15.0R)
- **MFE**: 1112.41 points
- **MAE**: 35.85 points

### Trade #1495 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:45:00
- **FVG 5m**: 24011.22 - 24019.30
- **Entrée**: 24027.13 @ 2025-09-09 10:52:00
- **Stop Loss**: 23959.85
- **Risk**: 67.28 points
- **TP 1RR**: 24094.41 ✅
- **TP 2RR**: 24161.68 ✅
- **TP 3RR**: 24228.96 ✅
- **TP 4RR**: 24296.24 ✅
- **TP 15RR**: 25036.30 ✅
- **PnL**: 1009.17 points (15.0R)
- **MFE**: 1009.62 points
- **MAE**: 10.10 points

### Trade #1496 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-09 09:45:00
- **FVG 5m**: 24011.22 - 24019.30
- **Entrée**: 24027.13 @ 2025-09-09 10:52:00
- **Stop Loss**: 23959.85
- **Risk**: 67.28 points
- **TP 1RR**: 24094.41 ✅
- **TP 2RR**: 24161.68 ✅
- **TP 3RR**: 24228.96 ✅
- **TP 4RR**: 24296.24 ✅
- **TP 15RR**: 25036.30 ✅
- **PnL**: 1009.17 points (15.0R)
- **MFE**: 1009.62 points
- **MAE**: 10.10 points

### Trade #1497 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 03:15:00
- **FVG 5m**: 24136.95 - 24146.80
- **Entrée**: 24130.64 @ 2025-09-10 03:33:00
- **Stop Loss**: 24180.85
- **Risk**: 50.21 points
- **TP 1RR**: 24080.43 ❌
- **TP 2RR**: 24030.23 ❌
- **TP 3RR**: 23980.02 ❌
- **TP 4RR**: 23929.81 ❌
- **TP 15RR**: 23377.52 ❌
- **PnL**: -50.21 points (-1.0R)
- **MFE**: 11.87 points
- **MAE**: 52.52 points

### Trade #1498 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 07:30:00
- **FVG 5m**: 24227.59 - 24235.17
- **Entrée**: 24225.32 @ 2025-09-10 08:01:00
- **Stop Loss**: 24294.52
- **Risk**: 69.20 points
- **TP 1RR**: 24156.12 ✅
- **TP 2RR**: 24086.92 ✅
- **TP 3RR**: 24017.72 ❌
- **TP 4RR**: 23948.52 ❌
- **TP 15RR**: 23187.31 ❌
- **PnL**: -69.20 points (-1.0R)
- **MFE**: 204.76 points
- **MAE**: 77.51 points

### Trade #1499 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 07:30:00
- **FVG 5m**: 24227.59 - 24235.17
- **Entrée**: 24225.32 @ 2025-09-10 08:01:00
- **Stop Loss**: 24294.52
- **Risk**: 69.20 points
- **TP 1RR**: 24156.12 ✅
- **TP 2RR**: 24086.92 ✅
- **TP 3RR**: 24017.72 ❌
- **TP 4RR**: 23948.52 ❌
- **TP 15RR**: 23187.31 ❌
- **PnL**: -69.20 points (-1.0R)
- **MFE**: 204.76 points
- **MAE**: 77.51 points

### Trade #1500 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 07:30:00
- **FVG 5m**: 24227.59 - 24235.42
- **Entrée**: 24238.70 @ 2025-09-10 08:12:00
- **Stop Loss**: 24151.38
- **Risk**: 87.32 points
- **TP 1RR**: 24326.02 ❌
- **TP 2RR**: 24413.34 ❌
- **TP 3RR**: 24500.66 ❌
- **TP 4RR**: 24587.98 ❌
- **TP 15RR**: 25548.50 ❌
- **PnL**: -87.32 points (-1.0R)
- **MFE**: 14.14 points
- **MAE**: 91.65 points

### Trade #1501 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24250.32
- **Risk**: 74.48 points
- **TP 1RR**: 24101.36 ✅
- **TP 2RR**: 24026.87 ✅
- **TP 3RR**: 23952.39 ❌
- **TP 4RR**: 23877.91 ❌
- **TP 15RR**: 23058.63 ❌
- **PnL**: -74.48 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 74.99 points

### Trade #1502 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24250.32
- **Risk**: 74.48 points
- **TP 1RR**: 24101.36 ✅
- **TP 2RR**: 24026.87 ✅
- **TP 3RR**: 23952.39 ❌
- **TP 4RR**: 23877.91 ❌
- **TP 15RR**: 23058.63 ❌
- **PnL**: -74.48 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 74.99 points

### Trade #1503 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24250.32
- **Risk**: 74.48 points
- **TP 1RR**: 24101.36 ✅
- **TP 2RR**: 24026.87 ✅
- **TP 3RR**: 23952.39 ❌
- **TP 4RR**: 23877.91 ❌
- **TP 15RR**: 23058.63 ❌
- **PnL**: -74.48 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 74.99 points

### Trade #1504 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24250.32
- **Risk**: 74.48 points
- **TP 1RR**: 24101.36 ✅
- **TP 2RR**: 24026.87 ✅
- **TP 3RR**: 23952.39 ❌
- **TP 4RR**: 23877.91 ❌
- **TP 15RR**: 23058.63 ❌
- **PnL**: -74.48 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 74.99 points

### Trade #1505 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 08:30:00
- **FVG 5m**: 24178.61 - 24203.36
- **Entrée**: 24175.84 @ 2025-09-10 10:19:00
- **Stop Loss**: 24250.32
- **Risk**: 74.48 points
- **TP 1RR**: 24101.36 ✅
- **TP 2RR**: 24026.87 ✅
- **TP 3RR**: 23952.39 ❌
- **TP 4RR**: 23877.91 ❌
- **TP 15RR**: 23058.63 ❌
- **PnL**: -74.48 points (-1.0R)
- **MFE**: 155.27 points
- **MAE**: 74.99 points

### Trade #1506 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 08:45:00
- **FVG 5m**: 24173.06 - 24182.15
- **Entrée**: 24188.96 @ 2025-09-10 09:01:00
- **Stop Loss**: 24124.89
- **Risk**: 64.08 points
- **TP 1RR**: 24253.04 ❌
- **TP 2RR**: 24317.12 ❌
- **TP 3RR**: 24381.20 ❌
- **TP 4RR**: 24445.28 ❌
- **TP 15RR**: 25150.14 ❌
- **PnL**: -64.08 points (-1.0R)
- **MFE**: 39.64 points
- **MAE**: 65.39 points

### Trade #1507 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24153.62 - 24159.93
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24190.20
- **Risk**: 41.38 points
- **TP 1RR**: 24107.44 ✅
- **TP 2RR**: 24066.07 ✅
- **TP 3RR**: 24024.69 ✅
- **TP 4RR**: 23983.32 ❌
- **TP 15RR**: 23528.18 ❌
- **PnL**: -41.38 points (-1.0R)
- **MFE**: 128.26 points
- **MAE**: 41.66 points

### Trade #1508 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24153.62 - 24159.93
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24190.20
- **Risk**: 41.38 points
- **TP 1RR**: 24107.44 ✅
- **TP 2RR**: 24066.07 ✅
- **TP 3RR**: 24024.69 ✅
- **TP 4RR**: 23983.32 ❌
- **TP 15RR**: 23528.18 ❌
- **PnL**: -41.38 points (-1.0R)
- **MFE**: 128.26 points
- **MAE**: 41.66 points

### Trade #1509 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24153.62 - 24159.93
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24190.20
- **Risk**: 41.38 points
- **TP 1RR**: 24107.44 ✅
- **TP 2RR**: 24066.07 ✅
- **TP 3RR**: 24024.69 ✅
- **TP 4RR**: 23983.32 ❌
- **TP 15RR**: 23528.18 ❌
- **PnL**: -41.38 points (-1.0R)
- **MFE**: 128.26 points
- **MAE**: 41.66 points

### Trade #1510 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 11:15:00
- **FVG 5m**: 24153.62 - 24159.93
- **Entrée**: 24148.82 @ 2025-09-10 12:19:00
- **Stop Loss**: 24190.20
- **Risk**: 41.38 points
- **TP 1RR**: 24107.44 ✅
- **TP 2RR**: 24066.07 ✅
- **TP 3RR**: 24024.69 ✅
- **TP 4RR**: 23983.32 ❌
- **TP 15RR**: 23528.18 ❌
- **PnL**: -41.38 points (-1.0R)
- **MFE**: 128.26 points
- **MAE**: 41.66 points

### Trade #1511 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 11:45:00
- **FVG 5m**: 24151.85 - 24156.65
- **Entrée**: 24161.44 @ 2025-09-10 11:57:00
- **Stop Loss**: 24121.86
- **Risk**: 39.59 points
- **TP 1RR**: 24201.03 ❌
- **TP 2RR**: 24240.62 ❌
- **TP 3RR**: 24280.21 ❌
- **TP 4RR**: 24319.79 ❌
- **TP 15RR**: 24755.25 ❌
- **PnL**: -39.59 points (-1.0R)
- **MFE**: 15.91 points
- **MAE**: 52.52 points

### Trade #1512 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 12:15:00
- **FVG 5m**: 24107.67 - 24112.46
- **Entrée**: 24097.32 @ 2025-09-10 13:19:00
- **Stop Loss**: 24175.29
- **Risk**: 77.98 points
- **TP 1RR**: 24019.34 ❌
- **TP 2RR**: 23941.36 ❌
- **TP 3RR**: 23863.38 ❌
- **TP 4RR**: 23785.40 ❌
- **TP 15RR**: 22927.65 ❌
- **PnL**: -77.98 points (-1.0R)
- **MFE**: 76.75 points
- **MAE**: 78.02 points

### Trade #1513 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 12:15:00
- **FVG 5m**: 24107.67 - 24112.46
- **Entrée**: 24097.32 @ 2025-09-10 13:19:00
- **Stop Loss**: 24175.29
- **Risk**: 77.98 points
- **TP 1RR**: 24019.34 ❌
- **TP 2RR**: 23941.36 ❌
- **TP 3RR**: 23863.38 ❌
- **TP 4RR**: 23785.40 ❌
- **TP 15RR**: 22927.65 ❌
- **PnL**: -77.98 points (-1.0R)
- **MFE**: 76.75 points
- **MAE**: 78.02 points

### Trade #1514 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 12:15:00
- **FVG 5m**: 24107.67 - 24112.46
- **Entrée**: 24097.32 @ 2025-09-10 13:19:00
- **Stop Loss**: 24175.29
- **Risk**: 77.98 points
- **TP 1RR**: 24019.34 ❌
- **TP 2RR**: 23941.36 ❌
- **TP 3RR**: 23863.38 ❌
- **TP 4RR**: 23785.40 ❌
- **TP 15RR**: 22927.65 ❌
- **PnL**: -77.98 points (-1.0R)
- **MFE**: 76.75 points
- **MAE**: 78.02 points

### Trade #1515 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 13:15:00
- **FVG 5m**: 24084.69 - 24096.56
- **Entrée**: 24082.17 @ 2025-09-10 13:47:00
- **Stop Loss**: 24136.65
- **Risk**: 54.48 points
- **TP 1RR**: 24027.69 ✅
- **TP 2RR**: 23973.21 ❌
- **TP 3RR**: 23918.73 ❌
- **TP 4RR**: 23864.25 ❌
- **TP 15RR**: 23264.99 ❌
- **PnL**: -54.48 points (-1.0R)
- **MFE**: 61.60 points
- **MAE**: 63.37 points

### Trade #1516 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 14:45:00
- **FVG 5m**: 24099.34 - 24106.66
- **Entrée**: 24107.67 @ 2025-09-10 17:03:00
- **Stop Loss**: 24074.16
- **Risk**: 33.50 points
- **TP 1RR**: 24141.17 ✅
- **TP 2RR**: 24174.67 ✅
- **TP 3RR**: 24208.18 ❌
- **TP 4RR**: 24241.68 ❌
- **TP 15RR**: 24610.22 ❌
- **PnL**: -33.50 points (-1.0R)
- **MFE**: 103.77 points
- **MAE**: 33.58 points

### Trade #1517 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-10 19:00:00
- **FVG 5m**: 24120.29 - 24123.83
- **Entrée**: 24117.51 @ 2025-09-10 19:15:00
- **Stop Loss**: 24154.33
- **Risk**: 36.81 points
- **TP 1RR**: 24080.70 ❌
- **TP 2RR**: 24043.89 ❌
- **TP 3RR**: 24007.07 ❌
- **TP 4RR**: 23970.26 ❌
- **TP 15RR**: 23565.31 ❌
- **PnL**: -36.81 points (-1.0R)
- **MFE**: 9.59 points
- **MAE**: 37.37 points

### Trade #1518 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-10 19:30:00
- **FVG 5m**: 24144.02 - 24146.55
- **Entrée**: 24147.31 @ 2025-09-10 21:27:00
- **Stop Loss**: 24105.96
- **Risk**: 41.35 points
- **TP 1RR**: 24188.65 ✅
- **TP 2RR**: 24230.00 ❌
- **TP 3RR**: 24271.34 ❌
- **TP 4RR**: 24312.69 ❌
- **TP 15RR**: 24767.50 ❌
- **PnL**: -41.35 points (-1.0R)
- **MFE**: 64.13 points
- **MAE**: 73.22 points

### Trade #1519 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24183.16 - 24205.12
- **Entrée**: 24172.05 @ 2025-09-11 08:39:00
- **Stop Loss**: 24225.56
- **Risk**: 53.51 points
- **TP 1RR**: 24118.54 ❌
- **TP 2RR**: 24065.02 ❌
- **TP 3RR**: 24011.51 ❌
- **TP 4RR**: 23958.00 ❌
- **TP 15RR**: 23369.36 ❌
- **PnL**: -53.51 points (-1.0R)
- **MFE**: 25.50 points
- **MAE**: 69.68 points

### Trade #1520 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24062.05
- **Risk**: 112.27 points
- **TP 1RR**: 24286.59 ✅
- **TP 2RR**: 24398.86 ✅
- **TP 3RR**: 24511.13 ✅
- **TP 4RR**: 24623.40 ✅
- **TP 15RR**: 25858.37 ✅
- **PnL**: 1684.05 points (15.0R)
- **MFE**: 1685.18 points
- **MAE**: 27.77 points

### Trade #1521 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24062.05
- **Risk**: 112.27 points
- **TP 1RR**: 24286.59 ✅
- **TP 2RR**: 24398.86 ✅
- **TP 3RR**: 24511.13 ✅
- **TP 4RR**: 24623.40 ✅
- **TP 15RR**: 25858.37 ✅
- **PnL**: 1684.05 points (15.0R)
- **MFE**: 1685.18 points
- **MAE**: 27.77 points

### Trade #1522 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24062.05
- **Risk**: 112.27 points
- **TP 1RR**: 24286.59 ✅
- **TP 2RR**: 24398.86 ✅
- **TP 3RR**: 24511.13 ✅
- **TP 4RR**: 24623.40 ✅
- **TP 15RR**: 25858.37 ✅
- **PnL**: 1684.05 points (15.0R)
- **MFE**: 1685.18 points
- **MAE**: 27.77 points

### Trade #1523 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24062.05
- **Risk**: 112.27 points
- **TP 1RR**: 24286.59 ✅
- **TP 2RR**: 24398.86 ✅
- **TP 3RR**: 24511.13 ✅
- **TP 4RR**: 24623.40 ✅
- **TP 15RR**: 25858.37 ✅
- **PnL**: 1684.05 points (15.0R)
- **MFE**: 1685.18 points
- **MAE**: 27.77 points

### Trade #1524 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-11 07:30:00
- **FVG 5m**: 24161.95 - 24165.48
- **Entrée**: 24174.32 @ 2025-09-11 07:46:00
- **Stop Loss**: 24062.05
- **Risk**: 112.27 points
- **TP 1RR**: 24286.59 ✅
- **TP 2RR**: 24398.86 ✅
- **TP 3RR**: 24511.13 ✅
- **TP 4RR**: 24623.40 ✅
- **TP 15RR**: 25858.37 ✅
- **PnL**: 1684.05 points (15.0R)
- **MFE**: 1685.18 points
- **MAE**: 27.77 points

### Trade #1525 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-11 09:45:00
- **FVG 5m**: 24266.22 - 24274.30
- **Entrée**: 24263.45 @ 2025-09-11 10:38:00
- **Stop Loss**: 24270.02
- **Risk**: 6.57 points
- **TP 1RR**: 24256.87 ✅
- **TP 2RR**: 24250.30 ✅
- **TP 3RR**: 24243.72 ✅
- **TP 4RR**: 24237.15 ❌
- **TP 15RR**: 24164.83 ❌
- **PnL**: -6.57 points (-1.0R)
- **MFE**: 22.72 points
- **MAE**: 10.86 points

### Trade #1526 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-12 14:45:00
- **FVG 5m**: 24350.55 - 24356.86
- **Entrée**: 24349.29 @ 2025-09-12 14:59:00
- **Stop Loss**: 24385.21
- **Risk**: 35.92 points
- **TP 1RR**: 24313.37 ❌
- **TP 2RR**: 24277.45 ❌
- **TP 3RR**: 24241.53 ❌
- **TP 4RR**: 24205.61 ❌
- **TP 15RR**: 23810.50 ❌
- **PnL**: -35.92 points (-1.0R)
- **MFE**: 18.68 points
- **MAE**: 37.46 points

### Trade #1527 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 03:00:00
- **FVG 5m**: 24336.00 - 24340.75
- **Entrée**: 24335.25 @ 2025-09-15 03:56:00
- **Stop Loss**: 24394.94
- **Risk**: 59.69 points
- **TP 1RR**: 24275.56 ❌
- **TP 2RR**: 24215.87 ❌
- **TP 3RR**: 24156.18 ❌
- **TP 4RR**: 24096.48 ❌
- **TP 15RR**: 23439.88 ❌
- **PnL**: -59.69 points (-1.0R)
- **MFE**: 15.25 points
- **MAE**: 73.50 points

### Trade #1528 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-15 03:00:00
- **FVG 5m**: 24336.00 - 24339.75
- **Entrée**: 24340.25 @ 2025-09-15 03:42:00
- **Stop Loss**: 24305.59
- **Risk**: 34.66 points
- **TP 1RR**: 24374.91 ✅
- **TP 2RR**: 24409.57 ✅
- **TP 3RR**: 24444.23 ✅
- **TP 4RR**: 24478.89 ✅
- **TP 15RR**: 24860.13 ❌
- **PnL**: -34.66 points (-1.0R)
- **MFE**: 307.00 points
- **MAE**: 48.50 points

### Trade #1529 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-15 03:00:00
- **FVG 5m**: 24336.00 - 24339.75
- **Entrée**: 24340.25 @ 2025-09-15 03:42:00
- **Stop Loss**: 24305.59
- **Risk**: 34.66 points
- **TP 1RR**: 24374.91 ✅
- **TP 2RR**: 24409.57 ✅
- **TP 3RR**: 24444.23 ✅
- **TP 4RR**: 24478.89 ✅
- **TP 15RR**: 24860.13 ❌
- **PnL**: -34.66 points (-1.0R)
- **MFE**: 307.00 points
- **MAE**: 48.50 points

### Trade #1530 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 07:15:00
- **FVG 5m**: 24392.25 - 24396.50
- **Entrée**: 24388.75 @ 2025-09-15 07:31:00
- **Stop Loss**: 24425.21
- **Risk**: 36.46 points
- **TP 1RR**: 24352.29 ❌
- **TP 2RR**: 24315.84 ❌
- **TP 3RR**: 24279.38 ❌
- **TP 4RR**: 24242.92 ❌
- **TP 15RR**: 23841.90 ❌
- **PnL**: -36.46 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 48.25 points

### Trade #1531 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 07:15:00
- **FVG 5m**: 24392.25 - 24396.50
- **Entrée**: 24388.75 @ 2025-09-15 07:31:00
- **Stop Loss**: 24425.21
- **Risk**: 36.46 points
- **TP 1RR**: 24352.29 ❌
- **TP 2RR**: 24315.84 ❌
- **TP 3RR**: 24279.38 ❌
- **TP 4RR**: 24242.92 ❌
- **TP 15RR**: 23841.90 ❌
- **PnL**: -36.46 points (-1.0R)
- **MFE**: 8.25 points
- **MAE**: 48.25 points

### Trade #1532 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 15:00:00
- **FVG 5m**: 24537.00 - 24539.50
- **Entrée**: 24530.00 @ 2025-09-15 17:01:00
- **Stop Loss**: 24566.78
- **Risk**: 36.78 points
- **TP 1RR**: 24493.22 ❌
- **TP 2RR**: 24456.45 ❌
- **TP 3RR**: 24419.67 ❌
- **TP 4RR**: 24382.89 ❌
- **TP 15RR**: 23978.34 ❌
- **PnL**: -36.78 points (-1.0R)
- **MFE**: 6.00 points
- **MAE**: 38.00 points

### Trade #1533 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-15 15:00:00
- **FVG 5m**: 24537.00 - 24539.50
- **Entrée**: 24530.00 @ 2025-09-15 17:01:00
- **Stop Loss**: 24566.78
- **Risk**: 36.78 points
- **TP 1RR**: 24493.22 ❌
- **TP 2RR**: 24456.45 ❌
- **TP 3RR**: 24419.67 ❌
- **TP 4RR**: 24382.89 ❌
- **TP 15RR**: 23978.34 ❌
- **PnL**: -36.78 points (-1.0R)
- **MFE**: 6.00 points
- **MAE**: 38.00 points

### Trade #1534 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-16 08:15:00
- **FVG 5m**: 24578.75 - 24586.00
- **Entrée**: 24570.50 @ 2025-09-16 08:33:00
- **Stop Loss**: 24621.80
- **Risk**: 51.30 points
- **TP 1RR**: 24519.20 ✅
- **TP 2RR**: 24467.89 ✅
- **TP 3RR**: 24416.59 ✅
- **TP 4RR**: 24365.28 ✅
- **TP 15RR**: 23800.93 ❌
- **PnL**: -51.30 points (-1.0R)
- **MFE**: 328.50 points
- **MAE**: 53.00 points

### Trade #1535 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-16 08:45:00
- **FVG 5m**: 24530.00 - 24535.00
- **Entrée**: 24522.25 @ 2025-09-16 10:01:00
- **Stop Loss**: 24582.54
- **Risk**: 60.29 points
- **TP 1RR**: 24461.96 ✅
- **TP 2RR**: 24401.68 ✅
- **TP 3RR**: 24341.39 ✅
- **TP 4RR**: 24281.11 ✅
- **TP 15RR**: 23617.97 ❌
- **PnL**: -60.29 points (-1.0R)
- **MFE**: 280.25 points
- **MAE**: 63.50 points

### Trade #1536 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-16 08:45:00
- **FVG 5m**: 24530.00 - 24535.00
- **Entrée**: 24522.25 @ 2025-09-16 10:01:00
- **Stop Loss**: 24582.54
- **Risk**: 60.29 points
- **TP 1RR**: 24461.96 ✅
- **TP 2RR**: 24401.68 ✅
- **TP 3RR**: 24341.39 ✅
- **TP 4RR**: 24281.11 ✅
- **TP 15RR**: 23617.97 ❌
- **PnL**: -60.29 points (-1.0R)
- **MFE**: 280.25 points
- **MAE**: 63.50 points

### Trade #1537 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-16 14:45:00
- **FVG 5m**: 24535.00 - 24538.25
- **Entrée**: 24531.25 @ 2025-09-16 15:58:00
- **Stop Loss**: 24575.28
- **Risk**: 44.03 points
- **TP 1RR**: 24487.22 ✅
- **TP 2RR**: 24443.19 ✅
- **TP 3RR**: 24399.16 ✅
- **TP 4RR**: 24355.12 ✅
- **TP 15RR**: 23870.78 ❌
- **PnL**: -44.03 points (-1.0R)
- **MFE**: 289.25 points
- **MAE**: 44.25 points

### Trade #1538 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 03:45:00
- **FVG 5m**: 24514.75 - 24517.50
- **Entrée**: 24517.75 @ 2025-09-17 04:04:00
- **Stop Loss**: 24467.51
- **Risk**: 50.24 points
- **TP 1RR**: 24567.99 ❌
- **TP 2RR**: 24618.23 ❌
- **TP 3RR**: 24668.47 ❌
- **TP 4RR**: 24718.71 ❌
- **TP 15RR**: 25271.35 ❌
- **PnL**: -50.24 points (-1.0R)
- **MFE**: 23.00 points
- **MAE**: 51.75 points

### Trade #1539 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 03:45:00
- **FVG 5m**: 24514.75 - 24517.50
- **Entrée**: 24517.75 @ 2025-09-17 04:04:00
- **Stop Loss**: 24467.51
- **Risk**: 50.24 points
- **TP 1RR**: 24567.99 ❌
- **TP 2RR**: 24618.23 ❌
- **TP 3RR**: 24668.47 ❌
- **TP 4RR**: 24718.71 ❌
- **TP 15RR**: 25271.35 ❌
- **PnL**: -50.24 points (-1.0R)
- **MFE**: 23.00 points
- **MAE**: 51.75 points

### Trade #1540 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 06:00:00
- **FVG 5m**: 24496.25 - 24501.25
- **Entrée**: 24501.50 @ 2025-09-17 06:48:00
- **Stop Loss**: 24474.26
- **Risk**: 27.24 points
- **TP 1RR**: 24528.74 ✅
- **TP 2RR**: 24555.99 ❌
- **TP 3RR**: 24583.23 ❌
- **TP 4RR**: 24610.47 ❌
- **TP 15RR**: 24910.15 ❌
- **PnL**: -27.24 points (-1.0R)
- **MFE**: 39.25 points
- **MAE**: 29.25 points

### Trade #1541 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24354.00 - 24382.75
- **Entrée**: 24393.00 @ 2025-09-17 13:59:00
- **Stop Loss**: 24279.60
- **Risk**: 113.40 points
- **TP 1RR**: 24506.40 ✅
- **TP 2RR**: 24619.79 ✅
- **TP 3RR**: 24733.19 ✅
- **TP 4RR**: 24846.58 ✅
- **TP 15RR**: 26093.94 ❌
- **PnL**: -113.40 points (-1.0R)
- **MFE**: 1001.00 points
- **MAE**: 142.50 points

### Trade #1542 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24354.00 - 24382.75
- **Entrée**: 24393.00 @ 2025-09-17 13:59:00
- **Stop Loss**: 24279.60
- **Risk**: 113.40 points
- **TP 1RR**: 24506.40 ✅
- **TP 2RR**: 24619.79 ✅
- **TP 3RR**: 24733.19 ✅
- **TP 4RR**: 24846.58 ✅
- **TP 15RR**: 26093.94 ❌
- **PnL**: -113.40 points (-1.0R)
- **MFE**: 1001.00 points
- **MAE**: 142.50 points

### Trade #1543 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24354.00 - 24382.75
- **Entrée**: 24393.00 @ 2025-09-17 13:59:00
- **Stop Loss**: 24279.60
- **Risk**: 113.40 points
- **TP 1RR**: 24506.40 ✅
- **TP 2RR**: 24619.79 ✅
- **TP 3RR**: 24733.19 ✅
- **TP 4RR**: 24846.58 ✅
- **TP 15RR**: 26093.94 ❌
- **PnL**: -113.40 points (-1.0R)
- **MFE**: 1001.00 points
- **MAE**: 142.50 points

### Trade #1544 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 13:15:00
- **FVG 5m**: 24354.00 - 24382.75
- **Entrée**: 24393.00 @ 2025-09-17 13:59:00
- **Stop Loss**: 24279.60
- **Risk**: 113.40 points
- **TP 1RR**: 24506.40 ✅
- **TP 2RR**: 24619.79 ✅
- **TP 3RR**: 24733.19 ✅
- **TP 4RR**: 24846.58 ✅
- **TP 15RR**: 26093.94 ❌
- **PnL**: -113.40 points (-1.0R)
- **MFE**: 1001.00 points
- **MAE**: 142.50 points

### Trade #1545 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24501.00 - 24505.50
- **Entrée**: 24506.25 @ 2025-09-17 15:28:00
- **Stop Loss**: 24416.54
- **Risk**: 89.71 points
- **TP 1RR**: 24595.96 ✅
- **TP 2RR**: 24685.68 ✅
- **TP 3RR**: 24775.39 ✅
- **TP 4RR**: 24865.11 ✅
- **TP 15RR**: 25851.97 ❌
- **PnL**: -89.71 points (-1.0R)
- **MFE**: 887.75 points
- **MAE**: 121.25 points

### Trade #1546 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24501.00 - 24505.50
- **Entrée**: 24506.25 @ 2025-09-17 15:28:00
- **Stop Loss**: 24416.54
- **Risk**: 89.71 points
- **TP 1RR**: 24595.96 ✅
- **TP 2RR**: 24685.68 ✅
- **TP 3RR**: 24775.39 ✅
- **TP 4RR**: 24865.11 ✅
- **TP 15RR**: 25851.97 ❌
- **PnL**: -89.71 points (-1.0R)
- **MFE**: 887.75 points
- **MAE**: 121.25 points

### Trade #1547 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24501.00 - 24505.50
- **Entrée**: 24506.25 @ 2025-09-17 15:28:00
- **Stop Loss**: 24416.54
- **Risk**: 89.71 points
- **TP 1RR**: 24595.96 ✅
- **TP 2RR**: 24685.68 ✅
- **TP 3RR**: 24775.39 ✅
- **TP 4RR**: 24865.11 ✅
- **TP 15RR**: 25851.97 ❌
- **PnL**: -89.71 points (-1.0R)
- **MFE**: 887.75 points
- **MAE**: 121.25 points

### Trade #1548 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 14:15:00
- **FVG 5m**: 24501.00 - 24505.50
- **Entrée**: 24506.25 @ 2025-09-17 15:28:00
- **Stop Loss**: 24416.54
- **Risk**: 89.71 points
- **TP 1RR**: 24595.96 ✅
- **TP 2RR**: 24685.68 ✅
- **TP 3RR**: 24775.39 ✅
- **TP 4RR**: 24865.11 ✅
- **TP 15RR**: 25851.97 ❌
- **PnL**: -89.71 points (-1.0R)
- **MFE**: 887.75 points
- **MAE**: 121.25 points

### Trade #1549 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-17 20:00:00
- **FVG 5m**: 24593.00 - 24596.50
- **Entrée**: 24597.00 @ 2025-09-17 21:13:00
- **Stop Loss**: 24548.22
- **Risk**: 48.78 points
- **TP 1RR**: 24645.78 ✅
- **TP 2RR**: 24694.56 ✅
- **TP 3RR**: 24743.34 ✅
- **TP 4RR**: 24792.12 ✅
- **TP 15RR**: 25328.70 ❌
- **PnL**: -48.78 points (-1.0R)
- **MFE**: 430.25 points
- **MAE**: 51.25 points

### Trade #1550 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 07:30:00
- **FVG 5m**: 24716.00 - 24729.75
- **Entrée**: 24713.25 @ 2025-09-18 07:53:00
- **Stop Loss**: 24773.38
- **Risk**: 60.13 points
- **TP 1RR**: 24653.12 ✅
- **TP 2RR**: 24592.99 ❌
- **TP 3RR**: 24532.86 ❌
- **TP 4RR**: 24472.73 ❌
- **TP 15RR**: 23811.29 ❌
- **PnL**: -60.13 points (-1.0R)
- **MFE**: 114.50 points
- **MAE**: 66.00 points

### Trade #1551 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 08:30:00
- **FVG 5m**: 24657.75 - 24666.50
- **Entrée**: 24656.75 @ 2025-09-18 08:49:00
- **Stop Loss**: 24725.61
- **Risk**: 68.86 points
- **TP 1RR**: 24587.89 ❌
- **TP 2RR**: 24519.04 ❌
- **TP 3RR**: 24450.18 ❌
- **TP 4RR**: 24381.32 ❌
- **TP 15RR**: 23623.90 ❌
- **PnL**: -68.86 points (-1.0R)
- **MFE**: 15.25 points
- **MAE**: 73.25 points

### Trade #1552 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 08:30:00
- **FVG 5m**: 24657.75 - 24666.50
- **Entrée**: 24656.75 @ 2025-09-18 08:49:00
- **Stop Loss**: 24725.61
- **Risk**: 68.86 points
- **TP 1RR**: 24587.89 ❌
- **TP 2RR**: 24519.04 ❌
- **TP 3RR**: 24450.18 ❌
- **TP 4RR**: 24381.32 ❌
- **TP 15RR**: 23623.90 ❌
- **PnL**: -68.86 points (-1.0R)
- **MFE**: 15.25 points
- **MAE**: 73.25 points

### Trade #1553 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 08:45:00
- **FVG 5m**: 24698.50 - 24721.75
- **Entrée**: 24722.00 @ 2025-09-18 09:04:00
- **Stop Loss**: 24586.45
- **Risk**: 135.55 points
- **TP 1RR**: 24857.55 ✅
- **TP 2RR**: 24993.10 ✅
- **TP 3RR**: 25128.65 ❌
- **TP 4RR**: 25264.20 ❌
- **TP 15RR**: 26755.24 ❌
- **PnL**: -135.55 points (-1.0R)
- **MFE**: 305.25 points
- **MAE**: 136.75 points

### Trade #1554 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 08:45:00
- **FVG 5m**: 24698.50 - 24721.75
- **Entrée**: 24722.00 @ 2025-09-18 09:04:00
- **Stop Loss**: 24586.45
- **Risk**: 135.55 points
- **TP 1RR**: 24857.55 ✅
- **TP 2RR**: 24993.10 ✅
- **TP 3RR**: 25128.65 ❌
- **TP 4RR**: 25264.20 ❌
- **TP 15RR**: 26755.24 ❌
- **PnL**: -135.55 points (-1.0R)
- **MFE**: 305.25 points
- **MAE**: 136.75 points

### Trade #1555 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-18 09:30:00
- **FVG 5m**: 24777.00 - 24781.00
- **Entrée**: 24772.75 @ 2025-09-18 10:42:00
- **Stop Loss**: 24821.65
- **Risk**: 48.90 points
- **TP 1RR**: 24723.85 ✅
- **TP 2RR**: 24674.94 ✅
- **TP 3RR**: 24626.04 ❌
- **TP 4RR**: 24577.13 ❌
- **TP 15RR**: 24039.18 ❌
- **PnL**: -48.90 points (-1.0R)
- **MFE**: 117.75 points
- **MAE**: 51.75 points

### Trade #1556 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 22:00:00
- **FVG 5m**: 24721.50 - 24730.00
- **Entrée**: 24730.75 @ 2025-09-18 22:11:00
- **Stop Loss**: 24697.65
- **Risk**: 33.10 points
- **TP 1RR**: 24763.85 ❌
- **TP 2RR**: 24796.96 ❌
- **TP 3RR**: 24830.06 ❌
- **TP 4RR**: 24863.17 ❌
- **TP 15RR**: 25227.32 ❌
- **PnL**: -33.10 points (-1.0R)
- **MFE**: 6.75 points
- **MAE**: 36.25 points

### Trade #1557 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 23:15:00
- **FVG 5m**: 24696.00 - 24702.75
- **Entrée**: 24703.00 @ 2025-09-18 23:28:00
- **Stop Loss**: 24669.66
- **Risk**: 33.34 points
- **TP 1RR**: 24736.34 ❌
- **TP 2RR**: 24769.68 ❌
- **TP 3RR**: 24803.02 ❌
- **TP 4RR**: 24836.36 ❌
- **TP 15RR**: 25203.12 ❌
- **PnL**: -33.34 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 33.50 points

### Trade #1558 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-18 23:15:00
- **FVG 5m**: 24696.00 - 24702.75
- **Entrée**: 24703.00 @ 2025-09-18 23:28:00
- **Stop Loss**: 24669.66
- **Risk**: 33.34 points
- **TP 1RR**: 24736.34 ❌
- **TP 2RR**: 24769.68 ❌
- **TP 3RR**: 24803.02 ❌
- **TP 4RR**: 24836.36 ❌
- **TP 15RR**: 25203.12 ❌
- **PnL**: -33.34 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 33.50 points

### Trade #1559 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-19 02:15:00
- **FVG 5m**: 24715.25 - 24719.50
- **Entrée**: 24720.50 @ 2025-09-19 04:23:00
- **Stop Loss**: 24654.42
- **Risk**: 66.08 points
- **TP 1RR**: 24786.58 ✅
- **TP 2RR**: 24852.67 ✅
- **TP 3RR**: 24918.75 ✅
- **TP 4RR**: 24984.83 ✅
- **TP 15RR**: 25711.75 ❌
- **PnL**: -66.08 points (-1.0R)
- **MFE**: 306.75 points
- **MAE**: 66.50 points

### Trade #1560 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-19 02:15:00
- **FVG 5m**: 24715.25 - 24719.50
- **Entrée**: 24720.50 @ 2025-09-19 04:23:00
- **Stop Loss**: 24654.42
- **Risk**: 66.08 points
- **TP 1RR**: 24786.58 ✅
- **TP 2RR**: 24852.67 ✅
- **TP 3RR**: 24918.75 ✅
- **TP 4RR**: 24984.83 ✅
- **TP 15RR**: 25711.75 ❌
- **PnL**: -66.08 points (-1.0R)
- **MFE**: 306.75 points
- **MAE**: 66.50 points

### Trade #1561 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 08:15:00
- **FVG 5m**: 24761.75 - 24765.00
- **Entrée**: 24759.75 @ 2025-09-19 08:32:00
- **Stop Loss**: 24797.14
- **Risk**: 37.39 points
- **TP 1RR**: 24722.36 ❌
- **TP 2RR**: 24684.97 ❌
- **TP 3RR**: 24647.57 ❌
- **TP 4RR**: 24610.18 ❌
- **TP 15RR**: 24198.86 ❌
- **PnL**: -37.39 points (-1.0R)
- **MFE**: 22.25 points
- **MAE**: 42.50 points

### Trade #1562 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 08:45:00
- **FVG 5m**: 24760.75 - 24766.25
- **Entrée**: 24759.00 @ 2025-09-19 09:41:00
- **Stop Loss**: 24829.91
- **Risk**: 70.91 points
- **TP 1RR**: 24688.09 ❌
- **TP 2RR**: 24617.18 ❌
- **TP 3RR**: 24546.27 ❌
- **TP 4RR**: 24475.37 ❌
- **TP 15RR**: 23695.37 ❌
- **PnL**: -70.91 points (-1.0R)
- **MFE**: 51.00 points
- **MAE**: 76.50 points

### Trade #1563 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-19 10:30:00
- **FVG 5m**: 24735.00 - 24744.00
- **Entrée**: 24747.50 @ 2025-09-19 10:43:00
- **Stop Loss**: 24695.65
- **Risk**: 51.85 points
- **TP 1RR**: 24799.35 ✅
- **TP 2RR**: 24851.21 ✅
- **TP 3RR**: 24903.06 ✅
- **TP 4RR**: 24954.92 ✅
- **TP 15RR**: 25525.31 ❌
- **PnL**: -51.85 points (-1.0R)
- **MFE**: 279.75 points
- **MAE**: 53.25 points

### Trade #1564 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-19 12:45:00
- **FVG 5m**: 24816.00 - 24820.00
- **Entrée**: 24814.25 @ 2025-09-19 13:47:00
- **Stop Loss**: 24841.66
- **Risk**: 27.41 points
- **TP 1RR**: 24786.84 ❌
- **TP 2RR**: 24759.42 ❌
- **TP 3RR**: 24732.01 ❌
- **TP 4RR**: 24704.59 ❌
- **TP 15RR**: 24403.03 ❌
- **PnL**: -27.41 points (-1.0R)
- **MFE**: 7.00 points
- **MAE**: 36.25 points

### Trade #1565 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-22 02:00:00
- **FVG 5m**: 24791.25 - 24797.25
- **Entrée**: 24785.50 @ 2025-09-22 02:18:00
- **Stop Loss**: 24843.42
- **Risk**: 57.92 points
- **TP 1RR**: 24727.58 ❌
- **TP 2RR**: 24669.67 ❌
- **TP 3RR**: 24611.75 ❌
- **TP 4RR**: 24553.84 ❌
- **TP 15RR**: 23916.77 ❌
- **PnL**: -57.92 points (-1.0R)
- **MFE**: 36.75 points
- **MAE**: 58.25 points

### Trade #1566 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-22 08:30:00
- **FVG 5m**: 24849.00 - 24855.25
- **Entrée**: 24859.00 @ 2025-09-22 08:48:00
- **Stop Loss**: 24801.84
- **Risk**: 57.16 points
- **TP 1RR**: 24916.16 ✅
- **TP 2RR**: 24973.31 ✅
- **TP 3RR**: 25030.47 ❌
- **TP 4RR**: 25087.63 ❌
- **TP 15RR**: 25716.36 ❌
- **PnL**: -57.16 points (-1.0R)
- **MFE**: 168.25 points
- **MAE**: 78.50 points

### Trade #1567 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-22 08:30:00
- **FVG 5m**: 24849.00 - 24855.25
- **Entrée**: 24859.00 @ 2025-09-22 08:48:00
- **Stop Loss**: 24801.84
- **Risk**: 57.16 points
- **TP 1RR**: 24916.16 ✅
- **TP 2RR**: 24973.31 ✅
- **TP 3RR**: 25030.47 ❌
- **TP 4RR**: 25087.63 ❌
- **TP 15RR**: 25716.36 ❌
- **PnL**: -57.16 points (-1.0R)
- **MFE**: 168.25 points
- **MAE**: 78.50 points

### Trade #1568 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-23 11:00:00
- **FVG 5m**: 24930.75 - 24941.75
- **Entrée**: 24944.25 @ 2025-09-23 11:19:00
- **Stop Loss**: 24902.54
- **Risk**: 41.71 points
- **TP 1RR**: 24985.96 ❌
- **TP 2RR**: 25027.67 ❌
- **TP 3RR**: 25069.37 ❌
- **TP 4RR**: 25111.08 ❌
- **TP 15RR**: 25569.86 ❌
- **PnL**: -41.71 points (-1.0R)
- **MFE**: 10.25 points
- **MAE**: 43.00 points

### Trade #1569 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-23 12:15:00
- **FVG 5m**: 24880.00 - 24895.50
- **Entrée**: 24872.50 @ 2025-09-23 12:27:00
- **Stop Loss**: 24926.21
- **Risk**: 53.71 points
- **TP 1RR**: 24818.79 ✅
- **TP 2RR**: 24765.09 ✅
- **TP 3RR**: 24711.38 ✅
- **TP 4RR**: 24657.67 ✅
- **TP 15RR**: 24066.90 ❌
- **PnL**: -53.71 points (-1.0R)
- **MFE**: 450.00 points
- **MAE**: 58.75 points

### Trade #1570 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-23 12:15:00
- **FVG 5m**: 24880.00 - 24895.50
- **Entrée**: 24872.50 @ 2025-09-23 12:27:00
- **Stop Loss**: 24926.21
- **Risk**: 53.71 points
- **TP 1RR**: 24818.79 ✅
- **TP 2RR**: 24765.09 ✅
- **TP 3RR**: 24711.38 ✅
- **TP 4RR**: 24657.67 ✅
- **TP 15RR**: 24066.90 ❌
- **PnL**: -53.71 points (-1.0R)
- **MFE**: 450.00 points
- **MAE**: 58.75 points

### Trade #1571 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 11:15:00
- **FVG 5m**: 24701.00 - 24714.00
- **Entrée**: 24716.75 @ 2025-09-24 12:09:00
- **Stop Loss**: 24621.18
- **Risk**: 95.57 points
- **TP 1RR**: 24812.32 ❌
- **TP 2RR**: 24907.88 ❌
- **TP 3RR**: 25003.45 ❌
- **TP 4RR**: 25099.02 ❌
- **TP 15RR**: 26150.25 ❌
- **PnL**: -95.57 points (-1.0R)
- **MFE**: 76.75 points
- **MAE**: 96.50 points

### Trade #1572 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 12:00:00
- **FVG 5m**: 24728.00 - 24732.00
- **Entrée**: 24740.75 @ 2025-09-24 12:30:00
- **Stop Loss**: 24670.41
- **Risk**: 70.34 points
- **TP 1RR**: 24811.09 ❌
- **TP 2RR**: 24881.43 ❌
- **TP 3RR**: 24951.77 ❌
- **TP 4RR**: 25022.12 ❌
- **TP 15RR**: 25795.87 ❌
- **PnL**: -70.34 points (-1.0R)
- **MFE**: 52.75 points
- **MAE**: 72.25 points

### Trade #1573 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 12:00:00
- **FVG 5m**: 24728.00 - 24732.00
- **Entrée**: 24740.75 @ 2025-09-24 12:30:00
- **Stop Loss**: 24670.41
- **Risk**: 70.34 points
- **TP 1RR**: 24811.09 ❌
- **TP 2RR**: 24881.43 ❌
- **TP 3RR**: 24951.77 ❌
- **TP 4RR**: 25022.12 ❌
- **TP 15RR**: 25795.87 ❌
- **PnL**: -70.34 points (-1.0R)
- **MFE**: 52.75 points
- **MAE**: 72.25 points

### Trade #1574 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-24 19:00:00
- **FVG 5m**: 24782.75 - 24785.75
- **Entrée**: 24787.50 @ 2025-09-24 20:48:00
- **Stop Loss**: 24740.12
- **Risk**: 47.38 points
- **TP 1RR**: 24834.88 ❌
- **TP 2RR**: 24882.25 ❌
- **TP 3RR**: 24929.63 ❌
- **TP 4RR**: 24977.01 ❌
- **TP 15RR**: 25498.14 ❌
- **PnL**: -47.38 points (-1.0R)
- **MFE**: 6.00 points
- **MAE**: 50.00 points

### Trade #1575 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 02:30:00
- **FVG 5m**: 24740.00 - 24748.25
- **Entrée**: 24751.00 @ 2025-09-25 03:02:00
- **Stop Loss**: 24714.64
- **Risk**: 36.36 points
- **TP 1RR**: 24787.36 ❌
- **TP 2RR**: 24823.73 ❌
- **TP 3RR**: 24860.09 ❌
- **TP 4RR**: 24896.45 ❌
- **TP 15RR**: 25296.45 ❌
- **PnL**: -36.36 points (-1.0R)
- **MFE**: 13.00 points
- **MAE**: 38.00 points

### Trade #1576 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 07:45:00
- **FVG 5m**: 24560.00 - 24576.25
- **Entrée**: 24581.00 @ 2025-09-25 08:19:00
- **Stop Loss**: 24533.48
- **Risk**: 47.52 points
- **TP 1RR**: 24628.52 ❌
- **TP 2RR**: 24676.05 ❌
- **TP 3RR**: 24723.57 ❌
- **TP 4RR**: 24771.09 ❌
- **TP 15RR**: 25293.84 ❌
- **PnL**: -47.52 points (-1.0R)
- **MFE**: 6.00 points
- **MAE**: 49.25 points

### Trade #1577 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 09:00:00
- **FVG 5m**: 24569.25 - 24576.50
- **Entrée**: 24579.25 @ 2025-09-25 09:11:00
- **Stop Loss**: 24432.78
- **Risk**: 146.47 points
- **TP 1RR**: 24725.72 ✅
- **TP 2RR**: 24872.19 ✅
- **TP 3RR**: 25018.67 ✅
- **TP 4RR**: 25165.14 ✅
- **TP 15RR**: 26776.34 ❌
- **PnL**: -146.47 points (-1.0R)
- **MFE**: 814.75 points
- **MAE**: 151.50 points

### Trade #1578 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 09:15:00
- **FVG 5m**: 24624.75 - 24633.75
- **Entrée**: 24638.75 @ 2025-09-25 10:11:00
- **Stop Loss**: 24564.21
- **Risk**: 74.54 points
- **TP 1RR**: 24713.29 ❌
- **TP 2RR**: 24787.83 ❌
- **TP 3RR**: 24862.36 ❌
- **TP 4RR**: 24936.90 ❌
- **TP 15RR**: 25756.82 ❌
- **PnL**: -74.54 points (-1.0R)
- **MFE**: 58.00 points
- **MAE**: 80.50 points

### Trade #1579 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-25 09:30:00
- **FVG 5m**: 24624.75 - 24633.75
- **Entrée**: 24638.75 @ 2025-09-25 10:11:00
- **Stop Loss**: 24596.70
- **Risk**: 42.05 points
- **TP 1RR**: 24680.80 ❌
- **TP 2RR**: 24722.86 ❌
- **TP 3RR**: 24764.91 ❌
- **TP 4RR**: 24806.97 ❌
- **TP 15RR**: 25269.57 ❌
- **PnL**: -42.05 points (-1.0R)
- **MFE**: 16.75 points
- **MAE**: 47.75 points

### Trade #1580 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 03:30:00
- **FVG 5m**: 24623.25 - 24627.75
- **Entrée**: 24620.25 @ 2025-09-26 03:43:00
- **Stop Loss**: 24653.32
- **Risk**: 33.07 points
- **TP 1RR**: 24587.18 ✅
- **TP 2RR**: 24554.11 ❌
- **TP 3RR**: 24521.04 ❌
- **TP 4RR**: 24487.97 ❌
- **TP 15RR**: 24124.19 ❌
- **PnL**: -33.07 points (-1.0R)
- **MFE**: 51.00 points
- **MAE**: 34.50 points

### Trade #1581 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 05:00:00
- **FVG 5m**: 24609.50 - 24612.25
- **Entrée**: 24608.50 @ 2025-09-26 06:17:00
- **Stop Loss**: 24640.31
- **Risk**: 31.81 points
- **TP 1RR**: 24576.69 ❌
- **TP 2RR**: 24544.87 ❌
- **TP 3RR**: 24513.06 ❌
- **TP 4RR**: 24481.24 ❌
- **TP 15RR**: 24131.29 ❌
- **PnL**: -31.81 points (-1.0R)
- **MFE**: 18.00 points
- **MAE**: 34.50 points

### Trade #1582 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 07:45:00
- **FVG 5m**: 24678.25 - 24681.75
- **Entrée**: 24672.75 @ 2025-09-26 08:01:00
- **Stop Loss**: 24738.61
- **Risk**: 65.86 points
- **TP 1RR**: 24606.89 ✅
- **TP 2RR**: 24541.02 ✅
- **TP 3RR**: 24475.16 ❌
- **TP 4RR**: 24409.30 ❌
- **TP 15RR**: 23684.80 ❌
- **PnL**: -65.86 points (-1.0R)
- **MFE**: 152.75 points
- **MAE**: 66.75 points

### Trade #1583 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 08:15:00
- **FVG 5m**: 24636.00 - 24672.50
- **Entrée**: 24618.75 @ 2025-09-26 09:07:00
- **Stop Loss**: 24699.34
- **Risk**: 80.59 points
- **TP 1RR**: 24538.16 ✅
- **TP 2RR**: 24457.56 ❌
- **TP 3RR**: 24376.97 ❌
- **TP 4RR**: 24296.38 ❌
- **TP 15RR**: 23409.85 ❌
- **PnL**: -80.59 points (-1.0R)
- **MFE**: 98.75 points
- **MAE**: 81.25 points

### Trade #1584 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-26 08:15:00
- **FVG 5m**: 24636.00 - 24672.50
- **Entrée**: 24618.75 @ 2025-09-26 09:07:00
- **Stop Loss**: 24699.34
- **Risk**: 80.59 points
- **TP 1RR**: 24538.16 ✅
- **TP 2RR**: 24457.56 ❌
- **TP 3RR**: 24376.97 ❌
- **TP 4RR**: 24296.38 ❌
- **TP 15RR**: 23409.85 ❌
- **PnL**: -80.59 points (-1.0R)
- **MFE**: 98.75 points
- **MAE**: 81.25 points

### Trade #1585 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 09:30:00
- **FVG 5m**: 24603.50 - 24621.25
- **Entrée**: 24623.00 @ 2025-09-26 11:19:00
- **Stop Loss**: 24526.73
- **Risk**: 96.27 points
- **TP 1RR**: 24719.27 ✅
- **TP 2RR**: 24815.54 ✅
- **TP 3RR**: 24911.81 ✅
- **TP 4RR**: 25008.08 ✅
- **TP 15RR**: 26067.04 ❌
- **PnL**: -96.27 points (-1.0R)
- **MFE**: 771.00 points
- **MAE**: 111.00 points

### Trade #1586 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 09:30:00
- **FVG 5m**: 24603.50 - 24621.25
- **Entrée**: 24623.00 @ 2025-09-26 11:19:00
- **Stop Loss**: 24526.73
- **Risk**: 96.27 points
- **TP 1RR**: 24719.27 ✅
- **TP 2RR**: 24815.54 ✅
- **TP 3RR**: 24911.81 ✅
- **TP 4RR**: 25008.08 ✅
- **TP 15RR**: 26067.04 ❌
- **PnL**: -96.27 points (-1.0R)
- **MFE**: 771.00 points
- **MAE**: 111.00 points

### Trade #1587 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-26 09:30:00
- **FVG 5m**: 24603.50 - 24621.25
- **Entrée**: 24623.00 @ 2025-09-26 11:19:00
- **Stop Loss**: 24526.73
- **Risk**: 96.27 points
- **TP 1RR**: 24719.27 ✅
- **TP 2RR**: 24815.54 ✅
- **TP 3RR**: 24911.81 ✅
- **TP 4RR**: 25008.08 ✅
- **TP 15RR**: 26067.04 ❌
- **PnL**: -96.27 points (-1.0R)
- **MFE**: 771.00 points
- **MAE**: 111.00 points

### Trade #1588 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-28 19:00:00
- **FVG 5m**: 24795.00 - 24801.75
- **Entrée**: 24802.75 @ 2025-09-28 19:44:00
- **Stop Loss**: 24752.62
- **Risk**: 50.13 points
- **TP 1RR**: 24852.88 ✅
- **TP 2RR**: 24903.01 ✅
- **TP 3RR**: 24953.15 ✅
- **TP 4RR**: 25003.28 ❌
- **TP 15RR**: 25554.74 ❌
- **PnL**: -50.13 points (-1.0R)
- **MFE**: 172.75 points
- **MAE**: 57.50 points

### Trade #1589 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 01:30:00
- **FVG 5m**: 24842.75 - 24847.75
- **Entrée**: 24848.50 @ 2025-09-29 02:23:00
- **Stop Loss**: 24821.33
- **Risk**: 27.17 points
- **TP 1RR**: 24875.67 ✅
- **TP 2RR**: 24902.83 ✅
- **TP 3RR**: 24930.00 ✅
- **TP 4RR**: 24957.17 ✅
- **TP 15RR**: 25256.00 ❌
- **PnL**: -27.17 points (-1.0R)
- **MFE**: 127.00 points
- **MAE**: 34.25 points

### Trade #1590 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-29 10:00:00
- **FVG 5m**: 24894.25 - 24917.75
- **Entrée**: 24884.25 @ 2025-09-29 10:15:00
- **Stop Loss**: 24955.22
- **Risk**: 70.97 points
- **TP 1RR**: 24813.28 ✅
- **TP 2RR**: 24742.31 ✅
- **TP 3RR**: 24671.34 ✅
- **TP 4RR**: 24600.36 ❌
- **TP 15RR**: 23819.68 ❌
- **PnL**: -70.97 points (-1.0R)
- **MFE**: 251.00 points
- **MAE**: 73.50 points

### Trade #1591 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-29 10:00:00
- **FVG 5m**: 24894.25 - 24917.75
- **Entrée**: 24884.25 @ 2025-09-29 10:15:00
- **Stop Loss**: 24955.22
- **Risk**: 70.97 points
- **TP 1RR**: 24813.28 ✅
- **TP 2RR**: 24742.31 ✅
- **TP 3RR**: 24671.34 ✅
- **TP 4RR**: 24600.36 ❌
- **TP 15RR**: 23819.68 ❌
- **PnL**: -70.97 points (-1.0R)
- **MFE**: 251.00 points
- **MAE**: 73.50 points

### Trade #1592 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-29 10:00:00
- **FVG 5m**: 24894.25 - 24917.75
- **Entrée**: 24884.25 @ 2025-09-29 10:15:00
- **Stop Loss**: 24955.22
- **Risk**: 70.97 points
- **TP 1RR**: 24813.28 ✅
- **TP 2RR**: 24742.31 ✅
- **TP 3RR**: 24671.34 ✅
- **TP 4RR**: 24600.36 ❌
- **TP 15RR**: 23819.68 ❌
- **PnL**: -70.97 points (-1.0R)
- **MFE**: 251.00 points
- **MAE**: 73.50 points

### Trade #1593 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 10:30:00
- **FVG 5m**: 24834.00 - 24838.75
- **Entrée**: 24846.50 @ 2025-09-29 12:52:00
- **Stop Loss**: 24827.33
- **Risk**: 19.17 points
- **TP 1RR**: 24865.67 ✅
- **TP 2RR**: 24884.84 ❌
- **TP 3RR**: 24904.01 ❌
- **TP 4RR**: 24923.18 ❌
- **TP 15RR**: 25134.05 ❌
- **PnL**: -19.17 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 21.50 points

### Trade #1594 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 10:45:00
- **FVG 5m**: 24834.00 - 24838.75
- **Entrée**: 24846.50 @ 2025-09-29 12:52:00
- **Stop Loss**: 24818.33
- **Risk**: 28.17 points
- **TP 1RR**: 24874.67 ❌
- **TP 2RR**: 24902.83 ❌
- **TP 3RR**: 24931.00 ❌
- **TP 4RR**: 24959.16 ❌
- **TP 15RR**: 25268.98 ❌
- **PnL**: -28.17 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 33.00 points

### Trade #1595 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 12:00:00
- **FVG 5m**: 24834.00 - 24838.75
- **Entrée**: 24846.50 @ 2025-09-29 12:52:00
- **Stop Loss**: 24787.85
- **Risk**: 58.65 points
- **TP 1RR**: 24905.15 ❌
- **TP 2RR**: 24963.80 ❌
- **TP 3RR**: 25022.45 ❌
- **TP 4RR**: 25081.10 ❌
- **TP 15RR**: 25726.25 ❌
- **PnL**: -58.65 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 66.00 points

### Trade #1596 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-29 14:15:00
- **FVG 5m**: 24813.75 - 24816.75
- **Entrée**: 24818.75 @ 2025-09-29 14:38:00
- **Stop Loss**: 24768.11
- **Risk**: 50.64 points
- **TP 1RR**: 24869.39 ❌
- **TP 2RR**: 24920.03 ❌
- **TP 3RR**: 24970.67 ❌
- **TP 4RR**: 25021.31 ❌
- **TP 15RR**: 25578.35 ❌
- **PnL**: -50.64 points (-1.0R)
- **MFE**: 38.00 points
- **MAE**: 64.00 points

### Trade #1597 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 01:30:00
- **FVG 5m**: 24831.75 - 24834.25
- **Entrée**: 24831.00 @ 2025-09-30 01:48:00
- **Stop Loss**: 24867.93
- **Risk**: 36.93 points
- **TP 1RR**: 24794.07 ✅
- **TP 2RR**: 24757.14 ✅
- **TP 3RR**: 24720.22 ❌
- **TP 4RR**: 24683.29 ❌
- **TP 15RR**: 24277.08 ❌
- **PnL**: -36.93 points (-1.0R)
- **MFE**: 108.75 points
- **MAE**: 46.00 points

### Trade #1598 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 02:45:00
- **FVG 5m**: 24801.25 - 24805.00
- **Entrée**: 24814.50 @ 2025-09-30 04:30:00
- **Stop Loss**: 24748.62
- **Risk**: 65.88 points
- **TP 1RR**: 24880.38 ❌
- **TP 2RR**: 24946.26 ❌
- **TP 3RR**: 25012.14 ❌
- **TP 4RR**: 25078.02 ❌
- **TP 15RR**: 25802.71 ❌
- **PnL**: -65.88 points (-1.0R)
- **MFE**: 30.50 points
- **MAE**: 69.25 points

### Trade #1599 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 04:30:00
- **FVG 5m**: 24796.50 - 24803.00
- **Entrée**: 24794.00 @ 2025-09-30 05:13:00
- **Stop Loss**: 24832.66
- **Risk**: 38.66 points
- **TP 1RR**: 24755.34 ❌
- **TP 2RR**: 24716.68 ❌
- **TP 3RR**: 24678.02 ❌
- **TP 4RR**: 24639.36 ❌
- **TP 15RR**: 24214.10 ❌
- **PnL**: -38.66 points (-1.0R)
- **MFE**: 20.00 points
- **MAE**: 41.50 points

### Trade #1600 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 07:15:00
- **FVG 5m**: 24823.50 - 24831.50
- **Entrée**: 24834.75 @ 2025-09-30 07:39:00
- **Stop Loss**: 24776.61
- **Risk**: 58.14 points
- **TP 1RR**: 24892.89 ❌
- **TP 2RR**: 24951.04 ❌
- **TP 3RR**: 25009.18 ❌
- **TP 4RR**: 25067.33 ❌
- **TP 15RR**: 25706.92 ❌
- **PnL**: -58.14 points (-1.0R)
- **MFE**: 10.25 points
- **MAE**: 63.75 points

### Trade #1601 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 07:15:00
- **FVG 5m**: 24823.50 - 24831.50
- **Entrée**: 24834.75 @ 2025-09-30 07:39:00
- **Stop Loss**: 24776.61
- **Risk**: 58.14 points
- **TP 1RR**: 24892.89 ❌
- **TP 2RR**: 24951.04 ❌
- **TP 3RR**: 25009.18 ❌
- **TP 4RR**: 25067.33 ❌
- **TP 15RR**: 25706.92 ❌
- **PnL**: -58.14 points (-1.0R)
- **MFE**: 10.25 points
- **MAE**: 63.75 points

### Trade #1602 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 08:30:00
- **FVG 5m**: 24795.25 - 24817.75
- **Entrée**: 24832.50 @ 2025-09-30 09:48:00
- **Stop Loss**: 24729.13
- **Risk**: 103.37 points
- **TP 1RR**: 24935.87 ❌
- **TP 2RR**: 25039.24 ❌
- **TP 3RR**: 25142.61 ❌
- **TP 4RR**: 25245.98 ❌
- **TP 15RR**: 26383.06 ❌
- **PnL**: -103.37 points (-1.0R)
- **MFE**: 81.25 points
- **MAE**: 104.50 points

### Trade #1603 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 08:30:00
- **FVG 5m**: 24795.25 - 24817.75
- **Entrée**: 24832.50 @ 2025-09-30 09:48:00
- **Stop Loss**: 24729.13
- **Risk**: 103.37 points
- **TP 1RR**: 24935.87 ❌
- **TP 2RR**: 25039.24 ❌
- **TP 3RR**: 25142.61 ❌
- **TP 4RR**: 25245.98 ❌
- **TP 15RR**: 26383.06 ❌
- **PnL**: -103.37 points (-1.0R)
- **MFE**: 81.25 points
- **MAE**: 104.50 points

### Trade #1604 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 08:30:00
- **FVG 5m**: 24795.25 - 24817.75
- **Entrée**: 24832.50 @ 2025-09-30 09:48:00
- **Stop Loss**: 24729.13
- **Risk**: 103.37 points
- **TP 1RR**: 24935.87 ❌
- **TP 2RR**: 25039.24 ❌
- **TP 3RR**: 25142.61 ❌
- **TP 4RR**: 25245.98 ❌
- **TP 15RR**: 26383.06 ❌
- **PnL**: -103.37 points (-1.0R)
- **MFE**: 81.25 points
- **MAE**: 104.50 points

### Trade #1605 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 08:30:00
- **FVG 5m**: 24795.25 - 24817.75
- **Entrée**: 24832.50 @ 2025-09-30 09:48:00
- **Stop Loss**: 24729.13
- **Risk**: 103.37 points
- **TP 1RR**: 24935.87 ❌
- **TP 2RR**: 25039.24 ❌
- **TP 3RR**: 25142.61 ❌
- **TP 4RR**: 25245.98 ❌
- **TP 15RR**: 26383.06 ❌
- **PnL**: -103.37 points (-1.0R)
- **MFE**: 81.25 points
- **MAE**: 104.50 points

### Trade #1606 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-09-30 09:45:00
- **FVG 5m**: 24835.50 - 24839.25
- **Entrée**: 24841.75 @ 2025-09-30 09:58:00
- **Stop Loss**: 24778.35
- **Risk**: 63.40 points
- **TP 1RR**: 24905.15 ❌
- **TP 2RR**: 24968.54 ❌
- **TP 3RR**: 25031.94 ❌
- **TP 4RR**: 25095.33 ❌
- **TP 15RR**: 25792.68 ❌
- **PnL**: -63.40 points (-1.0R)
- **MFE**: 21.00 points
- **MAE**: 86.25 points

### Trade #1607 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 10:00:00
- **FVG 5m**: 24833.75 - 24838.25
- **Entrée**: 24828.00 @ 2025-09-30 10:14:00
- **Stop Loss**: 24875.18
- **Risk**: 47.18 points
- **TP 1RR**: 24780.82 ✅
- **TP 2RR**: 24733.64 ✅
- **TP 3RR**: 24686.46 ❌
- **TP 4RR**: 24639.27 ❌
- **TP 15RR**: 24120.28 ❌
- **PnL**: -47.18 points (-1.0R)
- **MFE**: 96.25 points
- **MAE**: 49.00 points

### Trade #1608 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 10:15:00
- **FVG 5m**: 24787.00 - 24791.25
- **Entrée**: 24779.25 @ 2025-09-30 11:58:00
- **Stop Loss**: 24846.17
- **Risk**: 66.92 points
- **TP 1RR**: 24712.33 ❌
- **TP 2RR**: 24645.42 ❌
- **TP 3RR**: 24578.50 ❌
- **TP 4RR**: 24511.58 ❌
- **TP 15RR**: 23775.50 ❌
- **PnL**: -66.92 points (-1.0R)
- **MFE**: 47.50 points
- **MAE**: 68.00 points

### Trade #1609 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 12:15:00
- **FVG 5m**: 24773.00 - 24775.75
- **Entrée**: 24772.50 @ 2025-09-30 12:58:00
- **Stop Loss**: 24788.64
- **Risk**: 16.14 points
- **TP 1RR**: 24756.36 ❌
- **TP 2RR**: 24740.22 ❌
- **TP 3RR**: 24724.09 ❌
- **TP 4RR**: 24707.95 ❌
- **TP 15RR**: 24530.43 ❌
- **PnL**: -16.14 points (-1.0R)
- **MFE**: 10.50 points
- **MAE**: 18.00 points

### Trade #1610 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 12:15:00
- **FVG 5m**: 24773.00 - 24775.75
- **Entrée**: 24772.50 @ 2025-09-30 12:58:00
- **Stop Loss**: 24788.64
- **Risk**: 16.14 points
- **TP 1RR**: 24756.36 ❌
- **TP 2RR**: 24740.22 ❌
- **TP 3RR**: 24724.09 ❌
- **TP 4RR**: 24707.95 ❌
- **TP 15RR**: 24530.43 ❌
- **PnL**: -16.14 points (-1.0R)
- **MFE**: 10.50 points
- **MAE**: 18.00 points

### Trade #1611 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 14:30:00
- **FVG 5m**: 24878.00 - 24892.00
- **Entrée**: 24876.00 @ 2025-09-30 15:03:00
- **Stop Loss**: 24890.69
- **Risk**: 14.69 points
- **TP 1RR**: 24861.31 ✅
- **TP 2RR**: 24846.62 ✅
- **TP 3RR**: 24831.93 ✅
- **TP 4RR**: 24817.24 ✅
- **TP 15RR**: 24655.66 ✅
- **PnL**: 220.34 points (15.0R)
- **MFE**: 221.75 points
- **MAE**: 2.00 points

### Trade #1612 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 14:30:00
- **FVG 5m**: 24878.00 - 24892.00
- **Entrée**: 24876.00 @ 2025-09-30 15:03:00
- **Stop Loss**: 24890.69
- **Risk**: 14.69 points
- **TP 1RR**: 24861.31 ✅
- **TP 2RR**: 24846.62 ✅
- **TP 3RR**: 24831.93 ✅
- **TP 4RR**: 24817.24 ✅
- **TP 15RR**: 24655.66 ✅
- **PnL**: 220.34 points (15.0R)
- **MFE**: 221.75 points
- **MAE**: 2.00 points

### Trade #1613 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 14:30:00
- **FVG 5m**: 24878.00 - 24892.00
- **Entrée**: 24876.00 @ 2025-09-30 15:03:00
- **Stop Loss**: 24890.69
- **Risk**: 14.69 points
- **TP 1RR**: 24861.31 ✅
- **TP 2RR**: 24846.62 ✅
- **TP 3RR**: 24831.93 ✅
- **TP 4RR**: 24817.24 ✅
- **TP 15RR**: 24655.66 ✅
- **PnL**: 220.34 points (15.0R)
- **MFE**: 221.75 points
- **MAE**: 2.00 points

### Trade #1614 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-09-30 15:00:00
- **FVG 5m**: 24848.00 - 24852.75
- **Entrée**: 24845.25 @ 2025-09-30 15:34:00
- **Stop Loss**: 24913.70
- **Risk**: 68.45 points
- **TP 1RR**: 24776.80 ✅
- **TP 2RR**: 24708.35 ✅
- **TP 3RR**: 24639.90 ✅
- **TP 4RR**: 24571.45 ❌
- **TP 15RR**: 23818.49 ❌
- **PnL**: -68.45 points (-1.0R)
- **MFE**: 212.00 points
- **MAE**: 75.50 points

### Trade #1615 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 01:30:00
- **FVG 5m**: 24730.50 - 24745.25
- **Entrée**: 24729.00 @ 2025-10-01 01:44:00
- **Stop Loss**: 24765.63
- **Risk**: 36.63 points
- **TP 1RR**: 24692.37 ✅
- **TP 2RR**: 24655.75 ✅
- **TP 3RR**: 24619.12 ❌
- **TP 4RR**: 24582.49 ❌
- **TP 15RR**: 24179.60 ❌
- **PnL**: -36.63 points (-1.0R)
- **MFE**: 95.75 points
- **MAE**: 37.00 points

### Trade #1616 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 01:30:00
- **FVG 5m**: 24730.50 - 24745.25
- **Entrée**: 24729.00 @ 2025-10-01 01:44:00
- **Stop Loss**: 24765.63
- **Risk**: 36.63 points
- **TP 1RR**: 24692.37 ✅
- **TP 2RR**: 24655.75 ✅
- **TP 3RR**: 24619.12 ❌
- **TP 4RR**: 24582.49 ❌
- **TP 15RR**: 24179.60 ❌
- **PnL**: -36.63 points (-1.0R)
- **MFE**: 95.75 points
- **MAE**: 37.00 points

### Trade #1617 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 03:30:00
- **FVG 5m**: 24723.75 - 24732.75
- **Entrée**: 24737.50 @ 2025-10-01 04:08:00
- **Stop Loss**: 24665.66
- **Risk**: 71.84 points
- **TP 1RR**: 24809.34 ✅
- **TP 2RR**: 24881.18 ✅
- **TP 3RR**: 24953.02 ✅
- **TP 4RR**: 25024.86 ✅
- **TP 15RR**: 25815.08 ❌
- **PnL**: -71.84 points (-1.0R)
- **MFE**: 656.50 points
- **MAE**: 74.00 points

### Trade #1618 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 03:30:00
- **FVG 5m**: 24723.75 - 24732.75
- **Entrée**: 24737.50 @ 2025-10-01 04:08:00
- **Stop Loss**: 24665.66
- **Risk**: 71.84 points
- **TP 1RR**: 24809.34 ✅
- **TP 2RR**: 24881.18 ✅
- **TP 3RR**: 24953.02 ✅
- **TP 4RR**: 25024.86 ✅
- **TP 15RR**: 25815.08 ❌
- **PnL**: -71.84 points (-1.0R)
- **MFE**: 656.50 points
- **MAE**: 74.00 points

### Trade #1619 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 04:00:00
- **FVG 5m**: 24742.00 - 24744.50
- **Entrée**: 24745.25 @ 2025-10-01 04:23:00
- **Stop Loss**: 24701.39
- **Risk**: 43.86 points
- **TP 1RR**: 24789.11 ✅
- **TP 2RR**: 24832.96 ✅
- **TP 3RR**: 24876.82 ✅
- **TP 4RR**: 24920.68 ✅
- **TP 15RR**: 25403.10 ❌
- **PnL**: -43.86 points (-1.0R)
- **MFE**: 648.75 points
- **MAE**: 51.25 points

### Trade #1620 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 04:30:00
- **FVG 5m**: 24742.75 - 24746.75
- **Entrée**: 24742.25 @ 2025-10-01 05:29:00
- **Stop Loss**: 24774.63
- **Risk**: 32.38 points
- **TP 1RR**: 24709.87 ❌
- **TP 2RR**: 24677.49 ❌
- **TP 3RR**: 24645.11 ❌
- **TP 4RR**: 24612.73 ❌
- **TP 15RR**: 24256.53 ❌
- **PnL**: -32.38 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 33.50 points

### Trade #1621 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 08:15:00
- **FVG 5m**: 24781.75 - 24803.25
- **Entrée**: 24773.50 @ 2025-10-01 08:48:00
- **Stop Loss**: 24803.65
- **Risk**: 30.15 points
- **TP 1RR**: 24743.35 ✅
- **TP 2RR**: 24713.21 ❌
- **TP 3RR**: 24683.06 ❌
- **TP 4RR**: 24652.92 ❌
- **TP 15RR**: 24321.32 ❌
- **PnL**: -30.15 points (-1.0R)
- **MFE**: 47.50 points
- **MAE**: 34.50 points

### Trade #1622 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 08:15:00
- **FVG 5m**: 24781.75 - 24803.25
- **Entrée**: 24773.50 @ 2025-10-01 08:48:00
- **Stop Loss**: 24803.65
- **Risk**: 30.15 points
- **TP 1RR**: 24743.35 ✅
- **TP 2RR**: 24713.21 ❌
- **TP 3RR**: 24683.06 ❌
- **TP 4RR**: 24652.92 ❌
- **TP 15RR**: 24321.32 ❌
- **PnL**: -30.15 points (-1.0R)
- **MFE**: 47.50 points
- **MAE**: 34.50 points

### Trade #1623 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 08:30:00
- **FVG 5m**: 24823.25 - 24825.75
- **Entrée**: 24828.00 @ 2025-10-01 09:13:00
- **Stop Loss**: 24730.38
- **Risk**: 97.62 points
- **TP 1RR**: 24925.62 ✅
- **TP 2RR**: 25023.24 ✅
- **TP 3RR**: 25120.86 ✅
- **TP 4RR**: 25218.49 ✅
- **TP 15RR**: 26292.32 ❌
- **PnL**: -97.62 points (-1.0R)
- **MFE**: 566.00 points
- **MAE**: 134.00 points

### Trade #1624 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 12:15:00
- **FVG 5m**: 24986.00 - 24993.50
- **Entrée**: 25000.00 @ 2025-10-01 13:05:00
- **Stop Loss**: 24955.52
- **Risk**: 44.48 points
- **TP 1RR**: 25044.48 ✅
- **TP 2RR**: 25088.97 ✅
- **TP 3RR**: 25133.45 ✅
- **TP 4RR**: 25177.94 ✅
- **TP 15RR**: 25667.26 ❌
- **PnL**: -44.48 points (-1.0R)
- **MFE**: 196.50 points
- **MAE**: 48.50 points

### Trade #1625 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 12:45:00
- **FVG 5m**: 24986.00 - 24993.50
- **Entrée**: 25000.00 @ 2025-10-01 13:05:00
- **Stop Loss**: 24952.52
- **Risk**: 47.48 points
- **TP 1RR**: 25047.48 ✅
- **TP 2RR**: 25094.96 ✅
- **TP 3RR**: 25142.45 ✅
- **TP 4RR**: 25189.93 ✅
- **TP 15RR**: 25712.24 ❌
- **PnL**: -47.48 points (-1.0R)
- **MFE**: 196.50 points
- **MAE**: 48.50 points

### Trade #1626 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-01 12:45:00
- **FVG 5m**: 24986.00 - 24993.50
- **Entrée**: 25000.00 @ 2025-10-01 13:05:00
- **Stop Loss**: 24952.52
- **Risk**: 47.48 points
- **TP 1RR**: 25047.48 ✅
- **TP 2RR**: 25094.96 ✅
- **TP 3RR**: 25142.45 ✅
- **TP 4RR**: 25189.93 ✅
- **TP 15RR**: 25712.24 ❌
- **PnL**: -47.48 points (-1.0R)
- **MFE**: 196.50 points
- **MAE**: 48.50 points

### Trade #1627 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 14:30:00
- **FVG 5m**: 25000.75 - 25010.75
- **Entrée**: 24999.25 @ 2025-10-01 15:01:00
- **Stop Loss**: 25048.02
- **Risk**: 48.77 points
- **TP 1RR**: 24950.48 ❌
- **TP 2RR**: 24901.71 ❌
- **TP 3RR**: 24852.95 ❌
- **TP 4RR**: 24804.18 ❌
- **TP 15RR**: 24267.73 ❌
- **PnL**: -48.77 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 52.00 points

### Trade #1628 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 14:30:00
- **FVG 5m**: 25000.75 - 25010.75
- **Entrée**: 24999.25 @ 2025-10-01 15:01:00
- **Stop Loss**: 25048.02
- **Risk**: 48.77 points
- **TP 1RR**: 24950.48 ❌
- **TP 2RR**: 24901.71 ❌
- **TP 3RR**: 24852.95 ❌
- **TP 4RR**: 24804.18 ❌
- **TP 15RR**: 24267.73 ❌
- **PnL**: -48.77 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 52.00 points

### Trade #1629 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-01 14:30:00
- **FVG 5m**: 25000.75 - 25010.75
- **Entrée**: 24999.25 @ 2025-10-01 15:01:00
- **Stop Loss**: 25048.02
- **Risk**: 48.77 points
- **TP 1RR**: 24950.48 ❌
- **TP 2RR**: 24901.71 ❌
- **TP 3RR**: 24852.95 ❌
- **TP 4RR**: 24804.18 ❌
- **TP 15RR**: 24267.73 ❌
- **PnL**: -48.77 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 52.00 points

### Trade #1630 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-02 08:30:00
- **FVG 5m**: 25071.50 - 25076.25
- **Entrée**: 25069.25 @ 2025-10-02 08:46:00
- **Stop Loss**: 25181.58
- **Risk**: 112.33 points
- **TP 1RR**: 24956.92 ❌
- **TP 2RR**: 24844.58 ❌
- **TP 3RR**: 24732.25 ❌
- **TP 4RR**: 24619.91 ❌
- **TP 15RR**: 23384.23 ❌
- **PnL**: -112.33 points (-1.0R)
- **MFE**: 75.50 points
- **MAE**: 113.25 points

### Trade #1631 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 08:45:00
- **FVG 5m**: 25038.50 - 25061.50
- **Entrée**: 25062.75 @ 2025-10-02 10:54:00
- **Stop Loss**: 25001.49
- **Risk**: 61.26 points
- **TP 1RR**: 25124.01 ✅
- **TP 2RR**: 25185.26 ✅
- **TP 3RR**: 25246.52 ❌
- **TP 4RR**: 25307.78 ❌
- **TP 15RR**: 25981.61 ❌
- **PnL**: -61.26 points (-1.0R)
- **MFE**: 133.75 points
- **MAE**: 79.25 points

### Trade #1632 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 08:45:00
- **FVG 5m**: 25038.50 - 25061.50
- **Entrée**: 25062.75 @ 2025-10-02 10:54:00
- **Stop Loss**: 25001.49
- **Risk**: 61.26 points
- **TP 1RR**: 25124.01 ✅
- **TP 2RR**: 25185.26 ✅
- **TP 3RR**: 25246.52 ❌
- **TP 4RR**: 25307.78 ❌
- **TP 15RR**: 25981.61 ❌
- **PnL**: -61.26 points (-1.0R)
- **MFE**: 133.75 points
- **MAE**: 79.25 points

### Trade #1633 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 10:45:00
- **FVG 5m**: 25063.75 - 25069.75
- **Entrée**: 25071.00 @ 2025-10-02 11:52:00
- **Stop Loss**: 25003.49
- **Risk**: 67.51 points
- **TP 1RR**: 25138.51 ✅
- **TP 2RR**: 25206.02 ❌
- **TP 3RR**: 25273.52 ❌
- **TP 4RR**: 25341.03 ❌
- **TP 15RR**: 26083.62 ❌
- **PnL**: -67.51 points (-1.0R)
- **MFE**: 125.50 points
- **MAE**: 69.25 points

### Trade #1634 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-02 17:30:00
- **FVG 5m**: 25085.50 - 25091.25
- **Entrée**: 25092.25 @ 2025-10-02 17:42:00
- **Stop Loss**: 25060.46
- **Risk**: 31.79 points
- **TP 1RR**: 25124.04 ✅
- **TP 2RR**: 25155.82 ✅
- **TP 3RR**: 25187.61 ✅
- **TP 4RR**: 25219.40 ❌
- **TP 15RR**: 25569.05 ❌
- **PnL**: -31.79 points (-1.0R)
- **MFE**: 104.25 points
- **MAE**: 33.75 points

### Trade #1635 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 06:30:00
- **FVG 5m**: 25148.00 - 25153.25
- **Entrée**: 25155.75 @ 2025-10-03 06:43:00
- **Stop Loss**: 25118.68
- **Risk**: 37.07 points
- **TP 1RR**: 25192.82 ❌
- **TP 2RR**: 25229.88 ❌
- **TP 3RR**: 25266.95 ❌
- **TP 4RR**: 25304.01 ❌
- **TP 15RR**: 25711.73 ❌
- **PnL**: -37.07 points (-1.0R)
- **MFE**: 8.00 points
- **MAE**: 42.00 points

### Trade #1636 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-03 07:30:00
- **FVG 5m**: 25117.75 - 25122.00
- **Entrée**: 25114.25 @ 2025-10-03 07:44:00
- **Stop Loss**: 25158.07
- **Risk**: 43.82 points
- **TP 1RR**: 25070.43 ❌
- **TP 2RR**: 25026.60 ❌
- **TP 3RR**: 24982.78 ❌
- **TP 4RR**: 24938.96 ❌
- **TP 15RR**: 24456.91 ❌
- **PnL**: -43.82 points (-1.0R)
- **MFE**: 11.25 points
- **MAE**: 45.50 points

### Trade #1637 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 09:00:00
- **FVG 5m**: 25099.75 - 25105.25
- **Entrée**: 25110.50 @ 2025-10-03 09:37:00
- **Stop Loss**: 25038.47
- **Risk**: 72.03 points
- **TP 1RR**: 25182.53 ❌
- **TP 2RR**: 25254.55 ❌
- **TP 3RR**: 25326.58 ❌
- **TP 4RR**: 25398.60 ❌
- **TP 15RR**: 26190.88 ❌
- **PnL**: -72.03 points (-1.0R)
- **MFE**: 45.50 points
- **MAE**: 79.75 points

### Trade #1638 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-03 12:45:00
- **FVG 5m**: 24998.25 - 25001.00
- **Entrée**: 24987.00 @ 2025-10-03 13:49:00
- **Stop Loss**: 25028.26
- **Risk**: 41.26 points
- **TP 1RR**: 24945.74 ❌
- **TP 2RR**: 24904.48 ❌
- **TP 3RR**: 24863.23 ❌
- **TP 4RR**: 24821.97 ❌
- **TP 15RR**: 24368.13 ❌
- **PnL**: -41.26 points (-1.0R)
- **MFE**: 8.00 points
- **MAE**: 42.75 points

### Trade #1639 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-03 12:45:00
- **FVG 5m**: 24957.50 - 24970.50
- **Entrée**: 24980.75 @ 2025-10-03 13:11:00
- **Stop Loss**: 24910.79
- **Risk**: 69.96 points
- **TP 1RR**: 25050.71 ✅
- **TP 2RR**: 25120.67 ✅
- **TP 3RR**: 25190.63 ✅
- **TP 4RR**: 25260.60 ✅
- **TP 15RR**: 26030.17 ❌
- **PnL**: -69.96 points (-1.0R)
- **MFE**: 413.25 points
- **MAE**: 72.00 points

### Trade #1640 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 00:00:00
- **FVG 5m**: 25090.75 - 25097.25
- **Entrée**: 25088.25 @ 2025-10-06 02:24:00
- **Stop Loss**: 25115.30
- **Risk**: 27.05 points
- **TP 1RR**: 25061.20 ✅
- **TP 2RR**: 25034.15 ❌
- **TP 3RR**: 25007.10 ❌
- **TP 4RR**: 24980.04 ❌
- **TP 15RR**: 24682.48 ❌
- **PnL**: -27.05 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 28.00 points

### Trade #1641 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-06 02:30:00
- **FVG 5m**: 25076.00 - 25079.00
- **Entrée**: 25079.50 @ 2025-10-06 02:51:00
- **Stop Loss**: 25032.98
- **Risk**: 46.52 points
- **TP 1RR**: 25126.02 ✅
- **TP 2RR**: 25172.55 ✅
- **TP 3RR**: 25219.07 ✅
- **TP 4RR**: 25265.59 ✅
- **TP 15RR**: 25777.34 ❌
- **PnL**: -46.52 points (-1.0R)
- **MFE**: 195.50 points
- **MAE**: 51.75 points

### Trade #1642 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-06 02:45:00
- **FVG 5m**: 25093.25 - 25097.25
- **Entrée**: 25106.75 @ 2025-10-06 03:05:00
- **Stop Loss**: 25054.47
- **Risk**: 52.28 points
- **TP 1RR**: 25159.03 ✅
- **TP 2RR**: 25211.32 ✅
- **TP 3RR**: 25263.60 ✅
- **TP 4RR**: 25315.88 ❌
- **TP 15RR**: 25891.00 ❌
- **PnL**: -52.28 points (-1.0R)
- **MFE**: 168.25 points
- **MAE**: 53.75 points

### Trade #1643 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 07:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25226.61
- **Risk**: 75.36 points
- **TP 1RR**: 25075.89 ❌
- **TP 2RR**: 25000.54 ❌
- **TP 3RR**: 24925.18 ❌
- **TP 4RR**: 24849.82 ❌
- **TP 15RR**: 24020.90 ❌
- **PnL**: -75.36 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 78.75 points

### Trade #1644 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 07:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25226.61
- **Risk**: 75.36 points
- **TP 1RR**: 25075.89 ❌
- **TP 2RR**: 25000.54 ❌
- **TP 3RR**: 24925.18 ❌
- **TP 4RR**: 24849.82 ❌
- **TP 15RR**: 24020.90 ❌
- **PnL**: -75.36 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 78.75 points

### Trade #1645 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 08:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25234.36
- **Risk**: 83.11 points
- **TP 1RR**: 25068.14 ❌
- **TP 2RR**: 24985.03 ❌
- **TP 3RR**: 24901.92 ❌
- **TP 4RR**: 24818.81 ❌
- **TP 15RR**: 23904.59 ❌
- **PnL**: -83.11 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 85.00 points

### Trade #1646 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 08:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25234.36
- **Risk**: 83.11 points
- **TP 1RR**: 25068.14 ❌
- **TP 2RR**: 24985.03 ❌
- **TP 3RR**: 24901.92 ❌
- **TP 4RR**: 24818.81 ❌
- **TP 15RR**: 23904.59 ❌
- **PnL**: -83.11 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 85.00 points

### Trade #1647 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 08:30:00
- **FVG 5m**: 25151.75 - 25155.25
- **Entrée**: 25151.25 @ 2025-10-06 09:27:00
- **Stop Loss**: 25234.36
- **Risk**: 83.11 points
- **TP 1RR**: 25068.14 ❌
- **TP 2RR**: 24985.03 ❌
- **TP 3RR**: 24901.92 ❌
- **TP 4RR**: 24818.81 ❌
- **TP 15RR**: 23904.59 ❌
- **PnL**: -83.11 points (-1.0R)
- **MFE**: 42.75 points
- **MAE**: 85.00 points

### Trade #1648 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-06 14:30:00
- **FVG 5m**: 25213.50 - 25217.25
- **Entrée**: 25212.50 @ 2025-10-06 14:42:00
- **Stop Loss**: 25242.11
- **Risk**: 29.61 points
- **TP 1RR**: 25182.89 ✅
- **TP 2RR**: 25153.27 ✅
- **TP 3RR**: 25123.66 ✅
- **TP 4RR**: 25094.04 ❌
- **TP 15RR**: 24768.28 ❌
- **PnL**: -29.61 points (-1.0R)
- **MFE**: 90.00 points
- **MAE**: 35.00 points

### Trade #1649 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 08:00:00
- **FVG 5m**: 25246.50 - 25260.25
- **Entrée**: 25243.75 @ 2025-10-07 08:14:00
- **Stop Loss**: 25287.64
- **Risk**: 43.89 points
- **TP 1RR**: 25199.86 ✅
- **TP 2RR**: 25155.97 ✅
- **TP 3RR**: 25112.09 ✅
- **TP 4RR**: 25068.20 ✅
- **TP 15RR**: 24585.44 ❌
- **PnL**: -43.89 points (-1.0R)
- **MFE**: 259.00 points
- **MAE**: 47.00 points

### Trade #1650 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 08:45:00
- **FVG 5m**: 25147.25 - 25172.25
- **Entrée**: 25144.50 @ 2025-10-07 10:04:00
- **Stop Loss**: 25277.38
- **Risk**: 132.88 points
- **TP 1RR**: 25011.62 ✅
- **TP 2RR**: 24878.74 ❌
- **TP 3RR**: 24745.85 ❌
- **TP 4RR**: 24612.97 ❌
- **TP 15RR**: 23151.26 ❌
- **PnL**: -132.88 points (-1.0R)
- **MFE**: 159.75 points
- **MAE**: 146.25 points

### Trade #1651 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 09:45:00
- **FVG 5m**: 25147.25 - 25172.25
- **Entrée**: 25144.50 @ 2025-10-07 10:04:00
- **Stop Loss**: 25223.36
- **Risk**: 78.86 points
- **TP 1RR**: 25065.64 ✅
- **TP 2RR**: 24986.79 ✅
- **TP 3RR**: 24907.93 ❌
- **TP 4RR**: 24829.08 ❌
- **TP 15RR**: 23961.67 ❌
- **PnL**: -78.86 points (-1.0R)
- **MFE**: 159.75 points
- **MAE**: 83.00 points

### Trade #1652 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-07 10:00:00
- **FVG 5m**: 25056.75 - 25064.25
- **Entrée**: 25067.50 @ 2025-10-07 11:33:00
- **Stop Loss**: 25040.47
- **Risk**: 27.03 points
- **TP 1RR**: 25094.53 ❌
- **TP 2RR**: 25121.55 ❌
- **TP 3RR**: 25148.58 ❌
- **TP 4RR**: 25175.61 ❌
- **TP 15RR**: 25472.90 ❌
- **PnL**: -27.03 points (-1.0R)
- **MFE**: 24.50 points
- **MAE**: 35.00 points

### Trade #1653 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-07 10:15:00
- **FVG 5m**: 25080.25 - 25095.00
- **Entrée**: 25073.50 @ 2025-10-07 10:28:00
- **Stop Loss**: 25138.56
- **Risk**: 65.06 points
- **TP 1RR**: 25008.44 ✅
- **TP 2RR**: 24943.37 ❌
- **TP 3RR**: 24878.31 ❌
- **TP 4RR**: 24813.25 ❌
- **TP 15RR**: 24097.56 ❌
- **PnL**: -65.06 points (-1.0R)
- **MFE**: 88.75 points
- **MAE**: 75.50 points

### Trade #1654 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-08 03:45:00
- **FVG 5m**: 25094.25 - 25097.00
- **Entrée**: 25093.50 @ 2025-10-08 06:14:00
- **Stop Loss**: 25124.06
- **Risk**: 30.56 points
- **TP 1RR**: 25062.94 ✅
- **TP 2RR**: 25032.39 ❌
- **TP 3RR**: 25001.83 ❌
- **TP 4RR**: 24971.28 ❌
- **TP 15RR**: 24635.16 ❌
- **PnL**: -30.56 points (-1.0R)
- **MFE**: 51.00 points
- **MAE**: 33.50 points

### Trade #1655 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-08 03:45:00
- **FVG 5m**: 25094.25 - 25097.00
- **Entrée**: 25093.50 @ 2025-10-08 06:14:00
- **Stop Loss**: 25124.06
- **Risk**: 30.56 points
- **TP 1RR**: 25062.94 ✅
- **TP 2RR**: 25032.39 ❌
- **TP 3RR**: 25001.83 ❌
- **TP 4RR**: 24971.28 ❌
- **TP 15RR**: 24635.16 ❌
- **PnL**: -30.56 points (-1.0R)
- **MFE**: 51.00 points
- **MAE**: 33.50 points

### Trade #1656 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-08 08:30:00
- **FVG 5m**: 25167.25 - 25174.25
- **Entrée**: 25175.25 @ 2025-10-08 08:57:00
- **Stop Loss**: 25061.46
- **Risk**: 113.79 points
- **TP 1RR**: 25289.04 ✅
- **TP 2RR**: 25402.82 ❌
- **TP 3RR**: 25516.61 ❌
- **TP 4RR**: 25630.40 ❌
- **TP 15RR**: 26882.06 ❌
- **PnL**: -113.79 points (-1.0R)
- **MFE**: 218.75 points
- **MAE**: 120.50 points

### Trade #1657 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-08 08:30:00
- **FVG 5m**: 25167.25 - 25174.25
- **Entrée**: 25175.25 @ 2025-10-08 08:57:00
- **Stop Loss**: 25061.46
- **Risk**: 113.79 points
- **TP 1RR**: 25289.04 ✅
- **TP 2RR**: 25402.82 ❌
- **TP 3RR**: 25516.61 ❌
- **TP 4RR**: 25630.40 ❌
- **TP 15RR**: 26882.06 ❌
- **PnL**: -113.79 points (-1.0R)
- **MFE**: 218.75 points
- **MAE**: 120.50 points

### Trade #1658 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-08 08:45:00
- **FVG 5m**: 25167.25 - 25174.25
- **Entrée**: 25175.25 @ 2025-10-08 08:57:00
- **Stop Loss**: 25113.94
- **Risk**: 61.31 points
- **TP 1RR**: 25236.56 ✅
- **TP 2RR**: 25297.88 ✅
- **TP 3RR**: 25359.19 ✅
- **TP 4RR**: 25420.50 ❌
- **TP 15RR**: 26094.95 ❌
- **PnL**: -61.31 points (-1.0R)
- **MFE**: 218.75 points
- **MAE**: 111.25 points

### Trade #1659 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-09 12:30:00
- **FVG 5m**: 25200.25 - 25203.75
- **Entrée**: 25209.25 @ 2025-10-09 13:11:00
- **Stop Loss**: 25148.17
- **Risk**: 61.08 points
- **TP 1RR**: 25270.33 ✅
- **TP 2RR**: 25331.41 ✅
- **TP 3RR**: 25392.49 ❌
- **TP 4RR**: 25453.57 ❌
- **TP 15RR**: 26125.46 ❌
- **PnL**: -61.08 points (-1.0R)
- **MFE**: 178.75 points
- **MAE**: 81.50 points

### Trade #1660 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-09 14:45:00
- **FVG 5m**: 25282.75 - 25286.50
- **Entrée**: 25287.25 @ 2025-10-09 15:59:00
- **Stop Loss**: 25256.37
- **Risk**: 30.88 points
- **TP 1RR**: 25318.13 ✅
- **TP 2RR**: 25349.02 ✅
- **TP 3RR**: 25379.90 ❌
- **TP 4RR**: 25410.79 ❌
- **TP 15RR**: 25750.52 ❌
- **PnL**: -30.88 points (-1.0R)
- **MFE**: 68.00 points
- **MAE**: 31.25 points

### Trade #1661 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 01:15:00
- **FVG 5m**: 25331.75 - 25336.25
- **Entrée**: 25313.75 @ 2025-10-10 01:36:00
- **Stop Loss**: 25366.93
- **Risk**: 53.18 points
- **TP 1RR**: 25260.57 ✅
- **TP 2RR**: 25207.40 ❌
- **TP 3RR**: 25154.22 ❌
- **TP 4RR**: 25101.04 ❌
- **TP 15RR**: 24516.09 ❌
- **PnL**: -53.18 points (-1.0R)
- **MFE**: 62.75 points
- **MAE**: 58.25 points

### Trade #1662 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 01:15:00
- **FVG 5m**: 25331.75 - 25336.25
- **Entrée**: 25313.75 @ 2025-10-10 01:36:00
- **Stop Loss**: 25366.93
- **Risk**: 53.18 points
- **TP 1RR**: 25260.57 ✅
- **TP 2RR**: 25207.40 ❌
- **TP 3RR**: 25154.22 ❌
- **TP 4RR**: 25101.04 ❌
- **TP 15RR**: 24516.09 ❌
- **PnL**: -53.18 points (-1.0R)
- **MFE**: 62.75 points
- **MAE**: 58.25 points

### Trade #1663 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 05:45:00
- **FVG 5m**: 25296.50 - 25299.50
- **Entrée**: 25300.25 @ 2025-10-10 05:59:00
- **Stop Loss**: 25269.86
- **Risk**: 30.39 points
- **TP 1RR**: 25330.64 ✅
- **TP 2RR**: 25361.03 ✅
- **TP 3RR**: 25391.42 ❌
- **TP 4RR**: 25421.82 ❌
- **TP 15RR**: 25756.12 ❌
- **PnL**: -30.39 points (-1.0R)
- **MFE**: 87.75 points
- **MAE**: 40.00 points

### Trade #1664 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 08:45:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25400.69
- **Risk**: 206.19 points
- **TP 1RR**: 24988.31 ✅
- **TP 2RR**: 24782.11 ✅
- **TP 3RR**: 24575.92 ✅
- **TP 4RR**: 24369.72 ✅
- **TP 15RR**: 22101.59 ❌
- **PnL**: -206.19 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 325.50 points

### Trade #1665 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25383.44
- **Risk**: 188.94 points
- **TP 1RR**: 25005.56 ✅
- **TP 2RR**: 24816.63 ✅
- **TP 3RR**: 24627.69 ✅
- **TP 4RR**: 24438.76 ✅
- **TP 15RR**: 22360.47 ❌
- **PnL**: -188.94 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 189.25 points

### Trade #1666 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25383.44
- **Risk**: 188.94 points
- **TP 1RR**: 25005.56 ✅
- **TP 2RR**: 24816.63 ✅
- **TP 3RR**: 24627.69 ✅
- **TP 4RR**: 24438.76 ✅
- **TP 15RR**: 22360.47 ❌
- **PnL**: -188.94 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 189.25 points

### Trade #1667 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25383.44
- **Risk**: 188.94 points
- **TP 1RR**: 25005.56 ✅
- **TP 2RR**: 24816.63 ✅
- **TP 3RR**: 24627.69 ✅
- **TP 4RR**: 24438.76 ✅
- **TP 15RR**: 22360.47 ❌
- **PnL**: -188.94 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 189.25 points

### Trade #1668 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25383.44
- **Risk**: 188.94 points
- **TP 1RR**: 25005.56 ✅
- **TP 2RR**: 24816.63 ✅
- **TP 3RR**: 24627.69 ✅
- **TP 4RR**: 24438.76 ✅
- **TP 15RR**: 22360.47 ❌
- **PnL**: -188.94 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 189.25 points

### Trade #1669 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25383.44
- **Risk**: 188.94 points
- **TP 1RR**: 25005.56 ✅
- **TP 2RR**: 24816.63 ✅
- **TP 3RR**: 24627.69 ✅
- **TP 4RR**: 24438.76 ✅
- **TP 15RR**: 22360.47 ❌
- **PnL**: -188.94 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 189.25 points

### Trade #1670 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 09:00:00
- **FVG 5m**: 25196.00 - 25330.00
- **Entrée**: 25194.50 @ 2025-10-10 09:59:00
- **Stop Loss**: 25383.44
- **Risk**: 188.94 points
- **TP 1RR**: 25005.56 ✅
- **TP 2RR**: 24816.63 ✅
- **TP 3RR**: 24627.69 ✅
- **TP 4RR**: 24438.76 ✅
- **TP 15RR**: 22360.47 ❌
- **PnL**: -188.94 points (-1.0R)
- **MFE**: 1036.00 points
- **MAE**: 189.25 points

### Trade #1671 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:00:00
- **FVG 5m**: 24967.25 - 24993.00
- **Entrée**: 24941.25 @ 2025-10-10 10:18:00
- **Stop Loss**: 25208.60
- **Risk**: 267.35 points
- **TP 1RR**: 24673.90 ✅
- **TP 2RR**: 24406.55 ✅
- **TP 3RR**: 24139.21 ❌
- **TP 4RR**: 23871.86 ❌
- **TP 15RR**: 20931.03 ❌
- **PnL**: -267.35 points (-1.0R)
- **MFE**: 782.75 points
- **MAE**: 268.50 points

### Trade #1672 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:00:00
- **FVG 5m**: 24967.25 - 24993.00
- **Entrée**: 24941.25 @ 2025-10-10 10:18:00
- **Stop Loss**: 25208.60
- **Risk**: 267.35 points
- **TP 1RR**: 24673.90 ✅
- **TP 2RR**: 24406.55 ✅
- **TP 3RR**: 24139.21 ❌
- **TP 4RR**: 23871.86 ❌
- **TP 15RR**: 20931.03 ❌
- **PnL**: -267.35 points (-1.0R)
- **MFE**: 782.75 points
- **MAE**: 268.50 points

### Trade #1673 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:15:00
- **FVG 5m**: 24790.00 - 24802.50
- **Entrée**: 24780.00 @ 2025-10-10 10:31:00
- **Stop Loss**: 25090.54
- **Risk**: 310.54 points
- **TP 1RR**: 24469.46 ✅
- **TP 2RR**: 24158.92 ✅
- **TP 3RR**: 23848.38 ❌
- **TP 4RR**: 23537.84 ❌
- **TP 15RR**: 20121.91 ❌
- **PnL**: -310.54 points (-1.0R)
- **MFE**: 621.50 points
- **MAE**: 316.75 points

### Trade #1674 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-10 10:15:00
- **FVG 5m**: 24790.00 - 24802.50
- **Entrée**: 24780.00 @ 2025-10-10 10:31:00
- **Stop Loss**: 25090.54
- **Risk**: 310.54 points
- **TP 1RR**: 24469.46 ✅
- **TP 2RR**: 24158.92 ✅
- **TP 3RR**: 23848.38 ❌
- **TP 4RR**: 23537.84 ❌
- **TP 15RR**: 20121.91 ❌
- **PnL**: -310.54 points (-1.0R)
- **MFE**: 621.50 points
- **MAE**: 316.75 points

### Trade #1675 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 10:30:00
- **FVG 5m**: 24790.00 - 24810.00
- **Entrée**: 24861.25 @ 2025-10-10 10:44:00
- **Stop Loss**: 24658.41
- **Risk**: 202.84 points
- **TP 1RR**: 25064.09 ❌
- **TP 2RR**: 25266.92 ❌
- **TP 3RR**: 25469.76 ❌
- **TP 4RR**: 25672.59 ❌
- **TP 15RR**: 27903.78 ❌
- **PnL**: -202.84 points (-1.0R)
- **MFE**: 47.00 points
- **MAE**: 209.25 points

### Trade #1676 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 10:30:00
- **FVG 5m**: 24790.00 - 24810.00
- **Entrée**: 24861.25 @ 2025-10-10 10:44:00
- **Stop Loss**: 24658.41
- **Risk**: 202.84 points
- **TP 1RR**: 25064.09 ❌
- **TP 2RR**: 25266.92 ❌
- **TP 3RR**: 25469.76 ❌
- **TP 4RR**: 25672.59 ❌
- **TP 15RR**: 27903.78 ❌
- **PnL**: -202.84 points (-1.0R)
- **MFE**: 47.00 points
- **MAE**: 209.25 points

### Trade #1677 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 12:15:00
- **FVG 5m**: 24688.75 - 24694.25
- **Entrée**: 24695.25 @ 2025-10-10 12:27:00
- **Stop Loss**: 24603.69
- **Risk**: 91.56 points
- **TP 1RR**: 24786.81 ❌
- **TP 2RR**: 24878.37 ❌
- **TP 3RR**: 24969.92 ❌
- **TP 4RR**: 25061.48 ❌
- **TP 15RR**: 26068.62 ❌
- **PnL**: -91.56 points (-1.0R)
- **MFE**: 55.75 points
- **MAE**: 91.75 points

### Trade #1678 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 14:30:00
- **FVG 5m**: 24514.25 - 24520.25
- **Entrée**: 24535.50 @ 2025-10-10 14:44:00
- **Stop Loss**: 24434.78
- **Risk**: 100.72 points
- **TP 1RR**: 24636.22 ❌
- **TP 2RR**: 24736.95 ❌
- **TP 3RR**: 24837.67 ❌
- **TP 4RR**: 24938.39 ❌
- **TP 15RR**: 26046.35 ❌
- **PnL**: -100.72 points (-1.0R)
- **MFE**: 21.25 points
- **MAE**: 107.75 points

### Trade #1679 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-10 15:00:00
- **FVG 5m**: 24422.00 - 24542.00
- **Entrée**: 24735.50 @ 2025-10-12 17:00:00
- **Stop Loss**: 24380.55
- **Risk**: 354.95 points
- **TP 1RR**: 25090.45 ✅
- **TP 2RR**: 25445.39 ✅
- **TP 3RR**: 25800.34 ✅
- **TP 4RR**: 26155.29 ✅
- **TP 15RR**: 30059.70 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1663.50 points
- **MAE**: 325.50 points

### Trade #1680 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-12 17:00:00
- **FVG 5m**: 24698.00 - 24703.25
- **Entrée**: 24719.25 @ 2025-10-12 17:18:00
- **Stop Loss**: 24529.73
- **Risk**: 189.52 points
- **TP 1RR**: 24908.77 ✅
- **TP 2RR**: 25098.29 ❌
- **TP 3RR**: 25287.81 ❌
- **TP 4RR**: 25477.33 ❌
- **TP 15RR**: 27562.07 ❌
- **PnL**: -189.52 points (-1.0R)
- **MFE**: 325.00 points
- **MAE**: 193.50 points

### Trade #1681 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 03:30:00
- **FVG 5m**: 24847.50 - 24859.25
- **Entrée**: 24845.00 @ 2025-10-13 05:43:00
- **Stop Loss**: 24893.19
- **Risk**: 48.19 points
- **TP 1RR**: 24796.81 ✅
- **TP 2RR**: 24748.62 ✅
- **TP 3RR**: 24700.43 ❌
- **TP 4RR**: 24652.24 ❌
- **TP 15RR**: 24122.14 ❌
- **PnL**: -48.19 points (-1.0R)
- **MFE**: 120.50 points
- **MAE**: 62.25 points

### Trade #1682 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 06:00:00
- **FVG 5m**: 24792.00 - 24809.00
- **Entrée**: 24814.25 @ 2025-10-13 07:14:00
- **Stop Loss**: 24720.63
- **Risk**: 93.62 points
- **TP 1RR**: 24907.87 ✅
- **TP 2RR**: 25001.48 ✅
- **TP 3RR**: 25095.10 ❌
- **TP 4RR**: 25188.72 ❌
- **TP 15RR**: 26218.50 ❌
- **PnL**: -93.62 points (-1.0R)
- **MFE**: 230.00 points
- **MAE**: 126.25 points

### Trade #1683 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 06:30:00
- **FVG 5m**: 24792.00 - 24809.00
- **Entrée**: 24814.25 @ 2025-10-13 07:14:00
- **Stop Loss**: 24723.63
- **Risk**: 90.62 points
- **TP 1RR**: 24904.87 ✅
- **TP 2RR**: 24995.49 ✅
- **TP 3RR**: 25086.10 ❌
- **TP 4RR**: 25176.72 ❌
- **TP 15RR**: 26173.52 ❌
- **PnL**: -90.62 points (-1.0R)
- **MFE**: 230.00 points
- **MAE**: 126.25 points

### Trade #1684 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 11:15:00
- **FVG 5m**: 24922.75 - 24945.50
- **Entrée**: 24919.50 @ 2025-10-13 12:12:00
- **Stop Loss**: 24942.72
- **Risk**: 23.22 points
- **TP 1RR**: 24896.28 ✅
- **TP 2RR**: 24873.07 ❌
- **TP 3RR**: 24849.85 ❌
- **TP 4RR**: 24826.64 ❌
- **TP 15RR**: 24571.27 ❌
- **PnL**: -23.22 points (-1.0R)
- **MFE**: 31.00 points
- **MAE**: 26.00 points

### Trade #1685 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 12:00:00
- **FVG 5m**: 24922.75 - 24945.50
- **Entrée**: 24919.50 @ 2025-10-13 12:12:00
- **Stop Loss**: 24971.48
- **Risk**: 51.98 points
- **TP 1RR**: 24867.52 ❌
- **TP 2RR**: 24815.54 ❌
- **TP 3RR**: 24763.56 ❌
- **TP 4RR**: 24711.58 ❌
- **TP 15RR**: 24139.81 ❌
- **PnL**: -51.98 points (-1.0R)
- **MFE**: 36.50 points
- **MAE**: 58.50 points

### Trade #1686 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24987.00 - 24995.50
- **Entrée**: 24998.50 @ 2025-10-13 19:29:00
- **Stop Loss**: 24931.03
- **Risk**: 67.47 points
- **TP 1RR**: 25065.97 ❌
- **TP 2RR**: 25133.44 ❌
- **TP 3RR**: 25200.92 ❌
- **TP 4RR**: 25268.39 ❌
- **TP 15RR**: 26010.58 ❌
- **PnL**: -67.47 points (-1.0R)
- **MFE**: 45.75 points
- **MAE**: 71.00 points

### Trade #1687 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24987.00 - 24995.50
- **Entrée**: 24998.50 @ 2025-10-13 19:29:00
- **Stop Loss**: 24931.03
- **Risk**: 67.47 points
- **TP 1RR**: 25065.97 ❌
- **TP 2RR**: 25133.44 ❌
- **TP 3RR**: 25200.92 ❌
- **TP 4RR**: 25268.39 ❌
- **TP 15RR**: 26010.58 ❌
- **PnL**: -67.47 points (-1.0R)
- **MFE**: 45.75 points
- **MAE**: 71.00 points

### Trade #1688 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24987.00 - 24995.50
- **Entrée**: 24998.50 @ 2025-10-13 19:29:00
- **Stop Loss**: 24931.03
- **Risk**: 67.47 points
- **TP 1RR**: 25065.97 ❌
- **TP 2RR**: 25133.44 ❌
- **TP 3RR**: 25200.92 ❌
- **TP 4RR**: 25268.39 ❌
- **TP 15RR**: 26010.58 ❌
- **PnL**: -67.47 points (-1.0R)
- **MFE**: 45.75 points
- **MAE**: 71.00 points

### Trade #1689 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-13 19:15:00
- **FVG 5m**: 24987.00 - 24995.50
- **Entrée**: 24998.50 @ 2025-10-13 19:29:00
- **Stop Loss**: 24931.03
- **Risk**: 67.47 points
- **TP 1RR**: 25065.97 ❌
- **TP 2RR**: 25133.44 ❌
- **TP 3RR**: 25200.92 ❌
- **TP 4RR**: 25268.39 ❌
- **TP 15RR**: 26010.58 ❌
- **PnL**: -67.47 points (-1.0R)
- **MFE**: 45.75 points
- **MAE**: 71.00 points

### Trade #1690 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 21:45:00
- **FVG 5m**: 24943.25 - 24953.75
- **Entrée**: 24938.00 @ 2025-10-13 22:04:00
- **Stop Loss**: 24995.49
- **Risk**: 57.49 points
- **TP 1RR**: 24880.51 ✅
- **TP 2RR**: 24823.02 ✅
- **TP 3RR**: 24765.53 ✅
- **TP 4RR**: 24708.03 ✅
- **TP 15RR**: 24075.63 ❌
- **PnL**: -57.49 points (-1.0R)
- **MFE**: 517.00 points
- **MAE**: 59.00 points

### Trade #1691 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-13 21:45:00
- **FVG 5m**: 24943.25 - 24953.75
- **Entrée**: 24938.00 @ 2025-10-13 22:04:00
- **Stop Loss**: 24995.49
- **Risk**: 57.49 points
- **TP 1RR**: 24880.51 ✅
- **TP 2RR**: 24823.02 ✅
- **TP 3RR**: 24765.53 ✅
- **TP 4RR**: 24708.03 ✅
- **TP 15RR**: 24075.63 ❌
- **PnL**: -57.49 points (-1.0R)
- **MFE**: 517.00 points
- **MAE**: 59.00 points

### Trade #1692 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-14 00:30:00
- **FVG 5m**: 24702.25 - 24712.00
- **Entrée**: 24702.00 @ 2025-10-14 01:38:00
- **Stop Loss**: 24809.40
- **Risk**: 107.40 points
- **TP 1RR**: 24594.60 ✅
- **TP 2RR**: 24487.20 ✅
- **TP 3RR**: 24379.80 ❌
- **TP 4RR**: 24272.41 ❌
- **TP 15RR**: 23091.02 ❌
- **PnL**: -107.40 points (-1.0R)
- **MFE**: 281.00 points
- **MAE**: 111.75 points

### Trade #1693 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 06:00:00
- **FVG 5m**: 24605.00 - 24615.50
- **Entrée**: 24620.25 @ 2025-10-14 06:21:00
- **Stop Loss**: 24533.73
- **Risk**: 86.52 points
- **TP 1RR**: 24706.77 ❌
- **TP 2RR**: 24793.30 ❌
- **TP 3RR**: 24879.82 ❌
- **TP 4RR**: 24966.34 ❌
- **TP 15RR**: 25918.10 ❌
- **PnL**: -86.52 points (-1.0R)
- **MFE**: 44.75 points
- **MAE**: 86.75 points

### Trade #1694 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 08:45:00
- **FVG 5m**: 24638.00 - 24686.50
- **Entrée**: 24688.50 @ 2025-10-14 09:24:00
- **Stop Loss**: 24408.79
- **Risk**: 279.71 points
- **TP 1RR**: 24968.21 ✅
- **TP 2RR**: 25247.92 ✅
- **TP 3RR**: 25527.63 ✅
- **TP 4RR**: 25807.34 ✅
- **TP 15RR**: 28884.16 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1710.50 points
- **MAE**: 278.50 points

### Trade #1695 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 08:45:00
- **FVG 5m**: 24638.00 - 24686.50
- **Entrée**: 24688.50 @ 2025-10-14 09:24:00
- **Stop Loss**: 24408.79
- **Risk**: 279.71 points
- **TP 1RR**: 24968.21 ✅
- **TP 2RR**: 25247.92 ✅
- **TP 3RR**: 25527.63 ✅
- **TP 4RR**: 25807.34 ✅
- **TP 15RR**: 28884.16 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1710.50 points
- **MAE**: 278.50 points

### Trade #1696 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 11:30:00
- **FVG 5m**: 24899.00 - 24906.75
- **Entrée**: 24910.50 @ 2025-10-14 12:06:00
- **Stop Loss**: 24855.82
- **Risk**: 54.68 points
- **TP 1RR**: 24965.18 ❌
- **TP 2RR**: 25019.87 ❌
- **TP 3RR**: 25074.55 ❌
- **TP 4RR**: 25129.24 ❌
- **TP 15RR**: 25730.76 ❌
- **PnL**: -54.68 points (-1.0R)
- **MFE**: 27.50 points
- **MAE**: 136.75 points

### Trade #1697 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-14 11:30:00
- **FVG 5m**: 24899.00 - 24906.75
- **Entrée**: 24910.50 @ 2025-10-14 12:06:00
- **Stop Loss**: 24855.82
- **Risk**: 54.68 points
- **TP 1RR**: 24965.18 ❌
- **TP 2RR**: 25019.87 ❌
- **TP 3RR**: 25074.55 ❌
- **TP 4RR**: 25129.24 ❌
- **TP 15RR**: 25730.76 ❌
- **PnL**: -54.68 points (-1.0R)
- **MFE**: 27.50 points
- **MAE**: 136.75 points

### Trade #1698 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-14 22:30:00
- **FVG 5m**: 24809.00 - 24816.00
- **Entrée**: 24808.25 @ 2025-10-14 22:43:00
- **Stop Loss**: 24842.92
- **Risk**: 34.67 points
- **TP 1RR**: 24773.58 ❌
- **TP 2RR**: 24738.92 ❌
- **TP 3RR**: 24704.25 ❌
- **TP 4RR**: 24669.59 ❌
- **TP 15RR**: 24288.27 ❌
- **PnL**: -34.67 points (-1.0R)
- **MFE**: 11.75 points
- **MAE**: 34.75 points

### Trade #1699 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 08:30:00
- **FVG 5m**: 24987.25 - 25013.00
- **Entrée**: 25021.25 @ 2025-10-15 08:58:00
- **Stop Loss**: 24908.04
- **Risk**: 113.21 points
- **TP 1RR**: 25134.46 ❌
- **TP 2RR**: 25247.67 ❌
- **TP 3RR**: 25360.88 ❌
- **TP 4RR**: 25474.09 ❌
- **TP 15RR**: 26719.40 ❌
- **PnL**: -113.21 points (-1.0R)
- **MFE**: 93.75 points
- **MAE**: 139.75 points

### Trade #1700 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 10:30:00
- **FVG 5m**: 24961.25 - 24967.25
- **Entrée**: 24958.75 @ 2025-10-15 10:41:00
- **Stop Loss**: 25071.78
- **Risk**: 113.03 points
- **TP 1RR**: 24845.72 ✅
- **TP 2RR**: 24732.69 ✅
- **TP 3RR**: 24619.66 ❌
- **TP 4RR**: 24506.63 ❌
- **TP 15RR**: 23263.31 ❌
- **PnL**: -113.03 points (-1.0R)
- **MFE**: 295.50 points
- **MAE**: 113.25 points

### Trade #1701 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 10:30:00
- **FVG 5m**: 24961.25 - 24967.25
- **Entrée**: 24958.75 @ 2025-10-15 10:41:00
- **Stop Loss**: 25071.78
- **Risk**: 113.03 points
- **TP 1RR**: 24845.72 ✅
- **TP 2RR**: 24732.69 ✅
- **TP 3RR**: 24619.66 ❌
- **TP 4RR**: 24506.63 ❌
- **TP 15RR**: 23263.31 ❌
- **PnL**: -113.03 points (-1.0R)
- **MFE**: 295.50 points
- **MAE**: 113.25 points

### Trade #1702 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 10:30:00
- **FVG 5m**: 24961.25 - 24967.25
- **Entrée**: 24958.75 @ 2025-10-15 10:41:00
- **Stop Loss**: 25071.78
- **Risk**: 113.03 points
- **TP 1RR**: 24845.72 ✅
- **TP 2RR**: 24732.69 ✅
- **TP 3RR**: 24619.66 ❌
- **TP 4RR**: 24506.63 ❌
- **TP 15RR**: 23263.31 ❌
- **PnL**: -113.03 points (-1.0R)
- **MFE**: 295.50 points
- **MAE**: 113.25 points

### Trade #1703 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 11:45:00
- **FVG 5m**: 24857.75 - 24892.25
- **Entrée**: 24832.75 @ 2025-10-15 12:05:00
- **Stop Loss**: 24950.97
- **Risk**: 118.22 points
- **TP 1RR**: 24714.53 ✅
- **TP 2RR**: 24596.31 ❌
- **TP 3RR**: 24478.09 ❌
- **TP 4RR**: 24359.87 ❌
- **TP 15RR**: 23059.46 ❌
- **PnL**: -118.22 points (-1.0R)
- **MFE**: 169.50 points
- **MAE**: 124.75 points

### Trade #1704 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 12:00:00
- **FVG 5m**: 24750.75 - 24776.00
- **Entrée**: 24723.50 @ 2025-10-15 12:11:00
- **Stop Loss**: 24916.20
- **Risk**: 192.70 points
- **TP 1RR**: 24530.80 ❌
- **TP 2RR**: 24338.10 ❌
- **TP 3RR**: 24145.39 ❌
- **TP 4RR**: 23952.69 ❌
- **TP 15RR**: 21832.97 ❌
- **PnL**: -192.70 points (-1.0R)
- **MFE**: 60.25 points
- **MAE**: 193.00 points

### Trade #1705 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:15:00
- **FVG 5m**: 24791.50 - 24805.50
- **Entrée**: 24809.00 @ 2025-10-15 12:36:00
- **Stop Loss**: 24650.92
- **Risk**: 158.08 points
- **TP 1RR**: 24967.08 ✅
- **TP 2RR**: 25125.16 ✅
- **TP 3RR**: 25283.24 ❌
- **TP 4RR**: 25441.33 ❌
- **TP 15RR**: 27180.22 ❌
- **PnL**: -158.08 points (-1.0R)
- **MFE**: 370.50 points
- **MAE**: 165.50 points

### Trade #1706 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:15:00
- **FVG 5m**: 24791.50 - 24805.50
- **Entrée**: 24809.00 @ 2025-10-15 12:36:00
- **Stop Loss**: 24650.92
- **Risk**: 158.08 points
- **TP 1RR**: 24967.08 ✅
- **TP 2RR**: 25125.16 ✅
- **TP 3RR**: 25283.24 ❌
- **TP 4RR**: 25441.33 ❌
- **TP 15RR**: 27180.22 ❌
- **PnL**: -158.08 points (-1.0R)
- **MFE**: 370.50 points
- **MAE**: 165.50 points

### Trade #1707 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:30:00
- **FVG 5m**: 24825.00 - 24836.75
- **Entrée**: 24838.00 @ 2025-10-15 12:44:00
- **Stop Loss**: 24726.63
- **Risk**: 111.37 points
- **TP 1RR**: 24949.37 ✅
- **TP 2RR**: 25060.74 ✅
- **TP 3RR**: 25172.11 ✅
- **TP 4RR**: 25283.48 ❌
- **TP 15RR**: 26508.54 ❌
- **PnL**: -111.37 points (-1.0R)
- **MFE**: 341.50 points
- **MAE**: 141.75 points

### Trade #1708 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-15 12:45:00
- **FVG 5m**: 24926.75 - 24935.75
- **Entrée**: 24939.00 @ 2025-10-15 14:16:00
- **Stop Loss**: 24824.33
- **Risk**: 114.67 points
- **TP 1RR**: 25053.67 ✅
- **TP 2RR**: 25168.34 ✅
- **TP 3RR**: 25283.01 ❌
- **TP 4RR**: 25397.67 ❌
- **TP 15RR**: 26659.03 ❌
- **PnL**: -114.67 points (-1.0R)
- **MFE**: 240.50 points
- **MAE**: 137.50 points

### Trade #1709 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-15 13:30:00
- **FVG 5m**: 24934.75 - 24938.75
- **Entrée**: 24933.75 @ 2025-10-15 14:33:00
- **Stop Loss**: 24962.47
- **Risk**: 28.72 points
- **TP 1RR**: 24905.03 ✅
- **TP 2RR**: 24876.30 ✅
- **TP 3RR**: 24847.58 ✅
- **TP 4RR**: 24818.85 ❌
- **TP 15RR**: 24502.88 ❌
- **PnL**: -28.72 points (-1.0R)
- **MFE**: 88.75 points
- **MAE**: 30.50 points

### Trade #1710 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 07:00:00
- **FVG 5m**: 25069.25 - 25072.00
- **Entrée**: 25065.25 @ 2025-10-16 08:22:00
- **Stop Loss**: 25086.54
- **Risk**: 21.29 points
- **TP 1RR**: 25043.96 ✅
- **TP 2RR**: 25022.68 ❌
- **TP 3RR**: 25001.39 ❌
- **TP 4RR**: 24980.10 ❌
- **TP 15RR**: 24745.94 ❌
- **PnL**: -21.29 points (-1.0R)
- **MFE**: 24.75 points
- **MAE**: 40.50 points

### Trade #1711 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 09:45:00
- **FVG 5m**: 25087.50 - 25099.50
- **Entrée**: 25085.25 @ 2025-10-16 10:24:00
- **Stop Loss**: 25192.09
- **Risk**: 106.84 points
- **TP 1RR**: 24978.41 ✅
- **TP 2RR**: 24871.57 ✅
- **TP 3RR**: 24764.73 ✅
- **TP 4RR**: 24657.89 ✅
- **TP 15RR**: 23482.65 ❌
- **PnL**: -106.84 points (-1.0R)
- **MFE**: 675.25 points
- **MAE**: 116.25 points

### Trade #1712 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 10:45:00
- **FVG 5m**: 24942.75 - 24952.00
- **Entrée**: 24930.50 @ 2025-10-16 11:18:00
- **Stop Loss**: 25030.26
- **Risk**: 99.76 points
- **TP 1RR**: 24830.74 ✅
- **TP 2RR**: 24730.98 ✅
- **TP 3RR**: 24631.22 ✅
- **TP 4RR**: 24531.46 ✅
- **TP 15RR**: 23434.12 ❌
- **PnL**: -99.76 points (-1.0R)
- **MFE**: 520.50 points
- **MAE**: 122.00 points

### Trade #1713 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-16 11:15:00
- **FVG 5m**: 24877.75 - 24895.00
- **Entrée**: 24875.25 @ 2025-10-16 11:26:00
- **Stop Loss**: 25008.75
- **Risk**: 133.50 points
- **TP 1RR**: 24741.75 ✅
- **TP 2RR**: 24608.25 ✅
- **TP 3RR**: 24474.76 ✅
- **TP 4RR**: 24341.26 ❌
- **TP 15RR**: 22872.78 ❌
- **PnL**: -133.50 points (-1.0R)
- **MFE**: 465.25 points
- **MAE**: 150.00 points

### Trade #1714 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 11:45:00
- **FVG 5m**: 24728.00 - 24752.50
- **Entrée**: 24762.00 @ 2025-10-16 13:43:00
- **Stop Loss**: 24719.63
- **Risk**: 42.37 points
- **TP 1RR**: 24804.37 ✅
- **TP 2RR**: 24846.73 ❌
- **TP 3RR**: 24889.10 ❌
- **TP 4RR**: 24931.46 ❌
- **TP 15RR**: 25397.49 ❌
- **PnL**: -42.37 points (-1.0R)
- **MFE**: 58.75 points
- **MAE**: 51.50 points

### Trade #1715 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 11:45:00
- **FVG 5m**: 24728.00 - 24752.50
- **Entrée**: 24762.00 @ 2025-10-16 13:43:00
- **Stop Loss**: 24719.63
- **Risk**: 42.37 points
- **TP 1RR**: 24804.37 ✅
- **TP 2RR**: 24846.73 ❌
- **TP 3RR**: 24889.10 ❌
- **TP 4RR**: 24931.46 ❌
- **TP 15RR**: 25397.49 ❌
- **PnL**: -42.37 points (-1.0R)
- **MFE**: 58.75 points
- **MAE**: 51.50 points

### Trade #1716 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 11:45:00
- **FVG 5m**: 24728.00 - 24752.50
- **Entrée**: 24762.00 @ 2025-10-16 13:43:00
- **Stop Loss**: 24719.63
- **Risk**: 42.37 points
- **TP 1RR**: 24804.37 ✅
- **TP 2RR**: 24846.73 ❌
- **TP 3RR**: 24889.10 ❌
- **TP 4RR**: 24931.46 ❌
- **TP 15RR**: 25397.49 ❌
- **PnL**: -42.37 points (-1.0R)
- **MFE**: 58.75 points
- **MAE**: 51.50 points

### Trade #1717 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-16 13:30:00
- **FVG 5m**: 24728.00 - 24752.50
- **Entrée**: 24762.00 @ 2025-10-16 13:43:00
- **Stop Loss**: 24631.18
- **Risk**: 130.82 points
- **TP 1RR**: 24892.82 ❌
- **TP 2RR**: 25023.64 ❌
- **TP 3RR**: 25154.47 ❌
- **TP 4RR**: 25285.29 ❌
- **TP 15RR**: 26724.33 ❌
- **PnL**: -130.82 points (-1.0R)
- **MFE**: 96.50 points
- **MAE**: 135.75 points

### Trade #1718 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-17 00:30:00
- **FVG 5m**: 24669.75 - 24677.25
- **Entrée**: 24668.00 @ 2025-10-17 01:11:00
- **Stop Loss**: 24690.59
- **Risk**: 22.59 points
- **TP 1RR**: 24645.41 ✅
- **TP 2RR**: 24622.82 ✅
- **TP 3RR**: 24600.23 ✅
- **TP 4RR**: 24577.64 ✅
- **TP 15RR**: 24329.16 ❌
- **PnL**: -22.59 points (-1.0R)
- **MFE**: 258.00 points
- **MAE**: 52.50 points

### Trade #1719 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-17 00:45:00
- **FVG 5m**: 24674.75 - 24677.25
- **Entrée**: 24677.75 @ 2025-10-17 01:04:00
- **Stop Loss**: 24609.19
- **Risk**: 68.56 points
- **TP 1RR**: 24746.31 ❌
- **TP 2RR**: 24814.87 ❌
- **TP 3RR**: 24883.43 ❌
- **TP 4RR**: 24951.99 ❌
- **TP 15RR**: 25706.16 ❌
- **PnL**: -68.56 points (-1.0R)
- **MFE**: 13.00 points
- **MAE**: 81.25 points

### Trade #1720 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-17 08:45:00
- **FVG 5m**: 24861.75 - 24894.75
- **Entrée**: 24857.75 @ 2025-10-17 09:34:00
- **Stop Loss**: 24902.19
- **Risk**: 44.44 points
- **TP 1RR**: 24813.31 ✅
- **TP 2RR**: 24768.86 ✅
- **TP 3RR**: 24724.42 ✅
- **TP 4RR**: 24679.97 ✅
- **TP 15RR**: 24191.08 ❌
- **PnL**: -44.44 points (-1.0R)
- **MFE**: 182.75 points
- **MAE**: 50.25 points

### Trade #1721 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-17 08:45:00
- **FVG 5m**: 24861.75 - 24894.75
- **Entrée**: 24857.75 @ 2025-10-17 09:34:00
- **Stop Loss**: 24902.19
- **Risk**: 44.44 points
- **TP 1RR**: 24813.31 ✅
- **TP 2RR**: 24768.86 ✅
- **TP 3RR**: 24724.42 ✅
- **TP 4RR**: 24679.97 ✅
- **TP 15RR**: 24191.08 ❌
- **PnL**: -44.44 points (-1.0R)
- **MFE**: 182.75 points
- **MAE**: 50.25 points

### Trade #1722 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-17 13:15:00
- **FVG 5m**: 25011.25 - 25021.00
- **Entrée**: 25023.25 @ 2025-10-17 15:21:00
- **Stop Loss**: 24953.02
- **Risk**: 70.23 points
- **TP 1RR**: 25093.48 ✅
- **TP 2RR**: 25163.72 ✅
- **TP 3RR**: 25233.95 ✅
- **TP 4RR**: 25304.18 ✅
- **TP 15RR**: 26076.74 ❌
- **PnL**: -70.23 points (-1.0R)
- **MFE**: 344.75 points
- **MAE**: 113.25 points

### Trade #1723 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-17 14:00:00
- **FVG 5m**: 25011.25 - 25021.00
- **Entrée**: 25023.25 @ 2025-10-17 15:21:00
- **Stop Loss**: 24983.00
- **Risk**: 40.25 points
- **TP 1RR**: 25063.50 ✅
- **TP 2RR**: 25103.75 ❌
- **TP 3RR**: 25143.99 ❌
- **TP 4RR**: 25184.24 ❌
- **TP 15RR**: 25626.97 ❌
- **PnL**: -40.25 points (-1.0R)
- **MFE**: 76.00 points
- **MAE**: 45.25 points

### Trade #1724 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-19 17:15:00
- **FVG 5m**: 25053.50 - 25056.50
- **Entrée**: 25052.50 @ 2025-10-19 18:01:00
- **Stop Loss**: 25086.79
- **Risk**: 34.29 points
- **TP 1RR**: 25018.21 ✅
- **TP 2RR**: 24983.93 ✅
- **TP 3RR**: 24949.64 ❌
- **TP 4RR**: 24915.35 ❌
- **TP 15RR**: 24538.19 ❌
- **PnL**: -34.29 points (-1.0R)
- **MFE**: 96.75 points
- **MAE**: 46.50 points

### Trade #1725 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-19 19:15:00
- **FVG 5m**: 24983.75 - 24998.25
- **Entrée**: 25004.00 @ 2025-10-19 19:39:00
- **Stop Loss**: 24943.27
- **Risk**: 60.73 points
- **TP 1RR**: 25064.73 ✅
- **TP 2RR**: 25125.46 ✅
- **TP 3RR**: 25186.18 ✅
- **TP 4RR**: 25246.91 ✅
- **TP 15RR**: 25914.92 ❌
- **PnL**: -60.73 points (-1.0R)
- **MFE**: 364.00 points
- **MAE**: 94.00 points

### Trade #1726 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-20 03:45:00
- **FVG 5m**: 25074.25 - 25088.00
- **Entrée**: 25071.50 @ 2025-10-20 05:44:00
- **Stop Loss**: 25111.30
- **Risk**: 39.80 points
- **TP 1RR**: 25031.70 ❌
- **TP 2RR**: 24991.90 ❌
- **TP 3RR**: 24952.10 ❌
- **TP 4RR**: 24912.30 ❌
- **TP 15RR**: 24474.51 ❌
- **PnL**: -39.80 points (-1.0R)
- **MFE**: 33.50 points
- **MAE**: 45.25 points

### Trade #1727 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-20 06:00:00
- **FVG 5m**: 25065.75 - 25069.25
- **Entrée**: 25070.50 @ 2025-10-20 06:12:00
- **Stop Loss**: 25025.48
- **Risk**: 45.02 points
- **TP 1RR**: 25115.52 ✅
- **TP 2RR**: 25160.54 ✅
- **TP 3RR**: 25205.56 ✅
- **TP 4RR**: 25250.58 ✅
- **TP 15RR**: 25745.79 ❌
- **PnL**: -45.02 points (-1.0R)
- **MFE**: 297.50 points
- **MAE**: 47.00 points

### Trade #1728 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-20 09:15:00
- **FVG 5m**: 25250.00 - 25266.25
- **Entrée**: 25278.00 @ 2025-10-20 09:27:00
- **Stop Loss**: 25202.64
- **Risk**: 75.36 points
- **TP 1RR**: 25353.36 ✅
- **TP 2RR**: 25428.72 ❌
- **TP 3RR**: 25504.07 ❌
- **TP 4RR**: 25579.43 ❌
- **TP 15RR**: 26408.36 ❌
- **PnL**: -75.36 points (-1.0R)
- **MFE**: 90.00 points
- **MAE**: 84.75 points

### Trade #1729 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-20 09:30:00
- **FVG 5m**: 25287.50 - 25294.75
- **Entrée**: 25295.50 @ 2025-10-20 09:41:00
- **Stop Loss**: 25253.12
- **Risk**: 42.38 points
- **TP 1RR**: 25337.88 ✅
- **TP 2RR**: 25380.27 ❌
- **TP 3RR**: 25422.65 ❌
- **TP 4RR**: 25465.03 ❌
- **TP 15RR**: 25931.24 ❌
- **PnL**: -42.38 points (-1.0R)
- **MFE**: 72.50 points
- **MAE**: 42.50 points

### Trade #1730 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-20 09:30:00
- **FVG 5m**: 25287.50 - 25294.75
- **Entrée**: 25295.50 @ 2025-10-20 09:41:00
- **Stop Loss**: 25253.12
- **Risk**: 42.38 points
- **TP 1RR**: 25337.88 ✅
- **TP 2RR**: 25380.27 ❌
- **TP 3RR**: 25422.65 ❌
- **TP 4RR**: 25465.03 ❌
- **TP 15RR**: 25931.24 ❌
- **PnL**: -42.38 points (-1.0R)
- **MFE**: 72.50 points
- **MAE**: 42.50 points

### Trade #1731 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-20 20:15:00
- **FVG 5m**: 25342.00 - 25345.00
- **Entrée**: 25339.75 @ 2025-10-20 20:27:00
- **Stop Loss**: 25371.93
- **Risk**: 32.18 points
- **TP 1RR**: 25307.57 ✅
- **TP 2RR**: 25275.39 ✅
- **TP 3RR**: 25243.21 ✅
- **TP 4RR**: 25211.03 ✅
- **TP 15RR**: 24857.06 ✅
- **PnL**: 482.69 points (15.0R)
- **MFE**: 486.50 points
- **MAE**: 28.25 points

### Trade #1732 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-20 20:15:00
- **FVG 5m**: 25342.00 - 25345.00
- **Entrée**: 25339.75 @ 2025-10-20 20:27:00
- **Stop Loss**: 25371.93
- **Risk**: 32.18 points
- **TP 1RR**: 25307.57 ✅
- **TP 2RR**: 25275.39 ✅
- **TP 3RR**: 25243.21 ✅
- **TP 4RR**: 25211.03 ✅
- **TP 15RR**: 24857.06 ✅
- **PnL**: 482.69 points (15.0R)
- **MFE**: 486.50 points
- **MAE**: 28.25 points

### Trade #1733 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-20 21:30:00
- **FVG 5m**: 25353.00 - 25356.75
- **Entrée**: 25352.50 @ 2025-10-20 21:43:00
- **Stop Loss**: 25380.68
- **Risk**: 28.18 points
- **TP 1RR**: 25324.32 ✅
- **TP 2RR**: 25296.13 ✅
- **TP 3RR**: 25267.95 ✅
- **TP 4RR**: 25239.76 ✅
- **TP 15RR**: 24929.74 ✅
- **PnL**: 422.76 points (15.0R)
- **MFE**: 442.50 points
- **MAE**: 3.25 points

### Trade #1734 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-21 08:30:00
- **FVG 5m**: 25254.00 - 25258.75
- **Entrée**: 25267.25 @ 2025-10-21 09:18:00
- **Stop Loss**: 25220.38
- **Risk**: 46.87 points
- **TP 1RR**: 25314.12 ❌
- **TP 2RR**: 25360.98 ❌
- **TP 3RR**: 25407.85 ❌
- **TP 4RR**: 25454.72 ❌
- **TP 15RR**: 25970.25 ❌
- **PnL**: -46.87 points (-1.0R)
- **MFE**: 18.75 points
- **MAE**: 61.25 points

### Trade #1735 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-21 09:45:00
- **FVG 5m**: 25292.25 - 25307.50
- **Entrée**: 25311.25 @ 2025-10-21 10:47:00
- **Stop Loss**: 25217.63
- **Risk**: 93.62 points
- **TP 1RR**: 25404.87 ❌
- **TP 2RR**: 25498.48 ❌
- **TP 3RR**: 25592.10 ❌
- **TP 4RR**: 25685.71 ❌
- **TP 15RR**: 26715.48 ❌
- **PnL**: -93.62 points (-1.0R)
- **MFE**: 37.25 points
- **MAE**: 96.75 points

### Trade #1736 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-21 20:00:00
- **FVG 5m**: 25245.75 - 25249.75
- **Entrée**: 25252.25 @ 2025-10-21 20:47:00
- **Stop Loss**: 25201.89
- **Risk**: 50.36 points
- **TP 1RR**: 25302.61 ✅
- **TP 2RR**: 25352.96 ❌
- **TP 3RR**: 25403.32 ❌
- **TP 4RR**: 25453.68 ❌
- **TP 15RR**: 26007.61 ❌
- **PnL**: -50.36 points (-1.0R)
- **MFE**: 86.00 points
- **MAE**: 59.00 points

### Trade #1737 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 04:15:00
- **FVG 5m**: 25256.25 - 25259.75
- **Entrée**: 25269.00 @ 2025-10-22 04:55:00
- **Stop Loss**: 25218.88
- **Risk**: 50.12 points
- **TP 1RR**: 25319.12 ❌
- **TP 2RR**: 25369.23 ❌
- **TP 3RR**: 25419.35 ❌
- **TP 4RR**: 25469.46 ❌
- **TP 15RR**: 26020.74 ❌
- **PnL**: -50.12 points (-1.0R)
- **MFE**: 36.50 points
- **MAE**: 52.25 points

### Trade #1738 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 06:00:00
- **FVG 5m**: 25260.00 - 25270.50
- **Entrée**: 25272.00 @ 2025-10-22 08:13:00
- **Stop Loss**: 25214.89
- **Risk**: 57.11 points
- **TP 1RR**: 25329.11 ❌
- **TP 2RR**: 25386.23 ❌
- **TP 3RR**: 25443.34 ❌
- **TP 4RR**: 25500.46 ❌
- **TP 15RR**: 26128.71 ❌
- **PnL**: -57.11 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 58.50 points

### Trade #1739 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 07:00:00
- **FVG 5m**: 25260.00 - 25270.50
- **Entrée**: 25272.00 @ 2025-10-22 08:13:00
- **Stop Loss**: 25205.64
- **Risk**: 66.36 points
- **TP 1RR**: 25338.36 ❌
- **TP 2RR**: 25404.72 ❌
- **TP 3RR**: 25471.08 ❌
- **TP 4RR**: 25537.44 ❌
- **TP 15RR**: 26267.39 ❌
- **PnL**: -66.36 points (-1.0R)
- **MFE**: 6.50 points
- **MAE**: 78.75 points

### Trade #1740 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 08:30:00
- **FVG 5m**: 25226.50 - 25236.25
- **Entrée**: 25245.25 @ 2025-10-22 08:41:00
- **Stop Loss**: 25159.66
- **Risk**: 85.59 points
- **TP 1RR**: 25330.84 ❌
- **TP 2RR**: 25416.42 ❌
- **TP 3RR**: 25502.01 ❌
- **TP 4RR**: 25587.59 ❌
- **TP 15RR**: 26529.04 ❌
- **PnL**: -85.59 points (-1.0R)
- **MFE**: 44.00 points
- **MAE**: 100.00 points

### Trade #1741 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 08:30:00
- **FVG 5m**: 25226.50 - 25236.25
- **Entrée**: 25245.25 @ 2025-10-22 08:41:00
- **Stop Loss**: 25159.66
- **Risk**: 85.59 points
- **TP 1RR**: 25330.84 ❌
- **TP 2RR**: 25416.42 ❌
- **TP 3RR**: 25502.01 ❌
- **TP 4RR**: 25587.59 ❌
- **TP 15RR**: 26529.04 ❌
- **PnL**: -85.59 points (-1.0R)
- **MFE**: 44.00 points
- **MAE**: 100.00 points

### Trade #1742 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 08:30:00
- **FVG 5m**: 25226.50 - 25236.25
- **Entrée**: 25245.25 @ 2025-10-22 08:41:00
- **Stop Loss**: 25159.66
- **Risk**: 85.59 points
- **TP 1RR**: 25330.84 ❌
- **TP 2RR**: 25416.42 ❌
- **TP 3RR**: 25502.01 ❌
- **TP 4RR**: 25587.59 ❌
- **TP 15RR**: 26529.04 ❌
- **PnL**: -85.59 points (-1.0R)
- **MFE**: 44.00 points
- **MAE**: 100.00 points

### Trade #1743 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 09:15:00
- **FVG 5m**: 25142.25 - 25187.50
- **Entrée**: 25139.25 @ 2025-10-22 09:28:00
- **Stop Loss**: 25257.62
- **Risk**: 118.37 points
- **TP 1RR**: 25020.88 ✅
- **TP 2RR**: 24902.50 ✅
- **TP 3RR**: 24784.13 ❌
- **TP 4RR**: 24665.76 ❌
- **TP 15RR**: 23363.66 ❌
- **PnL**: -118.37 points (-1.0R)
- **MFE**: 334.50 points
- **MAE**: 124.75 points

### Trade #1744 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 09:15:00
- **FVG 5m**: 25142.25 - 25187.50
- **Entrée**: 25139.25 @ 2025-10-22 09:28:00
- **Stop Loss**: 25257.62
- **Risk**: 118.37 points
- **TP 1RR**: 25020.88 ✅
- **TP 2RR**: 24902.50 ✅
- **TP 3RR**: 24784.13 ❌
- **TP 4RR**: 24665.76 ❌
- **TP 15RR**: 23363.66 ❌
- **PnL**: -118.37 points (-1.0R)
- **MFE**: 334.50 points
- **MAE**: 124.75 points

### Trade #1745 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 09:30:00
- **FVG 5m**: 25071.75 - 25115.50
- **Entrée**: 25060.00 @ 2025-10-22 10:22:00
- **Stop Loss**: 25154.82
- **Risk**: 94.82 points
- **TP 1RR**: 24965.18 ✅
- **TP 2RR**: 24870.36 ✅
- **TP 3RR**: 24775.54 ❌
- **TP 4RR**: 24680.72 ❌
- **TP 15RR**: 23637.68 ❌
- **PnL**: -94.82 points (-1.0R)
- **MFE**: 255.25 points
- **MAE**: 102.00 points

### Trade #1746 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 09:45:00
- **FVG 5m**: 25139.00 - 25161.75
- **Entrée**: 25164.50 @ 2025-10-22 09:58:00
- **Stop Loss**: 25037.97
- **Risk**: 126.53 points
- **TP 1RR**: 25291.03 ❌
- **TP 2RR**: 25417.55 ❌
- **TP 3RR**: 25544.08 ❌
- **TP 4RR**: 25670.60 ❌
- **TP 15RR**: 27062.38 ❌
- **PnL**: -126.53 points (-1.0R)
- **MFE**: 27.75 points
- **MAE**: 134.25 points

### Trade #1747 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 10:30:00
- **FVG 5m**: 25043.75 - 25060.25
- **Entrée**: 25063.75 @ 2025-10-22 10:42:00
- **Stop Loss**: 24990.75
- **Risk**: 73.00 points
- **TP 1RR**: 25136.75 ❌
- **TP 2RR**: 25209.75 ❌
- **TP 3RR**: 25282.75 ❌
- **TP 4RR**: 25355.76 ❌
- **TP 15RR**: 26158.77 ❌
- **PnL**: -73.00 points (-1.0R)
- **MFE**: 68.00 points
- **MAE**: 153.75 points

### Trade #1748 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 10:30:00
- **FVG 5m**: 25043.75 - 25060.25
- **Entrée**: 25063.75 @ 2025-10-22 10:42:00
- **Stop Loss**: 24990.75
- **Risk**: 73.00 points
- **TP 1RR**: 25136.75 ❌
- **TP 2RR**: 25209.75 ❌
- **TP 3RR**: 25282.75 ❌
- **TP 4RR**: 25355.76 ❌
- **TP 15RR**: 26158.77 ❌
- **PnL**: -73.00 points (-1.0R)
- **MFE**: 68.00 points
- **MAE**: 153.75 points

### Trade #1749 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 11:30:00
- **FVG 5m**: 24874.25 - 24878.50
- **Entrée**: 24879.75 @ 2025-10-22 13:03:00
- **Stop Loss**: 24854.57
- **Risk**: 25.18 points
- **TP 1RR**: 24904.93 ✅
- **TP 2RR**: 24930.12 ❌
- **TP 3RR**: 24955.30 ❌
- **TP 4RR**: 24980.48 ❌
- **TP 15RR**: 25257.50 ❌
- **PnL**: -25.18 points (-1.0R)
- **MFE**: 28.75 points
- **MAE**: 26.00 points

### Trade #1750 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 12:00:00
- **FVG 5m**: 24942.00 - 24947.25
- **Entrée**: 24933.50 @ 2025-10-22 12:14:00
- **Stop Loss**: 25023.76
- **Risk**: 90.26 points
- **TP 1RR**: 24843.24 ✅
- **TP 2RR**: 24752.99 ❌
- **TP 3RR**: 24662.73 ❌
- **TP 4RR**: 24572.48 ❌
- **TP 15RR**: 23579.67 ❌
- **PnL**: -90.26 points (-1.0R)
- **MFE**: 128.75 points
- **MAE**: 101.25 points

### Trade #1751 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 12:45:00
- **FVG 5m**: 24874.25 - 24878.50
- **Entrée**: 24879.75 @ 2025-10-22 13:03:00
- **Stop Loss**: 24792.35
- **Risk**: 87.40 points
- **TP 1RR**: 24967.15 ✅
- **TP 2RR**: 25054.55 ✅
- **TP 3RR**: 25141.96 ✅
- **TP 4RR**: 25229.36 ✅
- **TP 15RR**: 26190.79 ✅
- **PnL**: 1311.04 points (15.0R)
- **MFE**: 1312.00 points
- **MAE**: 52.75 points

### Trade #1752 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-22 19:00:00
- **FVG 5m**: 24995.50 - 25002.50
- **Entrée**: 25003.25 @ 2025-10-22 19:12:00
- **Stop Loss**: 24938.77
- **Risk**: 64.48 points
- **TP 1RR**: 25067.73 ✅
- **TP 2RR**: 25132.20 ❌
- **TP 3RR**: 25196.68 ❌
- **TP 4RR**: 25261.15 ❌
- **TP 15RR**: 25970.38 ❌
- **PnL**: -64.48 points (-1.0R)
- **MFE**: 124.75 points
- **MAE**: 66.25 points

### Trade #1753 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-22 23:00:00
- **FVG 5m**: 25074.50 - 25078.25
- **Entrée**: 25072.50 @ 2025-10-22 23:14:00
- **Stop Loss**: 25107.30
- **Risk**: 34.80 points
- **TP 1RR**: 25037.70 ❌
- **TP 2RR**: 25002.91 ❌
- **TP 3RR**: 24968.11 ❌
- **TP 4RR**: 24933.31 ❌
- **TP 15RR**: 24550.54 ❌
- **PnL**: -34.80 points (-1.0R)
- **MFE**: 19.00 points
- **MAE**: 35.00 points

### Trade #1754 - ✅ GAGNANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-23 07:30:00
- **FVG 5m**: 24949.75 - 24960.50
- **Entrée**: 24961.50 @ 2025-10-23 07:43:00
- **Stop Loss**: 24924.53
- **Risk**: 36.97 points
- **TP 1RR**: 24998.47 ✅
- **TP 2RR**: 25035.44 ✅
- **TP 3RR**: 25072.41 ✅
- **TP 4RR**: 25109.37 ✅
- **TP 15RR**: 25516.03 ✅
- **PnL**: 554.53 points (15.0R)
- **MFE**: 558.50 points
- **MAE**: 20.75 points

### Trade #1755 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-23 08:30:00
- **FVG 5m**: 25077.50 - 25091.25
- **Entrée**: 25092.25 @ 2025-10-23 08:44:00
- **Stop Loss**: 24986.50
- **Risk**: 105.75 points
- **TP 1RR**: 25198.00 ✅
- **TP 2RR**: 25303.75 ✅
- **TP 3RR**: 25409.50 ✅
- **TP 4RR**: 25515.25 ✅
- **TP 15RR**: 26678.49 ❌
- **PnL**: -105.75 points (-1.0R)
- **MFE**: 1306.75 points
- **MAE**: 144.25 points

### Trade #1756 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-23 20:15:00
- **FVG 5m**: 25305.00 - 25315.00
- **Entrée**: 25303.75 @ 2025-10-23 20:29:00
- **Stop Loss**: 25333.91
- **Risk**: 30.16 points
- **TP 1RR**: 25273.59 ❌
- **TP 2RR**: 25243.43 ❌
- **TP 3RR**: 25213.27 ❌
- **TP 4RR**: 25183.11 ❌
- **TP 15RR**: 24851.34 ❌
- **PnL**: -30.16 points (-1.0R)
- **MFE**: 6.75 points
- **MAE**: 31.25 points

### Trade #1757 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-24 11:15:00
- **FVG 5m**: 25550.00 - 25554.00
- **Entrée**: 25549.25 @ 2025-10-24 12:59:00
- **Stop Loss**: 25575.78
- **Risk**: 26.53 points
- **TP 1RR**: 25522.72 ✅
- **TP 2RR**: 25496.19 ❌
- **TP 3RR**: 25469.66 ❌
- **TP 4RR**: 25443.12 ❌
- **TP 15RR**: 25151.28 ❌
- **PnL**: -26.53 points (-1.0R)
- **MFE**: 51.75 points
- **MAE**: 219.00 points

### Trade #1758 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-27 08:15:00
- **FVG 5m**: 25844.50 - 25848.75
- **Entrée**: 25840.50 @ 2025-10-27 09:17:00
- **Stop Loss**: 25852.42
- **Risk**: 11.92 points
- **TP 1RR**: 25828.58 ✅
- **TP 2RR**: 25816.66 ❌
- **TP 3RR**: 25804.74 ❌
- **TP 4RR**: 25792.82 ❌
- **TP 15RR**: 25661.70 ❌
- **PnL**: -11.92 points (-1.0R)
- **MFE**: 17.50 points
- **MAE**: 22.75 points

### Trade #1759 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-27 08:30:00
- **FVG 5m**: 25854.50 - 25862.25
- **Entrée**: 25871.00 @ 2025-10-27 09:03:00
- **Stop Loss**: 25783.60
- **Risk**: 87.40 points
- **TP 1RR**: 25958.40 ✅
- **TP 2RR**: 26045.80 ✅
- **TP 3RR**: 26133.19 ✅
- **TP 4RR**: 26220.59 ✅
- **TP 15RR**: 27181.97 ❌
- **PnL**: -87.40 points (-1.0R)
- **MFE**: 528.00 points
- **MAE**: 108.00 points

### Trade #1760 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 09:00:00
- **FVG 5m**: 26289.50 - 26298.75
- **Entrée**: 26287.75 @ 2025-10-29 09:42:00
- **Stop Loss**: 26339.66
- **Risk**: 51.91 points
- **TP 1RR**: 26235.84 ✅
- **TP 2RR**: 26183.92 ✅
- **TP 3RR**: 26132.01 ✅
- **TP 4RR**: 26080.10 ✅
- **TP 15RR**: 25509.05 ❌
- **PnL**: -51.91 points (-1.0R)
- **MFE**: 238.50 points
- **MAE**: 62.25 points

### Trade #1761 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 09:00:00
- **FVG 5m**: 26289.50 - 26298.75
- **Entrée**: 26287.75 @ 2025-10-29 09:42:00
- **Stop Loss**: 26339.66
- **Risk**: 51.91 points
- **TP 1RR**: 26235.84 ✅
- **TP 2RR**: 26183.92 ✅
- **TP 3RR**: 26132.01 ✅
- **TP 4RR**: 26080.10 ✅
- **TP 15RR**: 25509.05 ❌
- **PnL**: -51.91 points (-1.0R)
- **MFE**: 238.50 points
- **MAE**: 62.25 points

### Trade #1762 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 11:00:00
- **FVG 5m**: 26232.25 - 26242.75
- **Entrée**: 26244.00 @ 2025-10-29 11:23:00
- **Stop Loss**: 26190.15
- **Risk**: 53.85 points
- **TP 1RR**: 26297.85 ❌
- **TP 2RR**: 26351.70 ❌
- **TP 3RR**: 26405.55 ❌
- **TP 4RR**: 26459.41 ❌
- **TP 15RR**: 27051.77 ❌
- **PnL**: -53.85 points (-1.0R)
- **MFE**: 46.00 points
- **MAE**: 91.50 points

### Trade #1763 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 11:15:00
- **FVG 5m**: 26234.50 - 26239.00
- **Entrée**: 26240.50 @ 2025-10-29 12:39:00
- **Stop Loss**: 26208.14
- **Risk**: 32.36 points
- **TP 1RR**: 26272.86 ✅
- **TP 2RR**: 26305.22 ❌
- **TP 3RR**: 26337.58 ❌
- **TP 4RR**: 26369.94 ❌
- **TP 15RR**: 26725.91 ❌
- **PnL**: -32.36 points (-1.0R)
- **MFE**: 49.50 points
- **MAE**: 35.75 points

### Trade #1764 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 12:15:00
- **FVG 5m**: 26234.50 - 26238.25
- **Entrée**: 26227.50 @ 2025-10-29 12:30:00
- **Stop Loss**: 26281.38
- **Risk**: 53.88 points
- **TP 1RR**: 26173.62 ❌
- **TP 2RR**: 26119.73 ❌
- **TP 3RR**: 26065.85 ❌
- **TP 4RR**: 26011.96 ❌
- **TP 15RR**: 25419.24 ❌
- **PnL**: -53.88 points (-1.0R)
- **MFE**: 4.50 points
- **MAE**: 62.50 points

### Trade #1765 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 13:30:00
- **FVG 5m**: 26234.50 - 26248.50
- **Entrée**: 26213.00 @ 2025-10-29 15:06:00
- **Stop Loss**: 26296.64
- **Risk**: 83.64 points
- **TP 1RR**: 26129.36 ❌
- **TP 2RR**: 26045.72 ❌
- **TP 3RR**: 25962.07 ❌
- **TP 4RR**: 25878.43 ❌
- **TP 15RR**: 24958.37 ❌
- **PnL**: -83.64 points (-1.0R)
- **MFE**: 63.00 points
- **MAE**: 87.25 points

### Trade #1766 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 13:30:00
- **FVG 5m**: 26234.50 - 26248.50
- **Entrée**: 26213.00 @ 2025-10-29 15:06:00
- **Stop Loss**: 26296.64
- **Risk**: 83.64 points
- **TP 1RR**: 26129.36 ❌
- **TP 2RR**: 26045.72 ❌
- **TP 3RR**: 25962.07 ❌
- **TP 4RR**: 25878.43 ❌
- **TP 15RR**: 24958.37 ❌
- **PnL**: -83.64 points (-1.0R)
- **MFE**: 63.00 points
- **MAE**: 87.25 points

### Trade #1767 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 13:45:00
- **FVG 5m**: 26219.50 - 26224.50
- **Entrée**: 26232.00 @ 2025-10-29 14:48:00
- **Stop Loss**: 26047.97
- **Risk**: 184.03 points
- **TP 1RR**: 26416.03 ❌
- **TP 2RR**: 26600.06 ❌
- **TP 3RR**: 26784.09 ❌
- **TP 4RR**: 26968.12 ❌
- **TP 15RR**: 28992.46 ❌
- **PnL**: -184.03 points (-1.0R)
- **MFE**: 167.00 points
- **MAE**: 189.00 points

### Trade #1768 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 15:00:00
- **FVG 5m**: 26212.50 - 26229.25
- **Entrée**: 26193.50 @ 2025-10-29 17:00:00
- **Stop Loss**: 26392.94
- **Risk**: 199.44 points
- **TP 1RR**: 25994.06 ❌
- **TP 2RR**: 25794.62 ❌
- **TP 3RR**: 25595.18 ❌
- **TP 4RR**: 25395.74 ❌
- **TP 15RR**: 23201.90 ❌
- **PnL**: -199.44 points (-1.0R)
- **MFE**: 39.25 points
- **MAE**: 200.25 points

### Trade #1769 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 15:00:00
- **FVG 5m**: 26212.50 - 26229.25
- **Entrée**: 26193.50 @ 2025-10-29 17:00:00
- **Stop Loss**: 26392.94
- **Risk**: 199.44 points
- **TP 1RR**: 25994.06 ❌
- **TP 2RR**: 25794.62 ❌
- **TP 3RR**: 25595.18 ❌
- **TP 4RR**: 25395.74 ❌
- **TP 15RR**: 23201.90 ❌
- **PnL**: -199.44 points (-1.0R)
- **MFE**: 39.25 points
- **MAE**: 200.25 points

### Trade #1770 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-29 15:00:00
- **FVG 5m**: 26199.25 - 26222.75
- **Entrée**: 26230.75 @ 2025-10-29 18:22:00
- **Stop Loss**: 26146.67
- **Risk**: 84.08 points
- **TP 1RR**: 26314.83 ✅
- **TP 2RR**: 26398.91 ✅
- **TP 3RR**: 26482.99 ❌
- **TP 4RR**: 26567.07 ❌
- **TP 15RR**: 27491.95 ❌
- **PnL**: -84.08 points (-1.0R)
- **MFE**: 168.25 points
- **MAE**: 90.75 points

### Trade #1771 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 22:15:00
- **FVG 5m**: 26355.00 - 26367.75
- **Entrée**: 26345.25 @ 2025-10-29 23:05:00
- **Stop Loss**: 26406.95
- **Risk**: 61.70 points
- **TP 1RR**: 26283.55 ✅
- **TP 2RR**: 26221.86 ✅
- **TP 3RR**: 26160.16 ✅
- **TP 4RR**: 26098.46 ✅
- **TP 15RR**: 25419.80 ✅
- **PnL**: 925.45 points (15.0R)
- **MFE**: 927.25 points
- **MAE**: 5.50 points

### Trade #1772 - ➖ BE

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-29 23:00:00
- **FVG 5m**: 26245.00 - 26303.00
- **Entrée**: 26217.25 @ 2025-10-29 23:13:00
- **Stop Loss**: 26395.94
- **Risk**: 178.69 points
- **TP 1RR**: 26038.56 ✅
- **TP 2RR**: 25859.87 ✅
- **TP 3RR**: 25681.18 ✅
- **TP 4RR**: 25502.48 ✅
- **TP 15RR**: 23536.88 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1508.00 points
- **MAE**: 111.00 points

### Trade #1773 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26025.75 - 26040.00
- **Entrée**: 26014.75 @ 2025-10-30 09:51:00
- **Stop Loss**: 26140.56
- **Risk**: 125.81 points
- **TP 1RR**: 25888.94 ✅
- **TP 2RR**: 25763.12 ❌
- **TP 3RR**: 25637.31 ❌
- **TP 4RR**: 25511.49 ❌
- **TP 15RR**: 24127.54 ❌
- **PnL**: -125.81 points (-1.0R)
- **MFE**: 161.75 points
- **MAE**: 130.75 points

### Trade #1774 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26025.75 - 26040.00
- **Entrée**: 26014.75 @ 2025-10-30 09:51:00
- **Stop Loss**: 26140.56
- **Risk**: 125.81 points
- **TP 1RR**: 25888.94 ✅
- **TP 2RR**: 25763.12 ❌
- **TP 3RR**: 25637.31 ❌
- **TP 4RR**: 25511.49 ❌
- **TP 15RR**: 24127.54 ❌
- **PnL**: -125.81 points (-1.0R)
- **MFE**: 161.75 points
- **MAE**: 130.75 points

### Trade #1775 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26025.75 - 26040.00
- **Entrée**: 26014.75 @ 2025-10-30 09:51:00
- **Stop Loss**: 26140.56
- **Risk**: 125.81 points
- **TP 1RR**: 25888.94 ✅
- **TP 2RR**: 25763.12 ❌
- **TP 3RR**: 25637.31 ❌
- **TP 4RR**: 25511.49 ❌
- **TP 15RR**: 24127.54 ❌
- **PnL**: -125.81 points (-1.0R)
- **MFE**: 161.75 points
- **MAE**: 130.75 points

### Trade #1776 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-30 08:30:00
- **FVG 5m**: 26025.75 - 26040.00
- **Entrée**: 26014.75 @ 2025-10-30 09:51:00
- **Stop Loss**: 26140.56
- **Risk**: 125.81 points
- **TP 1RR**: 25888.94 ✅
- **TP 2RR**: 25763.12 ❌
- **TP 3RR**: 25637.31 ❌
- **TP 4RR**: 25511.49 ❌
- **TP 15RR**: 24127.54 ❌
- **PnL**: -125.81 points (-1.0R)
- **MFE**: 161.75 points
- **MAE**: 130.75 points

### Trade #1777 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:30:00
- **FVG 5m**: 25996.00 - 26053.50
- **Entrée**: 26056.00 @ 2025-10-30 08:48:00
- **Stop Loss**: 25929.28
- **Risk**: 126.72 points
- **TP 1RR**: 26182.72 ❌
- **TP 2RR**: 26309.44 ❌
- **TP 3RR**: 26436.16 ❌
- **TP 4RR**: 26562.88 ❌
- **TP 15RR**: 27956.82 ❌
- **PnL**: -126.72 points (-1.0R)
- **MFE**: 126.50 points
- **MAE**: 137.75 points

### Trade #1778 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:30:00
- **FVG 5m**: 25996.00 - 26053.50
- **Entrée**: 26056.00 @ 2025-10-30 08:48:00
- **Stop Loss**: 25929.28
- **Risk**: 126.72 points
- **TP 1RR**: 26182.72 ❌
- **TP 2RR**: 26309.44 ❌
- **TP 3RR**: 26436.16 ❌
- **TP 4RR**: 26562.88 ❌
- **TP 15RR**: 27956.82 ❌
- **PnL**: -126.72 points (-1.0R)
- **MFE**: 126.50 points
- **MAE**: 137.75 points

### Trade #1779 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:45:00
- **FVG 5m**: 26013.75 - 26023.00
- **Entrée**: 26031.50 @ 2025-10-30 11:04:00
- **Stop Loss**: 25950.77
- **Risk**: 80.73 points
- **TP 1RR**: 26112.23 ❌
- **TP 2RR**: 26192.96 ❌
- **TP 3RR**: 26273.70 ❌
- **TP 4RR**: 26354.43 ❌
- **TP 15RR**: 27242.48 ❌
- **PnL**: -80.73 points (-1.0R)
- **MFE**: 65.50 points
- **MAE**: 83.50 points

### Trade #1780 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 08:45:00
- **FVG 5m**: 26013.75 - 26023.00
- **Entrée**: 26031.50 @ 2025-10-30 11:04:00
- **Stop Loss**: 25950.77
- **Risk**: 80.73 points
- **TP 1RR**: 26112.23 ❌
- **TP 2RR**: 26192.96 ❌
- **TP 3RR**: 26273.70 ❌
- **TP 4RR**: 26354.43 ❌
- **TP 15RR**: 27242.48 ❌
- **PnL**: -80.73 points (-1.0R)
- **MFE**: 65.50 points
- **MAE**: 83.50 points

### Trade #1781 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:00:00
- **FVG 5m**: 26006.00 - 26011.25
- **Entrée**: 26016.25 @ 2025-10-30 15:16:00
- **Stop Loss**: 25840.07
- **Risk**: 176.18 points
- **TP 1RR**: 26192.43 ✅
- **TP 2RR**: 26368.60 ❌
- **TP 3RR**: 26544.78 ❌
- **TP 4RR**: 26720.96 ❌
- **TP 15RR**: 28658.90 ❌
- **PnL**: -176.18 points (-1.0R)
- **MFE**: 257.75 points
- **MAE**: 184.75 points

### Trade #1782 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:00:00
- **FVG 5m**: 26006.00 - 26011.25
- **Entrée**: 26016.25 @ 2025-10-30 15:16:00
- **Stop Loss**: 25840.07
- **Risk**: 176.18 points
- **TP 1RR**: 26192.43 ✅
- **TP 2RR**: 26368.60 ❌
- **TP 3RR**: 26544.78 ❌
- **TP 4RR**: 26720.96 ❌
- **TP 15RR**: 28658.90 ❌
- **PnL**: -176.18 points (-1.0R)
- **MFE**: 257.75 points
- **MAE**: 184.75 points

### Trade #1783 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:00:00
- **FVG 5m**: 26006.00 - 26011.25
- **Entrée**: 26016.25 @ 2025-10-30 15:16:00
- **Stop Loss**: 25840.07
- **Risk**: 176.18 points
- **TP 1RR**: 26192.43 ✅
- **TP 2RR**: 26368.60 ❌
- **TP 3RR**: 26544.78 ❌
- **TP 4RR**: 26720.96 ❌
- **TP 15RR**: 28658.90 ❌
- **PnL**: -176.18 points (-1.0R)
- **MFE**: 257.75 points
- **MAE**: 184.75 points

### Trade #1784 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 15:45:00
- **FVG 5m**: 26148.75 - 26151.50
- **Entrée**: 26154.50 @ 2025-10-30 18:42:00
- **Stop Loss**: 26107.94
- **Risk**: 46.56 points
- **TP 1RR**: 26201.06 ✅
- **TP 2RR**: 26247.62 ✅
- **TP 3RR**: 26294.18 ❌
- **TP 4RR**: 26340.74 ❌
- **TP 15RR**: 26852.91 ❌
- **PnL**: -46.56 points (-1.0R)
- **MFE**: 119.50 points
- **MAE**: 53.25 points

### Trade #1785 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 18:30:00
- **FVG 5m**: 26148.75 - 26151.50
- **Entrée**: 26154.50 @ 2025-10-30 18:42:00
- **Stop Loss**: 26114.44
- **Risk**: 40.06 points
- **TP 1RR**: 26194.56 ✅
- **TP 2RR**: 26234.63 ✅
- **TP 3RR**: 26274.69 ❌
- **TP 4RR**: 26314.76 ❌
- **TP 15RR**: 26755.46 ❌
- **PnL**: -40.06 points (-1.0R)
- **MFE**: 119.50 points
- **MAE**: 42.25 points

### Trade #1786 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-30 19:15:00
- **FVG 5m**: 26180.25 - 26185.25
- **Entrée**: 26186.25 @ 2025-10-30 19:27:00
- **Stop Loss**: 26139.17
- **Risk**: 47.08 points
- **TP 1RR**: 26233.33 ✅
- **TP 2RR**: 26280.40 ❌
- **TP 3RR**: 26327.48 ❌
- **TP 4RR**: 26374.55 ❌
- **TP 15RR**: 26892.39 ❌
- **PnL**: -47.08 points (-1.0R)
- **MFE**: 87.75 points
- **MAE**: 53.00 points

### Trade #1787 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 02:30:00
- **FVG 5m**: 26198.50 - 26201.75
- **Entrée**: 26205.50 @ 2025-10-31 02:42:00
- **Stop Loss**: 26160.16
- **Risk**: 45.34 points
- **TP 1RR**: 26250.84 ❌
- **TP 2RR**: 26296.17 ❌
- **TP 3RR**: 26341.51 ❌
- **TP 4RR**: 26386.85 ❌
- **TP 15RR**: 26885.55 ❌
- **PnL**: -45.34 points (-1.0R)
- **MFE**: 14.25 points
- **MAE**: 46.25 points

### Trade #1788 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 03:00:00
- **FVG 5m**: 26174.00 - 26187.25
- **Entrée**: 26160.50 @ 2025-10-31 03:14:00
- **Stop Loss**: 26231.11
- **Risk**: 70.61 points
- **TP 1RR**: 26089.89 ❌
- **TP 2RR**: 26019.28 ❌
- **TP 3RR**: 25948.67 ❌
- **TP 4RR**: 25878.06 ❌
- **TP 15RR**: 25101.36 ❌
- **PnL**: -70.61 points (-1.0R)
- **MFE**: 3.00 points
- **MAE**: 71.75 points

### Trade #1789 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 03:00:00
- **FVG 5m**: 26174.00 - 26187.25
- **Entrée**: 26160.50 @ 2025-10-31 03:14:00
- **Stop Loss**: 26231.11
- **Risk**: 70.61 points
- **TP 1RR**: 26089.89 ❌
- **TP 2RR**: 26019.28 ❌
- **TP 3RR**: 25948.67 ❌
- **TP 4RR**: 25878.06 ❌
- **TP 15RR**: 25101.36 ❌
- **PnL**: -70.61 points (-1.0R)
- **MFE**: 3.00 points
- **MAE**: 71.75 points

### Trade #1790 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-10-31 07:45:00
- **FVG 5m**: 26173.75 - 26191.50
- **Entrée**: 26158.75 @ 2025-10-31 08:31:00
- **Stop Loss**: 26243.87
- **Risk**: 85.12 points
- **TP 1RR**: 26073.63 ✅
- **TP 2RR**: 25988.52 ✅
- **TP 3RR**: 25903.40 ✅
- **TP 4RR**: 25818.29 ❌
- **TP 15RR**: 24882.02 ❌
- **PnL**: -85.12 points (-1.0R)
- **MFE**: 270.00 points
- **MAE**: 101.00 points

### Trade #1791 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26087.45
- **Risk**: 71.80 points
- **TP 1RR**: 26231.05 ❌
- **TP 2RR**: 26302.85 ❌
- **TP 3RR**: 26374.65 ❌
- **TP 4RR**: 26446.45 ❌
- **TP 15RR**: 27236.25 ❌
- **PnL**: -71.80 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 75.75 points

### Trade #1792 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26087.45
- **Risk**: 71.80 points
- **TP 1RR**: 26231.05 ❌
- **TP 2RR**: 26302.85 ❌
- **TP 3RR**: 26374.65 ❌
- **TP 4RR**: 26446.45 ❌
- **TP 15RR**: 27236.25 ❌
- **PnL**: -71.80 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 75.75 points

### Trade #1793 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26087.45
- **Risk**: 71.80 points
- **TP 1RR**: 26231.05 ❌
- **TP 2RR**: 26302.85 ❌
- **TP 3RR**: 26374.65 ❌
- **TP 4RR**: 26446.45 ❌
- **TP 15RR**: 27236.25 ❌
- **PnL**: -71.80 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 75.75 points

### Trade #1794 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26087.45
- **Risk**: 71.80 points
- **TP 1RR**: 26231.05 ❌
- **TP 2RR**: 26302.85 ❌
- **TP 3RR**: 26374.65 ❌
- **TP 4RR**: 26446.45 ❌
- **TP 15RR**: 27236.25 ❌
- **PnL**: -71.80 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 75.75 points

### Trade #1795 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 09:30:00
- **FVG 5m**: 26150.75 - 26159.00
- **Entrée**: 26159.25 @ 2025-10-31 09:41:00
- **Stop Loss**: 26087.45
- **Risk**: 71.80 points
- **TP 1RR**: 26231.05 ❌
- **TP 2RR**: 26302.85 ❌
- **TP 3RR**: 26374.65 ❌
- **TP 4RR**: 26446.45 ❌
- **TP 15RR**: 27236.25 ❌
- **PnL**: -71.80 points (-1.0R)
- **MFE**: 23.50 points
- **MAE**: 75.75 points

### Trade #1796 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-10-31 14:15:00
- **FVG 5m**: 25988.50 - 26012.75
- **Entrée**: 26031.25 @ 2025-11-02 17:00:00
- **Stop Loss**: 26011.99
- **Risk**: 19.26 points
- **TP 1RR**: 26050.51 ✅
- **TP 2RR**: 26069.78 ✅
- **TP 3RR**: 26089.04 ✅
- **TP 4RR**: 26108.30 ✅
- **TP 15RR**: 26320.19 ❌
- **PnL**: -19.26 points (-1.0R)
- **MFE**: 234.75 points
- **MAE**: 25.00 points

### Trade #1797 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-03 02:00:00
- **FVG 5m**: 26057.25 - 26063.00
- **Entrée**: 26064.50 @ 2025-11-03 02:26:00
- **Stop Loss**: 26006.49
- **Risk**: 58.01 points
- **TP 1RR**: 26122.51 ✅
- **TP 2RR**: 26180.52 ✅
- **TP 3RR**: 26238.53 ✅
- **TP 4RR**: 26296.54 ❌
- **TP 15RR**: 26934.65 ❌
- **PnL**: -58.01 points (-1.0R)
- **MFE**: 201.50 points
- **MAE**: 58.25 points

### Trade #1798 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:00:00
- **FVG 5m**: 26188.00 - 26226.00
- **Entrée**: 26182.25 @ 2025-11-03 08:38:00
- **Stop Loss**: 26272.88
- **Risk**: 90.63 points
- **TP 1RR**: 26091.62 ✅
- **TP 2RR**: 26000.99 ✅
- **TP 3RR**: 25910.36 ✅
- **TP 4RR**: 25819.73 ✅
- **TP 15RR**: 24822.80 ✅
- **PnL**: 1359.45 points (15.0R)
- **MFE**: 1361.50 points
- **MAE**: 8.00 points

### Trade #1799 - ➖ BE

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:30:00
- **FVG 5m**: 26146.25 - 26153.25
- **Entrée**: 26145.00 @ 2025-11-03 08:53:00
- **Stop Loss**: 26279.13
- **Risk**: 134.13 points
- **TP 1RR**: 26010.87 ✅
- **TP 2RR**: 25876.73 ✅
- **TP 3RR**: 25742.60 ✅
- **TP 4RR**: 25608.47 ✅
- **TP 15RR**: 24133.00 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1435.75 points
- **MAE**: 35.00 points

### Trade #1800 - ➖ BE

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:30:00
- **FVG 5m**: 26146.25 - 26153.25
- **Entrée**: 26145.00 @ 2025-11-03 08:53:00
- **Stop Loss**: 26279.13
- **Risk**: 134.13 points
- **TP 1RR**: 26010.87 ✅
- **TP 2RR**: 25876.73 ✅
- **TP 3RR**: 25742.60 ✅
- **TP 4RR**: 25608.47 ✅
- **TP 15RR**: 24133.00 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1435.75 points
- **MAE**: 35.00 points

### Trade #1801 - ➖ BE

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 08:30:00
- **FVG 5m**: 26146.25 - 26153.25
- **Entrée**: 26145.00 @ 2025-11-03 08:53:00
- **Stop Loss**: 26279.13
- **Risk**: 134.13 points
- **TP 1RR**: 26010.87 ✅
- **TP 2RR**: 25876.73 ✅
- **TP 3RR**: 25742.60 ✅
- **TP 4RR**: 25608.47 ✅
- **TP 15RR**: 24133.00 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1435.75 points
- **MAE**: 35.00 points

### Trade #1802 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 09:15:00
- **FVG 5m**: 26044.00 - 26081.00
- **Entrée**: 26043.75 @ 2025-11-03 09:26:00
- **Stop Loss**: 26141.06
- **Risk**: 97.31 points
- **TP 1RR**: 25946.44 ❌
- **TP 2RR**: 25849.12 ❌
- **TP 3RR**: 25751.81 ❌
- **TP 4RR**: 25654.49 ❌
- **TP 15RR**: 24584.04 ❌
- **PnL**: -97.31 points (-1.0R)
- **MFE**: 28.25 points
- **MAE**: 100.25 points

### Trade #1803 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 11:15:00
- **FVG 5m**: 26149.75 - 26152.50
- **Entrée**: 26144.75 @ 2025-11-03 12:47:00
- **Stop Loss**: 26157.07
- **Risk**: 12.32 points
- **TP 1RR**: 26132.43 ✅
- **TP 2RR**: 26120.11 ✅
- **TP 3RR**: 26107.78 ✅
- **TP 4RR**: 26095.46 ✅
- **TP 15RR**: 25959.92 ❌
- **PnL**: -12.32 points (-1.0R)
- **MFE**: 78.50 points
- **MAE**: 35.25 points

### Trade #1804 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 11:15:00
- **FVG 5m**: 26149.75 - 26152.50
- **Entrée**: 26144.75 @ 2025-11-03 12:47:00
- **Stop Loss**: 26157.07
- **Risk**: 12.32 points
- **TP 1RR**: 26132.43 ✅
- **TP 2RR**: 26120.11 ✅
- **TP 3RR**: 26107.78 ✅
- **TP 4RR**: 26095.46 ✅
- **TP 15RR**: 25959.92 ❌
- **PnL**: -12.32 points (-1.0R)
- **MFE**: 78.50 points
- **MAE**: 35.25 points

### Trade #1805 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 15:00:00
- **FVG 5m**: 26127.50 - 26131.00
- **Entrée**: 26123.75 @ 2025-11-03 15:12:00
- **Stop Loss**: 26193.09
- **Risk**: 69.34 points
- **TP 1RR**: 26054.41 ✅
- **TP 2RR**: 25985.07 ✅
- **TP 3RR**: 25915.73 ✅
- **TP 4RR**: 25846.39 ✅
- **TP 15RR**: 25083.65 ✅
- **PnL**: 1040.10 points (15.0R)
- **MFE**: 1059.25 points
- **MAE**: 7.25 points

### Trade #1806 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-03 23:30:00
- **FVG 5m**: 25849.75 - 25873.75
- **Entrée**: 25845.25 @ 2025-11-03 23:45:00
- **Stop Loss**: 25899.44
- **Risk**: 54.19 points
- **TP 1RR**: 25791.06 ✅
- **TP 2RR**: 25736.86 ✅
- **TP 3RR**: 25682.67 ✅
- **TP 4RR**: 25628.48 ✅
- **TP 15RR**: 25032.35 ✅
- **PnL**: 812.90 points (15.0R)
- **MFE**: 815.00 points
- **MAE**: 48.25 points

### Trade #1807 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 00:00:00
- **FVG 5m**: 25775.00 - 25780.00
- **Entrée**: 25788.25 @ 2025-11-04 00:47:00
- **Stop Loss**: 25739.87
- **Risk**: 48.38 points
- **TP 1RR**: 25836.63 ❌
- **TP 2RR**: 25885.00 ❌
- **TP 3RR**: 25933.38 ❌
- **TP 4RR**: 25981.76 ❌
- **TP 15RR**: 26513.90 ❌
- **PnL**: -48.38 points (-1.0R)
- **MFE**: 11.25 points
- **MAE**: 52.75 points

### Trade #1808 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 00:15:00
- **FVG 5m**: 25766.75 - 25774.00
- **Entrée**: 25762.50 @ 2025-11-04 01:02:00
- **Stop Loss**: 25811.90
- **Risk**: 49.40 points
- **TP 1RR**: 25713.10 ✅
- **TP 2RR**: 25663.70 ✅
- **TP 3RR**: 25614.30 ❌
- **TP 4RR**: 25564.90 ❌
- **TP 15RR**: 25021.51 ❌
- **PnL**: -49.40 points (-1.0R)
- **MFE**: 117.50 points
- **MAE**: 60.25 points

### Trade #1809 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 00:15:00
- **FVG 5m**: 25766.75 - 25774.00
- **Entrée**: 25762.50 @ 2025-11-04 01:02:00
- **Stop Loss**: 25811.90
- **Risk**: 49.40 points
- **TP 1RR**: 25713.10 ✅
- **TP 2RR**: 25663.70 ✅
- **TP 3RR**: 25614.30 ❌
- **TP 4RR**: 25564.90 ❌
- **TP 15RR**: 25021.51 ❌
- **PnL**: -49.40 points (-1.0R)
- **MFE**: 117.50 points
- **MAE**: 60.25 points

### Trade #1810 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 04:15:00
- **FVG 5m**: 25717.25 - 25735.50
- **Entrée**: 25740.50 @ 2025-11-04 04:33:00
- **Stop Loss**: 25658.41
- **Risk**: 82.09 points
- **TP 1RR**: 25822.59 ✅
- **TP 2RR**: 25904.67 ❌
- **TP 3RR**: 25986.76 ❌
- **TP 4RR**: 26068.84 ❌
- **TP 15RR**: 26971.78 ❌
- **PnL**: -82.09 points (-1.0R)
- **MFE**: 153.00 points
- **MAE**: 86.50 points

### Trade #1811 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 08:45:00
- **FVG 5m**: 25855.75 - 25864.00
- **Entrée**: 25875.25 @ 2025-11-04 08:59:00
- **Stop Loss**: 25722.38
- **Risk**: 152.87 points
- **TP 1RR**: 26028.12 ❌
- **TP 2RR**: 26180.99 ❌
- **TP 3RR**: 26333.85 ❌
- **TP 4RR**: 26486.72 ❌
- **TP 15RR**: 28168.26 ❌
- **PnL**: -152.87 points (-1.0R)
- **MFE**: 18.25 points
- **MAE**: 153.50 points

### Trade #1812 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 08:45:00
- **FVG 5m**: 25855.75 - 25864.00
- **Entrée**: 25875.25 @ 2025-11-04 08:59:00
- **Stop Loss**: 25722.38
- **Risk**: 152.87 points
- **TP 1RR**: 26028.12 ❌
- **TP 2RR**: 26180.99 ❌
- **TP 3RR**: 26333.85 ❌
- **TP 4RR**: 26486.72 ❌
- **TP 15RR**: 28168.26 ❌
- **PnL**: -152.87 points (-1.0R)
- **MFE**: 18.25 points
- **MAE**: 153.50 points

### Trade #1813 - ➖ BE

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 09:45:00
- **FVG 5m**: 25720.50 - 25725.00
- **Entrée**: 25715.00 @ 2025-11-04 11:06:00
- **Stop Loss**: 25883.69
- **Risk**: 168.69 points
- **TP 1RR**: 25546.31 ✅
- **TP 2RR**: 25377.63 ✅
- **TP 3RR**: 25208.94 ✅
- **TP 4RR**: 25040.26 ✅
- **TP 15RR**: 23184.72 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 1005.75 points
- **MAE**: 165.00 points

### Trade #1814 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 15:00:00
- **FVG 5m**: 25540.50 - 25573.75
- **Entrée**: 25539.75 @ 2025-11-04 17:03:00
- **Stop Loss**: 25605.80
- **Risk**: 66.05 points
- **TP 1RR**: 25473.70 ✅
- **TP 2RR**: 25407.66 ✅
- **TP 3RR**: 25341.61 ✅
- **TP 4RR**: 25275.56 ❌
- **TP 15RR**: 24549.05 ❌
- **PnL**: -66.05 points (-1.0R)
- **MFE**: 257.75 points
- **MAE**: 80.75 points

### Trade #1815 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 15:15:00
- **FVG 5m**: 25540.50 - 25573.75
- **Entrée**: 25539.75 @ 2025-11-04 17:03:00
- **Stop Loss**: 25594.04
- **Risk**: 54.29 points
- **TP 1RR**: 25485.46 ✅
- **TP 2RR**: 25431.17 ✅
- **TP 3RR**: 25376.88 ✅
- **TP 4RR**: 25322.59 ✅
- **TP 15RR**: 24725.39 ❌
- **PnL**: -54.29 points (-1.0R)
- **MFE**: 257.75 points
- **MAE**: 56.25 points

### Trade #1816 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 15:15:00
- **FVG 5m**: 25540.50 - 25573.75
- **Entrée**: 25539.75 @ 2025-11-04 17:03:00
- **Stop Loss**: 25594.04
- **Risk**: 54.29 points
- **TP 1RR**: 25485.46 ✅
- **TP 2RR**: 25431.17 ✅
- **TP 3RR**: 25376.88 ✅
- **TP 4RR**: 25322.59 ✅
- **TP 15RR**: 24725.39 ❌
- **PnL**: -54.29 points (-1.0R)
- **MFE**: 257.75 points
- **MAE**: 56.25 points

### Trade #1817 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:00:00
- **FVG 5m**: 25352.75 - 25357.25
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25423.71
- **Risk**: 72.21 points
- **TP 1RR**: 25279.29 ❌
- **TP 2RR**: 25207.09 ❌
- **TP 3RR**: 25134.88 ❌
- **TP 4RR**: 25062.68 ❌
- **TP 15RR**: 24268.42 ❌
- **PnL**: -72.21 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 72.25 points

### Trade #1818 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:00:00
- **FVG 5m**: 25352.75 - 25357.25
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25423.71
- **Risk**: 72.21 points
- **TP 1RR**: 25279.29 ❌
- **TP 2RR**: 25207.09 ❌
- **TP 3RR**: 25134.88 ❌
- **TP 4RR**: 25062.68 ❌
- **TP 15RR**: 24268.42 ❌
- **PnL**: -72.21 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 72.25 points

### Trade #1819 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-04 19:00:00
- **FVG 5m**: 25352.75 - 25357.25
- **Entrée**: 25351.50 @ 2025-11-04 19:16:00
- **Stop Loss**: 25423.71
- **Risk**: 72.21 points
- **TP 1RR**: 25279.29 ❌
- **TP 2RR**: 25207.09 ❌
- **TP 3RR**: 25134.88 ❌
- **TP 4RR**: 25062.68 ❌
- **TP 15RR**: 24268.42 ❌
- **PnL**: -72.21 points (-1.0R)
- **MFE**: 69.50 points
- **MAE**: 72.25 points

### Trade #1820 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 19:45:00
- **FVG 5m**: 25323.25 - 25338.75
- **Entrée**: 25354.00 @ 2025-11-04 20:37:00
- **Stop Loss**: 25279.85
- **Risk**: 74.15 points
- **TP 1RR**: 25428.15 ✅
- **TP 2RR**: 25502.29 ✅
- **TP 3RR**: 25576.44 ✅
- **TP 4RR**: 25650.59 ✅
- **TP 15RR**: 26466.19 ❌
- **PnL**: -74.15 points (-1.0R)
- **MFE**: 526.00 points
- **MAE**: 76.75 points

### Trade #1821 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-04 20:30:00
- **FVG 5m**: 25358.75 - 25366.50
- **Entrée**: 25369.00 @ 2025-11-04 20:44:00
- **Stop Loss**: 25283.35
- **Risk**: 85.65 points
- **TP 1RR**: 25454.65 ✅
- **TP 2RR**: 25540.30 ✅
- **TP 3RR**: 25625.94 ✅
- **TP 4RR**: 25711.59 ✅
- **TP 15RR**: 26653.72 ❌
- **PnL**: -85.65 points (-1.0R)
- **MFE**: 511.00 points
- **MAE**: 91.75 points

### Trade #1822 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-05 05:30:00
- **FVG 5m**: 25460.25 - 25469.75
- **Entrée**: 25471.00 @ 2025-11-05 05:44:00
- **Stop Loss**: 25422.03
- **Risk**: 48.97 points
- **TP 1RR**: 25519.97 ✅
- **TP 2RR**: 25568.93 ✅
- **TP 3RR**: 25617.90 ✅
- **TP 4RR**: 25666.87 ✅
- **TP 15RR**: 26205.51 ❌
- **PnL**: -48.97 points (-1.0R)
- **MFE**: 409.00 points
- **MAE**: 57.75 points

### Trade #1823 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-05 18:30:00
- **FVG 5m**: 25666.00 - 25676.00
- **Entrée**: 25678.50 @ 2025-11-05 20:33:00
- **Stop Loss**: 25658.41
- **Risk**: 20.09 points
- **TP 1RR**: 25698.59 ✅
- **TP 2RR**: 25718.67 ✅
- **TP 3RR**: 25738.76 ✅
- **TP 4RR**: 25758.84 ❌
- **TP 15RR**: 25979.78 ❌
- **PnL**: -20.09 points (-1.0R)
- **MFE**: 64.00 points
- **MAE**: 21.25 points

### Trade #1824 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 07:45:00
- **FVG 5m**: 25774.25 - 25778.50
- **Entrée**: 25774.00 @ 2025-11-06 07:56:00
- **Stop Loss**: 25819.40
- **Risk**: 45.40 points
- **TP 1RR**: 25728.60 ✅
- **TP 2RR**: 25683.19 ✅
- **TP 3RR**: 25637.79 ✅
- **TP 4RR**: 25592.39 ✅
- **TP 15RR**: 25092.95 ✅
- **PnL**: 681.05 points (15.0R)
- **MFE**: 689.75 points
- **MAE**: 1.25 points

### Trade #1825 - ✅ GAGNANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 07:45:00
- **FVG 5m**: 25774.25 - 25778.50
- **Entrée**: 25774.00 @ 2025-11-06 07:56:00
- **Stop Loss**: 25819.40
- **Risk**: 45.40 points
- **TP 1RR**: 25728.60 ✅
- **TP 2RR**: 25683.19 ✅
- **TP 3RR**: 25637.79 ✅
- **TP 4RR**: 25592.39 ✅
- **TP 15RR**: 25092.95 ✅
- **PnL**: 681.05 points (15.0R)
- **MFE**: 689.75 points
- **MAE**: 1.25 points

### Trade #1826 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 08:00:00
- **FVG 5m**: 25701.50 - 25704.75
- **Entrée**: 25689.75 @ 2025-11-06 08:24:00
- **Stop Loss**: 25787.14
- **Risk**: 97.39 points
- **TP 1RR**: 25592.36 ✅
- **TP 2RR**: 25494.98 ✅
- **TP 3RR**: 25397.59 ✅
- **TP 4RR**: 25300.20 ✅
- **TP 15RR**: 24228.94 ❌
- **PnL**: -97.39 points (-1.0R)
- **MFE**: 980.50 points
- **MAE**: 97.50 points

### Trade #1827 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 09:30:00
- **FVG 5m**: 25268.00 - 25296.00
- **Entrée**: 25258.00 @ 2025-11-06 10:37:00
- **Stop Loss**: 25526.51
- **Risk**: 268.51 points
- **TP 1RR**: 24989.49 ✅
- **TP 2RR**: 24720.99 ✅
- **TP 3RR**: 24452.48 ❌
- **TP 4RR**: 24183.97 ❌
- **TP 15RR**: 21230.40 ❌
- **PnL**: -268.51 points (-1.0R)
- **MFE**: 548.75 points
- **MAE**: 269.00 points

### Trade #1828 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 10:30:00
- **FVG 5m**: 25294.25 - 25326.25
- **Entrée**: 25291.00 @ 2025-11-06 12:04:00
- **Stop Loss**: 25345.42
- **Risk**: 54.42 points
- **TP 1RR**: 25236.58 ✅
- **TP 2RR**: 25182.17 ❌
- **TP 3RR**: 25127.75 ❌
- **TP 4RR**: 25073.33 ❌
- **TP 15RR**: 24474.75 ❌
- **PnL**: -54.42 points (-1.0R)
- **MFE**: 65.50 points
- **MAE**: 59.75 points

### Trade #1829 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-06 10:30:00
- **FVG 5m**: 25294.25 - 25326.25
- **Entrée**: 25291.00 @ 2025-11-06 12:04:00
- **Stop Loss**: 25345.42
- **Risk**: 54.42 points
- **TP 1RR**: 25236.58 ✅
- **TP 2RR**: 25182.17 ❌
- **TP 3RR**: 25127.75 ❌
- **TP 4RR**: 25073.33 ❌
- **TP 15RR**: 24474.75 ❌
- **PnL**: -54.42 points (-1.0R)
- **MFE**: 65.50 points
- **MAE**: 59.75 points

### Trade #1830 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 11:15:00
- **FVG 5m**: 25283.25 - 25288.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25185.15
- **Risk**: 113.10 points
- **TP 1RR**: 25411.35 ✅
- **TP 2RR**: 25524.45 ❌
- **TP 3RR**: 25637.55 ❌
- **TP 4RR**: 25750.65 ❌
- **TP 15RR**: 26994.73 ❌
- **PnL**: -113.10 points (-1.0R)
- **MFE**: 140.25 points
- **MAE**: 136.25 points

### Trade #1831 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 11:30:00
- **FVG 5m**: 25283.25 - 25288.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25217.38
- **Risk**: 80.87 points
- **TP 1RR**: 25379.12 ✅
- **TP 2RR**: 25459.98 ❌
- **TP 3RR**: 25540.85 ❌
- **TP 4RR**: 25621.71 ❌
- **TP 15RR**: 26511.23 ❌
- **PnL**: -80.87 points (-1.0R)
- **MFE**: 140.25 points
- **MAE**: 82.25 points

### Trade #1832 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 11:30:00
- **FVG 5m**: 25283.25 - 25288.00
- **Entrée**: 25298.25 @ 2025-11-06 11:43:00
- **Stop Loss**: 25217.38
- **Risk**: 80.87 points
- **TP 1RR**: 25379.12 ✅
- **TP 2RR**: 25459.98 ❌
- **TP 3RR**: 25540.85 ❌
- **TP 4RR**: 25621.71 ❌
- **TP 15RR**: 26511.23 ❌
- **PnL**: -80.87 points (-1.0R)
- **MFE**: 140.25 points
- **MAE**: 82.25 points

### Trade #1833 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 13:15:00
- **FVG 5m**: 25396.50 - 25409.25
- **Entrée**: 25416.75 @ 2025-11-06 13:26:00
- **Stop Loss**: 25350.07
- **Risk**: 66.68 points
- **TP 1RR**: 25483.43 ❌
- **TP 2RR**: 25550.11 ❌
- **TP 3RR**: 25616.79 ❌
- **TP 4RR**: 25683.48 ❌
- **TP 15RR**: 26416.97 ❌
- **PnL**: -66.68 points (-1.0R)
- **MFE**: 21.75 points
- **MAE**: 68.75 points

### Trade #1834 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-06 19:30:00
- **FVG 5m**: 25233.25 - 25246.50
- **Entrée**: 25252.75 @ 2025-11-06 20:33:00
- **Stop Loss**: 25188.40
- **Risk**: 64.35 points
- **TP 1RR**: 25317.10 ❌
- **TP 2RR**: 25381.45 ❌
- **TP 3RR**: 25445.80 ❌
- **TP 4RR**: 25510.15 ❌
- **TP 15RR**: 26218.01 ❌
- **PnL**: -64.35 points (-1.0R)
- **MFE**: 28.75 points
- **MAE**: 90.75 points

### Trade #1835 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 03:15:00
- **FVG 5m**: 25283.25 - 25292.25
- **Entrée**: 25280.50 @ 2025-11-07 03:27:00
- **Stop Loss**: 25338.66
- **Risk**: 58.16 points
- **TP 1RR**: 25222.34 ✅
- **TP 2RR**: 25164.17 ✅
- **TP 3RR**: 25106.01 ✅
- **TP 4RR**: 25047.85 ✅
- **TP 15RR**: 24408.05 ❌
- **PnL**: -58.16 points (-1.0R)
- **MFE**: 571.25 points
- **MAE**: 111.00 points

### Trade #1836 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 05:00:00
- **FVG 5m**: 25133.75 - 25176.00
- **Entrée**: 25125.00 @ 2025-11-07 05:14:00
- **Stop Loss**: 25232.86
- **Risk**: 107.86 points
- **TP 1RR**: 25017.14 ✅
- **TP 2RR**: 24909.28 ✅
- **TP 3RR**: 24801.42 ✅
- **TP 4RR**: 24693.56 ❌
- **TP 15RR**: 23507.10 ❌
- **PnL**: -107.86 points (-1.0R)
- **MFE**: 415.75 points
- **MAE**: 266.50 points

### Trade #1837 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 05:45:00
- **FVG 5m**: 25093.50 - 25120.00
- **Entrée**: 25130.00 @ 2025-11-07 07:48:00
- **Stop Loss**: 25122.93
- **Risk**: 7.07 points
- **TP 1RR**: 25137.07 ❌
- **TP 2RR**: 25144.14 ❌
- **TP 3RR**: 25151.20 ❌
- **TP 4RR**: 25158.27 ❌
- **TP 15RR**: 25236.02 ❌
- **PnL**: -7.07 points (-1.0R)
- **MFE**: 3.00 points
- **MAE**: 11.00 points

### Trade #1838 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 06:30:00
- **FVG 5m**: 25113.00 - 25128.00
- **Entrée**: 25107.50 @ 2025-11-07 06:44:00
- **Stop Loss**: 25173.83
- **Risk**: 66.33 points
- **TP 1RR**: 25041.17 ✅
- **TP 2RR**: 24974.84 ✅
- **TP 3RR**: 24908.51 ✅
- **TP 4RR**: 24842.18 ✅
- **TP 15RR**: 24112.54 ❌
- **PnL**: -66.33 points (-1.0R)
- **MFE**: 398.25 points
- **MAE**: 78.25 points

### Trade #1839 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-07 08:30:00
- **FVG 5m**: 24975.75 - 24983.00
- **Entrée**: 24970.75 @ 2025-11-07 09:01:00
- **Stop Loss**: 25123.56
- **Risk**: 152.81 points
- **TP 1RR**: 24817.94 ✅
- **TP 2RR**: 24665.14 ❌
- **TP 3RR**: 24512.33 ❌
- **TP 4RR**: 24359.53 ❌
- **TP 15RR**: 22678.67 ❌
- **PnL**: -152.81 points (-1.0R)
- **MFE**: 261.50 points
- **MAE**: 157.00 points

### Trade #1840 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 08:30:00
- **FVG 5m**: 24975.75 - 24984.75
- **Entrée**: 25006.50 @ 2025-11-07 09:19:00
- **Stop Loss**: 24905.29
- **Risk**: 101.21 points
- **TP 1RR**: 25107.71 ❌
- **TP 2RR**: 25208.92 ❌
- **TP 3RR**: 25310.13 ❌
- **TP 4RR**: 25411.34 ❌
- **TP 15RR**: 26524.63 ❌
- **PnL**: -101.21 points (-1.0R)
- **MFE**: 32.50 points
- **MAE**: 121.00 points

### Trade #1841 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 11:15:00
- **FVG 5m**: 24805.25 - 24833.75
- **Entrée**: 24841.25 @ 2025-11-07 11:59:00
- **Stop Loss**: 24754.87
- **Risk**: 86.38 points
- **TP 1RR**: 24927.63 ✅
- **TP 2RR**: 25014.02 ✅
- **TP 3RR**: 25100.40 ✅
- **TP 4RR**: 25186.78 ✅
- **TP 15RR**: 26137.00 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 988.75 points
- **MAE**: 20.00 points

### Trade #1842 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 13:30:00
- **FVG 5m**: 25126.75 - 25160.75
- **Entrée**: 25167.75 @ 2025-11-07 14:58:00
- **Stop Loss**: 24938.77
- **Risk**: 228.98 points
- **TP 1RR**: 25396.73 ✅
- **TP 2RR**: 25625.70 ✅
- **TP 3RR**: 25854.68 ❌
- **TP 4RR**: 26083.65 ❌
- **TP 15RR**: 28602.38 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 662.25 points
- **MAE**: 14.25 points

### Trade #1843 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-07 15:00:00
- **FVG 5m**: 25208.75 - 25212.75
- **Entrée**: 25215.25 @ 2025-11-07 15:34:00
- **Stop Loss**: 25148.17
- **Risk**: 67.08 points
- **TP 1RR**: 25282.33 ✅
- **TP 2RR**: 25349.41 ✅
- **TP 3RR**: 25416.49 ✅
- **TP 4RR**: 25483.57 ✅
- **TP 15RR**: 26221.46 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 614.75 points
- **MAE**: 6.75 points

### Trade #1844 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-09 17:00:00
- **FVG 5m**: 25313.50 - 25335.00
- **Entrée**: 25300.50 @ 2025-11-09 18:03:00
- **Stop Loss**: 25404.20
- **Risk**: 103.70 points
- **TP 1RR**: 25196.80 ❌
- **TP 2RR**: 25093.11 ❌
- **TP 3RR**: 24989.41 ❌
- **TP 4RR**: 24885.72 ❌
- **TP 15RR**: 23745.06 ❌
- **PnL**: -103.70 points (-1.0R)
- **MFE**: 31.50 points
- **MAE**: 103.75 points

### Trade #1845 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-09 17:00:00
- **FVG 5m**: 25313.50 - 25335.00
- **Entrée**: 25300.50 @ 2025-11-09 18:03:00
- **Stop Loss**: 25404.20
- **Risk**: 103.70 points
- **TP 1RR**: 25196.80 ❌
- **TP 2RR**: 25093.11 ❌
- **TP 3RR**: 24989.41 ❌
- **TP 4RR**: 24885.72 ❌
- **TP 15RR**: 23745.06 ❌
- **PnL**: -103.70 points (-1.0R)
- **MFE**: 31.50 points
- **MAE**: 103.75 points

### Trade #1846 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 00:45:00
- **FVG 5m**: 25471.25 - 25477.00
- **Entrée**: 25463.25 @ 2025-11-10 02:12:00
- **Stop Loss**: 25516.25
- **Risk**: 53.00 points
- **TP 1RR**: 25410.25 ❌
- **TP 2RR**: 25357.25 ❌
- **TP 3RR**: 25304.24 ❌
- **TP 4RR**: 25251.24 ❌
- **TP 15RR**: 24668.22 ❌
- **PnL**: -53.00 points (-1.0R)
- **MFE**: 6.25 points
- **MAE**: 56.75 points

### Trade #1847 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-10 08:30:00
- **FVG 5m**: 25499.00 - 25511.25
- **Entrée**: 25513.25 @ 2025-11-10 10:58:00
- **Stop Loss**: 25512.49
- **Risk**: 0.76 points
- **TP 1RR**: 25514.01 ❌
- **TP 2RR**: 25514.78 ❌
- **TP 3RR**: 25515.54 ❌
- **TP 4RR**: 25516.30 ❌
- **TP 15RR**: 25524.69 ❌
- **PnL**: -0.76 points (-1.0R)
- **MFE**: 11.00 points
- **MAE**: 1.75 points

### Trade #1848 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 09:45:00
- **FVG 5m**: 25525.25 - 25539.50
- **Entrée**: 25524.00 @ 2025-11-10 09:59:00
- **Stop Loss**: 25643.57
- **Risk**: 119.57 points
- **TP 1RR**: 25404.43 ❌
- **TP 2RR**: 25284.87 ❌
- **TP 3RR**: 25165.30 ❌
- **TP 4RR**: 25045.74 ❌
- **TP 15RR**: 23730.52 ❌
- **PnL**: -119.57 points (-1.0R)
- **MFE**: 72.00 points
- **MAE**: 123.25 points

### Trade #1849 - ➖ BE

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-10 10:00:00
- **FVG 5m**: 25499.00 - 25511.25
- **Entrée**: 25513.25 @ 2025-11-10 10:58:00
- **Stop Loss**: 25458.26
- **Risk**: 54.99 points
- **TP 1RR**: 25568.24 ✅
- **TP 2RR**: 25623.22 ✅
- **TP 3RR**: 25678.21 ✅
- **TP 4RR**: 25733.19 ✅
- **TP 15RR**: 26338.03 ❌
- **PnL**: 0.00 points (0.0R)
- **MFE**: 316.75 points
- **MAE**: 34.75 points

### Trade #1850 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 12:45:00
- **FVG 5m**: 25664.25 - 25667.75
- **Entrée**: 25663.00 @ 2025-11-10 12:56:00
- **Stop Loss**: 25695.34
- **Risk**: 32.34 points
- **TP 1RR**: 25630.66 ❌
- **TP 2RR**: 25598.32 ❌
- **TP 3RR**: 25565.98 ❌
- **TP 4RR**: 25533.63 ❌
- **TP 15RR**: 25177.88 ❌
- **PnL**: -32.34 points (-1.0R)
- **MFE**: 20.50 points
- **MAE**: 33.75 points

### Trade #1851 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-10 14:45:00
- **FVG 5m**: 25722.50 - 25729.00
- **Entrée**: 25719.00 @ 2025-11-10 15:51:00
- **Stop Loss**: 25773.38
- **Risk**: 54.38 points
- **TP 1RR**: 25664.62 ✅
- **TP 2RR**: 25610.24 ✅
- **TP 3RR**: 25555.86 ✅
- **TP 4RR**: 25501.48 ✅
- **TP 15RR**: 24903.30 ❌
- **PnL**: -54.38 points (-1.0R)
- **MFE**: 240.50 points
- **MAE**: 56.50 points

### Trade #1852 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-11 08:45:00
- **FVG 5m**: 25587.25 - 25594.50
- **Entrée**: 25607.75 @ 2025-11-11 08:56:00
- **Stop Loss**: 25547.47
- **Risk**: 60.28 points
- **TP 1RR**: 25668.03 ❌
- **TP 2RR**: 25728.31 ❌
- **TP 3RR**: 25788.59 ❌
- **TP 4RR**: 25848.87 ❌
- **TP 15RR**: 26511.95 ❌
- **PnL**: -60.28 points (-1.0R)
- **MFE**: 25.75 points
- **MAE**: 63.25 points

### Trade #1853 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-11 12:30:00
- **FVG 5m**: 25638.25 - 25652.50
- **Entrée**: 25656.75 @ 2025-11-11 12:41:00
- **Stop Loss**: 25594.45
- **Risk**: 62.30 points
- **TP 1RR**: 25719.05 ✅
- **TP 2RR**: 25781.36 ✅
- **TP 3RR**: 25843.66 ❌
- **TP 4RR**: 25905.96 ❌
- **TP 15RR**: 26591.30 ❌
- **PnL**: -62.30 points (-1.0R)
- **MFE**: 173.25 points
- **MAE**: 63.75 points

### Trade #1854 - ❌ PERDANT

- **Direction**: LONG
- **Sweep**: BULLISH @ 2025-11-11 19:00:00
- **FVG 5m**: 25722.00 - 25728.00
- **Entrée**: 25728.25 @ 2025-11-11 19:54:00
- **Stop Loss**: 25666.16
- **Risk**: 62.09 points
- **TP 1RR**: 25790.34 ✅
- **TP 2RR**: 25852.43 ❌
- **TP 3RR**: 25914.52 ❌
- **TP 4RR**: 25976.61 ❌
- **TP 15RR**: 26659.59 ❌
- **PnL**: -62.09 points (-1.0R)
- **MFE**: 101.75 points
- **MAE**: 67.25 points

### Trade #1855 - ❌ PERDANT

- **Direction**: SHORT
- **Sweep**: BEARISH @ 2025-11-11 19:15:00
- **FVG 5m**: 25728.00 - 25735.00
- **Entrée**: 25722.50 @ 2025-11-11 20:47:00
- **Stop Loss**: 25733.86
- **Risk**: 11.36 points
- **TP 1RR**: 25711.14 ✅
- **TP 2RR**: 25699.78 ❌
- **TP 3RR**: 25688.42 ❌
- **TP 4RR**: 25677.06 ❌
- **TP 15RR**: 25552.09 ❌
- **PnL**: -11.36 points (-1.0R)
- **MFE**: 14.00 points
- **MAE**: 12.00 points


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
| **Stop Loss** | Au-dessus du sweep high (short) / En-dessous du sweep low (long) |
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

*Rapport généré le 2025-11-30 23:05:36*
