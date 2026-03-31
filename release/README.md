# TouchToggle

TouchToggle is a lightweight Windows desktop utility that lets you quickly enable or disable your laptop touchscreen with one click.

Built with Python and PyQt6, it uses Windows PowerShell device commands under the hood to provide a simple and practical control panel for touchscreen state.

## Author

- GitHub: [Marvin-Codex](https://github.com/Marvin-Codex)

## Features

- One-click touchscreen toggle
- Real-time touchscreen status display
- Administrator privilege detection with user guidance
- Clean desktop UI optimized for Windows
- Built-in error handling and status feedback

## Requirements

- Windows 10 or Windows 11
- Python 3.8+
- Administrator privileges (required for enabling/disabling device drivers)

## Project Structure

```text
touchtoggle/
|-- main.py
|-- requirements.txt
|-- run_touchtoggle.bat
|-- setup.py
|-- build_exe.py
|-- ui/
|   |-- __init__.py
|   `-- main_window.py
|-- logic/
|   |-- __init__.py
|   `-- touchscreen_manager.py
`-- assets/
   `-- icons/
```

## Clone The Repository

```powershell
git clone https://github.com/Marvin-Codex/TouchUtility.git
cd TouchUtility/touchtoggle
```

If your repository name/path is different, replace the URL with your actual repository URL.

## Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run The App

### Option 1: Run With Python Command

```powershell
python main.py
```

### Option 2: Run With Batch File

```powershell
./run_touchtoggle.bat
```

## Recommended: Run As Administrator

Touchscreen driver changes require elevated permissions.

To run with admin rights:

1. Right-click `run_touchtoggle.bat` or `TouchToggle.exe`
2. Select **Run as administrator**

## Build Guide (Create EXE)

Use one of the methods below to generate a standalone Windows executable.

### Method 1: Python Build Script (Recommended)

```powershell
python build_exe.py
```

### Method 2: Batch File

```powershell
./build_exe.bat
```

### Build Output

- Main artifact: `dist/TouchToggle.exe`
- Distribution copy: `release/TouchToggle.exe`

### Build Notes

- If `assets/icons/touchtoggle.ico` exists, it will be embedded as the EXE icon.
- Rebuild after code or icon updates to refresh the executable.
- Run the generated EXE as Administrator for full touchscreen control.

## Troubleshooting

### App Starts But Cannot Toggle Touchscreen

- Ensure the app is running as Administrator.
- Confirm your device exposes a HID touchscreen in Device Manager.

### "No Touchscreen Detected"

- Verify your hardware supports touch input.
- Check that touchscreen drivers are installed and enabled.

### PyQt6 Import Errors

- Reinstall dependencies:

```powershell
pip install -r requirements.txt --upgrade
```

## Security Note

TouchToggle uses built-in Windows PowerShell device management commands and does not modify system files directly.

## License

This project is provided as-is for educational and utility purposes.
