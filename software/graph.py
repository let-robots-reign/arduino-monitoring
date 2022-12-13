from time import strftime, sleep
from tkinter import *
from random import randint, uniform
######################################################################
# CONSTANTS

MAX_TEMPERATURE = 40.0
MIN_TEMPERATURE = 0.0

MAX_BRIGHTNESS = 250
MIN_BRIGHTNESS = 0

######################################################################
# Queues of data

values_i = []
values_t = []
values_b = []


######################################################################

MODE = "REAL"  # REAL or FAKE

# Fake data


def generate_fake():
    rand = {'iteration': randint(0, 2500), 'temperature': round(uniform(
        MIN_TEMPERATURE, MAX_TEMPERATURE), 2), 'brightness': round(uniform(MIN_BRIGHTNESS, MAX_BRIGHTNESS), 2)}

    values_i.append(int(rand['iteration']))

    values_t.append(float(rand['temperature']))

    values_b.append(float(rand['brightness']))

######################################################################
# Bar (temperature, brightness)


def horizontal_bar(root, current_value, x, y, bar_length, bar_height, min_value, max_value, bar_color, bar_name):

    canv = Canvas(root, width=bar_length + 50, height=bar_height + 40,
                  bg='black', bd=0, highlightthickness=0, relief='ridge')

    canv.place(x=x, y=y)

    if (current_value > max_value):
        current_value = max_value-1

    value = (float(bar_length) / float(max_value)) * current_value

    # Bar border

    canv.create_rectangle(1, 1, bar_length, bar_height,
                          fill='black', outline='white')

    # Inner bar

    canv.create_rectangle(2, 2, int(value), bar_height -
                          1, fill=bar_color, outline=bar_color)

    # Bar serifs

    # 1
    canv.create_line(1, bar_height, 1, bar_height+5, width=1, fill='white')

    # 2
    canv.create_line(bar_length, bar_height, bar_length,
                     bar_height+5, width=1, fill='white')

    # 3
    canv.create_line(1+bar_length/4, bar_height, 1+bar_length/4,
                     bar_height+5, width=1, fill='white')

    # 4
    canv.create_line(1+bar_length/2, bar_height, 1+bar_length/2,
                     bar_height+5, width=1, fill='white')

    # 5
    canv.create_line(1+bar_length-bar_length/4, bar_height, 1+bar_length -
                     bar_length/4, bar_height+5, width=1, fill='white')

    # Minimal value label
    canv.create_text(0, bar_height+10, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=str(min_value))

    # Maximum value label
    canv.create_text(bar_length - 10, bar_height+10, font='Rockwell 10',
                     anchor='w', justify=CENTER, fill='white', text=str(max_value))

    # Serif labels

    canv.create_text(bar_length/2 - 10, bar_height+10, font='Rockwell 10',
                     anchor='w', justify=CENTER, fill='white', text=str(int(max_value/2)))

    canv.create_text(bar_length/4-10, bar_height+10, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=str(int(max_value/4)))

    canv.create_text(bar_length-bar_length/4-10, bar_height+10, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=str(int(max_value-max_value/4)))

    # Current value label

    canv.create_text(bar_length/2 - 10, bar_height-8, font='Rockwell 10',
                     anchor='w', justify=CENTER, fill='white', text=str(current_value))

    # Bar name

    canv.create_text(1, bar_height+21, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=bar_name)

######################################################################
# Plot (temperature, brightness)


def plot(root, x, y, box_length, box_height, min_value, max_value, color, name, data):

    canv = Canvas(root, width=box_length + 50, height=box_height + 40,
                  bg='black', bd=0, highlightthickness=0, relief='ridge')

    canv.place(x=x, y=y)

    # Box border
    canv.create_rectangle(1, 1, box_length, box_height,
                          fill='black', outline=color)

    # Dash lines
    canv.create_line(50, box_height / 2, box_length - 5, box_height / 2,
                     width=0.1, fill='white', dash=(4, 2))

    canv.create_line(50, box_height / 4, box_length - 5, box_height / 4,
                     width=0.1, fill='white', dash=(4, 2))

    canv.create_line(50, box_height - box_height / 4, box_length - 5, box_height -
                     box_height/4, width=0.2, fill='white', dash=(4, 2))

    # Serif labels

    canv.create_text(10, box_height - 10, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=str(min_value))

    canv.create_text(10, 12, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=str(max_value))

    canv.create_text(10, box_height / 2, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=str(int(max_value / 2)))

    canv.create_text(10, box_height / 4, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=str(int(max_value-max_value / 4)))

    canv.create_text(10, box_height - box_height / 4, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=str(int(max_value / 4)))

    # Current value label

    canv.create_text(1, box_height + 25, font='Rockwell 10', anchor='w',
                     justify=CENTER, fill='white', text=name)

    # Zero dot
    prev_y = box_height - float(box_height) / float(max_value) * data[0]

    prev_x = 5

    cur_x = 0

    # Connect all data

    for counter in range(0, len(data)):

        value = data[counter]

        cur_y = box_height - float(box_height) / float(max_value) * value

        cur_x += 10

        canv.create_line(prev_x, prev_y, cur_x, cur_y, width=1.5, fill=color)

        prev_y = cur_y
        prev_x = cur_x

    # Get latest value

    latest_value = data[len(data) - 1]

    # Output latest data value

    canv.create_line(cur_x, box_height - 10, cur_x, 0, width=0.5, fill='white')

    canv.create_text(cur_x + 10, cur_y, font='Rockwell 12', anchor='w',
                     justify=CENTER, fill='white', text=str(latest_value))

    canv.create_text(cur_x + 10, cur_y + 20, font='Rockwell 12', anchor='w',
                     justify=CENTER, fill='white', text=strftime('%H:%M:%S'))


######################################################################
# Update tkinter data

def update(data_json):
    if MODE == "REAL":
        values_i.append(data_json["iteration"])
        values_t.append(data_json["temperature"])
        values_b.append(data_json["brightness"])
    elif MODE == "FAKE":
        generate_fake()

    # Iteration number

    data = values_i.pop(0)

    canv.itemconfig(iter, text=str(data))

    # Temperature bar

    data = values_t.pop(0)

    horizontal_bar(
        root, data, 20, 50, 450, 20, MIN_TEMPERATURE, MAX_TEMPERATURE, 'red', 'Temperature')

    history_t.append(data)

    # Brightness bar

    data = values_b.pop(0)

    horizontal_bar(
        root, data, 20, 120, 450, 20, MIN_BRIGHTNESS, MAX_BRIGHTNESS, 'green', 'Brightness')

    history_b.append(data)

    # Draw plots

    plot(root, 20, 180, 200, 200, MIN_TEMPERATURE,
         MAX_TEMPERATURE, 'red', 'Temperature', history_t)

    plot(root, 270, 180, 200, 200, MIN_BRIGHTNESS,
         MAX_BRIGHTNESS, 'green', 'Brightness', history_b)

    # Clear history if chart is full

    if len(history_t) == 19:
        history_t.clear()

    if len(history_b) == 19:
        history_b.clear()


######################################################################

# Plot history
history_b = []
history_t = []

root = Tk()

# Window title
root.title('SCADA')

# Window geometry
root.geometry('{}x{}'.format(500, 500))
root.resizable(width=False, height=False)

# Background

canv = Canvas(root, width=510, height=510, bg='black')

# Crutch due to tkinter's magic
canv.place(x=-10, y=-10)

# Title
canv.create_text(190, 20, font='Georgia 14', anchor='w',
                    justify=CENTER, fill='white', text='Kafka-to-OPCUA')

# Iteration number
canv.create_text(250, 40, font='Georgia 12', anchor='w',
                    justify=CENTER, fill='white', text=str(0))

# Tkinter main loop
root.mainloop()
