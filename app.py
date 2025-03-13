from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Ваши ключи от Yandex Cloud
API_KEY = 'AQVN3ZRt6ebA5kd8RX9uNd_19qltrrmedcNd0oYO'
FOLDER_ID = 'b1gga2g49ehhsstgpaes'

# Yandex SpeechKit URL
SPEECHKIT_URL = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'

# Yandex NLP URL
NLP_URL = 'https://nlp.api.cloud.yandex.net/nlp/v1/analyze'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.json.get('text')
    voice = request.json.get('voice', 'oksana')

    # Запрос к Yandex SpeechKit
    response = requests.post(
        SPEECHKIT_URL,
        headers={
            'Authorization': f'Api-Key {API_KEY}',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'text': text,
            'lang': 'ru-RU',
            'voice': voice,
            'folderId': FOLDER_ID
        }
    )

    if response.status_code == 200:
        return response.content, 200, {'Content-Type': 'audio/mpeg'}
    else:
        return jsonify({'error': 'Ошибка при синтезе речи'}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json.get('text')

    # Запрос к Yandex NLP
    response = requests.post(
        NLP_URL,
        headers={
            'Authorization': f'Api-Key {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'folderId': FOLDER_ID,
            'analyzeSpecs': [{
                'text': text,
                'features': {
                    'classification': True,  # Анализ тональности
                    'keywords': True        # Извлечение ключевых слов
                }
            }]
        }
    )

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Ошибка при анализе текста'}), 500

if __name__ == '__main__':
    app.run(debug=True)