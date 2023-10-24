pip3 install -r requirements.txt --break-system-packages

psql
createuser jawa with password '123'
brew services start postgresql
createdb ProtoRH -U jawa
psql -U jawa --password -d ProtoRH
brew services stop postgresql