# Registered_kill.py

def format_registered_kill(
    log_line: str,
    data: dict,
    registered_user: str,
    full_timestamp: str,
    last_game_mode: str,
    success: bool = True
):
    from urllib.parse import quote
    from fetch import fetch_player_details, fetch_victim_image_base64
    from kill_parser import KillParser
    import re

    victim = data.get('victim', 'Unknown')
    zone = data.get('zone', 'Unknown')
    damage_type = data.get('damage_type', 'Unknown')
    weapon = data.get('weapon', 'Unknown')
    
    killer_ship = data.get('killer_ship', "Player destruction")
    killer_ship = re.sub(r'_\d+$', '', killer_ship)
    killer_ship = killer_ship.replace("_", " ")
    killer_ship = re.sub(r'\s+\d+$', '', killer_ship)
    if killer_ship.lower() == "no ship":
        killer_ship = ""
    
    formatted_zone = KillParser.format_zone(zone)
    formatted_weapon = KillParser.format_weapon(weapon)
    details = fetch_player_details(victim)
    victim_image_data_uri = fetch_victim_image_base64(victim)
    victim_profile_url = f"https://robertsspaceindustries.com/citizens/{quote(victim)}"
    victim_link = f'<a href="{victim_profile_url}" style="color:#f04747; text-decoration:none;">{victim}</a>'
    display_timestamp = full_timestamp.split(" ")[0] if " " in full_timestamp else full_timestamp
    
    log_line_with_mode = (
        log_line.strip() +
        f" [GameMode: {last_game_mode if last_game_mode else 'Unknown'}]"
    )
    
    if damage_type.lower() == "vehicledestruction":
        if killer_ship.lower() not in ["vehicle destruction", "player destruction", ""]:
            engagement = f"{killer_ship} using {formatted_weapon}"
        else:
            engagement = f"{formatted_weapon}"
        method = "Vehicle destruction"
    else:
        engagement = f"{formatted_weapon}"
        method = "Player destruction"

    header_text = (
        "New Kill Recorded Successfully"
        if success else "New Kill Did Not Get Recorded Successfully"
    )
    
    readout = f"""
<html>
<body style="margin:0; padding:0;">
    <div style="position: relative; display: inline-block; width: 100%;" class="newEntry">
        <table width="100%" cellspacing="0" cellpadding="15"
               style="background-color:#121212; font-family:'Segoe UI', Arial, sans-serif;
                      color:#e0e0e0; box-shadow: 0 0 15px 5px #66ff66,
                      0 0 25px 10px #66ff66; margin-bottom:15px; 
                      border-radius: 10px; overflow: hidden;">
            <tr>
                <td colspan="2" style="background: linear-gradient(135deg, #151515, #0d0d0d); border-bottom: 1px solid #333333; padding: 12px 15px;">
                    <div style="font-size:22px; font-weight:bold; color: #66ff66; text-shadow: 0 0 5px #66ff66; display: flex; align-items: center;">
                        <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: #66ff66; margin-right: 10px; box-shadow: 0 0 5px #66ff66;"></span>
                        YOU KILLED {victim.upper()}
                    </div>
                </td>
            </tr>
            <tr>
                <td style="vertical-align:top; padding-top: 15px; width: 70%;">
                    <table style="width: 100%; border-collapse: separate; border-spacing: 0 8px;">
                        <tr>
                            <td style="background-color: #262610; padding: 12px; border-radius: 8px; border-left: 3px solid #ffcc00;">
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #ffcc00;">Timestamp:</b> {display_timestamp}</p>
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #ffcc00;">Game Mode:</b> <span style="color: #00ccff; text-shadow: 0 0 2px #00ccff;">{last_game_mode if last_game_mode else 'Unknown'}</span></p>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #102610; padding: 12px; border-radius: 8px; border-left: 3px solid #66ff66;">
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #66ff66;">Attacker:</b> <span style="color: #66ff66; text-shadow: 0 0 2px #66ff66;">{registered_user}</span></p>
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #66ff66;">Engagement:</b> {engagement}</p>
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #66ff66;">Method:</b> {method}</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #260c0c; padding: 12px; border-radius: 8px; border-left: 3px solid #f04747;">
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #f04747;">Victim:</b> {victim_link}</p>
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #f04747;">Location:</b> {formatted_zone}</p>
                                <p style="font-size:14px; margin:4px 0;">
                                    <b style="color: #f04747;">Organization:</b> {details.get('org_name', 'None')} 
                                    <span style="color: #888888;">(Tag:</span>
                                    <a href="https://robertsspaceindustries.com/en/orgs/{details.get('org_tag', 'None')}"
                                       style="color:#f04747; text-decoration:none;">
                                       {details.get('org_tag', 'None')}
                                    </a><span style="color: #888888;">)</span>
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
                <td style="vertical-align:top; text-align:right; padding-top: 15px; width: 30%;">
                    <div style="border-radius: 50%; padding: 3px; box-shadow: 0 0 10px #f04747;">
                        <div style="position: relative; overflow: hidden; border-radius: 50%;">
                            <img src="{victim_image_data_uri}" width="110" height="110"
                                 style="object-fit:cover; border-radius: 50%;" alt="Profile Image">
                            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                                      border-radius: 50%; box-shadow: inset 0 0 20px #f04747;"></div>
                        </div>
                    </div>
                </td>
            </tr>
        </table>
    </div>
</body>
</html>
"""
    
    payload_ship = killer_ship if killer_ship.lower() not in ["vehicle destruction", "player destruction"] else ""
    payload = {
        'log_line': log_line.strip(),
        'game_mode': last_game_mode if last_game_mode else "Unknown",
        'killer_ship': payload_ship,
        'method': method
    }
    
    return readout, payload