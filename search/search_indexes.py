from haystack import indexes
from profiles.models import Profile


class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='user')

    def get_model(self):
        return Profile

    def index_queryset(self, using = None):
        return self.get_model().objects.all()