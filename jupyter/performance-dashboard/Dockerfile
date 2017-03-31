FROM jupyter/scipy-notebook

USER root

RUN conda install --quiet --yes \
    pymongo plotly pytables ipywidgets \
    && conda clean -tipsy

RUN mkdir -p /notebooks
COPY *.ipynb /notebooks/
COPY schema.py /notebooks/
COPY start-singleuser.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/start-singleuser.sh

USER $NB_USER
