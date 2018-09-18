import copy
import string
class compiler:
    def __init__(self):
        self.lists=[]
        self.productions=[]
        self.tot=0
        self.maps={}
        self.mirror=[]#unterminals
        self.terminals=[]
        self.first={}
        self.follow={}
        self.table={}
    def get_productions(self):
        filename='syntax.txt'
        fp=open(filename,'r')
        lis=fp.readlines()
        for i in range(len(lis)):
            tmp=[]
            self.lists.append(lis[i].split())
            if self.lists[i][0] not in self.maps.keys():
                self.maps[self.lists[i][0]]=self.tot
                self.mirror.append(self.lists[i][0])
                self.productions.append([])
                self.tot+=1
            self.productions[self.maps[self.lists[i][0]]].append(i)
        fp.close()
        for x in self.mirror:
            for k in self.productions[self.maps[x]]:
                item=self.lists[k][2:]
                for y in item:
                    if (y not in self.mirror) and (y not in self.terminals):
                        self.terminals.append(y)
    def eliminate_left_recursive(self):
        fjsdl=len(self.mirror)
        for i in range(fjsdl):
            x=self.mirror[i]
            lre=[]
            nre=[]
            for k in self.productions[self.maps[x]]:
                item=self.lists[k][2:]
                if item[0]==x:
                    lre.append(k)
                else:
                    nre.append(k)
            if len(lre)==0:
                continue
            
            tmps=x+"'"
            self.mirror.append(tmps)
            self.maps[tmps]=self.tot
            self.tot+=1
            for k in nre:
                self.lists[k].append(tmps)
            self.productions[self.maps[x]]=nre

            self.lists.append([tmps,'->','empty'])
            for k in lre:
                self.lists[k][0]=tmps
                self.lists[k].remove(self.lists[k][2])
                self.lists[k].append(tmps)
            lre.append(len(self.lists)-1)
            self.productions.append([])
            self.productions[self.maps[tmps]]=lre
    def calc_first(self):
        self.first[self.mirror[0]]=set()
        change=True
        while change:
            change=False
            for x in self.mirror:
                for k in self.productions[self.maps[x]]:
                    item=self.lists[k][2:]
                    flag=True
                    for i in range(len(item)):
                        y=item[i]
                        if y not in self.first.keys():
                            self.first[y]=set()
                            if y not in self.mirror:
                                self.first[y].add(y)
                            change=True
                        if flag:
                            tmp=len(self.first[x])
                            self.first[x]=self.first[x] | self.first[y]
                            if tmp<len(self.first[x]):
                                change=True
                        if 'empty' not in self.first[y]:
                            flag=False
    def calc_follow(self):
        for x in self.mirror:
            self.follow[x]=set()
        self.follow[self.mirror[0]].add('$')
        for x in self.mirror:
            for k in self.productions[self.maps[x]]:
                item=self.lists[k][2:]
                for i in range(len(item)-1):
                    y=item[i]
                    if y not in self.mirror:
                        continue
                    self.follow[y]=self.follow[y] | self.first[item[i+1]]
        change=True
        while change:
            change=False
            for x in self.mirror:
                for k in self.productions[self.maps[x]]:
                    item=self.lists[k][2:]
                    for i in range(len(item)-1,-1,-1):
                        y=item[i]
                        if y=='empty':
                            continue
                        if y not in self.mirror:
                            break
                        tmp=len(self.follow[y])
                        self.follow[y]=self.follow[y] | self.follow[x]
                        if tmp<len(self.follow[y]):
                            change=True
                        if 'empty' not in self.first[y]:
                            break
        for x in self.mirror:
            if 'empty' in self.follow[x]:
                self.follow[x].remove('empty')
    def calc_table(self):
        for x in self.mirror:
            for y in self.terminals:
                self.table[(x,y)]=set()
            self.table[(x,'$')]=set()
        for x in self.mirror:
            for k in self.productions[self.maps[x]]:
                item=self.lists[k][2:]
                flag=True
                for y in item:
                    if (y in self.terminals) and (y != 'empty'):
                        self.table[(x,y)].add(k)
                        flag=False
                        break
                    if (y in self.mirror):
                        for z in self.first[y]:
                            if z != 'empty':
                                self.table[(x,z)].add(k)
                    if 'empty' not in self.first[y]:
                        flag=False
                        break
                if flag:
                    for y in self.follow[x]:
                        self.table[x,y].add(k)
    def output_table(self):
        fp=open('predict_table.txt','w')
        self.terminals.append('$')
        tmp=''
        fp.write(tmp.ljust(20))
        for x in self.terminals:
            if x=='empty':
                continue
            fp.write(x.ljust(20))
        fp.write("\n")
        for x in self.mirror:
            fp.write(x.ljust(20))
            for y in self.terminals:
                if y=='empty':
                    continue
                if len(self.table[(x,y)])==0:
                    fp.write(tmp.ljust(20))
                    continue
                s=''
                for k in self.table[(x,y)]:
                    z=tmp.join(self.lists[k])
                    s=s+z+';'
                fp.write(s.ljust(20))
            fp.write("\n")
        fp.close()
def test():
    c=compiler()
    c.get_productions()
    for item in c.lists:
        print item
    print
    c.eliminate_left_recursive()
    for item in c.lists:
        print item
    c.calc_first()
    print c.first
    c.calc_follow()
    print c.follow
    c.calc_table()
    c.output_table()
def main():
    c=compiler()
    c.get_productions()
    c.eliminate_left_recursive()
    c.calc_first()
    c.calc_follow()
    c.calc_table()
    c.output_table()

if __name__=="__main__":
    main()
