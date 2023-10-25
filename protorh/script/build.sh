brew install postgresql
brew install python3
brew install pip3
pip3 install -r requirements.txt --break-system-packages
brew services start postgresql
createdb ProtoRH
psql -d ProtoRH -U mathisdiallo-themista -a -f database_rh.psql
brew services stop postgresql