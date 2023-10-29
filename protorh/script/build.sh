pip3 install -r requirements.txt --break-system-packages
brew services start postgresql
createdb protorh -U app
psql -d protorh -f database_rh.psql
#psql -U app --password -d protorh -f database_rh.psql
brew services stop postgresql