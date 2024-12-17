import tkinter as tk
from tkinter import Menu, simpledialog
from PIL import Image, ImageTk
import os
import database
from path_utils import get_path_and_distances, scale_coordinates
from datetime import datetime

class MiddleEarthTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Middle-earth Walking Tracker")

        self.conn = database.create_connection('middle_earth_tracker.db')
        database.create_tables(self.conn)

        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_progress)
        file_menu.add_command(label="Load", command=self.load_progress)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.close_application)


        options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Reset Progress", command=self.reset_progress)

        self.original_size = (1600, 900)
        self.new_size = (1600, 900)
        self.image_scale = 1.0

        self.path, self.distances = get_path_and_distances()
        self.total_distance = 0
        self.max_distance = sum(self.distances)
        self.scaled_path = scale_coordinates(self.path, self.original_size, self.new_size)

        self.canvas = tk.Canvas(self.root, width=self.new_size[0], height=self.new_size[1], bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        image_path = "map-of-mearth.jpeg"
        if os.path.exists(image_path):
            self.original_image = Image.open(image_path)
            self.display_image = self.original_image.copy()
            self.tk_image = ImageTk.PhotoImage(self.display_image)
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        else:
            print(f"Error: Image file '{image_path}' not found. Ensure the file is in the correct directory.")

        self.draw_full_path()
        self.mark_locations()

        input_frame = tk.Frame(self.root, bg="white", height=100)
        input_frame.pack(side=tk.BOTTOM, pady=0, fill=tk.X)

        self.distance_label = tk.Label(input_frame, text="Enter distance in miles:", bg="white")
        self.distance_label.pack(side=tk.LEFT, padx=10)

        self.distance_entry = tk.Entry(input_frame, bg="white")
        self.distance_entry.pack(side=tk.LEFT, padx=10)

        self.submit_button = tk.Button(input_frame, text="Submit Distance", command=self.submit_distance, bg="white", width=15, height=2)
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(input_frame, text="Reset", command=self.reset_progress, bg="white", width=15, height=2)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.total_distance_label = tk.Label(input_frame, text="Total Distance: 0 miles", bg="white")
        self.total_distance_label.pack(side=tk.LEFT, padx=10)

        self.distance_to_next_label = tk.Label(input_frame, text="Distance to Next Location: 100 miles", bg="white")
        self.distance_to_next_label.pack(side=tk.LEFT, padx=10)

        status_frame = tk.Frame(self.root, bg="white")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5, expand=True)

        self.current_user_label = tk.Label(status_frame, text="Current User: None", bg="white")
        self.current_user_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.last_entry_label = tk.Label(status_frame, text="Date of Last Entry: N/A", bg="white")
        self.last_entry_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.date_time_label = tk.Label(status_frame, text="", bg="white")
        self.date_time_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")
        self.update_time()

        self.elapsed_days_label = tk.Label(status_frame, text="Days Elapsed: 0", bg="white")
        self.elapsed_days_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="center")

        self.coord_label = tk.Label(status_frame, text="Coordinates: (0, 0)", bg="white")
        self.coord_label.pack(side=tk.RIGHT, padx=10, pady=5, anchor="e")

        self.root.update()

        self.canvas.bind("<Motion>", self.display_coordinates)

        self.bind_keyboard_zoom()
        self.bind_mouse_wheel()

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        self.reset_counter = 0
        self.last_location_index = -1

        self.start_date = None  # Initialize start_date to None
        self.update_elapsed_days()  # Start updating the elapsed days

        # Bind the window close event to the close_application method
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    def draw_full_path(self):
        scaled_path = scale_coordinates(self.path, self.original_size, self.new_size)
        for i in range(len(scaled_path) - 1):
            x1, y1 = scaled_path[i]
            x2, y2 = scaled_path[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2, dash=(2, 2), tags="path")

    def mark_locations(self):
        scaled_path = scale_coordinates(self.path, self.original_size, self.new_size)
        for x, y in scaled_path:
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="yellow", outline="black", tags="location")

    def on_button_press(self, event):
        """Handle the initial mouse button press for starting a drag."""
        self.canvas.scan_mark(event.x, event.y)

    def on_mouse_drag(self, event):
        """Handle the mouse drag motion."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def bind_keyboard_zoom(self):
        """Bind keyboard keys for zooming in and out."""
        self.root.bind("<Up>", self.zoom_in)
        self.root.bind("<Down>", self.zoom_out)

    def bind_mouse_wheel(self):
        """Bind mouse wheel events for different operating systems."""
        self.canvas.bind("<MouseWheel>", self.zoom_image)  # Windows
        self.canvas.bind("<Button-4>", self.zoom_in)       # Linux scroll up
        self.canvas.bind("<Button-5>", self.zoom_out)      # Linux scroll down

    def zoom_image(self, event):
        if event.delta > 0:
            self.zoom_in(event)
        elif event.delta < 0:
            self.zoom_out(event)

    def zoom_in(self, event=None):
        """Zoom in on the image."""
        print("Zooming in")
        self.image_scale *= 1.1
        self.apply_zoom()

    def zoom_out(self, event=None):
        """Zoom out of the image."""
        print("Zooming out")
        self.image_scale /= 1.1
        self.apply_zoom()

    def apply_zoom(self):
        """Apply the zoom effect on the image."""
        print(f"Image scale: {self.image_scale}")
        width = int(self.original_image.width * self.image_scale)
        height = int(self.original_image.height * self.image_scale)
        self.display_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(self.display_image)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.image_id, image=self.tk_image)

        # Update the path and location points
        self.update_path_and_locations()

        # Update the progress line to match the new zoom level
        self.update_progress_line()

    def update_path_and_locations(self):
        """Update the positions of the path and location markers based on the zoom level."""
        self.canvas.delete("path", "location", "progress")
        scaled_path = [(int(x * self.image_scale), int(y * self.image_scale)) for x, y in self.path]

        # Draw the scaled path with a gray line
        for i in range(len(scaled_path) - 1):
            x1, y1 = scaled_path[i]
            x2, y2 = scaled_path[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2, dash=(2, 2), tags="path")

        # Mark the scaled locations
        distance_covered = 0
        for i, (x, y) in enumerate(scaled_path):
            if self.total_distance >= distance_covered:
                color = "yellow"
            else:
                color = "gray"
            self.canvas.create_oval
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline="black", tags=("location", f"location_{i}"))
            distance_covered += self.distances[i] if i < len(self.distances) else 0

        # Update the progress line
        self.update_progress_line(scaled_path)

    def update_progress_line(self, scaled_path=None):
        """Update the progress line based on the total distance covered."""
        self.canvas.delete("progress")
        if self.total_distance == 0:
            return
        if scaled_path is None:
            scaled_path = [(int(x * self.image_scale), int(y * self.image_scale)) for x, y in self.path]

        distance_covered = 0
        for i, dist in enumerate(self.distances):
            if self.total_distance > distance_covered + dist:
                x1, y1 = scaled_path[i]
                x2, y2 = scaled_path[i + 1]
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=4, tags="progress")
                distance_covered += dist
            else:
                x1, y1 = scaled_path[i]
                ratio = (self.total_distance - distance_covered) / dist
                x2 = x1 + ratio * (scaled_path[i + 1][0] - x1)
                y2 = y1 + ratio * (scaled_path[i + 1][1] - y1)
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=4, tags="progress")
                break

    def display_coordinates(self, event):
        """Display the coordinates of the mouse pointer on the canvas."""
        x, y = event.x, event.y
        self.coord_label.config(text=f"Coordinates: ({x}, {y})")

    def submit_distance(self):
        """Update the total distance and check if a new location is reached."""
        entered_text = self.distance_entry.get()
        if not entered_text.strip():
            return
        try:
            distance = float(entered_text)
            self.last_distance_added = distance  # Track the last distance added
            self.total_distance += distance
            self.total_distance_label.config(text=f"Total Distance: {self.total_distance:.2f} miles")
            self.check_next_location()
            self.update_progress_line()
            self.update_path_and_locations()
            self.distance_entry.delete(0, tk.END)
            # Update the last location index
            distance_covered = 0
            for i, dist in enumerate(self.distances):
                distance_covered += dist
                if self.total_distance >= distance_covered:
                    self.last_location_index = i
                else:
                    break
        except ValueError:
            self.distance_entry.delete(0, tk.END)  # Clear the entry field if invalid

    def check_next_location(self):
        """Check if the total distance reaches the next key location."""
        distance_covered = 0
        for i, dist in enumerate(self.distances):
            distance_covered += dist
            if self.total_distance < distance_covered:
                next_distance = distance_covered - self.total_distance
                self.distance_to_next_label.config(text=f"Distance to Next Location: {next_distance:.2f} miles")
                return
        self.distance_to_next_label.config(text="Journey Completed!")

    def reset_progress(self):
        """Handle the reset progress logic based on the number of clicks."""
        self.reset_counter += 1

        if self.reset_counter == 1:
            # Reset the most recent distance entry
            self.total_distance -= self.last_distance_added
            self.update_progress_line()
            self.update_path_and_locations()
            self.total_distance_label.config(text=f"Total Distance: {self.total_distance:.2f} miles")
            self.check_next_location()
        elif self.reset_counter == 2:
            # Reset to the last location
            if self.last_location_index >= 0:
                self.total_distance = sum(self.distances[:self.last_location_index + 1])
                self.update_progress_line()
                self.update_path_and_locations()
                self.total_distance_label.config(text=f"Total Distance: {self.total_distance:.2f} miles")
                self.check_next_location()
            else:
                print("No location to reset to.")
        elif self.reset_counter == 3:
            # Reset progress entirely
            self.total_distance = 0
            self.update_progress_line()
            self.update_path_and_locations()
            self.total_distance_label.config(text="Total Distance: 0 miles")
            self.distance_to_next_label.config(text=f"Distance to Next Location: {self.distances[0]:.2f} miles")
            self.reset_counter = 0

        # Log the reset operation (for debugging)
        print(f"Reset operation: {self.reset_counter}")

    def save_progress(self):
        """Save the current progress to the database."""
        if not hasattr(self, 'current_user'):
            self.current_user = simpledialog.askstring("Save Progress", "Enter user name:")
            if self.current_user:
                self.start_date = datetime.now()  # Set the start date if not set
        if self.current_user:
            user_id = database.get_user_id(self.conn, self.current_user)
            if user_id is None:
                print(f"Adding new user: {self.current_user}")
                user_id = database.add_user(self.conn, self.current_user, str(self.total_distance))
                self.start_date = datetime.now()  # Set the start date
            else:
                print(f"User found: {self.current_user} with user_id: {user_id}")
                database.save_progress(self.conn, user_id, str(self.total_distance))
                # Load the start date and last entry date from the database if they exist
                start_date_str, last_entry_date = database.load_start_and_last_entry_dates(self.conn, user_id)
                if start_date_str:
                    self.start_date = datetime.strptime(start_date_str, "%m/%d/%Y %H:%M")
                if last_entry_date:
                    self.last_entry_label.config(text=f"Date of Last Entry: {last_entry_date}")
            self.display_current_user()

    def load_progress(self):
        """Load the progress from the database."""
        users = database.get_all_users(self.conn)
        if users:
            self.show_user_selection_dialog(users)
        else:
            print("No users found.")

    def show_user_selection_dialog(self, users):
        """Show a dialog to select the user from a list."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Load Progress")

        tk.Label(dialog, text="Select user name:").pack(side=tk.TOP, fill=tk.X, pady=10)

        listbox = tk.Listbox(dialog, selectmode=tk.SINGLE)
        for user in users:
            listbox.insert(tk.END, user)
        listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)

        def on_select():
            selection = listbox.curselection()
            if selection:
                user = listbox.get(selection[0])
                self.current_user = str(user)  # Ensure user is a string
                print(f"Selected user: {self.current_user}")
                user_id = database.get_user_id(self.conn, self.current_user)  # Pass self.current_user to the query
                if user_id is not None:
                    print(f"User ID for {self.current_user}: {user_id}")
                    progress = database.load_progress(self.conn, user_id)
                    if progress:
                        print(f"Progress loaded for user_id {user_id}: {progress}")
                        self.total_distance = float(progress[0])  # Load the progress data
                        self.total_distance_label.config(text=f"Total Distance: {self.total_distance:.2f} miles")
                        self.update_progress_line()
                        self.update_path_and_locations()
                        self.check_next_location()
                        self.display_current_user()

                        # Load the start date and last entry date
                        start_date_str, last_entry_date = database.load_start_and_last_entry_dates(self.conn, user_id)
                        if start_date_str:
                            self.start_date = datetime.strptime(start_date_str, "%m/%d/%Y %H:%M")
                        if last_entry_date:
                            self.last_entry_label.config(text=f"Date of Last Entry: {last_entry_date}")
                        self.update_elapsed_days()
                    else:
                        print("No progress found for the specified user.")
                else:
                    print("User not found.")
            dialog.destroy()

        tk.Button(dialog, text="Load", command=on_select).pack(side=tk.BOTTOM, pady=10)

    def display_current_user(self):
        """Display the current user in the UI."""
        if hasattr(self, 'current_user'):
            self.current_user_label.config(text=f"Current User: {self.current_user}")

    def update_elapsed_days(self):
        """Update the days elapsed since the start date."""
        if self.start_date:
            now = datetime.now()
            elapsed_days = (now - self.start_date).days
            self.elapsed_days_label.config(text=f"Days Elapsed: {elapsed_days}")
        self.root.after(86400000, self.update_elapsed_days)  # Update every day

    def show_about(self):
        """Show the about dialog."""
        pass  # Implement the FAQ/About dialog here

    def close_connection(self):
        """Close the SQLite connection."""
        self.conn.close()

    def close_application(self):
        """Close the application and SQLite connection."""
        self.close_connection()
        self.root.destroy()

    def update_time(self):
        """Update the date and time on the label."""
        now = datetime.now().strftime("%m/%d/%Y %H:%M")
        self.date_time_label.config(text=f"Current Date and Time: {now}")
        self.root.after(1000, self.update_time)  # Update the time every second

if __name__ == "__main__":
    root = tk.Tk()
    app = MiddleEarthTracker(root)
    root.protocol("WM_DELETE_WINDOW", app.close_application)
    root.mainloop()
