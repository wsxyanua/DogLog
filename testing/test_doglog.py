#!/usr/bin/env python3
"""
Unit tests for DogLog Enhanced
"""

import unittest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import tempfile

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_modules.detector import LogAnomalyDetector
from core_modules.alerts import AlertManager
from core_modules.config import Config

class TestLogAnomalyDetector(unittest.TestCase):
    """Test cases for LogAnomalyDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = LogAnomalyDetector(window_minutes=5, error_threshold=3)
        
    def test_parse_iso_format(self):
        """Test parsing ISO format log lines"""
        line = "2024-01-15 10:30:45 ERROR Authentication failed for user admin"
        result = self.detector.parse_line(line)
        
        self.assertIsNotNone(result)
        timestamp, level, message, metadata = result
        self.assertEqual(level, "ERROR")
        self.assertIn("Authentication failed", message)
        
    def test_parse_syslog_format(self):
        """Test parsing syslog format"""
        line = "Jan 15 10:30:45 server sshd[1234]: Failed password for user admin from 192.168.1.100"
        result = self.detector.parse_line(line)
        
        self.assertIsNotNone(result)
        timestamp, level, message, metadata = result
        self.assertEqual(level, "ERROR")
        self.assertIn("Failed password", message)
        self.assertEqual(metadata.get('ip'), "192.168.1.100")
        self.assertEqual(metadata.get('user'), "admin")
        
    def test_parse_invalid_format(self):
        """Test parsing invalid log format"""
        line = "Invalid log line without timestamp"
        result = self.detector.parse_line(line)
        
        self.assertIsNone(result)
        
    def test_add_event(self):
        """Test adding events to detector"""
        timestamp = datetime.now()
        self.detector.add_event(timestamp, "ERROR", {"ip": "192.168.1.100"})
        
        self.assertEqual(len(self.detector.events), 1)
        self.assertEqual(self.detector.level_counts["ERROR"], 1)
        self.assertIn("192.168.1.100", self.detector.ip_events)
        
    def test_evict_old_events(self):
        """Test eviction of old events"""
        now = datetime.now()
        old_time = now - timedelta(minutes=10)
        
        # Add old event
        self.detector.add_event(old_time, "ERROR")
        
        # Add current event to trigger eviction
        self.detector.add_event(now, "INFO")
        
        # Old event should be evicted
        self.assertEqual(len(self.detector.events), 1)
        self.assertEqual(self.detector.level_counts["ERROR"], 0)
        
    def test_check_anomaly_error_threshold(self):
        """Test anomaly detection for error threshold"""
        # Add events below threshold
        for i in range(2):
            self.detector.add_event(datetime.now(), "ERROR")
            
        has_anomaly, anomalies = self.detector.check_anomaly()
        self.assertFalse(has_anomaly)
        
        # Add more events to exceed threshold
        for i in range(2):
            self.detector.add_event(datetime.now(), "ERROR")
            
        has_anomaly, anomalies = self.detector.check_anomaly()
        self.assertTrue(has_anomaly)
        self.assertIn('error_threshold', anomalies)
        
    def test_check_brute_force_anomaly(self):
        """Test brute force attack detection"""
        ip = "192.168.1.100"
        
        # Add failed attempts from same IP
        for i in range(Config.ALERT_THRESHOLDS['brute_force']):
            self.detector.add_event(datetime.now(), "ERROR", {"ip": ip})
            
        has_anomaly, anomalies = self.detector.check_anomaly()
        self.assertTrue(has_anomaly)
        self.assertIn('brute_force', anomalies)
        self.assertEqual(anomalies['brute_force']['ip'], ip)
        
    def test_get_statistics(self):
        """Test statistics generation"""
        self.detector.add_event(datetime.now(), "ERROR", {"ip": "192.168.1.100"})
        self.detector.add_event(datetime.now(), "INFO", {"ip": "192.168.1.101"})
        
        stats = self.detector.get_statistics()
        
        self.assertEqual(stats['total_events'], 2)
        self.assertEqual(stats['unique_ips'], 2)
        self.assertEqual(stats['level_counts']['ERROR'], 1)
        self.assertEqual(stats['level_counts']['INFO'], 1)

class TestAlertManager(unittest.TestCase):
    """Test cases for AlertManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.alert_manager = AlertManager()
        
    def test_create_alert_message(self):
        """Test alert message creation"""
        alert_info = {
            'ip': '192.168.1.100',
            'failed_attempts': 15,
            'threshold': 10
        }
        
        message = self.alert_manager._create_alert_message('brute_force', alert_info, '/var/log/auth.log')
        
        self.assertIn('BRUTE FORCE ATTACK DETECTED', message)
        self.assertIn('192.168.1.100', message)
        self.assertIn('15', message)
        
    def test_send_console_alert(self):
        """Test console alert sending"""
        message = "Test alert message"
        result = self.alert_manager._send_console_alert(message)
        
        self.assertTrue(result)
        
    @patch('subprocess.run')
    def test_block_ip_success(self, mock_run):
        """Test successful IP blocking"""
        mock_run.return_value.returncode = 1  # IP not already blocked
        mock_run.return_value = Mock(returncode=0)  # Block command succeeds
        
        result = self.alert_manager._block_ip("192.168.1.100")
        self.assertTrue(result)
        
    @patch('subprocess.run')
    def test_block_ip_already_blocked(self, mock_run):
        """Test blocking already blocked IP"""
        mock_run.return_value.returncode = 0  # IP already blocked
        
        result = self.alert_manager._block_ip("192.168.1.100")
        self.assertTrue(result)
        
    def test_get_alert_history(self):
        """Test alert history retrieval"""
        # Add some test alerts
        test_alert = {
            'timestamp': '2024-01-15T10:30:45',
            'type': 'test_alert',
            'data': {'test': 'data'},
            'source': '/var/log/test.log',
            'message': 'Test alert'
        }
        
        self.alert_manager.alert_history.append(test_alert)
        
        history = self.alert_manager.get_alert_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['type'], 'test_alert')
        
    def test_export_alerts(self):
        """Test alert export functionality"""
        # Add test alert
        test_alert = {
            'timestamp': '2024-01-15T10:30:45',
            'type': 'test_alert',
            'data': {'test': 'data'},
            'source': '/var/log/test.log',
            'message': 'Test alert'
        }
        
        self.alert_manager.alert_history.append(test_alert)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
            
        try:
            result = self.alert_manager.export_alerts(temp_file)
            self.assertTrue(result)
            
            # Verify file was created and contains data
            self.assertTrue(os.path.exists(temp_file))
            with open(temp_file, 'r') as f:
                content = f.read()
                self.assertIn('test_alert', content)
                
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)

class TestConfig(unittest.TestCase):
    """Test cases for Config class"""
    
    def test_get_log_files(self):
        """Test log file discovery"""
        log_files = Config.get_log_files()
        
        # Should return a list
        self.assertIsInstance(log_files, list)
        
        # Should only include existing files
        for log_file in log_files:
            self.assertTrue(os.path.isfile(log_file))
            
    def test_color_codes(self):
        """Test color code definitions"""
        self.assertIn('RED', Config.COLORS)
        self.assertIn('GREEN', Config.COLORS)
        self.assertIn('RESET', Config.COLORS)
        
    def test_pattern_definitions(self):
        """Test pattern definitions"""
        self.assertIn('iso_format', Config.LOG_PATTERNS)
        self.assertIn('syslog_ssh', Config.LOG_PATTERNS)
        self.assertIn('ip_address', Config.LOG_PATTERNS)
        
    def test_alert_thresholds(self):
        """Test alert threshold definitions"""
        self.assertIn('brute_force', Config.ALERT_THRESHOLDS)
        self.assertIn('suspicious_ip', Config.ALERT_THRESHOLDS)
        self.assertIn('system_error', Config.ALERT_THRESHOLDS)

if __name__ == '__main__':
    unittest.main() 