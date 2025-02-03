# 나만의 모델 만들기

## 필요한 pip 패키지 다운

```shell
pip install huggingface_hub
```

```python
###### 필요 디렉토리에서 아래의 .py파일로 모델을 다운받습니다!!#######

from huggingface_hub import snapshot_download
model_id= "MLP-KTLim/llama-3-Korean-Bllossom-8B"
snapshot_download(repo_id=model_id, local_dir="bllossom",
local_dir_use_symlinks=False, revision="main")
#####################################################################
```

## gguf 만들기위한 llama.cpp파일 다운

```shell
git clone https://github.com/ggerganov/llama.cpp.git
```

## llama.cpp의 필요 환경 설치

```shell
pip install -r llama.cpp/requirements.txt
## cd llama.cpp
## make
```

## gguf 만들기 시작!!!

llama.cpp/convert-hf-to-gguf.py 파일을 기반으로,
bllossom/ 에 있는 파일들을
--outfile bllossom.gguf 로 만들어줍니다!!

```shell
python llama.cpp/convert_hf_to_gguf.py bllossom/ --outfile bllossom.gguf

python llama.cpp/convert_llama_ggml-to_gguf.py bllossom/ --outfile bllossom.gguf
```

## 이제,gguf 기반으로 ollama를 실행해보겠습니다!!

우선 gguf가 있는 디렉토리에 "Modelfile" 라는 이름으로 아래와 같이 파일을 만듭니다!!

```text
FROM bllossom.gguf

TEMPLATE """{{- if .System }}
<s>{{ .System }}</s>
{{- end }}
<s>Human:
{{ .Prompt }}</s>
<s>Assistant:
"""

SYSTEM """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."""

PARAMETER temperature 0
PARAMETER num_predict 3000
PARAMETER num_ctx 4096
PARAMETER stop <s>
PARAMETER stop </s>
```

## 그다음으로!! ollama가 실행된 상테에서 아래와 같이 create해줍니다!!

```shell
ollama create bllossom-8B -f Modelfile
```

## 드디어완성!! 이제 model run 을해줘볼까요~?

```shell
ollama run bllossom-8B
```
