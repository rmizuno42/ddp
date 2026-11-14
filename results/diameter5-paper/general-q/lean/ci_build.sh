#!/usr/bin/env bash
# Build the Lean project one module at a time (to bound memory), record the time and
# peak memory of each module, and report failures as GitHub annotations so that they
# can be read without access to the raw logs.
set -u
cd "$(dirname "$0")"

enc() {  # encode text for a GitHub workflow command
  local s
  s=$(cat)
  s=${s//'%'/'%25'}
  s=${s//$'\r'/'%0D'}
  s=${s//$'\n'/'%0A'}
  printf '%s' "$s"
}

mods="DDPGeneralQ.Basic DDPGeneralQ.Good DDPGeneralQ.Codes DDPGeneralQ.Checks DDPGeneralQ.Instances"
for f in DDPGeneralQ/Charts/*.lean; do
  mods="$mods DDPGeneralQ.Charts.$(basename "$f" .lean)"
done
mods="$mods DDPGeneralQ.LargePrimes DDPGeneralQ.Main DDPGeneralQ"

mkdir -p ci-logs
status=0
summary=""
for m in $mods; do
  start=$(date +%s)
  if [ -x /usr/bin/time ]; then
    timer=(/usr/bin/time -v -o "ci-logs/$m.time")
  else
    timer=()
  fi
  if "${timer[@]}" lake build "$m" > "ci-logs/$m.log" 2>&1; then
    ok=ok
  else
    ok=FAILED
    status=1
    tail -n 60 "ci-logs/$m.log" | enc | sed "s/^/::error title=$m failed::/"
    echo
  fi
  secs=$(( $(date +%s) - start ))
  rss=$(awk -F': ' '/Maximum resident set size/ {printf "%d", $2/1024}' "ci-logs/$m.time" 2>/dev/null)
  line="$m: $ok, ${secs}s, peak ${rss:-?} MB"
  echo "$line"
  summary="$summary$line"$'\n'
done

summary="$summary$(free -m | head -3)"$'\n'"$(df -h / /mnt 2>/dev/null)"
printf '%s' "$summary" | enc | sed 's/^/::notice title=Lean build summary::/'
echo
exit $status
