import tkinter as tk
from screeninfo import get_monitors

def scan_monitor_windows():
  root = tk.Tk()
  root.withdraw()  # Hide the root window

  monitors = get_monitors()
  windows = []

  for i, monitor in enumerate(monitors):
      window = tk.Toplevel(root)
      window.title(f"Monitor {i}")
      window.geometry(f"200x100+{monitor.x}+{monitor.y}")
      label = tk.Label(window, text=f"INDEX {i}", font=("Helvetica", 24))
      label.pack(expand=True)
      note_label = tk.Label(window, text="Use ESC key to EXIT", font=("Helvetica", 12))
      note_label.pack(expand=True)
      windows.append(window)

  def on_key(event):
    if event.keysym == 'Escape':
      root.destroy()

  root.bind_all('<Key>', on_key)
  root.mainloop()
