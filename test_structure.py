#!/usr/bin/env python3
"""
Test script để kiểm tra cấu trúc DogLog Enhanced
"""

import os
import sys
import importlib

def test_imports():
    """Test import tất cả modules"""
    print("🔍 Testing imports...")
    
    try:
        # Test core modules
        from core_modules.config import Config
        print("✅ Config imported successfully")
        
        from core_modules.detector import LogAnomalyDetector
        print("✅ Detector imported successfully")
        
        from core_modules.alerts import AlertManager
        print("✅ Alerts imported successfully")
        
        # Test detector functionality
        detector = LogAnomalyDetector()
        print("✅ Detector instance created successfully")
        
        # Test config functionality
        log_files = Config.get_log_files()
        print(f"✅ Config.get_log_files() returned {len(log_files)} files")
        
        # Test alerts functionality
        alert_manager = AlertManager()
        print("✅ AlertManager instance created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_file_structure():
    """Test cấu trúc file"""
    print("\n📁 Testing file structure...")
    
    expected_dirs = [
        'core_modules',
        'configuration', 
        'testing',
        'deployment',
        'documentation',
        'legacy'
    ]
    
    expected_files = [
        'core_modules/config.py',
        'core_modules/detector.py',
        'core_modules/alerts.py',
        'core_modules/logdog_enhanced.py',
        'configuration/requirements.txt',
        'configuration/doglog_config.json',
        'testing/test_doglog.py',
        'deployment/install.sh',
        'documentation/README.md',
        'documentation/README_ENHANCED.md',
        'legacy/logdog.py',
        'README_STRUCTURE.md',
        'LICENSE'
    ]
    
    # Check directories
    for dir_name in expected_dirs:
        if os.path.isdir(dir_name):
            print(f"✅ Directory {dir_name} exists")
        else:
            print(f"❌ Directory {dir_name} missing")
            return False
    
    # Check files
    for file_path in expected_files:
        if os.path.isfile(file_path):
            print(f"✅ File {file_path} exists")
        else:
            print(f"❌ File {file_path} missing")
            return False
    
    return True

def test_configuration():
    """Test cấu hình"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from core_modules.config import Config
        
        # Test color codes
        assert 'RED' in Config.COLORS
        assert 'GREEN' in Config.COLORS
        assert 'RESET' in Config.COLORS
        print("✅ Color codes defined")
        
        # Test patterns
        assert 'iso_format' in Config.LOG_PATTERNS
        assert 'syslog_ssh' in Config.LOG_PATTERNS
        assert 'ip_address' in Config.LOG_PATTERNS
        print("✅ Log patterns defined")
        
        # Test thresholds
        assert 'brute_force' in Config.ALERT_THRESHOLDS
        assert 'suspicious_ip' in Config.ALERT_THRESHOLDS
        assert 'system_error' in Config.ALERT_THRESHOLDS
        print("✅ Alert thresholds defined")
        
        # Test log files
        log_files = Config.get_log_files()
        assert isinstance(log_files, list)
        print(f"✅ Log files discovery: {len(log_files)} files found")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_detector():
    """Test detector functionality"""
    print("\n🔍 Testing detector...")
    
    try:
        from core_modules.detector import LogAnomalyDetector
        
        detector = LogAnomalyDetector(window_minutes=5, error_threshold=3)
        
        # Test parsing
        test_line = "2024-01-15 10:30:45 ERROR Authentication failed for user admin"
        result = detector.parse_line(test_line)
        assert result is not None
        print("✅ Log parsing works")
        
        # Test event adding
        from datetime import datetime
        detector.add_event(datetime.now(), "ERROR", {"ip": "192.168.1.100"})
        assert len(detector.events) == 1
        print("✅ Event adding works")
        
        # Test statistics
        stats = detector.get_statistics()
        assert 'total_events' in stats
        assert 'unique_ips' in stats
        print("✅ Statistics generation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Detector test failed: {e}")
        return False

def test_alerts():
    """Test alerts functionality"""
    print("\n🚨 Testing alerts...")
    
    try:
        from core_modules.alerts import AlertManager
        
        alert_manager = AlertManager()
        
        # Test alert message creation
        alert_info = {
            'ip': '192.168.1.100',
            'failed_attempts': 15,
            'threshold': 10
        }
        
        message = alert_manager._create_alert_message('brute_force', alert_info, '/var/log/auth.log')
        assert 'BRUTE FORCE ATTACK DETECTED' in message
        assert '192.168.1.100' in message
        print("✅ Alert message creation works")
        
        # Test alert history
        history = alert_manager.get_alert_history()
        assert isinstance(history, list)
        print("✅ Alert history works")
        
        return True
        
    except Exception as e:
        print(f"❌ Alerts test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🏗️ Testing DogLog Enhanced Structure")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Configuration", test_configuration),
        ("Imports", test_imports),
        ("Detector", test_detector),
        ("Alerts", test_alerts)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Structure is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the structure.")
        return False

if __name__ == "__main__":
    # Add current directory to Python path
    sys.path.append('.')
    main() 