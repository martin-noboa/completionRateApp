from fpdf import FPDF

class PDFSingleton:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PDFSingleton, cls).__new__(cls)
            cls._instance.pdf = FPDF()
            cls._instance.setDefaultConfiguration()
        return cls._instance

    def setDefaultConfiguration(self):
        """Initialize default text configurations."""
        self.textConfiguration = {
            'title': {
                'font': 'Arial',
                'style': 'bold',
                'size': 24,
                'color': (0, 0, 0)  # Black color
            },
            'subtitle': {
                'font': 'Arial',
                'style': 'italic',
                'size': 18,
                'color': (100, 100, 100)  # Dark grey color
            },
            'sectionHeader': {
                'font': 'Arial',
                'style': 'bold',
                'size': 16,
                'color': (50, 50, 50)  # Grey color
            },
            'body': {
                'font': 'Arial',
                'style': 'normal',
                'size': 12,
                'color': (0, 0, 0)  # Black color
            }
        }

        self.letterheadConfiguration = {
            'directory': "./resources/header.png",
            'x':0,
            'y':0,
        }

        self.lineHeight = 7
        self.width = 210
        self.height= 297


    def updateTextConfiguration(self, textType, **kwargs):
        """
        Update the text configuration for a specific text type.
        
        :param textType: One of 'title', 'subtitle', 'section_header', 'body'.
        :param kwargs: Key-value pairs to update the configuration.
        """
        if textType in self.textConfiguration:
            self.textConfiguration[textType].update(kwargs)
        else:
            raise ValueError(f"Invalid text type: {textType}")
        
    
    def updateLetterheadConfiguration(self, textType, **kwargs):
        """
        Update the letterhead configuration.
        
        :param kwargs: Key-value pairs to update the configuration.
        """
        self.textConfiguration[textType].update(kwargs)


    def addPage(self):
        self.pdf.add_page()

    def writeToPDF (self, textType, text):
        self.pdf.set_text_color(r=self.textConfiguration[textType]['color'][0],g=self.textConfiguration[textType]['color'][1],b=self.textConfiguration[textType]['color'][2])
        self.pdf.set_font(self.textConfiguration[textType]['font'], self.textConfiguration[textType]['style'], self.textConfiguration[textType]['size'])
        self.pdf.write(self.lineHeight, text)
    
    def addCoverletter (self):
        self.pdf.image(self.letterheadConfiguration['directory'], self.letterheadConfiguration['x'], self.letterheadConfiguration['y'], self.width)
            

