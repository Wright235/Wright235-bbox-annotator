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
    
    color = 'red' if label.lower() == 'person' else 'blue'
    
    img_response = requests.get(image_url)
    img = Image.open(io.BytesIO(img_response.content))
    
    w, h = img.size
    x1 = int(box['left'] * w)
    y1 = int(box['top'] * h)
    x2 = int(box['right'] * w)
    y2 = int(box['bottom'] * h)
    
    draw = ImageDraw.Draw(img)
    draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
    draw.text((x1, y1 - 20), label, fill=color)
    
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    
    return send_file(buf, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
