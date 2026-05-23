"""
CLYVO VET - IoT Sensor Simulation
Disruptive Architectures: IoT, IoB & Generative IA - Sprint 1
FIAP 2026

Descrição:
    Simula os sensores do dispositivo IoT wearable para pets:
      - DHT22: temperatura corporal
      - Sensor de batimentos cardíacos (simulado)
      - Display LCD (saída no terminal / dashboard)
    Publica dados via HTTP para o dashboard local.
"""

import time
import random
import math
import json
import threading
import requests
from datetime import datetime

# ─── Configurações ────────────────────────────────────────────────────────────
DASHBOARD_URL = "http://localhost:5000/api/sensor-data"
PUBLISH_INTERVAL_SECONDS = 2
PET_NAME = "Thor"
PET_SPECIES = "dog"   # "dog" ou "cat"

# Faixas normais por espécie
NORMAL_RANGES = {
    "dog": {"temp": (37.5, 39.2), "hr": (60, 140), "rr": (10, 35)},
    "cat": {"temp": (37.8, 39.2), "hr": (120, 220), "rr": (16, 40)},
}


# ─── Sensores Simulados ───────────────────────────────────────────────────────
class DHT22Sensor:
    """Simula sensor de temperatura e umidade DHT22."""

    def __init__(self, base_temp: float = 38.5):
        self.base_temp = base_temp
        self._tick = 0

    def read(self) -> dict:
        self._tick += 1
        # Oscilação realista com componente senoidal + ruído
        temp = self.base_temp + 0.4 * math.sin(self._tick / 20) + random.uniform(-0.1, 0.1)
        humidity = 55.0 + 5 * math.sin(self._tick / 15) + random.uniform(-1, 1)
        return {
            "temperature_c": round(temp, 2),
            "humidity_pct":  round(humidity, 1),
            "sensor":        "DHT22",
        }


class HeartRateSensor:
    """Simula sensor de batimentos cardíacos (tipo MAX30102 ou pulso manual)."""

    def __init__(self, base_hr: int = 90):
        self.base_hr = base_hr
        self._tick = 0

    def read(self) -> dict:
        self._tick += 1
        hr = self.base_hr + int(12 * math.sin(self._tick / 25)) + random.randint(-5, 5)
        spo2 = round(98.5 - 0.5 * abs(math.sin(self._tick / 30)) + random.uniform(-0.2, 0.2), 1)
        return {
            "heart_rate_bpm": hr,
            "spo2_pct":       spo2,
            "sensor":         "HeartRate-Simulated",
        }


class LCDDisplay:
    """Simula display LCD 16x2 (saída no terminal)."""

    WIDTH = 16

    def show(self, line1: str, line2: str = ""):
        def pad(s): return s[:self.WIDTH].ljust(self.WIDTH)
        border = "+" + "-" * self.WIDTH + "+"
        print(border)
        print(f"|{pad(line1)}|")
        print(f"|{pad(line2)}|")
        print(border)


# ─── Health Monitor ───────────────────────────────────────────────────────────
class PetHealthMonitor:
    """Agrega leituras dos sensores e avalia estado de saúde."""

    def __init__(self, pet_name: str, species: str):
        base_temp = 38.5 if species == "dog" else 38.8
        base_hr   = 90   if species == "dog" else 160
        self.name     = pet_name
        self.species  = species
        self.dht22    = DHT22Sensor(base_temp)
        self.hr_sensor = HeartRateSensor(base_hr)
        self.lcd      = LCDDisplay()
        self.history  = []

    def read_all(self) -> dict:
        temp_data = self.dht22.read()
        hr_data   = self.hr_sensor.read()
        return {
            "timestamp":       datetime.now().isoformat(),
            "pet_name":        self.name,
            "species":         self.species,
            "temperature_c":   temp_data["temperature_c"],
            "humidity_pct":    temp_data["humidity_pct"],
            "heart_rate_bpm":  hr_data["heart_rate_bpm"],
            "spo2_pct":        hr_data["spo2_pct"],
            "alerts":          self._check_alerts(temp_data, hr_data),
        }

    def _check_alerts(self, temp_data: dict, hr_data: dict) -> list[str]:
        r = NORMAL_RANGES.get(self.species, NORMAL_RANGES["dog"])
        alerts = []
        t = temp_data["temperature_c"]
        hr = hr_data["heart_rate_bpm"]
        if not (r["temp"][0] <= t <= r["temp"][1]):
            alerts.append(f"Temperatura fora do normal: {t}°C")
        if not (r["hr"][0] <= hr <= r["hr"][1]):
            alerts.append(f"FC fora do normal: {hr} bpm")
        return alerts

    def update_display(self, reading: dict):
        line1 = f"{self.name[:8]} {reading['temperature_c']}C"
        line2 = f"FC:{reading['heart_rate_bpm']}bpm SpO2:{reading['spo2_pct']}%"
        self.lcd.show(line1, line2)

    def push_to_dashboard(self, reading: dict):
        try:
            requests.post(DASHBOARD_URL, json=reading, timeout=2)
        except Exception:
            pass  # Dashboard pode não estar ativo; não interrompe o sensor

    def run(self, interval: float = PUBLISH_INTERVAL_SECONDS):
        print("=" * 50)
        print(f"  CLYVO VET — IoT Sensor Simulation")
        print(f"  Pet: {self.name}  |  Espécie: {self.species}")
        print("=" * 50)
        print("  Ctrl+C para encerrar\n")

        try:
            while True:
                reading = self.read_all()
                self.history.append(reading)
                self.update_display(reading)

                ts = reading["timestamp"][11:19]
                print(f"  [{ts}] Temp: {reading['temperature_c']}°C  "
                      f"FC: {reading['heart_rate_bpm']} bpm  "
                      f"SpO2: {reading['spo2_pct']}%")

                if reading["alerts"]:
                    for alert in reading["alerts"]:
                        print(f"  ⚠  ALERTA: {alert}")

                self.push_to_dashboard(reading)

                # Salva histórico local
                with open("logs/sensor_history.json", "w", encoding="utf-8") as f:
                    json.dump(self.history[-200:], f, ensure_ascii=False, indent=2)

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n  Simulação encerrada.")
            print(f"  {len(self.history)} leituras salvas em logs/sensor_history.json")


# ─── Entrada ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    monitor = PetHealthMonitor(PET_NAME, PET_SPECIES)
    monitor.run()
