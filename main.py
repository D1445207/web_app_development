from flask import Flask, render_template, request, jsonify
from models.data import CPI_DATA, COMMODITY_PRICE

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/years', methods=['GET'])
def get_years():
    # 為了讓前端自動生成年份選項而保留的路由
    years = sorted(list(CPI_DATA.keys()))
    return jsonify({'years': years})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    start_year = int(data.get('start_year'))
    end_year = int(data.get('end_year'))
    amount = float(data.get('amount'))
    
    # F-01: 金額轉換運算 (由吳瑞誠負責完善邏輯)
    if start_year in CPI_DATA and end_year in CPI_DATA:
        real_value = amount * (CPI_DATA[end_year] / CPI_DATA[start_year])
    else:
        return jsonify({"error": "不支援的年份"}), 400

    # F-02: 商品具象化比較 (由何安負責完善邏輯)
    big_mac_count = real_value / COMMODITY_PRICE['big_mac']
    pork_bento_count = real_value / COMMODITY_PRICE['pork_bento']
    
    return jsonify({
        "real_value": round(real_value, 2),
        "big_mac_count": round(big_mac_count, 1),
        "pork_bento_count": round(pork_bento_count, 1)
    })

if __name__ == '__main__':
    app.run(debug=True)
