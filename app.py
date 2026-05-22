from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import requests
import io

app = Flask(__name__)

@app.route('/annotate', methods=['POST'])
def annotate():
    data = request.json
    image_url = data['thumbnailUrl']
    obj = data['objectsFound'][0]
    label = obj['type']
    box = obj['box']

    img_response = requests.get(image_url)
    img = Image.open(io.BytesIO(img_response.content))

    w, h = img.size
    x1 = int(box['left'] * w)
    y1 = int(box['top'] * h)
    x2 = int(box['right'] * w)
    y2 = int(box['bottom'] * h)

    draw = ImageDraw.Draw(img)

    if label.lower() == 'person':
        # Full box with padding and thin line
        pad = 8
        draw.rectangle(
            [x1 - pad, y1 - pad, x2 + pad, y2 + pad],
            outline='#FF0000',
            width=2
        )
    else:
        # Corner targeting for vehicles
        lw = 5
        cl = min(int((x2 - x1) * 0.25), int((y2 - y1) * 0.25), 30)
        # Top left
        draw.line([(x1, y1), (x1 + cl, y1)], fill='#00FF00', width=lw)
        draw.line([(x1, y1), (x1, y1 + cl)], fill='#00FF00', width=lw)
        # Top right
        draw.line([(x2, y1), (x2 - cl, y1)], fill='#00FF00', width=lw)
        draw.line([(x2, y1), (x2, y1 + cl)], fill='#00FF00', width=lw)
        # Bottom left
        draw.line([(x1, y2), (x1 + cl, y2)], fill='#00FF00', width=lw)
        draw.line([(x1, y2), (x1, y2 - cl)], fill='#00FF00', width=lw)
        # Bottom right
        draw.line([(x2, y2), (x2 - cl, y2)], fill='#00FF00', width=lw)
        draw.line([(x2, y2), (x2, y2 - cl)], fill='#00FF00', width=lw)

    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)

    return send_file(buf, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
