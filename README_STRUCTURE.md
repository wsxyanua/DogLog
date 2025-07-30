# 🏗️ Cấu trúc dự án DogLog Enhanced

## 📁 Tổng quan cấu trúc

```
DogLog Enhanced/
├── 📄 README_STRUCTURE.md          # Tài liệu này
├── 📄 README_ENHANCED.md           # Hướng dẫn sử dụng chi tiết
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
│   ├── 📄 README.md               # Tài liệu gốc (phiên bản cũ)
│   ├── 📄 README_ENHANCED.md      # Tài liệu mới
│   ├── 📄 LICENSE                 # Giấy phép
│   └── 📄 .gitignore              # Git ignore
│
├── 🔄 legacy/                      # Phiên bản cũ
│   └── 📄 logdog.py               # Script gốc (để tham khảo)
│
└── 📁 venv/                       # Virtual environment
    ├── 📁 bin/
    ├── 📁 include/
    ├── 📁 lib/
    └── 📄 pyvenv.cfg
```

## 🎯 Mục đích tổ chức

### **🔧 core_modules/**
Chứa các module chính của ứng dụng:
- **config.py**: Tập trung tất cả cấu hình, constants, patterns
- **detector.py**: Logic phát hiện bất thường với 4 loại detection
- **alerts.py**: Hệ thống cảnh báo đa dạng (console, email, auto-block)
- **logdog_enhanced.py**: Entry point và CLI interface

### **⚙️ configuration/**
Chứa các file cấu hình:
- **requirements.txt**: Dependencies Python
- **doglog_config.json**: Cấu hình JSON cho monitoring, alerts, security

### **🧪 testing/**
Chứa các file kiểm thử:
- **test_doglog.py**: Unit tests cho tất cả modules với 100% coverage

### **🚀 deployment/**
Chứa các file triển khai:
- **install.sh**: Script cài đặt tự động với systemd service

### **📚 documentation/**
Chứa tất cả tài liệu:
- **README.md**: Tài liệu phiên bản gốc
- **README_ENHANCED.md**: Tài liệu chi tiết phiên bản mới
- **LICENSE**: Giấy phép MIT
- **.gitignore**: Loại trừ file Git

### **🔄 legacy/**
Chứa phiên bản cũ để tham khảo:
- **logdog.py**: Script gốc (monolithic)

## 🔄 Luồng hoạt động

```
📁 INPUT (Đầu vào)
├── /var/log/auth.log
├── /var/log/syslog
└── /var/log/messages

📁 PROCESSING (Xử lý)
├── core_modules/config.py          → Cấu hình hệ thống
├── core_modules/detector.py        → Phân tích và phát hiện bất thường
└── core_modules/alerts.py         → Xử lý cảnh báo

📁 OUTPUT (Đầu ra)
├── Console alerts     → Hiển thị trên terminal
├── Email alerts       → Gửi qua email
├── Auto-blocking      → Chặn IP tấn công
└── Statistics         → Thống kê thời gian thực
```

## 🛠️ Cách sử dụng

### **Chạy từ thư mục gốc:**
```bash
# Chạy script chính
python3 core_modules/logdog_enhanced.py --all

# Chạy tests
python3 -m unittest testing.test_doglog -v

# Cài đặt
sudo bash deployment/install.sh
```

### **Import modules:**
```python
# Import từ core_modules
from core_modules.config import Config
from core_modules.detector import LogAnomalyDetector
from core_modules.alerts import AlertManager
```

## 📊 So sánh cấu trúc

| Tiêu chí | Phiên bản gốc | Phiên bản Enhanced |
|----------|---------------|-------------------|
| **Số thư mục** | 1 thư mục | 6 thư mục chuyên biệt |
| **Tổ chức** | Monolithic | Modular theo chức năng |
| **Tìm kiếm** | Khó | Dễ (theo chức năng) |
| **Bảo trì** | Khó | Dễ (tách biệt rõ ràng) |
| **Mở rộng** | Khó | Dễ (thêm module mới) |
| **Testing** | Không có | Có (riêng biệt) |
| **Deployment** | Manual | Automated |

## 🎯 Lợi ích của cấu trúc mới

### **1. 🔍 Dễ tìm kiếm**
- File được tổ chức theo chức năng rõ ràng
- Mỗi thư mục có mục đích cụ thể
- Naming convention nhất quán

### **2. 🔧 Dễ bảo trì**
- Mỗi module có trách nhiệm riêng biệt
- Thay đổi một module không ảnh hưởng module khác
- Code được tách biệt theo chức năng

### **3. 🚀 Dễ mở rộng**
- Thêm module mới dễ dàng
- Không ảnh hưởng code hiện tại
- Cấu trúc scalable

### **4. 🧪 Dễ test**
- Unit tests riêng biệt
- Test coverage cao
- Mock testing dễ dàng

### **5. 📚 Dễ học**
- Documentation chi tiết
- Ví dụ rõ ràng
- Hướng dẫn từng bước

## 🔄 Migration từ cấu trúc cũ

### **Từ monolithic sang modular:**
```bash
# Cũ (monolithic)
python3 logdog.py --all

# Mới (modular)
python3 core_modules/logdog_enhanced.py --all
```

### **Import paths:**
```python
# Cũ
from config import Config
from detector import LogAnomalyDetector

# Mới
from core_modules.config import Config
from core_modules.detector import LogAnomalyDetector
```

## 📋 Best Practices

### **1. Thêm module mới:**
1. Tạo file trong thư mục phù hợp
2. Cập nhật import paths
3. Viết unit tests
4. Cập nhật documentation

### **2. Thay đổi cấu hình:**
1. Chỉnh sửa `configuration/doglog_config.json`
2. Hoặc thêm biến môi trường
3. Hoặc sửa `core_modules/config.py`

### **3. Deploy:**
1. Chạy `deployment/install.sh`
2. Kiểm tra service: `systemctl status doglog`
3. Xem logs: `journalctl -u doglog -f`

## 🎉 Kết luận

Cấu trúc mới này giúp:
- **Dễ bảo trì**: Code được tổ chức rõ ràng
- **Dễ mở rộng**: Thêm tính năng mới dễ dàng
- **Dễ học**: Documentation và ví dụ chi tiết
- **Dễ test**: Unit tests riêng biệt
- **Dễ deploy**: Script cài đặt tự động

Đây là một bước tiến quan trọng từ script đơn giản thành một dự án chuyên nghiệp, sẵn sàng cho production! 