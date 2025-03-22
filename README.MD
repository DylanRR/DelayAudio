# DelayAudio

DelayAudio is a Python-based project designed to manage audio and video devices, including webcams, microphones, speakers, and Phidget controllers. It provides functionality for delayed audio playback, multi-monitor video display, and hardware interaction using Phidgets.

## Features
- Audio delay functionality for microphones and speakers.
- Multi-monitor video display with webcam feeds.
- Phidget button interaction for triggering audio and video events.
- Configuration management for hardware devices.
- UI for configuring devices and advanced properties.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/DylanRR/DelayAudio
cd DelayAudio
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment
- On **Linux/macOS**:
  ```bash
  source .venv/bin/activate
  ```

### 4. Install Dependencies
Install the required Python packages using `pip3`:

```bash
pip3 install -r requirements.txt
```

---

## Usage

### 1. Configuration
The project uses a configuration file located at `config/config.json`. Ensure the file is properly set up with your hardware details. If the file is missing or invalid, it can be rebuilt using the `ConfigurationLoader` class.

### 2. Running the Main Application
To start the main application, run:

```bash
python3 src/main.py
```

### 3. Testing Individual Components
You can test individual components using the scripts in the `testing` and `utils` directories. For example:
- Test webcams:
  ```bash
  python3 devTooling/scanWebcams.py
  ```
- Test audio devices:
  ```bash
  python3 devTooling/scanAudio.py
  ```
- Test Phidgets:
  ```bash
  python3 devTooling/scanPhidgets.py
  ```

---

## Project Structure
- **`src/`**: Contains the main application logic.
- **`utils/`**: Utility scripts for scanning and managing hardware devices.
- **`devTooling/`**: Development tools for testing and debugging.
- **`config/`**: Configuration management and default settings.
- **`archive/`**: Archived scripts for reference or legacy functionality.
- **`testing/`**: Scripts for testing individual components.

---

## Troubleshooting

### Common Issues
1. **Device Unavailable**: Ensure the device is not being used by another application.
2. **Permissions**: On Linux, you may need to run the scripts with `sudo` or configure udev rules for device access.
3. **Dependencies**: Ensure all dependencies are installed correctly using the `requirements.txt` file.

### Debugging
Enable debugging by checking the `debug.txt` file for logs or running scripts with verbose output.

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

---

## Acknowledgments
- [OpenCV](https://opencv.org/) for video processing.
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for audio handling.
- [Phidget22](https://www.phidgets.com/) for hardware interaction.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the configuration UI.