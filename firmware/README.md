# Calendar demonstration

Target: Seeed XIAO ESP32C6, GDEY075T7 only. USB supplies the module and carrier.

`EPDCalendar/config.h` defaults to a clearly marked fixed-date offline calendar. Enter Wi-Fi credentials and a POSIX timezone rule locally for NTP. Wi-Fi is disabled before refreshing. Credentials are not logged. The panel uses a full update once per boot and then on a date change; no account/cloud calendar service is involved.

For first bench use, set `RUN_PANEL_TESTS=true` to see black, white and checkerboard frames before the calendar. Return it to false afterwards. SPI starts at 1MHz; the buffer is 8000 bytes. The exact GxEPD2 panel driver is selected, not a generic 7.5-inch driver.

BUSY is low-active. An 8-second busy watchdog holds reset low and permits one reboot retry. A second failure latches the board in reset across reboot using NVS. After correcting the hardware issue, clear flash/NVS with the programming tool, or temporarily erase the `epd-c6` Preferences namespace. Do not simply defeat the timeout. Startup, brownout, rail stress and fault behavior still need physical testing.

## Reproduce the firmware build

Install Arduino CLI and use a recent supported operating system/toolchain. Install these pinned dependencies:

```sh
arduino-cli config init
arduino-cli config add board_manager.additional_urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli core update-index
arduino-cli core install esp32:esp32@3.3.12
arduino-cli lib install "GxEPD2@1.6.9" "Adafruit GFX Library@1.12.6" "Adafruit BusIO@1.17.4"
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32C6 firmware/EPDCalendar --output-dir firmware/build
```

Run from the repository root. If CLI configuration already exists, retain it and add the Espressif URL only if absent. Arduino IDE users can install the same versions through Boards/Library Manager. Keep Wi-Fi credentials local and remove them before committing `config.h`.

See `analysis/firmware-build.log` and `firmware/versions.txt` for the recorded compile and pinned versions. The original Apple Silicon build required a project-local rebuilt Arduino ctags host tool; see `docs/ATTRIBUTION.md`. Tool binaries, board packages and libraries are not vendored. No hardware upload has been performed.
