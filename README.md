
# DogLog - Real-Time Log Anomaly Detector 🐾

DogLog is a Python-based real-time log monitoring and anomaly detection tool designed for Linux systems. It watches important log files like `/var/log/auth.log`, `/var/log/syslog`, and `/var/log/messages` to detect suspicious patterns such as brute-force SSH attacks or authentication anomalies.

Created for defenders, sysadmins, and SOC analysts who want a simple but powerful alerting system for their logs.

---

## Features

- **Real-time multi-log monitoring:** Instantly detects changes in multiple log files simultaneously.
- **Sliding window anomaly detection:** Uses configurable time windows and error thresholds to spot bursts of suspicious activity.
- **Color-coded authentication events:** Authentication failures are highlighted in red, successes in green for quick visual scanning.
- **Optional auto-blocking:** Can prompt to block brute-force IPs (with confirmation) to help mitigate attacks.
- **Systemd compatible:** Easily runs as a background service and survives reboots.
- **Flexible command-line interface:** Customize log sources, detection thresholds, and more.
- **Lightweight & portable:** Minimal dependencies, suitable for servers, desktops, and Raspberry Pi.

---

## Requirements

- Python 3.6+
- Linux system with access to log files (e.g., `/var/log/auth.log`)
- Root privileges (required for IP blocking)

### Python Dependencies

You can install dependencies in two ways:

#### Recommended: Using a Virtual Environment (venv)

```bash
sudo apt update
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install watchdog termcolor
```

#### Or, install globally (not recommended on modern Linux):

```bash
pip3 install watchdog termcolor
```

---

## Installation

1. Clone the repository or download the script:

    ```bash
    git clone https://github.com/wsxyanua/DogLog.git
    cd logdog
    ```

2. Make it executable:

    ```bash
    chmod +x logdog.py
    ```

---

## Usage

### Basic Usage

Monitor default logs (auth.log, syslog, messages):

```bash
sudo python3 logdog.py
```

### Full Help Menu

Display all available options and usage examples:

```bash
python3 logdog.py --help
```

```text
usage: logdog.py [-h] [--window WINDOW] [--threshold THRESHOLD] [--logs LOGS [LOGS ...]] [--all] [--autoblock]

Real-time log anomaly detector and SSH brute-force monitor.

optional arguments:
  -h, --help            Show this help message and exit
  --window WINDOW       Sliding window size in minutes (default: 5)
  --threshold THRESHOLD Threshold for ERROR count to trigger anomaly (default: 5)
  --logs LOGS [LOGS ...]
                        Paths to specific log files to monitor
  --all                 Monitor common system logs (auth.log, syslog, messages)
  --autoblock           Prompt to auto-block brute-force IPs (optional confirmation)
```

---

## Example Commands

- **Monitor all default logs:**
    ```bash
    sudo python3 logdog.py --all
    ```

- **Monitor specific logs:**
    ```bash
    sudo python3 logdog.py --logs /var/log/auth.log /var/log/secure
    ```

- **Enable auto-blocking of brute-force IPs (with prompt):**
    ```bash
    sudo python3 logdog.py --all --autoblock
    ```

- **Customize detection window and threshold:**
    ```bash
    sudo python3 logdog.py --window 10 --threshold 7 --logs /var/log/auth.log
    ```

---

## Systemd Integration

To run LogDog as a background service:

1. Move the script:

    ```bash
    sudo mkdir -p /opt/logdog
    sudo mv logdog.py /opt/logdog/logdog.py
    sudo chmod +x /opt/logdog/logdog.py
    ```

2. Create a systemd service:

    ```ini
    # /etc/systemd/system/logdog.service
    [Unit]
    Description=LogDog - Real-time Log Anomaly Detector
    After=network.target

    [Service]
    Type=simple
    ExecStart=/usr/bin/python3 /opt/logdog/logdog.py --all
    Restart=on-failure
    User=root
    WorkingDirectory=/opt/logdog
    StandardOutput=journal
    StandardError=journal

    [Install]
    WantedBy=multi-user.target
    ```

3. Enable and start the service:

    ```bash
    sudo systemctl daemon-reexec
    sudo systemctl daemon-reload
    sudo systemctl enable logdog.service
    sudo systemctl start logdog.service
    ```

4. Monitor logs:

    ```bash
    sudo journalctl -u logdog -f
    ```

---

## Output Example

```text
ANOMALY DETECTED in /var/log/auth.log: 6 ERRORs in last 0:05:00 at 2025-05-25 16:40:12
[!] Authentication failure from IP: 192.168.1.100
[+] Successful login detected from IP: 192.168.1.42
```

---

## Troubleshooting

- **Permission denied:** Make sure you run DogLog with `sudo` to access protected log files.
- **No output:** Check that the log files exist and are being updated. Use the `--logs` option to specify custom log paths if needed.
- **Dependency errors:** Ensure you have activated your virtual environment (if used) and installed all dependencies.
- **Externally managed environment error:** Use a virtual environment as described above to avoid system Python restrictions on modern Linux distributions.

---

## Security Notice

- This tool requires root access for reading logs like `/var/log/auth.log` and for performing `iptables` blocking.
- The auto-block feature must be used carefully. Always confirm IPs before blocking or enable optional confirmation prompts.

---

## License

MIT License. See `LICENSE` file for details.

---

## Author

**DogLog** is written by **xyanua**.  
Contributions and pull requests are welcome!
