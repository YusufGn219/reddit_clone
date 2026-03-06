from .models import Community
from .models import Community, CommunityModerator


def navbar_communities(request):
    return {
        "navbar_communities": Community.objects.all().order_by("name")[:15]
    }

def navbar_data(request):

    communities = Community.objects.all().order_by("name")[:10]

    moderating = []

    if request.user.is_authenticated:

        moderating_ids = CommunityModerator.objects.filter(
            user=request.user
        ).values_list("community_id", flat=True)

        moderating = Community.objects.filter(id__in=moderating_ids)

    return {
        "navbar_communities": communities,
        "navbar_moderating": moderating
    }