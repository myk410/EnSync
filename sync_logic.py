#sync_logic.py

import os
import shutil
import tkinter as tk

def is_system_file(file_name):
	# Add other system file names if needed
	return file_name in ['.DS_Store', 'Thumbs.db']

def sync_directories(src, dst, update_progress, file_list, end, only_update_newer, completion_message_func):
	total_files = sum([len(files) for r, d, files in os.walk(src) if not is_system_file(files)])
	processed_files = 0
	
	for src_dir, dirs, files in os.walk(src):
		dst_dir = src_dir.replace(src, dst, 1)
		if not os.path.exists(dst_dir):
			os.makedirs(dst_dir)
			
		for file_ in files:
			if is_system_file(file_):
				continue  # Skip system files
			
			src_file = os.path.join(src_dir, file_)
			dst_file = os.path.join(dst_dir, file_)
			
			if only_update_newer:
				# Only update if source file is newer
				if os.path.exists(dst_file) and os.stat(src_file).st_mtime <= os.stat(dst_file).st_mtime:
					continue
				
			try:
				shutil.copy2(src_file, dst_dir)
				file_list.insert(tk.END, f"Copying: {src_file} to {dst_file}\n\n", 'file')
			except Exception as e:
				file_list.insert(tk.END, f"Error copying {src_file}: {str(e)}\n\n", 'error')
				
			processed_files += 1
			progress = 100 if total_files == 0 else (processed_files / total_files) * 100
			update_progress(progress)
			
	update_progress(100)  # Ensure the progress bar reaches 100%
	completion_message_func()  # Call the completion message function
	
def verify_transfer(src, dst, file_list):
	file_list.insert(tk.END, "Verifying files...\n\n", 'verify')
	
	verification_errors = []
	
	for src_dir, dirs, files in os.walk(src):
		dst_dir = src_dir.replace(src, dst, 1)
		
		for file_ in files:
			if is_system_file(file_):
				continue  # Skip system files
			
			src_file = os.path.join(src_dir, file_)
			dst_file = os.path.join(dst_dir, file_)
			
			if not os.path.exists(dst_file):
				verification_errors.append(f"Missing file: {dst_file}")
				continue
			
			src_stat = os.stat(src_file)
			dst_stat = os.stat(dst_file)
			
			if src_stat.st_size != dst_stat.st_size or src_stat.st_mtime != dst_stat.st_mtime:
				verification_errors.append(f"File mismatch: {src_file} -> {dst_file}")
				
	return verification_errors
