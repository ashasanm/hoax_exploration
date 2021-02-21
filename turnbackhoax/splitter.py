import pandas as pd
import re

class Splitter:
    def __init__(self, raw_content):
        self.raw_content = raw_content


    def replace_text(self):
        result = str(self.raw_content).replace("(function(d, s, id) {  var js, fjs = d.getElementsByTagName(s)[0];  if (d.getElementById(id)) return;  js = d.createElement(s); js.id = id;  js.src = 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.10';  fjs.parentNode.insertBefore(js, fjs);}(document, 'script', 'facebook-jssdk'));", '')
        result = result.replace('[…]', '')
        result = result.replace('\n', '')
        result = result.replace('\xa0', '')
        result = result.replace('=', '')
        result = result.replace('[', '')
        result = result.replace(']', '')
        result = result.replace('Selengkapnya di bagian PENJELASAN dan REFERENSI', '')
        result = result.replace('Selengkapnya di PENJELASAN dan REFERENSI', '')
        return result


    def check_data(self, text):
        validator = [
            'KATEGORI|Kategori', 'SUMBER|Sumber',
            'NARASI|Narasi', 'PENJELASAN|Penjelasan',
            'REFERENSI|Referensi'
        ]
        results = []
        for validate in validator:
            try:
                result = re.search(validate, text)
                result = result.group(0)
                results.append(result)
            except:
                result = ''
                results.append(result)

        return results


    def find_data(self, text):  
        divided = []
        index = 0
        check_li = self.check_data(text)
        for found in check_li:
            result = text[text.find(found):]
            index += 1
            if index <= 4 and found != '':
                stop = check_li[index]
                result = result[:result.find(stop)]
            elif found == '':
                result = ''
            result = self.clean_tag(result)
            divided.append(result)
        return divided

    
    def clean_tag(self, text):
        text = text.lower()
        result = text.replace(':', '')
        result = result.replace('kategori', '')
        result = result.replace('sumber', '')
        result = result.replace('narasi', '')
        result = result.replace('penjelasan', '')
        result = result.replace('referensi', '')
        result = " ".join(result.split())

        return result


    def get_data(self, content):
        source_val = []
        source_li = content[4].split(' ')
        for url in source_li:
            if 'http' in url:
                source_val.append(url)

        new_text = {
            'category': content[0],
            'source_hoax': content[1],
            'narration': content[2],
            'explanation_detail': content[3],
            'source_validation': source_val,
        }
        return new_text

    
    def start_split(self):
        text = self.replace_text()
        divided = self.find_data(text)
        content = self.get_data(divided)
        return content

