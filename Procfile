web: bundle exec unicorn -p $PORT -c ./config/unicorn.rb
web: uvicorn api:app --host=0.0.0.0 --port=${PORT:8000}
