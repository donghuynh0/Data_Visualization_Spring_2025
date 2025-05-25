import pandas as pd


def win_percentage(df, country):
    # Home
    home_matches = df[df['home_team'] == country]
    home_wins = home_matches[home_matches['winner'] == country]
    home_win_per = round((len(home_wins) / len(home_matches)) * 100, 2) if len(home_matches) > 0 else 0.0

    # Away
    away_matches = df[df['away_team'] == country]
    away_wins = away_matches[away_matches['winner'] == country]
    away_win_per = round((len(away_wins) / len(away_matches)) * 100, 2) if len(away_matches) > 0 else 0.0

    # Total matches

    matches_played = len(home_matches) + len(away_matches)

    return {
        "country": country,
        "home_win_percent": home_win_per,
        "away_win_percent": away_win_per,
        "home matches": len(home_matches),
        "away_matches": len(away_matches),
        "total matches": matches_played
    }


def country_match_summary(df):
    records = []

    countries = pd.unique(df[['home_team', 'away_team']].values.ravel())

    for country in countries:
        for tournament in df['tournament'].unique():
            # Filter relevant matches
            matches = df[
                ((df['home_team'] == country) | (df['away_team'] == country)) & (df['tournament'] == tournament)]

            total_matches = len(matches)
            wins = len(matches[matches['winner'] == country])
            draws = len(matches[matches['winner'] == 'Draw'])
            losses = total_matches - wins - draws

            if total_matches > 0:
                records.append({
                    'country': country,
                    'tournament': tournament,
                    'total_matches': total_matches,
                    'wins': wins,
                    'losses': losses,
                    'draws': draws
                })

    return pd.DataFrame(records)
