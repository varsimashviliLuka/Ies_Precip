import pymysql
'''
ცვლადების, ფუნქციების სახელები, კოდის განლაგება, რაც არ მოგეწონება ყველაფერი შეცვალე კოდის ლოგიკის გარდა და თან დააკომენტარე,
თვითონ კოდის ფუნქციონალი იმიტო არა რო თუ ჩემით, წვალებით გავაკეთებ უფრო გამიჯდება ტვინში
'''



try:
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="Ml@Root88",
        database="weather"
    )
except Exception as err:
    print(f"ბაზასთან კავშირი ვერ შედგა - {err}")


def pa_long_db_accumulator():
    mycursor = mydb.crusor()
    mycursor.execute("select ")










