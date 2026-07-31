import sqlite3
con = sqlite3.connect('db/zhongyi.db'); con.row_factory = sqlite3.Row; c = con.cursor()
names = ['合谷','足三里','委中','中脘','章门','阳陵泉','悬钟','绝骨','膈俞','大杼',
         '太渊','膻中','公孙','内关','足临泣','外关','后溪','申脉','照海','百会',
         '水沟','人中','关元','气海','神阙','涌泉','三阴交','太冲','风池','大椎','命门']
for n in names:
    r = c.execute('SELECT id,name FROM acupoints WHERE name=?', (n,)).fetchone()
    print(n, (r['id'], r['name']) if r else 'NULL')
con.close()
