import re
import time
from collections import deque, Counter, defaultdict
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Optional
from core_modules.config import Config

class LogAnomalyDetector:
    """Enhanced anomaly detector with multiple detection types"""
    
    def __init__(self, window_minutes: int = 5, error_threshold: int = 5):
        self.window = timedelta(minutes=window_minutes)
        self.error_threshold = error_threshold
        self.events = deque()
        self.level_counts = Counter()
        self.ip_events = defaultdict(list)  # Track IP-based events
        self.user_events = defaultdict(list)  # Track user-based events
        
    def parse_line(self, line: str) -> Optional[Tuple[datetime, str, str, Dict]]:
        """Parse log line and extract timestamp, level, message, and metadata"""
        
        # Format 1: Custom app logs — ISO format
        match = re.match(Config.LOG_PATTERNS['iso_format'], line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
            level = match.group(2)
            message = match.group(3)
            metadata = self._extract_metadata(message)
            return timestamp, level, message, metadata

        # Format 2: Syslog/SSH
        match = re.match(Config.LOG_PATTERNS['syslog_ssh'], line)
        if match:
            log_time = f"{datetime.now().year} {match.group(1)}"
            timestamp = datetime.strptime(log_time, '%Y %b %d %H:%M:%S')
            message = match.group(2)
            metadata = self._extract_metadata(message)

            if "Failed" in message or "Invalid" in message:
                level = "ERROR"
            elif "Accepted" in message or "session opened" in message:
                level = "INFO"
            else:
                level = "DEBUG"

            return timestamp, level, message, metadata

        return None
    
    def _extract_metadata(self, message: str) -> Dict:
        """Extract metadata from log message"""
        metadata = {}
        
        # Extract IP addresses
        ip_match = re.search(Config.LOG_PATTERNS['ip_address'], message)
        if ip_match:
            metadata['ip'] = ip_match.group()
            
        # Extract usernames (common patterns)
        user_patterns = [
            r'user (\w+)',
            r'for (\w+) from',
            r'(\w+)@',
        ]
        
        for pattern in user_patterns:
            user_match = re.search(pattern, message)
            if user_match:
                metadata['user'] = user_match.group(1)
                break
                
        # Extract service/process
        service_patterns = [
            r'sshd\[(\d+)\]',
            r'(\w+)\[(\d+)\]',
        ]
        
        for pattern in service_patterns:
            service_match = re.search(pattern, message)
            if service_match:
                metadata['service'] = service_match.group(1)
                metadata['pid'] = service_match.group(2) if len(service_match.groups()) > 1 else None
                break
                
        return metadata

    def add_event(self, timestamp: datetime, level: str, metadata: Dict = None):
        """Add event to detector"""
        self.events.append((timestamp, level, metadata))
        self.level_counts[level] += 1
        
        # Track IP-based events
        if metadata and 'ip' in metadata:
            self.ip_events[metadata['ip']].append((timestamp, level))
            
        # Track user-based events  
        if metadata and 'user' in metadata:
            self.user_events[metadata['user']].append((timestamp, level))
            
        self._evict_old_events(timestamp)

    def _evict_old_events(self, current_time: datetime):
        """Remove old events outside the time window"""
        while self.events and (current_time - self.events[0][0]) > self.window:
            _, old_level, old_metadata = self.events.popleft()
            self.level_counts[old_level] -= 1
            
            # Clean up IP events
            if old_metadata and 'ip' in old_metadata:
                ip = old_metadata['ip']
                if ip in self.ip_events:
                    self.ip_events[ip] = [
                        (ts, lvl) for ts, lvl in self.ip_events[ip] 
                        if (current_time - ts) <= self.window
                    ]
                    if not self.ip_events[ip]:
                        del self.ip_events[ip]
                        
            # Clean up user events
            if old_metadata and 'user' in old_metadata:
                user = old_metadata['user']
                if user in self.user_events:
                    self.user_events[user] = [
                        (ts, lvl) for ts, lvl in self.user_events[user]
                        if (current_time - ts) <= self.window
                    ]
                    if not self.user_events[user]:
                        del self.user_events[user]

    def check_anomaly(self) -> Tuple[bool, Dict]:
        """Check for various types of anomalies"""
        anomalies = {}
        
        # Check error threshold
        error_count = self.level_counts.get('ERROR', 0)
        if error_count >= self.error_threshold:
            anomalies['error_threshold'] = {
                'type': 'error_threshold',
                'count': error_count,
                'threshold': self.error_threshold
            }
            
        # Check brute force attacks
        for ip, events in self.ip_events.items():
            error_events = [e for e in events if e[1] == 'ERROR']
            if len(error_events) >= Config.ALERT_THRESHOLDS['brute_force']:
                anomalies['brute_force'] = {
                    'type': 'brute_force',
                    'ip': ip,
                    'failed_attempts': len(error_events),
                    'threshold': Config.ALERT_THRESHOLDS['brute_force']
                }
                
        # Check suspicious user activity
        for user, events in self.user_events.items():
            error_events = [e for e in events if e[1] == 'ERROR']
            if len(error_events) >= 3:  # 3 failed attempts per user
                anomalies['suspicious_user'] = {
                    'type': 'suspicious_user',
                    'user': user,
                    'failed_attempts': len(error_events)
                }
                
        # Check multiple IPs in short time (potential distributed attack)
        if len(self.ip_events) >= Config.ALERT_THRESHOLDS['suspicious_ip']:
            total_errors = sum(len([e for e in events if e[1] == 'ERROR']) 
                             for events in self.ip_events.values())
            if total_errors >= 10:
                anomalies['distributed_attack'] = {
                    'type': 'distributed_attack',
                    'unique_ips': len(self.ip_events),
                    'total_errors': total_errors
                }
                
        return len(anomalies) > 0, anomalies

    def get_statistics(self) -> Dict:
        """Get current statistics"""
        return {
            'total_events': len(self.events),
            'level_counts': dict(self.level_counts),
            'unique_ips': len(self.ip_events),
            'unique_users': len(self.user_events),
            'window_minutes': self.window.total_seconds() / 60
        } 