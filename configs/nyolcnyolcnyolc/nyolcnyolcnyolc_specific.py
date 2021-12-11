#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*

import re

from html2tei import parse_date, BASIC_LINK_ATTRS, decompose_listed_subtrees_and_mark_media_descendants, tei_defaultdict

PORTAL_URL_PREFIX = 'https://888.hu'

ARTICLE_ROOT_PARAMS_SPEC = [(('div',), {'class': 'maincontent8'}),
                            (('div',), {'class': 'm-wideContent__cnt'})]


HTML_BASICS = {'p', 'h3', 'h2', 'h4', 'h5', 'em', 'i', 'b', 'strong', 'mark', 'u', 'sub', 'sup', 'del', 'strike',
               'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'quote', 'figure', 'iframe'}


def get_meta_from_articles_spec(tei_logger, url, bs):
    data = tei_defaultdict()
    data['sch:url'] = url
    article_root = bs.find('div', id='cikkholder')
    if article_root is not None:
        date_tag = article_root.find('p').get_text().replace(' ','')
        if date_tag is not None:
            parsed_date = parse_date(date_tag, '%Y.%m.%d.%H:%M')
            data['sch:datePublished'] = parsed_date
        else:
            tei_logger.log('WARNING', f'{url}: DATE FORMAT ERROR!')
        title = article_root.find('h1')
        if title is not None:
            data['sch:name'] = title.text.strip()
        else:
            tei_logger.log('WARNING', f'{url}: TITLE NOT FOUND IN URL!')
        author = article_root.find('div', class_='text-wrap')
        if author is not None:
            source = [i for i in author.text.strip().split(', ') if i in ['888.hu', 'MTI']]
            data['sch:source'] = source
            authors = [i for i in author.text.strip().split(', ') if i not in ['888.hu', 'MTI']]
            data['sch:author'] = authors
        else:
            tei_logger.log('WARNING', f'{url}: AUTHOR TAG NOT FOUND!')
        section_tag = bs.find('a', class_='btn-link')
        if section_tag is not None:
            data['sch:articleSection'] = section_tag.text.strip()
        else:
            tei_logger.log('WARNING', f'{url}: SECTION TAG NOT FOUND!')
        keywords_root = bs.find('div', class_='plugin-holder').find('div', class_='text').text.strip().split(', ')
        if keywords_root is not None:
            data['sch:keywords'] = keywords_root
        else:
            tei_logger.log('DEBUG', f'{url}: TAGS NOT FOUND!')
        return data
    else:
        tei_logger.log('WARNING', f'{url}: METADATA CONTAINER NOT FOUND!')
        return None


def excluded_tags_spec(tag):
    return tag


BLOCK_RULES_SPEC = {}
BIGRAM_RULES_SPEC = {}
LINKS_SPEC = BASIC_LINK_ATTRS

DECOMP = [(('div',), {'class': 'AdW'}),
          ]
MEDIA_LIST = []


def decompose_spec(article_dec):
    decompose_listed_subtrees_and_mark_media_descendants(article_dec, DECOMP, MEDIA_LIST)
    return article_dec


BLACKLIST_SPEC = []

LINK_FILTER_SUBSTRINGS_SPEC = re.compile('|'.join(['LINK_FILTER_DUMMY_STRING']))

MULTIPAGE_URL_END = re.compile(r'^\b$')  # Dummy


def next_page_of_article_spec(_):
    return None
