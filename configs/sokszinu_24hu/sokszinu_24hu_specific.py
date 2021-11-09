#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*

import re

from html2tei import parse_date, BASIC_LINK_ATTRS, decompose_listed_subtrees_and_mark_media_descendants, tei_defaultdict

PORTAL_URL_PREFIX = 'https://sokszinuvidek.24.hu/'

ARTICLE_ROOT_PARAMS_SPEC = [(('div',), {'class': 'o-post__lead lead post-lead cf _ce_measure_widget'}),
                            (('div',), {'class': 'o-post__body o-postCnt post-body'}),
                            (('div',), {'class': 'o-post__body o-postCnt -widthFull post-body'})]

HTML_BASICS = {'p', 'h3', 'h2', 'h4', 'h5', 'em', 'i', 'b', 'strong', 'mark', 'u', 'sub', 'sup', 'del', 'strike',
               'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'quote', 'figure', 'iframe'}

def get_meta_from_articles_spec(tei_logger, url, bs):
    data = tei_defaultdict()
    data['sch:url'] = url
    date_tag = bs.find('meta', property='article:published_time')
    if date_tag is not None:
        parsed_date = parse_date(date_tag.attrs['content'][:19], '%Y-%m-%dT%H:%M:%S')
        data['sch:datePublished'] = parsed_date
    else:
        tei_logger.log('WARNING', f'{url}: DATE NOT FOUND IN URL!')
    modified_date_tag = bs.find('meta', property='article:modified_time')
    if modified_date_tag is not None:
        parsed_moddate = parse_date(modified_date_tag.attrs['content'][:19], '%Y-%m-%dT%H:%M:%S')
        data['sch:dateModified'] = parsed_moddate
    else:
        tei_logger.log('WARNING', f'{url}: MODIFIED DATE NOT FOUND IN URL!')
    title = bs.find('h1')
    if title is not None:
        data['sch:name'] = title.text.strip()
    else:
        tei_logger.log('WARNING', f'{url}: TITLE TAG NOT FOUND!')
    article_root = bs.find('div', id='content')
    if article_root is not None:
        author = article_root.find_all('a', class_='m-author__name')
        if author is not None:
            source = [i.get_text() for i in author if i in ['Sokszínű Vidék', 'Szponzorált tartalom']]
            data['sch:source'] = source
            authors = [i.get_text() for i in author if i not in ['Sokszínű Vidék', 'Szponzorált tartalom']]
            data['sch:author'] = authors
        else:
            tei_logger.log('WARNING', f'{url}: AUTHOR TAG NOT FOUND!')
        section = article_root.find('a', id='post-cat-title')
        if section is not None:
            data['sch:articleSection'] = section.text.strip()
        #else:
        #    tei_logger.log('WARNING', f'{url}: SECTION TAG NOT FOUND!')
    else:
        tei_logger.log('WARNING', f'{url}: METADATA CONTAINER NOT FOUND!')
    keywords_root = bs.find_all('meta', property='article:tag')
    if keywords_root is not None:
        keywords_list = [i.attrs['content'] for i in keywords_root]
        data['sch:keywords'] = keywords_list
    else:
        tei_logger.log('WARNING', f'{url}: TAGS NOT FOUND!')
    return data


def excluded_tags_spec(tag):
    return tag


BLOCK_RULES_SPEC = {}
BIGRAM_RULES_SPEC = {}
LINKS_SPEC = BASIC_LINK_ATTRS

DECOMP = [(('div',), {'class':
                          'o-post__articRecommend m-articRecommend -hasImg cf '
                          'article-recommendation-container cf _ce_measure_widget'})]
MEDIA_LIST = []


def decompose_spec(article_dec):
    decompose_listed_subtrees_and_mark_media_descendants(article_dec, DECOMP, MEDIA_LIST)
    return article_dec


BLACKLIST_SPEC = []

MULTIPAGE_URL_END = re.compile(r'^\b$')  # Dummy


def next_page_of_article_spec(_):
    return None
