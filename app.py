from chalice import Chalice
import sqlalchemy as db

app = Chalice(app_name='checkout_cart')

engine = db.create_engine('mysql+pymysql://vikas:vikas@localhost/chaliceapp')
con = engine.connect()

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/create-tables')
def route_create_tables():
    print("Running query")
    # cursor = con.cursor()
    cursor = con.execute("select * from users")
    records = cursor.fetchall()
    print("Total number of rows in table: ", cursor.rowcount)

    print("\nPrinting each row")
    dict = {}
    for row in records:
        dict["Name"] = row[0]
        dict["Email"] = row[1]
    return {"Output": dict}
