// VOX_PKG:
// VOX_DEP:

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define _TASK_TRANS_INTENT_FUZZY_UNIVERSAL_OUTPUT_PIVOTS \
    " then output ", " then execute ", " then press ", " then type ", " then run ", " then do ", " then ", \
    " than output ", " than execute ", " than press ", " than dp ", " than do ", " than ", \
    " output command ", " output ", " out ", \
    " execute command ", " execute ", \
    " run command ", " run ", \
    " trigger macro ", " trigger ", \
    " press key ", " press ", \
    " hit key ", " hit ", \
    " tap key ", " tap ", \
    " type out ", " type ", \
    " send command ", " send ", \
    " perform ", " activate ", " initiate ", " invoke ", " fire ", " do ", NULL

#define _TASK_TRANS_INTENT_FUZZY_UNIVERSAL_TRIGGER_PIVOTS \
    "every time i say ", "every time i type ", "every time i enter ", \
    "whenever i say ", "whenever i type ", "whenever i enter ", \
    "as soon as i say ", "as soon as i type ", \
    "when i command ", "when i prompt ", \
    "when i input ", "when i enter ", "when i speak ", "when i write ", \
    "when i type ", "when i say ", \
    "if i command ", "if i prompt ", \
    "if i input ", "if i enter ", "if i speak ", "if i write ", \
    "if i type ", "if i say ", \
    "tell you to ", "ask you for ", "ask for ", \
    "please ", "just ", \
    ", or ", " or ", ",", NULL

// =====================================================
// Core
// =====================================================

static void _split_pivots(char* payload, const char* output_pivots[], char** command_value)
{
}

static void task_trans_intent_fuzzy_universal_intent_add(char* payload, const int payload_size)
{
    // Normalize: lower
    VOX_STRING_LOWER(payload, payload_size);

    // Shatter: Output
    char* output = NULL; 
    const char* output_pivots[] = { _TASK_TRANS_INTENT_FUZZY_UNIVERSAL_OUTPUT_PIVOTS };
    _split_pivots(payload, output_pivots, &output);
    if (output == NULL)
        return;

    // Shater: Triggers
    char* triggers = NULL;
    const char* trigger_pivots[] = { _TASK_TRANS_INTENT_FUZZY_UNIVERSAL_TRIGGER_PIVOTS };
    _split_pivots(payload, trigger_pivots, &triggers);
    if (triggers == NULL)
        return;
}

// =====================================================
// Task
// =====================================================

static bool (*_task_trans_intent_fuzzy_universal_on_event_bus)(const int type, const void* payload, const int size, const char* source) = NULL;

static inline void task_trans_intent_fuzzy_universal_boot(VoxEventBusTransmit transmit) 
{
    _task_trans_intent_fuzzy_universal_on_event_bus = transmit;
    const char* boot_msg = "--ui_notify_header Task booted: Trans_Intent";
    _task_trans_intent_fuzzy_universal_on_event_bus(VOX_BUS_EVENT_STRING, boot_msg, strlen(boot_msg) + 1, NULL);
}

static inline void task_trans_intent_fuzzy_universal_terminate(void)
{
}

static inline void task_trans_intent_fuzzy_universal_run(float delta_time) 
{
}

static inline bool task_trans_intent_fuzzy_universal_on_event_bus(const int type, const void* payload, const int size, const char* source) 
{
    // Guard
    if (type != VOX_BUS_EVENT_STRING) return false;

    // Payload : normalized
    char payload_normalized[1024];
    VOX_STRING_COPY(payload, payload_normalized, 1024);
    VOX_STRING_LOWER_UNTIL_ANY(payload_normalized, 1024, " ");

    // Command: intent add
    if (strncmp(payload_normalized, "--intent_add ", 13) == 0)
    {
         VOX_STRING_CHOP_UNTIL_ANY(payload_normalized, " ");
         task_trans_intent_fuzzy_universal_intent_add(payload_normalized, size - 13);
         return true;
    }
    
    // Command: intent remove
    else if (strncmp(payload_normalized, "--intent_remove ", 14) == 0)
    {
        VOX_STRING_CHOP_UNTIL_ANY(payload_normalized, " ");
        return true;
    }

    // Command : Other
    bool is_command;
    VOX_STRING_STARTS_WITH(payload_normalized, "--", is_command);
    if (is_command)
        return false;

    // Parse intent here

    return false;
}