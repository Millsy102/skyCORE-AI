# Kill_thread.py

import os
import re
import json
import base64
import requests
import logging
import time
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote
from typing import Optional, Dict, Any, List

from PyQt5.QtCore import pyqtSignal, QThread, QDir, QTimer, Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QPushButton, QMessageBox
)

from kill_parser import GAME_MODE_MAPPING, GAME_MODE_PATTERN, KILL_LOG_PATTERN, CHROME_USER_AGENT, KillParser

from Registered_kill import format_registered_kill

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": CHROME_USER_AGENT})
cleanupPattern = re.compile(r'^(.+?)_\d+$')

class MissingKillsDialog(QDialog):
    def __init__(self, missing_kills, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Missing Kills Found")
        self.missing_kills = missing_kills
        self.checkbox_list = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        info_label = QLabel("Select which kills you’d like to send:")
        layout.addWidget(info_label)

        for kill in self.missing_kills:
            local_key = kill.get("local_key", "Unknown")
            parts = local_key.split("::")
            if len(parts) >= 3:
                label_text = f"{parts[1]} ({parts[2]})"
            else:
                label_text = local_key
            checkbox = QCheckBox(label_text)
            checkbox.setChecked(True)
            layout.addWidget(checkbox)
            self.checkbox_list.append((checkbox, kill))

        button_layout = QHBoxLayout()
        send_button = QPushButton("Send Selected")
        send_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(send_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.initStyles()

    def getSelectedKills(self):
        selected = []
        for checkbox, kill_data in self.checkbox_list:
            if checkbox.isChecked():
                selected.append(kill_data)
        return selected

    def initStyles(self):
        self.setStyleSheet(
            "QDialog { background-color: #0d0d0d; color: #f0f0f0; border: 1px solid #f04747; }"
            "QLabel { color: #f0f0f0; font-weight: bold; font-size: 14px; }"
            "QCheckBox { color: #f0f0f0; }"
            "QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #2a2a2a; "
            "   border-radius: 3px; background-color: #1e1e1e; }"
            "QCheckBox::indicator:checked { background-color: #f04747; }"
            "QPushButton { background-color: #1e1e1e; border: 1px solid #2a2a2a; "
            "   border-radius: 4px; padding: 8px 12px; color: #f0f0f0; }"
            "QPushButton:hover { background-color: #2a2a2a; border-color: #f04747; }"
        )

class TailThread(QThread):
    kill_detected = pyqtSignal(str, str)
    death_detected = pyqtSignal(str, str)
    player_registered = pyqtSignal(str)
    game_mode_changed = pyqtSignal(str)
    payload_ready = pyqtSignal(dict, str, str, str)
    death_payload_ready = pyqtSignal(dict, str, str, str)
    ship_updated = pyqtSignal(str)

    def __init__(self, file_path: str, config_file: Optional[str] = None, callback=None) -> None:
        super().__init__()
        self.file_path = file_path
        self.config_file = config_file
        self._stop_event = False
        self.last_game_mode: str = "Unknown"
        self.registered_user: Optional[str] = None
        self.has_registered = False
        self.current_attacker_ship: Optional[str] = "Player destruction"

    def reset_killer_ship(self) -> None:
        self.current_attacker_ship = "No Ship"
        self.update_config_killer_ship("No Ship")
        self.ship_updated.emit("No Ship")

    def update_config_killer_ship(self, ship: str) -> None:
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except Exception as e:
                logging.error(f"Error reading config: {e}")
                config = {}
            config["killer_ship"] = ship
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                logging.info(f"Updated config with killer_ship: {ship}")
            except Exception as e:
                logging.error(f"Error saving config with killer_ship: {e}")

    def clear_config_killer_ship(self) -> None:
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except Exception as e:
                logging.error(f"Error reading config for clearing killer_ship: {e}")
                config = {}
            if "killer_ship" in config:
                del config["killer_ship"]
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                logging.info("Cleared killer_ship from config.")
            except Exception as e:
                logging.error(f"Error saving config while clearing killer_ship: {e}")

    def run(self) -> None:
        logging.info("TailThread started.")
        timeout_seconds = 10
        while not self._stop_event:
            try:
                with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
                    self.process_existing_player_registrations(f)
                    f.seek(0, os.SEEK_END)
                    last_activity = time.time()
                    logging.info(f"Started tailing {self.file_path} for new entries...")
                    while not self._stop_event:
                        line = f.readline()
                        if line:
                            self.process_line(line.strip())
                            last_activity = time.time()
                        else:
                            try:
                                current_size = os.path.getsize(self.file_path)
                                if f.tell() > current_size:
                                    logging.info("Detected file truncation. Resetting pointer to beginning.")
                                    f.seek(0, os.SEEK_SET)
                                    last_activity = time.time()
                            except Exception as e:
                                logging.error(f"Error checking file size: {e}")
                            
                            if time.time() - last_activity > timeout_seconds:
                                try:
                                    if os.path.getsize(self.file_path) == 0:
                                        logging.info("Log file appears empty. Waiting for new entries...")
                                        f.seek(0, os.SEEK_SET)
                                        last_activity = time.time()
                                except Exception as e:
                                    logging.error(f"Error checking file size: {e}")
                            time.sleep(0.1)
            except Exception as e:
                logging.error(f"Error in TailThread: {e}")
            time.sleep(0.5)
        logging.info("TailThread terminated.")

    def process_existing_player_registrations(self, f) -> None:
        logging.info("Processing existing entries for legacy login responses and game modes...")
        for line in f:
            stripped_line = line.strip()
            legacy_login_match = re.search(
                r"<(?P<timestamp>[^>]+)> \[Notice\] <Legacy login response> \[CIG-net\] User Login Success - Handle\[(?P<handle>[^\]]+)\]",
                stripped_line
            )
            if legacy_login_match:
                handle = legacy_login_match.group('handle').strip()
                if self.registered_user != handle:
                    self.registered_user = handle
                    self.has_registered = True
                    self.player_registered.emit(f"Registered user: {handle}")
                    logging.info(f"Updated registered user to: {handle}")
            gm_match = GAME_MODE_PATTERN.search(stripped_line)
            if gm_match:
                data = gm_match.groupdict()
                raw = data.get('game_mode')
                mapped = GAME_MODE_MAPPING.get(raw)
                if mapped and mapped != self.last_game_mode:
                    self.last_game_mode = mapped
                    self.game_mode_changed.emit(f"Monitoring game mode: {mapped}")
                    self.reset_killer_ship()
                elif not mapped:
                    logging.warning(f"Unknown game mode '{raw}'")

    def process_jump_drive_line(self, line: str) -> None:
        match = re.search(r'\(adam:\s+(?P<ship>(?:[A-Za-z0-9_]+?)(?=_\d+\s+in zone)|[A-Za-z0-9_]+)\s+in zone', line)
        if match:
            raw_ship = match.group('ship')
            if not re.match(r'^(ORIG|CRUS|RSI|AEGS|VNCL|DRAK|ANVL|BANU|MISC|CNOU|XIAN|GAMA|TMBL|ESPR|KRIG|GRIN|XNAA|MRAI)', raw_ship):
                logging.warning(f"Jump Drive: Ship name doesn't have a recognized manufacturer code: {raw_ship}")
                return

            cleaned_ship = re.sub(r'_\d+$', '', raw_ship)
            cleaned_ship = cleaned_ship.replace('_', ' ')
            cleaned_ship = re.sub(r'\s+\d+$', '', cleaned_ship)
            
            self.current_attacker_ship = cleaned_ship
            logging.info(f"Jump Drive: Updated killer ship to: {cleaned_ship}")
            self.update_config_killer_ship(cleaned_ship)
            self.ship_updated.emit(cleaned_ship)

    def process_line(self, line: str) -> None:
        if "<Jump Drive Requesting State Change>" in line:
            self.process_jump_drive_line(line)
        legacy_login_match = re.search(
            r"<(?P<timestamp>[^>]+)> \[Notice\] <Legacy login response> \[CIG-net\] User Login Success - Handle\[(?P<handle>[^\]]+)\]",
            line
        )
        if legacy_login_match:
            handle = legacy_login_match.group('handle').strip()
            if self.registered_user != handle:
                self.registered_user = handle
                self.has_registered = True
                self.player_registered.emit(f"Registered user updated: {handle}")
                logging.info(f"Updated registered user to: {handle}")
            return
        gm_match = GAME_MODE_PATTERN.search(line)
        if gm_match:
            data = gm_match.groupdict()
            gm_raw = data.get('game_mode')
            mapped = GAME_MODE_MAPPING.get(gm_raw, gm_raw)
            if mapped and mapped != self.last_game_mode:
                self.last_game_mode = mapped
                self.game_mode_changed.emit(f"Monitoring game mode: {mapped}")
            elif not mapped:
                logging.warning(f"Unknown game mode '{gm_raw}' encountered.")
            return
        kill_match = KILL_LOG_PATTERN.search(line)
        if kill_match:
            self.handle_kill_event(line, kill_match)

    def handle_kill_event(self, line: str, match_obj: re.Match) -> None:
        data = match_obj.groupdict()
        timestamp_iso = data.get('timestamp')
        try:
            dt = datetime.fromisoformat(timestamp_iso.replace('Z', '+00:00'))
            full_timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            display_timestamp = dt.strftime('%Y-%m-%d')
        except ValueError:
            full_timestamp = timestamp_iso
            display_timestamp = timestamp_iso

        victim = data.get('victim', '').strip()
        attacker = data.get('attacker', '').strip()

        if KillParser.is_npc(victim):
            logging.info(f"NPC kill detected (victim: {victim}). Not processing.")
            return
            
        if "subside" in victim.lower() or "subside" in attacker.lower():
            return
        if not self.registered_user:
            return
        if (attacker.lower() == self.registered_user.strip().lower() and
            victim.lower() == self.registered_user.strip().lower()):
            try:
                from Death_kill import format_death_kill
                captured_game_mode = self.last_game_mode if self.last_game_mode and self.last_game_mode != "Unknown" else "Unknown"
                readout = format_death_kill(line, data, self.registered_user, display_timestamp, captured_game_mode)
                self.death_detected.emit(readout, victim)
            except Exception as e:
                logging.error(f"Error formatting suicide event: {e}")
            return

        captured_game_mode = self.last_game_mode if self.last_game_mode and self.last_game_mode != "Unknown" else "Unknown"
        if data.get("damage_type", "").lower() == "vehicledestruction":
            chosen_ship = self.current_attacker_ship.strip() or "Unknown Ship"
            data["killer_ship"] = chosen_ship
        else:
            data["killer_ship"] = "Player destruction"

        if attacker.lower() == self.registered_user.strip().lower():
            try:
                readout, payload = format_registered_kill(
                    line, data, self.registered_user, full_timestamp, captured_game_mode, success=True
                )
                self.kill_detected.emit(readout, attacker)
                self.payload_ready.emit(payload, full_timestamp, attacker, readout)
            except Exception as e:
                logging.error(f"Error formatting registered kill: {e}")
        elif victim.lower() == self.registered_user.strip().lower():
            try:
                from Death_kill import format_death_kill
                readout = format_death_kill(line, data, self.registered_user, full_timestamp, captured_game_mode)
                self.death_detected.emit(readout, victim)

                death_payload = {
                    'log_line': line.strip(),
                    'game_mode': captured_game_mode,
                    'victim_name': victim,
                    'attacker_name': attacker,
                    'weapon': data.get('weapon', 'Unknown'),
                    'damage_type': data.get('damage_type', 'Unknown'),
                    'location': data.get('zone', 'Unknown'),
                    'timestamp': full_timestamp,
                    'event_type': 'death'
                }
                self.death_payload_ready.emit(death_payload, full_timestamp, attacker, readout)
            except Exception as e:
                logging.error(f"Error formatting or sending death payload: {e}")
        else:
            logging.info("Ignoring kill event: registered user is neither attacker nor victim.")

    def stop(self) -> None:
        logging.info("Stopping TailThread.")
        self._stop_event = True
        self.clear_config_killer_ship()

class RescanThread(QThread):
    rescanFinished = pyqtSignal(list)

    def __init__(self, file_path: str, registered_user: str, parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self.file_path = file_path
        self._stop_event = False
        self.found_kills: List[dict] = []
        self.registered_user = registered_user.lower() if registered_user else ""

    def run(self) -> None:
        current_game_mode = "Unknown"
        current_ship = ""
        jump_drive_pattern = re.compile(r'\(adam:\s+(?P<ship>(?:[A-Za-z0-9_]+?)(?=_\d+\s+in zone)|[A-Za-z0-9_]+)\s+in zone')
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    if self._stop_event:
                        break
                    stripped = line.strip()
                    if "Loading GameModeRecord=" in stripped:
                        gm_match = GAME_MODE_PATTERN.search(stripped)
                        if gm_match:
                            data = gm_match.groupdict()
                            raw = data.get('game_mode')
                            mapped = GAME_MODE_MAPPING.get(raw, "Unknown")
                            current_game_mode = mapped
                    j_match = jump_drive_pattern.search(stripped)
                    if j_match:
                        raw_ship = j_match.group('ship')

                        raw_ship = re.sub(r'_\d+$', '', raw_ship)
                        current_ship = raw_ship.replace('_', ' ')
                        current_ship = re.sub(r'\s+\d+$', '', current_ship)
                    if "CActor::Kill:" in stripped:
                        kill_match = KILL_LOG_PATTERN.search(stripped)
                        if kill_match:
                            data = kill_match.groupdict()
                            attacker = data.get('attacker', '').lower().strip()
                            victim = data.get('victim', '').lower().strip()

                            if KillParser.is_npc(victim):
                                logging.info(f"NPC kill detected during rescan (victim: {victim}). Skipping.")
                                continue
                                
                            if attacker == self.registered_user:
                                timestamp_iso = data.get('timestamp')
                                try:
                                    timestamp = datetime.fromisoformat(timestamp_iso.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
                                except ValueError:
                                    timestamp = timestamp_iso
                                local_key = f"{timestamp}::{victim}::{current_game_mode}"
                                payload = {'log_line': stripped, 'game_mode': current_game_mode}
                                if data.get("damage_type", "").lower() == "vehicledestruction":
                                    if current_ship:
                                        cleaned_ship = re.sub(r'_\d+$', '', current_ship)
                                        cleaned_ship = cleaned_ship.replace('_', ' ')
                                        cleaned_ship = re.sub(r'\s+\d+$', '', cleaned_ship)
                                        payload["killer_ship"] = cleaned_ship
                                    else:
                                        payload["killer_ship"] = "Unknown Ship"
                                else:
                                    payload["killer_ship"] = "Player destruction"
                                self.found_kills.append({
                                    "local_key": local_key,
                                    "payload": payload,
                                    "timestamp": timestamp
                                })
                    QThread.yieldCurrentThread()
        except Exception as e:
            logging.error(f"Error in RescanThread: {e}")
        self.rescanFinished.emit(self.found_kills)

    def stop(self) -> None:
        self._stop_event = True

class ApiSenderThread(QThread):
    apiResponse = pyqtSignal(str)

    def __init__(self, api_endpoint: str, headers: Dict[str, str], payload: dict, local_key: str, parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self.api_endpoint = api_endpoint
        self.headers = headers
        self.payload = payload
        self.local_key = local_key
        self.retry_count = 0
        self.max_retries = 5
        self.backoff = 1

    def run(self) -> None:
        while self.retry_count < self.max_retries:
            try:
                resp = requests.post(self.api_endpoint, headers=self.headers, json=self.payload, timeout=10)
                if resp.status_code == 201:
                    data_resp = resp.json()
                    server_msg = data_resp.get("message", "")
                    if "duplicate" in server_msg.lower():
                        self.apiResponse.emit("Duplicate kill. Not logged (server).")
                    return
                elif resp.status_code == 200:
                    data_resp = resp.json()
                    if data_resp.get("message") == "NPC not logged":
                        self.apiResponse.emit("NPC kill not logged.")
                    return
                elif 400 <= resp.status_code < 500:
                    error_text = f"Failed to log kill: {resp.status_code} - {resp.text}"
                    self.apiResponse.emit(error_text)
                    return
                else:
                    raise requests.exceptions.HTTPError(f"Server error: {resp.status_code}")
            except requests.exceptions.RequestException as e:
                self.retry_count += 1
                error_text = f"API request failed (Attempt {self.retry_count}/{self.max_retries}): {e}"
                self.apiResponse.emit(error_text)
                time.sleep(self.backoff)
                self.backoff *= 2
        self.apiResponse.emit("API request failed after maximum retries.")