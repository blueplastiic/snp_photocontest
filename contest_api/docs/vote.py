from drf_spectacular.utils import OpenApiResponse

from service_objects_autodocs.common import add_pagination_to_data_serializer 
from service_objects_autodocs.auto_parameters_spectacular import (
    prepare_parameters_for_docs, 
    prepare_request_body_for_docs
)
from service_objects_autodocs.exceptions import (                    
    get_authentication_failed_yasg_response,
    get_validation_error_yasg_response,
)

from contest_api.services.vote import (
    CreateVoteService,
    DeleteVoteService
)

#CREATE VOTE APIVIEW
votes_create_docs = {
    "tags": ['/contest_api/votes/'],
    "request": prepare_request_body_for_docs(
        CreateVoteService, exclude=("user",)
    ),
    "responses": {
        "200": OpenApiResponse(),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}

#DELETE VOTE APIVIEW
votes_delete_docs = {
    "tags": ['/contest_api/votes/'],
    "parameters": prepare_parameters_for_docs(
        DeleteVoteService, 
        exclude=("user",)
    ),
    "responses": {
        "200": OpenApiResponse(
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}

