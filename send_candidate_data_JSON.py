import emailAndContact
import tech_stack
import Name_entity_extraction
import Read_from_pdf
import os 
import yearOfExperience
import requests
import skillMatching
import updatedVacancy
import experienceMatching
import jdMatching
import checkExtractedFields
import sendingMailToCandidate

headers={'Content-type':'application/json', 'Accept':'application/json'}
def listToString(s):  
    str1 = " "  
    return (str1.join(s)) 

def send(pdf_file,webLink):
        pdfNamevancancy=pdf_file.split('_')
        Lines=""
        candidate_name=""
        candidate_contact=[]
        candidate_email=[]
        candidate_tech_stack=[]
        Lines=Read_from_pdf.read_text_by_lines(pdf_file)
        text_file=open('demo.txt',encoding="utf-8")
        candidate_name=Name_entity_extraction.name_entity_extraction(Lines,text_file)
        text_file=open('demo.txt',encoding="utf-8")
        txt=text_file.read()
        candidate_contact=emailAndContact.findContact(txt)
        candidate_email=emailAndContact.findEmail(txt)
        candidate_tech_stack=tech_stack.techno_stack(txt)
        candidate_experience=yearOfExperience.getExperience(pdf_file)
        text_file.close()
        #os.remove(pdf_file)
        os.remove('sample.txt')
        os.remove('demo.txt')
        emailAddress=''
        if len(candidate_email)!=0:
                emailAddress=candidate_email[0]
        contactNo=""
        if  len(candidate_contact)==2 and len(candidate_contact)!=0:
                contactNo=candidate_contact[0]+"/"+candidate_contact[1]
        else :
                contactNo=candidate_contact[0]

        candidate_data={
        "candidateName":candidate_name,
        "email":emailAddress,
        "contactNo":contactNo,
        "technologyStack":listToString(candidate_tech_stack),
        "reqMatchingPercent":0,
        "shortSummaryMatchingPercent":0,
        "technologyStackMatchingPercent":0,
        "yearOfExperience":candidate_experience,
        "resumeURL":webLink
        }


        feildsNotFound=checkExtractedFields.whichFieldsNotExtracted(candidate_data)
        if len(feildsNotFound)!=0:
                reciver_mail_address=candidate_data.get('email')
                sendingMailToCandidate.sendMail('akhawatsahdev@gmail.com',feildsNotFound)
                print(candidate_data)
        else:
                        
                if len(pdfNamevancancy)!=0:
                        print(pdfNamevancancy[0])
                        if int(pdfNamevancancy[0])!=0:
                                print('for one vancancy')
                                vacancies=updatedVacancy.getVaccnacyByid(int(pdfNamevancancy[0]))
                                print(vacancies.json().get('shortSummary'))
                                if len(vacancies.json())!=0:
                                        shortSummary=vacancies.json().get('shortSummary')
                                        jd=vacancies.json().get('jd')

                                        tech_stack_matchingPercent=skillMatching.skillMatching(candidate_tech_stack,jd)
                                        candidate_reqMatching={"technologyStackMatchingPercent":tech_stack_matchingPercent}
                                        candidate_data.update(candidate_reqMatching)

                                        short_summary_matchingPercent=jdMatching.extractKeySkillsFromCv(txt,shortSummary)
                                        candidate_reqMatching_shortsummary={"shortSummaryMatchingPercent":short_summary_matchingPercent}
                                        candidate_data.update(candidate_reqMatching_shortsummary)

                                        candidate_combined_matchingPercent=skillMatching.combinedPercent(tech_stack_matchingPercent,short_summary_matchingPercent)
                                        candidate_reqMatching_combined={"reqMatchingPercent":candidate_combined_matchingPercent}
                                        candidate_data.update(candidate_reqMatching_combined)

                                        print(candidate_data)
                                        if experienceMatching.compareExperience(candidate_data.get('yearOfExperience'),vacancies.json().get('experienceRequired')):
                                                print("api calling")
                                                url2='https://cv-processing-api.herokuapp.com/v1/candidiate/{}'.format(vacancies.json().get('vacancyId'))
                                                y=requests.put(url2,json=candidate_data,headers=headers)
                                                print(y)

                        else:
                                vacancies=updatedVacancy.getVacancies()
                                if len(candidate_data.get('candidateName'))!=0:

                                                
                                        for i in range(len(vacancies.json())):
                                                shortSummary=vacancies.json()[i].get('shortSummary')
                                                jd=vacancies.json()[i].get('jd')

                                                tech_stack_matchingPercent=skillMatching.skillMatching(candidate_tech_stack,jd)
                                                candidate_reqMatching={"technologyStackMatchingPercent":tech_stack_matchingPercent}
                                                candidate_data.update(candidate_reqMatching)

                                                short_summary_matchingPercent=jdMatching.extractKeySkillsFromCv(txt,shortSummary)
                                                candidate_reqMatching_shortsummary={"shortSummaryMatchingPercent":short_summary_matchingPercent}
                                                candidate_data.update(candidate_reqMatching_shortsummary)

                                                candidate_combined_matchingPercent=skillMatching.combinedPercent(tech_stack_matchingPercent,short_summary_matchingPercent)
                                                candidate_reqMatching_combined={"reqMatchingPercent":candidate_combined_matchingPercent}
                                                candidate_data.update(candidate_reqMatching_combined)

                                                print(candidate_data)
                                                if experienceMatching.compareExperience(candidate_data.get('yearOfExperience'),vacancies.json()[i].get('experienceRequired')):
                                                        url2='https://cv-processing-api.herokuapp.com/v1/candidiate/{}'.format(vacancies.json()[i].get('vacancyId'))
                                                        y=requests.put(url2,json=candidate_data,headers=headers)




