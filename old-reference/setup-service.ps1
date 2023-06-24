#####
$serviceName = "Mabi-AH"
$mainFile = $pwd.Path + "\main.py"
#$outputFileDir = $pwd.Path + "\output\output.txt"
$errorFileDir = $pwd.Path + "\output\error.txt"


.\nssm install $serviceName python $mainFile
# nssm set $serviceName AppStdout $outputFileDir
.\nssm set $serviceName AppStderr $errorFileDir
.\nssm start $serviceName