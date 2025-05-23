#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
from datetime import datetime
import sys
from pheonix import calculate_hash, recover_file, find_and_recover, setup_logging

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

class PhoenixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Phoenix Data Recovery Tool")
        self.root.geometry("900x700")
        
        # Configure dark theme colors
        style = ttk.Style()
        style.configure(".", background="#2E2E2E", foreground="white")
        style.configure("TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="white")
        style.configure("TButton", background="#404040", foreground="white", padding=5)
        style.configure("TLabelframe", background="#2E2E2E", foreground="white")
        style.configure("TLabelframe.Label", background="#2E2E2E", foreground="white")
        style.configure("TCheckbutton", background="#2E2E2E", foreground="white")
        
        # Configure root window
        self.root.configure(bg="#2E2E2E")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Phoenix Data Recovery", font=("Helvetica", 24))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Directory selection
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(1, weight=1)
        
        ttk.Label(dir_frame, text="Original Directory:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.original_dir = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.original_dir, width=50).grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(dir_frame, text="Browse", command=lambda: self.browse_directory(self.original_dir)).grid(row=0, column=2)

        ttk.Label(dir_frame, text="Backup Directory:", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.backup_dir = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.backup_dir, width=50).grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(dir_frame, text="Browse", command=lambda: self.browse_directory(self.backup_dir)).grid(row=1, column=2)

        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        self.dry_run = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Dry Run (Simulate recovery)", variable=self.dry_run).grid(row=0, column=0, padx=20)
        
        self.debug_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Debug Mode", variable=self.debug_mode).grid(row=0, column=1, padx=20)

        # Action buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        start_btn = ttk.Button(buttons_frame, text="Start Recovery", command=self.start_recovery, style="Accent.TButton")
        start_btn.pack(side=tk.LEFT, padx=10)
        
        list_btn = ttk.Button(buttons_frame, text="List Backup Files", command=self.list_backups)
        list_btn.pack(side=tk.LEFT, padx=10)

        # Progress
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var, font=("Helvetica", 10))
        progress_label.grid(row=4, column=0, columnspan=3, pady=(10, 5))

        # Output text area with custom styling
        self.output_text = scrolledtext.ScrolledText(
            main_frame, 
            height=15,
            bg="#1E1E1E",
            fg="#FFFFFF",
            font=("Courier", 10)
        )
        self.output_text.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))

        # Redirect stdout to our text widget
        sys.stdout = RedirectText(self.output_text)

    def browse_directory(self, string_var):
        directory = filedialog.askdirectory()
        if directory:
            string_var.set(directory)

    def start_recovery(self):
        if not self.original_dir.get() or not self.backup_dir.get():
            self.progress_var.set("⚠️ Please select both directories first!")
            return

        self.output_text.delete(1.0, tk.END)
        self.progress_var.set("🔄 Recovery in progress...")
        
        # Setup logging
        setup_logging(self.debug_mode.get())
        
        def recovery_thread():
            try:
                find_and_recover(self.original_dir.get(), self.backup_dir.get(), self.dry_run.get())
                self.progress_var.set("✅ Recovery completed!")
            except Exception as e:
                self.progress_var.set(f"❌ Error: {str(e)}")

        threading.Thread(target=recovery_thread, daemon=True).start()

    def list_backups(self):
        if not self.backup_dir.get():
            self.progress_var.set("⚠️ Please select backup directory first!")
            return

        self.output_text.delete(1.0, tk.END)
        self.progress_var.set("🔍 Listing backup files...")
        
        def list_thread():
            try:
                for root, _, files in os.walk(self.backup_dir.get()):
                    for file in files:
                        full_path = os.path.join(root, file)
                        print(f"📄 {full_path}")
                self.progress_var.set("✅ Backup files listed!")
            except Exception as e:
                self.progress_var.set(f"❌ Error: {str(e)}")

        threading.Thread(target=list_thread, daemon=True).start()

def main():
    root = tk.Tk()
    app = PhoenixGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 