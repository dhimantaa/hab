"""
Requirements:
speech_recognition
PyAudio
sounddevice
"""

import sounddevice as sd
import speech_recognition as sr

class speech_to_text:
    
    def __init__(self):
        return
        
    def device_details(self):
        print("\n"+"Sound related devices connected to the system are as follows:")
        print (sd.query_devices())
        print("\n")
        print("The  > and  < signs indicates the current active microphone and speaker:"+"\n")
        print("To change the microphone and speaker device pass the indices to device_setup method eg: device_setup([1,4])")
        
    def device_setup(self,device_index_list):
        sd.default.device=device_index_list
        print("The new setting is as follows:")
        print (sd.query_devices())

    def convert_using_google(self):
        r = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:                                                                       
            print("Speak:")                                                                                   
            audio = r.listen(source) 
        try:
            return (r.recognize_google(audio))
        except sr.UnknownValueError:
            return ("Could not understand audio")
        except sr.RequestError as e:
            return ("Could not request results; {0}".format(e))

        
            
        


