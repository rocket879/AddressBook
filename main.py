from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtGui import QIcon
import sys
import mysql.connector

DB_COLUMNS = ["name", "hp", "email"]


class AddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('미니 주소록 프로그램')
        self.setWindowIcon(QIcon('./icon/address_book.png'))
        self.setGeometry(100, 100, 700, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label_name = QLabel('Name:')
        self.edit_name = QLineEdit()
        layout.addWidget(label_name)
        layout.addWidget(self.edit_name)

        label_phone = QLabel('Phone:')
        self.edit_phone = QLineEdit()
        layout.addWidget(label_phone)
        layout.addWidget(self.edit_phone)

        label_email = QLabel('E-mail:')
        self.edit_email = QLineEdit()
        layout.addWidget(label_email)
        layout.addWidget(self.edit_email)

        self.btn_select = QPushButton('연락처 조회')
        self.btn_select.clicked.connect(self.select_contact)
        layout.addWidget(self.btn_select)

        self.btn_add = QPushButton('연락처 추가')
        self.btn_add.clicked.connect(self.add_contact)
        layout.addWidget(self.btn_add)

        self.btn_update = QPushButton('연락처 수정')
        self.btn_update.clicked.connect(self.update_contact)
        layout.addWidget(self.btn_update)

        self.btn_delete = QPushButton('연락처 삭제')
        self.btn_delete.clicked.connect(self.delete_contact)
        layout.addWidget(self.btn_delete)

        self.list_contacts = QListWidget()
        layout.addWidget(self.list_contacts)

    # 주소록 추가
    def add_contact(self):
        name = self.edit_name.text()
        phone = self.edit_phone.text()
        email = self.edit_email.text()
        
        check = "SHOW TABLES LIKE 'ADDR_TABLE'"
        mycursor.execute(check)
        result = mycursor.fetchall()
        if not len(result):
            print("존재하는 테이블이 없습니다")
            return None

        if name and phone and email:
            contact = f"[이름]: {name}    [번호]: {phone}    [E-mail]: {email}"
            self.list_contacts.addItem(contact)
            self.edit_name.clear()
            self.edit_phone.clear()
            self.edit_email.clear()

            query = "INSERT INTO ADDR_TABLE (name, hp, email) VALUES (%s, %s, %s)"
            val = (name, phone, email)
            mycursor.execute(query, val)
            mydb.commit()
            print("----- 연락처가 추가되었습니다. -----")
        else:
            QMessageBox.warning(self, 'Warning', '내용을 입력해주세요.')

    # 주소록 조회
    def select_contact(self):
        print("----- 연락처가 조회되었습니다. -----")
        check = "SHOW TABLES LIKE 'ADDR_TABLE'"
        mycursor.execute(check)
        result = mycursor.fetchall()
        if not len(result):
            print("존재하는 테이블이 없습니다")
            return None

        mycursor.execute("SELECT * FROM ADDR_TABLE")
        myresult = mycursor.fetchall()

        self.list_contacts.clear()
        for id, name, phone, email in myresult:
            # print(f"ID:{id}\t이름: {name:9s}번호: {phone:15s}E-mail: {email}")
            contact = f"[이름]: {name}    [번호]: {phone}    [E-mail]: {email}"
            self.list_contacts.addItem(contact)

    # 주소록 수정
    def update_contact(self):
        current_row = self.list_contacts.currentRow()

        if current_row >= 0:
            # 텍스트에서 column 추출하기
            current_item = self.list_contacts.currentItem().text()
            text = current_item.replace(' ', '')
            idx1, idx2, idx3 = text.find('이름'), text.find('번호'), text.find('E-mail')
            before_data = [text[idx1+4:idx2-1], text[idx2+4:idx3-1], text[idx3+8:]]
            # print(before_data)

            name = self.edit_name.text()
            phone = self.edit_phone.text()
            email = self.edit_email.text()

            if name or phone or email:
                check = "SHOW TABLES LIKE 'ADDR_TABLE'"
                mycursor.execute(check)
                result = mycursor.fetchall()
                if not len(result):
                    print("존재하는 테이블이 없습니다.")
                    return None

                query = f"UPDATE ADDR_TABLE \
                            SET name='{name}', hp='{phone}', email='{email}' \
                            WHERE hp='{before_data[1]}'"
                mycursor.execute(query)
                mydb.commit()

                contact = f"[이름]: {name}    [번호]: {phone}    [E-mail]: {email}"
                self.list_contacts.takeItem(current_row)
                self.list_contacts.insertItem(current_row, contact)
                self.edit_name.clear()
                self.edit_phone.clear()
                self.edit_email.clear()
            else:
                QMessageBox.warning(self, 'Warning', '이름, 번호, 이메일을 입력해주세요')
        else:
            QMessageBox.warning(self, 'Warning', '수정할 연락처를 선택해주세요.')

    # 연락처 삭제
    def delete_contact(self):
        current_row = self.list_contacts.currentRow()

        if current_row >= 0:
            # 텍스트에서 column 추출하기
            current_item = self.list_contacts.currentItem().text()
            text = current_item.replace(' ', '')
            idx1, idx2, idx3 = text.find('이름'), text.find('번호'), text.find('E-mail')
            before_data = [text[idx1+4:idx2-1], text[idx2+4:idx3-1], text[idx3+8:]]
            print(before_data)
            
            query = f"DELETE FROM ADDR_TABLE WHERE hp='{before_data[1]}';"
            mycursor.execute(query)
            mydb.commit()

            self.list_contacts.takeItem(current_row)
            self.edit_name.clear()
            self.edit_phone.clear()
            self.edit_email.clear()

            print("연락처가 삭제되었습니다.")
        else:
            QMessageBox.warning(self, 'Warning', '삭제할 연락처를 선택해주세요.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddressBook()
    window.show()

    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="0000",
        port=3306,
        database="address_book"
    )

    mycursor = mydb.cursor()

    if app.exec_() == 0:
        mydb.close()
        mycursor.close()
        print("Successful Termination")
    
    # sys.exit(app.exec_())
