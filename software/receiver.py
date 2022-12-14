import logging
import subprocess
from datetime import date, datetime
from json import loads
from math import log, log10
from sys import stdout

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests

######################################################################
# PRIVATE DATA

# MAC_ADDRESS = "${mac}"
# TOKEN = '${token}'
MAC_ADDRESS = "44:17:93:11:2F:DB"
TOKEN = "Token 1234"

######################################################################
# GlOBAL DATA

RECEIVER_MODE = "LOCAL"  # LOCAL or TUNNEL

######################################################################
# PLOT DATA

fig, (ax_t, ax_b) = plt.subplots(2)
fig.suptitle('Monitoring')
time_x = []
temps_y = []
brightness_y = []
######################################################################
# We search for dynamic IP of specific MAC address


def get_ip_by_mac(macaddr):
    try:
        # for now - uncomment if arp -a does not see NodeMCU
        # TODO - more accurate solution
        # for i in range (0, 255):
        #    system(f"ping 192.168.0.{i}")

        cmd = f'arp -a | findstr "{macaddr.replace(":", "-").lower()}" '

        returned_output = subprocess.check_output(
            (cmd), shell=True, stderr=subprocess.STDOUT)

        IP_ADDRESS = str(returned_output).split(' ', 1)[1].split(' ')[1]

        return IP_ADDRESS

    except Exception:
        print("[ERROR] IP not found, check WiFi connection of NodeMCU.")
        exit()


######################################################################
# http-get to nodemcu server


def request_update(ipaddr):
    try:
        return requests.get(
            f"http://{ipaddr}/update",
            headers={'Authorization': TOKEN},
        ).content.decode("utf-8")
    except (requests.ConnectionError):
        print("[ERROR] Connection failed.")
        return None
    except (requests.HTTPError):
        print("[ERROR] HTTP connection failed.")
        return None
    except (requests.Timeout):
        print("[ERROR] Connection timeout.")
        return None

######################################################################
# Convert raw voltages to SI format

def normalize(answer):
    # Convert raw temperature data to Celsius degrees
    normalized_temperature = 1 / \
        (log((answer["temperature"] * 0.5 * 5.0 / 1023.0) / 2.5) /
         4300.0 + 1.0 / 298.0) - 273.0

    # Convert raw brightness data to lux

    normalized_brightness = pow(10, (log10(
        20000 / ((answer["brightness"] * 0.5 * 10000) / (1024 - answer["brightness"] * 0.5))) / 0.37))

    # Round and save
    answer["temperature"] = round(normalized_temperature, 2)
    answer["brightness"] = round(normalized_brightness, 2)

    return answer


######################################################################

def get_data(ip):
    answer = request_update(ip)

    if answer:
        logging.info(
            f'{datetime.now().time().replace(microsecond=0)} {answer}')

        answer = normalize(loads(answer))

        logging.info(
            f'{datetime.now().time().replace(microsecond=0)} Normalized data: {answer}')

        return answer

    return None

######################################################################


def animate_plot(i, ip, time_x, temps_y, bright_y):
    time_x.append(datetime.now().strftime('%H:%M:%S'))

    answer = get_data(ip)
    if not answer:
        return

    logging.info(f'{datetime.now().time().replace(microsecond=0)} GOT MEASUREMENTS: {answer}')
    temps_y.append(answer["temperature"])
    bright_y.append(answer["brightness"])

    time_x = time_x[-20:]
    temps_y = temps_y[-20:]
    bright_y =  bright_y[-20:]

    ax_t.clear()
    ax_b.clear()
    ax_t.plot(time_x, temps_y)
    ax_b.plot(time_x, bright_y)

    # Format plot
    ax_t.tick_params('x', labelrotation=45)
    ax_t.set_title('Temperatures')
    ax_t.set_ylabel('Temperature (deg C)')

    ax_b.tick_params('x', labelrotation=45)
    ax_b.set_title('Brightness')
    ax_b.set_ylabel('Brightness (lux)')

    fig.tight_layout()
    plt.subplots_adjust(bottom=0.30)

######################################################################

def main():
    dn = date.today()

    logging.basicConfig(filename=f"{dn}.log", level=logging.INFO)

    logging.getLogger().addHandler(logging.StreamHandler(stdout))

    logging.info(
        f'{datetime.now().time().replace(microsecond=0)} New session starting')

    if (RECEIVER_MODE == "LOCAL"):
        IP_ADDRESS = get_ip_by_mac(MAC_ADDRESS)

    elif (RECEIVER_MODE == "TUNNEL"):
        IP_ADDRESS = '3ecea0ee0d12.ngrok.io'
    else:
        print("[ERROR] Please specify receiver mode")

    logging.info(
        f'{datetime.now().time().replace(microsecond=0)} Starting for IP: {IP_ADDRESS}')

    ani = animation.FuncAnimation(fig, animate_plot, fargs=(IP_ADDRESS, time_x, temps_y, brightness_y), interval=10000)
    plt.show()

######################################################################


if __name__ == '__main__':
    main()
