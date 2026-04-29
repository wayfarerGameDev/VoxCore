// VOX_DEP: mac: -framework ApplicationServices
#include <ApplicationServices/ApplicationServices.h>

#include <string.h>
#include <stdlib.h>


// =====================================================
// Key Registry
// =====================================================

typedef struct { const char* name; uint16_t code; } _OutputKeysKeyMap;
static const _OutputKeysKeyMap _output_keys_desktop_registry[] = 
{
    // --- Default Modifiers ---
    {"alt", 58}, {"option", 58}, {"ctrl", 59}, {"control", 59}, {"shift", 56}, {"cmd", 55}, {"command", 55},

    // --- Explicit Left Modifiers ---
    {"left_alt", 58}, {"left_option", 58}, {"left_ctrl", 59}, {"left_control", 59}, {"left_shift", 56}, {"left_cmd", 55}, {"left_command", 55},

    // --- Explicit Right Modifiers ---
    {"right_alt", 61}, {"right_option", 61}, {"right_ctrl", 62}, {"right_control", 62}, {"right_shift", 60}, {"right_cmd", 54}, {"right_command", 54},

    // --- Standard Controls ---
    {"space", 49}, {"enter", 36}, {"return", 36}, {"esc", 53}, {"tab", 48}, {"backspace", 51}, {"delete", 51}, {"caps", 57}, {"capslock", 57},

    // --- Alphabet ---
    {"a", 0},  {"b", 11}, {"c", 8},  {"d", 2},  {"e", 14}, {"f", 3},  {"g", 5},  {"h", 4},
    {"i", 34}, {"j", 38}, {"k", 40}, {"l", 37}, {"m", 46}, {"n", 45}, {"o", 31}, {"p", 35},
    {"q", 12}, {"r", 15}, {"s", 1},  {"t", 17}, {"u", 32}, {"v", 9},  {"w", 13}, {"x", 7},
    {"y", 16}, {"z", 6},

    // --- Numbers ---
    {"1", 18}, {"2", 19}, {"3", 20}, {"4", 21}, {"5", 23}, {"6", 22}, {"7", 26}, {"8", 28}, {"9", 25}, {"0", 29},

    // --- Numpad ---
    {"numpad_0", 82}, {"numpad_1", 83}, {"numpad_2", 84}, {"numpad_3", 85}, {"numpad_4", 86}, {"numpad_5", 87}, {"numpad_6", 88}, {"numpad_7", 89}, {"numpad_8", 91}, {"numpad_9", 92}, 
    {"numpad_decimal", 65}, {"numpad_multiply", 67}, {"numpad_plus", 69}, {"numpad_clear", 71}, {"numpad_divide", 75}, {"numpad_enter", 76}, {"numpad_minus", 78}, {"numpad_equals", 81},

    // --- Punctuation ---
    {"-", 27}, {"minus", 27}, {"dash", 27}, {"=", 24}, {"equals", 24}, {"equal", 24}, {"[", 33}, {"left_bracket", 33}, {"bracket_left", 33},
    {"]", 30}, {"right_bracket", 30}, {"bracket_right", 30}, {"\\", 42}, {"backslash", 42}, {";", 41}, {"semicolon", 41}, {"'", 39}, {"quote", 39}, {"apostrophe", 39},
    {",", 43}, {"comma", 43}, {".", 47}, {"period", 47}, {"dot", 47}, {"/", 44}, {"slash", 44}, {"forward_slash", 44}, {"`", 50}, {"tick", 50}, {"backtick", 50},

    // --- Arrow Keys ---
    {"up", 126}, {"down", 125}, {"left", 123}, {"right", 124},

    // --- F Keys ---
    {"f1", 122}, {"f2", 120}, {"f3", 99},  {"f4", 118}, {"f5", 96},  {"f6", 97},  {"f7", 98},  {"f8", 100}, {"f9", 101}, {"f10", 109}, {"f11", 103}, {"f12", 111},
    {"f13", 105}, {"f14", 107}, {"f15", 113}, {"f16", 106}, {"f17", 64},  {"f18", 79},  {"f19", 80}
};
static const int _output_keys_desktop_registry_count = sizeof(_output_keys_desktop_registry) / sizeof(_OutputKeysKeyMap);

// =====================================================
// Other
// =====================================================

static bool (*_task_output_keys_on_event_bus)(const int type, const void* payload, const int size, const char* source) = NULL;

// =====================================================
// Core
// =====================================================

static uint16_t _output_keys_desktop_get_code(const char* name)
{
    for (int i = 0; i < _output_keys_desktop_registry_count; i++)
        if (strcmp(_output_keys_desktop_registry[i].name, name) == 0) return _output_keys_desktop_registry[i].code;
    return 0xFFFF;
}

static void _output_keys_desktop_post(uint16_t code, bool down, CGEventFlags flags)
{
    CGEventRef ev = CGEventCreateKeyboardEvent(NULL, (CGKeyCode)code, down);
    if (flags) CGEventSetFlags(ev, flags);
    CGEventPost(kCGHIDEventTap, ev);
    CFRelease(ev);
}

static void _output_keys_desktop_press_string(char* key_string)
{
    CGEventFlags flags = 0;
    uint16_t keys[16]; 
    int key_cnt = 0;

    for (char* t = strtok(key_string, " "); t; t = strtok(NULL, " "))
    {
        if (!strcmp(t, "cmd") || !strcmp(t, "command"))    flags |= kCGEventFlagMaskCommand;
        else if (!strcmp(t, "alt") || !strcmp(t, "option"))     flags |= kCGEventFlagMaskAlternate;
        else if (!strcmp(t, "ctrl") || !strcmp(t, "control"))   flags |= kCGEventFlagMaskControl;
        else if (!strcmp(t, "shift"))                           flags |= kCGEventFlagMaskShift;
        else 
        {
             uint16_t c = _output_keys_desktop_get_code(t);
            if (c != 0xFFFF && key_cnt < 16) keys[key_cnt++] = c;
        }
    }

    for (int i = 0; i < key_cnt; i++) _output_keys_desktop_post(keys[i], true, flags);
    for (int i = key_cnt - 1; i >= 0; i--) _output_keys_desktop_post(keys[i], false, flags);

}

// =====================================================
// Task
// =====================================================

static inline void task_output_keys_desktop_boot(VoxEventBusTransmit transmit)
{
    _task_output_keys_on_event_bus = transmit;

    char* m1 = strdup("--ui_notify_header Task booted: Output_Keys");
    char* m2 = strdup("--ui_notify_attention Accessibility Required: Grant permissions in System Settings. If running via Terminal, ensure the Terminal has Accessibility access."); 
    _task_output_keys_on_event_bus(VOX_BUS_EVENT_STRING, m1, strlen(m1) + 1, "keys");
    _task_output_keys_on_event_bus(VOX_BUS_EVENT_STRING, m2, strlen(m2) + 1, "keys");
}

static inline void task_output_keys_desktop_terminate(void)
{
}

static inline void task_output_keys_desktop_run(float delta_time) 
{
}

static inline bool task_output_keys_desktop_on_event_bus(const int type, const void* payload, const int size, const char* source)
{
    // Guard
    if (type != VOX_BUS_EVENT_STRING) return false;

    // Payload : normalized
    char payload_normalized[1024];
    VOX_STRING_COPY(payload, payload_normalized, 1024);
    VOX_STRING_LOWER_UNTIL_ANY(payload_normalized, 1024, " ");

    if (strncmp(payload_normalized, "--key ", 6) == 0)
    {
        char args[256]; strncpy(args, payload_normalized + 6, 255); args[255] = '\0';
        _output_keys_desktop_press_string(args);
        return true;
    }
    if (strncmp(payload_normalized, "--keys ", 7) == 0)
    {
        char args[256]; strncpy(args, payload_normalized + 7, 255); args[255] = '\0';
        _output_keys_desktop_press_string(args);
        return true;
    }

    return false;
}