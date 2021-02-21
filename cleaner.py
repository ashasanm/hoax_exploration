import pandas as pd
import re

class Splitter:
    def load_data(self):
        data = pd.read_csv('turnbackhoax.csv')
        return data


    def replace_text(self, text):
        result = str(text).replace("(function(d, s, id) {  var js, fjs = d.getElementsByTagName(s)[0];  if (d.getElementById(id)) return;  js = d.createElement(s); js.id = id;  js.src = 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.10';  fjs.parentNode.insertBefore(js, fjs);}(document, 'script', 'facebook-jssdk'));", '')
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
            divided.append(result)
        return divided


    def get_data(self, content):
        new_text = {
            'category': content[0],
            'source_hoax': content[1],
            'narration': content[2],
            'explanation_detail': content[3],
            'source_validation': content[4],
        }
        return new_text


    def save_data(self, new_data):
        df = pd.DataFrame(new_data)
        df.to_json('turnbackhoax_content.json')

    
    
    def main(self):
        data = self.load_data()
        new_data = []
        for text in data['raw_content']:
            text = self.replace_text(text)
            divided = self.find_data(text)
            new_text = self.get_data(content=divided)
            new_data.append(new_text)
        self.save_data(new_data)


if __name__ == '__main__':
    splitter = Splitter()
    splitter.main()