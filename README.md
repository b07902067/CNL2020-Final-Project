# 計網實 final project
- ![](https://i.imgur.com/frUxmPz.png)
- ![](https://i.imgur.com/7tmwvLX.png)

- 假設使用者都是好人的情況下，只是不希望洩漏隱私
- local 端只需要存 14 天的 key，如果 server 端想要用 key mapping client，則需要太大量的記憶體。
- Routine:
    - client 每天向一個獨立的 server 拿 <img src="https://render.githubusercontent.com/render/math?math=k_i">
    - client 連上 AP 後，將自己的 <img src="https://render.githubusercontent.com/render/math?math=ID_{ij}"> 繳給 AP，AP 確認沒問題後回傳目前紀錄過的 $ID$ 給 client.
- 若有 client 確診，即可上繳他 14 天內擁有的 key，供每個 client check 是否有接觸。

- MAC function
    - https://docs.python.org/3/library/hmac.html
    - key: 32 bytes

---

## Device
#### Management Server
- 獨立於外網的伺服器
- 負責產生 key
- 負責計算確診者的 ID 並公佈

#### AP server
- 連接在 AP 上的伺服器
- 負責記錄這個小時連線者的 ID 
- 負責轉送連線者的 ID 給所有連線者

#### client
- 每天連接 management server 取得 key，保存 14 天
- 連上 AP 時，自己負責算自己這小時的 ID
- 自己負責記錄 AP server 送過來的接觸者的 ID，保存 14 天
- 確診時，上傳自己的 14 個 key
- 可以連接 management server 檢查自己是否有和確診者接觸時

## Functions of each device
#### Management Server
- `genKey()`
    - 當 client 索取 key 的時候，從一個 key pool 裡面隨機選擇一個 key 
- `sendKey()`
    - 將 key 傳送給 client
- `recvKey()`
    - 從確診的 client 處獲得 14 個 key
- `computeID()`
    - 由從確診者處獲得的 14 個 key 來計算過去 14 天每個小時該 client 的 ID 為何，並公佈

#### AP server
- `reqID()`
    - 當有新的 client 連線進 AP 時，向其要求 ID
- `saveID()`
    - 儲存 client 提供的 ID 
- `sendID()`
    - 新連線的 client 提供其 ID 後，將此 ID 傳送給所有目前正在連線的 client，並且將前一個小時記錄到的所有 ID 傳送給這個新加入的 client


#### client
- `reqKey()`
    - 每天向 management server 要求一個 key
- `saveKey()`
    - 將 key 儲存起來
    - 須保存過去 13 天的 key 
- `computeID()`
    - 當被 AP server 要求 ID 時，使用今天的 key 來生成 ID 
- `sendID()`
    - 將 ID 送給 AP server 
- `recvID()`
    - 接收來自 AP server 的 ID
- `saveID()`
    - 儲存來自 AP server 的 ID
    - 這些 ID 資料會在 14 天後過期
- `sendKey()`
    - 當確診時，將 14 個 keys 送給 management server
- `checkID()`
    - 比對儲存在資料庫裡的 ID 和 management server 公布的確診者 ID ，檢查自己和確診者是否有接觸

---

## routine
- client 每天向 manage server 索取 key
>client.reqKey() 
><img src="https://render.githubusercontent.com/render/math?math=\rightarrow"> manage_server.genKey()  <img src="https://render.githubusercontent.com/render/math?math=\rightarrow"> manage_server.sendKey() 
><img src="https://render.githubusercontent.com/render/math?math=\rightarrow"> client.saveKey()
- 當 client 連上某 AP 時
>AP_server.reqID() 
><img src="https://render.githubusercontent.com/render/math?math=\rightarrow"> client.sendID(client.computeID())

> AP_server.sendID() 
><img src="https://render.githubusercontent.com/render/math?math=\rightarrow"> client.recvID() <img src="https://render.githubusercontent.com/render/math?math=\rightarrow"> client.saveID()
>
- 當某 client 連線的 AP 有新的連上的 client 時
>AP_server.sendID() 
><img src="https://render.githubusercontent.com/render/math?math=\rightarrow"> client.saveID()
- 當 client 確診時
>client.sendKey()  
><img src="https://render.githubusercontent.com/render/math?math=\rightarrow"> manage_server.recvKey() $<img src="https://render.githubusercontent.com/render/math?math=\rightarrow"> manage_server.computeID()
- 當 client 檢查過去 14 天是否有與確診者接觸時
>client.checkID() 






