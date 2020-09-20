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
