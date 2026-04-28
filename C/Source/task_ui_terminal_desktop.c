#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include <termios.h>

// =====================================================
// PALETTE REGISTRY
// =====================================================

typedef struct 
{
    const char* name;
    const char* hex[8];
} UI_Theme;

static const UI_Theme UI_REGISTRY[] = 
{
    // --- Iconic Tech & IDE Themes ---
    {"dracula",       {"af87ff", "ff87d7", "5fff87", "ffff87", "ff5f5f", "ffffff", "8787af", "af87ff"}},
    {"gruvbox",       {"ffaf00", "ff8700", "afaf00", "d78700", "afaf00", "ffd7af", "767676", "ffaf00"}},
    {"nord",          {"87afd7", "5f87af", "afd787", "d7af87", "d75f5f", "87afff", "767676", "87afd7"}},
    {"monokai",       {"ff005f", "afd700", "5fd7ff", "ff8700", "d7005f", "ffffff", "6c6c6c", "ff005f"}},
    {"oceanic",       {"00afd7", "0087d7", "5fd7af", "ffd75f", "ff5f5f", "afd7d7", "5f8787", "00afd7"}},
    {"solar",         {"0087ff", "00afaf", "5f8700", "af8700", "d70000", "8a8a8a", "8a8a8a", "0087ff"}},

    // --- Retro Hardware & Gaming ---
    {"pipboy_green",  {"00ff5f", "008700", "00ff00", "5fff00", "ff0000", "87ffaf", "005f00", "00ff5f"}},
    {"pipboy_amber",  {"ff8700", "af5f00", "ffaf00", "ff5f00", "d75f00", "ffaf5f", "875f00", "ff8700"}},
    {"pipboy_blue",   {"00ffff", "0087af", "00d7ff", "00afff", "005f87", "87ffff", "005f5f", "00ffff"}},
    {"pipboy_white",  {"eeeeee", "808080", "d0d0d0", "bcbcbc", "a8a8a8", "ffffff", "585858", "eeeeee"}},
    {"pipboy_red",    {"ff0000", "870000", "d70000", "af0000", "5f0000", "ff5f5f", "5f0000", "ff0000"}},
    {"pipboy_purple", {"d75fff", "8700ff", "af5fff", "af00ff", "5f00af", "d7afff", "5f0087", "d75fff"}},
    {"pipboy_yellow", {"ffff00", "878700", "ffd700", "d7d700", "af8700", "ffffaf", "5f5f00", "ffff00"}},
    {"pipboy_pink",   {"ff87ff", "d70087", "ff5faf", "ff00d7", "87005f", "ffafff", "5f005f", "ff87ff"}},
    {"amber",         {"ffaf00", "d78700", "ffd700", "ffaf00", "ff0000", "ffaf5f", "af5f00", "ffaf00"}},
    {"phosphor",      {"00ff00", "008700", "87ff87", "00ff00", "af0000", "5fff87", "005f00", "00ff00"}},
    {"c64",           {"5f5fff", "8787ff", "87afff", "ffff5f", "d70000", "afd7ff", "00005f", "5f5fff"}},
    {"gameboy",       {"005f00", "5f8700", "008700", "878700", "5f0000", "87af5f", "5f8700", "005f00"}},
    {"matrix",        {"00ff00", "005f00", "87ff87", "d7ff00", "af0000", "00ff87", "00ff00", "00ff00"}},

    // --- Original & Custom "Vox" Themes ---
    {"dusty",         {"d75f5f", "8787af", "87af87", "d7d787", "af5f5f", "d0d0d0", "8787af", "d75f5f"}},
    {"forest",        {"00af00", "5f875f", "87d75f", "afaf00", "870000", "d7ffd7", "5f875f", "00af00"}},
    {"midnight",      {"ff0087", "00d7ff", "00ff00", "ffaf00", "d70000", "00d7ff", "00d7ff", "ff0087"}},
    {"void",          {"eeeeee", "303030", "a8a8a8", "808080", "af0000", "dadada", "080808", "eeeeee"}},
    {"bone",          {"d0d0d0", "808080", "bcbcbc", "a8a8a8", "444444", "eeeeee", "808080", "d0d0d0"}},

    // --- High-Energy & Aesthetic ---
    {"synth",         {"ff00ff", "af00ff", "00ffff", "ffff00", "ff005f", "00ffff", "5f5faf", "ff00ff"}},
    {"vapor",         {"ff00ff", "d75fff", "00ffff", "ffff00", "ff5f87", "00ffff", "d75fff", "ff00ff"}},
    {"cyber",         {"ffff00", "00ffff", "ff00ff", "00ff00", "ff0000", "00ffff", "00ffff", "ffff00"}},
    {"sakura",        {"ffafaf", "ffd7ff", "ff87af", "ffd75f", "ff0000", "eeeeee", "d0d0d0", "ffafaf"}},

    // --- Earth & Elemental ---
    {"oasis",         {"5faf87", "5f8787", "87d7af", "d7af5f", "af5f5f", "d7ffd7", "005f5f", "5faf87"}},
    {"lava",          {"ff0000", "ff5f00", "ff8700", "ffaf00", "d70000", "ffffd7", "6c6c6c", "ff0000"}},
    {"glacier",       {"87d7ff", "87afff", "afd7ff", "eeeeee", "005f87", "d7ffff", "87afaf", "87d7ff"}},
    {"coffee",        {"875f00", "af875f", "af8787", "d7af87", "5f0000", "ffffd7", "444444", "875f00"}},
    {"crimson",       {"d70000", "870000", "ff0000", "ff5f00", "5f0000", "eeeeee", "870000", "d70000"}},
    {"steel",         {"808080", "585858", "bcbcbc", "a8a8a8", "262626", "eeeeee", "585858", "808080"}},
    {"windblown",     {"87d7ff", "808080", "afff87", "ffd787", "d75f5f", "eeeeee", "585858", "87d7ff"}},

    // --- Gundam ---
    {"gundam_rx78",     {"FFFFFF", "19428F", "C70039", "FFC300", "FF69B4", "D1D1D1", "19428F", "FFFFFF"}},
    {"gundam_red_comet", {"E32227", "4A4A4A", "FFD700", "E32227", "FFCC00", "BCBCBC", "4A4A4A", "E32227"}}
};

static const int _UI_PALETTE_COUNT = sizeof(UI_REGISTRY) / sizeof(UI_Theme);

// =====================================================
// INTERNAL STATE & STACK
// =====================================================

// Console commands
#define _UI_CONSOLE_COMMAND_ANSI_RESET_ALL                      "\033[0m"
#define _UI_CONSOLE_COMMAND_CURSOR_COLOR                        "\033]12;#%s\007"
#define _UI_CONSOLE_COMMAND_CLEAR                               "\033[2J\033[3J\033[H"
#define _UI_CONSOLE_COMMAND_CLEAR_LINE                          "\033[F\033[2K\r"
#define _UI_CONSOLE_COMMAND_CURSOR_STYLE_BLINK_BLOCK            "\033[1 q"
#define _UI_CONSOLE_COMMAND_CURSOR_STYLE_STEADY_BLOCK           "\033[2 q"
#define _UI_CONSOLE_COMMAND_CURSOR_STYLE_BLINK_UNDER            "\033[3 q"
#define _UI_CONSOLE_COMMAND_CURSOR_STYLE_STEADY_UNDER           "\033[4 q"
#define _UI_CONSOLE_COMMAND_CURSOR_STYLE_BLINK_BAR              "\033[5 q"
#define _UI_CONSOLE_COMMAND_CURSOR_STYLE_STEADY_BAR             "\033[6 q"

// Title
static bool ui_title_enabled = true;

// Pallet
static char _ui_palette_current[8][32]; 

// Stack
#define _UI_STACK_ELEMENT_BUFFER_SIZE                           1024
#define _UI_STACK_SIZE                                          32
static char ui_stack_header[_UI_STACK_ELEMENT_BUFFER_SIZE * _UI_STACK_SIZE];
static int  ui_stack_colors[_UI_STACK_SIZE];
static int  ui_stack_lengths[_UI_STACK_SIZE];
static int  ui_stack_active_count = 0;

// Typewriter
#define _UI_TYPEWRITER_DELAY_US                                 5000
#define _UI_TYPEWRITER_DELAY_TITLE                              1000
#define _UI_TYPEWRITER_DELAY_NOTIFY                             3000
#define _UI_TYPEWRITER_DELAY_ERROR                              2000
#define _UI_TYPEWRITER_DELAY_ATTENTION                          3000
static bool ui_typewriter_enabled = true;
static volatile bool ui_typewriter_typing = false;

// Command
static bool (*_task_ui_terminal_on_event_bus)(const int type, const void* payload, const int size, const char* source) = NULL;
static pthread_t  task_ui_terminal_desktop_listener_thread;

// =====================================================
// Core
// =====================================================

static void task_ui_terminal_desktop_set_echo(bool enable) 
{
    struct termios t;
    tcgetattr(STDIN_FILENO, &t);
    enable ? (t.c_lflag |= ECHO) : (t.c_lflag &= ~ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &t);
}

static void task_ui_terminal_desktop_print(int color_index, const char* text, int delay, const bool b_wipe_line)
{
    // 1. Wipe the current line (removes the "> " prompt)
    // \r = start of line, \033[K = clear to end of line
    if (b_wipe_line)
        printf("\r\033[K"); 
        
    
    // Lock terminal input
    ui_typewriter_typing = true;
    task_ui_terminal_desktop_set_echo(false);

    // Color
    printf("%s", _ui_palette_current[color_index]);
    fflush(stdout);

    // Print
    if (!ui_typewriter_enabled)
    {
        printf("%s", text);
    }
    for (int i = 0; text[i] != '\0'; i++)
    {
        putchar(text[i]);
        fflush(stdout);
        usleep(delay);
    }
        
    // Delete any keys the user typed while the typewriter was running
    tcflush(STDIN_FILENO, TCIFLUSH); 
    
    // Rename terminal inpiut
    task_ui_terminal_desktop_set_echo(true);
    ui_typewriter_typing = false;
    fflush(stdout);

    // Forced Newline (fixes the 'clumping' issue)
    //  Redraw the prompt at the new bottom position
    if (b_wipe_line)
    {
        printf("\n");    
        printf("%s> %s", _ui_palette_current[0], _ui_palette_current[5]);
        fflush(stdout);
    }
}

static void task_ui_terminal_desktop_title()
{
    task_ui_terminal_desktop_print(0, "██╗   ██╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗ ██████╗ ███████╗\n", _UI_TYPEWRITER_DELAY_TITLE, false);
    task_ui_terminal_desktop_print(0, "██║   ██║██╔═══██╗╚██╗██╔╝    ██╔════╝ ██╔═══██╗██╔══██╗██╔════╝\n", _UI_TYPEWRITER_DELAY_TITLE, false);
    task_ui_terminal_desktop_print(0, "██║   ██║██║   ██║ ╚███╔╝     ██║      ██║   ██║██████╔╝█████╗\n", _UI_TYPEWRITER_DELAY_TITLE, false);
    task_ui_terminal_desktop_print(0, "██║   ██║██║   ██║ ╚███╔╝     ██║      ██║   ██║██████╔╝█████╗\n", _UI_TYPEWRITER_DELAY_TITLE, false);
    task_ui_terminal_desktop_print(0, "╚██╗ ██╔╝██║   ██║ ██╔██╗     ██║      ██║   ██║██╔══██╗██╔══╝\n", _UI_TYPEWRITER_DELAY_TITLE, false);
    task_ui_terminal_desktop_print(0, "╚████╔╝ ╚██████╔╝██╔╝ ██╗    ╚██████╗ ╚██████╔╝██║  ██║███████╗\n", _UI_TYPEWRITER_DELAY_TITLE, false);
    task_ui_terminal_desktop_print(0, "╚═══╝   ╚═════╝ ╚═╝  ╚═╝     ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝\n", _UI_TYPEWRITER_DELAY_TITLE, false);
    task_ui_terminal_desktop_print(1, "M i c r o k e r n e l   ", _UI_TYPEWRITER_DELAY_US, false);
    task_ui_terminal_desktop_print(2, "c _ e d i t i o n\n\n", _UI_TYPEWRITER_DELAY_US, false);
}

static void task_ui_terminal_desktop_clear() 
{
    //
    printf(_UI_CONSOLE_COMMAND_CLEAR);
    fflush(stdout);
    
    // Guard
    if (!ui_title_enabled)
        return;
}

static void task_ui_terminal_desktop_stack_clear() 
{
    ui_stack_active_count = 0;
}

static void task_ui_terminal_desktop_stack_push(int color_index, const char* text) 
{
    // Guard
    if (ui_stack_active_count >= _UI_STACK_SIZE) return;

    // Create
    int i = ui_stack_active_count;
    ui_stack_colors[i] = color_index;
    ui_stack_lengths[i] = (int)strlen(text);
    if (ui_stack_lengths[i] > _UI_STACK_ELEMENT_BUFFER_SIZE - 1)
        ui_stack_lengths[i] = _UI_STACK_ELEMENT_BUFFER_SIZE - 1;
    ui_stack_active_count++;
    
    // Write
    strncpy(&ui_stack_header[i * _UI_STACK_ELEMENT_BUFFER_SIZE], text, ui_stack_lengths[i]);
}

static void task_ui_terminal_refresh() 
{   
    // Cache typewriter enabled
    bool ui_typewriter_enabled_previous = ui_typewriter_enabled;
    ui_typewriter_enabled = false;

    // Clear
    task_ui_terminal_desktop_clear();
    task_ui_terminal_desktop_title();

    // print stack
    for (int i = 0; i < ui_stack_active_count; i++) 
    {
        const char* color_code = _ui_palette_current[ui_stack_colors[i]];
        const char* text_ptr = &ui_stack_header[i * _UI_STACK_ELEMENT_BUFFER_SIZE];
        printf("%s%.*s\n", color_code, ui_stack_lengths[i], text_ptr);
    }

    // Reset typewriter enabled
    ui_typewriter_enabled = ui_typewriter_enabled_previous;
}

static void task_ui_terminal_desktop_console_command(const char* ansi_code) 
{
    printf("%s", ansi_code);
    fflush(stdout);
}

static bool task_ui_terminal_desktop_set_palette(const char* name) 
{
    for (int i = 0; i < _UI_PALETTE_COUNT; i++) 
    {
        // Find the match in the registry
        if (strcmp(UI_REGISTRY[i].name, name) == 0) 
        {
            // Bake Hex -> ANSI (Per color)
            for (int j = 0; j < 8; j++) 
            {
                unsigned int r, g, b;
                sscanf(UI_REGISTRY[i].hex[j], "%02x%02x%02x", &r, &g, &b);
                sprintf(_ui_palette_current[j], "\033[38;2;%u;%u;%um", r, g, b);
            }

            // Set cursor color
            printf(_UI_CONSOLE_COMMAND_CURSOR_COLOR, UI_REGISTRY[i].hex[5]);
            fflush(stdout);
            return true;
        }
    }
    
    // No theme found
    return false;
}

static void* task_ui_terminal_desktop_input_listener(void* arg) 
{
    char input_buffer[_UI_STACK_ELEMENT_BUFFER_SIZE];
    while (true) 
    {
        // Command Indicator
        printf("%s> %s", _ui_palette_current[0], _ui_palette_current[5]);
        fflush(stdout);

        if (fgets(input_buffer, sizeof(input_buffer), stdin) != NULL) 
        {
            // GUARD: If the typewriter is currently running, ignore this input completely!
            if (ui_typewriter_typing) continue;
            

            // Clear line
            input_buffer[strcspn(input_buffer, "\n")] = 0;
            task_ui_terminal_desktop_console_command(_UI_CONSOLE_COMMAND_CLEAR_LINE);

            // Input
            if (strlen(input_buffer) > 0) 
            {
                int size = strlen(input_buffer) + 1;
                char* cmd = (char*)VOX_MALLOC(size);
                strncpy(cmd, input_buffer, size);
                _task_ui_terminal_on_event_bus(VOX_BUS_EVENT_STRING, cmd, size, "Keyboard");
            }
        }
    }
    return NULL;
}

// =====================================================
// Task
// =====================================================

static inline void task_ui_terminal_desktop_boot(VoxEventBusTransmit transmit) 
{
    _task_ui_terminal_on_event_bus = transmit;
    task_ui_terminal_desktop_console_command(_UI_CONSOLE_COMMAND_CURSOR_STYLE_BLINK_BLOCK);
    task_ui_terminal_desktop_set_palette("pipboy_green");
    task_ui_terminal_desktop_clear();
    task_ui_terminal_desktop_title();
    pthread_create(&task_ui_terminal_desktop_listener_thread, NULL, task_ui_terminal_desktop_input_listener, NULL);
}

static inline void task_ui_terminal_desktop_terminate(void) 
{
    pthread_cancel(task_ui_terminal_desktop_listener_thread);
    task_ui_terminal_desktop_clear();
    printf("%s", _UI_CONSOLE_COMMAND_ANSI_RESET_ALL);
}

static inline void task_ui_terminal_desktop_run(float delta_time) 
{
}

static inline bool task_ui_terminal_desktop_on_event_bus(const int type, const void* payload, const int size, const char* source) 
{    
    if (type != VOX_BUS_EVENT_STRING) return false;
    const char* command = (const char*)payload;

    // Parse command
    char command_action[32] = {0};
    const char* command_args = "";
    const char* split_pos = strchr(command, ' ');
    
    if (split_pos != NULL) 
    {
        int len = split_pos - command;
        if (len >= sizeof(command_action)) len = sizeof(command_action) - 1;
        strncpy(command_action, command, len);
        command_args = split_pos + 1;
    } 
    else strncpy(command_action, command, sizeof(command_action) - 1);

    if (strcmp(command_action, "--ui_clear") == 0) 
    {
        task_ui_terminal_desktop_stack_clear();
        task_ui_terminal_refresh();
        return true;
    }

    if (strcmp(command_action, "--ui_notify") == 0 && strlen(command_args) > 0) 
    {
        task_ui_terminal_desktop_stack_push(2, command_args);
        task_ui_terminal_desktop_print(6, command_args, _UI_TYPEWRITER_DELAY_US, true);
        return true;
    }

    if (strcmp(command_action, "--ui_notify_header") == 0 && strlen(command_args) > 0) 
    {
        task_ui_terminal_desktop_stack_push(2, command_args);
        task_ui_terminal_desktop_print(2, command_args, _UI_TYPEWRITER_DELAY_US, true);
        return true;
    }

    if (strcmp(command_action, "--ui_notify_attention") == 0 && strlen(command_args) > 0) 
    {
        char formatted_msg[1024]; 
        snprintf(formatted_msg, sizeof(formatted_msg), "[!] %s", command_args);
        task_ui_terminal_desktop_stack_push(2, formatted_msg);
        task_ui_terminal_desktop_print(6, formatted_msg, _UI_TYPEWRITER_DELAY_US, true);    
        return true;
    }

    if (strcmp(command_action, "--ui_notify_error") == 0 && strlen(command_args) > 0) 
    {
        task_ui_terminal_desktop_stack_push(2, command_args);
        task_ui_terminal_desktop_print(4, command_args, _UI_TYPEWRITER_DELAY_US, true);
        return true;
    }

    if (strcmp(command_action, "--ui_palette") == 0 && strlen(command_args) > 0) 
    {
        task_ui_terminal_desktop_set_palette(command_args);
        task_ui_terminal_refresh();
        return true;
    }

    return false;
}