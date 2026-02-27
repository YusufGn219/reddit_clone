from django.db.models import Sum, Value, IntegerField
from django.db.models.functions import Coalesce

def with_post_score(qs):
    return qs.annotate(
        score = Coalesce(
            Sum("votes__value"),
            Value(0),
            output_field=IntegerField()
        )
    )