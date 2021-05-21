import pdfkit
from DarkWebHelpers.app import AppConfigurations


def Create():
    try:
        with open(AppConfigurations.HTML_FILE, 'rb') as f:
            config = pdfkit.configuration(wkhtmltopdf=AppConfigurations.PATH_TO_wkhtmltopdf)
            pdfkit.from_file(output_path=AppConfigurations.PDF_FILE, configuration=config,input=AppConfigurations.HTML_FILE)
        return True
    except BaseException as e:
        print(e)
        return False
