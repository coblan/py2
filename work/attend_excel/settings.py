from mytime import Time

lateLevel={
    'late1':["8:31","8:45"],
    'late2':["8:46","9:30"],
    'late3':["9:31","17:30"]
}


for k ,v in lateLevel.items():
    lateLevel[k]=[Time.strptime(str_) for str_ in v]