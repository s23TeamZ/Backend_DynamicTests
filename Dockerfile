FROM ubuntu:20.04

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -qq update \
    && apt-get -qq install -y python3 python3-pip ffmpeg libsm6 libxext6
ARG DEBIAN_FRONTEND=noninteractive

RUN echo "===> Installing system dependencies..." && \
    BUILD_DEPS="curl unzip" && \
    apt-get update && apt-get install --no-install-recommends -y \
    wget \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 libgbm1 libu2f-udev \
    $BUILD_DEPS \
    xvfb  wdiff && \
    \
    echo "===> Installing chromedriver and google-chrome..." && \
    CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/bin && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver_linux64.zip && \
    \
    CHROME_SETUP=google-chrome.deb && \
    wget -O $CHROME_SETUP "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    dpkg -i $CHROME_SETUP && \
    apt-get install -y -f && \
    rm $CHROME_SETUP && \
    \
    \
    echo "===> Remove build dependencies..." && \
    apt-get remove -y $BUILD_DEPS && rm -rf /var/lib/apt/lists/*
# echo "===> Installing BrowserMob Proxy..." && \
    # wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip && \
    # unzip && \
    # cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs && \
    # rm phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    # \
    # \
WORKDIR /app
RUN mkdir "downloads_folder"
RUN mkdir "websites_html"
COPY websites_html/ websites_html/
RUN echo "===> Installing python dependencies..."
COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

COPY main.py .
COPY browser_func.py .
COPY ublock_origin_1_48_0_0.crx .

# CMD tail -f /dev/null
# CMD python3 example.py
EXPOSE 7077
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7077", "--workers", "1"]