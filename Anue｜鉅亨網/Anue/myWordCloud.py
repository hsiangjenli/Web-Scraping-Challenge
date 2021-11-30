


class myWordCloud:
	def __init__(self, 
				 data=None, 
				 filename='myWordCloud', 
				 mask='./bear-market.png', 
				 font_path='./jf-openhuninn-1.1.ttf', 
				 background_color='white', 
				 recolor=False):
		
		'''
		Parameters
		----------
		data : string
			文章
		filename : string
			輸出時的文字雲的檔案名稱，不須包含副檔名。
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

		self.data = data
		self.filename = filename
		self.mask = mask
		self.font_path = font_path
		self.background_color = background_color
		self.recolor = recolor

		from PIL import Image

	def generate(self):

		raise NotImplementedError


	def generate_from_frequency(self):

		raise NotImplementedError

	def preprocssing(self):
		'''
		# Preprocessing Data

		## Adding your personal stopwords
		> 'stopwords.txt'

		## Adding your personal userdict
		> 'userdict.txt'

		'''
		data = self.data

		return cleaned_data


	def to_frequency(self):
		data = self.data
		frequency = {}


		self.frequency = frequency

		return frequency

	def recolor(self):

		mask = np.array(Image.open(self.mask))

		if self.recolor:




