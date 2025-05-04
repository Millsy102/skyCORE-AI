from PySide6.QtCore import QThread, Signal
import socket
import threading

class TwitchChatReader(QThread):
    message_received = Signal(str)

    def __init__(self, oauth, nickname, channel):
        super().__init__()
        self.oauth = oauth
        self.nickname = nickname
        self.channel = channel
        self.running = True

    def run(self):
        try:
            s = socket.socket()
            s.connect(("irc.chat.twitch.tv", 6667))
            s.send(f"PASS {self.oauth}\r\n".encode("utf-8"))
            s.send(f"NICK {self.nickname}\r\n".encode("utf-8"))
            s.send(f"JOIN #{self.channel}\r\n".encode("utf-8"))

            while self.running:
                resp = s.recv(2048).decode("utf-8")
                if resp.startswith("PING"):
                    s.send("PONG\r\n".encode("utf-8"))
                elif "PRIVMSG" in resp:
                    user = resp.split("!", 1)[0][1:]
                    msg = resp.split("PRIVMSG", 1)[1].split(":", 1)[1]
                    self.message_received.emit(f"💬 {user}: {msg.strip()}")
        except Exception as e:
            self.message_received.emit(f"⚠️ Chat error: {e}")

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
