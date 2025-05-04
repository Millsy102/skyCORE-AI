# **SCTool Tracker**

## **Video instructions**

`https://www.youtube.com/watch?v=d8SwnmVPuGI`

## **Overview**

SCTool Tracker is an application for Star Citizen that monitors the game's log file to track and record player kills and deaths. This tool provides real-time notifications about combat events and sends this data to the SCTool API to maintain your combat statistics.

## **How It Works**

The tracker operates by:

1. **Log File Monitoring**: The application continuously reads the Star Citizen Game.log file to detect combat events.
2. **Event Parsing**: When a kill or death event is detected, it extracts relevant information such as attacker, victim, weapon, location, and timestamp.
3. **UI Display**: Combat events are displayed in the application with formatted panels showing detailed information about each event.
4. **API Integration**: Kill data can be sent to the starcitizentool.com API to track your statistics over time.
5. **Ship Detection**: The tracker can detect which ship you're using for accurate kill attribution.

## **Getting Started**

### **Requirements**
- Windows operating system
- Star Citizen installed
- Python 3.8+ (if running from source)
- PyQt5 (if running from source)
- BeautifulSoup4 (if running from source)
- Requests library (if running from source)

### **Installation**

1. Download the latest release from [starcitizentool.com/download-sctool](https://starcitizentool.com/download-sctool)
2. Extract the files to a location of your choice
3. Run the SCTool Tracker executable

### **Configuration**

1. **API Key**: Enter your API key from starcitizentool.com in the provided field
2. **Game.log Path**: Select your Star Citizen Game.log file location (typically in the game's LIVE folder)
3. **Sound Settings**: Configure optional sound notifications for kills
4. **Killer Ship**: Select or enter your current ship for proper attribution

## **Features**

- **Real-time Kill/Death Tracking**: Instantly see your combat events as they happen
- **API Integration**: Send your kills to the SCTool API for statistics tracking
- **Ship Detection**: Automatically detects your current ship
- **Kill Sound**: Optional sound notification when you get a kill
- **Missing Kill Detection**: Scan for kills that might have been missed
- **Game Mode Detection**: Identifies which game mode you're playing (PU, Arena Commander, etc.)
- **Session Statistics**: Track kills, deaths, and K/D ratio for your current session
- **Rescan Capability**: Search through your game logs to find kills that may have been missed
- **Export Functionality**: Save your combat logs as HTML for future reference
- **Auto-Updates**: Automatically download and install the latest version
- **System Tray Integration**: Minimize to system tray for unobtrusive operation
- **Twitch Integration**: Create clips and post kill messages to your Twitch chat
- **User Profile Images**: Display profile images fetched from RSI website

## **Technical Architecture**

The SCTool Tracker is built with a modular architecture consisting of several key components:

### **Core Components**

1. **Main Application (Kill_main.py)**: Entry point that initializes the GUI and monitoring systems
2. **GUI Interface (Kill_form.py)**: PyQt5-based interface that displays kill/death events and provides user controls
3. **Log Monitoring (Kill_thread.py)**: Background threads that monitor the game log file in real-time
4. **Event Parser (kill_parser.py)**: Specialized parser that extracts combat data from log entries
5. **Event Formatters (Registered_kill.py, Death_kill.py)**: Format extracted data into visual HTML displays
6. **Twitch Integration (twitch_integration.py)**: Handles Twitch authentication, chat messaging, and clip creation
7. **Utility Functions (utlity.py)**: Common utilities and helper functions for UI and configuration

### **Data Flow**

1. TailThread monitors the Game.log file for new entries
2. When a combat event is detected, the log line is parsed using regular expressions
3. Extracted data is formatted into HTML and displayed in the application
4. If API integration is enabled, the data is sent to the SCTool API
5. Local statistics are updated and displayed in the session panel
6. If Twitch integration is enabled, kill events can trigger clip creation and chat messages

### **File Structure**

- **Kill_main.py**: Main entry point of the application
- **Kill_form.py**: Main GUI implementation and application logic
- **Kill_thread.py**: Background monitoring threads and API communication
- **kill_parser.py**: Log parsing and data extraction utilities
- **Registered_kill.py**: Formats kill events for display
- **Death_kill.py**: Formats death events for display
- **twitch_integration.py**: Twitch API integration for clips and chat
- **fetch.py**: Functions for fetching profile data and images
- **utlity.py**: Utility functions and UI helpers
- **README.md**: Documentation

## **Log File Parsing Details**

Star Citizen logs combat events in a specific format that the tracker parses. The key patterns include:

### **Kill Events**

```
<timestamp> [Notice] <Actor Death> CActor::Kill: 'victim' [victim_geid] in zone 'zone' killed by 'attacker' [attacker_geid] using 'weapon' [...] with damage type 'damage_type' from direction x: X, y: Y, z: Z [...]
```

### **Ship Detection**

The tracker identifies the player's current ship through:

1. **Jump Drive Events**: When a player uses a quantum drive
2. **Interior Zone Changes**: When a player enters or exits a ship
3. **Manual Selection**: User can manually select their current ship

### **Game Mode Detection**

Game modes are detected through log entries following this pattern:

```
<timestamp> Loading GameModeRecord='game_mode' with EGameModeId='id'
```

## **Building Your Own Tracker**

If you want to build your own tracker that integrates with the SCTool API, follow these guidelines:

### **API Integration**

1. **Obtain an API Key**: Contact starcitizentool.com to get an API key
2. **API Endpoints**: 
   - Kills: `https://starcitizentool.com/api/v1/kills`
   - Deaths: `https://starcitizentool.com/api/v1/deaths`

### **Required Headers**

```
Content-Type: application/json
X-API-Key: YOUR_API_KEY
User-Agent: YOUR_APPLICATION_NAME
X-Client-ID: YOUR_CLIENT_ID
X-Client-Version: YOUR_VERSION
```

### **Payload Structure**

When sending a kill event to the API, your JSON payload should include:

```
{
  "log_line": "Raw log line from the game",
  "game_mode": "Game mode (PU, Elimination, etc.)",
  "killer_ship": "Ship used by the attacker (optional)",
  "method": "Vehicle destruction or Player destruction"
}
```

When sending a death event to the API, your JSON payload should include:

```
{
  "log_line": "Raw log line from the game",
  "game_mode": "Game mode (PU, Elimination, etc.)",
  "victim_name": "Name of the victim",
  "attacker_name": "Name of the attacker",
  "weapon": "Weapon used",
  "damage_type": "Type of damage",
  "location": "Location of death",
  "timestamp": "Timestamp of the death",
  "event_type": "death"
}
```

### **Development Setup**

1. Clone the repository or start a new Python project
2. Install required dependencies:
   ```
   pip install PyQt5 beautifulsoup4 requests packaging
   ```
3. Implement the core components: log monitoring, parsing, and API integration
4. Test with actual Star Citizen log files

## **Troubleshooting**

Common issues and solutions:

- **Ship Not Detected**: Manually select your ship in the Killer Ship dropdown
- **Kills Not Showing**: Verify the path to your Game.log file is correct
- **API Connection Fails**: Check your network connection and API key
- **Missed Kills**: Use the "Find Missed Kills" feature to scan for unregistered kills
- **Application Crashes**: Check the kill_logger.log file in the application data folder for error details
- **Twitch Integration Issues**: Ensure your Twitch channel name is correct and try reconnecting

## **Data Storage**

The application stores configuration and data in the following locations:

- **Configuration**: `%APPDATA%\SCTool_Tracker\config.json`
- **Local Kill Cache**: `%APPDATA%\SCTool_Tracker\logged_kills.json`
- **Application Logs**: `%APPDATA%\SCTool_Tracker\kill_logger.log`
- **Updates**: `%APPDATA%\SCTool_Tracker\Updates\`

## **Contributing**

Contributions to SCTool Tracker are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## **Contact**

For support or inquiries, please visit [starcitizentool.com](https://starcitizentool.com).