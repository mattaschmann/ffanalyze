import re

import pandas as pd
from pandas import Series
from pandas.io.formats.style import StylerRenderer

from ffanalyze import colors
from ffanalyze.col_names import ColNames

def highlight_owner(val: str):
    match val:
        case 'Injured Reserves':
            return 'background-color: #b7e1cd; color: black'
        case 'FA':
            return 'background-color: #c9daf8; color: black'
        case _:
            if re.match(r'^W\ .*', val):
                return 'background-color: #ffd966; color: black'
            return ''

def highlight_status(status: str):
    match status:
        case 'Q':
            return 'background-color: #d0e0e3; color: black'
        case 'O':
            return 'background-color: #fce5cd; color: black'
        case 'IR':
            return 'background-color: #990000; color: black'
        case _:
            return ''



def color_column(col: Series, color: str):
    return [f'background-color: {color}; color: black'] * len(col)


def style_sheet(sheet: pd.DataFrame, col_names: ColNames) -> StylerRenderer:
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    styled = sheet.style\
        .map(highlight_owner, subset='Owner')\
        .map(highlight_status, subset='Sts')\
        .apply(lambda col: color_column(col, '#fce5cd'), subset=col_names.opp_col)\
        .apply(lambda col: color_column(col, '#d9ead3'), subset=col_names.pt_opp_col)\
        .apply(lambda col: color_column(col, '#d9d2e9'), subset=col_names.ops_g_col)\
        .apply(lambda col: color_column(col, '#d0e0e3'), subset='Pts/G')\
        .background_gradient(cmap=colors.dark_rwg_cm, subset='GP')\
        .background_gradient(cmap=colors.rwg_cm, subset=col_names.pt_opp_z_col)\
        .background_gradient(cmap=colors.dark_rwg_cm, subset=col_names.ops_g_z_col)\
        .background_gradient(cmap=colors.cwy_cm, subset='P/G Z')\
        .background_gradient(cmap=colors.bwo_cm, subset='Zval')\
        .format(precision=2, subset=[col_names.ops_g_col, 'Pts', col_names.pt_opp_col, col_names.pt_opp_z_col, 'Pts/G', col_names.ops_g_z_col, 'P/G Z', 'Zval'])

    return styled
