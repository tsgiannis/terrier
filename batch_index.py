import os
import pyterrier as pt
#os.environ['TZ'] = 'UTC'

if not pt.started():
  pt.init()
# list of filenames to index

#build the index
indexer = pt.TRECCollectionIndexer("./wt2g_index", verbose=True, blocks=False)
files = pt.io.find_files("/home/masteripper/terrier-project-5.5/WPI_60K/data")

dest_index_path = "./wt2g_index"
if not os.path.exists(f"{dest_index_path}/data.properties"):
  indexer = pt.TRECCollectionIndexer("./wt2g_index", verbose=True, blocks=False)
  files = pt.io.find_files("/home/masteripper/terrier-project-5.5/WPI_60K/data")
  indexref = indexer.index(files)

else:
  indexref = f"{dest_index_path}/data.properties"

# Create Pyterrier index object.
index = pt.IndexFactory.of(indexref)



topics_path = "/home/masteripper/terrier-project-5.5/WPI_60K/queries.txt"
topics= topics = pt.io.read_topics(topics_path, format='singleline')
qrels_path ="/home/masteripper/terrier-project-5.5/WPI_60K/50_topics_eval_students/eval_qrels.txt"
qrels = pt.io.read_qrels(qrels_path)
# load the index, print the statistics

# Run Pyterrier experiment for BM25, DPH and DPH+BO1
bm25 = pt.BatchRetrieve(index, wmodel="BM25", verbose=True)
dph = pt.BatchRetrieve(index, wmodel='DPH', verbose=True)
bo1 = dph >> pt.rewrite.Bo1QueryExpansion(index) >> dph

pt.Experiment(
    [bm25, dph, bo1],
    topics,
    qrels,
    ["map"],
    names=['bm25', 'dph', 'dph+bo1'],filter_by_topics=False,filter_by_qrels=False
  )