from random import randint

from square_authentication_helper import SquareAuthenticationHelper

square_authentication_helper_obj = SquareAuthenticationHelper()
username = "temp" + str(randint(1, 2000))
password = "temp"
app_id = 1

# Example: register username
register_username_output = square_authentication_helper_obj.register_username_v0(
    username=username,
    password=password,
)
print(register_username_output)

user_id = register_username_output["data"]["main"]["user_id"]
# Example: update user app ids
update_user_app_ids_output = square_authentication_helper_obj.update_user_app_ids_v0(
    user_id=user_id, app_ids_to_add=[app_id], app_ids_to_remove=[]
)
print(update_user_app_ids_output)


# Example: update user app ids
get_user_app_ids_output = square_authentication_helper_obj.get_user_app_ids_v0(
    user_id=user_id,
)
print(get_user_app_ids_output)


# Example: login username
login_username_output = square_authentication_helper_obj.login_username_v0(
    username=username, password=password, app_id=app_id
)
print(login_username_output)

# Example: update username
new_username = "temp" + str(randint(1, 2000))
update_username_output = square_authentication_helper_obj.update_username_v0(
    new_username=new_username,
    access_token=login_username_output["data"]["main"]["access_token"],
)
print(update_username_output)

# Example: generate access token
generate_access_token_output = (
    square_authentication_helper_obj.generate_access_token_v0(
        user_id=user_id,
        app_id=app_id,
        refresh_token=login_username_output["data"]["main"]["refresh_token"],
    )
)
print(generate_access_token_output)

# Example: logout
logout_output = square_authentication_helper_obj.logout_v0(
    user_id=user_id,
    app_id=app_id,
    access_token=generate_access_token_output["data"]["main"]["access_token"],
    refresh_token=login_username_output["data"]["main"]["refresh_token"],
)
print(logout_output)
