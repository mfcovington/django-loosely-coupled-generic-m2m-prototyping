from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class RelatedContent(models.Model):
    """
    Relates any one entry to another entry irrespective of their individual models.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent_content_type = models.ForeignKey(ContentType, related_name="parent_test_link")
    parent_object_id = models.PositiveIntegerField()
    parent_content_object = GenericForeignKey('parent_content_type', 'parent_object_id')

    def __str__(self):
        return "{}: {}".format(self.content_type.name, self.content_object)

class DataPublicationRelationship(models.Model):

    data_limit = models.Q(app_label='data', model='data') | \
        models.Q(app_label='data', model='dataset')
    data_content_type = models.ForeignKey(ContentType, limit_choices_to=data_limit, related_name='related_data')
    data_object_id = models.PositiveIntegerField()
    data_content_object = GenericForeignKey('data_content_type', 'data_object_id')

    publications_limit = models.Q(app_label='publication', model='publication') | \
        models.Q(app_label='publication', model='publicationset')
    publications_content_type = models.ForeignKey(ContentType, limit_choices_to=publications_limit, related_name='related_publications')
    publications_object_id = models.PositiveIntegerField()
    publications_content_object = GenericForeignKey('publications_content_type', 'publications_object_id')

    def __str__(self):
        return "{}: {} ⟷ {}: {}".format(
            self.data_content_type.name, self.data_content_object,
            self.publications_content_type.name, self.publications_content_object)
