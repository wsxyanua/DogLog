#!/usr/bin/env python3
"""
Wrapper script để chạy DogLog Enhanced
"""

import sys
import os
import subprocess

def main():
    """Main function"""
    print("🐕 DogLog Enhanced Runner")
    print("=" * 40)
    
    # Add current directory to Python path
    sys.path.append('.')
    
    # Check if core modules exist
    if not os.path.exists('core_modules/logdog_enhanced.py'):
        print("❌ Error: core_modules/logdog_enhanced.py not found!")
        print("Please run this script from the DogLog root directory.")
        sys.exit(1)
    
    # Get command line arguments
    args = sys.argv[1:] if len(sys.argv) > 1 else ['--help']
    
    # Run DogLog Enhanced
    try:
        cmd = ['python3', 'core_modules/logdog_enhanced.py'] + args
        print(f"🚀 Running: {' '.join(cmd)}")
        print()
        
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error running DogLog: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 