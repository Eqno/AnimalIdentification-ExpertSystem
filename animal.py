pre = {} # 前置词
det = {} # 限定词
rule = {} # 规则库
know = {} # 知识库
pun = ['，', '。', '；', '\n'] # 标点
typ = ['动物', '类', '界', '门', '纲', '目', '科', '属', '种']
allname = {} # 全名

def load(n:str, m:dict):
    with open(n, 'r', encoding='utf-8') as f:
        for i, s in enumerate(f.readlines()):
            for j in filter(lambda x: x!='' and x!='\n',
                s.split('#')[0].split(' ')):
                    m[j.replace('\n', '')] = i+1
        f.close()

def query(s:str, m:dict):
    for r, n in know.items():
        # rule
        if s.find(r) != -1:
            for k, v in n.items():
                m[k] = v
            s = s.replace(r, '')
    for r, n in rule.items():
        n = r
        # pre - det - rule
        for i in pre:
            for j in det:
                if s.find(i+j+'的'+r) != -1:
                    m[n] = pre[i]*len(det)+det[j]
                    s = s.replace(i+j+'的'+r, '')
                elif s.find(i+j+r) != -1:
                    m[n] = pre[i]*len(det)+det[j]
                    s = s.replace(i+j+r, '')
        # pre - rule
        for i in pre:
            if s.find(i+'的'+r) != -1:
                m[n] = pre[i]
                s = s.replace(i+'的'+r, '')
            if s.find(i+r) != -1:
                m[n] = pre[i]
                s = s.replace(i+r, '')
        # det - rule
        for i in det:
            if s.find(i+'的'+r) != -1:
                m[n] = det[i]
                s = s.replace(i+'的'+r, '')
            if s.find(i+r) != -1:
                m[n] = det[i]
                s = s.replace(i+r, '')
        # rule
        if s.find(r) != -1:
            m[n] = 0
            s = s.replace(r, '')

def parse(s:str):
    t = s.split('是')
    a = t[0]
    b = t[1]
    for i in pun:
        if b.find(i) != -1:
            b = b.replace(i, '')
    l = {}
    query(a, l)
    c = b.replace('动物', '').replace('类', '')
    allname[c] = b
    return l, c

def learn(n:str):
    with open(n, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            que, ans = parse(i)
            if know.get(ans, False):
                know[ans].update(que)
            else:
                know[ans] = que
        f.close()

def prinl(l:list):
    flag = False
    for i in l:
        if flag:
            print('，', end='')
        else:
            flag = True
        print(i, end='')
    print('。')

def main():
    load('前置词.txt', pre)
    load('限定词.txt', det)
    load('规则库.txt', rule)
    learn('知识库.txt')
    # for i, j in know.items():
    #     print(i, j)
    while True:
        print('请输入查询条件，以“停止”结束：')
        q = input()
        if q == '停止':
            break
        l = {}
        query(q, l)
        flag = False
        for k, v in know.items():
            if len(l.items()-v.items()):
                flag = True
        if not flag:
            print('未知特征。')
            continue
        t = []
        s = []
        for k, v in know.items():
            if not len(l.items()-v.items()):
                a = allname[k]
                flag = False
                for i in typ:
                    if a.find(i) != -1:
                        t.append(a)
                        flag = True
                        break
                if not flag:
                    s.append(a)
        flag = False
        if len(t):
            print('它可能的类型：', end='')
            prinl(t)
            flag = True
        if len(s):
            print('它可能的物种：', end='')
            prinl(s)
            flag = True
        if not flag:
            print('未知物种。')

if __name__ == '__main__':
    main()