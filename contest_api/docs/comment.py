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
from contest_api.services.comment import (
    ListCommentService,
    CreateCommmentService,
    UpdateCommentService,
    DeleteCommentService
)

#LIST CREATE COMMENT APIVIEW
comments_list_docs = {
    "tags": ['/contest_api/photos/'], #not sure with the tag
    "parameters": prepare_parameters_for_docs(
        ListCommentService,
        exclude=('photo_id',)
    ),
    "responses": {
        "200": OpenApiResponse(
            response=ParentCommentSerializer,
        ),
        "400": get_validation_error_yasg_response(),
    }
}

comments_create_docs = {
    "tags": ['/contest_api/photos/'], #same problemito baninito
    "request": prepare_request_body_for_docs(
        CreateCommmentService, exclude=("user",)
    ),
    "responses": {
        "200": OpenApiResponse(
            response=NewCommentSerializer,
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}

#UPDATE DELETE COMMENT APIVIEW
comments_update_docs = {
    "tags": ['/contest_api/comments/'],
    "request": prepare_request_body_for_docs(
        UpdateCommentService, 
        exclude=("user",)
    ),
    "responses": {
        "200": OpenApiResponse(
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}

comments_delete_docs = {
    "tags": ['/contest_api/comments/'],
    "parameters": prepare_parameters_for_docs(
        DeleteCommentService, 
        exclude=("user",)
    ),
    "responses": {
        "200": OpenApiResponse(
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}

