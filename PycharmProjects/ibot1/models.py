import peewee

database = peewee.SqliteDatabase('user_info.db')


class User(peewee.Model):
    user_id = peewee.CharField(unique=True)
    username = peewee.CharField()
    full_name = peewee.CharField()
    follows_count = peewee.IntegerField()
    followed_by_count = peewee.IntegerField()

    class Meta:
        database = database


class Media(peewee.Model):
    user_id = peewee.ForeignKeyField(User, to_field="user_id")
    media_id = peewee.CharField(unique=True)
    media_type = peewee.CharField()
    media_link = peewee.CharField()

    class Meta:
        database = database


class Comment(peewee.Model):
    comment_id = peewee.CharField(unique=True)
    media_id = peewee.ForeignKeyField(Media, to_field="media_id")
    user_id = peewee.ForeignKeyField(User, to_field="user_id")
    comment_text = peewee.CharField()

    class Meta:
        database = database


def initialize_db():
    database.create_tables([User, Media, Comment], safe=True)


initialize_db()
new_user = user(user_id='5', username='acadview',
                full_name='Acadview', follows_count=200, followd_by_count=1200)
new_user.save()

print new_user.username
print new_user.id
print new_user.user_id
