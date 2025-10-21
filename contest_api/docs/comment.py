from drf_spectacular.utils import OpenApiResponse

from service_objects_autodocs.auto_parameters_spectacular import prepare_parameters_for_docs #type: ignore
from service_objects_autodocs.common import add_pagination_to_data_serializer #type: ignore
from service_objects_autodocs.exceptions import ( #type: ignore
    get_authentication_failed_yasg_response,
    get_validation_error_yasg_response,
)


from contest_api.serializers.comment import ParentCommentSerializer
from contest_api.services.comment import ListCommentService


comments_list_docs = {
    "tags": ['/comment/'],
    "parameters": prepare_parameters_for_docs(
        ListCommentService, exclude=("current_user",)
    ),
    "responses": {
        "200": OpenApiResponse(
            response=ParentCommentSerializer,
        ),
        "400": get_validation_error_yasg_response(),
    }
}

