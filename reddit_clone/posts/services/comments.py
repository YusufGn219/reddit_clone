from collections import defaultdict
from ..models import Comment

def build_comment_tree(post):
    qs = Comment.objects.filter(post=post).select_related("author").order_by("created_at")

    by_parent = defaultdict(list)
    nodes = {}

    for c in qs:
        c.child_nodes = []   # ✅ runtime liste (model field değil)
        nodes[c.id] = c
        by_parent[c.parent_id].append(c)

    for parent_id, kids in by_parent.items():
        if parent_id is None:
            continue
        parent = nodes.get(parent_id)
        if parent:
            parent.child_nodes.extend(kids)

    return by_parent[None]