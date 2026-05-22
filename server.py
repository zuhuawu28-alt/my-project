from flask import Flask, request, jsonify, send_from_directory
import json, os, uuid, threading, datetime, shutil

app = Flask(__name__, static_folder='.', static_url_path='')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
LOCK = threading.Lock()

def data_path(name):
    return os.path.join(DATA_DIR, name + '.json')

def read_json(name):
    p = data_path(name)
    if not os.path.exists(p): return {}
    with LOCK:
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)

def write_json(name, data):
    with LOCK:
        with open(data_path(name), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

def ensure_defaults():
    if not os.path.exists(data_path('admins')):
        write_json('admins', [
            {'id':'s1','user':'superadmin','pass':'admin123','role':'superadmin','name':'超级管理员'},
            {'id':'c1','user':'content','pass':'content123','role':'content','name':'内容管理员'},
            {'id':'t1','user':'template','pass':'template123','role':'template','name':'模板管理员'}
        ])
    if not os.path.exists(data_path('articles')):
        write_json('articles', [
            {'id':'a0','section':'shizheng','title':'习近平强调以更大力度加强基础研究 提升原始创新能力','content':'中共中央总书记、国家主席、中央军委主席习近平近日在考察时强调，要瞄准世界科技前沿，以更大力度加强基础研究，提升原始创新能力，为实现高水平科技自立自强提供有力支撑。','images':[],'videos':[],'comments':[],'source':'新华社','date':'2026-04-30','featured':True},
            {'id':'a1','section':'shizheng','title':'习近平强调"义乌发展经验"：因地制宜探索高质量发展之路','content':'习近平在浙江考察时指出，义乌的发展经验是中国特色社会主义在县域层面的生动实践，要因地制宜探索高质量发展之路。','images':[],'videos':[],'comments':[],'source':'新华社','date':'2026-04-25','featured':False},
            {'id':'a2','section':'fenghuo','title':'中国海军宣传片引猜想：第四艘航母是否已"出鞘"？','content':'中国海军最新发布的宣传片中出现的新航母画面引发广泛关注。分析人士指出，这可能是中国第四艘航母的首次公开亮相。','images':[],'videos':[],'comments':[],'source':'央视军事','date':'2026-04-28','featured':True},
            {'id':'a3','section':'ziyuan','title':'中巴建交75周年：巴基斯坦总统以最高礼仪致敬中国开国领袖','content':'在庆祝中巴建交75周年之际，巴基斯坦总统以最高礼仪向中国开国领袖致敬，体现两国深厚情谊。','images':[],'videos':[],'comments':[],'source':'新华社','date':'2026-04-28','featured':True},
            {'id':'a4','section':'kexue','title':'中国科学家发布天文AI模型"星衍"：发现160余个宇宙早期星系','content':'中国科学家发布天文AI模型"星衍"，探测深度跃升1星等，发现160余个宇宙早期星系。','images':[],'videos':[],'comments':[],'source':'科技日报','date':'2026-02-21','featured':False}
        ])
    if not os.path.exists(data_path('videos')):
        write_json('videos', [
            {'id':'v1','title':'中国航天：星辰大海','desc':'中国航天事业发展历程','url':'https://www.youtube.com/embed/dQw4w9WgXcQ','thumb':'🚀','date':'2026-04'},
            {'id':'v2','title':'未来科技趋势','desc':'人工智能与未来生活','url':'https://www.youtube.com/embed/dQw4w9WgXcQ','thumb':'🤖','date':'2026-03'}
        ])
    if not os.path.exists(data_path('templates')):
        write_json('templates', [
            {'id':'t1','name':'暗色科技','icon':'🚀','active':True,'css':':root{--bg:#050510;--bg2:#0a0a1a;--bg3:rgba(255,255,255,0.03);--bg4:rgba(0,200,255,0.05);--primary:#00c8ff;--secondary:#7b61ff;--accent:#ff61d8;--text:#e0e0e0;--text2:#8aaec8;--text3:#5a7a90;--border:rgba(0,200,255,0.12);--card-bg:rgba(255,255,255,0.03);--card-hover:rgba(0,200,255,0.06);--header-bg:linear-gradient(180deg,rgba(5,5,16,0.95),transparent);--font:\'Microsoft YaHei\',\'PingFang SC\',sans-serif;--radius:12px;--glow:0 0 30px rgba(0,200,255,0.08);--hero-gradient:linear-gradient(135deg,#00c8ff,#7b61ff)}'},
            {'id':'t2','name':'中国水墨','icon':'🎋','active':False,'css':':root{--bg:#f5f0e8;--bg2:#ede4d3;--bg3:rgba(0,0,0,0.02);--bg4:rgba(180,120,60,0.06);--primary:#8b4513;--secondary:#6b3410;--accent:#c4a265;--text:#2a1a0a;--text2:#6a5a4a;--text3:#9a8a7a;--border:rgba(139,69,19,0.15);--card-bg:rgba(255,255,255,0.5);--card-hover:rgba(255,255,255,0.7);--header-bg:linear-gradient(180deg,rgba(245,240,232,0.95),transparent);--font:\'STKaiti\',\'KaiTi\',\'SimSun\',serif;--radius:8px;--glow:0 0 20px rgba(139,69,19,0.06);--hero-gradient:linear-gradient(135deg,#8b4513,#c4a265)}'},
            {'id':'t3','name':'极简白','icon':'✨','active':False,'css':':root{--bg:#ffffff;--bg2:#f5f7fa;--bg3:rgba(0,0,0,0.02);--bg4:rgba(0,120,255,0.04);--primary:#0066cc;--secondary:#004999;--accent:#ff6600;--text:#1a1a2e;--text2:#4a5a6a;--text3:#8a9aaa;--border:rgba(0,0,0,0.08);--card-bg:#ffffff;--card-hover:rgba(0,120,255,0.04);--header-bg:linear-gradient(180deg,rgba(255,255,255,0.95),transparent);--font:\'Microsoft YaHei\',\'PingFang SC\',sans-serif;--radius:10px;--glow:0 0 20px rgba(0,102,204,0.06);--hero-gradient:linear-gradient(135deg,#0066cc,#004999)}'}
        ])
    if not os.path.exists(data_path('session')):
        write_json('session', {})
    if not os.path.exists(data_path('sections')):
        write_json('sections', {'shizheng':'时政深一度','fenghuo':'烽火铁甲','jingwei':'经纬脉搏','sheji':'社稷春秋','keji':'科技双刃','liebian':'裂变重溯','ziyuan':'资源配置','chongtu':'冲突重构','kexue':'科学探索','wenming':'文明博弈','qianxuesen':'伤痕铸就星辰的归国之路','mantou':'馒头与星辰','crown':'百元美钞上的王冠','water':'水的囚徒'})

ensure_defaults()

@app.route('/')
def index(): return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin(): return send_from_directory('.', 'admin.html')

@app.route('/uploads/<path:filename>')
def uploaded(filename): return send_from_directory(UPLOAD_DIR, filename)

@app.route('/api/login', methods=['POST'])
def api_login():
    body = request.get_json()
    admins = read_json('admins')
    found = None
    for a in admins:
        if a['user'] == body.get('user','') and a['pass'] == body.get('pass',''):
            found = a; break
    if not found: return jsonify({'ok':False,'msg':'用户名或密码错误'})
    write_json('session', {'user':found['user'],'role':found['role'],'time':now()})
    return jsonify({'ok':True,'user':found['user'],'role':found['role']})

@app.route('/api/logout', methods=['POST'])
def api_logout(): write_json('session', {}); return jsonify({'ok':True})

@app.route('/api/session')
def api_session(): return jsonify(read_json('session'))

@app.route('/api/session/check', methods=['GET'])
def api_check_session():
    s = read_json('session')
    if s.get('user'):
        for a in read_json('admins'):
            if a['user'] == s['user']:
                return jsonify({'ok':True,'user':a['user'],'role':a['role']})
    write_json('session', {})
    return jsonify({'ok':False})

def check_role():
    s = read_json('session')
    if not s.get('user'): return None
    return s.get('role','')

@app.route('/api/data', methods=['GET'])
def api_get_data():
    return jsonify({
        'articles': read_json('articles'),
        'videos': read_json('videos'),
        'templates': read_json('templates'),
        'admins': read_json('admins'),
        'sections': read_json('sections')
    })

@app.route('/api/data', methods=['POST'])
def api_save_data():
    body = request.get_json()
    role = check_role()
    if not role: return jsonify({'ok':False,'msg':'未登录'})
    if 'articles' in body and role in ('superadmin','content'): write_json('articles', body['articles'])
    if 'videos' in body and role in ('superadmin','content'): write_json('videos', body['videos'])
    if 'templates' in body and role in ('superadmin','template'): write_json('templates', body['templates'])
    if 'admins' in body and role == 'superadmin': write_json('admins', body['admins'])
    if 'sections' in body and role in ('superadmin','content'): write_json('sections', body['sections'])
    return jsonify({'ok':True})

@app.route('/api/frontend-data')
def api_frontend_data():
    return jsonify({
        'articles': read_json('articles'),
        'videos': read_json('videos'),
        'sections': read_json('sections')
    })

@app.route('/api/template/css')
def api_template_css():
    tmpl = read_json('templates')
    active = next((t for t in tmpl if t.get('active')), tmpl[0] if tmpl else None)
    return jsonify({'name':active['name'] if active else '默认','css':active['css'] if active else ''})

@app.route('/api/comments', methods=['GET'])
def api_get_comments():
    articles = read_json('articles')
    all_comments = []
    for a in articles:
        for c in a.get('comments',[]):
            c['articleTitle'] = a['title']
            c['articleId'] = a['id']
            all_comments.append(c)
    return jsonify(all_comments)

@app.route('/api/comments/approve', methods=['POST'])
def api_approve_comment():
    role = check_role()
    if not role or role not in ('superadmin','content'): return jsonify({'ok':False,'msg':'权限不足'})
    body = request.get_json()
    cid = body.get('id')
    articles = read_json('articles')
    for a in articles:
        for c in a.get('comments',[]):
            if c['id'] == cid:
                c['approved'] = body.get('approved', True)
                write_json('articles', articles)
                return jsonify({'ok':True})
    return jsonify({'ok':False,'msg':'未找到留言'})

@app.route('/api/comments/delete', methods=['POST'])
def api_delete_comment():
    role = check_role()
    if not role or role not in ('superadmin','content'): return jsonify({'ok':False,'msg':'权限不足'})
    body = request.get_json()
    cid = body.get('id')
    articles = read_json('articles')
    for a in articles:
        a['comments'] = [c for c in a.get('comments',[]) if c['id'] != cid]
    write_json('articles', articles)
    return jsonify({'ok':True})

@app.route('/api/comment', methods=['POST'])
def api_add_comment():
    body = request.get_json()
    aid = body.get('articleId')
    user = body.get('user','访客').strip() or '访客'
    content = body.get('content','').strip()
    if not aid or not content: return jsonify({'ok':False,'msg':'参数不完整'})
    articles = read_json('articles')
    for a in articles:
        if a['id'] == aid:
            a.setdefault('comments',[]).append({
                'id':'c'+str(uuid.uuid4())[:8],
                'user':user,
                'content':content,
                'time':now(),
                'approved':False
            })
            write_json('articles', articles)
            return jsonify({'ok':True})
    return jsonify({'ok':False,'msg':'文章不存在'})

@app.route('/api/upload', methods=['POST'])
def api_upload():
    role = check_role()
    if not role or role not in ('superadmin','content'): return jsonify({'ok':False,'msg':'权限不足'})
    if 'file' not in request.files: return jsonify({'ok':False,'msg':'未选择文件'})
    f = request.files['file']
    if not f.filename: return jsonify({'ok':False,'msg':'文件名为空'})
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ('.jpg','.jpeg','.png','.gif','.webp','.svg'): return jsonify({'ok':False,'msg':'不支持的文件格式'})
    name = str(uuid.uuid4())[:12] + ext
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    f.save(os.path.join(UPLOAD_DIR, name))
    return jsonify({'ok':True,'url':'/uploads/'+name})

if __name__ == '__main__':
    port = 5099
    print(f'Cii.China 服务器启动: http://localhost:{port}')
    print(f'前台: http://localhost:{port}')
    print(f'后台: http://localhost:{port}/admin')
    app.run(host='0.0.0.0', port=port, debug=False)
