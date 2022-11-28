from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
import main


class AddClientForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


class CreateProductForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    categories = QuerySelectMultipleField(
        query_factory=main.Category.query.all, allow_blank=False, get_label='name', get_pk=lambda obj: str(obj)
    )


class CreateStockForm(FlaskForm):
    quantity = IntegerField('quantity', validators=[DataRequired()])
    product_id = QuerySelectField(
        query_factory=main.Product.query.all, allow_blank=True, get_label='name', get_pk=lambda obj: str(obj)
    )


class CreateCategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
