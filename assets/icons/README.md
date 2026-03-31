# TouchToggle Icon Instructions

## Adding an Icon to Your Executable

To add a custom icon to your TouchToggle executable:

### 1. **Icon Requirements:**
- **Format**: `.ico` file (Windows Icon format)
- **Size**: Recommended 256x256 pixels (will scale automatically)
- **Color**: Support for multiple sizes and color depths

### 2. **Icon Placement:**
Place your icon file at:
```
assets/icons/touchtoggle.ico
```

### 3. **Icon Creation Options:**

#### **Online Converters:**
- [ConvertICO.com](https://convertio.co/png-ico/)
- [ICO Convert](https://icoconvert.com/)
- Upload a PNG/JPG image and download as .ico

#### **Free Icon Resources:**
- [Flaticon](https://www.flaticon.com/) - Free icons (attribution required)
- [Icons8](https://icons8.com/) - Free icons with account
- [Feather Icons](https://feathericons.com/) - Simple, elegant icons

#### **Recommended Icon Style:**
For TouchToggle, consider icons representing:
- 👆 Touch/finger icon
- 📱 Device/tablet icon  
- ⚡ Power/toggle icon
- 🔄 Switch/toggle icon

### 4. **After Adding Icon:**
1. Save your `.ico` file as `assets/icons/touchtoggle.ico`
2. Run the build script: `python build_exe.py`
3. The icon will automatically be included in your executable

### 5. **Icon Preview:**
Your icon will appear:
- ✅ In Windows Explorer
- ✅ On the taskbar when running
- ✅ In the system tray (if added later)
- ✅ In the executable properties

---

**Note**: If no icon is provided, PyInstaller will use the default Python icon.
