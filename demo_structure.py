#!/usr/bin/env python3
"""
Demo script để hiển thị cấu trúc và tính năng DogLog Enhanced
"""

import sys
import os

def show_structure():
    """Hiển thị cấu trúc dự án"""
    print("🏗️ DogLog Enhanced Structure")
    print("=" * 50)
    
    structure = """
DogLog Enhanced/
├── 📄 README_STRUCTURE.md          # Tài liệu này
├── 📄 LICENSE                      # Giấy phép MIT
├── 📄 .gitignore                   # Loại trừ file Git
│
├── 🔧 core_modules/                # Modules chính
│   ├── 📄 config.py                # Cấu hình tập trung
│   ├── 📄 detector.py              # Phát hiện bất thường
│   ├── 📄 alerts.py                # Hệ thống cảnh báo
│   └── 📄 logdog_enhanced.py       # Script chính
│
├── ⚙️ configuration/               # Cấu hình
│   ├── 📄 requirements.txt         # Dependencies Python
│   └── 📄 doglog_config.json      # Cấu hình JSON
│
├── 🧪 testing/                     # Kiểm thử
│   └── 📄 test_doglog.py          # Unit tests
│
├── 🚀 deployment/                  # Triển khai
│   └── 📄 install.sh              # Script cài đặt tự động
│
├── 📚 documentation/               # Tài liệu
│   ├── 📄 README.md               # Tài liệu gốc
│   ├── 📄 README_ENHANCED.md      # Tài liệu mới
│
├── 🔄 legacy/                      # Phiên bản cũ
│   └── 📄 logdog.py               # Script gốc
│
└── 📁 venv/                       # Virtual environment
    """
    
    print(structure)

def show_features():
    """Hiển thị tính năng mới"""
    print("\n✨ Enhanced Features")
    print("=" * 50)
    
    features = """
🔍 Phát hiện bất thường nâng cao:
   • Brute Force Detection
   • Distributed Attack Detection  
   • User-based Anomaly
   • Error Threshold Monitoring

🚨 Hệ thống cảnh báo đa dạng:
   • Console Alerts với màu sắc
   • Email Alerts (có thể cấu hình)
   • Auto-blocking IP tấn công
   • Alert History và Export

📊 Thống kê và báo cáo:
   • Real-time Statistics
   • Event Tracking (IP, user, service)
   • Performance Metrics
   • Alert Export to JSON

⚙️ Cấu hình linh hoạt:
   • JSON Configuration
   • Modular Architecture
   • Environment Variables
   • Logging System
    """
    
    print(features)

def show_usage():
    """Hiển thị cách sử dụng"""
    print("\n🛠️ Usage Examples")
    print("=" * 50)
    
    usage = """
# Chạy từ thư mục gốc:
python3 core_modules/logdog_enhanced.py --all

# Chạy với tùy chỉnh:
python3 core_modules/logdog_enhanced.py --window 10 --threshold 7 --auto-block

# Chạy tests:
python3 -m unittest testing.test_doglog -v

# Cài đặt:
sudo bash deployment/install.sh

# Import modules:
from core_modules.config import Config
from core_modules.detector import LogAnomalyDetector
from core_modules.alerts import AlertManager
    """
    
    print(usage)

def show_comparison():
    """Hiển thị so sánh với phiên bản gốc"""
    print("\n📊 Comparison with Original Version")
    print("=" * 50)
    
    comparison = """
| Tiêu chí | Phiên bản gốc | Phiên bản Enhanced |
|----------|---------------|-------------------|
| **Số file** | 3 files | 13+ files |
| **Cấu trúc** | Monolithic | Modular |
| **Cấu hình** | Hard-coded | JSON + ENV |
| **Testing** | Không có | Comprehensive |
| **Installation** | Manual | Automated |
| **Documentation** | Basic | Detailed |
| **Maintainability** | Khó | Dễ |
    """
    
    print(comparison)

def test_imports():
    """Test import các modules"""
    print("\n🧪 Testing Imports")
    print("=" * 50)
    
    try:
        # Add current directory to path
        sys.path.append('.')
        
        # Test imports
        from core_modules.config import Config
        print("✅ Config imported successfully")
        
        from core_modules.detector import LogAnomalyDetector
        print("✅ Detector imported successfully")
        
        from core_modules.alerts import AlertManager
        print("✅ Alerts imported successfully")
        
        # Test functionality
        detector = LogAnomalyDetector()
        print("✅ Detector instance created")
        
        alert_manager = AlertManager()
        print("✅ AlertManager instance created")
        
        log_files = Config.get_log_files()
        print(f"✅ Found {len(log_files)} log files")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    """Main function"""
    print("🐕 DogLog Enhanced - Structure Demo")
    print("=" * 60)
    
    # Show structure
    show_structure()
    
    # Show features
    show_features()
    
    # Show usage
    show_usage()
    
    # Show comparison
    show_comparison()
    
    # Test imports
    if test_imports():
        print("\n🎉 Demo completed successfully!")
        print("✅ Structure is working correctly")
        print("✅ All modules can be imported")
        print("✅ Ready for development and deployment")
    else:
        print("\n⚠️ Demo completed with issues")
        print("❌ Some modules failed to import")
        print("⚠️ Please check the structure")

if __name__ == "__main__":
    main() 