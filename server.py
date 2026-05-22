from flask import Flask, request, jsonify, send_from_directory
import json, os, uuid, threading

app = Flask(__name__, static_folder='.', static_url_path='')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
LOCK = threading.Lock()

def data_path(name):
    return os.path.join(DATA_DIR, name + '.json')

def read_json(name):
    p = data_path(name)
    if not os.path.exists(p):
        return {}
    with LOCK:
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)

def write_json(name, data):
    with LOCK:
        with open(data_path(name), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def ensure_defaults():
    if not os.path.exists(data_path('admins')):
        write_json('admins', [
            {'id':'s1','user':'superadmin','pass':'admin123','role':'superadmin','name':'超级管理员'},
            {'id':'c1','user':'content','pass':'content123','role':'content','name':'内容管理员'},
            {'id':'t1','user':'template','pass':'template123','role':'template','name':'模板管理员'}
        ])
    if not os.path.exists(data_path('sections')):
        write_json('sections', {})
    if not os.path.exists(data_path('news')):
        write_json('news', [
            {'id':'n0','title':'习近平强调以更大力度加强基础研究 提升原始创新能力','body':'中共中央总书记、国家主席、中央军委主席习近平近日在考察时强调...','date':'2026-04-30','tag':'时政深一度'},
            {'id':'n1','title':'中巴建交75周年：巴基斯坦总统以最高礼仪致敬中国开国领袖','body':'在庆祝中巴建交75周年之际，巴基斯坦总统以最高礼仪向中国开国领袖致敬...','date':'2026-04-28','tag':'文明公约'}
        ])
    if not os.path.exists(data_path('templates')):
        write_json('templates', [
            {'id':'t1','name':'暗色科技','icon':'🚀','active':True},
            {'id':'t2','name':'中国水墨','icon':'🎋','active':False},
            {'id':'t3','name':'极简白','icon':'✨','active':False}
        ])
    if not os.path.exists(data_path('session')):
        write_json('session', {})

ensure_defaults()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin():
    return send_from_directory('.', 'admin.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    body = request.get_json()
    admins = read_json('admins')
    user = body.get('user', '')
    passwd = body.get('pass', '')
    found = None
    for a in admins:
        if a['user'] == user and a['pass'] == passwd:
            found = a
            break
    if not found:
        return jsonify({'ok': False, 'msg': '用户名或密码错误'})
    write_json('session', {'user': found['user'], 'role': found['role'], 'time': str(__import__('datetime').datetime.now())})
    return jsonify({'ok': True, 'user': found['user'], 'role': found['role']})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    write_json('session', {})
    return jsonify({'ok': True})

@app.route('/api/session')
def api_session():
    return jsonify(read_json('session'))

@app.route('/api/data', methods=['GET'])
def api_get_data():
    return jsonify({
        'admins': read_json('admins'),
        'sections': read_json('sections'),
        'news': read_json('news'),
        'templates': read_json('templates')
    })

@app.route('/api/data', methods=['POST'])
def api_save_data():
    body = request.get_json()
    admin_session = read_json('session')
    if not admin_session.get('user'):
        return jsonify({'ok': False, 'msg': '未登录'})
    role = admin_session.get('role', '')
    if 'sections' in body and role in ('superadmin', 'content'):
        write_json('sections', body['sections'])
    if 'news' in body and role in ('superadmin', 'content'):
        write_json('news', body['news'])
    if 'templates' in body and role in ('superadmin', 'template'):
        write_json('templates', body['templates'])
    if 'admins' in body and role == 'superadmin':
        write_json('admins', body['admins'])
    return jsonify({'ok': True})

@app.route('/api/session/check', methods=['GET'])
def api_check_session():
    s = read_json('session')
    if s.get('user'):
        admins = read_json('admins')
        for a in admins:
            if a['user'] == s['user']:
                return jsonify({'ok': True, 'user': a['user'], 'role': a['role']})
    write_json('session', {})
    return jsonify({'ok': False})

if __name__ == '__main__':
    port = 5099
    print(f'Cii.China 服务器启动: http://localhost:{port}')
    print(f'前台: http://localhost:{port}')
    print(f'后台: http://localhost:{port}/admin')
    app.run(host='0.0.0.0', port=port, debug=False)
