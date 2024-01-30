#gui.py

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk

def show_completion_message():
	messagebox.showinfo("Sync Completed", "File synchronization is complete!")

def create_app(on_sync):
	app = tk.Tk()
	app.title("EnSync")
	
	left_frame = tk.Frame(app)
	left_frame.grid(row=0,column=0, padx=10, pady=10)
	
	y_spacing = 20
	x_spacing = 20
	row=0
	
	# Load the high-resolution image using PIL
	original_image = Image.open('ensync_logo.png')  # Ensure this is the path to your high-resolution image
	
	# Calculate the new size maintaining the aspect ratio
	base_width = 200  # Set this to the desired display width
	w_percent = (base_width / float(original_image.size[0]))
	h_size = int((float(original_image.size[1]) * float(w_percent)))
	
	# Resize the image for display while maintaining the high resolution data
	display_image = original_image.resize((base_width, h_size), Image.ANTIALIAS)
	
	# Convert the PIL image to a Tkinter-compatible photo image
	logo_image = ImageTk.PhotoImage(display_image)
	
	# Create a label to display the image
	logo_label = tk.Label(left_frame, image=logo_image)
	logo_label.image = logo_image  # Keep a reference to avoid garbage collection
	logo_label.grid(row=row, column=0, sticky='ew', padx=x_spacing, pady=(y_spacing, 0))
	row+=1
	
	src_entry = tk.Entry(left_frame)
	src_entry.grid(row=row, column=0, sticky='s', pady=(y_spacing,0), padx=x_spacing)
	row+=1
	
	src_button = tk.Button(left_frame, text="Select Source", command=lambda: select_directory(src_entry))
	src_button.grid(row=row, column=0, sticky='n', pady=(0,y_spacing))
	row+=1
	
	dst_entry = tk.Entry(left_frame)
	dst_entry.grid(row=row, column=0, sticky='s', pady=(y_spacing,0))
	row+=1
	
	dst_button = tk.Button(left_frame, text="Select Destination", command=lambda: select_directory(dst_entry))
	dst_button.grid(row=row, column=0, sticky='n', pady=(0,y_spacing))
	row+=1
	
	# Checkbox for 'Only Update Newer Files'
	update_newer_var = tk.BooleanVar(value=True)  # Default value is True
	update_newer_checkbox = tk.Checkbutton(left_frame, text="Only Update Newer", variable=update_newer_var)
	update_newer_checkbox.grid(row=row, column=0, pady=y_spacing)
	row += 1
	
	sync_button = tk.Button(left_frame, text="Start Sync", command=lambda: on_sync(src_entry.get(), dst_entry.get()))
	sync_button.grid(row=row, column=0, pady=y_spacing)
	row+=1
	
	# Progress Bar in the Status Frame (Modifying the existing status frame)
	status_frame = tk.Frame(left_frame)
	status_frame.grid(row=row, column=0, sticky="we", pady=(10))
	progress_bar = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
	progress_bar.pack(fill=tk.X, expand=True)
	
	# Right Frame (New)
	right_frame = tk.Frame(app)
	right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
	
	# Configure the weight of the right frame's column and row
	# This allows the listbox to expand
	right_frame.columnconfigure(0, weight=1)
	right_frame.rowconfigure(0, weight=1)
	
	# Replace the Listbox with a Text widget
	file_list = tk.Text(right_frame, height=15, width=50)
	file_list.configure(bg='white', padx=10, pady=10)
	file_list.pack(fill=tk.BOTH, expand=True)
	
	# Configure text tags for color-coding messages
	file_list.tag_configure('file', foreground='black')
	file_list.tag_configure('error', foreground='red')
	file_list.tag_configure('verify', foreground='blue')
	file_list.tag_configure('complete', foreground='green')
	
	return app, progress_bar, file_list, update_newer_var

def select_directory(entry):
	path = filedialog.askdirectory()
	entry.delete(0, tk.END)
	entry.insert(0, path)
	
def update_status(progress_bar, value):
	progress_bar['value'] = value
	progress_bar.update()
	