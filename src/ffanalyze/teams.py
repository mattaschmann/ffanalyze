import pandas as pd

def team_abbr() -> pd.DataFrame:
    return pd.DataFrame({
        'Abbr': [ 'Ari', 'Atl', 'Bal', 'Buf', 'Car', 'Chi', 'Cin', 'Cle', 'Dal', 'Den', 'Det', 'GB', 'Hou', 'Ind', 'Jax', 'KC', 'LAC', 'LAR', 'LV', 'Mia', 'Min', 'NE', 'NO', 'NYG', 'NYJ', 'Phi', 'Pit', 'SF', 'Sea', 'TB', 'Ten', 'Was' ],
        'Team': [ 'Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants', 'New York Jets', 'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Commanders' ]
    })


if __name__ == '__main__':
    print(team_abbr())
