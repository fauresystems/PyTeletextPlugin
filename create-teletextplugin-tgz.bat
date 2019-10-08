C:\"Program Files"\7-Zip\7z.exe a -ttar teletextplugin-%date:~6,4%%date:~3,2%%date:~0,2%.tar -xr!_SYNCAPP -xr!*.tgz -xr!*.vs -xr!*.pyc -xr!*.log.* -xr!.eric* -xr!_eric* -xr!__* ./
;C:\"Program Files"\7-Zip\7z.exe a -tgzip teletextplugin-1.0-%date:~6,4%%date:~3,2%%date:~0,2%.tgz teletextplugin-%date:~6,4%%date:~3,2%%date:~0,2%.tar
;del teletextplugin-%date:~6,4%%date:~3,2%%date:~0,2%.tar
