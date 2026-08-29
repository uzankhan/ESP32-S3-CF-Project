# 🌍 IoT Smart Street Light & Environmental Monitoring System

[![ESP32](https://img.shields.io/badge/ESP32-000000?style=for-the-badge&logo=espressif&logoColor=white)](https://www.espressif.com/)
[![PlatformIO](https://img.shields.io/badge/PlatformIO-FF7F2A?style=for-the-badge&logo=platformio&logoColor=white)](https://platformio.org/)
[![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/uzankhan/CITYFLOW-IoT)](https://github.com/uzankhan/CITYFLOW-IoT/stargazers)

---

## 📌 Overview

**CITYFLOW** is a multi-sensor IoT system designed to automate street lighting while providing real-time environmental monitoring. The system automatically turns street lights ON/OFF based on ambient light intensity (LDR sensor) and displays temperature, humidity, gas levels, motion detection, and distance data on an I2C LCD screen.

This project demonstrates the power of **ESP32** in building **cost-effective, energy-efficient** smart city infrastructure.

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| **💡 Adaptive Street Lighting** | Automatically turns ON in darkness and OFF in bright light using LDR sensor |
| **🌡️ Environmental Monitoring** | Real-time Temperature & Humidity (DHT11) |
| **🔊 Safety Alerts** | Gas leak detection (MQ2) + Motion detection (PIR) with Buzzer alerts |
| **📏 Distance Measurement** | HC-SR04 Ultrasonic sensor for proximity detection |
| **🖥️ Real-time Display** | 16x2 I2C LCD shows all sensor data in real-time |
| **🔌 Modular Design** | Well-structured, easily extensible codebase |
| **⚡ Energy Efficient** | Optimized power management for ESP32 |

---

## 🧩 Hardware Components

| Component | Quantity | Purpose |
|-----------|----------|---------|
| [ESP32 Dev Board](https://www.espressif.com/en/products/socs/esp32) | 1 | Main Microcontroller |
| [LDR Sensor](https://en.wikipedia.org/wiki/Photoresistor) | 1 | Ambient light detection |
| [DHT11 Sensor](https://www.adafruit.com/product/386) | 1 | Temperature & Humidity |
| [HC-SR04 Ultrasonic](https://www.adafruit.com/product/3942) | 1 | Distance measurement |
| [MQ2 Gas Sensor](https://www.adafruit.com/product/257) | 1 | Gas leak detection (LPG, Smoke) |
| [PIR Motion Sensor](https://www.adafruit.com/product/189) | 1 | Motion detection |
| [Relay Module](https://www.adafruit.com/product/2935) | 1 | Street light control |
| [16x2 I2C LCD](https://www.adafruit.com/product/399) | 1 | Display sensor data |
| [Passive Buzzer](https://www.adafruit.com/product/1536) | 1 | Audible alerts |
| [5V Power Supply 2A](https://www.adafruit.com/product/1995) | 1 | External power source |

---

## 📐 Wiring Diagram & Pin Mapping

### ESP32 GPIO Pin Configuration:

| Component | ESP32 GPIO | Function |
|-----------|------------|----------|
| **LCD** | SDA: 21, SCL: 22 | I2C Communication |
| **LDR** | GPIO 34 | Analog Read (ADC1) |
| **Relay** | GPIO 23 | Digital Output |
| **DHT11** | GPIO 15 | Digital Input |
| **HC-SR04** | TRIG: 17, ECHO: 18 | Ultrasonic |
| **MQ2** | GPIO 2 | Digital Input |
| **PIR** | GPIO 19 | Digital Input |
| **Buzzer** | GPIO 26 | Digital Output |

> **⚠️ Important:** HC-SR04 ECHO pin is **5V** — use a **voltage divider** (1kΩ + 2kΩ) to convert to 3.3V for ESP32.

---

## 💻 Software Stack
CITYFLOW-IoT
├── Arduino Framework (C++)
├── Libraries Used:
│ ├── Wire.h (I2C Communication)
│ ├── LiquidCrystal_I2C.h (LCD Display)
│ ├── DHT.h (DHT11 Sensor)
│ ├── WiFi.h (ESP32 Networking)
│ └── Arduino.h (Core Framework)
└── Development Platform
├── Arduino IDE / PlatformIO
└── ESP32 Board Package (v2.0.14+)


---

## 📦 Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/uzankhan/CITYFLOW-IoT.git
cd CITYFLOW-IoT

---

2. Install Required Libraries (Arduino IDE)
Go to Sketch → Include Library → Manage Libraries and install:

LiquidCrystal I2C by Frank de Brabander

DHT sensor library by Adafruit

3. Configure ESP32 Board
Board: ESP32 Dev Module

Port: Select your COM port

Upload Speed: 115200

4. Upload the Code
Connect ESP32 via USB

Open CITYFLOW-IoT.ino

Click Upload

![Uploading deepseek_mermaid_20260829_0af329.svg…]()

📊 Real-World Applications
Use Case	Description
Smart Cities	Energy-efficient street lighting systems
Industrial Automation	Automated lighting in warehouses
Home Automation	Smart garage/driveway lighting
Environmental Monitoring	Gas leak detection in industrial zones
Security Systems	Motion-triggered surveillance integration
🔧 Troubleshooting Common Issues
Problem	Solution
LCD Not Displaying	Check I2C address (0x27 or 0x3F) & contrast potentiometer
5V Pin Not Working	Use external 5V 2A power supply
HC-SR04 Not Reading	Add voltage divider on ECHO pin (1kΩ+2kΩ)
DHT11 Reading Failed	Check DATA pin wiring & pull-up resistor
ESP32 Not Uploading	Press BOOT button while uploading
Relay Not Triggering	Check relay module is active-low or active-high type
🔬 Future Enhancements
□ Wi-Fi Connectivity — Send data to cloud (AWS/Azure/ThingSpeak)
□ Mobile App — Control and monitor via React Native app
□ Blynk Integration — Real-time dashboard & mobile notifications
□ AI/ML — Predictive maintenance using historical sensor data
□ LoRaWAN — Long-range communication for remote deployments
□ Solar Power — Solar panel integration for off-grid operation
🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create a new branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE file for more information.
