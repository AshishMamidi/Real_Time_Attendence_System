# Real_Time_Attendence_System

A real-time attendance system using Python typically involves capturing and processing real-time attendance data, utilizing various technologies such as biometrics, RFID (Radio Frequency Identification) or facial recognition.
## Real-Time Attendance System using OpenCV and Google Firebase

This application is a real-time attendance system developed using Python and various libraries such as OpenCV, Google Firebase, and more. The system allows for live attendance marking by capturing images through a camera, generating facial encodings, and updating the attendance records in a Firebase database.

### Features

- Real-time attendance marking: The application captures live images using OpenCV and processes them to recognize faces using the face_recognition library. Facial encodings are generated and compared to the existing encodings in the database for identification.

- Firebase integration: The attendance records are updated and stored in Google Firebase, a cloud-based NoSQL database. This ensures seamless synchronization and accessibility of attendance data from different devices or platforms.

- Image encodings: The face_recognition library is utilized to generate facial encodings for each individual. These encodings are stored in a pickle file and used for subsequent identification during attendance marking.

- Timestamps and date tracking: The application uses the datetime library to record timestamps and track attendance dates. Each attendance entry is associated with the corresponding date and time for accurate record-keeping.

- User-friendly interface: The application utilizes the cvzone library to create an intuitive and interactive user interface. The interface displays the live camera feed, recognized faces, and attendance status in real time.

### Requirements

- Python 3.x
- OpenCV
- Firebase Admin SDK
- face_recognition
- numpy
- cvzone
- datetime
- more in the requirements.txt

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/your-repo.git
   ```

2. Install the required dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

3. Set up Firebase credentials:
   - Create a Firebase project and obtain the credentials.
   - Place the Firebase credentials JSON file in the project directory.

4. Upload the images in the images folder along with the names of the student.
   - Goto images folder and paste the student images along with their names.

5. Run the application:
   ```
   python main.py
   ```

### Usage

1. Launch the application by running the `main.py` file.

2. The application will start the camera feed and display recognized faces.

3. As faces are detected, the application matches them with the stored encodings and updates the attendance records in real time.

4. The attendance data is synchronized with the Google Firebase database for easy access and management.

5. Press `Q` to quit the application.

### Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.

2. Create a new branch:
   ```
   git checkout -b feature/your-feature
   ```

3. Make your changes and commit them:
   ```
   git commit -m "Add your commit message"
   ```

4. Push to the branch:
   ```
   git push origin feature/your-feature
   ```

5. Open a pull request on GitHub.

### Contact

If you have any questions or suggestions, feel free to reach out to [kumarashish96690@gmail.com](mailto:kumarashish96690@gmail.com).

HAPPY CODING 😁
