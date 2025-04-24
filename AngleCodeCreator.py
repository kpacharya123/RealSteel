from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='templates')

TEMPLATE_CODE = """
from robot_command.rpl import *
import math

set_units("mm", "deg")

def main():
    movej(j[0,0,0,0,{{ angle }},0], velocity_scale = 0.2)
    
    userFrame_pos_x = 400
    userFrame_pos_y = 0
    userFrame_pos_z = 550
    userFrame_rotation_A = 0
    userFrame_rotation_B = 0
    userFrame_rotation_C = 0
    set_user_frame("user_frame1", position=p[userFrame_pos_x, userFrame_pos_y, userFrame_pos_z, userFrame_rotation_A, userFrame_rotation_B, userFrame_rotation_C])
    change_user_frame("user_frame1")
    
    radius = 100
    for angle in range(0,180,5):
        y_coord = 100 * math.cos(math.radians(angle))
        z_coord = 100 * math.sin(math.radians(angle))
        movej(p[0, y_coord, z_coord, angle-{{ angle }},0,0], velocity_scale = 0.2)
    exit()
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Received request at /")  # Debugging output

    angle = 90  # Default angle
    if request.method == 'POST':
        try:
            angle = int(request.form['angle'])
            print(f"Received angle input: {angle}")
        except ValueError:
            print("Invalid input received, using default angle 90")
            pass  # Keep default if input is invalid
    
    generated_code = TEMPLATE_CODE.replace("{{ angle }}", str(angle))
    print(f"Generated code:\n{generated_code}")
    
    return render_template('index.html', code=generated_code, angle=angle)

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)