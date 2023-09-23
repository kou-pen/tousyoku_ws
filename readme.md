# 盗食防止したい

## 仕組み
マーカーはOpenCVのArucoマーカーを使用(QRコードよりも都合が良かった)  
ついでにPDF化して使いやすくした  
顔識別はface_recognitionで行い、SQLAlchemyを用いてデータベースに登録
あとはFlask/Jinja2でなんとかしてる  
OpenCVによるカメラアクセスは排他制御であるため、  
`cv2.VideoCapture` をstaticmethod内に実装することで、各インスタンスで共通の処理を参照する  
おまけ機能でLINE Notifyを使って通知する  

## Raspiは何に使ってるの?
明るさセンサで撮影用ライト(今回はRpiHOMEのLEDで代用)を制御する  
FastAPIを用いてRpi側にAPIサーバーを立てて情報を取得  
こちら側からもAPIサーバーにデータを送ってLEDを制御   

## 使ったライブラリとか(requirements.txtなんて知らない)
OpenCV(cv2)  
numpy  
greenlet  
face_recognition  
img2pdf  
shutil  
sqlalchemy  
Flask  
jinja2  

wiringpi  
fastapi  
uvicorn  

## 参考サイト
https://pystyle.info/perform-face-recognition-with-python/  
https://rooter.jp/web-crawling/line-notify_with_python/  
https://docs.python.org/ja/3/library/configparser.html  
https://qiita.com/RIckyBan/items/a7dea207d266ef835c48  
https://python-academia.com/opencv-aruco/  

あとはメモし忘れた