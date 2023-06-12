#!/usr/bin/python3.4
from __future__ import absolute_import, division, unicode_literals
from future import standard_library
from future.builtins import *
standard_library.install_aliases()

import os, sys, xbmc, time, stat, xbmcvfs, xbmcaddon, xbmcplugin, xbmcgui, zipfile, gzip, subprocess, urllib.request

# Ajout de LOG pour la verification du type d'OS
xbmc.log(msg=f'RCLONE: Installation sur OS de type : {os.name}', level=xbmc.LOGINFO)
is_android: bool = hasattr(sys, 'getandroidapilevel')
xbmc.log(msg=f'RCLONE: Installation sur Android : {is_android}', level=xbmc.LOGINFO)

# Définition des variables de path pour les différents fichiers
PY3 =  sys.version_info > (3, 0)
if PY3:
	zippath  = xbmcvfs.translatePath("special://temp/rclone.gz")
	#loc = xbmcvfs.translatePath("special://xbmcbin/../../../cache/lib/rclone-android-16-arm")
	locandroid = xbmcvfs.translatePath("special://xbmcbin/../../../cache/lib/rclone-android-21-armv7a")
	locwin = xbmcvfs.translatePath("special://xbmcbin/rclone.exe")
	locposix = xbmcvfs.translatePath("special://xbmcbin/rclone")
	loc2 = xbmcvfs.translatePath("special://masterprofile/rclone.conf")
	pidfile  = xbmcvfs.translatePath("special://temp/librclone.pid")
	logfile  = xbmcvfs.translatePath("special://temp/librclone.log")
	cachepath  = xbmcvfs.translatePath("special://temp") 
else:
	zippath  = xbmc.translatePath("special://temp/rclone.gz")
	#loc = xbmc.translatePath("special://xbmcbin/../../../cache/lib/rclone-android-16-arm")
	locandroid = xbmc.translatePath("special://xbmcbin/../../../cache/lib/rclone-android-21-armv7a")
	locwin = xbmc.translatePath("special://xbmcbin/rclone.exe")
	locposix = xbmc.translatePath("special://xbmcbin/rclone")
	loc2 = xbmc.translatePath("special://masterprofile/rclone.conf")
	pidfile  = xbmc.translatePath("special://temp/librclone.pid")
	logfile  = xbmc.translatePath("special://temp/librclone.log")
	cachepath  = xbmc.translatePath("special://temp") 	

# Définition de l'URL source de l'executable rclone & de la destination de l'executable
rclone_version = xbmcaddon.Addon().getSetting("rclone-version")
# sourceurl = xbmcaddon.Addon().getSetting("rclonedownload")
# Par defaut pour Android
sourceurl = f'https://beta.rclone.org/{rclone_version}/testbuilds/rclone-android-21-armv7a.gz'
binary_path_in_zip_file = f'rclone-android-21-armv7a'
loc = locandroid
# Pour Windows
if os.name == 'nt':
	sourceurl = f'https://downloads.rclone.org/{rclone_version}/rclone-{rclone_version}-windows-amd64.zip'
	binary_path_in_zip_file = f'rclone-{rclone_version}-windows-amd64/rclone.exe'
	loc = locwin
# Pour linux
if os.name == 'posix' and not is_android:
	sourceurl = f'https://downloads.rclone.org/{rclone_version}/rclone-{rclone_version}-linux-amd64.zip'
	binary_path_in_zip_file = f'rclone-{rclone_version}-linux-amd64/rclone'
	loc = locposix
	
# Test de la présence du binaire rclone
if not xbmcvfs.exists(loc):
	# S'il n'existe pas téléchargement du binaire défini dans la variable `sourceurl`
	xbmc.log(msg=f'RCLONE: Aucun binaire détecté. téléchargement du fichier : {sourceurl}', level=xbmc.LOGINFO)
	
	# Création d'une barre de progression
	progress_bar = xbmcgui.DialogProgressBG()
	progress_bar.create('Download', '')

	def reporthook(block_number, block_size, total_size):
		if 0 == block_number & 511:
			 percent = (block_number * block_size * 100) / total_size
			 progress_bar.update(int(percent))
			 
	# Téléchargement du fichier défini dans `sourceurl` vers la destination `zippath`
	urllib.request.urlretrieve(sourceurl, zippath, reporthook)
	progress_bar.close()
	
	# Lecture du fichier zip ou gz
	if zipfile.is_zipfile(zippath):
		zip_file = zipfile.ZipFile(zippath, 'r')
		s = zip_file.read(binary_path_in_zip_file)
	else:
		zip_file = gzip.GzipFile(zippath, 'rb')
		s = zip_file.read()
	
	zip_file.close()
	
	output = open(loc, 'wb')
	xbmc.log(msg=f'RCLONE: Extraction du fichier [{binary_path_in_zip_file}] dans [{loc}]', level=xbmc.LOGINFO)
	output.write(s)
	output.close()
	st = os.stat(loc)
	os.chmod(loc, st.st_mode | stat.S_IEXEC)
else:
	xbmc.log(msg=f'RCLONE: Binaire [{loc}] détecté.', level=xbmc.LOGINFO)

# Construction de la commande webdav rclone à partir des éléments saisie dans les paramètres (au 1ier lancement, lors de l'installation, le script récupere les données par défaut)
#command = xbmcaddon.Addon().getSetting("parameters")
remote_name = xbmcaddon.Addon().getSetting("remote-name")
remote_folder = xbmcaddon.Addon().getSetting("remote-folder")
webdav_port = xbmcaddon.Addon().getSetting("webdav-port")
webdav_parameters = xbmcaddon.Addon().getSetting("webdav-parameters")
command = f'serve webdav {remote_name}:{remote_folder} --addr :{webdav_port} {webdav_parameters}'

def run(cmd):
	os.environ['PYTHONUNBUFFERED'] = "1"
	if os.name == 'nt':
		proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True  )
	else:
		proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True, shell = True  )
	xbmc.log(msg='RCLONE: Executing ' + cmd, level=xbmc.LOGINFO)
	stdout = []
	stderr = []
	mix = []
	while proc.poll() is None:
		line = proc.stdout.readline()
		if line != "":
			stdout.append(line)
			mix.append(line)
			xbmc.log(msg='RCLONE:' + line, level=xbmc.LOGINFO)
		line = proc.stderr.readline()
		if line != "":
			stderr.append(line)
			mix.append(line)
			xbmc.log(msg='RCLONE:' + line, level=xbmc.LOGINFO)
	return proc.returncode, stdout, stderr, mix

while True:
	if os.name == 'nt':
		code, out, err, mix = run("\"" + loc + "\" " + command + " --config \"" + loc2 + "\" --log-file \"" + logfile + "\" --cache-dir \"" + cachepath + "\"")
	else:
		code, out, err, mix = run(loc + " " + command + " --config " + loc2 + " --log-file=" + logfile + " --cache-dir " + cachepath + " &")
	time.sleep(2)
