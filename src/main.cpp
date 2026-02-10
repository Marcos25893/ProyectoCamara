#include <Arduino.h>
#include "WifiAp.h"

const char *WIFI_SSID = "Riego_243";
const char *WIFI_PASSWORD = "primaram100";

static const uint32_t PHOTO_INTERVAL_MS = 60UL * 60UL * 1000UL;

WifiAp wifi(WIFI_SSID, WIFI_PASSWORD);

static uint32_t lastPhotoMs = 0;
static bool photoRequested = false;

void takePhotoAndCollectData()
{
    Serial.println("Taking photo...");
    // esp_camera_fb_get()

    Serial.println("Collecting data...");
    // sensores, estado, etc.

    Serial.println("Photo done");
}

void setup()
{
    Serial.begin(115200);
    delay(1000);
    Serial.println("ESP32 Camera on");

    wifi.connect();

    lastPhotoMs = millis();
}

void loop()
{
    const uint32_t nowMs = millis();

    wifi.loop();

    if (!photoRequested && (nowMs - lastPhotoMs >= PHOTO_INTERVAL_MS))
    {
        Serial.println("Photo interval reached");
        photoRequested = true;

        if (!wifi.isConnected())
        {
            Serial.println("WiFi not connected, retrying...");
            wifi.connect();
        }
    }

    if (photoRequested && wifi.isConnected())
    {
        takePhotoAndCollectData();

        lastPhotoMs = millis();
        photoRequested = false;
    }

    delay(10); // watchdog safe
}
