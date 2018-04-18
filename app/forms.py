from flask import Flask

from wtforms import Form, StringField,TextAreaField,PasswordField, validators, SelectField, SelectMultipleField,widgets, RadioField

from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, InputRequired


ingredients_list = [
    'Chicken Stock', 'Carrots', 'Potatoes', 'Peas', 'Heavy Cream', 'Modified Food Starch', 'Wheat Flour', 'Salt', 'Chicken Fat', 'Dried Dairy Blend','Whey', 'Calcium Caseinate', 
    'Butter','Cream', 'Natural Flavoring', 'Maltodextrin', 'Milk Solids', 'Nonfat Dry Milk', 'Chicken Fat', 'Beef Extract', 'Ascorbic Acid', 'Monosodium Glutamate', 'Liquid Margarine',
    'Vegetable Oil Blend','Liquid Soybean', 'Hydrogenated Cottonseed', 'Hydrogenated Soybean', 'Water', 'Vegetable Mono And Diglycerides', 'Beta Carotene','Roasted Garlic Juice Flavor'
    'Garlic Juice', 'Gelatin', 'Roasted Onion Juice Flavor','Onion Juice', 'Hydrolyzed Corn', 'Soy', 'Wheat Gluten Protein','Vegetable Stock','Celery', 'Maltodextrin', 'Partially Hydrogenated Soybean Oil',
    'Dextrose', 'Chicken Broth', 'Chicken Stock', 'Sugar', 'Mono','Diglycerides', 'Citric Acid', 'Spice', 'Seasoning','Oleoresin Turmeric', 'Spice Extractives','Parsley','Caramel Color',
    'Yellow','Enriched Flour','Bleached Wheat Flour','Niacin', 'Ferrous Sulfate', 'Thiamin Mononitrate', 'Riboflavin', 'Folic Acid', 'Hydrogenated Palm Kernel Oil','Nonfat Milk',
    'Dough Conditioner', 'L-Cysteine Hydrochloride', 'Potassium Sorbate', 'Sodium Benzoate','Garlic Powder', 'Corn Syrup Solids','Anti Caking Agent','Rice','Paprika','Hot Sauce','Shrimp',
    'Steak','Milk','Cinamon Powder','Vanilla','bluberry','strawberry','Apple','Apricot','Avocado','Banana','Bilberry','Blackberry','Blackcurrant','Boysenberry','Buddha','Crab apples','Currant','Cherry','Cherimoya','Chico fruit',
    'Cloudberry','Coconut','Cranberry','Cucumber','Custard apple','Damson','Date','Dragonfruit','Durian','Elderberry','Feijoa','Fig','Goji berry','Gooseberry','Grape','Raisin','Grapefruit',
    'Guava','Honeyberry','Huckleberry','Jabuticaba','Jackfruit','Jambul','Jujube','Juniper berry','Kiwano horned melon)','Kiwifruit','Kumquat','Lemon','Lime','Loquat','Longan','skellion','black pepper'
    
    ]











class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegisterForm(Form):
    lastname = StringField('Last Name',validators=[InputRequired()])
    firstname = StringField('First Name',validators=[InputRequired()])
    email = StringField('Email',validators=[InputRequired()])
    username =StringField('Username',[validators.Length(min=4,max=25)])
    phonenumber = StringField('Number',validators=[InputRequired()])
    preferedmeal = StringField('Preferred Meal')
    city = StringField('City', validators =[InputRequired()])
    street = StringField('Street', validators=[InputRequired()])
    password = PasswordField('Password',[validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    
class RecipeForm(Form):
    name = StringField('Name',validators=[InputRequired()])
    instructions = TextAreaField('Instructions',validators=[InputRequired()])
    
class SearchForm(Form):
    searchtext = StringField('',validators=[InputRequired()])
    
    
class IngredientsForm(Form):
    
    ingredients = MultiCheckboxField('Ingredients', choices=[('Chicken Stock','Chicken Stock'),( 'Carrots', 'Carrots'),('Potatoes','Potatoes'),('Peas','Potatoes'),('Heavy Cream','Heavy Cream'),('Modified Food Starch','Modified Food Starch') ])
        
    
class TracklistForm(Form):
    ingredients = RadioField ('', choices=[('Sufficient in Stock','Sufficient in Stock'), ('Low in Stock','Low in Stock')])
