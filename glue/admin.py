from django.contrib import admin

from genericadmin.admin import GenericAdminModelAdmin, GenericTabularInline

from .models import (DataPublicationsRelationship, DataScientistsRelationship,
    PublicationsScientistsRelationship)


######################################################
# RELATIONSHIPS FOR GENERATED ADMIN & INLINE CLASSES #
######################################################
# For example, ('data', 'publications') yields:      #
# - DataToPublicationsRelationshipInline             #
# - PublicationsToDataRelationshipInline             #
# - DataPublicationsAdmin                            #
######################################################


relationships = [
    ('data', 'publications'),
    ('data', 'scientists'),
    ('publications', 'scientists'),
]


###################################
# ADMIN & INLINE CLASS GENERATORS #
###################################


def generate_tabular_inline_model(relationship):
    """
    Generates a tabular inline model from a relationship tuple.

    Usage:
        generate_tabular_inline_model(('data', 'publications'))

    Equivalent To:
        class DataToPublicationsRelationshipInline(GenericTabularInline):
            model = DataPublicationsRelationship
            ct_field = 'data_content_type'
            ct_fk_field = 'data_object_id'
            ordering = ['publications_content_type']
    """
    content_1, content_2 = relationship
    klass_name = '{}To{}RelationshipInline'.format(content_1.capitalize(), content_2.capitalize())
    klass = type(
        klass_name,
        (GenericTabularInline,),
        {
            'ct_field': '{}_content_type'.format(content_1.lower()),
            'ct_fk_field': '{}_object_id'.format(content_1.lower()),
            'ordering': ['{}_content_type'.format(content_2.lower())],
            'model': eval('{}{}Relationship'.format(*sorted(map(lambda x: x.capitalize(), r)))),
            '__module__': __name__,
        }
    )
    globals()[klass_name] = klass

def generate_and_register_admin_model(relationship):
    """
    Generates and registers an admin model from a relationship tuple.

    Usage:
        generate_and_register_admin_model(('data', 'publications'))

    Equivalent To:
        class DataPublicationsAdmin(GenericAdminModelAdmin):
            pass
        admin.site.register(DataPublicationsRelationship, DataPublicationsAdmin)
    """
    content_1, content_2 = sorted(map(lambda x: x.capitalize(), relationship))
    klass_name = ''.format(content_1, content_2)
    klass = type(
        klass_name,
        (GenericAdminModelAdmin,),
        {
            '__module__': __name__,
        }
    )
    globals()[klass_name] = klass

    model = eval('{}{}Relationship'.format(content_1, content_2))
    admin.site.register(model, klass_name)


####################
# GENERATE CLASSES #
####################


for r in relationships:
    generate_tabular_inline_model(sorted(r))
    generate_tabular_inline_model(sorted(r, reverse=True))
    generate_and_register_admin_model(r)
