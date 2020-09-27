#!/usr/bin/python3

import requests
from html.parser import HTMLParser
import re
import json
import datetime
import socket
import unidecode
import yaml
import jinja2

import os.path
import hashlib

def j2_hash_filter(value):

    #print(value)
    value = value.strip()
    computed_hash = hashlib.md5(value.encode()).hexdigest()

    return computed_hash[0:2]


#define book_map

bibletrans = {
    '1Móz': 'Genesis',
    '2Móz': 'Exodus',
    '3Móz': 'Leviticus',
    '4Móz': 'Numbers',
    '5Móz': 'Deuteronomy',
    'Józs': 'Joshua',
    'Bír':  'Judges',
    'Ruth': 'Ruth',
    '1Sám': '1 Samuel',
    '2Sám': '2 Samuel',
    '1Kir': '1 Kings',
    '2Kir': '2 Kings',
    '1Krón': '1 Chronicles',
    '2Krón': '2 Chronicles',
    'Ezsd': 'Ezra',
    'Neh':  'Nehemiah',
    'Eszt': 'Esther',
    'Jób':  'Job',
    'Zsolt': 'Psalms',
    'Péld': 'Proverbs',
    'Préd': 'Ecclesiastes',
    'Énekek': 'Song of Solomon',
    'Ézs':  'Isaiah',
    'Jer':  'Jeremiah',
    'Jsir': 'Lamentations',
    'Ez':   'Ezekiel',
    'Dán':  'Daniel',
    'Hós':  'Hosea',
    'Jóel': 'Joel',
    'Ám':   'Amos',
    'Abd':  'Obadiah',
    'Jón':  'Jonah',
    'Mik':  'Micah',
    'Náh':  'Nahum',
    'Hab':  'Habakkuk',
    'Zof':  'Zephaniah',
    'Hag':  'Haggai',
    'Zak':  'Zechariah',
    'Mal':  'Malachi',
    'Mt':  'Matthew',
    'Mk':  'Mark',
    'Lk':  'Luke',
    'Jn':  'John',
    'ApCsel': 'Acts',
    'Róm': 'Romans',
    '1Kor': '1 Corinthians',
    '2Kor': '2 Corinthians',
    'Gal': 'Galatians',
    'Ef':  'Ephesians',
    'Fil': 'Philippians',
    'Kol': 'Colossians',
    '1Thessz': '1 Thessalonians',
    '2Thessz': '2 Thessalonians',
    '1Tim': '1 Timothy',
    '2Tim': '2 Timothy',
    'Tit': 'Titus',
    'Filem': 'Philemon',
    'Zsid': 'Hebrews',
    'Jak': 'James',
    '1Pt': '1 Peter',
    '2Pt': '2 Peter',
    '1Jn': '1 John',
    '2Jn': '2 John',
    '3Jn': '3 John',
    'Jud': 'Jude',
    'Jel': 'Revelation'
}

bibletrans_short_karoli = {
    '1Móz': 'Gen',
    '2Móz': 'Exod',
    '3Móz': 'Lev',

    '4Móz': 'Num',
    '5Móz': 'Deut',
    'Józs': 'Josh',
    'Bir':  'Judg',
    'Bír':  'Judg',
    'Ruth': 'Ruth',
    '1Sám': '1Sam',
    '2Sám': '2Sam',
    '1Kir': '1Kgs',
    '2Kir': '2Kgs',
    '1Krón': '1Chr',
    '2Krón': '2Chr',
    'Ezsd': 'Ezra',
    'Ezsdr': 'Ezra',
    'Neh':  'Neh',
    'Nehem':  'Neh',
    'Eszt': 'Esth',
    'Jób':  'Job',
    'Zsolt': 'Ps',
    'Zsolt,': 'Ps',
    'Péld': 'Prov',
    'Préd': 'Eccl',
    'Énekek': 'Song',
    'Ének.Én': 'Song',
    'Én': 'Song',
    'Ésa':  'Isa',
    'Ézs':  'Isa',
    'Jer':  'Jer',
    'Jsir': 'Lam',
    'Siral': 'Lam',
    'Sir': 'Lam',
    'Ez':   'Ezek',
    'Ezék':   'Ezek',

    'Dán':  'Dan',
    'Hós':  'Hos',
    'Jóel': 'Joel',
    'Ám':   'Amos',
    'Ámós':   'Amos',
    'Abd':  'Obad',
    'Jón':  'Jonah',
    'Mik':  'Mic',
    'Náh':  'Nah',
    'Hab':  'Hab',
    'Zof':  'Zeph',
    'Sof':  'Zeph',
    'Hag':  'Hag',
    'Agge':  'Hag',
    'Agg':  'Hag',
    'Zak':  'Zech',
    'Mal':  'Mal',
    'Malak':  'Mal',


    'Máté':  'Matt',
    'Mát':  'Matt',
    'Mt':  'Matt',
    'Márk':  'Mark',
    'Mk':  'Mark',
    'Lk':  'Luke',

    'Luk':  'Luke',
    'Ján':  'John',
    'Jn':  'John',

    'ApCsel': 'Acts',
    'Csel': 'Acts',
    'Róm': 'Rom',
    '1Kor': '1Cor',
    '2Kor': '2Cor',
    'Gal': 'Gal',
    'Ef':  'Eph',
    'Eféz':  'Eph',
    'Fil': 'Phil',
    'Filem': 'Phlm',
    'Kol': 'Col',
    '1Thessz': '1Thess',
    '1Thess': '1Thess',
    '2Thessz': '2Thess',
    '2Thess': '2Thess',
    '1Tim': '1Tim',
    '2Tim': '2Tim',
    'Tit': 'Titus',
    'Zsid': 'Heb',
    'Jak': 'Jas',
    '1Pét': '1Pet',
    '1Pt': '1Pet',
    '2Pt': '2Pet',

    '2Pét': '2Pet',
    '1Ján': '1John',
    '2Ján': '2John',
    '3Ján': '3John',
    '1Jn': '1John',
    '2Jn': '2John',
    '3Jn': '3John',

    'Jud': 'Jude',
    'Júd': 'Jude',
    'Jel': 'Rev'
}


books_web = {
    '1Móz' :'GEN',
    '2Móz' :'EXO',
    '3Móz' :'LEV',
    '4Móz' :'NUM',
    '5Móz' :'DEU',
    'Józs' :'JOS',
    'Bir' :'JDG',
    'Ruth' :'RUT',
    '1Sám' :'1SA',
    '2Sám' :'2SA',
    '1Kir' :'1KI',
    '2Kir' :'2KI',
    '1Krón' :'1CH',
    '2Krón' :'2CH',
    'Ezsdr' :'EZR',
    'Neh' :'NEH',
    'Eszt' :'EST',
    'Jób' :'JOB',
    'Zsolt' :'PSA',
    'Péld' :'PRO',
    'Préd' :'ECC',
    'Ének.Én' :'SNG',
    'Ésa' :'ISA',
    'Jer' :'JER',
    'Sir' :'LAM',
    'Ezék' :'EZK',
    'Dán' :'DAN',
    'Hós' :'HOS',
    'Jóel' :'JOL',
    'Ámós' :'AMO',
    'Abd' :'OBA',
    'Jón' :'JON',
    'Mik' :'MIC',
    'Náh' :'NAM',
    'Hab' :'HAB',
    'Sof' :'ZEP',
    'Agg' :'HAG',
    'Zak' :'ZEC',
    'Malak' :'MAL',
    'Mát' :'MAT',
    'Márk' :'MRK',
    'Luk' :'LUK',
    'Ján' :'JHN',
    'Csel' :'ACT',
    'Róm' :'ROM',
    '1Kor' :'1CO',
    '2Kor' :'2CO',
    'Gal' :'GAL',
    'Eféz' :'EPH',
    'Fil' :'PHP',
    'Kol' :'COL',
    '1Thess' :'1TH',
    '2Thess' :'2TH',
    '1Tim' :'1TI',
    '2Tim' :'2TI',
    'Tit' :'TIT',
    'Filem' :'PHM',
    'Zsid' :'HEB',
    'Jak' :'JAS',
    '1Pét' :'1PE',
    '2Pét' :'2PE',
    '1Ján' :'1JN',
    '2Ján' :'2JN',
    '3Ján' :'3JN',
    'Júd' :'JUD',
    'Jel' :'REV'
}



class ABMHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = {}

    def handle_starttag(self, tag, attrs):
        if(tag == 'h3'):
            #section_found
            self.section_found = 1
            self.section = {}
    #    print("Encountered a start tag:", tag)
        if(tag == 'p' and self.section_found == 2):
            #first verse found
            self.section_found = 0
            self.section['verse'] = int(attrs[1][1].replace('v',''))
            self.sections[self.section['verse']] = self.section
            #print(json.dumps(self.section))

    def handle_endtag(self, tag):
        if(tag == 'h3' and self.section_found == 1):
            self.section_found = 2


    #    print("Encountered an end tag :", tag)
    json_text = ""
    def handle_data(self, data):
        try:
            if self.section_found == 1:
                #print(data)
                mydata = re.sub(r'\d\. fejezet\n', '', data)
                self.section['title'] = mydata
        except:
            pass
        #if(re.search(r'window.__DW_SVELTE_PROPS__', data) and re.search(r'chartData', data)):
        #    lines = data.split('\n')
        #    self.json_text = re.sub(r'^window.__DW_SVELTE_PROPS__ = JSON.parse\("', '', lines[0])
        #    self.json_text = re.sub(r'"\);$', '', self.json_text)
        #    self.json_text = re.sub(r'\\"', '"', self.json_text)
        #    self.json_text = re.sub(r'\\\\n', '\n', self.json_text)
        #    self.json_text = re.sub(r'\\\\"', '\\"', self.json_text)
        #    self.json_text = re.sub(r'\n', '', self.json_text)
        #    self.json_text = re.sub(r'\r', '', self.json_text)

class SZIHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.verse_coming = 0
        self.cite_coming = 0
        self.chapter_raw = []
        self.verse = {}

    def handle_starttag(self, tag, attrs):
        #print('>' + tag + ': ' + json.dumps(attrs))
        if(tag == 'span' and attrs[0][1] == 'text-muted numv'):
            #print('verse_coming')
            self.verse_coming = 1
        if(tag == 'sup' and self.verse_coming == 3):
            self.cite_coming = 1
        if(tag == 'a' and self.cite_coming == 1):
            self.cite_coming = 2
        if(tag == 'br' and self.verse_coming == 3):
            self.verse_coming = 4
        if(tag == 'hr' and self.verse_coming > 0):
            self.verse_coming = 0


    def handle_endtag(self, tag):
        #end of document append last verse
        if tag == 'html':
            if 'num' in self.verse:
                self.chapter_raw.append(self.verse)
            self.verse = {}

        #print('<' + tag)
        #if(tag == 'h3' and self.section_found == 1):

    def handle_data(self, data):
        if self.verse_coming == 1:
            #print('num: ' + data)
            if 'num' in self.verse:
                self.chapter_raw.append(self.verse)
            self.verse = {}
            self.verse['num'] = int(data)

            self.verse_coming = 2
        elif self.verse_coming == 2:
            #print('text: ' + data.strip())
            self.verse['text'] = data.strip()
            self.verse_coming = 3
        if self.verse_coming == 4:
            self.verse['text'] += ' ' + data.strip()
            self.verse_coming = 3
        elif self.cite_coming == 2:
            #print('cite: ' + data)
            self.verse['cite'] = data
            self.cite_coming = 0
        else:
            #print('raw:' + data)
            pass
            #print("Encountered some data  :", json_text)

#get book list
r = requests.get('https://szentiras.hu/api/books/KG')
books = json.loads(r.text)

src_dir = '/home/kris/Nextcloud/projects/hunuj/HunKar/szentiras.hu/KG'
section_src_dir = '/home/kris/Nextcloud/projects/hunuj/abibliamindenkie.hu/karoli'

bible = {
    'bookgroups': [
        {'title': 'Ótestamentom',
        'books': []},
        {'title': 'Új Testamentom',
        'books': []}
    ]
}


for book in books['books']:
    #print(book['abbrev'])
    if(book['abbrev'] not in ['1Móz', 'Zsolt', 'Dán', 'Márk', 'Eféz', 'Jel']):
        #continue
        pass

    if book['abbrev'] not in bibletrans_short_karoli:
        print('no short english name')
    if book['abbrev'] not in bibletrans:
        #print('no  english name')
        pass
    chap_num = 1
    bookgroup_id = int(book['number'] / 100) - 1
    bookid = bibletrans_short_karoli[book['abbrev']]
    chapters = []
    #print(book['abbrev'] + ': ' + bibletrans_short_karoli[book['abbrev']])

    while os.path.exists(src_dir + '/' + book['abbrev'] + str(chap_num)):

        chapter_src = src_dir + '/' + book['abbrev'] + str(chap_num)
        chapter = {
            'sections': [],
            'num': chap_num,
            'book': book['abbrev'],
            'chapterid': bookid + '.' + str(chap_num)
        }
        #print('chapter found: ' + book['abbrev'] + str(chap_num))
        section_src = section_src_dir + '/' + books_web[book['abbrev']] + '/' + str(chap_num) + '/' + 'index.html'
        if os.path.exists(section_src):
            #print('section source found')
            with open(section_src,'r') as file:
                section_src_html = file.read()

            parser = ABMHTMLParser()
            parser.feed(section_src_html)
            #print(json.dumps(parser.sections))

        with open(chapter_src,'r') as file:
            chapter_src_html = file.read()
        chapter_parser = SZIHTMLParser()
        chapter_src_html = re.sub(r'<br>', r'<br/>', chapter_src_html)
        chapter_parser.feed(chapter_src_html)
        #print(json.dumps(chapter_parser.chapter_raw))

        section = {}

        passed = True

        for verse in chapter_parser.chapter_raw:
            if verse['num'] in parser.sections:
                if 'verses' in section:
                    chapter['sections'].append(section)
                    section = {}
                section['title'] = parser.sections[verse['num']]['title']
                section['verses'] = []
            #text correction
            verse['text'] = re.sub(r'• ', r'', verse['text']) #remove old * references
            if chapter['chapterid'] + '.' + str(verse['num']) == 'Gal.2.6':
                verse['text'] = re.sub(r'személyét :', r'személyét):', verse['text'])

            #we need to do something with citations here
            if 'cite' in verse:
                #print('-----')
                #print('> ' + verse['cite'])

                #fix single weirdness
                if chapter['chapterid'] + '.' + str(verse['num']) == '1Kgs.12.21':
                    verse['cite'] = re.sub('Vers 21-24: v. ö. ','',verse['cite'])


                verse['cite'] = re.sub('Eféz 2;12;13;Ján;','Eféz 2,12-13; Ján ',verse['cite'])
                verse['cite'] = re.sub('Eféz 5;27;30;','Eféz 5,27-30; ',verse['cite'])
                verse['cite'] = re.sub('2Kor;11,2','2Kor 11,2',verse['cite'])
                verse['cite'] = re.sub('Jel 12;6;;','Jel 12,6;',verse['cite'])
                verse['cite'] = re.sub(r' Ezék. ','; Ezék ',verse['cite'])
                verse['cite'] = re.sub(r'\. Józs,(\d)',r'; Józs \1',verse['cite'])
                verse['cite'] = re.sub(r'\. Józs',r'; Józs',verse['cite'])
                verse['cite'] = re.sub(r'(5Móz|2Sám),(\d+)', r'\1 \2,',verse['cite'])
                verse['cite'] = re.sub(r'5Móz (\d+) ', r'5Móz \1,',verse['cite'])
                verse['cite'] = re.sub(r'\. 2Sám ', r'; 2Sám ',verse['cite'])
                verse['cite'] = re.sub(r'\. (\d)(Kir|Sám|Krón) ', r'; \1\2 ',verse['cite'])
                verse['cite'] = re.sub(r'(1Kir|Neh),13 ', r'\1 13,',verse['cite'])
                verse['cite'] = re.sub(r'Ámós 8-10,', r'Ámós 8,10',verse['cite'])
                verse['cite'] = re.sub(r'Filem (\d+)', r'Filem 1,\1',verse['cite']) #Acts.19.29, Phil.1.3
                verse['cite'] = re.sub(r'Fil 15;1Kor',r'Fil 3,15; 1Kor', verse['cite']) #Phil.3.17

                verse['cite'] = re.sub(r'Fil 4;9;', r'',verse['cite']) #Phil.4.7 -- not ther in 1947 edition
                #TODO verse['cite'] = re.sub(r'Fil 15;', r'Fil 1,25; ',verse['cite']) #Phil.4.7
                verse['cite'] = re.sub(r'^2Pét 2;10-15;Ján;8,34$', r'2Pét 2,10-15; Ján 8,34',verse['cite']) #in 2Pet.2.19
                verse['cite'] = re.sub(r'^2Ján 8', r'2Ján 1,8',verse['cite']) #in Gal.3.4
                verse['cite'] = re.sub(r';Róm;1,8', r'; Róm 1,8',verse['cite']) #in Phil.1.3
                verse['cite'] = re.sub(r'Filem 1,1,4;', r'Filem 1,4; ',verse['cite']) #in Phil.1.3
                verse['cite'] = re.sub(r'Fil,2 ', r'Fil 2,',verse['cite']) #in Phil.2.30
                verse['cite'] = re.sub(r'Kol;3,15;', r'Kol 3,15;',verse['cite']) #in Phil.4.7

                verse['cite'] = re.sub(r'^Filem,1 ', r'Filem 1,',verse['cite']) #in Phil.1.20
                verse['cite'] = re.sub(r'1Kor;4,16;11,1', r'1Kor 4,16;11,1',verse['cite']) #in Phil.1.17



                if(chapter['chapterid'] + '.' + str(verse['num']) == 'Gal.2.11'):
                    verse['cite'] = "Gal 2,12-13; Ján 14,18; Róm 8,9.10.16; 2Kor 3,17;13,5.3; Ésa 57,19"

                if chapter['chapterid'] + '.' + str(verse['num']) in ['John.21.1', 'Acts.12.6', 'Acts.15.18']:
                    continue #there is no citation in these verses, runaway from Acts.19.29


                verse['cite2'] = re.sub(r'\.(\d)(\D+);', r'; \1\2 ', verse['cite'])
                if verse['cite2'] != verse['cite']:
                    pass #print('+2 ' + verse['cite2'])
                verse['cite3'] = re.sub(r'(\d) (Móz|Pét|Thess|Tim|Kor|Ján|Sám|Krón|Kir)', r'\1\2', verse['cite2'])

                if verse['cite2'] != verse['cite3']:
                    verse['cite3'] = re.sub(r'\. (\d)(Móz|Pét|Thess|Tim|Kor|Ján|Krón|Sám)', r'; \1\2', verse['cite3'])
                    pass #print('+3 ' + verse['cite3'])

                books_string = '|'.join(bibletrans_short_karoli.keys())
                verse['cite4'] = re.sub(r'\. (' + books_string + ')', r'; \1', verse['cite3'])
                if verse['cite3'] != verse['cite4']:
                    pass #print('+4 ' + verse['cite4'])


                cites = verse['cite4'].split('; ')



                verse['cites'] = []
                for cite in cites:
                    cite_text = cite.strip()
                    if cite_text == "":
                        continue

                    matchObj = re.search(r'^([^\s\,]+)[\s\,](.*)', cite)
                    if matchObj:

                        cite_book = re.sub(r'\.$', r'',  matchObj[1])
                        #print(cite_book + ': ' + matchObj[2])
                        cite_verses_text = matchObj[2]
                        cite_verses = cite_verses_text.split(';')
                        if len(cite_verses) == 1:
                            cite_verses_text = re.sub(r'[\s\.]+(\d+\,)', r';\1', cite_verses_text)
                            cite_verses = cite_verses_text.split(';')



                        for cite_verse in cite_verses:
                            if cite_verse == "":
                                continue


                            matchObj_1 = re.search(r'^(\d+)\D+(\d+)\.{0,1}$', cite_verse)
                            if matchObj_1:
                                #print("#1 variant found: " + cite_book +  "   " + cite_verse)
                                verse['cites'].append(
                                    {
                                    'ref': bibletrans_short_karoli[cite_book] + '.' + matchObj_1[1] + '.' +  matchObj_1[2],
                                    'text': cite_book + ' ' +  matchObj_1[1] + ',' + matchObj_1[2]
                                    }
                                )
                                continue



                                #print("#1 variant found: " + cite_book +  "   " + cite_verse)

                            matchObj_2 = re.search(r'^(\d+)[^0-9]*(\d+)[^0-9]*(\d+)\.{0,1}$', cite_verse)

                            if matchObj_2 and not matchObj_1:
                                #print("#2 variant found: " + cite_book +  "   " + cite_verse + ' result: ' + cite_book + ' ' +  matchObj_2[1] + ',' + matchObj_2[2] + '-' + matchObj_2[3] )
                                verse['cites'].append(
                                    {
                                    'ref': bibletrans_short_karoli[cite_book] + '.' + matchObj_2[1] + '.' +  matchObj_2[2] + '-' + bibletrans_short_karoli[cite_book] + '.' + matchObj_2[1] + '.' +  matchObj_2[3],
                                    'text': cite_book + ' ' +  matchObj_2[1] + ',' + matchObj_2[2] + '-' + matchObj_2[3]
                                    }
                                )
                                continue

                            matchObj_3 = re.search(r'^(\d+)[^0-9]*(\d+)([^0-9]*)(\d+)([^0-9]*)(\d+)([^0-9]*)$', cite_verse)

                            if matchObj_3 and not matchObj_2 and not matchObj_1:
                                verse_1 = int(matchObj_3[2])
                                delim_1 = matchObj_3[3]
                                verse_2 = int(matchObj_3[4])
                                diff_1 = verse_2 - verse_1

                                delim_2 = matchObj_3[5]
                                verse_3 = int(matchObj_3[6])
                                diff_2 = verse_3 - verse_2

                                if diff_2 < diff_1:
                                    solo = verse_1
                                    pair = [verse_2, verse_3]
                                elif diff_1 <= diff_2:
                                    pair = [verse_1, verse_2]
                                    solo  = verse_3

                                if delim_2 == '-':
                                    solo = verse_1
                                    pair = [verse_2, verse_3]

                                if delim_1 == '-':
                                    solo = verse_3
                                    pair = [verse_1, verse_2]

                                cite_base = bibletrans_short_karoli[cite_book] + '.' + matchObj_3[1]
                                cite_base_hu = cite_book + ' ' +  matchObj_3[1]


                                #print("#3 variant found: " + cite_book +  "   " + cite_verse + ' result: ' + cite_base + '.' +  str(solo) + ' -- ' +  cite_base + '.' +  str(pair[0]) + '-' + cite_base + '.' +  str(pair[1]))

                                if(solo == verse_1):
                                    verse['cites'].append(
                                        {
                                        'ref': cite_base + '.' +  str(solo),
                                        'text': cite_base_hu + ',' + str(solo)
                                        }
                                    )



                                verse['cites'].append(
                                    {
                                    'ref': cite_base + '.' +  str(pair[0]) + '-' + cite_base + '.' +  str(pair[1]),
                                    'text': cite_base_hu + ',' + str(pair[0]) + '-' + str(pair[1])
                                    }
                                )

                                if(solo == verse_3):
                                    verse['cites'].append(
                                        {
                                        'ref': cite_base + '.' +  str(solo),
                                        'text': cite_base_hu + ',' + str(solo)
                                        }
                                    )


                                continue

                            #>51,13. 14. 25-28 (in Dan.1.9)
                            matchobj_4 = re.match(r'(\d+)\,([\d\s\.\-]+)', cite_verse)
                            if matchobj_4 and not matchObj_3 and not matchObj_2 and not matchObj_1:
                                chapter_verse_ref = matchobj_4[1]
                                verse_ref_full_text = matchobj_4[2]
                                verse_ref_full_text = re.sub(r'(\d+\.)\s',r'\1', verse_ref_full_text).strip()
                                if chapter['chapterid'] + '.' + str(verse['num']) in ['Deut.9.4','1Kgs.13.1']:
                                    print("DEBUG: " + verse_ref_full_text)



                                if re.match(r'^[\d\.\-]+$',verse_ref_full_text) and verse_ref_full_text.find('-') > 0:
                                    #print("DEBUG: splitting on dot: " +  verse_ref_full_text)
                                    verse_refs = verse_ref_full_text.split('.')
                                    #print("DEBUG: " + json.dumps(verse_refs))

                                else:
                                    verse_refs = verse_ref_full_text.split(' ')


                                for verse_ref in verse_refs:
                                    verse_ref = re.sub(r'\.$', r'', verse_ref)
                                    if verse_ref == '':
                                        continue
                                    matchObj_41 = re.match(r'^(\d+)$', verse_ref)
                                    if matchObj_41:
                                        verse['cites'].append(
                                            {
                                            'ref': bibletrans_short_karoli[cite_book] + '.' +  chapter_verse_ref + '.' +  matchObj_41[1],
                                            'text': cite_book + ' ' +  chapter_verse_ref + ',' + matchObj_41[1]
                                            }
                                        )
                                        continue
                                    matchObj_42 = re.match(r'^(\d+)\D*\-\D*(\d+)$', verse_ref)
                                    if matchObj_42:
                                        verse['cites'].append(
                                            {
                                            'ref': bibletrans_short_karoli[cite_book] + '.' + chapter_verse_ref + '.' +  matchObj_42[1] + '-' + bibletrans_short_karoli[cite_book] + '.' + chapter_verse_ref + '.' +  matchObj_42[2],
                                            'text': cite_book + ' ' +  chapter_verse_ref + ',' + matchObj_42[1] + '-' + matchObj_42[2]
                                            }
                                        )
                                        continue

                                    if(re.match(r'^[\s\d\.]+$', verse_ref)):

                                        bumbers = []
                                        if(verse_ref.find('-') == -1):
                                            numbers = verse_ref.split('.')
                                            numbers = [int(x) for x in numbers]
                                            numbers.sort()

                                            i = 0
                                            while(i < len(numbers)-1):
                                                if i == 0:
                                                    bumbers.append(numbers[i])
                                                else:
                                                    if numbers[i] - numbers[i-1] == 1 and numbers[i+1] - numbers[i] == 1:
                                                        bumbers.append('-')
                                                    else:
                                                        bumbers.append(numbers[i])
                                                        #if i > 0 and bumbers[i-1] != '-':
                                                        #    bumbers.append('-')

                                                i = i + 1
                                            bumbers.append(numbers[i])
                                        else:
                                            numbers = verse_ref.split(' ')
                                            bumbers = list(filter(lambda x: x != '.', verse_ref))
                                            bumbers = list(map(lambda x: int(x) if x != '-' else '-', bumbers))
                                        #print(bumbers)
                                        i = 0
                                        while i < len(bumbers):
                                            if i+1 < len(bumbers) and (bumbers[i+1] == '-' or  (bumbers[i] != '-'  and bumbers[i+1] == bumbers[i] + 1)):
                                                n = i + 1
                                                while bumbers[n] == '-':
                                                    n = n + 1

                                                verse['cites'].append(
                                                    {
                                                    'ref': bibletrans_short_karoli[cite_book] + '.' + chapter_verse_ref + '.' +  str(bumbers[i]) + '-' + bibletrans_short_karoli[cite_book] + '.' + chapter_verse_ref + '.' +  str(bumbers[n]),
                                                    'text': cite_book + ' ' +  chapter_verse_ref + ',' + str(bumbers[i]) + '-' + str(bumbers[n])
                                                    }
                                                )
                                                i = n + 1
                                            else:
                                                verse['cites'].append(
                                                    {
                                                    'ref': bibletrans_short_karoli[cite_book] + '.' + chapter_verse_ref + '.' +  str(bumbers[i]),
                                                    'text': cite_book + ' ' +  chapter_verse_ref + ',' + str(bumbers[i])
                                                    }
                                                )
                                                i = i + 1

                                        continue

                                    print("(sub) variant found: (" + chapter['chapterid'] + '.' + str(verse['num']) + ") " + cite_book +  "   >" + cite_verse  + "<  >" + verse_ref_full_text + '<')
                                    print('cite unprocessed: ' + chapter['chapterid'] + '.' + str(verse['num']) + ' -- ' + verse['cite4'])


                                continue

                            if not matchobj_4 and not matchObj_3 and not matchObj_2 and not matchObj_1:
                                #passed = False
                                print("variant found: (" + chapter['chapterid'] + '.' + str(verse['num']) + ") " + cite_book +  "   >" + cite_verse  + "<")
                                print('cite unprocessed: ' + chapter['chapterid'] + '.' + str(verse['num']) + ' -- ' + verse['cite4'])




                            verse_ref = re.sub(r'(\d+)\D(\d+).*', r'\1.\2', cite_verse, 1)




                            #print(matchObj[1] + ': ' + cite_verse + '    ' + verse_ref)
                            #ref = bibletrans_short_karoli[cite_book] + '.' + verse_ref
                            #text = matchObj[1] + ' ' + re.sub(r'\.$',r'',cite_verse)
                            try:
                                verse['cites'].append(
                                    {
                                    #Acts.14.15">Csel 14:15
                                    'ref': bibletrans_short_karoli[cite_book] + '.' + verse_ref,
                                    'text': cite_book + ' ' + re.sub(r'\.$',r'',cite_verse)
                                    }
                                )
                            except:
                                print('cite append failed')
#                                passed = False

#                        if not passed:
#                            print('cite unprocessed: ' + chapter['chapterid'] + '.' + str(verse['num']) + ' -- ' + verse['cite2'])






            verse['id'] = chapter['chapterid'] + '.' + str(verse['num'])

            section['verses'].append(verse)
        chapter['sections'].append(section)

        chapters.append(chapter)
        chap_num+=1
        if(chap_num == 3):
            pass #break



    print(bookid + ': ' + str(len(chapters)))
    book_data = {
        'bookid': bookid,
        'abbrev': book['abbrev'],
        'title': book['name'],
        'chapters': chapters,
        }


    if len(chapters) == 0:
        try:
            with open(bookid + '.xml','r') as file:
                book_data['raw_xml'] = file.read()
        except:
            pass




    bible['bookgroups'][bookgroup_id]['books'].append(book_data)






templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
templateEnv.filters["hash"] = j2_hash_filter
TEMPLATE_FILE = "osis.j2.xml"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(bible=bible)

with open("osis.xml", "w") as text_file:
    print(f"{outputText}", file=text_file)

#print(outputText)
#print(yaml.dump(books,indent=2,allow_unicode=True))
