# 路由與頁面設計文件 (API Design)

依據 PRD 與架構設計，本文件定義了「個人簿記系統」的所有的路由，包含 URL、HTTP 動作、對應的操作與將要渲染的 Jinja2 模板。在此遵循 RESTful 風格設計。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (明細清單) | GET | `/` | `templates/index.html` | 取得收支列表、統計總額並顯示首頁 |
| 新增收支頁面 | GET | `/records/new` | `templates/form.html` | 顯示新增收支紀錄的表單頁面 |
| 新增收支動作 | POST | `/records` | — | 接收表單並寫入資料庫，完成後重導到 `/` |
| 編輯收支頁面 | GET | `/records/<int:id>/edit` | `templates/form.html` | 依 ID 抓取特定紀錄並呈現在表單中供修改 |
| 更新收支動作 | POST | `/records/<int:id>/update`| — | 接收並更新指定 ID 的紀錄，完成後重導到 `/` |
| 刪除收支動作 | POST | `/records/<int:id>/delete`| — | 將指定的紀錄從資料庫刪除，完成後重導到 `/` |

> *備註：因瀏覽器原生表單不支援 PUT/DELETE 方法，所以更新與刪除操作改用 POST 來傳遞*。

## 2. 每個路由的詳細說明

### 首頁 (`/`)
- **輸入**: 無
- **處理邏輯**: 呼叫 `RecordModel.get_all()` 得到歷史紀錄，並進一步計算清單中的總收入、總支出與目前餘額。
- **輸出**: 將資料傳遞並渲染 `templates/index.html`。
- **錯誤處理**: 若無任何資料，於前端顯示「目前尚無紀錄」的提示。

### 新增收支頁面 (`/records/new`)
- **輸入**: 無
- **處理邏輯**: 準備渲染空白表單。
- **輸出**: 渲染 `templates/form.html`，可傳遞參數如 `action="new"` 供 Jinja2 判斷為新增狀態。

### 新增收支動作 (`/records`)
- **輸入**: 前端表單送出的 `type`, `amount`, `category`, `date`, `description`
- **處理邏輯**: 驗證必填欄位。成功後呼叫 `RecordModel.create(...)`。
- **輸出**: 成功後 `redirect(url_for('main.index'))`。
- **錯誤處理**: 如果欄位錯誤或漏填，利用 flash message 提醒使用者，並退回至 `/records/new`。

### 編輯收支頁面 (`/records/<int:id>/edit`)
- **輸入**: URL 中的 `id`
- **處理邏輯**: 呼叫 `RecordModel.get_by_id(id)`，若找不到該 ID 則產生 404 (Not Found)。
- **輸出**: 渲染 `templates/form.html`，並將取得的 `record` 資料傳入，讓 Jinja2 自動帶入預設值。

### 更新收支動作 (`/records/<int:id>/update`)
- **輸入**: URL 中的 `id` 以及表單送出的各個欄位
- **處理邏輯**: 呼叫 `RecordModel.update(...)` 來更新對應欄位。
- **輸出**: 更新完成後 `redirect(url_for('main.index'))`。
- **錯誤處理**: 若 `id` 不存在回傳 404；資料驗證失敗則保留輸入退回原表單。

### 刪除收支動作 (`/records/<int:id>/delete`)
- **輸入**: URL 中的 `id`
- **處理邏輯**: 呼叫 `RecordModel.delete(id)` 進行刪除。
- **輸出**: 執行後 `redirect(url_for('main.index'))`。

## 3. Jinja2 模板清單

視圖檔案將被統一放置於 `app/templates` 資料夾中。

- **`base.html`**:
  - 全站共用的基礎模板，包含 `<head>` 中的資源載入 (CSS, Fonts 等)，以及共用的導覽列和 Footer。
- **`index.html`**:
  - 繼承 `base.html`。
  - 用於顯示**頂部統計卡片**與**歷史明細清單**。
- **`form.html`**:
  - 繼承 `base.html`。
  - 設計成且**新增與編輯共用**的表單頁面（根據傳入的參數動態修改 `<form action="...">` 路徑及欄位初始值）。

## 4. 路由骨架程式碼
按照模組關注點分離原則，對應的 Python 檔案位於 `app/routes/` 之下：
- `app/routes/main.py`：處理首頁，以及將來不需要歸屬於特定資源的通用畫面。
- `app/routes/records.py`：專門負責收支紀錄資源的增刪改查介面。
