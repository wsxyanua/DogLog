import re
import time
import os
import sys
import argparse
from collections import deque, Counter
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogAnomalyDetector:
    def __init__(self, window_minutes=5, error_threshold=5):
        self.window = timedelta(minutes=window_minutes)
        self.error_threshold = error_threshold
        self.events = deque()
        self.level_counts = Counter()

    def parse_line(self, line):
        # Format 1: Custom app logs — ISO format
        match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.*)', line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            level = match.group(2)
            message = match.group(3)
            return timestamp, level, message

        # Format 2: Syslog/SSH
        match = re.match(r'([A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2}) .*?sshd.*?: (.*)', line)
        if match:
            log_time = f"{datetime.now().year} {match.group(1)}"
            timestamp = datetime.strptime(log_time, '%Y %b %d %H:%M:%S')
            message = match.group(2)

            if "Failed" in message or "Invalid" in message:
                level = "ERROR"
            elif "Accepted" in message or "session opened" in message:
                level = "INFO"
            else:
                level = "DEBUG"

            return timestamp, level, message

        return None

    def add_event(self, timestamp, level):
        self.events.append((timestamp, level))
        self.level_counts[level] += 1
        self._evict_old_events(timestamp)

    def _evict_old_events(self, current_time):
        while self.events and (current_time - self.events[0][0]) > self.window:
            _, old_level = self.events.popleft()
            self.level_counts[old_level] -= 1

    def check_anomaly(self):
        error_count = self.level_counts.get('ERROR', 0)
        if error_count >= self.error_threshold:
            return True, error_count
        return False, error_count

class LogHandler(FileSystemEventHandler):
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

    def __init__(self, detector, filepath):
        super().__init__()
        self.detector = detector
        self.filepath = filepath
        self._open_log()

    def _open_log(self):
        self.logfile = open(self.filepath, 'r')
        self.logfile.seek(0, os.SEEK_END)

    def on_modified(self, event):
        if event.src_path == self.filepath:
            lines = self.logfile.readlines()
            for line in lines:
                parsed = self.detector.parse_line(line)
                if not parsed:
                    continue
                timestamp, level, message = parsed
                self.detector.add_event(timestamp, level)

                if "Failed" in message or "Invalid" in message:
                    print(f"{self.RED}[AUTH FAIL] {timestamp} - {message}{self.RESET}")
                elif "Accepted" in message or "session opened" in message:
                    print(f"{self.GREEN}[AUTH OK]   {timestamp} - {message}{self.RESET}")

                anomaly, error_count = self.detector.check_anomaly()
                if anomaly:
                    print(f"{self.RED}\n[!!] ANOMALY DETECTED in {self.filepath}: {error_count} ERRORs in last {self.detector.window} at {timestamp}\n{self.RESET}")

def monitor_logs(filepaths, window_minutes=5, error_threshold=5):
    detector = LogAnomalyDetector(window_minutes, error_threshold)
    observer = Observer()
    handlers = []

    for path in filepaths:
        if not os.path.isfile(path):
            print(f"[!] Warning: {path} does not exist or is not a file.")
            continue
        handler = LogHandler(detector, path)
        handlers.append(handler)
        observer.schedule(handler, os.path.dirname(path), recursive=False)

    observer.start()
    print(f"\n👀 Monitoring logs: {', '.join(filepaths)}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def show_banner():
    GREEN = '\033[92m'
    RESET = '\033[0m'

    banner = r"""
      __                      ____
     /\ \                    /\  _`\                     
     \ \ \        ___      __\ \ \/\ \     / \__         __
      \ \ \  __  / __`\  /'_ `\ \ \ \ \   (    @\___   /'_ `\   
       \ \ \L\ \/\ \L\ \/\ \L\ \ \ \_\ \  /          O/\ \L\ \  
        \ \____/\ \____/\ \____ \ \____/ /    (_____/ \ \____ \ 
         \/___/  \/___/  \/___L\ \/___/ /_____/    U   \/___L\ \
                           /\____/                       /\____/
                           \_/__/                        \_/__/ 
               Real-time Log Anomaly Detector by X3RX3S
"""
    print(f"{GREEN}{banner}{RESET}")

def get_all_default_logs():
    return [
        "/var/log/auth.log",
        "/var/log/syslog",
        "/var/log/messages",
        "/var/log/secure",
        "/var/log/faillog",
        "/var/log/kern.log",
        "/var/log/dmesg"
    ]

if __name__ == "__main__":
    show_banner()

    parser = argparse.ArgumentParser(
        description="🔍 LogDog - Real-time Log Anomaly Detector by X3RX3S. Insta @mindfuckerrrr",
        epilog="""
Examples:
  python3 logsentinel.py --all
  python3 logsentinel.py --logs /var/log/auth.log /var/log/syslog
  python3 logsentinel.py --window 10 --threshold 7 --logs /var/log/secure

Options:
  --window     Number of minutes to track errors in sliding window
  --threshold  Max ERRORs allowed before anomaly triggers
  --logs       Specific log file paths to monitor
  --all        Monitor all standard Linux logs at once
""",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--window", type=int, default=5,
                        help="Sliding time window in minutes (default: 5)")
    parser.add_argument("--threshold", type=int, default=5,
                        help="Number of ERROR events before triggering an anomaly (default: 5)")
    parser.add_argument("--logs", nargs='+',
                        help="Paths to specific log files to monitor (e.g. /var/log/auth.log)")
    parser.add_argument("--all", action='store_true',
                        help="Enable monitoring of all common Linux log files")

    args = parser.parse_args()

    if not args.logs and not args.all:
        parser.print_help()
        sys.exit(1)

    log_files = get_all_default_logs() if args.all else args.logs
    monitor_logs(log_files, args.window, args.threshold)
