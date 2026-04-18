import os   
import sys
import time

# Iconic Tech & IDE Themes
PALETTE_DRACULA         = ['\033[38;5;141m', '\033[38;5;212m', '\033[38;5;84m', '\033[38;5;228m', '\033[38;5;203m', '\033[38;5;231m', '\033[0m', '\033[38;5;103m']
PALETTE_GRUVBOX         = ['\033[38;5;214m', '\033[38;5;208m', '\033[38;5;142m', '\033[38;5;172m', '\033[38;5;142m', '\033[38;5;223m', '\033[0m', '\033[38;5;243m']
PALETTE_NORD            = ['\033[38;5;110m', '\033[38;5;67m', '\033[38;5;150m', '\033[38;5;180m', '\033[38;5;167m', '\033[38;5;111m', '\033[0m', '\033[2m']
PALETTE_MONOKAI         = ['\033[38;5;197m', '\033[38;5;148m', '\033[38;5;81m', '\033[38;5;208m', '\033[38;5;161m', '\033[38;5;231m', '\033[0m', '\033[38;5;242m']
PALETTE_OCEANIC         = ['\033[38;5;38m', '\033[38;5;32m', '\033[38;5;79m', '\033[38;5;221m', '\033[38;5;203m', '\033[38;5;152m', '\033[0m', '\033[38;5;66m']
PALETTE_SOLAR           = ['\033[38;5;33m', '\033[38;5;37m', '\033[38;5;64m', '\033[38;5;136m', '\033[38;5;160m', '\033[38;5;245m', '\033[0m', '\033[2m']

# Retro Hardware & Gaming
PALETTE_PIPBOY_GREEN    = ['\033[38;5;47m', '\033[38;5;28m', '\033[38;5;46m', '\033[38;5;82m', '\033[38;5;196m', '\033[38;5;121m', '\033[0m', '\033[38;5;22m']
PALETTE_PIPBOY_AMBER    = ['\033[38;5;208m', '\033[38;5;130m', '\033[38;5;214m', '\033[38;5;202m', '\033[38;5;166m', '\033[38;5;215m', '\033[0m', '\033[38;5;94m']
PALETTE_PIPBOY_BLUE     = ['\033[38;5;51m', '\033[38;5;31m', '\033[38;5;45m', '\033[38;5;39m', '\033[38;5;24m', '\033[38;5;123m', '\033[0m', '\033[38;5;23m']
PALETTE_PIPBOY_WHITE    = ['\033[38;5;255m', '\033[38;5;244m', '\033[38;5;252m', '\033[38;5;250m', '\033[38;5;248m', '\033[38;5;231m', '\033[0m', '\033[38;5;240m']
PALETTE_PIPBOY_RED      = ['\033[38;5;196m', '\033[38;5;88m', '\033[38;5;160m', '\033[38;5;124m', '\033[38;5;52m', '\033[38;5;203m', '\033[0m', '\033[38;5;52m']
PALETTE_PIPBOY_PURPLE   = ['\033[38;5;171m', '\033[38;5;93m', '\033[38;5;135m', '\033[38;5;129m', '\033[38;5;55m', '\033[38;5;183m', '\033[0m', '\033[38;5;54m']
PALETTE_PIPBOY_YELLOW   = ['\033[38;5;226m', '\033[38;5;100m', '\033[38;5;220m', '\033[38;5;184m', '\033[38;5;136m', '\033[38;5;229m', '\033[0m', '\033[38;5;58m']
PALETTE_PIPBOY_PINK     = ['\033[38;5;213m', '\033[38;5;162m', '\033[38;5;205m', '\033[38;5;200m', '\033[38;5;89m', '\033[38;5;219m', '\033[0m', '\033[38;5;53m']
PALETTE_AMBER           = ['\033[38;5;214m', '\033[38;5;172m', '\033[38;5;220m', '\033[38;5;214m', '\033[38;5;196m', '\033[38;5;215m', '\033[0m', '\033[38;5;130m']
PALETTE_PHOSPHOR        = ['\033[38;5;46m', '\033[38;5;28m', '\033[38;5;120m', '\033[38;5;46m', '\033[38;5;124m', '\033[38;5;84m',  '\033[0m', '\033[38;5;22m']
PALETTE_C64             = ['\033[38;5;63m', '\033[38;5;105m', '\033[38;5;111m', '\033[38;5;227m', '\033[38;5;160m', '\033[38;5;153m', '\033[0m', '\033[38;5;17m']
PALETTE_GAMEBOY         = ['\033[38;5;22m', '\033[38;5;64m', '\033[38;5;28m', '\033[38;5;100m', '\033[38;5;52m', '\033[38;5;107m', '\033[0m', '\033[2m']
PALETTE_MATRIX          = ['\033[38;5;46m', '\033[38;5;22m', '\033[38;5;120m', '\033[38;5;190m', '\033[38;5;124m', '\033[38;5;48m',  '\033[0m', '\033[2m']

# Original & Custom "Vox" Themes
PALETTE_DUSTY           = ['\033[38;5;167m', '\033[38;5;103m', '\033[38;5;108m', '\033[38;5;186m', '\033[38;5;131m', '\033[38;5;252m', '\033[0m', '\033[2m']
PALETTE_FOREST          = ['\033[38;5;34m', '\033[38;5;65m', '\033[38;5;113m', '\033[38;5;142m', '\033[38;5;88m', '\033[38;5;194m', '\033[0m', '\033[2m']
PALETTE_MIDNIGHT        = ['\033[38;5;198m', '\033[38;5;45m', '\033[38;5;46m', '\033[38;5;214m', '\033[38;5;160m', '\033[38;5;45m',  '\033[0m', '\033[2m']
PALETTE_VOID            = ['\033[38;5;255m', '\033[38;5;236m', '\033[38;5;248m', '\033[38;5;244m', '\033[38;5;124m', '\033[38;5;253m', '\033[0m', '\033[38;5;232m']
PALETTE_BONE            = ['\033[38;5;252m', '\033[38;5;244m', '\033[38;5;250m', '\033[38;5;248m', '\033[38;5;238m', '\033[38;5;255m', '\033[0m', '\033[2m']

# High-Energy & Aesthetic
PALETTE_SYNTH           = ['\033[38;5;201m', '\033[38;5;129m', '\033[38;5;51m', '\033[38;5;226m', '\033[38;5;197m', '\033[38;5;51m',  '\033[0m', '\033[38;5;61m']
PALETTE_VAPOR           = ['\033[38;5;201m', '\033[38;5;171m', '\033[38;5;51m', '\033[38;5;226m', '\033[38;5;204m', '\033[38;5;51m',  '\033[0m', '\033[2m']
PALETTE_CYBER           = ['\033[38;5;226m', '\033[38;5;51m', '\033[38;5;201m', '\033[38;5;46m', '\033[38;5;196m', '\033[38;5;51m',  '\033[0m', '\033[2m']
PALETTE_SAKURA          = ['\033[38;5;218m', '\033[38;5;225m', '\033[38;5;211m', '\033[38;5;221m', '\033[38;5;196m', '\033[38;5;255m', '\033[0m', '\033[38;5;252m']

# Earth & Elemental
PALETTE_OASIS           = ['\033[38;5;72m', '\033[38;5;66m', '\033[38;5;115m', '\033[38;5;179m', '\033[38;5;131m', '\033[38;5;194m', '\033[0m', '\033[38;5;23m']
PALETTE_LAVA            = ['\033[38;5;196m', '\033[38;5;202m', '\033[38;5;208m', '\033[38;5;214m', '\033[38;5;160m', '\033[38;5;230m', '\033[0m', '\033[38;5;242m']
PALETTE_GLACIER         = ['\033[38;5;117m', '\033[38;5;111m', '\033[38;5;153m', '\033[38;5;255m', '\033[38;5;24m', '\033[38;5;159m', '\033[0m', '\033[38;5;109m']
PALETTE_COFFEE          = ['\033[38;5;94m', '\033[38;5;137m', '\033[38;5;138m', '\033[38;5;180m', '\033[38;5;52m', '\033[38;5;230m', '\033[0m', '\033[38;5;238m']
PALETTE_CRIMSON         = ['\033[38;5;160m', '\033[38;5;88m', '\033[38;5;196m', '\033[38;5;202m', '\033[38;5;52m', '\033[38;5;255m', '\033[0m', '\033[2m']
PALETTE_STEEL           = ['\033[38;5;244m', '\033[38;5;240m', '\033[38;5;250m', '\033[38;5;248m', '\033[38;5;235m', '\033[38;5;255m', '\033[0m', '\033[2m']
PALETTE_WINDBLOWN       = ['\033[38;5;117m', '\033[38;5;244m', '\033[38;5;158m', '\033[38;5;222m', '\033[38;5;167m', '\033[38;5;255m', '\033[0m', '\033[38;5;240m']

# Set Active Theme
PALETTE_CURRENT = PALETTE_PIPBOY_GREEN

PALETTE_MAP = {
    "dracula": PALETTE_DRACULA,
    "gruvbox": PALETTE_GRUVBOX,
    "nord": PALETTE_NORD,
    "monokai": PALETTE_MONOKAI,
    "oceanic": PALETTE_OCEANIC,
    "solar": PALETTE_SOLAR,
    "pipboy": PALETTE_PIPBOY_GREEN,
    "pipboy_green": PALETTE_PIPBOY_GREEN,
    "pipboy_amber": PALETTE_PIPBOY_AMBER,
    "pipboy_blue": PALETTE_PIPBOY_BLUE,
    "pipboy_white": PALETTE_PIPBOY_WHITE,
    "pipboy_red": PALETTE_PIPBOY_RED,
    "pipboy_purple": PALETTE_PIPBOY_PURPLE,
    "pipboy_yellow": PALETTE_PIPBOY_YELLOW,
    "pipboy_pink": PALETTE_PIPBOY_PINK,
    "amber": PALETTE_PIPBOY_AMBER,
    "phosphor": PALETTE_PHOSPHOR,
    "c64": PALETTE_C64,
    "gameboy": PALETTE_GAMEBOY,
    "matrix": PALETTE_MATRIX,
    "dusty": PALETTE_DUSTY,
    "forest": PALETTE_FOREST,
    "midnight": PALETTE_MIDNIGHT,
    "void": PALETTE_VOID,
    "bone": PALETTE_BONE,
    "synth": PALETTE_SYNTH,
    "vapor": PALETTE_VAPOR,
    "cyber": PALETTE_CYBER,
    "sakura": PALETTE_SAKURA,
    "oasis": PALETTE_OASIS,
    "lava": PALETTE_LAVA,
    "glacier": PALETTE_GLACIER,
    "coffee": PALETTE_COFFEE,
    "crimson": PALETTE_CRIMSON,
    "steel": PALETTE_STEEL,
    "windblown": PALETTE_WINDBLOWN
}

# TERMINAL LINE-EDITING ENGINE (CROSS-PLATFORM)
USE_READLINE = False
try:
    if os.name != 'nt':
        import readline
        USE_READLINE = True
        if readline and 'libedit' in (readline.__doc__ or ''):
            readline.parse_and_bind("bind ^[[A ed-prev-history")
            readline.parse_and_bind("bind ^[[B ed-next-history")
            readline.parse_and_bind("bind ^[[C el-forward-char")
            readline.parse_and_bind("bind ^[[D el-backward-char")
        elif readline:
            readline.parse_and_bind("tab: complete")
except Exception:
    USE_READLINE = False

class ServiceUITerminal:
    command = "--service_ui_terminal"
    
    def __init__(self, command_router_function, palette=None, typewriter=True):
        self.route_command = command_router_function
        self.p = PALETTE_MAP.get(palette.lower(), PALETTE_CURRENT) if palette else PALETTE_CURRENT
        self.ui_buffer = []
        self.use_typewriter = typewriter
        self._lock = False
        self.typewriter_speed_scalar = 1.0
        self.typewriter_speeds = {
            "title": 0.001,
            "header": 0.005,
            "notify": 0.003,
            "error": 0.002,
            "attention": 0.005,
            "default": 0.003
        }

        self._logo = r"""
██╗   ██╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ██████╗ ███████╗
██║   ██║██╔═══██╗╚██╗██╔╝    ██╔════╝ ██╔═══██╗██╔══██╗██╔════╝
██║   ██║██║   ██║ ╚███╔╝     ██║      ██║   ██║██████╔╝█████╗  
╚██╗ ██╔╝██║   ██║ ██╔██╗     ██║      ██║   ██║██╔══██╗██╔══╝  
╚████╔╝ ╚██████╔╝██╔╝ ██╗    ╚██████╗ ╚██████╔╝██║  ██║███████╗
╚═══╝   ╚═════╝ ╚═╝  ╚═╝     ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝"""

        self._logo_sub = "M i c r o k e r n e l"
        self._logo_edition = "  p y t h o n _ e d i t i o n\n"

    def _clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            sys.stdout.write('\033[2J\033[3J\033[H')
            sys.stdout.flush()

    def _print(self, text, speed_key="default"):
        self._lock = True
        
        # Clear current prompt line
        sys.stdout.write(f"\r{' ' * 60}\r")
        sys.stdout.flush()

        if self.use_typewriter:
            base_speed = self.typewriter_speeds.get(speed_key, 0.003)
            speed = base_speed * self.typewriter_speed_scalar
            
            i = 0
            while i < len(text):
                # Handle ANSI escape sequences as single atomic blocks
                if text[i] == '\033':
                    end = text.find('m', i)
                    if end != -1:
                        sys.stdout.write(text[i:end+1])
                        i = end + 1
                        continue
                
                sys.stdout.write(text[i])
                sys.stdout.flush()
                time.sleep(speed)
                i += 1
                
            sys.stdout.write('\n')
            sys.stdout.flush()
        else:
            print(text)
            
        self._lock = False

    def start(self):
        self.on_command("--ui_clear")
        self.on_command("--ui_app_title")
        self.on_command("--ui_header Service added: UI_Terminal")
        self.on_command("--ui_attention Input from system is strictly limited to the active VoxCore interface. Keystrokes are only processed when explicitly submitted, and no background keylogging or system-wide tracking is ever performed.")
        self.on_command("--ui_spacer")

    def run(self):
        while True:
            # Wait for typewriter/printing lock to release
            while self._lock: 
                time.sleep(0.05)

            prompt_str = f"\001{self.p[5]}\002VoxCore > " if USE_READLINE else f"{self.p[5]}VoxCore > "

            try:
                user_input = input(prompt_str).strip()
                
                if self._lock: 
                    continue
                
                if user_input:
                    sys.stdout.write(f"\033[F\r{' ' * 60}\r") 
                    
                    if USE_READLINE:
                        import readline
                        readline.add_history(user_input)

                    self.route_command(f"--ui_input Keyboard | {user_input}")            
                    self.route_command(user_input, "Keyboard")
                else:
                    sys.stdout.write(f"\033[F\r{' ' * 60}\r")
                    sys.stdout.flush() 
                    
            except (KeyboardInterrupt, EOFError):
                break

    def on_command(self, text: str) -> bool:
        while self._lock: 
            time.sleep(0.03)

        cmd = text.strip()
        cmd_l = cmd.lower()

        if cmd_l == "--ui_clear":
            self._clear_screen()
            self.ui_buffer.clear()
            return True

        elif cmd_l == "--ui_refresh":
            self._clear_screen()            
            old_buffer = list(self.ui_buffer)
            self.ui_buffer.clear()
            temp_typewriter_state = self.use_typewriter
            self.use_typewriter = False
            for old_cmd in old_buffer: 
                self.on_command(old_cmd)
            self.use_typewriter = temp_typewriter_state
            return True

        elif cmd_l == "--ui_typewriter":
            self.use_typewriter = not self.use_typewriter
            return True

        elif cmd_l.startswith("--ui_typewriter_speed_scalar "):
            val = cmd[29:].strip()
            try:
                self.typewriter_speed_scalar = float(val)
            except ValueError:
                pass
            return True

        elif cmd_l.startswith("--ui_typewriter_speed "):
            payload = cmd[22:].strip()
            if " " in payload:
                cat, val = payload.split(" ", 1)
                try:
                    self.typewriter_speeds[cat.lower()] = float(val)
                except ValueError:
                    pass
            return True

        elif cmd_l.startswith("--ui_palette "):
            palette_key = cmd[13:].strip().lower()
            if palette_key in PALETTE_MAP:
                self.p = PALETTE_MAP[palette_key]
                self.on_command("--ui_refresh")
            return True
        
        elif cmd_l == "--ui_app_title":
            output = f"{self.p[0]}{self._logo}\n{self.p[1]}{self._logo_sub}{self.p[2]}{self._logo_edition}{self.p[6]}"
            self._print(output, "title")
            self.ui_buffer.append(text)
            return True
        
        elif cmd_l == "--ui_spacer":
            self._print(" ", "default")
            self.ui_buffer.append(text)
            return True
            
        elif cmd_l.startswith("--ui_header "):
            msg = cmd[12:].strip()
            if msg: 
                self._print(f"{self.p[2]}{msg}{self.p[6]}", "header")
                self.ui_buffer.append(text)
            return True
            
        elif cmd_l.startswith("--ui_notify "):
            msg = cmd[12:].strip()
            if msg: 
                self._print(f"{self.p[7]}{msg}{self.p[6]}", "notify")
                self.ui_buffer.append(text)
            return True
            
        elif cmd_l.startswith("--ui_error "):
            msg = cmd[11:].strip()
            if msg: 
                self._print(f"{self.p[4]}[!]Error: {msg}{self.p[6]}", "error")
                self.ui_buffer.append(text)
            return True
            
        elif cmd_l.startswith("--ui_attention "):
            msg = cmd[15:].strip()
            if msg: 
                self._print(f"{self.p[3]}[!]Attention: {msg}{self.p[6]}", "attention")
                self.ui_buffer.append(text)
            return True

        elif cmd_l.startswith("--ui_input "):
            payload = cmd[11:].strip()
            if "|" in payload:
                cat, val = [x.strip() for x in payload.split("|", 1)]
                self._print(f"{self.p[1]}[{cat.upper()}]{self.p[5]}{val}{self.p[6]}", "default")
                self.ui_buffer.append(text)
            return True
            
        return False