FILE_EXTENSION = '.m'
MUSIC_DIR = 'm_files/'

def get_file(path: str) -> tuple:
    if not '_' in path:
        return False, None, None
    parts = path.split('_')
    return True, parts[-2], int(parts[-1][0:-len(FILE_EXTENSION)])

def get_path(name: str, num: int) -> str:
    return '{}{}_{:03d}{}'.format(MUSIC_DIR, name, num, FILE_EXTENSION)