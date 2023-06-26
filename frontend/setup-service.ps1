#####
$serviceName = "Mabi-AH-Frontend"
$mainFile = $pwd.Path + "\main.py"


.\nssm install $serviceName python $mainFile
.\nssm start $serviceName