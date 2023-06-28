To run the simulation, the OPS_Simulation repository must be pulled. This repository is included as a subrespository.

In the inputs.py file, the parameters in the simulation can be adjusted. Some parameters are still present, but are not
used in the program litterInput["amount"], droneInput["dronetotal"], ... . When there is an array with multiple inputs,
the parameter can be specified for the small litter drone/litter and the big drone/litter.

To animate the a* pathplanning algorithm:
pathplanningPar["animation"]=True


To plot the operation:
simPar["plotOperation"]=True

Repository of the control code submodule 
https://github.com/ADIOS-DSE/OPS_Simulation.git
