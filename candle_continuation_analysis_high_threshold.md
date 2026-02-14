# Analyse de Probabilité de Continuation des Bougies (Seuils Élevés)

## Paramètres de l'Analyse

- **Période d'analyse**: 2018 - 2025
- **Heures de trading**: 02:00 - 12:00 (New York time)

### Critères

- **Bougie haussière sans mèche**: Close > Open ET High == Close (pas de mèche haute)
- **Bougie baissière sans mèche**: Close < Open ET Low == Close (pas de mèche basse)
- **Continuation haussière**: La bougie suivante clôture au-dessus de la clôture actuelle
- **Continuation baissière**: La bougie suivante clôture en dessous de la clôture actuelle

### Taille Minimale du Corps

| Timeframe | Taille Minimale |
|-----------|-----------------|
| 1 minute  | ≥ 10 points     |
| 5 minutes | ≥ 40 points     |
| 15 minutes| ≥ 80 points     |

---

## Résultats

### Timeframe: 1M

| Métrique | Valeur |
|----------|--------|
| Total bougies analysées | 1,219,548 |
| Bougies haussières sans mèche | 3,055 |
| Bougies baissières sans mèche | 3,166 |
| **Total bougies sans mèche** | **6,221** |
| Continuations haussières | 1,459 |
| Continuations baissières | 1,437 |
| **Total continuations** | **2,896** |

**Probabilités de Continuation:**
- Probabilité globale: **46.55%**
- Probabilité haussière: 47.76%
- Probabilité baissière: 45.39%

---

### Timeframe: 5M

| Métrique | Valeur |
|----------|--------|
| Total bougies analysées | 245,532 |
| Bougies haussières sans mèche | 59 |
| Bougies baissières sans mèche | 63 |
| **Total bougies sans mèche** | **122** |
| Continuations haussières | 29 |
| Continuations baissières | 27 |
| **Total continuations** | **56** |

**Probabilités de Continuation:**
- Probabilité globale: **45.90%**
- Probabilité haussière: 49.15%
- Probabilité baissière: 42.86%

---

### Timeframe: 15M

| Métrique | Valeur |
|----------|--------|
| Total bougies analysées | 83,186 |
| Bougies haussières sans mèche | 11 |
| Bougies baissières sans mèche | 9 |
| **Total bougies sans mèche** | **20** |
| Continuations haussières | 5 |
| Continuations baissières | 2 |
| **Total continuations** | **7** |

**Probabilités de Continuation:**
- Probabilité globale: **35.00%**
- Probabilité haussière: 45.45%
- Probabilité baissière: 22.22%

---

## Résumé

| Timeframe | Bougies Sans Mèche | Continuations | Probabilité |
|-----------|-------------------|---------------|-------------|
| 1m | 6,221 | 2,896 | **46.55%** |
| 5m | 122 | 56 | **45.90%** |
| 15m | 20 | 7 | **35.00%** |

---

*Analyse générée automatiquement à partir des données historiques.*
