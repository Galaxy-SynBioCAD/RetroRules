FROM python:3.7

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

WORKDIR home/

RUN wget https://retrorules.org/dl/preparsed/rr02/rp2/hs -O /home/rules_rall_rp2.tar.gz && \
    tar xf /home/rules_rall_rp2.tar.gz -C /home/ && \
    mv /home/retrorules_rr02_rp2_hs/retrorules_rr02_rp2_flat_forward.csv /home/rules_rall_rp2_forward.csv && \
    mv /home/retrorules_rr02_rp2_hs/retrorules_rr02_rp2_flat_retro.csv /home/rules_rall_rp2_retro.csv && \
    mv /home/retrorules_rr02_rp2_hs/retrorules_rr02_rp2_flat_all.csv /home/rules_rall_rp2.csv && \
    rm -r /home/retrorules_rr02_rp2_hs && \
    rm /home/rules_rall_rp2.tar.gz

COPY rpTool.py /home/
COPY galaxy_tool/tool_RetroRules.py /home/
