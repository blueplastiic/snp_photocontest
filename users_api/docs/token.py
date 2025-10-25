from drf_spectacular.utils import OpenApiResponse

from service_objects_autodocs.auto_parameters_spectacular import prepare_parameters_for_docs, prepare_request_body_for_docs
from service_objects_autodocs.common import add_pagination_to_data_serializer 
from service_objects_autodocs.exceptions import ( 
    get_authentication_failed_yasg_response,
    get_validation_error_yasg_response,
)

from users_api.services.token.update import UpdateTokenService
from users_api.serializers.token.retrieve import RetrieveTokenSerializer

user_update_docs = {
    "tags": ['/users_api/'],
    "parameters": prepare_parameters_for_docs(
        UpdateTokenService, 
        exclude=("user",)
    ),
    "responses": {
        "201": OpenApiResponse(
            RetrieveTokenSerializer
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}

