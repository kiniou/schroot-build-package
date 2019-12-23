FROM debian:buster-slim

RUN apt-get update -y && apt-get install --no-install-recommends -y \
  distro-info-data \
  schroot \
  debootstrap \
  python3.7 \
  python3-pip \
  && python3 -m pip install -U -I pip setuptools \
  && rm /usr/bin/pip3 \
  # Cleanup docs
  && rm -rf /usr/share/doc/* /usr/share/man/* \
  # Cleanup apt cache
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./setup.py ./setup.cfg ./README.md /usr/src/app/
COPY ./schroot_build_package /usr/src/app/schroot_build_package
RUN \
  export PBR_VERSION=$(python3 -c "import schroot_build_package; print(schroot_build_package.__version__)") \
  && pip install -e .

CMD sbp
