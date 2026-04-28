import os
import mpv
import platform
import string

# Radio stations
# IDs must be in lower
RADIO_STATIONS = {
    "fallout radio web": "https://www.youtube.com/watch?v=6qQ0TMK7ZuE",
    "fallout sleep web": "https://www.youtube.com/watch?v=0sJcSgs8CIU",
    "persona 3 reload rainy web": "https://www.youtube.com/watch?v=iCyHMKAVT8E&list=RDiCyHMKAVT8E&start_radio=1"
}

class TaskOutputRadioMpvDesktop:
    command = "--task_output_radio_mpv_desktop"
        
    def __init__(self, command_router_function, flags=None):
        self.route_command = command_router_function
        self.flags = flags if flags is not None else {}
        self.player = None
        self.station_name = ""
        self.player = mpv.MPV(ytdl=True, video=False)
        self.player.ytdl_format = "bestaudio/best"
             
    def boot(self):
        self.route_command("--ui_header Task booted: Output_Radio_MPV_Desktop")
        self._local_files_home_load()
        self._local_files_external_load()
    
    def terminate(self):
        self.player.terminate()
        self.player = None
        self.route_command("--ui_header Task terminated: Output_Radio_MPV_Desktop")

    def run(self, delta_time: float):
            pass
        
    def on_command(self, command: str) -> bool:
        command_lower = command.lower()

        # Radio volume
        if command_lower.startswith("--radio_volume "):
            try:
                self.player.volume = max(0, min(int(command_lower[15:].strip() or 0),100))
            except (ValueError, IndexError):
                return False

        # Radio play
        if command_lower.startswith("--radio_play "):
            id = command_lower[12:].strip()
            if id in RADIO_STATIONS: 
                self._radio_play(id, RADIO_STATIONS[id])
                return True
        
        # Radio stop
        if command_lower == "--radio_stop":
           self._radio_stop()
           return True
           
        return False
    
    def _local_files_home_load(self):
        # Automatically find the user's home directory and music folder(Works on Win/Mac/Linux)
        home_dir = os.path.expanduser("~")
        music_path = os.path.join(home_dir, "Music")
        if not os.path.exists(music_path):
            print(f"Warning: Music folder not found at {music_path}")
            return

        # Get files
        for filename in os.listdir(music_path):
            if filename.lower().endswith((".mp3", ".wav", ".m4a", ".flac", ".ogg")):
                station_name = os.path.splitext(filename)[0].lower()
                full_path = os.path.join(music_path, filename)
                RADIO_STATIONS[station_name] = full_path

    def _local_files_external_load(self):
        # Get OS
        current_os = platform.system()
        drive_roots = []

        # Path: Windows
        # Get valid drive letters (D:\ through Z:\)  
        if current_os == "Windows":
            for letter in string.ascii_uppercase:
                if letter not in ['A', 'B', 'C'] and os.path.exists(f"{letter}:\\"):
                    drive_roots.append(f"{letter}:\\")

        # Path: Mac
        # Get mounted volumes on macOS
        elif current_os == "Darwin": 
            if os.path.exists("/Volumes"):
                for volume in os.listdir("/Volumes"):
                    volume_path = os.path.join("/Volumes", volume)
                    if os.path.isdir(volume_path):
                        drive_roots.append(volume_path)

        # Path : Linux
        # Get mounted drives on Linux
        elif current_os == "Linux":
            user = os.environ.get("USER", os.environ.get("LOGNAME", ""))
            for base in [f"/media/{user}", f"/run/media/{user}", "/mnt"]:
                if os.path.exists(base):
                    for mount in os.listdir(base):
                        mount_path = os.path.join(base, mount)
                        if os.path.isdir(mount_path):
                            drive_roots.append(mount_path)

        # Get files
        for root in drive_roots:
            for folder_name in ["Music", "music"]:
                music_path = os.path.join(root, folder_name)
                if os.path.exists(music_path):
                    try:
                        for filename in os.listdir(music_path):
                            if filename.lower().endswith((".mp3", ".wav", ".m4a", ".flac", ".ogg")):
                                station_name = os.path.splitext(filename)[0].lower()
                                full_path = os.path.join(music_path, filename)
                                RADIO_STATIONS[station_name] = full_path
                    except PermissionError:
                        self.route_command(f"--ui_error Permission denied accessing: {music_path}")

    def _radio_play(self, station_name, url):
        try:
            self.station_name = station_name
            self.stream_url = url
            self.route_command(f"--ui_header Radio started: {self.station_name}\nURL: {self.stream_url}")
            self.player.play(self.stream_url)
        except Exception as e:
            self.route_command(f"--ui_error Error starting stream: {e}")

    def _radio_stop(self):
        try:
            self.route_command(f"--ui_header Radio stopped: {self.station_name}\nURL: {self.stream_url}")
            self.player.stop()
            self.station_name = ""
            self.stream_url = ""
        except Exception as e:
            self.route_command(f"--ui_error Error stopping stream: {e}")

    