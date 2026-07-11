"""
data/teams_wnba.py
===================
WNBA team list + name normalization, same pattern as data/teams.py (kept
separate rather than merged so MLB abbreviations never collide with WNBA
ones -- e.g. "CON" Connecticut Sun vs no MLB clash, but future sports might).
"""

WNBA_TEAMS = {
    "ATL": {"name": "Atlanta Dream", "aliases": ["dream"]},
    "CHI": {"name": "Chicago Sky", "aliases": ["sky"]},
    "CON": {"name": "Connecticut Sun", "aliases": ["sun", "connecticut"]},
    "DAL": {"name": "Dallas Wings", "aliases": ["wings"]},
    "GSV": {"name": "Golden State Valkyries", "aliases": ["valkyries", "golden state"]},
    "IND": {"name": "Indiana Fever", "aliases": ["fever"]},
    "LAS": {"name": "Las Vegas Aces", "aliases": ["aces"]},
    "LA": {"name": "Los Angeles Sparks", "aliases": ["sparks"]},
    "MIN": {"name": "Minnesota Lynx", "aliases": ["lynx"]},
    "NY": {"name": "New York Liberty", "aliases": ["liberty"]},
    "PHX": {"name": "Phoenix Mercury", "aliases": ["mercury"]},
    "SEA": {"name": "Seattle Storm", "aliases": ["storm"]},
    "WAS": {"name": "Washington Mystics", "aliases": ["mystics"]},
}

_LOOKUP = {}
for _abbr, _info in WNBA_TEAMS.items():
    _LOOKUP[_abbr.lower()] = _abbr
    _LOOKUP[_info["name"].lower()] = _abbr
    for _alias in _info["aliases"]:
        _LOOKUP[_alias.lower()] = _abbr


def normalize_wnba_team(raw):
    if not raw:
        return raw
    key = raw.strip().lower()
    if key in _LOOKUP:
        return _LOOKUP[key]
    for alias, abbr in _LOOKUP.items():
        if alias in key or key in alias:
            return abbr
    return raw.strip().upper()[:3]


def wnba_team_full_name(abbr):
    return WNBA_TEAMS.get(abbr, {}).get("name", abbr)
