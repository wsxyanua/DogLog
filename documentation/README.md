
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

**⚠️ Important:** Modern Linux distributions (Ubuntu 22.04+, Debian 12+, Kali Linux) have externally managed Python environments. Choose one of the following installation methods:

#### Method 1: Global Installation (Recommended for quick setup)

```bash
# Install dependencies globally
sudo pip3 install watchdog termcolor

# If you get "externally-managed-environment" error, use:
sudo pip3 install --break-system-packages watchdog termcolor
```

#### Method 2: Virtual Environment (Recommended for development)

```bash
# Create and activate virtual environment
sudo apt update
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install watchdog termcolor
```

---

## Installation

1. Clone the repository or download the script:

    ```bash
    git clone https://github.com/wsxyanua/DogLog.git
    cd DogLog
    ```

2. Make it executable:

    ```bash
    chmod +x logdog.py
    ```

---

## Usage

### ⚠️ Important: Running with sudo

DogLog requires root privileges to access system log files. However, when running with `sudo`, Python may not find your virtual environment. Use one of these methods:

#### Method 1: Global Dependencies (Simplest)

```bash
# Install dependencies globally first
sudo pip3 install watchdog termcolor

# Then run normally
sudo python3 logdog.py --all
```

#### Method 2: Virtual Environment with sudo

```bash
# If using virtual environment, run with full path
sudo -E env "PATH=$PATH" /path/to/venv/bin/python3 logdog.py --all
```

#### Method 3: Activate venv before sudo

```bash
# Activate virtual environment
source venv/bin/activate

# Run with sudo while preserving environment
sudo -E python3 logdog.py --all
```

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

## Testing the Installation

To verify DogLog is working correctly:

1. **Start SSH service (if not running):**
    ```bash
    sudo systemctl start ssh
    ```

2. **Create test log events:**
    ```bash
    # Try SSH connections to generate auth logs
    ssh -o ConnectTimeout=1 -o BatchMode=yes test@localhost
    
    # Or create a test log file
    sudo touch /var/log/test.log
    echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR Test error message" | sudo tee -a /var/log/test.log
    ```

3. **Run DogLog and observe output:**
    ```bash
    sudo python3 logdog.py --logs /var/log/test.log
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
      __                      ____
     /\ \                    /\  _`\                     
     \ \ \        ___      __\ \ \/\ \     / \__         __
      \ \ \  __  / __`\  /'_ `\ \ \ \ \   (    @\___   /'_ `\   
       \ \ \L\ \/\ \L\ \/\ \L\ \ \ \_\ \  /          O/\ \L\ \  
        \ \____/\ \____/\ \____ \ \____/ /    (_____/ \ \____ \ 
         \/___/  \/___/  \/___L\ \/___/ /_____/    U   \/___L\ \
                           /\____/                       /\____/
                           \_/__/                        \_/__/ 
               Real-time Log Anomaly Detector by xyanua.

👀 Monitoring logs: /var/log/auth.log, /var/log/syslog, /var/log/messages

[!] ANOMALY DETECTED in /var/log/auth.log: 6 ERRORs in last 0:05:00 at 2025-07-28 03:32:18
[!] Authentication failure from IP: 192.168.1.100
[+] Successful login detected from IP: 192.168.1.42
```

---

## Troubleshooting

### Common Issues and Solutions

- **`ModuleNotFoundError: No module named 'watchdog'`**
  - **Solution:** Install dependencies globally: `sudo pip3 install watchdog termcolor`
  - **Alternative:** Use virtual environment with full path: `sudo -E env "PATH=$PATH" /path/to/venv/bin/python3 logdog.py --all`

- **`Permission denied`**
  - **Solution:** Make sure you run DogLog with `sudo` to access protected log files

- **`No such file or directory` for log files**
  - **Solution:** Check if log files exist: `sudo ls -la /var/log/auth.log`
  - **Alternative:** Create test log file: `sudo touch /var/log/test.log`

- **`Externally managed environment error`**
  - **Solution:** Use `sudo pip3 install --break-system-packages watchdog termcolor`
  - **Alternative:** Use virtual environment as described above

- **No output from DogLog**
  - **Solution:** Check that log files exist and are being updated
  - **Test:** Create test events: `ssh -o ConnectTimeout=1 -o BatchMode=yes test@localhost`

- **SSH service not running**
  - **Solution:** Start SSH service: `sudo systemctl start ssh`

### Modern Linux Distribution Notes

- **Ubuntu 22.04+, Debian 12+, Kali Linux:** Use global installation or virtual environment with proper sudo handling
- **Systemd-based systems:** Logs may be in journald instead of traditional log files
- **Check available logs:** `sudo journalctl -u ssh --since "5 minutes ago"`

---

## Security Notice

- This tool requires root access for reading logs like `/var/log/auth.log` and for performing `iptables` blocking.
- The auto-block feature must be used carefully. Always confirm IPs before blocking or enable optional confirmation prompts.
- Consider running in a controlled environment when testing auto-blocking features.

---

## License

MIT License. See `LICENSE` file for details.

---

## Author

**DogLog** is written by **xyanua**.  
Contributions and pull requests are welcome!
