#!/bin/bash

# DogLog Enhanced Installer
# Tự động cài đặt và cấu hình DogLog Enhanced

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${GREEN}"
cat << "EOF"
      __                      ____
     /\ \                    /\  _`\                     
     \ \ \        ___      __\ \ \/\ \     / \__         __
      \ \ \  __  / __`\  /'_ `\ \ \ \ \   (    @\___   /'_ `\   
       \ \ \L\ \/\ \L\ \/\ \L\ \ \ \_\ \  /          O/\ \L\ \  
        \ \____/\ \____/\ \____ \ \____/ /    (_____/ \ \____ \ 
         \/___/  \/___/  \/___L\ \/___/ /_____/    U   \/___L\ \
                           /\____/                       /\____/
                           \_/__/                        \_/__/ 
               Enhanced Real-time Log Anomaly Detector Installer
EOF
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${YELLOW}⚠️  Warning: Running as root. This is normal for installation.${NC}"
else
   echo -e "${RED}❌ Error: This script must be run as root (use sudo)${NC}"
   exit 1
fi

# Function to print status
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check system requirements
print_status "Checking system requirements..."

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3.6+ first."
    exit 1
fi

# Check if pip is available
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
else
    print_error "pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install system dependencies
print_status "Installing system dependencies..."

# Update package list
apt-get update -qq

# Install required packages
apt-get install -y python3-venv python3-pip iptables-persistent

print_success "System dependencies installed"

# Create installation directory
INSTALL_DIR="/opt/doglog"
print_status "Creating installation directory: $INSTALL_DIR"

mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Copy files
print_status "Copying DogLog Enhanced files..."

# Copy core modules
mkdir -p $INSTALL_DIR/core_modules
cp -f /home/logntsu/DogLog/core_modules/*.py $INSTALL_DIR/core_modules/

# Copy configuration
mkdir -p $INSTALL_DIR/configuration
cp -f /home/logntsu/DogLog/configuration/* $INSTALL_DIR/configuration/

# Copy testing
mkdir -p $INSTALL_DIR/testing
cp -f /home/logntsu/DogLog/testing/*.py $INSTALL_DIR/testing/

# Copy documentation
mkdir -p $INSTALL_DIR/documentation
cp -f /home/logntsu/DogLog/documentation/* $INSTALL_DIR/documentation/

# Copy legacy
mkdir -p $INSTALL_DIR/legacy
cp -f /home/logntsu/DogLog/legacy/*.py $INSTALL_DIR/legacy/

# Copy deployment
mkdir -p $INSTALL_DIR/deployment
cp -f /home/logntsu/DogLog/deployment/* $INSTALL_DIR/deployment/

# Make executable
chmod +x $INSTALL_DIR/core_modules/logdog_enhanced.py

print_success "Files copied successfully"

# Create virtual environment
print_status "Creating Python virtual environment..."

python3 -m venv $INSTALL_DIR/venv
source $INSTALL_DIR/venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."

pip install --upgrade pip
pip install -r configuration/requirements.txt

print_success "Python dependencies installed"

# Create systemd service
print_status "Creating systemd service..."

cat > /etc/systemd/system/doglog.service << EOF
[Unit]
Description=DogLog Enhanced - Real-time Log Anomaly Detector
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
Group=root
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/core_modules/logdog_enhanced.py --all
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment=PYTHONPATH=$INSTALL_DIR

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

print_success "Systemd service created"

# Create configuration directory
CONFIG_DIR="/etc/doglog"
mkdir -p $CONFIG_DIR

# Copy configuration
cp $INSTALL_DIR/configuration/doglog_config.json $CONFIG_DIR/

print_success "Configuration copied to $CONFIG_DIR"

# Create log directory
LOG_DIR="/var/log/doglog"
mkdir -p $LOG_DIR
chmod 755 $LOG_DIR

print_success "Log directory created: $LOG_DIR"

# Create symlink for easy access
ln -sf $INSTALL_DIR/core_modules/logdog_enhanced.py /usr/local/bin/doglog

print_success "Symlink created: /usr/local/bin/doglog"

# Set permissions
chown -R root:root $INSTALL_DIR
chmod -R 755 $INSTALL_DIR
chmod 644 $CONFIG_DIR/doglog_config.json

print_success "Permissions set correctly"

# Test installation
print_status "Testing installation..."

# Test Python imports
if $INSTALL_DIR/venv/bin/python -c "import watchdog, termcolor, psutil, colorama; print('All dependencies imported successfully')" 2>/dev/null; then
    print_success "Python dependencies test passed"
else
    print_error "Python dependencies test failed"
    exit 1
fi

# Test configuration
if $INSTALL_DIR/venv/bin/python -c "from core_modules.config import Config; print('Configuration loaded successfully')" 2>/dev/null; then
    print_success "Configuration test passed"
else
    print_error "Configuration test failed"
    exit 1
fi

print_success "Installation test completed"

# Create uninstall script
cat > $INSTALL_DIR/uninstall.sh << 'EOF'
#!/bin/bash

echo "Uninstalling DogLog Enhanced..."

# Stop and disable service
systemctl stop doglog.service 2>/dev/null || true
systemctl disable doglog.service 2>/dev/null || true

# Remove systemd service
rm -f /etc/systemd/system/doglog.service
systemctl daemon-reload

# Remove symlink
rm -f /usr/local/bin/doglog

# Remove installation directory
rm -rf /opt/doglog

# Remove configuration
rm -rf /etc/doglog

# Remove logs
rm -rf /var/log/doglog

echo "DogLog Enhanced uninstalled successfully"
EOF

chmod +x $INSTALL_DIR/uninstall.sh

# Final instructions
echo -e "\n${GREEN}🎉 DogLog Enhanced installed successfully!${NC}\n"

echo -e "${BLUE}📋 Installation Summary:${NC}"
echo -e "  • Installation directory: ${GREEN}$INSTALL_DIR${NC}"
echo -e "  • Configuration: ${GREEN}$CONFIG_DIR${NC}"
echo -e "  • Logs: ${GREEN}$LOG_DIR${NC}"
echo -e "  • Executable: ${GREEN}/usr/local/bin/doglog${NC}"

echo -e "\n${BLUE}🚀 Usage:${NC}"
echo -e "  • Start service: ${GREEN}systemctl start doglog${NC}"
echo -e "  • Stop service: ${GREEN}systemctl stop doglog${NC}"
echo -e "  • Enable auto-start: ${GREEN}systemctl enable doglog${NC}"
echo -e "  • View logs: ${GREEN}journalctl -u doglog -f${NC}"
echo -e "  • Manual run: ${GREEN}doglog --all${NC}"

echo -e "\n${BLUE}🔧 Configuration:${NC}"
echo -e "  • Edit config: ${GREEN}nano $CONFIG_DIR/doglog_config.json${NC}"
echo -e "  • Test config: ${GREEN}doglog --help${NC}"

echo -e "\n${BLUE}🧪 Testing:${NC}"
echo -e "  • Run tests: ${GREEN}cd $INSTALL_DIR && python -m unittest testing.test_doglog -v${NC}"
echo -e "  • Test with sample log: ${GREEN}echo '\$(date) ERROR Test error' | sudo tee -a /var/log/test.log && doglog --logs /var/log/test.log${NC}"

echo -e "\n${BLUE}🗑️  Uninstall:${NC}"
echo -e "  • Run: ${GREEN}$INSTALL_DIR/uninstall.sh${NC}"

echo -e "\n${YELLOW}⚠️  Important Notes:${NC}"
echo -e "  • DogLog requires root privileges to read system logs"
echo -e "  • Auto-blocking feature requires iptables"
echo -e "  • Configure email alerts in $CONFIG_DIR/doglog_config.json"
echo -e "  • Monitor logs with: journalctl -u doglog -f"

echo -e "\n${GREEN}✅ Installation completed successfully!${NC}" 