cmd_/home/b-hermanowski/SIM8200_for_RPI/qmi_wwan_simcom/Module.symvers := sed 's/ko$$/o/' /home/b-hermanowski/SIM8200_for_RPI/qmi_wwan_simcom/modules.order | scripts/mod/modpost -m -a   -o /home/b-hermanowski/SIM8200_for_RPI/qmi_wwan_simcom/Module.symvers -e -i Module.symvers   -T -
