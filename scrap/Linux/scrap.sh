#!/bin/bash

# Useful variables
battery_file="/sys/class/power_supply/BAT0/uevent"
therm_file="/sys/class/thermal/thermal_zone*/temp"

# Epoch
echo epoch,$(date +"%s")

# Voltage min design (mV)
voltage_min_design=$(grep -w "POWER_SUPPLY_VOLTAGE_MIN_DESIGN" $battery_file | cut -f2 -d=)
echo voltage_min_design,$(( $voltage_min_design / 1000 ))

# Voltage now (mV)
voltage_now=$(grep -w "POWER_SUPPLY_VOLTAGE_NOW" $battery_file | cut -f2 -d=)
echo voltage_now,$(( $voltage_now / 1000 ))

# Current now (mA)
current_now=$(grep -w "POWER_SUPPLY_CURRENT_NOW" $battery_file | cut -f2 -d=)
echo current_now,$(( $current_now / 1000 ))

# Charge full design (mAh)
charge_full_design=$(grep -w "POWER_SUPPLY_CHARGE_FULL_DESIGN" $battery_file | cut -f2 -d=)
echo charge_full_design,$(( $charge_full_design / 1000 ))

# Charge full (mAh)
charge_full=$(grep -w "POWER_SUPPLY_CHARGE_FULL" $battery_file | cut -f2 -d=)
echo charge_full,$(( $charge_full / 1000 ))

# Charge now (mAh)
charge_now=$(grep -w "POWER_SUPPLY_CHARGE_NOW" $battery_file | cut -f2 -d=)
echo charge_now,$(( $charge_now / 1000 ))

# Capacity
echo capacity,$(grep -w "POWER_SUPPLY_CAPACITY" $battery_file | cut -f2 -d=)

# Manufacturer
echo \@manufacturer,$(grep -w "POWER_SUPPLY_MANUFACTURER" $battery_file | cut -f2 -d=)

# CPU temperature (°C) 
echo cpu_temp,$(sensors | grep "Core 0:" | grep "\+[0-9][0-9]*\.[0-9]" -o | head -n 1 | cut -c 2-)

# Number of running threads
echo n_running_threads,$(( `ps axms | wc -l` - 1 ))

# Load average (m-1, m-5, m-15)
echo load_average_1,$(uptime | grep -E "[0-9],[0-9]{2}" -o | sed '1q;d' | sed 's/,/\./' )
echo load_average_5,$(uptime | grep -E "[0-9],[0-9]{2}" -o | sed '2q;d' | sed 's/,/\./' )
echo load_average_15,$(uptime | grep -E "[0-9],[0-9]{2}" -o | sed '3q;d' | sed 's/,/\./' )

#- Fan speeds (rotation per minute)
echo fans_rpm,$(sensors | grep "RPM" | head -n 1 | awk '{$1=$1};1' | cut -d" " -f2)

# CPU speed
echo cpu_speed,$(lscpu | grep "MHz" | head -n 1 | cut -f2 -d: | awk '{$1=$1};1')

# RAM load (kB)
echo ram_load,$(grep -w "Active:" /proc/meminfo | tr -s ' ' | cut -f2 -d" ")

# Swap load (kB)
_swap_total=$(grep -w "SwapTotal:" /proc/meminfo | tr -s ' ' | cut -f2 -d" ")
_swap_free=$(grep -w "SwapFree:" /proc/meminfo | tr -s ' ' | cut -f2 -d" ")
echo swap_load,$(( $_swap_total - $_swap_free ))

# Battery status
echo \@battery_status,$(grep "POWER_SUPPLY_STATUS" $battery_file | cut -f2 -d=)
