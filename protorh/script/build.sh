pip3 install -r requirements.txt --break-system-packages
brew services start postgresql
psql -d protorh -f database_rh.psql
brew services stop postgresql