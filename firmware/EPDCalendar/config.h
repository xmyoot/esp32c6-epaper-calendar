#pragma once
// Offline demonstration is the default. Set SSID / password locally for NTP.
constexpr char WIFI_SSID[] = "";
constexpr char WIFI_PASSWORD[] = "";
constexpr char TZ_RULE[] = "PST8PDT,M3.2.0,M11.1.0";
constexpr int DEMO_YEAR = 2026;
constexpr int DEMO_MONTH = 10;
constexpr int DEMO_DAY = 20;
// Opt in for first bring-up only: black, white and checkerboard refreshes.
constexpr bool RUN_PANEL_TESTS = false;
