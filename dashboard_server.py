"""
CLYVO VET - Dashboard Web
Disruptive Architectures: IoT, IoB & Generative IA - Sprint 1
FIAP 2026

Servidor Flask que:
  - Recebe dados dos sensores via HTTP POST /api/sensor-data
  - Expõe dados em tempo real via SSE (Server-Sent Events)
  - Serve a interface web do dashboard
"""

from flask import Flask, render_template, request, jsonify, Response
import json
import threading
import queue
import os
from datetime import datetime

app = Flask(__name__)

# Fila de eventos SSE (Server-Sent Events)
sse_clients: list[queue.Queue] = []
sse_lock = threading.Lock()

# Buffer das últimas leituras
sensor_buffer: list[dict] = []
MAX_BUFFER = 100


def broadcast(data: dict):
    """Envia dado para todos os clientes SSE conectados."""
    payload = f"data: {json.dumps(data)}\n\n"
    with sse_lock:
        dead = []
        for q in sse_clients:
            try:
                q.put_nowait(payload)
            except queue.Full:
                dead.append(q)
        for q in dead:
            sse_clients.remove(q)


@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/api/sensor-data", methods=["POST"])
def receive_sensor_data():
    """Endpoint que recebe dados dos sensores (iot_sensor_simulation.py)."""
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Payload inválido"}), 400

    data.setdefault("timestamp", datetime.now().isoformat())
    sensor_buffer.append(data)
    if len(sensor_buffer) > MAX_BUFFER:
        sensor_buffer.pop(0)

    broadcast(data)
    return jsonify({"status": "ok"}), 200


@app.route("/api/history")
def history():
    """Retorna histórico das últimas leituras."""
    return jsonify(sensor_buffer)


@app.route("/stream")
def stream():
    """SSE endpoint — o dashboard se conecta aqui para receber dados em tempo real."""
    def generate():
        q: queue.Queue = queue.Queue(maxsize=50)
        with sse_lock:
            sse_clients.append(q)
        try:
            # Envia histórico recente imediatamente
            for entry in sensor_buffer[-10:]:
                yield f"data: {json.dumps(entry)}\n\n"
            while True:
                payload = q.get(timeout=30)
                yield payload
        except (GeneratorExit, queue.Empty):
            pass
        finally:
            with sse_lock:
                if q in sse_clients:
                    sse_clients.remove(q)

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    print("=" * 50)
    print("  CLYVO VET — Dashboard")
    print("  Acesse: http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
