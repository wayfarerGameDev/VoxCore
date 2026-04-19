import sys

if sys.platform == 'darwin':
    import time
    import Quartz

    class ServiceCommandKeysMac:
        command = "--service_command_keys_mac"
        
        def __init__(self, command_router_function):
            self.route_command = command_router_function
            
            self.key_map_mac = {
                # --- Default Modifiers (Maps to Left for easy typing) ---
                "alt": 58,       
                "option": 58,
                "ctrl": 59,      
                "control": 59,
                "shift": 56,     
                "cmd": 55,       
                "command": 55,

                # --- Explicit Left Modifiers ---
                "left_alt": 58,       
                "left_option": 58,
                "left_ctrl": 59,      
                "left_control": 59,
                "left_shift": 56,     
                "left_cmd": 55,       
                "left_command": 55,

                # --- Explicit Right Modifiers ---
                "right_alt": 61,
                "right_option": 61,
                "right_ctrl": 62,
                "right_control": 62,
                "right_shift": 60,
                "right_cmd": 54,
                "right_command": 54,

                # --- Standard Controls ---
                "space": 49,
                "enter": 36,
                "return": 36,
                "esc": 53,
                "tab": 48,
                "backspace": 51,
                "delete": 51,
                "caps": 57,
                "capslock": 57,

                # --- The Alphabet ---
                "a": 0,  "b": 11, "c": 8,  "d": 2,
                "e": 14, "f": 3,  "g": 5,  "h": 4,
                "i": 34, "j": 38, "k": 40, "l": 37,
                "m": 46, "n": 45, "o": 31, "p": 35,
                "q": 12, "r": 15, "s": 1,  "t": 17,
                "u": 32, "v": 9,  "w": 13, "x": 7,
                "y": 16, "z": 6,

                # --- Numbers (Top Row) ---
                "1": 18, "2": 19, "3": 20, "4": 21, "5": 23,
                "6": 22, "7": 26, "8": 28, "9": 25, "0": 29,

                # --- Numpad ---
                "numpad_0": 82, "numpad_1": 83, "numpad_2": 84, "numpad_3": 85,
                "numpad_4": 86, "numpad_5": 87, "numpad_6": 88, "numpad_7": 89,
                "numpad_8": 91, "numpad_9": 92, 
                "numpad_decimal": 65, "numpad_multiply": 67, "numpad_plus": 69,
                "numpad_clear": 71, "numpad_divide": 75, "numpad_enter": 76,
                "numpad_minus": 78, "numpad_equals": 81,

                # --- Punctuation & Symbols (AI Voice Safe) ---
                "-": 27,         "minus": 27,          "dash": 27,
                "=": 24,         "equals": 24,         "equal": 24,
                "[": 33,         "left_bracket": 33,   "bracket_left": 33,
                "]": 30,         "right_bracket": 30,  "bracket_right": 30,
                "\\": 42,        "backslash": 42,
                ";": 41,         "semicolon": 41,
                "'": 39,         "quote": 39,          "apostrophe": 39,
                ",": 43,         "comma": 43,
                ".": 47,         "period": 47,         "dot": 47,
                "/": 44,         "slash": 44,          "forward_slash": 44,
                "`": 50,         "tick": 50,           "backtick": 50,

                # --- Arrow Keys ---
                "up": 126,
                "down": 125,
                "left": 123,
                "right": 124,
                
                # --- F Keys ---
                "f1": 122, "f2": 120, "f3": 99,  "f4": 118,
                "f5": 96,  "f6": 97,  "f7": 98,  "f8": 100,
                "f9": 101, "f10": 109, "f11": 103, "f12": 111,
                "f13": 105, "f14": 107, "f15": 113, "f16": 106,
                "f17": 64,  "f18": 79,  "f19": 80
            }

        def start(self):
            self.route_command("--ui_header Service added: Output_Keyboard_Mac")
            self.route_command("--ui_attention Accessibility Required: You must grant your Terminal/IDE 'Accessibility' permissions in System Settings > Privacy & Security.")
            self.route_command("--ui_notify Quartz Event Engine Initialized.")

        def stop(self):
            self.route_command("--ui_notify Service removed: Output_Keyboard_Mac")

        def on_command(self, text: str) -> bool:
            if not text.startswith("--key "):
                return False

            # Clean the input: replace hyphens and pluses with spaces
            raw_key_data = text.replace("--key ", "").strip().lower()
            key_data = raw_key_data.replace("-", " ").replace("+", " ")
            
            modifier_flags = {
                "cmd": Quartz.kCGEventFlagMaskCommand,
                "opt": Quartz.kCGEventFlagMaskAlternate,
                "alt": Quartz.kCGEventFlagMaskAlternate,
                "ctrl": Quartz.kCGEventFlagMaskControl,
                "shift": Quartz.kCGEventFlagMaskShift
            }

            try:
                # Simply split by spaces now!
                parts = key_data.split()
                
                if len(parts) > 1:
                    # 1. Separate modifiers from the main key
                    mods = [p for p in parts if p in modifier_flags]
                    main_keys = [p for p in parts if p not in modifier_flags]
                    
                    # 2. Build the combined flag mask
                    flags = 0
                    for m in mods:
                        flags |= modifier_flags[m]
                    
                    # 3. Press the main key(s) WITH the modifiers attached
                    codes = [self._get_code(k) for k in main_keys]
                    
                    if all(c is not None for c in codes):
                        for code in codes:
                            self._post_key(code, True, flags)
                        time.sleep(0.05)
                        for code in reversed(codes):
                            self._post_key(code, False, flags)
                        return True
                    else:
                        self.route_command(f"--ui_error Missing key in map for: {key_data}")
                        return False

                else:
                    # Single key press
                    code = self._get_code(parts[0])
                    if code is not None:
                        self._post_key(code, True, 0)
                        time.sleep(0.05)
                        self._post_key(code, False, 0)
                        return True

                return False
                
            except Exception as err:
                self.route_command(f"--ui_error macOS Key Injection Failed: {str(err)}")
                return False

        def _get_code(self, key_name):
            if key_name in self.key_map_mac:
                return self.key_map_mac[key_name]
            return None

        def _post_key(self, code, is_down, flags):
            """Sends a raw hardware event with combined modifier flags."""
            event = Quartz.CGEventCreateKeyboardEvent(None, code, is_down)
            if flags > 0:
                Quartz.CGEventSetFlags(event, flags)
                Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

# Not supported
else:
   class ServiceCommandKeysMac:
        
        def __init__(self, command_router_function):
            self.route_command = command_router_function

        def start(self):
           self.route_command("--ui_error Service not supported on device: Command_Keys_Mac")
           pass

        def stop(self):
            pass

        def on_command(self, text: str) -> bool:
            return False