#!/usr/bin/env python3
"""
DogLog Enhanced - Real-Time Log Anomaly Detector
Enhanced version with better structure, multiple detection types, and improved alerting
"""

import os
import sys
import time
import argparse
import signal
from datetime import datetime
from typing import List, Dict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_modules.config import Config
from core_modules.detector import LogAnomalyDetector
from core_modules.alerts import AlertManager

class EnhancedLogHandler(FileSystemEventHandler):
    """Enhanced log file handler with better event processing"""
    
    def __init__(self, detector: LogAnomalyDetector, alert_manager: AlertManager, filepath: str):
        super().__init__()
        self.detector = detector
        self.alert_manager = alert_manager
        self.filepath = filepath
        self._open_log()
        self.line_count = 0
        
    def _open_log(self):
        """Open log file and seek to end"""
        try:
            self.logfile = open(self.filepath, 'r')
            self.logfile.seek(0, os.SEEK_END)
        except Exception as e:
            print(f"{Config.COLORS['RED']}[ERROR] Cannot open {self.filepath}: {e}{Config.COLORS['RESET']}")
            self.logfile = None

    def on_modified(self, event):
        """Handle file modification events"""
        if event.src_path == self.filepath and self.logfile:
            try:
                lines = self.logfile.readlines()
                for line in lines:
                    self._process_line(line.strip())
            except Exception as e:
                print(f"{Config.COLORS['RED']}[ERROR] Failed to read {self.filepath}: {e}{Config.COLORS['RESET']}")

    def _process_line(self, line: str):
        """Process a single log line"""
        if not line:
            return
            
        parsed = self.detector.parse_line(line)
        if not parsed:
            return
            
        timestamp, level, message, metadata = parsed
        self.detector.add_event(timestamp, level, metadata)
        self.line_count += 1
        
        # Display authentication events with colors
        self._display_auth_event(timestamp, level, message, metadata)
        
        # Check for anomalies
        has_anomaly, anomalies = self.detector.check_anomaly()
        if has_anomaly:
            self.alert_manager.send_alert(anomalies, self.filepath)

    def _display_auth_event(self, timestamp: datetime, level: str, message: str, metadata: Dict):
        """Display authentication events with appropriate colors"""
        timestamp_str = timestamp.strftime('%H:%M:%S')
        
        if "Failed" in message or "Invalid" in message:
            ip_info = f" from {metadata.get('ip', 'unknown')}" if metadata.get('ip') else ""
            print(f"{Config.COLORS['RED']}[AUTH FAIL] {timestamp_str} - {message}{ip_info}{Config.COLORS['RESET']}")
        elif "Accepted" in message or "session opened" in message:
            ip_info = f" from {metadata.get('ip', 'unknown')}" if metadata.get('ip') else ""
            print(f"{Config.COLORS['GREEN']}[AUTH OK]   {timestamp_str} - {message}{ip_info}{Config.COLORS['RESET']}")
        elif level == "ERROR":
            print(f"{Config.COLORS['YELLOW']}[ERROR]     {timestamp_str} - {message}{Config.COLORS['RESET']}")

def show_banner():
    """Display the DogLog banner"""
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
               Enhanced Real-time Log Anomaly Detector by xyanua.
"""
    print(f"{Config.COLORS['GREEN']}{banner}{Config.COLORS['RESET']}")

def show_statistics(detector: LogAnomalyDetector, alert_manager: AlertManager):
    """Display current statistics"""
    stats = detector.get_statistics()
    alerts = alert_manager.get_alert_history(5)
    
    print(f"\n{Config.COLORS['CYAN']}📊 STATISTICS{Config.COLORS['RESET']}")
    print(f"Total Events: {stats['total_events']}")
    print(f"Unique IPs: {stats['unique_ips']}")
    print(f"Unique Users: {stats['unique_users']}")
    print(f"Window Size: {stats['window_minutes']:.1f} minutes")
    print(f"Recent Alerts: {len(alerts)}")
    
    if alerts:
        print(f"\n{Config.COLORS['YELLOW']}🚨 RECENT ALERTS{Config.COLORS['RESET']}")
        for alert in alerts[-3:]:
            print(f"  {alert['timestamp']} - {alert['type']}")

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print(f"\n{Config.COLORS['YELLOW']}🛑 Shutting down DogLog...{Config.COLORS['RESET']}")
    sys.exit(0)

def monitor_logs(filepaths: List[str], window_minutes: int = 5, error_threshold: int = 5, 
                alert_config: Dict = None):
    """Monitor multiple log files with enhanced detection"""
    
    # Initialize components
    detector = LogAnomalyDetector(window_minutes, error_threshold)
    alert_manager = AlertManager(alert_config)
    observer = Observer()
    handlers = []

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create handlers for each log file
    for path in filepaths:
        if not os.path.isfile(path):
            print(f"{Config.COLORS['YELLOW']}[!] Warning: {path} does not exist or is not a file.{Config.COLORS['RESET']}")
            continue
            
        handler = EnhancedLogHandler(detector, alert_manager, path)
        handlers.append(handler)
        observer.schedule(handler, os.path.dirname(path), recursive=False)

    if not handlers:
        print(f"{Config.COLORS['RED']}[ERROR] No valid log files to monitor!{Config.COLORS['RESET']}")
        return

    # Start monitoring
    observer.start()
    print(f"\n{Config.COLORS['GREEN']}👀 Monitoring logs: {', '.join(filepaths)}{Config.COLORS['RESET']}")
    print(f"{Config.COLORS['BLUE']}Press Ctrl+C to stop{Config.COLORS['RESET']}")
    
    try:
        last_stats_time = time.time()
        while True:
            time.sleep(1)
            
            # Show statistics every 30 seconds
            if time.time() - last_stats_time > 30:
                show_statistics(detector, alert_manager)
                last_stats_time = time.time()
                
    except KeyboardInterrupt:
        print(f"\n{Config.COLORS['YELLOW']}🛑 Stopping monitoring...{Config.COLORS['RESET']}")
    finally:
        observer.stop()
        observer.join()
        
        # Final statistics
        show_statistics(detector, alert_manager)

def main():
    """Main entry point"""
    show_banner()

    parser = argparse.ArgumentParser(
        description="🔍 DogLog Enhanced - Real-time Log Anomaly Detector",
        epilog="""
Examples:
  python3 logdog_enhanced.py --all
  python3 logdog_enhanced.py --logs /var/log/auth.log /var/log/syslog
  python3 logdog_enhanced.py --window 10 --threshold 7 --auto-block

Features:
  --window     Sliding time window in minutes (default: 5)
  --threshold  Error threshold before triggering anomaly (default: 5)
  --logs       Specific log file paths to monitor
  --all        Monitor all standard Linux logs
  --auto-block Automatically block brute force IPs
  --export     Export alerts to JSON file
""",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--window", type=int, default=Config.DEFAULT_WINDOW_MINUTES,
                        help=f"Sliding time window in minutes (default: {Config.DEFAULT_WINDOW_MINUTES})")
    parser.add_argument("--threshold", type=int, default=Config.DEFAULT_ERROR_THRESHOLD,
                        help=f"Error threshold before triggering anomaly (default: {Config.DEFAULT_ERROR_THRESHOLD})")
    parser.add_argument("--logs", nargs='+',
                        help="Paths to specific log files to monitor")
    parser.add_argument("--all", action='store_true',
                        help="Enable monitoring of all common Linux log files")
    parser.add_argument("--auto-block", action='store_true',
                        help="Automatically block brute force IPs")
    parser.add_argument("--export", type=str,
                        help="Export alerts to JSON file")

    args = parser.parse_args()

    if not args.logs and not args.all:
        parser.print_help()
        sys.exit(1)

    # Determine log files to monitor
    if args.all:
        log_files = Config.get_log_files()
    else:
        log_files = args.logs

    # Alert configuration
    alert_config = {
        'auto_block': args.auto_block,
        'email_enabled': False,  # Can be enabled via config file
    }

    # Start monitoring
    monitor_logs(log_files, args.window, args.threshold, alert_config)

if __name__ == "__main__":
    main() 