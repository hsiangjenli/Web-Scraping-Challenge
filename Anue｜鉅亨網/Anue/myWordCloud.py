from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import jieba
import sys

userdictPATH = sys.path[0] + '\\userdict.txt'
fontPATH = './Anue/jf-openhuninn-1.1.ttf'

class myWordCloud:
    def __init__(self, 
                 #data=None, 
                 #filename='myWordCloud', 
                 mask='./Anue/bear-market.png', 
                 font_path=fontPATH, 
                 background_color=None, 
                 recolor=False):
        
        '''
        Parameters
        ----------
        mask : string
            文字雲的形狀。圖片的路徑。
        font_path : string
            個人化字體設定。字型的路徑。
        background_color : string
            文字雲的背景顏色。
            e.g. '#FFFFFF', 'white'
        recolor : bool
            字的顏色是否根據mask重新上色。
        '''
        self.mask = mask
        self.font_path = font_path
        self.background_color = background_color
        self.recolor = recolor

        from PIL import Image

    def generate(self):
        self.wc = WordCloud(mode="RGBA", 
                            background_color=self.background_color,
                            scale=5, 
                            mask=self.color_mask, 
                            font_path=self.font_path)
        self.wc.generate_from_frequencies(self.frequency)
        
        if self.recolor:
            self.myrecolor()
        
        plt.figure(figsize=(20, 20))
        plt.imshow(self.wc, interpolation="bilinear")
        self.wc.to_file(f'WC_{self.filename}.png')

    def generate_from_frequency(self):

        raise NotImplementedError

    def fit(self, filename='myWordCloud', data=None):
        '''
        Parameters
        ----------
        data : string
            文章內容
        filename : string
            輸出時的文字雲的檔案名稱，不須包含副檔名。
        '''
        self.filename = filename
        self.data = data
        
        self.userdict()
        self.stopwords()
        self.to_frequency()
        try:
            self.mymask()
        except:
            pass
    
    def userdict(self):       
        data = self.data
        data = data.translate({ord(c):None for c in list("(),.“”（）「」，。、：；！|\n/ 《》〔〕〈〉？<>【】")})
        jieba.load_userdict("./Anue/userdict.txt")
        self.terms = jieba.cut(data)
        return self
    
    def stopwords(self):        
        with open("./Anue/stopwords.txt", "r", encoding = "utf-8") as fp:
            stopwords = [word.strip() for word in fp.readlines()]
            stopwords.append('nbsp')
            self.keyterms = [keyterm for keyterm in self.terms if keyterm not in stopwords]        
        return self
        
    def to_frequency(self):
        frequency = {}
        for word in self.keyterms:
            if word.lower() not in frequency:
                frequency[word.lower()] = 1
            else:
                frequency[word.lower()] += 1
        self.frequency = {f: frequency[f] for f in frequency if len(f)>1}
        return self
    
    def mymask(self):
        self.mask = np.array(Image.open(self.mask))
        self.mask = self.mask[::1, ::1]
        color_mask = self.mask.copy()
        color_mask[color_mask.sum(axis=2) == 0] = 255
        self.color_mask = color_mask
        return self

    def myrecolor(self):
        image_colors = ImageColorGenerator(self.mask)
        self.wc.recolor(color_func=image_colors)
        



