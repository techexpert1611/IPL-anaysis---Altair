import altair as alt
from . import data_reader as dr


def facet_wrap(subplts, plots_per_row):
    rows = [subplts[i * plots_per_row:i * plots_per_row + plots_per_row] for i in range(len(subplts) // plots_per_row)]
    rows = [alt.hconcat(*charts) for charts in rows]
    return alt.vconcat(*rows).configure_axis(grid=False).configure_view(strokeOpacity=0).configure_axisBottom(
        labelAngle=0
    )


def batsman_vs_team(player, team):
    batsman_vs_teams = dr.batsman_runs[dr.batsman_runs['player'] == player][
        dr.batsman_runs['team'] == team]
    highlight = alt.selection(type='multi', on='mouseover',
                              fields=['match'], nearest=True)

    batsman_vs_team_base = alt.Chart(batsman_vs_teams).encode(
        x='match:O',
        y='runs:Q',
        tooltip=['player', 'runs', 'season', 'stadium'],
    )

    batsman_vs_team_points = batsman_vs_team_base.mark_circle().encode(
        opacity=alt.condition(~highlight, alt.value(0.7), alt.value(1)),
        size=alt.condition(~highlight, alt.value(70), alt.value(140))
    ).add_selection(
        highlight,
    ).properties(
        height=300,
        width=900
    )

    batsman_vs_team_lines = batsman_vs_team_base.mark_line(point=True).encode(
        opacity=alt.condition(~highlight, alt.value(0.7), alt.value(0.7)),
        size=alt.condition(~highlight, alt.value(2), alt.value(2))
    )
    return (batsman_vs_team_points + batsman_vs_team_lines).configure_axis(
        labels=False
    )


def top_runs_all_season():
    top_runs_bars = alt.Chart(dr.top_runs.head(10)).mark_bar().encode(
        x=alt.X('Player:N', sort=alt.EncodingSortField(field='Runs:Q', order='ascending')),
        y='Runs:Q',
        tooltip=['Player', 'Runs', 'Season'],
        color='Season:N',
    ).properties(
        height=300,
        width=900,
    ).configure_axis(
        labelFontSize=15,
        titleFontSize=17,
    ).configure_axisBottom(
        labelAngle=-45
    )
    return top_runs_bars


def top_runs_vs_teams():
    subplts = []
    for team in dr.top_runs_vs_team['team'].unique():
        subplts.append(
            (alt.Chart(dr.top_runs_vs_team[dr.top_runs_vs_team['team'] == team]).mark_bar(opacity=0.5).encode(
                x=alt.X('player:N'),
                y=alt.Y('runs:Q', axis=alt.Axis(tickCount=20)),
                tooltip=['player', 'runs', 'average'],
            ) + alt.Chart(dr.top_runs_vs_team[dr.top_runs_vs_team['team'] == team]).mark_line(point=True).encode(
                x=alt.X('player:N'),
                y=alt.Y('average:Q', axis=alt.Axis(tickCount=20)),
                tooltip=['player', 'runs', 'average'],
            )).properties(
                height=300,
                width=700,
                title=team
            )
        )
    compound_chart = facet_wrap(subplts, plots_per_row=1)
    return compound_chart.configure_line(
        color='red'
    ).configure_point(
        color='green',
        filled=True,
        opacity=1
    )


def batsman_vs_season(player, season):
    batsman_vs_seasons = dr.batsman_runs[dr.batsman_runs['player'] == player][
        dr.batsman_runs['season'] == int(season)]
    highlight = alt.selection(type='multi', on='mouseover',
                              fields=['match'], nearest=True)

    batsman_vs_season_base = alt.Chart(batsman_vs_seasons).encode(
        x='match:O',
        y='runs:Q',
        tooltip=['player', 'runs', 'team', 'stadium'],
    )

    batsman_vs_season_points = batsman_vs_season_base.mark_circle().encode(
        opacity=alt.condition(~highlight, alt.value(0.7), alt.value(1)),
        size=alt.condition(~highlight, alt.value(70), alt.value(140))
    ).add_selection(
        highlight,
    ).properties(
        height=300,
        width=900
    )

    batsman_vs_season_lines = batsman_vs_season_base.mark_line(point=True).encode(
        opacity=alt.condition(~highlight, alt.value(0.7), alt.value(0.7)),
        size=alt.condition(~highlight, alt.value(2), alt.value(2))
    )
    return (batsman_vs_season_points + batsman_vs_season_lines).configure_axis(
        labels=False
    )


def batsman_vs_stadium(player, stadium):
    batsman_vs_stadiums = dr.batsman_runs[dr.batsman_runs['player'] == player][
        dr.batsman_runs['stadium'] == stadium]
    highlight = alt.selection(type='multi', on='mouseover',
                              fields=['match'], nearest=True)

    batsman_vs_stadium_base = alt.Chart(batsman_vs_stadiums).encode(
        x='match:O',
        y='runs:Q',
        tooltip=['player', 'runs', 'team', 'season'],
    )

    batsman_vs_stadium_points = batsman_vs_stadium_base.mark_circle().encode(
        opacity=alt.condition(~highlight, alt.value(0.7), alt.value(1)),
        size=alt.condition(~highlight, alt.value(70), alt.value(140))
    ).add_selection(
        highlight,
    ).properties(
        height=300,
        width=900
    )

    batsman_vs_stadium_lines = batsman_vs_stadium_base.mark_line(point=True).encode(
        opacity=alt.condition(~highlight, alt.value(0.7), alt.value(0.7)),
        size=alt.condition(~highlight, alt.value(2), alt.value(2))
    )
    return batsman_vs_stadium_points + batsman_vs_stadium_lines


def wickets_vs_teams(player):
    wickets_against_a_team = dr.wickets_against_a_team[dr.wickets_against_a_team['player'] == player]
    wickets_vs_teams_bar = alt.Chart(wickets_against_a_team).mark_bar().encode(
        x='team',
        y='wickets',
        tooltip=['player', 'team', 'wickets', 'matches']
    ).properties(
        height=300,
        width=900
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=17,
        grid=False,
    ).configure_axisBottom(
        labelAngle=-45
    ).configure_view(
        strokeOpacity=0
    )
    wickets_vs_teams_bar.encoding.x.title = 'Vs Team'
    return wickets_vs_teams_bar


def wickets_vs_season(player):
    wickets_vs_seasons = dr.wickets_in_season[dr.wickets_in_season['player'] == player]
    wickets_vs_seasons_base = alt.Chart(wickets_vs_seasons).encode(
        x='season:O',
        y='wickets:Q',
        tooltip=['player', 'wickets', 'matches'],
    )
    highlight = alt.selection(type='multi', on='mouseover',
                              fields=['season'], nearest=True)

    wickets_vs_season_points = wickets_vs_seasons_base.mark_circle().encode(
        opacity=alt.condition(~highlight, alt.value(0.7), alt.value(1)),
        size=alt.condition(~highlight, alt.value(70), alt.value(140))
    ).add_selection(
        highlight,
    ).properties(
        height=300,
        width=900
    )

    wickets_vs_season_lines = wickets_vs_seasons_base.mark_line(point=True).encode(
        opacity=alt.condition(~highlight, alt.value(0.7), alt.value(0.7)),
        size=alt.condition(~highlight, alt.value(2), alt.value(2))
    )
    return (wickets_vs_season_points + wickets_vs_season_lines).configure_axis(
        grid=False
    ).configure_view(
        strokeOpacity=0
    ).configure_axisBottom(
        labelAngle=0
    )


def captains():
    captain_win_bar = alt.Chart(dr.captain_win_loss).mark_bar(color='steelblue', opacity=0.8).encode(
        x=alt.X('sum(wins):Q', axis=alt.Axis(title='wins and loses')),
        y='player:N',
        tooltip=['player', 'total', 'wins']
    )
    captain_loss_bar = alt.Chart(dr.captain_win_loss).mark_bar(color='red', opacity=0.5).encode(
        x='sum(loss):Q',
        y='player:N',
        tooltip=['player', 'total', 'loss']
    )
    return (captain_win_bar + captain_loss_bar).configure_axis(
        grid=False
    ).configure_view(
        strokeOpacity=0
    ).configure_axisBottom(
        labelAngle=-45
    ).resolve_scale(x='shared', y='shared')
