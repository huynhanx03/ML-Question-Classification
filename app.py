import Recommended_System.recommend
import Chatbot.chatbot

from flask import Flask, request, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)  

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/recommend', methods=['POST'])
def recommendHTTP():
    try:
        data = request.get_json()

        product_id = data['MaSanPham']
        user_id = data['MaKhachHang']

        productRecommend = Recommended_System.recommend.RS.recommend(user_id, product_id, True, True)

        return jsonify(productRecommend)
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/chatbot', methods=['POST'])
def chatbotHTTP():
    try:
        data = request.get_json()

        question = data['CauHoi']
        user_id = data['MaKhachHang']

        resp = Chatbot.chatbot.chatBotGetMessage(question, user_id)

        return jsonify(resp)
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()