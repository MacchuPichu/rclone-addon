# rclone-addon
## Rclone addon for Kodi 

### To be used with 
- Android boxes/phones
- linux
- Windows

1. Place rclone.conf in profile directory (pour android : ANDROID\DATA\ORG.XBMC.KODI\FILES\.KODI\USERDATA)
2. Zip the folder script.service.rclone et garder le nom le 'script.service.rclone.zip'
3. Dans Kodi Parameters/addons/Install from zip
4. Redémarrer KODI

### Parametre du service
|Parameter name|Valeur par défaut|
|:--|:--|
|rclone-version		|"v1.62.2"|
|remote-name			|remote"|
|remote-folder		|"folder1/"|
|webdav-port			|"23457"|
|webdav-parameters	|"--dir-cache-time 2400h --vfs-cache-max-age 2400h --poll-interval 10m"|

#### rclone version pour android

* URL : https://beta.rclone.org/v1.62.2/testbuilds/rclone-android-21-armv7a.gz
* Mi Box S = arm v7a

### Add a library
Then you can add a Webdav Source to localhost:23457 in kodi to access your files like this : 
  - Protocole : Serveur WebDAV (HTTP)
  - Adresse du serveur : localhost
  - Port : 23457

### Help
Aide dans le fil : https://forum.kodi.tv/showthread.php?tid=354249
