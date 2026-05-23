# CLYVO VET — IoT & Computer Vision
### FIAP Challenge 2026 · Disruptive Architectures: IoT, IoB & Generative IA · Sprint 1

---

## 📌 Sobre o Projeto

O **CLYVO VET** é uma plataforma digital voltada à jornada contínua de saúde dos pets, conectando clínicas, tutores e o ecossistema veterinário. Este repositório contém a entrega do **Sprint 1** — foco em **IoT e Visão Computacional**.

A solução monitora a saúde do pet em tempo real através de:
- 🐾 **Detecção e classificação** de pets por Visão Computacional (OpenCV + YOLOv4)
- 🌡️ **Leitura de sensores** IoT simulados (DHT22, batimentos, LCD)
- 📊 **Dashboard web** com atualização em tempo real (Flask + SSE + Chart.js)
- 🔌 **Simulação de circuito** ESP32 no Wokwi (diagrama + código Arduino)

---

## 🗂️ Estrutura do Repositório

```
IOT/
├── pet_detection.py          # Visão Computacional — detecção de pets
├── iot_sensor_simulation.py  # Simulação dos sensores IoT (Python)
├── dashboard_server.py       # Servidor Flask do dashboard
├── requirements.txt          # Dependências Python
├── templates/
│   └── dashboard.html        # Interface web do dashboard
├── wokwi/
│   ├── diagram.json          # Circuito ESP32 (Wokwi)
│   ├── sketch.ino            # Firmware Arduino
│   └── libraries.txt         # Bibliotecas Wokwi
├── models/                   # (opcional) Pesos YOLO — ver instruções
├── logs/                     # Gerado automaticamente
└── screenshots/              # Gerado automaticamente
```

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia | Finalidade |
|---|---|---|
| Visão Computacional | Python + OpenCV 4 | Detecção e classificação de pets |
| Modelo de detecção | YOLOv4-tiny (COCO) | Identificação de cão/gato em vídeo |
| IoT Software | Python (simulação) | Emulação de DHT22, sensor de FC, LCD |
| IoT Hardware | ESP32 + Wokwi | Circuito simulado com firmware real |
| Dashboard | Flask + Chart.js | Visualização em tempo real via SSE |
| Protocolo | HTTP (REST + SSE) | Comunicação sensor → dashboard |

---

## 🚀 Como Executar

### Pré-requisitos
```bash
python -m pip install -r requirements.txt
```

> **Modelos YOLO (opcional — necessário para detecção real):**
> ```
> # Baixe e coloque na pasta models/
> yolov4-tiny.weights  →  https://github.com/AlexeyAB/darknet/releases
> yolov4-tiny.cfg      →  https://github.com/AlexeyAB/darknet/blob/master/cfg/yolov4-tiny.cfg
> coco.names           →  https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
> ```
> Sem os modelos, o sistema usa **modo de simulação** automaticamente.

---

### 1. Dashboard (inicie primeiro)
```bash
python dashboard_server.py
# Acesse: http://localhost:5000
```

### 2. Simulação de Sensores IoT
```bash
python iot_sensor_simulation.py
# Publica leituras de temperatura, FC e SpO2 para o dashboard
```

### 3. Detecção de Pets por Visão Computacional
```bash
# Webcam
python pet_detection.py

# Arquivo de vídeo
python pet_detection.py caminho/video.mp4

# Imagem estática
python pet_detection.py caminho/imagem.jpg
```

### 4. Simulação de Circuito (Wokwi)
1. Acesse [wokwi.com](https://wokwi.com) e clique em **"New Project → ESP32"**
2. Importe o arquivo `wokwi/diagram.json`
3. Cole o conteúdo de `wokwi/sketch.ino` no editor
4. Clique em **Play ▶** para iniciar a simulação

---

## 🔬 Sensores e Circuito

| Componente | Pino ESP32 | Função |
|---|---|---|
| DHT22 | D4 | Temperatura corporal e umidade |
| LED vermelho | D2 | Pulsa no ritmo dos batimentos cardíacos |
| LCD I2C 16×2 | SDA=D21, SCL=D22 | Exibe nome do pet, temperatura e FC |
| Buzzer | D5 | Alerta sonoro em caso de valor anormal |

**Faixas normais monitoradas:**
- **Temperatura** (cão): 37,5 – 39,2 °C
- **FC** (cão): 60 – 140 bpm
- **SpO₂**: ≥ 95%

---

## 📊 Resultados Parciais

- ✅ Detecção de cão/gato em tempo real (modo simulado funcional sem YOLO)
- ✅ HUD com vitais simulados, bounding box e log de eventos
- ✅ Sensores publicando via HTTP a cada 2 segundos
- ✅ Dashboard atualizado em tempo real com gráfico histórico e log de alertas
- ✅ Circuito ESP32 com DHT22 + LCD + LED batimentos funcionando no Wokwi

---

## 🎥 Vídeo de Demonstração

> Link do YouTube: *https://youtu.be/gApzF3kRXaw*

---

## 🔗 Repositório

> Link do GitHub: *https://github.com/EduMollo/CS-parte-1-e-2-IOT-Grupo-FIEDMACALU*

---

## 👥 Integrantes

| Nome | RM |
|---|---|
| *Carlos Alberto Guedes* | *566022* |
| *Eduardo Novaes Mollo* | *561515* |
| *Filippo Dal Medico Tolone* | *562329* |
| *Luan Peixoto Marins* | *562258* |
| *Mathaus Victor Souza Marcelino* | *564146* |
