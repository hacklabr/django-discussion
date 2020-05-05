from rest_framework import permissions
from discussion.models import Topic, Comment, Forum


class IsForumAuthor(permissions.BasePermission):
    """
    Custom permission to only allow a forum author to edit its own topic
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.is_superuser:
            return True
        elif request.user.is_authenticated and isinstance(obj, Forum) and obj.author == request.user:
            return True


class IsTopicAuthor(permissions.BasePermission):
    """
    Custom permission to only allow a topic author to edit its own topic
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.is_superuser:
            return True
        elif request.user.is_authenticated and isinstance(obj, Topic) and obj.author == request.user:
            return True


class IsCommentAuthor(permissions.BasePermission):
    """
    Custom permission to only allow a comment author to edit its own comment
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.is_superuser:
            return True
        elif request.user.is_authenticated and isinstance(obj, Comment) and obj.author == request.user:
            return True
