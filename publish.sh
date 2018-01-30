#!/usr/bin/env bash
#

GSUTIL="lib/google-cloud-sdk/bin/gsutil"

if [ "$(uname)" == "Darwin" ]; then
    GCSDK="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-148.0.1-darwin-x86_64.tar.gz"
fi

if [ ! -f $GSUTIL ]; then
    echo "Installing Google Cloud SDK..."
    curl $GCSDK | tar -xz -C lib
fi

if [ ! -d "build" ]; then
    echo "Build does not exist. Run 'gulp build'."
else
    echo "Publishing build..."
    $GSUTIL -m rsync -x 'ref/*' -rd build gs://defold-doc
fi
