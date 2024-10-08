import itertools
import os
import subprocess
import os
import random
from random import sample
import shutil

def get_result_file(result_folder):
    import os

    folder_path = result_folder
    extension = ".res"

    for filename in os.listdir(folder_path):
        if filename.endswith(extension):
            return filename


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        # if the demo_folder directory is not present
        # then create it.
        os.makedirs(folder_path)

#define Terrier
terrier_exec = '/home/masteripper/terrier-project-5.5/bin/terrier'
terrier_etc = '/home/masteripper/terrier-project-5.5/etc'
terrier_batch = '/home/masteripper/terrier-project-5.5/batch/index'
terrier_batch_results = '/home/masteripper/terrier-project-5.5/batch/results'

# Define the possible values for each property
#wmodels ='DPH'
trecquerytags_processes = ['TOP','NUM','TITLE','ABSTRACT','SHORTDESC','SUMMARY']
trecquerytags_skips = ['DESC','NARR']
termpipelines = ['Stopwords', 'PorterStemmer', 'Stopwords,PorterStemmer','WeakPorterStemmer','TRv2PorterStemmer',
                 'SnowballStemmer','EnglishSnowballStemmer']
fieldtags_processes = ['TITLE', 'ELSE']


# Read the Terrier properties file
terrier_sample_properties = os.path.join(terrier_etc,'terrier_sample.properties')
terrier_properties = os.path.join(terrier_etc,'terrier.properties')
with open(terrier_sample_properties) as f:
    lines = f.readlines()

# Generate all possible combinations of the properties
for i in range(30):
    wmodels = random.choice(['BM25', 'DPH', 'InL2', 'Hiemstra_LM','BM25F' ])
    trecquerytags_processes_rnd = random.randint(1, len(trecquerytags_processes))
    trecquerytags_skips_rnd = random.randint(1, len(trecquerytags_skips))
    termpipelines_rnd = random.randint(1, len(termpipelines))
    fieldtags_processes_rnd = random.randint(1, len(fieldtags_processes))
    combinations = [wmodels,
                    sample(trecquerytags_processes,trecquerytags_processes_rnd),
                    sample(trecquerytags_skips,trecquerytags_skips_rnd),
                    sample(termpipelines,termpipelines_rnd),
                    sample(fieldtags_processes,fieldtags_processes_rnd)]

# Generate a new properties file, execute indexing and retrieval for each combination

    new_lines = []
    for line in lines:
        if line.startswith('querying.default.controls='):
            to_replace = line.split(',')
            result = [y for y in to_replace if 'wmodel' in y]
            if len(result)>0 :
                result_splitted = result[0].split('=')
                result_resplitted =result_splitted[1].split(':')
                result_resplitted[1] = combinations[0]
                w_model  =':'.join(result_resplitted)
                result_splitted[1] = w_model
                quering_default = '='.join(result_splitted)
                to_replace[0]=quering_default
                new_lines.append(','.join(to_replace))





        elif line.startswith('TrecQueryTags.process='):
            processed = ','.join(combinations[1])
            new_lines.append(f'TrecQueryTags.process={processed}\n')
        elif line.startswith('TrecQueryTags.skip='):
            skipped = ','.join(combinations[2])
            new_lines.append(f'TrecQueryTags.skip={skipped}\n')
        elif line.startswith('termpipelines='):
            term_lines = ','.join(combinations[3])
            new_lines.append(f'termpipelines={term_lines}\n')
        elif line.startswith('FieldTags.process='):
            tag_process=  ','.join(combinations[4])
            new_lines.append(f'FieldTags.process={tag_process}\n')
        elif line.startswith('terrier.index.path'):
            new_lines.append('# placeholder\n')

        else:
            new_lines.append(line)
    index_folder = os.path.join(terrier_batch,f"index_{i}")
    results_folder = os.path.join(terrier_batch_results, f"results_{i}")
    ##
    old_name = terrier_properties
    new_name = terrier_properties + f"_0{i}"
    os.rename(old_name, new_name)
    new_lines.append(f'terrier.index.path={index_folder}/\n')
    new_lines.append(f'trec.results={results_folder}/\n')
    new_lines.append("trec.topics = /home/masteripper/terrier-project-5.5/WPI_60K/queries_ubuntu.txt")
    with open(terrier_properties, 'w') as f:
        f.writelines(new_lines)
#
    # if not os.path.exists(index_folder):
    #     # if the demo_folder directory is not present
    #     # then create it.
    #     os.makedirs(index_folder)
        create_folder_if_not_exists(index_folder)
        create_folder_if_not_exists(results_folder)
    #http://terrier.org/docs/v4.2/properties.html

        """  Indexing"""
    subprocess.run([f'{terrier_exec}', 'batchindexing'])
    """Retrieval"""
#trec.results=/path/to/results/for/WT2G
    subprocess.run([f'{terrier_exec}', 'batchretrieval'])
    """ Evaluating """
    #subprocess.run([f'{terrier_exec}', 'batchindexing'])
    # /trec_eval /home/masteripper/terrier-project-5.5/WPI_60K/50_topics_eval_students/eval_qrels.txt /home/masteripper/terrier-project-5.5/var_temp/results/DPH_0.res
    #https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
    path_trec_eval = "/home/masteripper/terrier-project-5.5/bin/trec_eval"
    results_file = get_result_file(results_folder)
    results_file = os.path.join(results_folder,results_file)
    qrels_file = "/home/masteripper/terrier-project-5.5/WPI_60K/50_topics_eval_students/eval_qrels.txt"
    #result = subprocess.run([f'{path_trec_eval}',f'{qrels_file}',f'{results_file}'],stdout=subprocess.PIPE)
    #result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
    terrier_properties_new_path = os.path.join(index_folder,"terrier.properties")
    trec_eval_file = os.path.join(results_folder,"results.txt")
    with open(trec_eval_file, "w") as output_file:
        subprocess.run([f'{path_trec_eval}',f'{qrels_file}',f'{results_file}'], stdout=output_file)
    trec_eval_score = os.path.join(results_folder, "results_score.txt")
    with open(trec_eval_score, "w") as output_file:
        subprocess.run([f'{path_trec_eval}','-m map',f'{qrels_file}',f'{results_file}'], stdout=output_file)
    shutil.copy(terrier_properties, terrier_properties_new_path)


    #subprocess.run(['terrier', 'batchretrieve', '-Dterrier.index.path=index_{}'.format(i), '-Dtrec.results.file=results_{}.txt'.format(i), '-p', 'terrier_{}.properties'.format(i)])
    #subprocess.run(['trec_eval', '-q', '-c', '-M1000', '-m', 'map', 'qrels.txt', 'results_{}.txt'.format(i)], stdout=open('eval_{}.txt'.format(i), 'w'))

# Collect the evaluation results for each combination and print them to the console
# for i, combination in enumerate(combinations):
#     with open('eval_{}.txt'.format(i)) as f:
#         lines = f.readlines()
#     for line in lines:
#         if line.startswith('map'):
#             map_score = line.split()[2]
#             print('Combination {}: wmodel={}, TrecQueryTags.process={}, TrecQueryTags.skip={}, termpipelines={}, FieldTags.process={}, MAP={}'.format(i, combination[0], combination[1], combination[2], combination[3], combination[4], map_score))
