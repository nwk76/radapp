from flask import render_template, redirect, request, Flask
from pythonping import ping
import telnetlib


app = Flask(__name__)

ip_address = ""
is_ping_ok = None
is_login_ok = None
is_response_ok = None
username = ""
password = ""
command = ""
response = ""
telnet = None


@app.route("/start", methods=["GET", "POST"])
def start():
    global ip_address, is_login_ok, is_ping_ok, is_response_ok

    is_ping_ok = None
    is_login_ok = None
    is_response_ok = None

    if request.method == "POST":
        ip_address = request.form["ip_address"]
        ping_response = ping(ip_address)
        is_ping_ok = ping_response.success()

        if is_ping_ok:
            return redirect("/login")
        else:
            return render_template("start.html", ip_address=ip_address, is_ping_ok=is_ping_ok)
    else:
        return render_template("start.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    global ip_address, is_login_ok, password, telnet, username

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # LOGIN in reality
        # try:
        #     telnet = telnetlib.Telnet(ip_address)
        #     telnet.read_until(b"Login:")
        #     telnet.write(username.encode("ascii") + b"\n")
        #     telnet.read_until(b"Password:")
        #     telnet.write(password.encode("ascii") + b"\n")
        #     is_login_ok = True
        # except OSError as e:
        #     is_login_ok = False
        #     return render_template("login.html", ip_address=ip_address, is_telnet_ok=is_login_ok)

        # LOGIN simulation
        is_login_ok = True

        if is_login_ok is False:
            return render_template("login.html", ip_address=ip_address, is_login_ok=is_login_ok)
        elif is_login_ok:
            return redirect("/command")
    else:
        return render_template("login.html", ip_address=ip_address, is_login_ok=is_login_ok)


@app.route("/command", methods=["GET", "POST"])
def command():
    global command, ip_address, is_response_ok, response, telnet

    if request.method == "POST":
        command = request.form["command"]
        command_bytes = bytes(command + "\n", "utf-8")

        # RESONSE in reality
        # telnet.write(command_bytes)
        # response = telnet.read_all().decode("ascii")

        # RESPONSE simulation & verification
        response = "rad# bla bla bla from the device"
        is_response_ok = True

        return render_template("command.html", ip_address=ip_address, response=response, is_response_ok=is_response_ok)
    else:
        return render_template("command.html", ip_address=ip_address, response=response, is_response_ok=is_response_ok)


if __name__ == "__main__":
    app.run(debug=True)
