from . import user

@user.route('/signup', methods=['POST'])
def signup():
    
    return