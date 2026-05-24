# server.py
#
# Vespa Helper Server
# WebSocket temporário (compatível com joystick oficial)
#
# Instalar:
# pip install flask websocket-client
#
# Rodar:
# python server.py
#

import json
import os
import time

from flask import Flask, jsonify, render_template_string
from websocket import create_connection


# =========================================================
# CONFIG
# =========================================================

VESPA_WS = os.environ.get("VESPA_WS", "ws://192.168.4.1/ws")
PORT = int(os.environ.get("PORT", "5000"))

app = Flask(__name__)

logs = []


# =========================================================
# LOG
# =========================================================

def log(msg):

    global logs

    ts = time.strftime("%H:%M:%S")

    line = f"[{ts}] {msg}"

    print(line)

    logs.append(line)

    if len(logs) > 100:
        logs.pop(0)


# =========================================================
# WS TEMPORÁRIO
# =========================================================

def ws_send(data):

    ws = None

    try:

        payload = json.dumps(data)

        log(f"WS CONNECT")

        ws = create_connection(
            VESPA_WS,
            timeout=2
        )

        ws.send(payload)

        log(f"TX {payload}")

        time.sleep(0.03)

        ws.close()

        log("WS CLOSE")

        return True

    except Exception as e:

        log(f"ERRO {e}")

        try:
            if ws:
                ws.close()
        except Exception:
            pass

        return False


# =========================================================
# MOVIMENTO
# =========================================================

def frente():

    return ws_send({
        "velocidade": 70,
        "angulo": 90
    })


def tras():

    return ws_send({
        "velocidade": 70,
        "angulo": 270
    })


def esquerda():

    return ws_send({
        "velocidade": 70,
        "angulo": 180
    })


def direita():

    return ws_send({
        "velocidade": 70,
        "angulo": 0
    })


def parar():

    return ws_send({
        "velocidade": 0,
        "angulo": 0
    })


# =========================================================
# SERVOS
# =========================================================

def servo(sid, ang):

    return ws_send({
        "servo": sid,
        "posicao": ang
    })


# =========================================================
# HTML
# =========================================================

HTML = """

<!DOCTYPE html>
<html>

<head>

<title>Vespa WS Server</title>

<style>

body{
    background:#111;
    color:white;
    font-family:Arial;
    text-align:center;
    padding:20px;
}

.box{
    background:#222;
    max-width:900px;
    margin:auto;
    padding:20px;
    border-radius:14px;
}

button{

    width:140px;
    height:60px;

    border:none;

    border-radius:10px;

    margin:5px;

    font-size:18px;

    cursor:pointer;
}

.move{
    background:#2196f3;
    color:white;
}

.stop{
    background:#f44336;
    color:white;
}

.servo{
    width:350px;
}

#logs{

    margin-top:20px;

    background:black;

    text-align:left;

    padding:10px;

    height:260px;

    overflow:auto;

    font-family:monospace;
}

</style>

</head>

<body>

<div class="box">

<h1>🤖 Vespa WebSocket Server</h1>

<p>
Usando WebSocket temporário compatível com joystick oficial.
</p>

<hr>

<h2>Movimento</h2>

<button class="move" onclick="cmd('frente')">
↑ Frente
</button>

<br>

<button class="move" onclick="cmd('esquerda')">
← Esquerda
</button>

<button class="stop" onclick="cmd('parar')">
STOP
</button>

<button class="move" onclick="cmd('direita')">
Direita →
</button>

<br>

<button class="move" onclick="cmd('tras')">
↓ Ré
</button>

<hr>

<h2>Servos</h2>

<p>Servo 1</p>

<input
class="servo"
type="range"
min="0"
max="180"
value="90"
oninput="servo(1,this.value)"
>

<p>Servo 2</p>

<input
class="servo"
type="range"
min="0"
max="180"
value="90"
oninput="servo(2,this.value)"
>

<p>Servo 3</p>

<input
class="servo"
type="range"
min="0"
max="180"
value="90"
oninput="servo(3,this.value)"
>

<p>Servo 4</p>

<input
class="servo"
type="range"
min="0"
max="180"
value="90"
oninput="servo(4,this.value)"
>

<div id="logs"></div>

</div>

<script>

async function cmd(c){

    await fetch("/cmd/" + c,{
        method:"POST"
    })

}

async function servo(id,ang){

    await fetch("/servo/" + id + "/" + ang,{
        method:"POST"
    })

}

async function update(){

    let r = await fetch("/logs")

    let data = await r.json()

    document.getElementById("logs").innerHTML =
        data.logs.join("<br>")

}

setInterval(update,1000)

</script>

</body>
</html>

"""


# =========================================================
# ROTAS
# =========================================================

@app.route("/")
def home():

    return render_template_string(HTML)


# ---------------------------------------------------------

@app.route("/cmd/<cmd>", methods=["POST"])
def command(cmd):

    ok = False

    if cmd == "frente":
        ok = frente()

    elif cmd == "tras":
        ok = tras()

    elif cmd == "esquerda":
        ok = esquerda()

    elif cmd == "direita":
        ok = direita()

    elif cmd == "parar":
        ok = parar()

    return jsonify({
        "success": ok
    })


# ---------------------------------------------------------

@app.route("/servo/<int:sid>/<int:ang>", methods=["POST"])
def servo_route(sid, ang):

    ok = servo(sid, ang)

    return jsonify({
        "success": ok
    })


# ---------------------------------------------------------

@app.route("/logs")
def get_logs():

    return jsonify({
        "logs": logs[-30:]
    })


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print(" Vespa WebSocket Helper Server")
    print("======================================")
    print()

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False
    )