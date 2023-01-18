#!sh
set -e
d=$(dirname "$0")
for f in $d/hl3/*.hl3
do
  name=$(basename $f)
  out=${f%.hl3}.out
  python3 $d/../hl3_compiler.py < $f | python3 $d/../lambda_interpreter.py | diff $out -
  echo $name ok
done
