pip3 install -r requirements.txt --break-system-packages

psql
CREATE USER mathisdiallo-themista WITH PASSWORD '123'
brew services start postgresql
createdb ProtoRH -U mathisdiallo-themista
psql -U mathisdiallo-themista --password -d ProtoRH
brew services stop postgresql