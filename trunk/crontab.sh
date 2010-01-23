echo '0,30 * * * * cd '`pwd`' && ./check.sh' > crontab.temp~
crontab crontab.temp~
rm crontab.temp~
