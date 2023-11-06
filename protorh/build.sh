pip3 install -r requirements.txt --break-system-packages
brew services start postgresql
createdb protorh -U ilyes
psql -d protorh -f database_rh.psql
psql -U ilyes --password -d protorh
#psql -U ilyes --password -d protorh