from django.utils import timezone
from datetime import timedelta
from .querysets import with_post_score

VALID_SORTS = {"new", "top","hot"}
VALID_T = {"day", "week","month","all"}

def normalize_sort_and_time(get_params):
    sort = get_params.get("sort", "new")
    if sort not in VALID_SORTS:
        sort = "new"

    t = get_params.get("t", "all")
    if t not in VALID_T:
        t = "all"

    return sort, t

def _apply_time_filter(qs,t):
    now = timezone.now()

    if t == "day":
        return qs.filter(created_at__gte=now - timedelta(days=1))
    elif t == "week":
        return qs.filter(created_at__gte=now - timedelta(weeks=1))
    elif t == "month":
        return qs.filter(created_at__gte=now - timedelta(days=30))
    return qs  # "all"

def apply_sort(qs, sort, t="all"):
    if sort == "new":
        return qs.order_by("-created_at")

    elif sort == "top":
        qs = _apply_time_filter(qs, t)
        qs = with_post_score(qs)
        return qs.order_by("-score")

    elif sort == "hot":
        qs = with_post_score(qs)
        return qs.order_by("-score", "-created_at")

    return qs.order_by("-created_at")