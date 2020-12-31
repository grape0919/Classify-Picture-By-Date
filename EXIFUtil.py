from PIL import Image
from PIL.ExifTags import TAGS


class EXIFGetter :
    IMAGE_FILE_PATH = ''
    EXIF = None
    
    def __init__(self, image):
        if image:
            self.loadEXIF(image)

    def loadEXIF(self, image):
        self.IMAGE_FILE_PATH = image
        img = Image.open(self.IMAGE_FILE_PATH)
        info = img._getexif()
        self.EXIF = {}
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                self.EXIF[decoded] = value
        
            return self.EXIF
        else:
            return False

    def getDate(self):
        if self.EXIF is not None and 'DateTime' in self.EXIF.keys():
            data_str= self.EXIF['DateTime']
            data_str = data_str.split(' ')
            if len(data_str) == 2:
                return data_str[0]
        else :
            return None

    def getGPSInfo(self):
        exifGPS = self.EXIF['GPSInfo']
        print('!@#!@# GPSInfo : ', exifGPS)
        latData = exifGPS[2]
        lonData = exifGPS[4]
        # calculae the lat / long
        print('!@#!@# latData : ', latData)
        print('!@#!@# lonData : ', lonData)
        latDeg = latData[0][0] / float(latData[0][1])
        latMin = latData[1][0] / float(latData[1][1])
        latSec = latData[2][0] / float(latData[2][1])
        lonDeg = lonData[0][0] / float(lonData[0][1])
        lonMin = lonData[1][0] / float(lonData[1][1])
        lonSec = lonData[2][0] / float(lonData[2][1])
        # correct the lat/lon based on N/E/W/S
        Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
        if exifGPS[1] == 'S': 
            Lat = Lat * -1
        Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
        if exifGPS[3] == 'W': 
            Lon = Lon * -1

        #TODO
        #지오코더 (좌표 to 주소)
        #구현