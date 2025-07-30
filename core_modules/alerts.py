import json
import smtplib
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core_modules.config import Config

class AlertManager:
    """Manages different types of alerts"""
    
    def __init__(self, alert_config: Dict = None):
        self.alert_config = alert_config or {}
        self.alert_history = []
        
    def send_alert(self, anomaly_data: Dict, source_file: str) -> bool:
        """Send alert based on anomaly type"""
        try:
            alert_type = list(anomaly_data.keys())[0]
            alert_info = anomaly_data[alert_type]
            
            # Create alert message
            message = self._create_alert_message(alert_type, alert_info, source_file)
            
            # Store in history
            self.alert_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': alert_type,
                'data': alert_info,
                'source': source_file,
                'message': message
            })
            
            # Send based on type
            if alert_type == 'brute_force':
                return self._handle_brute_force_alert(alert_info, message)
            elif alert_type == 'distributed_attack':
                return self._handle_distributed_attack_alert(alert_info, message)
            elif alert_type == 'error_threshold':
                return self._handle_error_threshold_alert(alert_info, message)
            else:
                return self._send_console_alert(message)
                
        except Exception as e:
            print(f"{Config.COLORS['RED']}[ALERT ERROR] Failed to send alert: {e}{Config.COLORS['RESET']}")
            return False
    
    def _create_alert_message(self, alert_type: str, alert_info: Dict, source_file: str) -> str:
        """Create formatted alert message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if alert_type == 'brute_force':
            return f"""
🚨 BRUTE FORCE ATTACK DETECTED 🚨
Time: {timestamp}
Source: {source_file}
IP Address: {alert_info['ip']}
Failed Attempts: {alert_info['failed_attempts']}
Threshold: {alert_info['threshold']}
Action Required: Consider blocking IP {alert_info['ip']}
"""
        elif alert_type == 'distributed_attack':
            return f"""
🌐 DISTRIBUTED ATTACK DETECTED 🌐
Time: {timestamp}
Source: {source_file}
Unique IPs: {alert_info['unique_ips']}
Total Errors: {alert_info['total_errors']}
Action Required: Review firewall rules and consider rate limiting
"""
        elif alert_type == 'error_threshold':
            return f"""
⚠️ ERROR THRESHOLD EXCEEDED ⚠️
Time: {timestamp}
Source: {source_file}
Error Count: {alert_info['count']}
Threshold: {alert_info['threshold']}
Action Required: Investigate system errors
"""
        else:
            return f"Unknown alert type: {alert_type}"
    
    def _handle_brute_force_alert(self, alert_info: Dict, message: str) -> bool:
        """Handle brute force attack alerts"""
        print(f"{Config.COLORS['RED']}{message}{Config.COLORS['RESET']}")
        
        # Auto-block option
        if self.alert_config.get('auto_block', False):
            return self._block_ip(alert_info['ip'])
        
        return True
    
    def _handle_distributed_attack_alert(self, alert_info: Dict, message: str) -> bool:
        """Handle distributed attack alerts"""
        print(f"{Config.COLORS['MAGENTA']}{message}{Config.COLORS['RESET']}")
        
        # Could implement rate limiting or firewall rules here
        return True
    
    def _handle_error_threshold_alert(self, alert_info: Dict, message: str) -> bool:
        """Handle error threshold alerts"""
        print(f"{Config.COLORS['YELLOW']}{message}{Config.COLORS['RESET']}")
        return True
    
    def _send_console_alert(self, message: str) -> bool:
        """Send alert to console"""
        print(f"{Config.COLORS['RED']}{message}{Config.COLORS['RESET']}")
        return True
    
    def _block_ip(self, ip_address: str) -> bool:
        """Block IP address using iptables"""
        try:
            # Check if IP is already blocked
            check_cmd = f"iptables -C INPUT -s {ip_address} -j DROP"
            result = subprocess.run(check_cmd, shell=True, capture_output=True)
            
            if result.returncode == 0:
                print(f"{Config.COLORS['YELLOW']}IP {ip_address} is already blocked{Config.COLORS['RESET']}")
                return True
            
            # Block the IP
            block_cmd = f"iptables -A INPUT -s {ip_address} -j DROP"
            result = subprocess.run(block_cmd, shell=True, capture_output=True)
            
            if result.returncode == 0:
                print(f"{Config.COLORS['GREEN']}Successfully blocked IP {ip_address}{Config.COLORS['RESET']}")
                return True
            else:
                print(f"{Config.COLORS['RED']}Failed to block IP {ip_address}: {result.stderr.decode()}{Config.COLORS['RESET']}")
                return False
                
        except Exception as e:
            print(f"{Config.COLORS['RED']}Error blocking IP {ip_address}: {e}{Config.COLORS['RESET']}")
            return False
    
    def send_email_alert(self, message: str, subject: str = "DogLog Alert") -> bool:
        """Send email alert (if configured)"""
        if not self.alert_config.get('email_enabled', False):
            return False
            
        try:
            smtp_config = self.alert_config.get('smtp', {})
            
            msg = MIMEMultipart()
            msg['From'] = smtp_config.get('from_email')
            msg['To'] = smtp_config.get('to_email')
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(smtp_config.get('server'), smtp_config.get('port', 587))
            server.starttls()
            server.login(smtp_config.get('username'), smtp_config.get('password'))
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"{Config.COLORS['RED']}Failed to send email alert: {e}{Config.COLORS['RESET']}")
            return False
    
    def get_alert_history(self, limit: int = 10) -> List[Dict]:
        """Get recent alert history"""
        return self.alert_history[-limit:] if self.alert_history else []
    
    def export_alerts(self, filename: str) -> bool:
        """Export alert history to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.alert_history, f, indent=2)
            return True
        except Exception as e:
            print(f"{Config.COLORS['RED']}Failed to export alerts: {e}{Config.COLORS['RESET']}")
            return False 