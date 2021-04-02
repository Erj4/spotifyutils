FROM python:3.8-alpine
WORKDIR /spotifyutils
COPY . .
RUN pip3 install .
ENV PATH=/spotifyutils/.local/bin:$PATH