
# Face Recognition Attendance System

A Python project that uses face recognition, blink-based liveness detection, and MySQL database integration for attendance tracking. This project also supports dynamic registration of unknown faces via a Tkinter GUI.

## Features

- **Face Detection & Recognition:**  
  Uses the `face_recognition` library to detect and recognize faces from a live webcam feed.
  
- **Blink-Based Liveness Detection:**  
  Prevents spoofing by detecting a blink as a sign of liveness.

- **Unknown Face Registration:**  
  When an unknown face is detected, the user is prompted via a GUI dialog (using Tkinter) to register by entering their name. The new face image is saved and added to the system for future recognition.

- **MySQL Integration:**  
  Attendance records (name, date, time) and student details (e.g., age, gender) are stored in a MySQL database.

- **GUI Interface:**  
  A Tkinter-based GUI displays the live video feed and provides controls for unknown face registration.

## Prerequisites

- **Python 3.7+**
- **MySQL Server**
- **Required Python Packages:**
  - `face_recognition`
  - `opencv-python`
  - `numpy`
  - `mysqlclient`
  - `Pillow`  
  - *(Tkinter is included with most Python installations.)*

## Installation

### 1. Clone the Repository

Open your terminal (or Git Bash) and run:

```bash
git clone https://github.com/AtharvaJahagirdar13/Attendance-using-Facial-Recognition
```

Then, change to the project directory:

```bash
cd YourRepoName
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **On Linux/Mac:**

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required packages using pip:

```bash
pip install face_recognition opencv-python numpy mysqlclient Pillow
```

*Note:* Tkinter usually comes with Python. If it's missing, install it using your package manager.

### 4. Configure MySQL Database

- Create a MySQL database (e.g., `attendance_db`).
- Update the credentials in `db_manage.py` and `student_db_manager.py` to match your MySQL settings.
- The project will automatically create the necessary tables (e.g., `attendance`, `student_details`) if they don't exist.

### 5. Prepare the Faces Folder

Ensure a folder named `faces` exists in the project directory and contains initial face images (if any) in the format `personname_image.jpg`.

## Usage

### Running the Application

To start the main application, run:

```bash
python main.py
```

This will open the webcam feed, perform face recognition, and display a window with the live video feed.

### Unknown Face Registration

- When an unknown face is detected, a message is overlaid on the video feed.
- Press **r** to trigger a GUI dialog asking for the new name.
- The new face image is saved in the `faces` folder and added to the known faces list for future recognition.

### Exiting the Application

Press **q** in the video window to quit the application.

## Contributing

Contributions are welcome! If you would like to suggest improvements, add new features, or fix bugs, please follow these steps:

1. **Fork the Repository:**  
   Click the "Fork" button on GitHub to create a copy in your account.

2. **Create a Branch:**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make Changes:**  
   Implement your changes or improvements.

4. **Commit Changes:**

   ```bash
   git add .
   git commit -m "Add feature: YourFeatureName"
   ```

5. **Push to Your Fork:**

   ```bash
   git push origin feature/YourFeatureName
   ```

6. **Submit a Pull Request:**  
   Go to the original repository on GitHub and create a new pull request describing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [face_recognition](https://github.com/ageitgey/face_recognition) for robust face detection and recognition.
- [OpenCV](https://opencv.org/) for powerful image processing.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI components.
```

Feel free to modify the repository URL, license, or any section to suit your project's specific details.
