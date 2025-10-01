from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound, ValidationError
from service_objects.fields import ModelField
from django import forms
from models_app.models import Comment, User

class DeleteCommentService(ServiceWithResult):
    photo_id = forms.IntegerField()
    comment_id = forms.IntegerField()
    user = ModelField(User)

    def process(self): #pyright: ignore
        photo_id = self.cleaned_data.get('photo_id')
        comment_id = self.cleaned_data.get('comment_id')
        user = self.cleaned_data.get('user')
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise NotFound(additional_info='Comment does not exist')

        if comment.photo_id != photo_id: #pyright: ignore
            raise ValidationError(additional_info=f'Comment {comment_id} does not belong to photo {photo_id}')

        if comment.user_id != user.id: #pyright: ignore
            raise ValidationError(additional_info='You can only delete your comments') #apparently we dont need drf permission in this case

        comment.delete()
        return self

