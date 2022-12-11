from getpass import getpass
from mysql.connector import connect, Error

#make functions return a valid sql query and set it to a variable then commit it. allow it to take in parameters for the query?
def add_course(courseNum, sectionNum, openSeats, credits, major):
    ret_query = """
    INSERT INTO courses (CourseNum, Section_Num, Open_seats, Credits, Major)
    VALUES
    ({par1}, {par2}, {par3}, {par4}, "{par5}")
    """.format(par1=courseNum,par2=sectionNum,par3=openSeats,par4=credits,par5=major)
    print(ret_query)
    return ret_query


#def drop_course()
#def change_section()
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
                cursor.execute(add_course(5,8,20,3,"Computer Science"))
                connection.commit()
except Error as e:
    print(e)

