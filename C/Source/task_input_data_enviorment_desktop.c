// VOX_PKG: curl cjson
// VOX_DEP: -lcurl -lcjson


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <curl/curl.h>
#include <cjson/cJSON.h>

// =====================================================
// Data Registry
// =====================================================

#define _TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_LOCATION                                                         0
#define _TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_WEATHER                                                          1
#define _TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_SPACE_WEATHER                                                    2
#define _TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_SPACE_CELESTIALS                                                 3
#define _TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_SPACE_PERSONNEL                                                  4
#define _TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_SPACE_ASTEROIDS                                                  5
#define _TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_SPACE_EQUIPMENT                                                  6
#define _TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_MAX                                                              7

#define _TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE                                                            256
#define _TASK_INPUT_DATA_ENVIORMENT_BUCKET_BIG_SIZE                                                              2048
#define _TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZEOF                                                          _TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE
#define _TASK_INPUT_DATA_ENVIORMENT_BUCKET_BIG_SIZEOF                                                            _TASK_INPUT_DATA_ENVIORMENT_BUCKET_BIG_SIZE

// Location
static char _task_input_enviorment_desktop_region[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                 = {0};
static char _task_input_enviorment_desktop_city[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                   = {0};
static char _task_input_enviorment_desktop_lon[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                    = {0};
static char _task_input_enviorment_desktop_lat[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                    = {0};
static char _task_input_enviorment_desktop_elevation[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]              = {0};

// Weather
static char _task_input_enviorment_desktop_temp[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                   = {0};
static char _task_input_enviorment_desktop_windspeed[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]              = {0};
static char _task_input_enviorment_desktop_winddir[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                = {0};
static char _task_input_enviorment_desktop_weathercode[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]            = {0};
static char _task_input_enviorment_desktop_aqi[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                    = {0};
static char _task_input_enviorment_desktop_aqi_status[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]             = {0};
static char _task_input_enviorment_desktop_uv_index[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]               = {0};
static char _task_input_enviorment_desktop_uv_status[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]              = {0};

// Space
static char _task_input_enviorment_desktop_sunrise[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                = {0};
static char _task_input_enviorment_desktop_sunset[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                 = {0};
static char _task_input_enviorment_desktop_moonrise[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]               = {0};
static char _task_input_enviorment_desktop_moonset[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                = {0};
static char _task_input_enviorment_desktop_moonphase[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]              = {0};
static char _task_input_enviorment_desktop_daylight[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]               = {0};
static char _task_input_enviorment_desktop_is_day[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]                 = {0};
static char _task_input_enviorment_desktop_kp_index[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]               = {0};
static char _task_input_enviorment_desktop_space_alert[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]            = {0};
static char _task_input_enviorment_desktop_solar_flare[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]            = {0};
static char _task_input_enviorment_desktop_iss_country[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_SMALL_SIZE]            = {0};

// Details
static char _task_input_enviorment_desktop_personnel[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_BIG_SIZE]                = {0};
static char _task_input_enviorment_desktop_asteroids[_TASK_INPUT_DATA_ENVIORMENT_BUCKET_BIG_SIZE ]               = {0};

// Flags
static bool _task_input_enviorment_desktop_imperial                                                              = false;
static bool _task_input_enviorment_desktop_location_valid                                                        = false;

// =====================================================
// Other
// =====================================================

static bool (*_task_input_data_enviorment_on_event_bus)(const int type, const void* payload, const int size, const char* source) = NULL;

// =====================================================
// Helpers
// ATTENTION: Generated by Gemini 3
// =====================================================

struct _CurlBuf { char* data; size_t size; };

static size_t _curl_write_cb(void* ptr, size_t size, size_t nmemb, void* up) 
{
    // Calculate size of new chunk
    // Access our persistent buffer
    size_t res = size * nmemb;
    struct _CurlBuf* mem = (struct _CurlBuf*)up;
    
    //  Grow our buffer to fit the new data + 1 for the null terminator
    char* tmp = realloc(mem->data, mem->size + res + 1); 
    if (!tmp) return 0; // Out of memory!
    
    // Copy data into our buffer
    // Null terminate
    mem->data = tmp;
    memcpy(&(mem->data[mem->size]), ptr, res);
    mem->size += res;
    mem->data[mem->size] = 0;
    
    return res;
}

static char* _http_get(const char* url) 
{
    CURL* curl = curl_easy_init();
    if (!curl) return NULL;
    struct _CurlBuf chunk = { malloc(1), 0 };
    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "User-Agent: VoxUniversal/1.0");

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, _curl_write_cb);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&chunk);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 15L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

    if (curl_easy_perform(curl) != CURLE_OK) { free(chunk.data); chunk.data = NULL; }
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    return chunk.data;
}

// =====================================================
// Time
// ATTENTION: Generated by Gemini 3
// =====================================================

static void _to_12h(char* out, const char* iso_time) 
{
    if (!iso_time || strlen(iso_time) < 5) { strcpy(out, "N/A"); return; }
    int h, m;
    const char* t_part = strchr(iso_time, 'T');
    if (sscanf(t_part ? t_part + 1 : iso_time, "%d:%d", &h, &m) >= 2)
        snprintf(out, 31, "%d:%02d %s", (h % 12 == 0) ? 12 : h % 12, m, (h >= 12) ? "PM" : "AM");
    else strcpy(out, "N/A");
}

// =====================================================
// Core Update Logic
// =====================================================

static void _env_update(int cat) 
{
    char url[1024];
    char* res = NULL;
    cJSON* json = NULL;
    time_t now = time(NULL);
    struct tm* t_now = localtime(&now);

    switch(cat) 
    {
        case _TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_LOCATION:
            if ((res = _http_get("http://ip-api.com/json/"))) 
            {
                if ((json = cJSON_Parse(res))) 
                {
                    strncpy(_task_input_enviorment_desktop_region, cJSON_GetObjectItem(json, "region") ? cJSON_GetObjectItem(json, "region")->valuestring : "N/A", 63);
                    strncpy(_task_input_enviorment_desktop_city, cJSON_GetObjectItem(json, "city") ? cJSON_GetObjectItem(json, "city")->valuestring : "N/A", 63);
                    snprintf(_task_input_enviorment_desktop_lat, 31, "%.4f", cJSON_GetObjectItem(json, "lat")->valuedouble);
                    snprintf(_task_input_enviorment_desktop_lon, 31, "%.4f", cJSON_GetObjectItem(json, "lon")->valuedouble);
                    cJSON_Delete(json);
                }
                free(res);
            }
            break;
    }
}

// =====================================================
// Task Interface
// =====================================================

static inline void task_input_data_enviorment_desktop_boot(VoxEventBusTransmit transmit) 
{
    _task_input_data_enviorment_on_event_bus = transmit;
    char* boot_msg = strdup("--ui_notify_header Task booted: Input_Data_Enviorment");
    _task_input_data_enviorment_on_event_bus(VOX_BUS_EVENT_STRING, boot_msg, strlen(boot_msg) + 1, "input_data_enviorment");
    curl_global_init(CURL_GLOBAL_ALL);
}

static inline void task_input_data_enviorment_desktop_terminate(void)
{
}

static inline void task_input_data_enviorment_desktop_run(float delta_time) 
{
}

static inline bool task_input_data_enviorment_desktop_on_event_bus(const int type, const void* payload, const int size, const char* source) 
{
    // Guard
    if (type != VOX_BUS_EVENT_STRING) return false;

    // Payload : normalized
    char payload_normalized[1024];
    VOX_STRING_COPY(payload, payload_normalized, 1024);
    VOX_STRING_LOWER_UNTIL_ANY(payload_normalized, 1024, " ");

    // Location
    if (strcmp(payload_normalized, "--data_enviorment_location") == 0) 
    {
        if (_task_input_enviorment_desktop_location_valid == 0) _env_update(_TASK_INPUT_DATA_ENVIORMENT_DESKTOP_CAT_LOCATION);
        char b[512]; snprintf(b, 511, "--ui_notify Data Enviorment Location -> City: %s | Lat: %s | Lon: %s", _task_input_enviorment_desktop_city, _task_input_enviorment_desktop_lat, _task_input_enviorment_desktop_lon);
        _task_input_data_enviorment_on_event_bus(VOX_BUS_EVENT_STRING, b, strlen(b) + 1, "input_data_enviorment");
        return true;
    }

    return false;
}