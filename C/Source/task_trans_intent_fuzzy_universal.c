// VOX_PKG:
// VOX_DEP:

#define  _OUTPUT_PIVOTS\
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

#define _TRIGGER_PIVOTS \
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

#define _TRIGGER_MAX_PER_INTENT 10

#define _MODE_ADD       0
#define _MODE_REMOVE    1

// =====================================================
// Core
// =====================================================

static void task_trans_intent_fuzzy_universal_intent_compile(char* payload, int payload_length, int Mode)
{
    // Normalize: lower
    VOX_STRING_LOWER(payload, payload_length);

    // Output
    /* 
     * REVERSE WINDOW SEARCH: 
     * Identifies the final output segment by sliding a search window from the 
     * right (end) of the payload toward the left. This allows the logic to 
     * isolate only the most recent pivot and its subsequent command data.
     */
    char* output_start = NULL;
    char* output_commad = NULL;
    int output_command_length = 0;
    {
        // Current pivot
        const char* output_pivots[] = { _OUTPUT_PIVOTS };
        for(int i = 0; output_pivots[i] != NULL; i++)
        {
            // Window properties
            int window_length = 0;
            VOX_STRING_LENGTH(output_pivots[i],window_length);
            int window_step_count = payload_length - window_length;
            // if (window_step_count < 0) continue;
            char* window_tail = payload + window_step_count;

            // Slide window (find match)
            while(window_step_count >= 0)
            {
                // Mismatched
                int is_match = 1; 
                for (int j = 0; j < window_length; j++) 
                    if (window_tail[j] != output_pivots[i][j]) 
                    {
                        is_match = 0;
                        break;
                    }

                // Matched
                if (is_match) 
                {
                    if (output_commad == NULL || window_tail > output_start)
                    {
                        output_start = window_tail;
                        output_commad = window_tail + window_length;
                        output_command_length = payload_length - (window_step_count + window_length) - 1;
                    }
                    break; 
                }

                // Slide window
                window_tail--;
                window_step_count--;
            }
        }

        // Cut off output | Abort if we have no input
        if (output_start != NULL)
        {
            *output_start = '\0';
            payload_length = (int)(output_start - payload);
        }
        else return;

        // Trim output
        VOX_STRING_TRIM(output_commad, output_command_length);
            
        // Debug
        #if VOX_DEBUG
        if (output_commad != NULL) 
        {
            printf("\n[DEBUG] Itent_Compile (Fuzzy)\n");
            printf("PAYLOAD: \"%s\"\n", payload);
            printf("PAYLOAD LENGTH: %d\n", payload_length);
            printf("COMMAND: \"%s\"\n", output_commad);
            printf("COMMAND LENGTH: %d \n", output_command_length);
        } 
        #endif
    }

    // Triggers
    char* trigger_ptrs[_TRIGGER_MAX_PER_INTENT];
    int trigger_lens[_TRIGGER_MAX_PER_INTENT];
    int trigger_count = 0;
    {
        const char* trigger_pivots[] = { _TRIGGER_PIVOTS};
    }
}

// =====================================================
// Task
// =====================================================

static bool (*_task_trans_intent_fuzzy_universal_on_event_bus)(int type, void* payload, int size, char* source) = NULL;

static inline void task_trans_intent_fuzzy_universal_boot(VoxEventBusTransmit transmit) 
{
    _task_trans_intent_fuzzy_universal_on_event_bus = transmit;
    char* boot_msg = "--ui_notify_header Task booted: Trans_Intent";
    _task_trans_intent_fuzzy_universal_on_event_bus(VOX_BUS_EVENT_STRING, boot_msg, strlen(boot_msg) + 1, NULL);

    char* msg ="--intent_add If I say fly or land, output --key control command q";
    _task_trans_intent_fuzzy_universal_on_event_bus(VOX_BUS_EVENT_STRING, msg, strlen(msg) + 1, NULL);
}

static inline void task_trans_intent_fuzzy_universal_terminate(void)
{
}

static inline void task_trans_intent_fuzzy_universal_run(float delta_time) 
{
}

static inline bool task_trans_intent_fuzzy_universal_on_event_bus(int type, void* payload, int size, char* source) 
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
         task_trans_intent_fuzzy_universal_intent_compile(payload_normalized, size - 13, _MODE_ADD);
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