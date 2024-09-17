import pandas as pd

def z_score(s) -> float:
    return (s - s.mean()) / s.std()

def coef(s) -> float:
    return s / s.mean()
