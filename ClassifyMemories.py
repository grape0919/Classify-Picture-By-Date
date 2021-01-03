from EXIFUtil import EXIFGetter
import os
import shutil

class Classfier:
    Getter = EXIFGetter(None)

    @classmethod
    def classifyImg(self, img):
        if img.lower().endswith('.mp4'):
            # print("!@#!@# This file is type of mp4")
            if not os.path.isdir('memories/'+'ect'):
                os.mkdir('memories/'+'ect')
            if not os.path.exists(img):
                try:
                    fcopy(img,'memories/'+'ect')
            # except shutil.SameFileError:
            #     pass
                except PermissionError:
                    with open("./FailedList.log", "a") as file:
                        file.write(img)
                        file.write('\n')
        elif img.lower().endswith('.jpg'):
            # print("!@#!@# This file is type of .jpg")
            getter = False
            try:
                getter = self.Getter.loadEXIF(img)
            except PermissionError:
                with open("./FailedList.log", "a") as file:
                    try:
                        fcopy(img,'memories/'+'ect')
                    except PermissionError:
                        with open("./FailedList.log", "a") as file:
                            file.write(img)
                            file.write('\n')
            if getter is False:
                # print("!@#!@#!@# EXIF 가 존재하지 않습니다.")
                if not os.path.isdir('memories/'+'ect'):
                    os.mkdir('memories/'+'ect')
                if not os.path.exists(img):
                    try:
                        fcopy(img,'ect')
                    except PermissionError:
                        with open("./FailedList.log", "a") as file:
                            file.write(img)
                            file.write('\n')

            else:
                # print("!@#!@#!@# EXIF 가 존재합니다.")
                try:

                    date = self.Getter.getDate()
                
                except PermissionError:
                    date = None

                if date:
                    date = date.split(':')
                    year = date[0]
                    month = date[1]
                    day = date[2]

                    if not os.path.isdir('memories/'+year):
                        os.mkdir('memories/'+year)

                    if not os.path.isdir('memories/'+year + '/' + month):
                        os.mkdir('memories/'+year + '/' + month)

                    if not os.path.isdir('memories/'+year + '/' + month + '/' + day):
                        os.mkdir('memories/'+year + '/' + month + '/' + day)

                    fcopy(img,'memories/'+year + '/' + month + '/' + day)
                else:
                    # print("!@#!@# date 데이터가 없습니다.")
                    if not os.path.isdir('memories/'+'ect'):
                        os.mkdir('memories/'+'ect')
                    fcopy(img,'memories/'+'ect')
        else:
            # print("!@#!# This is not media file")
            if not os.path.isdir('memories/'+'ect'):
                os.mkdir('memories/'+'ect')

            fcopy(img,'memories/'+'ect')    
        # except shutil.SameFileError:
        #     pass

    @classmethod
    def folderScanner(self, folder_path):
        temp = []
        file_list = os.listdir(folder_path)
        for f in file_list:
            if os.path.isdir(folder_path+"/"+f):
                temp.extend(self.folderScanner(folder_path+"/"+f))
            elif os.path.isfile(folder_path+"/"+f):
                if f.lower().endswith('.jpg') or f.lower().endswith('.mp4'):
                    temp.append(folder_path+"/"+f)

        return temp

def fcopy(source, target):
    if os.path.isdir(target):
        target = target + "/" + os.path.basename(source)
    
    try:
        print("start copy")
        with open(source, 'rb') as f:
            data = f.read()
        with open(target, 'wb') as t:
            t.write(data)

    except PermissionError:
        with open("./FailedList.log", "a") as file:
            file.write(target)
            file.write('\n')


if __name__ == "__main__" :

    # root_path = "D:/HONGKYO/사진백업20191007"
    # root_path = "D:/HONGKYO/NOTE20백업"
    root_path = './memories'
    file_list = Classfier.folderScanner(root_path)
    
    print('file count = ', len(file_list))
    # for file in file_list:
    #     print("file : ", file)
    #     Classfier.classifyImg(file)
    # Classfier.classifyImg('D:/HONGKYO/NOTE20백업/Camera/20200517_113943.jpg')