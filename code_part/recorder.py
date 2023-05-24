import sounddevice as sd
from scipy.io.wavfile import write
from fragment_fingerprinting import main_main
from flask import Flask, render_template, url_for, request

def record_some():
    freq = 22050
    duration = 15
    recording = sd.rec(int(duration * freq),
                    samplerate=freq, channels=1)
    sd.wait()
    write("../unknown_songs/recording_for_test.wav", freq, recording)
    return "../unknown_songs/recording_for_test.wav"

application = Flask(__name__)

@application.route("/")
def open_first_page():
    return render_template('index1.html')

@application.route("/map", methods = ["POST"])
def run_a_site():
    main_func = record_some()
    song = main_main(main_func)
    return render_template('index2.html', variable=song)


if __name__ == "__main__":
    application.run(port=8000, debug=True)
