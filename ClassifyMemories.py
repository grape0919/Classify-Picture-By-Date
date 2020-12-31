from EXIFUtil import EXIFGetter
import os
import shutil

class Classfier:
    Getter = EXIFGetter(None)

    @classmethod
    def classifyImg(self, img):
        getter = self.Getter.loadEXIF(img)
        if getter is False:
            try:
                shutil.copy(img,'ect')
            except shutil.SameFileError:
                pass
        else:
            date = self.Getter.getDate().split(':')
            year = date[0]
            month = date[1]
            day = date[2]

            if not os.path.isdir(year):
                os.mkdir(year)

            if not os.path.isdir(year + '/' + month):
                os.mkdir(year + '/' + month)

            if not os.path.isdir(year + '/' + month + '/' + day):
                os.mkdir(year + '/' + month + '/' + day)

            try:
                shutil.copy(img,year + '/' + month + '/' + day)
            except shutil.SameFileError:
                pass

    @classmethod
    def folderScanner(self, folder_path):
        temp = []
        file_list = os.listdir(folder_path)
        for f in file_list:
            if os.path.isdir(folder_path+"/"+f):
                temp.extend(self.folderScanner(folder_path+"/"+f))
            elif os.path.isfile(folder_path+"/"+f):
                if f.lower().endswith('.jpg'):
                    temp.append(folder_path+"/"+f)

        return temp


if __name__ == "__main__" :

    root_path = "D:/HONGKYO/사진백업20191007"
    file_list = Classfier.folderScanner(root_path)
    
    
    for file in file_list:
        print("file : ", file)
        Classfier.classifyImg(file)