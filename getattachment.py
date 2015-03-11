import imaplib
import email
import os

svdir = '/tmp/'


mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login("username","password")
mail.select("[Gmail]/All Mail")	

print "Logged in"

#typ, msgs = mail.search(None, 'UNSEEN','FROM','(SUBJECT "Jamaica)')
#msgs = msgs[0].split()

resp, msgs = mail.search(None, 'UNSEEN','FROM')#'UNSEEN') # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
msgs = msgs[0].split() # getting the mails id

print msgs
for emailid in msgs:
    print emailid	
    resp, data = mail.fetch(emailid, "(RFC822)")
    email_body = data[0][1] 
    m = email.message_from_string(email_body)


    if m.get_content_maintype() != 'multipart':
        continue

    print "["+m["From"]+"] :" + m["Subject"]

    for part in m.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename=part.get_filename()
        if filename is not None:
            sv_path = os.path.join(svdir, filename)
            if not os.path.isfile(sv_path):
                print sv_path       
                fp = open(sv_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
