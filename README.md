# rclone-addon
Rclone addon for Kodi 

To be used with Android boxes and phones.

1. Place rclone.conf in profile directory
2. Install from zip
3. Configure the rclone command to run in the plugin configuration

Default: serve webdav your_rclone_remote:/ --addr :23457 --dir-cache-time 2400h --vfs-cache-max-age 2400h  --poll-interval 10m

Change your_rclone_remote to the rclone remote in your config.

Then you can add a Webdav Source to localhost:23457 in kodi to access your files.
