#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import queue

# Function to handle the software installation process
def install_selected_software():
    total_packages = len(selected_software)
    message_display.insert(tk.END, "Installing software...\n")
    
    # Create a list of commands to install selected software
    commands_to_run = []
    for package, var in selected_software:
        if var.get() == 1:
            installation_commands = {
                "firefox": "sudo apt-get install firefox -y",
                "google-chrome-stable": "wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo dpkg -i google-chrome-stable_current_amd64.deb && sudo apt-get install -f -y && rm google-chrome-stable_current_amd64.deb",
                "chromium-browser": "sudo apt-get install chromium-browser -y",
                "code": "wget https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64 -O code.deb && sudo dpkg -i code.deb && sudo apt-get install -f -y && rm code.deb",
                "sublime-text": "wget https://download.sublimetext.com/sublime-text_build-4107_amd64.deb && sudo dpkg -i sublime-text_build-4107_amd64.deb && rm sublime-text_build-4107_amd64.deb",
                "python3": "sudo apt-get install python3 -y",
                "nodejs": "curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash - && sudo apt-get install -y nodejs",
                "git": "sudo apt-get install git -y",
            }
            
            if package in installation_commands:
                commands_to_run.append(installation_commands[package])
    
    if not commands_to_run:
        message_display.insert(tk.END, "No software selected for installation.\n")
    else:
        # Use a thread-safe queue to manage installation order
        installation_queue = queue.Queue()
        for command in commands_to_run:
            installation_queue.put(command)
        
        # Start the installation process in a separate thread
        thread = threading.Thread(target=install_from_queue, args=(installation_queue,))
        thread.start()

# Function to install software packages one by one from a queue
def install_from_queue(installation_queue):
    while not installation_queue.empty():
        command = installation_queue.get()
        message_display.insert(tk.END, f"Running command: {command}\n")
        try:
            # Open a new terminal window for each installation command
            terminal_command = f"gnome-terminal -- bash -c '{command}; read -p \"Press Enter to continue...\"'"
            subprocess.Popen(terminal_command, shell=True)
            
            message_display.insert(tk.END, "Installation in progress...\n")
        except Exception as e:
            message_display.insert(tk.END, f"Error during installation: {str(e)}\n")
    
    message_display.insert(tk.END, "All selected software packages are installed!\n")

# Create the main application window
root = tk.Tk()
root.title("Software Installation App")
root.geometry("600x400")

# Create a label
label = tk.Label(root, text="Select Software to Install:")
label.pack()

# Create a list of software packages to install
software_packages = [
    "firefox",
    "google-chrome-stable",
    "chromium-browser",
    "code",  # Visual Studio Code
    "sublime-text",  # Sublime Text
    "python3",
    "nodejs",  # Node.js
    "git",  # Git
    # Add more software packages here
]

# Create Checkbuttons to select software packages
selected_software = []  # To store selected software
for package in software_packages:
    var = tk.IntVar()
    checkbox = tk.Checkbutton(root, text=package, variable=var)
    checkbox.pack()
    selected_software.append((package, var))  # Store the package name and its associated variable

# Create an "Install" button to start the installation process
install_button = tk.Button(root, text="Install", command=install_selected_software)
install_button.pack()

# Add a message display area (for displaying installation messages)
message_display = tk.Text(root, height=5, width=40)
message_display.pack()

# Run the GUI main loop
root.mainloop()


