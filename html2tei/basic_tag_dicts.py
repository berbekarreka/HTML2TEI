#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# article_body_converter.py + tei_utils.py
INLINE_TAGS = {'felkover', 'dolt', 'kiemelt', 'hivatkozas', 'alahuzott', 'athuzott', 'felsoindex', 'alsoindex',
               'inline_idezet', 'hi', 'ref'}
# article_body_converter.py
HI_TAGS = INLINE_TAGS.difference({'media_hivatkozas', 'hivatkozas'})

# article_body_converter.py
PARAGRAPH_LIKE_TAGS = {'bekezdes', 'cimsor', 'forras', 'kozvetites_meta', 'kozvetites_content', 'kozvetites_ido', 'kerdes'}

# article_body_converter.py
BLOCKS = {'doboz', 'vez_bekezdes', 'lista', 'idezet', 'table_text', 'kozvetites', 'galeria', 'kviz', 'forum'}
# article_body_converter.py
TEMPORARILY_USED_TAGS = {'media_hivatkozas', 'hivatkozas'}
# article_body_converter.py
USED_NOTEXT_TAGS = {'galeria', 'media_tartalom', 'beagyazott_tartalom', 'abra', 'social_media'}

# article_body_converter.py
OUR_BUILTIN_TAGS = {'to_decompose', 'to_unwrap', 'bekezdes', 'doboz', 'vez_bekezdes', 'cimsor',
                    'lista', 'listaelem', 'idezet', 'forras',
                    'felkover', 'dolt', 'kiemelt', 'alahuzott', 'athuzott', 'felsoindex', 'alsoindex',
                    'table_text',
                    'social_media',
                    'inline_idezet',
                    'hivatkozas',
                    'oszlop_valid', 'sor_valid', 'oszlop_sor', 'tablazat_cimsor', 'kozvetites',
                    'kozvetites_meta', 'kozvetites_ido', 'kozvetites_szerzo', 'kozvetites_content', 'cimsor', 'galeria',
                    'kviz', 'kerdes', 'valaszblokk', 'valasz', 'forum', 'media_tartalom', 'beagyazott_tartalom',
                    'abra', 'hi', 'ref'}

# configs/*
BASIC_LINK_ATTRS = {'a', '0_MDESC_a', 'img', '0_MDESC_img', 'iframe', '0_MDESC_iframe'}

# read_config.py
BLOCK_RULES = {'idezet': {'rename': {'cimsor': 'felkover'},
                          'default': 'bekezdes',
                          'not_valid_inner_blocks': [],
                          'not_valid_as_outer_for': ['idezet', 'doboz', 'kozvetites', 'galeria', 'kviz', 'forum']},
               'doboz': {'rename': {
                   'oszlop': 'to_unwrap',
                   'sor': 'bekezdes',
                   'oszlop_sor': 'bekezdes'},
                   'default': 'bekezdes',
                   'not_valid_inner_blocks': [],
                   'not_valid_as_outer_for': ['kozvetites', 'vez_bekezdes']},
               'lista': {'rename': {},
                         'default': 'listaelem',
                         'not_valid_inner_blocks': ['doboz'],
                         'not_valid_as_outer_for': ['kozvetites', 'vez_bekezdes'],
                         },
               'vez_bekezdes': {'rename': {'cimsor': 'felkover'},
                                'default': 'bekezdes',
                                'not_valid_inner_blocks': ['doboz'],
                                'not_valid_as_outer_for': []},
               'table_text': {'rename': {'oszlop': 'oszlop_valid', 'sor': 'sor_valid'},
                              'default': 'oszlop_sor',
                              'not_valid_inner_blocks': ['doboz'],
                              'not_valid_as_outer_for': []},
               'kozvetites': {'rename': {'bekezdes': 'unwrap'},
                              'default': 'kozvetites_content',
                              'not_valid_inner_blocks': ['doboz'],
                              'not_valid_as_outer_for': []},
               'galeria': {'rename': {},
                           'default': 'bekezdes',
                           'not_valid_inner_blocks': [],
                           'not_valid_as_outer_for': ['doboz', 'table_text', 'lista', 'kozvetites', 'vez_bekezdes'],
                           },
               'kviz': {'rename': {},
                        'default': 'bekezdes',
                        'not_valid_inner_blocks': ['doboz', 'table_text', 'kozvetites', 'vez_bekezdes'],
                        'not_valid_as_outer_for': ['kozvetites', 'vez_bekezdes']},
               'forum': {'rename': {},
                         'default': 'bekezdes',
                         'not_valid_inner_blocks': [],
                         'not_valid_as_outer_for': ['kozvetites', 'vez_bekezdes']}
               }

# article_body_converter.py + tei_utils.py
MEDIA_DICT = {'media_tartalom': ('media_hivatkozas', 'forras', 'bekezdes', 'hivatkozas'),
              'social_media': ('social_header', 'bekezdes', 'hivatkozas'),
              'abra': ('media_hivatkozas',),
              'beagyazott_tartalom': ('bekezdes', 'hivatkozas', 'media_hivatkozas', 'media_tartalom')
              }

# tei_utils.py
XML_CONVERT_DICT = {'bekezdes': 'p',
                    'idezet': 'quote',
                    'inline_idezet': 'quote',
                    'lista': 'list',
                    'listaelem': 'item',
                    'szakasz': 'to_unwrap',
                    'jegyzet': 'note',
                    'sor_valid': 'row',
                    'table_text': 'table',
                    'tablazat_cimsor': 'head',
                    'kiemelt': 'hi',
                    'valasz': 'item',
                    }
# tei_utils.py
TAGNAME_AND_ATTR_TABLE = {'cimsor': ('p', 'head'),
                          'felkover': ('hi', 'bold'),
                          'dolt': ('hi', 'italic'),
                          'alahuzott': ('hi', 'underline'),
                          'athuzott': ('hi', 'strikeout'),
                          'felsoindex': ('hi', 'superscript'),
                          'alsoindex': ('hi', 'subscript'),
                          'forras': ('p', 'ref'),
                          'kozvetites_meta': ('p', 'meta'),
                          'kozvetites_ido': ('p', 'time'),
                          'kozvetites_szerzo': ('p', 'author'),
                          'kozvetites_content': ('p', 'content'),
                          'kerdes': ('p', 'question')}

# article_body_converter.py + tei_utils.py
FIGURE_REND_ATTRS = {'media_tartalom': 'media_content',
                     'abra': 'diagram',  # illustration
                     'beagyazott_tartalom': 'embedded_content'}
