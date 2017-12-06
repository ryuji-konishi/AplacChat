from flask import Flask
import tensorflow as tf
import nmt.nmt

app = Flask(__name__)
from infer_web import controller
