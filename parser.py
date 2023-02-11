from bs4 import BeautifulSoup

from utils import title_selector, salary_selcetor, job_experience_selector, time_type_selector, \
    skill_requirement_selector, gender_selector, army_situation_selector, minimum_degree_selector


class AdvertisementsParser:
    def __init__(self):
        self.soup = None


    @property
    def title(self):
        title = self.soup.select_one(title_selector)
        if title:
            return title.text
        return None

    @property
    def salary(self):
        salary = self.soup.select_one(salary_selcetor)
        if salary:
            return salary.text
        return None

    @property
    def job_experience(self):
        job_experience = self.soup.select_one(job_experience_selector)
        if job_experience:
            return job_experience.text
        return None

    @property
    def work_time(self):
        work_time = self.soup.select_one(time_type_selector)
        if work_time:
            return work_time.text
        return None

    @property
    def skill_requirement(self):
        skill_requirement = self.soup.select_one(skill_requirement_selector)
        if skill_requirement:
            return skill_requirement.text
        return None

    @property
    def minimum_degree(self):
        minimum_degree = self.soup.select_one(minimum_degree_selector)
        if minimum_degree:
            return minimum_degree.text
        return None

    @property
    def gender(self):
        gender = self.soup.select_one(gender_selector)
        if gender:
            return gender.text
        return None

    @property
    def army_situation(self):
        army_situation = self.soup.select_one(army_situation_selector)
        if army_situation:
            return army_situation.text
        return None

    def parse(self, response):
        self.soup = BeautifulSoup(response.text, 'html.parser')
        parsed_data = dict(
            title=self.title, salary=self.salary, job_experience=self.job_experience,
            work_time=self.work_time, skill_requirement=self.skill_requirement,
            gender=self.gender, minimum_degree=self.minimum_degree,
            army_situation=self.army_situation,
        )
        return parsed_data



