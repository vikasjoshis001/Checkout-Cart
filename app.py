from chalice import Chalice, Response
import sqlalchemy as db
from DatabaseTasks.main import Product, Session, User, engine
import requests
from hashlib import sha256
import json

app = Chalice(__name__)

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


# Making a POST request to login a user
@app.route('/login', methods=['POST'])
def login():
    """ Login a user """
    try:
        # Taking the data from the request
        data = app.current_request.json_body
        user_name = data['user_name']
        password = data['password']
        isUser = False

        # Checking if user name is registered
        users = local_session.query(User).all()
        for user in users:
            if(user.user_name == user_name):
                old_password = user.password
                isUser = True

        # If user name is not registered return error
        if not isUser:
            return Response(
                body={
                    "Type": "Error",
                    "Message": "User not registered",
                },
                status_code=400,
            )

        #  Converting the password to hash
        h = sha256()
        h.update(password.encode())
        hash = h.hexdigest()

        # Checking if password is correct
        if(old_password != hash):
            return Response(
                body={
                    "Type": "Error",
                    "Message": "Password is incorrect",
                },
                status_code=400,
            )

        return Response(
            body={
                "Type": "Success",
                "Message": "User logged in successfully",
            },
            status_code=200,
        )

    # Handling the error
    except Exception as e:
        return Response(
            body={
                "Type": "Error",
                "Message": "Something went wrong, please try again.",
                "Error": str(e),
            },
            status_code=400,
        )

@app.route('/api/getProduct')
def get_product():
    products=local_session.query(Product).all()
    output=[]
    for product in products:
        dict={}
        dict['id']=product.id
        dict['title']=product.title
        dict['price']=product.price
        dict['category']=product.category
        dict['description']=product.description
        dict['image']=product.image

        output.append(dict)
    
    return json.dumps(output,indent=4)

@app.route('/api/getProduct/{id}')
def get_particular_prod(id):
    prod=local_session.query(Product).filter(Product.id==id).first()

    if not prod:
        return json.dumps({'message':'no such product'})

    prod_data={}
    prod_data['id']=prod.id
    prod_data['title']=prod.title
    prod_data['price']=prod.price
    prod_data['category']=prod.category
    prod_data['description']=prod.description
    prod_data['image']=prod.image

    return json.dumps(prod_data,indent=4)

# #  Driver code
# if "__name__" == "__main__":
#     app.run(debug=True)
