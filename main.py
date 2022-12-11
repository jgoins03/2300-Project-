from getpass import getpass
from mysql.connector import connect, Error

#make functions return a valid sql query and set it to a variable then commit it. allow it to take in parameters for the query?
def add_course(courseNum, sectionNum, openSeats, credits, major):
    ret_query = """
    INSERT INTO courses (CourseNum, Section_Num, Open_seats, Credits, Major)
    VALUES
    ({par1}, {par2}, {par3}, {par4}, "{par5}")
    """.format(par1=courseNum,par2=sectionNum,par3=openSeats,par4=credits,par5=major)
    return ret_query

def drop_course(courseNum, sectionNum, openSeats, credits, major):
    ret_query = """
    DELETE FROM courses
    WHERE CourseNum = {par1}
    AND Section_Num = {par2}
    AND Open_seats = {par3}
    AND Credits = {par4}
    AND Major = "{par5}"
    """.format(par1=courseNum,par2=sectionNum,par3=openSeats,par4=credits,par5=major)
    return ret_query

def change_section(courseNum, sectionNum):
    ret_query = """
    UPDATE courses
    SET Section_Num = {par1}
    WHERE CourseNum = {par2}
    """.format(par1=sectionNum,par2=courseNum)
    return ret_query

#def update_grade()
#def switch_department()
#def change_housing()
#def schedule_housing()
#def current_grades()
#def average_grades()
#def get_average_grade_in_course()
#def get_min_in_course()
#def get_max_in_course()
try:
    with connect(host="localhost",user=input("Enter username: "),password=getpass("Enter password: "),database="mydb") as connection:
            with connection.cursor() as cursor:
                print(connection)
                cursor.execute(change_section(5,20))
                connection.commit()
except Error as e:
    print(e)

