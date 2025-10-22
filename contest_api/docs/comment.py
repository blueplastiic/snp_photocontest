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

)

#LIST CREATE COMMENT APIVIEW
# comments_list_docs = {
#     "tags": ['/comment/'],
#     "parameters": prepare_request_body_for_docs(
#         ListCommentService,
#     ),
#     "responses": {
#         "200": OpenApiResponse(
#             response=ParentCommentSerializer,
#         ),
#         "400": get_validation_error_yasg_response(),
#     }
# }
#
# comments_create_docs = {
#     "tags": ['/comment/'],
#     "parameters": prepare_request_body_for_docs(
#         CreateCommmentService, exclude=("user",)
#     ),
#     "responses": {
#         "200": OpenApiResponse(
#             response=NewCommentSerializer,
#         ),
#         "400": get_validation_error_yasg_response(),
#     }
# }
#
