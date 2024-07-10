# from functools import wraps
# from flask import abort, request
# from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
# from aldo.models.user_accounts import User

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         verify_jwt_in_request()
#         user_id = get_jwt_identity()
#         user = User.query.get(user_id)
#         if user is None or not user.is_admin:
#             abort(403)  # Forbidden
#         return f(*args, **kwargs)
#     return decorated_function
from functools import wraps
from flask import abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from aldo.models.user_accounts import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user is None or not user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

