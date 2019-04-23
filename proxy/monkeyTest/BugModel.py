import os

try:
    from peewee import *
    from playhouse.pool import PooledMySQLDatabase
except ImportError:
    os.system("pip install peewee")
    from peewee import *
    from playhouse.pool import PooledMySQLDatabase

try:
    monkey_bug_db = PooledMySQLDatabase('monkey_bug_db_test', user='root', password='100%SanityXm',
                                        host="10.232.52.151", port=3306)
except ImproperlyConfigured:
    os.system("pip install PyMySQL")
    monkey_bug_db = PooledMySQLDatabase('monkey_bug_db_test', user='root', password='100%SanityXm',
                                        host="10.232.52.151", port=3306)


class BaseModel(Model):
    id = PrimaryKeyField(_hidden=True)
    create_time = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], _hidden=True)
    update_time = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')],
                                _hidden=True)

    def __str__(self):
        return str(self.__data__)

    class Meta:
        database = monkey_bug_db


class Bugs(BaseModel):
    bug_detail = TextField()
    bug_signature_code = CharField(unique=True, index=True)
    bug_pid = IntegerField()
    bug_package_name = CharField()
    bug_summary = CharField()
    bug_time = CharField()
    bug_type = CharField()
    tag = CharField()


class BugTag(BaseModel):
    bug_signature_code = CharField()
    tag = CharField(index=True)


class BugRom(BaseModel):
    bug_signature_code = CharField(index=True)
    device_name = CharField()
    jira_miui_model = CharField()
    rom_version = CharField()
    tag = CharField()


class BugFile(BaseModel):
    bug_signature_code = CharField(index=True)
    file_name = TextField()
    tag = CharField()


class BugJira(BaseModel):
    bug_signature_code = CharField(unique=True, index=True)
    jira_id = CharField()
    tag = CharField()


class Jiras(BaseModel):
    jira_id = CharField(unique=True, index=True)
    jira_summary = CharField()
    jira_assignee = CharField()
    tag = CharField()


class UseInfo(BaseModel):
    user_name = CharField()
    test_type = CharField()
    test_package_name = CharField()
    test_done = IntegerField()
    tag = CharField()


def create_tables():
    with monkey_bug_db:
        monkey_bug_db.create_tables([Bugs, BugFile, BugJira, BugRom, Jiras])


def delete_tables():
    with monkey_bug_db:
        monkey_bug_db.drop_tables([Bugs, BugFile, BugJira, BugRom, Jiras])


def insert(table_name):
    with monkey_bug_db:
        table_name.save()


def update(table_name):
    with monkey_bug_db:
        table_name.update()

# if __name__ == "__main__":
# bug_jira = BugJira(id=2, bug_signature_code="adbsdkajfiwhfvjenvk222", jira_id="abuvrg", tag="asgweqgvqag222222")
# BugJira.update(jira_id="abuvrg00000").where(BugJira.bug_signature_code == "adbsdkajfiwhfvjenvk222").execute()
# update(bug_jira)
# r = BugFile.select().where(BugFile.bug_signature_code == "224efdcd919a94fd983e97850aba").get()
# r = BugFile.get(BugFile.bug_signature_code == "224efdcd919a94fd983e97850aba1d3d")
# print r
