#!/bin/bash

# Useful variables
battery_file="/sys/class/power_supply/BAT0/uevent"
therm_file="/sys/class/thermal/thermal_zone*/temp"

# Epoch
echo epoch,$(date +"%s")

# Voltage min design
echo voltage_min_design,$(grep -w "POWER_SUPPLY_VOLTAGE_MIN_DESIGN" $battery_file | cut -f2 -d=)

# Voltage now
echo voltage_now,$(grep -w "POWER_SUPPLY_VOLTAGE_NOW" $battery_file | cut -f2 -d=)

# Current now
echo current_now,$(grep -w "POWER_SUPPLY_CURRENT_NOW" $battery_file | cut -f2 -d=)

# Charge full design
echo charge_full_design,$(grep -w "POWER_SUPPLY_CHARGE_FULL_DESIGN" $battery_file | cut -f2 -d=)

# Charge full
echo charge_full,$(grep -w "POWER_SUPPLY_CHARGE_FULL" $battery_file | cut -f2 -d=)

# Charge now
echo charge_now,$(grep -w "POWER_SUPPLY_CHARGE_NOW" $battery_file | cut -f2 -d=)

# Capacity
echo capacity,$(grep -w "POWER_SUPPLY_CAPACITY" $battery_file | cut -f2 -d=)

# Manufacturer
echo manufacturer,$(grep -w "POWER_SUPPLY_MANUFACTURER" $battery_file | cut -f2 -d=)

# CPU temperature (TODO: multiple values)
# echo $(cat $therm_file)

# Number of running threads
echo n_running_threads,$(( `ps axms | wc -l` - 1 ))

# Load average (m-1, m-5, m-15)
echo load_average_1,$(uptime | awk '{$1=$1};1' | cut -f11 -d" " | head -c4)
echo load_average_5,$(uptime | awk '{$1=$1};1' | cut -f12 -d" " | head -c4)
echo load_average_15,$(uptime | awk '{$1=$1};1' | cut -f13 -d" " | head -c4)

#- Fan speeds: istats

#- Battery temp: istats

#- CPU usage

# CPU speed
echo cpu_speed,$(lscpu | grep "MHz" | head -n 1 | cut -f2 -d: | awk '{$1=$1};1')

# RAM load (kB)
echo ram_load,$(grep -w "Active:" /proc/meminfo | tr -s ' ' | cut -f2 -d" ")

# Swap load (kB)
_swap_total=$(grep -w "SwapTotal:" /proc/meminfo | tr -s ' ' | cut -f2 -d" ")
_swap_free=$(grep -w "SwapFree:" /proc/meminfo | tr -s ' ' | cut -f2 -d" ")
echo swap_load,$(( $_swap_total - $_swap_free ))

# Battery status (TODO: str)
echo battery_status,$(grep "POWER_SUPPLY_STATUS" $battery_file | cut -f2 -d=)
