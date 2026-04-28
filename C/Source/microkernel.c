// ==========================================
// VoxCore : Mac Desktop Unity Build
// ==========================================

#include <stdio.h>
#include <string.h>
#include <sys/time.h>
#include <unistd.h>
#include "vox_autogen.c"

static volatile bool vox_running = true;

// =====================================================
// Event bus
// =====================================================

bool bus_transmit(const int type, const void* payload, const int size, const char* source) 
{
    if (payload == NULL || size <= 0) return false;

    // Handle System-Level Payloads
    {
        const char* text = (const char*)payload;
        if (strcmp(text, "--quit") == 0 || strcmp(text, "--exit") == 0) 
        {
            vox_running = false;
            return true; 
        }
    }

    // Broadcast to Task Stack
    bool handled = false;
    #define VOX_TASK(name, prefix) \
        if (!handled) { \
            handled = prefix##_on_event_bus(type, payload, size, source); \
        }
    VOX_TASK_STACK
    #undef VOX_TASK

    return handled; 
}

// =====================================================
// Main
// =====================================================

int main(int argc, char **argv) 
{
    // Time: boot
    struct timeval time_now, time_last;
    gettimeofday(&time_last, NULL);

    // Tasks: boot
    #define VOX_TASK(name, prefix) prefix##_boot(bus_transmit);
    VOX_TASK_STACK
    #undef VOX_TASK

    // Run
    while (vox_running) 
    {
        // Time: delta time
        gettimeofday(&time_now, NULL);
        float delta_time = (time_now.tv_sec - time_last.tv_sec) + (time_now.tv_usec - time_last.tv_usec) * 1e-6f;
        time_last = time_now;

        // Tasks: run
        #define VOX_TASK(name, prefix) prefix##_run(delta_time);
        VOX_TASK_STACK
        #undef VOX_TASK
        
        // Wait a bit to prevent 100% cpu usuage
        usleep(1000); 
    }

    // Task: terminate
    #define VOX_TASK(name, prefix) prefix##_terminate();
    VOX_TASK_STACK
    #undef VOX_TASK

    return 0;
}