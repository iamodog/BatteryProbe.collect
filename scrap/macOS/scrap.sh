#!/bin/bash

#Epoch
printf "epoch:"
printf "$(date +%s )"
printf "\n"

#Voltage now, in mV
printf "voltage_now:"
printf "$(system_profiler SPPowerDataType | grep Voltage| cut -f2 -d: | sed 's/ //g')"
printf "\n"

#Current now in mA
printf "current_now:"
echo "$(system_profiler SPPowerDataType | grep Amperage | cut -f2 -d: | sed 's/ //g' | cut -d "-" -f2)"

#Charge full design in mAh
printf "charge_full_design:"
echo $(istats battery capacity --value-only | sed '3q;d')

#Charge full now in mAh
printf "charge_full:"
charge_full=$(system_profiler SPPowerDataType | grep "Full Charge Capacity" | cut -f2 -d: | sed 's/ //g')
echo $charge_full

#Charge now in mAh
printf "charge_now:"
# MAC OS Catalina version
#charge_now=$(system_profiler SPPowerDataType | grep "Charge Remaining" | cut -f2 -d: | sed 's/ //g' )
# MAC OS Big Sur version
charge_now=$(istats battery capacity --value-only | sed '1q;d')
echo $charge_now

#Supply manufacturer
printf "@manufacturer:"
printf "$(system_profiler SPPowerDataType | grep Manufacturer | cut -f2 -d: | sed 's/ //g' | head -n 1)"
printf "\n"

#Nb of running threads
printf "n_running_threads:"
printf "$(top -l 1 -n 0 | grep thread | cut -d "," -f4 | tr -dc '0-9')"
printf "\n"

#CPU temp (°C)
printf "cpu_temp:"
echo $(istats cpu --value-only)

#Load averages
printf "load_average_1:"
printf "$(sysctl -n vm.loadavg | cut -d " " -f2)" 
printf '\n'
printf "load_average_5:"
printf "$(sysctl -n vm.loadavg | cut -d " " -f3)"
printf '\n'
printf "load_average_15:"
printf "$(sysctl -n vm.loadavg | cut -d " " -f4)"
printf '\n'

#Number of fans & rpm
printf "number_of_fans:"
n_fans=`istats fan | cut -d: -f2 | head -n 1 | sed 's/ //g'`
echo "$n_fans"
sum_rpm=0
for i in `seq 1 $n_fans`
do
    rpm=$(istats fan speed | cut -d ":" -f2 | cut -d "R" -f1 | sed "$iq;d")
    sum_rpm=$((sum_rpm+rpm))
done
printf "mean_fans_rpm:"
echo "scale=2; $sum_rpm/$n_fans" | bc 

#Battery temp (°C)
printf "battery_temp:"
echo $(istats battery temp --value-only)

#Cycle count
printf "cycle_count:"
echo $(istats battery cc --value-only | head -n 1)

#Battery status : Charging, Full or Discharging
Fully_charged=`system_profiler SPPowerDataType | grep Fully | cut -d ":" -f2 | sed 's/ //g'`
Charging=`system_profiler SPPowerDataType | grep Charging | cut -d ":" -f2 | sed 's/ //g' | head -n 1`
printf "@battery_status:"
if [ $Charging = "Yes" ]
then 
    printf "Charging"
else
    if [ $Fully_charged = "Yes" ]
    then
        printf "Full"
    else
        printf "Discharging"
    fi
fi
printf "\n"


