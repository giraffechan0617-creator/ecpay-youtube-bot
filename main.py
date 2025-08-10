from flask import Flask, request
import socket
import threading

# Twitch bot 設定（改成你的資料）
TWITCH_SERVER = "irc.chat.twitch.tv"
TWITCH_PORT = 6667
TWITCH_NICK = "qooq2011"  # Twitch 帳號（小寫）
TWITCH_TOKEN = "oauth:5ti4wm0fpwyjvi12wg8fhys324t4a9"  # https://twitchapps.com/tmi/
TWITCH_CHANNEL = "#陳景路"  # 前面要有 #

app = Flask(__name__)

# 發送訊息到 Twitch 聊天室
def send_twitch_message(message):
    sock = socket.socket()
    sock.connect((TWITCH_SERVER, TWITCH_PORT))
    sock.send(f"PASS {TWITCH_TOKEN}\n".encode("utf-8"))
    sock.send(f"NICK {TWITCH_NICK}\n".encode("utf-8"))
    sock.send(f"JOIN {TWITCH_CHANNEL}\n".encode("utf-8"))
    sock.send(f"PRIVMSG {TWITCH_CHANNEL} :{message}\n".encode("utf-8"))
    sock.close()

@app.route("/ecpay_notify", methods=["POST"])
def ecpay_notify():
    data = request.form.to_dict()
    video_url = data.get("CustomField1", "")  # 綠界備註欄放影片網址

    if "youtube.com" in video_url or "youtu.be" in video_url:
        threading.Thread(target=send_twitch_message, args=(f"/sr {video_url}",)).start()
    else:
        print(f"收到非 YouTube 連結：{video_url}")

    return "1|OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
