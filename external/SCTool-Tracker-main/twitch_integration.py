# twitch_integration.py
import os
import json
import time
import webbrowser
import logging
import threading
import http.server
import socketserver
import socket
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable, List
from urllib.parse import urlparse, parse_qs

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QTextBrowser,
    QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox, QGroupBox, QCheckBox,
    QSlider, QFormLayout, QLabel, QComboBox, QDialog, QSizePolicy, QProgressDialog
)

TWITCH_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "twitch_config.json")

class TwitchAuthHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for Twitch OAuth callback"""
    def do_GET(self):
        """Handle GET request to OAuth callback URL"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query
        params = parse_qs(query)
        
        if path == "/" or path == "/callback":
            if "error" in params:
                error_type = params.get("error", ["unknown"])[0]
                error_description = params.get("error_description", ["No description"])[0]
                logging.error(f"Authentication error: {error_type} - {error_description}")
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                error_html = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <!-- Meta Tags and Title -->
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>SCTool - Authentication Error</title>

                    <!-- Google Fonts -->
                    <link href="https://fonts.googleapis.com/css2?family=verdana:wght@400;700&display=swap" rel="stylesheet">

                    <!-- Font Awesome for Icons -->
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />

                    <!-- Bootstrap CSS -->
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">

                    <style>
                        /* CSS Variables */
                        :root {{
                            --primary-color: #ff5100;
                            --secondary-color: #1a1a1a; 
                            --accent-color: #e74c3c;
                            --background-color: #121212;
                            --text-color: #f5f5f5;
                            --secondary-text-color: #aaaaaa;
                            --button-color: #27ae60;
                            --font-family: 'verdana', sans-serif;
                            --card-background: #1a1a1a;
                            --card-border: #333333;
                            --card-shadow: rgba(0, 0, 0, 0.2);
                            --hover-shadow: rgba(0, 0, 0, 0.4);
                            --transition-speed: 0.3s;
                        }}

                        /* Reset and Base Styles */
                        * {{
                            margin: 0;
                            padding: 0;
                            box-sizing: border-box;
                        }}

                        html {{
                            scroll-behavior: smooth;
                            scroll-padding-top: 80px;
                        }}

                        body {{
                            display: flex;
                            flex-direction: column;
                            min-height: 100vh;
                            font-family: var(--font-family);
                            background-image: url('Static/SCtool.png');
                            background-repeat: no-repeat;
                            background-position: center center;
                            background-attachment: fixed;
                            background-size: cover;
                            color: var(--text-color);
                            overflow-x: hidden;
                            position: relative;
                        }}              

                        a {{
                            text-decoration: none;
                            color: inherit;
                        }}

                        /* Container */
                        .container {{
                            width: 90%;
                            max-width: 1200px;
                            margin: 0 auto;
                        }}

                        /* Navigation Bar */
                        .navbar {{
                            background-color: var(--secondary-color);
                            padding-top: 15px;
                            padding-bottom: 15px;
                            height: 70px;
                            border-bottom: 2px solid var(--primary-color);
                            position: fixed;
                            width: 100%;
                            top: 0;
                            z-index: 1000;
                            transition: background-color 0.3s, box-shadow 0.3s;
                        }}

                        .navbar .container {{
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            position: relative;
                            max-width: 1200px;
                            margin: 0 auto;
                            padding: 0 20px;
                            height: 50px;
                        }}

                        .navbar .brand {{
                            display: flex;
                            align-items: center;
                            align-self: flex-start;
                            margin-top: -3px;
                        }}        

                        .navbar .brand span {{
                            font-size: 1.8rem;
                            font-weight: bold;
                            color: var(--primary-color);
                        }}

                        /* Main Content */
                        main {{
                            flex: 1;
                            padding-top: 80px;
                        }}

                        /* Authentication Content */
                        .auth-container {{
                            max-width: 600px;
                            margin: 40px auto;
                            background-color: var(--secondary-color);
                            padding: 30px;
                            border-radius: 8px;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                            text-align: center;
                        }}

                        h1, h2, h3 {{ 
                            margin-bottom: 20px;
                        }}
                        
                        h1 {{ color: var(--primary-color); }}
                        h2.error {{ color: #ff0000; }}

                        p {{ 
                            margin: 20px 0; 
                            line-height: 1.5; 
                        }}

                        /* Footer */
                        footer {{
                            background-color: var(--secondary-color);
                            padding: 20px 0;
                            border-top: 2px solid var(--accent-color);
                            position: relative;
                            display: block;
                            width: 100%;
                        }}
                        
                        footer .container {{
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            max-width: 1200px;
                            margin: 0 auto;
                            padding: 0 20px;
                        }}
                        
                        footer p {{
                            text-align: center;
                            color: var(--text-color);
                            font-size: 0.9rem;
                            margin-bottom: 10px;
                        }}
                    </style>
                </head>
                <body>
                    <!-- Navigation Bar -->
                    <nav class="navbar">
                        <div class="container">
                            <div class="brand">
                                <a href="https://starcitizentool.com/">
                                    <span>SCTool</span>
                                </a>
                            </div>
                        </div>
                    </nav>

                    <!-- Main Content -->
                    <main>
                        <div class="auth-container">
                            <h1>SCTool Tracker</h1>
                            <h2 class="error">Authentication Failed</h2>
                            <p>{error_description}</p>
                            <p>Please check your Twitch application settings and try again.</p>
                            <p><strong>Make sure your redirect URI is exactly:</strong><br>
                            http://localhost:17563</p>
                        </div>
                    </main>

                    <!-- Footer -->
                    <footer>
                        <div class="container">
                            <p>&copy; 2024 SCTool. All rights reserved.</p>
                            <p>
                                <a href="https://starcitizentool.com/privacy-policy">Privacy Policy</a> | 
                                <a href="https://starcitizentool.com/terms-of-service">Terms of Service</a>
                            </p>
                        </div>
                    </footer>

                    <!-- Bootstrap JS -->
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                </body>
                </html>
                """
                
                self.wfile.write(error_html.encode())
                self.server.auth_code = None
                self.server.auth_handled = True
                return
                
            code = params.get('code', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            response_content = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <!-- Meta Tags and Title -->
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{% block title %}SCTool{% endblock %}</title>

                    <link href="https://fonts.googleapis.com/css2?family=verdana:wght@400;700&display=swap" rel="stylesheet">

                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />

                    <link href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet">

                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">

                    <style>
                        /* CSS Variables */
                        :root {
                            --primary-color: #ff5100;
                            --secondary-color: #1a1a1a;
                            --accent-color: #e74c3c;
                            --background-color: #121212;
                            --text-color: #f5f5f5;
                            --secondary-text-color: #aaaaaa;
                            --button-color: #27ae60;
                            --font-family: 'verdana', sans-serif;
                            --card-background: #1a1a1a;
                            --card-border: #333333;
                            --card-shadow: rgba(0, 0, 0, 0.2);
                            --hover-shadow: rgba(0, 0, 0, 0.4);
                            --transition-speed: 0.3s;
                        }

                        /* Reset and Base Styles */
                        * {
                            margin: 0;
                            padding: 0;
                            box-sizing: border-box;
                        }

                        html {
                            scroll-behavior: smooth;
                            scroll-padding-top: 80px;
                        }

                        body {
                            display: flex;
                            flex-direction: column;
                            min-height: 100vh;
                            font-family: var(--font-family);
                            background-image: url('file:///C:/Users/caleb/OneDrive/Desktop/SCTool Tracker/Static/SCtool.png');
                            background-repeat: no-repeat;
                            background-position: center center;
                            background-attachment: fixed;
                            background-size: cover;
                            color: var(--text-color);
                            overflow-x: hidden;
                            position: relative;
                        }              

                        a {
                            text-decoration: none;
                            color: inherit;
                        }

                        /* Container */
                        .container {
                            width: 90%;
                            max-width: 1200px;
                            margin: 0 auto;
                        }

                        /* Navigation Bar */
                        .navbar {
                            background-color: var(--secondary-color);
                            padding-top: 15px;
                            padding-bottom: 15px;
                            height: 70px;
                            border-bottom: 2px solid var(--primary-color);
                            position: fixed;
                            width: 100%;
                            top: 0;
                            z-index: 1000;
                            transition: background-color 0.3s, box-shadow 0.3s;
                        }

                        .navbar .container {
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            position: relative;
                            max-width: 1200px;
                            margin: 0 auto;
                            padding: 0 20px;
                            height: 50px;
                        }

                        .navbar .brand {
                            display: flex;
                            align-items: center;
                            align-self: flex-start;
                            margin-top: -3px;
                        }        

                        .navbar .brand span {
                            font-size: 1.8rem;
                            font-weight: bold;
                            color: var(--primary-color);
                        }

                        /* Main Content */
                        main {
                            flex: 1;
                            padding-top: 80px;
                        }

                        /* Authentication Content */
                        .auth-container {
                            max-width: 600px;
                            margin: 40px auto;
                            background-color: var(--secondary-color);
                            padding: 30px;
                            border-radius: 8px;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                            text-align: center;
                        }

                        h1, h2, h3 { 
                            margin-bottom: 20px;
                        }
                        
                        h1 { color: var(--primary-color); }
                        h2.success { color: #00ff00; }
                        h2.error { color: #ff0000; }

                        p { 
                            margin: 20px 0; 
                            line-height: 1.5; 
                        }

                        /* Leaderboard Card */
                        .leaderboard {
                            margin: 30px auto;
                            padding: 25px;
                            background-color: var(--card-background);
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                            max-width: 500px;
                        }

                        .leaderboard h3 {
                            color: var(--primary-color);
                            margin-top: 0;
                        }

                        /* Button Styling */
                        .btn-primary {
                            padding: 12px 25px;
                            background-color: var(--primary-color);
                            color: var(--text-color);
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 1rem;
                            font-weight: bold;
                            transition: background-color 0.3s, transform 0.3s;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                            text-align: center;
                            display: inline-block;
                            margin-top: 15px;
                        }

                        .btn-primary:hover {
                            background-color: var(--accent-color);
                            transform: translateY(-2px);
                        }

                    </style>
                </head>
                <body>
                    <!-- Navigation Bar -->
                    <nav class="navbar">
                        <div class="container">
                            <div class="brand">
                                <a href="https://starcitizentool.com/">
                                    <span>SCTool</span>
                                </a>
                            </div>
                        </div>
                    </nav>

                    <!-- Main Content -->
                    <main>
                        <div class="auth-container">
                            <h1>SCTool Tracker</h1>
            """
            
            if code:
                response_content += """
                            <h2 class="success">Authentication Successful!</h2>
                            <p>You have successfully connected your Twitch account to SCTool Tracker.</p>
                            <p>You can now close this window and return to the application.</p>
                        </div>
                        
                        <div class="leaderboard">
                            <h3>Global Kill Leaderboard</h3>
                            <p>Want to see how you rank against other players?</p>
                            <p>Check out the global kill leaderboard to see top players and stats!</p>
                            <a href="https://starcitizentool.com/kills/kill_leaderboard" target="_blank" class="btn-primary">View Global Leaderboard</a>
                        </div>
                """
                self.server.auth_code = code
            else:
                response_content += """
                            <h2 class="error">Authentication Failed</h2>
                            <p>There was a problem connecting your Twitch account.</p>
                            <p>Please try again or contact support.</p>
                        </div>
                """
                self.server.auth_code = None
            
            self.wfile.write(response_content.encode())
            
            self.server.auth_handled = True
            return
            
        return super().do_GET()
        
    def log_message(self, *args, **kwargs):
        return f"🔧 log_message executed with args={args} kwargs={kwargs}"

class TwitchIntegration:
    def __init__(self, broadcaster_name: str = "") -> None:
        self.client_id = ""
        self.client_secret = ""
        self.redirect_uri = "http://localhost:17563"
        
        self.broadcaster_name = broadcaster_name
        self.broadcaster_id = ""
        self.access_token = ""
        self.refresh_token = ""
        self.token_expiry = None
        self.is_authenticated = False
        self.pending_clips: Dict[str, Dict[str, Any]] = {}
        self.clip_delay_seconds = 0
        
        self.auth_callback = None
        self.clip_callbacks = {}
        
        self.load_config()

    def load_config(self) -> None:
        """Load Twitch configuration from file"""
        try:
            if os.path.exists(TWITCH_CONFIG_FILE):
                with open(TWITCH_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                    self.broadcaster_name = config.get('broadcaster_name', '')
                    self.broadcaster_id = config.get('broadcaster_id', '')
                    self.access_token = config.get('access_token', '')
                    self.refresh_token = config.get('refresh_token', '')
                    self.clip_delay_seconds = config.get('clip_delay_seconds', 0)
                    expiry_str = config.get('token_expiry')
                    if expiry_str:
                        self.token_expiry = datetime.fromisoformat(expiry_str)
                    
                    if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
                        self.is_authenticated = True
                        if self.broadcaster_name and not self.broadcaster_id:
                            self._get_broadcaster_id()
                logging.info("Twitch configuration loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load Twitch configuration: {e}")

    def save_config(self) -> None:
        """Save Twitch configuration to file"""
        try:
            config = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'broadcaster_name': self.broadcaster_name,
                'broadcaster_id': self.broadcaster_id,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'token_expiry': self.token_expiry.isoformat() if self.token_expiry else None,
                'clip_delay_seconds': self.clip_delay_seconds
            }
            
            with open(TWITCH_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
                
            logging.info("Twitch configuration saved successfully")
        except Exception as e:
            logging.error(f"Failed to save Twitch configuration: {e}")

    def setup(self, client_id: str, client_secret: str) -> bool:
        """Setup Twitch API credentials"""
        self.client_id = client_id
        self.client_secret = client_secret
        self.save_config()
        return True

    def authenticate(self, callback: Callable[[bool], None]) -> None:
        """Authenticate user with Twitch"""
        if not self.client_id or not self.client_secret:
            logging.error("Client ID and Secret must be set before authentication")
            callback(False)
            return
        
        self.auth_callback = callback
        
        try:
            scopes = [
                "clips:edit",
                "user:read:broadcast",
                "chat:edit",
                "chat:read"
            ]
            
            scope_str = "+".join(scopes)
            
            auth_url = (f"https://id.twitch.tv/oauth2/authorize"
                      f"?client_id={self.client_id}"
                      f"&redirect_uri={self.redirect_uri}"
                      f"&response_type=code"
                      f"&scope={scope_str}")
            
            webbrowser.open(auth_url)
            
            def run_server():
                try:
                    port = 17563
                    
                    try:
                        with socketserver.TCPServer(("", port), TwitchAuthHandler) as httpd:
                            logging.info(f"Started authentication server on port {port}")
                            
                            httpd.auth_code = None
                            httpd.auth_handled = False
                            
                            httpd.socket.settimeout(1.0)
                            
                            timeout = time.time() + 300
                            while not getattr(httpd, 'auth_handled', False) and time.time() < timeout:
                                try:
                                    httpd.handle_request()
                                except socket.timeout:
                                    pass
                            
                            auth_code = getattr(httpd, 'auth_code', None)
                            if auth_code:
                                token_url = "https://id.twitch.tv/oauth2/token"
                                data = {
                                    "client_id": self.client_id,
                                    "client_secret": self.client_secret,
                                    "code": auth_code,
                                    "grant_type": "authorization_code",
                                    "redirect_uri": self.redirect_uri
                                }
                                
                                response = requests.post(token_url, data=data)
                                if response.status_code == 200:
                                    token_data = response.json()
                                    self.access_token = token_data.get("access_token", "")
                                    self.refresh_token = token_data.get("refresh_token", "")
                                    expires_in = token_data.get("expires_in", 14400)
                                    self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                                    self.is_authenticated = True
                                    
                                    if self.broadcaster_name:
                                        self._get_broadcaster_id()
                                    else:
                                        self._get_user_info()
                                    
                                    self.save_config()
                                    
                                    if self.auth_callback:
                                        self._handle_auth_success(True)
                                else:
                                    logging.error(f"Failed to get access token: {response.text}")
                                    self._handle_auth_success(False)
                            else:
                                logging.error("No authorization code received")
                                self._handle_auth_success(False)
                    except OSError as e:
                        if e.errno == 10048:
                            logging.error(f"Port {port} is already in use. Please restart the application and try again.")
                        else:
                            logging.error(f"Server error: {e}")
                        self._handle_auth_success(False)
                except Exception as e:
                    logging.error(f"Error in authentication server: {str(e)}")
                    self._handle_auth_success(False)
            
            threading.Thread(target=run_server, daemon=True).start()
        
        except Exception as e:
            logging.error(f"Failed to initiate authentication: {e}")
            callback(False)
    
    def _handle_auth_success(self, success: bool) -> None:
        """Safely handle auth callback from worker thread to main thread"""
        if self.auth_callback:
            self._auth_success = success
            
    def process_auth_callback(self) -> Optional[bool]:
        """Process authentication callback in main thread"""
        if hasattr(self, '_auth_success'):
            success = self._auth_success
            callback = self.auth_callback
            
            delattr(self, '_auth_success')
            self.auth_callback = None
            
            if callback:
                callback(success)
            
            return success
        return None

    def _get_user_info(self) -> None:
        """Get authenticated user information"""
        if not self.access_token:
            return
            
        try:
            headers = {
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.get("https://api.twitch.tv/helix/users", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("data") and len(data["data"]) > 0:
                    user_data = data["data"][0]
                    self.broadcaster_name = user_data.get("login", "")
                    self.broadcaster_id = user_data.get("id", "")
                    logging.info(f"Got user info: {self.broadcaster_name} (ID: {self.broadcaster_id})")
        except Exception as e:
            logging.error(f"Failed to get user info: {e}")

    def _get_broadcaster_id(self) -> None:
        """Get broadcaster ID from username"""
        if not self.access_token or not self.broadcaster_name:
            return
        
        try:
            headers = {
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.get(
                f"https://api.twitch.tv/helix/users?login={self.broadcaster_name}", 
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("data") and len(data["data"]) > 0:
                    self.broadcaster_id = data["data"][0].get("id", "")
                    logging.info(f"Found broadcaster ID: {self.broadcaster_id}")
                else:
                    logging.warning(f"Could not find broadcaster ID for {self.broadcaster_name}")
        except Exception as e:
            logging.error(f"Failed to get broadcaster ID: {e}")

    def set_broadcaster_name(self, broadcaster_name: str) -> bool:
        """Set the broadcaster name and get its ID"""
        self.broadcaster_name = broadcaster_name
        
        if self.is_authenticated:
            self._get_broadcaster_id()
            self.save_config()
            return bool(self.broadcaster_id)
        return False

    def set_clip_delay(self, seconds: int) -> None:
        """Set the delay in seconds before creating a clip after a kill"""
        self.clip_delay_seconds = max(0, int(seconds))
        logging.info(f"Clip delay set to {self.clip_delay_seconds} seconds")
        self.save_config()

    def create_clip(self, kill_data: Dict[str, Any], callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """Create a clip of the current stream for a kill event"""
        if not self.is_authenticated or not self.broadcaster_id:
            logging.error("Cannot create clip: Not authenticated or no broadcaster ID")
            callback("", kill_data)
            return
        
        clip_request_id = f"clip_{int(time.time())}_{hash(str(kill_data))}"
        self.clip_callbacks[clip_request_id] = callback
            
        try:
            if self.clip_delay_seconds > 0:
                logging.info(f"Delaying clip creation by {self.clip_delay_seconds} seconds")
                
                threading.Thread(
                    target=self._delayed_clip_worker,
                    args=(kill_data, clip_request_id),
                    daemon=True
                ).start()
            else:
                threading.Thread(
                    target=self._create_clip_worker,
                    args=(kill_data, clip_request_id),
                    daemon=True
                ).start()
        except Exception as e:
            logging.error(f"Failed to start clip creation thread: {e}")
            callback("", kill_data)
            
    def _delayed_clip_worker(self, kill_data: Dict[str, Any], clip_request_id: str) -> None:
        """Worker thread that waits for the specified delay before creating a clip"""
        try:
            time.sleep(self.clip_delay_seconds)
            
            self._create_clip_worker(kill_data, clip_request_id)
        except Exception as e:
            logging.error(f"Error in delayed clip worker: {e}")
            self._handle_clip_result("", kill_data, clip_request_id)

    def _create_clip_worker(self, kill_data: Dict[str, Any], clip_request_id: str) -> None:
        """Worker thread for clip creation"""
        try:
            headers = {
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.post(
                "https://api.twitch.tv/helix/clips",
                headers=headers,
                params={"broadcaster_id": self.broadcaster_id}
            )
            
            if response.status_code == 202:
                clip_data = response.json()
                clip_id = clip_data.get("data", [{}])[0].get("id")
                
                if clip_id:
                    logging.info(f"Clip creation initiated, ID: {clip_id}")
                    
                    clip_url = f"https://clips.twitch.tv/{clip_id}"
                    
                    logging.info(f"Clip link available: {clip_url}")
                    self._handle_clip_result(clip_url, kill_data, clip_request_id)
                    
                else:
                    logging.error("Failed to create clip: No clip ID returned")
                    self._handle_clip_result("", kill_data, clip_request_id)
            else:
                error_message = "Unknown error"
                try:
                    error_message = response.json().get("message", "Unknown error")
                except:
                    pass
                logging.error(f"Failed to create clip: {error_message}")
                self._handle_clip_result("", kill_data, clip_request_id)
        except Exception as e:
            logging.error(f"Failed to create clip: {e}")
            self._handle_clip_result("", kill_data, clip_request_id)

    def _handle_clip_result(self, clip_url: str, kill_data: Dict[str, Any], clip_request_id: str) -> None:
        """Store the clip result to be processed by the main thread"""
        self._clip_results = self._clip_results if hasattr(self, '_clip_results') else {}
        self._clip_results[clip_request_id] = (clip_url, kill_data)

    def process_clip_callbacks(self) -> List[tuple]:
        """Process clip callbacks in the main thread - returns list of (clip_url, kill_data) tuples"""
        results = []
        
        if hasattr(self, '_clip_results'):
            clip_results = self._clip_results
            self._clip_results = {}
            
            for clip_request_id, (clip_url, kill_data) in clip_results.items():
                if clip_request_id in self.clip_callbacks:
                    callback = self.clip_callbacks[clip_request_id]
                    if callback:
                        callback(clip_url, kill_data)
                    del self.clip_callbacks[clip_request_id]
                results.append((clip_url, kill_data))
        
        return results

    def is_ready(self) -> bool:
        """Check if Twitch integration is set up and ready to use"""
        if self.is_authenticated and self.token_expiry and datetime.now() > self.token_expiry:
            self._refresh_auth_token()
            
        return (
            self.is_authenticated and 
            bool(self.broadcaster_id)
        )
        
    def _refresh_auth_token(self) -> bool:
        """Refresh authentication token if expired"""
        try:
            if not self.refresh_token:
                return False
                
            token_url = "https://id.twitch.tv/oauth2/token"
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            }
            
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token", "")
                self.refresh_token = token_data.get("refresh_token", "")
                expires_in = token_data.get("expires_in", 14400)
                self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                self.is_authenticated = True
                self.save_config()
                return True
            else:
                logging.error(f"Failed to refresh token: {response.text}")
                self.is_authenticated = False
                return False
        except Exception as e:
            logging.error(f"Failed to refresh authentication token: {e}")
            self.is_authenticated = False
            return False
            
    def disconnect(self) -> None:
        """Disconnect from Twitch"""
        self.is_authenticated = False
        self.access_token = ""
        self.refresh_token = ""
        self.token_expiry = None
        self.broadcaster_id = ""
        self.save_config()

    def send_chat_message(self, message: str) -> bool:
        """Send a message to the broadcaster's Twitch chat"""
        if not self.is_authenticated or not self.broadcaster_id or not self.broadcaster_name:
            logging.error("Cannot send chat message: Not authenticated or no broadcaster info")
            return False
            
        try:
            import socket
            import time
            
            server = "irc.chat.twitch.tv"
            port = 6667
            nickname = "sctoolbot"
            channel = f"#{self.broadcaster_name.lower()}"
            
            logging.debug(f"Connecting to Twitch IRC server: {server}:{port} as {nickname} for channel {channel}")
            
            irc_sock = socket.socket()
            irc_sock.settimeout(10)
            irc_sock.connect((server, port))
            logging.debug(f"Connected to IRC server {server}:{port}")
            
            if self.token_expiry and datetime.now() > self.token_expiry:
                logging.info("Token expired, refreshing before sending chat message")
                if not self._refresh_auth_token():
                    logging.error("Failed to refresh token for chat message")
                    return False
            
            auth_token = self.access_token
            if not auth_token.startswith("oauth:"):
                auth_token = f"oauth:{auth_token}"
                
            auth_command = f"PASS {auth_token}\r\n"
            logging.debug(f"Sending auth command to IRC server (token hidden)")
            irc_sock.send(auth_command.encode('utf-8'))
            
            nick_command = f"NICK {nickname}\r\n"
            logging.debug(f"Sending nick command: {nick_command.strip()}")
            irc_sock.send(nick_command.encode('utf-8'))
            
            response = ""
            try:
                start_time = time.time()
                while time.time() - start_time < 5:
                    try:
                        part = irc_sock.recv(2048).decode('utf-8', errors='ignore')
                        if not part:
                            break
                        
                        response += part
                        logging.debug(f"IRC server response: {part}")
                        
                        if "authentication failed" in part.lower():
                            logging.error(f"Twitch IRC authentication failed: {part}")
                            return False

                        if " 001 " in part:
                            logging.debug("Successfully authenticated with Twitch IRC")
                            break
                            
                    except socket.timeout:
                        break
            except socket.timeout:
                logging.warning("Timeout waiting for IRC server response")

            join_command = f"JOIN {channel}\r\n"
            logging.debug(f"Sending join command: {join_command.strip()}")
            irc_sock.send(join_command.encode('utf-8'))
            
            try:
                join_response = ""
                start_time = time.time()
                join_successful = False
                
                while time.time() - start_time < 3:
                    try:
                        part = irc_sock.recv(2048).decode('utf-8', errors='ignore')
                        if not part:
                            break
                            
                        join_response += part
                        logging.debug(f"IRC join response: {part}")

                        if f":{nickname}!{nickname}@{nickname}.tmi.twitch.tv JOIN {channel}" in part or f"JOIN {channel}" in part:
                            join_successful = True
                            logging.debug(f"Successfully joined channel {channel}")
                            break
                            
                    except socket.timeout:
                        break
                        
                if not join_successful:
                    logging.warning(f"No explicit join confirmation received for {channel}, attempting to send message anyway")

                time.sleep(0.5)
            except socket.timeout:
                logging.warning("Timeout waiting for join confirmation - attempting to send message anyway")
            
            chat_message = f"PRIVMSG {channel} :{message}\r\n"
            logging.debug(f"Sending chat message: {chat_message.strip()}")
            irc_sock.send(chat_message.encode('utf-8'))

            try:
                msg_response = irc_sock.recv(2048).decode('utf-8', errors='ignore')
                logging.debug(f"Message response: {msg_response}")
            except socket.timeout:
                pass

            time.sleep(0.5)

            quit_cmd = "QUIT :Disconnecting\r\n"
            try:
                irc_sock.send(quit_cmd.encode('utf-8'))
            except:
                pass

            irc_sock.close()
            
            logging.info(f"Message sent to Twitch chat ({channel}): {message}")
            return True
            
        except socket.gaierror:
            logging.error(f"DNS resolution failed for Twitch IRC server. Check your network connection.")
            return False
        except socket.timeout:
            logging.error(f"Connection to Twitch IRC server timed out")
            return False
        except Exception as e:
            logging.error(f"Failed to send chat message: {e}", exc_info=True)
            return False
            
    def post_kill_to_chat(self, message: str) -> None:
        """Post a kill notification to Twitch chat"""
        if not self.is_ready():
            logging.warning("Tried to post to chat but Twitch integration is not ready")
            return
            
        try:
            result = self.send_chat_message(message)
            if result:
                logging.info("Successfully sent kill message to Twitch chat")
            else:
                logging.error("Failed to send kill message to Twitch chat")
                raise Exception("Failed to send chat message")
        except Exception as e:
            logging.error(f"Error posting kill to Twitch chat: {e}")
            raise e

def process_twitch_callbacks(self) -> None:
    """Process any pending Twitch callbacks (auth or clip results) in the main thread"""
    auth_result = self.twitch.process_auth_callback()
    if auth_result is not None:
        if auth_result:
            self.update_bottom_info("twitch_connected", "Twitch Connected")
            self.showCustomMessageBox("Twitch Integration", 
                                    "Successfully connected to Twitch!\n\nKill clips will be created automatically.", 
                                    QMessageBox.Information)
            self.save_config()
        else:
            self.update_bottom_info("twitch_connected", "Twitch Not Connected")
            self.showCustomMessageBox("Twitch Integration", 
                                        "Failed to connect to Twitch. Check your credentials and try again.", 
                                        QMessageBox.Warning)
    
    clip_results = self.twitch.process_clip_callbacks()
    for clip_url, kill_data in clip_results:
        if clip_url:
            self.on_create_clip_finished(clip_url, kill_data)