# DogLog Enhanced - Real-Time Log Anomaly Detector 🐾

DogLog Enhanced là phiên bản cải tiến của công cụ giám sát log thời gian thực, được thiết kế với kiến trúc module hóa và nhiều tính năng nâng cao để phát hiện các mối đe dọa bảo mật.

## ✨ Tính năng mới

### 🔍 **Phát hiện bất thường nâng cao**
- **Brute Force Detection**: Phát hiện tấn công brute force từ cùng một IP
- **Distributed Attack Detection**: Phát hiện tấn công phân tán từ nhiều IP
- **User-based Anomaly**: Theo dõi hoạt động bất thường của user
- **Error Threshold Monitoring**: Giám sát ngưỡng lỗi hệ thống

### 🚨 **Hệ thống cảnh báo đa dạng**
- **Console Alerts**: Cảnh báo màu sắc trên terminal
- **Email Alerts**: Gửi cảnh báo qua email (có thể cấu hình)
- **Auto-blocking**: Tự động chặn IP tấn công (tùy chọn)
- **Alert History**: Lưu trữ lịch sử cảnh báo

### 📊 **Thống kê và báo cáo**
- **Real-time Statistics**: Thống kê thời gian thực
- **Event Tracking**: Theo dõi số lượng event, IP, user
- **Alert Export**: Xuất cảnh báo ra file JSON
- **Performance Metrics**: Đo lường hiệu suất hệ thống

### ⚙️ **Cấu hình linh hoạt**
- **JSON Configuration**: Cấu hình qua file JSON
- **Modular Architecture**: Kiến trúc module dễ mở rộng
- **Environment Variables**: Hỗ trợ biến môi trường
- **Logging System**: Hệ thống logging tích hợp

## 🏗️ Kiến trúc mới

```
DogLog Enhanced/
├── config.py              # Cấu hình tập trung
├── detector.py            # Module phát hiện bất thường
├── alerts.py              # Hệ thống cảnh báo
├── logdog_enhanced.py     # Script chính cải tiến
├── requirements.txt       # Dependencies
├── doglog_config.json     # Cấu hình JSON
├── test_doglog.py         # Unit tests
└── README_ENHANCED.md     # Tài liệu này
```

## 🚀 Cài đặt

### 1. **Cài đặt dependencies**

```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. **Cấu hình (tùy chọn)**

Chỉnh sửa file `doglog_config.json` để tùy chỉnh:
- Ngưỡng cảnh báo
- Cấu hình email
- Danh sách IP whitelist/blacklist
- Cài đặt hiển thị

## 📖 Sử dụng

### **Cơ bản**

```bash
# Giám sát tất cả log mặc định
sudo python3 logdog_enhanced.py --all

# Giám sát log cụ thể
sudo python3 logdog_enhanced.py --logs /var/log/auth.log /var/log/syslog

# Tùy chỉnh window và threshold
sudo python3 logdog_enhanced.py --window 10 --threshold 7 --all
```

### **Nâng cao**

```bash
# Tự động chặn IP tấn công
sudo python3 logdog_enhanced.py --all --auto-block

# Xuất cảnh báo ra file
sudo python3 logdog_enhanced.py --all --export alerts.json

# Chạy với cấu hình tùy chỉnh
sudo python3 logdog_enhanced.py --config custom_config.json --all
```

## 🔧 Cấu hình

### **File cấu hình JSON**

```json
{
  "monitoring": {
    "default_window_minutes": 5,
    "default_error_threshold": 5,
    "log_files": ["/var/log/auth.log", "/var/log/syslog"]
  },
  "alerts": {
    "auto_block": false,
    "email_enabled": false,
    "thresholds": {
      "brute_force": 10,
      "suspicious_ip": 5
    }
  },
  "security": {
    "whitelist_ips": ["192.168.1.1"],
    "blacklist_ips": [],
    "rate_limit_per_minute": 60
  }
}
```

### **Biến môi trường**

```bash
export DOGLOG_CONFIG_FILE="/path/to/config.json"
export DOGLOG_LOG_LEVEL="DEBUG"
export DOGLOG_AUTO_BLOCK="true"
```

## 🧪 Testing

### **Chạy unit tests**

```bash
python3 -m unittest test_doglog.py -v
```

### **Test với log giả**

```bash
# Tạo log test
echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR Test error message" | sudo tee -a /var/log/test.log

# Chạy DogLog với log test
sudo python3 logdog_enhanced.py --logs /var/log/test.log
```

## 📊 Ví dụ output

```
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

👀 Monitoring logs: /var/log/auth.log, /var/log/syslog, /var/log/messages
Press Ctrl+C to stop

[AUTH FAIL] 14:30:15 - Failed password for user admin from 192.168.1.100
[AUTH OK]   14:30:20 - Accepted password for user admin from 192.168.1.101

📊 STATISTICS
Total Events: 15
Unique IPs: 3
Unique Users: 2
Window Size: 5.0 minutes
Recent Alerts: 1

🚨 RECENT ALERTS
  2024-01-15T14:30:15 - brute_force

🚨 BRUTE FORCE ATTACK DETECTED 🚨
Time: 2024-01-15 14:30:15
Source: /var/log/auth.log
IP Address: 192.168.1.100
Failed Attempts: 12
Threshold: 10
Action Required: Consider blocking IP 192.168.1.100
```

## 🔒 Bảo mật

### **Tính năng bảo mật**

- **Auto-blocking**: Tự động chặn IP tấn công
- **Rate Limiting**: Giới hạn số lượng kết nối
- **Whitelist/Blacklist**: Danh sách IP được phép/chặn
- **Alert Verification**: Xác minh cảnh báo trước khi thực hiện

### **Best Practices**

1. **Chạy với quyền root**: Cần thiết để đọc log và chặn IP
2. **Cấu hình email**: Thiết lập SMTP để nhận cảnh báo từ xa
3. **Monitoring**: Theo dõi log của DogLog để phát hiện vấn đề
4. **Backup**: Sao lưu cấu hình và lịch sử cảnh báo

## 🛠️ Troubleshooting

### **Vấn đề thường gặp**

1. **Permission denied**
   ```bash
   sudo python3 logdog_enhanced.py --all
   ```

2. **Module not found**
   ```bash
   pip install -r requirements.txt
   ```

3. **Log files not found**
   ```bash
   # Kiểm tra log files tồn tại
   ls -la /var/log/auth.log
   ```

4. **IP blocking failed**
   ```bash
   # Kiểm tra iptables
   sudo iptables -L
   ```

## 🤝 Đóng góp

### **Cách đóng góp**

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

### **Guidelines**

- Tuân thủ PEP 8 style guide
- Viết unit tests cho tính năng mới
- Cập nhật documentation
- Test trên nhiều môi trường

## 📄 License

MIT License - xem file `LICENSE` để biết chi tiết.

## 👨‍💻 Author

**DogLog Enhanced** được phát triển bởi **xyanua** với sự đóng góp từ cộng đồng.

---

**Lưu ý**: Phiên bản Enhanced này tương thích ngược với phiên bản gốc nhưng có thêm nhiều tính năng mới. Khuyến nghị sử dụng phiên bản Enhanced cho môi trường production. 