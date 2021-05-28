from flask import Flask
from flask_restful import Resource, Api, reqparse, abort


app=Flask(__name__)
api=Api(app)


todos = {
    1: {'task':'Write Hello World Program.', 'summary':'Write the code using Python.'},
    2: {'task':'Task2.', 'summary':'Summary2.'},
    3: {'task':'Task3.', 'summary':'Summary3.'},
    4: {'task':'Task4.', 'summary':'Summary4.'}

}

task_post_args=reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='Task is required' , required=True)
task_post_args.add_argument('summary', type=str, help='Summary is required' , required=True)

task_update_args = reqparse.RequestParser()
task_update_args.add_argument('task', type=str)
task_update_args.add_argument('summary', type=str)



class ToDoList(Resource):
    def get(self):
        return todos


class ToDo(Resource):

    def get(self, todo_id):
        return todos[todo_id]

    def post(self, todo_id):
        args=task_post_args.parse_args()
        if todo_id in todos:
            abort(409, 'Task Id already taken')
        todos[todo_id]={'task':args['task'], 'summary':args['summary']}
        return todos[todo_id]

    def put(self, todo_id):
        args=task_update_args.parse_args()
        if todo_id not in todos:
            abort(404, message="Task doesn't exist. Cannot Update.")
        if args['task']:
            todos[todo_id]['task']=args['task']
        if args['summary']:
            todos[todo_id]['summary']=args['summary']
        return todos[todo_id]

    def delete(self, todo_id):
        del todos[todo_id]
        return todos



api.add_resource(ToDo,'/todos/<int:todo_id>')
api.add_resource(ToDoList, '/todos')

if __name__=='__main__':
    app.run(debug=True)
