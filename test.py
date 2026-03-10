from unilabos.devices.workstation.resin_workstation import ResinWorkstation

workstation = ResinWorkstation(port=8889)
workstation.connect_device()
res = workstation.post_process_discharge_off(1)
print(res)