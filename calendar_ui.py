
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import calendar
from datetime import datetime, timedelta
from reminder_manager import ReminderManager
from notification import play_sound
import threading
import time

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar and Reminder App")
        self.root.geometry("1200x800")
        self.style = tb.Style(theme="superhero")

        self.reminder_manager = ReminderManager('C:\\Users\\VASANTH RAO\\Desktop\\CalendarReminderApp\\data.json')

        self.year = datetime.now().year
        self.month = datetime.now().month
        self.selected_date = None

        self.notified_reminders = set()
        self.last_check_date = datetime.now().date()

        self.create_widgets()
        self.update_calendar()

        self.check_reminders_thread = threading.Thread(target=self.check_reminders_loop, daemon=True)
        self.check_reminders_thread.start()

    def create_widgets(self):
        main_frame = tb.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        left_frame = tb.Frame(main_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

        right_frame = tb.Frame(main_frame)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

        # --- Calendar Frame ---
        calendar_frame = tb.Labelframe(left_frame, text="Calendar", bootstyle=PRIMARY)
        calendar_frame.pack(fill=BOTH, expand=True)

        nav_frame = tb.Frame(calendar_frame)
        nav_frame.pack(pady=10)

        tb.Button(nav_frame, text="<<", command=lambda: self.change_year(-1)).pack(side=LEFT, padx=5)
        tb.Button(nav_frame, text="<", command=lambda: self.change_month(-1)).pack(side=LEFT, padx=5)
        self.month_year_label = tb.Label(nav_frame, text="", font=("Helvetica", 14, "bold"))
        self.month_year_label.pack(side=LEFT, padx=10)
        tb.Button(nav_frame, text=">", command=lambda: self.change_month(1)).pack(side=LEFT, padx=5)
        tb.Button(nav_frame, text=">>", command=lambda: self.change_year(1)).pack(side=LEFT, padx=5)

        self.calendar_grid = tb.Frame(calendar_frame)
        self.calendar_grid.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # --- Reminder Form Frame ---
        form_frame = tb.Labelframe(left_frame, text="Manage Reminder", bootstyle=INFO)
        form_frame.pack(fill=X, pady=20)

        tb.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.title_entry = tb.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=EW)

        tb.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.desc_entry = tb.Entry(form_frame, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=EW)

        tb.Label(form_frame, text="Time (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.time_entry = tb.Entry(form_frame, width=10)
        self.time_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)
        self.ampm_var = tk.StringVar(value="AM")
        tb.Combobox(form_frame, textvariable=self.ampm_var, values=["AM", "PM"], width=5).grid(row=2, column=2, padx=5, pady=5, sticky=W)

        tb.Label(form_frame, text="Repeat:").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.repeat_var = tk.StringVar(value="None")
        tb.Combobox(form_frame, textvariable=self.repeat_var, values=["None", "Daily", "Weekly", "Monthly"], width=10).grid(row=3, column=1, padx=5, pady=5, sticky=W)

        button_frame = tb.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)
        tb.Button(button_frame, text="Add Reminder", command=self.add_reminder, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        self.save_button = tb.Button(button_frame, text="Save Changes", command=self.save_reminder, bootstyle=PRIMARY, state=DISABLED)
        self.save_button.pack(side=LEFT, padx=5)
        self.delete_button = tb.Button(button_frame, text="Delete Reminder", command=self.delete_reminder, bootstyle=DANGER, state=DISABLED)
        self.delete_button.pack(side=LEFT, padx=5)
        self.clear_button = tb.Button(button_frame, text="Clear Form", command=self.clear_form, bootstyle=SECONDARY)
        self.clear_button.pack(side=LEFT, padx=5)
        
        danger_button_frame = tb.Frame(form_frame)
        danger_button_frame.grid(row=5, column=0, columnspan=4, pady=10)
        tb.Button(danger_button_frame, text="Clear All On Date", command=self.clear_all_on_date, bootstyle=DANGER).pack(side=LEFT, padx=5)


        # --- Reminders List Frame ---
        reminders_frame = tb.Labelframe(right_frame, text="Reminders for Selected Date", bootstyle=SUCCESS)
        reminders_frame.pack(fill=BOTH, expand=True)

        self.reminders_tree = tb.Treeview(reminders_frame, columns=("time", "title", "repeat"), show="headings", bootstyle=PRIMARY)
        self.reminders_tree.heading("time", text="Time")
        self.reminders_tree.heading("title", text="Title")
        self.reminders_tree.heading("repeat", text="Repeat")
        self.reminders_tree.column("time", width=100, anchor=CENTER)
        self.reminders_tree.column("title", width=200)
        self.reminders_tree.column("repeat", width=100, anchor=CENTER)
        self.reminders_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.reminders_tree.bind("<<TreeviewSelect>>", self.on_reminder_select)

    def update_calendar(self):
        for widget in self.calendar_grid.winfo_children():
            widget.destroy()

        self.month_year_label.config(text=f"{calendar.month_name[self.month]} {self.year}")

        cal = calendar.monthcalendar(self.year, self.month)
        today = datetime.now()

        # Day headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tb.Label(self.calendar_grid, text=day, font=("Helvetica", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)

        for r, week in enumerate(cal, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    continue
                
                date_str = f"{self.year}-{self.month:02d}-{day:02d}"
                btn_style = SECONDARY
                if self.year == today.year and self.month == today.month and day == today.day:
                    btn_style = PRIMARY # Today's date
                
                reminders = self.reminder_manager.get_reminders_for_date(date_str)
                if reminders:
                    btn_style = SUCCESS if btn_style != PRIMARY else PRIMARY
                
                day_button = tb.Button(self.calendar_grid, text=str(day), bootstyle=btn_style,
                                       command=lambda d=day: self.select_date(d))
                day_button.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

        for i in range(7):
            self.calendar_grid.grid_columnconfigure(i, weight=1)
        for i in range(len(cal) + 1):
            self.calendar_grid.grid_rowconfigure(i, weight=1)

    def select_date(self, day):
        self.selected_date = f"{self.year}-{self.month:02d}-{day:02d}"
        self.update_reminders_list()
        self.clear_form()

    def change_month(self, delta):
        self.month += delta
        if self.month > 12:
            self.month = 1
            self.year += 1
        elif self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_calendar()

    def change_year(self, delta):
        self.year += delta
        self.update_calendar()

    def update_reminders_list(self):
        for item in self.reminders_tree.get_children():
            self.reminders_tree.delete(item)
        
        if self.selected_date:
            reminders = self.reminder_manager.get_reminders_for_date(self.selected_date)
            for i, reminder in enumerate(reminders):
                self.reminders_tree.insert("", END, iid=i, values=(reminder['time'], reminder['title'], reminder['repeat']))

    def add_reminder(self):
        if not self.selected_date:
            messagebox.showwarning("No Date Selected", "Please select a date from the calendar first.")
            return

        title = self.title_entry.get()
        desc = self.desc_entry.get()
        time_str = self.time_entry.get()
        ampm = self.ampm_var.get()
        repeat = self.repeat_var.get()

        if not title or not time_str:
            messagebox.showwarning("Missing Information", "Title and time are required.")
            return
        
        try:
            datetime.strptime(f"{time_str} {ampm}", "%I:%M %p")
        except ValueError:
            messagebox.showwarning("Invalid Time", "Please enter time in HH:MM format.")
            return

        reminder = {
            "title": title,
            "description": desc,
            "time": f"{time_str} {ampm}",
            "repeat": repeat
        }
        self.reminder_manager.add_reminder(self.selected_date, reminder)
        self.update_reminders_list()
        self.update_calendar()
        self.clear_form()

    def on_reminder_select(self, event):
        selected_items = self.reminders_tree.selection()
        if not selected_items:
            return

        self.clear_form()
        item_iid = selected_items[0]
        index = int(item_iid)
        
        reminders = self.reminder_manager.get_reminders_for_date(self.selected_date)
        if 0 <= index < len(reminders):
            reminder = reminders[index]
            self.title_entry.insert(0, reminder['title'])
            self.desc_entry.insert(0, reminder['description'])
            time_parts = reminder['time'].split()
            self.time_entry.insert(0, time_parts[0])
            self.ampm_var.set(time_parts[1])
            self.repeat_var.set(reminder['repeat'])

            self.save_button.config(state=NORMAL)
            self.delete_button.config(state=NORMAL)

    def save_reminder(self):
        selected_items = self.reminders_tree.selection()
        if not selected_items or not self.selected_date:
            return

        index = int(selected_items[0])
        
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        time_str = self.time_entry.get()
        ampm = self.ampm_var.get()
        repeat = self.repeat_var.get()

        if not title or not time_str:
            messagebox.showwarning("Missing Information", "Title and time are required.")
            return

        updated_reminder = {
            "title": title,
            "description": desc,
            "time": f"{time_str} {ampm}",
            "repeat": repeat
        }
        self.reminder_manager.update_reminder(self.selected_date, index, updated_reminder)
        self.update_reminders_list()
        self.clear_form()

    def delete_reminder(self):
        if self.selected_reminder_index is None or not self.selected_date:
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reminder?"):
            try:
                self.reminder_manager.delete_reminder(self.selected_date, self.selected_reminder_index)
                self.update_reminders_list()
                self.update_calendar()
                self.clear_form()
            except (ValueError, IndexError) as e:
                messagebox.showerror("Error", f"Could not delete reminder: {e}")

    def clear_all_on_date(self):
        if not self.selected_date:
            messagebox.showwarning("No Date Selected", "Please select a date to clear.")
            return
        
        if messagebox.askyesno("Confirm Clear All", f"Are you sure you want to delete ALL reminders for {self.selected_date}?"):
            self.reminder_manager.delete_all_for_date(self.selected_date)
            self.update_reminders_list()
            self.update_calendar()
            self.clear_form()

    def clear_form(self):
        self.title_entry.delete(0, END)
        self.desc_entry.delete(0, END)
        self.set_default_time()
        self.repeat_var.set("None")
        self.save_button.config(state=DISABLED)
        self.delete_button.config(state=DISABLED)
        if self.reminders_tree.selection():
            self.reminders_tree.selection_remove(self.reminders_tree.selection())

    def set_default_time(self):
        now = datetime.now()
        time_str = now.strftime("%I:%M")
        ampm_str = now.strftime("%p")
        self.time_entry.delete(0, END)
        self.time_entry.insert(0, time_str)
        self.ampm_var.set(ampm_str)

    def show_tkinter_notification(self, title, message):
        notification_window = tb.Toplevel(self.root)
        notification_window.title("Reminder!")
        notification_window.resizable(False, False)
        
        # Position window at the bottom right
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - 360
        y = screen_height - 200
        notification_window.geometry(f"350x150+{x}+{y}")

        notification_window.attributes("-topmost", True)
        
        main_frame = tb.Frame(notification_window, padding=15)
        main_frame.pack(fill=BOTH, expand=True)

        title_label = tb.Label(main_frame, text=title, font=("Helvetica", 12, "bold"), bootstyle=INVERSE + PRIMARY)
        title_label.pack(pady=(0, 5), fill=X)
        
        message_label = tb.Label(main_frame, text=message, wraplength=320)
        message_label.pack(pady=5, fill=X)

        # Auto-close the window after 10 seconds
        notification_window.after(10000, notification_window.destroy)
        
        # Close on click
        notification_window.bind("<Button-1>", lambda e: notification_window.destroy())
        title_label.bind("<Button-1>", lambda e: notification_window.destroy())
        message_label.bind("<Button-1>", lambda e: notification_window.destroy())

        play_sound()


    def check_reminders_loop(self):
        while True:
            now = datetime.now()
            
            if now.date() > self.last_check_date:
                self.notified_reminders.clear()
                self.last_check_date = now.date()

            all_reminders = self.reminder_manager.get_all_reminders()
            for date_str, reminders in all_reminders.items():
                for i, reminder in enumerate(reminders):
                    # Use a unique ID that includes the date for repeating reminders
                    today_id = (now.strftime('%Y-%m-%d'), date_str, i)
                    original_id = (date_str, i)

                    if today_id in self.notified_reminders or (reminder['repeat'] == 'None' and original_id in self.notified_reminders):
                        continue

                    try:
                        reminder_time_obj = datetime.strptime(reminder['time'], "%I:%M %p").time()
                    except ValueError:
                        continue

                    reminder_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    
                    should_notify = False
                    reminder_datetime = datetime.combine(now.date(), reminder_time_obj)

                    if reminder['repeat'] == 'None':
                        if reminder_date == now.date() and reminder_datetime <= now:
                            should_notify = True
                    elif reminder['repeat'] == 'Daily':
                        if reminder_datetime <= now:
                            should_notify = True
                    elif reminder['repeat'] == 'Weekly':
                        if reminder_date.weekday() == now.weekday() and reminder_datetime <= now:
                            should_notify = True
                    elif reminder['repeat'] == 'Monthly':
                        if reminder_date.day == now.day and reminder_datetime <= now:
                            should_notify = True
                    
                    if should_notify:
                        self.root.after(0, self.show_tkinter_notification, f"Reminder: {reminder['title']}", reminder['description'])
                        
                        if reminder['repeat'] == 'None':
                            self.notified_reminders.add(original_id)
                        else:
                            self.notified_reminders.add(today_id)

            time.sleep(1)
