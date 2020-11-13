#!/bin/bash

cd ~/Projects/Others/videoAUTO/News/$(date +"%Y-%m-%d")/Images

for f in *;
do
    cd "$f";
    for img in *;
    do
        if [[ ${img: -1} =~ [1-9] ]]; then
            mv $img ${img: -1}${img: 0: -2}
        else
            :
        fi
    done
    cd ..;
done
