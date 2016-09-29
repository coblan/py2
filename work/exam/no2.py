def lovely_print_name(content):
    clean_content=content.strip()
    length=len(clean_content)+2
    star_space='*'*length
    print('*'+star_space+'*')
    print('* '+clean_content+' *')
    print('*'+star_space+'*')


lovely_print_name('shelly millon')