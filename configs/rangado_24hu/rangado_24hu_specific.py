#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*

import re

from html2tei import parse_date, BASIC_LINK_ATTRS, decompose_listed_subtrees_and_mark_media_descendants, tei_defaultdict

PORTAL_URL_PREFIX = 'https://rangado.24.hu/'

ARTICLE_ROOT_PARAMS_SPEC = [(('div',), {'class': 'wpb_wrapper'}),
                            (('div',), {'class': 'm-wideContent__cnt'})]


HTML_BASICS = {'p', 'h3', 'h2', 'h4', 'h5', 'em', 'i', 'b', 'strong', 'mark', 'u', 'sub', 'sup', 'del', 'strike',
               'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'quote', 'figure', 'iframe'}


def get_meta_from_articles_spec(tei_logger, url, bs):
    data = tei_defaultdict()
    data['sch:url'] = url
    date_tag = bs.find('meta', property='article:published_time')
    if date_tag is not None:
        parsed_date = parse_date(date_tag.attrs['content'][:19], '%Y-%m-%dT%H:%M:%S')
        data['sch:datePublished'] = parsed_date
    elif bs.find('span', class_='a-date') is not None:
        parsed_date = parse_date(bs.find('span', class_='a-date').get_text().strip(), '%Y. %m. %d. %H:%M')
        data['sch:datePublished'] = parsed_date
    else:
        print('WARNING', f'{url}: DATE NOT FOUND IN URL!')
    modified_date_tag = bs.find('meta', property='article:modified_time')
    if modified_date_tag is not None:
        parsed_moddate = parse_date(modified_date_tag.attrs['content'][:19], '%Y-%m-%dT%H:%M:%S')
        data['sch:dateModified'] = parsed_moddate
    else:
        tei_logger.log('WARNING', f'{url}: MODIFIED DATE NOT FOUND IN URL!')
    title = bs.find('h1', class_='o-post__title')
    if title is not None:
        data['sch:name'] = title.text.strip()
    else:
        tei_logger.log('WARNING', f'{url}: TITLE TAG NOT FOUND!')
    article_root = bs.find('div', id='content')
    if article_root is not None:
        author = article_root.find_all('a', class_='m-author__name')
        if len(author) > 0:
            source = [i.get_text() for i in author if i.get_text() in ['Rangadó']]
            data['sch:source'] = source
            authors = [i.get_text() for i in author if i.get_text() not in ['Rangadó']]
            data['sch:author'] = authors
        else:
            tei_logger.log('WARNING', f'{url}: AUTHOR TAG NOT FOUND!')
        section = article_root.find('a', id='post-cat-title')
        if section is not None:
            data['sch:articleSection'] = section.text.strip()
        elif article_root.find('a', class_='o-articleHead__catWrap m-cat -catLive flex0') is not None:
            data['sch:articleSection'] = article_root.find(
                'a', class_='o-articleHead__catWrap m-cat -catLive flex0').text.strip()
        else:
            tei_logger.log('WARNING', f'{url}: SECTION TAG NOT FOUND!')
    else:
        tei_logger.log('WARNING', f'{url}: METADATA CONTAINER NOT FOUND!')
    keywords_root = bs.find('meta', attrs={'name': 'keywords'})
    if keywords_root is not None:
        keywords_list = keywords_root.attrs['content'].split(',')
        data['sch:keywords'] = keywords_list
    else:
        tei_logger.log('WARNING', f'{url}: TAGS NOT FOUND!')
    return data


def excluded_tags_spec(tag):
    return tag


BLOCK_RULES_SPEC = {}
BIGRAM_RULES_SPEC = {}
LINKS_SPEC = BASIC_LINK_ATTRS

DECOMP = [(('div',), {'id': 'content-toggle-placeholder'}),
          (('div',), {'class': 'banner_container'}),
          (('div',), {'class': 'm-articRecommend'}),
          (('div',), {'class': 'm-fbComment__txtAndIframeWrap'}),
          (('div',), {'class': 'twitter-tweet'}),
          (('div',), {'class': 'article_box_border'}),
          (('div',), {'class': 'o-post__head'}),
          (('div',), {'class': 'a-hirstartRecommender'}),
          (('div',), {'class': 'related-posts-box-old'}),
          (('div',), {'id': 'content-toggle-placeholder'}),
          (('div',), {'class': 'banner-container'})
          ]


MEDIA_LIST = []


def decompose_spec(article_dec):
    decompose_listed_subtrees_and_mark_media_descendants(article_dec, DECOMP, MEDIA_LIST)
    return article_dec


BLACKLIST_SPEC = ['https://rangado.24.hu/informacio/2011/05/14/szerzoi-jogok/',
                  'https://rangado.24.hu/teremfoci/2014/04/23/futsal-2/',
                  'https://rangado.24.hu/hirek/2013/11/06/facebook-2/']

LINK_FILTER_SUBSTRINGS_SPEC = re.compile('|'.join(['LINK_FILTER_DUMMY_STRING']))

MULTIPAGE_URL_END = re.compile(r'^\b$')  # Dummy


def next_page_of_article_spec(_):
    return None
