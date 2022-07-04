import numpy as np
import os, cv2, flask, webbrowser, requests
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
app = flask.Flask(__name__)
app.secret_key = "secret key"

word = "none"
show_style = "none"
wordsize = "none"
# word_color = "#D68BBB"
# background_color = "#000000"



@app.route('/')
def home():
    global frequency #移動頻率
    frequency = 0
    return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)

@app.route("/get_Word", methods=["POST"])
def get_Word():
    global word
    word = flask.request.values.get('Word')
    return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)

# @app.route('/get_Color',  methods=['GET', 'POST'])
# def get_Color():
#     global word_color, background_color
#     word_color = flask.request.values.get('word-color')
#     background_color = flask.request.values.get('background-color')
#     return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)

@app.route("/set_mingliu")
def set_mingliu():
    global show_style, font_style
    font_style = "mingliu.ttc"
    show_style = "新明細體"
    return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)

@app.route("/set_msjh")
def set_msjh():
    global show_style, font_style
    font_style = "msjh.ttc"
    show_style = "微軟正黑體"
    return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)

@app.route("/set_kaiu")
def set_kaiu():
    global show_style, font_style
    font_style = "kaiu.ttf"
    show_style = "標楷體"
    return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)

@app.route("/set_24px")
def set_24px():
    global wordsize
    wordsize = "24"
    return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)
@app.route("/set_36px")
def set_36px():
    global wordsize
    wordsize = "36"
    return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)
@app.route("/set_48px")
def set_48px():
    global wordsize
    wordsize = "48"
    return flask.render_template('page.html', show_word_area = "輸入的文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)
@app.route("/set_64px")
def set_64px():
    global wordsize
    wordsize = "64"
    return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)
@app.route("/set_72px")
def set_72px():
    global wordsize
    wordsize = "72"
    return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize)


@app.route("/start",  methods=['GET', 'POST'])
def start():
    if word == "none" or word == "":
        return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize , show_status_area = "請輸入文字")
    if wordsize == "none":
        return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize, show_status_area = "請選擇字體大小")
    if show_style == "none":
        return flask.render_template('page.html', show_word_area = "輸入文字為: " + word, show_type_area = "選擇字體為: " + show_style, show_size_area = "字體大小為: " + wordsize, show_status_area = "請選擇字體")
    
    word_color = flask.request.values.get('word-color')
    background_color = flask.request.values.get('background-color')
    
    global image
    fontsize = int(wordsize)
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
    port = 3007
    link = "http://127.0.0.1:{0}".format(port)
    webbrowser.open(link)
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", debug = False, port = port)
