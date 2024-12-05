import tensorflow as tf
from tensorflow.keras import mixed_precision
tf.config.intra_op_parallelism_threads = 4  # Giới hạn số lượng thread CPU sử dụng
tf.config.inter_op_parallelism_threads = 2  # Điều chỉnh số lượng thread giữa các phép toán
tf.config.optimizer.set_jit(True)  # Bật JIT (XLA)

policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)

# import Recommended_System.recommend
import Chatbot.chatbot

# from flask import Flask, request, jsonify
# from flask_cors import CORS 

# app = Flask(__name__)
# CORS(app)  

# @app.route('/')
# def hello_world():
# 	return 'Hello World!'

# @app.route('/recommend', methods=['POST'])
# def recommendHTTP():
#     try:
#         data = request.get_json()

#         product_id = data['MaSanPham']
#         user_id = data['MaKhachHang']

#         productRecommend = RS.recommend(user_id, product_id, True, True)

#         return jsonify(productRecommend)
    
#     except Exception as e:
#         return jsonify({"error": str(e)})

print(Chatbot.chatbot.chatBotGetMessage("tôi nên dùng cà phê nào", "KH0001"))

# if __name__ == "__main__":
#     app.run()