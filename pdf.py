from fpdf import FPDF
from datetime import datetime,timedelta

class PDFSingleton:

    _instance = None

    def __new__(cls, *args, **kwargs):

      

        if cls._instance is None:
            cls._instance = super(PDFSingleton, cls).__new__(cls)
            cls._instance.pdf = FPDF()
              # Accessing custom configuration passed in kwargs
            default_config = kwargs.get('defaultConfig', True)
            cls._instance.directory = "./" + kwargs.get('date') + "/"
            endDateStr = kwargs.get('date', '') + "-" + datetime.now().strftime("%Y")
            cls._instance.endDate = datetime.strptime(endDateStr, "%d-%m-%Y").date()
            cls._instance.startDate = cls._instance.endDate - timedelta(days=kwargs.get('timePeriod', 7))
            if default_config:
                cls._instance.setDefaultConfiguration()
        return cls._instance

    def setDefaultConfiguration(self):
        """Initialize default text configurations."""
        self.textConfiguration = {
            'title': {
                'font': 'Helvetica',
                'style': 'bold',
                'size': 24,
                'color': (0, 0, 0)  # Black color
            },
            'subtitle': {
                'font': 'AriHelveticaal',
                'style': 'italic',
                'size': 18,
                'color': (100, 100, 100)  # Dark grey color
            },
            'sectionHeader': {
                'font': 'Helvetica',
                'style': 'bold',
                'size': 16,
                'color': (50, 50, 50)  # Grey color
            },
            'body': {
                'font': 'Helvetica',
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
        
    
    def updateLetterheadConfiguration(self, **kwargs):
        """
        Update the letterhead configuration.
        
        :param kwargs: Key-value pairs to update the configuration.
        """
        self.letterheadConfiguration.update(kwargs)

    def getTimeRange(self):
        return self.endDate.strftime("%m/%d/%Y") + " - " + self.startDate.strftime("%m/%d/%Y")

    def addPage(self):
        self.pdf.add_page()

    def writeToPDF (self, textType, text):
        self.pdf.set_text_color(r=self.textConfiguration[textType]['color'][0],g=self.textConfiguration[textType]['color'][1],b=self.textConfiguration[textType]['color'][2])
        self.pdf.set_font(self.textConfiguration[textType]['font'], self.textConfiguration[textType]['style'], self.textConfiguration[textType]['size'])
        self.pdf.write(self.lineHeight, text)
    
    def addCoverletter (self):
        self.pdf.image(self.letterheadConfiguration['directory'], self.letterheadConfiguration['x'], self.letterheadConfiguration['y'], self.width)
            

    def build (self):
        self.pdf.output(self.directory + "completionRateReport_"+ self.endDate.strftime("%m_%d_%Y")+".pdf")
        print("Completion report built.")

    def ln(self, space = 10):
        self.pdf.ln(10)