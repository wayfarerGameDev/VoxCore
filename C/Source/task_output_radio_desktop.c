// VOX_PKG: mpv
// VOX_DEP: -lmpv

#include <mpv/client.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>

// =====================================================
// Platform
// =====================================================

#if defined(_WIN32)
    #include <windows.h>
    #include <stdlib.h>
    #define OUTPUT_RADIO_DIRECTORY_HOME getenv("USERPROFILE")
    #define OUTPUT_RADIO_PATH_SEP "\\"
#elif defined(__APPLE__)
    #include <TargetConditionals.h>
    #include <stdlib.h>
    #define OUTPUT_RADIO_DIRECTORY_HOME getenv("HOME")
    #define OUTPUT_RADIO_PATH_SEP "/"
#elif defined(__linux__)
    #include <stdlib.h>
    #define OUTPUT_RADIO_DIRECTORY_HOME getenv("HOME")
    #define OUTPUT_RADIO_PATH_SEP "/"
#endif

// =====================================================
// Radio Registry
// =====================================================

#define _OUTPUT_RADIO_STATION_REGISTRY_MAX                  2056
#define _OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX             64
#define _OUTPUT_RADIO_STATION_REGISTRY_URL_MAX              512
static char _output_radio_station_registry_names[_OUTPUT_RADIO_STATION_REGISTRY_MAX * _OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX];
static char _output_radio_station_registry_urls[_OUTPUT_RADIO_STATION_REGISTRY_MAX * _OUTPUT_RADIO_STATION_REGISTRY_URL_MAX];
static int _output_radio_station_registry_count = 0;
static char _radio_station_current[_OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX] = "None";

// =====================================================
// Other
// =====================================================

static bool (*_task_output_radio_on_event_bus)(const int type, const void* payload, const int size, const char* source) = NULL;
static mpv_handle* _output_radio_mpv_handle = NULL;

// =====================================================
// Core
// =====================================================

static void _output_radio_station_registry_add(const char* name, const char* url) 
{
    // Guard
    if (_output_radio_station_registry_count >= _OUTPUT_RADIO_STATION_REGISTRY_MAX) 
    {
        // UI (Fix: Heap allocate for router)
        if (_task_output_radio_on_event_bus) 
        {
            char* err_msg = strdup("--ui_notify_error Task Error: Output_Radio -> Radio station max count reached :(");
            _task_output_radio_on_event_bus(VOX_BUS_EVENT_STRING, err_msg, strlen(err_msg) + 1, "radio");
        }
        return;
    }

    // Add
    strncpy(memset(&_output_radio_station_registry_names[_output_radio_station_registry_count * _OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX], 0, _OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX), name, _OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX - 1);
    strncpy(memset(&_output_radio_station_registry_urls[_output_radio_station_registry_count * _OUTPUT_RADIO_STATION_REGISTRY_URL_MAX], 0, _OUTPUT_RADIO_STATION_REGISTRY_URL_MAX), url, _OUTPUT_RADIO_STATION_REGISTRY_URL_MAX - 1);
    _output_radio_station_registry_count++;
}

static void _output_radio_station_registry_add_directory(const char* base_path) 
{
    // Open directory
    DIR* dir = opendir(base_path);
    if (!dir) return;

    // Add
    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL) 
    {
        // Skip hidden
        if (entry->d_name[0] == '.') continue; 
        
        // Match audio extensions
        if (strstr(entry->d_name, ".mp3") || strstr(entry->d_name, ".wav") ||  strstr(entry->d_name, ".flac") || strstr(entry->d_name, ".m4a")) 
        {   
            // Full path
            char full_path[1024];
            snprintf(full_path, sizeof(full_path), "%s" OUTPUT_RADIO_PATH_SEP "%s", base_path, entry->d_name);
            
            // Clean name
            char clean_name[64];
            strncpy(clean_name, entry->d_name, 63);
            char* dot = strrchr(clean_name, '.');
            if (dot) *dot = '\0';
            
            // Add
            _output_radio_station_registry_add(clean_name, full_path);
        }
    }

    // Close directory
    closedir(dir);
}

static void _output_radio_station_registry_add_directories_external() 
{
    // Windows
    #if defined(_WIN32)
    char drives[256];
    if (GetLogicalDriveStringsA(sizeof(drives), drives)) {
        char* drive = drives;
        while (*drive) {
            UINT type = GetDriveTypeA(drive);
            if (type == DRIVE_FIXED || type == DRIVE_REMOVABLE) {
                _output_radio_station_registry_add_directory(drive);
            }
            drive += strlen(drive) + 1;
        }
    }    

    // MacOS
    #elif defined(__APPLE__)
    _output_radio_station_registry_add_directory("/Volumes");
    
    // Linux
    #elif defined(__linux__)
    _output_radio_station_registry_add_directory("/media");
    _output_radio_station_registry_add_directory("/mnt");
    #endif
}

static void _output_radio_station_registry_add_directory_home() 
{
    char music_path[1024];
    const char* home = OUTPUT_RADIO_DIRECTORY_HOME;
    if (home) {
        snprintf(music_path, sizeof(music_path), "%s" OUTPUT_RADIO_PATH_SEP "Music", home);    
        _output_radio_station_registry_add_directory(music_path);
    }
}

// =====================================================
// Task
// =====================================================

static inline void task_output_radio_desktop_boot(VoxEventBusTransmit transmit) 
{
    // Guard
    if (_output_radio_mpv_handle)
        return;

    // Command
    _task_output_radio_on_event_bus = transmit;

    // Mpv
    _output_radio_mpv_handle = mpv_create();
    mpv_set_option_string(_output_radio_mpv_handle, "ytdl", "yes");
    mpv_set_option_string(_output_radio_mpv_handle, "vo", "null");
    mpv_initialize(_output_radio_mpv_handle);

    // Radio stations
    _output_radio_station_registry_add("fallout_radio", "https://www.youtube.com/watch?v=6qQ0TMK7ZuE");
    _output_radio_station_registry_add("fallout_sleep", "https://www.youtube.com/watch?v=0sJcSgs8CIU");
    _output_radio_station_registry_add("persona_rainy", "https://www.youtube.com/watch?v=iCyHMKAVT8E");
    _output_radio_station_registry_add_directory_home();
    _output_radio_station_registry_add_directories_external();
   
    // UI
    char* boot_msg = strdup("--ui_notify_header Task booted: Output_Radio");
    _task_output_radio_on_event_bus(VOX_BUS_EVENT_STRING, boot_msg, strlen(boot_msg) + 1, "radio");
}

static inline void task_output_radio_desktop_run(float delta_time) 
{
}

static inline void task_output_radio_desktop_terminate(void) 
{
    // Guard
    if (!_output_radio_mpv_handle)
        return;

    mpv_terminate_destroy(_output_radio_mpv_handle);
    _output_radio_mpv_handle = NULL;
}

static inline bool task_output_radio_desktop_on_event_bus(const int type, const void* payload, const int size, const char* source) 
{
    // Guard
    if (type != VOX_BUS_EVENT_STRING) return false;

    // Payload : normalized
    char payload_normalized[1024];
    VOX_STRING_COPY(payload, payload_normalized, 1024);
    VOX_STRING_LOWER_UNTIL_ANY(payload_normalized, 1024, " ");

    if (strncmp(payload_normalized, "--radio_play ", 13) == 0)
    {
        for (int i = 0; i < _output_radio_station_registry_count; i++) 
            if (strcmp(&_output_radio_station_registry_names[i * _OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX], payload_normalized + 13) == 0)
            {
                mpv_command(_output_radio_mpv_handle, (const char*[]){"loadfile", &_output_radio_station_registry_urls[i * _OUTPUT_RADIO_STATION_REGISTRY_URL_MAX], NULL});
                strncpy(_radio_station_current, &_output_radio_station_registry_names[i * _OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX], _OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX - 1);
                return true;
            }
    }
    else if (strcmp(payload_normalized, "--radio_stop") == 0) 
    {
        mpv_command(_output_radio_mpv_handle, (const char*[]){"stop", NULL});
        strncpy(_radio_station_current, "None", _OUTPUT_RADIO_STATION_REGISTRY_NAME_MAX - 1);
        return true;
    }
    else if (strncmp(payload_normalized, "--radio_volume ", 15) == 0) 
    {
        mpv_set_property_string(_output_radio_mpv_handle, "volume", payload_normalized + 15);
        return true;
    }

    return false;
}