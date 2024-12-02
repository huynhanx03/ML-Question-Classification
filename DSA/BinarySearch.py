import Helper.helper
import Helper.firebase

products = Helper.firebase.GetProducts()
product_size = len(products)

def binary_search(product_id):
    left, right = 0, product_size - 1
    while left <= right:
        mid = (left + right) // 2
        mid_id = Helper.helper.extract_number_from_id(products[mid]['MaSanPham'])
        target_id = Helper.helper.extract_number_from_id(product_id)
        if mid_id == target_id:
            return products[mid]
        elif mid_id < target_id:
            left = mid + 1
        else:
            right = mid - 1
    return None