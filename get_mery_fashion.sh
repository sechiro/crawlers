#!/bin/bash
set -ue
script_dir=$(cd $(dirname $0);pwd)

#DATE=`date "+%Y-%m-%dT%H:%M:%SZ"`
DATE=`date "+%Y%m%d"`
SPIDER=mery-fashion
DATA_DIR=$script_dir/data
OUTPUT_FILE=$DATA_DIR/${SPIDER}-${DATE}
scrapy crawl $SPIDER -o $OUTPUT_FILE
