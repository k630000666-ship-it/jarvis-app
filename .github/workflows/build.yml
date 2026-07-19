import flet as ft
import webbrowser
import os
import datetime
import random
import requests
import json
import subprocess
import platform
import folium
import geocoder
import threading
import time
import pyttsx3
import speech_recognition as sr
from plyer import notification
import psutil
import socket
import speedtest

# ------------------- JARVIS CYBER COMMAND CENTER -------------------
class JarvisCyberAI:
    def __init__(self):
        self.name = "JARVIS-CYBER"
        self.version = "5.0"
        self.status = "🟢 ACTIVE"
        self.location = None
        self.command_history = []
        self.hack_mode = False
        
        # Voice Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 1.0)
        
        # Network Info
        self.get_network_info()
        
    def get_network_info(self):
        try:
            self.hostname = socket.gethostname()
            self.ip = socket.gethostbyname(self.hostname)
        except:
            self.hostname = "Unknown"
            self.ip = "0.0.0.0"
    
    def speak(self, text):
        def _speak():
            self.engine.say(text)
            self.engine.runAndWait()
        threading.Thread(target=_speak, daemon=True).start()
    
    def get_location(self):
        try:
            g = geocoder.ip('me')
            self.location = {
                'lat': g.latlng[0] if g.latlng else 28.6139,
                'lng': g.latlng[1] if g.latlng else 77.2090,
                'city': g.city if g.city else "Delhi",
                'country': g.country if g.country else "India"
            }
            return self.location
        except:
            self.location = {'lat': 28.6139, 'lng': 77.2090, 'city': 'Delhi', 'country': 'India'}
            return self.location
    
    def create_map(self):
        loc = self.get_location()
        m = folium.Map(location=[loc['lat'], loc['lng']], zoom_start=12)
        
        folium.Marker(
            [loc['lat'], loc['lng']],
            popup=f"{loc['city']}, {loc['country']}",
            icon=folium.Icon(color='red', icon='info-sign'),
        ).add_to(m)
        
        # Add circle
        folium.Circle(
            radius=5000,
            location=[loc['lat'], loc['lng']],
            popup="Your Location",
            color="cyan",
            fill=True,
        ).add_to(m)
        
        m.save("location_map.html")
        webbrowser.open("location_map.html")
        return "Map opened in browser!"
    
    def system_info(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"""
        ═══════════════════════════════
        🖥️ SYSTEM INFORMATION
        ═══════════════════════════════
        💻 Hostname: {self.hostname}
        🌐 IP Address: {self.ip}
        📍 Location: {self.location['city']}, {self.location['country']}
        ⚡ CPU Usage: {cpu}%
        🧠 RAM: {memory.percent}% used ({memory.used//(1024**3)}GB/{memory.total//(1024**3)}GB)
        💾 Disk: {disk.percent}% used
        🕐 Time: {datetime.datetime.now().strftime('%I:%M:%S %p')}
        📅 Date: {datetime.datetime.now().strftime('%B %d, %Y')}
        ═══════════════════════════════
        """
        return info
    
    def network_scan(self):
        try:
            result = subprocess.check_output(['ping', '-c', '4', 'google.com']).decode()
            return f"✅ Network Active\n{result[:500]}..."
        except:
            return "❌ Network Error!"
    
    def wifi_password(self):
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode()
                profiles = [line.split(":")[1].strip() for line in output.split('\n') if "All User Profile" in line]
                passwords = []
                for profile in profiles:
                    try:
                        info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode()
                        password = [line.split(":")[1].strip() for line in info.split('\n') if "Key Content" in line]
                        if password:
                            passwords.append(f"{profile}: {password[0]}")
                    except:
                        pass
                return "\n".join(passwords) if passwords else "No saved WiFi"
            else:
                return "🔒 Feature available on Windows only"
        except:
            return "❌ Access Denied!"
    
    def speed_test(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            return f"📥 Download: {download:.2f} Mbps\n📤 Upload: {upload:.2f} Mbps"
        except:
            return "⚠️ Speed test failed!"
    
    def hack_simulator(self):
        # Legal simulation with cool effect
        steps = [
            "🔍 Scanning network...",
            "📡 Connecting to server...",
            "🔑 Brute forcing access...",
            "✅ Access granted!",
            "📁 Downloading data...",
            "🕵️ Extracting information...",
            "🔥 Data encrypted!",
            "🔒 Securing connection...",
            "⚠️ Security alert!",
            "🔄 Re-routing through proxy...",
            "✅ Mission complete!"
        ]
        return steps
    
    def process_command(self, cmd):
        cmd = cmd.lower().strip()
        response = ""
        
        if "map" in cmd or "location" in cmd:
            response = self.create_map()
        
        elif "system" in cmd or "info" in cmd:
            response = self.system_info()
        
        elif "network" in cmd or "ping" in cmd:
            response = self.network_scan()
        
        elif "wifi" in cmd and "password" in cmd:
            response = self.wifi_password()
        
        elif "speed" in cmd:
            response = self.speed_test()
        
        elif "hack" in cmd:
            response = "\n".join(self.hack_simulator())
            self.hack_mode = True
        
        elif "whoami" in cmd:
            response = f"🕵️ You are: {os.getlogin()}\n💻 Host: {self.hostname}\n🌐 IP: {self.ip}"
        
        elif "help" in cmd:
            response = """
            ════════════════════════════════════════
            🤖 JARVIS CYBER COMMANDS
            ════════════════════════════════════════
            🗺️ map - Show your location
            💻 system - System information
            🌐 network - Network status
            📶 wifi password - Show saved WiFi
            ⚡ speed - Internet speed test
            🔥 hack - Activate hack mode
            🕵️ whoami - Your identity
            🎯 google - Open Google
            📺 youtube - Open YouTube
            🎮 matrix - Matrix effect
            ⏰ time - Current time
            🗓️ date - Today's date
            ❌ exit - Quit JARVIS
            ════════════════════════════════════════
            """
        
        elif "google" in cmd:
            webbrowser.open("https://google.com")
            response = "🌐 Opening Google..."
        
        elif "youtube" in cmd:
            webbrowser.open("https://youtube.com")
            response = "📺 Opening YouTube..."
        
        elif "matrix" in cmd:
            response = self.matrix_effect()
        
        elif "time" in cmd:
            response = f"🕐 {datetime.datetime.now().strftime('%I:%M:%S %p')}"
        
        elif "date" in cmd:
            response = f"📅 {datetime.datetime.now().strftime('%B %d, %Y')}"
        
        elif "exit" in cmd or "quit" in cmd:
            response = "⚠️ Shutting down... See you later!"
            self.speak(response)
            exit()
        
        else:
            response = f"❓ Unknown command: {cmd}\nType 'help' for commands"
        
        self.command_history.append((datetime.datetime.now(), cmd, response))
        return response
    
    def matrix_effect(self):
        chars = "01"
        matrix = "\n".join(["".join(random.choice(chars) for _ in range(50)) for _ in range(10)])
        return f"🌀 MATRIX MODE\n{matrix}"

# ------------------- FLET UI - CYBER EDITION -------------------
def main(page: ft.Page):
    page.title = "JARVIS CYBER COMMAND CENTER"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.BLACK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    
    jarvis = JarvisCyberAI()
    
    # Cyber Matrix Animation
    def matrix_background():
        for i in range(100):
            color = ft.colors.GREEN if random.random() > 0.5 else ft.colors.BLACK
            yield ft.Container(
                content=ft.Text(random.choice("01"), color=color, size=random.randint(8, 20)),
                left=random.randint(0, 800),
                top=random.randint(0, 600),
                animate=ft.animation.Animation(1000, "bounceOut"),
            )
    
    # Custom Scrollable Chat
    chat_container = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        height=450,
        width=700,
    )
    
    # Terminal Style Input
    input_field = ft.TextField(
        hint_text=">_ ENTER COMMAND...",
        width=550,
        border_color=ft.colors.CYAN,
        focused_border_color=ft.colors.GREEN,
        text_style=ft.TextStyle(
            color=ft.colors.GREEN,
            font_family="Courier",
            size=16
        ),
        hint_style=ft.TextStyle(
            color=ft.colors.GREY,
            font_family="Courier",
            size=14
        ),
        on_submit=lambda e: send_command(),
        prefix_text="> ",
        prefix_style=ft.TextStyle(color=ft.colors.CYAN),
    )
    
    # Cyber Buttons
    def create_cyber_button(text, icon, color, action):
        return ft.IconButton(
            icon=icon,
            icon_color=color,
            icon_size=25,
            tooltip=text,
            on_click=action,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.colors.BLACK,
                side=ft.border.all(1, color),
            ),
        )
    
    # Status Bar
    status_bar = ft.Container(
        content=ft.Row([
            ft.Text("⚡ JARVIS-CYBER", color=ft.colors.CYAN, weight=ft.FontWeight.BOLD),
            ft.Text("•", color=ft.colors.GREY),
            ft.Text("SYSTEM ACTIVE", color=ft.colors.GREEN, size=12),
            ft.Text("•", color=ft.colors.GREY),
            ft.Text(f"IP: {jarvis.ip}", color=ft.colors.YELLOW, size=12),
            ft.Text("•", color=ft.colors.GREY),
            ft.Text(datetime.datetime.now().strftime("%H:%M:%S"), color=ft.colors.CYAN, size=12),
        ]),
        padding=10,
        bgcolor=ft.colors.BLUE_GREY_900,
        border=ft.border.all(1, ft.colors.CYAN),
        border_radius=5,
        width=700,
    )
    
    # Command Output
    def add_output(text, is_user=False):
        color = ft.colors.GREEN if not is_user else ft.colors.CYAN
        prefix = "👤" if is_user else "🤖"
        
        container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(prefix, size=16),
                    ft.Text(
                        text,
                        color=color,
                        size=14,
                        font_family="Courier",
                    )
                ]),
            ]),
            padding=10,
            bgcolor=ft.colors.BLACK if not is_user else ft.colors.BLUE_GREY_900,
            border=ft.border.all(1, color),
            border_radius=10,
            width=650,
        )
        chat_container.controls.append(container)
        page.update()
        # Auto scroll
        if len(chat_container.controls) > 0:
            chat_container.scroll_to(offset=-1, duration=300)
    
    # Send Command
    def send_command():
        if input_field.value.strip():
            cmd = input_field.value
            add_output(f"{cmd}", is_user=True)
            input_field.value = ""
            page.update()
            
            # Process
            response = jarvis.process_command(cmd)
            
            # If hack mode, show cool effect
            if "hack" in cmd:
                for step in response.split('\n'):
                    add_output(f"⚡ {step}")
                    time.sleep(0.3)
                    page.update()
            else:
                add_output(response)
            
            jarvis.speak(response[:100])  # Speak first 100 chars
    
    # Voice Command
    def voice_command():
        try:
            status_bar.content.controls[2] = ft.Text("🎤 LISTENING...", color=ft.colors.RED, size=12)
            page.update()
            
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio)
                input_field.value = text
                page.update()
                send_command()
        except:
            add_output("⚠️ Voice recognition failed!")
        finally:
            status_bar.content.controls[2] = ft.Text("SYSTEM ACTIVE", color=ft.colors.GREEN, size=12)
            page.update()
    
    # Clear Screen
    def clear_screen(e):
        chat_container.controls.clear()
        add_output("🔄 Screen cleared!")
        page.update()
    
    # Special Hack Button
    def hack_mode(e):
        add_output("🔥 ACTIVATING HACK MODE...")
        response = jarvis.hack_simulator()
        for step in response:
            add_output(f"⚡ {step}")
            time.sleep(0.2)
            page.update()
        add_output("✅ HACK MODE ACTIVE - ALL SYSTEMS GO!")
    
    # Buttons Row
    button_row = ft.Row([
        create_cyber_button("Map", ft.icons.MAP, ft.colors.GREEN, lambda e: send_command_with("map")),
        create_cyber_button("System", ft.icons.DEVICES, ft.colors.CYAN, lambda e: send_command_with("system")),
        create_cyber_button("Network", ft.cons.NETWORK_WIFI, ft.colors.YELLOW, lambda e: send_command_with("network")),
        create_cyber_button("Speed", ft.icons.SPEED, ft.colors.PURPLE, lambda e: send_command_with("speed")),
        create_cyber_button("Hack", ft.icons.BOLT, ft.colors.RED, hack_mode),
        create_cyber_button("Clear", ft.icons.CLEAR, ft.colors.WHITE, clear_screen),
        create_cyber_button("Mic", ft.icons.MIC, ft.colors.ORANGE, lambda e: voice_command()),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
    
    def send_command_with(cmd):
        input_field.value = cmd
        send_command()
    
    # Main Layout
    main_container = ft.Container(
        content=ft.Column([
            status_bar,
            ft.Divider(color=ft.colors.CYAN, height=1),
            chat_container,
            ft.Divider(color=ft.colors.CYAN, height=1),
            input_field,
            button_row,
        ]),
        bgcolor=ft.colors.BLACK,
        border=ft.border.all(2, ft.colors.CYAN),
        border_radius=15,
        padding=20,
        width=750,
    )
    
    # Background Matrix
    matrix_bg = ft.Stack([
        ft.Container(
            content=ft.Row([
                ft.Text("01", color=ft.colors.GREEN_400, size=10, opacity=0.1)
                for _ in range(30)
            ]),
            width=800,
            height=700,
            opacity=0.1,
        ),
    ])
    
    page.add(matrix_bg, main_container)
    
    # Welcome
    add_output("╔═══════════════════════════════════════╗")
    add_output("║   🤖 JARVIS CYBER COMMAND CENTER     ║")
    add_output("║   Version 5.0 | AI Personal Assistant ║")
    add_output("╚═══════════════════════════════════════╝")
    add_output("💡 Type 'help' for commands")
    add_output("📍 Location detected: " + jarvis.location['city'] if jarvis.location else "")
    add_output(f"🌐 IP: {jarvis.ip}")
    add_output("🟢 System ready!")
    
    jarvis.speak("JARVIS Cyber system activated")

# ------------------- RUN -------------------
if __name__ == "__main__":
    ft.app(target=main)
