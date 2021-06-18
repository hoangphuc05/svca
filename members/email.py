from mailjet_rest import Client
import os
import html2text
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
print(dotenv_path)
load_dotenv(dotenv_path)


api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.environ['MJ_APIKEY_PRIVATE']
mailjet = Client(auth=(api_key, api_secret))

text_maker = html2text.HTML2Text()
text_maker.ignore_images = True
text_maker.ignore_links = True
text_maker.ignore_tables = True
text_maker.ignore_emphasis = True


def send_an_email(subject, html_content, recipients, variables, from_email, from_name):
    # try to get the text from the html content
    text_content = ""
    try:
        text_content = text_maker.handle(html_content)
    except:
        pass
    data = {
        'FromEmail': from_email,
        'FromName': from_name,
        'Subject': subject,
        'Text-part': text_maker.handle(text_content),
        'Html-part': html_content,
        # 'Vars': variables,
        'Recipients': recipients,
    }
    result = mailjet.send.create(data=data)