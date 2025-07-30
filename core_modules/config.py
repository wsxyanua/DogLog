import os
from typing import List, Dict, Any

class Config:
    """Configuration class for DogLog"""
    
    # Default settings
    DEFAULT_WINDOW_MINUTES = 5
    DEFAULT_ERROR_THRESHOLD = 5
    DEFAULT_LOG_LEVEL = "INFO"
    
    # Log file paths
    DEFAULT_LOG_FILES = [
        "/var/log/auth.log",
        "/var/log/syslog", 
        "/var/log/messages",
        "/var/log/secure",
        "/var/log/faillog",
        "/var/log/kern.log",
        "/var/log/wtmp",
        "/var/log/btmp",
        "/var/log/cron",
        "/var/log/dmesg"
    ]
    
    # Color codes
    COLORS = {
        'RED': '\033[91m',
        'GREEN': '\033[92m', 
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'MAGENTA': '\033[95m',
        'CYAN': '\033[96m',
        'RESET': '\033[0m'
    }
    
    # Pattern matching
    LOG_PATTERNS = {
        'iso_format': r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.*)',
        'syslog_ssh': r'([A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2}) .*?sshd.*?: (.*)',
        'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    }
    
    # Alert thresholds
    ALERT_THRESHOLDS = {
        'brute_force': 10,  # Failed attempts per window
        'suspicious_ip': 5,  # Different IPs in short time
        'system_error': 20   # System errors per window
    }
    
    @classmethod
    def get_log_files(cls) -> List[str]:
        """Get list of log files that exist"""
        existing_files = []
        for log_file in cls.DEFAULT_LOG_FILES:
            if os.path.isfile(log_file):
                existing_files.append(log_file)
        return existing_files 