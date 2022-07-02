import numpy as np
import os, cv2, flask, webbrowser, requests
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
app = flask.Flask(__name__)
app.secret_key = "secret key"
RGB = "none"
word = "none"
show_style = "none"
word_color = "none"
background_color = "none"




@app.route('/')
def home():
    global frequency #移動頻率
    frequency = 0
    return flask.render_template('page.html', show_word_area = "輸入的文字為: " + word, show_type_area = "選擇的字體為: " + show_style)

@app.route("/get_Word", methods=["POST"])
def get_Word():
    global word
    word = flask.request.values.get('Word')
    return flask.render_template('page.html', show_word_area = "輸入的文字為: " + word, show_type_area = "選擇的字體為: " + show_style)

@app.route("/set_mingliu")
def set_mingliu():
    global show_style, font_style
    font_style = "mingliu.ttc"
    show_style = "新明細體"
    return flask.render_template('page.html', show_word_area = "輸入的文字為: " + word, show_type_area = "選擇的字體為: " + show_style)

@app.route("/set_msjh")
def set_msjh():
    global show_style, font_style
    font_style = "msjh.ttc"
    show_style = "微軟正黑體"
    return flask.render_template('page.html', show_word_area = "輸入的文字為: " + word, show_type_area = "選擇的字體為: " + show_style)

@app.route("/set_kaiu")
def set_kaiu():
    global show_style, font_style
    font_style = "kaiu.ttf"
    show_style = "標楷體"
    return flask.render_template('page.html', show_word_area = "輸入的文字為: " + word, show_type_area = "選擇的字體為: " + show_style)


word_color = (0,255,255)
background_color = (255, 251, 240)

@app.route("/start",  methods=['GET', 'POST'])
def start():
    global image
    fontsize = 32
    
    font = ImageFont.truetype(font_style, fontsize, encoding='utf-8')
    # RGB
    image = Image.new(mode = 'RGB', size = (fontsize * len(word), fontsize), color = background_color)
    draw = ImageDraw.Draw(image)
    if font_style == "msjh.ttc":
        draw.text((0, -1 * (fontsize/5)), word, fill = word_color, font=font)
    else:
        draw.text((0,0), word, fill = word_color, font=font)
    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    
    return flask.render_template('execute.html')

@app.route('/video_feed')
def video_feed():
    return flask.Response(frames(), mimetype = 'multipart/x-mixed-replace; boundary=frame')
 ##移動速度
def frames():
    while True:
        frame = cv2.resize(image, None, fx = 960 / image.shape[0], fy= 960 / image.shape[0], interpolation = cv2.INTER_AREA)
        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass
        first = image[:,[0]]
        for i in range(image.shape[1]-1):
            image[:,[i]] = image[:,[i+1]]
        image[:,[image.shape[1]-1]] = first

if __name__ == "__main__":
    port = 3000
    link = "http://127.0.0.1:{0}".format(port)
    webbrowser.open(link)
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", debug = False, port = port)
