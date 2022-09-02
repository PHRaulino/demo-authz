class Authorizer:
    def __init__(self, functionality):
        self.functionality = self.get_functionality(functionality)

    def get_functionality(self, fnct):
        self.functionalities = {
            "User": 1,
            "Group": 2,
            "Policy": 3,
            "Functionality": 4,
            "Action": 5,
            "Relationship_User": 6,
            "Relationship_Group": 7,
            "Relationship_Policy": 8,
            "Relationship_Functionality": 9,
        }
        return self.functionalities[fnct]

    def authorize(self, action, token):
        self.action = action
        self.token = token
        return True
