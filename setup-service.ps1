#####
$serviceName = "Mabi-AH"
$mainFile = $pwd.Path + "\main.py"
$errorFileDir = $pwd.Path + "\output\error.txt"


.\nssm install $serviceName python $mainFile
.\nssm start $serviceName