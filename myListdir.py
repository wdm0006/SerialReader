from zipfile import ZipFile, ZipInfo
import os

def myListdir(pathString):
    components=os.path.normpath(pathString).split(os.sep)
    for item in enumerate(components):
        index=item[0]
        component=item[1]
        (root, ext)=os.path.splitext(component)
        if ext=='.zip':
            results=[]
            zipPath=os.sep.join(components[0:index+1])
            archivePath=components[index+1]
            zipobj=ZipFile(zipPath,'r')
            contents=zipobj.namelist()
            zipobj.close()
            for item in enumerate(contents):
                (index,name)=item
                nameComponents-name.split('/')
                if nameComponents[0:-1]==archivePath:
                    results.append(nameComponents[-1])
            return results
        else:
            return previousListDir(pathString)
        pass
previousListDir=os.listdir
os.listdir=myListdir
                                   
        
