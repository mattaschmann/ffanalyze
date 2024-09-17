from enum import Enum
import os
from typing import List, cast

import pandas as pd
from pandas.io.formats.style import StylerRenderer

from ffanalyze import defense, format, math_utils, teams
from ffanalyze.col_names import ColNames

pd.options.mode.chained_assignment = None  # default='warn'

dirname = os.path.dirname(__file__)

def sheet() -> pd.DataFrame:
    number_cols = ['GP', 'Pts', '0-19', '20-29', '30-39', '40-49', '50+', 'Pat']
    df = pd.read_json(os.path.join(dirname, f'../../data/Ks.json'))
    k_df = df.copy()

    # cleanup, convert to number
    for col in number_cols:
        k_df[col] = pd.to_numeric(df[col].replace('-', 0))

    k_df = k_df.query('GP > 0 & Pts > 0')

    # pre-join dynamic columns
    k_df['Pts/G'] = k_df['Pts'] / k_df['GP']                 # Points per game

    # get defense
    pts_ag = defense.sheet(os.path.join(dirname, f'../../data/KPtsAg.json'))
    # needs to have actually played and scored positive points
    result = k_df.set_index('Opp').join(pts_ag.set_index('Abbr'))

    # # dynamic columns
    # result[col_names.pt_opp_col] = pos_df['Pts'] / result[col_names.opp_col]            # Points per opp
    # result[col_names.ops_g_col] = result[col_names.opp_col] / pos_df['GP']              # Ops per game
    # result['Pts/G'] = k_df['Pts'] / k_df['GP']                 # Points per game
    # result[col_names.pt_opp_z_col] = math_utils.z_score(result[col_names.pt_opp_col])   # Points per opp z-score
    # result[col_names.ops_g_z_col] = math_utils.z_score(result[col_names.ops_g_col])    # Ops per game z-score
    # result['P/G Z'] = math_utils.z_score(result['Pts/G'])    # Points per game z-score
    # result['Zval'] = (result[col_names.ops_g_z_col] + result['P/G Z']) / 2 # Z value score
    result['ExPt'] = result['D PCo'] * result['Pts/G']

    return result
