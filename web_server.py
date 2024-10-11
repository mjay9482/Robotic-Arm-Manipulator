# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit

# app = Flask(__name__)
# socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @socketio.on('control_command')
# def handle_control(data):
#     command = data['action']
#     print(f"Received control command: {command}")
#     emit('response', {'status': 'Command received'})

# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000)


from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

# Define a ROS 2 Node to handle commands
class CommandPublisher(Node):
    def __init__(self):
        super().__init__('command_publisher')
        self.publisher_ = self.create_publisher(String, 'robot_commands', 10)

    def publish_command(self, command):
        msg = String()
        msg.data = command
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing command: {command}')

# Initialize ROS 2
rclpy.init()
command_publisher = CommandPublisher()

# Run ROS 2 in a separate thread
def ros_thread():
    while rclpy.ok():
        rclpy.spin_once(command_publisher)

# Start the ROS thread
ros_thread_instance = Thread(target=ros_thread)
ros_thread_instance.start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('control_command')
def handle_control(data):
    command = data['action']
    print(f"Received control command: {command}")
    command_publisher.publish_command(command)  # Publish the command to ROS 2
    emit('response', {'status': 'Command received'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
    rclpy.shutdown()
