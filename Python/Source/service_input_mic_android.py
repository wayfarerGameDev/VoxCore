import sys
import os
import time
import threading
import logging

# Android only
# Termux uniquely sets a PREFIX environment variable. 
# We check this to definitively know if we are on Android.
is_android = hasattr(sys, 'getandroidapilevel') or 'com.termux' in os.environ.get('PREFIX', '')

if is_android:
    import speech_recognition as sr
    from flask import Flask, request, render_template_string

    class ServiceInputMicAndroid:
        command = "--service_input_mic_android"
        
        def __init__(self, command_router_function):
            self.route_command = command_router_function 
            self.recognizer = sr.Recognizer()
            self.muted = False
            self.is_listening = False
            
            self.hallucinations = [
                "thank you.", "thank you", "thanks for watching", 
                "thanks for watching.", "please subscribe.", "you", 
                "...", "ammen", "bye.", "peace out."
            ]

            # --- FLASK SETUP ---
            self.app = Flask(__name__)
            
            # Disable Flask's default terminal spam so it doesn't ruin your CLI UI
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            
            self.server_thread = None
            self._setup_routes()

        def _setup_routes(self):
            @self.app.route('/')
            def index():
                # The hidden webpage that records from Android Chrome
                html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Whisper Mic Service</title>
                </head>
                <body style="background:#121212; color:#ffffff; font-family:sans-serif; text-align:center; padding-top:20vh; margin:0;">
                    <h2 style="color: #4CAF50;">Python Audio Service</h2>
                    <p style="color: #aaa; margin-bottom: 30px;">Keep this tab open to stream microphone to Termux.</p>
                    
                    <button id="startBtn" style="padding:20px 40px; font-size:18px; background:#4CAF50; border:none; border-radius:10px; color:white; font-weight:bold; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        Start Microphone Sync
                    </button>
                    
                    <p id="status" style="margin-top: 30px; font-size: 16px; color: #888;">Waiting for user...</p>

                    <script>
                        let mediaRecorder;
                        let audioChunks = [];

                        document.getElementById('startBtn').onclick = async () => {
                            try {
                                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                                mediaRecorder = new MediaRecorder(stream);
                                
                                document.getElementById('status').innerText = "🔴 Listening and streaming to Termux...";
                                document.getElementById('status').style.color = "#ff5252";
                                document.getElementById('startBtn').style.display = 'none';

                                mediaRecorder.ondataavailable = event => {
                                    audioChunks.push(event.data);
                                };

                                mediaRecorder.onstop = async () => {
                                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                                    audioChunks = [];
                                    
                                    // Send audio to Python backend
                                    const formData = new FormData();
                                    formData.append('audio', audioBlob, 'chunk.webm');
                                    
                                    try {
                                        await fetch('/upload', { method: 'POST', body: formData });
                                    } catch(e) {
                                        console.error("Connection to Termux lost.");
                                    }
                                    
                                    // Loop to record next chunk
                                    mediaRecorder.start();
                                    setTimeout(() => { mediaRecorder.stop(); }, 3500); // 3.5 second chunks
                                };

                                mediaRecorder.start();
                                setTimeout(() => { mediaRecorder.stop(); }, 3500);
                            } catch (err) {
                                document.getElementById('status').innerText = "Error: Please grant microphone permissions in Chrome.";
                            }
                        };
                    </script>
                </body>
                </html>
                """
                return render_template_string(html)

            @self.app.route('/upload', methods=['POST'])
            def upload():
                if self.muted or not self.is_listening:
                    return "Ignored", 200

                if 'audio' not in request.files:
                    return "No audio", 400

                # Save the incoming webm audio chunk
                audio_file = request.files['audio']
                
                # Use a unique timestamp to prevent file collision if processing is slow
                temp_path = f"temp_chunk_{int(time.time()*1000)}.webm"
                audio_file.save(temp_path)

                # Process the audio in a separate thread to keep the web server fast
                threading.Thread(target=self._process_audio, args=(temp_path,), daemon=True).start()
                
                return "Received", 200

        def _process_audio(self, filepath):
            wav_path = filepath.replace(".webm", ".wav")
            try:
                # Convert webm to wav (Whisper/speech_recognition needs wav/flac format)
                os.system(f"ffmpeg -y -i {filepath} -ar 16000 {wav_path} >/dev/null 2>&1")

                with sr.AudioFile(wav_path) as source:
                    audio = self.recognizer.record(source)

                text = self.recognizer.recognize_whisper(audio, model="tiny.en").strip()
                
                if text and len(text) >= 2 and text.lower() not in self.hallucinations:
                    sys.stdout.write('\r\033[K') 
                    sys.stdout.flush()
                    
                    self.route_command(f"--ui_input Android Chrome | {text}")
                    self.route_command(text, "Microphone")
                    self._refresh_prompt()
                    
            except sr.UnknownValueError:
                pass
            except Exception as e:
                pass
            finally:
                # Clean up temp files
                if os.path.exists(filepath): 
                    os.remove(filepath)
                if os.path.exists(wav_path): 
                    os.remove(wav_path)

        def _refresh_prompt(self):
            self.route_command("--ui_prompt")

        def _run_server(self):
            # Run Flask on port 5000. host='0.0.0.0' allows Chrome to connect
            self.app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

        def start(self):
            if self.is_listening: return

            self.is_listening = True
            self.route_command("--ui_header Service added: Input_Mic_Android")
            self.route_command("--ui_notify Please open http://127.0.0.1:5000 in your Android Chrome browser.")
            self.route_command("--ui_spacer")

            # Start the web server in a background thread
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()

        def stop(self):
            self.is_listening = False
            self.route_command("--ui_notify Service removed: Input_Mic_Android.")
            self._refresh_prompt()

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
            
# Fallback for desktops / non-Android devices
else:
   class ServiceInputMicAndroid:
        command = "--service_input_mic_android"
        
        def __init__(self, command_router_function):
            self.route_command = command_router_function

        def start(self):
           self.route_command("--ui_error Service not supported on this OS: Input_Mic_Android")

        def stop(self):
            pass

        def on_command(self, text: str) -> bool:
            return False