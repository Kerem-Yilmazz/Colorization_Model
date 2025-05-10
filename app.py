# İlk kodun aynısı burada kalacak
# Flask ve diğer kütüphaneleri import etme
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms
import io
import numpy as np

app = Flask(__name__)
CORS(app)  # Tüm yollar için CORS'u etkinleştir

# Model tanımı
class ColorizationNet(nn.Module):
    def __init__(self):
        super(ColorizationNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=5, stride=1, padding=4, dilation=2)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=5, stride=1, padding=4, dilation=2)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=5, stride=1, padding=4, dilation=2)
        self.conv4 = nn.Conv2d(128, 3, kernel_size=5, stride=1, padding=4, dilation=2)

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = nn.functional.relu(self.conv3(x))
        x = torch.sigmoid(self.conv4(x))
        return x

# Modeli oluşturma ve ağırlıkları yükleme (CPU üzerinde)
model = ColorizationNet()
try:
    model.load_state_dict(torch.load('colorization_model.pth', map_location=torch.device('cpu')))
    model.eval()
except Exception as e:
    print(f"Model yükleme hatası: {e}")

def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])
    img = Image.open(image).convert('L')  # Gri tonlamaya çevir
    img = transform(img).unsqueeze(0)
    return img

@app.route('/predict', methods=['POST'])
def predict_image():
    try:
        file = request.files['image']
        img_tensor = preprocess_image(file)

        with torch.no_grad():
            output = model(img_tensor)

        # Çıktı tensörünü görüntüye dönüştür
        output_image = output.squeeze().numpy().transpose(1, 2, 0) * 255
        output_image = np.clip(output_image, 0, 255).astype(np.uint8)
        pil_image = Image.fromarray(output_image)

        # Byte buffer'a kaydet
        img_io = io.BytesIO()
        pil_image.save(img_io, 'JPEG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
