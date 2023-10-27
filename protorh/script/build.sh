pip3 install -r requirements.txt --break-system-packages
brew services start postgresql
createdb protorh
psql -d protorh -U app -a -f database_rh.psql
brew services stop postgresql