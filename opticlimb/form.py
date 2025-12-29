import sqlalchemy as sa

from wtforms import FieldList
from wtforms import Form
from wtforms import FormField
from wtforms import SelectField

from .model import OpticlimbRecord

def criteria_form(model):
    """
    Create a form of a list of conditions from a database model.
    """
    mapper = sa.inspect(model)

    type_name = f'{model.__name__}ConditionForm'
    base_class = Form

    fields = {}
    fieldname_choices = []
    for prop in mapper.attrs.values():
        if getattr(prop, 'columns', None):
            column = prop.columns[0]
            if column.primary_key:
                continue
            label = column.info.get('label', None)
            fieldname_choices.append((prop.key, label))

    fields.update({
        'fieldname_select': SelectField(
            label = 'Field',
            choices = fieldname_choices,
        )
    })

    condition_form = type(type_name, (base_class, ), fields)

    criteria_form = type(f'{model.__name__}Criteria', (base_class, ), {'condition': FieldList(FormField(condition_form))})
    return criteria_form

OpticlimbRecordCriteria = criteria_form(OpticlimbRecord)
