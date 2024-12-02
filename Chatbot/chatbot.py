import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModel
from tensorflow.keras.layers import Input, Lambda, Dense, Concatenate, Conv1D, GlobalAveragePooling1D, Dropout, BatchNormalization, Bidirectional, LSTM, Layer
from tensorflow.keras.models import Model, load_model
from sklearn.utils import class_weight
import numpy as np

import DSA
import DSA.BinarySearch
import DSA.KMP
import Helper.helper
import Recommended_System.recommend

# Configuration and Model Parameters
bert_name = "vinai/phobert-base"

# Load pre-trained BERT model and tokenizer
bert = TFAutoModel.from_pretrained(bert_name)
tokenizer = AutoTokenizer.from_pretrained(bert_name)

MAX_LEN_CONTEXT = 25

class BERTEmbeddingLayer(Layer):
    def __init__(self, bert_model_name, max_length, **kwargs):
        super(BERTEmbeddingLayer, self).__init__(**kwargs)
        self.bert_model_name = bert_model_name
        self.max_length = max_length
        # Load the BERT model inside the layer
        self.bert = TFAutoModel.from_pretrained(bert_model_name)

    def call(self, inputs):
        input_ids, attention_mask = inputs
        # Obtain BERT outputs
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        return outputs.last_hidden_state  # Equivalent to outputs[0]

    def get_config(self):
        config = super(BERTEmbeddingLayer, self).get_config()
        config.update({
            'bert_model_name': self.bert_model_name,
            'max_length': self.max_length,
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)
    
model = tf.keras.models.load_model('model_coffee_question_classification.keras', custom_objects={'BERTEmbeddingLayer': BERTEmbeddingLayer})

MAX_LEN_CONTEXT = 25

def getNumberPredict(question):
  test_contexts = [question]

  # Tokenize the test contexts
  test_encodings = tokenizer(
      test_contexts,
      truncation=True,
      padding='max_length',
      max_length=MAX_LEN_CONTEXT,
      add_special_tokens=True,
      return_tensors='tf'
  )

  # Prepare input tensors
  test_input_ids = test_encodings['input_ids']
  test_attention_mask = test_encodings['attention_mask']

  # Make predictions using the model
  predictions = model.predict([test_input_ids, test_attention_mask], batch_size=32)

  # Convert predictions to class labels (e.g., using argmax)
  predicted_classes = np.argmax(predictions, axis=1)

  return predicted_classes[0]

beginMessage = "Chào bạn, ESPRO xin trả lời câu hỏi của bạn lưu ý đây là tin nhắn tự động của trí tuệ nhân tạo."
endMessage = (
    "Mong bạn hài lòng với câu trả lời của chúng tôi.\n"
    "Hiện tại, chúng tôi chỉ trả lời các câu hỏi liên quan đến thông tin sản phẩm, "
    "sản phẩm bán chạy và gợi ý sản phẩm.\nVí dụ:\n"
    "- Cà phê sữa còn hàng không?\n"
    "- Cho tôi danh sách sản phẩm bán chạy của quán.\n"
    "- Gợi ý cho tôi sản phẩm với.\n"
    "Chân thành cảm ơn bạn đã sử dụng dịch vụ của quán."
)
def getMessage(number, question, customer_id):
    message = [beginMessage]

    # Find products in the question
    productInQuestion = DSA.KMP.find_products_in_question_kmp_precomputed(question)
    sizeProductInQuestion = len(productInQuestion)

    ingredientInQuestion = DSA.KMP.find_ingredients_in_question_kmp_precomputed(question)

    if number == 0:
        # Information
        message.append("\n")
        message.extend(Helper.helper.getInfomationProduct(product) for product in productInQuestion)

    elif number == 1:
        # Top sell
        productIDs = Helper.helper.GetTopProductID()
        productTopSell = [DSA.BinarySearch.binary_search(productID) for productID in productIDs]

        message.append('Sản phẩm được bán chạy nhiều nhất của cửa hàng:\n')
        message.extend(f'- {product["TenSanPham"]}\n' for product in productTopSell)

    elif number == 2:
        # Recommendation
        product_id = productInQuestion[0]['MaSanPham'] if sizeProductInQuestion != 0 else "SP0001"
        user_id = "" if sizeProductInQuestion != 0 else customer_id

        productsRecommend = Recommended_System.recommend.RS.recommend(user_id, product_id, True, True)

        message.append('Sản phẩm gợi ý cho bạn:')
        message.extend(f'- {product["TenSanPham"]}' for product in productsRecommend)

    elif number == 3:
        productFromIngredients = Helper.helper.getProductFromIngredients(ingredientInQuestion)
        message.append('Các sản phẩm có thành phần bạn quan tâm:\n')
        message.extend(f'- {Helper.helper.getInfomationProduct(product)}' for product in productFromIngredients)

    elif number == 4:
        # Quality information
        if productInQuestion:
          message.append(f'Thông tin về chất lượng của sản phẩm: {Helper.helper.get_quality_info(productInQuestion)}\n')
        else:
          message.append('Sản phẩm của cửa hàng đều ngon.\n')

    elif number == 5:
        # Greeting
        message = ['Chào bạn! Cảm ơn bạn đã quan tâm đến cửa hàng của chúng tôi. Nếu bạn cần thông tin cụ thể về sản phẩm hoặc dịch vụ, vui lòng hỏi nhé!']

    # Combine the messages into a single string
    return '\n'.join(message) + '\n' + endMessage

def chatBotGetMessage(question, customer_id):
    number = getNumberPredict(question)
    return getMessage(number, question, customer_id)