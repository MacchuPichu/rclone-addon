# rclone-addon
Rclone addon for Kodi 

To be used with Android boxes and phones.

1. Place rclone.conf in profile directory : dans ANDROID\DATA\ORG.XBMC.KODI\FILES\.KODI\USERDATA
2. Install from zip
3. Configure the rclone command to run in the plugin configuration
4. Redémarrer KODI

Defaut rclone version : https://beta.rclone.org/v1.62.2/testbuilds/rclone-android-21-armv7a.gz
Mi Box S : arm v7a

Default: serve webdav pCloud_Encrypted:Médiathèque/ --addr :23457 --dir-cache-time 2400h --vfs-cache-max-age 2400h  --poll-interval 10m

Change your_rclone_remote to the rclone remote in your config.

Then you can add a Webdav Source to localhost:23457 in kodi to access your files.

Aide dans le fil : https://forum.kodi.tv/showthread.php?tid=354249
