import json
from urllib.parse import parse_qs
from framework import App, Response

users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
    {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'},
]

app = App()

# обычный GET
@app.route('/')
def index(request):
    html = """
    <html>
        <head><title>Web Framework Example</title></head>
        <body>
            <h1>Welcome to the Web Framework!</h1>
            <ul>
                <li><a href="/hello">Hello Page</a></li>
                <li><a href="/users">Users API</a></li>
                <li><a href="/form">Form Example</a></li>
            </ul>
        </body>
    </html>
    """
    return Response(body=html)


# GET c query параметрами
@app.route('/hello')
def hello(request):
    name = request.query.get('name', 'World')
    html = f"""
    <html>
        <head><title>Hello</title></head>
        <body>
            <h1>Hello, {name}!</h1>
            <a href="/">Back to home</a>
        </body>
    </html>
    """
    return Response(body=html)


# GET с ответом в формате JSON, поддерживает фильтрацию
@app.route('/users', methods=['GET'])
def get_users(request):
    search = request.query.get('search', '')
    result = users
    if search:
        result = [u for u in users if search.lower() in u['name'].lower()]
    return Response(
        body=json.dumps(result),
        headers={'Content-Type': 'application/json'}
    )

# Метод POST с параметрами в формате json, и формирование ответа в том же формате
@app.route('/users', methods=['POST'])
def create_user(request):
    global users
    try:
        data = request.json()
        name = data.get('name', 'Unknown')
        email = data.get('email', '')
        new_id = max([u['id'] for u in users], default=0) + 1
        new_user = {
            'id': new_id,
            'name': name,
            'email': email
        }
        users.append(new_user)

        return Response(
            body=json.dumps({'message': 'User created', 'user': new_user}),
            status=201,
            headers={'Content-Type': 'application/json'}
        )
    except Exception as e:
        return Response(
            body=json.dumps({'error': str(e)}),
            status=400,
            headers={'Content-Type': 'application/json'}
        )


# GET запрос, отображающий форму для заполнения
@app.route('/form', methods=['GET'])
def show_form(request):
    html = """
    <html>
        <head><title>Form Example</title></head>
        <body>
            <h1>Submit Data</h1>
            <form method="POST" action="/form">
                <label>Name:</label><br>
                <input type="text" name="name"><br><br>
                <label>Email:</label><br>
                <input type="email" name="email"><br><br>
                <button type="submit">Submit</button>
            </form>
            <a href="/">Back to home</a>
        </body>
    </html>
    """
    return Response(body=html)

# POST запрос, который обрабатывает данные формы и добавляет нового пользователя в глобальный список
# Возвращает страницу с подтверждением отправки
@app.route('/form', methods=['POST'])
def handle_form(request):
    global users
    try:
        body = request.body.decode() if request.body else ''
        data = parse_qs(body)

        name = data.get('name', [''])[0]
        email = data.get('email', [''])[0]

        if not name or not email:
            if not name or not email:
                html = """
                    <html>
                        <head><title>400 Bad Request</title></head>
                        <body>
                            <h1>400 Bad Request</h1>
                            <a href="/form">Назад к форме</a>
                        </body>
                    </html>
                    """
                return Response(body=html, status=400)

        html = f"""
        <html>
            <head><title>Form Submitted</title></head>
            <body>
                <h1>Form Submitted Successfully!</h1>
                <p>Name: {name}</p>
                <p>Email: {email}</p>
                <a href="/form">Submit another</a> | <a href="/">Home</a>
            </body>
        </html>
        """
        new_id = max([u['id'] for u in users], default=0) + 1
        new_user = {'id': new_id, 'name': name, 'email': email}
        users.append(new_user)
        return Response(body=html)

    except Exception as e:
        return Response(
            body=f'<html><body><h1>Error: {str(e)}</h1></body></html>',
            status=400
        )


if __name__ == '__main__':
    print("Starting web server...")
    print("Visit http://127.0.0.1:8000/ in your browser")
    app.run(host='127.0.0.1', port=8000)