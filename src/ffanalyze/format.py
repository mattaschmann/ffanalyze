import re

from pandas import Series

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


def color_column(col: Series, color: str):
    return [f'background-color: {color}; color: black'] * len(col)
