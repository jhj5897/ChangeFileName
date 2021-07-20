import os
import re
import shutil
import ChangeFileName as FNT


def execute(self, src, oldStr, newStr, oldOption, newOption, isBlankCheck):
    # oldOption(True = 옮기기 / False = 삭제)
    # newOption(True = 옮기기 / False = 냅두기)
    count = 0

    try:
        files = os.listdir(src)
        p = re.compile(oldStr) if not isBlankCheck else re.compile(oldStr.replace(" ", "[_ ]?"))

        if oldOption:
            oldDist = src + "\\old(%s)" % oldStr
            if not os.path.exists(oldDist):
                os.mkdir(oldDist)

        if newOption:
            newDist = src + "\\new(%s)" % newStr
            if not os.path.exists(newDist):
                os.mkdir(newDist)
        else:
            newDist = src

        for file in files:
            oldFilePath = src + "\\" + file
            changedFileName = p.sub(newStr, file)
            if p.search(file) and os.path.isfile(oldFilePath):

                if os.path.exists(os.path.join(newDist, changedFileName)):
                    reply = FNT.ChangeFileName.alertMessageDiaglog(self, "파일 존재함",
                                                                     "다음 파일이 이미 존재합니다. 덮어쓰시겠습니까?\n" + changedFileName)
                    if not reply:
                        continue

                if oldOption: 
                    shutil.copy(oldFilePath, os.path.join(oldDist, file))   #원본 복사

                os.rename(oldFilePath, os.path.join(src, changedFileName))    #파일 이름 수정

                if newOption:
                    shutil.move(os.path.join(src, changedFileName), os.path.join(newDist, changedFileName)) #남아있던 파일 이동
                
                count+=1


        if count==0:
            countSentence = "수정할 파일을 찾지 못했습니다."
            if oldOption and not os.listdir(oldDist):
                os.rmdir(oldDist)
            if newOption and not os.listdir(newDist):
                os.rmdir(newDist)
        else:
            countSentence = ("총 %d 개의 파일을 수정했습니다." % count)

        FNT.ChangeFileName.alertInformationDiaglog(self, "알림", countSentence)
    except Exception as e:
        FNT.ChangeFileName.alertInformationDiaglog(self, "Error", "%d개의 파일을 수정하던 중, 다음과 같은 오류가 발생했습니다.\n%s" % (count, str(e)))