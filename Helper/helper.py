import random
from collections import Counter
import Helper.firebase

def GetTopProductID(number = 5):
  bill_data = Helper.firebase.GetBills()

  product_quantities = Counter()

  for bill_details in bill_data.values():
      for product_details in bill_details['ChiTietHoaDon'].values():
          product_quantities[product_details['MaSanPham']] += product_details['SoLuong']

  top_products = product_quantities.most_common(number)

  return [productID for productID, quantity in top_products]

def extract_number_from_id(product_id):
    return int(product_id[2:])

products = Helper.firebase.GetProducts()

def getProductFromIngredients(ingredients):
    ingredient_codes = {ingredient["MaNguyenLieu"] for ingredient in ingredients}

    matching_products = []

    for product in products:
        product_ingredient_codes = {ingredient['MaNguyenLieu'] for ingredient in product['CongThuc']}

        if ingredient_codes.issubset(product_ingredient_codes):
            matching_products.append(product)

    return matching_products[:5]

def getInfomationProduct(product):
    # Tạo câu mô tả sản phẩm
    text = f"{product['TenSanPham']} thuộc loại sản phẩm {product['LoaiSanPham']}. "
    text += f"Sản phẩm này được mô tả như sau: {product['MoTa']}. "
    text += "Nguyên liệu chính gồm: "

    # Danh sách các nguyên liệu từ 'CongThuc'
    ingredients = ", ".join(congthuc.get('TenNguyenLieu', 'N/A') for congthuc in product['CongThuc'])
    text += f"{ingredients}. "

    # Thông tin về số lượng sản phẩm hiện có
    text += f"Số lượng hiện tại trong kho: {product['SoLuong']}.\n"

    return text

def get_quality_info(products):
    product = ""

    if len(products) == 1:
        product = products[0]
    else:
        product = random.choice(products)

    message = f"Sản phẩm {product['TenSanPham']} rất ngon "
    ingredients = ", ".join(congthuc.get('TenNguyenLieu', 'N/A') for congthuc in product['CongThuc'])
    message += f"vì được làm từ những nguyên liệu chất lượng như {ingredients}."

    return message