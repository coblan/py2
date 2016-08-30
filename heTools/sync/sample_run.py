from sync_code import sync_with_config

dc={
    'ignore_files':'\.pyc$',
    'dirs':[
        (ur'D:\try\hellodj',ur'D:\try\test'),
    ]
}

sync_with_config(dc)