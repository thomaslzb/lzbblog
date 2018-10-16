from app import create_app, db, cli
from app.models import User, Post, Notification, Message, Task
import logging

app = create_app()
app.app_context().push()

cli.register(app)

# 如果 Elasticsearch 服务没有启动， 以下这句可以隐藏错误提醒
logging.getLogger("elasticsearch").setLevel(logging.CRITICAL)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task}


if __name__ == "__main__":
    # 检查 Elasticsearch 是否启动
    if not app.elasticsearch.ping():
        app.elasticsearch = None
        print('* Not connected to Elasticsearch...')

    # 检查服务器的DataBase Server 是否启动
    with app.app_context():
        db.init_app(app)
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        app.dbconnect = True
        print('*** DB is running...')
    except Exception as e:
        print(f"*** {e}")
        app.dbconnect = False
        print('*** WARNING! WARNING! WARNING! MySQL do not start...')

    app.run(debug=True, host="0.0.0.0", port=80)
