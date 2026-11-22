from fastapi.testclient import TestClient
from main import app, schema

with TestClient(app) as client:
    def run(query, variables=None):
        response = client.post('/graphql', json={'query': query, 'variables': variables or {}})
        return response, response.json()
    _, data = run('{ books { title } }')
    assert len(data['data']['books']) == 3
    assert set(data['data']['books'][0]) == {'title'}
    _, data = run('{ books(search:"PYTHON", inStock:true) { title author { name } } }')
    assert data['data']['books'] == [{'title':'Python for Beginners','author':{'name':'Anita Rao'}}]
    _, data = run('query($id:Int!){book(id:$id){id price inStock}}', {'id':2})
    assert data['data']['book'] == {'id':2,'price':699.0,'inStock':True}
    _, data = run('{book(id:999){title}}')
    assert data['data']['book'] is None and 'errors' not in data
    _, data = run('{books{rating}}')
    assert data.get('errors')
    _, data = run('{books(search:"nonexistent"){title}}')
    assert data['data']['books'] == []
    _, data = run('{books(inStock:false){id}}')
    assert data['data']['books'] == [{'id':3}]
    _, data = run('{first:book(id:1){id} second:book(id:2){id}}')
    assert data['data'] == {'first':{'id':1},'second':{'id':2}}
    assert client.get('/graphql', headers={'Accept':'text/html'}).status_code == 200
    assert 'inStock: Boolean!' in schema.as_str()
print('PASS: field selection, nesting, variables, aliases, filters, null, errors, GraphiQL and schema')
