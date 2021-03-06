#imports!
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
#import cv2
 
class PiVideoStream:
	def __init__(self, resolution=(320,240), framerate=60):
		# initialize the camera and stream
		self.camera = PiCamera()
		self.camera.resolution = resolution
		#self.camera.hflip = True
		self.camera.framerate = framerate
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)
 
		self.camera.hflip=False
		self.camera.vflip=False
		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=(), daemon=False).start()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			self.frame = f.array
			#hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)
			self.rawCapture.truncate(0)
 
			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return

	def hflip(self):
		self.camera.hflip= !self.camera.hflip
	
	def vflip(self):
		self.camera.vflip= !self.camera.vflip

	def read(self):
		# return the frame most recently read
		return self.frame
 
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		self.join()
