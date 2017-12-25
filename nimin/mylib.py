# -*- coding: utf-8 -*-
from blogDB import get_db

def createPagn(page,pMax):
    if page>pMax or page<1:
        return []
    pagn = [[x,'',x] for x in range(max(1,page-4),min(pMax,page+4)+1)]
    pagn[min(page-1,4)][1]='active'
    if page==1:
        before=[]
    else:
        before=[['','prev',page-1],]
    if page==pMax:
        after=[]
    else:
        after=[['','next',page+1],]
    pagn = before+pagn+after
    return pagn

class PostList:
    def __init__(self,section = 0,pid = 1):
        self.section = section
        self.offset = ( pid - 1 ) * 10
        self.page = pid
    def getAl(self):
        try:
            blogdb = get_db()
            cur = blogdb.cursor()
            if self.section:
                cur.execute('SELECT id,name,img,quote,content,section,date FROM posts WHERE owner = 0 and section = %s ORDER BY hot DESC LIMIT 10 OFFSET %s',(self.section,self.offset,))
            else:
                cur.execute('SELECT id,name,img,quote,content,section,date FROM posts WHERE owner = 0 ORDER BY hot DESC LIMIT 10 OFFSET %s',(self.offset,))
            curPosts = cur.fetchall()
            results=[]
            for curPost in curPosts:
                temp = Post(curPost[0],curPost[1],curPost[2],curPost[3],curPost[4],curPost[5],curPost[6])
                temp.getRep()
                results.append(temp)
            self.results = results
            if self.section:
                cur.execute('SELECT count(*) FROM posts WHERE owner = 0 and section = %s;',(self.section,))
            else:
                cur.execute('SELECT count(*) FROM posts where owner = 0;')
            pMax = cur.fetchall()
            pMax = (int(pMax[0][0])+9)/10
            self.pagn = createPagn(self.page,pMax)
            return True
        except:
            return False

class Post:
    def __init__(self,id='',name='',img='',quote='',content='',section='',date=''):
        self.id = id
        self.name = name
        self.img = img
        self.quote = quote
        self.content = content
        self.section = section
        self.date = date
    def getIt(self,pid=1):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT name,img,quote,content,section,date FROM posts WHERE id = %s',(self.id,))
        arti = cur.fetchall()[0]
        self.name = arti[0]
        self.img = arti[1]
        self.quote = arti[2]
        self.content = arti[3]
        self.section = arti[4]
        self.date = arti[5]
        cur.execute('SELECT id,name,img,content,date FROM posts WHERE owner = %s ORDER BY id LIMIT %s OFFSET %s',(self.id,10,(pid-1)*10))
        self.reply = cur.fetchall()
        cur.execute('SELECT count(*) FROM posts where owner = %s;',(self.id,))
        pMax = cur.fetchall()
        pMax = (int(pMax[0][0])+9)/10
        self.pagn = createPagn(pid,pMax)
        return True
    def getRep(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT id,name,img,content,date FROM posts WHERE owner = %s ORDER BY id LIMIT 5',(self.id,))
        self.reply = cur.fetchall()
        cur.execute('SELECT count(*) FROM posts where owner = %s;',(self.id,))
        pMax = cur.fetchall()
        self.pagn = pMax[0][0]
        return True
    def newPost(self,author,img,quote,content,section,ip,owner):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('insert into posts (name,img,quote,content,section,ip,owner,hot) values (%s, %s, %s, %s, %s, %s, %s,CURRENT_TIMESTAMP)', (author,(img or ""),(quote or ""),content,section,ip,owner))
        if section:
            cur.execute('select @@IDENTITY')
            blog = cur.fetchall()[0][0]
            blogdb.commit()
            return blog
        else:
            cur.execute('update posts set hot = CURRENT_TIMESTAMP where id = %s', (owner,))
            return owner
    def getPg(self,pid):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT count(*) FROM posts where owner = %s and id < %s;',(self.id,pid))
        pg = cur.fetchall()
        pg = (int(pg[0][0])+10)/10
        return pg
    def dele(self,tid):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('DELETE FROM `posts` where `id` = %s or `owner` = %s;',(tid,tid,))
        return 0