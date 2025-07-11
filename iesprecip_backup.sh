#!/bin/bash

# -------- LOAD .env VARIABLES --------
ENV_FILE="/home/iesflask/Ies_Precip/.env"

if [ -f "$ENV_FILE" ]; then
    set -o allexport
    source "$ENV_FILE"
    set +o allexport
else
    echo "❌ .env ფაილი არ მოიძებნა: $ENV_FILE"
    exit 1
fi

# -------- MYSQL BACKUP --------

DB_BACKUP_PATH="/flask_app/backups/Ies_Precip/databases"
DATE=$(date +"%Y%m%d")
SQL_FILE="${DB_BACKUP_PATH}/${MYSQL_DATABASE}_backup_${DATE}.sql"
LOG_FILE="${DB_BACKUP_PATH}/${MYSQL_DATABASE}_backup_${DATE}.log"

# შექმენით ბექაფის დირექტორია, თუ არ არსებობს
mkdir -p "$DB_BACKUP_PATH"

# შექმენით ბექაფის ლოგ ფაილი
{
    echo "📅 ბექაფის დაწყება: $(date)"
    
    # MySQL ბექაფის შექმნა Docker კონტეინერიდან
    docker exec "$MYSQL_CONTAINER_NAME" \
        mysqldump -u "$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" > "$SQL_FILE"

    if [ $? -eq 0 ]; then
        echo "✅ MySQL ბექაფი წარმატებით დასრულდა: $SQL_FILE"
    else
        echo "❌ ბექაფის შეცდომა!"
        rm -f "$SQL_FILE"  # წაშალე დაზიანებული SQL ფაილი
        exit 2
    fi
} >> "$LOG_FILE" 2>&1

# ძველი ბექაფებისა და მათი ლოგების წაშლა (მხოლოდ 7 ახალი დატოვოს)
find "$DB_BACKUP_PATH" -name "${MYSQL_DATABASE}_backup_*.sql" -mtime +7 | while read OLD_SQL; do
    OLD_LOG="${OLD_SQL%.sql}.log"
    echo "🗑️ წაშლა: $OLD_SQL" >> "$LOG_FILE"
    rm -f "$OLD_SQL"
    [ -f "$OLD_LOG" ] && rm -f "$OLD_LOG"
done

# -------- DONE --------
echo "🎉 ყველა ბექაფი წარმატებით დასრულდა: $(date)" >> "$LOG_FILE"
