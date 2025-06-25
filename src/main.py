# Local Development Imports
# from dotenv import load_dotenv
# load_dotenv()
# Importing the Environment Variables
import sys
import os
CLASSES_ID = os.getenv("NOTION_DB_ID_classes")
INSTRUCTORS_ID = os.getenv("NOTION_DB_ID_instructors")
STUDENTS_ID = os.getenv("NOTION_DB_ID_students")

DEBUG = "debug" in sys.argv
if DEBUG:
    DEBUG = True if DEBUG=="True" else False
else:
    DEBUG = True

from notion_utils import get_database
from time_utils import get_current_time
from whatsapp_utils import send_whatsapp_message, prepare_message

if DEBUG:
    print("CLASSES_ID:", CLASSES_ID)
    print("INSTRUCTORS_ID:", INSTRUCTORS_ID)
    print("STUDENTS_ID:", STUDENTS_ID)

def main():
    # Fetch the Classes Database
    classes = get_database(CLASSES_ID)
    for class_row in classes["results"]:
        class_name = class_row["properties"]["Name"]["title"][0]["plain_text"]
        day_name = class_row["properties"]["Day"]["select"]["name"]
        start_time = class_row["properties"]["Start Time"]["rich_text"][0]["plain_text"]
        curr_time, curr_day = get_current_time()
        if DEBUG:
            print("Class Details:", class_name, day_name, start_time, "Current Details:", curr_time, curr_day)
        if not (curr_time == start_time and curr_day == day_name):
            if DEBUG:
                print("Skipping Class:",class_name)
            continue
        # Fetch the Instructors Database
        instructors = get_database(INSTRUCTORS_ID)
        instructors_details = []
        for instructor in instructors["results"]:
            for class_instructor in class_row["properties"]["Instructor"]["relation"]:
                if instructor["id"] == class_instructor["id"]:
                    instuctor_name = instructor["properties"]["Name"]["title"][0]["plain_text"]
                    instructor_contact = instructor["properties"]["Contact"]["phone_number"]
                    instructors_details.append((instuctor_name, instructor_contact))
                    if DEBUG:
                        print("Instructor Name: ", instuctor_name, "and Contact: ", instructor_contact)
        # Fetch the Students Database
        students = get_database(STUDENTS_ID)
        student_details = []
        for student in students["results"]:
            for class_student in class_row["properties"]["Students"]["relation"]:
                if student["id"] == class_student["id"]:
                    student_name = student["properties"]["Name"]["title"][0]["plain_text"]
                    student_contact = student["properties"]["Contact"]["phone_number"]
                    student_details.append((student_name, student_contact))
                    if DEBUG:
                        print("Student Name: ", student_name, "and Contact: ", student_contact)
        # Send WhatsApp Message
        if DEBUG:
            print("Instructors: ", instructors_details)
            print("Students: ", student_details)
        for name, contact in instructors_details:
            student_names = [student[0] for student in student_details]
            message = prepare_message(name, day_name, start_time, student_names, "instructor")
            if DEBUG:
                print(message, contact)
            send_whatsapp_message(message, contact)
        for name, contact in student_details:
            instructors_names = [instructor[0] for instructor in instructors_details]
            message = prepare_message(name, day_name, start_time, instructors_names, "student")
            # send_whatsapp_message(message, contact)


if __name__ == "__main__":
    main()
