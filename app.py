# import Helper.firebase
# import Recommended_System.recommend

# productsRC = Helper.firebase.GetProductRC()
# RS = Recommended_System.recommend.HybridRecommender(productsRC, k = 10)

from flask import Flask, request, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)  

@app.route('/')
def hello_world():
	return 'Hello World!'

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

if __name__ == "__main__":
    app.run()