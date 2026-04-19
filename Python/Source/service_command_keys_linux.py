import sys

if sys.platform == 'linux':

    import time
    from evdev import UInput, ecodes as e

    class ServiceCommandKeysLinux:
        command = "--service_output_keyboard"
        
        def __init__(self, command_router_function):
            self.route_command = command_router_function
            self.ui = None
            
            # Mapping common names to evdev codes
            self.key_map = {
                "alt": e.KEY_LEFTALT,
                "ctrl": e.KEY_LEFTCTRL,
                "shift": e.KEY_LEFTSHIFT,
                "win": e.KEY_LEFTMETA,
                "space": e.KEY_SPACE,
                "enter": e.KEY_ENTER,
                "esc": e.KEY_ESC,
                "tab": e.KEY_TAB,
                "backspace": e.KEY_BACKSPACE
            }

        def start(self):
            self.route_command("--ui_header Service added: Output_Keyboard")
            self.route_command("--ui_attention Linux Hardware Injection: This service uses evdev to simulate a physical keyboard. Ensure your user has permissions for /dev/uinput.")
            
            # Initialize Virtual Device
            try:
                # We register a broad range of keys (A-Z, 0-9, and our map)
                keys = list(self.key_map.values()) + [getattr(e, f"KEY_{chr(i).upper()}") for i in range(ord('a'), ord('z')+1)]
                keys += [getattr(e, f"KEY_{i}") for i in range(10)]
                
                capabilities = {e.EV_KEY: keys}
                self.ui = UInput(capabilities, name='voxcore-virtual-keyboard')
                self.route_command("--ui_notify Virtual Keyboard Initialized.")
            except Exception as err:
                self.route_command(f"--ui_error Failed to initialize evdev: {str(err)}")

        def stop(self):
            if self.ui:
                self.ui.close()
            self.route_command("--ui_notify Service removed: Output_Keyboard")

        def on_command(self, text: str) -> bool:
            if not text.startswith("--key ") or not self.ui:
                return False

            key_data = text.replace("--key ", "").strip().lower()
            
            try:
                # Handle combinations (e.g., alt-n)
                if "-" in key_data:
                    parts = key_data.split("-")
                    codes = [self._get_code(k) for k in parts]
                    
                    if all(codes):
                        # Press all in order
                        for code in codes:
                            self.ui.write(e.EV_KEY, code, 1)
                        self.ui.syn()
                        
                        # Small hold for game engine detection
                        time.sleep(0.05) 
                        
                        # Release all in reverse order
                        for code in reversed(codes):
                            self.ui.write(e.EV_KEY, code, 0)
                        self.ui.syn()
                else:
                    # Single key press
                    code = self._get_code(key_data)
                    if code:
                        self.ui.write(e.EV_KEY, code, 1)
                        self.ui.syn()
                        time.sleep(0.05)
                        self.ui.write(e.EV_KEY, code, 0)
                        self.ui.syn()
                
                return True

            except Exception as err:
                self.route_command(f"--ui_error Key Injection Failed: {str(err)}")
                return False

        def _get_code(self, key_name):
            """Helper to find the correct evdev code."""
            # Check our manual map first (modifiers)
            if key_name in self.key_map:
                return self.key_map[key_name]
            
            # Try to find KEY_X dynamically
            try:
                return getattr(e, f"KEY_{key_name.upper()}")
            except AttributeError:
                self.route_command(f"--ui_error Unknown key: {key_name}")
                return None

# Not supported
else:
   class ServiceCommandKeysLinux:
        command = "--service_output_keyboard"
        
        def __init__(self, command_router_function):
            self.route_command = command_router_function

        def start(self):
           self.route_command("--ui_error Service not supported on platofrm:  Command_Keys_Linux")
           pass

        def stop(self):
            pass

        def on_command(self, text: str) -> bool:
            return False