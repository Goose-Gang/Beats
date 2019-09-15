import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

import beats
import os
def test_download_song():
	beats.download_song_as_wav("https://firebasestorage.googleapis.com/v0/b/beatsme-66dd6.appspot.com/o/Sheppard%20-%20Keep%20Me%20Crazy.mp3?alt=media&token=26995dc3-d972-491f-b71e-9dd857a4ca00", "beep1")
	if os.path.exists("music/beep1.mp3"):
		print("mp3 download: passed")
	else:
		print("mp3 download: failed")

	if os.path.exists("music/beep1.wav"):
		print("mp3 to wav conversion: passed")
	else:
		print("mp3 to wav conversion: failed")

def test_clean_up_song():
	beats.clean_up_song('beep1')
	if os.path.exists("music/beep1.mp3") or os.path.exists("music/beep1.wav"):
		print("mp3 clean-up: failed")
	else:
		print("mp3 clean-up: passed")

def test():
	test_download_song()
	test_clean_up_song()