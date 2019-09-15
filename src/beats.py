import urllib
import os
from pydub import AudioSegment

import librosa
from matplotlib import pyplot
import math
import numpy as np

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import firebase
import google.cloud.exceptions

# Use a service account
cred = credentials.Certificate('beatsme.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
storage = firebase.storage()

# given the url to a file, download the song and convert to wav
# save under music/wav
def download_song_as_wav(url, file_name):
	urllib.request.urlretrieve(url, "music/"+file_name+".mp3")
	sound = AudioSegment.from_mp3("music/"+file_name+".mp3")
	sound.export("music/"+file_name+".wav", format="wav")

# remove song from music and music/wav
def clean_up_song(file_name):
	if os.path.exists("music/"+file_name+".mp3"):
		os.remove("music/"+file_name+".mp3")
	if os.path.exists("music/"+file_name+".wav"):
		os.remove("music/"+file_name+".wav")

# given mp3 song name, discretize amplitude by second
def process_song(file_name):
	filename = "music/"+file_name+".wav"

	if not os.path.exists(filename):
		return

	y, sr = librosa.load(filename)

	'''
	FOR DEBUGGING
	print(y, sr)
	pyplot.plot(y)
	pyplot.savefig("graphs/original.png")
	pyplot.clf()
	'''

	#take absolute value
	y = abs(y)

	'''
	FOR DEBUGGING
	pyplot.plot(y)
	pyplot.show()
	pyplot.savefig("graphs/magnitude.png")
	pyplot.clf()
	'''

	#take average per second
	duration = math.ceil(librosa.get_duration(y=y, sr=sr))
	amplitude_by_second = np.array_split(y, duration)
	_get_array_mean = lambda a: np.mean(a)
	mean_func = np.vectorize(_get_array_mean)
	amplitude_by_second = mean_func(amplitude_by_second)

	#normalize
	#testing with timeit shows that max is faster than np.amax
	maximum = max(amplitude_by_second)
	# we want max value to be 1.0
	amplitude_by_second = amplitude_by_second/maximum
	return amplitude_by_second.tolist()

	'''
	FOR DEBUGGING
	pyplot.plot(amplitude_by_second)
	pyplot.savefig("graphs/final.png")
	pyplot.clf()
	'''

# given document_id and bars, write into Firestore Bars collection
def write_into_firestore(document_id, bars):
	if bars == None:
		return

	doc_ref = db.collection('Music').document(document_id).collection('Bars')
	batch = db.batch()
	for i in range(len(bars)):
		batch.set(doc_ref.document(), {
		    'timestamp': i,
		    'weight': round(bars[i],3)
		})
	batch.commit()

# given document_id, download the mp3 from firebase storage
def download_from_firestore(document_id):
	doc_ref = db.collection('Music').document(document_id)
	try:
		doc = doc_ref.get()
	except google.cloud.exceptions.NotFound:
		return
	
	doc_dict = doc.to_dict()
	if not 'path' in doc_dict:
		return
	path = doc_dict['path']
	gsReference = storage.refFromURL('gs://bucket/images/stars.jpg')
	print(gsReference)
			

download_from_firestore('cV03UE9fPMMI0V4NlwqS')

#write_into_firestore('cV03UE9fPMMI0V4NlwqS', process_song('beep1'))