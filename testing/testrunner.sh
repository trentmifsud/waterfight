#!/bin/bash
filename='testdata.csv'
url='http://127.0.0.1:5000/game'
n=1
while read line; do
# reading each line
echo "Test No. $n "
n=$((n+1))
curl -d "$line" -H "Content-Type: application/json" -X POST -w "\n" $url
done < $filename