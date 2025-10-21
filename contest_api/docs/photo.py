
from drf_spectacular.utils import OpenApiResponse

from service_objects_autodocs.auto_parameters_spectacular import prepare_parameters_for_docs #type: ignore
from service_objects_autodocs.common import add_pagination_to_data_serializer #type: ignore
from service_objects_autodocs.exceptions import (                    
    get_authentication_failed_yasg_response,
    get_validation_error_yasg_response,
)


from contest_api.serializers.photo import ListPhotoSerializer
from contest_api.services.photo import ListPhotoService


photos_list_docs = {
    "tags": ['/comment/'],
    "parameters": prepare_parameters_for_docs(
        ListPhotoService, exclude=("current_user",)
    ),
    "responses": {
        "200": OpenApiResponse(
            response=add_pagination_to_data_serializer(ListPhotoSerializer),
        ),
        "400": get_validation_error_yasg_response(),
        #"401": get_authentication_failed_yasg_respnse()
    }
}

