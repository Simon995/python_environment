SHELL := /bin/bash

MODEL_NAME=ct_radiology_$(MODEL_VERSION)

PREFIX_URL=172.30.0.54:/volume1/数据使用/模型工程封装/放射科工程封装

MODEL_URL=$(PREFIX_URL)/模型参数文件/$(MODEL_NAME)
DATA_URL=$(PREFIX_URL)/数据文件/测试数据/

INPUT_PATH=data/input
OUTPUT_PATH=data/output
MODEL_PATH=model

GPU=1

run: prepare
	. add_env.sh; \
	python example/main.py \
	--gpus=$(GPU) \
	--input_path=$(INPUT_PATH) \
	--output_path=$(OUTPUT_PATH) \
	--model_path=$(MODEL_PATH)/$(MODEL_NAME)

prepare: check
	if [ ! -e $(MODEL_PATH)/$(MODEL_NAME) ] ; then \
		echo "Downloading model..."; \
		mkdir -p $(MODEL_PATH); \
		rsync -avP $(USER_NAME)@$(MODEL_URL) $(MODEL_PATH);\
	fi
	if [ ! -d $(INPUT_PATH) ]; then \
		echo "Downloading input data..."; \
		mkdir -p $(INPUT_PATH); \
		rsync -avP $(USER_NAME)@$(DATA_URL) $(INPUT_PATH); \
	fi
	if [ ! -d $(OUTPUT_PATH) ]; then \
		mkdir -p $(OUTPUT_PATH); \
	fi

check:
ifeq ($(strip $(USER_NAME)), )
		echo "USER_NAME cannot be empty."
		false
endif
ifeq ($(strip $(MODEL_VERSION)), )
		echo "MODEL_VERSION cannot be empty, like 'm0.0.1'"
		false
endif
		echo "welcome $(USER_NAME), model name is $(MODEL_NAME)"
