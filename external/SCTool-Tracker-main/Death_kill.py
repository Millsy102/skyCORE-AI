# Death_kill.py

def format_death_kill(log_line: str, data: dict, registered_user: str, timestamp: str, last_game_mode: str):
    from urllib.parse import quote
    from fetch import fetch_player_details, fetch_victim_image_base64
    from kill_parser import KillParser

    attacker = data.get('attacker', 'Unknown')
    zone = data.get('zone', 'Unknown')
    weapon = data.get('weapon', 'Unknown')
    formatted_zone = KillParser.format_zone(zone)
    formatted_weapon = KillParser.format_weapon(weapon)
    details = fetch_player_details(attacker)
    attacker_image_data_uri = fetch_victim_image_base64(attacker)
    attacker_profile_url = f"https://robertsspaceindustries.com/citizens/{quote(attacker)}"
    attacker_link = f'<a href="{attacker_profile_url}" style="color:#f04747; text-decoration:none;">{attacker}</a>'

    readout = f"""
<html>
<body>
    <div class="newEntry" style="width: 100%;">
        <table width="100%" cellspacing="0" cellpadding="15"
               style="background-color:#121212; font-family:'Segoe UI', Arial, sans-serif;
                      color:#e0e0e0; box-shadow: 0 0 15px 5px #f04747, 0 0 25px 10px #f04747; 
                      border-radius: 10px; margin-bottom: 15px; overflow: hidden;">
            <tr>
                <td colspan="2" style="background: linear-gradient(135deg, #151515, #0d0d0d); border-bottom: 1px solid #333333; padding: 12px 15px;">
                    <div style="font-size:24px; font-weight:bold; color: #f04747; text-shadow: 0 0 5px #f04747; display: flex; align-items: center;">
                        <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: #f04747; margin-right: 10px; box-shadow: 0 0 5px #f04747;"></span>
                        YOU DIED
                    </div>
                </td>
            </tr>
            <tr>
                <td style="vertical-align:top; padding-top: 15px; width: 70%;">
                    <table style="width: 100%; border-collapse: separate; border-spacing: 0 8px;">
                        <tr>
                            <td style="background-color: #0c2026; padding: 12px; border-radius: 8px; border-left: 3px solid #00ccff;">
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #00ccff;">Game Mode:</b> <span style="color: #00ccff; text-shadow: 0 0 2px #00ccff;">{last_game_mode if last_game_mode else 'Unknown'}</span></p>
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #00ccff;">Timestamp:</b> {timestamp}</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #260c0c; padding: 12px; border-radius: 8px; border-left: 3px solid #f04747;">
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #f04747;">Attacker:</b> {attacker_link}</p>
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
                        <tr>
                            <td style="background-color: #262610; padding: 12px; border-radius: 8px; border-left: 3px solid #ffcc00;">
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #ffcc00;">Location:</b> {formatted_zone}</p>
                                <p style="font-size:14px; margin:4px 0;"><b style="color: #ffcc00;">Damage Type:</b> {formatted_weapon}</p>
                            </td>
                        </tr>
                    </table>
                </td>
                <td style="vertical-align:top; text-align:right; padding-top: 15px; width: 30%;">
                    <div style="border-radius: 50%; padding: 3px; box-shadow: 0 0 10px #f04747;">
                        <div style="position: relative; overflow: hidden; border-radius: 50%;">
                            <img src="{attacker_image_data_uri}" width="110" height="110"
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
    return readout