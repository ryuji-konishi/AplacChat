# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Utility to handle vocabularies."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import codecs
import os
import tensorflow as tf

from ..utils import misc_utils as utils

# TODO(ebrevdo): When we add code to load pretrained embeddings,
# ensure that the first three rows of the embedding correspond to UNK, SOS, EOS.
UNK = "<unk>"
SOS = "<s>"
EOS = "</s>"
UNK_ID = 0


def init_vocab(sos, eos, unk):
  """Initialize with special symbols."""
  vocab = []
  vocab_hash = {}
  freq_hash = {}
  for word in [unk, sos, eos]:
    if word:
      vocab_hash[word] = len(vocab)
      freq_hash[word] = 0
      vocab.append(word)
  return vocab, vocab_hash, freq_hash


def add_word(word, vocab, vocab_hash, freq_hash=None):
  """Check if a word exists. If not, add to vocab."""
  if word not in vocab_hash:
    vocab_hash[word] = len(vocab)  # This line needs to be first
    vocab.append(word)
    if freq_hash:
      freq_hash[word] = 0
  if freq_hash:
    freq_hash[word] += 1


def save_vocab(path, vocab):
  """Save a list of words into file, one item per line."""
  utils.print_out("# Save vocab to %s" % path)
  with codecs.getreader("utf-8")(tf.gfile.GFile(path, "w")) as f:
    for word in vocab:
      f.write("%s\n" % word)


def check_and_extract_vocab(vocab_file,
                            corpus_file,
                            out_dir,
                            freq=None,
                            max_vocab_size=None,
                            sos=None,
                            eos=None,
                            unk=None):
  """Check if vocab_file doesn't exist, create from corpus_file."""
  if tf.gfile.Exists(vocab_file):
    utils.print_out("# Vocab file %s exists" % vocab_file)
    vocab = []
    with codecs.getreader("utf-8")(tf.gfile.GFile(vocab_file, "rb")) as f:
      vocab_size = 0
      for word in f:
        vocab_size += 1
        vocab.append(word.strip())

    # Verify if the vocab starts with unk, sos, eos
    # If not, prepend those tokens & generate a new vocab file
    if not unk: unk = UNK
    if not sos: sos = SOS
    if not eos: eos = EOS
    assert len(vocab) >= 3
    if vocab[0] != unk or vocab[1] != sos or vocab[2] != eos:
      utils.print_out("The first 3 vocab words [%s, %s, %s]"
                      " are not [%s, %s, %s]" %
                      (vocab[0], vocab[1], vocab[2], unk, sos, eos))
      vocab = [unk, sos, eos] + vocab
      vocab_size += 3
      new_vocab_file = os.path.join(out_dir, os.path.basename(vocab_file))
      with codecs.getreader("utf-8")(tf.gfile.GFile(new_vocab_file, "w")) as f:
        for word in vocab:
          f.write("%s\n" % word)
      vocab_file = new_vocab_file
  else:
    vocab, _ = extract_corpus_vocab(
        corpus_file, sos=sos, eos=eos, unk=unk,
        freq=freq, max_vocab_size=max_vocab_size)
    save_vocab(vocab_file, vocab)

  vocab_size = len(vocab)
  return vocab_size, vocab_file


def extract_corpus_vocab(path,
                         freq=None,
                         max_vocab_size=None,
                         sos=None,
                         eos=None,
                         unk=None):
  """Generate vocabulary from a text file."""
  utils.print_out(
      "# Generating vocab from %s, freq=%s, max_vocab_size=%s ... " %
      (path, str(freq), str(max_vocab_size)), new_line=False)

  vocab, vocab_hash, freq_hash = init_vocab(sos=sos, eos=eos, unk=unk)
  num_train_words = 0
  num_lines = 0
  with codecs.getreader("utf-8")(tf.gfile.GFile(path, "r")) as f:
    for line in f:
      words = line.strip().split()
      num_train_words += len(words)
      for word in words:
        add_word(word, vocab, vocab_hash, freq_hash)

      num_lines += 1
      if num_lines % 100000 == 0:
        utils.print_out("  (%d)" % num_lines, new_line=False)
    utils.print_out("\n  vocab_size=%d, num_train_words=%d, num_lines=%d" %
                    (len(vocab), num_train_words, num_lines))

    if unk and (freq or max_vocab_size):
      vocab, vocab_hash = filter_vocab(
          freq_hash, freq, max_vocab_size, sos=sos, eos=eos, unk=unk)

  return vocab, vocab_hash


def filter_vocab(freq_hash, freq, max_vocab_size, sos=None, eos=None, unk=None):
  """Filter out rare words (<freq) or keep the top vocab_size frequent words."""
  vocab, vocab_hash, _ = init_vocab(sos=sos, eos=eos, unk=unk)
  sorted_items = sorted(freq_hash.items(), key=lambda x: x[1], reverse=True)

  if freq > 0:
    for (word, _) in sorted_items:
      if freq_hash[word] < freq:  # rare word
        break
      add_word(word, vocab, vocab_hash)

    utils.print_out("  convert rare words (freq<%d) to %s:"
                    " new vocab size=%d" % (freq, unk, len(vocab)))
  else:  # Get top frequent words
    assert max_vocab_size > 0
    for (word, _) in sorted_items:
      add_word(word, vocab, vocab_hash)
      if len(vocab) == max_vocab_size:
        break
    utils.print_out("  update vocab: new vocab size=%d" % len(vocab))

  return vocab, vocab_hash
