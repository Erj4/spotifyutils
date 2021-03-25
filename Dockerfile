FROM python:3.8
WORKDIR /spotifyutils
COPY . .
RUN pip3 install .
ENV PATH=/spotifyutils/.local/bin:$PATH