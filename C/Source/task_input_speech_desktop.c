// VOX_DEP: -lportaudio -lvosk
// VOX_PKG: 

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <portaudio.h>
#include <vosk_api.h>

// =====================================================
// Dependencies / External
// =====================================================

// Injected at runtime via boot
static bool (*_task_input_speech_desktop_transmit)(const int type, const void* payload, const int size, const char* source) = NULL;

// =====================================================
// Data Registry / Configuration
// =====================================================
#define _SPEECH_SAMPLE_RATE                                 16000
#define _SPEECH_CHANNELS                                    1
#define _SPEECH_MAX_TEXT_SIZE                               512
#define _SPEECH_MODEL_PATH                                  "models/vosk-model-small-en"

// =====================================================
// State (The Silo)
// =====================================================
static PaStream* _task_speech_pa_stream      = NULL;
static VoskModel* _task_speech_model          = NULL;
static VoskRecognizer* _task_speech_recognizer     = NULL;

static int                      _task_speech_muted          = 0;
static char                     _task_speech_ui_buffer[1024] = {0};
static char                     _task_speech_raw_buffer[_SPEECH_MAX_TEXT_SIZE] = {0};

// Hallucination filter (Matches your Python list)
static const char* _task_speech_junk[] = {
    "thank you.", "thank you", "thanks for watching", "thanks for watching.",
    "please subscribe.", "you", "...", "ammen", "bye.", "peace out."
};

// =====================================================
// Private Logic
// =====================================================

static void _task_speech_ui_send(const char* text)
{
    if (_task_input_speech_desktop_transmit == NULL || _task_speech_muted) return;

    // 1. Length and Junk Filter
    if (strlen(text) < 2) return;
    for (int i = 0; i < 10; i++) 
    {
        if (strcasecmp(text, _task_speech_junk[i]) == 0) return;
    }

    // 2. Format: --ui_input Microphone | {text}
    snprintf(_task_speech_ui_buffer, sizeof(_task_speech_ui_buffer), "--ui_notify Microphone | %s", text);
    _task_input_speech_desktop_transmit(VOX_BUS_EVENT_STRING, _task_speech_ui_buffer, (int)strlen(_task_speech_ui_buffer) + 1, "task_input_speech_desktop");

    // 3. Dispatch raw text as command (for the router)
    _task_input_speech_desktop_transmit(VOX_BUS_EVENT_STRING, text, (int)strlen(text) + 1, "Microphone");
}

static void _task_speech_parse_json(const char* json_str) 
{
    const char* key = "\"text\" : \"";
    char* start = strstr(json_str, key);
    
    if (start != NULL) 
    {
        start += strlen(key);
        char* end = strchr(start, '\"');
        
        if (end != NULL) 
        {
            int len = end - start;
            if (len > 0 && len < _SPEECH_MAX_TEXT_SIZE) 
            {
                memcpy(_task_speech_raw_buffer, start, len);
                _task_speech_raw_buffer[len] = '\0';
                _task_speech_ui_send(_task_speech_raw_buffer);
            }
        }
    }
}

// PortAudio Callback
static int _task_speech_pa_callback(
    const void *inputBuffer, void *outputBuffer,
    unsigned long framesPerBuffer,
    const PaStreamCallbackTimeInfo* timeInfo,
    PaStreamCallbackFlags statusFlags,
    void *userData)
{
    if (_task_speech_muted || _task_speech_recognizer == NULL) return paContinue;

    // Feed bits to Vosk. Returns 1 when a sentence is finalized.
    if (vosk_recognizer_accept_waveform(_task_speech_recognizer, (const char*)inputBuffer, framesPerBuffer * sizeof(short))) 
    {
        _task_speech_parse_json(vosk_recognizer_result(_task_speech_recognizer));
    }
    
    return paContinue;
}

// =====================================================
// Public Task Lifecycle
// =====================================================

typedef bool (*VoxEventBusTransmit)(const int, const void*, const int, const char*);

static inline void task_input_speech_desktop_boot(VoxEventBusTransmit transmit)
{
    if (transmit == NULL) return;
    _task_input_speech_desktop_transmit = transmit;

    // 1. Init Vosk
    vosk_set_log_level(-1);
    _task_speech_model = vosk_model_new(_SPEECH_MODEL_PATH);
    if (_task_speech_model == NULL) return;
    _task_speech_recognizer = vosk_recognizer_new(_task_speech_model, _SPEECH_SAMPLE_RATE);

    // 2. Init PortAudio
    Pa_Initialize();
    
    PaStreamParameters inputParams;
    inputParams.device = Pa_GetDefaultInputDevice();
    if (inputParams.device == paNoDevice) return;

    inputParams.channelCount = _SPEECH_CHANNELS;
    inputParams.sampleFormat = paInt16;
    inputParams.suggestedLatency = Pa_GetDeviceInfo(inputParams.device)->defaultLowInputLatency;
    inputParams.hostApiSpecificStreamInfo = NULL;

    PaError err = Pa_OpenStream(
        &_task_speech_pa_stream,
        &inputParams,
        NULL, 
        _SPEECH_SAMPLE_RATE,
        1024,  // Buffer frames
        paClipOff,
        _task_speech_pa_callback,
        NULL
    );

    if (err == paNoError) 
    {
        Pa_StartStream(_task_speech_pa_stream);
        const char* msg = "--ui_notify_header Task booted: Input_Speech (PortAudio)";
        _task_input_speech_desktop_transmit(VOX_BUS_EVENT_STRING, msg, (int)strlen(msg) + 1, "task_input_speech_desktop");
    }
}

static inline void task_input_speech_desktop_run(float delta_time) 
{
}

void task_input_speech_desktop_terminate() 
{
    if (_task_speech_pa_stream) 
    {
        Pa_StopStream(_task_speech_pa_stream);
        Pa_CloseStream(_task_speech_pa_stream);
    }
    Pa_Terminate();

    if (_task_speech_recognizer) vosk_recognizer_free(_task_speech_recognizer);
    if (_task_speech_model) vosk_model_free(_task_speech_model);
}

bool task_input_speech_desktop_on_event_bus(const int type, const void* payload, const int size, const char* source) 
{
    if (type == VOX_BUS_EVENT_STRING)
    {
        const char* cmd = (const char*)payload;
        if (strcmp(cmd, "--mic_mute") == 0 || strcmp(cmd, "--mic_off") == 0) 
        {
            _task_speech_muted = 1;
            return true;
        }
        if (strcmp(cmd, "--mic_on") == 0 || strcmp(cmd, "--mic_unmute") == 0) 
        {
            _task_speech_muted = 0;
            return true;
        }
    }
    return false;
}