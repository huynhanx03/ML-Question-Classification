import random
import os
import pandas as pd
from datetime import datetime, timedelta

def create_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

size = 1000

def create_evaluate_data():
    evaluate_data = []
    
    for _ in range(1, size + 1):
        evaluate_data.append({
            "MaKhachHang": f"KH{random.randint(1, 10):04d}",
            "MaSanPham": f"SP{random.randint(1, 50):04d}",
            "DiemDanhGia": random.randint(1, 5)
        })

    return evaluate_data

def create_bill_data():
    bill_data = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now()

    for _ in range(1, size + 1):
        random_date = create_random_date(start_date, end_date)
        bill_data.append({
            "MaKhachHang": f"KH{random.randint(1, 10):04d}",
            "MaSanPham": f"SP{random.randint(1, 50):04d}",
            "SoLuong": random.randint(1, 10),
            "NgayTao": random_date.strftime('%d/%m/%Y')  # Định dạng ngày dd/MM/yyyy
        })
            
    return bill_data

def export_to_csv(data, file_name, fieldnames):
    directory = '../Data'
    if not os.path.exists(directory):
        os.makedirs(directory)

    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)

    file_path = os.path.join(directory, file_name)
    df.to_csv(file_path, index=False, encoding='utf-8', header=fieldnames)

evaluate_data = create_evaluate_data()
export_to_csv(evaluate_data, "evaluates.csv", ["MaKhachHang", "MaSanPham", "DiemDanhGia"])

bill_data = create_bill_data()
export_to_csv(bill_data, "bills.csv", ["MaKhachHang", "MaSanPham", "SoLuong", "NgayTao"])