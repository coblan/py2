from mytime import Time
late={
    'late1':["8:30","8:45"],
    'late2':["8:46","9:30"],
    'late3':["9:31","17:30"]
}


for k ,v in late.items():
    late[k]=[Time.strptime(str_) for str_ in v]