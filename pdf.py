class PDFSingleton:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PDFSingleton, cls).__new__(cls)
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

    def updateTextConfiguration(self, text_type, **kwargs):
        """
        Update the text configuration for a specific text type.
        
        :param text_type: One of 'title', 'subtitle', 'section_header', 'body'.
        :param kwargs: Key-value pairs to update the configuration.
        """
        if text_type in self.textConfiguration:
            self.textConfiguration[text_type].update(kwargs)
        else:
            raise ValueError(f"Invalid text type: {text_type}")
        
    
    def updateLetterheadConfiguration(self, text_type, **kwargs):
        """
        Update the letterhead configuration.
        
        :param kwargs: Key-value pairs to update the configuration.
        """
        self.textConfiguration[text_type].update(kwargs)

        

    def reset_text_config(self):
        """Reset all text configurations to their default values."""
        self._initialize_default_config()

    def build_pdf(self, content):
        """Simulate building the PDF with the current configuration."""
        print("Building PDF with the following text configurations:")
        for text_type, config in self.textConfiguration.items():
            print(f"{text_type.capitalize()} Config: {config}")
        # Implement actual PDF generation logic here
        print("PDF content:", content)

