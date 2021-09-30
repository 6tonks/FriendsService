from application_services.BaseApplicationResource import BaseApplicationResource

import middleware.context as context

class FriendsResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_friends(cls, user):
        db_resource = context.get_db_resource()
        template = {
            'label': "user",
            'template': {"user_id": user},
        }
        res = db_resource.find_by_node_relationship_outward(template, relationship="friend")
        return res

    @classmethod
    def get_pending_friends(cls, user):
        db_resource = context.get_db_resource()
        template = {
            'label': "user",
            'template': {"user_id": user},
        }
        res = db_resource.find_by_node_relationship_inward(template, relationship="pending_friend")
        return res

    @classmethod
    def get_pending_friends_request(cls, user):
        db_resource = context.get_db_resource()
        template = {
            "label": "user",
            "template": {"user_id": user},
        }
        res = db_resource.find_by_node_relationship_outward(template, relationship="pending_friend")
        return res

    @classmethod
    def accept_friend_request(cls, user, friend):
        db_resource = context.get_db_resource()
        user_template = {
            "label": "user",
            "template": {"user_id": user},
        }
        friend_template = {
            "label": "user",
            "template": {"user_id": friend},
        }
        # Bidirectional
        db_resource.create_relationship(user_template, friend_template, relationship="friend")
        db_resource.create_relationship(friend_template, user_template, relationship="friend")

        # Delete pending request
        db_resource.delete_relationship(friend_template, user_template, relationship="pending_friend")
        return True

    @classmethod
    def decline_friend_request(cls, user, friend):
        db_resource = context.get_db_resource()
        user_template = {
            "label": "user",
            "template": {"user_id": user},
        }
        friend_template = {
            "label": "user",
            "template": {"user_id": friend},
        }
        # Delete pending request
        db_resource.delete_relationship(friend_template, user_template, relationship="pending_friend")
        return True

    @classmethod
    def add_friend_request(cls, user, friend):
        db_resource = context.get_db_resource()
        user_template = {
            "label": "user",
            "template": {"user_id": user},
        }
        friend_template = {
            "label": "user",
            "template": {"user_id": friend},
        }
        db_resource.create_relationship(user_template, friend_template, relationship="pending_friend")
        return True

    @classmethod
    def cancel_friend_request(cls, user, friend):
        db_resource = context.get_db_resource()
        user_template = {
            "label": "user",
            "template": {"user_id": user},
        }
        friend_template = {
            "label": "user",
            "template": {"user_id": friend},
        }
        # Delete pending request
        db_resource.delete_relationship(user_template, friend_template, relationship="pending_friend")
        return True

    @classmethod
    def delete_friend(cls, user, friend):
        db_resource = context.get_db_resource()
        user_template = {
            "label": "user",
            "template": {"user_id": user},
        }
        friend_template = {
            "label": "user",
            "template": {"user_id": friend},
        }
        # Delete friend bidirectional
        db_resource.delete_relationship(user_template, friend_template, relationship="friend")
        db_resource.delete_relationship(friend_template, user_template, relationship="friend")
        return True

    @classmethod
    def insert_user(cls, user):
        db_resource = context.get_db_resource()
        template = {
            "user_id": user,
        }
        res = db_resource.create_node(label="user", **template)
        return res

    @classmethod
    def delete_user(cls, user):
        db_resource = context.get_db_resource()
        user_template = {
            "label": "user",
            "template": {"user_id": user},
        }
        res = db_resource.delete_node(user_template)
        return res