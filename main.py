import os
import sys
import json
import time
import datetime
import random
import re
from dataclasses import dataclass
from typing import Optional, Dict, List, Any
import requests

# मोबाइल के लिए उपयुक्त AI और मीडिया लाइब्रेरी
import openai
import wolframalpha
import flet as ft

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config:
    """JARVIS Mobile Configuration"""
    name: str = "JARVIS"
    wake_word: str = "jarvis"
    
    # API Keys (यहाँ अपनी असली कीज़ डालें)
    openai_api_key: str = "YOUR_OPENAI_API_KEY"
    wolfram_app_id: str = "YOUR_WOLFRAM_APP_ID"
    weather_api_key: str = "YOUR_WEATHER_API_KEY"
    news_api_key: str = "YOUR_NEWS_API_KEY"
    
    # Paths (मोबाइल स्टोरेज के अनुकूल)
    data_dir: str = "jarvis_mobile_data"
    
    # Features
    enable_ai_chat: bool = True
    enable_reminders: bool = True

# ============================================================================
# CORE ENGINE (MOBILE VERSION)
# ============================================================================

class JarvisEngine:
    """Core AI Engine optimized for Mobile Devices"""
    
    def __init__(self, config: Config):
        self.config = config
        self.context = {}
        self.memory = []
        self.user_preferences = {"location": "New York"}
        self.active_tasks = []
        
        self._init_ai_models()
        self._create_directories()
        self._load_memory()
        
    def _init_ai_models(self):
        """API आधारित एआई मॉडल्स को एक्टिव करना"""
        # OpenAI Setup
        if self.config.openai_api_key != "YOUR_OPENAI_API_KEY":
            openai.api_key = self.config.openai_api_key
            self.openai_available = True
        else:
            self.openai_available = False
            
        # WolframAlpha Setup
        if self.config.wolfram_app_id != "YOUR_WOLFRAM_APP_ID":
            self.wolfram = wolframalpha.Client(self.config.wolfram_app_id)
            self.wolfram_available = True
        else:
            self.wolfram_available = False
    
    def _create_directories(self):
        os.makedirs(self.config.data_dir, exist_ok=True)
    
    def _load_memory(self):
        memory_file = os.path.join(self.config.data_dir, "memory.json")
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memory = data.get('memory', [])
                    self.user_preferences = data.get('preferences', {"location": "New York"})
            except:
                pass
    
    def _save_memory(self):
        memory_file = os.path.join(self.config.data_dir, "memory.json")
        try:
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'memory': self.memory[-50:], 
                    'preferences': self.user_preferences
                }, f, ensure_ascii=False)
        except:
            pass
    
    def think(self, input_text: str) -> str:
        """यूजर की बात समझकर बेस्ट एक्शन चुनना"""
        text_lower = input_text.lower()
        
        # 1. साधारण बातचीत और कमांड्स की पहचान
        if any(kw in text_lower for kw in ['hello', 'hi', 'hey', 'नमस्ते']):
            return random.choice(["Hello sir! How may I assist you today?", "At your service! What do you need?"])
            
        elif any(kw in text_lower for kw in ['bye', 'goodbye', 'अल्विदा']):
            return "Goodbye sir! I'll be here if you need me."
            
        elif 'time' in text_lower or 'समय' in text_lower:
            now = datetime.datetime.now()
            return f"The current time is {now.strftime('%I:%M %p')}."
            
        elif 'weather' in text_lower or 'मौसम' in text_lower:
            return self.get_weather()
            
        elif 'news' in text_lower or 'समाचार' in text_lower:
            return self.get_news()
            
        elif any(kw in text_lower for kw in ['calculate', 'solve', 'math']):
            expr = text_lower.replace('calculate', '').replace('solve', '').replace('math', '').strip()
            return self.calculate(expr)
            
        elif 'code' in text_lower or 'प्रोग्राम' in text_lower:
            return self.generate_code(input_text)
            
        # 2. अगर कुछ समझ न आए तो OpenAI GPT से पूछना
        else:
            return self.chat_gpt(input_text)
            
    def get_weather(self) -> str:
        location = self.user_preferences.get('location', 'New York')
        if self.config.weather_api_key == "YOUR_WEATHER_API_KEY":
            return f"Sir, please set your Weather API key to check the weather for {location}."
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.config.weather_api_key}&units=metric"
            data = requests.get(url).json()
            if data.get('cod') == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                return f"The weather in {location} is currently {desc} with a temperature of {temp}°C."
            return "I couldn't fetch the weather right now."
        except:
            return "Network error while fetching weather data."
            
    def get_news(self) -> str:
        if self.config.news_api_key == "YOUR_NEWS_API_KEY":
            return "Sir, please set your News API key first."
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={self.config.news_api_key}"
            data = requests.get(url).json()
            if data.get('status') == 'ok':
                articles = data['articles'][:3]
                news_list = [f"• {a['title']}" for a in articles]
                return "Top Headlines:\n" + "\n".join(news_list)
            return "Could not retrieve the news."
        except:
            return "Network error while fetching news."

    def calculate(self, expression: str) -> str:
        if self.wolfram_available:
            try:
                result = self.wolfram.query(expression)
                return next(result.results).text
            except:
                pass
        try:
            allowed = {'+', '-', '*', '/', '**', '(', ')', '.', ' '}
            if all(c in allowed or c.isdigit() for c in expression):
                return f"The result is {eval(expression)}"
            return "I can only handle basic arithmetic operations locally."
        except:
            return "Calculation failed. Please verify the expression."

    def chat_gpt(self, message: str) -> str:
        if self.openai_available:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are JARVIS, an advanced personal AI mobile assistant."},
                        {"role": "user", "content": message}
                    ]
                )
                return response.choices[0].message.content
            except:
                return "I'm having trouble reaching my primary AI servers."
        return "Offline Mode: Sir, please configure your OpenAI API key for advanced reasoning."

    def generate_code(self, task: str) -> str:
        if self.openai_available:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional coding expert. Generate clean Python code based on requests."},
                        {"role": "user", "content": task}
                    ]
                )
                return f"Here is the requested script:\n\n{response.choices[0].message.content}"
            except:
                return "Failed to connect to the code generation engine."
        return "Code generation requires an active OpenAI API key."

# ============================================================================
# USER INTERFACE (FLET MOBILE UI)
# ============================================================================

def main(page: ft.Page):
    page.title = "JARVIS AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    
    # मोबाइल रिस्पॉन्सिव सेटिंग्स
    page.window_width = 400
    page.window_height = 700

    # जार्विस कोर इंजन को शुरू करना
    config = Config()
    jarvis = JarvisEngine(config)

    # चैट लेआउट बनाना
    chat_list = ft.ListView(
        expand=True,
        spacing=15,
        auto_scroll=True
    )

    def on_send_click(e):
        if not user_input.value.strip():
            return
            
        user_text = user_input.value.strip()
        
        # 1. यूजर का मैसेज चैट में जोड़ना
        chat_list.controls.append(
            ft.Container(
                content=ft.Text(user_text, color=ft.colors.WHITE),
                alignment=ft.alignment.center_right,
                padding=10,
                bgcolor=ft.colors.BLUE_GREY_800,
                border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15)
            )
        )
        user_input.value = ""
        page.update()
        
        # 2. जार्विस का सोचना और जवाब देना
        response_text = jarvis.think(user_text)
        
        # 3. जार्विस का मैसेज चैट में जोड़ना
        chat_list.controls.append(
            ft.Container(
                content=ft.Text(f"JARVIS: {response_text}", color=ft.colors.CYAN_ACCENT),
                alignment=ft.alignment.center_left,
                padding=10,
                bgcolor=ft.colors.BLACK,
                border=ft.border.all(1, ft.colors.CYAN),
                border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15)
            )
        )
        page.update()

    # इनपुट बॉक्स और सेंड बटन
    user_input = ft.TextField(
        hint_text="Ask JARVIS anything...",
        expand=True,
        border_color=ft.colors.CYAN,
        on_submit=on_send_click
    )
    
    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=ft.colors.CYAN,
        on_click=on_send_click
    )

    # स्वागत संदेश (Welcome Note)
    chat_list.controls.append(
        ft.Text("JARVIS System Online. Awaiting your commands, sir.", color=ft.colors.CYAN, text_align=ft.TextAlign.CENTER)
    )

    # स्क्रीन पर सब कुछ व्यवस्थित करना
    page.add(
        ft.Container(
            content=chat_list,
            expand=True,
            border=ft.border.all(1, ft.colors.GREY_800),
            border_radius=10,
            padding=10,
            bgcolor=ft.colors.BLACK
        ),
        ft.Row(
            controls=[user_input, send_button],
            spacing=10
        )
    )

if __name__ == "__main__":
    ft.app(target=main)

