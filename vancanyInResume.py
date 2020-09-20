import updatedVacancy
import Read_from_pdf
import skillMatching
import jdMatching
import experienceMatching
import requests
pdfName="52_xyz"
pdfNamevancancy=pdfName.split('_')


pdf_file='/home/sahdev/ProjectCV/python /python/CV/ajitrods.pdf'
Lines=Read_from_pdf.read_text_by_lines(pdf_file)
text_file=open('demo.txt')
txt=text_file.read()

headers={'Content-type':'application/json', 'Accept':'application/json'}
candidate_data={
"candidateName":"mona",
"email":"mona123@gmail.com",
"contactNo":"9868956985",
"technologyStack":"Java,SpringBoot,Hibernate",
"reqMatchingPercent":0,
"shortSummaryMatchingPercent":0,
"technologyStackMatchingPercent":0,
"yearOfExperience":5
}
candidate_tech_stack="Java,SpringBoot,Hibernate"

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
                url2='https://cv-processing-api.herokuapp.com/v1/candidiate/{}'.format(vacancies.json().get('vacancyId'))
                y=requests.put(url2,json=candidate_data,headers=headers)

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