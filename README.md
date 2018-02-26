# AplacChat

AplacChat is a deep learning project that focuses on Neural Machine Translation (NMT).
AplacChat consists of the following components.
* HTML Parser
* Chat
* Front-End Web Page

## Running Environment
* Python 2 for MacOS
* Python 3 for Windows
* Tensorflow 1.4
* Google Cloud Platform used for NMT Training
* Amazon Web Service used for NMT Inference back-end
* Microsoft Azure used for front-end web page

## HTML Parser
HTML Parser is used to parse Japanese sentenses in HTML files and emit files that are the input dataset for NMT training. The dataset files that are generated by HTML Parser are:
* Training source (*.src)
* Training target (*.tgt)
* Vocaburary (vocab.src)

The HTML files, that are fed into HTML Parser, are downloaded from APLaC site and saved locally as HTML (*.html) files. 

[How to setup and run HTML Parser](<README%20Setup%20HTML%20Parser.md>)

## Chat
Chat is the component that plays the main role of the AplacChat project that is NMT Training and Inference. The running environment of this component changes depending on the project phases and the usage of this component.

### Local Development
When the project is in the development phase and you test run it locally, your local computer (MacOS X) is used. Here both NMT Training and Inference are your main subject.

[How to setup Chat on MacOS](<README%20Setup%20Chat%20on%20MacOS.md>)

### NMT Training
The project phase moves on, when you want to train Chat, Google Cloud Platform (GCP) is used. This is the case where you want to run training intensively but your local machine is not sufficient as a resource, and thus you need a more powerful machine. You upload the Chat component to GCP and it runs on there.

[How to setup Chat on GCP](<README%20Setup%20chat%20on%20GCP.md>)

### NMT Inference
The final phase is inference. In this phase you upload the Chat component to Amazon Web Service (AWS) in which a Linux EC2 instance executes the inference part of Chat.

[How to setup Chat on AWS EC2](<README%20Setup%20chat%20on%20AWS%20EC2.md>)

## Front-End Web Page
Front-End is a web page that accepts the text the user types in, sends the text to the Chat component and shows the translation that is the result of NMT Inference.

[How to setup Front-End on Linux](<README%20Setup%20frontend%20on%20Linux.md>)
