from flask import Blueprint
                           
blueprint = Blueprint(     
    'user_blueprint',
    __name__,              
    url_prefix='/user',         
    template_folder='templates',
    static_folder='static' 
) 

