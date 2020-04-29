import os
import torch
import joblib
from cdqa.reader import BertProcessor, BertQA
from cdqa.utils.download import download_squad
import time

start_time = time.time()

print(" \n\n Download SQuAD datasets")
download_squad(dir='./data')
print("--- %s seconds ---" % (time.time() - start_time))

print(" \n\n Preprocess SQuAD 1.1 examples")
train_processor = BertProcessor(do_lower_case=True, is_training=True)
# train_examples, train_features = train_processor.fit_transform(X='./data/SQuAD_1.1/train-v1.1.json')
train_examples, train_features = train_processor.fit_transform(X='./data/irs/train-v1.1.json')
print("--- %s seconds ---" % (time.time() - start_time))

print(" \n\n Train the model")
reader = BertQA(train_batch_size=1,
                # train_batch_size=12,
                learning_rate=3e-5,
                num_train_epochs=2,
                do_lower_case=True,
                output_dir='models')
reader.fit(X=(train_examples, train_features))
print("--- %s seconds ---" % (time.time() - start_time))

print(" \n\n Send model to CPU")
reader.model.to('cpu')
reader.device = torch.device('cpu')
print("--- %s seconds ---" % (time.time() - start_time))

print(" \n\n Save model locally \n\n")
joblib.dump(reader, os.path.join(reader.output_dir, 'bert_qa.joblib'))
print("--- %s seconds ---" % (time.time() - start_time))



import tensorflow_datasets.public_api as tfds
import tensorflow.compat.v2 as tf


def _generate_examples(self, filepath):
	squad_data = tfds.core.SplitGenerator(name=tfds.Split.TRAIN,gen_kwargs={"filepath": "dev-v2.0-copy-jb.json"})
	with tf.io.gfile.GFile(filepath) as f:
		with tf.io.gfile.GFile(filepath) as f:
		  squad = json.load(f)
		  for article in squad["data"]:
			title = article.get("title", "").strip()
			for paragraph in article["paragraphs"]:
			  context = paragraph["context"].strip()
			  for qa in paragraph["qas"]:
				question = qa["question"].strip()
				id_ = qa["id"]

				answer_starts = [answer["answer_start"] for answer in qa["answers"]]
				answers = [answer["text"].strip() for answer in qa["answers"]]
				yield id_, {
					"title": title,
					"context": context,
					"question": question,
					"id": id_,
					"answers": {
						"answer_start": answer_starts,
						"text": answers,
					},
				}

squad_data = _generate_examples("")
print(squad_data)