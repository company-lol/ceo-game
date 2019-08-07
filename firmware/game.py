import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time 
import led
import cv2
from tinydb import TinyDB, Query

#GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

class webcam:
    def __init__(self, path="./images/"):
        self.path = path
        pass
        
    def capture(self, num_images = 5, base_filename="cam"):
        camera = cv2.VideoCapture(0)
        
        for i in range(num_images):
            return_value, image = camera.read()
            filename = self.path + base_filename+'_'+str(i)+'.png'
            print(filename)
            cv2.imwrite(filename, image)
        del(camera)



class button:
    states = ['ready','started','stopped']
    button_state = 0
    button_state_time = 0
    button_delay = 1

    def __init__(self):
        if self.button_state_time == 0:
            self.button_state_time = time.time()

    def button_callback(self, channel):
        now = time.time()
        if ((now-self.button_state_time)>self.button_delay):
            print("Button was pushed!")
            self.button_state_time = now
            if self.button_state == 0:
                self.button_state = 1
            elif self.button_state == 1:
                self.button_state = 2
            elif self.button_state == 2:
                self.button_state = 0
    
    def state(self):
        return self.states[self.button_state]

def main():
    led.clear()
    cam = webcam()
    cam.capture()

    db = TinyDB('./scores.json')
    
    print("Press button to start game\n\n")
    b = button()
    GPIO.add_event_detect(10,GPIO.RISING, callback=b.button_callback) # Setup event on pin 10 rising edge
    
    ready_state = False
    stopped_state = True
    while True:
        while b.state() =="ready":
            if not ready_state:
                led.display("00.00000")
                
                ready_state = True
                stopped_state = False
            start = time.time()
        while b.state() == "started":
            time.sleep(.1)
            end = time.time()
            elapsed = end - start
            float_elapsed = float(elapsed)
            (left,right)= str(float_elapsed).split(".")
            left = left.rjust(2,"0")
            right= right[:5]
            formatStr = left + "." + right
            led.display(formatStr)
        while b.state() == "stopped":
            if not stopped_state:
                timestr = time.strftime("%Y%m%d-%H%M%S")
                score = abs(float(formatStr)-10)
                obj = {'timestamp': timestr, 'time': formatStr, 'score':score}
                cam = webcam()
                cam.capture(base_filename=timestr)
                db.insert(obj)
                print("image captured: " + formatStr)
                stopped_state = True
                ready_state = False

        pass

    GPIO.cleanup() # Clean up

if __name__ == "__main__":
    main()
    
