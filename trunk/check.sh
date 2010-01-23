for x in `ps ax | grep ./manage.py\ check | awk {'print $1'}`
do
	echo 'kill '$x
	kill $x
done
./manage.py check
