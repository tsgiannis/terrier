
from bs4 import BeautifulSoup
import os

# Set the path to the folder containing the XML files
xml_folder = r'/home/masteripper/terrier-project-5.5/WPI_60K/50_topics_eval_students/topics'

# Set the path to the output TREC topic file
trec_file = r'/home/masteripper/terrier-project-5.5/WPI_60K/queries_ubuntu.txt'

# Open the TREC topic file for writing
with open(trec_file, 'w',encoding='utf-8') as output_file:
    # Loop over the XML files in the folder
    for file_name in os.listdir(xml_folder):
        if file_name.endswith('.xml'):
            # Open the XML file
            print(file_name)
            with open(os.path.join(xml_folder, file_name), 'r',encoding='utf-8') as xml_file:
                xml_data = xml_file.read()

            # Parse the XML data with BeautifulSoup
            soup = BeautifulSoup(xml_data, 'xml')

            # Loop over the <topic> elements in the XML file
            #for content in soup.contents:
                # Extract the topic ID, title, and description
            topic_id = soup.find('patent-document').attrs['ucid']
            title = soup.find('invention-title').contents[0]
            abstract = soup.find('abstract').contents[0].contents[0]
            claims = soup.find('claims').contents[1].text
            full_description =soup.find('description').text
            if full_description.find('FIELD') >0:
                short_descr =soup.find('description').text.split('FIELD')[1].split('CITATION')[0].split('.')[0]
            elif full_description.find('BRIEF SUMMARY OF THE INVENTION')> 0:
                short_descr = soup.find('description').text.split('BRIEF SUMMARY OF THE INVENTION')[1].split('DETAILED DESCRIPTION OF THE INVENTION')[0].split('.')[0]
                # Write the topic data to the TREC topic file
            else :
                short_descr = soup.find('description').text[:500]
            output_file.write(f'<top>\n<num>{topic_id}</num>\n<title>{title}</title>\n<abstract>{abstract}</abstract>\n<claims>{claims}</claims>\n<shortdesc>{short_descr}</shortdesc>\n</top>\n')
