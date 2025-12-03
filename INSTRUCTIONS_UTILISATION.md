# 📖 INSTRUCTIONS D'UTILISATION - Analyse Tokyo Session

## 🎯 Vue d'ensemble

Ce projet contient une analyse complète de la stratégie de trading basée sur la session Tokyo et la zone de manipulation de Londres, avec des scripts Python prêts à l'emploi et des rapports détaillés.

---

## 📦 Prérequis

### Installation des dépendances Python

```bash
pip install pandas numpy matplotlib
```

ou si vous utilisez pip3:

```bash
pip3 install pandas numpy matplotlib
```

---

## 🚀 Guide de Démarrage Rapide

### 1️⃣ Exécuter l'Analyse Complète

Pour analyser toutes les données de 2018 à 2025:

```bash
cd /home/runner/work/Backtest-Trading/Backtest-Trading
python3 tokyo_session_analysis.py
```

**Durée estimée**: 2-3 minutes

**Fichiers générés**:
- `tokyo_analysis_report.txt` - Rapport textuel détaillé
- `tokyo_analysis_results.csv` - Données brutes en CSV

### 2️⃣ Générer les Visualisations

Pour créer les graphiques:

```bash
python3 visualize_results.py
```

**Durée estimée**: 10-15 secondes

**Fichiers générés**:
- `tokyo_statistics.png` - Statistiques globales
- `tokyo_time_series.png` - Évolution temporelle
- `tokyo_range_analysis.png` - Analyse de la range

### 3️⃣ Consulter les Résultats

**Pour un aperçu rapide**:
```bash
cat ANALYSE_TOKYO_RESUME.md
```

**Pour le rapport complet**:
```bash
cat tokyo_analysis_report.txt
```

**Pour les données détaillées**:
```bash
head -50 tokyo_analysis_results.csv
```

---

## 📊 Structure des Fichiers

### 📝 Scripts Python

#### `tokyo_session_analysis.py`
**Description**: Script principal d'analyse  
**Fonction**: 
- Charge les données CSV (2018-2025)
- Identifie les sessions Tokyo (19:00-00:00)
- Détecte les zones de manipulation (02:00-02:30)
- Calcule les cassures et probabilités
- Génère les rapports

**Utilisation**:
```bash
python3 tokyo_session_analysis.py
```

**Personnalisation possible**:
```python
# Dans le script, vous pouvez modifier:
# - Les années à analyser
analyzer.load_data(years=range(2018, 2026), timeframes=['5m', '15m', '1H'])

# - La fenêtre de temps pour le retour (actuellement 6 heures)
return_info = analyzer.check_return_to_equilibrium(
    breakout_time,
    tokyo_eq,
    hours=6  # Modifier ici
)
```

#### `visualize_results.py`
**Description**: Générateur de visualisations  
**Fonction**:
- Lit le fichier `tokyo_analysis_results.csv`
- Génère 3 graphiques en PNG haute résolution
- Affiche un résumé textuel

**Utilisation**:
```bash
python3 visualize_results.py
```

**Note**: Nécessite matplotlib

---

### 📄 Rapports et Documentation

#### `ANALYSE_TOKYO_RESUME.md`
**Résumé exécutif** avec:
- Probabilité globale (68.47%)
- Statistiques clés
- Performance par type de cassure
- Performance annuelle
- Conclusions et recommandations

#### `TOKYO_ANALYSIS_README.md`
**Documentation complète** incluant:
- Règles détaillées de la stratégie
- Résultats détaillés par année
- Statistiques de temps de retour
- Guide d'utilisation
- Interprétation des résultats
- Code source commenté

#### `tokyo_analysis_report.txt`
**Rapport technique détaillé** contenant:
- Règles de la stratégie
- Résultats globaux
- Décomposition par type de cassure
- Statistiques temporelles
- Répartition annuelle
- 20 exemples de signaux détaillés

---

### 📊 Données

#### `tokyo_analysis_results.csv`
**Colonnes**:
- `date`: Date de la session Tokyo
- `tokyo_start`, `tokyo_end`: Horaires de la session
- `tokyo_high`, `tokyo_low`, `tokyo_eq`: Niveaux clés
- `tokyo_range`: Taille de la range
- `breakout_type`: HIGH ou LOW
- `breakout_time`: Moment de la cassure
- `breakout_price`: Prix de la cassure
- `returned_to_eq`: True/False (retour au 50%)
- `return_time`: Moment du retour (si applicable)
- `time_to_return_hours`: Temps écoulé
- `year`: Année

**Utilisation**:
```python
import pandas as pd
df = pd.read_csv('tokyo_analysis_results.csv')

# Filtrer les cassures LOW réussies
low_success = df[(df['breakout_type'] == 'LOW') & (df['returned_to_eq'] == True)]

# Analyser les temps de retour
print(low_success['time_to_return_hours'].describe())
```

---

### 🖼️ Graphiques

#### `tokyo_statistics.png`
Contient 4 visualisations:
1. **Taux de réussite global** (pie chart)
2. **Comparaison HIGH vs LOW** (bar chart)
3. **Distribution du temps de retour** (histogram)
4. **Performance annuelle** (bar chart)

#### `tokyo_time_series.png`
Contient 2 visualisations:
1. **Évolution du taux de réussite cumulé** (line chart)
2. **Nombre de signaux par mois** (bar chart)

#### `tokyo_range_analysis.png`
Contient 2 visualisations:
1. **Taux de réussite vs Range Tokyo** (bar chart)
2. **Distribution de la range** (histogram)

---

## 🔧 Personnalisation Avancée

### Modifier les Heures de Session

Dans `tokyo_session_analysis.py`, méthode `identify_tokyo_session()`:

```python
# Session Tokyo actuelle: 19:00-00:00
tokyo_start = pd.Timestamp(date) + pd.Timedelta(hours=19)
tokyo_end = tokyo_start + pd.Timedelta(hours=5)

# Pour modifier, par exemple 18:00-23:00:
tokyo_start = pd.Timestamp(date) + pd.Timedelta(hours=18)
tokyo_end = tokyo_start + pd.Timedelta(hours=5)
```

### Modifier la Zone de Manipulation

Dans `tokyo_session_analysis.py`, méthode `identify_manipulation_zone()`:

```python
# Zone actuelle: 02:00-02:30
manip_start = next_day + pd.Timedelta(hours=2)
manip_end = manip_start + pd.Timedelta(minutes=30)

# Pour modifier, par exemple 01:00-02:00:
manip_start = next_day + pd.Timedelta(hours=1)
manip_end = manip_start + pd.Timedelta(hours=1)
```

### Analyser une Période Spécifique

```python
# Dans tokyo_session_analysis.py, fonction main():
analyzer.load_data(
    years=range(2022, 2025),  # Seulement 2022-2024
    timeframes=['5m']          # Seulement 5 minutes
)
```

---

## 📈 Analyses Supplémentaires Possibles

### 1. Filtrer par Année Spécifique

```python
import pandas as pd
df = pd.read_csv('tokyo_analysis_results.csv')

# Analyse pour 2023 uniquement
df_2023 = df[df['year'] == 2023]
success_rate_2023 = df_2023['returned_to_eq'].mean() * 100
print(f"Taux 2023: {success_rate_2023:.2f}%")
```

### 2. Analyser par Mois

```python
df['month'] = pd.to_datetime(df['date']).dt.month
monthly_stats = df.groupby('month')['returned_to_eq'].agg(['mean', 'count'])
print(monthly_stats)
```

### 3. Analyser par Range Tokyo

```python
# Diviser en ranges petite/moyenne/grande
df['range_category'] = pd.cut(
    df['tokyo_range'], 
    bins=[0, 40, 80, float('inf')],
    labels=['Petite', 'Moyenne', 'Grande']
)

range_stats = df.groupby('range_category')['returned_to_eq'].mean() * 100
print(range_stats)
```

---

## 🐛 Dépannage

### Problème: "ModuleNotFoundError: No module named 'pandas'"
**Solution**:
```bash
pip install pandas numpy
```

### Problème: "FileNotFoundError: tokyo_analysis_results.csv"
**Solution**: Exécuter d'abord `tokyo_session_analysis.py`
```bash
python3 tokyo_session_analysis.py
```

### Problème: Graphiques ne s'affichent pas
**Solution**: Installer matplotlib
```bash
pip install matplotlib
```

### Problème: "Permission denied"
**Solution**: Vérifier les permissions
```bash
chmod +x tokyo_session_analysis.py visualize_results.py
```

---

## 💡 Conseils d'Utilisation

### Pour Traders
1. ✅ Consultez `ANALYSE_TOKYO_RESUME.md` pour les conclusions
2. ✅ Regardez les graphiques PNG pour la visualisation
3. ✅ Notez que les cassures LOW sont plus fiables (73.41% vs 64.29%)
4. ✅ La médiane de retour est 1 heure - surveillez activement

### Pour Analystes
1. ✅ Utilisez `tokyo_analysis_results.csv` pour vos propres analyses
2. ✅ Modifiez les scripts pour tester d'autres paramètres
3. ✅ Exportez les données vers Excel/R/autres outils
4. ✅ Consultez le code source pour comprendre la méthodologie

### Pour Développeurs
1. ✅ Le code est bien commenté et structuré en classe
2. ✅ Facilement extensible pour d'autres stratégies
3. ✅ Utilisez pandas pour la manipulation des données
4. ✅ Ajoutez vos propres méthodes d'analyse

---

## 📞 Questions Fréquentes

### Q: Puis-je modifier les heures de la session Tokyo?
**R**: Oui, voir section "Personnalisation Avancée"

### Q: Comment exporter vers Excel?
**R**: Le fichier CSV peut être directement ouvert dans Excel

### Q: Puis-je analyser d'autres instruments?
**R**: Oui, remplacez les fichiers CSV par vos propres données (même format)

### Q: Quelle est la précision des résultats?
**R**: 1,478 signaux analysés sur 8 ans - statistiquement significatif

### Q: Dois-je réexécuter l'analyse régulièrement?
**R**: Oui, ajoutez les nouvelles données et relancez le script

---

## 📚 Ressources Additionnelles

### Documentation Pandas
- https://pandas.pydata.org/docs/

### Documentation Matplotlib
- https://matplotlib.org/stable/contents.html

### Analyse de Données Financières
- Consultez les livres sur l'analyse technique
- Forums de trading algorithmique

---

## ✅ Checklist de Démarrage

- [ ] Installer Python 3.x
- [ ] Installer pandas, numpy, matplotlib
- [ ] Vérifier que les fichiers CSV sont présents
- [ ] Exécuter `tokyo_session_analysis.py`
- [ ] Vérifier la génération des fichiers de sortie
- [ ] Exécuter `visualize_results.py`
- [ ] Consulter les graphiques et rapports
- [ ] Lire `ANALYSE_TOKYO_RESUME.md`

---

**Dernière mise à jour**: Décembre 2025  
**Version**: 1.0  
**Support**: Consultez les fichiers de documentation

---

*Bonne analyse! 📊📈*
