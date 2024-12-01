import Helper.firebase
import Recommended_System.recommend

productsRC = Helper.firebase.GetProductRC()
# print(productsRC)
RS = Recommended_System.recommend.HybridRecommender(productsRC, k = 10)

resultRC = RS.recommend("KH0001", "SP0039", False, True)

def display_products(products):
    print(f"{'Mã Sản Phẩm':<15}{'Tên Sản Phẩm':<70}{'Loại Sản Phẩm':<15}")
    print("="*200)
    for product in products:
        print(f"{product['MaSanPham']:<15}{product['TenSanPham']:<70}{product['LoaiSanPham']:<15}")

display_products(resultRC)