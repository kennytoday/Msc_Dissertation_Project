# IMPORT ALL NECESARY LIBRARY


import tkinter as tk #GUI library
from tkinter import ttk

import threading # multi activity
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # graph
import time
import matplotlib.pyplot as plt # graph
from matplotlib.figure import Figure #graph
import numpy as np # datatype
import csv
import tensorflow as tf
from tensorflow import keras # AI
from tensorflow.keras import layers
from tensorflow.keras.models import load_model

# Initialize the main window
import serial

# Set up the serial connection


root = tk.Tk()
root.title("Battery Management System")
root.geometry("800x600")
root.configure(bg="#2c3e50")

# Create style
style = ttk.Style()
style.theme_use("clam")

# Define colors
bg_color = "#34495e"
fg_color = "#ecf0f1"
highlight_color = "#e74c3c"

# Configure styles
style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Helvetica", 14))
style.configure("TButton", background=highlight_color, foreground=fg_color,  font=("Helvetica", 12))
style.configure("TProgressbar", thickness=30)

# Header frame
header_frame = ttk.Frame(root, padding="10")
header_frame.pack(side=tk.TOP, fill=tk.X)

header_label = tk.Label(header_frame, text="KEHINDE ONI", fg = 'white', bg= 'black',font=("Helvetica", 28, "bold"))
header_label.pack(pady=10)

header_label = ttk.Label(header_frame, text="Battery Management System", font=("Helvetica", 16, "bold"))
header_label.pack(pady=10)

b_frame = ttk.Frame(root, width=300, height=300)
# b_frame.grid_propagate(False)  # Prevent the frame from resizing to fit its children
b_frame.pack()

b_frame.grid_columnconfigure(0, weight=1)
b_frame.grid_columnconfigure(1, weight=1)
b_frame.grid_columnconfigure(2, weight=1)
b_frame.grid_rowconfigure(0, weight=1)
# Footer frame
footer_frame = ttk.Frame(root, padding="10")
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
content_frame = None
graph_frame = None
epoch_label = None
def csv_to_numpy_array(csv_filename):
    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        data = list(reader)
        # Convert data to numpy array
        numpy_array = np.array(data, dtype=float)
    return numpy_array

csv_filename = 'workshop_datasheet01.csv'
numpy_array = csv_to_numpy_array(csv_filename)
canvas = None
fig = None



def sub_train_show():
    global canvas
    global fig
    global epoch_label
    full_data = numpy_array.tolist()
    x_train_list = []
    y_train_list = []
    x_test_list = []
    y_test_list = []
    train_lenght = int(len(full_data) * 0.6)
    test_lenght = len(full_data) - train_lenght
    count = 0
    for x in full_data:
        if count < train_lenght:
            x_train_list.append(x[: 3])
            if x[-1] == 1:
                y_train_list.append([1,0])
            else:
                y_train_list.append([0,1])

            
        else:
            x_test_list.append(x[: 3])
            if x[-1] == 1:
                y_test_list.append([1,0])
            else:
                y_test_list.append([0,1])
        count += 1

    x_train = np.array(x_train_list)
    y_train = np.array(y_train_list)

    x_val = np.array(x_test_list)
    y_val = np.array(y_test_list)

    model = keras.Sequential([
        layers.Dense(3, activation='relu', input_shape=(3,)),
        layers.Dense(20, activation='relu'),
        layers.Dense(20, activation='relu'),
        layers.Dense(2, activation='softmax')  # Use 'softmax' for multi-class classification
    ])

    class CaptureOutput(tf.keras.callbacks.Callback):
        def __init__(self, label):
            super().__init__()
            self.epoch_logs = []
            self.progress_count = 0
            self.label = label

        def on_epoch_end(self, epoch, logs=None):
            self.epoch_logs.append(logs)
            self.progress_count += 1
            root.after(0, self.update_label)
        
        def update_label(self):
            self.label.config(text= "EPOCH: " + str(self.progress_count * 2) + "%")
            if self.progress_count * 2 >= 99:
                self.label.config(fg = "#23bfff")
            else:
                self.label.config(fg = 'red')

            # print(f"Epoch {self.progress_count} ended.")  # Debugging statement

    output_capture = CaptureOutput(epoch_label)




    # Compile the model
    model.compile(optimizer='adam',  # You can choose other optimizers based on your task
                loss='categorical_crossentropy',  # Use 'categorical_crossentropy' for one-hot encoded labels
                metrics=['accuracy'])





    history = model.fit(x_train, y_train, epochs=50, batch_size=5, validation_data=(x_val, y_val), callbacks=[output_capture])

    # model
    model.save('kehinde_ai_model.h5')
    fig = Figure(figsize= (3.5,2.1), dpi= 120)
    fig.clf()
    canvas.get_tk_widget().pack_forget()
    ax2 = fig.add_subplot(111)
    ax2.plot(history.history['accuracy'], label = 'training')
    ax2.plot(history.history['val_accuracy'], label = 'validation')
    canvas = FigureCanvasTkAgg(fig, master = graph_frame)
    fig.set_size_inches(2,1)
    canvas.draw()
    canvas.get_tk_widget().pack()

def train_show():
    content_frame.pack_forget()
    graph_frame.pack(fill=tk.X)
    time.sleep(0.1)
    gui_thread2 = threading.Thread(target= sub_train_show)
    gui_thread2.start()
    


def control_show():
    content_frame.pack(expand=True, fill=tk.BOTH)
    graph_frame.pack_forget()

buttons1 = tk.Button(b_frame, bg = 'purple', width = 25, text = 'TRAIN NEURAL N', command = train_show)
buttons1.grid(row=0, column=0, padx=5, pady=5)

buttons2 = tk.Button(b_frame, bg = 'green', width = 25, text = 'AI CONTROL', command = control_show)
buttons2.grid(row=0, column=2, padx=5, pady=5)

def pp():
    global canvas
    global fig
    time.sleep(0.21)
    # fig, (ax2) = plt.subplots(1, 1)
    fig = Figure(figsize= (3.5,2.1), dpi= 120)
    arr2 = []#[1,4,2,8,3,9,5]
    ax2 = fig.add_subplot(111)
    ax2.plot(arr2,  color='purple')
    canvas = FigureCanvasTkAgg(fig, master = graph_frame)
    fig.set_size_inches(2,1)
    canvas.draw()
    canvas.get_tk_widget().pack()


gui_thread = threading.Thread(target=pp)
gui_thread.start()


# Main content frame
content_frame = ttk.Frame(root, padding="20")
content_frame.pack(expand=True, fill=tk.BOTH)


# Battery status frame
battery_frame = ttk.Frame(content_frame)
battery_frame.grid(row=0, column=0, padx=20, pady=4, sticky="nsew")


battery_label = ttk.Label(battery_frame, text="Battery Status")
battery_label.pack(pady=4)


battery_progress = ttk.Progressbar(battery_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
battery_progress.pack(pady=4)
battery_progress['value'] = 75  # Example battery percentage


# Temperature frame
temp_frame = ttk.Frame(content_frame)
temp_frame.grid(row=0, column=1, padx=20, pady=4, sticky="nsew")

temp_label = ttk.Label(temp_frame, text="Temperature")
temp_label.pack(pady=4)

temp_value_label = ttk.Label(temp_frame, text="35°C", font=("Helvetica", 18))
temp_value_label.pack(pady=4)

# Voltage frame
voltage_frame = ttk.Frame(content_frame)
voltage_frame.grid(row=1, column=0, padx=20, pady=4, sticky="nsew")

voltage_label = ttk.Label(voltage_frame, text="Voltage")
voltage_label.pack(pady=4)

voltage_value_label = ttk.Label(voltage_frame, text="3.7V", font=("Helvetica", 18))
voltage_value_label.pack(pady=4)

# Current frame
current_frame = ttk.Frame(content_frame)
current_frame.grid(row=1, column=1, padx=20, pady=4, sticky="nsew")

current_label = ttk.Label(current_frame, text="Current")
current_label.pack(pady=4)

current_value_label = ttk.Label(current_frame, text="2.5A", font=("Helvetica", 18))
current_value_label.pack(pady=4)

cycle_frame = ttk.Frame(content_frame)
cycle_frame.grid(row=2, column=0, padx=20, pady=4, sticky="nsew")

cycle_label = ttk.Label(cycle_frame, text="Cycle")
cycle_label.pack(pady=4)

cycle_value_label = ttk.Label(cycle_frame, text="43", font=("Helvetica", 18))
cycle_value_label.pack(pady=4)

prediction_frame = ttk.Frame(content_frame)
prediction_frame.grid(row=2, column=1, padx=20, pady=4, sticky="nsew")

prediction_label = ttk.Label(prediction_frame, text="Predict Activation")
prediction_label.pack(pady=4)

prediction_value_label = tk.Label(prediction_frame, text="ACTIVE", font=("Helvetica", 18), fg= 'green')
prediction_value_label.pack(pady=4)

graph_frame = ttk.Frame(root, padding="10")
epoch_label = tk.Label(graph_frame, text="EPOCH: 0%" , fg= 'red' , bg = 'black')
epoch_label.pack(pady=4)


word = ""
# Wait for the serial connection to initialize
voltage_ = 0
current_ = 0
temperature_ = 0
dictionary = {}
def th3():
    ser = serial.Serial(
        port='COM3',  # Replace with your port name
        baudrate=9600,  # Match the baud rate with your Arduino program
        timeout=1
        )   
    def read_from_arduino():
        global dictionary
        global voltage_
        global current_
        global temperature_
        time.sleep(5)
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                # print(f"Received: {line}")
                try:
                    dictionary = eval(line)
                    voltage_ = dictionary["Voltages"][-1]
                    current_ = dictionary["Current"]
                    temperature_ = dictionary["Temperature"]
                except:
                    print("incomplete stream")
                
                current_value_label.config(text = str(current_) + "A")
                voltage_value_label.config(text = str(voltage_) + "V")
                temp_value_label.config(text = str(temperature_) + "Celcius")

                

                

    if __name__ == "__main__":
        try:
            read_from_arduino()
        except KeyboardInterrupt:
            print("Program interrupted")
        finally:
            ser.close()
            print("Serial connection closed")

gui_thread3 = threading.Thread(target=th3)
gui_thread3.start()



exit_button = ttk.Button(footer_frame, text="Exit",  command=root.quit)
exit_button.pack(pady=4)

# Run the application
root.mainloop()
