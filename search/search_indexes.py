from haystack import indexes
from django.db.models import Q
from profiles.models import Profile


class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    bio = indexes.CharField(model_attr='bio')
    slug = indexes.CharField(model_attr='slug')


    def get_model(self):
        return Profile

    def index_queryset(self, using = None):
        return self.get_model().objects.all()