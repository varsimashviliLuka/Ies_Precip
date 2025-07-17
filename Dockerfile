FROM python:3.11.1-slim

# სამუშაო დირექტორია
WORKDIR /app

# აპლიკაციის კოდის კოპირება
COPY . .

# მოთხოვნილებების ინსტალაცია
RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install python3-dev gcc build-essential
RUN pip install -r requirements.txt

RUN chmod +x /app/flask_app.sh
RUN chmod +x /app/run_scheduler.sh

# საჭირო იქნება, რომ გადაიტანოთ ლოგების ფაილი
RUN mkdir -p /app/logs

# 5000 პორტის გახსნა
EXPOSE 5000

CMD ["sh", "-c", "./run_scheduler.sh & uwsgi uwsgi.ini"]
