// VOX_DEP: -lvosk
// VOX_PKG: 

#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <vosk_api.h>

// =====================================================
// Dependencies / External
// =====================================================

static bool (*_task_input_speech_vosk_desktop_transmit)(const int type, const void* payload, const int size, const char* source) = NULL;

// =====================================================
// Data Registry / Configuration
// =====================================================

#define _AUDIO_SAMPLE_RATE                                  16000
#define _AUDIO_BUFFER_SIZE                                  32000
#define _AUDIO_CHUNK_SIZE                                   1024

// =====================================================
// State (The Silo)
// =====================================================

static short* _task_input_speech_vosk_data_buffer            = NULL;
static int* _task_input_speech_vosk_data_buffer_write_index  = NULL;
static int* _task_input_speech_vosk_data_buffer_read_index   = NULL;

static VoskModel* _task_speech_model                        = NULL;
static VoskRecognizer* _task_speech_recognizer              = NULL;

// =====================================================
// speech buffer
// =====================================================

#define _SPEECH_TEXT_MAX                                    4096

static int _task_speech_muted                               = 0;
static char _task_speech_ui_buffer[_SPEECH_TEXT_MAX + 64]   = {0};
static char _task_speech_raw_buffer[_SPEECH_TEXT_MAX]       = {0};

// =====================================================
// Core
// =====================================================

static void _task_speech_parse(const char* json_str) 
{
    // JSON Manual
    // Define the JSON key anchor |  Locate the start of the "text" key in the raw JSON
    const char* key = "\"text\" : \"";
    char* start = strstr(json_str, key);
    if (!start) return;

    // JSON Manual
    // Shift pointer past the key and quote to the actual value | Find the closing quote that marks the end of the text
    start += strlen(key);
    char* end = strchr(start, '\"');
    if (!end) return;

    // JSON Manual : text length
    int len = (int)(end - start);
    if (len <= 0 || len >= _SPEECH_TEXT_MAX) return;

    // JSON Manual : Copy json text to buffer
    memcpy(_task_speech_raw_buffer, start, len);
    _task_speech_raw_buffer[len] = '\0';
              
    // UI
    snprintf(_task_speech_ui_buffer, sizeof(_task_speech_ui_buffer), "--ui_notify [Microphone] %s", _task_speech_raw_buffer);
    _task_input_speech_vosk_desktop_transmit(VOX_BUS_EVENT_STRING, _task_speech_ui_buffer, (int)strlen(_task_speech_ui_buffer) + 1, NULL);

    // Raw Text (for Router/Other Tasks)
    _task_input_speech_vosk_desktop_transmit(VOX_BUS_EVENT_STRING, _task_speech_raw_buffer, len + 1, NULL);
}

// =====================================================
// Task
// =====================================================

typedef bool (*VoxEventBusTransmit)(const int, const void*, const int, const char*);

static inline void task_input_speech_vosk_desktop_boot(VoxEventBusTransmit transmit)
{
    // Guard
    if (!transmit) return;
    _task_input_speech_vosk_desktop_transmit = transmit;

    // Vosk : Silence internal technical logs to maintain a clean console output
    vosk_set_log_level(-1);

    // Vosk : Load model (Early return if folder is missing or corrupt)
    _task_speech_model = vosk_model_new("models/vosk-model-small-en");
    if (!_task_speech_model) return;

    // Vosk : Initialize recognizer at the unified sample rate
    _task_speech_recognizer = vosk_recognizer_new(_task_speech_model, _AUDIO_SAMPLE_RATE);
    if (!_task_speech_recognizer) return;

    // UI
    const char* msg = "--ui_notify_header Task booted: Input_Speech";
    _task_input_speech_vosk_desktop_transmit(VOX_BUS_EVENT_STRING, msg, (int)strlen(msg) + 1, NULL);
}

static inline void task_input_speech_vosk_desktop_run(float delta_time) 
{
    // Guard
    if (!_task_input_speech_vosk_data_buffer || !_task_speech_recognizer || _task_speech_muted)
        return;

    // Audio : Local storage for the current processing slice
    short temp_buffer[_AUDIO_BUFFER_SIZE];
    int frames = 0;    

    // Ring Buffer : Catch up to data buffer | Sample-by-sample copy applies modulo wrap at every index to avoid multi-stage memcpy logic
    short* data_buffer =  _task_input_speech_vosk_data_buffer;
    int* data_buffer_write_index =  _task_input_speech_vosk_data_buffer_write_index;
    int* data_buffer_read_index = _task_input_speech_vosk_data_buffer_read_index;

    while (*data_buffer_read_index != *data_buffer_write_index && frames < _AUDIO_BUFFER_SIZE) 
    {
        temp_buffer[frames++] = data_buffer[*data_buffer_read_index];
        *data_buffer_read_index = (*data_buffer_read_index + 1) % _AUDIO_BUFFER_SIZE;
    }

    // Vosk : Feed waveform to engine | Trigger parser if final result is ready
    if (frames > 0 && vosk_recognizer_accept_waveform(_task_speech_recognizer, (const char*)temp_buffer, frames * (int)sizeof(short))) 
        _task_speech_parse(vosk_recognizer_result(_task_speech_recognizer));
}

void task_input_speech_vosk_desktop_terminate() 
{
    // Vosk: Free
    if (_task_speech_recognizer) vosk_recognizer_free(_task_speech_recognizer);
    if (_task_speech_model) vosk_model_free(_task_speech_model);
}

bool task_input_speech_vosk_desktop_on_event_bus(const int type, const void* payload, const int size, const char* source) 
{
    // Data buffer
    if (type == VOX_BUS_EVENT_MIC_POINTER)
    {
        void** state = (void**)payload;
        _task_input_speech_vosk_data_buffer = (short*)state[0];
        _task_input_speech_vosk_data_buffer_write_index = (int*)state[1];
        _task_input_speech_vosk_data_buffer_read_index = (int*)state[2];
        return true;
    }

    // Other
    if (type == VOX_BUS_EVENT_STRING)
    {
        const char* payload_c = (const char*)payload;
        if (strcmp(payload_c, "--mic_mute") == 0 || strcmp(payload_c, "--mic_off") == 0) return (_task_speech_muted = 1), true;
        if (strcmp(payload_c, "--mic_on") == 0 || strcmp(payload_c, "--mic_unmute") == 0) return (_task_speech_muted = 0), true;
    }
    return false;
}