from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .permission import UserIsOwner
from . import serializers, models

# User = get_user_model()

class UserProfileAPIView(generics.RetrieveAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwner,
    )
    serializer_class = serializers.UserProfileChangeSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self):
        user_id = self.kwargs["user_id"]
        obj = get_object_or_404(models.CustomUser, id=user_id)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
