"""
data/schedule_provider_wnba.py
================================
Today's WNBA schedule from ESPN's public scoreboard endpoint -- free, no key,
same "never raises" contract as data/schedule_provider.py (MLB): any
network/parsing problem logs and returns [] so the daily run still produces
a report instead of crashing.

WNBA games have no probable-pitcher equivalent, so Game.home_pitcher/
away_pitcher stay None -- grading factors that depend on those (matchup_
pitching, advanced_analytics) degrade gracefully to a neutral signal, same
as they already do on any MLB day with unconfirmed starters.
"""

import logging

import requests

from engine.models import Game
from data.teams_wnba import normalize_wnba_team

logger = logging.getLogger(__name__)

ESPN_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard"


def get_todays_wnba_games(date_str):
    """date_str: 'YYYY-MM-DD'."""
    try:
        resp = requests.get(ESPN_SCOREBOARD, params={"dates": date_str.replace("-", "")}, timeout=15)
        resp.raise_for_status()
        payload = resp.json()
    except Exception as exc:
        logger.error("Failed to fetch WNBA schedule for %s: %s", date_str, exc)
        return []

    games = []
    for event in payload.get("events", []):
        try:
            games.append(_parse_event(event, date_str))
        except Exception as exc:
            logger.warning("Skipping one WNBA game we couldn't parse: %s", exc)
    return [g for g in games if g]


def _parse_event(event, date_str):
    competitions = event.get("competitions", [])
    if not competitions:
        return None
    competitors = competitions[0].get("competitors", [])
    home = next((c for c in competitors if c.get("homeAway") == "home"), None)
    away = next((c for c in competitors if c.get("homeAway") == "away"), None)
    if not home or not away:
        return None

    return Game(
        game_id=f"wnba-{event['id']}",
        date=date_str,
        home_team=normalize_wnba_team(home.get("team", {}).get("displayName", "")),
        away_team=normalize_wnba_team(away.get("team", {}).get("displayName", "")),
        game_time_utc=event.get("date"),
        sport="WNBA",
    )
