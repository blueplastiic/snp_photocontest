from drf_spectacular.utils import OpenApiResponse

from service_objects_autodocs.auto_parameters_spectacular import prepare_parameters_for_docs, prepare_request_body_for_docs #type: ignore
from service_objects_autodocs.common import add_pagination_to_data_serializer #type: ignore
from service_objects_autodocs.exceptions import (                    
    get_authentication_failed_yasg_response,
    get_validation_error_yasg_response,
)


from contest_api.serializers.photo import (
    ListPhotoSerializer, 
    ListCurrentUserPhotoSerializer,
    RetrievePhotoSerializer,
    NewPhotoSerializer
)

from contest_api.services.photo import (
    ListPhotoService,
    ListUserPhotoService, 
    ListCurrentUserPhotoService, 
    RetrievePhotoService,
    CreatePhotoService
)

#LIST CREATE PHOTO APIVIEW    
photos_list_docs = {
    "tags": ['/photo/'],
    "parameters": prepare_parameters_for_docs(ListPhotoService),
    "responses": {
        "200": OpenApiResponse(
            response=add_pagination_to_data_serializer(ListPhotoSerializer),
        ),
        "400": get_validation_error_yasg_response(),
    }
}
#trouble here
# photo_create_docs = {
#     "tags": ['/photo/'],
#     "parameters": prepare_request_body_for_docs(
#         CreatePhotoService,
#         exclude=("user",),
#         
#     ),
#     "responses": {
#         "200": OpenApiResponse(
#             response=NewPhotoSerializer,
#         ),
#         "400": get_validation_error_yasg_response(),
#     }
# }


#LIST USER PHOTO APIVIEW
user_photos_list_docs = {
    "tags": ['/photo/'],
    "parameters": prepare_parameters_for_docs(
        ListUserPhotoService,
        exclude=('user_id',),
    ),
    "responses": {
        "200": OpenApiResponse(
            response=add_pagination_to_data_serializer(ListPhotoSerializer),
        ),
        "400": get_validation_error_yasg_response(),
        #"401": get_authentication_failed_yasg_respnse()
    }
}

current_user_photos_list_docs = {
    "tags": ['/photo/'],
    "parameters": prepare_parameters_for_docs(
        ListCurrentUserPhotoService,
        exclude=("user",),
    ),
    "responses": {
        "200": OpenApiResponse(
            response=add_pagination_to_data_serializer(ListCurrentUserPhotoSerializer),
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response()
    }
}

photo_retrieve_docs = {
    "tags": ['/photo/'],
    "parameters": prepare_parameters_for_docs(
        RetrievePhotoService,
        exclude=("photo_id",),
    ),
    "responses": {
        "200": OpenApiResponse(
            response=RetrievePhotoSerializer,
        ),
        "400": get_validation_error_yasg_response(),
    }
}

