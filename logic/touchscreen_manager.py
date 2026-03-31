"""
TouchScreen Manager Module

Handles all touchscreen-related operations including detection,
enabling, and disabling touchscreen devices via PowerShell commands.
"""

import subprocess
import logging
from typing import Tuple, Optional


class TouchScreenManager:
    """Manages touchscreen device operations using PowerShell commands."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_touchscreen_status(self) -> Tuple[bool, str]:
        """
        Get the current status of touchscreen devices.
        
        Returns:
            Tuple[bool, str]: (is_enabled, status_message)
        """
        try:
            # PowerShell command to get touchscreen device status
            cmd = [
                "powershell.exe", 
                "-Command",
                "Get-PnpDevice -Class 'HIDClass' | Where-Object { $_.FriendlyName -match 'Touch' } | Select-Object FriendlyName, Status"
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                shell=True,
                timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if "OK" in output:
                    return True, "Touchscreen is ON"
                elif "Error" in output or "Problem" in output:
                    return False, "Touchscreen is OFF"
                else:
                    return False, "No touchscreen detected"
            else:
                self.logger.error(f"PowerShell command failed: {result.stderr}")
                return False, "Error checking touchscreen status"
                
        except subprocess.TimeoutExpired:
            self.logger.error("PowerShell command timed out")
            return False, "Timeout checking touchscreen status"
        except Exception as e:
            self.logger.error(f"Error checking touchscreen status: {e}")
            return False, "Error checking touchscreen status"
    
    def disable_touchscreen(self) -> Tuple[bool, str]:
        """
        Disable touchscreen devices.
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            cmd = [
                "powershell.exe",
                "-Command",
                "Get-PnpDevice -Class 'HIDClass' | Where-Object { $_.FriendlyName -match 'Touch' } | Disable-PnpDevice -Confirm:$false"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                timeout=15
            )
            
            if result.returncode == 0:
                self.logger.info("Touchscreen disabled successfully")
                return True, "Touchscreen disabled successfully"
            else:
                error_msg = result.stderr.strip() or "Unknown error occurred"
                self.logger.error(f"Failed to disable touchscreen: {error_msg}")
                return False, f"Failed to disable touchscreen: {error_msg}"
                
        except subprocess.TimeoutExpired:
            self.logger.error("Disable command timed out")
            return False, "Disable operation timed out"
        except Exception as e:
            self.logger.error(f"Error disabling touchscreen: {e}")
            return False, f"Error disabling touchscreen: {e}"
    
    def enable_touchscreen(self) -> Tuple[bool, str]:
        """
        Enable touchscreen devices.
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            cmd = [
                "powershell.exe",
                "-Command", 
                "Get-PnpDevice -Class 'HIDClass' | Where-Object { $_.FriendlyName -match 'Touch' } | Enable-PnpDevice -Confirm:$false"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                timeout=15
            )
            
            if result.returncode == 0:
                self.logger.info("Touchscreen enabled successfully")
                return True, "Touchscreen enabled successfully"
            else:
                error_msg = result.stderr.strip() or "Unknown error occurred"
                self.logger.error(f"Failed to enable touchscreen: {error_msg}")
                return False, f"Failed to enable touchscreen: {error_msg}"
                
        except subprocess.TimeoutExpired:
            self.logger.error("Enable command timed out")
            return False, "Enable operation timed out"
        except Exception as e:
            self.logger.error(f"Error enabling touchscreen: {e}")
            return False, f"Error enabling touchscreen: {e}"
    
    def toggle_touchscreen(self) -> Tuple[bool, str]:
        """
        Toggle touchscreen state (enable if disabled, disable if enabled).
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        is_enabled, status_msg = self.get_touchscreen_status()
        
        if is_enabled:
            return self.disable_touchscreen()
        else:
            return self.enable_touchscreen()
    
    def is_admin(self) -> bool:
        """
        Check if the application is running with administrator privileges.
        
        Returns:
            bool: True if running as admin, False otherwise
        """
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False
