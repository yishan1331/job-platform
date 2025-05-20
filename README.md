# TalentLabs 專案設置指南

## 系統架構

本專案採用前後端分離架構：

-   後端：Django + PostgreSQL
-   前端：Vue3 + Vite
-   認證：JWT (Ninja-jwt)

## 後端設置 (Backend Setup)

1. 進入後端目錄

```bash
cd backend
```

2. 建立虛擬環境

```bash
python -m venv venv
```

3. 啟動虛擬環境

```bash
source venv/bin/activate  # Linux/Mac
# 或
. venv/bin/activate      # Mac
```

4. 安裝依賴套件

```bash
pip install -r requirements.txt
```

5. 環境設定

-   將 `env.local` 檔案重命名為 `.env`
-   確保設定正確的資料庫連線資訊

6. 啟動 PostgreSQL 容器

```bash
docker-compose up -d
```

7. 執行資料庫遷移

```bash
python manage.py migrate
```

8. 建立管理員帳號

```bash
python manage.py createsuperuser
```

9. 啟動開發伺服器

```bash
python manage.py runserver
```

-   開發伺服器網址：http://127.0.0.1:8000/
-   API 文件：http://127.0.0.1:8000/api/v1/docs

## 前端設置 (Frontend Setup)

1. 進入前端目錄

```bash
cd frontend
```

2. 安裝依賴套件

```bash
npm install
```

3. 啟動開發伺服器

```bash
npm run dev
```

-   前端應用網址：http://localhost:5173/

## 系統功能說明

### 資料庫結構

-   Companies 表：管理公司資訊
-   Job Postings 表：管理職缺資訊（與 Companies 為一對多關係）
-   Users 表：管理使用者資訊

### 權限管理

系統支援三種使用者角色：

-   `applicant`：求職者
    -   僅能查詢職缺資訊
-   `recruiter`：招募者
    -   可管理所屬公司的職缺資訊
    -   與公司為一對一關係
-   `admin`：系統管理員
    -   擁有完整系統管理權限

### 重要說明

1. 職缺標題與公司組合必須為唯一值
2. 使用 JWT 進行身份驗證
3. 招募者只能查看和管理自己公司的職缺
4. 系統至少需要建立一個公司資料才能發布職缺

## 開發注意事項

-   確保 PostgreSQL 容器正常運行
-   遵循 API 文件規範進行開發
