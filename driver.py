from getpass import getpass
from mysql.connector import connect, Error

def validateCourse(cursor, courseNum=-1, department=""):
    if(courseNum == -1 and department != ""):
        ret_query = """
        SELECT *
        FROM courses
        WHERE Department = "{par1}"
        """.format(par1 = department)
    elif(courseNum != -1 and department == ""):
        ret_query = """
        SELECT *
        FROM courses
        WHERE CourseNum = {par1}
        """.format(par1 = courseNum)
    else:
        ret_query = """
        SELECT *
        FROM courses
        WHERE CourseNum = {par1}
        AND Department = "{par2}"
        """.format(par1 = courseNum, par2 = department)

    cursor.execute(ret_query)
    result = cursor.fetchall()

    if (len(result) == 0):
        return False
    elif (len(result) >= 1):
        return True

#for a student to drop a course they are currently enrolled in
def drop_course(cursor, courseNum, sectionNum, department, studentID):
    ret_query = """
    DELETE FROM takes
    WHERE Courses_CourseNum = "{par1}"
    AND SectionNum = "{par2}"
    AND Department = "{par3}"
    AND Students_ID = "{par4}"
    """.format(par1=courseNum,par2=sectionNum,par3=department,par4=studentID)
    return ret_query

def change_section(courseNum, sectionNum):
    ret_query = """
    UPDATE takes
    SET SectionNum = "{par1}"
    WHERE Courses_CourseNum = "{par2}"
    """.format(par1=sectionNum,par2=courseNum)
    return ret_query


def change_housing(oldState, oldStreet, oldZip, stateAddress, streetAddress, zipCode):
    ret_query = """
    UPDATE Housing
    SET Rooms = Rooms + 1
    WHERE StateAddress = "{par1}"
    AND StreetAddress = "{par2}"
    AND ZipCode = "par3}"

    SET Rooms = Rooms - 1
    WHERE StateAddress = "{par4}"
    AND StreetAddress = "{par5}"
    AND ZipCode = "{par6}"
    AND Rooms > 0
    """
    return ret_query

def schedule_housing(stateAddress, streetAddress, zipCode):
    ret_query = """
    UPDATE Housing
    SET Rooms = Rooms - 1
    WHERE StateAddress = "{par1}"
    AND StreetAddress = "{par2}"
    AND ZipCode = "{par3}"
    AND Rooms > 0
    """
    return ret_query

def current_grades(cursor, studentID):
    ret_query = """
    SELECT *
    FROM Grades
    WHERE Students_ID = "{par1}"
    """.format(par1=studentID)
    return ret_query

def average_grades(courseNum):
    ret_query = """
    SELECT AVG(NumGrade)
    FROM GRADES
    WHERE Courses_courseNum = "{par1}"
    """.format(par1=courseNum)
    return ret_query

def get_min_in_course(courseNum):
    ret_query = """
    SELECT MIN(NumGrade)
    FROM GRADES
    WHERE Courses_courseNum = "{par1}"
    """.format(par1=courseNum)
    return ret_query

def get_max_in_course(courseNum, department):
    ret_query = """
    SELECT MAX(NumGrade)
    FROM GRADES
    WHERE Courses_courseNum = "{par1}"
    AND Department = "{par2}"
    """.format(par1=courseNum, par2 = department)
    return ret_query

def update_grade(newGrade, courseNum, stuID):
    ret_query = """
    UPDATE GRADES
    SET Grade = "{par1}"
    WHERE CourseNum = "{par2}"
    AND Students_ID = "{par3}"
    """.format(par1=newGrade, par2 = courseNum, par3 = stuID)

    return ret_query

def switch_department(cursor, profID, newDepartment):
    ret_query = """
    UPDATE professors
    SET Department = "{par1}"
    WHERE id = "{par2}"
    """.format(par1 = newDepartment, par2 = profID)

    return ret_query

def validateProfessor(cursor, profID):
    ret_query = """
    SELECT count(*)
    FROM professors
    WHERE ID = "{par1}"
    """.format(par1 = profID)

    cursor.execute(ret_query)
    result = cursor.fetchall()

    if (len(result) == 0):
        return False
    elif (len(result) >= 1):
        return True

def validateStudent(cursor, studentID):
    ret_query = """
    SELECT count(*)
    FROM students
    WHERE ID = {par1}
    """.format(par1 = studentID)

    cursor.execute(ret_query)
    result = cursor.fetchall()

    if (len(result) == 0):
        return False
    elif (len(result) >= 1):
        return True

def changeProfDepartmentMenu(connection, cursor):
    print("")
    profID = 0
    print("1) Enter the Professors ID")
    print("2) Go back to the previous menu")
    print("")

    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2):
                print("Must be a number between 1-2, inclusive.")
                continue
        except ValueError:
            print("Not a valid input. Please re-enter")
        else:
            break

    if (choice == 2):
        prof_menu(connection, cursor)

    print("Enter the professors ID")
    print("Enter 0 to return to the previous menu")

    while True:
        try:
            profID = int(input())
            if (profID == 0):
                break
            if (validateProfessor(cursor, profID)):
                break
            else:
                print("Must be a valid id:")
                continue
        except ValueError as e:
            print("Must be a valid id:")
        else:
            break

    if profID == 0:
        prof_menu(connection, cursor)

    department = input("Enter the new department: ")
    change = switch_department(cursor, profID, department)
    try:
        cursor.execute(change)
        connection.commit()
    except Error as e:
        print(e)

    prof_menu(connection, cursor)

def findStuID(cursor, studentID):
    ret_query = """
    SELECT *
    FROM students
    WHERE ID = "{par1}"
    """.format(par1=studentID)

    return ret_query

def findStuNameDOB(cursor, fname, lname, day, month, year):
    ret_query = """
    SELECT *
    FROM students
    WHERE FirstName = "{par1}"
    AND LastName = "{par2}"
    AND DOBDay = "{par3}"
    AND DOBMonth = "{par4}"
    AND DOBYear = "{par5}"
    """.format(par1=fname, par2=lname, par3=day, par4=month, par5=year)

    return ret_query

def findProfName(cursor, name):
    ret_query = """
    SELECT *
    FROM professors
    WHERE Name = "{par1}"
    """.format(par1 = name)

    return ret_query

def findProfDepart(cursor, department):
    ret_query = """
    SELECT *
    FROM professors
    WHERE Department = "{par1}"
    """.format(par1 = department)

    return ret_query

def findProfDOB(cursor, day, month, year):
    ret_query = """
    SELECT *
    FROM professors
    WHERE DOBDay = {par1}
    AND DOBMonth = {par2}
    AND DOBYear = {par3}
    """.format(par1 = day, par2 = month, par3 = year)

    return ret_query

def findCourse(cursor, courseNum=-1, department=""):
    if(courseNum == -1 and department != ""):
        ret_query = """
        SELECT *
        FROM courses
        WHERE Department = "{par1}"
        """.format(par1 = department)
    elif(courseNum != -1 and department == ""):
        ret_query = """
        SELECT *
        FROM courses
        WHERE CourseNum = "{par1}"
        """.format(par1 = courseNum)
    elif(courseNum != -1 and department != ""):
        ret_query = """
        SELECT *
        FROM courses
        WHERE CourseNum = {par1}
        AND Department = "{par2}"
        """.format(par1 = courseNum, par2 = department)
    else:
        ret_query = """
        SELECT *
        FROM courses
        """
    return ret_query

def findProfessorMenu(connection, cursor):
    print("")
    print("What parameter would you like to search by?")
    print("1) Name")
    print("2) Department")
    print("3) DOB")
    name = 0
    department = 0
    dob = 0

    choice = 0
    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2 and choice != 3):
                print("Must be a number between 1-3, inclusive.")
                continue
        except ValueError:
            print("Not a valid input. Please input a number between 1-3:")
        else:
            break

    if choice == 1:
        name = input("Enter the professors name: ")
        query = findProfName(cursor, name)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                print("")
                print("Name:", i[0], ", Department:", i[5], ", ID:", str(i[4]), ", DOB: "+str(i[1])+"/"+str(i[2])+"/" +str(i[3]))
                print("")

            if not result:
                print ("No Results Found.")
        except Error as e:
            print(e)

    if choice == 2:
        department = input("Enter the professors department: ")
        query = findProfDepart(cursor, department)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                print("")
                print("Name:", i[0], "Department:", i[5], ", ID:", str(i[4]), ", DOB: "+str(i[1])+"/"+str(i[2])+"/" +str(i[3]))

            if not result:
                print ("No Results Found.")
        except Error as e:
            print(e)

    if choice == 3:
        day = input("Enter the day of birth: ")
        month = input ("Enter the month of birth: ")
        year = input("Enter the year of birth: ")
        query = findProfDOB(cursor, day, month, year)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                print("")
                print("Name:", i[0], "Department:", i[5], ", ID:", str(i[4]), ", DOB: "+str(i[1])+"/"+str(i[2])+"/" +str(i[3]))

            if not result:
                print ("No Results Found.")
        except Error as e:
            print(e)


    prof_menu(connection, cursor)

def add_course(cursor, courseNum, sectionNum, department, studentID):
    ret_query = """
    INSERT INTO takes
    VALUES ("{par1}", "{par2}", "{par3}", "{par4}", {par5})
    """.format(par1 = sectionNum, par2 = studentID, par3 = courseNum, par4 = department, par5 = 0)
    return ret_query

def addCourseMenu(connection, cursor):
    while True:
        try:
            print("Enter 0 to return to the previous menu")
            studentID = int(input("Enter the student's ID: "))
            if (studentID == 0):
                break
            if (validateStudent(cursor, studentID)):
                break
            else:
                print("Must be a valid id:")
                continue
        except ValueError as e:
            print("Must be a valid id:")
    while True:
        try:
            courseNum = int(input("Enter the course number: "))
            sectionNum = int(input("Enter the section number: "))
            department = input("Enter the department: ")
            if (validateAddCourse(cursor, courseNum, department)):
                break
            else:
                print("Must be valid course information:")
                continue
        except ValueError as e:
            print("Must be valid course information:")
    query = add_course(cursor, courseNum, sectionNum, department, studentID)
    try:
        cursor.execute(query)
        print("Course successfully added.")
        connection.commit()
    except Error as e:
        print(e)

    student_menu(connection, cursor)
def add_course(cursor, courseNum, sectionNum, department, studentID):
    ret_query = """
    INSERT INTO takes
    VALUES ("{par1}", "{par2}", "{par3}", "{par4}", {par5})
    """.format(par1 = sectionNum, par2 = studentID, par3 = courseNum, par4 = department, par5 = 0)
    return ret_query
def validateAddCourse(cursor, courseNum, department):
    ret_query = """
    SELECT count(*)
    FROM courses
    WHERE CourseNum = "{par1}"
    AND Department = "{par2}"
    """.format(par1 = courseNum, par2 = department)

    cursor.execute(ret_query)
    result = cursor.fetchall()

    if (len(result) == 0):
        return False
    elif (len(result) == 1):
        return True

def dropCourseMenu(connection, cursor):
    while True:
        try:
            print("Enter 0 to return to the previous menu")
            studentID = int(input("Enter the student's ID: "))
            if (studentID == 0):
                break
            if (validateStudent(cursor, studentID)):
                break
            else:
                print("Must be a valid id:")
                continue
        except ValueError as e:
            print("Must be a valid id:")
    courseNum = input("Enter the course number: ")
    sectionNum = input("Enter the section number: ")
    department = input("Enter the department: ")
    query = drop_course(cursor, courseNum, sectionNum, department, studentID)
    try:
        cursor.execute(query)
        print("Course successfully dropped.")
        connection.commit()
    except Error as e:
        print(e)
    student_menu(connection, cursor)

def printGradesMenu(connection, cursor):
    while True:
        try:
            print("Enter 0 to return to the previous menu")
            studentID = int(input("Enter the student's ID: "))
            if (studentID == 0):
                break
            if (validateStudent(cursor, studentID)):
                break
            else:
                print("Must be a valid id:")
                continue
        except ValueError as e:
            print("Must be a valid id:")
    query = current_grades(cursor, studentID)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            print(str(i[1]) + ":", i[0], "- " + str(i[4])+ " "+ str(i[2]))

        if not result:
            print ("No Results Found.")
    except Error as e:
        print("ERROR",e)
    student_menu(connection, cursor)

def findStudentMenu(connection, cursor):
    print("")
    print("What parameter would you like to search by?")
    print("1) ID")
    print("2) Name & DOB")

    choice = 0
    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2):
                print("Input must be either 1 or 2.")
                continue
        except ValueError:
            print("Not a valid input. Please input either 1 or 2:")
        else:
            break

    if choice == 1:
        studentID = input("Enter the student's ID: ")
        query = findStuID(cursor, studentID)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                print("")
                print("Name:", i[3], i[4], i[5], "- DOB:", str(i[9])+"/"+str(i[10])+"/"+str(i[11]), "- Major:", i[1], " - Credits Earned:", i[2])

            if not result:
                print ("No Results Found.")
        except Error as e:
            print(e)

    if choice == 2:
        fname = input("Enter the student's first name: ")
        lname = input("Enter the student's last name: ")
        day = input("Enter the student's day of birth: ")
        month = input ("Enter the student's month of birth: ")
        year = input("Enter the student's year of birth: ")
        query = findStuNameDOB(cursor, fname, lname, day, month, year)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                print("")
                print("Name:", i[3], i[4], i[5], "- DOB:", str(i[9])+"/"+str(i[10])+"/"+str(i[11]), "- Major:", i[1], " - Credits:", i[2])
                print("")

            if not result:
                print ("No Results Found.")
        except Error as e:
            print(e)
    student_menu(connection, cursor)


def find_course_menu(connection, cursor):
    print("")
    choice = 0
    query = ""
    courseNum = -1
    department = ""
    print("How would you like to search for a course?")
    print("1) Department")
    print("2) Course Number")
    print("3) Department and Course Number")
    print("4) List all courses")
    print("5) Go back to previous menu")

    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2 and choice != 3 and choice != 4 and choice != 5):
                print("Must be a number between 1-5, inclusive.")
                continue
        except ValueError:
            print("Not a valid input. Please input a number between 1-4:")
        else:
            break
    if choice == 1:
        department = input("Enter the department: ")
        if(validateCourse(cursor,-1,department)):
            query = findCourse(cursor,-1,department)

    elif choice == 2:
        courseNum = int(input("Enter the course number: "))
        if(validateCourse(cursor,courseNum, "")):
            query = findCourse(cursor,courseNum,"")

    elif choice == 3:
        department = input("Enter the department: ")
        courseNum = int(input("Enter the course number: "))
        if(validateCourse(cursor,courseNum,department)):
            query = findCourse(cursor,courseNum,department)
    elif choice == 4:
            query = findCourse(cursor,courseNum,department)
    elif choice == 5:
        course_menu(connection, cursor)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            print("")
            print("Course Number:", i[0], ", Credits:", i[1], ", Department:", str(i[2]))
            print("")

        if not result:
            print ("No Results Found.")
    except Error as e:
        print(e)
    course_menu(connection, cursor)

def add_course_menu(connection, cursor):
    print("")
    courseNum = int(input("Enter the course number:"))
    department = input("Enter the department:")
    credits = int(input("Enter the amount of credits: "))
    query = ret_query = """
        INSERT INTO courses(courseNum,Credits,Department)
        VALUES
        ({par1},{par2},"{par3}")
        """.format(par1 = courseNum, par2 = credits, par3 = department)
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)
    course_menu(connection, cursor)

def remove_course(connection, cursor):
    print("")
    choice = 0
    courseNum = int(input("Enter the course number:"))
    department = input("Enter the department:")
    credits = int(input("Enter the amount of credits: "))
    query = ret_query = """
        DELETE FROM courses
        WHERE courseNum = {par1}
        AND Department = "{par3}"
        AND Credits = {par2}
        """.format(par1 = courseNum, par2 = credits, par3 = department)
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)
    course_menu(connection, cursor)

def aggregate(connection, cursor):
    print("")
    choice = 0
    course_num = -1
    query = ""
    print("What would you like to do?")
    print("1) Find max grade in a course")
    print("2) Find min grade in a course")
    print("3) Find average grade in a course")
    print("4) Go back to previous menu")
    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2 and choice != 3 and choice != 4):
                print("Must be a number between 1-4, inclusive.")
                continue
        except ValueError:
            print("Not a valid input. Please input a number between 1-4:")
        else:
            break

    if choice == 1:
            course_num = int(input("Enter the course number: "))
            department = input("Enter the department: ")
            query = get_max_in_course(course_num, department)
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                for i in result:
                    print("")
                    print("Max Grade:", i[0])
                    print("")

                if not result:
                    print ("Course does not exist.")
            except Error as e:
                print(e)

    elif choice == 2:
            course_num = int(input("Enter the course number: "))
            department = input("Enter the department: ")
            query = get_min_in_course(course_num)
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                for i in result:
                    print("")
                    print("Min Grade:", i[0])
                    print("")

                if not result:
                    print ("Course does not exist.")
            except Error as e:
                print(e)

    elif choice == 3:
            course_num = int(input("Enter the course number: "))
            department = input("Enter the department: ")

            query = average_grades(course_num)
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                for i in result:
                    print("")
                    print("Average Grade:", i[0])
                    print("")

                if not result:
                    print ("Course does not exist.")
            except Error as e:
                print(e)
    course_menu(connection,cursor)

def showProfessorCourses(cursor, profID):
    ret_query = """
    SELECT courses_CourseNum, SectionNum
    FROM instructs
    WHERE Professors_ID = {par1}
    """.format(par1 = profID)

    return ret_query

def dropProfessorCourse(cursor, profID, CourseNum, Department, SectNum):
    ret_query = """
    DELETE from
    instructs
    WHERE Professors_ID = {par1}
    AND courses_CourseNum = {par2}
    AND Departments = "{par3}"
    AND SectionNum = {par4}
    """.format(par1=profID, par2 = CourseNum, par3 = Department, par4 = SectNum)

    return ret_query


def dropProfessorCourseMenu(connection, cursor):
    profID = 0
    courseNum = 0
    print("Enter the professors ID")
    print("Enter 0 to return to the previous menu")

    while True:
        try:
            profID = int(input())
            if (profID == 0):
                break
            if (validateProfessor(cursor, profID)):
                break
            else:
                print("Must be a valid id:")
                continue
        except ValueError as e:
            print("Must be a valid id:")
        else:
            break

    if profID == 0:
        changeProfessorCourses(connection, cursor)

    department = input("Enter the department name: ")
    print("Enter the course number: ")
    while True:
        try:
            courseNum = int(input())
            if (validateCourse(cursor, courseNum, department)):
                break
            else:
                print("Must be a valid course number: ")
        except ValueError as e:
            print("Must be a valid course number: ")
        else:
            break

    sectNum = int(input("Enter a section number: "))
    query = dropProfessorCourse(cursor, profID, courseNum, department, sectNum)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        print("Course successfully removed")
    except Error as e:
        print(e)

    changeProfessorCourses(connection, cursor)


def addProfessorCourse(cursor, profID, CourseNum, Department, SectionNum):
    ret_query = """
    INSERT INTO
    INSTRUCTS VALUES(
    {par1}, {par2}, "{par3}", {par4}
    )""".format(par1=profID, par2 = SectionNum, par3 = Department, par4 = CourseNum)

    return ret_query


def addProfessorCourseMenu(connection, cursor):
    profID = 0
    courseNum = 0
    print("Enter the professors ID")
    print("Enter 0 to return to the previous menu")

    while True:
        try:
            profID = int(input())
            if (profID == 0):
                break
            if (validateProfessor(cursor, profID)):
                break
            else:
                print("Must be a valid id:")
                continue
        except ValueError as e:
            print("Must be a valid id:")
        else:
            break

    if profID == 0:
        changeProfessorCourses(connection, cursor)

    department = input("Enter the department name: ")
    print("Enter the course number: ")
    while True:
        try:
            courseNum = int(input())
            if (validateCourse(cursor, courseNum, department)):
                break
            else:
                print("Must be a valid course number: ")
        except ValueError as e:
            print("Must be a valid course number:")
        else:
            break

    sectNum = int(input("Enter a section number: "))
    query = addProfessorCourse(cursor, profID, courseNum, department, sectNum)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        print("Course successfully added")
    except Error as e:
        print(e)

    changeProfessorCourses(connection, cursor)


def showProfessorCourseMenu(connection, cursor):
    profID = 0
    print("Enter the professors ID")
    print("Enter 0 to return to the previous menu")

    while True:
        try:
            profID = int(input())
            if (profID == 0):
                break
            if (validateProfessor(cursor, profID)):
                break
            else:
                print("Must be a valid id:")
                continue
        except ValueError as e:
            print("Must be a valid id:")
        else:
            break

    query = showProfessorCourses(cursor, profID)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            print("Course Number: " + str(i[0]) + ", Section Number: " + str(i[1]))
    except Error as e:
        print(e)

    changeProfessorCourses(connection, cursor)


def changeProfessorCourses(connection, cursor):
    print("")
    profID = 0
    course = 0
    department = 0
    print("Please choose a number from the available options:")
    print("1) Add a course for a professor")
    print("2) Drop a course for a profssor")
    print("3) View a professors courses")
    print("4) Return to the previous menu")

    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2 and choice != 3 and choice != 4):
                print("Must be a number between 1-4, inclusive.")
                continue
        except ValueError:
            print("Not a valid input. Please input a number between 1-4:")
        else:
            break

    if choice == 1:
        addProfessorCourseMenu(connection, cursor)
    if choice == 2:
        dropProfessorCourseMenu(connection, cursor)
    if choice == 3:
        showProfessorCourseMenu(connection, cursor)
    if choice == 4:
        prof_menu(connection, cursor)


def prof_menu(connection, cursor):
    print("")
    choice = 0
    print("Welcome to the professors menu.")
    print("Please choose a number from the available options: ")
    print("1) Change Professors Department")
    print("2) Change Professors Courses")
    print("3) Find Professor")
    print("4) Go back to the previous menu")

    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2 and choice != 3 and choice != 4):
                print("Must be a number between 1-4, inclusive.")
                continue
        except ValueError:
            print("Not a valid input. Please input a number between 1-4:")
        else:
            break

    if choice == 1:
        changeProfDepartmentMenu(connection, cursor)
    if choice == 2:
        changeProfessorCourses(connection, cursor)
    if choice == 3:
        findProfessorMenu(connection, cursor)
    if choice == 4:
        mainMenu(connection, cursor)




def student_menu(connection, cursor):
    print("")
    choice = 0
    print("Welcome to the students menu.")
    print("Please choose a number from the available options: ")
    print("1) Add Course for student")
    print("2) Drop Course for student")
    print("3) Print Current Grades")
    print("4) Find Student")
    print("5) Return to the previous menu")
    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2 and choice != 3 and choice != 4 and choice != 5):
                print("Must be a number between 1-5, inclusive.")
                continue
        except ValueError:
            print("Not a valid input. Please input a number between 1-5:")
        else:
            break

    if choice == 1:
        addCourseMenu(connection, cursor)
    elif choice == 2:
        dropCourseMenu(connection, cursor)
    elif choice == 3:
        printGradesMenu(connection, cursor)
    elif choice == 4:
        findStudentMenu(connection, cursor)
    elif choice == 5:
        mainMenu(connection, cursor)




def course_menu(connection, cursor):
    print("")
    choice = 0
    print("Welcome to the course menu.")
    print("Please choose a number from the available options: ")
    print("1) Find a Course")
    print("2) Remove a Course")
    print("3) Add a Course")
    print("4) Find Min, Max, or Average Grade in a course")
    print("5) Return to the previous menu")

    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2 and choice != 3 and choice != 4 and choice != 5):
                print("Must be a number between 1-4, inclusive.")
                continue
        except ValueError:
            print("Not a valid input. Please input a number between 1-3:")
        else:
            break
    if choice == 1:
       find_course_menu(connection,cursor)
    if choice == 2:
        remove_course(connection,cursor)
    if choice == 3:
        add_course_menu(connection,cursor)
    if choice == 4:
        aggregate(connection, cursor)
    if choice == 5:
        mainMenu(connection, cursor)




def mainMenu(connection, cursor):
    print("Please choose a number from the available options: ")
    print("1) Alter or view a professors records")
    print("2) Alter or view a students records")
    print("3) Alter or view a courses records")
    print("4) Exit the application")
    choice = 0

    while True:
        try:
            choice = int(input())
            if (choice != 1 and choice != 2 and choice != 3 and choice != 4):
                print("Must be a number between 1-4, inclusive.")
                continue
        except ValueError:
            print("Not a valid input. Please input a number between 1-4:")
        else:
            break

    if choice == 1:
        prof_menu(connection, cursor)
    if choice == 2:
        student_menu(connection, cursor)
    if choice == 3:
        course_menu(connection, cursor)
    if choice == 4:
        return




def driver():
    try:
        with connect(host="localhost",user="root",password=input("Enter your passowrd:"),database="mydb") as connection:
                with connection.cursor() as cursor:
                    print("Welcome to the Missouri S&T administrative tool.")
                    mainMenu(connection, cursor)
                    connection.commit()
    except Error as e:
        print(e)





driver()
