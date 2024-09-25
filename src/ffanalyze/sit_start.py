import pandas as pd
from pandas.io.formats.style import StylerRenderer

from ffanalyze import colors, stats
from ffanalyze.format import color_column, highlight_owner, highlight_status
from ffanalyze.position import Position


def sheet() -> pd.DataFrame:
    target_positions = [
        Position.QB,
        Position.WR,
        Position.RB,
        Position.TE,
    ]
    all_pos = []
    for p in target_positions:
        temp = stats.sheet(p)[
            [
                "PlayerId",
                "PlayerName",
                "Sts",
                "Pos",
                "Owner",
                "GP",
                "Pts/G",
                "P/G Z",
                "Zval",
                "Opp",
                "D PCo",
                "EZ",
            ]
        ]

        temp = temp[
            (temp["Owner"] == "Injured Reserves")
            | (temp["Owner"] == "FA")
            | (temp["Owner"].str.match(r"^W\ \(.*\).*$"))  # type: ignore
        ]
        all_pos.append(temp)

    result = pd.concat(all_pos, axis=0)
    result = result.drop_duplicates(subset="PlayerId", keep="last")
    result.set_index("PlayerId", inplace=True)
    return result


def style_sheet(sheet: pd.DataFrame) -> StylerRenderer:
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)

    styled = (
        sheet.style.map(highlight_owner, subset="Owner")
        .map(highlight_status, subset="Sts")
        .apply(lambda col: color_column(col, "#d0e0e3"), subset="Pts/G")
        .background_gradient(cmap=colors.rwg_cm, subset=["D PCo"])
        .background_gradient(cmap=colors.bwo_cm, subset=["Zval", "EZ"])
        .background_gradient(cmap=colors.cwy_cm, subset=["P/G Z"])
        .background_gradient(cmap=colors.dark_rwg_cm, subset="GP")
        .set_properties(**{"text-align": "left"}, subset=["PlayerName", "Opp", "Owner"])
        .set_properties(**{"text-align": "center", "font-weight": "bold"}, subset=["Sts"])
        .set_table_styles([{"selector": "th", "props": [("text-align", "left")]}])
    )
    result = styled.format(
        precision=2,
        subset=[
            "Pts/G",
            "P/G Z",
            "Zval",
            "D PCo",
            "EZ",
        ],
    )

    return result
