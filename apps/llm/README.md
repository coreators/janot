### Llama Setup
* llama-cpp-python

[llama-cpp-python](https://github.com/abetlen/llama-cpp-python)

### Install the requirements
Install llama-cpp-python

```
$ poetry add llama-cpp-python
```
## Download models

This example covers only [llama.cpp](https://github.com/ggerganov/llama.cpp) (GGML) models. 

Models should be placed inside the `models/` folder. 

[Hugging Face](https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads) is the main place to download models. These are some examples:

* [WizardLM 7B](https://huggingface.co/TheBloke/WizardLM-7B-uncensored-GGML)
* [Guanaco 7B](https://huggingface.co/TheBloke/guanaco-7B-GGML)

You can automatically download a model from HF using the cript `download-model.py`:

```
python download-model.py organization/model
```

For example:

```
python download-model.py facebook/opt-1.3b
```

* If you want to download a model manually, you can drop the file name contains `ggml` somewhere and ends in `.bin`.

## Starting the web UI

Before start change `model_path` in `llama.talk.py`.

```
python llama.talk.py
```

## Web Server

`llama-cpp-python` offers a web server which aims to 
act as a drop-in replacement for the OpenAI API. This allows you to use llama.cpp compatible models with any OpenAI compatible client (language libraries, services, etc).

To install the server package and get started:

```
pip install llama-cpp-python[server]
python3 -m llama_cpp.server --model models/7B/ggml-model.bin
```

You can use local `llm` instead `OpenAI` in langchain.

```python
import os

from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "sk-xxxxxxxx" # can be anything
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"

llms = OpenAI()
```