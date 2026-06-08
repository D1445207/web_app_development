# app/models/data.py

# 預設 CPI 參數字典 (基準年可自訂)
CPI_DATA = {
    2000: 80.5,
    2010: 92.3,
    2020: 102.1,
    2023: 105.8,
    2024: 108.2
}

# 預設商品單價字典 (用於具象化比較)
COMMODITY_PRICE = {
    "big_mac": 75,      # 大麥克價格
    "pork_bento": 100   # 排骨飯價格
}
