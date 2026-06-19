from flask import Flask, request, jsonify, send_from_directory
import json, os, uuid, threading, datetime

app = Flask(__name__, static_folder='.', static_url_path='')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
LOCK = threading.Lock()

def data_path(name): return os.path.join(DATA_DIR, name + '.json')

def read_json(name):
    p = data_path(name)
    if not os.path.exists(p): return {}
    with LOCK:
        with open(p, 'r', encoding='utf-8') as f: return json.load(f)

def write_json(name, data):
    with LOCK:
        with open(data_path(name), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def now(): return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

SECTIONS_DATA = [
  {"key":"shizheng","name":"时政深一度","parent":"","order":1},
  {"key":"fenghuo","name":"烽火铁甲","parent":"","order":2},
  {"key":"jingwei","name":"经纬脉搏","parent":"","order":3},
  {"key":"sheji","name":"社稷春秋","parent":"","order":4},
  {"key":"houxique","name":"后稀缺时代","parent":"","order":5},
  {"key":"keji","name":"科技双刃","parent":"houxique","order":1},
  {"key":"zhineng","name":"智能革命","parent":"keji","order":1},
  {"key":"jiyin","name":"基因边界","parent":"keji","order":2},
  {"key":"xushi","name":"虚实重构","parent":"keji","order":3},
  {"key":"nengyuan","name":"能源革命","parent":"keji","order":4},
  {"key":"diyuan","name":"地缘裂变","parent":"keji","order":5},
  {"key":"diqiu","name":"地球工程","parent":"keji","order":6},
  {"key":"liebian","name":"裂变重溯","parent":"houxique","order":2},
  {"key":"gongying","name":"供应链战","parent":"liebian","order":1},
  {"key":"duobian","name":"多边新生","parent":"liebian","order":2},
  {"key":"zimeiti","name":"自媒体悖论","parent":"liebian","order":3},
  {"key":"renzhi","name":"认知升维","parent":"liebian","order":4},
  {"key":"xushiwen","name":"虚实文明","parent":"liebian","order":5},
  {"key":"qidian","name":"奇点信仰","parent":"liebian","order":6},
  {"key":"lanxing","name":"蓝星体系","parent":"","order":6},
  {"key":"ziyuan","name":"资源配置","parent":"lanxing","order":1},
  {"key":"jiyinsu","name":"基因溯源","parent":"ziyuan","order":1},
  {"key":"zijiao","name":"资源角力","parent":"ziyuan","order":2},
  {"key":"shengtai","name":"生态武器","parent":"ziyuan","order":3},
  {"key":"zhenying","name":"阵营博弈","parent":"ziyuan","order":4},
  {"key":"dailiren","name":"代理人战","parent":"ziyuan","order":5},
  {"key":"wenmingg","name":"文明公约","parent":"ziyuan","order":6},
  {"key":"chongtu","name":"冲突重构","parent":"lanxing","order":2},
  {"key":"yineng","name":"异能觉醒","parent":"chongtu","order":1},
  {"key":"hongan","name":"红岸突围","parent":"chongtu","order":2},
  {"key":"shengwei","name":"升维实验","parent":"chongtu","order":3},
  {"key":"xingji","name":"星际建构","parent":"chongtu","order":4},
  {"key":"jinqu","name":"禁区法则","parent":"chongtu","order":5},
  {"key":"pingdeng","name":"平等转型","parent":"chongtu","order":6},
  {"key":"diwai","name":"地外文明","parent":"","order":7},
  {"key":"kexue","name":"科学探索","parent":"diwai","order":1},
  {"key":"shenkong","name":"深空探秘","parent":"kexue","order":1},
  {"key":"xingxing","name":"行星考古","parent":"kexue","order":2},
  {"key":"guance","name":"观测矩阵","parent":"kexue","order":3},
  {"key":"yixing","name":"异星生态","parent":"kexue","order":4},
  {"key":"jiduan","name":"极端适应","parent":"kexue","order":5},
  {"key":"shengwub","name":"生物标踪","parent":"kexue","order":6},
  {"key":"wenmingb","name":"文明博弈","parent":"diwai","order":2},
  {"key":"jiechu","name":"接触准则","parent":"wenmingb","order":1},
  {"key":"chongtu2","name":"冲突预案","parent":"wenmingb","order":2},
  {"key":"xinyang","name":"信仰重构","parent":"wenmingb","order":3},
  {"key":"lianhe","name":"联合探秘","parent":"wenmingb","order":4},
  {"key":"gongmin","name":"公民科探","parent":"wenmingb","order":5},
  {"key":"kechuan","name":"科传平衡","parent":"wenmingb","order":6},
  {"key":"pojian","name":"破茧者说","parent":"","order":8},
  {"key":"xindeng","name":"心灯无界","parent":"","order":9}
]

def ensure_defaults():
    if not os.path.exists(data_path('admins')):
        write_json('admins', [
            {'id':'s1','user':'superadmin','pass':'admin123','role':'superadmin','name':'超级管理员'},
            {'id':'c1','user':'content','pass':'content123','role':'content','name':'内容管理员'},
            {'id':'t1','user':'template','pass':'template123','role':'template','name':'模板管理员'}
        ])
    if not os.path.exists(data_path('sections')):
        write_json('sections', SECTIONS_DATA)
    if not os.path.exists(data_path('articles')):
        write_json('articles', [])
    if not os.path.exists(data_path('videos')):
        write_json('videos', [])
    if not os.path.exists(data_path('templates')):
        write_json('templates', [
            {'id':'t1','name':'暗色科技','icon':'🚀','active':True,'css':':root{--bg:#050510;--bg2:#0a0a1a;--bg3:rgba(255,255,255,0.03);--bg4:rgba(0,200,255,0.05);--primary:#00c8ff;--secondary:#7b61ff;--accent:#ff61d8;--text:#e0e0e0;--text2:#8aaec8;--text3:#5a7a90;--border:rgba(0,200,255,0.12);--card-bg:rgba(255,255,255,0.03);--card-hover:rgba(0,200,255,0.06);--header-bg:linear-gradient(180deg,rgba(5,5,16,0.95),transparent);--font:\'Microsoft YaHei\',\'PingFang SC\',sans-serif;--radius:12px;--glow:0 0 30px rgba(0,200,255,0.08);--hero-gradient:linear-gradient(135deg,#00c8ff,#7b61ff)}'},
            {'id':'t2','name':'中国水墨','icon':'🎋','active':False,'css':':root{--bg:#f5f0e8;--bg2:#ede4d3;--bg3:rgba(0,0,0,0.02);--bg4:rgba(180,120,60,0.06);--primary:#8b4513;--secondary:#6b3410;--accent:#c4a265;--text:#2a1a0a;--text2:#6a5a4a;--text3:#9a8a7a;--border:rgba(139,69,19,0.15);--card-bg:rgba(255,255,255,0.5);--card-hover:rgba(255,255,255,0.7);--header-bg:linear-gradient(180deg,rgba(245,240,232,0.95),transparent);--font:\'STKaiti\',\'KaiTi\',\'SimSun\',serif;--radius:8px;--glow:0 0 20px rgba(139,69,19,0.06);--hero-gradient:linear-gradient(135deg,#8b4513,#c4a265)}'},
            {'id':'t3','name':'极简白','icon':'✨','active':False,'css':':root{--bg:#ffffff;--bg2:#f5f7fa;--bg3:rgba(0,0,0,0.02);--bg4:rgba(0,120,255,0.04);--primary:#0066cc;--secondary:#004999;--accent:#ff6600;--text:#1a1a2e;--text2:#4a5a6a;--text3:#8a9aaa;--border:rgba(0,0,0,0.08);--card-bg:#ffffff;--card-hover:rgba(0,120,255,0.04);--header-bg:linear-gradient(180deg,rgba(255,255,255,0.95),transparent);--font:\'Microsoft YaHei\',\'PingFang SC\',sans-serif;--radius:10px;--glow:0 0 20px rgba(0,102,204,0.06);--hero-gradient:linear-gradient(135deg,#0066cc,#004999)}'}
        ])
    if not os.path.exists(data_path('session')):
        write_json('session', {})
    if not os.path.exists(data_path('members')):
        write_json('members', [])

ensure_defaults()

def get_section_tree():
    sections = read_json('sections')
    if isinstance(sections, list): return sections
    return []

def get_children(parent_key, all_sec):
    return [s for s in all_sec if s.get('parent') == parent_key]

@app.route('/')
def index(): return send_from_directory('.', 'index.html')
@app.route('/admin')
def admin(): return send_from_directory('.', 'admin.html')
@app.route('/uploads/<path:filename>')
def uploaded(filename): return send_from_directory(UPLOAD_DIR, filename)

@app.route('/api/login', methods=['POST'])
def api_login():
    body = request.get_json()
    for a in read_json('admins'):
        if a['user'] == body.get('user','') and a['pass'] == body.get('pass',''):
            write_json('session', {'user':a['user'],'role':a['role'],'time':now()})
            return jsonify({'ok':True,'user':a['user'],'role':a['role']})
    return jsonify({'ok':False,'msg':'用户名或密码错误'})

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
    write_json('session', {}); return jsonify({'ok':False})

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
        'sections': read_json('sections'),
        'members': read_json('members')
    })

@app.route('/api/data', methods=['POST'])
def api_save_data():
    body = request.get_json(); role = check_role()
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
        'sections': get_section_tree()
    })

@app.route('/api/template/css')
def api_template_css():
    tmpl = read_json('templates')
    active = next((t for t in tmpl if t.get('active')), tmpl[0] if tmpl else None)
    return jsonify({'name':active['name'] if active else '默认','css':active['css'] if active else ''})

@app.route('/api/comments', methods=['GET'])
def api_get_comments():
    all_comments = []
    for a in read_json('articles'):
        for c in a.get('comments',[]):
            c['articleTitle'] = a['title']; c['articleId'] = a['id']; all_comments.append(c)
    return jsonify(all_comments)

@app.route('/api/comments/approve', methods=['POST'])
def api_approve_comment():
    role = check_role()
    if not role or role not in ('superadmin','content'): return jsonify({'ok':False,'msg':'权限不足'})
    body = request.get_json()
    articles = read_json('articles')
    for a in articles:
        for c in a.get('comments',[]):
            if c['id'] == body.get('id'): c['approved'] = body.get('approved',True); write_json('articles', articles); return jsonify({'ok':True})
    return jsonify({'ok':False,'msg':'未找到留言'})

@app.route('/api/comments/delete', methods=['POST'])
def api_delete_comment():
    role = check_role()
    if not role or role not in ('superadmin','content'): return jsonify({'ok':False,'msg':'权限不足'})
    cid = request.get_json().get('id')
    articles = read_json('articles')
    for a in articles: a['comments'] = [c for c in a.get('comments',[]) if c['id'] != cid]
    write_json('articles', articles); return jsonify({'ok':True})

# ===== MEMBER API =====
MEMBER_LEVELS = {'normal':'普通会员','vip1':'VIP会员','vip2':'黄金VIP','vip3':'钻石VIP'}

def get_member_session():
    s = read_json('session')
    mid = s.get('member_id','')
    if not mid: return None
    members = read_json('members')
    for m in members:
        if m['id'] == mid: return m
    return None

def save_member_session(mid):
    s = read_json('session')
    s['member_id'] = mid
    write_json('session', s)

def clear_member_session():
    s = read_json('session')
    s.pop('member_id', None)
    write_json('session', s)

@app.route('/api/member/register', methods=['POST'])
def api_member_register():
    body = request.get_json()
    user = (body.get('user') or '').strip()
    pwd = (body.get('pass') or '').strip()
    if not user or not pwd: return jsonify({'ok':False,'msg':'用户名和密码不能为空'})
    if len(user) < 2 or len(user) > 20: return jsonify({'ok':False,'msg':'用户名长度2-20个字符'})
    if len(pwd) < 4: return jsonify({'ok':False,'msg':'密码至少4位'})
    members = read_json('members')
    if any(m['user'] == user for m in members): return jsonify({'ok':False,'msg':'用户名已存在'})
    new_member = {
        'id': 'm' + str(uuid.uuid4())[:8],
        'user': user, 'pass': pwd,
        'level': 'normal', 'points': 0,
        'registerDate': now(), 'avatar': '',
        'commentCount': 0
    }
    members.append(new_member)
    write_json('members', members)
    save_member_session(new_member['id'])
    return jsonify({'ok':True, 'member':{'id':new_member['id'],'user':new_member['user'],'level':new_member['level'],'points':new_member['points']}})

@app.route('/api/member/login', methods=['POST'])
def api_member_login():
    body = request.get_json()
    user = (body.get('user') or '').strip()
    pwd = (body.get('pass') or '').strip()
    if not user or not pwd: return jsonify({'ok':False,'msg':'请输入用户名和密码'})
    members = read_json('members')
    for m in members:
        if m['user'] == user and m['pass'] == pwd:
            save_member_session(m['id'])
            return jsonify({'ok':True, 'member':{'id':m['id'],'user':m['user'],'level':m['level'],'points':m['points']}})
    return jsonify({'ok':False,'msg':'用户名或密码错误'})

@app.route('/api/member/session')
def api_member_session():
    m = get_member_session()
    if m: return jsonify({'ok':True, 'member':{'id':m['id'],'user':m['user'],'level':m['level'],'points':m['points']}})
    return jsonify({'ok':False})

@app.route('/api/member/logout', methods=['POST'])
def api_member_logout():
    clear_member_session()
    return jsonify({'ok':True})

@app.route('/api/members', methods=['GET'])
def api_get_members():
    role = check_role()
    if not role or role not in ('superadmin','content'): return jsonify({'ok':False,'msg':'权限不足'})
    members = read_json('members')
    return jsonify(members)

@app.route('/api/members/update', methods=['POST'])
def api_update_member():
    role = check_role()
    if not role or role not in ('superadmin','content'): return jsonify({'ok':False,'msg':'权限不足'})
    body = request.get_json()
    mid = body.get('id'); new_level = body.get('level')
    if not mid or new_level not in MEMBER_LEVELS: return jsonify({'ok':False,'msg':'参数错误'})
    members = read_json('members')
    for m in members:
        if m['id'] == mid: m['level'] = new_level; write_json('members', members); return jsonify({'ok':True})
    return jsonify({'ok':False,'msg':'未找到会员'})

@app.route('/api/members/delete', methods=['POST'])
def api_delete_member():
    role = check_role()
    if not role or role not in ('superadmin','content'): return jsonify({'ok':False,'msg':'权限不足'})
    mid = request.get_json().get('id')
    members = read_json('members')
    members = [m for m in members if m['id'] != mid]
    write_json('members', members)
    return jsonify({'ok':True})

@app.route('/api/comment', methods=['POST'])
def api_add_comment():
    body = request.get_json()
    aid = body.get('articleId'); content = body.get('content','').strip()
    if not aid or not content: return jsonify({'ok':False,'msg':'参数不完整'})
    member = get_member_session()
    user = member['user'] if member else (body.get('user','访客').strip() or '访客')
    level = member['level'] if member else ''
    articles = read_json('articles')
    for a in articles:
        if a['id'] == aid:
            cmt = {'id':'c'+str(uuid.uuid4())[:8],'user':user,'content':content,'time':now(),'approved':False}
            if level: cmt['memberLevel'] = level
            a.setdefault('comments',[]).append(cmt)
            write_json('articles', articles)
            # update member comment count
            if member:
                members = read_json('members')
                for m in members:
                    if m['id'] == member['id']:
                        m['commentCount'] = m.get('commentCount',0) + 1
                        m['points'] = m.get('points',0) + 1
                        write_json('members', members)
                        break
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
    if ext not in ('.jpg','.jpeg','.png','.gif','.webp','.svg','.mp4','.webm','.mov','.avi','.mkv'): return jsonify({'ok':False,'msg':'不支持的文件格式'})
    name = str(uuid.uuid4())[:12] + ext
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    f.save(os.path.join(UPLOAD_DIR, name))
    url = '/uploads/'+name
    if ext in ('.mp4','.webm','.mov','.avi','.mkv'):
        url = name
    return jsonify({'ok':True,'url':'/uploads/'+name})

if __name__ == '__main__':
    port = 5099
    print(f'Cii.China 服务器启动: http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=False)
