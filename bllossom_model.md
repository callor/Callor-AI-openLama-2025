# Bllossom 모델 ollama 에서 실행하기기

## https://huggingface.co/ 페이지의 모델 소개내용

```text
저희 Bllossom팀 에서 한국어-영어 이중 언어모델인 Bllossom을 공개했습니다!
서울과기대 슈퍼컴퓨팅 센터의 지원으로 100GB가넘는 한국어로 모델전체를 풀튜닝한 한국어 강화 이중언어 모델입니다!
한국어 잘하는 모델 찾고 있지 않으셨나요?
 - 한국어 최초! 무려 3만개가 넘는 한국어 어휘확장
 - Llama3대비 대략 25% 더 긴 길이의 한국어 Context 처리가능
 - 한국어-영어 Pararell Corpus를 활용한 한국어-영어 지식연결 (사전학습)
 - 한국어 문화, 언어를 고려해 언어학자가 제작한 데이터를 활용한 미세조정
 - 강화학습
이 모든게 한꺼번에 적용되고 상업적 이용이 가능한 Bllossom을 이용해 여러분 만의 모델을 만들어보세욥!
무려 Colab 무료 GPU로 학습이 가능합니다. 혹은 양자화 모델로 CPU에올려보세요 [양자화모델](https://huggingface.co/MLP-KTLim/llama-3-Korean-Bllossom-8B-4bit)

1. Bllossom-8B는 서울과기대, 테디썸, 연세대 언어자원 연구실의 언어학자와 협업해 만든 실용주의기반 언어모델입니다! 앞으로 지속적인 업데이트를 통해 관리하겠습니다 많이 활용해주세요 🙂
2. 초 강력한 Advanced-Bllossom 8B, 70B모델, 시각-언어모델을 보유하고 있습니다! (궁금하신분은 개별 연락주세요!!)
3. Bllossom은 NAACL2024, LREC-COLING2024 (구두) 발표로 채택되었습니다.
4. 좋은 언어모델 계속 업데이트 하겠습니다!! 한국어 강화를위해 공동 연구하실분(특히논문) 언제든 환영합니다!!
   특히 소량의 GPU라도 대여 가능한팀은 언제든 연락주세요! 만들고 싶은거 도와드려요.
```

## 최신버전 다운로드 링크

https://huggingface.co/MLP-KTLim/llama-3-Korean-Bllossom-8B

## 양자화된 CPU 버전 링크

https://huggingface.co/MLP-KTLim/llama-3-Korean-Bllossom-8B-4bit

## 모델 생성하기

이 환경은 python 3+, 아나콘다 등이 설치된 환경에서 운영한다

### 필요한 pip 패키지 다운로드하여 설치한다

```shell
pip install huggingface_hub
```

임의의 작업 폴더에 `install.py` 파일을 생성하고 아래 코드를 복사 붙여넣기 한다

```python
###### 필요 디렉토리에서 아래의 .py파일로 모델을 다운받습니다!!#######

from huggingface_hub import snapshot_download
model_id= "MLP-KTLim/llama-3-Korean-Bllossom-8B"
snapshot_download(repo_id=model_id, local_dir="bllossom",
local_dir_use_symlinks=False, revision="main")
#####################################################################
```

shell 프롬프트에서 `install.py` 파일을 실행한다
파일들을 다운로드 받는데 많은 시간이 소요되므로 인내심을 갖고 기다린다

```shell
python ./install.py
```

## gguf 만들기위한 llama.cpp파일 다운

```shell
git clone https://github.com/ggerganov/llama.cpp.git
```

## llama.cpp의 필요 환경 설치

환경설정을 하고 _.cpp 파일을 생성하는 과정이 있으나, 현시점(2025.2.3) _.cpp 파일 컴파일 작업이 필요 없다.

다음명령으로 python 환경만 실행하자

```shell
pip install -r llama.cpp/requirements.txt
```

## gguf 만들기

llama.cpp/convert-hf-to-gguf.py 파일을 기반으로,
bllossom/ 에 있는 파일들을 --outfile bllossom.gguf 로 만들어준다.

상당한 시간이 필요하므로 인내심을 갖고 기다려야 한다

```shell
python llama.cpp/convert_hf_to_gguf.py bllossom/ --outfile bllossom.gguf
```

## 이제,gguf 기반으로 ollama를 실행해 보자

우선 gguf가 있는 디렉토리에 "Modelfile" 라는 이름으로 파일을 생성하고 아래 코드를 복사 붙이기 한다

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

### 다음 명령으로 ollama 에서 사용가능한 모델을 생성한다

이 과정도 상당한 시간이 소요된다

```shell
ollama create bllossom-8B -f Modelfile
```

## 드디어완성!! 이제 model run 을 해 보자

```shell
ollama run bllossom-8B
```
