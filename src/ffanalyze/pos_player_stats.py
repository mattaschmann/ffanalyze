from enum import Enum
import pandas as pd
from pandas.io.formats.style import StylerRenderer
import os
from typing import List, cast

from ffanalyze import defense, math_utils, format
from ffanalyze.col_names import ColNames

pd.options.mode.chained_assignment = None  # default='warn'

dirname = os.path.dirname(__file__)

class Position(Enum):
    QB = 'QB'
    WR = 'WR'
    RB = 'RB'
    TE = 'TE'

RET_YDS_PT = 50 # return yards per point

def sheet(position: Position) -> pd.DataFrame:
    number_cols = ['GP', 'Pts', 'PaY', 'PaTd', 'Int', 'RuAt', 'RuY', 'RuTd', 'Tar', 'Rec', 'RecY', 'RecTd', 'RetY', 'RetTd', 'TwPt', 'Fum']
    df = pd.read_json(os.path.join(dirname, f'../../data/{position.value}s.json'))
    pos_df = df.copy()

    # cleanup
    for col in number_cols:
        pos_df[col] = pd.to_numeric(df[col].replace('-', 0))

    # needs to have actually played and scored positive points
    result = pos_df.query('GP > 0 & Pts > 0')

    # dynamic columns
    match position:        # total opp
        case Position.QB:
            col_names = ColNames('Y')
            result[col_names.opp_col] = pos_df[['PaY', 'RuY']].sum(axis = 1)
        case Position.WR|Position.RB|Position.TE:
            col_names = ColNames('O')
            result[col_names.opp_col] = pos_df[['RuAt', 'Tar']].sum(axis = 1) + (pos_df['RetY'] / RET_YDS_PT)
        case _:
            raise Exception(f'Postion "{position.value}" not found')


    result[col_names.pt_opp_col] = pos_df['Pts'] / result[col_names.opp_col]            # Points per opp
    result[col_names.ops_g_col] = result[col_names.opp_col] / pos_df['GP']              # Ops per game
    result['Pts/G'] = pos_df['Pts'] / pos_df['GP']                 # Points per game
    result[col_names.pt_opp_z_col] = math_utils.z_score(result[col_names.pt_opp_col])   # Points per opp z-score
    result[col_names.ops_g_z_col] = math_utils.z_score(result[col_names.ops_g_col])    # Ops per game z-score
    result['P/G Z'] = math_utils.z_score(result['Pts/G'])    # Points per game z-score
    result['Zval'] = (result[col_names.ops_g_z_col] + result['P/G Z']) / 2 # Z value score

    # get defense
    # @Matt TODO: add points against stuff
    # pts_ag = defense.sheet(os.path.join(dirname, f'../../data/{position.value}PtsAg.json'))

    return result

def style_sheet(sheet: pd.DataFrame, opp_abbr: str) -> StylerRenderer:
    return format.style_sheet(sheet, ColNames(opp_abbr))

def qb_sheet():
    return sheet(Position.QB)

def wr_sheet():
    return sheet(Position.WR)

if __name__ == '__main__':
    print(qb_sheet())
