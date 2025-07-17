#!/bin/bash

# Forbidden internal terms (obfuscated for privacy)
FORBIDDEN_TERMS=("word1" "word2" "word3" "word4")

# Files staged for commit
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|txt|md|csv|xml|xlsx|xls)$')

EXIT_CODE=0

for FILE in $FILES; do
  for TERM in "${FORBIDDEN_TERMS[@]}"; do
    if grep -n -i "$TERM" "$FILE" > /dev/null; then
      echo "❌ Forbidden term '$TERM' found in file: $FILE"
      grep -n -i "$TERM" "$FILE"
      EXIT_CODE=1
    fi
  done
done

exit $EXIT_CODE