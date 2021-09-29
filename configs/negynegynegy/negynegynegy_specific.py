#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*

import re

from html2tei import parse_date, decompose_listed_subtrees_and_mark_media_descendants, tei_defaultdict

PORTAL_URL_PREFIX = 'https://444.hu/'

ARTICLE_ROOT_PARAMS_SPEC = [(('section',), {'id': 'main-section'})]

HTML_BASICS = {'p', 'h3', 'h2', 'h4', 'h5', 'em', 'i', 'b', 'strong', 'mark', 'u', 'sub', 'sup', 'del', 'strike',
               'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'quote', 'figure', 'iframe'}


def get_meta_from_articles_spec(tei_logger, url, bs):
    data = tei_defaultdict()
    data['sch:url'] = url
    basic_article = True
    raw_meta = bs.find('div', id='headline')
    articles = bs.find_all('article')
    if raw_meta is not None and articles is not None:
        if len(articles) > 1 and all('class' in art.attrs.keys() and art.attrs['class'] == ['report']
                                     for art in articles):
            basic_article = False
        else:
            tei_logger.log('WARNING', f'{url}: UNKNOWN ARTICLE SCHEME (not basic but not report)!')
    else:
        tei_logger.log('WARNING', f'{url}: ARTICLE BODY NOT FOUND OR UNKNOWN ARTICLE SCHEME!')
        return None
    if basic_article in [True, False]:
        date_tag = bs.find('meta', property='article:published_time')
        # 2021-05-11T19:31:11+02:00"
        if date_tag is not None:
            parsed_date = parse_date(date_tag.attrs['content'][:19], '%Y-%m-%dT%H:%M:%S')
            data['sch:datePublished'] = parsed_date
        else:
            tei_logger.log('WARNING', f'{url}: DATE NOT FOUND IN URL!')
        modified_date_tag = bs.find('meta', property='article:modified_time').attrs['content']
        if modified_date_tag is not None:
            parsed_moddate = parse_date(modified_date_tag[:19], '%Y-%m-%dT%H:%M:%S')
            data['sch:dateModified'] = parsed_moddate

    if basic_article:
        title = raw_meta.find('h1')
        if title is not None:
            data['sch:name'] = title.text.strip()
        else:
            tei_logger.log('WARNING', f'{url}: TITLE TAG NOT FOUND!')
        authors_list = raw_meta.find(class_='byline__authors')
        if authors_list is not None:
            authors_list = [a.text.strip() for a in authors_list.find_all('a')]
            data['sch:author'] = authors_list
        else:
            tei_logger.log('WARNING', f'{url}: AUTHOR TAG NOT FOUND!')
        section = raw_meta.find(class_='byline__category')
        if section is not None:
            data['sch:articleSection'] = section.text.strip()
        else:
            tei_logger.log('WARNING', f'{url}: SECTION TAG NOT FOUND!')
        keywords_root = bs.find('meta', {'name': 'keywords'})
        if keywords_root is not None:
            keywords_list = keywords_root.attrs['content'].split(',')
            data['sch:keywords'] = keywords_list
        else:
            tei_logger.log('DEBUG', f'{url}: TAGS NOT FOUND!')
        return data
    elif not basic_article:
        # The scheme of broadcasts is different, metadata is handled differently
        authors_tag = bs.find_all(class_='report__author')
        if authors_tag is not None:
            authors_list = [au.text.strip() for au in authors_tag]
            data['sch:author'] = authors_list
        else:
            tei_logger.log('WARNING', f'{url}: AUTHOR TAG NOT FOUND!')
        section = bs.find('meta', {'itemprop': 'articleSection'})
        if section is not None and 'content' in section.attrs.keys():
            data['sch:articleSection'] = section.attrs['content'].strip()
            print(data['sch:articleSection'])
        else:
            tei_logger.log('WARNING', f'{url}: SECTION TAG NOT FOUND!')
        title = bs.find('h1', {'class': 'livestream__title'})
        if title is not None:
            data['sch:name'] = title.text.strip()
        else:
            tei_logger.log('WARNING', f'{url}: TITLE TAG NOT FOUND!')
        return data


def excluded_tags_spec(tag):
    if tag.name not in HTML_BASICS:
        tag.name = 'else'
    tag.attrs = {}
    return tag


BLOCK_RULES_SPEC = {}
BIGRAM_RULES_SPEC = {'szakasz': {('temp_table_id', 'det_by_child'): ('table_text', 'temp')}}

LINKS_SPEC = {'a': 'href', '0_MDESC_a': 'href', 'img': 'href', '0_MDESC_img': 'href'}
DECOMP = [(('div',), {'id': 'headline'}),
          (('div',), {'class': 'hide-print'}),
          (('div',), {'class': 'hide-for-print'}),  # class=row hide-for-print
          (('aside',), {'id': 'content-sidebar'}),
          (('div',), {'id': 'ep-banner'}),
          (('div',), {'class': 'widget-recommendation'}),
          (('script',), {}),
          (('noscript',), {}),
          (('iframe',), {}),
          (('center',), {}),
          (('style',), {}),  # css
          (('footer',), {}),
          # TODO: 'tovább'-os, kellhet https://444.hu/2014/09/15/orban-viktor-visszaadja-a-bankok-penzet-az-embereknek
          (('footer',), {'class': 'hide-print'}),
          (('footer',), {'class': 'hide-for-print'}),
          (('div',), {'class': 'jeti-roadblock'}),
          (('div',), {'class': 'tumblr-post'}),
          (('div',), {'class': 'd36-top'}),
          (('div',), {'id': 'epaperPromoBox'}),
          (('div',), {'id': 'actions'}),
          (('div',), {'id': 'content'}),
          (('span',), {'class': 'embed-444'}),  # hirdetés
          (('div',), {'class': 'fb-root'}),
          (('div',), {'id': 'fb-root'}),
          (('div',), {'class': 'flex-video'}),
          (('div',), {'class': 'storify'}),
          (('div',), {'id': 'szohir-444mozi'}),
          (('h2',), {'class': 'szohir-444mozi'}),
          (('h2',), {'class': 'szohir-jo2kampany'}),
          (('h2',), {'class': 'szohir-tldr'}),
          (('h2',), {'class': 'ad-insighthungary'}),
          (('h2',), {'class': 'ad-johirlevel'}),
          (('ul',), {'class': 'pagination'}),
          (('div',), {'class': 'pagination'})]

MEDIA_LIST = [(('div',), {'id': 'bodyContent'}),  # 1 db wikipedia cikk
              (('div',), {'id': 'mw-content-text'}),
              (('figure',), {}),
              (('iframe',), {}),
              (('object',), {}),  # ????
              (('video',), {}),  # ????
              (('div',), {'class': 'embedly-card'}),  # ????
              (('div',), {'class': 'fb-video'}),
              (('div',), {'class': 'fb-post'}),
              (('blockquote',), {'class': 'twitter-tweet'}),
              (('blockquote',), {'class': 'instagram-media'}),
              (('blockquote',), {'class': 'twitter-video'}),
              (('svg',), {'id': 'Layer_1'}),
              (('svg',), {'class': 'meszaros-orban'}),
              (('defs',), {}),
              (('div',), {'class': 'whitebox'})]


def decompose_spec(article_dec):
    # from 2020: <a class="pr-box pr-box--compact pr-box--centered" href="https://membership.444.hu">
    for h2 in article_dec.find_all('h2'):
        for a in h2.find_all('a', {'href': 'direkt36_spec'}):
            print(h2)
            a.decompose()
    decompose_listed_subtrees_and_mark_media_descendants(article_dec, DECOMP, MEDIA_LIST)

    return article_dec


BLACKLIST_SPEC = []

LINK_FILTER_SUBSTRINGS_SPEC = re.compile('|'.join(['LINK_FILTER_DUMMY_STRING']))

MULTIPAGE_URL_END = re.compile(r'^\b$')  # Dummy


def next_page_of_article_spec(_):
    return None
