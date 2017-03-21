while read line; do
   curl -H"X-FullContact-APIKey:$FULLCONTACT_KEY" "https://api.fullcontact.com/v2/person.json?email=$line" | grep "twitter.com" | cut -d '/' -f 4 | sed 's/",/\n/' >> list_of_handles.txt
done <list_of_emails.txt

