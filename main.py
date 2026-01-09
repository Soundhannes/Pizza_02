import tkinter as tk
from tkinter import ttk, messagebox

class ColorDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RGB Color Display")
        self.root.geometry("400x300")
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="RGB Color Display", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # RGB input fields
        ttk.Label(main_frame, text="R:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.r_var = tk.StringVar()
        self.r_entry = ttk.Entry(main_frame, textvariable=self.r_var, width=10)
        self.r_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(main_frame, text="G:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        self.g_var = tk.StringVar()
        self.g_entry = ttk.Entry(main_frame, textvariable=self.g_var, width=10)
        self.g_entry.grid(row=2, column=1, padx=5)
        
        ttk.Label(main_frame, text="B:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5))
        self.b_var = tk.StringVar()
        self.b_entry = ttk.Entry(main_frame, textvariable=self.b_var, width=10)
        self.b_entry.grid(row=3, column=1, padx=5)
        
        # Display button
        display_button = ttk.Button(main_frame, text="Display Color", command=self.display_color)
        display_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Color display area
        self.color_frame = tk.Frame(main_frame, width=200, height=100, bg="white", relief="solid", borderwidth=2)
        self.color_frame.grid(row=5, column=0, columnspan=3, pady=10)
        self.color_frame.grid_propagate(False)
        
        # Color info label
        self.color_info = ttk.Label(main_frame, text="Enter RGB values (0-255)")
        self.color_info.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def display_color(self):
        try:
            # Get RGB values
            r = int(self.r_var.get())
            g = int(self.g_var.get())
            b = int(self.b_var.get())
            
            # Validate RGB values
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                messagebox.showerror("Error", "RGB values must be between 0 and 255")
                return
            
            # Convert to hex color
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Update color display
            self.color_frame.configure(bg=hex_color)
            
            # Update info label
            self.color_info.configure(text=f"RGB({r}, {g}, {b}) = {hex_color}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for RGB values")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorDisplayApp(root)
    root.mainloop()