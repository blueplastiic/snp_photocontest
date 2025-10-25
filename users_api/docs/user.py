from drf_spectacular.utils import OpenApiResponse

from service_objects_autodocs.auto_parameters_spectacular import prepare_parameters_for_docs, prepare_request_body_for_docs
from service_objects_autodocs.common import add_pagination_to_data_serializer 
from service_objects_autodocs.exceptions import ( 
    get_authentication_failed_yasg_response,
    get_validation_error_yasg_response,
)


from contest_api.serializers.comment import (
    ParentCommentSerializer,
    NewCommentSerializer, 
)
from users_api.serializers.token.retrieve import RetrieveTokenSerializer
from users_api.services.user import (
    CreateUserService,
    DeleteUserService,
    RetrieveUserService,
    UpdatePublicInfoUserService
)

#RETRIEVE USER APIVIEW
user_public_retrieve_docs = {
    "tags": ['/users_api/'], 
    "parameters": prepare_parameters_for_docs(
        RetrieveUserService,
        exclude=('user_id',)
    ),
    "responses": {
        "200": OpenApiResponse(
            response=ParentCommentSerializer,
        ),
        "400": get_validation_error_yasg_response(),
    }
}

#RETRIEVE UPDATE DELETE USER APIVIEW 
user_private_retrieve_docs = {
    "tags": ['/users_api/'], 
    "responses": {
        "200": OpenApiResponse(
            response=NewCommentSerializer,
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}

user_update_docs = {
    "tags": ['/users_api/'],
    "request": prepare_request_body_for_docs(
        UpdatePublicInfoUserService, 
        exclude=("user",)
    ),
    "responses": {
        "200": OpenApiResponse(
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}

user_delete_docs = {
    "tags": ['/users_api/'],
    "parameters": prepare_parameters_for_docs(
        DeleteUserService, 
        exclude=("user",)
    ),
    "responses": {
        "200": OpenApiResponse(
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}


#CREATE USER APIVIEW
user_create_docs = {
    "tags": ['/users_api/'],
    "request": prepare_request_body_for_docs(
        CreateUserService, 
    ),
    "responses": {
        "201": OpenApiResponse(
            RetrieveTokenSerializer
        ),
        "400": get_validation_error_yasg_response(),
    }
}

