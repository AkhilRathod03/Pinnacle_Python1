# Calendar Reminder App

A desktop application built with Python and Tkinter that allows you to manage reminders with a calendar interface.

## Features

*   **Interactive Calendar:** Easily navigate through months and years.
*   **Reminder Management:** Add, edit, and delete reminders for any date.
*   **Customizable Reminders:** Set a title, description, and specific time for each reminder.
*   **Repeating Reminders:** Configure reminders to repeat daily, weekly, or monthly.
*   **Desktop Notifications:** Receive desktop notifications when a reminder is due.
*   **Modern UI:** A clean and modern user interface thanks to the `ttkbootstrap` library.

## Technologies Used

*   **Python:** The core programming language.
*   **Tkinter:** For the graphical user interface (GUI).
*   **ttkbootstrap:** To create a modern look and feel for the Tkinter UI.
*   **playsound:** To play a sound with the reminder notification.
*   **plyer:** To display desktop notifications.

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd CalendarReminderApp
    ```

2.  **Install the dependencies:**
    Make sure you have Python installed. Then, install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

## File Structure

*   `main.py`: The main entry point of the application.
*   `calendar_ui.py`: Contains the `CalendarApp` class, which builds and manages the user interface.
*   `reminder_manager.py`: Handles the logic for loading, saving, and managing reminders.
*   `notification.py`: Manages the reminder notifications.
*   `data.json`: The JSON file where all the reminder data is stored.
*   `requirements.txt`: A list of the Python dependencies required to run the application.
*   `assets/`: A directory for storing application assets (like icons or sound files).
