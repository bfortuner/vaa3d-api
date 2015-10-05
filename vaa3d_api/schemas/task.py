from .. import ma
from ..models.task import Task


class TaskSchema(ma.Schema):
    class Meta:
        fields = ['id']


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
