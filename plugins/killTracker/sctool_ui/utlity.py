# utlity.py

import os
import re
import sys
import json
import time
import logging
from datetime import datetime, timedelta
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFormLayout, QComboBox, QCheckBox,
    QSlider, QFileDialog, QTextBrowser, QScrollArea,
    QSizePolicy, QApplication, QStackedWidget
)

from PyQt5.QtCore import (
    Qt, QUrl, QTimer, QStandardPaths, QDir, QSize, QRect
)

def get_appdata_paths() -> tuple[str, str, str]:
    appdata_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    if not appdata_dir:
        appdata_dir = os.path.expanduser("~")
    tracker_dir = os.path.join(appdata_dir, "SCTool_Tracker")
    QDir().mkpath(tracker_dir)

    config_file = os.path.join(tracker_dir, "config.json")
    log_file = os.path.join(tracker_dir, "kill_logger.log")
    return config_file, log_file, tracker_dir

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

CONFIG_FILE, LOG_FILE, TRACKER_DIR = get_appdata_paths()

logging.basicConfig(
    filename=LOG_FILE,
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def init_ui(self) -> None:
    main_widget = QWidget()
    main_widget.setStyleSheet(
        "QWidget { background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
        "stop:0 #1a1a1a, stop:1 #0d0d0d); "
        "border: 1px solid #2a2a2a; border-radius: 10px; }"
    )
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    sidebar = QWidget()
    sidebar.setFixedWidth(220)
    sidebar.setStyleSheet(
        "QWidget { background-color: #151515; border-right: 1px solid #2a2a2a; "
        "border-top-left-radius: 10px; border-bottom-left-radius: 10px; "
        "border-top-right-radius: 0px; border-bottom-right-radius: 0px; }"
    )
    sidebar_layout = QVBoxLayout(sidebar)
    sidebar_layout.setContentsMargins(0, 15, 0, 15)
    sidebar_layout.setSpacing(2)
    logo_container = QWidget()
    logo_container.setStyleSheet("border: none; background: transparent;")
    logo_layout = QVBoxLayout(logo_container)
    logo_layout.setContentsMargins(10, 0, 10, 20)

    self.user_profile_image = QLabel()
    self.user_profile_image.setFixedSize(64, 64)
    self.user_profile_image.setStyleSheet(
        "QLabel { border-radius: 32px; border: 2px solid #333333; background-color: #1a1a1a; }"
    )
    self.user_profile_image.setAlignment(Qt.AlignCenter)
    logo_layout.addWidget(self.user_profile_image, alignment=Qt.AlignCenter)
    self.set_default_user_image()
    
    app_title = QLabel("SCTool Tracker")
    app_title.setStyleSheet(
        "QLabel { color: #f04747; font-size: 16px; font-weight: bold; background: transparent; border: none; }"
    )
    app_title.setAlignment(Qt.AlignCenter)
    logo_layout.addWidget(app_title)
    
    self.user_display = QLabel("User: Not logged in")
    self.user_display.setStyleSheet(
        "QLabel { color: #f0f0f0; font-size: 12px; background: transparent; border: none; }"
    )
    self.user_display.setAlignment(Qt.AlignCenter)
    logo_layout.addWidget(self.user_display)
    
    self.game_mode_display = QLabel("Mode: Unknown")
    self.game_mode_display.setStyleSheet(
        "QLabel { color: #00ccff; font-size: 12px; background: transparent; border: none; }"
    )
    self.game_mode_display.setAlignment(Qt.AlignCenter)
    logo_layout.addWidget(self.game_mode_display)
    
    sidebar_layout.addWidget(logo_container)
    status_container = QWidget()
    status_container.setStyleSheet("border: none; background: transparent;")
    status_layout = QVBoxLayout(status_container)
    status_layout.setContentsMargins(15, 0, 15, 15)
    status_layout.setSpacing(10)
    monitoring_status = QHBoxLayout()
    self.monitoring_indicator = QLabel()
    self.monitoring_indicator.setFixedSize(12, 12)
    self.update_monitor_indicator(False)
    monitoring_label = QLabel("MONITORING")
    monitoring_label.setStyleSheet("QLabel { color: #999999; font-size: 11px; background: transparent; border: none; }")
    monitoring_status.addWidget(self.monitoring_indicator)
    monitoring_status.addWidget(monitoring_label)
    monitoring_status.addStretch()
    api_status = QHBoxLayout()
    self.api_indicator = QLabel()
    self.api_indicator.setFixedSize(12, 12)
    self.update_api_indicator(False)
    api_label = QLabel("API CONNECTED")
    api_label.setStyleSheet("QLabel { color: #999999; font-size: 11px; background: transparent; border: none; }")
    api_status.addWidget(self.api_indicator)
    api_status.addWidget(api_label)
    api_status.addStretch()
    twitch_status = QHBoxLayout()
    self.twitch_indicator = QLabel()
    self.twitch_indicator.setFixedSize(12, 12)
    self.update_twitch_indicator(False)
    twitch_label = QLabel("TWITCH CONNECTED")
    twitch_label.setStyleSheet("QLabel { color: #999999; font-size: 11px; background: transparent; border: none; }")
    twitch_status.addWidget(self.twitch_indicator)
    twitch_status.addWidget(twitch_label)
    twitch_status.addStretch()
    
    status_layout.addLayout(monitoring_status)
    status_layout.addLayout(api_status)
    status_layout.addLayout(twitch_status)
    
    sidebar_layout.addWidget(status_container)
    self.start_button = QPushButton("START MONITORING")
    self.start_button.setIcon(QIcon(resource_path("start_icon.png")))
    self.start_button.clicked.connect(self.toggle_monitoring)
    self.start_button.setStyleSheet(
        "QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #3a3a3a, stop:1 #202020); color: white; border: none; "
        "border-radius: 4px; padding: 10px; font-weight: bold; font-size: 12px; "
        "margin: 5px 10px; }"
        "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #4a4a4a, stop:1 #303030); }"
        "QPushButton:pressed { background: #202020; }"
    )
    sidebar_layout.addWidget(self.start_button)
    self.rescan_button = QPushButton("FIND MISSED KILLS")
    self.rescan_button.setIcon(QIcon(resource_path("search_icon.png")))
    self.rescan_button.clicked.connect(self.on_rescan_button_clicked)
    self.rescan_button.setEnabled(False)
    self.rescan_button.setToolTip("You must start monitoring first before searching for missed kills")
    self.rescan_button.setStyleSheet(
        "QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #3a3a3a, stop:1 #202020); color: white; border: none; "
        "border-radius: 4px; padding: 10px; font-weight: bold; font-size: 12px; "
        "margin: 5px 10px; }"
        "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #4a4a4a, stop:1 #303030); }"
        "QPushButton:pressed { background: #202020; }"
        "QPushButton:disabled { background: #222222; color: #666666; }"
    )
    sidebar_layout.addWidget(self.rescan_button)
    separator = QWidget()
    separator.setFixedHeight(1)
    separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    separator.setStyleSheet("background-color: #2a2a2a; margin: 10px 15px;")
    sidebar_layout.addWidget(separator)
    self.nav_buttons = []
    killfeed_btn = self.create_nav_button("Killfeed", "dashboard")
    killfeed_btn.setCheckable(True)
    killfeed_btn.setChecked(True)
    self.nav_buttons.append(killfeed_btn)
    sidebar_layout.addWidget(killfeed_btn)
    killfeed_settings_btn = self.create_nav_button("Killfeed Settings", "killfeed_tab")
    killfeed_settings_btn.setCheckable(True)
    self.nav_buttons.append(killfeed_settings_btn)
    sidebar_layout.addWidget(killfeed_settings_btn)
    api_btn = self.create_nav_button("API Settings", "api_tab") 
    api_btn.setCheckable(True)
    self.nav_buttons.append(api_btn)
    sidebar_layout.addWidget(api_btn)
    sound_btn = self.create_nav_button("Sound Settings", "sound_tab")
    sound_btn.setCheckable(True)
    self.nav_buttons.append(sound_btn)
    sidebar_layout.addWidget(sound_btn)
    twitch_btn = self.create_nav_button("Twitch Integration", "twitch_tab")
    twitch_btn.setCheckable(True)
    self.nav_buttons.append(twitch_btn)
    sidebar_layout.addWidget(twitch_btn)
    sidebar_layout.addStretch(1)
    main_layout.addWidget(sidebar)

    content_area = QWidget()
    content_area.setStyleSheet(
        "QWidget { background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
        "stop:0 #1a1a1a, stop:1 #0d0d0d); "
        "border-top-left-radius: 0px; border-bottom-left-radius: 0px; "
        "border-top-right-radius: 10px; border-bottom-right-radius: 10px; }"
    )
    content_layout = QVBoxLayout(content_area)
    content_layout.setContentsMargins(15, 15, 15, 15)
    content_layout.setSpacing(15)

    self.stats_panel = QWidget()
    self.stats_panel.setStyleSheet(
        "QWidget { background-color: rgba(20, 20, 20, 0.8); border-radius: 8px; "
        "border: 1px solid #333333; }"
    )
    stats_layout = QHBoxLayout(self.stats_panel)
    stats_layout.setContentsMargins(15, 15, 15, 15)
    stats_layout.setSpacing(20)
    
    kill_stats = self.create_stat_card("KILLS", "0", "#66ff66")
    death_stats = self.create_stat_card("DEATHS", "0", "#f04747")
    kd_stats = self.create_stat_card("K/D RATIO", "--", "#00ccff")
    session_stats = self.create_stat_card("SESSION TIME", "00:00", "#ffffff")
    
    self.kill_count_display = kill_stats.findChild(QLabel, "stat_value")
    self.death_count_display = death_stats.findChild(QLabel, "stat_value")
    self.kd_ratio_display = kd_stats.findChild(QLabel, "stat_value")
    self.session_time_display = session_stats.findChild(QLabel, "stat_value")
    
    stats_layout.addWidget(kill_stats)
    stats_layout.addWidget(death_stats)
    stats_layout.addWidget(kd_stats)
    stats_layout.addWidget(session_stats)
    
    content_layout.addWidget(self.stats_panel)
    self.content_stack = QStackedWidget()
    killfeed_page = QWidget()
    killfeed_layout = QVBoxLayout(killfeed_page)
    killfeed_layout.setContentsMargins(0, 0, 0, 0)
    killfeed_layout.setSpacing(15)

    kill_feed_container = QWidget()
    kill_feed_container.setStyleSheet(
        "QWidget { background-color: rgba(20, 20, 20, 0.8); border-radius: 8px; "
        "border: 1px solid #333333; }"
    )
    kill_feed_layout = QVBoxLayout(kill_feed_container)
    kill_feed_layout.setContentsMargins(15, 15, 15, 15)
    kill_feed_layout.setSpacing(10)
    
    kill_feed_header = QLabel("KILL FEED")
    kill_feed_header.setStyleSheet(
        "QLabel { color: #f0f0f0; font-size: 14px; font-weight: bold; "
        "background: transparent; border: none; }"
    )
    kill_feed_layout.addWidget(kill_feed_header)
    
    self.kill_display = QTextBrowser()
    self.kill_display.setReadOnly(True)
    self.kill_display.setOpenExternalLinks(True)
    self.kill_display.setStyleSheet(
        "QTextBrowser { background-color: #121212; border: 1px solid #2a2a2a; border-radius: 8px; padding: 10px; }"
        "QTextBrowser QScrollBar:vertical { background: #1a1a1a; width: 12px; margin: 0px; }"
        "QTextBrowser QScrollBar::handle:vertical { background: #2a2a2a; min-height: 20px; border-radius: 6px; }"
        "QTextBrowser QScrollBar::handle:vertical:hover { background: #f04747; }"
        "QTextBrowser QScrollBar::add-line:vertical, QTextBrowser QScrollBar::sub-line:vertical { height: 0px; }"
        "QTextBrowser QScrollBar::add-page:vertical, QTextBrowser QScrollBar::sub-page:vertical { background: none; }"
    )
    kill_feed_layout.addWidget(self.kill_display)
    
    killfeed_layout.addWidget(kill_feed_container, 1)

    killfeed_settings_page = QWidget()
    killfeed_settings_layout = QVBoxLayout(killfeed_settings_page)
    killfeed_settings_layout.setContentsMargins(0, 0, 0, 0)
    killfeed_settings_layout.setSpacing(15)

    game_card = QWidget()
    game_card.setStyleSheet(
        "QWidget { background-color: rgba(20, 20, 20, 0.8); border-radius: 8px; "
        "border: 1px solid #333333; }"
    )
    game_card_layout = QFormLayout(game_card)
    game_card_layout.setContentsMargins(20, 20, 20, 20)
    game_card_layout.setSpacing(15)
    game_card_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
    
    game_header = QLabel("GAME CONFIGURATION")
    game_header.setStyleSheet(
        "QLabel { color: #f0f0f0; font-size: 18px; font-weight: bold; background: transparent; border: none; }"
    )
    game_card_layout.addRow(game_header)
    
    game_desc = QLabel("Configure Star Citizen-specific settings to track your gameplay.")
    game_desc.setStyleSheet(
        "QLabel { color: #cccccc; font-size: 13px; background: transparent; border: none; }"
    )
    game_desc.setWordWrap(True)
    game_card_layout.addRow(game_desc)
    
    log_path_label = QLabel("Game.log Path:")
    log_path_label.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; background: transparent; border: none; font-size: 14px; }")
    
    log_path_container = QWidget()
    log_path_container.setStyleSheet("background: transparent; border: none;")
    log_path_layout = QHBoxLayout(log_path_container)
    log_path_layout.setContentsMargins(0, 0, 0, 0)
    log_path_layout.setSpacing(10)
    
    self.log_path_input = QLineEdit()
    self.log_path_input.setPlaceholderText("Enter path to your Game.log")
    self.log_path_input.setStyleSheet(
        "QLineEdit { background-color: #1e1e1e; color: #f0f0f0; padding: 12px; "
        "border: 1px solid #2a2a2a; border-radius: 4px; font-size: 14px; }"
        "QLineEdit:hover, QLineEdit:focus { border-color: #f04747; }"
    )
    
    browse_log_btn = QPushButton("Browse")
    browse_log_btn.setIcon(QIcon(resource_path("browse_icon.png")))
    browse_log_btn.setStyleSheet(
        "QPushButton { background-color: #1e1e1e; color: #f0f0f0; "
        "border: 1px solid #2a2a2a; border-radius: 4px; padding: 12px; }"
        "QPushButton:hover { border-color: #f04747; background-color: #2a2a2a; }"
    )
    browse_log_btn.setFixedWidth(120)
    browse_log_btn.clicked.connect(self.browse_file)
    
    log_path_layout.addWidget(self.log_path_input)
    log_path_layout.addWidget(browse_log_btn)
    
    game_card_layout.addRow(log_path_label, log_path_container)

    log_help = QLabel("This should be the path to your Star Citizen Game.log file, typically located in the "
                    "StarCitizen\\LIVE\\game.log directory.")
    log_help.setStyleSheet("QLabel { color: #aaaaaa; font-style: italic; background: transparent; border: none; }")
    log_help.setWordWrap(True)
    game_card_layout.addRow("", log_help)
    
    ship_label = QLabel("Killer Ship:")
    ship_label.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; background: transparent; border: none; font-size: 14px; }")
    
    self.ship_combo = QComboBox()
    self.ship_combo.setEditable(True)
    self.load_ship_options()
    self.ship_combo.currentTextChanged.connect(self.on_ship_combo_changed)
    self.ship_combo.setStyleSheet(
        "QComboBox { background-color: #1e1e1e; color: #f0f0f0; padding: 12px; "
        "border: 1px solid #2a2a2a; border-radius: 4px; padding-right: 20px; font-size: 14px; }"
        "QComboBox:hover { border-color: #f04747; }"
        "QComboBox::drop-down { border: none; width: 20px; }"
        "QComboBox::down-arrow { width: 0; height: 0; border-left: 5px solid transparent; "
        "   border-right: 5px solid transparent; border-top: 5px solid #f04747; margin-right: 8px; }"
        "QComboBox QAbstractItemView { background-color: #1e1e1e; color: #f0f0f0; "
        "selection-background-color: #f04747; selection-color: white; border: 1px solid #2a2a2a; }"
    )
    self.ship_combo.setMinimumWidth(300)
    
    game_card_layout.addRow(ship_label, self.ship_combo)

    ship_help = QLabel("Select or enter the ship you are currently using. This information will be included with your kill data.")
    ship_help.setStyleSheet("QLabel { color: #aaaaaa; font-style: italic; background: transparent; border: none; }")
    ship_help.setWordWrap(True)
    game_card_layout.addRow("", ship_help)
    
    killfeed_settings_layout.addWidget(game_card)

    export_card = QWidget()
    export_card.setStyleSheet(
        "QWidget { background-color: rgba(20, 20, 20, 0.8); border-radius: 8px; "
        "border: 1px solid #333333; }"
    )
    export_layout = QVBoxLayout(export_card)
    export_layout.setContentsMargins(20, 20, 20, 20)
    export_layout.setSpacing(15)
    
    export_header = QLabel("EXPORT KILL LOGS")
    export_header.setStyleSheet(
        "QLabel { color: #f0f0f0; font-size: 18px; font-weight: bold; background: transparent; border: none; }"
    )
    export_layout.addWidget(export_header)
    
    export_desc = QLabel("Export your kill and death logs as an HTML file. This includes all kills and deaths "
                        "recorded during your current session.")
    export_desc.setStyleSheet(
        "QLabel { color: #cccccc; font-size: 13px; background: transparent; border: none; }"
    )
    export_desc.setWordWrap(True)
    export_layout.addWidget(export_desc)
    
    self.export_button = QPushButton("EXPORT LOGS")
    self.export_button.setIcon(QIcon(resource_path("export_icon.png")))
    self.export_button.clicked.connect(self.export_logs)
    self.export_button.setStyleSheet(
        "QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #3a3a3a, stop:1 #202020); color: white; border: none; "
        "border-radius: 4px; padding: 10px 16px; font-weight: bold; font-size: 13px; }"
        "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #4a4a4a, stop:1 #303030); }"
        "QPushButton:pressed { background: #202020; }"
    )
    self.export_button.setMaximumWidth(250)
    export_button_layout = QHBoxLayout()
    export_button_layout.addStretch()
    export_button_layout.addWidget(self.export_button)
    export_layout.addLayout(export_button_layout)
    
    killfeed_settings_layout.addWidget(export_card)

    files_card = QWidget()
    files_card.setStyleSheet(
        "QWidget { background-color: rgba(20, 20, 20, 0.8); border-radius: 8px; "
        "border: 1px solid #333333; }"
    )
    files_layout = QVBoxLayout(files_card)
    files_layout.setContentsMargins(20, 20, 20, 20)
    files_layout.setSpacing(15)
    
    files_header = QLabel("APPLICATION FILES")
    files_header.setStyleSheet(
        "QLabel { color: #f0f0f0; font-size: 18px; font-weight: bold; background: transparent; border: none; }"
    )
    files_layout.addWidget(files_header)
    
    files_desc = QLabel("Access the application's data files including configuration files, logs, and saved kill records. "
                      "This is useful for troubleshooting or backing up your data.")
    files_desc.setStyleSheet(
        "QLabel { color: #cccccc; font-size: 13px; background: transparent; border: none; }"
    )
    files_desc.setWordWrap(True)
    files_layout.addWidget(files_desc)
    
    self.files_button = QPushButton("OPEN SCTOOL FILES")
    self.files_button.setIcon(QIcon(resource_path("files_icon.png")))
    self.files_button.clicked.connect(self.open_tracker_files)
    self.files_button.setStyleSheet(
        "QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #3a3a3a, stop:1 #202020); color: white; border: none; "
        "border-radius: 4px; padding: 10px 16px; font-weight: bold; font-size: 13px; }"
        "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #4a4a4a, stop:1 #303030); }"
        "QPushButton:pressed { background: #202020; }"
    )
    self.files_button.setMaximumWidth(250)
    files_button_layout = QHBoxLayout()
    files_button_layout.addStretch()
    files_button_layout.addWidget(self.files_button)
    files_layout.addLayout(files_button_layout)
    
    killfeed_settings_layout.addWidget(files_card)

    app_settings_card = QWidget()
    app_settings_card.setStyleSheet(
        "QWidget { background-color: rgba(20, 20, 20, 0.8); border-radius: 8px; "
        "border: 1px solid #333333; }"
    )
    app_settings_layout = QVBoxLayout(app_settings_card)
    app_settings_layout.setContentsMargins(20, 20, 20, 20)
    app_settings_layout.setSpacing(20)
    
    app_settings_header = QLabel("APPLICATION SETTINGS")
    app_settings_header.setStyleSheet(
        "QLabel { color: #f0f0f0; font-size: 18px; font-weight: bold; background: transparent; border: none; }"
    )
    app_settings_layout.addWidget(app_settings_header)

    tray_container = QWidget()
    tray_container.setStyleSheet("background: transparent; border: none;")
    tray_layout = QVBoxLayout(tray_container)
    tray_layout.setContentsMargins(0, 0, 0, 0)
    tray_layout.setSpacing(10)
    
    self.minimize_to_tray_checkbox = QCheckBox("Minimize to system tray")
    self.minimize_to_tray_checkbox.setChecked(self.minimize_to_tray)
    self.minimize_to_tray_checkbox.stateChanged.connect(self.on_minimize_to_tray_changed)
    self.minimize_to_tray_checkbox.setStyleSheet(
        "QCheckBox { color: #ffffff; spacing: 10px; background: transparent; border: none; font-size: 14px; }"
        "QCheckBox::indicator { width: 20px; height: 20px; }"
        "QCheckBox::indicator:unchecked { border: 1px solid #2a2a2a; background-color: #1e1e1e; border-radius: 3px; }"
        "QCheckBox::indicator:checked { border: 1px solid #f04747; background-color: #f04747; border-radius: 3px; }"
    )
    tray_layout.addWidget(self.minimize_to_tray_checkbox)
    
    tray_desc = QLabel("When minimized, the application will hide in the system tray instead of the taskbar.")
    tray_desc.setStyleSheet(
        "QLabel { color: #999999; font-size: 12px; background: transparent; border: none; }"
    )
    tray_desc.setWordWrap(True)
    tray_layout.addWidget(tray_desc)
    
    app_settings_layout.addWidget(tray_container)
    
    autostart_container = QWidget()
    autostart_container.setStyleSheet("background: transparent; border: none;")
    autostart_layout = QVBoxLayout(autostart_container)
    autostart_layout.setContentsMargins(0, 0, 0, 0)
    autostart_layout.setSpacing(10)
    
    self.start_with_system_checkbox = QCheckBox("Start with Windows")
    self.start_with_system_checkbox.setChecked(self.start_with_system)
    self.start_with_system_checkbox.stateChanged.connect(self.on_start_with_system_changed)
    self.start_with_system_checkbox.setStyleSheet(
        "QCheckBox { color: #ffffff; spacing: 10px; background: transparent; border: none; font-size: 14px; }"
        "QCheckBox::indicator { width: 20px; height: 20px; }"
        "QCheckBox::indicator:unchecked { border: 1px solid #2a2a2a; background-color: #1e1e1e; border-radius: 3px; }"
        "QCheckBox::indicator:checked { border: 1px solid #f04747; background-color: #f04747; border-radius: 3px; }"
    )
    autostart_layout.addWidget(self.start_with_system_checkbox)
    
    autostart_desc = QLabel("Launch SCTool Tracker automatically when your computer starts.")
    autostart_desc.setStyleSheet(
        "QLabel { color: #999999; font-size: 12px; background: transparent; border: none; }"
    )
    autostart_desc.setWordWrap(True)
    autostart_layout.addWidget(autostart_desc)
    
    app_settings_layout.addWidget(autostart_container)
    
    killfeed_settings_layout.addWidget(app_settings_card)
    killfeed_settings_layout.addStretch(1)
    api_page = QWidget()
    api_layout = QVBoxLayout(api_page)
    api_layout.setContentsMargins(0, 0, 0, 0)
    api_layout.setSpacing(15)
    
    api_card = QWidget()
    api_card.setStyleSheet(
        "QWidget { background-color: rgba(20, 20, 20, 0.8); border-radius: 8px; "
        "border: 1px solid #333333; }"
    )
    api_card_layout = QFormLayout(api_card)
    api_card_layout.setContentsMargins(20, 20, 20, 20)
    api_card_layout.setSpacing(15)
    api_card_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
    
    api_header = QLabel("API CONNECTION")
    api_header.setStyleSheet(
        "QLabel { color: #f0f0f0; font-size: 18px; font-weight: bold; background: transparent; border: none; }"
    )
    api_card_layout.addRow(api_header)
    
    api_desc = QLabel("Connect to the SCTool online service to track your kill statistics across sessions and compare with other players.")
    api_desc.setStyleSheet(
        "QLabel { color: #cccccc; font-size: 13px; background: transparent; border: none; }"
    )
    api_desc.setWordWrap(True)
    api_card_layout.addRow(api_desc)
    
    self.send_to_api_checkbox = QCheckBox("Send Kills to API")
    self.send_to_api_checkbox.setChecked(True)
    self.send_to_api_checkbox.setStyleSheet(
        "QCheckBox { color: #ffffff; spacing: 10px; background: transparent; border: none; font-size: 14px; }"
        "QCheckBox::indicator { width: 20px; height: 20px; }"
        "QCheckBox::indicator:unchecked { border: 1px solid #2a2a2a; background-color: #1e1e1e; border-radius: 3px; }"
        "QCheckBox::indicator:checked { border: 1px solid #f04747; background-color: #f04747; border-radius: 3px; }"
    )
    api_card_layout.addRow("", self.send_to_api_checkbox)
    
    api_key_label = QLabel("API Key:")
    api_key_label.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; background: transparent; border: none; }")
    self.api_key_input = QLineEdit()
    self.api_key_input.setPlaceholderText("Enter your API key here")
    self.api_key_input.setStyleSheet(
        "QLineEdit { background-color: #1e1e1e; color: #f0f0f0; padding: 12px; "
        "border: 1px solid #2a2a2a; border-radius: 4px; font-size: 14px; }"
        "QLineEdit:hover, QLineEdit:focus { border-color: #f04747; }"
    )
    self.api_key_input.setMinimumWidth(300)
    api_card_layout.addRow(api_key_label, self.api_key_input)
    
    api_help = QLabel("Your API key connects your account to the SCTool Tracker service. "
                    "Visit starcitizentool.com to register and get your API key.")
    api_help.setStyleSheet("QLabel { color: #aaaaaa; font-style: italic; background: transparent; border: none; }")
    api_help.setWordWrap(True)
    api_card_layout.addRow("", api_help)
    
    api_layout.addWidget(api_card)
    api_layout.addStretch(1)
    
    # === SOUND SETTINGS PAGE ===
    sound_page = QWidget()
    sound_layout = QVBoxLayout(sound_page)
    sound_layout.setContentsMargins(0, 0, 0, 0)
    sound_layout.setSpacing(15)
    
    sound_card = QWidget()
    sound_card.setStyleSheet(
        "QWidget { background-color: rgba(20, 20, 20, 0.8); border-radius: 8px; "
        "border: 1px solid #333333; }"
    )
    sound_card_layout = QFormLayout(sound_card)
    sound_card_layout.setContentsMargins(20, 20, 20, 20)
    sound_card_layout.setSpacing(15)
    sound_card_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
    
    sound_header = QLabel("SOUND OPTIONS")
    sound_header.setStyleSheet(
        "QLabel { color: #f0f0f0; font-size: 18px; font-weight: bold; background: transparent; border: none; }"
    )
    sound_card_layout.addRow(sound_header)
    
    sound_desc = QLabel("Configure sound notifications for when you get kills in Star Citizen.")
    sound_desc.setStyleSheet(
        "QLabel { color: #cccccc; font-size: 13px; background: transparent; border: none; }"
    )
    sound_desc.setWordWrap(True)
    sound_card_layout.addRow(sound_desc)
    
    self.kill_sound_checkbox = QCheckBox("Enable Kill Sound")
    self.kill_sound_checkbox.setChecked(False)
    self.kill_sound_checkbox.stateChanged.connect(self.on_kill_sound_toggled)
    self.kill_sound_checkbox.setStyleSheet(
        "QCheckBox { color: #ffffff; spacing: 10px; background: transparent; border: none; font-size: 14px; }"
        "QCheckBox::indicator { width: 20px; height: 20px; }"
        "QCheckBox::indicator:unchecked { border: 1px solid #2a2a2a; background-color: #1e1e1e; border-radius: 3px; }"
        "QCheckBox::indicator:checked { border: 1px solid #f04747; background-color: #f04747; border-radius: 3px; }"
    )
    sound_card_layout.addRow("", self.kill_sound_checkbox)
    
    sound_path_label = QLabel("Kill Sound File:")
    sound_path_label.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; background: transparent; border: none; font-size: 14px; }")
    
    sound_path_container = QWidget()
    sound_path_container.setStyleSheet("background: transparent; border: none;")
    sound_path_layout = QHBoxLayout(sound_path_container)
    sound_path_layout.setContentsMargins(0, 0, 0, 0)
    sound_path_layout.setSpacing(10)
    
    self.kill_sound_path_input = QLineEdit()
    self.kill_sound_path_input.setText(self.kill_sound_path)
    self.kill_sound_path_input.setStyleSheet(
        "QLineEdit { background-color: #1e1e1e; color: #f0f0f0; padding: 12px; "
        "border: 1px solid #2a2a2a; border-radius: 4px; font-size: 14px; }"
        "QLineEdit:hover, QLineEdit:focus { border-color: #f04747; }"
    )
    
    sound_browse_btn = QPushButton("Browse")
    sound_browse_btn.setStyleSheet(
        "QPushButton { background-color: #1e1e1e; color: #f0f0f0; "
        "border: 1px solid #2a2a2a; border-radius: 4px; padding: 12px; }"
        "QPushButton:hover { border-color: #f04747; background-color: #2a2a2a; }"
    )
    sound_browse_btn.setFixedWidth(120)
    sound_browse_btn.clicked.connect(self.on_kill_sound_file_browse)
    
    sound_path_layout.addWidget(self.kill_sound_path_input)
    sound_path_layout.addWidget(sound_browse_btn)
    
    sound_card_layout.addRow(sound_path_label, sound_path_container)
    
    volume_label = QLabel("Volume:")
    volume_label.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; background: transparent; border: none; font-size: 14px; }")
    
    volume_container = QWidget()
    volume_container.setStyleSheet("background: transparent; border: none;")
    volume_layout = QVBoxLayout(volume_container)
    volume_layout.setContentsMargins(0, 0, 0, 0)
    volume_layout.setSpacing(10)
    
    self.volume_slider = QSlider(Qt.Horizontal)
    self.volume_slider.setRange(0, 100)
    self.volume_slider.setValue(self.kill_sound_volume)
    self.volume_slider.valueChanged.connect(self.on_kill_sound_volume_changed)
    self.volume_slider.setStyleSheet(
        "QSlider::groove:horizontal { border: 1px solid #2a2a2a; height: 10px; "
        "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1a1a1a, stop:1 #2a2a2a); "
        "margin: 2px 0; border-radius: 5px; }"
        "QSlider::handle:horizontal { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #f04747, stop:1 #d03737); border: 1px solid #2a2a2a; "
        "width: 20px; height: 20px; margin: -6px 0; border-radius: 10px; }"
        "QSlider::sub-page:horizontal { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
        "stop:0 #d03737, stop:1 #f04747); border-radius: 5px; }"
        "QSlider::handle:horizontal:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #ff5757, stop:1 #e04747); border: 1px solid #f04747; }"
    )
    volume_layout.addWidget(self.volume_slider)

    self.volume_percentage = QLabel(f"{self.kill_sound_volume}%")
    self.volume_percentage.setAlignment(Qt.AlignCenter)
    self.volume_percentage.setStyleSheet("QLabel { color: #f0f0f0; background: transparent; border: none; }")
    volume_layout.addWidget(self.volume_percentage)

    self.volume_slider.valueChanged.connect(lambda value: self.volume_percentage.setText(f"{value}%"))
    
    sound_card_layout.addRow(volume_label, volume_container)
    sound_layout.addWidget(sound_card)
    sound_layout.addStretch(1)
    
    twitch_page = QWidget()
    twitch_layout = QVBoxLayout(twitch_page)
    twitch_layout.setContentsMargins(0, 0, 0, 0)
    twitch_layout.setSpacing(15)
    
    twitch_card = QWidget()
    twitch_card.setStyleSheet(
        "QWidget { background-color: rgba(20, 20, 20, 0.8); border-radius: 8px; "
        "border: 1px solid #333333; }"
    )
    twitch_card_layout = QFormLayout(twitch_card)
    twitch_card_layout.setContentsMargins(20, 20, 20, 20)
    twitch_card_layout.setSpacing(15)
    twitch_card_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
    
    twitch_header = QLabel("TWITCH INTEGRATION")
    twitch_header.setStyleSheet(
        "QLabel { color: #9146FF; font-size: 18px; font-weight: bold; background: transparent; border: none; }"
    )
    twitch_card_layout.addRow(twitch_header)
    
    twitch_desc = QLabel("Connect your Twitch account to automatically create clips of your kills during your stream.")
    twitch_desc.setStyleSheet(
        "QLabel { color: #cccccc; font-size: 13px; background: transparent; border: none; }"
    )
    twitch_desc.setWordWrap(True)
    twitch_card_layout.addRow(twitch_desc)
    
    self.twitch_enabled_checkbox = QCheckBox("Enable Twitch Integration")
    self.twitch_enabled_checkbox.setChecked(False)
    self.twitch_enabled_checkbox.setStyleSheet(
        "QCheckBox { color: #ffffff; spacing: 10px; background: transparent; border: none; font-size: 14px; }"
        "QCheckBox::indicator { width: 20px; height: 20px; }"
        "QCheckBox::indicator:unchecked { border: 1px solid #2a2a2a; background-color: #1e1e1e; border-radius: 3px; }"
        "QCheckBox::indicator:checked { border: 1px solid #9146FF; background-color: #9146FF; border-radius: 3px; }"
    )
    twitch_card_layout.addRow("", self.twitch_enabled_checkbox)
    
    twitch_channel_label = QLabel("Twitch Channel:")
    twitch_channel_label.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; background: transparent; border: none; font-size: 14px; }")
    
    self.twitch_channel_input = QLineEdit()
    self.twitch_channel_input.setPlaceholderText("Enter your Twitch channel name")
    self.twitch_channel_input.setStyleSheet(
        "QLineEdit { background-color: #1e1e1e; color: #f0f0f0; padding: 12px; "
        "border: 1px solid #2a2a2a; border-radius: 4px; font-size: 14px; }"
        "QLineEdit:hover, QLineEdit:focus { border-color: #9146FF; }"
    )
    self.twitch_channel_input.setMinimumWidth(300)
    
    twitch_card_layout.addRow(twitch_channel_label, self.twitch_channel_input)
    
    twitch_buttons = QWidget()
    twitch_buttons.setStyleSheet("background: transparent; border: none;")
    twitch_buttons_layout = QHBoxLayout(twitch_buttons)
    twitch_buttons_layout.setContentsMargins(0, 0, 0, 0)
    twitch_buttons_layout.setSpacing(10)
    
    self.twitch_connect_button = QPushButton("Connect Twitch")
    self.twitch_connect_button.clicked.connect(self.connect_to_twitch)
    self.twitch_connect_button.setStyleSheet(
        "QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #9146FF, stop:1 #7a33e5); color: white; border: none; "
        "border-radius: 4px; padding: 12px; font-weight: bold; }"
        "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #a366ff, stop:1 #8a3bff); }"
        "QPushButton:pressed { background: #7a33e5; }"
    )
    
    self.twitch_disconnect_button = QPushButton("Disconnect Twitch")
    self.twitch_disconnect_button.clicked.connect(self.disconnect_from_twitch)
    self.twitch_disconnect_button.setStyleSheet(
        "QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #3a3a3a, stop:1 #202020); color: white; border: none; "
        "border-radius: 4px; padding: 12px; font-weight: bold; }"
        "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #4a4a4a, stop:1 #303030); }"
        "QPushButton:pressed { background: #202020; }"
    )
    
    twitch_buttons_layout.addWidget(self.twitch_connect_button)
    twitch_buttons_layout.addWidget(self.twitch_disconnect_button)
    twitch_buttons_layout.addStretch()
    
    twitch_card_layout.addRow("", twitch_buttons)
    clip_section_label = QLabel("CLIP SETTINGS")
    clip_section_label.setStyleSheet(
        "QLabel { color: #9146FF; font-size: 16px; font-weight: bold; background: transparent; border: none; margin-top: 10px; }"
    )
    twitch_card_layout.addRow(clip_section_label)
    
    self.clip_creation_checkbox = QCheckBox("Create clips when getting a kill")
    self.clip_creation_checkbox.setChecked(True)
    self.clip_creation_checkbox.setStyleSheet(
        "QCheckBox { color: #ffffff; spacing: 10px; background: transparent; border: none; font-size: 14px; }"
        "QCheckBox::indicator { width: 20px; height: 20px; }"
        "QCheckBox::indicator:unchecked { border: 1px solid #2a2a2a; background-color: #1e1e1e; border-radius: 3px; }"
        "QCheckBox::indicator:checked { border: 1px solid #9146FF; background-color: #9146FF; border-radius: 3px; }"
    )
    self.clip_creation_checkbox.stateChanged.connect(self.on_clip_creation_toggled)
    twitch_card_layout.addRow("", self.clip_creation_checkbox)
    
    self.chat_posting_checkbox = QCheckBox("Post kills to Twitch chat")
    self.chat_posting_checkbox.setChecked(True)
    self.chat_posting_checkbox.stateChanged.connect(self.on_chat_posting_toggled)
    self.chat_posting_checkbox.setStyleSheet(
        "QCheckBox { color: #ffffff; spacing: 10px; background: transparent; border: none; font-size: 14px; }"
        "QCheckBox::indicator { width: 20px; height: 20px; }"
        "QCheckBox::indicator:unchecked { border: 1px solid #2a2a2a; background-color: #1e1e1e; border-radius: 3px; }"
        "QCheckBox::indicator:checked { border: 1px solid #9146FF; background-color: #9146FF; border-radius: 3px; }"
    )
    twitch_card_layout.addRow("", self.chat_posting_checkbox)
    
    clip_delay_label = QLabel("Delay after kill:")
    clip_delay_label.setStyleSheet("QLabel { color: #ffffff; font-weight: bold; background: transparent; border: none; font-size: 14px; }")
    
    clip_delay_container = QWidget()
    clip_delay_container.setStyleSheet("background: transparent; border: none;")
    clip_delay_layout = QHBoxLayout(clip_delay_container)
    clip_delay_layout.setContentsMargins(0, 0, 0, 0)
    clip_delay_layout.setSpacing(10)
    
    self.clip_delay_slider = QSlider(Qt.Horizontal)
    self.clip_delay_slider.setRange(0, 60)
    self.clip_delay_slider.setValue(self.twitch.clip_delay_seconds)
    self.clip_delay_slider.setStyleSheet(
        "QSlider::groove:horizontal { border: 1px solid #2a2a2a; height: 10px; "
        "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1a1a1a, stop:1 #2a2a2a); "
        "margin: 2px 0; border-radius: 5px; }"
        "QSlider::handle:horizontal { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #9146FF, stop:1 #7a33e5); border: 1px solid #2a2a2a; "
        "width: 20px; height: 20px; margin: -6px 0; border-radius: 10px; }"
        "QSlider::sub-page:horizontal { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
        "stop:0 #7a33e5, stop:1 #9146FF); border-radius: 5px; }"
        "QSlider::handle:horizontal:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 #a366ff, stop:1 #8a3bff); border: 1px solid #9146FF; }"
    )
    
    self.clip_delay_value = QLabel(f"{self.twitch.clip_delay_seconds} seconds")
    self.clip_delay_value.setStyleSheet("QLabel { color: #ffffff; background: transparent; border: none; font-size: 14px; }")
    self.clip_delay_slider.valueChanged.connect(self.on_clip_delay_changed)
    
    clip_delay_layout.addWidget(self.clip_delay_slider)
    clip_delay_layout.addWidget(self.clip_delay_value)
    
    twitch_card_layout.addRow(clip_delay_label, clip_delay_container)
    
    note_label = QLabel("Note: Clip creation requires you to be actively streaming on Twitch")
    note_label.setStyleSheet("QLabel { color: #aaaaaa; font-style: italic; background: transparent; border: none; }")
    note_label.setWordWrap(True)
    twitch_card_layout.addRow("", note_label)
    
    twitch_layout.addWidget(twitch_card)
    twitch_layout.addStretch(1)
    
    self.content_stack.addWidget(killfeed_page)
    self.content_stack.addWidget(killfeed_settings_page)
    self.content_stack.addWidget(api_page)
    self.content_stack.addWidget(sound_page)
    self.content_stack.addWidget(twitch_page)
    self.content_stack.setCurrentIndex(0)
    
    for i, button in enumerate(self.nav_buttons):
        button.clicked.connect(lambda checked, index=i: self.switch_page(index))
    
    content_layout.addWidget(self.content_stack)
    
    main_layout.addWidget(content_area, stretch=1)
    main_widget.setLayout(main_layout)
    self.setCentralWidget(main_widget)
    self.setMinimumSize(1000, 700)

    self.session_start_time = None
    self.session_timer = QTimer()
    self.session_timer.timeout.connect(self.update_session_time)
    
    self.send_to_api_checkbox.stateChanged.connect(self.update_api_status)
    self.twitch_enabled_checkbox.stateChanged.connect(self.on_twitch_enabled_changed)

def create_nav_button(self, text, obj_name=None):
    """Create a styled navigation button for the sidebar"""
    button = QPushButton(text)
    button.setStyleSheet(
        "QPushButton { text-align: left; padding: 12px 15px; font-weight: bold; color: #bbbbbb; "
        "background-color: transparent; border: none; border-left: 3px solid transparent; }"
        "QPushButton:hover { color: #ffffff; background-color: #222222; border-left: 3px solid #f04747; }"
        "QPushButton:checked { color: #ffffff; background-color: #252525; border-left: 3px solid #f04747; }"
    )
    if obj_name:
        button.setObjectName(obj_name)
    return button

def create_stat_card(self, label_text, value_text, value_color):
    """Create a styled stat card widget"""
    card = QWidget()
    card.setStyleSheet("border: none; background: #1a1a1a; border-radius: 8px;")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(5)
    
    value = QLabel(value_text)
    value.setObjectName("stat_value")
    value.setStyleSheet(
        f"QLabel {{ color: {value_color}; font-size: 24px; font-weight: bold; background: transparent; border: none; }}"
    )
    value.setAlignment(Qt.AlignCenter)
    
    label = QLabel(label_text)
    label.setStyleSheet(
        "QLabel { color: #aaaaaa; font-size: 12px; background: transparent; border: none; }"
    )
    label.setAlignment(Qt.AlignCenter)
    
    layout.addWidget(value)
    layout.addWidget(label)
    
    return card

def switch_page(self, index):
    """Switch to the specified page in the stacked widget"""
    self.content_stack.setCurrentIndex(index)

    for i, button in enumerate(self.nav_buttons):
        button.setChecked(i == index)

def load_config(self) -> None:
    """Load configuration from config file"""
    try:
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.api_key = config.get('api_key', '')
            self.api_key_input.setText(self.api_key)
            self.send_to_api_checkbox.setChecked(config.get('send_to_api', True))
            
            log_path = config.get('log_path', '')
            if log_path:
                self.log_path_input.setText(log_path)
            
            killer_ship = config.get('killer_ship', 'No Ship')
            if killer_ship != 'No Ship':
                index = self.ship_combo.findText(killer_ship)
                if index != -1:
                    self.ship_combo.setCurrentIndex(index)
                else:
                    self.ship_combo.addItem(killer_ship)
                    self.ship_combo.setCurrentIndex(self.ship_combo.count() - 1)
            
            self.kill_sound_enabled = config.get('kill_sound', False)
            self.kill_sound_checkbox.setChecked(self.kill_sound_enabled)
            
            kill_sound_path = config.get('kill_sound_path', '')
            if kill_sound_path and os.path.isfile(kill_sound_path):
                self.kill_sound_path = kill_sound_path
                self.kill_sound_path_input.setText(kill_sound_path)
            
            self.kill_sound_volume = config.get('kill_sound_volume', 100)
            self.volume_slider.setValue(self.kill_sound_volume)
            self.twitch_enabled = config.get('twitch_enabled', False)
            self.twitch_enabled_checkbox.setChecked(self.twitch_enabled)
            
            twitch_channel = config.get('twitch_channel', '')
            if twitch_channel:
                self.twitch_channel_input.setText(twitch_channel)
                self.twitch.set_broadcaster_name(twitch_channel)
                
            self.clip_creation_enabled = config.get('clip_creation_enabled', True)
            self.clip_creation_checkbox.setChecked(self.clip_creation_enabled)
            
            self.chat_posting_enabled = config.get('chat_posting_enabled', True)
            self.chat_posting_checkbox.setChecked(self.chat_posting_enabled)
            
            self.clips = config.get('clips', {})
            clip_delay = config.get('clip_delay_seconds', 0)
            self.twitch.set_clip_delay(clip_delay)
            self.clip_delay_slider.setValue(clip_delay)
            self.clip_delay_value.setText(f"{clip_delay} seconds")
            self.minimize_to_tray = config.get('minimize_to_tray', False)
            self.minimize_to_tray_checkbox.setChecked(self.minimize_to_tray)
            self.start_with_system = config.get('start_with_system', False)
            self.start_with_system_checkbox.setChecked(self.start_with_system)
            self.local_user_name = config.get('local_user_name', '')
            if self.local_user_name:
                self.user_display.setText(f"User: {self.local_user_name}")
                self.update_user_profile_image(self.local_user_name)
                self.rescan_button.setEnabled(True)
            
            if config.get('monitoring_active', False):
                QTimer.singleShot(500, self.toggle_monitoring)
                
            logging.info("Configuration loaded successfully")
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        
def load_local_kills(self) -> None:
    """Load locally saved kills from JSON file"""
    try:
        if os.path.isfile(self.kills_local_file):
            with open(self.kills_local_file, 'r', encoding='utf-8') as f:
                self.local_kills = json.load(f)
                
            logging.info(f"Loaded {len(self.local_kills)} previous kills from local storage")
    except Exception as e:
        logging.error(f"Failed to load local kills: {e}")
        self.local_kills = {}

def apply_styles(self) -> None:
    """Apply additional custom styles to the application"""
    app_style = """
        QMainWindow {
            background-color: #0d0d0d;
        }
        QToolTip {
            background-color: #1e1e1e;
            color: #f0f0f0;
            border: 1px solid #3a3a3a;
            padding: 5px;
            border-radius: 4px;
        }
    """
    self.setStyleSheet(app_style)
    self.setWindowOpacity(0.98)

class CollapsibleSettingsPanel(QWidget):
    """Legacy class for backwards compatibility"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
    def addWidget(self, widget):
        self.layout.addWidget(widget)