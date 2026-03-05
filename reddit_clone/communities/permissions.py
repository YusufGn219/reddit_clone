from .models import CommunityModerator

def is_community_owner(user, community):
    return community.created_by == user

def is_community_mod(user, community):
    return CommunityModerator.objects.filter(
        community=community,
        user=user
    ).exists()

def can_moderate(user, community):
    return is_community_owner(user, community) or is_community_mod(user, community)