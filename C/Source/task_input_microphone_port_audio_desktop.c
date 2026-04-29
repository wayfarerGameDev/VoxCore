// VOX_DEP: -lportaudio
// VOX_PKG: 

#include <string.h>
#include <stdbool.h>
#include <portaudio.h>

// =====================================================
// Dependencies / External
// =====================================================
static bool (*_task_input_microphone_port_audio_desktop_transmit)(const int type, const void* payload, const int size, const char* source) = NULL;

// =====================================================
// Data Registry / Configuration
// =====================================================

#define _AUDIO_SAMPLE_RATE                                  16000
#define _AUDIO_BUFFER_SIZE                                  32000
#define _AUDIO_CHUNK_SIZE                                   1024

// =====================================================
// State (The Silo)
// =====================================================
static PaStream* _task_mic_pa_stream = NULL;

static short _task_mic_buffer[_AUDIO_BUFFER_SIZE] = {0};
static int _task_mic_write_index = 0;
static int _task_mic_read_index = 0;

// =====================================================
// Private Logic
// =====================================================
static int _task_mic_pa_callback(const void *input_buffer, void *unused_output_buffer, unsigned long frames_per_buffer, const PaStreamCallbackTimeInfo* unused_time_info, PaStreamCallbackFlags unused_status_flags, void *unused_user_data)
{
    const short* input = (const short*)input_buffer;
    for (unsigned long i = 0; i < frames_per_buffer; i++) 
    {
        _task_mic_buffer[_task_mic_write_index] = input[i];
        _task_mic_write_index = (_task_mic_write_index + 1) % _AUDIO_BUFFER_SIZE;
    }
    return paContinue;
}

// =====================================================
// Public Task Lifecycle
// =====================================================
typedef bool (*VoxEventBusTransmit)(const int, const void*, const int, const char*);

static inline void task_input_microphone_port_audio_desktop_boot(VoxEventBusTransmit transmit)
{
    // Guard
    if (!transmit) return;
    _task_input_microphone_port_audio_desktop_transmit = transmit;

    // UI
    const char* msg = "--ui_notify_header Task booted: Input_Microphone";
    _task_input_microphone_port_audio_desktop_transmit(VOX_BUS_EVENT_STRING, msg, (int)strlen(msg) + 1, NULL);

    // Mic state: send through event bus so other tasks can "sync" with data
    static void* task_mic_state[3] = {_task_mic_buffer, &_task_mic_write_index, &_task_mic_read_index};
    _task_input_microphone_port_audio_desktop_transmit(VOX_BUS_EVENT_MIC_POINTER, task_mic_state, sizeof(task_mic_state), NULL);

    // Port audio : Initalize
    Pa_Initialize();

    // Port audio : Set input device
    int default_device = Pa_GetDefaultInputDevice();
    if (default_device == paNoDevice) return;

    // Port audio: input parameters
    PaStreamParameters input_params = 
    {
        .device = default_device,
        .channelCount = 1,
        .sampleFormat = paInt16,
        .suggestedLatency = Pa_GetDeviceInfo(default_device)->defaultLowInputLatency,
        .hostApiSpecificStreamInfo = NULL
    };
    
    // Port audio: start stream
    if (Pa_OpenStream(&_task_mic_pa_stream, &input_params, NULL, _AUDIO_SAMPLE_RATE, _AUDIO_CHUNK_SIZE, paClipOff, _task_mic_pa_callback, NULL) == paNoError) 
        Pa_StartStream(_task_mic_pa_stream);
}

static inline void task_input_microphone_port_audio_desktop_run(float delta_time) 
{

}

void task_input_microphone_port_audio_desktop_terminate() 
{
    // Port audio: stop stream
    if (_task_mic_pa_stream) 
    {
        Pa_StopStream(_task_mic_pa_stream);
        Pa_CloseStream(_task_mic_pa_stream);
    }

    // Port audio: terminate
    Pa_Terminate();
}

bool task_input_microphone_port_audio_desktop_on_event_bus(const int type, const void* payload, const int size, const char* source) 
{
    return false;
}