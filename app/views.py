from flask import Flask, render_template,flash, redirect,request,url_for,session,logging,send_from_directory
from app import app
#from data import Recipes
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from forms import RegisterForm
from functools import wraps
from faker import Faker
from forms import RecipeForm, SearchForm, IngredientsForm,TracklistForm
import random
from random import shuffle

bcrypt = Bcrypt(app)
mysql = MySQL(app)
fake = Faker()

fake.seed(20000900)
val = fake.name()
#Recipes = Recipes()

recipe_n=[
    
'Acorn Squash and Pear Soup','Affogato','Almond Malted Brittle Bars','Alphabet Soup','Amaretto Biscotti','American Chop Suey','Anchovy-Crusted Pork Loin','Antipasto Salad','Apple and Cheddar',
'Baked French Toast','Apple Buttermilk Waffles with Apple Bourbon Sauce','Apple Chai Cupcakes','Apple Chunkies','Apple Cider Doughnut Holes','Apple Cider Poke Pound Cake','Apple Cranberry'
'Egg Rolls','Apple Crisp','Apple Doughnut Bombs','Apple Ginger Kombucha Cocktail','Apple Harvest Squares','Apple Pandowdy','Apple Pear Compote','Apple Streusel Bread','Apple Topped Cake','Apple Zucchini Crumb Bars',
'Apple-Stuffed Acorn Squash','Asiago Potato Stacks','Asian Barbecue Chicken Wings','Asian Barbecue Pork Ribs','Asian Barbecue Sauce','Asian Burgers','Asian Chicken Salad','Asian Chicken Soup','Asian Chicken Stock','Asian Citrus Vinaigrette',
'Asian Noodle Salad with Chicken','Asian Noodle Soup','Asian Salad with Roasted Delicata Squash','Asian Spice Apple Egg Rolls','Asparagus Lemon Risotto','Asparagus with Lemon and Feta',
'Atlantic Beach Pie','Autumn Cape Codder','Autumn Pork Stew','Avocado Chicken Pasta Salad','Avocado Poppy Seed Dressing','Avocado Rye Canapes''Avocado, Corn and Tomato Salad','Bacon and Blue Cheese',
'Stuffed Burgers','Bacon and Hash Browns Breakfast Bread','Bacon Cheeseburger Dip','Bacon Topped Cornbread','Bacon-Wrapped Gulf Shrimp with Blue Cheese Butter and Port Reduction','Baconnaise',
'Baked Apple and Cheddar Purses','Baked Brie','Baked Brie with Mostarda','Baked Chicken Salad','Baked Chicken Taquitos','Baked Cod with Boursin','Baked Crusted Salmon','Baked Fig Crostini',
'Baked Gnocchi with Italian Sausage','Baked Haddock with Cashew Cracker Crust','Baked Jalapeno Poppers','Baked Manicotti with Turkey Sausage''Baked Stuffed Parmesan Tomatoes','Baked Stuffed Shrimp','Baked Tilapia with Quinoa and Garlicky Green Beans',
'Baked Tortellini with Chicken Gratinati','Baked Winter Squash and Apple Casserole with Crispy Topping','Baked Zucchini Fries','Banana Chocolate Chip Granola Muffins',
'Banana Chocolate Chip Sheet Cake with Cream Cheese Frosting', 'Bang Bang Shrimp','Barbecue Chicken Wings',"Basil Chicken in Coconut-Curry Sauce","Beans and Rice","Beef and Bean Enchiladas","Beef and Guinness Casserole with Noodles",
"Beef Chimichangas","Beef Crostini with Horseradish Spread","Beef Goulash Soup","Beef Short Ribs Gravy","Beef Soup Series Part 1: Brown Stock","Beef Soup Series  Part 2: Beef and Barley Soup",
"Beef Soup Series Part 3: Hearty Beef Vegetable Soup","Beef Stew with Dumplings","Beef Stroganoff","Beef Teriyaki and Vegetables","Beef Tostadas","Beer Braised Barbecue Pork Butt",
"Best Apple Cake Ever","Best Ever Banana Bread","Best Leftover Ham Recipes","Bigos Polish Hunters Stew","Biscoff Crunch Ice Cream Cake","Black Garlic Bulgogi Beef Crostini","Blackened Tilapia Soft Tacos",
"BLT Crostini with Boursin Cheese","BLT Panzanella","BLT Ranch Rollups & Baked Spinach and Chicken DipFavorite Family Night Foods","Blue Cheese Aioli","Blue Cheese Coleslaw","Blue Cheese Dressing",
"Blue Hubbard Squash and White Bean Soup","Blue Moon Chicken","Blueberry Buckle","Blueberry Cream Cheese Muffins","Blueberry Ginger Lemon Scones","Bog Hollow Cranberry Brownies",
"Bolognese","Boozy Guinness Cupcakes","Boston Baked Beans","Bourbon Barbecue Sauce","Bourbon Poached Peaches","Bourbon Spice Barbecue Chicken Wings","Bourbon Truffles","Boursin Cheese",
"Braised Beef and Tortelloni","Braised Beef Over Egg Noodles","Braised Cabbage and Apples","Braised Chicken Limoncello with Green Beans","Braised Mustard Carrots","Bratwurst and Sauerkraut",
"Breakfast Burritos","Brew Moon Chocolate Pudding","Broccoli and Bacon Salad","Broccoli Rabe","Brodo","Brown Sugar Cookies","Brownie Sundae with Baileys Sauce","Brussels Sprouts and Bacon Pizza",
"Brussels Sprouts with Sweet Chili Sauce","Bubble and Squeak with Ham","Buffalo Chicken Arancini","Buffalo Chicken Dip","Buffalo Chicken Nachos","Buffalo Chicken Pizza",
"BulgogiKorean Beef Barbecue","Butter Chicken Panini","Buttermilk Corn Muffins","Butternut Squash and Chicken Chowder","Butternut Squash and Sausage Chili","Butternut Squash Parmesan with Linguine",
"Butternut Squash Pasta Sauce","Butternut Squash Puree","Butternut Squash Risotto","Butternut Squash with Rainbow Quinoa","Cacio e Pepe Spaghetti Squash","Caesar Salad with Grilled Caesar Chicken",
"Candied Cashews","Caponata","Caprese Salad","Cara Cara Beet Salad","Caramelized Onion Dip","Caramelized Pineapple Topping","Carb-Conscious Deli Lunch Spread","Carnitas","Carrot and Ginger Soup",
"Carrot Cupcakes with Ginger-Orange Cream Cheese Frosting","Carrot Salad","Carrots with Herbes de Provence","Cashew Cookie Balls","Cashew Cranberry Crunch Muffins",
"Cashew Frosted Brownies","Cashew Milk","Cassata RicottaSponge Cake with Ricotta","Catalina Dressing","Cauliflower Puree","Cemita Pulled Pork Pizza",
"Ceviche Salmon and Peas on Triscuit Crackers","Chai Coconut Chicken Strips","Chai Sugar Cookie Squares","Chai Tea Smoothie","Champagne Cosmos","Cheddar Beer Soup","Cheddar Topped Shepherds Pie",
"Cheeseburger Pie","Cheesesteak Egg Rolls","Cheesy Baked Stuffed Cod","Cheesy Smoked Sausage Skillet","Chefs Salad","Cherry Granola","Chesapeake Salsa",
"Chick Pea and Green Bean Salad", "Chicken alla Boscaiola," "Chicken and Apples in Honey Mustard Sauce", "Chicken and Linguica Sheet Pan Dinner", "Chicken Bellagio", "Chicken Breasts with Mushroom and Onion Dijon Sauce", "Chicken Broccoli Pasta Bake",
"Chicken Cacciatore", "Chicken Cakes", "Chicken Carbonara", "Chicken Chimichangas", "Chicken Cordon Bleu" "Chicken Cordon Bleu Sliders" "Chicken Corn Chowder", "Chicken Enchiladas with White Sauce", "Chicken Escalope with Mushroom Sauce", "Chicken in Pepitoria SaucePollo en Pepitoria", "Chicken Liver Pate", "Chicken Marbella", "Chicken Marsala", "Chicken Noodle SoupNew York Penicillin", "Chicken Parmesan", "Chicken Pepper Bacon Melts", "Chicken Piccata", "Chicken Pizzaiola", "Chicken Stock",
"Chicken Tender Saute", "Chicken Thighs with Mushrooms, Lemon and Herbs", "Chicken with Pignoli Crust", "Chicken with Sage Dumplings", "Chicken with Sweet and Sour Plum Sauce", "Chicken with Vindaloo Spices", "Chile con Queso", "Chili Cheese Enchiladas",
"Chili Dip", "Chili Lime Steak Bites", "Chimichurri", "Chinese Fried Walnuts", "Chocolate Almond Biscotti", "Chocolate Banana SmoothieVegan and Gluten Free", "Chocolate Bourbon Pecan Pie", "Chocolate Chip Caramel Crumble Bars", "Chocolate Chip Cookie Dough Bars", "Chocolate Chip Scones", "Chocolate Chocolate Chip Zucchini Muffins", "Chocolate Cookie Candy Pretzel Bark", "Chocolate Crunch Squares", "Chocolate Crunch Strawberry Ice Cream Cake", "Chocolate Dipped Almond Fingers", "Chocolate Malted Crinkles",
"Chocolate Malted Ice Cream", "Chocolate Malted Mousse", "Chocolate Mint Sugar Wafers", "Chocolate Nutella Toffee Icebox Cake", "Chocolate Peanut Butter Cheesecake Bites", "Chocolate Peanut Butter Cupcakes", "Chocolate Peanut Butter Pie", "Chocolate Peppermint Milkshake", "Chocolate Ranger Cookies", "Chocolate-Bourbon Pecan Torte", "Chop Suey Cake", "Chopped Salad with Pasta", "Christmas Cornmeal Cookies", "Christmas Crunchies", "Christmas Pudding with Hard Sauce", "Christmas Rocks", "Cider Glazed Bone-in Pork Roast with Apple Stuffing", "Cider Glazed Carrots", "Cinnamon Chip Biscotti", "Cinnamon Raisin English Muffins", "Cinnamon Raisin Swirl Babka", "Cinnamon Roll Bread Pudding with Bourbon Sauce", "Cinnamon Rolls with Bourbon-Soaked Raisins", "Cioppino", "Citrus Chicken and Rice Soup", "Citrus Grilled Chicken", "Classic Buffalo Wings", "Classic Cheesecake", "Classic Egg Salad", "Classic Lasagna", "Classic Stuffed Peppers", "Cocktail Sauce", "Coconut Rice", "Coconut Shrimp", 
"CoconutSnowball Cookies", "Cod Fish Cakes", "Coffee and Donuts Ice Cream", "Coffee Nut Brittle", "Colcannon", "Cold Veggie Pizza", "Coleslaw", "Condensed Cream of Chicken Soup", "Condensed Cream of Mushroom Soup", "Condensed Milk Pound Cake", 
"Confetti ChickenTacos", "Confetti Corn", "Copycat Entenmanns Chocolate Chip Cookies", "Copycat Kraft Macaroni and Cheese", "Copycat NewBridge Cafe Red Wine Vinaigrette", "Copycat Willow Tree Chicken Salad", "Corn and Bacon Casserole", "Corn Chip Chili Bowl", "Cornbread",
"Cornbread and Sausage Stuffing", "Cornbread Fries with Honey-Sage Dipping Sauce", "Cornbread Sausage Stuffing", "Corned Beef Breakfast Hash", "Country Baked Chicken", "Couscous with Lentils and Vegetables", "Crab Cakes", "Crab Imperial with Crostini",
"Crab Rangoon", "Craisins Pistachio Dark Chocolate Clusters", "Cranberry Almond Coconut Macaroons", "Cranberry Apple Clafoutis", "Cranberry Barbecue Sauce", "Cranberry Barbecue Turkey Pizza", "Cranberry Buffalo Wings", 
"Cranberry Ginger Upside Down Cakewith Rum Whipped Cream", "Cranberry Orange Relish", "Cranberry Orange Scones", "Cranberry Orange Sorbet", "Cranberry Pistachio Biscotti", "Cranberry Sauce", "Cranberry Squash Dinner Rolls", "Cranberry Walnut Oatmeal Cookies", "Cranberry Walnut Tart",
"Cream Cheese Crumb Bars", "Cream Cheese Muffins", "Cream Cheese, Scallion and Bacon RITZwich", "Cream of Turkey Soup", "Cream of Turkey Soup with Fennel and Apple", "Creamed Salmon and Peas Over Linguini", "Creamed Spinach", "Creamed Turkey on Toast",
"Creamed Vidalia Onions in Pastry", "Creamy Cauliflower Chowder", "Creamy Chicken and Prosciutto Stuffed Shells", "Creamy Chicken and Rice Soup", "Creamy Chicken Queso Dip", "Creamy Horseradish Sauce", "Creamy Italian Dressing", 
"Creamy Italian Pasta Salad", "Creamy Melon Granita", "Creamy Polenta with Pancetta and Broccoli Rabe", "Creamy Pumpkin Pasta Bake", "Creamy Roasted Tomato Bacon Dip", "Creamy Summer Squash Casserole", "Creamy Tortellini and Chicken with Sun-Dried Tomatoes", 
"Creme Brulee(for Two", "Creme Fraiche", "Crispy Apple Crusted Pork Chops", "Crispy Asian Chicken Wings with Ginger-Lime Dipping Sauce", "Crispy Chocolate Biscoff Truffles", "Crispy Creamy Potato Pancakes", "Crispy Parmesan Chickpeas", 
"Crispy Pretzel Chicken with Parmesan Honey Mustard Sauce", "Crispy Zaletti Cookies", "Crumb Crusted Pork ChopsCopycat Shake n Bake", "Crunchie Munchie Cookies", "Crunchy Sweet and Salty Chicken", "Crunchy Vegetable Rice Bowl with Warm Peanut Sauce", "Crustless Coconut Custard Pie", "Crustless Ham and Cheddar Quiche", "Curried Rice Pilaf With Red Lentils", "Curried Turkey and Rice Soup", "D", "Deconstructed Stuffed Cabbage", "Deconstructed Stuffed Peppers", 
"Deluxe Toll House Mud Bars", "Deviled Eggs", "Dinner Party Series Part 1: Tuscan Kale Salad with Oranges, Currants and Feta", "Dinner Party Series Part 3: Herb Basted Salmon", "Dinner Party Series  Part 4 Almond Orange Cake", "Dinner Party Series Part 2 Roasted Root Vegetables", "Dinner Rolls", "Double Chocolate Pudding", "Dry Rub Spicy Barbecue Chicken Wings", "Duchess Sweet Potatoes", "E", "Easter Pie", "Easy Asian Slaw", "Easy Blender Chocolate Mousse", "Easy Brunch Egg Cups& Make-Your-Own Brunch Bar Ideas", "Easy Cheesy Potato Casserole", "Easy Chicken & Rice", "Easy Freezer Meatballs", "Easy Glazed Salmon", "Easy Italian Sausage and Potato Skillet", "Easy Meat Lovers Pizza", "Easy Napa Cabbage Slaw", "Easy No-Cook Pizza Sauce", "Easy Tortellini Soup", "Easy Zesty Cheese Dip", "Egg-Free Caesar Dressingand Marinade", "Eggnog Pancakes with Fresh Cranberry Syrup", "Eggplant and Garlic Pizza", "Eggplant Fries with Marinara Sauce", "Eggplant Parmesan", "Enchilada Sauce", 
"English-StyleFish and Chips", "Espresso Black Bottom Pie", "Espresso Martini", "Everyday Asian Dressing", "Everyday Steak Tips", "F", "Fall Fruit Pie", "Fall Harvest Vegetarian Corn and Butternut Chowder"
, "Farfalle with Zucchini and Sun Gold Tomato Sauce", "Farm Box Vegetable Egg Rolls", "Farro Salad with Grapes, Goat Cheese and Tarragon Vinaigrette", "Farro with Butternut Squash and Baby Kale", "Favorite Vinaigrette", "Fennel and Apple Slaw", "Festive JELL-O Popcorn Balls", "Festive Pineapple Cranberry Punchand Ice Ring", "Fettuccine in Cream, Tomato & Basil Sauce", "Fiesta Style Cranberry Sauce", "Fig Bar Cookies", "Filet Mignon with Mushroom Sauce", "Filipino Beans and Rice", "Filipino Picadillo", "Fire Roasted Tomato and Barley Risotto", "Fish Tacos", "Flaxseed Twisty Sticks", "Flour Bakerys Chunky Lola Cookies", "Flourless Peanut Butter Cookies with Sea Salt", "Focaccia", "Forbidden Rice Pilaf", "French Dressing", "French Onion Soup", 
"Fresh Apple Torte", "Fresh Carrots with Butter and Dill", "Fresh Cherry and Spiced Rum Cocktail", "Fresh Cherry Sauce", "Fresh Pineapple Peach Smoothie", "Fresh Strawberry Yogurt Cake", "Fresh Tomato Au Gratin", "Fresh Vegetable Pasta Salad", "Fried Green Tomatoes", "Fried Manchego Cheese with Apricot-Sage Dipping Sauce", "Fruit and Cheese Ball", "Fruit and Cucumber Salsa", "Fruit and Nut Oatmeal Breakfast Cups", "Fusilli with CauliflowerFusilli con Cavolfiore", "G", "Garden Tomato Compote", "Garden Vegetable Ragout",
"Garden Vegetable Ratatouille", "Garlic Bread", "Garlic Lemon Shrimp with Savory Root Vegetable Rice Pilaf", "Garlicky Tuscan Kale", "Gazpacho", "Ginger Maple Sweet Potato Casserole", "Ginger Molasses Cookies with Cherry Cream Filling", "Ginger Peach Blueberry Ice Cream", "Giouvetsi", "Glazed Fig Salad with Prosciutto and Feta Cheese", "Glenns Sweet & Spicy Slow Cooker Chili", "Gluten Free Flat Bread", "Gluten Free Veggie Burgers", "Goat Cheese, Pesto and Sun-Dried Tomato Terrine", 
"Golden Crusted Baked Chicken", "Gooey Ginger Chicken", "Grampas Firehouse Chicken", "Grandma Gennacos Beef Braciole", "Granola Chocolate Chip Cookies", "Grape-Nuts Bread", "Grapenut Pudding with Fig Sauce", "Great Grains Chewy Breakfast Bars", "Greek Chicken Roulade",
"Greek Lemon Chicken Soup with Orzo", "Greek RiceSpanakorizo", "Greek Salad Dressing", "Greek Salad with Meat", "Greek Spinach with White Beans and Feta", "Greek Yogurt Panna Cotta", "Green Bean Casserole", "Green Beans Almondine", "Green Beans with Tarragon",
"Green Beans with Tomatoes", "Green Tomato Soup with Black Forest Ham", "Grilled Balsamic Peaches", "Grilled Bananas and Pineapple with Rum-Molasses Glaze", "Grilled Basil Garlic Chicken Breasts", "Grilled Beef Patties with Mediterranean SalsaWhole30", "Grilled Chicken Calzones", "Grilled Chicken Club with Rosemary Aioli", "Grilled Chicken Skewers with Thai Chili Peanut Sauce", "Grilled Chicken with Roasted Vegetables and Whole Wheat Couscous", "Grilled Corn and Tomato Salsa", 
"Grilled Corn on the Cob with Roasted Red Pepper Butter", "Grilled Graffiti Eggplant", "Grilled Italian Vegetable Napoleons with Basil Oil", "Grilled Kielbasa Rolls with White Barbecue Sauce", "Grilled Marinated Chicken with Tropical Salsa", "Grilled Pineapple Salsa",
"Grilled Polenta with Bacon Jam", "Grilled Pork Chops with Grilled Vegetable Medley", "Grilled Pound Cake with Vanilla Custard and Fresh Berries", "Grilled Romaine Hearts and Pears with Bleu Cheese", "Grilled Seasonal Vegetables with Infused Oils", 
"Grilled Southwest Burger", "Grilled Steak and Corn Salad", "Grilled Stone Fruit with Mascarpone and Cherry Granola", "Grilled Summer Vegetable Salad", "Grilled Sweet Potato Salad with Sweet and Sour Bacon Dressing", "Grilled Tropical Fruit Salad with Prosciutto",
"Grilled Vegetable Salad with Basil Dressing", "Grilled Vegetable Tostadas", "Grilled Watermelon Bites", "Grilled Yellow Potatoes with Mustard Sauce", "Grilled Zucchini Salad", "Ground Beef Tacos", "Guacamole", "Guinness Barbecue Sauce", 
"Guinness Barbecued Pork Tips", "H", "Halal Cart-Style Chicken and Rice with White Yogurt Sauce", "Halloween Thumbprint Cookies", "HaluskiFried Cabbage and Noodles", "Ham and Cheese Breakfast Casserole", "Ham and Swiss Quiche", "Ham and Vegetable Soup", "Ham Salad", 
"Hamburger Cheese Bake", "Hamburger Soup", "Harissa", "Hartford Election Cake", "Harvard Beets", "Hash Brown Crusted Salmon", "Hash Browns Breakfast Stacks", "Hawaiian French Toast with Pineapple and Mascarpone", "Hazelnut Affogato", "Hazelnut Truffles",
"Healthy Golden Flax Breakfast Cookies", "Healthy Whole Wheat Muffins", "Hearty Vegetable Soup", "Herb Crusted Grilled Pork Tenderloin with Crispy Shallots", "Herb-Infused Oil", "Herbed Boiled Potatoes", "Herbed Tomatoes", "Hermits", "Holiday Chicken Soup",
"Homemade Baking Mix", "Homemade Ketchup", "Homemade Magic Shell", "Homemade Mayonnaise", "Homemade Multigrain Cereal", "Homemade Nutella", "Homemade Steak Sauce", "Homemade Tater Tots", "Homemade Tomato Juice",
"Honey Butter", "Honey Dijon Ranch Dressing", "Honey Mustard Soy Glazed Chicken Wings", "Honeydew Melon Smoothie", "Hoppin John with Kale", "Horchata", "Hot Crab Dip with Crostini", "Hot Fudge Pudding Cake", "Hummus with Caramelized Cauliflower and Onions",
"Hungry Grilled Romaine Salad", "I", "Iced Gingerbread Cookies ", "Indian Pudding", "Individual Beef Pot Pies", "Instant Pot Beef and Noodles", "Instant Pot Country Chicken", "Israeli Couscous Salad with Mediterranean Roastedm Vegetables", "Israeli Couscous with Chicken and Peas", "Its Peanut Butter Jelly Time With Recipes", "Italian Anisette Cookies", "Italian Carrots", "Italian Cheesy Bread", "Italian Chicken Soup with Meatballs and Escarole", "Italian Chili", 
"Italian Cold Cut Lasagna Rollups", "Italian Easter BreadPane di Pasqua", "Italian Fish Chowder", "Italian Fish Stew", "Italian Ricotta Pie", "Italian Sausage and Eggplant Tailgate Dip", "Italian Sausage and Rice Dressing with Kale and Cranberries", 
"Italian Sausage Sub with Toasted Fennel Aioli", "Italian Tomato Sauce", "Italian Tortellini Salad", "Italian Zucchini Bread", "Italian-Style Meatballs", "J", "Jacks Apple Pudding", "Jacks Chili", "Jacks Meatloaf With Gravy", "Jacks Potato Salad", 
"Jones Scrapple Cornbread Stuffing", "Jordan Pond Popovers", "K", "Kale and Shiitake Mushroom Soup with Ginger Sesame Lavash Crackers", "Kale Apple Walnut Salad", "Kale Puttanesca", "KapustaPolish Cabbage Soup", "Kathys Chocolate Chocolate Chip Cake", "Key Lime Ice Cream with Graham Cracker Pistachio Crumb Topping", "Key Lime Torte", "Kielbasa and Pineapple Spiced Candy", "Kielbasa and Red Cabbage Skillet with Apples", "Kielbasa Reuben", "Kofta", "Korean Barbecue Chicken Wings", "Korean-Style Kimchi Gochujang Chicken Wings", "Korean-Style Marinated Cucumbers", "L", "Lamb and Eggplant Crostini with Salad", "Lamb Shepherds Pie", "Lamb, Tomato and Barley Soup", "Lazanki with Mushrooms and Beef", "Lemon Almond Tea Cookies", "Lemon Bars", 
"Lemon Blueberry Cream Pie", "Lemon Blueberry Zucchini Muffins", "Lemon Buttermilk Sorbet", "Lemon Curd", "Lemon Dill Compound Butter", "Lemon Ginger Poppy Seed Biscotti", "Lemon Iced Tea Loaf", "Lemon Loaf Cake  Kid Chef Bakes Cookbook Giveaway", "Lemon Meringue Pie", 
 "Lemon Mousse Cups", "Lemon Oreo Cheesecake Bars", "Lemon Pasta", "Lemon Ricotta Pancakes", "Lemon Rosemary Chicken", "Lemon Star Cookies", "Lemon Sugar Cookies", "Lemon-Ginger Broccoli",
"Lemon-Glazed Swordfish Skewers Over Rice", "Lentils with Brown Rice and Feta", "Lidias Rice and Zucchini Crostata", "Lime and Coriander Tofu Mayonnaise", "Linguine with Sun Dried Tomatoes and Brie", "Linguine with White Clam Sauce", 
"Linguini with Clam Sauce  Basque-Style", "Littlenecks in Fennel Broth", "Loaded Baked Potato Soup", "Loaded Chocolate Covered Rice Krispie Bars", "Loaded Italian Sub with Roasted Red Pepper Aioli", "Loaded Mashed Potato Casserole", "Loaded Pub Fries", "Lobster Corn Chowder",
"Lobster Mac and Cheese", "Lobster Sambuca Over Fettuccini", "Low Carb Pancakes with Blueberry Sauce", "M", "Mac and Cheese Cupcakes", "Macaroni and Cheese with Roasted Tomatoes", "Macaroni Salad", "Malted Chocolate Buttermilk Pie", "Malted Mocha Bars",
"Malted Mocha Swiss Roll", "Malted Mousse Cake", "Mandarin Marmalade", "Mandarin Pork Tenderloin Medallions", "Mango Orange Lassi", "Mango Yogurt Mousse", "Maple Cider Glazed Turkey", "Maple Sage Roasted Delicata Squash", "Maple Streusel Muffins", 
"Margarita Shrimp with Rice", "Margarita Skirt Steak", "Margaritas", "Marinara Sauce", "Marinated Green Beans with Cilantro and Garlic", "Marinated Grilled Chicken", "Marinated Mushrooms", "Marinated Spiced Carrot Salad", 
"Mario Batalis Green BeansFagiolini in Padella", "Marshmallow Crisp Milkshake", "Marthas Meatloaf", "Mascarpone Strawberry Stuffed French Toast", "Mashed Cauliflower and Spinach", "Mashed Sweet Potatoes with Kale and Boursin Cheese", "Massaged Kale", "Matunuck Oyster Bar Stew", 
"Meal Planning and Meal Prepping", "Meat Lovers Dr Pepper Baked Beans", "Meat Lovers Manicotti Stracotto-Style", "Meatball Subs", "Mediterranean Flatbread", "Mediterranean Grilled Chicken", "Mediterranean Haddock", "Mediterranean Israeli Couscous Salad", 
"Mediterranean Nachos", "Mediterranean Pasta Primavera", "Mediterranean Pasta Salad", "Melon Balls with Poppy Seed Dressing", "Mexican Bread Pudding", "Mexican Brownies", "Mexican Corn Salad", "Mexican Hot Fudge Pudding Cake", "Mexican Lasagna with White Sauce", 
"Mexican Pulled Chicken", "Mexican Rice", "Mexican Shredded Beef", "Milk Braised Pulled Pork with Mushrooms", "Milk Streets Sweet and Spicy Ginger Green Beans", "Milky Way Bites Ice Cream ", "Minestrone", "Mini Pumpkin Pies", 
"Mini Shepherds Pie Bites", "Mini Stuffed Sweet Peppers", "Miso Butter", "Miso Fried Rice", "Mississippi Sin Ham Sliders", "Mixed Berry Buckle", "Mixed Berry Cobbler", "Mixed Berry Muffins", "Mixed Greens with Pears, Goat Cheese, Dried Cranberries and Spiced Pecans", 
"Mixed Greens with Prosciutto and Cantaloupe", "Mocha Bread Pudding", "Mocha Cupcakes", "Mock Apple Crumb PieMade with Zucchini", "Moo Shu Beef Lettuce Cups", "Morning Glory Muffins", "Moscows", "Mostarda", "Mozelles Barbecue Sauce", "Mujadarra", 
"Mushroom Ragout", "Mushroom Risotto", "Myles Standish Sandwich", "N", "Name That Cheeseburger The Peppercorn Pileup", "Nannys Black Midnight Cake", "Nannys Italian Stuffed Peppers", "Nannys Rum Raisin Sugar Cookies", "Nantucket Corn Pudding", "Nautical Mary",
"Needhams Maines Famous Potato Candy", "New England Apple Cider Cake", "New England Boiled DinnerCorned Beef and Cabbage", "New England Clam Chowder", "New England Fish Fry", "New England Lobster Roll", "New England Pumpkin Caramel Pudding", 
"No Bake Nutella Almond Cheesecake", "No-Bake Amaretto Truffles", "No-Bake Chocolate Cheesecake Pie", "No-Bake Chocolate Oatmeal Cookies", "No-Bake Mini Pumpkin Cheesecakes", "No-Bake Peach Cheesecake Mousse", "No-Bake White Chocolate Peppermint Cheesecakes",
"No-Churn Cinnamon Ice Cream", "No-Churn Peppermint Chip Ice Cream", "No-Cook Puttanesca Sauce Over Pasta", "Noodle Kugel", "Noodles Romanoff with Mushrooms", "Nourishing RiceArroz de Sustancia", "Nutella Crunch Ice Cream Cake", "O", 
"Oat Buttermilk Waffles with Mango-Fig Spread", "Oatmeal Apple Scones", "Oatmeal Cranberry Cheesecake Bars", "Oatmeal Raisin Ice Cream", "Oatmeal Snickerdoodles", "Oatmeal Stout Beef Pot Pie", "Olive Dipping Sauce", "Olive Oil & Herb Savory Biscotti", 
"One Pot Pasta and Chicken with Spinach", "One Pot Tex-Mex Pasta", "Onion Jam Crostini with Herbed Goat Cheese", "Onion Rings", "Orange Almond Biscotti", "Orange and Ginger Cookies with Chocolate Drizzle", "Orange Chicken and Vegetables", "Orange Chicken Roasted Spatchcock-Style",
"Orange Poppy Seed Cake", "Orange Ricotta Cookies", "Orange Sugared Cranberries", "Orange Zucchini Cookies", "Orzo with Mushrooms, Scallions and Parmesan", "Our American Kitchen Memories & Our Favorite Family Recipes", "Our Christmas Family Feast",
"Our DoAC Atlantic City Food Tour", "Our Favorite Milk, Cream, Yogurt and Cheese Recipes", "Our Kitchen Makeover After", "Our Kitchen Makeover Appliance Research & Inspiration", "Our Kitchen Makeover Before", "Our Kitchen Makeover New Hardwood Floors",
"Our Thanksgiving Family Feast", "Oven Fried Rosemary Chicken", "Oven Roasted Brussels Sprouts with Bacon", "Oven Roasted Brussels Sprouts with Lemon Aioli", "Oven Roasted Brussels Sprouts with Mustard and Shallots", "Oven Roasted Cauliflower with Crunchy Topping", "Oven Roasted Parmesan Cauliflower", "P", "Palm Springs Date Shake", "Pan Roasted Tomatoes with Herbs", "Pan Roasted Tomatoes with Quinoa", "Pan Seared Halibut with Mango-Avocado Salsa", "Panang Beef Curry", 
"Pane Siciliano Sesame Seed Sicilian bread", "Panettone Muffins", "Panna Cotta with Balsamic Strawberries", "Panzanella Bread Salad", "Pappa Al Pomodoro Bread and Tomato Soup", "Parker House Rolls", "Parmesan Chicken Cutlets", "Parmesan Chicken Nuggets", 
"Parmesan Peas with Pancetta and Shallots", "Parmesan Pull-Apart Rolls", "Parmesan Truffle Fries", "Parmesan-Coated Asparagus Wrapped In Prosciutto", "Parsnip and Celery Root Puree", "Pasta al Finocchio", "Pasta con Tonno", "Pasta Frolla Christmas Jam Cookies", "Pasta Luva with Gorgonzola", "Pasta Primavera", "Pasta Sauce Raphael", "Pasta with Arugula Cream Sauce", "Pasta with Pesto Cream Sauce", "Pasta with Yellow Pepper Sauce", "Pasta, Chicken & Asparagus in Garlic Tomato Sauce", "Pauls Thanksgiving Stuffing", "Peach Butter",
"Peaches and Cream Almond Crumb Tart", "Peanut Ginger Chicken", "Peanut Goodies", "Pear and Dark Chocolate Crisp", "Pear and Gorgonzola Pizza with Arugula and Ranch Dressing", "Pearl Onions in Cream Sauce", "Peas with Prosciutto", 
"Pegs Green TomatoSalsa", "Pepper Jack Potato Pancakes", "Pepper Pig Breakfast Sandwich", "Pepperidge Farm Milano Tiramisu", "Peppermint Hearts", "Peppery Peach Glazed Pork Tenderloin", "Peppery Peach Sauce", "Perdues Favorite Sweet and Smoky Chicken", "Perfect Asparagus",
"Perfect Herb Roasted Chicken", "Perfect Holiday Ham", "Perfect Macaroni and Cheese", "Perfect Mashed Potatoes", "Perfect Pan-Seared Scallops with a Simple Pan Sauce", "Perfect Pan-Seared Steak", "Perfect Pork Chops", "Perfect Pork Tenderloin", 
"PerfectPrime Rib", "Perfect Roast Turkey", "Perfect Turkey Gravy", "Pesto", "Pesto Chicken over Sauteed Cannellini Beans", "Petite Marmite", "Philly Cheesesteak Stuffed Peppers", "Pickled Golden Beets", "Pickled Peppers", "Pickled Red Onions", "Pico de Gallo",
"Pierogi", "Pineapple Lime Rickey Punch", "Pineapple Mango Mahi Mahi and Vegetables Over Rice", "Pineapple Mango Salsa", "Pineapple Raisin Sauce", "Pistachio Lemon Lime Shortbread Cookies", "Pizza Margherita with Roasted Tomato Pizza Sauce", "Poached Cod with Tarragon and Cherry Tomatoes", "Poached Pears in Red Wine with Vanilla Custard Sauce", "Polish Babka", "Polish Dill Pickle Soup", "Polish Hamburgers", "Polish-Style Steamed PEI Mussels", "POM Pomegranate Sherbet", "Pomfresca Cocktail", 
"Pomfresca Float", "Poppy Seed Chicken", "Pork and Apple Skewers With Orange Balsamic Glaze", "Pork Larb Lettuce Cups", "Pork Lomitos Tacos", "Pork Meatballs with Currants", "Pork Medallions Portuguese", "Pork Tenderloin Tips with Apricot Sauce", "Pork Tenderloin with Pomegranate Pan Sauce", "Pork Tenderloin with Strawberry-Plum Sauce and Herbed Biscuits", "Portuguese Kale Soup", "Portuguese Rice Pudding", "Portuguese Tomato Rice Arroz de Tomate", "Portuguese-Style Mussels in Garlic Cream Sauce", 
"Potato Rosemary Kaiser Rolls", "Potatoes Fontecchio", "Potatoes OBrien", "Poutine", "Poutine-Style Turkey, Gravy and Potatoes", "Praline Pumpkin Mousse", "Pretzel Cookies", "Prosciutto and Cheese Biscuits", "Prosciutto and Fig Pizza with Arugula", "Prosciutto Rolls",
"Prosciutto Wrapped Zucchini Over Melon Pasta", "Puff Pastry Bacon Twists", "Pulled Chicken Chilaquiles", "Pulled Chicken Tacos", "Pulled Pork with Bourbon Barbecue Sauce", "Pumpkin Cheesecake", "Pumpkin Corn Chowder", "Pumpkin Corn Fritters", "Pumpkin Corn Pudding", "Pumpkin Oatmeal Chocolate Chip Cookies", "Pumpkin Pancakes with Maple Pumpkin Butter", "Pumpkin Pecan Toffee Chip Cookies", "Pumpkin Spice Sugar Cookies", "Q", "Quick and Easy Chili", "Quick Skillet Chicken with Grapes",
"Quinoa Chicken and Vegetable Salad", "Quinoa Pilaf", "Quinoa Salad with Pecans, Orange and Currants", "Quinoa With Spinach, Artichokes and Chicken", "R", "Ranch Buffalo Chicken Meatloaf", "Ranch Chicken Chopped Salad", "Raspberry Fool", "Raspberry Melon Smoothie", 
"Ratatouille Bruschetta", "Red Potato Coins", "Red Velvet PEEPS Holiday Wreath Cake", "Red-Eye Burger", "REESES Dream Team Chocolate Peanut Butter Pie Pops", "Refried Beans", "Reuben Dip", "Rice Pilaf", "Rissole Potatoes Fresco", "Roasted Boneless Lamb with Red Wine Pan Sauce", "Roasted Butternut Squash and Swiss Chard", "Roasted Carrots and Parsnips", "Roasted Chicken with Rosemary Compound Butter", "Roasted Eggplant and White Bean Dip with Caraway Crackers", "Roasted Fennel and Onion Gratinati", "Roasted French-Style Potatoes", "Roasted Garlic Aioli", "Roasted Lamb London Broil-Style", "Roasted Mashed Sweet Potatoes", "Roasted Potato Soup", "Roasted Radishes and Root Vegetables", "Roasted Red Pepper Dipping Sauce", "Roasted Salmon with Tomato-Olive Relish", 
"Roasted Strawberries", "Roasted Strawberry Creme Fraiche Ice Cream", "Roasted Tomato Pizza Sauce", "Robin Egg Cheesecake Cookie Bars", "Rocket Fuel Homemade Hot Sauce", "Rocky Road Fudge Bites", "Roman Wedge Salad", "Rookie Cookies", "Ropa Vieja", "Rosemary Compound Butter", "Rosemary Flatbread", "Rotisserie Chicken Skillet", "Ruby Red Grapefruit and Cranberry Chicken", "Russian Dressing", "S", "Saffron Cauliflower Rice", "Saigon Cinnamon Ginger Cookies", "Salami & Cheddar Quiche", "Salisbury Steak",
"Salmon and Parsnip Chowder", "Salmon Egg Salad", "Salmon Hash with Poached Eggs", "Salmon with Zucchini and Spaghetti", "Salsa", "Salty Dog", "Sausage and Apple Empanadas", "Sausage and Broccoli Rabe Risotto", "Sausage and Pepper Calzone", "Sausage and Ricotta Pizza", "Sausage Bread", "Sausage Gravy Over Chicken Fried Steak", "Sausage Stuffed Mushrooms with Mascarpone", "Sausage Stuffed Zucchini", "Sausage Veggie Breakfast Bake", "Sauteed Beet Greens", "Sauteed Fresh Corn", "Sauteed Mushrooms with Bourbon",
"Sauteed Salmon with Rice and Tomatoes", "Savory Citrus Dressing", "Savory Fried Plantains", "Savory Soft Polenta", "Scallion Cream Cheese Bagel Spread", "Scallop Ceviche", "Scalloped Ham and Potato Casserole", "Scallops Alla Veneziana with Parmesan Toasts",
"Scarpaccia", "ScottigliaMixed Meat Stew", "Sea Scallops with Cipollini Onions and Pasta", "Seafood Salad", "Seared Beef with Cipolline Onions and Horseradish Dumplings", "Seasoned Hamburgers with Caramelized Onions", 
"Sesame Chicken Skewers with Sriracha-Soy Dipping Sauce", "Shakshuka", "Shaved Brussels Sprout Salad", "Shaved Brussels Sprouts with Bacon", "Shoo Fly Pie", "Shrimp Scampi", "Sicilian Twists Infasciadedde", "Simple Cucumber Salad", "Simple Red Wine Vinaigrette", 
"Skillet Goulash", "Skinny Creamy Chicken Enchiladas", "Skinny Marble Cheesecake", "Sloppy Joes", "Sloppy Tom Sandwich", "Slow Cooker Applesauce with Cranberries", "Slow Cooker Barbecue Beef Brisket", "Slow Cooker Beefy Mac", "Slow Cooker Chicken Tikka Masala",
"Slow Cooker Creamed Fresh Corn", "Slow Cooker Honey-Garlic Baby Back Ribs", "Slow Cooker Italian Beef Subs", "Slow Cooker Kalua Pulled Pork", "Slow Cooker Pulled Buffalo Chicken", "Slow Cooker Pumpkin Puree", 
"Slow Cooker Sourdough Stuffing with Turkey Sausage and Apples", "Slow Cooker Swiss Steak", "Slow Cooker Tex-Mex Chicken Stew", "Slow Cooker Tomato and Tortellini Soup", "Slow Cooker Tomato Crab Bisque", "Slow Cooker Tuscan White Bean Soup", "Small Batch Fig Jam", "Smoked Bluefish Pate", "Smoked Fish Chowder", "Smoked Ham with Butternut Squash over Noodles", "Smoky Joe", "Snowflake OREO Cookie Balls", "Soft Honey Sesame Pretzel Rolls", "Soft Pumpkin Chocolate Chip Cookies", "Sour Cream Coffee Cake Muffins", "Sour Cream Pudding Cake", 
"Sour Cream Streusel Coffeecake", "Southwest Tuna Salad Lettuce Boats", "Southwestern Breakfast Muffins", "Southwestern Cheesy Corn Dip", "Southwestern Rachel Sandwich with Southwestern Slaw Boars Head Boldest Bracket Challenge", "Southwestern Red Chile Sauce",
"Spaghetti allAmatriciana", "Spaghetti Squash Gremolata", "Spanish Rice", "Spanish-Style Garlic Shrimp Gambas al Ajillo", "Spatchcocked Grilled Turkey", "Spice Rub for Chicken", "Spiced Apple Coconut Muffins", "Spiced Eggnog Chocolate Chip Cake", "Spiced Eggnog Cocktail", "Spiced Pecans", "Spiced Rum Bundt Cake", "Spicy Cauliflower Au Gratin", "Spicy Grilled Peel and Eat Shrimp", "Spicy Thai Ketchup", "Spinach and Cheddar Quiche", "Spinach and Kale Gratin", "Spinach Salad with Warm Bacon Dressing", 
"Spinach Strawberry Salad with Strawberry Vinaigrette", "Spritz Cookies", "Star Spangled Fruit Salad", "Star Spangled Sugar Cookies", "Steak au Poivre with Crispy Shallots", "Steak Bites", "Steak Bomb Sandwich", "Steak Tips with Caramelized Onions", 
"Steel Cut Oatmeal Honey Bread", "Steel Cut Oats Breakfast Biscotti", "Stewed Tomatoes", "Stir Fry Salmon and Vegetables with Multi-Grain Medley", "Straw and Hay Paglia e Fieno", "Strawberries Romanoff", "Strawberry Brambles", "Strawberry Cheesecake Mousse", 
"Strawberry Cheesecake Streusel Muffins", "Strawberry Nutella Crumb Torte", "Strawberry Shortcake with Mini Angel Food Cakes", "Strawberry Torte", "Strawberry Vinegar", "Stuffed Crust Pizza Braid", "Stuffed Italian Frying Peppers", "Stuffed Meatballs", 
"Stuffed Nutella Cookies", "Stuffed Veal Sliders", "Sugar Cookie Bars", "Summer Salad with Goat Cheese-Filled Potato Cakes", "Summer Squash Spaghetti Ricotta Pie", "Summer Vegetable Torte", "Sunday Cooking Lesson How to Easily Cut Fresh Corn Kernels Off the Cob", "Sunday Cooking Lesson Bechamel Sauce", "Sunday Cooking Lesson Clarified Butter", "Sunday Cooking Lesson Homemade Croutons", "Sunday Cooking Lesson Homemade Ricotta Cheese", "Sunday Cooking Lesson How to Cut a Whole Chicken", "Sunday Cooking Lesson How to Grill Pizza", "Sunday Cooking Lesson How to Make a Taco Shell Bowl", "Sunday Cooking Lesson Perfect French Fries", "Sunday Cooking Lesson Perfect Hard-Boiled Eggs", "Sunday Cooking Lesson Perfect Pizza Dough", 
"Sunday Cooking Lesson Perfect Poached Chicken", "Sunday Gravy", "Sundried Tomato and Basil Cream Cheese Spread", "Swedish Meatballs over Noodles", "Sweet and Sour Balsamic Glazed Onions", "Sweet and Sour Chicken", "Sweet and Sour Glazed Pork Tenderloin", "Sweet and Sour Key Lime Pork", "Sweet and Sour Sauce", "Sweet and Sour Shrimp Stir-Fry", "Sweet and Spicy Cocktail Meatballs", "Sweet and Spicy Shrimp, Pineapple and Bacon Skewers", "Sweet and Tangy Cocktail Meatballs", "Sweet Bell Pepper Slaw With Pineapple", "Sweet Buttermilk Biscuits",
"Sweet Chili Dipping Sauce", "Sweet Corn Gelato", "Sweet Corn Soup", "Sweet Hot Mustard Sauce with Grilled Kielbasa", "Sweet Potato and Apple Cake", "Sweet Potato Cauliflower Mash", "Sweet Potato Pancakes", "Sweet Potato Risotto", 
"Sweet Potato Soup with Orange Creme Fraiche and Electrolux Immersion Blender Giveaway", "Sweet Potato Spinach and Bacon Turkey Burgers", "T", "Taco Salad", "Taco Sauce", "Tartar Sauce", "Teriyaki Sauce", "Texas Hash", "Texas Tornado Cake", "Thai Chili Peanut Sauce", "Thai Corn Salad", "Thai Iced Tea", "Thai Peanut Chicken Noodle Salad", "Thai Vegetable Dip", "Thanksgiving Casserole", "The Best Vanilla Ice Cream", "The Best Wild Rice", "The New England Pasty", "The Real Jordan Marsh Blueberry Muffins Recipe", 
"Three Cheese Baked Ziti With Meatballs and Sausage", "Three Mustard Chicken Fricassee", "Toffee Pecan Bundt Cake with Caramel Drizzle", "Toll House Chocolate Chip Cupcakes", "Toll House Chocolate Chip Pie", "Tomato Eggplant Gratin", "Tomato Jam", "Tomato Lentil Soup with Sausage", "Tomato Pickle Mix", "Tomato Pie", "Tomato Portobello Gratin", "Tomato Soup", "Tomato Tart with Smoked Gruyere and Cracked Black Pepper", "Top of the Round Roast", "Tortellini Salad with Roasted Vegetables", 
"Touchdown Mini Meatloaf and Buffalo Chicken Bites", "Tri-Color Cauliflower Salad", "Tuna Meatball Sub", "Turkey & Stuffing Turnovers", "Turkey and Gravy Savory Herbed Waffles", "Turkey Brine Recipe & Thanksgiving Menu Planning", "Turkey Cocktail Meatballs with Apple Mustard Glaze",
"Turkey Divan", "Turkey Kielbasa and Baby Kale Strata", "Turkey Meatball Soup with Orzo", "Turkey Meatballs with Cranberry Sweet & Sour Sauce", "Turkey Monte Cristo with Rosemary Aioli", "Turkey Pinwheel Bites", "Turkey Pot Pie", "Turkey Salad Sandwich",
"Turkey Salad with Cranberries and Toasted Pecans", "Turkey Soup with Potato Dumplings", "Turkey Stock", "Turkey Stracciatella Soup", "Turkey Tetrazzini", "Turkish Flatbread", "Tuscan Gilded Carrots", "Tuscan Roasted Potatoes", "Tuscan Stuffed Mushrooms",
"Tuscan Zucchini with Tomatoes, Garlic & Mint", "Tuscan-Style Beans", "Tuscan-Style Roasted Carrots", "Twice Baked Potatoes", "Twice Cooked Quinoa with Chipotle and Lime Chicken", "Tzatziki", "Tzimmes", "V", "Vanilla Cream Cheese Custard", "Vanilla Custard Sauce", "Veal and Portobello Mushroom Stew", "Vegetable Broth & Chef Knife Giveaway", "Vegetable Chili", "Vegetable Shepherds Pie", "Vegetarian Stuffed Zucchini", "Veggie Dip Bread Bowl Wreath", "Velvet Chicken with Vegetables", "Vietnamese Caramel Sauce",
"Vietnamese Chicken and Cabbage Salad", "Vietnamese Dipping Sauce", "W", "Waldorf Salad", "Warm Mushroom Bacon Dip", "Watermelon and Pink Grapefruit Frozen Margaritas", "Watermelon Berry Smoothies and Popsicles", "Watermelon Mint Aqua Fresca", 
"Watermelon, Feta and Mint Salad", "Weekday Triple Play  Meal #1 Beef and Cabbage Stir Fry", "Weekday Triple Play  Meal #2 Beef Calzones", "Weekday Triple Play  Meal #3 California Slaw", "Weekday Triple Play Cabbage Blend", "Wheat Berry Salad with Dried Figs and Whole Foods Market $50 Gift Card Giveaway", "Wheatberry Salad with Cranberries, Feta and Orange Citronette", "White Balsamic Vinaigrette", "White Barbecue Chicken", "White Barbecue Pizza with Prosciutto and Caramelized Onions", "White Barbecue Sauce",
"White Barbecue Sauce Pork Ribs", "White Bean and Kale Dip", "White Bean Dip", "White Chicken Pizza", "White Chili with Chicken", "White Chocolate Apricot Scones", "White Chocolate Peppermint Martini",
"White Christmas Pie", "White Lasagna Chicken Rollups", "White Vegetable Lasagna", "White Wine Sangria", "Whole Wheat Spaetzle With Butternut Squash", "Whole Wheat Zucchini Bread", "Whole30 Cauliflower and Yam Potato Salad", "Whole30 Chili", "Whole30 Salmon Cakes with Tartar Sauce", "Whole30 Spaghetti Squash with Pesto", "Whole30 Stuffed Cabbage", "Whole30 West Coast Chicken", "Whoopie Pies", "Wicked Pickles", "Wild Mushroom and Black Garlic Soup", "Winter Vegetable Salad", "Y", "Yankee Pot Roast",
"Yogurt and Feta Dip", "Yorkshire Pudding", "Z", "Zesty Cheesy Ritz Dip", "Zesty Chicken with Shallots, Capers and Olives", "Zesty Pulled Turkey", "Zesty Salmon Burgers with Dill Spread", "Zucchini and Eggs", "Zucchini Brownies", "Zucchini Butter", "Zucchini Corn Bread with Bacon", "Zucchini Frittata with Tuscan Kale", "Zucchini Fritters", "Zucchini Johnnycakes", "Zucchini Lasagna", "Zucchini Parmesan", "Zucchini Risotto with Goat Cheese and Prosciutto", "Zucchini Spaghetti",
"Zucchini Tomato Risotto", "Zucchini Tomato Skewers with Fresh Herb Dressing", "Zucchini, Ham and Rice Skillet",
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ]

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



metrics = [
            '1/16 teaspoon','dash','1/8 teaspoon','a pinch','3 teaspoons','1 Tablespoon','1/8 cup','2 tablespoons','1 standard coffee scoop','1/4 cup','4 Tablespoons','1/3 cup',
            '5 Tablespoons', '1 teaspoon','1/2 cup','8 Tablespoons','3/4 cup','12 Tablespoons','1 cup','16 Tablespoons','1 Pound','16 ounces','8 Fluid ounces','1 Cup','1 Pint',
            '2 Cups','16 fluid ounces','1 Quart','2 Pints','4 cups','1 Gallon','4 Quarts','16 cups','1/5 teaspoon','1 ml','1 teaspoon','5 ml','1 tablespoon','15 ml','1 fluid oz','30 ml',
            '1/5 cup','50 ml','1 cup','240 ml','2 cups','1 pint','470 ml','4 cups','1 quart','.95 liter','4 quarts','1 gal','3.8 liters','1 oz','28 grams','1 pound','454 grams','1 milliliter',
            '1/5 teaspoon','5 ml','1 teaspoon','15 ml','1 tablespoon','30 ml','1 fluid oz','100 ml','3.4 fluid oz','240 ml','1 cup','1 liter','34 fluid oz','1 liter','4.2 cups','2.1 pints',
            '100 grams','3.5 ounces','500 grams','1.10 pounds','1 kilogram','2.205 pounds','35 oz'
            ]
my_word_list = [
'rice','pepper','sugar','salt','water','preheat','sesame','cranberry','beans','deep fry','pie','bar','ice','oat', 'put','the','pot','350 degrees','heat','fry','coconut oil', 
'chicken breast', 'ackee','skellion','black pepper', 'roast','bake','steam','fish','oven','oil','jerk','honey','potato','jackfruit','juice','remove','defrost','amount','weigh',
'from','100','20','50','250','grams','table spoon','tea spoon','granola','raisin', 'pineapple','cook','caramel','icing','cane juice','lime','crush','flask','bread crums','turkey',
'neck','eggs','egg','season all','pan','grease','butter','yogurt','tomatoes','tomato','carrot','cucumber','spaghetti','macaroni','bring to','low fire','dash','leave','the','the','put'
'put','put','put','pot','leave','leave','salted','salt fish','1/16 teaspoon','dash','1/8 teaspoon','a pinch','3 teaspoons','1 Tablespoon','1/8 cup','2 tablespoons',
'1 standard coffee scoop','1/4 cup','4 Tablespoons','1/3 cup','5 Tablespoons', '1 teaspoon','1/2 cup','8 Tablespoons','3/4 cup','12 Tablespoons','1 cup','16 Tablespoons','1 Pound',
'16 ounces','8 Fluid ounces','1 Cup','1 Pint','2 Cups','16 fluid ounces','1 Quart','2 Pints','4 cups','1 Gallon','4 Quarts','16 cups','1/5 teaspoon','1 ml','1 teaspoon','5 ml',
'1 tablespoon','15 ml','1 fluid oz','30 ml','1/5 cup','50 ml','1 cup','240 ml','2 cups','1 pint','470 ml','4 cups','1 quart','.95 liter','4 quarts','1 gal','3.8 liters','1 oz',
'28 grams','1 pound','454 grams','1 milliliter','1/5 teaspoon','5 ml','1 teaspoon','15 ml','1 tablespoon','30 ml','1 fluid oz','100 ml','3.4 fluid oz','240 ml','1 cup','1 liter',
'34 fluid oz','1 liter','4.2 cups','2.1 pints','100 grams','3.5 ounces','500 grams','1.10 pounds','1 kilogram','2.205 pounds','35 oz',    'Chicken Stock', 'Carrots', 'Potatoes', 'Peas', 
'Heavy Cream', 'Modified Food Starch', 'Wheat Flour', 'Salt', 'Chicken Fat', 'Dried Dairy Blend','Whey', 'Calcium Caseinate','Butter','Cream', 'Natural Flavoring', 'Maltodextrin', 
'Milk Solids', 'Nonfat Dry Milk', 'Chicken Fat', 'Beef Extract', 'Ascorbic Acid', 'Monosodium Glutamate', 'Liquid Margarine','Vegetable Oil Blend','Liquid Soybean', 'Hydrogenated Cottonseed', 
'Hydrogenated Soybean', 'Water', 'Vegetable Mono And Diglycerides', 'Beta Carotene','Roasted Garlic Juice Flavor','Garlic Juice', 'Gelatin', 'Roasted Onion Juice Flavor','Onion Juice', 
'Hydrolyzed Corn', 'Soy', 'Wheat Gluten Protein','Vegetable Stock','Celery', 'Maltodextrin', 'Partially Hydrogenated Soybean Oil','Dextrose', 'Chicken Broth', 'Chicken Stock', 'Sugar', 
'Mono','Diglycerides', 'Citric Acid', 'Spice', 'Seasoning','Oleoresin Turmeric', 'Spice Extractives','Parsley','Caramel Color','Yellow','Enriched Flour','Bleached Wheat Flour','Niacin', 
'Ferrous Sulfate', 'Thiamin Mononitrate', 'Riboflavin', 'Folic Acid', 'Hydrogenated Palm Kernel Oil','Nonfat Milk','Dough Conditioner', 'L-Cysteine Hydrochloride', 'Potassium Sorbate', 
'Sodium Benzoate','Garlic Powder', 'Corn Syrup Solids','Anti Caking Agent','Rice','Paprika','Hot Sauce','Shrimp','Steak','Milk','Cinamon Powder','Vanilla','black pepper','skellion','thyme',
'bluberry','strawberry','Apple','Apricot','Avocado','Banana','Bilberry','Blackberry','Blackcurrant','Boysenberry','Buddha','Crab apples','Currant','Cherry','Cherimoya','Chico fruit',
'Cloudberry','Coconut','Cranberry','Cucumber','Custard apple','Damson','Date','Dragonfruit','Durian','Elderberry','Feijoa','Fig','Goji berry','Gooseberry','Grape','Raisin','Grapefruit',
'Guava','Honeyberry','Huckleberry','Jabuticaba','Jackfruit','Jambul','Jujube','Juniper berry','Kiwano horned melon)','Kiwifruit','Kumquat','Lemon','Lime','Loquat','Longan'
 ]


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method== 'POST' and form.validate():
        firstname = str(form.firstname.data)
        lastname = str(
        form.lastname.data)
        username = str(
        form.username.data)
        email = str(
        form.email.data)
        phone = form.phonenumber.data
        preffered = str(
        form.preferedmeal.data)
        #password = bcrypt.generate_password_hash(str(form.password.data))
        password = str(form.password.data)
        city = str(
        form.city.data)
        street = str(
        form.street.data)
        
        
        
        
        #Create cursor
        
        cur = mysql.connection.cursor()
        c1 = mysql.connection.cursor()
        c1.execute('INSERT INTO address(city,userAccName,street) VALUES (%s,%s,%s)',(city,username,street))
        mysql.connection.commit()
        
        result = c1.execute('SELECT * FROM address WHERE userAccName = %s ',(username,))
        data = c1.fetchone()
        fact = data['addressid']
        cur.execute('INSERT INTO user(userAccName, userFname, userLname, email, uPassword,uPhoneNum, addressid,uPrefferedMeal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(username,firstname,lastname,email,password,phone,fact,preffered))
       
        #Commit to DB
        mysql.connection.commit()
         
         #Close connection
        cur.close()
        c1.close()
         
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)
@app.route('/login', methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        #GET FORM Fields
        
        username = request.form['username']
        password_cand= request.form['password']
        
        #Crete cursor
        cur = mysql.connection.cursor()
        
        #GET user by username
        result = cur.execute("SELECT * FROM user WHERE userAccName = %s", [username])
        
        if result>0:
            
            #Get stored hash
            data = cur.fetchone()
            password = data['uPassword']
            global Iuse
            Iuse = data['userId']
            
            
            #Compare Passwords
            
            #if bcrypt.check_password_hash(password,password_cand):
            if password == password_cand:
                
                #Passed
                session['logged_in']=True
                session['username'] = username
                flash ('You are now logged in', 'success')
                return redirect(url_for('home'))
            
            else:
                flash('Invalid Login', 'error')
                return render_template('login.html')
            #Close connection
            cur.close()
        else:
            flash ('Username not found', 'error')
            return render_template('login.html')
    return render_template('login.html')
    
    
#Check if user logged in

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
    
@app.route('/')
@is_logged_in
def home():
    cur = mysql.connection.cursor()
    res = cur.callproc('countit',(Iuse,))
    data = cur.fetchone()
    print(data)
    return render_template('home.html',data=data)
    
@app.route('/profile/',methods=['GET','POST'])
@is_logged_in
def profile():
    #Create cursor
    cur = mysql.connection.cursor()
    #Execute 
    profile = cur.execute('SELECT * FROM user WHERE userId = %s',(Iuse,))
    profdat = cur.fetchone()
    cur.close()
    
    return render_template('profile.html',profdat=profdat)
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash ('You are now logged out', 'success')
    return redirect(url_for('login'))
    
@app.route('/add_recipe',methods=['GET','POST'])
@is_logged_in
def addrecipe():
    form = RecipeForm(request.form)
    if request.method=='POST' and form.validate():
        Rname = str(form.name.data)
        Instruct = str(form.instructions.data)
        
        
        #Create cursor
        cur = mysql.connection.cursor()
        cur1 = mysql.connection.cursor()
        cur4 = mysql.connection.cursor()
        
        #Execute
        cur.execute('INSERT INTO recipe (userId,rname,rdescription) VALUES (%s,%s,%s)',(Iuse,Rname, Instruct,))
        
        #Commit
        mysql.connection.commit()
        
        result = cur.execute("SELECT * FROM recipe WHERE userId = %s  ", (Iuse,))
        data = cur.fetchone()
        fact = data['recipeId']
        cur1.execute('INSERT INTO instruction (recipeId) VALUES (%s)', (fact,)) 
        
        #Commit
        mysql.connection.commit()
        
        
        result = cur1.execute("SELECT * FROM instruction WHERE recipeId = %s  ", (fact,))
        data = cur1.fetchone()
        fact1 = data['instructionId']
    
        
        cur.execute ('UPDATE instruction SET recipeId = %s WHERE instructionId = %s',(fact,fact1) )
        mysql.connection.commit()
        cur4.execute('INSERT INTO user_recipe (userId,recipeId) VALUES (%s,%s)',(Iuse,fact,))

       
       
        #Commit
        mysql.connection.commit()
        
        #Close connection
        cur.close()
        cur1.close()
        cur4.close()
        
        flash('Recipe Updated', 'success')
        return redirect(url_for('home'))
    return render_template ('add_recipe.html', form = form)
        
@app.route('/recipes')
def recipes():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.callproc('list_recipes')
    if result>0:
        
        recipes = cur.fetchall()
        print(recipes)
        cur.close()
        return render_template('recipe.html', recipes=recipes)
    else:
        msg = 'No Recipe Found'
        return render_template('recipe.html', msg=msg)
    # Close connection
    cur.close()
    
@app.route('/recipe/<string:id>/')
def recipe(id):
     # Create cursor
    cur = mysql.connection.cursor()
    
    #Get recipe
    
    result = cur.execute("SELECT * FROM recipe WHERE recipeId = %s",[id] )
    recipes = cur.fetchone()
    cur.close()
    return render_template('Arecipe.html', recipes = recipes)
    
    
@app.route('/edit_recipe/<string:id>',methods=['GET', 'POST'])
@is_logged_in
def edit_recipe(id):
    
    # Create cursor
    cur = mysql.connection.cursor()
    
    #Get recipe
    result = cur.execute('SELECT * FROM recipe WHERE recipeId = %s',[id])
    
    recipe = cur.fetchone()
    
    cur.close()
    
    #GET FORM
    form = RecipeForm(request.form)
   
    #Populate the fields
    form.name.data = recipe['rname']
    form.instructions.data = recipe ['rdescription']
    
    if request.method=='POST' and form.validate():
        Rname = request.form['name']
        Instruct = request.form['instructions']
        
        
        #Create cursor
        cur = mysql.connection.cursor()
        
        
        #Execute
        cur.execute("UPDATE recipe SET rname = %s, rdescription = %s WHERE recipeId = %s",(Rname,Instruct,id))
        
        #Commit
        mysql.connection.commit()
        
        #Close connection
        cur.close()
        
        flash('Recipe Updated', 'success')
        return redirect(url_for('home'))
    return render_template('edit_recipe.html', form = form, recipe=recipe)
    
@app.route('/delete_recipe/<string:id>', methods=['POST'])
@is_logged_in
def delete_recipe(id):
    
    #Create cursor
    
    cur= mysql.connection.cursor()
    
    #Execute
    cur.execute('DELETE FROM instruction WHERE recipeId=%s',[id])
    cur.execute('DELETE FROM recipe WHERE recipeId=%s',[id])
    
    
    
    #Commit
    mysql.connection.commit()
        
    #Close connection
    cur.close()
    
    flash('Recipe Deleted', 'success')
    return redirect(url_for('home'))
    
    
    



@app.route('/search', methods=['GET', 'POST'])
@is_logged_in
def ser():
    search = SearchForm(request.form)
    
    if request.method == 'POST'and search.validate():
        searchtext = search.searchtext.data
        if searchtext and searchtext.strip():
            #Create cursor
            cur = mysql.connection.cursor()
            #Execute 
            result = cur.execute("SELECT * FROM recipe WHERE rname  LIKE %s ", ("%" + searchtext +"%",))
            
            if result > 0 :
                recipes = cur.fetchmany(1000000)
                return render_template('recipe.html', recipes=recipes)
            else:
                flash('No results found!')
                return render_template('recipe.html')
             
             
        else:
            
            #Create cursor
            cur = mysql.connection.cursor()
            #Execute 
            result = cur.execute('SELECT * FROM recipe')
            if result > 0 :
                recipes = cur.fetchall()
                return render_template('recipe.html', recipes=recipes)
            else:
                flash('No results found!')
                return render_template('recipe.html')
                
 
    return render_template('recipe.html', form=search)


    
    
    
    
    

@app.route('/inventory', methods = ['GET','POST'])
@is_logged_in
def invent():
    form = IngredientsForm(request.form)
    
    
    if request.method == 'POST':
        #Create cursors
        cur = mysql.connection.cursor()
        cur1 = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        cur3 = mysql.connection.cursor()
        cur4 = mysql.connection.cursor()
        #Execute to check if user has a kitchen already assigned
        result = cur1.execute("SELECT * FROM kitchen WHERE userId = %s",(Iuse,))
        
        
        if result> 0:
            data = cur1.fetchone()
            kit = data['kitchenId']
            ingredients = form.ingredients.data
            for ing in ingredients:
                #Execute to insert ingredient
                cur.execute("INSERT INTO ingredient(ingredient_name) VALUES (%s)", (ing,))
                mysql.connection.commit()
                
                
                #Execute to get the ingredient that was recently inserted in database
                resul = cur2.execute("SELECT * FROM ingredient WHERE ingredient_name = %s AND ingredientId IN (SELECT max(ingredientId) FROM ingredient)",(ing,))
                data2= cur2.fetchone()
                ingid = data2['ingredientId']
 
                cur3.execute("INSERT INTO ingredient_kitchen(kitchenId,ingredientId)VALUES(%s,%s)",(kit,ingid,))
                #Commit
                mysql.connection.commit()
                
            flash("Ingredients Added To Your Inventory","success")
            #Close Cursors
            cur.close()
            cur1.close()
            cur2.close()
            cur3.close()
            cur4.close()
            return redirect(url_for('invent'))
        
   
                
        else:
            cur1.execute("INSERT INTO kitchen (userId) VALUES(%s)",(Iuse,))
            
            result = cur2.execute("SELECT * FROM kitchen WHERE userId = %s",(Iuse,))
            data = cur2.fetchone()
            kit = data['kitchenId']
            ingredients = form.ingredients.data
            for ing in ingredients:
                #Execute to insert ingredient
                cur.execute("INSERT INTO ingredient(ingredient_name) VALUES (%s)", (ing,))
                mysql.connection.commit()
                
                
                #Execute to get the ingredient that was recently inserted in database
                resul = cur3.execute("SELECT * FROM ingredient WHERE ingredient_name = %s AND ingredientId IN (SELECT max(ingredientId) FROM ingredient)",(ing,))
                data2= cur3.fetchone()
                ingid = data2['ingredientId']
                
                
                
                cur4.execute("INSERT INTO ingredient_kitchen(kitchenId,ingredientId)VALUES(%s,%s)",(kit,ingid,))
                #Commit
                mysql.connection.commit()
                
                
            flash("Ingredients Added To Your Inventory","success")
            #Close Cursors
            cur.close()
            cur1.close()
            cur2.close()
            cur3.close()
            cur4.close()
            return redirect(url_for('invent'))
            
            
            
    
    return render_template('inventory.html', form=form)
            
@app.route("/inventlist")
@is_logged_in
def listitems():
    
    #Create cursor
    cur = mysql.connection.cursor()
    cur1 = mysql.connection.cursor()
    
    #Execute 
    result = cur.execute("SELECT ingredient_name FROM ingredient WHERE ingredientId IN(SELECT ingredientId FROM ingredient_kitchen WHERE kitchenId In(SELECT kitchenId FROM kitchen WHERE userId = %s) )",(Iuse,))
    
    if result>0:
        data = cur.fetchmany(70000)
        return render_template('ingredientlist.html', data=data)
    
    #
    else:
        msg = 'Nothing added to inventory yet'
        return render_template('ingredientlist.html', msg=msg)
    
    
@app.route("/tracklist")
def tracklist():
    #Create cursor
    cur = mysql.connection.cursor()
    
    #Execute 
    result = cur.execute("SELECT ingredient_name FROM ingredient WHERE ingredientId IN(SELECT ingredientId FROM ingredient_kitchen WHERE kitchenId In(SELECT kitchenId FROM kitchen WHERE userId = %s) )",(Iuse,))

    if result>0:
        data = cur.fetchmany(70000)
        return render_template('ingredientlist.html', data=data)
        
@app.route("/ingredlist",methods=['GET','POST'])
def ingredlist():
    form = TracklistForm(request.form)
 
    if request.method == 'POST':
        
        ingredstat = form.ingredients.data
        print(ingredstat)
        cur = mysql.connection.cursor()
        cur1 = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM kitchen WHERE userId = %s",(Iuse,))
        
        if result > 0:
            datar = cur.fetchone()
            datar = datar['kitchenId']
            result2 = cur1.execute("SELECT * FROM ingredient_kitchen WHERE kitchenId = %s",(datar,))
            if result2 >0:
                cur2.execute('UPDATE ingredient_kitchen SET measurementId = %s WHERE kitchenId = %s',(ingredstat,datar,))
                mysql.connection.commit()
                cur.close()
                cur1.close()
                cur2.close()
                flash('Status Submitted','success')
                return redirect(url_for('ingredlist'))
        else:
            flash('Not here')
    cur5 = mysql.connection.cursor()
    #Execute 
    result = cur5.execute("SELECT ingredient_name FROM ingredient WHERE ingredientId IN(SELECT ingredientId FROM ingredient_kitchen WHERE kitchenId In(SELECT kitchenId FROM kitchen WHERE userId = %s) )",(Iuse,))

    if result>0:
            data = cur5.fetchmany(70000)
            return render_template('tracklist.html',data=data, form=form)
            cur5.close()
    

@app.route('/popingred')
@is_logged_in
def popingred():
    for  i in ingredients_list:
        cur = mysql.connection.cursor()
    
        cur.execute("INSERT INTO ingredient(ingredient_name)VALUES(%s)",(i,))
        mysql.connection.commit()
        cur.close()
    return render_template('home.html')
        
   
@app.route('/supermarketlist')
@is_logged_in
def supermarket():
    
    cur = mysql.connection.cursor()
    resu= cur.callproc('O_list',(Iuse,))
    data = cur.fetchall()
    print(data)
    #cur1 = mysql.connection.cursor()
    #cur1.execute("SELECT * FROM ingredient WHERE ingredientId IN(SELECT ingredientId FROM ingredient_kitchen WHERE measurementId='Low in Stock' AND kitchenId IN (SELECT kitchenId FROM kitchen WHERE userId = %s))",(Iuse,))
    #data = cur1.fetchmany(30000)
    cur.close()
    return render_template('super.html',data=data)
@app.route('/populate',methods=['POST','GET'])
@is_logged_in
def db_insert():
    print ("Reach")
    count = 0
    counter = 0
    counters = 0
    
    
    if request.method == "POST":
        print ("Reach")
        #CREATE CURSORS
        cur = mysql.connection.cursor()
        cur1 = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        cur3= mysql.connection.cursor()
        cur4= mysql.connection.cursor()
        cur5= mysql.connection.cursor()
        cur6= mysql.connection.cursor()
        cur7 = mysql.connection.cursor()
        cur8 = mysql.connection.cursor()
        cur9 = mysql.connection.cursor()
        cur10 = mysql.connection.cursor()
        cur11 = mysql.connection.cursor()
        cur12 = mysql.connection.cursor()
        cur13 = mysql.connection.cursor()
        cur14 = mysql.connection.cursor()
        cur15 = mysql.connection.cursor()
        print ("Create Cursor")
        global resul
        for i in range (0,100000):
            city = str(fake.city())
            street = str(fake.street_name())
            userFname = str(fake.first_name())
            userLname = str(fake.last_name()) 
            uPassword = str(fake.password())
            uPhoneNum = str(fake.phone_number())
            email = str((fake.email()))
            userAccName = str(fake.user_name())
            print ("Save VARIABLES")
            
            #addressid =str(fake.random_int(min=60000,max=100000000))
            
            
            #INSERT into address table
            cur1.execute("INSERT INTO address(city,street,userAccName)VALUES(%s,%s,%s)",(city,street,userAccName,))
            mysql.connection.commit()
            reu = cur1.execute("SELECT * FROM address WHERE userAccName = %s",(userAccName,))
            res = cur1.fetchone()
            res = res['addressid']
            cur.execute("INSERT INTO user (userAccName,userFname,userLname,email,uPassword,uPhoneNum,addressid) VALUES (%s, %s, %s, %s, %s,%s,%s)", (userAccName, userFname, userLname,email, uPassword,uPhoneNum,res,))
            mysql.connection.commit()
            data = cur.execute("SELECT * FROM user WHERE userAccName = %s",(userAccName,))
            resul= cur.fetchone()
            resul = resul['userId']
            print ("Insert into address")
            
            #INSERT into kitchen using user id
            cur4.execute("INSERT INTO kitchen (userId)VALUES(%s)",(resul,))
            mysql.connection.commit()
            print ("Insert into kitchen")
            
            
            
            for x in range (1,5):
                dish = random.choice(recipe_n)
                random.shuffle(recipe_n)
                dish1 = random.choice(recipe_n)
                des = str(fake.sentence(ext_word_list=my_word_list))
                print ("Variables for dishes")
                #Execute
            
                #Create meal 
                cur12.execute("INSERT INTO meal (mName) VALUES (%s)",(dish,))
                mysql.connection.commit()
                cur2.execute("INSERT INTO recipe (userId,rname,rdescription)VALUES(%s,%s,%s)",(resul,dish1,des,))
                mysql.connection.commit()
                print ("Create meal")
            
            
                recipei = cur6.execute("SELECT * FROM recipe WHERE userId = %s AND recipeId IN(SELECT max(recipeId) FROM recipe)",(resul,))
                datar= cur6.fetchone()
                datar = datar['recipeId']
                print('Get repid')
                #Insert into user_recipe
                cur10.execute("INSERT INTO user_recipe(recipeId,userId) VALUES(%s,%s)",(datar,resul,))
                mysql.connection.commit()
                print ("Insert into rep")
            
                #SELECT MEAL 
                cur14.execute("SELECT *  FROM meal WHERE mName = %s",(dish,))
                mea = cur14.fetchone()
                meat = mea['mealId']
                print ("Select meal")
           
                #INSERT in recipe__meal 
                cur9.execute("INSERT INTO recipe_meal(recipeId,mealId)VALUES(%s,%s)",(datar,meat,))
                mysql.connection.commit()
                print ("recipe_meal")
                
        
            
         
                #INSERT into instruction with recipeid
                cur3.execute("INSERT INTO instruction (recipeId)VALUES(%s)",(datar,))
                mysql.connection.commit
                print('Inserting in instruction')
                count = count + 1
                print(count)
        print ("Closing cursor First round")
        cur.close()
    	cur1.close()
    	cur4.close()
    	cur12.close()
    	cur2.close()
    	cur6.close()
    	cur9.close()
    	cur10.close()
    	cur14.close()
    	cur3.close()
        print('First round Over')
            
            
        for i in ingredients_list:
            
            print('Going for it')
            #INSERT ingredient name in ingredient
            cur5.execute("INSERT INTO ingredient (ingredient_name) VALUES (%s)",(i,))
            mysql.connection.commit()
            cur13.execute("SELECT * FROM ingredient WHERE ingredient_name = %s ",(i,))
            resulted = cur13.fetchone()
            resulted = resulted['ingredientId']
            
            #GET kitchen ID
            cur15.execute("SELECT * FROM kitchen WHERE userId=%s",(resul,))
            uto = cur15.fetchone()
            uto =uto['kitchenId']
            #INSERTING ingredientid in kitchen
            cur7.execute("INSERT INTO ingredient_kitchen (ingredientId,kitchenId) VALUES(%s,%s)",(resulted,uto,))
            mysql.connection.commit()
            
            #INSERT in ingredient_recipe
            cur8.execute("INSERT INTO ingredient_recipe(ingredientId, recipeId)VALUES(%s,%s)",(resulted,datar,))
            mysql.connection.commit()
            counter = counter + 1
            print(counter)
        print ("Closing cursor second round")
        cur5.close()
        cur13.close()
    	cur15.close()
    	cur7.close()
    	cur8.close()
        print('Second Round Over')

        for i in metrics:
            
    	    #Generate measurement table
    	    print('measurement')
    	    cur11.execute("INSERT INTO measurement (measurementName) VALUES (%s)",(i,))
    	    mysql.connection.commit()
    	    counters = counters + 1
    	    print(counters)
    	print ("Closing cursor third round")
    	cur11.close()
    	print('Third round over')
    	flash("Everything Up")
    	
    return render_template('populate.html')

   
   


        
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
    
