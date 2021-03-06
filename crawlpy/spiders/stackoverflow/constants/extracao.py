# -*- coding: utf-8 -*-
import re

from scrapy.loader.processors import Join, TakeFirst
from crawlpy.processors import TakeLast


_base_xpath_job = ('//div[contains(@class, "job-details--about")]/'
                   '/div[@class="mb8"]//span[preceding-sibling::span['
                   'contains(., "{}")]]/text()').format

COMMON_SKILLS = ['docker', 'ansible', 'linux', 'python', 'django', 'c#',
                'java', 'flask', 'c++', '.net', 'javascript', 'elixir',
                'html', 'html5', 'css', 'css3', 'redux', 'react', 'angular',
                'less', 'swift', 'objective-c', 'jquery', 'php', 'wordpress']

def _clean_skills(skills):
    pattern = re.compile(
        r'(iphone|http|https|http:\/\/.*|https:\/\/.*|www|\.com|\.com\..*|@)')
    new_list = []
    for element in skills:
        if not re.findall(pattern, element):
            for skill in COMMON_SKILLS:
                if skill in element:
                    element = skill
            new_list.append(element)
    return list(set(new_list))


XPATHS_JOB = {

    # Jobs infos
    'title': '//h1[contains(@class, "headline1")]//a/text()',
    '_type': _base_xpath_job('Job type'),
    'experience_level': _base_xpath_job('Experience level'),
    'role': _base_xpath_job('Role'),
    'industry': _base_xpath_job('Industry'),
    'company_size': _base_xpath_job('Company size'),
    'company_type': _base_xpath_job('Company type'),
    'tecnologies': ('//section[contains(., "Technologies")]//div//a/text()',
                    _clean_skills),

    'description': (
        '//section[contains(., "Job description")]//p//text() | '
        '//section[contains(., "Job description")]//p//text()', Join()),
    'joel_test': ('//section[contains(., "Joel Test")]'
                  '//div[@class="mb4" and //span[conta'
                  'ins(@class, "green")]]//span/following::text()[1]'),
    'link_apply': ('//a[contains(@class, "_apply")]/@href', TakeFirst()),
    'benefits': '//section[contains(@class, "benefits")]//ul//li/@title',

    # Company infos
    'company': ('//h1[contains(@class, "headline1")]/'
                'following-sibling::div[1]//a//text()'),
    'location': ('//h1[contains(@class, "headline1")]/'
                 'following::span[contains(@class, "fc-black-500")]'
                 '//span/following::text()[1]', TakeFirst()),
    'salary': '//header//span[contains(@class, "-salary")]/text()',
    'sponsor': ('//span[contains(@class, "-visa")]/text()', TakeFirst()),
    'paid': ('//span[contains(@class, "-relocation")]/text()', TakeFirst())
}
