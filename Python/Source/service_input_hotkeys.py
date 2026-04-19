import sys

if sys.platform == 'darwin':
    from pynput import keyboard
    class ServiceInputHotkeys:
        command = "--service_input_hotkeys"
        
        def __init__(self, command_router_function):
            self.route_command = command_router_function 
            self.hotkey_listener = None
            self.hotkeys = []

        def start(self):
            self.route_command("--ui_header Service added: Input_Hotkeys")
            self.hotkeys_add( "--mic_toggle", 'ctrl shift m')
            self.hotkeys_add("--quit", 'ctrl q')
            self.route_command("--ui_spacer")
        
        def stop(self):
            if self.hotkey_listener:
                self.hotkey_listener.stop()
            self.route_command("--ui_notify Service removed: Input_Hotkeys")

        def on_command(self, text: str) -> bool:
            return False

        def hotkeys_add(self,command,hotkey):
            # Format
            hotkey = self._hotkey_format(hotkey)

            # Guard
            if hotkey in self.hotkeys:
                return
            
            # Add
            self.hotkeys.append(command)
            self.hotkeys.append(hotkey)
            self.route_command(f"--ui_notify Hotkey added: {command} {hotkey}")
            self._hotkeys_build()

        def _hotkeys_build(self):
            # Listner : Unbind
            if self.hotkey_listener:
                self.hotkey_listener.stop()
                self.hotkey_listener = None

            # Hotkey mapping
            mapping = {}
            for i in range(0, len(self.hotkeys), 2):
                hotkey = self.hotkeys[i+1]
                command = self.hotkeys[i]
                mapping[hotkey] = lambda c=command: self._on_hotkey(c)    

            # Listner: Bind
            try:
                self.hotkey_listener = keyboard.GlobalHotKeys(mapping)
                self.hotkey_listener.start()
            except Exception as e:
                self.route_command(f"--ui_error Hotkey binding failed: {e}")
        
        def _hotkey_format(self, raw_hotkey):
            # Standardize all delimiters to spaces
            cleaned = raw_hotkey.replace('-', ' ').replace(',', ' ').replace('+', ' ')
            parts = cleaned.split()

            # Define the modifiers pynput expects to be wrapped in brackets
            modifiers = {'ctrl', 'shift', 'alt', 'cmd', 'super', 'opt', 'win'}

            # Format
            formatted_parts = []
            for part in parts:
                part_lower = part.lower()
                formatted_parts.append(f"<{part_lower}>" if part_lower in modifiers else part_lower)
            return "+".join(formatted_parts)
        
        def _on_hotkey(self, command):
            self.route_command(command, "keyboard")

# Not supported
else:
   class ServiceInputHotkeys:
        command = "--service_command_keys_mac"
        
        def __init__(self, command_router_function):
            self.route_command = command_router_function

        def start(self):
           self.route_command("--ui_error Service not supported on device: Command_Keys_Mac")
           pass

        def stop(self):
            pass

        def on_command(self, text: str) -> bool:
            return False