import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="iot_user",
    password="ai12345!",
    port=3307,
    database="mydatabase"
)

mycursor = mydb.cursor()

def show_menu():
    print('-' * 50)
    print('1. 주소록 생성')
    print('2. 주소록 추가')
    print('3. 주소록 조회')
    print('4. 주소록 수정')
    print('5. 주소록 삭제')
    print('6. 종료')

    menu_num = int(input('메뉴: '))
    return menu_num

# 주소록 생성
def create_table():
    check = "SHOW TABLES LIKE 'ADDR_TABLE'"
    mycursor.execute(check)
    result = mycursor.fetchall()
    if len(result):
        print("존재하는 테이블이 있습니다")
        return None

    mycursor.execute("CREATE TABLE ADDR_TABLE "
                     "(addr_id INTEGER PRIMARY KEY AUTO_INCREMENT,"
                     "name VARCHAR(255), "
                     "hp VARCHAR(255))")

    print("테이블이 생성되었습니다.")

# 주소록 추가
def insert_data():
    check = "SHOW TABLES LIKE 'ADDR_TABLE'"
    mycursor.execute(check)
    result = mycursor.fetchall()
    if not len(result):
        print("존재하는 테이블이 없습니다")
        return None

    name = input("이름을 입력해주세요: ")
    phone_num = input("전화번호를 입력해주세요: ")

    query = "INSERT INTO ADDR_TABLE (name, hp) VALUES (%s, %s)"
    val = (name, phone_num)

    mycursor.execute(query, val)
    mydb.commit()

    print(f"id:{mycursor.rowcount} 데이터가 정상적으로 입력되었습니다.")

# 주소록 조회
def select_data():
    check = "SHOW TABLES LIKE 'ADDR_TABLE'"
    mycursor.execute(check)
    result = mycursor.fetchall()
    if not len(result):
        print("존재하는 테이블이 없습니다")
        return None

    mycursor.execute("SELECT * FROM ADDR_TABLE")
    myresult = mycursor.fetchall()

    print("ADDR_ID\t name\tHP")
    for id, name, hp in myresult:
        print(f"{id}\t     {name}\t{hp}")

# 주소록 수정
def update_data():
    check = "SHOW TABLES LIKE 'ADDR_TABLE'"
    mycursor.execute(check)
    result = mycursor.fetchall()
    if not len(result):
        print("존재하는 테이블이 없습니다")
    return None

    col = int(input("변경할 옵션 선택[1.이름, 2. 전화번호]: "))
    if col == 1:
        column = 'name'
    else:
        column = 'hp'

    value1= input(f"수정하고 싶은 {column}을 입력하세요 : ")
    value2= input("수정할 내용을 입력하세요 : ")
    query = f"UPDATE ADDR_TABLE SET {column}='{value2}' WHERE {column}='{value1}'"

    mycursor.execute(query)
    mydb.commit()

# 주소록 삭제
def delete_table():
    check = "SHOW TABLES LIKE 'ADDR_TABLE'"
    mycursor.execute(check)
    result = mycursor.fetchall()
    if len(result):
        query = "DROP TABLE ADDR_TABLE"
        mycursor.execute(query)
        print("테이블이 삭제되었습니다.")
    else:
        print("존재하는 테이블이 없습니다")

def menu_func(num):
    if num == 1:
        create_table()
    elif num == 2:
        print("주소록 추가")
        insert_data()
    elif num == 3:
        print("주소록 조회")
        select_data()
    elif num == 4:
        print("주소록 수정")
        update_data()
    elif num == 5:
        print("주소록 삭제")
        delete_table()
    else:
        print("다시 입력")


if __name__ == "__main__":
    while True:
        print("*****미니주소록*****")
        menu_num = show_menu()
        if menu_num == 6:
            break
        else:
            menu_func(menu_num)

    mydb.close()
    mycursor.close()
