
from flask import Flask, render_template, Response, request,send_file,jsonify
from Pi_carema import Camera

app = Flask(__name__)

class G:
    camera_handle = None

@app.route('/')
def index():
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    while True:
        frame = G.camera_handle.export_video_stream()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/picture')
def take_picture():
    print("take picture!!!")
    picture_name  = G.camera_handle.take_picture()
    return  picture_name ,200

@app.route('/api/video')
def record_video():
    print("record_video!!")
    return "success",200

@app.route('/image/<picture_name>')
def image(picture_name):
    return send_file( "picture/"+ picture_name, as_attachment=True)





if __name__ == '__main__':
    G.camera_handle = Camera()
    #G.camera_handle.initialize()
    app.run(host='192.168.1.104', port =8080, debug=True, threaded=True)
