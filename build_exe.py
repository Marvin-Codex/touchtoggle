"""
Build script for creating TouchToggle executable

This script uses PyInstaller to create a standalone executable
from the TouchToggle Python application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Build the TouchToggle executable using PyInstaller."""
    
    print("🔧 Building TouchToggle executable...")
    print("=" * 50)
    
    # Get the current directory
    current_dir = Path.cwd()
    
    # Define paths
    main_script = current_dir / "main.py"
    build_dir = current_dir / "build"
    dist_dir = current_dir / "dist"
    icon_path = current_dir / "assets" / "icons" / "touchtoggle.ico"
    
    # Check if main.py exists
    if not main_script.exists():
        print("❌ Error: main.py not found in current directory")
        return False
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # PyInstaller command with options for a clean, single-file executable
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--windowed",                   # No console window (GUI app)
        "--name=TouchToggle",           # Name of the executable
        "--clean",                      # Clean cache before building
        "--noconfirm",                  # Replace output directory without asking
        "--add-data=ui;ui",             # Include UI package
        "--add-data=logic;logic",       # Include logic package
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtGui",
        "--collect-all=PyQt6",
        "--version-file=version_info.txt",  # Add version info for better Windows integration
    ]
    
    # Add icon if it exists
    if icon_path.exists():
        pyinstaller_cmd.extend(["--icon", str(icon_path)])
        # Also add icon as data file for runtime access
        pyinstaller_cmd.extend(["--add-data", f"{icon_path};assets/icons/"])
        print(f"🎨 Using icon: {icon_path}")
    else:
        print(f"ℹ️  No icon found at {icon_path}")
        print("   Place your .ico file there to add an icon to the executable")
    
    pyinstaller_cmd.append(str(main_script))
    
    try:
        print("🔨 Running PyInstaller...")
        print(f"Command: {' '.join(pyinstaller_cmd)}")
        print()
        
        # Run PyInstaller
        result = subprocess.run(
            pyinstaller_cmd,
            check=True,
            capture_output=False,  # Show output in real-time
            text=True
        )
        
        print()
        print("✅ Build completed successfully!")
        
        # Check if executable was created
        exe_path = dist_dir / "TouchToggle.exe"
        if exe_path.exists():
            print(f"📦 Executable created: {exe_path}")
            print(f"📊 File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            
            # Create a release folder
            release_dir = current_dir / "release"
            if release_dir.exists():
                shutil.rmtree(release_dir)
            release_dir.mkdir()
            
            # Copy executable to release folder
            release_exe = release_dir / "TouchToggle.exe"
            shutil.copy2(exe_path, release_exe)
            
            # Copy README to release folder
            readme_path = current_dir / "README.md"
            if readme_path.exists():
                shutil.copy2(readme_path, release_dir / "README.md")
            
            print(f"📁 Release folder created: {release_dir}")
            print()
            print("🚀 Your TouchToggle executable is ready!")
            print(f"   Location: {release_exe}")
            print()
            print("💡 Tips:")
            print("   • Run TouchToggle.exe as Administrator for full functionality")
            print("   • The executable is portable - no installation required")
            print("   • You can distribute the 'release' folder to others")
            
            return True
        else:
            print("❌ Error: Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller failed with error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during build: {e}")
        return False

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        print("📥 Installing PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0.0"], check=True)
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False

def main():
    """Main build function."""
    print("TouchToggle Executable Builder")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    if not install_pyinstaller():
        input("Press Enter to exit...")
        return
    
    # Build the executable
    if build_executable():
        print("\n🎉 Build process completed successfully!")
    else:
        print("\n💥 Build process failed!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
