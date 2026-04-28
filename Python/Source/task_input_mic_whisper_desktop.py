import speech_recognition as sr
import sys
import time

class TaskInputMicWhisperDesktop:
    command = "--task_input_mic_whisper_desktop"
    
    def __init__(self, command_router_function, flags=None):
        self.route_command = command_router_function
        self.flags = flags if flags is not None else {}
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.is_listening = False
        self.stop_listening_func = None
        self.muted = False

        self.hallucinations = [
            "thank you.", "thank you", "thanks for watching", 
            "thanks for watching.", "please subscribe.", "you", 
            "...", "ammen", "bye.", "peace out."
        ]

    def boot(self):
        if self.is_listening: return

        self.route_command("--ui_header Task booted: Input_Mic_Whisper_Desktop")
        
        # --- THE SAFETY BUFFER ---
        # Pause ensures the keyboard listener (pynput) 
        # is fully registered with macOS before we hit the mic
        time.sleep(0)

        self.route_command("--ui_debug Calibrating microphone for ambient noise...")

        with self.mic as source:
            # Slightly tighter calibration for speed
            # self.recognizer.adjust_for_ambient_noise(source, duration=1)
            # self.recognizer.energy_threshold += 150 
            # self.recognizer.pause_threshold = 0.7 

            # Longer sentances
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.energy_threshold += 150 
            self.recognizer.pause_threshold = 1.5
            self.recognizer.phrase_threshold = 0.25
            self.recognizer.non_speaking_duration = 0.8
            
           
        self.route_command("--ui_debug Calibrated and Listening.")
        if self.flags["debug"]:
            self.route_command("--ui_spacer")

        self.stop_listening_func = self.recognizer.listen_in_background(self.mic, self._audio_callback)
        self.is_listening = True

    def terminate(self):
        if self.stop_listening_func:
            self.stop_listening_func(wait_for_stop=False)
            self.is_listening = False
            self.stop_listening_func = None
            self.route_command("--ui_header Task terminated: Input_Mic_Whisper_Desktop")
            self._refresh_prompt()

    def run(self, delta_time: float):
            pass
        
    def on_command(self, text: str) -> bool:
        text_clean = text.lower().strip()

        if text_clean in ["--mic_off", "--mic_mute"]:
            self.muted = True
            self.route_command("--ui_notify [Microphone MUTED]")
            self._refresh_prompt()
            
        elif text_clean in ["--mic_on", "--mic_unmute"]:
            self.muted = False
            self.route_command("--ui_notify [Microphone LISTENING]")
            self._refresh_prompt()
            
        elif text_clean == "--mic_toggle":
            self.muted = not self.muted
            status = "MUTED" if self.muted else "LISTENING"
            self.route_command(f"--ui_notify [Microphone {status}]")
            self._refresh_prompt()
            
        return False
    
    def _audio_callback(self, recognizer, audio):
        # Drop audio immediately if muted
        if self.muted:
            return

        try:
            # --- ENGINE: tiny.en is much faster than base.en ---
            text = recognizer.recognize_whisper(audio, model="tiny.en").strip()
            
            if not text or len(text) < 2 or text.lower() in self.hallucinations:
                return 

            sys.stdout.write('\r\033[K') 
            sys.stdout.flush()
            
            self.route_command(f"--ui_input Microphone | {text}")
            self.route_command(text, "Microphone")
            self._refresh_prompt()
            
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            self.route_command(f"--ui_error Listener failed: {e}")
            self._refresh_prompt()

    def _refresh_prompt(self):
       self.route_command("--ui_prompt")