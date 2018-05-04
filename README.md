# AplacChat

AplacChat is a deep learning project that focuses on Neural Machine Translation (NMT). The final outcome is [here](http://aplac-chat.koni4.net/).
AplacChat consists of the following components.
* Corpus Builder
* Chat
* Front-End Web Page

## Running Environment
* Python 2 for MacOS/Linux
* Python 3 for Windows
* Tensorflow 1.4
* Google Cloud Platform used for NMT Training
* .NET Core 2

## Corpus Builder
Corpus Builder reads text data from HTML files, generates standard corpus files and generates the NMT dataset. The NMT dataset files inclue:
* Training source (train.src/dev.src/test.src)
* Training target (train.tgt/dev.tgt/test.tgt)
* Vocaburary (vocab.src)

Corpus Builder can export text data from a banch of HTML files. For the AplacChat project, the HTML files are downloaded from [APLaC site](https://aplac.net/) and saved locally as HTML (*.html) files.

For more details refer to [Corpus Builder](CorpusBuilder/README.md)

## Chat
Chat is the component that plays the main role of the AplacChat project that is NMT Training and Inference. The running environment of this component changes depending on the project phases and the usage of this component.

### Local Development
When the project is in the development phase and you test run it locally, your local computer (MacOS X) is used. Here both NMT Training and Inference are your main subject.

[How to setup Chat on MacOS](chat/README%20Setup%20Chat%20on%20MacOS.md)

### NMT Training
The project phase moves on, when you want to train Chat, Google Cloud Platform (GCP) is used. This is the case where you want to run training intensively but your local machine is not sufficient as a resource, and thus you need a more powerful machine. You upload the Chat component to GCP and it runs on there.

[How to setup Chat on GCP](chat/README%20Setup%20chat%20on%20GCP.md)

### NMT Inference
The final phase is inference. In this phase you run the Chat component on the production Linux server.

The Chat component can be separatelly setup, but here we set it up together with the Front-End component on the same Linux instance on Amazon Web Service (AWS). Follow the steps in [How to setup Chat/Frontend on AWS EC2](frontend/README%20Setup%20chat-frontend%20on%20AWS%20EC2.md).

## Front-End Web Page
Front-End is a web page that accepts user inputs, transfer the input text to the Chat component for NMT inference, and shows the translation result that is returned from the Chat component.

To start a local debugging on your Mac with Visual Studio Code, read [How to setup Front-End on MacOS](frontend/README%20Setup%20frontend%20on%20MacOS.md). To deploy on to AWS EC2 Linux instance, refer to [How to setup Chat/Frontend on AWS EC2](frontend/README%20Setup%20chat-frontend%20on%20AWS%20EC2.md).
