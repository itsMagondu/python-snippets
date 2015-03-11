x = '''
There are names of 16 books of the Bible hidden in the passage below. A preacher used 20 minutes to find 15 of them; it took him 3 weeks to find the last one. See how long it would take you, if you could identify them! 
I once made a remark about the hidden books of the Bible. It was a lulu, kept people looking so hard for the facts and for others it was a reveation. Some were in a jam, especially since the names of the books were not capitalized. But the truth finally struck home to numbers of our readers. To others it was a real job. We want it to be a most fascinating few moments for you. Yes, there will be some really easy ones to spot. Others may require judges to help find them. I will quickly admit it usually takes a minister to find one of them, and there will be loud lamentations when it is found. A lady says she brews a cup of tea so that she can concentrate better. See how well you can compete. Relax now, for there really are sixteen names of books of the Bible in this passage. Look them up. There you are...start thinking/ looking. I found them all. Send back a reply
'''

x = x.replace(' ','').replace('\n','').replace(';','').replace('.','').replace('!','')
x= x.replace('/','').replace(',','').lower()

numbers = ['0','1','2','3']
books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers ', 'Deuteronomy', 'Joshua', 'Judges', 'Psalms', 'Ruth', '1Samuel', '2Samuel', 'Job', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Hosea ', 'Joel ', 'Amos', 'Obadiah', 'Jonah ', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', '1Kings', '2Kings', '1Chronicles', '2Chronicles', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Danie', 'Ezra', 'Nehemiah', 'Esther', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', '1Thessalonians ', '2Thessalonians', '1Corinthians ', '2Corinthians', 'Romans   ', 'Luke', 'Galatians', 'Ephesians ', 'Philippians', 'Colossians ', 'Philemon', 'Acts', '1Timothy', '2Timothy', 'Titus', 'Hebrews', 'James', 'Jude', '1Peter ', '2Peter', 'Mark', 'John', '1John ', '2John', '3John', 'Revelation']

for item in books:
    [item.strip(s) for s in numbers]
    item = item.lower().strip()
    if item in x:
        x = x.replace(item,item.upper())
        print item

print x
