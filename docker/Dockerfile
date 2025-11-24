# syntax=docker/dockerfile:1
FROM hub.infervision.com/algo/starship_pip:2.3.2
WORKDIR /service

# Custom ct_chest dockerfile content
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib/python3.11/site-packages/bw_ocean/objmatch"
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib/python3.11/site-packages/torch/lib"
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib/python3.11/site-packages/vtkmodules"
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"
ENV MXNET_CUDNN_AUTOTUNE_DEFAULT=0

COPY ./pyproject.toml ./poetry.lock  ./
# onnxruntime-gpu安装有很奇怪的操作，但只能这么干
RUN echo "[global]" > /etc/pip.conf && \
    echo "index-url = https://repos.infervision.com/repository/pypi/simple" >> /etc/pip.conf && \
    # 解决容器内OpenGL版本低的问题
    echo '{ "file_format_version" : "1.0.0", "ICD" : { "library_path" : "libEGL_nvidia.so.0" } }' > /usr/share/glvnd/egl_vendor.d/10_nvidia.json
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
RUN echo Y | pip uninstall onnxruntime && \
    pip install ivtk-onnxruntime-gpu==1.10.0 -i https://repos.infervision.com/repository/pypi/simple && \
    echo Y | pip uninstall ivtk-onnxruntime-gpu && \
    pip install ivtk-onnxruntime-gpu==1.10.0 -i https://repos.infervision.com/repository/pypi/simple
RUN rm -f pyproject.toml poetry.lock

COPY ./ ./
# Custom end

ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"

RUN wget https://repos.infervision.com/repository/raw-local/nvvm_d.tar && \
    mkdir -p /usr/local/cuda/nvvm && \
    tar -xvf nvvm_d.tar -C /usr/local/cuda/nvvm &&  \
    rm -f nvvm_d.tar

RUN pip install decrypt==2.3 -i https://repos.infervision.com/repository/pypi/simple

CMD ["python", "run.py"]
