# import numpy as np 
# import pygame 

# class Controller: 
#     def __init__(self): 
#         self.gripper_closed = None 
        
#         pygame.init() 
#         pygame.joystick.init() 
        
#         self.joystick = pygame.joystick.Joystick(0)
#         self.joystick.init() 
        
#     def get_action(self): 
        
#         action = np.zeros(9) 
#         gripper_button_pressed = False 
        
#         action[0] = self.joystick.get_axis[0] 
#         action[1] = self.joystick.get_axis[1] 
        
#         # Map Left joystick to joint1 and joint2 angular velocity 
#         action[0] = action[0] * -1               # Left joystick horizontal 
#         action[1] = action[1] * -1               # Left stick vertical 
        
#         # Map Right joystick to joint3 and joint4 angular velocity 
        
#         action[2] = self.joystick.get_axis[2] 
#         action[3] = self.joystick.get_axis[3] 
        
#         action[3] = action[3] * -1               # Right joystick horizontal 
        
#         if self.joystcik.get_button(0): 
#             action[4] = -1.0                  
#             print("Button 0 is pressed")
        
#         elif self.joystcik.get_button(2): 
#             action[4] = 1.0                  
#             print("Button 2 is pressed")
        
#         elif self.joystcik.get_button(1):
#             self.gripper_closed = True
#             gripper_button_pressed = True
#             print("Button 1 is pressed")
        
#         elif self.joystcik.get_button(3):
#             self.gripper_closed = False
#             gripper_button_pressed = True
#             print("Button 3 is pressed")
            
#         elif self.joystick.get_button(4):
#             action[5] = 1.0
#             print("Button 4 is pressed")
            
#         elif self.joystick.get_button(5):
#             action[5] = -1.0
#             print("Button 5 is pressed")
        
#         elif self.joystick.get_button(6):
#             action[6] = 1.0
#             print("Button 6 is pressed")

#         elif self.joystick.get_button(7):
#             action[6] = -1.0
#             print("Button 7 is pressed")
        
#         elif self.joystick.get_button(8):
#             action[7] = 1.0
#             print("Button 8 is pressed")
        
#         elif self.joystick.get_button(9):
#             action[7] = -1.0
#             print("Button 9 is pressed")
        
#         mask = np.abs(action) >= 0.1
#         action = action * mask
#         action = np.where(action == -0.0, 0.0, action)
        
#         if np.all(action == 0 and gripper_button_pressed == False): 
#             action = None 
#         else: 
#             if self.gripper_closed == True: 
#                 action[7] = -1.0
#                 action[8] = -1.0
#             elif self.gripper_closed == False: 
#                 action[7] = 1.0
#                 action[8] = 1.0
      
#         return action
            
# # 2nd imp.        
# import numpy as np
# from flask_socketio import SocketIO

# class WebController:
#     def __init__(self, socketio):
#         self.socketio = socketio
#         self.gripper_closed = None
#         self.action = np.zeros(9)

#         @socketio.on('control_command')
#         def receive_command(data):
#             command = data['action']
#             self.map_command_to_action(command)

#     def map_command_to_action(self, command):
#         if command == 'up':
#             self.action[1] = -1
#         elif command == 'down':
#             self.action[1] = 1
#         elif command == 'left':
#             self.action[0] = -1
#         elif command == 'right':
#             self.action[0] = 1
#         elif command == 'grip_close':
#             self.gripper_closed = True
#         elif command == 'grip_open':
#             self.gripper_closed = False

#     def get_action(self):
#         if self.gripper_closed == True:
#             self.action[7] = -1.0
#             self.action[8] = -1.0
#         elif self.gripper_closed == False:
#             self.action[7] = 1.0
#             self.action[8] = 1.0
        
#         return self.action

# import numpy as np
# from flask_socketio import SocketIO

# class WebController:
#     def __init__(self, socketio):
#         self.socketio = socketio
#         self.gripper_closed = None
#         self.action = np.zeros(9)

#         @socketio.on('control_command')
#         def receive_command(data):
#             command = data.get('action')  # Use .get() for safety
#             if command:
#                 print(f"Received command: {command}")
#                 self.map_command_to_action(command)

#     def map_command_to_action(self, command):
#         # Reset action array before mapping
#         self.action.fill(0)  # Clear previous actions
        
#         # Map commands to action array similar to joystick
#         if command == 'up':
#             self.action[1] = -1  # Move up
#         elif command == 'down':
#             self.action[1] = 1   # Move down
#         elif command == 'left':
#             self.action[0] = -1  # Move left
#         elif command == 'right':
#             self.action[0] = 1   # Move right
#         elif command == 'grip_close':
#             self.gripper_closed = True
#             print("Gripper closed.")
#         elif command == 'grip_open':
#             self.gripper_closed = False
#             print("Gripper opened.")

#         # Handle gripper state actions
#         self.update_gripper_action()

#     def update_gripper_action(self):
#         # Update the action based on gripper state
#         if self.gripper_closed:
#             self.action[7] = -1.0  # Close gripper
#             self.action[8] = -1.0  # Close gripper
#         else:
#             self.action[7] = 1.0   # Open gripper
#             self.action[8] = 1.0   # Open gripper

#     def get_action(self):
#         # Return the current action state
#         return self.action


import numpy as np
from flask_socketio import SocketIO

class WebController:
    def __init__(self, socketio):
        self.socketio = socketio
        self.gripper_closed = None
        self.action = np.zeros(9)

        @socketio.on('control_command')
        def receive_command(data):
            command = data.get('action')  # Access 'action' instead of 'command'
            if command:
                self.map_command_to_action(command)
                print(f"Received command: {command}")

    def map_command_to_action(self, command):
        # Reset action array before mapping
        self.action.fill(0)  # Clear previous actions
        
        if command == 'up':
            self.action[1] = -1
        elif command == 'down':
            self.action[1] = 1
        elif command == 'left':
            self.action[0] = -1
        elif command == 'right':
            self.action[0] = 1
        elif command == 'grip_close':
            self.gripper_closed = True
            print("Gripper closed.")
        elif command == 'grip_open':
            self.gripper_closed = False
            print("Gripper opened.")

        # Set gripper actions based on the gripper state
        self.update_gripper_action()

    def update_gripper_action(self):
        if self.gripper_closed:
            self.action[7] = -1.0
            self.action[8] = -1.0
        else:
            self.action[7] = 1.0
            self.action[8] = 1.0

    def get_action(self):
        return self.action

