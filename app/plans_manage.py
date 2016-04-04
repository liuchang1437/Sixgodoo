def create_plans(id,count):
    with open('static/plans/%s' % id,'w+') as f:
        f.write('%d\n' %count)
        for i in range(0,count):
            f.write('0')
def is_n(id, n):
    with open('static/plans/%s' %id,'r+') as f:
        progress=f.readlines()
        progress=progress[1]
        if progress[n-1]== '0':
            return False
        else:
            return True
def set_n(id, ,count,n):
    with open('static/plans/%s' %id,'r+') as f:
        progress=f.readlines()
        progress=progress[1]
        progress[n-1]= '1'
        f.write('%d\n' %count)
        for i in range(0,count):
            f.write(progress[i])
