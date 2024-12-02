import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, normalize
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import load_model
import Helper.firebase

class CB(object):
    def __init__(self, Y_data, k=10, bias_factor=0.5):
        """
        Initialize the Content-Based Recommendation model.

        :param Y_data: List of products, each represented as a dictionary of attributes.
        :param k: Number of recommendations to return.
        :param bias_factor: Scaling factor for dynamic bias to control the balance between similarity and randomness.
        """
        self.Y_data = Y_data
        self.k = k
        self.weights = {"LoaiSanPham": 0.4, "CongThuc": 0.6}
        self.bias_factor = bias_factor
        self.tfidf = TfidfVectorizer()
        self.one_hot_encoder = OneHotEncoder(sparse_output=False)

    def embeddings_matrix(self):
        """
        Create the embeddings matrix based on product attributes.
        - LoaiSanPham (Product Type) uses one-hot encoding.
        - CongThuc (Recipe) uses TF-IDF for vectorization.
        """
        type_features = self.one_hot_encoder.fit_transform(
            [[p["LoaiSanPham"]] for p in self.Y_data]
        ) * self.weights["LoaiSanPham"]

        recipe_features = self.tfidf.fit_transform(
            [p["CongThuc"] for p in self.Y_data]
        ).toarray() * self.weights["CongThuc"]

        self.combined_features = normalize(
            np.hstack([type_features, recipe_features])
        )

    def calculate_similarity(self):
        """
        Calculate the similarity matrix with a dynamic bias.
        - Cosine similarity is calculated for the embeddings.
        - A dynamic bias is added to the similarity score to promote diversity.
        """
        base_similarity = cosine_similarity(self.combined_features)

        random_bias = np.random.rand(*base_similarity.shape)

        self.similarity_matrix = base_similarity + self.bias_factor * random_bias * (1 - base_similarity)

    def refresh(self):
        """
        Refresh the embeddings matrix and similarity matrix.
        This should be called whenever the product data changes.
        """
        self.embeddings_matrix()
        self.calculate_similarity()

    def fit(self):
        """
        Initialize and prepare the recommendation model.
        """
        self.refresh()

    def recommend(self, product_id):
        """
        Recommend products based on a given product ID.

        :param product_id: The product ID to base recommendations on.
        :return: A list of recommended products.
        """
        idx = next(i for i, Y in enumerate(self.Y_data) if Y["MaSanPham"] == product_id)

        sorted_indices = sorted(
            enumerate(self.similarity_matrix[idx]),
            key=lambda x: -x[1]
        )

        return [self.Y_data[i] for i, _ in sorted_indices[:self.k]]
    
class CF(object):
    def __init__(self, k=10):
        self.user_factors = np.load("Data/user_factors.npy")
        self.item_factors = np.load("Data/item_factors.npy")

        with open("Data/user_index_mapping.pkl", "rb") as f:
            self.user_index_mapping = pickle.load(f)
        with open("Data/item_index_mapping.pkl", "rb") as f:
            self.item_index_mapping = pickle.load(f)

        self.model = load_model("Model/recommendation_model.h5")

        self.k = k

    def recommend(self, u):
        user_index = self.user_index_mapping.get(u)

        if user_index is not None:
            user_vector = self.user_factors[user_index]

            predicted_scores = []

            for item_id, item_index in self.item_index_mapping.items():
                item_vector = self.item_factors[item_index]
                score = self.model.predict([np.array([user_vector]), np.array([item_vector])])[0][0]
                predicted_scores.append((item_id, score))

            predicted_scores.sort(key=lambda x: x[1], reverse=True)
            print(predicted_scores)
            return [item_id for item_id, score in predicted_scores[:self.k]]

        else:
            return []
        
class HybridRecommender:
    def __init__(self, products, k = 10):
        self.cb_recommender = CB(products, k)
        self.cb_recommender.fit()

        self.cf_recommender = CF(k = k)

        self.k = k

        self.products = products

    def recommend(self, user_id, product_id, isCF, isCB):
        recommendations = []

        if user_id and isCF:
            # Sử dụng Collaborative Filtering đầu tiên
            # Chỉ có các mã sản phẩm
            cf_recommendations = self.cf_recommender.recommend(user_id)
            cf_recommendations = [product for product in self.products if product['MaSanPham'] in cf_recommendations]
            recommendations = cf_recommendations

        if product_id and isCB:
            if len(recommendations) < self.k:
                # Nếu không đủ, sử dụng Content-based Filtering
                num_more = self.k - len(recommendations)
                cb_recommendations = self.cb_recommender.recommend(product_id)

                for product in cb_recommendations:
                    if product['MaSanPham'] == product_id:
                        continue

                    if num_more == 0:
                        break

                    if product not in recommendations:
                        recommendations.append(product)
                        num_more -= 1

        return recommendations
    
productsRC = Helper.firebase.GetProductRC()
RS = HybridRecommender(productsRC, k = 10)