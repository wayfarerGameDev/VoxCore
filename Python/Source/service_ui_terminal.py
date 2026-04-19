import os   
import sys
import time

# Iconic Tech & IDE Themes
PALETTE_DRACULA         = ['#af87ff', '#ff87d7', '#5fff87', '#ffff87', '#ff5f5f', '#ffffff', '#8787af', '#af87ff']
PALETTE_GRUVBOX         = ['#ffaf00', '#ff8700', '#afaf00', '#d78700', '#afaf00', '#ffd7af', '#767676', '#ffaf00']
PALETTE_NORD            = ['#87afd7', '#5f87af', '#afd787', '#d7af87', '#d75f5f', '#87afff', '#767676', '#87afd7']
PALETTE_MONOKAI         = ['#ff005f', '#afd700', '#5fd7ff', '#ff8700', '#d7005f', '#ffffff', '#6c6c6c', '#ff005f']
PALETTE_OCEANIC         = ['#00afd7', '#0087d7', '#5fd7af', '#ffd75f', '#ff5f5f', '#afd7d7', '#5f8787', '#00afd7']
PALETTE_SOLAR           = ['#0087ff', '#00afaf', '#5f8700', '#af8700', '#d70000', '#8a8a8a', '#8a8a8a', '#0087ff']

# Retro Hardware & Gaming
PALETTE_PIPBOY_GREEN    = ['#00ff5f', '#008700', '#00ff00', '#5fff00', '#ff0000', '#87ffaf', '#005f00', '#00ff5f']
PALETTE_PIPBOY_AMBER    = ['#ff8700', '#af5f00', '#ffaf00', '#ff5f00', '#d75f00', '#ffaf5f', '#875f00', '#ff8700']
PALETTE_PIPBOY_BLUE     = ['#00ffff', '#0087af', '#00d7ff', '#00afff', '#005f87', '#87ffff', '#005f5f', '#00ffff']
PALETTE_PIPBOY_WHITE    = ['#eeeeee', '#808080', '#d0d0d0', '#bcbcbc', '#a8a8a8', '#ffffff', '#585858', '#eeeeee']
PALETTE_PIPBOY_RED      = ['#ff0000', '#870000', '#d70000', '#af0000', '#5f0000', '#ff5f5f', '#5f0000', '#ff0000']
PALETTE_PIPBOY_PURPLE   = ['#d75fff', '#8700ff', '#af5fff', '#af00ff', '#5f00af', '#d7afff', '#5f0087', '#d75fff']
PALETTE_PIPBOY_YELLOW   = ['#ffff00', '#878700', '#ffd700', '#d7d700', '#af8700', '#ffffaf', '#5f5f00', '#ffff00']
PALETTE_PIPBOY_PINK     = ['#ff87ff', '#d70087', '#ff5faf', '#ff00d7', '#87005f', '#ffafff', '#5f005f', '#ff87ff']
PALETTE_AMBER           = ['#ffaf00', '#d78700', '#ffd700', '#ffaf00', '#ff0000', '#ffaf5f', '#af5f00', '#ffaf00']
PALETTE_PHOSPHOR        = ['#00ff00', '#008700', '#87ff87', '#00ff00', '#af0000', '#5fff87', '#005f00', '#00ff00']
PALETTE_C64             = ['#5f5fff', '#8787ff', '#87afff', '#ffff5f', '#d70000', '#afd7ff', '#00005f', '#5f5fff']
PALETTE_GAMEBOY         = ['#005f00', '#5f8700', '#008700', '#878700', '#5f0000', '#87af5f', '#5f8700', '#005f00']
PALETTE_MATRIX          = ['#00ff00', '#005f00', '#87ff87', '#d7ff00', '#af0000', '#00ff87', '#00ff00', '#00ff00']

# Original & Custom "Vox" Themes
PALETTE_DUSTY           = ['#d75f5f', '#8787af', '#87af87', '#d7d787', '#af5f5f', '#d0d0d0', '#8787af', '#d75f5f']
PALETTE_FOREST          = ['#00af00', '#5f875f', '#87d75f', '#afaf00', '#870000', '#d7ffd7', '#5f875f', '#00af00']
PALETTE_MIDNIGHT        = ['#ff0087', '#00d7ff', '#00ff00', '#ffaf00', '#d70000', '#00d7ff', '#00d7ff', '#ff0087']
PALETTE_VOID            = ['#eeeeee', '#303030', '#a8a8a8', '#808080', '#af0000', '#dadada', '#080808', '#eeeeee']
PALETTE_BONE            = ['#d0d0d0', '#808080', '#bcbcbc', '#a8a8a8', '#444444', '#eeeeee', '#808080', '#d0d0d0']

# High-Energy & Aesthetic
PALETTE_SYNTH           = ['#ff00ff', '#af00ff', '#00ffff', '#ffff00', '#ff005f', '#00ffff', '#5f5faf', '#ff00ff']
PALETTE_VAPOR           = ['#ff00ff', '#d75fff', '#00ffff', '#ffff00', '#ff5f87', '#00ffff', '#d75fff', '#ff00ff']
PALETTE_CYBER           = ['#ffff00', '#00ffff', '#ff00ff', '#00ff00', '#ff0000', '#00ffff', '#00ffff', '#ffff00']
PALETTE_SAKURA          = ['#ffafaf', '#ffd7ff', '#ff87af', '#ffd75f', '#ff0000', '#eeeeee', '#d0d0d0', '#ffafaf']

# Earth & Elemental
PALETTE_OASIS           = ['#5faf87', '#5f8787', '#87d7af', '#d7af5f', '#af5f5f', '#d7ffd7', '#005f5f', '#5faf87']
PALETTE_LAVA            = ['#ff0000', '#ff5f00', '#ff8700', '#ffaf00', '#d70000', '#ffffd7', '#6c6c6c', '#ff0000']
PALETTE_GLACIER         = ['#87d7ff', '#87afff', '#afd7ff', '#eeeeee', '#005f87', '#d7ffff', '#87afaf', '#87d7ff']
PALETTE_COFFEE          = ['#875f00', '#af875f', '#af8787', '#d7af87', '#5f0000', '#ffffd7', '#444444', '#875f00']
PALETTE_CRIMSON         = ['#d70000', '#870000', '#ff0000', '#ff5f00', '#5f0000', '#eeeeee', '#870000', '#d70000']
PALETTE_STEEL           = ['#808080', '#585858', '#bcbcbc', '#a8a8a8', '#262626', '#eeeeee', '#585858', '#808080']
PALETTE_WINDBLOWN       = ['#87d7ff', '#808080', '#afff87', '#ffd787', '#d75f5f', '#eeeeee', '#585858', '#87d7ff']

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
        
        # Initialize internal color system
        self.hex_palette = []
        self.p = []
        initial_hex_list = PALETTE_MAP.get(palette.lower(), PALETTE_CURRENT) if palette else PALETTE_CURRENT
        self._set_palette(initial_hex_list)
        
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

    def _set_palette(self, hex_list):
        self.hex_palette = hex_list
        self.p = []
        # Compile text hex codes to 24-bit TrueColor ANSI
        for hex_code in hex_list[:8]:
            h = hex_code.lstrip('#')
            r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            self.p.append(f"\033[38;2;{r};{g};{b}m")
        self._set_cursor_color(self.hex_palette[5])

    def _set_cursor_color(self, hex_color):
        sys.stdout.write(f"\033]12;{hex_color}\a")
        sys.stdout.flush()

    def _clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            sys.stdout.write('\033[2J\033[3J\033[H')
            sys.stdout.flush()

    def _print(self, text, speed_key="default", color_hex=None):
        self._lock = True
        
        # Dynamically shift cursor to match the element about to be printed
        if color_hex:
            self._set_cursor_color(color_hex)
        
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
        try:
            while True:
                # Wait for typewriter/printing lock to release
                while self._lock: 
                    time.sleep(0.05)

                prompt_str = f"\001{self.p[5]}\002VoxCore > " if USE_READLINE else f"{self.p[5]}VoxCore > "
                
                # Reset cursor color to match the prompt before asking for input
                self._set_cursor_color(self.hex_palette[5])

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
        finally:
            sys.stdout.write("\033]112;\a\033[0m\n")
            sys.stdout.flush()

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
                self._set_palette(PALETTE_MAP[palette_key])
                self.on_command("--ui_refresh")
            return True
        
        elif cmd_l == "--ui_app_title":
            output = f"{self.p[0]}{self._logo}\n{self.p[1]}{self._logo_sub}{self.p[2]}{self._logo_edition}\033[0m"
            self._print(output, "title", self.hex_palette[0])
            self.ui_buffer.append(text)
            return True
        
        elif cmd_l == "--ui_spacer":
            self._print(" ", "default", self.hex_palette[5])
            self.ui_buffer.append(text)
            return True
            
        elif cmd_l.startswith("--ui_header "):
            msg = cmd[12:].strip()
            if msg: 
                self._print(f"{self.p[2]}{msg}\033[0m", "header", self.hex_palette[2])
                self.ui_buffer.append(text)
            return True
            
        elif cmd_l.startswith("--ui_notify "):
            msg = cmd[12:].strip()
            if msg: 
                self._print(f"{self.p[6]}{msg}\033[0m", "notify", self.hex_palette[6])
                self.ui_buffer.append(text)
            return True
            
        elif cmd_l.startswith("--ui_error "):
            msg = cmd[11:].strip()
            if msg: 
                self._print(f"{self.p[4]}[!]Error: {msg}\033[0m", "error", self.hex_palette[4])
                self.ui_buffer.append(text)
            return True
            
        elif cmd_l.startswith("--ui_attention "):
            msg = cmd[15:].strip()
            if msg: 
                self._print(f"{self.p[3]}[!]Attention: {msg}\033[0m", "attention", self.hex_palette[3])
                self.ui_buffer.append(text)
            return True

        elif cmd_l.startswith("--ui_input "):
            payload = cmd[11:].strip()
            if "|" in payload:
                cat, val = [x.strip() for x in payload.split("|", 1)]
                self._print(f"{self.p[1]}[{cat.upper()}]\033[0m{self.p[5]}{val}\033[0m", "default", self.hex_palette[5])
                self.ui_buffer.append(text)
            return True
            
        return False