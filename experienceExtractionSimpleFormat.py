
import pdfplumber
import io
import re
def experience(filepath):
    text_file = open('sample.txt', 'w',encoding="utf-8") 
    pdf = pdfplumber.open(filepath)
    for page in range(len(pdf.pages)):
        text_file.write(pdf.pages[page].extract_text())
    text_file.close()
    text_file = open('sample.txt', 'r',encoding="utf-8") 
    txt=text_file.read()
   
    exp_text=([ t for t in txt.split('. ') if 'experience' in t and ('years' in t or 'year' in t)])


    exp_text=str(exp_text)
    exp_text=exp_text.replace('\\n','')
    exp_text=str(exp_text)
    exp_text=exp_text.replace('\\','')
    

    pattern0=r"\d{1,2}\\*\.\d*\+\syears"
    pattern1=r"\d{1,2}\\*\.\d\syears"
    pattern2=r"\d{1,2}\\*\+\syears"
    pattern3=r"\d{1,2}\syears"

    patternList=[pattern0,pattern1,pattern2,pattern3]
    gotMatch = False
    for pattern in patternList:
        experience = re.findall(pattern,exp_text)
        if experience:
            gotMatch = True
            break



        
    if len(experience)!=0:
        patternForYear=r"\d{1,2}"
        yearOfExperience=re.findall(patternForYear,experience[0])
        return int(yearOfExperience[0])
    else:
        return 0