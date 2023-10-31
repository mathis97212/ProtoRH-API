pip3 install -r requirements.txt --break-system-packages
apt services start postgresql
createdb protorh -U app
psql -d protorh -f database_rh.psql
#psql -U app --password -d protorh -f database_rh.psql
apt services stop postgresql