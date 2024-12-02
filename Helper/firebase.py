import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Khởi tạo kết nối với Firebase
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://coffee-4053c-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def GetProducts():
    product_data = db.reference('SanPham').get()

    product_type_data = db.reference('LoaiSanPham').get()
    list_product_type = list(product_type_data.values())

    products = [
        {
            'MaSanPham': product['MaSanPham'],
            'TenSanPham': product['TenSanPham'],
            'SoLuong': product['SoLuong'],
            'MoTa': product['Mota'],
            'HinhAnh': product['HinhAnh'],
            'LoaiSanPham': next((x['LoaiSanPham'] for x in list_product_type if x['MaLoaiSanPham'] == product['MaLoaiSanPham']), None),
            'CongThuc': list(product['CongThuc'].values())
        }
        for product in product_data.values()
    ]

    return products
def GetEvaluate():
    evaluate_data = db.reference('DanhGia').get()

    evaluates = [
        {
            'MaKhachHang': evaluete['MaNguoiDung'],
            'MaSanPham': evaluete['MaSanPham'],
            'DiemDanhGia': evaluete['DiemDanhGia']
        }
        for evaluete in evaluate_data.values()
    ]

    return evaluates

def GetProductRC():
    product_data = db.reference('SanPham').get()

    product_type_data = db.reference('LoaiSanPham').get()
    list_product_type = list(product_type_data.values())

    products = [
        {
            'MaSanPham': product['MaSanPham'],
            'TenSanPham': product['TenSanPham'],
            'SoLuong': product['SoLuong'],
            'LoaiSanPham': next((x['LoaiSanPham'] for x in list_product_type if x['MaLoaiSanPham'] == product['MaLoaiSanPham']), None),
            'CongThuc': ' | '.join([congthuc['TenNguyenLieu'] for congthuc in product['CongThuc'].values()])
        }
        for product in product_data.values()
    ]

    return products

def GetBills():
    bill_data = db.reference('HoaDon').get()
    return bill_data

def GetIngredients():
    ingredient_data = db.reference('NguyenLieu').get()
    ingredients = list(ingredient_data.values())

    return ingredients