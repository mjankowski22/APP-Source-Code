cmd_/home/b-hermanowski/SIM8200_for_RPI/option/modules.order := {   echo /home/b-hermanowski/SIM8200_for_RPI/option/option.ko; :; } | awk '!x[$$0]++' - > /home/b-hermanowski/SIM8200_for_RPI/option/modules.order