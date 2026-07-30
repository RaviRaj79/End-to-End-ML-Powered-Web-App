# EDA notebook guide

Create `01_exploration.ipynb` to document the model-development story:

1. Load anonymized resume/job text pairs into Pandas.
2. Inspect null values, role distribution, text length and duplicate records.
3. Plot skill frequencies by role with Matplotlib/Seaborn.
4. Compare a baseline keyword-overlap score against TF-IDF cosine similarity.
5. Evaluate with labelled relevant/not-relevant pairs using precision, recall and F1.
6. Record bias and privacy considerations: never use protected attributes; retain only consented, minimally necessary candidate text.

The production app intentionally uses transparent TF-IDF scoring, then supplements it with explicit skill coverage so users can understand every recommendation.
