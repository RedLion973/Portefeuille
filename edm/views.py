from FUTFactory.edm.models import Folder

def get_folders(folder_id):
    f = Folder.objects.get(id=folder_id)
    tree = '<li><span class="folder">' + f.name + '</span>'
    if not f.documents.all().count() == 0:
        tree += '<ul>'
        for d in f.documents.all():
            tree += '<li><span class="file">' + d.name + '</span></li>'
        tree += '</ul>'
    for folder in f.subfolders.all():
        get_folders(folder.id)
    tree += '</li>'
    return tree