# 📦 Object Detection: Kit Type Verification System

This project is a real-time object detection and classification system for verifying different types of kits on a production line. It supports both **Jetson Nano** and **Windows** platforms and uses **IDS uEye Cameras** for image acquisition.

## 🔧 Features

- Real-time object detection using pre-trained models
- Kit type classification
- Compatible with **Jetson Nano** and **Windows**
- Camera input via **IDS uEye cameras**
- MQTT integration for data publishing
- Image processing with OpenCV
- GPIO control for industrial signaling (Jetson only)

---

## 📥 Requirements

- Python >= 3.6
- IDS uEye Software Suite
- Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📷 Camera Setup: IDS uEye

This project uses **IDS uEye** cameras (e.g., UI-358xLE) for high-quality and low-latency image capture.

### ✅ Requirements

- [IDS Software Suite](https://en.ids-imaging.com/download-ueye.html) (Windows/Linux)
- `pyueye` Python package for accessing camera in Linux

### 🖥 Windows Setup

1. Install IDS Software Suite
2. Use uEye Cockpit to test and configure the camera
3. Run the project script — camera is detected automatically

### 🤖 Jetson Nano Setup

1. Install uEye Software Suite (Linux ARM64 version)
2. Install Python SDK:

```bash
sudo apt install libudev-dev
pip install pyueye
```

3. Connect camera via USB
4. Use `lsusb` to check camera detection
5. Run the project

---

## 🚀 How to Run

### On Jetson Nano:

```bash
python3 main.py --platform jetson
```

### On Windows:

```bash
python main.py --platform windows
```

> Note: Make sure the camera is connected and drivers are correctly installed.

---

## 📡 MQTT Integration

The project sends results (kit type, image status, timestamp) to an MQTT broker. Configure `mqtt_config.json` to match your broker settings.

---

## ⚡ GPIO Control (Jetson only)

Jetson Nano can control output signals via GPIO to trigger other devices or indicators based on classification results.

---

## 🧪 Testing and Calibration

You can test the camera and detection results using the `test_camera.py` and `test_detection.py` scripts.

---

## 📝 Summary

This system provides an edge-computing solution for verifying kit types on production lines using machine vision. It is designed to be lightweight for Jetson Nano while retaining flexibility to run on Windows. IDS uEye cameras offer reliable and configurable image input. The system is ideal for factories needing real-time verification and simple integration into existing workflows.

---

## 📂 Repository Structure

```
├── main.py                # Entry point
├── detection/             # Object detection logic
├── camera/                # Camera handling (UEye integration)
├── gpio/                  # Jetson GPIO control
├── mqtt/                  # MQTT communication
├── utils/                 # Helper functions
├── test_camera.py         # Camera test script
├── test_detection.py      # Detection test script
└── README.md
```

---

## 🛠 Author

Developed by [nrefi321](https://github.com/nrefi321)
