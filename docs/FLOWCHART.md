<<<<<<< HEAD
# 使用者與系統流程圖

```mermaid
graph TD
    A[使用者進入首頁] --> B[輸入：原始年份、目標年份、金額]
    B --> C{點擊計算按鈕}
    C --> D[前端發送 API 請求]
    D --> E[後端: 金額轉換運算 F-01]
    E --> F[後端: 換算大麥克/排骨飯數量 F-02]
    F --> G[後端回傳計算結果]
    G --> H[前端: 更新巨大結果顯示區]
    H --> I[前端: 寫入/更新本次登入的歷史紀錄 F-03]
    I --> J[畫面顯示 3-5 筆歷史紀錄清單]
    J --> B
```
=======
# 使用者與系統流程圖 (FLOWCHART)

本文件依據 PRD 與架構設計，繪製了「個人簿記系統」的操作路徑以及背後資料流動的關係，方便確保各個環節沒有遺漏。

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站開始，一直到完成每一項任務（如新增、編輯、刪除收支等）的瀏覽路徑與選項。

```mermaid
flowchart LR
    A([使用者開啟網站]) --> B[首頁 - 收支明細與結餘總覽]
    
    B --> C{選擇欲執行的操作}
    
    C -->|檢視統計| D[瀏覽首頁的分類統計區塊]
    D --> B
    
    C -->|新增收支| E[點擊新增按鈕]
    E --> F[進入「新增紀錄」表單頁]
    F --> G[填寫金額、日期、分類等]
    G --> H([送出表單])
    H --> B
    
    C -->|編輯紀錄| I[點擊特定紀錄的編輯按鈕]
    I --> J[進入「編輯紀錄」表單頁]
    J --> K[修改內容]
    K --> L([送出修改])
    L --> B
    
    C -->|刪除紀錄| M[點擊特定紀錄的刪除按鈕]
    M --> N{跳出確認視窗}
    N -->|確認| O([送出刪除指令])
    O --> B
    N -->|取消| B
```

## 2. 系統序列圖（Sequence Diagram）

以下描繪使用者進行「新增一筆收支紀錄」時，從瀏覽器到 Flask 伺服器再到資料庫的詳細溝通序列。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (View)
    participant Flask as Flask 路由 (Controller)
    participant Model as 紀錄模型 (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 在表單填寫收支資訊並點擊送出
    Browser->>Flask: HTTP POST /record/add (傳遞表單 Data)
    Flask->>Flask: 驗證欄位是否完整與格式是否正確
    Flask->>Model: 呼叫 add_record(amount, category, date...)
    Model->>DB: 執行 SQL: INSERT INTO records ...
    DB-->>Model: 操作成功 (回傳受影響資料)
    Model-->>Flask: 成功通知
    Flask-->>Browser: HTTP 302 重導向 (Redirect) 到首頁 (/)
    Browser->>Flask: HTTP GET / (請求首頁與最新資料)
    Flask-->>Browser: 回傳渲染完畢的新首頁 HTML 
    Browser->>User: 畫面更新，顯示最新列表與結餘
```

## 3. 功能清單與路由對照表

開發時將依照以下對應表格來建置 Flask 路由，涵蓋目前 MVP 階段中所有的必須功能操作。

| 功能描述 | URL 路徑 | HTTP 方法 | 備註說明 |
| --- | --- | --- | --- |
| 顯示首頁 (明細與總結) | `/` | GET | 從 Model 取得所有紀錄，計算總收支並呈現列表 |
| 新增紀錄表單頁面 | `/record/add` | GET | 呈現一個空白的 HTML 表單元件 |
| 接收並處理新增紀錄 | `/record/add` | POST | 接收表單發送的字典資料，寫入資料庫後 Redirect |
| 編輯紀錄表單頁面 | `/record/edit/<int:id>` | GET | 以 id 取出該紀錄原有資料，填補進表單供使用者修改 |
| 接收並處理編輯紀錄 | `/record/edit/<int:id>` | POST | 接收修改後的表單資料，更新資料庫紀錄並 Redirect |
| 接收並處理刪除紀錄 | `/record/delete/<int:id>`| POST | （通常透過隱藏表單送出）從資料庫刪除紀錄並 Redirect |

>>>>>>> 363dcaa7c992d8f9048f739053a6f9344920de7b
