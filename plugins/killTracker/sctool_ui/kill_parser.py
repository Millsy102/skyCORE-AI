# kill_parser.py

import re
from typing import Optional

CHROME_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/112.0.5615.121 Safari/537.36"
)
KILL_LOG_PATTERN = re.compile(
    r"<(?P<timestamp>[^>]+)> \[Notice\] <Actor Death> CActor::Kill: '(?P<victim>[^']+)' "
    r"\[(?P<victim_geid>\d+)\] in zone '(?P<zone>[^']+)' "
    r"killed by '(?P<attacker>[^']+)' \[(?P<attacker_geid>\d+)\] using '(?P<weapon>[^']+)' \[.*\] "
    r"with damage type '(?P<damage_type>\w+)' "
    r"from direction x: (?P<x>-?[\d.]+), y: (?P<y>-?[\d.]+), z: (?P<z>-?[\d.]+) \[.*?\]"
)
GAME_MODE_PATTERN = re.compile(
    r"<(?P<timestamp>[^>]+)> Loading GameModeRecord='(?P<game_mode>[^']+)' with EGameModeId='[^']+'"
)

GAME_MODE_MAPPING = {
    'EA_TeamElimination': 'Team Elimination',
    'EA_Elimination': 'Elimination',
    'SC_Default': 'PU',
    'EA_FPSGunGame': 'Gun Rush',
    'EA_TonkRoyale_TeamBattle': 'Tonk Royale',
    'EA_FreeFlight': 'Free Flight',
    'EA_SquadronBattle': 'Squadron Battle',
    'EA_VehicleKillConfirmed': 'Vehicle Kill Confirmed',
    'EA_FPSKillConfirmed': 'FPS Kill Confirmed',
    'EA_Control': 'Control',
    'EA_Duel': 'Duel',
    'SC_Frontend': 'Main Menu'
}

class KillParser:
    @staticmethod
    def process_replacements(replacements: dict, text: str) -> str:
        for pattern, repl in replacements.items():
            text = re.sub(pattern, repl, text)
        return text

    @staticmethod
    def format_zone(zone: str) -> str:
        if not zone:
            return "Unknown"
        zone = KillParser.process_replacements({r"_[0-9]+$": ""}, zone)

        container_replacements = {
            r"OOC_([A-Za-z]+)_([A-Za-z0-9]{1,2})_(.*)": r"\3 (\1 \2)",
            r"ObjectContainer-ugf.*": "Bunker",
            r"^Hangar_": "Hangar",
            r"ObjectContainer-0002_INT": "Klescher Interior"
        }
        zone = KillParser.process_replacements(container_replacements, zone)
        match = re.match(r"^([A-Z]{3,4})_(.*)$", zone)
        if match:
            make_code = match.group(1)
            model = match.group(2).replace("_", " ")
            makes = {
                "AEGS": "Aegis",
                "ANVL": "Anvil",
                "XIAN": "Aopoa",
                "XNAA": "Aopoa",
                "ARGO": "Argo",
                "BANU": "Banu",
                "CNOU": "C.O.",
                "CRUS": "Crusader",
                "DRAK": "Drake",
                "ESPR": "Esperia",
                "GAMA": "Gatac",
                "GRIN": "Greycat",
                "KRIG": "Kruger",
                "MRAI": "Mirai",
                "MISC": "MISC",
                "ORIG": "Origin",
                "RSI": "RSI",
                "TMBL": "Tumbril",
                "VNCL": "Vanduul"
            }
            make = makes.get(make_code, make_code)
            zone = f"{make} {model}"
        return zone

    @staticmethod
    def format_weapon(weapon: str) -> str:
        if not weapon:
            return "Unknown"
        replacements = {
            r"^[A-Za-z]{4}_": "",
            r"_[0-9]{2}_.*": "",
            r"_[0-9]+$": "",
            r"([a-z])([A-Z])": r"\1 \2",
            r"smg": "SMG",
            r"energy": "Laser"
        }
        weapon = KillParser.process_replacements(replacements, weapon)
        parts = weapon.split('_')
        if len(parts) > 1:
            weapon = " ".join(reversed(parts))
        return weapon.title()

    @staticmethod
    def determine_death_type(parsed: dict, handle: str) -> str:
        victim = parsed.get('victim', '')
        attacker = parsed.get('attacker', '')
        damage_type = parsed.get('damage_type', '')
        if victim == handle and (attacker == handle or damage_type.lower() == "suicide"):
            return "Suicide"
        elif victim == handle:
            return "Death"
        elif attacker == handle:
            return "Kill"
        elif attacker == victim or damage_type.lower() == "suicide":
            return "Selfkill"
        else:
            return "Other"

    @staticmethod
    def is_npc(name, actor_id=None):
        """
        Determine if a player name is an NPC based on common patterns.
        """
        if not name:
            return False

        name_lower = name.lower()

        if "kopion" in name_lower or "quasigrazer" in name_lower:
            return True

        npc_patterns = ["pu_", "npc", "enemy", "criminal", "soldier", "engineer",
                        "gunner", "sniper", "shipjacker"]
        for pattern in npc_patterns:
            if pattern in name_lower:
                return True

        if re.search(r"\d{8,}$", name):
            return True

        return False

    @staticmethod
    def parse_actor_death_event(log_line: str, handle: Optional[str] = None) -> dict:
        match = KILL_LOG_PATTERN.search(log_line)
        if not match:
            return {}

        data = match.groupdict()
        data['zone'] = KillParser.format_zone(data.get('zone', ''))
        data['weapon'] = KillParser.format_weapon(data.get('weapon', ''))

        victim = data.get('victim', '')
        data['victim_is_npc'] = KillParser.is_npc(victim, data.get('victim_geid'))

        attacker = data.get('attacker', '')
        data['attacker_is_npc'] = KillParser.is_npc(attacker, data.get('attacker_geid'))

        if handle:
            data['death_type'] = KillParser.determine_death_type(data, handle)

        return data