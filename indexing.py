import os
import pyterrier as pt
#os.environ['TZ'] = 'UTC'

if not pt.started():
  pt.init()
# list of filenames to index
files = pt.io.find_files("/home/masteripper/terrier-project-5.5/WPI_60K/data")
#build the index
indexer = pt.TRECCollectionIndexer("./wt2g_index", verbose=True, blocks=False)
indexref = indexer.index(files)
dest_index_path = "./wt2g_index"
if not os.path.exists("{}/index.properties".format(dest_index_path)):
  dataset = pt.get_dataset("irds:msmarco-passage")
  iter_indexer = pt.IterDictIndexer(dest_index_path)
  indexref = iter_indexer.index(dataset.get_corpus_iter(), meta=['docno', 'text'], meta_lengths=[20, 4096])
else:
  indexref = "{}/index.properties".format(dest_index_path)

# Create Pyterrier index object.
index = pt.IndexFactory.of(indexref)



topics_path = "/home/masteripper/terrier-project-5.5/WPI_60K/data/queries.txt"
topics= topics = pt.io.read_topics(topics_path, format='singleline')
qrels_path ="/home/masteripper/terrier-project-5.5/WPI_60K/50_topics_eval_students/eval_qrels.txt"
qrels = pt.io.read_qrels(qrels_path)
# load the index, print the statistics
index = pt.IndexFactory.of(indexref)
print(index.getCollectionStatistics().toString())