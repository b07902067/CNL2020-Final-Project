# AP 在接觸史中的應用

### Usage
- 詳見 [demo連結](https://www.youtube.com/watch?v=EYR9DQhYl_4)

### 目的
將『和確診者在相近時段內，連接過同一AP者』定義為接觸者。

期望使用戶得以查詢自己與確診者是否進行過接觸。

### 架構
- Manage server
    - 可放置於內網或外網，負責提供用戶查詢自己的接觸史以及紀錄確診者上傳的紀錄
- AP server
    - 連接於AP之上，負責確保於相近時間內連接至該 AP 之人，能互相確認到彼此做過接觸
<img src="https://i.imgur.com/XOoxTWB.png" alt="Cover" width="50%"/>

### 實作
- 使用每人每日每小時皆不同的 ID 作為用戶身份的識別方式
- 詳見 [report](https://github.com/b07902067/CNL2020-Final-Project/blob/main/report.pdf)
