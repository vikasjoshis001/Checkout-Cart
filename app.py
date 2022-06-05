from chalice import Chalice, Response
import sqlalchemy as db
from DatabaseTasks.main import Product, Session, User, engine
import requests
from hashlib import sha256

app = Chalice(app_name='checkout_cart')

local_session = Session(bind=engine)


@app.route('/')
def index():
    return {'hello': 'world'}


#  Making a POST request to register a new user
@app.route('/register', methods=['POST'])
def register():
    """ Register a new user """
    try:
        # Taking the data from the request
        data = app.current_request.json_body
        user_name = data['user_name']
        full_name = data['full_name']
        password = data['password']

        #  Checking if password is strong enough
        if(len(password) < 8):
            return Response(
                body={
                    "Type": "Error",
                    "Message": "Password must be atleast 8 characters long"
                },
                status_code=400,
            )

        # Checking if user name is already taken
        users = local_session.query(User).all()
        for user in users:
            if(user.user_name == user_name):
                return Response(
                    body={
                        "Type": "Error",
                        "Message": "User already exists"
                    },
                    status_code=400,
                )

        #  Converting the password to hash
        h = sha256()
        h.update(password.encode())
        hash = h.hexdigest()

        # Creating the user
        user_data = User(user_name=user_name,
                         full_name=full_name, password=hash)
        local_session.add(user_data)

        #  Committing the changes
        local_session.commit()

        # Returning the response
        return Response(
            body={
                "Type": "Success",
                "Message": "User registered successfully",
            },
            status_code=201,
        )

    #  Handling the error
    except Exception as e:
        return Response(
            body={
                "Type": "Error",
                "Message": "Something went wrong, please try again.",
                "Error": str(e),
            },
            status_code=400,
        )


#  Driver code
if "__name__" == "__main__":
    app.run(debug=True)
