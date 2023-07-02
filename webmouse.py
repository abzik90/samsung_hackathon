from flask import Flask, request
import pyautogui

app = Flask(__name__)

last_position = (0, 0)

@app.route('/')
def handle_request():
    accel_x = request.args.get('accel_x', default=0, type=int)
    accel_y = request.args.get('accel_y', default=0, type=int)
    action = request.args.get('action', default='move', type=str)

    global last_position
    x, y = last_position
    x += accel_x
    y += accel_y
    last_position = (x, y)

    if action == 'move':
        pyautogui.move(accel_x, accel_y)
        return f"Mouse moved to ({x}, {y})"
    elif action == 'click':
        pyautogui.click(x, y)
        return f"Mouse clicked at ({x}, {y})"
    else:
        return "Invalid action"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
