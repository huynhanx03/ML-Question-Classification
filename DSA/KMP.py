import Helper.firebase

product_list = Helper.firebase.GetProducts()
ingredient_list = Helper.firebase.GetIngredients()

def compute_lps_array(pattern):
    lps = [0] * len(pattern)
    length = 0 
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search_with_precomputed_lps(text, pattern, lps):
    i = 0  # Index for text
    j = 0  # Index for pattern

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            return True  # Pattern found
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return False  # Pattern not found

# Function to find product names in a question using precomputed LPS
def find_products_in_question_kmp_precomputed(question):
    question_lower = question.lower()
    lps_question = compute_lps_array(question_lower)

    detected_products = []

    for product in product_list:
        product_name = product["TenSanPham"].lower()
        if kmp_search_with_precomputed_lps(question_lower, product_name, lps_question):
            detected_products.append(product)

    return detected_products

def find_ingredients_in_question_kmp_precomputed(question):
    question_lower = question.lower()
    lps_question = compute_lps_array(question_lower)

    detected_ingredients = []

    for ingredient in ingredient_list:
        ingredient_name = ingredient["TenNguyenLieu"].lower()
        if kmp_search_with_precomputed_lps(question_lower, ingredient_name, lps_question):
            detected_ingredients.append(ingredient)

    return detected_ingredients