import gui
import sync_logic
import tkinter as tk
from tkinter import messagebox

def on_sync(src, dst):
    file_list.delete('1.0', tk.END)
    only_update_newer = update_newer_var.get()
    
    def on_sync_completed():
        verification_errors = sync_logic.verify_transfer(src, dst, file_list)  # Pass 'file_list' as an argument
        if verification_errors:
            for error in verification_errors:
                file_list.insert(tk.END, error + '\n', 'error')
        else:
            file_list.insert(tk.END, "Sync Complete.\n", 'complete')
            
    sync_logic.sync_directories(src, dst, lambda value: gui.update_status(progress_bar, value), file_list, tk.END, only_update_newer, on_sync_completed)
    
if __name__ == "__main__":
    app, progress_bar, file_list, update_newer_var = gui.create_app(on_sync)
    app.mainloop()
    
    
    